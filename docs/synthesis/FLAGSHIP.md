# MS408 — Living Synthesis (W5 flagship)

**Status:** revised **post-i09** (experiments E1–E25 folded in). Grades A–D
(RESEARCH-PLAN §6); i01 numbers from `results/synthesis/findings_registry.json`,
i02–i09 numbers from `results/experiments/e{1..25}*.json` (L3 firewall). Living
document, not a final verdict. Every A/B result carries a clean-context refutation pass
(E21's first-pass B was overturned by one; the i08 negative was itself walked back by i09).

**i07 update (characterising the generative class, E21–E22).** i06 pointed to a
template/positional *generative* system; i07 tested that positive complement — can such
a generator, not tuned to Voynich, reproduce the *full* signature? The refutation-
hardened answer is an informative **negative [C]**: a context-free positional/template
grammar reproduces the VMS's low entropy, its block-scale ΔI, and (via block contrast)
its weak-but-**positive** word-class structure — but across a broad a-priori grid (E22,
64 configs) it **never** reproduces the VMS's morphology connectivity (ED1 ≈ 0.75; the
generator overshoots to ≈ 0.97), its lexical reuse (TTR ≈ 0.22; generator ≈ 0.59), or
its frequency slope, and no tuning reconciles them (the axes are structurally
unreachable). A control — real Latin word types under a context-free block wrapper —
lands in the VMS's *syntax* bands (fc_z −1.4 / wc_z 2.5), confirming that the VMS's weak
surface syntax is just what context-free block sampling of any lexicon produces. So
"template/positional generation" as a **bag-of-slots is only a PARTIAL account**; the
misses point to the next required ingredient — heavier **word reuse / a smaller
effective lexicon / correlated slots** (looping back to the self-citation/copying
family, now evidence-motivated, not circular). *Process note:* E21's first-pass "class
sufficiency [B]" was overturned by the refutation pass — its constants had been grid-
selected to hit the VMS bands (a fitted point, not an a-priori draw) and its
weak-syntax leg used a one-sided threshold a full shuffle also passes — and was
narrowed to this negative, which E22 then made decisive.

**i09 update (is the i08 coupling real? — E25).** The E22/E23 refutation warned that i08's
residual obstruction (morphology connectivity, ED1) might be an artifact of the slot
grammar, where ED1 is rigidly coupled to word length/branching and saturates near 1.0.
i09 tested this by making ED1 an **independent knob** — a large character space (85-glyph
alphabet, swept pool size) with a connected-core/isolate lexicon — and scoring **multi-
seed** (generator-side CI-overlap), not single-seed. The result **substantially deflates
i08**: once ED1 is a real knob, it **co-occurs** (CI-overlap) with block-ΔI, lexical reuse
AND frequency slope — which the small-pool families (E22–E24) never could, confirming
E24's ED1 ≈ 0.97 saturation was largely an artifact of the tiny character space. What
survives is a single, shallow, *principled* tension between **character entropy and
morphology connectivity**: low h2 needs a small effective character space (dense
edit-graph → high ED1), and enlarging it to lower ED1 raises h2. The (h2, ED1) frontier
passes near but not through the VMS box (h2 in-band → ED1 reaches 0.63 vs floor 0.74; ED1
in-band → h2 reaches 2.04 vs floor 2.11) — a ~0.05–0.11 near-miss, **not** the gross
incompatibility i08 reported, and plausibly crossable with word-length variance (indel
connectivity decouples ED1 from the character space). **Net:** the VMS's hard-axis
signature constrains the generative mechanism *far less* than i08 claimed; a positional +
decoupled type-lexicon generator comes within ~0.05–0.11 on all five hard axes at once.
The i08 "no generative family reproduces the signature" framing (paper v4 §4.7) is
**superseded** and should be softened in a v5. (Grade C; soft fc_z/wc_z not counted;
single word length; no identification — L7.)

**i08 update (word reuse and type-level concentration, E23–E24).** i07 named the missing
ingredient — frequency concentration. i08 tested two ways to add it, each an a-priori
sweep. **E23 (token reuse, 104 configs):** copy-from-history rescues every axis i07 could
never reach (ED1, TTR, Zipf) individually, but trades them against entropy/ΔI — the copy
rate that concentrates frequency deflates the character entropy and block-ΔI (ceiling
4/8). **E24 (type-level small lexicon, 144 configs):** concentrating frequency at the
*type* level instead **resolves that entropy-vs-reuse tension** — TTR now sits in-band
*jointly* with h2, which token-copying could never do — but leaves a residual coupling,
now centred on **morphology connectivity** (matching ED1 ≈ 0.75 forces a regime out of
band on entropy/reuse/frequency) plus a block-contrast trade-off (retained ΔI wants weak
contrast; a positive word-class z wants strong). **Net across i07–i08 (E21–E24):** across
the three generative families swept — context-free positional, +token-reuse, +type-level
small lexicon — **none reproduces the VMS's full 8-axis signature over the swept ranges**;
the summary statistics are mutually coupled in a way these mechanisms do not capture.
*Scope (from the E22/E23 clean-context refutation, applied throughout):* this is a
**coupling within bounded sweeps, not a proof of impossibility**; two of the eight axes
(fc_z/wc_z) are soft (2-point Currier-A/B ranges, not CIs, confounded with sectional
drift — the control reaches the "weak-positive" wc_z with no reuse); results are single-
seed. Robustness follow-ups: multi-seed + generator-side bootstrap; branching below the
grid floor; a type lexicon decoupled from the slot grammar.

**i06 update (cryptanalytic direction, E18–E20).** Turning to the decipherment
question, we asked whether the VMS could be a cipher of a real text — targeting the two
classes our own work had left non-excluded (deterministic-verbose/nomenclator, abjad/
abbreviation). Using the i05 mid-level syntax measures as new discriminators, the
answer is a strong, refutation-hardened **exclusion**: the VMS uniquely combines LOW
character entropy, RETAINED (block-scale) word-order ΔI, and WEAK word-level syntax — a
combination **no cipher of real prose produces**. Word-order-PRESERVING ciphers (abjad,
1:1 substitution, nomenclator) retain the source language's strong word-syntax the VMS
lacks (~10σ), and this holds across typologically diverse languages including **Hebrew,
a native abjad** (E19/E19b); the only surviving lead — a transposition cipher — gives
weak syntax but collapses the ΔI, so retained-ΔI and weak-syntax are mutually exclusive
under any such cipher (E20). This **closes the cipher-of-real-prose class** and, with
the E1/E2 result that the ΔI is block/section structure rather than word order, points
to a **template-driven / positional generative system, not an enciphered real text.** A
decipherment attack is, by our own evidence, low-yield. (E18 also documents that ~12%
of the foliated range is missing and the vocabulary is non-saturating — see
Limitations.)

**i05 update (the mid-level linguistic program, E13–E17).** i01–i04 showed the VMS is
strongly structured but that magnitude-of-structure statistics cannot reach meaning
(E9). i05 built the *mid-level* layers between structure and semantics — morphology,
word-classes, syntax — each **null-model-corrected** (a reusable framework that
z-scores every statistic against a matched null holding its nuisance parameters fixed,
after the first probes proved confounded) and stratified by Currier A/B. Two validated,
robustness-checked findings emerged, both scoped to *surface distributional* structure
(L7): (i) the VMS lacks the natural-language surface **content>function collocational
gap** — its content-band words carry only near-chance collocational selectivity and its
*most-frequent* words are the more collocational (template-like, the opposite of flat
function words), robust across band cutoffs (E13c/E13d); and (ii) the VMS has **weak
distributional word-class (POS) structure** — ~0.13–0.19× real language, robust across
clustering parameters (E14/E14b). A dedicated content-controlled A-vs-B study (E17)
then showed the apparent A/B difference in word-class structure is a **section/content
confound, not a dialect difference**: it vanishes within the herbal section (the only
one carrying both dialects). Net i05 thesis: **the VMS's structure lives below the word
(characters, morphology); its word-level syntactic structure is weak; and the two
Currier systems do not differ in mid-level grammar once content is controlled** — their
established difference (F2) is vocabulary, not grammar.

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
  raised h2 the wrong way). **i06 UPDATE — the abjad/cipher revival is now closed
  (E19/E20):** while an abjad reaches the ED1 network, the i05 mid-level syntax
  discriminators exclude it (and the whole cipher-of-real-prose class) on the JOINT
  signature — an abjad/substitution/nomenclator of any real language (including Hebrew,
  a native abjad) retains strong word-syntax the VMS lacks, and the ΔI+weak-syntax
  combination is unreachable by any cipher of real prose (§ i06 update). So the abjad
  was a live *structural-morphology* lead but is **excluded once word-syntax is added.**

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

- **template-driven / positional generation** (incl. structured-meaningless) — the
  best-supported class, but i07–i08 show it is INCOMPLETE as any simple generative model:
  it is the natural reading of the VMS's block/positional ΔI (E1/E2) + weak word-syntax
  (i05) + low entropy, and the only class NOT excluded by the i06 cipher analysis; a
  context-free positional generator reproduces those three but not (E22) the VMS's
  morphology connectivity, lexical reuse, or frequency slope *simultaneously* — but i09
  (E25) showed this apparent coupling was **largely an artifact**: with ED1 made an
  independent knob (large character space), a positional + decoupled type-lexicon generator
  comes **within ~0.05–0.11 on all five hard axes at once** (multi-seed), leaving only a
  shallow, principled **entropy↔connectivity** frontier near-miss. So the joint signature
  constrains the generative mechanism much less than i07–i08 first suggested; the
  best-supported class is a positional/template + type-lexicon generator, near-reproducing
  the hard-axis signature. E1/E9 also removed the statistics that had counted against
  structured-meaningless (they measure structure, not meaning);
- **cipher of a real text** (abjad / abbreviation / substitution / nomenclator /
  transposition) — **EXCLUDED by i06 (E19/E19b/E20)** on the joint signature: no such
  cipher of any real language reproduces the VMS's low-entropy + retained-ΔI +
  weak-word-syntax combination. The abjad E6 revived on morphology is excluded once
  word-syntax is added;
- **constructed language** (Lingua-Ignota class) — not a *distinguished* fit (E5/E8),
  not excluded, but must also explain the weak word-syntax (i05);
- **invented-world notation** (Codex-Seraphinianus class);
- a **meaningful-but-non-nomenclatural** natural text — weakened by i05/i06 (real prose,
  enciphered or not, carries strong word-syntax the VMS lacks); the one candidate
  *positive* thread (the root↔leaf visual bundle) is UNRESOLVED-underpowered (E12),
  pending a human panel, and is not carried as a live positive.

Not ranked. The evidence does not separate meaningful from meaningless, and cannot
license "no referents exist" over "referents not recovered by these methods." There
is currently **no confirmed positive referential signal** — the strongest candidate
dissolved into a measurement-ceiling UNRESOLVED (E12).

**i05 adds a layered constraint on WHERE the structure lives.** The VMS is strongly
structured at the character (entropy anomaly) and morphology (ED1 network) levels, but
its **word-level surface syntax is weak**: it lacks the natural-language content>function
collocational gap (content words carry only near-chance collocational selectivity, and
frequent words are template-like rather than flat function words; E13c/E13d), and its
distributional word-class structure is ~0.13–0.19× real language (E14/E14b). And the
two Currier systems do **not** differ in this mid-level grammar once content is
controlled (E17) — their difference is lexical (F2), not grammatical. This is
compatible with several of the unranked hypotheses (a verbose/abbreviatory cipher or a
template-driven generation process would both depress surface word-syntax while leaving
character/morphology structure intact) and is scoped strictly to *surface* distribution
(L7): it does not prove absence of an underlying grammar.

## 5. Origin (unchanged, grade C)

German/Alemannic iconographic gravity (crossbowman Sagittarius, cycle comparanda)
c. 1420s–1460s, in tension with the northern-Italian working premise (L1);
provenance documentary-solid only to 1637 (Baresch); Rudolf II purchase and Bacon
attribution grade D. Carried as rival localizations.

## 6. Iteration findings folded in → i09 agenda

**i03 (E6–E10):** E6 (verbose cipher excluded on ED1; abjad revived), E7 (no lexical
anchor at higher power), E8 (no family distinguished under whitening), E9 (no
structural statistic localizes meaning), E10 (root↔leaf reopened; E4b overturned).
**i04 (E11–E12):** E11 (root↔leaf survives palette-style control), E12 (independent-
lineage rater → the bundle is UNRESOLVED-underpowered; E10's positive claim withdrawn).
**i05 (E13–E17), the mid-level program:** the null-correction framework; E13c/E13d
(no natural-language surface content/function collocation gap; frequent words
template-like); E14/E14b (weak distributional word-class structure, ~0.13–0.19× real);
E17 (the A/B word-class difference is a content confound, not dialect).
**i06 (E18–E20), the cryptanalytic direction:** E18 (~12% of the foliated range
missing; non-saturating vocabulary); E19/E19b (no cipher of a real language matches the
VMS's joint signature; the exclusion is universal across typology incl. Hebrew abjad;
the "favours generation" positive was dropped as circular); E20 (the transposition lead
is closed — retained-ΔI and weak-syntax are mutually exclusive under any cipher of real
prose). Net: the cipher-of-real-prose class is EXCLUDED; template/positional generation
is favoured.
**i07 (E21–E22), characterising the generative class:** E21 (a positional/template
generator matches the VMS's entropy + block-ΔI + weak-positive syntax, but a first-pass
"class sufficiency [B]" was refuted — constants were grid-selected to the VMS, and the
weak-syntax leg used a shuffle-passable threshold — and narrowed to [C]); E22 (an
a-priori grid NEVER reproduces the VMS's morphology connectivity, lexical reuse, or
frequency slope; the context-free bag-of-slots is a PARTIAL account only). Net: template/
positional generation is favoured for entropy/ΔI/weak-syntax but is INSUFFICIENT as a
context-free model — the signature demands an added word-reuse / smaller-lexicon /
correlated-slot mechanism.
**i08 (E23–E24), adding frequency concentration:** token reuse (E23, 104 configs) rescues
ED1/TTR/Zipf individually but trades them against entropy/ΔI (ceiling 4/8); type-level
small-lexicon concentration (E24, 144 configs) resolves the entropy-vs-reuse tension (TTR
co-occurs with h2) but leaves a residual coupling on morphology connectivity (ED1).
**i09 (E25), is that coupling real?:** with ED1 made an independent knob (large char-space,
multi-seed CI-overlap), the coupling **largely dissolves** — ED1 co-occurs with ΔI/TTR/Zipf
— leaving only a shallow entropy↔connectivity frontier near-miss (~0.05–0.11). Net: the
i08 "no generative family" claim is deflated; a positional + decoupled type-lexicon
generator near-reproduces the hard-axis signature.

**i09 leads:**

0. **Human panel on the root↔leaf consensus subset** — the ONLY decisive test left
   for the visual bundle (E12); pre-register + power-analyse first.
0b. **Harden and extend the E21–E24 coupling result** — E24 resolved the entropy-vs-reuse
   tension (TTR co-occurs with h2) but left morphology connectivity (ED1) as the residual
   obstruction. Before the "no tested generative family reproduces the signature" headline
   can strengthen, the refutation's demands: (a) multi-seed + generator-side bootstrap to
   convert tight single-seed in/out calls (esp. ED1's ~0.03 band) into CI overlaps; (b) the
   untested corners — branching below the grid floor, steeper frequency laws crossed with
   reuse, and a type lexicon **decoupled** from the slot grammar so ED1 tunes independently
   of entropy/word-length; (c) put fc_z/wc_z on a proper null (they are soft 2-point ranges
   confounded with sectional drift). Still a class account, never identification (L7).
1. **A larger content-matched A-vs-B sample** — E17's within-herbal null is
   underpowered (Herbal-B ≈3.3k tokens); firm it up, and extend the mid-level probes
   (E16 long-range dependency; a cleaner-null morphology retry).
2. **Abjad/abbreviation joint-signature test:** does any single parameterization reach
   ED1≈0.80 **and** h2≈2.1 **and** the 812-scale ΔI **together** (E6 showed abjad
   overshoots ED1 and misses h2)? The abjad/abbreviatory reading is also consistent
   with i05's weak surface word-syntax.
3. **Exact-p graded anchor hunt** (E7's Mann–Whitney approx is anti-conservative);
   **retire the whitened bracket** (E8, ill-conditioned Σ); **extend the variable-
   introduction program with structured-meaningless endpoints** (E9/L35).

## 7. Methodological contribution (the most robust result)

Every statistic was computed by deterministic versioned code and validated on a
synthetic harness before touching real-manuscript claims. Across eight iterations
the clean-context refutation rule has caught **a dozen-plus** over-reads and silent
bugs before they were reported. i06/i07 give two clean recent examples. i06: E19's
first-pass "the VMS is favoured as a generation process" was rejected as **circular**
(the matching generator was the Voynich-tuned one), narrowing the claim to the robust
*negative* (the cipher-of-real-prose exclusion) — and the refutation's demanded control
(test the discriminator across typologically diverse languages) then *upgraded* that
exclusion to universal (E19b). i07: E21's first-pass "class sufficiency [B]" for the
favoured generative account was **overturned** — the refutation showed its constants had
been grid-selected to hit the VMS bands (a fitted point dressed as an a-priori draw, the
very move that made E19's positive circular) and that its weak-syntax leg used a
one-sided threshold a full order-shuffle also passes — and the corrected, band-honest
test (E22) turned an apparent positive into a precise **negative** (the context-free
generator is insufficient) that names the next mechanism — and then, one iteration later,
i09 (E25) **walked back that very negative**: the refutation's suspicion proved right, the
"coupling" was largely a slot-grammar artifact, and with connectivity decoupled the
generator near-reproduces the hard-axis signature. The pipeline overturns its own
negatives as readily as its positives. i05 added a reusable
**null-model-correction framework**: the first mid-level probes were confounded (by i05 added a reusable
**null-model-correction framework**: the first mid-level probes were confounded (by
type-token ratio, sample size, number of stems), and the harness-first discipline
refused a manuscript claim from each until the confound was corrected — four
inconclusive probes (E13/E13b raw function-content, E15/E15b morphology) that a
less-disciplined pipeline would have reported. When correction succeeded, refutation
still narrowed the result (E13c's "undifferentiated / no grammar" was corrected to a
precise *surface-collocation* claim by a band-decomposition check), self-caught an
over-read (E14's code flagged "A≠B, different processes" from a threshold-straddle,
which we down-weighted as noise), and — decisively — a dedicated content-controlled
study **overturned the resulting A/B difference as a section confound (E17), just as
E12 overturned E10**. i04's E12 is a textbook case: a first-pass "KILLED —
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
- [x] **i04 complete (E11–E12):** root↔leaf resolved to UNRESOLVED-underpowered.
- [x] **i05 complete (E13–E17):** mid-level program — null-correction framework; VMS
  lacks surface content/function collocation (E13c) and has weak word-class structure
  (E14); A/B don't differ in mid-level grammar once content is controlled (E17).
  Folded into paper v2.
- [x] **i06 complete (E18–E20):** cryptanalytic direction — the cipher-of-real-prose
  class is EXCLUDED (VMS uniquely combines low entropy + retained ΔI + weak word-syntax,
  which no cipher of real prose produces; universal across typology incl. Hebrew abjad);
  ~12% of the foliated range is missing (E18). Favours template/positional generation.
  Folded into paper v3.
- [x] **i07 complete (E21–E22):** characterising the generative class — a context-free
  positional/template generator matches the VMS's entropy + block-ΔI + weak-positive
  word-class structure, but across a broad a-priori grid NEVER its morphology
  connectivity (ED1), lexical reuse (TTR), or frequency slope (E22); the bag-of-slots is
  a PARTIAL account. E21's first-pass "class sufficiency [B]" was refuted (grid-selected
  constants + shuffle-passable syntax threshold) → [C].
- [x] **i08 complete (E23–E24):** adding frequency concentration — token reuse (E23)
  rescues ED1/TTR/Zipf individually but trades them against entropy/ΔI; type-level
  concentration (E24) resolves the entropy-vs-reuse tension (TTR co-occurs with h2) but
  leaves a residual coupling on morphology connectivity. Folded into paper v4. **Note:
  i08's strong "no generative family" claim was walked back by i09.**
- [x] **i09 in progress (E25):** the i08 coupling is largely a slot-grammar artifact —
  with ED1 an independent knob (large char-space, multi-seed), a positional + decoupled
  type-lexicon generator comes within ~0.05–0.11 on all five hard axes at once, leaving
  only a shallow entropy↔connectivity frontier near-miss. Supersedes v4 §4.7 (→ v5).
- [ ] i09/i10 open — E26 word-length variance (try to cross the h2↔ED1 frontier); multi-
  seed bootstrap of soft fc_z/wc_z; root↔leaf human panel; larger content-matched A/B.
