// Copy curated repo docs into src/content/docs/ with frontmatter, and rewrite cross-file
// links so the site stays a single source of truth with docs/. Runs on every build.
import { mkdirSync, rmSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, '..', '..');          // repo root
const OUT = resolve(__dirname, '..', 'src', 'content', 'docs');
const BASE = (process.env.SITE_BASE || '/').replace(/\/$/, '');
const REPO_URL = process.env.REPO_URL || 'https://github.com/direlabs/ms408';

// Curated set: which repo docs become site pages, in order, with metadata.
const DOCS = [
  { src: 'docs/TUTORIAL.md',    slug: 'tutorial',     title: 'Tutorial',     order: 1,
    audience: 'researcher', desc: 'Evaluate a hypothesis, end to end.' },
  { src: 'docs/LIMITS.md',      slug: 'limits',       title: 'Limits',       order: 2,
    audience: 'both',       desc: 'Read before quoting any number.' },
  { src: 'docs/METHODOLOGY.md', slug: 'methodology',  title: 'Methodology',  order: 3,
    audience: 'both',       desc: 'Harness, firewall, grading, refutation.' },
  { src: 'docs/GLOSSARY.md',    slug: 'glossary',     title: 'Glossary',     order: 4,
    audience: 'both',       desc: 'Domain + technical terms.' },
  { src: 'CONTRIBUTING.md',     slug: 'contributing', title: 'Contributing', order: 5,
    audience: 'developer',  desc: 'The discipline as contribution rules.' },
];

// basename(lowercase, no .md) -> site path, for rewriting intra-repo .md links.
const toSite = new Map(DOCS.map((d) => [d.src.split('/').pop().toLowerCase().replace(/\.md$/, ''),
  `${BASE}/docs/${d.slug}`]));
toSite.set('readme', `${BASE}/`);

function rewriteLinks(md) {
  // [text](target) where target ends in .md (with optional ./ ../ dir/ prefix and #anchor)
  return md.replace(/\]\(([^)]+?\.md)(#[^)]*)?\)/g, (whole, target, anchor = '') => {
    if (/^https?:\/\//.test(target)) return whole;                 // external, leave
    const base = target.split('/').pop().toLowerCase().replace(/\.md$/, '');
    if (toSite.has(base)) return `](${toSite.get(base)}${anchor})`; // included doc -> site route
    const clean = target.replace(/^(\.\.\/)+/, '').replace(/^\.\//, '');
    return `](${REPO_URL}/blob/main/${clean}${anchor})`;           // else -> GitHub source
  });
}

function stripLeadingH1(md) {
  return md.replace(/^\s*#\s+.*\n+/, ''); // drop the first H1 (title comes from frontmatter)
}

function esc(s) { return s.replace(/"/g, '\\"'); }

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

for (const d of DOCS) {
  const raw = readFileSync(resolve(REPO, d.src), 'utf8');
  const body = rewriteLinks(stripLeadingH1(raw));
  const fm = [
    '---',
    `title: "${esc(d.title)}"`,
    `description: "${esc(d.desc)}"`,
    `order: ${d.order}`,
    `audience: "${d.audience}"`,
    `source: "${d.src}"`,
    '---',
    '',
  ].join('\n');
  writeFileSync(resolve(OUT, `${d.slug}.md`), fm + body);
  console.log(`synced ${d.src} -> src/content/docs/${d.slug}.md`);
}
console.log(`Done: ${DOCS.length} docs (BASE=${BASE}).`);
