# E2 — Word-order signal confound

Generated 2026-07-07T21:36:14+00:00 at commit `6d1edfab09` by `python -m ms408.experiments.e2_wordorder_confound`. Numbers in `results/experiments/e2_wordorder_confound.json`.

| corpus | Delta-I | peak scale | tokens |
|---|---|---|---|
| VMS, natural folio order | 0.3064 | 812 | 34,111 |
| VMS, section-reordered (i01) | 0.3072 | 812 | 34,111 |
| Blocked natural text (Vulgate books) | 0.3564 | 812 | 34,111 |
| **Meaningless** block stream (Zipfian, no semantics) | 2.1781 | 6822 | 34,110 |
| Homophonic verbose cipher of blocked text | 0.0135 | 1991 | 119,507 |
| **Deterministic** verbose cipher of blocked text | 0.3564 | 812 | 34,111 |
| Pliny plaintext (i01 H2 source) | 0.1034 | 642 | 8,998 |

- Reorder inflation: **0.0008 bits**.
- Meaningless blocks reach Delta-I: **True** (confirms the statistic measures block structure, not meaning).
- Homophonic cipher retains Delta-I: **False**; deterministic (type-preserving) cipher retains Delta-I: **True**.

## Verdict [B, refutation pass applied]

E2 (post-refutation): Delta-I measures BLOCK STRUCTURE, not meaning. (1) Reordering is not the artifact — natural folio order 0.3064 ~ reordered 0.3072 (though the critic notes natural folio order is already section-blocked, so this rules out only the analyst-reordering confound). (2) Block structure ALONE produces the signal: a MEANINGLESS block stream (region-specific Zipfian vocab, zero semantics) reaches Delta-I 2.1781 — confirming the statistic is meaning-independent. (3) The anti-cipher point is CORRECTED: a HOMOPHONIC verbose cipher collapses Delta-I to 0.0135 (destroys word-type identity), but a type-PRESERVING deterministic verbose cipher of the same blocked text RETAINS it (Delta-I 0.3564) — so nomenclator / deterministic-verbose / syllabary ciphers are NOT ruled out and remain a standing hypothesis; only heavy-homophony (Naibbe-class) ciphers are disfavoured.

**Implication.** With E1, the word-order story is: Delta-I is meaning-blind (E1) and measures section-block structure (E2 — a meaningless block stream reproduces it). It disfavours heavy-homophony verbose ciphers (Naibbe-class) but NOT type-preserving deterministic-verbose / nomenclator / syllabary ciphers, which retain it and remain standing. The flagship's 'off-the-shelf uniform verbose cipher disfavoured' is upheld and sharpened to 'heavy-homophony disfavoured; deterministic/nomenclator cipher open'.
