# E9 Pre-Registration — VMS Coordinate (dose-response localization)

**Committed before any E9 code runs (L35).** This file fixes the axis set, the
statistic-that-moves per axis, the endpoints, and the **predicted** VMS position,
so no post-hoc axis selection or direction-flipping can occur. Amendments must be
dated additions below, never edits to the registered rows.

**Frame.** i02 showed the meaningful-vs-meaningless question is not settled by any
single statistic as a binary (E1: ΔI is block-structure; E5: no family
distinguished). E9 reframes it as **localization**: on each interpretable axis, a
generator parameter is swept from a known-**meaningful** endpoint (real text) to a
known-**meaningless** endpoint (structure-matched null), the axis's statistic is
calibrated across the sweep, and the **VMS is placed as a coordinate** (0 =
meaningless endpoint, 1 = meaningful endpoint) by inverting the calibration at the
VMS's observed statistic value. Bootstrap CIs on every coordinate.

**Type (L35).** Type B — synthetic ground-truth variables. All endpoints have known
answers; the VMS is the only unknown placed against them.

## Registered axes

| # | Axis | Generator parameter swept | Meaningful endpoint (coord 1) | Meaningless endpoint (coord 0) | **Statistic-that-moves** (pre-committed) | **Predicted VMS coordinate** |
|---|---|---|---|---|---|---|
| A1 | Word-order information | phrase/block coherence of token order | real Latin/German text, natural order | fully token-shuffled (same unigrams) | Montemurro–Zanette ΔI peak value | **mid-high (~0.5–0.8)** — E1/E2 say VMS has real order-structure, but it indexes block structure, so not saturated at 1 |
| A2 | Homophony degree | fraction of types with multiple spellings (E5 verbose knob), scored **inverted** so 1 = type-preserving | deterministic / type-preserving (retains ΔI) | heavy-homophony (collapses type identity) | type–token coupling (ΔI retention ratio) | **high (~0.7–1.0)** — E2: VMS retains ΔI, so it sits toward the homophone-poor end |
| A3 | Morphological-paradigm strength | conlang paradigm fraction `p` (shared-stem templates) | dense paradigm (ED1 network) | atomic lexicon (no network) | edit-distance-1 main-component share | **very high (~0.8–1.0)** — F12: VMS ED1 ≈ 0.80, far above natural language |
| A4 | Vocabulary drift / source-locality | region-specific vocabulary drift rate across sections | one coherent source (low drift) | independent per-section vocab (max drift) | section↔text co-variation (adjusted Rand index) | **mid (~0.3–0.6)** — F8: VMS Language-A ARI ≈ 0.35, moderate section coherence |

**Reading the coordinates jointly (pre-committed interpretation).** A profile that
reads **meaningful-like on A1+A4 but is only reachable via A3's constructed
paradigm** would point to *constructed morphology*, not natural-language meaning.
A profile **high on A2+A3 but low on A1** would point to *structured-meaningless*.
No single axis is decisive; the coordinate VECTOR is the deliverable.

## Method (pre-committed)

- Each axis: sweep its parameter over ≥11 points between the two endpoints;
  generate on the same corpus length as the VMS; compute the axis statistic at each
  point (mean over ≥5 seeds); fit a monotone calibration curve; the VMS coordinate
  = inverse-interpolated position of the VMS's observed statistic on that curve,
  clamped to [0,1] and reported with the raw (unclamped) value.
- **Bootstrap:** block resample (block > 812) the VMS ≥150× to get a CI on each
  coordinate. Endpoints also bootstrapped to confirm they anchor at ~0 and ~1.
- **Multiple testing:** the four axes are one pre-registered family; any "VMS is
  distinctively meaningful on axis X" claim is BH-FDR corrected across the four.
- **Refutation trigger:** every axis whose VMS coordinate lands in the
  meaningful-leaning region (>0.6) gets a dedicated refutation pass asking whether
  the position is an artifact of the parameterization (e.g., the statistic is
  monotone in a nuisance property like word length or inventory size, not the
  intended axis). Logged in the E9 verdict.

## Grading (pre-committed, L35)

All per-axis coordinates are **grade D (exploratory)** in E9 itself. A coordinate
rises above D only when independently replicated — a *different* statistic for the
same axis, or a held-out corpus — in a later confirmatory experiment. E9's
success = a reproducible coordinate vector with CIs + the single most promising
axis nominated for that confirmatory follow-up. No meaningful-vs-meaningless
verdict is issued from E9 alone.

## Falsifiable pre-commitments (scored after the run)

1. If **A3** (paradigm) coordinate is NOT high (≥0.7), the F12 ED1 result is weaker
   than believed — a surprise that would itself be a finding.
2. If **A1** (word-order) saturates at ≥0.9, E1's "block-structure not meaning"
   framing is challenged (the VMS would look maximally ordered, not mid).
3. If **all four** coordinates land meaningful-leaning (>0.6), the
   structured-meaningless hypothesis weakens; if A1/A4 land low while A2/A3 land
   high, it strengthens.
