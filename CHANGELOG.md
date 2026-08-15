# Changelog

All notable changes to the `ms408` package. This is the software changelog; the preprint
changelog is `paper/CHANGELOG.md`. Format loosely follows [Keep a Changelog]; versions follow
[SemVer]. Dates are ISO-8601.

## [Unreleased]

### Changed — BREAKING (evaluator)

Both of these change numbers the tool reports. They came out of an external review of the
v0.1.0 release; see `docs/planning/i01/DECISIONS.md` L38/L39 and `docs/LIMITS.md`.

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

### Added
- `ms408.experiments.e34_band_dialect_scope` — per-dialect band coverage diagnostic:
  slides matched-budget windows across each dialect and scores them against that dialect's
  own bands and the other's. Records that **Currier B's bands generalise poorly within B**
  (`ed1` in band for 2 of 14 windows) — see `docs/LIMITS.md`.
- Advisory axes now carry their measured `subsample_bias` in the artifact, so the D23
  demotion is auditable rather than asserted.
- `ms408.verify` reports cross-dialect separation as `INFO` rows.
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
