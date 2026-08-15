# E1 — Is Montemurro-Zanette DI a meaning detector?

Generated 2026-08-14T06:55:25+00:00 at commit `4800a23cbe` by `python -m ms408.experiments.e1_meaning_detector`. Full numbers in `results/experiments/e1_meaning_detector.json`.

**Design.** Reorder the VMS's own 34,111 tokens meaninglessly (each word type clustered around a random centre). Character entropy and Zipf are unchanged by construction (verified: True); only word ORDER changes. Question: does reproducing the VMS DI require meaning?

**VMS:** DI = 0.3072 at scale 812 words (bootstrap 95% CI [0.2431, 0.3237]).

## Meaningless drift-null sweep

| spread (frac of N) | mean DI | mean peak scale |
|---|---|---|
| 0.02 | 2.196 | 1624 |
| 0.04 | 1.6516 | 2436 |
| 0.06 | 1.3049 | 3221 |
| 0.08 | 1.0483 | 3411 |
| 0.1 | 0.8442 | 4263 |
| 0.15 | 0.4686 | 3695 |
| 0.2 | 0.2225 | 4263 |
| 0.3 | 0.0302 | 2774 |

- Meaningless generator's **max DI**: 2.196 (spread 0.02, scale 1624).
- Best DI match to VMS: 0.2225 at scale 4263.
- **Reaches VMS DI: True**.

Independent corroboration: i01 encoding bracket: the self-citation null scored MZ DI 0.497 (already > VMS 0.307), at scale 275 — an independent second meaningless generator that also exceeds the VMS DI.

## Verdict [C, pending refutation pass]

MODEST claim stands, STRONG claim withdrawn. Established [C, already conceded in i01]: the DI *value* alone is not a meaning certificate — a meaningless reordering of the VMS's own words reaches and exceeds it (max 2.2 vs VMS 0.307), so a high DI value does not imply content. NOT established: that a meaningless PROCESS reproduces the VMS phenomenon, which is DI value AND its 812-word characteristic scale. The drift-null hits the value at the wrong scale; the i01 self-citation process overshot the value (0.497) also at the wrong scale (275). E2 resolves what the 812 scale IS — it is the section/topic-block scale (blocked Vulgate books peak at 812), reachable by any block-structured vocabulary, meaningful or not. Net: DI cannot settle meaningful-vs-meaningless (confirms T3.3/C5); the 812 scale is a block-structure signature, not a meaning signature.

**Refutation pass outcome (standing i02 rule).** A clean-context critic WEAKENED the first draft, correctly: (1) the drift-null installs clustering by fiat rather than via a meaningless *process*, so it shows DI measures clustering, not that meaning is unnecessary for the manuscript; (2) DI is a curve peaking at a characteristic SCALE — the drift-null matches the VMS *value* (0.307) only at the wrong scale (1624+ vs 812), and matching height but not location is not reproducing the point. The strong claim ('reproducing the manuscript's word-order information requires no meaning') is withdrawn; the modest claim ('DI value alone is not a meaning certificate') stands and was already conceded in i01.

**Implication for the flagship.** Confirms the T3.3/C5 downgrade — the meaningful-vs-meaningless question cannot be settled by MZ. E2 identifies the 812-word scale as the section/topic-block scale (blocked meaningful text peaks there too), so the scale is a block-structure signature, not a meaning signature. The anti-uniform-cipher point is separate and is tested — and survives — in E2.
