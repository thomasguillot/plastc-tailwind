import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'posts'>;

export const BLOG_CATEGORIES = [
  { key: 'product', label: 'Product updates' },
  { key: 'guides', label: 'Guides' },
  { key: 'stories', label: 'Studio stories' },
] as const;

export const BLOG_AUTHORS = {
  ines: { name: 'Ines Varga', initials: 'IV', role: 'Design' },
  tobias: { name: 'Tobias Oyelaran', initials: 'TO', role: 'Head of support' },
  hana: { name: 'Hana Lindqvist', initials: 'HL', role: 'Payments engineering' },
} as const;

export const categoryLabel = (key: string) => BLOG_CATEGORIES.find((c) => c.key === key)!.label;

export const isoDate = (d: Date) => d.toISOString().slice(0, 10);
export const displayDate = (d: Date) => d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });

export async function getPosts() {
  const posts = await getCollection('posts');
  return posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export const postHref = (post: Post, featured: Post) => (post.id === featured.id ? 'article.html' : `post-${post.data.slug}.html`);
