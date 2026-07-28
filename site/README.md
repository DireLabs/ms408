# MS408 site

The public website (Astro → GitHub Pages). It is a **mirror of the repository**: the docs
pages are synced from `../docs` and `../CONTRIBUTING.md` at build time (`scripts/sync-content.mjs`),
so documentation has one source of truth. See `../docs/SITE_PLAN.md` for the roadmap.

## Develop

```bash
cd site
npm install
npm run dev        # runs the content sync, then a local server
```

`npm run build` writes static output to `dist/`. `npm run sync` alone refreshes the synced
docs. Synced content (`src/content/docs/`), `node_modules/`, `dist/`, and `.astro/` are
gitignored — everything under `src/pages`, `src/layouts`, `src/data`, `src/styles`, and the
config is the committed source.

## Deploy

Pushed automatically by `.github/workflows/pages.yml` on changes to `site/**` or `docs/**`.
The Action derives the base path and origin from the repo's Pages settings (project vs
user/org), so no hardcoded URL is needed in CI. For a **local** build the base defaults to
`/ms408` (a project page) — override with `SITE_BASE=/` for a user/org or custom-domain site.

## What's here (v1) and what's next

- **v1:** landing, layered docs (tutorial / limits / methodology / glossary / contributing),
  papers list, about, cite.
- **v2 (see SITE_PLAN):** blog/news, the interactive research timeline, and the community
  research map (a separate `ms408-community-map` repo consumed here).

## Placeholders to replace before launch

`direlabs/ms408` appears as a default in `astro.config.mjs` and `src/config.ts` (both overridden
in CI). Also replace it in the repo-level `CITATION.cff`, README badges, and
`.github/ISSUE_TEMPLATE/config.yml`. Tracked in `../OSS_RELEASE.md`.
