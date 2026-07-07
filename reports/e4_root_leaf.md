# E4 — root<->leaf: masked positive or real null?

Generated 2026-07-07T21:41:11+00:00 at commit `691d0b0d38` by `python -m ms408.experiments.e4_root_leaf`. Numbers in `results/experiments/e4_root_leaf.json`.

128 herbal pages. Root-region × leaf-region associations, raw and disattenuated for inter-annotator noise (reliability = 1 − QA disagreement). The clean feature (root_coloring, ~4% noise) carries the affirmative test; disattenuation of the noisy root_type is an approximate guide only.

| pair | root reliability | raw V | disattenuated V | p | significant |
|---|---|---|---|---|---|
| root_type x leaf_shape | 0.65 | 0.2558 | 0.3713 | 0.26575 | no |
| root_type x leaf_arrangement | 0.65 | 0.207 | 0.3185 | 0.69986 | no |
| root_type x leaf_count_band | 0.65 | 0.2495 | 0.3357 | 0.25215 | no |
| root_coloring x leaf_shape | 0.96 | 0.2287 | 0.2732 | 0.24515 | no |
| root_coloring x leaf_arrangement | 0.96 | 0.3953 | 0.5004 | 0.0044 | YES |
| root_coloring x leaf_count_band | 0.96 | 0.361 | 0.3996 | 0.019 | YES |

- Clean root_coloring significant with: **['root_coloring x leaf_arrangement', 'root_coloring x leaf_count_band']**.
- Cross-organ bundle exists: **True**.

## Verdict [B, pending refutation pass]

OVERTURNS the i01 'no cross-organ bundle' null. The CLEAN root-region feature root_coloring (~4% noise) associates significantly with leaf morphology (root_coloring x leaf_arrangement, root_coloring x leaf_count_band) — a real cross-organ (root-region <-> leaf-region) feature bundle that root_type's 35% noise could not show. The i01 headline pair root_type x leaf_shape (V 0.2558, p 0.26575) disattenuates to ~0.3713 — a moderate association sitting right at the E3 page-level detection floor (phi~0.4), i.e. a masked positive, not a true null. The herbal has cross-organ morphological structure after all; the T2.6 'within-organ only' verdict is withdrawn. (This does NOT by itself decide real-vs-invented: a systematically invented herbal also has bundled features. It removes one of the three legs i01 leaned against the referential-herbal reading.)
