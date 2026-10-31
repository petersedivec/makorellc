import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// One Markdown file per property in src/content/homes/. The body is the description.
// Deliberately no address field: the public site never shows street addresses.
const homes = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/homes' }),
  schema: ({ image }) => {
    const status = z.enum(['occupied', 'available']);
    return z.object({
      title: z.string(), // e.g. "Craftsman duplex near the beach"
      city: z.string(),
      state: z.enum(['CA', 'OR']),
      market: z.enum(['socal', 'bend']),
      type: z.string(), // "Single-family home", "Duplex", "Fourplex"…
      order: z.number(), // acquisition order, for stable sorting
      beds: z.number().optional(), // single-family homes; multi-family uses units[]
      baths: z.number().optional(),
      status: status.default('occupied'),
      zillowUrl: z.url().optional(),
      hero: image().optional(),
      gallery: z.array(image()).default([]),
      units: z
        .array(
          z.object({
            name: z.string(), // "Unit A", "Upstairs"
            beds: z.number(),
            baths: z.number(),
            description: z.string().optional(), // plain text; blank lines separate paragraphs
            status: status.default('occupied'),
            zillowUrl: z.url().optional(),
            photos: z.array(image()).default([]), // a few headline shots
          }),
        )
        .default([]),
    });
  },
});

export const collections = { homes };
