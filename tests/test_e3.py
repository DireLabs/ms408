import random

from ms408.experiments.e3_anchor_power import _plant_for_phi
from ms408.studies.anchor_hunt import phi as phi_coeff


def test_plant_realises_target_phi():
    all_pages = [f"p{i}" for i in range(120)]
    feature_pages = set(all_pages[:40])  # feature on 40 of 120
    rng = random.Random(0)
    for target in (0.3, 0.4, 0.5):
        planted = _plant_for_phi(feature_pages, all_pages, target, rng)
        assert planted is not None
        n = len(all_pages)
        a = len(planted & feature_pages)
        b = len(planted - feature_pages)
        c = len(feature_pages - planted)
        d = n - a - b - c
        realised = phi_coeff(a, b, c, d)
        assert abs(realised - target) < 0.08


def test_plant_returns_none_for_impossible_phi():
    all_pages = [f"p{i}" for i in range(20)]
    feature_pages = set(all_pages[:2])  # tiny feature -> high phi unreachable cleanly
    rng = random.Random(1)
    # phi 0.99 with a 2-page feature and the >=3-page token constraint is unattainable
    assert _plant_for_phi(feature_pages, all_pages, 0.99, rng) is None
