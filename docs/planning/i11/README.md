# i11 — Engaging the concurrent literature (Naibbe, Parisel)

**Inherits** all locks L1–L37; the standing refutation rule; firewall (L3); harness (L4);
L7 absolute; A/B + hand stratification (L8); **consume-only external data (L19)**. Continues
the ledger as **E29–**.

## Why

An external value/novelty review (2026-07-17) surfaced two concurrent works our program had
not engaged, both directly relevant to the i06 cipher analysis:

- **Naibbe (Greshko, *Cryptologia* 2025)** — a hand-constructable, 15th-c.-plausible,
  *decipherable* homophonic substitution cipher that encrypts respaced Latin/Italian into
  Voynichese-like ciphertext and "reproduces many statistical properties of the VMS at once"
  (author concedes replication is *incomplete*, esp. Voynich B). Public code + ciphertext at
  `github.com/greshko/naibbe-cipher`. This is a **constructive existence proof** of a
  Voynich-matching cipher of real prose — the strongest possible adversary to our i06
  "cipher-of-real-prose excluded" claim.
- **Parisel (arXiv:2604.19762, 2026)** — an independent joint multi-signature analysis
  (slot generator + Cardan grille, calibrated per Currier A/B) concluding no single generator
  class reproduces all signatures — methodologically adjacent to our E21/E22 and partially
  pre-dating our v5b.

The review's verdict: our one novel-ish result (the i06 joint-signature exclusion) is
soft-by-our-own-admission, partly scooped (Parisel), and contested (Naibbe), and we cite
neither. Non-optional to fix. The make-or-break experiment: **run Naibbe's actual ciphertext
through our discriminators.**

## The test (E29) and its stakes

Our i06 prediction: no cipher of real prose reproduces the VMS's *joint* signature — low h₂
+ **retained (block-scale) ΔI** + weak word-syntax — because retained-ΔI and weak-syntax are
mutually exclusive under any cipher (order-preserving keeps ΔI but strong syntax;
homophonic/transposition gives weak syntax but destroys ΔI). Naibbe is homophonic, so we
**predict** it gives weak syntax but collapses ΔI, and thus fails to reproduce the VMS's
retained ΔI.

- If Naibbe **fails** our joint signature → the i06 exclusion is confirmed against a real
  constructive counterexample (a strong, novel, defensible result; enters the live debate).
- If Naibbe **passes** (low h₂ + retained ΔI + weak syntax together) → the i06 exclusion is
  falsified, and we learn it before a referee does — exactly what the method demands.

L19: Naibbe's code/ciphertext are consumed from `data/raw/` (gitignored, not redistributed);
only derived statistics are written to `results/`. L7: no decipherment/meaning claim — this
is a statistical discriminator test.

## Open decisions (D-items)

- **i11-a — cite/engage in the papers.** Add Naibbe + Parisel to FLAGSHIP and the preprints as
  concurrent work (non-optional per the review); reframe the i06 headline around "a
  discriminator battery that candidate generators must pass."
- **i11-b — harden the soft mid-level measures** (fc_z/wc_z proper nulls/CIs, deconfound from
  sectional drift) — the review's second required fix. Note: if E29 shows the exclusion is
  carried by the (non-soft) ΔI axis, this de-risks the soft-measure concern for the cipher case.
