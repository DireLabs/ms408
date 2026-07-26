import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Docs are synced from ../docs by scripts/sync-content.mjs (see package.json "sync").
const docs = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    order: z.number().default(99),
    audience: z.enum(['researcher', 'developer', 'both']).default('both'),
    source: z.string().optional(),
  }),
});

// Guided activities for the library/education portal — authored + committed (not synced).
const activities = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/activities' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    ages: z.string(),               // e.g. "8–12" or "all ages"
    duration: z.string(),           // e.g. "30–45 min"
    group: z.string().default('small group or solo'),
    materials: z.array(z.string()).default([]),
    objectives: z.array(z.string()).default([]),
    order: z.number().default(99),
    classroom_tested: z.boolean().default(false),
    contributor: z.string().default('MS408 project'),
  }),
});

export const collections = { docs, activities };
