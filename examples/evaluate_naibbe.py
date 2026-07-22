"""Worked example — run Greshko's Naibbe cipher through the MS408 evaluator.

The Naibbe cipher (Greshko 2025, Cryptologia, doi:10.1080/01611194.2025.2566408;
github.com/greshko/naibbe-cipher) is a verbose homophonic substitution that respaces Latin
into Voynichese-like ciphertext. It is the sharpest real test of the evaluator, and it
teaches the tool's single most important discipline: **an out-of-band result is not, by
itself, exclusion** — you have to know which axes are informative.

Run:
    python -m ms408.acquire                 # fetch pinned Naibbe data (consume-only, L19)
    python examples/evaluate_naibbe.py

What you'll see: the published ciphertext lands 0/3 on the hard axes (its morphology
network `ed1` is far denser than the manuscript's, and its word-order information `dI` has
collapsed). The naive read is "0/3 → excluded." That read is WRONG, and E29 is why:
  * `dI` is a confounded axis. The collapse is mostly Greshko's *respacing*, applied to the
    plaintext BEFORE the cipher — the word-boundary Latin `dI` sits inside the VMS band. An
    out-of-band `dI` here is an artifact, not evidence.
  * On the deconfounded mid-level syntax axes (the load-bearing ones, E30/E31),
    verbose+homophonic ciphers are NOT robustly separable from the manuscript. So this cipher
    family is *inconclusive* — neither reproduced nor excluded — converging with Greshko.
The `ed1` mismatch reflects THIS cipher's particular homophone tables, not a property every
verbose-homophonic cipher must have.

This example is why the evaluator counts only hard axes, flags `dI` confounded, and prints
"necessary, not sufficient" on every verdict.
"""

from __future__ import annotations

import json
import random

from ms408 import evaluate
from ms408.signature import BLOCK, format_verdict
from ms408.sources import RAW_ROOT, path_for

ROOT = RAW_ROOT.parents[1]   # data/raw -> data -> repo root

N_TOKENS = 10_000   # match the VMS reference-band token budget for a fair comparison
SEED = 408


def _matched_sample(tokens: list) -> list:
    """Deterministic block sample to the VMS token budget (h2/ed1/zipf and especially the
    token-sensitive ttr are only comparable at a similar budget)."""
    nb = len(tokens) // BLOCK
    need = N_TOKENS // BLOCK
    if nb <= need:
        return tokens[:N_TOKENS]
    keep = sorted(random.Random(SEED).sample(range(nb), need))
    return [tokens[j] for i in keep for j in range(i * BLOCK, (i + 1) * BLOCK)][:N_TOKENS]


def _e29_decomposition() -> dict | None:
    """Dereference the recorded E29 result (firewall: quote results/, don't recall numbers).
    Gitignored, so absent on a fresh clone — then we point at the committed report."""
    p = ROOT / "results" / "experiments" / "e29_naibbe_discriminators.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    return {"dI_decomposition": d.get("dI_decomposition"),
            "respacing_share": d.get("respacing_share_of_dI_loss"),
            "grade": d.get("grade")}


def main() -> int:
    try:
        ciphertext = path_for("naibbe_nathist_ciphertext").read_text().split()
    except FileNotFoundError:
        print("Naibbe ciphertext not acquired. Fetch it (consume-only, L19) with:\n"
              "    python -m ms408.acquire\n"
              "It clones pinned files from github.com/greshko/naibbe-cipher into data/raw/.")
        return 1

    sample = _matched_sample(ciphertext)
    print(f"Naibbe ciphertext: {len(ciphertext):,} tokens; "
          f"evaluating a matched {len(sample):,}-token sample.\n")
    verdict = evaluate(sample)
    print(format_verdict(verdict))

    print("\n" + "=" * 74)
    print("READING THIS HONESTLY (see docs/LIMITS.md, reports/e29_naibbe_discriminators.md):")
    print("- 0/3 hard is NOT 'cipher excluded'. dI is a CONFOUNDED axis; its collapse here is")
    print("  mostly Greshko's respacing of the plaintext, applied before the cipher.")
    d = _e29_decomposition()
    if d and d.get("dI_decomposition"):
        wb = d["dI_decomposition"].get("word_boundary_latin", {})
        print(f"  E29 (results/): word-boundary Latin dI = {wb.get('dI')} "
              f"(in VMS band: {wb.get('in_vms_band')}); "
              f"respacing accounts for {d['respacing_share']:.0%} of the dI loss. Grade {d['grade']}.")
    else:
        print("  (Run E29 for the exact decomposition: "
              "python -m ms408.experiments.e29_naibbe_discriminators)")
    print("- On the DECONFOUNDED syntax axes (E30/E31), verbose+homophonic ciphers are not")
    print("  robustly separable from the VMS -> this cipher family is INCONCLUSIVE, not excluded.")
    print("- The ed1 mismatch is THIS cipher's homophone tables, not a law of the class.")
    print("\nCitation: Greshko (2025), 'The Naibbe cipher', Cryptologia, "
          "doi:10.1080/01611194.2025.2566408.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
