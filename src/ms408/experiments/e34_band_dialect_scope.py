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


def _score(tokens: list, bands: dict) -> dict:
    """Hard-axis in-band tally for one window, using the evaluator's own code path."""
    vals = axis_values(tokens)
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
    bands = vms_bands()
    hard = sorted(HARD_AXES)
    dialects, windows = {}, []
    for d in DIALECTS:
        toks = _vms_tokens(d)
        starts = _windows(toks, N_TOKENS, STEP)
        scored = []
        for s in starts:
            w = _score(toks[s : s + N_TOKENS], bands)
            w |= {"dialect": d, "start": s}
            windows.append(w)
            scored.append(w)
        dialects[d] = {
            "tokens": len(toks),
            "n_windows": len(scored),
            "per_axis_in_band": {
                a: sum(1 for w in scored if w["axes"][a]["in_band"]) for a in hard
            },
            "best_hard_axes_in_band": max((w["hard_axes_in_band"] for w in scored),
                                          default=None),
            "worst_hard_axes_in_band": min((w["hard_axes_in_band"] for w in scored),
                                           default=None),
        }

    tokens_by_dialect = {d: dialects[d]["tokens"] for d in DIALECTS}
    total = sum(tokens_by_dialect.values())
    return {
        "meta": {
            "script": "ms408.experiments.e34_band_dialect_scope",
            "git_commit": git_commit(),
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "purpose": "Diagnostic for the E32 band-scope defect: the shipped bands are "
                       "labelled Currier A+B but the A+B concatenation truncated at "
                       "N_TOKENS contains only A.",
            "band_provenance": bands["meta"],
            "n_tokens": N_TOKENS,
            "step": STEP,
            "hard_axes": hard,
            "caveat": "Windows overlap; per-dialect counts describe coverage, not "
                      "independent samples. No decipherment or meaning claim (L7).",
        },
        "band_sample_composition": {
            "expression": '_sub(_vms_tokens("A") + _vms_tokens("B"), N_TOKENS)',
            "tokens_by_dialect": tokens_by_dialect,
            "b_share_of_corpus": round(tokens_by_dialect["B"] / total, 4),
            "sample_is_pure_a": _vms_tokens("A")[:N_TOKENS]
            == (_vms_tokens("A") + _vms_tokens("B"))[:N_TOKENS],
            "b_tokens_in_band_sample": max(0, N_TOKENS - tokens_by_dialect["A"]),
        },
        "dialects": dialects,
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
    comp = art["band_sample_composition"]
    print(f"band sample is pure Currier A: {comp['sample_is_pure_a']} "
          f"(B tokens reaching the bands: {comp['b_tokens_in_band_sample']})")
    for d, s in art["dialects"].items():
        per = ", ".join(f"{a} {n}/{s['n_windows']}" for a, n in s["per_axis_in_band"].items())
        print(f"  Currier {d}: {s['tokens']:>6} tokens, {s['n_windows']:>2} windows — {per}"
              f" | best {s['best_hard_axes_in_band']}/{len(art['meta']['hard_axes'])}")
