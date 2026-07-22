# Examples

Runnable demonstrations of the evaluator. They need the acquired reference data
(`python -m ms408.acquire`, consume-only under L19).

- **`evaluate_naibbe.py`** — run Greshko's Naibbe cipher (2025) through `ms408.evaluate`.
  Teaches the tool's central discipline: the published ciphertext lands 0/3 on the hard
  axes, but that is **not** exclusion — its `dI` collapse is a respacing artifact on a
  confounded axis, and verbose+homophonic ciphers are not robustly separable from the
  manuscript on the deconfounded axes (E29/E30/E31). Cite Greshko 2025
  (doi:10.1080/01611194.2025.2566408) if you use the Naibbe data.

  ```bash
  python -m ms408.acquire
  python examples/evaluate_naibbe.py
  ```

To reproduce the numbers the evaluator ships (prove they come from code, not by hand):

```bash
python -m ms408.verify          # recompute the VMS point + self-consistency
python -m ms408.verify --full   # also rebuild the reference bands and diff (~1 min)
```
