# T1.1 Replication Targets — Currier A/B Differences & Positional Glyph Effects

**Purpose.** Canonical published/documented statistics that our pipeline must reproduce to pass the
T1.1 replication gate (G1). Every row pairs a source claim + verbatim quote with a concrete
quantitative test we can implement as a deterministic `src/` script writing to `results/`.

**Grade of the underlying claims:** these are *published baseline observations* we are trying to
**replicate**, not accept — treat as grade C targets (documented, some >45 yr old, transliteration
and corpus definitions vary). A target is "hit" only when our own code reproduces the direction
(and, where stated, roughly the magnitude) on our versioned dataset.

## Notation & source caveats

- Currier wrote in his own transliteration alphabet, not EVA. voynich.nu renders his glyphs with an
  EVA webfont; below, glyph slots are given in **EVA** (decoded from the page's PUA codepoints). Where
  a mapping is load-bearing note it explicitly. Currier `dy` = EVA `dy`; Currier gallows
  `t k p f` = EVA `t k p f`; Currier "ligatures" `cTh cKh cPh cFh` = EVA pedestalled/benched gallows
  `cth ckh cph cfh`; Currier `ch`/`Sh` = EVA `ch`/`sh`.
- **Corpus split matters.** "Language A" vs "Language B" is a per-page/per-section label. Our tests
  must stratify by the A/B (and cluster) assignment we adopt (see DECISIONS — dialect labeling is a
  stratification requirement, CLAUDE.md rule 7). Zandbergen's clusters: Herbal-A, Pharma-A, Herbal-B,
  Stars-B, Stars-Bio, Bio-B.
- Currier's stated sample sizes: Herbal A ≈ 6,500 words / ~1,000 lines / ~7 words per line; largest
  single sample ~15,000 words; ~25,000 words across three herbal+biological runs; Biological B ≈ 20
  pages.

## Sources

- **[S1]** Currier, P. (1976), *Papers on the Voynich Manuscript* (talk + Appendix A "Some Notes and
  Observations", Oct 1976), in *New Research on the Voynich Manuscript: Proceedings of a Seminar*, ed.
  M.E. D'Imperio. HTML transcription (Guy & Reeds 1992; HTML R. Zandbergen):
  https://www.voynich.nu/extra/curr_main.html
- **[S2]** Zandbergen, R., *Analysis — Character statistics* (voynich.nu §2, incl. Tiltman 1967,
  Currier 1976, D'Imperio 1978 observations, and §2.7 line/paragraph properties):
  https://www.voynich.nu/a2_char.html
- **[S3]** Zandbergen, R., *Currier A and B: two different languages?* (per-cluster frequent-word
  tables, absolute counts): https://www.voynich.nu/extra/lang.html
- **[S4]** Zandbergen, R., *Analysis — Word structure/paradigms* (Tiltman roots/suffixes; notes chedy
  as a B-only word): https://www.voynich.nu/a3_para.html
- **[S5]** Bowern, C. & Lindemann, L. (2020/21), *The Linguistics of the Voynich Manuscript*
  (quoted via S2): entropy/positional-restriction conclusion.

---

## A. Currier's A/B lexical & glyph differences

Currier, Appendix A ¶2, "The principal differences between the two languages in this Section [Herbal]
are" [S1]:

| # | Claim | Source | Verbatim quote | Suggested quantitative test |
|---|-------|--------|----------------|-----------------------------|
| A1 | Final `dy` very high in B, near-absent in A | S1 | "(a) Final [dy] is very high in Language B; almost non-existent in Language A." | `rate(word-final dy \| B pages) / rate(... \| A pages) >> 1`; expect A rate ≈ 0. Report per-cluster word-final-`dy` token rate. |
| A2 | `chol`, `chor` high in A (often repeated), low in B | S1 | "(b) The symbol groups [chol] and [chor] are very high in A and often occur repeated; low in B." | `rate(chol)+rate(chor)` per 1k tokens, A vs B; expect A >> B. Also test consecutive-repeat rate of chol/chor in A. |
| A3 | `chain`/`chaiin` rare in B, medium in A | S1 | "(c) The symbol groups [chain] and [chaiin] rarely occur in B; medium frequency in A." | Per-1k-token rate of `chain`,`chaiin`: A medium, B ≈ 0. |
| A4 | Initial `chot` high in A, rare in B | S1 | "(d) Initial [chot] high in A; rare in B." | `rate(word-initial chot \| A) / rate(\| B) >> 1`. |
| A5 | Initial `cth`(cTh) very high in A, very low in B | S1 | "(e) Initial [cTh] very high in A; very low in B." | `rate(word-initial cth \| A) >> rate(\| B)`. |
| A6 | Many "unattached finals" characteristic of B, not A | S1 | "(f) Unattached finals scattered throughout Language B texts in considerable profusion; generally much less noticeable in Language A." | Define unattached finals = standalone tokens in {n,in,iin,l,r,m,ir,...}; `rate(unattached-final tokens \| B) >> rate(\| A)`. |
| A7 | `chot` (initial group) example count | S1 | "[chot], for example, occurs only 5 times in Herbal B, but 212 times in Herbal A." | Direct count check: `chot`-initial tokens ≈ 212 in Herbal-A, ≈ 5 in Herbal-B (order-of-magnitude; corpus-dependent). |
| A8 | `p`/`f` never followed by `e`; `t`/`k` followed by `e` ~half the time | S1 | "The letters [t k] are followed anywhere in a word by our little friend [e] about half the time (say 750 out of a total of 1500) ... These two, [p f], are never, ever, anywhere in the manuscript, followed by [e]." | `P(next=e \| prev∈{t,k}) ≈ 0.5`; `P(next=e \| prev∈{p,f}) ≈ 0`. Whole-MS, not A/B-specific. |
| A9 | Pedestalled gallows (cTh/cKh/cPh/cFh) high initial in A, very low in B | S1 | "In Herbal A material, in fact in all A material, this series is initially high; in B, it is very low — another way of identifying the two languages." | `rate(word-initial cth/ckh/cph/cfh \| A) >> rate(\| B)`. |

### Modern re-quantification of A/B (Zandbergen, per-cluster counts) [S3]

voynich.nu tabulates most-frequent words per cluster with absolute counts (cluster token totals in
parentheses: Herbal-A 7975, Pharma-A 2234, Herbal-B 3335, Stars-B 5251, Stars-Bio 5483, Bio-B 6696).

| # | Claim | Source | Verbatim quote | Suggested quantitative test |
|---|-------|--------|----------------|-----------------------------|
| A10 | `chedy` is the single most frequent B word and does **not occur at all** in A | S3 (also S4) | "In the B corpus, the most frequent word is [chedy] ... A peculiar fact is that the latter word does not occur at all in the A corpus, whereas [daiin] is relatively frequent in B as well." / S4: "specifically B-language words, such as fourth-ranked [chedy]." | `count(chedy \| A pages) == 0` (or ≈0); `chedy` in top-2 of B by frequency. |
| A11 | `daiin` is top word everywhere but rarer in B (verbosity/normalization) | S3 | "The inverse frequency of daiin is: 19 for Herbal-A and Pharma-A, 38 for Herbal-B, 50, 54 and 60 for the other three B dialects." | `token_share(daiin)` ≈ 1/19 in A, ≈ 1/38 Herbal-B, ≈ 1/50–1/60 in Stars-B/Stars-Bio/Bio-B. |
| A12 | `-dy` ending: in B preceded by `e` (`edy`); in A preceded by `o` (`ody`) | S3 | "high-frequency ending -dy ([dy]) in B, almost always preceded by e ([e]). In A, this ending is often preceded by o ([ody])." | Among word-final `dy` tokens: `P(e before dy \| B) ≈ 1` vs elevated `P(o before dy \| A)`. |
| A13 | `qok-` / `qokeey` family dominates B (esp. Stars-Bio), scarce in A | S3 | Bio-B top list: "254 shedy, 214 chedy, 194 qokaiin ..."; Stars-Bio: "136 qokeey, 125 qokaiin ..." (A lists have no qok- words in top ranks) | `rate(word-initial qok- \| B) >> rate(\| A)`; `rate(qo- prefix \| B) > rate(\| A)`. |
| A14 | `shedy` top of Bio-B; `chedy`/`shedy` are the B signature | S3 | Bio-B counts: "254 shedy ... 214 chedy"; Herbal-B: "63 chedy ... 36 shedy" | `rate(chedy)+rate(shedy)` per 1k: near-0 in A, large in Bio-B/Herbal-B. |
| A15 | Shared words exist across A/B → not two different plaintext languages (verbose cipher not excluded) | S3 | "Some words are frequent in all clusters: daiin, chey, ol, or, saiin, which essentially excludes the possibility that the A and B languages are different plaintext languages. A verbose encryption of two different plaintext languages cannot be excluded, though." | Confirm {daiin, chey, ol, or, saiin} present with substantial frequency in every cluster. |

---

## B. Line-position effects ("the line is a functional entity")

Currier [S1], paraphrased/summarized by Zandbergen [S2 §2.7.1]. Three pillars: (1) line-edge glyph
frequencies differ from interior, (2) line-final "filler" glyphs, (3) no word-repeat crosses a line
break.

| # | Claim | Source | Verbatim quote | Suggested quantitative test |
|---|-------|--------|----------------|-----------------------------|
| B1 | Line-edge char frequencies differ markedly from interior | S1/S2 | "The frequency counts of the beginnings and endings of lines are markedly different from the counts of the same characters internally." | For each glyph, compare P(glyph \| line-initial word) and P(glyph \| line-final word) vs interior; chi-square / effect sizes; flag glyphs with large deviation. |
| B2 | Some chars essentially cannot begin a line; some ~1/100 of expected | S1 | "There are, for instance, some characters that may not occur initially in a line. There are others whose occurrence as the initial syllable of the first word of a line is about one hundredth of the expected." | Identify glyphs with `observed/expected ≈ 0.01` as first-word initial; expected = uniform-over-position baseline. |
| B3 | Words with `ch`/`sh` initial suppressed line-initially (~0.1× expected) | S1 | "words with initial [ch Sh] are unexpectedly low in line initial position (on average about .1 of expected)" | `rate(line-initial word starts ch/sh) / expected ≈ 0.1`. |
| B4 | Line-initial "replacements" look like modified ch-initial words (dch, ych, ...) | S1 | "other words occur in this position far more frequently than expected, particularly words with initial [dch], [ych] etc., which have the appearance of [ch]-initial words suitably modified for line-initial use." | Enrichment of line-initial tokens beginning `d`+gallows/`ch` or `y`+... vs interior. |
| B5 | One symbol occurs at line-end 85% of its occurrences (Zandbergen: almost certainly `m`) | S1/S2 | "There is, for instance, one symbol that, while it does occur elsewhere, occurs at the end of the last words of lines 85% of the time." (S2 note 18: "Currier almost certainly means [m]") | `P(token is line-final \| token contains/ends m) ≈ 0.85`; test candidate = `m`. |
| B6 | `ch`/`sh` word-initial suppressed line-initially except with intercalated `o` — A only | S1/S2 | "it is a very infrequent word initial at the beginning of a line, except when there is an intercalated [o]. This applies only to 'Language' A." | In A: line-initial `ch/sh`-words rare unless `cho-/sho-`; compute conditional rates; test A-specificity. |
| B7 | No repeated word-sequence crosses a line boundary (~25k words) | S1/S2 | "in all of that, which is almost 25,000 words, there is not one single case of a repeat going over the end of a line to the beginning of the next; not one." | Count adjacent identical (or repeated n-gram) word pairs straddling line breaks; expect ≈ 0 vs a within-line baseline of repeats. |
| B8 | `y` line-initial behaviour (Tiltman) | S2 | "[y] occurs quite frequently as the initial symbol of a line followed immediately by a combination of symbols which seem to be happy without it ... in any part of a line away from the beginning." | `rate(line-initial words starting y) > interior`; check the following-glyph distribution. |
| B9 | First word of a line ~1 char longer than following words (Vogt 2012, via S2) | S2 | "the first word tends to be on average 1 character longer than the second and following words." (EVA) | `mean(len(first word of line)) − mean(len(other words)) ≈ +1` char (EVA). |

---

## C. Paragraph-position effects

| # | Claim | Source | Verbatim quote | Suggested quantitative test |
|---|-------|--------|----------------|-----------------------------|
| C1 | `p`/`f` (the "second"/split gallows) appear 90–95% of the time in **first lines of paragraphs** | S1/S2 | "They ([p f]) appear 90-95% of the time in the first lines of paragraphs, in some 400 occurrences in one section of the manuscript." | `P(occurrence is in paragraph-first-line \| glyph∈{p,f}) ≈ 0.90–0.95`; report the section-level N (~400). |
| C2 | Split gallows occur essentially only on first lines of paragraphs and in labels (D'Imperio) | S2 | "The split gallows seem only to occur on first lines of paragraphs, and in labels." | `P(split/pedestalled gallows in para-first-line or label) ≈ 1`; near-0 in paragraph-interior lines. |
| C3 | Paragraphs nearly always begin with a gallows `k/t` (or variant `f/p`), often the second variant (Tiltman) | S2 | "Paragraphs nearly always begin with [k] [(f)] or [t] [(p)], most commonly in the second variant forms, which also occur frequently in words in the top lines of paragraphs where there is some extra space." | `P(first glyph of paragraph ∈ {t,k,p,f}) ≈ 1`; elevated share of `p/f` among these. |
| C4 | Herbal first paragraph usually starts `t/k/p/f` then `ch/sh/o/y/aiin/dy` (D'Imperio) | S2 | "On most herbal folios, the first paragraph usually starts with [t], [k], [p] or [f], usually immediately followed by [ch], [Sh], [o], [y], [aiin] or [dy]." | On herbal folios: `P(folio's first paragraph opens with gallows) high`; tabulate the second-glyph distribution. |
| C5 | Pedestalled-gallows ligatures never paragraph-initial, almost never line-initial | S1/S2 | "The ligatures can never occur as paragraph initial, and almost never line initial." / S2: "[cKh cTh cFh cPh] can never occur as paragraph initial, and almost never line initial." | `count(paragraph-initial word starts cth/ckh/cph/cfh) == 0`; line-initial rate ≈ 0. |
| C6 | Labels rarely start with gallows; start instead with o/d/y/s/ch (contrast to paragraphs) | S2 | "Labels very rarely start with [t], [k], [p] or [f]. Instead, they often start with [o], [d], [y] or sometimes [s] or [ch]." | Compare first-glyph distribution: labels vs paragraph-initial words; gallows share low for labels. |

---

## D. Word-boundary (adjacency) effect — Currier's 4th finding

Bonus target (Currier's "effect of word-final symbols on the initial of the following word"), strongly
A/B-stratified.

| # | Claim | Source | Verbatim quote | Suggested quantitative test |
|---|-------|--------|----------------|-----------------------------|
| D1 | Word-final `y` followed ~4× more often than expected by next-word `qo-`; Biological-B | S1 | "Words ending in the [y] sort of symbol ... are followed about four times as often by words beginning with [qo]. That is a fact, and it holds true throughout the entire twenty pages of Biological B." | In Bio-B: `P(next word starts qo- \| current word ends y) / baseline P(qo- initial) ≈ 4`. |
| D2 | `qo-`-initial words preceded largely by `y`-final; effect is B-only (A ≈ expected) | S1 | "the final symbol of words preceding words with an initial [qo] was restricted pretty largely to [y] ... This phenomenon occurs ... especially in ... Language B, but in no case with quite the same definity as in Biological B. Language A texts are fairly close to expected in this respect." | Compute preceding-word-final distribution before `qo-` words, per cluster; strong `y` skew in Bio-B, ≈ baseline in A. |

---

## E. Robustness assessment (modern re-analysis, Zandbergen [S2]/[S5])

| Target(s) | Modern assessment | Verbatim / basis |
|-----------|-------------------|-------------------|
| A/B distinction itself (A1–A15) | **Established.** Currier's split is confirmed and quantified; the open question is *interpretation* (dialect vs subject-matter vs cipher-style), not existence. | S3: "The usual differences between A and B are obvious"; A/B split independently reproduced in per-cluster frequency tables. Note S3: shared words "essentially excludes ... different plaintext languages." |
| Low conditional entropy / positional restriction (context for why these effects exist) | **Established / robust**, replicated by Bowern & Lindemann across 316 comparison texts. | S5 (quoted in S2): "an unusual conditional character entropy that is distinctly lower than any of the 316 comparison texts ... largely the result of common characters which are heavily restricted to certain positions within the word." |
| Line as functional entity (B1–B9) | **Accepted as a real, oft-cited feature**; further analysed (Vogt 2012 first-word length; Bunn/Schinner gallows positions). Zandbergen flags B2's exact meaning as **not fully understood**. | S2 note 17: "This statement is not fully understood, and it seems worthwhile to understand what he means." |
| Line-final `m` = 85% (B5) | Zandbergen **endorses the identity** of the symbol as `m` ("almost certainly"), but the 85% figure is Currier's and un-restated with modern counts → **replicate to confirm magnitude.** | S2 note 18. |
| Paragraph gallows enrichment (C1–C6) | **Widely accepted / repeatedly observed** (Currier, Tiltman, D'Imperio all converge). Good replication target; "grove words" = paragraph-initial gallows-word phenomenon. | Triangulated across S1/S2. |
| Vowel/consonant & HMM "circular" structure | **Weaker / harder to reproduce** — noted as unstable (Reddy/Knight result "very hard to reproduce"; V/C detection "confidence ... not very high"). Not a T1.1 target. | S2 §2.5–2.6. |

**T1.1 priority set (highest-confidence, cheapest to reproduce first):** A1, A2, A10, A11 (A/B lexical
signature) → B5, B7 (line entity) → C1/C2, C5 (paragraph gallows) → D1 (adjacency). These give a
spread across all four phenomena with clear pass/fail directions and, where available, target
magnitudes.
