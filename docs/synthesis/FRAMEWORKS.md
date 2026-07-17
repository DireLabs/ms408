# Alternative frameworks for MS408: is it *data* rather than *language*?

_Companion to [TIMELINE.md](TIMELINE.md). An exploratory review (grade D/C — a direction,
not a finding) prompted by the "each symbol carries a value" idea from the film *Arrival*.
The film is a **heuristic prompt only**; below we replace it with grounded, real precedents
and a decipherment-free test battery. L7 still binds absolutely: no reading is claimed, and
any future claim requires an independent statistical anchor._

## 1. The grounded version of the idea

*Arrival*'s logograms decode to binary/geometric **data** rather than transcribed speech.
The realistic analog is a **non-glottographic quantitative register** — a script whose
signs carry *values* (numbers, magnitudes, table entries, tallies) rather than phonemes.
This is not exotic; it is attested and, in one case, decoded:

- **Khipu / quipu** (Inka) — the cleanest real "each sign carries a positional value"
  system. Knot clusters are **base-10 digits**; position along the cord gives the power of
  ten; knot type distinguishes 1 vs 2–9 (Ascher & Ascher, *Code of the Quipu*, 1981).
  Urton & Brezine (*Science* 309:1065, 2005) decoded **hierarchical summation** at
  Puruchuco — cords that literally add up. Decoded **without phonetics**.
- **Cistercian numerals** (13th c., Cistercian monks) — a *single glyph* encodes any number
  1–9999 by **place-value quadrants** on a vertical stave. A compact position-value notation
  from the VMS's own European monastic milieu.
- **Gematria / isopsephy** (Greek Milesian, Hebrew, Arabic abjad) — letters *are* numbers,
  so every word carries a computable value. Shows a value-scheme can ride on a
  letter-like inventory.

The unifying, testable property of all three: a value-encoding produces **arithmetic
redundancy** — summation or checksum relations that phonetic text does not have.

## 2. Why this framing fits *our* envelope (the original point)

Strikingly, a structured non-linguistic register is **not excluded** by anything we found —
and several results actively point that way. Every number below is firewall-sourced (see
[FLAGSHIP.md](FLAGSHIP.md)):

| Our finding | Under a "symbols-as-values / register" reading |
|---|---|
| Low conditional entropy h₂≈2.08 (vs 3.1–3.9 for language) | A small effective symbol set with strong positional constraints — **exactly** what a numeral/tally system looks like. **Consistent, mildly supportive.** |
| Weak word-syntax; no content>function collocation gap (i05) | Numbers/tables have **no linguistic syntax**. The absence we kept finding is *expected* of a data register. **Supportive.** |
| Retained block-scale ΔI + strong positional grammar (i01, E1/E2) | Columnar / sectional / tabular structure. **Consistent.** |
| Dense ED1 morphology network (0.80): words form paradigmatic families | Positional numerals share structure (units/tens/…): "families" are what place-value produces. **Consistent, even suggestive.** |
| **Cipher-of-real-prose class EXCLUDED (i06)** | A numeric register is **not prose** — the exclusion removes a *competitor* and leaves the register hypothesis standing. **Consistent.** |
| **Distributional signature doesn't discriminate the mechanism (i09)** | The register hypothesis is, like the language and hoax hypotheses, **underdetermined by distribution**. It cannot be won on statistics — it needs a *checkable artifact*. |

That last row is the crux, and it converts a sci-fi prompt into disciplined science: our own
i09 walk-back showed summary statistics don't pin the mechanism, and i06/L7 have always
demanded an **independent anchor**. A value-register uniquely *supplies a candidate anchor
the language reading lacks* — **arithmetic redundancy** (khipu-style summation, gematria
totals, check-digits). A checksum either exists beyond chance or it does not; that is
falsifiable in a way "reads plausibly" never is.

## 3. Methodological parallels (what other decoders did, and the entropy debate)

- **Kober & Ventris (Linear B, 1952):** the decipherment ran **distribution/position first,
  meaning last** — Ventris's "grid" placed signs by co-occurrence before assigning sounds.
  Our program's stance mirrors this: structure before semantics.
- **The Indus entropy debate directly corroborates E9.** Rao et al. (*Science* 324:1165,
  2009) argued conditional entropy shows the Indus script is linguistic; **Sproat (2014,
  *Language* 90(2):457–481)** showed published entropy/bigram measures **cannot reliably
  separate linguistic from non-linguistic symbol systems**. This is the exact lesson our
  harness (L4) encodes and E9 found independently — an external, peer-reviewed anchor for
  our central methodological claim.
- **Modern computational decipherment** (Snyder–Barzilay 2010 Ugaritic; Luo–Cao–Barzilay
  2019 Linear B) exploits distributional + **cognate** structure — but assumes a
  *glottographic* script with a known relative. If the VMS is a data register, these do not
  apply, which is itself informative about why decipherment attempts stall.
- **Benford's law is a *consequence of place-value notation*** (Berger & Hill, 2011): a
  numeric register predicts a leading-value signature that a linguistic or hoax text does
  not — the two hypotheses make **opposite** predictions, so the test discriminates.

## 4. A decipherment-free test battery (if this is pursued)

All firewall-compatible (deterministic code → `results/`), harness-gated (validate on
known numeral registers *and* on matched non-numeric synthetic controls before claiming
anything — L4), stratified by Currier A/B and hand (L8), and L7-bound (a positive requires
the independent arithmetic anchor):

1. **Benford / leading-glyph magnitude test** — map glyph rank or a candidate word-value to
   magnitudes; test for a place-value leading-digit signature vs a matched control.
2. **Base-N modular periodicity** — scan lines/paragraphs for token classes recurring at
   fixed positional periods (the khipu/Cistercian place-value tell).
3. **Positional place-value structure** — Voynichese *already* has strong positional glyph
   constraints; test whether they behave like **digit-slots** (place-value) vs syllable-slots.
4. **Summation / check-digit search** — on tabular / list-like folios (recipe star-lines,
   zodiac rings, pharma rows), test whether candidate numeric lines **sum** to a header/
   footer token beyond chance. *This is the L7 anchor* — the one test that could elevate the
   hypothesis above D.
5. **Glyph-value entropy vs known numeral registers** — compare the VMS entropy/repetition
   profile to corpora of *known* value-registers (khipu transcriptions, medieval account
   books, Cistercian tables), the control class the Rao–Sproat debate says the field omits.
6. **A/B and section stratification** — a numeric register should be stable across "dialects"
   and vary by section (herbal vs. astronomical vs. balneological) differently than a
   language would.

## 5. Honest verdict

> **Update (i10, E27–E28): the direction was scoped, the primary anchor was tested, and it
> came back NULL — the register hypothesis stays grade D.** E27 excluded a positional-*numeral*
> sub-type on shape (the VMS is strongly position-specialised, unlike a base-N system that
> reuses digits across places). E28 ran the decipherment-free arithmetic anchor on the
> manuscript's most number-like folios — the angular-tagged zodiac rings — with a
> sensitivity-confirmed test, and found **no robust ordinal structure** in the labels (a lone
> f73r hit that does not reproduce across the other 11 rings). So the register framing remains
> *consistent with* the envelope but gains **no positive anchor**; per L7 it cannot rise above
> D. The direction closes here barring a materially different anchor or folio class. Original
> pre-test verdict retained below for the record.

**Grade D (exploratory), with a clear path to C/B *only* via test #4.** The
symbols-as-values framing is (i) grounded in a genuinely decoded precedent (khipu) and a
period-contemporary notation (Cistercian), (ii) **consistent with, not contradicted by,
our entire constraint envelope**, and (iii) uniquely equipped with a falsifiable,
decipherment-free anchor (arithmetic redundancy) that the language reading lacks — which is
why it is more tractable than yet another decipherment attempt.

**Heavy caveats, stated plainly:** matching VMS statistics is **necessary, not sufficient**
— the Rugg Cardan-grille (2004) and Timm–Schinner self-citation (2019) generators already
reproduce Voynichese statistics with *no* meaning, so a register that merely "looks right"
distributionally is worth nothing without the summation anchor. No prior work has
demonstrated a numeric or check-digit reading of the VMS; this is an **open, untested
hypothesis**, not a supported claim. Some sources surfaced in review (recent arXiv
preprints ~2604.*, and the "Naibbe" dice-cipher press) could **not be independently
verified** and are excluded from any load-bearing role here; the solid anchors are
Rao/Sproat, Ascher, Urton & Brezine, Ventris, Rugg, and Timm–Schinner (verify each before
formal citation).

**Recommendation:** if a next direction is wanted after the current approach, this is the
best-motivated one — scoped tightly to the **decipherment-free arithmetic/ordinal anchor**
first, because that single test is what separates "consistent with a register" (which we
already are) from "is a register" (which only an anchor can show).

**Scoped as i10** ([docs/planning/i10/](../planning/i10/)). One refinement from inspecting
the actual data: the generic **summation/check-digit search (#4)** is deprecated as the
primary anchor — the VMS has no figure-columns — in favour of **ordinal/periodic structure in
the angular-tagged circular diagrams**. The 12 zodiac pages carry `<!HH:MM>` angular-position
tags on their labels (plus 84 circular + 142 radial loci), so we can test whether label
*content* tracks angular position (as a degree/date/count would) beyond a matched null —
grounded, killable, on existing data. E27 (the "quantify the symbols" step) is cheap
grounding; **E28 (the angular anchor) gates the whole iteration**; controls (#5) and
digit-slot tests (#3) run only if E28 signals. Honest prior: a positive is unlikely (no
obvious numeric tables), so the most probable outcome is a clean graded *negative* — still a
real envelope result. L7 binds throughout.
