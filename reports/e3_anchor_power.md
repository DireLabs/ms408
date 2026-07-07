# E3 — Anchor-hunt power curve

Generated 2026-07-07T21:50:46+00:00 at commit `6fb18eb360` by `python -m ms408.experiments.e3_anchor_power`. Numbers in `results/experiments/e3_anchor_power.json`.

Herbal: 129 pages, 314 tokens × 34 features = 10,676 FDR tests (q=0.05). Synthetic anchors injected at controlled phi; recovery measured against the real multiple-testing burden.

| target phi | mean realised phi | attempts | recovered | recovery rate |
|---|---|---|---|---|
| 0.2 | 0.2 | 60 | 0 | 0.0 |
| 0.3 | 0.3 | 60 | 0 | 0.0 |
| 0.4 | 0.4 | 60 | 51 | 0.85 |
| 0.5 | 0.499 | 60 | 60 | 1.0 |
| 0.6 | 0.6 | 60 | 58 | 0.967 |
| 0.8 | 0.8 | 60 | 60 | 1.0 |

- Minimum detectable effect (≥80% recovery, averaged): **phi = 0.4** — but this hides prevalence dependence (below).

### Power at phi=0.4 by feature prevalence (the refutation's key point)

| feature prevalence | features in band | recovery rate |
|---|---|---|
| rare (<20 pp) | 14 | 0.725 |
| mid (20-45 pp) | 8 | 1.0 |
| balanced (45+ pp) | 12 | 1.0 |

## Verdict [B, refutation pass applied]

The power ANALYSIS is sound but the 'null is informative' claim is OVERSOLD. Recovery is a cliff: phi<=0.3 -> 0%, phi=0.4 -> 85%. And power is strongly prevalence-dependent at phi=0.4 — rare features 0.725, mid 1.0, balanced 1.0. Honest bound: the i01 anchor hunt EXCLUDES only STRONG, prevalence-balanced anchors (phi>=0.4 on common features); it does NOT exclude the WEAK (phi 0.2-0.35) or RARE-feature anchors that a genuine but imperfect herbal cipher would most plausibly produce. So the i01 null is a WEAKER constraint than the flagship implied — it bounds the anchor away from the strong-signal corner, no more. The real test is finer (label-adjacency) granularity, deferred.
