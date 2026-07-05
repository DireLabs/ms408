# MS408 Research Program — Handoff Package

Research program for computational and historical analysis of the Voynich Manuscript (Beinecke MS 408), scoped to content, language structure/semantics, visual semantics, and creation-milieu influences. Working premise: genuine early-15th-century artifact with meaningful content.

## Package contents (read in this order)

1. **README.md** — this file. Orientation and rules of engagement.
2. **DECISIONS.md** — locked/open decision ledger. Read before doing anything; L-items are binding, D-items must be flagged to Tim, never silently resolved.
3. **RESEARCH-PLAN.md** — the program: premise, design principles, validation harness, workstreams W1–W7, phasing, evaluation rubric, deliverables.
4. **WORKFLOW.md** — execution: task table with dependencies, DAG, surface/model routing (Claude Cowork vs. Claude Code), QA protocol, session kickoff briefs.

## Roles

- **Tim** — program owner and reviewer. Sole authority to lock open decisions and sign off at human gates (G0–G4).
- **Claude Cowork (+ subagents)** — default surface: research dossiers, annotation schema and QA, assumption audit, narrative synthesis, interpretation, adversarial critique orchestration.
- **Claude Code** — technical surface: corpus pipeline, validation harness, all statistical machinery, annotation pipeline plumbing, discriminator implementations.

## Rules of engagement (binding on all agents)

1. **Firewall principle.** All statistics are computed by deterministic, versioned code. Models never estimate metrics in-context. Models design, interpret, critique — scripts measure.
2. **Harness first.** No method makes claims about the real manuscript until validated on the synthetic ground-truth harness (RESEARCH-PLAN §3).
3. **Replication gate.** No novel experiments until the pipeline reproduces published baseline statistics (T1.1, gate G1).
4. **No translation claims without an independent statistical anchor.** Ever. Plausible-sounding output is the field's primary failure mode and ours to avoid.
5. **Evidence grading.** Every claim in every output carries a grade (A–D scale, RESEARCH-PLAN §6). Ungraded claims are treated as grade D.
6. **Flag, don't resolve.** Any decision not covered by DECISIONS.md gets logged as a new D-item and surfaced to Tim. Agents do not make silent judgment calls on open questions.

## Status

Phase 0, not started. Gate G0 (decision locks) is the first action — D1 (transliteration choice) blocks the critical path.
