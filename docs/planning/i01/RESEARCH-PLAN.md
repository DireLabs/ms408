# RESEARCH-PLAN.md — MS408 Research Program

## 1. Premise and scope

**Working premise (scoped assumption, not a truth claim):** Beinecke MS 408 is a genuine artifact of ~1404–1438, likely northern Italian milieu, produced by multiple scribes, containing meaningful content. The hoax hypothesis is acknowledged but out of scope by design; W7's discriminator studies partially stress-test the premise from within.

**In scope:** the content of the book; the structure and semantics of the language and visuals; potential influences around its creation.

**Out of scope:** new physical forensics (we consume published carbon dating, ink/pigment analysis); decipherment-as-goal (decipherment would be a byproduct of constraint-shrinking, not the success criterion); for W7, any investigation of a contact mechanism (black-boxed per L2).

**Success definition:** defensibly shrink the constraint envelope around what the book *is* — genre, purpose, encoding class, community of origin — with every claim evidence-graded. Progress does not require decipherment.

## 2. Core design principles

The field's graveyard is full of "translations" that are plausible-sounding pattern-matching — and generating plausible meaning is precisely what language models do best. The program therefore firewalls generation from evidence:

- **P1 — Firewall.** Deterministic code computes all statistics; models hypothesize, design experiments, interpret outputs, and critique. A model never "estimates" an entropy value in-context.
- **P2 — Harness first.** Every method must prove itself on synthetic ground truth (§3) before touching real-manuscript claims.
- **P3 — Replication gate.** The pipeline must reproduce published baseline results before any novel experiment runs.
- **P4 — Independent anchors.** No translation or semantic claim stands without a statistical anchor derived independently of the claim.
- **P5 — Adversarial review.** Clean-context critic instances (no authoring history) review all A/B-graded claims before they stand.
- **P6 — Competing narratives.** Synthesis outputs present rival explanations with evidence ledgers, never a single confident story.

This discipline is the program's differentiator versus prior AI attempts and is itself part of the narrative deliverable.

## 3. Validation harness (keystone)

A benchmark of four corpus classes, matched for length and formatting where feasible:

| Class | Content | Ground truth | Source method |
|---|---|---|---|
| H1 | Real Voynichese | Unknown | EVA transliteration (per D1) |
| H2 | Voynich-like ciphertext from known Latin/Italian plaintext | Meaningful, recoverable | Naibbe verbose substitution cipher (Greshko 2025, *Cryptologia*) — reimplement generator |
| H3 | Sophisticated meaningless text matching Voynichese surface statistics | Meaningless | Timm–Schinner self-citation algorithm (2020) — reimplement generator |
| H4 | Plain medieval control texts | Meaningful, known | Latin, Italian, plus reference languages per D3 |

**Gate rule:** any technique claiming to detect meaning, recover structure, or identify encoding must correctly discriminate or recover on H2/H3/H4 before its H1 results are admissible. Optional extensions (flag as D-items if pursued): abjad/abbreviated variants of H4 texts; Codex Seraphinianus sample as a known invented-world control (D7).

The harness itself — generators, scoring API, benchmark report — is a publishable methodological contribution independent of any Voynich finding.

## 4. Workstreams

### W1 — Corpus foundation
**Objective:** the machine-readable asset everything runs on.
**Contents:** EVA transliteration (v101 sensitivity copy per D1); Beinecke high-resolution scans; page-level metadata joining section type (herbal/astronomical/balneological/pharmaceutical/recipes), Currier A/B dialect, and scribal hand (Fagin Davis ~5-hand model). Verify source availability and licensing during build (D10).
**Output:** versioned page-level dataset (text + image + metadata), loaders, integrity checks.

### W2 — Language structure
**Objective:** characterize Voynichese as a formal system and bracket its encoding class.
**Methods:** morphological segmentation (prefix/stem/suffix regularities; chol/chor-type networks); positional effects (line-initial gallows, word-final constraints, line-as-functional-unit tests); unsupervised topic induction from co-occurrence alone.
**Key test:** does internally derived topic structure independently reproduce the visual section boundaries?
**Encoding-hypothesis bracket:** verbose cipher (Naibbe family) · abjad + anagram (Hauer–Kondrak family) · abbreviation/shorthand (Latin brevigraphy) · constructed language (Lingua Ignota precedent) · null/self-citation. Each expressed as a generative model scored against the harness.

### W3 — Visual semantics and text–image alignment
**Objective:** the workstream where a multimodal frontier model genuinely exceeds prior art; highest ceiling in the program.
**Methods:** systematic annotation of every illustration (plant morphology features; star counts/configurations; jar types; nymph/plumbing configurations) under a fixed schema (D5). **Anchor hunt:** token clusters that statistically co-occur with specific visual features across pages — does anything behave like "root"? Exhaustive iconographic comparison against northern Italian alchemical-herbal and zodiac-emblem traditions, at full coverage with provenance-tracked confidence (prior art here is manual and piecemeal).
**Note:** plant identifications are soft priors, not hard anchors, pending D4.

### W4 — Influence mapping
**Objective:** situate the object in its documented milieu (bottom-up).
**Dossiers:** early-15th-c. cipher culture (pre-Alberti Milanese/Venetian chancery practice); balneological medicine (De balneis tradition); the Hartlieb-adjacent gynecological reading (Brewer & Lewis 2024); astrological iconography dating; provenance chain backward from Rudolf II into the pre-1600 gap.
**Output:** a constrained cultural-origin model with sourced claims, not vibes.

### W5 — Synthesis
**Objective:** the living narrative document arguing what the book *is* — genre, purpose, encoding class, community of origin — every claim graded per §6. Updated as workstreams land; final version is the program's flagship deliverable.

### W6 — Cold case
**Insight:** historically, "unsolvable" texts fell when someone killed a boring assumption everyone shared (Linear B / not-Greek; Mayan / pure ideography; Copiale / language-ID-first; Z340 / transposition), not when exotic hypotheses were added. Two moments:
**W6a (early) — assumption audit.** Enumerate and stress-test what every prior attempt took for granted: spaces = word boundaries; left-to-right/top-down reading order; one glyph ≈ one sound; text relates to adjacent image; single language throughout; line breaks arbitrary (vs. line as functional unit); single encoding layer; transliteration neutrality. Each assumption becomes a testable Phase 2 variant.
**W6b (late) — narrative synthesis.** Evidence-board work: timeline; means/motive/opportunity for candidate creator communities; chain-of-custody reconstruction; negative-space evidence (near-absence of corrections; no colophon; no reader marginalia in Voynichese — each a datum). Guard: outputs are *competing* narratives with explicit evidence ledgers (P6) — story-plausibility is the hallucination surface we firewalled.
**Boundary vs. W4:** W4 is bottom-up (situate in documented milieu); W6 is top-down (construct rival explanatory narratives and stress-test them).

### W7 — Plan Z discovery zone
**Framing:** with the contact mechanism black-boxed (L2), the ET-influence hypothesis reduces to "the referents lie outside the scribes' experiential world" — which is observationally equivalent, from inside the text, to invented-world and visionary/dream content. ET, fiction, and mysticism form one equivalence class absent external anchors; that class is testable. Modern existence proof of the artifact type: Codex Seraphinianus.
**Study 1 — Referential-realism discriminator.** Real taxa produce correlated feature bundles (root type × leaf type co-occurrence consistency across pages); invention-by-recombination produces free mixing. Measure which regime the ~130 herbal illustrations occupy. Same logic for star sections: any astronomically consistent structure against period catalogs (D11), or decorative?
**Study 2 — Anachronism scan.** The one signature that would genuinely distinguish nonhuman-influenced content: information exceeding 15th-century observational capability. Search for it. Expected result: null — and a rigorous null is itself a citable constraint.
**Study 3 — Purpose-reframing essay.** Genre analysis under each hypothesis family: reference work vs. record of experience vs. work of imagination ("a herbal of another world — what would that make the book *for*?"). Written regardless of which family wins; feeds W6b.
**Output form:** likelihood ratios across hypothesis families, W7's included. Nothing here reaches proof; that is the honest version of the "proof-level" ambition.

## 5. Phasing

- **Phase 0 — Foundation.** Decision locks (G0); corpus pipeline; validation harness.
- **Phase 1 — Calibration.** Replication gate (G1): h2 ≈ 2 character entropy, both Zipf laws, Currier A/B statistical split, Montemurro–Zanette long-range information structure, positional-glyph effects — all within tolerance of published values. Annotation schema + bulk annotation (G2). W6a assumption audit.
- **Phase 2 — Novel experiments.** W2 studies, W3 anchor hunt, encoding bracket, W4 dossiers, W7 studies. Parallelizable.
- **Phase 3 — Synthesis.** W6b narratives; W5 living document (G3); adversarial review; final narrative (G4).

## 6. Evidence grading scale

- **A** — Validated on harness, statistically robust, survived adversarial review.
- **B** — Statistically suggestive; single method or unreplicated; survived adversarial review.
- **C** — Qualitative/iconographic/historical with cited sources.
- **D** — Hypothesis or speculation, clearly labeled.

## 7. Approach-evaluation rubric

For scoring methods — ours and the literature's: falsifiability · ground-truth validation · hallucination surface area · incremental value over prior art · reproducibility. Candidate for an interactive scoring matrix (Latchel/Lula-style tool) if useful.

## 8. Deliverables

1. Corpus dataset + pipeline (W1)
2. Validation harness + benchmark report (§3) — standalone publishable
3. Replication report (Phase 1)
4. Annotated illustration dataset (W3)
5. Study reports: morphology, topic alignment, anchor hunt, encoding bracket, W7 discriminators
6. Influence dossiers (W4)
7. Assumption-audit matrix (W6a) and competing-narratives evidence board (W6b)
8. Living synthesis narrative with graded claims (W5) — flagship
9. Approach-evaluation matrix (§7)

## 9. Failure modes and guards

| Failure mode | Guard |
|---|---|
| Plausible-translation hallucination | P1, P4, L7 |
| Overfitting to one transliteration | D1 sensitivity pass |
| Annotation drift at scale | QA sampling protocol (WORKFLOW §5) |
| Narrative overconfidence in W6b/W7 | P5, P6, likelihood-ratio output form |
| Pipeline bugs masquerading as findings | P3 replication gate |
| Silent scope creep | DECISIONS.md flag-don't-resolve rule |

## 10. Key sources (verify exact citations and fetch during T0.2)

Hauer & Kondrak, *TACL* (algorithmic decipherment; press 2018) · Montemurro & Zanette 2013, *PLOS ONE* (long-range word structure) · Timm & Schinner 2020 (self-citation generator) · Rugg 2004, *Cryptologia* (grille hoax hypothesis) · Bowern & Lindemann (character entropy comparisons; Voynich linguistics survey) · Fagin Davis 2020, *Manuscript Studies* (scribal hands) · Brewer & Lewis 2024, *Social History of Medicine* (gynecological reading) · Greshko 2025, *Cryptologia* (Naibbe cipher) · Zandbergen, voynich.nu (provenance, dating, transliteration resources) · Beinecke Digital Collections (MS 408 scans).
