"""IVTFF (Intermediate Voynich Transliteration File Format) parser.

Parses IVTFF 2.0 files as distributed at voynich.nu (spec: data/raw/specs/IVTFF_format.pdf).

Design rules:
- Locus text is preserved verbatim in `Locus.text`. Nothing is silently normalized.
- All cleaning is explicit via `TextPolicy`; every policy choice is a named field so
  analyses can state (and vary) exactly which reading conventions they used.

Page header variables (spec Table 6):
    $Q quire  $P page-in-quire  $F folio-in-quire  $B bifolio
    $I illustration type (A/B/C/H/P/S/T/Z)  $L Currier language (A/B)
    $H writing hand = Fagin Davis scribes 1-5 ('@' = overridden by in-line <@H=n> tags)
    $C Currier hand  $X extraneous writing

Locus locator (e.g. "@P0", "+P0", "=Pt"): first char is the continuation/position code,
remainder is the locus type (P* paragraph text, L* labels, C* circular, R* radial).
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

FILE_HEADER_RE = re.compile(r"^#=IVTFF\s+(?P<alphabet>\S+)\s+(?P<version>\S+)")
PAGE_RE = re.compile(r"^<(?P<name>[^.,>\s]+)>\s*(?:<!(?P<vars>.*)>)?\s*$")
LOCUS_RE = re.compile(r"^<(?P<page>[^.,>\s]+)\.(?P<num>\d+),(?P<locator>[^>]+)>\s*(?P<text>.*)$")
VAR_RE = re.compile(r"\$(\w)=(\S+)")

_INLINE_COMMENT_RE = re.compile(r"<![^>]*>")
_INLINE_TAG_RE = re.compile(r"<[^>]*>")  # <%>, <$>, <->, <~>, <@H=2>, ...
_ALT_READING_RE = re.compile(r"\[([^:\[\]]*)((?::[^:\[\]]*)+)\]")  # [a:b] or [a:b:c]


@dataclass(frozen=True)
class TextPolicy:
    """Explicit reading conventions applied when cleaning raw locus text."""

    first_alternative: bool = True  # [a:b] -> a (else b, the last alternative)
    comma_is_word_break: bool = True  # ',' (uncertain space) treated like '.'
    strip_braces: bool = True  # {ck} -> ck (keep contents, drop grouping)
    drop_uncertain_words: bool = False  # drop words containing '?' (illegible char)


DEFAULT_POLICY = TextPolicy()


@dataclass
class Locus:
    page: str
    num: int
    locator: str
    text: str  # verbatim from file

    @property
    def continuation(self) -> str:
        return self.locator[0]

    @property
    def locus_type(self) -> str:
        return self.locator[1:]

    def clean(self, policy: TextPolicy = DEFAULT_POLICY) -> str:
        return clean_text(self.text, policy)

    def words(self, policy: TextPolicy = DEFAULT_POLICY) -> list[str]:
        return words(self.text, policy)


@dataclass
class Page:
    name: str
    variables: dict[str, str] = field(default_factory=dict)
    loci: list[Locus] = field(default_factory=list)

    @property
    def illustration_type(self) -> str | None:
        return self.variables.get("I")

    @property
    def currier_language(self) -> str | None:
        return self.variables.get("L")

    @property
    def hand(self) -> str | None:
        """Fagin Davis scribe assignment ('1'-'5', or '@' = varies within page)."""
        return self.variables.get("H")


@dataclass
class IVTFFDocument:
    alphabet: str
    version: str
    pages: list[Page]

    @property
    def loci(self) -> list[Locus]:
        return [locus for page in self.pages for locus in page.loci]

    def page(self, name: str) -> Page:
        for p in self.pages:
            if p.name == name:
                return p
        raise KeyError(name)

    def variable_counts(self, var: str) -> Counter:
        """Distribution of a page variable; pages lacking it count under None."""
        return Counter(p.variables.get(var) for p in self.pages)

    @classmethod
    def parse(cls, text: str) -> "IVTFFDocument":
        alphabet = version = ""
        pages: list[Page] = []
        current: Page | None = None
        for lineno, line in enumerate(text.splitlines(), start=1):
            line = line.rstrip()
            if not line:
                continue
            if line.startswith("#=IVTFF"):
                m = FILE_HEADER_RE.match(line)
                if not m:
                    raise ValueError(f"line {lineno}: malformed IVTFF header: {line!r}")
                alphabet, version = m.group("alphabet"), m.group("version")
                continue
            if line.startswith("#"):
                continue
            m = LOCUS_RE.match(line)
            if m:
                if current is None or m.group("page") != current.name:
                    raise ValueError(
                        f"line {lineno}: locus for {m.group('page')!r} outside its page block"
                    )
                current.loci.append(
                    Locus(
                        page=m.group("page"),
                        num=int(m.group("num")),
                        locator=m.group("locator"),
                        text=m.group("text"),
                    )
                )
                continue
            m = PAGE_RE.match(line)
            if m:
                variables = dict(VAR_RE.findall(m.group("vars") or ""))
                current = Page(name=m.group("name"), variables=variables)
                pages.append(current)
                continue
            raise ValueError(f"line {lineno}: unrecognized line: {line!r}")
        if not alphabet:
            raise ValueError("missing #=IVTFF file header")
        return cls(alphabet=alphabet, version=version, pages=pages)

    @classmethod
    def load(cls, path: str | Path) -> "IVTFFDocument":
        return cls.parse(Path(path).read_text(encoding="utf-8", errors="strict"))


def clean_text(raw: str, policy: TextPolicy = DEFAULT_POLICY) -> str:
    """Reduce raw locus text to transliteration characters plus word breaks."""
    s = _INLINE_COMMENT_RE.sub("", raw)
    s = _INLINE_TAG_RE.sub("", s)

    def pick(m: re.Match) -> str:
        first = m.group(1)
        alternatives = m.group(2).lstrip(":").split(":")
        return first if policy.first_alternative else alternatives[-1]

    s = _ALT_READING_RE.sub(pick, s)
    if policy.strip_braces:
        s = s.replace("{", "").replace("}", "")
    return s.strip()


def words(raw: str, policy: TextPolicy = DEFAULT_POLICY) -> list[str]:
    """Split cleaned locus text into word tokens."""
    s = clean_text(raw, policy)
    if policy.comma_is_word_break:
        s = s.replace(",", ".")
    tokens = [t for t in s.split(".") if t]
    if policy.drop_uncertain_words:
        tokens = [t for t in tokens if "?" not in t]
    return tokens
