# MS408 Research Program — Voynich Manuscript (Beinecke MS 408)

Computational and historical analysis of the Voynich Manuscript, scoped to content, language
structure/semantics, visual semantics, and creation-milieu influences.

**Orient first:** `docs/planning/i01/` holds the program docs — `README.md` (rules of engagement),
`DECISIONS.md` (locked/open decision ledger), `RESEARCH-PLAN.md` (workstreams, validation harness,
evidence grading), `WORKFLOW.md` (task table, DAG, session briefs), `STATUS.md` (current task and
gate state — read it to orient, update it whenever you change a task or gate state).

## Binding rules — every session and every subagent

1. **Firewall (L3).** All statistics come from deterministic, versioned code in `src/`, written to
   `results/`. Never estimate or recall a metric in-context; if a number isn't in `results/`, write
   the script that computes it.
2. **Harness first (L4).** No method makes claims about the real manuscript until validated on the
   synthetic benchmark (RESEARCH-PLAN §3).
3. **Replication gate (L5).** No novel experiments until the pipeline reproduces published baseline
   statistics (T1.1, gate G1 — Tim signs off).
4. **No translation claims without an independent statistical anchor (L7).** Ever. Plausible-sounding
   output is the field's primary failure mode.
5. **Evidence grading (L6).** Every claim in every output carries a grade A–D (RESEARCH-PLAN §6).
   Ungraded claims are treated as grade D.
6. **Flag, don't resolve.** Any decision not covered by DECISIONS.md becomes a new D-item surfaced
   to Tim; continue on the least-committal path or pause if blocked. No silent judgment calls.
7. **Stratification (L8).** All text analyses stratify by Currier A/B dialect and scribal hand.
8. **Transliteration (L11).** EVA is primary; all Phase 2 experiments get a v101 sensitivity pass.
9. **Licensing (L19).** Consume-only for external data until verified and Tim sets policy. Raw
   downloads live in `data/raw/` (gitignored); do not redistribute or commit third-party data.

## Layout

- `src/` — pipeline, harness generators, statistics. The only source of numbers.
- `data/raw/` (gitignored) — external sources as downloaded. `data/processed/` — versioned derived dataset.
- `results/` — machine-written JSON from `src/` scripts. Every result file records its producing
  script, git commit, input dataset version, and parameters.
- `reports/` — human-readable study reports with graded claims.
- `docs/dossiers/` — W4 influence dossiers. `docs/planning/i01/` — program docs and STATUS.md.

Python is the working language. Prefer boring, reproducible code: pinned dependencies, fixed seeds,
and no notebook-only analyses — anything that produces a reported number must be a script.
