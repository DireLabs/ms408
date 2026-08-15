# E23 — Positional + reuse generator: genericity sweep

Generated 2026-08-14T06:58:40+00:00 at commit `4800a23cbe` by `python -m ms408.experiments.e23_reuse_generator`. Numbers in `results/experiments/e23_reuse_generator.json`.

A-priori grid: 104 configs, ranges {'rho': [0.0, 0.2, 0.4, 0.6, 0.8], 'variant': ['local_w50', 'local_w200', 'global'], 'branching': [4, 5, 6, 7], 'boost': [6.0, 16.0], 'zipf_exp': 0.8, 'block_len': 400, 'note': 'fixed a-priori; a sweep, not a fitted point'}.

## Did reuse close the three axes E22 never matched?

- **ed1_main_component**: IN-band from ρ=0.6 (global/local_w200/local_w50)
- **type_token_ratio**: IN-band from ρ=0.4 (global/local_w200/local_w50)
- **zipf_slope**: IN-band from ρ=0.8 (global/local_w200)

## Basin

- ≥6/8 axes incl. VMS positive wc_z: **0%** (0 configs)
- ρ=0 baseline best: 2/8 (E22 regime)
- axes never matched anywhere: **['mean_word_length']**

Best config: ρ=0.4, global, branching 5, boost 6.0 -> 4/8 (vms_syntax=True).

## Verdict [C, refutation pass pending]

REUSE HELPS (notably restores the VMS's word-class structure) BUT A PARETO TENSION REMAINS. Word reuse individually rescues every axis E22 could never reach — ED1, TTR and Zipf all become reachable — and GLOBAL preferential attachment additionally lifts wc_z from E22's anti-structure (−1.02) into the VMS's weak-positive band (restored), a real gain over the context-free generator. BUT the axes are MUTUALLY CONSTRAINING under reuse and never align: each E22-missed axis is reachable only at its OWN reuse level (ED1 ρ≥0.6, TTR ρ≥0.4, Zipf ρ≥0.8), and no single config satisfies even the whole frequency-concentration group ['ed1_main_component', 'type_token_ratio', 'zipf_slope'] (0 configs do), let alone jointly with the entropy/ΔI/word-class group ['h2', 'mz_peak_value', 'wc_z'] (1 config holds that group, at ρ=0.4 global; 0 config holds BOTH). The reuse level that concentrates frequency (high ρ) simultaneously deflates the character entropy and block-ΔI and re-negates the word-class structure. So the VMS's low entropy + retained ΔI + weak-positive syntax COEXIST with heavy word reuse in a way simple token-copying cannot reproduce; the next mechanism must concentrate frequency WITHOUT spending entropy/ΔI (e.g. a genuinely small, skewed TYPE lexicon with constrained morphology, rather than token-level copying). SCOPE: grid fixes Zipf exponent, block length and word length (~5.15, a narrow-band near-miss); the tension is over ρ×variant×branching×boost. Over an a-priori grid of 104 (ρ [0.0, 0.2, 0.4, 0.6, 0.8] × variant ['local_w50', 'local_w200', 'global'] × branching [4, 5, 6, 7] × boost [6.0, 16.0]). Reuse vs the E22 misses — ed1: IN-band (from ρ=0.6, global/local_w200/local_w50); type: IN-band (from ρ=0.4, global/local_w200/local_w50); zipf: IN-band (from ρ=0.8, global/local_w200). ρ=0 baseline best 2/8; best overall (ρ=0.4, global, branching 5, boost 6.0) 4/8 (vms_syntax=True). Axes never matched anywhere: [mean_word_length]. Best sig: h2=2.1275 ΔI=0.0841 ED1=0.9787 TTR=0.4126 Zipf=-0.53 fc_z=-4.47 wc_z=2.06. (L7.)
