# STATUS.md — i09 Coordination Bus

_Last updated: 2026-07-16 (spec drafted; building E25)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); L7 absolute.
Continues the ledger as E25–. Hardens the i07–i08 coupling result per the E22/E23
refutation (multi-seed; ED1 decoupled from entropy/word-length).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E25 | Decoupled-ED1 type-lexicon generator, multi-seed | P1 gating | ✅ done → **i08 coupling largely DISSOLVES; shallow h2↔ED1 frontier near-miss [C]** | 48-config × 6-seed a-priori sweep, ED1 made a real knob via a large character space (85-glyph alphabet, pool-size sweep) + connected-core/isolate lexicon; scored by generator-side CI-overlap on the 5 non-trivial hard axes. **Deflation:** ED1 now CO-OCCURS (CI-overlap) with block-ΔI, TTR AND Zipf — which the small-pool families (E22–E24) could not; E24's ED1≈0.97 saturation was largely an artifact of the tiny character space. **Residual:** one shallow, principled h2↔ED1 tension — low h2 needs a small char-space (dense edit-graph → high ED1); enlarging it to lower ED1 raises h2. The (h2,ED1) frontier passes NEAR but not through the VMS box: h2 in-band → max ED1 0.625 (floor 0.74, gap ~0.11); ED1 in-band → max h2 2.037 (floor 2.11). A ~0.05–0.11 near-miss, not the gross incompatibility E24 reported; plausibly crossable with word-length variance (indel connectivity decouples ED1 from the char-space). |

| E26 | Word-length variance vs the h2↔ED1 frontier | P1 gating (v5) | ✅ done → **frontier all-but-crossed [C]** | 48-config × 5-seed a-priori sweep; small shared alphabet (low h2) + symmetric length PMF centred on 5 (spread = ED1 knob) + word-Zipf + block themes; multi-seed CI-overlap on all 6 profile axes. Length variance supplies the connectivity control fixed-length words lacked: **ED1 now lands IN-band (0.757) jointly with ΔI/TTR/Zipf**, so the E25 entropy↔connectivity tension is largely resolved (E25 capped ED1@h2-in-band at 0.63; VMS floor 0.74). No all-6 config under strict CI-overlap (ceiling 4/6); the two residual misses are a **~0.03 overshoot on h2** at the ED1-in-band point and a **mean-length construction artifact** (small alphabet saturates short words → mean skews to ~6.4) — neither fundamental. Net E25–E26: successive principled mechanisms shrank the i08 "coupling" from a gross multi-axis incompatibility to a ~0.03 single-axis near-miss + a fixable artifact. |

## i09 outcome (so far)

**E25 substantially walks back the i08 "no generative family reproduces the signature"
headline.** The strong coupling was largely a slot-grammar artifact (ED1 saturated by a
too-small character space). With connectivity as an independent knob, a positional-
morphology + decoupled type-lexicon generator comes **within ~0.05–0.11 on all five hard
axes at once**, leaving only a shallow entropy↔connectivity frontier unresolved. **E26
then all-but-crossed that frontier** with word-length variance: ED1 lands in-band jointly
with ΔI/TTR/Zipf, and the residual is a ~0.03 h2 near-miss plus a fixable length-
construction artifact. **Combined i08 walk-back (E25–E26):** the "no generative family
reproduces the signature" claim collapses to a ~0.03 single-axis near-miss — the VMS's
hard-axis signature does NOT meaningfully constrain the generative mechanism beyond the
per-axis values; the standing constraints are the i06 cipher exclusion and the character/
morphology structure, not a joint-signature barrier. **→ package into paper v5**, softening
v4 §4.7 accordingly. Still open (post-v5): the root↔leaf human panel; multi-seed bootstrap
of the soft fc_z/wc_z axes; the fixable length-construction artifact.

## Working hypothesis

If ED1 becomes an independent knob (connected-core + isolates lexicon), the E24 residual
coupling either dissolves (⇒ artifact of the slot-grammar morphology; deflate the i08
"no generative family" headline) or persists (⇒ real; harden it). Scored by multi-seed
generator-side CI-overlap with the VMS bootstrap bands. Either outcome is honest and
gets folded into v4/FLAGSHIP.

## Sessions

- **Code session (i09)** — spec drafted 2026-07-16; building E25.
