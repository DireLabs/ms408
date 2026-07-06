"""Montemurro-Zanette "information in the distribution of words" (T1.1).

Reimplements the ΔI(s) measure of Montemurro & Zanette 2013 (PLoS ONE 8(6):e66344),
per the method spec in docs/planning/i01/specs/T11-montemurro-targets.md:

    ΔI(s) = Σ_w p(w) [ ⟨Ĥ(J|w)⟩ − H(J|w) ]        (bits per word)

where the text is cut into P contiguous parts of s = N//P words, H(J|w) is the
entropy of word w's distribution over parts (Eq. 3), and the shuffled baseline
⟨Ĥ(J|w)⟩ is the ANALYTIC hypergeometric closed form (their 2010 Appendix C) —
no Monte-Carlo needed (but see tests, which validate the closed form against a
shuffle average).

Published targets: peak scale ≈ 807 words for the Voynich text; natural languages
peak at ~600-800 words; max ΔI between ~0.2 (Latin) and ~0.6 (Chinese) bits/word,
Voynich slightly above English.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from functools import lru_cache


@lru_cache(maxsize=None)
def expected_shuffled_entropy(n: int, total: int, parts: int) -> float:
    """⟨Ĥ(J|w)⟩ for a word of frequency n in a text of `total` tokens cut into
    `parts` parts of size s = total // parts (hypergeometric closed form).

    ⟨Ĥ⟩ = −P · Σ_{m=1..min(n,s)} p(m) · (m/n) · log2(m/n)
    p(m) = C(n,m) C(N−n, s−m) / C(N,s)
    """
    size = total // parts
    # p(0) = C(N-n, s) / C(N, s), computed in log space
    log_p = sum(
        math.log((total - n - i) / (total - i)) for i in range(size)
    ) if total - n >= size else -math.inf
    p = math.exp(log_p)
    expected = 0.0
    for m in range(1, min(n, size) + 1):
        # recurrence: p(m)/p(m-1) = (n-m+1)(s-m+1) / (m (N-n-s+m))
        denominator = m * (total - n - size + m)
        if denominator <= 0:
            break
        p = p * (n - m + 1) * (size - m + 1) / denominator
        if m < n:
            expected -= p * (m / n) * math.log2(m / n)
    return parts * expected


def word_part_entropies(tokens: list, parts: int) -> dict:
    """H(J|w) per word type (Eq. 3), on the text truncated to parts*size tokens."""
    size = len(tokens) // parts
    truncated = tokens[: parts * size]
    per_part: dict = defaultdict(Counter)
    for i, token in enumerate(truncated):
        per_part[token][i // size] += 1
    entropies = {}
    for word, counts in per_part.items():
        n = sum(counts.values())
        entropies[word] = -sum(
            (c / n) * math.log2(c / n) for c in counts.values()
        )
    return entropies


def delta_information(tokens: list, parts: int) -> tuple:
    """(ΔI(s) in bits/word, per-word contributions dict) for a given part count."""
    size = len(tokens) // parts
    total = parts * size
    truncated = tokens[:total]
    frequencies = Counter(truncated)
    real_entropies = word_part_entropies(truncated, parts)
    per_word = {}
    for word, n in frequencies.items():
        expected = expected_shuffled_entropy(n, total, parts)
        per_word[word] = (n / total) * (expected - real_entropies[word])
    return sum(per_word.values()), per_word


def scan_scales(tokens: list, part_counts: tuple | None = None) -> list:
    """ΔI across a sweep of part counts. Returns [(scale_words, parts, delta_bits)]."""
    n = len(tokens)
    if part_counts is None:
        part_counts = tuple(
            p for p in (2, 3, 4, 5, 6, 8, 10, 12, 14, 17, 21, 25, 30, 36, 42,
                        50, 60, 72, 85, 100, 120, 145, 170, 200, 240, 300)
            if n // p >= 20
        )
    return [(n // p, p, delta_information(tokens, p)[0]) for p in part_counts]


def peak(scan: list) -> tuple:
    """(scale_words, parts, delta_bits) at the maximum of a scan."""
    return max(scan, key=lambda row: row[2])


def top_informative_words(tokens: list, target_scale: int = 807, k: int = 30) -> list:
    """Top-k words by per-word ΔI at the part count closest to the target scale."""
    n = len(tokens)
    parts = max(2, round(n / target_scale))
    _, per_word = delta_information(tokens, parts)
    ranked = sorted(per_word.items(), key=lambda item: item[1], reverse=True)
    return [(word, round(value, 6)) for word, value in ranked[:k]]
