# T2.4 Study Report — Encoding-Hypothesis Bracket (W2)

Generated 2026-07-06T06:32:54+00:00 at commit `0e07c0b6fe` by `python -m ms408.studies.encoding`; full numbers in `results/studies/encoding_bracket.json`.

Five encoding families as generative models, scored against the real manuscript on 34,111 tokens each. one parameterization per family; T1.4 variants pending. Metrics substitution-invariant except residual alphabet-inventory dependence in h1/h2.

| corpus | h1 | h2 | mean len | TTR | zipf | abbrev ρ | ED1 comp. | pos. entropy | repeat | MZ peak | MZ scale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| vms | 3.879 | 2.129 | 5.10 | 0.218 | -1.103 | -0.347 | 0.797 | 0.667 | 0.0081 | 0.307 | 812 |
| verbose_cipher | 3.884 | 2.086 | 5.25 | 0.164 | -0.932 | -0.194 | 0.944 | 0.616 | 0.0016 | 0.000 | 1364 |
| selfcitation | 3.785 | 1.995 | 4.77 | 0.128 | -1.101 | -0.341 | 0.911 | 0.670 | 0.0093 | 0.497 | 275 |
| abjad_anagram | 4.129 | 2.867 | 3.97 | 0.212 | -0.919 | -0.340 | 0.924 | 0.680 | 0.0016 | 0.447 | 947 |
| abbreviation | 4.000 | 3.502 | 4.00 | 0.205 | -0.931 | -0.391 | 0.493 | 0.906 | 0.0003 | 0.256 | 1364 |
| conlang_relex | 3.849 | 2.818 | 7.08 | 0.205 | -0.963 | -0.083 | 0.001 | 0.934 | 0.0003 | 0.356 | 812 |

## Compatibility ordering (mean |z − z_VMS| across all metrics)

1. **selfcitation** — distance 0.628 (largest deviations: type_token_ratio, mz_peak_scale, mz_peak_value)
2. **abjad_anagram** — distance 0.886 (largest deviations: zipf_slope, h1, repetition_rate)
3. **verbose_cipher** — distance 0.954 (largest deviations: zipf_slope, mz_peak_value, repetition_rate)
4. **abbreviation** — distance 1.19 (largest deviations: h2, zipf_slope, repetition_rate)
5. **conlang_relex** — distance 1.237 (largest deviations: abbreviation_rho, ed1_main_component, position_entropy)

## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 review — L10)

1. **[C, candidate B pending T3.3]** No family reproduces the VMS's signature combination: gibberish-like character structure (h2 2.13, ED1 component 0.80) TOGETHER WITH genuine word-order information at natural-language scale (ΔI 0.307 bits/word peaking at 812 words). Compatibility ordering: selfcitation > abjad_anagram > verbose_cipher > abbreviation > conlang_relex.
2. **[C, candidate B pending T3.3]** The homophonic verbose cipher (Naibbe, as published) matches character structure almost perfectly (h2 2.09) but ERASES word-order information (ΔI 0.000 vs VMS 0.307): random homophone draws decouple ciphertext types from plaintext types. The VMS's intact topic-scale information is evidence AGAINST homophone-heavy verbose cipher as parameterized — a homophone-poor variant is the key T1.4 sweep.
3. **[C, candidate B pending T3.3]** Self-citation is closest overall (distance 0.628) but OVERSHOOTS word-order information at the wrong scale (ΔI 0.497 peaking at 275 words vs VMS 0.307 at 812) and runs a too-small vocabulary (TTR 0.128 vs 0.218): page-local copying produces stronger, shorter-range clustering than the VMS actually shows.
4. **[C]** Decisive single-metric exclusions under these parameterizations: abbreviation raises h2 to 3.50 (wrong direction, echoing Lindemann-Bowern's diplomatic-text finding); anagrammed abjad lands at h2 2.87; the non-paradigmatic conlang has no morphological network at all (ED1 0.001 vs VMS 0.797). Per-family worst metrics: selfcitation: type_token_ratio, mz_peak_scale; abjad_anagram: zipf_slope, h1; verbose_cipher: zipf_slope, mz_peak_value; abbreviation: h2, zipf_slope; conlang_relex: abbreviation_rho, ed1_main_component.
5. **[D]** Family parameterizations are single points in their design spaces: a homophone-poor verbose cipher, a templatic/paradigmatic conlang (closer to the real Lingua Ignota), and mixed abbreviation intensities are the obvious sweeps for the T1.4 variant matrix before this bracket is treated as settled.
