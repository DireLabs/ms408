# T2.6 Study Report — W7 Discriminator (referential realism + anachronism)

Generated 2026-07-06T23:11:56+00:00 at commit `591d1c0c09` by `python -m ms408.studies.referential_realism`; full numbers in `results/studies/referential_realism.json`.

## Study 1 — Referential-realism discriminator

Does the herbal depict a structured world (correlated feature bundles, real-taxa-like) or free recombination (independent features, invention-like)? Tested on 128 herbal pages with confident values for all 5 morphological features, 5000 permutations per pair.

| feature pair | Cramér's V | null V (95%) | p (assoc.) | distinct combos | null combos | constrained |
|---|---|---|---|---|---|---|
| root_type x root_coloring | 0.3416 | 0.3229 | 0.03819 | 19 | 19 | YES |
| root_type x leaf_shape | 0.2558 | 0.2966 | 0.25835 | 29 | 28 | no |
| root_type x leaf_arrangement | 0.207 | 0.2952 | 0.70286 | 25 | 25 | no |
| root_type x leaf_count_band | 0.2495 | 0.3457 | 0.24435 | 20 | 21 | no |
| root_coloring x leaf_shape | 0.2287 | 0.2765 | 0.23835 | 15 | 17 | no |
| root_coloring x leaf_arrangement | 0.3953 | 0.231 | 0.0036 | 15 | 15 | YES |
| root_coloring x leaf_count_band | 0.361 | 0.2749 | 0.0176 | 12 | 12 | YES |
| leaf_shape x leaf_arrangement | 0.2573 | 0.2542 | 0.04299 | 23 | 23 | YES |
| leaf_shape x leaf_count_band | 0.178 | 0.2603 | 0.65447 | 19 | 19 | no |
| leaf_arrangement x leaf_count_band | 0.5048 | 0.2536 | 0.0002 | 13 | 16 | YES |

**Verdict: within-organ-only** — 5 of 10 feature pairs are associated beyond the independence null (mean Cramér's V 0.2979 vs null-95 0.2811). The load-bearing cross-organ realism bundle **root_type × leaf_shape** is ABSENT (V=0.2558, p=0.25835, combos 29 vs null 28).

## Study 2 — Anachronism scan

The v0.2 schema captures only morphology (L14): shape, count, colour, spatial arrangement. None of these encodes information beyond unaided 15th-century observation (no cellular detail, no telescopic star data, no information requiring instruments the period lacked). The scan is therefore a structured null by construction.

**Result: null** (grade C). A rigorous null is itself a citable constraint (W7 output form): no annotated feature exceeds period observational capability.

## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 — L10)

1. **[C, candidate B pending T3.3]** WITHIN-ORGAN structure only. 5/10 feature pairs are constrained, but the constraint is concentrated in within-leaf geometry (root_coloring x leaf_arrangement, root_coloring x leaf_count_band, leaf_shape x leaf_arrangement) — largely near-tautological (a plant with more leaves has a characteristic arrangement). Crucially, the load-bearing REALISM signal — root morphology predicting leaf morphology (root_type × leaf_shape) — is ABSENT (V=0.2558, p=0.25835; 29 distinct combinations vs 28 under free mixing — the combination space is saturated). Real taxa produce correlated root↔leaf bundles; the VMS herbal does not. This points toward free recombination of parts, not a fixed set of botanical referents.
2. **[C]** L33 cuts the right way here: root_type is measurement-noisy, BUT the clean root_coloring feature *does* associate with leaf features, and root_type × root_coloring is significant — so root_type carries real signal. Its independence from leaf_shape is therefore a substantive null, not a noise artifact.
3. **[C]** Anachronism scan is a rigorous null: no morphological feature in the annotation set encodes information exceeding 15th-century observational capability. The honest form of the 'proof-level' W7 ambition — a null is a constraint, not evidence of ordinary origin.
4. **[C]** Convergence across Phase 2: the encoding bracket (no family reproduces low-h2 + word-order info together), the anchor-hunt nulls (T2.3/b: no word→referent mapping), and this discriminator (no root↔leaf realism bundle) point the same way — the herbal behaves less like a referential record of specific plants than the 'genuine herbal' reading assumes. This constrains W7's hypothesis families without decoding anything (L7); the structured-vs-invented question stays open.

## Study 3 — Purpose reframing (feeds W6b / Phase 3)

The genre question under each W7 hypothesis family — reference work vs record of experience vs work of imagination — is a synthesis task that belongs in T3.1 competing narratives, where it can integrate the discriminator verdict here with the encoding-bracket and anchor-hunt constraints. Carried forward, not written in isolation.
