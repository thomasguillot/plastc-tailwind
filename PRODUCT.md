# Product

## Platform

web

## Stack

Tailwind CSS v4 (CSS-first `@theme` tokens + `@utility` neumorphic primitives + component classes), distributed as importable CSS, plus static HTML reference screens and a showcase site built with it. No JS framework. Deploy target: none yet; preview locally with `npm run build` and `npm run serve`.

## Users

Front-end developers and designers who want a soft-UI (neumorphic) look in a Tailwind project without hand-tuning dual shadows for every element. They are evaluating the kit: browsing components, judging whether it holds up (contrast, states, dark mode), then copying class names.

## Product Purpose

A complete UI library on the scale of Untitled UI (foundations, a full component set, and composed app screens: dashboards, tables, settings, auth, marketing sections), committed fully to neumorphism, for Tailwind. Every piece shares one depth system of extruded and inset surfaces and pressed states; depth is the whole design language, not an accent. Success: a team can build a real, dense product (dashboard, admin, settings) with only the library's classes, and it stays readable and usable.

## Positioning

Most neumorphism kits are a box-shadow snippet on a few demo cards that falls apart on real UI (unreadable text, no focus states, a single light theme). This kit treats depth as a token system (elevation levels, light direction, press states) with accessible contrast and both light and dark substrates.

## Capabilities and Constraints

- Inferred (not confirmed): light and dark substrates; keyboard focus visible on every control; text contrast meets WCAG AA despite low-contrast surfaces.
- Scope (confirmed): full library including app screens and dashboards, not just marketing components. Dense Operate-mode screens are the hardest test and drive the depth system.
- The showcase demonstrates the kit; it must not claim downloads, users, stars, or testimonials.
- Name: Plastc. The repository is plastc-tailwind.

## Evidence on Hand

None. No users, metrics, or testimonials exist; do not fabricate them.

## Product Principles

1. Depth is the language: every surface sits on the same substrate and differs only by elevation.
2. Tactile honesty: things that press look pressable, and things that don't, don't.
3. Readable first: contrast and focus never get sacrificed for softness.
4. Copyable: every effect shown maps to a class a developer can paste.

## Accessibility & Inclusion

Inferred: WCAG 2.1 AA text contrast, visible focus rings, prefers-reduced-motion respected.
