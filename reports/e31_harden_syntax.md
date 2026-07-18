# E31 — Hardened syntax discriminators (deconfounded + CI'd)

Generated 2026-07-17T09:38:11+00:00 at commit `8e89c50506` by `python -m ms408.experiments.e31_harden_syntax`. Numbers in `results/experiments/e31_harden_syntax.json`.

Global null = order-shuffle (confounded with topic drift); local null = within-250-word-block shuffle (preserves topic, destroys adjacency → grammar only).

| corpus | wc global | wc **local** | fc global | fc **local** |
|---|---|---|---|---|
| VMS | 1.98 | **1.97** | -1.19 | **-1.54** |
| cipher_order_preserving | 15.04 | **15.72** | 19.48 | **13.92** |
| cipher_verbose_homophonic | 2.21 | **3.74** | -2.71 | **-3.0** |

VMS 90% subsample CI (no replacement): wc_local [-1.44, 1.94], fc_local [-3.72, 0.1].
Stability SD (VMS): wc_local ±0.94, fc_local ±0.19.
VMS wc topic-drift share (global−local): 0.01.

## Verdict [B]

HARDENING FIRMS THE ROBUST LEG and confirms the homophonic class stays open. Once the null is deconfounded and the measures' true (small) seed-noise is used instead of an invalid resampling CI, the order-preserving cipher is separable from the VMS by a LARGE margin (fc_local 6.8σ, wc_local 8.0σ) — so word-order-preserving ciphers are robustly EXCLUDED, and the exclusion does NOT depend on the 2-point band or on topic drift (the VMS's weak wc_z survives deconfounding). The verbose+homophonic (Naibbe-class) cipher, by contrast, sits in the VMS's own weak-syntax regime (fc_local -3.0 vs VMS -1.54; wc_local 3.74 vs 1.97) and is NOT jointly separable, so it remains NOT excludable — the VMS-as-homophonic-cipher hypothesis (Naibbe) stays viable. NET: the E30 partition survives hardened, deconfounded measures. Deconfounded (within-block null, grammar only) vs confounded (global-shuffle) z. VMS wc: global 1.98 → local 1.97 (topic-drift share 0.01 ≈ 0 → the VMS's weak wc_z is REAL grammar, NOT sectional drift). Measures are STABLE to seed noise (SD: VMS fc_local ±0.19, wc_local ±0.94). Separability (gap / combined SD): order-preserving fc_local 6.8σ, wc_local 8.0σ; verbose+homophonic fc_local 2.1σ, wc_local 1.2σ. (Block-bootstrap WITH replacement was found INVALID here — duplicate blocks inflate these measures — so CIs use subsampling without replacement + the seed-SD.) (Statistical — L7.)
