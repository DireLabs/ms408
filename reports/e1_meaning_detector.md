# E1 — Is Montemurro-Zanette DI a meaning detector?

Generated 2026-07-07T21:24:28+00:00 at commit `8058cdb674` by `python -m ms408.experiments.e1_meaning_detector`. Full numbers in `results/experiments/e1_meaning_detector.json`.

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

## Verdict [B, pending refutation pass]

MZ DI is NOT a meaning detector: a meaningless reordering of the VMS's own word multiset — identical character statistics and Zipf — reaches the VMS DI. Word-order information at this level does not require meaning. The i01 'meaningful vs meaningless' lean cannot rest on MZ DI.

**Scale caveat (honest).** The meaningless generator reproduces the VMS DI *value* trivially (bracketed at spread 0.15–0.20) and vastly exceeds it (max 2.2), but its broad-Gaussian clustering peaks at a *longer* scale than the VMS's 812. Matching the exact 812-word scale as well would need a block-structured drift — but that is unnecessary for the conclusion: i01's argument compared DI *values*, and a meaningless process reproduces or exceeds any DI value on the VMS's own vocabulary.

**Implication for the flagship.** This confirms the T3.3/C5 downgrade: the meaningful-vs-meaningless question cannot be settled by MZ word-order information. It must be pursued (if at all) by a statistic shown to discriminate meaning on the harness — which MZ is not. (This does not revive the anti-cipher point F5, which is that the uniform cipher destroys the vocabulary clustering the VMS has — a separate claim, tested in E2.)
