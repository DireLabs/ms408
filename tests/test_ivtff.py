"""Integrity tests for the IVTFF parser against independently verified reference counts.

Reference counts come from docs/planning/i01/SOURCES.md §1: they were established by
direct inspection of ZL3b-n.txt during source verification (2026-07-05), independent
of this parser. If the parser reproduces them, parsing and the file are both intact.
"""

import pytest

from ms408.ivtff import DEFAULT_POLICY, IVTFFDocument, TextPolicy, words
from ms408.sources import path_for

ZL_PATH = path_for("zl")
GC_PATH = path_for("gc")

needs_data = pytest.mark.skipif(
    not ZL_PATH.exists(), reason="run `python -m ms408.acquire` first"
)


@pytest.fixture(scope="module")
def zl() -> IVTFFDocument:
    return IVTFFDocument.load(ZL_PATH)


@needs_data
class TestZLIntegrity:
    def test_file_header(self, zl):
        assert zl.alphabet == "Eva-"
        assert zl.version == "2.0"

    def test_page_count(self, zl):
        assert len(zl.pages) == 227

    def test_locus_count(self, zl):
        # 5385 locus lines counted directly in ZL3b-n.txt (transcr.html says "5389
        # identified loci"; the file as distributed carries 5385 locus lines)
        assert len(zl.loci) == 5385

    def test_illustration_distribution(self, zl):
        # Direct grep of page-header lines. (A commented-out header for f101r2
        # carries one more $I=P — it is a comment, not a page.)
        counts = zl.variable_counts("I")
        assert counts["H"] == 129
        assert counts["S"] == 25
        assert counts["B"] == 19
        assert counts["P"] == 16
        assert counts["Z"] == 12
        assert counts["C"] == 11
        assert counts["A"] == 8
        assert counts["T"] == 7

    def test_currier_language_distribution(self, zl):
        counts = zl.variable_counts("L")
        assert counts["A"] == 114
        assert counts["B"] == 83
        assert counts[None] == 30

    def test_hand_distribution(self, zl):
        counts = zl.variable_counts("H")
        assert counts["1"] == 113
        assert counts["2"] == 46
        assert counts["3"] == 33
        assert counts["4"] == 27
        assert counts["5"] == 7
        assert counts["@"] == 1  # f115r: hand changes mid-page (in-line <@H=n> tags)
        assert counts[None] == 0

    def test_f115r_is_the_mixed_hand_page(self, zl):
        assert zl.page("f115r").hand == "@"

    def test_loci_belong_to_their_pages(self, zl):
        for page in zl.pages:
            assert all(locus.page == page.name for locus in page.loci)


@needs_data
class TestCleaning:
    def test_first_locus_words(self, zl):
        # <f1r.1,@P0>  <%>fachys.ykal.ar.ataiin.shol.shory.[cth:oto]res.y.kor.sholdy<!@254;>
        locus = zl.page("f1r").loci[0]
        assert locus.words() == [
            "fachys", "ykal", "ar", "ataiin", "shol",
            "shory", "cthres", "y", "kor", "sholdy",
        ]

    def test_alternative_reading_policy(self):
        raw = "sho.[cth:oto]res"
        assert words(raw, DEFAULT_POLICY) == ["sho", "cthres"]
        assert words(raw, TextPolicy(first_alternative=False)) == ["sho", "otores"]

    def test_comma_policy(self):
        raw = "sory.ckhar.or,y"
        assert words(raw, DEFAULT_POLICY) == ["sory", "ckhar", "or", "y"]
        assert words(raw, TextPolicy(comma_is_word_break=False)) == ["sory", "ckhar", "or,y"]

    def test_uncertain_word_policy(self):
        raw = "cho.?o.kaiin"
        assert words(raw, DEFAULT_POLICY) == ["cho", "?o", "kaiin"]
        assert words(raw, TextPolicy(drop_uncertain_words=True)) == ["cho", "kaiin"]

    def test_braces_and_tags_stripped(self, zl):
        for locus in zl.loci:
            cleaned = locus.clean()
            assert "<" not in cleaned and ">" not in cleaned
            assert "{" not in cleaned and "}" not in cleaned


@pytest.mark.skipif(not GC_PATH.exists(), reason="run `python -m ms408.acquire` first")
class TestGCv101:
    def test_parses_complete(self):
        gc = IVTFFDocument.load(GC_PATH)
        assert gc.alphabet == "v101"
        assert len(gc.pages) == 226
        assert len(gc.loci) == 5367

    def test_page_names_match_zl_except_f116v(self, zl):
        # v101 never transcribed f116v (the Latin/German marginalia page —
        # appendix-only for us anyway, per L12)
        gc = IVTFFDocument.load(GC_PATH)
        zl_names = {p.name for p in zl.pages}
        gc_names = {p.name for p in gc.pages}
        assert zl_names - gc_names == {"f116v"}
        assert gc_names - zl_names == set()
