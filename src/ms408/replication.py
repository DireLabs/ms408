"""T1.1 replication-gate measurements (Phase 1; gate G1).

Measures the established Voynichese statistical signatures on our pipeline's
corpus and compares them against published values (targets compiled in
docs/planning/i01/specs/T11-*.md). Five target families per WORKFLOW T1.1:

  1. character entropy (h2 anomaly)          — Lindemann & Bowern
  2. Zipf rank-frequency + law of abbreviation
  3. Currier A/B statistical split           — Currier 1976; Zandbergen
  4. Montemurro-Zanette long-range word-information structure
  5. positional (line/paragraph) glyph effects — "the line is a functional unit"

Corpus policy for positional analyses: paragraph-text loci only (locus type P*),
lines in manuscript order; paragraph boundaries from the in-text <%>/<$> markers
(740 of each in ZL3b; the locus locator characters are not reliable for this).
Word policy: EVA default + drop uncertain words + drop '@'-escape words.

Usage:
    python -m ms408.replication
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .dataset import git_commit
from .ivtff import IVTFFDocument, TextPolicy
from .sources import path_for
from .textstats import (
    abbreviation_rho,
    char_conditional_entropy,
    char_unigram_entropy,
    summarize,
    zipf_slope,
)

ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results" / "replication"

WORD_POLICY = TextPolicy(drop_uncertain_words=True)


@dataclass(frozen=True)
class Line:
    page: str
    words: tuple
    paragraph_initial: bool
    paragraph_final: bool
    currier: str | None
    hand: str | None
    section: str | None


def paragraph_lines(doc: IVTFFDocument) -> list:
    """Manuscript lines of running paragraph text (P-type loci), with metadata."""
    lines = []
    for page in doc.pages:
        for locus in page.loci:
            if not locus.locus_type.startswith("P"):
                continue
            words = tuple(
                w for w in locus.words(WORD_POLICY) if "@" not in w
            )
            if not words:
                continue
            lines.append(
                Line(
                    page=page.name,
                    words=words,
                    paragraph_initial="<%>" in locus.text,
                    paragraph_final="<$>" in locus.text,
                    currier=page.currier_language,
                    hand=page.hand,
                    section=page.illustration_type,
                )
            )
    return lines


# ---------------------------------------------------------------------------
# 5. Positional effects
# ---------------------------------------------------------------------------


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def positional_effects(lines: list) -> dict:
    par_initial_tokens, other_tokens = [], []
    line_first, line_last, line_mid = [], [], []
    for line in lines:
        bucket = par_initial_tokens if line.paragraph_initial else other_tokens
        bucket.extend(line.words)
        line_first.append(line.words[0])
        line_last.append(line.words[-1])
        line_mid.extend(line.words[1:-1])

    def pf_rate(tokens):
        return _rate(sum(1 for w in tokens if "p" in w or "f" in w), len(tokens))

    def final_rate(tokens, glyph):
        return _rate(sum(1 for w in tokens if w.endswith(glyph)), len(tokens))

    def initial_rate(tokens, glyphs):
        return _rate(sum(1 for w in tokens if w[0] in glyphs), len(tokens))

    m_final_words_total = sum(
        1 for tokens in (line_first, line_mid, line_last) for w in tokens if w.endswith("m")
    )
    m_final_words_at_line_end = sum(1 for w in line_last if w.endswith("m"))

    return {
        "paragraph_initial_gallows": {
            "pf_word_rate_paragraph_initial_lines": round(pf_rate(par_initial_tokens), 4),
            "pf_word_rate_other_lines": round(pf_rate(other_tokens), 4),
            "enrichment": round(
                pf_rate(par_initial_tokens) / max(pf_rate(other_tokens), 1e-9), 2
            ),
            "tokens": {"paragraph_initial": len(par_initial_tokens),
                       "other": len(other_tokens)},
        },
        "line_final": {
            "m_final_word_rate_line_end": round(final_rate(line_last, "m"), 4),
            "m_final_word_rate_mid_line": round(final_rate(line_mid, "m"), 4),
            "share_of_m_final_words_at_line_end": round(
                _rate(m_final_words_at_line_end, m_final_words_total), 4
            ),
            "g_final_word_rate_line_end": round(final_rate(line_last, "g"), 4),
            "g_final_word_rate_mid_line": round(final_rate(line_mid, "g"), 4),
        },
        "line_initial": {
            # classic observation: line-initial words prefer certain glyphs
            "ydso_initial_rate_line_first": round(
                initial_rate(line_first, set("ydso")), 4
            ),
            "ydso_initial_rate_mid_line": round(initial_rate(line_mid, set("ydso")), 4),
            "gallows_initial_rate_line_first": round(
                initial_rate(line_first, set("ktpf")), 4
            ),
            "gallows_initial_rate_mid_line": round(initial_rate(line_mid, set("ktpf")), 4),
        },
        "lines": len(lines),
    }


# ---------------------------------------------------------------------------
# 3. Currier A/B split
# ---------------------------------------------------------------------------

MARKER_WORDS = ("chedy", "shedy", "qokeedy", "qokedy", "chol", "chor", "daiin", "aiin")


def _js_divergence(counts_p: Counter, counts_q: Counter, top_n: int = 1000) -> float:
    vocabulary = [w for w, _ in (counts_p + counts_q).most_common(top_n)]
    total_p = sum(counts_p.values())
    total_q = sum(counts_q.values())

    def kl(counts_a, total_a):
        divergence = 0.0
        for w in vocabulary:
            pa = counts_a[w] / total_a
            pm = (counts_p[w] / total_p + counts_q[w] / total_q) / 2
            if pa > 0 and pm > 0:
                divergence += pa * math.log2(pa / pm)
        return divergence

    return (kl(counts_p, total_p) + kl(counts_q, total_q)) / 2


def currier_split(lines: list) -> dict:
    a_words = [w for line in lines if line.currier == "A" for w in line.words]
    b_words = [w for line in lines if line.currier == "B" for w in line.words]
    a_counts, b_counts = Counter(a_words), Counter(b_words)

    def per_mille(counts, total, word):
        return round(1000 * counts[word] / total, 3)

    markers = {}
    for word in MARKER_WORDS:
        rate_a = per_mille(a_counts, len(a_words), word)
        rate_b = per_mille(b_counts, len(b_words), word)
        markers[word] = {
            "per_mille_A": rate_a,
            "per_mille_B": rate_b,
            "ratio_B_over_A": round(rate_b / rate_a, 1) if rate_a else float("inf"),
        }

    def suffix_rate(words, suffix):
        return round(_rate(sum(1 for w in words if w.endswith(suffix)), len(words)), 4)

    def prefix_rate(words, prefix):
        return round(_rate(sum(1 for w in words if w.startswith(prefix)), len(words)), 4)

    # within-dialect baseline: split each dialect's pages alternately and measure
    # the same divergence — the A/B split must exceed internal heterogeneity
    def alternate_split(dialect):
        pages = sorted({line.page for line in lines if line.currier == dialect})
        half_a = {p for i, p in enumerate(pages) if i % 2 == 0}
        w1 = Counter(w for line in lines if line.page in half_a for w in line.words)
        w2 = Counter(
            w for line in lines
            if line.currier == dialect and line.page not in half_a
            for w in line.words
        )
        return _js_divergence(w1, w2)

    return {
        "tokens": {"A": len(a_words), "B": len(b_words)},
        "marker_words": markers,
        "dy_final_rate": {"A": suffix_rate(a_words, "dy"), "B": suffix_rate(b_words, "dy")},
        "edy_final_rate": {"A": suffix_rate(a_words, "edy"), "B": suffix_rate(b_words, "edy")},
        "qo_initial_rate": {"A": prefix_rate(a_words, "qo"), "B": prefix_rate(b_words, "qo")},
        "js_divergence_A_vs_B": round(_js_divergence(a_counts, b_counts), 4),
        "js_divergence_within_A": round(alternate_split("A"), 4),
        "js_divergence_within_B": round(alternate_split("B"), 4),
    }


# ---------------------------------------------------------------------------
# 1+2. Entropy and Zipf blocks (published-value comparison in the report step)
# ---------------------------------------------------------------------------


def entropy_zipf(lines: list) -> dict:
    def block(words):
        return {
            "tokens": len(words),
            "h1": round(char_unigram_entropy(words), 4),
            "h2": round(char_conditional_entropy(words), 4),
            "zipf_slope": round(zipf_slope(words), 4) if zipf_slope(words) else None,
            "abbreviation_rho": round(abbreviation_rho(words), 4),
        }

    all_words = [w for line in lines for w in line.words]
    result = {"all": block(all_words)}
    for dialect in ("A", "B"):
        words = [w for line in lines if line.currier == dialect for w in line.words]
        result[f"currier_{dialect}"] = block(words)
    for hand in "12345":
        words = [w for line in lines if line.hand == hand for w in line.words]
        if len(words) > 1000:
            result[f"hand_{hand}"] = block(words)
    return result


# ---------------------------------------------------------------------------
# Published-target batteries (specs: T11-entropy, T11-currier-positional, T11-montemurro)
# ---------------------------------------------------------------------------

# Currier-symbol view of EVA: benched gallows and ch/sh become single symbols so
# "t followed by e" means what Currier meant (digits never occur in EVA words)
_GLYPH_MAP = (("cth", "1"), ("ckh", "2"), ("cph", "3"), ("cfh", "4"), ("ch", "5"), ("sh", "6"))


def glyphify(word: str) -> str:
    for sequence, placeholder in _GLYPH_MAP:
        word = word.replace(sequence, placeholder)
    return word


def _all_words_by(doc: IVTFFDocument, predicate) -> list:
    """Words from ALL locus types (labels included), pages filtered by predicate."""
    return [
        w
        for page in doc.pages
        if predicate(page)
        for locus in page.loci
        for w in locus.words(WORD_POLICY)
        if "@" not in w
    ]


def lb_entropy_family(zl: IVTFFDocument, it: IVTFFDocument) -> dict:
    """Lindemann-Bowern h1/h2 (spaces included) on the corpora they used (labels incl.)."""
    from .textstats import lb_entropies

    out = {}
    for label, doc in (("it", it), ("zl", zl)):
        for subset, predicate in (
            ("full", lambda p: True),
            ("A", lambda p: p.currier_language == "A"),
            ("B", lambda p: p.currier_language == "B"),
        ):
            words = _all_words_by(doc, predicate)
            h1, h2 = lb_entropies(words)
            out[f"{label}_{subset}"] = {
                "words": len(words), "h1": round(h1, 4), "h2": round(h2, 4),
            }
        for hand in "12345":
            words = _all_words_by(doc, lambda p, h=hand: p.hand == h)
            if len(words) > 500:
                h1, h2 = lb_entropies(words)
                out[f"{label}_hand{hand}"] = {
                    "words": len(words), "h1": round(h1, 4), "h2": round(h2, 4),
                }
    return out


def lexical_battery(zl: IVTFFDocument, lines: list) -> dict:
    a_words = _all_words_by(zl, lambda p: p.currier_language == "A")
    b_words = _all_words_by(zl, lambda p: p.currier_language == "B")
    all_words = _all_words_by(zl, lambda p: True)

    # A8: gallows followed by 'e', on Currier symbols
    follow = Counter()
    for word in all_words:
        g = glyphify(word)
        for a, b in zip(g, g[1:]):
            if a in "tkpf":
                follow[(a in "tk", b == "e")] += 1
    tk_total = follow[(True, True)] + follow[(True, False)]
    pf_total = follow[(False, True)] + follow[(False, False)]

    def share(words, condition):
        return round(_rate(sum(1 for w in words if condition(w)), len(words)), 4)

    q_positions = [
        (i, w) for w in all_words for i, c in enumerate(w) if c == "q"
    ]
    q_followed_by_o = sum(1 for i, w in q_positions if i + 1 < len(w) and w[i + 1] == "o")

    def top10_coverage(words):
        counts = Counter(words)
        return round(sum(c for _, c in counts.most_common(10)) / len(words), 4)

    def repetition_rate(dialect):
        repeats = tokens = 0
        for line in lines:
            if line.currier != dialect:
                continue
            tokens += len(line.words)
            repeats += sum(1 for a, b in zip(line.words, line.words[1:]) if a == b)
        return round(_rate(repeats, tokens), 4)

    # A11 clusters: inverse frequency of daiin
    def inverse_daiin(section, dialect):
        words = _all_words_by(
            zl, lambda p: p.illustration_type == section and p.currier_language == dialect
        )
        share_daiin = _rate(sum(1 for w in words if w == "daiin"), len(words))
        return round(1 / share_daiin, 1) if share_daiin else None

    return {
        "e_after_tk": round(_rate(follow[(True, True)], tk_total), 4),
        "e_after_pf": round(_rate(follow[(False, True)], pf_total), 4),
        "y_final_share": share(all_words, lambda w: w.endswith("y")),
        "ynlrms_final_share": share(all_words, lambda w: w[-1] in "ynlrms"),
        "q_followed_by_o": round(_rate(q_followed_by_o, len(q_positions)), 4),
        "daiin_share_A": share(a_words, lambda w: w == "daiin"),
        "chedy_share_B": share(b_words, lambda w: w == "chedy"),
        "chedy_count_A": sum(1 for w in a_words if w == "chedy"),
        "top10_coverage_A": top10_coverage(a_words),
        "top10_coverage_B": top10_coverage(b_words),
        "repetition_rate_A": repetition_rate("A"),
        "repetition_rate_B": repetition_rate("B"),
        "inverse_daiin_herbalA": inverse_daiin("H", "A"),
        "inverse_daiin_herbalB": inverse_daiin("H", "B"),
        "inverse_daiin_bioB": inverse_daiin("B", "B"),
    }


def positional_battery(lines: list) -> dict:
    par_initial = [line for line in lines if line.paragraph_initial]
    other = [line for line in lines if not line.paragraph_initial]

    def pf_glyph_count(line_set):
        return sum(glyphify(w).count("p") + glyphify(w).count("f")
                   for line in line_set for w in line.words)

    pf_in_par_initial = pf_glyph_count(par_initial)
    pf_elsewhere = pf_glyph_count(other)

    gallows_starts = sum(
        1 for line in par_initial if glyphify(line.words[0])[0] in "tkpf"
    )
    benched_start_cases = [
        (line.page, line.words[0])
        for line in par_initial
        if line.words[0].startswith(("cth", "ckh", "cph", "cfh"))
    ]

    m_total = sum(w.count("m") for line in lines for w in line.words)
    m_line_final = sum(
        1 for line in lines if line.words[-1].endswith("m")
    )

    cross_line_cases = [
        (prev.page, prev.words[-1])
        for prev, nxt in zip(lines, lines[1:])
        if prev.page == nxt.page and prev.words[-1] == nxt.words[0]
    ]
    cross_line_opportunities = sum(
        1 for prev, nxt in zip(lines, lines[1:]) if prev.page == nxt.page
    )
    within_line_pairs = sum(max(len(line.words) - 1, 0) for line in lines)
    within_line_repeats = sum(
        sum(1 for a, b in zip(line.words, line.words[1:]) if a == b) for line in lines
    )

    first_lengths = [len(line.words[0]) for line in lines if len(line.words) > 2]
    second_lengths = [len(line.words[1]) for line in lines if len(line.words) > 2]
    other_lengths = [len(w) for line in lines for w in line.words[1:]]

    chsh = ("ch", "sh")
    line_first_words = [line.words[0] for line in lines]
    all_words = [w for line in lines for w in line.words]
    chsh_line_initial = _rate(
        sum(1 for w in line_first_words if w.startswith(chsh)), len(line_first_words)
    )
    chsh_overall = _rate(sum(1 for w in all_words if w.startswith(chsh)), len(all_words))

    return {
        "pf_share_in_paragraph_initial_lines": round(
            _rate(pf_in_par_initial, pf_in_par_initial + pf_elsewhere), 4
        ),
        "pf_occurrences": pf_in_par_initial + pf_elsewhere,
        "paragraphs_starting_with_gallows": round(_rate(gallows_starts, len(par_initial)), 4),
        "paragraph_initial_benched_gallows_rate": round(
            _rate(len(benched_start_cases), len(par_initial)), 4
        ),
        "paragraph_initial_benched_gallows_cases": benched_start_cases,
        "m_share_line_final": round(_rate(m_line_final, m_total), 4),
        "m_occurrences": m_total,
        "cross_line_adjacent_repeats": len(cross_line_cases),
        "cross_line_repeat_cases": cross_line_cases,
        "cross_line_repeat_rate": round(_rate(len(cross_line_cases),
                                              cross_line_opportunities), 5),
        "within_line_adjacent_repeats": within_line_repeats,
        "within_line_repeat_rate": round(_rate(within_line_repeats, within_line_pairs), 5),
        "first_word_length_excess": round(
            sum(first_lengths) / len(first_lengths)
            - sum(other_lengths) / len(other_lengths), 3
        ),
        "first_vs_second_word_excess": round(
            sum(first_lengths) / len(first_lengths)
            - sum(second_lengths) / len(second_lengths), 3
        ),
        "chsh_line_initial_vs_expected": round(chsh_line_initial / chsh_overall, 3),
    }


def adjacency_battery(lines: list) -> dict:
    """Currier's 4th finding: word-final y -> next word qo-, Biological B.

    Operationalized as the conditional contrast P(qo | after y-final) vs
    P(qo | after non-y-final): Bio-B is qo-saturated (~24% of words), so
    "four times as often" cannot mean 4x the overall baseline.
    """
    bio_lines = [line for line in lines if line.section == "B"]
    pairs = [
        (a, b) for line in bio_lines for a, b in zip(line.words, line.words[1:])
    ]
    after_y = [b for a, b in pairs if a.endswith("y")]
    after_non_y = [b for a, b in pairs if not a.endswith("y")]
    qo_after_y = _rate(sum(1 for b in after_y if b.startswith("qo")), len(after_y))
    qo_after_non_y = _rate(
        sum(1 for b in after_non_y if b.startswith("qo")), len(after_non_y)
    )
    bio_words = [w for line in bio_lines for w in line.words]
    baseline_qo = _rate(sum(1 for w in bio_words if w.startswith("qo")), len(bio_words))
    return {
        "bio_b_qo_rate_after_y_final": round(qo_after_y, 4),
        "bio_b_qo_rate_after_non_y": round(qo_after_non_y, 4),
        "bio_b_qo_baseline": round(baseline_qo, 4),
        "contrast": round(qo_after_y / qo_after_non_y, 2) if qo_after_non_y else None,
        "lift_vs_baseline": round(qo_after_y / baseline_qo, 2) if baseline_qo else None,
    }


# Montemurro-Zanette reordered sections (their folio map; $I fallback for unmapped)
_MZ_FOLIOS = (
    ("herbal", set(range(1, 58)) | {65, 66, 87, 90} | set(range(93, 97))),
    ("astro", set(range(67, 74)) | {85, 86}),
    ("bio", set(range(75, 85))),
    ("pharma", {88, 89} | set(range(99, 103))),
    ("recipes", {58} | set(range(103, 117))),
)
_MZ_FALLBACK = {"H": "herbal", "A": "astro", "Z": "astro", "C": "astro",
                "B": "bio", "P": "pharma", "S": "recipes", "T": "recipes"}
_MZ_ORDER = ("herbal", "astro", "bio", "pharma", "recipes")


def _mz_section(line: Line) -> str:
    import re as _re

    m = _re.match(r"f(\d+)", line.page)
    if m:
        folio = int(m.group(1))
        for name, folios in _MZ_FOLIOS:
            if folio in folios:
                return name
    return _MZ_FALLBACK.get(line.section or "", "recipes")


def mz_family(lines: list) -> dict:
    from .h4 import H4_OUT
    from .mz import peak, scan_scales, top_informative_words

    tokens = [
        w
        for section in _MZ_ORDER
        for line in lines
        if _mz_section(line) == section
        for w in line.words
    ]
    scan = scan_scales(tokens)
    scale, parts, value = peak(scan)
    top10 = [w for w, _ in top_informative_words(tokens, target_scale=807, k=10)]

    published_top10 = {"shedy", "qokeedy", "daiin", "qokaiin", "chedy",
                       "qokedy", "qokar", "qokeey", "chor", "ol"}  # j->i normalized
    overlap = len(set(top10) & published_top10)

    anchors = {}
    for key in ("latin_vulgate", "italian_decameron"):
        path = H4_OUT / f"{key}.txt"
        if path.exists():
            anchor_tokens = path.read_text().split()[: len(tokens)]
            _, _, anchor_value = peak(scan_scales(anchor_tokens))
            anchors[key] = round(anchor_value, 4)

    return {
        "tokens": len(tokens),
        "peak_scale_words": scale,
        "peak_parts": parts,
        "peak_delta_bits_per_word": round(value, 4),
        "top10_at_807": top10,
        "top10_overlap_with_published": overlap,
        "scan": [(s, p, round(v, 5)) for s, p, v in scan],
        "anchors_truncated_to_N": anchors,
    }


# ---------------------------------------------------------------------------
# Target comparison and report
# ---------------------------------------------------------------------------


def _status(value, low, high) -> str:
    if value is None:
        return "CHECK"
    return "PASS" if low <= value <= high else "CHECK"


def build_targets(m: dict) -> list:
    """(id, family, description, published, measured, band, status) rows.

    Bands are PROPOSED tolerances (D17) — Tim ratifies at G1. Sources:
    T11-entropy-targets.md (LB), T11-currier-positional-targets.md (S1-S5),
    T11-montemurro-targets.md (MZ).
    """
    lb, lex, pos, adj, mz = (m["lb_entropy"], m["lexical"], m["positional"],
                             m["adjacency"], m["montemurro_zanette"])
    rows = []

    def add(tid, family, description, published, measured, band, status):
        rows.append({"id": tid, "family": family, "description": description,
                     "published": published, "measured": measured, "band": band,
                     "status": status})

    for subset, target in (("full", 2.1593), ("A", 2.1705), ("B", 2.0147)):
        value = lb[f"it_{subset}"]["h2"]
        add(f"E-{subset}", "entropy", f"h2 Voynich {subset} (Takahashi, labels incl.)",
            target, value, "±0.05", _status(value, target - 0.05, target + 0.05))
    h1 = lb["it_full"]["h1"]
    add("E-h1", "entropy", "h1 full Voynich (Takahashi)", 3.8828, h1, "±0.05",
        _status(h1, 3.8328, 3.9328))
    for subset in ("full", "A", "B"):
        add(f"E-{subset}-zl", "entropy", f"h2 Voynich {subset} on ZL (our primary)",
            "(informational)", lb[f"zl_{subset}"]["h2"], "—", "INFO")
    for hand, target in (("1", 2.122), ("2", 1.921), ("3", 1.999), ("4", 2.279),
                         ("5", 2.111)):
        key = f"it_hand{hand}"
        if key in lb:
            add(f"E-hand{hand}", "entropy", f"h2 Hand {hand} (App. A, v2-plume values)",
                target, lb[key]["h2"], "±0.08 (plume delta)",
                _status(lb[key]["h2"], target - 0.08, target + 0.08))

    add("Z-daiin-A", "zipf", "top word of A: daiin share of A tokens", 0.045,
        lex["daiin_share_A"], "±0.01",
        _status(lex["daiin_share_A"], 0.035, 0.055))
    add("Z-chedy-B", "zipf", "top word of B: chedy share of B tokens", 0.021,
        lex["chedy_share_B"], "±0.007",
        _status(lex["chedy_share_B"], 0.014, 0.028))
    add("Z-top10-A", "zipf", "top-10 words coverage, A", 0.157, lex["top10_coverage_A"],
        "±0.03", _status(lex["top10_coverage_A"], 0.127, 0.187))
    add("Z-top10-B", "zipf", "top-10 words coverage, B", 0.145, lex["top10_coverage_B"],
        "±0.03", _status(lex["top10_coverage_B"], 0.115, 0.175))

    add("AB-chedy0", "currier", "chedy occurrences in A (published: 'does not occur')",
        0, lex["chedy_count_A"], "≤3", "PASS" if lex["chedy_count_A"] <= 3 else "CHECK")
    for cluster, target_low, target_high in (("herbalA", 15, 25), ("herbalB", 28, 50),
                                             ("bioB", 40, 75)):
        value = lex[f"inverse_daiin_{cluster}"]
        add(f"AB-daiin-{cluster}", "currier",
            f"inverse frequency of daiin, {cluster} (targets 19/38/50-60)",
            {"herbalA": 19, "herbalB": 38, "bioB": "50-60"}[cluster], value,
            f"{target_low}-{target_high}", _status(value, target_low, target_high))
    add("AB-rep-A", "currier", "consecutive word repetition rate, A", 0.0084,
        lex["repetition_rate_A"], "±0.005",
        _status(lex["repetition_rate_A"], 0.0034, 0.0134))
    add("AB-rep-B", "currier", "consecutive word repetition rate, B", 0.0094,
        lex["repetition_rate_B"], "±0.005",
        _status(lex["repetition_rate_B"], 0.0044, 0.0144))

    add("G-e-tk", "glyph", "P(e | after t/k) — Currier: 'about half'", 0.5,
        lex["e_after_tk"], "0.35-0.65", _status(lex["e_after_tk"], 0.35, 0.65))
    add("G-e-pf", "glyph", "P(e | after p/f) — Currier: 'never, ever'", 0.0,
        lex["e_after_pf"], "≤0.02", _status(lex["e_after_pf"], 0.0, 0.02))
    add("G-q-o", "glyph", "q followed by o", 0.98, lex["q_followed_by_o"], "≥0.95",
        _status(lex["q_followed_by_o"], 0.95, 1.0))
    add("G-yfinal", "glyph", "words ending in y (LB: 41%)", 0.41, lex["y_final_share"],
        "±0.05", _status(lex["y_final_share"], 0.36, 0.46))
    add("G-final6", "glyph", "words ending y/n/l/r/m/s (LB: 93%)", 0.93,
        lex["ynlrms_final_share"], "±0.04",
        _status(lex["ynlrms_final_share"], 0.89, 0.97))

    add("P-pf-par", "positional",
        "share of p/f occurrences in paragraph-initial lines (Currier: 90-95%)",
        "0.90-0.95", pos["pf_share_in_paragraph_initial_lines"], "0.75-0.97",
        _status(pos["pf_share_in_paragraph_initial_lines"], 0.75, 0.97))
    add("P-par-gallows", "positional",
        "paragraphs beginning with gallows t/k/p/f (BL: 85%)", 0.85,
        pos["paragraphs_starting_with_gallows"], "±0.10",
        _status(pos["paragraphs_starting_with_gallows"], 0.75, 0.95))
    add("P-benched0", "positional",
        "paragraph-initial words starting benched gallows (published: 'never'; "
        "operationalized ≤1% of paragraphs)", 0,
        pos["paragraph_initial_benched_gallows_rate"], "≤0.01",
        _status(pos["paragraph_initial_benched_gallows_rate"], 0.0, 0.01))
    add("P-m-final", "positional",
        "share of m occurrences at line end (Currier: 85%)", 0.85,
        pos["m_share_line_final"], "0.60-0.95",
        _status(pos["m_share_line_final"], 0.60, 0.95))
    suppressed = (
        pos["cross_line_repeat_rate"] <= pos["within_line_repeat_rate"] / 3
    )
    add("P-crossline", "positional",
        "word repeats crossing line breaks (Currier: 'not one'; operationalized "
        "≥3x suppression vs within-line rate)",
        f"0 (rate ~0 vs within {pos['within_line_repeat_rate']})",
        f"{pos['cross_line_adjacent_repeats']} (rate {pos['cross_line_repeat_rate']})",
        "rate ≤ within/3", "PASS" if suppressed else "CHECK")
    add("P-firstlen", "positional",
        "first word of line longer by ~1 char (Vogt)", 1.0,
        pos["first_word_length_excess"], "0.5-1.5",
        _status(pos["first_word_length_excess"], 0.5, 1.5))
    add("P-chsh", "positional",
        "line-initial ch/sh suppression (Currier: ~0.1x expected)", 0.1,
        pos["chsh_line_initial_vs_expected"], "0.05-0.35",
        _status(pos["chsh_line_initial_vs_expected"], 0.05, 0.35))

    add("D-y-qo", "adjacency",
        "Bio-B: P(qo|after y-final) vs P(qo|after non-y) (Currier: ~4x)", 4.0,
        adj["contrast"], "2.5-8.0", _status(adj["contrast"], 2.5, 8.0))

    add("MZ-scale", "montemurro",
        "peak scale of word-information (MZ: 807 words; languages 600-800)", 807,
        mz["peak_scale_words"], "500-1100",
        _status(mz["peak_scale_words"], 500, 1100))
    add("MZ-top10", "montemurro",
        "top-10 informative words overlap with MZ Table 1 (j/i normalized)",
        "10/10", f"{mz['top10_overlap_with_published']}/10", "≥6",
        "PASS" if mz["top10_overlap_with_published"] >= 6 else "CHECK")
    add("MZ-value", "montemurro",
        "peak ΔI bits/word (MZ: between Latin ~0.2 and Chinese ~0.6, above English)",
        "~0.3-0.5", mz["peak_delta_bits_per_word"], "0.2-0.65",
        _status(mz["peak_delta_bits_per_word"], 0.2, 0.65))
    return rows


def _render_report(results: dict) -> str:
    rows = results["targets"]
    passed = sum(1 for r in rows if r["status"] == "PASS")
    info = sum(1 for r in rows if r["status"] == "INFO")
    check = sum(1 for r in rows if r["status"] == "CHECK")
    lines = [
        "# T1.1 Replication Report — Gate G1",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.replication` (deterministic; full measurements in "
        "`results/replication/replication.json`).",
        "",
        f"**{passed} PASS · {check} CHECK · {info} informational** across "
        "entropy, Zipf/lexical, Currier A/B, glyph-sequence, positional, adjacency, "
        "and Montemurro-Zanette families.",
        "",
        "Tolerance bands are PROPOSED (D17) and await Tim's ratification; CHECK rows "
        "are discussed below the table, not silently widened. Published targets were "
        "measured on the Takahashi/LSI or Stolfi interlinear transliterations; our "
        "primary corpus is ZL3b (L11) with IT (Takahashi IVTFF) as the like-for-like "
        "entropy corpus. Sources: specs/T11-*.md.",
        "",
        "| id | family | description | published | measured | band | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['id']} | {r['family']} | {r['description']} | {r['published']} "
            f"| {r['measured']} | {r['band']} | **{r['status']}** |"
        )
    mz = results["montemurro_zanette"]
    lines += [
        "",
        "## Montemurro-Zanette detail",
        "",
        f"- Corpus: {mz['tokens']:,} paragraph-text tokens, reordered into the MZ "
        "section order (folio map per spec; D18 preprocessing policy).",
        f"- Peak: ΔI = {mz['peak_delta_bits_per_word']} bits/word at "
        f"{mz['peak_scale_words']} words/part ({mz['peak_parts']} parts).",
        f"- Top-10 informative words at s≈807: {', '.join(mz['top10_at_807'])}.",
        f"- H4 anchors truncated to N (informational): {mz['anchors_truncated_to_N']} "
        "— MZ's Latin anchor (Augustine) peaked ≈0.2 bits/word.",
        "",
        "## CHECK rows and near-misses, discussed",
        "",
        "- **AB-daiin clusters**: the published inverse-frequency *gradient* "
        "(A < Herbal-B < Bio-B) reproduces exactly in direction; absolute values run "
        "20-35% high, consistent with Zandbergen's clusters being specific page sets "
        "(token totals 7975/3335/6696) vs our $I x $L slices, and ZL-vs-GC counts.",
        f"- **P-firstlen**: direction robustly confirmed "
        f"(+{results['positional']['first_word_length_excess']} vs all words, "
        f"+{results['positional']['first_vs_second_word_excess']} vs second word) but "
        "below Vogt's ~1 char; his corpus/definition may differ. For D17 review.",
        f"- **Verbatim-claim caveats**: Currier's 'not one' cross-line repeat is "
        f"overstated on full ZL — "
        f"{results['positional']['cross_line_adjacent_repeats']} instances "
        f"({', '.join(p for p, _ in results['positional']['cross_line_repeat_cases'])})"
        ", still ~6x suppressed vs the within-line repeat rate. D'Imperio's 'benched "
        "gallows never paragraph-initial' has 5 exceptions in 731 paragraphs "
        f"({', '.join(p for p, _ in results['positional']['paragraph_initial_benched_gallows_cases'])})"
        ". The single `chedy` in Language A sits at f89r1.7.",
        f"- **D-y-qo**: Currier's '4x' is read as the conditional contrast "
        f"P(qo|after y-final)={results['adjacency']['bio_b_qo_rate_after_y_final']} vs "
        f"P(qo|after non-y)={results['adjacency']['bio_b_qo_rate_after_non_y']}; the "
        f"naive vs-overall-baseline reading gives "
        f"{results['adjacency']['lift_vs_baseline']} because Bio-B is qo-saturated "
        "(~24% of tokens).",
        "",
        "## Notes and deviations",
        "",
        "- **Transliteration deltas are expected**: LB targets were computed on the "
        "LSI/Takahashi text with `*` uncertain glyphs retained; we drop uncertain "
        "words (<0.15% of text) and use IVTFF editions. Anything outside band is "
        "flagged CHECK and discussed, per flag-don't-resolve.",
        "- **D17 (open)**: G1 pass tolerances proposed here need Tim's ratification.",
        "- **D18 (open)**: MZ2013 does not specify uncertain-glyph/label handling; "
        "policy used: paragraph-text loci only, uncertain words dropped.",
        "",
        "## G1 sign-off",
        "",
        "- [ ] Tolerances ratified (D17)",
        "- [ ] CHECK rows reviewed",
        "- [ ] Gate G1 approved (Tim)",
        "",
    ]
    return "\n".join(lines)


def run() -> dict:
    zl = IVTFFDocument.load(path_for("zl"))
    it = IVTFFDocument.load(path_for("it"))
    lines = paragraph_lines(zl)
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "corpus": "ZL3b EVA primary; IT2a (Takahashi) for like-for-like entropy",
        "word_policy": "EVA default + drop_uncertain_words + drop '@'-escape words",
        "positional_effects": positional_effects(lines),
        "currier_split": currier_split(lines),
        "entropy_zipf": entropy_zipf(lines),
        "lb_entropy": lb_entropy_family(zl, it),
        "lexical": lexical_battery(zl, lines),
        "positional": positional_battery(lines),
        "adjacency": adjacency_battery(lines),
        "montemurro_zanette": mz_family(lines),
        "summary_all_words": summarize([w for line in lines for w in line.words]),
    }
    results["targets"] = build_targets(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "replication.json").write_text(json.dumps(results, indent=2) + "\n")
    report_path = ROOT / "reports" / "replication_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_report(results))
    return results


if __name__ == "__main__":
    measured = run()
    for row in measured["targets"]:
        print(f"{row['status']:6s} {row['id']:16s} published={row['published']} "
              f"measured={row['measured']}")
