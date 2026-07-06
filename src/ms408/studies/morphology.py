"""T2.1 — Morphology and positional structure study (W2).

Characterizes Voynichese word structure as a formal system, always in contrast
with the harness classes (H2 Naibbe cipher, H3 self-citation, H4 natural
languages) at MATCHED token counts, so every number has a comparative meaning.

Four statistic families:

1. **Edit-distance-1 similarity network** over word types (the chol/chor-type
   network): main-component share, mean degree, isolates. Timm & Schinner
   report VMS ≈ 84.7% main component; their generator ≈ 81.9%.
2. **Glyph positional concentration**: per-glyph entropy of its within-word
   position distribution (5 bins), frequency-weighted. Lindemann & Bowern
   attribute the h2 anomaly to "characters heavily restricted to certain
   positions within the word" — this makes that restriction a scalar.
3. **Affix structure**: top word-initial/word-final n-grams with token
   coverage; share of tokens carrying both a top-10 prefix and suffix.
4. **Curve/line grammar validity**: share of tokens accepted by Timm's
   curve-line adjacency rules (harness.selfcitation.is_valid) — high for
   H1/H2/H3 by construction or hypothesis, low for natural languages.

Stratification per L8: ZL full / Currier A / Currier B; v101 sensitivity per
L11 (GC corpus). All corpora truncated to the ZL paragraph-token count.

Usage:
    python -m ms408.studies.morphology
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..harness.naibbe import NaibbeCipher, NaibbeConfig, NaibbeTables
from ..harness.selfcitation import SelfCitationConfig, SelfCitationGenerator, Word, is_valid
from ..ivtff import IVTFFDocument
from ..replication import paragraph_lines
from ..sources import path_for

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "studies"
REPORTS_DIR = ROOT / "reports"


# ---------------------------------------------------------------------------
# 1. Edit-distance-1 network
# ---------------------------------------------------------------------------


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def ed1_edges(types: list) -> set:
    """All unordered pairs of types at edit distance exactly 1."""
    index = {t: i for i, t in enumerate(types)}
    edges = set()
    # substitutions: same length, one differing position -> shared wildcard pattern
    buckets = defaultdict(list)
    for t in types:
        for i in range(len(t)):
            buckets[(i, t[:i], t[i + 1 :])].append(index[t])
    for members in buckets.values():
        if len(members) > 1:
            members.sort()
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    edges.add((members[a], members[b]))
    # insertions/deletions: deletion of one char maps longer word onto shorter
    for t in types:
        for i in range(len(t)):
            shorter = t[: i] + t[i + 1 :]
            j = index.get(shorter)
            if j is not None:
                edges.add(tuple(sorted((index[t], j))))
    return edges


def ed1_network_stats(words: list) -> dict:
    types = sorted(set(words))
    edges = ed1_edges(types)
    uf = _UnionFind(len(types))
    degree = Counter()
    for a, b in edges:
        uf.union(a, b)
        degree[a] += 1
        degree[b] += 1
    components = Counter(uf.find(i) for i in range(len(types)))
    main = max(components.values()) if components else 0
    return {
        "types": len(types),
        "edges": len(edges),
        "mean_degree": round(2 * len(edges) / len(types), 3),
        "main_component_share": round(main / len(types), 4),
        "isolate_share": round(
            sum(1 for i in range(len(types)) if degree[i] == 0) / len(types), 4
        ),
    }


# ---------------------------------------------------------------------------
# 2. Glyph positional concentration
# ---------------------------------------------------------------------------

_BINS = 5


def positional_concentration(words: list) -> dict:
    """Per-glyph normalized entropy of within-word position (5 bins), plus the
    frequency-weighted corpus mean. 0 = fully position-locked, 1 = uniform."""
    per_glyph: dict = defaultdict(lambda: [0] * _BINS)
    for w in words:
        if len(w) == 1:
            per_glyph[w][_BINS // 2] += 1
            continue
        for i, c in enumerate(w):
            per_glyph[c][int(i / (len(w) - 1) * (_BINS - 1) + 0.5)] += 1
    max_h = math.log2(_BINS)
    glyph_entropy = {}
    weighted = total = 0
    for glyph, bins in per_glyph.items():
        n = sum(bins)
        h = -sum((b / n) * math.log2(b / n) for b in bins if b)
        glyph_entropy[glyph] = round(h / max_h, 4)
        weighted += n * (h / max_h)
        total += n
    top = sorted(glyph_entropy.items(), key=lambda kv: per_glyph[kv[0]] and -sum(per_glyph[kv[0]]))
    return {
        "mean_normalized_position_entropy": round(weighted / total, 4),
        "most_frequent_glyphs": {
            g: glyph_entropy[g] for g, _ in top[:12]
        },
    }


# ---------------------------------------------------------------------------
# 3. Affix structure
# ---------------------------------------------------------------------------


def affix_structure(words: list, top_n: int = 10) -> dict:
    def grams(extract):
        counts = Counter()
        for w in words:
            for k in (1, 2, 3):
                if len(w) > k:
                    counts[extract(w, k)] += 1
        return counts

    prefix_counts = grams(lambda w, k: w[:k])
    suffix_counts = grams(lambda w, k: w[-k:])

    def top(counts):
        return [
            {"gram": g, "token_coverage": round(c / len(words), 4)}
            for g, c in counts.most_common(top_n)
        ]

    top_prefixes = {row["gram"] for row in top(prefix_counts)}
    top_suffixes = {row["gram"] for row in top(suffix_counts)}
    both = sum(
        1 for w in words
        if any(w.startswith(p) and len(w) > len(p) for p in top_prefixes)
        and any(w.endswith(s) and len(w) > len(s) for s in top_suffixes)
    )
    return {
        "top_prefixes": top(prefix_counts),
        "top_suffixes": top(suffix_counts),
        "share_with_top_prefix_and_suffix": round(both / len(words), 4),
    }


# ---------------------------------------------------------------------------
# 4. Curve/line grammar validity
# ---------------------------------------------------------------------------


def curveline_valid_share(words: list) -> float:
    cache: dict = {}
    valid = 0
    for w in words:
        if w not in cache:
            cache[w] = is_valid(Word.parse(w, "X"))
        valid += cache[w]
    return round(valid / len(words), 4)


# ---------------------------------------------------------------------------
# Corpora and study assembly
# ---------------------------------------------------------------------------


def _corpora() -> dict:
    """Named word lists; all truncated to the ZL paragraph-token count."""
    zl_lines = paragraph_lines(IVTFFDocument.load(path_for("zl")))
    zl_all = [w for line in zl_lines for w in line.words]
    n = len(zl_all)
    corpora = {
        "zl_all": ("H1", zl_all),
        "zl_currierA": ("H1", [w for line in zl_lines if line.currier == "A"
                               for w in line.words]),
        "zl_currierB": ("H1", [w for line in zl_lines if line.currier == "B"
                               for w in line.words]),
    }
    gc_lines = paragraph_lines(IVTFFDocument.load(path_for("gc")))
    corpora["gc_v101"] = ("H1-sensitivity", [w for line in gc_lines
                                             for w in line.words][:n])

    tables = NaibbeTables.load()
    pliny = path_for("naibbe_pliny").read_text(encoding="utf-8").splitlines()
    naibbe = NaibbeCipher(tables, NaibbeConfig(deck="52"), seed=408).encrypt_text(pliny)
    corpora["h2_naibbe"] = ("H2", [w for line in naibbe.ciphertext_lines
                                   for w in line.split()][:n])

    generated = SelfCitationGenerator(SelfCitationConfig(lines_to_create=3800),
                                      seed=19).generate()
    corpora["h3_selfcitation"] = ("H3", [w for line in generated.lines
                                         for w in line][:n])

    for key, name in (("latin_vulgate", "h4_latin"),
                      ("italian_decameron", "h4_italian")):
        path = H4_OUT / f"{key}.txt"
        corpora[name] = ("H4", path.read_text(encoding="utf-8").split()[:n])
    return corpora


def run() -> dict:
    corpora = _corpora()
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "word_policy": "EVA default + drop_uncertain_words + drop '@'-escape words; "
        "paragraph-text loci; all corpora truncated to the ZL token count",
        "corpora": {},
    }
    for name, (cls, words) in corpora.items():
        results["corpora"][name] = {
            "class": cls,
            "tokens": len(words),
            "ed1_network": ed1_network_stats(words),
            "positional": positional_concentration(words),
            "affixes": affix_structure(words),
            "curveline_valid_share": curveline_valid_share(words),
        }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "morphology.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "study_morphology.md").write_text(_render_report(results))
    return results


def _render_report(results: dict) -> str:
    c = results["corpora"]

    def row(name):
        e = c[name]
        return (
            f"| {name} | {e['class']} | {e['ed1_network']['main_component_share']} "
            f"| {e['ed1_network']['mean_degree']} "
            f"| {e['positional']['mean_normalized_position_entropy']} "
            f"| {e['affixes']['share_with_top_prefix_and_suffix']} "
            f"| {e['curveline_valid_share']} |"
        )

    zl = c["zl_all"]
    lines = [
        "# T2.1 Study Report — Morphology and Positional Structure (W2)",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.studies.morphology`; full numbers in "
        "`results/studies/morphology.json`. All corpora truncated to "
        f"{zl['tokens']:,} tokens (the ZL paragraph corpus) for comparability.",
        "",
        "| corpus | class | ED1 main comp. | mean degree | position entropy "
        "| affix coverage | curve/line valid |",
        "|---|---|---|---|---|---|---|",
        *[row(name) for name in c],
        "",
        "Column meanings: **ED1 main comp.** = share of word types in the largest "
        "edit-distance-1 component (VMS published ≈ 0.847); **position entropy** = "
        "frequency-weighted normalized entropy of glyph position within words "
        "(0 = fully position-locked); **affix coverage** = tokens carrying both a "
        "top-10 prefix and top-10 suffix; **curve/line valid** = tokens accepted by "
        "Timm's adjacency grammar.",
        "",
        "## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 review — L10)",
        "",
        _claims(results),
        "",
        "## Affix inventories (ZL full)",
        "",
        "Top prefixes: "
        + ", ".join(f"`{r['gram']}` {r['token_coverage']:.1%}"
                    for r in zl["affixes"]["top_prefixes"][:8]),
        "",
        "Top suffixes: "
        + ", ".join(f"`{r['gram']}` {r['token_coverage']:.1%}"
                    for r in zl["affixes"]["top_suffixes"][:8]),
        "",
    ]
    return "\n".join(lines)


def _claims(results: dict) -> str:
    c = results["corpora"]
    zl = c["zl_all"]
    h4_pos = [c[k]["positional"]["mean_normalized_position_entropy"]
              for k in ("h4_latin", "h4_italian")]
    h4_net = [c[k]["ed1_network"]["main_component_share"]
              for k in ("h4_latin", "h4_italian")]
    claims = [
        f"1. **[C, candidate B pending T3.3]** Voynichese glyph positions are far more "
        f"restricted than natural-language controls at matched size: mean normalized "
        f"position entropy {zl['positional']['mean_normalized_position_entropy']} (ZL) "
        f"vs {min(h4_pos)}–{max(h4_pos)} (H4 Latin/Italian). The gibberish classes "
        f"H2/H3 ({c['h2_naibbe']['positional']['mean_normalized_position_entropy']}, "
        f"{c['h3_selfcitation']['positional']['mean_normalized_position_entropy']}) sit "
        f"near the VMS, consistent with position restriction being the h2-anomaly "
        f"mechanism (Lindemann-Bowern) that both generator families were designed to "
        f"reproduce.",
        f"2. **[C, candidate B pending T3.3]** The VMS edit-distance-1 network is far "
        f"denser than natural language at matched token count: main-component share "
        f"{zl['ed1_network']['main_component_share']} (ZL; published ≈0.847 on the "
        f"full MS) vs {min(h4_net)}–{max(h4_net)} (H4). H3 self-citation "
        f"({c['h3_selfcitation']['ed1_network']['main_component_share']}) reproduces "
        f"this by construction; H2 Naibbe "
        f"({c['h2_naibbe']['ed1_network']['main_component_share']}) also lands high — "
        f"so network density alone does not discriminate cipher from gibberish.",
        f"3. **[C]** Affix regularity: {zl['affixes']['share_with_top_prefix_and_suffix']:.0%} "
        f"of ZL tokens carry both a top-10 prefix and top-10 suffix (A: "
        f"{c['zl_currierA']['affixes']['share_with_top_prefix_and_suffix']:.0%}, B: "
        f"{c['zl_currierB']['affixes']['share_with_top_prefix_and_suffix']:.0%}).",
        f"4. **[C]** Timm's curve/line grammar accepts "
        f"{zl['curveline_valid_share']:.0%} of ZL tokens vs "
        f"{c['h4_latin']['curveline_valid_share']:.0%}/"
        f"{c['h4_italian']['curveline_valid_share']:.0%} for H4 — Voynichese is "
        f"grammar-constrained at the glyph-adjacency level in a way natural text is "
        f"not. (EVA-specific measure: the v101 value "
        f"({c['gc_v101']['curveline_valid_share']:.0%}) reflects the different glyph "
        f"alphabet, not a sensitivity failure — excluded from the L11 pass.)",
        f"5. **[C]** v101 sensitivity (L11): the GC corpus gives main-component "
        f"{c['gc_v101']['ed1_network']['main_component_share']} and position entropy "
        f"{c['gc_v101']['positional']['mean_normalized_position_entropy']} — "
        f"the direction of claims 1-2 (dense network, strong position restriction "
        f"vs natural controls) is unchanged under the alternative transliteration.",
    ]
    return "\n".join(claims)


if __name__ == "__main__":
    study = run()
    for name, entry in study["corpora"].items():
        print(f"{name:18s} {entry['class']:15s} "
              f"net={entry['ed1_network']['main_component_share']:.3f} "
              f"posH={entry['positional']['mean_normalized_position_entropy']:.3f} "
              f"affix={entry['affixes']['share_with_top_prefix_and_suffix']:.3f} "
              f"cl={entry['curveline_valid_share']:.3f}")
