"""E4 — root<->leaf: masked positive or real null? (i02, critique C4)

i01 (T2.6) concluded the herbal has NO real-taxa cross-organ bundle because
root_type x leaf_shape was non-significant (Cramer's V 0.256, p 0.26). The C4
critic objected: root_type is ~35% inter-annotator-noisy, which ATTENUATES the
association toward null, and the CLEAN feature root_coloring (~4% noise) *did*
associate with leaf features — buried affirmative evidence.

E4 resolves it two ways:
  (1) Disattenuate the noisy root_type x leaf associations for measurement error
      (reliabilities from the QA disagreement rates). Approximate for categorical
      data — reported with that caveat, not leaned on.
  (2) THE CLEAN TEST (leaned on): test every clean root-region feature
      (root_coloring, low noise) x every leaf-region feature with permutation.
      A significant clean cross-organ association IS a real-taxa-like feature
      bundle that root_type's noise could not show — overturning the i01 null.

Cross-references E3: the disattenuated root x leaf estimate sits near the E3
minimum detectable effect (phi~0.4), i.e. exactly in the power gap where a real
moderate bundle would be missed at page level.

Usage:
    python -m ms408.experiments.e4_root_leaf
"""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..studies.referential_realism import _herbal_feature_table, association_test

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
REPORTS_DIR = ROOT / "reports"
SEED = 408

# per-field inter-annotator DISAGREEMENT rates from the G2 QA (results/annotations
# /t13_qa.json); reliability = 1 - disagreement.
DISAGREEMENT = {
    "root_type": 0.35, "leaf_arrangement": 0.35, "leaf_shape": 0.27,
    "root_coloring": 0.04, "leaf_count_band": 0.15,
}
ROOT_FEATURES = ("root_type", "root_coloring")
LEAF_FEATURES = ("leaf_shape", "leaf_arrangement", "leaf_count_band")


def _reliability(field: str) -> float:
    return 1.0 - DISAGREEMENT.get(field, 0.0)


def _disattenuate(v: float, fx: str, fy: str) -> float:
    """Approximate correction of an observed association for measurement error.
    Standard for correlations; applied to Cramer's V as an order-of-magnitude
    guide only (categorical disattenuation is not exact)."""
    denom = math.sqrt(_reliability(fx) * _reliability(fy))
    return round(v / denom, 4) if denom else v


def run() -> dict:
    annotations = [json.loads(line) for line in
                   (ROOT / "results" / "annotations" / "t13_annotations.jsonl")
                   .read_text().splitlines() if line.strip()]
    table, n = _herbal_feature_table(annotations)

    seed = SEED
    pairs = {}
    for rf in ROOT_FEATURES:
        for lf in LEAF_FEATURES:
            seed += 1
            res = association_test(table[rf], table[lf], seed)
            res["disattenuated_v"] = _disattenuate(res["cramers_v"], rf, lf)
            res["root_feature"] = rf
            res["leaf_feature"] = lf
            res["root_reliability"] = round(_reliability(rf), 2)
            pairs[f"{rf} x {lf}"] = res

    clean_pairs = {k: v for k, v in pairs.items()
                   if v["root_feature"] == "root_coloring"}
    clean_significant = [k for k, v in clean_pairs.items() if v["constrained"]]
    noisy_pairs = {k: v for k, v in pairs.items() if v["root_feature"] == "root_type"}

    cross_organ_bundle_exists = len(clean_significant) >= 1

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E4 — root<->leaf masked positive",
        "herbal_pages": n,
        "pairs": pairs,
        "clean_root_coloring_significant_with": clean_significant,
        "cross_organ_bundle_exists": bool(cross_organ_bundle_exists),
    }
    results["verdict"], results["grade"] = _verdict(results, clean_pairs, noisy_pairs)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e4_root_leaf.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "e4_root_leaf.md").write_text(_render(results))
    return results


def _verdict(r: dict, clean_pairs: dict, noisy_pairs: dict) -> tuple:
    if r["cross_organ_bundle_exists"]:
        sig = ", ".join(r["clean_root_coloring_significant_with"])
        rt_leaf = noisy_pairs.get("root_type x leaf_shape", {})
        return (
            f"OVERTURNS the i01 'no cross-organ bundle' null. The CLEAN root-region "
            f"feature root_coloring (~4% noise) associates significantly with leaf "
            f"morphology ({sig}) — a real cross-organ (root-region <-> leaf-region) "
            f"feature bundle that root_type's 35% noise could not show. The i01 "
            f"headline pair root_type x leaf_shape (V {rt_leaf.get('cramers_v')}, "
            f"p {rt_leaf.get('p_associated')}) disattenuates to "
            f"~{rt_leaf.get('disattenuated_v')} — a moderate association sitting "
            f"right at the E3 page-level detection floor (phi~0.4), i.e. a masked "
            f"positive, not a true null. The herbal has cross-organ morphological "
            f"structure after all; the T2.6 'within-organ only' verdict is "
            f"withdrawn. (This does NOT by itself decide real-vs-invented: a "
            f"systematically invented herbal also has bundled features. It removes "
            f"one of the three legs i01 leaned against the referential-herbal "
            f"reading.)", "B")
    return (
        "The i01 null STANDS on firmer ground: even the clean root_coloring feature "
        "does not associate with leaf morphology after permutation testing, so the "
        "absence of a cross-organ bundle is not a measurement-noise artifact.", "B")


def _render(r: dict) -> str:
    lines = [
        "# E4 — root<->leaf: masked positive or real null?",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e4_root_leaf`. Numbers in "
        "`results/experiments/e4_root_leaf.json`.",
        "",
        f"{r['herbal_pages']} herbal pages. Root-region × leaf-region associations, "
        "raw and disattenuated for inter-annotator noise (reliability = 1 − QA "
        "disagreement). The clean feature (root_coloring, ~4% noise) carries the "
        "affirmative test; disattenuation of the noisy root_type is an approximate "
        "guide only.",
        "",
        "| pair | root reliability | raw V | disattenuated V | p | significant |",
        "|---|---|---|---|---|---|",
    ]
    for name, v in r["pairs"].items():
        lines.append(
            f"| {name} | {v['root_reliability']} | {v['cramers_v']} "
            f"| {v['disattenuated_v']} | {v['p_associated']} "
            f"| {'YES' if v['constrained'] else 'no'} |"
        )
    lines += [
        "",
        f"- Clean root_coloring significant with: "
        f"**{r['clean_root_coloring_significant_with'] or 'none'}**.",
        f"- Cross-organ bundle exists: **{r['cross_organ_bundle_exists']}**.",
        "",
        f"## Verdict [{r['grade']}, pending refutation pass]",
        "",
        r["verdict"],
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    for name, v in out["pairs"].items():
        print(f"{name:34s} V={v['cramers_v']:.3f} disatt={v['disattenuated_v']:.3f} "
              f"p={v['p_associated']:.4f} sig={v['constrained']}")
    print(f"cross-organ bundle exists: {out['cross_organ_bundle_exists']}")
    print(f"grade {out['grade']}: {out['verdict'][:110]}...")
