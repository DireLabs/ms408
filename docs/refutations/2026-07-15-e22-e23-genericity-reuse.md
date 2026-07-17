# Refutation — E22/E23 ("no generative family / structurally unreachable"), 2026-07-15

_Clean-context adversarial pass. Preserved from the session's adversary output._

## Verdict: grade C correct on both; the public wording over-reaches.

The underlying negatives are real, but "structurally unreachable / never at any tuning / more
mutually constraining than any generative family we have tested" is stronger than the grid
licenses, and two of the eight axes carrying the headline are methodologically soft.

## Accepted points

1. **"Structurally unreachable" → "coupling within swept ranges."** Each "never matched" axis
   has an obvious untested lever pointing the right way: `mean_word_length` is *frozen* at
   ~5.19 by `P_PRESENT`/slot-count (a ~1.4% near-miss, not structural); `zipf_slope` is capped
   at the grid's Zipf-exponent boundary (1.2) exactly where TTR first enters band; `ED1` falls
   monotonically toward band as branching rises (1.0→0.887) and the grid was cut two steps
   short. The honest content is a **coupling** (h2↔ED1↔TTR through the branching knob), not an
   impossibility.
2. **fc_z/wc_z are soft.** Their "bands" are the two Currier-A/B point estimates treated as an
   interval (no CI), and wc_z is hyper-unstable (ranges to ~140 under mild reuse). The E22
   control (real Latin *types* under a block wrapper) reproduces the VMS's weak-positive wc_z
   **with no reuse at all** → that "positive" signal is sectional vocabulary drift, not grammar.
   Do not lean on it.
3. **Report the ceiling** (E23 max 4/8; "0/104 ≥6/8" is far, not knife-edge), and disclose the
   Zipf-exponent × reuse cross-slice was never run, so "token copying cannot concentrate
   frequency without spending entropy/ΔI" holds only at the swept exponent.
4. **Cleared (reported so the maintainer doesn't chase):** no seed/state-leak; the module-global
   mutation and ρ=0 dedup are correct.

## Fixes applied
Narrowed the three headline phrases to "coupling within bounded sweeps, not impossibility";
flagged fc_z/wc_z as soft 2-point ranges + sectional-drift confound; reported the 4/8 ceiling;
added single-seed + fixed-length/slot-count scope caveats. Fed forward into E24–E26 and the
paper Limitations.
