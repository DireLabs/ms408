# MS408 — a cold, reproducible evaluator for Voynich-Manuscript hypotheses

[![CI](https://github.com/DireLabs/ms408/actions/workflows/ci.yml/badge.svg)](https://github.com/DireLabs/ms408/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/ms408.svg)](https://pypi.org/project/ms408/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.11%E2%80%933.13-blue)
<!-- DOI badge: after enabling Zenodo + cutting the first Release, paste the concept-DOI badge here, e.g.
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX) -->
[![site](https://img.shields.io/badge/site-ms408.direlabs.com-6b4e2e)](https://ms408.direlabs.com)

> **New here? Pick your path.**
> - **You study the Voynich Manuscript** (and want to test an idea, or understand what's
>   been found): start with the [tutorial](docs/TUTORIAL.md), then [`LIMITS.md`](docs/LIMITS.md)
>   and the [glossary](docs/GLOSSARY.md). You do not need to read the code.
> - **You're a developer / not a Voynich specialist**: the [glossary](docs/GLOSSARY.md)
>   defines the domain terms; then the API in `ms408.signature`, [`CONTRIBUTING.md`](CONTRIBUTING.md),
>   and the reproducibility path (`python -m ms408.verify`).

**What this is.** A firewall-disciplined toolkit and methodology for the computational study
of the Voynich Manuscript (Beinecke MS 408) and other undeciphered corpora. It does **not**
propose a solution. It gives you a *rigorous, reproducible way to evaluate* a hypothesis —
"is this a cipher of Latin?", "does my generator reproduce the manuscript?", "does this
transliteration change the statistics?" — and to grade the answer honestly.

Think of it as a **cold logical evaluator**: point it at your hypothesis and it reports,
against firewall-computed reference bands, which of the manuscript's statistical properties
you actually reproduce — and which you only appear to. It is built to be unimpressed,
including by its own authors: the project's public record includes the toolkit **retracting
its authors' own headline result** after a concurrently-published cipher was run through it.

**What this is not.** Not a decipherment, not a translation, not a claim to have solved the
manuscript. No output should be read as meaning. Matching the bands is *necessary, not
sufficient*: it means a hypothesis is not excluded, never that it is the mechanism. The
statistical evaluator is cold and reproducible; the accompanying *adversarial-review
protocol* uses a fallible language model and is a discipline, not an oracle
([`docs/LIMITS.md`](docs/LIMITS.md), [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)).

## Why it exists

Computational Voynich work has a long record of confident, mutually incompatible
"solutions," because with no ground truth "it looks like X" is nearly unfalsifiable. This
project inverts the order: **validate first, claim second.** Four coupled disciplines
(detailed in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)):

- **Harness** — every method must separate real language from matched
  structured-meaningless controls and ciphers *before* it is trusted on the manuscript.
- **Firewall** — every number comes from deterministic, versioned code; nothing is
  estimated or recalled (this applies to the tool too: `evaluate()` refuses to run if its
  reference-band artifact is missing rather than invent a band).
- **Evidence grading** — every claim carries a grade A–D and never gets upgraded to look
  stronger.
- **Adversarial refutation** — every A/B claim is attacked by an independent clean-context
  reviewer before it stands; the briefs are archived ([`docs/refutations/`](docs/refutations/)).

## Install

```bash
pip install -e .                  # core evaluator (numpy / pandas / requests only)
pip install -e ".[vision]"        # + the optional vision-annotation track (anthropic)
pip install -e ".[dev]"           # + pytest / ruff
```

The [tutorial](docs/TUTORIAL.md) walks through the whole loop end to end.

## Quickstart — evaluate your own hypothesis

```bash
python -m ms408 my_tokens.txt          # whitespace-separated word tokens; prints a table
python -m ms408 --json my_tokens.txt   # machine-readable verdict
cat my_tokens.txt | python -m ms408 -  # tokens from stdin
```

> `my_tokens.txt` needs **at least ~1,000 word tokens** (the reference bands are built at
> 10,000; below ~8,000 some axes aren't strictly comparable). Shorter streams are refused
> with a clear error rather than a misleading verdict — see [`docs/LIMITS.md`](docs/LIMITS.md).

```python
from ms408 import evaluate

verdict = evaluate(open("my_cipher_output.txt").read().split())

# Bands are stratified by Currier dialect — there is no pooled "the manuscript" band set.
for dialect, block in verdict["dialects"].items():
    print(f"Currier {dialect}: {block['hard_axes_in_band']} of "
          f"{block['hard_axes_total']} hard axes match")
    for axis, r in block["axes"].items():
        flag = " [soft]" if r["soft"] else (" [confounded]" if r["confounded"] else "")
        print(f"  {axis:12} {r['value']}  band={r['band']}  in={r['in_band']}{flag}")
        # r["caveat"] carries the honest hedge for that axis

print(verdict["best_match"])          # the dialect you matched most closely
# evaluate(tokens, dialect="B") scopes the verdict to one dialect.
```

Each axis reports its value, that dialect's reference band, and whether you land in it —
**with the caveat attached** (the homophony-confounded `dI`, the token-sensitive advisory
`ttr` and `zipf`, the soft mid-level syntax z's). The `hard_axes` count deliberately excludes
the confounded, soft, and advisory axes, so the tool cannot be quoted without its hedges.

**Dialect matters more than anything else here.** Currier A and B are different generative
regimes: each one's own signature sits *outside* the other's hard bands on every axis, and B
is 68% of the manuscript. In-band for one dialect is not in-band for the manuscript — always
say which. See [`docs/LIMITS.md`](docs/LIMITS.md) for how well each dialect's bands cover the
rest of that dialect (B's do so poorly on `ed1`).

Sanity check the discrimination yourself: each dialect lands in all of its own hard bands,
misses the other's, and raw Latin prose (high character entropy, no morphology network)
lands in none of either — `tests/test_signature.py` pins all three.

**Worked example — a real cipher.** [`examples/evaluate_naibbe.py`](examples/evaluate_naibbe.py)
runs Greshko's Naibbe cipher (2025) through the evaluator. It lands 0 hard axes against both
dialects — and
the example explains why that is *not* exclusion (the `dI` collapse is a respacing artifact on
a confounded axis; verbose+homophonic ciphers are inconclusive, not excluded). It is the
sharpest demonstration of the tool's discipline.

**Reproduce the numbers.** The numbers the tool ships are reproducible from committed code:

```bash
python -m ms408.verify          # recompute the VMS point + check self-consistency
python -m ms408.verify --full   # also rebuild the reference bands and diff vs the shipped file
```

## What's in the box

- `ms408.evaluate` / `ms408.signature` — the public evaluator: `evaluate`, `axis_values`,
  `vms_bands`, `format_verdict`, and the CLI (`python -m ms408`).
- `ms408.verify` — reproduce-our-numbers self-check (`python -m ms408.verify [--full]`).
- `examples/` — runnable demos (`evaluate_naibbe.py`).
- `ms408.harness`, `ms408.experiments.e6/e21–e26` — matched controls: real-language corpora,
  self-citation and Naibbe-style cipher generators, positional/reuse/type-lexicon generators.
- `ms408.acquire` / `ms408.sources` — pinned, sha256-verified, license-aware data acquisition.
- `ms408.experiments.e*` — the firewall studies behind the papers (reproductions, not the
  API); `e32_reference_bands` builds the evaluator's committed reference bands.
- `docs/` — [`TUTORIAL.md`](docs/TUTORIAL.md) (end-to-end walkthrough),
  [`METHODOLOGY.md`](docs/METHODOLOGY.md) (the refutation protocol),
  [`LIMITS.md`](docs/LIMITS.md), the graded synthesis (`synthesis/`),
  [`refutations/`](docs/refutations/) (the archived adversary briefs), and the preprints
  (`paper/`). Contributing? See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## The honest record (a feature, not an embarrassment)

[`docs/refutations/`](docs/refutations/) and the papers document the discipline overturning
the program's *own* conclusions — a circular positive, a fitted-to-target "sufficiency"
claim, an over-strong negative later walked back, and, most tellingly, a **cipher-exclusion
headline retracted after running a concurrently-published cipher (Greshko's Naibbe, 2025)
through this very toolkit**. If you use it to test *your* hypothesis, expect it to be
equally cold with you.

## Limits (read before quoting any number)

See [`docs/LIMITS.md`](docs/LIMITS.md). In brief: the evidence is a single manuscript;
`dI` is homophony/respacing-confounded (a homophony detector, not a clean word-order
measure); `ttr` is token-count-sensitive; the two mid-level syntax measures are soft (their
VMS-side confidence interval crosses zero); and the adversarial-review protocol uses a
same-model-family LLM, so cross-vendor or human refutation is the stronger check.

## Data & licensing

The package ships **no third-party corpora**. Run `python -m ms408.acquire` to fetch pinned,
sha256-checksummed sources into gitignored `data/raw/` under a consume-only policy; the
registry (`src/ms408/sources.py`) records each source's licence. If you use the Naibbe
example data, cite Greshko 2025 (doi:10.1080/01611194.2025.2566408) per its source licence.

Acquired and derived data land under the repo's `data/` when you run from a checkout. From a
`pip install` there is no checkout, so they land in `$XDG_DATA_HOME/ms408` (default
`~/.local/share/ms408`). Set `MS408_DATA_HOME` to override either case — useful for CI and
shared caches.

Code is licensed under **Apache-2.0** (see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)).
Companion preprints: the constraint-envelope paper (`paper/v6b/`) and the methods paper on
adversarial self-correction (`paper/methods/v3/`).
