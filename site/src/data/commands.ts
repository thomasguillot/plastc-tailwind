import type { CommandItem } from '../components/CommandMenu.astro';

export const THEME_COMMAND: CommandItem = {
  icon: 'moon',
  text: '<span data-theme-next>Switch to dark</span>',
  attrs: { 'data-command': 'theme' },
};
