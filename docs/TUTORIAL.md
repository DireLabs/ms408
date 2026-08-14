# Tutorial — evaluate a hypothesis about the Voynich Manuscript

This walks through the whole loop: install, point the evaluator at a token stream, read the
verdict *honestly*, and reproduce the numbers. It assumes nothing beyond Python 3.11+.

The one idea to hold onto: **matching the manuscript is necessary, not sufficient.** The tool
tells you whether your hypothesis is *not excluded* — never that it is the answer. Half of
learning to use it is learning which axes are informative and which are traps.

## 1. Install and fetch reference data

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .                 # core evaluator: numpy / pandas / requests only
python -m ms408.acquire          # pinned, sha256-checked reference data (consume-only, L19)
```

The reference bands themselves ship inside the package, so `evaluate()` works immediately;
`acquire` is needed for the worked example, the data-gated tests, and `verify`.

## 2. Evaluate a token stream

Your input is a list of whitespace-separated word tokens — a cipher's output, a generator's
output, a transliteration variant, a candidate plaintext rendering. From the shell:

```bash
python -m ms408 my_tokens.txt          # pretty table
python -m ms408 --json my_tokens.txt   # machine-readable verdict
cat my_tokens.txt | python -m ms408 -  # from stdin
```

Or in Python:

```python
from ms408 import evaluate

verdict = evaluate(open("my_tokens.txt").read().split())

# The bands are stratified by Currier dialect: you get one block per dialect.
for dialect, block in verdict["dialects"].items():
    print(f"Currier {dialect}: {block['hard_axes_in_band']} of "
          f"{block['hard_axes_total']} hard axes match")
    for axis, r in block["axes"].items():
        print(f"  {axis:12} value={r['value']!s:>9}  band={r['band']}  in={r['in_band']}")
        # r["caveat"] carries the honest hedge; r["soft"] / r["confounded"] /
        # r["token_sensitive"] say how much weight the axis can bear

print(verdict["best_match"])            # e.g. {"dialect": "A", ...}
verdict_b = evaluate(tokens, dialect="B")   # or scope to one dialect
```

> **Say which dialect.** Currier A and B are different generative regimes — each sits
> outside the other's hard bands on every axis, and B is 68% of the manuscript. "Matches
> the Voynich manuscript" is not a claim this tool can produce; "matches Currier A at 2/2
> hard axes" is.

> **Match the token budget.** The bands are built at ~10,000 tokens. `h2` and `ed1` are
> fairly budget-robust, but `ttr` and `zipf` are token-count-sensitive — which is why
> neither is banded or counted (D23) — so compare at a similar budget. See how `examples/evaluate_naibbe.py` takes a matched block sample.

## 3. Read the verdict honestly

The verdict groups axes by how much weight they can bear:

| kind | axes | how to read an in-band result |
|---|---|---|
| **hard** | `h2`, `ed1` | Real evidence. These are counted in `hard_axes_in_band`. |
| **confounded** | `dI`, `*_global` | Weak. `dI` collapses under homophony/respacing (E29) — an in-band `dI` is *not* "intact word order". Not counted. |
| **soft** | `fc_z_local`, `wc_z_local`, ... | Weak. Currier A's own CI for these crosses zero (in B, three of the four do not). Reported, not counted. |
| **advisory** | `ttr`, `zipf` | Token-count-sensitive; no band, not counted. |

Two verdicts that look similar but aren't:

- **All hard axes in band.** Your hypothesis reproduces the manuscript's load-bearing
  statistics. That is the *strongest* the tool can say — and it is still only "not excluded".
  It does **not** identify a mechanism (many different processes can share a statistical
  envelope). Treat it as a licence to investigate further, not a result.
- **Zero hard axes in band.** Usually your hypothesis is genuinely off. But check *which*
  axes failed and whether any were confounded before you conclude "excluded" — see §4.

## 4. The cautionary tale: a real cipher scoring zero

Run the worked example (needs the Naibbe data from `acquire`):

```bash
python examples/evaluate_naibbe.py
```

Greshko's Naibbe cipher (2025) — a genuine, decipherable verbose-homophonic cipher — scores
**0 hard axes, against both dialects**. The naive read is "0 → the manuscript isn't this
cipher". That read is wrong,
and it is exactly the mistake the tool is built to prevent:

- The `dI` axis has collapsed to ~0, but `dI` is **confounded**: most of the collapse is
  Greshko's *respacing* of the plaintext, applied before enciphering. Word-boundary Latin
  `dI` (0.076) sits inside the manuscript's band. An out-of-band `dI` here is an artifact.
- On the deconfounded mid-level syntax axes — the load-bearing ones — verbose+homophonic
  ciphers are **not** robustly separable from the manuscript (E30/E31). So this cipher family
  is *inconclusive*, not excluded.
- The `ed1` mismatch reflects *this* cipher's homophone tables, not a law every
  verbose-homophonic cipher must obey.

The lesson: a raw count is not a conclusion. You have to know which axes are informative for
the mechanism you're testing. This is why the tool separates hard from confounded/soft and
prints "necessary, not sufficient" on every verdict. Full analysis:
[`LIMITS.md`](LIMITS.md), `reports/e29_naibbe_discriminators.md`.

## 5. Reproduce the numbers

Everything the tool reports is reproducible from committed code:

```bash
python -m ms408.verify          # recompute the VMS point signature; check self-consistency
python -m ms408.verify --full   # also rebuild the reference bands and diff (bit-for-bit)
```

If you change an axis definition, rebuild the bands and re-pin the tests:

```bash
python -m ms408.experiments.e32_reference_bands   # rewrites src/ms408/data/reference_bands.json
# then update tests/test_verify.py::PINNED_* and confirm `ms408.verify --full` passes
```

## Where to go next

- [`METHODOLOGY.md`](METHODOLOGY.md) — the harness / firewall / grading / refutation
  discipline, and how to run the adversarial-review protocol on your own claim.
- [`LIMITS.md`](LIMITS.md) — the per-axis caveats in full.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — the rules for adding a discriminator or source.
