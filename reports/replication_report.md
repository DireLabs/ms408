# T1.1 Replication Report — Gate G1

Generated 2026-07-06T00:45:40+00:00 at commit `d720081f5c` by `python -m ms408.replication` (deterministic; full measurements in `results/replication/replication.json`).

**32 PASS · 3 CHECK · 3 informational** across entropy, Zipf/lexical, Currier A/B, glyph-sequence, positional, adjacency, and Montemurro-Zanette families.

Tolerance bands are PROPOSED (D17) and await Tim's ratification; CHECK rows are discussed below the table, not silently widened. Published targets were measured on the Takahashi/LSI or Stolfi interlinear transliterations; our primary corpus is ZL3b (L11) with IT (Takahashi IVTFF) as the like-for-like entropy corpus. Sources: specs/T11-*.md.

| id | family | description | published | measured | band | status |
|---|---|---|---|---|---|---|
| E-full | entropy | h2 Voynich full (Takahashi, labels incl.) | 2.1593 | 2.1637 | ±0.05 | **PASS** |
| E-A | entropy | h2 Voynich A (Takahashi, labels incl.) | 2.1705 | 2.1924 | ±0.05 | **PASS** |
| E-B | entropy | h2 Voynich B (Takahashi, labels incl.) | 2.0147 | 2.0197 | ±0.05 | **PASS** |
| E-h1 | entropy | h1 full Voynich (Takahashi) | 3.8828 | 3.8743 | ±0.05 | **PASS** |
| E-full-zl | entropy | h2 Voynich full on ZL (our primary) | (informational) | 2.1643 | — | **INFO** |
| E-A-zl | entropy | h2 Voynich A on ZL (our primary) | (informational) | 2.2023 | — | **INFO** |
| E-B-zl | entropy | h2 Voynich B on ZL (our primary) | (informational) | 2.0248 | — | **INFO** |
| E-hand1 | entropy | h2 Hand 1 (App. A, v2-plume values) | 2.122 | 2.1866 | ±0.08 (plume delta) | **PASS** |
| E-hand2 | entropy | h2 Hand 2 (App. A, v2-plume values) | 1.921 | 1.9764 | ±0.08 (plume delta) | **PASS** |
| E-hand3 | entropy | h2 Hand 3 (App. A, v2-plume values) | 1.999 | 2.0291 | ±0.08 (plume delta) | **PASS** |
| E-hand4 | entropy | h2 Hand 4 (App. A, v2-plume values) | 2.279 | 2.2919 | ±0.08 (plume delta) | **PASS** |
| E-hand5 | entropy | h2 Hand 5 (App. A, v2-plume values) | 2.111 | 2.1907 | ±0.08 (plume delta) | **PASS** |
| Z-daiin-A | zipf | top word of A: daiin share of A tokens | 0.045 | 0.0416 | ±0.01 | **PASS** |
| Z-chedy-B | zipf | top word of B: chedy share of B tokens | 0.021 | 0.0207 | ±0.007 | **PASS** |
| Z-top10-A | zipf | top-10 words coverage, A | 0.157 | 0.1488 | ±0.03 | **PASS** |
| Z-top10-B | zipf | top-10 words coverage, B | 0.145 | 0.1439 | ±0.03 | **PASS** |
| AB-chedy0 | currier | chedy occurrences in A (published: 'does not occur') | 0 | 1 | ≤3 | **PASS** |
| AB-daiin-herbalA | currier | inverse frequency of daiin, herbalA (targets 19/38/50-60) | 19 | 21.7 | 15-25 | **PASS** |
| AB-daiin-herbalB | currier | inverse frequency of daiin, herbalB (targets 19/38/50-60) | 38 | 50.9 | 28-50 | **CHECK** |
| AB-daiin-bioB | currier | inverse frequency of daiin, bioB (targets 19/38/50-60) | 50-60 | 78.8 | 40-75 | **CHECK** |
| AB-rep-A | currier | consecutive word repetition rate, A | 0.0084 | 0.008 | ±0.005 | **PASS** |
| AB-rep-B | currier | consecutive word repetition rate, B | 0.0094 | 0.008 | ±0.005 | **PASS** |
| G-e-tk | glyph | P(e | after t/k) — Currier: 'about half' | 0.5 | 0.3673 | 0.35-0.65 | **PASS** |
| G-e-pf | glyph | P(e | after p/f) — Currier: 'never, ever' | 0.0 | 0.0033 | ≤0.02 | **PASS** |
| G-q-o | glyph | q followed by o | 0.98 | 0.9762 | ≥0.95 | **PASS** |
| G-yfinal | glyph | words ending in y (LB: 41%) | 0.41 | 0.4033 | ±0.05 | **PASS** |
| G-final6 | glyph | words ending y/n/l/r/m/s (LB: 93%) | 0.93 | 0.9304 | ±0.04 | **PASS** |
| P-pf-par | positional | share of p/f occurrences in paragraph-initial lines (Currier: 90-95%) | 0.90-0.95 | 0.8317 | 0.75-0.97 | **PASS** |
| P-par-gallows | positional | paragraphs beginning with gallows t/k/p/f (BL: 85%) | 0.85 | 0.827 | ±0.10 | **PASS** |
| P-benched0 | positional | paragraph-initial words starting benched gallows (published: 'never'; operationalized ≤1% of paragraphs) | 0 | 0.0068 | ≤0.01 | **PASS** |
| P-m-final | positional | share of m occurrences at line end (Currier: 85%) | 0.85 | 0.6756 | 0.60-0.95 | **PASS** |
| P-crossline | positional | word repeats crossing line breaks (Currier: 'not one'; operationalized ≥3x suppression vs within-line rate) | 0 (rate ~0 vs within 0.00904) | 6 (rate 0.00153) | rate ≤ within/3 | **PASS** |
| P-firstlen | positional | first word of line longer by ~1 char (Vogt) | 1.0 | 0.392 | 0.5-1.5 | **CHECK** |
| P-chsh | positional | line-initial ch/sh suppression (Currier: ~0.1x expected) | 0.1 | 0.327 | 0.05-0.35 | **PASS** |
| D-y-qo | adjacency | Bio-B: P(qo|after y-final) vs P(qo|after non-y) (Currier: ~4x) | 4.0 | 5.97 | 2.5-8.0 | **PASS** |
| MZ-scale | montemurro | peak scale of word-information (MZ: 807 words; languages 600-800) | 807 | 812 | 500-1100 | **PASS** |
| MZ-top10 | montemurro | top-10 informative words overlap with MZ Table 1 (j/i normalized) | 10/10 | 8/10 | ≥6 | **PASS** |
| MZ-value | montemurro | peak ΔI bits/word (MZ: between Latin ~0.2 and Chinese ~0.6, above English) | ~0.3-0.5 | 0.3072 | 0.2-0.65 | **PASS** |

## Montemurro-Zanette detail

- Corpus: 34,111 paragraph-text tokens, reordered into the MZ section order (folio map per spec; D18 preprocessing policy).
- Peak: ΔI = 0.3072 bits/word at 812 words/part (42 parts).
- Top-10 informative words at s≈807: shedy, qokain, qokeedy, qokedy, daiin, chedy, chor, ol, qokeey, qol.
- H4 anchors truncated to N (informational): {'latin_vulgate': 0.3564, 'italian_decameron': 0.1895} — MZ's Latin anchor (Augustine) peaked ≈0.2 bits/word.

## CHECK rows and near-misses, discussed

- **AB-daiin clusters**: the published inverse-frequency *gradient* (A < Herbal-B < Bio-B) reproduces exactly in direction; absolute values run 20-35% high, consistent with Zandbergen's clusters being specific page sets (token totals 7975/3335/6696) vs our $I x $L slices, and ZL-vs-GC counts.
- **P-firstlen**: direction robustly confirmed (+0.392 vs all words, +0.421 vs second word) but below Vogt's ~1 char; his corpus/definition may differ. For D17 review.
- **Verbatim-claim caveats**: Currier's 'not one' cross-line repeat is overstated on full ZL — 6 instances (f47v, f78v, f82r, f84r, f84r, f87r), still ~6x suppressed vs the within-line repeat rate. D'Imperio's 'benched gallows never paragraph-initial' has 5 exceptions in 731 paragraphs (f1r, f65v, f76v, f101r, f102r2). The single `chedy` in Language A sits at f89r1.7.
- **D-y-qo**: Currier's '4x' is read as the conditional contrast P(qo|after y-final)=0.3988 vs P(qo|after non-y)=0.0667; the naive vs-overall-baseline reading gives 1.63 because Bio-B is qo-saturated (~24% of tokens).

## Notes and deviations

- **Transliteration deltas are expected**: LB targets were computed on the LSI/Takahashi text with `*` uncertain glyphs retained; we drop uncertain words (<0.15% of text) and use IVTFF editions. Anything outside band is flagged CHECK and discussed, per flag-don't-resolve.
- **D17 (open)**: G1 pass tolerances proposed here need Tim's ratification.
- **D18 (open)**: MZ2013 does not specify uncertain-glyph/label handling; policy used: paragraph-text loci only, uncertain words dropped.

## G1 sign-off

- [ ] Tolerances ratified (D17)
- [ ] CHECK rows reviewed
- [ ] Gate G1 approved (Tim)
