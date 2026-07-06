"""Validate the Montemurro-Zanette implementation.

The critical check (spec T11-montemurro §checklist step 3): the analytic
hypergeometric baseline must agree with a Monte-Carlo shuffle average.
"""

import math
import random
import statistics

from ms408.mz import (
    delta_information,
    expected_shuffled_entropy,
    peak,
    scan_scales,
    word_part_entropies,
)


def _entropy_of_counts(counts):
    n = sum(counts)
    return -sum((c / n) * math.log2(c / n) for c in counts if c)


class TestAnalyticBaseline:
    def test_matches_monte_carlo(self):
        rng = random.Random(0)
        total, parts, n = 1200, 6, 40
        size = total // parts
        positions = list(range(total))
        samples = []
        for _ in range(3000):
            chosen = rng.sample(positions, n)
            counts = [0] * parts
            for pos in chosen:
                counts[pos // size] += 1
            samples.append(_entropy_of_counts(counts))
        analytic = expected_shuffled_entropy(n, total, parts)
        assert abs(analytic - statistics.mean(samples)) < 0.01

    def test_frequency_one_word_contributes_zero(self):
        # a hapax has H = 0 in real text and ⟨Ĥ⟩ = 0: log2(1/1) = 0
        assert expected_shuffled_entropy(1, 1000, 5) == 0.0

    def test_uniform_upper_bound(self):
        # ⟨Ĥ⟩ can never exceed log2(P)
        for n in (5, 50, 500):
            assert expected_shuffled_entropy(n, 2000, 8) <= math.log2(8) + 1e-9


class TestDeltaInformation:
    def test_clustered_text_beats_shuffled_text(self):
        rng = random.Random(1)
        # clustered: each "topic word" concentrated in one block
        clustered = []
        for block in range(6):
            clustered.extend(
                [f"topic{block}" if rng.random() < 0.3 else f"common{rng.randrange(20)}"
                 for _ in range(500)]
            )
        shuffled = clustered[:]
        rng.shuffle(shuffled)
        delta_clustered, _ = delta_information(clustered, 6)
        delta_shuffled, _ = delta_information(shuffled, 6)
        assert delta_clustered > 5 * max(delta_shuffled, 1e-9)
        assert delta_shuffled < 0.02  # shuffled text carries ~no ordering information

    def test_topic_words_rank_top(self):
        rng = random.Random(2)
        tokens = []
        for block in range(4):
            tokens.extend(
                [f"topic{block}" if rng.random() < 0.25 else f"common{rng.randrange(10)}"
                 for _ in range(400)]
            )
        _, per_word = delta_information(tokens, 4)
        top4 = sorted(per_word, key=per_word.get, reverse=True)[:4]
        assert set(top4) == {f"topic{i}" for i in range(4)}

    def test_word_part_entropy_bounds(self):
        tokens = ["a"] * 100 + ["b"] * 100
        entropies = word_part_entropies(tokens, 2)
        assert entropies["a"] == 0.0  # 'a' entirely in part 0
        uniform = ["a", "b"] * 100
        entropies = word_part_entropies(uniform, 2)
        assert abs(entropies["a"] - 1.0) < 1e-9  # evenly split over 2 parts


class TestScan:
    def test_peak_at_block_scale(self):
        rng = random.Random(3)
        block_size = 300
        tokens = []
        for block in range(10):
            tokens.extend(
                [f"topic{block}" if rng.random() < 0.3 else f"common{rng.randrange(15)}"
                 for _ in range(block_size)]
            )
        scan = scan_scales(tokens)
        scale, _, value = peak(scan)
        # information should peak near the planted block scale, not at extremes
        assert 100 <= scale <= 1500
        assert value > 0.05
