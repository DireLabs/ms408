# E28 — Angular/ordinal anchor in the zodiac rings

Generated 2026-07-17T03:31:55+00:00 at commit `fbb3babd01` by `python -m ms408.experiments.e28_angular_anchor`. Numbers in `results/experiments/e28_angular_anchor.json`.

Anchor signal: **False**. Positive control detects ordered values: **True** (Mantel r=0.2402, p=0.001).

Mantel combined p = **0.00742** (1/12 rings p<0.05); length-autocorr combined p = 0.388.

| page | lang | hand | n | Mantel r | Mantel p | len ac1 | len p |
|---|---|---|---|---|---|---|---|
| f70v2 | None | 4 | 29 | 0.0352 | 0.174 | 0.146 | 0.181 |
| f70v1 | None | 4 | 15 | -0.1031 | 0.881 | 0.0278 | 0.367 |
| f71r | None | 4 | 15 | -0.1564 | 0.975 | 0.2162 | 0.13 |
| f71v | None | 4 | 15 | 0.1534 | 0.05 | 0.0894 | 0.257 |
| f72r1 | None | 4 | 15 | -0.1878 | 0.992 | -0.0044 | 0.387 |
| f72r2 | None | 4 | 29 | 0.0133 | 0.379 | -0.147 | 0.733 |
| f72r3 | None | 4 | 30 | 0.0464 | 0.149 | 0.1729 | 0.124 |
| f72v3 | None | 4 | 30 | 0.0404 | 0.174 | -0.097 | 0.666 |
| f72v2 | None | 4 | 30 | 0.0468 | 0.139 | 0.0602 | 0.279 |
| f72v1 | None | 4 | 30 | 0.0516 | 0.076 | 0.0106 | 0.369 |
| f73r | None | 4 | 30 | 0.2404 | 0.001 | -0.2416 | 0.881 |
| f73v | None | 4 | 30 | 0.0092 | 0.344 | -0.1055 | 0.67 |

## Verdict [D, refutation pass n/a]

NO ROBUST ANCHOR — the register hypothesis STAYS D (clean graded negative). The positive control confirms the test detects ordinal structure when present, yet across the 12 rings there is no CONSISTENT angular-ordinal signal. The Fisher-combined Mantel p (0.00742) is driven by a SINGLE ring (f73r, p=0.001): dropping it, the combined p is 0.1116 (n.s.); only 1/12 rings are individually p<0.05, with mixed sign (9/12 positive r), and the length-autocorrelation is null (0.388). Since all 12 rings are the SAME diagram type, a genuine value-encoding of the labels would appear across them, not in one — so the lone f73r hit reads as a chance fluctuation (a footnote-worthy idiosyncrasy at most, not an anchor). Combined with E27 (positional-numeral shape excluded), the symbols-as-values direction finds NO support in the manuscript's most number-like folios — the astronomical rings. i10 closes here unless a materially different anchor is proposed; the standing constraints remain the i06 cipher exclusion and the character/morphology structure. (No value/number claim — L7.) 12 zodiac rings (langs [], hands ['4']), 999 permutations. Mantel (angular-distance vs label-edit-distance) combined p=0.00742 (1/12 rings individually p<0.05); length-autocorrelation combined p=0.388. Positive control (ordered integers on a ring): Mantel r=0.2402 p=0.001 — DETECTS ordered values (test is sensitive).
