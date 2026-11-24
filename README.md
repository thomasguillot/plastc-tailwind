<img src="site/mark-light.svg" alt="" width="96" height="96">

# Plastc

*Every button a real button.*

A neumorphic UI library for Tailwind CSS v4, cast as molded appliance plastic. Parts you press stand up, parts that hold input sit in, and everything else stays flush.

**→ [Website](https://plastc.space.fast/)**: every component live, plus full reference screens in light and dark.

**Requires Tailwind CSS v4. Not on npm yet: it is one CSS file you copy into your project.**

---

## For users

### What it does

- **One depth grammar.** Four levels, each with one job: plane for layout, raised for parts you press, recessed for parts that hold input or output, float for overlays. Data is never extruded.
- **Light and dark housings.** Warm pebble-gray plastic and smoked dark plastic, switched with one attribute on any element. Every shadow is alpha over the housing, so one recipe works on both.
- **Components.** Buttons, fields, input groups, comboboxes, a date picker, checkboxes, radios, switches, segmented controls, ranges, choice cards, file upload, tabs, breadcrumbs, pagination, a command menu, badges with status lamps, tags, meters, progress bars, spinners, skeletons, alerts, LCD readouts, empty states, accordions, description lists, avatar groups, timelines, tables, charts, pricing cards, menus, popovers, dialogs, sheets, toasts and tooltips.
- **Reference screens.** A dashboard, invoices, customers, reports, products, tabbed settings, sign-in and a marketing landing page, all built only with the library's classes.
- **Readable first.** Every text color is checked against WCAG 2 and APCA in both housings. Focus is a 2px ink ring on every control, and Windows High Contrast gets real borders.
- **Motion with a reason.** Presses go down in 80ms and come back in 160ms. Overlays arrive and leave on one curve, nothing moves on scroll, and reduced motion keeps the fades.
- **CSS only.** Every class is a Tailwind `@utility`, unprefixed (`btn`, `field`, `tabs`), so variants work: `md:btn-lg`.

### Install

1. Download `plastc.css` from the [website](https://plastc.space.fast/), or copy [`src/plastc.css`](src/plastc.css) from this repository, into your project.
2. Import it after Tailwind in your entry stylesheet:

   ```css
   @import "tailwindcss";
   @import "./plastc.css";
   ```

3. Load Geist and Geist Mono:

   ```html
   <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400..800&family=Geist+Mono:wght@400..600&display=swap" rel="stylesheet">
   ```

4. Light is the default. Add `data-housing="dark"` to `<html>`, or to any section, for dark.

[DESIGN.md](DESIGN.md) documents the depth grammar, tokens, motion, the contrast table and every class.

---

## For developers

### Requirements

- Node 22+ (for the Tailwind CLI)
- Python 3 (for the page generator)

### Layout

- `src/plastc.css`: the library.
- `site/build.py`: generates the showcase (`site/index.html`) and the reference screens (`site/screens/`).
- `site/marketing/`: one Python file per marketing page (landing, and the pages that join it), run by the build.
- `site/plastc.js`: demo behavior for the showcase and screens. Not part of the library.
- `site/plastc.css`: a copy of `src/plastc.css` that the build writes for the website's download link. Not committed.
- `site/mark-light.svg`, `site/mark-dark.svg`, `site/favicon.svg`: the keycap mark.
- `DESIGN.md` and `PRODUCT.md`: the design system and the product brief.

### Build and preview

```sh
npm install
npm run build   # writes site/index.html, site/screens/, site/plastc.css and site/dist.css
npm run serve   # http://localhost:8765
```

The generated pages, `dist.css` and the `plastc.css` copy are not committed. Each component group's View HTML and Copy HTML markup is generated from its demo at build time, with the demo-only hooks removed.

## License

[MIT](LICENSE)
