# STATUS.md — i04 Coordination Bus

_Last updated: 2026-07-09 (spec drafted; E11 unblocked, E12 awaits D-i04-1)._

**Inherits:** all locks L1–L37; standing refutation rule; L8 stratification.
Continues the experiment ledger as E11–E12. Focused iteration: E10 confirm-or-kill.

## Experiments

| id | question | priority | state | verdict |
|---|---|---|---|---|
| E11 | Illustration-style control for root↔leaf | P1 | ✅ done → **survives (partial control)** | [C] Bundle survives conditioning on palette-richness style for BOTH models (palette-alone p: sonnet 0.003, haiku 0.014; holds through palette×hand×dialect). Not a palette-style artifact. CAVEAT: partial control (palette richness is the only usable style annotation); E12 independence remains decisive. |
| E12 | Independent-lineage (non-Anthropic/human) root rater | P1 | ⬜ blocked on D-i04-1 (research done → Gemini 3 + GPT-5 recommended) | — |

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
