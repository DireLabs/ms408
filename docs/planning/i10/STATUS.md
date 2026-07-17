# STATUS.md — i10 Coordination Bus

_Last updated: 2026-07-16 (scoping drafted; grounded on exploratory ZL reads)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); harness (L4); L7
absolute; A/B + hand stratification (L8); consume-only external data (L19). Continues the
ledger as E27–. Scopes the [FRAMEWORKS.md](../../synthesis/FRAMEWORKS.md) direction
(symbols-as-values / non-glottographic quantitative register).

## Open decisions surfaced to Tim

- **i10-a — pursue?** Recommendation: run E27 (cheap grounding; the "quantify the symbols"
  ask) + E28 (the angular ordinal anchor — killable, tractable, on existing data). Defer
  everything expensive until E28 signals.
- **i10-b — data policy (L19)** for numeral-register controls (khipu/account-books/Cistercian)
  — only if E28 signals.
- **i10-c — reading-order fidelity** of the `<!HH:MM>` angular tags + circular/radial locus
  order (an E28 precondition).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E27 | Symbol quantification (inventory, positional, system-type) | P2 grounding | ✅ done → **[D] descriptive; base-N register shape-EXCLUDED** | VMS paragraph: 37 glyph types, effective alphabet ~15 (small; 15 glyphs cover 95%). Decisive: **positional specialisation 0.74** (mean TV among initial/interior/final glyph distributions) vs base-10 numeral 0.07 / base-16 0.05 (same digits every place) / syllabary 0.51 / alphabet 0.39. So a **positional-NUMERAL sub-type is shape-incompatible** (the VMS uses strongly position-specific glyph sets — templatic, per i09); a non-positional value scheme (tallies / label-values) is untouched → E28. Stable across A/B (0.73/0.76) and labels (0.69). |
| E28 | Angular/ordinal anchor in circular diagrams | **P1 GATING** | ✅ done → **[D] NO robust anchor — register stays D** | Mantel test (angular-distance vs label-edit-distance) on all 12 zodiac rings (hand 4; 999 perms), with a positive control that DOES fire (ordered integers: r=0.24, p=0.001 — test is sensitive). Result: no consistent signal. Combined Mantel p=0.0074 is **driven by a single ring** (f73r p=0.001); dropping it → p=0.11 (n.s.); only 1/12 rings individually p<0.05, mixed sign; length-autocorrelation null (0.388). All 12 rings are the same diagram type, so a real value-encoding would show across them — the lone f73r hit reads as chance (a footnote, not an anchor). |
| E29 | Digit-slot discriminator + numeral-register controls | P2 (cond. on E28) | ❌ not triggered (E28 null) | — |

## i10 outcome

**The symbols-as-values direction finds NO support and closes at grade D — a clean graded
negative.** E27 excluded a positional-NUMERAL sub-type on shape (the VMS is strongly
position-specialised, unlike a base-N system that reuses digits across places). E28 — the
decipherment-free arithmetic anchor, run on the manuscript's *most number-like* folios (the
angular-tagged zodiac rings) with a sensitivity-confirmed test — found no robust ordinal
structure in the labels. So the register hypothesis, though *consistent with* the
distributional envelope (FRAMEWORKS §2), gains **no positive anchor**; per L7 it cannot be
elevated above D, exactly as the honest prior predicted. The standing constraints remain the
i06 cipher exclusion and the character/morphology structure, not a value-register reading.
**Footnote lead (not pursued):** f73r alone shows adjacent-label similarity (Mantel r=0.24,
p=0.001) — a lone idiosyncrasy someone could probe, but not reproduced across the other 11
rings. i10 closes unless a materially different anchor (or folio class) is proposed.

## Exploratory grounding (to be formalised by E27 — NOT firewall-committed)

- ZL paragraph text: **~39 distinct EVA glyphs**, ~15 carry nearly all mass; rare tail
  (8,7,9,0,b,j,u,z,v).
- Distinct word-initial {o,c,q,s,d,a,y,l} vs word-final {y,n,l,r,o,s,m,d} glyph sets.
- Loci: 4130 P (paragraph), 1029 L (label; incl. 299 Lz zodiac, 194 Lf), 84 C (circular),
  142 R (radial). 12 zodiac pages carry `<!HH:MM>` angular-position tags on labels.

## Working hypothesis / honest prior

The envelope is *consistent with* a quantitative register, but distribution can't settle it
(i09) — only the E28 arithmetic/ordinal anchor can. Prior on a positive is **low** (no obvious
numeric tables), so the most likely outcome is a clean graded **negative** at E28 — which is
still a valuable envelope result. L7 binds: no value/number/date is ever named.

## Sessions

- **Code session (i10)** — scoping drafted 2026-07-16; E27/E28 specced, awaiting go/no-go.
