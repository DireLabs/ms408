from ms408.studies.morphology import (
    affix_structure,
    curveline_valid_share,
    ed1_edges,
    ed1_network_stats,
    positional_concentration,
)


class TestED1Network:
    def test_edges_found(self):
        types = ["chol", "chor", "shol", "cho", "daiin", "xxxxx"]
        edges = ed1_edges(types)
        pairs = {tuple(sorted((types[a], types[b]))) for a, b in edges}
        assert ("chol", "chor") in pairs  # substitution
        assert ("chol", "shol") in pairs  # substitution
        assert ("cho", "chol") in pairs  # insertion/deletion
        assert not any("daiin" in p or "xxxxx" in p for p in pairs)

    def test_stats(self):
        stats = ed1_network_stats(["chol", "chor", "shol", "daiin"] * 10)
        assert stats["types"] == 4
        assert stats["main_component_share"] == 0.75  # daiin isolated
        assert stats["isolate_share"] == 0.25

    def test_no_self_or_duplicate_edges(self):
        edges = ed1_edges(["aa", "ab", "ba"])
        assert all(a != b for a, b in edges)
        assert len(edges) == len(set(edges))


class TestPositional:
    def test_locked_glyph_scores_zero(self):
        # 'q' always word-initial, 'y' always word-final
        result = positional_concentration(["qokedy", "qokain", "qotedy"] * 20)
        assert result["most_frequent_glyphs"]["q"] == 0.0

    def test_uniform_glyph_scores_high(self):
        # 'a' appears at every position of 5-char words
        words = ["abbbb", "babbb", "bbabb", "bbbab", "bbbba"] * 10
        result = positional_concentration(words)
        assert result["most_frequent_glyphs"]["a"] > 0.9

    def test_bounds(self):
        result = positional_concentration(["chol", "daiin", "shedy"] * 5)
        assert 0.0 <= result["mean_normalized_position_entropy"] <= 1.0


class TestAffixes:
    def test_coverage(self):
        words = ["qokedy", "qokain", "chedy", "chor"] * 25
        result = affix_structure(words)
        grams = {r["gram"] for r in result["top_prefixes"]}
        assert "qo" in grams and "ch" in grams
        assert 0.0 <= result["share_with_top_prefix_and_suffix"] <= 1.0


def test_curveline_share_bounds():
    assert curveline_valid_share(["daiin", "chedy"]) == 1.0
    assert curveline_valid_share(["et", "in", "principio"]) < 0.5
