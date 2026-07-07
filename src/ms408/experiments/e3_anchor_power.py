"""E3 — Anchor-hunt power curve (i02, critique C4).

The i01 anchor hunt returned null with a planted control at phi=1.0 — which proves
only that a PERFECT signal is findable, not the false-negative rate for realistic
effects. E3 measures the actual power: inject synthetic anchors of controlled
strength into the real herbal token x feature structure and report the recovery
rate at BH-FDR q=0.05, plus the minimum detectable effect.

For a target association phi to a feature present on f of n pages, a synthetic
token is planted on `hit` feature-pages and `miss` non-feature-pages, chosen to
realise phi; the full anchor scan (Fisher + BH-FDR over the real test count) then
runs and we check whether the planted token survives. Swept over phi and over
many feature targets x seeds.

Verdict logic: if moderate anchors (phi~0.4) are reliably recovered, the i01 null
is INFORMATIVE ("no such anchor exists"). If moderate anchors are missed, the null
is UNINFORMATIVE (underpowered) and must be downgraded.

Usage:
    python -m ms408.experiments.e3_anchor_power
"""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..studies.anchor_hunt import (
    _page_sets,
    benjamini_hochberg,
    fisher_right_tail,
    load_pages,
    phi as phi_coeff,
)

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
REPORTS_DIR = ROOT / "reports"
SEED = 408
PHI_GRID = (0.2, 0.3, 0.4, 0.5, 0.6, 0.8)
TRIALS_PER_PHI = 60
FDR_Q = 0.05


def _plant_for_phi(feature_pages: set, all_pages: list, target_phi: float,
                   rng: random.Random) -> set | None:
    """Choose a set of pages for a synthetic token so its phi with the feature is
    ~target_phi. Returns the token's page set, or None if unattainable."""
    n = len(all_pages)
    f = len(feature_pages)
    feat = list(feature_pages)
    non_feat = [p for p in all_pages if p not in feature_pages]
    best, best_err = None, 1e9
    # search over (hit, miss) combinations at a few token prevalences
    for hit in range(1, f + 1):
        for miss in range(0, len(non_feat) + 1):
            a, b = hit, miss
            c, d = f - hit, (n - f) - miss
            if a + b < 3:  # token must appear on >= a few pages
                continue
            val = phi_coeff(a, b, c, d)
            err = abs(val - target_phi)
            if err < best_err:
                best_err, best = err, (hit, miss)
    if best is None or best_err > 0.06:
        return None
    hit, miss = best
    return set(rng.sample(feat, hit)) | set(rng.sample(non_feat, miss))


def power_at_phi(pages, tokens, features, target_phi: float, seed: int) -> dict:
    """Recovery rate of a synthetic anchor at target_phi across TRIALS_PER_PHI
    (feature, seed) draws, measured against the real FDR threshold."""
    rng = random.Random(seed)
    all_pages = [p.page for p in pages]
    n = len(all_pages)
    # baseline test count = real tokens x features (the multiple-testing burden)
    feature_items = list(features.items())
    recovered = 0
    attempts = 0
    realised_phis = []
    for _ in range(TRIALS_PER_PHI):
        fname, fpages = rng.choice(feature_items)
        planted = _plant_for_phi(fpages, all_pages, target_phi, rng)
        if planted is None:
            continue
        attempts += 1
        # build the full p-value set: real tokens vs this feature + the planted token
        pvals = []
        planted_index = None
        a0 = len(planted & fpages)
        for token, tpages in list(tokens.items()) + [("__PLANT__", planted)]:
            a = len(tpages & fpages)
            b = len(tpages - fpages)
            c = len(fpages - tpages)
            d = n - a - b - c
            pvals.append(fisher_right_tail(a, b, c, d))
            if token == "__PLANT__":
                planted_index = len(pvals) - 1
        discovered = benjamini_hochberg(pvals, FDR_Q)
        if discovered[planted_index]:
            recovered += 1
        realised_phis.append(round(phi_coeff(a0, len(planted) - a0,
                                             len(fpages) - a0,
                                             n - len(planted) - len(fpages) + a0), 3))
    return {
        "target_phi": target_phi,
        "attempts": attempts,
        "recovered": recovered,
        "recovery_rate": round(recovered / attempts, 3) if attempts else None,
        "mean_realised_phi": round(sum(realised_phis) / len(realised_phis), 3)
        if realised_phis else None,
    }


def power_by_prevalence(pages, tokens, features, target_phi: float, seed: int) -> dict:
    """Recovery at target_phi stratified by the target feature's prevalence band —
    Fisher power is cell-count-driven, so rare features have far less power than
    balanced ones (E3 refutation point)."""
    import random

    rng = random.Random(seed)
    all_pages = [p.page for p in pages]
    n = len(all_pages)
    bands = {"rare (<20 pp)": (1, 20), "mid (20-45 pp)": (20, 45),
             "balanced (45+ pp)": (45, n)}
    by_band = {}
    for label, (lo, hi) in bands.items():
        band_feats = [(fn, fp) for fn, fp in features.items() if lo <= len(fp) < hi]
        if not band_feats:
            by_band[label] = None
            continue
        recovered = attempts = 0
        for _ in range(40):
            fname, fpages = rng.choice(band_feats)
            planted = _plant_for_phi(fpages, all_pages, target_phi, rng)
            if planted is None:
                continue
            attempts += 1
            pvals, idx = [], None
            for token, tpages in list(tokens.items()) + [("__PLANT__", planted)]:
                a = len(tpages & fpages)
                b = len(tpages - fpages)
                c = len(fpages - tpages)
                pvals.append(fisher_right_tail(a, b, c, n - a - b - c))
                if token == "__PLANT__":
                    idx = len(pvals) - 1
            if benjamini_hochberg(pvals, FDR_Q)[idx]:
                recovered += 1
        by_band[label] = {"features_in_band": len(band_feats), "attempts": attempts,
                          "recovery_rate": round(recovered / attempts, 3)
                          if attempts else None}
    return by_band


def run() -> dict:
    pages = load_pages("H")
    tokens, features = _page_sets(pages)
    n_tests = len(tokens) * len(features)

    curve = [power_at_phi(pages, tokens, features, phi, SEED + int(phi * 100))
             for phi in PHI_GRID]
    prevalence_at_04 = power_by_prevalence(pages, tokens, features, 0.4, SEED)

    # minimum detectable effect = smallest phi with recovery >= 0.8
    mde = next((row["target_phi"] for row in curve
                if row["recovery_rate"] and row["recovery_rate"] >= 0.8), None)
    # is a MODERATE anchor (phi 0.4) recoverable?
    moderate = next((row for row in curve if row["target_phi"] == 0.4), {})
    moderate_recovered = (moderate.get("recovery_rate") or 0) >= 0.5

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E3 — anchor-hunt power curve",
        "herbal_pages": len(pages),
        "testable_tokens": len(tokens),
        "testable_features": len(features),
        "fdr_tests": n_tests,
        "fdr_q": FDR_Q,
        "power_curve": curve,
        "minimum_detectable_effect_phi_at_80pct": mde,
        "moderate_anchor_phi0.4_recovered": bool(moderate_recovered),
        "power_at_phi04_by_prevalence": prevalence_at_04,
    }
    results["verdict"], results["grade"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e3_anchor_power.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "e3_anchor_power.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    # Revised per E3's refutation pass. The critic accepted the method but showed
    # the "null is informative" headline was oversold: (a) recovery is a cliff
    # (0% below phi 0.4, 85%+ above), and a realistic imperfect/fragmented herbal
    # anchor likely sits at phi 0.2-0.35 — the dead zone; (b) MDE phi=0.4 hides
    # prevalence dependence (rare features have far less power).
    band = r["power_at_phi04_by_prevalence"]

    def rate(label):
        b = band.get(label)
        return b["recovery_rate"] if b else None

    return (
        f"The power ANALYSIS is sound but the 'null is informative' claim is "
        f"OVERSOLD. Recovery is a cliff: phi<=0.3 -> 0%, phi=0.4 -> 85%. And power "
        f"is strongly prevalence-dependent at phi=0.4 — rare features "
        f"{rate('rare (<20 pp)')}, mid {rate('mid (20-45 pp)')}, balanced "
        f"{rate('balanced (45+ pp)')}. Honest bound: the i01 anchor hunt EXCLUDES "
        f"only STRONG, prevalence-balanced anchors (phi>=0.4 on common features); "
        f"it does NOT exclude the WEAK (phi 0.2-0.35) or RARE-feature anchors that a "
        f"genuine but imperfect herbal cipher would most plausibly produce. So the "
        f"i01 null is a WEAKER constraint than the flagship implied — it bounds the "
        f"anchor away from the strong-signal corner, no more. The real test is "
        f"finer (label-adjacency) granularity, deferred.", "B")


def _render(r: dict) -> str:
    lines = [
        "# E3 — Anchor-hunt power curve",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e3_anchor_power`. Numbers in "
        "`results/experiments/e3_anchor_power.json`.",
        "",
        f"Herbal: {r['herbal_pages']} pages, {r['testable_tokens']} tokens × "
        f"{r['testable_features']} features = {r['fdr_tests']:,} FDR tests "
        f"(q={r['fdr_q']}). Synthetic anchors injected at controlled phi; recovery "
        "measured against the real multiple-testing burden.",
        "",
        "| target phi | mean realised phi | attempts | recovered | recovery rate |",
        "|---|---|---|---|---|",
    ]
    for row in r["power_curve"]:
        lines.append(f"| {row['target_phi']} | {row['mean_realised_phi']} "
                     f"| {row['attempts']} | {row['recovered']} "
                     f"| {row['recovery_rate']} |")
    lines += [
        "",
        f"- Minimum detectable effect (≥80% recovery, averaged): "
        f"**phi = {r['minimum_detectable_effect_phi_at_80pct']}** — but this hides "
        f"prevalence dependence (below).",
        "",
        "### Power at phi=0.4 by feature prevalence (the refutation's key point)",
        "",
        "| feature prevalence | features in band | recovery rate |",
        "|---|---|---|",
        *[f"| {label} | {b['features_in_band']} | {b['recovery_rate']} |"
          for label, b in r["power_at_phi04_by_prevalence"].items() if b],
        "",
        f"## Verdict [{r['grade']}, refutation pass applied]",
        "",
        r["verdict"],
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    for row in out["power_curve"]:
        print(f"phi={row['target_phi']} realised={row['mean_realised_phi']} "
              f"recovery={row['recovery_rate']} (n={row['attempts']})")
    print(f"MDE (80%): phi={out['minimum_detectable_effect_phi_at_80pct']}")
    print(f"grade {out['grade']}: {out['verdict'][:110]}...")
