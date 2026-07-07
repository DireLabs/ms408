# i02 — Experiment Agenda

Five experiments from the T3.3 critique log (`../../synthesis/T33-critique-log.md`).
Each names the open question, the design, and the pass/fail criterion. All are
pure-code on data in hand unless marked. Priority: E1 first (it settles the
central meaningful-vs-meaningless question).

---

## E1 — Blind adversarial null: is MZ word-order information a meaning detector? [P1]

**Open question (C5).** i01's "meaning-bearing / not a hoax" lean rested on the
VMS scoring MZ ΔI ≈ 0.31 while the team's self-citation null scored lower — but
that null was self-built and self-tuned, and MZ is a topic-clustering statistic,
not a meaning detector.

**Design.** Build a parameterized *structured-meaningless* generator (self-citation
+ tunable vocabulary-drift / source-locality / section structure — no plaintext,
no meaning). Optimize its parameters to **maximize ΔI subject to matching VMS h2
and both Zipf slopes**, blind to the VMS ΔI value (objective = maximize ΔI, not
"hit 0.31"). Report the achievable ΔI ceiling. Also bootstrap the VMS ΔI to a CI
at VMS length.

**Pass/fail.**
- If an adversarially-optimized meaningless generator **reaches or exceeds** VMS
  ΔI while matching h2 + Zipf → MZ does not discriminate meaning; the i01 lean is
  **dead**, and "meaningful vs meaningless" stays open on other grounds.
- If the meaningless ceiling **falls short** of the VMS ΔI CI by a clear margin →
  the lean is **supported** (candidate B, pending refutation pass).

---

## E2 — De-confound the word-order signal [P1]

**Open question (C2).** The VMS ΔI = 0.31 was measured on analyst-*reordered*-by-
section text, whose sections coincide with A/B + quire drift — so it may index
scribe/dialect blocking, not plaintext word-order.

**Design.** (a) Recompute ΔI on the VMS in **natural folio order** (no reordering);
compare to the reordered value. (b) Build a **scribe-switching / drifting-key**
verbose cipher of a topically heterogeneous Latin text, blocked into "sections"
the same way the VMS was, and measure its ΔI. (c) Report ΔI of the exact Pliny
plaintext used for the H2 cipher.

**Pass/fail.** The word-order argument SURVIVES only if natural-order VMS stays
high AND the block-structured switching cipher stays low. If natural-order VMS
collapses toward the cipher, or the switching cipher reaches VMS levels, the
argument is **refuted** and ΔI is a blocking artifact.

---

## E3 — Anchor-hunt power curve [P2]

**Open question (C4).** The three anchor nulls may be underpowered false negatives;
the planted control (φ=1.0) proved only that a perfect signal is findable.

**Design.** Inject synthetic anchors at φ = 0.3 / 0.4 / 0.5 on realistic page
counts into the herbal token×feature data; report recovery rate and the minimum
detectable effect at BH-FDR q=0.05. Re-run the anchor hunt (a) restricted to
mid-prevalence features and (b) at line/label-adjacency granularity rather than
whole-page.

**Pass/fail.** If moderate anchors (φ≈0.4) are recoverable at realistic page
counts and the finer-granularity re-run is still null → the "no strong anchor"
claim **strengthens** toward "no anchor." If the power curve shows moderate anchors
are undetectable → the null is **downgraded to uninformative** (power too low to
conclude anything).

---

## E4 — root↔leaf: masked positive or real null? [P2]

**Open question (C4).** 35% root_type noise attenuates the association; the clean
root_coloring feature *did* associate with leaf features.

**Design (pure-code now).** Report root_type × leaf_shape disattenuated for the
measured inter-annotator reliability; follow the root_coloring → leaf_shape /
leaf_arrangement association fully with permutation tests. **Optional (small API
spend, needs Tim's OK):** a third independent annotator pass on root_type only, to
adjudicate and reduce noise.

**Pass/fail.** If disattenuated root×leaf and the clean root_coloring→leaf hits are
significant → the i01 "no real-taxa bundle" claim is **overturned** (a bundle
exists, masked by noise). If both stay null after disattenuation → the null
**stands** on firmer ground.

---

## E5 — Encoding bracket, fair [P3]

**Open question (C1).** The paradigmatic-conlang "win" was circular (VMS-informed
template); the z-metric double-counts collinear dimensions; composed encodings
were never tested.

**Design.** Give **all** families the same VMS-informed tuning budget on a
*held-out* metric split (fit on half, score on half). Add composed families
(cipher∘conlang, abbreviation∘agglutinative). Cluster collinear metrics before
computing distances; bootstrap the z-distances with CIs.

**Pass/fail.** If the conlang still wins on held-out metrics with equal tuning and
de-duplicated dimensions → the "conlang best fit" claim **earns** grade B. If the
gap closes → confirm the i01 downgrade (no family distinguished; bracket is
descriptive only).
