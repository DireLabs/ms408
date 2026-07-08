# i03 — Experiment Agenda

Five experiments (E6–E10) that follow directly from the i02 refutation passes
(`../i02/STATUS.md`, `../../synthesis/FLAGSHIP.md` §6). Each names the open
question it inherits, the design, and the pass/fail criterion. All are pure-code on
data in hand unless marked. Priority: **E6 and E9 are co-flagship (P1)** — E6 tests
the one cipher family i02 could not exclude, E9 attacks the central meaningful-vs-
meaningless question. E8 is a dependency of E6 (supplies the whitened distance).

Dependency DAG:  E8 → E6 ;  E7, E9, E10 independent.

---

## E6 — Deterministic-verbose / nomenclator cipher: joint-signature reconstruction [P1, flagship]

**Open question (from E2).** E2 re-opened this family: a type-preserving
deterministic verbose cipher of blocked text **retains** the word-order signal (ΔI
0.356 @ 812), unlike the homophone-rich Naibbe form (ΔI 0.013). So the word-order
argument does **not** exclude deterministic-verbose / nomenclator / syllabary
ciphers. But i01's bracket established that *no family reproduced the VMS's JOINT
signature*. The live question: can a deterministic-verbose/nomenclator cipher
reproduce the whole signature **at once** — low h2 **and** the 812-scale ΔI **and**
the dense ED1 morphology network (main component ≈ 0.80) **and** both Zipf slopes?

**Design.** Build a parameterized deterministic verbose / nomenclator cipher over a
real medieval source (Latin herbal/Pliny + a German control), blocked into
sections the way the VMS is. Parameters: verbose glyph-string table per letter/
syllable; a nomenclator table mapping frequent plaintext words to fixed cipher
tokens; segmentation/respacing policy. Tune (equal-budget, held-out, per the E8
protocol) toward the VMS profile. Score the **full 11-metric profile** and, using
E8's whitened distance, report the joint match with bootstrap CIs. Report which
metric(s), if any, the family cannot satisfy simultaneously — the **ED1
paradigmatic-network** metric is the a-priori hard one (verbose ciphers of natural
text tend to ED1 ≈ 0.16–0.22; the VMS is 0.80).

**Pass/fail.**
- If a deterministic-verbose/nomenclator cipher can be tuned to match **h2 AND
  ΔI@~812 AND ED1≈0.80 AND Zipf** within held-out whitened CIs → the cipher
  hypothesis is **reinstated as a non-excluded reconstruction** (candidate B: "a
  deterministic verbose cipher reproduces the joint signature"; L7 — says nothing
  about plaintext).
- If it matches ΔI + h2 but **cannot** generate the ED1 network without breaking
  another metric → document the exact metric it breaks on; the family stays
  "consistent-with-word-order-only," and the paradigmatic network becomes positive
  evidence for a **constructed-morphology** mechanism over enciphered natural text.

---

## E7 — Fine-granularity anchor hunt (weak / rare regime) [P2]

**Open question (from E3).** E3's power curve showed the i01 anchor null excludes
only **strong, prevalence-balanced** anchors (φ≥0.4 on common features); recovery
cliffs to 0% at φ≤0.3, and rare-feature power is ~0.72. So a **weak (φ 0.2–0.35) or
rare-feature** anchor — exactly what an imperfect real-herbal encoding would
produce — is **not excluded**, and label-adjacency granularity was deferred.

**Design.** Re-run the anchor hunt at **finer granularity** — line-level and
label-adjacency (token adjacent to a labelled illustration element) rather than
page-level — restricted to **mid/rare-prevalence** features. Calibrate detectability
at that granularity with an E3-style planted-anchor power curve (the multiple-
testing burden changes with granularity, so power must be recomputed, not assumed).

**Pass/fail.** If a word→feature anchor appears at finer granularity that survives
BH-FDR **and** the granularity-specific power calibration says it is not a fluke →
a candidate **referential signal** (C→B, refutation pass required). If still null at
calibrated power → the anti-labelled-herbal bound extends into the weak/rare regime
and the constraint tightens.

---

## E8 — Whitened, continuously-tuned encoding bracket [P2, dependency of E6]

**Open question (from E5 refutation).** E5's fair bracket had two residual holes
the critic named: (1) the pre-declared 6-cluster vote left **cross-cluster
collinearity** (zipf~MZ-scale 0.85, position-entropy~repetition 0.80), so "one vote
per cluster" was not truly independent; (2) equal knob-**count** ≠ equal tuning
**power** — several families **railed at grid edges**, so their optima lay outside
the tested grid.

**Design.** Replace the cluster-vote distance with a **Mahalanobis / PCA-whitened**
distance on the empirical metric covariance (principled de-collinearization). Give
each family a **continuous / wider** tuning search (past the grid edges where
families railed), still fit-on-half / score-on-held-out, bootstrap CIs. Re-run all
seven i02 families + E6's deterministic-verbose family.

**Pass/fail.** Primarily a **method-hardening** experiment: does any family become
**robustly distinguished** (P(closest) ≥ 0.9, whitened-CI-separated) under the
corrected distance and fair tuning power? Expected null (confirming E5) — but now on
unimpeachable footing; a family emerging would be a genuine positive. Deliverable
also **provides the whitened distance E6 consumes.**

---

## E9 — VMS coordinate: dose-response localization [P1, flagship]

**Open question (from E1 + E5).** No single statistic settles meaningful-vs-
meaningless as a binary (E1: ΔI is block-structure; E5: no family distinguished).
Reframe the question as **continuous localization**: on interpretable generative
axes, *where does the VMS sit* between known-meaningful and known-meaningless
anchors? (This is the first study under the variable-introduction framework,
`../CONCEPT-variable-introduction.md`; **Type B**, synthetic ground-truth.)

**Design (pre-registered).** Pre-register a small set of **interpretable axes**,
each a generator parameter swept from a known-meaningful endpoint (real text) to a
known-meaningless endpoint (drift-null), with **the statistic that moves** named per
axis:
- word-order-information level (statistic: ΔI peak/scale),
- homophony degree (statistic: type-token coupling / ΔI retention),
- morphological-paradigm strength (statistic: ED1 main component),
- vocabulary-drift / source-locality rate (statistic: section↔text co-variation).

For each axis, calibrate the statistic's response across the sweep, then place the
**VMS as a coordinate** on that axis (with bootstrap CIs) relative to the anchors.
FDR across the axis family. Every axis on which the VMS looks *distinctively*
meaningful gets a dedicated refutation pass ("is the position an artifact of how the
axis was parameterized?").

**Pass/fail (exploratory by construction).** Success = a **reproducible VMS
coordinate with CIs on each pre-registered axis**, plus a plain statement of which
axes the VMS reads as meaningful-like vs meaningless-like. Per L35, all per-axis
leans are **grade D (exploratory) until independently replicated** on held-out data
or a fresh method. The deliverable is a hypothesis-generating map, not a verdict —
its value is converting an unanswerable binary into calibrated positions and
surfacing the single most promising axis for a future confirmatory study.

---

## E10 — root↔leaf: third independent rater [P3, needs D-i03-2]

**Open question (from E4b).** E4b resolved the root↔leaf association as tracking one
vision model's root labels, not the manuscript; the decisive control the critic
named is a **third, independent — ideally human — root_coloring rater**. Blocked on
Tim's source/spend decision (D-i03-2).

**Design.** A third independent root_coloring annotation of the herbal pages
(human, or a third vision-model family), blind. Re-run the cross-rater association:
does the leaf association reappear with a **non-Sonnet** root label? Report
inter-rater reliability and disattenuated associations.

**Pass/fail.** If the leaf association reappears with the third rater's (non-Sonnet)
root labels → a real manuscript bundle after all (overturns i01/E4b). If it appears
**only ever** with the original Sonnet root labels → confirmed single-model
artifact; the E4b verdict and i01 "within-organ only" leg are **locked**.
