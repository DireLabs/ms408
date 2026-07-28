# MS408 UI kit

A small, portable design kit distilled from the MS408 website — so the look can be reused and,
eventually, spun out as its own open-source project. Everything here is **original and
redistributable**: motifs are our own vector art (inspired by, never traced from, the public-
domain manuscript), and the palette/type are documented tokens. See `docs/THEME_PLAN.md` for the
full plan.

## Two flavors, one token set

- **Architectural** — IBM Plex + Carbon-derived neutrals + interactive blue, sharp corners. The
  professional default (docs, research, home).
- **Manuscript** — iron-gall ink + vellum parchment + rubric red, IBM Plex Serif headings,
  botanical/glyph/rosette motifs. The MS408 skin (library = full book look; media = a lighter
  "clippings" variant).

`tokens.css` is the single source of truth; the website CSS and the ports below all derive from it.

## What's here

```
theme-kit/
  tokens.css                     # canonical design tokens (both palettes + type + flag colors)
  bootstrap/_ms408-variables.scss# Bootstrap 5 variable map (import before bootstrap)
  wordpress/theme.json           # WordPress block-theme starter (palette + font families)
  motifs/                        # framework-agnostic SVGs (currentColor, recolorable)
    botanical-divider.svg  glyph-frieze.svg  herbal-sprig.svg  rosette.svg
```

The live web components (Astro) live in `site/src/components/` and the scoped skin in
`site/src/styles/theme-ms408.css`; the `motifs/*.svg` here are their portable equivalents.

## Using it

- **Plain HTML/CSS:** include `tokens.css`, load IBM Plex (e.g. `@fontsource/ibm-plex-*`), and use
  the `--ms408-*` variables. Drop motifs in as `<img>` or inline SVG; they inherit `currentColor`.
- **Bootstrap 5:** `@import "bootstrap/_ms408-variables"; @import "bootstrap/scss/bootstrap";`
  Uncomment the manuscript block to swap the whole theme to the MS408 skin.
- **WordPress:** use `wordpress/theme.json` as a block-theme starter (palette slugs + font
  families); a `styles/` variation can flip between the architectural and manuscript palettes.

## Honesty note (carries the project's posture)

The glyph frieze and any glyph-like marks are **ornamental pen-flourishes** — they evoke the
manuscript's handwritten rhythm but are **not** real Voynich glyphs and are never a
transliteration. Keep them decorative and `aria-hidden`.

## Roadmap

- ⬜ Marginalia / initial frames; a fuller herbal illustration set.
- ⬜ A proper glyph dingbat **font** (build via a font pipeline, e.g. FontForge/opentype.js).
- ⬜ Package as a standalone repo (`ms408-ui-kit`) with a small demo, once the components settle.
- ⬜ Ship the Bootstrap theme + WordPress block theme as installable artifacts.
