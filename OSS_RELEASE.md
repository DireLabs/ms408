# OSS release checklist

Living checklist for publishing `ms408` as an open-source repository. Grouped by severity.
`[x]` done · `[ ]` open · **(you)** = author action I can't do (key rotation, publishing,
naming). Diagnostics as of the last update: `pip check` clean · `ruff check src tests examples`
clean · `python -m ms408.verify` PASS · `pytest -q` **180 passed** · wheel builds and ships
`reference_bands.json` + CLI · `import ms408` makes no network/API calls.

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
- [ ] **(you) Enable GitHub Pages** for the repo (Settings → Pages → Source: GitHub Actions)
  so the `pages` workflow can deploy.
- [ ] v2 (see `docs/SITE_PLAN.md`): blog/news, interactive research timeline, and the separate
  `ms408-community-map` repo.

## Open URLs / naming (fill once the GitHub repo exists)

- [ ] **(you) Replace the `OWNER/ms408` placeholder** with the real repo path in: README badges,
  `CITATION.cff` (`repository-code`), `.github/ISSUE_TEMPLATE/config.yml`, and the two site
  defaults (`site/astro.config.mjs`, `site/src/config.ts` — CI overrides these, so only the
  local-build defaults). (Grep `OWNER/ms408`.)
- [x] **Contact line `ti.mims.ms` is NOT a typo** — it is Tim's actual personal site
  (https://ti.mims.ms), alongside direlabs.com. The paper contact lines are correct as-is.
  (Earlier flagged as a possible typo; retracted.)
- [ ] **(you) DOI:** mint on arXiv/Zenodo registration, then add to `CITATION.cff` and a README badge.

## Release-build steps (when the above are green)

1. `git status` clean; confirm no `.env`, no `.DS_Store`, no `data/raw/` in the tree.
2. Fresh clone to a temp dir; `pip install -e ".[dev]"`; `ruff check src tests examples`; `pytest -q`.
3. `python -m ms408.acquire` then `python -m ms408.verify --full` (reproduces the shipped bands).
4. `python -m build` from the clean clone; verify the wheel ships `reference_bands.json`.
5. Tag `v0.1.0`; push; confirm CI green; publish.
