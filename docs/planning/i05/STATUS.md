# STATUS.md — i05 Coordination Bus

_Last updated: 2026-07-09 (spec drafted; starting E13, the function/content probe)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); A/B
stratification (L8); harness-first (L4, extended to mid-level probes). Continues the
experiment ledger as E13–E16. Theme: build the mid-level grammar (morphology →
word-classes → syntax), stratified by Currier A/B; characterise grammar, not meaning
(L7).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E13 | Function-word vs content-word bimodality | P1 flagship | ✅ done → **inconclusive (probe failed calibration)** | [D] Three global operationalisations (neighbour-entropy promiscuity; freq–dispersion-evenness correlation; evenness variance) all FAIL to separate has-grammar from generated calibration corpora — so NO VMS function/content verdict is issued (harness-first: an uncalibrated probe yields no manuscript claim). Learnings: global stats are TTR/randomness-confounded; the self-citation & conlang nulls are contaminated (they inherit real grammar). **Redesign (E13b):** explicitly identify candidate function words (top-freq, cross-section-stable) and test even-dispersion + position-locking vs matched content words, against CLEAN nulls (shuffle/markov only). |
| E13b | Function/content via collocational selectivity (redesign) | P1 | ✅ done → **inconclusive (failed calibration)** | [D] 4th operationalisation; the content−function selectivity gap doesn't cleanly separate real language (0.081) from the shuffle null (0.051; sep 0.03 < 0.05) — peak selectivity is sample-size-confounded (content band is lower-freq → inflated). NET across E13+E13b: **the function/content probe is not cleanly detectable with word-stream corpora** (function words ARE the high-freq ones → can't frequency-match vs content; nulls each preserve different structure). Parked pending sentence-segmented controls + a frequency-matched design. |
| E14 | Distributional word-class (POS) induction | P2 | ⬜ ready | — |
| E15 | Morphology segmentation & productivity | P2 | ✅ done → **inconclusive (n-confounded measure)** | [D] Paradigm-coherence (top-10 sigs / n) separates cleanly with a token-shuffle null (0.41) but that null is invalid (same word types as Latin); with a proper within-word char-shuffle null the measure is n-confounded (char-shuffle 0.44 > Latin 0.41 via small n), separation 0.10 < 0.15 → no VMS verdict. Descriptive values are suggestively ordered (VMS-A 0.29 / B 0.35 below Latin 0.41, far below conlang 0.98, above abjad 0.16 — hinting only-partly-paradigmatic) but NOT trusted without n-correction. |

## Null-correction framework (built) + corrected re-runs

`src/ms408/experiments/mid_level_null.py` — `null_z()` expresses each corpus's raw
statistic as a z-score vs a matched-null ensemble holding its OWN nuisance parameters
fixed, so z is comparable across corpora and VMS-A vs VMS-B directly.

| id | probe (corrected) | state | verdict |
|---|---|---|---|
| E13c | Function/content, order-shuffle null | ✅ done + refuted → **narrowed** | [C] **CALIBRATED** (real langs latin z=19, german z=8.5). Refutation corrected the framing: NOT "undifferentiated/no grammar". Narrow SURFACE finding — VMS has only weak near-chance surface collocation in both bands (excess over shuffle ~0.01–0.02 vs real-language content 0.15), NO natural-language content>function gap, and its most-FREQUENT words are marginally MORE collocational than content words (template-like daiin/ol/chedy repeats, the OPPOSITE of flat real function words). Holds in A AND B. **Scope (L7): surface collocation only** — a cipher/morphology/low-repetition could erase surface collocation while preserving grammar; does NOT say "no grammar". First substantive i05 result. |
| E15b | Morphology coherence, random-signature null | ✅ done → still inconclusive | [D] n-confound removed, but calibration STILL fails — collision nulls induce spurious signature structure (char-shuffle z=15.8, abjad z=5.3 both clear the bar). No clean "no-morphology" null; VMS z (11–15) high but so is char-shuffle. |
| E13d | Band-cutoff robustness for E13c | ✅ done → **E13c ROBUST** | [C] The critic's decisive check. On all CLEAN (non-overlapping) band cells (function top-2/5% × content 5-30/5-60): Latin gap-z 15–20 (present everywhere), VMS-A [−1.3,−1.0] / VMS-B [−7.2,−4.8] (absent everywhere), inversion stable. Instability appears ONLY in degenerate overlapping-band cells where even Latin flips (z=−10.9) → band-specification artifact, not VMS fragility. E13c's finding is confirmed, not a cutoff artifact. |

**Meta:** the framework converted ONE of two probes (function/content) from confounded
to answerable — a genuine methodological win. Morphology (E15b) needs a fundamentally
cleaner null (char-shuffle preserves character constraints that fake signatures);
deferred. E14 (POS induction) / E16 (dependency) should be built with null-correction
from the start.
| E16 | Grammar depth: long-range dependency | P3 | ⬜ ready | — |

## Standing rule (i05)

Every probe: calibrate on H4 real languages + nulls/generators → state the decision
rule → run on VMS-A and VMS-B (+ v101) → refutation pass → grade. The A-vs-B contrast
is the headline deliverable (Tim's "two different processes?" hypothesis).

## Notes / carry-forward

- Gemini (Google) billing enabled and key authorized, but the API is returning 503
  (capacity) as of 2026-07-09 — retry later; NOT needed for i05 (text-only) or for the
  root↔leaf question (E12: underpowered, moot).
- Paper v1 shipped (through E12). Re-run `/package-paper` after i05 for v2.

## Sessions

- **Code session (i05)** — spec drafted 2026-07-09; building E13.
