from ms408.synthesis.narratives import GRADE_WEIGHT, tally
from ms408.synthesis.registry import NARRATIVES, build_findings


def test_registry_builds_from_results():
    findings = build_findings()
    assert len(findings) >= 13
    # every finding cites a source and a valid grade
    for f in findings:
        fd = f.__dict__ if hasattr(f, "__dict__") else f
        assert fd["source"]
        assert fd["grade"] in GRADE_WEIGHT
        # every support/undercut references a real narrative id
        for nid in list(fd["supports"]) + list(fd["undercuts"]):
            assert nid in NARRATIVES


def test_findings_carry_computed_numbers():
    findings = {f.id: f for f in build_findings()}
    # the load-bearing anchor null must reflect the real gate result
    anchor = findings["F9-anchor-hunt-null"]
    assert anchor.value["gate_passed"] is True
    assert anchor.value["admissible_anchors"] == 0
    # cipher word-order erasure vs VMS
    cipher = findings["F5-cipher-erases-wordorder"]
    assert cipher.value["cipher_mz"] < cipher.value["vms_mz"]


def test_tally_grade_weighting():
    findings = [f.__dict__ for f in build_findings()]
    t = tally(findings, "N-conlang")
    assert t["support_weight"] > 0
    assert t["net"] == t["support_weight"] - t["undercut_weight"]
    # conlang is supported and never undercut in the registry
    assert t["undercut_weight"] == 0


def test_natural_reading_is_undercut_by_the_nulls():
    findings = [f.__dict__ for f in build_findings()]
    t = tally(findings, "N-natural")
    undercut_ids = {f["id"] for f in t["undercut"]}
    assert {"F9-anchor-hunt-null", "F10-labels-not-naming",
            "F11-no-root-leaf-bundle"} <= undercut_ids
