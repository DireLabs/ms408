# E22 — Genericity / coupling sweep of the positional generator

Generated 2026-07-15T08:45:01+00:00 at commit `396487221f` by `python -m ms408.experiments.e22_generator_genericity`. Numbers in `results/experiments/e22_generator_genericity.json`.

A-priori grid: 64 configs, ranges {'branching': [4, 5, 6, 7], 'zipf': [0.6, 0.8, 1.0, 1.2], 'boost': [3.0, 6.0, 10.0, 16.0], 'block_len': 400, 'note': 'fixed a-priori; not centred on the E21 point'}.

## Basins (fraction of grid)

- entropy + ΔI in band: **6%**
- >= 5/8 axes: **0%** (0 configs)
- >= 5/8 axes INCL VMS positive wc_z: **0%** (0 configs)

## Coupling (refutation's prediction)

- configs with TTR in band: 2
- of those, also matching h2 AND ED1: **0**
- axes NEVER matched anywhere on the grid: **['ed1_main_component', 'zipf_slope', 'mean_word_length']**

Best config: branching 6, zipf 1.2, boost 16.0 -> 3/8 axes (vms_syntax=False).

Control (real Latin lexicon under context-free block wrapper): fc_z -1.41, wc_z 2.5.

## Verdict [C, refutation-scoped]

CLASS INSUFFICIENT (coupling failure — the i07 negative stands). NO config in the a-priori grid jointly matches >=5/8 VMS axes with the weak-positive word-class structure; the axes [ed1_main_component, zipf_slope, mean_word_length] are STRUCTURALLY unreachable by a context-free positional slot grammar at any tuning in range. The generator can be tuned to the VMS's entropy and block-ΔI, but not simultaneously to its morphological connectivity (ED1), lexical productivity (TTR), and mild positive word-class structure — those require heavier word reuse / a smaller effective lexicon / correlated slots that a bag-of-slots lacks. So the minimal positional/template class is a partial account only, and the VMS signature demands an added reuse+mild-syntax mechanism. SCOPE: the sweep is the 6-slot family with block_len fixed (the exclusion is over branching/zipf/boost, not slot-count); but the misses are DIRECTIONAL overshoots (ED1, TTR too HIGH) that more slots only worsen, while fewer slots break h2 — so no slot-count reconciles them without the added reuse/correlation mechanism. Over an a-priori grid of 64 configs (branching [4, 5, 6, 7], zipf [0.6, 0.8, 1.0, 1.2], boost [3.0, 6.0, 10.0, 16.0]), 6% match entropy+ΔI, but only 0 configs reach >=5/8 axes and 0 of those also match the VMS's positive wc_z. Axes NEVER matched anywhere on the grid: [ed1_main_component, zipf_slope, mean_word_length]. COUPLING: of 2 configs with TTR in-band, 0 also match h2 AND ED1. Best config (branching 6, zipf 1.2, boost 16.0) reaches 3/8. CONTROL (real Latin lexicon, context-free block wrapper): fc_z -1.41, wc_z 2.5 — confirms context-free block sampling is weak-syntax even with a real lexicon, so the weak syntax is a property of context-free positional sampling, not of the invented morphology. (L7.)
