"""E11 — Illustration-style control for the root↔leaf bundle (i04).

E10 reopened the root_coloring↔leaf_arrangement bundle: reproduced by two
independent Anthropic models and surviving scribal-hand + Currier-dialect
stratification. One residual confound (the E10 refutation) is a finer illustration-
STYLE convention — a drawing habit correlating how roots are coloured with how
leaves are drawn — that any competent rater would read off the same page without
implying real botanical structure. E11 conditions the association on an illustration-
style proxy and re-tests.

HONEST LIMITATION. The only usable page-level style annotation is `color_palette`
(text_image_relationship is ~constant; illustration_coverage_pct is unpopulated). So
E11 is a PARTIAL style control: it conditions on palette RICHNESS (a coarse drawing-
elaboration proxy, orthogonal to the specific root colour), not on every possible
drawing convention. A fuller control needs finer style annotation (i05+ item).

Method. Reuse E10's CMH-style within-stratum permutation test. Run the root↔leaf
association (sonnet_root×sonnet_leaf and haiku_root×haiku_leaf) stratified by, in
increasing fineness: palette-band alone; palette×dialect; and the full
palette×hand×dialect (flagged for over-stratification — tiny strata inflate p and
lose power, so it is reported, not decisive). Over-stratification guard: mean pages
per stratum reported; schemes below ~5/stratum are marked unreliable.

Pass/fail. If the association SURVIVES conditioning on palette style (both models,
permutation p<0.05, on a non-over-stratified scheme) → not a palette-style confound;
the bundle strengthens and E12 (independence) is the sole remaining test. If it
COLLAPSES within palette strata → an illustration-style artifact; the bundle is
KILLED and the i01 'within-organ only' leg re-locks.

Usage:
    python -m ms408.experiments.e11_style_control
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from .e10_third_rater import (
    OPUS_SRC,
    OUT as HAIKU_SRC,
    SONNET_SRC,
    _page_strata,
    _stratified_perm,
)

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"


def _palette_band(palette) -> str:
    n = len({p for p in (palette or [])})
    return "rich_4plus" if n >= 4 else "sparse_2to3"


def _load_sonnet_full() -> dict:
    out = {}
    for x in SONNET_SRC.read_text().splitlines():
        if not x.strip():
            continue
        rec = json.loads(x)
        sf = rec["section_features"]
        out[rec["page"]] = {
            "root": sf.get("root_coloring"), "leaf": sf.get("leaf_arrangement"),
            "palette": _palette_band(rec.get("common", {}).get("color_palette"))}
    return out


def _load_features(src: Path) -> dict:
    out = {}
    for x in src.read_text().splitlines():
        if not x.strip():
            continue
        rec = json.loads(x)
        f = rec["features"]
        out[rec["page"]] = {"root": f.get("root_coloring"),
                            "leaf": f.get("leaf_arrangement")}
    return out


def run() -> dict:
    sonnet = _load_sonnet_full()
    opus = _load_features(OPUS_SRC)
    haiku = _load_features(HAIKU_SRC)
    strata_map = _page_strata()
    pages = [p for p in haiku if p in sonnet and p in opus]

    palette = {p: sonnet[p]["palette"] for p in pages}
    hand_dialect = {p: strata_map.get(p, ("?", "?")) for p in pages}

    # Stratification schemes (increasing fineness).
    schemes = {
        "hand_dialect": [hand_dialect[p] for p in pages],           # E10 baseline
        "palette": [(palette[p],) for p in pages],                  # style alone
        "palette_dialect": [(palette[p], hand_dialect[p][1]) for p in pages],
        "palette_hand_dialect": [(palette[p], *hand_dialect[p]) for p in pages],
    }

    models = {
        "sonnet": ([sonnet[p]["root"] for p in pages],
                   [sonnet[p]["leaf"] for p in pages]),
        "haiku": ([haiku[p]["root"] for p in pages],
                  [haiku[p]["leaf"] for p in pages]),
    }

    results_by_scheme = {}
    for sname, strata in schemes.items():
        n_strata = len(set(strata))
        mean_per = round(len(pages) / n_strata, 1)
        per_model = {}
        for mname, (rv, lv) in models.items():
            per_model[mname] = _stratified_perm(rv, lv, strata, seed=hash(sname + mname) % 9999)
        results_by_scheme[sname] = {
            "n_strata": n_strata, "mean_pages_per_stratum": mean_per,
            "over_stratified": mean_per < 5.0,
            "sonnet": per_model["sonnet"], "haiku": per_model["haiku"]}

    # Decisive scheme = palette (style alone), not over-stratified. Both models must
    # survive (perm p<0.05) for the bundle to clear the palette-style confound.
    dec = results_by_scheme["palette"]
    survives_style = (not dec["over_stratified"]
                      and dec["sonnet"]["perm_p"] is not None
                      and dec["haiku"]["perm_p"] is not None
                      and dec["sonnet"]["perm_p"] < 0.05
                      and dec["haiku"]["perm_p"] < 0.05)

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E11 — illustration-style (palette) control for root↔leaf",
        "pages": len(pages),
        "style_proxy": "color_palette richness band (sparse 2-3 vs rich 4+ colours)",
        "palette_distribution": {b: sum(1 for p in pages if palette[p] == b)
                                 for b in ("sparse_2to3", "rich_4plus")},
        "stratified": results_by_scheme,
        "decisive_scheme": "palette",
        "bundle_survives_palette_style": bool(survives_style),
        "partial_control_caveat": "palette richness only; not a full drawing-style "
                                  "control (other style annotations unusable).",
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e11_style_control.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    dec = r["stratified"]["palette"]
    s, h = dec["sonnet"], dec["haiku"]
    common = (
        f"Palette control: sonnet V={s['observed_v']} p={s['perm_p']}, haiku "
        f"V={h['observed_v']} p={h['perm_p']} ({dec['n_strata']} strata, "
        f"{dec['mean_pages_per_stratum']} pg/stratum). PARTIAL control — palette "
        f"richness only ({r['partial_control_caveat']}); E12 (independent-lineage "
        f"rater) remains the decisive independence test. Visual-only; no plaintext or "
        f"real-taxon claim (L7).")
    if r["bundle_survives_palette_style"]:
        return "C", (
            "SURVIVES the palette-style control — the root↔leaf association holds "
            "within palette-richness bands for BOTH models, so it is not (this) "
            "illustration-style artifact. Combined with E10 (independent-model "
            "reproduction + hand/dialect survival), the bundle STRENGTHENS further; "
            "only the shared-Anthropic-lineage confound remains (E12). " + common)
    return "C", (
        "DOES NOT clearly survive the palette-style control for both models — "
        "consistent with (part of) the association being an illustration-style "
        "artifact rather than a referential bundle. The bundle is WEAKENED pending "
        "E12; if a fuller style control also collapses it, the E4b-in-spirit 'not a "
        "referential bundle' conclusion is restored. " + common)


if __name__ == "__main__":
    out = run()
    print(f"pages={out['pages']} palette={out['palette_distribution']}")
    for sname, sc in out["stratified"].items():
        flag = " OVER-STRATIFIED" if sc["over_stratified"] else ""
        print(f"  [{sname}] {sc['n_strata']} strata ({sc['mean_pages_per_stratum']} pg/str){flag}")
        for m in ("sonnet", "haiku"):
            v = sc[m]
            print(f"      {m:7s} V={v['observed_v']} p={v['perm_p']} n={v['n']}")
    print(f"survives_palette_style={out['bundle_survives_palette_style']}")
    print(f"grade {out['grade']}: {out['verdict'][:110]}...")
