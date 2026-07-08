# STATUS.md — i03 Coordination Bus

_Last updated: 2026-07-08 (i03 spec drafted; awaiting Tim's ratification of the
agenda + D-i03-1/2/3)._

**Inherits:** all i01 locks L1–L34, the i02 standing refutation rule, and the five
standing corrections (README §"Standing corrections"). Continues the experiment
package as E6–E10.

## Experiments

| id | question | priority | state | verdict |
|---|---|---|---|---|
| E6 | Deterministic-verbose/nomenclator cipher — joint-signature reconstruction | P1 flagship | ⬜ blocked on E8 | — |
| E7 | Fine-granularity anchor hunt (weak/rare regime) | P2 | ⬜ ready | — |
| E8 | Whitened, continuously-tuned encoding bracket (fixes E5 residuals; feeds E6) | P2 | ⬜ ready | — |
| E9 | VMS coordinate — dose-response localization (variable-introduction flagship) | P1 flagship | ⬜ blocked on L35 | — |
| E10 | root↔leaf third independent rater | P3 | ⬜ blocked on D-i03-2 | — |

**DAG:** E8 → E6 ; E7, E9, E10 independent. Suggested run order: **E8 → E6** (cipher
reconstruction track) in parallel with **E9** (coordinate track); E7 alongside;
E10 once D-i03-2 lands.

## Open decisions for Tim

- **D-i03-1 — flagship selection.** Recommend E6 + E9 as co-flagships; E9 first if
  bandwidth-limited. Ratify / re-order.
- **D-i03-2 — E10 rater source & spend.** Human vs third vision-model vs defer.
- **D-i03-3 — ratify L35** (variable-introduction discipline: Type A/B only,
  pre-registered axes + statistic-that-moves, exploratory-until-replicated, FDR).
  Gates E9.

## What each experiment closes

- **E6** — the one cipher family i02 re-opened (E2). Positive sufficiency test, not
  decipherment (L7).
- **E7** — the weak/rare-anchor gap E3 left open.
- **E8** — the two E5-refutation holes (residual collinearity; tuning power).
- **E9** — reframes the central open question (meaningful vs meaningless) as a
  calibrated coordinate; first study under the variable-introduction framework.
- **E10** — the human-ground-truth control E4b named.

## Sessions

- **Code session (i03)** — spec drafted 2026-07-08; not yet kicked off (awaiting
  ratification).
