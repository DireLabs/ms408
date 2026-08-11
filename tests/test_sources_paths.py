"""Tests for data-root resolution (ms408.sources.data_home).

These guard the packaging contract: a repo checkout keeps using the repo's own data/,
while a wheel install resolves to a writable user directory instead of site-packages'
parent. Data-free — no acquired corpus needed.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ms408.sources import DATA_HOME, RAW_ROOT, data_home

REPO_ROOT = Path(__file__).resolve().parents[1]

# data_home() is called as a function rather than re-imported, so these tests never
# reload the module: DATA_HOME (and dataset.PROCESSED_ROOT, bound from it at import)
# stay exactly as the rest of the suite found them, in any test order.


def test_env_override_wins(monkeypatch, tmp_path):
    monkeypatch.setenv("MS408_DATA_HOME", str(tmp_path / "custom"))
    assert data_home() == (tmp_path / "custom").resolve()


@pytest.mark.skipif(
    not (REPO_ROOT / "pyproject.toml").is_file(), reason="not a source checkout"
)
def test_checkout_uses_repo_data(monkeypatch):
    """From a source checkout the documented repo layout is unchanged."""
    monkeypatch.delenv("MS408_DATA_HOME", raising=False)
    assert data_home() == REPO_ROOT / "data"


def test_wheel_install_falls_back_to_user_data_dir(monkeypatch, tmp_path):
    """With no repo above the package, resolve under XDG_DATA_HOME — not site-packages.

    This is the regression: the old `parents[2]` walk pointed inside the installed
    package's parent, so `python -m ms408.acquire` (the README quickstart) died with
    PermissionError. Simulated by pointing the repo probe at a directory tree with no
    pyproject.toml in it.
    """
    monkeypatch.delenv("MS408_DATA_HOME", raising=False)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))
    fake_pkg = tmp_path / "site-packages" / "ms408" / "sources.py"
    fake_pkg.parent.mkdir(parents=True)
    fake_pkg.touch()
    monkeypatch.setattr("ms408.sources.__file__", str(fake_pkg))
    assert data_home() == (tmp_path / "xdg" / "ms408").resolve()


def test_resolved_root_is_creatable(monkeypatch, tmp_path):
    """Whatever the resolution, acquire() must be able to create its target."""
    monkeypatch.setenv("MS408_DATA_HOME", str(tmp_path / "acq"))
    raw = data_home() / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    assert raw.is_dir()


def test_module_constants_agree():
    assert RAW_ROOT == DATA_HOME / "raw"
