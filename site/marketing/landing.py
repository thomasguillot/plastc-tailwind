LP_LOGOS = [
    ('font-extrabold tracking-[-0.04em]', '<svg viewBox="0 0 20 20" class="inline-block w-[0.9em] h-[0.9em] mr-1.5 -mt-0.5 align-middle" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="currentColor"/></svg>Halden Studio'),
    ('font-mono font-medium uppercase tracking-[0.06em] !text-[15px] md:!text-[16px]', 'Northwind Co-op'),
    ('font-semibold uppercase tracking-[0.2em] !text-[14px] md:!text-[15px]', '<svg viewBox="0 0 20 20" class="inline-block w-[1.1em] h-[1.1em] mr-1.5 -mt-0.5 align-middle" aria-hidden="true"><path d="M10 2 18 17H2z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>Alder Robotics'),
    ('font-normal tracking-[-0.02em]', 'Brightwater <b class="font-extrabold">Labs</b>'),
    ('font-bold tracking-[-0.01em]', 'Ortiz <span class="font-normal">&amp;</span> Lane'),
    ('font-mono font-semibold lowercase !text-[16px] md:!text-[17px]', 'kettle hill bakery'),
]
lp_logos = "".join(f'<li class="{c}">{t}</li>' for c, t in LP_LOGOS)

LP_STATS = [
    ("Average time to get paid", "18 days", "Down from 26 before reminders were on"),
    ("Paid by the due date", "86%", "Of invoices sent with a pay link"),
    ("Paid through pay links", "$38M", "By card and bank transfer last year"),
    ("Studios invoicing", "4,200", "From one person to forty"),
]
lp_stats = "".join(f'<div class="stat"><dt>{k}</dt><dd class="stat-value">{v}</dd><dd>{d}</dd></div>' for k, v, d in LP_STATS)

LP_QUOTES = [
    ("MO", "Mira Okafor", "Owner, Halden Studio", "We used to spend Friday afternoons chasing late invoices. Now the reminders go out on their own, and I only step in when a customer replies."),
    ("IO", "Ines Ortiz", "Partner, Ortiz &amp; Lane", "Most of our clients pay by card straight from the email. We stopped sending bank details by hand in the first week."),
    ("RL", "Rosa Lind", "Owner, Kettle Hill Bakery", "I bill six cafés every Monday. With saved products, each invoice takes about as long as pouring a coffee."),
]
lp_quotes = "".join(f'<figure class="quote"><blockquote><p>“{q}”</p></blockquote><figcaption><span class="avatar">{a}</span><span><strong>{n}</strong>{r}</span></figcaption></figure>' for a, n, r, q in LP_QUOTES)

def lp_step(key, n, title, body, points, visual, hidden=True):
    pts = "".join(f"<li>{p}</li>" for p in points)
    return f'''<div role="tabpanel" id="hw-{key}" aria-labelledby="hw-tab-{key}" class="grid gap-8 md:gap-14 md:grid-cols-[1fr_1.15fr] items-center pt-10"{" hidden" if hidden else ""}>
    <div><p class="engraved">Step {n} of 3</p><h3 class="text-[26px] md:text-[30px] font-bold tracking-[-0.015em] text-balance mt-3">{title}</h3><p class="text-ink-2 text-lg mt-3 max-w-[44ch] text-pretty">{body}</p><ul class="check-list mt-6">{pts}</ul></div>
    <div class="rounded-[22px] seam p-5 md:p-8 min-w-0">{visual}</div>
  </div>'''

lp_send = f'''<div class="grid gap-4">
  <div class="flex items-center justify-between gap-3"><p class="font-bold">New invoice</p><span class="tag">INV-0194</span></div>
  <div><label class="label" for="hw-c">Customer</label><select id="hw-c" class="field field-select"><option>Halden Studio</option><option>Northwind Co-op</option><option>Kettle Hill Bakery</option></select></div>
  <div><label class="label" for="hw-i">Item</label><select id="hw-i" class="field field-select"><option>Brand identity</option><option>Website design</option><option>Design day</option></select></div>
  <div class="grid grid-cols-2 gap-4"><div class="min-w-0"><label class="label" for="hw-a">Amount</label><div class="input-group"><span class="input-affix">$</span><input id="hw-a" inputmode="decimal" value="4,820.00"></div></div><div class="min-w-0"><label class="label" for="hw-d">Due in</label><select id="hw-d" class="field field-select"><option>14 days</option><option selected>30 days</option></select></div></div>
  <div class="flex flex-wrap items-center justify-between gap-3 pt-1"><p class="text-sm text-ink-2">Goes to billing@halden.studio</p><button type="button" class="btn" data-toast="INV-0194 sent to Halden Studio">{i("send")}Send invoice</button></div>
</div>'''

lp_switches = "".join(f'''<label class="flex items-start gap-3.5 py-2.5"><input type="checkbox" role="switch" class="switch mt-0.5"{" checked" if on else ""}><span><span class="block text-sm font-semibold">{t}</span><span class="block text-sm text-ink-2">{d}</span></span></label>'''
    for t, d, on in [("The morning after the due date", "A short note with the pay link.", True), ("Every 7 days until it is paid", "The same note, with the days overdue.", True), ("Pause when they reply", "Reminders wait while you talk it through.", True)])
lp_remind = f'''<div>
  <div class="flex flex-wrap items-start justify-between gap-3"><div><p class="font-bold">Reminders for Northwind Co-op</p><p class="text-sm text-ink-2 mt-0.5 tabular-nums">INV-0191 · $9,300.00 · due Oct 26</p></div><span class="badge lamp-danger">Overdue</span></div>
  <div class="mt-3">{lp_switches}</div>
  <ol class="timeline mt-5 pt-5 border-t border-[color:var(--k-seam)]"><li class="lamp-off"><b>Next reminder</b> to finance@northwind.coop<time>Nov 3 · 8:00 AM</time></li><li class="lamp-warn"><b>Reminder sent</b> the morning after the due date<time>Oct 27 · 8:00 AM</time></li><li><b>Sent</b> by Mira Okafor<time>Oct 12 · 4:18 PM</time></li></ol>
</div>'''

lp_paid = f'''<div class="grid gap-5">
  <dl class="lcd px-5 py-4 grid gap-4 sm:grid-cols-2"><div class="stat"><dt>Paid in full</dt><dd class="stat-value !text-[28px]">$4,820.00</dd></div><div class="stat"><dt>In your bank</dt><dd class="stat-value !text-[28px]">Oct 30</dd></div></dl>
  <dl class="desc-list"><div><dt>Invoice</dt><dd>INV-0193 · Halden Studio</dd></div><div><dt>Status</dt><dd><span class="badge lamp-ok">Paid</span></dd></div><div><dt>Method</dt><dd>Visa ending 4242</dd></div><div><dt>Paid on</dt><dd>Oct 28 · 9:14 AM</dd></div></dl>
  <div class="flex flex-wrap items-center justify-between gap-3"><p class="text-sm text-ink-2">You hear about it the moment it lands.</p><button type="button" class="btn" data-toast="INV-0193 paid in full: $4,820.00">{i("bell")}Show the alert</button></div>
</div>'''

lp_tabs = "".join(f'<button role="tab" id="hw-tab-{k}" aria-controls="hw-{k}" aria-selected="{"true" if n == 0 else "false"}"{TI if n else ""}>{i(ic, "w-4 h-4")}{l}</button>' for n, (k, l, ic) in enumerate([("send", "Send", "send"), ("remind", "Remind", "bell"), ("paid", "Get paid", "check")]))

landing = f'''<section id="top" class="max-w-[1200px] mx-auto px-4 md:px-8 pt-14 md:pt-24 pb-16 md:pb-20 grid gap-12 lg:grid-cols-[1.05fr_1fr] items-center">
  <div>
    <h1 class="display text-[48px] sm:text-[64px] md:text-[80px] text-balance">Invoices that chase themselves.</h1>
    <p class="text-lg text-ink-2 max-w-[44ch] mt-7 leading-relaxed text-pretty">Send an invoice in a minute. Reminders follow up on their own, and one readout shows what is paid, open and overdue.</p>
    <div class="flex flex-wrap gap-3 mt-9"><a class="btn btn-signal btn-xl" href="sign-in.html">Start free</a><a class="btn btn-xl" href="dashboard.html">See the dashboard</a></div>
  </div>
  <div class="panel !p-4 sm:!p-5 min-w-0">
    <div class="lcd px-5 py-4 grid grid-cols-3 gap-4">{"".join(f'<div><p class="text-[11px] tracking-[0.12em] uppercase text-lcd-dim">{k}</p><p class="text-lg sm:text-xl font-semibold mt-1">{v}</p></div>' for k, v in (("Paid", "$48,210"), ("Open", "$15,447"), ("Overdue", "$9,300")))}</div>
    <div class="table-scroll mt-3">{table(CUSTOMERS[:4], select=False, actions=False, dates=False)}</div>
  </div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 pb-8" aria-labelledby="customers-h">
  <div class="py-10 border-y border-[color:var(--k-seam)]">
    <h2 id="customers-h" class="engraved text-center">Studios and small firms that invoice with Plastc</h2>
    <ul class="logo-strip mt-7">{lp_logos}</ul>
    <p class="text-center text-[13px] text-ink-2 mt-7">Sample customers. These businesses are made up.</p>
  </div>
</section>

<section id="features" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <h2 class="display text-[40px] md:text-[56px] max-w-[16ch] text-balance">Built for the part after you hit send</h2>
  <div class="mt-12">
  {feature("Reminders that go out on their own", "The morning after a due date passes, then every week until the invoice is paid. Pause them for one customer whenever you need to.", """<ol class="timeline"><li class="lamp-ok"><b>Paid in full</b> by card<time>Oct 28 · 9:14 AM</time></li><li class="lamp-warn"><b>Reminder sent</b> to billing@halden.studio<time>Oct 24 · 8:00 AM</time></li><li><b>Viewed</b> by Halden Studio<time>Oct 3 · 2:31 PM</time></li><li><b>Sent</b> by Mira Okafor<time>Oct 1 · 10:02 AM</time></li></ol>""")}
  {feature("Paid the way your customers prefer", "Every invoice carries a pay link for card and bank transfer. Payments mark the invoice paid as they land.", """<div class="grid gap-3" role="radiogroup" aria-label="Payment method"><label class="choice-card"><input type="radio" name="lpm" class="radio mt-0.5" checked><span><span class="block text-sm font-bold">Card</span><span class="block text-sm text-ink-2">Visa, Mastercard and Amex. Paid in seconds.</span></span></label><label class="choice-card"><input type="radio" name="lpm" class="radio mt-0.5"><span><span class="block text-sm font-bold">Bank transfer</span><span class="block text-sm text-ink-2">Details on the invoice. Matched when it arrives.</span></span></label></div>""", flip=True)}
  {feature("Know where you stand", "Paid, open and overdue in one readout, updated as payments arrive. No spreadsheet to keep in step.", f"""<div class="flex flex-wrap items-center gap-6"><div class="w-[140px] shrink-0">{donut([("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")], "$63.8k", "invoiced", "Invoiced this quarter: $63,800. Paid 62%, open 21%, overdue 9%, draft 8%.")}</div><ul class="grid gap-2 text-sm min-w-[150px]">{"".join(f'<li class="flex items-center justify-between gap-4"><span class="badge {l}">{n}</span><span class="tabular-nums text-ink-2">{p}%</span></li>' for n, p, l in (("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")))}</ul></div>""")}
  </div>
</section>

<section id="how-it-works" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24" aria-labelledby="how-h">
  <h2 id="how-h" class="display text-[40px] md:text-[56px] max-w-[16ch] text-balance">One invoice, from draft to paid</h2>
  <p class="text-ink-2 text-lg mt-4 max-w-[48ch] text-pretty">Each step shows the part of the app that does the work. The controls are real, so try them.</p>
  <div class="tabs mt-10" role="tablist" aria-label="How it works">{lp_tabs}</div>
  <div class="md:grid md:min-h-[560px] md:items-start md:[&>*]:col-start-1 md:[&>*]:row-start-1 md:[&>[hidden]]:!grid md:[&>[hidden]]:invisible">
  {lp_step("send", 1, "Send it in a minute", "Pick the customer and the work, choose the terms, and send. The invoice arrives by email with a pay link.", ["Line items from your saved products", "Terms remembered for each customer", "A PDF copy for their records"], lp_send, hidden=False)}
  {lp_step("remind", 2, "Let the reminders follow up", "Once the due date passes, reminders go out on a schedule you set. They stop the moment the invoice is paid.", ["Set the schedule once, or per customer", "Pause for one customer at any time", "See every reminder on the invoice"], lp_remind)}
  {lp_step("paid", 3, "Get paid and see it land", "Card payments mark the invoice paid in seconds. Bank transfers are matched when they arrive.", ["Card and bank transfer on every invoice", "Payouts on a set schedule", "An alert for every payment"], lp_paid)}
  </div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 pt-16 md:pt-24 pb-4 md:pb-8" aria-labelledby="numbers-h">
  <div class="flex flex-wrap items-end justify-between gap-x-8 gap-y-4">
    <h2 id="numbers-h" class="display text-[40px] md:text-[56px] max-w-[16ch] text-balance">Paid sooner, with less chasing</h2>
    <p class="text-sm text-ink-2">Sample figures. The product and its numbers are made up.</p>
  </div>
  <dl class="lcd mt-10 px-6 py-6 md:px-8 md:py-7 grid gap-x-6 gap-y-8 grid-cols-2 lg:grid-cols-4">{lp_stats}</dl>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24" aria-labelledby="quotes-h">
  <div class="flex flex-wrap items-end justify-between gap-x-8 gap-y-4">
    <h2 id="quotes-h" class="display text-[40px] md:text-[56px] max-w-[16ch] text-balance">What studios tell us</h2>
    <p class="text-sm text-ink-2">Sample quotes. The people and businesses are made up.</p>
  </div>
  <div class="quotes mt-10">{lp_quotes}</div>
</section>

<section id="pricing" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <div class="flex flex-wrap items-end justify-between gap-6">
    <div><h2 class="display text-[40px] md:text-[56px]">Pricing</h2><p class="text-ink-2 text-lg mt-4 max-w-[44ch]">Start free. Move up when your team or your client list grows.</p></div>
    <div class="seg" role="group" aria-label="Billing period"><button type="button" aria-pressed="true" data-billing="monthly">Monthly</button><button type="button" aria-pressed="false" data-billing="yearly">Yearly <span class="text-ink-2 font-semibold">2 months free</span></button></div>
  </div>
  <div class="grid gap-5 md:grid-cols-3 mt-10 items-stretch">{plan_cards}</div>
  <p class="mt-8 text-sm text-ink-2">Need the detail? <a class="font-bold text-ink underline" href="pricing.html">Compare every feature</a></p>
</section>

<section id="faq" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24 grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="display text-[40px] md:text-[56px]">Questions</h2><p class="text-ink-2 text-lg mt-4 max-w-[36ch]">Something else? Write to the team from inside the app.</p></div>
  <div class="accordion">{"".join(f'<details{" open" if n == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for n, (q, a) in enumerate(FAQS))}</div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <div class="panel !px-6 !py-10 md:!px-12 md:!py-14 flex flex-wrap items-center justify-between gap-8">
    <div><h2 class="text-[32px] md:text-[40px] font-bold tracking-[-0.02em] text-balance max-w-[18ch]">Send your next invoice in a minute.</h2><p class="text-ink-2 text-lg mt-3">Free for your first five invoices every month.</p></div>
    <div class="flex flex-wrap gap-3"><a class="btn btn-signal btn-lg" href="sign-in.html">Start free</a><a class="btn btn-lg" href="pricing.html">Compare plans</a></div>
  </div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 pt-4 pb-12 md:pb-16" aria-labelledby="news-h">
  <div class="grid gap-6 md:gap-12 md:grid-cols-2 md:items-center">
    <div><h2 id="news-h" class="text-[24px] md:text-[28px] font-bold tracking-[-0.015em] text-balance">Product notes, once a month</h2><p class="text-ink-2 mt-2 max-w-[44ch] text-pretty">What changed in the app, and one tip on getting paid sooner. Nothing else.</p></div>
    <div class="min-w-0">
      <form novalidate data-newsletter="news-done">
        <label class="label" for="news-email">Email</label>
        <div class="input-group">{i("mail")}<input id="news-email" type="email" autocomplete="email" placeholder="you@studio.com" aria-describedby="news-err news-hint"><button type="submit" class="btn">Subscribe</button></div>
        <span id="news-err" class="hint-error" data-newsletter-error hidden></span>
        <span id="news-hint" class="hint">One email a month. Every issue has a one-click unsubscribe.</span>
      </form>
      <div id="news-done" tabindex="-1" class="rounded-[16px] seam px-5 py-4 focus-visible:outline-none" hidden>
        <p class="badge lamp-ok !text-sm">You are subscribed</p>
        <p class="text-sm text-ink-2 mt-2">The first issue goes to <span class="font-semibold text-ink break-all" data-newsletter-email></span> on the first Monday of the month.</p>
        <button type="button" class="btn btn-quiet btn-sm mt-3 -ml-3" data-newsletter-reset>Use a different email</button>
      </div>
    </div>
  </div>
</section>
'''
mkt_page("screens/landing.html", "Landing page · Plastc", landing)
