"""E32 — build the committed VMS reference-band artifact for the public evaluator.

`ms408.evaluate()` checks a user's token stream against Voynich-manuscript reference
bands. Those bands must come from deterministic, versioned code (L3 firewall), not be
hand-typed into the library. This script computes them once and writes:

  * ``src/ms408/data/reference_bands.json`` — the SHIPPED artifact (committed, loaded by
    ``ms408.signature.vms_bands()``); carries its own provenance.
  * ``results/experiments/e32_reference_bands.json`` — the firewall record.

PER-DIALECT SCOPE (D21, resolved 2026-08-13). One band set is built for each Currier
dialect, separately, at the same matched token budget. The previous single band set was
built from ``_sub(A + B, N_TOKENS)``, which — because Currier A alone exceeds the budget —
silently contained only A while claiming to be A+B; Currier B, 68% of the manuscript,
then scored 0-1 of 3 hard axes against it (E34). Since A and B being different generative
regimes is one of this program's own grade-A findings, and L8 requires dialect
stratification everywhere else, the evaluator now stratifies too.

The sampling rule is identical for both dialects — the first ``N_TOKENS`` paragraph
tokens in page order — so the two band sets are like-for-like. A consequence worth
stating: the A band set is byte-identical to the pre-D21 shipped artifact (the old
"A+B" sample WAS ``A[:N_TOKENS]``), so nothing about A changed; B is new. It also means
each dialect's sample is a page-ordered prefix, not a spread sample: A[:10000] is 93% of
A, but B[:10000] is only 44% of B, so B's bands are built on B's earlier folios. E34
re-scores every window of each dialect against its OWN bands and reports the coverage,
which is the check on whether that prefix is representative.

Band construction — subsample WITHOUT replacement throughout (75% of distinct blocks):
  * profile axes (h2, dI, ed1) — 95% CI.
  * syntax axes (fc/wc, local + global) — 90% CI (E31 convention).
  Block-bootstrap WITH replacement is NOT used: duplicate blocks depress TTR, distort the
  Zipf slope, and inject spurious collocation/adjacency — under it the VMS falls outside
  its own TTR/Zipf band (E31 flagged the same duplicate-block bias for the syntax
  measures). Subsampling without replacement avoids it and lands every band on its point.
  * TTR and the ZIPF SLOPE are token-count-sensitive, so a resampled band — computed at
    75% of the budget — would exclude the full-corpus value by construction rather than
    describe it. Both ship as ADVISORY axes (band = null; the reference point, the
    subsample range, and the measured `subsample_bias` are recorded) and neither counts
    toward the hard-axis tally. TTR was known from the start; zipf was added at D23, when
    per-dialect bands put Currier B's own zipf point outside B's own band. The mechanism
    is the fixed [10, 1000] rank window running into the count-saturated tail at 7,500
    tokens; A's bias is small enough to hide inside its CI, B's is 13x larger.
    THE HARD-AXIS TALLY IS THEREFORE OVER 2 AXES (h2, ed1), not 3.

Every axis value is computed by ``ms408.signature.axis_values`` / its helpers, the SAME
code path ``evaluate()`` runs on user input — so a user's value and its band can never
drift apart.

Usage:
    python -m ms408.experiments.e32_reference_bands
"""

from __future__ import annotations

import json
import random
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..signature import BLOCK, N_NULL, SEED, _fc_z, _glob, _loc, _wc_z, axis_values
from ..studies.encoding import profile
from .e13_function_content import N_TOKENS, _sub, _vms_tokens

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
SHIPPED = ROOT / "src" / "ms408" / "data" / "reference_bands.json"

PROFILE_SUBSAMPLE = 120      # subsample-without-replacement reps for profile axes
SYNTAX_SUBSAMPLE = 40        # subsample-without-replacement reps for syntax axes (E31)
KEEP_FRAC = 0.75

PROFILE_AXES = ("h2", "dI", "ed1")           # banded, duplicate-safe
ADVISORY_AXES = ("zipf", "ttr")              # banded-null: token-count-sensitive (D23)

DIALECTS = ("A", "B")        # one band set each (D21, L8)
SCHEMA_VERSION = 2           # 1 = single pooled band set (pre-D21); 2 = per-dialect


def _profile_axis(p: dict) -> dict:
    """Map a raw profile() dict onto the evaluator's profile-axis names."""
    return {"h2": p["h2"], "dI": p["mz_peak_value"], "ed1": p["ed1_main_component"],
            "zipf": p["zipf_slope"], "ttr": p["type_token_ratio"]}


def _ci(sorted_vals: list, lo: float, hi: float) -> list:
    n = len(sorted_vals)
    return [round(sorted_vals[int(lo * n)], 4),
            round(sorted_vals[min(n - 1, int(hi * n))], 4)]


def _subsample(vms: list, nb: int, frac: float, seed: int) -> list:
    """75% of distinct blocks, no duplication (duplicate-safe resample)."""
    rng = random.Random(seed)
    keep = sorted(rng.sample(range(nb), int(frac * nb)))
    return [vms[j] for i in keep
            for j in range(i * BLOCK, min((i + 1) * BLOCK, len(vms)))]


def _build_dialect(dialect: str) -> dict:
    """Bands + point for ONE Currier dialect, at the matched token budget (D21).

    Identical construction for every dialect, so the band sets are like-for-like; the only
    difference is which paragraph token stream goes in.
    """
    vms = _sub(_vms_tokens(dialect), N_TOKENS)
    if len(vms) < N_TOKENS:
        raise ValueError(
            f"Currier {dialect} has only {len(vms)} paragraph tokens, below the "
            f"{N_TOKENS}-token reference budget — its bands would not be comparable."
        )
    nb = len(vms) // BLOCK

    # --- profile axes: subsample-without-replacement 95% CI ----------------------------
    prof_boot = {a: [] for a in (*PROFILE_AXES, *ADVISORY_AXES)}
    for b in range(PROFILE_SUBSAMPLE):
        pa = _profile_axis(profile(_subsample(vms, nb, KEEP_FRAC, 7000 + b)))
        for a in prof_boot:
            prof_boot[a].append(pa[a])
    profile_bands = {a: _ci(sorted(prof_boot[a]), 0.025, 0.975) for a in PROFILE_AXES}

    # --- syntax axes: subsample-without-replacement 90% CI ------------------------------
    syn_boot = {"fc_z_local": [], "wc_z_local": [], "fc_z_global": [], "wc_z_global": []}
    for b in range(SYNTAX_SUBSAMPLE):
        resamp = _subsample(vms, nb, KEEP_FRAC, 9000 + b)
        s = SEED + b
        syn_boot["fc_z_local"].append(_fc_z(resamp, _loc, s))
        syn_boot["wc_z_local"].append(_wc_z(resamp, _loc, s))
        syn_boot["fc_z_global"].append(_fc_z(resamp, _glob, s))
        syn_boot["wc_z_global"].append(_wc_z(resamp, _glob, s))
    syntax_bands = {k: _ci(sorted(v for v in vals if v is not None), 0.05, 0.95)
                    for k, vals in syn_boot.items()}

    prof_method = f"subsample-without-replacement 95% CI ({PROFILE_SUBSAMPLE} reps)"
    syn_method = (f"subsample-without-replacement 90% CI ({SYNTAX_SUBSAMPLE} reps, "
                  f"{int(KEEP_FRAC * 100)}% of blocks; N_NULL={N_NULL})")
    full = _profile_axis(profile(vms))
    axes = {}
    for a in PROFILE_AXES:
        axes[a] = {"band": profile_bands[a], "method": prof_method,
                   "soft": False, "crosses_zero": False}
    # ttr and zipf: advisory (token-count-sensitive) — no band, reference values only.
    # Their subsample CI is computed at 75% of the token budget, and both are biased by
    # that gap, so a band would exclude the full-corpus point by construction rather than
    # describe it (ttr: known since the artifact was first built; zipf: D23, found when
    # per-dialect bands put Currier B's point outside B's own band).
    for a in ADVISORY_AXES:
        axes[a] = {"band": None,
                   "method": "advisory (token-count-sensitive; not banded)",
                   "soft": False, "token_sensitive": True,
                   "vms_full_point": round(full[a], 4),
                   "vms_subsample_75pct_range": _ci(sorted(prof_boot[a]), 0.025, 0.975),
                   "subsample_bias": round(
                       statistics.median(prof_boot[a]) - full[a], 4)}
    for a in syntax_bands:
        b = syntax_bands[a]
        axes[a] = {"band": b, "method": syn_method, "soft": True,
                   "crosses_zero": bool(b[0] <= 0 <= b[1])}

    return {
        "dialect": dialect,
        "vms_dataset": f"ZL EVA transliteration, Currier {dialect}, "
                       f"first {N_TOKENS} paragraph tokens in page order",
        "corpus_tokens": len(_vms_tokens(dialect)),
        "method": "profile axes = " + prof_method + "; syntax axes = " + syn_method,
        "vms_point": axis_values(vms),
        "axes": axes,
    }


def build() -> dict:
    """Compute the reference-band artifact deterministically. No file IO (reads only the
    acquired VMS corpus). `run()` writes it; `ms408.verify` rebuilds and compares."""
    dialects = {d: _build_dialect(d) for d in DIALECTS}
    return {
        "schema": SCHEMA_VERSION,
        "meta": {
            "script": "ms408.experiments.e32_reference_bands",
            "git_commit": git_commit(),
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "vms_dataset": "ZL EVA transliteration, one band set per Currier dialect, "
                           "matched token budget",
            "dialect_scope": {
                "dialects": list(DIALECTS),
                "note": "Bands are stratified by Currier dialect (D21, L8). A and B are "
                        "different generative regimes — a stream matching A's bands "
                        "typically misses B's and vice versa — so there is no single "
                        "'the manuscript' band set and evaluate() reports every dialect "
                        "rather than picking one. Each sample is the first "
                        f"{N_TOKENS} paragraph tokens of that dialect in page order; see "
                        "docs/LIMITS.md and E34 for how well that prefix covers "
                        "the rest of the dialect.",
                "evidence": "ms408.experiments.e34_band_dialect_scope",
                "history": "Before D21 a single band set was built from A+B truncated at "
                           "the budget, which contained only A while claiming A+B. The A "
                           "band set here is byte-identical to that artifact.",
            },
            "n_tokens": N_TOKENS,
            "seed": SEED,
            "block": BLOCK,
            "method": "per dialect: " + dialects[DIALECTS[0]]["method"],
            "params": {"profile_subsample": PROFILE_SUBSAMPLE,
                       "syntax_subsample": SYNTAX_SUBSAMPLE,
                       "keep_frac": KEEP_FRAC, "n_null": N_NULL,
                       "resample": "subsample-without-replacement (duplicate-safe)"},
            "caveats": {
                "dI": "homophony/respacing-confounded (E29); in-band is weak evidence",
                "syntax_soft": "VMS-side CIs cross zero — soft axes; see docs/LIMITS.md",
                "dialect": "In-band for one dialect is NOT in-band for the manuscript; "
                           "report which dialect (L8).",
            },
        },
        "dialects": dialects,
    }


def run() -> dict:
    """Build the artifact and write it (shipped copy + firewall record)."""
    artifact = build()
    SHIPPED.parent.mkdir(parents=True, exist_ok=True)
    SHIPPED.write_text(json.dumps(artifact, indent=2) + "\n")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e32_reference_bands.json").write_text(json.dumps(artifact, indent=2) + "\n")
    return artifact


if __name__ == "__main__":
    art = run()
    print(f"Wrote {SHIPPED.relative_to(ROOT)} at commit {art['meta']['git_commit'][:10]}")
    for dialect, spec in art["dialects"].items():
        print(f"\nCurrier {dialect} — {spec['corpus_tokens']} paragraph tokens, "
              f"bands at {N_TOKENS}")
        for axis, a in spec["axes"].items():
            z = "  (CI crosses 0)" if a.get("crosses_zero") else ""
            print(f"  {axis:<13} band {a['band']}{z}")
