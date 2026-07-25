import json

import pytest

from ms408.h4 import H4_RAW, HEBREW_MARKS, TEXTS, build, words_hebrew, words_latinlike

needs_data = pytest.mark.skipif(
    not (H4_RAW / "MANIFEST.json").exists(), reason="H4 raw acquisitions not present"
)


class TestNormalizers:
    def test_latinlike_strips_punctuation_digits_case(self):
        assert words_latinlike("In principio, creavit 3 Deus!") == [
            "in", "principio", "creavit", "deus",
        ]

    def test_latinlike_keeps_marks_only_when_asked(self):
        dipl = "vſſer weltn̄"  # combining macron (abbreviation mark)
        assert words_latinlike(dipl, keep_marks=True) == ["vſſer", "weltn̄"]
        assert words_latinlike(dipl, keep_marks=False) == ["vſſer", "weltn"]

    def test_hebrew_marks_never_split_words(self):
        pointed_word = "כָתַב"  # kaf-qamats-tav-patah-bet
        assert words_hebrew(pointed_word, pointed=False) == ["כתב"]
        assert words_hebrew(pointed_word, pointed=True) == [pointed_word]

    def test_hebrew_strips_html(self):
        assert words_hebrew("<b>שם</b>", pointed=False) == ["שם"]


@needs_data
class TestBuild:
    @staticmethod
    @pytest.fixture(scope="class")
    def manifest(tmp_path_factory):
        out = tmp_path_factory.mktemp("h4")
        result = build(out_root=out)
        result["_out"] = out
        return result

    def test_all_texts_built(self, manifest):
        assert set(manifest["texts"]) == {t.key for t in TEXTS}
        for key in manifest["texts"]:
            assert (manifest["_out"] / f"{key}.txt").exists()

    def test_volume_targets(self, manifest):
        texts = manifest["texts"]
        assert texts["latin_vulgate"]["chars"] > 2_000_000
        assert texts["italian_decameron"]["chars"] > 1_000_000
        german = sum(v["chars"] for k, v in texts.items() if k.endswith("_dipl"))
        assert german > 400_000
        assert texts["hebrew_mishneh_torah_consonantal"]["chars"] > 300_000

    def test_hebrew_registers_align(self, manifest):
        texts = manifest["texts"]
        assert (
            texts["hebrew_mishneh_torah_consonantal"]["words"]
            == texts["hebrew_mishneh_torah_pointed"]["words"]
        )
        consonantal = (manifest["_out"] / "hebrew_mishneh_torah_consonantal.txt").read_text()
        assert not (set(consonantal) & HEBREW_MARKS)
        pointed = (manifest["_out"] / "hebrew_mishneh_torah_pointed.txt").read_text()
        assert set(pointed) & HEBREW_MARKS

    def test_german_registers(self, manifest):
        dipl = (manifest["_out"] / "german_ulmer_wundarznei_dipl.txt").read_text()
        assert "ſ" in dipl  # long s survives in the diplomatic register
        # the corpus's "ascii" simplification retains umlauts/ß — assert it drops
        # the diplomatic apparatus (long s, combining marks), not strict ASCII
        import unicodedata

        simplified = (manifest["_out"] / "german_ulmer_wundarznei_ascii.txt").read_text()
        assert "ſ" not in simplified
        assert not any(unicodedata.category(c) == "Mn" for c in simplified)

    def test_no_digits_or_uppercase_anywhere(self, manifest):
        for key in manifest["texts"]:
            content = (manifest["_out"] / f"{key}.txt").read_text()
            assert not any(c.isdigit() for c in content), key
            assert content == content.lower(), key

    def test_known_openings(self, manifest):
        vulgate = (manifest["_out"] / "latin_vulgate.txt").read_text()
        assert vulgate.startswith("in principio creavit deus")
        decameron = (manifest["_out"] / "italian_decameron.txt").read_text()
        assert decameron.startswith("comincia il libro chiamato decameron")

    def test_manifest_provenance(self, manifest):
        assert manifest["git_commit"]
        with open(manifest["_out"] / "manifest.json") as f:
            on_disk = json.load(f)
        assert set(on_disk["texts"]) == set(manifest["texts"])
        for info in on_disk["texts"].values():
            assert info["sources"] and all(len(s) == 64 for s in info["sources"].values())
