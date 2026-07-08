# Concept Memo — Controlled Variable Introduction as a Study Unit

**Status:** design memo (Tim's idea, 2026-07-07). Not yet an iteration; a framework
for how future iterations could use *introduced variables* to re-run experiments
and surface findings. Written against what i01/i02 already built.

## The idea (restated)

As the harness and validation harden, can we systematically **introduce controlled
variability along specific dimensions** of the data, re-run the experiments, and
learn how each dimension affects the results — each introduction framed by its own
hypothesis narrative, potentially surfacing new findings?

**Verdict: yes, and it's the natural generalization of what the program already
does — but it has a sharp double edge, and the framework's entire job is to keep
us on the right side of it.**

## Why it fits: we already do this (three proofs of concept)

Every one of these is a "variable introduction" in Tim's sense:
- **v101 vs EVA** (i02 V1 / P1 sweep): introduce the *transliteration* variable →
  discovered v101 carries **more** recoverable structure than EVA. A real,
  unexpected finding from a variable introduction.
- **The harness generators** (Naibbe, self-citation, drift-null): introduce a
  *generative-mechanism* variable → calibrate what the statistics mean.
- **Planted anchors / drift spread / homophony sweeps** (E1, E2, E3, V2): introduce
  a *known synthetic* variable → calibrate detectability (power, validity).

So the machinery exists; the idea is to promote it to a **first-class, repeatable
study unit** with its own discipline.

## The two legitimate types — and the one dangerous one

The key insight is that "introduce a variable" splits into three epistemically
different operations. The first two are gold; the third is the trap the whole
program was built to avoid.

### Type A — Representation / measurement variables (sensitivity analysis)
Vary *how we represent or measure* the manuscript, holding the manuscript fixed:
transliteration (EVA/v101), tokenization (`TextPolicy` grid), section grouping,
annotation granularity/schema, corpus subsetting (by scribe/quire/dialect),
reading order. **Hypothesis form:** "does finding X survive when representation
dimension D changes?" A finding that survives is *more* trustworthy; one that flips
was an artifact of D. **Risk: low — this can only make claims more honest.**

### Type B — Synthetic ground-truth variables (validity / power calibration)
Inject a *known, controlled* variable into synthetic or perturbed data where the
answer is known: planted anchors, drift-clustering level, block structure,
homophony degree, injected-meaning strength. **Hypothesis form:** "if the
manuscript had property P at level L, would our method detect it?" Calibrates what
the methods can and cannot see. **Risk: low — it is the harness logic.**

### Type C — Variables that could manufacture findings (the trap)
Introduce *many* variables, re-run *many* experiments, and hunt for "interesting
impacts." **You can always impact results by introducing variables.** The danger is
mistaking the impact *of the introduced variable* for a property *of the
manuscript* — the garden of forking paths, p-hacking, narrative overfitting. This
session's E4 is a live example: introducing `root_coloring` as a "clean feature"
produced an association that *looked* like a finding but may be a same-model-source
artifact (E4b tests it). **The framework exists to prevent Type C from wearing
Type A/B's clothing.**

## The framework: a variable introduction as a study unit

Each introduced variable is registered like a W6a matrix variant, with:

1. **Hypothesis narrative** (Tim's framing): the dimension, *why* it might matter,
   the *mechanism* by which it could move results, and the **predicted direction**
   — pre-registered before running (flag-don't-resolve → pre-registration).
2. **Type declaration:** A (representation) or B (synthetic). A bare Type C is not
   permitted; if a variable can't be cast as A or B, it doesn't run.
3. **The statistic that would move** (mandatory, as in the variant matrix).
4. **Harness-first validity check** (esp. Type B): confirm the pipeline responds
   correctly to the *known* version of the variable on synthetic data before
   interpreting its effect on the real manuscript.
5. **Multiple-testing accounting:** pre-register the variable *set*; FDR-correct
   across the family; grade **confirmatory** (pre-registered) vs **exploratory**
   (D-grade until independently replicated on held-out data or a fresh method).
6. **Adversarial refutation pass** (the standing i02 rule): every "variable X
   meaningfully changed result Y" claim gets a clean-context critic asking *"is the
   change an artifact of HOW you introduced X?"* — the exact question that has
   caught 4+ overclaims across i01/i02.

## Where it gets genuinely interesting (the fertile version)

The best variable introductions are ones where **the variable is a dimension of a
hypothesis about what the manuscript is.** Two high-value shapes:

- **Dose-response over the harness (the gem).** Instead of the false binary
  "meaningful vs meaningless," parameterize a generator along a *continuous*
  interpretable dimension (word-order-information level, homophony degree,
  morphological-paradigm strength, injected-meaning strength) and locate **where
  the VMS sits on that continuum** relative to known-meaningful and known-
  meaningless anchors. Turns yes/no into "how far along dimension D is the VMS" —
  more informative, less prone to false dichotomy. E1/E2 already started this
  (sweeping drift spread, homophony); generalize it into a **"VMS coordinate" in a
  space of interpretable generative dimensions.**
- **Assumption-relaxation variables** (the W6a leads, now as first-class studies):
  reading order, scribe/hand stratification, segmentation policy, section grouping.
  Each bears on a specific hypothesis (directionality, multi-author, spaces-aren't-
  boundaries, section-content-distinctness).

## Concrete near-term shape: a "sensitivity atlas" iteration (i03 candidate)

Organize an iteration entirely around Type A: systematically map how **every
headline finding** responds to **every representation variable** (transliteration ×
tokenization × section-grouping × subsetting), producing a **robustness matrix**.
Findings invariant across the atlas are the trustworthy core; findings that flip
are flagged and down-graded. Directly extends what we have; almost pure code; and
its output is exactly the kind of defensible, honest deliverable the program values
— "here is precisely how load-bearing each conclusion is to our representational
choices."

## The honest caveat to hold onto

More variables × more re-runs = more exploration, and exploration inflates false
positives and tempts narrative overfitting (finding the frame that makes the VMS
look special). The program's answer is already in hand: the **confirmatory/
exploratory split**, **independent replication before rising above grade D**, and
the **adversarial review** that has repeatedly caught the program's own overclaims.
Variable introduction is a *hypothesis-generation* engine (exploratory, D-grade by
default); anything it surfaces must be independently confirmed before it counts.

**Bottom line for Tim:** the idea is sound, tractable, and already half-built. Run
it as Types A and B only, each variable pre-registered with a hypothesis + a
statistic-that-moves + a refutation pass, graded exploratory-until-replicated. The
single most valuable first step is the dose-response "VMS coordinate" — it converts
the program's central open question (meaningful vs meaningless, which i02 showed no
single statistic can settle) into a *position on interpretable continua*, which is
both more honest and more likely to surface something new.
