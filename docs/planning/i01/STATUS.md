# STATUS.md — i01 Coordination Bus

**Protocol:** any session that starts, finishes, or blocks a task — or raises a new D-item — updates
this file (and DECISIONS.md when relevant). Keep entries terse; this is how Code sessions, Cowork
sessions, and Tim stay synchronized.

_Last updated: 2026-07-05 (Code session 1)_

## Gates

| Gate | State | Notes |
|---|---|---|
| G0 decision locks | ✅ signed off 2026-07-05 | D1–D8, D10, D11 locked as L11–L20. D9 open until end of Phase 1; D12 open until T1.3. |
| G1 replication | ✅ signed off 2026-07-06 | 35/38 scored targets PASS; D13–D18 locked as L21–L26. Report: reports/replication_report.md @ ab19821. |
| G2 annotation | ✅ signed off 2026-07-06 | Schema v0.2-fine; QA passes retuned thresholds (L32). root_type flagged low-confidence (L33). T2.3b unblocked. |
| G3 synthesis | pending | |
| G4 final | pending | |

## Tasks

| ID | State | Notes |
|---|---|---|
| T0.1 decision locks | ✅ done 2026-07-05 | G0 run in-session with Tim. |
| T0.2 corpus pipeline | ✅ done 2026-07-05 | Text: pinned acquisition + IVTFF parser + dataset v0.1.0 w/ provenance manifest. Scans: all 213 canvases full-res (536 MB), 0 dimension mismatches. Scan↔page join: 227/227 mapped; 20 foldout panels ambiguous (2 candidates each — resolve visually at T1.2); 9 unmatched canvases are binding shots. 19 tests green. |
| T0.3 validation harness | ✅ done 2026-07-05 | H2 Naibbe (golden decrypt byte-exact) + H3 self-citation (5-seed distributional match; spec §17 fidelity notes) + H4 normalized in 4 languages w/ edition registers + scoring API (textstats) + **benchmark report**: 29 corpora in reports/harness_benchmark.md, results/harness/benchmark.json. Class separation as designed: H1 h2≈2.0–2.1 vs H4 naturals 2.9–3.9; H2/H3 reproduce the low-h2 property. Informal: ZL Currier B h1/h2 = 3.866/1.958 vs published EVA VMS-B 3.860/1.954 — formal comparison is T1.1. |
| T1.1 replication gate | ✅ done — **G1 signed off 2026-07-06** | 35/38 scored targets PASS (h2 full 2.1637 vs 2.1593; MZ peak 812 vs 807; glyph rules within ~1%). Tolerances locked (L25), MZ policy locked (L26). |
| T1.2 annotation schema | ✅ done 2026-07-06 | v0.1-coarse locked with defaults (L31). T12-annotation-schema.md. T1.3 green-lit under $100 cap. |
| T1.4 W6a assumption audit | ✅ done 2026-07-06 | 11 assumptions, 11 variants (W6a-assumption-audit.md); Tim approved P1 set (L30); **P1 sweeps run** — see reports/study_p1_variants.md. Headline: verbose-cipher family cannot retain word-order info (V2/V2c); paradigmatic conlang reproduces the full VMS signature (V3). P2/P3 variants (V6 resegmentation, V7 line-conditioning, V9 compositions, V10, V11) remain. |
| T2.1 morphology | ✅ done 2026-07-06 (baseline) | 4 stat families × 8 corpora at matched size. VMS+gibberish classes co-cluster on every axis vs naturals. reports/study_morphology.md. Variant sweep pending T1.4. |
| T2.2 topic alignment | ✅ done 2026-07-06 (baseline) | Key test result: co-occurrence structure dominated by A/B (v101 2-cluster ARI 0.90); section alignment survives dialect confound in Language A only (ARI 0.35/0.27, p=0.0005); B textually homogeneous across sections (null). reports/study_topics.md. |
| T2.4 encoding bracket | ✅ done 2026-07-06 (baseline) | No family reproduces low-h2 + intact word-order info together. Homophonic verbose cipher erases MZ info (0.000 vs 0.307); self-citation overshoots at wrong scale. reports/study_encoding_bracket.md. Parameter sweeps pending T1.4. |
| T2.5 W4 dossiers | ✅ done 2026-07-06 | All 5 in docs/dossiers/ (cipher culture, balneology, gynecological reading, astro iconography, provenance chain), claims graded C/D. New D-items D19/D20 (deferred). Key tensions for W6b: German/Alemannic zodiac iconography vs L1 northern-Italy premise; no attested in-window verbose cipher; provenance C-solid only from 1637. |
| T1.3 bulk annotation | ✅ done — **G2 signed off 2026-07-06** | 227 pages, schema v0.2-fine, $3.55. QA passes ratified thresholds (L32): 0.211/0.223/0.346 vs 0.25/0.25/0.40. root_type low-confidence (L33). Dataset accepted. |
| T2.3b label-level anchoring | ✅ done 2026-07-06 | Labels are NOT a naming system: herbal near-label-free (3/129); in every labeled section labels recur LESS than running text (pharma 95% unique, 8 recurring vs null [25,41]). Coherent with T2.3a — no word→referent mapping detectable. reports/study_anchor_labels.md. |
| T2.3 anchor hunt | ✅ done 2026-07-06 (page-level) | Harness gate PASSED (null 0/14758 false disc.; planted recovered). **Rigorous null**: no token anchors to a herbal feature after FDR; nothing behaves like "root" at page granularity. Strongest raw signals = noise / A/B confound. Label-level follow-up (T2.3b) flagged. reports/study_anchor_hunt.md. |
| T2.6 W7 discriminator | ✅ done 2026-07-06 | Referential-realism: "within-organ-only" — root_type×leaf_shape (the realism bundle) ABSENT (p=0.26, saturated); constraint only in tautological within-leaf geometry. No root↔leaf real-taxa bundle. Anachronism scan = rigorous null. reports/study_referential_realism.md. **Phase 2 COMPLETE (7/7 studies).** |
| **Phase 3** (T3.1→T3.2 G3→T3.3→T3.4 G4) | ⬜ ready | **All Phase 2 studies + dossiers complete.** T3.1 competing narratives next. |

## Sessions

- **Code session 1** (Claude Code, Fable 5) — the program's primary session per amended L9: Phase 0+1 complete, G0+G1 gates passed, T2.1/T2.2/T2.4 baselines done. As of 2026-07-06, orchestrating 7 background subagents: 5× T2.5 dossiers, T1.4 assumption audit (matrix → Tim review per L29), T1.2 annotation schema.
- Cowork: not in use for this program (Tim's Cowork capacity committed elsewhere; L9 amended).

## New D-items raised since G0

All resolved at G1 (2026-07-06): D13–D18 locked as L21–L26. Open by design: D9 (publication intent, decide by end of Phase 1), D12 (annotation budget, set before T1.3 — I'll bring a cost estimate when T1.2's schema exists).
