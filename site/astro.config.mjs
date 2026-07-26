// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages config. For a PROJECT site (owner.github.io/ms408) keep base '/ms408'.
// For a user/org site or a custom domain, set SITE_BASE=/ and SITE_URL accordingly.
// The deploy Action sets SITE_URL/SITE_BASE from repo settings.
const site = process.env.SITE_URL || 'https://OWNER.github.io';
const base = process.env.SITE_BASE || '/ms408';

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
  markdown: {
    shikiConfig: { theme: 'github-light' },
  },
});
