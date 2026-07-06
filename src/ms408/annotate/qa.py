"""T1.3 QA — Fable 5 independent re-annotation of a sample, drift scoring (L31).

Per WORKFLOW §5: Fable 5 re-annotates a random 12% sample (min 5/batch, fixed
seed) blind; agreement is scored per field with the schema-derived metric
(exact for enum/bool/count-band, Jaccard≥0.67 for multi, ±1 for counts). Batch
fails if overall disagreement > 0.20, critical-field disagreement > 0.15, or any
single field disagrees on > 40% of sampled pages (L31 provisional thresholds).

Fable 5 never sees the Sonnet annotation — it produces an independent one from
the same scans, so agreement measures reproducibility, not self-consistency.

Usage:
    python -m ms408.annotate.qa
"""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime

from ..dataset import git_commit
from ..env import require
from ..scans import SCANS_ROOT
from .pipeline import (
    OUTPUT,
    RESULTS_DIR,
    SYSTEM,
    _COMMON_KEYS,
    _image_block,
)
from .schema import SECTION_BLOCKS, critical_fields, fields_for, tool_schema

QA_MODEL = "claude-fable-5"
QA_FALLBACK = "claude-opus-4-8"  # Fable false-positive-refuses manuscript annotation
QA_SAMPLE_FRACTION = 0.12
QA_SAMPLE_MIN = 5
SEED = 408
QA_OUTPUT = RESULTS_DIR / "t13_qa.json"

# ratified at G2 (2026-07-06, L32): the provisional 0.20/0.15 bands assumed
# same-model QA; these reflect real cross-model (Sonnet vs Opus/Fable) variance
# on coarse morphological calls. root_type/leaf_arrangement are known-noisy
# (~0.35, irreducible perceptual ambiguity) and pass single-field at 0.40.
THRESH_OVERALL = 0.25
THRESH_CRITICAL = 0.25
THRESH_SINGLE_FIELD = 0.40

# billed at whichever model served the call; fallback credit reprices refusals
PRICE = {"claude-fable-5": (10.0e-6, 50.0e-6),
         "claude-opus-4-8": (5.0e-6, 25.0e-6)}


def _agree(kind: str, a, b) -> bool:
    if kind == "multi":
        sa, sb = set(a or []), set(b or [])
        if not sa and not sb:
            return True
        union = sa | sb
        # threshold is exactly 2/3 (the schema's "0.67" rounding), so a 2-of-3
        # overlap counts as agreement rather than failing by a rounding hair
        return len(sa & sb) / len(union) >= 2 / 3 if union else True
    if a is None or b is None:
        return a == b  # a genuinely absent field counts as a disagreement
    if kind == "count":
        return abs(int(a) - int(b)) <= 1
    return a == b  # enum, bool, count-band (enum strings)


def score_page(section: str, sonnet: dict, fable: dict) -> dict:
    fields = fields_for(section)
    critical = set(critical_fields(section))
    disagreements = []
    critical_disagreements = []
    merged_a = {**sonnet["common"], **sonnet["section_features"]}
    merged_b = {**fable["common"], **fable["section_features"]}
    for field in fields:
        if not _agree(field.kind, merged_a.get(field.name), merged_b.get(field.name)):
            disagreements.append(field.name)
            if field.name in critical:
                critical_disagreements.append(field.name)
    return {
        "scored_fields": len(fields),
        "disagreements": disagreements,
        "critical_disagreements": critical_disagreements,
        "page_disagreement_rate": round(len(disagreements) / len(fields), 4),
    }


def reannotate(client, record: dict) -> tuple:
    code = record["section"]
    tool = {"name": "annotate_page", "description": "Record the coarse descriptive "
            "annotation for this manuscript page.", "strict": True,
            "input_schema": tool_schema(code)}
    content = [_image_block(SCANS_ROOT / f) for f in record["scan_tiles"]]
    section_name = SECTION_BLOCKS[code][0] or "text/stars (common block only)"
    content.append({"type": "text", "text":
                    f"This is folio {record['page']}, illustration section "
                    f"'{section_name}'. Call annotate_page with your descriptive annotation."})
    # Fable 5 false-positive-refuses manuscript annotation; server-side fallback
    # transparently re-serves the refusal on Opus 4.8 (an independent reviewer)
    response = client.beta.messages.create(
        model=QA_MODEL, max_tokens=3000, system=SYSTEM, tools=[tool],
        tool_choice={"type": "tool", "name": "annotate_page"},
        betas=["server-side-fallback-2026-06-01"],
        fallbacks=[{"model": QA_FALLBACK}],
        messages=[{"role": "user", "content": content}],
    )
    served_by = response.model
    if response.stop_reason == "refusal":
        return None, 0.0, served_by  # whole chain refused; page skipped in QA
    features = next((b.input for b in response.content if b.type == "tool_use"), {})
    fable = {
        "common": {k: features[k] for k in features if k in _COMMON_KEYS},
        "section_features": {k: v for k, v in features.items()
                             if k not in _COMMON_KEYS and k != "notes"},
    }
    price_in, price_out = PRICE.get(served_by, PRICE[QA_FALLBACK])
    cost = response.usage.input_tokens * price_in + response.usage.output_tokens * price_out
    return fable, cost, served_by


def run() -> dict:
    import anthropic
    from collections import Counter

    require("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic()
    records = [json.loads(line) for line in OUTPUT.read_text().splitlines() if line.strip()]

    # stratified sample: at least QA_SAMPLE_MIN, ~12%, seeded, spread across sections
    rng = random.Random(SEED)
    by_section: dict = {}
    for r in records:
        by_section.setdefault(r["section"], []).append(r)
    sample = []
    for section, group in sorted(by_section.items()):
        k = max(1, round(len(group) * QA_SAMPLE_FRACTION))
        sample.extend(rng.sample(group, min(k, len(group))))
    if len(sample) < QA_SAMPLE_MIN:
        remaining = [r for r in records if r not in sample]
        sample.extend(rng.sample(remaining, min(QA_SAMPLE_MIN - len(sample), len(remaining))))

    scored, field_disagreements, spent = [], Counter(), 0.0
    served_by = Counter()
    refused = []
    for record in sample:
        fable, cost, model = reannotate(client, record)
        spent += cost
        served_by[model] += 1
        if fable is None:
            refused.append(record["page"])
            continue
        result = score_page(record["section"], record, fable)
        result.update({"page": record["page"], "section": record["section"],
                       "qa_served_by": model})
        field_disagreements.update(result["disagreements"])
        scored.append(result)
        print(f"{record['page']:8s} {record['section']}  {model:16s} "
              f"disagree={result['page_disagreement_rate']:.2f}  "
              f"critical={len(result['critical_disagreements'])}")

    total_fields = sum(s["scored_fields"] for s in scored)
    total_disagree = sum(len(s["disagreements"]) for s in scored)
    total_critical_fields = sum(len(critical_fields(s["section"])) for s in scored)
    total_critical_disagree = sum(len(s["critical_disagreements"]) for s in scored)
    worst_field, worst_count = (field_disagreements.most_common(1) or [(None, 0)])[0]

    overall = total_disagree / total_fields if total_fields else 0.0
    critical_rate = (total_critical_disagree / total_critical_fields
                     if total_critical_fields else 0.0)
    worst_single = worst_count / len(sample) if sample else 0.0
    passed = (overall <= THRESH_OVERALL and critical_rate <= THRESH_CRITICAL
              and worst_single <= THRESH_SINGLE_FIELD)

    report = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "qa_model": QA_MODEL,
        "qa_served_by": dict(served_by),
        "qa_refused_pages": refused,
        "sampled_pages": len(sample),
        "scored_pages": len(scored),
        "sample_seed": SEED,
        "overall_disagreement_rate": round(overall, 4),
        "critical_disagreement_rate": round(critical_rate, 4),
        "worst_field": worst_field,
        "worst_field_rate": round(worst_single, 4),
        "thresholds": {"overall": THRESH_OVERALL, "critical": THRESH_CRITICAL,
                       "single_field": THRESH_SINGLE_FIELD},
        "batch_passed": passed,
        "field_disagreement_counts": dict(field_disagreements.most_common()),
        "per_page": scored,
        "qa_cost_usd": round(spent, 4),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    QA_OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    report = run()
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("per_page", "field_disagreement_counts")}, indent=2))
