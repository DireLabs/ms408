# T2.3 Study Report — Anchor Hunt (W3)

Generated 2026-07-06T21:15:39+00:00 at commit `abb7923414` by `python -m ms408.studies.anchor_hunt`; full numbers in `results/studies/anchor_hunt.json`.

Section H: 129 pages, 314 testable tokens × 34 feature indicators = 10,676 tests, BH-FDR q=0.05.

## Harness gate (L4 — must pass before anchors are admissible)

- **Null control** (features × page-shuffled text): 0 false discoveries in 10,676 tests (fraction 0.0, ≤ q required).
- **Planted control** (synthetic token on 'illustration_coverage_pct=51-75' pages): recovered = True (phi 1.0, p 0.0).
- **Gate PASSED** — H1 anchors admissible.

## Candidate anchors (graded C pending T3.3; L7 — no translation claim)

Token↔feature associations surviving FDR, by phi. These are co-occurrence statistics, NOT meanings: a high-phi pair means the token and the visual feature tend to appear on the same pages, nothing more.

| token | feature | phi | p | pages(token∧feature) |
|---|---|---|---|---|
| _(none survived FDR)_ | | | | |

## Result: rigorous null (graded C; a null is itself a constraint)

**No Voynichese token anchors to a herbal visual feature** after FDR correction across 10,676 tests — nothing behaves like 'root' at page-level granularity with the coarse schema. The harness gate passed (null control 0 false discoveries, planted anchor recovered), so this is a real negative, not a broken method.

Strongest sub-threshold associations (none significant), for texture:

| token | feature | phi | p | co-pages |
|---|---|---|---|---|
| `todaiin` | plant_count=3 | 0.5278 | 0.000552 | 3 |
| `olor` | color_palette=yellow | 0.4118 | 0.000763 | 4 |
| `qokchdy` | plant_count=3 | 0.3923 | 0.003153 | 3 |
| `okar` | plant_count=3 | 0.3828 | 0.001265 | 4 |
| `ain` | leaf_shape=palmate | 0.373 | 0.004308 | 3 |
| `cheeky` | leaf_arrangement=basal-rosette | 0.3505 | 0.005637 | 3 |
| `yky` | leaf_shape=palmate | 0.3489 | 0.006041 | 3 |
| `shar` | plant_count=2 | 0.3401 | 0.003483 | 4 |
| `qokaiin` | plant_count=3 | 0.3361 | 0.002939 | 4 |
| `chdy` | plant_count=3 | 0.3361 | 0.002939 | 4 |

Two caveats on the strongest raw signals: (a) most co-occur on only 2-5 pages (tiny-sample noise); (b) the very strongest (`qokedy`/`shedy` ↔ separate-zones layout) reflect the **Currier A/B dialect confound** leaking through a layout feature, not semantics. The higher-power follow-up is label-level anchoring (word-next-to-feature), which needs label-region↔feature annotation beyond the coarse schema — flag for the fine-schema extension (L15) and T2.3b.

## Notes
- Claims graded C (candidate B pending T3.3 adversarial review, L10).
- L7: nothing here is a translation. An anchor is a statistical co-occurrence, to be corroborated by an independent method before any semantic reading is entertained.
