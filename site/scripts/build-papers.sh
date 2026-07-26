#!/usr/bin/env bash
# Build the preprint PDFs and stage them as static site assets (site/public/papers/<id>.pdf),
# so the papers page can link them without committing binaries. Run from anywhere.
# CI (pages.yml) runs this before the Astro build; run it locally too if you want PDFs in dev.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root
OUT="site/public/papers"
mkdir -p "$OUT"

build() {                           # build <source-dir> <out-id>
  local src="$1" id="$2"
  ( cd "$src" && latexmk -pdf -interaction=nonstopmode main.tex >/dev/null 2>&1 )
  cp "$src/main.pdf" "$OUT/$id.pdf"
  echo "built $OUT/$id.pdf ($(cd "$src" && pdfinfo main.pdf 2>/dev/null | awk '/^Pages/{print $2" pp"}'))"
}

# Keep the ids in sync with site/src/data/papers.json (id + pdf fields).
build paper/v7          constraint-envelope
build paper/methods/v3  adversarial-self-correction
echo "Done. PDFs in $OUT/"
