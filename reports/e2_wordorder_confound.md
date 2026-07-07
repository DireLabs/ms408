# E2 — Word-order signal confound

Generated 2026-07-07T21:28:34+00:00 at commit `bb465830a3` by `python -m ms408.experiments.e2_wordorder_confound`. Numbers in `results/experiments/e2_wordorder_confound.json`.

| corpus | Delta-I | peak scale | tokens |
|---|---|---|---|
| VMS, natural folio order | 0.3064 | 812 | 34,111 |
| VMS, section-reordered (i01) | 0.3072 | 812 | 34,111 |
| Blocked natural text (Vulgate books) | 0.3564 | 812 | 34,111 |
| Verbose cipher OF blocked text | 0.0135 | 1991 | 119,507 |
| Pliny plaintext (i01 H2 source) | 0.1034 | 642 | 8,998 |

- Reorder inflation: **0.0008 bits** (natural → section-reordered).
- Blocking alone produces Delta-I: **True**.
- Block cipher retains Delta-I: **False**.

## Verdict [B, pending refutation pass]

E2: section-reordering does NOT materially inflate Delta-I (0.3064 natural vs 0.3072 reordered) — the signal is intrinsic to folio order; and even a cipher of block-structured text loses word-order information (Delta-I 0.0135), so the anti-cipher point survives block structure.

**Implication.** With E1 (Delta-I is not a meaning detector) this closes the word-order story: the statistic that carried i01's distinctive lean is both meaning-blind (E1) and — to the extent shown here — sensitive to blocking and survivable by a non-uniform cipher (E2). The honest position from the flagship (meaningful-vs-meaningless open; only the UNIFORM cipher disfavoured) is reinforced.
