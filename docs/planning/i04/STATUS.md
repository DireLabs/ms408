# STATUS.md — i04 Coordination Bus

_Last updated: 2026-07-09 (i04 COMPLETE — E11 survives; E12 UNRESOLVED-underpowered)._

**i04 outcome:** the root↔leaf bundle survived the palette-style control (E11) but the
independence test (E12) shows the model-annotation approach is **underpowered/untestable**
(leaf-label noise ceiling). E10's positive-candidate claim is **withdrawn to UNRESOLVED**.
Decisive future test = human panel. D-i04-1 is effectively **moot** — a 5th model can't
settle a noise-limited question, so Google-billing for Gemini is **not** needed for this.

**Inherits:** all locks L1–L37; standing refutation rule; L8 stratification.
Continues the experiment ledger as E11–E12. Focused iteration: E10 confirm-or-kill.

## Experiments

| id | question | priority | state | verdict |
|---|---|---|---|---|
| E11 | Illustration-style control for root↔leaf | P1 | ✅ done → **survives (partial control)** | [C] Bundle survives conditioning on palette-richness style for BOTH models (palette-alone p: sonnet 0.003, haiku 0.014; holds through palette×hand×dialect). Not a palette-style artifact. CAVEAT: partial control (palette richness is the only usable style annotation); E12 independence remains decisive. |
| E12 | Independent-lineage (non-Anthropic/human) root rater | P1 | ✅ done + refuted → **UNRESOLVED-underpowered** | [C] GPT-5.1 (OpenAI, $0.20) re-annotated all 129 pages. GPT root agrees 0.86–0.91 with Anthropic roots yet does NOT reproduce the leaf association (cross-rater nulls: gpt_root×anthropic_leaf p 0.5–0.97). First-pass "KILLED (rater-idiosyncratic)" was CORRECTED by refutation: the root-agreement argument is a red herring (noisy variable is LEAF, κ≈0.45 for all). Consensus-subset power analysis: n=74 reliable pages, effect ~nil there (V=0.19 p=0.63) but MDE φ=0.33 ⇒ underpowered for the ~0.28 effect. **Terminal: model annotation cannot adjudicate; a 5th model won't help (leaf-noise ceiling). E10's positive-candidate claim WITHDRAWN to UNRESOLVED.** Decisive future test = pre-registered 3-human panel on the consensus subset. |

## Open decisions for Tim

- **D-i04-1 — E12 rater source:** non-Anthropic vision model (needs non-Anthropic
  API credentials) · human rater (logistics) · defer E12. Blocks E12; E11 is
  independent of it. **Research (2026):** default = **Google Gemini 3 Flash**
  (`gemini-3-flash`) — best non-Anthropic vision, combines structured-output +
  function-calling for enum-locked fields, ~$0.30–1.00 for 129 images; add
  **GPT-5.x** (OpenAI) as a second cross-pretraining voter for a defensible
  independence claim. Specialized botanical/manuscript models are a POOR fit
  (taxon classifiers / HTR, misaligned with coarse-morphology enums; Voynich plants
  are fantastical). Independence caveat: all VLM encoders descend from CLIP-ViT;
  Gemini+GPT (SigLIP-family vs CLIP-descended) is the strongest cross-vendor,
  cross-pretraining split available. Needs Google (and/or OpenAI) API key in `.env`.

## Sessions

- **Code session (i04)** — spec drafted 2026-07-09. E11 can start immediately;
  E12 on Tim's rater-source decision.
