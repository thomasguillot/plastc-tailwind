export interface Plan {
  name: string;
  monthly: string;
  yearly: string;
  blurb: string;
  features: string[];
  featured: boolean;
  cta: string;
}

export const PLANS: Plan[] = [
  { name: 'Solo', monthly: '0', yearly: '0', blurb: 'For your first few clients.', features: ['5 invoices a month', 'Card and bank payments', 'Automatic reminders'], featured: false, cta: 'Start free' },
  { name: 'Studio', monthly: '12', yearly: '120', blurb: 'For a small team that bills every week.', features: ['Up to 3 people', '200 invoices a month', 'Reminders and late fees', 'CSV export'], featured: true, cta: 'Start with Studio' },
  { name: 'Practice', monthly: '29', yearly: '290', blurb: 'For firms with many clients.', features: ['Unlimited people', 'Unlimited invoices', 'Your own domain for pay links', 'Priority support'], featured: false, cta: 'Start with Practice' },
];

export type Faq = [question: string, answer: string];

export const FAQS: Faq[] = [
  ['Do my customers need an account?', 'No. They get an email with a link to the invoice, and they can pay from there by card or bank transfer.'],
  ['Can I bring invoices from another tool?', 'Yes. Import a CSV export and your customers, invoices and their statuses come across together.'],
  ['What happens when I void an invoice?', 'The customer can no longer pay it and it leaves your outstanding total. It stays in your history, marked void.'],
  ['Can I change plans later?', 'Any time. Moving up takes effect at once; moving down takes effect at the end of the billing period.'],
];

export const PRICING_FAQS: Faq[] = [
  ['How does yearly billing work?', 'You pay for ten months and get twelve. The yearly price is charged once, at the start of your billing year.'],
  ['Is there a contract?', 'No. Plans renew each month, or each year on yearly billing. Cancel from Settings and your plan runs to the end of the period you paid for.'],
  ['What if I go over my invoice limit?', 'Nothing gets blocked. Invoices over the limit wait as drafts until the next month starts, or until you move up a plan.'],
  ...FAQS,
];

export type CompareValue = string | boolean;

export const PRICING_COMPARE: { group: string; rows: [label: string, ...values: CompareValue[]][] }[] = [
  {
    group: 'Invoicing',
    rows: [
      ['Invoices a month', '5', '200', 'Unlimited'],
      ['Pay links for card and bank transfer', true, true, true],
      ['Saved products and line items', true, true, true],
      ['Recurring invoices', false, true, true],
      ['Your own domain for pay links', false, false, true],
    ],
  },
  {
    group: 'Reminders',
    rows: [
      ['Automatic reminders', true, true, true],
      ['Pause when a customer replies', true, true, true],
      ['Late fees', false, true, true],
    ],
  },
  {
    group: 'Team',
    rows: [
      ['People', '1', 'Up to 3', 'Unlimited'],
      ['Owner, admin and member roles', false, true, true],
    ],
  },
  {
    group: 'Reports and data',
    rows: [
      ['Dashboard and reports', true, true, true],
      ['CSV export', false, true, true],
      ['API access', false, true, true],
    ],
  },
  {
    group: 'Support',
    rows: [
      ['Help center and email', true, true, true],
      ['Priority support, a reply within 4 hours', false, false, true],
    ],
  },
];

export const MKT_NAV = [
  { key: 'features', label: 'Features', href: 'landing.html#features' },
  { key: 'pricing', label: 'Pricing', href: 'pricing.html' },
  { key: 'blog', label: 'Blog', href: 'blog.html' },
  { key: 'about', label: 'About', href: 'about.html' },
  { key: 'contact', label: 'Contact', href: 'contact.html' },
];

export const FOOTER_NAV: { heading: string; links: { label: string; href: string; top?: boolean }[] }[] = [
  { heading: 'Product', links: [{ label: 'Features', href: 'landing.html#features' }, { label: 'Pricing', href: 'pricing.html' }, { label: 'Blog', href: 'blog.html' }] },
  { heading: 'Company', links: [{ label: 'About', href: 'about.html' }, { label: 'Careers', href: 'about.html#careers' }, { label: 'Contact', href: 'contact.html' }] },
  { heading: 'App', links: [{ label: 'Dashboard', href: 'dashboard.html' }, { label: 'Invoices', href: 'invoices.html' }, { label: 'Settings', href: 'settings.html' }] },
  { heading: 'Plastc', links: [{ label: 'The UI library', href: '../index.html', top: true }, { label: 'Source on GitHub', href: 'https://github.com/thomasguillot/plastc-tailwind', top: true }] },
];

export const LP_LOGOS = [
  { class: 'font-extrabold tracking-[-0.04em]', html: '<svg viewBox="0 0 20 20" class="inline-block w-[0.9em] h-[0.9em] mr-1.5 -mt-0.5 align-middle" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="currentColor"/></svg>Halden Studio' },
  { class: 'font-mono font-medium uppercase tracking-[0.06em] !text-[15px] md:!text-[16px]', html: 'Northwind Co-op' },
  { class: 'font-semibold uppercase tracking-[0.2em] !text-[14px] md:!text-[15px]', html: '<svg viewBox="0 0 20 20" class="inline-block w-[1.1em] h-[1.1em] mr-1.5 -mt-0.5 align-middle" aria-hidden="true"><path d="M10 2 18 17H2z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>Alder Robotics' },
  { class: 'font-normal tracking-[-0.02em]', html: 'Brightwater <b class="font-extrabold">Labs</b>' },
  { class: 'font-bold tracking-[-0.01em]', html: 'Ortiz <span class="font-normal">&amp;</span> Lane' },
  { class: 'font-mono font-semibold lowercase !text-[16px] md:!text-[17px]', html: 'kettle hill bakery' },
];

export const LP_STATS = [
  { label: 'Average time to get paid', value: '18 days', note: 'Down from 26 before reminders were on' },
  { label: 'Paid by the due date', value: '86%', note: 'Of invoices sent with a pay link' },
  { label: 'Paid through pay links', value: '$38M', note: 'By card and bank transfer last year' },
  { label: 'Studios invoicing', value: '4,200', note: 'From one person to forty' },
];

export const LP_QUOTES = [
  { initials: 'MO', name: 'Mira Okafor', role: 'Owner, Halden Studio', quote: 'We used to spend Friday afternoons chasing late invoices. Now the reminders go out on their own, and I only step in when a customer replies.' },
  { initials: 'IO', name: 'Ines Ortiz', role: 'Partner, Ortiz & Lane', quote: 'Most of our clients pay by card straight from the email. We stopped sending bank details by hand in the first week.' },
  { initials: 'RL', name: 'Rosa Lind', role: 'Owner, Kettle Hill Bakery', quote: 'I bill six cafés every Monday. With saved products, each invoice takes about as long as pouring a coffee.' },
];

export const ABOUT_VALUES = [
  { title: 'Say what is owed', text: 'An invoice states the amount, the date and how to pay. Nothing else competes with that for space.' },
  { title: 'Chase politely, and keep chasing', text: 'Reminders are firm and courteous, and they stop the moment a customer replies. Nobody should have to write an awkward email.' },
  { title: 'Keep the books honest', text: 'Totals match on every screen. A voided invoice stays in the history, marked void, and is never deleted.' },
  { title: 'Small and sturdy', text: 'We build for studios and practices of one to thirty people. We would rather do fewer things and have them work every time.' },
];

export const ABOUT_TEAM = [
  { name: 'Wren Castellan', role: 'Founder, product', initials: 'WC' },
  { name: 'Dov Aldana', role: 'Engineering lead', initials: 'DA' },
  { name: 'Ines Varga', role: 'Design', initials: 'IV' },
  { name: 'Hana Lindqvist', role: 'Payments engineering', initials: 'HL' },
  { name: 'Tobias Oyelaran', role: 'Head of support', initials: 'TO' },
  { name: 'Pilar Nwosu', role: 'Customer support', initials: 'PN' },
  { name: 'Emre Kovacs', role: 'Finance and operations', initials: 'EK' },
];

export const ABOUT_ROLES = [
  { title: 'Senior full-stack engineer', team: 'Engineering', location: 'Remote, UTC-3 to UTC+2', kind: 'Full time' },
  { title: 'Product designer', team: 'Design', location: 'Remote, UTC-8 to UTC+1', kind: 'Full time' },
  { title: 'Customer support specialist', team: 'Support', location: 'Portland, OR or remote', kind: 'Full time' },
  { title: 'Payments operations analyst', team: 'Finance', location: 'Remote, UTC-5 to UTC+1', kind: 'Part time' },
  { title: 'Technical writer', team: 'Docs', location: 'Remote', kind: 'Contract' },
];

export const CONTACT_TOPICS = [
  { value: 'support', title: 'Using Plastc', text: 'A question about an invoice, a reminder or a setting.' },
  { value: 'pricing', title: 'Pricing and plans', text: 'Which plan fits, or moving between plans.' },
  { value: 'careers', title: 'Careers', text: 'A role on the about page, or one that is not.' },
  { value: 'other', title: 'Something else', text: 'Press, partnerships, or anything we missed.' },
];
