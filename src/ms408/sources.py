"""Pinned registry of external sources (T0.2).

Every external file the pipeline consumes is pinned here by exact URL and sha256.
Files land in data/raw/ (gitignored — consume-only per L19); SOURCES.md in
docs/planning/i01/ documents provenance and licensing for each.

Upstream files version-bump in place (e.g. ZL3a -> ZL3b), so a checksum mismatch
on re-download means the source moved: re-verify, then re-pin deliberately.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    dest: str  # path relative to data/raw/
    sha256: str
    notes: str


SOURCES: dict[str, Source] = {
    s.name: s
    for s in [
        Source(
            name="zl",
            url="https://www.voynich.nu/data/ZL3b-n.txt",
            dest="transliterations/ZL3b-n.txt",
            sha256="bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
            notes="Zandbergen-Landini EVA, v3b 2025-05-13. Primary corpus (L11). "
            "Complete: 227 pages, 5389 loci, $I/$L/$H/$C metadata in page headers.",
        ),
        Source(
            name="gc",
            url="https://www.voynich.nu/data/GC2a-n.txt",
            dest="transliterations/GC2a-n.txt",
            sha256="b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f",
            notes="Claston v101 in IVTFF form. Sensitivity corpus (L11). "
            "High-ASCII glyphs escaped as @nnn;.",
        ),
        Source(
            name="v101_original",
            url="https://www.voynich.nu/data/voyn_101.txt",
            dest="transliterations/voyn_101.txt",
            sha256="f278a451d873c520f7ab509c4af12152698a1d3efd2353924e177a565c17ba7e",
            notes="Claston's original v101 file (provenance reference; cp1252-style "
            "high-ASCII bytes, non-IVTFF record format).",
        ),
        Source(
            name="rf",
            url="https://www.voynich.nu/data/RF1b-e.txt",
            dest="transliterations/RF1b-e.txt",
            sha256="e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782",
            notes="Reference transliteration (extended EVA, combines ZL+GC). Cross-check only.",
        ),
        Source(
            name="ivtff_spec",
            url="https://www.voynich.nu/software/ivtt/IVTFF_format.pdf",
            dest="specs/IVTFF_format.pdf",
            sha256="7ac9c4a82064763cac8767cca6f661cc4e1b4503ab9342acc03032ddb6939d49",
            notes="IVTFF format spec v2.0.1 (doc issue 2.0.2, 2025-07-08).",
        ),
    ]
}

RAW_ROOT = Path(__file__).resolve().parents[2] / "data" / "raw"


def path_for(name: str) -> Path:
    """Absolute path where a registered source lives locally."""
    return RAW_ROOT / SOURCES[name].dest
