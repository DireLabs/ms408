"""Value-pinning + reproducibility guards for the evaluator.

`test_shipped_bands_are_pinned` runs WITHOUT the corpus: it freezes the exact numbers the
tool reports, so any code change that silently shifts them fails CI. The reproduction and
worked-example checks are data-gated. If you deliberately rebuild the bands
(`python -m ms408.experiments.e32_reference_bands`), update the pinned block below AND
confirm `python -m ms408.verify --full` passes.
"""

from __future__ import annotations

import pytest

from ms408.signature import HARD_AXES, vms_bands
from ms408.sources import path_for
from ms408.verify import verify

needs_data = pytest.mark.skipif(
    not path_for("zl").exists(), reason="run `python -m ms408.acquire` first"
)
needs_naibbe = pytest.mark.skipif(
    not path_for("naibbe_nathist_ciphertext").exists(),
    reason="acquire the Naibbe example data first",
)

# The committed reference-band artifact, frozen. Rebuild + `verify --full` if you change it.
PINNED_POINT = {
    "tokens": 10000, "types": 3292, "h2": 2.1822, "dI": 0.1634, "ed1": 0.7509,
    "zipf": -1.0486, "ttr": 0.3292, "mz_peak_scale": 333,
    "fc_z_local": -1.54, "wc_z_local": 1.97, "fc_z_global": -1.19, "wc_z_global": 1.98,
}
PINNED_BANDS = {
    "h2": [2.1595, 2.1972], "dI": [0.1435, 0.178], "ed1": [0.7374, 0.7619],
    "zipf": [-1.0673, -1.0358], "ttr": None,
    "fc_z_local": [-4.51, 0.72], "wc_z_local": [-1.23, 2.56],
    "fc_z_global": [-4.65, 0.43], "wc_z_global": [-1.07, 2.93],
}


def test_shipped_bands_are_pinned():
    """Freeze the exact numbers the tool reports (no corpus needed)."""
    bands = vms_bands()
    assert bands["vms_point"] == PINNED_POINT
    assert {a: s["band"] for a, s in bands["axes"].items()} == PINNED_BANDS


def test_shipped_bands_self_consistent():
    """Each hard band contains the VMS point (a miscalibrated artifact would fail)."""
    bands = vms_bands()
    for axis in HARD_AXES:
        lo, hi = bands["axes"][axis]["band"]
        assert lo <= bands["vms_point"][axis] <= hi


@needs_data
def test_verify_reproduces_from_code():
    """The shipped VMS point must recompute from the corpus (the firewall, as a test)."""
    failed, checks = verify(full=False)
    assert failed == 0, [c for c in checks if c[1] is False]
    assert any(name.startswith("vms_point.") for name, _, _ in checks)


@needs_naibbe
def test_naibbe_example_headline_is_stable():
    """Pin the worked example's headline: the published Naibbe ciphertext is 0/3 hard, and
    its dI is out of band (the collapse the example explains as a respacing artifact)."""
    import importlib.util
    from pathlib import Path

    ex = Path(__file__).resolve().parents[1] / "examples" / "evaluate_naibbe.py"
    spec = importlib.util.spec_from_file_location("evaluate_naibbe_example", ex)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    from ms408 import evaluate

    ciphertext = path_for("naibbe_nathist_ciphertext").read_text().split()
    v = evaluate(mod._matched_sample(ciphertext))
    assert v["hard_axes_in_band"] == 0
    assert v["axes"]["dI"]["in_band"] is False
    assert v["axes"]["ed1"]["in_band"] is False
