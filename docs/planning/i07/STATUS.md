# STATUS.md — i07 Coordination Bus

_Last updated: 2026-07-15 (spec drafted; building E21)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); L7 absolute.
Continues the experiment ledger as E21–E22.

## Open decisions surfaced to Tim

- **D-item i07-a — the circularity firewall protocol.** How generator parameters are
  chosen so the test is not circular (self-citation's fatal flaw). Default taken (least-
  committal): all parameters frozen a priori / from Latin structure, blind to the VMS;
  deliverable is the ingredient→property map + honest mismatch list, not a distance-to-VMS;
  E22 maps a parameter *landscape* rather than committing to one tuned point. Flagged for
  Tim to confirm or tighten before any A/B claim is locked.

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E21 | Minimal positional generator + necessity ablation | P1 gating | ✅ done + **REFUTED → downgraded B→C** | A GRID-SELECTED (not a-priori — firewall framing retracted) positional/template point matches the VMS on character entropy (h2 2.14) + block-scale ΔI (0.081) but MISSES the VMS on its own bands elsewhere: it does NOT reproduce the VMS's weak-but-POSITIVE word-class structure (VMS wc_z [1.9,2.64]; FULL wc_z −1.02 = **anti**-structure, below its own shuffle), and OVERSHOOTS vocabulary productivity (TTR 0.59 vs 0.22), morphology connectivity (ED1 0.998 vs 0.75) and frequency flatness (Zipf −0.37 vs −0.90). Matches 3/8 axes (h2, ΔI, fc_z). Ingredient map corrected: morphology is CO-necessary for ΔI (−morph collapses ΔI harder than −pos); context-free→weak-syntax is TAUTOLOGICAL. **Net (informative negative):** the minimal context-free positional grammar is INSUFFICIENT for the full VMS signature; it constrains the class toward heavier word reuse, a smaller effective lexicon, and mild positive sequential structure. |
| E22 | Genericity / coupling sweep (refutation-scoped) | P1 (now gating the i07 conclusion) | ⏳ next | Must use an a-priori-fixed grid; score against the VMS's ACTUAL bands (incl. positive wc_z ∈ [1.9,2.64], not the discredited one-sided `<3`); require JOINT coverage of ≥5/8 axes bringing ED1+TTR+Zipf in-band SIMULTANEOUSLY with h2/ΔI. Test the coupling the refutation predicts (does satisfying TTR force h2/ED1 out?). Add the pre-registered real-language-under-positional-wrapper control. Broad basin covering ≥5 incl. real wc_z → B; coupling failure / knife-edge → i07 concludes with the E21 negative (class INSUFFICIENT), grade C. |

## Refutation record (E21)

Clean-context refutation (2026-07-15) downgraded E21 **B→C** on three decisive grounds,
all conceded: (1) constants were grid-selected against the VMS band, so "a-priori/blind"
was false — a fitted point, not class sufficiency; (2) the weak-syntax leg used a VMS-blind
one-sided `<WEAK_Z` threshold a full order-shuffle also passes, and FULL's wc_z is
wrong-signed vs the VMS band; (3) the "necessity" count was inflated by one tautological
link (context-free→weak) and one non-unique link (morphology also collapses ΔI). Fixes
baked into the code + verdict. This is the same self-correction that narrowed E19.

## Working hypothesis

The template/positional mechanism reproduces the VMS core three (low h2, retained block
ΔI, weak word-syntax) because each is produced by a separate ingredient — paradigmatic
morphology (h2/ED1), block reweighting (ΔI), context-free slot fill (weak syntax) — and
the ablation should show each ingredient is necessary for its property. Expected honest
mismatches: ΔI *scale* and TTR (self-citation missed these too). This would establish the
class as a viable positive account (B ceiling) without identifying the VMS as it (L7).

## Sessions

- **Code session (i07)** — spec drafted 2026-07-15; building E21.
