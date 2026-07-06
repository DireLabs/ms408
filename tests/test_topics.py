import random

import numpy as np
import pytest

from ms408.studies.topics import ari, average_linkage, nmi, permutation_p


class TestARI:
    def test_identical_partitions(self):
        assert ari([0, 0, 1, 1, 2], [5, 5, 9, 9, 7]) == 1.0

    def test_independent_partitions_near_zero(self):
        rng = random.Random(0)
        a = [rng.randrange(4) for _ in range(600)]
        b = [rng.randrange(4) for _ in range(600)]
        assert abs(ari(a, b)) < 0.02

    def test_symmetric(self):
        a, b = [0, 0, 1, 1, 2, 2], [0, 1, 1, 2, 2, 0]
        assert ari(a, b) == pytest.approx(ari(b, a))


class TestNMI:
    def test_identical(self):
        assert nmi([0, 0, 1, 1], [1, 1, 0, 0]) == pytest.approx(1.0)

    def test_constant_labels(self):
        assert nmi([0, 0, 0], [0, 1, 2]) == 0.0


class TestClustering:
    def test_recovers_planted_blocks(self):
        rng = np.random.default_rng(1)
        centers = np.eye(3)
        rows = []
        truth = []
        for c in range(3):
            for _ in range(15):
                v = centers[c] + rng.normal(0, 0.15, 3)
                rows.append(v / np.linalg.norm(v))
                truth.append(c)
        matrix = np.array(rows)
        clusters = average_linkage(matrix @ matrix.T, 3)
        assert ari(clusters, truth) > 0.9

    def test_deterministic(self):
        rng = np.random.default_rng(2)
        matrix = rng.random((20, 5))
        matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)
        sim = matrix @ matrix.T
        assert average_linkage(sim, 4) == average_linkage(sim, 4)


def test_permutation_p_detects_real_alignment():
    clusters = [0] * 30 + [1] * 30
    aligned = ["x"] * 30 + ["y"] * 30
    p = permutation_p(clusters, aligned, ari(clusters, aligned))
    assert p < 0.01
    rng = random.Random(3)
    noise = [rng.choice("xy") for _ in range(60)]
    p_noise = permutation_p(clusters, noise, ari(clusters, noise))
    assert p_noise > 0.05
