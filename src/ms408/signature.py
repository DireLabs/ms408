"""Public evaluator — run *your* hypothesis through the MS408 discriminator battery.

This is the one entry point a stranger needs. Give it a list of word tokens (your
cipher output, a generator's output, a transliteration variant, a candidate plaintext
rendering, ...) and it reports, for each statistical axis, your value, the Voynich
manuscript's reference band, and whether you land inside it — **with the honest caveat
for that axis travelling attached**, so no number can be quoted without its hedge.

    from ms408 import evaluate
    verdict = evaluate(open("my_tokens.txt").read().split())

Design contract (why this file exists rather than importing the experiments directly):

  * `axis_values()` is the SINGLE canonical computation of every axis. The reference-band
    builder (`ms408.experiments.e32_reference_bands`) calls THIS function on the VMS, so a
    user's value and the band it is checked against are computed by identical code — no
    drift. If you change an axis here, rebuild the bands.
  * Nothing here estimates or recalls a number (L3 firewall). The bands come from the
    committed artifact `ms408/data/reference_bands.json`, produced by the builder script,
    which records its own git commit, params, and VMS dataset. If that file is missing,
    `evaluate()` refuses rather than inventing a band.
  * The two mid-level syntax axes are reported in BOTH a global-null form (confounded by
    section/topic vocabulary drift — E22) and a deconfounded within-block-null form (E31);
    both are flagged `soft` because the VMS's own subsample CI crosses zero. The word-order
    axis dI is flagged as homophony/respacing-confounded (E29). These flags are not
    decoration — they are the anti-over-claim discipline, encoded.

The statistical evaluator here is cold and deterministic. The project's *adversarial
refutation* protocol (docs/METHODOLOGY.md) is a separate, human-run discipline using a
fallible LLM — it is not in this file and is not an oracle. See docs/LIMITS.md.
"""

from __future__ import annotations

import json
import random
from importlib import resources

from .experiments.e13b_function_content import _gap
from .experiments.e14_word_classes import _adjacent_class_nmi
from .experiments.mid_level_null import null_z, order_shuffle
from .studies.encoding import profile

SEED = 408
N_NULL = 20          # null replicates per syntax z (matches E31 hardening)
BLOCK = 250          # within-block local-shuffle block (E31 deconfounding null)
WEAK_Z = 3.0         # legacy one-sided "weak syntax" reference threshold (E19)
REFERENCE_TOKENS = 10_000   # the token budget the VMS bands are built at (e32)
MIN_TOKENS = 1_000   # below this the axes are unreliable / undefined; evaluate() refuses
LOW_BUDGET_TOKENS = 8_000   # below this, axes (esp. ttr) are not comparable to the bands

# Axes carried by evaluate(), in report order, each with its standing caveat. The caveat
# text is the honest hedge for that axis; it ships with every verdict.
AXES = {
    "h2": "Lindemann-Bowern conditional character entropy (space included).",
    "dI": "Montemurro-Zanette word-order information. CONFOUNDED: collapses under "
          "homophony and under re-spacing alone (E29) — a homophony/type-token detector, "
          "not a clean word-order measure. In-band here is weak evidence.",
    "ed1": "Edit-distance-1 morphology main-component share.",
    "zipf": "Zipf rank-frequency slope.",
    "ttr": "Type-token ratio. ADVISORY: intrinsically token-count-sensitive (fewer tokens "
           "-> higher TTR), so it is not banded and not counted. Only compare at a similar "
           "token budget to the VMS reference (see band_provenance.vms_full_point).",
    "fc_z_local": "Function/content collocation-gap z vs a WITHIN-BLOCK null (deconfounded "
                  "of topic drift; E31). SOFT: the VMS's own subsample CI crosses zero.",
    "wc_z_local": "Adjacent word-class NMI z vs a WITHIN-BLOCK null (deconfounded; E31). "
                  "SOFT: the VMS's own subsample CI crosses zero.",
    "fc_z_global": "Function/content collocation-gap z vs a GLOBAL order-shuffle null "
                   "(E19). CONFOUNDED by section/topic vocabulary drift (E22) — compare to "
                   "fc_z_local to see the drift share.",
    "wc_z_global": "Adjacent word-class NMI z vs a GLOBAL order-shuffle null (E19). "
                   "CONFOUNDED by section/topic vocabulary drift (E22).",
}
SOFT_AXES = frozenset({"fc_z_local", "wc_z_local", "fc_z_global", "wc_z_global"})
CONFOUNDED_AXES = frozenset({"dI", "fc_z_global", "wc_z_global"})
TOKEN_SENSITIVE_AXES = frozenset({"ttr"})
# Hard axes (counted): everything not soft, not confounded, not token-sensitive.
HARD_AXES = frozenset(AXES) - SOFT_AXES - CONFOUNDED_AXES - TOKEN_SENSITIVE_AXES


def _local_shuffle(tokens: list, block: int, seed: int) -> list:
    """Shuffle WITHIN fixed blocks: preserves each block's vocabulary (topic/section
    composition), destroys local adjacency. The deconfounded null (E31)."""
    rng = random.Random(seed)
    out: list = []
    for i in range(0, len(tokens), block):
        chunk = tokens[i:i + block]
        rng.shuffle(chunk)
        out.extend(chunk)
    return out


def _fc_z(tokens: list, null_fn, seed: int) -> float | None:
    obs = _gap(tokens)
    if obs.get("insufficient"):
        return None
    nulls = [_gap(null_fn(tokens, seed + i)).get("gap") for i in range(N_NULL)]
    z = null_z(obs["gap"], [g for g in nulls if g is not None])["z"]
    return None if z is None else round(z, 2)


def _wc_z(tokens: list, null_fn, seed: int) -> float | None:
    obs = _adjacent_class_nmi(tokens, seed)
    nulls = [_adjacent_class_nmi(null_fn(tokens, seed + 1 + i), seed + 1 + i)
             for i in range(N_NULL)]
    z = null_z(obs, nulls)["z"]
    return None if z is None else round(z, 2)


def _glob(t, s):
    return order_shuffle(t, s)


def _loc(t, s):
    return _local_shuffle(t, BLOCK, s)


def axis_values(tokens: list, seed: int = SEED) -> dict:
    """Canonical computation of every discriminator axis for a token list.

    Deterministic given `seed`. The reference-band builder and evaluate() both call this,
    so a user's value and its band are always computed by identical code.

    Refuses inputs below MIN_TOKENS: several axes (the MZ word-order scan, the mid-level
    syntax z's) are undefined or unstable on short streams, and the bands are built at
    REFERENCE_TOKENS — so a tiny sample would either crash or, worse, report a confident
    but meaningless verdict. See docs/LIMITS.md.
    """
    if len(tokens) < MIN_TOKENS:
        raise ValueError(
            f"evaluate needs at least {MIN_TOKENS} word tokens (the reference bands are built "
            f"at {REFERENCE_TOKENS}); got {len(tokens)}. Short streams leave several axes "
            f"undefined — see docs/LIMITS.md."
        )
    p = profile(tokens)
    return {
        "tokens": p["tokens"],
        "types": p["types"],
        "h2": round(p["h2"], 4),
        "dI": round(p["mz_peak_value"], 4),
        "ed1": round(p["ed1_main_component"], 4),
        "zipf": None if p["zipf_slope"] is None else round(p["zipf_slope"], 4),
        "ttr": round(p["type_token_ratio"], 4),
        "mz_peak_scale": p["mz_peak_scale"],
        "fc_z_local": _fc_z(tokens, _loc, seed),
        "wc_z_local": _wc_z(tokens, _loc, seed),
        "fc_z_global": _fc_z(tokens, _glob, seed),
        "wc_z_global": _wc_z(tokens, _glob, seed),
    }


def vms_bands() -> dict:
    """Load the committed VMS reference-band artifact (built by the e32 script).

    Raises with a clear instruction rather than fabricating a band if it is absent —
    the firewall applies to the tool as much as to the research.
    """
    try:
        raw = resources.files("ms408.data").joinpath("reference_bands.json").read_text()
    except (FileNotFoundError, ModuleNotFoundError) as exc:
        raise FileNotFoundError(
            "ms408/data/reference_bands.json is missing. Build it with:\n"
            "    python -m ms408.experiments.e32_reference_bands\n"
            "(needs the acquired VMS transliteration; run `python -m ms408.acquire` first)."
        ) from exc
    return json.loads(raw)


def evaluate(tokens: list, seed: int = SEED) -> dict:
    """Evaluate a token stream against the VMS discriminator bands.

    Returns a verdict dict: per-axis value / band / in_band with the axis caveat attached,
    a hard-axis and soft-axis match count, and top-level notes. The caveats travel with the
    verdict by construction, so it cannot be quoted without its hedges.
    """
    av = axis_values(tokens, seed)
    bands = vms_bands()
    band_axes = bands["axes"]
    out_axes: dict = {}
    hard_in = hard_n = 0
    for axis, caveat in AXES.items():
        value = av.get(axis)
        spec = band_axes.get(axis)
        band = spec["band"] if spec else None
        in_band = (
            None if value is None or band is None
            else bool(band[0] <= value <= band[1])
        )
        entry = {
            "value": value,
            "band": band,
            "in_band": in_band,
            "soft": axis in SOFT_AXES,
            "confounded": axis in CONFOUNDED_AXES,
            "token_sensitive": axis in TOKEN_SENSITIVE_AXES,
            "caveat": caveat,
        }
        if spec and spec.get("method"):
            entry["band_method"] = spec["method"]
        out_axes[axis] = entry
        if axis in HARD_AXES and in_band is not None:
            hard_n += 1
            hard_in += int(in_band)

    soft_in = sum(
        1 for a in SOFT_AXES if out_axes[a]["in_band"]
    )
    notes = [
        "Matching the VMS on these axes is NECESSARY, not sufficient: it means your "
        "hypothesis is not excluded, NOT that it is the manuscript's mechanism (L7).",
        "Hard-axis count excludes the confounded (dI, *_global) and soft (*_local) axes. "
        "A soft axis in-band is weak evidence — its VMS-side CI crosses zero.",
        "dI is homophony/respacing-confounded (E29); do not read an in-band dI as intact "
        "word order.",
        f"Reference bands: {bands['meta']['method']} (built at commit "
        f"{bands['meta'].get('git_commit', '?')[:10]}). See docs/LIMITS.md.",
    ]
    if av["tokens"] < LOW_BUDGET_TOKENS:
        notes.insert(0, (
            f"LOW TOKEN BUDGET: {av['tokens']} tokens is well below the reference budget "
            f"({REFERENCE_TOKENS}); axes (especially ttr and the CIs) are not strictly "
            f"comparable to the bands. Evaluate near {REFERENCE_TOKENS} tokens where possible."
        ))
    return {
        "axes": out_axes,
        "hard_axes_in_band": hard_in,
        "hard_axes_total": hard_n,
        "soft_axes_in_band": soft_in,
        "soft_axes_total": len(SOFT_AXES),
        "band_provenance": bands["meta"],
        "notes": notes,
    }


def format_verdict(verdict: dict) -> str:
    """Human-readable table of an evaluate() verdict (used by the CLI)."""
    lines = ["axis          value      VMS band                  in-band  flags",
             "-" * 74]
    for axis, e in verdict["axes"].items():
        band = e["band"]
        btxt = f"[{band[0]:>8.3f}, {band[1]:>8.3f}]" if band else "        (no band)      "
        val = "   n/a  " if e["value"] is None else f"{e['value']:>8.3f}"
        ib = "  ?  " if e["in_band"] is None else ("  ✓  " if e["in_band"] else "  ✗  ")
        flags = ",".join(f for f, on in (
            ("soft", e["soft"]), ("confounded", e["confounded"]),
            ("advisory", e.get("token_sensitive")),
        ) if on)
        lines.append(f"{axis:<13} {val}  {btxt}   {ib}   {flags}")
    lines.append("-" * 74)
    lines.append(
        f"hard axes in band: {verdict['hard_axes_in_band']}/{verdict['hard_axes_total']}   "
        f"soft axes in band: {verdict['soft_axes_in_band']}/{verdict['soft_axes_total']}"
    )
    lines.append("")
    for n in verdict["notes"]:
        lines.append(f"note: {n}")
    return "\n".join(lines)
