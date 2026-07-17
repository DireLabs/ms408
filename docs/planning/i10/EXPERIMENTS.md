# i10 — Experiment Agenda (E27–): the symbols-as-values direction

Anchor-first (per README): the make-or-break is E28. E27 is cheap grounding; E29+ run
only if E28 signals.

## E27 — Symbol quantification [P2, grounding; descriptive]

**Question (the "quantify the symbols" ask).** What is the Voynichese symbol inventory, and
do its *structural* parameters resemble a numeral system, a syllabary, or an alphabet?

**Design.** From the ZL transliteration (EVA; v101 sensitivity per L11), compute, stratified
by Currier A/B, hand, and locus type (paragraph vs label vs circular/radial): the distinct
glyph inventory and frequency distribution; the **effective** alphabet size (e.g.
perplexity / Heaps of glyphs, since ~15 of ~39 carry nearly all mass); the positional glyph
distributions (word-initial / medial / final "slots"); and a small set of
**system-type discriminators** — per-position branching, positional entropy profile, and
glyph-repetition structure — reported next to reference values for known **base-N numeral
systems, syllabaries, and alphabets**. No claim beyond description.

**Deliverable / grade.** A firewall result characterising the inventory. Descriptive (feeds
E28/E29); it **cannot** on its own support a register claim (L7, and the i09 lesson).

## E28 — Angular/ordinal anchor in the circular diagrams [P1, GATING the whole iteration]

**Question.** Do label sequences in the angular-tagged circular diagrams (zodiac rings,
radial/circular loci) show **ordinal or periodic structure** — content that tracks angular
position the way a degree, date, or count would — beyond a matched null? This is the
decipherment-free arithmetic anchor; it is the one test that can lift the register hypothesis
above grade D.

**Design.**
- **Extract** (E28 precondition, D-item i10-c): from the 12 zodiac pages, the
  `(angular position, label token)` pairs (`<!HH:MM>` clock tags); from circular (C*) and
  radial (R*) loci, the ordered token sequence. Verify the tags/order encode true spatial
  sequence before scoring.
- **Value-agnostic ordinal tests** (no glyph→value map assumed): for each ring, test whether
  a *panel* of label features — token length, first/last glyph, glyph multiset, a rank-based
  value proxy — varies with angular position via (a) **monotone trend** (Spearman vs a
  circular/linear coordinate), (b) **periodicity** (autocorrelation / a single dominant
  Fourier component around the ring), and (c) **local ordering** (adjacent labels more
  similar than distant — a "counting" signature). Aggregate across the 12 rings.
- **Null + harness (L4).** Compare every statistic to (i) a within-ring label-order shuffle
  (destroys angular structure, preserves the label multiset) and (ii) a positive control —
  a *synthetic* ring of known ordered values (dates/degrees) rendered through a VMS-like
  glyph grammar — to confirm the test *detects* ordinal structure when present. Stratify by
  A/B and hand (L8).

**Pass/fail.** A robust, refutation-passed ordinal/periodic signal beyond the null, present
across multiple rings and matching the positive control's behaviour → **the register
hypothesis is elevated to C/B** and E29 becomes worthwhile. No signal (the likely outcome
given the low prior) → the register hypothesis **stays D**; i10 closes with a clean graded
negative (angular labels carry no detectable value-order), a real envelope result. Either
way: refutation pass; no value/number/date is ever named (L7).

## E29 — Digit-slot discriminator + numeral-register controls [P2, CONDITIONAL on E28 signal]

**Runs only if E28 signals.** (a) **Digit-slot vs syllable-slot:** does Voynichese positional
glyph structure behave like place-value digit-slots (value a function of position, small
per-slot alphabet, no cross-slot phonotactic constraints) or like syllable-slots? Scored
against known numeral registers *and* syllabic scripts. (b) **Control-corpus acquisition**
(L19 policy, D-item i10-b): profile known value-registers (khipu transcriptions, medieval
account books, Cistercian tables) — the control class the Rao–Sproat debate says the field
omits — and place the VMS against them, not just against languages.

**Pass/fail.** Digit-slot structure + register-corpus proximity, *with* the E28 anchor →
a graded (B-ceiling) "consistent with a quantitative register" account. Without the E28
anchor these are descriptive only (the i09 caution) and do not lift the grade.

## Not in scope for i10

Any glyph→value assignment, decoding, or "reading"; generic summation search on
non-tabular folios (deprecated in favour of the angular anchor); expensive control
acquisition before E28 justifies it.
