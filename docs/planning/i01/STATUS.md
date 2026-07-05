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
| T0.2 corpus pipeline | ✅ done 2026-07-05 | Text: pinned acquisition + IVTFF parser + dataset v0.1.0 w/ provenance manifest. Scans: all 213 canvases full-res (536 MB), 0 dimension mismatches. Scan↔page join: 227/227 mapped; 20 foldout panels ambiguous (2 candidates each — resolve visually at T1.2); 9 unmatched canvases are binding shots. 19 tests green. |
| T0.3 validation harness | 🔄 in progress | Sources verified. Spec agents extracting both generator algorithms from author code; H4 control-text acquisition underway. Implementation next. |
| T2.5 W4 dossiers | ⬜ ready | Unblocked by G0. Awaiting Cowork session 1 — kickoff brief in WORKFLOW.md §6. |
| all others | ⬜ blocked | Per DAG in WORKFLOW.md §3. |

## Sessions

- **Code session 1** (Claude Code, Fable 5) — workflow setup, G0, now T0.2 + T0.3. Started 2026-07-05.
- **Cowork session 1** — T2.5 dossiers. Ready for Tim to launch with the WORKFLOW.md §6 brief.

## New D-items raised since G0

(none)
