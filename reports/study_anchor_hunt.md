# T2.3 Study Report — Anchor Hunt (W3)

Generated 2026-07-06T19:09:25+00:00 at commit `fa4d52f4f8` by `python -m ms408.studies.anchor_hunt`; full numbers in `results/studies/anchor_hunt.json`.

Section H: 129 pages, 314 testable tokens × 47 feature indicators = 14,758 tests, BH-FDR q=0.05.

## Harness gate (L4 — must pass before anchors are admissible)

- **Null control** (features × page-shuffled text): 0 false discoveries in 14,758 tests (fraction 0.0, ≤ q required).
- **Planted control** (synthetic token on 'illustration_coverage_pct=51-75' pages): recovered = True (phi 1.0, p 0.0).
- **Gate PASSED** — H1 anchors admissible.

## Candidate anchors (graded C pending T3.3; L7 — no translation claim)

Token↔feature associations surviving FDR, by phi. These are co-occurrence statistics, NOT meanings: a high-phi pair means the token and the visual feature tend to appear on the same pages, nothing more.

| token | feature | phi | p | pages(token∧feature) |
|---|---|---|---|---|
| _(none survived FDR)_ | | | | |

## Result: rigorous null (graded C; a null is itself a constraint)

**No Voynichese token anchors to a herbal visual feature** after FDR correction across 14,758 tests — nothing behaves like 'root' at page-level granularity with the coarse schema. The harness gate passed (null control 0 false discoveries, planted anchor recovered), so this is a real negative, not a broken method.

Strongest sub-threshold associations (none significant), for texture:

| token | feature | phi | p | co-pages |
|---|---|---|---|---|
| `todaiin` | plant_count=3 | 0.4756 | 0.001084 | 3 |
| `olor` | color_palette=yellow | 0.4283 | 0.000576 | 4 |
| `qokaiin` | plant_count=3 | 0.3892 | 0.000508 | 5 |
| `qokedy` | text_image_relationship=separate-zones | 0.3739 | 6.4e-05 | 13 |
| `shedy` | text_image_relationship=separate-zones | 0.3492 | 0.000192 | 12 |
| `yky` | leaf_shape=palmate | 0.3489 | 0.006041 | 3 |
| `qokchdy` | plant_count=3 | 0.3489 | 0.006041 | 3 |
| `shdy` | stem_features=multiple | 0.3448 | 0.000394 | 9 |
| `chodar` | root_type=zoomorphic | 0.3371 | 0.017044 | 2 |
| `chal` | illustration_coverage_pct=26-50 | 0.3371 | 0.017044 | 2 |

Two caveats on the strongest raw signals: (a) most co-occur on only 2-5 pages (tiny-sample noise); (b) the very strongest (`qokedy`/`shedy` ↔ separate-zones layout) reflect the **Currier A/B dialect confound** leaking through a layout feature, not semantics. The higher-power follow-up is label-level anchoring (word-next-to-feature), which needs label-region↔feature annotation beyond the coarse schema — flag for the fine-schema extension (L15) and T2.3b.

## Notes
- Claims graded C (candidate B pending T3.3 adversarial review, L10).
- L7: nothing here is a translation. An anchor is a statistical co-occurrence, to be corroborated by an independent method before any semantic reading is entertained.
