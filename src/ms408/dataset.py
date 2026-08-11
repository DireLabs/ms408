"""Build the versioned page-level dataset (T0.2).

Joins transliteration text and page metadata from the pinned raw sources into
page-level JSONL under data/processed/, one file per transliteration, plus a
build manifest recording input checksums, dataset version, and the producing
git commit (L3 provenance discipline).

The JSONL files stay gitignored (L19 consume-only: the repo does not carry
third-party text, even derived); the manifest is committed. The dataset is
reproducible exactly via:

    python -m ms408.acquire && python -m ms408.dataset

Loci carry raw IVTFF text verbatim — word extraction happens at analysis time
via an explicit ivtff.TextPolicy, never at build time.
"""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from .acquire import sha256_of
from .ivtff import IVTFFDocument
from .sources import DATA_HOME, SOURCES, path_for

DATASET_VERSION = "0.1.0"
PROCESSED_ROOT = DATA_HOME / "processed"
TRANSLITERATIONS = ("zl", "gc")  # EVA primary + v101 sensitivity (L11)


def page_record(page) -> dict:
    return {
        "page": page.name,
        "quire": page.variables.get("Q"),
        "page_in_quire": page.variables.get("P"),
        "folio_in_quire": page.variables.get("F"),
        "bifolio": page.variables.get("B"),
        "illustration": page.variables.get("I"),
        "currier_language": page.variables.get("L"),
        "hand": page.variables.get("H"),
        "currier_hand": page.variables.get("C"),
        "extraneous": page.variables.get("X"),
        "loci": [
            {"num": locus.num, "locator": locus.locator, "text": locus.text}
            for locus in page.loci
        ],
    }


def git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def build(out_root: Path = PROCESSED_ROOT) -> dict:
    out_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "dataset_version": DATASET_VERSION,
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "sources": {},
        "counts": {},
    }
    for name in TRANSLITERATIONS:
        source, path = SOURCES[name], path_for(name)
        doc = IVTFFDocument.load(path)
        out_path = out_root / f"pages_{name}.jsonl"
        with open(out_path, "w") as out:
            for page in doc.pages:
                out.write(json.dumps(page_record(page)) + "\n")
        manifest["sources"][name] = {
            "url": source.url,
            "sha256": sha256_of(path),
            "pinned_sha256": source.sha256,
            "alphabet": doc.alphabet,
        }
        manifest["counts"][name] = {
            "pages": len(doc.pages),
            "loci": len(doc.loci),
        }
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
