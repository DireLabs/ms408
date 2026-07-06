# Dossier: Early-15th-Century Cipher Culture (pre-Alberti, northern Italy)

**Task:** T2.5, dossier 1 of 5 (W4 influence dossiers)
**Window:** ~1404–1438 (MS 408 vellum radiocarbon range); milieu: northern Italy
**Method:** web research over secondary literature; every claim graded **C** (sourced) or **D**
(inference/speculation) per RESEARCH-PLAN §6. No numbers here feed `results/`; this is milieu
context only (L3 firewall unaffected).

**Source-quality caveat (flag, not resolved):** the strongest accessible sources for this period are
serious hobbyist/researcher syntheses (Pelling/Cipher Mysteries, Philip Neal) and tertiary summaries
of the archival literature (Meister 1902/1906, Kahn 1967, Pasini 1872). Primary cipher-key archives
(Vatican, Mantua, Milan, Lucca, Venice) were not consulted directly. If any W5 claim comes to rest
on a single detail below, it should be re-verified against Meister or the archive itself. → New
D-item for Tim: whether to acquire Meister 1902/1906 scans for primary verification.

---

## 1. Baseline: cipher practice before the manuscript's window

- The earliest substantial European cipher-key collection is the ledger of **Gabriele de Lavinde**
  of Parma, cipher secretary to (anti)pope Clement VII, **1379** — keys for 24 correspondents, each
  combining a monoalphabetic substitution alphabet with nulls and a short list of two-character
  code equivalents for names/words: the prototype **nomenclator** (Kahn's coinage for the hybrid
  cipher+code form). Held in the Vatican archives ("Liber Zifrarum," Collection 393 f. 166–181).
  **[C]** — [Britannica, "Gabriele de Lavinde"](https://www.britannica.com/biography/Gabriele-de-Lavinde);
  [Pommerening, Uni Mainz, "Cryptology: Codebooks"](https://www.staff.uni-mainz.de/pommeren/Cryptology/Classic/1_Monoalph/Codebook.html);
  [Wikipedia, "Codebook"](https://en.wikipedia.org/wiki/Codebook).
- The nomenclator remained the dominant European cipher form from the 15th century to roughly the
  mid-19th — the technology of our window is the *beginning* of a 400-year-stable form, not an
  exotic dead end. **[C]** — [Pommerening, ibid.](https://www.staff.uni-mainz.de/pommeren/Cryptology/Classic/1_Monoalph/Codebook.html)
- Parallel to the diplomatic line there is an older **non-diplomatic scribal tradition** of trivial
  ciphers in monasteries and manuscript margins: vowel-replacement systems (the *bfk* cipher,
  a=b, e=f, i=k, o=p, u=x), vowel→dot substitutions, and similar toys, surveyed in **Bischoff,
  "Übersicht über die nichtdiplomatischen Geheimschriften des Mittelalters," MIÖG 62 (1954)**.
  These conceal colophons, recipes, and glosses — never whole books. **[C]** —
  [Bischoff 1954, bibliographic record](https://katalog.ub.uni-heidelberg.de/cgi-bin/titel.cgi?katkey=2008200);
  [Glossenwiki (Uni Augsburg), "Geheimschriften"](https://glossenwiki.phil.uni-augsburg.de/wiki/Geheimschriften);
  [Porck 2017, "Anglo-Saxon Cryptography"](https://thijsporck.com/2017/05/15/anglo-saxon-cryptography/).
- Two distinct cultures therefore coexist by 1400: sophisticated-but-small diplomatic keys, and
  trivial-but-bookish scribal ciphers. A whole enciphered *book* sits in neither mainstream. **[D]**

## 2. Chancery practice inside the window (~1404–1438), by court

### Mantua (Gonzaga archive)
- **1401:** cipher prepared for correspondence between the Gonzaga chancery (Francesco I Gonzaga)
  and **Simeone de Crema** — the earliest known **homophonic** key: multiple cipher shapes
  allocated to each of the five vowels. **[C]** —
  [Wikipedia, "Substitution cipher"](https://en.wikipedia.org/wiki/Substitution_cipher);
  [Pelling, "Fifteenth Century Cryptography," Cipher Mysteries, 2016](https://ciphermysteries.com/2016/07/06/fifteenth-century-cryptography).
- The Mantua State Archives preserve **55 cipher keys dated 1401–1416** — the densest surviving
  key collection inside our exact window. **[C]** —
  [Pelling, "Paolo Guinigi and ciphers," Cipher Mysteries, 2020](https://ciphermysteries.com/2020/06/10/paolo-guinigi-and-ciphers).
- Pelling's reading (contra Kahn): early homophones were a **steganographic patch for the
  vowel-heavy endings of Italian/Latin**, not a defense against frequency analysis — he finds "no
  evidence suggesting any kind of awareness of frequency analysis in the West in the fifteenth
  century" before Alberti. **[C]** for the claim's existence; the negative is an argument from
  silence **[D]** —
  [Pelling 2016, ibid.](https://ciphermysteries.com/2016/07/06/fifteenth-century-cryptography);
  [Pelling, "Fifteenth Century Cryptography Revisited," academia.edu, 2017](https://www.academia.edu/33813775/Fifteenth_Century_Cryptography_Revisited).

### Venice
- Earliest surviving evidence of enciphered diplomatic correspondence in the Venetian archives:
  **1411** ("Steno's cipher," with both vowel and consonant homophones). **[C]** —
  [Pasini 1872, "Written ciphers used by the Republic of Venice," transl. 2021, academia.edu](https://www.academia.edu/45153646/Paper_WRITTEN_CIPHERS_USED_BY_THE_REPUBLIC_OF_VENICE_LUIGI_PASINI_1872_TRANSLATED_2021);
  [Iordanou, "The Professionalization of Cryptology in Sixteenth-Century Venice," *Enterprise & Society*, 2018](https://radar.brookes.ac.uk/radar/file/d6c33ee2-34c8-4994-b765-959f8ccfb14d/1/Professionalization%20of%20cryptology%20-%202018%20-%20Iordanou.pdf).
- Cipher administration sat with the **Council of Ten** from the early 15th century; disclosure of
  a key was treason. Professionalized cryptanalysis (Giovanni Soro as cipher secretary) is **1506**
  — well after our window. **[C]** —
  [Atlas Obscura, "The Hidden Professional Code Breakers of Renaissance Venice"](https://www.atlasobscura.com/articles/cryptography-renaissance-venice);
  [Iordanou 2018, ibid.](https://radar.brookes.ac.uk/radar/file/d6c33ee2-34c8-4994-b765-959f8ccfb14d/1/Professionalization%20of%20cryptology%20-%202018%20-%20Iordanou.pdf).

### Lucca (Guinigi archive) — smaller court, in-window
- Paolo Guinigi's chancery (Lucca, 1400–1430) left enciphered passages in correspondence from
  **1404–1406, 1410, and 1413–1418**, embedded *inside* otherwise-plaintext letters (partial
  encipherment). Meister catalogued Lucca's "Codex 5": **74 keys, dated 1412–1439; of the first
  26 keys, 14 are pure nomenclatures.** **[C]** —
  [Pelling, "Paolo Guinigi and ciphers," 2020](https://ciphermysteries.com/2020/06/10/paolo-guinigi-and-ciphers),
  reporting Meister, *Die Anfänge der modernen diplomatischen Geheimschrift*, 1902.
- Modena preserves a further 16 fifteenth-century keys. **[C]** — [Pelling 2020, ibid.](https://ciphermysteries.com/2020/06/10/paolo-guinigi-and-ciphers)

### Milan (Visconti → Sforza)
- The famous Milanese ledger — **Francesco Tranchedino's cipher book, ÖNB Codex Vindobonensis
  2398** (~287 complete keys) — documents Sforza chancery practice **1450–1496**, under Cicco
  Simonetta's secretariat. It is *after* our window. **[C]** —
  [Facsimile Finder, "Francesco Tranchedino: Secret Diplomatic Documents"](https://www.facsimilefinder.com/facsimiles/francesco-tranchedino-secret-diplomatic-documents-facsimile);
  [Ziereis Facsimiles](https://www.facsimiles.com/facsimiles/francesco-tranchedino-diplomatic-secret-documents);
  [Buonafalce-related HistoCrypt paper, "Nicodemo Tranchedini's Diplomatic Cipher: New Evidence"](https://ep.liu.se/ecp/149/007/ecp18149007.pdf).
- Surviving *Visconti-era* (pre-1447) Milanese keys are conspicuously scarce; researcher Mark
  Knowles has publicly searched for 1430s Filippo Maria Visconti ciphers without a published find.
  Milan under the Visconti certainly ran enciphered diplomacy, but the key material we can point to
  is post-1450. **[C]** for the scarcity;
  [Pelling, "Milanese enciphered letters, call for help," 2011](https://ciphermysteries.com/2011/06/28/milanese-enciphered-letters-call-for-help);
  [Pelling 2017 post w/ Knowles comments](https://ciphermysteries.com/2017/07/08/new-paper-fifteenth-century-cryptography).
- Mid-century Milanese/Mantuan keys (Tranchedino ledger; a 1450 Mantuan ducal cipher) show the
  mature in-window toolkit scaled up: 2 homophones per consonant, 3 per vowel, shapes for doubled
  letters and common syllable groups (ab, ac, ad…), nulls, and mini-codebooks of common words
  (*come, quando, quanto, non*) growing to 80+ nomenclator entries. Pelling: the 1400–1460
  evolution is **scale, not concept** — more homophones, more nulls, bigger nomenclators. **[C]** —
  [Pelling 2016, ibid.](https://ciphermysteries.com/2016/07/06/fifteenth-century-cryptography)

### Papal curia
- The curia inherited the Lavinde practice; Meister, *Die Geheimschrift im Dienste der päpstlichen
  Kurie* (1906), collects papal keys but is thin on the early 15th century relative to the 16th.
  **[C]** — [Lasry et al., "Deciphering papal ciphers from the 16th to the 18th Century," *Cryptologia*, 2020](https://www.tandfonline.com/doi/full/10.1080/01611194.2020.1755915);
  [de.wikisource, "Aloys Meister"](https://de.wikisource.org/wiki/Aloys_Meister).

## 3. What demonstrably existed by 1440 — and what did not

**Existed (attested in-window):**
1. Monoalphabetic substitution with **invented symbol alphabets** (not just letter-to-letter). **[C]** (Lavinde; Tranchedino symbol keys; Fontana below)
2. **Homophones**, concentrated on vowels (Mantua 1401; Venice 1411). **[C]**
3. **Nulls** (from Lavinde 1379 onward). **[C]**
4. **Small nomenclators / codewords** for names and common words; whole keys that are *only*
   nomenclatures (Lucca). **[C]**
5. Signs for **doubled letters and common syllables/digraphs** (early verbose-ish elements). **[C]** (Pelling 2016)
6. **Partial encipherment** — cipher stretches embedded in plaintext letters (Guinigi archive). **[C]**
7. **Entire books in cipher by one individual**: Giovanni Fontana (Padua/Venice, physician-engineer,
   ~1395–after 1454) wrote *Bellicorum instrumentorum liber* and *Secretum de thesauro* (c. 1420s–1430s)
   in a simple monoalphabetic substitution with invented glyphs — proof that "cipher the whole
   manuscript" was a live practice in exactly our window and milieu, by a university-trained
   physician. **[C]** —
   [Philip Neal, "Fontana Cipher Manuscripts"](http://philipneal.net/voynichsources/fontana_cipher_manuscripts/);
   [Wikipedia, "Giovanni Fontana (engineer)"](https://en.wikipedia.org/wiki/Giovanni_Fontana_(engineer));
   [Pelling, review of *Le Macchine Cifrate di Giovanni Fontana*, 2008](https://ciphermysteries.com/2008/12/06/review-of-le-macchine-cifrate-di-giovanni-fontana).

**Not in evidence before ~1440 (post-window technology):**
1. **Polyalphabetic substitution** — Alberti, *De componendis cifris*, **c. 1466–67**, which also
   contains the first *Western* description of frequency analysis. **[C]** —
   [Wikipedia, "Alberti cipher"](https://en.wikipedia.org/wiki/Alberti_cipher);
   [HistoryofInformation.com, "Leon Battista Alberti Describes 'The Alberti Cipher'"](https://www.historyofinformation.com/detail.php?id=3161).
2. **Codified cryptanalysis** — earliest Western manual is Cicco Simonetta's *Regule ad extrahendum
   litteras ziferatas sine exemplo*, Pavia, **1474** (language ID via word-ending counts; vowel
   isolation; the q-u pattern). Arabic frequency analysis (al-Kindī, 9th c.) has no demonstrated
   Western transmission in this period. **[C]** —
   [Cipher Foundation, "Cicco Simonetta's Regule"](http://cipherfoundation.org/older-ciphers/voynich-manuscript/cicco-simonettas-regule/);
   [Pelling, "Cicco Simonetta's Treatise on Decipherment," 2016](https://ciphermysteries.com/2016/12/17/cicco-simonettas-treatise-on-decipherment);
   [Wikipedia, "History of cryptography"](https://en.wikipedia.org/wiki/History_of_cryptography).
3. **Large-scale verbose homophonic systems of Naibbe type** — *constructible* with period
   materials (Greshko's design constraint) but **not attested** in any surviving key. The Naibbe
   cipher is a modern demonstration of feasibility, not a historical find. **[C]** for
   non-attestation / **[D]** that absence of key ≠ absence of practice —
   [Greshko, "The Naibbe cipher," *Cryptologia*, 2025](https://www.tandfonline.com/doi/full/10.1080/01611194.2025.2566408).
4. Cipher disks, Vigenère-type autokeys, printed cipher treatises: all later 15th–16th c. **[C]** (Alberti/Trithemius lineage, ibid.)

## 4. Who used ciphers

- **Chanceries and diplomats** — the overwhelming majority of surviving material (Vatican, Mantua,
  Venice, Lucca, Modena, Milan). **[C]** (sources above)
- **Merchants** — attested from the **1430s** in Venice (Andrea Barbarigo's codes with agents;
  word-substitution "*in parabula*" methods), i.e. the tail end of our window; commercial secrecy
  culture predates professional state cryptology. **[C]** —
  [JSTOR Daily, "The Merchants of Venice—In Code"](https://daily.jstor.org/the-merchants-of-venice-in-code/),
  reporting Iordanou 2018.
- **Physicians/engineers/scholars** — Fontana (above) is the standing in-window exemplar of a
  medical-degree holder enciphering technical books; the broader scribal tradition (Bischoff)
  shows recipe- and margin-level concealment. **[C]**
- **Cipher secretaries as a profession** emerge visibly with Simonetta's secretariat (1450s Milan)
  and formally in Venice only in 1506. In-window encipherment was a chancery-clerk skill, not yet
  a specialized office. **[C]** — Iordanou 2018, ibid. **[D]** on the generalization.

## 5. What a cipher of this era would look like statistically

- **Monoalphabetic (Fontana-style):** all plaintext statistics survive relabeling — character
  entropy, conditional entropy h2, Zipf profile identical to the underlying language. Fontana's
  books read off almost trivially. **[C]** (Neal; Pelling 2008, above). VMS h2 ≈ 2.0 is far below
  any European plaintext (our own harness: H4 naturals 2.9–3.9, results/harness/benchmark.json),
  so a *plain* monoalphabetic cipher of Latin/Italian is excluded on our A-graded numbers. **[C/A]**
- **Homophonic/nomenclator (chancery-style):** *larger* symbol inventory than plaintext (dozens to
  ~300 units), *flattened* unigram frequencies, raised unigram entropy; code tokens for whole
  words. The VMS has the opposite profile — small core glyph set, highly *peaked* distributions,
  ultra-low h2 — which is the classic "too few symbols" argument against nomenclator/homophonic
  readings. **[C]** —
  [Wikipedia, "Voynich manuscript" (cipher-theories section)](https://en.wikipedia.org/wiki/Voynich_manuscript);
  [Greshko 2025, ibid.](https://www.tandfonline.com/doi/full/10.1080/01611194.2025.2566408)
- **Verbose substitution** (one plaintext letter → multi-glyph group) *inverts* both signatures:
  it shrinks the apparent alphabet and *lowers* conditional entropy, because glyph sequences become
  internally predictable — the mechanism by which Naibbe reproduces VMS-like stats (and consistent
  with our T0.3 replication: H2 reproduces the low-h2 property). **[C]** — Greshko 2025, ibid.
- **Presentation:** in-window ciphertexts typically preserve word divisions (or are re-spaced into
  word-like groups), are embedded in plaintext carriers, and are short (paragraphs, not books —
  Fontana excepted). Corrections and mixed hands are normal chancery features. **[C]** for word
  division and embedding (Pelling 2016/2020); **[D]** for the generalization to "typically."

## 6. Constraints for W5/W6 — what this rules in/out for a 1420s cipher hypothesis

1. **Ruled out on period-technology grounds:** polyalphabetic encipherment (post-1467) and any
   scheme presupposing Western frequency-analysis awareness (post-Alberti/Simonetta). A 1420s
   cipher hypothesis must be operable with tables/keys, pen, and at most card- or dice-like
   randomizers. **[C]**
2. **Ruled out on statistics (our A-grade numbers + this dossier):** straight monoalphabetic and
   classic homophonic/nomenclator forms — wrong direction on entropy and symbol count. **[C/A]**
3. **Ruled in as historically live:** (a) whole-book encipherment by a single scholar/physician
   (Fontana precedent — same decades, same region, same book-culture); (b) verbose/syllable-sign
   elements (doubled-letter and syllable signs are in real keys by mid-century); (c) heavy
   vowel-focused manipulation (the *first* thing Italian cipher designers attacked was vowel
   statistics). **[C]**, with the leap from "elements existed" to "a full verbose system existed"
   remaining **[D]** — this is exactly the gap the Naibbe hypothesis occupies.
4. **Sociological constraint for W6b:** in-window ciphers were held by chanceries and individual
   scholars; a 200+-page enciphered codex has *no* chancery use-case (keys are short; dispatches
   are short). A cipher hypothesis therefore implies a Fontana-like *private* actor, not a
   diplomatic office — means/motive/opportunity should be evaluated on that profile. **[D]**
5. **Negative-space datum for W6b:** VMS text shows near-absence of corrections, while chancery
   ciphertext production was correction-prone clerical work; and no key, no plaintext carrier, and
   no contemporary decrypt survives for the VMS, whereas real keys survive in the dozens per
   archive. Either datum can cut for or against cipher — flag, don't resolve. **[D]**

## 7. Flagged candidates for statistical tests (pipeline-ready)

We already have: Naibbe verbose-cipher generator (`src/ms408/harness/naibbe.py`, T0.3, golden-decrypt
byte-exact) and the T2.4 encoding bracket (verbose cipher · abjad+anagram · abbreviation ·
conlang · self-citation), with the T2.4 baseline finding that homophonic verbose ciphering erases
Montemurro–Zanette word-order information (0.000 vs 0.307). Candidates this dossier motivates:

- **T-1 Vowel-channel test.** Period designers homophoned *vowels first*. Build a
  vowel-only-homophone variant of the H2 generator (consonants monoalphabetic, 2–4 homophones per
  vowel, per Mantua 1401 / Venice 1411 / Mantua 1450 key shapes) and score it in the bracket —
  does selective vowel flattening move h1/h2 toward or away from VMS values?
- **T-2 Nomenclator admixture.** Add an 80-entry word-level codebook (per the 1450s keys) at
  varying plaintext-coverage rates to H2 output; measure effect on Zipf slope, type–token curve,
  and MZ information. Tests whether *any* nomenclator fraction is compatible with VMS word stats.
- **T-3 Nulls sweep.** Inject nulls at period-plausible rates into H2/H1 streams; measure entropy
  and word-grammar degradation — bounds how much null-padding a 1420s cipher could carry and still
  look like Voynichese.
- **T-4 Syllable-sign (proto-verbose) ladder.** Interpolate between attested practice (signs for
  doubled letters + ~20 common syllables) and full Naibbe verbosity; find the minimum verbosity
  level that reproduces the low-h2 + peaked-frequency signature. Locates the VMS's required
  technology on the attested→hypothetical axis — directly quantifies constraint 3's [D] gap.
- **T-5 Partial-encipherment probe.** Guinigi-style cipher-in-plaintext implies section-level
  statistical heterogeneity. We can invert this: test VMS section/dialect strata (L8) for
  signatures of *mixed* encoding regimes vs one uniform regime (ties into W6a's "single encoding
  layer" assumption audit).
- **T-6 Fontana control corpus.** Fontana's two manuscripts are deciphered and published (Battisti
  & Saccaro Battisti 1984); if a transcription is obtainable (licensing per L19, consume-only), a
  *real* in-window enciphered book is the ideal H2-adjacent control — measure whether its
  statistics behave as our monoalphabetic model predicts. → New D-item: pursue Fontana
  transcription acquisition?

---
*Prepared 2026-07-06 for T2.5. Grades: [A] harness-validated (referenced from results/), [C]
sourced, [D] inference/speculation. All URLs accessed 2026-07-06.*
