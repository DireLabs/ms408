# Limits — read before quoting any number from this tool

`ms408.evaluate()` tells you which of the Voynich manuscript's statistical properties a
token stream reproduces. That is a **necessary, not sufficient** test (binding rule L7):
landing in-band means your hypothesis is *not excluded*, never that it is the manuscript's
mechanism. Plausible-looking output is the field's primary failure mode; this tool is
built to withhold, not to confirm.

## Token budget (a minimum, and a comparability floor)

`evaluate()` **refuses inputs below 1,000 tokens** with a clear error: the MZ word-order
scan and the mid-level syntax z's are undefined or unstable on short streams, and a tiny
sample would otherwise crash or — worse — report a confident but meaningless verdict. The
reference bands are built at **10,000 tokens**; below ~8,000 the axes (especially the
token-sensitive `ttr`, and the confidence intervals) are not strictly comparable, and the
verdict carries a `LOW TOKEN BUDGET` note. Evaluate near 10,000 tokens where you can.

## Dialect: there is no single "the manuscript" band set

**The bands are stratified by Currier dialect** (D21). `evaluate()` scores your stream
against Currier A and Currier B separately and reports both; `evaluate(tokens,
dialect="B")` scopes to one. There is no pooled band set, because pooling the two is not
meaningful: A and B are different generative regimes, and each one's point sits outside the
other's hard bands on every axis.

This replaced a single band set labelled "Currier A+B" that in fact contained only A — the
A and B streams were concatenated and truncated at the 10,000-token budget, and A alone
supplies 10,709 tokens, so no B token ever reached it. Currier B, 22,864 tokens and 68% of
the manuscript, then scored 0–1 of 3 hard axes against "the manuscript's" own bands.

**What this means when you read a verdict.** In-band for one dialect is *not* in-band for
the manuscript. Always report which dialect you matched. A generator tuned to A's low-ish
entropy is not thereby a model of the majority of the text.

### How representative each dialect's bands are

Each dialect's bands are built from the **first 10,000 paragraph tokens of that dialect in
page order** — the same rule for both, so the two sets are like-for-like. That is 93% of
Currier A but only 44% of Currier B. `ms408.experiments.e34_band_dialect_scope` slides
matched-budget windows at 1,000-token strides and scores each against its own dialect's
bands:

| dialect | windows | `h2` in own band | `ed1` in own band | best | worst | best vs *other* dialect |
|---|---|---|---|---|---|---|
| Currier A | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 |
| Currier B | 14 | 9/14 | 2/14 | 2/2 | 0/2 | 0/2 |

Two things to take from this, in order of importance:

1. **Currier B's bands generalise poorly to the rest of Currier B**, especially on `ed1`
   (2 of 14 windows). B's later folios differ from its earlier ones by more than the band
   width. Treat a B verdict as calibrated against *early* B, and an out-of-band B result as
   correspondingly weak evidence. A's bands do not have this problem, but A is also 93%
   covered by its own sample, so that is close to a tautology rather than a strong result.
2. **The dialects genuinely separate.** No B window reaches even 1 of 2 hard axes against
   A's bands. Stratifying is showing structure, not manufacturing it.

The windows overlap, and each dialect's first window *is* its band sample, so these counts
describe coverage — they are not independent samples and not a significance test.

Whether to rebuild B's bands from a spread sample rather than a page-order prefix is an
open follow-up (`D24`); it is left alone for now because choosing a sampling scheme
*because* it improves a coverage statistic is the kind of post-hoc tuning L35 exists to
prevent.

## The single manuscript (n = 1)

The reference bands come from one artifact resampled by subsampling its own blocks. That
captures internal variability, not true sampling variability across a population of such
manuscripts, which does not exist. Bands are a **reproducibility envelope**, not a
frequentist confidence statement about a population.

## Axis-by-axis

| axis | status | what it does and does not support |
|---|---|---|
| `h2` | **hard** | Conditional character entropy, **Lindemann–Bowern convention: the space counts as a character and bigrams span word boundaries** (`textstats.lb_entropies`). Robust and substitution-invariant. A genuine anomaly of the manuscript; among the strongest axes. ⚠️ The literature also calls the *within-word* statistic (`textstats.char_conditional_entropy`, no space, no boundary-crossing) "h2", and it gives a materially different number on the same text — this repo uses both, for different reference targets. Never compare an h2 across sources without checking which convention each used. |
| `ed1` | **hard** | Edit-distance-1 morphology main-component share. Robust; captures the tight morphological network. But see the dialect section: it is the axis on which Currier B's bands generalise worst within B. |
| `zipf` | **advisory** (was hard, until D23) | Zipf slope, least-squares over ranks [10, 1000] (or to the last type if fewer). **Token-count-sensitive**, so not banded and not counted. The fixed rank window runs into the count-saturated tail on smaller samples — at 7,500 tokens the ranks near 1000 are mostly frequency-1, which flattens the fit — so the subsample CI is biased off the full-sample point. Measured bias: −0.005 in Currier A (small enough to hide inside a 0.032-wide CI) but **+0.059 in Currier B against a 0.025-wide CI**, which put B's own point outside B's own band. Only compare at a similar token budget. |
| `dI` | **confounded** | Montemurro–Zanette word-order information. **Collapses under homophony alone and under re-spacing alone** (E29) — it is a homophony / type-token-coupling detector, not a clean word-order measure. An in-band `dI` is weak evidence; never read it as "intact word order." Not counted in the hard tally. |
| `ttr` | **advisory** | Type-token ratio. Intrinsically token-count-sensitive (fewer tokens → higher TTR). Not banded and not counted; only compare at a token budget close to the VMS reference. |
| `fc_z_local`, `wc_z_local` | **soft** | Mid-level syntax (function/content collocation gap; adjacent word-class NMI) vs a *within-block* null that removes topic-drift confound (E31). **Soft: the VMS's own subsample CI crosses zero.** An in-band soft axis is weak evidence. |
| `fc_z_global`, `wc_z_global` | **soft + confounded** | Same measures vs a *global* order-shuffle null. Additionally **confounded by section/topic vocabulary drift** (E22): a block-wrapper control with no grammar can reproduce them. Reported for transparency and to expose the drift share against the local versions. |

**"Soft" is a property of Currier A, not of the manuscript.** All four syntax bands cross
zero in A. In **B** three of them do not: `fc_z_local` is [−3.87, −0.66], `fc_z_global` is
[−5.74, −1.22], and `wc_z_global` is [0.29, 3.63] — all entirely off zero. This became
visible only when the bands were split by dialect (D21); the pooled artifact was A, so
"the syntax axes are soft" was really "the syntax axes are soft in A." The axes are still
flagged soft everywhere, because the flag is a floor on how much weight to put on them and
because **this observation has not been through adversarial review** (L10) — it is
recorded here as an artifact-level description, deliberately ungraded, and is raised as
`D25` for a proper look. Do not cite it as a finding about Currier B's syntax.

**The honest partition on the cipher question.** Word-order-*preserving* ciphers of a real
language are robustly separable from the VMS on the deconfounded syntax axes; a
*verbose + homophonic* (Naibbe-class) cipher is **not** cleanly excluded — the evidence is
inconclusive there, converging with Greshko (2025). Do not use this tool to claim a cipher
is "ruled in" or "ruled out" beyond that partition.

## What the tool is not

- **Not a decipherment or translation.** It reports statistics, never meaning or value.
- **Not the refutation protocol.** The adversarial-review discipline
  (`docs/METHODOLOGY.md`) is human-run, uses a fallible same-model-family LLM, and is not
  code in this repository. "Survived refutation" ≠ "true."
- **Not a stylometric fingerprint.** Matching the bands says your generator lands in the
  same statistical envelope, not that it works the way the manuscript does.

## Determinism and versioning

`evaluate()` is deterministic given its seed. The bands carry the git commit and
parameters that produced them (`verdict["band_provenance"]`); if you rebuild the bands
with different code, re-pin the tests. Every number here is reproducible from committed
code plus acquired data.
