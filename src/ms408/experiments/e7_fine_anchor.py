"""E7 — Fine-granularity anchor hunt (i03; closes the E3 weak/rare-anchor gap).

E3 showed the i01 page-level anchor hunt excludes only STRONG, prevalence-balanced
anchors (φ≥0.4 on common features): recovery cliffs to 0% at φ≤0.3, and rare-feature
power is ~0.72. Two follow-ups were flagged: finer granularity, and the weak/rare
regime. E7 runs both — with an important negative en route.

Finding 0 — LABEL ANCHORING IS INFEASIBLE ON HERBAL. The i01/E3 "higher-power
label-adjacency" idea (a label token next to a feature) cannot run on the herbal
section: across the 129 annotated herbal pages there are only ~20 label token types
and NONE appears on ≥2 pages (herbal labels are page-unique). Cross-page association
needs repeated tokens, so labels give zero testable anchors here. This is a METHOD
limitation (unique names are undetectable by co-occurrence), not evidence about
labelling.

The power gain therefore comes from a GRADED test. E3 used binary "token present on
page," discarding within-page frequency. E7 uses per-page token COUNTS with a
rank-based (Mann–Whitney) association — a strictly more powerful test — restricted to
E3's higher-power mid/rare feature bands, with a matched planted-anchor power curve.

Pass/fail. If the graded higher-power test surfaces a token→feature anchor that
survives BH-FDR AND the granularity-specific power curve says it is not a fluke →
candidate REFERENTIAL signal (weakens the anti-labelled-herbal null; refutation pass
required). If still null at demonstrably higher power → the bound tightens: no anchor
even where E3 said we had the most power.

Usage:
    python -m ms408.experiments.e7_fine_anchor
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..sources import path_for
from ..studies.anchor_hunt import (
    MIN_TOKEN_PAGES,
    WORD_POLICY,
    benjamini_hochberg,
    load_pages,
)

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
SEED = 408
FDR_Q = 0.05
TRIALS = 60
R_GRID = (0.1, 0.2, 0.3, 0.4, 0.5)  # target rank-biserial effect sizes


def _counts_and_labels(section_pages: set):
    """Per-page paragraph-token COUNTS and label-token page-sets, restricted to the
    section's pages (herbal). Label restriction matters: other sections carry many
    repeated labels, so counting them here would spuriously report label anchoring as
    feasible when it is not for the herbal section."""
    zl = IVTFFDocument.load(path_for("zl"))
    para_counts: dict = {}
    label_pages: dict = {}
    for p in zl.pages:
        if p.name not in section_pages:
            continue
        cc: Counter = Counter()
        for loc in p.loci:
            t = loc.locus_type or ""
            toks = [w for w in loc.words(WORD_POLICY) if "@" not in w]
            if t.startswith("P"):
                cc.update(toks)
            elif t.startswith("L"):
                for w in set(toks):
                    label_pages.setdefault(w, set()).add(p.name)
        para_counts[p.name] = cc
    return para_counts, label_pages


def _null_control(page_names, tokens, features, counts, seed, n_perm=50):
    """Permute each feature's page-set to random pages of the same prevalence,
    breaking any token↔feature association, and count BH discoveries per permutation.
    The per-test Mann–Whitney normal approx is anti-conservative on sparse tied
    counts (so individual BH 'discoveries' are unreliable), BUT the permutation
    distribution of the discovery COUNT is a valid calibrated reference: a real count
    inside this null distribution means no anchor excess over chance."""
    gen = np.random.default_rng(seed)
    counts_out = []
    for _ in range(n_perm):
        perm = {f: set(gen.choice(page_names, size=len(s), replace=False).tolist())
                for f, s in features.items()}
        tests = _graded_scan(page_names, tokens, perm, counts)
        counts_out.append(sum(1 for t in tests if t["discovery"]))
    return counts_out


def _mannwhitney_p(x: np.ndarray, y: np.ndarray) -> float:
    """One-sided Mann–Whitney (H1: x stochastically > y), normal approx with tie
    correction. x = counts on feature pages, y = counts on non-feature pages."""
    nx, ny = len(x), len(y)
    if nx == 0 or ny == 0:
        return 1.0
    allv = np.concatenate([x, y])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv), float)
    ranks[order] = np.arange(1, len(allv) + 1)
    # average ranks for ties
    _, inv, counts = np.unique(allv, return_inverse=True, return_counts=True)
    sums = np.zeros(len(counts))
    np.add.at(sums, inv, ranks)
    avg = sums / counts
    ranks = avg[inv]
    r_x = ranks[:nx].sum()
    u_x = r_x - nx * (nx + 1) / 2
    mu = nx * ny / 2
    n = nx + ny
    _, tc = np.unique(allv, return_counts=True)
    tie = (tc**3 - tc).sum()
    sd = np.sqrt(nx * ny / 12 * ((n + 1) - tie / (n * (n - 1)))) if n > 1 else 0.0
    if sd == 0:
        return 1.0
    z = (u_x - mu) / sd
    # one-sided upper-tail p via erfc
    from math import erfc
    return 0.5 * erfc(z / np.sqrt(2))


def _feature_bands(pages: list):
    """Feature page-sets restricted to E3's higher-power MID and RARE bands."""
    n = len(pages)
    feat: dict = {}
    for p in pages:
        for f in p.features:
            feat.setdefault(f, set()).add(p.page)
    mid = {f: s for f, s in feat.items() if 0.20 * n <= len(s) < 0.45 * n}
    rare = {f: s for f, s in feat.items() if 3 <= len(s) < 0.20 * n}
    return mid, rare, n


def _count_vector(tok: str, page_names: list, counts: dict) -> np.ndarray:
    return np.array([counts[p].get(tok, 0) for p in page_names], float)


def _graded_scan(page_names, tokens, features, counts):
    """Mann–Whitney token-count ~ feature over all (token, feature); BH-FDR."""
    names = np.array(page_names)
    tests = []
    for f, fpages in features.items():
        mask = np.array([p in fpages for p in page_names])
        for tok in tokens:
            v = _count_vector(tok, page_names, counts)
            p = _mannwhitney_p(v[mask], v[~mask])
            tests.append({"token": tok, "feature": f, "p": p})
    disc = benjamini_hochberg([t["p"] for t in tests], FDR_Q)
    for t, d in zip(tests, disc):
        t["discovery"] = bool(d)
        t["p"] = round(t["p"], 6)
    _ = names
    return tests


def _power_curve(page_names, real_pvals, features, seed):
    """Plant a graded synthetic anchor of controlled strength on a random feature and
    measure recovery against the REAL multiple-testing burden (the actual test
    p-values as background). Effect is a Poisson count-mean shift on feature pages;
    strength is reported as the realised rank-biserial r."""
    gen = np.random.default_rng(seed)
    fitems = list(features.items())
    out = []
    for r_target in R_GRID:
        shift = 4.0 * r_target  # monotone knob; realised r reported below
        recovered = attempts = 0
        realized = []
        for _ in range(TRIALS):
            _, fpages = fitems[int(gen.integers(len(fitems)))]
            mask = np.array([p in fpages for p in page_names])
            v = gen.poisson(1.0 + shift * mask).astype(float)
            x, y = v[mask], v[~mask]
            wins = float((x[:, None] > y[None, :]).sum()
                         + 0.5 * (x[:, None] == y[None, :]).sum())
            realized.append(2 * wins / (len(x) * len(y)) - 1)
            p_plant = _mannwhitney_p(x, y)
            if benjamini_hochberg(list(real_pvals) + [p_plant], FDR_Q)[-1]:
                recovered += 1
            attempts += 1
        out.append({"r_target": r_target,
                    "mean_realised_r": round(float(np.mean(realized)), 3),
                    "recovery_rate": round(recovered / attempts, 3) if attempts else None})
    return out


def run() -> dict:
    pages = load_pages("H")
    page_names = [p.page for p in pages]
    counts, label_pages = _counts_and_labels(set(page_names))
    label_repeated = sum(1 for s in label_pages.values() if len(s) >= 2)

    mid, rare, n = _feature_bands(pages)
    features = {**mid, **rare}
    # testable tokens: present (count>0) on >= MIN_TOKEN_PAGES pages
    presence = Counter()
    for p in page_names:
        presence.update(set(counts[p]))
    tokens = [t for t, c in presence.items() if c >= MIN_TOKEN_PAGES]

    tests = _graded_scan(page_names, tokens, features, counts)
    discoveries = [t for t in tests if t["discovery"]]
    raw = len(discoveries)
    # NULL GATE (L4): permutation reference for the discovery COUNT. The per-test BH
    # is anti-conservative here, but the count-level permutation test is valid: is the
    # real discovery count in the upper tail of the permuted-null distribution?
    null_disc = _null_control(page_names, tokens, features, counts, SEED)
    null_mean = round(sum(null_disc) / len(null_disc), 2)
    perm_p = round(sum(1 for d in null_disc if d >= raw) / len(null_disc), 3)
    anchor_excess = perm_p <= 0.05  # real discoveries exceed the chance count
    net_discoveries = raw if anchor_excess else 0

    power = _power_curve(page_names, [t["p"] for t in tests], features, SEED)
    mde = next((row["r_target"] for row in power
                if row["recovery_rate"] and row["recovery_rate"] >= 0.8), None)

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E7 — fine-granularity (graded) anchor hunt",
        "seed": SEED, "herbal_pages": n, "fdr_q": FDR_Q,
        "label_anchoring": {
            "label_token_types": len(label_pages),
            "label_types_on_ge2_pages": label_repeated,
            "feasible": label_repeated > 0,
            "note": "herbal labels are page-unique → 0 testable label anchors "
                    "(method limitation, not evidence about labelling)"},
        "graded_test": {
            "testable_tokens": len(tokens),
            "mid_prevalence_features": len(mid), "rare_prevalence_features": len(rare),
            "fdr_tests": len(tests),
            "raw_discoveries": raw,
            "null_discoveries_mean": null_mean,
            "null_discoveries_min_max": [min(null_disc), max(null_disc)],
            "permutation_p_of_count": perm_p,
            "anchor_excess_over_chance": bool(anchor_excess),
            "net_discoveries": net_discoveries,
            "top_discoveries": sorted(discoveries, key=lambda t: t["p"])[:10]},
        "power_curve_rank_biserial": power,
        "minimum_detectable_r_at_80pct": mde,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e7_fine_anchor.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    g = r["graded_test"]
    mde = r["minimum_detectable_r_at_80pct"]
    la = r["label_anchoring"]
    label_note = (
        f"Label-adjacency anchoring is INFEASIBLE on herbal ({la['label_token_types']} "
        f"label types, {la['label_types_on_ge2_pages']} on ≥2 pages) — herbal labels "
        f"are page-unique, so cross-page association has nothing to test (a method "
        f"limitation, not evidence about labelling).")
    if g["anchor_excess_over_chance"]:
        return "C", (
            f"CANDIDATE ANCHOR EXCESS: the graded test found {g['raw_discoveries']} "
            f"discoveries, MORE than the permuted-feature null (mean "
            f"{g['null_discoveries_mean']}, range {g['null_discoveries_min_max']}; "
            f"permutation p={g['permutation_p_of_count']} ≤ 0.05). This weakens the "
            f"anti-labelled-herbal null and REQUIRES a refutation pass before any "
            f"referential reading. Note the per-test BH is anti-conservative on sparse "
            f"counts, so the individual anchors need exact-p re-testing. {label_note}")
    return "C", (
        f"NULL HOLDS AT HIGHER POWER. A graded Mann–Whitney anchor hunt (per-page "
        f"token COUNTS, more powerful than E3's binary presence test), restricted to "
        f"the mid/rare feature bands where E3 had the most power "
        f"({g['mid_prevalence_features']} mid + {g['rare_prevalence_features']} rare × "
        f"{g['testable_tokens']} tokens = {g['fdr_tests']} tests), gives "
        f"{g['raw_discoveries']} raw discoveries — but that is NOT above chance: the "
        f"permuted-feature null yields mean {g['null_discoveries_mean']} (range "
        f"{g['null_discoveries_min_max']}), permutation p={g['permutation_p_of_count']}. "
        f"So the per-test BH is anti-conservative on the sparse tied counts and the raw "
        f"'discoveries' are false positives; the calibrated count-level test finds NO "
        f"anchor excess (graded-test MDE rank-biserial r={mde} at 80%). Even at higher "
        f"power the anti-labelled-herbal null HOLDS. {label_note} (L7: absence of a "
        f"detectable anchor is not proof no referents exist.)")


if __name__ == "__main__":
    out = run()
    la = out["label_anchoring"]
    print(f"labels: {la['label_token_types']} types, >=2pg {la['label_types_on_ge2_pages']} "
          f"→ feasible={la['feasible']}")
    g = out["graded_test"]
    print(f"graded: {g['testable_tokens']} tokens × "
          f"{g['mid_prevalence_features']}mid+{g['rare_prevalence_features']}rare feats "
          f"= {g['fdr_tests']} tests → {g['raw_discoveries']} raw discoveries")
    print(f"NULL mean={g['null_discoveries_mean']} range={g['null_discoveries_min_max']} "
          f"perm_p={g['permutation_p_of_count']} → excess={g['anchor_excess_over_chance']} "
          f"NET={g['net_discoveries']}")
    for row in out["power_curve_rank_biserial"]:
        print(f"  r={row['r_target']} realised={row['mean_realised_r']} "
              f"recovery={row['recovery_rate']}")
    print(f"MDE(80%): r={out['minimum_detectable_r_at_80pct']}")
    print(f"grade {out['grade']}: {out['verdict'][:120]}...")
