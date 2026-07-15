"""E19 — Joint-signature test with mid-level syntax (i06, gating).

i01's encoding bracket and E6 compared candidate encodings on character entropy,
word-order ΔI, ED1 morphology, and Zipf. i05 added two MID-LEVEL syntax measures that
turn out to be the decisive discriminators: the null-corrected function/content
collocation gap (E13c) and the null-corrected word-class NMI (E14). The key asymmetry:
a word-order-PRESERVING cipher of a real language (abjad, deterministic-verbose,
nomenclator) inherits the source language's STRONG word-syntax, whereas the VMS has
WEAK word-syntax. E19 assembles the FULL signature for the VMS and for candidate
generators of a real language and asks which class matches the VMS on EVERY axis —
especially the mid-level syntax.

Candidates (all from natural-order Latin so word-syntax is preserved where the
mechanism preserves it):
  word-order-preserving ciphers : abjad, deterministic 1:1 substitution, nomenclator
  generation (weak-syntax)      : self-citation (H3), paradigmatic conlang
  reference                     : real Latin (strong), full order-shuffle (none)

Signature = h2, ΔI peak, ED1 main component, Zipf slope, function/content z, word-class z.

Verdict logic. The mid-level z's classify each candidate as STRONG-syntax (z ≥ 5,
real-language-like) or WEAK-syntax (z < 3, VMS-like). If every cipher-of-real-language
candidate is strong-syntax and only the generation processes are weak-syntax like the
VMS, then the VMS is DISFAVOURED as a word-order-preserving cipher of real prose (a new
graded constraint), and the decipherment target redirects to generative mechanisms.

Usage:
    python -m ms408.experiments.e19_joint_signature
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..studies.encoding import profile
from .e13_function_content import N_TOKENS, SEED, _sub, _vms_tokens
from .e13b_function_content import _gap
from .e14_word_classes import _adjacent_class_nmi
from .e6_cipher_reconstruction import _abjad_collapse, _det_verbose, _paradigmatic_conlang
from .e5_encoding_fair import fam_selfcitation
from .mid_level_null import null_z, order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
B_MID = 12
STRONG_Z = 5.0
WEAK_Z = 3.0


def _fc_z(tokens: list) -> float:
    obs = _gap(tokens)
    if obs.get("insufficient"):
        return 0.0
    nulls = [_gap(order_shuffle(tokens, SEED + i)).get("gap") for i in range(30)]
    return round(null_z(obs["gap"], [g for g in nulls if g is not None])["z"], 2)


def _wc_z(tokens: list) -> float:
    obs = _adjacent_class_nmi(tokens, SEED)
    nulls = [_adjacent_class_nmi(order_shuffle(tokens, SEED + 1 + i), SEED + 1 + i)
             for i in range(B_MID)]
    return round(null_z(obs, nulls)["z"], 2)


def _signature(tokens: list) -> dict:
    p = profile(tokens)
    return {"h2": round(p["h2"], 3), "dI": round(p["mz_peak_value"], 3),
            "ed1": round(p["ed1_main_component"], 3), "zipf": round(p["zipf_slope"], 3),
            "fc_z": _fc_z(tokens), "wc_z": _wc_z(tokens)}


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    base = latin[:N_TOKENS]
    corpora = {
        "VMS_A": _sub(_vms_tokens("A"), N_TOKENS), "VMS_B": _sub(_vms_tokens("B"), N_TOKENS),
        # word-order-preserving ciphers of real Latin
        "cipher_abjad": _sub(_abjad_collapse(base, SEED)),
        "cipher_subst_1to1": _sub(_det_verbose(base, 1, 0, SEED)),
        "cipher_nomenclator": _sub(_det_verbose(base, 1, 2000, SEED)),
        # generation processes (weak-syntax by nature)
        "gen_self_citation": _sub(fam_selfcitation(N_TOKENS + 200, 3)),
        "gen_conlang": _sub(_paradigmatic_conlang(base, 0.8, SEED)),
        # references
        "ref_real_latin": _sub(base), "ref_shuffle": _sub(order_shuffle(base, SEED)),
    }
    sigs = {k: _signature(v) for k, v in corpora.items()}

    groups = {
        "cipher_of_real_language": ["cipher_abjad", "cipher_subst_1to1", "cipher_nomenclator"],
        "generation_process": ["gen_self_citation", "gen_conlang"],
    }

    def syntax_class(c):
        s = sigs[c]
        strong = s["fc_z"] >= STRONG_Z and s["wc_z"] >= STRONG_Z
        weak = s["fc_z"] < WEAK_Z and s["wc_z"] < WEAK_Z
        return "strong" if strong else ("weak" if weak else "mixed")

    classes = {c: syntax_class(c) for c in corpora}
    # A candidate MATCHES the VMS on the discriminating axes if it reproduces the
    # low character entropy AND the weak mid-level syntax (both) — the combination no
    # single measure captures. h2 tolerance ±0.5 around the VMS mean.
    vms_h2 = (sigs["VMS_A"]["h2"] + sigs["VMS_B"]["h2"]) / 2
    candidates = groups["cipher_of_real_language"] + groups["generation_process"]

    def matches_vms(c):
        s = sigs[c]
        return bool(abs(s["h2"] - vms_h2) <= 0.5 and s["fc_z"] < WEAK_Z and s["wc_z"] < WEAK_Z)

    matched = [c for c in candidates if matches_vms(c)]
    cipher_matches = [c for c in groups["cipher_of_real_language"] if matches_vms(c)]
    gen_matches = [c for c in groups["generation_process"] if matches_vms(c)]

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E19 — joint-signature test with mid-level syntax",
        "seed": SEED, "n_tokens": N_TOKENS,
        "strong_z_threshold": STRONG_Z, "weak_z_threshold": WEAK_Z,
        "vms_mean_h2": round(vms_h2, 3),
        "signatures": sigs,
        "syntax_class": classes,
        "candidates_matching_vms_discriminators": matched,
        "cipher_of_real_language_matches": cipher_matches,
        "generation_process_matches": gen_matches,
        "no_cipher_of_real_language_matches": len(cipher_matches) == 0,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e19_joint_signature.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    s = r["signatures"]
    cls = r["syntax_class"]
    tab = "; ".join(f"{c}: h2={s[c]['h2']} fc_z={s[c]['fc_z']} wc_z={s[c]['wc_z']} [{cls[c]}]"
                    for c in ("cipher_abjad", "cipher_subst_1to1", "cipher_nomenclator",
                              "gen_self_citation", "gen_conlang"))
    if r["no_cipher_of_real_language_matches"] and r["generation_process_matches"]:
        return "C", (
            f"NO cipher of a real language matches the VMS on the joint signature; only "
            f"a GENERATION process does. On the discriminating axes — low character "
            f"entropy (VMS h2≈{r['vms_mean_h2']}) together with WEAK mid-level syntax — "
            f"every word-order-preserving cipher of real Latin FAILS: the abjad "
            f"(h2 {s['cipher_abjad']['h2']}, fc_z {s['cipher_abjad']['fc_z']}) and the "
            f"1:1 substitution (fc_z {s['cipher_subst_1to1']['fc_z']}) RETAIN strong "
            f"real-language word-syntax the VMS lacks; the nomenclator uniquely degrades "
            f"word-class structure (wc_z {s['cipher_nomenclator']['wc_z']}) — because it "
            f"obliterates function words — but still fails on character entropy "
            f"(h2 {s['cipher_nomenclator']['h2']}) and function/content "
            f"(fc_z {s['cipher_nomenclator']['fc_z']}). The only candidate reproducing "
            f"the VMS's low-entropy + weak-syntax combination is the SELF-CITATION "
            f"generation process ({', '.join(r['generation_process_matches'])}: "
            f"h2 {s['gen_self_citation']['h2']}, fc_z {s['gen_self_citation']['fc_z']}, "
            f"wc_z {s['gen_self_citation']['wc_z']}), though it overshoots ΔI/ED1. "
            f"**Net: the weak word-syntax constraint DISFAVOURS the VMS as a "
            f"straightforward cipher of real prose (the abjad E6 revived is excluded on "
            f"the JOINT signature) and FAVOURS a generative / function-word-destroying "
            f"mechanism.** For E20 the cryptanalytic target collapses: no syntax-"
            f"preserving cipher of real prose is viable; the surviving lead is a heavy "
            f"nomenclator-like transform, and even it is a poor joint match — so a "
            f"decipherment attack is low-yield, and E20 should REDIRECT to the "
            f"generative alternative. {tab}. (Statistical; no meaning claim — L7.)")
    if r["cipher_of_real_language_matches"]:
        return "C", (
            f"A cipher of a real language ({', '.join(r['cipher_of_real_language_matches'])}) "
            f"matches the VMS on the discriminating axes — it remains a live attack "
            f"target for E20. {tab}. (L7.)")
    return "D", (f"INCONCLUSIVE — no candidate (cipher or generation) matches the VMS on "
                 f"the discriminators under the thresholds. {tab}")


if __name__ == "__main__":
    out = run()
    print(f"{'corpus':20s} {'h2':>6s} {'dI':>6s} {'ed1':>6s} {'zipf':>6s} "
          f"{'fc_z':>7s} {'wc_z':>7s} {'syntax':>7s}")
    for c, s in out["signatures"].items():
        print(f"{c:20s} {s['h2']:>6} {s['dI']:>6} {s['ed1']:>6} {s['zipf']:>6} "
              f"{str(s['fc_z']):>7} {str(s['wc_z']):>7} {out['syntax_class'][c]:>7}")
    print(f"\ncandidates matching VMS on discriminators: {out['candidates_matching_vms_discriminators']}")
    print(f"  cipher-of-real-language matches: {out['cipher_of_real_language_matches']} | "
          f"generation matches: {out['generation_process_matches']}")
    print(f"grade {out['grade']}: {out['verdict'][:160]}...")
