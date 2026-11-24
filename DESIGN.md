# Plastc design system

Neumorphism as molded appliance plastic, for Tailwind CSS v4. Source of truth: `src/plastc.css`.

## Depth grammar (the rule everything follows)

| Level | Means | Used by | Recipe |
|---|---|---|---|
| Plane | The housing and every layout container | `.panel`, `.seam`, tables, charts, sidebars, page sections | Flush. Moulded seam: 1px parting line + highlight lip. No drop shadow. |
| Raised | A part you press | `.btn*`, `.key`, switch/range thumbs, selected `.seg` item, `.kbd` | `--k-raised`: specular top edge, lower lip, contact shadow, mid shadow, ambient falloff, faint top-left light bounce. Pressing swaps to `--k-pressed` and moves 1px. |
| Recessed | A part that holds input or output | `.field`, `.check`, `.radio`, `.switch` slot, `.seg` channel, `.range` track, `.lcd`, a checked `.choice-card`, `.meter`, the current `.nav-item` | `--k-recessed`: inner contact at top, soft inner fill, highlight lip on the lower outside edge. |
| Float | An overlay | `.menu`, `.dialog`, `.sheet`, `.toast`, `.tooltip` | `--k-float`: hairline, short + long ambient shadows. The only level with a long shadow. |

Never extrude data (chart bars, table rows, stat cards) or containers. If a thing is neither pressed nor filled, it is plane.

State drives depth: a `.choice-card` is flush until its input is checked, then recessed (`:has(:checked)`); a selected table row sinks to `housing-down`; a latched `.key[aria-pressed=true]` stays pressed. Nothing raised goes inside an `.lcd` (glass); actions printed on glass use `.lcd-action`.

One sanctioned exception: the showcase hero unit is a raised housing because it depicts a physical device. Product screens never raise a container.

LCD rule: the LCD is a material. As a readout set into the housing (KPI band, meter, empty-state counter) it is recessed. Toasts and tooltips are LCD labels cut as separate floating parts, so they take `--k-float`; nothing raised ever sits on LCD glass (use `.lcd-action`).

Dark recesses use a darker well (`--k-housing-down: #21201c`) and a dark edge ring (`--k-edge: rgb(0 0 0 / .55)`) so sunken parts read as sunken, not outlined. A latched `.key[aria-pressed=true]` sits in that darker well in both housings.

Light comes from the top-left. All shadows are alpha over `--k-sh` / `--k-hl`, scaled by `--k-sh-a` / `--k-hl-a` per housing, so one recipe works on both housings. `--k-depth` (0.5 to 1.7; `.depth-soft`, `.depth-deep`) scales offsets and blurs; recipes are re-declared on `[data-housing]`, `.depth-soft` and `.depth-deep` so they resolve locally.

## Housings

- **Light** (default, or `data-housing="light"`): `#dcd8cf` warm grey ABS, umber shadows, warm-white highlights.
- **Dark**: `data-housing="dark"` on any ancestor. `#2b2a27` smoked plastic; shadows strengthen (×2.6), highlights drop to 16%.

## Colour

- Semantic (housing-aware): `housing(-up/-down)`, `ink`, `ink-2` (secondary, ≥6:1), `ink-3` (placeholder, ≥4.5:1), `lcd`, `lcd-ink`, `lcd-dim`, `signal`, `signal-text` (orange for text on housing), `go`, `danger`, `warn`, `ok`.
- Scales: `gray-25…950` (warm, tuned to the light housing), `brand-25…950` (signal orange), `success`, `warning`, `error`.
- Signal orange marks the one primary action per view. Green (`btn-go`) is for confirm/positive actions. Status uses lamps (`.badge.lamp-*`), not filled pills.
- The sage LCD is a readout material: key figures, toasts, tooltips, code lines. Text inside is Geist Mono.

## Type

Geist for everything; Geist Mono for readouts and code. Sentence case throughout.
Display `.display`: 700, line-height 0.96, tracking −0.04em, 40–96px. Page title 28–30/700/−0.015em. Body 14–16. Labels 13/700. Engraved section labels `.engraved`: 11/700, +0.09em, uppercase. Minimum functional size 11px.

## Naming

Classes are unprefixed (`btn`, `field`, `panel`), the same convention as other Tailwind component libraries. Every class is a Tailwind `@utility`, so variants work (`md:btn-lg`).

## Accessibility

Every text token is checked against both WCAG 2 (ratio) and APCA (Lc, W3C draft 0.0.98G). Targets: body text Lc 75+, labels and short bold text Lc 60+, placeholders and large text Lc 45+. WCAG 2 alone overrates light-on-dark, so dark-housing tokens are tuned to APCA.

| Pair | Light WCAG | Light Lc | Dark WCAG | Dark Lc |
|---|---|---|---|---|
| Body ink | 11.8:1 | 81 | 12.3:1 | 92 |
| Secondary ink-2 | 8.8:1 | 76 | 10.0:1 | 79 |
| Placeholder ink-3 | 4.9:1 | 58 | 6.2:1 | 50 |
| Orange button label (white on `#c4470e`→`#b23c0a`, both housings) | 4.9–5.9:1 | 79–84 | same | same |
| Green button label | 4.7:1 | 78 | 4.7:1 | 78 |
| Orange text (`signal-text`, reserved; links now use ink + underline) | 6.3:1 | 67 | 7.6:1 | 63 |
| Error text / overdue counts | 6.2:1 | 66 | 8.8:1 | 71 (69 on menus) |
| LCD text | 8.9:1 | 67 | 10.8:1 | 81 |
| LCD labels (11px caps) | 6.9:1 | 62 | 8.6:1 | 67 |
| Focus ring vs housing | 11.8:1 | 81 | 12.3:1 | 92 |

Disabled text (`--k-ink-off`) is deliberately below these (about 3:1); WCAG exempts disabled controls.

Orange is only the primary action (plus the range fill). Overdue counts use `danger` (matching the red lamps); links are ink and underlined; the chart highlight is ink; text selection is an ink tint.

Focus is its own token: a 2px ink ring (light ink in dark) with an offset, never orange, so it can't be confused with the primary action or an error. Orange means "the primary action" (plus the range fill); radio dots are ink. Field edges carry a 30% umber ring; a `forced-colors` block gives every part a real border in Windows High Contrast. The housings are called light and dark everywhere: labels, docs and the `data-housing` values.

Pressing a coloured button keeps its colour: variants set `--btn-pressed-bg` / `--btn-pressed-shadow`, which `.btn:active` reads.

## Components

Buttons `.btn` + `.btn-signal | .btn-go | .btn-quiet | .btn-danger`, sizes `.btn-sm | -md | -lg | -xl | -2xl`, `.btn-icon`, states `:disabled`, `aria-busy`, `aria-pressed`.
Fields `.field`, `.field-select`, `.field-area`, `.label`, `.hint`, `.hint-error`, invalid via `aria-invalid="true"`.
Selection `.check`, `.radio`, `.switch` (`role="switch"`), `.seg` (children use `aria-pressed`, `aria-selected` or `aria-current`), `.range` (`--fill`).
Overlays `.menu` (on `[popover]`, anchored with CSS anchor positioning), `.dialog` and `.sheet` (on `<dialog>`), `.toast` (on `[popover=manual]`), `.tooltip` (`data-tip`), `.lcd-action`.
Selection also `.choice-card`. Code `.code`. Tables `.table-scroll` (edge fade on narrow screens).
Display `.panel`, `.raised`, `.recessed`, `.seam`, `.float`, `.lcd`, `.meter`, `.badge` + `.lamp-ok|warn|danger|signal|off`, `.tag`, `.avatar`, `.alert`, `.ktable` (`.num` cells), `.nav-item`, `.menu`, `.dialog`, `.toast`, `.kbd`, `.key`.

## Motion

One curve: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` (plus `--ease-drawer` for the sheet). Durations are custom properties on `:root`.

| What | Timing | Notes |
|---|---|---|
| Press (`.btn`, `.key`, `.pressable`) | 80ms down, 160ms up | 1px drop, scale 0.985, shadow reverses to `--k-pressed`. Asymmetric: the `:active` state carries the shorter duration. No bounce. |
| Hover | 160ms | Gated to `(hover: hover) and (pointer: fine)`. Light catches the top edge (`--k-raised-hover`); geometry does not move. |
| Toggles (switch, check, radio, choice card, seg) | 160–200ms | Marks scale from 0.5, never from 0. Seg selection latches without travel. |
| Menu (`[popover]`) | 180ms in, 120ms out | Opacity + scale 0.96 from the trigger corner. Native popover: Esc and outside click close it. Items are plain buttons (no `role=menu`), so Tab works and nothing promises arrow keys. |
| Dialog (`<dialog>`) | 240ms in, 160ms out | Opacity + scale 0.96 from centre; backdrop fades with it. |
| Sheet | 300ms in, 220ms out | Slides from the left edge on `--ease-drawer`. |
| Toast (`[popover=manual]`) | 360ms in, 240ms out, `ease` | Rises from the bottom (bottom-right on desktop) and leaves the same way. Stays 6s, pauses on hover or focus; Undo also on `Z`. |
| Keyboard shortcuts | none | Overlays opened by a shortcut get `.no-motion`. |
| Tooltip | 125ms, 400ms hover delay | Esc dismisses it at once (`data-tip-off`, WCAG 1.4.13). |

Nothing animates on scroll. Reduced motion keeps fades and colour changes and drops translate/scale; the sheet fades instead of sliding; the busy spinner slows to 1.6s instead of stopping.

## Screens

`site/screens/`: dashboard, invoices (filter tabs, search, bulk selection, row menus, void with confirm + undo, empty state, pagination), settings (tabbed: profile, notifications, billing with choice cards, team, API), sign-in (validation, error, busy). Customers, Reports and Products are honest "not built yet" pages. Mobile: top bar + navigation sheet. Shortcuts: `/` search, `N` new invoice. Sample data only.
