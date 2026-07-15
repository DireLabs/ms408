# i07 — Experiment Agenda (E21–E22): characterising positional/template generation

## E21 — Minimal positional generator + necessity ablation [P1, gating]

**Question.** Does a principled, non-Voynich-tuned template/positional generator land in
the VMS full-signature band (h2, ΔI, fc_z, wc_z), and which ingredient is *necessary* for
each property?

**The generator (three ingredients, each a switch).** A word stream built from:
- **morphology** — a paradigmatic slot grammar (prefix·root·suffix over small a-priori
  glyph inventories) so that words sharing a slot are edit-distance-1 neighbours. Drives
  low h2 + dense ED1. OFF ⇒ flat random types.
- **positional** — the stream is cut into fixed-length blocks; each block draws from its
  own lexicon subset / reweighting, so the type distribution shifts across the document.
  Drives retained block-scale ΔI. OFF ⇒ one global distribution.
- **syntactic** (the *anti*-ingredient) — within a block, the next word's class depends on
  the previous word's class, injecting word-class structure. ON ⇒ raises fc_z/wc_z. The
  template mechanism's defining property is that this is **OFF** (context-free slot fill),
  which yields weak word-syntax by construction — the generative dual of the i06 finding.

**Parameters (frozen a priori — circularity firewall).** Glyph inventory, slot-inventory
sizes, Zipf sampling exponent, and block length are set from fixed constants / Latin
structure, documented as chosen blind to the VMS. None is fit to a VMS number.

**Configs.** FULL (morph=on, pos=on, syn=off) = the template/positional generator; then
the ablations −morphology, −positional, +syntactic; plus reference anchors (real Latin,
full shuffle) already in the harness.

**Pass/fail & deliverable.** For each config, profile the full signature and test against
the VMS band (block-bootstrap CIs on h2/ΔI/ED1/Zipf; the E19 WEAK_Z line on fc_z/wc_z).
The result is the **ingredient→property map**: FULL should hit the core three; −morphology
should lose h2/ED1; −positional should lose ΔI; +syntactic should lose weak-syntax. Report
every axis the FULL generator still **misses** (ΔI scale, TTR, word length, Zipf) — these
are honest mismatches, not hidden. Refutation pass required. Grade B ceiling (sufficiency
of a class, never identification — L7).

## E22 — Genericity / landscape sweep [P2, CONDITIONAL on E21 landing in-band]

**Runs only if E21's FULL config reaches the VMS band.** Guards against the charge that
the match is a fine-tuned point. Sweep the a-priori parameters (inventory sizes, block
length, Zipf exponent) over a coarse grid and map the fraction of the family that lands in
the VMS band. If a **broad** sub-region hits it, the match is generic to the mechanism
(strong positive for the class); if only a knife-edge does, the match is fragile and the
claim weakens to C. Optionally: a "real-language input under the same positional wrapper"
control, to show it is the generative slot-fill (not the block wrapper) that produces the
weak syntax.

**Pass/fail.** Broad basin → the positional/template class is a robust positive account of
the VMS signature [B]. Knife-edge → fragile [C]. Either way it is a class account, not an
identification; L7 stands and the refutation pass applies.
