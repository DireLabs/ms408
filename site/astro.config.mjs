// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Deploys to the custom domain ms408.direlabs.com (see site/public/CNAME) at the root.
// The deploy Action overrides SITE_URL/SITE_BASE from Pages settings; these are the local
// defaults (base '/' for a custom domain — set SITE_BASE=/reponame for a project sub-path).
const site = process.env.SITE_URL || 'https://ms408.direlabs.com';
const base = process.env.SITE_BASE || '/';

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
  integrations: [
    // Exclude the hidden /balneo easter egg from the sitemap.
    sitemap({ filter: (page) => !page.includes('/balneo') }),
  ],
  markdown: {
    shikiConfig: { theme: 'github-light' },
  },
});
