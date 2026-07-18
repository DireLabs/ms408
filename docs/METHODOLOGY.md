# Methodology — how MS408 keeps itself honest

This project's transferable contribution is not a finding about the Voynich Manuscript.
It is a **discipline for making, and un-making, claims about an undeciphered corpus**,
built to resist the field's dominant failure mode: confident, mutually incompatible
"solutions" that are unfalsifiable because there is no ground truth. Four coupled
mechanisms. The first three are code; the fourth is a human-run protocol.

## 1. Harness (validate before you claim)

No method is trusted on the manuscript until it separates **known positives** (real
language) from **matched, structured-but-meaningless controls** and **ciphers**. The
controls are generators that reproduce surface structure without carrying meaning:
self-citation/auto-copying, positional/slot generators, type-lexicon reuse, and cipher
families (verbose, abjad, nomenclator, and the Naibbe-class verbose+homophonic cipher).
If a discriminator cannot tell real language from a meaningless generator on synthetic
data, it is not allowed to opine on the manuscript. See `ms408.harness` and the E-series
experiments.

## 2. Firewall (numbers come only from code)

Every reported number is produced by deterministic, versioned code writing a
machine-readable result; nothing is estimated, remembered, or hand-typed. The reference
bands the public evaluator checks against are themselves built by a script
(`ms408.experiments.e32_reference_bands`) that records its own git commit, parameters,
and input dataset into the shipped artifact. `ms408.evaluate()` refuses to run if that
artifact is missing rather than invent a band. The firewall applies to the tool exactly
as it applies to the research.

## 3. Evidence grading (every claim wears its strength)

Every claim carries a grade A–D. A is replicated/robust; D is speculative. The grade is
part of the claim — an ungraded assertion is treated as D. Grades are never raised to
make a paper stronger.

## 4. Adversarial refutation (an independent skeptic attacks every strong claim)

This is the distinctive mechanism, and the one most easily misrepresented, so read the
caveat.

**The protocol.** Before any A/B-grade claim stands, it is handed to an independent
reviewer given a **clean context** — the claim, the code, and the data, but *not* the
original analyst's narrative or sunk cost — and tasked to build the strongest possible
case *against* it. The reviewer's brief is preserved (`docs/refutations/`). If it lands,
the claim is downgraded, narrowed, or retracted, and the correction is versioned.

**This is a protocol, not a feature in this repository.** Grep the codebase for a
refuter and you will not find one: the refutation passes are run out-of-band with
fresh-context agents, and survive as the archived briefs. The self-correction record is
the demonstration that the protocol bites — it has overturned the program's *own*
conclusions repeatedly, including retracting a cipher-exclusion headline after running a
concurrently-published cipher (Greshko's Naibbe, 2025) through this very toolkit.

**Honest limits of the refuter (important).** The reviewer is *context*-independent but
not *model*- or *operator*-independent: it is a fresh-context agent of the same model
family, spawned by the same operator, over the same repository. It is a fallible language
model, not an oracle. Cross-vendor and human refutation remain the stronger checks where
stakes are high. Do not read "survived the refutation pass" as "true" — read it as "the
strongest same-family clean-context attack we could mount did not break it."

### Running the protocol yourself

1. Freeze the claim and the exact code/results that produce its numbers.
2. Open a fresh context (new agent session, ideally a different model/vendor, or a human).
   Give it the claim, the code, and the data — withhold your narrative and your priors.
3. Instruct it to *refute*: find the confound, the leakage, the circularity, the
   fabricated or recalled number, the over-general wording. Default to skepticism.
4. If it lands a hit, downgrade/narrow/retract and version the correction. Preserve the
   brief so the "the refuter caught it" attribution is dereferenceable, not operator
   summary.
5. Repeat until an honest attack finds nothing new — then the claim stands *at its
   grade*, with the caveats the pass surfaced attached.

See `docs/refutations/README.md` for the archived briefs and their independence caveat,
and `docs/LIMITS.md` for what the statistics can and cannot support.
