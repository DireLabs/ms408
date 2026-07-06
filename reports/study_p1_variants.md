# P1 Variant Sweeps (T1.4 matrix, L30)

Generated 2026-07-06T17:36:35+00:00 at commit `6a216cb9a3` by `python -m ms408.studies.variants`; full numbers in `results/studies/p1_variants.json`. VMS reference (EVA/ZL): h2 2.1294, ΔI 0.3072 @ 812, ED1 0.7975.

## V2 — homophone-poor verbose cipher (the decisive sweep)

| deck | h2 | TTR | ED1 | ΔI | peak scale |
|---|---|---|---|---|---|
| 52 | 2.086 | 0.1643 | 0.944 | 0.0002 | 1364 |
| alpha-only | 1.5706 | 0.0108 | 0.336 | 0.0166 | 473 |
| alpha-only-deterministic | 1.5062 | 0.009 | 0.3464 | 0.0277 | 473 |
| VMS | 2.1294 | 0.2176 | 0.7975 | 0.3072 | 812 |

**Verdict [C, candidate B pending T3.3]:** no corner of the verbose-cipher family retains the VMS's word-order information. Removing homophony (alpha-only) and even making segmentation deterministic per plaintext type still leaves ΔI ≈ 0.02–0.03 vs the VMS's 0.307 — the fragmentation of words into sub-word cipher units is itself the destroyer, since cipher 'words' are units shared across many plaintext types. A verbose cipher that preserved word-token identity would have to map whole words to whole words — i.e., converge on a nomenclator/relexification structure (see V3).

## V3 — paradigmatic conlang (family upper bound)

h2 2.0286, mean len 6.502, ED1 0.7569, position entropy 0.565, ΔI 0.3564 @ 812 (VMS: ED1 0.7975, ΔI 0.3072 @ 812). template uses a VMS-informed affix inventory — this is the constructed-language family's UPPER BOUND, not a neutral parameterization.

**Verdict [C, candidate B pending T3.3]:** first family to reproduce the full VMS signature — low h2, dense ED1 network, positional restriction, AND word-order information at the right scale (812 words exactly). Combined with V2: the joint profile points at systems that map meaning-bearing word tokens ~1:1 to Voynichese types built from a tight positional template — relexification-like structure, whether construed as invented language, nomenclator-style whole-word cipher, or heavily conventionalized notation. The 'meaningful vs gibberish' question now concentrates in whether self-citation (which needs no plaintext) can be tuned to the VMS's TTR and MZ scale — its current misses.

## V4 — A/B-stratified bracket

- A (10,709 tokens): ranking selfcitation > verbose_cipher > conlang_paradigm > abjad_anagram > abbreviation; VMS-A h2 2.1848, ΔI 0.1777 @ 764
- B (22,864 tokens): ranking selfcitation > conlang_paradigm > verbose_cipher > abjad_anagram > abbreviation; VMS-B h2 2.0088, ΔI 0.2309 @ 381

## V5 — reading-order probe

ΔI forward {'scale': 812, 'value': 0.3072} vs words-reversed-within-lines {'scale': 812, 'value': 0.3071}; h2 forward 2.1294 vs glyph-reversed 2.1294. MZ ΔI is structurally near-invariant under within-line reversal (part membership barely changes) and h2 is exactly invariant under full string reversal (bigram bijection). The run documents these invariances: direction evidence must come from positional asymmetries (paragraph-initial gallows, line-final m), not from ΔI or h2.

## V8 — tokenization sensitivity

Across the 16-cell TextPolicy grid: h2 range [2.1289, 2.1996], ED1 main-component range [0.6863, 0.7978].

## V1 — v101 substrate (co-reported per L30)

v101 stream profile: h2 2.5329, ΔI 0.2765 @ 866, ED1 0.8945, TTR 0.2295 (EVA reference above). word segmentation is shared between transliterations; char-level metrics (h1/h2, ED1, position entropy) shift with v101's finer glyph units. Co-reported per L30; topics/morphology v101 rows already exist in their studies.
