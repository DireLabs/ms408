# STATUS.md — i08 Coordination Bus

_Last updated: 2026-07-15 (spec drafted; building E23)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); L7 absolute.
Continues the experiment ledger as E23–. Directly answers the E22 negative (the
context-free positional generator is a PARTIAL account) by adding word reuse.

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E24 | Type-level small-lexicon generator | P1 | ✅ done → **real win, residual coupling [C]** | 144-config a-priori sweep (lex_size × branching × word-Zipf × block-boost). **THE WIN:** type-level concentration resolves the E23 entropy-vs-reuse tension — TTR now sits in-band JOINTLY with h2 (ttr∧h2 co-occur = True), which token-copying never could. **RESIDUAL:** ceiling 4/8; within the swept family these pairs never co-occur in-band — h2×ED1, ED1×TTR, ED1×Zipf, ED1×wc, Zipf×wc, ΔI×wc — so the obstruction is now morphology connectivity (ED1 ≈0.75 forces a regime incompatible with the rest) plus a block-contrast trade-off (retained ΔI wants weak contrast, positive wc_z wants strong). **Scope (refutation):** a COUPLING within swept ranges, not impossibility; fc_z/wc_z are 2-point ranges (not CIs) and wc_z is confounded with sectional drift → soft axes; single seed. Net i07–i08: no tested generative family reproduces the full 8-axis signature over the swept ranges. |
| E23 | Positional + reuse generator, genericity sweep | P1 gating | ✅ done → **reuse helps, Pareto tension remains [C]** | 104-config a-priori sweep (ρ × {local_w50, local_w200, global} × branching × boost). Word reuse individually rescues every axis E22 could never reach (ED1 from ρ≥0.6, TTR ρ≥0.4, Zipf ρ≥0.8) and **global preferential attachment restores the VMS's weak-positive wc_z** (+2.06, up from E22's anti-structure −1.02) — a real gain. BUT the axes are mutually constraining: **0 configs** satisfy even the whole frequency group {ED1,TTR,Zipf} at once, and **0** satisfy it jointly with {h2,ΔI,wc_z}; the reuse rate that concentrates frequency (high ρ) deflates entropy + block-ΔI and re-negates syntax. Best 4/8 (ρ=0.4 global). So low entropy + retained ΔI COEXIST with heavy reuse in a way simple token-copying can't reproduce. |

## i08 outcome (E21–E24 arc)

**Across three generative mechanisms — context-free positional (E21/E22), + token reuse
(E23), + type-level small lexicon (E24) — none reproduces the VMS's full 8-axis signature
over the swept ranges.** Each mechanism resolves the previous one's blocker and exposes a
new one: token reuse fixed the frequency axes but spent entropy/ΔI (E23); type-level
concentration fixed the entropy-vs-reuse tension (TTR now co-occurs with h2) but left a
residual coupling centred on **morphology connectivity (ED1 ≈ 0.75)** plus a block-contrast
trade-off (ΔI vs positive wc_z) (E24). Net: the VMS's summary statistics are **mutually
coupled in a way these mechanisms do not capture** — a real tightening of the constraint
envelope. **Scope (from the E22/E23 refutation, applied throughout):** this is a coupling
within bounded sweeps, NOT a proof that no generative process can match; fc_z/wc_z are
soft axes (2-point ranges, sectional-drift confound); results are single-seed. Robustness
follow-ups named: multi-seed + generator-side bootstrap; extend branching below 4 and
Zipf above 1.2; a type lexicon decoupled from the slot grammar.

**Status:** i07–i08 folded into paper v4 (with the refutation's wording corrections + E24).

## Working hypothesis

Copy-from-recent-context reuse concentrates frequency → lowers TTR, steepens Zipf, and
sparsifies the realised type set so ED1 drops off saturation; the copy adjacency lifts
wc_z from anti-structure toward the VMS's weak-positive band. If a broad a-priori basin
covers ≥6/8 axes incl. positive wc_z, the positional + reuse class is a *sufficient*
account of the full signature (B ceiling; never identification, L7). Built as a sweep
from the start to avoid E21's grid-select-then-call-it-a-priori circularity.

## Sessions

- **Code session (i08)** — spec drafted 2026-07-15; building E23.
