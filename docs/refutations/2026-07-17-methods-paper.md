# Refutation — the methods paper (`paper/methods/`), 2026-07-17

_Clean-context adversarial pass. Target: "Adversarial Self-Correction for Computational
Research on Undeciphered Corpora." Refuter: fresh-context agent (same model family), read
access to the repo, no analyst narrative._

## Verdict

**The record (Table 1 / §4) is factually accurate — no fabricated or materially mis-stated
number; every quantitative claim traces cleanly to the firewall JSONs.** But the paper's
**central inferential claims are over-stated as written**: the leap from "our record contains
~12 overturns" to "the architecture *works*, is *transferable*, catches errors
*bidirectionally*" is not earned. A corrected v2 is warranted; fixes are mostly wording/scoping
plus one artifact-preservation task.

**Deepest internal inconsistency:** the mechanism the paper credits ("the refuter caught it",
every Table-1 "what caught it" cell) is **not preserved anywhere under the firewall** — no
saved briefs, no versioned refuter output. A paper whose ethos is "no claim that lives only in
prose" rested its own empirical core on prose-only attributions. (This archive is the fix.)

## Table 1 accuracy audit — all entries verified accurate against the JSONs

E19 circular positive (`generation_process_matches:["gen_self_citation"]`), E21 fitted point
(`constants_were_grid_selected_against_vms:true`), E7 "18 anchors / p≈0.48"
(`raw_discoveries:18`, `permutation_p_of_count:0.48`, `net_discoveries:0`), E6 abjad refutation,
E8 ill-conditioned Σ (`sigma_condition_number:10062`), E9 retracted pre-registered commitment,
E14→E17 confound (global B−A +1.79 → within-herbal −1.24), E12 KILLED→unresolved, i08→i09
artifact, recursive v5→v5b (`basin_all_core5:0.0`), E19→E19b universal — **all accurate.**
Caveat: the E19→E19b row is *selective* — E19b also opened the transposition gap
(`cipher_order_scramble_latin` fc_z 2.19) that E20 had to close; the row reports the
strengthening and omits the simultaneous new gap.

## Where the paper over-claims (accepted fixes)

1. **n=1, no counterfactual, "before they were reported" is loose.** No denominator (how many
   first-pass claims total; method false-negatives?). And the i08 negative was the **headline of
   released preprint v4**; v5 shipped the walk-back; v5b corrected v5 — so over-reads were
   corrected **across preprint versions**, not silently pre-report. §4's "before they reached a
   reader" contradicts the program's own CHANGELOG.
2. **Refutation record prose-only** (deepest point, above).
3. **"Bidirectional / recursive" is the shakiest, not the strongest, claim.** Neither negative
   was overturned to a *positive*: root↔leaf KILLED→**UNRESOLVED** (non-finding); generative
   "no family"→**within-family under-determination** (softened, not restored). So "overturns
   negatives as readily as positives" overstates the symmetry — the honest statement is
   "declines to over-read negatives just as positives." The recursive v5→v5b episode has an
   equally-supported skeptical reading: "three headlines on one question in ~48h = instability,
   not virtuosity," and what actually **adjudicated** was *new computation* (E25/E26), not the
   refutation pass — the paper conflates "ran the pass" with "ran more experiments" (exactly the
   confound §6 admits it can't rule out). Address head-on.
4. **"Independent skeptic" carries unearned model-/operator-independence.** Context-independent
   only; same family, same operator, same repo; the only cross-vendor check (E12) was a *rater*,
   not a *refuter*. "The analyst is worst-placed to destroy it" is a *motivating hypothesis*,
   not a finding.
5. **Over-generalisation** from one corpus/operator/model family to "undeciphered corpora"
   broadly and "any ground-truth-free corpus" — conjecture, not earned.
6. **§5 prior-art gaps:** ML **"adversarial validation"** (the paper's keyword #1! and ≈ what the
   harness does — separate real positives from matched negatives) is uncited; **Mayo
   severe-testing / error-statistics** is the closest philosophical precedent and is absent; AI
   red-teaming gestured at but uncited.
7. **Abstract confidence vs §6 hedges** — "**caught** a dozen-plus … a **practical route to
   defensible research**" asserts causation §6 disclaims. `gelman2013garden` still `% UNVERIFIED`.

## Strongest honest version of the thesis (refuter's wording)

> Over a ten-iteration, single-operator program on the Voynich Manuscript we imposed three
> disciplines — a synthetic harness, a code-only firewall, a standing clean-context LLM
> refutation pass — and document a versioned record in which ~a dozen first-pass conclusions
> (several asserted by the analysis code itself, two of them *negatives*) were narrowed,
> withdrawn, or retracted-then-partially-restored before the program's final synthesis. We
> cannot show these would have been published without the discipline (no counterfactual; n=1;
> same-family refuter; briefs not [previously] preserved), and in the recursive case the
> adjudication came partly from new experiments rather than the pass alone. We therefore offer
> the architecture as a *disciplined default worth adopting and testing*, not a demonstrated
> cure — its most verifiable output is the firewall, and its most novel *behaviour* is the
> willingness to soften its own negatives to "unresolved" rather than over-read them.

## Prioritised fixes → v2
P0: preserve the briefs (this archive) + abstract to record-language, import §6 hedges, drop
"practical route." P1: §4 concede the skeptical reading of i08→i09→v5b + that new experiments
adjudicated; "declines to over-read negatives" not "overturns as readily"; §5 add ML adversarial
validation + Mayo severe-testing + red-teaming cite; §2.3 qualify "independent"; E19b row note the
transposition gap. P2: fix gelman ref; soften transfer to conjecture; state the missing denominator.
