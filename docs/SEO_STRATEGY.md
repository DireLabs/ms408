# SEO Strategy — MS408 / Voynich Manuscript site

_Evidence-based plan for a small, new, academically credible open-source site (Astro +
GitHub Pages). Produced from a web-grounded research pass (2026 landscape). Keyword volumes
are **directional, from observed SERPs — not measured** (grade C); validate in Search Console
before over-investing. Best-practice/landscape claims are grade B with sources inline._

## 0. Strategic framing

We are a **new, high-topic-authority but zero-domain-authority** site in a niche with (a)
entrenched community sites (voynich.nu, voynich.ninja) and (b) a large pop-culture
"decoded!/solved!" clickbait flood. Our edge is the opposite of that flood: the **cold,
reproducible, refutation-first** resource — which is also the best modern-SEO asset, because
AI answer engines and Google E-E-A-T now reward citable, structured, methodologically
transparent content.

Three consequences drive everything:
1. **Don't fight head terms; own the methodology long tail.** We won't outrank Wikipedia/Yale
   for "voynich manuscript"; we can own "evaluate voynich cipher hypothesis," "voynich EVA
   transliteration," "voynich manuscript statistics."
2. **AEO/GEO is first-class.** ~55% of Google searches show AI Overviews; being the precise,
   hedged, sourced answer to "has the Voynich been decoded?" is a real acquisition channel.
3. **Protect credibility while chasing discovery.** The pop-culture "media" page is
   top-of-funnel gold but must be editorially walled off so it feeds — not dilutes — the core.

## 1. Keyword clusters (priority: B & D first, then C, then A/F via AEO, then E)

- **A — Head/informational** (`voynich manuscript`, `…decoded`, `…translation`): HIGH
  competition; do NOT target for ranking. Capture via **AEO** — one hedged, sourced explainer +
  FAQ that answer engines cite for "has it been decoded?" (counter the 2026 "AI cracked it" wave).
- **B — Methodology/computational** (PRIMARY WINNABLE): `evaluate voynich cipher hypothesis`,
  `voynich manuscript statistics`, `voynich transliteration EVA`/`v101`, `Currier A B voynich`,
  `voynich entropy`/`conditional entropy`/`zipf`/`word length`, `undeciphered corpus benchmark`,
  `voynich python package`/`ms408`. One page per concept, definition-first.
- **C — Tool/how-to** (audience 2): `how to score a voynich hypothesis`, `voynich dataset
  download`, `pip install ms408`, `voynich statistical bands`. Match verbatim install strings.
- **D — Glossary long tail** (cheapest, compounding): one anchor/page per term — EVA, Currier
  A/B, vord, labelese, conditional entropy, statistical band, Beinecke MS 408, quire/bifolio.
- **E — Education/library** (audience 4, seasonal): `voynich lesson plan`, `cryptography
  classroom activity`, `library program medieval manuscripts`.
- **F — Pop-culture adjacency** (top-of-funnel via media page): `voynich in Assassin's Creed`,
  `voynich documentary`, `voynich AI decoded` (debunk), `voynich theories`.

## 2. Technical SEO (Astro + GitHub Pages)

- **2.1 Domain decision (load-bearing prerequisite — see DECISIONS).** Use a **custom root
  domain**, not `user.github.io/ms408/`. A project sub-path forces an Astro `base` and makes
  every canonical/OG/sitemap URL fragile. Set `site` to the full domain; add `CNAME` + enforce
  HTTPS; pick apex-vs-www and 301 the other.
- **2.2 Crawl/index:** `@astrojs/sitemap`; `robots.txt` linking it and **allowing AI crawlers**
  (GPTBot/ClaudeBot/PerplexityBot/Google-Extended — being cited is the goal here); absolute
  canonical tags on every page (protects attribution against scrapers).
- **2.3 Per-page metadata:** one reusable `<SEO>` component (e.g. `astro-seo`); unique
  deliberate title + meta description per page; Open Graph + Twitter cards (default 1200×630 +
  per-paper images) — the papers/media pages are the shareable surfaces.
- **2.4 Structured data (JSON-LD):** `ScholarlyArticle` (papers), `SoftwareSourceCode`/`
  SoftwareApplication` (the tool), `Article`/`TechArticle` (docs), `FAQPage` (glossary/FAQ —
  markup still feeds AI answers though Google restricted the rich result), `Course`/`
  LearningResource` (education), `Dataset` (**Google drops its rich result Jan 2026 — still add
  it; no penalty; used by Dataset Search + AI grounding**), `Organization`+`WebSite` (entity
  recognition — high value), `BreadcrumbList`.
- **2.5 Core Web Vitals:** lean into Astro's static output — near-zero JS (islands only for the
  timeline), self-host/preconnect fonts, compressed OG images, lazy-load below fold.
- **2.6 Indexability:** interactive sections (timeline, media feed) need **static-HTML
  fallbacks**; stable human-readable URLs (`/glossary/eva-transliteration`); interlink everything.

## 3. Content strategy per section

- **Docs + Glossary = the SEO engine** (clusters B/C/D). AEO-first: lead each page with a 1–2
  sentence direct definition, then depth. The glossary is disproportionately valuable (dozens of
  cheap long-tail captures); the **Limits page** is the honest, citable answer to "has it been
  solved?"
- **Papers** = authority + academic conversion. Each preprint gets its own indexable HTML
  landing page (crawlable abstract, `ScholarlyArticle` JSON-LD, DOI/arXiv/Zenodo links,
  how-to-cite) — not a PDF-only link (PDFs index poorly; AI prefers HTML).
- **Timeline** = engagement + long-tail; must have a static-HTML fallback.
- **Library/education** = audience 4 + a realistic **backlink magnet** (education/DH directories
  link to free classroom resources); `Course` schema; design activities as linkable units.
- **Media/pop-culture feed** = top-of-funnel, **quarantined**: `/media/` path, each item gets a
  one-line graded/sourced reality-check linking inward to methodology/limits (the funnel); keep
  `Organization` schema consistent; don't let it dominate the homepage or sitemap prominence.

## 4. Authority & backlinks (realistic for academic OSS)

- **Do (high realism):** `CITATION.cff` → GitHub "Cite this repository" → **Zenodo DOI** on
  release (single highest-leverage action); **arXiv** preprints linking back; rich GitHub repo;
  **JOSS** if the tool qualifies (peer-reviewed → DOI → Wikipedia-citability path); genuine
  engagement with the **Voynich community** (voynich.nu, voynich.ninja + wiki, Bowern's Yale
  Voynich resources) for earned, topically-perfect mentions; DH tool/method directories.
- **Medium:** Papers-with-Code **retired (Jul 2025)** → use **CodeSOTA** + publish a
  **Croissant** dataset-metadata doc (how ML researchers now find benchmark corpora); academic
  Bluesky/Mastodon/X for human shares that lead to citations.
- **Low / manage expectations:** **Wikipedia** — do NOT self-cite (reverted; preprints are
  low-reliability there); path in is peer-review first, then a neutral third party cites us.
- **Avoid:** paid links, mass directory spam, forum comment spam — they damage the credibility
  that is our whole moat.

## 5. Measurement

- **Analytics (privacy-respecting, matches OSS ethos):** GoatCounter (lightest, cookieless,
  free for OSS) or Plausible (more features + built-in Search Console integration). No Google
  Analytics.
- **Search Console** (mandatory — only real query data; validates §1 hypotheses) + Bing
  Webmaster (also feeds ChatGPT search).
- **KPIs:** indexed-page coverage; impressions on cluster-B/D queries; non-brand organic clicks
  to docs/glossary/papers; backlinks from the target ecosystem; a **quarterly manual AEO
  citation check** ("has the Voynich been decoded?" in ChatGPT/Perplexity/AI Overviews); PyPI
  downloads / GitHub stars as adoption proxies.

## 6. Roadmap — top 5 highest-leverage actions for a new small site

1. **Lock the domain + Astro `site` config** (custom root domain, HTTPS) — blocks all
   canonical/OG/sitemap work.
2. **Technical baseline:** `@astrojs/sitemap`, `robots.txt` (AI crawlers allowed), per-page
   canonical + meta + OG/Twitter, `Organization`+`WebSite` JSON-LD, one reusable `<SEO>` component.
3. **Build the glossary + core stat/method pages AEO-first** (definition-first, one concept per
   page, heavily interlinked) — cheapest, most compounding, most winnable.
4. **`CITATION.cff` → Zenodo DOI** + arXiv links; each preprint an HTML landing page with
   `ScholarlyArticle` schema.
5. **Search Console + privacy analytics + submit sitemap** — measure from day one.

**Do next:** flesh out docs clusters; the hedged "has it been decoded?" explainer/FAQ; Croissant
+ CodeSOTA listing; education portal with `Course` schema + directory outreach; community
engagement. **Later:** timeline + media feed (with static fallbacks + the media credibility
firewall); JOSS submission; quarterly freshness + AEO audit.

## Decision to surface
- **D-site-5 — custom domain.** A custom root domain (e.g. `ms408.<tld>`) is a prerequisite for
  most technical SEO and cleaner than a `user.github.io/ms408/` project path. Not covered by the
  existing site decisions — worth deciding before the SEO/technical baseline work.
