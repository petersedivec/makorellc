// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Served at the custom domain (public/CNAME), so no base path.
export default defineConfig({
  site: 'https://makorellc.com',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      // The annual survey page is for current residents only — keep it out of search.
      filter: (page) => !page.includes('/survey/'),
    }),
  ],
});
