from collections import Counter

import pytest

from ms408.ivtff import IVTFFDocument
from ms408.replication import _js_divergence, currier_split, paragraph_lines, positional_effects
from ms408.sources import path_for

needs_data = pytest.mark.skipif(
    not path_for("zl").exists(), reason="run `python -m ms408.acquire` first"
)


@pytest.fixture(scope="module")
def lines():
    return paragraph_lines(IVTFFDocument.load(path_for("zl")))


class TestJSDivergence:
    def test_identical_is_zero(self):
        counts = Counter({"a": 10, "b": 5})
        assert _js_divergence(counts, counts) == 0.0

    def test_disjoint_is_one_bit(self):
        assert abs(_js_divergence(Counter({"a": 10}), Counter({"b": 10})) - 1.0) < 1e-9

    def test_symmetric(self):
        p, q = Counter({"a": 8, "b": 2}), Counter({"a": 3, "b": 7, "c": 1})
        assert abs(_js_divergence(p, q) - _js_divergence(q, p)) < 1e-12


@needs_data
class TestParagraphLines:
    def test_paragraph_markers_paired(self, lines):
        # ZL3b carries 740 <%> and 740 <$>; a handful of loci clean to empty
        initial = sum(1 for line in lines if line.paragraph_initial)
        final = sum(1 for line in lines if line.paragraph_final)
        assert 730 <= initial <= 740
        assert 730 <= final <= 740

    def test_only_paragraph_text(self, lines):
        assert len(lines) > 4000  # P-type loci minus empty-cleaning ones
        assert all(line.words for line in lines)


@needs_data
class TestEstablishedPhenomena:
    """The pipeline must reproduce the qualitative signatures; exact values are
    compared against published targets in the replication report."""

    def test_currier_markers(self, lines):
        split = currier_split(lines)
        markers = split["marker_words"]
        assert markers["chedy"]["ratio_B_over_A"] > 20
        assert markers["shedy"]["ratio_B_over_A"] > 20
        assert markers["chol"]["ratio_B_over_A"] < 0.5
        assert split["dy_final_rate"]["B"] > 2 * split["dy_final_rate"]["A"]

    def test_ab_divergence_exceeds_internal(self, lines):
        split = currier_split(lines)
        assert split["js_divergence_A_vs_B"] > 2 * split["js_divergence_within_A"]
        assert split["js_divergence_A_vs_B"] > 2 * split["js_divergence_within_B"]

    def test_paragraph_gallows_enrichment(self, lines):
        effects = positional_effects(lines)
        assert effects["paragraph_initial_gallows"]["enrichment"] > 5

    def test_line_final_m(self, lines):
        effects = positional_effects(lines)
        line_final = effects["line_final"]
        assert line_final["m_final_word_rate_line_end"] > 5 * line_final["m_final_word_rate_mid_line"]
        assert line_final["share_of_m_final_words_at_line_end"] > 0.5
