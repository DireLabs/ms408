"""E32 — build the committed VMS reference-band artifact for the public evaluator.

`ms408.evaluate()` checks a user's token stream against Voynich-manuscript reference
bands. Those bands must come from deterministic, versioned code (L3 firewall), not be
hand-typed into the library. This script computes them once and writes:

  * ``src/ms408/data/reference_bands.json`` — the SHIPPED artifact (committed, loaded by
    ``ms408.signature.vms_bands()``); carries its own provenance.
  * ``results/experiments/e32_reference_bands.json`` — the firewall record.

Band construction — subsample WITHOUT replacement throughout (75% of distinct blocks):
  * profile axes (h2, dI, ed1, zipf) — 95% CI.
  * syntax axes (fc/wc, local + global) — 90% CI (E31 convention).
  Block-bootstrap WITH replacement is NOT used: duplicate blocks depress TTR, distort the
  Zipf slope, and inject spurious collocation/adjacency — under it the VMS falls outside
  its own TTR/Zipf band (E31 flagged the same duplicate-block bias for the syntax
  measures). Subsampling without replacement avoids it and lands every band on its point.
  * TTR is intrinsically token-count-sensitive (fewer tokens -> higher TTR), so a
    resampled band would exclude the full-corpus value by construction. TTR ships as an
    ADVISORY axis (band = null; a reference value + the VMS TTR-vs-tokens is recorded) and
    is not counted toward the hard-axis tally.

Every axis value is computed by ``ms408.signature.axis_values`` / its helpers, the SAME
code path ``evaluate()`` runs on user input — so a user's value and its band can never
drift apart.

Usage:
    python -m ms408.experiments.e32_reference_bands
"""

from __future__ import annotations

import json
import random
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

PROFILE_AXES = ("h2", "dI", "ed1", "zipf")   # banded, duplicate-safe
# ttr is banded-null (advisory): intrinsically token-count-sensitive.


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


def run() -> dict:
    vms = _sub(_vms_tokens("A") + _vms_tokens("B"), N_TOKENS)
    nb = len(vms) // BLOCK

    # --- profile axes: subsample-without-replacement 95% CI ----------------------------
    prof_boot = {a: [] for a in (*PROFILE_AXES, "ttr")}
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
    axes = {}
    for a in PROFILE_AXES:
        axes[a] = {"band": profile_bands[a], "method": prof_method,
                   "soft": False, "crosses_zero": False}
    # ttr: advisory (token-count-sensitive) — no band, carry reference values only.
    axes["ttr"] = {"band": None, "method": "advisory (token-count-sensitive; not banded)",
                   "soft": False, "token_sensitive": True,
                   "vms_full_point": round(profile(vms)["type_token_ratio"], 4),
                   "vms_subsample_75pct_range": _ci(sorted(prof_boot["ttr"]), 0.025, 0.975)}
    for a in syntax_bands:
        b = syntax_bands[a]
        axes[a] = {"band": b, "method": syn_method, "soft": True,
                   "crosses_zero": bool(b[0] <= 0 <= b[1])}

    artifact = {
        "meta": {
            "script": "ms408.experiments.e32_reference_bands",
            "git_commit": git_commit(),
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "vms_dataset": "ZL EVA transliteration, Currier A+B, matched token budget",
            "n_tokens": N_TOKENS,
            "seed": SEED,
            "block": BLOCK,
            "method": "profile axes = " + prof_method + "; syntax axes = " + syn_method,
            "params": {"profile_subsample": PROFILE_SUBSAMPLE,
                       "syntax_subsample": SYNTAX_SUBSAMPLE,
                       "keep_frac": KEEP_FRAC, "n_null": N_NULL,
                       "resample": "subsample-without-replacement (duplicate-safe)"},
            "caveats": {
                "dI": "homophony/respacing-confounded (E29); in-band is weak evidence",
                "syntax_soft": "VMS-side CIs cross zero — soft axes; see docs/LIMITS.md",
            },
        },
        "vms_point": axis_values(vms),
        "axes": axes,
    }

    SHIPPED.parent.mkdir(parents=True, exist_ok=True)
    SHIPPED.write_text(json.dumps(artifact, indent=2) + "\n")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e32_reference_bands.json").write_text(json.dumps(artifact, indent=2) + "\n")
    return artifact


if __name__ == "__main__":
    art = run()
    print(f"Wrote {SHIPPED.relative_to(ROOT)} at commit {art['meta']['git_commit'][:10]}")
    for axis, spec in art["axes"].items():
        z = "  (CI crosses 0)" if spec.get("crosses_zero") else ""
        print(f"  {axis:<13} band {spec['band']}{z}")
