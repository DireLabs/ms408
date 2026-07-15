# STATUS.md — i08 Coordination Bus

_Last updated: 2026-07-15 (spec drafted; building E23)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); L7 absolute.
Continues the experiment ledger as E23–. Directly answers the E22 negative (the
context-free positional generator is a PARTIAL account) by adding word reuse.

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E23 | Positional + reuse generator, genericity sweep | P1 gating | ✅ done → **reuse helps, Pareto tension remains [C]** | 104-config a-priori sweep (ρ × {local_w50, local_w200, global} × branching × boost). Word reuse individually rescues every axis E22 could never reach (ED1 from ρ≥0.6, TTR ρ≥0.4, Zipf ρ≥0.8) and **global preferential attachment restores the VMS's weak-positive wc_z** (+2.06, up from E22's anti-structure −1.02) — a real gain. BUT the axes are mutually constraining: **0 configs** satisfy even the whole frequency group {ED1,TTR,Zipf} at once, and **0** satisfy it jointly with {h2,ΔI,wc_z}; the reuse rate that concentrates frequency (high ρ) deflates entropy + block-ΔI and re-negates syntax. Best 4/8 (ρ=0.4 global). So low entropy + retained ΔI COEXIST with heavy reuse in a way simple token-copying can't reproduce. |

## i08 outcome

**Reuse is a necessary improvement but not sufficient — the VMS signature is more
mutually-constraining than a positional-grammar-plus-token-copying class.** The specific
tension names the next mechanism: frequency concentration must be bought **without
spending character entropy or block-ΔI** — i.e. a genuinely small, skewed **TYPE lexicon**
with constrained morphology (concentration at the type level), rather than token-level
copying that also compresses the character grammar. Candidate next: E24 (small skewed
type-lexicon + positional morphology). **Decision point with Tim:** package i07–i08 into
paper v4 now (the "generative class characterised and constrained" story, companion to
i06's cipher exclusion), or run E24 first and fold all together.

## Working hypothesis

Copy-from-recent-context reuse concentrates frequency → lowers TTR, steepens Zipf, and
sparsifies the realised type set so ED1 drops off saturation; the copy adjacency lifts
wc_z from anti-structure toward the VMS's weak-positive band. If a broad a-priori basin
covers ≥6/8 axes incl. positive wc_z, the positional + reuse class is a *sufficient*
account of the full signature (B ceiling; never identification, L7). Built as a sweep
from the start to avoid E21's grid-select-then-call-it-a-priori circularity.

## Sessions

- **Code session (i08)** — spec drafted 2026-07-15; building E23.
