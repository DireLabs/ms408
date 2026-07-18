"""Tests for the public evaluator (ms408.signature / ms408.evaluate).

These guard the tool's *contract* — determinism, the caveat-attachment discipline, and the
two behaviours that make it a discriminator: the VMS lands in its own hard bands, and raw
real-language does not. Value-pinning tests that need the acquired corpus skip cleanly.
"""

from __future__ import annotations

import pytest

from ms408 import evaluate
from ms408.signature import (
    AXES,
    CONFOUNDED_AXES,
    HARD_AXES,
    SOFT_AXES,
    TOKEN_SENSITIVE_AXES,
    axis_values,
    vms_bands,
)
from ms408.sources import path_for

needs_data = pytest.mark.skipif(
    not path_for("zl").exists(), reason="run `python -m ms408.acquire` first"
)


def _toy(n: int = 600) -> list:
    # deterministic pseudo-text with some structure (not meant to match the VMS)
    vocab = [f"w{i}" for i in range(40)]
    return [vocab[(i * 7 + (i // 5)) % len(vocab)] for i in range(n)]


def test_axis_values_deterministic():
    a = axis_values(_toy(), seed=408)
    b = axis_values(_toy(), seed=408)
    assert a == b
    # seed changes the null-based syntax z's, not the profile axes
    c = axis_values(_toy(), seed=99)
    assert a["h2"] == c["h2"] and a["ed1"] == c["ed1"]


def test_axis_values_rejects_tiny_input():
    with pytest.raises(ValueError):
        axis_values(["only-one"])


def test_reference_bands_shape():
    bands = vms_bands()
    assert set(bands["axes"]) == set(AXES)
    assert bands["meta"]["git_commit"]
    # every syntax (soft) band crosses zero — the honest "soft axis" fact
    for a in SOFT_AXES:
        lo, hi = bands["axes"][a]["band"]
        assert lo <= 0 <= hi, f"{a} band should cross zero"
    # ttr is advisory: no band
    assert bands["axes"]["ttr"]["band"] is None


def test_evaluate_contract_and_caveats():
    v = evaluate(_toy())
    # every axis carries its caveat and correct flags
    for axis, entry in v["axes"].items():
        assert entry["caveat"], f"{axis} missing caveat"
        assert entry["soft"] == (axis in SOFT_AXES)
        assert entry["confounded"] == (axis in CONFOUNDED_AXES)
        assert entry["token_sensitive"] == (axis in TOKEN_SENSITIVE_AXES)
    # hard count only over HARD_AXES, and never exceeds their number
    assert v["hard_axes_total"] <= len(HARD_AXES)
    assert 0 <= v["hard_axes_in_band"] <= v["hard_axes_total"]
    # the L7 necessary-not-sufficient note is always present
    assert any("NECESSARY" in n for n in v["notes"])


def test_hard_axes_exclude_soft_and_confounded():
    assert HARD_AXES.isdisjoint(SOFT_AXES)
    assert HARD_AXES.isdisjoint(CONFOUNDED_AXES)
    assert HARD_AXES.isdisjoint(TOKEN_SENSITIVE_AXES)
    assert "dI" not in HARD_AXES and "ttr" not in HARD_AXES


@needs_data
def test_vms_is_self_consistent():
    """The VMS must land in its own hard bands (else the bands are miscalibrated)."""
    from ms408.experiments.e13_function_content import N_TOKENS, _sub, _vms_tokens

    vms = _sub(_vms_tokens("A") + _vms_tokens("B"), N_TOKENS)
    v = evaluate(vms)
    assert v["hard_axes_in_band"] == v["hard_axes_total"] == len(HARD_AXES)


@needs_data
def test_real_latin_is_excluded():
    """Raw natural-language prose must NOT pass the hard axes (high h2, no ED1 network)."""
    from ms408.experiments.e13_function_content import N_TOKENS, _sub
    from ms408.h4 import H4_OUT

    latin = _sub((H4_OUT / "latin_vulgate.txt").read_text().split(), N_TOKENS)
    v = evaluate(latin)
    assert v["hard_axes_in_band"] == 0
    assert v["axes"]["h2"]["in_band"] is False
    assert v["axes"]["ed1"]["in_band"] is False
