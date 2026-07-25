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

## The single manuscript (n = 1)

The reference bands come from one artifact resampled by subsampling its own blocks. That
captures internal variability, not true sampling variability across a population of such
manuscripts, which does not exist. Bands are a **reproducibility envelope**, not a
frequentist confidence statement about a population.

## Axis-by-axis

| axis | status | what it does and does not support |
|---|---|---|
| `h2` | **hard** | Conditional character entropy. Robust and substitution-invariant. A genuine anomaly of the manuscript; among the strongest axes. |
| `ed1` | **hard** | Edit-distance-1 morphology main-component share. Robust; captures the tight morphological network. |
| `zipf` | **hard** | Zipf slope. Reasonably sample-stable; mild finite-sample sensitivity. |
| `dI` | **confounded** | Montemurro–Zanette word-order information. **Collapses under homophony alone and under re-spacing alone** (E29) — it is a homophony / type-token-coupling detector, not a clean word-order measure. An in-band `dI` is weak evidence; never read it as "intact word order." Not counted in the hard tally. |
| `ttr` | **advisory** | Type-token ratio. Intrinsically token-count-sensitive (fewer tokens → higher TTR). Not banded and not counted; only compare at a token budget close to the VMS reference. |
| `fc_z_local`, `wc_z_local` | **soft** | Mid-level syntax (function/content collocation gap; adjacent word-class NMI) vs a *within-block* null that removes topic-drift confound (E31). **Soft: the VMS's own subsample CI crosses zero.** An in-band soft axis is weak evidence. |
| `fc_z_global`, `wc_z_global` | **soft + confounded** | Same measures vs a *global* order-shuffle null. Additionally **confounded by section/topic vocabulary drift** (E22): a block-wrapper control with no grammar can reproduce them. Reported for transparency and to expose the drift share against the local versions. |

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
