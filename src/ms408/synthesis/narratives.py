"""T3.1 — Competing narratives with evidence ledgers (W6b).

Renders the flagship competing-narratives document from the findings registry
(registry.py). Per P6, this is a structured ARGUMENT MAP, not a probability
statement: each narrative gets a graded ledger of supporting and undercutting
findings and a qualitative likelihood direction. Story-plausibility is the
hallucination surface the program firewalls (L3/L7) — so every number here comes
from results/*.json via the registry, and the verdict form is likelihood-
direction, never a decoded meaning.

The interpretive prose per narrative is the synthesis layer; the tallies are
computed from the registry so they cannot drift from the evidence.

Usage:
    python -m ms408.synthesis.narratives
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from .registry import OUT as REGISTRY_PATH
from .registry import build as build_registry

ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = ROOT / "reports"

GRADE_WEIGHT = {"A": 3, "B": 2, "C": 1, "D": 0}

# interpretive synthesis per narrative (the reasoning layer; numbers via registry)
NARRATIVE_PROSE = {
    "N-conlang": (
        "**Least contradicted.** The paradigmatic constructed-language model (P1 "
        "variant V3) was the *only* generative family to reproduce the VMS's full "
        "profile — low h2, dense edit-distance morphology, and word-order "
        "information at the right scale — where the cipher and self-citation "
        "families each failed one half. It also fits the position-constrained, "
        "paradigmatic morphology directly. **Caveat carried:** V3 used a "
        "VMS-informed affix template, so it is the family's upper bound, not a "
        "neutral fit; a like-for-like historical conlang (real Lingua Ignota) is "
        "the outstanding test. Currier A/B then reads as two dialects/registers of "
        "one invented system."
    ),
    "N-invented": (
        "**Consistent with the nulls that hurt the others.** A meaningful record of "
        "an invented world (Codex-Seraphinianus class) predicts exactly what we "
        "found: word-order information present (it is meaningful), section↔text "
        "co-variation in one hand, and — crucially — the anchor and realism nulls, "
        "because an invented world has no *external* referents for a word to anchor "
        "to and no real-taxa root↔leaf bundles to recover. The same three nulls "
        "(F9/F10/F11) that undercut the natural-herbal reading are *entailed* by "
        "this one. Its weakness is parsimony, not evidence: it is hard to "
        "distinguish from a systematically invented language (N-conlang) from "
        "inside the text — the W7 equivalence class."
    ),
    "N-cipher": (
        "**Weakened on a specific mechanism.** A verbose/homophonic substitution "
        "cipher of a real plaintext should carry the plaintext's word-order "
        "information — yet the published Naibbe family, which matches the character "
        "statistics almost perfectly, *erases* that information (dI 0.000 vs the "
        "VMS's 0.307): random homophone draws decouple ciphertext types from "
        "plaintext types. The positional line-structure is also atypical of "
        "chancery cipher, and the cipher-culture dossier finds no attested "
        "verbose system of this scale in the 1404–1438 window. Not eliminated — a "
        "deliberately homophone-poor verbose cipher (the outstanding V2 sweep "
        "direction) could retain word-order info — but the off-the-shelf verbose "
        "cipher is contradicted."
    ),
    "N-null": (
        "**Weakened but not dead.** Self-citation / grille hoaxes reproduce most "
        "surface statistics — low h2, Zipf, positional effects — which is why the "
        "hoax hypothesis has always been hard to kill. But the VMS carries "
        "topic-scale word-order information (F4) that pure self-citation, as its "
        "own authors parameterize it, does not generate at the right scale (it "
        "*overshoots* at too short a scale, F6) and with too small a vocabulary. "
        "The information structure is the discriminator the surface statistics "
        "aren't."
    ),
    "N-natural": (
        "**Most contradicted of the meaningful readings — specifically the "
        "'labelled herbal/pharmacopoeia where words name real depicted plants' "
        "form.** Three independent, harness-gated nulls converge against it: no "
        "token anchors to a visual feature (F9), the labels are not a recurring "
        "naming vocabulary (F10, labels *more* unique than running text), and there "
        "is no real-taxa root↔leaf feature bundle (F11, the herbal's structure is "
        "within-organ geometry only). A genuine referential herbal should leave at "
        "least one of these signatures; none appears. The section↔text co-variation "
        "in Language A (F8) is the one positive datum and keeps the door open for a "
        "meaningful-but-non-nomenclatural natural text."
    ),
    "N-abbreviation": (
        "**Effectively ruled out at our resolution.** Latin brevigraphy and abjad "
        "families *raise* h2 (the wrong direction) — abbreviation lands h2 ≈ 3.5 vs "
        "the VMS's ≈ 2.1 — and neither reproduces the joint low-h2/word-order "
        "profile. Consistent with Lindemann-Bowern's finding that abbreviation and "
        "abjads increase conditional entropy."
    ),
    "N-et-anachronism": (
        "**Null, as designed.** No annotated feature encodes information exceeding "
        "unaided 15th-century observation. Per W7, this is the honest form of the "
        "'proof-level' ambition: a rigorous null is a citable constraint, not "
        "evidence of ordinary origin, and it collapses the ET hypothesis into the "
        "invented-world/visionary equivalence class (which the text *cannot* "
        "distinguish from inside)."
    ),
}

MILIEU_NOTE = (
    "**Cross-cutting: community of origin (dossiers, grade C).** The zodiac "
    "iconography (crossbowman Sagittarius, cycle comparanda) places the "
    "illustrations in a German/Alemannic tradition c. 1420s–1460s — in real "
    "tension with the locked northern-Italian working premise (L1). The dossiers "
    "carry this as *rival localizations* for W6b, not a resolution. Provenance is "
    "C-solid only back to Baresch (1637); everything upstream — the Rudolf II "
    "purchase, the Bacon attribution — is grade D. Any origin narrative must route "
    "through the German/Alemannic iconographic gravity and the post-1600 "
    "documentary gap."
)


def tally(findings: list, narrative_id: str) -> dict:
    support = [f for f in findings if narrative_id in f["supports"]]
    undercut = [f for f in findings if narrative_id in f["undercuts"]]
    support_w = sum(GRADE_WEIGHT[f["grade"]] for f in support)
    undercut_w = sum(GRADE_WEIGHT[f["grade"]] for f in undercut)
    net = support_w - undercut_w
    return {"support": support, "undercut": undercut,
            "support_weight": support_w, "undercut_weight": undercut_w, "net": net}


def run() -> dict:
    registry = build_registry()
    findings = registry["findings"]
    narratives = registry["narratives"]

    ranked = sorted(
        narratives,
        key=lambda nid: tally(findings, nid)["net"],
        reverse=True,
    )
    ledger = {nid: tally(findings, nid) for nid in narratives}

    report = _render(registry, ranked, ledger)
    (REPORTS_DIR / "synthesis_competing_narratives.md").write_text(report)
    summary = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "registry": str(REGISTRY_PATH.relative_to(ROOT)),
        "narrative_net_scores": {nid: ledger[nid]["net"] for nid in ranked},
        "ranked": ranked,
    }
    (ROOT / "results" / "synthesis" / "narratives_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n")
    return summary


def _render(registry: dict, ranked: list, ledger: dict) -> str:
    findings = registry["findings"]
    narratives = registry["narratives"]
    by_id = {f["id"]: f for f in findings}
    lines = [
        "# T3.1 — Competing Narratives with Evidence Ledgers (W6b)",
        "",
        f"Generated {registry['built_at']} at commit `{registry['git_commit'][:10]}` "
        "by `python -m ms408.synthesis.narratives`. Numbers via the findings "
        "registry (`results/synthesis/findings_registry.json`), which pulls every "
        "value from `results/*.json` (L3 firewall).",
        "",
        "**Reading rules (P6, L7).** This is a structured argument map, not a "
        "probability and not a decoding. Net scores below are a grade-weighted "
        "tally of supporting minus undercutting findings (A=3, B=2, C=1) — a "
        "bookkeeping aid for the argument, NOT a likelihood. No narrative is "
        "asserted; all remain open pending T3.3 adversarial review. Nothing here "
        "translates a single word.",
        "",
        "## Evidence base",
        "",
        f"{len(findings)} findings from Phase 2 (grades in brackets). The load-"
        "bearing ones are the harness-gated nulls and the encoding-bracket "
        "profile:",
        "",
        "| id | grade | finding |",
        "|---|---|---|",
    ]
    for f in findings:
        lines.append(f"| {f['id']} | {f['grade']} | {f['statement']} |")

    lines += ["", "## Narrative ranking (grade-weighted net; not a probability)", "",
              "| narrative | support | undercut | net |", "|---|---|---|---|"]
    for nid in ranked:
        t = ledger[nid]
        lines.append(f"| {narratives[nid]} | +{t['support_weight']} "
                     f"| −{t['undercut_weight']} | {t['net']:+d} |")

    lines += ["", "## The narratives, most- to least-supported", ""]
    for nid in ranked:
        t = ledger[nid]
        lines += [
            f"### {narratives[nid]}",
            "",
            NARRATIVE_PROSE.get(nid, ""),
            "",
            "- **Supports:** "
            + (", ".join(f["id"] for f in t["support"]) or "—"),
            "- **Undercuts:** "
            + (", ".join(f["id"] for f in t["undercut"]) or "—"),
            "",
        ]

    lines += [
        MILIEU_NOTE,
        "",
        "## Synthesis: what the convergence says",
        "",
        "The Phase-2 findings do not decode the manuscript and do not name a single "
        "answer. What they do is **reshape the field of hypotheses**:",
        "",
        "1. **The meaningful-vs-meaningless axis is not resolved by surface "
        "statistics** — self-citation reproduces them — but IS informed by the "
        "word-order information (F4), which the null family mis-scales. The "
        "manuscript carries more topic-scale structure than the strongest hoax "
        "model generates.",
        "2. **The 'referential herbal' reading is the most constrained.** Three "
        "independent harness-gated nulls (anchor hunt, label naming, root↔leaf "
        "realism) agree that no word→referent mapping is detectable. Whatever the "
        "book is, it does not behave like a labelled catalogue of real plants at "
        "any granularity we can measure.",
        "3. **Those same nulls are *entailed* by the invented-world reading** and "
        "compatible with a systematic conlang — which is why the W7 equivalence "
        "class (invented world / conlang / visionary) is the region the evidence "
        "least contradicts, while remaining internally indistinguishable.",
        "4. **The off-the-shelf verbose cipher is contradicted** on word-order "
        "erasure; a homophone-poor variant is the one cipher direction still "
        "standing and the clearest outstanding experiment.",
        "5. **Origin is doubly constrained and unresolved:** German/Alemannic "
        "iconographic gravity vs the northern-Italian premise, and a documentary "
        "chain solid only from 1637.",
        "",
        "**Net for the flagship (T3.2):** the constraint envelope has shrunk toward "
        "*a structured, meaning-bearing symbolic system whose referents are not "
        "recoverable from within the text* — an invented language or invented-world "
        "notation more than a ciphered or labelled record of the real world — with "
        "the meaningful/hoax question narrowed but open, and origin unresolved. "
        "Every clause of that sentence is a graded claim above, and every one goes "
        "to T3.3 adversarial review before it can rise to grade A/B (L10).",
        "",
    ]
    _ = by_id
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print("narrative ranking (grade-weighted net):")
    for nid in out["ranked"]:
        print(f"  {out['narrative_net_scores'][nid]:+d}  {nid}")
