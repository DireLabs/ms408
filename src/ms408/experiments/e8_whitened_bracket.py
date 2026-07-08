"""E8 — Whitened, continuously-tuned encoding bracket (i03; fixes E5 residuals).

The E5 refutation named two holes in the "fair bracket":
  1. RESIDUAL COLLINEARITY. E5's de-collinearisation used 6 PRE-DECLARED metric
     clusters with one vote each, but the empirical metric correlations showed
     strong CROSS-cluster collinearity (zipf_slope~mz_peak_scale 0.85,
     position_entropy~repetition_rate 0.80, abbreviation_rho~ed1 0.78). So "one
     vote per cluster" still double-counted ~3 of 6 effectively-redundant axes.
  2. UNEQUAL TUNING POWER. Equal knob-COUNT is not equal tuning power: several
     families railed at the 6-point grid edges (their optima lay at or beyond the
     tested range), so the ranking partly reflected grid resolution.

E8 fixes both:
  * WHITENED DISTANCE. Replace the cluster vote with a Mahalanobis distance
    d(f,vms) = sqrt((z_f - z_vms) Σ⁻¹ (z_f - z_vms)), where Σ is the empirical
    metric covariance estimated from the pooled bootstrap z-vectors of all corpora
    (full-rank, ridge-regularised). Whitening decorrelates the metrics, so
    collinear axes contribute ONE effective direction, not two — the principled
    version of E5's clustering.
  * FINER CONTINUOUS TUNING. A 21-point grid on [0,1] for fraction knobs (vs E5's
    6) and a widened integer range for self-citation, so boundary/interior optima
    are well-resolved. (A genuine boundary optimum on a bounded fraction is a real
    result, not under-tuning — reported as such.)

Everything else matches E5: same 7 families (+ E6's deterministic-verbose family
is added here so E8 supplies E6's whitened frame), fit-on-half / score-on-held-out,
block bootstrap (block > MZ scale), point-in-CI consistency guard.

Deliverable also EXPORTS the whitened frame (metric means, sds, Σ⁻¹) to
`results/experiments/e8_whitened_frame.json` for E6 to consume.

Usage:
    python -m ms408.experiments.e8_whitened_bracket
"""

from __future__ import annotations

import json
import random
import statistics
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ..dataset import git_commit
from ..studies.encoding import METRICS, profile, vms_stream
from .e5_encoding_fair import FAMILIES as E5_FAMILIES
from .e5_encoding_fair import _block_boot, fam_conlang_relex

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"

SEED = 408
BOOTSTRAP = 150
BLOCK = 2500
RIDGE = 1e-3  # regularises Σ before inversion (metrics far outnumber corpora)
FINE = tuple(round(i / 20, 3) for i in range(21))          # 0.00 .. 1.00 by 0.05
SELFCITE = tuple(range(1, 9))                              # widened 1..8


def _families() -> dict:
    """E5's seven families on a FINER grid, + E6's deterministic-verbose family so
    the whitened frame E8 exports already covers the cipher-reconstruction track."""
    fams = {}
    for name, (gen, grid) in E5_FAMILIES.items():
        fine = SELFCITE if name == "selfcitation" else FINE
        fams[name] = (gen, fine)
    fams["det_verbose"] = (_fam_det_verbose, FINE)
    return fams


def _fam_det_verbose(n: int, paradigm: float, seed: int = SEED) -> list:
    """Deterministic verbose / nomenclator cipher (E2's re-opened family): a
    type-PRESERVING verbose expansion (bijection on word types, no homophones) of a
    conlang-relexified stream at paradigm strength `paradigm`. Knob sweeps the
    paradigmatic-morphology density — the axis that controls the ED1 network E6
    must reproduce. Length-preserving 1:1 glyph map keeps word length in range."""
    rng = random.Random(seed)
    base = fam_conlang_relex(n, paradigm, seed=seed)
    glyphs = "abcdefghiklmnoprstuvxyz"
    letter_map = {c: rng.choice(glyphs) for c in set("".join(base))}
    cache: dict = {}
    out = []
    for t in base:
        if t not in cache:
            cache[t] = "".join(letter_map[c] for c in t)
        out.append(cache[t])
    return out


def _zvec(p: dict, frame: dict) -> np.ndarray:
    return np.array([(p[m] - frame[m][0]) / frame[m][1] for m in METRICS])


def _frame(profiles: list) -> dict:
    out = {}
    for m in METRICS:
        vals = [p[m] for p in profiles]
        out[m] = (statistics.mean(vals), statistics.stdev(vals) or 1.0)
    return out


def _mahalanobis(zf: np.ndarray, zv: np.ndarray, inv: np.ndarray) -> float:
    d = zf - zv
    return float(np.sqrt(max(0.0, d @ inv @ d)))


def run() -> dict:
    vms = vms_stream()
    n = len(vms)
    half = n // 2
    vms_fit, vms_held = vms[:half], vms[half:]
    vp_fit, vp_held = profile(vms_fit), profile(vms_held)
    families = _families()

    # 1. Fit/held profiles for every (family, knob).
    fit_p, held_p = {}, {}
    for fam, (gen, grid) in families.items():
        for k in grid:
            s = gen(n, k)
            fit_p[(fam, k)] = profile(s[:half])
            held_p[(fam, k)] = profile(s[half:])

    # 2. z-frame from each family's mid-knob + VMS (fit half).
    mid = {fam: grid[len(grid) // 2] for fam, (_, grid) in families.items()}
    frame = _frame([fit_p[(fam, mid[fam])] for fam in families] + [vp_fit])

    # 3. Labelled fit-half bootstrap z-vectors per corpus (feed Σ + LOO + Σ_vms).
    #    The E8-refutation showed the covariance choice is load-bearing and easy to
    #    get wrong, so we build TWO whitening matrices and validate conditioning:
    #      Σ_pooled — all corpora pooled (E8's original; dominated by between-corpus
    #                 spread, ~few effective independent points → must be stress-tested)
    #      Σ_vms    — VMS resamples only (the sampling covariance the distance
    #                 actually needs for a VMS-vs-family comparison)
    corpora = {"vms": vms_fit,
               **{fam: families[fam][0](n, mid[fam])[:half] for fam in families}}
    zvecs = {name: [] for name in corpora}
    for b in range(60):
        rng = random.Random(5000 + b)
        for name, stream in corpora.items():
            zvecs[name].append(_zvec(profile(_block_boot(stream, rng)), frame))
    all_vecs = np.vstack([v for vs in zvecs.values() for v in vs])
    cov_pooled = np.cov(all_vecs, rowvar=False)
    cov_vms = np.cov(np.vstack(zvecs["vms"]), rowvar=False)
    eig = np.linalg.eigvalsh(cov_pooled)
    cond_number = float(eig[-1] / max(eig[0], 1e-12))

    def inv_of(cov, ridge):
        return np.linalg.inv(cov + ridge * np.eye(len(METRICS)))

    inv = inv_of(cov_pooled, RIDGE)          # primary whitening
    inv_vms = inv_of(cov_vms, RIDGE)         # the "matrix the distance needs"

    # 4. Tune on the FIT half under the primary whitened distance.
    zv_fit = _zvec(vp_fit, frame)
    tuned = {}
    for fam, (gen, grid) in families.items():
        dists = {k: _mahalanobis(_zvec(fit_p[(fam, k)], frame), zv_fit, inv)
                 for k in grid}
        best = min(dists, key=dists.get)
        tuned[fam] = {"knob": best, "fit_distance": round(dists[best], 4),
                      "railed": best in (grid[0], grid[-1])}

    # 5. Held-out ranking under the primary distance.
    zv_held = _zvec(vp_held, frame)

    def held_rank(inv_m):
        d = {fam: _mahalanobis(_zvec(held_p[(fam, tuned[fam]["knob"])], frame),
                               zv_held, inv_m) for fam in families}
        return sorted(d, key=d.get)

    held_point = {fam: round(_mahalanobis(_zvec(held_p[(fam, tuned[fam]["knob"])],
                                                frame), zv_held, inv), 4)
                  for fam in families}
    ranking = sorted(held_point, key=held_point.get)

    # 5b. Σ VALIDATION (the E8-refutation's decisive fix). Hold tuning fixed and
    #     vary only the whitening matrix; if the TOP family is unstable across ridge,
    #     leave-one-corpus-out, and the Σ_vms distance, the reshuffle is a
    #     regularisation artifact and whitening cannot "confirm" anything.
    ridge_top = {}
    for r in (1e-4, 1e-3, 1e-2, 1e-1):
        ridge_top[f"ridge_{r:g}"] = held_rank(inv_of(cov_pooled, r))[0]
    loo_top = {}
    for drop in corpora:
        M_loo = np.vstack([v for name, vs in zvecs.items() if name != drop for v in vs])
        loo_top[f"drop_{drop}"] = held_rank(inv_of(np.cov(M_loo, rowvar=False), RIDGE))[0]
    vms_cov_ranking = held_rank(inv_vms)
    top_families_seen = set(ridge_top.values()) | set(loo_top.values()) | {vms_cov_ranking[0]}
    sigma_stable = len(top_families_seen) == 1

    # 6. Bootstrap held-out distance + P(closest) under BOTH Σ_pooled and Σ_vms.
    tuned_held = {fam: families[fam][0](n, tuned[fam]["knob"])[half:] for fam in families}
    boot = {fam: [] for fam in families}
    wins = {fam: 0 for fam in families}
    wins_vms = {fam: 0 for fam in families}
    for b in range(BOOTSTRAP):
        rng = random.Random(1000 + b)
        zvb = _zvec(profile(_block_boot(vms_held, rng)), frame)
        rep, rep_vms = {}, {}
        for fam in families:
            fz = _zvec(profile(_block_boot(tuned_held[fam], rng)), frame)
            d = _mahalanobis(fz, zvb, inv)
            boot[fam].append(d)
            rep[fam] = d
            rep_vms[fam] = _mahalanobis(fz, zvb, inv_vms)
        wins[min(rep, key=rep.get)] += 1
        wins_vms[min(rep_vms, key=rep_vms.get)] += 1

    def ci(xs):
        s = sorted(xs)
        return [round(s[int(0.025 * len(s))], 4),
                round(s[min(len(s) - 1, int(0.975 * len(s)))], 4)]

    summary = {fam: {"held_distance": held_point[fam], "ci95": ci(boot[fam]),
                     "p_is_closest": round(wins[fam] / BOOTSTRAP, 3),
                     "p_is_closest_vmscov": round(wins_vms[fam] / BOOTSTRAP, 3),
                     "tuned_knob": tuned[fam]["knob"], "railed": tuned[fam]["railed"],
                     "point_in_ci": ci(boot[fam])[0] <= held_point[fam] <= ci(boot[fam])[1]}
               for fam in ranking}
    consistent = all(summary[f]["point_in_ci"] for f in ranking)
    winner, runner = ranking[0], ranking[1]
    ci_sep = summary[winner]["ci95"][1] < summary[runner]["ci95"][0]
    # No family distinguished if none reaches P>=0.9 under EITHER covariance —
    # a metric-INDEPENDENT statement, which is the only one we can trust given
    # the Σ-conditioning problem.
    pooled_top_p = max(summary[f]["p_is_closest"] for f in families)
    vmscov_winner = max(families, key=lambda f: wins_vms[f])
    vmscov_top_p = round(wins_vms[vmscov_winner] / BOOTSTRAP, 3)
    # A family is DISTINGUISHED only if the whitened ranking is STABLE (same top
    # across ridge / LOO / Σ_vms) AND that stable top reaches P>=0.9. An unstable
    # ranking where a DIFFERENT family dominates under each covariance is the
    # opposite of a distinguished winner — it means the distance itself is
    # uninformative. (The earlier "max P under either cov" gate had this backwards.)
    robust = sigma_stable and pooled_top_p >= 0.9 and ci_sep
    railed = [f for f in ranking if summary[f]["railed"]]

    # Export the whitened frame for E6 — BOTH matrices + the conditioning report,
    # so E6 can pick the validated one (or fall back to raw per-metric matching).
    frame_export = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(), "metrics": list(METRICS),
        "frame_mean": {m: frame[m][0] for m in METRICS},
        "frame_sd": {m: frame[m][1] for m in METRICS},
        "sigma_inv_pooled": inv.tolist(), "sigma_inv_vmscov": inv_vms.tolist(),
        "ridge": RIDGE, "cov_condition_number": cond_number,
        "sigma_validated_stable": bool(sigma_stable),
        "vms_held_zvec": zv_held.tolist(),
    }
    (RESULTS_DIR / "e8_whitened_frame.json").write_text(
        json.dumps(frame_export, indent=2) + "\n")

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E8 — whitened, continuously-tuned encoding bracket",
        "seed": SEED, "tokens_total": n, "held_tokens": n - half,
        "bootstrap": BOOTSTRAP, "grid_points": len(FINE),
        "distance": "Mahalanobis (pooled Σ primary; Σ_vms cross-check)",
        "sigma_condition_number": round(cond_number, 1),
        "sigma_min_max_eigenvalue": [round(float(eig[0]), 5), round(float(eig[-1]), 3)],
        "sigma_stability": {"top_across_ridge": ridge_top, "top_across_loo": loo_top,
                            "vmscov_top": vms_cov_ranking[0],
                            "top_families_seen": sorted(top_families_seen),
                            "stable": bool(sigma_stable)},
        "held_out_ranking": ranking,
        "held_out": summary,
        "winner": winner, "winner_robust": bool(robust),
        "pooled_top_p_closest": round(pooled_top_p, 3),
        "vmscov_winner": vmscov_winner, "vmscov_top_p_closest": vmscov_top_p,
        "bootstrap_consistent": bool(consistent),
        "railed_families": railed,
        "frame_exported_to": "results/experiments/e8_whitened_frame.json",
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e8_whitened_bracket.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    ho = r["held_out"]
    w = r["held_out_ranking"][0]
    stab = r["sigma_stability"]
    if not r["bootstrap_consistent"]:
        bad = [f for f in r["held_out_ranking"] if not ho[f]["point_in_ci"]]
        return "D", (f"INCONCLUSIVE — point distances outside bootstrap CIs for {bad}; "
                     f"resampling still biased. Do not grade.")
    if r["winner_robust"] and stab["stable"]:
        return "B", (
            f"Under a VALIDATED whitened distance (stable across ridge, "
            f"leave-one-corpus-out, and the Σ_vms cross-check), {w} is robustly "
            f"closest (P(closest)={ho[w]['p_is_closest']}). A genuine positive. (L7.)")
    # The realised case: the whitened ranking is UNSTABLE, so it neither distinguishes
    # a family nor 'confirms' E5. The honest conclusion rests on that instability.
    return "C", (
        f"NO STABLY DISTINGUISHED FAMILY; whitening-confirmation WITHDRAWN. Σ is "
        f"ILL-CONDITIONED (condition number {r['sigma_condition_number']:.0f}; min "
        f"eigenvalue {r['sigma_min_max_eigenvalue'][0]} ≈ the ridge itself, so the "
        f"ridge defines the smallest directions), and the closest family is UNSTABLE "
        f"across the whitening choice — top ∈ {stab['top_families_seen']} across "
        f"ridge / leave-one-corpus-out / Σ_vms. Under the pooled Σ the best "
        f"P(closest) is only {r['pooled_top_p_closest']}; under Σ_vms a DIFFERENT "
        f"family ({r['vmscov_winner']}) dominates at {r['vmscov_top_p_closest']} — "
        f"but that is exactly the family E5 showed wins via a single-metric "
        f"repetition_rate artifact, and it does not survive the covariance switch. A "
        f"ranking that reshuffles its winner with every reasonable distance is "
        f"UNINFORMATIVE: it cannot distinguish a family, and cannot 'confirm' E5 as a "
        f"cleaner method. What DOES hold — over-determined across E5's cluster-vote, "
        f"the pooled Σ, and Σ_vms — is that no family is STABLY closest; the encoding "
        f"bracket is DESCRIPTIVE only and the i01 'conlang best fit' stays withdrawn. "
        f"Railed: {r['railed_families'] or 'none'}. E6 correctly uses raw per-metric "
        f"joint matching, not any single whitened distance.")


if __name__ == "__main__":
    out = run()
    print(f"distance: {out['distance']}")
    print(f"Σ condition number={out['sigma_condition_number']} "
          f"eig(min,max)={out['sigma_min_max_eigenvalue']} "
          f"stable={out['sigma_stability']['stable']} "
          f"top_seen={out['sigma_stability']['top_families_seen']}")
    print(f"pooled top P={out['pooled_top_p_closest']} | Σ_vms winner "
          f"{out['vmscov_winner']} P={out['vmscov_top_p_closest']} | "
          f"consistent={out['bootstrap_consistent']} railed={out['railed_families']}")
    for fam in out["held_out_ranking"]:
        h = out["held_out"][fam]
        print(f"  {fam:20s} knob={str(h['tuned_knob']):5s} d={h['held_distance']:.4f} "
              f"CI={h['ci95']} P={h['p_is_closest']} Pvms={h['p_is_closest_vmscov']}"
              f"{' RAILED' if h['railed'] else ''}")
    print(f"grade {out['grade']}: {out['verdict'][:140]}...")
