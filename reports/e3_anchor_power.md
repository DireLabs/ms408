# E3 — Anchor-hunt power curve

Generated 2026-07-07T21:38:45+00:00 at commit `34f7690875` by `python -m ms408.experiments.e3_anchor_power`. Numbers in `results/experiments/e3_anchor_power.json`.

Herbal: 129 pages, 314 tokens × 34 features = 10,676 FDR tests (q=0.05). Synthetic anchors injected at controlled phi; recovery measured against the real multiple-testing burden.

| target phi | mean realised phi | attempts | recovered | recovery rate |
|---|---|---|---|---|
| 0.2 | 0.2 | 60 | 0 | 0.0 |
| 0.3 | 0.3 | 60 | 0 | 0.0 |
| 0.4 | 0.4 | 60 | 51 | 0.85 |
| 0.5 | 0.499 | 60 | 60 | 1.0 |
| 0.6 | 0.6 | 60 | 56 | 0.933 |
| 0.8 | 0.8 | 60 | 60 | 1.0 |

- Minimum detectable effect (≥80% recovery): **phi = 0.4**.
- Moderate anchor (phi=0.4) recovered: **True**.

## Verdict [B, pending refutation pass]

The anchor hunt IS adequately powered: a moderate synthetic anchor (phi=0.4) is recovered 85% of the time, minimum detectable effect (80% power) phi=0.4. So the i01 null is INFORMATIVE: had a moderate token<->feature anchor existed, it would likely have been found. 'No strong page-level anchor' strengthens toward 'no moderate-or-strong anchor'.
