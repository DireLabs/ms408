# E4 — root<->leaf: masked positive or real null?

Generated 2026-07-07T21:51:26+00:00 at commit `6fb18eb360` by `python -m ms408.experiments.e4_root_leaf`. Numbers in `results/experiments/e4_root_leaf.json`.

128 herbal pages. Root-region × leaf-region associations, raw and disattenuated for inter-annotator noise (reliability = 1 − QA disagreement). The clean feature (root_coloring, ~4% noise) carries the affirmative test; disattenuation of the noisy root_type is an approximate guide only.

| pair | root reliability | raw V | disattenuated V | p | significant |
|---|---|---|---|---|---|
| root_type x leaf_shape | 0.65 | 0.2558 | 0.3713 | 0.26575 | no |
| root_type x leaf_arrangement | 0.65 | 0.207 | 0.3185 | 0.69986 | no |
| root_type x leaf_count_band | 0.65 | 0.2495 | 0.3357 | 0.25215 | no |
| root_coloring x leaf_shape | 0.96 | 0.2287 | 0.2732 | 0.24515 | no |
| root_coloring x leaf_arrangement | 0.96 | 0.3953 | 0.5004 | 0.0044 | YES |
| root_coloring x leaf_count_band | 0.96 | 0.361 | 0.3996 | 0.019 | YES |

Multiple-comparison note: BH/Bonferroni across 6 tested pairs; Bonferroni alpha 0.0083. root_coloring pairs surviving BH across the 6: **['root_coloring x leaf_arrangement']**.

### Pigmentation-confound controls (E4 refutation's decisive test)

- Binary coloured/uncoloured root × leaf_arrangement (does 'is it coloured at all' drive it?): V 0.0676, p 0.9764 — NOT significant.
- root_coloring × leaf_arrangement within COLOURED-only pages (115 pages): V 0.4598, p 0.0012, significant True — survives and strengthens.
- (root_coloring × page-coloured is uninformative: ~90% of herbal pages are coloured, so page-coloured barely varies — not a rebuttal either way.)

- **Cross-organ bundle SUGGESTIVE (crude confound rebutted, deep same-source confound pending): True**. Decisive test: independent re-annotation (E4 third-annotator) to rule out same-model-source confound.

## Verdict [B, refutation pass applied]

SUGGESTIVE but not confirmed — the T2.6 'within-organ only' verdict is WEAKENED, not cleanly overturned. root_coloring x leaf_arrangement survives BH across the 6 pairs (p 0.0012 within colours), and the crude page-pigmentation confound is rebutted: the binary coloured/uncoloured split does NOT drive it (V 0.0676, p 0.9764), and it SURVIVES and strengthens within coloured-only pages (V 0.4598, p 0.0012, n 115). BUT the deep confound the refutation raised — both features come from ONE vision model on ONE image, so a shared visual-gestalt correlation could persist within colours too — is NOT resolvable from these controls. Only INDEPENDENT re-annotation (the E4 third-annotator pass) settles it. Two cautions remain: only leaf_arrangement survives correction (leaf_count_band does not, and the two are non-independent), and the pre-registered pair root_type x leaf_shape is still null even disattenuated (~0.3713, p 0.26575). Net: the herbal MAY have a real cross-organ bundle; the page-colouring artifact is ruled out but the same-source artifact is not. Decisive test pending.
