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
| E15 | Morphology segmentation & productivity | P2 | 🔷 in progress (firmer ground: ED1 network + clean abjad/Latin contrast) | — |
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
