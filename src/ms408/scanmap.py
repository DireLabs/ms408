"""Join IVTFF pages to Beinecke scan files (T0.2).

IVTFF names foldout panels as separate pages (f70r1, f70r2, fRos, ...) while Yale
photographs physical spreads ("69v and 70r", "70v (part)", "85v and 86r (foldout)").
The join is therefore many-to-many at foldouts:

- simple folios: exact 1:1 by folio-side ("1r" -> f1r)
- foldout panels: every canvas whose label mentions the panel's base folio-side is a
  candidate; identical "(part)" labels cannot be told apart without inspecting pixels,
  so those pages carry ambiguous=true (resolve manually at annotation time, T1.2)
- fRos (the rosettes spread) is folio 85v+86r by definition

Output: data/processed/scan_map.json — {page: {files: [...], ambiguous: bool}} plus
the list of canvases matching no text page (covers, edges, flyleaves — expected).

Usage: python -m ms408.scanmap
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .dataset import PROCESSED_ROOT
from .ivtff import IVTFFDocument
from .scans import SCANS_ROOT
from .sources import path_for

FOLIO_SIDE_RE = re.compile(r"(\d+)(r|v)")
PAGE_RE = re.compile(r"f(\d+)(r|v)\d*$")


def page_base(page_name: str) -> str | None:
    """IVTFF page name -> base folio-side ('f70r2' -> '70r'); None for fRos etc."""
    m = PAGE_RE.match(page_name)
    return f"{int(m.group(1))}{m.group(2)}" if m else None


def label_sides(label: str) -> set[str]:
    """Canvas label -> folio-sides it depicts ('69v and 70r' -> {'69v', '70r'})."""
    return {f"{int(n)}{side}" for n, side in FOLIO_SIDE_RE.findall(label)}


def build_scan_map(out_path: Path | None = None) -> dict:
    zl = IVTFFDocument.load(path_for("zl"))
    records = [json.loads(line) for line in open(SCANS_ROOT / "index.jsonl")]
    for record in records:
        record["sides"] = label_sides(record["label"])

    pages: dict[str, dict] = {}
    matched_files: set[str] = set()
    for page in zl.pages:
        base = page_base(page.name)
        if page.name == "fRos":
            base = None
            candidates = [r for r in records if {"85v", "86r"} <= r["sides"]]
        elif base is None:
            candidates = []
        else:
            candidates = [r for r in records if base in r["sides"]]
        files = [r["file"] for r in candidates]
        matched_files.update(files)
        pages[page.name] = {"files": files, "ambiguous": len(files) > 1}

    unmatched = [r["file"] for r in records if r["file"] not in matched_files]
    scan_map = {
        "pages": pages,
        "unmatched_canvases": unmatched,
        "stats": {
            "pages_total": len(pages),
            "pages_unmapped": sum(1 for p in pages.values() if not p["files"]),
            "pages_ambiguous": sum(1 for p in pages.values() if p["ambiguous"]),
            "canvases_unmatched": len(unmatched),
        },
    }
    out_path = out_path or PROCESSED_ROOT / "scan_map.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(scan_map, indent=2) + "\n")
    return scan_map


if __name__ == "__main__":
    print(json.dumps(build_scan_map()["stats"], indent=2))
