import libraryCss from '../../../src/plastc.css?raw';
import { decodeHTML } from 'entities';
import { iconSvg } from './icons';

type Attr = [string, string | null];
interface Node {
  tag: string | null;
  attrs: Attr[];
  selfclose: boolean;
  children: Child[];
}
type Child = Node | string;

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const SVG_CASE: Record<string, string> = { viewbox: 'viewBox', preserveaspectratio: 'preserveAspectRatio', lineargradient: 'linearGradient' };
const LIBRARY_DATA = new Set(libraryCss.match(/data-[a-z-]+/g) ?? []);

const TOKEN = /<!--[\s\S]*?-->|<\/([a-zA-Z][^\s/>]*)[^>]*>|<([a-zA-Z][^\s/>]*)((?:\s+[^\s"'>/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+))?)*)\s*(\/?)>/g;
const ATTR = /([^\s"'>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;

function parse(markup: string): Node {
  const root: Node = { tag: null, attrs: [], selfclose: false, children: [] };
  const stack: Node[] = [root];
  let last = 0;
  const text = (s: string) => {
    if (s) stack[stack.length - 1].children.push(decodeHTML(s));
  };
  for (const m of markup.matchAll(TOKEN)) {
    text(markup.slice(last, m.index));
    last = m.index! + m[0].length;
    if (m[0].startsWith('<!--')) continue;
    if (m[1]) {
      const tag = m[1].toLowerCase();
      for (let k = stack.length - 1; k > 0; k--) {
        if (stack[k].tag === tag) {
          stack.length = k;
          break;
        }
      }
      continue;
    }
    const tag = m[2].toLowerCase();
    const attrs: Attr[] = [];
    for (const a of (m[3] ?? '').matchAll(ATTR)) {
      const v = a[2] ?? a[3] ?? a[4];
      attrs.push([a[1].toLowerCase(), v === undefined ? null : decodeHTML(v)]);
    }
    const node: Node = { tag, attrs, selfclose: m[4] === '/', children: [] };
    stack[stack.length - 1].children.push(node);
    if (!node.selfclose && !VOID.has(tag)) stack.push(node);
  }
  text(markup.slice(last));
  return root;
}

const isNode = (c: Child): c is Node => typeof c !== 'string';
const attrMap = (n: Node) => Object.fromEntries(n.attrs) as Record<string, string | null>;

const WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

function isoDate(d: Date) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export function staticCalendar(value: string) {
  const [y, mo, da] = value.split('-').map(Number);
  const sel = new Date(y, mo - 1, da);
  const first = new Date(y, mo - 1, 1);
  const start = new Date(y, mo - 1, 1 - first.getDay());
  const today = isoDate(new Date());
  let rows = '';
  for (let w = 0; w < 6; w++) {
    let cells = '';
    for (let d = 0; d < 7; d++) {
      const day = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7 + d);
      const isSel = isoDate(day) === value;
      const extra = (day.getMonth() !== sel.getMonth() ? ' data-outside' : '') + (isoDate(day) === today ? ' aria-current="date"' : '');
      cells += `<td><button type="button" tabindex="${isSel ? 0 : -1}" aria-label="${WEEKDAYS[day.getDay()]}, ${MONTH_NAMES[day.getMonth()]} ${day.getDate()}, ${day.getFullYear()}"${extra} aria-pressed="${isSel ? 'true' : 'false'}">${day.getDate()}</button></td>`;
    }
    rows += `<tr>${cells}</tr>`;
  }
  const title = `${MONTH_NAMES[first.getMonth()]} ${first.getFullYear()}`;
  const heads = WEEKDAYS.map((n) => `<th scope="col"><abbr title="${n}">${n.slice(0, 2)}</abbr></th>`).join('');
  const step = (label: string, d: string) => `<button type="button" class="btn btn-quiet btn-sm btn-icon" aria-label="${label}">${iconSvg(`<path d="${d}"/>`)}</button>`;
  return (
    `<div class="calendar-head">${step('Previous month', 'm15 6-6 6 6 6')}<p class="calendar-title" aria-live="polite">${title}</p>${step('Next month', 'm9 6 6 6-6 6')}</div>` +
    `<table role="grid" aria-label="${title}"><thead><tr>${heads}</tr></thead><tbody>${rows}</tbody></table>`
  );
}

function stripDemo(node: Node, dialog: string | null = null) {
  const kept: Child[] = [];
  for (const c of node.children) {
    if (!isNode(c)) {
      kept.push(c);
      continue;
    }
    const names = new Set(c.attrs.map(([k]) => k));
    if (names.has('data-demo-note')) continue;
    if (names.has('data-calendar') && !c.children.some(isNode)) {
      c.children = parse(staticCalendar(attrMap(c)['data-value'] || isoDate(new Date()))).children;
    }
    const attrs: Attr[] = [];
    for (const [k, v] of c.attrs) {
      if (k === 'data-open-dialog') attrs.push(['commandfor', v], ['command', 'show-modal']);
      else if (k === 'data-open-command') attrs.push(['commandfor', 'command'], ['command', 'show-modal']);
      else if (k === 'data-close-dialog' && dialog) attrs.push(['commandfor', dialog], ['command', 'close']);
      else if (k.startsWith('data-') && !LIBRARY_DATA.has(k)) continue;
      else attrs.push([k, v]);
    }
    c.attrs = attrs;
    stripDemo(c, c.tag === 'dialog' ? (Object.fromEntries(attrs).id ?? null) : dialog);
    kept.push(c);
  }
  node.children = kept;
}

const escText = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const cased = (k: string) => SVG_CASE[k] ?? k;

function openTag(n: Node) {
  const attrs = n.attrs.map(([k, v]) => (v === null ? ` ${cased(k)}` : ` ${cased(k)}="${v.replace(/&/g, '&amp;').replace(/"/g, '&quot;')}"`)).join('');
  return `<${cased(n.tag!)}${attrs}${n.selfclose ? '/' : ''}>`;
}

function inline(n: Child): string {
  if (!isNode(n)) return escText(n.replace(/\s+/g, ' '));
  if (n.selfclose || VOID.has(n.tag!)) return openTag(n);
  return openTag(n) + n.children.map(inline).join('') + `</${cased(n.tag!)}>`;
}

function breaks(n: Child): boolean {
  if (!isNode(n) || n.tag === 'pre' || n.tag === 'textarea') return false;
  if (n.tag === 'svg' && !(attrMap(n).class ?? '').includes('chart')) return false;
  if (n.children.some((c) => !isNode(c) && c.trim())) return false;
  const kids = n.children.filter(isNode);
  return kids.length > 1 || (kids.length === 1 && breaks(kids[0]));
}

function pretty(n: Node, depth = 0): string {
  const pad = '  '.repeat(depth);
  if (!breaks(n)) return pad + inline(n);
  const kids = n.children.filter(isNode).map((c) => pretty(c, depth + 1)).join('\n');
  return `${pad}${openTag(n)}\n${kids}\n${pad}</${cased(n.tag!)}>`;
}

export function cleanHtml(markup: string) {
  const tree = parse(markup);
  stripDemo(tree);
  return tree.children.filter(isNode).map((c) => pretty(c)).join('\n');
}
