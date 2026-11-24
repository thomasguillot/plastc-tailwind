import libraryCss from '../../../src/plastc.css?raw';
import pkg from '../../../package.json';

export const LIBRARY_CSS = libraryCss;
export const VERSION = pkg.version;
export const CSS_KB = Math.round(Buffer.byteLength(libraryCss, 'utf8') / 1024);
export const REPO = 'https://github.com/thomasguillot/plastc-tailwind';
export const CSS_ON_GITHUB = `${REPO}/blob/main/src/plastc.css`;
export const SITE = 'https://plastc.space.fast';
export const DESCRIPTION =
  'Plastc is a neumorphic UI library for Tailwind CSS v4: components, app screens and tokens in one CSS file, with light and dark themes and contrast checked against WCAG 2 and APCA.';
export const SCREEN_DESCRIPTION = 'A reference screen built with Plastc, a neumorphic UI library for Tailwind CSS v4. Sample data only.';
export const HOME_TITLE = 'Neumorphic UI library for Tailwind CSS v4 · Plastc';
export const IMPORT_LINE = '@import "tailwindcss";\n@import "./plastc.css";';
