# Security Policy

## Reporting a vulnerability

Please report security issues privately to **tim@mims.ms** rather than opening a public
issue. Include steps to reproduce and the affected version/commit. We aim to acknowledge
within a few days.

## Secrets

- **Never commit secrets.** API keys live only in a local, gitignored `.env` (see
  `.env.example`). The repository ships no keys, and `import ms408` makes no network calls —
  the core evaluator needs no credentials. Keys are required only at call time for the
  optional vision-annotation / cross-rater track (`ms408.annotate`, `e10`/`e12`/`e4b`).
- **If a key is ever exposed** (committed, pasted, or left in a directory that becomes
  public): rotate/revoke it immediately. Removing it from a later commit does not
  un-expose it.
- Build release artifacts (sdist/wheel/tarball) from a **clean checkout**, never from a
  working directory that may contain a `.env`.

## Scope

This is a research toolkit, not a networked service. The main practical risks are (1)
accidental credential disclosure and (2) trusting a number without its caveat — the
evaluator attaches per-axis hedges precisely to prevent the latter (see `docs/LIMITS.md`).
