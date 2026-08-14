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
    assert bands["meta"]["git_commit"]
    assert bands["dialects"], "artifact must carry at least one dialect band set"
    for dialect, spec in bands["dialects"].items():
        assert set(spec["axes"]) == set(AXES), dialect
        # ttr and zipf are advisory (token-count-sensitive, D23): no band, either dialect
        for a in TOKEN_SENSITIVE_AXES:
            assert spec["axes"][a]["band"] is None, f"{dialect}.{a} must not be banded"
        # every banded axis must be a real interval
        for a, entry in spec["axes"].items():
            if entry["band"] is not None:
                lo, hi = entry["band"]
                assert lo <= hi, f"{dialect}.{a} band is inverted"


def test_soft_axis_zero_crossing_is_per_dialect():
    """Soft axes are soft in Currier A — but NOT uniformly across dialects (D21).

    The pre-D21 artifact was A-only, so "every syntax band crosses zero" read as a
    property of the manuscript. With B banded separately it is visibly a property of A:
    B's fc_z_local and both global z bands sit entirely off zero. Descriptive only —
    this pins what the artifact says, it does not grade the claim.
    """
    bands = vms_bands()
    crosses = {
        d: {a for a in SOFT_AXES
            if (b := spec["axes"][a]["band"]) and b[0] <= 0 <= b[1]}
        for d, spec in bands["dialects"].items()
    }
    assert crosses["A"] == set(SOFT_AXES), "all four soft axes cross zero in Currier A"
    assert crosses["B"] != set(SOFT_AXES), "not all soft axes cross zero in Currier B"


def test_reference_bands_are_dialect_stratified():
    """The artifact must be per-dialect and say which dialect each set is (D21, L8).

    Regression guard for the original defect: a single band set built from A+B truncated
    at the token budget, which contained only A while claiming to be A+B.
    """
    bands = vms_bands()
    assert bands["schema"] >= 2
    assert set(bands["dialects"]) == {"A", "B"}
    for dialect, spec in bands["dialects"].items():
        assert spec["dialect"] == dialect
        assert f"Currier {dialect}" in spec["vms_dataset"]
        assert "A+B" not in spec["vms_dataset"]
    # the single-dialect accessor returns that dialect's block
    assert vms_bands("B")["dialect"] == "B"
    with pytest.raises(ValueError, match="unknown Currier dialect"):
        vms_bands("Q")


def test_evaluate_contract_and_caveats():
    v = evaluate(_toy())
    assert set(v["dialects"]) == {"A", "B"}
    for dialect, block in v["dialects"].items():
        # every axis carries its caveat and correct flags
        for axis, entry in block["axes"].items():
            assert entry["caveat"], f"{dialect}.{axis} missing caveat"
            assert entry["soft"] == (axis in SOFT_AXES)
            assert entry["confounded"] == (axis in CONFOUNDED_AXES)
            assert entry["token_sensitive"] == (axis in TOKEN_SENSITIVE_AXES)
        # hard count only over HARD_AXES, and never exceeds their number
        assert block["hard_axes_total"] <= len(HARD_AXES)
        assert 0 <= block["hard_axes_in_band"] <= block["hard_axes_total"]
    # the L7 necessary-not-sufficient note is always present, and so is the L8 one
    assert any("NECESSARY" in n for n in v["notes"])
    assert any("per Currier dialect" in n for n in v["notes"])
    # best_match points at a real dialect and agrees with its block
    best = v["best_match"]
    assert best["hard_axes_in_band"] == v["dialects"][best["dialect"]]["hard_axes_in_band"]


def test_evaluate_can_scope_to_one_dialect():
    v = evaluate(_toy(), dialect="B")
    assert set(v["dialects"]) == {"B"}
    assert v["best_match"]["dialect"] == "B"
    with pytest.raises(ValueError, match="unknown Currier dialect"):
        evaluate(_toy(), dialect="Q")


def test_hard_axes_exclude_soft_confounded_and_token_sensitive():
    assert HARD_AXES.isdisjoint(SOFT_AXES)
    assert HARD_AXES.isdisjoint(CONFOUNDED_AXES)
    assert HARD_AXES.isdisjoint(TOKEN_SENSITIVE_AXES)
    # zipf was demoted to advisory at D23; the hard tally is h2 + ed1 only
    assert HARD_AXES == {"h2", "ed1"}
    assert {"dI", "ttr", "zipf"}.isdisjoint(HARD_AXES)


@needs_data
@pytest.mark.parametrize("dialect", ["A", "B"])
def test_vms_is_self_consistent(dialect):
    """Each dialect must land in its OWN hard bands (else that band set is miscalibrated)."""
    from ms408.experiments.e13_function_content import N_TOKENS, _sub, _vms_tokens

    vms = _sub(_vms_tokens(dialect), N_TOKENS)
    block = evaluate(vms, dialect=dialect)["dialects"][dialect]
    assert block["hard_axes_in_band"] == block["hard_axes_total"] == len(HARD_AXES)


@needs_data
def test_dialects_are_mutually_excluded():
    """Each dialect must MISS the other's bands (D21).

    If A sat inside B's bands and vice versa, stratifying would be pointless — the split
    would be hiding structure rather than showing it. Descriptive of the manuscript.
    """
    from ms408.experiments.e13_function_content import N_TOKENS, _sub, _vms_tokens

    for dialect, other in (("A", "B"), ("B", "A")):
        vms = _sub(_vms_tokens(dialect), N_TOKENS)
        block = evaluate(vms, dialect=other)["dialects"][other]
        assert block["hard_axes_in_band"] < block["hard_axes_total"], (
            f"Currier {dialect} should not fully satisfy Currier {other}'s bands"
        )


@needs_data
@needs_h4
def test_real_latin_is_excluded():
    """Raw natural-language prose must NOT pass the hard axes of ANY dialect."""
    from ms408.experiments.e13_function_content import N_TOKENS, _sub

    latin = _sub((H4_OUT / "latin_vulgate.txt").read_text().split(), N_TOKENS)
    v = evaluate(latin)
    assert v["best_match"]["hard_axes_in_band"] == 0
    for dialect, block in v["dialects"].items():
        assert block["hard_axes_in_band"] == 0, dialect
        assert block["axes"]["h2"]["in_band"] is False
        assert block["axes"]["ed1"]["in_band"] is False


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
    assert v["axis_values"]["zipf"] is None
    for dialect, block in v["dialects"].items():
        assert block["axes"]["zipf"]["value"] is None, dialect
        # zipf is advisory since D23, so it is unbanded and in_band is undefined either way
        assert block["axes"]["zipf"]["in_band"] is None
        assert block["axes"]["zipf"]["caveat"]
        # The hard axes (h2, ed1) are still defined, so the denominator is intact.
        assert block["hard_axes_total"] == len(HARD_AXES)
