# T03 — Self-Citation Text Generator (Timm & Schinner): Reimplementation Spec

Harness class **H3** (RESEARCH-PLAN §3). Target module: `src/ms408/harness/selfcitation.py`.
Written 2026-07-05 from primary sources (see §1); consume-only (L19) — author code and paper live in
the session scratchpad and `data/raw/`, never in this repo.

This spec is intended to be sufficient to reimplement the generator **without** the original code.
Where behavior is quirky (off-by-one thresholds, dead code, Java-container ordering), the quirk is
documented explicitly with a fidelity note, because our reimplementation must decide whether to
reproduce or rationalize it (§15, §16).

---

## 1. Sources and provenance

| Source | Role | Version pinned |
|---|---|---|
| `github.com/TorstenTimm/SelfCitationTextgenerator` | **Authoritative algorithm + all parameters** (Java, companion to the 2020 Cryptologia paper). | commit `a6ede2202dd7ad6285ce2c007bf22c2a0e7709b7` (2019-11-29) |
| `github.com/TorstenTimm/VoynichTextGenerator` | Older iOS/Swift variant ("previous version" per author README). Consult-only — **no license file** (§13). | commit `13f73a808ee1a782d5a5ff22a9c5d582cbf60c75` (2019-05-13) |
| arXiv:1407.6639 (v3), Timm, "How the Voynich Manuscript was created" | Free description of the self-citation hypothesis and the qualitative mechanism. **Contains no formal algorithm and no parameter values.** | v3 (latest) |
| Timm & Schinner (2020), "A possible generating algorithm of the Voynich manuscript", *Cryptologia* 44(1):1–19, DOI 10.1080/01611194.2019.1596999 | Formalizes the method; paywalled (T&F 403s bots). Abstract confirmed via Semantic Scholar API. | unread in full (§16 R1) |
| Zenodo DOI 10.5281/zenodo.2531632 | Archived snapshot of the Java repo (badge in repo README). Use as citable frozen artifact. | — |
| arXiv:1601.07435, Timm, "Co-Occurrence Patterns in the Voynich Manuscript" | Supporting statistics on spatial clustering of similar words (optional validation reading). | v2 |

Key structural fact: **every concrete number in this spec comes from the Java code and its shipped
`conf.properties`**, not from the papers. The arXiv paper motivates the mechanism; the code defines it.

Files referenced below (paths relative to the Java repo):

- `source/src/main/java/de/voynich/text/SelfCitationTextGenerator.java` — main loop, line/paragraph/page assembly
- `.../Glyph.java` — glyph inventory, all substitution tables (the core data; fully transcribed in §5)
- `.../GlyphGroup.java` — word object + tokenizer
- `.../Substitution.java` — (tokens[], cumulative-probability) pair
- `.../Constants.java` — hard defaults
- `.../StatisticHelper.java` — running statistics, suggestion mechanism, Currier A/B switch
- `.../morph/SlimGroupMorpher.java`, `.../morph/AbstractBaseGroupMorpher.java` — all morph operations
- `.../sourcechooser/PageSourceGroupChooser.java`, `.../sourcechooser/ChooserHelper.java` — self-citation source selection
- `.../canfollow/CurveLineCanFollow.java` — glyph-adjacency ("curve/line") rules
- `.../util/Config.java`, `executable/conf.properties`, `PROPERTIES.md` — parameters
- `.../util/random/PseudoRandomNumberGenerator.java` — RNG
- `executable/generate/generated_text.txt` — **committed reference output** (seed 19, default config)
- `.../canfollow/vms/VoynichGroups*.java` — VMS word-type dictionaries (~8k lines), used only by the
  non-default `voynich` canFollow mode; do not transcribe, point here if ever needed.

---

## 2. Scope

Reimplement the **default configuration** of the Java generator (the configuration that produced the
author's published analyzed text): `method.morph=slim`, `method.canFollow=curveline`,
`method.sourceChooser=page`, `method.suggestions=top`, pseudo-RNG. The code contains alternative
strategies (canFollow: `statistic`/`voynich`/`none`; sourceChooser: `position`/`random`; suggestions:
`daiin`/`random`/`none`; morph: only `slim` is wired). These are out of scope for T03; the plugin
points in §15 keep the door open.

Output contract: EVA-alphabet lowercase text, words separated by single spaces, one line per text
line, lines grouped into paragraphs and 29-line pages (paragraph/page boundaries must be recoverable
— see §15).

---

## 3. Algorithm overview

The generator emulates a scribe who writes meaningless but Voynich-like text by **copying a word he
can already see on the page and modifying it slightly** before writing it down ("self-citation").

State:
- `lines` — list of already-generated lines, each a list of words (GlyphGroups)
- `paragraph_initial_lines` — subset of `lines` that started a paragraph
- `stats` — running counters: token counts by type-class (i / dy / ol / other), per-page and
  per-document usage maps, consecutive-repeat counters, lines-in-page, lines-in-paragraph
- `valid_words` — dictionary of every acceptable word generated so far (used for random fallback)

Per new word:
1. **Choose source word(s)** from previously generated text (usually a nearby line on the same page;
   sometimes the same writing position in an earlier line; for paragraph-initial lines, from earlier
   paragraph-initial lines; occasionally a "suggestion" injected to keep type-class frequencies on
   target). Two consecutive source words are returned (`source[0]`, `source[1]`).
2. **Morph** `source[0]` by one of three operation families — add/remove a prefix or gallow glyph,
   combine with `source[1]` / split into two words, or replace 1–3 tokens by "similar" tokens using
   weighted substitution tables — subject to glyph-adjacency legality (the "curve/line" rules).
3. **Accept/reject** the morphed word(s): line-length budget, repeated-word damping, per-type-class
   repeat caps, then append to the line and update statistics.

Lines are filled to a character budget (55), paragraphs end stochastically after ≥4 lines (with the
last line shortened), pages have exactly 29 lines. Paragraph-initial lines get gallows-heavy
decoration (EVA p/f); line-initial and line-final positions get their own glyph preferences. All of
this makes the output reproduce Voynich positional statistics, not just word statistics.

Everything below specifies these steps exactly.

---

## 4. Tokenization and glyph inventory

Words are strings over the EVA lowercase alphabet. Internally every word is a list of **tokens**
(glyphs or ligature-like multi-glyph units). Tokenization (`GlyphGroup.parse()`):

- Scan left to right. At each position, if the remaining string starts with a token from the
  **ligature set** below, consume that token; otherwise consume a single character.
- Special case: a string starting with `eee` is tokenized as `eee` (checked before the general set,
  because `ee` would also match).

Ligature set (42 entries, `Glyph.ligatureStrings`):

```
ol or al ar dy qo ch sh cs
ee eee
cth cthh ckh ckhh cph cfh
ith ikh iph ifh
eke ete
in iin iiin  ir iir iiir  is iis iiis  il iil iiil  im iim iiim
om am og ag
```

> **Fidelity warning (F1):** the Java lookup iterates a `HashMap.keySet()` — for overlapping tokens
> (`ckh` vs `ckhh`, `cth` vs `cthh`, `in` vs `iin` after an `i` is consumed, etc.) match order is the
> JVM's hash order, not longest-first. In practice, use **longest-match-first**; that is the evident
> intent (the explicit `eee` special case exists precisely because hash order broke it). Flag any
> observable divergence in tests. See §16 R3.

Glyph classes (`Glyph.java`):

| Class | Members | Used for |
|---|---|---|
| gallows | `k t p f` | prefix/infix insertion; `p f` are "first-line gallows" (paragraph-initial lines), `k t` ordinary |
| line-initial glyphs | `o y d s` | preferred first glyph of a line |
| line-final glyphs | `m g` | preferred last glyph of a line |
| prefix glyphs | `l o y ch sh q d x` | addable word prefixes (see prefix table below) |
| combinable ligatures | `ol al or ar` (+`om am` in "all" variant) | word-joining pivots |
| e-family / i-family | `e ee` / `in iin iiin` | curve/line adjacency classes (§6) |
| ol-family | `ol al or ar` | "ol-type" word classification |

Prefix admissibility (`Glyph.prefixGlyphsStrings`) — a prefix may be added only if the word's first
token is in the listed set:

| Prefix | Allowed first tokens of the word |
|---|---|
| `l` | `k t p f d ch sh o a e i o` (sic — `o` listed twice) |
| `o` | `k t p f d ch sh` |
| `y` | `k t p f d ch sh` |
| `ch` | `k t p f d ol or al ar` |
| `sh` | `k t p f d ol or al ar` |
| `q` | *(none — special-cased: `q` only forms `qo` by replacing a leading `o`/`y`, §8.2)* |
| `d` | `a` |
| `x` | `ol or al ar` |

Combinable-ligature deletion table (`allCombinableLigature`): after joining word1+word2 where word1
ends in one of `ol al or ar om am`, delete word2's first token if it is `l`, `r`, or `s`
(prevents e.g. `ol`+`l…`).

Positional replacement tables:

- `finalLineReplacements` (applied when trimming the last word of a line, §9.4):
  `ol→om, or→om, al→am, ar→am, om→og, am→ag, im→mg, in→n, iin→im, iiin→im`
- `ingroupGlyphReplacements` (word-internal form when self-combining, §8.4):
  `y→o, m→r, g→r, n→r, in→ir, iin→iir, dy→da`
- `groupFinalGlyphReplacements` (word-final form when self-combining):
  `o→y, a→y, k→t, t→k, p→f, f→p`

---

## 5. Substitution tables (the "similar glyph" weights)

`Substitution(tokens[], p)` = replacement candidate; `p` is a **cumulative percentage threshold**.
Selection (`SlimGroupMorpher.choose`): draw `r = rand(100)` (uniform 0–99), take the **first** entry
in list order with `p > r`. So consecutive thresholds encode a discrete CDF; e.g. for `k`:
t 77%, p 17%, f 6%.

### 5.1 General substitution map (`Glyph.substitutionObjects`) — verbatim

Format: `source → candidate(threshold), …`; a candidate written `a+b` is a multi-token replacement.

```
k    → t(77) p(94) f(100)
t    → k(84) p(96) f(100)
p    → k(59) t(97) f(100)
f    → k(56) t(92) p(100)

in   → n(8) iin(84) iiin(87) ir(97) iir(98) iis(99) il(100)
iin  → n(13) in(70) iiin(74) ir(92) iir(97) is(99) il(100)
iiin → n(6) in(31) iin(90) ir(98) iir(100)

ir   → r(6) in(33) iin(95) iiin(97) iir(99) iiir(100)
iir  → r(6) in(30) iin(89) iiin(91) ir(99) iiir(100)
iiir → ir(90) iir(100)

is   → in(50) iis(100)
iis  → iin(50) is(100)

il   → in(50) iil(100)
iil  → iin(50) il(99) iiil(100)
iiil → il(66) iil(100)

im   → in(30) iin(100)
iim  → in(30) iin(100)
iiim → in(30) iin(100)

om   → ol(45) or(94) og(98) omg(100)
am   → al(45) ar(94) ag(98) amg(100)
og   → or(30) al(63) ar(100)
ag   → ol(48) or(72) ar(100)

ol   → or(30) al(63) ar(100)
or   → ol(47) al(73) ar(100)
al   → ol(48) or(72) ar(100)
ar   → ol(49) or(73) al(100)

e    → e(50) ee(99) eee(100)
ee   → ch(40) ch+e(50) e(98) eee(100)
eee  → ch(10) ch+e(20) ee(65) e(100)

ch   → ee(10) ch+e(20) sh(90) ckh(97) cth(100)
sh   → ee(10) ch(90) ckh(97) cth(100)

ckh  → cth(30) k+ch(50) t+ch(70) eke(72) ete(74) cph(78) ch(100)
cth  → ckh(30) k+ch(50) t+ch(70) eke(72) ete(74) cph(78) cfh(80) ch(100)

cs   → sh(100)
ckhh → ckh(100)
cthh → cth(100)
ikh  → ckh(100)   ith → cth(100)   iph → cph(100)   ifh → cfh(100)

eke  → ckh(30) cth(50) k+ee(56) t+ee(60) ete(65) ee(100)
ete  → ckh(30) cth(50) k+ee(56) t+ee(60) eke(65) ee(100)

cph  → ckh(40) cth(75) cfh(80) ch(100)
cfh  → ckh(40) cth(75) cph(80) ch(100)

y    → o(100)
o    → y(100)

n    → r(50) in(63) iin(100)
l    → r(100)
r    → r(50) s(100)
g    → m(100)
s    → r(75) d(100)
d    → d(90) s(100)
a    → a(98) o(100)
qo   → o(80) y(100)
```

Note the self-substitutions (`e→e` 50%, `d→d` 90%, `a→a` 98%, `r→r` 50%): these are deliberate
no-op weights — the replace operation then counts as "failed" for that position and tries another
position, which shapes the effective replacement distribution.

### 5.2 Word-final substitution map (`combinableFinalSubstitutionObjects`) — verbatim

Used instead of §5.1 when replacing the **last token** of a word on retry (see §8.5 condition), if
`method.morph.use_word_final_substitutions=true` (default):

```
om → o(8) y(30) ol(75) or(100)
am → o(4) y(30) al(70) ar(100)
og → o(8) y(30) or(55) al(80) ar(100)
ag → o(4) y(30) ol(65) or(80) ar(100)

ol → o(8) y(30) or(54) al(81) ar(100)
or → o(8) y(30) ol(63) al(81) ar(100)
al → o(4) y(30) ol(64) or(81) ar(100)
ar → o(4) y(30) ol(64) or(82) al(100)

y  → o(20) ol(44) or(60) al(75) ar(100)
o  → y(20) ol(44) or(60) al(75) ar(100)

d  → dy(70) d(100)
dy → d(10) dy(100)
```

### 5.3 Random glyph draws

`randomGallow(firstLine)` — one draw `r = rand(100)`:
- `firstLine=true` (paragraph-initial line): `k` 35% (r≤34), `t` 15% (r≤49), `p` 40% (r≤89), `f` 10% (r≤99)
- `firstLine=false`: `k` 75%, `t` 25% (the p/f branches fall back to k/t)

`randomLineInitalGlyph()` — `r = rand(100)`: `o` 46% (r≤45), `y` 30% (r≤75), `d` 15% (r≤90), `s` 9% (r≤99).

`choosePrefix(j, previousGroup, alreadyTried)` — one draw `r = rand(100)` per attempt `j` (0–6):
- If `j==0` and the **previous generated word** ends with token `dy` and `r<90` → `q`.
  (This is what makes `qo…` words follow `…dy` words, a signature Voynich bigram pattern.)
- Else first match in this cascade, skipping prefixes already tried:
  `r<5`→`l`, `r<34`→`o`, `r<40`→`y`, `r<61`→`ch`, `r<72`→`sh`, `r<88`→`q`, `r<99`→`d`,
  else (`r==99`, only when `j==0`)→`x`; final fallback `o`.

---

## 6. Glyph-adjacency rules — `CurveLineCanFollow` (default)

Implements Timm's "curve/line theorem": tokens built on the curved stroke *c/e* and tokens built on
the straight stroke *i* form two families; membership determines which token may follow which.

Token classes (verbatim lists):

```
startGlyphList      = qo a o y c s d k t p f x     # legal word-initial tokens
finalGlyphList      = y n l r s d m g x            # legal word-final glyphs (suffix match)
ccTokenList (curve–curve) = e h d s y o ch sh ckh cth cph cfh al ol x l
cFinalTokenList     = d g o y dy s om am og ag al ar ol or x
clTokenList (curve–line)  = a
lcTokenList (line–curve)  = ikh ith iph ifh
llTokenList (line–line)   = i
lFinalTokenList     = n in iin iiin r ir iir iiir m im iiil iil il iis is
gallowTokenList     = k t p f
afterGallowTokenList= a e o y h ch sh              # what may follow a gallow
beforeGallowTokenList = "" a e o l y h             # what a gallow may follow ("" = word start)
aoyTokenList        = a o y
rmngTokenList       = r m n g
```

Type resolution:
- `endType(tok)`: "" → EMPTY; ends-with any of `clTokenList`∪`llTokenList` → LINE; else ends-with any
  `ccTokenList`∪`lcTokenList` → CURVE; else ends-with any `finalGlyphList` → FINAL; else ends-with
  gallow → GALLOW; else NONE. (Checked in that order; suffix matching.)
- `startType(tok)`: "" → EMPTY; starts-with any `llTokenList`∪`lcTokenList`∪`lFinalTokenList` → LINE;
  else starts-with any `ccTokenList`∪`clTokenList`∪`cFinalTokenList` → CURVE; else starts-with gallow
  → GALLOW; else NONE. (Prefix matching, in that order.)

`canFollowBefore(add, rest)` — may token `add` be placed immediately before string `rest`:
1. If `add` ∈ combinable ligatures (`ol al or ar om am`) and `rest` starts with `a|o|y` → **true**.
2. If `rest` starts with a combinable ligature and `add` ends with `r|m|n|g` → **true**.
3. If `add` ≠ "" and `rest`.startswith(`add`) → **false** (no immediate doubling).
4. If `rest` == "" (word end) and word-final substitutions enabled: **true** iff `add` ∈
   `lFinalTokenList` ∪ `cFinalTokenList`, else false.
5. Else switch on `endType(add)`:
   - EMPTY (word start): true iff `rest` starts with an element of `startGlyphList`.
   - LINE: true iff `rest` starts with element of `lcTokenList`∪`lFinalTokenList`∪`llTokenList`.
   - CURVE: true iff `rest` starts with element of `ccTokenList`∪`clTokenList`∪`cFinalTokenList`∪gallows.
   - GALLOW: true iff `rest` starts with element of `afterGallowTokenList`.
   - FINAL: true iff `rest` == "".
   - NONE: false.

`canFollowAfter(head, add)` — may token `add` be appended after string `head`:
1. Combinable-ligature shortcuts mirroring rules 1–2 above (swap roles).
2. If `add` ≠ "" and `head`.endswith(`add`) → **false**.
3. If `head` == "" and word-final substitutions enabled: true iff `add` ∈ `startGlyphList` (exact).
4. Else switch on `startType(add)`:
   - EMPTY: true iff `head` ends with an element of `finalGlyphList` (word may end).
   - LINE: true iff `head` ends with element of `llTokenList`∪`clTokenList`.
   - CURVE: true iff `head` ends with element of `ccTokenList`∪`lcTokenList`∪gallows.
   - GALLOW: true iff `head` == "" or `head` ends with `a|e|o|l|y|h`.
   - NONE: false.

`isValid(word)`: word start passes `canFollowBefore("", word)` and every adjacent token pair passes
both `canFollowAfter(prev, next)` and `canFollowBefore(prev, next)`.

`hasValidStartGlyph(word)`: INITIAL words always valid; else `canFollowBefore("", word)`.

Error-rate escape hatch: if `method.canFollow.error_rate = E > 0`, a failed check is overridden with
probability `rand(100) ≤ E`. Default `E = 0` (no override, and the RNG is **not** drawn — draw only
happens when the check fails and E>0; keep this exact for RNG-stream fidelity).

---

## 7. Source-word selection — `PageSourceGroupChooser` (default)

Called once per candidate word with the full generation state. Returns exactly two source words.

Mode selection, in order (later checks override earlier):
1. Default mode = LOCAL.
2. If `len(lines) < initial_line_count` → RANDOM (only relevant right after seeding).
3. Draw `r = rand(100)`. If this is a paragraph-initial line, and ≥2 paragraph-initial lines exist,
   and (we are at the start of the line **or** (≥2 words already in current line and `r < 70`))
   → PARAGRAPH_INITIAL. (70 = `Constants.PARAGRAPH_INITIAL_PROBABILITY`; the draw happens
   unconditionally — RNG-stream note.)
4. If suggestions are pending (`stats.hasSuggestedGroups()`, §10) draw `r = rand(100)`; if
   `r < 40` (= `method.suggestions.probability`) → SUGGESTION.

Modes:
- **LOCAL** (`chooseFromPage`): pick line index
  `line = len(lines) - (1 + rand(max(2, linesInPage) - 2))`; if negative, use last line.
  (I.e. one of the last ~`linesInPage-2` lines — the visible page above the pen.) Then choose
  position: draw `r = rand(100)`; with `r ≤ P` use **same writing position** via
  `calcLinePosition` (below), else `pos = rand(len(source_line))`. `P` = 28
  (`method.sourceChooser.same_position_probability`) mid-line, `max(10, 28/2) = 14` when choosing
  the line's first word. Return `source_line[pos]` and its right neighbor (or left neighbor if at
  line end; or itself if the line has 1 word).
- **PARAGRAPH_INITIAL**: uniformly pick one of the previous paragraph-initial lines
  (`rand(len(paragraph_initial_lines))`), then `pos = rand(len(line))`, neighbor rule as above.
  (This is why paragraph-initial vocabulary — gallows-rich words — recirculates among paragraph
  starts.)
- **SUGGESTION**: `stats.suggestGroups()` (§10); if it returns a single word, append one word chosen
  by RANDOM as `source[1]`.
- **RANDOM**: two independent uniform draws from the keys of `valid_words`.
  > **Fidelity warning (F2):** the Java draws an index into `HashMap.keySet()` order —
  > JVM-hash-dependent. A Python reimplementation cannot reproduce this stream exactly; use
  > insertion order (dict) and validate distributionally (§14). Same issue in the suggestion
  > tie-break (§10) and `getFirstCombinableLigature` (4-key map, minor).

`calcLinePosition(current_line, source_line)`: writing position in characters =
`Σ (len(word)+1)` over words already in the current line; walk `source_line` accumulating
`len(word)+1` and return the first index where the accumulated length ≥ writing position; fallback
`min(len(source_line)-1, len(current_line))`.

Post-processing (`removeInitialGallow`): for each returned source word that **starts with a gallow
token**, strip that first token (if something remains). Sources are copied "as seen" minus their
paragraph decoration.

---

## 8. Morph operations — `SlimGroupMorpher` (default; only morpher wired in code)

Entry: `morphGroup(sources, previousGeneratedWord, isParagraphInitial, isLineInitial)` → list of 0–2
words. Every returned word carries a `generate_type` tag
(`INITIAL | ADD | DELETE | REPLACE | COMBINE | SPLIT | SHORTEN`) — COMBINE tags persist through later
modification and gate several rules; implement the tag.

### 8.1 Operation family selection

`L = len_chars(source[0])`. Draw `r = rand(100)` — **except** when `isParagraphInitial and
isLineInitial`, where `r := 0` without drawing (paragraph-initial first word always takes the
add path, feeding the gallow decoration).

- `r ≤ A` (default A=20, `add_remove.probability`) **and** source[0] is not COMBINE-tagged → **add/remove**
- else `r ≤ A + C` (default C=30, `combine_split.probability`) → **combine/split**
- else → **replace** (default effective 50%; enforced `replace ≥ 20`; A ≤ 80 clamp; if A+C > 80, C is
  clamped so replace keeps ≥20. Config warns unless A+C+replace=100.)

### 8.2 add/remove

If `L < 6`: try `addRandomGlyph`, else skip straight to remove-on-unchanged:
- `addRandomGlyph`: draw `r = rand(100)`; with `r < 80` (paragraph-initial) / `r < 8` (otherwise)
  try **addGallow** (§8.3), else **tryToAddPrefix**:
  - Up to 7 attempts; each attempt picks a prefix via §5.3 cascade (skipping already-tried).
  - Prefix `q`: only applies if word starts with token `o` or `y` → replace that token with `qo`.
  - Prefix `x`: only before `ol|or|al|ar` first token; prepend `x`.
  - Other prefixes: allowed iff word's first token ∈ prefix table (§4). Before prepending, if the
    word has >2 tokens and starts with `d|ch|sh`: draw a gallow (`randomGallow(false)`); if
    `canFollowBefore(gallow, token2)` and `canFollowAfter(prefix, gallow)` then with probability
    70% (`rand(100) < 70`) **replace** the first token with that gallow (this produces
    `o`+`daiin`→`okaiin`, `y`+`chol`→`ykol`). Then prepend the prefix. Tag ADD (COMBINE preserved).
- If nothing was added (word unchanged): **tryToDeletePrefix** — remove the first token if the word
  has >2 tokens and `canFollowBefore("", rest)`; if the remainder now starts with a gallow, draw
  `r = rand(100)` once: if next token starts with `a` and `r<50` → first token becomes `d`
  (`kain→dain`); if next token starts with `e` or `o` and `r<50` → becomes `ch` (`kedy→chedy`).
  Tag DELETE. If still unchanged → operation failed, return empty list.

### 8.3 addGallow / tryToPlaceGallow

`addGallow(word, isParagraphInitial, isLineInitial)`:
- Paragraph-initial **and** line-initial: `g = randomGallow(firstLine=True)`; try to place at
  position 0 (`tryToPlaceGallow`); if the result does not start with `g`, additionally prepend —
  before `g` — an `o` (if `canFollowBefore("o", word)`) else an `a` (same check), then `g` at front.
  (Produces `pochedy`-style paragraph openers.)
- Else if word has >1 token: if it already contains a gallow, skip with 90% probability
  (`rand(100) < 90` → no-op). Otherwise up to 5 attempts: position
  `pos = rand(tokens)` if paragraph-initial else (1 if tokens==2 else `1 + rand(tokens-2)`)
  (never position 0 mid-paragraph), gallow = `randomGallow(isParagraphInitial)`; accept first
  attempt whose placement changes the word.

`tryToPlaceGallow(g, word, pos)`:
- If token at `pos` is already a gallow → replace it with `g`.
- Else check `lastOk = canFollowAfter(token[pos-1] or "", g)` and
  `nextOk = canFollowBefore(g, token[pos] or "")`:
  - both → insert `g` at `pos`;
  - only lastOk and a token exists after `pos` → overwrite token at `pos` with `g` if
    `canFollowBefore(g, token[pos+1])`;
  - only nextOk and `pos-2 > 0` → overwrite token at `pos-1` with `g` if
    `canFollowAfter(token[pos-2], g)`;
  - else no-op.

### 8.4 combine / split

Draw `r = rand(100)`. Decide **combine** vs **split** (`L` = char length of source[0]):
- source[0] COMBINE-tagged → always split.
- `L < 6` → combine iff `L ≤ 2 or r < 96`;
- `L ≥ 6` → combine iff `r < 4 and L ≤ 8` (i.e. long words are split).

**Combine** (needs `source[1]`): take a left part of source[0] and a right part of source[1] via
`chooseSubgroupsForCombine`:
- left: whole word if ≤2 tokens, else the part before the first "split point";
- right: whole word if ≤3 tokens, else the part after the split point (or the first part if only
  one part came back).
- Split point (`calcSplitPosition`) = first index `i ≥ 1` where `not canFollowBefore(tok[i-1], tok[i])`
  **or** `tok[i-1]` is a combinable ligature **or** `tok[i]` is a gallow — but only if `i > 1` or
  `len(tok[0]) > 1`; else no split point (−1).
- Join: if left ends in `ol|al|or|ar|om|am`, drop a leading `l|r|s` from the right part. Require
  left char-length > 1, right nonempty with char-length > 1, combined char-length < 9, and
  (left-last is combinable ligature or `canFollowBefore(left_last, right_first)`) and
  `canFollowAfter(right_last, "")`. Tag COMBINE.
- On failure fall through to the **base combine** (`AbstractBaseGroupMorpher.combineGlyphgroups`):
  - If source[0] has 2 tokens (or is itself a single combinable ligature): with 60%
    (`rand(100) < 60`) try **selfCombine**: if `canFollowBefore(last_token, first_token)`,
    duplicate the word — the first copy's last token gets `ingroupGlyphReplacements` applied
    (e.g. `chol`+`chol`→`chorchol`… via `l→r`? no: `y→o,m→r,g→r,n→r,in→ir,iin→iir,dy→da`), the
    second copy's last token gets `groupFinalGlyphReplacements` applied with 80% probability;
    additionally with 30% insert a random gallow (`randomGallow(false)`) at position 1 if adjacency
    allows. Result tag COMBINE. (Produces `olol`, `chochy`-type words.)
  - Else choose a right part from source[1] via `chooseSubgroups`: `r = rand(100)`;
    `r ≤ 39` → random-length prefix of source[1] (`1 + rand(tokens-1)` tokens, requires ≥2 tokens);
    `r ≤ 59` → source[1] minus last token; else → its first combinable ligature as a 1-token list,
    falling back to source[1] minus last token. Then the same ligature-deletion and adjacency checks
    as above, token-count < 9. Tag COMBINE. Final fallbacks: selfCombine if source[0] ≤2 tokens,
    else return source[0] unchanged (= failure).

**Split**: compute split point as above; return the two parts, keeping part 1 only if it has ≥2
tokens (or is a combinable ligature) **and** `canFollowAfter(part1_last, "")`; keep part 2 only if
≥2 tokens. Tag SPLIT. If nothing kept → the unchanged word (failure signal: result equals source).
Note: a successful split returns **two words**, both written to the line in order.

### 8.5 replace

Draw `r = rand(100)`: `r ≤ 30` → 1 replacement attempt; `r ≤ 40` → 3 chained attempts; else → 2
chained attempts. Each chain step calls `replaceRandomToken` on the previous step's output; a step
that returns the input unchanged is skipped (the chain keeps the last changed value). For the 1×
case, a failed attempt is retried once. If the final result equals the original source → failure.

`replaceRandomToken(word, isParagraphInitial)`:
- Build position pool = every token index **twice**; iterate `len(pool)` times: pick and remove a
  random pool element (`rand(len(pool))`), giving position `pos`.
- Look up candidates: if word-final substitutions are enabled **and this is not the first attempt
  (`j > 0`) and `pos` is the last token** → table §5.2, else table §5.1. No candidates → next
  attempt.
- Choose a substitution via CDF (§5.1 preamble). If the substitute contains a gallow and the next
  token is a gallow, mark `removeNext` (allows `cht → ckh`).
- `isReplacable` check: `lastOk = canFollowAfter(prev_token, sub.first)`;
  `nextOk = canFollowBefore(sub.last, next_token)` (next skips the removed one if `removeNext`).
  If both OK but the word **already contains** `sub.first` elsewhere and it is not a combinable
  ligature: reject with probability 80% (or `100 − error_rate` if `sub.first == prev` or
  `sub.last == next`) — repeated glyphs inside a word are rare in the VMS. Else accept iff both OK.
- Apply: remove token(s) at `pos` (+next if `removeNext`), insert substitute tokens. Tag REPLACE
  (COMBINE preserved). Return on first successful change.

### 8.6 Post-processing every successful morph (`handleGallows`, then reuse)

For the default (non-`voynich`) canFollow:
- **Line-initial word**: draw `r = rand(100)`; if paragraph-initial and `r < 94`
  (`PARAGRAPH_STARTS_WITH_GALLOW_PROPABILITY`) → `addGallow(word, True, True)` (§8.3). Otherwise →
  `addLineInitalGlyph`: if the word does not already start with `o|y|d|s`, with 30% prepend
  `randomLineInitalGlyph()`; if prepending `o|y` to a word starting `d|ch` (>2 tokens), with 90%
  first turn that `d|ch` into a random gallow when adjacency allows (`odaiin→okaiin`); accept only
  if `canFollowToInitalGlyph` (= `canFollowBefore`) passes.
- **Mid-line word** starting with `o|y|d|s`: draw `r = rand(8)` (`rand(len(prefixGlyphs))`); if
  `r < 3` and the word has >3 tokens → remove the line-initial glyph (§8.2 removal incl. the
  gallow→`d`/`ch` softening rules).
- **Gallow bookkeeping**: if the (possibly modified) word contains a gallow: mid-paragraph, with
  probability 94% replace any first-line gallows `p|f` by a fresh `randomGallow(False)` (k/t);
  in a paragraph-initial line, replace **all** gallows by a fresh `randomGallow(True)` draw
  (per token containing one).

**Reuse-last** (`reuseLastMorphedGroup`, only if exactly one word resulted): with probability 10%
(`method.morph.reuse_last.probability`) derive a second word from the result: if it contains a
combinable ligature (`ol al or ar`), the second word is that ligature alone; else try
`tryToDeletePrefix`. Either way, with 50% (`morphReusedProbability`) run one `replaceRandomToken`
over the second word. Produces `chol ol`-type echo pairs. (Both words are then written.)

---

## 9. Line, paragraph, and page assembly (`SelfCitationTextGenerator`)

### 9.1 Seeding

- `text.initial_line` (split on `#` into multiple lines if present) is written verbatim as line(s) 0
  and its words are `remember()`-ed with tag INITIAL. Lines longer than `max_line_length` are
  truncated word-wise (`trimInitialLine`: keep appending words while the accumulated length is
  `< max_line_length` before appending).
- **Currier type inference**: if any initial line contains the substring `"ed"` → Currier **B**,
  else **A** (`Config.readConfig`). No other switch exists.
- If the seed has fewer than 6 words, also remember `daiin`, `ol`, and `chedy` (B) / `cheody` (A).
- Default seed (Currier B) = VMS line **f103v.P.9**:
  `pchal shal shorchdy okeor okain shedy pchedy qotchedy qotar ol lkar`
  The Swift app additionally shipped a Currier-A default (f1r.P.1): `fachys ykal ar ataiin shol
  shory cthres y kor sholdy`, and an alternative B line: `polchedy qokeol okain checthy oteey lshedy
  okain qokain qokalshedy oteys` — use the f1r line for our A-dialect preset.
- `stats.linesInParagraph = stats.linesInPage = number_of_seed_lines` (so the first generated line
  is *not* paragraph-initial).

### 9.2 Document loop

For `i` from `len(seed_lines)` to `lines_to_create − 1`:
- `isParagraphInitial = (stats.linesInParagraph == 0)` (checked **before** the increment)
- `stats.newLine()` (increments linesInPage, linesInParagraph)
- Boundary logic:
  - if `linesInPage == 29` (`text.lines_per_page`) or this is the final line → mark
    **paragraph-final**, `newPage()` (resets both counters and the per-page usage maps);
  - else if `linesInPage < 27` and `linesInParagraph > 3` and `i < lines_to_create − 2`:
    draw `r = rand(100)`; if `r < linesInParagraph * 10` → **paragraph-final**, `newParagraph()`.
    (Paragraph length: geometric-ish, P(end) = 40% at the 4th line, 50% at the 5th, …)
- Generate the line (§9.3) and append.

### 9.3 Line loop (`generateLine`)

- Budget: `maxLen = 55` (`text.max_line_length`); if paragraph-final, `maxLen = rand(55)` clamped to
  ≥ 15 (`text.min_line_length`) — this produces the short trailing lines of paragraphs.
- Loop while `len(line_str) + max(tries − 3, 0) < maxLen`:
  1. `count += 1`; `avail = maxLen − len(line_str)`.
  2. Choose sources (§7).
  3. `use = True` unless: source[0] has **> 5 tokens**, in which case draw `r = rand(4)` and require
     `len_chars(source[0]) < 4 + r` (long sources are mostly skipped).
     - *(Dead code note D1: a "don't use the same source twice in a row" check exists but its
       `lastSourceGroups` variable is never assigned — it can never fire. Do not implement.)*
  4. If source[0] is COMBINE-tagged: if source[1] is also COMBINE-tagged → `use = False`; else draw
     `r = rand(100)`, `use = False` if `r < 30`
     (`method.morph.combined.dismiss_as_source_probability`). Combined words are damped as sources
     so word-length statistics stay stable.
  5. Anti-livelock: if (`not use` and `count > 100`) or `count > 105`: sources =
     `stats.suggestGroupsForce(count − 100)` (§10), `use = True`; if `count > 110` set
     `forceUsage = True` (skip acceptance checks below); if `count > 130` → hard error.
  6. If `use`: `morphed = morphGroup(sources, lastGeneratedWord, isParagraphInitial, isLineInitial)`
     (§8). If empty → next iteration.
  7. Acceptance of `morphed[0]`:
     - must pass `hasValidStartGlyph` (§6);
     - if equal to the **previous word in this line**: accept with 50% (`rand(100) < 50`) —
       this is what lets `daiin daiin` happen but not always;
     - else classify (`isTypeI`/`isTypeDy`/`isTypeOl`, §10) and reject if the corresponding
       consecutive-repeat counter exceeds `text.max_repeat_count = 3` (also for the "other" class).
  8. If accepted (or `forceUsage`): `count = 0`; for each word in `morphed` (1 or 2): if it doesn't
     fit (`avail − len(word) ≤ 0`) try `tryToTrim` (§9.4); if it fits after that, append
     (space-separated; `avail` decremented by `len(word)+1` after the first word of the line),
     `remember()` it (§10), set `lastGeneratedWord`, `tries = 0`; else `tries += 1`.
     (`tries` inflates the loop-exit expression, so ~3 consecutive "doesn't fit" events end the line.)
- Finally add the word list to `lines` (and to `paragraph_initial_lines` if paragraph-initial).
  Note the empty-`morphed`/rejection paths do **not** reset `count` — only a successful append does.

### 9.4 Line-final trimming (`tryToTrim`)

To squeeze a last word into the remaining budget:
1. Replace the last token via `finalLineReplacements` (§4): `ol→om`, `iin→im`, `in→n`, … —
   this is what concentrates `m`/`g` glyphs at line ends.
2. While still too long, replace any token that has a strictly shorter single-token substitute in
   table §5.1 (`searchShorterGlyph` picks the shortest such candidate).
3. While still too long and > 2 tokens remain, drop tokens from the **front**.
4. Tag SHORTEN if changed. The caller re-checks the fit; if it still doesn't fit it is discarded
   (`tries += 1`).

---

## 10. Feedback statistics, type classes, suggestions, Currier A/B

Type classification of a word (`GlyphGroup`, if/else precedence exactly):
1. **i-type** iff the raw string contains the character `i` (e.g. `daiin`, `okain`);
2. else **dy-type** iff any token equals `dy` **or** the last character is `y` or `d`
   (e.g. `chedy`, `oteey`, `okeod`);
3. else **ol-type** iff any token ∈ {`ol`,`al`,`or`,`ar`} (e.g. `chol`, `qokar`);
4. else **other**.

`remember(word)` (called for every written word, including seeds):
- Add to `valid_words` iff INITIAL-tagged, or (`canFollow.isValid(word)` and token count < 8 and not
  COMBINE-tagged). Add to the all-words map unconditionally.
- Update per-type counters and per-page/per-document type usage maps; reset the other classes'
  consecutive-repeat counters and increment this class's (this drives §9.3 step 7).

Suggestion mechanism (keeps global type proportions near VMS values):
- `hasSuggestedGroups()`: Currier **B** → true iff `%i < 0.20` or `%dy < 0.25`; Currier **A** → true
  iff `%i < 0.20` or `%ol < 0.25`. (Thresholds = `method.suggestions.{iType,olType,dyType}_min_percentage` / 100.)
- `suggestGroups()` (mode SUGGESTION, §7): returns 1 word — B: i-group if `%i` low else dy-group;
  A: i-group if `%i` low else ol-group.
- Group choice under default `method.suggestions=top`: the **most frequent** word of that class on
  the current page (falling back to defaults `daiin` / `chol` / `chedy`|`cheody` (B|A) when the page
  map is empty; document-level maps exist in code but the page map branch is always taken —
  `size() >= 0` is always true; another intent-vs-code quirk, D2).
- `suggestGroupsForce(tryCount)` (anti-livelock, §9.3 step 5): if `tryCount < 12` use
  `suggestGroups()` if it yields anything; else/additionally return a rotating pair by
  `tryCount % 3` — B: (i,dy) / (dy,i) / (ol,i); A: (i,ol) / (ol,i) / (dy,i).

Currier dependence summary (all of it):
1. seed line (and the `"ed"`-substring inference, §9.1);
2. suggestion classes (B watches dy, A watches ol);
3. default dy-group `chedy` (B) vs `cheody` (A);
4. force-rotation order.
Everything else (tables, probabilities) is dialect-independent — the A/B statistical differences
emerge from the seed + feedback loop.

---

## 11. Parameter table (defaults as shipped)

"Shipped conf" = `executable/conf.properties` (the configuration of the published reference output).
"Code default" = `Constants.java` / fallback in `Config.readConfig` when a key is missing.

| Parameter | Shipped conf | Code default | Meaning (§) |
|---|---|---|---|
| `text.lines_to_create` | **1200** | 500 | total lines incl. seed (§9.2) |
| `text.max_line_length` | 55 | 55 (floor 40) | chars per line (§9.3) |
| `text.min_line_length` | 15 | 15 (floor 5) | min length of paragraph-final line |
| `text.lines_per_page` | 29 | 29 | page size (§9.2) |
| `text.max_repeat_count` | 3 | 3 (clamp 1–5) | consecutive same-type cap (§9.3) |
| `text.initial_line` | f103v.P.9 (B) | same | seed (§9.1) |
| `method.random` | pseudo | pseudo | RNG kind (§12) |
| `method.random.pseudo.seed` | **19** | 19 | RNG seed. *(Comment text in conf.properties says "DEFAULT=55" and mentions an `auto` mode — both stale; the code accepts only integers and defaults to 19. D3)* |
| `method.canFollow` | curveline | curveline | §6 |
| `method.canFollow.error_rate` | 0 | 0 (clamp 0–10) | §6 |
| `method.sourceChooser` | page | page | §7 |
| `method.sourceChooser.same_position_probability` | 28 | 28 *(fallback constant misused in code — it falls back to `METHOD_REUSE_LAST_PROBABILITY_DEFAULT`=10 if unparsable; D4)* | §7 |
| `method.morph` | slim | slim | §8 |
| `method.morph.add_remove.probability` | 20 | 20 *(fallback 20)* | §8.1 |
| `method.morph.combine_split.probability` | 30 | *(fallback 15)* | §8.1 |
| `method.morph.replace.probability` | 50 | *(fallback 65; min 20 enforced)* | §8.1 |
| `method.morph.reuse_last.probability` | 10 | 10 | §8.6 |
| `method.morph.combined.dismiss_as_source_probability` | 30 | 30 | §9.3 |
| `method.morph.use_word_final_substitutions` | true | true | §5.2/§6 |
| `method.suggestions` | top | top | §10 |
| `method.suggestions.probability` | 40 | 40 | §7 |
| `method.suggestions.iType_min_percentage` | 20 | 20 | §10 |
| `method.suggestions.olType_min_percentage` | 25 | 25 | §10 |
| `method.suggestions.dyType_min_percentage` | 25 | 25 | §10 |

Hard-coded (not in conf): paragraph-initial-source probability 70 (§7); paragraph-start-gallow 94%
(§8.6); line-initial-glyph add 30% / removal 3-in-8 (§8.6); gallow-add 80%/8% (§8.2); prefix→gallow
mutation 70%/90% (§8.2, §8.6); combine-vs-split 96%/4% (§8.4); selfCombine 60/80/30 (§8.4); replace
1×/3×/2× = 31/10/59 (§8.5); in-word-repeat rejection 80% (§8.5); repeat-word acceptance 50% (§9.3);
reuse-morph 50% (§8.6); long-source gate `rand(4)` (§9.3); multi-gallow skip 90% (§8.3); paragraph
end `linesInParagraph×10`% (§9.2); glyph draw distributions (§5.3).

**Our canonical preset** = shipped conf (reference-output configuration), plus an A-dialect variant
that changes only `text.initial_line` to the f1r line (§9.1).

---

## 12. Randomness model

- Java: `java.util.Random(seed)` — the standard 48-bit LCG
  (`state' = (state*0x5DEECE66D + 0xB) mod 2^48`, seed scrambled by XOR with `0x5DEECE66D`),
  `nextInt(bound)` per the JDK spec. Single global stream; every probabilistic decision above is one
  `rand(max)` call in the documented order. `rand(0)` returns 0 **without consuming state**.
- Default seed **19**; documented range 1–9999; "real" mode = nondeterministic (out of scope).
- The Swift app used `srandom()/random() % max` with default seed 90 — different stream, different
  defaults; ignore for fidelity purposes.
- **Bit-exact replication of the Java output is NOT an achievable goal**, even with a faithful
  `java.util.Random` port, because the Java code consults `HashMap` iteration order in three places
  (§4 F1 tokenizer, §7 F2 random dictionary draws, §10 top-group tie order). Validation therefore
  must be **distributional** against the committed reference output (§14), not byte-level.
- Our implementation: single explicit RNG object threaded through all components,
  `rand(max) -> int in [0, max)`, seeded from config; default backend `random.Random(seed)`
  (Mersenne) is fine since exactness is off the table — but keep the call discipline (one draw per
  documented decision, same order) so that the *structure* of randomness matches, and record
  `(seed, backend)` in every result file per L2/L3.

---

## 13. License and attribution

- **SelfCitationTextgenerator (Java): MIT License, Copyright (c) 2019 Torsten Timm** (LICENSE file
  in repo root). Reimplementation, modification, and redistribution permitted; include the copyright
  + permission notice wherever we redistribute substantial portions (we will: the §5 tables are
  copied data). Action: reproduce the MIT notice in the header docstring of
  `src/ms408/harness/selfcitation.py` and cite the Zenodo DOI.
- **VoynichTextGenerator (iOS/Swift): NO license file** → all rights reserved by default.
  Treat as read-only reference; do **not** port code or tables from it. (Everything needed is in the
  MIT repo anyway; the Swift app only contributed the A-dialect seed line, which is a VMS
  transliteration line, not copyrightable code.)
- Cite: Timm & Schinner 2020 (DOI 10.1080/01611194.2019.1596999), arXiv:1407.6639, and Zenodo
  DOI 10.5281/zenodo.2531632 in reports using H3 output.
- L19 compliance: repos cloned to scratchpad for this analysis; permanent copies should go to
  `data/raw/timm-selfcitation/` (gitignored) with a checksum manifest before implementation starts.

---

## 14. Validation targets and reference outputs

### 14.1 Author-published quantitative targets

From the repo README §2.2 (default config, seed 19, 1200 lines) — grade B (author-published,
reproducible from committed artifacts):

| Statistic | Generated text | VMS | Currier A | Currier B |
|---|---|---|---|---|
| Main similarity-network component (share of word types connected by edit-distance-1 edges) | **81.9 %** (1826/2229 types) | 84.7 % | 82.0 % | 85.5 % |
| Longest path in that network | **21** | 21 | 20 | 24 |

From the committed reference output header (`executable/generate/generated_text.txt`) — grade B:

| Statistic | Value |
|---|---|
| Lines | 1200 (≈ 10,834 tokens, 2229 types) |
| Tokens that are genuine VMS word types | 7678 = **70 %** (non-VMS 3156 = 30 %) |
| i-type token proportion | 0.241 |
| ol-type token proportion | 0.396 |
| dy-type token proportion | 0.256 |

From the Cryptologia 2020 abstract (verified verbatim via Semantic Scholar) — grade B for the claim,
C for any specific numbers until we obtain the full paper: the generated sample "reproduces some of
the statistical key properties of the Voynich manuscript; in particular, **both of Zipf's laws** are
fulfilled" — i.e. (1) the rank–frequency power law and (2) the law of abbreviation
(frequency–length). The arXiv paper additionally establishes the properties the mechanism is
designed to explain (grade C as generator targets until measured by us): binomial word-length
distribution; spatial clustering of similar words (edit-distance-1 neighbors co-occur on the same
page/line); line as functional unit (line-initial words longer, `m`/`g` at line ends, `p`/`f` in
paragraph-initial lines); absence of repeated phrases > ~2 words; weak word order.

### 14.2 Our acceptance criteria for the reimplementation (H3 gate)

Computed by `src/` scripts into `results/` (L3), comparing our generator (default preset,
1200 lines, ≥10 seeds) against (a) the committed reference output and (b) ZL3b-derived VMS
statistics:

1. **Type proportions**: i/ol/dy token proportions within ±0.03 of 0.241/0.396/0.256 (matching the
   author's run, averaged over seeds).
2. **Vocabulary overlap**: 65–75 % of generated tokens are VMS word types (author run: 70 %),
   using the ZL3b word-type inventory.
3. **Zipf rank–frequency**: log–log slope over ranks 10–1000 within the interval measured on the
   reference output ±0.1; **law of abbreviation**: negative Spearman corr(frequency, length),
   magnitude within ±0.1 of the reference output's.
4. **Word-length distribution**: within total-variation distance 0.05 of the reference output's.
5. **Similarity network**: main-component share 80–86 %, longest path 18–24.
6. **Positional signatures**: paragraph-initial lines contain ≥ 3× the p/f gallow rate of other
   lines; `m|g`-final words concentrated at line ends; both qualitatively present in the VMS and the
   reference output.
7. **Character conditional entropy h2** in the range measured for the reference output (compute,
   don't assume; Voynichese target ≈ 2 bits per Lindemann & Bowern is a check on *both*).
8. **Determinism**: identical output for identical (seed, config) across runs and platforms.

Criteria 1–2 are hard gates (they are what the feedback loop explicitly controls); 3–7 are
report-with-tolerance gates — any miss is flagged to Tim with the measured value rather than
silently widened (per rule 6).

### 14.3 Running the author's generator (cross-validation reference)

```
cd <clone>/SelfCitationTextgenerator/executable
./start.sh          # = java -jar text-generator.jar ; needs Java 8+ JRE
# reads ./conf.properties, writes ./generate/generated_text.txt
# (header block = config + summary stats, then 1200 text lines)
```

Notes:
- **Java is not installed on the current machine** (verified 2026-07-05: "Unable to locate a Java
  Runtime"). Options: `brew install --cask temurin` (or any JRE ≥ 8), or rely on the committed
  reference output, which *is* the author's own seed-19 default run — sufficient for criteria 1–7.
  A fresh run is only needed to (i) confirm the jar reproduces the committed file bit-for-bit on a
  modern JVM (HashMap order is JVM-version-stable in practice, but confirm), and (ii) generate
  additional seeds for variance estimates. Do both when a JRE is available; record JVM version.
- The jar is a compiled artifact committed to the repo; `source/` + `mvn package` (pom.xml present)
  rebuilds it if provenance of the binary is ever questioned.
- Output format detail: the header lines are prefixed with `#` — strip `^#.*` lines before analysis;
  pages are **not** delimited in the output (count lines: 29 per page, seed line included in page 1);
  paragraph boundaries are likewise implicit (short line = paragraph end) — our reimplementation
  must do better (§15 output format).

---

## 15. Reimplementation plan — `src/ms408/harness/selfcitation.py`

Design principles: pure functions + one RNG object; every table from §4–§5 as module-level frozen
data with a comment pointing at `Glyph.java` line ranges; no I/O in the generator itself.

```
src/ms408/harness/selfcitation.py         # single module is fine (~600 lines); split only if it grows
tests/harness/test_selfcitation.py
```

Suggested internal structure:

1. **Data section**: `LIGATURES` (longest-first tuple), `SUBSTITUTIONS`, `FINAL_SUBSTITUTIONS`
   (dicts token → list[(replacement_tokens, cum_threshold)]), prefix table, replacement maps,
   canfollow token lists — all verbatim from §4–§6.
2. `tokenize(word: str) -> tuple[str, ...]` — longest-match-first (§4, F1 decision: rationalize).
3. `Word` dataclass: `tokens`, `text` (cached join), `gen_type` enum, plus the `is_type_i/dy/ol`,
   `contains_gallow`, etc. predicates (§10, §4).
4. `CurveLineCanFollow` class implementing §6 exactly (`can_follow_before/after`, `is_valid`,
   `has_valid_start`), with the error-rate hook (draw only on failure and only if E>0).
5. `Morpher` implementing §8 (add/remove, combine/split, replace, handle_gallows, reuse_last), all
   probability literals as named constants.
6. `PageSourceChooser` implementing §7 (LOCAL / PARAGRAPH_INITIAL / SUGGESTION / RANDOM;
   `valid_words` kept as an insertion-ordered dict — deterministic Python replacement for F2).
7. `Stats` implementing §10 (counters, per-page/doc usage maps, suggestions incl. force rotation).
8. `SelfCitationConfig` dataclass mirroring §11 (defaults = shipped conf), with `currier` derived
   from the seed line exactly as §9.1 (substring `"ed"`), overridable.
9. `generate(config, seed) -> GeneratedText` implementing §9; `GeneratedText` carries
   `pages -> paragraphs -> lines -> words` **explicitly** (don't reconstruct boundaries from line
   lengths like the original), plus provenance: config dict, seed, module version, git commit.
   Provide `to_ivtff_like()` / `to_plain_lines()` serializers so H3 samples flow through the same
   pipeline entry points as real transliterations (L4 harness contract).
10. CLI hook (`python -m ms408.harness.selfcitation --seed N --lines 1200 --dialect A|B --out …`)
    writing to `results/`-compatible JSON + text, per L3.

Testing plan (same file order):
- table integrity: every substitution list's last threshold == 100; ligature set matches §4; CDF
  monotone non-decreasing;
- tokenizer round-trips every word type in the reference output (`"".join(tokenize(w)) == w`) and
  agrees with hand-checked cases (`qokeedy → qo|k|ee|dy`, `ckhhy`, `daiin → d|a|iin`);
- canfollow unit cases: `isValid` accepts all seed-line words and the §14.1 defaults, rejects
  `doiin`-style constructions the paper calls out (error_rate=0);
- morph operators: golden-file micro-tests per operation with a fixed RNG stub (sequence-injected),
  e.g. q-prefix on `okeedy → qokeedy`, `kain → dain` softening, selfCombine `chol → chorchol`
  variants, tryToTrim `…ol → …om`;
- end-to-end: fixed seed → byte-identical output across runs/platforms (criterion 14.2.8);
- distributional gate script (separate, in `src/ms408/stats/`): computes criteria 14.2.1–7 against
  the committed reference output copied into `data/raw/timm-selfcitation/`.

Sequencing note: implement tokenizer + canfollow + tables first (they are testable standalone),
then morph ops, then choosers/stats, then assembly; the distributional gate is the last step and is
the H3 acceptance evidence for RESEARCH-PLAN §3.

---

## 16. Risks, discrepancies, and flagged decisions

- **R1 — 2020 parameter fidelity (SOURCES.md risk #2)**: we could not read the Cryptologia paper
  (T&F blocks bots; abstract verified only). The Java repo *is* the paper's companion code
  (README links the DOI), and its committed reference output is what the paper analyzes, so the code
  is the better ground truth for reimplementation regardless. Residual risk: the paper may describe
  parameter values or pseudo-code that differ from the code's quirks (e.g. D4). **Action**: obtain
  the paper (author copy via academia.edu/ResearchGate, or ILL) before writing the H3 report;
  reconcile and note any deltas. → New D-item for Tim (paper acquisition path).
- **R2 — arXiv paper contains no algorithm**: anyone auditing "reimplemented from free sources" must
  understand the split: mechanism/motivation = arXiv 1407.6639; executable definition = MIT-licensed
  code. This spec is the bridge; cite both.
- **R3 / F1, F2 — JVM container-order nondeterminism**: tokenizer ligature matching, random
  dictionary draws, and top-group tie-breaks depend on Java `HashMap` iteration order. Consequence:
  bit-exact cross-implementation output is impossible by design; validation is distributional
  (§14.2). Our replacements (longest-match-first; insertion-ordered dict; first-max tie-break) are
  deterministic and documented here — treat them as part of *our* spec, not Timm's.
- **D1 — dead code**: the "same source twice" rejection in `generateLine` can never trigger
  (`lastSourceGroups` never assigned). We do not implement it. If the 2020 paper *describes* it,
  reconcile under R1.
- **D2 — page-vs-document suggestion maps**: `size() >= 0` conditions make the document-level
  fallback unreachable; page-level map (with `daiin`/`chol`/`chedy|cheody` defaults) is always used.
  Implemented as written (page map + defaults).
- **D3 — stale comments**: conf.properties comments claim seed default 55 and an `auto` seed mode;
  code has neither. PROPERTIES.md and Constants agree on 19. Use 19.
- **D4 — wrong fallback constant**: missing `same_position_probability` falls back to 10 (the
  reuse-last constant) instead of 28. Irrelevant under our explicit-config policy; noted for R1
  reconciliation.
- **R4 — no Java on the analysis machine**: fresh author-generator runs (multi-seed variance,
  jar-vs-committed-file confirmation) deferred until a JRE is installed; the committed seed-19
  output is sufficient to start (§14.3).
- **R5 — iOS repo unlicensed**: consult-only boundary must be respected in implementation (§13);
  the only thing we take from it is the f1r seed line (VMS transliteration text, not code).
- **R6 — EVA normalization**: the generator emits plain lowercase EVA without IVTFF markup. When
  comparing against ZL3b statistics, use the same normalization pipeline (T1.x) for both sides —
  e.g. VMS word-type inventory for criterion 14.2.2 must be extracted with identical
  space/uncertain-glyph handling, or the 70 % target moves.
