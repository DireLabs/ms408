# arXiv submission bundle — ready to upload

Two preprints, packaged so submission is a single pass. **Nothing here has been submitted.**
Build the source tarballs with `bash paper/make_arxiv_bundle.sh` → `paper/dist/*.tar.gz`
(each = `main.tex` + `main.bbl`; both verified to compile standalone with `pdflatex` and no
`bibtex`, 0 undefined references). The full paper abstracts live in the PDFs; the
**arXiv abstract field caps at ~1920 characters**, so a condensed field-ready abstract is
given below for each (the v6b paper abstract is 5.1k chars and must be shortened for the form).

## Before you upload — shared checklist

- [ ] **Contact line.** All three of `metadata.yaml`, `paper/v6b/main.tex:24`, and
      `paper/methods/v3/main.tex:24` read `tim@direlabs.com \quad direlabs.com \quad
      ti.mims.ms`. `ti.mims.ms` looks malformed (your registered address is `tim@mims.ms`).
      Fix or confirm before submitting — it's on the title page of both papers.
- [ ] **Bibliography details.** A few `refs.bib` entries carry `% UNVERIFIED` notes (they do
      not appear in the compiled PDF, but resolve them before any journal version):
      - both papers: Currier A/B origin; scribal-hands (Manuscript Studies) venue;
        self-citation/auto-copying source; the h1/h2 entropy reference.
      - methods/v3 additionally: one entry's exact venue/date; one entry's exact pages.
- [ ] **Categories** — confirm the primary + cross-lists proposed per paper below.
- [ ] **License** — recommend **CC BY 4.0** (matches the Apache-2.0 code's openness); the
      default arXiv non-exclusive licence is the fallback. Your choice, set at upload.
- [ ] Optional: add an ACM/MSC class (suggestions below) in the arXiv form.

## Upload steps (per paper)

1. New submission → upload `paper/dist/<name>-arxiv.tar.gz`.
2. Paste the condensed abstract below into the Abstract field; fill title/authors.
3. Set primary category + cross-lists; set the Comments field; pick the license.
4. Preview the arXiv-rendered PDF (should match `paper/<dir>/main.pdf`), then submit.

---

## Paper 1 — Constraint-envelope paper

- **Tarball:** `paper/dist/v6b-constraint-envelope-arxiv.tar.gz` · **12 pages** · source `paper/v6b/`
- **Title:** Shrinking the Constraint Envelope of the Voynich Manuscript: A
  Firewall-Disciplined, Self-Correcting Computational Program
- **Authors:** Tim Walsh (Principal Researcher, DireLabs, LLC)
- **Primary category:** `cs.CL` (Computation and Language).
  **Cross-list:** `cs.DL` (Digital Libraries); optionally `stat.AP`.
- **Comments field:** `12 pages. Companion open-source evaluator and methodology; all
  statistics firewall-reproducible. No decipherment or translation claim.`
- **ACM class (optional):** I.2.7; J.5
- **Condensed abstract (≈1.8k chars, field-ready):**

> We report a computational program on Beinecke MS 408 (the Voynich Manuscript) whose goal is
> not decipherment but defensibly shrinking the constraint envelope around what the book is,
> with every claim carrying an A–D evidence grade. The program couples three disciplines: a
> synthetic ground-truth harness every method must pass before touching the manuscript; a
> firewall in which all statistics come from deterministic, versioned code; and a standing
> clean-context adversarial refutation pass on every finding. We confirm the low-entropy
> anomaly (conditional character entropy h2≈2.08 vs 3.07–3.91 for natural-language controls),
> a two-system (Currier A/B) structure, strong positional grammar, and dense paradigmatic
> morphology. We find no lexical label→feature naming system for the herbal, and no statistic
> localizes meaning: against structured-meaningless baselines a meaningless generator
> out-scores meaningful text on every axis. The manuscript's structure lives below the word —
> it lacks the natural-language content/function collocational gap and shows only weak
> word-class structure. Turning that mid-level signature into a cryptanalytic discriminator,
> we robustly exclude word-order-preserving ciphers of real prose (they inherit strong surface
> syntax the manuscript lacks, by 6.8σ/8.0σ once deconfounded). We initially over-reached to
> the entire cipher-of-real-prose class, but engaging a concurrent verbose-homophonic cipher
> (Greshko 2025) forced a retraction: a homophonic cipher is not ruled out, and it and a
> positional/generative account both remain live. A favoured generative family
> under-determines the sub-mechanism without being uninformative. The most
> robust result is the architecture itself: across iterations the refutation pass repeatedly
> overturned the program's own conclusions — including ones produced by its own code — before
> they reached print. We make no translation or real-taxon claim.

---

## Paper 2 — Methods paper

- **Tarball:** `paper/dist/methods-v3-adversarial-self-correction-arxiv.tar.gz` · **9 pages** ·
  source `paper/methods/v3/`
- **Title:** Adversarial Self-Correction for Computational Research on Ground-Truth-Free
  Corpora
- **Authors:** Tim Walsh (Principal Researcher, DireLabs, LLC)
- **Primary category:** `cs.DL` (Digital Libraries) or `cs.CL`.
  **Cross-list:** `cs.AI`; `cs.CL` (if `cs.DL` primary).
- **Comments field:** `9 pages. Companion to the MS 408 constraint-envelope preprint; the
  refutation-pass briefs are archived with the program.`
- **ACM class (optional):** I.2.7; H.3.7
- **Condensed abstract (≈1.85k chars, field-ready):**

> Computational study of ground-truth-free corpora is unusually prone to plausible-but-wrong
> conclusions: with no key to check a reading against, "it looks like language / a cipher / a
> number system" is nearly unfalsifiable and the analyst's degrees of freedom are vast. We
> describe an operating architecture that couples three disciplines to blunt this: a synthetic
> ground-truth harness (every method must separate known positives from matched
> null/meaningless controls before touching the real object); a firewall (every reported
> number is produced by deterministic, versioned code recording its script, commit, inputs,
> and parameters — nothing estimated or recalled); and a standing clean-context adversarial
> refutation pass in which an independent skeptic, without the original analysis's context,
> builds the strongest case against each finding, its brief archived. We do not claim to have
> proven the discipline "works": the evidence is a single program's record with no controlled
> counterfactual. What we report, over an eleven-iteration program on the Voynich Manuscript
> (Beinecke MS 408), is a firewall-verified record in which over a dozen first-pass
> conclusions — several asserted by the program's own analysis code, two of them negatives —
> were narrowed, withdrawn, or retracted-then-partly-restored. In the sharpest episode,
> engaging a concurrently-published cipher designed to imitate the manuscript, the pass
> reversed a first-pass result that flattered the program's prior conclusion, and a further
> pass caught a recalled, unsourced number in the retraction write-up itself. We situate the
> architecture against pre-registration, multiverse analysis, severe testing, adversarial
> collaboration, and reproducible research, and offer it — with an adoption checklist — as a
> disciplined default worth adopting and testing, not a demonstrated cure. This paper was
> itself subjected to the same pass.

---

## Note on scope vs. the papers' current text

These preprints predate two closing results from the release/verification work. Neither
changes a headline, but a future revision (v7 / methods-v4) should fold them:

- **E33** (this iteration): the block-scale, like-for-like ΔI test — the last untested way the
  word-order leg could have discriminated. A first pass wrongly found it *reached* the VMS
  corner; the refutation pass showed that was a homophony-marker artifact, and under a fair
  model the (h2, block-ΔI) plane **weakly separates** verbose+homophonic ciphers (closest
  config still misses, and only at 3× the VMS word length). This does NOT revive ΔI into a
  hard discriminator, so the program-level "inconclusive" cipher disposition (resting on the
  soft syntax measures) is unchanged — but the "ΔI leg is dead even at block scale" phrasing
  is retired. A v7 should state the block-scale plane weakly separates.
- The program shipped as an **open-source evaluator** (`ms408.evaluate`, Apache-2.0); the
  papers can cite the repo as the reproducibility artifact.

Consider whether to submit now (papers are internally consistent and honest as-is) or after a
v7 that folds E33 + the release. Recommend: submit the methods paper now (unaffected), and
hold the constraint-envelope paper for a short v7 that cites E33 and the repo.
