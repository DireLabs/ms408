# i04 — Experiment Agenda (E11–E12)

Two experiments that close E10's two residual confounds. E11 is pure-code and
unblocked; E12 needs D-i04-1 (rater source).

---

## E11 — Illustration-style control for the root↔leaf bundle [P1, unblocked]

**Open question (from E10).** The bundle survives scribal hand + dialect, but a
finer illustration-STYLE convention (a drawing habit correlating root-colouring with
leaf-drawing on the page) could still produce it in any competent rater without
implying real botanical structure.

**Design (pure-code, existing annotations).** Build a coarse illustration-style
proxy per page from data already annotated: `color_palette`, `illustration_
coverage_pct`, `text_image_relationship`, and colored-vs-uncoloured. Re-run the
E10 CMH-style within-stratum permutation test for the root↔leaf association, now
stratified by (style-proxy × hand × dialect) — for BOTH Sonnet and Haiku roots.
Report observed Cramér's V and within-stratum permutation p.

**Pass/fail.** If the association SURVIVES conditioning on the style proxy (both
models, permutation p < 0.05) → not a style confound; the bundle strengthens further
and E12 (independence) becomes the sole remaining test. If it COLLAPSES within
style strata → the association is an illustration-style artifact; the bundle is
KILLED and the i01 "within-organ only" leg re-locks. Refutation pass required either
way (a null-endpoint style proxy is a real risk).

---

## E12 — Independent-lineage root rater [P1, blocked on D-i04-1]

**Open question (from E10).** All three raters share an Anthropic vision lineage; a
common prior could drive the association. The decisive independence test is a rater
OUTSIDE that lineage.

**Design.** Re-annotate the 129 herbal pages' root_coloring + leaf_arrangement,
blind, with a **non-Anthropic vision model** OR a **human** rater (D-i04-1). Add its
root labels to the E10 three-model cross analysis and test: does the leaf
association reproduce with this out-of-lineage root label, across the other raters'
leaf labels? Report inter-rater agreement and the stratified (hand×dialect, and
if E11 passes, ×style) association.

**Pass/fail.** If the out-of-lineage rater ALSO reproduces the association (survives
BH-FDR and, ideally, the stratified controls) → the bundle is **CONFIRMED** as not a
shared-model-lineage artifact — the program's first graded referential-signal
finding (still visual-only, no plaintext claim, L7). If it does NOT reproduce → the
association is consistent with an Anthropic-lineage shared bias; the bundle is not
established and E4b's artifact conclusion effectively stands (now on lineage rather
than single-model grounds).

---

## Not in i04 (backlog / i05)

- Abjad/abbreviation joint-signature test, exact-p graded anchor hunt, whitened-
  bracket retirement (FLAGSHIP §6 leads 2–4) — deferred; not part of the E10
  confirm-or-kill.
- The mid-level linguistic program (morphology, word-classes, function/content
  bimodality, syntax) with A/B stratification — **i05** (L37).
