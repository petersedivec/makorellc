# Mako Real Estate: makorellc.com

Marketing site for **Mako Real Estate**, Peter Sedivec's owner-operated rental business: 6 homes in SoCal (Long Beach, San Clemente, San Juan Capistrano, San Diego) and Bend, OR. Astro static site, deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

## Commands
- `npm run dev`: dev server (see AGENTS.md: `astro dev --background` / `astro dev stop`)
- `npm run build`: must pass before committing; the content schema rejects bad home data
- `npm run preview`: serves `dist/` at `http://localhost:4321/makorellc/`

## Hard rules
- **Never write "LLC" in visible text.** No LLC is formed; Peter is a sole proprietor doing business as "Mako Real Estate". The domain `makorellc.com` is fine. Brand, legal line, DRE number and contact info live in `src/site.config.ts`. Never hard-code them in pages.
- **No street addresses anywhere.** Homes show city + type + beds/baths only. The `homes` schema (`src/content.config.ts`) deliberately has no address field. Slugs must not contain street names.
- **Survey privacy:** the public results page shows only portfolio-wide aggregates. Never show per-property or per-city breakdowns (several cities have a single respondent), property-specific issues or action items, or anything that identifies a tenant. Quotes are unattributed, with tenant names removed.
- **Strip photo metadata before committing.** Source images in `src/assets/` are public in this repo. Re-save with PIL so no EXIF/GPS survives (verify with `Image.open(p).getexif()` being empty). Raw downloads go in `raw/` (gitignored).
- Every page includes the footer DRE number and the Equal Housing Opportunity statement (via `src/layouts/Base.astro`).
- **Don't `git push` unless Peter explicitly asks.** Commit locally; he reviews and pushes.

## Base path
Preview deploys to `petersedivec.github.io/makorellc`, so `astro.config.mjs` sets `base: '/makorellc'`. Build every internal link with `url()` from `src/site.config.ts`, never a bare `/path`. At the domain cutover, set `site: 'https://makorellc.com'`, delete `base`, and add `public/CNAME` containing `makorellc.com`.

DNS is at GoDaddy. Google Workspace email uses the domain's **MX/TXT records: never touch them.** The cutover only changes the apex `A` records (to GitHub's 185.199.108–111.153) and the `www` CNAME (to `petersedivec.github.io`).

## Content
- **Add or edit a home:** `src/content/homes/<slug>.md`; frontmatter per the schema. Multi-family homes list `units[]`, each with a few headline `photos`.
- Source photos come from Peter's Google Drive: root folders `NN. <street>` (acquisition order) → `Listing Photos/`.
- Survey data: past results are in Drive (`Tenant Satisfaction Survey - YYYY (Responses)` sheets, `YYYY Tenant Survey Feedback/Results` docs) and Sent mail ("Tenant Survey"). Future surveys run on Tally (`SITE.tallyFormId`), embedded at `/survey/` (noindex, excluded from the sitemap).
- Peter's local photo drop is `raw/<street>/<unit or area>/`, with his pick for each named `Hero.*`. Street→slug: Linden=long-beach, Escalones=san-clemente, Calle Delphina=san-juan-capistrano, Robinson=san-diego, Longfellow=bend-home, Vail=bend-townhome.
- **Blur house numbers and license plates** on exterior shots (Gaussian blur over the region) and check at full size before committing. Skip photos showing tenants' belongings, kids' names, or family photos.
- External IDs pending Peter's signups: `formspreeId`, `tallyFormId` in `src/site.config.ts`. The components fall back to email/phone until set. `stessaUrl` is the generic `https://www.stessa.com` login.
- Contact info (email/phone) appears on the Contact and Residents pages, not in the footer (Peter's call).
- **Descriptions:** came from the Drive doc "Property Listing Descriptions — Final"; the site has since moved ahead of it (Long Beach Units 3/4 parking, San Clemente Unit 1 bathroom year 2026), so the `.md` files are now the source of truth. Property text is the home's Markdown body; unit text is `units[].description`. Keep out move-in dates, deposits, fee amounts and tenant details; avoid wording that signals a preference about children/familial status (fair housing).

## Status (end of 2026-10-31)
Done: skeleton, all pages, survey results (2024 + 2026 from full response CSVs), unit lists, photos for all 6 properties (Peter's Hero picks plus a few headline shots per unit; house numbers/plates blurred), property + unit descriptions, Bend beds/baths (both 3 / 2.5). Contact page split into renting / investment deals. Nothing pushed; Pages not enabled yet.

Open items waiting on Peter:
- San Clemente Unit 1 still uses the earlier Drive photos (no Unit 1 folder in `raw/`).
- Confirm "You said, we did" items in `src/data/survey.json` (`confirmed: true` + `did`).
- Formspree + Tally signups, About copy review, design feedback.
- Then: push, enable Pages (Source: GitHub Actions), review, and run the DNS cutover.
