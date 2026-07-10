"""Null-model correction framework for i05 mid-level probes.

The i05 probes (E13/E13b/E15) each computed a raw statistic that turned out to be
confounded by a nuisance parameter (type-token ratio, sample size, number of stems),
so raw values were not comparable across corpora. The fix, identical in every case:
express the observed statistic as a z-score against an ensemble of NULL replicates that
share the corpus's own nuisance parameters but lack the linguistic signal. The z is
then nuisance-controlled BY CONSTRUCTION — each corpus is compared to its own matched
null — so z-scores ARE comparable across corpora (and VMS-A vs VMS-B directly).

This module provides the z utility and the reusable order-shuffle null. Probe-specific
nulls (e.g. random morpheme-signature assignment) live with their probes.
"""

from __future__ import annotations

import random
import statistics


def null_z(observed: float, null_values: list) -> dict:
    """Observed statistic as a z-score + percentile against a null ensemble."""
    vals = [v for v in null_values if v is not None]
    if not vals:
        return {"observed": observed, "z": None, "percentile": None,
                "null_mean": None, "null_std": None, "n_null": 0}
    m = statistics.mean(vals)
    s = statistics.pstdev(vals)
    z = (observed - m) / s if s else 0.0
    pct = sum(1 for v in vals if v <= observed) / len(vals)
    return {"observed": round(observed, 4), "null_mean": round(m, 4),
            "null_std": round(s, 4), "z": round(z, 2), "percentile": round(pct, 3),
            "n_null": len(vals)}


def order_shuffle(tokens: list, seed: int) -> list:
    """Permute token ORDER while preserving the exact word-type multiset (so
    frequency, vocabulary, and type-token ratio are held fixed). Destroys all
    collocational / positional structure. The clean null for order-based measures."""
    t = list(tokens)
    random.Random(seed).shuffle(t)
    return t
