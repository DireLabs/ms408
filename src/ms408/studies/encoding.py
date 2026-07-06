"""T2.4 — Encoding-hypothesis bracket (W2).

Each of the five encoding families from RESEARCH-PLAN §4 is expressed as a
generative model producing a word stream, and every stream is scored on the
same statistical profile as the real manuscript:

  1. verbose cipher      — Naibbe v2 on Pliny Latin (our H2 generator)
  2. null/self-citation  — Timm-Schinner (our H3 generator)
  3. abjad + anagram     — Hauer-Kondrak family: consonantal Hebrew (a real
                           abjad) with within-word letter anagramming
                           (alphagram, their canonical form)
  4. abbreviation        — Latin brevigraphy: seeded suspension/contraction
                           of Vulgate words (medieval scribal abbreviation)
  5. constructed language — Lingua-Ignota-style relexification: each Latin
                           word type mapped to an a-priori generated word
                           (CV(C) syllables, frequency-ranked lengths), so
                           plaintext word order survives under an invented
                           lexicon

Metrics are SUBSTITUTION-INVARIANT (unchanged under renaming glyphs), so no
arbitrary EVA rendering is needed: h1/h2 (Lindemann-Bowern, space included),
Zipf slope, law of abbreviation, type-token ratio, mean word length, ED1
network density, positional concentration, adjacent repetition, and the
Montemurro-Zanette word-order information (peak scale + value). Cross-alphabet
caveat: h1/h2 retain some inventory dependence; noted in the report.

Score: per metric, z-normalize across {five families + VMS}; a family's
distance = mean |z_family − z_VMS|. One parameterization per family (T1.4
variants pending) — this is a compatibility ordering, not a likelihood.

Usage:
    python -m ms408.studies.encoding
"""

from __future__ import annotations

import json
import math
import random
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..harness.naibbe import NaibbeCipher, NaibbeConfig, NaibbeTables
from ..harness.selfcitation import SelfCitationConfig, SelfCitationGenerator
from ..ivtff import IVTFFDocument
from ..mz import peak, scan_scales
from ..replication import _MZ_ORDER, _mz_section, paragraph_lines
from ..sources import path_for
from ..textstats import abbreviation_rho, lb_entropies, zipf_slope
from .morphology import ed1_network_stats, positional_concentration

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "studies"
REPORTS_DIR = ROOT / "reports"

SEED = 408
VOWELS = set("aeiou")


# ---------------------------------------------------------------------------
# Family generators (word streams)
# ---------------------------------------------------------------------------


def vms_stream() -> list:
    """ZL paragraph text in the MZ-reordered section order (matches T1.1)."""
    lines = paragraph_lines(IVTFFDocument.load(path_for("zl")))
    return [
        w
        for section in _MZ_ORDER
        for line in lines
        if _mz_section(line) == section
        for w in line.words
    ]


def family_verbose_cipher(n: int) -> list:
    tables = NaibbeTables.load()
    pliny = path_for("naibbe_pliny").read_text(encoding="utf-8").splitlines()
    result = NaibbeCipher(tables, NaibbeConfig(deck="52"), seed=SEED).encrypt_text(pliny)
    return [w for line in result.ciphertext_lines for w in line.split()][:n]


def family_selfcitation(n: int) -> list:
    generated = SelfCitationGenerator(
        SelfCitationConfig(lines_to_create=3800), seed=19
    ).generate()
    return [w for line in generated.lines for w in line][:n]


def family_abjad_anagram(n: int) -> list:
    words = (H4_OUT / "hebrew_mishneh_torah_consonantal.txt").read_text().split()[:n]
    return ["".join(sorted(w)) for w in words]


def family_abbreviation(n: int, seed: int = SEED) -> list:
    rng = random.Random(seed)
    out = []
    for w in (H4_OUT / "latin_vulgate.txt").read_text(encoding="utf-8").split()[:n]:
        if len(w) > 4 and rng.random() < 0.7:
            if rng.random() < 0.5:
                out.append(w[:3])  # suspension: trunk only
            else:
                skeleton = "".join(c for c in w[1:-1] if c not in VOWELS)
                out.append(w[0] + skeleton + w[-1])  # contraction
        else:
            out.append(w)
    return out


_CONSONANTS = "ptkschdz"
_CONLANG_VOWELS = "aioe"


def _conlang_word(rank: int, rng: random.Random) -> str:
    length_syllables = max(1, min(4, 1 + int(math.log2(rank + 2) / 2.5)))
    word = ""
    for _ in range(length_syllables):
        word += rng.choice(_CONSONANTS) + rng.choice(_CONLANG_VOWELS)
        if rng.random() < 0.3:
            word += rng.choice("nrls")
    return word


def family_conlang(n: int, seed: int = SEED) -> list:
    """Relexification: Latin token stream through an a-priori invented lexicon."""
    tokens = (H4_OUT / "latin_vulgate.txt").read_text(encoding="utf-8").split()[:n]
    from collections import Counter

    ranked = [w for w, _ in Counter(tokens).most_common()]
    rng = random.Random(seed)
    lexicon = {}
    used = set()
    for rank, word_type in enumerate(ranked):
        candidate = _conlang_word(rank, rng)
        while candidate in used:
            candidate = _conlang_word(rank, rng)
        lexicon[word_type] = candidate
        used.add(candidate)
    return [lexicon[t] for t in tokens]


# ---------------------------------------------------------------------------
# Profile and scoring
# ---------------------------------------------------------------------------

METRICS = (
    "h1", "h2", "mean_word_length", "type_token_ratio", "zipf_slope",
    "abbreviation_rho", "ed1_main_component", "position_entropy",
    "repetition_rate", "mz_peak_value", "mz_peak_scale",
)


def profile(words: list) -> dict:
    h1, h2 = lb_entropies(words)
    scan = scan_scales(words)
    scale, _, value = peak(scan)
    repeats = sum(1 for a, b in zip(words, words[1:]) if a == b)
    return {
        "tokens": len(words),
        "types": len(set(words)),
        "h1": round(h1, 4),
        "h2": round(h2, 4),
        "mean_word_length": round(sum(map(len, words)) / len(words), 3),
        "type_token_ratio": round(len(set(words)) / len(words), 4),
        "zipf_slope": round(zipf_slope(words), 4),
        "abbreviation_rho": round(abbreviation_rho(words), 4),
        "ed1_main_component": ed1_network_stats(words)["main_component_share"],
        "position_entropy": positional_concentration(words)[
            "mean_normalized_position_entropy"
        ],
        "repetition_rate": round(repeats / (len(words) - 1), 5),
        "mz_peak_value": round(value, 4),
        "mz_peak_scale": scale,
    }


def scorecard(profiles: dict) -> dict:
    """Mean |z_family − z_VMS| across METRICS (z over all corpora incl. VMS)."""
    scores = {}
    z: dict = {}
    for metric in METRICS:
        values = [profiles[name][metric] for name in profiles]
        mean = statistics.mean(values)
        sd = statistics.stdev(values) or 1.0
        for name in profiles:
            z.setdefault(name, {})[metric] = (profiles[name][metric] - mean) / sd
    for name in profiles:
        if name == "vms":
            continue
        scores[name] = {
            "distance": round(
                statistics.mean(
                    abs(z[name][m] - z["vms"][m]) for m in METRICS
                ), 3
            ),
            "worst_metrics": sorted(
                METRICS, key=lambda m: -abs(z[name][m] - z["vms"][m])
            )[:3],
        }
    return dict(sorted(scores.items(), key=lambda kv: kv[1]["distance"]))


def run() -> dict:
    vms = vms_stream()
    n = len(vms)
    streams = {
        "vms": vms,
        "verbose_cipher": family_verbose_cipher(n),
        "selfcitation": family_selfcitation(n),
        "abjad_anagram": family_abjad_anagram(n),
        "abbreviation": family_abbreviation(n),
        "conlang_relex": family_conlang(n),
    }
    profiles = {name: profile(words) for name, words in streams.items()}
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "seed": SEED,
        "note": "one parameterization per family; T1.4 variants pending. Metrics "
        "substitution-invariant except residual alphabet-inventory dependence in "
        "h1/h2.",
        "profiles": profiles,
        "scorecard": scorecard(profiles),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "encoding_bracket.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "study_encoding_bracket.md").write_text(_render_report(results))
    return results


def _render_report(results: dict) -> str:
    profiles = results["profiles"]
    scores = results["scorecard"]
    header = ("| corpus | h1 | h2 | mean len | TTR | zipf | abbrev ρ | ED1 comp. "
              "| pos. entropy | repeat | MZ peak | MZ scale |")
    rows = [
        f"| {name} | {p['h1']:.3f} | {p['h2']:.3f} | {p['mean_word_length']:.2f} "
        f"| {p['type_token_ratio']:.3f} | {p['zipf_slope']:.3f} "
        f"| {p['abbreviation_rho']:.3f} | {p['ed1_main_component']:.3f} "
        f"| {p['position_entropy']:.3f} | {p['repetition_rate']:.4f} "
        f"| {p['mz_peak_value']:.3f} | {p['mz_peak_scale']} |"
        for name, p in profiles.items()
    ]
    ranking = [
        f"{i + 1}. **{name}** — distance {s['distance']} "
        f"(largest deviations: {', '.join(s['worst_metrics'])})"
        for i, (name, s) in enumerate(scores.items())
    ]
    lines = [
        "# T2.4 Study Report — Encoding-Hypothesis Bracket (W2)",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.studies.encoding`; full numbers in "
        "`results/studies/encoding_bracket.json`.",
        "",
        "Five encoding families as generative models, scored against the real "
        f"manuscript on {profiles['vms']['tokens']:,} tokens each. "
        f"{results['note']}",
        "",
        header,
        "|" + "---|" * 12,
        *rows,
        "",
        "## Compatibility ordering (mean |z − z_VMS| across all metrics)",
        "",
        *ranking,
        "",
        "## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 review — L10)",
        "",
        _claims(results),
        "",
    ]
    return "\n".join(lines)


def _claims(results: dict) -> str:
    p = results["profiles"]
    scores = results["scorecard"]
    ordering = list(scores)
    failures = "; ".join(
        f"{name}: {', '.join(s['worst_metrics'][:2])}" for name, s in scores.items()
    )
    return "\n".join([
        f"1. **[C, candidate B pending T3.3]** No family reproduces the VMS's "
        f"signature combination: gibberish-like character structure (h2 "
        f"{p['vms']['h2']:.2f}, ED1 component {p['vms']['ed1_main_component']:.2f}) "
        f"TOGETHER WITH genuine word-order information at natural-language scale "
        f"(ΔI {p['vms']['mz_peak_value']:.3f} bits/word peaking at "
        f"{p['vms']['mz_peak_scale']} words). Compatibility ordering: "
        f"{' > '.join(ordering)}.",
        f"2. **[C, candidate B pending T3.3]** The homophonic verbose cipher "
        f"(Naibbe, as published) matches character structure almost perfectly (h2 "
        f"{p['verbose_cipher']['h2']:.2f}) but ERASES word-order information "
        f"(ΔI {p['verbose_cipher']['mz_peak_value']:.3f} vs VMS "
        f"{p['vms']['mz_peak_value']:.3f}): random homophone draws decouple "
        f"ciphertext types from plaintext types. The VMS's intact topic-scale "
        f"information is evidence AGAINST homophone-heavy verbose cipher as "
        f"parameterized — a homophone-poor variant is the key T1.4 sweep.",
        f"3. **[C, candidate B pending T3.3]** Self-citation is closest overall "
        f"(distance {scores['selfcitation']['distance']}) but OVERSHOOTS word-order "
        f"information at the wrong scale (ΔI "
        f"{p['selfcitation']['mz_peak_value']:.3f} peaking at "
        f"{p['selfcitation']['mz_peak_scale']} words vs VMS "
        f"{p['vms']['mz_peak_value']:.3f} at {p['vms']['mz_peak_scale']}) and runs "
        f"a too-small vocabulary (TTR {p['selfcitation']['type_token_ratio']:.3f} "
        f"vs {p['vms']['type_token_ratio']:.3f}): page-local copying produces "
        f"stronger, shorter-range clustering than the VMS actually shows.",
        f"4. **[C]** Decisive single-metric exclusions under these "
        f"parameterizations: abbreviation raises h2 to "
        f"{p['abbreviation']['h2']:.2f} (wrong direction, echoing "
        f"Lindemann-Bowern's diplomatic-text finding); anagrammed abjad lands at "
        f"h2 {p['abjad_anagram']['h2']:.2f}; the non-paradigmatic conlang has no "
        f"morphological network at all (ED1 "
        f"{p['conlang_relex']['ed1_main_component']:.3f} vs VMS "
        f"{p['vms']['ed1_main_component']:.3f}). Per-family worst metrics: "
        f"{failures}.",
        "5. **[D]** Family parameterizations are single points in their design "
        "spaces: a homophone-poor verbose cipher, a templatic/paradigmatic conlang "
        "(closer to the real Lingua Ignota), and mixed abbreviation intensities "
        "are the obvious sweeps for the T1.4 variant matrix before this bracket "
        "is treated as settled.",
    ])


if __name__ == "__main__":
    study = run()
    for name, entry in study["scorecard"].items():
        print(f"{name:16s} distance={entry['distance']:.3f} "
              f"worst={entry['worst_metrics']}")
    vms_profile = study["profiles"]["vms"]
    print(f"{'vms':16s} h2={vms_profile['h2']} mz={vms_profile['mz_peak_value']}")
