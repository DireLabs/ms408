# SOURCES.md — Verified Source Inventory (T0.2/T0.3)

Verified 2026-07-05 by Code session 1 research agents. Consume-only policy in force (L19) until
Tim revisits. Grades on statements here follow RESEARCH-PLAN §6 where applicable; this file is an
inventory, not a claims document.

## 1. Transliterations and page metadata (T0.2)

All files at `https://www.voynich.nu/data/` (index: transcr.html Table 8; README last updated 2026-03-24). Format spec: IVTFF v2.0.1, `voynich.nu/software/ivtt/IVTFF_format.pdf`.

| File | Role | Header | Completeness |
|---|---|---|---|
| `ZL3b-n.txt` (Zandbergen–Landini v3b, 2025-05-13) | **Primary EVA corpus (L11)** | `#=IVTFF Eva- 2.0 M 5` | Complete: 227 pages, all 5,389 loci |
| `GC2a-n.txt` (Claston v101, IVTFF conversion) | **v101 sensitivity corpus (L11)** | `#=IVTFF v101 2.0 M 6` | Complete; high-ASCII glyphs as `@nnn;` escapes |
| `voyn_101.txt` (Claston original) | v101 provenance reference | GC's own format, cp1252-style bytes | Complete |
| `RF1b-e.txt`, `IT2a-n.txt`, `VT0e-n.txt` | Alternates/cross-checks | IVTFF | Near-complete |

**Metadata embedded in IVTFF page headers — no manual join needed:**
`$Q` quire · `$P` page-in-quire · `$F` folio · `$B` bifolio · `$I` illustration section (H/A/Z/B/C/P/S/T) · `$L` Currier language (A/B) · `$H` **Fagin Davis scribe 1–5** (added in ZL v3; f115r uses in-line `<@H=n>` tags for a mid-page hand change) · `$C` Currier hand · `$X` extraneous writing. Locus types distinguish paragraph text vs. labels vs. circular/radial text — sub-page granularity for free.

**Verified reference counts (ZL3b, from the file itself — used as parser integrity checks in `tests/test_ivtff.py`):** 227 page headers; **5,385 locus lines** (transcr.html's "5,389 identified loci" doesn't match the distributed file's line count); `$I`: H=129, S=25, B=19, **P=16**, Z=12, C=11, A=8, T=7 (a commented-out header for f101r2 carries one extra `$I=P` — it's a comment, not a page); `$L`: A=114, B=83, unassigned=30; `$H` present on all 227 pages (113/46/33/27/7 for scribes 1–5, plus f115r `@`). **GC2a (v101):** 226 pages, 5,367 loci — identical page set except f116v (marginalia page, never in v101; appendix-only for us per L12).

**License:** no formal instrument. Zandbergen's roadmap.html states the transliterations "have always been in the public domain" (site copyright and non-commercial restriction apply to images, not transliteration data). v101's author (Tim Rayhel/Glen Claston) died 2014 — no grant obtainable. Treat as public-domain-by-community-convention: fine under consume-only (L19); email Zandbergen before any verbatim redistribution if D9 lands on publication.

**Risks:** files version-bump in place (`ZL3a→3b` in 2025; `beta/` and `previous/` subdirs exist) — pin exact filenames and checksums, archive local copies immediately. 30 pages lack Currier `$L` (mostly astro/cosmo pages Currier never classified) — stratified analyses must handle "unassigned". `$H` is Zandbergen's encoding of Davis's assignments and a few are flagged uncertain in her paper (e.g., Rose side of Q14) — cheap manual cross-check against her Jan 2025 "Voynich Codicology" blog diagrams is worthwhile insurance before T2.x.

## 2. Beinecke scans (T0.2)

- **Canonical record:** collections.library.yale.edu/catalog/2002046 (the old brbl-dl platform is retired).
- **IIIF (tested live):** Presentation 3.0 manifest at `https://collections.library.yale.edu/manifests/2002046` — **213 canvases**, front cover through back cover including all fold-outs (rosettes widest at 9078 px). Image API v2 level 2 per canvas; `full/full/0/default.jpg` verified working even on the largest fold-out despite the nominal `maxArea` cap. Take image oids from the manifest (not contiguous); preserve canvas labels (folio numbers) for filenames.
- **Rights:** Yale Open Access Policy — "Open access digital images may be used by anyone for any purpose." Download, computational use, and redistribution permitted; attribution customary. No machine-readable license URI in the manifest (its per-image "Rights" field is cautious boilerplate) — cite the policy when redistributing. **This substantially relaxes the D10/L19 concern for scans specifically.**
- **Download plan:** polite manifest crawl (213 requests, ≤2 concurrent), ~2–3.5 MB per regular folio, **≈0.6–0.9 GB total** as served JPEGs. IIIF JPEGs are recompressed derivatives — adequate for annotation work; if pixel-critical analysis ever matters, the archive.org 2014-JP2 mirror (`archive.org/details/voynich`, 2.19 GB, unofficial provenance) or a masters request to Beinecke are the fallbacks.
- **Crawler guards:** verify returned pixel dimensions against canvas width/height (fall back to tile-stitching if Yale starts enforcing maxArea); note current set is 213 images vs. ~225 in the 2014 file set if reconciling against older research datasets.

## 3. Key papers: generators and replication targets (T0.3, T1.1)

### Generators (to reimplement)

| Paper | Citation | Access | Reimplementation basis |
|---|---|---|---|
| Naibbe cipher (H2 generator) | Greshko, M. A. (2025). "The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript–like ciphertext." *Cryptologia*, online-first. DOI 10.1080/01611194.2025.2566408 | **Open access** (T&F, browser only — 403s bots) | Author Python reference impl: github.com/greshko/naibbe-cipher (modified MIT, attribution required); cipher tables on Zenodo DOI 10.5281/zenodo.16415087 (CC-BY 4.0). Feasibility: **excellent** |
| Self-citation (H3 generator) | Timm, T. & Schinner, A. (2020). "A possible generating algorithm of the Voynich manuscript." *Cryptologia* 44(1), 1–19. DOI 10.1080/01611194.2019.1596999 | Journal **paywalled**; algorithm free via arXiv:1407.6639 | Author source code: github.com/TorstenTimm/SelfCitationTextgenerator and /VoynichTextGenerator. Feasibility: **good** (verify 2020 parameter values vs. arXiv version — see risks) |

### Replication targets (G1) and baselines

| Paper | Citation | Access | What we take from it |
|---|---|---|---|
| Character entropy | Lindemann, L. & Bowern, C. (2020/21). "Character Entropy in Modern and Historical Texts." arXiv:2010.14697 | **Free** (arXiv) | h2 ≈ 2 for Voynichese vs. ≈3–4 natural languages; robust across transcription/scribe/dialect; per-language h2 tables in appendix |
| Linguistics survey | Bowern, C. & Lindemann, L. (2021). "The Linguistics of the Voynich Manuscript." *Annu. Rev. Linguist.* 7, 285–308 | Paywalled; **free preprint** lingbuzz/005415 | Zipf's law + law of abbreviation confirmations; survey framing for W6a |
| Long-range structure | Montemurro, M. A. & Zanette, D. H. (2013). "Keywords and Co-Occurrence Patterns in the Voynich Manuscript." *PLoS ONE* 8(6):e66344 | **Open access** (CC-BY) | Scale-dependent word-entropy peak at ~600–800-word scale; informative-word rankings; co-occurrence networks |
| Scribal hands | Fagin Davis, L. (2020). "How Many Glyphs and How Many Scribes?" *Manuscript Studies* 5(1) | **OA copies**: Penn ScholarlyCommons repository.upenn.edu/mss_sims/vol5/iss1/6 | 5-scribe model (L8 stratification covariate) |
| Algorithmic decipherment | Hauer, B. & Kondrak, G. (2016). "Decoding Anagrammed Texts Written in an Unknown Language and Script." *TACL* 4, 75–86 | **Open access** (CC-BY, aclanthology.org/Q16-1006) | Encoding-bracket baseline (abjad+anagram family). Treat VM application as method baseline, not accepted result — widely criticized |
| Grille hoax | Rugg, G. (2004). "An Elegant Hoax?" *Cryptologia* 28(1), 31–46. DOI 10.1080/0161-110491892755 | **Paywalled**; method documented free in Zandbergen & Rich 2021 critique (voynich.nu/papers/Grilles_RZ_2021.pdf) | Table-and-grille mechanism context for H3 family; exact replication would need ILL |

## 4. H4 control corpora (T0.3, per L13: Latin + Italian + MHG + Hebrew)

| Language | Recommended source | Format / download | License | Notes |
|---|---|---|---|---|
| Medieval Latin | **Corpus Corporum** (mlat.uzh.ch) — Patrologia Latina, Vulgate, medieval scientific collections | TEI-XML, per-text download (no bulk endpoint) | Per-source; PD-source texts safe | Genre-matched Latin herbal (Macer Floridus, *Circa instans*) needs one follow-up title-level search. Latin Library = fallback only ("personal/educational" terms) |
| Early Italian | **Biblioteca Italiana** (TEI, 13th–15th c. prose) + **Liber Liber** Decameron (~365k words, instant) | TEI-XML per-text / plain txt bulk | BI: non-commercial research OK; LL: PD + CC BY-NC-SA apparatus | OVI is the gold standard but query-only, no export (site unreachable at check). LL orthography is modernized — affects char-level stats |
| Middle High German | **ReM** (1050–1350, ~2M forms) + **ReF** (1350–1650, incl. Arzneibuch medical prose) | Bulk CorA-XML / TEI / JSON | **CC BY-SA 4.0** (cleanest of all) | Period-correct German for early-15th-c. is technically ENHG (ReF); label accordingly in analyses |
| Hebrew | **Sefaria-Export** (github.com/Sefaria/Sefaria-Export; GCS bucket) — filter to PD/CC0/CC-BY versions | JSON + plain txt, scripted bulk | Per-text license field | Mishneh Torah = ideal single work (large, medieval, plain prose). WLC (tanach.us, unrestricted) as second register. Medieval Hebrew *medical* texts absent from open corpora — accept genre mismatch |

## Risks / open items

1. **Automated-fetch blocks:** Taylor & Francis and Annual Reviews 403 bots — pull from GitHub/Zenodo/arXiv/ACL/PLOS mirrors in scripts; Greshko OA paper needs a manual browser download.
2. **Timm–Schinner parameter fidelity:** confirm the 2020 journal parameters match arXiv:1407.6639 + published code (author copies on academia.edu/ResearchGate, or ILL).
3. **Normalization confound (H4):** diplomatic transcriptions (ReM/ReF) preserve abbreviations; critical editions (BI, Patrologia) silently expand them. Character-entropy and word-length stats are not comparable across edition types without a normalization pass — this must be a deliberate pipeline stage with its own documentation.
4. **Italian access fragility:** OVI unreachable; Biblioteca Italiana historically flaky — archive local copies early (consume-only, gitignored per L19).
5. **Naibbe pagination:** Greshko 2025 is online-first — recheck volume/issue before any write-up; take cipher tables from Zenodo (CC-BY) rather than paper figures.
6. **Hebrew/Latin genre gaps:** no open machine-readable medieval Hebrew medical prose; Latin herbal availability unconfirmed at title level. Flag at T0.3 corpus assembly if it materially weakens the encoding bracket.
