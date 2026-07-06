"""Annotation schema v0.1-coarse (T12-annotation-schema.md, locked L31).

Each section block has ~10 strictly morphological/descriptive fields (L14: no
species/sign identification). Field definitions here are the single source of
truth: they generate the strict-tool JSON schema the annotator model must fill,
the Haiku format validator, and the QA agreement metric.

Field kinds:
  enum   -> one value from `values`
  multi  -> subset of `values` (array, may be empty via "none")
  count  -> integer 0-9 (9 means 9+)
  bool   -> true/false
"""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "v0.2-fine"

# v0.2 changes (G2 batch-1 retune, T2.3b readiness):
# - text_image_relationship: 4 clear categories (was 7; drove 46% QA drift)
# - dropped damage_or_stain + marginalia_present from scored fields -> notes only
# - herbal root_color -> coarse root_coloring enum (faded pigment drove 35% drift)
# - added label_attachment (herbal, pharma): which plant parts carry adjacent
#   labels -> the label-region capture T2.3b label-level anchoring needs


@dataclass(frozen=True)
class Field:
    name: str
    kind: str  # enum | multi | count | bool
    values: tuple = ()
    instruction: str = ""
    critical: bool = False  # anchor-hunt fields, tracked separately in QA


UNCLEAR = "unclear"


def _enum(name, values, instruction, critical=False):
    return Field(name, "enum", tuple(values) + (UNCLEAR,), instruction, critical)


def _multi(name, values, instruction, critical=False):
    return Field(name, "multi", tuple(values), instruction, critical)


def _count(name, instruction, critical=False):
    return Field(name, "count", (), instruction, critical)


def _bool(name, instruction, critical=False):
    return Field(name, "bool", (), instruction, critical)


COMMON = [
    _enum("illustration_coverage_pct", ["0", "1-25", "26-50", "51-75", "76-100"],
          "Band of page area occupied by illustration vs text/blank."),
    _enum("text_image_relationship",
          ["image-with-running-text", "image-with-labels-only", "image-only", "text-only"],
          "Does the running Voynichese text share the page with the image? "
          "'image-with-running-text' = paragraphs of text beside/around the image; "
          "'image-with-labels-only' = only short word-labels touch the image; "
          "'image-only' / 'text-only' = essentially one or the other."),
    _multi("color_palette", ["none/ink-only", "green", "blue", "red", "ochre/brown",
                             "yellow"], "Pigments present anywhere on the page."),
]
# damage/staining and later marginalia are captured in `notes` only (v0.2):
# both were 35% cross-model-noisy as scored booleans and are not analysis inputs.

HERBAL = [
    _count("plant_count", "Number of distinct whole-plant drawings on the page.", True),
    _enum("root_type", ["none", "taproot", "branched", "bulbous", "tuberous",
                        "fibrous/stringy", "zoomorphic", "other"],
          "Dominant root morphology of the primary plant. Shape only, no species.", True),
    _enum("root_coloring", ["uncolored", "brown-ochre", "red", "green", "other"],
          "Coarse dominant pigment of the root (faded — one bucket, not a hue list)."),
    _enum("leaf_shape", ["simple-entire", "lobed", "palmate", "serrated",
                        "needle/linear", "compound", "heart"],
          "Dominant leaf outline of the primary plant.", True),
    _enum("leaf_arrangement", ["alternate", "opposite", "whorled", "basal-rosette", "single"],
          "How leaves attach along the stem."),
    _enum("leaf_count_band", ["1-3", "4-8", "9-20", "20+"],
          "Coarse count band of leaves on the primary plant."),
    _bool("flower_present", "Are flowers/inflorescences drawn?", True),
    _multi("stem_features", ["single", "multiple", "branched", "tendrils", "none/unclear"],
           "Stem structure of the primary plant."),
    _multi("label_attachment", ["none", "root", "leaf", "flower", "stem", "whole-plant"],
           "Which plant parts have a short Voynichese word-label drawn touching or "
           "immediately beside them (label-level anchoring, T2.3b). 'none' if labels "
           "are absent or not attached to a specific part.", True),
    _bool("container_present", "Is the plant shown in/emerging from a pot, jar, or vessel?"),
]

BIOLOGICAL = [
    _enum("nymph_count_band", ["0", "1-3", "4-8", "9-15", "16+"],
          "Coarse count of human figures ('nymphs') on the page.", True),
    _multi("nymph_pose_class", ["standing", "reclining", "in-vessel",
                                "swimming/floating", "holding-object"],
           "Dominant pose category/categories."),
    _bool("basin_tub_present", "Any basin, tub, bath, or pool structure holding figures?"),
    _count("basin_count", "Number of distinct basins/tubs/pools."),
    _bool("plumbing_present", "Any pipes, tubes, channels, or spouts connecting features?", True),
    _multi("plumbing_connects", ["none", "basin-basin", "basin-figure", "basin-margin",
                                 "tube-network"], "What the plumbing links."),
    _bool("liquid_depicted", "Is water/liquid shown (green/blue fill, wavy lines)?"),
    _multi("liquid_color", ["none", "green", "blue", "uncolored"], "Pigment used for liquid/pools."),
    _multi("figure_adornment", ["none", "crown", "headdress", "held-object", "star"],
           "Recurring accessories on figures (descriptive)."),
    _enum("layout_flow", ["single-scene", "top-bottom-panels", "network/branching"],
          "Overall compositional structure."),
]

ZODIAC_ASTRO = [
    _enum("diagram_form", ["concentric-rings", "radial-spokes", "medallion", "rosette",
                          "grid", "freeform"], "Overall diagram geometry."),
    _enum("central_emblem_class", ["none", "sun", "moon", "star", "human-figure",
                                  "animal/zodiac-creature", "vessel", "floral"],
          "Class of the central motif (descriptive, not zodiac-name).", True),
    _count("ring_band_count", "Number of concentric rings/bands."),
    _enum("nymph_count_band", ["0", "1-3", "4-8", "9-15", "16-30", "30+"],
          "Coarse count of human figures in the diagram.", True),
    _enum("star_count_band", ["0", "1-10", "11-30", "31+"],
          "Coarse count of star glyphs.", True),
    _bool("figures_in_containers", "Are figures shown standing in tubs/barrels?"),
    _multi("label_positions", ["none", "radial-spoke", "ring-inner", "ring-outer",
                               "beside-figure", "corner"],
           "Where text labels sit relative to the diagram."),
    _multi("celestial_bodies", ["none", "sun", "moon", "stars"],
           "Which celestial motifs appear anywhere on the page."),
    _multi("color_zones", ["none", "red", "blue", "green", "ochre"],
           "Pigments used to fill diagram sectors/figures."),
    _bool("panel_of_foldout", "Is this page one panel of a larger foldout?"),
]

PHARMACEUTICAL = [
    _count("container_count", "Number of jars/vessels ('albarelli') drawn.", True),
    _multi("container_types", ["none", "cylindrical-jar", "footed/pedestal",
                               "ornate-tiered", "spouted", "banded", "other"],
           "Vessel silhouette classes present."),
    _multi("container_colors", ["none", "red", "green", "blue", "ochre", "uncolored"],
           "Pigments on the vessels."),
    _count("plant_part_rows", "Number of horizontal rows of plant-part fragments."),
    _multi("plant_parts_depicted", ["roots", "leaves", "stems", "flowers",
                                    "seeds/fruit", "whole-plant"],
           "Which detached plant parts appear (morphological only).", True),
    _multi("root_forms", ["none", "taproot", "branched", "bulbous", "fibrous", "zoomorphic"],
           "Root morphologies among the fragments."),
    _multi("leaf_forms", ["none", "simple", "lobed", "serrated", "compound"],
           "Leaf morphologies among the fragments."),
    _multi("label_attachment", ["none", "jar", "root", "leaf", "stem", "flower", "seed"],
           "Which elements have a short Voynichese word-label drawn touching or "
           "immediately beside them (label-level anchoring, T2.3b). 'none' if labels "
           "are absent or not attached to a specific element.", True),
    _enum("parts_per_row_band", ["1-3", "4-8", "9+", "mixed"],
          "Coarse density of items per row."),
    _bool("whole_plant_present", "Is any complete plant (not just a fragment) shown?"),
]

# illustration-type code ($I) -> section block
SECTION_BLOCKS = {
    "H": ("herbal", HERBAL),
    "B": ("biological", BIOLOGICAL),
    "Z": ("zodiac_astro", ZODIAC_ASTRO),
    "A": ("zodiac_astro", ZODIAC_ASTRO),
    "C": ("zodiac_astro", ZODIAC_ASTRO),
    "P": ("pharmaceutical", PHARMACEUTICAL),
    # S (recipes/stars) and T (text-only) get the common block only
    "S": (None, []),
    "T": (None, []),
}


def _json_property(field: Field) -> dict:
    if field.kind == "enum":
        return {"type": "string", "enum": list(field.values), "description": field.instruction}
    if field.kind == "multi":
        return {
            "type": "array",
            "items": {"type": "string", "enum": list(field.values)},
            "description": field.instruction + " (list all that apply; use 'none' if none)",
        }
    if field.kind == "count":
        # strict tool use forbids minimum/maximum; use a bounded integer enum instead
        return {"type": "integer", "enum": list(range(10)),
                "description": field.instruction + " (0-9; use 9 for 9 or more)"}
    if field.kind == "bool":
        return {"type": "boolean", "description": field.instruction}
    raise ValueError(field.kind)


def tool_schema(section_code: str) -> dict:
    """Strict-tool input_schema for a page of the given illustration type."""
    _, block = SECTION_BLOCKS.get(section_code, (None, []))
    fields = COMMON + block
    properties = {f.name: _json_property(f) for f in fields}
    properties["notes"] = {
        "type": "string",
        "description": "Ambiguity only, <=120 chars, descriptive not identificational. "
        "Empty string if nothing to note.",
    }
    return {
        "type": "object",
        "properties": properties,
        "required": [f.name for f in fields] + ["notes"],
        "additionalProperties": False,
    }


def fields_for(section_code: str) -> list:
    _, block = SECTION_BLOCKS.get(section_code, (None, []))
    return COMMON + block


def critical_fields(section_code: str) -> list:
    return [f.name for f in fields_for(section_code) if f.critical]
