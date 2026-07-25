# Release-readiness assessment — MS408 as an open-source evaluator + methodology

> **Historical internal memo (kept for provenance).** This is the assessment that motivated
> the release; the Tier-0/1/2 work below is now done. The `evaluate()` API sketch in §4 is
> illustrative and predates the implementation — for the real verdict shape see
> [`TUTORIAL.md`](TUTORIAL.md), the `ms408.signature` docstrings, and [`GLOSSARY.md`](GLOSSARY.md).
> The live pre-publication checklist is [`../OSS_RELEASE.md`](../OSS_RELEASE.md).

_Grounded inventory of what is reusable vs. research-scaffolding, the gap between "our
research pipeline" and "a tool a stranger can run," a proposed public entry point, and a
tiered work plan. Written 2026-07-17. No timelines (sequencing/scope only)._

## TL;DR verdict

**Closer to releasable than expected.** The bones are strong: a proper installable package
(`pyproject.toml`, `src/ms408`, hatchling), **no hardcoded absolute paths**, a **pinned +
sha256-checksummed, license-aware data-acquisition registry** (`sources.py` / `python -m
ms408.acquire`) that already respects the consume-only data policy (L19), an existing (partial)
test suite, and 53 firewall result files. The real gap is not the science or the data
plumbing — it is **(a) a public API** (the discriminators are private underscore-functions
scattered across experiment scripts) and **(b) honest packaging** (README/LICENSE, and framing
the refutation loop as a *protocol*, since it is not in the codebase). This is a focused
packaging effort, not a rewrite.

## 1. Inventory: three layers

### (A) The reusable core — this is "the tool"
Cold, deterministic, no LLM required. Currently scattered; needs consolidation into a public API.
| capability | lives in | notes |
|---|---|---|
| character stats: `lb_entropies` (h1/h2), `zipf_slope`, word-length | `textstats.py` | clean, public-ish |
| joint `profile()`: h2, ΔI (Montemurro–Zanette), ED1 morphology, Zipf, TTR | `studies/encoding.py` | the workhorse; takes any `list[str]` |
| ED1 morphology network | `studies/morphology.py` | reusable |
| word-order information ΔI | `mz.py` | reusable |
| mid-level syntax `_fc_z`/`_wc_z` (null-corrected) | `experiments/e19_joint_signature.py` | **private, buried in an experiment** |
| deconfounded (within-block-null) syntax + stability | `experiments/e31_harden_syntax.py` | **private, buried** |
| VMS reference bands `_vms_band` (block-bootstrap) | `experiments/e21_positional_generator.py` | **private, recomputed each call — should be a cached artifact** |
| harness generators (self-citation, Naibbe, verbose/abjad/nomenclator ciphers, positional/reuse/type-lexicon generators) | `harness/`, `experiments/e6`, `e21–e26` | the "matched controls" — reusable but spread out |
| data acquisition (pinned URLs + sha256 + licensing) | `sources.py`, `acquire.py` | **release-grade already** |

### (B) Research scaffolding — the experiments (E1–E31)
The 37 `experiments/e*.py` are **one-off studies**, not library code: each has a `run()` that
writes a specific `results/*.json`, hardcodes its own grid/seeds, and several **mutate module
globals** (e.g. `e30`/`e31` set `e21.SLOT_SIZES` etc.). These are the *worked record*, not the
product. They should ship as-is (reproducible, firewall-stamped) but be clearly labelled
"reproductions of the paper's studies," not "the API."

### (C) Out-of-band methodology — the refutation loop
**Important and easy to misrepresent:** the clean-context adversarial refutation pass is **not
in the codebase.** `grep` for `refut` hits only docstrings/verdicts; the only `anthropic`
usage is the *vision-annotation* pipeline (`annotate/`, `e10`/`e12`/`e4b`), not a refuter. The
refutation was run out-of-band (fresh-context agents) and survives only as the **archived
briefs in `docs/refutations/` (7 of them)**. So the refutation loop must be released as a
**documented protocol + worked examples**, NOT implied to be a runnable feature. This is the
single most important honesty point for the release (and consistent with the whole project's
ethos).

## 2. What is already release-grade (strengths)
- Installable package; `requires-python >=3.11`; pinned deps; ruff + pytest configured.
- **No absolute paths** anywhere in `src/`.
- **L19-clean data policy**: `data/raw/`, `data/processed/*`, and `results/experiments/*.json`
  are gitignored; nothing third-party is committed. `sources.py` pins every external file by
  URL + sha256 with per-source licensing notes (e.g. Naibbe → "must cite Greshko 2025").
- A **reproducible data-acquisition CLI** (`python -m ms408.acquire [--verify]`).
- An existing test suite (`tests/test_encoding.py`, `test_e1`–`e4`, `test_dataset`, …) — though
  coverage stops well before the newer discriminators/generators.
- 53 firewall result files + the full graded synthesis (`FLAGSHIP`, `TIMELINE`, `FRAMEWORKS`).

## 3. The gap to "a stranger can run it"

**Blocking (must, for any release):**
1. **No public API.** The value proposition — "run *your* hypothesis, get a graded verdict" —
   has no entry point. The needed functions are private (`_fc_z`, `_wc_z`, `_vms_band`) and
   inside experiment scripts. → consolidate into one public module (§4).
2. **No README / LICENSE / CONTRIBUTING.** No license = legally unusable. README is the whole
   pitch.
3. **The refutation loop must be documented as a protocol, not shipped as code** (§1C).
4. **The VMS reference bands** must become a cached, versioned artifact (they are currently
   recomputed by a private experiment function via block-bootstrap on every call).

**Should (for a credible tool):**
5. Test the newer discriminators (fc_z/wc_z, deconfounding, ΔI) and pin their expected values —
   right now nothing guards the numbers the tool would report.
6. Make `anthropic` an **optional** dependency (it is only needed for the vision-annotation
   track, not for the discriminator tool).
7. A `--verify`-only path so a user can reproduce the paper's numbers from committed code +
   acquired data, and confirm the firewall.
8. A short "honest limits" doc: the statistical discriminators are cold/reproducible; the
   refutation protocol uses a fallible, same-model-family LLM (a review protocol, not an oracle);
   the mid-level syntax measures have a manuscript-side CI that crosses zero; the VMS is n=1.

**Nice:**
9. Rename decision: `ms408` is opaque for a public tool (see Decisions).
10. A worked "evaluate a cipher" notebook/example using the pinned Naibbe data (cite Greshko).
11. CI (run tests + ruff on push).

## 4. Proposed public entry point — "evaluate your own hypothesis"

Consolidate the scattered core into one public module, e.g. `ms408/signature.py` + a thin CLI.
Sketch (design, not yet implemented):

```python
from ms408 import evaluate

# `tokens` is any list[str] of word tokens — your cipher output, generator output,
# a transliteration variant, a candidate plaintext rendering, ...
verdict = evaluate(tokens)
# ->
# {
#   "axes": {
#     "h2":  {"value": 2.08, "vms_band": [2.11, 2.20], "in_band": False},
#     "dI":  {"value": 0.16, "vms_band": [0.07, 0.21], "in_band": True},
#     "ed1": {...}, "zipf": {...}, "ttr": {...},
#     "fc_z":{"value": ..., "vms_band": [...], "in_band": ..., "soft": True},
#     "wc_z":{..., "soft": True, "deconfounded": ...},
#   },
#   "n_axes_in_band": 3,
#   "controls": {"real_latin": {...}, "self_citation": {...}, "naibbe": {...}},  # matched
#   "notes": ["fc_z/wc_z are soft (2-point ranges; VMS CI crosses zero) — see LIMITS.md",
#             "ΔI is homophony-confounded — see the E29 caveat"],
# }
```

CLI: `python -m ms408.evaluate mytokens.txt` → the same verdict as a table. The `evaluate`
function is a thin wrapper over the *existing, tested* `profile()` + the promoted `fc_z`/`wc_z`
+ the cached `vms_bands()`; the honest caveats travel *with* every verdict (so the tool cannot
be quoted without its own hedges — the anti-over-claim discipline, encoded).

This is the highest-leverage single deliverable: it turns a pile of experiments into a tool.

## 5. Data & licensing (L19)
- **Ship no third-party data.** Users run `python -m ms408.acquire` to fetch pinned sources
  into gitignored `data/raw/`. The registry already carries per-source licensing (ZL
  transliteration, Naibbe → cite Greshko, etc.).
- **Pick a code LICENSE** (MIT or Apache-2.0 recommended; Apache-2.0 adds a patent grant and is
  friendlier for a "tool"). The Naibbe optional example inherits Greshko's modified-MIT
  cite-requirement, which `sources.py` already records.

## 6. The refutation loop, released honestly
Ship: (a) `docs/refutations/` (the 7 briefs) as worked examples; (b) a `METHODOLOGY.md`
describing the protocol — harness → firewall → graded claim → standing clean-context
adversarial pass — and how to run it (spawn a fresh-context reviewer, give it the claim+code,
require it to attack, preserve the brief); (c) the explicit caveat that it is a *protocol using
a fallible LLM*, strongest cross-vendor/human, not a packaged oracle. The self-correction
record (papers §7, TIMELINE) is the demonstration.

## 7. Tiered work plan (sequence, not schedule)
- **Tier 0 (releasable v0.1 — the minimum honest release):** LICENSE; README (draft below);
  promote `fc_z`/`wc_z`/`vms_bands` into a public `signature.py`; the `evaluate()` entry point +
  CLI with caveats attached; cache the VMS bands as a committed artifact; `METHODOLOGY.md` +
  point to `docs/refutations/`; `LIMITS.md`.
- **Tier 1 (credible tool) — DONE (2026-07-22):** ✅ value-pinning tests
  (`test_verify.py::test_shipped_bands_are_pinned`, data-free, freezes the exact reported
  numbers) + reproducibility/example guards; ✅ `anthropic` optional (`vision` extra, done
  in Tier 0); ✅ worked "evaluate the Naibbe cipher" example (`examples/evaluate_naibbe.py`);
  ✅ reproduce-our-numbers path (`python -m ms408.verify [--full]`, rebuilds the bands and
  diffs vs the shipped artifact — bit-for-bit). Pulled forward from Tier 2: ✅ minimal CI
  (`.github/workflows/ci.yml`, ruff + pytest on 3.11/3.12) so the pinning tests actually
  guard on push. Note: `--verify` reproduces the EVALUATOR's own bands; full paper-number
  reproduction remains per-experiment (each `e*` writes its own `results/*.json`).
- **Tier 2 (community-facing) — mostly DONE (2026-07-22):** rename decided (kept `ms408`);
  ✅ CI hardened (`.github/workflows/ci.yml` — matrix lint+test + wheel-build guard, caching,
  concurrency); ✅ `CONTRIBUTING.md` (the discipline as contribution rules); ✅
  `docs/TUTORIAL.md` (markdown, not a notebook — project ethos). **Remaining (need Tim):**
  (i) register the DOI/arXiv companion (v6b + methods-v3) — a *publishing* action, Tim's call;
  (ii) the block-scale like-for-like ΔI research experiment — the one untested way the ΔI leg
  could still discriminate; this reopens the *research* track (needs a refutation pass +
  grade), not packaging.

## 8. Risks / scope discipline
- **Don't let the tool over-claim** — the same failure mode we spent ten iterations fighting.
  The `evaluate()` verdict must carry its own hedges (soft axes, confounded ΔI, n=1).
- **Don't gold-plate.** Tier 0 is a real, honest release; Tiers 1–2 can follow community
  feedback. Resist building a general framework nobody asked for.
- **The refutation protocol is the interesting part but the least "productizable"** — resist
  implying it is a push-button feature.

## Decisions to surface
- **D-a — Public name.** Keep `ms408` (accurate, opaque) or rename (e.g. an "envelope"/"cold
  reader"/"voynich-evaluator" identity). Naming affects the whole README.
- **D-b — License** (Apache-2.0 recommended).
- **D-c — Scope of v0.1**: discriminator-evaluator only, or evaluator + methodology docs + the
  reproduction scaffolding together.
