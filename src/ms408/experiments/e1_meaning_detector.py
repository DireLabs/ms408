"""E1 — Is Montemurro-Zanette DI a meaning detector? (i02, critique C5)

i01 leaned on the VMS scoring MZ DI ~ 0.31 while a self-citation null scored
lower. The critique: MZ is a topic-clustering statistic, and the null was self-
tuned. E1 settles it with a clean isolation.

**Design.** Take the VMS's OWN token multiset (its word types at their real
frequencies) — so character entropy h2 and Zipf are matched EXACTLY, by
construction — and produce a MEANINGLESS reordering in which each word type is
clustered around a random centre with a tunable spread. This changes only word
ORDER, nothing else. If a meaningless reordering reproduces the VMS's DI at the
VMS's scale, then DI does not require meaning.

Parameters of the drift null:
- `spread_frac`: each type's tokens are placed at positions drawn around a random
  centre with stdev = spread_frac * N. Small -> contiguous blocks (high DI);
  large -> uniform (DI ~ 0). Controls DI magnitude.
- The characteristic scale emerges from the clustering; we also report it.

The objective is to MAXIMIZE DI (blind to the 0.31 target) and, separately, to
find the spread that best matches the VMS DI, then compare peak scales. We also
bootstrap the VMS DI to a CI so "0.31 vs X" is meaningful.

Usage:
    python -m ms408.experiments.e1_meaning_detector
"""

from __future__ import annotations

import json
import random
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..mz import delta_information, peak, scan_scales
from ..replication import _MZ_ORDER, _mz_section, paragraph_lines
from ..sources import path_for

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
REPORTS_DIR = ROOT / "reports"
SEED = 408
BOOTSTRAP = 400


def vms_tokens() -> list:
    lines = paragraph_lines(IVTFFDocument.load(path_for("zl")))
    return [
        w
        for section in _MZ_ORDER
        for line in lines
        if _mz_section(line) == section
        for w in line.words
    ]


def drift_reorder(tokens: list, spread_frac: float, rng: random.Random) -> list:
    """Meaningless reordering of the SAME multiset: each type clustered around a
    random centre with stdev spread_frac*N. Character stats + Zipf are unchanged;
    only word order changes."""
    n = len(tokens)
    by_type: dict = {}
    for t in tokens:
        by_type.setdefault(t, 0)
        by_type[t] += 1
    placements = []  # (position, token)
    for word_type, count in by_type.items():
        centre = rng.uniform(0, n)
        for _ in range(count):
            pos = rng.gauss(centre, spread_frac * n) % n
            placements.append((pos, word_type))
    placements.sort()
    return [t for _, t in placements]


def bootstrap_vms_di(tokens: list, parts: int, seed: int) -> dict:
    """CI on the VMS DI at a fixed part count via block bootstrap over parts."""
    rng = random.Random(seed)
    size = len(tokens) // parts
    blocks = [tokens[i * size:(i + 1) * size] for i in range(parts)]
    values = []
    for _ in range(BOOTSTRAP):
        resampled = []
        for _ in range(parts):
            resampled.extend(rng.choice(blocks))
        values.append(delta_information(resampled, parts)[0])
    values.sort()
    return {
        "mean": round(sum(values) / len(values), 4),
        "ci95": [round(values[int(0.025 * BOOTSTRAP)], 4),
                 round(values[int(0.975 * BOOTSTRAP)], 4)],
    }


def run() -> dict:
    tokens = vms_tokens()
    n = len(tokens)

    vms_scan = scan_scales(tokens)
    vms_scale, vms_parts, vms_di = peak(vms_scan)
    vms_ci = bootstrap_vms_di(tokens, vms_parts, SEED)

    # sweep the meaningless drift null across spreads; for each, its own DI + scale
    sweep = []
    for spread in (0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30):
        # average a few random meaningless orderings at this spread
        dis, scales = [], []
        for rep in range(3):
            reordered = drift_reorder(tokens, spread, random.Random(SEED + rep))
            s, _, v = peak(scan_scales(reordered))
            dis.append(v)
            scales.append(s)
        sweep.append({
            "spread_frac": spread,
            "mean_di": round(sum(dis) / len(dis), 4),
            "mean_peak_scale": int(sum(scales) / len(scales)),
        })

    # the spread whose DI best matches the VMS DI, and the max achievable DI
    best_match = min(sweep, key=lambda r: abs(r["mean_di"] - vms_di))
    max_di = max(sweep, key=lambda r: r["mean_di"])
    reaches_vms = max_di["mean_di"] >= vms_ci["ci95"][0]

    # verify character stats truly unchanged under reordering (sanity)
    stats_identical = Counter(tokens) == Counter(
        drift_reorder(tokens, 0.05, random.Random(1)))

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E1 — is MZ DI a meaning detector?",
        "tokens": n,
        "vms": {"peak_scale": vms_scale, "peak_di": round(vms_di, 4),
                "di_ci95": vms_ci["ci95"]},
        "drift_null_sweep": sweep,
        "meaningless_best_di_match": best_match,
        "meaningless_max_di": max_di,
        "meaningless_reaches_vms_di": bool(reaches_vms),
        "character_stats_preserved_by_reorder": bool(stats_identical),
        "self_citation_reference": {
            "note": "i01 encoding bracket: the self-citation null scored MZ DI "
            "0.497 (already > VMS 0.307), at scale 275 — an independent second "
            "meaningless generator that also exceeds the VMS DI.",
        },
    }
    verdict, grade = _verdict(results)
    results["verdict"] = verdict
    results["grade"] = grade

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e1_meaning_detector.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "e1_meaning_detector.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    # Revised per E1's clean-context refutation pass (standing i02 rule). The
    # critic accepted the modest point and refuted the strong one: (1) the
    # drift-null installs clustering by fiat rather than via a meaningless PROCESS
    # (question-begging for a sufficiency claim); (2) DI is a curve peaking at a
    # characteristic SCALE, and the drift-null hits the VMS value only at the wrong
    # scale (1624+ vs 812) — matching height but not location.
    return (
        "MODEST claim stands, STRONG claim withdrawn. Established [C, already "
        "conceded in i01]: the DI *value* alone is not a meaning certificate — a "
        "meaningless reordering of the VMS's own words reaches and exceeds it "
        "(max 2.2 vs VMS 0.307), so a high DI value does not imply content. NOT "
        "established: that a meaningless PROCESS reproduces the VMS phenomenon, "
        "which is DI value AND its 812-word characteristic scale. The drift-null "
        "hits the value at the wrong scale; the i01 self-citation process overshot "
        "the value (0.497) also at the wrong scale (275). E2 resolves what the 812 "
        "scale IS — it is the section/topic-block scale (blocked Vulgate books peak "
        "at 812), reachable by any block-structured vocabulary, meaningful or not. "
        "Net: DI cannot settle meaningful-vs-meaningless (confirms T3.3/C5); the "
        "812 scale is a block-structure signature, not a meaning signature.",
        "C",
    )


def _render(r: dict) -> str:
    v = r["vms"]
    lines = [
        "# E1 — Is Montemurro-Zanette DI a meaning detector?",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e1_meaning_detector`. Full numbers in "
        "`results/experiments/e1_meaning_detector.json`.",
        "",
        f"**Design.** Reorder the VMS's own {r['tokens']:,} tokens meaninglessly "
        "(each word type clustered around a random centre). Character entropy and "
        "Zipf are unchanged by construction "
        f"(verified: {r['character_stats_preserved_by_reorder']}); only word ORDER "
        "changes. Question: does reproducing the VMS DI require meaning?",
        "",
        f"**VMS:** DI = {v['peak_di']} at scale {v['peak_scale']} words "
        f"(bootstrap 95% CI {v['di_ci95']}).",
        "",
        "## Meaningless drift-null sweep",
        "",
        "| spread (frac of N) | mean DI | mean peak scale |",
        "|---|---|---|",
    ]
    for row in r["drift_null_sweep"]:
        lines.append(f"| {row['spread_frac']} | {row['mean_di']} "
                     f"| {row['mean_peak_scale']} |")
    lines += [
        "",
        f"- Meaningless generator's **max DI**: {r['meaningless_max_di']['mean_di']} "
        f"(spread {r['meaningless_max_di']['spread_frac']}, scale "
        f"{r['meaningless_max_di']['mean_peak_scale']}).",
        f"- Best DI match to VMS: {r['meaningless_best_di_match']['mean_di']} "
        f"at scale {r['meaningless_best_di_match']['mean_peak_scale']}.",
        f"- **Reaches VMS DI: {r['meaningless_reaches_vms_di']}**.",
        "",
        f"Independent corroboration: {r['self_citation_reference']['note']}",
        "",
        f"## Verdict [{r['grade']}, pending refutation pass]",
        "",
        r["verdict"],
        "",
        "**Refutation pass outcome (standing i02 rule).** A clean-context critic "
        "WEAKENED the first draft, correctly: (1) the drift-null installs clustering "
        "by fiat rather than via a meaningless *process*, so it shows DI measures "
        "clustering, not that meaning is unnecessary for the manuscript; (2) DI is a "
        "curve peaking at a characteristic SCALE — the drift-null matches the VMS "
        "*value* (0.307) only at the wrong scale (1624+ vs 812), and matching height "
        "but not location is not reproducing the point. The strong claim "
        "('reproducing the manuscript's word-order information requires no meaning') "
        "is withdrawn; the modest claim ('DI value alone is not a meaning "
        "certificate') stands and was already conceded in i01.",
        "",
        "**Implication for the flagship.** Confirms the T3.3/C5 downgrade — the "
        "meaningful-vs-meaningless question cannot be settled by MZ. E2 identifies "
        "the 812-word scale as the section/topic-block scale (blocked meaningful "
        "text peaks there too), so the scale is a block-structure signature, not a "
        "meaning signature. The anti-uniform-cipher point is separate and is "
        "tested — and survives — in E2.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print(f"VMS DI {out['vms']['peak_di']} @ {out['vms']['peak_scale']} "
          f"(CI {out['vms']['di_ci95']})")
    print(f"meaningless max DI {out['meaningless_max_di']['mean_di']} "
          f"@ {out['meaningless_max_di']['mean_peak_scale']}")
    print(f"reaches VMS DI: {out['meaningless_reaches_vms_di']}")
    print(f"grade {out['grade']}: {out['verdict'][:100]}...")
