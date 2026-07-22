# E33 — Block-scale like-for-like ΔI (the last untested ΔI leg)

Generated 2026-07-22T09:06:15+00:00 at `0854fb88a8` by `python -m ms408.experiments.e33_block_scale_di`; numbers in `results/experiments/e33_block_scale_di.json`.

Homophony model: fair in-alphabet verbose homophonic (no markers); replaces the marker-injecting _homoph that the refutation pass showed deflates h2 by ~0.34 bits.

**VMS:** h2 2.1822 (CI [2.162, 2.1972]), block ΔI 0.1619 (CI [0.1449, 0.1742]), mean word length 5.03. **Plaintext control** (blocked Latin, h=1): h2 3.2934, block ΔI 0.3676, mwl 5.25.

Verbose × homophony sweep (median over seeds); a config 'reaches the corner' if its median h2 is within tol AND its block ΔI is within the VMS CI:

| verb | homoph h | h2 | block ΔI | mwl | h2✓ | ΔI✓ | |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 3.019 | 0.3645 | 5.25 | · | · |  |
| 1 | 2 | 2.794 | 0.2538 | 6.25 | · | · |  |
| 1 | 3 | 2.875 | 0.2067 | 6.25 | · | · |  |
| 1 | 4 | 2.942 | 0.1787 | 6.25 | · | · |  |
| 1 | 5 | 2.995 | 0.1526 | 6.25 | · | ✓ |  |
| 1 | 6 | 3.035 | 0.1323 | 6.25 | · | · |  |
| 1 | 8 | 3.089 | 0.1191 | 6.25 | · | · |  |
| 1 | 10 | 3.132 | 0.0989 | 6.25 | · | · |  |
| 1 | 12 | 3.180 | 0.0862 | 6.25 | · | · |  |
| 1 | 16 | 3.242 | 0.0681 | 6.25 | · | · |  |
| 1 | 24 | 3.203 | 0.0523 | 7.25 | · | · |  |
| 1 | 32 | 3.277 | 0.0405 | 7.25 | · | · |  |
| 2 | 1 | 2.281 | 0.3687 | 10.49 | · | · |  |
| 2 | 2 | 2.268 | 0.2590 | 11.49 | · | · |  |
| 2 | 3 | 2.330 | 0.2087 | 11.49 | · | · |  |
| 2 | 4 | 2.363 | 0.1783 | 11.49 | · | · |  |
| 2 | 5 | 2.391 | 0.1549 | 11.49 | · | ✓ |  |
| 2 | 6 | 2.402 | 0.1346 | 11.49 | · | · |  |
| 2 | 8 | 2.444 | 0.1189 | 11.49 | · | · |  |
| 2 | 10 | 2.493 | 0.0996 | 11.49 | · | · |  |
| 2 | 12 | 2.518 | 0.0868 | 11.49 | · | · |  |
| 2 | 16 | 2.562 | 0.0686 | 11.49 | · | · |  |
| 2 | 24 | 2.650 | 0.0541 | 12.49 | · | · |  |
| 2 | 32 | 2.689 | 0.0412 | 12.49 | · | · |  |
| 3 | 1 | 2.159 | 0.3687 | 15.74 | ✓ | · |  |
| 3 | 2 | 2.172 | 0.2590 | 16.74 | ✓ | · |  |
| 3 | 3 | 2.228 | 0.2087 | 16.74 | ✓ | · |  |
| 3 | 4 | 2.271 | 0.1783 | 16.74 | · | · |  |
| 3 | 5 | 2.284 | 0.1549 | 16.74 | · | ✓ |  |
| 3 | 6 | 2.289 | 0.1346 | 16.74 | · | · |  |
| 3 | 8 | 2.329 | 0.1189 | 16.74 | · | · |  |
| 3 | 10 | 2.339 | 0.0996 | 16.74 | · | · |  |
| 3 | 12 | 2.374 | 0.0868 | 16.74 | · | · |  |
| 3 | 16 | 2.414 | 0.0686 | 16.74 | · | · |  |
| 3 | 24 | 2.513 | 0.0541 | 17.74 | · | · |  |
| 3 | 32 | 2.523 | 0.0412 | 17.74 | · | · |  |

Closest config: {'expansion': 3, 'h': 5, 'h2': 2.2843, 'block_di': 0.1549, 'mwl': 16.74, 'normalized_distance': 1.36}.

**Grade C.** BLOCK-SCALE, LIKE-FOR-LIKE ΔI WEAKLY SEPARATES verbose+homophonic ciphers. Under a FAIR in-alphabet homophony model, NO config in the (verbose × homophony) sweep reaches the VMS's (h2 2.1822, block ΔI 0.1619) corner: the closest sits at normalized distance 1.36 (matching the VMS's block ΔI forces character entropy h2 out of its window, and vice versa). This CORRECTS the first pass, which used a marker-injecting homophony that deflated h2 and produced a spurious corner hit; the refutation pass caught it (docs/refutations). Honest reading: at block scale, like-for-like, the (h2, block-ΔI) plane does NOT collapse — matching the manuscript's low character entropy AND its block-scale word-order information at once is not achieved by this cipher family. This does NOT by itself revive ΔI into a hard standalone discriminator (one soft axis, a single generative family tested, and the verbose cipher's mean word length 16.74 vs the VMS's 5.03 is a further mismatch), and the program-level cipher disposition still rests on the deconfounded mid-level syntax measures (E30/E31). But it retires the earlier 'ΔI leg is dead even at block scale' claim: it is not.
