"""Committed data artifacts shipped with the package (not third-party corpora).

Currently: ``reference_bands.json`` — the VMS discriminator reference bands, built by
``ms408.experiments.e32_reference_bands`` (it records its own git commit and params).
Third-party corpora are never shipped here; users fetch those with ``ms408.acquire`` into
gitignored ``data/raw/`` under the consume-only policy (L19).
"""
