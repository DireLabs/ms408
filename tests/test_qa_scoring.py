from ms408.annotate.qa import _agree, score_page


class TestAgree:
    def test_enum_exact(self):
        assert _agree("enum", "taproot", "taproot")
        assert not _agree("enum", "taproot", "bulbous")

    def test_bool(self):
        assert _agree("bool", True, True)
        assert not _agree("bool", True, False)

    def test_count_within_one(self):
        assert _agree("count", 3, 4)
        assert _agree("count", 3, 3)
        assert not _agree("count", 3, 5)

    def test_multi_jaccard(self):
        assert _agree("multi", ["green", "red"], ["green", "red"])
        assert _agree("multi", ["green", "red", "blue"], ["green", "red"])  # 2/3 = 0.67
        assert not _agree("multi", ["green", "red"], ["blue", "yellow"])
        assert _agree("multi", [], [])
        assert _agree("multi", ["none"], ["none"])


def test_score_page_counts_disagreements():
    sonnet = {
        "common": {"illustration_coverage_pct": "51-75", "text_image_relationship":
                   "text-wraps-image", "color_palette": ["green"], "marginalia_present":
                   False, "damage_or_stain": False},
        "section_features": {"plant_count": 1, "root_type": "taproot", "root_color":
                             ["brown"], "leaf_shape": "lobed", "leaf_arrangement":
                             "alternate", "leaf_count_band": "4-8", "flower_present": True,
                             "flower_color": ["red"], "stem_features": ["single"],
                             "container_present": False},
    }
    fable = {
        "common": dict(sonnet["common"]),
        "section_features": dict(sonnet["section_features"]),
    }
    # perfect agreement
    result = score_page("H", sonnet, fable)
    assert result["page_disagreement_rate"] == 0.0
    assert result["disagreements"] == []

    # flip a critical field
    fable["section_features"]["root_type"] = "bulbous"
    result = score_page("H", sonnet, fable)
    assert "root_type" in result["disagreements"]
    assert "root_type" in result["critical_disagreements"]
    assert result["page_disagreement_rate"] > 0
