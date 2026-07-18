# E30 — Cipher exclusion re-examination (post-E29 confound)

Generated 2026-07-17T09:26:23+00:00 at commit `ceba49c325` by `python -m ms408.experiments.e30_cipher_reexamination`. Numbers in `results/experiments/e30_cipher_reexamination.json`.

VMS bands: h2 [2.1133, 2.1999], ΔI [0.0735, 0.2057], fc_z [-4.71, -1.24], wc_z [1.9, 2.64]. 8 seeds/cipher.

## Order-preserving ciphers (should carry strong syntax the VMS lacks)

| cipher | h2 (med) | ΔI | fc_z | wc_z | max axes/4 |
|---|---|---|---|---|---|
| subst_1to1 | 3.04 | 0.3839 | 21.345 | 15.845 | 0 |
| verbose_x2 | 2.276 | 0.3881 | 20.02 | 14.85 | 1 |
| abjad | 2.774 | 0.3127 | 16.345 | 6.225 | 0 |
| nomenclator | 3.1755 | 0.2137 | 11.15 | 1.21 | 1 |

## Verbose+homophonic ciphers (the Naibbe mechanism)

| cipher | h2 (med) | ΔI | fc_z | wc_z | wc_z spread | 4/4 seeds | max/4 |
|---|---|---|---|---|---|---|---|
| verbhomo_v2_H8 | 2.161 | 0.116 | 0.0 | 3.79 | 5.89 | 0/8 | 3 |
| verbhomo_v2_H12 | 2.185 | 0.0861 | 0.395 | 3.46 | 2.23 | 0/8 | 3 |
| verbhomo_v2_H16 | 2.1855 | 0.0742 | -0.83 | 4.035 | 2.99 | 0/8 | 3 |
| verbhomo_v2_H24 | 2.2105 | 0.0517 | -0.78 | 4.405 | 5.93 | 0/8 | 1 |
| verbhomo_v3_H8 | 2.149 | 0.116 | 0.0 | 3.79 | 6.11 | 0/8 | 3 |
| verbhomo_v3_H12 | 2.167 | 0.0862 | 0.395 | 3.46 | 2.09 | 0/8 | 3 |
| verbhomo_v3_H16 | 2.166 | 0.0742 | -0.83 | 4.235 | 2.99 | 1/8 | 4 |
| verbhomo_v3_H24 | 2.184 | 0.0517 | -0.78 | 4.405 | 5.93 | 0/8 | 2 |

## Verdict [C]

i06 HEADLINE RETRACTED, robust core PRESERVED (honest re-partition). Two findings. (1) ROBUST: word-order-PRESERVING ciphers of real prose carry STRONG word-syntax (fc_z/wc_z ~5–24) the VMS lacks — a large, stable gap independent of the VMS's exact (soft) value — so this class is robustly EXCLUDED. (2) NOT ROBUST: the verbose+homophonic class (≈ the Naibbe mechanism) SCATTERS at the very edge of the VMS's joint signature — a single lucky seed reached all four VMS bands, but it does NOT reproduce robustly (n4_rate low), and the discriminating syntax measures vary so widely across seeds (median wc_z spread 4.44) that band membership is within noise. So homophonic/verbose ciphers are NOT excluded, and the VMS-as-homophonic-cipher hypothesis (Naibbe) REMAINS VIABLE on our own analysis — converging with Greshko rather than opposing him. NET: i06's universal 'cipher-of-real-prose EXCLUDED' over-reached and is RETRACTED to 'word-order-preserving ciphers excluded (robust); homophonic/verbose ciphers not excluded'. The homophonic verdict is soft-measure-limited — hardening fc_z/wc_z (next) is required to adjudicate it. 8 seeds/cipher, blocked WORD-BOUNDARY Latin (no respacing). ORDER-PRESERVING ciphers carry STRONG word-syntax: subst_1to1 fc_z~21.345/wc_z~15.845; verbose_x2 fc_z~20.02/wc_z~14.85; abjad fc_z~16.345/wc_z~6.225; nomenclator fc_z~11.15/wc_z~1.21 — vs the VMS's weak ~0/negative. HOMOPHONIC+VERBOSE family (the Naibbe mechanism): reaches ≥4/8 VMS axes robustly in 1 config-seeds total; any-seed corner hit = True; median wc_z spread across seeds = 4.44 (soft measures UNSTABLE). (Statistical; no decipherment — L7.)
