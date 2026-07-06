# T1.1 Replication Targets — Character Entropy (Lindemann & Bowern)

**Purpose:** exact published numbers and method details our pipeline must reproduce to pass gate G1.

**Primary source (LB2021):** Lindemann, L. & Bowern, C. (2021). *Character Entropy in Modern and
Historical Texts: Comparison Metrics for an Undeciphered Manuscript.* arXiv:2010.14697v2
(18 May 2021; 53 pp.). All section/table/figure references below are to v2.
**Secondary source (BL2020):** Bowern, C. & Lindemann, L. *The Linguistics of the Voynich
Manuscript* (Annual Review of Linguistics 2021, 7:285–308), preprint at lingbuzz/005415 —
section references are to the lingbuzz preprint.
**Code/corpus:** github.com/chirila/Voynich-public (file `R code/Entropy_Functions.R`,
`Corpora/Voynich_texts_statistics.csv`). Method statements below verified against that code.

All claims in this document are Grade A (direct quotation of published values) unless marked
otherwise. Numbers were transcribed manually from the sources on 2026-07-05; PDFs archived in the
session scratchpad only (L19: do not commit third-party PDFs).

---

## 1. Method (what exactly to compute)

### 1.1 Entropy definitions (LB2021 §4, Appendix A; verified in `Entropy_Functions.R::sumentropy`)

All entropies in **bits (shannons)**, plug-in / maximum-likelihood estimates, **no smoothing**:

- **h0** (zero-order) = log2(character set size) — "maximum entropy given the num of characters".
- **h1 = H1** (first-order) = Shannon entropy of the unigram character distribution:
  `H1 = −Σ p(c) log2 p(c)`.
- **H2** (second-order absolute) = Shannon entropy of the **bigram** distribution:
  `H2 = −Σ p(c1c2) log2 p(c1c2)`.
- **h2** (conditional character entropy, the headline metric) = **H2 − H1**.
  BL2020 §2.3.2 eq. (1) gives the equivalent form `H(X|Y) = Σ_{i,j} P(x_i,y_j) log2 [P(y_j)/P(x_i,y_j)]`.

### 1.2 Treatment of spaces — INCLUDED

Word spaces are **included as a regular character** (rendered `#`). The R code default is
`remove.spaces = FALSE`, which does `gsub(' ', '#', s)` before counting; bigrams are counted over
the whole document string with `stringdist::qgrams(s, q=2)`, so bigrams **span word boundaries**
(word-final char + `#`, and `#` + word-initial char both count). Confirmed in-paper: "The first
ranked character for each language is a space" (Fig. 7 caption) and bigrams like `y#`, `d#`
(§4.6.1). Entropy is NOT computed within words only.

### 1.3 Text preparation (LB2021 §3.2.1, §3.3.2)

- Lowercase; punctuation removed.
- Characters with < 0.01% frequency removed (Wikipedia texts in Latin/Cyrillic/Greek/Arabic/Hebrew
  scripts; Latin-script historical texts). Non-Latin scripts filtered by Unicode range.
  Stated effect: negligible — filtered vs unfiltered English h2 = 3.403 vs 3.406 (0.08%, §4.3.1).
- Diplomatic historical texts keep special characters intact.

### 1.4 Voynich text source and variants (LB2021 §3.1)

- **Transliteration:** Takeshi Takahashi's transcription, extracted from the Landini–Stolfi
  Interlinear file (LSI), EVA encoding (§3.1.2). Only **credible word breaks** (periods in LSI)
  used as spaces; possible breaks (commas) ignored (fn. 12).
- **Uncertain glyphs:** ~250 unreadable glyphs kept as EVA asterisk `*`; 16 characters occur < 50
  times each; all told < 0.15% of text (§3.1.1).
- **Three transcription systems** (Fig. 4, Fig. 5):
  - **Full Maximal** = EVA including capitalized ligature variants (e.g. `cTh`) and rare
    characters, with one v2 change: plumes written as apostrophe (EVA `sh` → `c'h`; EVA
    standalone `s` remains `s`). Effect of the plume change on h2: −0.0 to −3.2% depending on
    sample (fn. 10). *(v1 Maximal = plain EVA; the repo CSV values match v1.)*
  - **Simplified Maximal** = Maximal with ligatures decapitalized and all rare characters (except
    `x`) replaced by `*`; 23 characters vs 45 (§3.1.1).
  - **Minimal** = EVA with Currier-style single-character substitutions for common glyph
    sequences (`ch`, `sh`, `cth`… `iin`, `ain`, …) plus two extra combinations from Zandbergen
    (`ee`, `qo`) (Fig. 4).
- **Subsets:** Full / Currier A / Currier B / Davis Hands 1–5, each with and without label text
  (16 documents; §3.1). Label text = text in labels and diagrams; "Text" variants are running
  paragraph text only.

### 1.5 Sample-size adequacy (LB2021 §4.2, Fig. 8)

English Wikipedia (199,564 words), 1,000 random windows per size: at 50 words mean h2 = 2.62,
range 2.0–2.9, sd = 0.12 (overall text h2 = 3.40); at 10,000 words mean = 3.35, range 3.22–3.42,
sd = 0.033 — "for documents of around 10,000 words we should therefore reasonably expect h2 to be
accurate to about one-tenth of a bit." Voynich A/B sd at 50 words: 0.13 / 0.15 (English 0.13);
at 5,000 words: 0.049 / 0.072 (English 0.048).

---

## 2. Voynich target values

### 2.1 Appendix A, table 1 — Maximal transcription, paragraphs vs labels (LB2021 App. A)

| Text | Char count | Char set | Word count | Word set | h2 |
|---|---|---|---|---|---|
| Full Voynich Text | 234,404 | 45 | 37,940 | 8,172 | **2.072** |
| — Paragraphs | 205,014 | 36 | 33,111 | 6,936 | 2.117 |
| — Labels | 29,389 | 36 | 4,829 | 2,283 | 2.309 |
| Voynich A | 68,612 | 36 | 11,415 | 3,460 | **2.122** |
| — Paragraphs | 66,477 | 33 | 11,081 | 3,281 | 2.101 |
| — Labels | 2,134 | 25 | 334 | 289 | 2.425 |
| Voynich B | 145,745 | 32 | 23,226 | 4,947 | **1.973** |
| — Paragraphs | 136,046 | 30 | 21,632 | 4,661 | 1.964 |
| — Labels | 9,698 | 26 | 1,594 | 778 | 2.044 |
| Hand 1 | 64,747 | 42 | 10,877 | 3,260 | 2.122 |
| — Paragraphs | 61,963 | 33 | 10,352 | 3,032 | 2.083 |
| — Labels | 2,783 | 31 | 525 | 365 | 2.572 |
| Hand 2 | 67,929 | 27 | 11,070 | 2,590 | 1.921 |
| — Paragraphs | 61,698 | 27 | 10,054 | 2,367 | 1.910 |
| — Labels | 6,230 | 21 | 1,016 | 531 | 1.975 |
| Hand 3 | 75,182 | 30 | 11,755 | 3,419 | 1.999 |
| — Paragraphs | 72,550 | 30 | 11,328 | 3,302 | 1.991 |
| — Labels | 2,631 | 22 | 427 | 294 | 2.086 |
| Hand 4 | 17,850 | 25 | 2,864 | 1,548 | 2.279 |
| — Paragraphs | 2,219 | 21 | 353 | 268 | 2.083 |
| — Labels | 15,630 | 25 | 2,511 | 1,399 | 2.284 |
| Hand 5 | 5,774 | 26 | 930 | 563 | 2.111 |
| — Paragraphs | 3,662 | 22 | 580 | 387 | 2.079 |
| — Labels | 2,111 | 26 | 350 | 255 | 2.055 |

Caveat (flagged, not resolved): the paper's top-level rows are labelled "…Text" yet include
labels (paragraph + label word counts sum to the total), and the "Full Voynich Text" h2 of 2.072
conflicts with the 2.114 in the second Appendix A table and §4.3.1. Treat 2.114 (table 2.2 below)
as the primary Full-Voynich Maximal target; report both in the replication report.

### 2.2 Appendix A, table 2 — char set size / h2 by transcription system (LB2021 App. A)

Format: character set size / h2 (bits).

| Text | Maximal | Maximal Simplified | Minimal |
|---|---|---|---|
| Full Voynich | 45 / **2.114** | 23 / **2.112** | 41 / **2.475** |
| Language A | 36 / **2.122** | 22 / 2.119 | 39 / 2.504 |
| Language B | 32 / **1.973** | 23 / 1.973 | 40 / 2.304 |
| Hand 1 | 42 / 2.122 | 23 / 2.117 | 40 / 2.506 |
| Hand 2 | 27 / 1.921 | 23 / 1.921 | 39 / 2.219 |
| Hand 3 | 30 / 1.999 | 23 / 1.999 | 39 / 2.338 |
| Hand 4 | 25 / 2.279 | 22 / 2.279 | 36 / 2.558 |
| Hand 5 | 26 / 2.111 | 23 / 2.112 | 31 / 2.319 |

### 2.3 h1 (unigram entropy) and summary ranges (LB2021 §4.1, §4.3)

- **H1 = 3.91 bits** (Maximal Voynich), **3.94 bits** (Minimal Voynich); alphabets in their
  corpora range 3.57–4.82 bits (§4.1). Character set size: Maximal 42, Minimal 45 per §4.1 prose
  (note: conflicts with Appendix A's 45/41 — flag in report).
- Across all Voynich subsets and transcriptions: char set 21–45; **h2 range 1.91–2.56 bits**
  (§4.3).
- Average Minimal Voynich h2 2.48 vs Maximal 2.11 (§4.4).

### 2.4 Repo-CSV values (v1 Maximal = plain EVA) — closest targets for a plain-EVA replication

From `Corpora/Voynich_texts_statistics.csv` (Grade B: repo artifact, predates the v2 plume
change; matches BL2020's h2 quotes of A=2.17, B=2.01):

| Text (Maximal = EVA, labels incl.) | words | h1 | h2 |
|---|---|---|---|
| Full Voynich | 37,940 | 3.8828 | **2.1593** |
| Voynich A | 11,415 | 3.8527 | **2.1705** |
| Voynich B | 23,226 | 3.8780 | **2.0147** |

If we replicate on unmodified EVA (our L11 primary), expect these values, not §2.2's.

---

## 3. Reference values for comparison languages

### 3.1 Wikipedia corpus (LB2021 Appendix B; ~200k words/sample, cleaned per §1.3)

Key anchor languages (h2 in bits, spaces included):

| Language | Script | Char set | h2 |
|---|---|---|---|
| English | Latin | 27 | **3.403** |
| Latin | Latin | 28 | **3.412** |
| Italian | Latin | 33 | **3.272** |
| German | Latin | 31 | **3.394** |
| French | Latin | 39 | 3.354 |
| Spanish | Latin | 33 | 3.291 |
| Occitan | Latin | 38 | 3.358 |
| Hebrew | Hebrew (abjad) | 28 | **3.664** |
| Arabic | Arabic (abjad) | 44 | 3.702 |
| Greek | Greek | 34 | 3.519 |
| Georgian | Georgian | 43 | 3.566 |
| Icelandic | Latin | 36 | 3.596 |
| Persian | Arabic | 42 | 3.651 |
| Turkish | Latin | 34 | 3.549 |
| Hawaiian | Latin | 31 | **2.765** |
| Venda | Latin | 30 | **2.792** |
| Tswana | Latin | 28 | 2.816 |
| Min Dong | Latin | 48 | 2.841 |
| Tahitian | Latin | 43 | 2.846 |
| Hakka | Latin | 44 | 2.857 |
| Sango | Latin | 38 | 2.862 |
| Chinese | logographic | 6,222 | 6.142 |

### 3.2 Stated natural-language ranges (LB2021)

- Whole Wikipedia corpus (311 samples): **h2 = 2.77–6.14**; no sample overlaps Voynichese (§4.4).
- Latin-script languages: h2 **2.8–3.8** (§4.4).
- Historical corpus: alphabets (Latin, Georgian) **3.0–3.5**; abjads (Hebrew, Arabic scripts)
  **3.5–4.0** (§4.5, Fig. 13).
- Closest non-Voynich texts overall = Hawaiian 2.77, Venda 2.79, Tswana 2.82, Min Dong 2.84,
  Tahitian 2.85, Hakka 2.86, Sango 2.86 (Fig. 10 caption) — vs Voynich Maximal ~1.97–2.12.

### 3.3 Historical corpus anchors (LB2021 Appendix C)

(Note: the Appendix C column headers appear mislabeled in the PDF; magnitudes indicate the columns
are word count / word types / char count / char set. h2 column is unambiguous.)

| Text | Language | h2 |
|---|---|---|
| Medical Casebooks (normalized / diplomatic) | English | 3.418 / 3.435 |
| Three Books of Occult Philosophy | English | 3.241 |
| Science of Cirurgie | English | 3.240 |
| Secretum Secretorum (Copland tr.) | English | 3.111 |
| Alphabet of Tales | English | 3.254 |
| Amiran-Darejaniani | Georgian | 3.420 |
| Mishneh Torah | Hebrew | 3.637 |
| Masoretic Tanakh, Bereshit (no niqqud / with niqqud) | Hebrew | **3.526 / 3.256** |
| Codex Wormianus (normalized / diplomatic) | Icelandic | 3.390 / 3.490 |
| La Rettorica | Italian | 3.141 |
| Necrologium Lundense (normalized / diplomatic) | Latin | 3.348 / 3.204 |
| De Ortu Et Tempo Antichristi | Latin | 3.252 |
| Historia Hierosylmitanae Expeditionis | Latin | 3.368 |
| De Magia | Latin | 3.315 |
| Secretum Secretorum (Philip of Tripoli) | Latin | **3.277** |
| Steganographia | Latin | 3.424 |
| Sindbad-Name | Persian | 3.871 |
| Picatrix | Spanish | 3.244 |

BL2020 §2.3.2 adds: abbreviated Latin Secreta Secretorum h2 ≈ 3.4 vs 3.2 plain-text version.

---

## 4. Robustness conclusions (with quantitative spreads)

1. **Transcription system.** Full vs Simplified Maximal: 0.08% h2 difference on Full Voynich
   (2.114 vs 2.112) despite 45→23 characters (§4.3.1) — rare-character handling is negligible.
   Maximal vs Minimal: appreciable (2.114 vs 2.475 Full) but "all transcriptions of Voynich are
   significantly lower than any other text in the corpora" (§4); Minimal average 2.48 still below
   the corpus minimum 2.77 (§4.4). v2 plume change: h2 falls 0.0–3.2% by sample (fn. 10).
2. **Scribe/hand.** Hand 1 ≈ Language A (2.122 = 2.122); Hands 2–3 ≈ B (1.921, 1.999 vs 1.973);
   Hands 4–5 slightly higher (2.279, 2.111) because they are label-heavy (§4.3, App. A). Variation
   between hands/transcriptions is of the same order as the Hebrew niqqud effect (0.25 bits) but
   "all the Voynich measurements are substantially lower than the historical samples" (§4.5.1).
3. **Dialect (Currier A/B).** B lower than A in every transcription (1.973 vs 2.122 Maximal).
   Cause: `-edy` word-final sequence is **86× more common in B** (~1 in 5 B words ends in it) and
   `qo-` word-initial is **~2× more common in B** (~1 in 5 B words); remove both sequences from
   both texts and A/B h2 agree "within about 1%" (§4.3.2). BL2020 §3.2 (older values): A h2 2.17
   vs B 2.01; after deleting the two affixes, 2.23 and 2.24.
4. **Not abjad/abbreviation artifacts.** Abjads have *higher* h2 than alphabets; adding niqqud
   vowels lowers Hebrew h2 by 0.25 bits (3.526→3.256); diplomatic (abbreviated) versions have
   *higher* h2 than normalized (§4.5.1). Monoalphabetic substitution leaves h2 unchanged; most
   polyalphabetic ciphers would raise it (§4.7 discussion).
5. **Bigram concentration** (secondary targets, §4.6.3): bigrams with conditional probability
   > 50% cover **3.3%** of English text (4 bigrams: qu 96%, y# 75%, ve 59%, d# 54%), **29.3%** of
   Simple Maximal Voynich (12 bigrams), **23.9%** of Minimal Voynich (23 bigrams).
   Word-final structure (Simple Maximal): **41% of words end in `y`; 93% end in y/n/l/r/m/s**
   (§4.6.2); `q` is followed by `o` 98% of the time (Fig. 4 caption).

---

## 5. Quantitative values from the survey preprint (BL2020, lingbuzz/005415)

### 5.1 Zipf rank–frequency

- **No slope value is published** in either paper. BL2020 §3.3 states both Voynich languages
  "follow a Zipfian distribution" (citing Landini 2001; Reddy & Knight 2011), with Figure 7
  showing rank–frequency of the top 100 words normalized to the top word (illustrative point
  quoted: Occitan word 2 = 43%, word 3 = 40% of word 1). Voynich B is an outlier because its top
  three words (chedy, ol, shedy) are near-equal in frequency; merging chedy/shedy ("Voynich B
  (Modified)") reduces the anomaly.
- Grade B (repo CSV `Voynich_texts_statistics.csv`, unpublished): Zipf fit `freq ∝ rank^beta`
  (nls on min-max-normalized frequencies; `zipf_fit` in Entropy_Functions.R): Full Voynich
  Maximal beta = **−0.634** (se 0.0015), top-100-only beta = **−0.604** (se 0.0117);
  Voynich A beta = **−0.780** / top-100 **−0.857**; Voynich B beta = **−0.598** / top-100
  **−0.526**. Use only as sanity anchors, not published targets.
- Published word-frequency targets (BL2020 §3.3): top word of A `daiin` = **4.5%** of A tokens;
  top word of B `chedy` = **2.1%** of B tokens; top-10 words cover **15.7%** (A) and **14.5%**
  (B) — "within the range" of the 101-language sample (Fig. 8).

### 5.2 Positional glyph effects (BL2020 §4.1)

- **Paragraph-initial:** "85% of the paragraphs in the text begin with one of t, k, f, p"
  (gallows). Gallows-initial words are otherwise rare; minimal pairs tchor/chor, pol/ol,
  tchedy/chedy; `daiin` is never paragraph-initial (fn. 10: only two possible `pdaiin`).
  Paragraph-initial words appearing elsewhere usually begin k/f rather than p/t. In B,
  paragraphs are more commonly marked by `p`.
- **Line-initial:** first word "somewhat more likely" to begin with `s-`, apparently only for
  words otherwise beginning `o-`/`a-` (aiin→saiin, ol→sol, or→sor). Top line-initial words:
  daiin, saiin, dain, sol, sor (Table 3).
- **Line-final:** `m` and `g` concentrate line-finally, plausibly variants of `-iin` and `-y`
  (dam/daiin, am/aiin; g/y, alg/aly, dairodg/dairody, arg/ary); `-iin`/`-y` still occur
  line-finally, "albeit somewhat less frequently" (no percentage given). Top line-final words:
  daiin, dy, dam, am, dal (Table 3).
- No further enrichment percentages are published; only the 85% figure is quantitative.

### 5.3 Currier A/B lexical differences (BL2020 §3.2–3.3, Table 2)

- Top-10 words, A: daiin 4.5, chol 2.5, chor 1.6, s 1.4, dy 1.1, shol 1.0, sho 0.9, chy 0.9,
  cthy 0.9, ol 0.9 (total 15.7%).
- Top-10 words, B: chedy 2.1, ol 1.8, shedy 1.8, aiin 1.5, daiin 1.4, qokeedy 1.3, qokain 1.2,
  qokedy 1.2, qokeey 1.1, chey 1.0 (total 14.5%). (All percentages of tokens in that language.)
- Affixes: `qo-` prefix ≈ **2×** and `-dy` suffix ≈ **3×** more common in B than A (§3.2).
  Labels tend to lack `qo-` (§3.2 fn. 9). LB2021 §4.3.2 sharpens: `-edy` 86× more common in B;
  `chedy` is the most common B word and "almost entirely absent from A".
- Consecutive word repetition (exact): **0.84%** of A words repeat, **0.94%** of B; corpus range
  0.02–4.8%, mean 0.63%; family means Germanic 0.37%, Romance 0.36%, Semitic 0.36%, Iranian
  0.25% (§4.2 fn. 11).
- §2.2: `ol`, `or` common in A, rare in B; `dy` the reverse. Scribe 1 writes A; Scribes 2–5
  write B (Davis 2020 correspondence, one exception f58r… stated as "with the exception of 58r"
  in LB2021 §2).

---

## 6. Replication protocol implied for T1.1

1. Parse LSI, Takahashi transcriber lines only; periods = word breaks; strip metadata/notes.
2. Build Full/A/B (minimum) documents, labels included and excluded; EVA as-is (v1 Maximal)
   first, then optionally the v2 plume variant and Simplified/Minimal mappings of Fig. 4.
3. Replace spaces with a space token; compute unigram and bigram distributions over the whole
   string (bigrams cross word boundaries); h1 = H1, h2 = H2 − H1, bits, no smoothing.
4. Pass criteria to propose to Tim: h2 within ±0.05 bits of the matching published targets
   (per §1.5 the authors' own accuracy claim at ~10k words is ±0.1 bit; our corpus should be
   deterministic vs theirs modulo LSI-version and parsing differences — investigate anything
   larger than ±0.02 on identical corpus versions). Tolerance choice is a G1 decision for Tim
   (D-item), not settled here.
