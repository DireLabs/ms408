"""MS408 research program: corpus pipeline, validation harness, statistics.

All reported numbers must come from scripts in this package writing to results/ (L3 firewall).

Public evaluator entry point:

    from ms408 import evaluate
    verdict = evaluate(open("my_tokens.txt").read().split())

`evaluate(tokens)` scores a word-token stream against the Voynich manuscript's
discriminator bands and returns a per-axis verdict with each axis's honest caveat
attached. Matching is necessary, not sufficient (L7). See `ms408.signature` and
docs/LIMITS.md.
"""

from .signature import axis_values, evaluate, format_verdict, vms_bands

__all__ = ["evaluate", "axis_values", "vms_bands", "format_verdict"]
