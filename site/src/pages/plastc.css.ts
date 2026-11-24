import { LIBRARY_CSS } from '../data/site';

export const GET = () => new Response(LIBRARY_CSS, { headers: { 'Content-Type': 'text/css; charset=utf-8' } });
