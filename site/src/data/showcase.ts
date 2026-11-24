export interface ShowcaseGroupInfo {
  id: string;
  title: string;
  classes: string;
  wide?: boolean;
}

const slug = (title: string) => title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const group = (title: string, classes: string, wide = false): ShowcaseGroupInfo => ({ id: slug(title), title, classes, wide });

export const GROUPS = {
  buttons: group('Buttons', '.btn  .btn-signal  .btn-go  .btn-quiet  .btn-sm…2xl'),
  inputs: group('Inputs', '.field  .field-select  .field-area  .label  .hint'),
  inputGroups: group('Input groups', '.input-group  .input-affix'),
  status: group('Status & feedback', '.badge  .lamp-*  .tag  .meter  .alert'),
  combobox: group('Combobox & date picker', '.combobox  .calendar  .popover'),
  selection: group('Selection', '.check  .radio  .switch  .choice-card  .seg  .range'),
  empty: group('Empty states', '.empty  .readout  .empty-actions'),
  overlays: group('Overlays', '.menu  .dialog  .toast  .tooltip'),
  progress: group('Progress & loading', '.progress  .spinner  .skeleton'),
  upload: group('File upload', '.dropzone  .file-item'),
  tabs: group('Tabs & pagination', '.tabs  .pager  .pager-pages  .pager-status'),
  command: group('Breadcrumbs & command menu', '.breadcrumbs  .command'),
  accordion: group('Accordion & description list', '.accordion  .desc-list'),
  timeline: group('Avatar group & timeline', '.avatar-group  .timeline'),
  charts: group('Charts', '.bar-chart  .chart  .sparkline', true),
  navigation: group('Navigation & data', '.nav-item  .seg  .ktable  .kbd  .lcd', true),
} satisfies Record<string, ShowcaseGroupInfo>;

export const SCREENS = [
  { key: 'dashboard', title: 'Dashboard' },
  { key: 'invoices', title: 'Invoices' },
  { key: 'customers', title: 'Customers' },
  { key: 'reports', title: 'Reports' },
  { key: 'products', title: 'Products' },
  { key: 'settings', title: 'Settings' },
];

export const MARKETING_SCREENS = [
  { key: 'landing', title: 'Landing page' },
  { key: 'pricing', title: 'Pricing' },
  { key: 'blog', title: 'Blog' },
  { key: 'article', title: 'Article' },
  { key: 'about', title: 'About' },
  { key: 'contact', title: 'Contact' },
  { key: 'sign-in', title: 'Sign in' },
  { key: '404', title: '404' },
];

export const DEPTH_TOKENS = [
  { name: 'Plane', token: '--k-seam-line', style: 'background:var(--k-housing);border:1px solid var(--k-seam);box-shadow:var(--k-seam-line)', note: 'Flush. Panels, tabs, tables.', decl: 'box-shadow: var(--k-seam-line);' },
  { name: 'Raised', token: '--k-raised', style: 'background:var(--k-housing);box-shadow:var(--k-raised)', note: 'A part you press.', decl: 'box-shadow: var(--k-raised);' },
  { name: 'Pressed', token: '--k-pressed', style: 'background:var(--k-housing);box-shadow:var(--k-pressed)', note: 'A raised part, pushed in.', decl: 'box-shadow: var(--k-pressed);' },
  { name: 'Recessed', token: '--k-recessed', style: 'background:var(--k-housing);box-shadow:var(--k-recessed)', note: 'Holds input or output.', decl: 'box-shadow: var(--k-recessed);' },
  { name: 'Float', token: '--k-float', style: 'background:var(--k-housing-up);box-shadow:var(--k-float)', note: 'Overlays only.', decl: 'box-shadow: var(--k-float);' },
];

export const SCALE = [25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950];
