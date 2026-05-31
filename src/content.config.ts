import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const docSchema = z.object({
  title: z.string(),
  description: z.string().optional(),
  order: z.number(),
  status: z.enum(['stable', 'wip', 'draft']).default('stable'),
});

// Strip extension (.md / .mdx) and numeric prefix so 03-glossaire.md → id "glossaire"
const cleanId = ({ entry }: { entry: string }) =>
  entry.replace(/\.mdx?$/, '').replace(/^\d+-/, '');

const regles = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/regles', generateId: cleanId }),
  schema: docSchema,
});

const conseilsMj = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/conseils-mj', generateId: cleanId }),
  schema: docSchema,
});

const extensions = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/extensions', generateId: cleanId }),
  schema: docSchema,
});

const ressources = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/ressources', generateId: cleanId }),
  schema: docSchema,
});

export const collections = { regles, 'conseils-mj': conseilsMj, extensions, ressources };
