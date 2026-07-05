"""Download Beinecke MS 408 scans via IIIF manifest crawl (T0.2).

Yale's Open Access Policy permits any use of these images (SOURCES.md §2).
Polite crawl: sequential, delayed. Resumable: files already on disk are skipped.

Each downloaded JPEG's actual pixel dimensions are compared against the canvas
dimensions declared in the manifest — the Image API profile declares a maxArea
that is not currently enforced for full/full requests, and this guard detects
if Yale ever starts enforcing it (index records carry a `dims_ok` flag).

Usage:
    python -m ms408.scans          # fetch manifest + all missing images, write index
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

from .sources import RAW_ROOT

MANIFEST_URL = "https://collections.library.yale.edu/manifests/2002046"
SCANS_ROOT = RAW_ROOT / "scans"
FETCH_DELAY_S = 1.0
USER_AGENT = "ms408-research/0.1"


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def _label_text(label) -> str:
    if isinstance(label, dict):
        for values in label.values():
            if values:
                return str(values[0])
    return str(label)


def _slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_") or "unlabeled"


def jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    """(width, height) from JPEG SOF marker; None if not parseable."""
    data = path.read_bytes()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height = int.from_bytes(data[i + 5 : i + 7], "big")
            width = int.from_bytes(data[i + 7 : i + 9], "big")
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + int.from_bytes(data[i + 2 : i + 4], "big")
    return None


def canvas_records(manifest: dict) -> list[dict]:
    records = []
    for seq, canvas in enumerate(manifest["items"], start=1):
        body = canvas["items"][0]["items"][0]["body"]
        service = body["service"][0]
        service_id = service.get("@id") or service.get("id")
        label = _label_text(canvas.get("label"))
        records.append(
            {
                "seq": seq,
                "label": label,
                "service": service_id,
                "canvas_width": canvas.get("width"),
                "canvas_height": canvas.get("height"),
                "file": f"{seq:03d}_{_slug(label)}.jpg",
            }
        )
    return records


def crawl() -> int:
    SCANS_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = SCANS_ROOT / "manifest.json"
    if not manifest_path.exists():
        manifest_path.write_bytes(_get(MANIFEST_URL))
        time.sleep(FETCH_DELAY_S)
    manifest = json.loads(manifest_path.read_text())
    records = canvas_records(manifest)
    print(f"{len(records)} canvases in manifest")

    mismatches = 0
    with open(SCANS_ROOT / "index.jsonl", "w") as index:
        for record in records:
            dest = SCANS_ROOT / record["file"]
            if not dest.exists():
                url = f"{record['service']}/full/full/0/default.jpg"
                dest.write_bytes(_get(url))
                time.sleep(FETCH_DELAY_S)
            dims = jpeg_dimensions(dest)
            record["file_width"], record["file_height"] = dims or (None, None)
            record["dims_ok"] = dims == (record["canvas_width"], record["canvas_height"])
            if not record["dims_ok"]:
                mismatches += 1
                print(f"  DIMENSION MISMATCH {record['file']}: canvas "
                      f"{record['canvas_width']}x{record['canvas_height']}, file {dims}")
            index.write(json.dumps(record) + "\n")
            if record["seq"] % 10 == 0:
                print(f"  {record['seq']}/{len(records)} done")

    print(f"crawl complete: {len(records)} images, {mismatches} dimension mismatches")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(crawl())
