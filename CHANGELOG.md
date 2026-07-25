# Changelog

All notable changes to the `ms408` package. This is the software changelog; the preprint
changelog is `paper/CHANGELOG.md`. Format loosely follows [Keep a Changelog]; versions follow
[SemVer]. Dates are ISO-8601.

## [Unreleased]

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
