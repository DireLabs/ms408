import pytest

from ms408.h4 import H4_OUT
from ms408.studies.encoding import (
    family_abbreviation,
    family_abjad_anagram,
    family_conlang,
    profile,
    scorecard,
)

needs_h4 = pytest.mark.skipif(
    not (H4_OUT / "manifest.json").exists(), reason="run `python -m ms408.h4` first"
)


@needs_h4
class TestFamilyGenerators:
    def test_abjad_anagram_sorts_letters(self):
        words = family_abjad_anagram(500)
        assert len(words) == 500
        assert all(list(w) == sorted(w) for w in words)

    def test_abbreviation_shortens_and_is_deterministic(self):
        a = family_abbreviation(2000, seed=1)
        b = family_abbreviation(2000, seed=1)
        c = family_abbreviation(2000, seed=2)
        assert a == b and a != c
        original = (H4_OUT / "latin_vulgate.txt").read_text().split()[:2000]
        assert sum(map(len, a)) < sum(map(len, original))

    def test_conlang_is_bijective_relexification(self):
        words = family_conlang(3000, seed=1)
        original = (H4_OUT / "latin_vulgate.txt").read_text().split()[:3000]
        mapping = {}
        for latin, con in zip(original, words):
            assert mapping.setdefault(latin, con) == con  # consistent lexicon
        assert len(set(mapping.values())) == len(mapping)  # injective


def test_profile_and_scorecard_smoke():
    import random

    rng = random.Random(0)
    base = [f"w{rng.randrange(60)}" for _ in range(3000)]
    # zipf_slope needs enough word types to fit — keep both corpora above that
    profiles = {
        "vms": profile(base),
        "same": profile(list(base)),
        "different": profile([f"xx{rng.randrange(40)}" for _ in range(3000)]),
    }
    scores = scorecard(profiles)
    assert scores["same"]["distance"] < scores["different"]["distance"]
    assert scores["same"]["distance"] == 0.0
