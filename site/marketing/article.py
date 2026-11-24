BLOG_CATEGORIES = [("product", "Product updates"), ("guides", "Guides"), ("stories", "Studio stories")]
BLOG_AUTHORS = {
    "ines": ("Ines Carvalho", "IC", "Product lead"),
    "sam": ("Sam Adeyemi", "SA", "Support lead"),
    "hana": ("Hana Ota", "HO", "Engineer"),
}

def blog_lcd_cell(label, value):
    return f'<div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">{label}</p><p class="text-[15px] sm:text-base font-semibold mt-1 whitespace-nowrap">{value}</p></div>'

BLOG_REPLY_TIMELINE = '''<ol class="timeline">
  <li><b>Sent</b> by Mira Okafor<time datetime="2026-10-12T10:02">Oct 12 · 10:02 AM</time></li>
  <li class="lamp-warn"><b>Reminder sent</b> to finance@northwind.coop<time datetime="2026-10-27T08:00">Oct 27 · 8:00 AM</time></li>
  <li class="lamp-warn"><b>Reminder sent</b> to finance@northwind.coop<time datetime="2026-11-03T08:00">Nov 3 · 8:00 AM</time></li>
  <li class="lamp-ok"><b>Reply received, reminders paused</b> until Nov 17<time datetime="2026-11-03T11:26">Nov 3 · 11:26 AM</time></li>
  <li class="lamp-off"><b>Reminder skipped</b> while paused<time datetime="2026-11-10T08:00">Nov 10 · 8:00 AM</time></li>
</ol>'''

def blog_reply_fragment(compact=False):
    steps = BLOG_REPLY_TIMELINE if not compact else '''<ol class="timeline">
  <li class="lamp-warn"><b>Reminder sent</b> to finance@northwind.coop<time datetime="2026-11-03T08:00">Nov 3 · 8:00 AM</time></li>
  <li class="lamp-ok"><b>Reply received, reminders paused</b><time datetime="2026-11-03T11:26">Nov 3 · 11:26 AM</time></li>
  <li class="lamp-off"><b>Reminder skipped</b> while paused<time datetime="2026-11-10T08:00">Nov 10 · 8:00 AM</time></li>
</ol>'''
    return f'''<div class="grid gap-5">
  <div class="lcd px-4 py-3 grid grid-cols-3 gap-3">{blog_lcd_cell("Invoice", "INV-0191")}{blog_lcd_cell("Due", "$9,300")}{blog_lcd_cell("Reminders", "Paused")}</div>
  {steps}
</div>'''

BLOG_VISUALS = {
    "terms": '<div class="grid justify-items-center"><div class="lcd readout"><span class="readout-value">Net 30</span><span class="readout-unit">Due Dec 24</span></div></div>',
    "marlow": bar_chart([18, 22, 21, 26, 29], ["Jun", "Jul", "Aug", "Sep", "Oct"], "Invoices sent by Marlow Print Co., June to October: 18, 22, 21, 26 and 29.", h=130),
    "transfers": ''.join(f'<div class="flex items-center justify-between gap-3 py-2.5{" border-t border-[color:var(--k-seam)]" if n else ""}"><span><span class="block text-sm font-semibold">{inv}</span><span class="block text-[13px] text-ink-2 tabular-nums">Transfer {amt}</span></span><span class="badge lamp-{lamp}">{st}</span></div>'
                         for n, (inv, amt, st, lamp) in enumerate((("INV-0189", "$2,275.00", "Matched", "ok"), ("INV-0184", "$1,980.00", "Waiting", "warn")))),
    "followup": f'<div class="lcd px-4 py-3 grid grid-cols-3 gap-3">{blog_lcd_cell("Day 1", "Note")}{blog_lcd_cell("Day 7", "Remind")}{blog_lcd_cell("Day 30", "Call")}</div>',
    "varga": f'<div class="lcd px-4 py-3"><div class="flex items-end justify-between gap-3">{blog_lcd_cell("Sent on Fridays", "15 clients")}<p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">Jan–Oct</p></div><div class="mt-3">{sparkline([4, 5, 4, 6, 7, 6, 8, 7, 9, 9])}</div></div>',
    "shortcuts": ''.join(f'<p class="flex items-center gap-3 text-sm{" mt-2.5" if n else ""}"><span class="flex gap-1 w-16">{keys}</span><span class="text-ink-2">{what}</span></p>'
                         for n, (keys, what) in enumerate((('<kbd class="kbd">N</kbd>', "New invoice"), ('<kbd class="kbd">/</kbd>', "Search"), ('<kbd class="kbd">⌘</kbd><kbd class="kbd">K</kbd>', "Everything else")))),
}

def blog_visual_well(html, cls="h-[168px]"):
    return f'<div class="rounded-[14px] seam {cls} grid items-center p-4 overflow-hidden" aria-hidden="true"><div class="min-w-0 w-full grid justify-items-center"><div class="w-full max-w-[300px]">{html}</div></div></div>'


def _blog_article_body():
    return f'''<p>Until now, reminders kept to their schedule no matter what happened in between. They went out the morning after the due date, then every week until the invoice was paid. If a customer wrote back to say the payment was on its way, or to ask about a line item, the next reminder still arrived a few days later.</p>
<p>Now a reply to any invoice or reminder email <strong>pauses reminders for that invoice</strong>. The reply shows up on the invoice timeline, the invoice gets a <em>Reminders paused</em> label, and nothing else goes out until you have had a chance to answer.</p>

<figure>
  <div class="rounded-[18px] seam p-5 sm:p-6">{blog_reply_fragment()}</div>
  <figcaption>An overdue invoice after the customer replied on Nov 3. The reminder due on Nov 10 was skipped. The next one waits until Nov 17, unless the invoice is paid first.</figcaption>
</figure>

<h2>Why we changed it</h2>
<p>A customer who replies is usually already dealing with the invoice. Sending them another reminder after they have written “paying on Friday” reads as if nobody opened their message, and it puts you in the position of apologizing for your own software.</p>
<p>It was also the most common thing people asked support about this year: how to stop the next reminder for one invoice, right after a customer had answered. You could already pause reminders by hand, but you had to remember to do it.</p>

<h2>How it works</h2>
<ol>
  <li>Every invoice email has its own reply-to address, so a reply is tied to one invoice, not to the whole customer.</li>
  <li>When a reply arrives, we forward it to you as before and pause reminders for that invoice only. Other invoices for the same customer keep their schedule.</li>
  <li>Reminders stay paused for 14 days, or until you resume them. If the invoice is still unpaid after that, the schedule picks up where it stopped.</li>
</ol>
<p>A typical reply that pauses reminders looks like this:</p>
<blockquote>
  <p>Thanks for the reminder. This one is approved and goes out with our Friday payment run.</p>
  <footer>Finance team, Northwind Co-op</footer>
</blockquote>

<h3>What counts as a reply</h3>
<p>Only messages written by a person. Automatic replies, such as out-of-office notices and delivery failures, are ignored. Here is what happens to reminders in each case:</p>
<div class="table-scroll">
  <table>
    <thead><tr><th>When this happens</th><th>Reminders</th></tr></thead>
    <tbody>
      <tr><td>The customer replies to a reminder</td><td>Paused for 14 days</td></tr>
      <tr><td>The customer replies to the original invoice</td><td>Paused for 14 days</td></tr>
      <tr><td>An out-of-office or bounce comes back</td><td>Keep their schedule</td></tr>
      <tr><td>The invoice is paid</td><td>Stop for good</td></tr>
      <tr><td>14 days pass without payment</td><td>Resume</td></tr>
    </tbody>
  </table>
</div>

<h3>Resuming early</h3>
<p>Open the invoice and choose <strong>Resume reminders</strong>. The next reminder goes out on its usual morning, not straight away, so a customer never gets two emails in an hour.</p>

<h2>How to turn it off</h2>
<p>Pausing on reply is on for every account. If you would rather keep reminders on a fixed schedule, go to <a href="settings.html">Settings</a>, open <strong>Notifications</strong>, and switch off <em>Pause reminders when a customer replies</em>. You can also change how long a pause lasts: 7, 14 or 30 days.</p>
<p>If you manage reminders through the API, the same two settings live on the account:</p>
<pre><code>PATCH /v1/settings/reminders

{{
  "pause_on_reply": true,
  "pause_days": 14
}}</code></pre>
<p>Invoices also have a new <code>reminders_paused_until</code> field. It is <code>null</code> unless a reply paused them, and it is cleared when you resume reminders or the invoice is paid.</p>

<h2>What it does not cover yet</h2>
<ul>
  <li>Replies by phone, or to a personal address instead of the invoice email, cannot pause anything. Use <strong>Pause reminders</strong> on the invoice for those.</li>
  <li>Customers who reply to a monthly statement pause reminders on every invoice in that statement. We are looking at making this per invoice.</li>
</ul>

<hr>

<p>Questions, or a case we did not think of? <a href="contact.html">Write to us</a>. We read every message, and a few of them shaped this change.</p>'''

BLOG_ARTICLE_BODY = _blog_article_body()
BLOG_ARTICLE_MINS = max(1, round(len(re.sub(r"<[^>]+>", " ", BLOG_ARTICLE_BODY).split()) / 220))

BLOG_POSTS = [
    dict(cat="product", title="Reminders now pause when a customer replies", summary="When a customer answers a reminder, the next one waits until you have had a chance to read the reply.",
         date="Nov 18, 2026", iso="2026-11-18", mins=BLOG_ARTICLE_MINS, author="ines", visual="reply"),
    dict(cat="guides", title="Payment terms your customers will actually read", summary="Where to put the due date, what to call a late fee, and when net 30 is the wrong choice.",
         date="Nov 10, 2026", iso="2026-11-10", mins=6, author="sam", visual="terms"),
    dict(cat="stories", title="How Marlow Print Co. stopped chasing wholesale invoices", summary="Eleven shops, weekly invoices, and one person doing the books on a Sunday evening.",
         date="Oct 30, 2026", iso="2026-10-30", mins=5, author="ines", visual="marlow"),
    dict(cat="product", title="Bank transfers now match to invoices on their own", summary="We read the reference on each incoming transfer and mark the right invoice paid.",
         date="Oct 21, 2026", iso="2026-10-21", mins=3, author="hana", visual="transfers"),
    dict(cat="guides", title="A calm way to follow up on an overdue invoice", summary="What to say on day one, day seven and day thirty, with wording you can copy.",
         date="Oct 14, 2026", iso="2026-10-14", mins=7, author="sam", visual="followup"),
    dict(cat="stories", title="Studio Varga on billing a two-person practice", summary="Two architects, fifteen clients, and why every invoice goes out on a Friday.",
         date="Sep 29, 2026", iso="2026-09-29", mins=5, author="ines", visual="varga"),
    dict(cat="guides", title="Keyboard shortcuts for sending invoices faster", summary="N for a new invoice, slash to search, and Cmd K for everything else.",
         date="Sep 16, 2026", iso="2026-09-16", mins=2, author="hana", visual="shortcuts"),
]

def blog_cat_label(key):
    return dict(BLOG_CATEGORIES)[key]

def blog_post_meta(p, with_cat=True):
    items = ([f'<span>{blog_cat_label(p["cat"])}</span>'] if with_cat else []) + [f'<time datetime="{p["iso"]}">{p["date"]}</time>', f'<span>{p["mins"]} min read</span>']
    return f'<p class="post-meta">{"".join(items)}</p>'

def blog_byline(key, extra=""):
    name, ini, role = BLOG_AUTHORS[key]
    return f'<div class="byline"><span class="avatar !w-8 !h-8 !text-[11px]">{ini}</span><div><strong>{name}</strong>{extra or role}</div></div>'

def blog_post_card(p, href="article.html", tag="h3"):
    visual = blog_reply_fragment(compact=True) if p["visual"] == "reply" else BLOG_VISUALS[p["visual"]]
    return f'''<article class="post-card" data-category="{p["cat"]}">
  {blog_visual_well(visual)}
  {blog_post_meta(p)}
  <{tag}><a href="{href}">{p["title"]}</a></{tag}>
  <p class="text-[15px] leading-normal text-ink-2 -mt-1">{p["summary"]}</p>
  {blog_byline(p["author"])}
</article>'''

def blog_subscribe(id_):
    return f'''<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-14 md:py-20" aria-labelledby="{id_}-h">
  <div class="panel !px-6 !py-8 md:!px-10 md:!py-10 grid gap-6 md:grid-cols-[1fr_minmax(0,420px)] items-center">
    <div><h2 id="{id_}-h" class="text-[26px] md:text-[30px] font-bold tracking-[-0.015em] text-balance">Get new posts by email</h2><p class="text-ink-2 mt-2 max-w-[44ch]">One email when a post goes up, usually twice a month. Unsubscribe from any of them.</p></div>
    <form class="min-w-0" data-subscribe novalidate>
      <label class="label" for="{id_}-email">Email</label>
      <div class="input-group">{i("mail")}<input id="{id_}-email" type="email" autocomplete="email" placeholder="you@studio.com" required aria-describedby="{id_}-hint"><button class="btn btn-signal">Subscribe</button></div>
      <p class="hint" id="{id_}-hint" data-subscribe-hint>We only use it to send the blog.</p>
    </form>
  </div>
</section>'''


_post = BLOG_POSTS[0]
_name, _ini, _role = BLOG_AUTHORS[_post["author"]]
_blog_article = f'''<article>
  <header class="max-w-[1200px] mx-auto px-4 md:px-8 pt-10 md:pt-16">
    <div class="max-w-[648px] mx-auto">
      <nav aria-label="Breadcrumb"><ol class="breadcrumbs"><li><a href="blog.html">Blog</a></li><li><a href="blog.html?category=product">Product updates</a></li><li><span aria-current="page">{_post["title"]}</span></li></ol></nav>
      <h1 class="display text-[38px] sm:text-[48px] md:text-[56px] mt-6 text-balance">{_post["title"]}</h1>
      <p class="text-lg md:text-xl text-ink-2 mt-5 leading-relaxed text-pretty">{_post["summary"]} You do not need to change anything to get it.</p>
      <div class="byline mt-8 pb-8 border-b border-[color:var(--k-seam)]"><span class="avatar">{_ini}</span><div><strong>{_name}</strong><p class="post-meta"><span>{_role}</span><time datetime="{_post["iso"]}">{_post["date"]}</time><span>{_post["mins"]} min read</span></p></div></div>
    </div>
  </header>
  <div class="max-w-[1200px] mx-auto px-4 md:px-8 pt-10 md:pt-12 pb-6">
    <div class="prose mx-auto">
{BLOG_ARTICLE_BODY}
    </div>
  </div>
</article>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 pt-14 md:pt-20" aria-labelledby="more-h">
  <div class="flex flex-wrap items-end justify-between gap-4 pt-10 border-t border-[color:var(--k-seam)]">
    <h2 id="more-h" class="text-[26px] md:text-[30px] font-bold tracking-[-0.015em]">More from the blog</h2>
    <a class="btn btn-sm" href="blog.html">All posts{i("right", "w-4 h-4")}</a>
  </div>
  <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 mt-8">{"".join(blog_post_card(p, href="blog.html") for p in (BLOG_POSTS[3], BLOG_POSTS[4], BLOG_POSTS[1]))}</div>
</section>

{blog_subscribe("article-sub")}
'''
mkt_page("screens/article.html", f'{_post["title"]} · Plastc', _blog_article, active="blog")
