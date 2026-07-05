import pytest

from ms408.scanmap import build_scan_map, label_sides, page_base
from ms408.scans import SCANS_ROOT

needs_scans = pytest.mark.skipif(
    not (SCANS_ROOT / "index.jsonl").exists(), reason="run `python -m ms408.scans` first"
)


def test_page_base():
    assert page_base("f1r") == "1r"
    assert page_base("f70r2") == "70r"
    assert page_base("f86v4") == "86v"
    assert page_base("fRos") is None


def test_label_sides():
    assert label_sides("1r") == {"1r"}
    assert label_sides("69v and 70r") == {"69v", "70r"}
    assert label_sides("85r (part) 86v (part) (part of 85-86 foldout)") == {"85r", "86v"}
    assert label_sides("[Front cover]") == set()


@needs_scans
def test_every_page_has_a_scan(tmp_path):
    scan_map = build_scan_map(out_path=tmp_path / "scan_map.json")
    assert scan_map["stats"]["pages_unmapped"] == 0

    # simple folios map exactly 1:1
    f1r = scan_map["pages"]["f1r"]
    assert len(f1r["files"]) == 1 and not f1r["ambiguous"]

    # the rosettes page maps to the 85v/86r foldout canvas
    ros = scan_map["pages"]["fRos"]
    assert len(ros["files"]) == 1
    assert "85v" in ros["files"][0]

    # unmatched canvases are only non-text shots (bracketed labels: covers, edges)
    assert all("_" in f for f in scan_map["unmatched_canvases"])
    assert scan_map["stats"]["canvases_unmatched"] <= 12
