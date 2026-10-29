// The whole page: eleven categories, each with a "+" to add a posting, the
// open cards sorted by region, the application record and the e-mail log.
// Two boards share the page: Germany and Europe (outside Germany). The switch
// under the masthead picks one; each board has its own three regions, and the
// record counts both.
// A card leaves the list in one of two ways, Applied or Not relevant, and
// both are kept and counted in the record.
//
// Every category (and the record) is a fold-out card: the header is the
// control, the body unfolds beneath it. Folding happens in place, without
// rebuilding the page, so the height really animates, and the scroll
// position is managed so that nothing on screen ever jumps: a section that
// opens low is brought up into view; a section closed from deep inside
// keeps its pinned header exactly where it is. Which sections are open is
// remembered in this browser. Each posting card can also be opened for its
// details.
//
// Carried over from Physik Radar (AppDeploy, src/claude/view/page.js, stored
// version 1792255367672). Changes for the Cloudflare version: every visible
// word comes from i18n.js (German by default, English on the switch); the
// catalogue entries are objects { key, en, de }; sign-out goes to Cloudflare
// Access; on the German page a card shows the employer's own title first.

import { saveMark, addPosting, deleteAdded, SIGN_OUT_URL } from './api.js';
import { el, fill, hostOf } from './dom.js';
import { t, getLang, setLang, dateLabel, label } from './i18n.js';

const store = {
  get(key, fallback) { try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; } catch { return fallback; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode */ } },
};
// A server refusal names its reason as a code; the page says it in the reader's language.
const errorText = (error, fallbackKey) => {
  const d = error?.data ?? {};
  if (d.error === 'invalid_posting' && d.field) return t('err.invalid_posting.' + d.field);
  if (d.error === 'capacity') return t('err.capacity');
  if (d.error === 'forbidden_origin') return t('err.forbidden_origin');
  return t(fallbackKey);
};
const cut = (value, max = 300) => (value == null ? null : String(value).slice(0, max));
const STAGES = ['applied', 'rejected', 'confirmed', 'interview', 'offer', 'withdrawn'];
const stageLabel = s => (STAGES.includes(s) ? t('stage.' + s) : null);
const motion = () => !matchMedia('(prefers-reduced-motion: reduce)').matches;

// One curve and two durations for everything that moves: the fold (CSS),
// the chevron (CSS) and the scroll glide (JS) all follow these, so a section
// and the window move as one. The CSS reads them from these variables.
const FOLD = { open: 320, close: 240, curve: [0.4, 0, 0.2, 1] };
for (const [k, v] of [['--fold-open', FOLD.open + 'ms'], ['--fold-close', FOLD.close + 'ms'], ['--fold-ease', 'cubic-bezier(' + FOLD.curve.join(',') + ')']]) {
  document.documentElement.style.setProperty(k, v);
}
const bezier = ([x1, y1, x2, y2]) => {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = t => ((ax * t + bx) * t + cx) * t, sy = t => ((ay * t + by) * t + cy) * t, dx = t => (3 * ax * t + 2 * bx) * t + cx;
  return x => {
    let t = x;
    for (let i = 0; i < 6; i++) { const e = sx(t) - x; if (Math.abs(e) < 1e-5) break; const d = dx(t); if (Math.abs(d) < 1e-6) break; t -= e / d; }
    return sy(Math.min(1, Math.max(0, t)));
  };
};
const ease = bezier(FOLD.curve);
// A close that also has to drop the page (a section near the end of the page,
// closed from deep inside) gets a little longer, in step with the distance,
// so a window-high drop never has to happen in a quarter of a second.
const closeMs = dist => dist > 0 ? Math.round(Math.min(420, Math.max(FOLD.close, dist * 0.45))) : FOLD.close;

// Moves the window to `to` on the fold's own curve and clock, one frame at
// a time, so that the scroll and the unfolding height stay in step and the
// browser never has to clamp or re-anchor. A wheel or touch cancels it.
let glideId = 0;
function glide(to, ms) {
  const id = ++glideId;
  const from = scrollY;
  if (Math.abs(to - from) < 1) return;
  const stop = () => { if (id === glideId) glideId++; };
  addEventListener('wheel', stop, { once: true, passive: true });
  addEventListener('touchmove', stop, { once: true, passive: true });
  const dur = motion() ? ms : 0;
  let t0 = null, frames = 0;
  (function step(now) {
    if (id !== glideId) return;
    frames++;
    if (!dur) { if (frames < 3) return requestAnimationFrame(step); scrollTo({ top: to, behavior: 'instant' }); return; }
    t0 ??= now;
    const p = ease(Math.min(1, (now - t0) / dur));
    scrollTo({ top: from + (to - from) * p, behavior: 'instant' });
    if (p < 1) requestAnimationFrame(step);
  })(performance.now());
}

// Marks saved before Applied / Not relevant existed carry a stage or a
// removed flag; they read as outcomes. An explicit `outcome` (even null,
// after Undo) always wins. The importer writes an explicit outcome for
// every mark, so on Cloudflare the first line decides.
export function outcomeOf(mark) {
  if (!mark) return null;
  if (Object.hasOwn(mark, 'outcome')) return mark.outcome ?? null;
  if (mark.stage) return 'applied';
  if (mark.removed) return 'not_relevant';
  return null;
}

// Sun, moon, or a half-filled circle for "follow the system".
function themeIcon(kind) {
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 16 16'); svg.setAttribute('width', 14); svg.setAttribute('height', 14); svg.setAttribute('aria-hidden', 'true');
  const add = (tag, attrs) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); svg.append(n); };
  const line = { fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round' };
  if (kind === 'light') {
    add('circle', { cx: 8, cy: 8, r: 3, ...line });
    for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, c = Math.cos(a), s = Math.sin(a); add('path', { d: `M${8 + 5 * c} ${8 + 5 * s}L${8 + 6.5 * c} ${8 + 6.5 * s}`, ...line }); }
  } else if (kind === 'dark') {
    add('path', { d: 'M13 9.5A5.5 5.5 0 1 1 6.5 3a4.5 4.5 0 0 0 6.5 6.5z', ...line, 'stroke-linejoin': 'round' });
  } else {
    add('circle', { cx: 8, cy: 8, r: 5.5, ...line });
    add('path', { d: 'M8 2.5a5.5 5.5 0 0 1 0 11z', fill: 'currentColor' });
  }
  return svg;
}

/** A chevron that turns 180° about its own centre when its parent opens. */
function chev(size = 14) {
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'chev'); svg.setAttribute('viewBox', '0 0 14 14');
  svg.setAttribute('width', size); svg.setAttribute('height', size); svg.setAttribute('aria-hidden', 'true');
  const path = document.createElementNS(NS, 'path');
  path.setAttribute('d', 'M3 5l4 4 4-4'); path.setAttribute('fill', 'none'); path.setAttribute('stroke', 'currentColor');
  path.setAttribute('stroke-width', '1.8'); path.setAttribute('stroke-linecap', 'round'); path.setAttribute('stroke-linejoin', 'round');
  svg.append(path);
  return svg;
}

/** Opens or closes a rendered fold (section or card) without a rebuild. */
function setFold(node, open) {
  if (!node) return;
  node.setAttribute('data-collapsed', open ? '0' : '1');
  const fold = node.querySelector(':scope > [data-fold]');
  if (fold) { fold.setAttribute('data-open', open ? '1' : '0'); fold.toggleAttribute('inert', !open); }
  const btn = node.querySelector(':scope > [data-head] [data-toggle], :scope > .actions [data-toggle]');
  if (btn) {
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? btn.dataset.labelOpen : btn.dataset.labelClosed);
    if (btn.dataset.textOpen) btn.firstChild.textContent = open ? btn.dataset.textOpen : btn.dataset.textClosed;
  }
}

export function renderPage(mount, data) {
  const { marks } = data;
  let postings = data.postings ?? [];
  let added = data.added ?? [];
  let meta = data.meta ?? {};
  let applicationLog = data.applicationLog ?? [];
  let categories = data.categories ?? [];
  let areas = data.areas ?? [];
  let boards = data.boards ?? [{ key: 'de', en: 'Germany', de: 'Deutschland' }];

  // Theme: 'auto' follows the system, or 'light' / 'dark' as chosen; stored per browser. The button cycles the three.
  let theme = store.get('radar.theme', 'auto');
  if (!['auto', 'light', 'dark'].includes(theme)) theme = 'auto';
  document.documentElement.setAttribute('data-theme', theme);
  let board = store.get('radar.board', 'de');
  let area = store.get('radar.area', 'all');
  let cat = store.get('radar.cat', 'all');   // 'all' or one category key: the board then shows only that category
  let filterOpen = false;                    // the filter panel starts closed; it is only needed to change the view
  let form = null;          // { category, url, title, company, city, area, error, busy }
  let choosing = null;      // key of the card whose Remove choice is open
  let banner = '';          // last save problem, shown at the top
  let pendingData = null;   // a refresh that arrived while a form was open

  // Everything starts folded: the page opens as a column of category cards
  // and you open the one you want.
  const openSecs = new Set(store.get('radar.open', []));
  const openCards = new Set();
  const saveOpen = () => store.set('radar.open', [...openSecs]);

  const catLabel = key => label(categories.find(c => c.key === key)) || key;
  const areaLabel = key => label(areas.find(a => a.key === key)) || key;
  const boardOf = key => areas.find(a => a.key === key)?.board ?? 'de';
  // The regions of the board on show; every list, count and filter below uses these.
  const boardAreas = () => areas.filter(a => (a.board ?? 'de') === board);

  function cards() {
    const listed = postings.filter(p => !p.removed_on).map(p => ({
      key: 'j' + p.n, n: p.n, title: p.title, original: p.title_original, company: p.company, city: p.city,
      area: p.location_group, category: p.category, url: p.url, quote: p.eligibility_quote_de, note: p.note, noteDe: p.note_de,
      eligEn: p.eligibility_en, salary: p.salary, employment: p.employment, addedOn: p.added_on,
      mine: false, sortKey: 'b' + String(p.n).padStart(8, '0'),
    }));
    const mine = added.map(p => ({
      key: p.item_id, n: null, title: p.title, company: p.company, city: p.city, area: p.area,
      category: p.category, url: p.url, mine: true, addedAt: p.added_at, sortKey: 'c' + p.added_at,
    }));
    return [...mine, ...listed];
  }

  function recordItems(all) {
    const byKey = new Map(all.map(c => [c.key, c]));
    const byN = new Map(postings.map(p => [p.n, p]));
    const de = getLang() === 'de';
    const items = [];
    for (const mark of marks.values()) {
      const outcome = outcomeOf(mark);
      if (!outcome) continue;
      const key = mark.item_id;
      const card = byKey.get(key);
      const old = key.startsWith('j') ? byN.get(Number(key.slice(1))) : null;
      const snap = mark.snapshot ?? (card ? card : old ? { title: old.title, company: old.company, city: old.city,
        area: old.location_group, category: old.category, url: old.url } : null);
      const title = (de && old?.title_original) || snap?.title ||
        (key.startsWith('j') ? t('record.earlier_posting', { n: key.slice(1) }) : t('record.earlier_record', { key }));
      items.push({
        key, outcome, at: mark.outcome_at ?? mark.stage_at ?? mark.updated_at ?? '',
        stage: mark.stage ?? null, stageAt: mark.stage_at ?? null, stageNote: typeof mark.note === 'string' ? mark.note : '',
        title, company: snap?.company ?? '', url: snap?.url ?? null, category: snap?.category ?? null, area: snap?.area ?? null,
      });
    }
    return items.sort((a, b) => String(b.at).localeCompare(String(a.at)));
  }

  // ---- folding -------------------------------------------------------------
  // Two levels fold: the categories, and inside each open category its three
  // regions. A region's state is remembered per category; when the area chips
  // narrow the list to one region, that region opens by itself (until closed).
  const openAreas = new Set(store.get('radar.openAreas', []));
  const filterClosed = new Set();
  const saveAreas = () => store.set('radar.openAreas', [...openAreas]);
  const areaKey = (c, a) => c + ':' + a;
  const isAreaOpen = k => (area === 'all' ? openAreas.has(k) : !filterClosed.has(k));
  function rememberArea(k, open, save = true) {
    if (area === 'all') { open ? openAreas.add(k) : openAreas.delete(k); if (save) saveAreas(); }
    else open ? filterClosed.delete(k) : filterClosed.add(k);
  }

  const secNode = id => document.getElementById(id === 'record' ? 'record' : 'cat-' + id);
  const areaNode = k => document.getElementById('area-' + k.replace(':', '-'));
  const foldOf = node => node?.querySelector(':scope > [data-fold]');
  const isOpen = node => node?.getAttribute('data-collapsed') === '0';
  const pageEnd = () => document.documentElement.scrollHeight - innerHeight;

  // Where a fold's header pins while you scroll inside it: a category's at
  // the top of the window, a region's just under its category's header.
  function pinLine(node) {
    if (!node?.classList.contains('area')) return 0;
    const sec = node.closest('.cat');
    return pinLine(sec) + (sec?.querySelector(':scope > [data-head]')?.offsetHeight ?? 0);
  }

  // Brings a fold into view when its header sits low in the window (or above
  // its pin line), so the body unfolds on screen rather than below the edge.
  // The glide runs on the fold's clock and aims at where the page will end
  // once the body is fully out, so it is never clamped half-way.
  function reveal(node) {
    if (!node) return;
    const line = pinLine(node), top = node.getBoundingClientRect().top;
    if (top >= line && top <= Math.max(line + 48, innerHeight * 0.4)) return;
    const fold = foldOf(node);
    const growth = fold ? fold.firstElementChild.firstElementChild.offsetHeight - fold.getBoundingClientRect().height : 0;
    glide(Math.max(0, Math.min(scrollY + top - line - (line ? 8 : 12), pageEnd() + growth)), FOLD.open);
  }

  // Opens or closes one fold (a category or a region) in place, managing the
  // scroll so that nothing on screen jumps.
  function fold(node, open, bring = true) {
    if (!node) return;
    if (isOpen(node) !== open) {
      if (!open) {
        // Closing from deep inside: the header is pinned at its line while
        // the fold's own top is far above it. Put the fold's top where the
        // pinned header already is, so the header stays put and only the
        // body folds away beneath it. When the page will end up too short to
        // keep it there, glide down to the final position on the fold's own
        // curve rather than letting the browser snap at the end.
        const line = pinLine(node), top = node.getBoundingClientRect().top;
        if (top < line) scrollTo({ top: scrollY + top - line, behavior: 'instant' });
        const end = pageEnd() - (foldOf(node)?.getBoundingClientRect().height ?? 0);
        const ms = closeMs(scrollY - end);
        node.style.setProperty('--fold-close', ms + 'ms');
        if (scrollY > end) glide(Math.max(0, end), ms);
      }
      setFold(node, open);
    }
    if (open && bring) reveal(node);
  }

  function toggleSec(id, force, bring = true) {
    const open = force ?? !openSecs.has(id);
    open ? openSecs.add(id) : openSecs.delete(id);
    saveOpen();
    fold(secNode(id), open, bring);
  }

  function toggleArea(k, force) {
    const node = areaNode(k);
    const open = force ?? !isOpen(node);
    rememberArea(k, open);
    fold(node, open);
  }

  // All at once is done without animation: thirty heights moving together
  // is noise, not information. Collapsing all first puts the list's top at
  // the top of the window, so the result is one clean cut, not a jump.
  // It applies to both levels: categories and the regions inside them.
  function foldAll(open) {
    const list = mount.querySelector('.sections');
    if (!open && list) {
      const top = list.getBoundingClientRect().top + scrollY - 12;
      if (scrollY > top) scrollTo({ top, behavior: 'instant' });
    }
    list?.classList.add('no-anim');
    for (const id of [...categories.map(c => c.key), 'record', 'email-log']) {
      open ? openSecs.add(id) : openSecs.delete(id);
      if (secNode(id)) setFold(secNode(id), open);
    }
    for (const node of list?.querySelectorAll('.area') ?? []) { rememberArea(node.dataset.key, open, false); setFold(node, open); }
    saveOpen(); saveAreas();
    void list?.offsetWidth; // commit the new state before transitions return
    list?.classList.remove('no-anim');
  }

  // The region headers pin under their category's header, whose height varies
  // (long titles wrap, phones are narrower): each section carries its
  // header's height as --head-h for the region headers' sticky offset.
  const headObserver = new ResizeObserver(entries => {
    for (const e of entries) e.target.parentElement?.style.setProperty('--head-h', e.target.offsetHeight + 'px');
  });

  function toggleCard(key, node) {
    const open = !openCards.has(key);
    open ? openCards.add(key) : openCards.delete(key);
    setFold(node, open);
  }

  // A fold-out section: a header (title, counts, chevron) and a body beneath.
  function foldSection(id, attrs, headMain, body, name) {
    const open = openSecs.has(id);
    const bodyId = (attrs.id ?? id) + '-body';
    const section = el('section', { ...attrs, 'data-sec': '1', 'data-collapsed': open ? '0' : '1' });
    const btn = el('button', {
      type: 'button', class: 'toggle', 'data-toggle': '1', 'aria-controls': bodyId, 'aria-expanded': String(open),
      'data-label-open': t('sec.collapse', { name }), 'data-label-closed': t('sec.expand', { name }),
      'aria-label': open ? t('sec.collapse', { name }) : t('sec.expand', { name }),
      onclick: e => { e.stopPropagation(); toggleSec(id); },
    }, chev());
    section.append(
      el('header', { class: 'sec-head', 'data-head': '1', onclick: () => toggleSec(id) },
        el('div', { class: 'head-main' }, ...headMain),
        el('div', { class: 'head-side' }, btn)),
      el('div', { class: 'fold', 'data-fold': '1', 'data-open': open ? '1' : '0', id: bodyId, inert: !open },
        el('div', { class: 'fold-i' }, el('div', { class: 'sec-body' }, ...body))));
    return section;
  }

  // A region inside a category: the same fold one level down, smaller and in
  // the region's colour (the colour of the region pill on its cards).
  function foldArea(catKey, a, list) {
    const k = areaKey(catKey, a.key);
    const open = isAreaOpen(k);
    const id = 'area-' + catKey + '-' + a.key;
    const n = list.length;
    const name = label(a) + ', ' + catLabel(catKey);
    const btn = el('button', {
      type: 'button', class: 'atoggle', 'data-toggle': '1', 'aria-controls': id + '-body', 'aria-expanded': String(open),
      'data-label-open': t('sec.collapse', { name }), 'data-label-closed': t('sec.expand', { name }),
      'aria-label': open ? t('sec.collapse', { name }) : t('sec.expand', { name }),
      onclick: e => { e.stopPropagation(); toggleArea(k); },
    }, chev(12));
    return el('div', { class: 'area', id, 'data-area': a.key, 'data-key': k, 'data-collapsed': open ? '0' : '1' },
      el('div', { class: 'area-head', 'data-head': '1', onclick: () => toggleArea(k) },
        el('span', { class: 'area-name' }, label(a)),
        el('span', { class: 'area-count' }, t('sec.open_count', { n })),
        btn),
      el('div', { class: 'fold', 'data-fold': '1', 'data-open': open ? '1' : '0', id: id + '-body', inert: !open },
        el('div', { class: 'fold-i' }, el('div', { class: 'area-body' },
          n ? el('div', { class: 'grid' }, ...list.map(card)) : el('p', { class: 'empty' }, t('area.empty'))))));
  }

  // ---- actions -----------------------------------------------------------
  async function setOutcome(c, outcome) {
    const key = c.key;
    const before = marks.get(key) ?? null;
    const patch = outcome
      ? { outcome, outcome_at: new Date().toISOString(), snapshot: {
          title: cut(c.title), company: cut(c.company), city: cut(c.city), area: c.area,
          category: c.category, url: cut(c.url, 2000), n: c.n ?? null } }
      : { outcome: null, outcome_at: null };
    marks.set(key, { ...(before ?? { item_id: key }), ...patch });
    choosing = null; banner = '';
    render();
    try {
      marks.set(key, await saveMark(key, patch));
    } catch (error) {
      before ? marks.set(key, before) : marks.delete(key);
      banner = errorText(error, 'err.save');
    }
    render();
  }

  async function removeMistake(c) {
    if (!confirm(t('card.confirm_delete', { title: c.title }))) return;
    const before = added;
    added = added.filter(p => p.item_id !== c.key);
    choosing = null; banner = '';
    render();
    try { await deleteAdded(c.key); }
    catch (error) { added = before; banner = errorText(error, 'err.delete'); }
    render();
  }

  function openForm(category) {
    form = { category, url: '', title: '', company: '', city: '', area: area === 'all' ? '' : area, error: '', busy: false };
    choosing = null;
    openSecs.add(category); saveOpen();
    render();
    reveal(secNode(category));
    requestAnimationFrame(() => mount.querySelector('[data-addform] input[name=url]')?.focus({ preventScroll: true }));
  }

  function closeForm() {
    form = null;
    render();
  }

  async function submitForm(event) {
    event.preventDefault();
    if (!form || form.busy) return;
    const input = { url: form.url.trim(), title: form.title.trim(), company: form.company.trim(),
      city: form.city.trim(), area: form.area, category: form.category };
    let problem = '';
    try { const u = new URL(input.url); if (!['https:', 'http:'].includes(u.protocol)) problem = 'x'; } catch { problem = 'x'; }
    if (problem) problem = t('form.err_link');
    else if (!input.title) problem = t('form.err_title');
    else if (!input.city) problem = t('form.err_city');
    else if (!input.area) problem = t('form.err_area');
    else if (cards().some(c => c.url === input.url)) problem = t('form.err_duplicate');
    if (problem) { form.error = problem; render(); return; }
    form.busy = true; form.error = ''; render();
    try {
      const posting = await addPosting(input);
      added = [posting, ...added.filter(p => p.item_id !== posting.item_id)];
      closeForm();
    } catch (error) {
      if (form) { form.busy = false; form.error = errorText(error, 'err.save_form'); }
      render();
    }
  }

  function applyData(next) {
    if (next.postings) postings = next.postings;
    if (next.added) added = next.added;
    if (next.meta) meta = next.meta;
    if (next.applicationLog) applicationLog = next.applicationLog;
    if (next.categories) categories = next.categories;
    if (next.areas) areas = next.areas;
    if (next.boards) boards = next.boards;
  }

  // ---- view --------------------------------------------------------------
  function card(c) {
    const de = getLang() === 'de';
    const open = choosing === c.key;
    const expanded = openCards.has(c.key);
    // German page: the employer's own title first, the English one beneath it. English page: the other way round.
    const heading = de && c.original ? c.original : c.title;
    const second = de ? (c.original && c.original !== c.title ? c.title : null) : (c.original && c.original !== c.title ? c.original : null);
    const note = de && c.noteDe ? c.noteDe : c.note;
    const noteIsEnglish = !(de && c.noteDe);
    const employment = c.employment ? (t('employment.' + c.employment) !== 'employment.' + c.employment ? t('employment.' + c.employment) : c.employment) : null;
    const details = !c.mine && [
      !de && c.eligEn && el('p', { class: 'more-row' }, el('span', { class: 'lbl' }, t('card.in_short')), c.eligEn),
      c.salary && el('p', { class: 'more-row' }, el('span', { class: 'lbl' }, t('card.salary')), c.salary),
      employment && el('p', { class: 'more-row' }, el('span', { class: 'lbl' }, t('card.contract')), employment),
      c.addedOn && el('p', { class: 'more-row' }, el('span', { class: 'lbl' }, t('card.added')), dateLabel(c.addedOn)),
    ].filter(Boolean);
    const hasMore = !c.mine && (details.length > 0 || (note && note.length > 160));
    const node = el('article', { class: 'card' + (c.mine ? ' mine' : ''), 'data-card': c.key, 'data-collapsed': expanded ? '0' : '1' },
      el('div', { class: 'card-top' },
        el('span', { class: 'pill area-' + c.area }, areaLabel(c.area)),
        el('span', { class: 'city' }, c.city ?? ''),
        el('span', { class: 'num' }, c.mine ? t('card.added_by_you') : t('card.number', { n: c.n }))),
      el('h4', {}, el('a', { href: c.url, target: '_blank', rel: 'noopener noreferrer' }, heading)),
      second && el('p', { class: 'orig', lang: de ? 'en' : 'de' }, second),
      el('p', { class: 'co' }, c.company || hostOf(c.url)),
      c.quote && el('blockquote', { lang: 'de' }, '„' + c.quote + '“'),
      note && el('p', { class: 'note', lang: noteIsEnglish ? 'en' : 'de' }, note),
      hasMore && el('div', { class: 'fold card-more', 'data-fold': '1', 'data-open': expanded ? '1' : '0', inert: !expanded },
        el('div', { class: 'fold-i' }, el('div', { class: 'more-in' }, ...details))),
      el('div', { class: 'actions' },
        el('a', { class: 'open', href: c.url, target: '_blank', rel: 'noopener noreferrer' }, t('card.open')),
        hasMore && el('button', {
          type: 'button', class: 'more', 'data-toggle': '1', 'aria-expanded': String(expanded),
          'data-label-open': t('card.hide_details'), 'data-label-closed': t('card.show_details'),
          'data-text-open': t('card.less'), 'data-text-closed': t('card.more'),
          'aria-label': expanded ? t('card.hide_details') : t('card.show_details'),
          onclick: () => toggleCard(c.key, node),
        }, expanded ? t('card.less') : t('card.more'), chev(12)),
        !open && el('button', { type: 'button', class: 'remove', onclick: () => { choosing = c.key; render(); } }, t('card.remove'))),
      open && el('div', { class: 'choose', role: 'group', 'aria-label': t('card.remove_group') },
        el('p', {}, t('card.remove_because')),
        el('div', { class: 'choose-buttons' },
          el('button', { type: 'button', class: 'applied', onclick: () => setOutcome(c, 'applied') }, t('card.applied')),
          el('button', { type: 'button', class: 'notrel', onclick: () => setOutcome(c, 'not_relevant') }, t('card.not_relevant')),
          el('button', { type: 'button', class: 'cancel', onclick: () => { choosing = null; render(); } }, t('card.cancel'))),
        c.mine && el('button', { type: 'button', class: 'mistake', onclick: () => removeMistake(c) }, t('card.mistake'))));
    return node;
  }

  function addForm(catKey) {
    const f = form;
    const bind = name => ({ name, value: f[name], oninput: e => { f[name] = e.target.value; } });
    return el('form', { class: 'addform', 'data-addform': '1', onsubmit: submitForm, novalidate: true },
      el('p', { class: 'form-title' }, t('form.title', { category: catLabel(catKey) })),
      el('label', {}, el('span', {}, t('form.link')), el('input', { type: 'url', inputmode: 'url', placeholder: 'https://…', autocomplete: 'off', ...bind('url') })),
      el('label', {}, el('span', {}, t('form.job_title')), el('input', { type: 'text', ...bind('title') })),
      el('label', {}, el('span', {}, t('form.company')), el('input', { type: 'text', ...bind('company') })),
      el('label', {}, el('span', {}, t('form.city')), el('input', { type: 'text', ...bind('city') })),
      el('fieldset', {}, el('legend', {}, t('form.area')),
        ...boardAreas().map(a => el('label', { class: 'radio' },
          el('input', { type: 'radio', name: 'area', value: a.key, checked: f.area === a.key, onchange: () => { f.area = a.key; } }), label(a)))),
      f.error && el('p', { class: 'form-error', role: 'alert' }, f.error),
      el('div', { class: 'form-buttons' },
        el('button', { type: 'submit', class: 'save', disabled: f.busy }, f.busy ? t('form.saving') : t('form.save')),
        el('button', { type: 'button', class: 'cancel', onclick: closeForm }, t('form.cancel'))));
  }

  function themeButton() {
    const name = t('theme.' + theme), title = t('theme.' + theme + '_title');
    const btn = el('button', { type: 'button', class: 'ubtn theme', title, 'aria-label': title }, themeIcon(theme), name);
    btn.addEventListener('click', () => {
      theme = { auto: 'light', light: 'dark', dark: 'auto' }[theme];
      store.set('radar.theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
      btn.replaceWith(themeButton());
    });
    return btn;
  }

  // The language switch names the other language in that language ("English" on the German page, "Deutsch" on the English one).
  function langButton() {
    const other = getLang() === 'de' ? 'en' : 'de';
    return el('button', { type: 'button', class: 'ubtn lang', lang: other, title: t('util.lang_title'), 'aria-label': t('util.lang_title'),
      onclick: () => { setLang(other); render(); } }, t('util.lang_switch'));
  }

  function render() {
    if (pendingData && !form && !choosing) { applyData(pendingData); pendingData = null; }
    if (!boards.some(b => b.key === board)) board = 'de';
    const de = getLang() === 'de';
    const regions = boardAreas();
    if (area !== 'all' && !regions.some(a => a.key === area)) area = 'all';
    const all = cards();
    const openAll = all.filter(c => !outcomeOf(marks.get(c.key)));
    const openList = openAll.filter(c => boardOf(c.area) === board);
    const record = recordItems(all);
    const applied = record.filter(r => r.outcome === 'applied');
    const notRelevant = record.filter(r => r.outcome === 'not_relevant');
    const shownAreas = area === 'all' ? regions : regions.filter(a => a.key === area);
    const toRecord = e => { e.preventDefault(); toggleSec('record', true); };

    if (cat !== 'all' && !categories.some(c => c.key === cat)) cat = 'all';
    const areaCount = key => openList.filter(c => (key === 'all' || c.area === key) && (cat === 'all' || c.category === cat)).length;
    const catCount = key => openList.filter(c => (key === 'all' || c.category === key) && (area === 'all' || c.area === area)).length;
    const setArea = key => { area = key; store.set('radar.area', key); filterClosed.clear(); render(); };
    const setBoard = key => {
      if (key === board) return;
      board = key; store.set('radar.board', key);
      area = 'all'; store.set('radar.area', 'all'); filterClosed.clear(); form = null; choosing = null;
      render();
      scrollTo({ top: 0, behavior: 'instant' });
    };
    const boardSwitch = el('div', { class: 'boardrow' },
      el('div', { class: 'seg', role: 'group', 'aria-label': t('board.group') },
        ...boards.map(b => el('button', {
          type: 'button', class: 'segbtn' + (board === b.key ? ' on' : ''), 'aria-pressed': String(board === b.key),
          onclick: () => setBoard(b.key) }, label(b),
          el('span', { class: 'n' }, openAll.filter(c => boardOf(c.area) === b.key).length)))));
    const setCat = key => {
      cat = key; store.set('radar.cat', key);
      if (key !== 'all') { openSecs.add(key); saveOpen(); }   // the one category you picked is shown open
      render();
    };
    const tag = (text, undo, title) => el('button', { type: 'button', class: 'tag', title, onclick: undo },
      text, el('i', { 'aria-hidden': 'true' }, '×'));
    const tags = [
      area !== 'all' && tag(areaLabel(area), () => setArea('all'), t('filter.clear_area')),
      cat !== 'all' && tag(catLabel(cat), () => setCat('all'), t('filter.clear_category')),
    ].filter(Boolean);

    const panel = el('div', { class: 'fpanel', id: 'fpanel', 'data-open': filterOpen ? '1' : '0', inert: !filterOpen },
      el('div', { class: 'fpanel-i' }, el('div', { class: 'fcard' },
        el('div', {},
          el('p', { class: 'flabel' }, t('filter.area')),
          el('div', { class: 'seg', role: 'group', 'aria-label': t('filter.area') },
            ...[{ key: 'all', all: true }, ...regions].map(a => el('button', {
              type: 'button', class: 'segbtn' + (area === a.key ? ' on' : ''), 'aria-pressed': String(area === a.key),
              onclick: () => setArea(a.key) }, a.all ? t('filter.all_areas') : label(a), el('span', { class: 'n' }, areaCount(a.key)))))),
        el('div', {},
          el('p', { class: 'flabel' }, t('filter.category')),
          el('div', { class: 'cchips', role: 'group', 'aria-label': t('filter.category') },
            el('button', { type: 'button', class: 'cchip all' + (cat === 'all' ? ' on' : ''), 'aria-pressed': String(cat === 'all'),
              onclick: () => setCat('all') }, t('filter.all_categories'), el('span', { class: 'n' }, catCount('all'))),
            ...categories.map((c, i) => el('button', {
              type: 'button', class: 'cchip' + (cat === c.key ? ' on' : ''), 'data-cat': c.key, 'aria-pressed': String(cat === c.key),
              onclick: () => setCat(cat === c.key ? 'all' : c.key) },
              el('span', { class: 'jn' }, String(i + 1).padStart(2, '0')), label(c), el('span', { class: 'n' }, catCount(c.key)))))))));
    const fbtn = el('button', { type: 'button', class: 'fbtn', 'aria-expanded': String(filterOpen), 'aria-controls': 'fpanel',
      onclick: () => {
        filterOpen = !filterOpen;
        panel.setAttribute('data-open', filterOpen ? '1' : '0');
        panel.inert = !filterOpen;
        fbtn.setAttribute('aria-expanded', String(filterOpen));
      } }, t('filter.button'), chev(12));

    const root = el('div', { class: 'board' });
    root.append(el('header', { class: 'top' },
      el('div', { class: 'topline' },
        el('p', { class: 'kicker' }, t('app.kicker')),
        el('div', { class: 'utility', role: 'group', 'aria-label': t('util.group') },
          el('button', { type: 'button', class: 'ubtn', onclick: () => foldAll(true) }, t('util.expand_all')),
          el('button', { type: 'button', class: 'ubtn', onclick: () => foldAll(false) }, t('util.collapse_all')),
          el('a', { class: 'ubtn absagen-link', href: de ? '/absagen' : '/absagen?lang=en' }, t('util.absagen')),
          langButton(),
          themeButton(),
          el('a', { class: 'ubtn quiet signout', href: SIGN_OUT_URL }, t('util.sign_out')))),
      boardSwitch,
      el('div', { class: 'titlerow' },
        el('h1', {}, board === 'eu' ? t('head.open_eu') : t('head.open_de')),
        el('div', { class: 'tally' },
          el('span', { class: 't open' }, el('b', {}, openList.length), el('span', {}, t('tally.open'))),
          el('a', { href: '#record', class: 't applied', onclick: toRecord }, el('b', {}, applied.length), el('span', {}, t('tally.applied'))),
          el('a', { href: '#record', class: 't notrel', onclick: toRecord }, el('b', {}, notRelevant.length), el('span', {}, t('tally.not_relevant'))))),
      el('div', { class: 'filterrow' }, fbtn, ...tags, !tags.length && el('span', { class: 'fnote' }, t('filter.none'))),
      panel));

    if (banner) root.append(el('p', { class: 'banner', role: 'alert' }, banner));

    const main = el('main', { class: 'sections' });
    categories.forEach((c, i) => {
      if (cat !== 'all' && c.key !== cat) return;
      const inCat = openList.filter(x => x.category === c.key);
      const shown = inCat.filter(x => area === 'all' || x.area === area).length;
      const counts = regions.map(a => el('span', {}, label(a) + ' ' + inCat.filter(x => x.area === a.key).length));
      const formHere = form && form.category === c.key;
      const body = [
        formHere ? addForm(c.key)
          : el('div', { class: 'sec-tools' }, el('button', { type: 'button', class: 'add', onclick: () => openForm(c.key) }, t('sec.add'))),
      ];
      for (const a of shownAreas) {
        body.push(foldArea(c.key, a, inCat.filter(x => x.area === a.key).sort((x, y) => y.sortKey.localeCompare(x.sortKey))));
      }
      main.append(foldSection(c.key, { class: 'cat', id: 'cat-' + c.key, 'data-cat': c.key },
        [el('h2', {}, el('span', { class: 'num' }, String(i + 1).padStart(2, '0')), label(c)),
         el('p', { class: 'counts' }, el('span', { class: 'lead' }, t('sec.open_count', { n: shown })), ' · ',
           ...counts.flatMap((x, j) => (j ? [' · ', x] : [x])))],
        body, label(c)));
    });

    const recordList = (items, empty) => items.length
      ? el('ul', {}, ...items.map(r => el('li', {},
          el('span', { class: 'when' }, dateLabel(r.at)),
          el('span', { class: 'what' },
            r.url ? el('a', { href: r.url, target: '_blank', rel: 'noopener noreferrer' }, r.title) : r.title,
            el('span', { class: 'meta' }, [r.company, r.category && catLabel(r.category), r.area && areaLabel(r.area)].filter(Boolean).join(' · ')),
            stageLabel(r.stage) && r.stage !== 'applied' ? el('span', { class: 'stage ' + r.stage }, stageLabel(r.stage) + (r.stageAt ? ' · ' + dateLabel(r.stageAt) : '')) : null,
            stageLabel(r.stage) && r.stage !== 'applied' && r.stageNote ? el('span', { class: 'src' }, r.stageNote) : null),
          el('button', { type: 'button', class: 'undo', title: t('record.undo_title'),
            onclick: () => setOutcome({ key: r.key }, null) }, t('record.undo')))))
      : el('p', { class: 'empty' }, empty);
    main.append(foldSection('record', { class: 'cat record', id: 'record', 'data-cat': 'record' },
      [el('h2', {}, t('record.title')),
       el('p', { class: 'counts' }, el('span', { class: 'lead' }, t('record.counts', { applied: applied.length, notrel: notRelevant.length })))],
      [el('div', { class: 'record-cols' },
        el('div', {}, el('h3', {}, t('record.applied') + ' ', el('span', { class: 'count' }, applied.length)), recordList(applied, t('record.empty'))),
        el('div', {}, el('h3', {}, t('record.not_relevant') + ' ', el('span', { class: 'count' }, notRelevant.length)), recordList(notRelevant, t('record.empty'))))],
      t('record.label')));

    const logStatus = s => (['portal_invitation', 'unclear', ...STAGES].includes(s) ? t('stage.' + s) : s);
    const logRows = applicationLog.toSorted((a, b) => String(b.date).localeCompare(String(a.date)));
    const logBody = el('div', {},
      el('p', { class: 'intro' }, t('log.intro')),
      el('ul', {}, ...logRows.map(r => el('li', { 'data-email-entry': r.id },
        el('span', { class: 'when' }, dateLabel(r.date)),
        el('span', { class: 'what' }, r.title || t('log.untitled'),
          el('span', { class: 'meta' }, [r.company, r.cards.length ? r.cards.map(n => t('card.number', { n })).join(', ') : t('log.off_list')].join(' · ')),
          el('span', { class: 'stage ' + r.status }, logStatus(r.status)),
          r.note && el('span', { class: 'src' }, r.note))))));
    const logCount = meta.log_updated
      ? t('log.counts_dated', { n: applicationLog.length, date: dateLabel(meta.log_updated) })
      : t('log.counts', { n: applicationLog.length });
    main.append(foldSection('email-log', { class: 'cat record', id: 'cat-email-log', 'data-cat': 'record' },
      [el('h2', {}, t('log.title')), el('p', { class: 'counts' }, logCount)],
      [logBody], t('log.label')));
    root.append(main);

    // The list rules are data (meta), written in both languages; English is the fallback.
    const ruleKey = (board === 'eu' ? 'rule_eu' : 'rule');
    const rule = (de && (meta[ruleKey + '_de'] ?? (board === 'eu' ? meta.rule_de : null))) || meta[ruleKey] || meta.rule || '';
    root.append(el('footer', {},
      el('p', { lang: de && (meta[ruleKey + '_de'] || (board === 'eu' && meta.rule_de)) ? 'de' : 'en' }, rule),
      el('p', {}, t('footer.updated', { date: meta.updated ? dateLabel(meta.updated) : '—' }))));
    fill(mount, root);
    headObserver.disconnect();
    for (const head of mount.querySelectorAll('.cat > [data-head]')) headObserver.observe(head);
  }

  render();

  return {
    updateData(next) {
      // Never redraw under a half-typed form or an open Remove choice.
      if (form || choosing) { pendingData = next; return; }
      applyData(next);
      render();
    },
  };
}
