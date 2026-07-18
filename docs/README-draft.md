<!-- DRAFT README for review (do not move to repo root until the Tier-0 work in
RELEASE-READINESS.md is done and the public API exists). Name/license are placeholders
pending decisions D-a/D-b. -->

# MS408 — a cold, reproducible evaluator for Voynich-Manuscript hypotheses

**What this is.** A firewall-disciplined toolkit and methodology for the computational study
of the Voynich Manuscript (Beinecke MS 408) and other undeciphered corpora. It does **not**
propose a solution. It provides a *rigorous, reproducible way to evaluate* a hypothesis —
"is this a cipher of Latin?", "does my generator reproduce the manuscript?", "does this
transliteration change the statistics?" — and to grade the answer honestly.

Think of it as a **cold logical evaluator**: point it at your hypothesis and it tells you,
against firewall-computed reference bands and matched controls, which of the manuscript's
statistical properties you actually reproduce — and which you only appear to. It is built to
be unimpressed, including by its own authors: the project's public record includes the tool
**retracting its authors' own headline result** when the evidence turned.

**What this is not.** Not a decipherment, not a translation, not a claim to have solved the
manuscript. No output should be read as meaning. The statistical evaluator is cold and
reproducible; the accompanying *adversarial-review protocol* uses a fallible language model and
is a discipline, not an oracle (see `LIMITS.md`).

## Why it exists

Computational Voynich work has a long record of confident, mutually incompatible "solutions,"
because with no ground truth "it looks like X" is nearly unfalsifiable. This project inverts the
order: **validate first, claim second.** Three coupled disciplines:

- **Harness** — every method must separate known positives (real language) from matched
  structured-meaningless controls (auto-copying, grille, null generators) and ciphers *before*
  it is trusted on the manuscript.
- **Firewall** — every reported number comes from deterministic, versioned code writing
  machine-readable results; nothing is estimated or recalled.
- **Adversarial refutation** — every A/B-grade claim is attacked by an independent
  clean-context reviewer before it stands; the briefs are archived (`docs/refutations/`).

## Quickstart (evaluate your own hypothesis)

```bash
pip install ms408                 # or: pip install -e .
python -m ms408.acquire           # fetch pinned, checksummed reference data (consume-only)
python -m ms408.evaluate my_tokens.txt      # my_tokens.txt = whitespace-separated word tokens
```

```python
from ms408 import evaluate
verdict = evaluate(open("my_cipher_output.txt").read().split())
for axis, r in verdict["axes"].items():
    print(axis, r["value"], "in VMS band" if r["in_band"] else "OUT", r.get("notes", ""))
print(verdict["n_axes_in_band"], "of", len(verdict["axes"]), "axes match the manuscript")
```

`evaluate()` returns each axis (character entropy, word-order information ΔI, edit-distance-1
morphology, Zipf slope, type-token ratio, and the mid-level syntax z-scores) with its value,
the manuscript's reference band, and whether you land in it — **with the honest caveats
attached to each verdict** (soft axes, the homophony-confounded ΔI, single-manuscript CIs) so
the numbers cannot be quoted without their hedges.

## What's in the box

- `ms408.signature` — the discriminator battery (`evaluate`, `joint_signature`, `vms_bands`).
- `ms408.harness` — matched controls: real-language corpora, self-citation and Naibbe-style
  cipher generators, positional/reuse/type-lexicon generators.
- `ms408.acquire` / `ms408.sources` — pinned, sha256-verified, license-aware data acquisition.
- `ms408/experiments/` — the 37 firewall studies behind the papers (reproductions, not the API).
- `docs/` — `METHODOLOGY.md` (the refutation protocol), `LIMITS.md`, the graded synthesis
  (`FLAGSHIP`, `TIMELINE`), `refutations/` (the archived adversary briefs), and the preprints.

## The honest record (a feature, not an embarrassment)

`docs/refutations/` and the papers document the discipline overturning the program's own
conclusions — a circular positive, a fitted-to-target "sufficiency" claim, an over-strong
negative later walked back, and, most tellingly, a **cipher-exclusion headline retracted after
running a concurrently-published cipher (Greshko's Naibbe, 2025) through this very toolkit**.
If you use it to test *your* hypothesis, expect it to be equally cold with you.

## Limits (read before quoting any number)

See `LIMITS.md`. In brief: the evidence is a single manuscript; two mid-level syntax measures
are "soft" (their manuscript-side confidence interval crosses zero); the word-order statistic ΔI
is confounded by homophony and word-spacing; and the adversarial-review protocol uses a
same-model-family LLM, so cross-vendor or human refutation is the stronger check.

## Cite / license

License: `<Apache-2.0 — pending>`. If you use the pinned Naibbe example data, cite Greshko 2025
(doi:10.1080/01611194.2025.2566408) per its source licence. Companion preprints: the constraint-
envelope paper (`paper/v6b/`) and the methods paper on adversarial self-correction
(`paper/methods/v3/`).
