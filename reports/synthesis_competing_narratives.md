# T3.1 — Competing Narratives with Evidence Ledgers (W6b)

Generated 2026-07-07T01:37:46+00:00 at commit `274156c39d` by `python -m ms408.synthesis.narratives`. Numbers via the findings registry (`results/synthesis/findings_registry.json`), which pulls every value from `results/*.json` (L3 firewall).

**Reading rules (P6, L7).** This is a structured argument map, not a probability and not a decoding. Net scores below are a grade-weighted tally of supporting minus undercutting findings (A=3, B=2, C=1) — a bookkeeping aid for the argument, NOT a likelihood. No narrative is asserted; all remain open pending T3.3 adversarial review. Nothing here translates a single word.

## Evidence base

13 findings from Phase 2 (grades in brackets). The load-bearing ones are the harness-gated nulls and the encoding-bracket profile:

| id | grade | finding |
|---|---|---|
| F1-entropy-anomaly | A | Voynichese conditional character entropy h2 is far below natural language and replicates published values. |
| F2-currier-ab | A | The manuscript is two statistically distinct systems (Currier A/B), recovered from word co-occurrence alone. |
| F3-positional-structure | A | Strong positional constraints: paragraph-initial gallows enrichment, line-final m concentration — 'the line is a functional unit'. |
| F4-mz-word-order-info | B | The manuscript carries topic-scale word-order information at a natural-language scale (Montemurro-Zanette). |
| F5-cipher-erases-wordorder | B | Homophonic verbose cipher matches character structure but ERASES the word-order information the VMS has (dI 0.000 vs 0.307). |
| F6-selfcitation-overshoots | B | Self-citation (null hypothesis) overshoots word-order info at the wrong scale and runs too small a vocabulary. |
| F7-no-family-full-profile | B | No encoding family reproduces the VMS's full profile (low h2 AND intact word-order info together). |
| F8-section-alignment-A-only | B | Text co-varies with illustration sections in Language A only; Language B is textually homogeneous across its sections. |
| F9-anchor-hunt-null | B | No Voynichese token anchors to a herbal visual feature after FDR (harness gate passed). |
| F10-labels-not-naming | B | Illustration labels are not a naming system: labels recur across pages LESS than running text; herbal near label-free. |
| F11-no-root-leaf-bundle | B | The herbal shows no real-taxa root<->leaf feature bundle (root_type x leaf_shape independent); structure is within-organ only. |
| F12-morphology-paradigmatic | B | Voynichese is a dense, position-constrained, paradigmatic morphology unlike natural language; a paradigmatic conlang reproduces the full profile (p1-variant V3). |
| F13-anachronism-null | C | No annotated feature encodes information exceeding 15th-century observational capability (W7 anachronism scan). |

## Narrative ranking (grade-weighted net; not a probability)

| narrative | support | undercut | net |
|---|---|---|---|
| A-priori constructed language (Lingua-Ignota class) | +13 | −0 | +13 |
| Meaningful record of an invented world (Codex-Seraphinianus class) | +10 | −0 | +10 |
| Meaningless glossolalia / self-citation (elaborate hoax) | +8 | −6 | +2 |
| Verbose/substitution cipher of a real plaintext | +8 | −7 | +1 |
| Genuine natural-language herbal/reference work, labelled | +7 | −6 | +1 |
| Content exceeding period capability (W7 hard signature) | +0 | −1 | -1 |
| Abbreviated/shorthand natural language | +0 | −2 | -2 |

## The narratives, most- to least-supported

### A-priori constructed language (Lingua-Ignota class)

**Least contradicted.** The paradigmatic constructed-language model (P1 variant V3) was the *only* generative family to reproduce the VMS's full profile — low h2, dense edit-distance morphology, and word-order information at the right scale — where the cipher and self-citation families each failed one half. It also fits the position-constrained, paradigmatic morphology directly. **Caveat carried:** V3 used a VMS-informed affix template, so it is the family's upper bound, not a neutral fit; a like-for-like historical conlang (real Lingua Ignota) is the outstanding test. Currier A/B then reads as two dialects/registers of one invented system.

- **Supports:** F1-entropy-anomaly, F2-currier-ab, F3-positional-structure, F4-mz-word-order-info, F12-morphology-paradigmatic
- **Undercuts:** —

### Meaningful record of an invented world (Codex-Seraphinianus class)

**Consistent with the nulls that hurt the others.** A meaningful record of an invented world (Codex-Seraphinianus class) predicts exactly what we found: word-order information present (it is meaningful), section↔text co-variation in one hand, and — crucially — the anchor and realism nulls, because an invented world has no *external* referents for a word to anchor to and no real-taxa root↔leaf bundles to recover. The same three nulls (F9/F10/F11) that undercut the natural-herbal reading are *entailed* by this one. Its weakness is parsimony, not evidence: it is hard to distinguish from a systematically invented language (N-conlang) from inside the text — the W7 equivalence class.

- **Supports:** F1-entropy-anomaly, F3-positional-structure, F4-mz-word-order-info, F8-section-alignment-A-only
- **Undercuts:** —

### Meaningless glossolalia / self-citation (elaborate hoax)

**Weakened but not dead.** Self-citation / grille hoaxes reproduce most surface statistics — low h2, Zipf, positional effects — which is why the hoax hypothesis has always been hard to kill. But the VMS carries topic-scale word-order information (F4) that pure self-citation, as its own authors parameterize it, does not generate at the right scale (it *overshoots* at too short a scale, F6) and with too small a vocabulary. The information structure is the discriminator the surface statistics aren't.

- **Supports:** F1-entropy-anomaly, F3-positional-structure, F12-morphology-paradigmatic
- **Undercuts:** F4-mz-word-order-info, F6-selfcitation-overshoots, F7-no-family-full-profile

### Verbose/substitution cipher of a real plaintext

**Weakened on a specific mechanism.** A verbose/homophonic substitution cipher of a real plaintext should carry the plaintext's word-order information — yet the published Naibbe family, which matches the character statistics almost perfectly, *erases* that information (dI 0.000 vs the VMS's 0.307): random homophone draws decouple ciphertext types from plaintext types. The positional line-structure is also atypical of chancery cipher, and the cipher-culture dossier finds no attested verbose system of this scale in the 1404–1438 window. Not eliminated — a deliberately homophone-poor verbose cipher (the outstanding V2 sweep direction) could retain word-order info — but the off-the-shelf verbose cipher is contradicted.

- **Supports:** F1-entropy-anomaly, F2-currier-ab, F4-mz-word-order-info
- **Undercuts:** F3-positional-structure, F5-cipher-erases-wordorder, F7-no-family-full-profile

### Genuine natural-language herbal/reference work, labelled

**Most contradicted of the meaningful readings — specifically the 'labelled herbal/pharmacopoeia where words name real depicted plants' form.** Three independent, harness-gated nulls converge against it: no token anchors to a visual feature (F9), the labels are not a recurring naming vocabulary (F10, labels *more* unique than running text), and there is no real-taxa root↔leaf feature bundle (F11, the herbal's structure is within-organ geometry only). A genuine referential herbal should leave at least one of these signatures; none appears. The section↔text co-variation in Language A (F8) is the one positive datum and keeps the door open for a meaningful-but-non-nomenclatural natural text.

- **Supports:** F2-currier-ab, F4-mz-word-order-info, F8-section-alignment-A-only
- **Undercuts:** F9-anchor-hunt-null, F10-labels-not-naming, F11-no-root-leaf-bundle

### Content exceeding period capability (W7 hard signature)

**Null, as designed.** No annotated feature encodes information exceeding unaided 15th-century observation. Per W7, this is the honest form of the 'proof-level' ambition: a rigorous null is a citable constraint, not evidence of ordinary origin, and it collapses the ET hypothesis into the invented-world/visionary equivalence class (which the text *cannot* distinguish from inside).

- **Supports:** —
- **Undercuts:** F13-anachronism-null

### Abbreviated/shorthand natural language

**Effectively ruled out at our resolution.** Latin brevigraphy and abjad families *raise* h2 (the wrong direction) — abbreviation lands h2 ≈ 3.5 vs the VMS's ≈ 2.1 — and neither reproduces the joint low-h2/word-order profile. Consistent with Lindemann-Bowern's finding that abbreviation and abjads increase conditional entropy.

- **Supports:** —
- **Undercuts:** F7-no-family-full-profile

**Cross-cutting: community of origin (dossiers, grade C).** The zodiac iconography (crossbowman Sagittarius, cycle comparanda) places the illustrations in a German/Alemannic tradition c. 1420s–1460s — in real tension with the locked northern-Italian working premise (L1). The dossiers carry this as *rival localizations* for W6b, not a resolution. Provenance is C-solid only back to Baresch (1637); everything upstream — the Rudolf II purchase, the Bacon attribution — is grade D. Any origin narrative must route through the German/Alemannic iconographic gravity and the post-1600 documentary gap.

## Synthesis: what the convergence says

The Phase-2 findings do not decode the manuscript and do not name a single answer. What they do is **reshape the field of hypotheses**:

1. **The meaningful-vs-meaningless axis is not resolved by surface statistics** — self-citation reproduces them — but IS informed by the word-order information (F4), which the null family mis-scales. The manuscript carries more topic-scale structure than the strongest hoax model generates.
2. **The 'referential herbal' reading is the most constrained.** Three independent harness-gated nulls (anchor hunt, label naming, root↔leaf realism) agree that no word→referent mapping is detectable. Whatever the book is, it does not behave like a labelled catalogue of real plants at any granularity we can measure.
3. **Those same nulls are *entailed* by the invented-world reading** and compatible with a systematic conlang — which is why the W7 equivalence class (invented world / conlang / visionary) is the region the evidence least contradicts, while remaining internally indistinguishable.
4. **The off-the-shelf verbose cipher is contradicted** on word-order erasure; a homophone-poor variant is the one cipher direction still standing and the clearest outstanding experiment.
5. **Origin is doubly constrained and unresolved:** German/Alemannic iconographic gravity vs the northern-Italian premise, and a documentary chain solid only from 1637.

**Net for the flagship (T3.2):** the constraint envelope has shrunk toward *a structured, meaning-bearing symbolic system whose referents are not recoverable from within the text* — an invented language or invented-world notation more than a ciphered or labelled record of the real world — with the meaningful/hoax question narrowed but open, and origin unresolved. Every clause of that sentence is a graded claim above, and every one goes to T3.3 adversarial review before it can rise to grade A/B (L10).
