# W6a Assumption Audit → Phase 2 Variant Matrix (T1.4)

Generated for Tim's review before any Phase 2 sweep runs. Task T1.4 per RESEARCH-PLAN §4-W6a and
WORKFLOW.md §6 ("Cowork session 2"). Binding rules in force: evidence grading (L6), flag-don't-resolve
(rule 6), transliteration sensitivity (L11), stratification (L8).

**Purpose.** Every prior decipherment attempt inherited a stack of unexamined assumptions from the
transliteration it used. The historical pattern (RESEARCH-PLAN §4-W6): undeciphered scripts fell when
someone killed a *boring shared assumption* (Linear B ≠ Greek-first; Mayan ≠ pure ideography; Z340
transposition), not when exotic hypotheses were added. This document (1) inventories those assumptions
with graded evidence for and against, (2) turns each into a concrete runnable variant against our
actual pipeline naming the statistic that would move if the assumption is false, and (3) recommends a
P1 set of ≤6.

**How to read the matrix.** "Operationalization" names the real module and the specific hook
(`ivtff.TextPolicy`, `studies/topics.py::page_vectors`, etc.). "Statistic that moves" is mandatory per
the workflow brief: if relaxing the assumption does not move that number, the assumption was harmless
for our conclusions. Costs are relative to our existing deterministic runs (a full study is minutes).

**Scope note (flag, not resolve).** Several variants below require a *new pipeline capability* that
does not exist yet (right-to-left token reversal, alternative word-segmentation, layer-stripping
transforms). Those are flagged `[NEW CODE]`; the matrix specifies what to build, but building it is a
Code-session task gated on this matrix's approval. Nothing here is executed.

---

## Part 1 — Assumption Inventory

Each entry: **who relies on it · evidence for/against (graded) · what breaks if false.** Grades per
RESEARCH-PLAN §6 (A validated on harness / B suggestive / C sourced-qualitative / D speculation).

### A1. Spaces = word boundaries

- **Who relies on it.** Everything word-level: our `ivtff.words()`, the Zipf/lexical battery, MZ
  word-order information, morphology's ED1 network, topics' page TF-IDF. Every published attempt that
  counts "words" (Currier, Bowern–Lindemann, Montemurro–Zanette, Naibbe).
- **For.** Spaces produce a stable, reproducible token stream with strong Zipfian word-frequency
  structure and a 807-word MZ information peak matching natural language (replication_report.md
  MZ-scale PASS) — **[B]** these regularities would be hard to obtain from arbitrary segmentation.
  Currier's own positional findings (word-final `-dy`, word-initial `qo-`) presuppose word units and
  replicate cleanly **[B, our replication PASS]**.
- **Against.** Currier himself: *"That's just the point — they're **not words**!"* — he flagged they
  might be "syllables, letters, even digits" **[C, voynich.nu/curr_main]**. Transcribers disagree on
  where spaces fall; word-boundary placement is "based on subjective decisions … deriving from the
  layout" and the main transliterations "do not all capture the same information"
  **[C, voynich.nu/sp_transcr]**. The LSI/Takahashi convention counts only "credible" breaks
  (periods) and drops "possible" breaks (commas) — a policy choice, not a datum (spec T11-entropy
  §1.4). Our own `TextPolicy.comma_is_word_break` defaults True, i.e. we currently *merge* uncertain
  spaces into breaks — the opposite of LB's convention, and untested for sensitivity.
- **What breaks if false.** If spaces are prosodic/decorative or mark sub-word units, then "word
  frequency," Zipf, the MZ peak, and TTR are all artifacts of segmentation, and the whole
  word-morphology program (chol/chor network) is measuring glyph-run co-occurrence, not lexicon. This
  is the single highest-leverage assumption in the stack.

### A2. Reading order: left-to-right, top-to-bottom, front-to-back

- **Who relies on it.** MZ word-order information (order-sensitive by construction), any
  bigram/adjacency statistic (Currier's 4th finding, our `adjacency_battery`), the "line as functional
  unit" tests, and any future decode. Naibbe H2 assumes L-to-R plaintext order.
- **For.** Paragraph-initial gallows enrichment (85%, our P-par-gallows PASS) and the systematic
  line-initial/line-final asymmetries are only coherent under a fixed directional reading
  **[B, replication PASS]**. Feaster's rightward/downward gradient analysis argues glyph choice is
  *constrained by position rightward and downward*, consistent with L-to-R/top-down writing
  **[C, Feaster 2022, CEUR Vol-3313]**.
- **Against.** A published (weak) claim that the VMS is "partially written right to left" exists
  **[C/D, ResearchGate preprint, low credibility]**. More seriously, order-sensitivity is *itself*
  the thing MZ measures: we have never tested whether the 807-word peak survives token reversal, so we
  do not know how much of our "natural-language-like word-order information" is direction-dependent vs
  a symmetric clustering artifact.
- **What breaks if false.** MZ information and all adjacency findings would need reinterpretation. A
  null result (peak survives reversal) is itself a useful constraint: it would show the information is
  in *clustering*, not *sequence*.

### A3. One glyph ≈ one sound / one unit (transcription granularity is meaningful)

- **Who relies on it.** All character-entropy work (h1/h2, the headline "anomaly"), Timm's curve-line
  grammar, the abjad/abbreviation encoding families. EVA's `ch`/`sh`/`iin` are transcription
  compromises, not claims about units.
- **For.** The h2 anomaly (2.13, below every one of 316 comparison texts) is robust across Maximal,
  Simplified, and Minimal EVA and across v101 **[A-adjacent, LB2021 §4; our E-full PASS; morphology
  claim 5 v101 direction-stable]**.
- **Against.** EVA renders `ch` as two half-characters purely so struck-through gallows can be written
  `cth`/`ckh` — an explicitly *typographic* decision **[C, ciphermysteries]**. Whether `r`/`s`/tailed
  glyphs are one unit or several is openly unknown **[C, voynich.nu]**. Glen Claston built v101
  precisely on the belief that incidental shape differences EVA collapses may encode distinct tokens
  **[C]**. The choice of alphabet changes h2 by up to the Maximal→Minimal gap (2.11→2.48) — small
  relative to the anomaly, but non-zero (spec T11-entropy §4).
- **What breaks if false.** If the true unit is the glyph-*group* (verbose cipher: `ol`/`aiin`/`qo`
  = one plaintext letter), then character entropy is computed on the wrong alphabet and the "anomaly"
  is partly a units artifact. This is the mechanism behind the verbose-cipher family.

### A4. Text relates to the adjacent image

- **Who relies on it.** W3 anchor hunt (T2.3), the topics key test (T2.2), the whole
  "herbal/balneological/astronomical content" reading, plant-ID priors.
- **For.** Topic structure induced from text alone reproduces section boundaries above chance at
  whole-MS level **[B, our topics claim 2, ZL p=0.004 / v101 p=0.0005]**, and *within Language A* the
  text tracks sections strongly (ARI 0.35, p=0.0005) — text-image co-variation is real on the A side
  **[B]**. MZ's section network links Pharma↔Herbal (both plant images) purely from text
  **[C, MZ2013]**.
- **Against.** **Our own strongest new finding:** within Language B the text does **not** track
  sections at all (ARI 0.0036, p=0.40; v101 0.0086, p=0.28) — B's bio/stars/herbal-B/recipes pages are
  textually homogeneous **[B, topics claim 2]**. So text-image alignment is an A-side, page-granularity
  phenomenon; assuming it holds everywhere is false for half the manuscript.
- **What breaks if false.** The anchor hunt (T2.3) must be stratified A vs B and may be near-hopeless
  on B; plant-ID soft priors (L14) are even softer on B pages; any "this text describes this picture"
  narrative is A-only.

### A5. Single language / single system throughout

- **Who relies on it.** Any pooled-corpus statistic; the encoding bracket (fits one generative model
  to the whole stream); pooled entropy targets.
- **For.** Shared high-frequency words across all clusters (`daiin, chey, ol, or, saiin`) argue
  against two *different plaintext languages* **[C, Zandbergen]**. A/B differ in degree (affix rates),
  not kind.
- **Against.** Currier A/B is *established* structure, not hypothesis: it is the dominant axis our
  topic clustering recovers (v101 2-cluster ARI 0.90) **[B, topics claim 1]**; entropy differs (A 2.12
  vs B 1.97) **[A, replication PASS]**. Currier flagged possibly "as many as eight or a dozen"
  hands and doubted even his own A/B universality on intermediate pharma pages **[C, curr_main]**.
  Fagin Davis's 5-hand model (L8) is a further subdivision.
- **What breaks if false.** Pooled entropy/Zipf/encoding-bracket numbers are mixtures. The encoding
  bracket especially: if A and B are different *encodings* (e.g. A = plaintext-ish, B = more processed),
  fitting one family to the pooled stream is category error. **L8 already mandates A/B stratification;
  the gap is that our encoding bracket (T2.4) does NOT yet stratify** — it fits families to the pooled
  MZ-reordered stream.

### A6. Line breaks are arbitrary (vs. line as a functional unit)

- **Who relies on it.** Treating the token stream as continuous prose (MZ reordering concatenates
  across lines; morphology ignores line position). The "it's just text that wraps" default.
- **For.** — (little; the evidence runs the other way).
- **Against.** Strong and old. Currier: *"the line is a functional entity … on all those pages where
  the text is presented linearly"* **[C, curr_main]**. Line-initial `ch/sh` suppression (our P-chsh
  PASS), line-final `m` concentration (P-m-final PASS), first-word-longer effect (P-firstlen CHECK,
  direction confirmed), and no-repeat-across-line-break (P-crossline PASS, ~6× suppressed) all
  replicate on our corpus **[B, multiple replication PASS]**. Vogt (LAAFU 2012) and Feaster's
  downwardness both formalize it **[C]**.
- **What breaks if false (i.e. if lines ARE functional).** Then concatenating across line breaks (as
  MZ and we do) mixes a layout-structured signal into "word order," and morphology should be computed
  *conditioned on line position*. The line, not the paragraph, may be the composition unit.

### A7. Single encoding layer

- **Who relies on it.** The encoding bracket's premise that one generative transform maps plaintext →
  Voynichese. All single-step decode attempts.
- **For.** Parsimony; no positive evidence *requires* multiple layers.
- **Against.** Our encoding bracket's central negative result: **no single family reproduces the VMS
  signature** — gibberish-like h2 (2.13) *together with* natural-scale word-order information (ΔI 0.307
  @ 812) **[B, encoding claim 1]**. A verbose cipher matches h2 but erases word order (ΔI 0.000);
  self-citation gets word order but at the wrong scale/vocabulary. A layered account (e.g. verbose
  substitution over a real-language skeleton, or a template + fill) is the natural reading of "no one
  family fits."
- **What breaks if false (multi-layer true).** Single-transform decode is doomed; the bracket must
  test *compositions* of families, not single families.

### A8. Transliteration neutrality (EVA is a neutral window)

- **Who relies on it.** Any result reported on EVA alone; the implicit claim that EVA choices don't
  steer findings.
- **For.** The headline anomalies (h2, ED1 density, position restriction) hold in *direction* across
  EVA and v101 **[B, morphology claim 5; topics claim 4]**.
- **Against.** **Our own finding, and it is not subtle:** v101 consistently shows *stronger* structure
  than EVA. Topics: section ARI 0.28 (v101) vs 0.07 (EVA); 2-cluster A/B ARI 0.90 vs 0.44
  **[B, topics claim 4]**. If a finer transliteration carries more recoverable signal, EVA is
  *lossy*, not neutral — it is discarding distinctions that matter. L11 already mandates a v101
  sensitivity pass; this finding says the sensitivity pass is not a formality but a lead.
- **What breaks if false.** EVA-only results understate structure; the "right" alphabet is an open
  empirical question, and v101 (or an even finer one) may be the correct substrate for the anchor hunt
  and encoding work.

### A9. (Added) Word tokenization = EVA glyph segmentation

- Distinct from A1 (where the *spaces* fall) and A3 (what a *glyph* is): even granting spaces and
  glyphs, we tokenize with a fixed policy (`ivtff.TextPolicy`: first-alternative for `[a:b]`, strip
  braces, comma=break). These are load-bearing, undocumented-as-sensitivity choices. **[C]** Relies on:
  every word count. Breaks if false: token identities (and thus type counts, ED1 network, TTR) shift.

### A10. (Added) Page/folio order = composition order

- **Who relies on it.** MZ reordering uses a *specific* folio→section map (spec T11-montemurro §c);
  the sequential boundary test (topics) uses manuscript order.
- **Against.** Codicological consensus: the current binding order is **not** original — bifolios were
  reordered, A/B herbal bifolios "arbitrarily mixed," quire 19 belongs before quire 15
  **[C, voynich.nu/descr; ciphermysteries]**. **[C]**
- **What breaks if false.** The sequential (adjacent-page) boundary test is measuring a modern binder's
  order, not the author's. MZ's section-reordering already *corrects* for this by aggregating to
  thematic sections, so the equal-parts MZ peak is robust; the adjacent-page Δ (0.0687, p=0.034) is
  not. Low-severity for our headline stats, but it invalidates one specific test.

### A11. (Added) All hands write the same system

- L8 stratifies by A/B and by hand, but our encoding bracket and much of morphology pool across hands.
  Currier: possibly "eight or a dozen" hands, and he could not confirm the pharma section is one hand
  **[C]**. Fagin Davis: 5 hands **[C, L8]**. Breaks if false: per-hand encoding could differ; pooled
  bracket is a mixture (overlaps A5).

---

## Part 2 — Variant Matrix

Runnable Phase-2 variants. Module hooks verified against source docstrings. "Stat that moves" is the
falsifier. Cost: **trivial** = param flip on an existing run; **moderate** = new corpus/config, existing
code paths; **expensive** = new pipeline capability `[NEW CODE]`.

| ID | Assumption relaxed | Operationalization (module · hook) | Statistic that moves if assumption is wrong | Cost | Prio | One-line justification |
|---|---|---|---|---|---|---|
| **V1** | A3 units / A8 neutrality | `studies/encoding.py` + `studies/topics.py` + `studies/morphology.py`: rerun full battery on **v101 (GC)** as the *primary* substrate, not just sensitivity. Hook: corpus selection already exists (`_corpora` has `gc_v101`); promote it to first-class across all three studies. | Topic ARI (v101 0.28 vs EVA 0.07); 2-cluster A/B ARI (0.90 vs 0.44); any encoding-family distance re-ranking under v101 units | trivial | **P1** | Our data already says v101 carries more signal; make it primary and quantify the gap everywhere, not just topics. |
| **V2** | A7 single layer + A3 units (homophone-poor verbose cipher) | `harness/naibbe.py` `NaibbeConfig`: raise `respacing` (18=simplified, higher→more unigram/fewer homophone draws) and/or reduce deck (`deck="52"`→smaller) to suppress homophony; re-score via `studies/encoding.py::family_verbose_cipher`. | **MZ peak value** (published-Naibbe erases it: ΔI 0.000 vs VMS 0.307). A homophone-poor cipher should *recover* nonzero word-order info; the value + peak scale (812) are the target. | moderate | **P1** | Directly named lead (encoding claim 2/5): the published Naibbe erases the word-order info the VMS has; test whether a low-homophony variant restores it. |
| **V3** | A5 conlang morphology (paradigmatic/templatic relexification) | `studies/encoding.py::family_conlang` / `_conlang_word`: replace the naive per-type random lexicon with a **paradigm generator** — shared prefix/stem/suffix slots (Lingua-Ignota-like), so word types share morphology. | **ED1 main-component share** (naive conlang = 0.001 vs VMS 0.797) and position entropy. A templatic conlang should build the dense edit-distance network the naive one lacks. | moderate | **P1** | Named lead (encoding claim 4/5): naive relexification has *no* morphology network; the real test is a paradigmatic conlang. |
| **V4** | A4 text-image + A5 single system (B-side homogeneity) | `studies/topics.py::analyze`: formalize the within-A vs within-B asymmetry — add per-section-within-B pairwise cosine and a B-only anchor-feasibility metric; feed A/B split into `studies/encoding.py` so the bracket fits families **separately to A and B streams**. | Within-B section ARI (currently 0.0036, p=0.40) vs within-A (0.35); per-family encoding distance computed on B-only vs A-only vs pooled | moderate | **P1** | Named lead (topics claim 2): text-image co-variation is A-side only; the encoding bracket currently ignores A/B (violates spirit of L8) and may be averaging two systems. |
| **V5** | A2 reading order (direction) | `[NEW CODE]` in the token-stream builder feeding `mz.py`: reverse token order within-line (and a within-word glyph-reverse variant); recompute MZ ΔI and `adjacency_battery`. | **MZ peak value + scale** and Currier's 4th-finding ratio (y→qo). If word-order info is direction-bound, reversal collapses ΔI; if it survives, the info is in clustering, not sequence. | moderate | **P2** | Cheap-ish new code; a null (survives) is itself a citable constraint on where the information lives. |
| **V6** | A1 spaces = boundaries | `[NEW CODE]` alternative segmentation on `ivtff` cleaned text: (a) ignore spaces, re-segment by a data-driven unsupervised morpheme model (e.g. Morfessor/BPE) or fixed n-gram windows; (b) toggle `TextPolicy.comma_is_word_break`. Rerun Zipf + MZ + ED1. | **MZ peak scale** (807/812), Zipf slope, TTR, ED1 main-component. If these regularities survive resegmentation they are space-independent; if they vanish they were segmentation artifacts. | expensive | **P2** | Highest-leverage assumption (Currier: "they're not words"), but needs a new segmentation module + careful design; do after the trivial/moderate P1s. |
| **V7** | A6 line as functional unit | `studies/morphology.py`: recompute affix + positional-concentration statistics **conditioned on line position** (line-initial / interior / line-final word), not pooled; add line-position as a stratum. | Position-entropy and affix-coverage deltas between line-initial vs interior words; whether the ED1 network differs by line slot | moderate | **P2** | Strong replicated evidence lines are functional (P-chsh, P-m-final, P-crossline all PASS); pooling may wash out line-structured morphology. |
| **V8** | A8 neutrality (finer than v101) / A9 tokenization | `ivtff.TextPolicy` sensitivity grid: flip `first_alternative`, `comma_is_word_break`, `strip_braces`, `drop_uncertain_words`; report metric spread. | Type count, TTR, ED1 main-component, h2 spread across policy grid | trivial | **P2** | Cheap robustness floor: shows how much our headline numbers depend on undocumented tokenization defaults. |
| **V9** | A7 single layer (composed encodings) | `studies/encoding.py`: add composed generators — e.g. verbose-substitution *over* a conlang skeleton, or template+fill — as new `family_*` functions scored on the same profile. | Joint (h2, MZ peak value, ED1) distance to VMS: does any *composition* achieve low h2 AND ΔI≈0.307 that no single family reaches? | expensive | **P3** | The bracket's central negative result points at layering; but combinatorial and best attempted after single-family sweeps (V2/V3) narrow the space. |
| **V10** | A10 page order = composition order | `studies/topics.py::boundary_test`: recompute the adjacent-page test under alternative codicological orderings (e.g. Currier bifolio groupings) vs current binding order. | Adjacent-page within/across-boundary Δ (currently 0.0687, p=0.034) | trivial | **P3** | Invalidates one specific test if binding ≠ original; low severity (MZ already section-aggregates), so low priority. |
| **V11** | A11 per-hand system | `studies/encoding.py` + `morphology.py`: stratify by Fagin Davis hand (metadata already joined, `$H`), rerun bracket/morphology per hand. | Per-hand h2, ED1, encoding-family distance; do hands within B differ? | moderate | **P3** | L8 already flags hand stratification; largely subsumed by V4's A/B split for first-pass purposes. |

---

## Part 3 — Recommended P1 Set (run first)

Six variants, chosen so that (a) the four named leads from our own studies are each covered by a
concrete run, (b) the two highest-leverage *general* assumptions (transliteration neutrality; single
system) get first-class treatment, and (c) all six are trivial/moderate cost — no P1 depends on new
pipeline capability, so they can run immediately on approval.

1. **V1 — v101 as primary substrate** (trivial). Our data already shows v101 > EVA for recoverable
   structure (topics ARI 0.28 vs 0.07). Promoting it across all three studies is a param change that
   directly tests A8 (transliteration non-neutrality) and re-grounds everything else. Do this first
   because it may shift the baselines the other variants are measured against.

2. **V2 — homophone-poor verbose cipher** (moderate). Named lead. The published Naibbe erases
   word-order information (ΔI 0.000 vs VMS 0.307); the whole verbose-cipher hypothesis lives or dies on
   whether a low-homophony parameterization restores the 807-word MZ peak. Highest-information single
   experiment for the encoding bracket.

3. **V3 — paradigmatic/templatic conlang** (moderate). Named lead. The naive relexification has no
   morphology network (ED1 0.001 vs 0.797); a Lingua-Ignota-style paradigm generator is the fair test
   of the constructed-language hypothesis. Pairs with V2 to properly bracket cipher vs conlang.

4. **V4 — A/B stratified bracket + B-homogeneity formalization** (moderate). Named lead, and it fixes a
   real gap: our encoding bracket currently pools A and B, contra the spirit of L8. Text-image
   co-variation is A-side only; if A and B are different systems, every pooled number (V2/V3 included)
   is a mixture. Run alongside V2/V3 so their generators are scored against the right (stratified)
   target.

5. **V8 — tokenization/TextPolicy sensitivity grid** (trivial). Cheap robustness floor for A9/A8. Before
   we build expensive resegmentation (V6), quantify how much our headline numbers already move under
   the tokenization choices we *already* make. If the spread is large, V6 becomes urgent; if small, the
   space-boundary question is better-posed.

6. **V5 — reading-order reversal** (moderate, small new code). The cheapest probe of the biggest
   untested directional assumption (A2). A null (MZ peak survives reversal) is a genuinely useful
   published constraint — it localizes the manuscript's information in *clustering* rather than
   *sequence* — and it is a prerequisite framing for interpreting V2/V6.

**Deferred to P2/P3 and why.** V6 (unsupervised resegmentation of A1) is the single highest-leverage
assumption but needs a designed new module and should follow V8's evidence on how fragile tokenization
already is. V7 (line-as-unit conditioning) and V9 (composed encodings) are strong but second-order:
run after the P1 set tells us whether we are even working on the right substrate (V1) and unit (V8).
V10/V11 are low-severity or subsumed by V4.

**Open items flagged for Tim (flag-don't-resolve).**
- The encoding bracket (T2.4) pooling across A/B is arguably already inconsistent with L8's
  stratification mandate — V4 proposes the fix, but whether to *re-run the baseline bracket stratified*
  before Phase 2 is a decision for you.
- V1 proposes making v101 a *primary* substrate rather than a sensitivity pass; that touches L11's
  "EVA primary" lock. Surfacing as a potential new D-item rather than acting on it.
