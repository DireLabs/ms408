# MS408 theme — a manuscript-derived design layer

A Phase-2 design system that layers a *manuscript-inspired* skin over the professional IBM
Plex / architectural base (`global.css`). Opt-in per section: warmer and book-like for
**Library**, a looser setting for **Media**, while Docs/Papers/Home keep the clean default.
Goal: a distinctive, tasteful "MS408 look" we can also spin out as its own open component kit.

## Licensing stance (important)

The Voynich Manuscript is public domain (early 15th c.). Rather than embed Yale/Beinecke scan
photography (whose reproduction rights can be murky across jurisdictions), we build **original
vector motifs inspired by the manuscript's visual language** — botanical line-art, rosette/
cosmological rings, decorative initials, parchment textures. Everything ships under our own
license, fully redistributable, with no third-party image dependency. If we later want actual
folios (e.g. on the Media/Timeline pages), we link out to Yale's viewer rather than re-host.

## Design tokens (the manuscript palette)

Derived from the manuscript's materials, not copied from it:
- **Vellum/parchment** backgrounds — warm cream `#f3ead6` → `#efe4cb`.
- **Iron-gall ink** — brown-black `#2b2117` (text), `#4a3c2a` (secondary).
- **Rubric red** — faded vermilion `#9e3b2f` (the themed accent — authentic to medieval rubrication).
- **Botanical green** `#6b7250` and **faded blue** `#5b6b7a` — secondary accents (herbal / astro pages).
- **Tan hairlines** `#d8c9a8`.
- Type: keep IBM Plex for legibility; **IBM Plex Serif** for themed headings + reading, with
  decorative initials (drop-caps) and manuscript flourishes as accents.

## Motif inventory (original SVG/CSS)

1. **Botanical divider** — an herbal-inspired sprig used as a section rule. ✅ v1
2. **Rosette** — concentric ring motif (cosmological pages) for corner/hero accents. ✅ v1
3. **Drop-cap / decorative initial** — first-letter treatment for themed prose. ✅ v1 (CSS)
4. **Parchment texture** — a very subtle vellum background (CSS, no image). ✅ v1
5. Later: a "Voynichese-flavored" glyph dingbat set (original marks, clearly decorative — never
   presented as real transliteration), marginalia/initial frames, a herbal corner illustration.

## Application (opt-in via a `theme` prop on the layout)

- `theme="ms408"` sets `class="theme-ms408"` on `<body>`; `theme-ms408.css` scopes every
  override under that class, so unthemed pages are untouched.
- **Library** (v1): full skin — parchment, serif headings, botanical dividers, drop-caps on
  activities (book-like, kid-friendly).
- **Media** (planned): a lighter setting — parchment tint + serif headings, but the feed keeps
  its structure (a "looser" variant, e.g. `theme="ms408-media"` or a modifier class).
- **Timeline** (optional): a rosette accent could suit the "record" framing.
- Docs / Papers / Home stay on the clean default.

## Distribution roadmap (later)

- Extract the tokens + motifs into a standalone package (CSS variables + SVG components) — an
  "MS408 UI kit."
- Port to popular platforms: a Bootstrap 5 theme (SCSS variable map + a few components) and a
  WordPress block theme (theme.json palette + block styles). Each is a mechanical mapping of the
  same tokens; scope as a follow-up once the web components settle.

## Status

- ✅ v1: `theme-ms408.css` + botanical divider, rosette, drop-cap, parchment texture; applied to
  the Library section.
- ⬜ Media "looser" variant; Timeline rosette accent; the glyph dingbat set; the Bootstrap /
  WordPress ports.
