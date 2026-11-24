import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const posts = defineCollection({
  loader: glob({ base: './src/content/posts', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    ledeNote: z.string().optional(),
    author: z.enum(['ines', 'tobias', 'hana']),
    category: z.enum(['product', 'guides', 'stories']),
    date: z.coerce.date(),
    readTime: z.number().int().positive(),
    slug: z.string(),
    visual: z.enum(['reply', 'terms', 'marlow', 'transfers', 'followup', 'varga', 'shortcuts']),
  }),
});

export const collections = { posts };
