import type { CommandGroup, CommandItem } from '../components/CommandMenu.astro';
import { PAGES } from '../components/components/pages';
import { MARKETING_SCREENS, SCREENS } from './showcase';
import { IMPORT_LINE, REPO } from './site';

type Icon = CommandItem['icon'];

export const THEME_COMMAND: CommandItem = {
  icon: 'moon',
  text: '<span data-theme-next>Switch to dark</span>',
  attrs: { 'data-command': 'theme' },
};

const SCREEN_ICONS: Record<string, Icon> = {
  dashboard: 'home',
  invoices: 'file',
  settings: 'cog',
  customers: 'users',
  reports: 'chart',
  products: 'box',
  landing: 'send',
  pricing: 'tag',
  blog: 'book',
  article: 'article',
  about: 'info',
  contact: 'mail',
  'sign-in': 'key',
  '404': 'compass',
};

const screen = (key: string, text: string, icon: Icon, hash = ''): CommandItem => ({
  icon,
  text,
  attrs: { href: `/screens/${key}.html${hash}`, 'data-open-screen': `${key}${hash}` },
});

const keywords = (page: (typeof PAGES)[number]) =>
  [...new Set([page.title, page.classes, ...page.rows.map((r) => r.cls)].join(' ').replace(/[.,]/g, ' ').split(/\s+/).filter(Boolean))].join(' ');

export function siteCommands(onThisPage: CommandItem[] = []): CommandGroup[] {
  const marketing = MARKETING_SCREENS.flatMap(({ key, title }) => [
    screen(key, title, SCREEN_ICONS[key]),
    ...(key === 'about' ? [screen('about', 'Careers', 'briefcase', '#careers')] : []),
  ]);
  return [
    { label: 'Screens', items: SCREENS.map(({ key, title }) => screen(key, title, SCREEN_ICONS[key])) },
    { label: 'Marketing pages', items: marketing },
    ...(onThisPage.length ? [{ label: 'On this page', items: onThisPage }] : []),
    {
      label: 'Components',
      items: [
        { icon: 'grid', text: 'Browse all components', attrs: { href: '/components/' } },
        ...PAGES.map((p) => ({ icon: 'grid' as const, text: p.title, attrs: { href: `/components/${p.slug}/`, 'data-keywords': keywords(p) } })),
      ],
    },
    {
      label: 'Actions',
      items: [
        THEME_COMMAND,
        { icon: 'down', text: 'Download plastc.css', attrs: { href: '/plastc.css', download: true } },
        { icon: 'copy', text: 'Copy the import line', attrs: { 'data-copy': IMPORT_LINE } },
        { icon: 'external', text: 'Source on GitHub', attrs: { href: REPO } },
      ],
    },
  ];
}
