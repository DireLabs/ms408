# i09 — Hardening the i07–i08 coupling: is the ED1 obstruction real or an artifact?

**Inherits** all locks L1–L37; the standing refutation rule; the firewall (L3); L7
absolute. Continues the ledger as **E25–**.

## Where i08 left us — and the refutation's central doubt

i07–i08 (E21–E24) concluded that across three generative families (context-free
positional, +token-reuse, +type-level small lexicon) **none reproduces the VMS's full
8-axis signature over the swept ranges**, with the residual obstruction centred on
**morphology connectivity (ED1 ≈ 0.75)**. The E22/E23 clean-context refutation flagged the
sharpest doubt: in the slot-grammar generator, **ED1 is rigidly coupled to word length and
branching** (all words share slots, so the network saturates near 1.0). So the "coupling"
may be an artifact of that morphology parameterisation, not a real constraint on the
generative mechanism — and the results are single-seed with a tight (~0.03) ED1 band.

## The i09 question (a falsification test)

**If ED1 is made an INDEPENDENT knob — decoupled from entropy and word length — does the
residual coupling dissolve (E24's obstruction was an artifact) or persist (it is real)?**
Scored with **multi-seed generator-side CIs**, not single-seed hard in/out.

Mechanism: build the type lexicon as a **connected core** (grown by single-substitution
steps → one giant ED1 component) plus **isolates** (words with no realised neighbour), so
`isolate_frac ≈ 1 − ED1_main_component_share` is a direct knob, orthogonal to the
character grammar (h2), lexicon size / word-Zipf (TTR, frequency slope), and block themes
(ΔI). Fixed word length keeps ED1 substitution-only and removes the length confound.

Honest either way:
- **Dissolves** (a broad multi-seed basin hits all hard axes incl. ED1 ≈ 0.75) ⇒ the i08
  coupling was largely a slot-grammar artifact; the joint signature constrains the
  generative mechanism *less* than i08 claimed — an honest **deflation** that must be
  folded back into v4/FLAGSHIP.
- **Persists** (ED1 ≈ 0.75 still cannot co-occur with the other hard axes even when
  nominally decoupled) ⇒ the coupling is robust; the i08 negative hardens.

## Discipline

A-priori sweep (not a fitted point); score the six profile ("hard") axes by generator-side
CI-overlap with the VMS bootstrap bands; fc_z/wc_z remain soft (2-point ranges) and are
reported, not counted. Sufficiency of a class is the ceiling (B); never identification (L7).
Refutation pass before any A/B lock.
