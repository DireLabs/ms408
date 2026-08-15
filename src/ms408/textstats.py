"""Deterministic text statistics (the scoring core of the validation harness).

Pure functions: word list in, numbers out. No corpus knowledge, no I/O — corpus
assembly and provenance live in ms408.benchmark. Every reported number in the
program flows through here or a sibling module (L3 firewall).

Character entropies are computed within words only (no cross-word bigrams),
matching the method used by Lindemann & Bowern (arXiv:2010.14697) and the
Naibbe reference statistics (spec T03-naibbe §8).
"""

from __future__ import annotations

import math
from collections import Counter


def char_unigram_entropy(words: list) -> float:
    """h1: Shannon entropy (bits) of the character distribution inside words."""
    counts = Counter(c for w in words for c in w)
    total = sum(counts.values())
    return -sum((n / total) * math.log2(n / total) for n in counts.values())


def char_conditional_entropy(words: list) -> float:
    """WITHIN-WORD conditional character entropy: H(next char | previous char) over
    word-internal adjacent pairs only.

    NOT the same statistic as the `h2` the evaluator bands, and the two are routinely
    confused because both get called "h2" in the literature. This one excludes the space
    and never crosses a word boundary; `lb_entropies` (Lindemann & Bowern) includes the
    space as a character and lets bigrams span boundaries. They give materially different
    numbers on the same text. Use this one only where the reference statistic being
    matched is itself within-word (e.g. the Naibbe comparisons); use `lb_entropies` for
    anything compared against the reference bands or the T1.1 entropy targets. Always say
    which convention a reported h2 uses.
    """
    pair_counts: Counter = Counter()
    first_counts: Counter = Counter()
    for w in words:
        for a, b in zip(w, w[1:]):
            pair_counts[(a, b)] += 1
            first_counts[a] += 1
    total = sum(pair_counts.values())
    h = 0.0
    for (a, _), n in pair_counts.items():
        p_pair = n / total
        p_cond = n / first_counts[a]
        h -= p_pair * math.log2(p_cond)
    return h


def lb_entropies(words: list) -> tuple:
    """(h1, h2) per Lindemann & Bowern: spaces INCLUDED as a character, bigrams
    span word boundaries, h2 = H2 - H1 (plug-in, bits, no smoothing).

    Spec: docs/planning/i01/specs/T11-entropy-targets.md §1. This differs from
    char_conditional_entropy above, which is the within-word convention used by
    the Naibbe reference statistics.
    """
    text = " ".join(words)
    n = len(text)
    unigram_counts = Counter(text)
    h1 = -sum((c / n) * math.log2(c / n) for c in unigram_counts.values())
    bigram_counts = Counter(text[i : i + 2] for i in range(n - 1))
    n2 = n - 1
    big_h2 = -sum((c / n2) * math.log2(c / n2) for c in bigram_counts.values())
    return h1, big_h2 - h1


def zipf_slope(words: list, min_rank: int = 10, max_rank: int = 1000) -> float | None:
    """Log-log slope of the rank-frequency curve over [min_rank, max_rank].

    Least-squares fit; None if fewer than min_rank + 10 types.
    """
    freqs = sorted(Counter(words).values(), reverse=True)
    hi = min(max_rank, len(freqs))
    if hi < min_rank + 10:
        return None
    xs = [math.log10(r) for r in range(min_rank, hi + 1)]
    ys = [math.log10(freqs[r - 1]) for r in range(min_rank, hi + 1)]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    denominator = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denominator


def _average_ranks(values: list) -> list:
    """Ranks (1-based) with ties assigned their average rank."""
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        average = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = average
        i = j + 1
    return ranks


def spearman(xs: list, ys: list) -> float:
    """Spearman rank correlation (average ranks for ties)."""
    rx, ry = _average_ranks(xs), _average_ranks(ys)
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0 or vy == 0:
        return 0.0
    return cov / math.sqrt(vx * vy)


def abbreviation_rho(words: list) -> float:
    """Zipf's law of abbreviation: Spearman corr(type frequency, type length).

    Negative for natural languages (frequent words are shorter).
    """
    counts = Counter(words)
    types = list(counts)
    return spearman([counts[t] for t in types], [len(t) for t in types])


def word_length_distribution(words: list) -> dict:
    counts = Counter(len(w) for w in words)
    total = len(words)
    return {length: counts[length] / total for length in sorted(counts)}


def tv_distance(p: dict, q: dict) -> float:
    """Total-variation distance between two discrete distributions."""
    keys = set(p) | set(q)
    return sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys) / 2


def summarize(words: list) -> dict:
    """The standard metric block computed for every harness corpus."""
    total_chars = sum(len(w) for w in words)
    return {
        "tokens": len(words),
        "types": len(set(words)),
        "mean_word_length": round(total_chars / len(words), 4),
        "char_inventory": len({c for w in words for c in w}),
        "h1": round(char_unigram_entropy(words), 4),
        "h2": round(char_conditional_entropy(words), 4),
        "zipf_slope": (
            round(s, 4) if (s := zipf_slope(words)) is not None else None
        ),
        "abbreviation_rho": round(abbreviation_rho(words), 4),
        "word_length_distribution": {
            str(k): round(v, 5) for k, v in word_length_distribution(words).items()
        },
    }
