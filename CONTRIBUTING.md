# Contributing to MS408

The value of this project is its **discipline**, not any single finding. Contributions are
welcome, but they have to keep the discipline intact — that is what makes the tool worth
trusting. Please read this before opening a PR.

## The non-negotiables

These are binding (see [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and `CLAUDE.md`):

1. **Firewall — numbers come only from code.** Every reported number must be produced by
   deterministic, versioned code writing a machine-readable result. Never hand-enter,
   estimate, or recall a metric. If a number isn't produced by a script, write the script.
   The evaluator obeys this too: `evaluate()` refuses if its band artifact is missing rather
   than fabricate one, and `python -m ms408.verify --full` proves the shipped numbers
   rebuild from code.
2. **Harness first.** A new discriminator or measure must separate real language from matched
   structured-meaningless controls (and ciphers) on synthetic data *before* it is applied to
   the manuscript. Add it to `ms408.harness` / the experiments with that separation shown.
3. **Evidence grading.** Every claim carries a grade A–D. Don't raise a grade to make a
   result look stronger. Ungraded assertions are treated as D.
4. **No decipherment / no meaning claims (L7).** This project reports statistics, never
   plaintext, meaning, or symbol values. Matching the manuscript's bands is *necessary, not
   sufficient*. PRs that claim to "read" or "solve" the manuscript will be declined.
5. **Adversarial refutation for A/B claims.** Any strong claim should survive an independent
   clean-context skeptic before it stands; preserve the brief in `docs/refutations/`. See the
   protocol in `docs/METHODOLOGY.md`.
6. **Consume-only external data (L19).** Never commit third-party corpora. Add new sources to
   `ms408.sources` pinned by URL + sha256 with a licensing note; users fetch them with
   `ms408.acquire` into gitignored `data/raw/`.
7. **Stratify text analyses** by Currier A/B dialect and scribal hand where applicable.

## Dev setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python -m ms408.acquire        # fetch pinned reference data (needed for data-gated tests)
ruff check src tests examples
pytest -q
```

CI (`.github/workflows/ci.yml`) runs ruff + pytest on 3.11/3.12 and a wheel-build guard.
Data-gated tests skip when the corpus isn't present; the value-pinning test runs data-free.

## Where code goes

- **Public API** (`src/ms408/signature.py`) — the stable surface a stranger calls
  (`evaluate`, `axis_values`, `vms_bands`). Keep it thin and caveat-carrying. `axis_values`
  is the *single* canonical axis computation; the band builder and `evaluate()` both call it,
  so a user's value and its band never drift. If you change an axis, rebuild the bands
  (`python -m ms408.experiments.e32_reference_bands`) and re-pin the tests.
- **Experiments** (`src/ms408/experiments/e*.py`) — one-off firewall studies. Each has a
  `run()` that writes `results/*.json` with its git commit + params. These are the *record*,
  not the API; some mutate module globals — don't import them into the public surface.
- **Reference bands** are a committed artifact (`src/ms408/data/reference_bands.json`) built
  by `e32`. If you rebuild them: update `tests/test_verify.py::PINNED_*` and confirm
  `python -m ms408.verify --full` passes.

## Determinism

Fixed seeds, pinned dependencies, no wall-clock or randomness in reported computations. A
result that isn't reproducible from committed code + acquired data is a bug.

## Pull requests

- Keep changes focused; match the surrounding code's style (ruff, line length 100).
- Add/adjust tests. If you touch the reported numbers, update the pinned values and say so.
- State the evidence grade of any empirical claim in the PR description.
- Be honest about limitations — an accurately-scoped negative is more valuable here than an
  overstated positive.
