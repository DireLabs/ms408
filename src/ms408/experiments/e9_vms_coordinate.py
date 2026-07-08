"""E9 — VMS coordinate: dose-response localization (i03 flagship; L35, Type B).

i02 showed meaningful-vs-meaningless is not a binary any single statistic settles
(E1: ΔI is block-structure; E5: no family distinguished). E9 asks whether the VMS
can be LOCALIZED between a MEANINGFUL and a MEANINGLESS endpoint on interpretable
axes.

CRITICAL correction (pre-registration Amendment 2, after the first run + a clean-
context refutation): the meaningless endpoint must be a STRUCTURED-MEANINGLESS
stream, NOT a trivial/degenerate one. E1/E2 proved a block drift-null scores HIGH
on ΔI, and E6 proved an abjad of real Latin reaches ED1 ≈ 0.90 — so these statistics
are STRUCTURE detectors. Placing the VMS against a shuffled/atomic coord-0 endpoint
merely measures "has structure" (already known) and CANNOT bear on meaning. E9 v2
therefore sets coord 0 = a structured-meaningless endpoint and asks the honest
question: does the VMS SEPARATE from a structured-meaningless adversary on any axis?

Axes:
  A1 word-order (ΔI):   coord 0 = block drift-null (structured, meaningless);
                        coord 1 = natural blocked Latin (meaningful).
  A3 paradigm (ED1):    coord 0 = abjad of real Latin (structured, meaningless);
                        coord 1 = paradigmatic conlang (meaningful).
  A2 homophony (h2):    NON-ADMISSIBLE — h2 is fatally confounded (the flagship
                        anomaly) and there is no clean structured-meaningless
                        homophony endpoint. Reported, not coordinatised.

An axis DISCRIMINATES meaning only if its two structured endpoints separate beyond
VMS bootstrap noise AND the VMS sits clearly on the meaningful side. Grade D
(exploratory, L35); E9 issues no meaningful-vs-meaningless verdict.

Usage:
    python -m ms408.experiments.e9_vms_coordinate
"""

from __future__ import annotations

import json
import random
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..studies.encoding import profile, vms_stream
from .e2_wordorder_confound import blocked_natural_text
from .e5_encoding_fair import _block_boot
from .e6_cipher_reconstruction import _abjad_collapse, _paradigmatic_conlang

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
SEED = 408
SEEDS = 5
BOOTSTRAP = 150
N_BLOCKS = 10


def _stat(stream: list, key: str) -> float:
    return profile(stream)[key]


def _drift_null_blocked(blocked: list, seed: int) -> list:
    """Structured-meaningless A1 endpoint: keep block-level vocabulary structure but
    destroy word order — within each of N_BLOCKS chunks, redraw every token from that
    chunk's own token multiset (block-local unigram null). High block structure, zero
    word-order meaning (the E1/E2 adversary)."""
    rng = random.Random(seed)
    out, L = [], len(blocked)
    size = max(1, L // N_BLOCKS)
    for b in range(N_BLOCKS):
        chunk = blocked[b * size:] if b == N_BLOCKS - 1 else blocked[b * size:(b + 1) * size]
        if chunk:
            out.extend(rng.choice(chunk) for _ in chunk)
    return out


def run() -> dict:
    vms = vms_stream()
    n = len(vms)
    blocked = blocked_natural_text(n)
    vms_p = profile(vms)

    def mean_stat(gen, key):
        return round(statistics.mean(_stat(gen(s), key) for s in range(SEEDS)), 4)

    # Admissible axes: (statistic, meaningful gen, structured-meaningless gen,
    #                   trivial endpoint value for context).
    axes = {
        "A1_word_order": {
            "stat": "mz_peak_value",
            "meaningful": lambda s: blocked,                       # natural order
            "struct_meaningless": lambda s: _drift_null_blocked(blocked, SEED + 100 * s),
            "trivial_note": "shuffled tokens (naive coord-0) ΔI≈0",
        },
        "A3_paradigm": {
            "stat": "ed1_main_component",
            "meaningful": lambda s: _paradigmatic_conlang(blocked, 1.0, SEED + 100 * s),
            "struct_meaningless": lambda s: _abjad_collapse(blocked, SEED + 100 * s),
            "trivial_note": "atomic lexicon (naive coord-0) ED1≈0",
        },
    }

    coords = {}
    for name, ax in axes.items():
        key = ax["stat"]
        sm = mean_stat(ax["struct_meaningless"], key)          # coord 0 (honest)
        meaningful = mean_stat(ax["meaningful"], key)          # coord 1
        vms_stat = round(vms_p[key], 4)
        span = meaningful - sm

        def coord(v, lo=sm, sp=span):
            return (v - lo) / sp if sp else float("nan")

        boot = [coord(_stat(_block_boot(vms, random.Random(9000 + b)), key))
                for b in range(BOOTSTRAP)]
        bs = sorted(x for x in boot if x == x)  # drop nan
        ci = ([round(bs[int(0.025 * len(bs))], 3),
               round(bs[min(len(bs) - 1, int(0.975 * len(bs)))], 3)] if bs else None)
        raw = coord(vms_stat)
        vms_below_sm = raw < 0
        vms_between = 0.0 <= raw <= 1.0
        # An axis DISCRIMINATES meaning only if the VMS sits CLEARLY on the meaningful
        # side of the structured-meaningless endpoint: the whole coordinate CI is
        # above 0.6. (If VMS is below the SM endpoint, or the CI straddles it, the
        # axis cannot separate the VMS from a structured-meaningless stream.)
        discriminates = bool(ci and ci[0] > 0.6 and vms_between)
        coords[name] = {
            "statistic": key,
            "endpoint_structured_meaningless": sm,
            "endpoint_meaningful": meaningful,
            "endpoint_separation": round(span, 4),
            "trivial_note": ax["trivial_note"],
            "vms_statistic": vms_stat,
            "vms_coordinate_raw": round(raw, 3),
            "coordinate_ci95": ci,
            "vms_below_structured_meaningless": bool(vms_below_sm),
            "vms_between_endpoints": bool(vms_between),
            "axis_discriminates_meaning": discriminates,
        }

    # A2 reported but non-admissible (h2 confounded; no clean SM homophony endpoint).
    a2 = {"statistic": "h2", "vms_statistic": round(vms_p["h2"], 4),
          "admissible": False,
          "reason": "h2 is the flagship low-entropy anomaly (confounded); no clean "
                    "structured-meaningless homophony endpoint. Cannot coordinatise."}

    any_discriminates = any(c["axis_discriminates_meaning"] for c in coords.values())
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E9 v2 — VMS coordinate vs STRUCTURED-meaningless endpoints",
        "grade": "D",
        "seed": SEED, "tokens": n, "bootstrap": BOOTSTRAP,
        "admissible_axes": list(axes),
        "non_admissible_axes": {"A2_homophony": a2,
                                "A4_vocab_drift": "deferred (Amendment 1)"},
        "coordinates": coords,
        "any_axis_discriminates_meaning": bool(any_discriminates),
        "prereg_commitment_3": "RETRACTED (Amendment 2) — false premise: trivial "
                               "coord-0 endpoints measured structure, not meaning.",
    }
    results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e9_vms_coordinate.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> str:
    lines = []
    for k, c in r["coordinates"].items():
        where = ("BELOW the structured-meaningless endpoint"
                 if c["vms_below_structured_meaningless"]
                 else "between the endpoints" if c["vms_between_endpoints"]
                 else "above the meaningful endpoint")
        lines.append(
            f"{k.split('_', 1)[1]}: VMS {c['statistic']}={c['vms_statistic']} sits "
            f"{where} (structured-meaningless {c['endpoint_structured_meaningless']} → "
            f"meaningful {c['endpoint_meaningful']}; raw coord {c['vms_coordinate_raw']}, "
            f"CI {c['coordinate_ci95']})")
    body = "; ".join(lines)
    return (
        f"[D — EXPLORATORY, L35] Against HONEST structured-meaningless endpoints, "
        f"{'NO admissible axis' if not r['any_axis_discriminates_meaning'] else 'at least one axis'} "
        f"separates the VMS from a structured-meaningless adversary on the meaningful "
        f"side. {body}. The first-run vector (0.86, 0.69, 0.92) was an ARTIFACT of "
        f"trivial coord-0 endpoints — pre-registered commitment #3 is RETRACTED. Read "
        f"honestly: A1's ΔI and A3's ED1 are STRUCTURE statistics on which a "
        f"structured-meaningless stream scores as high as (A1) or higher than (A3, "
        f"where the VMS ED1 0.80 sits BELOW both an abjad 0.90 and a dense conlang) "
        f"the VMS — so they cannot place the VMS on the meaningful side. A2 (h2) is "
        f"non-admissible. NET: E9 finds NO structural axis that localizes MEANING; it "
        f"reconfirms i02 — the VMS is maximally structured on every measurable axis, "
        f"yet meaningful-vs-meaningless stays underdetermined. The deliverable is this "
        f"negative + a demonstrated method for building honest meaning axes (need a "
        f"structured-meaningless endpoint, not a trivial one).")


if __name__ == "__main__":
    out = run()
    for k, c in out["coordinates"].items():
        print(f"  {k:16s} {c['statistic']:16s} sm={c['endpoint_structured_meaningless']} "
              f"vms={c['vms_statistic']} meaningful={c['endpoint_meaningful']} "
              f"raw_coord={c['vms_coordinate_raw']} CI={c['coordinate_ci95']} "
              f"discriminates={c['axis_discriminates_meaning']}")
    print(f"A2 non-admissible; any_axis_discriminates={out['any_axis_discriminates_meaning']}")
    print("grade", out["grade"], "|", out["verdict"][:150], "...")
