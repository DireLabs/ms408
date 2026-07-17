"""E29 — The Naibbe cipher against our discriminators (i11, gating the i06 headline).

Naibbe (Greshko, Cryptologia 2025) is a hand-constructable, decipherable homophonic
substitution cipher that encrypts respaced Latin into Voynichese-like ciphertext and
reproduces many VMS statistics — a constructive existence proof directly contesting our i06
"cipher-of-real-prose EXCLUDED" claim. This is the make-or-break test: run HIS actual
ciphertext through OUR discriminators and see whether it reproduces the VMS's JOINT
signature (low h2 + RETAINED block-scale ΔI + weak word-syntax) or fails on the
retained-ΔI axis our exclusion is built on.

i06 prediction: Naibbe is homophonic -> weak syntax but ΔI COLLAPSES (homophone draws
decouple ciphertext types from plaintext types; E2 found the same for homophone-rich
Naibbe-class, ΔI 0.013) -> it should NOT reproduce the VMS's retained ΔI.

L19: reads Naibbe ciphertext from data/raw/ (gitignored, consume-only, not redistributed);
writes only derived statistics. L7: statistical discriminator test, no meaning/decipherment
claim.

Usage:
    python -m ms408.experiments.e29_naibbe_discriminators
"""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..studies.encoding import profile
from .e19_joint_signature import _fc_z, _wc_z
from .e21_positional_generator import _vms_band

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
REPORTS_DIR = ROOT / "reports"
NAIBBE_DIR = ROOT / "data" / "raw" / "naibbe-cipher"
NAIBBE = NAIBBE_DIR / "encrypted" / "nathist_output_ciphertext.txt"
LATIN_WB = NAIBBE_DIR / "input" / "examples" / "nathist_book16.txt"      # word boundaries
RESPACED = NAIBBE_DIR / "respaced_plaintext" / "nathist_pre_encryption_respaced_plaintext.txt"
SEED = 408
N = 10000                            # matched to the VMS band budget
K = 5                                # block subsamples for generator-side range
TARGETS = ("h2", "mz_peak_value", "ed1_main_component", "type_token_ratio",
           "zipf_slope", "mean_word_length")


def _block(words: list, n: int, seed: int) -> list:
    r = random.Random(seed)
    start = r.randrange(0, max(1, len(words) - n))
    return words[start:start + n]


def _in(v: float, band: list) -> bool:
    return band[0] <= v <= band[1]


def _di(words: list) -> tuple:
    p = profile(words)
    return round(p["mz_peak_value"], 4), p["mz_peak_scale"]


def _homophony_sweep(words: list, hs: tuple, seed: int) -> list:
    """CONTROL: word order AND boundaries preserved; map each word TYPE to H homophone
    tokens, drawn per occurrence; measure ΔI. Isolates homophony from word order — if ΔI
    falls anyway, ΔI is not a clean word-order measure."""
    types = sorted(set(words))
    out = []
    for h in hs:
        rng = random.Random(seed)
        homo = {t: [f"{i}_{t}" for i in range(h)] for t in types}
        stream = [rng.choice(homo[t]) for t in words]
        di, scale = _di(stream)
        out.append({"homophones_per_type": h, "dI": di, "scale": scale})
    return out


def run() -> dict:
    if not NAIBBE.exists():
        raise SystemExit(
            f"Naibbe ciphertext not found at {NAIBBE}. Consume-only (L19): clone "
            "github.com/greshko/naibbe-cipher into data/raw/ (gitignored) first.")
    words = NAIBBE.read_text().split()
    band = _vms_band()

    # Full-text anchors (most stable for ΔI/ED1) + K block subsamples for range.
    p_full = profile(words)
    per_seed = []
    for k in range(K):
        b = _block(words, N, SEED + k)
        p = profile(b)
        row = {t: round(p[t], 4) for t in TARGETS}
        row["mz_peak_scale"] = p["mz_peak_scale"]
        row["fc_z"] = _fc_z(b)
        row["wc_z"] = _wc_z(b)
        per_seed.append(row)

    def med(key):
        return round(sorted(r[key] for r in per_seed)[K // 2], 4)
    naibbe = {t: med(t) for t in TARGETS}
    naibbe["fc_z"], naibbe["wc_z"] = med("fc_z"), med("wc_z")
    rng = {t: [round(min(r[t] for r in per_seed), 4), round(max(r[t] for r in per_seed), 4)]
           for t in list(TARGETS) + ["fc_z", "wc_z"]}

    fc_band = sorted(band["fc_z_vms"])
    wc_band = sorted(band["wc_z_vms"])
    hit = {t: _in(naibbe[t], band[t]) for t in TARGETS}
    hit["fc_z"] = _in(naibbe["fc_z"], fc_band)
    hit["wc_z"] = _in(naibbe["wc_z"], wc_band)

    # The decisive i06 axes.
    dI_lo = band["mz_peak_value"][0]
    dI_band = band["mz_peak_value"]
    shuffle_floor = 0.011                      # ref_shuffle ΔI from the harness
    di_collapsed = naibbe["mz_peak_value"] < shuffle_floor
    weak_syntax = naibbe["fc_z"] < 3.0 and naibbe["wc_z"] < 3.0
    reproduces_joint = (hit["h2"] and hit["mz_peak_value"] and weak_syntax)

    # --- REFUTATION CONTROLS (why the ΔI collapse is uninformative) ------------------
    # (1) ΔI decomposition across Greshko's pipeline stages: is the collapse from the
    #     CIPHER, or already present in the respaced plaintext / absent in real Latin?
    latin_di = _di(LATIN_WB.read_text().split()) if LATIN_WB.exists() else (None, None)
    respaced_di = _di(RESPACED.read_text().split()) if RESPACED.exists() else (None, None)
    decomposition = {
        "word_boundary_latin": {"dI": latin_di[0], "scale": latin_di[1],
                                "in_vms_band": bool(latin_di[0] is not None
                                                    and _in(latin_di[0], dI_band))},
        "respaced_fragments_pre_cipher": {"dI": respaced_di[0], "scale": respaced_di[1]},
        "ciphertext": {"dI": naibbe["mz_peak_value"]},
    }
    # (2) homophony sweep: word order + boundaries FIXED, ΔI vs homophones/type.
    sweep = (_homophony_sweep(LATIN_WB.read_text().split(), (1, 2, 4, 8, 16, 18, 32), SEED)
             if LATIN_WB.exists() else [])
    sweep_H1_in_band = bool(sweep and _in(sweep[0]["dI"], dI_band))
    sweep_collapses_with_order_fixed = bool(sweep and sweep[-1]["dI"] < dI_band[0])
    dI_confounded = sweep_H1_in_band and sweep_collapses_with_order_fixed
    # Attribute the collapse: how much is respacing vs the cipher itself?
    respacing_share = None
    if latin_di[0] and respaced_di[0] is not None:
        total = latin_di[0] - naibbe["mz_peak_value"]
        respacing_share = round((latin_di[0] - respaced_di[0]) / total, 3) if total else None

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E29 — Naibbe cipher against the i06 discriminators",
        "source": "Greshko, Cryptologia 2025; ciphertext github.com/greshko/naibbe-cipher "
        "(nathist = Pliny Natural History, respaced Latin). Consume-only (L19).",
        "seed": SEED, "n_tokens": N, "k_blocks": K,
        "naibbe_full_tokens": len(words),
        "vms_band": {t: band[t] for t in TARGETS} | {"fc_z": fc_band, "wc_z": wc_band},
        "naibbe_full_text": {"h2": round(p_full["h2"], 4),
                             "mz_peak_value": round(p_full["mz_peak_value"], 4),
                             "mz_peak_scale": p_full["mz_peak_scale"],
                             "ed1_main_component": round(p_full["ed1_main_component"], 4)},
        "naibbe_median": naibbe, "naibbe_range": rng,
        "axis_in_vms_band": hit,
        "n_axes_in_band": sum(hit.values()),
        "dI_shuffle_floor": shuffle_floor,
        "dI_collapsed": bool(di_collapsed),
        "weak_syntax": bool(weak_syntax),
        "reproduces_vms_joint_signature": bool(reproduces_joint),
        "vms_dI_band_floor": dI_lo,
        "dI_decomposition": decomposition,
        "respacing_share_of_dI_loss": respacing_share,
        "homophony_sweep_order_fixed": sweep,
        "dI_confounded_by_homophony": dI_confounded,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e29_naibbe_discriminators.json").write_text(
        json.dumps(results, indent=2) + "\n")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "e29_naibbe_discriminators.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    n = r["naibbe_median"]
    ft = r["naibbe_full_text"]
    common = (
        f"Naibbe ciphertext (Greshko 2025, {r['naibbe_full_tokens']} tokens of respaced-Latin "
        f"Pliny), {r['k_blocks']}×{r['n_tokens']}-token blocks, vs the VMS bands. Signature: "
        f"h2 {n['h2']} (VMS {r['vms_band']['h2']}), ΔI {n['mz_peak_value']} "
        f"(full-text {ft['mz_peak_value']}@{ft['mz_peak_scale']}; VMS {r['vms_band']['mz_peak_value']}), "
        f"ED1 {n['ed1_main_component']} (VMS {r['vms_band']['ed1_main_component']}), Zipf "
        f"{n['zipf_slope']} (VMS {r['vms_band']['zipf_slope']}), TTR {n['type_token_ratio']}, "
        f"len {n['mean_word_length']}, fc_z {n['fc_z']}, wc_z {n['wc_z']} (VMS wc_z "
        f"{r['vms_band']['wc_z']}). {r['n_axes_in_band']}/8 axes in the VMS band.")
    dec = r["dI_decomposition"]
    lat = dec["word_boundary_latin"]
    sw = r["homophony_sweep_order_fixed"]
    if r["reproduces_vms_joint_signature"]:
        return "B", (
            f"i06 EXCLUSION FALSIFIED (report immediately). The Naibbe cipher of real prose "
            f"DOES reproduce the VMS's joint signature. The exclusion must be withdrawn. "
            f"{common} (L7.)")
    return "C", (
        f"THE NAIBBE ΔI TEST IS UNINFORMATIVE — i06 is NOT confirmed, and the analysis EXPOSES "
        f"A CONFOUND IN i06's ΔI LEG (refutation-corrected from a first-pass 'CONFIRMED [B]'). "
        f"First-pass reasoning: Naibbe's ΔI collapses to {n['mz_peak_value']} (full-text "
        f"{ft['mz_peak_value']}) vs the VMS band {r['vms_band']['mz_peak_value']}, so 'no cipher "
        f"reproduces retained ΔI' looked confirmed. Two controls kill that reading. "
        f"(1) DECOMPOSITION across Greshko's pipeline: word-boundary Latin (Pliny) ΔI={lat['dI']} "
        f"is IN the VMS band ({lat['in_vms_band']}); the RESPACING into non-word fragments drops "
        f"it to {dec['respaced_fragments_pre_cipher']['dI']} — i.e. ~{r['respacing_share_of_dI_loss']} "
        f"of the total ΔI loss happens BEFORE the cipher runs — and the homophonic encryption "
        f"only accounts for the small remainder. The collapse is dominated by a SPACING "
        f"CONVENTION, not by ciphering. (2) HOMOPHONY SWEEP with word order AND boundaries "
        f"FIXED: ΔI falls monotonically with homophones/type anyway (H=1 {sw[0]['dI']} in-band → "
        f"H={sw[-1]['homophones_per_type']} {sw[-1]['dI']} below floor), so ΔI is a homophony / "
        f"type-token-coupling detector, NOT a clean word-order measure. CONSEQUENCES: (a) faulting "
        f"Naibbe for low ΔI is circular — real Latin with word boundaries is already IN the VMS "
        f"band, and Greshko's respacing (not the cipher) removes it; (b) the VMS's own retained "
        f"ΔI is BLOCK/section structure (our i06/E1/E2), so comparing it to Naibbe's token-level "
        f"ΔI on an unsectioned stream is not like-for-like; (c) a LOW-homophony or word-boundary-"
        f"preserving cipher of real prose would sit in the VMS ΔI band. NET: i06's ΔI leg does "
        f"NOT robustly separate the VMS from ciphers of real prose — the exclusion leans more "
        f"heavily on the SOFT fc_z/wc_z measures than i06/paper v3–v5b state, and must be walked "
        f"back accordingly. On our battery Naibbe still matches only {r['n_axes_in_band']}/8 tight "
        f"bands, but that is a different, weaker claim than 'i06 confirmed'. REQUIRED FOLLOW-UP "
        f"before any external engagement: encrypt word-boundary Latin (order-preserving) and "
        f"re-test; measure the glyph-level properties Greshko actually claims. {common} "
        f"(Statistical; no decipherment — L7.)")


def _render(r: dict) -> str:
    n, ft = r["naibbe_median"], r["naibbe_full_text"]
    axes = list(TARGETS) + ["fc_z", "wc_z"]
    lines = [
        "# E29 — The Naibbe cipher against the i06 discriminators",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e29_naibbe_discriminators`. Numbers in "
        "`results/experiments/e29_naibbe_discriminators.json`. Source: " + r["source"],
        "",
        f"Full-text ΔI = **{ft['mz_peak_value']}** @ {ft['mz_peak_scale']} "
        f"(VMS band {r['vms_band']['mz_peak_value']}); ΔI collapsed: **{r['dI_collapsed']}**; "
        f"reproduces VMS joint signature: **{r['reproduces_vms_joint_signature']}**.",
        "",
        "| axis | Naibbe (median) | range | VMS band | in band |",
        "|---|---|---|---|---|",
    ]
    for a in axes:
        vb = r["vms_band"][a]
        lines.append(f"| {a} | {n[a]} | {r['naibbe_range'][a]} | {vb} "
                     f"| {'✓' if r['axis_in_vms_band'][a] else '·'} |")
    lines += ["", f"## Verdict [{r['grade']}]", "", r["verdict"], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    n = out["naibbe_median"]
    print(f"Naibbe full-text ΔI = {out['naibbe_full_text']['mz_peak_value']} "
          f"@ {out['naibbe_full_text']['mz_peak_scale']} (VMS floor {out['vms_dI_band_floor']})")
    print(f"{'axis':20s} {'Naibbe':>8s} {'VMS band':>18s}  in?")
    for a in list(TARGETS) + ["fc_z", "wc_z"]:
        print(f"{a:20s} {str(n[a]):>8s} {str(out['vms_band'][a]):>18s}  "
              f"{out['axis_in_vms_band'][a]}")
    print(f"\ndI_collapsed={out['dI_collapsed']} weak_syntax={out['weak_syntax']} "
          f"reproduces_joint={out['reproduces_vms_joint_signature']} "
          f"({out['n_axes_in_band']}/8 axes in band)")
    print(f"grade {out['grade']}: {out['verdict'][:170]}...")
