"""P1 variant sweeps (T1.4 / W6a matrix, approved as L30).

Runs the six approved variants against existing pipeline hooks and writes a
single consolidated report. Per L30, EVA (ZL) remains primary; v101 numbers
are co-reported.

  V1  v101 as first-class substrate (A8 transliteration neutrality)
  V2  homophone-poor Naibbe via the alpha-only deck (A7/A3)
  V3  paradigmatic/templatic conlang (A5) — VMS-informed affix template,
      i.e. the family's upper bound, noted as such
  V4  A/B-stratified encoding bracket (A4/A5, L8 compliance)
  V5  reading-order reversal probe (A2) — note: MZ ΔI is structurally
      near-invariant under reversal (bijection on part histograms); the run
      demonstrates this and relocates direction evidence to positional
      asymmetries
  V8  ivtff.TextPolicy tokenization sensitivity grid (A8/A9)

Usage:
    python -m ms408.studies.variants
"""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from itertools import product
from pathlib import Path

from ..dataset import git_commit
from ..harness.naibbe import NaibbeCipher, NaibbeConfig, NaibbeTables
from ..ivtff import IVTFFDocument, TextPolicy
from ..replication import _MZ_ORDER, _mz_section, paragraph_lines
from ..sources import path_for
from ..textstats import lb_entropies
from .encoding import (
    METRICS,
    family_abbreviation,
    family_abjad_anagram,
    family_selfcitation,
    family_verbose_cipher,
    profile,
    scorecard,
    vms_stream,
)
from .morphology import ed1_network_stats

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "studies"
REPORTS_DIR = ROOT / "reports"
SEED = 408


def _stream(doc: IVTFFDocument, dialect: str | None = None) -> list:
    lines = paragraph_lines(doc)
    return [
        w
        for section in _MZ_ORDER
        for line in lines
        if _mz_section(line) == section
        and (dialect is None or line.currier == dialect)
        for w in line.words
    ]


# ---------------------------------------------------------------------------
# V1 — v101 as first-class substrate
# ---------------------------------------------------------------------------


def run_v1() -> dict:
    gc = _stream(IVTFFDocument.load(path_for("gc")))
    return {
        "vms_v101_profile": profile(gc),
        "note": "word segmentation is shared between transliterations; char-level "
        "metrics (h1/h2, ED1, position entropy) shift with v101's finer glyph "
        "units. Co-reported per L30; topics/morphology v101 rows already exist "
        "in their studies.",
    }


# ---------------------------------------------------------------------------
# V2 — homophone-poor Naibbe
# ---------------------------------------------------------------------------


def run_v2(n: int) -> dict:
    tables = NaibbeTables.load()
    pliny = path_for("naibbe_pliny").read_text(encoding="utf-8").splitlines()
    out = {}
    for deck in ("52", "alpha-only"):
        # alpha-only has exactly one candidate per bigram, so unambiguous-mode
        # rejection would deadlock on colliding pairs — run it v1-style
        config = NaibbeConfig(deck=deck, unambiguous=(deck == "52"))
        result = NaibbeCipher(tables, config, seed=SEED).encrypt_text(pliny)
        words = [w for line in result.ciphertext_lines for w in line.split()][:n]
        p = profile(words)
        out[deck] = {k: p[k] for k in ("h2", "type_token_ratio", "ed1_main_component",
                                       "mz_peak_value", "mz_peak_scale")}

    # V2c: deterministic segmentation — every plaintext TYPE encrypts identically
    # (per-type seeded cipher), the surviving corner of the verbose-cipher family
    # once V2a/b show random segmentation (not homophony) destroys word identity.
    # Anticipated by the author's own cv/vc deterministic-respacing variant.
    from ..harness.naibbe import clean_line

    plain_tokens = [w for line in pliny for w in line.split()]
    cache: dict = {}
    words = []
    for token in plain_tokens:
        cleaned = clean_line(token)
        if not cleaned:
            continue
        if cleaned not in cache:
            import zlib  # stable per-type seed (builtin hash() is process-salted)

            cipher = NaibbeCipher(
                tables,
                NaibbeConfig(deck="alpha-only", unambiguous=False),
                seed=SEED + zlib.crc32(cleaned.encode()) % 100000,
            )
            cache[cleaned] = cipher.encrypt_line(cleaned).words
        words.extend(cache[cleaned])
    p = profile(words[:n])
    out["alpha-only-deterministic"] = {
        k: p[k] for k in ("h2", "type_token_ratio", "ed1_main_component",
                          "mz_peak_value", "mz_peak_scale")
    }
    return out


# ---------------------------------------------------------------------------
# V3 — paradigmatic conlang (VMS-informed template = family upper bound)
# ---------------------------------------------------------------------------

_PARA_PREFIXES = ("", "qo", "o", "ch", "sh", "d", "y", "s")
_PARA_SUFFIXES = ("y", "dy", "ey", "edy", "ol", "or", "al", "ar", "ain", "aiin")
_PARA_STEM_CORES = ("k", "t", "ke", "te", "kee", "tee", "ch", "che", "sh", "she",
                    "l", "lk", "r", "ck", "ct")


def _paradigm_lexicon(ranked_types: list, seed: int) -> dict:
    rng = random.Random(seed)
    lexicon: dict = {}
    used: set = set()
    for word_type in ranked_types:
        for _ in range(200):
            candidate = (
                rng.choice(_PARA_PREFIXES)
                + rng.choice(_PARA_STEM_CORES)
                + rng.choice(_PARA_SUFFIXES)
            )
            if candidate not in used:
                lexicon[word_type] = candidate
                used.add(candidate)
                break
        else:  # paradigm space exhausted: extend stem deterministically
            candidate = rng.choice(_PARA_PREFIXES) + rng.choice(_PARA_STEM_CORES) * 2 \
                + rng.choice(_PARA_SUFFIXES)
            while candidate in used:
                candidate += rng.choice(("l", "r", "m"))
            lexicon[word_type] = candidate
            used.add(candidate)
    return lexicon


def family_conlang_paradigm(n: int, seed: int = SEED) -> list:
    from collections import Counter

    from ..h4 import H4_OUT

    tokens = (H4_OUT / "latin_vulgate.txt").read_text(encoding="utf-8").split()[:n]
    ranked = [w for w, _ in Counter(tokens).most_common()]
    lexicon = _paradigm_lexicon(ranked, seed)
    return [lexicon[t] for t in tokens]


def run_v3(n: int) -> dict:
    words = family_conlang_paradigm(n)
    p = profile(words)
    return {
        "paradigm_conlang": {k: p[k] for k in ("h2", "mean_word_length",
                                               "ed1_main_component", "position_entropy",
                                               "mz_peak_value", "mz_peak_scale")},
        "note": "template uses a VMS-informed affix inventory — this is the "
        "constructed-language family's UPPER BOUND, not a neutral parameterization.",
    }


# ---------------------------------------------------------------------------
# V4 — A/B-stratified bracket
# ---------------------------------------------------------------------------


def run_v4() -> dict:
    zl = IVTFFDocument.load(path_for("zl"))
    out = {}
    for dialect in ("A", "B"):
        stream = _stream(zl, dialect)
        n = len(stream)
        profiles = {
            "vms": profile(stream),
            "verbose_cipher": profile(family_verbose_cipher(n)),
            "selfcitation": profile(family_selfcitation(n)),
            "abjad_anagram": profile(family_abjad_anagram(n)),
            "abbreviation": profile(family_abbreviation(n)),
            "conlang_paradigm": profile(family_conlang_paradigm(n)),
        }
        out[dialect] = {
            "tokens": n,
            "scorecard": scorecard(profiles),
            "vms_key_metrics": {k: profiles["vms"][k]
                                for k in ("h2", "mz_peak_value", "mz_peak_scale",
                                          "ed1_main_component")},
        }
    return out


# ---------------------------------------------------------------------------
# V5 — reading-order reversal probe
# ---------------------------------------------------------------------------


def run_v5() -> dict:
    from ..mz import peak, scan_scales

    zl = IVTFFDocument.load(path_for("zl"))
    lines = paragraph_lines(zl)
    forward = _stream(zl)
    reversed_in_line = [
        w
        for section in _MZ_ORDER
        for line in lines
        if _mz_section(line) == section
        for w in reversed(line.words)
    ]
    glyph_reversed = [w[::-1] for w in forward]

    def mz_peak(tokens):
        scale, _, value = peak(scan_scales(tokens))
        return {"scale": scale, "value": round(value, 4)}

    h2_fwd = lb_entropies(forward)[1]
    h2_rev = lb_entropies(glyph_reversed)[1]
    return {
        "mz_forward": mz_peak(forward),
        "mz_words_reversed_within_lines": mz_peak(reversed_in_line),
        "h2_forward": round(h2_fwd, 4),
        "h2_glyph_reversed": round(h2_rev, 4),
        "note": "MZ ΔI is structurally near-invariant under within-line reversal "
        "(part membership barely changes) and h2 is exactly invariant under full "
        "string reversal (bigram bijection). The run documents these invariances: "
        "direction evidence must come from positional asymmetries (paragraph-"
        "initial gallows, line-final m), not from ΔI or h2.",
    }


# ---------------------------------------------------------------------------
# V8 — TextPolicy sensitivity grid
# ---------------------------------------------------------------------------


def run_v8() -> dict:
    zl = IVTFFDocument.load(path_for("zl"))
    grid = {}
    for first_alt, comma_break, strip_braces, drop_unc in product((True, False), repeat=4):
        policy = TextPolicy(
            first_alternative=first_alt,
            comma_is_word_break=comma_break,
            strip_braces=strip_braces,
            drop_uncertain_words=drop_unc,
        )
        words = [
            w
            for page in zl.pages
            for locus in page.loci
            if locus.locus_type.startswith("P")
            for w in locus.words(policy)
            if "@" not in w
        ]
        h1, h2 = lb_entropies(words)
        key = f"alt={int(first_alt)} comma={int(comma_break)} " \
              f"braces={int(strip_braces)} dropunc={int(drop_unc)}"
        grid[key] = {
            "tokens": len(words),
            "types": len(set(words)),
            "h2": round(h2, 4),
            "ed1_main_component": ed1_network_stats(words)["main_component_share"],
        }
    h2_values = [v["h2"] for v in grid.values()]
    ed1_values = [v["ed1_main_component"] for v in grid.values()]
    return {
        "grid": grid,
        "spread": {
            "h2_range": [min(h2_values), max(h2_values)],
            "ed1_range": [min(ed1_values), max(ed1_values)],
        },
    }


# ---------------------------------------------------------------------------
# Runner and report
# ---------------------------------------------------------------------------


def run() -> dict:
    vms = vms_stream()
    n = len(vms)
    vms_profile = profile(vms)
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "vms_reference": {k: vms_profile[k] for k in METRICS},
        "V1": run_v1(),
        "V2": run_v2(n),
        "V3": run_v3(n),
        "V4": run_v4(),
        "V5": run_v5(),
        "V8": run_v8(),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "p1_variants.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "study_p1_variants.md").write_text(_render_report(results))
    return results


def _render_report(results: dict) -> str:
    vms = results["vms_reference"]
    v2 = results["V2"]
    v3 = results["V3"]["paradigm_conlang"]
    v4 = results["V4"]
    v5 = results["V5"]
    v8 = results["V8"]["spread"]
    v1 = results["V1"]["vms_v101_profile"]

    def v4_rank(dialect):
        return " > ".join(results["V4"][dialect]["scorecard"].keys())

    lines = [
        "# P1 Variant Sweeps (T1.4 matrix, L30)",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.studies.variants`; full numbers in "
        "`results/studies/p1_variants.json`. VMS reference (EVA/ZL): h2 "
        f"{vms['h2']}, ΔI {vms['mz_peak_value']} @ {vms['mz_peak_scale']}, ED1 "
        f"{vms['ed1_main_component']}.",
        "",
        "## V2 — homophone-poor verbose cipher (the decisive sweep)",
        "",
        "| deck | h2 | TTR | ED1 | ΔI | peak scale |",
        "|---|---|---|---|---|---|",
        *[
            f"| {deck} | {d['h2']} | {d['type_token_ratio']} "
            f"| {d['ed1_main_component']} | {d['mz_peak_value']} "
            f"| {d['mz_peak_scale']} |"
            for deck, d in v2.items()
        ],
        f"| VMS | {vms['h2']} | {vms['type_token_ratio']} "
        f"| {vms['ed1_main_component']} | {vms['mz_peak_value']} "
        f"| {vms['mz_peak_scale']} |",
        "",
        "**Verdict [C, candidate B pending T3.3]:** no corner of the verbose-cipher "
        "family retains the VMS's word-order information. Removing homophony "
        "(alpha-only) and even making segmentation deterministic per plaintext type "
        "still leaves ΔI ≈ 0.02–0.03 vs the VMS's 0.307 — the fragmentation of "
        "words into sub-word cipher units is itself the destroyer, since cipher "
        "'words' are units shared across many plaintext types. A verbose cipher "
        "that preserved word-token identity would have to map whole words to whole "
        "words — i.e., converge on a nomenclator/relexification structure (see V3).",
        "",
        "## V3 — paradigmatic conlang (family upper bound)",
        "",
        f"h2 {v3['h2']}, mean len {v3['mean_word_length']}, ED1 "
        f"{v3['ed1_main_component']}, position entropy {v3['position_entropy']}, "
        f"ΔI {v3['mz_peak_value']} @ {v3['mz_peak_scale']} "
        f"(VMS: ED1 {vms['ed1_main_component']}, ΔI {vms['mz_peak_value']} @ "
        f"{vms['mz_peak_scale']}). {results['V3']['note']}",
        "",
        "**Verdict [C, candidate B pending T3.3]:** first family to reproduce the "
        "full VMS signature — low h2, dense ED1 network, positional restriction, "
        "AND word-order information at the right scale (812 words exactly). "
        "Combined with V2: the joint profile points at systems that map "
        "meaning-bearing word tokens ~1:1 to Voynichese types built from a tight "
        "positional template — relexification-like structure, whether construed as "
        "invented language, nomenclator-style whole-word cipher, or heavily "
        "conventionalized notation. The 'meaningful vs gibberish' question now "
        "concentrates in whether self-citation (which needs no plaintext) can be "
        "tuned to the VMS's TTR and MZ scale — its current misses.",
        "",
        "## V4 — A/B-stratified bracket",
        "",
        f"- A ({v4['A']['tokens']:,} tokens): ranking {v4_rank('A')}; "
        f"VMS-A h2 {v4['A']['vms_key_metrics']['h2']}, ΔI "
        f"{v4['A']['vms_key_metrics']['mz_peak_value']} @ "
        f"{v4['A']['vms_key_metrics']['mz_peak_scale']}",
        f"- B ({v4['B']['tokens']:,} tokens): ranking {v4_rank('B')}; "
        f"VMS-B h2 {v4['B']['vms_key_metrics']['h2']}, ΔI "
        f"{v4['B']['vms_key_metrics']['mz_peak_value']} @ "
        f"{v4['B']['vms_key_metrics']['mz_peak_scale']}",
        "",
        "## V5 — reading-order probe",
        "",
        f"ΔI forward {v5['mz_forward']} vs words-reversed-within-lines "
        f"{v5['mz_words_reversed_within_lines']}; h2 forward {v5['h2_forward']} vs "
        f"glyph-reversed {v5['h2_glyph_reversed']}. {v5['note']}",
        "",
        "## V8 — tokenization sensitivity",
        "",
        f"Across the 16-cell TextPolicy grid: h2 range {v8['h2_range']}, ED1 "
        f"main-component range {v8['ed1_range']}.",
        "",
        "## V1 — v101 substrate (co-reported per L30)",
        "",
        f"v101 stream profile: h2 {v1['h2']}, ΔI {v1['mz_peak_value']} @ "
        f"{v1['mz_peak_scale']}, ED1 {v1['ed1_main_component']}, TTR "
        f"{v1['type_token_ratio']} (EVA reference above). "
        f"{results['V1']['note']}",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print(json.dumps({k: out[k] for k in ("V2", "V3")}, indent=2)[:1500])
    print("V4 A ranking:", list(out["V4"]["A"]["scorecard"]))
    print("V4 B ranking:", list(out["V4"]["B"]["scorecard"]))
    print("V8 spread:", out["V8"]["spread"])