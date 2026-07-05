# T0.3 Spec — Naibbe Cipher Generator (Harness Class H2)

**Status:** implementation-ready spec, pending review.
**Target module:** `src/ms408/harness/naibbe.py`
**Program context:** RESEARCH-PLAN §3 — H2 = "Voynich-like ciphertext from known Latin/Italian
plaintext; meaningful, recoverable; Naibbe verbose substitution cipher (Greshko 2025,
*Cryptologia*) — reimplement generator."

## 1. Source and provenance

- **Paper:** Greshko, Michael A. (2025). *The Naibbe cipher: a substitution cipher that encrypts
  Latin and Italian as Voynich Manuscript-like ciphertext.* Cryptologia.
  https://doi.org/10.1080/01611194.2025.2566408
- **Reference implementation:** https://github.com/greshko/naibbe-cipher — studied at commit
  `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2` (2026-05-29). Key files:
  - `naibbe.py` — v1 generator (52-card default; unigram-collision avoidance only).
  - `naibbe_v2.py` — v2 generator (adds cross-bigram collision avoidance; 78-card default).
    `naibbe_v2.ipynb` is the same code in notebook form (99.5% identical).
  - `naibbe_cv_vc_reuse.py` — experimental variant (CV/VC deterministic respacing + short/long-range
    token-reuse mechanisms). Not required for H2; see §10.
  - `decrypt_naibbe.py` / `decrypt_naibbe.ipynb` — decrypter.
  - `references/naibbe_tables.csv` — **the cipher key** (all six tables; see §5).
  - `voynichesque.py` / `.ipynb` — a *different*, simpler comparison cipher from the same paper.
    Out of scope for H2.
  - `input/examples/` (Pliny *Naturalis Historia* bk 16 Latin; Dante *Divina Commedia* Italian),
    `encrypted/`, `respaced_plaintext/`, `decrypted/` — worked example corpora.
  - `figure_utils/` — the author's statistical validation code + reference outputs (see §8).
- **Zenodo:** README cites extended datasets incl. the original Excel implementations at DOI
  10.5281/zenodo.16415087. The task brief also references DOI 10.5281/zenodo.17219445 (apparently a
  newer deposit/version). Neither is needed to reimplement; not downloaded (L19 consume-only).

## 2. License and attribution (binding)

The repository is under a **modified MIT license** (full text in repo `README.md` and in every
source file header). Beyond standard MIT terms, it adds this condition, quoted verbatim:

> - Any publications making use of the Software and Datasets, or any substantial
>   portions thereof, shall cite the Software and Datasets's original publication:
>
> > Greshko, Michael A. (2025). The Naibbe cipher: a substitution cipher that encrypts
> Latin and Italian as Voynich Manuscript-like ciphertext.
> Cryptologia. https://doi.org/10.1080/01611194.2025.2566408

Consequences for us:
1. Any publication using our reimplementation or the table data **must cite Greshko 2025**.
2. Copies/substantial portions must carry the copyright notice + permission notice.
3. Per program rule L19 (consume-only until Tim sets policy), we do **not** vendor
   `naibbe_tables.csv` into the versioned repo yet; it lives in `data/raw/naibbe-cipher/`
   (gitignored). See D-item flag in §10.

## 3. Cipher overview

The Naibbe cipher is a **verbose homophonic substitution cipher** operable by hand with 15th-century
materials (two dice + a deck of *naibi* playing cards):

1. Plaintext (Latin/Italian) is normalized to a 23-letter alphabet and stripped of word spaces.
2. The letter stream is re-segmented into **units** of 1 letter ("unigram") or 2 letters ("bigram")
   by a random process (historically: a two-dice roll per decision).
3. Each unit becomes exactly **one ciphertext word**. A card drawn from a shuffled deck selects one
   of **six encryption tables** (alpha, beta1, beta2, beta3, gamma1, gamma2). A unigram unit uses
   the table's *unigram* row for its letter → one whole word. A bigram unit uses two independent
   card draws: first letter → *prefix* glyph string, second letter → *suffix* glyph string,
   concatenated into one word.
4. Ciphertext words are emitted in order, space-separated, one output line per input line.
5. Optionally, a "respaced" copy of the output randomly deletes ~3% of word-separating spaces to
   mimic uncertain Voynich spacing.

Ciphertext is written in **EVA glyphs** (basic EVA, lowercase ASCII). Because every table entry is
a Voynichese-plausible string, output words look like Voynich words (`qokedy`, `chol`, `daiin`, …).

## 4. Exact algorithm

### 4.1 Plaintext preprocessing (`clean_line`)

Applied per input line; a line that cleans to empty is preserved as an empty output line.

1. Unicode NFD-normalize; delete all combining marks (category `Mn`) — strips diacritics.
2. Replace ligatures/special letters: `æ/Æ→ae`, `œ/Œ→oe`, `ð/Ð→d`, `þ/Þ→th`, `ł/Ł→l`, `ß→ss`,
   `ø/Ø→o`.
3. Keep only alphabetic characters (`str.isalpha()`); drop digits, punctuation, spaces.
4. Uppercase, then substitute `W→UU`, `J→I`, `K→C`; lowercase the result.

Result: a lowercase string over the **23-letter effective alphabet** `a–z` minus `{j, k, w}`
(classical Latin conventions: i/j merged, no k/w). The cipher tables define exactly these
23 letters. Our implementation must **raise** on any letter without a table entry (the author's
code would silently emit a placeholder code string; unreachable given `clean_line`, but we should
fail loudly).

### 4.2 Unit segmentation ("respacing", the dice roll)

Per line, on the cleaned string `t` (original word spaces already removed):

```
i = 0; units = []
while i < len(t):
    if i == len(t) - 1 or rng.random() < RESPACING/36:
        units.append(t[i]);     i += 1     # unigram
    else:
        units.append(t[i:i+2]); i += 2     # bigram
```

- `RESPACING = 17` (**standard**): P(unigram) = 17/36 ≈ 0.4722 per decision — the hand method is a
  2d6 roll with 17 of the 36 outcomes assigned to "take one letter". `RESPACING = 18` is the
  documented "simplified" 50/50 variant. Default: 17.
- The final letter of a line is always a unigram if it stands alone.
- Empirical check (author's `respaced_plaintext/nathist_pre_encryption_respaced_plaintext.txt`):
  48.6% unigram / 51.4% bigram units (slightly above 17/36 due to the forced line-final unigram).
- The author's tooling writes the segmented plaintext (space-joined units) to a
  `respaced_plaintext/` file; our generator must also emit this as the **ground-truth alignment**
  artifact (one ciphertext word per unit, in order).

### 4.3 Table selection (the card draw)

Six tables; selection weights come from a physical card deck, drawn **without replacement**:

| Deck | alpha | beta1 | beta2 | beta3 | gamma1 | gamma2 | total |
|---|---|---|---|---|---|---|---|
| 52-card (naibbe/naibi) | 20 | 8 | 8 | 8 | 4 | 4 | 52 |
| 78-card (tarot-like)   | 28 | 14 | 11 | 11 | 7 | 7 | 78 |

Mechanics (must be reproduced exactly — it is *not* i.i.d. sampling):

- A deck is a list containing each table name repeated by its weight, shuffled (`rng.shuffle`).
- **A fresh shuffled deck is created at the start of every line** (each `encrypt_naibbe` call).
- Cards are consumed one per table lookup: 1 for a unigram unit, 2 for a bigram unit (prefix draw,
  then suffix draw). When the deck is exhausted mid-line, a new deck is created and shuffled.
- In unambiguous mode (§4.5), **rejected draws still consume cards**.

### 4.4 The six encryption tables (cipher key)

Each table maps (role, letter) → EVA glyph string, roles = {unigram, prefix, suffix}, letters = the
23-letter alphabet. Total 6 × 3 × 23 = **414 entries**, held in
`references/naibbe_tables.csv` (UTF-8 **with BOM**; sha256
`4e7cfd54b7ec66515d39a51e11ec97e8e19b643b0b189124eebc3982e707dcec`). Format: header `code,glyphs`;
`code` = `{role}_{table}_{letter}`, e.g.:

```
unigram_alpha_a,ol
unigram_alpha_n,daiin
prefix_alpha_t,qok
suffix_alpha_e,edy
unigram_gamma2_z,olkeeedy
```

Do not retype the tables — load them from the author's CSV (read with `utf-8-sig`). Structural
invariants to assert at load time (verified against the CSV at the studied commit):

- Exactly 414 rows; every (role, table, letter) combination present exactly once.
- All prefix glyphs distinct (138); all suffix glyphs distinct (138); unigram glyphs distinct
  except `dar`, which appears as both `unigram_beta2_e` and `unigram_beta3_e` (same plaintext
  letter, so harmless).
- Glyph strings overlap heavily across roles (e.g. `dar` is also `prefix_beta3_d` and
  `suffix_gamma2_e`) — ambiguity is controlled at encryption time (§4.5) and by decryption
  precedence (§4.7), not by table disjointness.
- Of the 138×138 = 19,044 possible prefix+suffix concatenations, 18,935 are distinct strings;
  **105 strings have multiple (prefix,suffix) parses** (all with conflicting plaintext readings),
  and ~120 collide with a unigram glyph. These two collision sets drive the v1/v2 difference below.

### 4.5 Encryption per unit

- **Unigram unit** (letter `x`): draw card → table `T`; emit glyph `T[unigram, x]` as one word.
- **Bigram unit** (letters `x`,`y`): draw card → `T1`, glyph `p = T1[prefix, x]`; draw card → `T2`,
  glyph `s = T2[suffix, y]`; candidate word `p + s`.
  - **UNAMBIGUOUS mode (default, recommended):** reject and redraw (both cards) if the candidate:
    1. equals any unigram glyph (v1 and v2), or
    2. **(v2 only)** has any *other* (prefix,suffix) parse in the precomputed catalog of all
       19,044 concatenations (i.e., the string is one of the 105 ambiguous strings).
    Retry until acceptance, up to `MAX_BIGRAM_RETRIES = 10000` (v2 safety fuse; on exhaustion the
    author emits the last attempt — we should instead raise). Count retries for diagnostics.
  - Non-unambiguous mode simply emits `p + s`.

### 4.6 Word/line assembly and output respacing

- One input line → one ciphertext line; words joined by single spaces. Empty input line → empty
  output line.
- **Respaced output** (second artifact): per interior word boundary, with probability
  `SPACE_REMOVAL_RATE = 0.03` merge the two adjacent words (delete the space). Lines with <2 words
  pass through unchanged. This models Voynich spacing uncertainty; the primary statistical corpus
  in the author's analyses is the *un*-respaced output (reference ciphertexts are one word per
  cell/line), so keep both artifacts.

### 4.7 Decryption (needed for harness "recoverable" ground truth)

From `decrypt_naibbe.py`; implement for round-trip validation:

- Build reverse maps glyph→letter per role (table identity is irrelevant to decryption).
- Per ciphertext word: if it is a unigram glyph → that letter (**unigram reading takes precedence**,
  `BASIC = True`). Else try every split point: if `word[:i]` ∈ prefix map and `word[i:]` ∈ suffix
  map → two-letter reading; de-duplicate; a single reading decrypts, multiple readings are reported
  as `(ab|cd)` (cannot occur for v2-generated text). Unparseable words → `[?]`, optionally trying a
  compound split into two valid words (handles the merged words of the respaced output).
- **Guarantee:** v2 UNAMBIGUOUS output round-trips exactly: unigram-collision rejection means no
  bigram word ever equals a unigram glyph, and cross-bigram rejection means every emitted bigram
  word has a unique parse. v1 output can contain the 105 ambiguous strings (multi-reading).

### 4.8 v1 vs v2 — implement v2 semantics

Differences: (a) v2 adds the cross-bigram-collision rejection (4.5.2) making decryption unique;
(b) v2 adds the retry fuse; (c) config defaults differ (v1 `USE_78_CARD_DECK=False`, v2 `True`).
**Implement v2 logic** — it is the author's refined version and guarantees the "meaningful,
recoverable" ground-truth property H2 requires. Keep the v1 behavior reachable via config flag
(`cross_bigram_check=False`) for sensitivity checks. Deck size is a config parameter, not a
version difference; the author's reference statistics cover **both** deck sizes (10 samples each).

## 5. Parameter summary (defaults for our generator)

| Parameter | Default | Meaning / values |
|---|---|---|
| `respacing` | 17 | numerator of P(unigram) = n/36; 17 standard, 18 simplified |
| `deck` | `"52"` and `"78"` both generated | card weights per §4.3 |
| `unambiguous` | True | reject unigram collisions |
| `cross_bigram_check` | True (v2) | reject multi-parse bigram strings |
| `max_bigram_retries` | 10000 | raise if exceeded |
| `space_removal_rate` | 0.03 | respaced-output space deletion prob |
| `tables_csv` | `data/raw/naibbe-cipher/references/naibbe_tables.csv` | key file, sha256 pinned |
| `seed` | required, no default | see §6 |

## 6. Randomness model

The author uses Python's global `random` module (Mersenne Twister), unseeded → outputs are not
reproducible run-to-run. RNG touchpoints, in stream order per line:

1. All segmentation decisions for the line (`rng.random()` per position) — fully consumed first;
2. deck shuffle(s) (`rng.shuffle`) — one at line start, more on exhaustion — interleaved with draws;
3. respaced-output space deletions (`rng.random()` per word boundary), applied after the line is
   encrypted.

Our implementation: accept `seed` and use one injected `random.Random(seed)` instance for
everything; record seed + all parameters + tables-CSV sha256 + git commit in the output manifest
(program rule L3). We do **not** need bitwise compatibility with the author's stream, only
distributional equivalence + the §8 validation targets; but preserving the same call order costs
nothing and keeps the option of exact replay against a locally seeded copy of the author's code.

## 7. Reference corpora and runnable commands

The author's code runs as-is (Python 3, needs `pandas`; run from repo root so relative paths
resolve). Verified working during this study:

```
python3 -m venv venv && venv/bin/pip install pandas
cd <scratch>/naibbe-cipher
venv/bin/python naibbe_v2.py        # encrypts input/examples/nathist_book16.txt (78-card)
venv/bin/python naibbe.py           # encrypts input/examples/divina_commedia.txt (52-card)
venv/bin/python decrypt_naibbe.py   # decrypts encrypted/divcom_output_ciphertext.txt
```

Note: fresh runs are unseeded (new random ciphertext each run — statistically comparable, not
byte-identical). To produce a *seeded* author-side reference, `import random; random.seed(S)`
before calling `encrypt_naibbe` (verified: seed 408, v2 code, 52-deck, plaintext
`gratias tibi ago` → `cphdam chol oddy ol ytcham qotedy olkchdy qokedy lssaiin al`, which
round-trips through `decrypt_naibbe` to `gr a ti a st i b i ag o`).

Committed reference outputs (use directly; no rerun needed):

- `encrypted/nathist_output_ciphertext.txt` (+ `_respaced`) with matching
  `respaced_plaintext/nathist_pre_encryption_respaced_plaintext.txt` and
  `decrypted/nathist_output_ciphertext_decrypted.txt`; same trio for `divcom` (decrypted +
  respaced plaintext committed; full divcom ciphertext reproducible via `naibbe.py`).
- `figure_utils/entropy/data/naibbe_reference_ciphertexts.csv` — **20 independent reference
  ciphertexts** (columns `52_01..52_10`, `78_01..78_10`; one word per row; ~21k words each), plus
  a CUVA-transliterated version (`naibbe_reference_cuva.csv`) and Voynich B reference
  (`voyb_reference.csv`).
- `figure_utils/gaskell_bowern_2022/data/naibbe_reference_ciphertexts/` — the same 20 samples
  wrapped 10 words/line; `metrics.csv` — 42 Gaskell–Bowern gibberish-test metrics per sample.
- `encrypted/examples/endofpaper.txt` → `decrypted/endofpaper_decrypted.txt`
  ("g ra ti as t i bi ag o" = *gratias tibi ago*) — tiny worked example.

## 8. Validation targets for our reimplementation

Functional (hard requirements):

1. **Round-trip:** for any H4 Latin/Italian text, v2-mode encrypt → decrypt (unigram-precedence)
   recovers the cleaned plaintext exactly (spaces removed). 100%, by construction.
2. **Decrypt the author's ciphertexts:** our decrypter on `encrypted/nathist_output_ciphertext.txt`
   must reproduce `decrypted/nathist_output_ciphertext_decrypted.txt` byte-for-byte (modulo
   trailing whitespace).
3. **Table invariants** of §4.4 assert clean.

Statistical (compare our generated ciphertext of `input/examples/nathist_book16.txt` against the
author's 20 reference samples; matching within the spread of those 20 samples = pass; all numbers
below recomputed from repo files during this study, per L3 they must be reproduced by `src/`
scripts into `results/` before being cited in any report):

4. **Character entropy** (author's method, `figure_utils/entropy/entropy.ipynb`: corpus-level char
   unigram entropy h1 and conditional bigram entropy h2 computed *within words only*, on
   **CUVA-transliterated** text): author's Naibbe references h1 ≈ 3.916–3.924, h2 ≈ 2.311–2.339
   (52 and 78 decks overlap; 78 slightly higher h2). Voynich B reference: CUVA h1 = 3.899,
   h2 = 2.255; EVA h1 = 3.860, h2 = 1.954. Requires an EVA→CUVA conversion step — the CUVA
   reference CSV in `figure_utils/entropy/data/` pins the expected conversion output.
5. **Token/type statistics** (un-respaced nathist run, 52-deck v1-era reference): 34,764 tokens,
   mean ciphertext word length 5.234 chars, 5,600 distinct word types; Gaskell–Bowern
   `metrics.csv` gives per-sample targets (e.g. `wordlen_mean` ≈ 5.25–5.27, `zipf`, `entropy`,
   `compression`, repetition and positional-bias metrics — 42 columns) for all 20 samples.
6. **Segmentation distribution:** unigram-unit share ≈ 0.486 at `respacing=17` (§4.2).
7. Optional deeper checks mirroring the author's figures: PCA/k-means clustering vs Voynich B
   (`figure_utils/pca_naibbe/`), long-range correlation / RMSF (`figure_utils/rmsf/`).

## 9. Reimplementation plan (`src/ms408/harness/naibbe.py`)

- Single module, stdlib only (csv + random; no pandas dependency).
- `NaibbeConfig` dataclass: fields of §5 + `deck: Literal["52","78"]`.
- `NaibbeTables.load(path)` — parses CSV (utf-8-sig), asserts §4.4 invariants + pinned sha256,
  precomputes unigram-glyph set and the bigram parse catalog.
- `NaibbeCipher(tables, config, rng)` with:
  - `clean_line(str) -> str` (§4.1)
  - `segment(str) -> list[str]` (§4.2)
  - `encrypt_line(str) -> EncryptedLine` carrying `(units, words)` so plaintext↔ciphertext
    alignment is preserved for harness ground truth
  - `encrypt_text(iterable[str]) -> NaibbeResult` (ciphertext lines, respaced lines, segmented
    plaintext lines, diagnostics: retry count, deck draws)
  - `decrypt_line / decrypt_text` (§4.7)
- CLI entry (`python -m ms408.harness.naibbe --in … --seed … --deck 52 …`) writing ciphertext,
  respaced ciphertext, segmented plaintext, and a JSON manifest (script, git commit, seed, params,
  tables sha256) per L3.
- Tests: round-trip property test; decrypt-author-ciphertext golden test; table invariants;
  segmentation fraction; deck-composition exhaustion behavior (52 draws → reshuffle).
- Validation script `src/…/validate_naibbe.py` computing §8 metrics into
  `results/harness/naibbe_validation.json` for the T0.3 benchmark report.

## 10. Open decisions to flag (per rule 6 — flag, don't resolve)

- **D-new-1 (tables redistribution):** license permits committing `naibbe_tables.csv` (with
  copyright notice + citation), but L19 says consume-only until Tim sets policy. Interim: keep in
  `data/raw/` (gitignored) with pinned sha256 + a fetch script. Tim to decide whether to vendor.
- **D-new-2 (canonical H2 config):** author publishes both 52- and 78-card reference sets.
  Proposal: generate both (H2-52, H2-78) with `respacing=17`, v2 unambiguous mode; treat the
  respaced (3% space-drop) variants as a sensitivity layer, not the primary corpus.
- **D-new-3 (H2 plaintext choice):** author used Pliny *Nat. Hist.* bk 16 (Latin) and Dante
  *Divina Commedia* (Italian), both included in the repo. Reusing them maximizes comparability with
  the author's reference statistics; D3 corpus policy may add others.
- **D-new-4 (cv/vc + reuse variant):** `naibbe_cv_vc_reuse.py` adds deterministic consonant-vowel
  segmentation modes and short-range (exponential-lag, rate 0.004) / long-range (Pareto-lag
  α=0.75, rate 0.006) ciphertext-token reuse to raise the Hurst exponent. Out of scope for baseline
  H2; candidate extension for T2.4 encoding-hypothesis bracket.
- **D-new-5 (Zenodo deposits):** two DOIs in circulation (10.5281/zenodo.16415087 in README;
  10.5281/zenodo.17219445 in the task brief). Not needed for reimplementation; verify which is
  current if we ever cite the deposited Excel implementation.

---

*Attribution: this spec describes, and its validation data derive from, Greshko (2025),
Cryptologia, https://doi.org/10.1080/01611194.2025.2566408, per the modified MIT license in §2.*
