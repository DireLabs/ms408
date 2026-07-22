#!/usr/bin/env bash
# Assemble arXiv-ready source tarballs for the two preprints.
#
# arXiv compiles the LaTeX source itself, so we ship main.tex + main.bbl (the pre-built
# bibliography, so arXiv need not run bibtex) — nothing else. Build artifacts
# (.aux/.log/.out/.fls/.fdb_latexmk/.blg/.pdf) are excluded. Run from repo root:
#
#     bash paper/make_arxiv_bundle.sh
#
# Output: paper/dist/<name>-arxiv.tar.gz, each self-contained. Does NOT submit anything.
set -euo pipefail
cd "$(dirname "$0")/.."          # repo root

DIST="paper/dist"
rm -rf "$DIST"
mkdir -p "$DIST"

bundle() {                       # bundle <src-dir> <out-name>
  local src="$1" name="$2"
  ( cd "$src" && latexmk -pdf -interaction=nonstopmode main.tex >/dev/null 2>&1 )  # ensure fresh .bbl
  local stage="$DIST/$name"
  mkdir -p "$stage"
  cp "$src/main.tex" "$src/main.bbl" "$stage/"
  ( cd "$DIST" && tar -czf "$name-arxiv.tar.gz" "$name" && rm -rf "$name" )
  echo "  $DIST/$name-arxiv.tar.gz  ($(cd "$src" && pdfinfo main.pdf 2>/dev/null | awk '/^Pages/{print $2" pp"}'))"
}

echo "Building arXiv bundles:"
bundle paper/v6b          v6b-constraint-envelope
bundle paper/methods/v3   methods-v3-adversarial-self-correction
echo "Done. See paper/SUBMISSION.md for the arXiv metadata + checklist."
