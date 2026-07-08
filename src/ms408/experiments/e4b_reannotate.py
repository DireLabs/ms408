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

    cross_sig = [k for k in ("sonnet_root x OPUS_leaf", "opus_root x SONNET_leaf")
                 if tests[k]["constrained"]]
    bundle_confirmed = len(cross_sig) >= 1

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E4b — cross-model root<->leaf (same-source confound test)",
        "pages": len(pages),
        "second_model": MODEL,
        "inter_model_agreement": {
            "root_coloring": agree(s_rootcol, o_rootcol),
            "leaf_arrangement": agree(s_leafarr, o_leafarr),
        },
        "associations": {k: {"cramers_v": v["cramers_v"], "p": v["p_associated"],
                             "significant": v["constrained"]}
                         for k, v in tests.items()},
        "cross_model_significant": cross_sig,
        "bundle_confirmed_across_models": bool(bundle_confirmed),
    }
    results["verdict"] = _verdict(results)
    (RESULTS_DIR / "e4b_crossmodel.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> str:
    a = r["associations"]
    if r["bundle_confirmed_across_models"]:
        return (
            f"CONFIRMED across models: root<->leaf association survives when the two "
            f"features come from DIFFERENT vision models ({', '.join(r['cross_model_significant'])}), "
            f"so it is NOT a single-model visual-gestalt artifact. The cross-organ "
            f"bundle is real (in the annotations, at least) — i01's 'within-organ "
            f"only' verdict is OVERTURNED. Inter-model agreement: root_coloring "
            f"{r['inter_model_agreement']['root_coloring']}, leaf_arrangement "
            f"{r['inter_model_agreement']['leaf_arrangement']}. (Still does not "
            f"decide real-vs-invented herbal.)")
    return (
        f"NOT confirmed across models: the cross-model associations are "
        f"non-significant (sonnet_root x OPUS_leaf p "
        f"{a['sonnet_root x OPUS_leaf']['p']}, opus_root x SONNET_leaf p "
        f"{a['opus_root x SONNET_leaf']['p']}), while within-model associations "
        f"may hold — consistent with the E4 signal being a SINGLE-MODEL annotation "
        f"artifact. The i01 'within-organ only' null STANDS. Inter-model agreement: "
        f"root_coloring {r['inter_model_agreement']['root_coloring']}, "
        f"leaf_arrangement {r['inter_model_agreement']['leaf_arrangement']}.")


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
