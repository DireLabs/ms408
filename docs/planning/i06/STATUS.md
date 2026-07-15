# STATUS.md — i06 Coordination Bus

_Last updated: 2026-07-15 (spec drafted; building E19 joint-signature test)._

**Inherits:** all locks L1–L37; standing refutation rule; firewall (L3); null-
correction framework (i05); **L7 absolute** (no decipherment without an independent
anchor). Continues the experiment ledger as E19–E20 (E18 = completeness known-issue).

## Experiments

| id | probe | priority | state | verdict |
|---|---|---|---|---|
| E19 | Joint-signature test with mid-level syntax | P1 gating | ✅ done + refuted → **VMS not a cipher of real prose [B]** | Adds i05 mid-level syntax to the encoding signature. No cipher of a real language matches the VMS's low-h2 + weak-syntax combination; order-preserving ciphers (abjad, 1:1 substitution, nomenclator) retain strong syntax the VMS lacks (~10σ on fc_z/wc_z). Refutation narrowed it: the NEGATIVE is grade B; the "favours generation" positive was CIRCULAR (self-citation is the Voynich-tuned Timm–Schinner generator) → dropped. |
| E19b | Language-universality control (refutation-demanded) | P1 | ✅ done → **exclusion is UNIVERSAL [B]** | fc_z/wc_z across Romance (Latin/Italian), Germanic (German), Semitic/consonantal (Hebrew) + an order-scramble cipher. NO real language is weak — Hebrew (a native abjad) has fc_z 9.7 / wc_z 4.1, far above VMS — so the E19 exclusion is not Latin-specific and directly answers the abjad revival. REFINEMENT: an order-SCRAMBLING (transposition) cipher IS weak (fc_z 2.2, wc_z 1.1) → the only surviving cipher lead, but in tension with the VMS retaining ΔI (a transposition would destroy it). |
| E20 | Constrained cryptanalytic attack (conditional) | P2 | ⬜ **target largely collapsed** | E19/E19b exclude order-preserving ciphers of real prose universally; the surviving cipher lead (weak-transposition) is self-conflicting (VMS retains ΔI). A decipherment attack is low-yield; E20 would be a redirected *generative* characterisation, or deferred. |

## Working hypothesis (from the i05 preview)

Word-order-preserving ciphers of a real language (abjad, deterministic-verbose,
nomenclator) inherit the source language's STRONG word-syntax (abjad of Latin: word-
class z≈11, function/content z≈14), but the VMS has WEAK word-syntax (z≈2 / ≈−4). So
E19 likely DISFAVOURS the VMS as a syntax-preserving cipher of real prose and redirects
the decipherment question toward non-syntax-preserving / generative mechanisms. E19
tests this rigorously before any attack effort (E20).

## Sessions

- **Code session (i06)** — spec drafted 2026-07-15; building E19.
