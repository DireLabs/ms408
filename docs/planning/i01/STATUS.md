# STATUS.md — i01 Coordination Bus

**Protocol:** any session that starts, finishes, or blocks a task — or raises a new D-item — updates
this file (and DECISIONS.md when relevant). Keep entries terse; this is how Code sessions, Cowork
sessions, and Tim stay synchronized.

_Last updated: 2026-07-05 (Code session 1)_

## Gates

| Gate | State | Notes |
|---|---|---|
| G0 decision locks | ✅ signed off 2026-07-05 | D1–D8, D10, D11 locked as L11–L20. D9 open until end of Phase 1; D12 open until T1.3. |
| G1 replication | pending | |
| G2 annotation | pending | |
| G3 synthesis | pending | |
| G4 final | pending | |

## Tasks

| ID | State | Notes |
|---|---|---|
| T0.1 decision locks | ✅ done 2026-07-05 | G0 run in-session with Tim. |
| T0.2 corpus pipeline | 🔄 nearly done | Sources verified (SOURCES.md) + pinned by sha256. IVTFF parser + integrity tests green (227p/5385 loci ZL; 226p/5367 GC). Versioned dataset v0.1.0 builds with provenance manifest. Scans: IIIF crawl running. Remaining: scan↔page join after crawl. |
| T0.3 validation harness | 🔄 in progress | Source verification ✅ done — both generators have author code (GitHub) + free algorithm descriptions; replication targets all freely accessible. Implementation not started. |
| T2.5 W4 dossiers | ⬜ ready | Unblocked by G0. Awaiting Cowork session 1 — kickoff brief in WORKFLOW.md §6. |
| all others | ⬜ blocked | Per DAG in WORKFLOW.md §3. |

## Sessions

- **Code session 1** (Claude Code, Fable 5) — workflow setup, G0, now T0.2 + T0.3. Started 2026-07-05.
- **Cowork session 1** — T2.5 dossiers. Ready for Tim to launch with the WORKFLOW.md §6 brief.

## New D-items raised since G0

(none)
