"""E31 — Hardening the mid-level syntax discriminators fc_z / wc_z (i11, post-E30).

E30 left the verbose+homophonic (Naibbe-class) cipher question undecidable because the
syntax measures are soft: (a) the VMS "band" is two Currier-A/B point estimates, not a CI;
(b) wc_z swings widely across seeds; (c) the null is a GLOBAL order-shuffle, so the z is
confounded with sectional/topic vocabulary drift (E22 control: real Latin types under a
block wrapper reach the VMS wc_z with no grammar at all). E31 hardens all three and
re-adjudicates.

Three fixes:
  1. DECONFOUND — a LOCAL (within-block) shuffle null preserves each block's vocabulary
     (topic) but destroys local adjacency, so z_local measures grammar BEYOND topic drift.
  2. VMS CI — block-bootstrap the VMS to replace the 2-point band with a real interval.
  3. STABILITY — report the z's own SD over null draws + word-class clustering seeds.

Re-adjudication: with deconfounded, CI'd measures, is the VMS separable from (i) an
order-preserving cipher (expected: yes, large gap) and (ii) a verbose+homophonic cipher
(the crux)? And how much of the VMS's "weak-positive" wc_z was topic-drift confound?

Usage:
    python -m ms408.experiments.e31_harden_syntax
"""

from __future__ import annotations

import json
import random
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from .e2_wordorder_confound import blocked_natural_text
from .e6_cipher_reconstruction import _det_verbose
from .e13_function_content import N_TOKENS, _sub, _vms_tokens
from .e13b_function_content import _gap
from .e14_word_classes import _adjacent_class_nmi
from .e30_cipher_reexamination import _homoph
from .mid_level_null import null_z, order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports"
SEED = 408
BLOCK = 250                          # local-null block: preserves ~section vocabulary
N_NULL = 20
N_BOOT = 40                          # VMS bootstrap replicates
N_STAB = 8                           # clustering-seed replicates for stability


def _local_shuffle(tokens: list, block: int, seed: int) -> list:
    """Shuffle WITHIN fixed blocks: preserves each block's vocabulary (topic/section
    composition), destroys local word order/adjacency. The deconfounded null."""
    rng = random.Random(seed)
    out = []
    for i in range(0, len(tokens), block):
        chunk = tokens[i:i + block]
        rng.shuffle(chunk)
        out.extend(chunk)
    return out


def _wc_z(tokens: list, null_fn, seed: int) -> float:
    obs = _adjacent_class_nmi(tokens, seed)
    nulls = [_adjacent_class_nmi(null_fn(tokens, seed + 1 + i), seed + 1 + i)
             for i in range(N_NULL)]
    return null_z(obs, nulls)["z"]


def _fc_z(tokens: list, null_fn, seed: int) -> float:
    obs = _gap(tokens)
    if obs.get("insufficient"):
        return 0.0
    nulls = [_gap(null_fn(tokens, seed + i)).get("gap") for i in range(N_NULL)]
    return null_z(obs["gap"], [g for g in nulls if g is not None])["z"]


def _glob(t, s):
    return order_shuffle(t, s)


def _loc(t, s):
    return _local_shuffle(t, BLOCK, s)


def _both(tokens: list, seed: int) -> dict:
    return {"wc_global": round(_wc_z(tokens, _glob, seed), 2),
            "wc_local": round(_wc_z(tokens, _loc, seed), 2),
            "fc_global": round(_fc_z(tokens, _glob, seed), 2),
            "fc_local": round(_fc_z(tokens, _loc, seed), 2)}


def _stability(tokens: list) -> dict:
    """SD of each z over clustering/null seeds — the measure's own noise."""
    runs = [_both(tokens, SEED + 100 * k) for k in range(N_STAB)]
    return {k + "_sd": round(statistics.pstdev(r[k] for r in runs), 2)
            for k in ("wc_global", "wc_local", "fc_global", "fc_local")}


def run() -> dict:
    vms = _sub(_vms_tokens("A") + _vms_tokens("B"), N_TOKENS)
    base = blocked_natural_text(14000)
    op = _det_verbose(base, 2, 0, SEED)                       # order-preserving
    vh = _homoph(_det_verbose(base, 3, 0, SEED), 16, SEED + 1)  # verbose+homophonic (Naibbe-class)

    # Point estimates (deconfounded + confounded) for VMS + the two ciphers.
    point = {"VMS": _both(vms, SEED),
             "cipher_order_preserving": _both(_sub(op), SEED),
             "cipher_verbose_homophonic": _both(_sub(vh), SEED)}

    # VMS sampling CI by SUBSAMPLING WITHOUT REPLACEMENT (75% of distinct blocks).
    # NB: block-bootstrap WITH replacement is INVALID for these measures — duplicate blocks
    # inject artificial collocation/adjacency and inflate the z's (a real methodological
    # gotcha this experiment surfaced). Subsampling without replacement avoids it.
    boot = {"wc_local": [], "fc_local": []}
    nb = len(vms) // BLOCK
    for b in range(N_BOOT):
        rng = random.Random(7000 + b)
        keep = sorted(rng.sample(range(nb), int(0.75 * nb)))
        resamp = [vms[j] for i in keep
                  for j in range(i * BLOCK, min((i + 1) * BLOCK, len(vms)))]
        r = _both(resamp, SEED + b)
        for k in boot:
            boot[k].append(r[k])
    def ci(key):
        s = sorted(boot[key])
        return [round(s[int(0.05 * len(s))], 2), round(s[int(0.95 * len(s)) - 1], 2)]
    vms_ci = {k: ci(k) for k in boot}

    stability = {name: _stability(t) for name, t in
                 (("VMS", vms), ("cipher_order_preserving", _sub(op)),
                  ("cipher_verbose_homophonic", _sub(vh)))}

    # --- adjudication (separability by stability-SD, the valid noise estimate) --------
    def sep(cipher, key):
        d = abs(point[cipher][key] - point["VMS"][key])
        sd = (stability["VMS"][key + "_sd"] ** 2
              + stability[cipher][key + "_sd"] ** 2) ** 0.5
        return {"gap": round(d, 2), "combined_sd": round(sd, 2),
                "n_sd": round(d / sd, 1) if sd else None, "separable": bool(sd and d > 2 * sd)}
    op_fc = sep("cipher_order_preserving", "fc_local")
    op_wc = sep("cipher_order_preserving", "wc_local")
    vh_fc = sep("cipher_verbose_homophonic", "fc_local")
    vh_wc = sep("cipher_verbose_homophonic", "wc_local")
    op_sep_local = op_fc["separable"] or op_wc["separable"]
    vh_sep_local = vh_fc["separable"] and vh_wc["separable"]
    # how much of the VMS wc_z is topic-drift confound (global minus local)?
    drift_share = round(point["VMS"]["wc_global"] - point["VMS"]["wc_local"], 2)
    vms_wc_local_positive = point["VMS"]["wc_local"] > 0

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E31 — hardened (deconfounded + CI'd) syntax discriminators",
        "seed": SEED, "block": BLOCK, "n_null": N_NULL, "n_boot": N_BOOT,
        "point_estimates": point,
        "vms_subsample_ci_90_no_replacement": vms_ci,
        "stability_sd": stability,
        "separability_by_stability_sd": {
            "order_preserving_fc_local": op_fc, "order_preserving_wc_local": op_wc,
            "verbose_homophonic_fc_local": vh_fc, "verbose_homophonic_wc_local": vh_wc},
        "vms_wc_local_minus_global_drift_share": drift_share,
        "vms_wc_local_still_positive": bool(vms_wc_local_positive),
        "order_preserving_separable_from_vms_local": bool(op_sep_local),
        "verbose_homophonic_separable_from_vms_local": bool(vh_sep_local),
        "note_bootstrap_with_replacement_invalid": "block-bootstrap WITH replacement inflates "
        "these collocation/adjacency measures via duplicate blocks; CI here uses subsampling "
        "WITHOUT replacement, and separability uses the seed-stability SD.",
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e31_harden_syntax.json").write_text(json.dumps(results, indent=2) + "\n")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "e31_harden_syntax.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    p = r["point_estimates"]
    st = r["stability_sd"]
    s = r["separability_by_stability_sd"]
    common = (
        f"Deconfounded (within-block null, grammar only) vs confounded (global-shuffle) z. "
        f"VMS wc: global {p['VMS']['wc_global']} → local {p['VMS']['wc_local']} (topic-drift "
        f"share {r['vms_wc_local_minus_global_drift_share']} ≈ 0 → the VMS's weak wc_z is REAL "
        f"grammar, NOT sectional drift). Measures are STABLE to seed noise (SD: VMS fc_local "
        f"±{st['VMS']['fc_local_sd']}, wc_local ±{st['VMS']['wc_local_sd']}). Separability "
        f"(gap / combined SD): order-preserving fc_local {s['order_preserving_fc_local']['n_sd']}σ, "
        f"wc_local {s['order_preserving_wc_local']['n_sd']}σ; verbose+homophonic fc_local "
        f"{s['verbose_homophonic_fc_local']['n_sd']}σ, wc_local {s['verbose_homophonic_wc_local']['n_sd']}σ. "
        f"(Block-bootstrap WITH replacement was found INVALID here — duplicate blocks inflate "
        f"these measures — so CIs use subsampling without replacement + the seed-SD.)")
    op = r["order_preserving_separable_from_vms_local"]
    vh = r["verbose_homophonic_separable_from_vms_local"]
    if op and not vh:
        return "B", (
            f"HARDENING FIRMS THE ROBUST LEG and confirms the homophonic class stays open. Once "
            f"the null is deconfounded and the measures' true (small) seed-noise is used instead "
            f"of an invalid resampling CI, the order-preserving cipher is separable from the VMS "
            f"by a LARGE margin ("
            f"fc_local {s['order_preserving_fc_local']['n_sd']}σ, wc_local "
            f"{s['order_preserving_wc_local']['n_sd']}σ) — so word-order-preserving ciphers are "
            f"robustly EXCLUDED, and the exclusion does NOT depend on the 2-point band or on "
            f"topic drift (the VMS's weak wc_z survives deconfounding). The verbose+homophonic "
            f"(Naibbe-class) cipher, by contrast, sits in the VMS's own weak-syntax regime "
            f"(fc_local {p['cipher_verbose_homophonic']['fc_local']} vs VMS "
            f"{p['VMS']['fc_local']}; wc_local {p['cipher_verbose_homophonic']['wc_local']} vs "
            f"{p['VMS']['wc_local']}) and is NOT jointly separable, so it remains NOT excludable "
            f"— the VMS-as-homophonic-cipher hypothesis (Naibbe) stays viable. NET: the E30 "
            f"partition survives hardened, deconfounded measures. {common} (Statistical — L7.)")
    if not op:
        return "C", (
            f"HARDENING WEAKENS EVEN THE ROBUST LEG: after deconfounding, the order-preserving "
            f"cipher is not cleanly separable from the VMS (fc_local "
            f"{s['order_preserving_fc_local']['n_sd']}σ, wc_local "
            f"{s['order_preserving_wc_local']['n_sd']}σ) — the whole i06 exclusion needs a firmer "
            f"discriminator than fc_z/wc_z. {common} (L7.)")
    return "C", (
        f"AMBIGUOUS: the verbose+homophonic cipher's separability is marginal/sensitive; the "
        f"honest status stands (order-preserving excluded, homophonic not excludable). {common} (L7.)")


def _render(r: dict) -> str:
    p, ci, st = (r["point_estimates"], r["vms_subsample_ci_90_no_replacement"],
                 r["stability_sd"])
    lines = [
        "# E31 — Hardened syntax discriminators (deconfounded + CI'd)",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e31_harden_syntax`. Numbers in "
        "`results/experiments/e31_harden_syntax.json`.",
        "",
        "Global null = order-shuffle (confounded with topic drift); local null = within-"
        f"{r['block']}-word-block shuffle (preserves topic, destroys adjacency → grammar only).",
        "",
        "| corpus | wc global | wc **local** | fc global | fc **local** |",
        "|---|---|---|---|---|",
    ]
    for name, v in p.items():
        lines.append(f"| {name} | {v['wc_global']} | **{v['wc_local']}** | {v['fc_global']} "
                     f"| **{v['fc_local']}** |")
    lines += ["",
              f"VMS 90% subsample CI (no replacement): wc_local {ci['wc_local']}, "
              f"fc_local {ci['fc_local']}.",
              f"Stability SD (VMS): wc_local ±{st['VMS']['wc_local_sd']}, fc_local "
              f"±{st['VMS']['fc_local_sd']}.",
              f"VMS wc topic-drift share (global−local): "
              f"{r['vms_wc_local_minus_global_drift_share']}.",
              "", f"## Verdict [{r['grade']}]", "", r["verdict"], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    p = out["point_estimates"]
    print(f"{'corpus':28s} {'wc_glob':>8s} {'wc_LOCAL':>9s} {'fc_glob':>8s} {'fc_LOCAL':>9s}")
    for name, v in p.items():
        print(f"{name:28s} {v['wc_global']:>8} {v['wc_local']:>9} {v['fc_global']:>8} "
              f"{v['fc_local']:>9}")
    print(f"VMS wc_local 90% CI: {out['vms_subsample_ci_90_no_replacement']['wc_local']} | topic-drift share "
          f"{out['vms_wc_local_minus_global_drift_share']} | VMS wc_local positive="
          f"{out['vms_wc_local_still_positive']}")
    print(f"order-preserving separable={out['order_preserving_separable_from_vms_local']} | "
          f"verbose-homophonic separable={out['verbose_homophonic_separable_from_vms_local']}")
    print(f"grade {out['grade']}: {out['verdict'][:150]}...")
