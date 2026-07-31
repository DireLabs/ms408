# OSS release checklist

> **Live (pushed to `DireLabs/ms408`, 2026-07-28):** the **`ci` workflow is green** on `main`
> (lint + test matrix 3.11/3.12/3.13 + wheel-build). Fixes applied on push: pinned ruff's rule
> set (`[tool.ruff.lint] select`) so ruff 0.16's expanded defaults don't fail CI; corrected two
> data-dependent test guards (`test_encoding` checked `manifest.json` instead of the corpus
> `.txt`; `test_e2` was unguarded) so corpus tests skip cleanly when data is absent. The
> **`pages` workflow is ready but waits on you to enable Pages** (Settings → Pages → Source:
> GitHub Actions) — auto-enable needs an admin token the default `GITHUB_TOKEN` lacks.

Living checklist for publishing `ms408` as an open-source repository. Grouped by severity.
`[x]` done · `[ ]` open · **(you)** = author action I can't do (key rotation, publishing,
naming). Diagnostics as of the last update: `pip check` clean · `ruff check src tests examples`
clean · `python -m ms408.verify` PASS · `pytest -q` **180 passed** · wheel builds and ships
`reference_bands.json` + CLI · `import ms408` makes no network/API calls.

## Publish-safety — VERIFIED (2026-07-28)

The **tracked git tree is clean to publish**: no `.env`/key/credential/`.pem`/`.key` files
(only `.env.example`), no `data/raw`/gitignored data, no `.DS_Store`, and **no real API-key
patterns anywhere in the tracked tree**. A clean-checkout build (`git archive HEAD` → wheel)
contains no `.env` and produces a working `ms408-0.1.0` wheel. So `git push` leaks nothing.
(The `.env` on disk still holds keys → rotate per the blocking item, but git won't expose them.)

## BLOCKING — must be true before the repo is public

- [ ] **(you) Rotate/revoke the three API keys** currently in the working-tree `.env`
  (Anthropic, OpenAI, Google). They were **never committed** (0 hits across git history) and
  `.env` is gitignored, so `git push` won't leak them — but they've sat in a soon-to-be-public
  directory, so rotate regardless. Then keep only the local `.env`; `.env.example` is the
  committed template. Build the release from a **clean checkout**, never this working dir.
- [x] **Small-input crash fixed.** `evaluate()`/CLI used to crash with an internal traceback
  on short streams (the README's own example). Now: refuses `< 1000` tokens with a clear
  `ValueError`, warns below 8000 (`LOW TOKEN BUDGET`), and `mz.peak()` guards an empty scan.
  Documented in README/LIMITS/GLOSSARY; regression tests added (`test_evaluate_refuses_short_streams_cleanly`).

## SHOULD-FIX — credibility / quality

- [x] `SECURITY.md` (private disclosure + "never commit secrets / rotate on leak").
- [x] `CITATION.cff` (machine-readable citation; DOI + repo URL to fill — see Open URLs).
- [x] Root `CHANGELOG.md` (software) — distinct from `paper/CHANGELOG.md`.
- [x] `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1, contact tim@mims.ms).
- [x] `.github/PULL_REQUEST_TEMPLATE.md` (firewall/grade/re-pin discipline) + `ISSUE_TEMPLATE/`.
- [x] `docs/GLOSSARY.md` (EVA, Currier A/B, ΔI, h2, ed1, TTR, IVTFF, respacing, …) for the dual audience.
- [x] README **"Pick your path"** fork (researcher vs developer) + badges + token-minimum note.
- [x] `RELEASE-READINESS.md` marked a historical memo; its stale API sketch flagged (real shape → TUTORIAL/GLOSSARY).
- [x] CI matrix extended to 3.13 (was 3.11/3.12; `requires-python >=3.11`).
- [x] **Verified NOT stale:** CONTRIBUTING's "experiments mutate module globals" line is
  *accurate* — `e23_reuse_generator.py` sets `e21.SLOT_SIZES`/`BLOCK_LEN`/`THEME_BOOST`; the
  audit missed it (cross-module attribute assignment, not `global`). The public `signature.py`
  path correctly avoids those imports. Kept the warning.

## NICE-TO-HAVE

- [x] Untracked the 6 committed `paper/**/main.pdf` (contradicted `.gitignore`); PDFs are now
  build-on-demand / site-hosted. Deduped the `.gitignore` LaTeX block. Deleted loose `.DS_Store`.
- [x] Pytest class-scoped-fixture deprecation silenced (`test_h4.py` → `@staticmethod`); suite runs 0 warnings.
- [x] `e12_openai_annotations.jsonl` **cleared to ship** — 129 records of model-generated *feature
  labels* (keys: page/provider/model/features/_cost_usd); contains no third-party corpus text (L19-fine).

## SEO / discoverability baseline (pre-publish)

- [x] `@astrojs/sitemap` — `sitemap-index.xml` generated on build (17 public pages; the hidden
  `/balneo` is excluded via a filter).
- [x] `robots.txt` — Astro endpoint emitting an absolute, base-aware `Sitemap:` URL; AI crawlers
  allowed (per `docs/SEO_STRATEGY.md`).
- [x] Per-page `<link rel="canonical">` + Open Graph + Twitter-card meta in the layout; a
  `noindex` prop (set on `/balneo`).
- [ ] Later (SEO roadmap): a default OG image, JSON-LD (`ScholarlyArticle`/`Organization`),
  Search Console + privacy analytics — after the domain is fixed.

## Website (GitHub Pages)

- [x] Astro v1 site under `site/` — landing (researcher/developer fork), layered docs (synced
  from `docs/`), papers list, about, cite. Builds clean (10 pages). Deploy Action
  `.github/workflows/pages.yml` (derives base/origin from Pages settings).
- [x] Site set up for the **custom domain `ms408.direlabs.com`** (root base `/`): `site/public/CNAME`,
  `astro.config` defaults, sitemap/robots/canonical all on the custom domain. Verified in a build.
- [x] **Site is LIVE at https://ms408.direlabs.com** (2026-07-31) — DNS + Pages + custom domain
  verified (HTTPS 200, PDFs serve). The deploy had been blocked by a fragile LaTeX-in-CI
  `Build paper PDFs` step (latexmk exit 12); fixed by committing the PDFs as assets and dropping
  that step. Full DNS steps recorded in [`docs/DEPLOY.md`](docs/DEPLOY.md).
- [ ] **(you) optional:** tick **Enforce HTTPS** in Settings → Pages (cert is issued) to redirect
  http→https.
- [ ] v2 (see `docs/SITE_PLAN.md`): blog/news, interactive research timeline, and the separate
  `ms408-community-map` repo.

## Open URLs / naming

- [x] **Repo path resolved to `DireLabs/ms408`** — all `OWNER/ms408` placeholders replaced
  (README badges, `CITATION.cff`, issue config, site defaults, sync script). Domain →
  `ms408.direlabs.com`.
- [x] **Contact line `ti.mims.ms` is NOT a typo** — it is Tim's actual personal site
  (https://ti.mims.ms), alongside direlabs.com. The paper contact lines are correct as-is.
  (Earlier flagged as a possible typo; retracted.)
## PyPI + DOI release (PREPPED — one-time setup by you, then it's automated)

Everything is wired; both artifacts pass `twine check`. `ms408` is free on PyPI.

- [x] **`pyproject.toml` PyPI-ready** — public description, `readme`, `license = "Apache-2.0"`
  (+ `license-files`), authors, keywords, classifiers, `[project.urls]`. sdist + wheel build and
  **`twine check` PASSES**.
- [x] **`.github/workflows/publish.yml`** — publishes to PyPI on a GitHub Release via **Trusted
  Publishing** (OIDC, no stored tokens).
- [x] **README badges**: PyPI + site added; **DOI badge placeholder** ready to paste.
- [x] **`docs/RELEASE_NOTES_v0.1.0.md`** — draft release notes to paste into the GitHub Release.
- [ ] **(you) One-time PyPI setup:** on pypi.org add a *Trusted Publisher* (or "pending
  publisher") → owner `DireLabs`, repo `ms408`, workflow `publish.yml`, environment `pypi`.
- [ ] **(you) One-time Zenodo setup:** log into zenodo.org with GitHub → toggle `DireLabs/ms408`
  on.
- [ ] **(you) Cut the release:** create a GitHub Release tagged **`v0.1.0`** (paste the release
  notes). This one action → publishes to PyPI **and** mints the Zenodo DOI. Then paste the DOI
  badge into README + `CITATION.cff` (uncomment the placeholder). Bump `version` before any later
  release (PyPI won't overwrite).

## Release-build sanity (already verified locally)

1. Tree clean to publish (see Publish-safety above); no `.env`/data/`.DS_Store`.
2. `ruff check` clean · `pytest` 180 passed · `python -m ms408.verify --full` reproduces bands.
3. `python -m build` → sdist + wheel; wheel ships `reference_bands.json`; `twine check` passes.
