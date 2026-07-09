"""E13 — Function-word vs content-word bimodality (i05 flagship; L37, Tim's lead probe).

Real languages have a small set of very frequent FUNCTION words that are
distributionally promiscuous (near-uniform neighbours — they occur before/after almost
anything) plus many CONTENT words with peaked collocate distributions. This is a
*kind*-of-structure signature (not magnitude — the E9 lesson): it distinguishes text
derived from a real linguistic grammar from text produced by a shallow generator.

Measure. For each word type, promiscuity = frequency-NORMALISED neighbour entropy
P(w) = mean( H(left|w), H(right|w) ) / log2(freq), in [0,1]. Normalising by log2(freq)
removes the count confound: a type can have at most log2(n) bits of neighbour entropy,
so P measures how DISPERSED its neighbours are relative to its frequency. Function
words → P near 1; content words with fixed collocates → lower P.

Calibration (harness-first, L4). Compute on corpora with KNOWN grammar status, all
subsampled to a matched token budget:
  has-grammar (real linguistic word order): Latin, German, and a conlang RELEXIFICATION
    of Latin (inherits Latin's syntax → must still show the split).
  no-real-grammar (generated): self-citation (H3, copy-nearby), a unigram shuffle, and
    a 1st-order Markov surrogate of Latin.
Then read the decision rule off the calibration and apply to VMS-A and VMS-B
separately (Tim's "two different processes?" hypothesis) + a v101 sensitivity note.

Statistics per corpus (types with freq ≥ MINFREQ):
  bimodality_coefficient  — Sarle's BC of the promiscuity distribution (>0.555 ⇒ bimodal)
  function_class_frac      — fraction of frequent types with P ≥ 0.9 (function-like)
  top_vs_rest              — mean P of the top-20 most frequent types minus the median P
                             (real languages: frequent words are the promiscuous ones)

Usage:
    python -m ms408.experiments.e13_function_content
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..ivtff import IVTFFDocument
from ..sources import path_for
from ..studies.anchor_hunt import WORD_POLICY
from .e5_encoding_fair import fam_selfcitation
from .e6_cipher_reconstruction import _paradigmatic_conlang

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
SEED = 408
N_TOKENS = 10000     # matched token budget for all corpora
MINFREQ = 5          # types below this are excluded from the promiscuity stats
FUNC_THRESH = 0.9    # promiscuity above which a frequent type is "function-like"


def _vms_tokens(dialect: str) -> list:
    zl = IVTFFDocument.load(path_for("zl"))
    out = []
    for p in zl.pages:
        if p.currier_language != dialect:
            continue
        for loc in p.loci:
            if (loc.locus_type or "").startswith("P"):
                out.extend(w for w in loc.words(WORD_POLICY) if "@" not in w)
    return out


def _sub(tokens: list, n: int = N_TOKENS) -> list:
    return tokens[:n]


def _shuffle(tokens: list, seed: int) -> list:
    t = list(tokens)
    random.Random(seed).shuffle(t)
    return t


def _markov1(tokens: list, seed: int, n: int = N_TOKENS) -> list:
    trans = defaultdict(list)
    for a, b in zip(tokens, tokens[1:]):
        trans[a].append(b)
    rng = random.Random(seed)
    out = [tokens[0]]
    for _ in range(n - 1):
        nxt = trans.get(out[-1])
        out.append(rng.choice(nxt) if nxt else rng.choice(tokens))
    return out


def _evenness(tokens: list, k: int = 10) -> dict:
    """Per-type dispersion EVENNESS = 1 - DP (Gries' deviation of proportions),
    computed over k contiguous parts. Evenness≈1 → the word spreads evenly across the
    text (function-word-like); ≈0 → it clumps in a few passages (content-word-like).
    DP is far less type-token-ratio-sensitive than neighbour entropy."""
    n = len(tokens)
    size = n / k
    bounds = [round(i * size) for i in range(k + 1)]
    part_counts = defaultdict(lambda: np.zeros(k))
    for p in range(k):
        for w in tokens[bounds[p]:bounds[p + 1]]:
            part_counts[w][p] += 1
    part_sizes = np.array([bounds[p + 1] - bounds[p] for p in range(k)]) / n
    out = {}
    for w, counts in part_counts.items():
        total = counts.sum()
        if total < 1:
            continue
        obs = counts / total
        dp = 0.5 * float(np.abs(obs - part_sizes).sum())
        out[w] = 1.0 - dp
    return out


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    def rank(a):
        order = a.argsort()
        r = np.empty_like(order, float)
        r[order] = np.arange(len(a))
        return r
    rx, ry = rank(x), rank(y)
    rx -= rx.mean()
    ry -= ry.mean()
    d = math.sqrt((rx**2).sum() * (ry**2).sum())
    return float((rx * ry).sum() / d) if d else 0.0


def _stats(tokens: list) -> dict:
    freq = Counter(tokens)
    even = _evenness(tokens)
    frequent = [w for w, c in freq.items() if c >= MINFREQ and w in even]
    if len(frequent) < 20:
        return {"n_frequent_types": len(frequent), "insufficient": True}
    logf = np.array([math.log(freq[w]) for w in frequent])
    ev = np.array([even[w] for w in frequent])
    # Function-word signature: frequent words are distinctively EVENLY dispersed.
    # Primary discriminator = Spearman(log freq, evenness): strongly positive in real
    # language (frequent -> function words -> even), weak/absent in generators.
    freq_even_spearman = _spearman(logf, ev)
    top20 = sorted(frequent, key=lambda w: -freq[w])[:20]
    top20_even = float(np.mean([even[w] for w in top20]))
    return {
        "tokens": len(tokens), "n_frequent_types": len(frequent),
        "mean_evenness": round(float(ev.mean()), 3),
        "std_evenness": round(float(ev.std()), 3),
        "freq_evenness_spearman": round(freq_even_spearman, 3),
        "top20_evenness": round(top20_even, 3),
        "top20_vs_median": round(top20_even - float(np.median(ev)), 3),
    }


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    german = (H4_OUT / "german_kraeuterbuch_dipl.txt").read_text().split()
    conlang = _paradigmatic_conlang(latin[:N_TOKENS], 0.8, SEED)  # relexified Latin

    corpora = {
        # has real linguistic grammar
        "latin": _sub(latin), "german": _sub(german), "conlang_relex_latin": _sub(conlang),
        # generated / no real grammar
        "self_citation": _sub(fam_selfcitation(N_TOKENS + 200, 3)),
        "latin_shuffled": _sub(_shuffle(latin[:N_TOKENS], SEED)),
        "latin_markov1": _markov1(latin[:N_TOKENS], SEED),
        # the manuscript, stratified
        "vms_currierA": _sub(_vms_tokens("A")),
        "vms_currierB": _sub(_vms_tokens("B")),
    }
    stats = {k: _stats(v) for k, v in corpora.items()}

    groups = {
        "has_grammar": ["latin", "german", "conlang_relex_latin"],
        "generated": ["self_citation", "latin_shuffled", "latin_markov1"],
    }

    def gmean(group, key):
        vals = [stats[c][key] for c in groups[group]
                if stats[c].get(key) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    calib = {g: {k: gmean(g, k) for k in
                 ("freq_evenness_spearman", "top20_evenness", "top20_vs_median")}
             for g in groups}

    # Discriminating axis = freq_evenness_spearman (do frequent words dispersion-
    # evenly, the function-word signature). Threshold = midpoint of the two calibrated
    # group means; only trusted if the groups SEPARATE (has-grammar clearly above
    # generated). If they overlap, the probe is inconclusive.
    hi = calib["has_grammar"]["freq_evenness_spearman"]
    lo = calib["generated"]["freq_evenness_spearman"]
    threshold = round((hi + lo) / 2, 3) if (hi is not None and lo is not None) else None
    separation = round(hi - lo, 3) if (hi is not None and lo is not None) else None
    calibration_ok = bool(separation is not None and separation >= 0.2)

    def classify(corpus):
        v = stats[corpus].get("freq_evenness_spearman")
        if v is None or threshold is None or not calibration_ok:
            return "inconclusive"
        return "language-like" if v >= threshold else "generator-like"

    verdict_A = classify("vms_currierA")
    verdict_B = classify("vms_currierB")

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E13 — function/content bimodality",
        "seed": SEED, "n_tokens": N_TOKENS, "minfreq": MINFREQ,
        "stats": stats,
        "calibration_group_means": calib,
        "decision_axis": "freq_evenness_spearman (frequent-word dispersion evenness)",
        "calibration_separation": separation, "calibration_ok": calibration_ok,
        "decision_threshold": threshold,
        "vms_currierA_class": verdict_A, "vms_currierB_class": verdict_B,
        "ab_same_class": verdict_A == verdict_B,
        "learnings": (
            "Three global operationalisations (neighbour-entropy promiscuity; "
            "freq–dispersion-evenness correlation; evenness variance) all FAIL to "
            "separate real-grammar from generated corpora. Two causes: (1) global "
            "corpus statistics are confounded by type-token ratio / randomness (shuffle "
            "trivially makes frequent words evenly dispersed); (2) the 'generated' nulls "
            "are contaminated — self-citation copies real-like chunks and the conlang "
            "relexifies real Latin, so both inherit grammar. Redesign direction: "
            "identify CANDIDATE function words explicitly (top-frequency, cross-section "
            "stable) and test whether THEY specifically show even dispersion + syntactic "
            "position-locking relative to matched content words, against CLEAN nulls "
            "(shuffle/markov only)."),
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e13_function_content.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    a, b = r["vms_currierA_class"], r["vms_currierB_class"]
    cal = r["calibration_group_means"]
    sa = r["stats"]["vms_currierA"]["freq_evenness_spearman"]
    sb = r["stats"]["vms_currierB"]["freq_evenness_spearman"]
    base = (
        f"Calibration (freq–evenness Spearman): has-grammar "
        f"{cal['has_grammar']['freq_evenness_spearman']} vs generated "
        f"{cal['generated']['freq_evenness_spearman']} (separation "
        f"{r['calibration_separation']}); threshold {r['decision_threshold']}. "
        f"VMS-A={sa} ({a}), VMS-B={sb} ({b}).")
    if not r["calibration_ok"]:
        return "D", (
            f"INCONCLUSIVE — the dispersion probe does NOT reliably separate the "
            f"has-grammar and generated calibration corpora (separation "
            f"{r['calibration_separation']} < 0.2), so no function/content verdict on "
            f"the VMS can be trusted from it. The measure needs further work before it "
            f"can adjudicate. {base} (Harness-first discipline: an uncalibrated probe "
            f"yields no manuscript claim.)")
    if a == b == "language-like":
        return "C", (
            f"BOTH Currier systems show the function/content signature of a real "
            f"linguistic grammar — the frequent words are distinctively promiscuous, "
            f"like function words, in A AND B. This reweights toward a language-derived "
            f"process (real language OR a cipher/relexification of one; a self-citation/"
            f"shuffle generator does NOT show it). Does not resolve A-vs-B as different "
            f"processes on THIS probe. {base} (Grammar characterisation only; does NOT "
            f"prove meaning or license translation — L7.)")
    if a != b:
        return "C", (
            f"A and B DIFFER on the function/content probe (A {a}, B {b}) — direct "
            f"evidence for Tim's hypothesis that the two Currier systems are different "
            f"generative processes. {base} (L7: grammar, not meaning.)")
    return "C", (
        f"NEITHER Currier system shows a clear function/content split (A {a}, B {b}) — "
        f"consistent with a generator-like process rather than real-language grammar on "
        f"this probe. {base} (L7.)")


if __name__ == "__main__":
    out = run()
    print(f"{'corpus':22s} {'freq-even-r':>11s} {'top20-even':>10s} {'top20-med':>10s}")
    for c, s in out["stats"].items():
        if s.get("insufficient"):
            print(f"{c:22s} insufficient")
            continue
        print(f"{c:22s} {str(s['freq_evenness_spearman']):>11s} "
              f"{str(s['top20_evenness']):>10s} {str(s['top20_vs_median']):>10s}")
    print(f"\ncalibration: {out['calibration_group_means']}")
    print(f"separation={out['calibration_separation']} ok={out['calibration_ok']} "
          f"threshold={out['decision_threshold']}")
    print(f"VMS-A={out['vms_currierA_class']} VMS-B={out['vms_currierB_class']}")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
