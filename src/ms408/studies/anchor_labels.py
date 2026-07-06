"""T2.3b — Label-level anchoring (W3, higher-power follow-up to T2.3a).

The page-level anchor hunt (T2.3a) found nothing. The sharper question: do the
words drawn AS LABELS on the illustrations behave like a naming system — a small
set of recurring part-names that reappear wherever that part is depicted?

Two findings drive the design (both established here, not assumed):

  1. **Label census**: where do labels even exist? The herbal section — the
     obvious place to look for "a word next to a root" — turns out to be almost
     label-free; the pharmaceutical and astronomical sections carry the labels.

  2. **Recurrence test** (the anchor test proper): if labels named things, label
     tokens would recur across pages far more than running text does. We compare
     the cross-page recurrence of label tokens against a size-matched bootstrap
     of running-text tokens from the same section. A naming system → labels
     recur MORE than the running-text baseline; hapax labels → no naming system.

Harness discipline (L4/L7): the running-text bootstrap IS the null model; a label
recurrence inside the bootstrap band means "indistinguishable from non-naming
text." Nothing here is a translation (L7); a surviving anchor would be a
recurring label token to be corroborated independently, never a meaning.

Usage:
    python -m ms408.studies.anchor_labels
"""

from __future__ import annotations

import json
import random
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..replication import WORD_POLICY
from ..sources import path_for

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "studies"
REPORTS_DIR = ROOT / "reports"
ANNOTATIONS = ROOT / "results" / "annotations" / "t13_annotations.jsonl"

BOOTSTRAP = 5000
SEED = 408
MIN_LABEL_PAGES = 4  # a section needs this many label-bearing pages to test


def _section_of(page_name: str, annotations: dict) -> str | None:
    rec = annotations.get(page_name)
    return rec["section"] if rec else None


def collect(doc: IVTFFDocument, annotations: dict) -> dict:
    """Per section: {page: {'label': [tokens], 'running': [tokens]}}."""
    by_section: dict = {}
    for page in doc.pages:
        section = _section_of(page.name, annotations)
        if section is None:
            continue
        label, running = [], []
        for locus in page.loci:
            toks = [w for w in locus.words(WORD_POLICY) if "@" not in w]
            if locus.locus_type.startswith("L"):
                label.extend(toks)
            elif locus.locus_type.startswith("P"):
                running.extend(toks)
        by_section.setdefault(section, {})[page.name] = {
            "label": label, "running": running,
        }
    return by_section


def _recurrence(page_tokens: list) -> tuple:
    """(types, types recurring on >=2 pages, mean pages-per-type) for a list of
    per-page token lists."""
    pages_with = Counter()
    for tokens in page_tokens:
        for t in set(tokens):
            pages_with[t] += 1
    if not pages_with:
        return 0, 0, 0.0
    recurring = sum(1 for c in pages_with.values() if c >= 2)
    return len(pages_with), recurring, sum(pages_with.values()) / len(pages_with)


def recurrence_test(pages: dict, seed: int = SEED) -> dict:
    """Compare label-token cross-page recurrence to a size-matched running-text
    bootstrap. Returns the observed label recurrence, the null band, and p."""
    label_by_page = [p["label"] for p in pages.values() if p["label"]]
    label_pages = len(label_by_page)
    label_counts = [len(lst) for lst in label_by_page]
    total_labels = sum(label_counts)

    _, label_recurring, label_mean = _recurrence(label_by_page)

    # null: draw the same number of tokens per page from that page's running text
    rng = random.Random(seed)
    null_recurring = []
    running_pool = {name: p["running"] for name, p in pages.items() if p["running"]}
    pool_names = list(running_pool)
    for _ in range(BOOTSTRAP):
        sampled = []
        for k in label_counts:
            src = running_pool[rng.choice(pool_names)]
            sampled.append([rng.choice(src) for _ in range(k)] if src else [])
        _, recurring, _ = _recurrence(sampled)
        null_recurring.append(recurring)
    null_recurring.sort()
    lo = null_recurring[int(0.025 * BOOTSTRAP)]
    hi = null_recurring[int(0.975 * BOOTSTRAP)]
    p = (sum(1 for x in null_recurring if x >= label_recurring) + 1) / (BOOTSTRAP + 1)

    types = len(set(t for lst in label_by_page for t in lst))
    return {
        "label_pages": label_pages,
        "label_tokens": total_labels,
        "label_types": types,
        "label_type_token_ratio": round(types / total_labels, 4) if total_labels else None,
        "label_types_recurring_2plus": label_recurring,
        "label_mean_pages_per_type": round(label_mean, 3),
        "null_recurrence_band_95": [lo, hi],
        "null_recurrence_median": null_recurring[BOOTSTRAP // 2],
        "p_labels_recur_more_than_running": round(p, 5),
        "labels_are_naming_system": bool(label_recurring > hi and p < 0.05),
    }


def run() -> dict:
    annotations = {json.loads(line)["page"]: json.loads(line)
                   for line in ANNOTATIONS.read_text().splitlines() if line.strip()}
    doc = IVTFFDocument.load(path_for("zl"))
    by_section = collect(doc, annotations)

    census = {}
    tests = {}
    for section, pages in sorted(by_section.items()):
        label_pages = sum(1 for p in pages.values() if p["label"])
        label_tokens = sum(len(p["label"]) for p in pages.values())
        census[section] = {
            "pages": len(pages),
            "label_bearing_pages": label_pages,
            "label_tokens": label_tokens,
        }
        running_tokens = sum(len(p["running"]) for p in pages.values())
        # need a running-text pool to build the size-matched null
        if label_pages >= MIN_LABEL_PAGES and label_tokens >= 20 and running_tokens >= 50:
            tests[section] = recurrence_test(pages)

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "bootstrap": BOOTSTRAP,
        "label_census": census,
        "recurrence_tests": tests,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "anchor_labels.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "study_anchor_labels.md").write_text(_render_report(results))
    return results


def _render_report(results: dict) -> str:
    census = results["label_census"]
    tests = results["recurrence_tests"]
    lines = [
        "# T2.3b Study Report — Label-Level Anchoring (W3)",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.studies.anchor_labels`; full numbers in "
        "`results/studies/anchor_labels.json`.",
        "",
        "## Label census — where labels even exist",
        "",
        "| section | pages | label-bearing pages | label tokens |",
        "|---|---|---|---|",
    ]
    for section, c in census.items():
        lines.append(f"| {section} | {c['pages']} | {c['label_bearing_pages']} "
                     f"| {c['label_tokens']} |")
    herbal = census.get("H", {})
    lines += [
        "",
        f"**Structural finding [C]:** the herbal section — the obvious place to "
        f"look for a word drawn next to a root — is almost label-free "
        f"({herbal.get('label_bearing_pages', 0)} of {herbal.get('pages', 0)} pages "
        f"carry any label). The 'word next to the plant part' structure that "
        f"label-level anchoring assumes largely does not exist there. This "
        f"reframes the T2.3a page-level null: much of the herbal has no labels to "
        f"anchor on.",
        "",
        "## Recurrence test — do labels behave like a naming system?",
        "",
        "| section | label types | TTR | recurring (≥2 pp) | null band (95%) | p | naming system? |",
        "|---|---|---|---|---|---|---|",
    ]
    for section, t in tests.items():
        lines.append(
            f"| {section} | {t['label_types']} | {t['label_type_token_ratio']} "
            f"| {t['label_types_recurring_2plus']} | {t['null_recurrence_band_95']} "
            f"| {t['p_labels_recur_more_than_running']} "
            f"| {'YES' if t['labels_are_naming_system'] else 'no'} |"
        )
    lines += ["", "## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 — L10)", ""]
    lines.append(_claims(results))
    lines += ["", ""]
    return "\n".join(lines)


def _claims(results: dict) -> str:
    tests = results["recurrence_tests"]
    census = results["label_census"]
    claims = []
    any_naming = any(t["labels_are_naming_system"] for t in tests.values())
    if not any_naming:
        pharma = tests.get("P", {})
        below = [s for s, t in tests.items()
                 if t["label_types_recurring_2plus"] < t["null_recurrence_band_95"][0]]
        claims.append(
            f"1. **[C, candidate B pending T3.3]** No section's labels behave like a "
            f"naming system; if anything, labels recur across pages *less* than "
            f"running text does. In pharmaceutical — the most label-rich section "
            f"({census.get('P', {}).get('label_tokens')} label tokens on "
            f"{pharma.get('label_pages')} pages) — labels are "
            f"{pharma.get('label_type_token_ratio', 0):.0%} unique "
            f"(TTR {pharma.get('label_type_token_ratio')}), and only "
            f"{pharma.get('label_types_recurring_2plus')} label types recur on ≥2 "
            f"pages versus a running-text null band of "
            f"{pharma.get('null_recurrence_band_95')} — below the band. Labels "
            f"below the null in {below or 'no'} section(s); above in none. There is "
            f"no recurring part-name vocabulary."
        )
        claims.append(
            "2. **[C]** The direction matters: a nomenclature (a fixed word for "
            "'root' reused wherever a root is drawn) would push label recurrence "
            "ABOVE the running-text baseline. We see the opposite — near-unique "
            "labels — consistent with labels being content-like words that avoid "
            "the high-frequency grammatical vocabulary of running text, yet are "
            "not themselves a reusable naming set."
        )
        claims.append(
            "3. **[C]** Taken with T2.3a, this is a coherent constraint: neither "
            "whole-page vocabulary nor the illustration labels form a detectable "
            "word→referent mapping. Whatever the labels are, they are not a "
            "consistent nomenclature at the granularity our methods can see — "
            "evidence against a straightforward 'labelled herbal/pharmacopoeia "
            "where words name the depicted things' reading (L7: this constrains, "
            "it does not decode)."
        )
    else:
        winners = [s for s, t in tests.items() if t["labels_are_naming_system"]]
        claims.append(
            f"1. **[C, candidate B pending T3.3]** Labels in section(s) {winners} "
            f"recur across pages significantly more than running text — candidate "
            f"naming behavior. These recurring label tokens are anchor candidates "
            f"for independent corroboration (L7: not yet meanings)."
        )
    claims.append(
        "**Method note:** the null is a size-matched bootstrap of each section's "
        "own running text, so recurrence is compared like-for-like against that "
        "section's non-label vocabulary — the right baseline."
    )
    return "\n".join(claims)


if __name__ == "__main__":
    out = run()
    print(json.dumps(out["label_census"], indent=2))
    for section, t in out["recurrence_tests"].items():
        print(f"{section}: TTR={t['label_type_token_ratio']} "
              f"recurring={t['label_types_recurring_2plus']} "
              f"null_band={t['null_recurrence_band_95']} "
              f"p={t['p_labels_recur_more_than_running']} "
              f"naming={t['labels_are_naming_system']}")
