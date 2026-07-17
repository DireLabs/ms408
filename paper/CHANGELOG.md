# Paper changelog

## v1 — 2026-07-09
First preprint snapshot. Scope: iterations i01–i04 (experiments through E12).
Headline: constrained two-system script; meaning provably underdetermined by
structural statistics (E9); root↔leaf visual bundle resolved to UNRESOLVED-
underpowered (E12); harness + firewall + adversarial-refutation architecture as the
transferable contribution. All numbers firewall-sourced from results/. Future work:
human-panel root↔leaf adjudication, the i05 mid-level linguistic program (A/B),
abjad joint-signature test.

## v2 — 2026-07-14
Folds i05 (the mid-level linguistic program, E13–E17). Adds: the null-model-correction
framework to the Method; a Results subsection (§4.5) on mid-level structure — the VMS
lacks the natural-language surface content/function collocation gap (real langs z=19/8.5
vs VMS z=−1.3/−4.8) and has weak word-class structure (~0.13–0.19× real); and the A/B
mid-level difference is a content confound, not dialect (global B−A +1.79 reverses to
−1.24 within the herbal). Discussion adds the "structure below the word" thesis;
methodology adds E17 overturning the E14b A/B difference. All numbers firewall-sourced.
6pp. Future work updated (i05 done → human panel, larger A/B, E16, abjad joint-signature).

## v3 — 2026-07-15
Folds i06 (the discipline-gated cryptanalytic direction, E18–E20). Adds: a completeness
paragraph to Data (~12% of the foliated range lost, f1–f116, 14 missing folio numbers;
non-saturating vocabulary, Heaps β=0.73, ~20% new types/page in the final quartile —
E18); a new Results subsection (§4.6) EXCLUDING the cipher-of-real-prose class on the
joint signature — word-order-preserving ciphers keep the source language's strong
mid-level syntax (~10σ; abjad/subst/nomenclator fc_z 13.8/21.0/9.8), the exclusion is
language-universal (Latin/Italian/German/Hebrew all strong; Hebrew abjad fc_z 9.7/wc_z
4.1), and transposition cannot rescue it (retained ΔI and weak word-syntax are mutually
exclusive under reordering: latin_verbose ΔI 0.39/z 20 vs latin_verbose_transposed ΔI
0.01/z 0.83), pointing to a template-driven / positional generative system. Discussion
adds the ΔI/word-syntax paradox; methodology adds the E19→E19b circular-positive
narrowing-then-upgrade. Limitations add incompleteness + exclusion scope. Future work:
characterise the generator (non-Voynich-tuned). All numbers firewall-sourced. 8pp.

## v4 — 2026-07-15
Folds i07 (E21–E22) and i08 (E23–E24) — characterising and CONSTRAINING the favoured
generative class — and incorporates a clean-context refutation of the E22/E23 claims.
New Results subsection (§4.7): a non-Voynich-tuned positional/template generator
reproduces entropy (h2 2.14) + block-ΔI (0.08) + weak word-syntax but, across a 64-config
a-priori grid, not SIMULTANEOUSLY the VMS's morphology connectivity (ED1 ~0.75; generator
~0.97–1.0), lexical reuse (TTR ~0.22; ~0.59), or frequency slope (E22) — a COUPLING, not
an impossibility. Adding word reuse (E23, 104 configs) rescues those axes individually but
trades them against entropy/ΔI (ceiling 4/8). Type-level concentration (E24, 144 configs)
resolves the entropy-vs-reuse tension — TTR now co-occurs with h2 — but leaves a residual
coupling centred on morphology connectivity (ED1). Net across the three families: none
reproduces the full 8-axis signature over the swept ranges. Records the E21 B→C self-
correction. REFUTATION CORRECTIONS applied throughout: "structurally unreachable / any
generative family" → "coupling within swept ranges"; fc_z/wc_z flagged as 2-point dialect
ranges (not CIs) confounded with sectional drift (soft axes); 4/8 ceiling reported;
single-seed + fixed word-length/slot-count caveats added; Future Work → multi-seed +
decoupled type lexicon. All numbers firewall-sourced. 10pp.

## v5 — 2026-07-16
Folds i09 (E25–E26), which WALKS BACK v4's i08 "no generative family reproduces the
signature" negative. §4.7 retitled "an apparent constraint that dissolves": a
refutation-directed test made morphology connectivity (ED1) an INDEPENDENT control —
first via a larger character space (E25, multi-seed CI-overlap: ED1 co-occurs with
ΔI/TTR/Zipf; only a shallow entropy↔connectivity near-miss, ED1 0.63 at h2-in-band vs
floor 0.74), then via WORD-LENGTH VARIANCE (E26: ED1 lands in-band 0.76 jointly, residual
a ~0.03 h2 near-miss + a fixable mean-length construction artifact). So a positional +
skewed-type-lexicon generator reproduces ALL distributional hard axes to within ~0.03 —
the joint signature does NOT discriminate the generating mechanism; the load-bearing
constraints stay the i06 cipher exclusion + qualitative character/morphology structure.
Abstract, Discussion, methodology (adds the over-read-negative-then-walked-back episode),
Limitations, Future Work all updated; "nine iterations". Grade C throughout; soft
fc_z/wc_z not counted; L7. Compiles clean (10pp, 0 undefined cites, 0 overfull).

## v5b — 2026-07-16 (wording correction of v5, per clean-context refutation)
A refutation of v5 found the deflation directionally right but its headline over-stated.
Corrected throughout to the "honest middle": a RETRACTION of i08's hard constraint, NOT a
promotion to "no constraint." Fixes: (1) drop "reproduces ALL hard axes to within ~0.03" —
NO single config matches all axes in either experiment (E25 0/48, ceiling 4/5; E26 0/48,
ceiling 4/6, none at 5/6); the showcase config has TWO misses (h2 ~0.03 AND mean-length
~1.25), and "ED1 co-occurs with ΔI/TTR/Zipf" is a cross-config composite. (2) narrow "the
signature doesn't discriminate the mechanism" → "within this one generative family the hard
axes under-determine the sub-mechanism" and re-assert that the signature DOES discriminate
across classes (§4.6 cipher exclusion). (3) delete "fitting is easy/near-vacuous" —
contradicted by the 0% basin (fitting was hard and incomplete). (4) disclose the
scoring-method shift (single-seed hard → lenient multi-seed CI-overlap, not applied back to
i08; ~9–15% of matches median-out-of-band) and that the mean-length "artifact" is an
untested conjecture possibly = the same entropy/connectivity wall; ED1 target ~0.75 is a
10k-subsample value vs 0.80 full. Grade C stands for the deflation; the universal-quantifier
claims are removed. 11pp; compiles clean.

## methods/v1 — 2026-07-16 (standalone methods paper, separate from the envelope preprint)
"Adversarial Self-Correction for Computational Research on Undeciphered Corpora: A
Harness–Firewall–Refutation Architecture and Its Record" (paper/methods/, 8pp). Distinct
from the MS408 envelope preprint (v1–v5b): the case study is the program, but the claim is
the architecture. Sections: the problem (forking paths on ground-truth-free corpora; the
Indus Rao/Sproat archetype); the three coupled disciplines (harness, firewall, standing
clean-context refutation) + grades/decision-ledger; why each catches a distinct error class;
THE RECORD — a catalogued table of the program's own first-pass verdicts overturned before
publication (circular positives, fitted-to-target, missing-null false positives, confounds,
over-strong NEGATIVES walked back, and the recursive refutation of the walk-back itself);
relation to pre-registration / multiverse / adversarial collaboration / reproducible research;
reflexive limitations (n=1 program; over-refutation risk; the paper invites its own
refutation); an adoption checklist. Built on the shared template; refs extended (Ioannidis,
Simmons, Gelman/Loken, Steegen, Simonsohn, Nosek, Mellers, Sandve, Sproat, Rao). Compiles
clean (8pp, 0 undefined cites). gelman2013garden flagged % UNVERIFIED (exact venue/date).
NOT yet refutation-passed — which, per the paper's own §6, is the required next step.

## methods/v2 — 2026-07-17 (refutation-corrected methods paper)
A clean-context refutation of methods/v1 (archived: docs/refutations/2026-07-17-methods-paper.md)
verified every Table-1 number as accurate but found the inferential framing over-claimed.
v2 corrects it and — the P0 fix — the refutation briefs are now PRESERVED under the firewall
(docs/refutations/), closing the paper's own "no claim lives only in prose" doctrine against its
core evidence (partial: i06+ archived, earlier briefs documented only in FLAGSHIP §7, stated
honestly). Wording fixes: abstract drops causal "caught ... before they were reported" +
"practical route to defensible research" → record-language + "disciplined default worth adopting
and testing"; "bidirectional" softened (negatives resolved to NON-FINDINGS, not restored
positives — "declines to over-read a negative"); the recursive v5→v5b episode now states its
skeptical reading (three headlines on one question = possible instability) and concedes new
EXPERIMENTS, not the pass alone, adjudicated; "independent" qualified as context-independent only
(same model family/operator; cross-vendor E12 was a rater, not refuter; "analyst worst-placed" =
motivating hypothesis); §5 adds ML adversarial validation, Mayo severe-testing, red-teaming
(Perez 2022); §6 adds the missing denominator + partial-archive admission; transfer claim →
conjecture; E19b row notes the transposition gap. Refs +mayo2018severe, +perez2022red,
+rugg2004elegant. 9pp; compiles clean, 0 undefined cites. gelman2013garden + rugg2004elegant
remain % UNVERIFIED (exact venue/pages) — fix at submission.

## v6 — 2026-07-17 (i06 cipher exclusion RETRACTED; engages concurrent work)
Folds i11 (E29–E31), which RETRACTS v3–v5b's "cipher-of-real-prose EXCLUDED" headline after
engaging Michael Greshko's concurrent Naibbe cipher (Cryptologia 2025). §4.6 retitled
"Ciphers of real prose: word-order-preserving excluded, homophonic NOT":
- ROBUST (kept, firmed): word-order-preserving ciphers (subst/abjad/nomenclator) carry strong
  surface syntax the VMS lacks — language-universal, and ~30σ once the measure is DECONFOUNDED
  from topic drift (E31: within-block null; the VMS weak wc_z is real grammar, 1.98→1.97, not
  drift; block-bootstrap-with-replacement found INVALID for these measures).
- RETRACTED: the "entire class" claim leaned on a "retained-ΔI" leg now shown CONFOUNDED
  (E29) — real word-boundary Latin is IN the VMS ΔI band (0.076); ~82% of Naibbe's ΔI loss is
  from its RESPACING before the cipher; ΔI collapses under homophony alone with word order
  fixed. E30 (multi-seed, blocked word-boundary Latin): verbose+homophonic ciphers (≈ Naibbe)
  scatter at the edge of the joint-signature corner and CANNOT be excluded → the cipher
  hypothesis is viable, converging with Greshko + Parisel (arXiv:2604.19762).
Abstract, §4.7 opener, Discussion, methodology (adds "reversed a would-be favourable result
before it reached the cipher's author"), Limitations, Future Work all updated; "ten
iterations". Refs +greshko2025naibbe, +parisel2026layered. 11pp; compiles clean, 0 undefined
cites. NOTE: not yet put through a fresh refutation pass; paper/methods v2 also references the
(now-narrowed) cipher exclusion and should be updated to cite this retraction as its strongest
external-facing self-correction example.
