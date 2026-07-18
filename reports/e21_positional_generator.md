# E21 — Minimal positional/template generator + necessity ablation

Generated 2026-07-15T08:37:33+00:00 at commit `c5a35cb8f2` by `python -m ms408.experiments.e21_positional_generator`. Numbers in `results/experiments/e21_positional_generator.json`.

Constants frozen a-priori (circularity firewall, D-item i07-a): slot_sizes=[5, 6, 6, 5, 4, 3], theme_slot=1, class_slot=3, content_slot=0, zipf_exp=0.7, block_len=400, theme_boost=10.0, syn_stick=0.8.

VMS bands (match target): profile metrics = block-bootstrap 95% CI; fc_z/wc_z = VMS observed [A,B] two-sided. h2 [2.1133, 2.1999], ΔI [0.0735, 0.2057], ED1 [0.7393, 0.766], TTR [0.1634, 0.2961], Zipf [-0.9656, -0.8036], fc_z [-4.71, -1.24], wc_z [1.9, 2.64].

Constants GRID-SELECTED against the VMS bands (not a-priori — see honesty note); E21 shows a fitted point, not class sufficiency.

| config | h2 | ΔI | scale | fc_z | wc_z | ED1 | TTR | Zipf | axes✓ |
|---|---|---|---|---|---|---|---|---|---|
| FULL | 2.139 | 0.0809 | 400 | -2.24 | -1.02 | 0.9981 | 0.594 | -0.3692 | 3/8 |
| ablate_morphology | 4.8429 | 0.0002 | 1250 | 0.0 | 0.0 | 0.0003 | 0.9999 | 0.0 | 0/8 |
| ablate_positional | 2.1357 | 0.0054 | 476 | -0.19 | -0.48 | 0.9973 | 0.5928 | -0.3942 | 1/8 |
| add_syntactic | 1.9419 | 0.2075 | 400 | -6.93 | 6.2 | 0.9928 | 0.4038 | -0.5622 | 0/8 |
| ref_latin | 3.2934 | 0.3881 | 588 | 20.02 | 14.85 | 0.1329 | 0.2649 | -0.9087 | 2/8 |
| ref_shuffle | 3.2934 | 0.0101 | 833 | 0.83 | -0.1 | 0.1329 | 0.2649 | -0.9087 | 2/8 |

FULL matches: **h2, mz_peak_value, fc_z**; misses: **ed1_main_component, zipf_slope, type_token_ratio, mean_word_length, wc_z**.

## Ingredient → property map (refutation-corrected)

- `morphology_necessary_for_h2`: **True**
- `positional_necessary_for_dI`: **True**
- `morphology_ALSO_collapses_dI (ingredient map is NOT a bijection)`: **True**
- `context_free_->_weak_syntax (TAUTOLOGICAL, not counted)`: **True**

## Verdict [C, refutation pass applied]

EXISTENCE OF A FITTED POINT, NOT CLASS SUFFICIENCY (refutation-downgraded from a first-pass B). The generator constants were GRID-SELECTED to land in the VMS bands, so the earlier 'a-priori / blind / circularity firewall' framing is RETRACTED: this is a fitted point, exactly the move that made E19's 'favours generation' positive circular. On the VMS's OWN bands (not a one-sided threshold a full shuffle also passes), the fitted FULL config matches only [h2, mz_peak_value, fc_z] and MISSES [ed1_main_component, zipf_slope, type_token_ratio, mean_word_length, wc_z]. Decisively, it does NOT reproduce the VMS's word-class structure: VMS wc_z is weak-but-POSITIVE [1.9, 2.64] while FULL wc_z=-1.02 is NEGATIVE (less structure than its own shuffle) — a context-free positional grammar produces anti-structure, not the VMS's mild positive syntax. It also OVERSHOOTS vocabulary productivity (TTR 0.594 vs VMS [0.1634, 0.2961]) and morphology connectivity (ED1 0.9981 vs VMS [0.7393, 0.766]) and is too flat in frequency (Zipf -0.3692 vs VMS [-0.9656, -0.8036]). MECHANISM MAP CAVEATS: knocking out morphology collapses ΔI (0.0002) HARDER than knocking out the block wrapper (0.0054) , so morphology is CO-necessary for ΔI (not a clean one-ingredient-per-property map); and the context-free→weak-syntax link is TAUTOLOGICAL (the syntactic switch injects exactly what wc_z measures), so it is not counted. NET FINDING (informative negative): the minimal context-free positional/template grammar is INSUFFICIENT for the full VMS signature — it captures entropy and injected block-ΔI but undershoots the VMS's weak-positive word-class structure and overshoots its lexical productivity and morphological connectivity, which CONSTRAINS the class toward heavier word reuse, a smaller effective lexicon, and mild positive sequential structure. E22 (a-priori grid + VMS-actual bands incl. positive wc_z + real-language-wrapper control) is required before any class claim. FULL h2=2.139 ΔI=0.0809@400 fc_z=-2.24 wc_z=-1.02 ED1=0.9981 TTR=0.594 zipf=-0.3692; -morph h2=4.8429 ΔI=0.0002; -pos ΔI=0.0054; +syn wc_z=6.2. (Statistical; no identification — L7.)
