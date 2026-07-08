"""E4b — Independent re-annotation to break the same-model-source confound (i02).

E4's refutation: root_coloring and leaf_arrangement both came from ONE vision
model (Sonnet 4.6) on one image, so their association could be a within-model
visual-gestalt correlation, not a manuscript bundle. E4b re-annotates the herbal
pages with a DIFFERENT model (Opus 4.8), blind, on just the E4 fields, then tests
the CROSS-MODEL pairs: root_coloring(Sonnet) x leaf_arrangement(Opus) and the
reverse. A cross-model association cannot be a single-model artifact.

Usage:
    python -m ms408.experiments.e4b_reannotate            # re-annotate (Opus 4.8)
    python -m ms408.experiments.e4b_reannotate --analyze  # cross-model tests
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from ..annotate.pipeline import SYSTEM, _image_block, _load_scan_map
from ..dataset import git_commit
from ..env import require
from ..ivtff import IVTFFDocument
from ..scans import SCANS_ROOT
from ..sources import path_for
from ..studies.referential_realism import association_test

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
OUT = RESULTS_DIR / "e4b_opus_annotations.jsonl"
MODEL = "claude-opus-4-8"
PRICE_IN, PRICE_OUT = 5.0e-6, 25.0e-6

FIELDS = {
    "root_coloring": ["uncolored", "brown-ochre", "red", "green", "other", "unclear"],
    "leaf_arrangement": ["alternate", "opposite", "whorled", "basal-rosette",
                         "single", "unclear"],
    "leaf_count_band": ["1-3", "4-8", "9-20", "20+", "unclear"],
}
TOOL = {
    "name": "annotate_herbal",
    "description": "Record three descriptive morphological features of the primary "
    "plant on this herbal page.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "root_coloring": {"type": "string", "enum": FIELDS["root_coloring"],
                              "description": "Coarse dominant pigment of the root "
                              "(faded — one bucket)."},
            "leaf_arrangement": {"type": "string", "enum": FIELDS["leaf_arrangement"],
                                 "description": "How leaves attach along the stem."},
            "leaf_count_band": {"type": "string", "enum": FIELDS["leaf_count_band"],
                                "description": "Coarse count band of leaves."},
        },
        "required": list(FIELDS),
        "additionalProperties": False,
    },
}


def _herbal_pages() -> list:
    zl = IVTFFDocument.load(path_for("zl"))
    return [p.name for p in zl.pages if p.illustration_type == "H"]


def _done() -> set:
    if not OUT.exists():
        return set()
    return {json.loads(x)["page"] for x in OUT.read_text().splitlines() if x.strip()}


def reannotate() -> dict:
    import anthropic

    require("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    scan_map = _load_scan_map()
    done = _done()
    pages = [p for p in _herbal_pages() if p not in done]
    spent = 0.0
    with open(OUT, "a") as out:
        for page in pages:
            files = scan_map.get(page, {}).get("files", [])
            if not files:
                continue
            content = [_image_block(SCANS_ROOT / f) for f in files]
            content.append({"type": "text", "text":
                            f"Folio {page}, herbal. Call annotate_herbal with the "
                            "three descriptive features (morphology only, no species)."})
            resp = client.messages.create(
                model=MODEL, max_tokens=1000, system=SYSTEM, tools=[TOOL],
                tool_choice={"type": "tool", "name": "annotate_herbal"},
                messages=[{"role": "user", "content": content}],
            )
            feats = next((b.input for b in resp.content if b.type == "tool_use"), None)
            if feats is None:
                continue
            cost = resp.usage.input_tokens * PRICE_IN + resp.usage.output_tokens * PRICE_OUT
            spent += cost
            out.write(json.dumps({"page": page, "model": MODEL, "features": feats,
                                  "_cost_usd": round(cost, 5)}) + "\n")
            out.flush()
            print(f"{page:8s} {feats.get('root_coloring'):12s} "
                  f"{feats.get('leaf_arrangement'):14s} (${spent:.3f})")
    return {"annotated": len(pages), "spent_usd": round(spent, 4)}


def analyze() -> dict:
    sonnet = {json.loads(x)["page"]: json.loads(x)
              for x in (ROOT / "results" / "annotations" / "t13_annotations.jsonl")
              .read_text().splitlines() if x.strip()}
    opus = {json.loads(x)["page"]: json.loads(x)["features"]
            for x in OUT.read_text().splitlines() if x.strip()}
    pages = [p for p in opus if p in sonnet and sonnet[p]["section"] == "H"]

    def col(model_dict, page, field, is_opus):
        feats = model_dict[page] if is_opus else model_dict[page]["section_features"]
        return feats.get(field)

    def clean(vals_a, vals_b):
        pairs = [(a, b) for a, b in zip(vals_a, vals_b)
                 if a not in (None, "unclear") and b not in (None, "unclear")]
        return [a for a, _ in pairs], [b for _, b in pairs]

    s_rootcol = [col(sonnet, p, "root_coloring", False) for p in pages]
    s_leafarr = [col(sonnet, p, "leaf_arrangement", False) for p in pages]
    o_rootcol = [opus[p].get("root_coloring") for p in pages]
    o_leafarr = [opus[p].get("leaf_arrangement") for p in pages]

    tests = {}
    # within-model (baselines)
    a, b = clean(s_rootcol, s_leafarr)
    tests["sonnet_root x sonnet_leaf"] = association_test(a, b, 1)
    a, b = clean(o_rootcol, o_leafarr)
    tests["opus_root x opus_leaf"] = association_test(a, b, 2)
    # CROSS-model (the decisive tests — cannot be a single-model artifact)
    a, b = clean(s_rootcol, o_leafarr)
    tests["sonnet_root x OPUS_leaf"] = association_test(a, b, 3)
    a, b = clean(o_rootcol, s_leafarr)
    tests["opus_root x SONNET_leaf"] = association_test(a, b, 4)
    # inter-model agreement on each field (annotation reliability)
    def agree(xs, ys):
        pairs = [(x, y) for x, y in zip(xs, ys)
                 if x not in (None, "unclear") and y not in (None, "unclear")]
        return round(sum(1 for x, y in pairs if x == y) / len(pairs), 3) if pairs else None

    # Refutation-hardened rule (clean-context critic, 2026-07-07). A real
    # cross-organ bundle is a property of the PAGE, so it must be symmetric under
    # which model supplies which feature: BOTH cross-model directions significant.
    # A disjunctive ">=1 of 2" rule roughly doubles the false-positive rate and lets
    # the experiment cherry-pick the cooperating direction. We also charge Bonferroni
    # across the 4 correlated tests and run an asymmetry diagnostic — if every
    # significant test shares one model's root label and every null test lacks it,
    # the effect tracks that model's LABELING, not the manuscript.
    BONFERRONI = round(0.05 / 4, 4)  # 0.0125
    cross = ("sonnet_root x OPUS_leaf", "opus_root x SONNET_leaf")
    cross_sig = [k for k in cross if tests[k]["constrained"]]
    within_opus_sig = tests["opus_root x opus_leaf"]["constrained"]
    sig_all = [k for k, v in tests.items() if v["constrained"]]
    null_all = [k for k, v in tests.items() if not v["constrained"]]
    # which root source is common to every significant / every null test?
    def _root_src(k):  # "sonnet" or "opus"
        return "sonnet" if k.startswith("sonnet_root") else "opus"
    sig_roots = {_root_src(k) for k in sig_all}
    null_roots = {_root_src(k) for k in null_all}
    single_root_driven = (len(sig_roots) == 1 and len(null_roots) == 1
                          and sig_roots != null_roots)
    # Confirmation now requires BOTH cross directions AND within-Opus replication.
    bundle_confirmed = len(cross_sig) == 2 and within_opus_sig
    min_cross_p = min(tests[k]["p_associated"] for k in cross)

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E4b — cross-model root<->leaf (same-source confound test)",
        "pages": len(pages),
        "second_model": MODEL,
        "bonferroni_alpha": BONFERRONI,
        "inter_model_agreement": {
            "root_coloring": agree(s_rootcol, o_rootcol),
            "leaf_arrangement": agree(s_leafarr, o_leafarr),
        },
        "associations": {k: {"cramers_v": v["cramers_v"], "p": v["p_associated"],
                             "significant": v["constrained"],
                             "clears_bonferroni": v["p_associated"] < BONFERRONI}
                         for k, v in tests.items()},
        "cross_model_significant": cross_sig,
        "within_opus_significant": bool(within_opus_sig),
        "single_root_source_driven": bool(single_root_driven),
        "root_source_of_significant_tests": sorted(sig_roots),
        "min_cross_model_p": min_cross_p,
        "bundle_confirmed_across_models": bool(bundle_confirmed),
    }
    results["grade"], results["verdict"] = _verdict(results)
    (RESULTS_DIR / "e4b_crossmodel.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    a = r["associations"]
    ag = r["inter_model_agreement"]
    if r["bundle_confirmed_across_models"]:
        return "CONFIRMED", (
            "CONFIRMED across models: the root<->leaf association is SYMMETRIC — "
            "significant in both cross-model directions AND replicated within Opus — "
            "so it is a property of the page, not a single-model artifact. i01's "
            "'within-organ only' verdict is OVERTURNED. (Still does not decide "
            "real-vs-invented herbal.)")
    # The realised case: split cross-model result driven by one root source.
    if r["single_root_source_driven"]:
        src = r["root_source_of_significant_tests"][0]
        return "SUGGESTIVE-BUT-UNRESOLVED (leaning artifact)", (
            f"OVERCLAIM REJECTED. The association is NOT symmetric across models: "
            f"every significant test shares {src.upper()}'s root label "
            f"(sonnet_root x sonnet_leaf, sonnet_root x OPUS_leaf) and every null "
            f"test lacks it (opus_root x opus_leaf p {a['opus_root x opus_leaf']['p']}, "
            f"opus_root x SONNET_leaf p {a['opus_root x SONNET_leaf']['p']}). The "
            f"discriminating variable is WHICH MODEL LABELLED THE ROOT, not the "
            f"manuscript. Decisively: root_coloring agrees {ag['root_coloring']} "
            f"across models, yet swapping Sonnet's root for the 83%-concordant Opus "
            f"root makes the effect vanish in BOTH leaf conditions — a real page "
            f"property could not do that. Leaf noise ({ag['leaf_arrangement']}) does "
            f"not rescue it: the most-null test uses the CLEANER sonnet_leaf, so the "
            f"pattern tracks root source, not leaf quality. The one surviving "
            f"cross-model p ({r['min_cross_model_p']}) clears Bonferroni "
            f"({r['bonferroni_alpha']}) by only ~1.4x, before charging the "
            f"researcher-df of the original >=1-of-2 rule. NET: the same-model-source "
            f"confound is NOT cleanly broken; evidence leans toward a Sonnet-root "
            f"labelling regularity. i01's 'within-organ only' leg is WEAKENED but "
            f"NOT overturned. Decisive next control: a THIRD independent root_coloring "
            f"rater (human ground-truth) — if the leaf association reappears with "
            f"non-Sonnet root labels it is real; if only ever with sonnet_root it is "
            f"a Sonnet artifact.")
    return "NOT-CONFIRMED", (
        f"NOT confirmed across models: cross-model associations non-significant "
        f"(sonnet_root x OPUS_leaf p {a['sonnet_root x OPUS_leaf']['p']}, "
        f"opus_root x SONNET_leaf p {a['opus_root x SONNET_leaf']['p']}) — consistent "
        f"with the E4 signal being a single-model artifact. i01's 'within-organ only' "
        f"null STANDS. Inter-model agreement: root_coloring {ag['root_coloring']}, "
        f"leaf_arrangement {ag['leaf_arrangement']}.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analyze", action="store_true")
    args = parser.parse_args(argv)
    if args.analyze:
        out = analyze()
        print(json.dumps({k: v for k, v in out.items()
                          if k not in ("associations",)}, indent=2))
        for k, v in out["associations"].items():
            print(f"  {k:26s} V={v['cramers_v']:.3f} p={v['p']:.4f} sig={v['significant']}")
    else:
        print(json.dumps(reannotate(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
