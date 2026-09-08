# Changelog

All notable changes to the `ms408` package. This is the software changelog; the preprint
changelog is `paper/CHANGELOG.md`. Format loosely follows [Keep a Changelog]; versions follow
[SemVer]. Dates are ISO-8601.

## [Unreleased]

## [0.2.0] — 2026-08-26

Everything in this release came out of an independent, AI-assisted external review of the
v0.1.0 release, plus the defects found while acting on it. Decisions are recorded in
`docs/planning/i01/DECISIONS.md` (L38–L40, D24–D27) and the consequences in `docs/LIMITS.md`.

**Upgrading:** `evaluate()`'s return shape changed and the hard-axis denominator dropped from
3 to 2. Code reading `verdict["hard_axes_in_band"]` or `verdict["axes"]` must move to
`verdict["dialects"][d][...]`; see *Changed — BREAKING* below.

### Changed — BREAKING (evaluator)

- **Reference bands are now stratified by Currier dialect (D21 → L38).** There is no
  pooled band set: `reference_bands.json` carries one block per dialect (`schema: 2`) and
  `evaluate()` returns `verdict["dialects"]["A" | "B"]` plus `verdict["best_match"]`,
  instead of a single top-level `axes` / `hard_axes_in_band`. `vms_bands(dialect)` returns
  one dialect's block; `evaluate(tokens, dialect=…)` scopes a verdict.
  *Why:* the previous single band set was built from `A + B` truncated at the 10,000-token
  budget — and Currier A alone supplies 10,709 tokens, so it contained **zero** Currier B
  while being labelled "Currier A+B". Currier B, 68% of the manuscript, scored 0–1 of 3
  hard axes against "the manuscript's" own bands. Currier A's bands and point are
  byte-identical to v0.1.0; Currier B is new.
- **`zipf` is demoted from a hard axis to advisory (D23 → L39).** It is now unbanded,
  flagged `token_sensitive`, and excluded from the tally — so **the hard-axis count is out
  of 2 (`h2`, `ed1`), not 3**. *Why:* per-dialect bands revealed that its 75%-subsample CI
  is biased off the full-sample point (Currier B's own zipf point fell outside B's own
  band). The fixed [10, 1000] rank window runs into the count-saturated tail at 7,500
  tokens; A's bias was small enough to hide, B's was not. Same defect class as `ttr`, and
  the same existing policy is applied.

### Fixed

- **`python -m ms408.acquire` failed on a clean `pip install`** — the second command in the
  README quickstart. `RAW_ROOT` assumed a repo checkout, so from a wheel it resolved outside
  the package and, on system- or homebrew-managed installs, somewhere unwritable
  (`PermissionError`). Adds `sources.data_home()` with an explicit resolution order:
  `$MS408_DATA_HOME`, then the repo's `data/` when running from a checkout (layout
  unchanged), then `$XDG_DATA_HOME/ms408` (default `~/.local/share/ms408`).
  `dataset.PROCESSED_ROOT` routes through the same helper.
- **Degenerate token streams crashed `evaluate()`** with
  `TypeError: type NoneType doesn't define __round__` — on one word repeated and on two
  words alternating, the two most obvious inputs a newcomer tries. `zipf_slope()` documents
  a `None` return below `min_rank + 10` types, but two call sites rounded it unguarded.
  Both inputs now return a normal verdict with `zipf: None` and the caveats attached.
- `tests/test_signature.py::test_real_latin_is_excluded` failed on a clean checkout: it was
  guarded on the ZL transliteration but reads an H4 corpus that `ms408.acquire` cannot
  fetch. Now guarded on the corpus it actually needs, so it skips honestly.

### Added

- **The per-experiment results tier now ships (D22 → L40).** `.gitignore` keeps its blanket
  exclusion and allow-lists individual files that `scripts/audit_results_tier.py` clears as
  metrics-only; `tests/test_results_tier.py` re-runs that audit in CI, so a regenerated file
  that starts embedding third-party text fails the build. Reports citing a missing
  `results/` path fall from 19 of 28 to 12 of 28.
- `scripts/audit_results_tier.py` — L19 guard that detects both embedded running corpus text
  and redistributed *vocabulary slices* (a JSON keyed by VMS word type is still a slice of
  someone else's transliteration). Mutation-tested so it cannot pass vacuously.
- `ms408.experiments.e34_band_dialect_scope` — per-dialect band coverage diagnostic: slides
  matched-budget windows across each dialect and scores them against that dialect's own
  bands and the other's. Records that **Currier B's bands generalise poorly within B**
  (`ed1` in band for 2 of 14 windows) — see `docs/LIMITS.md`.
- `$MS408_DATA_HOME` to override where acquired and derived data land.
- Advisory axes carry their measured `subsample_bias` in the artifact, so the D23 demotion
  is auditable rather than asserted.
- `ms408.verify` checks every dialect and reports cross-dialect separation as `INFO` rows.

### Documentation

- **`h2` names its convention everywhere it is reported.** The codebase computes h2 two ways
  and called both "h2": `textstats.char_conditional_entropy` (within-word) and
  `textstats.lb_entropies` (Lindemann–Bowern, space-inclusive, bigrams crossing word
  boundaries — the convention the evaluator bands). They differ materially: 2.1247 vs 2.1643
  on ZL EVA, all pages. Two live errors fixed — `benchmark.py` described its own method as
  "within-word … (Lindemann-Bowern style)", and `GLOSSARY.md` quoted a within-word figure
  while attributing it to `lb_entropies`. Slice is stated alongside convention throughout.
- **The Zipf rank window is stated** wherever the slope is reported: least squares over ranks
  [10, 1000], or to the last type if fewer, `None` below 20 types. It is not scale-free.
- `docs/LIMITS.md` gains a dialect-scope section, per-dialect coverage numbers, and a note
  that the "soft axes" property holds in Currier A but not uniformly in B (ungraded, pending
  adversarial review — D25).

### Known limitations

- **25 of 36 offline experiments cannot be regenerated from a clean checkout (D27):** 22 need
  the H4 corpora, which `ms408.acquire` cannot fetch because those sources are unregistered,
  and 3 need a gitignored annotation JSONL. This caps what D22 could ship to 11 files and is
  why the harness's own "real language must fail the hard axes" claim is not yet externally
  checkable.
- Currier B's bands are built from B's first 10,000 tokens in page order — 44% of B — and
  generalise poorly to the rest of B (D24). Read a B verdict as calibrated against early B.

## [0.1.0] — 2026-08-04

### Added
- Public evaluator: `ms408.evaluate(tokens)` + `axis_values`, `vms_bands`, `format_verdict`,
  and the CLI `python -m ms408` (and console script `ms408`). Verdicts carry each axis's
  caveat, and separate hard / soft / confounded / advisory axes.
- `ms408.verify` — reproduce-our-numbers self-check (`--full` rebuilds the reference bands).
- Committed reference-band artifact `ms408/data/reference_bands.json` (built by
  `e32_reference_bands`), shipped in the wheel.
- Worked example `examples/evaluate_naibbe.py`; docs: `TUTORIAL`, `METHODOLOGY`, `LIMITS`,
  `GLOSSARY`; `CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, `CITATION.cff`; CI + issue/PR
  templates.

### Changed
- `anthropic` moved to the optional `[vision]` extra — the core evaluator installs with only
  numpy/pandas/requests and makes no network calls on import.

### Fixed
- `evaluate()` / the CLI now refuse inputs below `MIN_TOKENS` (1000) with a clear error and
  warn below the reference budget (8000), instead of crashing with an internal traceback on
  short streams; `mz.peak()` guards an empty scan.

[Keep a Changelog]: https://keepachangelog.com/en/1.1.0/
[SemVer]: https://semver.org/spec/v2.0.0.html
[Unreleased]: https://github.com/DireLabs/ms408/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/DireLabs/ms408/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/DireLabs/ms408/releases/tag/v0.1.0
