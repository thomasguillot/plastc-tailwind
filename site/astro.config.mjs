import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import { Features } from 'lightningcss';

export default defineConfig({
  site: 'https://plastc.space.fast',
  compressHTML: false,
  build: { format: 'file' },
  markdown: { syntaxHighlight: false },
  integrations: [mdx()],
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
