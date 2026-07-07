"""Findings registry (T3.1) — deterministic aggregation of Phase-2 results.

Pulls the load-bearing numbers from results/*.json into one machine-readable
registry, so the competing-narratives synthesis cites code-computed values (L3
firewall) rather than restating them from memory. Each finding carries a stable
id, the value(s), the producing result file, and an evidence grade.

Usage:
    python -m ms408.synthesis.registry
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "results"
OUT = RESULTS / "synthesis" / "findings_registry.json"


def _load(rel: str) -> dict:
    return json.loads((RESULTS / rel).read_text())


@dataclass
class Finding:
    id: str
    statement: str
    value: object
    source: str  # results file
    grade: str  # A-D per RESEARCH-PLAN §6
    supports: list = field(default_factory=list)  # narrative ids this raises
    undercuts: list = field(default_factory=list)  # narrative ids this lowers


def build_findings() -> list:
    rep = _load("replication/replication.json")
    bench = _load("harness/benchmark.json")
    enc = _load("studies/encoding_bracket.json")
    top = _load("studies/topics.json")
    morph = _load("studies/morphology.json")
    anchor = _load("studies/anchor_hunt.json")
    labels = _load("studies/anchor_labels.json")
    real = _load("studies/referential_realism.json")

    def enc_profile(name, metric):
        return enc["profiles"][name][metric]

    vms_h2 = rep["lb_entropy"]["it_full"]["h2"]
    findings = [
        Finding(
            "F1-entropy-anomaly",
            "Voynichese conditional character entropy h2 is far below natural "
            "language and replicates published values.",
            {"vms_h2": vms_h2,
             "natural_language_range": [bench["corpora"]["h4_latin_vulgate"]["metrics"]["h2"],
                                        bench["corpora"]["h4_hebrew_mishneh_torah_consonantal"]["metrics"]["h2"]]},
            "replication/replication.json", "A",
            supports=["N-cipher", "N-conlang", "N-null", "N-invented"],
        ),
        Finding(
            "F2-currier-ab",
            "The manuscript is two statistically distinct systems (Currier A/B), "
            "recovered from word co-occurrence alone.",
            {"js_divergence_A_vs_B": rep["currier_split"]["js_divergence_A_vs_B"],
             "within_dialect": [rep["currier_split"]["js_divergence_within_A"],
                                rep["currier_split"]["js_divergence_within_B"]],
             "two_cluster_ARI_v101": top["gc_v101"]["two_largest_clusters_vs_currier"]["ari"]},
            "replication + topics", "A",
            supports=["N-cipher", "N-conlang", "N-natural"],
        ),
        Finding(
            "F3-positional-structure",
            "Strong positional constraints: paragraph-initial gallows enrichment, "
            "line-final m concentration — 'the line is a functional unit'.",
            {"pf_share_paragraph_initial": rep["positional"]["pf_share_in_paragraph_initial_lines"],
             "m_share_line_final": rep["positional"]["m_share_line_final"]},
            "replication/replication.json", "A",
            supports=["N-conlang", "N-null", "N-invented"],
            undercuts=["N-cipher"],
        ),
        Finding(
            "F4-mz-word-order-info",
            "The manuscript carries topic-scale word-order information at a "
            "natural-language scale (Montemurro-Zanette).",
            {"peak_delta_bits": enc_profile("vms", "mz_peak_value"),
             "peak_scale": enc_profile("vms", "mz_peak_scale")},
            "studies/encoding_bracket.json", "B",
            supports=["N-cipher", "N-conlang", "N-natural", "N-invented"],
            undercuts=["N-null"],
        ),
        Finding(
            "F5-cipher-erases-wordorder",
            "Homophonic verbose cipher matches character structure but ERASES the "
            "word-order information the VMS has (dI 0.000 vs 0.307).",
            {"cipher_mz": enc_profile("verbose_cipher", "mz_peak_value"),
             "vms_mz": enc_profile("vms", "mz_peak_value")},
            "studies/encoding_bracket.json + p1_variants", "B",
            undercuts=["N-cipher"],
        ),
        Finding(
            "F6-selfcitation-overshoots",
            "Self-citation (null hypothesis) overshoots word-order info at the "
            "wrong scale and runs too small a vocabulary.",
            {"selfcite_mz": enc_profile("selfcitation", "mz_peak_value"),
             "selfcite_ttr": enc_profile("selfcitation", "type_token_ratio"),
             "vms_ttr": enc_profile("vms", "type_token_ratio")},
            "studies/encoding_bracket.json", "B",
            undercuts=["N-null"],
        ),
        Finding(
            "F7-no-family-full-profile",
            "No encoding family reproduces the VMS's full profile (low h2 AND "
            "intact word-order info together).",
            {"ordering": list(enc["scorecard"].keys()),
             "distances": {k: v["distance"] for k, v in enc["scorecard"].items()}},
            "studies/encoding_bracket.json", "B",
            undercuts=["N-cipher", "N-null", "N-abbreviation"],
        ),
        Finding(
            "F8-section-alignment-A-only",
            "Text co-varies with illustration sections in Language A only; "
            "Language B is textually homogeneous across its sections.",
            {"within_A_section_ARI": top["zl"]["within_dialect_section_alignment"].get("A", {}).get("ari"),
             "within_B_section_ARI": top["zl"]["within_dialect_section_alignment"].get("B", {}).get("ari")},
            "studies/topics.json", "B",
            supports=["N-natural", "N-invented"],
        ),
        Finding(
            "F9-anchor-hunt-null",
            "No Voynichese token anchors to a herbal visual feature after FDR "
            "(harness gate passed).",
            {"admissible_anchors": len(anchor["anchors"]),
             "gate_passed": anchor["harness_gate"]["passed"]},
            "studies/anchor_hunt.json", "B",
            undercuts=["N-natural"],
        ),
        Finding(
            "F10-labels-not-naming",
            "Illustration labels are not a naming system: labels recur across "
            "pages LESS than running text; herbal near label-free.",
            {"pharma_label_ttr": labels["recurrence_tests"]["P"]["label_type_token_ratio"],
             "pharma_recurring": labels["recurrence_tests"]["P"]["label_types_recurring_2plus"],
             "pharma_null_band": labels["recurrence_tests"]["P"]["null_recurrence_band_95"],
             "herbal_label_pages": labels["label_census"]["H"]["label_bearing_pages"]},
            "studies/anchor_labels.json", "B",
            undercuts=["N-natural"],
        ),
        Finding(
            "F11-no-root-leaf-bundle",
            "The herbal shows no real-taxa root<->leaf feature bundle "
            "(root_type x leaf_shape independent); structure is within-organ only.",
            {"verdict": real["referential_realism"]["verdict"],
             "root_leaf": real["referential_realism"]["cross_organ_root_leaf"]},
            "studies/referential_realism.json", "B",
            undercuts=["N-natural"],
        ),
        Finding(
            "F12-morphology-paradigmatic",
            "Voynichese is a dense, position-constrained, paradigmatic morphology "
            "unlike natural language; a paradigmatic conlang reproduces the full "
            "profile (p1-variant V3).",
            {"vms_ed1": morph["corpora"]["zl_all"]["ed1_network"]["main_component_share"],
             "h4_latin_ed1": morph["corpora"]["h4_latin"]["ed1_network"]["main_component_share"]},
            "studies/morphology.json + p1_variants", "B",
            supports=["N-conlang", "N-null"],
        ),
        Finding(
            "F13-anachronism-null",
            "No annotated feature encodes information exceeding 15th-century "
            "observational capability (W7 anachronism scan).",
            {"result": real["anachronism_scan"]["result"]},
            "studies/referential_realism.json", "C",
            undercuts=["N-et-anachronism"],
        ),
    ]
    return findings


NARRATIVES = {
    "N-cipher": "Verbose/substitution cipher of a real plaintext",
    "N-conlang": "A-priori constructed language (Lingua-Ignota class)",
    "N-null": "Meaningless glossolalia / self-citation (elaborate hoax)",
    "N-natural": "Genuine natural-language herbal/reference work, labelled",
    "N-invented": "Meaningful record of an invented world (Codex-Seraphinianus class)",
    "N-abbreviation": "Abbreviated/shorthand natural language",
    "N-et-anachronism": "Content exceeding period capability (W7 hard signature)",
}


def build() -> dict:
    findings = build_findings()
    registry = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "narratives": NARRATIVES,
        "findings": [asdict(f) for f in findings],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(registry, indent=2) + "\n")
    return registry


if __name__ == "__main__":
    reg = build()
    print(f"{len(reg['findings'])} findings across {len(reg['narratives'])} narratives")
    for f in reg["findings"]:
        print(f"  [{f['grade']}] {f['id']:28s} +{f['supports']} -{f['undercuts']}")
