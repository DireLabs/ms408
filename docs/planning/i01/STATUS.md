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
| T0.3 validation harness | 🔄 in progress | **H2 Naibbe done** (golden decrypt byte-exact; stats within author spread). **H3 self-citation done**: full reimplementation (tokenizer, curve/line rules, morph ops, page chooser, feedback stats, assembly); 5-seed means vs author reference: i 0.226/0.241, ol 0.397/0.396, dy 0.277/0.256 (all ±0.03 ✓), VMS overlap 0.688 (band 0.65–0.75 ✓); two spec ambiguities resolved empirically (spec §17, reconcile at D15). **H4 acquired** (13 files, licenses+sha256 in MANIFEST.json). Remaining: H4 normalization pass, scoring API, benchmark report. |
| T2.5 W4 dossiers | ⬜ ready | Unblocked by G0. Awaiting Cowork session 1 — kickoff brief in WORKFLOW.md §6. |
| all others | ⬜ blocked | Per DAG in WORKFLOW.md §3. |

## Sessions

- **Code session 1** (Claude Code, Fable 5) — workflow setup, G0, now T0.2 + T0.3. Started 2026-07-05.
- **Cowork session 1** — T2.5 dossiers. Ready for Tim to launch with the WORKFLOW.md §6 brief.

## New D-items raised since G0

- **D13** (2026-07-05): vendor Naibbe cipher-key CSV vs. consume-only pinned download. Proceeding on pinned download (least-committal) pending Tim. See DECISIONS.md.
- **D14** (2026-07-05): canonical H2 config/plaintexts. Proceeding on both decks + author plaintexts (max comparability) pending Tim. See DECISIONS.md.
