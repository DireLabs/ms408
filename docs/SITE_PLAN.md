# Site plan — the MS408 public website (GitHub Pages)

Scope: a website version of the repository — a front door for two audiences (Voynich/MS 408
researchers and technical users) — with room to grow. Surfaces requested:
1. **Docs mirror** — the repo's docs (tutorial, methodology, limits, glossary, evaluator) as
   layered web pages (overview → deep-dive), plus the "run your own hypothesis" pitch.
2. **Papers** — preprints (early/unofficial drafts *and* final publications), versioned, each
   with abstract, PDF, and DOI once minted.
3. **Blog / news** — ongoing insights and release notes; low-friction to publish.
4. **Interactive research timeline** — two tracks: (a) *our* program (iterations i01–i11, the
   E-series, the self-corrections), and (b) the *community's* body of MS 408 research, pulled
   from a separate contributor-editable repo.

## Recommended architecture

- **Hosting:** GitHub Pages, built by a GitHub Action on push to `main` (so we're not committing
  built HTML). Custom domain later via `CNAME` (e.g. a `direlabs.com` subdomain) — optional.
- **Static-site generator:** see the decision below. Lead recommendation **Astro** — content
  collections for Markdown/MDX (our docs are already Markdown), static output, and interactive
  "islands" for the timeline without shipping a heavy SPA; clean fit for docs + blog + landing +
  one interactive component, and it scales as surfaces are added.
- **Content source of truth stays in the repo.** Site pages import/transclude the existing
  `docs/*.md` where possible, so docs don't fork from the package. A short build step copies or
  symlinks `README`, `docs/`, and paper abstracts into the site's content dir.

## Site map (v1 → later)

```
/                     Landing: what it is, "pick your path", the honest-record hook
/docs/                Layered docs (mirror): overview → tutorial → evaluator → methodology
                      → limits → glossary   [v1]
/papers/              Preprints list; per-paper page (abstract, versions, PDF, DOI, BibTeX) [v1]
/blog/                Posts + release notes (RSS)                                    [v1 or v2]
/timeline/            Interactive: our program track (i01–i11 + E-series)            [v2]
/community/           Interactive: community research map, from ms408-community-map  [v2/v3]
/about/ , /cite/                                                                     [v1]
```

## The community map — a separate, contributor-editable repo

A dedicated **`ms408-community-map`** repo holds structured data (one YAML/JSON record per
community contribution: title, authors, year, type, claim, links, tags). The site pulls it at
build time to render the community timeline. Two low-friction contribution paths:
- **PR workflow** (technical contributors): add/edit a YAML file, open a PR; CI validates the
  schema.
- **Form workflow** (low-code contributors): a GitHub **Issue Form** captures the fields; an
  Action turns a submitted issue into a data file / PR — the "Slack-GitHub-integration" ergonomics.
Keeping it a separate repo (a) isolates community data + its PR traffic from the code repo, (b)
lets it be reused/versioned independently, and (c) gives contributors a small, unintimidating
surface. The main site consumes it read-only.

## Build & deploy (once the SSG is chosen)

- `site/` directory in this repo (or a dedicated `ms408-site` repo — decision below).
- `.github/workflows/pages.yml`: build on push, deploy to Pages. Papers' PDFs built by the
  existing `paper/make_arxiv_bundle.sh` / a latex Action, or uploaded as release assets and linked.
- Link-check + build in CI so a broken doc link fails the build.

## Decisions to confirm before building

- **D-site-1 — SSG framework** (Astro vs Docusaurus vs MkDocs Material). Shapes everything.
- **D-site-2 — Site location** (a `site/` folder in this repo, or a separate `ms408-site` repo).
- **D-site-3 — v1 scope** (docs+papers first, or include blog+timeline in the first cut).
- **D-site-4 — community-map repo** (create the separate `ms408-community-map` now, or defer to v2).
