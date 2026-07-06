"""T2.2 — Topic induction and section-alignment test (W2 key test).

Induces topic structure from word co-occurrence ALONE (page-level TF-IDF
vectors, deterministic average-linkage clustering — no image information,
no section labels), then asks whether the induced structure reproduces:

  (a) the illustration-based section labels ($I) — the KEY TEST,
  (b) the Currier A/B split ($L) — the known confound,
  (c) the Fagin Davis scribal hands ($H).

Agreement is scored with Adjusted Rand Index and Normalized Mutual Information,
with permutation p-values (seeded, deterministic). A complementary sequential
test compares adjacent-page cosine similarity within vs across section
boundaries in manuscript order.

Sensitivity per L11: the full battery reruns on the v101 (GC) corpus.

Usage:
    python -m ms408.studies.topics
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..replication import paragraph_lines
from ..sources import path_for

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "studies"
REPORTS_DIR = ROOT / "reports"

MIN_PAGE_TOKENS = 30
VOCAB_SIZE = 400
PERMUTATIONS = 2000
SEED = 408


# ---------------------------------------------------------------------------
# Vectors and clustering
# ---------------------------------------------------------------------------


def page_vectors(lines) -> tuple:
    """(page_names, tfidf_matrix, labels) from paragraph lines, manuscript order."""
    per_page: dict = {}
    labels: dict = {}
    for line in lines:
        per_page.setdefault(line.page, []).extend(line.words)
        labels[line.page] = {"section": line.section, "currier": line.currier,
                            "hand": line.hand}
    pages = [p for p, words in per_page.items() if len(words) >= MIN_PAGE_TOKENS]
    totals = Counter(w for p in pages for w in per_page[p])
    vocabulary = [w for w, _ in totals.most_common(VOCAB_SIZE)]
    vocab_index = {w: i for i, w in enumerate(vocabulary)}
    df = Counter(w for p in pages for w in set(per_page[p]) if w in vocab_index)
    matrix = np.zeros((len(pages), len(vocabulary)))
    for r, p in enumerate(pages):
        counts = Counter(per_page[p])
        n = len(per_page[p])
        for w, c in counts.items():
            i = vocab_index.get(w)
            if i is not None:
                matrix[r, i] = (c / n) * math.log(len(pages) / df[w])
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    matrix = matrix / np.where(norms == 0, 1, norms)
    return pages, matrix, {p: labels[p] for p in pages}


def average_linkage(similarity: np.ndarray, k: int) -> list:
    """Deterministic average-linkage agglomerative clustering into k clusters."""
    n = similarity.shape[0]
    clusters = {i: [i] for i in range(n)}
    sim = {(a, b): similarity[a, b] for a in range(n) for b in range(a + 1, n)}
    while len(clusters) > k:
        (a, b), _ = max(sim.items(), key=lambda kv: (kv[1], -kv[0][0], -kv[0][1]))
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
        for key in [key for key in sim if b in key]:
            del sim[key]
        for c in clusters:
            if c == a:
                continue
            pair = (min(a, c), max(a, c))
            sim[pair] = float(
                np.mean(similarity[np.ix_(clusters[a], clusters[c])])
            )
    assignment = [0] * n
    for label, members in enumerate(sorted(clusters.values(), key=min)):
        for m in members:
            assignment[m] = label
    return assignment


# ---------------------------------------------------------------------------
# Agreement measures
# ---------------------------------------------------------------------------


def ari(a: list, b: list) -> float:
    contingency: Counter = Counter(zip(a, b))
    rows, cols = Counter(a), Counter(b)
    n = len(a)
    sum_cells = sum(math.comb(c, 2) for c in contingency.values())
    sum_rows = sum(math.comb(c, 2) for c in rows.values())
    sum_cols = sum(math.comb(c, 2) for c in cols.values())
    expected = sum_rows * sum_cols / math.comb(n, 2)
    max_index = (sum_rows + sum_cols) / 2
    if max_index == expected:
        return 0.0
    return (sum_cells - expected) / (max_index - expected)


def nmi(a: list, b: list) -> float:
    n = len(a)
    joint = Counter(zip(a, b))
    pa, pb = Counter(a), Counter(b)
    mi = sum(
        (c / n) * math.log2((c / n) / ((pa[x] / n) * (pb[y] / n)))
        for (x, y), c in joint.items()
    )
    ha = -sum((c / n) * math.log2(c / n) for c in pa.values())
    hb = -sum((c / n) * math.log2(c / n) for c in pb.values())
    if ha == 0 or hb == 0:
        return 0.0
    return mi / math.sqrt(ha * hb)


def permutation_p(clusters: list, target: list, observed: float, seed: int = SEED) -> float:
    rng = random.Random(seed)
    shuffled = list(target)
    hits = 0
    for _ in range(PERMUTATIONS):
        rng.shuffle(shuffled)
        if ari(clusters, shuffled) >= observed:
            hits += 1
    return (hits + 1) / (PERMUTATIONS + 1)


# ---------------------------------------------------------------------------
# Study
# ---------------------------------------------------------------------------


def _alignment(clusters, labels_list) -> dict:
    observed = ari(clusters, labels_list)
    return {
        "ari": round(observed, 4),
        "nmi": round(nmi(clusters, labels_list), 4),
        "p_permutation": round(permutation_p(clusters, labels_list, observed), 5),
    }


def boundary_test(pages: list, matrix: np.ndarray, labels: dict) -> dict:
    """Adjacent-page cosine similarity, within vs across section boundaries."""
    sims, same = [], []
    for i in range(len(pages) - 1):
        sims.append(float(matrix[i] @ matrix[i + 1]))
        same.append(labels[pages[i]]["section"] == labels[pages[i + 1]]["section"])
    within = [s for s, flag in zip(sims, same) if flag]
    across = [s for s, flag in zip(sims, same) if not flag]
    observed = sum(within) / len(within) - sum(across) / len(across)
    rng = random.Random(SEED)
    hits = 0
    flags = list(same)
    for _ in range(PERMUTATIONS):
        rng.shuffle(flags)
        w = [s for s, f in zip(sims, flags) if f]
        x = [s for s, f in zip(sims, flags) if not f]
        if w and x and (sum(w) / len(w) - sum(x) / len(x)) >= observed:
            hits += 1
    return {
        "mean_within_section": round(sum(within) / len(within), 4),
        "mean_across_boundary": round(sum(across) / len(across), 4),
        "difference": round(observed, 4),
        "p_permutation": round((hits + 1) / (PERMUTATIONS + 1), 5),
        "boundaries": len(across),
    }


def analyze(doc: IVTFFDocument) -> dict:
    lines = paragraph_lines(doc)
    pages, matrix, labels = page_vectors(lines)
    similarity = matrix @ matrix.T

    section_labels = [labels[p]["section"] or "?" for p in pages]
    currier_labels = [labels[p]["currier"] or "?" for p in pages]
    hand_labels = [labels[p]["hand"] or "?" for p in pages]
    k_sections = len(set(section_labels))

    clusters_k = average_linkage(similarity, k_sections)

    # the two dominant clusters vs the A/B split (average-linkage at k=2 is a
    # chaining artifact — singletons split off — so evaluate the two largest
    # clusters of the k-sections solution instead)
    sizes = Counter(clusters_k)
    top_two = {label for label, _ in sizes.most_common(2)}
    subset = [i for i, cl in enumerate(clusters_k) if cl in top_two]
    two_big_vs_currier = _alignment(
        [clusters_k[i] for i in subset], [currier_labels[i] for i in subset]
    )

    # KEY-TEST CONFOUND CONTROL: section alignment WITHIN each dialect
    within = {}
    for dialect in ("A", "B"):
        idx = [i for i, lab in enumerate(currier_labels) if lab == dialect]
        sections_within = [section_labels[i] for i in idx]
        k = len(set(sections_within))
        if len(idx) >= 20 and k >= 2:
            sub_clusters = average_linkage(similarity[np.ix_(idx, idx)], k)
            within[dialect] = {
                "pages": len(idx),
                "k": k,
                **_alignment(sub_clusters, sections_within),
            }

    return {
        "pages": len(pages),
        "vocabulary": VOCAB_SIZE,
        "k_sections": k_sections,
        "alignment_kSections_vs_section": _alignment(clusters_k, section_labels),
        "alignment_kSections_vs_currier": _alignment(clusters_k, currier_labels),
        "alignment_kSections_vs_hand": _alignment(clusters_k, hand_labels),
        "two_largest_clusters_vs_currier": two_big_vs_currier,
        "within_dialect_section_alignment": within,
        "confound_section_vs_currier": {
            "ari": round(ari(section_labels, currier_labels), 4),
            "nmi": round(nmi(section_labels, currier_labels), 4),
        },
        "boundary_test": boundary_test(pages, matrix, labels),
        "cluster_sizes_k": sorted(sizes.values(), reverse=True),
    }


def run() -> dict:
    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "method": f"page TF-IDF (top {VOCAB_SIZE} words, pages ≥{MIN_PAGE_TOKENS} "
        "tokens, paragraph text only), cosine, deterministic average-linkage; "
        f"ARI/NMI with {PERMUTATIONS} permutations, seed {SEED}",
        "zl": analyze(IVTFFDocument.load(path_for("zl"))),
        "gc_v101": analyze(IVTFFDocument.load(path_for("gc"))),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "topics.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "study_topics.md").write_text(_render_report(results))
    return results


def _render_report(results: dict) -> str:
    zl, gc = results["zl"], results["gc_v101"]

    def block(tag, data):
        rows = [
            f"| {tag} k=sections vs sections | {data['alignment_kSections_vs_section']['ari']} "
            f"| {data['alignment_kSections_vs_section']['nmi']} "
            f"| {data['alignment_kSections_vs_section']['p_permutation']} |",
            f"| {tag} k=sections vs Currier | {data['alignment_kSections_vs_currier']['ari']} "
            f"| {data['alignment_kSections_vs_currier']['nmi']} "
            f"| {data['alignment_kSections_vs_currier']['p_permutation']} |",
            f"| {tag} k=sections vs hands | {data['alignment_kSections_vs_hand']['ari']} "
            f"| {data['alignment_kSections_vs_hand']['nmi']} "
            f"| {data['alignment_kSections_vs_hand']['p_permutation']} |",
            f"| {tag} two largest clusters vs Currier | "
            f"{data['two_largest_clusters_vs_currier']['ari']} "
            f"| {data['two_largest_clusters_vs_currier']['nmi']} "
            f"| {data['two_largest_clusters_vs_currier']['p_permutation']} |",
        ]
        for dialect, w in data["within_dialect_section_alignment"].items():
            rows.append(
                f"| {tag} within-{dialect} vs sections ({w['pages']}p, k={w['k']}) "
                f"| {w['ari']} | {w['nmi']} | {w['p_permutation']} |"
            )
        return rows

    b = zl["boundary_test"]
    lines = [
        "# T2.2 Study Report — Topic Induction and Section Alignment (W2 key test)",
        "",
        f"Generated {results['built_at']} at commit `{results['git_commit'][:10]}` by "
        "`python -m ms408.studies.topics`; full numbers in "
        "`results/studies/topics.json`.",
        "",
        f"Method: {results['method']}. No image information or labels enter the "
        "clustering — only word co-occurrence.",
        "",
        "| comparison | ARI | NMI | p (perm.) |",
        "|---|---|---|---|",
        *block("ZL", zl),
        *block("v101", gc),
        "",
        f"Section↔Currier confound (labels only): ARI "
        f"{zl['confound_section_vs_currier']['ari']}, NMI "
        f"{zl['confound_section_vs_currier']['nmi']}.",
        "",
        "## Sequential boundary test (ZL, manuscript order)",
        "",
        f"Adjacent-page cosine similarity: within-section "
        f"{b['mean_within_section']} vs across-boundary {b['mean_across_boundary']} "
        f"(difference {b['difference']}, p={b['p_permutation']}, "
        f"{b['boundaries']} boundaries).",
        "",
        "## Claims (graded per RESEARCH-PLAN §6; A/B require T3.3 review — L10)",
        "",
        _claims(results),
        "",
    ]
    return "\n".join(lines)


def _claims(results: dict) -> str:
    zl, gc = results["zl"], results["gc_v101"]
    key = zl["alignment_kSections_vs_section"]
    b = zl["boundary_test"]
    within = zl["within_dialect_section_alignment"]
    within_gc = gc["within_dialect_section_alignment"]
    within_rows = "; ".join(
        f"{d}: ARI {w['ari']} (p={w['p_permutation']}, {w['pages']}p)"
        for d, w in within.items()
    )
    within_gc_rows = "; ".join(
        f"{d}: ARI {w['ari']} (p={w['p_permutation']})" for d, w in within_gc.items()
    )
    return "\n".join([
        f"1. **[C, candidate B pending T3.3]** The dominant structure recoverable "
        f"from word co-occurrence alone is the Currier A/B split, not the sections: "
        f"clusters align with dialect at ARI "
        f"{zl['alignment_kSections_vs_currier']['ari']} (ZL) / "
        f"{gc['alignment_kSections_vs_currier']['ari']} (v101), and the two "
        f"dominant clusters recover A/B at ARI "
        f"{zl['two_largest_clusters_vs_currier']['ari']}.",
        f"2. **[C, candidate B pending T3.3]** Section structure is present above "
        f"chance at whole-MS level on both transliterations (ZL ARI {key['ari']}, "
        f"p={key['p_permutation']}; v101 ARI "
        f"{gc['alignment_kSections_vs_section']['ari']}, "
        f"p={gc['alignment_kSections_vs_section']['p_permutation']}) — but the "
        f"dialect-confound control reveals a sharp ASYMMETRY: within Language A the "
        f"text tracks the sections strongly ({within_rows.split(';')[0]}; v101 "
        f"{within_gc_rows.split(';')[0].split(': ')[1]}), while within Language B "
        f"it does not ({within_rows.split('; ')[1]}; v101 "
        f"{within_gc_rows.split('; ')[1].split(': ')[1]}). At page-vector "
        f"granularity, B's sections (bio, stars, herbal-B, recipes) are textually "
        f"homogeneous — the text-image co-variation is an A-side phenomenon.",
        f"3. **[C]** The sequential view agrees: adjacent pages are more similar "
        f"within sections than across boundaries (Δ={b['difference']}, "
        f"p={b['p_permutation']}); section↔dialect label correlation is ARI "
        f"{zl['confound_section_vs_currier']['ari']} for reference.",
        "4. **[C]** Method notes: deterministic average-linkage; k=2 cuts are "
        "chaining-degenerate (evaluated via the two largest clusters instead); "
        "v101 consistently shows STRONGER alignments than EVA — the "
        "transliteration's finer glyph distinctions appear to carry signal, worth "
        "a T1.4 variant.",
    ])


if __name__ == "__main__":
    study = run()
    for corpus in ("zl", "gc_v101"):
        data = study[corpus]
        key = data["alignment_kSections_vs_section"]
        print(f"{corpus:8s} pages={data['pages']} k={data['k_sections']} "
              f"sectionARI={key['ari']} p={key['p_permutation']} "
              f"currierARI={data['alignment_kSections_vs_currier']['ari']} "
              f"within={ {d: w['ari'] for d, w in data['within_dialect_section_alignment'].items()} }")
