ABOUT_VALUES = [
    ("Say what is owed", "An invoice states the amount, the date and how to pay. Nothing else competes with that for space."),
    ("Chase politely, and keep chasing", "Reminders are firm and courteous, and they stop the moment a customer replies. Nobody should have to write an awkward email."),
    ("Keep the books honest", "Totals match on every screen. A voided invoice stays in the history, marked void, and is never deleted."),
    ("Small and sturdy", "We build for studios and practices of one to thirty people. We would rather do fewer things and have them work every time."),
]

ABOUT_TEAM = [
    ("Wren Castellan", "Founder, product", "WC"),
    ("Dov Aldana", "Engineering lead", "DA"),
    ("Ines Varga", "Design", "IV"),
    ("Hana Lindqvist", "Payments engineering", "HL"),
    ("Tobias Oyelaran", "Head of support", "TO"),
    ("Pilar Nwosu", "Customer support", "PN"),
    ("Emre Kovacs", "Finance and operations", "EK"),
]

ABOUT_ROLES = [
    ("Senior full-stack engineer", "Engineering", "Remote, UTC-3 to UTC+2", "Full time"),
    ("Product designer", "Design", "Remote, UTC-8 to UTC+1", "Full time"),
    ("Customer support specialist", "Support", "Portland, OR or remote", "Full time"),
    ("Payments operations analyst", "Finance", "Remote, UTC-5 to UTC+1", "Part time"),
    ("Technical writer", "Docs", "Remote", "Contract"),
]

about_values = "".join(f'''<div class="grid gap-2 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] md:gap-10 py-6 border-t border-[color:var(--k-seam)]">
    <h3 class="text-lg font-bold tracking-[-0.01em]">{t}</h3>
    <p class="text-ink-2 text-pretty max-w-[56ch]">{d}</p>
  </div>''' for t, d in ABOUT_VALUES)

about_people = "".join(f'<li><span class="avatar" aria-hidden="true">{ini}</span><div class="min-w-0"><p class="people-name">{n}</p><p class="people-role">{r}</p></div></li>' for n, r, ini in ABOUT_TEAM)

about_roles = "".join(f'''<li>
      <div><h3 class="role-title">{t}</h3><p class="role-meta"><span>{team}</span><span>{loc}</span><span>{kind}</span></p></div>
      <a class="btn btn-sm" href="contact.html?topic=careers" aria-label="Apply for {t}">Apply</a>
    </li>''' for t, team, loc, kind in ABOUT_ROLES)

about = f'''{page_header("A small team that sends a lot of invoices.", "Plastc is invoicing for studios and small practices. We build it, we answer the support inbox, and we use it to bill our own work.")}

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-12 md:py-16 grid gap-8 lg:grid-cols-[1fr_1.4fr] lg:gap-16">
  <h2 class="text-[28px] md:text-[34px] font-bold tracking-[-0.02em] text-balance max-w-[14ch]">Why we built it</h2>
  <div class="grid gap-5 text-lg text-ink-2 leading-relaxed max-w-[60ch] text-pretty">
    <p>Plastc started in a two-person design studio. Every other Friday, one of us spent the afternoon working out which invoices had been paid, which had been seen and which needed a nudge, and then wrote the same polite email again.</p>
    <p>The tools we tried were built for bigger companies, with accounting modules we did not need and screens that took a manual to read. We wanted one page that said what was paid, what was open and what was late, and reminders that went out without us.</p>
    <p>That is the product. It does one job for small teams, and we try to keep every screen as plain as the first one.</p>
  </div>
</section>

<section class="max-w-[1200px] mx-auto px-4 md:px-8 py-12 md:py-16">
  <h2 class="text-[28px] md:text-[34px] font-bold tracking-[-0.02em]">How we work</h2>
  <div class="mt-8 border-b border-[color:var(--k-seam)]">{about_values}</div>
</section>

<section id="team" class="max-w-[1200px] mx-auto px-4 md:px-8 py-12 md:py-16">
  <h2 class="text-[28px] md:text-[34px] font-bold tracking-[-0.02em]">The team</h2>
  <p class="text-ink-2 text-lg mt-3 max-w-[50ch]">Seven people, working across four time zones.</p>
  <ul class="people mt-8">{about_people}</ul>
</section>

<section id="careers" class="max-w-[1200px] mx-auto px-4 md:px-8 py-12 md:py-16 scroll-mt-6">
  <h2 class="text-[28px] md:text-[34px] font-bold tracking-[-0.02em]">Careers</h2>
  <p class="text-ink-2 text-lg mt-3 max-w-[50ch]">We are hiring for five roles. These are sample listings.</p>
  <ul class="role-list mt-8">{about_roles}</ul>
  <p class="text-ink-2 mt-6 max-w-[60ch]">Do not see your role? <a class="font-bold text-ink underline underline-offset-3" href="contact.html?topic=careers">Write to us</a> and tell us what you would work on. We read everything.</p>
</section>
'''
mkt_page("screens/about.html", "About · Plastc", about, active="about")
