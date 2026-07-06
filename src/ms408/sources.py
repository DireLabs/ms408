"""Pinned registry of external sources (T0.2).

Every external file the pipeline consumes is pinned here by exact URL and sha256.
Files land in data/raw/ (gitignored — consume-only per L19); SOURCES.md in
docs/planning/i01/ documents provenance and licensing for each.

Upstream files version-bump in place (e.g. ZL3a -> ZL3b), so a checksum mismatch
on re-download means the source moved: re-verify, then re-pin deliberately.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    dest: str  # path relative to data/raw/
    sha256: str
    notes: str


NAIBBE_COMMIT = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
_NAIBBE_NOTES = (
    "Greshko naibbe-cipher repo @ {} — modified MIT: publications using this must cite "
    "Greshko 2025, doi:10.1080/01611194.2025.2566408 (spec T03-naibbe §2).".format(
        NAIBBE_COMMIT[:7]
    )
)


def _naibbe_sources() -> list[Source]:
    files = [
        ("naibbe_tables", "references/naibbe_tables.csv",
         "4e7cfd54b7ec66515d39a51e11ec97e8e19b643b0b189124eebc3982e707dcec"),
        ("naibbe_nathist_ciphertext", "encrypted/nathist_output_ciphertext.txt",
         "9cdf2de12f371ac7efdb2e78713f229ada508286c1717758184238a59cd64326"),
        ("naibbe_nathist_decrypted", "decrypted/nathist_output_ciphertext_decrypted.txt",
         "852d1ad67f82d6472c8ef1d99bfa12c62f76f3d37be2623a131f47232b753ca2"),
        ("naibbe_nathist_respaced", "respaced_plaintext/nathist_pre_encryption_respaced_plaintext.txt",
         "4979b6826c75dd47b90d6c95ac212a34cd3735b1151ca2a524e9d13b4112e93b"),
        ("naibbe_pliny", "input/examples/nathist_book16.txt",
         "957909f4982f7ff723dfaaf456678f0a131b844a5c2a8130d8ec75a8740397db"),
        ("naibbe_dante", "input/examples/divina_commedia.txt",
         "aafa15bbc0644dac7680ce3d0e4494b99775fbc83394cb7ad88145a0f8d6b31e"),
    ]
    return [
        Source(
            name=name,
            url=f"https://raw.githubusercontent.com/greshko/naibbe-cipher/{NAIBBE_COMMIT}/{rel}",
            dest=f"naibbe-cipher/{rel}",
            sha256=digest,
            notes=_NAIBBE_NOTES,
        )
        for name, rel, digest in files
    ]


TIMM_COMMIT = "a6ede2202dd7ad6285ce2c007bf22c2a0e7709b7"
_TIMM_NOTES = (
    "Timm SelfCitationTextgenerator repo @ {} — MIT (c) 2019 Torsten Timm. Cite Timm & "
    "Schinner 2020 doi:10.1080/01611194.2019.1596999 + Zenodo 10.5281/zenodo.2531632 "
    "(spec T03-selfcitation §13).".format(TIMM_COMMIT[:7])
)


def _timm_sources() -> list[Source]:
    files = [
        ("timm_reference_output", "executable/generate/generated_text.txt",
         "1e954a17b157e83f04ea21353ba877f70084b828b812fab3944347ac2888dc11"),
        ("timm_conf", "executable/conf.properties",
         "308af498cd5da6957e7f9d06e01efff0273856d7f59d5e15205edae86f9061ee"),
        ("timm_license", "LICENSE",
         "3621db279bfbb241057694d91c22895b4c5210e3c161ecef89c8402d091eb029"),
    ]
    return [
        Source(
            name=name,
            url="https://raw.githubusercontent.com/TorstenTimm/SelfCitationTextgenerator/"
            f"{TIMM_COMMIT}/{rel}",
            dest=f"timm-selfcitation/{Path(rel).name}",
            sha256=digest,
            notes=_TIMM_NOTES,
        )
        for name, rel, digest in files
    ]


SOURCES: dict[str, Source] = {
    s.name: s
    for s in [
        Source(
            name="zl",
            url="https://www.voynich.nu/data/ZL3b-n.txt",
            dest="transliterations/ZL3b-n.txt",
            sha256="bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
            notes="Zandbergen-Landini EVA, v3b 2025-05-13. Primary corpus (L11). "
            "Complete: 227 pages, 5389 loci, $I/$L/$H/$C metadata in page headers.",
        ),
        Source(
            name="gc",
            url="https://www.voynich.nu/data/GC2a-n.txt",
            dest="transliterations/GC2a-n.txt",
            sha256="b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f",
            notes="Claston v101 in IVTFF form. Sensitivity corpus (L11). "
            "High-ASCII glyphs escaped as @nnn;.",
        ),
        Source(
            name="v101_original",
            url="https://www.voynich.nu/data/voyn_101.txt",
            dest="transliterations/voyn_101.txt",
            sha256="f278a451d873c520f7ab509c4af12152698a1d3efd2353924e177a565c17ba7e",
            notes="Claston's original v101 file (provenance reference; cp1252-style "
            "high-ASCII bytes, non-IVTFF record format).",
        ),
        Source(
            name="rf",
            url="https://www.voynich.nu/data/RF1b-e.txt",
            dest="transliterations/RF1b-e.txt",
            sha256="e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782",
            notes="Reference transliteration (extended EVA, combines ZL+GC). Cross-check only.",
        ),
        Source(
            name="it",
            url="https://www.voynich.nu/data/IT2a-n.txt",
            dest="transliterations/IT2a-n.txt",
            sha256="7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
            notes="Takahashi transcription in IVTFF (EvaT). T1.1 like-for-like corpus for the "
            "Lindemann-Bowern entropy targets (they used Takahashi via the LSI interlinear).",
        ),
        Source(
            name="ivtff_spec",
            url="https://www.voynich.nu/software/ivtt/IVTFF_format.pdf",
            dest="specs/IVTFF_format.pdf",
            sha256="7ac9c4a82064763cac8767cca6f661cc4e1b4503ab9342acc03032ddb6939d49",
            notes="IVTFF format spec v2.0.1 (doc issue 2.0.2, 2025-07-08).",
        ),
        *_naibbe_sources(),
        *_timm_sources(),
    ]
}

RAW_ROOT = Path(__file__).resolve().parents[2] / "data" / "raw"


def path_for(name: str) -> Path:
    """Absolute path where a registered source lives locally."""
    return RAW_ROOT / SOURCES[name].dest
