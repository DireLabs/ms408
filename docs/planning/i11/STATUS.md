# STATUS.md — i11 Coordination Bus

_Last updated: 2026-07-17 (E29 run + refuted → C; i06 ΔI leg flagged confounded)._

**Inherits:** all locks; standing refutation rule; firewall (L3); harness (L4); L7 absolute;
L8; **L19 consume-only** (Naibbe raw data in `data/raw/`, gitignored, not redistributed).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E30 | Cipher exclusion re-examination (post-E29, multi-seed) | P1 gating | ✅ done → **i06 headline RETRACTED, robust core kept [C]** | Blocked WORD-BOUNDARY Latin (no respacing), 8 seeds/cipher. ROBUST: order-preserving ciphers (subst/verbose/abjad/nomenclator) carry STRONG syntax (fc_z 11–21) the VMS lacks → robustly EXCLUDED (large stable gap, soft-value-independent). NOT ROBUST: verbose+homophonic (≈ Naibbe) scatters at the VMS corner edge — several configs robustly hit 3/4 axes, one seed hit 4/4, but no config reaches 4/4 in ≥half of seeds, and wc_z swings 2–6 across seeds (soft measures unstable). So homophonic/verbose ciphers are NOT excluded → **Naibbe viable on our own analysis** (converges with Greshko). i06's universal "cipher EXCLUDED" retracted → "order-preserving excluded; homophonic not excluded." Homophonic verdict is soft-measure-limited → E31 (harden fc_z/wc_z). |
| E29 | Naibbe cipher vs the i06 discriminators | P1 gating | ✅ done + **REFUTED → C** | First pass read "i06 CONFIRMED [B]" (Naibbe ΔI collapses to 0.0035). Refutation killed it: word-boundary Latin ΔI = **0.0758 (IN the VMS band)**; **~82% of the ΔI loss is from Greshko's respacing, before the cipher**; and ΔI collapses under homophony alone with word order fixed (H-sweep). So Naibbe's ΔI collapse is a respacing+homophony artifact, NOT an informative test; ΔI is homophony-confounded, not a clean word-order axis; and the VMS's ΔI is block structure (not like-for-like). **i06 NOT confirmed against Naibbe**, and the exposed confound weakens i06's ΔI leg. |

## i11 outcome (so far) — and the important correction

**The make-or-break Naibbe test did not confirm i06; it exposed a confound in i06's own ΔI
leg.** Engaging the concurrent literature (as the external review demanded) revealed that:
- real word-boundary Latin sits IN the VMS ΔI band (0.076), so "the VMS retains ΔI that
  ciphers can't" is misleading;
- ΔI is confounded with homophony and with word-spacing, so it is not the "robust" axis i06
  leaned on;
- the cipher-of-real-prose exclusion therefore rests more on the SOFT fc_z/wc_z syntax
  measures than paper v3–v5b state.

**D-item i11-c — re-examine i06 (flag, don't over-correct).** Do NOT declare i06 dead: the
exclusion may still hold on cleaner axes — the ~10σ syntax gap for order-preserving ciphers,
or a low-h2 ↔ collapsed-ΔI mutual exclusivity on the h2×ΔI plane (untested). This needs a
dedicated experiment (E30). Meanwhile FLAGSHIP + the papers must flag the ΔI-leg confound and
soften the i06 headline; the soft-measure concern (already flagged in v5b) is now the load-
bearing one for the cipher exclusion.

**Net for the publish question:** engaging Naibbe (the right move) weakened our one novel
result rather than strengthening it — an honest, valuable correction, and a live demonstration
of the refutation architecture (a would-be headline caught before it reached the cipher's
author). E29's data engage the live Naibbe/Parisel debate regardless of the i06 fate.

## Open decisions
- **i11-a** cite/engage Naibbe + Parisel in FLAGSHIP + papers (still required).
- **i11-b** harden the soft mid-level measures (now the load-bearing leg of the cipher exclusion).
- **i11-c** E30 — re-examine i06 on cleaner axes (above).
