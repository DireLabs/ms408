import math
import random

from ms408.textstats import (
    abbreviation_rho,
    char_conditional_entropy,
    char_unigram_entropy,
    spearman,
    summarize,
    tv_distance,
    word_length_distribution,
    zipf_slope,
)


class TestEntropy:
    def test_uniform_unigram(self):
        # 4 equiprobable characters -> exactly 2 bits
        words = ["ab", "cd"] * 100
        assert math.isclose(char_unigram_entropy(words), 2.0)

    def test_deterministic_successor_has_zero_conditional_entropy(self):
        # every 'a' is followed by 'b', every 'b' by 'c': h2 == 0
        assert char_conditional_entropy(["abc"] * 50) == 0.0

    def test_random_text_h2_near_h1(self):
        rng = random.Random(1)
        alphabet = "abcdefgh"
        words = ["".join(rng.choice(alphabet) for _ in range(8)) for _ in range(4000)]
        h1 = char_unigram_entropy(words)
        h2 = char_conditional_entropy(words)
        assert abs(h1 - 3.0) < 0.01  # 8 equiprobable chars
        assert abs(h2 - h1) < 0.05  # independence: conditioning gains nothing

    def test_boundaries_excluded(self):
        # single-char words contribute nothing to h2
        assert char_conditional_entropy(["a", "b", "c"] * 10) == 0.0


class TestZipf:
    def test_power_law_slope_recovered(self):
        # freq(rank) = C * rank^-1 -> slope ~ -1
        words = []
        for rank in range(1, 1500):
            words.extend([f"w{rank}"] * max(1, int(30000 / rank)))
        slope = zipf_slope(words)
        assert slope is not None and abs(slope + 1.0) < 0.05

    def test_too_small_returns_none(self):
        assert zipf_slope(["a", "b", "c"]) is None


class TestSpearman:
    def test_perfect_monotone(self):
        assert math.isclose(spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        assert math.isclose(spearman([1, 2, 3, 4], [8, 6, 4, 2]), -1.0)

    def test_constant_input(self):
        assert spearman([1, 1, 1], [1, 2, 3]) == 0.0

    def test_abbreviation_negative_for_zipfian_text(self):
        # frequent short words, rare long words
        words = ["ab"] * 500 + ["cdef"] * 50 + ["ghijkl"] * 5
        assert abbreviation_rho(words) < -0.9


class TestDistributions:
    def test_word_length_distribution_sums_to_one(self):
        dist = word_length_distribution(["a", "bb", "bb", "ccc"])
        assert math.isclose(sum(dist.values()), 1.0)
        assert dist[2] == 0.5

    def test_tv_distance(self):
        assert tv_distance({1: 1.0}, {1: 1.0}) == 0.0
        assert tv_distance({1: 1.0}, {2: 1.0}) == 1.0
        assert math.isclose(tv_distance({1: 0.5, 2: 0.5}, {1: 1.0}), 0.5)


def test_summarize_block():
    words = ["daiin", "chol", "daiin", "shedy"] * 200
    block = summarize(words)
    assert block["tokens"] == 800
    assert block["types"] == 3
    assert 0 < block["h1"] < 4
    assert 0 <= block["h2"] <= block["h1"]
    assert set(block) >= {"mean_word_length", "abbreviation_rho", "word_length_distribution"}
