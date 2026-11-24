import type { CommandItem } from '../components/CommandMenu.astro';

export const HOUSING_COMMAND: CommandItem = {
  icon: 'moon',
  text: '<span data-housing-next>Switch to dark</span>',
  attrs: { 'data-command': 'housing' },
};
