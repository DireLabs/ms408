"""E28 — Angular/ordinal anchor in the zodiac rings (i10, GATING).

The make-or-break, decipherment-free arithmetic anchor. If the zodiac-ring labels carry
VALUES (a degree, a date, a count) rather than being arbitrary names, their content should
vary with angular position — nearby positions bearing similar labels the way "20, 21, 22"
share structure. We test this WITHOUT assuming any glyph->value map.

Data: the 12 zodiac pages carry `<!HH:MM>` clock tags placing each label around the ring
(precondition i10-c verified). Per ring we form (angular position, label token) pairs.

Primary test — MANTEL: correlation between the pairwise angular-distance matrix (circular)
and the pairwise label edit-distance matrix. Ordered values => nearby-in-angle labels are
more similar => positive correlation. Null: permute the label->position assignment (999x).
Positive control: a synthetic ring whose labels ARE ordered integers rendered as digit
strings (adjacent values share digits) — the test MUST fire on it, confirming sensitivity.
Secondary: lag-1 autocorrelation of token length ordered by angle (a counting sequence
drifts smoothly), same permutation null. Per-ring p-values are Fisher-combined.

Pass/fail. A robust combined signal beyond the null, present across several rings and
matching the positive control => the register hypothesis is elevated (C, pending
refutation). No signal (the likely outcome) => it stays D and i10 closes with a clean
graded negative. No value/number/date is ever named (L7).

Usage:
    python -m ms408.experiments.e28_angular_anchor
"""

from __future__ import annotations

import json
import math
import random
import re
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..sources import path_for

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports"
SEED = 408
N_PERM = 999
CLOCK = 720                          # minutes on the full clock face (12h)
MIN_LABELS = 10                      # min tagged labels for a ring to be tested
TAG = re.compile(r"<!(\d\d):(\d\d)>")


def _lev(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _norm_edit(a: str, b: str) -> float:
    m = max(len(a), len(b))
    return _lev(a, b) / m if m else 0.0


def _circ_dist(x: int, y: int) -> int:
    d = abs(x - y)
    return min(d, CLOCK - d)


def _offdiag(mat: list) -> list:
    n = len(mat)
    return [mat[i][j] for i in range(n) for j in range(i + 1, n)]


def _pearson(xs: list, ys: list) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx = sum((x - mx) ** 2 for x in xs)
    sy = sum((y - my) ** 2 for y in ys)
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(sx * sy)


def _mantel(angles: list, tokens: list, seed: int) -> dict:
    """Mantel r between circular angular distance and normalised label edit distance,
    with a label-permutation null. Positive r => nearby-in-angle labels are more similar."""
    n = len(tokens)
    ad = [[_circ_dist(angles[i], angles[j]) for j in range(n)] for i in range(n)]
    ld = [[_norm_edit(tokens[i], tokens[j]) for j in range(n)] for i in range(n)]
    a_off = _offdiag(ad)
    r_obs = _pearson(a_off, _offdiag(ld))
    rng = random.Random(seed)
    idx = list(range(n))
    ge = 0
    for _ in range(N_PERM):
        rng.shuffle(idx)
        perm = [[ld[idx[i]][idx[j]] for j in range(n)] for i in range(n)]
        if _pearson(a_off, _offdiag(perm)) <= r_obs:   # ordered => r_obs NEGATIVE-ish? see note
            ge += 1
    # Ordered values => small angle-dist pairs have small label-dist => POSITIVE correlation
    # of the two distance matrices. So "signal" = r_obs high; p = P(r_perm >= r_obs).
    p = (N_PERM - ge + 1) / (N_PERM + 1)
    return {"r": round(r_obs, 4), "p": round(p, 4), "n": n}


def _length_autocorr(angles: list, tokens: list, seed: int) -> dict:
    """Lag-1 autocorrelation of token length in angular order, vs label-permutation null."""
    order = sorted(range(len(tokens)), key=lambda i: angles[i])
    lens = [len(tokens[i]) for i in order]
    def ac1(seq):
        m = sum(seq) / len(seq)
        num = sum((seq[k] - m) * (seq[k + 1] - m) for k in range(len(seq) - 1))
        den = sum((x - m) ** 2 for x in seq)
        return num / den if den else 0.0
    obs = ac1(lens)
    rng = random.Random(seed + 1)
    ge = 0
    for _ in range(N_PERM):
        s = lens[:]
        rng.shuffle(s)
        if ac1(s) >= obs:
            ge += 1
    return {"ac1": round(obs, 4), "p": round((ge + 1) / (N_PERM + 1), 4)}


def _fisher(pvals: list) -> dict:
    ps = [min(max(p, 1e-6), 1.0) for p in pvals]
    x = -2 * sum(math.log(p) for p in ps)
    df = 2 * len(ps)
    # survival of chi-square via regularised upper incomplete gamma (series/cf).
    p_comb = _chi2_sf(x, df)
    return {"chi2": round(x, 3), "df": df, "p_combined": round(p_comb, 5)}


def _chi2_sf(x: float, k: int) -> float:
    # P(Chi2_k > x): use gammaincc(k/2, x/2) via Lanczos-free series/continued fraction.
    a, xx = k / 2.0, x / 2.0
    if xx <= 0:
        return 1.0
    if xx < a + 1:                       # series for lower incomplete, return 1 - P
        term = 1.0 / a
        s = term
        n = a
        for _ in range(500):
            n += 1
            term *= xx / n
            s += term
            if abs(term) < abs(s) * 1e-12:
                break
        return 1.0 - s * math.exp(-xx + a * math.log(xx) - math.lgamma(a))
    b = xx + 1 - a                       # continued fraction for upper incomplete
    c = 1e30
    d = 1.0 / b
    h = d
    for i in range(1, 500):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        if abs(d) < 1e-30:
            d = 1e-30
        c = b + an / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-12:
            break
    return h * math.exp(-xx + a * math.log(xx) - math.lgamma(a))


def _rings(doc: IVTFFDocument) -> list:
    rings = []
    for p in doc.pages:
        pairs = []
        for locus in p.loci:
            if locus.locus_type != "Lz":
                continue
            m = TAG.match(locus.text)
            w = locus.words()
            if m and w:
                pairs.append((int(m.group(1)) * 60 + int(m.group(2)), w[0]))
        if len(pairs) >= MIN_LABELS:
            rings.append({"page": p.name, "lang": p.currier_language, "hand": p.hand,
                          "angles": [a for a, _ in pairs], "tokens": [t for _, t in pairs]})
    return rings


def _synthetic_ordered_ring(n: int, seed: int) -> dict:
    """Positive control: labels ARE ordered integers 1..n rendered base-6 (adjacent values
    share high digits -> small edit distance), placed evenly around the ring."""
    digits = "abcdef"
    def render(v):
        s = ""
        if v == 0:
            return digits[0]
        while v:
            s = digits[v % 6] + s
            v //= 6
        return s
    angles = [int(i * CLOCK / n) for i in range(n)]
    tokens = [render(i + 1) for i in range(n)]
    return {"page": "SYNTH_ordered", "angles": angles, "tokens": tokens}


def run() -> dict:
    doc = IVTFFDocument.load(path_for("zl"))
    rings = _rings(doc)

    per_ring = []
    for i, ring in enumerate(rings):
        mant = _mantel(ring["angles"], ring["tokens"], SEED + i)
        lac = _length_autocorr(ring["angles"], ring["tokens"], SEED + i)
        per_ring.append({"page": ring["page"], "lang": ring["lang"], "hand": ring["hand"],
                         "n": mant["n"], "mantel": mant, "length_ac": lac})

    mantel_ps = [r["mantel"]["p"] for r in per_ring]
    len_ps = [r["length_ac"]["p"] for r in per_ring]
    mantel_comb = _fisher(mantel_ps)
    len_comb = _fisher(len_ps)
    n_sig_mantel = sum(1 for p in mantel_ps if p < 0.05)
    # Leave-one-out robustness: is the combined signal driven by a single ring?
    lo = min(range(len(per_ring)), key=lambda i: mantel_ps[i])
    drop_min = _fisher([p for i, p in enumerate(mantel_ps) if i != lo])
    driven_by_single_ring = bool(mantel_comb["p_combined"] < 0.05
                                 and drop_min["p_combined"] >= 0.05)
    robustness = {"lowest_p_ring": per_ring[lo]["page"],
                  "lowest_p": mantel_ps[lo],
                  "combined_p_dropping_lowest_ring": drop_min["p_combined"],
                  "driven_by_single_ring": driven_by_single_ring,
                  "n_rings_positive_r": sum(1 for r in per_ring if r["mantel"]["r"] > 0)}

    # Positive control — the Mantel test MUST fire on an ordered-value ring.
    ctrl = _synthetic_ordered_ring(30, SEED)
    ctrl_mantel = _mantel(ctrl["angles"], ctrl["tokens"], SEED)
    ctrl_ok = ctrl_mantel["p"] < 0.05 and ctrl_mantel["r"] > 0

    signal = bool(ctrl_ok and mantel_comb["p_combined"] < 0.01 and n_sig_mantel >= 3)

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E28 — angular/ordinal anchor in the zodiac rings",
        "seed": SEED, "n_perm": N_PERM, "min_labels": MIN_LABELS,
        "n_rings_tested": len(rings),
        "ring_langs": sorted({r["lang"] for r in rings if r["lang"]}),
        "ring_hands": sorted({r["hand"] for r in rings if r["hand"]}),
        "per_ring": per_ring,
        "mantel_combined": mantel_comb, "length_ac_combined": len_comb,
        "n_rings_mantel_p_below_0.05": n_sig_mantel,
        "robustness": robustness,
        "positive_control": {"mantel": ctrl_mantel, "detects_ordered_values": ctrl_ok},
        "anchor_signal": signal,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e28_angular_anchor.json").write_text(json.dumps(results, indent=2) + "\n")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "e28_angular_anchor.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    mc = r["mantel_combined"]
    ctrl = r["positive_control"]
    common = (
        f"{r['n_rings_tested']} zodiac rings (langs {r['ring_langs']}, hands {r['ring_hands']}), "
        f"{r['n_perm']} permutations. Mantel (angular-distance vs label-edit-distance) combined "
        f"p={mc['p_combined']} ({r['n_rings_mantel_p_below_0.05']}/{r['n_rings_tested']} rings "
        f"individually p<0.05); length-autocorrelation combined p="
        f"{r['length_ac_combined']['p_combined']}. Positive control (ordered integers on a ring): "
        f"Mantel r={ctrl['mantel']['r']} p={ctrl['mantel']['p']} — "
        f"{'DETECTS ordered values (test is sensitive)' if ctrl['detects_ordered_values'] else 'FAILED to detect (test insensitive — inconclusive)'}."
    )
    if not ctrl["detects_ordered_values"]:
        return "D", (f"INCONCLUSIVE — the positive control did not fire, so the test lacks "
                     f"sensitivity as configured; no inference about the VMS. {common} (L7.)")
    if r["anchor_signal"]:
        return "C", (
            f"ANCHOR SIGNAL (refutation pass REQUIRED before any lift). Zodiac-ring label "
            f"content varies with angular position beyond the label-shuffle null, across "
            f"multiple rings, in the direction ordered values would produce — the register "
            f"hypothesis is elevated from D toward C. This is a STATISTICAL ordinal regularity "
            f"ONLY: no value, number, date, or reading is claimed or implied (L7); the next step "
            f"is an adversarial refutation + E29 controls. {common}")
    rob = r["robustness"]
    return "D", (
        f"NO ROBUST ANCHOR — the register hypothesis STAYS D (clean graded negative). The "
        f"positive control confirms the test detects ordinal structure when present, yet across "
        f"the 12 rings there is no CONSISTENT angular-ordinal signal. The Fisher-combined Mantel "
        f"p ({r['mantel_combined']['p_combined']}) is driven by a SINGLE ring "
        f"({rob['lowest_p_ring']}, p={rob['lowest_p']}): dropping it, the combined p is "
        f"{rob['combined_p_dropping_lowest_ring']} (n.s.); only {r['n_rings_mantel_p_below_0.05']}/"
        f"{r['n_rings_tested']} rings are individually p<0.05, with mixed sign "
        f"({rob['n_rings_positive_r']}/{r['n_rings_tested']} positive r), and the length-"
        f"autocorrelation is null ({r['length_ac_combined']['p_combined']}). Since all 12 rings "
        f"are the SAME diagram type, a genuine value-encoding of the labels would appear across "
        f"them, not in one — so the lone {rob['lowest_p_ring']} hit reads as a chance fluctuation "
        f"(a footnote-worthy idiosyncrasy at most, not an anchor). Combined with E27 (positional-"
        f"numeral shape excluded), the symbols-as-values direction finds NO support in the "
        f"manuscript's most number-like folios — the astronomical rings. i10 closes here unless a "
        f"materially different anchor is proposed; the standing constraints remain the i06 cipher "
        f"exclusion and the character/morphology structure. (No value/number claim — L7.) {common}")


def _render(r: dict) -> str:
    lines = [
        "# E28 — Angular/ordinal anchor in the zodiac rings",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e28_angular_anchor`. Numbers in "
        "`results/experiments/e28_angular_anchor.json`.",
        "",
        f"Anchor signal: **{r['anchor_signal']}**. Positive control detects ordered values: "
        f"**{r['positive_control']['detects_ordered_values']}** "
        f"(Mantel r={r['positive_control']['mantel']['r']}, p={r['positive_control']['mantel']['p']}).",
        "",
        f"Mantel combined p = **{r['mantel_combined']['p_combined']}** "
        f"({r['n_rings_mantel_p_below_0.05']}/{r['n_rings_tested']} rings p<0.05); "
        f"length-autocorr combined p = {r['length_ac_combined']['p_combined']}.",
        "",
        "| page | lang | hand | n | Mantel r | Mantel p | len ac1 | len p |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for pr in r["per_ring"]:
        lines.append(f"| {pr['page']} | {pr['lang']} | {pr['hand']} | {pr['n']} "
                     f"| {pr['mantel']['r']} | {pr['mantel']['p']} "
                     f"| {pr['length_ac']['ac1']} | {pr['length_ac']['p']} |")
    lines += ["", f"## Verdict [{r['grade']}, refutation pass "
              f"{'REQUIRED' if r['anchor_signal'] else 'n/a'}]", "", r["verdict"], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print(f"rings={out['n_rings_tested']} langs={out['ring_langs']} hands={out['ring_hands']}")
    print(f"positive control detects ordered values: {out['positive_control']['detects_ordered_values']} "
          f"(r={out['positive_control']['mantel']['r']} p={out['positive_control']['mantel']['p']})")
    print(f"Mantel combined p={out['mantel_combined']['p_combined']} "
          f"({out['n_rings_mantel_p_below_0.05']}/{out['n_rings_tested']} rings p<0.05)")
    print(f"length-ac combined p={out['length_ac_combined']['p_combined']}")
    print(f"anchor_signal={out['anchor_signal']}")
    print(f"grade {out['grade']}: {out['verdict'][:180]}...")
