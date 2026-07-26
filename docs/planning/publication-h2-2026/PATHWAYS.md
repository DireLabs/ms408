# Publication pathways

Four pathways, codenamed **alpha / beta / gamma / delta**, chosen from the scored opportunities
([`SCORING.md`](SCORING.md)). They are deliberately non-exclusive and target *different
audiences*, so several can run in parallel (journals have no deadlines; conferences do). Each
has a v1 brief at `pathways/<name>/v1.md`.

| Codename | Paper | Primary venue | Alt | Audience | Why |
|---|---|---|---|---|---|
| **alpha** | A (constraint-envelope) | **TACL** | Computational Linguistics | Computational linguistics | Top-scored (4.50): free, flagship, fast rolling review, undeciphered-script appetite, anti-solution posture matches L7 |
| **beta** | B (methods) | **LRE** | Cambridge NLP | NLP methods / evaluation / reproducibility | Best economics for B (free non-OA route) + evaluation-methodology home |
| **gamma** | A (constraint-envelope) | **DHQ** | DSH | Digital humanities / manuscript studies | Direct 2026 no-decipherment Voynich precedent (Layfield & Fagin Davis); diamond OA; a *different readership* than alpha |
| **delta** | A (fast) + B (fast) | **CHR 2027** (A) & **EACL 2027 via ARR** (B) | HistoCrypt 2027 (A) | The research community, quickly | Imminent confirmed deadlines (Aug 14 / Aug 3) → fastest path to community visibility |

## How the four relate

- **alpha + gamma** publish *Paper A* to two non-overlapping audiences (CL/NLP vs DH). This is
  fine and common — but if simultaneous submission is a concern, alpha is the primary and gamma
  the fallback/second-audience; do not double-submit the *same* manuscript to two journals at
  once (dual-submission violation). Stagger, or differentiate the framing enough to be distinct
  contributions.
- **beta** is *Paper B*'s journal home; **delta** is the *conference fast-path* for either paper
  when speed matters more than journal prestige.
- **delta is time-boxed:** its value is the imminent Aug deadlines. If we don't move on those,
  delta collapses into "monitor HistoCrypt/SIGTYP for the winter cluster" and the journals
  (alpha/beta/gamma) become the spine.

## Decision gates (Tim)

1. **Speed or prestige?** Attempt the imminent Aug conference deadlines (delta), or aim the
   journals (alpha/beta/gamma) with no deadline pressure? The papers exist (v7, methods-v3), so
   Aug is *feasible* but tight (double-blind prep, format conversion).
2. **Which pathways to greenlight?** Recommended default: **alpha + beta** as the spine
   (journal homes for A and B), **gamma** as A's DH second-audience, **delta** only if we commit
   to an August push this week.
3. **Custom domain / arXiv-first?** Posting v7 + methods-v3 to arXiv now (allowed by current ACL
   policy, no blackout) establishes priority and is cited by every pathway. Recommended before
   any submission. (Ties to the OSS_RELEASE DOI item.)

## Per-pathway briefs

- [`pathways/alpha/v1.md`](pathways/alpha/v1.md) — Paper A → TACL
- [`pathways/beta/v1.md`](pathways/beta/v1.md) — Paper B → LRE
- [`pathways/gamma/v1.md`](pathways/gamma/v1.md) — Paper A → DHQ
- [`pathways/delta/v1.md`](pathways/delta/v1.md) — conference fast-path (CHR / EACL / HistoCrypt)

Each v1 is a *publication brief* (venue-tailored title + abstract, adaptation diff vs the
existing manuscript, format checklist, cover-letter angle, next deadline, risks) — not a new
full manuscript, since the content already exists in `paper/`. Full venue-tailored drafts are
produced once a pathway is greenlit.
