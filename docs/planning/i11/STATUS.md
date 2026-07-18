# STATUS.md — i11 Coordination Bus

_Last updated: 2026-07-17 (Tier-0 release engineering: public evaluate() API + bands + docs;
v6b ledger correction of the ~30σ/grammar slips; E29 run + refuted → C)._

**Inherits:** all locks; standing refutation rule; firewall (L3); harness (L4); L7 absolute;
L8; **L19 consume-only** (Naibbe raw data in `data/raw/`, gitignored, not redistributed).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E31 | Harden the fc_z/wc_z syntax discriminators | P1 | ✅ done → **robust leg FIRMED; homophonic still open [B]** | Deconfounds (local within-block null = grammar only, vs global-shuffle) + subsample CI + seed-stability SD. Findings: (1) the VMS's weak-positive wc_z is REAL grammar, not sectional drift (global 1.98 ≈ local 1.97) — rehabilitates the measure vs the earlier "it's drift" assumption; (2) the measures are STABLE to seed noise (SD 0.19–1.2), so E30's apparent instability was cross-config variance; (3) block-bootstrap WITH replacement is INVALID here (duplicate blocks inflate collocation) — use subsampling without replacement. Re-adjudication: order-preserving cipher separable from VMS by ~30σ (fc_local) → exclusion FIRM, NOT dependent on the 2-point band or drift; verbose+homophonic sits in the VMS weak-syntax regime, NOT jointly separable → still NOT excludable (Naibbe viable). E30 partition survives hardening. |
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

## Correction (2026-07-17, v6→v6b refutation) — read the E31 row with these fixes

The E31 narrative cell above carries two claims the clean-context refutation on paper v6
overturned; the corrected values (from `results/experiments/e31_harden_syntax.json`) are:
- **NOT "~30σ".** Order-preserving separability is **6.8σ (fc_local) / 8.0σ (wc_local)**.
  "~30σ" was a recalled number in no result JSON (an L1 firewall slip) — do not reuse it.
- **NOT "REAL grammar".** The VMS `wc_local` 90% CI is **[-1.44, 1.94]**, which crosses
  zero; the point 1.97 is not a grammar claim. The order-preserving exclusion still holds
  (6–16 vs a CI near zero), but the "weak-positive is real grammar" sub-claim is withdrawn.
- Honest partition (v6b): order-preserving ciphers robustly excluded; verbose+homophonic
  (Naibbe-class) **inconclusive** (1/64 seed-configs hit the corner; 1.2σ) — neither excluded
  nor robustly reached. Paper **v6b** and methods **v3** are the current honest statements.

## Release engineering (2026-07-17) — repo packaged as a public evaluator (Tier 0)

Per the open-source-tool pivot and the release-readiness assessment
(`docs/RELEASE-READINESS.md`). Decisions locked: name **ms408**, license **Apache-2.0**,
scope **evaluator + methodology + reproductions**.
- Public API `ms408.evaluate(tokens)` (`src/ms408/signature.py`) + CLI `python -m ms408`:
  per-axis {value, band, in_band} with each axis's caveat attached; hard axes {h2, ed1,
  zipf}; dI flagged confounded (E29) and uncounted; ttr advisory (token-sensitive); fc/wc
  soft (VMS CIs cross zero). Matching = necessary not sufficient (L7 note in every verdict).
- Reference bands built firewall-clean by `e32_reference_bands` →
  `src/ms408/data/reference_bands.json` (committed, shipped). **Subsample-without-
  replacement** throughout (fixes a real bug: block-bootstrap-with-replacement put the VMS
  OUTSIDE its own TTR/Zipf band — the duplicate-block bias E31 flagged). Self-consistency:
  VMS 3/3 hard; raw Latin 0/3.
- LICENSE + NOTICE (Greshko/ZL attributions, consume-only), README, `docs/METHODOLOGY.md`
  (refutation as protocol not code), `docs/LIMITS.md`. `anthropic` → optional `vision`
  extra (core import anthropic-free). Full suite **174 passed**; ruff clean; wheel builds
  and ships the bands.
- **Deferred (Tier 1+):** pin discriminator values in tests against acquired data on CI;
  worked "evaluate the Naibbe cipher" example; reproduce-the-paper `--verify` path; the
  block-scale like-for-like ΔI test the v6 refuter flagged as the one untested ΔI leg.
