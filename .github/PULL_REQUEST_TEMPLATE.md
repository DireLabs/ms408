<!-- Thanks for contributing. This project runs on a firewall discipline (see CONTRIBUTING.md);
the checklist below is that discipline at the door. -->

## What this PR does

<!-- one or two sentences -->

## Discipline checklist

- [ ] **Firewall:** every reported number is produced by deterministic, versioned code
      writing to `results/` — none hand-entered, estimated, or recalled.
- [ ] **Determinism:** fixed seeds; no wall-clock/randomness in reported computations. The
      result reproduces from committed code + acquired data.
- [ ] **Evidence grade:** any empirical claim states its grade (A–D). I have not raised a
      grade to make a result look stronger.
- [ ] **No decipherment / meaning claims (L7).** This PR makes no plaintext/meaning/symbol-value
      claim; "matches the manuscript" is treated as necessary, not sufficient.
- [ ] **Data (L19):** no third-party corpora committed; any new source is added to
      `ms408.sources` pinned by URL + sha256 + licence note.
- [ ] **Tests:** added/updated. If I changed a reported number or an axis definition, I
      rebuilt the reference bands and re-pinned `tests/test_verify.py`, and
      `python -m ms408.verify --full` passes.
- [ ] `ruff check src tests examples` and `pytest -q` pass locally.

## Adversarial check (for A/B-grade claims)

<!-- If this PR asserts a strong empirical claim, describe (or link) the clean-context
refutation it survived, per docs/METHODOLOGY.md. -->

## Notes / limitations

<!-- Be honest about what this does NOT establish. An accurately-scoped negative is welcome. -->
