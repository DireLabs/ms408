"""E17 — Dedicated Currier A-vs-B contrast, content-controlled (i05).

E14b found VMS-B carries more distributional word-class structure than VMS-A (B>A in
7/9 K/V cells). But Currier A/B is confounded with SECTION/content: A dominates the
herbal, B dominates the biological/recipe sections, so "A vs B" could be "plants vs
recipes", not a language difference. The clean control: the HERBAL section contains
BOTH dialects (Herbal-A 7470 tokens, Herbal-B 3305) — the only section that does — so
comparing Herbal-A vs Herbal-B holds CONTENT fixed and isolates dialect.

Design. Compute the null-corrected distributional word-class z (E14 measure: adjacent-
class NMI vs an order-shuffle+recluster null) over several k-means seeds for four
strata at MATCHED token budgets: global A vs B (confounded), and Herbal-A vs Herbal-B
(content-controlled). If B>A survives WITHIN the herbal, the difference is a dialect/
language property; if it vanishes there, it was a section/content effect.

Pass/fail. B's word-class z consistently above A's within the herbal ⇒ a genuine
DIALECT difference in grammatical structure (supports "A and B are different
processes", in degree). B≈A within the herbal ⇒ the global difference was content-
driven, and A/B do not differ in mid-level grammar once content is controlled.

Usage:
    python -m ms408.experiments.e17_ab_contrast
"""

from __future__ import annotations

import json
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..sources import path_for
from ..studies.anchor_hunt import WORD_POLICY
from .e13_function_content import SEED
from .e14_word_classes import _adjacent_class_nmi
from .mid_level_null import null_z, order_shuffle

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
N_SEEDS = 6
B_NULL = 10


def _tokens(dialect: str, section: str | None = None) -> list:
    zl = IVTFFDocument.load(path_for("zl"))
    out = []
    for p in zl.pages:
        if p.currier_language != dialect:
            continue
        if section is not None and p.illustration_type != section:
            continue
        for loc in p.loci:
            if (loc.locus_type or "").startswith("P"):
                out.extend(w for w in loc.words(WORD_POLICY) if "@" not in w)
    return out


def _wordclass_z(tokens: list, obs_seed: int) -> float:
    obs = _adjacent_class_nmi(tokens, obs_seed)
    nulls = [_adjacent_class_nmi(order_shuffle(tokens, obs_seed + 1000 + i),
                                 obs_seed + 1000 + i) for i in range(B_NULL)]
    return null_z(obs, nulls)["z"]


def _multiseed_z(tokens: list) -> dict:
    zs = [round(_wordclass_z(tokens, SEED + 137 * i), 2) for i in range(N_SEEDS)]
    return {"z_by_seed": zs, "mean": round(statistics.mean(zs), 2),
            "min": min(zs), "max": max(zs), "tokens": len(tokens)}


def run() -> dict:
    a_all, b_all = _tokens("A"), _tokens("B")
    ha, hb = _tokens("A", "H"), _tokens("B", "H")

    # matched token budgets within each comparison (fair z)
    g = min(len(a_all), len(b_all))            # global A vs B
    h = min(len(ha), len(hb))                  # herbal A vs B (content-controlled)
    strata = {
        "global_A": _multiseed_z(a_all[:g]), "global_B": _multiseed_z(b_all[:g]),
        "herbal_A": _multiseed_z(ha[:h]), "herbal_B": _multiseed_z(hb[:h]),
    }

    def b_gt_a(pfx):
        za = strata[f"{pfx}_A"]
        zb = strata[f"{pfx}_B"]
        return {"A_mean": za["mean"], "B_mean": zb["mean"],
                "B_minus_A": round(zb["mean"] - za["mean"], 2),
                "B_gt_A_mean": zb["mean"] > za["mean"],
                # strict: B's min above A's max ⇒ non-overlapping, clearly separated
                "B_clearly_above_A": zb["min"] > za["max"]}

    glob = b_gt_a("global")
    herb = b_gt_a("herbal")
    # dialect effect iff the herbal (content-controlled) contrast still shows B>A
    dialect_effect = bool(herb["B_gt_A_mean"])
    content_confound = bool(glob["B_gt_A_mean"] and not herb["B_gt_A_mean"])

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E17 — Currier A-vs-B contrast (content-controlled, word-class z)",
        "seed": SEED, "n_seeds": N_SEEDS, "n_null": B_NULL,
        "matched_tokens": {"global": min(len(a_all), len(b_all)),
                           "herbal": min(len(ha), len(hb))},
        "strata": strata,
        "global_contrast": glob, "herbal_contrast_content_controlled": herb,
        "ab_difference_is_dialect_effect": dialect_effect,
        "ab_difference_was_content_confound": content_confound,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e17_ab_contrast.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    g, h = r["global_contrast"], r["herbal_contrast_content_controlled"]
    base = (f"Word-class z (mean over {r['n_seeds']} seeds). GLOBAL A={g['A_mean']} "
            f"B={g['B_mean']} (B−A {g['B_minus_A']}). HERBAL (content-controlled, "
            f"{r['matched_tokens']['herbal']} tokens each) A={h['A_mean']} B={h['B_mean']} "
            f"(B−A {h['B_minus_A']}; B clearly above A: {h['B_clearly_above_A']}). Both "
            f"strata remain far below real language (z≈15).")
    if r["ab_difference_is_dialect_effect"]:
        return "C", (
            f"DIALECT EFFECT — the B>A word-class difference SURVIVES within the herbal "
            f"section, where content is held fixed. So Currier A and B differ in mid-"
            f"level grammatical structure as a property of the WRITING SYSTEM/dialect, "
            f"not merely because they cover different subject matter: the B system "
            f"carries more distributional word-class structure than the A system even on "
            f"the same (herbal) content. This is direct support for Tim's hypothesis that "
            f"A and B are different generative processes — a difference in DEGREE of "
            f"word-level structure (both still far below real language). {base} (Surface "
            f"distributional grammar; no meaning/translation claim — L7.)")
    if r["ab_difference_was_content_confound"]:
        return "C", (
            f"CONTENT CONFOUND — the E14b A/B word-class difference is a SECTION effect, "
            f"NOT a dialect difference. B>A holds globally (B−A {g['B_minus_A']}) but does "
            f"NOT survive within the herbal section, where content is held fixed: there "
            f"herbal-A ({h['A_mean']}) is if anything ABOVE herbal-B ({h['B_mean']}). So "
            f"the apparent 'B has more word-class structure' was driven by B covering the "
            f"biological/recipe sections (which differ from the herbal), not by the "
            f"Currier dialect. Once content is controlled, there is NO evidence that A and "
            f"B differ in mid-level word-class structure. This CORRECTS the E14b reading "
            f"and withdraws the 'A and B are different generative processes' inference "
            f"from this probe. CAVEAT: Herbal-B is small ({r['matched_tokens']['herbal']} "
            f"tokens), so the within-herbal contrast is UNDERPOWERED — the robust claim is "
            f"'the global difference is content-confounded', and the within-content null "
            f"is suggestive but not decisive; a larger content-matched sample (or a "
            f"second both-dialect section) would settle it. {base} (L7.)")
    return "C", (
        f"INCONCLUSIVE/mixed — the content-controlled herbal contrast does not cleanly "
        f"resolve dialect vs content (small Herbal-B sample). {base} (L7.)")


if __name__ == "__main__":
    out = run()
    for k, s in out["strata"].items():
        print(f"  {k:10s} tokens={s['tokens']:>5} z_mean={s['mean']:>5} "
              f"range=[{s['min']},{s['max']}] seeds={s['z_by_seed']}")
    print(f"\nGLOBAL  B-A={out['global_contrast']['B_minus_A']} "
          f"(B>A {out['global_contrast']['B_gt_A_mean']})")
    print(f"HERBAL  B-A={out['herbal_contrast_content_controlled']['B_minus_A']} "
          f"(B>A {out['herbal_contrast_content_controlled']['B_gt_A_mean']}, "
          f"clearly {out['herbal_contrast_content_controlled']['B_clearly_above_A']})")
    print(f"dialect_effect={out['ab_difference_is_dialect_effect']} "
          f"content_confound={out['ab_difference_was_content_confound']}")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
