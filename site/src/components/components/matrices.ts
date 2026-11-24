import { icon } from '../../lib/icons';

export type State = 'default' | 'hover' | 'focus' | 'active' | 'on' | 'disabled' | 'invalid' | 'busy';

export const STATE_LABEL: Record<State, string> = {
  default: 'Default',
  hover: 'Hover',
  focus: 'Focus',
  active: 'Pressed',
  on: 'On',
  disabled: 'Disabled',
  invalid: 'Invalid',
  busy: 'Busy',
};

export const NA_REASON: Record<State, string> = {
  default: 'Not shown here.',
  hover: 'No hover style.',
  focus: 'Cannot take focus.',
  active: 'No pressed style.',
  on: 'No on state.',
  disabled: 'No disabled style.',
  invalid: 'No invalid style.',
  busy: 'No busy state.',
};

export interface MatrixRow {
  name: string;
  cls: string;
  cells: Partial<Record<State, string>>;
  pad?: boolean;
}

export interface Matrix {
  states: State[];
  cellClass?: string;
  note?: string;
  rows: MatrixRow[];
}

const ATTR: Record<State, string> = {
  default: '',
  hover: '',
  focus: '',
  active: '',
  on: '',
  disabled: ' disabled',
  invalid: ' aria-invalid="true"',
  busy: ' aria-busy="true"',
};

const row = (name: string, cls: string, allow: State[], make: (state: State, attr: string) => string, pad = false): MatrixRow => ({
  name,
  cls,
  pad,
  cells: Object.fromEntries(allow.map((s) => [s, make(s, ATTR[s])])),
});

const press = (s: State, attr: string) => (s === 'on' ? ' aria-pressed="true"' : attr);

const button = (cls: string, label: string) => (s: State, attr: string) => `<button type="button" class="${cls}"${press(s, attr)}>${label}</button>`;
const BTN: State[] = ['default', 'hover', 'focus', 'active', 'on', 'disabled', 'busy'];

export const buttons: Matrix = {
  states: BTN,
  rows: [
    row('Secondary', '.btn', BTN, button('btn', 'Save')),
    row('Signal', '.btn-signal', BTN, button('btn btn-signal', 'Send')),
    row('Go', '.btn-go', BTN, button('btn btn-go', 'Approve')),
    row('Quiet', '.btn-quiet', BTN, button('btn btn-quiet', 'Cancel')),
    row('Danger', '.btn-danger', BTN, button('btn btn-danger', 'Delete')),
    row('Icon', '.btn-icon', BTN, (s, attr) => `<button type="button" class="btn btn-icon" aria-label="Notifications"${press(s, attr)}>${icon('bell')}</button>`),
    row('Key', '.key', ['default', 'hover', 'focus', 'active', 'on', 'disabled'], (s, attr) => `<button type="button" class="key" style="width:48px" aria-label="Escape"${press(s, attr)}>Esc</button>`),
  ],
};

const FIELD: State[] = ['default', 'focus', 'disabled', 'invalid'];
const fieldValue = (s: State) => (s === 'invalid' ? ' value="billing@halden"' : '');

export const fields: Matrix = {
  states: ['default', 'hover', 'focus', 'on', 'disabled', 'invalid'],
  cellClass: 'max-w-[148px]',
  rows: [
    row('Text field', '.field', FIELD, (s, attr) => `<input class="field" placeholder="Name or email" aria-label="Customer"${fieldValue(s)}${attr}>`),
    row('Select', '.field-select', FIELD, (s, attr) => `<select class="field field-select" aria-label="Currency"${attr}><option>USD</option><option>EUR</option></select>`),
    row('Text area', '.field-area', FIELD, (s, attr) => `<textarea class="field field-area !min-h-16" aria-label="Note" placeholder="Add a note"${attr}></textarea>`),
    row('Input group', '.input-group', FIELD, (s, attr) => `<label class="input-group">${icon('search')}<input aria-label="Search invoices" placeholder="Search"${fieldValue(s)}${attr}></label>`),
    row('List option', '.listbox', ['default', 'hover', 'focus', 'on', 'disabled'], (s) => `<div class="float rounded-[14px] w-full"><div class="listbox" role="listbox" aria-label="Customers"><div role="option" aria-selected="${s === 'on'}"${s === 'focus' ? ' data-active' : ''}${s === 'disabled' ? ' aria-disabled="true"' : ''}>Halden</div></div></div>`),
    row('Calendar day', '.calendar', ['default', 'hover', 'focus', 'on', 'disabled'], (s, attr) => `<div class="calendar"><table><tbody><tr><td><button type="button"${s === 'on' ? ' aria-pressed="true"' : attr}>24</button></td></tr></tbody></table></div>`),
    row('Drop zone', '.dropzone', ['default', 'focus', 'on', 'disabled', 'invalid'], (s, attr) => `<label class="dropzone"${s === 'on' ? ' data-dragover' : ''}>${icon('upload')}<span>Drop a file</span><input type="file" aria-label="Upload a file"${attr}></label>`),
  ],
};

const SELECT: State[] = ['default', 'hover', 'focus', 'on', 'disabled'];
const check = (cls: string, extra = '') => (s: State, attr: string) => `<input type="checkbox" class="${cls}"${extra} aria-label="Send copy"${s === 'on' ? ' checked' : ''}${s === 'disabled' || s === 'invalid' ? attr : ''}>`;

export const selection: Matrix = {
  states: [...SELECT, 'invalid'],
  rows: [
    row('Checkbox', '.check', ['default', 'focus', 'on', 'disabled', 'invalid'], check('check')),
    row('Radio', '.radio', ['default', 'focus', 'on', 'disabled', 'invalid'], (s, attr) => `<input type="radio" class="radio" aria-label="Monthly"${s === 'on' ? ' checked' : ''}${s === 'disabled' || s === 'invalid' ? attr : ''}>`),
    row('Switch', '.switch', ['default', 'focus', 'on', 'disabled'], check('switch', ' role="switch"')),
    row('Choice card', '.choice-card', SELECT, (s, attr) => `<label class="choice-card"><input type="checkbox" class="check mt-0.5"${s === 'on' ? ' checked' : ''}${s === 'disabled' ? attr : ''}><span class="text-sm font-bold">Monthly</span></label>`),
    row('Segment', '.seg', SELECT, (s) => `<div class="seg" role="group" aria-label="View"${s === 'disabled' ? ' aria-disabled="true"' : ''}><button type="button" aria-pressed="${s === 'on' || s === 'disabled'}"${s === 'disabled' ? ' disabled' : ''}>Grid</button></div>`),
    row('Range', '.range', ['default', 'focus', 'disabled'], (s, attr) => `<input type="range" class="range" min="0" max="10" value="4" aria-label="Late fee" style="--fill:40%;min-width:112px"${s === 'disabled' ? attr : ''}>`),
  ],
};

export const status: Matrix = {
  states: ['default', 'busy'],
  note: 'Badges, tags, meters, alerts and empty states take no input, so they look the same in every state. Spinners and skeletons appear only while something loads.',
  rows: [
    row('Progress', '.progress', ['default', 'busy'], (s) => `<div class="progress" role="progressbar" aria-label="Export"${s === 'busy' ? '' : ' aria-valuemin="0" aria-valuemax="100" aria-valuenow="64"'} style="min-width:96px"><span${s === 'busy' ? '' : ' style="--v:64%"'}></span></div>`),
    row('Spinner', '.spinner', ['busy'], () => `<span class="spinner" role="status"><span class="sr-only">Loading</span></span>`),
    row('Skeleton', '.skeleton', ['busy'], () => `<span class="grid gap-2" role="status" aria-label="Loading"><span class="skeleton h-3 w-24"></span><span class="skeleton h-3 w-16"></span></span>`),
  ],
};

export const overlays: Matrix = {
  states: ['default', 'hover', 'focus', 'disabled'],
  rows: [
    row('Menu item', '.menu', ['default', 'hover', 'focus', 'disabled'], (s, attr) => `<div class="menu !min-w-0 w-full"><button type="button"${attr}>${icon('copy')}Duplicate</button></div>`),
    row('Tooltip', '.tooltip', ['default', 'hover', 'focus'], () => `<span class="tooltip" data-tip="3 unread"><button type="button" class="btn btn-icon" aria-label="Notifications, 3 unread">${icon('bell')}</button></span>`, true),
    row('Toast action', '.lcd-action', ['default', 'hover', 'focus'], () => `<div class="toast"><span>Invoice sent</span><button type="button" class="lcd-action">Undo</button></div>`),
  ],
};

export const navigation: Matrix = {
  states: ['default', 'hover', 'focus', 'on', 'disabled'],
  rows: [
    row('Tab', '.tabs', ['default', 'hover', 'focus', 'on', 'disabled'], (s, attr) => `<div class="tabs" role="tablist" aria-label="Sections"><button type="button" role="tab" aria-selected="${s === 'on'}"${attr}>Invoices</button></div>`),
    row('Page number', '.pager-pages', ['default', 'hover', 'focus', 'on', 'disabled'], (s, attr) => `<div class="seg pager-pages" role="group" aria-label="Pages"><button type="button"${s === 'on' ? ' aria-current="page"' : ''}${attr}>2</button></div>`),
    row('Breadcrumb', '.breadcrumbs', ['default', 'hover', 'focus', 'on'], (s) => `<ol class="breadcrumbs"><li>${s === 'on' ? '<span aria-current="page">INV-0193</span>' : '<a href="#states">Invoices</a>'}</li></ol>`),
    row('Accordion row', '.accordion', ['default', 'hover', 'focus', 'on'], (s) => `<div class="accordion"><details${s === 'on' ? ' open' : ''}><summary>Reminders</summary><p>Sent after the due date.</p></details></div>`),
  ],
};

export const data: Matrix = {
  states: ['default', 'hover', 'focus', 'on', 'disabled'],
  rows: [
    row('Nav item', '.nav-item', ['default', 'hover', 'focus', 'on', 'disabled'], (s) => (s === 'disabled' ? `<a class="nav-item" role="link" aria-disabled="true">${icon('home')}Dashboard</a>` : `<a class="nav-item" href="#states"${s === 'on' ? ' aria-current="page"' : ''}>${icon('home')}Dashboard</a>`)),
    row('Table row', '.ktable', ['default', 'hover', 'on'], (s) => `<table class="ktable"><tbody><tr><td><input type="checkbox" class="check" aria-label="Select INV-0193"${s === 'on' ? ' checked' : ''}></td><td>INV-0193</td></tr></tbody></table>`),
    row('Chart bar', '.bar-chart', ['default', 'hover', 'on'], (s) => `<div class="bar-chart" style="--chart-h:72px;min-width:64px" role="img" aria-label="Invoices sent, 31"><div class="bar" style="--v:70%"${s === 'on' ? ' data-current' : ''}><span>31</span></div></div>`),
    row('Avatar button', '.avatar-group', ['default', 'focus'], () => `<div class="avatar-group"><button type="button" class="avatar" aria-label="3 more people">+3</button></div>`),
    row('Key hint', '.kbd', ['default'], () => `<span class="kbd">N</span>`),
    row('LCD readout', '.lcd', ['default'], () => `<div class="lcd px-4 py-2"><p class="text-xl font-semibold">$48,210</p></div>`),
  ],
};

export const surfaces: Matrix = {
  states: ['default', 'active'],
  note: 'Plane, raised, recessed and float have no states of their own. Add .pressable to a raised part to give it a pressed state.',
  rows: [
    row('Raised, pressable', '.pressable', ['default', 'active'], () => `<div class="raised pressable rounded-xl px-4 py-3 text-[13px] font-bold">Press</div>`),
  ],
};

export const MATRICES = { buttons, fields, selection, status, overlays, navigation, data, surfaces };
