"""CLI: evaluate a token stream against the VMS discriminator bands.

    python -m ms408 my_tokens.txt          # whitespace-separated word tokens
    python -m ms408 --json my_tokens.txt   # machine-readable verdict
    cat my_tokens.txt | python -m ms408 -  # read tokens from stdin

The verdict carries each axis's value, the VMS reference band, whether you land in it, and
the standing caveat for that axis. Matching is NECESSARY, not sufficient (L7): an in-band
result means your hypothesis is not excluded, not that it is the manuscript's mechanism.
"""

from __future__ import annotations

import argparse
import json
import sys

from .signature import evaluate, format_verdict


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="ms408",
        description="Evaluate a token stream against the Voynich discriminator bands.",
    )
    ap.add_argument("tokens", help="path to a whitespace-separated token file, or '-' for stdin")
    ap.add_argument("--json", action="store_true", help="emit the raw verdict as JSON")
    ap.add_argument("--seed", type=int, default=408, help="determinism seed (default 408)")
    args = ap.parse_args(argv)

    text = sys.stdin.read() if args.tokens == "-" else open(args.tokens, encoding="utf-8").read()
    tokens = text.split()
    if len(tokens) < 2:
        ap.error("need at least 2 whitespace-separated tokens")

    verdict = evaluate(tokens, seed=args.seed)
    if args.json:
        print(json.dumps(verdict, indent=2))
    else:
        print(format_verdict(verdict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
