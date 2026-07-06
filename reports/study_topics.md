# T2.2 Study Report — Topic Induction and Section Alignment (W2 key test)

Generated 2026-07-06T03:43:33+00:00 at commit `fbb6107fe0` by `python -m ms408.studies.topics`; full numbers in `results/studies/topics.json`.

Method: page TF-IDF (top 400 words, pages ≥30 tokens, paragraph text only), cosine, deterministic average-linkage; ARI/NMI with 2000 permutations, seed 408. No image information or labels enter the clustering — only word co-occurrence.

| comparison | ARI | NMI | p (perm.) |
|---|---|---|---|
| ZL k=sections vs sections | 0.0668 | 0.2433 | 0.004 |
| ZL k=sections vs Currier | 0.4043 | 0.4103 | 0.0005 |
| ZL k=sections vs hands | 0.2398 | 0.3701 | 0.0005 |
| ZL two largest clusters vs Currier | 0.4374 | 0.4511 | 0.0005 |
| ZL within-A vs sections (114p, k=4) | 0.3507 | 0.3444 | 0.0005 |
| ZL within-B vs sections (83p, k=5) | 0.0036 | 0.1657 | 0.4028 |
| v101 k=sections vs sections | 0.2835 | 0.3905 | 0.0005 |
| v101 k=sections vs Currier | 0.6291 | 0.6002 | 0.0005 |
| v101 k=sections vs hands | 0.5249 | 0.5683 | 0.0005 |
| v101 two largest clusters vs Currier | 0.9036 | 0.8393 | 0.0005 |
| v101 within-A vs sections (114p, k=4) | 0.2714 | 0.3482 | 0.0005 |
| v101 within-B vs sections (83p, k=5) | 0.0086 | 0.1814 | 0.27936 |

Section↔Currier confound (labels only): ARI 0.2793, NMI 0.3778.

## Sequential boundary test (ZL, manuscript order)

Adjacent-page cosine similarity: within-section 0.2636 vs across-boundary 0.1949 (difference 0.0687, p=0.03448, 23 boundaries).

## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 review — L10)

1. **[C, candidate B pending T3.3]** The dominant structure recoverable from word co-occurrence alone is the Currier A/B split, not the sections: clusters align with dialect at ARI 0.4043 (ZL) / 0.6291 (v101), and the two dominant clusters recover A/B at ARI 0.4374.
2. **[C, candidate B pending T3.3]** Section structure is present above chance at whole-MS level on both transliterations (ZL ARI 0.0668, p=0.004; v101 ARI 0.2835, p=0.0005) — but the dialect-confound control reveals a sharp ASYMMETRY: within Language A the text tracks the sections strongly (A: ARI 0.3507 (p=0.0005, 114p); v101 ARI 0.2714 (p=0.0005)), while within Language B it does not (B: ARI 0.0036 (p=0.4028, 83p); v101 ARI 0.0086 (p=0.27936)). At page-vector granularity, B's sections (bio, stars, herbal-B, recipes) are textually homogeneous — the text-image co-variation is an A-side phenomenon.
3. **[C]** The sequential view agrees: adjacent pages are more similar within sections than across boundaries (Δ=0.0687, p=0.03448); section↔dialect label correlation is ARI 0.2793 for reference.
4. **[C]** Method notes: deterministic average-linkage; k=2 cuts are chaining-degenerate (evaluated via the two largest clusters instead); v101 consistently shows STRONGER alignments than EVA — the transliteration's finer glyph distinctions appear to carry signal, worth a T1.4 variant.
