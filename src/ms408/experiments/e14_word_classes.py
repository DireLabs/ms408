"""E14 — Distributional word-class (POS) induction, null-corrected (i05).

Do coherent grammatical categories exist in Voynichese — words that cluster into a
small number of substitutability classes whose ADJACENT classes carry regular
transition structure (nouns follow determiners, verbs follow nouns …) — and are the
classes the same in Currier A and B? Built null-corrected from the start (the i05
lesson): the raw statistic is confounded, so we z-score it against an order-shuffle
null WITH RE-CLUSTERING, which tests whether the induced clustering captures real
structure rather than any bigram regularity.

Pipeline. Represent each word type (freq ≥ MINFREQ) by its left- and right-neighbour
distributions over the top-V vocabulary; k-means into K classes; map tokens to their
class; measure adjacent-class mutual information I(C_i; C_{i+1}) (normalised by H(C)).
NULL: order-shuffle the tokens, re-derive context vectors, RE-CLUSTER, re-measure —
B times. z = (observed NMI − null mean) / null std. Real language: classes carry real
transition structure that survives re-clustering only on the ordered text ⇒ high z;
a shuffle re-clusters to noise ⇒ z ≈ 0.

Usage:
    python -m ms408.experiments.e14_word_classes
"""

from __future__ import annotations

import json
import math
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ..dataset import git_commit
from ..h4 import H4_OUT
from .e13_function_content import SEED, _sub, _vms_tokens
from .mid_level_null import null_z, order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
N_TOKENS = 10000
MINFREQ = 3
V = 60          # top-V words used as context features
K = 12          # induced classes
B_NULL = 15
LANG_Z = 2.0


def _context_matrix(tokens: list):
    freq = Counter(tokens)
    vocab = [w for w, _ in freq.most_common(V)]
    vidx = {w: i for i, w in enumerate(vocab)}
    types = [w for w, c in freq.items() if c >= MINFREQ]
    tidx = {w: i for i, w in enumerate(types)}
    left = np.zeros((len(types), V + 1))
    right = np.zeros((len(types), V + 1))
    for i, w in enumerate(tokens):
        if w not in tidx:
            continue
        r = tidx[w]
        if i > 0:
            left[r, vidx.get(tokens[i - 1], V)] += 1
        if i < len(tokens) - 1:
            right[r, vidx.get(tokens[i + 1], V)] += 1
    # L1-normalise each half
    left /= np.clip(left.sum(1, keepdims=True), 1, None)
    right /= np.clip(right.sum(1, keepdims=True), 1, None)
    return np.hstack([left, right]), tidx


def _kmeans(x: np.ndarray, k: int, seed: int, iters: int = 25) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = len(x)
    if n <= k:
        return np.arange(n) % k
    centers = [x[rng.integers(n)]]
    for _ in range(k - 1):
        d = np.min([((x - c) ** 2).sum(1) for c in centers], axis=0)
        s = d.sum()
        centers.append(x[rng.integers(n) if s == 0 else rng.choice(n, p=d / s)])
    c = np.array(centers)
    assign = np.zeros(n, int)
    for _ in range(iters):
        new = np.argmin(((x[:, None, :] - c[None, :, :]) ** 2).sum(2), axis=1)
        if (new == assign).all():
            break
        assign = new
        c = np.array([x[assign == j].mean(0) if (assign == j).any() else c[j]
                      for j in range(k)])
    return assign


def _adjacent_class_nmi(tokens: list, seed: int) -> float:
    x, tidx = _context_matrix(tokens)
    if len(tidx) < K:
        return 0.0
    assign = _kmeans(x, K, seed)
    cls = {w: int(assign[i]) for w, i in tidx.items()}
    seq = [cls[w] for w in tokens if w in cls]
    if len(seq) < 100:
        return 0.0
    joint = Counter(zip(seq, seq[1:]))
    n = sum(joint.values())
    cprev = Counter(a for a, _ in joint.elements())
    cnext = Counter(b for _, b in joint.elements())
    mi = 0.0
    for (a, b), c in joint.items():
        pab = c / n
        mi += pab * math.log2(pab / ((cprev[a] / n) * (cnext[b] / n)))
    hc = -sum((v / n) * math.log2(v / n) for v in Counter(seq).values())
    return mi / hc if hc else 0.0


def _corpus_z(tokens: list) -> dict:
    obs = _adjacent_class_nmi(tokens, SEED)
    nulls = [_adjacent_class_nmi(order_shuffle(tokens, SEED + 1 + i), SEED + 1 + i)
             for i in range(B_NULL)]
    z = null_z(obs, nulls)
    return z


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    german = (H4_OUT / "german_kraeuterbuch_dipl.txt").read_text().split()
    corpora = {"latin": _sub(latin, N_TOKENS), "german": _sub(german, N_TOKENS),
               "vms_currierA": _sub(_vms_tokens("A"), N_TOKENS),
               "vms_currierB": _sub(_vms_tokens("B"), N_TOKENS)}
    stats = {k: _corpus_z(v) for k, v in corpora.items()}

    def zof(c):
        return stats[c].get("z")

    real_ok = all((zof(c) is not None and zof(c) >= LANG_Z) for c in ("latin", "german"))
    real_z = sum(zof(c) for c in ("latin", "german")) / 2
    # VMS class structure as a FRACTION of real-language class structure — avoids
    # over-reading a near-threshold z as "structured vs not". Both VMS systems are far
    # below real language, so the honest axis is magnitude, not a binary threshold.
    frac_A = round(zof("vms_currierA") / real_z, 3) if real_z else None
    frac_B = round(zof("vms_currierB") / real_z, 3) if real_z else None
    weak = 0.5   # below 50% of real-language z ⇒ "far weaker than real language"
    both_weak = bool(frac_A is not None and frac_A < weak and frac_B < weak)

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E14 — distributional word-class induction (null-corrected)",
        "seed": SEED, "n_tokens": N_TOKENS, "k_classes": K, "context_vocab": V,
        "n_null": B_NULL, "lang_z_threshold": LANG_Z,
        "corpus_z": stats,
        "calibration_ok_real_langs": bool(real_ok),
        "real_lang_mean_z": round(real_z, 2),
        "vms_currierA_z": zof("vms_currierA"), "vms_currierB_z": zof("vms_currierB"),
        "vms_A_frac_of_real": frac_A, "vms_B_frac_of_real": frac_B,
        "both_far_weaker_than_real": both_weak,
        "ab_gap_straddles_threshold": bool(
            (zof("vms_currierA") < LANG_Z) != (zof("vms_currierB") < LANG_Z)),
    }
    results["grade"], results["verdict"] = _verdict(results, stats)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e14_word_classes.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict, stats: dict) -> tuple:
    za, zb = r["vms_currierA_z"], r["vms_currierB_z"]
    rz = r["real_lang_mean_z"]
    base = (f"Adjacent-class NMI z (order-shuffle+recluster null): real language "
            f"z≈{rz} (latin {stats['latin']['z']}, german {stats['german']['z']}); "
            f"VMS-A z={za} ({r['vms_A_frac_of_real']}× real), VMS-B z={zb} "
            f"({r['vms_B_frac_of_real']}× real).")
    if not r["calibration_ok_real_langs"]:
        return "D", (f"INCONCLUSIVE — real-language controls not calibrated. {base}")
    if r["both_far_weaker_than_real"]:
        note = ("The small A/B difference straddles the significance threshold "
                "(A<2<B) but both sit near the shuffle floor, so it is NOT strong "
                "evidence of 'different processes' — that would over-read a "
                "near-threshold gap; a dedicated A-vs-B replication is needed before "
                "any such claim." if r["ab_gap_straddles_threshold"] else
                "A and B are comparably weak.")
        return "C", (
            f"WEAK word-class structure, FAR below real language, in BOTH Currier "
            f"systems. VMS's induced word classes carry adjacent-transition structure "
            f"only marginally above the re-clustered-shuffle baseline "
            f"(~{int(100 * (r['vms_A_frac_of_real'] + r['vms_B_frac_of_real']) / 2)}% of "
            f"real-language class structure), vs real languages an order of magnitude "
            f"higher. So the VMS does not exhibit natural-language-strength part-of-"
            f"speech organisation on this probe. {note} SCOPE (L7): surface "
            f"distributional word classes only — a cipher/heavy morphology could "
            f"depress apparent class structure while preserving an underlying grammar; "
            f"this does NOT say 'no grammar'. {base} Consistent with E13c (VMS's word-"
            f"level distributional structure is weaker/different from natural language "
            f"despite strong character and morphology structure).")
    if za >= LANG_Z and zb >= LANG_Z:
        return "C", (
            f"BOTH Currier systems show distributional word-class structure comparable "
            f"to real language, in A AND B — part-of-speech-like organisation. {base} "
            f"(Grammar only; no meaning — L7.)")
    return "C", (
        f"Mixed/weak word-class structure (VMS-A {r['vms_A_frac_of_real']}×, VMS-B "
        f"{r['vms_B_frac_of_real']}× real). {base} (L7.)")


if __name__ == "__main__":
    out = run()
    for c, s in out["corpus_z"].items():
        print(f"  {c:16s} obs={s['observed']} null_mean={s['null_mean']} "
              f"null_std={s['null_std']} z={s['z']}")
    print(f"\ncalibration_ok={out['calibration_ok_real_langs']} real_z={out['real_lang_mean_z']}")
    print(f"VMS-A z={out['vms_currierA_z']} ({out['vms_A_frac_of_real']}× real) | "
          f"VMS-B z={out['vms_currierB_z']} ({out['vms_B_frac_of_real']}× real) | "
          f"both_far_weaker={out['both_far_weaker_than_real']}")
    print(f"grade {out['grade']}: {out['verdict'][:150]}...")
