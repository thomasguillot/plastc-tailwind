import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import { Features } from 'lightningcss';
import { copyFile, mkdir, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const folderIndexes = {
  name: 'folder-indexes',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      const out = fileURLToPath(dir);
      const put = async (from, to) => {
        await mkdir(dirname(to), { recursive: true });
        await copyFile(from, to);
      };
      for (const entry of await readdir(out, { withFileTypes: true })) {
        if (!entry.isDirectory()) continue;
        const section = join(out, entry.name);
        if (!existsSync(`${section}.html`)) continue;
        await put(`${section}.html`, join(section, 'index.html'));
        for (const file of await readdir(section)) {
          if (file.endsWith('.html') && file !== 'index.html') await put(join(section, file), join(section, file.slice(0, -5), 'index.html'));
        }
      }
    },
  },
};

export default defineConfig({
  site: 'https://plastc.space.fast',
  compressHTML: false,
  build: { format: 'file' },
  markdown: { syntaxHighlight: false },
  integrations: [mdx(), folderIndexes],
  vite: {
    plugins: [tailwindcss()],
    css: {
      lightningcss: {
        include: Features.Nesting | Features.MediaQueries,
        exclude: Features.LogicalProperties | Features.DirSelector | Features.LightDark,
        targets: { safari: (16 << 16) | (4 << 8), ios_saf: (16 << 16) | (4 << 8), firefox: 128 << 16, chrome: 111 << 16 },
      },
    },
    build: {
      cssMinify: 'lightningcss',
      cssTarget: ['safari16.4', 'ios16.4', 'firefox128', 'chrome111'],
      rollupOptions: {
        output: {
          assetFileNames: (info) => (info.names?.includes('app.css') ? 'dist.css' : '_astro/[name].[hash][extname]'),
        },
      },
    },
  },
});
