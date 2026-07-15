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
| E22 | Genericity / coupling sweep (refutation-scoped) | P1 gating | ✅ done → **class INSUFFICIENT [C]** | A-priori 64-config grid (branching 4–7 × zipf 0.6–1.2 × boost 3–16, not centred on E21's point). **basin ≥5/8 axes = 0%**; ED1, Zipf and word-length are NEVER matched at any tuning; coupling confirmed (of 2 TTR-in-band configs, 0 also match h2 AND ED1). The best config reaches only 3/8 (h2, ΔI, and — with high block contrast — the VMS's weak-positive wc_z 2.62). CONTROL: real Latin types under a context-free block wrapper give fc_z −1.41 / wc_z 2.5, both IN the VMS bands → the VMS's weak-positive surface syntax is exactly what context-free block sampling of ANY lexicon produces. Conclusion: the minimal context-free positional/template grammar is a PARTIAL account — it matches entropy + block-ΔI + weak-positive syntax but STRUCTURALLY overshoots morphology connectivity (ED1) and lexical productivity (TTR) and is too flat in frequency (Zipf); the full VMS signature demands an ADDED reuse / smaller-effective-lexicon / correlated-slot mechanism a bag-of-slots lacks. |

## i07 outcome

**The positive complement did not confirm a clean generative account — it CONSTRAINED
one.** A context-free positional/template generator reproduces the VMS's low character
entropy, its block-scale ΔI, and (via block contrast) its weak-but-positive word-class
structure — but at NO tuning in a broad a-priori grid does it also reproduce the VMS's
morphological connectivity (ED1 ≈ 0.75; the generator overshoots to ≈ 0.97), lexical
reuse (TTR ≈ 0.22; generator ≈ 0.59), or frequency slope. So "template/positional
generation" as a *context-free bag-of-slots* is a PARTIAL account only. The specific
misses point the next mechanism: the VMS reuses words far more heavily and has a less
combinatorially productive, more clumped morphology than independent slot-sampling — i.e.
it needs a **word-reuse / copying** component (which loops back to the self-citation
family, now motivated by evidence rather than circularly) plus mild positive sequential
structure. **This is an informative negative [C], not a decipherment step (L7).** Next:
consolidate E18–E22 (i06+i07) — decide with Tim whether to fold i07 into a paper v4 or
carry the "reuse mechanism" question into i08.

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
