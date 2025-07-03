// src/content/config.ts
import { z, defineCollection } from 'astro:content';

// Define the schema for a book summary
const summariesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string(),
    category: z.string(),
    description: z.string(), // The new description field
  }),
});

// Export the collection
export const collections = {
  'summaries': summariesCollection,
};