---
name: package-paper
description: Package the current MS408 research state into a versioned LaTeX/arXiv preprint (PDF). Reads FLAGSHIP.md + results/ + reports/, assembles a graded paper snapshot, compiles to PDF. Re-run each iteration to re-release. Invoke when the user asks to build/update the paper, cut a preprint, or package research for peer feedback.
---

# package-paper — MS408 preprint packaging

Turn the program's current, already-graded synthesis into a self-contained
LaTeX/arXiv preprint PDF. This is a **re-releasable** snapshot: run it at the end of
any iteration to produce the next version. It does NOT do new analysis — it packages
what is already firewall-verified.

## Binding rules (inherit the program's discipline)

- **Firewall (L3).** Every number in the paper is copied from `results/**/*.json` or a
  `reports/*.md` table — never estimated or recalled. If a needed number isn't in
  `results/`, stop and say so; do not invent it.
- **Evidence grading (L6).** Carry the A–D grade on every claim, exactly as graded in
  `docs/synthesis/FLAGSHIP.md`. Do not upgrade a claim to make the paper stronger.
- **No translation / no over-reach (L7).** No decipherment, plaintext, or real-taxon
  claims. The paper's thesis is the *constraint envelope* + the *method*, not meaning.
- **Scope = the latest COMPLETED iteration.** Anything still in flight → "Future Work".
- **Honesty is the selling point.** The self-correction record (refutation passes
  overturning the program's own conclusions) is a headline contribution, not an
  embarrassment — report it plainly.

## Inputs (read in this order)

1. `docs/synthesis/FLAGSHIP.md` — the primary content source; it is already the
   graded, refutation-passed synthesis. The paper is essentially a formatted,
   citation-backed rendering of it.
2. `docs/planning/i0*/STATUS.md` — per-experiment verdicts and grades.
3. `results/experiments/*.json` and `results/**/*.json` — exact numbers (cite the
   producing script + the value; spot-check that FLAGSHIP's numbers match the JSON).
4. `reports/*.md` — human-readable per-study tables for figures/appendix.
5. `paper/metadata.yaml` — title, authors, affiliations, venue, keywords (create from
   `.claude/skills/package-paper/assets/metadata.example.yaml` if missing; if author
   fields are placeholders, compile anyway and WARN the user to fill them).

## Procedure

1. **Determine version.** Next `paper/vN/` (v1 if none). Read `paper/metadata.yaml`
   for `version` override; else N = highest existing + 1.
2. **Assemble `paper/vN/main.tex`** from the template
   (`.claude/skills/package-paper/assets/template.tex`), filling:
   - **Abstract** — the honest headline from FLAGSHIP: a genuine constrained two-system
     script; meaning underdetermined and *provably* so with current statistics; the
     one positive lead (root↔leaf) unresolved/underpowered; the method (harness +
     firewall + adversarial self-correction) as the transferable contribution.
   - **1 Introduction** — the manuscript; why prior decipherment claims fail; the
     program's stance (shrink the constraint envelope, every claim graded; decipherment
     is NOT the goal).
   - **2 Data & Transliteration** — Beinecke MS 408; EVA (Zandbergen–Landini) primary,
     v101 sensitivity; Currier A/B; Fagin Davis hands; the annotation pipeline.
   - **3 Method: harness, firewall, adversarial refutation** — H1–H4 controls; the
     replication gate; deterministic code→results→reports; evidence grades A–D; the
     standing clean-context refutation pass. This section is the methodological
     contribution; make it concrete.
   - **4 Results** — grouped as in FLAGSHIP §1–§3: (a) established [A] facts
     (entropy anomaly, A/B split, positional grammar, replication gate, ED1 network);
     (b) disfavoured [C] (no lexical herbal naming system; verbose ciphers excluded,
     abjad revived); (c) not established / underdetermined (meaning not localizable —
     E9; no encoding family distinguished — E5/E8); (d) the root↔leaf arc E4→E12 →
     UNRESOLVED-underpowered. Every subsection cites exact numbers from `results/`.
   - **5 Discussion** — meaning-vs-meaningless is underdetermined and E9 shows *why*
     (structure statistics ≠ meaning detectors); the abjad revival; the self-
     correction meta-result (list the overturned own-conclusions).
   - **6 Limitations** — annotation noise (leaf κ≈0.45), model-lineage dependence,
     single-corpus power limits, EVA-dependence (v101 sensitivity).
   - **7 Future Work** — everything post-scope: the human-panel root↔leaf adjudication;
     the i05 mid-level linguistic program (morphology, word-classes, function/content
     bimodality) with A/B stratification; abjad joint-signature test; second cross-
     vendor rater.
   - **References** — use `assets/refs.bib`; add any missing key works; mark any
     citation whose details you could not verify with a `% UNVERIFIED` comment.
3. **Copy** `assets/refs.bib` → `paper/vN/refs.bib`; copy any figures.
4. **Compile:** `cd paper/vN && latexmk -pdf -interaction=nonstopmode main.tex`
   (fallback: two `pdflatex` passes + `bibtex`). Fix LaTeX errors and recompile.
5. **Verify & report:** confirm `paper/vN/main.pdf` exists and page count > 0; list
   any `% UNVERIFIED` citations and placeholder metadata; print the version + path.
   Do NOT auto-send anywhere (publishing is a user decision).

## Re-release

Each run writes a new `paper/vN/`; prior versions are immutable. Bump the version in
`paper/metadata.yaml` or let the skill auto-increment. A changelog line per version
lives in `paper/CHANGELOG.md` (create/append).
