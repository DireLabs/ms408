"""E33 — the block-scale, like-for-like ΔI test (the last untested ΔI leg).

The v6 refutation flagged that i06's word-order (ΔI) leg was killed only *as applied*
(token-level, and confounded by Greshko's respacing, E29) — and that a **block-scale
like-for-like** ΔI comparison was untested. This is that test, cast as the decisive,
non-circular question the refuter pointed at: the mutual exclusivity (or not) of low
character entropy and block-scale word-order information.

    On the (h2, block-scale ΔI) plane, sweeping a verbose+homophonic cipher of a
    topically-structured real text, is there ANY setting that matches the VMS on BOTH
    axes at once — or does matching h2 force the block-scale ΔI to collapse below the VMS?

Why this is like-for-like (removing the E29 confounds):
  * no respacing — all systems are word-boundary, so token granularity is identical;
  * matched token budget N and matched partition counts, so ΔI scales are identical;
  * null-corrected — ΔI is measured against each system's OWN order-shuffle floor;
  * block scale — ΔI is read at the coarse (topic) partitions where the VMS's ΔI lives,
    not at the token level.

Homophony scatters plaintext types across ciphertext variants, so it destroys the
block-scale type-concentration that topic structure produces: as h rises, block ΔI falls.
The crux is whether it falls THROUGH the VMS's value at the same h that matches the VMS's
h2. If a cipher reaches the VMS corner on both axes, the block-scale ΔI does NOT separate
verbose+homophonic ciphers, and the ΔI leg is dead even here — the exclusion rests on the
(soft) mid-level syntax measures alone. If no setting reaches the corner, the leg revives.

Usage:
    python -m ms408.experiments.e33_block_scale_di
"""

from __future__ import annotations

import json
import random
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..mz import delta_information
from ..studies.encoding import profile
from .e2_wordorder_confound import blocked_natural_text
from .e6_cipher_reconstruction import _GLYPHS
from .e13_function_content import N_TOKENS, _sub, _vms_tokens
from .mid_level_null import order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports"
SEED = 408
N = 10_000
# coarse (topic-scale) partitions: scale = N/p words, ~333–3333 words — where the VMS's ΔI lives
COARSE = (3, 4, 5, 6, 8, 10, 15, 20, 30)
N_NULL = 4                       # order-shuffle nulls per ΔI point
EXPANSIONS = (1, 2, 3)          # verbose glyph-unit sizes (1 ≈ VMS word length)
H_SWEEP = (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 24, 32)
K_SEEDS = 5
# generous tolerances (do not stack the deck toward "separable")
H2_TOL = 0.08
BASE_TOKENS = 14_000


def _verbose(tokens: list, expansion: int, seed: int) -> list:
    """Deterministic verbose cipher: each plaintext letter → a fixed `expansion`-glyph unit
    (low h2 via repeated units; word types preserved). Local copy of the e6 primitive."""
    rng = random.Random(seed)
    letters = sorted({c for w in tokens for c in w})
    unit = {c: "".join(rng.choice(_GLYPHS) for _ in range(expansion)) for c in letters}
    cache: dict = {}
    out = []
    for w in tokens:
        if w not in cache:
            cache[w] = "".join(unit[c] for c in w)
        out.append(cache[w])
    return out


def _vhomoph(tokens: list, expansion: int, h: int, seed: int) -> list:
    """Verbose + homophonic cipher, FAIR (in-alphabet, no markers) and LOW-h2-preserving.

    Base = deterministic verbose (keeps the low character entropy a real verbose cipher has).
    Homophony = each occurrence appends one of `h` distinct in-alphabet suffix strings, so a
    plaintext type scatters across h ciphertext spellings (destroying block-scale type
    concentration) while the character structure stays low-entropy and in-alphabet.

    This replaces the shared `_homoph`, which prefixes "{i}#" to every token: the refutation
    pass showed that '#'/digit marker deflates h2 by ~0.34 bits and was the sole reason a
    cipher spuriously reached the VMS corner. This suffix model is the refuter's own validated
    fix and is CONSERVATIVE (most favourable to the cipher): it keeps h2 as low as the base
    verbose allows, so it does not overstate separation.
    """
    base = _verbose(tokens, expansion, seed)
    if h <= 1:
        return base
    rng = random.Random(seed + 1)
    width = 1 if h <= len(_GLYPHS) else 2
    suffixes: list = sorted({"".join(rng.choice(_GLYPHS) for _ in range(width))
                             for _ in range(h * 3)})[:h]
    while len(suffixes) < h:                      # top up if collisions left us short
        suffixes.append("".join(rng.choice(_GLYPHS) for _ in range(width + 1)))
    return [tok + rng.choice(suffixes) for tok in base]


def _mwl(tokens: list) -> float:
    t = tokens[:N]
    return round(sum(map(len, t)) / len(t), 2)


def block_di(tokens: list, seed: int) -> float:
    """Null-corrected ΔI at the coarse/topic partitions (max over COARSE). Like-for-like:
    matched partition counts + matched N; each point corrected by its own shuffle floor."""
    t = tokens[:N]
    best = -9.0
    for p in COARSE:
        obs = delta_information(t, p)[0]
        floor = statistics.mean(delta_information(order_shuffle(t, seed + i), p)[0]
                                for i in range(N_NULL))
        best = max(best, obs - floor)
    return round(best, 4)


def _point(tokens: list, seed: int) -> tuple:
    return round(profile(tokens[:N])["h2"], 4), block_di(tokens, seed)


def run() -> dict:
    vms = _sub(_vms_tokens("A") + _vms_tokens("B"), N_TOKENS)
    vms_h2, vms_bdi = _point(vms, SEED)

    # VMS joint CI by subsampling without replacement (duplicate-safe, per E31).
    BLOCK = 250
    nb = len(vms) // BLOCK
    vh2, vbdi = [], []
    for b in range(20):
        rng = random.Random(7000 + b)
        keep = sorted(rng.sample(range(nb), int(0.75 * nb)))
        rs = [vms[j] for i in keep for j in range(i * BLOCK, (i + 1) * BLOCK)]
        h2, bdi = _point(rs, SEED + b)
        vh2.append(h2)
        vbdi.append(bdi)

    def ci(vals):
        s = sorted(vals)
        return [round(s[int(0.05 * len(s))], 4), round(s[min(len(s) - 1, int(0.95 * len(s)))], 4)]
    vms_h2_ci, vms_bdi_ci = ci(vh2), ci(vbdi)

    vms_mwl = _mwl(vms)
    base = blocked_natural_text(BASE_TOKENS)
    plain_h2, plain_bdi = _point(base, SEED)   # h=1 positive control (full topic structure)

    # Sweep verbose expansion x FAIR (in-alphabet) homophony over K seeds.
    grid = []
    for vx in EXPANSIONS:
        for h in H_SWEEP:
            ciphers = [_vhomoph(base, vx, h, SEED + 100 + k) for k in range(K_SEEDS)]
            pts = [_point(c, SEED + k) for k, c in enumerate(ciphers)]
            med_h2 = round(statistics.median(p[0] for p in pts), 4)
            med_bdi = round(statistics.median(p[1] for p in pts), 4)
            med_mwl = round(statistics.median(_mwl(c) for c in ciphers), 2)
            # does this config reach the VMS corner on BOTH axes (median in tolerance)?
            h2_ok = abs(med_h2 - vms_h2) <= H2_TOL
            bdi_ok = vms_bdi_ci[0] <= med_bdi <= vms_bdi_ci[1]
            grid.append({"expansion": vx, "h": h, "h2": med_h2, "block_di": med_bdi,
                         "mwl": med_mwl, "h2_matches_vms": bool(h2_ok),
                         "bdi_matches_vms": bool(bdi_ok),
                         "reaches_corner": bool(h2_ok and bdi_ok)})

    corner = [g for g in grid if g["reaches_corner"]]
    # closest approach in normalized (h2, block_di) space
    h2_scale = H2_TOL or 1.0
    bdi_scale = (vms_bdi_ci[1] - vms_bdi_ci[0]) / 2 or 0.03

    def dist(g):
        return round(((g["h2"] - vms_h2) / h2_scale) ** 2
                     + ((g["block_di"] - vms_bdi) / bdi_scale) ** 2, 3) ** 0.5
    closest = min(grid, key=dist)
    # at the config best matching VMS h2, how far (in CI-half-widths) is block_di?
    h2_matched = [g for g in grid if g["h2_matches_vms"]]
    bdi_gap_at_h2 = None
    if h2_matched:
        best_h2 = min(h2_matched, key=lambda g: abs(g["h2"] - vms_h2))
        bdi_gap_at_h2 = {"config": {k: best_h2[k] for k in ("expansion", "h")},
                         "block_di": best_h2["block_di"], "vms_block_di": vms_bdi,
                         "vms_bdi_ci": vms_bdi_ci,
                         "in_vms_bdi_ci": bool(vms_bdi_ci[0] <= best_h2["block_di"] <= vms_bdi_ci[1])}

    separable = len(corner) == 0
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E33 — block-scale like-for-like ΔI on the (h2, block-ΔI) plane",
        "seed": SEED, "n_tokens": N, "coarse_partitions": list(COARSE), "n_null": N_NULL,
        "k_seeds": K_SEEDS, "h2_tol": H2_TOL,
        "vms_point": {"h2": vms_h2, "block_di": vms_bdi, "mwl": vms_mwl},
        "vms_h2_ci_90": vms_h2_ci, "vms_block_di_ci_90": vms_bdi_ci,
        "plaintext_control": {"h2": plain_h2, "block_di": plain_bdi, "mwl": _mwl(base)},
        "homophony_model": "fair in-alphabet verbose homophonic (no markers); replaces the "
        "marker-injecting _homoph that the refutation pass showed deflates h2 by ~0.34 bits",
        "grid": grid,
        "configs_reaching_vms_corner": corner,
        "closest_config": {**{k: closest[k] for k in ("expansion", "h", "h2", "block_di", "mwl")},
                           "normalized_distance": round(dist(closest), 2)},
        "block_di_gap_at_h2_matched_config": bdi_gap_at_h2,
        "block_scale_di_separates_verbose_homophonic": bool(separable),
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e33_block_scale_di.json").write_text(json.dumps(results, indent=2) + "\n")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "e33_block_scale_di.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    corner = r["configs_reaching_vms_corner"]
    v, b = r["vms_point"]["h2"], r["vms_point"]["block_di"]
    dist = r["closest_config"]["normalized_distance"]
    if not corner:
        return "C", (
            f"BLOCK-SCALE, LIKE-FOR-LIKE ΔI WEAKLY SEPARATES verbose+homophonic ciphers. "
            f"Under a FAIR in-alphabet homophony model, NO config in the (verbose × homophony) "
            f"sweep reaches the VMS's (h2 {v}, block ΔI {b}) corner: the closest sits at "
            f"normalized distance {dist} (matching the VMS's block ΔI forces character entropy "
            f"h2 out of its window, and vice versa). This CORRECTS the first pass, which used a "
            f"marker-injecting homophony that deflated h2 and produced a spurious corner hit; "
            f"the refutation pass caught it (docs/refutations). Honest reading: at block scale, "
            f"like-for-like, the (h2, block-ΔI) plane does NOT collapse — matching the "
            f"manuscript's low character entropy AND its block-scale word-order information at "
            f"once is not achieved by this cipher family. This does NOT by itself revive ΔI into "
            f"a hard standalone discriminator (one soft axis, a single generative family tested, "
            f"and the verbose cipher's mean word length {r['closest_config'].get('mwl')} vs the "
            f"VMS's {r['vms_point']['mwl']} is a further mismatch), and the program-level cipher "
            f"disposition still rests on the deconfounded mid-level syntax measures (E30/E31). "
            f"But it retires the earlier 'ΔI leg is dead even at block scale' claim: it is not.")
    return "C", (
        f"Even under a fair in-alphabet homophony model, {len(corner)} verbose+homophonic "
        f"config(s) reach the VMS's (h2, block-ΔI) corner → block-scale ΔI does NOT separate "
        f"Naibbe-class ciphers → the ΔI leg does not discriminate even here; the "
        f"verbose+homophonic exclusion stays INCONCLUSIVE, resting on the soft syntax measures "
        f"(E30/E31).")


def _render(r: dict) -> str:
    g = r["grid"]
    rows = [f"| {x['expansion']} | {x['h']} | {x['h2']:.3f} | {x['block_di']:.4f} | {x['mwl']} "
            f"| {'✓' if x['h2_matches_vms'] else '·'} | {'✓' if x['bdi_matches_vms'] else '·'} "
            f"| {'CORNER' if x['reaches_corner'] else ''} |" for x in g]
    return "\n".join([
        "# E33 — Block-scale like-for-like ΔI (the last untested ΔI leg)",
        "",
        f"Generated {r['built_at']} at `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e33_block_scale_di`; numbers in "
        "`results/experiments/e33_block_scale_di.json`.",
        "",
        f"Homophony model: {r['homophony_model']}.",
        "",
        f"**VMS:** h2 {r['vms_point']['h2']} (CI {r['vms_h2_ci_90']}), "
        f"block ΔI {r['vms_point']['block_di']} (CI {r['vms_block_di_ci_90']}), "
        f"mean word length {r['vms_point']['mwl']}. "
        f"**Plaintext control** (blocked Latin, h=1): h2 {r['plaintext_control']['h2']}, "
        f"block ΔI {r['plaintext_control']['block_di']}, mwl {r['plaintext_control']['mwl']}.",
        "",
        "Verbose × homophony sweep (median over seeds); a config 'reaches the corner' if its "
        "median h2 is within tol AND its block ΔI is within the VMS CI:",
        "",
        "| verb | homoph h | h2 | block ΔI | mwl | h2✓ | ΔI✓ | |",
        "|---|---|---|---|---|---|---|---|",
        *rows,
        "",
        f"Closest config: {r['closest_config']}.",
        "",
        f"**Grade {r['grade']}.** {r['verdict']}",
        "",
    ])


if __name__ == "__main__":
    res = run()
    print(f"Grade {res['grade']}")
    print(res["verdict"])
    print("configs reaching VMS corner:", len(res["configs_reaching_vms_corner"]))
    print("closest:", res["closest_config"])
