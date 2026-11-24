# The shared blog data and parts (BLOG_POSTS, blog_post_card, blog_subscribe) live in article.py, which build.py runs first.
_featured, _rest = BLOG_POSTS[0], BLOG_POSTS[1:]
_fname, _fini, _frole = BLOG_AUTHORS[_featured["author"]]

_blog_filters = f'''<div class="flex flex-wrap items-center justify-between gap-3">
  <div class="seg max-sm:[&>button]:!px-2.5" role="group" aria-label="Category" data-post-filter="posts">
    <button type="button" aria-pressed="true" data-category-filter="all">All</button>
    {"".join(f'<button type="button" aria-pressed="false" data-category-filter="{k}">{l}</button>' for k, l in BLOG_CATEGORIES)}
  </div>
  <label class="input-group w-full sm:w-72 min-w-0">{i("search")}<span class="sr-only">Search posts</span><input placeholder="Search posts" data-post-filter="posts"></label>
</div>'''

_blog = f'''{page_header("Blog", "Product updates, guides to getting paid on time, and stories from the studios that send their invoices with us.", _blog_filters)}

<div id="posts" class="max-w-[1200px] mx-auto px-4 md:px-8 pb-4">
  <article class="post-card" data-featured data-category="{_featured["cat"]}">
    <div class="grid gap-4 content-center">
      <p class="badge lamp-ok">Latest update</p>
      <h2><a href="article.html">{_featured["title"]}</a></h2>
      <p class="text-lg text-ink-2 leading-relaxed max-w-[44ch] text-pretty">{_featured["summary"]}</p>
      {blog_post_meta(_featured)}
      <div class="byline mt-2"><span class="avatar">{_fini}</span><div><strong>{_fname}</strong>{_frole}</div></div>
    </div>
    <div class="max-md:mt-2" aria-hidden="true">{blog_reply_fragment(compact=True)}</div>
  </article>

  <section class="mt-14 md:mt-16" aria-labelledby="latest-h" data-post-group>
    <h2 id="latest-h" class="engraved">More posts</h2>
    <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 mt-5">{"".join(blog_post_card(p) for p in _rest)}</div>
  </section>

  <div class="empty" data-post-empty hidden>
    <div class="lcd readout"><span class="readout-value">0</span><span class="readout-unit">posts</span></div>
    <h2>No posts match</h2>
    <p>Check the spelling, or look in another category.</p>
    <button type="button" class="btn btn-sm" data-post-clear="posts">{i("x")}Show all posts</button>
  </div>
</div>

{blog_subscribe("blog-sub")}
'''
mkt_page("screens/blog.html", "Blog · Plastc", _blog, active="blog")
