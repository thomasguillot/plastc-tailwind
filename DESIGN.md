# Plastc design system

Neumorphism as molded appliance plastic, for Tailwind CSS v4. Source of truth: `src/plastc.css`.

## Depth grammar (the rule everything follows)

| Level | Means | Used by | Recipe |
|---|---|---|---|
| Plane | The housing and every layout container | `.panel`, `.seam`, `.tabs`, `.empty`, `.accordion`, `.desc-list`, `.timeline`, `.chart`, tables, charts, sidebars, page sections | Flush. Moulded seam: 1px parting line + highlight lip. No drop shadow. |
| Raised | A part you press | `.btn*`, `.key`, switch/range thumbs, selected `.seg` item, `.kbd` | `--k-raised`: specular top edge, lower lip, contact shadow, mid shadow, ambient falloff, faint top-left light bounce. Pressing swaps to `--k-pressed` and moves 1px. |
| Recessed | A part that holds input or output | `.field`, `.input-group`, `.check`, `.radio`, `.switch` slot, `.range` track, `.lcd`, a checked `.choice-card`, the selected `.calendar` day, `.progress`, `.dropzone`, `.meter`, the current `.nav-item` | `--k-recessed`: inner contact at top, soft inner fill, highlight lip on the lower outside edge. |
| Float | An overlay | `.menu`, `.popover`, an open `.combobox` list, `.dialog`, `.sheet`, `.toast`, `.tooltip` | `--k-float`: hairline, short + long ambient shadows. The only level with a long shadow. |

Never extrude data (chart bars, table rows, stat cards) or containers. If a thing is neither pressed nor filled, it is plane.

State drives depth: a `.choice-card` is flush until its input is checked, then recessed (`:has(:checked)`); a selected table row (any checked checkbox in its cells) sinks to `housing-down` with a recessed top edge and ignores the hover tint; a latched `.key` or `.btn` (`aria-pressed="true"`) stays down in a dark well (see Latching). Nothing raised goes inside an `.lcd` (glass); actions printed on glass use `.lcd-action`.

One sanctioned exception: the showcase hero unit is a raised housing because it depicts a physical device. Product screens never raise a container.

LCD rule: the LCD is a material. As a readout set into the housing (KPI band, meter, empty-state counter) it is recessed. Toasts and tooltips are LCD labels cut as separate floating parts, so they take `--k-float`; nothing raised ever sits on LCD glass (use `.lcd-action`).

Dark recesses use a darker well (`--k-housing-down: #21201c`) and a dark edge ring (`--k-edge: rgb(0 0 0 / .55)`) so sunken parts read as sunken, not outlined.

## Latching

A press and a latch are different states and never look the same.

- **Press** (`:active`, momentary): the part drops 1px, shrinks to 0.985 and its shadow turns to `--k-pressed` on its own plastic (`housing` for neutral parts, the cap color for `.btn-signal` and `.btn-go`). It comes back up on release.
- **Latched** (`aria-pressed="true"` on a `.key` or a `.btn`, held): the part stays down 1px without shrinking, and sits in a darker well (see below). Pressing a latched part shrinks it while the well stays.
- **Chosen** (`.seg`, exclusive choice): the channel looks exactly like a latched button (`--k-well` with `--k-latched`), and the chosen item is the one raised part in it, with a cast body and a light shadow (`--k-cast`, specular top edge, short contact and mid shadows) and an ink label. It does not travel, because picking one option is a selection, not a toggle.
- **Chosen key** (a group of exclusive `.key`s): mark the group up as radios, not toggles. The wrapper is `role="radiogroup"` with a label, each key is `role="radio"` with `aria-checked`, and only the checked key is in the tab order (`tabindex="0"`, the rest `-1`); arrow keys move to the next key and check it. `.key[aria-checked="true"]` sinks into the same well as a latched key (down 1px, `--k-well` with `--k-latched`), with no extra mark. The others stay raised. Never use `aria-pressed` for a choice of one: every key would latch on its own.

The latched look comes from the plastic alone, with no light, dot or glow. The body drops into `--k-well`, a darker fill than `housing-down` (`#c1bbaf` light, `#171613` dark), and takes `--k-latched`: a deep inner shadow from the top and a highlight under the outside edge. Colored caps keep their own color (`--btn-latched-bg`) and take the same inner shadow (`--btn-latched-shadow`). Padding is the same latched or not, so the label never shifts. A disabled latched part shows the dashed outline only, the same as any disabled part.

Light comes from the top-left. All shadows are alpha over `--k-sh` / `--k-hl`, scaled by `--k-sh-a` / `--k-hl-a` per theme, so one recipe works in both themes. `--k-depth` (0.5 to 1.7; `.depth-soft`, `.depth-deep`) scales offsets and blurs; recipes are re-declared on `[data-theme]`, `.depth-soft` and `.depth-deep` so they resolve locally.

## Themes

- **Light** (default, or `data-theme="light"`): `#dcd8cf` warm grey ABS, umber shadows, warm-white highlights.
- **Dark**: `data-theme="dark"` on any ancestor. `#2b2a27` smoked plastic; shadows strengthen (×2.6), highlights drop to 16%.

## Colour

- Semantic (theme-aware): `housing(-up/-down)`, `ink`, `ink-2` (secondary, ≥6:1), `ink-3` (placeholder, ≥4.5:1), `lcd`, `lcd-ink`, `lcd-dim`, `signal`, `signal-text` (orange for text on housing), `go`, `danger`, `warn`, `ok`.
- Scales: `gray-25…950` (warm, tuned to the light theme), `brand-25…950` (signal orange), `success`, `warning`, `error`.
- Signal orange marks the one primary action per view. Green (`btn-go`) is for confirm/positive actions. Status uses lamps (`.badge.lamp-*`), not filled pills.
- The sage LCD is a readout material: key figures, toasts, tooltips, code lines. Text inside is Geist Mono.

## Type

Geist for everything; Geist Mono for readouts and code. Sentence case throughout.
Display `.display`: 700, line-height 0.96, tracking −0.04em, 40–96px. Page title 28–30/700/−0.015em. Body 14–16. Labels 13/700. Engraved section labels `.engraved`: 11/700, +0.09em, uppercase. Minimum functional size 11px.

## Naming

Classes are unprefixed (`btn`, `field`, `panel`), the same convention as other Tailwind component libraries. Every class is a Tailwind `@utility`, so variants work (`md:btn-lg`).

## Accessibility

Every text token is checked against both WCAG 2 (ratio) and APCA (Lc, W3C draft 0.0.98G). Targets: body text Lc 75+, labels and short bold text Lc 60+, placeholders and large text Lc 45+. WCAG 2 alone overrates light-on-dark, so dark-theme tokens are tuned to APCA.

| Pair | Light WCAG | Light Lc | Dark WCAG | Dark Lc |
|---|---|---|---|---|
| Body ink | 11.8:1 | 81 | 12.3:1 | 92 |
| Secondary ink-2 | 8.8:1 | 76 | 10.0:1 | 79 |
| Placeholder ink-3 | 4.9:1 | 58 | 6.2:1 | 50 |
| Input affix (ink-2 in a recessed well) | 7.9:1 | 69 | 11.4:1 | 80 |
| Orange button label (white on `#c4470e`→`#b23c0a`, both themes) | 4.9–5.9:1 | 79–84 | same | same |
| Green button label | 4.7:1 | 78 | 4.7:1 | 78 |
| Orange text (`signal-text`, reserved; links now use ink + underline) | 6.3:1 | 67 | 7.6:1 | 63 |
| Error text / overdue counts | 6.2:1 | 66 | 8.8:1 | 71 (69 on menus) |
| LCD text | 8.9:1 | 67 | 10.8:1 | 81 |
| LCD labels (11px caps) | 6.9:1 | 62 | 8.6:1 | 67 |
| Focus ring vs housing | 11.8:1 | 81 | 12.3:1 | 92 |
| Latched label (ink on `--k-well`) | 8.8:1 | 65 | 15.5:1 | 95 |
| Latched vs unlatched face, measured (non-text) | 1.37–1.43:1 (caps 1.47–1.53:1) | n/a | 1.26–1.31:1 (caps 1.47–1.53:1) | n/a |
| Switch slot on vs off (`--k-switch-on` vs `housing-down`) | 4.0:1 | 52 | 4.3:1 | 34 |
| Switch thumb vs on slot | 5.0:1 | 69 | 3.8:1 | 34 |

Disabled text (`--k-ink-off`) is deliberately below these (about 3:1); WCAG exempts disabled controls.

Orange is only the primary action (plus the range fill). Overdue counts use `danger` (matching the red lamps); links are ink and underlined; the chart highlight is ink; text selection is an ink tint.

Focus is its own token: a 2px ink ring (light ink in dark) with an offset, never orange, so it can't be confused with the primary action or an error. Orange means "the primary action" (plus the range fill); radio dots are ink. Field edges carry a 30% umber ring; a `forced-colors` block gives every part a real border in Windows High Contrast. There, a disabled `.btn` or `.key` takes a dashed `GrayText` border and `GrayText` label; a latched or chosen `.btn`, `.key` or `.choice-card` takes a `Highlight` border and outline, and a disabled latched `.btn` or `.key` takes a 2px dashed `GrayText` border instead of 1px, and on focus the outline turns `CanvasText` 3px out while the border stays `Highlight`; a chosen `.seg` item, the current `.nav-item` and the chosen calendar day fill with `Highlight` and `HighlightText`, with a `HighlightText` focus ring inside the chosen segment; the `.range` fill is `Highlight` and its thumb `ButtonText` with a `Canvas` ring. The themes are called light and dark everywhere: labels, docs and the `data-theme` values.

Pressing a coloured button keeps its colour: variants set `--btn-pressed-bg` / `--btn-pressed-shadow`, which `.btn:active` reads.

## Components

Buttons `.btn` + `.btn-signal | .btn-go | .btn-quiet | .btn-danger`, sizes `.btn-sm | -md | -lg | -xl | -2xl`, `.btn-icon`, states `:disabled`, `aria-busy`, `aria-pressed`. A busy `.btn-icon` hides its icon and shows only the spinner, at the same size. A `.key` takes `:disabled` or `aria-disabled="true"` the same way as a button: no body, a dashed outline, faded ink, and it no longer presses or lifts on hover. Hover never outranks a press: a pressed or latched button or key always shows `--k-pressed`. Variant hovers (`.btn-signal` lights its own cap, `.btn-quiet` shows its seam) outrank the base `.btn` hover, whose exclusions sit in `:where()`.
Fields `.field`, `.field-select`, `.field-area`, `.label`, `.hint`, `.hint-error`, invalid via `aria-invalid="true"`.
Input groups `.input-group` is one recessed well around a bare `<input>`: a leading or trailing icon, `.input-affix` text (a seam divides it from the value), a `.kbd` hint, or a `.btn` set into the well like the raised item in a `.seg` channel, with concentric corners (the well's radius minus the 4px inset) rather than a pill. Focus, invalid and disabled are read from the input. Wrap it in a `<label>` when it holds no button; with a button, use a `<div>` and a separate `<label for>`.
Tabs `.tabs` switch the panels of one page (`role="tablist"` with `aria-selected`) or the sections of a page (links with `aria-current="page"`): plane, on a seam, with an ink indicator under the current tab. Filters and view modes inside a panel stay `.seg`.
Pagination `.pager` lays out Previous, a middle slot, and Next. The middle slot holds `.seg.pager-pages` (page buttons with `aria-current="page"`, `<span>` for a gap) and/or `.pager-status`. Below 640px the page numbers hide and the status shows; with no page numbers, the status always shows.
Breadcrumbs `.breadcrumbs` on an `<ol>` inside `<nav aria-label="Breadcrumb">`; the last item carries `aria-current="page"`. Plane: text with slash separators.
Long-form reading `.prose` styles unclassed article markup: 17px (18px from 768px) on a 1.7 line height, capped at 36em, which measures about 72 characters a line in Geist. Headings get more space above than below (h2 2.1em above, 0.6em below). Links are ink, underlined, offset 0.22em, and thicken on hover. Bare `ul`/`ol` get markers in ink-2; lists with a class (a `.timeline`, a `.check-list`) keep their own look. A `blockquote` stays on the plane behind a 1px seam rule. Inline `code` is a Geist Mono chip recessed into `housing-down` (ink on it: 10.5:1, Lc 74 light; 13.9:1, Lc 94 dark; used for short runs only). A `pre` is the `.code` well at 14px, a `table` is the `.ktable` recipe with wrapping cells (wrap it in `.table-scroll`), `figcaption` is 14px ink-2, and `hr` is a seam. Figures hold live parts of the kit, not placeholder images.
Posts `.post-card` is a plane card whose title link stretches over the whole card: hover tints it `housing-up` and underlines the title, and keyboard focus rings the card. `data-featured` sets it in two columns from 768px with a larger title. `.post-meta` is a line of category, `<time>` and reading time separated by dots that screen readers skip. `.byline` sets an `.avatar` beside a `<strong>` name and a role or `.post-meta`. The sample blog (`site/src/pages/screens/blog.astro`, posts in `site/src/content/posts/`) filters posts by category and search with a small script in `plastc.js` and reads `?category=` from the URL; the article (`article.html`) shows the full reading style.
Combobox `.combobox` wraps an `.input-group` whose `<input>` has `role="combobox"`, `aria-controls` and `aria-expanded`, plus a `.listbox` that floats under it. Options are `role="option"`; `aria-selected="true"` adds a check and `data-active` marks the option `aria-activedescendant` points at. The library styles the states; filtering and arrow keys are your script's job (the showcase's `plastc.js` shows one way).
Date picker: a `.calendar` of day buttons (`aria-pressed="true"` sinks the chosen day into a recess, `aria-current="date"` puts a dot under today, `data-outside` dims the neighbouring months) inside a `.popover` anchored to an input group. The calendar also sits flat on the page on its own.
Popover `.popover` is the float panel for rich content on `[popover]`; `.menu` stays the panel for a list of actions.
Command menu `.dialog.command`: a search `.input-group`, a `.listbox` of `role="group"` sections with `.listbox-label` headings, and `.command-hints` along the bottom. The showcase and the app screens open it with Cmd+K or Ctrl+K.
Progress `.progress` is a recessed channel with an ink fill (`role="progressbar"`, `aria-valuenow`, the fill's `--v`). Without `aria-valuenow` it runs indeterminate. It is for a task in progress; `.meter` stays the LCD readout of a level.
Spinner `.spinner` (`.spinner-lg`, or set `--spinner-size`) for a wait with no measurable progress; pair it with `role="status"` and hidden text. Skeleton `.skeleton` blocks stand in for content while it loads; size them with utilities and label the region (`role="status"`, `aria-label`).
File upload: `.dropzone` is a recessed `<label>` around a file input, with `data-dragover` while a file is held over it. Each file is a `.file-item` row: `.file-icon`, `.file-name` and `.file-meta` (`.file-error` for a problem), an action button, and an optional `.progress` under the name.
Accordion `.accordion` holds native `<details>`/`<summary>` rows divided by seams. A summary tints to `housing-up` on hover, like a table row. Browsers with `::details-content` open it smoothly; others open at once.
Description list `.desc-list` on a `<dl>` of `<div><dt><dd></div>` rows; it stacks below 640px.
Avatar group `.avatar-group`: overlapping `.avatar`s with a ring the colour of the surface (`--ring`, the housing by default). A `button.avatar` at the end can open a `.popover` with the rest.
Timeline `.timeline` on an `<ol>`: each `<li>` gets a lamp dot (`lamp-ok`, `lamp-warn`, …) and a `<time>` underneath.
People `.people` on a `<ul>`: a grid of `<li>` rows divided by seams, each an `.avatar` (initials, 48px) beside `.people-name` and `.people-role`. It sits on the plane; nobody gets a floating card.
Role list `.role-list` on a `<ul>` for open positions or any list of things with one action each: every `<li>` holds a `.role-title`, a `.role-meta` line (team, place, type) and a `.btn.btn-sm` on the right, which wraps under the text on narrow screens. Rows are plane, divided by seams.
Charts: put `.chart` on an SVG and use `.chart-grid`, `.chart-bar` (`data-current` turns one bar ink), `.chart-value`, `.chart-track` and `.chart-seg` with a `lamp-*` class for donut segments, and `.chart-total`. Bars are plane, like all data. Bar charts are HTML: `.bar-chart` holds `.bar` elements sized by `--v` (percent of the tallest) with their value in a `<span>` above, and `.bar-chart-axis` holds the labels; `data-current` marks the period in focus. Every bar shows its value, so the bars can stay a light tint without the reading depending on them. `.sparkline` is a stroke-only SVG that takes the colour of its parent, so it reads in LCD ink inside a `.lcd`. Give every chart `role="img"` and an `aria-label` that states the numbers.
Pricing `.plan` is a plane card (`data-featured` outlines the recommended one, which also carries the page's orange button), with `.plan-price` for the figure and a `<small>` unit. `.check-list` is a list with ink checks, for plan features or any "what you get" list.
Plan comparison: `.compare` on a `.ktable` inside `.table-scroll`. One `<tbody>` per group, opened by a `tr.compare-group` row (`<th scope="rowgroup">` plus an empty cell per plan); feature rows use `<th scope="row">`, which stays pinned to the left edge while the table scrolls sideways on phones. Plan headers hold `.compare-plan` and `.compare-price`; cells hold a value or `.compare-yes` / `.compare-no` with hidden text ("Included", "Not included"). `data-featured` on the recommended plan's header and cells lights that column with `housing-up`; it stays plane.
Stats `.stat` on a `<div>` inside a `<dl>`: a `<dt>` label (11px caps), a `.stat-value` `<dd>` and an optional caption `<dd>`. Set the `<dl>` on an `.lcd` to make a readout band (the label turns `lcd-dim`); outside an LCD the label is `ink-2`.
Logo strip `.logo-strip` on a `<ul>` of customer names set as type in `ink-2`, wrapping and centered, spread across one row on wide screens. Set names in the kit's own fonts; never imitate a real brand's mark.
Quotes `.quotes` holds `<figure class="quote">` items (`<blockquote>`, then a `<figcaption>` with an `.avatar` and a `<strong>` name over the role). They sit on the plane between seams, stacked on phones and side by side from 768px. No cards.
Newsletter sign-up is a composition: an `.input-group` with an icon, an email input and a `.btn` set into the well, a `.hint` that says what is sent and how often, `.hint-error` with `aria-invalid` for a bad address, and a confirmation that replaces the form and takes focus.
Sample content: on a sample marketing page, every logo strip, quote and figure carries a visible note that it is made up.
Marketing pages are compositions, not new materials: the reference landing page (`site/src/pages/screens/landing.astro`) builds its hero, feature rows, pricing, questions, call to action and footer from the classes above. Each feature is illustrated with a live part of the kit rather than an icon card. Sample proof (logos, quotes, figures) is allowed only on the sample product's pages and must say on the page that it is made up; the library's own showcase never carries any. The marketing pages live one per file in `site/src/pages/screens/` and share a header, an optional announcement `.banner` and a footer through the `Marketing` layout in `site/src/layouts/Marketing.astro`.
Empty states `.empty` centre an LCD `.lcd.readout` (`.readout-value`, `.readout-unit`), a heading, a short reason and `.empty-actions`. Say why it is empty and what to do next; the copy depends on the cause (no data yet, a filter, a search).
Selection `.check`, `.radio` (20px, 24px on coarse pointers), `.switch` (`role="switch"`), `.seg` (children use `aria-pressed`, `aria-selected` or `aria-current`), `.range` (`--fill`; the input is a 24px hit area with negative margins, so it takes the 10px of the track in the layout and never reaches past a label's 7px margin; on coarse pointers it is 44px and takes its full height, so it never covers its neighbors; the track, fill and focus ring are drawn on the track in every browser). `.check` and `.radio` take `aria-invalid="true"` with the same 2px danger ring as a field. Hover is deliberately absent on fields, input groups, checks, radios, switches and ranges.
Disabled follows one grammar everywhere: faded ink (`--k-ink-off`), a `not-allowed` cursor, and no hover or press response. Raised parts lose their body for a dashed outline (`.btn`, `.key`, the chosen `.seg` item, the `.range` thumb); recessed parts drop their well for a seam ring (`.field`, `.input-group`, a whole `.seg`, the `.range` track, `.dropzone`); flat items only fade (`.tabs` items, `.menu` items, `.nav-item`, listbox options); a `.choice-card` takes the dashed outline and fades everything inside it. Use `:disabled` on form controls and `aria-disabled="true"` elsewhere: `.btn`, `.key`, `.seg` and its items, `.tabs` items, `.menu` items, `.nav-item`, `.dropzone` and `.choice-card` accept both, and the drop zone and choice card also read a disabled input inside them. `.dropzone` takes invalid from `aria-invalid="true"` on its input or itself; `data-dragover` outranks invalid, so a new drag after a rejected file still shows its ring.
Overlays `.menu` (on `[popover]`, anchored with CSS anchor positioning), `.dialog` and `.sheet` (on `<dialog>`; add `.dialog-full` for a 90vw × 90vh dialog that holds a full view, nearly edge to edge on phones), `.toast` (on `[popover=manual]`), `.tooltip` (`data-tip`), `.lcd-action`.
Selection also `.choice-card`. Code `.code`. Tables `.table-scroll` (edge fade on narrow screens).
Display `.panel`, `.raised`, `.recessed`, `.seam`, `.float`, `.lcd`, `.meter`, `.badge` + `.lamp-ok|warn|danger|signal|off`, `.tag`, `.avatar`, `.alert`, `.banner`, `.ktable` (`.num` cells), `.nav-item`, `.menu`, `.dialog`, `.toast`, `.kbd`, `.key`.

## Motion

One curve: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` (plus `--ease-drawer` for the sheet). Durations are custom properties on `:root`.

| What | Timing | Notes |
|---|---|---|
| Press (`.btn`, `.key`, `.pressable`) | 80ms down, 160ms up | 1px drop, scale 0.985, shadow reverses to `--k-pressed`. Asymmetric: the `:active` state carries the shorter duration. No bounce. |
| Latch (`aria-pressed` on `.btn`, `.key`) | 160ms into the well | The body and its shadow settle into the well on the press-up timing. Reduced motion: no 1px drop, the well still changes. |
| Hover | 160ms | Gated to `(hover: hover) and (pointer: fine)`. Light catches the top edge (`--k-raised-hover`); geometry does not move. |
| Toggles (switch, check, radio, choice card, seg) | 160–200ms | Marks scale from 0.5, never from 0. Seg selection latches without travel. |
| Menu (`[popover]`) | 180ms in, 120ms out | Opacity + scale 0.96 from the trigger corner. When it flips above its trigger, the origin flips with it (the reference script sets `transform-origin` on `toggle`). Native popover: Esc and outside click close it. Items are plain buttons (no `role=menu`), so Tab works and nothing promises arrow keys. |
| Dialog (`<dialog>`) | 240ms in, 160ms out | Opacity + scale 0.96 from centre; backdrop fades with it. |
| Sheet | 300ms in, 220ms out | Slides from the left edge on `--ease-drawer`. |
| Toast (`[popover=manual]`) | 360ms in, 240ms out, `ease` | Rises from the bottom (bottom-right on desktop) and leaves the same way. Stays 6s, pauses on hover or focus; Undo also on `Z`. App screens pad the bottom of the main area so the last row scrolls clear, and a menu opened over a toast renders above it. |
| Keyboard shortcuts | none | Overlays opened by a shortcut get `.no-motion`. |
| Popover, combobox list | 180ms in; the popover leaves in 120ms, the list closes at once | Opacity + scale 0.96–0.97 from the anchored edge. |
| Progress, spinner, skeleton | 300ms fill, 700ms spin, 1.5–1.6s loops | The fill reveals with `clip-path`, not `width`, so it never triggers layout. Loops run `linear`. Reduced motion: the indeterminate bar and skeletons breathe in place instead of sweeping; the spinner slows. |
| Accordion | 240ms open, 200ms chevron, 120ms hover tint | Height animates with `interpolate-size` where supported. Reduced motion opens at once. |
| Tabs | 120ms colour, 160ms indicator | The indicator appears under the new tab; it never slides across. |
| Tooltip | 125ms, 400ms hover delay | Hover is gated to fine pointers, so a tap never leaves it stuck open; keyboard focus shows it at once. Esc dismisses it at once (`data-tip-off`, WCAG 1.4.13). |
| Banner dismiss | 220ms | Collapses its height and fades, so the page closes the gap instead of jumping. Reduced motion: a 120ms fade. |
| Pricing toggle | 180ms | Changed figures fade in from a 2px blur and a 4px drop. Reduced motion: fade only. |
| In-page links (homepage only) | browser smooth scroll | `html{scroll-behavior:smooth}` on `index.astro`, so jumps from the header and the Cmd/Ctrl+K menu glide to their section. Reduced motion: `scroll-behavior:auto`, the page jumps. |
| Invoice totals tick (`LightDark.astro`) | 180ms, `--ease-out` | A changed line total, subtotal, tax or total fades in from a 2px blur and a 4px drop, through the Web Animations API. It skips while one is still running, so held keys never queue animations. Reduced motion: fade only. |
| Class name labels (`.annot`, homepage) | 240ms height and margin, 180ms opacity | "Show class names" opens each label's height from 0 with `interpolate-size`, so the panes grow instead of jumping. Reduced motion: opacity only, the height changes at once. |
| Screen viewer (`ScreenViewer.astro`) | 200ms fade in, none out | The iframe hides while a page loads (`data-loading`, no transition) and fades in once it has loaded, so a half-painted page never shows. Opacity only, so reduced motion keeps it. |
| Chart legend dimming (`StatusShare`) | none | Hovering or focusing a legend row dims the other segments and rows to 35% at once. It follows the pointer across rows, so any fade would lag behind it. |
| Accordion hover tint | 120ms, `ease` | A summary tints to `housing-up`, like a table row. Color only, so reduced motion keeps it. |

Nothing in the library or the app screens animates on scroll. Reduced motion keeps fades and colour changes and drops translate/scale; the sheet fades instead of sliding; the busy spinner slows to 1.6s instead of stopping.

One sanctioned exception, on the marketing showcase only: scroll-linked motion that explains the kit. The homepage wall drifts each row of screens sideways as the page scrolls (linear, tied to the first 100vh of scroll, `translate` only, through `animation-timeline: scroll()` with a rAF fallback that runs only while the wall is on screen). The anatomy section steps through its six layers as its track scrolls past; a click pins a layer (the row latches and shows a Pinned badge; an Auto key returns to stepping) and pauses the stepping until the track leaves the viewport, hover and focus preview a layer without overriding the pin, and in-page jumps skip the layers they pass. Theme and depth changes suspend all transitions for two frames (`data-retheme`, set by the demo script) so nothing fades behind the switch. The wall's loading placeholders shimmer only while on screen and stop once their screen has loaded. Reduced motion: the wall stays still, and the stepping still runs because it changes state rather than moving anything (its layer changes keep their 180ms fades). Library components and app screens never use either.

## Showcase

The homepage (`/`, `site/src/pages/index.astro`) runs in order: the hero with the wall of screens, the anatomy section, light and dark (the tuning deck and the two invoice panes), contrast, and install. The hero's primary action downloads `plastc.css`, which the build copies from `src/plastc.css`, with the version from `package.json` and the file size beside it; Install links the same download and the file on GitHub, and the header and footer link the repository. The Cmd/Ctrl+K menu lists the screens, the marketing pages, the sections of the homepage, the components index and the component pages (searchable by class name).

Components live at `/components/` (an index of the groups) and one page per group at `/components/<slug>/` (`site/src/pages/components/[slug].astro`, content in `site/src/components/components/pages.ts`). Each page has Examples (the live parts), Tokens where the group has its own, States (a state matrix from `matrices.ts`: every part in default, hover, focus, pressed, on, disabled, invalid and busy, with hover, focus and pressed held on by the site-only `data-force` attribute whose rules in `state-matrix.css` copy the library's), and Classes. Under each example, View HTML (a native `<details>`) shows clean markup that the build derives from the live demo's rendered HTML (`site/src/lib/clean-html.ts`): demo-only `data-*` hooks and notes are stripped, the `data-*` attributes the library styles are kept, dialog triggers become `commandfor`/`command`, and a script-built calendar is written out as a static month. Copy HTML copies exactly that text, keeps its icon (a check once copied) and holds its width. Where a part needs your own script, one line above the code says what and links `plastc.js`.

The homepage's tuning deck sets the depth (Soft, Normal, Deep) and an LCD tint (green, amber, blue) for the whole page. The theme is set by the header switch and the tint by the deck. The Contrast section has no controls of its own; its readout follows both. The tint is a showcase control, not a library token: green is the shipped `--k-lcd` set, and the contrast readout recomputes its LCD text figures (WCAG 2 and APCA 0.0.98G) for whichever tint is showing.

## Screens

`site/src/pages/screens/` (built to `screens/`): the marketing pages (landing, pricing, blog, article, about with careers, contact, 404), dashboard, invoices (filter tabs, search, bulk selection, row menus, void with confirm + undo, empty state, pagination), customers (filter switch, search, balances, row menus, empty state), reports (date range, LCD summary, revenue, invoices sent, status donut, top customers), products (active and archived, add product dialog), settings (tabbed: profile, notifications, billing with choice cards, team, API), sign-in (validation, error, busy). Mobile: top bar + navigation sheet. Shortcuts: `/` search, `N` new invoice, Cmd/Ctrl+K command menu. Sample data only, and the numbers agree across screens.
