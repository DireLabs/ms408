# MS408 — Living Synthesis (W5 flagship)

**Status:** revised post-T3.3 adversarial review (see `T33-critique-log.md`).
Draft for G4. Grades A–D (RESEARCH-PLAN §6); numbers cited from
`results/synthesis/findings_registry.json`, which pulls them from `results/*.json`
(L3 firewall). This is a *living* document, not a final verdict.

**Headline (honest, post-review).** Voynichese is a genuine constrained formal
system with a real two-system (Currier A/B) structure and the well-known
low-entropy anomaly, all reproduced against published baselines. Beyond that, the
program **disfavours the trivial explanations and the simplest "labelled herbal of
real plants" reading**, but — after adversarial review — it **does not establish**
the distinctive narrowing toward "invented language / invented-world notation"
that an earlier draft leaned to. The meaningful-vs-meaningless question remains
**open and underdetermined**. The success criterion (defensibly shrink the
envelope, every claim graded) is **met in a narrower, more honest form than first
drafted** — and the mechanism that produced this correction (harness + firewall +
clean-context adversarial review) is itself the program's most robust result.

---

## 1. What is established (survives adversarial review)

- **[A] The conditional character-entropy anomaly is real and replicates.** h2 ≈
  **2.16** for the manuscript vs **3.23–3.91** for medieval natural-language
  controls; matches published values within thousandths of a bit, robust across
  dialect and scribal hand (F1, gate G1).
- **[A] Two statistically distinct systems (Currier A/B).** Cross-dialect
  vocabulary divergence JS **0.26** vs within-dialect **0.04–0.09**; the A/B split
  is the strongest structure recoverable from word co-occurrence alone (F2).
- **[A] Strong positional grammar.** Paragraph-initial gallows enrichment, line as
  a functional unit (line-final m), glyph-adjacency constraints — all replicate
  (F3).
- **[A] The replication gate passed** on every targeted published statistic (h2,
  both Zipf laws, A/B split, Montemurro–Zanette *reproduction*, positional
  effects). These are descriptive facts and stand independently of any
  interpretation.
- **[B, candidate] Voynichese is a dense, position-constrained, paradigmatic
  morphology** unlike natural-language controls at matched size (edit-distance-1
  main component **0.80** vs **0.16–0.22** for Latin/Italian) (F12).

## 2. What is disfavoured (weakened but directional)

- **[C] The simplest "labelled herbal of real plants" reading is disfavoured** —
  but on *underpowered* evidence, so the claim is now "no **strong page-level**
  word→feature anchor exists at the achieved power," not "no mapping exists." The
  anchor hunt's minimum detectable effect is near-perfect nesting on ≥10 pages
  (C4); moderate anchors would not survive FDR. The label and root↔leaf legs are
  reframed below.
- **[C] Off-the-shelf uniform verbose cipher is disfavoured**, but narrowly: the
  word-order contrast that motivated this refutes a *single-key* cipher and shows
  *verbose segmentation* (not homophony) disrupts word-order; a scribe-switching
  or drifting-key verbose cipher is untested and could regenerate the observed
  structure (C2).
- **[C] Abbreviation / abjad families are disfavoured** — they move h2 the wrong
  direction (≈3.5 vs 2.1) (F7, unaffected by the review).

## 3. What is NOT established (downgraded by review)

- **The meaningful-vs-meaningless verdict.** The earlier "carries word-order
  information a hoax can't generate" lean rested on (i) the Montemurro–Zanette
  measure, which is a **topic-clustering statistic, not a meaning detector**; (ii)
  a VMS baseline computed on **analyst-reordered** text whose sections coincide
  with the A/B split and quire drift, so the 0.31 bits/word may index scribe/
  dialect **blocking**; and (iii) a **single self-citation null the team built and
  tuned**, whose copy-nearby-token mechanism is exactly what manufactures
  word-order correlation. Grading one's own null does not license the conclusion
  (C5, C2). **Status: open.**
- **The invented-language / invented-world narrowing.** The narrative ranking that
  produced it rewarded **unfalsifiability** (an invented world predicts every
  null, so nulls can't count against it — yet were spent against the herbal
  reading) and ranked two hypotheses it had declared *internally indistinguishable*
  (C3). The paradigmatic-conlang "match" was **circular** (VMS-informed template)
  (C1, C5). **Status: retired as a ranking.**
- **"No real-taxa root↔leaf bundle."** Withdrawn. 35% annotation noise on
  root_type attenuates the association; disattenuated V ≈ 0.37 (moderate), and the
  *clean* root_coloring feature *did* associate with leaf features — a **possible
  masked positive**, not a null (C4).

## 4. The honest constraint envelope

Per P6, a competing-narratives statement — now with symmetric treatment of nulls
and a first-class "structured-meaningless" rival (C3):

**The manuscript is a genuine, constrained, two-system formal script that
disfavours (a) random/meaningless marks, (b) a plain labelled catalogue of real
plants, and (c) a uniform single-key verbose cipher — while the data underdetermine
the remaining class of structured-symbolic hypotheses:**

- **structured-meaningless** ("grammar without recoverable meaning" — procedural/
  glossolalic generation with local vocabulary drift): the simplest hypothesis
  consistent with all findings; under-weighted in the first draft, now first-class;
- **cipher** of a real text (a scribe-switching / low-segmentation-artefact
  variant, not the uniform Naibbe form);
- **constructed language** (a-priori, Lingua-Ignota class);
- **invented-world notation** (Codex-Seraphinianus class);
- a **meaningful-but-non-nomenclatural** natural text (kept open by the
  Language-A section↔text co-variation, ARI **0.35**, F8).

These are not ranked. The evidence does not currently separate meaningful from
meaningless within this class, and **cannot license "no referents exist" over
"referents not recovered by these methods."**

## 5. Origin (unchanged by review, grade C)

German/Alemannic iconographic gravity (crossbowman Sagittarius, cycle comparanda)
c. 1420s–1460s, in tension with the northern-Italian working premise (L1);
provenance documentary-solid only to 1637 (Baresch), the Rudolf II purchase and
Bacon attribution grade D. Carried as rival localizations.

## 6. The i02 agenda — experiments that would settle the open questions

Each is a concrete follow-up the critics specified:

1. **Blind adversarial self-citation null:** red-team-optimize the H3 generator to
   maximize MZ word-order info while matching h2 + both Zipf slopes, blind to the
   VMS target; publish the tuning budget and the MZ CI at VMS length. Settles the
   meaningful-vs-meaningless question.
2. **De-confound the word-order signal:** recompute ΔI on natural folio order; test
   a scribe-switching verbose cipher blocked like the VMS.
3. **Anchor-hunt power curve:** inject synthetic anchors at φ=0.3/0.4/0.5; re-run
   at line/label-adjacency granularity; restrict to mid-prevalence features.
4. **root↔leaf:** third-annotator adjudication + disattenuation; follow the
   root_coloring→leaf hit.
5. **Encoding bracket, fair:** equal VMS-informed tuning for all families on
   held-out metrics; add composed families (cipher∘conlang); bootstrap with CIs.

## 7. Methodological contribution (the most robust result)

Every statistic was computed by deterministic versioned code and validated on a
synthetic ground-truth harness before touching real-manuscript claims; the
replication gate reproduced published baselines first; the anchor hunt gated on a
null control and a planted control; and — decisively — **clean-context adversarial
review downgraded the program's own most exciting conclusion before it could be
published.** No plausible-sounding translation was ever generated, and the one
over-reach (the invented-language lean) was caught by the process, not shipped.
The harness + firewall + adversarial-review architecture is the differentiator
versus prior AI attempts and is publishable independently of any Voynich finding —
including as a case study in an AI research pipeline correcting itself.

---

## G4 sign-off

- [ ] Revised synthesis accepted as the honest final (Tim)
- [ ] Critique-log dispositions ratified
- [ ] i02 agenda approved as the next iteration
- [ ] Gate G4 approved
