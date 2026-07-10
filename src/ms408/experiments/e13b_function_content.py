"""E13b — Function/content via collocational selectivity (i05; redesign of E13).

E13's three global operationalisations failed harness calibration; two causes were
(1) type-token-ratio / randomness confounds and (2) contaminated nulls (self-citation,
conlang) that inherit real grammar. E13b fixes both with a CONTRAST that a clean null
must break.

Signal. In real language, CONTENT words have specific dominant collocates (a peaked
neighbour distribution — "peak selectivity" near 1) while FUNCTION words (and random
words) do not (flat neighbours). So the discriminator is the GAP
  gap = mean_selectivity(content-band types) - mean_selectivity(function-band types)
which is POSITIVE in real language and ~0 when order is destroyed. Selectivity is the
peak neighbour probability (normalised by the word's own count), so it is robust to
type-token ratio. Bands: function = top-5% most frequent types; content = mid-frequency
(freq in [MINFREQ, 60]).

Nulls. The only CLEAN null here is a full SHUFFLE (destroys all collocation). A 1st-
order Markov surrogate and a conlang relexification PRESERVE bigrams / real word order,
so they inherit the gap — they are reported but flagged CONTAMINATED, not used to set
the threshold. Calibration therefore separates real language from shuffle; the probe is
trusted only if that separation is clean (>= 0.05).

Usage:
    python -m ms408.experiments.e13b_function_content
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ..dataset import git_commit
from ..h4 import H4_OUT
from .e13_function_content import (
    MINFREQ,
    N_TOKENS,
    SEED,
    _markov1,
    _shuffle,
    _sub,
    _vms_tokens,
)
from .e6_cipher_reconstruction import _paradigmatic_conlang

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"
CONTENT_MAX_FREQ = 60


def _selectivity(tokens: list) -> dict:
    left = defaultdict(Counter)
    right = defaultdict(Counter)
    for i, w in enumerate(tokens):
        if i > 0:
            left[w][tokens[i - 1]] += 1
        if i < len(tokens) - 1:
            right[w][tokens[i + 1]] += 1

    def peak(c: Counter) -> float:
        n = sum(c.values())
        return max(c.values()) / n if n else 0.0

    return {w: (peak(left[w]) + peak(right[w])) / 2 for w in set(tokens)}


def _gap(tokens: list) -> dict:
    freq = Counter(tokens)
    sel = _selectivity(tokens)
    types = list(freq)
    if len(types) < 40:
        return {"insufficient": True, "n_types": len(types)}
    cutoff = np.quantile([freq[w] for w in types], 0.95)
    function = [w for w in types if freq[w] >= cutoff]
    content = [w for w in types if MINFREQ <= freq[w] <= CONTENT_MAX_FREQ]
    if len(function) < 5 or len(content) < 20:
        return {"insufficient": True, "n_function": len(function), "n_content": len(content)}
    fs = float(np.mean([sel[w] for w in function]))
    cs = float(np.mean([sel[w] for w in content]))
    return {"selectivity_function": round(fs, 3), "selectivity_content": round(cs, 3),
            "gap": round(cs - fs, 3), "n_function": len(function), "n_content": len(content)}


def run() -> dict:
    latin = (H4_OUT / "latin_vulgate.txt").read_text().split()
    german = (H4_OUT / "german_kraeuterbuch_dipl.txt").read_text().split()
    corpora = {
        "latin": _sub(latin), "german": _sub(german),                    # clean real
        "latin_shuffled": _sub(_shuffle(latin[:N_TOKENS], SEED)),        # clean null
        "latin_markov1": _markov1(latin[:N_TOKENS], SEED),               # contaminated
        "conlang_relex_latin": _sub(_paradigmatic_conlang(latin[:N_TOKENS], 0.8, SEED)),
        "vms_currierA": _sub(_vms_tokens("A")), "vms_currierB": _sub(_vms_tokens("B")),
    }
    stats = {k: _gap(v) for k, v in corpora.items()}

    real = [stats[c]["gap"] for c in ("latin", "german") if "gap" in stats[c]]
    null = [stats[c]["gap"] for c in ("latin_shuffled",) if "gap" in stats[c]]
    real_mean = round(sum(real) / len(real), 3) if real else None
    null_mean = round(sum(null) / len(null), 3) if null else None
    separation = round(real_mean - null_mean, 3) if (real_mean is not None and null_mean is not None) else None
    threshold = round((real_mean + null_mean) / 2, 3) if separation is not None else None
    calibration_ok = bool(separation is not None and separation >= 0.05)

    def classify(c):
        g = stats[c].get("gap")
        if g is None or not calibration_ok:
            return "inconclusive"
        return "language-like" if g >= threshold else "generator-like"

    va, vb = classify("vms_currierA"), classify("vms_currierB")
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E13b — function/content via collocational selectivity",
        "seed": SEED, "n_tokens": N_TOKENS,
        "stats": stats,
        "calibration": {"real_mean_gap": real_mean, "clean_null_mean_gap": null_mean,
                        "separation": separation, "threshold": threshold,
                        "calibration_ok": calibration_ok,
                        "contaminated_ref": {c: stats[c].get("gap")
                                             for c in ("latin_markov1", "conlang_relex_latin")}},
        "vms_currierA_class": va, "vms_currierB_class": vb,
        "ab_same_class": va == vb,
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e13b_function_content.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def _verdict(r: dict) -> tuple:
    c = r["calibration"]
    a, b = r["vms_currierA_class"], r["vms_currierB_class"]
    ga = r["stats"]["vms_currierA"].get("gap")
    gb = r["stats"]["vms_currierB"].get("gap")
    base = (f"Content-minus-function selectivity gap: real language {c['real_mean_gap']} "
            f"vs clean shuffle null {c['clean_null_mean_gap']} (separation "
            f"{c['separation']}); threshold {c['threshold']}. VMS-A gap={ga} ({a}), "
            f"VMS-B gap={gb} ({b}). Contaminated refs (preserve bigrams, expected "
            f"real-like): {c['contaminated_ref']}.")
    if not c["calibration_ok"]:
        return "D", (
            f"INCONCLUSIVE — even the redesigned selectivity gap does not cleanly "
            f"separate real language from the shuffle null (separation {c['separation']} "
            f"< 0.05), so no VMS function/content verdict is issued. {base} The "
            f"function/content probe appears to need sentence-segmented controls and a "
            f"purpose-built matched null; the current word-stream corpora do not support "
            f"it. (Harness-first: no calibration, no claim.)")
    if a == b == "language-like":
        return "C", (
            f"BOTH Currier systems show the content>function selectivity gap of real "
            f"language (content words carry specific collocates; function words do not), "
            f"a signature a full shuffle destroys. Reweights toward a language-derived "
            f"process in A AND B; does not separate them on this probe. {base} (Grammar "
            f"only; no meaning/translation claim — L7.)")
    if a != b:
        return "C", (
            f"A and B DIFFER on the content/function selectivity gap (A {a}, B {b}) — "
            f"evidence that the two Currier systems behave like different generative "
            f"processes. {base} (L7: grammar, not meaning.)")
    return "C", (
        f"NEITHER Currier system shows the real-language content/function selectivity "
        f"gap (A {a}, B {b}) — consistent with a generator-like process on this probe. "
        f"{base} (L7.)")


if __name__ == "__main__":
    out = run()
    print(f"{'corpus':22s} {'sel_func':>8s} {'sel_cont':>8s} {'gap':>7s}")
    for c, s in out["stats"].items():
        if s.get("insufficient"):
            print(f"{c:22s} insufficient")
            continue
        print(f"{c:22s} {s['selectivity_function']:>8} {s['selectivity_content']:>8} {s['gap']:>7}")
    cal = out["calibration"]
    print(f"\nreal={cal['real_mean_gap']} shuffle_null={cal['clean_null_mean_gap']} "
          f"separation={cal['separation']} ok={cal['calibration_ok']}")
    print(f"VMS-A={out['vms_currierA_class']} VMS-B={out['vms_currierB_class']}")
    print(f"grade {out['grade']}: {out['verdict'][:130]}...")
