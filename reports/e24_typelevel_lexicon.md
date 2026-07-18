# E24 — Type-level small-lexicon generator

Generated 2026-07-15T23:45:42+00:00 at commit `d2e399e800` by `python -m ms408.experiments.e24_typelevel_lexicon`. Numbers in `results/experiments/e24_typelevel_lexicon.json`.

A-priori grid: 144 configs, ranges {'lex_size': [500, 1500, 3000, 6000], 'branching': [5, 6, 7], 'word_zipf': [0.8, 1.0, 1.2], 'boost': [2.0, 4.0, 8.0, 16.0], 'block_len': 400, 'note': 'a-priori sweep, not a fitted point'}.

## Basin

- ≥6/8 axes incl. VMS positive wc_z: **0%** (0 configs)
- configs with whole frequency group {ED1,TTR,Zipf}: 0
- with that AND {h2,ΔI,wc_z}: **0**
- axes never matched anywhere: **none**

Best config: lex 3000, branching 5, word-Zipf 0.8, boost 16.0 -> 4/8 (vms_syntax=True).

## Verdict [C, refutation pass pending]

TYPE-LEVEL CONCENTRATION SCORES A REAL WIN BUT DOES NOT CLOSE THE FULL SIGNATURE (within the swept family). THE WIN: it resolves the E23 entropy-vs-reuse tension — lexical reuse (TTR) now sits in-band JOINTLY with character entropy (h2) [ttr∧h2 co-occur = True], which token-copying could never do (there, concentrating TTR always deflated h2). THE RESIDUAL: no config reaches ≥6/8; the axes remain coupled, with the obstruction now centred on MORPHOLOGY CONNECTIVITY — matching the VMS's ED1 (≈0.75) forces a lexicon/branching regime incompatible in-band with h2, TTR, Zipf and the (soft) wc_z — and on a block-contrast trade-off (retained ΔI wants weak block contrast; a positive wc_z wants strong contrast). NET across i07–i08 (E21–E24): none of the tested generative families — context-free positional, +token-reuse, +type-level small lexicon — reproduces the VMS's full 8-axis signature over the swept ranges; the summary statistics are mutually coupled in a way these mechanisms do not capture. This CONSTRAINS the class (a strong result) without claiming impossibility for all generative processes. A-priori grid of 144 (lex_size [500, 1500, 3000, 6000] × branching [5, 6, 7] × word-Zipf [0.8, 1.0, 1.2] × boost [2.0, 4.0, 8.0, 16.0]). CEILING achieved = 4/8 (not a near-miss of 6). Configs with the whole frequency group {ED1,TTR,Zipf}: 0; with that AND {h2,ΔI,wc_z}: 0. Best (lex 3000, branching 5, word-Zipf 0.8, boost 16.0) 4/8 [h2, type_token_ratio, fc_z, wc_z]: h2=2.187 ΔI=0.4435 ED1=0.8777 TTR=0.2274 Zipf=-0.7496 wc_z=2.0. Pairs that do NOT co-occur in-band within this swept family: [h2×ed1_main_component; mz_peak_value×wc_z; ed1_main_component×type_token_ratio; ed1_main_component×zipf_slope; ed1_main_component×wc_z; zipf_slope×wc_z]. CAVEATS (refutation): this is a COUPLING within the swept ranges, NOT a proof of impossibility; fc_z/wc_z are 2-point Currier-A/B ranges (not CIs) and wc_z is confounded with sectional drift (the E22 control reaches it with no reuse), so they are soft axes; single base seed, so tight-band (ED1 ≈0.03 wide) in/out calls are fragile. (L7.)
