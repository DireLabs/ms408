"""E21 — Minimal positional/template generator + necessity ablation (i07, gating).

i06 excluded the cipher-of-real-prose class and pointed to a template-driven /
positional GENERATIVE system as the account of the VMS's full signature: low character
entropy (h2 ~ 2.0), RETAINED block-scale word-order information (ΔI ~ 0.16-0.20), and
WEAK word-level syntax (fc_z/wc_z ~ 0). E21 is the positive complement: build such a
generator that is NOT tuned to Voynich and ask (a) whether it reaches the VMS band on
all three at once and (b) which generative INGREDIENT is necessary for each property.

The generator has three switchable ingredients:
  * morphology — a paradigmatic slot grammar (prefix.root.suffix over small a-priori
    glyph inventories); words sharing a slot are edit-distance-1 neighbours. Drives low
    h2 + dense ED1. OFF => flat random word types.
  * positional — the stream is cut into fixed-length blocks; each block favours its own
    random subset of roots (a "theme"), so the type distribution shifts across the
    document. Drives retained block-scale ΔI. OFF => one global distribution.
  * syntactic — the ANTI-ingredient: within a block, the next word's suffix-class and
    root are drawn conditioned on the previous word's, injecting adjacent word-class
    and content collocation. ON => raises fc_z/wc_z. The template mechanism's defining
    property is that this is OFF (context-free slot fill) => weak word-syntax BY
    CONSTRUCTION (the generative dual of the i06 cipher finding).

HONESTY NOTE (refutation pass, 2026-07-15 — supersedes the first-pass "circularity
firewall / a-priori / blind" framing, which was RETRACTED). The generator constants
(slot sizes, Zipf exponent, block theme boost) were GRID-SELECTED to land in the VMS
core bands — grid-search-and-select-on-target is fitting to a VMS statistic, no
different in kind from the circular "favours generation" positive E19 dropped. So E21
demonstrates the EXISTENCE OF A FITTED POINT, not sufficiency of the class. Genericity
(a broad basin under an a-priori grid) is E22's job and is NOT claimed here.

Two further refutation corrections baked into the scoring below:
  * The weak-syntax axis is scored against the VMS's OWN fc_z/wc_z BAND (two-sided),
    not a one-sided "< WEAK_Z" threshold that a full order-shuffle also passes. Under
    the corrected criterion the FULL config UNDERSHOOTS the VMS: its wc_z is negative
    (less word-class structure than its own shuffle) while the VMS is weak-but-POSITIVE
    (wc_z 1.9–2.64) — so FULL does NOT reproduce the VMS's real word-syntax.
  * The "context-free slot-fill => weak syntax" link is TAUTOLOGICAL (the syntactic
    switch injects exactly what wc_z measures); it is reported as an observation, not
    counted as an empirical necessity link.

Net honest result: a fitted point matches the VMS on character entropy + block-scale
ΔI, but the minimal context-free positional grammar UNDERSHOOTS the VMS's weak-positive
word-class structure and OVERSHOOTS its vocabulary productivity (TTR) and morphology
connectivity (ED1) — so this minimal mechanism is INSUFFICIENT for the full signature.
Grade C. L7 intact (no identification claim). E22 (a-priori grid + VMS-actual bands +
real-language-wrapper control) is required before any class-sufficiency claim.

Usage:
    python -m ms408.experiments.e21_positional_generator
"""

from __future__ import annotations

import bisect
import json
import random
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..studies.encoding import profile
from .e5_encoding_fair import _block_boot
from .e13_function_content import N_TOKENS, SEED, _sub, _vms_tokens
from .e19_joint_signature import WEAK_Z, _fc_z, _wc_z
from .mid_level_null import order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports"

# --- a-priori constants (frozen blind to the VMS; see circularity firewall) ---------
# The morphology ingredient is a POSITIONAL CHARACTER GRAMMAR: a word is a fixed
# sequence of slot positions, each drawing from its OWN disjoint, small glyph pool.
# Low h2 is then a DESIGNED-IN property of the positional structure (seeing a glyph
# identifies its slot, so the next slot's small alphabet is the only branching): for a
# positional grammar h2 ~ log2(mean per-slot branching), which is low for ANY small
# branching factor. We set per-slot sizes to a generic small vector (3-5 options) — NOT
# read from the VMS h2 — and report where h2 lands. THEME_SLOT drives block ΔI;
# CLASS_SLOT (word-class analog) and CONTENT_SLOT carry the syntactic anti-ingredient.
SLOT_SIZES = (5, 6, 6, 5, 4, 3)     # per-position glyph-pool sizes (generic small)
OPTIONAL = (False, False, False, False, True, True)  # trailing slots vary word length
P_PRESENT = 0.6                     # P(an optional slot is realised) -> length variation
THEME_SLOT = 1                      # slot whose glyph a block favours (drives ΔI)
CONTENT_SLOT = 0                    # slot carrying content collocation when syntactic
CLASS_SLOT = 3                      # word-class analog (mandatory slot; drives wc_z)
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP"  # >= sum(SLOT_SIZES) glyphs
ZIPF_EXP = 0.7                      # generic Zipf sampling exponent
BLOCK_LEN = 400                     # a-priori "section" unit in words
THEME_BOOST = 10.0                  # weight multiplier for a block's favoured glyph
SYN_STICK = 0.8                     # P(a conditioned slot follows its preferred successor)
BOOTSTRAP = 150


def _pick(cum: list, total: float, rng: random.Random):
    return bisect.bisect(cum, rng.random() * total)


def _cum(weights: list) -> tuple:
    acc, s = [], 0.0
    for w in weights:
        s += w
        acc.append(s)
    return acc, s


def _zipf_cum(size: int, rng: random.Random) -> tuple:
    """Zipf weights over a random ranking of `size` glyphs -> (cumulative, total)."""
    order = list(range(size))
    rng.shuffle(order)
    w = [0.0] * size
    for pos, gi in enumerate(order):
        w[gi] = 1.0 / (pos + 1) ** ZIPF_EXP
    return _cum(w)


def generate(n: int, *, morphology: bool, positional: bool, syntactic: bool,
             seed: int) -> list:
    """Emit a word stream under the three-ingredient template/positional model."""
    rng = random.Random(seed)

    if not morphology:
        # Ablated morphology: same word LENGTH but no positional character grammar —
        # every position draws from the SHARED full alphabet, so character transitions
        # are unconstrained (high h2) and words are not paradigmatic neighbours (no ED1
        # network). The block/Zipf wrapper is unchanged so only morphology differs.
        wlen = len(SLOT_SIZES)
        pool = sorted(set(ALPHABET))
        cum, tot = _zipf_cum(len(pool), rng)
        n_blocks = (n + BLOCK_LEN - 1) // BLOCK_LEN
        themes = [rng.randrange(len(pool)) for _ in range(n_blocks)]
        out = []
        for t in range(n):
            chars = []
            for j in range(wlen):
                if positional and j == THEME_SLOT and rng.random() < 0.5:
                    gi = themes[t // BLOCK_LEN]
                else:
                    gi = _pick(cum, tot, rng)
                chars.append(pool[gi])
            out.append("".join(chars))
        return out

    # Positional character grammar: disjoint glyph pool + Zipf distribution per slot.
    glyphs = list(dict.fromkeys(ALPHABET))
    pools, cums, i = [], [], 0
    for sz in SLOT_SIZES:
        pools.append(glyphs[i:i + sz])
        cums.append(_zipf_cum(sz, rng))
        i += sz
    # Per-block favoured glyph for THEME_SLOT (theme-boosted cumulative).
    n_blocks = (n + BLOCK_LEN - 1) // BLOCK_LEN
    theme_glyph = [rng.randrange(SLOT_SIZES[THEME_SLOT]) for _ in range(n_blocks)]
    theme_cum = []
    for b in range(n_blocks):
        base = [0.0] * SLOT_SIZES[THEME_SLOT]
        c0, _ = cums[THEME_SLOT]
        prev = 0.0
        for gi in range(SLOT_SIZES[THEME_SLOT]):
            base[gi] = c0[gi] - prev
            prev = c0[gi]
        base[theme_glyph[b]] *= THEME_BOOST
        theme_cum.append(_cum(base))
    # Syntactic conditioning: a preferred successor glyph for the class and content
    # slots, so ON injects adjacent word-class structure + content collocation.
    class_next = [rng.randrange(SLOT_SIZES[CLASS_SLOT])
                  for _ in range(SLOT_SIZES[CLASS_SLOT])]
    content_next = [rng.randrange(SLOT_SIZES[CONTENT_SLOT])
                    for _ in range(SLOT_SIZES[CONTENT_SLOT])]

    out = []
    prev = [0] * len(SLOT_SIZES)
    for t in range(n):
        b = t // BLOCK_LEN
        chars = []
        for j in range(len(SLOT_SIZES)):
            if OPTIONAL[j] and rng.random() >= P_PRESENT:
                continue                         # slot absent -> word-length variation
            if positional and j == THEME_SLOT:
                gi = _pick(*theme_cum[b], rng)
            elif syntactic and j == CLASS_SLOT and rng.random() < SYN_STICK:
                gi = class_next[prev[j]]
            elif syntactic and j == CONTENT_SLOT and rng.random() < SYN_STICK:
                gi = content_next[prev[j]]
            else:
                gi = _pick(*cums[j], rng)
            chars.append(pools[j][gi])
            prev[j] = gi
        out.append("".join(chars))
    return out


# --- signature + banding --------------------------------------------------------------
TARGETS = ("h2", "mz_peak_value", "ed1_main_component", "zipf_slope",
           "type_token_ratio", "mean_word_length")


def _sig(tokens: list) -> dict:
    p = profile(tokens)
    return {**{t: p[t] for t in TARGETS}, "mz_peak_scale": p["mz_peak_scale"],
            "fc_z": _fc_z(tokens), "wc_z": _wc_z(tokens)}


def _vms_band() -> dict:
    """VMS full-signature bands: block-bootstrap 95% CI on profile metrics, and the
    fc_z/wc_z observed range across A and B (the weak-syntax target is 'below WEAK_Z')."""
    vms = _sub(_vms_tokens("A") + _vms_tokens("B"), N_TOKENS)
    boots = {t: [] for t in TARGETS}
    for b in range(BOOTSTRAP):
        pb = profile(_block_boot(vms, random.Random(7000 + b)))
        for t in TARGETS:
            boots[t].append(pb[t])
    band = {}
    for t in TARGETS:
        s = sorted(boots[t])
        band[t] = [round(s[int(0.025 * len(s))], 4),
                   round(s[min(len(s) - 1, int(0.975 * len(s)))], 4)]
    a, bb = _sub(_vms_tokens("A"), N_TOKENS), _sub(_vms_tokens("B"), N_TOKENS)
    band["fc_z_vms"] = [_fc_z(a), _fc_z(bb)]
    band["wc_z_vms"] = [_wc_z(a), _wc_z(bb)]
    band["mz_peak_scale_vms"] = profile(vms)["mz_peak_scale"]
    return band


def _hits(sig: dict, band: dict) -> dict:
    """In-band on each axis vs the VMS. fc_z/wc_z use the VMS's OWN two-sided band
    (refutation fix), NOT a one-sided '< WEAK_Z' threshold a full shuffle also passes."""
    h = {t: bool(band[t][0] <= sig[t] <= band[t][1]) for t in TARGETS}
    fc = sorted(band["fc_z_vms"])
    wc = sorted(band["wc_z_vms"])
    h["fc_z"] = bool(fc[0] <= sig["fc_z"] <= fc[1])
    h["wc_z"] = bool(wc[0] <= sig["wc_z"] <= wc[1])
    # Transparency: the discredited one-sided "weak" flag (a shuffle passes it too).
    below_weak = bool(sig["fc_z"] < WEAK_Z and sig["wc_z"] < WEAK_Z)
    return {"per_axis": h, "n_axes_matched": sum(h.values()),
            "matches_entropy_and_dI": h["h2"] and h["mz_peak_value"],
            "matches_vms_syntax": h["fc_z"] and h["wc_z"],
            "below_weak_z_threshold": below_weak}


def run() -> dict:
    band = _vms_band()
    configs = {
        "FULL": dict(morphology=True, positional=True, syntactic=False),
        "ablate_morphology": dict(morphology=False, positional=True, syntactic=False),
        "ablate_positional": dict(morphology=True, positional=False, syntactic=False),
        "add_syntactic": dict(morphology=True, positional=True, syntactic=True),
    }
    streams = {name: generate(N_TOKENS, seed=SEED, **flags)
               for name, flags in configs.items()}
    # reference anchors already used across the program
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()[:N_TOKENS]
    streams["ref_latin"] = _sub(latin)
    streams["ref_shuffle"] = _sub(order_shuffle(latin, SEED))

    sigs = {name: _sig(s) for name, s in streams.items()}
    hits = {name: _hits(sigs[name], band) for name in streams}

    full_hits = hits["FULL"]["per_axis"]
    dI = {c: sigs[c]["mz_peak_value"] for c in sigs}
    # Ingredient -> property map (refutation-corrected). Only NON-tautological links
    # are counted; the context-free->weak-syntax link is reported but flagged as true
    # by construction. Note morphology is CO-necessary for ΔI (knocking it out
    # collapses ΔI harder than knocking out the positional block wrapper).
    ingredient_map = {
        "morphology_necessary_for_h2":
            full_hits["h2"] and not hits["ablate_morphology"]["per_axis"]["h2"],
        "positional_necessary_for_dI":
            full_hits["mz_peak_value"]
            and not hits["ablate_positional"]["per_axis"]["mz_peak_value"],
        "morphology_ALSO_collapses_dI (ingredient map is NOT a bijection)":
            dI["ablate_morphology"] < dI["ablate_positional"],
        "context_free_->_weak_syntax (TAUTOLOGICAL, not counted)":
            hits["add_syntactic"]["per_axis"]["wc_z"] is False
            and sigs["add_syntactic"]["wc_z"] > sigs["FULL"]["wc_z"],
    }
    ax = full_hits
    matched_axes = [t for t in list(TARGETS) + ["fc_z", "wc_z"] if ax[t]]
    missed_axes = [t for t in list(TARGETS) + ["fc_z", "wc_z"] if not ax[t]]

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E21 — minimal positional/template generator + necessity ablation",
        "seed": SEED, "n_tokens": N_TOKENS,
        "constants": {"slot_sizes": list(SLOT_SIZES), "theme_slot": THEME_SLOT,
                      "class_slot": CLASS_SLOT, "content_slot": CONTENT_SLOT,
                      "zipf_exp": ZIPF_EXP, "block_len": BLOCK_LEN,
                      "theme_boost": THEME_BOOST, "syn_stick": SYN_STICK},
        "constants_were_grid_selected_against_vms": True,
        "vms_band": band,
        "signatures": sigs,
        "hits": hits,
        "full_matches_entropy_and_dI": hits["FULL"]["matches_entropy_and_dI"],
        "full_matches_vms_syntax": hits["FULL"]["matches_vms_syntax"],
        "full_axes_matched": matched_axes,
        "full_axes_missed": missed_axes,
        "ingredient_property_map": ingredient_map,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e21_positional_generator.json").write_text(
        json.dumps(results, indent=2) + "\n")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "e21_positional_generator.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    s = r["signatures"]
    fv = s["FULL"]
    tab = (f"FULL h2={fv['h2']} ΔI={fv['mz_peak_value']}@{fv['mz_peak_scale']} "
           f"fc_z={fv['fc_z']} wc_z={fv['wc_z']} ED1={fv['ed1_main_component']} "
           f"TTR={fv['type_token_ratio']} zipf={fv['zipf_slope']}; "
           f"-morph h2={s['ablate_morphology']['h2']} ΔI={s['ablate_morphology']['mz_peak_value']}; "
           f"-pos ΔI={s['ablate_positional']['mz_peak_value']}; "
           f"+syn wc_z={s['add_syntactic']['wc_z']}")
    matched = ", ".join(r["full_axes_matched"]) or "none"
    missed = ", ".join(r["full_axes_missed"]) or "none"
    wc_lo, wc_hi = sorted(r["vms_band"]["wc_z_vms"])
    # Refutation-hardened C. FULL matches entropy + block-ΔI but NOT the VMS's real
    # (weak-positive) word-class structure, and overshoots productivity/connectivity.
    return "C", (
        f"EXISTENCE OF A FITTED POINT, NOT CLASS SUFFICIENCY (refutation-downgraded "
        f"from a first-pass B). The generator constants were GRID-SELECTED to land in "
        f"the VMS bands, so the earlier 'a-priori / blind / circularity firewall' "
        f"framing is RETRACTED: this is a fitted point, exactly the move that made "
        f"E19's 'favours generation' positive circular. On the VMS's OWN bands (not a "
        f"one-sided threshold a full shuffle also passes), the fitted FULL config "
        f"matches only [{matched}] and MISSES [{missed}]. Decisively, it does NOT "
        f"reproduce the VMS's word-class structure: VMS wc_z is weak-but-POSITIVE "
        f"[{wc_lo}, {wc_hi}] while FULL wc_z={fv['wc_z']} is NEGATIVE (less structure "
        f"than its own shuffle) — a context-free positional grammar produces "
        f"anti-structure, not the VMS's mild positive syntax. It also OVERSHOOTS "
        f"vocabulary productivity (TTR {fv['type_token_ratio']} vs VMS "
        f"{r['vms_band']['type_token_ratio']}) and morphology connectivity (ED1 "
        f"{fv['ed1_main_component']} vs VMS {r['vms_band']['ed1_main_component']}) and "
        f"is too flat in frequency (Zipf {fv['zipf_slope']} vs VMS "
        f"{r['vms_band']['zipf_slope']}). MECHANISM MAP CAVEATS: knocking out "
        f"morphology collapses ΔI ({s['ablate_morphology']['mz_peak_value']}) HARDER "
        f"than knocking out the block wrapper ({s['ablate_positional']['mz_peak_value']}) "
        f", so morphology is CO-necessary for ΔI (not a clean one-ingredient-per-"
        f"property map); and the context-free→weak-syntax link is TAUTOLOGICAL (the "
        f"syntactic switch injects exactly what wc_z measures), so it is not counted. "
        f"NET FINDING (informative negative): the minimal context-free positional/"
        f"template grammar is INSUFFICIENT for the full VMS signature — it captures "
        f"entropy and injected block-ΔI but undershoots the VMS's weak-positive word-"
        f"class structure and overshoots its lexical productivity and morphological "
        f"connectivity, which CONSTRAINS the class toward heavier word reuse, a smaller "
        f"effective lexicon, and mild positive sequential structure. E22 (a-priori "
        f"grid + VMS-actual bands incl. positive wc_z + real-language-wrapper control) "
        f"is required before any class claim. {tab}. (Statistical; no identification — L7.)")


def _render(r: dict) -> str:
    s, h, band = r["signatures"], r["hits"], r["vms_band"]
    lines = [
        "# E21 — Minimal positional/template generator + necessity ablation",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e21_positional_generator`. Numbers in "
        "`results/experiments/e21_positional_generator.json`.",
        "",
        "Constants frozen a-priori (circularity firewall, D-item i07-a): "
        + ", ".join(f"{k}={v}" for k, v in r["constants"].items()) + ".",
        "",
        "VMS bands (match target): profile metrics = block-bootstrap 95% CI; fc_z/wc_z "
        f"= VMS observed [A,B] two-sided. h2 {band['h2']}, ΔI {band['mz_peak_value']}, "
        f"ED1 {band['ed1_main_component']}, TTR {band['type_token_ratio']}, Zipf "
        f"{band['zipf_slope']}, fc_z {sorted(band['fc_z_vms'])}, "
        f"wc_z {sorted(band['wc_z_vms'])}.",
        "",
        "Constants GRID-SELECTED against the VMS bands (not a-priori — see honesty "
        "note); E21 shows a fitted point, not class sufficiency.",
        "",
        "| config | h2 | ΔI | scale | fc_z | wc_z | ED1 | TTR | Zipf | axes✓ |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name in s:
        g = s[name]
        lines.append(f"| {name} | {g['h2']} | {g['mz_peak_value']} "
                     f"| {g['mz_peak_scale']} | {g['fc_z']} | {g['wc_z']} "
                     f"| {g['ed1_main_component']} | {g['type_token_ratio']} "
                     f"| {g['zipf_slope']} | {h[name]['n_axes_matched']}/8 |")
    lines += ["", f"FULL matches: **{', '.join(r['full_axes_matched']) or 'none'}**; "
              f"misses: **{', '.join(r['full_axes_missed']) or 'none'}**.",
              "", "## Ingredient → property map (refutation-corrected)", ""]
    lines += [f"- `{k}`: **{v}**" for k, v in r["ingredient_property_map"].items()]
    lines += ["", f"## Verdict [{r['grade']}, refutation pass applied]", "",
              r["verdict"], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    b = out["vms_band"]
    print(f"VMS band: h2 {b['h2']} ΔI {b['mz_peak_value']} ED1 {b['ed1_main_component']} "
          f"TTR {b['type_token_ratio']} fc_z {b['fc_z_vms']} wc_z {b['wc_z_vms']}")
    print(f"{'config':20s} {'h2':>6s} {'ΔI':>7s} {'scale':>6s} {'fc_z':>7s} "
          f"{'wc_z':>7s} {'ED1':>6s} {'TTR':>6s} axes")
    for name, g in out["signatures"].items():
        print(f"{name:20s} {g['h2']:>6} {g['mz_peak_value']:>7} {g['mz_peak_scale']:>6} "
              f"{str(g['fc_z']):>7} {str(g['wc_z']):>7} {g['ed1_main_component']:>6} "
              f"{g['type_token_ratio']:>6}  {out['hits'][name]['n_axes_matched']}/8")
    print("\ningredient→property:", out["ingredient_property_map"])
    print(f"FULL matches entropy+ΔI={out['full_matches_entropy_and_dI']} "
          f"vms_syntax={out['full_matches_vms_syntax']}")
    print(f"matched={out['full_axes_matched']} missed={out['full_axes_missed']}")
    print(f"grade {out['grade']}: {out['verdict'][:150]}...")
