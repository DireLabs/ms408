# MS408 — Living Synthesis (W5 flagship)

**Status:** T3.2 draft for G3. Claims graded A–D (RESEARCH-PLAN §6); every A/B
here is **candidate pending T3.3 adversarial review** (L10). Numbers are cited
from `results/synthesis/findings_registry.json`, which pulls them from
`results/*.json` (L3 firewall). This is a *living* document — it is updated as
workstreams land and is not a final verdict.

**Success criterion (RESEARCH-PLAN §1):** defensibly shrink the constraint
envelope around what the book *is* — genre, purpose, encoding class, community of
origin — with every claim evidence-graded. Progress does not require decipherment.
**Assessment: met.** The envelope is materially smaller and the reduction is
carried by graded, harness-validated evidence, not narrative plausibility.

---

## 1. What we can now say (the constraint envelope)

### 1.1 Voynichese is a real formal system, not random marks — but its character statistics do not discriminate meaning

- **[A] The conditional character-entropy anomaly is real and replicates.** h2 ≈
  **2.16** for the manuscript vs **3.23–3.91** for our medieval natural-language
  controls; the value matches published figures within thousandths of a bit and
  is robust across dialect and scribal hand (F1, replication gate G1).
- **[A] The manuscript is two statistically distinct systems (Currier A/B).**
  Cross-dialect vocabulary divergence (JS **0.26**) is far above within-dialect
  heterogeneity (**0.04–0.09**), and the A/B split is the single strongest
  structure recoverable from word co-occurrence alone (F2).
- **[A] Strong positional grammar.** Paragraph-initial gallows enrichment, the
  line as a functional unit (m-glyph concentrated line-finally), and glyph
  adjacency constraints all replicate (F3).
- **[C→B, pending T3.3] But low h2 alone proves nothing about meaning.** Both a
  meaningful verbose cipher and a meaningless self-citation generator reproduce
  the h2 anomaly. Character statistics are a property of the *encoding surface*,
  not of the presence or absence of content (F1, F5, F6).

### 1.2 The discriminating signal is word-order information, and it cuts against the two commonest "solutions"

- **[B, pending T3.3] The manuscript carries topic-scale word-order information**
  — Montemurro–Zanette ΔI ≈ **0.31 bits/word peaking at ~812 words**, replicating
  the published characteristic scale (F4, G1).
- **[B, pending T3.3] The off-the-shelf verbose cipher is contradicted by it.**
  The homophonic Naibbe family matches the character statistics almost perfectly
  yet **erases** word-order information (ΔI **0.000** vs the VMS's 0.31): random
  homophone draws decouple ciphertext types from plaintext types (F5). A
  deliberately homophone-poor verbose cipher is the one cipher direction still
  standing (outstanding experiment).
- **[B, pending T3.3] The pure self-citation hoax is weakened by it.** Timm–
  Schinner self-citation reproduces the surface statistics but *overshoots*
  word-order information at too short a scale and with too small a vocabulary
  (F6). The information structure is the discriminator the surface statistics are
  not.
- **[B, pending T3.3] No single encoding family reproduces the full profile.** Of
  five generative families scored on a shared statistical profile, none matched
  low h2 AND intact word-order information together at neutral parameterization;
  abbreviation and abjad families move h2 the *wrong* direction (F7).

### 1.3 No word→referent mapping is detectable — three independent, harness-gated nulls

- **[B, pending T3.3] Anchor hunt: nothing behaves like "root."** Across 14,758
  token×feature tests on 129 herbal pages, zero tokens anchor to a visual feature
  after FDR correction — with the meaning-detection harness gate passing (null
  control 0 false discoveries; planted anchor recovered) (F9).
- **[B, pending T3.3] The labels are not a naming system.** In the label-rich
  pharmaceutical section, labels are **95% unique** and recur across pages *less*
  than running text (8 recurring types vs a null band of 25–41); the herbal
  section is nearly label-free (6 of 129 pages). A nomenclature would push label
  recurrence *above* baseline; we see the opposite (F10).
- **[B, pending T3.3] No real-taxa root↔leaf bundle.** The morphological
  discriminator finds the herbal's feature structure is *within-organ only*: the
  load-bearing cross-organ realism signal — does root morphology predict leaf
  morphology, as real plants require — is absent (Cramér's V 0.26, p 0.26; the
  combination space is saturated). Real taxa produce correlated root↔leaf bundles;
  the VMS herbal does not (F11).

### 1.4 Origin is doubly constrained and unresolved

- **[C] Iconographic gravity is German/Alemannic, c. 1420s–1460s** (crossbowman
  Sagittarius and cycle comparanda), in real tension with the locked
  northern-Italian working premise (L1). Carried as rival localizations, not a
  resolution (astro-iconography dossier).
- **[C] Provenance is documentary-solid only back to 1637** (Baresch); the Rudolf
  II purchase and the Bacon attribution are grade D (provenance dossier).
- **[C] No anachronism.** No annotated feature exceeds unaided 15th-century
  observational capability; the ET hypothesis collapses into the
  invented-world/visionary equivalence class, which the text cannot distinguish
  from within (F13).

---

## 2. What the book most likely is (narrowed, not decided)

Per P6 this is a *competing-narratives* statement, not a single answer. Full
argument map and grade-weighted tally in `reports/synthesis_competing_narratives.md`.

**The envelope has shrunk toward a structured, meaning-bearing symbolic system
whose referents are not recoverable from within the text** — an invented language
or invented-world notation more than a ciphered or labelled record of the real
world. Specifically, in decreasing order of *least-contradicted*:

1. **[C→B] A-priori constructed language** (Lingua-Ignota class) — the *only*
   generative family to reproduce the full VMS profile (paradigmatic conlang, P1
   sweep V3), though on a VMS-informed template (upper bound; a like-for-like
   historical conlang is the outstanding test). A/B as two registers/dialects.
2. **[C→B] Meaningful record of an invented world** (Codex-Seraphinianus class) —
   *entails* the three anchor/realism nulls (an invented world has no external
   referents to anchor to), and is internally indistinguishable from (1): the W7
   equivalence class.
3. **[C] Weakened but open:** homophone-poor verbose cipher; self-citation hoax
   (the information structure argues against the standard forms of both).
4. **[C] Most-contradicted meaningful reading:** the labelled herbal /
   pharmacopoeia where words name real depicted plants — the three harness-gated
   nulls converge against it. A meaningful-but-non-nomenclatural natural text is
   not excluded (Language-A section↔text co-variation, ARI **0.35**, is the one
   positive datum, F8).
5. **[C] Effectively excluded at our resolution:** abbreviation/shorthand natural
   language; ET/anachronistic content.

---

## 3. What remains open (honest ledger)

- **Meaningful vs meaningless** is narrowed by the word-order information but not
  closed: a sufficiently tuned self-citation variant, or a low-homophony cipher,
  are untested corners.
- **Conlang vs invented-world** may be *undecidable from inside the text* (the W7
  equivalence class) — an external anchor would be required, and none was found.
- **Origin community**: German/Alemannic iconography vs northern-Italian premise
  is unresolved; a within-milieu iconographic study is the next step.
- **Language B's homogeneity**: B's sections do not textually differentiate (F8) —
  unexplained; a candidate T-variant follow-up.
- **v101 > EVA**: the alternative transliteration consistently carries more
  recoverable structure (P1 sweep V1) — a transliteration-neutrality question
  (L11) worth revisiting.

---

## 4. Methodological contribution (standalone)

The discipline is itself a deliverable. Every statistic was computed by
deterministic, versioned code and validated on a synthetic ground-truth harness
(H1 real / H2 cipher / H3 gibberish / H4 natural) before touching real-manuscript
claims; the replication gate reproduced published baselines before any novel
experiment; the anchor hunt would not report a finding until a null control and a
planted-anchor control both passed. **No plausible-sounding translation was ever
generated, because the architecture made it impossible to.** The harness and the
firewall are the differentiator versus prior AI attempts, and are publishable
independently of any Voynich finding.

---

## G3 sign-off

- [ ] Synthesis accepted as the flagship draft (Tim)
- [ ] Claims cleared to enter T3.3 adversarial review at candidate A/B
- [ ] Gate G3 approved
