# i08 — Experiment Agenda (E23–): closing the i07 misses with word reuse

## E23 — Positional + reuse generator, genericity sweep [P1, gating]

**Question.** Does adding a copy-from-recent-context reuse step to the E21 positional
generator bring ED1 + TTR + Zipf into the VMS band jointly with h2 + ΔI + weak-positive
wc_z, across a broad a-priori basin?

**Mechanism.** Take the E21 context-free positional stream and apply a reuse filter: at
each position, with probability ρ copy a token uniformly from the last W emitted tokens
(rich-get-richer / Yule–Simon; copies can be re-copied), else keep the fresh slot-grammar
word. ρ = 0 recovers the E22 baseline. Copying is block-local (W below block length) so it
preserves — and mildly sharpens — the block-scale ΔI.

**A-priori grid (ranges fixed before scoring; not centred on any fitted point).**
reuse-rate ρ ∈ {0, 0.2, 0.4, 0.6, 0.8} × branching ∈ {4,5,6,7} × block-theme boost ∈
{6,10,16}; Zipf exponent, block length, and the reuse window W held at generic constants.

**Scoring.** Each config's full 8-axis signature vs the VMS's own bands (reuse E21's
banding: block-bootstrap CIs on profile metrics; two-sided VMS fc_z/wc_z bands). Report:
the basin fraction reaching ≥6/8 axes including the VMS positive wc_z; whether ED1, TTR,
Zipf — the axes E22 could NEVER match — now come in-band, and at what ρ; the ρ=0 vs ρ>0
contrast (does reuse specifically close the gap?); and every axis still missed.

**Pass/fail.** Broad basin (≥10% of grid) reaching ≥6/8 incl. positive wc_z, with ED1+TTR
+Zipf brought in-band by reuse → the **positional + reuse class is a sufficient account**
of the VMS full signature [B]. Knife-edge → [C] fragile. Reuse fails to close some axis →
another narrowing negative that names the next ingredient. Refutation pass either way;
L7 stands (sufficiency, not identification).

## Deferred / parallel (not E23)

- **Human panel on the root↔leaf consensus subset** — still the only decisive test for
  the visual bundle (E12); pre-register + power-analyse. Independent of the text track.
- **W / Zipf-exponent sensitivity** — if E23 lands, confirm the basin is not W-specific
  (line-scale vs block-scale reuse) as a robustness follow-up.
