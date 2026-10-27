// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Preview lives at petersedivec.github.io/makorellc. At the domain cutover:
// set site to 'https://makorellc.com', delete `base`, and add public/CNAME.
export default defineConfig({
  site: 'https://petersedivec.github.io',
  base: '/makorellc',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      // The annual survey page is for current residents only — keep it out of search.
      filter: (page) => !page.includes('/survey/'),
    }),
  ],
});
