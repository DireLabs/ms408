# Validation Harness Benchmark Report (T0.3)

Generated 2026-07-06T00:04:24+00:00 at commit `8f3bf763da` by `python -m ms408.benchmark` (deterministic; machine-readable version: `results/harness/benchmark.json`).

All numbers are direct measurements by versioned code on pinned inputs (L3). Comparative claims against *published* values are deferred to the T1.1 replication gate; the H2/H3 generator-fidelity evidence is in the module test suites and the spec §17 notes.

| corpus | class | tokens | types | mean len | h1 | h2 | zipf | abbrev ρ |
|---|---|---|---|---|---|---|---|---|
| h1_zl_eva | H1 | 37,954 | 8,465 | 5.09 | 3.869 | 2.125 | -1.0816 | -0.338 |
| h1_zl_eva_currierA | H1 | 10,974 | 3,588 | 5.04 | 3.839 | 2.170 | -1.0121 | -0.380 |
| h1_zl_eva_currierB | H1 | 23,724 | 5,161 | 5.13 | 3.866 | 1.958 | -1.1219 | -0.327 |
| h1_gc_v101 | H1 | 40,283 | 9,535 | 3.91 | 4.150 | 2.648 | -1.0438 | -0.308 |
| h2_naibbe_pliny_deck52 | H2 | 34,808 | 5,653 | 5.25 | 3.868 | 2.010 | -0.9336 | -0.194 |
| h2_naibbe_pliny_deck78 | H2 | 34,730 | 5,791 | 5.26 | 3.869 | 2.018 | -0.9279 | -0.194 |
| h2_naibbe_dante_deck52 | H2 | 535,635 | 8,997 | 5.21 | 3.866 | 2.021 | -0.944 | -0.194 |
| h2_naibbe_dante_deck78 | H2 | 536,289 | 9,043 | 5.23 | 3.868 | 2.032 | -0.9505 | -0.193 |
| h3_selfcitation_B_seed19 | H3 | 10,254 | 1,928 | 4.87 | 3.772 | 1.845 | -1.0709 | -0.324 |
| h3_selfcitation_B_seed7 | H3 | 10,214 | 2,127 | 4.88 | 3.780 | 1.927 | -0.9907 | -0.343 |
| h3_selfcitation_B_seed42 | H3 | 10,373 | 2,241 | 4.77 | 3.821 | 2.006 | -0.9414 | -0.349 |
| h3_selfcitation_B_seed101 | H3 | 10,410 | 2,261 | 4.77 | 3.790 | 1.963 | -1.001 | -0.304 |
| h3_selfcitation_B_seed555 | H3 | 10,591 | 1,849 | 4.66 | 3.801 | 1.875 | -1.145 | -0.312 |
| h3_author_reference | H3 | 10,832 | 2,228 | 4.70 | 3.788 | 1.912 | -0.9761 | -0.337 |
| h4_latin_vulgate | H4 | 534,301 | 42,089 | 5.36 | 3.990 | 3.232 | -0.9837 | -0.244 |
| h4_latin_macer_floridus | H4 | 13,967 | 3,897 | 5.85 | 4.066 | 3.150 | -0.8149 | -0.242 |
| h4_italian_decameron | H4 | 269,563 | 17,621 | 4.45 | 4.057 | 2.987 | -1.1004 | -0.319 |
| h4_german_ulmer_wundarznei_dipl | H4 | 21,789 | 4,067 | 4.01 | 4.692 | 3.224 | -1.118 | -0.273 |
| h4_german_ulmer_wundarznei_ascii | H4 | 20,528 | 3,363 | 4.31 | 4.272 | 2.983 | -1.1342 | -0.334 |
| h4_german_feldbuch_wundarznei_dipl | H4 | 21,788 | 4,392 | 4.34 | 4.466 | 3.113 | -1.0393 | -0.285 |
| h4_german_feldbuch_wundarznei_ascii | H4 | 20,626 | 3,651 | 4.63 | 4.226 | 2.974 | -1.0399 | -0.312 |
| h4_german_arzneibuch_dipl | H4 | 27,445 | 4,396 | 4.84 | 4.362 | 3.116 | -1.1037 | -0.282 |
| h4_german_arzneibuch_ascii | H4 | 26,900 | 3,878 | 4.93 | 4.210 | 3.074 | -1.1243 | -0.307 |
| h4_german_wundarznei_dipl | H4 | 26,374 | 3,517 | 4.21 | 4.411 | 2.857 | -1.1248 | -0.263 |
| h4_german_wundarznei_ascii | H4 | 25,538 | 3,184 | 4.28 | 4.275 | 2.860 | -1.124 | -0.287 |
| h4_german_kraeuterbuch_dipl | H4 | 21,932 | 4,515 | 4.38 | 4.530 | 3.175 | -1.0873 | -0.213 |
| h4_german_kraeuterbuch_ascii | H4 | 20,726 | 3,871 | 4.82 | 4.202 | 2.969 | -1.117 | -0.232 |
| h4_hebrew_mishneh_torah_consonantal | H4 | 90,379 | 16,412 | 3.94 | 4.291 | 3.908 | -0.9379 | -0.296 |
| h4_hebrew_mishneh_torah_pointed | H4 | 90,379 | 18,052 | 7.19 | 4.811 | 3.364 | -0.9402 | -0.271 |

## H3 multi-seed vs. author reference

| metric | ours (5-seed mean ± sd) | author (Java, seed 19) |
|---|---|---|
| tokens | 10368.4 ± 148.517 | 10832 |
| types | 2081.2 ± 185.303 | 2228 |
| mean_word_length | 4.7894 ± 0.0879 | 4.7047 |
| h1 | 3.7929 ± 0.0192 | 3.7883 |
| h2 | 1.9233 ± 0.0652 | 1.912 |
| zipf_slope | -1.0298 ± 0.0793 | -0.9761 |
| abbreviation_rho | -0.3264 ± 0.0193 | -0.3371 |

## Notes

- **Gate rule (RESEARCH-PLAN §3):** techniques claiming meaning-detection or structure-recovery must discriminate/recover correctly on H2/H3/H4 before their H1 results are admissible. This report establishes the corpus classes and their baseline statistics; discriminator scoring builds on it.
- H1 policy, entropy method, and Zipf fit range are recorded in the JSON `policies` block; change them only alongside a version bump of this report.
- H4 registers expose the edition confound (diplomatic vs. critical, consonantal vs. pointed) — compare like with like, per the `edition` tag.
