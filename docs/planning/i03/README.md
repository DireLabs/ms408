# MS408 Research Program — Iteration 03

**Mandate:** i02 sharpened the envelope *by subtraction* — it showed the word-order
signal is block-structure not meaning (E1/E2), re-opened the deterministic/
nomenclator cipher family (E2), narrowed the anti-labelled-herbal null to a
strong-balanced-anchor bound (E3), resolved the root↔leaf "masked positive" as an
annotation artifact (E4b), and withdrew the "constructed-language best fit" claim
under fair tuning (E5). i03 turns from **subtraction to reconstruction**: it runs
the *positive* tests that the i02 refutations left as the live next questions, and
it operationalizes the central open question (meaningful vs meaningless) as a
**continuous localization** rather than a binary no single statistic could settle.

**Inheritance.** All i01 locks (L1–L34, `../i01/DECISIONS.md`) carry forward
unless amended here; i02 introduced no new locks, only the standing refutation
step. The pipeline, harness, corpus, v0.2 annotations, and the i02 experiment
package (`src/ms408/experiments/e{1..5}*.py`) are reused as-is. i03 experiments
continue the same package as **E6–E10** (one monotonic experiment ledger; iteration
is metadata, not a new numbering).

**Read in order:** this README → `EXPERIMENTS.md` (agenda + pass/fail) → `STATUS.md`
(live state).

## Standing corrections i03 must honor (unchanged from i02, + one addition)

1. **Blind nulls** — any "meaningless" baseline is adversarially optimized toward
   the discriminating statistic, blind to the real target.
2. **Confidence intervals** — no point comparison without the estimator's CI at
   real corpus length.
3. **Power reported** — no null without a power curve / minimum detectable effect.
4. **Disattenuation** — noisy-annotation associations reported raw and
   disattenuated.
5. **Symmetric evidence accounting** — nulls treated identically across hypotheses.
6. **Clean-context refutation pass** — every result gets one before grading A/B
   (i02 standing rule; it caught five over-reads and two silent method bugs in
   i02, including a verdict asserted by the analysis code itself).
7. **NEW — variable-introduction discipline** (for E9, see
   `../CONCEPT-variable-introduction.md`): controlled variables are introduced only
   as **Type A** (representation) or **Type B** (synthetic ground-truth), never a
   bare finding-hunt; the axis set is **pre-registered** with a statistic-that-moves
   per axis; results are **exploratory (grade D) until independently replicated**;
   FDR across the axis family. Candidate lock **L35** (D-i03-3).

## Reconstruction ≠ decipherment (L7 reaffirmed)

E6 asks whether a cipher *mechanism* can **reproduce the VMS's joint statistical
signature** — a sufficiency test on structure, not a claim about any plaintext. No
i03 experiment produces or endorses a reading; a positive E6 says "this encoding
class is not excluded," never "this is the text." The no-translation-without-an-
independent-statistical-anchor rule (L7) is absolute.

## Success criterion (i03)

For each experiment, a graded verdict that survives a fresh clean-context
refutation pass, OR a documented "remains underdetermined, because …". E9
additionally succeeds by producing a **reproducible VMS coordinate with CIs on
pre-registered axes** — its per-axis leans are explicitly exploratory (D) until
replicated. Decipherment is still not a goal (L1–L7).

## Open decisions for Tim (flag-don't-resolve)

- **D-i03-1 — i03 flagship.** E6 (cipher reconstruction) and E9 (VMS coordinate)
  are both flagship-class and attack *different* open questions. Recommendation:
  run **both** as co-flagships; if bandwidth-limited, **E9 first** (it targets the
  central meaningful-vs-meaningless question directly). Ratify or re-order.
- **D-i03-2 — E10 root-rater source.** The E4b critic wanted *human* ground-truth
  on root_coloring. Options: (a) a human annotator pass (logistics/spend), (b) a
  third independent *vision model* (cheap, but still model-labelling), (c) defer
  E10. Tim's call on source and spend.
- **D-i03-3 — ratify L35** (variable-introduction discipline) before E9 runs, so
  the garden-of-forking-paths guardrails are locked, not optional.
