# Refutation — E33 (block-scale like-for-like ΔI), 2026-07-22

_Clean-context adversarial pass, briefed to attack E33's conclusion. The reviewer re-ran the
experiment and tested the ΔI measure, the homophony model, the tolerance logic, and seed
stability with its own code._

## Verdict: CORRECT E33 — the conclusion had the direction BACKWARDS. → fixed and re-run.

E33 first concluded "a verbose+homophonic cipher reaches the VMS's (h2, block-ΔI) corner →
block-scale ΔI does NOT separate → the ΔI leg is dead even at block scale." The single
corner hit existed **only because the shared `_homoph` model prefixes `"{i}#"` to every
token**, injecting a constant `#` and small-range digit that deflate h2 by ~0.34 bits and
drag the block-ΔI-matching config down into the VMS h2 window. Under a fair in-alphabet
homophony model, **no config reaches the corner** and the plane *separates*. So the headline
mechanism was wrong; the honest direction is "block-scale ΔI **weakly separates**
verbose+homophonic ciphers," the opposite of "ΔI leg dead."

## Confirmed sound (survived attack)
- **Max-over-scales is not the culprit.** The corner survived under `mean` aggregation too;
  max inflates VMS and cipher symmetrically (both peak at the fine p=30 partition).
- **N_NULL=4 is a stable floor.** VMS block_di ∈ {0.163, 0.162, 0.162, 0.161, 0.163} for
  N_NULL ∈ {2,4,8,16,32}; ≈0.161–0.162 across null-seed bases.
- **Seed-stable.** With the (defective) marker model, (vx2,h5) was a corner in all 5 top-level
  seeds — robustly an artifact, not a lucky seed.
- **A/B mixing does not inflate the VMS corner.** A-only block_di 0.162, B-only 0.189, mix
  0.162 — the mix tracks A-only, manufacturing no excess block-ΔI.
- **No firewall violation.** E33's verdict/report strings are fully templated from the results
  dict; no recalled/hardcoded statistics.

## Disqualifying / must-fix (fixed)
1. **[disqualifying] The `#`/digit homophony marker corrupts the h2 axis and was the SOLE
   reason the corner was reached.** Same config (vx2,h5), same block_di 0.1538, only the
   homophony marker changed: dirty `#`/digit h2 = 2.13 (in the VMS window → CORNER) vs clean
   in-alphabet suffix h2 = 2.39 (0.24 above, 3× tolerance → NOT a corner). Even at zero
   homophony the marker alone dropped h2 from 2.30 to 1.96 (a 0.34-bit artifact). Under a full
   clean sweep, 0 configs reach the corner; closest normalized distance ~2.84 vs the reported
   0.69. **Fix applied:** E33 now uses a local `_vhomoph` = deterministic verbose (low h2) +
   an in-alphabet suffix homophony (no markers) — the reviewer's own suggested model, and the
   conservative choice (most favourable to the cipher). Re-run: **0 corners, closest distance
   1.36**, verdict corrected to "weakly separates; the ΔI leg is not dead at block scale."

## Should-fix (addressed)
2. **Word-length mismatch not reported.** The corner cipher had mean word length ~12–17 vs the
   VMS's 5.03 — a third axis of non-like-for-likeness on the character-entropy plane. E33 now
   reports `mwl` for every config and the closest config, and the verdict flags it (the only
   configs that even approach on (h2, block-ΔI) do so at expansion 3, word length ~16.7).
3. **The knife-edge argued the other way.** "1 of 24 configs in a generous tolerance" was weak
   evidence of separation, not "not separable." Under the fair model the knife-edge is gone.
4. **"Closes the open item" overstated.** E33 now says the block-scale ΔI leg is *addressed and
   corrected* — it weakly separates and does not revive ΔI into a hard standalone discriminator;
   the program-level verbose+homophonic disposition still rests on the soft syntax measures.

## Note carried forward
The defective `_homoph` marker also distorts the h2 axis wherever E30/E31 compare a
verbose+homophonic cipher's h2 to the VMS (E30 uses h2 as one of four bands; E31 uses a single
fixed config). Neither E30 nor E31's disposition ("verbose+homophonic inconclusive") depends on
that h2 leg — but a future pass should re-run them with the fair homophony model to confirm.
