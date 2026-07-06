"""Project environment loading.

Reads KEY=VALUE pairs from the repo-root .env (gitignored) into os.environ.
Existing environment variables are never overridden, so shell-exported values
win. Every ms408 module that needs a secret calls require() — no manual
export step is needed as long as .env exists.

For interactive shell use there is also scripts/load-env.sh:
    source scripts/load-env.sh
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env"


def load_env(path: Path = ENV_FILE) -> dict:
    """Parse .env and setdefault into os.environ. Returns the parsed pairs."""
    pairs: dict = {}
    if not path.exists():
        return pairs
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip("'\"")
        pairs[key] = value
        os.environ.setdefault(key, value)
    return pairs


def require(name: str) -> str:
    """Environment variable by name, loading .env first. Raises with guidance."""
    load_env()
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"{name} is not set. Add it to {ENV_FILE} (gitignored) or export it "
            "in your shell (source scripts/load-env.sh)."
        )
    return value
