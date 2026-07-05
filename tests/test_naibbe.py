"""Naibbe reimplementation tests (spec: docs/planning/i01/specs/T03-naibbe-spec.md §8).

The golden test decrypts the author's committed ciphertext and requires byte
equality with the author's committed decryption — validating our tables, reverse
maps, precedence rules, and multi-reading formatting against the reference
implementation without rerunning it.
"""

import pytest

from ms408.harness.naibbe import (
    DECKS,
    NaibbeCipher,
    NaibbeConfig,
    NaibbeTables,
    clean_line,
    decrypt_line,
)
from ms408.sources import path_for

TABLES_PATH = path_for("naibbe_tables")

needs_data = pytest.mark.skipif(
    not TABLES_PATH.exists(), reason="run `python -m ms408.acquire` first"
)


@pytest.fixture(scope="module")
def tables() -> NaibbeTables:
    return NaibbeTables.load()


def test_clean_line():
    assert clean_line("Grátias, tibi ago! 42") == "gratiastibiago"
    assert clean_line("WJK wjk") == "uuicuuic"
    assert clean_line("æther Œdipus") == "aetheroedipus"
    assert clean_line("1 ") == ""
    assert clean_line(" I ") == "i"


@needs_data
class TestTables:
    def test_invariants_load_clean(self, tables):
        assert len(tables.glyph) == 414

    def test_unigram_glyphs_distinct_except_dar(self, tables):
        # 138 unigram entries; 'dar' serves twice (both for plaintext 'e') -> 137 distinct
        assert len(tables.unigram_glyphs) == 137
        assert tables.to_letter["unigram"]["dar"] == "e"

    def test_ambiguous_bigram_catalog(self, tables):
        assert len(tables.ambiguous_bigrams) == 105

    def test_sha256_pin_enforced(self, tmp_path):
        bad = tmp_path / "tables.csv"
        bad.write_text("code,glyphs\nunigram_alpha_a,ol\n")
        with pytest.raises(ValueError, match="sha256"):
            NaibbeTables.load(bad)


@needs_data
class TestEncryption:
    def test_round_trip_and_alignment(self, tables):
        plaintext = path_for("naibbe_pliny").read_text().splitlines()[:120]
        cipher = NaibbeCipher(tables, NaibbeConfig(deck="52"), seed=408)
        result = cipher.encrypt_text(plaintext)
        for raw, ct_line, seg_line in zip(
            plaintext, result.ciphertext_lines, result.segmented_lines
        ):
            decrypted = decrypt_line(tables, ct_line)
            # v2 output decrypts uniquely, to exactly the unit segmentation
            assert decrypted == seg_line
            assert decrypted.replace(" ", "") == clean_line(raw)
            assert "(" not in decrypted and "[?]" not in decrypted
            assert len(ct_line.split()) == len(seg_line.split())

    def test_both_decks_and_reshuffle(self, tables):
        long_line = "x" * 200  # ~130 units -> >100 draws -> multiple deck reshuffles
        for deck in DECKS:
            cipher = NaibbeCipher(tables, NaibbeConfig(deck=deck), seed=7)
            enc = cipher.encrypt_line(long_line)
            assert "".join(enc.units) == "x" * 200
            assert len(enc.words) == len(enc.units) > 52

    def test_segmentation_fraction(self, tables):
        cipher = NaibbeCipher(tables, NaibbeConfig(), seed=99)
        units = cipher.segment("a" * 20000)
        unigram_share = sum(1 for u in units if len(u) == 1) / len(units)
        assert 0.45 < unigram_share < 0.50  # P(unigram)=17/36 with line-final forcing

    def test_seeded_determinism(self, tables):
        lines = ["gratias tibi ago"] * 3
        a = NaibbeCipher(tables, NaibbeConfig(), seed=42).encrypt_text(lines)
        b = NaibbeCipher(tables, NaibbeConfig(), seed=42).encrypt_text(lines)
        c = NaibbeCipher(tables, NaibbeConfig(), seed=43).encrypt_text(lines)
        assert a == b
        assert a.ciphertext_lines != c.ciphertext_lines

    def test_v1_mode_reachable(self, tables):
        config = NaibbeConfig(cross_bigram_check=False)
        cipher = NaibbeCipher(tables, config, seed=5)
        enc = cipher.encrypt_line("gratias tibi ago")
        assert decrypt_line(tables, " ".join(enc.words)).replace(" ", "") == "gratiastibiago"


@needs_data
class TestGoldenDecrypt:
    def test_author_ciphertext_decrypts_to_author_decryption(self, tables):
        ct_lines = path_for("naibbe_nathist_ciphertext").read_text().splitlines()
        golden = path_for("naibbe_nathist_decrypted").read_text().splitlines()
        assert len(ct_lines) == len(golden) == 1640
        for lineno, (ct, expected) in enumerate(zip(ct_lines, golden), start=1):
            assert decrypt_line(tables, ct) == expected.rstrip(), f"line {lineno}"

    def test_author_decryption_matches_segmentation_ground_truth(self, tables):
        # nathist is v1-generated, so the decryption contains multi-readings like
        # "(dy|st)" — each must include the true unit from the segmentation file
        golden = path_for("naibbe_nathist_decrypted").read_text().splitlines()
        segmented = path_for("naibbe_nathist_respaced").read_text().splitlines()
        multi_readings = 0
        for g_line, s_line in zip(golden, segmented):
            for g_tok, s_tok in zip(g_line.split(), s_line.split()):
                if g_tok.startswith("("):
                    multi_readings += 1
                    assert s_tok in g_tok[1:-1].split("|")
                else:
                    assert g_tok == s_tok
        assert multi_readings > 0  # v1 text does contain ambiguous bigrams
