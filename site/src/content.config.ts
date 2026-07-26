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

export const collections = { docs };
