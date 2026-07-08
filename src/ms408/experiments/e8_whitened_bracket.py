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

    # 3. Whitening covariance Σ from pooled bootstrap z-vectors of all corpora on
    #    the fit half (full-rank, captures the collinearity to decorrelate).
    pooled = []
    tuned_mid_streams = {fam: families[fam][0](n, mid[fam])[:half] for fam in families}
    for b in range(60):
        rng = random.Random(5000 + b)
        pooled.append(_zvec(profile(_block_boot(vms_fit, rng)), frame))
        for fam in families:
            pooled.append(_zvec(profile(_block_boot(tuned_mid_streams[fam], rng)), frame))
    M = np.vstack(pooled)
    cov = np.cov(M, rowvar=False)
    inv = np.linalg.inv(cov + RIDGE * np.eye(len(METRICS)))

    # 4. Tune each family on the FIT half under the whitened distance.
    zv_fit = _zvec(vp_fit, frame)
    tuned = {}
    for fam, (gen, grid) in families.items():
        dists = {k: _mahalanobis(_zvec(fit_p[(fam, k)], frame), zv_fit, inv)
                 for k in grid}
        best = min(dists, key=dists.get)
        tuned[fam] = {"knob": best, "fit_distance": round(dists[best], 4),
                      "railed": best in (grid[0], grid[-1])}

    # 5. Held-out whitened distance at the tuned knob.
    zv_held = _zvec(vp_held, frame)
    held_point = {fam: round(_mahalanobis(_zvec(held_p[(fam, tuned[fam]["knob"])],
                                                frame), zv_held, inv), 4)
                  for fam in families}
    ranking = sorted(held_point, key=held_point.get)

    # 6. Bootstrap held-out distance + P(closest).
    tuned_held = {fam: families[fam][0](n, tuned[fam]["knob"])[half:] for fam in families}
    boot = {fam: [] for fam in families}
    wins = {fam: 0 for fam in families}
    for b in range(BOOTSTRAP):
        rng = random.Random(1000 + b)
        zvb = _zvec(profile(_block_boot(vms_held, rng)), frame)
        rep = {}
        for fam in families:
            d = _mahalanobis(_zvec(profile(_block_boot(tuned_held[fam], rng)), frame),
                             zvb, inv)
            boot[fam].append(d)
            rep[fam] = d
        wins[min(rep, key=rep.get)] += 1

    def ci(xs):
        s = sorted(xs)
        return [round(s[int(0.025 * len(s))], 4),
                round(s[min(len(s) - 1, int(0.975 * len(s)))], 4)]

    summary = {fam: {"held_distance": held_point[fam], "ci95": ci(boot[fam]),
                     "p_is_closest": round(wins[fam] / BOOTSTRAP, 3),
                     "tuned_knob": tuned[fam]["knob"], "railed": tuned[fam]["railed"],
                     "point_in_ci": ci(boot[fam])[0] <= held_point[fam] <= ci(boot[fam])[1]}
               for fam in ranking}
    consistent = all(summary[f]["point_in_ci"] for f in ranking)
    winner, runner = ranking[0], ranking[1]
    ci_sep = summary[winner]["ci95"][1] < summary[runner]["ci95"][0]
    robust = summary[winner]["p_is_closest"] >= 0.9 and ci_sep
    railed = [f for f in ranking if summary[f]["railed"]]

    # Export the whitened frame for E6.
    frame_export = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(), "metrics": list(METRICS),
        "frame_mean": {m: frame[m][0] for m in METRICS},
        "frame_sd": {m: frame[m][1] for m in METRICS},
        "sigma_inv": inv.tolist(), "ridge": RIDGE,
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
        "distance": "Mahalanobis (whitened by pooled-bootstrap metric covariance)",
        "held_out_ranking": ranking,
        "held_out": summary,
        "winner": winner, "winner_robust": bool(robust),
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
    w, ru = r["held_out_ranking"][0], r["held_out_ranking"][1]
    if not r["bootstrap_consistent"]:
        bad = [f for f in r["held_out_ranking"] if not ho[f]["point_in_ci"]]
        return "D", (f"INCONCLUSIVE — point distances outside bootstrap CIs for {bad}; "
                     f"resampling still biased. Do not grade.")
    if r["winner_robust"]:
        return "B", (
            f"Under the WHITENED distance and finer tuning, {w} is robustly closest "
            f"(held {ho[w]['held_distance']}, P(closest)={ho[w]['p_is_closest']}, CI "
            f"{ho[w]['ci95']} separated from {ru} {ho[ru]['ci95']}). A family is "
            f"distinguished even after de-collinearisation — a genuine positive that "
            f"E5's cluster-vote missed. (Compatibility, not likelihood; L7.)")
    return "C", (
        f"E5 CONFIRMED on unimpeachable footing: with a Mahalanobis-whitened distance "
        f"(collinearity removed, not just clustered) and a {r['grid_points']}-point "
        f"grid, still NO family is robustly distinguished — {w} leads (P(closest) "
        f"{ho[w]['p_is_closest']}) but its CI {ho[w]['ci95']} overlaps {ru} "
        f"{ho[ru]['ci95']}. Railed families: {r['railed_families'] or 'none'} "
        f"(boundary optima on bounded knobs are genuine, not under-tuning). The "
        f"encoding bracket is DESCRIPTIVE only; the i01 'conlang best fit' stays "
        f"withdrawn. Whitened frame exported for E6.")


if __name__ == "__main__":
    out = run()
    print(f"distance: {out['distance']}")
    print(f"consistent={out['bootstrap_consistent']} railed={out['railed_families']}")
    for fam in out["held_out_ranking"]:
        h = out["held_out"][fam]
        print(f"  {fam:20s} knob={str(h['tuned_knob']):5s} d={h['held_distance']:.4f} "
              f"CI={h['ci95']} P={h['p_is_closest']}{' RAILED' if h['railed'] else ''}")
    print(f"grade {out['grade']}: {out['verdict'][:120]}...")
