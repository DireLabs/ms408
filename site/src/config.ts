// Central site config. Override REPO_URL at build via PUBLIC_REPO_URL.
export const REPO_URL = import.meta.env.PUBLIC_REPO_URL || 'https://github.com/OWNER/ms408';
export const SITE_TITLE = 'MS408';
export const SITE_TAGLINE = 'A cold, reproducible evaluator for Voynich-Manuscript hypotheses';

// Join the configured base path with a route (handles the trailing slash).
export function href(path = '') {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${path}`.replace(/\/{2,}/g, '/');
}
