# Refutation — E21 (positional generator, "class sufficiency [B]"), 2026-07-15

_Clean-context adversarial pass. Preserved from the session's adversary output._

## Verdict: downgrade **B → C**.

E21's grading gate (`core AND n_nec≥3 → B`) was propped up by definitional slack, and the
headline "sufficiency of the CLASS, built BLIND to the VMS" was contradicted by the code.

## Decisive points (all accepted)

1. **Circularity — the "a-priori / blind / firewall" framing is false as written.** The
   constants (`SLOT_SIZES`, `ZIPF_EXP`, `THEME_BOOST`) were **grid-selected** to land in the
   VMS core-three band — grid-search-and-select-on-target is fitting to a VMS statistic, the
   same move that made E19's "favours generation" positive circular. h2 landing in a ~4%-wide
   band, and the ΔI peak sitting exactly at `BLOCK_LEN`, are tuned outcomes, not generic ones.
   So E21 shows the **existence of a fitted point, not sufficiency of a class**.
2. **The weak-syntax leg is scored against a threshold a full order-shuffle also passes**
   (`fc_z<3 and wc_z<3`), and it ignores the VMS's own band: VMS wc_z is weak-but-**positive**
   (1.9–2.64) while FULL's wc_z = **−1.02** (below its own shuffle floor) — FULL produces
   *anti*-structure, not the VMS's mild positive syntax, yet "matches" because −1.02 < 3.
   `ref_shuffle` also passes weak_syntax — a criterion a random shuffle satisfies carries no
   information.
3. **"context-free ⇒ weak syntax" is tautological** (the syntactic switch injects exactly what
   wc_z measures); not an empirical necessity link. The "3/4" necessity count is inflated by
   this plus a non-unique link (morphology also collapses ΔI harder than the positional
   knockout, 0.0002 < 0.0054).
4. **ED1/TTR/Zipf are gross misses** (0.998 vs 0.75; 0.594 vs 0.22) reported as a trailing
   "honest mismatches" list while the headline claimed a viable account of the signature.

## Fixes applied
Retract "blind/a-priori/firewall"; score fc_z/wc_z against the VMS's own two-sided bands;
drop the tautological necessity link; grade **C** ("fitted point; the minimal context-free
positional grammar is INSUFFICIENT — undershoots the VMS's weak-positive word-class structure
and overshoots productivity/connectivity"). This is the origin of the i07 arc.
