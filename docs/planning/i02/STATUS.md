# STATUS.md — i02 Coordination Bus

_Last updated: 2026-07-07 (i02 kickoff)_

**Inherits:** all i01 locks L1–L34. Standing rule (new): every i02 result gets a
clean-context refutation pass before grading A/B.

## Experiments

| id | question | state | verdict |
|---|---|---|---|
| E1 | Is MZ a meaning detector? | ✅ done + refuted → revised | [C] DI value not a meaning certificate (stands); strong claim withdrawn on refutation (drift-null hits value at wrong scale). Confirms C5: DI can't settle meaningful-vs-meaningless. |
| E2 | Word-order signal confound | ✅ done + refuted → resolving controls run | [B] Reordering not an artifact; 812 = block scale; **anti-cipher point CORRECTED**: heavy-homophony cipher collapses DI (0.013) but type-preserving DETERMINISTIC verbose cipher RETAINS it (0.356) → nomenclator/deterministic cipher OPEN, not ruled out. Meaningless block stream reaches DI (2.18) → statistic measures block structure not meaning. |
| E3 | Anchor-hunt power curve | ✅ done + refuted → revised | [B] "Null informative" OVERSOLD (refutation applied). Recovery is a cliff (phi≤0.3→0%); power prevalence-dependent (rare 0.72 vs balanced 1.0). Honest: excludes only STRONG BALANCED anchors; weak/rare anchors NOT excluded → **weakens the flagship anchor leg**. |
| E4 | root↔leaf masked positive | ✅ done + refuted → **SUGGESTIVE-BUT-UNRESOLVED** | [C] Crude pigmentation confound rebutted; but E4b cross-model test (Opus 4.8 re-annotation) shows the association is **NOT symmetric**: every significant test rides on **Sonnet's** root label, every null test lacks it. root_coloring agrees 0.83 across models yet swapping to the 83%-concordant Opus root kills the effect in both leaf conditions — a real page property can't do that. Coded ">=1-of-2 cross" verdict was an **overclaim**, corrected to require symmetry + within-Opus replication (both fail). Same-source confound NOT cleanly broken; leans Sonnet-labelling artifact. i01 'within-organ only' WEAKENED, NOT overturned. Decisive control deferred: a THIRD (human) root rater. |
| E4b | E4 same-source confound test | ✅ done + refuted → correction applied | [C] See E4. `e4b_reannotate.py`; `results/experiments/e4b_crossmodel.json`. Refutation caught the coded overclaim; grade downgraded B→C. |
| E5 | Encoding bracket, fair (equal tuning, held-out) | ✅ done + refuted → **i01 downgrade CONFIRMED** | [C] With equal 6-point tuning, held-out scoring, de-collinearised clusters, composed families, and bootstrap CIs: **no family robustly distinguished.** conlang_relex leads by point estimate (0.669) but wins only 10% of bootstraps; selfcitation is modal (71%) but its lead is a **single-metric artifact** — drop `repetition_rate` (which its copying inflates) and P(closest) collapses 0.71→0.24, conlang re-leads. i01 'conlang best fit' does NOT survive fair tuning → **withdrawn as a distinguishing result**; bracket is descriptive only. Two bugs caught en route: 50-token block bootstrap destroyed the 812 MZ signal (fixed→2500, point-in-CI guard added); refutation caught selfcitation over-read. |

**Word-order story (E1+E2) resolved:** MZ cannot decide meaningful-vs-meaningless (E1); its 812 scale is a block-structure signature, not meaning (E1+E2); the signal is intrinsic, not a reordering artifact (E2); verbose cipher is disfavoured more firmly than i01 stated (E2). Net: flagship position reinforced, one part (anti-cipher) strengthened.

## Flagship revisions pending (fold in after E3–E5)

- **Cipher claim (from E2):** narrow "off-the-shelf verbose cipher disfavoured" →
  "heavy-homophony (Naibbe-class) verbose cipher disfavoured; type-preserving
  deterministic-verbose / nomenclator / syllabary cipher OPEN (retains the
  word-order structure)". This *re-opens* the cipher family i01 had leaned against.
- **Word-order framing (from E1+E2):** ΔI is a block-structure statistic, not a
  meaning statistic; the 812 scale is the section-block scale.

## Open decisions for Tim

- **E4 third-annotator (E4b) — DONE, resolved against the bundle.** Opus 4.8
  re-annotated 129 herbal pages blind ($4.14). Cross-model tests show the root↔leaf
  association is a **Sonnet-root labelling regularity**, not a manuscript bundle:
  only tests containing Sonnet's root are significant; the within-Opus replication
  fails despite 83% root agreement. Coded verdict self-corrected from "confirmed"
  to SUGGESTIVE-BUT-UNRESOLVED after the standing refutation pass. **i01's
  within-organ-only leg holds (weakened, not overturned).** The only control that
  would settle it further — a THIRD, human root_coloring rater — is deferred; flag
  to Tim as an optional future D-item (human-in-the-loop annotation), not blocking.
- **E5 fair encoding bracket — DONE, i01 downgrade confirmed.** No family
  survives fair tuning as a distinguishing fit. **All i02 experiments (E1–E5)
  complete.** Next: fold E1–E5 into a revised FLAGSHIP (consolidation, not new
  experiments). Proceed?

## i03 leads surfaced by the E5 refutation (deferred, not blocking)

- **Whitened distance.** Replace the pre-declared 6-cluster vote with a
  Mahalanobis/PCA-whitened distance on the empirical metric covariance — residual
  cross-cluster collinearity remains (zipf~MZ-scale 0.85, pos-entropy~repetition
  0.80). This is the principled de-collinearisation and a natural i03 Type-A
  (representation) variable per [[CONCEPT-variable-introduction]].
- **Equal tuning POWER, not just knob-count.** Several families railed at grid
  edges (verbose_cipher, conlang, composed) — their optima lie outside the 6-point
  grid, so "equal knob count" ≠ equal tuning power. Widen/continuous-optimise the
  grid before any family is treated as fairly beaten.
- **Human-in-the-loop root rater** (from E4b) — the one control that would settle
  the root↔leaf question.

## Sessions

- **Code session (i02)** — kickoff 2026-07-07, executing E1 first.
