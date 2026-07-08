# E6 — Deterministic-verbose / nomenclator cipher reconstruction

Generated 2026-07-08T18:31:59+00:00 at commit `04c3d73fe1` by `python -m ms408.experiments.e6_cipher_reconstruction`. Numbers in `results/experiments/e6_cipher_reconstruction.json`.

VMS discriminator targets (block-bootstrap 95% CI):

| metric | VMS | 95% CI |
|---|---|---|
| h2 | 2.1294 | [2.0175, 2.175] |
| mz_peak_value | 0.3072 | [0.2193, 0.3035] |
| ed1_main_component | 0.7975 | [0.7769, 0.8168] |
| zipf_slope | -1.1032 | [-1.1252, -1.0182] |
| mz_peak_scale | 812 | — |

## Joint match by config (✓ = within VMS CI)

| config | h2 | ΔI | ED1 | Zipf | scale | n/4 |
|---|---|---|---|---|---|---|
| latin_x1_nomen0 | 3.1386✗ | 0.3555✗ | 0.2798✗ | -0.9656✗ | 812 | 0 |
| latin_x1_nomen400 | 3.2895✗ | 0.2545✓ | 0.2549✗ | -0.9963✗ | 947 | 1 |
| latin_x2_nomen0 | 2.3069✗ | 0.3564✗ | 0.0007✗ | -0.9627✗ | 812 | 0 |
| latin_x2_nomen400 | 2.7✗ | 0.2601✓ | 0.0296✗ | -1.0011✗ | 812 | 1 |
| latin_x3_nomen0 | 2.1839✗ | 0.3564✗ | 0.0003✗ | -0.9627✗ | 812 | 0 |
| latin_x3_nomen400 | 2.5641✗ | 0.265✓ | 0.0299✗ | -0.9927✗ | 812 | 1 |
| latin_abjad | 2.8129✗ | 0.2917✓ | 0.9029✗ | -1.0654✓ | 473 | 2 |
| latin_x1_nomen4000 | 3.2395✗ | 0.1738✗ | 0.1792✗ | -1.752✗ | 473 | 0 |
| conlang_p0.4_x1 | 2.6866✗ | 0.345✗ | 0.2944✗ | -0.9893✗ | 812 | 0 |
| conlang_p0.8_x1 | 2.5777✗ | 0.3091✗ | 0.6764✗ | -1.1435✗ | 473 | 0 |
| conlang_p1.0_x1 | 2.4733✗ | 0.2912✓ | 0.9169✗ | -1.2121✗ | 568 | 1 |
| conlang_p0.8_x2 | 1.9564✗ | 0.3259✗ | 0.0009✗ | -0.9971✗ | 812 | 0 |

## Verdict [C, refutation pass pending]

NOT reinstated as a cipher of natural language (best real-Latin config latin_abjad: 2/4, missed [h2, ed1_main_component]). Two-part result on the ED1 network (VMS 0.7975). (1) VERBOSE CIPHER EXCLUDED on the ED1 network — DEDUCTIVELY. A letter→k-glyph bijection turns every 1-letter plaintext difference into a ≥k-glyph difference, so edit-distance-1 adjacency cannot survive expansion: Latin ED1 0.28 at 1:1 → 0.001 verbose; conlang 0.917 → 0.001. This is a definitional exclusion of the deterministic-VERBOSE cipher E2 re-opened, not an empirical surprise. (2) 'NEEDS CONSTRUCTED MORPHOLOGY' — REFUTED. A length-reducing, INVENTORY-COLLAPSING cipher of REAL Latin (abjad: drop vowels → consonantal skeleton) reaches ED1 0.903 ≥ the VMS band lower 0.7769 — inflectional families collapse to shared short skeletons that ARE edit-distance-1 neighbours, so the dense network arises from mere type-inventory reduction of natural language, NOT only from constructed morphology. The abjad/abbreviation/syllabary class (cf. medieval vowel-dropping) is now a live positive lead for the ED1 network. CAVEAT: the abjad reaches ED1 partly BY SHORTENING words (shorter words have more ED1 neighbours — a known metric confound), so it trades the ED1 match for a word-length mismatch; no transform here matches ED1 AND word length AND h2 together, so this is a lead for a joint follow-up, not a reconstruction. CAVEAT: the ΔI target CI is mildly biased low (block bootstrap attenuates the 812-peak) and the conlang's ΔI match sits at the wrong scale, so ΔI legs are weak. Structural sufficiency NOT claimed; no plaintext claim (L7).
