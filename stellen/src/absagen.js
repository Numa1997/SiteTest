// The Absagen page, in three kinds of request so each stays small (Cloudflare's free plan allows about 10 ms of
// computing per request):
//   GET /absagen                    the page: header, cover, index (one small query) and empty space for the mails
//   GET /absagen/part?offset=N      20 mails as ready HTML, oldest first; public/app/absagen.js fetches them one after another
//   GET /absagen/img/<gmail_id>/<n> one image the mail carried inside itself
// Printing (button "Drucken / als PDF", which waits until every mail is loaded) gives the document: a cover, an index,
// one mail per page, page x / y.
//
// Security: owner sign-in for all three (src/worker.js). The page has its own strict policy (PAGE_CSP): scripts only from
// this site, requests only to this site, images only from this site or as data:. The mail HTML was cleaned on arrival
// (src/sanitize.js) and is stored only in that form; this file escapes every other value it writes.
import { sender } from './mail.js';

export const PAGE_CSP = [
  "default-src 'none'", "script-src 'self'", "style-src 'self' 'unsafe-inline'", "img-src 'self' data:", "font-src 'self'",
  "connect-src 'self'", "frame-src 'none'", "object-src 'none'", "base-uri 'none'", "form-action 'none'", "frame-ancestors 'none'",
].join('; ');
const PART = 20;

const T = {
  de: {
    lang: 'de', title: 'Absagen', kicker: 'Stellenrecherche · Absagen', board: '← Zur Liste', print: 'Drucken / als PDF', other: 'EN',
    count: 'Absagen', first: 'erste', last: 'letzte', index: 'Inhalt', to: 'an', cc: 'Kopie', attachments: 'Anhänge',
    empty: 'Noch keine Absagen angekommen. Sie kommen aus dem Gmail-Label „Absagen“, sobald das Gmail-Skript eingerichtet ist.',
    cover_sub: 'Alle Absagen aus dem Gmail-Label „Absagen“, nach Eingang geordnet.', generated: 'Erstellt', footer: 'Absagen · Numa Koudsie',
    log: 'Im Bewerbungsprotokoll', nolog: 'Vor dem Bewerbungsprotokoll (vor dem 1. 9. 2026)', plain: 'Nur Text vorhanden', locale: 'de-DE',
    loading: 'Absagen werden geladen', loaded: 'Alle Absagen geladen', failed: 'Laden unterbrochen. Seite neu laden.',
    incomplete: 'UNVOLLSTÄNDIG: gedruckt, bevor alle Absagen geladen waren. Bitte die Taste „Drucken / als PDF“ benutzen.',
  },
  en: {
    lang: 'en', title: 'Rejections', kicker: 'Job search · Rejections', board: '← Back to the list', print: 'Print / save as PDF', other: 'DE',
    count: 'rejections', first: 'first', last: 'last', index: 'Contents', to: 'to', cc: 'cc', attachments: 'Attachments',
    empty: 'No rejections yet. They come from the Gmail label "Absagen" once the Gmail script is set up.',
    cover_sub: 'Every rejection from the Gmail label "Absagen", in the order received.', generated: 'Generated', footer: 'Rejections · Numa Koudsie',
    log: 'In the application log', nolog: 'Before the application log (before 1 Sep 2026)', plain: 'Text only', locale: 'en-GB',
    loading: 'Loading rejections', loaded: 'All rejections loaded', failed: 'Loading stopped. Reload the page.',
    incomplete: 'INCOMPLETE: printed before every rejection had loaded. Please use the "Print / save as PDF" button.',
  },
};
const lang = url => T[url.searchParams.get('lang') === 'en' ? 'en' : 'de'];

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

const FORMATS = new Map();   // building an Intl.DateTimeFormat costs ~0.1 ms: one per language and style, reused
function fmtDate(iso, t, withTime = true) {
  const key = t.locale + withTime;
  if (!FORMATS.has(key)) {
    FORMATS.set(key, new Intl.DateTimeFormat(t.locale, withTime
      ? { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Berlin' }
      : { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Europe/Berlin' }));
  }
  return FORMATS.get(key).format(new Date(iso));
}

const initial = s => (String(s).trim().match(/[A-Za-zÄÖÜäöü0-9]/)?.[0] ?? '?').toUpperCase();
// The avatar colour follows the sender, like Gmail's letter avatars; taken from the board's own accents.
const AVATAR = ['av-wine', 'av-slate', 'av-amber', 'av-ok', 'av-ink'];
const hue = s => AVATAR[[...String(s)].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7) % AVATAR.length];

const HEADERS = {
  'Content-Security-Policy': PAGE_CSP, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer',
  'X-Frame-Options': 'DENY', 'X-Robots-Tag': 'noindex, nofollow', 'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Resource-Policy': 'same-origin', 'Strict-Transport-Security': 'max-age=31536000',
};
const html = body => new Response(body, { headers: { 'Content-Type': 'text/html; charset=utf-8', ...HEADERS } });

/** GET /absagen */
export async function renderShell(db, url) {
  const t = lang(url);
  const { results: mails } = await db.prepare(`select gmail_id, received_at, from_header, subject from mail_rejections
    where label_present = 1 order by received_at asc, gmail_id asc`).all();
  const n = mails.length;
  const range = n ? `${esc(fmtDate(mails[0].received_at, t, false))} – ${esc(fmtDate(mails[n - 1].received_at, t, false))}` : '';
  const other = t.lang === 'de' ? 'en' : 'de';
  return html(`<!doctype html>
<html lang="${t.lang}" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${esc(t.title)} · Stellenrecherche</title>
<link rel="stylesheet" href="/fonts/instrument-plex.css">
<link rel="stylesheet" href="/styles/board.css">
<link rel="stylesheet" href="/styles/absagen.css">
<script src="/app/absagen.js" defer></script>
</head>
<body>
<div class="board absagen" data-count="${n}" data-part="${PART}" data-lang="${t.lang}"
  data-loading="${esc(t.loading)}" data-loaded="${esc(t.loaded)}" data-failed="${esc(t.failed)}">
<header class="top screenonly">
  <div class="topline">
    <p class="kicker">${esc(t.kicker)}</p>
    <div class="utility">
      <a class="ubtn" href="/">${esc(t.board)}</a>
      <a class="ubtn lang" href="/absagen?lang=${other}">${esc(t.other)}</a>
      <button type="button" class="ubtn printbtn" id="print"${n ? '' : ' disabled'}>${esc(t.print)}</button>
    </div>
  </div>
  <div class="titlerow">
    <h1>${esc(t.title)}</h1>
    <div class="tally">
      <span class="t notrel"><b>${n}</b><span>${esc(t.count)}</span></span>
      ${n ? `<span class="t"><b class="d">${esc(fmtDate(mails[0].received_at, t, false))}</b><span>${esc(t.first)}</span></span>
      <span class="t"><b class="d">${esc(fmtDate(mails[n - 1].received_at, t, false))}</b><span>${esc(t.last)}</span></span>` : ''}
    </div>
  </div>
  <p class="progress" id="progress" role="status" aria-live="polite"></p>
</header>
<section class="cover printonly">
  <p class="kicker">${esc(t.kicker)}</p>
  <h1>${esc(t.title)}</h1>
  <p class="cover-n"><b>${n}</b> ${esc(t.count)}${range ? ' · ' + range : ''}</p>
  <p class="cover-sub">${esc(t.cover_sub)}</p>
  <p class="cover-gen">${esc(t.generated)}: ${esc(fmtDate(new Date().toISOString(), t))}</p>
</section>
${n ? `<nav class="index" aria-label="${esc(t.index)}">
  <h2>${esc(t.index)}</h2>
  <ol>${mails.map((m, i) => {
    const s = sender(m.from_header);
    return `<li><a href="#m${esc(m.gmail_id)}"><span class="ino">${String(i + 1).padStart(3, '0')}</span><span class="idate">${esc(fmtDate(m.received_at, t, false))}</span><span class="ifrom">${esc(s.name || s.address)}</span><span class="isubj">${esc(m.subject)}</span></a></li>`;
  }).join('')}</ol>
</nav>` : `<p class="empty-big">${esc(t.empty)}</p>`}
<p class="incomplete printonly" id="incomplete">${esc(t.incomplete)}</p>
<main class="mails" id="mails"></main>
<footer class="pagefoot screenonly"><p>${esc(t.footer)} · ${esc(fmtDate(new Date().toISOString(), t))}</p></footer>
</div>
</body>
</html>
`);
}

function article(m, i, t) {
  const s = sender(m.from_header);
  const name = s.name || s.address;
  const atts = JSON.parse(m.attachments || '[]');
  const body = m.body_html
    ? `<div class="mb html"><template class="mbt">${m.body_html}</template></div>`
    : `<div class="mb plain"><p class="plain-note">${esc(t.plain)}</p><pre>${esc(m.body_text)}</pre></div>`;
  return `<article class="mail" id="m${esc(m.gmail_id)}">
<header class="mh">
  <p class="mno">${String(i + 1).padStart(3, '0')}</p>
  <h2 class="subj">${esc(m.subject || '—')}</h2>
  <div class="who">
    <span class="av ${hue(s.address)}" aria-hidden="true">${esc(initial(name))}</span>
    <div class="from"><b>${esc(name)}</b> <span class="addr">&lt;${esc(s.address)}&gt;</span>
      <div class="to">${esc(t.to)} ${esc(m.to_header)}${m.cc_header ? ' · ' + esc(t.cc) + ' ' + esc(m.cc_header) : ''}</div></div>
    <time class="when" datetime="${esc(m.received_at)}">${esc(fmtDate(m.received_at, t))}</time>
  </div>
  ${atts.length ? `<p class="atts"><span>${esc(t.attachments)}:</span> ${atts.map(a => `<span class="att">${esc(a)}</span>`).join(' ')}</p>` : ''}
</header>
${body}
<footer class="mf">${m.log_id ? `${esc(t.log)}: <code>${esc(m.log_id)}</code>` : esc(t.nolog)}</footer>
</article>
`;
}

/** GET /absagen/part?offset=N : the next 20 mails, as HTML for the page to append. */
export async function renderPart(db, url) {
  const t = lang(url);
  const offset = Math.max(0, Math.min(100000, Number.parseInt(url.searchParams.get('offset') ?? '0', 10) || 0));
  // First the sizes (cheap), then only as many full rows as fit in about 1 MB, so no answer reads more than it sends.
  const { results: sizes } = await db.prepare(`select gmail_id, length(body_html) + length(body_text) as size from mail_rejections
    where label_present = 1 order by received_at asc, gmail_id asc limit ? offset ?`).bind(PART, offset).all();
  const ids = [];
  let bytes = 0;
  for (const r of sizes) {
    if (ids.length && bytes + r.size > 1_000_000) break;
    bytes += r.size;
    ids.push(r.gmail_id);
  }
  const { results } = ids.length ? await db.prepare(`select gmail_id, received_at, from_header, to_header, cc_header, subject, attachments,
    body_text, body_html, log_id from mail_rejections where gmail_id in (${ids.map(() => '?').join(',')}) order by received_at asc, gmail_id asc`)
    .bind(...ids).all() : { results: [] };
  const parts = results.map((m, j) => article(m, offset + j, t));
  const res = html(parts.join(''));
  res.headers.set('X-Part-Count', String(parts.length));
  return res;
}

/** GET /absagen/img/<gmail_id>/<n> */
export async function renderImage(db, gmailId, n) {
  const row = await db.prepare('select mime, data_b64 from mail_images where gmail_id = ? and n = ?').bind(gmailId, n).first();
  if (!row) return new Response('Not found', { status: 404, headers: { 'Content-Type': 'text/plain', ...HEADERS } });
  const bin = atob(row.data_b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new Response(bytes, {
    headers: { 'Content-Type': row.mime, ...HEADERS, 'Content-Security-Policy': "default-src 'none'; sandbox", 'Cache-Control': 'private, max-age=86400' },
  });
}
