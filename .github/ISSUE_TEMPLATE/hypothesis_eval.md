---
name: Hypothesis / evaluation question
about: A question about evaluating a hypothesis, or an unexpected verdict
title: "[eval] "
labels: question
---

**Your hypothesis**
<!-- e.g. "my generator output should match the manuscript" / "is this cipher scheme excluded?" -->

**What the evaluator reported**
<!-- paste the `python -m ms408 --json ...` verdict, or the hard/soft axis counts -->

**What's confusing / what you expected**
<!-- Remember: matching the bands is NECESSARY, not SUFFICIENT. Out-of-band on a CONFOUNDED
axis (dI, *_global) or an ADVISORY axis (ttr) is not exclusion — see docs/LIMITS.md and the
Naibbe worked example (examples/evaluate_naibbe.py). -->

**Token budget**
- Number of tokens evaluated (bands are built at 10,000; below ~8,000 axes aren't strictly comparable):
