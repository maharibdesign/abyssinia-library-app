// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const summariesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string(),
    category: z.string(),
    description: z.string(),
    pdfUrl: z.string(), // The new field for the PDF link
  }),
});

export const collections = {
  'summaries': summariesCollection,
};