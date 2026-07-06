# T2.3b Study Report — Label-Level Anchoring (W3)

Generated 2026-07-06T23:05:34+00:00 at commit `e906816e83` by `python -m ms408.studies.anchor_labels`; full numbers in `results/studies/anchor_labels.json`.

## Label census — where labels even exist

| section | pages | label-bearing pages | label tokens |
|---|---|---|---|
| A | 8 | 5 | 148 |
| B | 19 | 11 | 125 |
| C | 11 | 5 | 212 |
| H | 129 | 6 | 31 |
| P | 16 | 15 | 238 |
| S | 25 | 0 | 0 |
| T | 7 | 3 | 62 |
| Z | 12 | 12 | 344 |

**Structural finding [C]:** the herbal section — the obvious place to look for a word drawn next to a root — is almost label-free (6 of 129 pages carry any label). The 'word next to the plant part' structure that label-level anchoring assumes largely does not exist there. This reframes the T2.3a page-level null: much of the herbal has no labels to anchor on.

## Recurrence test — do labels behave like a naming system?

| section | label types | TTR | recurring (≥2 pp) | null band (95%) | p | naming system? |
|---|---|---|---|---|---|---|
| A | 140 | 0.9459 | 4 | [5, 29] | 0.9914 | no |
| B | 112 | 0.896 | 7 | [11, 22] | 1.0 | no |
| C | 188 | 0.8868 | 6 | [3, 29] | 0.77325 | no |
| H | 20 | 0.6452 | 0 | [0, 2] | 1.0 | no |
| P | 225 | 0.9454 | 8 | [25, 41] | 1.0 | no |

## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 — L10)

1. **[C, candidate B pending T3.3]** No section's labels behave like a naming system; if anything, labels recur across pages *less* than running text does. In pharmaceutical — the most label-rich section (238 label tokens on 15 pages) — labels are 95% unique (TTR 0.9454), and only 8 label types recur on ≥2 pages versus a running-text null band of [25, 41] — below the band. Labels below the null in ['A', 'B', 'P'] section(s); above in none. There is no recurring part-name vocabulary.
2. **[C]** The direction matters: a nomenclature (a fixed word for 'root' reused wherever a root is drawn) would push label recurrence ABOVE the running-text baseline. We see the opposite — near-unique labels — consistent with labels being content-like words that avoid the high-frequency grammatical vocabulary of running text, yet are not themselves a reusable naming set.
3. **[C]** Taken with T2.3a, this is a coherent constraint: neither whole-page vocabulary nor the illustration labels form a detectable word→referent mapping. Whatever the labels are, they are not a consistent nomenclature at the granularity our methods can see — evidence against a straightforward 'labelled herbal/pharmacopoeia where words name the depicted things' reading (L7: this constrains, it does not decode).
**Method note:** the null is a size-matched bootstrap of each section's own running text, so recurrence is compared like-for-like against that section's non-label vocabulary — the right baseline.

