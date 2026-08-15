# E25 — Decoupled-ED1 type-lexicon generator (multi-seed)

Generated 2026-08-14T07:02:24+00:00 at commit `351193cbfa` by `python -m ms408.experiments.e25_decoupled_ed1`. Numbers in `results/experiments/e25_decoupled_ed1.json`.

A-priori grid 48 × 6 seeds. Scoring: generator-side CI (min..max over K seeds) overlaps VMS bootstrap band.

## Does decoupling ED1 dissolve the i08 coupling?

- configs matching ALL 5 non-trivial hard axes: **0** (0%); ceiling 4/5
- ED1 in-band at 8 configs; ED1 co-occurs with: h2=NO, mz_peak_value=yes, type_token_ratio=yes, zipf_slope=yes
- coupling resolved by decoupling: **False**

Best config: isolate_frac 0.15, lex 2500, pool_size 8, word-Zipf 0.9, boost 4.0 -> 4/5.

## Verdict [C, refutation pass pending]

THE i08 COUPLING LARGELY DISSOLVES; ONLY A SHALLOW h2↔ED1 FRONTIER NEAR-MISS REMAINS — SO THE i08 'no generative family' HEADLINE IS DEFLATED (honest walk-back). Once ED1 is a real knob (character-space size, absent in E22–E24 where tiny pools saturated it near 1.0), ED1 CO-OCCURS (multi-seed CI-overlap) with block-ΔI, lexical reuse AND frequency slope — h2:NO, mz:yes, type:yes, zipf:yes — which the coupled slot-grammar families could not. What survives is a single, shallow, PRINCIPLED tension between character entropy and morphology connectivity: low h2 needs a small effective character space, which densifies the edit-graph and raises ED1; enlarging the space to lower ED1 raises h2. The (h2, ED1) frontier passes NEAR but not through the VMS point — with h2 held in-band the closest ED1 gets is 0.625 (VMS floor 0.74; gap ≈ 0.11), and with ED1 in-band h2 rises only to 2.037 (VMS floor 2.11); the closest balanced point is h2=2.2887/ED1=0.6967 (gaps 0.089/0.043). This is a ~0.05–0.11 near-miss on a shallow frontier, NOT the gross incompatibility E24 reported, and is plausibly crossable with word-length variance (indel connectivity decouples ED1 from the character space) or non-uniform pools — the named next test. NET: the VMS's hard-axis signature constrains the generative mechanism FAR LESS than i08 claimed; a positional-morphology + decoupled type-lexicon generator comes within ~0.05 of it on all five hard axes, with only the entropy–connectivity frontier unresolved. (Grade C: not a broad all-5 basin, but a decisive deflation of the i08 negative. Soft fc_z/wc_z not counted; single fixed word length; no identification — L7.) A-priori grid of 48 × 6 seeds (isolate_frac [0.15, 0.3] × lex [2500, 4000] × pool_size [8, 9, 10] × word-Zipf [0.9, 1.1] × boost [2.0, 4.0]), CI-overlap scoring on the 5 non-trivial hard axes ['h2', 'mz_peak_value', 'ed1_main_component', 'type_token_ratio', 'zipf_slope']. ED1 in-band at 8 configs; ED1 co-occurs (CI-overlap) with — h2:NO, mz:yes, type:yes, zipf:yes. Ceiling 4/5; configs hitting ALL 5: 0 (0%). Best (isolate_frac 0.15, lex 2500, pool_size 8, word-Zipf 0.9, boost 4.0) 4/5; medians h2=2.2174 ΔI=0.1834 ED1=0.8305 TTR=0.1893 Zipf=-0.8521.
