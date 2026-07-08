# MS408 — Living Synthesis (W5 flagship)

**Status:** revised **post-i02** (experiments E1–E5 folded in; supersedes the
post-T3.3 draft). Grades A–D (RESEARCH-PLAN §6); i01 numbers from
`results/synthesis/findings_registry.json`, i02 numbers from
`results/experiments/e{1..5}*.json` (L3 firewall). Living document, not a final
verdict. Every i02 result carries a clean-context refutation pass.

**Headline (honest, post-i02).** Voynichese is a genuine constrained formal
system with a real two-system (Currier A/B) structure and the well-known
low-entropy anomaly, all reproduced against published baselines. i02 **sharpened
the envelope by subtraction, not by adding a positive lean**: it showed the
word-order signal that once looked like a meaning fingerprint is a **block-structure
statistic** (E1, E2), it **re-opened** the deterministic/nomenclator cipher family
that i01 had leaned against (E2), it **weakened** the anti-"labelled-herbal" anchor
null to a narrow bound (E3), it resolved the root↔leaf "masked positive" as an
**annotation artifact** rather than a manuscript bundle (E4/E4b), and it **withdrew**
the "constructed-language best fit" claim entirely: under fair, equal tuning **no
encoding family is distinguished** (E5). The meaningful-vs-meaningless question
remains **open and underdetermined**. The success criterion (defensibly shrink the
envelope, every claim graded) is **met in a narrower, more honest form** — and the
mechanism that produced these corrections (harness + firewall + clean-context
adversarial review) is the program's most robust result.

---

## 1. What is established (survives i01 review and i02)

- **[A] The conditional character-entropy anomaly is real and replicates.** h2 ≈
  **2.16** for the manuscript vs **3.23–3.91** for medieval natural-language
  controls; matches published values within thousandths of a bit, robust across
  dialect and scribal hand (F1, gate G1).
- **[A] Two statistically distinct systems (Currier A/B).** Cross-dialect
  vocabulary divergence JS **0.26** vs within-dialect **0.04–0.09** (F2).
- **[A] Strong positional grammar.** Paragraph-initial gallows enrichment, line as
  a functional unit (line-final m), glyph-adjacency constraints — all replicate
  (F3).
- **[A] The replication gate passed** on every targeted published statistic (h2,
  both Zipf laws, A/B split, Montemurro–Zanette *reproduction*, positional
  effects). Descriptive facts, independent of interpretation.
- **[B, candidate] Voynichese is a dense, position-constrained, paradigmatic
  morphology** unlike natural-language controls at matched size (edit-distance-1
  main component **0.80** vs **0.16–0.22** for Latin/Italian) (F12).

## 2. What is disfavoured (i02-refined)

- **[C] The simplest "labelled herbal of real plants" reading is disfavoured — but
  only at the strong-signal corner.** E3's power curve makes the bound precise:
  synthetic anchor recovery is a **cliff** — φ≤0.3 → **0%**, φ=0.4 → **85%** — and
  is prevalence-dependent (rare features **0.72**, balanced **1.0**). So the i01
  anchor null excludes only **strong, prevalence-balanced** word→feature anchors; a
  **weak or rare-feature** anchor (φ 0.2–0.35), which an imperfect real-herbal
  encoding would most plausibly produce, is **not excluded**. This is a weaker
  constraint than the i01 draft implied.
- **[C] Heavy-homophony (Naibbe-class) verbose cipher is disfavoured — but the
  cipher family is otherwise RE-OPENED.** E2 is decisive here: a heavy-homophony
  verbose cipher of blocked text **collapses** the word-order signal (ΔI **0.013**),
  but a **type-preserving deterministic** verbose cipher of the *same* text
  **retains** it (ΔI **0.356**). The VMS's intact ΔI therefore argues only against
  *homophone-rich* ciphers; **deterministic-verbose / nomenclator / syllabary
  ciphers are consistent with it** and are back on the table — a reversal of the
  i01 lean.
- **[C] Abbreviation / abjad families are disfavoured** — they move h2 the wrong
  direction (≈3.5 vs 2.1) (F7); unaffected by i02.

## 3. What is NOT established (i02 outcomes)

- **The meaningful-vs-meaningless verdict — remains OPEN, now on firmer footing.**
  E1 shows the Montemurro–Zanette ΔI is **not a meaning detector**: a drift-null
  with no meaning reproduces the ΔI *value* (mean ΔI **2.20**, but at a mismatched
  scale). E2 completes the picture — the VMS signal is **intrinsic, not an
  analyst-reordering artifact** (natural-order ΔI **0.306** ≈ reordered **0.307**),
  a **meaningless block stream reaches ΔI 2.18**, and the characteristic
  **812-token scale is the section-block scale** — so ΔI tracks **block structure**,
  not meaning. Net: the word-order story is *resolved* — it is real
  structure but **not evidence of meaning**. The meaningful-vs-meaningless question
  is not settled by any single statistic in hand (this was C5, now demonstrated).
- **The invented-language / constructed-language narrowing — WITHDRAWN (E5).** The
  i01 "conlang best fit" was retired on review grounds (circular VMS-informed
  template, C1); E5 now settles it empirically. Under **equal tuning budget,
  held-out scoring, de-collinearised metrics, composed families, and bootstrap
  CIs**, **no family is robustly distinguished**: conlang_relex leads by point
  estimate but wins only **10%** of bootstraps; the modal winner (self-citation,
  **71%**) is a **single-metric artifact** — dropping `repetition_rate` (which its
  copy mechanism inflates) collapses it to **24%**. The encoding bracket is a
  **descriptive compatibility ordering, not evidence for any one family.**
- **"No real-taxa root↔leaf bundle" / the E4 masked positive — RESOLVED as an
  annotation artifact (E4b).** The clean root_coloring↔leaf_arrangement association
  (Cramér's V **0.395**) does **not** survive independent re-annotation: with a
  second vision model, only pairings containing the *original* model's root label
  are significant, the within-second-model replication fails (V 0.214, p 0.14)
  despite **83%** root agreement, and the effect vanishes when the concordant
  second-model root is substituted. The association tracks **one model's labelling**,
  not the manuscript. i01's "within-organ only" leg **holds (weakened, not
  overturned)**; a masked *manuscript* positive is not established.

## 4. The honest constraint envelope (post-i02)

Per P6, a competing-narratives statement with symmetric treatment of nulls:

**The manuscript is a genuine, constrained, two-system formal script that
disfavours (a) random/meaningless marks, (b) a plain labelled catalogue of real
plants *with strong balanced anchors*, and (c) a *homophone-rich* verbose cipher —
while the data underdetermine the remaining class of structured-symbolic
hypotheses, none of which the encoding bracket can rank:**

- **structured-meaningless** ("grammar without recoverable meaning"): still the
  simplest hypothesis consistent with all findings; E1's block-structure result
  removes the main statistic that had counted against it;
- **cipher** of a real text — specifically a **deterministic-verbose / nomenclator**
  variant (E2 re-opened this; the homophone-rich Naibbe form stays disfavoured);
- **constructed language** (a-priori, Lingua-Ignota class) — no longer a
  *distinguished* fit (E5), but not excluded;
- **invented-world notation** (Codex-Seraphinianus class);
- a **meaningful-but-non-nomenclatural** natural text, kept open by the Language-A
  section↔text co-variation (ARI **0.35**, F8) and by E3's unexcluded weak/rare
  anchors.

These are **not ranked**. The evidence does not separate meaningful from
meaningless within this class, and cannot license "no referents exist" over
"referents not recovered by these methods."

## 5. Origin (unchanged, grade C)

German/Alemannic iconographic gravity (crossbowman Sagittarius, cycle comparanda)
c. 1420s–1460s, in tension with the northern-Italian working premise (L1);
provenance documentary-solid only to 1637 (Baresch); Rudolf II purchase and Bacon
attribution grade D. Carried as rival localizations.

## 6. i02 findings → i03 agenda

**i02 folded in (all five complete, each refutation-passed):** E1 (ΔI is
block-structure, not meaning), E2 (word-order intrinsic; homophony collapses ΔI but
deterministic verbose retains it), E3 (anchor null is a narrow strong-balanced
bound), E4/E4b (root↔leaf is an annotation artifact), E5 (no encoding family
distinguished under fair tuning).

**i03 leads (surfaced by the i02 refutation passes, not yet run):**

1. **Deterministic-verbose / nomenclator cipher, blocked like the VMS** — the
   cipher variant E2 re-opened; does it reproduce h2 **and** the 812-scale ΔI
   **and** the ED1 morphology network together?
2. **Anchor hunt at finer granularity** (line / label-adjacency) and restricted to
   the weak/rare-feature regime E3 left unexcluded.
3. **Whitened bracket distance** (Mahalanobis/PCA on the empirical metric
   covariance) + **continuous tuning** past the grid edges where families railed —
   the principled fix for E5's residual collinearity and unequal tuning *power*.
4. **Human-in-the-loop root_coloring rater** — the one control that would settle
   the root↔leaf question E4b left as a model-labelling artifact.
5. **Controlled variable-introduction studies** (see
   `docs/planning/CONCEPT-variable-introduction.md`): the dose-response "VMS
   coordinate" — locate the manuscript on continuous meaningful↔meaningless axes
   rather than forcing the binary that E1/E5 showed no single statistic can settle.

## 7. Methodological contribution (the most robust result)

Every statistic was computed by deterministic versioned code and validated on a
synthetic ground-truth harness before touching real-manuscript claims. i02
extended the record: the refutation rule caught **five** further over-reads before
they were reported — E1's drift-null (withdrew a "meaning certificate" claim), E2's
anti-cipher point (corrected homophony-vs-determinism), E3's "null is informative"
oversell, **E4b's own coded verdict** (the analysis script asserted "bundle
confirmed"; the refutation pass rejected it), and E5's self-citation over-read — plus
**two silent methodology bugs** (a block bootstrap that destroyed the 812-scale
signal, flagged by a point-in-CI guard; a disjunctive confirmation rule that doubled
the false-positive rate). No plausible-sounding translation was ever generated. The
harness + firewall + adversarial-review architecture — capable of overturning the
program's *own code's* stated conclusion — is the differentiator versus prior AI
attempts and is publishable independently of any Voynich finding.

---

## Gate sign-offs

- [x] G4 — post-T3.3 revised synthesis accepted; i02 agenda approved (L34).
- [ ] **G5 — post-i02 synthesis accepted as honest (Tim).** E1–E5 folded in;
  i03 agenda proposed above.
- [ ] i03 agenda approved as the next iteration.
