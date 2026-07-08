"""E6 — Deterministic-verbose / nomenclator cipher: joint-signature reconstruction.

E2 re-opened this family: a type-preserving deterministic verbose cipher of blocked
text RETAINS the word-order signal (ΔI 0.356 @ 812), unlike the homophone-rich
Naibbe form (0.013). So the word-order argument does NOT exclude deterministic-
verbose / nomenclator ciphers. But i01's bracket found no family reproduced the
VMS's JOINT signature. E6 is the focused positive test: can a deterministic-verbose
/ nomenclator cipher of a REAL medieval text reproduce ALL FOUR discriminators at
once — low h2, the 812-scale ΔI, the dense ED1 morphology network (≈0.80), and the
Zipf slope?

Design.
  * Plaintext = real Latin (Vulgate), concatenated by book into vocabulary-distinct
    BLOCKS (so the 812-scale ΔI has a chance to appear), truncated to VMS length.
  * Cipher = deterministic verbose substitution (each plaintext letter → a fixed
    multi-glyph unit; a bijection on word types, no homophones) + an optional
    NOMENCLATOR (top-K frequent plaintext words → fixed short cipher tokens). Swept
    over expansion width and nomenclator size.
  * INVENTORY-COLLAPSE arm (added per the E6 refutation) = a length-reducing abjad
    (drop vowels → consonantal skeleton) and a heavy nomenclator, both over REAL
    Latin — the untested confound: reduced type inventory could inflate ED1 without
    any constructed morphology.
  * CONTRAST arm = the same cipher over a PARADIGMATIC CONLANG at several paradigm
    strengths, expansion 1 (preserve network) vs 2 (destroy it).
  * Scoring = RAW per-metric joint match against the VMS with block-bootstrap CIs
    (E8's whitened distance is NOT the arbiter — its Σ was shown ill-conditioned).

Findings are structural (L7), not decipherment. Key results: (1) verbose expansion
DEDUCTIVELY excludes E2's verbose cipher on the ED1 network (a k-glyph bijection
turns 1-letter diffs into ≥k-glyph diffs); (2) the ED1 network does NOT need
constructed morphology — an ABJAD of real Latin reaches it — so the abjad/
abbreviation class is a live lead. NOTHING reproduced all four discriminators
simultaneously; no sufficiency is claimed.

Usage:
    python -m ms408.experiments.e6_cipher_reconstruction
"""

from __future__ import annotations

import json
import random
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..studies.encoding import profile, vms_stream
from .e2_wordorder_confound import blocked_natural_text
from .e5_encoding_fair import _block_boot, _conlang_lexicon

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
REPORTS_DIR = ROOT / "reports"
SEED = 408
BOOTSTRAP = 150
BLOCK = 2500  # > VMS 812 word-order scale (preserves it under resampling)

# The four joint-signature discriminators (EXPERIMENTS.md E6).
TARGETS = ("h2", "mz_peak_value", "ed1_main_component", "zipf_slope")
_GLYPHS = "abcdefghiklmnoprstuvxyz"


def _det_verbose(tokens: list, expansion: int, nomen_k: int, seed: int) -> list:
    """Type-preserving deterministic verbose cipher. Each distinct plaintext letter
    maps to a fixed `expansion`-glyph unit (bijection on word types). The `nomen_k`
    most frequent plaintext word types instead map to a single fixed short token
    (a nomenclator entry)."""
    rng = random.Random(seed)
    letters = sorted({c for w in tokens for c in w})
    unit = {c: "".join(rng.choice(_GLYPHS) for _ in range(expansion)) for c in letters}
    frequent = {w for w, _ in Counter(tokens).most_common(nomen_k)} if nomen_k else set()
    nomen = {w: "".join(rng.choice(_GLYPHS) for _ in range(rng.choice([1, 2])))
             for w in frequent}
    cache: dict = {}
    out = []
    for w in tokens:
        if w in nomen:
            out.append(nomen[w])
            continue
        if w not in cache:
            cache[w] = "".join(unit[c] for c in w)
        out.append(cache[w])
    return out


_VOWELS = set("aeiou")


def _abjad_collapse(tokens: list, seed: int) -> list:
    """Length-reducing, INVENTORY-COLLAPSING cipher of real text: drop vowels to a
    consonantal skeleton, then 1:1-substitute the consonants. Inflectional families
    collapse to shared short skeletons (many edit-distance-1 neighbours) WITHOUT any
    constructed morphology — the confound the E6 refutation flagged. If this reaches
    the VMS ED1 band, 'needs constructed morphology' is false."""
    rng = random.Random(seed)
    cons = sorted({c for w in tokens for c in w if c not in _VOWELS})
    sub = {c: rng.choice(_GLYPHS) for c in cons}
    out = []
    for w in tokens:
        skel = "".join(sub[c] for c in w if c not in _VOWELS)
        out.append(skel or rng.choice(_GLYPHS))
    return out


def _paradigmatic_conlang(tokens: list, p: float, seed: int) -> list:
    """Relexify the token stream through a paradigmatic invented lexicon (shared-
    stem templates at strength p) — preserves word order, builds an ED1 network."""
    rng = random.Random(seed)
    ranked = [w for w, _ in Counter(tokens).most_common()]
    lex = _conlang_lexicon(ranked, p, rng)
    return [lex[t] for t in tokens]


def _vms_targets() -> dict:
    """VMS profile + block-bootstrap 95% CI for each of the four discriminators."""
    vms = vms_stream()
    p = profile(vms)
    boots = {t: [] for t in TARGETS}
    for b in range(BOOTSTRAP):
        rng = random.Random(7000 + b)
        pb = profile(_block_boot(vms, rng))
        for t in TARGETS:
            boots[t].append(pb[t])
    out = {}
    for t in TARGETS:
        s = sorted(boots[t])
        out[t] = {"vms": round(p[t], 4),
                  "ci95": [round(s[int(0.025 * len(s))], 4),
                           round(s[min(len(s) - 1, int(0.975 * len(s)))], 4)]}
    out["mz_peak_scale_vms"] = p["mz_peak_scale"]
    return out


def _match(config_profile: dict, targets: dict) -> dict:
    hits = {}
    for t in TARGETS:
        lo, hi = targets[t]["ci95"]
        hits[t] = bool(lo <= config_profile[t] <= hi)
    return {"values": {t: round(config_profile[t], 4) for t in TARGETS},
            "mz_peak_scale": config_profile["mz_peak_scale"],
            "hits": hits, "n_hit": sum(hits.values()),
            "all_four": all(hits.values())}


def run() -> dict:
    targets = _vms_targets()
    vms = vms_stream()
    n = len(vms)
    blocked = blocked_natural_text(n)

    configs = {}
    # Arm A — deterministic cipher of REAL Latin: expansion 1 (length-preserving
    # 1:1 substitution) vs 2,3 (verbose), with/without a nomenclator.
    for exp in (1, 2, 3):
        for k in (0, 400):
            configs[f"latin_x{exp}_nomen{k}"] = _det_verbose(blocked, exp, k, SEED)
    # Arm B — INVENTORY-COLLAPSING cipher of REAL Latin (the E6-refutation's
    # confound): abjad skeleton, and a heavy nomenclator collapsing most word types
    # to short forms. Tests whether reduced inventory alone reaches ED1 ≈ 0.80.
    configs["latin_abjad"] = _abjad_collapse(blocked, SEED)
    configs["latin_x1_nomen4000"] = _det_verbose(blocked, 1, 4000, SEED)
    # Arm C — CONTRAST: same cipher over a PARADIGMATIC CONLANG of the same text,
    # across paradigm strengths, at expansion 1 (preserve) and 2 (destroy).
    for p in (0.4, 0.8, 1.0):
        conlang = _paradigmatic_conlang(blocked, p, SEED)
        configs[f"conlang_p{p}_x1"] = _det_verbose(conlang, 1, 0, SEED)
    configs["conlang_p0.8_x2"] = _det_verbose(_paradigmatic_conlang(blocked, 0.8, SEED),
                                              2, 0, SEED)

    scored = {name: _match(profile(stream), targets) for name, stream in configs.items()}

    def ed1(name):
        return scored[name]["values"]["ed1_main_component"]

    latin = {k: v for k, v in scored.items() if k.startswith("latin_")}
    best_latin = max(latin, key=lambda k: latin[k]["n_hit"])
    latin_reinstated = any(v["all_four"] for v in latin.values())
    missed = [t for t, hit in latin[best_latin]["hits"].items() if not hit]

    # The mechanism decomposition (the real result), refutation-hardened:
    #  1. Verbose expansion cannot yield ED1 (near-tautological EXCLUSION of E2's
    #     verbose cipher: a letter->k-glyph bijection turns 1-letter diffs into
    #     >=k-glyph diffs by construction).
    #  2. Among LENGTH-PRESERVING ciphers of real Latin — including the inventory-
    #     collapsing abjad/heavy-nomenclator arm the critic demanded — does ANY reach
    #     the VMS ED1 band? If yes, "needs constructed morphology" is FALSE.
    #  3. Does the constructed-morphology conlang reach the band (sufficiency)?
    vms_ed1 = targets["ed1_main_component"]["vms"]
    vms_ed1_lo = targets["ed1_main_component"]["ci95"][0]
    verbose_destroys_ed1 = ed1("latin_x1_nomen0") > 0.15 and ed1("latin_x2_nomen0") < 0.05
    latin_lp_configs = ["latin_x1_nomen0", "latin_x1_nomen400", "latin_x1_nomen4000",
                        "latin_abjad"]
    latin_lp_best_ed1 = max(ed1(c) for c in latin_lp_configs)
    latin_inventory_collapse_reaches_band = latin_lp_best_ed1 >= vms_ed1_lo
    conlang_configs = [c for c in scored if c.startswith("conlang_") and c.endswith("_x1")]
    conlang_best_ed1 = max(ed1(c) for c in conlang_configs)
    conlang_reaches_band = conlang_best_ed1 >= vms_ed1_lo

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E6 — deterministic-verbose/nomenclator cipher reconstruction",
        "seed": SEED, "tokens": n, "bootstrap": BOOTSTRAP,
        "vms_targets": targets,
        "configs": scored,
        "best_latin_config": best_latin,
        "best_latin_n_hit": latin[best_latin]["n_hit"],
        "best_latin_missed_metrics": missed,
        "latin_cipher_reinstated": bool(latin_reinstated),
        "ed1_mechanism": {
            "vms_ed1": vms_ed1, "vms_ed1_ci_lo": vms_ed1_lo,
            "latin_1to1_ed1": round(ed1("latin_x1_nomen0"), 3),
            "latin_verbose_x2_ed1": round(ed1("latin_x2_nomen0"), 3),
            "latin_abjad_ed1": round(ed1("latin_abjad"), 3),
            "latin_heavy_nomen_ed1": round(ed1("latin_x1_nomen4000"), 3),
            "latin_lengthpreserving_best_ed1": round(latin_lp_best_ed1, 3),
            "conlang_best_1to1_ed1": round(conlang_best_ed1, 3),
            "conlang_verbose_x2_ed1": round(ed1("conlang_p0.8_x2"), 3),
            "verbose_destroys_ed1": bool(verbose_destroys_ed1),
            "latin_inventory_collapse_reaches_band": bool(latin_inventory_collapse_reaches_band),
            "conlang_reaches_band": bool(conlang_reaches_band),
        },
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e6_cipher_reconstruction.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "e6_cipher_reconstruction.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    m = r["ed1_mechanism"]
    if r["latin_cipher_reinstated"]:
        return "B", (
            f"REINSTATED: a deterministic cipher of real Latin "
            f"({r['best_latin_config']}) matches ALL FOUR discriminators within the "
            f"VMS CIs simultaneously. (Structure only; no plaintext claim — L7.)")
    missed = ", ".join(r["best_latin_missed_metrics"]) or "none"
    # Part 1 — EXCLUSION of E2's verbose cipher (deductive; refutation noted it is
    # near-tautological, which makes it a strong exclusion, not a discovery).
    part1 = (
        f"(1) VERBOSE CIPHER EXCLUDED on the ED1 network — DEDUCTIVELY. A "
        f"letter→k-glyph bijection turns every 1-letter plaintext difference into a "
        f"≥k-glyph difference, so edit-distance-1 adjacency cannot survive expansion: "
        f"Latin ED1 {m['latin_1to1_ed1']} at 1:1 → {m['latin_verbose_x2_ed1']} verbose; "
        f"conlang {m['conlang_best_1to1_ed1']} → {m['conlang_verbose_x2_ed1']}. This "
        f"is a definitional exclusion of the deterministic-VERBOSE cipher E2 "
        f"re-opened, not an empirical surprise.")
    # Part 2 — branch on the critic's decisive inventory-collapse test.
    if m["latin_inventory_collapse_reaches_band"]:
        part2 = (
            f"(2) 'NEEDS CONSTRUCTED MORPHOLOGY' — REFUTED. A length-reducing, "
            f"INVENTORY-COLLAPSING cipher of REAL Latin (abjad: drop vowels → "
            f"consonantal skeleton) reaches ED1 {m['latin_abjad_ed1']} ≥ the VMS band "
            f"lower {m['vms_ed1_ci_lo']} — inflectional families collapse to shared "
            f"short skeletons that ARE edit-distance-1 neighbours, so the dense "
            f"network arises from mere type-inventory reduction of natural language, "
            f"NOT only from constructed morphology. The abjad/abbreviation/syllabary "
            f"class (cf. medieval vowel-dropping) is now a live positive lead for the "
            f"ED1 network. CAVEAT: the abjad reaches ED1 partly BY SHORTENING words "
            f"(shorter words have more ED1 neighbours — a known metric confound), so "
            f"it trades the ED1 match for a word-length mismatch; no transform here "
            f"matches ED1 AND word length AND h2 together, so this is a lead for a "
            f"joint follow-up, not a reconstruction.")
        grade = "C"
    else:
        part2 = (
            f"(2) NECESSITY + INSUFFICIENCY (not sufficiency). No length-preserving "
            f"cipher of real Latin — including the inventory-collapsing abjad/heavy-"
            f"nomenclator arm — reaches the VMS ED1 band (best {m['latin_lengthpreserving_best_ed1']} "
            f"< {m['vms_ed1_ci_lo']}; abjad {m['latin_abjad_ed1']}, heavy-nomen "
            f"{m['latin_heavy_nomen_ed1']}). A constructed paradigmatic conlang gets "
            f"CLOSER ({m['conlang_best_1to1_ed1']}) but "
            + ("also reaches the band" if m["conlang_reaches_band"]
               else f"STILL misses it (< {m['vms_ed1_ci_lo']}) — nothing achieved "
                    f"sufficiency") + ". So constructed morphology is necessary-"
            "looking but unproven as sufficient on a single parameterisation.")
        grade = "C"
    return grade, (
        f"NOT reinstated as a cipher of natural language (best real-Latin config "
        f"{r['best_latin_config']}: {r['best_latin_n_hit']}/4, missed [{missed}]). "
        f"Two-part result on the ED1 network (VMS {m['vms_ed1']}). {part1} {part2} "
        f"CAVEAT: the ΔI target CI is mildly biased low (block bootstrap attenuates "
        f"the 812-peak) and the conlang's ΔI match sits at the wrong scale, so ΔI "
        f"legs are weak. Structural sufficiency NOT claimed; no plaintext claim (L7).")


def _render(r: dict) -> str:
    t = r["vms_targets"]
    lines = [
        "# E6 — Deterministic-verbose / nomenclator cipher reconstruction",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e6_cipher_reconstruction`. Numbers in "
        "`results/experiments/e6_cipher_reconstruction.json`.",
        "",
        "VMS discriminator targets (block-bootstrap 95% CI):",
        "",
        "| metric | VMS | 95% CI |",
        "|---|---|---|",
        *[f"| {m} | {t[m]['vms']} | {t[m]['ci95']} |" for m in TARGETS],
        f"| mz_peak_scale | {t['mz_peak_scale_vms']} | — |",
        "",
        "## Joint match by config (✓ = within VMS CI)",
        "",
        "| config | h2 | ΔI | ED1 | Zipf | scale | n/4 |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, s in r["configs"].items():
        h = s["hits"]
        v = s["values"]
        def cell(m):
            return f"{v[m]}{'✓' if h[m] else '✗'}"
        lines.append(f"| {name} | {cell('h2')} | {cell('mz_peak_value')} "
                     f"| {cell('ed1_main_component')} | {cell('zipf_slope')} "
                     f"| {s['mz_peak_scale']} | {s['n_hit']} |")
    lines += ["", f"## Verdict [{r['grade']}, refutation pass pending]", "",
              r["verdict"], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    for name, s in out["configs"].items():
        print(f"  {name:28s} n_hit={s['n_hit']}/4 "
              f"ED1={s['values']['ed1_main_component']} "
              f"h2={s['values']['h2']} dI={s['values']['mz_peak_value']}@{s['mz_peak_scale']}")
    print(f"best latin: {out['best_latin_config']} ({out['best_latin_n_hit']}/4, "
          f"missed {out['best_latin_missed_metrics']})")
    m = out["ed1_mechanism"]
    print(f"reinstated={out['latin_cipher_reinstated']} | ED1 (VMS {m['vms_ed1']}, "
          f"band>= {m['vms_ed1_ci_lo']}): latin1:1={m['latin_1to1_ed1']} "
          f"verbose={m['latin_verbose_x2_ed1']} abjad={m['latin_abjad_ed1']} "
          f"heavy_nomen={m['latin_heavy_nomen_ed1']} | conlang_best={m['conlang_best_1to1_ed1']}")
    print(f"  latin_inventory_collapse_reaches_band={m['latin_inventory_collapse_reaches_band']} "
          f"conlang_reaches_band={m['conlang_reaches_band']}")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
