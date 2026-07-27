# Venue-tailored publication drafts

Full drafts adapted from the base manuscripts (`paper/v7` = Paper A; `paper/methods/v3` =
Paper B) for the pathways in `docs/planning/publication-h2-2026/`. Draft order (Tim's call):
**journals first, scored order** — alpha → beta → gamma → delta.

| Dir | Pathway | Paper → venue | Status |
|---|---|---|---|
| `alpha-tacl/` | alpha | A → TACL | ✅ v1 drafted (5pp, compiles clean) — anonymized, tool reframed as benchmark |
| `beta-lre/` | beta | B → LRE | ✅ v1 drafted (5pp) — methods paper reframed around released evaluation resources |
| `gamma-dhq/` | gamma | A → DHQ | ✅ v1 drafted (4pp) — DH/epistemology-first sibling of alpha (numbers-light) |
| `delta-conf/` | delta | A → CHR / HistoCrypt / Voynich Conf | ✅ v1 drafted (2pp conference short paper) |

All four v1 drafts compile clean (0 undefined refs/citations). Alpha & gamma both carry Paper A
to different audiences — see the gamma coordination note (do not dual-submit the *same*
manuscript; stagger or keep the framings distinct).

## Discipline notes

- **Firewall.** Every number in these drafts traces to the base papers, which are
  firewall-sourced from `results/**`. No new numbers are introduced here — only reframing,
  compression, and venue-specific positioning.
- **Formatting.** Drafts use `article` class for portability and to compile with the repo's
  toolchain. Convert to the venue's official template at submission (ACL/TACL `acl.sty` for
  alpha; Springer LRE for beta; DHQ's XML workflow for gamma; CEUR/ACL for delta). The content
  adaptation is the work; the template swap is mechanical.
- **Anonymization.** alpha (TACL) is drafted double-blind (author/affiliation and the tool's
  repo withheld). LRE/DHQ single-blind — de-anonymize per venue policy at submission.
- **Before submitting any:** post the base preprints to arXiv to timestamp priority (allowed;
  no ACL blackout), resolve the `% UNVERIFIED` bib details, and fix the `ti.mims.ms` contact.
