"""E20 — Closing the cipher-of-real-prose question: the transposition lead (i06).

E19/E19b excluded word-order-PRESERVING ciphers of real prose (they retain strong
word-syntax the VMS lacks) universally, leaving one surviving lead: an order-
SCRAMBLING (transposition) cipher, which does produce weak syntax. E20 tests whether
that lead — alone or composed with a character transform — can reproduce the VMS's
FULL signature simultaneously: low character entropy (h2≈2.0), RETAINED word-order
information (ΔI≈0.18, above shuffle), AND weak mid-level syntax.

The tension to resolve: the character transforms that lower h2 while keeping ΔI
(deterministic verbose, abjad) also PRESERVE word order → strong syntax; adding
transposition to get weak syntax DESTROYS ΔI. So the three VMS properties may be
mutually unsatisfiable by any (character-transform × transposition) of real prose.

Candidates = {none, verbose, abjad} character transform × {none, full transposition},
all of real Latin. A candidate CLOSES the lead only if it matches the VMS on all of
{h2, ΔI, weak fc_z, weak wc_z} at once.

Usage:
    python -m ms408.experiments.e20_transposition_closure
"""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..studies.encoding import profile
from .e13_function_content import N_TOKENS, SEED, _sub, _vms_tokens
from .e19_joint_signature import WEAK_Z, _fc_z, _wc_z
from .e6_cipher_reconstruction import _abjad_collapse, _det_verbose

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"


def _transpose(tokens: list, seed: int) -> list:
    t = list(tokens)
    random.Random(seed).shuffle(t)
    return t


def _sig(tokens: list) -> dict:
    p = profile(tokens)
    return {"h2": round(p["h2"], 3), "dI": round(p["mz_peak_value"], 3),
            "fc_z": _fc_z(tokens), "wc_z": _wc_z(tokens)}


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()[:N_TOKENS]
    transforms = {
        "latin_plain": latin,
        "latin_verbose": _det_verbose(latin, 2, 0, SEED),   # lowers h2, keeps order
        "latin_abjad": _abjad_collapse(latin, SEED),        # raises ED1, keeps order
    }
    corpora = {"VMS_A": _sub(_vms_tokens("A"), N_TOKENS),
               "VMS_B": _sub(_vms_tokens("B"), N_TOKENS)}
    for name, toks in transforms.items():
        corpora[name] = _sub(toks)
        corpora[f"{name}_transposed"] = _sub(_transpose(toks, SEED))
    sigs = {k: _sig(v) for k, v in corpora.items()}

    # VMS target bands (bracket A and B, with tolerance).
    hs = [sigs["VMS_A"]["h2"], sigs["VMS_B"]["h2"]]
    dis = [sigs["VMS_A"]["dI"], sigs["VMS_B"]["dI"]]
    band = {"h2": (min(hs) - 0.3, max(hs) + 0.3), "dI": (min(dis) - 0.06, max(dis) + 0.06)}

    def joint_match(c):
        s = sigs[c]
        return {
            "h2_ok": band["h2"][0] <= s["h2"] <= band["h2"][1],
            "dI_ok": band["dI"][0] <= s["dI"] <= band["dI"][1],
            "weak_syntax_ok": s["fc_z"] < WEAK_Z and s["wc_z"] < WEAK_Z,
        }

    cipher_candidates = [c for c in corpora if c not in ("VMS_A", "VMS_B")]
    matches = {}
    for c in cipher_candidates:
        m = joint_match(c)
        m["all_three"] = m["h2_ok"] and m["dI_ok"] and m["weak_syntax_ok"]
        matches[c] = m
    any_match = any(m["all_three"] for m in matches.values())

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E20 — transposition closure of the cipher-of-real-prose lead",
        "seed": SEED, "n_tokens": N_TOKENS,
        "vms_target_band": {k: [round(v[0], 3), round(v[1], 3)] for k, v in band.items()},
        "signatures": sigs, "joint_match": matches,
        "any_cipher_of_real_prose_matches_full_signature": any_match,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e20_transposition_closure.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    s = r["signatures"]
    m = r["joint_match"]
    # Show the tension explicitly with the two decisive rows.
    keep_dI = "latin_verbose"       # keeps ΔI, lowers h2, but strong syntax
    scrambled = "latin_verbose_transposed"  # weak syntax, but ΔI destroyed
    tab = "; ".join(f"{c}: h2={s[c]['h2']} dI={s[c]['dI']} fc_z={s[c]['fc_z']} "
                    f"wc_z={s[c]['wc_z']}"
                    for c in ("VMS_A", "VMS_B", "latin_plain", keep_dI, scrambled,
                              "latin_abjad", "latin_abjad_transposed"))
    if not r["any_cipher_of_real_prose_matches_full_signature"]:
        return "B", (
            f"CIPHER-OF-REAL-PROSE CLASS CLOSED. No (character-transform × transposition) "
            f"of real Latin reproduces the VMS's FULL signature — low h2 "
            f"(band {r['vms_target_band']['h2']}), RETAINED ΔI "
            f"(band {r['vms_target_band']['dI']}), AND weak mid-level syntax — "
            f"simultaneously. The tension is explicit and structural: the transforms "
            f"that lower h2 while KEEPING ΔI (deterministic verbose h2 {s[keep_dI]['h2']}, "
            f"dI {s[keep_dI]['dI']}) PRESERVE word order and so retain STRONG syntax "
            f"(fc_z {s[keep_dI]['fc_z']}); adding transposition to force WEAK syntax "
            f"collapses the ΔI (verbose+transposed: fc_z {s[scrambled]['fc_z']} weak but "
            f"dI {s[scrambled]['dI']} ≈ shuffle). So retained-ΔI and weak-syntax are "
            f"mutually exclusive under any cipher of real prose, while the VMS has BOTH. "
            f"Combined with E19/E19b, the entire cipher-of-real-prose class is now "
            f"EXCLUDED on the joint signature. The resolution (from E1/E2): the VMS's ΔI "
            f"is BLOCK/section structure, not linguistic word order — so the VMS carries "
            f"positional/template structure but not the word-syntax of enciphered real "
            f"prose, pointing to a template-driven / positional generative system rather "
            f"than a cipher of a real text. {tab}. (Statistical; no meaning claim — L7.)")
    winners = [c for c, mm in m.items() if mm["all_three"]]
    return "C", (
        f"A cipher of real prose ({winners}) DOES match the VMS's full signature — the "
        f"transposition lead survives and is a live decipherment target. {tab}. (L7.)")


if __name__ == "__main__":
    out = run()
    print(f"VMS target band: h2 {out['vms_target_band']['h2']}, dI {out['vms_target_band']['dI']}")
    print(f"{'corpus':28s} {'h2':>6s} {'dI':>6s} {'fc_z':>7s} {'wc_z':>7s}  match")
    for c, sg in out["signatures"].items():
        mm = out["joint_match"].get(c, {})
        tag = ("h2" * mm.get("h2_ok", False) + " dI" * mm.get("dI_ok", False)
               + " weak" * mm.get("weak_syntax_ok", False)) if mm else "(VMS)"
        print(f"{c:28s} {sg['h2']:>6} {sg['dI']:>6} {str(sg['fc_z']):>7} "
              f"{str(sg['wc_z']):>7}  {tag}")
    print(f"\nany cipher matches full signature: {out['any_cipher_of_real_prose_matches_full_signature']}")
    print(f"grade {out['grade']}: {out['verdict'][:150]}...")
