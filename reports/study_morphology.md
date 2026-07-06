# T2.1 Study Report — Morphology and Positional Structure (W2)

Generated 2026-07-06T03:39:11+00:00 at commit `fbb6107fe0` by `python -m ms408.studies.morphology`; full numbers in `results/studies/morphology.json`. All corpora truncated to 34,111 tokens (the ZL paragraph corpus) for comparability.

| corpus | class | ED1 main comp. | mean degree | position entropy | affix coverage | curve/line valid |
|---|---|---|---|---|---|---|
| zl_all | H1 | 0.7975 | 6.564 | 0.6675 | 0.6653 | 0.8875 |
| zl_currierA | H1 | 0.7544 | 5.253 | 0.7055 | 0.6635 | 0.9055 |
| zl_currierB | H1 | 0.8183 | 6.222 | 0.6315 | 0.668 | 0.8788 |
| gc_v101 | H1-sensitivity | 0.8927 | 11.71 | 0.643 | 0.5629 | 0.1264 |
| h2_naibbe | H2 | 0.944 | 9.631 | 0.6161 | 0.7003 | 0.8437 |
| h3_selfcitation | H3 | 0.9106 | 6.359 | 0.6699 | 0.7424 | 0.9676 |
| h4_latin | H4 | 0.1632 | 1.1 | 0.9185 | 0.6371 | 0.0254 |
| h4_italian | H4 | 0.2191 | 1.491 | 0.8641 | 0.5264 | 0.1092 |

Column meanings: **ED1 main comp.** = share of word types in the largest edit-distance-1 component (VMS published ≈ 0.847); **position entropy** = frequency-weighted normalized entropy of glyph position within words (0 = fully position-locked); **affix coverage** = tokens carrying both a top-10 prefix and top-10 suffix; **curve/line valid** = tokens accepted by Timm's adjacency grammar.

## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 review — L10)

1. **[C, candidate B pending T3.3]** Voynichese glyph positions are far more restricted than natural-language controls at matched size: mean normalized position entropy 0.6675 (ZL) vs 0.8641–0.9185 (H4 Latin/Italian). The gibberish classes H2/H3 (0.6161, 0.6699) sit near the VMS, consistent with position restriction being the h2-anomaly mechanism (Lindemann-Bowern) that both generator families were designed to reproduce.
2. **[C, candidate B pending T3.3]** The VMS edit-distance-1 network is far denser than natural language at matched token count: main-component share 0.7975 (ZL; published ≈0.847 on the full MS) vs 0.1632–0.2191 (H4). H3 self-citation (0.9106) reproduces this by construction; H2 Naibbe (0.944) also lands high — so network density alone does not discriminate cipher from gibberish.
3. **[C]** Affix regularity: 67% of ZL tokens carry both a top-10 prefix and top-10 suffix (A: 66%, B: 67%).
4. **[C]** Timm's curve/line grammar accepts 89% of ZL tokens vs 3%/11% for H4 — Voynichese is grammar-constrained at the glyph-adjacency level in a way natural text is not. (EVA-specific measure: the v101 value (13%) reflects the different glyph alphabet, not a sensitivity failure — excluded from the L11 pass.)
5. **[C]** v101 sensitivity (L11): the GC corpus gives main-component 0.8927 and position entropy 0.643 — the direction of claims 1-2 (dense network, strong position restriction vs natural controls) is unchanged under the alternative transliteration.

## Affix inventories (ZL full)

Top prefixes: `o` 20.1%, `c` 18.6%, `ch` 16.1%, `q` 15.5%, `qo` 15.0%, `s` 11.3%, `d` 9.1%, `qok` 8.9%

Top suffixes: `y` 39.9%, `dy` 17.4%, `n` 16.5%, `in` 16.2%, `l` 15.1%, `r` 14.6%, `edy` 11.7%, `iin` 11.5%
