# MS408 Research Program — Iteration 06 (cryptanalytic direction, discipline-gated)

**Mandate.** i02–i05 mapped the constraint envelope by statistics; i06 turns to the
*cryptographic/decipherment* direction Tim asked for — but gated by the program's
discipline so it does not become the field's usual plausible-but-wrong failure. Two
things make this safe and worthwhile now: (a) our own results **revived** exactly two
non-excluded encoding classes — deterministic-verbose / nomenclator (E2) and abjad /
abbreviation (E6) — so there is a *targeted* hypothesis to attack rather than a blind
search; and (b) i05 added a **new discriminating constraint** the cryptanalytic
question must respect.

**The i05 constraint that reframes decipherment.** A cipher that PRESERVES word order
(abjad, deterministic substitution, nomenclator) inherits the *source language's*
word-level syntax. But i05 showed the VMS has **weak word-level syntax** — no natural-
language function/content collocation gap (E13c), weak distributional word-class
structure (E14). Preview: an abjad of real Latin retains strong syntax (word-class
z≈11, function/content z≈14) while the VMS is weak (≈2 / ≈−4). So the weak-syntax
constraint appears to **disfavour any word-order-preserving cipher of a real language**
— which would mean a cryptanalytic attack on those classes is attacking a hypothesis
the evidence already argues against. i06 tests this rigorously (E19) *before* spending
effort on the attack (E20).

**Inheritance.** All locks L1–L37; standing refutation rule; firewall (L3); null-
correction framework (i05). Continues the experiment ledger as E19–E20. **L7 is
absolute**: no decipherment/translation claim survives without an independent
statistical anchor; the *expected and acceptable* outcome of a cryptanalytic attack is
a graded exclusion, not a "solution".

## Success criterion (i06)

E19: a graded verdict on whether ANY cipher-of-a-real-language class matches the VMS's
FULL joint signature — character entropy, word-order ΔI, ED1 morphology, Zipf, AND the
i05 mid-level syntax — simultaneously. E20 (conditional on E19 leaving a viable
target): a constrained, refutation-passed cryptanalytic search whose any candidate
must clear an independent anchor, or an honest "no anchor-surviving key in the searched
class" exclusion.

**Read:** this README → `EXPERIMENTS.md` → `STATUS.md`.
