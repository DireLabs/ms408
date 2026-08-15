"""Guard the shipped per-experiment results tier (D22, L19).

`.gitignore` excludes `results/experiments/*.json` and then allow-lists individual files
that `scripts/audit_results_tier.py` has cleared as metrics-only. This re-runs that audit
in CI over whatever is actually committed, so a regenerated file that starts embedding
third-party corpus text fails the build instead of shipping.

The audit needs the acquired corpora to build its vocabularies, so it skips cleanly
without them — but the cheap structural checks below always run.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

from ms408.sources import path_for

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "experiments"

needs_data = pytest.mark.skipif(
    not path_for("zl").exists(), reason="run `python -m ms408.acquire` first"
)


def _audit_module():
    spec = importlib.util.spec_from_file_location(
        "audit_results_tier", ROOT / "scripts" / "audit_results_tier.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tracked_results() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "results/experiments"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return [ROOT / p for p in out if p.endswith(".json")]


def test_tracked_results_exist_and_are_json():
    """Every allow-listed file must actually be present and parseable."""
    tracked = _tracked_results()
    assert tracked, "no experiment results are shipped — the allow-list is empty"
    for p in tracked:
        assert p.exists(), p
        json.loads(p.read_text())


def test_tracked_results_carry_provenance():
    """L3: a shipped result must record what produced it, and when, and at which commit.

    Two shapes are in use — provenance at the top level (`built_at` / `git_commit` /
    `experiment`) or nested under `meta` (`script` / `git_commit` / `built_at`). Accept
    either, but require a build stamp, a commit, and something naming the producer.
    """
    for p in _tracked_results():
        data = json.loads(p.read_text())
        meta = data["meta"] if isinstance(data.get("meta"), dict) else data
        assert meta.get("git_commit"), f"{p.name} records no git commit"
        assert meta.get("built_at") or meta.get("generated_at"), f"{p.name} has no build stamp"
        assert meta.get("script") or meta.get("experiment"), f"{p.name} names no producer"


@needs_data
def test_tracked_results_contain_no_third_party_text():
    """The L19 guard: no running corpus text, no redistributed vocabulary slice."""
    audit = _audit_module()
    vms, _ = audit._vms_vocab()
    naibbe, _ = audit._naibbe_vocab()
    vocabs = {"vms_transliteration": vms, "naibbe": naibbe}
    assert vms, "VMS vocabulary is empty — the audit would pass vacuously"

    offenders = {}
    for p in _tracked_results():
        result = audit.audit_file(p, vocabs)
        if result["verdict"] != "METRICS_ONLY":
            offenders[p.name] = result["examples"]
    assert not offenders, (
        "shipped results embed third-party corpus text; remove them from the "
        f".gitignore allow-list or strip the text: {json.dumps(offenders, indent=2)}"
    )


@needs_data
def test_audit_detects_planted_corpus_text(tmp_path):
    """Mutation check: an audit that never fires would pass everything vacuously."""
    audit = _audit_module()
    vms, _ = audit._vms_vocab()
    vocabs = {"vms_transliteration": vms}

    from ms408.experiments.e13_function_content import _vms_tokens

    tokens = _vms_tokens("A")
    planted = {
        "running_text": {"excerpt": " ".join(tokens[:40])},
        "vocabulary_slice": {"types": sorted(set(tokens[:400]))},
        "keyed_by_type": {"freqs": {w: 1 for w in sorted(set(tokens[:400]))}},
    }
    for name, payload in planted.items():
        p = tmp_path / f"{name}.json"
        p.write_text(json.dumps(payload))
        assert audit.audit_file(p, vocabs)["verdict"] == "CONTAINS_CORPUS_TEXT", name

    clean = tmp_path / "clean.json"
    clean.write_text(json.dumps({"h2": 2.18, "grade": "C", "axes": ["h2", "ed1"]}))
    assert audit.audit_file(clean, vocabs)["verdict"] == "METRICS_ONLY"
