"""E13c — Function/content, NULL-CORRECTED (i05; re-run of E13/E13b via mid_level_null).

E13b's content−function selectivity gap was sample-size confounded (the shuffle null
itself had a positive gap). The fix: for each corpus, express the observed gap as a
z-score against an ORDER-SHUFFLE null ensemble of the same corpus (same word types,
frequencies, TTR — only the token order randomised). The z is the excess content/
function differentiation BEYOND the sample-size baseline, and is nuisance-controlled by
construction, so z-scores are comparable across corpora and VMS-A vs VMS-B directly.

Interpretation: z ≫ 0 ⇒ content words carry collocational structure that function words
lack, beyond chance (a real function/content differentiation). z ≈ 0 ⇒ no such
differentiation (order-shuffle-like). Real languages should show high z; a full shuffle
is z=0 by construction; copying/bigram nulls (self-citation, markov) also show it since
they have local structure (reported as contaminated refs).

Usage:
    python -m ms408.experiments.e13c_function_content_corrected
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from .e13_function_content import N_TOKENS, SEED, _markov1, _sub, _vms_tokens
from .e13b_function_content import _gap
from .e6_cipher_reconstruction import _paradigmatic_conlang
from .mid_level_null import null_z, order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
B_NULL = 50
LANG_Z = 2.0  # z above this ⇒ real differentiation beyond the shuffle baseline


def _corpus_z(tokens: list) -> dict:
    obs = _gap(tokens)
    if obs.get("insufficient"):
        return {"insufficient": True}
    nulls = []
    for i in range(B_NULL):
        g = _gap(order_shuffle(tokens, SEED + i))
        if not g.get("insufficient"):
            nulls.append(g["gap"])
    z = null_z(obs["gap"], nulls)
    z["raw_gap"] = obs["gap"]
    return z


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    german = (H4_OUT / "german_kraeuterbuch_dipl.txt").read_text().split()
    corpora = {
        "latin": _sub(latin), "german": _sub(german),
        "latin_markov1": _markov1(latin[:N_TOKENS], SEED),               # contaminated ref
        "conlang_relex_latin": _sub(_paradigmatic_conlang(latin[:N_TOKENS], 0.8, SEED)),
        "vms_currierA": _sub(_vms_tokens("A")), "vms_currierB": _sub(_vms_tokens("B")),
    }
    stats = {k: _corpus_z(v) for k, v in corpora.items()}

    def zof(c):
        return stats[c].get("z")

    def cls(c):
        z = zof(c)
        return "differentiated" if (z is not None and z >= LANG_Z) else "undifferentiated"

    real_z = [zof(c) for c in ("latin", "german") if zof(c) is not None]
    calibration_ok = bool(real_z and min(real_z) >= LANG_Z)  # real langs must pass
    va, vb = cls("vms_currierA"), cls("vms_currierB")

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E13c — function/content, null-corrected (order-shuffle z)",
        "seed": SEED, "n_tokens": N_TOKENS, "n_null": B_NULL, "lang_z_threshold": LANG_Z,
        "corpus_z": stats,
        "calibration_ok_real_langs_differentiated": calibration_ok,
        "vms_currierA_z": zof("vms_currierA"), "vms_currierB_z": zof("vms_currierB"),
        "vms_currierA_class": va, "vms_currierB_class": vb, "ab_same_class": va == vb,
    }
    results["grade"], results["verdict"] = _verdict(results, stats)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e13c_function_content_corrected.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict, stats: dict) -> tuple:
    za, zb = r["vms_currierA_z"], r["vms_currierB_z"]
    a, b = r["vms_currierA_class"], r["vms_currierB_class"]
    ref = ", ".join(f"{c} z={stats[c]['z']}" for c in ("latin", "german", "latin_markov1",
                    "conlang_relex_latin") if stats[c].get("z") is not None)
    base = (f"Null-corrected (order-shuffle) function/content z — VMS-A={za} ({a}), "
            f"VMS-B={zb} ({b}); threshold {r['lang_z_threshold']}. Reference: {ref}.")
    if not r["calibration_ok_real_langs_differentiated"]:
        return "D", (f"INCONCLUSIVE — real-language controls do not clear the z "
                     f"threshold, so the corrected probe is not calibrated. {base}")
    if a == b == "differentiated":
        return "C", (
            f"BOTH Currier systems show real function/content DIFFERENTIATION beyond the "
            f"order-shuffle baseline (content words carry collocational structure "
            f"function words lack), like the real-language controls, in A AND B. "
            f"Nuisance-corrected, so this is not a type-token-ratio artifact. Reweights "
            f"toward a language-derived process; does not separate A vs B on this probe. "
            f"{base} (Grammar only; no meaning — L7.)")
    if a != b:
        return "C", (
            f"A and B DIFFER on null-corrected function/content differentiation (A {a}, "
            f"B {b}) — evidence the two Currier systems are different generative "
            f"processes. {base} (L7: grammar, not meaning.)")
    return "C", (
        f"NEITHER Currier system shows function/content differentiation beyond the "
        f"order-shuffle baseline (A {a}, B {b}) — undifferentiated, unlike real language; "
        f"consistent with a process whose content words lack distinctive collocates. "
        f"{base} (L7.)")


if __name__ == "__main__":
    out = run()
    print(f"{'corpus':22s} {'raw_gap':>8s} {'null_mean':>9s} {'z':>7s} {'pct':>6s}")
    for c, s in out["corpus_z"].items():
        if s.get("insufficient"):
            print(f"{c:22s} insufficient")
            continue
        print(f"{c:22s} {s['raw_gap']:>8} {s['null_mean']:>9} {str(s['z']):>7} {str(s['percentile']):>6}")
    print(f"\ncalibration_ok={out['calibration_ok_real_langs_differentiated']}")
    print(f"VMS-A z={out['vms_currierA_z']} ({out['vms_currierA_class']}) | "
          f"VMS-B z={out['vms_currierB_z']} ({out['vms_currierB_class']})")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
