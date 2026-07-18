# E29 — The Naibbe cipher against the i06 discriminators

Generated 2026-07-17T09:09:07+00:00 at commit `5dcdcc9118` by `python -m ms408.experiments.e29_naibbe_discriminators`. Numbers in `results/experiments/e29_naibbe_discriminators.json`. Source: Greshko, Cryptologia 2025; ciphertext github.com/greshko/naibbe-cipher (nathist = Pliny Natural History, respaced Latin). Consume-only (L19).

Full-text ΔI = **0.0035** @ 3476 (VMS band [0.0735, 0.2057]); ΔI collapsed: **True**; reproduces VMS joint signature: **False**.

| axis | Naibbe (median) | range | VMS band | in band |
|---|---|---|---|---|
| h2 | 2.0792 | [2.074, 2.0813] | [2.1133, 2.1999] | · |
| mz_peak_value | 0.0049 | [0.0016, 0.0083] | [0.0735, 0.2057] | · |
| ed1_main_component | 0.9116 | [0.9013, 0.9158] | [0.7393, 0.766] | · |
| type_token_ratio | 0.2998 | [0.298, 0.3042] | [0.1634, 0.2961] | · |
| zipf_slope | -0.8918 | [-0.8966, -0.8873] | [-0.9656, -0.8036] | ✓ |
| mean_word_length | 5.226 | [5.223, 5.252] | [4.917, 5.127] | · |
| fc_z | -0.39 | [-2.01, 0.79] | [-4.71, -1.24] | · |
| wc_z | -0.64 | [-1.65, 1.39] | [1.9, 2.64] | · |

## Verdict [C]

THE NAIBBE ΔI TEST IS UNINFORMATIVE — i06 is NOT confirmed, and the analysis EXPOSES A CONFOUND IN i06's ΔI LEG (refutation-corrected from a first-pass 'CONFIRMED [B]'). First-pass reasoning: Naibbe's ΔI collapses to 0.0049 (full-text 0.0035) vs the VMS band [0.0735, 0.2057], so 'no cipher reproduces retained ΔI' looked confirmed. Two controls kill that reading. (1) DECOMPOSITION across Greshko's pipeline: word-boundary Latin (Pliny) ΔI=0.0758 is IN the VMS band (True); the RESPACING into non-word fragments drops it to 0.0176 — i.e. ~0.821 of the total ΔI loss happens BEFORE the cipher runs — and the homophonic encryption only accounts for the small remainder. The collapse is dominated by a SPACING CONVENTION, not by ciphering. (2) HOMOPHONY SWEEP with word order AND boundaries FIXED: ΔI falls monotonically with homophones/type anyway (H=1 0.0758 in-band → H=32 0.0049 below floor), so ΔI is a homophony / type-token-coupling detector, NOT a clean word-order measure. CONSEQUENCES: (a) faulting Naibbe for low ΔI is circular — real Latin with word boundaries is already IN the VMS band, and Greshko's respacing (not the cipher) removes it; (b) the VMS's own retained ΔI is BLOCK/section structure (our i06/E1/E2), so comparing it to Naibbe's token-level ΔI on an unsectioned stream is not like-for-like; (c) a LOW-homophony or word-boundary-preserving cipher of real prose would sit in the VMS ΔI band. NET: i06's ΔI leg does NOT robustly separate the VMS from ciphers of real prose — the exclusion leans more heavily on the SOFT fc_z/wc_z measures than i06/paper v3–v5b state, and must be walked back accordingly. On our battery Naibbe still matches only 1/8 tight bands, but that is a different, weaker claim than 'i06 confirmed'. REQUIRED FOLLOW-UP before any external engagement: encrypt word-boundary Latin (order-preserving) and re-test; measure the glyph-level properties Greshko actually claims. Naibbe ciphertext (Greshko 2025, 34764 tokens of respaced-Latin Pliny), 5×10000-token blocks, vs the VMS bands. Signature: h2 2.0792 (VMS [2.1133, 2.1999]), ΔI 0.0049 (full-text 0.0035@3476; VMS [0.0735, 0.2057]), ED1 0.9116 (VMS [0.7393, 0.766]), Zipf -0.8918 (VMS [-0.9656, -0.8036]), TTR 0.2998, len 5.226, fc_z -0.39, wc_z -0.64 (VMS wc_z [1.9, 2.64]). 1/8 axes in the VMS band. (Statistical; no decipherment — L7.)
