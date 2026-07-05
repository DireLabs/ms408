"""Fetch and verify pinned external sources (T0.2).

Usage:
    python -m ms408.acquire            # fetch anything missing, verify everything
    python -m ms408.acquire zl gc      # fetch/verify named sources only
    python -m ms408.acquire --verify   # verify only, no network
"""

from __future__ import annotations

import hashlib
import sys
import time
import urllib.request

from .sources import RAW_ROOT, SOURCES, Source, path_for

FETCH_DELAY_S = 1.0  # politeness between requests to the same host


def sha256_of(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(source: Source, force: bool = False) -> str:
    """Download one source if missing (or force), then verify. Returns status."""
    dest = RAW_ROOT / source.dest
    if dest.exists() and not force:
        return verify(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(source.url, headers={"User-Agent": "ms408-research/0.1"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as out:
        out.write(resp.read())
    time.sleep(FETCH_DELAY_S)
    return verify(source)


def verify(source: Source) -> str:
    dest = RAW_ROOT / source.dest
    if not dest.exists():
        return "missing"
    return "ok" if sha256_of(dest) == source.sha256 else "CHECKSUM MISMATCH"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    verify_only = "--verify" in args
    names = [a for a in args if not a.startswith("--")] or list(SOURCES)
    failed = False
    for name in names:
        source = SOURCES[name]
        status = verify(source) if verify_only else fetch(source)
        print(f"{name:14s} {status:18s} {path_for(name)}")
        if status != "ok":
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
