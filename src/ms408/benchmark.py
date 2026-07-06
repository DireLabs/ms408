"""Validation-harness benchmark (T0.3 close-out; RESEARCH-PLAN §3).

Assembles all four harness corpus classes and computes the standard metric block
(ms408.textstats.summarize) for each, writing:

- results/harness/benchmark.json  — machine-readable, full provenance (L3)
- reports/harness_benchmark.md    — human-readable summary table

Corpus classes:
  H1  real Voynichese — ZL (EVA, primary) with Currier A/B strata (L8), GC (v101)
  H2  Naibbe ciphertext from known plaintext — our generator, both decks, both
      author plaintexts, seed 408
  H3  self-citation gibberish — our generator, 5 seeds (B dialect), plus the
      author's committed seed-19 reference output for side-by-side
  H4  known-meaningful medieval controls — all normalized registers

H1 word policy: EVA default TextPolicy plus drop words containing '?' (illegible)
or '@' (non-EVA escape codes); all locus types included (labels as well as
running text). T1.1 replication will refine per-method extraction; this report
is descriptive measurement, not replication claims.

Usage:
    python -m ms408.benchmark
"""

from __future__ import annotations

import json
import statistics
from datetime import UTC, datetime
from pathlib import Path

from .dataset import git_commit
from .h4 import H4_OUT
from .harness.naibbe import NaibbeCipher, NaibbeConfig, NaibbeTables
from .harness.selfcitation import SEED_LINE_B, SelfCitationConfig, SelfCitationGenerator
from .ivtff import IVTFFDocument, TextPolicy
from .sources import path_for
from .textstats import summarize

ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results" / "harness"
REPORTS_DIR = ROOT / "reports"

H1_POLICY = TextPolicy(drop_uncertain_words=True)
H2_SEED = 408
H3_SEEDS = (19, 7, 42, 101, 555)


def _clean_h1(words: list) -> list:
    return [w for w in words if "@" not in w]


def h1_corpora() -> dict:
    zl = IVTFFDocument.load(path_for("zl"))
    corpora = {}
    all_words, a_words, b_words = [], [], []
    for page in zl.pages:
        page_words = _clean_h1(
            [w for locus in page.loci for w in locus.words(H1_POLICY)]
        )
        all_words.extend(page_words)
        if page.currier_language == "A":
            a_words.extend(page_words)
        elif page.currier_language == "B":
            b_words.extend(page_words)
    corpora["h1_zl_eva"] = ("H1", "ZL3b EVA, all pages", all_words)
    corpora["h1_zl_eva_currierA"] = ("H1", "ZL3b EVA, Currier A pages", a_words)
    corpora["h1_zl_eva_currierB"] = ("H1", "ZL3b EVA, Currier B pages", b_words)
    gc = IVTFFDocument.load(path_for("gc"))
    gc_words = _clean_h1([w for locus in gc.loci for w in locus.words(H1_POLICY)])
    corpora["h1_gc_v101"] = ("H1", "GC v101 (sensitivity transliteration)", gc_words)
    return corpora


def h2_corpora() -> dict:
    tables = NaibbeTables.load()
    corpora = {}
    for source_name in ("naibbe_pliny", "naibbe_dante"):
        lines = path_for(source_name).read_text(encoding="utf-8").splitlines()
        for deck in ("52", "78"):
            cipher = NaibbeCipher(tables, NaibbeConfig(deck=deck), seed=H2_SEED)
            result = cipher.encrypt_text(lines)
            words = [w for line in result.ciphertext_lines for w in line.split()]
            plaintext = "Pliny (Latin)" if "pliny" in source_name else "Dante (Italian)"
            corpora[f"h2_naibbe_{source_name.split('_')[1]}_deck{deck}"] = (
                "H2",
                f"Naibbe v2, {plaintext}, {deck}-card deck, seed {H2_SEED}",
                words,
            )
    return corpora


def h3_corpora() -> dict:
    corpora = {}
    for seed in H3_SEEDS:
        generated = SelfCitationGenerator(
            SelfCitationConfig(initial_line=SEED_LINE_B), seed=seed
        ).generate()
        words = [w for line in generated.lines for w in line]
        corpora[f"h3_selfcitation_B_seed{seed}"] = (
            "H3",
            f"Self-citation, Currier B preset, seed {seed}, 1200 lines",
            words,
        )
    reference = [
        w
        for line in path_for("timm_reference_output").read_text().splitlines()
        if line.strip() and not line.startswith("#")
        for w in line.split()
    ]
    corpora["h3_author_reference"] = (
        "H3",
        "Timm & Schinner committed reference output (Java, seed 19)",
        reference,
    )
    return corpora


def h4_corpora() -> dict:
    manifest = json.loads((H4_OUT / "manifest.json").read_text())
    corpora = {}
    for key, info in manifest["texts"].items():
        words = (H4_OUT / f"{key}.txt").read_text(encoding="utf-8").split()
        description = (
            f"{info['language']}, {info['genre']}, {info['period']}, "
            f"{info['edition']} edition, {info['form']}"
        )
        corpora[f"h4_{key}"] = ("H4", description, words)
    return corpora


def _h3_aggregate(results: dict) -> dict:
    ours = [
        results[name]["metrics"]
        for name in results
        if name.startswith("h3_selfcitation")
    ]
    aggregate = {}
    for metric in ("tokens", "types", "mean_word_length", "h1", "h2",
                   "zipf_slope", "abbreviation_rho"):
        values = [m[metric] for m in ours if m[metric] is not None]
        aggregate[metric] = {
            "mean": round(statistics.mean(values), 4),
            "stdev": round(statistics.stdev(values), 4) if len(values) > 1 else 0.0,
        }
    aggregate["reference"] = {
        metric: results["h3_author_reference"]["metrics"][metric]
        for metric in ("tokens", "types", "mean_word_length", "h1", "h2",
                       "zipf_slope", "abbreviation_rho")
    }
    return aggregate


def run() -> dict:
    corpora: dict = {}
    for loader in (h1_corpora, h2_corpora, h3_corpora, h4_corpora):
        corpora.update(loader())

    results = {
        name: {"class": cls, "description": description, "metrics": summarize(words)}
        for name, (cls, description, words) in corpora.items()
    }
    benchmark = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "policies": {
            "h1_words": "EVA default TextPolicy + drop_uncertain_words; words containing "
            "'@' escapes removed; all locus types included",
            "entropy_method": "within-word character bigrams (Lindemann-Bowern style)",
            "zipf_fit": "log-log least squares, ranks 10-1000",
            "h2_seed": H2_SEED,
            "h3_seeds": list(H3_SEEDS),
        },
        "corpora": results,
        "h3_multiseed_vs_reference": _h3_aggregate(results),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "harness_benchmark.md").write_text(_render_report(benchmark))
    return benchmark


def _render_report(benchmark: dict) -> str:
    lines = [
        "# Validation Harness Benchmark Report (T0.3)",
        "",
        f"Generated {benchmark['built_at']} at commit `{benchmark['git_commit'][:10]}` "
        "by `python -m ms408.benchmark` (deterministic; machine-readable version: "
        "`results/harness/benchmark.json`).",
        "",
        "All numbers are direct measurements by versioned code on pinned inputs "
        "(L3). Comparative claims against *published* values are deferred to the "
        "T1.1 replication gate; the H2/H3 generator-fidelity evidence is in the "
        "module test suites and the spec §17 notes.",
        "",
        "| corpus | class | tokens | types | mean len | h1 | h2 | zipf | abbrev ρ |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for name, entry in benchmark["corpora"].items():
        m = entry["metrics"]
        lines.append(
            f"| {name} | {entry['class']} | {m['tokens']:,} | {m['types']:,} "
            f"| {m['mean_word_length']:.2f} | {m['h1']:.3f} | {m['h2']:.3f} "
            f"| {m['zipf_slope'] if m['zipf_slope'] is not None else '—'} "
            f"| {m['abbreviation_rho']:.3f} |"
        )
    agg = benchmark["h3_multiseed_vs_reference"]
    lines += [
        "",
        "## H3 multi-seed vs. author reference",
        "",
        "| metric | ours (5-seed mean ± sd) | author (Java, seed 19) |",
        "|---|---|---|",
    ]
    for metric, stats_block in agg.items():
        if metric == "reference":
            continue
        ref = agg["reference"][metric]
        lines.append(
            f"| {metric} | {stats_block['mean']} ± {stats_block['stdev']} | {ref} |"
        )
    lines += [
        "",
        "## Notes",
        "",
        "- **Gate rule (RESEARCH-PLAN §3):** techniques claiming meaning-detection or "
        "structure-recovery must discriminate/recover correctly on H2/H3/H4 before "
        "their H1 results are admissible. This report establishes the corpus classes "
        "and their baseline statistics; discriminator scoring builds on it.",
        "- H1 policy, entropy method, and Zipf fit range are recorded in the JSON "
        "`policies` block; change them only alongside a version bump of this report.",
        "- H4 registers expose the edition confound (diplomatic vs. critical, "
        "consonantal vs. pointed) — compare like with like, per the `edition` tag.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    result = run()
    print(f"{len(result['corpora'])} corpora benchmarked -> "
          f"{RESULTS_DIR / 'benchmark.json'}")
