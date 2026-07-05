import json

import pytest

from ms408.dataset import DATASET_VERSION, build
from ms408.sources import path_for

needs_data = pytest.mark.skipif(
    not path_for("zl").exists(), reason="run `python -m ms408.acquire` first"
)


@needs_data
def test_build_roundtrip(tmp_path):
    manifest = build(out_root=tmp_path)

    assert manifest["dataset_version"] == DATASET_VERSION
    assert manifest["counts"]["zl"] == {"pages": 227, "loci": 5385}
    assert manifest["counts"]["gc"] == {"pages": 226, "loci": 5367}
    for source in manifest["sources"].values():
        assert source["sha256"] == source["pinned_sha256"]

    with open(tmp_path / "pages_zl.jsonl") as f:
        pages = [json.loads(line) for line in f]
    assert len(pages) == 227
    f1r = pages[0]
    assert f1r["page"] == "f1r"
    assert f1r["illustration"] == "T"
    assert f1r["currier_language"] == "A"
    assert f1r["hand"] == "1"
    assert f1r["loci"][0]["num"] == 1
    assert (tmp_path / "manifest.json").exists()
