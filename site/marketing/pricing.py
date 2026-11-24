PRICING_COMPARE = [
    ("Invoicing", [
        ("Invoices a month", "5", "200", "Unlimited"),
        ("Pay links for card and bank transfer", True, True, True),
        ("Saved products and line items", True, True, True),
        ("Recurring invoices", False, True, True),
        ("Your own domain for pay links", False, False, True),
    ]),
    ("Reminders", [
        ("Automatic reminders", True, True, True),
        ("Pause when a customer replies", True, True, True),
        ("Late fees", False, True, True),
    ]),
    ("Team", [
        ("People", "1", "Up to 3", "Unlimited"),
        ("Owner, admin and member roles", False, True, True),
    ]),
    ("Reports and data", [
        ("Dashboard and reports", True, True, True),
        ("CSV export", False, True, True),
        ("API access", False, True, True),
    ]),
    ("Support", [
        ("Help center and email", True, True, True),
        ("Priority support, a reply within 4 hours", False, False, True),
    ]),
]

PRICING_FAQS = [
    ("How does yearly billing work?", "You pay for ten months and get twelve. The yearly price is charged once, at the start of your billing year."),
    ("Is there a contract?", "No. Plans renew each month, or each year on yearly billing. Cancel from Settings and your plan runs to the end of the period you paid for."),
    ("What if I go over my invoice limit?", "Nothing gets blocked. Invoices over the limit wait as drafts until the next month starts, or until you move up a plan."),
] + FAQS

def pricing_cell(v, featured):
    attr = " data-featured" if featured else ""
    if v is True: inner = '<span class="compare-yes"><span class="sr-only">Included</span></span>'
    elif v is False: inner = '<span class="compare-no"><span class="sr-only">Not included</span></span>'
    else: inner = f'<span class="font-semibold">{v}</span>'
    return f"<td{attr}>{inner}</td>"

pricing_featured = [p[5] for p in PLANS]
pricing_head = '<th scope="col"><span class="sr-only">Feature</span></th>' + "".join(
    f'<th scope="col"{" data-featured" if feat else ""}>{"<span class=\"badge lamp-signal\">Recommended</span>" if feat else ""}'
    f'<span class="compare-plan">{name}</span><span class="compare-price"><span data-price data-monthly="${mo}" data-yearly="${yr}">${mo}</span> <span data-price-unit>/ month</span></span></th>'
    for name, mo, yr, _b, _f, feat, _c in PLANS)
pricing_groups = "".join(
    f'<tbody><tr class="compare-group"><th scope="rowgroup">{group}</th>{"".join("<td data-featured></td>" if f else "<td></td>" for f in pricing_featured)}</tr>'
    + "".join(f'<tr><th scope="row">{label}</th>{"".join(pricing_cell(v, f) for v, f in zip(vals, pricing_featured))}</tr>' for label, *vals in rows)
    + "</tbody>"
    for group, rows in PRICING_COMPARE)

pricing_billing = '<div class="seg" role="group" aria-label="Billing period"><button type="button" aria-pressed="true" data-billing="monthly">Monthly</button><button type="button" aria-pressed="false" data-billing="yearly">Yearly <span class="text-ink-2 font-semibold">2 months free</span></button></div>'

pricing_body = f'''{page_header("Pay for the invoices you send", "Every plan has pay links, reminders and the dashboard. Start free, and move up when your team or your client list grows.", pricing_billing)}

<section class="max-w-[1200px] mx-auto px-4 md:px-8 pb-16 md:pb-24" aria-label="Plans">
  <div class="grid gap-5 md:grid-cols-3 items-stretch">{plan_cards}</div>
  <p class="mt-6 text-sm text-ink-2">Prices are in US dollars, per workspace. Sales tax is added at checkout where it applies.</p>
</section>

<section id="compare" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-20" aria-labelledby="compare-h">
  <h2 id="compare-h" class="display text-[40px] md:text-[56px] text-balance">Compare plans</h2>
  <p class="text-ink-2 text-lg mt-4 max-w-[48ch] text-pretty">Every feature, side by side. Studio is the plan most small teams pick.</p>
  <div class="table-scroll mt-10"><table class="ktable compare">
    <caption class="sr-only">Features included in the Solo, Studio and Practice plans</caption>
    <thead><tr>{pricing_head}</tr></thead>
    {pricing_groups}
  </table></div>
</section>

<section id="faq" class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-24 grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="display text-[40px] md:text-[56px]">Questions</h2><p class="text-ink-2 text-lg mt-4 max-w-[36ch]">About billing, limits and changing plans. Something else? Write to the team from inside the app.</p></div>
  <div class="accordion">{"".join(f'<details{" open" if n == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for n, (q, a) in enumerate(PRICING_FAQS))}</div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-16 md:py-20">
  <div class="panel !px-6 !py-10 md:!px-12 md:!py-14 flex flex-wrap items-center justify-between gap-8">
    <div><h2 class="text-[32px] md:text-[40px] font-bold tracking-[-0.02em] text-balance max-w-[18ch]">Start with five free invoices a month.</h2><p class="text-ink-2 text-lg mt-3">No card needed. Move up when you outgrow it.</p></div>
    <div class="flex flex-wrap gap-3"><a class="btn btn-signal btn-lg" href="sign-in.html">Start free</a><a class="btn btn-lg" href="dashboard.html">See the dashboard</a></div>
  </div>
</section>
'''
mkt_page("screens/pricing.html", "Pricing · Plastc", pricing_body, active="pricing")
