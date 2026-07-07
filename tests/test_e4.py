import math

from ms408.experiments.e4_root_leaf import _disattenuate, _reliability


def test_reliability_from_disagreement():
    assert _reliability("root_coloring") == 0.96  # 4% disagreement
    assert _reliability("root_type") == 0.65  # 35% disagreement


def test_disattenuation_inflates_toward_truth():
    # a noisy pair's observed V is pulled up when corrected for unreliability
    raw = 0.256
    corrected = _disattenuate(raw, "root_type", "leaf_shape")
    assert corrected > raw
    expected = raw / math.sqrt(0.65 * 0.73)
    assert abs(corrected - round(expected, 4)) < 1e-4


def test_clean_feature_barely_disattenuates():
    # a near-clean feature pair is corrected only slightly
    raw = 0.4
    corrected = _disattenuate(raw, "root_coloring", "leaf_count_band")
    assert corrected < raw * 1.15  # reliabilities 0.96 * 0.85 -> small correction
