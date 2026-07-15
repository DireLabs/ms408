"""E18 — Corpus completeness: missing folios and vocabulary growth (i06/known-issue).

How much of MS 408 is missing, and how much would the missing material have added? Two
firewall-clean measures from the transliteration itself:

1. FOLIATION GAPS. The manuscript is foliated f1..f116 in a later hand. We count which
   folio numbers survive in the transliteration and which are missing within that
   range — a lower bound on loss (it cannot detect folios lost before, or beyond, the
   numbering). We do have the end (f116), so the range is anchored.
2. VOCABULARY GROWTH. Heaps' law exponent β for cumulative types vs tokens in folio
   order, plus the per-page fraction of first-occurrence (new) word types. A high β and
   a still-high new-type rate at the end mean the text was NOT lexically saturating, so
   the missing folios likely held substantial UNSEEN vocabulary — which compounds the
   intrinsic sparsity (high TTR / many rare words) that limits lexical statistics.

Usage:
    python -m ms408.experiments.e18_corpus_completeness
"""

from __future__ import annotations

import json
import math
import re
import statistics
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..ivtff import IVTFFDocument
from ..sources import path_for
from ..studies.anchor_hunt import WORD_POLICY

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "experiments"


def run() -> dict:
    zl = IVTFFDocument.load(path_for("zl"))
    folnums = set()
    pages = []
    for p in zl.pages:
        m = re.match(r"f(\d+)", p.name)
        if m:
            folnums.add(int(m.group(1)))
        toks = [w for loc in p.loci if (loc.locus_type or "").startswith("P")
                for w in loc.words(WORD_POLICY) if "@" not in w]
        if toks:
            pages.append((p.name, toks))

    present = sorted(folnums)
    lo, hi = present[0], present[-1]
    missing = sorted(set(range(lo, hi + 1)) - folnums)

    # vocabulary growth in folio order
    seen: set = set()
    cum_tok = 0
    novelty = []
    xs, ys = [], []
    for name, toks in pages:
        new = sum(1 for w in toks if w not in seen)
        seen.update(toks)
        cum_tok += len(toks)
        novelty.append(round(new / len(toks), 3))
        xs.append(math.log(cum_tok))
        ys.append(math.log(len(seen)))
    mx, my = statistics.mean(xs), statistics.mean(ys)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    q = len(novelty) // 4

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E18 — corpus completeness (missing folios + vocabulary growth)",
        "foliation": {
            "pages_sides_present": len(pages), "folios_present": len(present),
            "range": f"f{lo}-f{hi}", "missing_folio_numbers_in_range": missing,
            "n_missing_in_range": len(missing),
            "surviving_fraction_of_foliated_range": round(len(present) / hi, 3),
            "note": "lower bound on loss; end (f116) is present so range is anchored; "
                    "cannot detect folios lost before/after the foliation"},
        "vocabulary_growth": {
            "total_tokens": cum_tok, "total_types": len(seen),
            "type_token_ratio": round(len(seen) / cum_tok, 3),
            "heaps_beta": round(beta, 3),
            "mean_new_type_fraction_first_quartile": round(statistics.mean(novelty[:q]), 3),
            "mean_new_type_fraction_last_quartile": round(statistics.mean(novelty[-q:]), 3),
            "interpretation": "beta~0.73 and ~20% new types/page even in the last "
                              "quartile => NOT lexically saturating => the ~12% missing "
                              "folios likely held substantial unseen vocabulary; the "
                              "high vocabulary richness + incompleteness compound the "
                              "sparsity that limits lexical/anchor statistics"},
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e18_corpus_completeness.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


if __name__ == "__main__":
    r = run()
    f, v = r["foliation"], r["vocabulary_growth"]
    print(f"Foliation: {f['folios_present']} folios present, range {f['range']}; "
          f"{f['n_missing_in_range']} missing in range {f['missing_folio_numbers_in_range']}")
    print(f"  surviving {f['surviving_fraction_of_foliated_range']:.0%} of the foliated range")
    print(f"Vocabulary: {v['total_tokens']} tokens, {v['total_types']} types, "
          f"TTR {v['type_token_ratio']}, Heaps beta {v['heaps_beta']}")
    print(f"  new-type/page: first quartile {v['mean_new_type_fraction_first_quartile']}, "
          f"last quartile {v['mean_new_type_fraction_last_quartile']}")
