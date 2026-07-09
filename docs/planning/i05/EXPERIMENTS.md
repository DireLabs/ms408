# i05 — Experiment Agenda (E13–E16): the mid-level linguistic layers

Four probes that build the grammar from the bottom up, each calibrated on real-
language + generator controls and stratified by Currier A/B. E13 leads (Tim's chosen
probe); E14–E16 extend upward and outward. A cross-cutting **A-vs-B grammar contrast**
is assembled from all four.

Common protocol for every probe: (1) define the measure; (2) compute it on H4 real
languages AND on the nulls/generators (self-citation, conlang, abjad, drift); (3) state
the calibrated decision rule (what value = "language-like" vs "generator-like"); (4)
compute on VMS-A and VMS-B (+ v101 sensitivity); (5) refutation pass; (6) grade.

---

## E13 — Function-word vs content-word bimodality [P1, flagship, Tim's lead probe]

**Question.** Real languages have a small set of very frequent **function words**
(the, of, and) that are *distributionally promiscuous* (occur in many contexts), plus
many **content words** that are topically clustered. Does Voynichese show this
bimodal grammar — and does it show it EQUALLY in A and B?

**Design.** For each word type compute frequency and a promiscuity measure — the
entropy / normalised diversity of its left+right neighbour distribution — controlling
for the frequency--diversity confound (compare at matched frequency, or use a
per-occurrence conditional neighbour entropy). Test for (a) **bimodality** in the
(frequency, promiscuity) structure (dip test / 2-component mixture), and (b) whether
the top-frequency band contains a distinct promiscuous class. Calibrate: real
languages should show a clear function-word class; a self-citation/conlang generator
should not (its high-frequency words are not specially promiscuous).

**Pass/fail.** If VMS shows the function/content bimodality that real languages show
and generators do not → strong evidence of **natural-language-like grammar** (candidate
B; reweights toward *language*, per L7 does not prove meaning). If uniform/generator-
like → consistent with a generative process. **A-vs-B:** if one dialect shows the
split and the other does not, that is direct evidence for Tim's "two different
processes" hypothesis.

---

## E14 — Distributional word-class (POS) induction [P2]

**Question.** Do coherent grammatical categories (noun/verb/adjective-like classes)
exist, and are they the same in A and B?

**Design.** Unsupervised word-class induction from neighbour distributions (Brown
clustering / HMM). Report the number of stable classes, their coherence (cluster
tightness vs a shuffled baseline), and class-transition regularities. Calibrate on
real languages (clean, few, coherent classes) vs generators (diffuse/unstable).
Cross-tabulate induced classes between A and B (do they align?).

**Pass/fail.** Coherent, stable, real-language-like class structure → grammar evidence
(B). Diffuse/unstable → generator-like. A/B class misalignment → different processes.

---

## E15 — Morphology segmentation & productivity [P2]

**Question.** Is the dense ED1 network (F12) a *productive, paradigmatic morphology*
(prefix/stem/suffix with real inflection-like paradigms) or decorative repetition —
and is it the same in A and B?

**Design.** Induce morpheme candidates from the ED1 network and Voynichese slot
structure (cf. Stolfi's prefix-midfix-suffix model); measure **productivity** (do
stems combine with a shared affix inventory across many lemmas?) and paradigm
coherence, against real-language morphology and against the abjad/conlang generators
(which produce *different* morphology signatures — E6 showed abjad reaches the ED1
band without paradigms).

**Pass/fail.** Productive, paradigmatic morphology like inflecting languages → B.
Non-productive / abjad-skeleton-like → reweights toward abbreviation/abjad. A/B
morphology divergence → different processes.

---

## E16 — Grammar depth: long-range / hierarchical dependency [P3]

**Question.** Does Voynichese structure exceed what a Markov / self-citation generator
produces — long-range agreement, non-adjacent dependencies, hierarchy?

**Design.** Compare the manuscript's predictability decay and non-adjacent mutual
information against fitted Markov models of matched order and against the self-citation
generator; test for dependencies beyond the generator's reach. Stratify A/B.

**Pass/fail.** Dependencies beyond Markov/self-citation → deeper grammar (B). Within
generator reach → consistent with local generation.

---

## Cross-cutting deliverable — the A-vs-B grammar contrast

Assemble E13–E16 into one statement: **do Currier A and B share a mid-level grammar,
or do they behave like different generative processes?** This directly adjudicates
Tim's hypothesis and is the headline i05 output. (L7: about grammar, not meaning.)
