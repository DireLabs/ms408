"""T1.3 bulk annotation runner (schema v0.1-coarse; budget cap L28 = $100).

Sonnet 4.6 does vision annotation via strict tool use (guaranteed schema-valid
output — replaces the Haiku format-validation step, which strict mode makes
redundant). Fable 5 QA is a separate module (qa.py). Cost is tracked per call
and the run aborts before exceeding the cap.

Resumable: pages already in the output JSONL are skipped, so a re-run continues.

Usage:
    python -m ms408.annotate.pipeline --limit 5        # pilot
    python -m ms408.annotate.pipeline --section H      # one section
    python -m ms408.annotate.pipeline                  # all illustrated pages
"""

from __future__ import annotations

import argparse
import base64
import json
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..env import require
from ..ivtff import IVTFFDocument
from ..scans import SCANS_ROOT
from ..sources import path_for
from .schema import SCHEMA_VERSION, SECTION_BLOCKS, tool_schema

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "annotations"
OUTPUT = RESULTS_DIR / "t13_annotations.jsonl"
MANIFEST = RESULTS_DIR / "t13_manifest.json"

ANNOTATOR_MODEL = "claude-sonnet-4-6"
BUDGET_CAP_USD = 100.0
# Sonnet 4.6 pricing, $/token
PRICE_IN = 3.0 / 1_000_000
PRICE_OUT = 15.0 / 1_000_000

SYSTEM = (
    "You are a careful manuscript-illustration annotator for a scholarly project on "
    "Beinecke MS 408 (the Voynich Manuscript). You describe what is drawn using a fixed "
    "controlled vocabulary. Strict rules:\n"
    "- Describe MORPHOLOGY only. Never identify a plant species, a zodiac sign, or a "
    "real-world referent. 'A branched root', never 'a mandrake'. 'An animal', never 'a bull'.\n"
    "- Judge only from what is visibly drawn. When the scan does not support a confident "
    "call, choose 'unclear' rather than guessing.\n"
    "- The manuscript's pigments are faded; read colors conservatively.\n"
    "- Fill every field of the annotate_page tool. Put any ambiguity in 'notes' (brief, "
    "descriptive, never identificational)."
)


def illustrated_pages(section: str | None = None) -> list:
    zl = IVTFFDocument.load(path_for("zl"))
    pages = []
    for page in zl.pages:
        code = page.illustration_type
        if code is None or code not in SECTION_BLOCKS:
            continue
        if section and code != section:
            continue
        pages.append((page.name, code))
    return pages


MAX_EDGE_PX = 7000  # API rejects any image dimension > 8000px; downscale foldouts


def _image_block(path: Path) -> dict:
    raw = path.read_bytes()
    from PIL import Image  # local import: only annotation needs it

    with Image.open(path) as img:
        if max(img.size) > MAX_EDGE_PX:
            import io

            scale = MAX_EDGE_PX / max(img.size)
            resized = img.convert("RGB").resize(
                (round(img.width * scale), round(img.height * scale)),
                Image.LANCZOS,
            )
            buffer = io.BytesIO()
            resized.save(buffer, format="JPEG", quality=90)
            raw = buffer.getvalue()
    data = base64.standard_b64encode(raw).decode()
    return {"type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}


def _load_scan_map() -> dict:
    return json.loads((ROOT / "data" / "processed" / "scan_map.json").read_text())["pages"]


def _done_pages() -> set:
    if not OUTPUT.exists():
        return set()
    return {json.loads(line)["page"] for line in OUTPUT.read_text().splitlines() if line.strip()}


def annotate_page(client, page_name: str, code: str, scan_map: dict) -> dict:
    entry = scan_map.get(page_name, {})
    files = entry.get("files", [])
    tool = {
        "name": "annotate_page",
        "description": "Record the coarse descriptive annotation for this manuscript page.",
        "strict": True,
        "input_schema": tool_schema(code),
    }
    content = [_image_block(SCANS_ROOT / f) for f in files]
    section_name = SECTION_BLOCKS[code][0] or "text/stars (common block only)"
    foldout_note = (
        "Multiple scan tiles are provided for this foldout panel; annotate the panel "
        "as a whole. " if len(files) > 1 else ""
    )
    content.append({"type": "text", "text":
                    f"This is folio {page_name}, illustration section '{section_name}'. "
                    f"{foldout_note}Call annotate_page with your descriptive annotation."})
    response = client.messages.create(
        model=ANNOTATOR_MODEL,
        max_tokens=2000,
        system=SYSTEM,
        tools=[tool],
        tool_choice={"type": "tool", "name": "annotate_page"},
        messages=[{"role": "user", "content": content}],
    )
    features = next(b.input for b in response.content if b.type == "tool_use")
    cost = (response.usage.input_tokens * PRICE_IN
            + response.usage.output_tokens * PRICE_OUT)
    record = {
        "schema_version": SCHEMA_VERSION,
        "page": page_name,
        "section": code,
        "scan_tiles": files,
        "foldout_ambiguous": entry.get("ambiguous", False),
        "annotator_model": ANNOTATOR_MODEL,
        "common": {k: features[k] for k in features if k in _COMMON_KEYS},
        "section_features": {k: v for k, v in features.items()
                             if k not in _COMMON_KEYS and k != "notes"},
        "notes": features.get("notes", ""),
        "qa": {"reviewed": False, "reviewer_model": None, "disagreements": []},
        "_cost_usd": round(cost, 5),
        "_input_tokens": response.usage.input_tokens,
        "_output_tokens": response.usage.output_tokens,
    }
    return record


_COMMON_KEYS = {"illustration_coverage_pct", "text_image_relationship", "color_palette",
                "marginalia_present", "damage_or_stain"}


def run(section: str | None = None, limit: int | None = None) -> dict:
    import anthropic

    require("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    scan_map = _load_scan_map()
    done = _done_pages()
    pages = [(n, c) for n, c in illustrated_pages(section) if n not in done]
    if limit:
        pages = pages[:limit]

    spent = sum(json.loads(line).get("_cost_usd", 0)
                for line in OUTPUT.read_text().splitlines()) if OUTPUT.exists() else 0.0
    annotated = 0
    with open(OUTPUT, "a") as out:
        for page_name, code in pages:
            if spent > BUDGET_CAP_USD:
                print(f"BUDGET CAP ${BUDGET_CAP_USD} reached (${spent:.2f}); stopping.")
                break
            record = annotate_page(client, page_name, code, scan_map)
            out.write(json.dumps(record) + "\n")
            out.flush()
            spent += record["_cost_usd"]
            annotated += 1
            print(f"{page_name:8s} {code}  ${record['_cost_usd']:.4f}  "
                  f"(total ${spent:.3f})")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "annotator_model": ANNOTATOR_MODEL,
        "budget_cap_usd": BUDGET_CAP_USD,
        "pages_annotated_total": len(_done_pages()),
        "spent_usd_total": round(spent, 4),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="T1.3 bulk annotation")
    parser.add_argument("--section", choices=sorted(SECTION_BLOCKS))
    parser.add_argument("--limit", type=int)
    args = parser.parse_args(argv)
    manifest = run(section=args.section, limit=args.limit)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
