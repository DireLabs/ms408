# Deploying the site (GitHub Pages + custom domain)

The site (`site/`) deploys to **https://ms408.direlabs.com** via the `pages.yml` GitHub Action.
One-time setup:

## 1. Enable Pages
Repo → **Settings → Pages → Build and deployment → Source: `GitHub Actions`** (not "Deploy from
a branch"). Ignore the branch/folder controls — those are only for the branch method.

## 2. DNS (subdomain → CNAME)
`ms408.direlabs.com` is a **subdomain**, so add a single **CNAME** record at whatever manages
`direlabs.com`'s DNS. (Subdomains use CNAME; only an apex/root domain uses A/ALIAS records.)

| Type | Host / Name | Value / Target | TTL |
|---|---|---|---|
| `CNAME` | `ms408` (or full `ms408.direlabs.com`) | `direlabs.github.io` | default |

The target is the **org's** github.io host — `direlabs.github.io`, **not** `direlabs.github.io/ms408`.
GitHub routes it to the `ms408` repo via the custom domain (below) + the shipped
`site/public/CNAME` file (`ms408.direlabs.com`).

## 3. Set the custom domain + HTTPS
Repo → **Settings → Pages → Custom domain** → `ms408.direlabs.com` → **Save**. GitHub runs a DNS
check (may show "pending" until DNS propagates — minutes to a few hours). Once verified, tick
**Enforce HTTPS** (Let's Encrypt cert auto-provisions; a few minutes up to ~24h).

## Gotchas
- **Cloudflare:** set the CNAME to **DNS only (grey cloud)** until GitHub issues the cert; a
  proxied (orange-cloud) record can block HTTPS provisioning. Re-enable proxy later with SSL
  mode **Full**.
- **CAA records:** if `direlabs.com` has any, they must permit `letsencrypt.org`.
- Don't keep a conflicting A/AAAA/other record for `ms408.direlabs.com` alongside the CNAME.

## Verify
```bash
dig +short ms408.direlabs.com        # -> direlabs.github.io, then GitHub Pages IPs
curl -I https://ms408.direlabs.com   # -> 200 once live + HTTPS
```

## If you'd rather use the project sub-path (no custom domain)
Serve at `direlabs.github.io/ms408` instead: set `SITE_BASE=/ms408` (the CI Action derives this
from Pages settings automatically), delete `site/public/CNAME`, and change the `astro.config.mjs`
local default `base` back to `'/ms408'`. Custom domain is recommended (cleaner canonical URLs +
SEO — see `docs/SEO_STRATEGY.md`).
