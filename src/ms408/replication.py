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


def run() -> dict:
    doc = IVTFFDocument.load(path_for("zl"))
    lines = paragraph_lines(doc)
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "corpus": "ZL3b EVA, paragraph-text loci (P*), <%>/<$> paragraph structure",
        "word_policy": "EVA default + drop_uncertain_words + drop '@'-escape words",
        "entropy_zipf": None,
        "currier_split": None,
        "positional_effects": None,
        "summary_all_words": None,
    }
    results["positional_effects"] = positional_effects(lines)
    results["currier_split"] = currier_split(lines)
    results["entropy_zipf"] = entropy_zipf(lines)
    results["summary_all_words"] = summarize([w for line in lines for w in line.words])
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "measurements.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


if __name__ == "__main__":
    measured = run()
    print(json.dumps({k: v for k, v in measured.items() if k != "summary_all_words"},
                     indent=2)[:4000])
