"""Timm-Schinner self-citation text generator (harness class H3) — reimplementation.

Spec: docs/planning/i01/specs/T03-selfcitation-spec.md (section references below are to it).
Authoritative source: github.com/TorstenTimm/SelfCitationTextgenerator @ a6ede22, whose
substitution tables and probability constants are reproduced here under its license:

    MIT License, Copyright (c) 2019 Torsten Timm. Permission is hereby granted, free of
    charge, to any person obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without restriction [...] subject to
    including the above copyright notice and this permission notice in all copies or
    substantial portions of the Software.

Cite in any report using H3 output: Timm & Schinner (2020), Cryptologia 44(1),
doi:10.1080/01611194.2019.1596999; arXiv:1407.6639; Zenodo doi:10.5281/zenodo.2531632.

Bit-exact replication of the Java output is impossible (JVM HashMap iteration order —
spec §12); our deterministic replacements are longest-match-first tokenization,
insertion-ordered dictionaries, and first-max tie-breaks (spec §16 R3). Validation is
therefore distributional against the author's committed seed-19 reference output
(data/raw/timm-selfcitation/generated_text.txt).

Usage:
    python -m ms408.harness.selfcitation --seed 19 --lines 1200 --dialect B
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# §4 — Tokenization and glyph inventory (Glyph.java)
# ---------------------------------------------------------------------------

LIGATURES = (
    "ol", "or", "al", "ar", "dy", "qo", "ch", "sh", "cs",
    "ee", "eee",
    "cth", "cthh", "ckh", "ckhh", "cph", "cfh",
    "ith", "ikh", "iph", "ifh",
    "eke", "ete",
    "in", "iin", "iiin", "ir", "iir", "iiir", "is", "iis", "iiis",
    "il", "iil", "iiil", "im", "iim", "iiim",
    "om", "am", "og", "ag",
)
_LIGATURES_BY_LENGTH = tuple(sorted(LIGATURES, key=len, reverse=True))

GALLOWS = ("k", "t", "p", "f")
LINE_INITIAL_GLYPHS = ("o", "y", "d", "s")
COMBINABLE = ("ol", "al", "or", "ar")  # core set (Glyph.combinableLigature)
COMBINABLE_ALL = ("ol", "al", "or", "ar", "om", "am")

# prefix -> allowed first tokens of the word (Glyph.prefixGlyphsStrings)
PREFIX_TABLE = {
    "l": ("k", "t", "p", "f", "d", "ch", "sh", "o", "a", "e", "i"),
    "o": ("k", "t", "p", "f", "d", "ch", "sh"),
    "y": ("k", "t", "p", "f", "d", "ch", "sh"),
    "ch": ("k", "t", "p", "f", "d", "ol", "or", "al", "ar"),
    "sh": ("k", "t", "p", "f", "d", "ol", "or", "al", "ar"),
    "d": ("a",),
    "x": ("ol", "or", "al", "ar"),
    # "q" is special-cased: it only forms qo by replacing a leading o/y (§8.2)
}

FINAL_LINE_REPLACEMENTS = {
    "ol": "om", "or": "om", "al": "am", "ar": "am", "om": "og", "am": "ag",
    "im": "mg", "in": "n", "iin": "im", "iiin": "im",
}
INGROUP_REPLACEMENTS = {
    "y": "o", "m": "r", "g": "r", "n": "r", "in": "ir", "iin": "iir", "dy": "da",
}
GROUP_FINAL_REPLACEMENTS = {"o": "y", "a": "y", "k": "t", "t": "k", "p": "f", "f": "p"}


def tokenize(text: str) -> tuple:
    """Longest-match-first ligature tokenization (spec §4, fidelity decision F1)."""
    tokens, i = [], 0
    while i < len(text):
        for lig in _LIGATURES_BY_LENGTH:
            if text.startswith(lig, i):
                tokens.append(lig)
                i += len(lig)
                break
        else:
            tokens.append(text[i])
            i += 1
    return tuple(tokens)


# generate_type tags (§8): COMBINE gates several rules and must persist
INITIAL, ADD, DELETE, REPLACE, COMBINE, SPLIT, SHORTEN, SUGGEST = (
    "INITIAL", "ADD", "DELETE", "REPLACE", "COMBINE", "SPLIT", "SHORTEN", "SUGGEST"
)


@dataclass(frozen=True)
class Word:
    tokens: tuple
    tag: str

    @property
    def text(self) -> str:
        return "".join(self.tokens)

    @classmethod
    def parse(cls, text: str, tag: str) -> "Word":
        return cls(tokens=tokenize(text), tag=tag)

    def contains_gallow(self) -> bool:
        return any(g in tok for tok in self.tokens for g in GALLOWS)

    def type_class(self) -> str:
        """§10 classification, if/else precedence exactly."""
        if "i" in self.text:
            return "i"
        if any(tok == "dy" for tok in self.tokens) or self.text[-1:] in ("y", "d"):
            return "dy"
        if any(tok in COMBINABLE for tok in self.tokens):
            return "ol"
        return "other"


# ---------------------------------------------------------------------------
# §5 — Substitution tables (Glyph.java, verbatim; thresholds are cumulative)
# ---------------------------------------------------------------------------
# Candidates are strings; multi-token candidates re-tokenize consistently
# (e.g. "che" -> ch|e, "kch" -> k|ch), so plain strings are faithful.

SUBSTITUTIONS = {
    "k": [("t", 77), ("p", 94), ("f", 100)],
    "t": [("k", 84), ("p", 96), ("f", 100)],
    "p": [("k", 59), ("t", 97), ("f", 100)],
    "f": [("k", 56), ("t", 92), ("p", 100)],
    "in": [("n", 8), ("iin", 84), ("iiin", 87), ("ir", 97), ("iir", 98), ("iis", 99), ("il", 100)],
    "iin": [("n", 13), ("in", 70), ("iiin", 74), ("ir", 92), ("iir", 97), ("is", 99), ("il", 100)],
    "iiin": [("n", 6), ("in", 31), ("iin", 90), ("ir", 98), ("iir", 100)],
    "ir": [("r", 6), ("in", 33), ("iin", 95), ("iiin", 97), ("iir", 99), ("iiir", 100)],
    "iir": [("r", 6), ("in", 30), ("iin", 89), ("iiin", 91), ("ir", 99), ("iiir", 100)],
    "iiir": [("ir", 90), ("iir", 100)],
    "is": [("in", 50), ("iis", 100)],
    "iis": [("iin", 50), ("is", 100)],
    "il": [("in", 50), ("iil", 100)],
    "iil": [("iin", 50), ("il", 99), ("iiil", 100)],
    "iiil": [("il", 66), ("iil", 100)],
    "im": [("in", 30), ("iin", 100)],
    "iim": [("in", 30), ("iin", 100)],
    "iiim": [("in", 30), ("iin", 100)],
    "om": [("ol", 45), ("or", 94), ("og", 98), ("omg", 100)],
    "am": [("al", 45), ("ar", 94), ("ag", 98), ("amg", 100)],
    "og": [("or", 30), ("al", 63), ("ar", 100)],
    "ag": [("ol", 48), ("or", 72), ("ar", 100)],
    "ol": [("or", 30), ("al", 63), ("ar", 100)],
    "or": [("ol", 47), ("al", 73), ("ar", 100)],
    "al": [("ol", 48), ("or", 72), ("ar", 100)],
    "ar": [("ol", 49), ("or", 73), ("al", 100)],
    "e": [("e", 50), ("ee", 99), ("eee", 100)],
    "ee": [("ch", 40), ("che", 50), ("e", 98), ("eee", 100)],
    "eee": [("ch", 10), ("che", 20), ("ee", 65), ("e", 100)],
    "ch": [("ee", 10), ("che", 20), ("sh", 90), ("ckh", 97), ("cth", 100)],
    "sh": [("ee", 10), ("ch", 90), ("ckh", 97), ("cth", 100)],
    "ckh": [("cth", 30), ("kch", 50), ("tch", 70), ("eke", 72), ("ete", 74), ("cph", 78), ("ch", 100)],
    "cth": [("ckh", 30), ("kch", 50), ("tch", 70), ("eke", 72), ("ete", 74), ("cph", 78), ("cfh", 80), ("ch", 100)],
    "cs": [("sh", 100)],
    "ckhh": [("ckh", 100)],
    "cthh": [("cth", 100)],
    "ikh": [("ckh", 100)],
    "ith": [("cth", 100)],
    "iph": [("cph", 100)],
    "ifh": [("cfh", 100)],
    "eke": [("ckh", 30), ("cth", 50), ("kee", 56), ("tee", 60), ("ete", 65), ("ee", 100)],
    "ete": [("ckh", 30), ("cth", 50), ("kee", 56), ("tee", 60), ("eke", 65), ("ee", 100)],
    "cph": [("ckh", 40), ("cth", 75), ("cfh", 80), ("ch", 100)],
    "cfh": [("ckh", 40), ("cth", 75), ("cph", 80), ("ch", 100)],
    "y": [("o", 100)],
    "o": [("y", 100)],
    "n": [("r", 50), ("in", 63), ("iin", 100)],
    "l": [("r", 100)],
    "r": [("r", 50), ("s", 100)],
    "g": [("m", 100)],
    "s": [("r", 75), ("d", 100)],
    "d": [("d", 90), ("s", 100)],
    "a": [("a", 98), ("o", 100)],
    "qo": [("o", 80), ("y", 100)],
}

FINAL_SUBSTITUTIONS = {
    "om": [("o", 8), ("y", 30), ("ol", 75), ("or", 100)],
    "am": [("o", 4), ("y", 30), ("al", 70), ("ar", 100)],
    "og": [("o", 8), ("y", 30), ("or", 55), ("al", 80), ("ar", 100)],
    "ag": [("o", 4), ("y", 30), ("ol", 65), ("or", 80), ("ar", 100)],
    "ol": [("o", 8), ("y", 30), ("or", 54), ("al", 81), ("ar", 100)],
    "or": [("o", 8), ("y", 30), ("ol", 63), ("al", 81), ("ar", 100)],
    "al": [("o", 4), ("y", 30), ("ol", 64), ("or", 81), ("ar", 100)],
    "ar": [("o", 4), ("y", 30), ("ol", 64), ("or", 82), ("al", 100)],
    "y": [("o", 20), ("ol", 44), ("or", 60), ("al", 75), ("ar", 100)],
    "o": [("y", 20), ("ol", 44), ("or", 60), ("al", 75), ("ar", 100)],
    "d": [("dy", 70), ("d", 100)],
    "dy": [("d", 10), ("dy", 100)],
}


class Rand:
    """rand(max) -> [0, max); rand(0) returns 0 without consuming state (spec §12)."""

    def __init__(self, seed: int):
        self._rng = random.Random(seed)

    def __call__(self, bound: int) -> int:
        if bound <= 0:
            return 0
        return self._rng.randrange(bound)


def choose_substitution(candidates: list, rng: Rand) -> str:
    """First entry in list order with threshold > r (cumulative CDF, spec §5)."""
    r = rng(100)
    for candidate, threshold in candidates:
        if threshold > r:
            return candidate
    return candidates[-1][0]


def random_gallow(rng: Rand, first_line: bool) -> str:
    r = rng(100)
    if first_line:
        if r <= 34:
            return "k"
        if r <= 49:
            return "t"
        if r <= 89:
            return "p"
        return "f"
    return "k" if r <= 74 else "t"


def random_line_initial_glyph(rng: Rand) -> str:
    r = rng(100)
    if r <= 45:
        return "o"
    if r <= 75:
        return "y"
    if r <= 90:
        return "d"
    return "s"


_PREFIX_CASCADE = (
    (5, "l"), (34, "o"), (40, "y"), (61, "ch"), (72, "sh"), (88, "q"), (99, "d"),
)


def choose_prefix(rng: Rand, attempt: int, previous_word, already_tried: set) -> str:
    r = rng(100)
    if (
        attempt == 0
        and previous_word is not None
        and previous_word.tokens
        and previous_word.tokens[-1] == "dy"
        and r < 90
    ):
        return "q"
    for threshold, prefix in _PREFIX_CASCADE:
        if r < threshold and prefix not in already_tried:
            return prefix
    if r == 99 and attempt == 0:
        return "x"
    return "o"


# ---------------------------------------------------------------------------
# §6 — Glyph adjacency: CurveLineCanFollow (default; error_rate=0)
# ---------------------------------------------------------------------------

START_GLYPHS = ("qo", "a", "o", "y", "c", "s", "d", "k", "t", "p", "f", "x")
FINAL_GLYPHS = ("y", "n", "l", "r", "s", "d", "m", "g", "x")
CC_TOKENS = ("e", "h", "d", "s", "y", "o", "ch", "sh", "ckh", "cth", "cph", "cfh", "al", "ol", "x", "l")
C_FINAL_TOKENS = ("d", "g", "o", "y", "dy", "s", "om", "am", "og", "ag", "al", "ar", "ol", "or", "x")
CL_TOKENS = ("a",)
LC_TOKENS = ("ikh", "ith", "iph", "ifh")
LL_TOKENS = ("i",)
L_FINAL_TOKENS = ("n", "in", "iin", "iiin", "r", "ir", "iir", "iiir", "m", "im", "iiil", "iil", "il", "iis", "is")
AFTER_GALLOW = ("a", "e", "o", "y", "h", "ch", "sh")
AOY = ("a", "o", "y")
RMNG = ("r", "m", "n", "g")

EMPTY, LINE, CURVE, GALLOW, FINAL, NONE = "EMPTY", "LINE", "CURVE", "GALLOW", "FINAL", "NONE"


def _ends_with_any(s: str, tokens) -> bool:
    return any(s.endswith(t) for t in tokens)


def _starts_with_any(s: str, tokens) -> bool:
    return any(s.startswith(t) for t in tokens)


def end_type(tok: str) -> str:
    if tok == "":
        return EMPTY
    if _ends_with_any(tok, CL_TOKENS + LL_TOKENS):
        return LINE
    if _ends_with_any(tok, CC_TOKENS + LC_TOKENS):
        return CURVE
    if _ends_with_any(tok, FINAL_GLYPHS):
        return FINAL
    if _ends_with_any(tok, GALLOWS):
        return GALLOW
    return NONE


def start_type(tok: str) -> str:
    if tok == "":
        return EMPTY
    if _starts_with_any(tok, LL_TOKENS + LC_TOKENS + L_FINAL_TOKENS):
        return LINE
    if _starts_with_any(tok, CC_TOKENS + CL_TOKENS + C_FINAL_TOKENS):
        return CURVE
    if _starts_with_any(tok, GALLOWS):
        return GALLOW
    return NONE


def can_follow_before(add: str, rest: str) -> bool:
    """May token `add` be placed immediately before string `rest` (spec §6)."""
    if add in COMBINABLE_ALL and _starts_with_any(rest, AOY):
        return True
    if _starts_with_any(rest, COMBINABLE_ALL) and _ends_with_any(add, RMNG):
        return True
    if add and rest.startswith(add):
        return False
    if rest == "":
        return add in L_FINAL_TOKENS or add in C_FINAL_TOKENS
    kind = end_type(add)
    if kind == EMPTY:
        return _starts_with_any(rest, START_GLYPHS)
    if kind == LINE:
        return _starts_with_any(rest, LC_TOKENS + L_FINAL_TOKENS + LL_TOKENS)
    if kind == CURVE:
        return _starts_with_any(rest, CC_TOKENS + CL_TOKENS + C_FINAL_TOKENS + GALLOWS)
    if kind == GALLOW:
        return _starts_with_any(rest, AFTER_GALLOW)
    if kind == FINAL:
        return rest == ""
    return False


def can_follow_after(head: str, add: str) -> bool:
    """May token `add` be appended after string `head` (spec §6)."""
    if _ends_with_any(head, COMBINABLE_ALL) and _starts_with_any(add, AOY):
        return True
    if add in COMBINABLE_ALL and _ends_with_any(head, RMNG):
        return True
    if add and head.endswith(add):
        return False
    if head == "":
        return add in START_GLYPHS
    kind = start_type(add)
    if kind == EMPTY:
        return _ends_with_any(head, FINAL_GLYPHS)
    if kind == LINE:
        return _ends_with_any(head, LL_TOKENS + CL_TOKENS)
    if kind == CURVE:
        return _ends_with_any(head, CC_TOKENS + LC_TOKENS + GALLOWS)
    if kind == GALLOW:
        return head == "" or _ends_with_any(head, ("a", "e", "o", "l", "y", "h"))
    return False


def is_valid(word: Word) -> bool:
    if not word.tokens:
        return False
    if not can_follow_before("", word.text):
        return False
    for prev, nxt in zip(word.tokens, word.tokens[1:]):
        if not (can_follow_after(prev, nxt) and can_follow_before(prev, nxt)):
            return False
    return True


def has_valid_start(word: Word) -> bool:
    if word.tag == INITIAL:
        return True
    return can_follow_before("", word.text)


# ---------------------------------------------------------------------------
# §8 — Morph operations (SlimGroupMorpher)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MorphConfig:
    add_remove_probability: int = 20
    combine_split_probability: int = 30
    reuse_last_probability: int = 10
    use_word_final_substitutions: bool = True
    max_repeat_count: int = 3


class Morpher:
    def __init__(self, rng: Rand, config: MorphConfig):
        self.rng = rng
        self.config = config

    # -- §8.1 entry -------------------------------------------------------

    def morph(self, sources, previous_word, is_par_initial, is_line_initial) -> list:
        src0 = sources[0]
        if is_par_initial and is_line_initial:
            r = 0  # forced add path, no draw (spec §8.1)
        else:
            r = self.rng(100)
        a = self.config.add_remove_probability
        c = self.config.combine_split_probability
        if r <= a and src0.tag != COMBINE:
            result = self._add_remove(src0, is_par_initial, is_line_initial)
        elif r <= a + c:
            result = self._combine_split(sources)
        else:
            result = self._replace_family(src0)
        if not result:
            return []
        result[0] = self._handle_gallows(result[0], is_par_initial, is_line_initial)
        if len(result) == 1:
            result.extend(self._reuse_last(result[0]))
        return result

    # -- §8.2 add/remove ---------------------------------------------------

    def _add_remove(self, word: Word, is_par_initial, is_line_initial) -> list:
        added = None
        if len(word.text) < 6:
            added = self._add_random_glyph(word, is_par_initial, is_line_initial)
        if added is not None:
            return [added]
        deleted = self._try_delete_prefix(word)
        return [deleted] if deleted is not None else []

    def _add_random_glyph(self, word, is_par_initial, is_line_initial):
        r = self.rng(100)
        if r < (80 if is_par_initial else 8):
            result = self._add_gallow(word, is_par_initial, is_line_initial)
            return result if result is not None and result.text != word.text else None
        return self._try_add_prefix(word)

    def _try_add_prefix(self, word: Word):
        tried: set = set()
        for attempt in range(7):
            prefix = choose_prefix(self.rng, attempt, self._previous_word, tried)
            if prefix in tried:
                continue
            tried.add(prefix)
            first = word.tokens[0]
            tag = COMBINE if word.tag == COMBINE else ADD
            if prefix == "q":
                if first in ("o", "y"):
                    return Word(("qo",) + word.tokens[1:], tag)
                continue
            if prefix == "x":
                if first in COMBINABLE:
                    return Word(("x",) + word.tokens, tag)
                continue
            if first not in PREFIX_TABLE.get(prefix, ()):
                continue
            tokens = word.tokens
            if len(tokens) > 2 and first in ("d", "ch", "sh"):
                gallow = random_gallow(self.rng, False)
                if (
                    can_follow_before(gallow, tokens[1])
                    and can_follow_after(prefix, gallow)
                    and self.rng(100) < 70
                ):
                    tokens = (gallow,) + tokens[1:]
            return Word((prefix,) + tokens, tag)
        return None

    def _try_delete_prefix(self, word: Word):
        if len(word.tokens) <= 2:
            return None
        rest = word.tokens[1:]
        if not can_follow_before("", "".join(rest)):
            return None
        if rest[0] in GALLOWS and len(rest) > 1:
            r = self.rng(100)
            if rest[1].startswith("a") and r < 50:
                rest = ("d",) + rest[1:]
            elif rest[1][:1] in ("e", "o") and r < 50:
                rest = ("ch",) + rest[1:]
        tag = COMBINE if word.tag == COMBINE else DELETE
        return Word(rest, tag)

    # -- §8.3 gallows ------------------------------------------------------

    def _add_gallow(self, word: Word, is_par_initial, is_line_initial):
        if is_par_initial and is_line_initial:
            gallow = random_gallow(self.rng, True)
            placed = self._try_place_gallow(gallow, word, 0)
            if not placed.text.startswith(gallow):
                for lead in ("o", "a"):
                    if can_follow_before(lead, placed.text):
                        return Word((gallow, lead) + placed.tokens, ADD)
                return Word((gallow,) + placed.tokens, ADD)
            return placed
        if len(word.tokens) > 1:
            if word.contains_gallow() and self.rng(100) < 90:
                return None
            for _ in range(5):
                n = len(word.tokens)
                if is_par_initial:
                    pos = self.rng(n)
                else:
                    pos = 1 if n == 2 else 1 + self.rng(n - 2)
                gallow = random_gallow(self.rng, is_par_initial)
                placed = self._try_place_gallow(gallow, word, pos)
                if placed.text != word.text:
                    return placed
        return None

    def _try_place_gallow(self, gallow: str, word: Word, pos: int) -> Word:
        tokens = word.tokens
        tag = COMBINE if word.tag == COMBINE else ADD
        if pos < len(tokens) and tokens[pos] in GALLOWS:
            return Word(tokens[:pos] + (gallow,) + tokens[pos + 1 :], tag)
        prev = tokens[pos - 1] if pos > 0 else ""
        nxt = tokens[pos] if pos < len(tokens) else ""
        last_ok = can_follow_after(prev, gallow)
        next_ok = can_follow_before(gallow, nxt)
        if last_ok and next_ok:
            return Word(tokens[:pos] + (gallow,) + tokens[pos:], tag)
        if last_ok and pos + 1 < len(tokens) and can_follow_before(gallow, tokens[pos + 1]):
            return Word(tokens[:pos] + (gallow,) + tokens[pos + 1 :], tag)
        if next_ok and pos - 2 > 0 and can_follow_after(tokens[pos - 2], gallow):
            return Word(tokens[: pos - 1] + (gallow,) + tokens[pos:], tag)
        return word

    # -- §8.4 combine / split ----------------------------------------------

    def _combine_split(self, sources) -> list:
        src0 = sources[0]
        src1 = sources[1] if len(sources) > 1 else src0
        r = self.rng(100)
        length = len(src0.text)
        if src0.tag == COMBINE:
            combine = False
        elif length < 6:
            combine = length <= 2 or r < 96
        else:
            combine = r < 4 and length <= 8
        return self._combine(src0, src1) if combine else self._split(src0)

    @staticmethod
    def _calc_split_position(tokens) -> int:
        for i in range(1, len(tokens)):
            if (
                not can_follow_before(tokens[i - 1], tokens[i])
                or tokens[i - 1] in COMBINABLE
                or tokens[i] in GALLOWS
            ):
                if i > 1 or len(tokens[0]) > 1:
                    return i
        return -1

    def _join(self, left, right) -> Word | None:
        if left and left[-1] in COMBINABLE_ALL and right and right[0] in ("l", "r", "s"):
            right = right[1:]
        if not right:
            return None
        left_text, right_text = "".join(left), "".join(right)
        combined = left + tuple(right)
        if (
            len(left_text) > 1
            and len(right_text) > 1
            and len(left_text + right_text) < 9
            and (left[-1] in COMBINABLE or can_follow_before(left[-1], right[0]))
            and can_follow_after(right[-1], "")
        ):
            return Word(combined, COMBINE)
        return None

    def _combine(self, src0: Word, src1: Word) -> list:
        pos0 = self._calc_split_position(src0.tokens)
        left = src0.tokens if len(src0.tokens) <= 2 or pos0 < 0 else src0.tokens[:pos0]
        if len(src1.tokens) <= 3:
            right = src1.tokens
        else:
            pos1 = self._calc_split_position(src1.tokens)
            right = src1.tokens[pos1:] if pos1 > 0 else src1.tokens
        joined = self._join(left, right)
        if joined is not None:
            return [joined]
        # base combine (AbstractBaseGroupMorpher)
        small = len(src0.tokens) == 2 or (len(src0.tokens) == 1 and src0.tokens[0] in COMBINABLE)
        if small and self.rng(100) < 60:
            selfed = self._self_combine(src0)
            if selfed is not None:
                return [selfed]
        r = self.rng(100)
        if r <= 39 and len(src1.tokens) >= 2:
            right = src1.tokens[: 1 + self.rng(len(src1.tokens) - 1)]
        elif r <= 59:
            right = src1.tokens[:-1]
        else:
            ligature = next((t for t in src1.tokens if t in COMBINABLE), None)
            right = (ligature,) if ligature else src1.tokens[:-1]
        if right and len(src0.tokens) + len(right) < 9:
            joined = self._join(src0.tokens, right)
            if joined is not None:
                return [joined]
        if len(src0.tokens) <= 2:
            selfed = self._self_combine(src0)
            if selfed is not None:
                return [selfed]
        return [src0]  # failure signal: unchanged

    def _self_combine(self, word: Word) -> Word | None:
        if not can_follow_before(word.tokens[-1], word.tokens[0]):
            return None
        first = list(word.tokens)
        first[-1] = INGROUP_REPLACEMENTS.get(first[-1], first[-1])
        second = list(word.tokens)
        if self.rng(100) < 80:
            second[-1] = GROUP_FINAL_REPLACEMENTS.get(second[-1], second[-1])
        tokens = tuple(first) + tuple(second)
        if self.rng(100) < 30 and len(tokens) > 1:
            gallow = random_gallow(self.rng, False)
            if can_follow_after(tokens[0], gallow) and can_follow_before(gallow, tokens[1]):
                tokens = tokens[:1] + (gallow,) + tokens[1:]
        return Word(tokens, COMBINE)

    def _split(self, src0: Word) -> list:
        pos = self._calc_split_position(src0.tokens)
        if pos < 0:
            return [src0]
        part1, part2 = src0.tokens[:pos], src0.tokens[pos:]
        result = []
        if (
            (len(part1) >= 2 or (len(part1) == 1 and part1[0] in COMBINABLE))
            and can_follow_after(part1[-1], "")
        ):
            result.append(Word(part1, SPLIT))
        if len(part2) >= 2:
            result.append(Word(part2, SPLIT))
        return result if result else [src0]

    # -- §8.5 replace -------------------------------------------------------

    def _replace_family(self, src0: Word) -> list:
        r = self.rng(100)
        attempts = 1 if r <= 30 else (3 if r <= 40 else 2)
        current = src0
        if attempts == 1:
            changed = self._replace_random_token(current, chain_step=0)
            if changed is None:
                changed = self._replace_random_token(current, chain_step=1)
            if changed is not None:
                current = changed
        else:
            for step in range(attempts):
                changed = self._replace_random_token(current, chain_step=step)
                if changed is not None:
                    current = changed
        if current.text == src0.text:
            return []
        tag = COMBINE if src0.tag == COMBINE else REPLACE
        return [Word(current.tokens, tag)]

    def _replace_random_token(self, word: Word, chain_step: int = 0) -> Word | None:
        # "not the first attempt (j > 0)" in spec §8.5 is ambiguous between the
        # within-call pool index and the chain-step index; the chain-step reading
        # reproduces the author's type-class proportions and is used here (§16 R1 —
        # reconcile against the 2020 paper / a live Java run when available).
        pool = list(range(len(word.tokens))) * 2
        for attempt in range(len(pool)):
            pos = pool.pop(self.rng(len(pool)))
            token = word.tokens[pos]
            last_position = pos == len(word.tokens) - 1
            # last_position alone would hit single-token words (pos 0 == last), and
            # the y/o candidates in the final table then flood the text with 1-char
            # words that self-amplify through citation — absent from the author's
            # output (0.2% 1-char words), so "final" requires a non-initial position.
            use_final = (
                self.config.use_word_final_substitutions
                and (chain_step > 0 or attempt > 0)
                and last_position
                and len(word.tokens) > 1
            )
            table = FINAL_SUBSTITUTIONS if use_final else SUBSTITUTIONS
            candidates = table.get(token)
            if not candidates:
                continue
            substitute = choose_substitution(candidates, self.rng)
            sub_tokens = tokenize(substitute)
            remove_next = (
                any(t in GALLOWS for t in sub_tokens)
                and pos + 1 < len(word.tokens)
                and word.tokens[pos + 1] in GALLOWS
            )
            if sub_tokens == (token,) and not remove_next:
                continue  # self-substitution: counts as a failed position (spec §5.1 note)
            next_index = pos + (2 if remove_next else 1)
            prev = word.tokens[pos - 1] if pos > 0 else ""
            nxt = word.tokens[next_index] if next_index < len(word.tokens) else ""
            if not (
                can_follow_after(prev, sub_tokens[0])
                and can_follow_before(sub_tokens[-1], nxt)
            ):
                continue
            others = word.tokens[:pos] + word.tokens[next_index:]
            if sub_tokens[0] in others and sub_tokens[0] not in COMBINABLE:
                reject_probability = (
                    100 if (sub_tokens[0] == prev or sub_tokens[-1] == nxt) else 80
                )
                if self.rng(100) < reject_probability:
                    continue
            new_tokens = word.tokens[:pos] + sub_tokens + word.tokens[next_index:]
            return Word(new_tokens, word.tag)
        return None

    # -- §8.6 post-processing ------------------------------------------------

    _previous_word: Word | None = None  # set by the generator before each morph call

    def _handle_gallows(self, word: Word, is_par_initial, is_line_initial) -> Word:
        if is_line_initial:
            r = self.rng(100)
            if is_par_initial and r < 94:
                placed = self._add_gallow(word, True, True)
                if placed is not None:
                    word = placed
            else:
                word = self._add_line_initial_glyph(word)
        elif word.tokens[0] in LINE_INITIAL_GLYPHS:
            if self.rng(8) < 3 and len(word.tokens) > 3:
                deleted = self._try_delete_prefix(word)
                if deleted is not None:
                    word = deleted
        return self._rebalance_gallows(word, is_par_initial)

    def _add_line_initial_glyph(self, word: Word) -> Word:
        if word.tokens[0] in LINE_INITIAL_GLYPHS:
            return word
        if self.rng(100) >= 30:
            return word
        glyph = random_line_initial_glyph(self.rng)
        tokens = word.tokens
        if glyph in ("o", "y") and tokens[0] in ("d", "ch") and len(tokens) > 2:
            if self.rng(100) < 90:
                gallow = random_gallow(self.rng, False)
                if can_follow_after(glyph, gallow) and can_follow_before(gallow, tokens[1]):
                    tokens = (gallow,) + tokens[1:]
        if can_follow_before(glyph, "".join(tokens)):
            return Word((glyph,) + tokens, word.tag)
        return word

    def _rebalance_gallows(self, word: Word, is_par_initial: bool) -> Word:
        if not word.contains_gallow():
            return word
        if not is_par_initial:
            if self.rng(100) < 94 and any("p" in t or "f" in t for t in word.tokens):
                fresh = random_gallow(self.rng, False)
                tokens = tuple(
                    t.replace("p", fresh).replace("f", fresh) if ("p" in t or "f" in t) else t
                    for t in word.tokens
                )
                return Word(tokens, word.tag)
            return word
        tokens = []
        for t in word.tokens:
            if any(g in t for g in GALLOWS):
                fresh = random_gallow(self.rng, True)
                for g in GALLOWS:
                    if g in t:
                        t = t.replace(g, fresh)
                        break
            tokens.append(t)
        return Word(tuple(tokens), word.tag)

    def _reuse_last(self, word: Word) -> list:
        if self.rng(100) >= self.config.reuse_last_probability:
            return []
        ligature = next((t for t in word.tokens if t in COMBINABLE), None)
        if ligature:
            second = Word((ligature,), word.tag)
        else:
            second = self._try_delete_prefix(word)
            if second is None:
                return []
        if self.rng(100) < 50:
            replaced = self._replace_random_token(second)
            if replaced is not None:
                second = replaced
        return [second]


# ---------------------------------------------------------------------------
# §10 — Feedback statistics and suggestions
# ---------------------------------------------------------------------------

TYPE_DEFAULTS_B = {"i": "daiin", "ol": "chol", "dy": "chedy"}
TYPE_DEFAULTS_A = {"i": "daiin", "ol": "chol", "dy": "cheody"}
FORCE_ROTATION = {
    "B": (("i", "dy"), ("dy", "i"), ("ol", "i")),
    "A": (("i", "ol"), ("ol", "i"), ("dy", "i")),
}


class Stats:
    def __init__(self, currier: str, max_word_tokens: int = 8):
        self.currier = currier
        self.max_word_tokens = max_word_tokens
        self.counts = {"i": 0, "dy": 0, "ol": 0, "other": 0}
        self.consecutive = {"i": 0, "dy": 0, "ol": 0, "other": 0}
        self.page_usage = {"i": {}, "dy": {}, "ol": {}}
        self.valid_words: dict = {}
        self.lines_in_page = 0
        self.lines_in_paragraph = 0

    def new_line(self):
        self.lines_in_page += 1
        self.lines_in_paragraph += 1

    def new_paragraph(self):
        self.lines_in_paragraph = 0

    def new_page(self):
        self.lines_in_page = 0
        self.lines_in_paragraph = 0
        self.page_usage = {"i": {}, "dy": {}, "ol": {}}

    def remember(self, word: Word):
        if word.tag == INITIAL or (
            is_valid(word) and len(word.tokens) < self.max_word_tokens and word.tag != COMBINE
        ):
            self.valid_words.setdefault(word.text, word)
        cls = word.type_class()
        self.counts[cls] += 1
        if cls in self.page_usage:
            self.page_usage[cls][word.text] = self.page_usage[cls].get(word.text, 0) + 1
        for other in self.consecutive:
            self.consecutive[other] = self.consecutive[other] + 1 if other == cls else 0

    def _proportion(self, cls: str) -> float:
        total = sum(self.counts.values())
        return self.counts[cls] / total if total else 0.0

    def has_suggestions(self) -> bool:
        if self.currier == "B":
            return self._proportion("i") < 0.20 or self._proportion("dy") < 0.25
        return self._proportion("i") < 0.20 or self._proportion("ol") < 0.25

    def _top_or_default(self, cls: str) -> Word:
        defaults = TYPE_DEFAULTS_B if self.currier == "B" else TYPE_DEFAULTS_A
        usage = self.page_usage.get(cls, {})
        if usage:
            best = max(usage, key=usage.get)  # first-max tie-break (insertion order)
            return Word.parse(best, SUGGEST)
        return Word.parse(defaults[cls], SUGGEST)

    def suggest(self) -> Word | None:
        watched = "dy" if self.currier == "B" else "ol"
        if self._proportion("i") < 0.20:
            return self._top_or_default("i")
        if self._proportion(watched) < 0.25:
            return self._top_or_default(watched)
        return None

    def suggest_force(self, try_count: int) -> list:
        first, second = FORCE_ROTATION[self.currier][try_count % 3]
        pair = [self._top_or_default(first), self._top_or_default(second)]
        if try_count < 12:
            suggested = self.suggest()
            if suggested is not None:
                pair[0] = suggested
        return pair


# ---------------------------------------------------------------------------
# §7 — Source selection (PageSourceGroupChooser)
# ---------------------------------------------------------------------------


class PageSourceChooser:
    SAME_POSITION_PROBABILITY = 28
    PARAGRAPH_INITIAL_PROBABILITY = 70
    SUGGESTION_PROBABILITY = 40

    def __init__(self, rng: Rand, stats: Stats):
        self.rng = rng
        self.stats = stats

    def choose(self, lines, paragraph_initial_lines, current_line,
               is_par_initial, initial_line_count) -> list:
        mode = "LOCAL"
        if len(lines) < initial_line_count:
            mode = "RANDOM"
        r = self.rng(100)  # drawn unconditionally (spec §7 RNG-stream note)
        if (
            is_par_initial
            and len(paragraph_initial_lines) >= 2
            and (len(current_line) == 0 or (len(current_line) >= 2 and r < self.PARAGRAPH_INITIAL_PROBABILITY))
        ):
            mode = "PARAGRAPH_INITIAL"
        if self.stats.has_suggestions():
            if self.rng(100) < self.SUGGESTION_PROBABILITY:
                mode = "SUGGESTION"

        if mode == "SUGGESTION":
            suggested = self.stats.suggest()
            if suggested is not None:
                return [suggested, self._random_word()]
            mode = "LOCAL"
        if mode == "RANDOM":
            return [self._random_word(), self._random_word()]
        if mode == "PARAGRAPH_INITIAL":
            line = paragraph_initial_lines[self.rng(len(paragraph_initial_lines))]
            pos = self.rng(len(line))
        else:  # LOCAL
            span = max(2, self.stats.lines_in_page) - 2
            index = len(lines) - (1 + self.rng(span))
            if index < 0:
                index = len(lines) - 1
            line = lines[index]
            threshold = (
                self.SAME_POSITION_PROBABILITY
                if current_line
                else max(10, self.SAME_POSITION_PROBABILITY // 2)
            )
            if self.rng(100) <= threshold:
                pos = self._calc_line_position(current_line, line)
            else:
                pos = self.rng(len(line))
        first = line[pos]
        if pos + 1 < len(line):
            second = line[pos + 1]
        elif pos - 1 >= 0:
            second = line[pos - 1]
        else:
            second = line[pos]
        return [self._strip_initial_gallow(first), self._strip_initial_gallow(second)]

    def _random_word(self) -> Word:
        words = list(self.stats.valid_words.values())
        if not words:
            return Word.parse("daiin", SUGGEST)
        return words[self.rng(len(words))]

    @staticmethod
    def _calc_line_position(current_line, source_line) -> int:
        writing_position = sum(len(w.text) + 1 for w in current_line)
        accumulated = 0
        for i, word in enumerate(source_line):
            accumulated += len(word.text) + 1
            if accumulated >= writing_position:
                return i
        return min(len(source_line) - 1, len(current_line))

    @staticmethod
    def _strip_initial_gallow(word: Word) -> Word:
        if word.tokens and word.tokens[0] in GALLOWS and len(word.tokens) > 1:
            return Word(word.tokens[1:], word.tag)
        return word


# ---------------------------------------------------------------------------
# §9 — Assembly (SelfCitationTextGenerator)
# ---------------------------------------------------------------------------

SEED_LINE_B = "pchal shal shorchdy okeor okain shedy pchedy qotchedy qotar ol lkar"  # f103v.P.9
SEED_LINE_A = "fachys ykal ar ataiin shol shory cthres y kor sholdy"  # f1r.P.1


@dataclass(frozen=True)
class SelfCitationConfig:
    lines_to_create: int = 1200
    max_line_length: int = 55
    min_line_length: int = 15
    lines_per_page: int = 29
    max_repeat_count: int = 3
    initial_line: str = SEED_LINE_B
    morph: MorphConfig = field(default_factory=MorphConfig)

    @property
    def currier(self) -> str:
        """B iff any seed line contains 'ed' (spec §9.1); no other switch exists."""
        return "B" if "ed" in self.initial_line else "A"


@dataclass
class GeneratedText:
    lines: list  # list[list[str]]
    line_meta: list  # per line: {"page": int, "paragraph": int, "paragraph_initial": bool}
    config: dict
    seed: int

    def to_plain_lines(self) -> list:
        return [" ".join(words) for words in self.lines]


class SelfCitationGenerator:
    def __init__(self, config: SelfCitationConfig, seed: int):
        self.config = config
        self.seed = seed
        self.rng = Rand(seed)
        self.stats = Stats(config.currier)
        self.morpher = Morpher(self.rng, config.morph)
        self.chooser = PageSourceChooser(self.rng, self.stats)
        self.lines: list = []
        self.paragraph_initial_lines: list = []
        self.last_generated: Word | None = None

    def generate(self) -> GeneratedText:
        seed_lines = [s.strip() for s in self.config.initial_line.split("#") if s.strip()]
        for seed_line in seed_lines:
            words, used = [], 0
            for text in seed_line.split():
                if used < self.config.max_line_length:
                    words.append(Word.parse(text, INITIAL))
                used += len(text) + 1
            for word in words:
                self.stats.remember(word)
            self.lines.append(words)
            self.paragraph_initial_lines.append(words)
        if sum(len(line) for line in self.lines) < 6:
            extras = ("daiin", "ol", "chedy" if self.config.currier == "B" else "cheody")
            for text in extras:
                self.stats.remember(Word.parse(text, INITIAL))
        self.stats.lines_in_page = len(seed_lines)
        self.stats.lines_in_paragraph = len(seed_lines)

        meta = [
            {"page": 0, "paragraph": 0, "paragraph_initial": i == 0}
            for i in range(len(seed_lines))
        ]
        page, paragraph = 0, 0
        total = self.config.lines_to_create
        for i in range(len(seed_lines), total):
            is_par_initial = self.stats.lines_in_paragraph == 0
            if is_par_initial:
                paragraph += 1
            self.stats.new_line()
            paragraph_final = False
            page_break = False
            if self.stats.lines_in_page == self.config.lines_per_page or i == total - 1:
                paragraph_final = True
                page_break = True
            elif (
                self.stats.lines_in_page < self.config.lines_per_page - 2
                and self.stats.lines_in_paragraph > 3
                and i < total - 2
            ):
                if self.rng(100) < self.stats.lines_in_paragraph * 10:
                    paragraph_final = True
            line = self._generate_line(is_par_initial, paragraph_final)
            self.lines.append(line)
            if is_par_initial:
                self.paragraph_initial_lines.append(line)
            meta.append(
                {"page": page, "paragraph": paragraph, "paragraph_initial": is_par_initial}
            )
            if page_break:
                page += 1
                self.stats.new_page()
            elif paragraph_final:
                self.stats.new_paragraph()

        config_dict = asdict(self.config)
        config_dict["currier"] = self.config.currier
        return GeneratedText(
            lines=[[w.text for w in line] for line in self.lines],
            line_meta=meta,
            config=config_dict,
            seed=self.seed,
        )

    def _generate_line(self, is_par_initial: bool, paragraph_final: bool) -> list:
        max_length = self.config.max_line_length
        if paragraph_final:
            max_length = max(self.config.min_line_length, self.rng(max_length))
        line: list = []
        line_length = 0
        tries = 0
        count = 0
        while line_length + max(tries - 3, 0) < max_length:
            count += 1
            available = max_length - line_length
            sources = self.chooser.choose(
                self.lines, self.paragraph_initial_lines, line,
                is_par_initial, initial_line_count=1,
            )
            use = True
            if len(sources[0].tokens) > 5:
                use = len(sources[0].text) < 4 + self.rng(4)
            if sources[0].tag == COMBINE:
                if len(sources) > 1 and sources[1].tag == COMBINE:
                    use = False
                elif self.rng(100) < 30:
                    use = False
            force = False
            if (not use and count > 100) or count > 105:
                if count > 130:
                    raise RuntimeError("line generation livelock")
                sources = self.stats.suggest_force(count - 100)
                use = True
                force = count > 110
            if not use:
                continue
            self.morpher._previous_word = self.last_generated
            morphed = self.morpher.morph(
                sources, self.last_generated, is_par_initial, is_line_initial=not line
            )
            if not morphed:
                continue
            if not force:
                head = morphed[0]
                if not has_valid_start(head):
                    continue
                if line and head.text == line[-1].text:
                    if self.rng(100) >= 50:
                        continue
                elif self.stats.consecutive[head.type_class()] >= self.config.max_repeat_count:
                    continue
            count = 0
            for word in morphed:
                available = max_length - line_length
                if available - len(word.text) <= 0:
                    trimmed = self._try_trim(word, available)
                    word = trimmed if trimmed is not None else word
                if available - len(word.text) > 0:
                    line.append(word)
                    self.stats.remember(word)
                    self.last_generated = word
                    line_length += len(word.text) + (1 if line_length else 0)
                    tries = 0
                else:
                    tries += 1
        return line

    def _try_trim(self, word: Word, available: int) -> Word | None:
        tokens = list(word.tokens)
        changed = False
        if tokens and tokens[-1] in FINAL_LINE_REPLACEMENTS:
            replacement = tokenize(FINAL_LINE_REPLACEMENTS[tokens[-1]])
            tokens[-1:] = replacement
            changed = True
        while available - len("".join(tokens)) <= 0:
            shorter = self._search_shorter_glyph(tokens)
            if shorter is None:
                break
            pos, replacement = shorter
            tokens[pos : pos + 1] = [replacement]
            changed = True
        while available - len("".join(tokens)) <= 0 and len(tokens) > 2:
            tokens.pop(0)
            changed = True
        if not changed or not tokens:
            return None
        return Word(tuple(tokens), SHORTEN)

    @staticmethod
    def _search_shorter_glyph(tokens):
        best = None
        for pos, token in enumerate(tokens):
            for candidate, _ in SUBSTITUTIONS.get(token, ()):
                candidate_tokens = tokenize(candidate)
                if len(candidate_tokens) == 1 and len(candidate) < len(token):
                    if best is None or len(candidate) < len(best[1]):
                        best = (pos, candidate)
        return best


# ---------------------------------------------------------------------------
# CLI (L3: outputs carry a provenance manifest)
# ---------------------------------------------------------------------------


def main(argv=None) -> int:
    from ..dataset import git_commit

    parser = argparse.ArgumentParser(description="Generate H3 self-citation text")
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--lines", type=int, default=1200)
    parser.add_argument("--dialect", choices=("A", "B"), default="B")
    parser.add_argument("--out-dir", type=Path,
                        default=Path(__file__).resolve().parents[3]
                        / "data" / "processed" / "harness" / "h3")
    args = parser.parse_args(argv)

    config = SelfCitationConfig(
        lines_to_create=args.lines,
        initial_line=SEED_LINE_B if args.dialect == "B" else SEED_LINE_A,
    )
    result = SelfCitationGenerator(config, seed=args.seed).generate()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"selfcitation_{args.dialect}_seed{args.seed}_lines{args.lines}"
    (args.out_dir / f"{stem}.txt").write_text("\n".join(result.to_plain_lines()) + "\n")
    manifest = {
        "generator": "ms408.harness.selfcitation",
        "git_commit": git_commit(),
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "seed": args.seed,
        "config": result.config,
        "line_meta": result.line_meta,
    }
    (args.out_dir / f"{stem}_manifest.json").write_text(json.dumps(manifest) + "\n")
    tokens = [w for line in result.lines for w in line]
    summary = {
        "lines": len(result.lines),
        "tokens": len(tokens),
        "types": len(set(tokens)),
        "output": str(args.out_dir / f"{stem}.txt"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
