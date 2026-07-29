# ms408 v0.1.0

Draft notes for the first GitHub Release. Cut a release tagged **`v0.1.0`** and paste this in;
that release (a) triggers the PyPI publish workflow (once Trusted Publishing is set up) and
(b) is what Zenodo archives to mint the DOI (once the Zenodo↔repo toggle is on).

---

**MS408 is a cold, reproducible evaluator and benchmark for hypotheses about the Voynich
Manuscript (Beinecke MS 408).** It does not propose a solution. It gives the research community a
shared, honest way to test an idea — *"is this a cipher of Latin?", "does my generator reproduce
the manuscript?"* — and to see, reproducibly, exactly where the evidence stands. Matching the
manuscript is **necessary, not sufficient**: an in-band result means a hypothesis is *not
excluded*, never that it is the mechanism.

## Highlights

- **`ms408.evaluate(tokens)`** + the `python -m ms408` CLI — score any word-token stream against
  the manuscript's discriminator bands and get a per-axis verdict **with each axis's caveat
  attached** (the confounded ΔI, the token-sensitive TTR, the soft mid-level syntax axes are
  flagged and not counted, so the tool can't be quoted without its hedges).
- **`python -m ms408.verify`** — reproduce the shipped reference numbers from committed code;
  `--full` rebuilds the bands.
- **A matched-control harness** (real language, cipher, and null/meaningless generators) and a
  committed, firewall-built reference-band artifact.
- **The honest record as a feature** — the archived clean-context refutation briefs document the
  discipline overturning the program's *own* conclusions, including a cipher-exclusion headline
  retracted after running a concurrently-published cipher (Greshko's Naibbe, 2025) through this
  very toolkit.
- **No decipherment, translation, or meaning claim.** Ever.

## Install

```bash
pip install ms408
python -m ms408.acquire          # pinned, checksummed reference data (consume-only)
python -m ms408 my_tokens.txt    # ≥1000 word tokens; prints a per-axis verdict
```

Core install needs only numpy / pandas / requests and makes no network calls on import. The
optional `[vision]` extra powers the annotation track.

## Read more

- Docs, tutorial, and the honest-limits page: **https://ms408.direlabs.com**
- Methodology (harness + firewall + adversarial refutation): `docs/METHODOLOGY.md`
- Preprints: the constraint-envelope paper (`paper/v7`) and the methods paper on adversarial
  self-correction (`paper/methods/v3`).

## Notes

- Requires Python 3.11–3.13.
- Evidence-graded (A–D) throughout; every reported number is produced by deterministic, versioned
  code (the firewall). See `docs/LIMITS.md` before quoting any number.
- License: Apache-2.0.
