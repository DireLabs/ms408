"""H4 control-corpus normalization (T0.3).

Extracts plain word streams from the raw H4 acquisitions (data/raw/h4/ — see
docs/planning/i01/specs/T03-h4-acquisition.md and data/raw/h4/MANIFEST.json for
provenance/licensing) into data/processed/h4/, one file per text and register,
plus a build manifest (L3 provenance).

The edition confound (SOURCES.md risk 3) is handled by *registers*, not hidden:
critical editions (Vulgate, Macer, Decameron) have expanded abbreviations; the
ReF transcriptions are diplomatic. German texts are therefore emitted twice —
`dipl` (UTF diplomatic: long s, superscripts preserved) and `ascii` (the corpus's
own ASCII simplification) — and Hebrew twice: `consonantal` (primary per D16
default) and `pointed`. Cross-register statistics must stratify by the manifest's
`edition` tag.

Output format: lowercase words separated by single spaces, 15 words per line.
Line breaks are non-semantic for H4 (only word order matters); characters outside
the language's letter inventory act as word separators.

Usage:
    python -m ms408.h4
"""

from __future__ import annotations

import json
import re
import tarfile
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

from .acquire import sha256_of
from .dataset import PROCESSED_ROOT, git_commit
from .sources import RAW_ROOT

H4_RAW = RAW_ROOT / "h4"
H4_OUT = PROCESSED_ROOT / "h4"
WORDS_PER_LINE = 15

REF_TAR = "german/ReF-v1.0.2.tar.gz"
REF_MEMBERS = {
    "F120": "./ReF-v1.0.2/ref-mlu/F120.xml",
    "F081": "./ReF-v1.0.2/ref-mlu/F081.xml",
    "F151": "./ReF-v1.0.2/ref-mlu/F151.xml",
    "F292": "./ReF-v1.0.2/ref-mlu/F292.xml",
    "F167": "./ReF-v1.0.2/ref-rub/F167.xml",
}
# Mishneh Torah books in canonical order (deterministic concatenation)
MISHNEH_FILES = [
    "hebrew/mishneh_torah_foundations_of_the_torah_torat_emet.json",
    "hebrew/mishneh_torah_human_dispositions_torat_emet.json",
    "hebrew/mishneh_torah_torah_study_torat_emet.json",
    "hebrew/mishneh_torah_foreign_worship_and_customs_of_the_nations_torat_emet.json",
    "hebrew/mishneh_torah_repentance_torat_emet.json",
    "hebrew/mishneh_torah_sabbath_torat_emet.json",
    "hebrew/mishneh_torah_forbidden_foods_torat_emet.json",
]

HEBREW_LETTERS = frozenset(chr(c) for c in range(0x05D0, 0x05EB))
HEBREW_MARKS = frozenset(chr(c) for c in range(0x0591, 0x05C8))


# ---------------------------------------------------------------------------
# Normalizers
# ---------------------------------------------------------------------------


def words_latinlike(text: str, keep_marks: bool = False) -> list:
    """Alphabetic characters (lowercased) form words; everything else separates.

    keep_marks preserves combining marks (diplomatic superscripts like u-ring);
    without it, marks are separators-stripped after NFC composition.
    """
    normalized = unicodedata.normalize("NFC", text)
    out = []
    for c in normalized:
        if c.isalpha():
            out.append(c.lower())
        elif keep_marks and unicodedata.category(c) == "Mn":
            out.append(c)
        else:
            out.append(" ")
    return "".join(out).split()


def words_hebrew(text: str, pointed: bool) -> list:
    text = re.sub(r"<[^>]+>", " ", text)  # stray HTML in Sefaria strings
    out = []
    for c in unicodedata.normalize("NFC", text):
        if c in HEBREW_LETTERS:
            out.append(c)
        elif c in HEBREW_MARKS:
            # marks are kept (pointed) or deleted (consonantal) — never separators,
            # or every nikud position would split its word apart
            if pointed:
                out.append(c)
        else:
            out.append(" ")
    return "".join(out).split()


def to_lines(words: list) -> str:
    lines = [
        " ".join(words[i : i + WORDS_PER_LINE]) for i in range(0, len(words), WORDS_PER_LINE)
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Extractors (raw file -> word list)
# ---------------------------------------------------------------------------


def extract_vulgate() -> list:
    xml = (H4_RAW / "latin/vulgate_bible-corpus_Latin.xml").read_text(encoding="utf-8")
    verses = re.findall(r"<seg id='[^']*' type='verse'>([^<]+)", xml)
    return words_latinlike(" ".join(verses))


def extract_macer() -> list:
    data = json.loads(
        (H4_RAW / "latin/macer_floridus_de_viribus_herbarum.wikitext.json").read_text()
    )
    wikitext = data["parse"]["wikitext"]
    if isinstance(wikitext, dict):
        wikitext = wikitext["*"]
    wikitext = re.sub(r"\{\{[^{}]*\}\}", " ", wikitext, flags=re.S)  # templates incl. {{Versus|n}}
    wikitext = re.sub(r"^==.*==\s*$", " ", wikitext, flags=re.M)  # chapter headings
    wikitext = re.sub(r"</?poem>", " ", wikitext)
    return words_latinlike(wikitext)


def extract_decameron() -> list:
    raw = (H4_RAW / "italian/boccaccio_decameron_branca.txt").read_bytes().decode("cp1252")
    lines = raw.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("COMINCIA IL LIBRO"))
    return words_latinlike("\n".join(lines[start:]))


_REF_CACHE: dict = {}


def _ref_tokens(sigle: str, register: str) -> list:
    """Token list from a ReF CorA-XML member; all members read in one tar pass."""
    if not _REF_CACHE:
        with tarfile.open(H4_RAW / REF_TAR) as tar:
            for name, member in REF_MEMBERS.items():
                root = ElementTree.parse(tar.extractfile(member)).getroot()
                _REF_CACHE[name] = {
                    "dipl": [el.get("utf", "") for el in root.iter("tok_dipl")],
                    "ascii": [el.get("ascii", "") for el in root.iter("tok_anno")],
                }
    return _REF_CACHE[sigle][register]


def extract_ref(sigle: str, register: str) -> list:
    tokens = _ref_tokens(sigle, register)
    return words_latinlike(" ".join(tokens), keep_marks=register == "dipl")


def _flatten(nested) -> list:
    if isinstance(nested, str):
        return [nested]
    out = []
    for item in nested:
        out.extend(_flatten(item))
    return out


def extract_mishneh(pointed: bool) -> list:
    words = []
    for rel in MISHNEH_FILES:
        data = json.loads((H4_RAW / rel).read_text())
        assert data.get("license") == "Public Domain", rel
        words.extend(words_hebrew(" ".join(_flatten(data["text"])), pointed=pointed))
    return words


# ---------------------------------------------------------------------------
# Registry and build
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class H4Text:
    key: str  # output filename stem
    language: str
    form: str  # prose | verse
    edition: str  # critical | diplomatic | diplomatic-ascii
    period: str
    genre: str
    sources: tuple  # raw files (relative to data/raw/h4) this output derives from
    extract: object  # () -> list[str]


def _ref_text(sigle: str, name: str, period: str, register: str) -> H4Text:
    return H4Text(
        key=f"german_{name}_{register}",
        language="german-enhg",
        form="prose",
        edition="diplomatic" if register == "dipl" else "diplomatic-ascii",
        period=period,
        genre="medical",
        sources=(REF_TAR,),
        extract=lambda: extract_ref(sigle, register),
    )


TEXTS = [
    H4Text("latin_vulgate", "latin", "prose", "critical", "4th c. (medieval transmission)",
           "scripture", ("latin/vulgate_bible-corpus_Latin.xml",), extract_vulgate),
    H4Text("latin_macer_floridus", "latin", "verse", "critical", "11th c.", "herbal",
           ("latin/macer_floridus_de_viribus_herbarum.wikitext.json",), extract_macer),
    H4Text("italian_decameron", "italian", "prose", "critical", "1349-1353", "narrative",
           ("italian/boccaccio_decameron_branca.txt",), extract_decameron),
    *[
        _ref_text(sigle, name, period, register)
        for sigle, name, period in [
            ("F120", "ulmer_wundarznei", "late 15th c."),
            ("F081", "feldbuch_wundarznei", "early 16th c."),
            ("F151", "arzneibuch", "early 17th c."),
            ("F292", "wundarznei", "early 16th c."),
            ("F167", "kraeuterbuch", "early 16th c."),
        ]
        for register in ("dipl", "ascii")
    ],
    H4Text("hebrew_mishneh_torah_consonantal", "hebrew", "prose", "critical", "1170-1180",
           "legal code", tuple(MISHNEH_FILES), lambda: extract_mishneh(pointed=False)),
    H4Text("hebrew_mishneh_torah_pointed", "hebrew", "prose", "critical", "1170-1180",
           "legal code", tuple(MISHNEH_FILES), lambda: extract_mishneh(pointed=True)),
]


def build(out_root: Path = H4_OUT) -> dict:
    out_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "words_per_line": WORDS_PER_LINE,
        "registers_note": (
            "Primary Hebrew register: consonantal (D16 default). German dipl/ascii pairs "
            "expose the diplomatic-vs-simplified confound; Vulgate/Macer/Decameron are "
            "critical editions with expanded abbreviations. Stratify by `edition`."
        ),
        "texts": {},
    }
    for text in TEXTS:
        words = text.extract()
        (out_root / f"{text.key}.txt").write_text(to_lines(words), encoding="utf-8")
        manifest["texts"][text.key] = {
            "language": text.language,
            "form": text.form,
            "edition": text.edition,
            "period": text.period,
            "genre": text.genre,
            "sources": {rel: sha256_of(H4_RAW / rel) for rel in text.sources},
            "words": len(words),
            "chars": sum(len(w) for w in words),
        }
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = build()
    for key, info in result["texts"].items():
        print(f"{key:42s} {info['words']:>8,} words {info['chars']:>10,} chars")
