"""E15 — Morphology productivity & paradigm coherence (i05).

E6 established that the VMS's dense edit-distance-1 network (main component 0.80) can
arise from very different mechanisms: real inflection, a constructed-paradigm conlang,
or a mere abjad (vowel-dropping → skeleton collisions). E15 asks which: is the
Voynichese morphology a PRODUCTIVE, PARADIGMATIC system (a small affix inventory
recurring across many stems, with coherent signatures like declension classes) — like
an inflecting language or a constructed conlang — or incoherent skeleton-collision like
an abjad? And is it the same in Currier A and B?

Measure (Goldsmith-lite unsupervised signatures). Take a small inventory of the most
common 2-char word-final strings; a STEM is a word-minus-suffix that occurs with ≥2
inventory suffixes; its SIGNATURE is that suffix set. Report:
  paradigm_coherence  — fraction of paradigmatic stems in the top-10 signatures (real
                        paradigms concentrate; random collisions do not);
  productivity        — mean distinct stems per inventory suffix (affix reuse);
  compression         — types per paradigmatic stem.
Calibrate on Latin & a constructed conlang (paradigmatic → HIGH coherence) vs an abjad
of Latin & a full shuffle (collisions/none → LOW coherence). Trust the probe only if
that separation is clean (≥ 0.15 on coherence); then place VMS-A and VMS-B.

Usage:
    python -m ms408.experiments.e15_morphology
"""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

import random

from ..dataset import git_commit
from ..h4 import H4_OUT
from .e13_function_content import N_TOKENS, SEED, _sub, _vms_tokens
from .e6_cipher_reconstruction import _abjad_collapse, _paradigmatic_conlang

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
N_SUFFIXES = 25
TOP_SIGS = 10


def _charshuffle(tokens: list, seed: int) -> list:
    """Shuffle characters WITHIN each word — destroys morpheme/affix structure while
    preserving each word's length and character multiset. The clean morphology null
    (a token-order shuffle is useless here: it keeps the word types unchanged)."""
    rng = random.Random(seed)
    out = []
    for w in tokens:
        cs = list(w)
        rng.shuffle(cs)
        out.append("".join(cs))
    return out


def _morphology(tokens: list) -> dict:
    words = [w for w in set(tokens) if len(w) >= 4]
    if len(words) < 100:
        return {"insufficient": True, "n_words": len(words)}
    suf2 = Counter(w[-2:] for w in words)
    top_sufs = {s for s, _ in suf2.most_common(N_SUFFIXES)}
    stem_sufs = defaultdict(set)
    for w in words:
        s2 = w[-2:]
        if s2 in top_sufs and len(w) - 2 >= 2:
            stem_sufs[w[:-2]].add(s2)
    para = {st: frozenset(ss) for st, ss in stem_sufs.items() if len(ss) >= 2}
    if len(para) < 20:
        return {"insufficient": True, "n_paradigmatic_stems": len(para)}
    n = len(para)
    sigs = Counter(para.values())
    coherence = sum(c for _, c in sigs.most_common(TOP_SIGS)) / n
    productivity = statistics.mean(len(ss) for ss in para.values())
    suf_stems = defaultdict(set)
    for st, ss in para.items():
        for s in ss:
            suf_stems[s].add(st)
    reuse = statistics.mean(len(v) for v in suf_stems.values())
    return {"n_types": len(words), "n_paradigmatic_stems": n,
            "paradigm_coherence": round(coherence, 3),
            "mean_signatures_per_suffix": round(reuse, 1),
            "mean_suffixes_per_stem": round(productivity, 2),
            "distinct_signatures": len(sigs)}


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    corpora = {
        "latin": _sub(latin),
        "conlang_relex_latin": _sub(_paradigmatic_conlang(latin[:N_TOKENS], 0.8, SEED)),
        "abjad_latin": _sub(_abjad_collapse(latin[:N_TOKENS], SEED)),
        "latin_charshuffled": _sub(_charshuffle(latin[:N_TOKENS], SEED)),
        "vms_currierA": _sub(_vms_tokens("A")),
        "vms_currierB": _sub(_vms_tokens("B")),
    }
    stats = {k: _morphology(v) for k, v in corpora.items()}

    def coh(c):
        return stats[c].get("paradigm_coherence")

    # Reference bar = real inflecting Latin (natural paradigms). Non-paradigmatic
    # anchors = abjad (skeleton collision) + within-word char shuffle (morphology
    # destroyed). The conlang is an idealised upper bound, reported not used as the bar.
    latin_bar = coh("latin")
    nonparadig = [coh(c) for c in ("abjad_latin", "latin_charshuffled") if coh(c) is not None]
    null_mean = round(statistics.mean(nonparadig), 3) if nonparadig else None
    separation = round(latin_bar - null_mean, 3) if (latin_bar is not None and null_mean is not None) else None
    calibration_ok = bool(separation is not None and separation >= 0.15)

    def classify(c):
        v = coh(c)
        if v is None or not calibration_ok:
            return "inconclusive"
        if v >= latin_bar:
            return "paradigmatic (≥ real inflection)"
        if v <= null_mean:
            return "collision-like (≤ null)"
        return "intermediate (below real inflection, above null)"

    va, vb = classify("vms_currierA"), classify("vms_currierB")
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E15 — morphology productivity & paradigm coherence",
        "seed": SEED, "n_tokens": N_TOKENS,
        "stats": stats,
        "calibration": {"real_inflection_bar_latin": latin_bar,
                        "null_mean_abjad_charshuffle": null_mean,
                        "conlang_upper_bound": coh("conlang_relex_latin"),
                        "separation": separation, "calibration_ok": calibration_ok},
        "vms_currierA_class": va, "vms_currierB_class": vb,
        "ab_same_class": va == vb,
        "learnings": (
            "The paradigm-coherence measure (top-10 signatures / n) is confounded by n: "
            "the char-shuffle null yields fewer paradigmatic stems (n≈111) so its top-10 "
            "cover a larger fraction (coherence 0.44 > real Latin 0.41), collapsing the "
            "calibration. Raw descriptive VALUES are still ordered as expected — VMS-A "
            "0.29 / VMS-B 0.35 sit BELOW real Latin (0.41) and FAR below the constructed "
            "conlang (0.98), ABOVE the abjad (0.16) — hinting VMS morphology is only "
            "partly paradigmatic, but this is NOT trusted without n-correction. Fix: an "
            "n-matched null-model-corrected coherence (the same permutation-baseline fix "
            "E13/E13b need) — the mid-level program needs this framework built once."),
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e15_morphology.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    c = r["calibration"]
    a, b = r["vms_currierA_class"], r["vms_currierB_class"]
    ca = r["stats"]["vms_currierA"].get("paradigm_coherence")
    cb = r["stats"]["vms_currierB"].get("paradigm_coherence")
    base = (f"Paradigm coherence anchors: real-inflection Latin {c['real_inflection_bar_latin']} "
            f"(the bar), null (abjad + char-shuffle) {c['null_mean_abjad_charshuffle']}, "
            f"conlang upper bound {c['conlang_upper_bound']}. VMS-A={ca} ({a}); VMS-B={cb} "
            f"({b}).")
    if not c["calibration_ok"]:
        return "D", (f"INCONCLUSIVE — coherence does not separate real inflection from "
                     f"the null (separation {c['separation']} < 0.15). {base}")
    both_para = a.startswith("paradigmatic") and b.startswith("paradigmatic")
    both_inter = a.startswith("intermediate") and b.startswith("intermediate")
    both_coll = a.startswith("collision") and b.startswith("collision")
    if both_para:
        return "C", (
            f"BOTH Currier systems reach real-inflection-level paradigm coherence — the "
            f"ED1 network is productive/paradigmatic, not abjad collision, in A AND B. "
            f"Sharpens F12. {base} (Grammar only; no meaning — L7.)")
    if both_inter:
        return "C", (
            f"BOTH Currier systems are INTERMEDIATE — VMS paradigm coherence sits BELOW "
            f"real inflecting Latin but ABOVE the collision null, in A and B. So the "
            f"dense ED1 network (F12) is only partly paradigmatic: more regular than an "
            f"abjad, but LESS paradigm-coherent than a real inflecting language. This "
            f"is consistent with a constrained slot-morphology (cf. Stolfi) that is "
            f"regular but not fully inflectional. {base} (Grammar only; no meaning — L7.)")
    if both_coll:
        return "C", (
            f"BOTH Currier systems are COLLISION-LIKE — coherence at or below the abjad/"
            f"shuffle null; the ED1 network is not productive paradigmatic morphology. "
            f"{base} (L7.)")
    return "C", (
        f"A and B DIFFER in morphological paradigm coherence (A {a}, B {b}) — evidence "
        f"the two Currier systems are morphologically different processes. {base} (L7.)")


if __name__ == "__main__":
    out = run()
    print(f"{'corpus':22s} {'coher':>6s} {'suf/stem':>9s} {'stem/suf':>9s} {'#stems':>7s}")
    for c, s in out["stats"].items():
        if s.get("insufficient"):
            print(f"{c:22s} insufficient ({s})")
            continue
        print(f"{c:22s} {s['paradigm_coherence']:>6} {s['mean_suffixes_per_stem']:>9} "
              f"{s['mean_signatures_per_suffix']:>9} {s['n_paradigmatic_stems']:>7}")
    cal = out["calibration"]
    print(f"\nlatin_bar={cal['real_inflection_bar_latin']} "
          f"null={cal['null_mean_abjad_charshuffle']} "
          f"conlang={cal['conlang_upper_bound']} "
          f"sep={cal['separation']} ok={cal['calibration_ok']}")
    print(f"VMS-A={out['vms_currierA_class']} VMS-B={out['vms_currierB_class']}")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
