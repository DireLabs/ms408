// Central site config. Override REPO_URL at build via PUBLIC_REPO_URL.
export const REPO_URL = import.meta.env.PUBLIC_REPO_URL || 'https://github.com/DireLabs/ms408';
export const SITE_TITLE = 'MS408';
export const SITE_TAGLINE = 'An honest, reproducible toolkit and shared benchmark for Voynich-Manuscript research';
export const PYPI_URL = 'https://pypi.org/project/ms408/';
// Fill after the first Zenodo release mints the concept DOI (e.g. '10.5281/zenodo.XXXXXXX').
// Set here or via PUBLIC_SOFTWARE_DOI at build; the Cite page + badge light up automatically.
export const SOFTWARE_DOI = import.meta.env.PUBLIC_SOFTWARE_DOI || '';

// Join the configured base path with a route (handles the trailing slash).
export function href(path = '') {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${path}`.replace(/\/{2,}/g, '/');
}
