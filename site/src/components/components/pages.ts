import { GROUPS } from '../../data/showcase';

export interface ClassRow {
  cls: string;
  use: string;
  notes: string;
}

export interface ComponentsPage {
  slug: string;
  title: string;
  summary: string;
  lead: string;
  classes: string;
  examples: (keyof typeof GROUPS)[];
  rows: ClassRow[];
}

export const PAGES: ComponentsPage[] = [
  {
    slug: 'surfaces',
    title: 'Surfaces',
    summary: 'The four depths and the tokens behind them, plus panels, seams and the color scales.',
    lead: 'Every part sits at one of four depths, and the depth tells you what the part does. Build your own parts at the right level with these classes.',
    classes: '.panel  .seam  .raised  .recessed  .float  .pressable',
    examples: [],
    rows: [
      { cls: '.panel', use: 'A layout container on the plane.', notes: 'Flush, with a seam and no drop shadow.' },
      { cls: '.seam', use: 'A parting line on any element.', notes: 'A 1px line with a highlight lip. Add a radius yourself.' },
      { cls: '.raised', use: 'A part you press.', notes: 'Uses --k-raised. Add .pressable to make it sink when pressed.' },
      { cls: '.pressable', use: 'Press physics for any raised part.', notes: 'Down in 80ms, back up in 160ms. Sets 1px of travel.' },
      { cls: '.recessed', use: 'A part that holds input or output.', notes: 'Uses --k-recessed on the darker fill.' },
      { cls: '.float', use: 'An overlay you build yourself.', notes: 'The only level with a long shadow. Prefer .menu, .popover or .dialog.' },
      { cls: '.depth-soft, .depth-deep', use: 'Scale every shadow in a region.', notes: 'Sets --k-depth to 0.5 or 1.7. Works on any ancestor.' },
    ],
  },
  {
    slug: 'buttons',
    title: 'Buttons',
    summary: 'Four colors, five sizes, the icon button and the round key.',
    lead: 'Buttons are the raised parts. They catch more light on hover, sink when pressed and keep their color while down.',
    classes: '.btn  .btn-signal  .btn-go  .btn-quiet  .btn-danger  .btn-icon  .key',
    examples: ['buttons'],
    rows: [
      { cls: '.btn', use: 'The default action.', notes: 'A raised pill. Add a color class for emphasis.' },
      { cls: '.btn-signal', use: 'The one primary action in a view.', notes: 'Orange. Use it once per view.' },
      { cls: '.btn-go', use: 'Confirming or positive actions.', notes: 'Green.' },
      { cls: '.btn-quiet', use: 'Tertiary actions in dense layouts.', notes: 'No body until you hover or press it.' },
      { cls: '.btn-danger', use: 'Destructive actions.', notes: 'Colors the label only. Combine it with .btn.' },
      { cls: '.btn-sm to .btn-2xl', use: 'Size.', notes: 'Heights of 32, 40, 46, 50 and 58px.' },
      { cls: '.btn-icon', use: 'A square button with only an icon.', notes: 'Give it an aria-label.' },
      { cls: '.key', use: 'Round, hardware-style controls.', notes: 'aria-pressed="true" latches it down. Set its width to size it.' },
      { cls: 'aria-busy="true"', use: 'A button that is working.', notes: 'Shows a spinner and keeps its body. Add disabled to block clicks.' },
    ],
  },
  {
    slug: 'fields',
    title: 'Fields',
    summary: 'Text fields, selects, input groups, the combobox, the date picker and file upload.',
    lead: 'Fields are recessed wells that hold input. Focus, invalid and disabled are read from the input, so you set the attribute and the well follows.',
    classes: '.field  .field-select  .field-area  .input-group  .combobox  .calendar  .dropzone',
    examples: ['inputs', 'inputGroups', 'combobox', 'upload'],
    rows: [
      { cls: '.field', use: 'A text input.', notes: 'Invalid with aria-invalid="true". Disabled drops the well.' },
      { cls: '.field-select', use: 'A native select.', notes: 'Add it next to .field. It draws its own chevron.' },
      { cls: '.field-area', use: 'A multi-line input.', notes: 'Resizes vertically. Minimum height 108px.' },
      { cls: '.label, .hint, .hint-error', use: 'Text around a field.', notes: 'Tie them to the input with for and aria-describedby.' },
      { cls: '.input-group', use: 'One well around an icon, affix, key hint or button.', notes: 'Wrap it in a label unless it holds a button.' },
      { cls: '.input-affix', use: 'Fixed text inside an input group.', notes: 'A seam divides it from the value.' },
      { cls: '.combobox, .listbox', use: 'An input with a list of options.', notes: 'Filtering and arrow keys are your script. plastc.js shows one way.' },
      { cls: '.calendar, .popover', use: 'A date picker.', notes: 'aria-pressed marks the chosen day and aria-current="date" marks today.' },
      { cls: '.dropzone, .file-item', use: 'File upload and its file list.', notes: 'data-dragover shows a file held over the zone.' },
    ],
  },
  {
    slug: 'selection',
    title: 'Selection',
    summary: 'Checkboxes, radios, switches, choice cards, segmented controls and the range slider.',
    lead: 'Choosing something changes its depth. Checked parts and chosen cards sink in, and the chosen segment stands up.',
    classes: '.check  .radio  .switch  .choice-card  .seg  .range',
    examples: ['selection'],
    rows: [
      { cls: '.check', use: 'A checkbox.', notes: '20px, or 24px on coarse pointers.' },
      { cls: '.radio', use: 'One choice from a group.', notes: 'The dot is ink, not orange.' },
      { cls: '.switch', use: 'An on or off setting that applies now.', notes: 'Put it on a checkbox with role="switch".' },
      { cls: '.choice-card', use: 'A large target for a radio or checkbox.', notes: 'Flush until checked, then recessed.' },
      { cls: '.seg', use: 'A filter or view mode inside a panel.', notes: 'Children use aria-pressed, aria-selected or aria-current.' },
      { cls: '.range', use: 'A value on a scale.', notes: 'Set --fill to the value as a percentage.' },
    ],
  },
  {
    slug: 'status',
    title: 'Status',
    summary: 'Badges, tags, meters and alerts, plus progress, spinners, skeletons and empty states.',
    lead: 'Status parts report and take no input. Lamps carry the state, so a badge is a lit dot beside a flat label rather than a filled pill.',
    classes: '.badge  .lamp-*  .tag  .meter  .alert  .progress  .spinner  .skeleton  .empty',
    examples: ['status', 'progress', 'empty'],
    rows: [
      { cls: '.badge', use: 'A status label.', notes: 'Pair with .lamp-ok, .lamp-warn, .lamp-danger, .lamp-signal or .lamp-off.' },
      { cls: '.tag', use: 'A neutral label such as a term or currency.', notes: 'No lamp.' },
      { cls: '.meter', use: 'A level shown as an LCD readout.', notes: 'role="meter" with the fill in --v.' },
      { cls: '.alert', use: 'A message that stays on the page.', notes: 'Add a lamp class for severity.' },
      { cls: '.progress', use: 'A task with a known or unknown length.', notes: 'No aria-valuenow runs it indeterminate.' },
      { cls: '.spinner', use: 'A wait with no measurable progress.', notes: 'Add .spinner-lg or set --spinner-size. Pair with role="status".' },
      { cls: '.skeleton', use: 'A placeholder while content loads.', notes: 'Size it with utilities and label the region.' },
      { cls: '.empty, .readout', use: 'A view with nothing in it yet.', notes: 'Say why it is empty and what to do next.' },
    ],
  },
  {
    slug: 'overlays',
    title: 'Overlays',
    summary: 'Menus, dialogs, toasts and tooltips, the only parts with a long shadow.',
    lead: 'Overlays sit above the page. Menus, dialogs and toasts are native popover and dialog elements, so Esc and outside clicks work without a script.',
    classes: '.menu  .dialog  .sheet  .toast  .tooltip  .lcd-action',
    examples: ['overlays'],
    rows: [
      { cls: '.menu', use: 'A list of actions.', notes: 'On [popover]. Items are plain buttons or links.' },
      { cls: '.dialog', use: 'A decision or a short form.', notes: 'On <dialog>. .dialog-full fills 90% of the viewport.' },
      { cls: '.sheet', use: 'Navigation on small screens.', notes: 'A dialog that slides in from the left edge.' },
      { cls: '.toast', use: 'Feedback after an action.', notes: 'On [popover="manual"]. Stays 6 seconds and pauses on hover.' },
      { cls: '.tooltip', use: 'A short label for an icon button.', notes: 'Set data-tip on the wrapper. Shows on hover or focus.' },
      { cls: '.lcd-action', use: 'An action printed on LCD glass.', notes: 'Use it instead of a raised button inside a toast.' },
    ],
  },
  {
    slug: 'navigation',
    title: 'Navigation',
    summary: 'Tabs, pagination, breadcrumbs, the command menu and the accordion.',
    lead: 'Navigation stays flat. The current tab carries an ink indicator and the current breadcrumb is bold, so nothing competes with the buttons.',
    classes: '.tabs  .pager  .breadcrumbs  .command  .accordion  .desc-list',
    examples: ['tabs', 'command', 'accordion'],
    rows: [
      { cls: '.tabs', use: 'Switch panels or sections of a page.', notes: 'aria-selected for panels, aria-current="page" for links.' },
      { cls: '.pager', use: 'Previous, page numbers and Next.', notes: 'Numbers hide below 640px and the status text shows.' },
      { cls: '.pager-pages, .pager-status', use: 'The middle of a pager.', notes: 'Pages are a .seg. The status reads "Page 1 of 8".' },
      { cls: '.breadcrumbs', use: 'Where this page sits.', notes: 'On an ol inside nav. The last item has aria-current="page".' },
      { cls: '.dialog.command', use: 'Search and jump to anything.', notes: 'A search input group and a .listbox. The key handling is your script.' },
      { cls: '.accordion', use: 'Rows that open in place.', notes: 'Native details and summary. Opens smoothly where supported.' },
      { cls: '.desc-list', use: 'Label and value pairs.', notes: 'On a dl of div rows. Stacks below 640px.' },
    ],
  },
  {
    slug: 'data',
    title: 'Data',
    summary: 'Nav items, tables, key hints, LCD readouts, avatar groups, timelines and charts.',
    lead: 'Data stays flat. Rows, bars and stat blocks are never extruded, and only LCD readouts sit in a well.',
    classes: '.nav-item  .ktable  .kbd  .lcd  .avatar-group  .timeline  .bar-chart  .chart',
    examples: ['navigation', 'timeline', 'charts'],
    rows: [
      { cls: '.nav-item', use: 'A sidebar link.', notes: 'aria-current="page" sinks the current one.' },
      { cls: '.ktable', use: 'A table of records.', notes: 'Wrap it in .table-scroll. A checked row sinks.' },
      { cls: '.kbd', use: 'A keyboard shortcut hint.', notes: 'One key per element.' },
      { cls: '.lcd', use: 'A readout of key figures.', notes: 'Geist Mono on sage glass. Nothing raised goes inside.' },
      { cls: '.avatar, .avatar-group', use: 'People, singly or overlapping.', notes: 'A button.avatar at the end can open the rest.' },
      { cls: '.timeline', use: 'Events in order.', notes: 'Each li gets a lamp dot and a time.' },
      { cls: '.bar-chart', use: 'Bars for a few periods.', notes: 'Each .bar is sized by --v. data-current marks the period in focus.' },
      { cls: '.chart, .sparkline', use: 'SVG charts and trend lines.', notes: 'Give every chart role="img" and an aria-label that states the numbers.' },
    ],
  },
];

export const ORDER = PAGES.map((p) => p.slug);
