import random
from collections import Counter

from ms408.experiments.e1_meaning_detector import drift_reorder


def test_drift_reorder_preserves_multiset():
    tokens = ["a", "b", "a", "c", "a", "b", "d"] * 20
    reordered = drift_reorder(tokens, 0.05, random.Random(0))
    assert Counter(reordered) == Counter(tokens)
    assert len(reordered) == len(tokens)


def test_tight_spread_clusters_types():
    # with a small spread, each type's tokens should be contiguous-ish: measure
    # mean gap between same-type positions -> small for tight spread
    tokens = [f"w{i}" for i in range(50) for _ in range(20)]
    rng = random.Random(1)
    tight = drift_reorder(tokens, 0.01, rng)
    loose = drift_reorder(tokens, 0.5, rng)

    def mean_spread(seq):
        pos = {}
        for i, t in enumerate(seq):
            pos.setdefault(t, []).append(i)
        return sum((max(p) - min(p)) for p in pos.values()) / len(pos)

    assert mean_spread(tight) < mean_spread(loose)


def test_deterministic_under_seed():
    tokens = ["a", "b", "c"] * 100
    a = drift_reorder(tokens, 0.1, random.Random(5))
    b = drift_reorder(tokens, 0.1, random.Random(5))
    assert a == b
