"""E5 — Fair encoding bracket (i02, critique C1).

The i01 bracket (T2.4) had three holes the C1 refutation flagged:
  1. CIRCULAR TUNING — only the conlang was hand-tuned toward the VMS; every
     other family ran a single default parameterization. A "win" under unequal
     tuning is meaningless.
  2. COLLINEAR DOUBLE-COUNTING — the mean-|z| distance summed 11 metrics as if
     independent, so correlated pairs (h1/h2, TTR/word-length) voted twice.
  3. NO COMPOSED FAMILIES and NO uncertainty — encodings were tested pure, and
     the ranking carried no error bars, so an accidental ordering read as real.

E5 fixes all three under one protocol:
  * EQUAL TUNING BUDGET — every family exposes a scalar mechanism knob on the
    SAME 6-point grid; each is tuned to minimise its distance to the VMS on a
    FIT half of the tokens.
  * HELD-OUT SCORING — the tuned knob is then scored on a DISJOINT held-out half
    (fit on first half, score on second), so tuning cannot overfit the metrics.
  * DE-COLLINEARISED DISTANCE — the 11 metrics are grouped into 6 pre-declared
    clusters (character-entropy, lexical-richness, distributional, morphology-
    network, positional, word-order); each cluster gets ONE vote, killing the
    double-count. The empirical metric correlation matrix is emitted so the
    grouping is auditable.
  * COMPOSED FAMILIES — cipher-of-conlang and abbreviation-of-agglutinative are
    added to the five base families.
  * BOOTSTRAP CIs — the held-out cluster distance for each family is block-
    bootstrapped (150 resamples) for a 95% CI, and we report the probability
    that the point-winner is truly the closest family.

Knobs (each a 6-point grid; mechanism-meaningful, not cosmetic):
  verbose_cipher       homophony fraction h — fraction of plaintext types given
                       multiple ciphertext spellings (E2's ΔI-destroying axis).
  selfcitation         max_repeat_count 1..6 — copying intensity.
  abjad_anagram        anagram fraction a — fraction of words alphagram-sorted.
  abbreviation         abbreviation rate r.
  conlang_relex        paradigm strength p — fraction of the lexicon placed on
                       shared-stem inflectional templates (builds the ED1
                       morphology network); p=0 is i01's non-paradigmatic conlang.
  cipher_of_conlang    homophony h over a fixed-paradigm (0.5) conlang.
  abbrev_of_agglut     abbreviation rate r over agglutinative (multi-morpheme) words.

Pass/fail (C1). If conlang_relex still ranks 1 on the HELD-OUT clustered distance
with equal tuning AND the bootstrap says it is robustly closest (P >= 0.9,
CI-separated from the runner-up) -> "conlang best fit" EARNS grade B. If the gap
closes (some non-conlang family ties/wins, or the winner's lead is not bootstrap-
robust) -> the i01 downgrade is CONFIRMED: no family is distinguished, the bracket
is descriptive only (grade C).

Usage:
    python -m ms408.experiments.e5_encoding_fair
"""

from __future__ import annotations

import json
import math
import random
import statistics
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from ..dataset import git_commit
from ..h4 import H4_OUT
from ..studies.encoding import METRICS, profile, vms_stream

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "experiments"
REPORTS_DIR = ROOT / "reports"

SEED = 408
GRID = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)  # continuous-knob families
DEFAULT_IDX = 2  # knob used to fix the z-normalisation reference frame
BOOTSTRAP = 150
# Block bootstrap must preserve correlation structure beyond the VMS's word-order
# scale (ΔI peaks at ~812 tokens). A block shorter than that destroys the MZ signal
# and biases the resampled distances (the block must exceed the longest scale we
# score). 2500 > 812 keeps the peak intact within each block.
BLOCK = 2500

_ALPHABET = "abcdefghiklmnoprst"  # ~18 glyphs, VMS-EVA-scale inventory
_VOWELS = set("aeiou")


# ---------------------------------------------------------------------------
# Source streams
# ---------------------------------------------------------------------------


def _vulgate_tokens(n: int) -> list:
    return (H4_OUT / "latin_vulgate.txt").read_text(encoding="utf-8").split()[:n]


def _hebrew_tokens(n: int) -> list:
    return (H4_OUT / "hebrew_mishneh_torah_consonantal.txt").read_text().split()[:n]


def _rand_word(rng: random.Random, syllables: int) -> str:
    w = ""
    for _ in range(syllables):
        w += rng.choice([c for c in _ALPHABET if c not in _VOWELS])
        w += rng.choice("aeio")
    return w


# ---------------------------------------------------------------------------
# Family generators — each returns a token stream of length ~n given a knob
# ---------------------------------------------------------------------------


def fam_verbose_cipher(n: int, h: float, seed: int = SEED) -> list:
    """Verbose homophonic substitution. Each plaintext letter expands to a fixed-
    width 2-glyph unit (verbose), but has a homophone TABLE of 3 alternate units.
    A fraction h of plaintext TYPES are homophonic (a fresh unit drawn per letter
    per occurrence, so one plaintext type maps to many ciphertext types of the
    SAME length); the rest are deterministic (first unit). Homophony is thus
    isolated from length — it decouples ciphertext types from plaintext types,
    the mechanism E2 showed destroys ΔI."""
    rng = random.Random(seed)
    toks = _vulgate_tokens(n)
    options = {c: [_rand_word(rng, 1) for _ in range(3)] for c in set("".join(toks))}
    is_homo = {t: rng.random() < h for t in set(toks)}
    det_cache: dict = {}
    out = []
    for t in toks:
        if is_homo[t]:
            out.append("".join(rng.choice(options[c]) for c in t) or _rand_word(rng, 1))
        else:
            if t not in det_cache:
                det_cache[t] = "".join(options[c][0] for c in t) or _rand_word(rng, 1)
            out.append(det_cache[t])
    return out


def fam_selfcitation(n: int, max_repeat: int, seed: int = 19) -> list:
    from ..harness.selfcitation import SelfCitationConfig, SelfCitationGenerator
    gen = SelfCitationGenerator(
        SelfCitationConfig(lines_to_create=3800, max_repeat_count=max_repeat),
        seed=seed,
    ).generate()
    return [w for line in gen.lines for w in line][:n]


def fam_abjad_anagram(n: int, a: float, seed: int = SEED) -> list:
    rng = random.Random(seed)
    out = []
    for w in _hebrew_tokens(n):
        out.append("".join(sorted(w)) if rng.random() < a else w)
    return out


def fam_abbreviation(n: int, r: float, seed: int = SEED) -> list:
    rng = random.Random(seed)
    out = []
    for w in _vulgate_tokens(n):
        if len(w) > 4 and rng.random() < r:
            if rng.random() < 0.5:
                out.append(w[:3])
            else:
                skel = "".join(c for c in w[1:-1] if c not in _VOWELS)
                out.append(w[0] + skel + w[-1])
        else:
            out.append(w)
    return out


def _conlang_lexicon(types_by_rank: list, p: float, rng: random.Random) -> dict:
    """Map plaintext types to invented words; a fraction p are placed on shared-
    stem inflectional templates (many ED1 neighbours = morphology network), the
    rest are atomic random words."""
    suffixes = ["a", "o", "e", "an", "or", "en", "al", "ir"]
    lexicon: dict = {}
    paradigmatic = [t for t in types_by_rank if rng.random() < p]
    atomic = [t for t in types_by_rank if t not in set(paradigmatic)]
    # group paradigmatic types into lemmas of ~len(suffixes); share a stem
    for i in range(0, len(paradigmatic), len(suffixes)):
        stem = _rand_word(rng, rng.choice([1, 2]))
        for j, t in enumerate(paradigmatic[i:i + len(suffixes)]):
            lexicon[t] = stem + suffixes[j % len(suffixes)]
    used = set(lexicon.values())
    for rank, t in enumerate(atomic):
        syll = max(1, min(4, 1 + int(math.log2(rank + 2) / 2.5)))
        w = _rand_word(rng, syll)
        while w in used:
            w = _rand_word(rng, syll)
        used.add(w)
        lexicon[t] = w
    return lexicon


def fam_conlang_relex(n: int, p: float, seed: int = SEED) -> list:
    rng = random.Random(seed)
    toks = _vulgate_tokens(n)
    ranked = [w for w, _ in Counter(toks).most_common()]
    lex = _conlang_lexicon(ranked, p, rng)
    return [lex[t] for t in toks]


def fam_cipher_of_conlang(n: int, h: float, seed: int = SEED) -> list:
    """Composed: relexify to a fixed-paradigm (0.5) conlang, then apply a length-
    preserving (1:1) homophonic substitution cipher at homophony h — each conlang
    letter maps to one cipher glyph, with a fraction h of conlang TYPES drawing
    from a 3-glyph homophone set per letter (same length, decoupled types)."""
    rng = random.Random(seed)
    conlang = fam_conlang_relex(n, 0.5, seed=seed)
    glyphs = "abcdefghiklmnoprstuvxyz0123456789"
    options = {c: rng.sample(glyphs, 3) for c in set("".join(conlang))}
    is_homo = {t: rng.random() < h for t in set(conlang)}
    det_cache: dict = {}
    out = []
    for t in conlang:
        if is_homo[t]:
            out.append("".join(rng.choice(options[c]) for c in t))
        else:
            if t not in det_cache:
                det_cache[t] = "".join(options[c][0] for c in t)
            out.append(det_cache[t])
    return out


def fam_abbrev_of_agglut(n: int, r: float, seed: int = SEED) -> list:
    """Composed: build agglutinative words (2-3 shared morphemes, deterministic
    per plaintext type), then abbreviate at rate r."""
    rng = random.Random(seed)
    toks = _vulgate_tokens(n)
    morphemes = [_rand_word(rng, 1) for _ in range(40)]
    forms: dict = {}
    for t in set(toks):
        k = 2 + (hash(t) % 2)
        forms[t] = "".join(morphemes[(hash(t + str(i)) % len(morphemes))]
                            for i in range(k))
    out = []
    for t in toks:
        w = forms[t]
        if len(w) > 4 and rng.random() < r:
            out.append(w[:3] if rng.random() < 0.5
                       else w[0] + "".join(c for c in w[1:-1] if c not in _VOWELS) + w[-1])
        else:
            out.append(w)
    return out


FAMILIES = {
    "verbose_cipher": (fam_verbose_cipher, GRID),
    "selfcitation": (fam_selfcitation, (1, 2, 3, 4, 5, 6)),
    "abjad_anagram": (fam_abjad_anagram, GRID),
    "abbreviation": (fam_abbreviation, GRID),
    "conlang_relex": (fam_conlang_relex, GRID),
    "cipher_of_conlang": (fam_cipher_of_conlang, GRID),
    "abbrev_of_agglut": (fam_abbrev_of_agglut, GRID),
}

# Pre-declared metric clusters (de-collinearity). One vote per cluster.
CLUSTERS = {
    "character_entropy": ["h1", "h2"],
    "lexical_richness": ["type_token_ratio", "mean_word_length"],
    "distributional": ["zipf_slope", "abbreviation_rho"],
    "morphology_network": ["ed1_main_component", "repetition_rate"],
    "positional": ["position_entropy"],
    "word_order": ["mz_peak_value", "mz_peak_scale"],
}


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _z_frame(profiles: dict) -> dict:
    """Per-metric (mean, sd) over the given profiles — the fixed reference frame."""
    frame = {}
    for m in METRICS:
        vals = [p[m] for p in profiles.values()]
        frame[m] = (statistics.mean(vals), statistics.stdev(vals) or 1.0)
    return frame


def _z(profile_dict: dict, frame: dict) -> dict:
    return {m: (profile_dict[m] - frame[m][0]) / frame[m][1] for m in METRICS}


def _clustered_distance(fam_p: dict, vms_p: dict, frame: dict,
                        clusters: dict = CLUSTERS) -> float:
    """Mean over clusters of the mean within-cluster |z_fam - z_vms|."""
    zf, zv = _z(fam_p, frame), _z(vms_p, frame)
    cluster_d = [statistics.mean(abs(zf[m] - zv[m]) for m in metrics)
                 for metrics in clusters.values() if metrics]
    return statistics.mean(cluster_d)


def _drop_metric(metric: str) -> dict:
    """CLUSTERS with one metric removed (empty clusters dropped) — for the
    collinearity ablation: selfcitation's copying mechanism drives BOTH
    repetition_rate and position_entropy (empirically ~0.80 correlated), so its
    lead may be a double-counted generator artifact. If dropping either metric
    collapses selfcitation's P(closest), the lead was the artifact."""
    out = {}
    for name, metrics in CLUSTERS.items():
        kept = [m for m in metrics if m != metric]
        if kept:
            out[name] = kept
    return out


def _block_boot(tokens: list, rng: random.Random) -> list:
    out = []
    n = len(tokens)
    while len(out) < n:
        start = rng.randrange(0, max(1, n - BLOCK))
        out.extend(tokens[start:start + BLOCK])
    return out[:n]


def _correlation_matrix(profiles: dict) -> dict:
    """Empirical |Pearson r| between metrics across corpora (audits CLUSTERS)."""
    zcols = {m: [(_z(p, _z_frame(profiles))[m]) for p in profiles.values()]
             for m in METRICS}
    out = {}
    for i, a in enumerate(METRICS):
        for b in METRICS[i + 1:]:
            xa, xb = zcols[a], zcols[b]
            ma, mb = statistics.mean(xa), statistics.mean(xb)
            cov = sum((x - ma) * (y - mb) for x, y in zip(xa, xb))
            da = math.sqrt(sum((x - ma) ** 2 for x in xa))
            db = math.sqrt(sum((y - mb) ** 2 for y in xb))
            if da and db:
                out[f"{a}~{b}"] = round(abs(cov / (da * db)), 3)
    return dict(sorted(out.items(), key=lambda kv: -kv[1])[:8])


def run() -> dict:
    vms = vms_stream()
    n = len(vms)
    half = n // 2
    vms_fit, vms_held = vms[:half], vms[half:]
    vp_fit, vp_held = profile(vms_fit), profile(vms_held)

    # 1. Build fit/held profiles for every (family, knob).
    fit_profiles: dict = {}
    held_profiles: dict = {}
    for fam, (gen, grid) in FAMILIES.items():
        for k in grid:
            stream = gen(n, k)
            s_fit, s_held = stream[:half], stream[half:]
            fit_profiles[(fam, k)] = profile(s_fit)
            held_profiles[(fam, k)] = profile(s_held)

    # 2. Fixed z-frame from the DEFAULT knob of each family + VMS (on the fit half).
    default_ps = {fam: fit_profiles[(fam, FAMILIES[fam][1][DEFAULT_IDX])]
                  for fam in FAMILIES}
    frame_profiles = {**default_ps, "vms": vp_fit}
    frame = _z_frame(frame_profiles)

    # 3. Tune each family on the FIT half; record the winning knob.
    tuned: dict = {}
    for fam, (gen, grid) in FAMILIES.items():
        dists = {k: _clustered_distance(fit_profiles[(fam, k)], vp_fit, frame)
                 for k in grid}
        best_k = min(dists, key=dists.get)
        tuned[fam] = {"knob": best_k,
                      "fit_distance": round(dists[best_k], 4),
                      "fit_distance_by_knob": {str(k): round(v, 4)
                                               for k, v in dists.items()}}

    # 4. Score the tuned knob on the HELD-OUT half.
    held_point = {fam: round(_clustered_distance(
        held_profiles[(fam, tuned[fam]["knob"])], vp_held, frame), 4)
        for fam in FAMILIES}
    ranking = sorted(held_point, key=held_point.get)

    # 5. Bootstrap the held-out clustered distance (block resample of held tokens).
    #    Same resampled profiles also feed the collinearity ablation (§7) at no
    #    extra profiling cost — only the distance is recomputed per cluster config.
    ablations = {"full": CLUSTERS,
                 "drop_repetition_rate": _drop_metric("repetition_rate"),
                 "drop_position_entropy": _drop_metric("position_entropy")}
    boot: dict = {fam: [] for fam in FAMILIES}
    win_counts = {fam: 0 for fam in FAMILIES}
    abl_wins = {cfg: {fam: 0 for fam in FAMILIES} for cfg in ablations}
    tuned_held_streams = {fam: FAMILIES[fam][0](n, tuned[fam]["knob"])[half:]
                          for fam in FAMILIES}
    for b in range(BOOTSTRAP):
        rng = random.Random(1000 + b)
        vboot = profile(_block_boot(vms_held, rng))
        rep = {}
        fps = {}
        for fam in FAMILIES:
            fp = profile(_block_boot(tuned_held_streams[fam], rng))
            fps[fam] = fp
            d = _clustered_distance(fp, vboot, frame)
            boot[fam].append(d)
            rep[fam] = d
        win_counts[min(rep, key=rep.get)] += 1
        for cfg, cl in ablations.items():
            dists = {fam: _clustered_distance(fps[fam], vboot, frame, cl)
                     for fam in FAMILIES}
            abl_wins[cfg][min(dists, key=dists.get)] += 1

    def ci(xs):
        s = sorted(xs)
        lo = s[int(0.025 * len(s))]
        hi = s[min(len(s) - 1, int(0.975 * len(s)))]
        return [round(lo, 4), round(hi, 4)]

    boot_summary = {fam: {"held_distance": held_point[fam],
                          "ci95": ci(boot[fam]),
                          "p_is_closest": round(win_counts[fam] / BOOTSTRAP, 3),
                          "point_in_ci": ci(boot[fam])[0] <= held_point[fam] <= ci(boot[fam])[1]}
                    for fam in ranking}
    # Sanity guard: if point estimates fall outside their bootstrap CIs, the
    # resampling is biased (e.g. block too short for the MZ scale) and the verdict
    # is not trustworthy — flag it rather than report a spurious ranking.
    boot_consistent = all(boot_summary[f]["point_in_ci"] for f in ranking)

    # Collinearity ablation summary: P(closest) per family under each config.
    ablation = {cfg: {fam: round(abl_wins[cfg][fam] / BOOTSTRAP, 3)
                      for fam in ranking}
                for cfg in ablations}
    # Does the modal bootstrap winner's lead depend on the doubly-counted
    # repetition_rate/position_entropy axis? (critic's decisive test)
    modal = max(ablation["full"], key=ablation["full"].get)
    modal_p = ablation["full"][modal]
    modal_collapses = any(ablation[cfg][modal] < modal_p * 0.5
                          for cfg in ("drop_repetition_rate", "drop_position_entropy"))

    winner = ranking[0]
    runner = ranking[1]
    ci_separated = boot_summary[winner]["ci95"][1] < boot_summary[runner]["ci95"][0]
    robust = boot_summary[winner]["p_is_closest"] >= 0.9 and ci_separated
    conlang_wins = winner == "conlang_relex" and robust

    results = {
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "experiment": "E5 — fair encoding bracket (equal tuning, held-out, "
                      "de-collinearised, composed, bootstrapped)",
        "seed": SEED,
        "tokens_total": n, "fit_tokens": half, "held_tokens": n - half,
        "bootstrap": BOOTSTRAP,
        "clusters": CLUSTERS,
        "top_metric_correlations_abs": _correlation_matrix(frame_profiles),
        "tuning": tuned,
        "held_out_ranking": ranking,
        "held_out": boot_summary,
        "winner": winner,
        "winner_robust": bool(robust),
        "winner_ci_separated_from_runner_up": bool(ci_separated),
        "bootstrap_consistent": bool(boot_consistent),
        "collinearity_ablation": ablation,
        "modal_winner": modal,
        "modal_winner_lead_collapses_under_ablation": bool(modal_collapses),
        "conlang_earns_B": bool(conlang_wins and boot_consistent),
    }
    results["grade"], results["verdict"] = _verdict(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "e5_encoding_fair.json").write_text(json.dumps(results, indent=2) + "\n")
    (REPORTS_DIR / "e5_encoding_fair.md").write_text(_render(results))
    return results


def _verdict(r: dict) -> tuple:
    w, ru = r["held_out_ranking"][0], r["held_out_ranking"][1]
    ho = r["held_out"]
    if not r["bootstrap_consistent"]:
        offenders = [f for f in r["held_out_ranking"] if not ho[f]["point_in_ci"]]
        return "D", (
            f"INCONCLUSIVE — bootstrap resampling is biased: point held-out "
            f"distances fall outside their 95% CIs for {offenders}, so the block "
            f"length still fails to preserve the scored structure and the ranking "
            f"cannot be trusted. Point ranking (unverified): "
            f"{' < '.join(r['held_out_ranking'])}. Do not grade until the resampling "
            f"is consistent.")
    if r["conlang_earns_B"]:
        return "B", (
            f"conlang_relex EARNS grade B: under equal tuning and de-collinearised, "
            f"held-out scoring it is robustly closest to the VMS (held distance "
            f"{ho[w]['held_distance']}, P(closest)={ho[w]['p_is_closest']}, CI "
            f"{ho[w]['ci95']} separated from runner-up {ru} {ho[ru]['ci95']}). The "
            f"i01 paradigmatic-conlang lead was NOT a tuning artifact — it survives "
            f"the fairness fixes. (Compatibility, not likelihood; still says nothing "
            f"about meaning.)")
    reason = (f"winner {w} is not conlang_relex" if w != "conlang_relex"
              else f"winner conlang_relex is not robust (P(closest)="
                   f"{ho[w]['p_is_closest']}, CI {ho[w]['ci95']} vs runner-up "
                   f"{ru} {ho[ru]['ci95']})")
    # Fold in the two refutation points: (i) name selfcitation's modal-win rather
    # than flatten it to "no winner"; (ii) report the collinearity ablation, which
    # tests whether that modal win is a double-counted generator artifact.
    modal = r["modal_winner"]
    abl = r["collinearity_ablation"]
    if r["modal_winner_lead_collapses_under_ablation"]:
        drop_metric = min(("repetition_rate", "position_entropy"),
                          key=lambda m: abl[f"drop_{m}"][modal])
        runner_up_after = max((f for f in abl[f"drop_{drop_metric}"] if f != modal),
                              key=lambda f: abl[f"drop_{drop_metric}"][f])
        modal_note = (
            f"That modal lead is an ARTIFACT of one doubly-counted metric: dropping "
            f"{drop_metric} alone (the axis {modal}'s copying mechanically inflates) "
            f"collapses its P(closest) from {abl['full'][modal]} to "
            f"{abl[f'drop_{drop_metric}'][modal]}, whereupon {runner_up_after} leads "
            f"({abl[f'drop_{drop_metric}'][runner_up_after]}). So even the weak modal "
            f"signal is single-metric-dependent and does not survive de-collinearisation.")
    else:
        modal_note = (
            f"{modal} is a WEAK modal winner (P(closest) {abl['full'][modal]}, "
            f"~{abl['full'][modal] / (1 / len(r['held_out_ranking'])):.1f}x chance) that "
            f"SURVIVES the collinearity ablation (P stays "
            f"{min(abl['drop_repetition_rate'][modal], abl['drop_position_entropy'][modal])} "
            f"when repetition_rate or position_entropy is dropped) — a real but "
            f"non-decisive lead worth an i03 follow-up, NOT a distinguished winner "
            f"(CIs overlap the field; a single scalar knob is not equal tuning POWER).")
    return "C", (
        f"i01 DOWNGRADE CONFIRMED: with equal tuning, held-out scoring, and "
        f"de-collinearised metrics, no family is robustly distinguished ({reason}). "
        f"Held-out ranking: {' < '.join(r['held_out_ranking'])}. {modal_note} The "
        f"encoding bracket is a DESCRIPTIVE compatibility ordering, not evidence for "
        f"any one family — the i01 'conlang best fit' claim does not survive fair "
        f"tuning and is withdrawn as a distinguishing result.")


def _render(r: dict) -> str:
    ho = r["held_out"]
    rows = [f"| {i + 1} | {fam} | {r['tuning'][fam]['knob']} "
            f"| {ho[fam]['held_distance']} | {ho[fam]['ci95']} "
            f"| {ho[fam]['p_is_closest']} |"
            for i, fam in enumerate(r["held_out_ranking"])]
    corr = "\n".join(f"- `{k}` |r|={v}" for k, v in
                     r["top_metric_correlations_abs"].items())
    return "\n".join([
        "# E5 — Fair Encoding Bracket",
        "",
        f"Generated {r['built_at']} at commit `{r['git_commit'][:10]}` by "
        "`python -m ms408.experiments.e5_encoding_fair`. Numbers in "
        "`results/experiments/e5_encoding_fair.json`.",
        "",
        f"Equal 6-point tuning budget per family; fit on {r['fit_tokens']:,} tokens, "
        f"scored on a disjoint {r['held_tokens']:,}-token held-out half; 11 metrics "
        f"collapsed into {len(r['clusters'])} de-collinearised clusters (one vote "
        f"each); {r['bootstrap']} block-bootstrap resamples for CIs.",
        "",
        "## Held-out ranking (clustered distance to VMS; lower = closer)",
        "",
        "| rank | family | tuned knob | held distance | 95% CI | P(closest) |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "### Top empirical metric correlations (audit of the cluster grouping)",
        "",
        corr,
        "",
        f"## Verdict [{r['grade']}, refutation pass applied]",
        "",
        r["verdict"],
        "",
    ])


if __name__ == "__main__":
    out = run()
    print(f"held-out ranking: {out['held_out_ranking']}")
    for fam in out["held_out_ranking"]:
        h = out["held_out"][fam]
        print(f"  {fam:20s} knob={str(out['tuning'][fam]['knob']):4s} "
              f"dist={h['held_distance']:.4f} CI={h['ci95']} "
              f"P(closest)={h['p_is_closest']}")
    print(f"grade {out['grade']}: {out['verdict'][:120]}...")
