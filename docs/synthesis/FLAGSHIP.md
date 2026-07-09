# MS408 — Living Synthesis (W5 flagship)

**Status:** revised **post-i04** (experiments E1–E12 folded in). Grades A–D
(RESEARCH-PLAN §6); i01 numbers from `results/synthesis/findings_registry.json`,
i02–i04 numbers from `results/experiments/e{1..12}*.json` (L3 firewall). Living
document, not a final verdict. Every i02–i04 result carries a clean-context
refutation pass.

**i04 update (E11–E12):** the one live positive lead — the root↔leaf visual bundle
that i03/E10 reopened — was pursued to its measurement ceiling. It survived a palette-
style control (E11), but the cross-lineage independence test (E12: GPT-5.1, a non-
Anthropic rater) does not reproduce it, and a consensus-subset power analysis shows
the model-annotation approach is **underpowered/untestable** (the leaf feature is too
noisy, κ≈0.45 for every rater; the reliable subset is only ~74 pages). **E10's
"strongest positive candidate" claim is WITHDRAWN to UNRESOLVED** — neither confirmed
nor an artifact; a pre-registered human panel is the only decisive test, and adding
more models cannot help. §3/§4 below reflect this.

**Headline (honest, post-i03).** Voynichese is a genuine constrained formal system
with a real two-system (Currier A/B) structure and the well-known low-entropy
anomaly, all reproduced against published baselines. i02 sharpened the envelope by
subtraction; **i03 did two things at once**: it *further hardened* the negatives —
no encoding family is distinguished even under a whitened distance (E8), and **no
structural statistic localizes meaning at all** (E9, the deepest confirmation that
the meaningful-vs-meaningless question is underdetermined) — while it also produced
the program's **first surviving referential-signal candidate**: the cross-organ
root↔leaf visual bundle, which i02 had written off as an annotation artifact, was
**reopened** when a third independent model reproduced it and it survived scribal-
hand/dialect stratification (E10, unconfirmed). On encoding mechanism, i03 excluded
the *verbose* cipher on morphology-network grounds but **revived the abjad/
abbreviation class** as the one route that reaches the VMS's dense edit-distance-1
network (E6). The success criterion (defensibly shrink the envelope, every claim
graded) is **met**, and the self-correcting mechanism — which this iteration used to
overturn *its own prior conclusion* (E4b) and *its own code's* verdicts — remains
the most robust result.

---

## 1. What is established (survives i01 review, i02, i03)

- **[A] The conditional character-entropy anomaly is real and replicates.** h2 ≈
  **2.16** vs **3.23–3.91** for medieval natural-language controls; matches
  published values within thousandths of a bit, robust across dialect and hand (F1).
- **[A] Two statistically distinct systems (Currier A/B).** Cross-dialect vocabulary
  divergence JS **0.26** vs within-dialect **0.04–0.09** (F2).
- **[A] Strong positional grammar** (paragraph-initial gallows, line-final m,
  glyph-adjacency constraints) (F3).
- **[A] The replication gate passed** on every targeted published statistic (F1–F3,
  gate G1). Descriptive facts, independent of interpretation.
- **[B, candidate] A dense, position-constrained, paradigmatic morphology** —
  edit-distance-1 main component **0.80** vs **0.16–0.22** for Latin/Italian (F12).
  i03/E6
  adds a mechanism constraint: this network is **destroyed by verbose expansion** and
  is reachable only by a length-preserving script over an inventory that already has
  it (a constructed morphology, an abjad, or a paradigmatic conlang).

## 2. What is disfavoured (i03-refined)

- **[C] A text-level "naming system" for the herbal is disfavoured — and now on a
  tighter bound.** E3 showed the page-level anchor null excludes only strong,
  prevalence-balanced word→feature anchors. E7 pushed further: a *graded* (token-
  count) anchor hunt over the mid/rare-prevalence bands, at higher power, still finds
  **no anchor above chance** (18 raw BH "hits" collapse under the permuted-feature
  null, permutation p=0.48). And **label-adjacency anchoring is infeasible** on the
  herbal section (labels are page-unique). So there is no detectable *lexical* label→
  feature mapping. (L7: not proof none exists.)
- **[C→reopened] BUT the *visual* cross-organ bundle is NOT disfavoured — see §3
  (E10).** The "within-organ only / no real-taxa bundle" leg no longer holds.
- **[C] Verbose ciphers (homophonic AND deterministic) are disfavoured; the abjad/
  abbreviation class is REVIVED.** E2 killed the *homophone-rich* verbose cipher (ΔI
  collapses to 0.013). E6 adds the decisive morphology constraint: a *verbose*
  cipher (≥2 glyphs/letter) **deductively destroys** the ED1 network (Latin ED1 0.28
  at 1:1 → 0.001 verbose), so the deterministic-verbose family E2 had re-opened is
  excluded after all. What *does* reach the VMS's ED1≈0.80 is an **abjad of real
  Latin** (vowel-dropping → shared consonantal skeletons, ED1 0.90) — reviving the
  abjad/abbreviation class (Hauer-Kondrak / medieval brevigraphy) as the live
  structural route to the morphology network, in tension with i01's F7 (abbreviation
  raised h2 the wrong way). Whether any single abjad/abbreviation parameterization
  hits ED1 **and** h2 **and** ΔI together is the open i04 test.

## 3. What is NOT established (i02/i03 outcomes)

- **The meaningful-vs-meaningless verdict — OPEN, and i03 shows WHY it is hard.** E1
  showed ΔI is not a meaning detector (a meaningless drift-null reaches ΔI 2.20). E9
  generalized this decisively: building a meaningful↔meaningless *coordinate* on
  interpretable axes, **every VMS-computable statistic turns out to be a structure
  detector, not a meaning detector** — against *honest* structured-meaningless
  endpoints, the meaningless adversary **out-scores** meaningful text on every axis
  (word-order: drift-null ΔI 0.57 > Latin 0.36; morphology: abjad ED1 0.89 > conlang
  0.87) and the VMS sits **below both**. So the VMS is maximally structured on every
  axis we can measure, yet no axis separates meaning. **Underdetermined, and provably
  so with current statistics.**
- **No encoding family is distinguished — confirmed under a whitened distance (E8).**
  E5 (cluster-vote) and E8 (Mahalanobis whitening) agree: no family is robustly
  closest (best P(closest) < 0.9 under any distance). E8's whitened ranking is itself
  a **regularization artifact** (Σ condition number 10,062; the top family flips
  across ridge/leave-one-out), which only reinforces that the bracket is a
  **descriptive compatibility ordering**, not evidence for any family. The i01
  "constructed-language best fit" stays **withdrawn**.
- **[C, UNRESOLVED-underpowered] The root↔leaf visual bundle — reopened (E10), then
  found UNTESTABLE by model annotation (E12).** The arc: E4b called it a Sonnet-
  specific artifact; E10 overturned that (Haiku reproduced it across other models'
  leaf labels; it survived hand + dialect); E11 survived a palette-style control. But
  E12 added GPT-5.1 (a genuinely non-Anthropic rater whose root labels agree 0.86–0.91
  with the Anthropic models) and it does **not** reproduce the association — every
  gpt_root×anthropic_leaf pairing is null (p 0.5–0.97). Crucially, the decisive tell
  is not root agreement but the **cross-rater nulls**: a real cross-organ property
  should survive pairing one rater's root with another's leaf, and it does not. Yet no
  firm negative is licensed either: **leaf_arrangement is noisy for every rater
  (κ≈0.44–0.53)**, the high-confidence consensus subset (≥3 raters agree on both
  organs) is only **74 pages** with minimum detectable φ≈0.33 — underpowered for the
  ~0.28 effect (where reliable, the association is ~nil: V=0.19, p=0.63). **Terminal
  status: too noisy for model annotation to adjudicate; E10's positive claim is
  WITHDRAWN to UNRESOLVED.** The E4b→E10→E12 sequence was partly narrative-fitting to
  the last-added model — a caution the program now records. The single decisive test
  is a **pre-registered 3-human panel** on the consensus subset (power reported
  first); more models cannot settle a noise-limited question. Visual only; no
  plaintext claim (L7).

## 4. The honest constraint envelope (post-i03)

**The manuscript is a genuine, constrained, two-system formal script whose
morphology network requires a length-preserving script over an already-structured
inventory. It disfavours (a) random/meaningless marks, (b) a *lexical* label→feature
naming system for the herbal (no text anchor at achieved power), and (c) verbose
ciphers (homophonic or deterministic). The remaining hypotheses are unranked:**

- **structured-meaningless** — still the simplest fit; E1/E9 removed the statistics
  that had counted against it (they measure structure, not meaning);
- **abjad / abbreviation** of a real language — REVIVED by E6 as the route that
  reaches the ED1 network (pending the joint-signature test);
- **constructed language** (Lingua-Ignota class) — not a *distinguished* fit (E5/E8),
  not excluded;
- **invented-world notation** (Codex-Seraphinianus class);
- a **meaningful-but-non-nomenclatural** natural text — kept open on the Language-A
  section↔text co-variation (F8) and E3's unexcluded weak/rare anchors. The one
  candidate *positive* thread (the root↔leaf visual bundle) was pursued in i04 and is
  now **UNRESOLVED-underpowered** (E12) — too noisy for model annotation to settle,
  pending a human panel; it is no longer carried as a live positive.

Not ranked. The evidence does not separate meaningful from meaningless, and cannot
license "no referents exist" over "referents not recovered by these methods." There
is currently **no confirmed positive referential signal** — the strongest candidate
dissolved into a measurement-ceiling UNRESOLVED (E12).

## 5. Origin (unchanged, grade C)

German/Alemannic iconographic gravity (crossbowman Sagittarius, cycle comparanda)
c. 1420s–1460s, in tension with the northern-Italian working premise (L1);
provenance documentary-solid only to 1637 (Baresch); Rudolf II purchase and Bacon
attribution grade D. Carried as rival localizations.

## 6. i03 findings → i04 agenda

**i03 folded in (E6–E10, each refutation-passed):** E6 (verbose cipher excluded on
ED1; abjad revived), E7 (no lexical anchor at higher power; labels infeasible), E8
(no family distinguished under whitening; ranking is a regularization artifact), E9
(no structural statistic localizes meaning), E10 (root↔leaf reopened; E4b overturned;
unconfirmed).

**i04 folded in (E11–E12):** E11 (root↔leaf survives palette-style control), E12
(independent-lineage rater GPT-5.1 → the bundle is UNRESOLVED-underpowered; model
annotation can't adjudicate; E10's positive claim withdrawn).

**i05+ leads:**

0. **Human panel on the root↔leaf consensus subset** — the ONLY decisive test left
   for the visual bundle (E12); pre-register + power-analyse first; if underpowered,
   declare it untestable by this design. More models cannot help.
1. **The mid-level linguistic program (i05, L37):** morphology segmentation,
   distributional word-class/POS induction, function-vs-content bimodality (lead
   probe), syntactic dependency — with Currier A/B as the primary stratification
   ("is one dialect a different generative process?"). The main forward thrust.
2. **Abjad/abbreviation joint-signature test:** does any single abjad/brevigraphy
   parameterization of a real language reach ED1≈0.80 **and** h2≈2.1 **and** the
   812-scale ΔI **together** (E6 showed abjad overshoots ED1 and misses h2)?
3. **Exact-p graded anchor hunt:** E7's Mann–Whitney normal approx is anti-
   conservative on sparse counts; an exact/permutation per-test p would let the
   higher-power anchor hunt make a *positive* claim, not just a null.
4. **Retire the whitened-bracket approach (E8):** Σ is ill-conditioned; a family-
   distinction claim needs a fundamentally better estimator or a larger corpus, not
   more whitening.
5. **Extend the variable-introduction program (L35):** E9 showed honest axes need a
   *structured-meaningless* endpoint; the next coordinate studies should be built
   that way from the start.

## 7. Methodological contribution (the most robust result)

Every statistic was computed by deterministic versioned code and validated on a
synthetic harness before touching real-manuscript claims. Across four iterations
the clean-context refutation rule has caught **a dozen-plus** over-reads and silent
bugs before they were reported. i04's E12 is a textbook case: a first-pass "KILLED —
rater-idiosyncratic" verdict was itself corrected by the refutation pass, which showed
the kill's central argument (root-label agreement) was a red herring and the honest
status is UNRESOLVED-underpowered — the pipeline declining to over-read a negative just
as it declines to over-read a positive. i03: E6's "needs constructed morphology" (refuted
by the abjad control the critic demanded), E7's **18 false-positive anchors** (caught
by the mandatory null gate — an anti-conservative test that BH-FDR did not control),
E8's "whitening confirms E5" (withdrawn once Σ was shown ill-conditioned) plus a
verdict-logic bug, E9's **two broken axes and a trivial-endpoint artifact** that
forced retraction of a *pre-registered commitment*, and E10 **overturning the
program's own prior E4b verdict** while surfacing (and fixing) an **L8 stratification
violation**. The architecture — capable of overturning its own code's conclusions
and its own prior iteration's verdict — is the differentiator versus prior AI
attempts and is publishable independently of any Voynich finding. No plausible-
sounding translation was ever generated.

---

## Gate sign-offs

- [x] G4 — post-T3.3 revised synthesis accepted; i02 agenda approved (L34).
- [x] **G5 — post-i02/i03 synthesis accepted as honest (Tim, 2026-07-09).** E1–E10
  folded in; all findings agreed. L37.
- [x] **i04 complete (E11–E12):** root↔leaf resolved to UNRESOLVED-underpowered; this
  is the intended end-of-scope for the first paper (anything past here = future work).
- [ ] i05 — the mid-level linguistic program with A/B stratification (L37).
