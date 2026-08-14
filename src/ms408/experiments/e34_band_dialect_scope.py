"""E34 — diagnostic: what dialect are the shipped reference bands actually built from?

E32 builds the public evaluator's bands from ``_sub(_vms_tokens("A") + _vms_tokens("B"),
N_TOKENS)``. Currier A alone supplies 10,709 paragraph tokens and ``N_TOKENS`` is 10,000,
so the truncation consumes A and never reaches B — while B is 22,864 tokens, the majority
of the manuscript. The shipped artifact's metadata nevertheless reads "Currier A+B".

This script does not change the bands. It measures the consequence so the scoping decision
(see docs/planning/i01/DECISIONS.md) is made against numbers rather than an argument:
it slides a matched-budget window across each dialect and records, for each window, how
many HARD axes fall inside the shipped bands.

Windows are ``N_TOKENS`` wide at ``STEP``-token strides, plus a final window flush to the
end of the dialect so the tail is covered. Windows overlap, so the per-dialect counts below
are NOT independent samples — they describe coverage of the dialect, not a significance
test.

Writes: ``results/experiments/e34_band_dialect_scope.json``.

Usage:
    python -m ms408.experiments.e34_band_dialect_scope
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..signature import HARD_AXES, axis_values, vms_bands
from .e13_function_content import N_TOKENS, _vms_tokens

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"

STEP = 1000
DIALECTS = ("A", "B")


def _windows(tokens: list, width: int, step: int) -> list:
    """Start offsets for `width`-token windows at `step` strides, tail included."""
    last = len(tokens) - width
    if last < 0:
        return []
    starts = list(range(0, last + 1, step))
    if starts[-1] != last:
        starts.append(last)
    return starts


def _score(vals: dict, bands: dict) -> dict:
    """Hard-axis in-band tally for one window's axis values against one dialect's bands.

    Takes precomputed values (from `axis_values`, the evaluator's own code path) because
    each window is scored against every dialect and the axes are the expensive part.
    """
    axes = {}
    for axis in sorted(HARD_AXES):
        band = bands["axes"][axis]["band"]
        value = vals[axis]
        in_band = None if (value is None or band is None) else bool(
            band[0] <= value <= band[1]
        )
        axes[axis] = {"value": value, "band": band, "in_band": in_band}
    scored = [a for a in axes.values() if a["in_band"] is not None]
    return {
        "axes": axes,
        "hard_axes_in_band": sum(a["in_band"] for a in scored),
        "hard_axes_total": len(scored),
    }


def build() -> dict:
    hard = sorted(HARD_AXES)
    dialects, windows = {}, []
    for d in DIALECTS:
        own = vms_bands(d)
        toks = _vms_tokens(d)
        starts = _windows(toks, N_TOKENS, STEP)
        scored = []
        for s in starts:
            vals = axis_values(toks[s : s + N_TOKENS])
            w = _score(vals, own)
            # Also score against every OTHER dialect's bands: the cross-dialect cell is
            # what makes the stratification worth having (or not).
            w |= {"dialect": d, "start": s,
                  "vs_other": {o: _score(vals, vms_bands(o))["hard_axes_in_band"]
                               for o in DIALECTS if o != d}}
            windows.append(w)
            scored.append(w)
        dialects[d] = {
            "tokens": len(toks),
            "n_windows": len(scored),
            "scored_against": f"Currier {d} bands (its own)",
            "per_axis_in_band": {
                a: sum(1 for w in scored if w["axes"][a]["in_band"]) for a in hard
            },
            "best_hard_axes_in_band": max((w["hard_axes_in_band"] for w in scored),
                                          default=None),
            "worst_hard_axes_in_band": min((w["hard_axes_in_band"] for w in scored),
                                           default=None),
            "vs_other_best": {
                o: max((w["vs_other"][o] for w in scored), default=None)
                for o in DIALECTS if o != d
            },
        }

    tokens_by_dialect = {d: dialects[d]["tokens"] for d in DIALECTS}
    total = sum(tokens_by_dialect.values())
    return {
        "meta": {
            "script": "ms408.experiments.e34_band_dialect_scope",
            "git_commit": git_commit(),
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "purpose": "Coverage check on the per-dialect reference bands (D21): does "
                       "each dialect's band set, built from that dialect's first "
                       f"{N_TOKENS} paragraph tokens, actually cover the REST of the same "
                       "dialect? And how far off is the other dialect? Originally written "
                       "to demonstrate the pre-D21 defect, where a single band set "
                       "labelled 'A+B' contained only A.",
            "band_provenance": vms_bands()["meta"],
            "n_tokens": N_TOKENS,
            "step": STEP,
            "hard_axes": hard,
            "caveat": "Windows overlap and each dialect's own bands were built from its "
                      "first window, so 'own-band' coverage is not an out-of-sample test "
                      "for that first window. Counts describe coverage, not independent "
                      "samples. No decipherment or meaning claim (L7).",
        },
        "dialects": dialects,
        "corpus": {
            "tokens_by_dialect": tokens_by_dialect,
            "b_share_of_corpus": round(tokens_by_dialect["B"] / total, 4),
            "prefix_share_of_dialect": {
                d: round(min(1.0, N_TOKENS / tokens_by_dialect[d]), 4) for d in DIALECTS
            },
        },
        "windows": windows,
    }


def run() -> dict:
    art = build()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e34_band_dialect_scope.json").write_text(
        json.dumps(art, indent=2) + "\n"
    )
    return art


if __name__ == "__main__":
    art = run()
    c = art["corpus"]
    print(f"corpus tokens by dialect: {c['tokens_by_dialect']} "
          f"(B is {c['b_share_of_corpus']:.0%} of the manuscript); each dialect's bands "
          f"are built from its first {N_TOKENS}, i.e. "
          + ", ".join(f"{d} {s:.0%}" for d, s in c["prefix_share_of_dialect"].items()))
    n_hard = len(art["meta"]["hard_axes"])
    for d, s in art["dialects"].items():
        per = ", ".join(f"{a} {n}/{s['n_windows']}" for a, n in s["per_axis_in_band"].items())
        other = ", ".join(f"vs {o} best {v}/{n_hard}" for o, v in s["vs_other_best"].items())
        print(f"  Currier {d}: {s['n_windows']:>2} windows vs its OWN bands — {per}"
              f" | best {s['best_hard_axes_in_band']}/{n_hard}, worst "
              f"{s['worst_hard_axes_in_band']}/{n_hard} | {other}")
