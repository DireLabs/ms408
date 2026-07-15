# i06 — Experiment Agenda (E19–E20): the discipline-gated cryptanalytic direction

## E19 — Joint-signature test with mid-level syntax [P1, gating]

**Question.** Does ANY cipher-of-a-real-language class match the VMS's FULL signature
at once? i01's bracket and E6 tested character/word-order/morphology; E19 adds the i05
**mid-level syntax** measures, which are the new discriminators. Crucially, word-order-
PRESERVING ciphers (abjad, deterministic-verbose, nomenclator) should inherit the
source language's strong word-syntax, unlike the VMS.

**Design.** Assemble a full signature vector for each candidate — character entropy
h2, word-order ΔI (peak value + scale), ED1 morphology main component, Zipf slope,
AND the null-corrected mid-level statistics (function/content gap z, word-class NMI z).
Compute it for the VMS (A and B) and for the candidate generators of a real language:
- word-order-PRESERVING ciphers: abjad, deterministic-verbose, nomenclator;
- generation processes (weak-syntax by nature): self-citation (H3), a template/drift
  generator;
- reference anchors: real Latin/German (strong syntax), full shuffle (no syntax).
Report which candidates match the VMS on EACH signature and, decisively, on the
mid-level syntax. A candidate "matches" only if it is within the VMS band on ALL.

**Pass/fail.** If a word-order-preserving cipher of a real language matches the VMS's
weak mid-level syntax too → that class stays a live attack target (→ E20). If (as the
preview suggests) those ciphers RETAIN strong syntax and only the generation/weak-
syntax processes match the VMS → a new graded constraint: **the VMS is disfavoured as
a word-order-preserving cipher of a real language**, and the decipherment target
narrows to non-syntax-preserving mechanisms (or the honest conclusion is that the weak
word-syntax is a property of the generative process, not an enciphering of real prose).
Refutation pass required either way.

## E20 — Constrained cryptanalytic attack [P2, CONDITIONAL on E19]

**Runs only if E19 leaves a viable cipher-of-a-real-language target.** If E19 excludes
the syntax-preserving classes, E20 is redirected (see below) or deferred.

**Design (if run).** For the surviving target class, search for a key (abjad glyph→
consonant map / nomenclator table / deterministic-verbose inverse) that maps VMS
ciphertext to candidate plaintext, optimised by a real-language language-model score
(perplexity), with STRICT guards:
- **Held-out validation:** fit the key on part of the corpus, require it to decode a
  HELD-OUT portion coherently (guards against overfitting a key to noise).
- **Null margin:** the best key must beat an ensemble of random keys by a large,
  pre-registered margin on the LM score (guards against "any key looks a bit like
  language").
- **L7 anchor gate:** a candidate is reportable ONLY if it clears an INDEPENDENT
  statistical anchor — e.g., the decoded plaintext reproduces the target language's own
  h2/Zipf AND places a known/expected token correctly — not merely "reads plausibly".
- **Refutation pass** on any positive.

**Pass/fail.** A key clearing all guards → an extraordinary result requiring the anchor
(L7); the far more likely and still-valuable outcome is **"no key in the searched class
yields anchor-surviving plaintext"** — a graded exclusion that closes the class.

**Redirect (if E19 excludes syntax-preserving ciphers).** Reframe E20 as a test of the
*generative* alternative: can a template/self-citation/constructed-weak-syntax process,
fit to the VMS, reproduce its full signature INCLUDING the weak mid-level syntax that
real-language ciphers cannot? That would make "structured generation" the best-fit
class — the positive complement of the E19 exclusion.
