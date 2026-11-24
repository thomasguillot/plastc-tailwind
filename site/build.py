"""Generates the Plastc showcase and reference screens. Run: python3 build.py"""
import pathlib, math, json, re, shutil, datetime
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).parent
CSS_SRC = HERE.parent / "src" / "plastc.css"
shutil.copyfile(CSS_SRC, HERE / "plastc.css")
VERSION = json.loads((HERE.parent / "package.json").read_text())["version"]
CSS_KB = round(CSS_SRC.stat().st_size / 1024)
REPO = "https://github.com/thomasguillot/plastc-tailwind"
CSS_ON_GITHUB = f"{REPO}/blob/main/src/plastc.css"

def ico(d, cls="", sw="1.8"):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

I = {
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    "home": '<path d="M3 10.5 12 4l9 6.5V20a1 1 0 0 1-1 1h-5.5v-6h-5v6H4a1 1 0 0 1-1-1z"/>',
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.3-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 14.8c1.7.7 2.8 2.4 3 5.2"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m7 15 4-5 3 3 5-6"/>',
    "box": '<path d="m21 8-9-5-9 5v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    "cog": '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.2a2.6 2.6 0 0 1 5 .9c0 1.8-2.5 2.3-2.5 3.9M12 17.2v.1"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "down": '<path d="M12 4v12M6 11l6 6 6-6M5 20h14"/>',
    "filter": '<path d="M3 5h18M6 12h12M10 19h4"/>',
    "dots": '<circle cx="5" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="19" cy="12" r="1.2"/>',
    "bell": '<path d="M6 9a6 6 0 0 1 12 0c0 6 2.5 7.5 2.5 7.5h-17S6 15 6 9z"/><path d="M10 20a2.2 2.2 0 0 0 4 0"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    "send": '<path d="m21 3-9.5 9.5M21 3l-6.5 18-3-8.5L3 9.5z"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.1"/>',
    "alert": '<path d="M10.3 4.2 2.6 17.6A2 2 0 0 0 4.3 20.6h15.4a2 2 0 0 0 1.7-3L13.7 4.2a2 2 0 0 0-3.4 0z"/><path d="M12 9.5v4.2M12 17v.1"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "upload": '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/>',
    "logout": '<path d="M15 4h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3M10 17l-5-5 5-5M5 12h11"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2 2M14.5 8.5l2 2"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "hash": '<path d="M5 9h14M5 15h14M10 4 8 20M16 4l-2 16"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5"/>',
}
GITHUB = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>'
def i(name, cls="", sw="1.8"):
    return ico(I[name], cls, sw)
def line_chart(values, labels, highlight=9, cls="h-[220px] sm:h-[260px]"):
    hi = max(values) * 1.15
    n = len(values)
    X = lambda k: k * 100 / (n - 1)
    Y = lambda v: 100 - v / hi * 100
    pts = [(X(k), Y(v)) for k, v in enumerate(values)]
    d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"
    for k in range(n - 1):
        p0 = pts[k - 1] if k else pts[k]; p1 = pts[k]; p2 = pts[k + 1]; p3 = pts[k + 2] if k + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}"
    area = d + f" L{pts[-1][0]:.2f},100 L{pts[0][0]:.2f},100 Z"
    ticks = [v for v in (10000, 20000, 30000, 40000, 50000) if v < hi]
    grid = "".join(f'<line x1="0" x2="100" y1="{Y(v):.2f}" y2="{Y(v):.2f}" vector-effect="non-scaling-stroke" class="stroke-[color:var(--k-seam)]"/>' for v in ticks)
    gl = "".join(f'<span class="absolute right-full pr-2 -translate-y-1/2 text-xs text-ink-2 tabular-nums" style="top:{Y(v):.2f}%">${v//1000}k</span>' for v in ticks)
    xl = "".join(f'<span class="absolute -translate-x-1/2 text-xs text-ink-2{"" if k % 3 == 2 else " max-sm:hidden"}" style="left:{X(k):.2f}%">{l}</span>' for k, l in enumerate(labels))
    hx, hy = pts[highlight]
    return f'''<div class="relative ml-10 mt-3 mb-8 {cls}" role="img" aria-label="Revenue by month, November 2025 to October 2026. October $44,900; peak $48,210 in August.">
  <svg viewBox="0 0 100 100" preserveAspectRatio="none" class="absolute inset-0 size-full overflow-visible" aria-hidden="true">
    <defs><linearGradient id="fillg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".10"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>
    <g fill="none">{grid}</g>
    <path d="{area}" fill="url(#fillg)" class="text-ink"/>
    <path d="{d}" fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke" class="text-ink" stroke-linejoin="round" stroke-linecap="round"/>
    <line x1="{hx:.2f}" x2="{hx:.2f}" y1="{hy:.2f}" y2="100" stroke="currentColor" vector-effect="non-scaling-stroke" class="text-ink" stroke-dasharray="2 3"/>
  </svg>
  <span class="absolute size-3.5 -translate-1/2 rounded-full bg-ink border-[2.5px] border-[color:var(--k-housing)]" style="left:{hx:.2f}%;top:{hy:.2f}%" aria-hidden="true"></span>
  <div aria-hidden="true">{gl}</div>
  <div class="absolute inset-x-0 top-full pt-2" aria-hidden="true">{xl}</div>
</div>'''

def bar_chart(values, labels, label, current=-1, w=360, h=190):
    n, hi = len(values), max(values)
    cur = current % n
    bars = "".join(f'<div class="bar" style="--v:{v / hi * 100:.1f}%"{" data-current" if k == cur else ""}><span>{v}</span></div>' for k, v in enumerate(values))
    axis = "".join(f'<span{" data-current" if k == cur else ""}>{l}</span>' for k, l in enumerate(labels))
    return (f'<div class="bar-chart" style="--chart-h:{h - 40}px" role="img" aria-label="{label}">{bars}</div>'
            f'<div class="bar-chart-axis" aria-hidden="true">{axis}</div>')

def donut(segments, total, caption, label, r=54, sw=14):
    import math
    c = 2 * math.pi * r; s = sum(v for _, v, _ in segments); gap = 3; off = 0; arcs = ""
    for name, v, lamp in segments:
        ln = c * v / s
        arcs += f'<circle class="chart-seg {lamp}" cx="70" cy="70" r="{r}" stroke-width="{sw}" stroke-dasharray="{max(ln - gap, 0.1):.2f} {c:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 70 70)"/>'
        off += ln
    return (f'<svg class="chart" viewBox="0 0 140 140" role="img" aria-label="{label}"><circle class="chart-track" cx="70" cy="70" r="{r}" stroke-width="{sw}"/>{arcs}'
            f'<text class="chart-total" x="70" y="70" text-anchor="middle">{total}</text><text class="chart-caption" x="70" y="89" text-anchor="middle">{caption}</text></svg>')

def sparkline(values, w=120, h=32):
    lo, hi = min(values), max(values)
    pts = " ".join(f"{k * w / (len(values) - 1):.1f},{h - 3 - (v - lo) / (hi - lo) * (h - 6):.1f}" for k, v in enumerate(values))
    return f'<svg class="sparkline" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true"><polyline points="{pts}"/></svg>'

MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
REV = [21400, 23800, 22100, 27300, 26100, 31800, 30200, 36900, 34100, 48210, 41800, 44900]

I.update({
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
})

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{extra}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400..800&family=Geist+Mono:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}dist.css">
<link rel="icon" href="{root}favicon.ico" sizes="32x32">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<script>(function(){{var r=document.documentElement,h=null;try{{h=localStorage.getItem('plastc-housing')}}catch(e){{}}if(h!=='light'&&h!=='dark'){{var t=r.getAttribute('data-theme');h=(t==='dark'||(!t&&matchMedia('(prefers-color-scheme: dark)').matches))?'dark':'light'}}r.dataset.housing=h}})();</script>
</head>
"""
FOOT = """<div id="live" class="sr-only" aria-live="polite"></div>
<div id="toast" class="toast" popover="manual" role="status"><span data-toast-text></span><span class="sr-only" data-toast-hint></span><button type="button" class="lcd-action" data-toast-undo>Undo</button></div>
<script src="{root}plastc.js"></script>
</body>
</html>
"""

SITE = "https://plastc.space.fast"
DESCRIPTION = "Plastc is a neumorphic UI library for Tailwind CSS v4: components, app screens and tokens in one CSS file, with light and dark themes and contrast checked against WCAG 2 and APCA."
SCREEN_DESCRIPTION = "A reference screen built with Plastc, a neumorphic UI library for Tailwind CSS v4. Sample data only."

def page(path, title, body, root="", description=SCREEN_DESCRIPTION, extra=""):
    (HERE / path).parent.mkdir(parents=True, exist_ok=True)
    (HERE / path).write_text(HEAD.format(title=title, root=root, description=description, extra=extra) + body + FOOT.format(root=root))

def housing_seg(extra=""):
    return f'''<div class="seg {extra}" role="group" aria-label="Appearance">
  <button type="button" class="!px-3" data-set-housing="light" aria-pressed="true" aria-label="Light">{i("sun", "w-4 h-4")}</button>
  <button type="button" class="!px-3" data-set-housing="dark" aria-pressed="false" aria-label="Dark">{i("moon", "w-4 h-4")}</button>
</div>'''

def mark(root="", size="w-10 h-10 -m-1.5"):
    return (f'<img src="{root}mark-light.svg" alt="" class="{size} shrink-0 [[data-housing=dark]_&]:hidden">'
            f'<img src="{root}mark-dark.svg" alt="" class="{size} shrink-0 hidden [[data-housing=dark]_&]:block">')
def wordmark(href, root="../"):
    return f'<a href="{href}" class="flex items-center gap-2.5 no-underline text-ink font-extrabold tracking-[-0.02em] text-[17px]">{mark(root)}Plastc</a>'

SKIP = '<a href="#main" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 btn btn-sm">Skip to content</a>'

# ------------------------------------------------------------------ data
EXP = ' aria-expanded="true"'
CUR = ' aria-current="page"'
CUSTOMERS = [
    ("INV-0193", "Halden Studio", "HS", "Oct 28, 2026", "Paid", "ok", 4820.00),
    ("INV-0192", "Ortiz & Lane", "OL", "Oct 27, 2026", "Paid", "ok", 1240.50),
    ("INV-0191", "Northwind Co-op", "NC", "Oct 12, 2026", "Overdue", "danger", 9300.00),
    ("INV-0190", "Priya Nair", "PN", "Oct 09, 2026", "Open", "warn", 612.00),
    ("INV-0189", "Brightwater Labs", "BL", "Oct 04, 2026", "Paid", "ok", 2275.00),
    ("INV-0188", "Fenwick & Daughters", "FD", "Sep 30, 2026", "Overdue", "danger", 3140.00),
    ("INV-0187", "Tamsin Reyes", "TR", "Sep 26, 2026", "Paid", "ok", 860.00),
    ("INV-0186", "Kettle Hill Bakery", "KH", "Sep 21, 2026", "Open", "warn", 415.25),
    ("INV-0185", "Alder Robotics", "AR", "Sep 18, 2026", "Paid", "ok", 12600.00),
    ("INV-0184", "Juno Park", "JP", "Sep 11, 2026", "Open", "warn", 1980.00),
]
money = lambda v: f"${v:,.2f}"

def row_menu(inv):
    mid = "m-" + inv.lower()
    return f'''<button class="btn btn-quiet btn-sm btn-icon" popovertarget="{mid}" style="anchor-name:--{mid}" aria-label="Actions for {inv}">{i("dots")}</button>
<div class="menu" popover id="{mid}" style="position-anchor:--{mid}" aria-label="{inv} actions">
  <a href="#">{i("file")}View invoice</a>
  <button type="button" data-toast="Reminder sent for {inv}">{i("send")}Send reminder</button>
  <button type="button" data-toast="{inv} duplicated as a draft">{i("copy")}Duplicate</button>
  <hr>
  <button type="button" class="!text-danger" data-void="{inv}">{i("trash")}Void invoice</button>
</div>'''

def table(rows, select=True, actions=True, dates=True, selected=()):
    head = ('<th class="w-10"><label class="grid place-items-center size-9 -m-2 cursor-pointer"><input type="checkbox" class="check" data-select-all aria-label="Select all invoices"></label></th>' if select else '') + \
        '<th class="hidden sm:table-cell">Invoice</th><th>Customer</th>' + ('<th class="hidden md:table-cell">Issued</th>' if dates else '') + '<th>Status</th><th class="num hidden sm:table-cell">Amount</th>' + \
        ('<th class="w-12"><span class="sr-only">Actions</span></th>' if actions else '')
    body = []
    for inv, name, ini, date, st, lamp, amt in rows:
        sel = ' checked' if inv in selected else ''
        body.append(f'''<tr data-status="{st.lower()}">
  {f'<td><label class="grid place-items-center size-9 -m-2 cursor-pointer"><input type="checkbox" class="check" data-row-select aria-label="Select {inv}"{sel}></label></td>' if select else ''}
  <td class="hidden sm:table-cell font-semibold">{inv}</td>
  <td><div class="flex items-center gap-3"><span class="avatar !w-8 !h-8 !text-[11px] !hidden sm:!inline-grid">{ini}</span><span><span class="block">{name}</span><span class="block sm:hidden text-[13px] text-ink-2 tabular-nums">{money(amt)}</span></span></div></td>
  {f'<td class="hidden md:table-cell text-ink-2">{date}</td>' if dates else ''}
  <td><span class="badge lamp-{lamp}">{st}</span></td>
  <td class="num font-semibold hidden sm:table-cell">{money(amt)}</td>
  {f'<td>{row_menu(inv)}</td>' if actions else ''}
</tr>''')
    return f'<table class="ktable">\n<thead><tr>{head}</tr></thead>\n<tbody>{"".join(body)}</tbody></table>'

def lcd_empty(n, unit):
    return f'<div class="lcd readout"><span class="readout-value">{n}</span><span class="readout-unit">{unit}</span></div>'

# ------------------------------------------------------------------ dialogs shared by app screens
NEW_INVOICE = f'''<dialog class="dialog" id="new-invoice" aria-labelledby="ni-h">
  <form method="dialog" class="grid gap-5" data-toast-on-submit="Draft invoice created">
    <div class="flex items-start justify-between gap-4"><div><h2 id="ni-h" class="text-lg font-bold">New invoice</h2><p class="text-sm text-ink-2 mt-1">Start a draft. You can add line items next.</p></div><button type="button" class="btn btn-quiet btn-sm btn-icon" data-close-dialog aria-label="Close">{i("x")}</button></div>
    <div><label class="label" for="ni-c">Customer</label><select id="ni-c" class="field field-select" autofocus><option>Halden Studio</option><option>Northwind Co-op</option><option>Juno Park</option></select></div>
    <div class="grid grid-cols-2 gap-4"><div><label class="label" for="ni-a">Amount</label><input id="ni-a" class="field" inputmode="decimal" placeholder="0.00"></div><div><label class="label" for="ni-d">Due in</label><select id="ni-d" class="field field-select"><option>14 days</option><option selected>30 days</option></select></div></div>
    <div class="flex justify-end gap-3 pt-1"><button type="button" class="btn" data-close-dialog>Cancel</button><button class="btn btn-signal" value="ok">Create draft</button></div>
  </form>
</dialog>
<dialog class="dialog" id="void-invoice" aria-labelledby="vi-h">
  <form method="dialog" class="grid gap-4">
    <h2 id="vi-h" class="text-lg font-bold">Void <span data-void-label>this invoice</span>?</h2>
    <p class="text-sm text-ink-2">The customer can no longer pay it, and it leaves your outstanding total. You can undo this for a few seconds.</p>
    <div class="flex justify-end gap-3 pt-2"><button type="button" class="btn" data-close-dialog autofocus>Keep invoice</button><button class="btn btn-danger" value="void" data-void-confirm>{i("trash")}Void invoice</button></div>
  </form>
</dialog>'''

# ------------------------------------------------------------------ app shell
NAV = [("dashboard", "Dashboard", "home"), ("invoices", "Invoices", "file"), ("customers", "Customers", "users"),
       ("reports", "Reports", "chart"), ("products", "Products", "box")]

def nav_block(active):
    items = "".join(
        f'<a class="nav-item" href="{k}.html"{CUR if k == active else ""}>{i(ic)}{label}'
        + ('<span class="ml-auto text-[12px] font-semibold text-danger"><span data-nav-count="overdue">2</span> overdue</span>' if k == "invoices" else '') + '</a>'
        for k, label, ic in NAV)
    return f'''<nav class="flex flex-col gap-1" aria-label="Main">{items}</nav>
    <div class="mt-auto flex flex-col gap-1 pt-6">
      <a class="nav-item" href="settings.html"{CUR if active == "settings" else ""}>{i("cog")}Settings</a>
      <a class="nav-item" href="../index.html#install" target="_top">{i("help")}Docs</a>
      <div class="flex items-center justify-between gap-3 px-3 py-3 mt-2"><span class="text-sm font-semibold text-ink-2">Appearance</span>{housing_seg()}</div>
      <div class="flex items-center gap-3 px-2 pt-4 border-t border-[color:var(--k-seam)]">
        <span class="avatar">MO</span>
        <div class="min-w-0 text-sm leading-tight"><p class="font-bold truncate">Mira Okafor</p><p class="text-ink-2 truncate">mira@halden.studio</p></div>
        <a href="sign-in.html" class="btn btn-quiet btn-sm btn-icon ml-auto" aria-label="Sign out">{i("logout")}</a>
      </div>
    </div>'''

def command_dialog(groups, placeholder="Search or jump to…"):
    body, n = "", 0
    for gi, (label, items) in enumerate(groups):
        opts = ""
        for icon, text, attrs, kbd in items:
            n += 1
            tag = "a" if "href=" in attrs else "div"
            key = f'<span class="kbd">{kbd}</span>' if kbd else ""
            opts += f'<{tag} role="option" id="cmd-o{n}" tabindex="-1" {attrs}>{i(icon)}<span>{text}</span>{key}</{tag}>'
        body += f'<div role="group" aria-labelledby="cmd-l{gi}"><p class="listbox-label" id="cmd-l{gi}">{label}</p>{opts}</div>'
    return f'''<dialog class="dialog command" id="command" aria-label="Command menu">
  <label class="input-group">{i("search")}<span class="sr-only">Search commands</span><input role="combobox" aria-expanded="true" aria-controls="command-list" aria-autocomplete="list" autocomplete="off" placeholder="{placeholder}"><span class="kbd" aria-hidden="true">esc</span></label>
  <div class="listbox" role="listbox" id="command-list" aria-label="Commands">{body}<p class="listbox-empty" hidden>No results. Try a page name or an action.</p></div>
  <div class="command-hints" aria-hidden="true"><span><span class="kbd">↑</span><span class="kbd">↓</span>to move</span><span><span class="kbd">↵</span>to open</span><span><span class="kbd">esc</span>to close</span></div>
</dialog>'''

HOUSING_CMD = ("moon", '<span data-housing-next>Switch to dark</span>', 'data-command="housing"', "")

def search():
    return f'''<label class="input-group">{i("search")}<span class="sr-only">Search</span><input placeholder="Search" data-search><span class="kbd" aria-hidden="true">/</span></label>'''

def shell(active, title, sub, actions, content):
    return f'''<body class="min-h-screen">
{SKIP}
<header class="lg:hidden sticky top-0 z-30 flex items-center gap-3 px-4 py-3 bg-housing border-b border-[color:var(--k-seam)]">
  <button class="btn btn-sm btn-icon" data-open-dialog="nav-sheet" aria-label="Open navigation">{i("menu")}</button>
  {wordmark("dashboard.html")}
</header>
<dialog class="sheet" id="nav-sheet" aria-label="Navigation">
  <div class="flex flex-col h-full gap-6">
    <div class="flex items-center justify-between">{wordmark("dashboard.html")}<button class="btn btn-quiet btn-sm btn-icon" data-close-dialog aria-label="Close navigation">{i("x")}</button></div>
    {nav_block(active)}
  </div>
</dialog>
<div class="flex min-h-screen">
  <aside class="hidden lg:flex sticky top-0 h-screen overflow-y-auto w-[272px] shrink-0 flex-col gap-6 px-4 py-6 border-r border-[color:var(--k-seam)] shadow-[1px_0_0_rgb(var(--k-hl)/calc(.6*var(--k-hl-a)))]">
    <div class="px-2">{wordmark("dashboard.html")}</div>
    {search()}
    {nav_block(active)}
  </aside>
  <main id="main" class="flex-1 min-w-0 px-4 py-6 sm:px-6 md:px-10 md:py-9">
    <header class="flex flex-wrap items-end gap-4 justify-between pb-7">
      <div><h1 class="text-[26px] md:text-[30px] font-bold tracking-[-0.015em] leading-tight">{title}</h1><p class="text-ink-2 mt-1">{sub}</p></div>
      <div class="flex flex-wrap gap-3">{actions}</div>
    </header>
    {content}
    <p class="text-xs text-ink-2 mt-10">Sample data for demonstration. Plastc reference screen.</p>
  </main>
</div>
{NEW_INVOICE}
{command_dialog([
    ("Go to", [(ic, label, f'href="{k}.html"', "") for k, label, ic in NAV] + [("cog", "Settings", 'href="settings.html"', "")]),
    ("Actions", [("plus", "New invoice", 'data-open-dialog="new-invoice"', "N"), HOUSING_CMD, ("logout", "Sign out", 'href="sign-in.html"', ""), ("left", "Back to Plastc", 'href="../index.html" target="_top"', "")]),
])}
'''

NEW_BTN = f'<span class="tooltip" data-tip="Shortcut: N"><button class="btn btn-signal" data-open-dialog="new-invoice" aria-keyshortcuts="N">{i("plus","", "2.2")}New invoice</button></span>'

# ------------------------------------------------------------------ dashboard
def attention(ini, name, status, lamp, amt, action):
    return f'''<li class="flex items-center gap-3 py-3.5"><span class="avatar !w-9 !h-9 !text-xs shrink-0">{ini}</span><div class="min-w-0 flex-1"><p class="font-semibold text-sm truncate">{name}</p><p class="mt-1"><span class="badge {lamp} !font-semibold !text-[13px] !text-ink-2 whitespace-nowrap">{status}</span></p></div><div class="flex flex-col items-end gap-1.5 shrink-0"><p class="font-semibold text-sm tabular-nums">{amt}</p>{action}</div></li>'''

dash = shell("dashboard", "Welcome back, Mira", "Here’s how invoicing is tracking this month.",
    f'<button class="btn" data-toast="Export started. We’ll email the CSV.">{i("down")}Export</button>{NEW_BTN}',
    f'''
<section class="lcd px-6 py-5 grid gap-5 sm:grid-cols-3 sm:gap-0 sm:divide-x divide-[color:rgb(0_0_0/0.14)]" aria-label="Key figures for October">
  <div class="sm:pr-6"><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Revenue · Oct</p><p class="text-[32px] font-semibold leading-none mt-2 tracking-[-0.02em]">$44,900</p><p class="text-xs mt-2">▲ 7.4% vs Sep</p></div>
  <div class="sm:px-6"><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Outstanding</p><p class="text-[32px] font-semibold leading-none mt-2 tracking-[-0.02em]">$15,447</p><p class="text-xs mt-2">2 of 5 overdue</p></div>
  <div class="sm:pl-6"><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Avg. days to pay</p><p class="text-[32px] font-semibold leading-none mt-2 tracking-[-0.02em]">18.2</p><p class="text-xs mt-2">▼ 2.1 days faster</p></div>
</section>

<div class="grid gap-6 xl:grid-cols-[1.6fr_1fr] mt-8 [&>*]:min-w-0">
  <section class="panel !p-5 sm:!p-6 flex flex-col" aria-labelledby="rev-h">
    <div class="flex flex-wrap items-center gap-3 justify-between mb-5">
      <div><h2 id="rev-h" class="font-bold">Revenue</h2><p class="text-sm text-ink-2">Paid invoices by month</p></div>
      <p class="text-sm text-ink-2 tabular-nums">Nov 2025 – Oct 2026</p>
    </div>
    {line_chart(REV, MONTHS, highlight=11, cls="h-[220px] sm:h-[260px] xl:h-auto xl:flex-1 xl:min-h-[220px]")}
  </section>
  <section class="panel !p-5 sm:!p-6" aria-labelledby="att-h">
    <div class="flex items-center justify-between mb-2"><h2 id="att-h" class="font-bold">Needs attention</h2><a href="invoices.html" class="btn btn-quiet btn-sm">View all</a></div>
    <ul class="divide-y divide-[color:var(--k-seam)]">
      {attention("NC", "Northwind Co-op", "22 days overdue", "lamp-danger", "$9,300.00", '<button class="btn btn-sm" data-toast="Reminder sent to Northwind Co-op">Remind</button>')}
      {attention("FD", "Fenwick &amp; Daughters", "34 days overdue", "lamp-danger", "$3,140.00", '<button class="btn btn-sm" data-toast="Reminder sent to Fenwick &amp; Daughters">Remind</button>')}
      {attention("JP", "Juno Park", "Due in 3 days", "lamp-warn", "$1,980.00", '<button class="btn btn-sm btn-quiet" data-toast="Snoozed until Friday">Snooze</button>')}
    </ul>
    <div class="mt-4">
      <div class="flex justify-between gap-3 text-[13px] mb-2"><span class="font-semibold">Collected this quarter</span><span class="text-ink-2 tabular-nums">$112,400 of $140,000</span></div>
      <div class="meter" role="meter" aria-valuemin="0" aria-valuemax="140000" aria-valuenow="112400" aria-label="Collected this quarter"><span style="--v:80%"></span></div>
    </div>
  </section>
</div>

<section class="panel !p-0 mt-8" aria-labelledby="recent-h">
  <div class="flex flex-wrap items-center justify-between gap-3 px-5 sm:px-6 pt-5 pb-3">
    <h2 id="recent-h" class="font-bold">Recent invoices</h2>
    <a class="btn btn-sm" href="invoices.html">All invoices{i("right")}</a>
  </div>
  <div class="table-scroll px-2 pb-2">{table(CUSTOMERS[:6], select=False)}</div>
</section>
''')
page("screens/dashboard.html", "Dashboard · Plastc", dash, "../")

# ------------------------------------------------------------------ invoices
inv = shell("invoices", "Invoices", "Create, send and track every invoice in one place.",
    f'<button class="btn" data-toast="Import is not part of this demo">{i("down")}Import</button>{NEW_BTN}',
    f'''
<div class="flex flex-wrap items-center gap-3 justify-between mb-5">
  <div class="seg" role="tablist" aria-label="Filter by status" data-filter-tabs>
    <button role="tab" aria-selected="true" data-filter="all">All <span class="text-ink-2 font-semibold" data-count="all">{len(CUSTOMERS)}</span></button>
    <button role="tab" aria-selected="false" data-filter="paid">Paid</button><button role="tab" aria-selected="false" data-filter="open">Open</button>
    <button role="tab" aria-selected="false" data-filter="overdue">Overdue <span class="text-danger" data-count="overdue">2</span></button><button role="tab" aria-selected="false" data-filter="draft">Draft</button>
  </div>
  <div class="flex gap-3 flex-1 sm:flex-none min-w-0">
    <label class="input-group flex-1 sm:w-72 min-w-0">{i("search")}<span class="sr-only">Search invoices</span><input placeholder="Search by customer or number" data-search data-table-search></label>
    <button class="btn btn-icon sm:!w-auto sm:!px-4" popovertarget="range-menu" style="anchor-name:--range-menu" aria-label="Date range: Sep 1 to Oct 31" data-range-btn>{i("cal")}<span class="hidden sm:inline" data-range-label>Sep 1 – Oct 31</span></button>
    <div class="menu" popover id="range-menu" style="position-anchor:--range-menu" aria-label="Date range"><button type="button" data-range="Last 30 days">Last 30 days</button><button type="button" data-range="Sep 1 – Oct 31">Sep 1 – Oct 31</button><button type="button" data-range="This quarter">This quarter</button><button type="button" data-range="This year">This year</button></div>
  </div>
</div>

<div class="alert mb-5" role="status" data-bulk-bar hidden>{i("info")}<div class="alert-body"><b data-bulk-count>0 invoices selected.</b> <span class="text-ink-2">Send reminders or export them together.</span></div><div class="alert-actions"><button class="btn btn-sm btn-quiet" data-clear-selection>Clear</button><button class="btn btn-sm" data-toast="Export started">Export</button><button class="btn btn-sm btn-go" data-bulk-remind>{i("send")}Send reminders</button></div></div>

<section class="panel !p-0">
  <div class="table-scroll px-2 pt-1" data-table-wrap>{table(CUSTOMERS)}</div>
  <div class="empty" data-empty hidden>
    <div class="lcd readout"><span class="readout-value">0</span><span class="readout-unit" data-empty-unit>Drafts</span></div>
    <h2 data-empty-title>Nothing waiting to send</h2>
    <p data-empty-text>Invoices you start but don’t send wait here. Everything you’ve started has gone out.</p>
    <button class="btn btn-sm" data-open-dialog="new-invoice" data-empty-new>{i("plus","", "2.2")}Start a draft</button>
    <button class="btn btn-sm" data-clear-search hidden>{i("x")}Clear search</button>
  </div>
  <nav class="pager px-5 sm:px-6 py-4 border-t border-[color:var(--k-seam)]" aria-label="Pagination" data-pager>
    <button class="btn btn-sm" disabled>{i("left")}Previous</button>
    <p class="pager-status" data-showing>Showing all 10 invoices</p>
    <button class="btn btn-sm" disabled>Next{i("right")}</button>
  </nav>
</section>
''')
page("screens/invoices.html", "Invoices · Plastc", inv, "../")

# ------------------------------------------------------------------ settings
def row(label, help_, field):
    return f'''<div class="grid gap-4 md:grid-cols-[260px_1fr] py-6 border-b border-[color:var(--k-seam)] shadow-[0_1px_0_rgb(var(--k-hl)/calc(.5*var(--k-hl-a)))] last:border-0 last:shadow-none">
  <div><p class="text-sm font-bold">{label}</p><p class="text-sm text-ink-2 mt-1">{help_}</p></div><div class="max-w-[560px] min-w-0">{field}</div></div>'''

notif = "".join(f'''<label class="flex items-start gap-3.5 py-2.5"><input type="checkbox" role="switch" class="switch mt-0.5"{" checked" if on else ""}><span><span class="block text-sm font-semibold">{t}</span><span class="block text-sm text-ink-2">{d}</span></span></label>'''
    for t, d, on in [("Invoice paid", "When a customer pays in full.", True), ("Invoice overdue", "The morning after a due date passes.", True), ("Weekly summary", "Mondays at 9:00, your local time.", False)])

plans = "".join(f'''<label class="choice-card"><input type="radio" name="plan" class="radio mt-0.5"{" checked" if sel else ""}><span class="flex-1"><span class="flex justify-between gap-3 text-sm font-bold"><span>{t}</span><span class="tabular-nums">{p}</span></span><span class="block text-sm text-ink-2 mt-0.5">{d}</span></span></label>'''
    for t, p, d, sel in [("Studio", "$12 / mo", "Up to 3 people and 200 invoices a month.", True), ("Practice", "$29 / mo", "Unlimited invoices, reminders and exports.", False)])

team = "".join(f'<tr><td><div class="flex items-center gap-3"><span class="avatar !w-8 !h-8 !text-[11px]">{a}</span><div><p class="font-semibold">{n}</p><p class="text-ink-2 text-[13px]">{e}</p></div></div></td><td><span class="tag">{r}</span></td></tr>'
    for a, n, e, r in [("MO", "Mira Okafor", "mira@halden.studio", "Owner"), ("DS", "Dev Sharma", "dev@halden.studio", "Admin"), ("LW", "Lena Wolff", "lena@halden.studio", "Member")])

def tabpanel(id_, label, body, hidden=False):
    return f'<div role="tabpanel" id="tp-{id_}" aria-labelledby="tab-{id_}"{" hidden" if hidden else ""}>{body}</div>'

TI = ' tabindex="-1"'
TABS = [("profile", "Profile"), ("notifications", "Notifications"), ("billing", "Billing"), ("team", "Team"), ("api", "API")]
tabs = "".join(f'<button role="tab" id="tab-{k}" aria-controls="tp-{k}" aria-selected="{"true" if n == 0 else "false"}"{TI if n else ""}>{l}</button>' for n, (k, l) in enumerate(TABS))

settings = shell("settings", "Settings", "Manage your studio profile, team and billing.", "", f'''
<div class="tabs mb-6" role="tablist" aria-label="Settings sections">{tabs}</div>
<section class="panel !px-5 !py-2 md:!px-8">
  {tabpanel("profile", "Profile", f"""
  {row("Studio name", "Shown on every invoice you send.", '<label class="sr-only" for="sn">Studio name</label><input id="sn" class="field" value="Halden Studio">')}
  {row("Billing email", "Where customers reply to invoices.", '<label class="sr-only" for="em">Billing email</label><input id="em" class="field" type="email" value="billing@halden.studio" aria-describedby="em-e"><span id="em-e" class="hint-error" hidden>Add the domain, for example billing@halden.studio.</span>')}
  {row("Logo", "SVG, PNG or JPG. At least 400 × 400 px.", f'<div class="flex items-center gap-5"><span class="avatar !w-16 !h-16 !text-lg">HS</span><label class="dropzone flex-1" data-dropzone>{i("upload")}<span><strong>Click to upload</strong> or drag and drop</span><input type="file" class="sr-only" accept="image/*"></label></div>')}
  {row("Default terms", "Applied to new invoices. You can change them per invoice.", '<div class="grid sm:grid-cols-2 gap-4"><div><label class="label" for="due">Payment due</label><select id="due" class="field field-select"><option>14 days</option><option selected>30 days</option><option>45 days</option></select></div><div><label class="label" for="cur">Currency</label><select id="cur" class="field field-select"><option>USD — US Dollar</option><option>EUR — Euro</option></select></div></div><label class="label mt-4" for="note">Footer note</label><textarea id="note" class="field field-area" maxlength="240">Thanks for working with us. Bank details are on page two.</textarea><span class="hint">Shown at the bottom of every invoice. 240 characters max.</span>')}
  """)}
  {tabpanel("notifications", "Notifications", row("Email me when", "Choose what lands in your inbox.", notif), True)}
  {tabpanel("billing", "Billing", row("Plan", "Billed monthly. Change any time.", f'<div class="grid gap-3" role="radiogroup" aria-label="Plan">{plans}</div>') + row("Card", "Charged on the 1st of each month.", '<p class="text-sm"><span class="font-semibold">Visa ending 4242</span> <span class="text-ink-2">· expires 08/28</span></p><button class="btn btn-sm mt-3">Update card</button>'), True)}
  {tabpanel("team", "Team", row("Members", "People who can create and send invoices.", f'<div class="table-scroll"><table class="ktable"><thead><tr><th>Name</th><th>Role</th></tr></thead><tbody>{team}</tbody></table></div><button class="btn btn-sm mt-4" data-toast="Invite link copied">{i("plus","", "2.2")}Invite someone</button>'), True)}
  {tabpanel("api", "API", row("API keys", "For connecting your own tools to Plastc.", f'<div class="flex flex-col items-start gap-4">{lcd_empty(0, "Keys")}<p class="text-sm text-ink-2">You haven’t created a key yet. Keys can read and create invoices.</p><button class="btn btn-sm" data-toast="Key created. Copy it now: it won’t be shown again.">{i("key")}Create key</button></div>'), True)}
  <div class="flex justify-end gap-3 py-6 border-t border-[color:var(--k-seam)]"><button class="btn" data-settings-cancel>Cancel</button><button class="btn btn-signal" data-settings-save>Save changes</button></div>
</section>
''')
page("screens/settings.html", "Settings · Plastc", settings, "../")

# ------------------------------------------------------------------ customers, reports, products
def money(v, cents=True):
    return f"${v:,.2f}" if cents else f"${v:,.0f}"

def row_actions(rid, label, items):
    body = "".join(items)
    return (f'<button class="btn btn-quiet btn-sm btn-icon" popovertarget="{rid}" style="anchor-name:--{rid}" aria-label="Actions for {label}">{i("dots")}</button>'
            f'<div class="menu" popover id="{rid}" style="position-anchor:--{rid}">{body}</div>')

def filter_toolbar(table_id, placeholder, segs):
    seg = "".join(f'<button type="button" aria-pressed="{"true" if n == 0 else "false"}" data-row-filter="{k}">{l}<span class="hidden sm:inline text-ink-2 font-semibold">{c}</span></button>' for n, (k, l, c) in enumerate(segs))
    return f'''<div class="flex flex-wrap items-center gap-3 justify-between mb-5">
  <div class="seg" role="group" aria-label="Filter" data-filter-for="{table_id}">{seg}</div>
  <label class="input-group flex-1 sm:flex-none sm:w-72 min-w-0">{i("search")}<span class="sr-only">Search</span><input placeholder="{placeholder}" data-filter-for="{table_id}"></label>
</div>'''

def filter_empty(table_id, unit):
    return f'''<div class="empty" data-empty-for="{table_id}" hidden>
    <div class="lcd readout"><span class="readout-value">0</span><span class="readout-unit">{unit}</span></div>
    <h2>Nothing matches</h2>
    <p>Check the spelling, or try another filter.</p>
    <button class="btn btn-sm" data-clear-filter="{table_id}">{i("x")}Clear search</button>
  </div>'''

CLIENTS = [
    ("Halden Studio", "HS", "billing@halden.studio", 24, 0, 64180, "Oct 28", "paid"),
    ("Ortiz & Lane", "OL", "accounts@ortizlane.com", 15, 0, 31480.50, "Oct 27", "paid"),
    ("Northwind Co-op", "NC", "finance@northwind.coop", 19, 9300, 71250, "Oct 12", "owes overdue"),
    ("Priya Nair", "PN", "priya@nair.design", 10, 612, 14210, "Oct 9", "owes"),
    ("Brightwater Labs", "BL", "ap@brightwater.io", 18, 0, 52300, "Oct 4", "paid"),
    ("Fenwick & Daughters", "FD", "office@fenwick.co", 12, 3140, 18900, "Sep 30", "owes overdue"),
    ("Tamsin Reyes", "TR", "tamsin@reyes.studio", 9, 0, 12600, "Sep 26", "paid"),
    ("Kettle Hill Bakery", "KH", "orders@kettlehill.co", 11, 415.25, 11449.50, "Sep 21", "owes"),
    ("Alder Robotics", "AR", "ap@alder-robotics.com", 22, 0, 96400, "Sep 18", "paid"),
    ("Juno Park", "JP", "juno@junopark.co", 11, 1980, 15840, "Sep 11", "owes"),
]

def client_row(n, c):
    name, ini, email, count, owed, billed, last, group = c
    if not owed: owed_cell = '<span class="text-ink-2">$0.00</span>'
    elif "overdue" in group: owed_cell = f'<div class="flex flex-col items-end gap-1"><span class="text-danger font-bold">{money(owed)}</span><span class="badge lamp-danger !text-[13px] !font-semibold !text-ink-2">Overdue</span></div>'
    else: owed_cell = f'<span class="font-semibold">{money(owed)}</span>'
    menu = row_actions(f"cm{n}", name, [
        f'<button type="button" data-open-dialog="new-invoice">{i("plus")}New invoice</button>',
        f'<button type="button" data-toast="Statement sent to {email}">{i("send")}Send statement</button>',
        '<hr>',
        f'<button type="button" data-toast="{name} archived">{i("box")}Archive</button>',
    ])
    return (f'<tr data-group="{group}"><td><div class="flex items-center gap-3"><span class="avatar !w-8 !h-8 !text-[11px]">{ini}</span>'
            f'<div class="min-w-0"><p class="font-semibold">{name}</p><p class="text-ink-2 text-[13px]">{email}</p></div></div></td>'
            f'<td class="hidden md:table-cell num">{count}</td><td class="num">{owed_cell}</td><td class="hidden md:table-cell num">{money(billed)}</td>'
            f'<td class="hidden md:table-cell text-ink-2 whitespace-nowrap">{last}</td><td class="w-12">{menu}</td></tr>')

ADD_CUSTOMER = f'''<dialog class="dialog" id="add-customer" aria-labelledby="ac-h">
  <form method="dialog" class="grid gap-5" data-toast-on-submit="Customer added">
    <div class="flex items-start justify-between gap-4"><div><h2 id="ac-h" class="text-lg font-bold">Add customer</h2><p class="text-sm text-ink-2 mt-1">Invoices and statements go to this address.</p></div><button type="button" class="btn btn-quiet btn-sm btn-icon" data-close-dialog aria-label="Close">{i("x")}</button></div>
    <div><label class="label" for="ac-n">Name</label><input id="ac-n" class="field" autocomplete="organization" autofocus></div>
    <div><label class="label" for="ac-e">Billing email</label><input id="ac-e" class="field" type="email" autocomplete="email"></div>
    <div class="flex justify-end gap-3 pt-1"><button type="button" class="btn" data-close-dialog>Cancel</button><button class="btn btn-signal" value="ok">Add customer</button></div>
  </form>
</dialog>'''

owes = sum(1 for c in CLIENTS if "owes" in c[7]); overdue = sum(1 for c in CLIENTS if "overdue" in c[7])
customers = shell("customers", "Customers", "Everyone you invoice, and what each of them owes.",
    f'<button class="btn" data-toast="Import is not part of this demo">{i("down")}Import</button><button class="btn btn-signal" data-open-dialog="add-customer">{i("plus","", "2.2")}Add customer</button>',
    f'''
{filter_toolbar("cust-table", "Search by name or email", [("all", "All", len(CLIENTS)), ("owes", "Owes money", owes), ("overdue", "Overdue", overdue), ("paid", "Paid up", len(CLIENTS) - owes)])}
<section class="panel !p-0">
  <div class="table-scroll px-2 pt-1"><table class="ktable" id="cust-table">
    <thead><tr><th>Customer</th><th class="hidden md:table-cell num">Invoices</th><th class="num">Owes</th><th class="hidden md:table-cell num">Billed this year</th><th class="hidden md:table-cell">Last invoice</th><th class="w-12"><span class="sr-only">Actions</span></th></tr></thead>
    <tbody>{"".join(client_row(n, c) for n, c in enumerate(CLIENTS))}</tbody>
  </table></div>
  {filter_empty("cust-table", "Matches")}
  <nav class="pager px-5 sm:px-6 py-4 border-t border-[color:var(--k-seam)]" aria-label="Pagination">
    <button class="btn btn-sm" disabled>{i("left")}Previous</button>
    <p class="pager-status" data-count-for="cust-table">Showing all {len(CLIENTS)} customers</p>
    <button class="btn btn-sm" disabled>Next{i("right")}</button>
  </nav>
</section>
{ADD_CUSTOMER}
''')
page("screens/customers.html", "Customers · Plastc", customers, "../")

INVOICES_SENT = [9, 10, 9, 12, 11, 13, 12, 14, 13, 16, 14, 18]
TOP = sorted(CLIENTS, key=lambda c: -c[5])[:5]
TOTAL = sum(c[5] for c in CLIENTS)
top_rows = "".join(
    f'<tr><td><div class="flex items-center gap-3"><span class="avatar !w-8 !h-8 !text-[11px]">{c[1]}</span><span class="font-semibold">{c[0]}</span></div></td>'
    f'<td class="hidden md:table-cell num">{c[3]}</td><td class="num">{money(c[5])}</td>'
    f'<td class="hidden sm:table-cell w-[28%] min-w-[120px]"><div class="flex items-center gap-3"><div class="meter flex-1" role="meter" aria-label="Share of revenue for {c[0]}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{c[5] / TOTAL * 100:.1f}"><span style="--v:{c[5] / TOTAL * 100 * 2.5:.1f}%"></span></div><span class="text-ink-2 tabular-nums text-[13px] w-12 text-right">{c[5] / TOTAL * 100:.1f}%</span></div></td></tr>'
    for c in TOP)

reports = shell("reports", "Reports", "How invoicing has gone over the last twelve months.",
    f'''<button class="btn" popovertarget="range-menu" style="anchor-name:--range-menu" aria-label="Date range: Last 12 months" data-range-btn>{i("cal")}<span data-range-label>Last 12 months</span></button>
    <div class="menu" popover id="range-menu" style="position-anchor:--range-menu" aria-label="Date range"><button type="button" data-range="Last 30 days">Last 30 days</button><button type="button" data-range="This quarter">This quarter</button><button type="button" data-range="Last 12 months">Last 12 months</button><button type="button" data-range="All time">All time</button></div>
    <button class="btn" data-toast="Export started. We’ll email the CSV.">{i("down")}Export</button>''',
    f'''
<section class="lcd px-6 py-5 grid gap-5 grid-cols-2 lg:grid-cols-4" aria-label="Key figures, last twelve months">
  {"".join(f'<div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">{k}</p><p class="text-[28px] font-semibold leading-none mt-2 tracking-[-0.02em]">{v}</p><p class="text-xs mt-2">{d}</p></div>' for k, v, d in (("Revenue", money(TOTAL, cents=False), "▲ 31% on the year before"), ("Invoices sent", str(sum(INVOICES_SENT)), "18 in October"), ("Avg. days to pay", "18.2", "▼ 2.1 days faster"), ("Paid on time", "86%", "of invoices due")))}
</section>

<section class="panel !p-5 sm:!p-6 mt-8" aria-labelledby="rr-h">
  <div class="flex flex-wrap items-center gap-3 justify-between mb-5"><div><h2 id="rr-h" class="font-bold">Revenue</h2><p class="text-sm text-ink-2">Paid invoices by month</p></div><p class="text-sm text-ink-2 tabular-nums">Nov 2025 – Oct 2026</p></div>
  {line_chart(REV, MONTHS, highlight=11)}
</section>

<div class="grid gap-6 lg:grid-cols-[1.5fr_1fr] mt-6 [&>*]:min-w-0">
  <section class="panel !p-5 sm:!p-6" aria-labelledby="rs-h">
    <h2 id="rs-h" class="font-bold">Invoices sent</h2><p class="text-sm text-ink-2">By month</p>
    <div class="mt-5 hidden sm:block">{bar_chart(INVOICES_SENT, MONTHS, "Invoices sent per month, November 2025 to October 2026. October: 18, the most in the year.", w=560, h=290)}</div>
    <div class="mt-5 sm:hidden">{bar_chart(INVOICES_SENT[6:], MONTHS[6:], "Invoices sent per month, May to October 2026. October: 18.")}</div>
  </section>
  <section class="panel !p-5 sm:!p-6" aria-labelledby="rd-h">
    <h2 id="rd-h" class="font-bold">By status</h2><p class="text-sm text-ink-2">Share of invoiced value this quarter</p>
    <div class="mt-5 flex flex-wrap items-center gap-6"><div class="w-[140px] shrink-0">{donut([("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")], "$63.8k", "invoiced", "Invoiced this quarter: $63,800. Paid 62%, open 21%, overdue 9%, draft 8%.")}</div>
    <ul class="grid gap-2 text-sm min-w-[150px] flex-1">{"".join(f'<li class="flex items-center justify-between gap-4"><span class="badge {l}">{n}</span><span class="tabular-nums text-ink-2">{p}%</span></li>' for n, p, l in (("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")))}</ul></div>
  </section>
</div>

<section class="panel !p-0 mt-6" aria-labelledby="rt-h">
  <div class="flex flex-wrap items-center justify-between gap-3 px-5 sm:px-6 pt-5 pb-3"><h2 id="rt-h" class="font-bold">Top customers</h2><a class="btn btn-sm" href="customers.html">All customers{i("right")}</a></div>
  <div class="table-scroll px-2 pb-2"><table class="ktable"><thead><tr><th>Customer</th><th class="hidden md:table-cell num">Invoices</th><th class="num">Billed</th><th class="hidden sm:table-cell">Share of revenue</th></tr></thead><tbody>{top_rows}</tbody></table></div>
</section>
''')
page("screens/reports.html", "Reports · Plastc", reports, "../")

PRODUCTS = [
    ("Brand identity", "Project", 6400, 9, "active"),
    ("Website design", "Project", 8200, 6, "active"),
    ("Design day", "Day", 950, 31, "active"),
    ("Consulting", "Hour", 140, 64, "active"),
    ("Print production", "Item", 380, 12, "active"),
    ("Monthly retainer", "Month", 1800, 14, "active"),
    ("Photography, half day", "Half day", 620, 3, "archived"),
]

def product_row(n, p):
    name, unit, price, used, group = p
    menu = row_actions(f"pm{n}", name, [
        f'<button type="button" data-open-dialog="add-product">{i("file")}Edit</button>',
        f'<button type="button" data-toast="{name} duplicated">{i("copy")}Duplicate</button>',
        '<hr>',
        f'<button type="button" data-toast="{name} {"restored" if group == "archived" else "archived"}">{i("box")}{"Restore" if group == "archived" else "Archive"}</button>',
    ])
    return (f'<tr data-group="{group}"{" hidden" if group == "archived" else ""}><td class="font-semibold">{name}</td><td class="hidden sm:table-cell"><span class="tag">{unit}</span></td>'
            f'<td class="num">{money(price)}</td><td class="hidden md:table-cell num">{used}</td><td class="w-12">{menu}</td></tr>')

ADD_PRODUCT = f'''<dialog class="dialog" id="add-product" aria-labelledby="ap-h">
  <form method="dialog" class="grid gap-5" data-toast-on-submit="Product saved">
    <div class="flex items-start justify-between gap-4"><div><h2 id="ap-h" class="text-lg font-bold">Product</h2><p class="text-sm text-ink-2 mt-1">Something you bill for. Add it to any invoice as a line item.</p></div><button type="button" class="btn btn-quiet btn-sm btn-icon" data-close-dialog aria-label="Close">{i("x")}</button></div>
    <div><label class="label" for="ap-n">Name</label><input id="ap-n" class="field" autofocus placeholder="Design day"></div>
    <div class="grid grid-cols-2 gap-4"><div><label class="label" for="ap-u">Unit</label><select id="ap-u" class="field field-select"><option>Hour</option><option selected>Day</option><option>Project</option><option>Item</option><option>Month</option></select></div>
    <div><label class="label" for="ap-p">Price</label><div class="input-group"><span class="input-affix">$</span><input id="ap-p" inputmode="decimal" placeholder="0.00"></div></div></div>
    <div class="flex justify-end gap-3 pt-1"><button type="button" class="btn" data-close-dialog>Cancel</button><button class="btn btn-signal" value="ok">Save product</button></div>
  </form>
</dialog>'''

active = sum(1 for p in PRODUCTS if p[4] == "active")
products = shell("products", "Products", "What you bill for, ready to drop into an invoice.",
    f'<button class="btn btn-signal" data-open-dialog="add-product">{i("plus","", "2.2")}Add product</button>',
    f'''
{filter_toolbar("prod-table", "Search products", [("active", "Active", active), ("archived", "Archived", len(PRODUCTS) - active)])}
<section class="panel !p-0">
  <div class="table-scroll px-2 pt-1"><table class="ktable" id="prod-table">
    <thead><tr><th>Name</th><th class="hidden sm:table-cell">Unit</th><th class="num">Price</th><th class="hidden md:table-cell num">On invoices</th><th class="w-12"><span class="sr-only">Actions</span></th></tr></thead>
    <tbody>{"".join(product_row(n, p) for n, p in enumerate(PRODUCTS))}</tbody>
  </table></div>
  {filter_empty("prod-table", "Matches")}
</section>
{ADD_PRODUCT}
''')
page("screens/products.html", "Products · Plastc", products, "../")

# ------------------------------------------------------------------ sign in
signin = f'''<body class="min-h-screen grid place-items-center px-4 py-12">
<main id="main" class="w-full max-w-[400px]">
  <div class="flex flex-col items-center text-center">
    {mark("../", "w-16 h-16 -m-2")}
    <h1 class="text-[28px] font-bold tracking-[-0.015em] mt-6">Sign in to Plastc</h1>
    <p class="text-ink-2 mt-1.5">Welcome back. Enter your details.</p>
  </div>
  <form class="mt-8 grid gap-5" novalidate data-signin>
    <div class="alert lamp-danger" role="alert" id="signin-err" hidden data-signin-error>{i("alert")}<div class="alert-body">That email and password don’t match. Check both, or reset your password.</div></div>
    <div><label class="label" for="e">Email</label><input id="e" class="field" type="email" autocomplete="email" placeholder="you@studio.com" required aria-describedby="e-err"><span id="e-err" class="hint-error" hidden>Enter the email you signed up with.</span></div>
    <div><label class="label" for="p">Password</label><input id="p" class="field" type="password" autocomplete="current-password" placeholder="Your password" required aria-describedby="p-err"><span id="p-err" class="hint-error" hidden>Enter your password.</span></div>
    <div class="flex flex-wrap items-center justify-between gap-3 text-sm"><label class="flex items-center gap-2.5 font-semibold"><input type="checkbox" class="check">Remember for 30 days</label><a href="#" class="font-bold text-ink underline py-1">Forgot password</a></div>
    <button type="submit" class="btn btn-signal btn-lg w-full">Sign in</button>
    <button type="button" class="btn btn-lg w-full">{i("key")}Sign in with SSO</button>
  </form>
  <p class="text-center text-sm text-ink-2 mt-8">Don’t have an account? <a href="#" class="font-bold text-ink">Sign up</a></p>
  <p class="text-center text-xs text-ink-2 mt-3">Demo: any email with the password “plastc” signs in. Anything else shows the error.</p>
  <div class="flex justify-center mt-8">{housing_seg()}</div>
</main>
'''
page("screens/sign-in.html", "Sign in · Plastc", signin, "../")


# ------------------------------------------------------------------ landing page (marketing sections)
LNAV = [("features", "Features"), ("pricing", "Pricing"), ("faq", "FAQ")]
PLANS = [
    ("Solo", "0", "0", "For your first few clients.", ["5 invoices a month", "Card and bank payments", "Automatic reminders"], False, "Start free"),
    ("Studio", "12", "120", "For a small team that bills every week.", ["Up to 3 people", "200 invoices a month", "Reminders and late fees", "CSV export"], True, "Start with Studio"),
    ("Practice", "29", "290", "For firms with many clients.", ["Unlimited people", "Unlimited invoices", "Your own domain for pay links", "Priority support"], False, "Start with Practice"),
]
plan_cards = "".join(f'''<article class="plan"{' data-featured' if feat else ''}>
  <div><div class="flex items-center justify-between gap-3"><h3 class="text-lg font-bold">{name}</h3>{'<span class="badge lamp-signal">Recommended</span>' if feat else ''}</div><p class="text-sm text-ink-2 mt-1">{blurb}</p></div>
  <p class="plan-price"><span data-price data-monthly="${mo}" data-yearly="${yr}">${mo}</span><small data-price-unit>/ month</small></p>
  <ul class="check-list">{"".join(f"<li>{x}</li>" for x in feats)}</ul>
  <a class="btn {'btn-signal' if feat else ''} w-full" href="sign-in.html">{cta}</a>
</article>''' for name, mo, yr, blurb, feats, feat, cta in PLANS)

FAQS = [
    ("Do my customers need an account?", "No. They get an email with a link to the invoice, and they can pay from there by card or bank transfer."),
    ("Can I bring invoices from another tool?", "Yes. Import a CSV export and your customers, invoices and their statuses come across together."),
    ("What happens when I void an invoice?", "The customer can no longer pay it and it leaves your outstanding total. It stays in your history, marked void."),
    ("Can I change plans later?", "Any time. Moving up takes effect at once; moving down takes effect at the end of the billing period."),
]

def feature(title, body, visual, flip=False):
    return f'''<div class="grid gap-8 md:gap-14 md:grid-cols-2 items-center py-12 border-t border-[color:var(--k-seam)]">
  <div class="{'md:order-2' if flip else ''}"><h3 class="text-[26px] md:text-[30px] font-bold tracking-[-0.015em] text-balance">{title}</h3><p class="text-ink-2 text-lg mt-3 max-w-[46ch] text-pretty">{body}</p></div>
  <div class="rounded-[22px] seam p-6 md:p-8">{visual}</div>
</div>'''

def footer_nav(cols):
    out = ""
    for h, links in cols:
        items = "".join(f'<li><a class="text-ink-2 hover:text-ink hover:underline underline-offset-3" href="{u}"{t}>{l}</a></li>' for l, u, t in links)
        out += f'<nav aria-label="{h}"><p class="engraved mb-3">{h}</p><ul class="grid gap-2 text-sm">{items}</ul></nav>'
    return out

FOOTER_NAV = footer_nav([
    ("Product", [("Features", "#features", ""), ("Pricing", "#pricing", ""), ("Questions", "#faq", "")]),
    ("App", [("Dashboard", "dashboard.html", ""), ("Invoices", "invoices.html", ""), ("Settings", "settings.html", "")]),
    ("Plastc", [("The UI library", "../index.html", ' target="_top"'), ("Source on GitHub", "https://github.com/thomasguillot/plastc-tailwind", ' target="_top"')]),
])

landing = f'''<body>
{SKIP}
<header class="max-w-[1200px] mx-auto px-4 md:px-8 pt-6 pb-2 flex flex-wrap items-center gap-x-6 gap-y-3">
  {wordmark("#top")}
  <nav class="order-3 md:order-none w-full md:w-auto flex flex-wrap gap-1 -mx-1 md:mx-0 md:ml-4" aria-label="Sections">{"".join(f'<a class="btn btn-quiet btn-sm" href="#{k}">{l}</a>' for k, l in LNAV)}</nav>
  <div class="ml-auto flex items-center gap-2"><a class="btn btn-quiet btn-sm" href="sign-in.html">Sign in</a><a class="btn btn-sm" href="dashboard.html">Open the app</a></div>
</header>

<main id="main">
<section id="top" class="max-w-[1200px] mx-auto px-4 md:px-8 pt-14 md:pt-24 pb-20 grid gap-12 lg:grid-cols-[1.05fr_1fr] items-center">
  <div>
    <h1 class="display text-[48px] sm:text-[64px] md:text-[80px] text-balance">Invoices that chase themselves.</h1>
    <p class="text-lg text-ink-2 max-w-[44ch] mt-7 leading-relaxed text-pretty">Send an invoice in a minute. Reminders follow up on their own, and one readout shows what is paid, open and overdue.</p>
    <div class="flex flex-wrap gap-3 mt-9"><a class="btn btn-signal btn-xl" href="sign-in.html">Start free</a><a class="btn btn-xl" href="dashboard.html">See the dashboard</a></div>
  </div>
  <div class="panel !p-4 sm:!p-5 min-w-0">
    <div class="lcd px-5 py-4 grid grid-cols-3 gap-4">{"".join(f'<div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">{k}</p><p class="text-lg sm:text-xl font-semibold mt-1">{v}</p></div>' for k, v in (("Paid", "$48,210"), ("Open", "$15,447"), ("Overdue", "$9,300")))}</div>
    <div class="table-scroll mt-3">{table(CUSTOMERS[:4], select=False, actions=False, dates=False)}</div>
  </div>
</section>

<section id="features" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <h2 class="display text-[40px] md:text-[56px] max-w-[16ch] text-balance">Built for the part after you hit send</h2>
  <div class="mt-12">
  {feature("Reminders that go out on their own", "The morning after a due date passes, then every week until the invoice is paid. Pause them for one customer whenever you need to.", """<ol class="timeline"><li class="lamp-ok"><b>Paid in full</b> by card<time>Oct 28 · 9:14 AM</time></li><li class="lamp-warn"><b>Reminder sent</b> to billing@halden.studio<time>Oct 24 · 8:00 AM</time></li><li><b>Viewed</b> by Halden Studio<time>Oct 3 · 2:31 PM</time></li><li><b>Sent</b> by Mira Okafor<time>Oct 1 · 10:02 AM</time></li></ol>""")}
  {feature("Paid the way your customers prefer", "Every invoice carries a pay link for card and bank transfer. Payments mark the invoice paid as they land.", """<div class="grid gap-3" role="radiogroup" aria-label="Payment method"><label class="choice-card"><input type="radio" name="lpm" class="radio mt-0.5" checked><span><span class="block text-sm font-bold">Card</span><span class="block text-sm text-ink-2">Visa, Mastercard and Amex. Paid in seconds.</span></span></label><label class="choice-card"><input type="radio" name="lpm" class="radio mt-0.5"><span><span class="block text-sm font-bold">Bank transfer</span><span class="block text-sm text-ink-2">Details on the invoice. Matched when it arrives.</span></span></label></div>""", flip=True)}
  {feature("Know where you stand", "Paid, open and overdue in one readout, updated as payments arrive. No spreadsheet to keep in step.", f"""<div class="flex flex-wrap items-center gap-6"><div class="w-[140px] shrink-0">{donut([("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")], "$63.8k", "invoiced", "Invoiced this quarter: $63,800. Paid 62%, open 21%, overdue 9%, draft 8%.")}</div><ul class="grid gap-2 text-sm min-w-[150px]">{"".join(f'<li class="flex items-center justify-between gap-4"><span class="badge {l}">{n}</span><span class="tabular-nums text-ink-2">{p}%</span></li>' for n, p, l in (("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")))}</ul></div>""")}
  </div>
</section>

<section id="pricing" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <div class="flex flex-wrap items-end justify-between gap-6">
    <div><h2 class="display text-[40px] md:text-[56px]">Pricing</h2><p class="text-ink-2 text-lg mt-4 max-w-[44ch]">Start free. Move up when your team or your client list grows.</p></div>
    <div class="seg" role="group" aria-label="Billing period"><button type="button" aria-pressed="true" data-billing="monthly">Monthly</button><button type="button" aria-pressed="false" data-billing="yearly">Yearly <span class="text-ink-2 font-semibold">2 months free</span></button></div>
  </div>
  <div class="grid gap-5 md:grid-cols-3 mt-10 items-stretch">{plan_cards}</div>
</section>

<section id="faq" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24 grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="display text-[40px] md:text-[56px]">Questions</h2><p class="text-ink-2 text-lg mt-4 max-w-[36ch]">Something else? Write to the team from inside the app.</p></div>
  <div class="accordion">{"".join(f'<details{" open" if n == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for n, (q, a) in enumerate(FAQS))}</div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <div class="panel !px-6 !py-10 md:!px-12 md:!py-14 flex flex-wrap items-center justify-between gap-8">
    <div><h2 class="text-[32px] md:text-[40px] font-bold tracking-[-0.02em] text-balance max-w-[18ch]">Send your next invoice in a minute.</h2><p class="text-ink-2 text-lg mt-3">Free for your first five invoices every month.</p></div>
    <div class="flex flex-wrap gap-3"><a class="btn btn-signal btn-lg" href="sign-in.html">Start free</a><a class="btn btn-lg" href="#pricing">Compare plans</a></div>
  </div>
</section>
</main>

<footer class="max-w-[1200px] mx-auto px-4 md:px-8 pt-12 pb-10 mt-6 border-t border-[color:var(--k-seam)]">
  <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
    <div>{wordmark("#top")}<p class="text-sm text-ink-2 mt-4 max-w-[32ch]">Invoicing for studios and small practices.</p></div>
    {FOOTER_NAV}
  </div>
  <div class="flex flex-wrap items-center justify-between gap-4 mt-12 pt-6 border-t border-[color:var(--k-seam)] text-sm text-ink-2">
    <p>Sample page built with Plastc. The product, prices and copy are made up.</p>
    {housing_seg()}
  </div>
</footer>
'''
page("screens/landing.html", "Landing page · Plastc", landing, "../")

# ------------------------------------------------------------------ showcase
def spec(name, cls, rule, specimen):
    return f'''<div class="flex flex-col gap-4">
  <div class="h-40 grid place-items-center rounded-[20px] px-4 seam">{specimen}</div>
  <div><p class="font-bold">{name} <code class="font-mono text-xs text-ink-2 ml-1">{cls}</code></p><p class="text-sm text-ink-2 mt-1 max-w-[36ch]">{rule}</p></div>
</div>'''

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SVG_CASE = {"viewbox": "viewBox", "preserveaspectratio": "preserveAspectRatio", "lineargradient": "linearGradient"}
LIBRARY_DATA = set(re.findall(r"data-[a-z-]+", CSS_SRC.read_text()))

class Node:
    def __init__(self, tag, attrs, selfclose=False):
        self.tag, self.attrs, self.selfclose, self.children = tag, attrs, selfclose, []

class Tree(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.root = Node(None, [])
        self.stack = [self.root]
        self.feed(markup); self.close()
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs); self.stack[-1].children.append(n)
        if tag not in VOID: self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs, True))
    def handle_endtag(self, tag):
        for k in range(len(self.stack) - 1, 0, -1):
            if self.stack[k].tag == tag:
                del self.stack[k:]; return
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def static_calendar(value):
    sel = datetime.date.fromisoformat(value)
    first = sel.replace(day=1)
    start = first - datetime.timedelta(days=(first.weekday() + 1) % 7)
    today = datetime.date.today()
    rows = ""
    for w in range(6):
        cells = ""
        for d in range(7):
            day = start + datetime.timedelta(days=w * 7 + d)
            extra = (" data-outside" if day.month != sel.month else "") + (' aria-current="date"' if day == today else "")
            cells += (f'<td><button type="button" tabindex="{0 if day == sel else -1}" aria-label="{day:%A, %B} {day.day}, {day.year}"'
                      f'{extra} aria-pressed="{"true" if day == sel else "false"}">{day.day}</button></td>')
        rows += f"<tr>{cells}</tr>"
    title = f"{first:%B %Y}"
    heads = "".join(f'<th scope="col"><abbr title="{n}">{n[:2]}</abbr></th>' for n in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))
    step = lambda label, d: f'<button type="button" class="btn btn-quiet btn-sm btn-icon" aria-label="{label}">{ico('<path d="' + d + '"/>')}</button>'
    return (f'<div class="calendar-head">{step("Previous month", "m15 6-6 6 6 6")}<p class="calendar-title" aria-live="polite">{title}</p>{step("Next month", "m9 6 6 6-6 6")}</div>'
            f'<table role="grid" aria-label="{title}"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table>')

def strip_demo(node, dialog=None):
    kept = []
    for c in node.children:
        if isinstance(c, str):
            kept.append(c); continue
        names = {k for k, _ in c.attrs}
        if "data-demo-note" in names: continue
        if "data-calendar" in names and not any(isinstance(x, Node) for x in c.children):
            c.children = Tree(static_calendar(dict(c.attrs).get("data-value") or datetime.date.today().isoformat())).root.children
        attrs = []
        for k, v in c.attrs:
            if k == "data-open-dialog": attrs += [("commandfor", v), ("command", "show-modal")]
            elif k == "data-open-command": attrs += [("commandfor", "command"), ("command", "show-modal")]
            elif k == "data-close-dialog" and dialog: attrs += [("commandfor", dialog), ("command", "close")]
            elif k.startswith("data-") and k not in LIBRARY_DATA: continue
            else: attrs.append((k, v))
        c.attrs = attrs
        strip_demo(c, dict(attrs).get("id") if c.tag == "dialog" else dialog)
        kept.append(c)
    node.children = kept

def esc_text(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def open_tag(n):
    attrs = "".join(f" {SVG_CASE.get(k, k)}" if v is None else f' {SVG_CASE.get(k, k)}="{v.replace("&", "&amp;").replace(chr(34), "&quot;")}"' for k, v in n.attrs)
    tag = SVG_CASE.get(n.tag, n.tag)
    return f"<{tag}{attrs}{'/' if n.selfclose else ''}>"

def inline(n):
    if isinstance(n, str): return esc_text(re.sub(r"\s+", " ", n))
    if n.selfclose or n.tag in VOID: return open_tag(n)
    return open_tag(n) + "".join(inline(c) for c in n.children) + f"</{SVG_CASE.get(n.tag, n.tag)}>"

def breaks(n):
    if isinstance(n, str) or n.tag in ("pre", "textarea"): return False
    if n.tag == "svg" and "chart" not in dict(n.attrs).get("class", ""): return False
    if any(isinstance(c, str) and c.strip() for c in n.children): return False
    kids = [c for c in n.children if isinstance(c, Node)]
    return len(kids) > 1 or (len(kids) == 1 and breaks(kids[0]))

def pretty(n, depth=0):
    pad = "  " * depth
    if not breaks(n): return pad + inline(n)
    kids = "\n".join(pretty(c, depth + 1) for c in n.children if isinstance(c, Node))
    return f"{pad}{open_tag(n)}\n{kids}\n{pad}</{SVG_CASE.get(n.tag, n.tag)}>"

def clean_html(markup):
    tree = Tree(markup).root
    strip_demo(tree)
    return "\n".join(pretty(c) for c in tree.children if isinstance(c, Node))

def script_note(body, extra):
    needs = [label for hit, label in (
        ('role="combobox"' in body, "combobox filtering and keys"),
        ("data-calendar" in body, "the calendar’s month grid"),
        ("data-page-step" in body, "moving the page numbers"),
        ("data-file-input" in body, "listing files and their upload progress"),
        ('class="toast"' in extra, "showing toasts and hiding them on a timer"),
        ("data-open-command" in body, "the Cmd+K shortcut, filtering and arrow keys"),
    ) if hit]
    if not needs: return ""
    last = ", and " if any(" and " in n for n in needs) else " and "
    said = needs[0] if len(needs) == 1 else ", ".join(needs[:-1]) + last + needs[-1]
    return f'<p class="text-[13px] text-ink-2">Your own script handles {said}. <a class="text-ink underline" href="{REPO}/blob/main/site/plastc.js">plastc.js</a> shows one way.</p>'

def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.replace("&amp;", " ").lower()).strip("-")

GROUPS = []
def group(title, classes, body, wide=False, extra=""):
    gid = slug(title)
    assert gid not in {g[0] for g in GROUPS}, gid
    GROUPS.append((gid, title, classes))
    span = " lg:col-span-2" if wide else ""
    markup = clean_html(body + extra)
    return f'''<section id="{gid}" class="py-7{span} border-t border-[color:var(--k-seam)] shadow-[inset_0_1px_0_rgb(var(--k-hl)/calc(.55*var(--k-hl-a)))] min-w-0 scroll-mt-4">
  <div class="flex flex-wrap items-center gap-x-4 gap-y-1.5 mb-5"><h3 class="engraved">{title}</h3><code class="order-last basis-full sm:order-none sm:basis-0 sm:flex-1 sm:text-right font-mono text-[11px] text-ink-2 break-words min-w-0">{classes}</code><button type="button" class="btn btn-quiet btn-sm ml-auto sm:ml-0 -mr-3.5" data-copy-from="{gid}-html">{i("copy")}Copy HTML</button></div>
  <div>{body}</div>
  <details class="group/code mt-5">
    <summary class="btn btn-quiet btn-sm -ml-3.5 [&::-webkit-details-marker]:hidden">{i("code")}View HTML{i("chevron", "transition-transform duration-200 ease-out motion-reduce:transition-none group-open/code:rotate-180")}</summary>
    <div class="grid gap-3 mt-3">{script_note(body, extra)}<pre class="code min-w-0 max-h-[28rem] overflow-y-auto" id="{gid}-html" tabindex="0" aria-label="HTML for {title}">{esc_text(markup)}</pre></div>
  </details>
</section>'''

def jump_list():
    links = "".join(f'<li><a class="btn btn-quiet btn-sm" href="#{gid}">{title}</a></li>' for gid, title, _ in GROUPS)
    return f'<nav aria-label="Component groups" class="mb-8"><ul class="flex flex-wrap gap-1 -ml-3.5">{links}</ul></nav>'

CB_SEEN = {}
for row_ in CUSTOMERS: CB_SEEN.setdefault(row_[1], row_[2])
CB_OPTS = "".join(f'<div role="option" id="cb1-o{n}" aria-selected="false" data-value="{name}"><span class="avatar !w-7 !h-7 !text-[11px]">{ini}</span>{name}</div>' for n, (name, ini) in enumerate(CB_SEEN.items()))
screens = [("dashboard", "Dashboard"), ("invoices", "Invoices"), ("customers", "Customers"), ("reports", "Reports"), ("products", "Products"), ("settings", "Settings")]
VIEWER_SCREENS = [("dashboard", "Dashboard"), ("invoices", "Invoices"), ("customers", "Customers"), ("reports", "Reports"), ("products", "Products"), ("settings", "Settings"), ("sign-in", "Sign in"), ("landing", "Landing page")]
viewer_tabs = "".join(f'<button type="button" data-screen="{k}"{' aria-current="page"' if k == "dashboard" else ""}>{t}</button>' for k, t in VIEWER_SCREENS)
viewer_options = "".join(f'<option value="{k}">{t}</option>' for k, t in VIEWER_SCREENS)
VIEWER = f'''<dialog class="dialog dialog-full" id="screen-viewer" aria-label="Reference screens">
  <div class="flex items-center gap-3 px-3 sm:px-4 py-2.5 border-b border-[color:var(--k-seam)]">
    <div class="hidden xl:block min-w-0"><div class="seg" role="group" aria-label="Screens">{viewer_tabs}</div></div>
    <label class="xl:hidden flex-1 min-w-0 max-w-[280px]"><span class="sr-only">Screen</span><select class="field field-select !h-10 !text-sm" data-screen-select>{viewer_options}</select></label>
    <a class="btn btn-quiet btn-sm ml-auto shrink-0" href="screens/dashboard.html" target="_blank" rel="noopener" data-screen-tab>{i("external")}<span class="hidden sm:inline">Open in new tab</span><span class="sr-only sm:hidden">Open in new tab</span></a>
    <button type="button" class="btn btn-sm btn-icon" data-close-dialog aria-label="Close">{i("x")}</button>
  </div>
  <iframe class="flex-1 min-h-0 w-full border-0 bg-housing" title="Dashboard" data-screen-frame></iframe>
</dialog>'''
previews = "".join(f'''<a href="screens/{k}.html" class="group block no-underline text-ink" data-open-screen="{k}">
  <div class="recessed rounded-[18px] p-2"><div class="relative overflow-hidden rounded-xl aspect-[16/10] bg-housing"><iframe src="screens/{k}.html" title="{t} preview" tabindex="-1" aria-hidden="true" class="absolute top-0 left-0 w-[1440px] h-[900px] origin-top-left scale-[var(--s)] pointer-events-none" style="--s:.25"></iframe></div></div>
  <p class="flex items-center justify-between font-bold mt-3">{t}<span class="text-ink-2 transition-transform duration-200 group-hover:translate-x-1">{i("right","w-4 h-4")}</span></p>
</a>''' for k, t in screens)
public_previews = "".join(f'''<a href="screens/{k}.html" class="group block no-underline text-ink" data-open-screen="{k}">
  <div class="recessed rounded-[18px] p-2"><div class="relative overflow-hidden rounded-xl aspect-[16/10] bg-housing"><iframe src="screens/{k}.html" title="{t} preview" tabindex="-1" aria-hidden="true" class="absolute top-0 left-0 w-[1440px] h-[900px] origin-top-left scale-[var(--s)] pointer-events-none" style="--s:.25"></iframe></div></div>
  <p class="flex items-center justify-between font-bold mt-3">{t}<span class="text-ink-2 transition-transform duration-200 group-hover:translate-x-1">{i("right","w-4 h-4")}</span></p>
</a>''' for k, t in (("landing", "Landing page"), ("sign-in", "Sign in")))

DEPTH_ROWS = (
    ("Plane", "--k-seam-line", "background:var(--k-housing);border:1px solid var(--k-seam);box-shadow:var(--k-seam-line)", "Flush. Panels, tabs, tables.", "box-shadow: var(--k-seam-line);"),
    ("Raised", "--k-raised", "background:var(--k-housing);box-shadow:var(--k-raised)", "A part you press.", "box-shadow: var(--k-raised);"),
    ("Pressed", "--k-pressed", "background:var(--k-housing);box-shadow:var(--k-pressed)", "A raised part, pushed in.", "box-shadow: var(--k-pressed);"),
    ("Recessed", "--k-recessed", "background:var(--k-housing);box-shadow:var(--k-recessed)", "Holds input or output.", "box-shadow: var(--k-recessed);"),
    ("Float", "--k-float", "background:var(--k-housing-up);box-shadow:var(--k-float)", "Overlays only.", "box-shadow: var(--k-float);"))
DEPTH = "".join(f'<div class="min-w-0"><div class="rounded-[18px] seam p-5"><div class="h-20 rounded-[14px] grid place-items-center text-[13px] font-bold" style="{st}">{name}</div></div><p class="font-mono text-[13px] font-bold mt-3">{tok}</p><p class="text-sm text-ink-2 mt-1">{note}</p><button class="btn btn-quiet btn-sm mt-2" data-copy="{decl}" aria-label="Copy {decl}">{i("copy")}Copy</button></div>' for name, tok, st, note, decl in DEPTH_ROWS)

IMPORT = '@import "tailwindcss";\n@import "./plastc.css";'
TOAST_EXAMPLE = '<div class="toast" popover="manual" role="status" id="toast"><span>Invoice INV-0193 sent</span><button type="button" class="lcd-action">Undo</button></div>'
COMMAND_EXAMPLE = command_dialog([
    ("Go to", [("home", "Dashboard", 'href="dashboard.html"', ""), ("file", "Invoices", 'href="invoices.html"', "")]),
    ("Actions", [("plus", "New invoice", 'data-command="new-invoice"', "N")]),
])
SHOWNAV = '<a class="btn btn-quiet btn-sm" href="#depth">Depth</a><a class="btn btn-quiet btn-sm" href="#components">Components</a><a class="btn btn-quiet btn-sm" href="#screens">Screens</a><a class="btn btn-quiet btn-sm" href="#install">Install</a>'

showcase = f'''<body>
{SKIP}
<header class="max-w-[1240px] mx-auto px-4 md:px-8 pt-6 pb-2 md:pb-6 flex flex-wrap items-center gap-x-6 gap-y-3">
  {wordmark("#top", "")}
  <nav class="order-3 md:order-none w-full md:w-auto flex flex-wrap gap-1 -mx-1 md:mx-0 md:ml-4" aria-label="Sections">{SHOWNAV}</nav>
  <a class="btn btn-quiet btn-sm ml-auto" href="{REPO}">{GITHUB}<span class="sr-only sm:not-sr-only">GitHub</span></a>
  {housing_seg()}
</header>

<main id="main">
<section id="top" class="max-w-[1240px] mx-auto px-4 md:px-8 pt-8 pb-12 md:pt-16 md:pb-24 grid gap-12 lg:grid-cols-[1.25fr_1fr] items-center">
  <div>
    <h1 class="display text-[52px] sm:text-[76px] lg:text-[96px]">Every button a real button.</h1>
    <p class="text-lg text-ink-2 max-w-[46ch] mt-7 leading-relaxed">Plastc is a neumorphic UI library for Tailwind v4, with components, app screens and tokens. Depth goes only where your hand expects it. Parts you press stand up, parts that hold input sit in, and everything else stays flush and quiet.</p>
    <div class="flex flex-wrap gap-3 mt-9"><a class="btn btn-signal btn-xl" href="plastc.css" download>{i("down")}Get the CSS</a><a class="btn btn-xl" href="screens/dashboard.html" data-open-screen="dashboard">Open the dashboard</a></div>
    <p class="text-sm text-ink-2 mt-4 tabular-nums">plastc.css · v{VERSION} · {CSS_KB} KB · MIT-Licensed</p>
  </div>

  <div class="relative mx-auto w-full max-w-[400px]">
    <div class="rounded-[34px] p-6 sm:p-7 bg-[image:var(--k-cast)] shadow-[var(--k-raised)]">
      <div class="lcd px-5 py-4 flex items-end justify-between">
        <div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Depth</p><p class="text-[40px] font-semibold leading-none mt-1" data-depth-readout>1.0</p></div>
        <div class="text-right"><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Housing</p><p class="text-lg font-semibold mt-1 uppercase" data-housing-readout>Light</p></div>
      </div>
      <p class="engraved mt-7 mb-3" id="dk">Depth</p>
      <div class="grid grid-cols-3 gap-4" role="group" aria-labelledby="dk">
        <button class="key text-sm" data-set-depth="0.5" aria-pressed="false">Soft</button>
        <button class="key text-sm" data-set-depth="1" aria-pressed="true">Normal</button>
        <button class="key text-sm" data-set-depth="1.7" aria-pressed="false">Deep</button>
      </div>
      <p class="engraved mt-6 mb-3" id="hk">Housing</p>
      <div class="grid grid-cols-3 gap-4" role="group" aria-labelledby="hk">
        <button class="key text-[13px]" data-set-housing="light" aria-pressed="true">Light</button>
        <button class="key text-[13px]" data-set-housing="dark" aria-pressed="false">Dark</button>
        <button class="key text-[13px]" data-reset>Reset</button>
      </div>
    </div>
  </div>
</section>

<section id="depth" class="max-w-[1240px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <h2 class="display text-[40px] md:text-[56px] max-w-[14ch]">Four depths. One reason each.</h2>
  <p class="text-ink-2 text-lg max-w-[56ch] mt-5">Most neumorphism extrudes everything, so nothing reads as touchable. Plastc gives each depth a job, and the job decides the shadow.</p>
  <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 mt-12">
    {spec("Plane", ".panel  .seam", "The housing and every layout container. Flush, separated by a moulded parting line.", '<div class="panel w-full max-w-[220px] !p-4 text-left"><p class="text-[13px] font-bold">INV-0193</p><div class="flex justify-between mt-2 text-[13px]"><span class="badge lamp-ok">Paid</span><span class="font-semibold tabular-nums">$4,820.00</span></div></div>')}
    {spec("Raised", ".btn  .key  .raised", "Only parts you press. Lit from the top, with a contact shadow. Pressing sets them flush.", '<button class="btn btn-lg" type="button">Press me</button>')}
    {spec("Recessed", ".field  .lcd  .recessed", "Only parts that hold input or output: fields, tracks, wells, readouts.", '<input class="field !w-44" placeholder="Type here" aria-label="Example field">')}
    {spec("Float", ".menu  .dialog  .toast", "Overlays only. The one level with a long shadow, because it really sits above the page.", '<div class="menu !min-w-0 w-40"><a href="#depth">Rename</a><a href="#depth">Duplicate</a></div>')}
  </div>
</section>

<section id="components" class="max-w-[1240px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <div class="flex flex-wrap items-end justify-between gap-6 mb-10">
    <h2 class="display text-[40px] md:text-[56px]">Components</h2>
    <p class="text-ink-2 max-w-[44ch]">Every part below is live HTML using the classes beside it. Press, type and toggle, then view or copy the markup.</p>
  </div>
  <!--jump-->
  <div class="grid lg:grid-cols-2 gap-x-14 [&>*]:min-w-0">
    {group("Buttons", ".btn  .btn-signal  .btn-go  .btn-quiet  .btn-sm…2xl", f"""
      <div class="flex flex-wrap items-center gap-3"><button class="btn btn-signal">{i("plus","", "2.2")}New invoice</button><button class="btn">Secondary</button><button class="btn btn-go">{i("check","", "2.2")}Approve</button><button class="btn btn-quiet">Tertiary</button></div>
      <div class="flex flex-wrap items-center gap-3 mt-4"><button class="btn btn-sm">Small</button><button class="btn btn-md">Medium</button><button class="btn btn-lg">Large</button><button class="btn btn-xl">X-large</button></div>
      <div class="flex flex-wrap items-center gap-3 mt-4"><button class="btn" disabled>Disabled</button><button class="btn" aria-busy="true">Saving</button><button class="btn btn-danger">Delete</button><span class="tooltip" data-tip="3 unread"><button class="btn btn-icon" aria-label="Notifications, 3 unread">{i("bell")}</button></span></div>""")}
    {group("Inputs", ".field  .field-select  .field-area  .label  .hint", """
      <div class="grid sm:grid-cols-2 gap-4">
        <div><label class="label" for="c1">Customer</label><input id="c1" class="field" placeholder="Search customers"></div>
        <div><label class="label" for="c2">Currency</label><select id="c2" class="field field-select"><option>USD — US Dollar</option><option>EUR — Euro</option></select></div>
        <div><label class="label" for="c3">Email</label><input id="c3" class="field" value="billing@halden" aria-invalid="true" aria-describedby="c3e"><span id="c3e" class="hint-error">Add a domain, for example .studio</span></div>
        <div><label class="label" for="c4">Invoice number</label><input id="c4" class="field" value="INV-0194" disabled aria-describedby="c4h"><span id="c4h" class="hint">Assigned automatically.</span></div>
      </div>""")}
    {group("Input groups", ".input-group  .input-affix", f"""
      <div class="grid sm:grid-cols-2 gap-4">
        <div><label class="label" for="ig1">Search</label><label class="input-group">{i("search")}<input id="ig1" placeholder="Search invoices"><span class="kbd" aria-hidden="true">/</span></label></div>
        <div><label class="label" for="ig2">Website</label><div class="input-group"><span class="input-affix">https://</span><input id="ig2" value="halden.studio"></div></div>
        <div><label class="label" for="ig3">Late fee</label><div class="input-group"><input id="ig3" inputmode="decimal" value="4"><span class="input-affix">% a month</span></div></div>
        <div><label class="label" for="ig4">API key</label><div class="input-group"><input id="ig4" class="!font-mono !text-[14px]" value="plc_live_4f2a…9c1e" readonly><button type="button" class="btn btn-sm" data-copy="plc_live_4f2a9c1e">{i("copy")}Copy</button></div></div>
      </div>""")}
    {group("Status &amp; feedback", ".badge  .lamp-*  .tag  .meter  .alert", f"""
      <div class="flex flex-wrap items-center gap-x-6 gap-y-3"><span class="badge lamp-ok">Paid</span><span class="badge lamp-warn">Open</span><span class="badge lamp-danger">Overdue</span><span class="badge lamp-off">Draft</span><span class="tag">Net 30</span><span class="tag">USD</span></div>
      <div class="mt-5"><div class="flex justify-between text-[13px] mb-2"><span class="font-semibold">Storage</span><span class="text-ink-2">6.2 of 10 GB</span></div><div class="meter" role="meter" aria-label="Storage" aria-valuemin="0" aria-valuemax="10" aria-valuenow="6.2"><span style="--v:62%"></span></div></div>
      <div class="alert lamp-warn mt-5">{i("alert")}<div class="alert-body"><b>Two invoices are due this week.</b><span class="block text-ink-2">Juno Park and Priya Nair. Reminders go out automatically.</span></div></div>""")}
    {group("Combobox &amp; date picker", ".combobox  .calendar  .popover", f"""
      <div class="grid gap-8 xl:grid-cols-[minmax(0,1fr)_auto] items-start">
        <div class="grid gap-6 sm:grid-cols-2 xl:grid-cols-1">
          <div><label class="label" id="cb1-l" for="cb1">Customer</label>
            <div class="combobox"><div class="input-group"><input id="cb1" role="combobox" aria-expanded="false" aria-controls="cb1-list" aria-autocomplete="list" autocomplete="off" placeholder="Search customers"><button type="button" class="btn btn-quiet btn-sm btn-icon" tabindex="-1" aria-label="Show customers" data-combobox-toggle>{i("chevron")}</button></div>
            <div class="listbox" role="listbox" id="cb1-list" aria-labelledby="cb1-l" hidden>{CB_OPTS}<p class="listbox-empty" hidden>No customers match.</p></div></div></div>
          <div><label class="label" for="dp1">Due date</label>
            <div class="input-group" style="anchor-name:--dp1"><input id="dp1" value="Nov 28, 2026"><button type="button" class="btn btn-quiet btn-sm btn-icon" popovertarget="dp1-cal" aria-label="Choose due date">{i("cal")}</button></div>
            <div class="popover" popover id="dp1-cal" style="position-anchor:--dp1;position-area:bottom span-left;transform-origin:top right"><div class="calendar" data-calendar data-for="dp1" data-value="2026-11-28"></div></div></div>
        </div>
        <div class="min-w-0"><p class="text-[13px] font-bold mb-2" id="cal-solo-l">Calendar, on its own</p><div class="w-fit max-w-full overflow-x-auto rounded-[20px] seam p-4" role="group" aria-labelledby="cal-solo-l"><div class="calendar" data-calendar data-value="2026-11-24"></div></div></div>
      </div>""")}
    {group("Selection", ".check  .radio  .switch  .choice-card  .seg  .range", """
      <div class="flex flex-wrap gap-x-8 gap-y-4">
        <label class="flex items-center gap-2.5 text-sm font-semibold"><input type="checkbox" class="check" checked>Send copy</label>
        <label class="flex items-center gap-2.5 text-sm font-semibold"><input type="checkbox" class="check">Attach PDF</label>
        <label class="flex items-center gap-2.5 text-sm font-semibold"><input type="checkbox" role="switch" class="switch" checked>Reminders</label>
      </div>
      <div class="grid sm:grid-cols-2 gap-3 mt-5" role="radiogroup" aria-label="Billing period">
        <label class="choice-card"><input type="radio" name="bp" class="radio mt-0.5" checked><span><span class="block text-sm font-bold">Monthly</span><span class="block text-sm text-ink-2">$12 / mo</span></span></label>
        <label class="choice-card"><input type="radio" name="bp" class="radio mt-0.5"><span><span class="block text-sm font-bold">Yearly</span><span class="block text-sm text-ink-2">$120 / yr, 2 months free</span></span></label>
      </div>
      <div class="flex flex-wrap items-end gap-5 mt-6"><div class="seg" role="group" aria-label="View"><button aria-pressed="true">Grid</button><button aria-pressed="false">List</button></div>
      <div class="flex-1 min-w-[200px]"><label class="label" for="rg">Late fee · <span data-range-out>4</span>%</label><input id="rg" type="range" min="0" max="10" value="4" class="range" style="--fill:40%"></div></div>""")}
    {group("Empty states", ".empty  .readout  .empty-actions", f"""
      <div class="empty seam rounded-[20px] !py-10">
        <div class="lcd readout"><span class="readout-value">0</span><span class="readout-unit">Customers</span></div>
        <h4>No customers yet</h4>
        <p>Customers appear here after you send their first invoice. You can also add one now.</p>
        <div class="empty-actions"><button class="btn btn-sm" data-toast="Customer form is not part of this demo">{i("plus","", "2.2")}Add customer</button><button class="btn btn-sm btn-quiet" data-toast="Import is not part of this demo">{i("down")}Import CSV</button></div>
      </div>""")}
    {group("Overlays", ".menu  .dialog  .toast  .tooltip", f"""
      <p class="text-sm text-ink-2 mb-4 max-w-[52ch]" data-demo-note>The only parts that float. Menus grow from their button, the dialog settles in from the centre, and toasts rise from the bottom. Each leaves faster than it arrives. All native: popover and &lt;dialog&gt;, so Esc and outside-click work without a script.</p>
      <div class="flex flex-wrap gap-3">
        <button class="btn" popovertarget="demo-menu" style="anchor-name:--demo-menu">{i("dots")}Open menu</button>
        <div class="menu" popover id="demo-menu" style="position-anchor:--demo-menu;position-area:bottom span-right;transform-origin:top left"><a href="#components">{i("file")}View</a><button type="button" data-toast="Duplicated">{i("copy")}Duplicate</button><hr><button type="button" class="!text-danger" data-open-dialog="demo-dialog">{i("trash")}Delete…</button></div>
        <button class="btn" data-open-dialog="demo-dialog">Open dialog</button>
        <button class="btn" data-toast="Invoice INV-0193 sent">Show toast</button>
      </div>
      <dialog class="dialog" id="demo-dialog" aria-labelledby="dd-h"><form method="dialog" class="grid gap-4"><h4 id="dd-h" class="text-lg font-bold">Delete this draft?</h4><p class="text-sm text-ink-2">It hasn’t been sent, so no one else has seen it. This can’t be undone.</p><div class="flex justify-end gap-3 pt-2"><button class="btn" value="cancel" autofocus>Keep draft</button><button class="btn btn-danger" value="delete">{i("trash")}Delete</button></div></form></dialog>""", extra=TOAST_EXAMPLE)}
    {group("Progress &amp; loading", ".progress  .spinner  .skeleton", f"""
      <div class="grid gap-6">
        <div><div class="flex justify-between text-[13px] mb-2"><span class="font-semibold" id="pg1-l">Exporting invoices</span><span class="text-ink-2 tabular-nums">64%</span></div><div class="progress" role="progressbar" aria-labelledby="pg1-l" aria-valuemin="0" aria-valuemax="100" aria-valuenow="64"><span style="--v:64%"></span></div></div>
        <div><p class="text-[13px] font-semibold mb-2" id="pg2-l">Syncing with your bank</p><div class="progress" role="progressbar" aria-labelledby="pg2-l"><span></span></div></div>
        <div class="flex flex-wrap items-center gap-6"><span class="spinner" role="status"><span class="sr-only">Loading</span></span><span class="spinner spinner-lg" role="status"><span class="sr-only">Loading</span></span><button class="btn btn-sm" aria-busy="true" disabled>Saving</button></div>
        <div class="flex items-center gap-3.5 p-4 rounded-[18px] seam" role="status" aria-label="Loading customer"><span class="skeleton size-10 !rounded-full"></span><span class="flex-1 grid gap-2"><span class="skeleton h-3 w-2/5"></span><span class="skeleton h-3 w-3/4"></span></span><span class="skeleton h-8 w-20 !rounded-full"></span></div>
      </div>""")}
    {group("File upload", ".dropzone  .file-item", f"""
      <label class="dropzone" data-dropzone>{i("upload")}<span><strong>Click to upload</strong> or drag and drop</span><span class="text-[13px]">PDF, PNG or JPG, up to 10 MB</span><input type="file" multiple accept=".pdf,.png,.jpg,.jpeg" data-file-input></label>
      <ul class="mt-3" data-file-list>
        <li class="file-item"><span class="file-icon">{i("file")}</span><div class="min-w-0"><p class="file-name">halden-logo.svg</p><p class="file-meta">240 KB · <span class="badge lamp-ok">Uploaded</span></p></div><button type="button" class="btn btn-quiet btn-sm btn-icon" aria-label="Remove halden-logo.svg" data-file-remove>{i("trash")}</button></li>
        <li class="file-item"><span class="file-icon">{i("file")}</span><div class="min-w-0"><p class="file-name">invoice-0193.pdf</p><p class="file-meta">1.2 MB · <span data-file-pct>64%</span></p></div><button type="button" class="btn btn-quiet btn-sm btn-icon" aria-label="Cancel invoice-0193.pdf" data-file-remove>{i("x")}</button><div class="progress" role="progressbar" aria-label="Uploading invoice-0193.pdf" aria-valuemin="0" aria-valuemax="100" aria-valuenow="64"><span style="--v:64%"></span></div></li>
        <li class="file-item"><span class="file-icon">{i("file")}</span><div class="min-w-0"><p class="file-name">receipt-scan.jpg</p><p class="file-meta file-error">14.8 MB · Over the 10 MB limit</p></div><button type="button" class="btn btn-quiet btn-sm btn-icon" aria-label="Remove receipt-scan.jpg" data-file-remove>{i("trash")}</button></li>
      </ul>""")}
    {group("Tabs &amp; pagination", ".tabs  .pager  .pager-pages  .pager-status", f"""
      <nav class="tabs" aria-label="Customer sections"><a href="#components" aria-current="page">Overview</a><a href="#components">Invoices <span class="text-ink-2 font-semibold">12</span></a><a href="#components">Payments</a><a href="#components">Activity</a></nav>
      <p class="text-sm text-ink-2 mt-4 max-w-[52ch]" data-demo-note>Tabs switch the panels of one page. For filters and view modes inside a panel, use <code class="font-mono">.seg</code>.</p>
      <nav class="pager mt-7" aria-label="Pagination">
        <button type="button" class="btn btn-sm" data-page-step="-1" disabled>{i("left")}Previous</button>
        <div class="seg pager-pages" role="group" aria-label="Pages"><button type="button" aria-current="page">1</button><button type="button">2</button><button type="button">3</button><button type="button">4</button><button type="button">5</button><span aria-hidden="true">…</span><button type="button">8</button></div>
        <p class="pager-status" aria-live="polite">Page 1 of 8</p>
        <button type="button" class="btn btn-sm" data-page-step="1">Next{i("right")}</button>
      </nav>""")}
    {group("Breadcrumbs &amp; command menu", ".breadcrumbs  .command", f"""
      <nav aria-label="Breadcrumb"><ol class="breadcrumbs"><li><a href="#components">{i("home")}Dashboard</a></li><li><a href="#components">Invoices</a></li><li><a href="#components">Halden Studio</a></li><li><span aria-current="page">INV-0193</span></li></ol></nav>
      <p class="text-sm text-ink-2 mt-6 max-w-[52ch]" data-demo-note>The command menu is a <code class="font-mono">.dialog</code> holding a search field and a <code class="font-mono">.listbox</code>. Open it from anywhere on this page, type to filter, and move with the arrow keys.</p>
      <button type="button" class="btn mt-4" data-open-command>{i("search")}Search or jump to<span class="kbd ml-1" data-kbd-mod>Ctrl K</span></button>""", extra=COMMAND_EXAMPLE)}
    {group("Accordion &amp; description list", ".accordion  .desc-list", f"""
      <div class="accordion">
        <details open><summary>When do reminders go out?</summary><p>The morning after a due date passes, then every seven days until the invoice is paid. You can change the schedule, or turn reminders off for one customer.</p></details>
        <details><summary>Can customers pay by card?</summary><p>Yes. Every invoice has a pay link that takes card and bank transfer. Paid invoices update on their own.</p></details>
        <details><summary>What happens when I void an invoice?</summary><p>The customer can no longer pay it and it leaves your outstanding total. The record stays in your history, marked void.</p></details>
      </div>
      <dl class="desc-list mt-6">
        <div><dt>Invoice</dt><dd class="font-mono">INV-0193</dd></div>
        <div><dt>Customer</dt><dd>Halden Studio</dd></div>
        <div><dt>Issued</dt><dd>Oct 1, 2026</dd></div>
        <div><dt>Amount</dt><dd class="tabular-nums">$4,820.00</dd></div>
        <div><dt>Status</dt><dd><span class="badge lamp-ok">Paid</span></dd></div>
      </dl>""")}
    {group("Avatar group &amp; timeline", ".avatar-group  .timeline", f"""
      <div class="flex flex-wrap items-center gap-4">
        <div class="avatar-group"><span class="avatar">MO</span><span class="avatar">DS</span><span class="avatar">LW</span><button type="button" class="avatar" popovertarget="team-more" style="anchor-name:--team-more" aria-label="3 more people">+3</button></div>
        <p class="text-sm text-ink-2">6 people can send invoices</p>
        <div class="popover" popover id="team-more" style="position-anchor:--team-more"><p class="engraved mb-3">Also on the team</p><ul class="grid gap-3">{"".join(f'<li class="flex items-center gap-3"><span class="avatar !w-8 !h-8 !text-[11px]">{a}</span><span><span class="block text-sm font-semibold">{n}</span><span class="block text-[13px] text-ink-2">{r}</span></span></li>' for a, n, r in (("AB", "Ade Bello", "Member"), ("SM", "Sofia Marin", "Member"), ("KI", "Kenji Ito", "Viewer")))}</ul></div>
      </div>
      <ol class="timeline mt-7">
        <li class="lamp-ok"><b>Paid in full</b> by card<time datetime="2026-10-28T09:14">Oct 28 · 9:14 AM</time></li>
        <li class="lamp-warn"><b>Reminder sent</b> to billing@halden.studio<time datetime="2026-10-24T08:00">Oct 24 · 8:00 AM</time></li>
        <li><b>Viewed</b> by Halden Studio<time datetime="2026-10-03T14:31">Oct 3 · 2:31 PM</time></li>
        <li><b>Sent</b> by Mira Okafor<time datetime="2026-10-01T10:02">Oct 1 · 10:02 AM</time></li>
      </ol>""")}
    {group("Charts", ".bar-chart  .chart  .sparkline", f"""
      <div class="grid gap-x-10 gap-y-8 md:grid-cols-[1.5fr_1fr_1fr] items-start">
        <figure><figcaption><span class="block font-bold">Invoices sent</span><span class="block text-sm text-ink-2">Last six months</span></figcaption><div class="mt-4">{bar_chart([18, 22, 19, 27, 24, 31], ["May", "Jun", "Jul", "Aug", "Sep", "Oct"], "Invoices sent per month, May to October 2026. October: 31, the most in six months.")}</div></figure>
        <figure><figcaption><span class="block font-bold">Where it stands</span><span class="block text-sm text-ink-2">By status, this quarter</span></figcaption>
          <div class="mt-4 flex items-center gap-5"><div class="w-[132px] shrink-0">{donut([("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")], "$63.8k", "invoiced", "Invoiced this quarter: $63,800. Paid 62%, open 21%, overdue 9%, draft 8%.")}</div>
          <ul class="grid gap-2 text-sm">{"".join(f'<li class="flex items-center justify-between gap-4"><span class="badge {l}">{n}</span><span class="tabular-nums text-ink-2">{p}%</span></li>' for n, p, l in (("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")))}</ul></div></figure>
        <figure><figcaption><span class="block font-bold">In a readout</span><span class="block text-sm text-ink-2">A sparkline on LCD glass</span></figcaption>
          <div class="lcd mt-4 px-5 py-4"><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Revenue · 12 mo</p><p class="text-2xl font-semibold mt-1">$44,900</p><div class="mt-3">{sparkline(REV)}</div></div></figure>
      </div>""", wide=True)}
    {group("Navigation &amp; data", ".nav-item  .seg  .ktable  .kbd  .lcd", f"""
      <div class="grid sm:grid-cols-[180px_1fr] gap-6 items-start">
        <nav class="flex flex-col gap-1" aria-label="Example"><a class="nav-item" href="#components" aria-current="page">{i("home")}Dashboard</a><a class="nav-item" href="#components">{i("file")}Invoices</a><a class="nav-item" href="#components">{i("users")}Customers</a></nav>
        <div class="flex flex-col gap-4 min-w-0">
          <div class="lcd px-5 py-3 flex gap-8"><div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Paid</p><p class="text-xl font-semibold">$48,210</p></div><div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Open</p><p class="text-xl font-semibold">$15,447</p></div></div>
          <p class="text-sm text-ink-2">Shortcut hints use <code class="font-mono">.kbd</code>. For example <span class="kbd">N</span> for a new invoice.</p>
        </div>
      </div>
      <div class="table-scroll mt-5">{table(CUSTOMERS[:3], select=False, actions=False, dates=False)}</div>""", wide=True)}
  </div>
</section>

<section id="screens" class="max-w-[1240px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <h2 class="display text-[40px] md:text-[56px]">App screens</h2>
  <p class="text-ink-2 text-lg max-w-[56ch] mt-5 mb-10">Full reference screens composed from the kit, on the same depth rules. Dense data stays flat and only the controls have depth. Try them on a phone too.</p>
  <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">{previews}</div>
</section>

<section id="marketing" class="max-w-[1240px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <h2 class="display text-[40px] md:text-[56px]">Marketing sections</h2>
  <p class="text-ink-2 text-lg max-w-[56ch] mt-5 mb-10">A landing page for the invoicing app above, and the sign-in it leads to: hero, features, pricing, questions, a call to action and a footer, built from the same parts.</p>
  <div class="grid gap-8 sm:grid-cols-2">{public_previews}</div>
</section>

<section id="tokens" class="max-w-[1240px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <h2 class="display text-[40px] md:text-[56px]">Tokens</h2>
  <div class="mt-10">
    <h3 class="engraved mb-4">Depth · four levels and the pressed state</h3>
    <div class="grid grid-cols-1 min-[480px]:grid-cols-2 lg:grid-cols-5 gap-x-4 gap-y-8">{DEPTH}</div>
    <p class="text-sm text-ink-2 max-w-[64ch] mt-6"><code class="font-mono">--k-depth</code> scales every offset and blur: <code class="font-mono">.depth-soft</code> sets it to 0.5 and <code class="font-mono">.depth-deep</code> to 1.7, on any region.</p>
  </div>
  <div class="grid gap-10 lg:grid-cols-2 mt-10">
    <div>
      <h3 class="engraved mb-4">Gray · warm, tuned to the light housing</h3>
      <div class="grid grid-cols-6 sm:grid-cols-12 gap-1.5">{"".join(f'<div class="min-w-0"><div class="h-12 rounded-md seam bg-gray-{n}" title="gray-{n}"></div><p class="font-mono text-[11px] text-ink-2 mt-1.5 text-center">{n}</p></div>' for n in (25,50,100,200,300,400,500,600,700,800,900,950))}</div>
      <h3 class="engraved mt-7 mb-4">Brand · signal orange</h3>
      <div class="grid grid-cols-6 sm:grid-cols-12 gap-1.5">{"".join(f'<div class="min-w-0"><div class="h-12 rounded-md seam bg-brand-{n}" title="brand-{n}"></div><p class="font-mono text-[11px] text-ink-2 mt-1.5 text-center">{n}</p></div>' for n in (25,50,100,200,300,400,500,600,700,800,900,950))}</div>
      <h3 class="engraved mt-7 mb-4">Success · Warning · Error</h3>
      <div class="grid grid-cols-6 gap-1.5">{"".join(f'<div class="min-w-0"><div class="h-10 rounded-md seam bg-{c}-{n}" title="{c}-{n}"></div><p class="font-mono text-[11px] text-ink-2 mt-1.5 text-center">{n}</p></div>' for c in ("success","warning","error") for n in (50,300,600))}</div>
    </div>
    <div>
      <h3 class="engraved mb-4">Type · Geist and Geist Mono</h3>
      <p class="display text-[48px] sm:text-[56px]">Display 700</p>
      <p class="text-[30px] font-bold tracking-[-0.015em] mt-4">Heading, 30 / bold</p>
      <p class="text-base mt-3 max-w-[52ch]">Body, 16 / regular. Geist throughout, sentence case everywhere. Display sizes tighten to −0.04em; UI text stays at default tracking.</p>
      <p class="font-mono text-sm mt-3">Readouts · Geist Mono · $48,210.00</p>
      <h3 class="engraved mt-8 mb-4">Motion</h3>
      <p class="text-sm text-ink-2 max-w-[52ch]">Press 80ms down, 160ms up. Toggles 200ms. Menus 180ms in, 120ms out. Dialogs 240ms in, 160ms out. One curve: <code class="font-mono">cubic-bezier(0.23, 1, 0.32, 1)</code>. Nothing moves on scroll.</p>
    </div>
  </div>
</section>

<section id="install" class="max-w-[1240px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <div class="grid gap-10 lg:grid-cols-[1fr_1.1fr] items-start [&>*]:min-w-0">
    <div>
      <h2 class="display text-[40px] md:text-[56px]">Install</h2>
      <p class="text-ink-2 text-lg max-w-[44ch] mt-5">Plastc isn’t on npm yet. It’s one CSS file you add next to your Tailwind v4 entry stylesheet.</p>
      <div class="flex flex-wrap gap-3 mt-8"><a class="btn btn-signal btn-lg" href="plastc.css" download>{i("down")}Download plastc.css</a><button type="button" class="btn btn-lg" data-copy='{IMPORT}'>{i("copy")}Copy the import</button></div>
      <p class="text-sm text-ink-2 mt-4 tabular-nums">v{VERSION} · {CSS_KB} KB · MIT-Licensed</p>
    </div>
    <ol class="grid grid-cols-1 gap-6 list-none p-0 m-0">
      <li><p class="font-bold mb-2">Add <code class="font-mono text-[14px]">plastc.css</code> to your project</p><p class="text-sm text-ink-2"><a class="text-ink underline" href="plastc.css" download>Download it</a>, or copy <a class="text-ink underline" href="{CSS_ON_GITHUB}"><code class="font-mono">src/plastc.css</code> on GitHub</a>. It holds the tokens, depth recipes and every component class.</p></li>
      <li><p class="font-bold mb-2">Import it after Tailwind</p>
        <pre class="code min-w-0">{IMPORT}</pre></li>
      <li><p class="font-bold mb-2">Load Geist</p>
        <div class="flex items-start gap-3"><pre class="code flex-1 min-w-0">&lt;link href="https://fonts.googleapis.com/css2?family=Geist:wght@400..800&amp;family=Geist+Mono:wght@400..600&amp;display=swap" rel="stylesheet"&gt;</pre><button class="btn btn-sm shrink-0 mt-1.5" data-copy='<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400..800&amp;family=Geist+Mono:wght@400..600&amp;display=swap" rel="stylesheet">'>{i("copy")}Copy</button></div></li>
      <li><p class="font-bold mb-2">Pick a housing</p><p class="text-sm text-ink-2">Light is the default. Add <code class="font-mono">data-housing="dark"</code> to <code class="font-mono">&lt;html&gt;</code> (or any section) for dark.</p></li>
    </ol>
  </div>
</section>
</main>
{VIEWER}
{command_dialog([
    ("Screens", [("home", "Dashboard", 'href="screens/dashboard.html" data-open-screen="dashboard"', ""), ("file", "Invoices", 'href="screens/invoices.html" data-open-screen="invoices"', ""), ("cog", "Settings", 'href="screens/settings.html" data-open-screen="settings"', ""), ("users", "Customers", 'href="screens/customers.html" data-open-screen="customers"', ""), ("chart", "Reports", 'href="screens/reports.html" data-open-screen="reports"', ""), ("box", "Products", 'href="screens/products.html" data-open-screen="products"', ""), ("key", "Sign in", 'href="screens/sign-in.html" data-open-screen="sign-in"', ""), ("send", "Landing page", 'href="screens/landing.html" data-open-screen="landing"', "")]),
    ("On this page", [("hash", label, f'href="#{k}"', "") for k, label in (("depth", "Depth"), ("components", "Components"), ("screens", "App screens"), ("marketing", "Marketing sections"), ("tokens", "Tokens"), ("install", "Install"))]),
    ("Actions", [HOUSING_CMD, ("down", "Download plastc.css", 'href="plastc.css" download', ""), ("copy", "Copy the import line", f"data-copy='{IMPORT}'", ""), ("external", "Source on GitHub", f'href="{REPO}"', "")]),
    ("Components", [("grid", title, f'href="#{gid}" data-keywords="{" ".join(re.findall(r"[.]([a-z][a-z0-9-]*)", classes))}"', "") for gid, title, classes in GROUPS]),
])}

<footer class="max-w-[1240px] mx-auto px-4 md:px-8 py-10 border-t border-[color:var(--k-seam)] flex flex-wrap gap-4 justify-between items-center text-sm text-ink-2">
  <p>© 2026 Thomas Guillot · MIT-Licensed · <a class="text-ink underline" href="{REPO}">Source on GitHub</a></p><a href="#top" class="btn btn-quiet btn-sm">Back to top</a>
</footer>
'''
showcase = showcase.replace("<!--jump-->", jump_list())
HOME_TITLE = "Neumorphic UI library for Tailwind CSS v4 · Plastc"
page("index.html", HOME_TITLE, showcase, description=DESCRIPTION, extra=f"""<link rel="canonical" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Plastc">
<meta property="og:title" content="{HOME_TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{SITE}/">
""")
print("built")
