"""Reproduce-our-numbers self-check for the evaluator (the firewall, made runnable).

The shipped reference bands (`ms408/data/reference_bands.json`) are what `evaluate()`
checks against. This module proves those numbers are reproducible from committed code plus
the acquired VMS corpus — nothing is hand-entered.

    python -m ms408.verify          # quick: recompute VMS point + self-consistency (~seconds)
    python -m ms408.verify --full   # also rebuild the bands and diff vs the shipped file (~1 min)

Exit code 0 iff every check passes. Needs the acquired corpus (`python -m ms408.acquire`);
without it the checks that require VMS text are reported as SKIPPED and do not fail the run.
This checks the EVALUATOR's own artifact. Full paper-number reproduction is per-experiment:
each `ms408.experiments.e*` writes its `results/*.json` with its own provenance.
"""

from __future__ import annotations

import argparse

from .signature import HARD_AXES, axis_values, vms_bands
from .sources import path_for

TOL = 1e-9   # profile axes are deterministic; syntax z's are seed-fixed -> exact match
INFO = "info"   # a reported observation, not a pass/fail check (None means SKIPPED)


def _have_corpus() -> bool:
    return path_for("zl").exists()


def _check_vms_point(bands: dict) -> list:
    """Recompute each dialect's point signature from the corpus; must equal the shipped one."""
    from .experiments.e13_function_content import N_TOKENS, _sub, _vms_tokens

    out = []
    for dialect, spec in bands["dialects"].items():
        fresh = axis_values(_sub(_vms_tokens(dialect), N_TOKENS))
        for axis, exp in spec["vms_point"].items():
            got = fresh.get(axis)
            if isinstance(exp, (int, float)) and isinstance(got, (int, float)):
                ok = abs(got - exp) <= TOL
            else:
                ok = got == exp
            out.append((f"vms_point.{dialect}.{axis}", ok,
                        f"shipped {exp} vs recomputed {got}"))
    return out


def _check_self_consistency(bands: dict) -> list:
    """Each dialect's point must lie inside its OWN hard bands (else it is miscalibrated)."""
    out = []
    for dialect, spec in bands["dialects"].items():
        point, axes = spec["vms_point"], spec["axes"]
        for axis in sorted(HARD_AXES):
            lo, hi = axes[axis]["band"]
            v = point[axis]
            out.append((f"self-consistency.{dialect}.{axis}", bool(lo <= v <= hi),
                        f"{v} in [{lo}, {hi}]"))
    return out


def _check_dialect_separation(bands: dict) -> list:
    """The dialects must actually differ (D21): if every dialect point sat inside every
    other dialect's hard bands, stratifying would be pointless and the split would be
    hiding rather than showing structure. Reported, never failed — this is a description
    of the manuscript, not a property the code controls."""
    out = []
    dialects = bands["dialects"]
    for d, spec in dialects.items():
        for other, ospec in dialects.items():
            if other == d:
                continue
            hits = [a for a in sorted(HARD_AXES)
                    if ospec["axes"][a]["band"][0] <= spec["vms_point"][a]
                    <= ospec["axes"][a]["band"][1]]
            out.append((f"cross-dialect.{d}-in-{other}", INFO,
                        f"{len(hits)}/{len(HARD_AXES)} hard axes"
                        f"{' (' + ', '.join(hits) + ')' if hits else ''}"))
    return out


def _check_full_rebuild(bands: dict) -> list:
    """Rebuild the bands from code and diff every dialect's point + axis bands."""
    from .experiments.e32_reference_bands import build

    rebuilt = build()
    out = []
    for dialect, spec in bands["dialects"].items():
        fresh = rebuilt["dialects"].get(dialect, {})
        for axis, exp in spec["vms_point"].items():
            got = fresh.get("vms_point", {}).get(axis)
            ok = abs(got - exp) <= TOL if isinstance(exp, (int, float)) else got == exp
            out.append((f"rebuild.{dialect}.vms_point.{axis}", ok, f"{exp} vs {got}"))
        for axis, aspec in spec["axes"].items():
            got = fresh.get("axes", {}).get(axis, {}).get("band")
            out.append((f"rebuild.{dialect}.band.{axis}", got == aspec["band"],
                        f"{aspec['band']} vs {got}"))
    return out


def verify(full: bool = False) -> tuple[int, list]:
    bands = vms_bands()
    checks: list = []
    checks += _check_dialect_separation(bands)
    if _have_corpus():
        checks += _check_vms_point(bands)
        checks += _check_self_consistency(bands)
        if full:
            checks += _check_full_rebuild(bands)
    else:
        checks.append(("corpus", None, "VMS corpus not acquired — run `python -m ms408.acquire`"))
    failed = sum(1 for _, ok, _ in checks if ok is False)
    return failed, checks


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ms408.verify",
                                 description="Reproduce the evaluator's shipped numbers from code.")
    ap.add_argument("--full", action="store_true",
                    help="also rebuild the reference bands and diff against the shipped file")
    args = ap.parse_args(argv)

    failed, checks = verify(full=args.full)
    for name, ok, detail in checks:
        tag = ("SKIP" if ok is None else "INFO" if ok == INFO
               else ("PASS" if ok else "FAIL"))
        print(f"[{tag}] {name}: {detail}")
    print("-" * 60)
    if any(ok is None for _, ok, _ in checks):
        print("Some checks skipped (corpus not acquired).")
    print("OK — shipped numbers reproduce from code." if failed == 0
          else f"{failed} check(s) FAILED — shipped numbers do not match code.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
