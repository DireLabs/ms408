"""E15b — Morphology paradigm coherence, NULL-CORRECTED (i05; re-run of E15).

E15's coherence measure (top-10 signatures / n) was confounded by the number of
paradigmatic stems n. The fix: for each corpus, express observed coherence as a
z-score against a RANDOM-SIGNATURE null that holds n, the stem degree sequence, and the
suffix popularity fixed — only WHICH suffix-set each stem takes is randomised. If a
corpus has real paradigms (stems non-randomly share the same suffix SETS), observed
coherence ≫ null ⇒ high z; abjad/char-shuffle collision ⇒ observed ≈ null ⇒ z ≈ 0. The
z removes the n-confound, so z is comparable across corpora and VMS-A vs VMS-B directly.

Usage:
    python -m ms408.experiments.e15b_morphology_corrected
"""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from .e13_function_content import N_TOKENS, SEED, _sub, _vms_tokens
from .e15_morphology import N_SUFFIXES, TOP_SIGS, _charshuffle
from .e6_cipher_reconstruction import _abjad_collapse, _paradigmatic_conlang
from .mid_level_null import null_z

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
B_NULL = 100
LANG_Z = 3.0  # z above this ⇒ paradigm coherence beyond random signature assignment


def _decompose(tokens: list):
    """Return {stem: frozenset(suffixes)} for paradigmatic stems (≥2 inventory
    suffixes) and the suffix popularity (stems per suffix)."""
    words = [w for w in set(tokens) if len(w) >= 4]
    if len(words) < 100:
        return None, None
    top_sufs = {s for s, _ in Counter(w[-2:] for w in words).most_common(N_SUFFIXES)}
    stem_sufs = defaultdict(set)
    for w in words:
        s2 = w[-2:]
        if s2 in top_sufs and len(w) - 2 >= 2:
            stem_sufs[w[:-2]].add(s2)
    para = {st: frozenset(ss) for st, ss in stem_sufs.items() if len(ss) >= 2}
    if len(para) < 20:
        return None, None
    pop = Counter()
    for ss in para.values():
        pop.update(ss)
    return para, pop


def _coherence(signatures: list) -> float:
    sigs = Counter(signatures)
    return sum(c for _, c in sigs.most_common(TOP_SIGS)) / len(signatures)


def _corpus_z(tokens: list) -> dict:
    para, pop = _decompose(tokens)
    if para is None:
        return {"insufficient": True}
    obs = _coherence(list(para.values()))
    suf_list = list(pop)
    weights = [pop[s] for s in suf_list]
    degrees = [len(ss) for ss in para.values()]
    nulls = []
    for i in range(B_NULL):
        rng = random.Random(SEED + i)
        rand_sigs = []
        for d in degrees:
            # sample d distinct suffixes weighted by popularity (configuration-model-ish)
            chosen = set()
            guard = 0
            while len(chosen) < d and guard < 50:
                chosen.add(rng.choices(suf_list, weights=weights, k=1)[0])
                guard += 1
            rand_sigs.append(frozenset(chosen))
        nulls.append(_coherence(rand_sigs))
    z = null_z(obs, nulls)
    z["n_stems"] = len(para)
    return z


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    corpora = {
        "latin": _sub(latin),
        "conlang_relex_latin": _sub(_paradigmatic_conlang(latin[:N_TOKENS], 0.8, SEED)),
        "abjad_latin": _sub(_abjad_collapse(latin[:N_TOKENS], SEED)),
        "latin_charshuffled": _sub(_charshuffle(latin[:N_TOKENS], SEED)),
        "vms_currierA": _sub(_vms_tokens("A")), "vms_currierB": _sub(_vms_tokens("B")),
    }
    stats = {k: _corpus_z(v) for k, v in corpora.items()}

    def zof(c):
        return stats[c].get("z")

    def cls(c):
        z = zof(c)
        return "paradigmatic" if (z is not None and z >= LANG_Z) else "not-paradigmatic"

    # Calibration: real inflection (latin) must clear the bar AND the collision nulls
    # (abjad, char-shuffle) must NOT — else the corrected probe is not calibrated.
    real_ok = zof("latin") is not None and zof("latin") >= LANG_Z
    null_ok = all((zof(c) is None or zof(c) < LANG_Z) for c in ("abjad_latin", "latin_charshuffled"))
    calibration_ok = bool(real_ok and null_ok)
    va, vb = cls("vms_currierA"), cls("vms_currierB")

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E15b — morphology coherence, null-corrected (random-signature z)",
        "seed": SEED, "n_tokens": N_TOKENS, "n_null": B_NULL, "lang_z_threshold": LANG_Z,
        "corpus_z": stats,
        "calibration_ok": calibration_ok,
        "vms_currierA_z": zof("vms_currierA"), "vms_currierB_z": zof("vms_currierB"),
        "vms_currierA_class": va, "vms_currierB_class": vb, "ab_same_class": va == vb,
    }
    results["grade"], results["verdict"] = _verdict(results, stats)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e15b_morphology_corrected.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict, stats: dict) -> tuple:
    za, zb = r["vms_currierA_z"], r["vms_currierB_z"]
    a, b = r["vms_currierA_class"], r["vms_currierB_class"]
    ref = ", ".join(f"{c} z={stats[c]['z']}" for c in ("latin", "conlang_relex_latin",
                    "abjad_latin", "latin_charshuffled") if stats[c].get("z") is not None)
    base = (f"Null-corrected (random-signature) coherence z — VMS-A={za} ({a}), "
            f"VMS-B={zb} ({b}); threshold {r['lang_z_threshold']}. Reference: {ref}.")
    if not r["calibration_ok"]:
        return "D", (f"INCONCLUSIVE — the corrected probe is not calibrated (real "
                     f"inflection must clear and collision nulls must not). {base}")
    if a == b == "paradigmatic":
        return "C", (
            f"BOTH Currier systems have PRODUCTIVE PARADIGMATIC morphology beyond random "
            f"signature assignment — stems non-randomly share suffix SETS, like an "
            f"inflecting language, in A AND B. Nuisance-corrected (n held fixed), so not "
            f"an n-artifact. Sharpens F12: the dense ED1 network reflects real paradigms, "
            f"not mere abjad collision. {base} (Grammar only; no meaning — L7.)")
    if a != b:
        return "C", (
            f"A and B DIFFER in null-corrected morphological coherence (A {a}, B {b}) — "
            f"evidence the two Currier systems are morphologically different processes. "
            f"{base} (L7.)")
    return "C", (
        f"NEITHER Currier system shows paradigm coherence beyond random signature "
        f"assignment (A {a}, B {b}) — the ED1 network is collision-like, not productive "
        f"paradigmatic morphology. {base} (L7.)")


if __name__ == "__main__":
    out = run()
    print(f"{'corpus':22s} {'obs':>7s} {'null_mean':>9s} {'z':>8s} {'#stems':>7s}")
    for c, s in out["corpus_z"].items():
        if s.get("insufficient"):
            print(f"{c:22s} insufficient")
            continue
        print(f"{c:22s} {s['observed']:>7} {s['null_mean']:>9} {str(s['z']):>8} {s['n_stems']:>7}")
    print(f"\ncalibration_ok={out['calibration_ok']}")
    print(f"VMS-A z={out['vms_currierA_z']} ({out['vms_currierA_class']}) | "
          f"VMS-B z={out['vms_currierB_z']} ({out['vms_currierB_class']})")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
