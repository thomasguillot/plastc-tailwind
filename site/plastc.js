// Plastc demo behaviour. The library itself is CSS; this file only wires the
// reference pages: housing, depth, tabs, dialogs, toasts, selection, copy.
(function () {
  const root = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const live = msg => { const l = $('#live'); if (l) { l.textContent = ''; setTimeout(() => l.textContent = msg, 30); } };
  const save = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };

  /* ---------- housing + depth */
  function setHousing(h) {
    root.dataset.housing = h; save('plastc-housing', h);
    $$('[data-set-housing]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setHousing === h)));
    $$('[data-housing-readout]').forEach(el => el.textContent = h === 'dark' ? 'Dark' : 'Light');
  }
  function setDepth(d) {
    root.style.setProperty('--k-depth', d);
    $$('[data-set-depth]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setDepth === String(d))));
    $$('[data-depth-readout]').forEach(el => el.textContent = (+d).toFixed(1));
  }
  setHousing(root.dataset.housing || 'light');

  /* ---------- toast */
  const toastEl = $('#toast');
  let toastTimer, undoFn = null;
  const TOAST_MS = 6000;
  const hideToast = () => { if (toastEl.matches(':popover-open')) toastEl.hidePopover(); undoFn = null; };
  const armToast = () => { clearTimeout(toastTimer); toastTimer = setTimeout(hideToast, TOAST_MS); };
  function toast(msg, undo) {
    if (!toastEl || !toastEl.showPopover) { live(msg); return; }
    $('[data-toast-text]', toastEl).textContent = msg;
    undoFn = undo || null;
    $('[data-toast-undo]', toastEl).hidden = !undo;
    if (toastEl.matches(':popover-open')) toastEl.hidePopover();
    requestAnimationFrame(() => toastEl.showPopover());
    const hint = $('[data-toast-hint]', toastEl); if (hint) hint.textContent = undo ? ' Press Z to undo.' : '';
    armToast();
  }
  if (toastEl) {
    // Pause while the pointer or keyboard is on the toast.
    toastEl.addEventListener('pointerenter', () => clearTimeout(toastTimer));
    toastEl.addEventListener('pointerleave', armToast);
    toastEl.addEventListener('focusin', () => clearTimeout(toastTimer));
    toastEl.addEventListener('focusout', armToast);
  }
  function runUndo() { const fn = undoFn; hideToast(); if (fn) fn(); }

  /* ---------- dialogs */
  function openDialog(id, instant) {
    const d = document.getElementById(id); if (!d) return;
    d.classList.toggle('no-motion', !!instant);
    d.returnValue = '';
    d.showModal();
  }
  $$('dialog').forEach(d => {
    d.addEventListener('click', e => { if (e.target === d) d.close(); }); // backdrop click
    d.addEventListener('close', () => {
      const f = $('form[data-toast-on-submit]', d);
      if (f && d.returnValue === 'ok') toast(f.dataset.toastOnSubmit);
    });
  });

  /* ---------- screen viewer (showcase) */
  const viewer = document.getElementById('screen-viewer');
  const frame = viewer && $('[data-screen-frame]', viewer);
  function syncViewer(k) {
    $$('[data-screen]', viewer).forEach(b => b.dataset.screen === k ? b.setAttribute('aria-current', 'page') : b.removeAttribute('aria-current'));
    const tab = $('[data-screen-tab]', viewer); if (tab) tab.href = `screens/${k}.html`;
    const b = $(`[data-screen="${k}"]`, viewer); if (b) frame.title = b.textContent;
  }
  function showScreen(k) {
    const url = `screens/${k}.html`;
    if (frame.getAttribute('src') !== url) frame.src = url;
    syncViewer(k);
  }
  if (viewer) {
    frame.addEventListener('load', () => {
      try { const m = frame.contentWindow.location.pathname.match(/screens\/([\w-]+?)(?:\.html)?$/); if (m) syncViewer(m[1]); } catch (e) {}
    });
    viewer.addEventListener('close', () => {
      try { const h = localStorage.getItem('plastc-housing'); if (h === 'light' || h === 'dark') setHousing(h); } catch (e) {}
    });
  }

  /* ---------- void with undo (invoices) */
  let voidRow = null;
  const voidDialog = $('#void-invoice');
  if (voidDialog) voidDialog.addEventListener('close', () => {
    if (voidDialog.returnValue !== 'void' || !voidRow) return;
    const row = voidRow, label = $('[data-void-label]', voidDialog).textContent;
    const cb = $('[data-row-select]', row); if (cb) cb.checked = false;
    row.hidden = true; filterRows();
    toast(`${label} voided`, () => { row.hidden = false; filterRows(); live(`${label} restored`); const b = $('[popovertarget]', row); if (b) b.focus(); });
    // Focus moves to the next row's actions, so keyboard users keep their place.
    const visible = r => r && !r.hidden && r.style.display !== 'none';
    let next = row.nextElementSibling; while (next && !visible(next)) next = next.nextElementSibling;
    let prev = row.previousElementSibling; while (prev && !visible(prev)) prev = prev.previousElementSibling;
    const target = (next && $('[popovertarget]', next)) || (prev && $('[popovertarget]', prev)) || $('[data-toast-undo]');
    setTimeout(() => target && target.focus(), 50);
  });

  /* ---------- clicks */
  document.addEventListener('click', e => {
    const t = e.target;
    const h = t.closest('[data-set-housing]'); if (h) return setHousing(h.dataset.setHousing);
    const d = t.closest('[data-set-depth]'); if (d) return setDepth(d.dataset.setDepth);
    if (t.closest('[data-reset]')) { setDepth('1'); setHousing('light'); return; }

    const od = t.closest('[data-open-dialog]'); if (od) { e.preventDefault(); closePopovers(); return openDialog(od.dataset.openDialog); }
    const cd = t.closest('[data-close-dialog]'); if (cd) return cd.closest('dialog').close();

    const vd = t.closest('[data-void]');
    if (vd) { closePopovers(); voidRow = vd.closest('tr'); $('[data-void-label]', voidDialog).textContent = vd.dataset.void; return openDialog('void-invoice'); }

    const os = t.closest('[data-open-screen]');
    if (os && viewer && e.button === 0 && !(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey)) {
      e.preventDefault(); showScreen(os.dataset.openScreen); viewer.showModal(); return;
    }
    const sc = t.closest('[data-screen]'); if (sc) return showScreen(sc.dataset.screen);

    const ts = t.closest('[data-toast]'); if (ts) { closePopovers(); return toast(ts.dataset.toast); }
    if (t.closest('[data-toast-undo]')) return runUndo();

    const c = t.closest('[data-copy], [data-copy-from]');
    if (c) {
      let text = c.dataset.copy;
      if (c.dataset.copyFrom) {
        const clone = document.getElementById(c.dataset.copyFrom).cloneNode(true);
        clone.querySelectorAll('[data-demo-note]').forEach(n => n.remove());
        clone.querySelectorAll('[data-toast]').forEach(n => n.removeAttribute('data-toast'));
        clone.querySelectorAll('[data-open-dialog]').forEach(n => { n.setAttribute('commandfor', n.dataset.openDialog); n.setAttribute('command', 'show-modal'); n.removeAttribute('data-open-dialog'); });
        text = dedent(clone.innerHTML);
      }
      const label = c.innerHTML;
      const done = ok => { c.textContent = ok ? 'Copied' : 'Select and copy'; live(ok ? 'Copied to clipboard' : 'Copy failed'); setTimeout(() => c.innerHTML = label, 1400); };
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => done(true), () => done(false));
      return;
    }

    const s = t.closest('.seg > button');
    if (s && !s.disabled) {
      const seg = s.parentElement;
      if (seg.getAttribute('role') === 'tablist') return selectTab(s);
      if (s.hasAttribute('aria-current')) return;
      [...seg.children].forEach(x => x.tagName === 'BUTTON' && x.setAttribute(s.hasAttribute('aria-pressed') ? 'aria-pressed' : 'aria-current', String(x === s)));
      if (seg.getAttribute('aria-label') === 'Pages') return goToPage(seg, Number(s.textContent));
    }

    const tb = t.closest('.tabs > [role=tab]'); if (tb) return selectTab(tb);
    const tl = t.closest('.tabs > a[href^="#"]');
    if (tl) { e.preventDefault(); [...tl.parentElement.children].forEach(x => x.removeAttribute('aria-current')); tl.setAttribute('aria-current', 'page'); return; }

    const step = t.closest('[data-page-step]');
    if (step && !step.disabled) {
      const seg = step.closest('.pager').querySelector('.pager-pages');
      const cur = Number(seg.querySelector('[aria-current]').textContent);
      goToPage(seg, cur + Number(step.dataset.pageStep));
    }
  });
  function goToPage(seg, cur) {
    const total = Number(seg.dataset.total || [...seg.querySelectorAll('button')].at(-1).textContent);
    seg.dataset.total = total;
    cur = Math.min(Math.max(cur, 1), total);
    const hadFocus = seg.contains(document.activeElement);
    const lo = Math.max(1, Math.min(cur - 1, total - 4)), hi = Math.min(total, Math.max(cur + 1, 5));
    const nums = [...new Set([1, ...Array.from({ length: hi - lo + 1 }, (_, n) => lo + n), total])].sort((a, b) => a - b);
    seg.innerHTML = nums.map((n, k) => (k && n - nums[k - 1] > 1 ? '<span aria-hidden="true">…</span>' : '') +
      `<button type="button"${n === cur ? ' aria-current="page"' : ''}>${n}</button>`).join('');
    if (hadFocus) seg.querySelector('[aria-current]').focus();
    const pager = seg.closest('.pager');
    const status = pager.querySelector('.pager-status'); if (status) status.textContent = `Page ${cur} of ${total}`;
    pager.querySelectorAll('[data-page-step]').forEach(b => { b.disabled = b.dataset.pageStep === '-1' ? cur === 1 : cur === total; });
  }
  const closePopovers = () => $$('[popover]:popover-open').forEach(p => p !== toastEl && p.hidePopover());
  const dedent = html => {
    const lines = html.replace(/^\n+|\s+$/g, '').split('\n');
    const pad = Math.min(...lines.filter(l => l.trim()).map(l => l.match(/^ */)[0].length));
    return lines.map(l => l.slice(pad)).join('\n');
  };

  /* ---------- tabs: click + arrow keys, with panels or table filters */
  function selectTab(tab, focus) {
    const list = tab.parentElement;
    $$('[role=tab]', list).forEach(x => {
      const on = x === tab;
      x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1;
      const p = x.getAttribute('aria-controls'); if (p) document.getElementById(p).hidden = !on;
    });
    if (focus) tab.focus();
    if (tab.dataset.filter) filterRows(tab.dataset.filter);
  }
  $$('[role=tablist]').forEach(list => {
    $$('[role=tab]', list).forEach((x, n) => x.tabIndex = x.getAttribute('aria-selected') === 'true' ? 0 : -1);
    list.addEventListener('keydown', e => {
      const tabs = $$('[role=tab]', list), cur = tabs.indexOf(document.activeElement);
      const next = { ArrowRight: cur + 1, ArrowLeft: cur - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (next === undefined || cur < 0) return;
      e.preventDefault(); selectTab(tabs[(next + tabs.length) % tabs.length], true);
    });
  });

  /* ---------- invoice table: filter, search, selection */
  const wrap = $('[data-table-wrap]'), empty = $('[data-empty]');
  let filter = 'all';
  function filterRows(f) {
    const scope = wrap || document;
    if (f && f !== filter) $$('[data-row-select]').forEach(c => c.checked = false);
    if (f) filter = f;
    const q = ($('[data-table-search]') || {}).value?.trim() || '';
    const ql = q.toLowerCase();
    const kept = $$('tbody tr[data-status]', scope).filter(r => !r.hidden);
    const matches = r => !ql || r.textContent.toLowerCase().includes(ql);
    // Counts follow the search, so the tabs never disagree with the rows.
    $$('[data-count]').forEach(el => { const k = el.dataset.count; el.textContent = kept.filter(r => (k === 'all' || r.dataset.status === k) && matches(r)).length; });
    // Sidebar counts are global: they ignore the table search.
    $$('[data-nav-count]').forEach(el => { const k = el.dataset.navCount; el.textContent = kept.filter(r => r.dataset.status === k).length; });
    if (!wrap) { updateBulk(); return; }
    let shown = 0;
    $$('tbody tr', wrap).forEach(r => {
      const ok = (filter === 'all' || r.dataset.status === filter) && matches(r);
      r.style.display = ok ? '' : 'none'; if (ok && !r.hidden) shown++;
    });
    if (empty) {
      wrap.style.display = shown ? '' : 'none'; empty.hidden = !!shown;
      if (!shown) {
        const label = { all: 'invoices', paid: 'paid invoices', open: 'open invoices', overdue: 'overdue invoices', draft: 'drafts' }[filter];
        const set = (sel, txt) => { const el = $(sel, empty); if (el) el.textContent = txt; };
        if (q) {
          set('[data-empty-unit]', 'Matches');
          set('[data-empty-title]', `No ${label} match “${q}”`);
          set('[data-empty-text]', 'Check the spelling, or search by invoice number or customer name.');
        } else if (filter === 'draft') {
          set('[data-empty-unit]', 'Drafts');
          set('[data-empty-title]', 'Nothing waiting to send');
          set('[data-empty-text]', 'Invoices you start but don’t send wait here. Everything you’ve started has gone out.');
        } else {
          set('[data-empty-unit]', label.split(' ')[0]);
          set('[data-empty-title]', `No ${label} right now`);
          set('[data-empty-text]', 'Nothing in this view. Try another status.');
        }
        $('[data-clear-search]', empty).hidden = !q;
        $('[data-empty-new]', empty).hidden = !!q || filter !== 'draft';
      }
    }
    const pager = $('[data-pager]'); if (pager) pager.hidden = !shown;
    const showing = $('[data-showing]'); if (showing) showing.textContent = shown === kept.length ? `Showing all ${shown} invoices` : `Showing ${shown} of ${kept.length} invoices`;
    updateBulk();
  }
  const searchBox = $('[data-table-search]'); if (searchBox) searchBox.addEventListener('input', () => filterRows());
  document.addEventListener('click', e => { if (e.target.closest('[data-clear-search]') && searchBox) { searchBox.value = ''; filterRows(); searchBox.focus(); } });

  const bulk = $('[data-bulk-bar]');
  function updateBulk() {
    if (!bulk) return;
    const rows = $$('[data-row-select]').filter(c => { const r = c.closest('tr'); return !r.hidden && r.style.display !== 'none'; });
    const n = rows.filter(c => c.checked).length;
    bulk.hidden = n === 0;
    $('[data-bulk-count]', bulk).textContent = `${n} invoice${n === 1 ? '' : 's'} selected.`;
    const all = $('[data-select-all]');
    if (all) { all.checked = n > 0 && n === rows.length; all.indeterminate = n > 0 && n < rows.length; }
  }
  document.addEventListener('change', e => {
    if (e.target.matches('[data-select-all]')) $$('[data-row-select]').forEach(c => { const r = c.closest('tr'); if (!r.hidden && r.style.display !== 'none') c.checked = e.target.checked; });
    if (e.target.matches('[data-select-all], [data-row-select]')) updateBulk();
  });
  if (bulk) {
    $('[data-clear-selection]', bulk).addEventListener('click', () => { $$('[data-row-select]').forEach(c => c.checked = false); updateBulk(); });
    $('[data-bulk-remind]', bulk).addEventListener('click', () => {
      const rows = $$('[data-row-select]:checked').map(c => c.closest('tr'));
      const due = rows.filter(r => r.dataset.status !== 'paid').length, paid = rows.length - due;
      toast(due ? `Reminders sent for ${due} invoice${due === 1 ? '' : 's'}` + (paid ? ` (${paid} paid skipped)` : '') : 'Those invoices are already paid');
    });
    updateBulk();
  }

  /* ---------- shortcuts: no animation, ever */
  document.addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const typing = e.target.closest('input, textarea, select, [contenteditable]');
    if (typing || document.querySelector('dialog[open]')) return;
    if ((e.key === 'z' || e.key === 'Z') && undoFn) { e.preventDefault(); return runUndo(); }
    if (e.key === '/') { const s = $('[data-table-search]') || $$('[data-search]').find(el => el.offsetParent); if (s) { e.preventDefault(); s.focus(); } }
    if ((e.key === 'n' || e.key === 'N') && $$('[data-open-dialog="new-invoice"]').some(b => b.offsetParent)) { e.preventDefault(); openDialog('new-invoice', true); }
    if (e.key === 'Escape') {
      // Tooltips must be dismissable without moving focus or the pointer (WCAG 1.4.13).
      $$('.tooltip').filter(t => t.matches(':hover') || t.contains(document.activeElement)).forEach(t => t.setAttribute('data-tip-off', ''));
    }
  });

  /* ---------- sign-in */
  const signin = $('form[data-signin]');
  if (signin) signin.addEventListener('submit', e => {
    e.preventDefault();
    const email = $('#e', signin), pw = $('#p', signin), btn = $('[type=submit]', signin), err = $('[data-signin-error]', signin);
    let bad = false;
    [[email, '#e-err'], [pw, '#p-err']].forEach(([f, id]) => { const empty = !f.value.trim(); f.setAttribute('aria-invalid', String(empty)); $(id).hidden = !empty; if (empty && !bad) { f.focus(); bad = true; } });
    err.hidden = true;
    if (bad) return;
    btn.setAttribute('aria-busy', 'true'); btn.disabled = true; btn.textContent = 'Signing in…';
    setTimeout(() => {
      if (pw.value === 'plastc') { location.href = 'dashboard.html'; return; }
      btn.removeAttribute('aria-busy'); btn.disabled = false; btn.textContent = 'Sign in';
      err.hidden = false;
      [email, pw].forEach(f => { f.setAttribute('aria-invalid', 'true'); f.setAttribute('aria-describedby', 'signin-err'); });
      pw.value = ''; pw.focus();
    }, 900);
  });

  /* ---------- tooltips come back after the pointer or focus leaves */
  $$('.tooltip').forEach(t => { const on = () => t.removeAttribute('data-tip-off'); t.addEventListener('pointerleave', on); t.addEventListener('focusout', on); });

  /* ---------- date range presets */
  document.addEventListener('click', e => {
    const r = e.target.closest('[data-range]'); if (!r) return;
    const label = $('[data-range-label]'), btn = $('[data-range-btn]');
    if (label) label.textContent = r.dataset.range;
    if (btn) btn.setAttribute('aria-label', 'Date range: ' + r.dataset.range);
    r.closest('[popover]').hidePopover(); if (btn) btn.focus();
  });

  /* ---------- settings: save validates, cancel really reverts */
  const saveBtn = $('[data-settings-save]'), cancelBtn = $('[data-settings-cancel]');
  if (saveBtn) {
    const fields = $$('#main input, #main select, #main textarea').filter(f => f.type !== 'file');
    const snapshot = () => fields.map(f => (f.type === 'checkbox' || f.type === 'radio') ? f.checked : f.value);
    let saved = snapshot();
    const em = $('#em'), emErr = $('#em-e');
    const validEmail = () => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim());
    em.addEventListener('input', () => { if (em.getAttribute('aria-invalid') === 'true' && validEmail()) { em.removeAttribute('aria-invalid'); emErr.hidden = true; } });
    saveBtn.addEventListener('click', () => {
      if (!validEmail()) {
        selectTab($('#tab-profile')); em.setAttribute('aria-invalid', 'true'); emErr.hidden = false; em.focus(); return;
      }
      saved = snapshot(); toast('Settings saved');
    });
    cancelBtn.addEventListener('click', () => {
      fields.forEach((f, n) => { if (f.type === 'checkbox' || f.type === 'radio') f.checked = saved[n]; else f.value = saved[n]; });
      em.removeAttribute('aria-invalid'); emErr.hidden = true;
      toast('Changes discarded');
    });
  }

  /* ---------- range readout */
  $$('input.range').forEach(r => {
    const out = r.closest('div').querySelector('[data-range-out]');
    const upd = () => { r.style.setProperty('--fill', ((r.value - r.min) / (r.max - r.min) * 100) + '%'); if (out) out.textContent = r.value; };
    r.addEventListener('input', upd); upd();
  });

  /* ---------- popover anchoring fallback (browsers without CSS anchor positioning) */
  if (!CSS.supports('position-area: bottom')) {
    $$('.menu[popover]').forEach(m => m.addEventListener('toggle', e => {
      if (e.newState !== 'open') return;
      const t = document.querySelector(`[popovertarget="${m.id}"]`); if (!t) return;
      const r = t.getBoundingClientRect(), w = m.offsetWidth;
      m.style.position = 'fixed'; m.style.margin = '0';
      m.style.top = Math.min(r.bottom + 6, innerHeight - m.offsetHeight - 8) + 'px';
      m.style.left = Math.max(8, Math.min(r.right - w, innerWidth - w - 8)) + 'px';
    }));
  }

  /* ---------- screen previews scale to their frame */
  if ('ResizeObserver' in window) {
    const ro = new ResizeObserver(es => es.forEach(en => { const f = en.target.querySelector('iframe'); if (f) f.style.setProperty('--s', en.contentRect.width / 1440); }));
    $$('iframe[style*="--s"]').forEach(f => ro.observe(f.parentElement));
  }
})();
