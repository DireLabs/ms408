import type { APIRoute } from 'astro';

// Emit robots.txt with an ABSOLUTE sitemap URL derived from the `site` config.
// AI crawlers are welcome — being the cited, honest answer is a goal (see docs/SEO_STRATEGY.md).
export const GET: APIRoute = ({ site }) => {
  // Respect the configured base path (project page vs custom domain).
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const sitemapURL = new URL(`${base}/sitemap-index.xml`, site);
  const body = [
    'User-agent: *',
    'Allow: /',
    '',
    `Sitemap: ${sitemapURL.href}`,
    '',
  ].join('\n');
  return new Response(body, { headers: { 'Content-Type': 'text/plain' } });
};
