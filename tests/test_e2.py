from collections import Counter

from ms408.experiments.e2_wordorder_confound import (
    deterministic_verbose_cipher,
    meaningless_block_stream,
)


def test_deterministic_cipher_is_type_preserving():
    # same plaintext word -> same cipher word (bijection on types)
    plain = ["aqua", "aqua", "herba", "aqua", "herba"]
    ciphered = deterministic_verbose_cipher(plain)
    assert len(ciphered) == 5
    # the two 'herba' map identically; 'aqua' maps identically
    assert ciphered[0] == ciphered[1] == ciphered[3]
    assert ciphered[2] == ciphered[4]
    assert ciphered[0] != ciphered[2]
    # verbose: cipher words are longer than plaintext (multi-glyph per letter)
    assert len(ciphered[0]) > len("aqua")


def test_deterministic_cipher_preserves_type_frequency_structure():
    plain = ["a"] * 10 + ["b"] * 5 + ["c"] * 2
    ciphered = deterministic_verbose_cipher(plain)
    # frequency multiset of types is preserved (just relabeled)
    assert sorted(Counter(ciphered).values()) == sorted(Counter(plain).values())


def test_meaningless_block_stream_is_blocked():
    tokens = meaningless_block_stream(1000, blocks=5, seed=1)
    assert len(tokens) == 1000
    # each block uses its own vocabulary prefix; block 0 words never appear late
    first_fifth = set(tokens[:200])
    last_fifth = set(tokens[800:])
    assert not (first_fifth & last_fifth)  # disjoint block vocabularies
