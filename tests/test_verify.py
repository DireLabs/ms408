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

# The committed reference-band artifact, frozen — one block per Currier dialect (D21).
# Rebuild + `verify --full` if you change it. Currier A's numbers are unchanged from the
# pre-D21 pooled artifact, because that "A+B" sample was in fact A[:10000].
PINNED_POINT = {
    "A": {
        "tokens": 10000, "types": 3292, "h2": 2.1822, "dI": 0.1634, "ed1": 0.7509,
        "zipf": -1.0486, "ttr": 0.3292, "mz_peak_scale": 333,
        "fc_z_local": -1.54, "wc_z_local": 1.97, "fc_z_global": -1.19, "wc_z_global": 1.98,
    },
    "B": {
        "tokens": 10000, "types": 2470, "h2": 1.961, "dI": 0.1993, "ed1": 0.7725,
        "zipf": -1.2151, "ttr": 0.247, "mz_peak_scale": 277,
        "fc_z_local": -3.7, "wc_z_local": 1.59, "fc_z_global": -4.83, "wc_z_global": 2.92,
    },
}
# zipf and ttr are advisory (token-count-sensitive, D23): band is null in both dialects.
PINNED_BANDS = {
    "A": {
        "h2": [2.1595, 2.1972], "dI": [0.1435, 0.178], "ed1": [0.7374, 0.7619],
        "zipf": None, "ttr": None,
        "fc_z_local": [-4.51, 0.72], "wc_z_local": [-1.23, 2.56],
        "fc_z_global": [-4.65, 0.43], "wc_z_global": [-1.07, 2.93],
    },
    "B": {
        "h2": [1.9259, 1.996], "dI": [0.1815, 0.2122], "ed1": [0.754, 0.7878],
        "zipf": None, "ttr": None,
        "fc_z_local": [-3.87, -0.66], "wc_z_local": [-0.04, 4.13],
        "fc_z_global": [-5.74, -1.22], "wc_z_global": [0.29, 3.63],
    },
}


def test_shipped_bands_are_pinned():
    """Freeze the exact numbers the tool reports, per dialect (no corpus needed)."""
    bands = vms_bands()
    assert set(bands["dialects"]) == set(PINNED_POINT)
    for dialect, spec in bands["dialects"].items():
        assert spec["vms_point"] == PINNED_POINT[dialect], dialect
        assert {a: s["band"] for a, s in spec["axes"].items()} == PINNED_BANDS[dialect]


def test_shipped_bands_self_consistent():
    """Each dialect's hard bands contain its own point (a miscalibrated set would fail).

    This is the check that caught D23: with bands built per dialect, Currier B's zipf
    point fell outside B's own zipf band, which is why zipf is now advisory.
    """
    for dialect, spec in vms_bands()["dialects"].items():
        for axis in HARD_AXES:
            lo, hi = spec["axes"][axis]["band"]
            assert lo <= spec["vms_point"][axis] <= hi, f"{dialect}.{axis}"


def test_advisory_axes_are_unbanded_in_every_dialect():
    """ttr and zipf must ship unbanded: their subsample CI is biased off the point (D23)."""
    for dialect, spec in vms_bands()["dialects"].items():
        for axis in ("ttr", "zipf"):
            entry = spec["axes"][axis]
            assert entry["band"] is None, f"{dialect}.{axis}"
            assert entry["token_sensitive"] is True
            # the measured bias is carried so the demotion is auditable, not asserted
            assert "subsample_bias" in entry


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
    assert v["best_match"]["hard_axes_in_band"] == 0
    for dialect, block in v["dialects"].items():
        assert block["hard_axes_in_band"] == 0, dialect
        assert block["axes"]["dI"]["in_band"] is False
        assert block["axes"]["ed1"]["in_band"] is False
