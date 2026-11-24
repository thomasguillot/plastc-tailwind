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
    $$('[data-housing-next]').forEach(el => el.textContent = h === 'dark' ? 'Switch to light' : 'Switch to dark');
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
    const b = $(`[data-screen="${k}"]`, viewer); frame.title = b ? b.textContent : 'Landing page';
    const sel = $('[data-screen-select]', viewer); if (sel) sel.value = k;
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
    const sel = $('[data-screen-select]', viewer); if (sel) sel.addEventListener('change', () => showScreen(sel.value));
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
    const co = t.closest('#command [role=option]'); if (co) co.closest('dialog').close();
    if (t.closest('[data-command="housing"]')) return setHousing(root.dataset.housing === 'dark' ? 'light' : 'dark');
    if (t.closest('[data-open-command]')) return openCommand(false);
    const ct = t.closest('[data-combobox-toggle]');
    if (ct) { const inp = $('input[role=combobox]', ct.closest('.combobox')); if (listboxFor(inp).hidden) { openList(inp); filterList(inp, true); } else closeList(inp); inp.focus(); return; }
    const opt = t.closest('.combobox [role=option]');
    if (opt) { choose($('input[role=combobox]', opt.closest('.combobox')), opt); return; }
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
      const from = c.dataset.copyFrom && document.getElementById(c.dataset.copyFrom);
      const text = from ? from.textContent : c.dataset.copy;
      if (!copyLabels.has(c)) copyLabels.set(c, c.innerHTML);
      const label = copyLabels.get(c);
      const done = ok => {
        if (!c.style.minWidth) c.style.minWidth = getComputedStyle(c).width;
        const svg = (label.match(/<svg[\s\S]*?<\/svg>/) || [''])[0];
        const icon = ok ? svg.replace(/(<svg[^>]*>)[\s\S]*<\/svg>/, '$1<path d="m5 12.5 4.5 4.5L19 7.5"/></svg>') : svg;
        c.innerHTML = icon + (ok ? 'Copied' : 'Copy failed');
        live(ok ? 'Copied to clipboard' : 'Copy failed. Select the text and copy it.');
        clearTimeout(c._copyTimer);
        c._copyTimer = setTimeout(() => { c.innerHTML = label; c.style.minWidth = ''; }, 1400);
      };
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
  const copyLabels = new WeakMap();

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

  /* ---------- file upload (simulated progress) */
  const fileIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></svg>';
  const xIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  const trashIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/></svg>';
  const fmtSize = b => b >= 1e6 ? `${(b / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(b / 1e3))} KB`;
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function simulate(li) {
    const bar = $('.progress', li), pct = $('[data-file-pct]', li);
    let v = Number(bar.getAttribute('aria-valuenow')) || 0;
    const tick = setInterval(() => {
      if (!li.isConnected) return clearInterval(tick);
      v = Math.min(100, v + 6 + Math.random() * 10);
      bar.setAttribute('aria-valuenow', Math.round(v)); $('span', bar).style.setProperty('--v', v + '%');
      if (pct) pct.textContent = Math.round(v) + '%';
      if (v >= 100) {
        clearInterval(tick); bar.remove();
        pct.outerHTML = '<span class="badge lamp-ok">Uploaded</span>';
        const btn = $('[data-file-remove]', li); btn.setAttribute('aria-label', btn.getAttribute('aria-label').replace('Cancel', 'Remove')); btn.innerHTML = trashIcon;
        live(`${$('.file-name', li).textContent} uploaded`);
      }
    }, 280);
  }
  function addFiles(list, files) {
    [...files].forEach(f => {
      const li = document.createElement('li'); li.className = 'file-item';
      const name = esc(f.name), big = f.size > 10e6;
      li.innerHTML = `<span class="file-icon">${fileIcon}</span><div class="min-w-0"><p class="file-name">${name}</p>`
        + (big ? `<p class="file-meta file-error">${fmtSize(f.size)} · Over the 10 MB limit</p></div>`
               : `<p class="file-meta">${fmtSize(f.size)} · <span data-file-pct>0%</span></p></div>`)
        + `<button type="button" class="btn btn-quiet btn-sm btn-icon" aria-label="${big ? 'Remove' : 'Cancel'} ${name}" data-file-remove>${big ? trashIcon : xIcon}</button>`
        + (big ? '' : `<div class="progress" role="progressbar" aria-label="Uploading ${name}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span style="--v:0%"></span></div>`);
      list.prepend(li);
      if (!big) simulate(li);
    });
  }
  $$('[data-dropzone]').forEach(z => {
    const input = $('input[type=file]', z), list = $('[data-file-list]', z.parentElement);
    const take = files => { if (list) addFiles(list, files); else live(`${files.length} file${files.length === 1 ? '' : 's'} chosen`); };
    input.addEventListener('change', () => { take(input.files); input.value = ''; });
    z.addEventListener('dragover', e => { e.preventDefault(); z.setAttribute('data-dragover', ''); });
    z.addEventListener('dragleave', () => z.removeAttribute('data-dragover'));
    z.addEventListener('drop', e => { e.preventDefault(); z.removeAttribute('data-dragover'); take(e.dataTransfer.files); });
  });
  document.addEventListener('click', e => {
    const rm = e.target.closest('[data-file-remove]'); if (!rm) return;
    const li = rm.closest('.file-item'), name = $('.file-name', li).textContent;
    li.remove(); live(`${name} removed`);
  });

  /* ---------- pricing: monthly or yearly */
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-billing]'); if (!b) return;
    const yearly = b.dataset.billing === 'yearly';
    $$('[data-price]').forEach(p => { p.textContent = yearly ? p.dataset.yearly : p.dataset.monthly; });
    $$('[data-price-unit]').forEach(u => { u.textContent = yearly ? '/ year' : '/ month'; });
  });

  /* ---------- generic table filter: a search box and a .seg, both pointing at one table */
  function applyFilter(id) {
    const table = document.getElementById(id); if (!table) return;
    const q = (($(`input[data-filter-for="${id}"]`) || {}).value || '').trim().toLowerCase();
    const on = $(`.seg[data-filter-for="${id}"] [aria-pressed="true"]`), f = on ? on.dataset.rowFilter : 'all';
    let shown = 0;
    $$('tbody tr', table).forEach(r => {
      const ok = (f === 'all' || (r.dataset.group || '').split(' ').includes(f)) && (!q || r.textContent.toLowerCase().includes(q));
      r.hidden = !ok; if (ok) shown++;
    });
    const empty = $(`[data-empty-for="${id}"]`), wrap = table.closest('.table-scroll');
    if (empty) { empty.hidden = !!shown; if (wrap) wrap.hidden = !shown; }
    const count = $(`[data-count-for="${id}"]`), total = $$('tbody tr', table).length;
    if (count) count.textContent = shown === total ? `Showing all ${total} customers` : `Showing ${shown} of ${total} customers`;
  }
  document.addEventListener('input', e => { const s = e.target.closest('input[data-filter-for]'); if (s) applyFilter(s.dataset.filterFor); });
  document.addEventListener('click', e => {
    const b = e.target.closest('.seg[data-filter-for] > button');
    if (b) { [...b.parentElement.children].forEach(x => x.setAttribute('aria-pressed', String(x === b))); return applyFilter(b.parentElement.dataset.filterFor); }
    const c = e.target.closest('[data-clear-filter]');
    if (c) { const id = c.dataset.clearFilter, inp = $(`input[data-filter-for="${id}"]`); if (inp) { inp.value = ''; inp.focus(); } applyFilter(id); }
  });

  /* ---------- listbox: combobox and command menu share one controller */
  function listboxFor(input) { return document.getElementById(input.getAttribute('aria-controls')); }
  const visibleOptions = lb => $$('[role=option]', lb).filter(o => !o.hidden && !o.closest('[hidden]'));
  function setActive(input, opt) {
    $$('[role=option][data-active]', listboxFor(input)).forEach(o => o.removeAttribute('data-active'));
    if (opt) { opt.setAttribute('data-active', ''); input.setAttribute('aria-activedescendant', opt.id); opt.scrollIntoView({ block: 'nearest' }); }
    else input.removeAttribute('aria-activedescendant');
  }
  function filterList(input, showAll) {
    const lb = listboxFor(input), q = showAll ? '' : input.value.trim().toLowerCase();
    $$('[role=option]', lb).forEach(o => { o.hidden = !!q && !(o.textContent + ' ' + (o.dataset.keywords || '')).toLowerCase().includes(q); });
    $$('[role=group]', lb).forEach(g => { g.hidden = !$$('[role=option]', g).some(o => !o.hidden); });
    const vis = visibleOptions(lb), empty = $('.listbox-empty', lb);
    if (empty) empty.hidden = vis.length > 0;
    setActive(input, vis.find(o => o.getAttribute('aria-selected') === 'true') || vis[0]);
  }
  function openList(input) { const lb = listboxFor(input); if (lb.hidden) { lb.hidden = false; input.setAttribute('aria-expanded', 'true'); } }
  function closeList(input) {
    if (input.closest('.combobox')) { listboxFor(input).hidden = true; input.setAttribute('aria-expanded', 'false'); }
    setActive(input, null);
  }
  function choose(input, opt) {
    if (!input.closest('.combobox')) return opt.click();
    $$('[role=option]', listboxFor(input)).forEach(o => o.setAttribute('aria-selected', String(o === opt)));
    input.value = opt.dataset.value || opt.textContent.trim();
    closeList(input);
  }
  document.addEventListener('input', e => {
    const inp = e.target.closest('input[role=combobox]'); if (!inp) return;
    openList(inp); filterList(inp);
  });
  document.addEventListener('keydown', e => {
    const inp = e.target.closest && e.target.closest('input[role=combobox]'); if (!inp) return;
    const lb = listboxFor(inp), vis = visibleOptions(lb), cur = vis.findIndex(o => o.hasAttribute('data-active'));
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (lb.hidden) { openList(inp); filterList(inp, true); return; }
      const n = cur < 0 ? 0 : e.key === 'ArrowDown' ? Math.min(cur + 1, vis.length - 1) : Math.max(cur - 1, 0);
      setActive(inp, vis[n]);
    } else if (e.key === 'Enter' && !lb.hidden && cur >= 0) {
      e.preventDefault(); choose(inp, vis[cur]);
    } else if (e.key === 'Escape' && inp.closest('.combobox') && !lb.hidden) {
      e.preventDefault(); closeList(inp);
    }
  });
  document.addEventListener('pointerdown', e => {
    $$('.combobox').forEach(c => { if (!c.contains(e.target)) { const i = $('input[role=combobox]', c); if (i && !listboxFor(i).hidden) closeList(i); } });
  });

  /* ---------- command menu (Cmd/Ctrl+K) */
  const command = document.getElementById('command');
  function openCommand(instant) {
    if (!command) return;
    if (command.open) return command.close();
    if (document.querySelector('dialog[open]')) return;
    const inp = $('input[role=combobox]', command);
    inp.value = ''; filterList(inp);
    command.classList.toggle('no-motion', !!instant);
    command.showModal(); inp.focus();
  }
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && !e.altKey && e.key.toLowerCase() === 'k' && command) { e.preventDefault(); openCommand(true); }
  });
  if (/Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent)) $$('[data-kbd-mod]').forEach(k => { k.textContent = '⌘K'; });

  /* ---------- calendar (date picker) */
  const fmtTitle = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' });
  const fmtLabel = new Intl.DateTimeFormat('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
  const fmtField = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  const chev = d => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;
  const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const parseIso = v => { const [y, m, d] = v.split('-').map(Number); return new Date(y, m - 1, d); };
  function renderCalendar(cal, focusIso) {
    const sel = cal.dataset.value ? parseIso(cal.dataset.value) : null;
    const view = parseIso(cal.dataset.view || cal.dataset.value || iso(new Date()));
    const y = view.getFullYear(), m = view.getMonth(), today = iso(new Date());
    const start = new Date(y, m, 1 - new Date(y, m, 1).getDay());
    const anchor = focusIso || (sel && sel.getMonth() === m && sel.getFullYear() === y ? iso(sel) : (today.startsWith(`${y}-${String(m + 1).padStart(2, '0')}`) ? today : iso(new Date(y, m, 1))));
    let rows = '';
    for (let w = 0; w < 6; w++) {
      rows += '<tr>';
      for (let d = 0; d < 7; d++) {
        const day = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7 + d), k = iso(day);
        rows += `<td><button type="button" data-day="${k}" tabindex="${k === anchor ? 0 : -1}" aria-label="${fmtLabel.format(day)}"`
          + `${day.getMonth() !== m ? ' data-outside' : ''}${k === today ? ' aria-current="date"' : ''} aria-pressed="${sel && k === iso(sel)}">${day.getDate()}</button></td>`;
      }
      rows += '</tr>';
    }
    const heads = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'], full = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    cal.innerHTML = `<div class="calendar-head"><button type="button" class="btn btn-quiet btn-sm btn-icon" data-cal-step="-1" aria-label="Previous month">${chev('m15 6-6 6 6 6')}</button>`
      + `<p class="calendar-title" aria-live="polite">${fmtTitle.format(view)}</p>`
      + `<button type="button" class="btn btn-quiet btn-sm btn-icon" data-cal-step="1" aria-label="Next month">${chev('m9 6 6 6-6 6')}</button></div>`
      + `<table role="grid" aria-label="${fmtTitle.format(view)}"><thead><tr>${heads.map((h, n) => `<th scope="col"><abbr title="${full[n]}">${h}</abbr></th>`).join('')}</tr></thead><tbody>${rows}</tbody></table>`;
    if (focusIso) { const b = $(`[data-day="${focusIso}"]`, cal); if (b) b.focus(); }
  }
  function moveCalendar(cal, toIso) {
    const d = parseIso(toIso);
    cal.dataset.view = iso(new Date(d.getFullYear(), d.getMonth(), 1));
    renderCalendar(cal, toIso);
  }
  $$('[data-calendar]').forEach(cal => {
    renderCalendar(cal);
    const input = cal.dataset.for && document.getElementById(cal.dataset.for);
    if (input) input.addEventListener('change', () => {
      const d = new Date(input.value); if (isNaN(d)) return;
      cal.dataset.value = iso(d); cal.dataset.view = iso(new Date(d.getFullYear(), d.getMonth(), 1)); renderCalendar(cal);
    });
    cal.addEventListener('click', e => {
      const step = e.target.closest('[data-cal-step]');
      if (step) { const v = parseIso(cal.dataset.view || cal.dataset.value || iso(new Date())); cal.dataset.view = iso(new Date(v.getFullYear(), v.getMonth() + Number(step.dataset.calStep), 1)); renderCalendar(cal); return; }
      const day = e.target.closest('[data-day]'); if (!day) return;
      cal.dataset.value = day.dataset.day; moveCalendar(cal, day.dataset.day);
      if (input) { input.value = fmtField.format(parseIso(day.dataset.day)); input.dispatchEvent(new Event('input', { bubbles: true })); }
      const pop = cal.closest('[popover]');
      if (pop) { pop.hidePopover(); if (input) input.focus(); }
    });
    cal.addEventListener('keydown', e => {
      const day = e.target.closest('[data-day]'); if (!day) return;
      const d = parseIso(day.dataset.day);
      const delta = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key];
      let next = null;
      if (delta) next = new Date(d.getFullYear(), d.getMonth(), d.getDate() + delta);
      else if (e.key === 'Home') next = new Date(d.getFullYear(), d.getMonth(), d.getDate() - d.getDay());
      else if (e.key === 'End') next = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 6 - d.getDay());
      else if (e.key === 'PageUp' || e.key === 'PageDown') next = new Date(d.getFullYear(), d.getMonth() + (e.key === 'PageUp' ? -1 : 1), d.getDate());
      if (!next) return;
      e.preventDefault(); moveCalendar(cal, iso(next));
    });
  });

  /* ---------- popover anchoring fallback (browsers without CSS anchor positioning) */
  if (!CSS.supports('position-area: bottom')) {
    $$('.menu[popover], .popover[popover]').forEach(m => m.addEventListener('toggle', e => {
      if (e.newState !== 'open') return;
      const t = document.querySelector(`[popovertarget="${m.id}"]`); if (!t) return;
      const r = t.getBoundingClientRect(), w = m.offsetWidth;
      m.style.position = 'fixed'; m.style.margin = '0';
      m.style.top = Math.min(r.bottom + 6, innerHeight - m.offsetHeight - 8) + 'px';
      m.style.left = Math.max(8, Math.min(r.right - w, innerWidth - w - 8)) + 'px';
    }));
  }

  /* ---------- announcement banner */
  $$('[data-banner]').forEach(b => {
    try { if (localStorage.getItem('plastc-banner') === 'dismissed') b.hidden = true; } catch (e) {}
  });
  document.addEventListener('click', e => {
    const x = e.target.closest('[data-banner-dismiss]'); if (!x) return;
    const b = x.closest('[data-banner]'); if (b) b.hidden = true;
    save('plastc-banner', 'dismissed');
  });

  /* ---------- screen previews scale to their frame */
  if ('ResizeObserver' in window) {
    const ro = new ResizeObserver(es => es.forEach(en => { const f = en.target.querySelector('iframe'); if (f) f.style.setProperty('--s', en.contentRect.width / 1440); }));
    $$('iframe[style*="--s"]').forEach(f => ro.observe(f.parentElement));
  }
})();
