# E26 — Word-length variance vs the h2↔ED1 frontier

Generated 2026-08-14T07:03:35+00:00 at commit `351193cbfa` by `python -m ms408.experiments.e26_length_variance`. Numbers in `results/experiments/e26_length_variance.json`.

A-priori grid 48 × 5 seeds. multi-seed generator-side CI (min..max over K seeds) vs VMS band; all 6 profile axes counted (word length now varies); fc_z/wc_z soft, not counted.

## Did length variance cross the h2↔ED1 frontier?

- configs matching ALL 6 hard axes: **0** (0%); ≥5/6: 0; ceiling 4/6
- ED1 reaches in-band (0.757) jointly with ΔI/TTR/Zipf; residual = h2 gap 0.034 (h2=2.2336) + length artifact (True)
- ED1 co-occurs with: h2=NO, mz_peak_value=yes, type_token_ratio=yes, zipf_slope=yes, mean_word_length=NO

Best config: alphabet 4, spread xwide, word-Zipf 1.0, boost 4.0, lex 3000 -> 4/6.

## Verdict [C, refutation pass pending]

RETRACTION OF THE i08 HARD CONSTRAINT — NOT a promotion to 'no constraint' (refutation-corrected). Word-length variance supplies the connectivity control fixed-length words lacked, so the E25 entropy↔connectivity tension is largely resolved and the i08 'gross multi-axis incompatibility' was largely a morphology-parameterisation artifact. NET across E25–E26: freeing connectivity collapses that incompatibility to a single shallow COUPLED entropy↔connectivity↔length frontier a flexible generator approaches within ~0.03–0.05 on 4/6 axes — but NO single config reproduces the full set (incomplete, NOT vacuous), and the last obstruction MOVED (ED1→h2/length) rather than vanished. So WITHIN this one generative family the hard axes under-determine the sub-mechanism; this is NOT a general non-discrimination claim — the same signature still EXCLUDES the cipher-of-real-prose class (i06). The load-bearing constraints stay i06 + the qualitative character/morphology structure, not a joint-signature barrier within the favoured class. (Grade C. Soft fc_z/wc_z not counted; no identification — L7.) A-priori grid 48 × 5 seeds (alphabet [4, 5] × spread ['mid', 'wide', 'xwide'] × word-Zipf [1.0, 1.2] × boost [2.0, 4.0]). Length variance brings ED1 into the VMS band at the best config (0.757) with block-ΔI/TTR/Zipf; the E25 sticking point (fixed length capped ED1@h2-in-band at 0.625) is largely gone. BUT no single config reaches all six (ceiling 4/6; 0 at ≥5/6): at that config the residual is TWO misses — h2 gap ~0.034 (h2=2.2336, band [2.1133, 2.1999]) AND mean length 6.376 vs band max ~5.13 (CONJECTURED short-word-saturation artifact, UNTESTED and possibly not separable — ED1-in-band configs are confined to the smallest alphabet + widest spread). CI-overlap scoring is lenient (seed min..max touches band) and was not applied to the i08 families, so the E24→E26 comparison is not apples-to-apples. Best config 4/6 [mz_peak_value, ed1_main_component, type_token_ratio, zipf_slope]: h2=2.2369 ΔI=0.2003 ED1=0.7298 TTR=0.1812 Zipf=-0.9098 len=6.11.
