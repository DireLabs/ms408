# T3.3 — Adversarial Review Critique Log

**Method (L10):** five clean-context critics received *only* a target claim plus
its raw numbers and method — never this session's synthesis reasoning — and were
instructed to refute. Each returned a verdict, objection, and resolving test.
Dispositions below are binding on the flagship (T3.2 → revised) and set the i02
follow-up agenda. **Outcome: the program's distinctive lean is downgraded; the
descriptive results and the harness/firewall method survive.** This is the P5
discipline functioning — it prevented a plausible-but-unsupported conclusion from
being published.

---

## C1 — "No encoding family reproduces the full profile" · verdict WEAKENED

**Objection (accepted).** The paradigmatic-conlang "win" is **circular**: that
variant was seeded with a VMS-derived affix inventory, so it fitted the target
rather than independently reproducing it — the identical MZ scale (812 vs 812) is
a tell of fitting. The z-distance metric double-counts collinear dimensions
(h1/h2, word length, ED1-network all co-move with morphology). The negative half
overreaches: only single-parameterization families were tested, and composed
encodings (cipher∘conlang) never were.

**Disposition.** ACCEPTED. The conlang is *not* an independent full-profile
match; drop that as support. Reframe the bracket result as "these five
single-parameterization families each miss one half" — not "no family can."

**i02 follow-up.** Equal VMS-informed tuning budget for all families on held-out
metrics; add composed families; bootstrap z-distances with CIs; cluster collinear
metrics.

---

## C2 — "Verbose cipher is contradicted by word-order information" · verdict WEAKENED

**Objection (accepted, two parts).**
1. The VMS ΔI = 0.307 is measured on **analyst-reordered-by-section** text, and
   the sections coincide with the Currier A/B split and quire-level vocabulary
   drift — so 0.307 may index scribe/dialect *blocking*, not plaintext word-order.
   The Naibbe cipher was a single homogeneous stream, never given analogous block
   structure: an asymmetric comparison. A multi-scribe / drifting-key cipher could
   regenerate block-scale ΔI.
2. **Mechanism mislabeled.** The type-*deterministic* verbose cipher (no
   homophony) still scored only 0.017–0.028 — so the word-order destruction comes
   from word-boundary/segmentation misalignment, **not homophony**. "Homophonic
   cipher erases word-order" attributes to homophony what is a tokenization
   effect.

**Disposition.** ACCEPTED. Reframe: the finding refutes a *uniform single-key*
verbose cipher and shows *verbose segmentation* (not homophony) disrupts
word-order; it does not contradict verbose substitution as a class.

**i02 follow-up.** Recompute ΔI on natural-folio-order VMS; build a
scribe-switching / drifting-key verbose cipher of heterogeneous Latin blocked like
the VMS; report ΔI of the exact Pliny plaintext used; publish the MZ estimator's
CI at VMS length.

---

## C3 — Narrative ranking logic (conlang > invented-world lean) · verdict WEAKENED→REFUTED

**Objection (accepted).** The grade-weighted tally **rewards unfalsifiability**:
invented-world's +10 is "little evidence *against*," banked as neutral-for-itself
while the same three nulls are spent as damage-to-herbal — asymmetric null
accounting (special pleading). Ranking two hypotheses declared "internally
indistinguishable" is self-refuting. "No detected mapping" does not license "no
referents exist" over "referents not recovered." Historical priors are omitted
where they hurt (a 15th-c. invented world of this scale is also near-unattested).
A simpler rival — **structured-but-meaningless ("grammar without meaning")** — is
under-weighted, wrongly folded into the hoax bucket.

**Disposition.** ACCEPTED. Retire the numeric #1/#2 ranking of the W7 equivalence
class. Treat nulls symmetrically. Add structured-meaningless as a first-class
rival. State outcome as "the data underdetermine a class of structured-symbolic
hypotheses" — never "no referents exist."

---

## C4 — Three anchor nulls ("no word→referent mapping") · verdict WEAKENED; (c) near-REFUTED

**Objection (accepted).** The planted control (φ=1.0 on many pages) proves the
harness can find a *perfect* signal — it is **not a power check** for realistic
effects, and power was never measured. Concretely: at 14,758 tests under BH-FDR,
the minimum detectable effect is ≈ near-perfect nesting on ≥10 pages; a
moderate anchor (φ≈0.45) falls below FDR and dies. The "testable" tokens are
frequency-filtered toward function-word-like tokens least likely to anchor.
Page-level granularity discards the word-next-to-organ adjacency where a real
label signal would live.
- **(c) root↔leaf near-REFUTED:** 35% root_type noise *attenuates* V toward null;
  disattenuating V=0.256 gives a true V≈0.37 (a moderate association masked by
  noise), and the clean `root_coloring` feature *did* associate with leaf
  features — buried affirmative evidence a noisy null cannot overturn.
- **(b) labels:** high-TTR/low-recurrence is *consistent with* a proper-noun
  naming system, not evidence against it; the running-text null band is inflated
  by function words. Wrong baseline.

**Disposition.** ACCEPTED. Downgrade all three from "no mapping detectable" to
"no *strong page-level* anchor at the achieved power." Flag root↔leaf as a
**possible masked positive** (follow the root_coloring→leaf hit), not a null. Drop
label (b) as evidence against naming — it may point the other way.

**i02 follow-up.** Publish a power curve (inject synthetic anchors at φ=0.3/0.4/0.5
on realistic page counts); restrict to mid-prevalence features; re-run at
line/label-adjacency granularity; third-annotator adjudication + disattenuation on
root_type; benchmark label recurrence against a real glossary with function words
stripped.

---

## C5 — Biggest hole (whole program) · the central lean rests on a self-built, self-tuned null

**Objection (accepted, load-bearing).** The distinctive claim — "meaning-bearing,
*not* a hoax" — comes from a *gap*: VMS MZ ≈ 0.31 vs the team's own reimplemented
self-citation generator scoring lower. But (i) MZ word-order information is a
**topic-clustering statistic, not a meaning detector** — any page-local
vocabulary drift produces it; (ii) the self-citation null's mechanism (copying
nearby tokens) is *precisely* what manufactures word-order correlation; (iii) only
**one** null was tested, at team-chosen tuning, knowing the target. That is
grading one's own null. The conlang match compounds it (reverse-engineered fit).

**What survives if it holds:** the replication gate (entropy, both Zipf laws, A/B,
MZ *reproduction*, positional effects — descriptive facts, grade A) and, partly,
the "unlike a simple labelled herbal" leg (on separate vision legs with their own
noise). **What dies:** the meaningful-vs-meaningless lean and the "not a hoax /
not an off-the-shelf cipher" verdict — these revert to "underdetermined."

**Disposition.** ACCEPTED as the governing revision. The meaningful-vs-meaningless
verdict is **NOT established**. It requires a blind, adversarially-optimized
self-citation null (red-team maximizes MZ while matching h2 + both Zipf slopes,
blind to the 0.31 target) that *still* falls short by more than the MZ CI. Until
then the honest statement is "we replicated known statistics and disfavored the
trivial explanations and the simplest referential-herbal reading."

---

## Net effect on grades

| Flagship claim | was | now | reason |
|---|---|---|---|
| Entropy anomaly; A/B; positional; replication | A | **A (stands)** | descriptive, gate-passed |
| VMS carries word-order information | B | **C** | reordering/blocking confound (C2), MZ not a meaning detector (C5) |
| Verbose cipher contradicted | B | **C** | single-key only; segmentation≠homophony (C2) |
| Self-citation weakened / "not a hoax" | B | **not established** | self-tuned single null (C5) |
| No family reproduces full profile | B | **C** | conlang circular; overreach (C1) |
| Three anchor nulls | B | **C** ("no strong page-level anchor") | underpowered (C4) |
| root↔leaf: no bundle | B | **withdrawn** — possible masked positive | noise attenuation + root_coloring hit (C4) |
| Conlang / invented-world lean | candidate B | **retired as a ranking** | unfalsifiability + circularity (C3, C1, C5) |

**Bottom line.** The envelope still shrank — the trivial explanations and the
simplest labelled-real-herbal reading are disfavored, and Voynichese is a genuine
constrained formal system with a real A/B split — but the program's *distinctive*
narrowing toward "invented language / invented-world notation" is **not
established** on the current evidence and is downgraded to an open,
underdetermined class. The five experiments above are the i02 agenda that would
settle it.
