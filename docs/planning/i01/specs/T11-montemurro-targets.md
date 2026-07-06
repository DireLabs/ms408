# T1.1 Replication Target — Montemurro & Zanette (2013)

**Purpose.** Extract the exact method and published numbers from Montemurro & Zanette's
information-theoretic analysis of the Voynich manuscript, precise enough to (1) reimplement the
"information in word ordering" measure and (2) quote replication targets in a T1.1 report.

**Primary source.** M. A. Montemurro & D. H. Zanette (2013), "Keywords and Co-Occurrence Patterns in
the Voynich Manuscript: An Information-Theoretic Analysis," *PLoS ONE* 8(6): e66344.
DOI: 10.1371/journal.pone.0066344. Open access, CC-BY.
URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344

**Method-defining companion (the "[6]" reference; contains the full derivation + analytic baseline).**
M. A. Montemurro & D. H. Zanette (2010), "Towards the quantification of the semantic information
encoded in written language," *Advances in Complex Systems* 13(2): 135–153.
arXiv: 0907.1558 (LaTeX source used below to recover exact formulas). This 2010 paper is where the
measure is *derived*; the 2013 Voynich paper reuses it verbatim (its Eqs. 1–3 = the 2010 Eqs. below).

All equations below were transcribed from the PLOS equation images (Eqs. 1–3) and cross-checked
against the arXiv 2010 LaTeX source (which gives the analytic shuffled-text baseline the 2013 paper
only references). Notation follows the papers.

---

## (a) THE METHOD — formula by formula

The measure is called **"information in the distribution of words"** (a.k.a. relative information
`ΔI(s)`), reported in **bits per word**. It is a bias-corrected mutual information between *word
identity* and *which part of the text a token falls in*, evaluated as a function of a partition
**scale s** (words per part). It is NOT an entropy-rate / character-entropy measure — do not confuse
with the older second-order character entropy work.

### Setup / partitioning
- Text has **N** tokens ("words"), with a lexicon of **K** distinct word types.
- The text is cut into **P** contiguous, equal-length parts, each of length **s = N/P** words.
  (So choosing a scale `s` is equivalent to choosing `P = N/s`. Sweep `s` — see "characteristic
  scale" below.)
- For a word `w` occurring `n` times total (`p(w) = n/N`), let `n_j` = number of occurrences of `w`
  in part `j` (`j = 1..P`), so `Σ_j n_j = n`.
- Probabilistic scaffold used to derive the measure (2013 Methods):
  - `p(j|w) = n_j / n` — distribution of word `w` over parts (normalized: `Σ_j p(j|w) = 1`).
  - `p(j) = 1/P` — a-priori (uniform) probability of part `j`.
  - `p(w) = n/N` — overall word frequency.
  - Bayes consistency: `p(j|w) p(w) = p(w|j) p(j)`.

### Eq. 1 — Mutual information (raw)
Mutual information between the sections of the text `J` and the word distribution `W`:

```
M(J,W) = Σ_{w=1..K} p(w) Σ_{j=1..P} p(j|w) · log2[ p(j|w) / p(j) ]        (Eq. 1)
```

(Equivalent bit-count form used in the 2010 paper: `M(J,W) = Σ_w Σ_j p(w) p(j|w) log2[p(j|w)/p(j)]`.)
This raw `M` is positively biased for low-frequency words because random fluctuations alone push
`p(j|w)` away from uniform. The bias is removed by subtracting the value expected under shuffling.

### Eq. 2 — Information in the distribution of words (the reported quantity, bits/word)
Define the shuffled-text mutual information `M̂(J,W)` = `M` computed on a random permutation of all
token positions, averaged `⟨·⟩` over all realizations. Then

```
ΔI(s) = M(J,W) − ⟨M̂(J,W)⟩
```

which, after expanding and regrouping (2013 Eq. 2 / 2010 Eq. "DIs"), becomes a per-word sum:

```
ΔI(s) = Σ_{w=1..K} p(w) · [ ⟨Ĥ(J|w)⟩ − H(J|w) ]                          (Eq. 2)
```

- `p(w) = n/N` (word frequency weight).
- `H(J|w)` = entropy of word `w`'s distribution over parts on the **real** text.
- `⟨Ĥ(J|w)⟩` = same entropy on the **shuffled** text, averaged over all shuffles (see Eq. 3 + baseline).
- Units: **bits per word** (verbatim, 2010: "`ΔI(s)` will have units of bits per word").
- Sign: real-text entropy `H(J|w)` is *lower* than the shuffled average for content words (clustered
  distribution), so each content word contributes a **positive** term; `ΔI(s) ≥ 0`.

### Eq. 3 — Per-word entropy on the real text
```
H(J|w) = − Σ_{j=1..P} (n_j / n) · log2(n_j / n)                          (Eq. 3)
```
(`n_j` = occurrences of `w` in part `j`; `n` = total occurrences of `w`.)

### The shuffled/randomized baseline `⟨Ĥ(J|w)⟩` — computed ANALYTICALLY (not by Monte-Carlo)
The 2013 paper says this "can be computed analytically [6]." The closed form (2010 Appendix C) is:

```
⟨Ĥ(J|w)⟩ = − P · Σ_{m=1..min(n, N/P)} p(m) · (m/n) · log2(m/n)
```
where `p(m)` is the hypergeometric probability of finding exactly `m` copies of `w` in one part:
```
p(m) = [ C(n, m) · C(N−n, N/P − m) ] / C(N, N/P)
```
(`C(a,b)` = binomial coefficient; part size `= N/P = s`.) This depends only on `n`, `N`, and `P`,
so it is a per-frequency lookup — you do NOT need to actually shuffle. (Monte-Carlo shuffling
reproduces it in the limit of infinite realizations; the paper's Fig. S1 shows real entropies
(black), one shuffle (grey), and this analytic mean (black line).)

### Per-word information value (for ranking keywords)
Each term of the Eq. 2 sum is the information contributed by one word:
```
ΔI_w = p(w) · [ ⟨Ĥ(J|w)⟩ − H(J|w) ]
```
This is the number reported in Table 1 (in bits). Ranking words by `ΔI_w` yields the "most
informative words" (keywords).

### Characteristic scale (peak-finding)
- `ΔI(s)` is evaluated as a function of scale `s` (equivalently number of parts `P`). Both large-`s`
  and small-`s` limits give low information (small `s`: every word appears 0/1 times per part →
  uninformative; large `s` → part ≈ whole text → uniform). Hence there is an interior **maximum**.
- The **characteristic / optimal scale** is the `s` (in words) at which `ΔI(s)` is maximal — "the
  scale at which the heterogeneity in the distribution of word frequencies over the text is largest."
- The reported max value = `max_s ΔI(s)` in bits/word; the reported scale = the arg-max `s`.
- Implementation note: `P = N/s` must be an integer-ish partition; sweep `P` over a range and plot
  `ΔI` vs `s = N/P`. (2010 examples swept from `s ≈ 100` words upward; peaks land in the
  hundreds-to-few-thousand-words range depending on corpus.)

### Significance of individual keywords (Table 1)
- Bootstrap: for each word, compare its real-text information `ΔI_w` against the distribution of
  values from **randomly shuffled** versions of the Voynich text.
- p-value = fraction of random realizations giving information ≥ the real-text value.
- **All 30 words in Table 1 have `p < 0.01`.** (Note the inline text also phrases the threshold as
  "1%".)

---

## (b) PUBLISHED VOYNICH NUMBERS + comparison corpora

### Characteristic scale
- **Optimal scale for the Voynich text = 807 words** (verbatim, Results: "the optimal scale is of
  807 words"). This is the arg-max of `ΔI(s)` used for Table 1 column 1.
- Natural-language texts peak at **~600–800 words**; the Voynich peak scale "is very similar to that
  of the human language examples" (Fig. 1B).
- Contrast corpora (Fortran source, yeast DNA) peak at scales "sensibly different from those of the
  human language texts and the Voynich manuscript" (Fig. 1B).

### Maximum information value `max_s ΔI(s)` (bits/word) — Figure 1A
Verbatim: "the maximum achieved by the information varies between approximately **0.2 bits/word for
Latin** to **0.6 bits/word for Chinese**." Placement of the others (qualitative, from Fig. 1A; the
paper gives no exact per-curve table):
- **Latin** (Augustine, *Confessions*): **≈ 0.2 bits/word** (lowest of the natural languages; high
  inflection → large vocabulary → less info/word).
- **English** (Darwin, *On the Origin of Species*): intermediate.
- **Voynich (V):** **"slightly above that of English"** and **"significantly below that of Chinese."**
- **Chinese** (Sima Qian, *Records of the Grand Historian*): **≈ 0.6 bits/word** (highest natural
  language; small effective vocabulary → more info/word).
- **Fortran (F)** and **yeast DNA (Y):** shown in Fig. 1A but distinguished mainly by *scale* (Fig.
  1B), not called out with numeric maxima in text.

> Figure 1A curve labels (verbatim): **F: Fortran; C: Chinese; V: Voynich; E: English; L: Latin;
> Y: yeast DNA.** All sequences were truncated to the *same number of words as the Voynich text*
> before analysis (see (c)). Figure 1B plots the scale of maximal information for each.

**Replication target summary (what T1.1 must reproduce, EVA / reordered Voynich):**
- Peak scale ≈ **807 words** (arg-max of `ΔI(s)`).
- Peak `ΔI` ≈ **just above the English curve**, between ~0.2 (Latin) and ~0.6 (Chinese) bits/word —
  i.e. plausibly in the **~0.3–0.5 bits/word** band. (The paper does not print an exact Voynich
  scalar; it is read off Fig. 1A. Treat "slightly above English, well below Chinese, peak at ~807
  words" as the quantitative gate, and reproduce the English/Latin/Chinese anchors as calibration.)

### Section-scale cross-check
- Optimal-scale partition uses `s = 807`. The **"thematic" sections average > 7500 words** each
  ("the average size of the 'thematic' sections is above 7500 words"). Table 1 column 2 recomputes
  word information using the 5 thematic sections as the partition instead of equal 807-word parts.

---

## (c) WHICH TEXT / preprocessing

- **Transliteration:** European Voynich Alphabet (**EVA**), the interlinear transcription maintained
  by **J. Stolfi**, file `98-12-28-interln16e6` from
  `http://www.ic.unicamp.br/~stolfi/voynich/98-12-28-interln16e6/`.
  (This is the interlinear EVA archive; the "16e6" majority-vote / reference interlinear version.)
- **Tokens ("words"):** space-separated character arrays. Analysis treats text as a sequence of
  word-tokens (not characters). Alphabet ≈ 40 symbols; words separated by spaces; no punctuation.
- **Reordering (important for exact replication):** results use a **reordered** manuscript where the
  ~dozen scattered folios are aggregated into their thematic section, preserving intra-section and
  overall section order. Section → folio mapping used:
  - Herbal: f1–57, 65–66, 87, 90, 93–96
  - Astrological: f67–73, 85–86
  - Biological: f75–84
  - Pharmacological: f88–89, 99–102
  - Recipes: f58, 103–116
  - Overall order: Herbal → Astrological → Biological → Pharmacological → Recipes.
- **Text length:** not stated as an explicit N in the paper. Inferable constraint: optimal scale 807
  words, and thematic sections average > 7500 words across 5 sections ⇒ **N ≈ 37,000–38,000 tokens**
  (order-of-magnitude; compute the exact N deterministically from the chosen EVA source in `src/` —
  do not hard-code). Manuscript = 104 extant folios.
- **Uncertain characters / labels:** the paper does not specify handling of EVA uncertainty markers,
  ambiguous glyphs, or whether isolated **labels** (astro/herbal label text) were included/excluded.
  → **FLAG (new D-item):** preprocessing of uncertain glyphs and label lines is unspecified in MZ2013;
  our T1.1 run must fix an explicit, documented policy and note the sensitivity. Do not assume.

---

## (d) Ranked most-informative words (Table 1) + significance

Table 1 = "The thirty most informative words in the Voynich manuscript" (EVA). Two partitions:
**Optimal Partition** (equal parts at `s = 807`) and **"Thematic" partition** (5 illustration-based
sections). Values are per-word information contributions in **bits** (`ΔI_w`). All entries `p < 0.01`.

| Rank | Optimal-partition word | ΔI (bits) | Thematic-partition word | ΔI (bits) |
|-----:|------------------------|-----------|-------------------------|-----------|
| 1 | shedy | 0.00937 | daiin | 0.00705 |
| 2 | qokeedy | 0.00840 | qokeedy | 0.00680 |
| 3 | daiin | 0.00777 | shedy | 0.00672 |
| 4 | qokaijn | 0.00754 | chedy | 0.00559 |
| 5 | chedy | 0.00716 | chor | 0.00512 |
| 6 | qokedy | 0.00649 | qokaijn | 0.00487 |
| 7 | qokar | 0.00538 | chol | 0.00487 |
| 8 | qokeey | 0.00518 | qokedy | 0.00461 |
| 9 | chor | 0.00514 | cthy | 0.00456 |
| 10 | ol | 0.00494 | qol | 0.00443 |
| 11 | chol | 0.00458 | s | 0.00376 |
| 12 | s | 0.00431 | qokeey | 0.00339 |
| 13 | cthy | 0.00431 | sho | 0.00319 |
| 14 | qokaiin | 0.00419 | ar | 0.00313 |
| 15 | qokal | 0.00372 | al | 0.00271 |
| 16 | al | 0.00372 | lchedy | 0.00263 |
| 17 | dy | 0.00337 | qokaiin | 0.00258 |
| 18 | ar | 0.00327 | chy | 0.00258 |
| 19 | aiin | 0.00302 | qokal | 0.00236 |
| 20 | okedy | 0.00300 | dain | 0.00231 |
| 21 | okaijn | 0.00287 | shol | 0.00223 |
| 22 | lchedy | 0.00285 | okaijn | 0.00221 |
| 23 | dain | 0.00282 | y | 0.00200 |
| 24 | okeey | 0.00281 | dy | 0.00192 |
| 25 | sho | 0.00270 | qotchy | 0.00190 |
| 26 | qokain | 0.00263 | cthol | 0.00190 |
| 27 | shey | 0.00251 | shor | 0.00189 |
| 28 | dal | 0.00245 | aiin | 0.00174 |
| 29 | otedy | 0.00244 | cthor | 0.00173 |
| 30 | chy | 0.00237 | qokain | 0.00171 |

**Replication acceptance for (d):** reproduce the optimal-partition top-10 set and ordering
(`shedy, qokeedy, daiin, qokaijn, chedy, qokedy, qokar, qokeey, chor, ol`) with `ΔI_w` values within
rounding of the above, and confirm each `p < 0.01` via the shuffle bootstrap.

**Significance procedure (verbatim intent):** per-word bootstrap; information on real text vs. many
randomly shuffled Voynich texts; `p` = fraction of shuffles with information ≥ real value; threshold
`p < 0.01`.

---

## (e) Co-occurrence / section-level findings (secondary; not part of the core T1.1 entropy gate)

These use a separate **word-space cosine** method, not the entropy measure. Included for completeness.

- **Word-space vectors.** Each of the top-informative words `w` → unit vector `u_w = f_w / |f_w|`,
  where `f_w` = frequency-over-parts vector (dimension P), `|·|` = L2 norm. Similarity matrix
  `S_{ww'} = u_w · u_w'` (= cosine of angle; all components ≥ 0 so `S ≥ 0`).
- **Word networks (Fig. 2):** computed on the **100 most informative** words; keep the strongest
  links (exact count rendered as an image in text; "the strongest [N] of connections"); each retained
  link verified `p < 0.01` by shuffling the part-indices of the frequency vectors independently.
- Morphological finding: strongly linked words share **prefixes** (e.g. `chol–chor`, Fig. 2C) or
  **suffixes** (e.g. `chedy–shedy`, Fig. 2A) → "strong connection between form and meaning."
- **Section network (Fig. 4):** same cosine method with sections as vectors of most-informative-word
  frequencies. Strongest link = **Pharmacological ↔ Herbal** (both plant illustrations); second
  strongest = **Recipes ↔ Astrological** (shared star-flower motif). Presented as first purely
  linguistic link between those section pairs.
- Cumulative-occurrence plots (Fig. 3) show slope changes at/near section boundaries → top words are
  section-specific.

---

## Reimplementation checklist (for `src/`)

1. Load EVA Stolfi interlinear `98-12-28-interln16e6`; build the **reordered** token stream via the
   folio→section map above; record exact **N** and **K** to `results/`.
2. For a swept set of part counts `P` (⇒ `s = N/P`): assign each token to part `⌊position / s⌋`;
   per word type compute `n`, `{n_j}`.
3. `H(J|w)` from Eq. 3; `⟨Ĥ(J|w)⟩` from the hypergeometric analytic form (Appendix C) — validate it
   against a Monte-Carlo shuffle mean on at least one `P` (they must agree).
4. `ΔI(s) = Σ_w (n/N)[⟨Ĥ⟩ − H]`; plot vs `s`; report arg-max scale (target ≈ 807) and max value
   (target: slightly > English, between Latin ~0.2 and Chinese ~0.6 bits/word).
5. At `s ≈ 807`: rank words by `ΔI_w`; reproduce Table 1 column 1; bootstrap `p`-values (< 0.01).
6. Calibrate by running the same pipeline on Latin/English/Chinese (Gutenberg: Augustine
   *Confessions*, Darwin *Origin of Species*, Sima Qian *Records of the Grand Historian*), each
   truncated to Voynich N, to reproduce the 0.2 (Latin) → 0.6 (Chinese) bits/word span and the
   600–800-word peak scale.

## Open items to FLAG (per binding rule 6)
- **D-item:** MZ2013 does not specify EVA uncertain-glyph / label-line handling. Fix an explicit,
  documented preprocessing policy for T1.1 and record a sensitivity note.
- The exact Voynich *scalar* max `ΔI` is not printed (read from Fig. 1A). Gate on {peak scale ≈ 807;
  ordering relative to English/Latin/Chinese anchors} rather than a single unpublished number.
- Exact "strongest N links" count for Figs. 2/4 is embedded as an equation image; retrieve if the
  co-occurrence network is later replicated (out of scope for the core entropy gate).
