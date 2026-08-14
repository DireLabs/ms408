"""Audit results/experiments/*.json for embedded third-party text (D22, L19).

The per-experiment result tier was excluded wholesale by `.gitignore`, so none of it
reached the release and ~18 shipped reports cited files an outside reader could not open.
Excluding third-party *corpora* is correct L19 practice; excluding derived *metric* JSONs
that contain no third-party text is over-broad. This script decides which is which, so the
call is auditable instead of eyeballed.

What counts as third-party text here — note the first one is easy to forget:

  * the VMS transliterations themselves (ZL / GC / v101 ...). They are other people's
    work, consumed under L19. A JSON that lists VMS word types redistributes a slice of
    the transliteration, however "derived" the surrounding analysis is.
  * the Naibbe cipher corpus (Greshko 2025) — plaintext, ciphertext, and key tables.
  * the H4 natural-language corpora (Vulgate, Decameron, ...). These cannot be checked
    directly on a machine that has not built H4, so their absence from this audit is
    reported rather than assumed away.

Method: every string leaf in the JSON is checked against the acquired corpora's vocabulary.
Provenance strings (script names, git commits, method descriptions, prose captions) are
English and structurally distinct from corpus tokens, so the test is deliberately narrow —
it asks whether a string is *made of corpus tokens*, not whether it merely mentions one.

Usage:
    python scripts/audit_results_tier.py            # human-readable table
    python scripts/audit_results_tier.py --json     # machine-readable, for CI
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "experiments"

# Two distinct redistribution risks, detected separately:
#
#   1. RUNNING TEXT — a string leaf that is mostly corpus tokens. Judged only from 3 tokens
#      up, and only counting tokens of >=3 characters. Without those floors the test fires
#      on provenance strings: "A", "C", "4" and short English words like "note" or "scale"
#      are all legitimately in the VMS/Naibbe vocabularies, and matching one proves nothing.
#   2. VOCABULARY SLICE — a string COLLECTION (array, or a dict's key set) with enough
#      distinct corpus types in it to constitute a redistributed word list. A metrics JSON
#      keyed by VMS word type is still a slice of someone else's transliteration.
MIN_TOKENS_TO_JUDGE = 3
MIN_TOKEN_CHARS = 3
CORPUS_HIT_RATE = 0.80
MIN_COLLECTION_TYPES = 20


def _vms_vocab() -> tuple[set, str]:
    """Word types from the acquired VMS transliterations, or an empty set if unacquired."""
    try:
        from ms408.ivtff import IVTFFDocument, TextPolicy
        from ms408.sources import path_for
    except ImportError:  # pragma: no cover - the package is always importable in-repo
        return set(), "ms408 not importable"
    vocab, seen = set(), []
    for name in ("zl", "gc"):
        p = path_for(name)
        if not p.exists():
            continue
        doc = IVTFFDocument.load(p)
        vocab |= {
            w for page in doc.pages for locus in page.loci
            for w in locus.words(TextPolicy(drop_uncertain_words=True))
        }
        seen.append(name)
    return vocab, ("+".join(seen) if seen else "none acquired")


def _naibbe_vocab() -> tuple[set, str]:
    try:
        from ms408.sources import path_for
    except ImportError:  # pragma: no cover
        return set(), "ms408 not importable"
    vocab, seen = set(), []
    for name in ("naibbe_nathist_ciphertext", "naibbe_nathist_decrypted",
                 "naibbe_pliny", "naibbe_dante"):
        p = path_for(name)
        if not p.exists():
            continue
        vocab |= set(p.read_text(errors="ignore").split())
        seen.append(name)
    return vocab, (f"{len(seen)} file(s)" if seen else "none acquired")


def _leaves(obj, path="") -> list:
    """Every string leaf with its JSON path."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out += _leaves(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _leaves(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        out.append((path, obj))
    return out


def _collections(obj, path="") -> list:
    """Every string COLLECTION: a list of strings, or a dict's key set, with its path."""
    out = []
    if isinstance(obj, dict):
        keys = [k for k in obj if isinstance(k, str)]
        if keys:
            out.append((f"{path} (keys)" if path else "(top-level keys)", keys))
        for k, v in obj.items():
            out += _collections(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        strs = [v for v in obj if isinstance(v, str)]
        if strs:
            out.append((path, strs))
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                out += _collections(v, f"{path}[{i}]")
    return out


def audit_file(path: Path, vocabs: dict) -> dict:
    data = json.loads(path.read_text())
    findings = []

    # 1. running text in a string leaf
    for jpath, s in _leaves(data):
        toks = [t for t in s.split() if len(t) >= MIN_TOKEN_CHARS]
        if len(toks) < MIN_TOKENS_TO_JUDGE:
            continue
        for corpus, vocab in vocabs.items():
            if not vocab:
                continue
            hits = sum(1 for t in toks if t in vocab)
            if hits / len(toks) >= CORPUS_HIT_RATE:
                findings.append({"kind": "running_text", "corpus": corpus,
                                 "json_path": jpath, "tokens": len(toks),
                                 "hit_rate": round(hits / len(toks), 3),
                                 "sample": s[:60]})
                break

    # 2. a redistributed vocabulary slice
    for jpath, strs in _collections(data):
        cand = {s for s in strs if len(s) >= MIN_TOKEN_CHARS and " " not in s}
        if len(cand) < MIN_COLLECTION_TYPES:
            continue
        for corpus, vocab in vocabs.items():
            if not vocab:
                continue
            hits = cand & vocab
            if len(hits) >= MIN_COLLECTION_TYPES and len(hits) / len(cand) >= CORPUS_HIT_RATE:
                findings.append({"kind": "vocabulary_slice", "corpus": corpus,
                                 "json_path": jpath, "tokens": len(hits),
                                 "hit_rate": round(len(hits) / len(cand), 3),
                                 "sample": ", ".join(sorted(hits)[:6])})
                break
    by_corpus: dict = {}
    for f in findings:
        by_corpus.setdefault(f["corpus"], []).append(f)
    return {
        "file": path.name,
        "bytes": path.stat().st_size,
        "verdict": "CONTAINS_CORPUS_TEXT" if findings else "METRICS_ONLY",
        "n_findings": len(findings),
        "by_corpus": {c: len(v) for c, v in by_corpus.items()},
        "examples": findings[:5],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    vms, vms_src = _vms_vocab()
    naibbe, naibbe_src = _naibbe_vocab()
    vocabs = {"vms_transliteration": vms, "naibbe": naibbe}

    files = sorted(RESULTS.glob("*.json"))
    audits = [audit_file(p, vocabs) for p in files]
    report = {
        "results_dir": str(RESULTS.relative_to(ROOT)),
        "n_files": len(files),
        "vocabularies": {
            "vms_transliteration": {"source": vms_src, "types": len(vms)},
            "naibbe": {"source": naibbe_src, "types": len(naibbe)},
            "h4_natural_language": {
                "source": "NOT CHECKED — H4 corpora are not fetchable by ms408.acquire",
                "types": 0,
            },
        },
        "params": {"corpus_hit_rate": CORPUS_HIT_RATE,
                   "min_tokens_to_judge": MIN_TOKENS_TO_JUDGE},
        "metrics_only": [a["file"] for a in audits if a["verdict"] == "METRICS_ONLY"],
        "contains_corpus_text": [a["file"] for a in audits
                                 if a["verdict"] == "CONTAINS_CORPUS_TEXT"],
        "audits": audits,
    }
    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"{len(files)} result file(s) in {report['results_dir']}")
    for k, v in report["vocabularies"].items():
        print(f"  vocab {k:<22} {v['types']:>6} types   ({v['source']})")
    print()
    for a in audits:
        tag = "TEXT" if a["verdict"] == "CONTAINS_CORPUS_TEXT" else "ok  "
        extra = f"  {a['by_corpus']}" if a["n_findings"] else ""
        print(f"  [{tag}] {a['file']:<46} {a['bytes']:>9,}b{extra}")
        for ex in a["examples"][:2]:
            print(f"           {ex['json_path'][:56]} :: {ex['sample']!r}")
    print(f"\nmetrics-only: {len(report['metrics_only'])}   "
          f"contains corpus text: {len(report['contains_corpus_text'])}")
    print("\nH4 natural-language corpora were NOT checked (not fetchable). Any file whose "
          "generating experiment reads H4 must be treated as unaudited.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
