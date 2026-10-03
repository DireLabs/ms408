# D27 — pinning the H4 control corpora into `ms408.sources`: staged work plan

**Status: PREPARATION ONLY. D27 is not decided here.** This document assembles the evidence
so the decision can be made cheaply; it registers no sources, changes no code, and commits no
corpora. The licensing call is Tim's under L19.

## The problem, measured

Running all 36 offline experiments on a clean checkout with `ms408.acquire` fully run
(all 15 pinned checksums verified): **11 succeeded, 25 failed.**

| blocker | experiments |
|---|---|
| H4 corpora absent (`data/processed/h4/*.txt`, `data/raw/h4/**`) | 22 |
| `results/annotations/t13_annotations.jsonl` (gitignored) | 3 |

The H4 sources are not registered in `ms408.sources`, so `acquire` cannot fetch them and
`python -m ms408.h4` has nothing to normalise. Consequences beyond the missing numbers:

- The harness's own claim that **real language must fail the hard axes** is not checkable by
  any external reader — `tests/test_signature.py::test_real_latin_is_excluded` skips.
- `results/harness/benchmark.json` cannot be regenerated, so the stale `entropy_method`
  policy string corrected in `src/ms408/benchmark.py` cannot be refreshed in the artifact.
- D22 could ship only 11 of ~36 experiment result files, because the other 25 could not be
  produced, let alone audited.

## What is already established (evidence, not argument)

### 1. Licensing is documented and looks permissive for *fetching*

From `docs/planning/i01/specs/T03-h4-acquisition.md`:

| family | text | licence as recorded |
|---|---|---|
| Latin | Vulgate, `christos-c/bible-corpus` CES-XML | text PD; packaging repo has no explicit licence — "consume-only OK" |
| Latin | Macer Floridus | (see spec) |
| Italian | Boccaccio, *Decameron* (Branca ed., Liber Liber) | underlying text PD; e-book apparatus CC BY-NC-SA 4.0 |
| German | ReM v2.1 (MHG) | CC BY-SA 4.0 |
| German | ReF v1.0.2 (ENHG) | Zenodo metadata CC BY 4.0; bundled LICENSE CC BY-SA 4.0 |
| Hebrew | Mishneh Torah, "Torat Emet 363" | Public Domain (licence field verified per file) |

Nothing here forbids *fetching*. Redistribution is the constrained act, and pinning does not
redistribute — `data/raw/` stays gitignored.

### 2. There is a locked precedent for exactly this pattern

**L21**: the Naibbe cipher data "stays a consume-only pinned download (`data/raw/`,
sha256-pinned); not vendored into the repo." That is the same posture D27 proposes, already
approved for a source with a *more* restrictive licence than most of H4.

### 3. The sha256 hashes survive in the repo — only the URLs were lost

`docs/planning/i01/specs/T03-h4-acquisition.md` defers per-file URLs and hashes to
`data/raw/h4/MANIFEST.json`, which is gitignored and **absent from this machine**. But
`ms408.h4` also writes each source's hash into the *processed* manifest, and that file **is
committed**. All 11 raw source hashes are therefore recoverable:

| raw file (under `data/raw/h4/`) | sha256 (recovered) |
|---|---|
| `german/ReF-v1.0.2.tar.gz` | `288a478d02de5796d14faa0b669879dc6bf67c47e2d7ee261815e15120b99f0e` |
| `hebrew/mishneh_torah_forbidden_foods_torat_emet.json` | `1f78ee8d3596e3fd1d85dd68b922796be2ce5797ba5e2b7602b94fffeb62c295` |
| `hebrew/mishneh_torah_foreign_worship_and_customs_of_the_nations_torat_emet.json` | `d44062dd9806a383ba2ab19ca6aba1e6ad04db0ec0b1d473a99a3a706a1c1e0f` |
| `hebrew/mishneh_torah_foundations_of_the_torah_torat_emet.json` | `a35c233dfb57fc67186aee6d0cebe4221c2d7be8b791eaa908efb80ab495ce7c` |
| `hebrew/mishneh_torah_human_dispositions_torat_emet.json` | `95080bf20ae830cd76702b8ad0e2b1bbaeb8c460a631f8d5d9b330da8a24bdcd` |
| `hebrew/mishneh_torah_repentance_torat_emet.json` | `1c0a500bc219f1751938a5ad955042cdb5ec35b9a61ded66b054beb78cd2cafe` |
| `hebrew/mishneh_torah_sabbath_torat_emet.json` | `9dd8918f452cfd6fc68ebfc375e55049a95e56e486f091710acfe60c96d0a196` |
| `hebrew/mishneh_torah_torah_study_torat_emet.json` | `08e1e3b3a2219dde6dbe654d4e8faf3019861b169e90a416bbfd14e00cbcb50b` |
| `italian/boccaccio_decameron_branca.txt` | `8c4b4dc24661c42daa90024f4c98395c98f70414d299a88b53ab75aea169a8f4` |
| `latin/macer_floridus_de_viribus_herbarum.wikitext.json` | `e3d0fe80a5623679281319c4724466720b76651096c62bd41843793fec564866` |
| `latin/vulgate_bible-corpus_Latin.xml` | `5bba9f75c06858a28ebe7b2fcc19cc32b3fbf587d6bc237ceac6fe7addd3df31` |

### 4. A verification method that makes re-pinning provable, not guesswork

Because the hashes survived, a candidate URL can be *proved* correct rather than trusted:

```
candidate URL → download → sha256 → compare against the recovered hash above
```

A match means the URL serves byte-identical content to what produced every published H4
number. This is strictly stronger than the usual "pin whatever the URL returns today".

### 5. The method works — the Latin Vulgate is already proven

```
https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/Latin.xml
  HTTP 200, 4,877,710 bytes
  sha256 5bba9f75c06858a28ebe7b2fcc19cc32b3fbf587d6bc237ceac6fe7addd3df31   ← exact match
```

For an immutable pin in the L21 style, that path last changed at commit
`0f35d074af28a0499cffe37e62b39922595f9db7` (2015-10-16), so a permalink pin is available and
the content has been stable for a decade.

## How much does each family actually unblock?

Static analysis, and I want to be explicit that it brackets rather than settles the answer.
Counting only **direct** H4 references in each experiment module gives 16 experiments:

| needs | count | experiments |
|---|---|---|
| Latin only | 9 | e2, e13d, e15, e15b, e19, e20, e21, e22, e27 |
| Latin + German | 5 | e13, e13b, e13c, e14, e14b |
| Latin + Hebrew | 1 | e5 |
| all four | 1 | e19b |

Propagating imports one hop instead gives 31 experiments and all four families almost
everywhere — but that over-attributes: e32 and e34 appear to need German and Hebrew, yet both
ran successfully with no H4 data at all. The truth is between the two, so:

**The realistic bracket is that Latin alone unblocks somewhere between 9 and 22 experiments.**
The cheap way to settle it is empirical, not analytical — pin Latin, re-run the suite, count.

## Cost, if approved

| family | download | note |
|---|---|---|
| Latin (Vulgate) | 4.9 MB | proven above |
| Hebrew (7 JSONs) | small | PD; 7 separate pins |
| Italian (Decameron) | ~1.5 MB | licence apparatus is the fiddliest of the four |
| German (ReF v1.0.2) | 143.5 MB | dominates `acquire` runtime and disk |
| German (ReM v2.1) | 27.9 MB | |

Pinning all of H4 would take `acquire` from ~15 modest files to roughly 180 MB. Worth deciding
whether the German bracket ships by default or behind an opt-in flag.

## Questions only Tim can answer

1. **Does L19 consume-only extend to registering these URLs?** The registry records a URL and
   a hash, not content — but it is the project's licensing posture, and it is your call.
2. **Is "no explicit repo licence" (bible-corpus packaging) acceptable to pin?** The text is
   PD; the XML packaging is unlicensed. L21 accepted a modified-MIT source with a citation
   requirement, which is a different shape of risk.
3. **Ship the 143.5 MB German bracket by default, or behind a flag?**
4. **Attribution:** CC BY-SA 4.0 (ReM/ReF) and CC BY-NC-SA 4.0 (Decameron apparatus) carry
   attribution terms. The `Source.notes` field already carries licence text for Naibbe; same
   mechanism would serve, but confirm it satisfies you.

## Implementation steps, if and when approved

1. Recover or re-derive one URL per raw file; **prove each against the recovered hash** by the
   method above. Do not pin any URL whose bytes do not match.
2. Add `_h4_sources()` to `src/ms408/sources.py` alongside `_naibbe_sources()` /
   `_timm_sources()`, carrying licence text in `notes` per source.
3. Run `python -m ms408.acquire`, then `python -m ms408.h4`; confirm the rebuilt
   `data/processed/h4/manifest.json` matches the committed one **hash for hash** — that
   proves the whole chain reproduces the published corpora exactly.
4. Re-run the 36 offline experiments; record the true unblocked count against the 9–22 bracket.
5. Extend the D22 allow-list with any newly produced result JSONs that
   `scripts/audit_results_tier.py` clears as metrics-only.
6. Drop the `needs_h4` skip from `test_real_latin_is_excluded` if it now runs in CI.
7. Regenerate `results/harness/benchmark.json` so its corrected `entropy_method` string ships.

## Time-sensitive

`data/raw/h4/MANIFEST.json` is the **only** record of the original download URLs, and it is
gitignored. It is absent from this machine. If it still exists on another machine (Tailscale
shows `macbook-pro-2`, last seen offline), copying it somewhere durable would turn step 1 from
re-derivation into transcription. Worth doing before that machine is wiped or rotated.
