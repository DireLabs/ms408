# E27 — Symbol quantification

Generated 2026-07-17T03:26:27+00:00 at commit `2e7ffde072` by `python -m ms408.experiments.e27_symbol_quantification`. Numbers in `results/experiments/e27_symbol_quantification.json`.

| corpus | glyph types | eff. alphabet | glyphs@95% | mean len | pos. specialisation |
|---|---|---|---|---|---|
| VMS_paragraph | 37 | 14.95 | 15 | 5.101 | 0.742 |
| VMS_A | 38 | 14.89 | 14 | 5.055 | 0.732 |
| VMS_B | 35 | 14.72 | 15 | 5.162 | 0.76 |
| VMS_labels | 36 | 15.05 | 15 | 5.348 | 0.685 |
| ref_alphabet_latin | 23 | 15.85 | 17 | 5.362 | 0.393 |
| ref_numeral_base10 | 10 | 9.96 | 10 | 3.892 | 0.072 |
| ref_numeral_base16 | 16 | 15.96 | 15 | 3.937 | 0.05 |
| ref_syllabary | 16 | 14.95 | 15 | 4.565 | 0.506 |

*Positional specialisation* = mean total-variation distance among the initial / interior / final glyph distributions. ~0 ⇒ same symbol set at every position (a positional numeral); high ⇒ position-specific sets (templatic / syllabic).

## Verdict [D, descriptive]

DESCRIPTIVE (grade D; cannot support a register reading alone — L7 / the i09 lesson; E28 is the anchor). The VMS paragraph inventory: 37 glyph types but an EFFECTIVE alphabet of 14.95 (15 glyphs cover 95%) — a SMALL symbol set, between a base-10 numeral (9.96) and an alphabet (Latin 15.85). DECISIVE STRUCTURAL POINT — positional specialisation (mean TV among initial/interior/final glyph distributions): VMS 0.742 vs base-10 numeral 0.072 (near-0: the SAME digits at every place) vs syllabary 0.506 vs alphabet 0.393. The VMS is HIGHLY position-specialised, UNLIKE a positional numeral (which reuses its digit set across places) and most like a templatic/syllabic layout — consistent with the i09 positional-template picture. So a POSITIONAL-NUMERAL sub-type is shape-incompatible; a non-positional value scheme (tallies / per-symbol values / a table of labels) is not touched by this and remains for E28 to test. VMS_A vs VMS_B effective alphabet 14.89/14.72, specialisation 0.732/0.76; labels 15.05 eff-alpha. (No value/number claim — L7.)
