import random

from ms408.studies.referential_realism import (
    _cramers_v,
    _distinct_combos,
    association_test,
)


class TestCramersV:
    def test_perfect_association(self):
        pairs = [("a", "x"), ("a", "x"), ("b", "y"), ("b", "y")]
        assert abs(_cramers_v(pairs) - 1.0) < 1e-9

    def test_no_association(self):
        # every x pairs equally with every y
        pairs = [(x, y) for x in "ab" for y in "xy" for _ in range(10)]
        assert _cramers_v(pairs) < 0.05

    def test_empty(self):
        assert _cramers_v([]) == 0.0


def test_distinct_combos():
    assert _distinct_combos([("a", "x"), ("a", "x"), ("b", "y")]) == 2


class TestAssociationTest:
    def test_detects_real_constraint(self):
        rng = random.Random(0)
        # a constrained world: root type determines leaf shape (bundled)
        bundles = {"taproot": "lobed", "bulbous": "simple", "fibrous": "serrated"}
        xs, ys = [], []
        for _ in range(90):
            root = rng.choice(list(bundles))
            xs.append(root)
            ys.append(bundles[root])
        result = association_test(xs, ys, seed=1)
        assert result["constrained"] is True
        assert result["cramers_v"] > 0.9
        # constrained -> far fewer distinct combos than the free-mixing null
        assert result["distinct_combinations"] < result["null_combinations_median"]

    def test_detects_free_mixing(self):
        rng = random.Random(1)
        # independent features: any root with any leaf
        roots = ["taproot", "bulbous", "fibrous"]
        leaves = ["lobed", "simple", "serrated"]
        xs = [rng.choice(roots) for _ in range(90)]
        ys = [rng.choice(leaves) for _ in range(90)]
        result = association_test(xs, ys, seed=2)
        assert result["constrained"] is False
        assert result["p_associated"] > 0.05
