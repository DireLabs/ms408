# MS408 (Voynich) — Program Timeline & Synthesis Artifact

_A milestone record of the research program through iteration i09 (experiments E1–E26),
compiled 2026-07-16. Numbers trace to `results/**` (firewall L3) via
[FLAGSHIP.md](FLAGSHIP.md); grades A–D per RESEARCH-PLAN §6. No decipherment or
real-taxon claim is made anywhere (L7)._

## The through-line

The program's goal is not to read the manuscript but to **shrink the constraint envelope**
around what it is — which classes of encoding, language, and origin remain consistent with
the evidence — with every claim graded and every A/B claim run past a **clean-context
adversarial refutation**. Three disciplines are load-bearing: a synthetic **harness**
(controls a method must pass before touching the real text), a **firewall** (all numbers
from deterministic versioned code), and the standing **refutation pass**. The most durable
result is the architecture itself: it has repeatedly overturned the program's own
conclusions — including ones asserted by its own code, and, in i09, one of its own
*negatives* — before they were reported.

## Iteration-by-iteration

| Iter | Question | Key experiments | Outcome | Self-correction on the record |
|---|---|---|---|---|
| **i01** | Reproduce published baselines; bracket the encoding families | replication gate (G1); T2.4 encoding bracket | **[A]** entropy anomaly (h₂≈2.08 vs 3.1–3.9 controls), Currier A/B split, dense ED1 morphology network (0.80), positional grammar all replicate | — |
| **i02–i03** | Can any statistic localize meaning? Which encoding family fits? | E1–E10 (meaning detector, word-order confound, anchor power, root↔leaf, encoding-fair, cipher reconstruction, fine anchor, whitened bracket, VMS coordinate, third rater) | **[A]** no statistic (nor a vector) separates meaning — structured-meaningless baselines match/exceed the VMS on every axis (E9). **[C]** verbose ciphers excluded on ED1; abjad revived; no family distinguished | E6's "needs constructed morphology" refuted by the abjad control; E7's 18 false-positive anchors caught by a mandatory null; E8's "whitening confirms" withdrawn (ill-conditioned Σ); E9's two broken axes + trivial-endpoint artifact forced a pre-registration retraction; E10 overturned the program's own E4b |
| **i04** | Is the root↔leaf visual bundle real? | E11 (style control), E12 (independent-lineage rater) | **UNRESOLVED-underpowered** — the one positive lead dies to noise; a human panel is the only decisive test | E12's first-pass "KILLED — rater-idiosyncratic" was itself corrected to "unresolved" by the refutation |
| **i05** | Where does the structure live between characters and meaning? | E13–E17 (function/content collocation, word-classes, morphology, A/B contrast) + null-correction framework | **[C]** VMS lacks the natural-language surface content>function collocation gap and has weak word-class structure (~0.13–0.19× real); the A/B mid-level difference is a **content confound, not dialect** (E17) | E14's code-asserted "A≠B, different processes" down-weighted; E17 overturned E14b's apparent dialect difference; several probes refused for want of a clean null |
| **i06** | Could the VMS be a cipher of a real text? | E18 (completeness), E19/E19b (joint signature), E20 (transposition closure) | **[B, negative]** the **cipher-of-real-prose class is EXCLUDED** — the VMS uniquely combines low entropy + retained block-scale ΔI + weak word-syntax, which no word-order-preserving cipher (universal incl. Hebrew abjad) nor transposition cipher can produce. **[known issue]** ~12% of the foliated range is missing, vocabulary non-saturating | E19's first-pass "favours generation" dropped as **circular** (the only match was a Voynich-tuned generator); the demanded control (diverse languages) then *upgraded* the exclusion to universal (E19b) |
| **i07** | Can a template/positional generator — not tuned to the VMS — reproduce the full signature? | E21 (positional generator + ablation), E22 (genericity sweep) | **[C]** a context-free positional generator matches entropy + block-ΔI + weak-positive syntax but not, jointly, morphology connectivity / lexical reuse / frequency slope | E21's first-pass "class sufficiency **[B]**" overturned — its constants had been **grid-selected to the VMS bands** (a fitted point), and its weak-syntax test used a threshold a shuffle also passes → narrowed to [C] |
| **i08** | Add the frequency-concentration mechanism the misses demand | E23 (token reuse), E24 (type-level small lexicon) | **[C]** token reuse rescues the frequency axes but trades them against entropy/ΔI; type-level concentration resolves that (TTR co-occurs with h₂) but leaves a residual coupling on **morphology connectivity (ED1)**. First-pass framing: "no tested family reproduces the signature" | The E22/E23 refutation narrowed "structurally unreachable / any family" to "a coupling within swept ranges"; flagged fc_z/wc_z as **soft** axes (2-point ranges, sectional-drift confound) |
| **i09** | Is that ED1 coupling real, or an artifact of the morphology model? | E25 (decoupled-ED1 generator, multi-seed), E26 (word-length variance) | **[C, walk-back]** the coupling was **largely an artifact**: with ED1 an independent knob (larger character space, then length variance), a positional + skewed-type-lexicon generator reproduces the distributional hard axes together to within a ~0.03 residual (+ a fixable length-construction artifact). **The distributional signature does not, by itself, discriminate the generating mechanism** | The pipeline **over-read its own i08 negative and then caught it** — the rarer direction of self-correction |

## The evidence ledger (current standing)

- **Established [A]:** conditional-entropy anomaly; two-system Currier A/B structure; dense
  paradigmatic ED1 morphology; strong positional grammar; the replication gate (G1).
- **Directional / disfavoured [C]:** no lexical label→feature naming system for the herbal
  at achieved power; verbose ciphers excluded; weak surface word-syntax / no
  function-content collocation gap; no encoding family distinguished.
- **Excluded [B, negative]:** the **cipher-of-real-prose** class (i06).
- **Underdetermined:** whether the structure carries *meaning* (E9 shows *why* it is hard —
  structure statistics are not meaning detectors); the root↔leaf visual bundle
  (unresolved-underpowered); the specific generating mechanism (i09 — the distributional
  signature does not pin it down).
- **The load-bearing constraints** are therefore the **cipher-class exclusion** and the
  **qualitative character/morphology structure**, *not* a joint-distribution barrier.

## Preprint snapshots

| Version | Date | Scope | Headline change |
|---|---|---|---|
| v1 | 2026-07-09 | i01–i04 | First snapshot: constrained two-system script; meaning provably underdetermined (E9); root↔leaf unresolved |
| v2 | 2026-07-14 | + i05 | Mid-level linguistic program; null-correction framework |
| v3 | 2026-07-15 | + i06 | Cipher-of-real-prose class excluded; ~12% missing folios |
| v4 | 2026-07-15 | + i07–i08 | Favoured generative class characterised and (apparently) constrained; E22/E23 refutation corrections |
| v5 | 2026-07-16 | + i09 | **Walk-back:** the apparent generative constraint dissolves; the signature does not discriminate the mechanism |

## Methodological headline (the transferable contribution)

Across nine iterations the refutation pass has overturned, *before* they were reported: a
"meaning certificate" read of the word-order statistic; a "constructed-language best fit";
a "needs constructed morphology" claim; a "whitening confirms" claim; 18 false-positive
anchors; a positive root↔leaf verdict (twice — over-claimed then over-killed); an A/B
grammatical difference (a section confound); a circular "favours generation" positive; a
grid-fitted "class sufficiency [B]"; and — most distinctively — an over-strong *negative*
("no generative family reproduces the signature") that a later iteration walked back. A
pipeline that overturns its own code's and its own prior iteration's verdicts, in *both*
directions, is the result we are most confident in.

---

## FUTURE / NEXT STEPS (addendum — held, not scheduled)

The current distributional/generative approach has reached a realistic endpoint: the
hard-axis signature is reproducible, so more generators are low-yield. The open threads,
in rough priority, are:

1. **Root↔leaf human panel** — the *only* decisive test for the one surviving visual
   lead (E12). Pre-registered, power-analysed, independent human raters on the
   high-confidence consensus subset. Blocked on protocol + raters, not on code. _(Held.)_
2. **Clean up the i09 residual** — eliminate the mean-word-length construction artifact,
   replace the single-fixed-length assumption, and put the soft fc_z/wc_z axes on a proper
   generator-side null — after which "the distributional signature does not discriminate
   the mechanism" can be stated at full strength.
3. **A new framework: symbols-as-values / quantitative encodings** — test whether
   Voynichese behaves like a *data* record (numerals, tables, a positional/accounting
   register) rather than transcribed language, using decipherment-free statistical probes
   (digit-frequency/Benford checks, base-N modular periodicity, place-value structure,
   glyph-value entropy vs known numeral systems). This is consistent with — not excluded
   by — the envelope (low entropy + block structure + weak word-syntax + cipher-of-prose
   exclusion all fit a non-glottographic register). See the companion review
   [FRAMEWORKS.md](FRAMEWORKS.md). _(Exploratory; L7 still binds — a checkable data artifact
   would be required before any claim.)_
4. **Meta-analysis / packaging** — the self-correction record is publishable independently
   of any Voynich finding; a methods paper on "adversarial self-correction for
   undeciphered-corpus research" is a natural standalone.
5. **Standing robustness debts** — multi-seed/bootstrap the remaining single-seed grids;
   v101 (GC) transliteration sensitivity beyond a spot layer; a second cross-vendor visual
   rater.
