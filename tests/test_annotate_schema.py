from ms408.annotate.schema import (
    SECTION_BLOCKS,
    critical_fields,
    fields_for,
    tool_schema,
)


def test_every_section_schema_is_strict_valid():
    for code in SECTION_BLOCKS:
        schema = tool_schema(code)
        assert schema["additionalProperties"] is False
        # strict tool use: every property must be required
        assert set(schema["required"]) == set(schema["properties"])
        # strict tool use forbids minimum/maximum on integers
        for prop in schema["properties"].values():
            assert "minimum" not in prop and "maximum" not in prop


def test_count_fields_are_bounded_enums():
    herbal = tool_schema("H")["properties"]
    assert herbal["plant_count"]["type"] == "integer"
    assert herbal["plant_count"]["enum"] == list(range(10))


def test_common_block_on_every_section():
    for code in SECTION_BLOCKS:
        props = tool_schema(code)["properties"]
        for common_field in ("illustration_coverage_pct", "color_palette", "marginalia_present"):
            assert common_field in props
        assert "notes" in props


def test_text_and_star_pages_get_common_only():
    for code in ("S", "T"):
        # 5 common fields + notes
        assert len(tool_schema(code)["properties"]) == 6


def test_critical_fields_are_anchor_hunt_features():
    assert set(critical_fields("H")) == {"plant_count", "root_type", "leaf_shape",
                                         "flower_present"}
    assert "plumbing_present" in critical_fields("B")
    assert "container_count" in critical_fields("P")


def test_enum_fields_include_unclear():
    for field in fields_for("H"):
        if field.kind == "enum":
            assert "unclear" in field.values
