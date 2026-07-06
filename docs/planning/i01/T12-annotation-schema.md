# T1.2 — Coarse Annotation Schema (MS408 illustrated pages)

**Task:** T1.2 (feeds T1.3 bulk annotation; gate G2). **Schema version:** `v0.1-coarse`.
**Binding decisions:** L14 (plant IDs are soft priors — features here are strictly
MORPHOLOGICAL/descriptive, never identificational) and L15 (start coarse at ~10 features per
illustration; extend only after the first QA batch).

## 0. Scope and section counts

Section (`illustration` field in `pages_zl.jsonl`) coverage of the illustrated corpus:

| Code | Section | Pages | Schema block |
|------|---------|-------|--------------|
| H | Herbal | 129 | Herbal |
| B | Biological / balneological | 19 | Biological |
| Z | Zodiac | 12 | Zodiac/Astro |
| A | Astronomical | 8 | Zodiac/Astro |
| C | Cosmological | 11 | Zodiac/Astro (astro variant) |
| P | Pharmaceutical | 16 | Pharmaceutical |
| S | Recipes / stars | 25 | Common block only (mostly text + star bullets) |
| T | Text-only | 7 | Common block only |

Total ~227 IVTFF page records; ~200 carry illustrations. Every page gets the **common block**;
pages in H/B/Z/A/C/P additionally get their section block. S and T pages get the common block only
(S pages carry star/paragraph markers but no compositional illustration to decompose).

**Foldout ambiguity (not resolved here — flagged per task):** 20 pages map ambiguously to scan
files in `scan_map.json` (`ambiguous: true`): f70v1, f70v2, f72v1–3, f85r1, f85r2, f86v3–6,
f89v1, f89v2, f90r1, f90r2, f95v1, f95v2, f101v, f102v1, f102v2. These are foldout panels split
across multiple scan tiles or sharing a tile. T1.3 must record which scan file(s) each panel was
annotated from; where a panel spans two tiles the annotator sets `scan_tiles` to the list and sets
`foldout_ambiguous: true`. Resolution of the IVTFF-panel↔tile mapping is deferred to Tim (open
question OQ-1).

---

## 1. Section schemas (~10 coarse features each)

Types: `enum` (single choice), `enum-multi` (set), `count` (integer; use `9` to mean "9 or more"),
`boolean`, `short-text` (≤5 words, descriptive only). Every field allows `unclear` / `null` when the
scan does not support a confident call — annotators are instructed to prefer `unclear` over guessing.

### 1a. Herbal (H) — anchor-hunt block

| # | Field | Type | Allowed values | Instruction |
|---|-------|------|----------------|-------------|
| 1 | `plant_count` | count | 0–9 (9=9+) | Number of distinct whole-plant drawings on the page. |
| 2 | `root_type` | enum | none, taproot, branched, bulbous, tuberous, fibrous/stringy, zoomorphic, other, unclear | Dominant root morphology of the primary plant. Shape only, no species. |
| 3 | `root_color` | enum-multi | none, brown, red, green, blue, ochre, uncolored | Pigments used on the root(s). |
| 4 | `leaf_shape` | enum | simple-entire, lobed, palmate, serrated, needle/linear, compound, heart, unclear | Dominant leaf outline of the primary plant. |
| 5 | `leaf_arrangement` | enum | alternate, opposite, whorled, basal-rosette, single, unclear | How leaves attach along the stem. |
| 6 | `leaf_count_band` | enum | 1-3, 4-8, 9-20, 20+, unclear | Coarse count band of leaves on the primary plant. |
| 7 | `flower_present` | boolean | true, false | Are flowers/inflorescences drawn? |
| 8 | `flower_color` | enum-multi | none, white/uncolored, red, blue, yellow/ochre, green, other | Pigments on the flowers. |
| 9 | `stem_features` | enum-multi | single, multiple, branched, tendrils, none/unclear | Stem structure of the primary plant. |
| 10 | `container_present` | boolean | true, false | Is the plant shown in/emerging from a pot, jar, or vessel? (rare in H, common in P). |

### 1b. Biological / balneological (B)

| # | Field | Type | Allowed values | Instruction |
|---|-------|------|----------------|-------------|
| 1 | `nymph_count_band` | enum | 0, 1-3, 4-8, 9-15, 16+, unclear | Coarse count of human figures ("nymphs") on the page. |
| 2 | `nymph_pose_class` | enum-multi | standing, reclining, in-vessel, swimming/floating, holding-object, unclear | Dominant pose category/categories. |
| 3 | `basin_tub_present` | boolean | true, false | Any basin, tub, bath, or pool structure holding figures? |
| 4 | `basin_count` | count | 0–9 | Number of distinct basins/tubs/pools. |
| 5 | `plumbing_present` | boolean | true, false | Any pipes, tubes, channels, or spouts connecting features? |
| 6 | `plumbing_connects` | enum-multi | none, basin-basin, basin-figure, basin-margin, tube-network, unclear | What the plumbing links. |
| 7 | `liquid_depicted` | boolean | true, false | Is water/liquid shown (green/blue fill, wavy lines)? |
| 8 | `liquid_color` | enum-multi | none, green, blue, uncolored | Pigment used for liquid/pools. |
| 9 | `figure_adornment` | enum-multi | none, crown, headdress, held-object, star, unclear | Recurring accessories on figures (descriptive). |
| 10 | `layout_flow` | enum | single-scene, top-bottom-panels, network/branching, unclear | Overall compositional structure. |

### 1c. Zodiac / Astronomical / Cosmological (Z, A, C)

| # | Field | Type | Allowed values | Instruction |
|---|-------|------|----------------|-------------|
| 1 | `diagram_form` | enum | concentric-rings, radial-spokes, medallion, rosette, grid, freeform, unclear | Overall diagram geometry. |
| 2 | `central_emblem_class` | enum | none, sun, moon, star, human-figure, animal/zodiac-creature, vessel, floral, unclear | Class of the central motif (descriptive, not zodiac-name). |
| 3 | `ring_band_count` | count | 0–9 | Number of concentric rings/bands. |
| 4 | `nymph_count_band` | enum | 0, 1-3, 4-8, 9-15, 16-30, 30+, unclear | Coarse count of human figures in the diagram. |
| 5 | `star_count_band` | enum | 0, 1-10, 11-30, 31+, unclear | Coarse count of star glyphs. |
| 6 | `figures_in_containers` | boolean | true, false | Are figures shown standing in tubs/barrels (as on zodiac rings)? |
| 7 | `label_positions` | enum-multi | none, radial-spoke, ring-inner, ring-outer, beside-figure, corner, unclear | Where text labels sit relative to the diagram. |
| 8 | `celestial_bodies` | enum-multi | none, sun, moon, stars, unclear | Which celestial motifs appear anywhere on the page. |
| 9 | `color_zones` | enum-multi | none, red, blue, green, ochre | Pigments used to fill diagram sectors/figures. |
| 10 | `panel_of_foldout` | boolean | true, false | Is this page one panel of a larger foldout (Z/A/C are foldout-heavy)? |

### 1d. Pharmaceutical (P)

| # | Field | Type | Allowed values | Instruction |
|---|-------|------|----------------|-------------|
| 1 | `container_count` | count | 0–9 | Number of jars/vessels ("albarelli") drawn. |
| 2 | `container_types` | enum-multi | none, cylindrical-jar, footed/pedestal, ornate-tiered, spouted, banded, other | Vessel silhouette classes present. |
| 3 | `container_colors` | enum-multi | none, red, green, blue, ochre, uncolored | Pigments on the vessels. |
| 4 | `plant_part_rows` | count | 0–9 | Number of horizontal rows of plant-part fragments. |
| 5 | `plant_parts_depicted` | enum-multi | roots, leaves, stems, flowers, seeds/fruit, whole-plant, unclear | Which detached plant parts appear (morphological only). |
| 6 | `root_forms` | enum-multi | none, taproot, branched, bulbous, fibrous, zoomorphic, unclear | Root morphologies among the fragments. |
| 7 | `leaf_forms` | enum-multi | none, simple, lobed, serrated, compound, unclear | Leaf morphologies among the fragments. |
| 8 | `label_present` | boolean | true, false | Are short text labels attached to individual parts/jars? |
| 9 | `parts_per_row_band` | enum | 1-3, 4-8, 9+, mixed, unclear | Coarse density of items per row. |
| 10 | `whole_plant_present` | boolean | true, false | Is any complete plant (not just a fragment) shown? |

---

## 2. Common block (every page)

| # | Field | Type | Allowed values | Instruction |
|---|-------|------|----------------|-------------|
| 1 | `illustration_coverage_pct` | enum | 0, 1-25, 26-50, 51-75, 76-100 | Band of page area occupied by illustration vs. text/blank. |
| 2 | `text_image_relationship` | enum | text-wraps-image, image-in-text-block, text-labels-only, separate-zones, text-only, image-only, unclear | How text and illustration are spatially arranged. |
| 3 | `color_palette` | enum-multi | none/ink-only, green, blue, red, ochre/brown, yellow | Pigments present anywhere on the page. |
| 4 | `marginalia_present` | boolean | true, false | Any later marginal notes, non-Voynichese script, or added marks? |
| 5 | `damage_or_stain` | boolean | true, false | Significant staining, offset, or damage that could affect feature calls. |
| 6 | `foldout_ambiguous` | boolean | true, false | Set true if this panel maps ambiguously to scan tiles (see §0). |

---

## 3. Worked examples

Annotations below were filled by reading the actual scans. `unclear`/ambiguity notes are called out.

### Example A — f2r · `005_2r.jpg` (Herbal)
Whole plant, thistle-like heads, red stem, red/brown claw-shaped root, palmate green leaves.
```
common: {coverage: 76-100, text_image_relationship: text-wraps-image, palette: [green, red, ochre/brown], marginalia: false, damage: false, foldout_ambiguous: false}
herbal: {plant_count: 1, root_type: branched, root_color: [red, brown], leaf_shape: palmate,
         leaf_arrangement: alternate, leaf_count_band: 9-20, flower_present: true,
         flower_color: [white/uncolored, ochre], stem_features: [branched], container_present: false}
```
*Ambiguity:* root reads as branched/zoomorphic (claw-like) — flagged `branched` with the zoomorphic
call left for the extended schema; a single faint word floats mid-right (possible label vs. bleed).

### Example B — f4r · `009_4r.jpg` (Herbal)
Tall plant, many small red/green paired leaflets up multiple stems, small buds, thin spidery root.
```
common: {coverage: 51-75, text_image_relationship: text-wraps-image, palette: [green, red], marginalia: false, damage: true, foldout_ambiguous: false}
herbal: {plant_count: 1, root_type: fibrous/stringy, root_color: [uncolored], leaf_shape: simple-entire,
         leaf_arrangement: opposite, leaf_count_band: 20+, flower_present: true,
         flower_color: [white/uncolored], stem_features: [multiple, branched], container_present: false}
```
*Ambiguity:* a faint grey offset plant + star glyph at left is bleed-through from the facing folio,
not this page's content — annotator must not count it (`damage: true` flags the risk).

### Example C — f75r · `135_75r.jpg` (Biological)
Cascade of nude figures descending a green channel into pools; figures also clustered in a green
pool bottom-right; dense two-column text.
```
common: {coverage: 51-75, text_image_relationship: text-wraps-image, palette: [green, ochre/brown], marginalia: false, damage: false, foldout_ambiguous: false}
biological: {nymph_count_band: 16+, nymph_pose_class: [standing, swimming/floating, in-vessel],
             basin_tub_present: true, basin_count: 2, plumbing_present: true,
             plumbing_connects: [basin-figure, tube-network], liquid_depicted: true,
             liquid_color: [green], figure_adornment: [none], layout_flow: network/branching}
```
*Ambiguity:* the green "channel" reads as both liquid and a plant-like stalk; counted as
plumbing/liquid per dominant reading. Exact nymph count not attempted (band 16+).

### Example D — f78r · `141_78r.jpg` (Biological)
Two green tubs of nymphs stacked vertically, joined by a labelled pipe/channel network at top;
figures inside each tub.
```
common: {coverage: 51-75, text_image_relationship: text-wraps-image, palette: [green, red, ochre/brown], marginalia: false, damage: false, foldout_ambiguous: false}
biological: {nymph_count_band: 9-15, nymph_pose_class: [in-vessel, standing], basin_tub_present: true,
             basin_count: 2, plumbing_present: true, plumbing_connects: [basin-basin, tube-network],
             liquid_depicted: true, liquid_color: [green], figure_adornment: [held-object],
             layout_flow: top-bottom-panels}
```
*Ambiguity:* top pipework has short inline labels — captured via common `text_image_relationship`
but no per-pipe label field exists at coarse tier (candidate for extension).

### Example E — f71r · `129_71r.jpg` (Zodiac)
Concentric ring diagram; outer + inner rings of clothed female figures, many holding stars; central
animal emblem; some figures in tubs; radial labels.
```
common: {coverage: 76-100, text_image_relationship: text-labels-only, palette: [red, blue, green, ochre/brown], marginalia: false, damage: true, foldout_ambiguous: false}
zodiac_astro: {diagram_form: concentric-rings, central_emblem_class: animal/zodiac-creature,
               ring_band_count: 2, nymph_count_band: 16-30, star_count_band: 11-30,
               figures_in_containers: true, label_positions: [radial-spoke, beside-figure],
               celestial_bodies: [stars], color_zones: [red, blue, green], panel_of_foldout: false}
```
*Ambiguity:* central creature morphology is descriptive only (`animal`) — no zodiac-sign label
assigned per L14. Small stain lower-center noted (`damage: true`).

### Example F — f99r · `175_99r.jpg` (Pharmaceutical)
Four red cylindrical/banded jars down the left margin; multiple rows of detached roots and leaves;
a large horizontal root-mass at the bottom.
```
common: {coverage: 76-100, text_image_relationship: separate-zones, palette: [red, green, ochre/brown], marginalia: false, damage: false, foldout_ambiguous: false}
pharma: {container_count: 4, container_types: [cylindrical-jar, banded], container_colors: [red],
         plant_part_rows: 4, plant_parts_depicted: [roots, leaves, stems],
         root_forms: [branched, fibrous, zoomorphic], leaf_forms: [simple, lobed],
         label_present: true, parts_per_row_band: 4-8, whole_plant_present: false}
```
*Ambiguity:* bottom root-mass could be one large specimen or a decorative flourish — `whole_plant`
left false, root counted within `plant_parts_depicted`.

*(Cross-check reads used but not fully written out: f88r `161_88r.jpg` — ornate tiered pedestal jars
+ root/leaf rows, confirms `container_types: ornate-tiered/footed`; f67r `121_67r.jpg` — astronomical
sun/moon medallions with radial star-labelled sectors, confirms Z/A block reuse for A/C.)*

---

## 4. QA design (per WORKFLOW §5)

**Roles (locked in WORKFLOW):** Sonnet 4.6 produces bulk annotations; Fable 5 reviews a random
10–15% sample per batch; disagreements adjudicated in Cowork; Tim spot-checks a small fixed subset
each batch for drift.

**Batching.** Process by section (H split into ~3 batches of ~40 pages; B/Z/A/C/P/S each one batch).
QA sample = 12% of each batch, min 5 pages (so small sections still get a floor sample), drawn with a
fixed seed recorded in the run manifest.

**Disagreement metric.** Per reviewed page, compute a per-field agreement then aggregate:
- Each `enum`/`boolean`/`count`-band field: exact match = agree.
- `enum-multi` fields: Jaccard overlap ≥ 0.67 = agree (partial-set tolerance).
- `count` (raw integers): agree if within ±1 or within the same band.
- **Page disagreement rate** = (# disagreeing fields) / (# scored fields on that page).
- **Batch disagreement rate** = mean page disagreement rate over the QA sample.
- Track a **critical-field** subset separately (anchor-hunt fields: herbal root_type/leaf_shape/
  flower_present; bio nymph_count_band/plumbing_present; pharma container_count) — these must not
  be masked by agreement on easy common-block fields.

**Batch-failure threshold (proposed).**
- Batch **fails** if overall batch disagreement rate > **0.20**, OR critical-field disagreement
  rate > **0.15**, OR any single field disagrees on > **40%** of sampled pages (systematic error).
- On failure: adjudicate the sample, patch the annotation instruction or the offending field's value
  set, re-run the whole batch. Thresholds are provisional (L15) and revisited after batch 1.

**Drift check.** Tim's fixed subset (propose 6 pages: 3 herbal, 1 bio, 1 zodiac, 1 pharma) is
re-scored every batch; a rising trend across batches signals model drift even if each batch passes.

## 4b. JSON output format for T1.3

One object per IVTFF page, schema-versioned, one file (`results/t13_annotations.jsonl`) plus a run
manifest recording producing script, git commit, dataset version, model, seed (firewall L1).

```json
{
  "schema_version": "v0.1-coarse",
  "page": "f2r",
  "section": "H",
  "scan_tiles": ["005_2r.jpg"],
  "foldout_ambiguous": false,
  "annotator_model": "sonnet-4.6",
  "annotated_at": "2026-07-06T00:00:00Z",
  "common": {
    "illustration_coverage_pct": "76-100",
    "text_image_relationship": "text-wraps-image",
    "color_palette": ["green", "red", "ochre/brown"],
    "marginalia_present": false,
    "damage_or_stain": false
  },
  "section_features": {
    "plant_count": 1,
    "root_type": "branched",
    "root_color": ["red", "brown"],
    "leaf_shape": "palmate",
    "leaf_arrangement": "alternate",
    "leaf_count_band": "9-20",
    "flower_present": true,
    "flower_color": ["white/uncolored", "ochre"],
    "stem_features": ["branched"],
    "container_present": false
  },
  "notes": "root reads branched/zoomorphic; faint mid-right word may be label",
  "qa": {"reviewed": false, "reviewer_model": null, "disagreements": []}
}
```
Rules: `section_features` keys are exactly the fields for that section's block; unknown values use
`"unclear"` or `null`; `notes` is free-text ≤120 chars for ambiguity only (not identification).
Haiku 4.5 does format validation (enum membership, required keys, band strings) before QA.

## 5. Open questions for Tim

- **OQ-1 (foldout mapping).** 20 panels map ambiguously to scan tiles. Annotate each panel from its
  best-guess tile(s) and flag, or first resolve the IVTFF-panel↔tile mapping as a data task? (Recommend
  annotate-and-flag; cheaper, keeps T1.3 within the $100 cap.)
- **OQ-2 (S pages).** 25 "recipes/stars" pages have star-bullet markers but no decomposable
  illustration. Common block only, or a tiny 2-field S block (`star_bullet_count_band`, `has_marginal_stars`)?
- **OQ-3 (thresholds).** Confirm provisional batch-fail thresholds (0.20 overall / 0.15 critical) and
  the drift-subset page list before batch 1, or accept as defaults and tune post-batch-1 (L15)?
- **OQ-4 (color under L19).** Palette fields assume the current scan set is the color reference. If a
  different color facsimile is later authoritative, palette calls may shift — acceptable for coarse tier?
- **OQ-5 (zoomorphic roots).** Root claw/animal-forms are a known anchor-hunt signal but flirt with
  identification. Keep `zoomorphic` as a pure-shape enum value (current choice), or defer to the
  extended schema to stay maximally descriptive under L14?
