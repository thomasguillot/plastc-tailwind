BLOG_POST_BODIES = {
    "payment-terms": '''<p>Most invoices are read once, quickly, by someone who did not hire you. They look for three things: how much, by when, and how to pay. If any of those takes more than a few seconds to find, the invoice goes to the bottom of the pile.</p>

<h2>Put the due date next to the total</h2>
<p>“Net 30” on its own asks the reader to count days from an issue date they may not remember. Write the date: <strong>Due Dec 24</strong>. Keep it directly beside the amount, in the same size, so the two are read together. Plastc does this by default, and shows the date again on every reminder.</p>

<h2>Name the late fee plainly</h2>
<p>“Late fee” is clear. “Finance charge”, “penalty interest” and “administrative surcharge” are not. Say what it is, what it costs and when it starts: <em>A late fee of 2% applies to any balance unpaid after the due date.</em> One sentence, in the terms line, not in the footer.</p>

<h2>When net 30 is the wrong choice</h2>
<ul>
  <li>Small jobs under a few hundred dollars. Ask for payment on receipt, or net 7. A month is a long time to wait for an amount that is easy to pay today.</li>
  <li>Customers who pay in weekly or biweekly runs. Match their cycle, or you will land just after a run and wait nearly two weeks longer than you planned.</li>
  <li>Large projects. Split them into a deposit and a final invoice, each with its own date, instead of one big invoice with one long term.</li>
</ul>

<h2>Keep one set of terms</h2>
<p>Customers remember what they were told last. If your quote says net 14, your contract says net 30 and your invoice says net 21, expect the longest. Pick one, set it as the account default, and change it per customer only when you have agreed to it in writing.</p>''',

    "marlow-print-co": '''<p>Marlow Print Co. makes packaging and printed menus for eleven wholesale customers, most of them restaurants and small retailers. Orders ship every week, so invoices go out every week. Until this summer, the person who sent them was also the person who ran the press.</p>

<h2>What Sunday evenings looked like</h2>
<p>Naveen Marlow did the books on Sunday evening, after the shop had closed. He exported the week’s orders, typed each one into a spreadsheet, and sent the invoices from his own email. Chasing the unpaid ones came after that, one message at a time, from a list he kept in a notes app.</p>
<p>“I knew who was late,” he said. “I just did not want to be the person who wrote to them every week, so I waited, and then it was a month.”</p>

<h2>What changed</h2>
<p>Marlow moved to weekly invoices created from a template for each customer, with reminders switched on at day one, day seven and day fourteen after the due date. The reminders come from his shop’s name and carry a pay link, so a customer can settle an invoice from the email in under a minute.</p>
<p>He kept one rule for himself: anything over 30 days gets a phone call, never another email.</p>

<h2>The result</h2>
<p>Invoices sent per month went from 18 in June to 29 in October as he added customers, and the Sunday session dropped from about three hours to twenty minutes. The share of invoices paid within a week of the due date went from roughly half to most of them. He still calls the slowest payer, but now it is one customer, not four.</p>
<p>“The press is the part of the job I like,” he said. “Now the books stay out of my weekend.”</p>''',

    "bank-transfer-matching": '''<p>If you take payment by bank transfer, someone has to connect each incoming amount to the invoice it pays. That used to mean opening the bank statement, finding the line, and marking the invoice paid by hand. Plastc now does the first two steps for you.</p>

<h2>How matching works</h2>
<p>Every invoice has a payment reference, such as <code>INV-0189</code>. When a transfer arrives with that reference, we compare the amount and the reference to your open invoices. If both agree, the invoice is marked paid and the transfer appears on its timeline.</p>
<p>If the reference is missing or mistyped, we look for an open invoice from the same customer with the same amount. When there is exactly one, we match it. When there are several, or none, we leave the transfer in <strong>Waiting</strong> and ask you to choose.</p>

<h2>What you will see</h2>
<p>A new <strong>Transfers</strong> list under Payments shows each incoming transfer, the invoice it was matched to, and its status. <em>Matched</em> means the invoice is paid. <em>Waiting</em> means we could not decide on our own.</p>

<h2>Partial and combined payments</h2>
<p>A transfer for less than the invoice total is recorded as a partial payment and the balance stays open. A transfer that covers two invoices is not split automatically. It waits for you, because guessing wrong would mark the wrong invoice paid.</p>
<p>Matching is on for every account that has a bank connection. You can turn it off in <strong>Settings</strong>, under Payments.</p>''',

    "overdue-follow-up": '''<p>Chasing an invoice is awkward because it feels like an accusation. It rarely is. Most late invoices are late because they were lost, not because anyone decided not to pay. A calm, specific message each time gets you paid sooner than a firm one.</p>

<h2>Day one: a note</h2>
<p>Send it the morning after the due date. Assume the invoice slipped past someone.</p>
<blockquote>
  <p>Hi Dana, a quick note that invoice INV-0191 for $9,300 was due yesterday. The pay link is below if it is easier. If it is already on its way, thank you, and please ignore this.</p>
</blockquote>

<h2>Day seven: a reminder</h2>
<p>By now it is worth asking whether something is wrong. Offer an answer to the most likely problems.</p>
<blockquote>
  <p>Hi Dana, INV-0191 is now a week overdue. If you need a purchase order number on it, or it should go to a different address, tell me and I will fix it today. Otherwise the pay link is here.</p>
</blockquote>

<h2>Day thirty: a call</h2>
<p>Stop writing. Call, and ask when you can expect payment. Then write down the date they give you and send it back to them in a short email, so there is a record you both agreed to.</p>

<h2>A few rules</h2>
<ul>
  <li>Always include the invoice number, the amount and the pay link. Nobody should have to search for them.</li>
  <li>Use the customer’s first name and your own. A message from a person is answered faster than one from a system.</li>
  <li>If they reply, stop the schedule. Plastc pauses reminders for you when a customer writes back.</li>
</ul>''',

    "studio-varga": '''<p>Studio Varga is two architects, Mila and Ondrej Varga, with fifteen active clients between them. They design houses, extensions and a few small public buildings, and they are paid in stages. For years, billing happened whenever one of them remembered.</p>

<h2>One day a week</h2>
<p>Last January they picked Friday. Every invoice goes out that day, whether it is for a deposit, a milestone or a monthly retainer. If a stage finishes on Tuesday, the invoice waits until Friday.</p>
<p>“It sounded like we were losing three days,” Mila said. “In practice, clients learned to expect it. Payment dates became predictable, and so did ours.”</p>

<h2>What they send</h2>
<p>Each client has a stage plan in Plastc, so the Friday session is mostly checking that the right amounts are ready and pressing send. A retainer client gets the same invoice on the same Friday every month. Everyone else gets one when a stage closes.</p>
<p>Reminders go out on the Tuesday after the due date, which keeps them away from the weekend and from the day the invoice arrived.</p>

<h2>What they would tell another small practice</h2>
<ul>
  <li>Pick the day first, then the tool. The habit does more than the software.</li>
  <li>Agree payment terms in the proposal, not on the invoice.</li>
  <li>Keep the invoice short. One line per stage is enough.</li>
</ul>
<p>Invoices sent on Fridays went from four in January to nine in October, as the practice took on more projects, and Ondrej says he has not thought about billing on a Monday since.</p>''',

    "keyboard-shortcuts": '''<p>If you send more than a handful of invoices a week, the mouse is the slow part. Plastc now has a small set of shortcuts that cover the things you do most.</p>

<h2>The three to learn first</h2>
<ul>
  <li><kbd class="kbd">N</kbd> starts a new invoice from anywhere in the app.</li>
  <li><kbd class="kbd">/</kbd> moves focus to search, so you can find a customer or an invoice number without reaching for the sidebar.</li>
  <li><kbd class="kbd">⌘</kbd> <kbd class="kbd">K</kbd> opens the command menu (on Windows and Linux, <kbd class="kbd">Ctrl</kbd> <kbd class="kbd">K</kbd>). Type what you want to do, such as “send reminder” or “export CSV”, and press Enter.</li>
</ul>

<h2>Inside an invoice</h2>
<p>Press <kbd class="kbd">Tab</kbd> to move from one line item to the next, and <kbd class="kbd">Enter</kbd> on the last row to add another. When the invoice is ready, <kbd class="kbd">⌘</kbd> <kbd class="kbd">Enter</kbd> sends it.</p>

<h2>Shortcuts and typing</h2>
<p>Single-letter shortcuts only work when you are not typing in a field, so writing a note to a customer will never start a new invoice by accident. Press <kbd class="kbd">Esc</kbd> to leave a field and use them again.</p>
<p>The full list is in the command menu: open it and type “shortcuts”.</p>''',
}

for _p in BLOG_POSTS[1:]:
    _start = BLOG_POSTS.index(_p)
    _related = [BLOG_POSTS[(_start + k) % len(BLOG_POSTS)] for k in (1, 2, 3)]
    blog_article_page(_p, BLOG_POST_BODIES[_p["slug"]], _related)
