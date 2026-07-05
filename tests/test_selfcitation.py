"""Self-citation reimplementation tests (spec T03-selfcitation §15 testing plan).

Bit-exact replication of the Java generator is impossible (spec §12), so these tests
pin table integrity, tokenizer behavior, adjacency rules, morph micro-behaviors with
injected RNG streams, and end-to-end determinism/structure. Distributional validation
against the author's reference output happens in the harness benchmark (T0.3 gate).
"""

import pytest

from ms408.harness.selfcitation import (
    FINAL_SUBSTITUTIONS,
    INITIAL,
    LIGATURES,
    SEED_LINE_A,
    SEED_LINE_B,
    SUBSTITUTIONS,
    Morpher,
    MorphConfig,
    SelfCitationConfig,
    SelfCitationGenerator,
    Word,
    is_valid,
    tokenize,
)


class FakeRand:
    """Injected RNG stream: returns scripted values, then zeros."""

    def __init__(self, values):
        self.values = list(values)

    def __call__(self, bound):
        if bound <= 0:
            return 0
        value = self.values.pop(0) if self.values else 0
        return min(value, bound - 1)


class TestTables:
    def test_ligature_count(self):
        assert len(LIGATURES) == 42
        assert len(set(LIGATURES)) == 42

    def test_substitution_cdfs_end_at_100_and_are_monotone(self):
        for table in (SUBSTITUTIONS, FINAL_SUBSTITUTIONS):
            for source, candidates in table.items():
                thresholds = [t for _, t in candidates]
                assert thresholds[-1] == 100, source
                assert thresholds == sorted(thresholds), source
                assert all(t > 0 for t in thresholds), source


class TestTokenizer:
    @pytest.mark.parametrize(
        ("word", "expected"),
        [
            ("qokeedy", ("qo", "k", "ee", "dy")),
            ("daiin", ("d", "a", "iin")),
            ("ckhhy", ("ckhh", "y")),
            ("eeey", ("eee", "y")),
            ("chol", ("ch", "ol")),
            ("pchal", ("p", "ch", "al")),
            ("shorchdy", ("sh", "or", "ch", "dy")),
        ],
    )
    def test_hand_cases(self, word, expected):
        assert tokenize(word) == expected

    def test_round_trip(self):
        for word in SEED_LINE_B.split() + SEED_LINE_A.split():
            assert "".join(tokenize(word)) == word


class TestCanFollow:
    def test_seed_words_bypass_validity(self):
        # Some genuine VMS words violate the curve/line theorem (shorchdy: or->ch is
        # an illegal adjacency) — which is exactly why INITIAL-tagged words bypass
        # isValid in the author's design. Verify the bypass and the violation.
        from ms408.harness.selfcitation import has_valid_start

        for text in SEED_LINE_B.split() + SEED_LINE_A.split():
            assert has_valid_start(Word.parse(text, INITIAL)), text
        assert not is_valid(Word.parse("shorchdy", "REPLACE"))

    def test_reference_defaults_are_valid(self):
        for text in ("daiin", "chedy", "cheody", "chol", "qokeedy", "ol"):
            assert is_valid(Word.parse(text, "REPLACE")), text

    def test_doiin_style_rejected(self):
        # line-family token (iin) directly after a curve glyph (o) is illegal
        assert not is_valid(Word.parse("doiin", "REPLACE"))


class TestTypeClasses:
    @pytest.mark.parametrize(
        ("word", "cls"),
        [
            ("daiin", "i"),
            ("okain", "i"),
            ("chedy", "dy"),
            ("oteey", "dy"),
            ("okeod", "dy"),
            ("chol", "ol"),
            ("qokar", "ol"),
            ("chee", "other"),
        ],
    )
    def test_classification(self, word, cls):
        assert Word.parse(word, "REPLACE").type_class() == cls


class TestMorphMicro:
    def make_morpher(self, values):
        morpher = Morpher(FakeRand(values), MorphConfig())
        morpher._previous_word = Word.parse("chedy", INITIAL)  # ends in dy
        return morpher

    def test_q_prefix_after_dy_word(self):
        # choose_prefix draw 50 (<90, attempt 0, prev ends dy) -> q; okeedy -> qokeedy
        morpher = self.make_morpher([50])
        result = morpher._try_add_prefix(Word.parse("okeedy", "REPLACE"))
        assert result is not None and result.text == "qokeedy"

    def test_delete_prefix_gallow_softening(self):
        # okain -> kain; k before a-initial token softens to d with r<50 -> dain
        morpher = self.make_morpher([10])
        result = morpher._try_delete_prefix(Word.parse("okain", "REPLACE"))
        assert result is not None and result.text == "dain"

    def test_self_combine_chol(self):
        # chol + chol; ingroup map has no 'ol' entry (first copy unchanged),
        # group-final draw 90 (>=80: second copy unchanged), gallow draw 90 (>=30: none)
        morpher = self.make_morpher([90, 90])
        result = morpher._self_combine(Word.parse("chol", "REPLACE"))
        assert result is not None and result.text == "cholchol"
        assert result.tag == "COMBINE"

    def test_trim_final_line_replacement(self):
        generator = SelfCitationGenerator(SelfCitationConfig(), seed=1)
        trimmed = generator._try_trim(Word.parse("chol", "REPLACE"), available=4)
        assert trimmed is not None
        assert trimmed.text.endswith("om")  # ol -> om (spec §9.4 step 1)
        assert trimmed.tag == "SHORTEN"


class TestEndToEnd:
    def test_deterministic_across_runs(self):
        config = SelfCitationConfig(lines_to_create=40)
        a = SelfCitationGenerator(config, seed=19).generate()
        b = SelfCitationGenerator(config, seed=19).generate()
        c = SelfCitationGenerator(config, seed=20).generate()
        assert a.to_plain_lines() == b.to_plain_lines()
        assert a.to_plain_lines() != c.to_plain_lines()

    def test_structure_and_meta(self):
        config = SelfCitationConfig(lines_to_create=64)
        result = SelfCitationGenerator(config, seed=19).generate()
        assert len(result.lines) == 64
        assert len(result.line_meta) == 64
        assert all(line for line in result.lines)  # no empty lines
        # a 64-line run spans pages 0..2 (29 lines per page, seed line included)
        assert result.line_meta[-1]["page"] >= 1
        # paragraph-initial flags exist beyond the seed line
        assert sum(m["paragraph_initial"] for m in result.line_meta) > 2

    def test_line_length_budget(self):
        config = SelfCitationConfig(lines_to_create=64)
        result = SelfCitationGenerator(config, seed=7).generate()
        for line in result.to_plain_lines():
            assert len(line) <= config.max_line_length + 10  # budget + last-word slack

    def test_currier_inference(self):
        assert SelfCitationConfig(initial_line=SEED_LINE_B).currier == "B"
        assert SelfCitationConfig(initial_line=SEED_LINE_A).currier == "A"

    def test_output_is_eva_lowercase(self):
        config = SelfCitationConfig(lines_to_create=40)
        result = SelfCitationGenerator(config, seed=19).generate()
        alphabet = set("abcdefghijklmnopqrstuvwxyz")
        for line in result.lines:
            for word in line:
                assert set(word) <= alphabet, word
