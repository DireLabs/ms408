"""T2.3 — Anchor hunt (W3, highest-ceiling study).

Question: does any Voynichese token statistically co-occur with a specific
visual feature across pages — does anything behave like "root"?

Method: per illustrated page we have a word set (ZL) and a set of binary visual
features (T13 annotations, one indicator per feature=value). For each frequent
token × each feature indicator, test association across pages with the phi
coefficient and a Fisher exact p-value, then control the false-discovery rate
with Benjamini-Hochberg.

Harness-first (L4, the meaning-detection gate — RESEARCH-PLAN §3): before any
real anchor is admissible, the method must (a) on a NULL control — the same
features paired with page-shuffled text — return false anchors at no more than
the FDR level, and (b) on a PLANTED control — a synthetic token injected onto
pages carrying a chosen feature — recover that anchor. Both run here and gate
the H1 report.

Usage:
    python -m ms408.studies.anchor_hunt
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
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

MIN_TOKEN_PAGES = 5  # token must appear on >= this many pages to be testable
MIN_FEATURE_PAGES = 5  # feature indicator must be present on >= this many pages
FDR_Q = 0.05
SEED = 408


# ---------------------------------------------------------------------------
# Association statistics
# ---------------------------------------------------------------------------


def phi(a: int, b: int, c: int, d: int) -> float:
    """Phi coefficient of a 2x2 table [[a,b],[c,d]] (token× feature presence)."""
    denom = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return (a * d - b * c) / denom if denom else 0.0


def _log_factorial(n: int, _cache={0: 0.0}) -> float:
    if n not in _cache:
        _cache[n] = _log_factorial(n - 1) + math.log(n)
    return _cache[n]


def _hypergeom_logp(a: int, b: int, c: int, d: int) -> float:
    n = a + b + c + d
    return (_log_factorial(a + b) + _log_factorial(c + d)
            + _log_factorial(a + c) + _log_factorial(b + d)
            - _log_factorial(a) - _log_factorial(b) - _log_factorial(c)
            - _log_factorial(d) - _log_factorial(n))


def fisher_right_tail(a: int, b: int, c: int, d: int) -> float:
    """One-sided (enrichment) Fisher exact p-value for a 2x2 table."""
    row1, col1, n = a + b, a + c, a + b + c + d
    p = 0.0
    hi = min(row1, col1)
    for x in range(a, hi + 1):
        p += math.exp(_hypergeom_logp(x, row1 - x, col1 - x, n - row1 - col1 + x))
    return min(p, 1.0)


def benjamini_hochberg(pvalues: list, q: float = FDR_Q) -> list:
    """Return the boolean 'discovery' mask under BH-FDR at level q."""
    m = len(pvalues)
    order = sorted(range(m), key=pvalues.__getitem__)
    threshold_rank = -1
    for rank, idx in enumerate(order, start=1):
        if pvalues[idx] <= q * rank / m:
            threshold_rank = rank
    discovered = [False] * m
    for rank, idx in enumerate(order, start=1):
        if rank <= threshold_rank:
            discovered[idx] = True
    return discovered


# ---------------------------------------------------------------------------
# Page data assembly
# ---------------------------------------------------------------------------


@dataclass
class PageData:
    page: str
    section: str
    tokens: frozenset
    features: frozenset  # "field=value" indicator strings


def _feature_indicators(record: dict) -> set:
    indicators = set()
    for block in ("common", "section_features"):
        for field, value in record.get(block, {}).items():
            if isinstance(value, list):
                for v in value:
                    indicators.add(f"{field}={v}")
            elif isinstance(value, bool):
                if value:
                    indicators.add(f"{field}=true")
            else:
                indicators.add(f"{field}={value}")
    return indicators


def load_pages(section: str | None = "H") -> list:
    zl = IVTFFDocument.load(path_for("zl"))
    words_by_page = {}
    for page in zl.pages:
        words_by_page[page.name] = frozenset(
            w for locus in page.loci for w in locus.words(WORD_POLICY) if "@" not in w
        )
    pages = []
    for line in ANNOTATIONS.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if section and record["section"] != section:
            continue
        page = record["page"]
        if page not in words_by_page:
            continue
        pages.append(PageData(page, record["section"], words_by_page[page],
                              frozenset(_feature_indicators(record))))
    return pages


# ---------------------------------------------------------------------------
# Association scan
# ---------------------------------------------------------------------------


def scan(pages: list, token_page_sets: dict, feature_page_sets: dict) -> list:
    n = len(pages)
    all_page_names = [p.page for p in pages]
    tests = []
    for token, tpages in token_page_sets.items():
        for feature, fpages in feature_page_sets.items():
            a = len(tpages & fpages)
            b = len(tpages - fpages)
            c = len(fpages - tpages)
            d = n - a - b - c
            tests.append({
                "token": token, "feature": feature,
                "a": a, "b": b, "c": c, "d": d,
                "phi": round(phi(a, b, c, d), 4),
                "p": fisher_right_tail(a, b, c, d),
            })
    pvals = [t["p"] for t in tests]
    discovered = benjamini_hochberg(pvals, FDR_Q)
    for t, disc in zip(tests, discovered):
        t["discovery"] = disc
        t["p"] = round(t["p"], 6)
    _ = all_page_names
    return tests


def _page_sets(pages: list):
    token_pages: dict = {}
    feature_pages: dict = {}
    for p in pages:
        for token in p.tokens:
            token_pages.setdefault(token, set()).add(p.page)
        for feature in p.features:
            feature_pages.setdefault(feature, set()).add(p.page)
    tokens = {t: s for t, s in token_pages.items() if len(s) >= MIN_TOKEN_PAGES}
    features = {f: s for f, s in feature_pages.items()
                if MIN_FEATURE_PAGES <= len(s) <= len(pages) - MIN_FEATURE_PAGES}
    return tokens, features


# ---------------------------------------------------------------------------
# Harness controls (the meaning-detection gate)
# ---------------------------------------------------------------------------


def null_control(pages: list, seed: int = SEED) -> dict:
    """Pair features with page-shuffled text; expect discoveries ≈ 0."""
    rng = random.Random(seed)
    shuffled_tokens = [p.tokens for p in pages]
    rng.shuffle(shuffled_tokens)
    permuted = [PageData(p.page, p.section, tok, p.features)
                for p, tok in zip(pages, shuffled_tokens)]
    tokens, features = _page_sets(permuted)
    tests = scan(permuted, tokens, features)
    discoveries = sum(1 for t in tests if t["discovery"])
    return {"tests": len(tests), "false_discoveries": discoveries,
            "false_discovery_fraction": round(discoveries / max(len(tests), 1), 5)}


def planted_control(pages: list, seed: int = SEED) -> dict:
    """Inject a synthetic token on pages carrying a chosen feature; expect recovery."""
    tokens, features = _page_sets(pages)
    if not features:
        return {"recovered": None, "reason": "no testable features"}
    target = max(features, key=lambda f: len(features[f]))
    target_pages = features[target]
    planted = []
    for p in pages:
        toks = set(p.tokens)
        if p.page in target_pages:
            toks.add("PLANT")
        planted.append(PageData(p.page, p.section, frozenset(toks), p.features))
    ptokens, pfeatures = _page_sets(planted)
    tests = scan(planted, ptokens, pfeatures)
    hit = next((t for t in tests
                if t["token"] == "PLANT" and t["feature"] == target), None)
    return {
        "planted_on_feature": target,
        "planted_pages": len(target_pages),
        "recovered": bool(hit and hit["discovery"]),
        "phi": hit["phi"] if hit else None,
        "p": hit["p"] if hit else None,
    }


def run(section: str = "H") -> dict:
    pages = load_pages(section)
    tokens, features = _page_sets(pages)
    null = null_control(pages)
    planted = planted_control(pages)
    gate_passed = (null["false_discovery_fraction"] <= FDR_Q
                   and planted.get("recovered") is True)

    real_tests = scan(pages, tokens, features)
    anchors = sorted(
        (t for t in real_tests if t["discovery"] and t["phi"] > 0),
        key=lambda t: -t["phi"],
    )
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "section": section,
        "pages": len(pages),
        "testable_tokens": len(tokens),
        "testable_features": len(features),
        "tests": len(real_tests),
        "fdr_q": FDR_Q,
        "harness_gate": {
            "null_control": null,
            "planted_control": planted,
            "passed": gate_passed,
        },
        "anchors": anchors[:50] if gate_passed else [],
        "anchors_admissible": gate_passed,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "anchor_hunt.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "study_anchor_hunt.md").write_text(_render_report(results))
    return results


def _render_report(results: dict) -> str:
    gate = results["harness_gate"]
    lines = [
        "# T2.3 Study Report — Anchor Hunt (W3)",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.studies.anchor_hunt`; full numbers in "
        "`results/studies/anchor_hunt.json`.",
        "",
        f"Section {results['section']}: {results['pages']} pages, "
        f"{results['testable_tokens']} testable tokens × {results['testable_features']} "
        f"feature indicators = {results['tests']:,} tests, BH-FDR q={results['fdr_q']}.",
        "",
        "## Harness gate (L4 — must pass before anchors are admissible)",
        "",
        f"- **Null control** (features × page-shuffled text): "
        f"{gate['null_control']['false_discoveries']} false discoveries in "
        f"{gate['null_control']['tests']:,} tests "
        f"(fraction {gate['null_control']['false_discovery_fraction']}, ≤ q required).",
        f"- **Planted control** (synthetic token on '"
        f"{gate['planted_control'].get('planted_on_feature')}' pages): "
        f"recovered = {gate['planted_control'].get('recovered')} "
        f"(phi {gate['planted_control'].get('phi')}, p {gate['planted_control'].get('p')}).",
        f"- **Gate {'PASSED' if gate['passed'] else 'FAILED'}** — H1 anchors "
        f"{'admissible' if gate['passed'] else 'NOT admissible'}.",
        "",
    ]
    if results["anchors_admissible"]:
        lines += [
            "## Candidate anchors (graded C pending T3.3; L7 — no translation claim)",
            "",
            "Token↔feature associations surviving FDR, by phi. These are "
            "co-occurrence statistics, NOT meanings: a high-phi pair means the token "
            "and the visual feature tend to appear on the same pages, nothing more.",
            "",
            "| token | feature | phi | p | pages(token∧feature) |",
            "|---|---|---|---|---|",
        ]
        for anchor in results["anchors"][:30]:
            lines.append(
                f"| `{anchor['token']}` | {anchor['feature']} | {anchor['phi']} "
                f"| {anchor['p']} | {anchor['a']} |"
            )
        if not results["anchors"]:
            lines.append("| _(none survived FDR)_ | | | | |")
    else:
        lines += ["## Anchors withheld", "",
                  "The harness gate did not pass; no H1 anchors are reported "
                  "(L4). Investigate the failing control before interpreting."]
    lines += ["",
              "## Notes",
              "- Claims graded C (candidate B pending T3.3 adversarial review, L10).",
              "- L7: nothing here is a translation. An anchor is a statistical "
              "co-occurrence, to be corroborated by an independent method before any "
              "semantic reading is entertained.",
              ""]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print(json.dumps({k: v for k, v in out.items() if k != "anchors"}, indent=2))
    print(f"admissible anchors: {len(out['anchors'])}")
