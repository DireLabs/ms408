# Refutation archive

Preserved outputs of the program's standing **clean-context adversarial refutation pass**
(binding rule; see `CLAUDE.md` and RESEARCH-PLAN §6). Each file is the actual brief returned
by an independent skeptic — a fresh-context agent given the claim, the code, and the data but
not the original analyst's narrative — tasked to build the strongest case against a finding.

This archive exists to close a gap the pass itself surfaced: the methods paper
(`paper/methods/`) argues "no claim should live only in prose," yet for most of the program
the refutation briefs lived only in prose (their corrected *numbers* are in `results/`, but
the adversary's reasoning was not versioned). Preserving the briefs makes the ``the refuter
caught it'' attributions **dereferenceable and checkable**, not operator summary.

## Honest coverage note

- **Archived here:** the briefs from iteration i06 onward (the current session): E21, the
  E22/E23 genericity+reuse pass, the E25/E26/v5 deflation pass, and the pass on the methods
  paper itself. These are the verbatim adversary outputs as received.
- **NOT archived (a real gap):** the earlier-iteration briefs (i03–i05: E6, E7, E8, E9, E12,
  E14/E17, …) were produced in prior sessions and their full text was not captured; they are
  documented only in `docs/synthesis/FLAGSHIP.md` §7 and their corrected numbers in
  `results/experiments/`. Those Table-1 rows in the methods paper are therefore corroborated
  by the corrected numbers (firewall-checkable) but the adversary's *reasoning* for them is
  not independently preserved.
- **Going forward:** every clean-context refutation is saved here.

## Standing caveat on independence

The refuter is *context*-independent (no access to the analyst's narrative or sunk cost) but
not model- or operator-independent: it is a fresh-context agent of the same model family,
spawned by the same operator, over the same repository. The one genuinely cross-vendor check
in the program (a non-Anthropic frontier model in E12) was used as a *rater*, not as a
refuter. Cross-vendor / human refutation remains the stronger check where stakes are high.

## Index

| file | target | verdict |
|---|---|---|
| `2026-07-15-e21-positional-generator.md` | E21 "class sufficiency [B]" | downgraded **B→C** (fitted point; shuffle-passable threshold) |
| `2026-07-15-e22-e23-genericity-reuse.md` | E22/E23 "structurally unreachable" | narrowed to "coupling within swept ranges" |
| `2026-07-16-e25-e26-v5-deflation.md` | v5 "reproduces all axes / signature doesn't constrain mechanism" | narrowed to "retraction, not reversal" → v5b |
| `2026-07-17-methods-paper.md` | the methods paper's inferential framing | record accurate; framing over-claims → v2 |
| `2026-07-17-e29-naibbe.md` | E29 "i06 confirmed against Naibbe" | ΔI test confounded → C; i06 ΔI leg weakened |
| `2026-07-17-paper-v6.md` | paper v6 i06 retraction | retraction sound; fabricated ~30σ + over-correction → v6b |
| `2026-07-22-e33-block-scale-di.md` | E33 "block-scale ΔI reaches VMS corner → leg dead" | direction BACKWARDS: the corner was a homophony-marker h2 artifact; fair model → 0 corners, "weakly separates" |
