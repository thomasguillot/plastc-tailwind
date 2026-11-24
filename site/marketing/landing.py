landing = f'''<section id="top" class="max-w-[1200px] mx-auto px-4 md:px-8 pt-14 md:pt-24 pb-20 grid gap-12 lg:grid-cols-[1.05fr_1fr] items-center">
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

<section id="features" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <h2 class="display text-[40px] md:text-[56px] max-w-[16ch] text-balance">Built for the part after you hit send</h2>
  <div class="mt-12">
  {feature("Reminders that go out on their own", "The morning after a due date passes, then every week until the invoice is paid. Pause them for one customer whenever you need to.", """<ol class="timeline"><li class="lamp-ok"><b>Paid in full</b> by card<time>Oct 28 · 9:14 AM</time></li><li class="lamp-warn"><b>Reminder sent</b> to billing@halden.studio<time>Oct 24 · 8:00 AM</time></li><li><b>Viewed</b> by Halden Studio<time>Oct 3 · 2:31 PM</time></li><li><b>Sent</b> by Mira Okafor<time>Oct 1 · 10:02 AM</time></li></ol>""")}
  {feature("Paid the way your customers prefer", "Every invoice carries a pay link for card and bank transfer. Payments mark the invoice paid as they land.", """<div class="grid gap-3" role="radiogroup" aria-label="Payment method"><label class="choice-card"><input type="radio" name="lpm" class="radio mt-0.5" checked><span><span class="block text-sm font-bold">Card</span><span class="block text-sm text-ink-2">Visa, Mastercard and Amex. Paid in seconds.</span></span></label><label class="choice-card"><input type="radio" name="lpm" class="radio mt-0.5"><span><span class="block text-sm font-bold">Bank transfer</span><span class="block text-sm text-ink-2">Details on the invoice. Matched when it arrives.</span></span></label></div>""", flip=True)}
  {feature("Know where you stand", "Paid, open and overdue in one readout, updated as payments arrive. No spreadsheet to keep in step.", f"""<div class="flex flex-wrap items-center gap-6"><div class="w-[140px] shrink-0">{donut([("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")], "$63.8k", "invoiced", "Invoiced this quarter: $63,800. Paid 62%, open 21%, overdue 9%, draft 8%.")}</div><ul class="grid gap-2 text-sm min-w-[150px]">{"".join(f'<li class="flex items-center justify-between gap-4"><span class="badge {l}">{n}</span><span class="tabular-nums text-ink-2">{p}%</span></li>' for n, p, l in (("Paid", 62, "lamp-ok"), ("Open", 21, "lamp-warn"), ("Overdue", 9, "lamp-danger"), ("Draft", 8, "lamp-off")))}</ul></div>""")}
  </div>
</section>

<section id="pricing" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24">
  <div class="flex flex-wrap items-end justify-between gap-6">
    <div><h2 class="display text-[40px] md:text-[56px]">Pricing</h2><p class="text-ink-2 text-lg mt-4 max-w-[44ch]">Start free. Move up when your team or your client list grows.</p></div>
    <div class="seg" role="group" aria-label="Billing period"><button type="button" aria-pressed="true" data-billing="monthly">Monthly</button><button type="button" aria-pressed="false" data-billing="yearly">Yearly <span class="text-ink-2 font-semibold">2 months free</span></button></div>
  </div>
  <div class="grid gap-5 md:grid-cols-3 mt-10 items-stretch">{plan_cards}</div>
</section>

<section id="faq" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24 grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="display text-[40px] md:text-[56px]">Questions</h2><p class="text-ink-2 text-lg mt-4 max-w-[36ch]">Something else? Write to the team from inside the app.</p></div>
  <div class="accordion">{"".join(f'<details{" open" if n == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for n, (q, a) in enumerate(FAQS))}</div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <div class="panel !px-6 !py-10 md:!px-12 md:!py-14 flex flex-wrap items-center justify-between gap-8">
    <div><h2 class="text-[32px] md:text-[40px] font-bold tracking-[-0.02em] text-balance max-w-[18ch]">Send your next invoice in a minute.</h2><p class="text-ink-2 text-lg mt-3">Free for your first five invoices every month.</p></div>
    <div class="flex flex-wrap gap-3"><a class="btn btn-signal btn-lg" href="sign-in.html">Start free</a><a class="btn btn-lg" href="#pricing">Compare plans</a></div>
  </div>
</section>
'''
mkt_page("screens/landing.html", "Landing page · Plastc", landing)
