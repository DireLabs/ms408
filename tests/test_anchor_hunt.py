import random

from ms408.studies.anchor_hunt import (
    PageData,
    benjamini_hochberg,
    fisher_right_tail,
    null_control,
    phi,
    planted_control,
    scan,
    _page_sets,
)


class TestStatistics:
    def test_phi_perfect_association(self):
        assert phi(10, 0, 0, 10) == 1.0
        assert phi(0, 10, 10, 0) == -1.0
        assert abs(phi(5, 5, 5, 5)) < 1e-9

    def test_fisher_enrichment_significant(self):
        # strong enrichment: token on 9/10 feature pages, 0/10 non-feature
        assert fisher_right_tail(9, 0, 1, 10) < 0.001
        # no enrichment
        assert fisher_right_tail(5, 5, 5, 5) > 0.3

    def test_fisher_bounds(self):
        assert 0.0 <= fisher_right_tail(3, 4, 5, 6) <= 1.0

    def test_bh_controls_discoveries(self):
        # 5 tiny p-values + 95 uniform nulls
        pvals = [1e-6] * 5 + [0.5] * 95
        discovered = benjamini_hochberg(pvals, 0.05)
        assert sum(discovered) == 5
        assert all(discovered[:5])

    def test_bh_no_discoveries_when_all_null(self):
        pvals = [0.5] * 100
        assert sum(benjamini_hochberg(pvals, 0.05)) == 0


def _synthetic_pages(rng, n=40, planted_feature="root_type=taproot"):
    pages = []
    for i in range(n):
        has_feature = i < n // 2
        features = {planted_feature} if has_feature else {"root_type=bulbous"}
        tokens = {f"noise{rng.randrange(30)}" for _ in range(8)}
        if has_feature and rng.random() < 0.9:
            tokens.add("signal")  # a real anchor for the feature
        pages.append(PageData(f"f{i}", "H", frozenset(tokens), frozenset(features)))
    return pages


class TestScanAndControls:
    def test_scan_finds_planted_signal(self):
        rng = random.Random(0)
        pages = _synthetic_pages(rng)
        tokens, features = _page_sets(pages)
        tests = scan(pages, tokens, features)
        hit = next(t for t in tests
                   if t["token"] == "signal" and t["feature"] == "root_type=taproot")
        assert hit["discovery"]
        assert hit["phi"] > 0.7

    def test_null_control_few_false_discoveries(self):
        rng = random.Random(1)
        pages = _synthetic_pages(rng)
        null = null_control(pages, seed=1)
        # shuffling text vs features should mostly destroy the association
        assert null["false_discovery_fraction"] <= 0.05

    def test_planted_control_recovers(self):
        rng = random.Random(2)
        pages = _synthetic_pages(rng)
        planted = planted_control(pages, seed=2)
        assert planted["recovered"] is True
        assert planted["phi"] > 0.9  # PLANT is on exactly the feature pages
