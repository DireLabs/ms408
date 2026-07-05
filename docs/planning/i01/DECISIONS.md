# DECISIONS.md — Locked/Open Ledger

**Change protocol:** only Tim promotes Open → Locked or amends a Lock. Agents encountering an uncovered decision add a new D-item with options and implications, then continue on the least-committal path or pause if blocked. Silent resolution is a process violation.

**G0 signed off 2026-07-05:** D1–D8, D10, D11 locked (L11–L20 below). D9 and D12 remain open by design, with their own decision points.

## Locked

| ID | Decision | Rationale |
|---|---|---|
| L1 | Working premise: genuine early-15th-c. artifact, meaningful content. Scoped assumption, not a truth claim. | Program framing per Tim; hoax hypothesis acknowledged, out of scope; W7 studies stress-test from within. |
| L2 | Scope: content, language structure/semantics, visual semantics, creation influences. No new physical forensics. W7 contact mechanism is a black box — no investigation of "who/how." | Keeps W7 falsifiable and the program grounded. |
| L3 | Firewall: deterministic versioned code computes all statistics; models never estimate metrics in-context. | The field's primary failure mode is plausible generation; this is the program's differentiator. |
| L4 | Harness-first: no method makes real-manuscript claims before validating on the synthetic benchmark. | Discipline against pattern-matching-as-decryption. |
| L5 | Replication gate (G1) before any novel experiment. | Pipeline bugs must not masquerade as findings. |
| L6 | Evidence grading (A–D per RESEARCH-PLAN §6) required on every claim; ungraded = D. | Traceability of the narrative deliverable. |
| L7 | No translation claims without an independent statistical anchor. | Non-negotiable, ever. |
| L8 | Multi-scribe working model (Fagin Davis hands); Currier A/B stratification in all text analyses. | Both are established structure; ignoring them confounds results. |
| L9 | Execution split: Cowork + subagents default; Claude Code for code-producing/technical tasks. | Tim's standard workflow. |
| L10 | Adversarial review by clean-context critic instances before any claim is graded A or B. | Decorrelates authorship bias from evaluation. |
| L11 | (was D1) Transliteration: EVA primary; v101 sensitivity pass on all Phase 2 experiments. | G0 2026-07-05. Guards against transliteration overfitting while keeping one canonical corpus. |
| L12 | (was D2) f116v marginalia: appendix-only — catalog it, don't build on it. | G0 2026-07-05. Small text, outsized speculation surface. |
| L13 | (was D3) H4 reference corpora: Latin + Italian + MHG + Hebrew; extend only if a bracket result motivates it. | G0 2026-07-05. Covers Romance, Germanic, and an abjad for the encoding bracket. |
| L14 | (was D4) Plant identifications are soft priors, never hard anchors. | G0 2026-07-05. Avoids importing centuries of contested IDs into the anchor hunt. |
| L15 | (was D5) Annotation schema starts coarse (~10 features/illustration); extend after first QA batch. | G0 2026-07-05. Revisit granularity at T1.2 with QA data in hand. |
| L16 | (was D6) Second model family as outside critic in T3.3, for A-graded claims only. | G0 2026-07-05. Decorrelated blind spots where the stakes are highest. |
| L17 | (was D7) Codex Seraphinianus control deferred; revisit if the T2.6 discriminator is ambiguous. | G0 2026-07-05. |
| L18 | (was D8) Repo name: `voynich-manuscript`. | G0 2026-07-05. Existing repo confirmed. |
| L19 | (was D10) Licensing: consume-only for all external data until T0.2 verification; Tim revisits policy on findings. | G0 2026-07-05. Raw downloads gitignored; no redistribution. |
| L20 | (was D11) Star-section comparisons start with widely available period references; expand on signal. | G0 2026-07-05. Bounds T2.6 Study 1 astronomy leg. |

## Open

| ID | Question | Options | Implications | Recommended default | Owner |
|---|---|---|---|---|---|
| D9 | Publication intent | Private · blog series · preprint | Sets rigor bar, licensing care, and write-up format for T3.4 | Decide by end of Phase 1 | Tim |
| D12 | API budget envelope for bulk annotation | Spend cap for Sonnet 4.6 batch + QA | Bounds T1.3 batch sizing and retry policy | Tim sets cap before T1.3 | Tim |
