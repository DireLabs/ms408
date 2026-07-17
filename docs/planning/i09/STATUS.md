# STATUS.md — i09 Coordination Bus

_Last updated: 2026-07-16 (spec drafted; building E25)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); L7 absolute.
Continues the ledger as E25–. Hardens the i07–i08 coupling result per the E22/E23
refutation (multi-seed; ED1 decoupled from entropy/word-length).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E25 | Decoupled-ED1 type-lexicon generator, multi-seed | P1 gating | ✅ done → **i08 coupling largely DISSOLVES; shallow h2↔ED1 frontier near-miss [C]** | 48-config × 6-seed a-priori sweep, ED1 made a real knob via a large character space (85-glyph alphabet, pool-size sweep) + connected-core/isolate lexicon; scored by generator-side CI-overlap on the 5 non-trivial hard axes. **Deflation:** ED1 now CO-OCCURS (CI-overlap) with block-ΔI, TTR AND Zipf — which the small-pool families (E22–E24) could not; E24's ED1≈0.97 saturation was largely an artifact of the tiny character space. **Residual:** one shallow, principled h2↔ED1 tension — low h2 needs a small char-space (dense edit-graph → high ED1); enlarging it to lower ED1 raises h2. The (h2,ED1) frontier passes NEAR but not through the VMS box: h2 in-band → max ED1 0.625 (floor 0.74, gap ~0.11); ED1 in-band → max h2 2.037 (floor 2.11). A ~0.05–0.11 near-miss, not the gross incompatibility E24 reported; plausibly crossable with word-length variance (indel connectivity decouples ED1 from the char-space). |

## i09 outcome (so far)

**E25 substantially walks back the i08 "no generative family reproduces the signature"
headline.** The strong coupling was largely a slot-grammar artifact (ED1 saturated by a
too-small character space). With connectivity as an independent knob, a positional-
morphology + decoupled type-lexicon generator comes **within ~0.05–0.11 on all five hard
axes at once**, leaving only a shallow entropy↔connectivity frontier unresolved. So the
VMS's hard-axis signature constrains the generative mechanism **far less** than i08
claimed — the paper v4 §4.7 framing is now superseded and must be softened (candidate
v5). **Open (decides v5 wording):** E26 — add word-length variance (indel connectivity)
and/or non-uniform pools to try to *cross* the frontier; if it crosses, the i08 negative
is fully overturned (the generator reproduces the hard-axis signature); if not, the
entropy↔connectivity tension is a genuine (if narrow) residual constraint. Also still
open: multi-seed generator-bootstrap of fc_z/wc_z (soft axes); the root↔leaf human panel.

## Working hypothesis

If ED1 becomes an independent knob (connected-core + isolates lexicon), the E24 residual
coupling either dissolves (⇒ artifact of the slot-grammar morphology; deflate the i08
"no generative family" headline) or persists (⇒ real; harden it). Scored by multi-seed
generator-side CI-overlap with the VMS bootstrap bands. Either outcome is honest and
gets folded into v4/FLAGSHIP.

## Sessions

- **Code session (i09)** — spec drafted 2026-07-16; building E25.
