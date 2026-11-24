import { PAGES } from '../components/components/pages';
import { SITE } from '../data/site';

export const GET = () => {
  const paths = ['/', '/components/', ...PAGES.map((p) => `/components/${p.slug}/`)];
  const urls = paths.map((p) => `  <url>\n    <loc>${SITE}${p}</loc>\n  </url>`).join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
