# Glossary

Plain-language definitions for the two audiences this project serves — Voynich/MS 408
researchers who may not be coders, and technical users who may not know the manuscript.
Where a term names a computed quantity, the "computed in" note points at the code.

## The manuscript

- **Voynich Manuscript / Beinecke MS 408** — an illustrated codex in an undeciphered script,
  held at Yale's Beinecke Library (shelfmark MS 408); carbon-dated to the early 15th century.
- **Folio** — a numbered manuscript leaf (e.g. f73r = folio 73, recto/front). Sections are
  conventionally labelled herbal, astronomical, balneological ("bathing"), pharmaceutical, etc.
- **Hand / scribe** — a distinct handwriting. Multiple scribal hands have been identified
  (Fagin Davis); text analyses stratify by hand.
- **Currier A / Currier B** — two statistically distinct "languages" or systems within the
  text (Prescott Currier). Whether they are dialects, registers, or vocabularies is open;
  all our text analyses stratify by A/B.

## Transliteration

- **Transliteration** — a rendering of the script's glyphs into ASCII so it can be computed
  on. The choice of scheme can change statistics, so we treat it as a variable.
- **EVA** — Extensible (originally European) Voynich Alphabet; the primary transliteration we
  use (Zandbergen–Landini, "ZL"). **v101** is an alternative scheme used as a sensitivity check.
- **IVTFF** — Intermediate Voynich Transliteration File Format; the file format the ZL
  transliteration ships in (parsed in `src/ms408/ivtff.py`).
- **Respacing** — re-drawing word boundaries. It changes token statistics dramatically and is
  a known confound (a cipher can respace its plaintext before enciphering) — see the E29 note.

## The discriminator axes (what `evaluate()` reports)

- **h2** — conditional (second-order) character entropy: how predictable the next character is
  given the previous one. The manuscript's is anomalously *low* vs natural language. A "hard"
  axis.
  **Two conventions share the name, and they give different numbers on the same text** —
  always say which you mean:
  - *within-word* (`textstats.char_conditional_entropy`): no space, bigrams never cross a word
    boundary. This is what the harness benchmark and the replication measurements report — the
    familiar ~2.08 for the manuscript (all words) against ~3.1–3.9 for natural language.
  - *Lindemann–Bowern* (`textstats.lb_entropies`): the space counts as a character and bigrams
    span word boundaries. **This is the convention the evaluator bands.** On the same
    all-pages slice it gives 2.1643, not 2.1247.

  The slice matters as much as the convention: "all words" (every locus type) is not
  "paragraph tokens only", and neither is a per-dialect or matched-10,000-token sample. The
  shipped band points are LB, paragraph tokens, 10,000-token budget, per dialect —
  Currier A 2.1822, Currier B 1.961 (`src/ms408/data/reference_bands.json`).
- **ΔI (dI) / MZ information** — Montemurro–Zanette word-order information: how much information
  the *order* of words carries at a given scale. **Confounded**: it collapses under homophony
  or respacing alone, so it is a homophony/type-token detector, not a clean word-order axis —
  never read an in-band ΔI as "intact word order." Computed in `src/ms408/mz.py`.
- **ed1 / ED1** — edit-distance-1 morphology: the share of word types connected in a network
  where an edge joins words one character-edit apart. The manuscript has a dense such network
  (~0.75–0.80). A "hard" axis. Computed in `studies/morphology.py`.
- **Zipf slope** — the slope of the rank–frequency law (log rank vs log frequency), fitted by
  least squares over a **fixed rank window of [10, 1000]** — or to the last type if there are
  fewer, and undefined (`None`) below 20 types. State the window whenever you quote a slope:
  it is not scale-free, and a different window gives a different number.
  **Advisory** since D23 — it was a "hard" axis until per-dialect bands showed its resampled
  CI is biased off the full-sample point, because at smaller token counts the ranks near 1000
  are mostly frequency-1 and the saturated tail flattens the fit. Not banded, not counted.
  Computed in `textstats.zipf_slope`.
- **TTR (type–token ratio)** — vocabulary richness = distinct words ÷ total words. **Advisory**:
  intrinsically sensitive to the token count (fewer tokens → higher TTR), so it is not banded
  and not counted; only compare at a similar token budget.
- **fc_z / wc_z (mid-level syntax)** — null-corrected z-scores for the function/content
  collocation gap (`fc`) and adjacent word-class structure (`wc`). "**local**" uses a
  within-block null (deconfounded of topic drift); "**global**" uses a full order-shuffle
  null (confounded by topic drift). Both are **soft**: the manuscript's own confidence interval
  crosses zero. Computed in `signature.py` (from `e13b`/`e14` primitives).
- **block scale** — a coarse partition of the text (hundreds of words), where topic/section
  structure lives, as opposed to the token/adjacency (word-to-word) scale.
- **null-corrected** — a statistic expressed relative to a matched random baseline (e.g. an
  order-shuffle of the same words), so nuisance factors cancel and corpora are comparable.

## The method

- **Harness** — matched controls (real language, ciphers, meaningless generators) that a
  method must separate on synthetic data before it is trusted on the manuscript.
- **Firewall** — the rule that every reported number comes from deterministic, versioned code
  writing machine-readable results; nothing estimated or recalled.
- **Refutation pass** — an independent, clean-context skeptic tasked to attack a strong claim
  before it stands; briefs archived in `docs/refutations/`. See `docs/METHODOLOGY.md`.
- **Evidence grade (A–D)** — the strength label every claim carries; A is replicated/robust,
  D is speculative. An ungraded claim is treated as D.
- **Necessary, not sufficient** — matching the manuscript's bands means a hypothesis is *not
  excluded*, never that it is the mechanism. The evaluator is built to withhold, not confirm.
