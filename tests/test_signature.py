"""Tests for the public evaluator (ms408.signature / ms408.evaluate).

These guard the tool's *contract* — determinism, the caveat-attachment discipline, and the
two behaviours that make it a discriminator: the VMS lands in its own hard bands, and raw
real-language does not. Value-pinning tests that need the acquired corpus skip cleanly.
"""

from __future__ import annotations

import pytest

from ms408 import evaluate
from ms408.h4 import H4_OUT
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

# The H4 control corpora are built by `python -m ms408.h4` from raw sources that are not
# in ms408.sources (they are not redistributable and not fetched by ms408.acquire), so a
# test needing them must guard on the corpus file itself, not on the VMS transliteration.
# Same guard as tests/test_encoding.py::needs_h4.
needs_h4 = pytest.mark.skipif(
    not (H4_OUT / "latin_vulgate.txt").exists(), reason="run `python -m ms408.h4` first"
)


def _toy(n: int = 1500) -> list:
    # deterministic pseudo-text with some structure (not meant to match the VMS); n is kept
    # above MIN_TOKENS so axis_values() does not (correctly) refuse it.
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


def test_evaluate_refuses_short_streams_cleanly():
    """A short stream must raise a clear ValueError, not crash with an internal traceback
    (regression: the README's own 9-token example used to hit max()/round(None))."""
    from ms408.signature import MIN_TOKENS

    for n in (9, 50, 700, MIN_TOKENS - 1):
        with pytest.raises(ValueError, match="at least"):
            evaluate([f"w{i % 20}" for i in range(n)])


def test_evaluate_low_budget_note():
    """Between MIN_TOKENS and the reference budget it must WORK (no crash) and warn."""
    v = evaluate(_toy(1500))
    assert any("LOW TOKEN BUDGET" in n for n in v["notes"])


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
@needs_h4
def test_real_latin_is_excluded():
    """Raw natural-language prose must NOT pass the hard axes (high h2, no ED1 network)."""
    from ms408.experiments.e13_function_content import N_TOKENS, _sub

    latin = _sub((H4_OUT / "latin_vulgate.txt").read_text().split(), N_TOKENS)
    v = evaluate(latin)
    assert v["hard_axes_in_band"] == 0
    assert v["axes"]["h2"]["in_band"] is False
    assert v["axes"]["ed1"]["in_band"] is False


@pytest.mark.parametrize(
    "tokens",
    [
        pytest.param(["qokeedy"] * 1500, id="single-type"),
        pytest.param(["qokeedy", "chedy"] * 750, id="two-types"),
    ],
)
def test_degenerate_input_returns_verdict_not_crash(tokens):
    """Streams with too few types must yield an undefined zipf, not a TypeError.

    zipf_slope() returns None below min_rank + 10 types (a documented contract). The
    verdict path must carry that None through rather than round() it: these are the
    first inputs a stranger tries, and a traceback is not a verdict. Data-free.
    """
    v = evaluate(tokens)
    assert v["axes"]["zipf"]["value"] is None
    assert v["axes"]["zipf"]["in_band"] is None
    # An undefined axis is excluded from the denominator, not silently counted as a miss.
    assert v["hard_axes_total"] == len(HARD_AXES) - 1
    assert v["axes"]["zipf"]["caveat"]
