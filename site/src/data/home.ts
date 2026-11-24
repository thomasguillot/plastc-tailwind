export const HOME_DESCRIPTION =
  'Plastc is a neumorphic UI library for Tailwind CSS v4. Real product screens composed from one CSS file, with light and dark themes and contrast checked against WCAG 2 and APCA.';

export interface WallTile {
  key: string;
  title: string;
  eager?: boolean;
}
export interface WallRow {
  dx: number;
  dy: number;
  tiles: WallTile[];
}

export const WALL_LABEL = 'A wall of 24 tiles showing 20 Plastc screens: the sample invoicing app, its marketing site and its blog.';

export const WALL: WallRow[] = [
  {
    dx: -210,
    dy: 0,
    tiles: [
      { key: 'pricing', title: 'Pricing' },
      { key: 'post-studio-varga', title: 'Blog post: studio varga' },
      { key: 'invoices', title: 'Invoices' },
      { key: 'about', title: 'About' },
      { key: 'post-payment-terms', title: 'Blog post: payment terms' },
      { key: 'settings', title: 'Settings' },
    ],
  },
  {
    dx: 150,
    dy: 0,
    tiles: [
      { key: 'blog', title: 'Blog' },
      { key: 'customers', title: 'Customers', eager: true },
      { key: 'dashboard', title: 'Dashboard', eager: true },
      { key: 'contact', title: 'Contact', eager: true },
      { key: 'post-marlow-print-co', title: 'Blog post: marlow print co', eager: true },
      { key: 'landing', title: 'Landing' },
    ],
  },
  {
    dx: -120,
    dy: 0,
    tiles: [
      { key: 'post-keyboard-shortcuts', title: 'Blog post: keyboard shortcuts' },
      { key: 'sign-in', title: 'Sign in', eager: true },
      { key: 'products', title: 'Products', eager: true },
      { key: 'article', title: 'Article', eager: true },
      { key: 'reports', title: 'Reports', eager: true },
      { key: '404', title: '404 page' },
    ],
  },
  {
    dx: 180,
    dy: 0,
    tiles: [
      { key: 'landing', title: 'Landing' },
      { key: 'post-overdue-follow-up', title: 'Blog post: overdue follow up' },
      { key: 'settings', title: 'Settings' },
      { key: 'post-bank-transfer-matching', title: 'Blog post: bank transfer matching' },
      { key: 'customers', title: 'Customers' },
      { key: 'invoices', title: 'Invoices' },
    ],
  },
];

export interface Layer {
  key: string;
  name: string;
  description: string;
  classes: string[];
  link: { label: string; href: string };
}

export const LAYERS: Layer[] = [
  { key: '1', name: 'Base', description: 'The page surface, seams and sidebar frame.', classes: ['[data-theme]', '.seam'], link: { label: 'Surfaces', href: '/components/surfaces/' } },
  { key: '2', name: 'Planes', description: 'Cards, charts and tables. Flat, no shadow.', classes: ['.panel', '.ktable', '.chart'], link: { label: 'Data', href: '/components/data/' } },
  { key: '3', name: 'Raised', description: 'Anything you press.', classes: ['.btn', '.key', '.seg'], link: { label: 'Buttons', href: '/components/buttons/' } },
  { key: '4', name: 'Recessed', description: "Where you type, and the page you're on.", classes: ['.field', '.input-group', '.nav-item'], link: { label: 'Fields', href: '/components/fields/' } },
  { key: '5', name: 'LCD', description: 'Readouts for key figures and levels.', classes: ['.lcd', '.stat', '.meter'], link: { label: 'Status', href: '/components/status/' } },
  { key: '6', name: 'Float', description: 'Menus and toasts, above everything else.', classes: ['.menu', '.toast'], link: { label: 'Overlays', href: '/components/overlays/' } },
];

export const layerNumber = (key: string) => key.padStart(2, '0');

export type TintName = 'green' | 'amber' | 'blue';
type Triple = [lcd: string, ink: string, dim: string];
export interface Tint {
  name: TintName;
  label: string;
  chip: { bg: string; fg: string };
  light: Triple;
  dark: Triple;
}

export const TINTS: Tint[] = [
  { name: 'green', label: 'Green', chip: { bg: '#bcc4ab', fg: '#1b2416' }, light: ['#bcc4ab', '#1b2416', '#2e3727'], dark: ['#1f281a', '#c8e2a4', '#b3ca97'] },
  { name: 'amber', label: 'Amber', chip: { bg: '#d9c58a', fg: '#2b1e05' }, light: ['#d9c58a', '#2b1e05', '#47340c'], dark: ['#2b2112', '#f2d08a', '#d9b872'] },
  { name: 'blue', label: 'Blue', chip: { bg: '#b5c7d6', fg: '#0e2030' }, light: ['#b5c7d6', '#0e2030', '#223b52'], dark: ['#16232f', '#a8d3f4', '#92bddf'] },
];

export const DEPTHS = [
  { value: '0.5', label: 'Soft' },
  { value: '1', label: 'Normal' },
  { value: '1.7', label: 'Deep' },
];

export interface Figure {
  label: string;
  light: [wcag: string, apca: string];
  dark: [wcag: string, apca: string];
  lcd?: boolean;
}

export const CONTRAST: Figure[] = [
  { label: 'Body ink', light: ['11.8:1', '81'], dark: ['12.3:1', '92'] },
  { label: 'Secondary ink', light: ['8.8:1', '76'], dark: ['10.0:1', '79'] },
  { label: 'Placeholder', light: ['4.9:1', '58'], dark: ['6.2:1', '50'] },
  { label: 'Input affix', light: ['7.9:1', '69'], dark: ['11.4:1', '80'] },
  { label: 'Orange button label', light: ['4.9 to 5.9:1', '79 to 84'], dark: ['4.9 to 5.9:1', '79 to 84'] },
  { label: 'Green button label', light: ['4.7:1', '78'], dark: ['4.7:1', '78'] },
  { label: 'Error text', light: ['6.2:1', '66'], dark: ['8.8:1', '71'] },
  { label: 'LCD text', light: ['8.9:1', '67'], dark: ['10.8:1', '81'], lcd: true },
  { label: 'Focus ring', light: ['11.8:1', '81'], dark: ['12.3:1', '92'] },
];

export const CONTRAST_RULES = [
  'Body text targets Lc 75 or more, labels Lc 60 or more, placeholders and large text Lc 45 or more.',
  "Focus is a 2px ink ring with an offset. It's never orange, so it can't be mistaken for the primary action.",
  'Plastc respects reduced motion, and forced colors give every part a real border.',
];

export interface InvoiceLine {
  d: string;
  p: number;
  q: number;
}
export interface InvoiceState {
  to: string;
  lines: InvoiceLine[];
  terms: number;
  rem: boolean;
  pay: number;
  note: string;
  err: boolean;
}

export const INVOICE_NUMBER = 'INV-0194';
export const INVOICE_INIT: InvoiceState = {
  to: 'Northwind Co-op',
  lines: [
    { d: 'Design workshop', p: 1200, q: 2 },
    { d: 'Icon set', p: 350, q: 3 },
  ],
  terms: 1,
  rem: true,
  pay: 0,
  note: '',
  err: false,
};
export const LINE_PRESETS: [string, number][] = [
  ['Brand photography', 900],
  ['Copywriting', 450],
];
export const MAX_LINES = 4;
export const QTY_MIN = 1;
export const QTY_MAX = 99;
export const TAX_PERCENT = 8;
export const TERMS = ['Net 14', 'Net 30', 'Net 60'];
export const PAYMENT_METHODS = [
  { label: 'Card', hint: 'They pay from the invoice link.' },
  { label: 'Bank transfer', hint: 'Your bank details print on the invoice.' },
];

export const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
export const invoiceTotals = (lines: InvoiceLine[]) => {
  const sub = lines.reduce((a, l) => a + l.p * l.q, 0);
  const tax = Math.round(sub * TAX_PERCENT) / 100;
  return { sub, tax, grand: sub + tax };
};
export const initials = (name: string) =>
  name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w.charAt(0).toUpperCase())
    .join('');
