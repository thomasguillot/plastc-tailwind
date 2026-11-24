import { iconSvg } from '../../lib/icons';
import { money, QTY_MAX, QTY_MIN, type InvoiceLine } from '../../data/home';

const esc = (v: string) => v.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);
const MINUS = iconSvg('<path d="M5 12h14"/>', 'w-4 h-4', '2');
const PLUS = iconSvg('<path d="M12 5v14M5 12h14"/>', 'w-4 h-4', '2');

export const lineId = (prefix: string, i: number) => `d${prefix}${i + 1}`;

export function lineHTML(prefix: string, i: number, l: InvoiceLine) {
  const id = lineId(prefix, i);
  const n = esc(l.d);
  return (
    `<li class="py-3 grid gap-2" data-line="${i}"><label class="sr-only" for="${id}">Description</label><input id="${id}" class="field" value="${n}" data-desc>` +
    `<div class="flex items-center gap-3"><div class="flex items-center gap-2" role="group" aria-label="Quantity">` +
    `<button type="button" class="key w-11 h-11 md:w-8 md:h-8" data-step="-1" aria-label="Decrease quantity for ${n}"${l.q <= QTY_MIN ? ' disabled' : ''}>${MINUS}</button>` +
    `<span class="font-mono text-sm font-semibold tabular-nums w-6 text-center" data-qty>${l.q}</span>` +
    `<button type="button" class="key w-11 h-11 md:w-8 md:h-8" data-step="1" aria-label="Increase quantity for ${n}"${l.q >= QTY_MAX ? ' disabled' : ''}>${PLUS}</button></div>` +
    `<span class="text-sm text-ink-2 tabular-nums">&times; ${money.format(l.p)}</span><span class="ml-auto font-semibold text-sm tabular-nums" data-total>${money.format(l.p * l.q)}</span></div></li>`
  );
}
