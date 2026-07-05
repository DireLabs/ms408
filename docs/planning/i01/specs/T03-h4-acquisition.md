# T03 — H4 Control Corpus Acquisition Report

Acquired 2026-07-05. Consume-only (L19): everything lives in `data/raw/h4/` (gitignored), nothing
committed. Full per-file provenance (URLs, sha256, bytes, licenses) in `data/raw/h4/MANIFEST.json`.
Target per L13: Latin + Italian + German (period-correct: ENHG) + Hebrew, ≥ ~200k chars per
language, prose, medical/herbal genre where available. Voynich reference size: ~38k words / ~170k chars.

## What was acquired

### Latin (`data/raw/h4/latin/`) — target met, genre partially met
| File | Text | Size | License |
|---|---|---|---|
| `vulgate_bible-corpus_Latin.xml` | Vulgate (whole Bible), CES-XML | 4.9 MB, ~3.37M text chars, 534k words | Text PD; packaging: christos-c/bible-corpus (no explicit repo license — consume-only OK) |
| `macer_floridus_de_viribus_herbarum.wikitext.json` | Macer Floridus, *De viribus herbarum* (11th c. herbal) | ~98k chars after markup strip | PD (11th-c. text, 1845 Panckoucke ed.; via la.wikisource, sourced from Corpus Corporum) |

- Vulgate: 4th-c. text but the ubiquitous medieval Latin register; modern critical-style e-text
  (no punctuation, abbreviations expanded).
- Macer Floridus is genre-matched (herbal, matching the VM herbal section) but **verse**
  (hexameters), not prose — SOURCES.md already flagged this. It alone is ~98k chars (< 200k);
  treat as a genre-stratified supplement, with the Vulgate carrying the volume requirement.

### Italian (`data/raw/h4/italian/`) — target met
| File | Text | Size | License |
|---|---|---|---|
| `boccaccio_decameron_branca.zip` / `.txt` | Boccaccio, *Decameron*, ed. Vittore Branca (Mondadori 1985, from the Hamilton 90 autograph) | ~1.51M chars | Underlying text PD ("DIRITTI D'AUTORE: no"); Liber Liber e-book license (CC BY-NC-SA 4.0 apparatus) |

- Better than expected: SOURCES.md warned the Liber Liber Decameron was orthographically
  modernized, but the edition actually served is **Branca's critical edition from the autograph** —
  orthography is substantially 14th-century. Period (1349–1353) and language are a good match;
  genre is narrative prose, not medical.

### German (`data/raw/h4/german/`) — target met, incl. period-correct medical prose
| File | Corpus | Size | License |
|---|---|---|---|
| `ReM-v2.1_tei.zip` | Referenzkorpus Mittelhochdeutsch (1050–1350), 409 TEI texts, ~2M forms | 27.9 MB (199 MB unzipped) | CC BY-SA 4.0 |
| `ReF-v1.0.2.tar.gz` | Referenzkorpus Frühneuhochdeutsch (1350–1650), 223 CorA-XML texts | 143.5 MB | Zenodo metadata CC BY 4.0, bundled LICENSE CC BY-SA 4.0 — treat as CC BY-SA 4.0 |

- ReF contains the genre/period ideal: **F120 "Ulmer Wundarznei"** (4th quarter 15th c., Swabian,
  medical prose, scribe Magnus Bengger) — closest of all acquisitions to the VM window (1404–1438).
  Also relevant: F081 *Feldbuch der Wundarznei* (early 16th c.), F151 *Arzneibuch* (17,1),
  F167 *Kräuterbuch/Rezeptsammlung* (16,1), F292 *Wundarznei* (16,1).
- ReM is pre-VM-period MHG; label analyses accordingly (L13 note). Use ReF for period-correct ENHG.

### Hebrew (`data/raw/h4/hebrew/`) — target met, genre mismatch as expected
7 books of Maimonides, *Mishneh Torah* (1170–1180), version **"Torat Emet 363" — license field
"Public Domain"** (verified in each file; versionSource toratemetfreeware.com), from the
Sefaria-Export public GCS bucket (`storage.googleapis.com/sefaria-export/`):

Foundations of the Torah, Human Dispositions, Foreign Worship, Repentance, Torah Study (= all of
Sefer Madda), plus Sabbath and Forbidden Foods. **Totals: 752,678 chars pointed / 459,333 chars
after nikud stripping** — comfortably over target either way.

- Genre: legal/codificatory prose. No open machine-readable medieval Hebrew *medical* prose exists
  (SOURCES.md risk 6) — accepted mismatch; Forbidden Foods (dietary law) is the closest practical
  register. Human Dispositions ch. 4 is a health/diet regimen — a small genuine regimen-genre patch.

## Substitutions and dead ends (documented per task rules)

1. **Corpus Corporum (mlat.uzh.ch)**: the recommended per-text TEI download is not scriptable —
   the site is a JS app whose BaseX backend returns 401 to direct requests. The Macer Floridus text
   was obtained via la.wikisource, whose page metadata credits Corpus Corporum as its source.
   *Circa instans* (prose): no open machine-readable copy found — gap stands.
2. **Clementine Vulgate project** (vulsearch.sourceforge.net): defunct (404). Substituted the
   bible-corpus XML Vulgate (verified content, e.g. Gen 1:1).
3. **ReF Lesetexte** (51.8 MB): downloaded, found to be PDF renderings only — discarded; replaced
   by the full ReF CorA-XML tarball.
4. **Deutsches Textarchiv** (Brunschwig 1497 etc.): probed as a lighter ENHG-medical alternative;
   book IDs could not be resolved non-interactively. ReF covers the need.
5. Total download traffic ≈ 230 MB (incl. the discarded 51.8 MB Lesetexte probe); ~178 MB retained
   on disk. Slightly over the ~200 MB soft cap due to the Lesetexte dead end; all downloads
   sequential.

## Recommended preprocessing per file (input to the normalization pipeline stage)

| File | Steps |
|---|---|
| Vulgate XML | Parse CES-XML, extract `<seg>` verses, join; note: abbreviations expanded, no punctuation (edition artifact) |
| Macer Floridus | Strip wikitext (`{{titulus2}}`, `{{Versus|n}}`, `<poem>`, `==headings==`); keep verse-line structure only if wanted; stratify as VERSE |
| Decameron | **Transcode cp1252 → UTF-8**; strip ~60-line Liber Liber boilerplate header and any trailing apparatus; abbreviations expanded (critical edition) |
| ReM TEI | Unzip; per-text TEI parse; extract diplomatic token forms; select prose subset via teiHeader genre/date; **diplomatic — abbreviations preserved** |
| ReF CorA-XML | Untar; parse CorA-XML (`<token>/<dipl>/<anno>`, spec: cora.readthedocs.io); start with F120; **diplomatic — abbreviations preserved** |
| Mishneh Torah JSON | Flatten nested `text` lists; strip stray HTML tags; produce two registers: pointed and consonantal (strip U+0591–U+05C7); analyze separately |

**Cross-corpus caveat (SOURCES.md risk 3, restated):** the set mixes critical editions with
expanded abbreviations (Vulgate, Decameron, Macer) and diplomatic transcriptions with preserved
abbreviations (ReM, ReF). Character-entropy and word-length statistics are not comparable across
these edition types without an explicit normalization pass — that pass must be a documented
pipeline stage before any H4 comparison is reported.

**Open decision flag (per "flag, don't resolve"):** whether H4 comparisons should use pointed or
consonantal Hebrew as primary (consonantal recommended — closer to what a medieval scribe wrote —
but this is a methodological choice Tim should ratify), and whether verse texts (Macer) enter the
main bracket or a genre-stratified side analysis.
