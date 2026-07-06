"""Naibbe cipher generator/decrypter (harness class H2) — reimplementation of Greshko (2025).

Spec: docs/planning/i01/specs/T03-naibbe-spec.md.
Reference implementation: github.com/greshko/naibbe-cipher @ f2675ec, modified MIT.
Any publication using this reimplementation or its table data must cite:
Greshko, Michael A. (2025). "The Naibbe cipher: a substitution cipher that encrypts
Latin and Italian as Voynich Manuscript-like ciphertext." Cryptologia.
https://doi.org/10.1080/01611194.2025.2566408

Implements v2 semantics by default (unambiguous mode with unigram-collision and
cross-bigram-collision rejection), which guarantees uniquely decryptable ciphertext —
the "meaningful, recoverable" ground-truth property H2 requires. v1 behavior is
reachable via NaibbeConfig(cross_bigram_check=False).

Usage:
    python -m ms408.harness.naibbe --source naibbe_pliny --seed 408 --deck 52
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from ..acquire import sha256_of
from ..dataset import git_commit
from ..sources import RAW_ROOT, SOURCES, path_for

TABLE_NAMES = ("alpha", "beta1", "beta2", "beta3", "gamma1", "gamma2")
DECKS = {
    "52": (20, 8, 8, 8, 4, 4),
    "78": (28, 14, 11, 11, 7, 7),
    # V2 (W6a variant matrix, L30): homophone-poor variant — alpha table only,
    # so each plaintext letter has exactly one unigram/prefix/suffix glyph and
    # homophony comes only from the random unigram/bigram segmentation
    "alpha-only": (52, 0, 0, 0, 0, 0),
}
ALPHABET = frozenset("abcdefghilmnopqrstuvxyz")  # 23 letters: a-z minus j, k, w
ROLES = ("unigram", "prefix", "suffix")
TABLES_SHA256 = SOURCES["naibbe_tables"].sha256
DEFAULT_TABLES_PATH = RAW_ROOT / "naibbe-cipher" / "references" / "naibbe_tables.csv"

_LIGATURES = str.maketrans(
    {
        "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE", "ð": "d", "Ð": "D",
        "þ": "th", "Þ": "TH", "ł": "l", "Ł": "L", "ß": "ss", "ø": "o", "Ø": "O",
    }
)


def clean_line(line: str) -> str:
    """Normalize plaintext to the 23-letter cipher alphabet, spaces removed (spec §4.1)."""
    s = unicodedata.normalize("NFD", line)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.translate(_LIGATURES)
    s = "".join(c for c in s if c.isalpha())
    return s.upper().replace("W", "UU").replace("J", "I").replace("K", "C").lower()


@dataclass(frozen=True)
class NaibbeTables:
    """The cipher key: (role, table, letter) -> EVA glyph string, plus derived indexes."""

    glyph: dict
    unigram_glyphs: frozenset
    ambiguous_bigrams: frozenset
    to_letter: dict  # role -> glyph -> plaintext letter(s)

    @classmethod
    def load(
        cls, path: Path = DEFAULT_TABLES_PATH, expected_sha256: str | None = TABLES_SHA256
    ) -> "NaibbeTables":
        if expected_sha256 and sha256_of(path) != expected_sha256:
            raise ValueError(f"{path}: sha256 mismatch against pinned cipher key")
        glyph: dict = {}
        with open(path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                role, table, letter = row["code"].split("_")
                key = (role, table, letter)
                if key in glyph:
                    raise ValueError(f"duplicate table entry {key}")
                glyph[key] = row["glyphs"]
        if len(glyph) != 414:
            raise ValueError(f"expected 414 table entries, got {len(glyph)}")
        for role in ROLES:
            for table in TABLE_NAMES:
                letters = {lt for (r, t, lt) in glyph if r == role and t == table}
                if letters != ALPHABET:
                    raise ValueError(f"table {role}/{table} letter set incomplete")

        unigram_glyphs = frozenset(g for (r, _, _), g in glyph.items() if r == "unigram")
        prefixes = {g for (r, _, _), g in glyph.items() if r == "prefix"}
        suffixes = {g for (r, _, _), g in glyph.items() if r == "suffix"}
        if len(prefixes) != 138 or len(suffixes) != 138:
            raise ValueError("prefix/suffix glyphs are expected to be 138 distinct each")
        concat_counts = Counter(p + s for p in prefixes for s in suffixes)
        ambiguous = frozenset(s for s, n in concat_counts.items() if n > 1)

        to_letter: dict = {role: {} for role in ROLES}
        for (role, _, letter), g in glyph.items():
            existing = to_letter[role].get(g)
            if existing is not None and existing != letter:
                raise ValueError(f"glyph {g!r} maps to conflicting letters in role {role}")
            to_letter[role][g] = letter

        return cls(
            glyph=glyph,
            unigram_glyphs=unigram_glyphs,
            ambiguous_bigrams=ambiguous,
            to_letter=to_letter,
        )


@dataclass(frozen=True)
class NaibbeConfig:
    deck: str = "52"
    respacing: int = 17  # P(unigram) = respacing/36; 17 standard, 18 simplified
    unambiguous: bool = True
    cross_bigram_check: bool = True  # v2 semantics; False reproduces v1
    max_bigram_retries: int = 10000
    space_removal_rate: float = 0.03


@dataclass
class EncryptedLine:
    units: list
    words: list
    retries: int


@dataclass
class NaibbeResult:
    ciphertext_lines: list
    respaced_lines: list
    segmented_lines: list
    total_retries: int


class NaibbeCipher:
    def __init__(self, tables: NaibbeTables, config: NaibbeConfig, seed: int):
        self.tables = tables
        self.config = config
        self.seed = seed
        self.rng = random.Random(seed)  # single injected stream (spec §6)
        self._deck: list = []

    def segment(self, cleaned: str) -> list:
        """Dice-roll unit segmentation (spec §4.2); line-final letter forced unigram."""
        p_unigram = self.config.respacing / 36
        units, i = [], 0
        while i < len(cleaned):
            if i == len(cleaned) - 1 or self.rng.random() < p_unigram:
                units.append(cleaned[i])
                i += 1
            else:
                units.append(cleaned[i : i + 2])
                i += 2
        return units

    def _draw(self) -> str:
        """Card draw without replacement; reshuffle a fresh deck on exhaustion (spec §4.3)."""
        if not self._deck:
            self._deck = [
                t for t, n in zip(TABLE_NAMES, DECKS[self.config.deck]) for _ in range(n)
            ]
            self.rng.shuffle(self._deck)
        return self._deck.pop()

    def _glyph(self, role: str, table: str, letter: str) -> str:
        try:
            return self.tables.glyph[(role, table, letter)]
        except KeyError:
            raise ValueError(f"letter {letter!r} has no {role} table entry") from None

    def encrypt_line(self, line: str) -> EncryptedLine:
        cleaned = clean_line(line)
        units = self.segment(cleaned)  # all segmentation randomness consumed first
        self._deck = []  # fresh shuffled deck per line
        words, retries = [], 0
        for unit in units:
            if len(unit) == 1:
                words.append(self._glyph("unigram", self._draw(), unit))
                continue
            unit_retries = 0
            while True:
                candidate = self._glyph("prefix", self._draw(), unit[0]) + self._glyph(
                    "suffix", self._draw(), unit[1]
                )
                if not self.config.unambiguous:
                    break
                collides = candidate in self.tables.unigram_glyphs or (
                    self.config.cross_bigram_check
                    and candidate in self.tables.ambiguous_bigrams
                )
                if not collides:
                    break
                unit_retries += 1  # rejected draws still consume cards
                if unit_retries > self.config.max_bigram_retries:
                    raise RuntimeError(f"bigram retry fuse blown for unit {unit!r}")
            retries += unit_retries
            words.append(candidate)
        return EncryptedLine(units=units, words=words, retries=retries)

    def _respace(self, words: list) -> list:
        """Merge ~3% of interior word boundaries (spec §4.6)."""
        if len(words) < 2:
            return list(words)
        out = [words[0]]
        for word in words[1:]:
            if self.rng.random() < self.config.space_removal_rate:
                out[-1] += word
            else:
                out.append(word)
        return out

    def encrypt_text(self, lines) -> NaibbeResult:
        result = NaibbeResult([], [], [], 0)
        for line in lines:
            enc = self.encrypt_line(line)
            result.ciphertext_lines.append(" ".join(enc.words))
            result.respaced_lines.append(" ".join(self._respace(enc.words)))
            result.segmented_lines.append(" ".join(enc.units))
            result.total_retries += enc.retries
        return result


def decrypt_word(tables: NaibbeTables, word: str) -> str:
    """Unigram reading takes precedence; multi-parse -> '(ab|cd)'; unparseable -> '[?]'."""
    if word in tables.to_letter["unigram"]:
        return tables.to_letter["unigram"][word]
    readings: list = []
    for i in range(1, len(word)):
        p, s = word[:i], word[i:]
        if p in tables.to_letter["prefix"] and s in tables.to_letter["suffix"]:
            reading = tables.to_letter["prefix"][p] + tables.to_letter["suffix"][s]
            if reading not in readings:
                readings.append(reading)  # discovery order, matching the author's output
    if len(readings) == 1:
        return readings[0]
    if readings:
        return "(" + "|".join(readings) + ")"
    return "[?]"


def decrypt_line(tables: NaibbeTables, line: str) -> str:
    return " ".join(decrypt_word(tables, w) for w in line.split())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Generate H2 Naibbe ciphertext")
    parser.add_argument("--source", required=True,
                        help="registered source name for plaintext (e.g. naibbe_pliny)")
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--deck", choices=sorted(DECKS), default="52")
    parser.add_argument("--respacing", type=int, default=17)
    parser.add_argument("--v1", action="store_true", help="disable cross-bigram check")
    parser.add_argument("--out-dir", type=Path,
                        default=Path(__file__).resolve().parents[3]
                        / "data" / "processed" / "harness" / "h2")
    args = parser.parse_args(argv)

    config = NaibbeConfig(
        deck=args.deck, respacing=args.respacing, cross_bigram_check=not args.v1
    )
    tables = NaibbeTables.load()
    plaintext_path = path_for(args.source)
    lines = plaintext_path.read_text(encoding="utf-8").splitlines()
    result = NaibbeCipher(tables, config, seed=args.seed).encrypt_text(lines)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{args.source}_deck{args.deck}_seed{args.seed}{'_v1' if args.v1 else ''}"
    outputs = {
        f"{stem}_ciphertext.txt": result.ciphertext_lines,
        f"{stem}_respaced.txt": result.respaced_lines,
        f"{stem}_segmented.txt": result.segmented_lines,
    }
    for filename, out_lines in outputs.items():
        (args.out_dir / filename).write_text("\n".join(out_lines) + "\n")
    manifest = {
        "generator": "ms408.harness.naibbe",
        "git_commit": git_commit(),
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "seed": args.seed,
        "config": asdict(config),
        "tables_sha256": TABLES_SHA256,
        "plaintext_source": args.source,
        "plaintext_sha256": sha256_of(plaintext_path),
        "total_bigram_retries": result.total_retries,
        "outputs": sorted(outputs),
    }
    (args.out_dir / f"{stem}_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
