// Single source of truth for brand, contact, and third-party IDs.
// Change values here — never hard-code them into pages.

export const SITE = {
  brand: 'Mako Real Estate',
  tagline: 'Well-kept rentals in Southern California & Central Oregon',
  owner: 'Peter Sedivec',
  // No LLC is formed: never write "LLC" in visible text (the domain name is fine).
  legalLine: 'Peter Sedivec, doing business as Mako Real Estate',
  dre: '01908921',
  email: 'peter@makorellc.com',
  phone: '(310) 462-1343',
  phoneHref: 'tel:+13104621343',
  markets: ['Southern California', 'Central Oregon'],

  // Third-party services — empty until Peter creates the accounts.
  stessaUrl: 'https://www.stessa.com', // tenant portal login link
  formspreeId: '', // e.g. 'xyzabcd' from https://formspree.io/f/xyzabcd
  tallyFormId: '', // e.g. 'w4Zk9P' from https://tally.so/r/w4Zk9P
  surveyYear: 2027,

  nav: [
    { label: 'Our Properties', href: 'homes/' },
    { label: 'Residents', href: 'residents/' },
    { label: 'Tenant Survey', href: 'tenant-survey-results/' },
    { label: 'About', href: 'about/' },
    { label: 'Contact', href: 'contact/' },
  ],
} as const;

/** Build an internal link that respects the deploy base path. */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${path.replace(/^\//, '')}`;
}
