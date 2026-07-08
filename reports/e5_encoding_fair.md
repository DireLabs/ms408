# E5 — Fair Encoding Bracket

Generated 2026-07-08T05:23:32+00:00 at commit `9b49077cb1` by `python -m ms408.experiments.e5_encoding_fair`. Numbers in `results/experiments/e5_encoding_fair.json`.

Equal 6-point tuning budget per family; fit on 17,055 tokens, scored on a disjoint 17,056-token held-out half; 11 metrics collapsed into 6 de-collinearised clusters (one vote each); 150 block-bootstrap resamples for CIs.

## Held-out ranking (clustered distance to VMS; lower = closer)

| rank | family | tuned knob | held distance | 95% CI | P(closest) |
|---|---|---|---|---|---|
| 1 | conlang_relex | 1.0 | 0.6691 | [0.6513, 0.9937] | 0.1 |
| 2 | selfcitation | 2 | 0.7288 | [0.5193, 0.8285] | 0.707 |
| 3 | abbrev_of_agglut | 0.0 | 0.7721 | [0.6353, 0.9934] | 0.173 |
| 4 | abjad_anagram | 1.0 | 0.8591 | [0.7186, 1.1337] | 0.02 |
| 5 | abbreviation | 1.0 | 1.2217 | [1.0474, 2.0751] | 0.0 |
| 6 | cipher_of_conlang | 0.0 | 1.2595 | [1.1553, 1.9436] | 0.0 |
| 7 | verbose_cipher | 0.0 | 1.5274 | [1.3832, 2.3321] | 0.0 |

### Top empirical metric correlations (audit of the cluster grouping)

- `h2~mz_peak_scale` |r|=0.885
- `h2~zipf_slope` |r|=0.861
- `h1~h2` |r|=0.837
- `zipf_slope~repetition_rate` |r|=0.831
- `zipf_slope~mz_peak_scale` |r|=0.809
- `position_entropy~repetition_rate` |r|=0.802
- `ed1_main_component~repetition_rate` |r|=0.746
- `h1~mz_peak_scale` |r|=0.741

## Verdict [C, refutation pass applied]

i01 DOWNGRADE CONFIRMED: with equal tuning, held-out scoring, and de-collinearised metrics, no family is robustly distinguished (winner conlang_relex is not robust (P(closest)=0.1, CI [0.6513, 0.9937] vs runner-up selfcitation [0.5193, 0.8285])). Held-out ranking: conlang_relex < selfcitation < abbrev_of_agglut < abjad_anagram < abbreviation < cipher_of_conlang < verbose_cipher. That modal lead is an ARTIFACT of one doubly-counted metric: dropping repetition_rate alone (the axis selfcitation's copying mechanically inflates) collapses its P(closest) from 0.707 to 0.24, whereupon conlang_relex leads (0.473). So even the weak modal signal is single-metric-dependent and does not survive de-collinearisation. The encoding bracket is a DESCRIPTIVE compatibility ordering, not evidence for any one family — the i01 'conlang best fit' claim does not survive fair tuning and is withdrawn as a distinguishing result.
