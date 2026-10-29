// The rejection e-mails: what the Gmail script (apps-script/Code.gs) sends, and how each mail feeds the
// e-mail log (application_log).
//
//   POST /api/ingest/known      { gmail_ids: [...] }              -> { missing: [...] }   ids the server still needs
//   POST /api/ingest/rejections { messages: [...] }               -> { results: [{ gmail_id, status, error? }] }
//   POST /api/ingest/present    { gmail_ids: [...], force? }      -> { hidden, restored }  ids that still carry the label
//
// Only the Gmail script's service token reaches these routes (src/access.js, requireService).
// Built for Cloudflare's free plan: per request at most a few database calls (every write of one mail is one
// db.batch, which D1 runs as one transaction and counts as one call) and a few milliseconds of computing.
//
// Safety rules:
// - Each mail is judged on its own: a bad mail is refused with a reason, the others are stored.
// - The mail HTML is cleaned once, on arrival (src/sanitize.js); the page only ever shows the cleaned copy.
// - The e-mail log is changed only by rule (feedLog), every change is written to mail_events with the values
//   it replaced, in the same transaction, and taking the label off the mail in Gmail undoes the change.
// - Nothing the user wrote is deleted; the only row ever deleted is one this pipeline added itself, when the
//   mail that caused it loses its label.
import { ApiError } from './validate.js';
import { sanitizeMail } from './sanitize.js';

export const MAX_INGEST_BODY = 2 * 1024 * 1024;   // one POST from the script (it sends one mail, at most ~1.3 MB)
const MAX_IDS = 5000;
const MAX_MESSAGES = 5;
const MAX_HTML_CLEAN = 120_000;                   // longer HTML is kept as text only (cleaning stays within the free plan's CPU time)
const MAX_IMAGE_B64 = 420_000;                    // one inline image, base64 characters (the script sends at most 300 KB = 409,600)
const MAX_IMAGES_B64 = 840_000;                   // all inline images of one mail (the script sends at most 600 KB = 819,200)
// The e-mail log covers the current search; older mails live only on /absagen.
export const LOG_SINCE = '2026-09-01';

const ID = /^[0-9a-f]{8,32}$/;
const cut = (v, max) => (typeof v === 'string' ? v.slice(0, max) : '');

export function validIds(input) {
  const ids = input?.gmail_ids;
  if (!Array.isArray(ids) || ids.length > MAX_IDS || !ids.every(x => typeof x === 'string' && ID.test(x))) {
    throw new ApiError(400, 'invalid_ids');
  }
  return [...new Set(ids)];
}

const FIELDS = ['gmail_id', 'thread_id', 'received_at', 'from', 'to', 'cc', 'subject', 'date_header', 'labels', 'snippet', 'text', 'html',
  'attachments', 'images'];
const MIME = /^image\/(png|jpeg|gif|webp)$/;

/** One mail as the Gmail script sends it -> a clean row, or ApiError 400 naming the field. Long headers are cut, not refused. */
export function cleanMessage(m) {
  if (!m || typeof m !== 'object' || Array.isArray(m) || !Object.keys(m).every(k => FIELDS.includes(k))) {
    throw new ApiError(400, 'invalid_message');
  }
  if (typeof m.gmail_id !== 'string' || !ID.test(m.gmail_id)) throw new ApiError(400, 'invalid_field', { field: 'gmail_id' });
  const thread = typeof m.thread_id === 'string' && ID.test(m.thread_id) ? m.thread_id : '';
  const at = typeof m.received_at === 'string' && m.received_at.length <= 40 ? Date.parse(m.received_at) : NaN;
  if (!Number.isFinite(at)) throw new ApiError(400, 'invalid_field', { field: 'received_at' });
  if (!Array.isArray(m.labels) || !m.labels.includes('Absagen')) throw new ApiError(400, 'invalid_field', { field: 'labels' });
  const attachments = (Array.isArray(m.attachments) ? m.attachments : []).filter(a => typeof a === 'string').slice(0, 50).map(a => a.slice(0, 300));
  // Inline images (src="cid:…" in the HTML), sent beside the HTML so the page can load each one separately.
  const images = [];
  let total = 0;
  for (const img of Array.isArray(m.images) ? m.images.slice(0, 30) : []) {
    if (!img || typeof img.cid !== 'string' || typeof img.mime !== 'string' || typeof img.b64 !== 'string') continue;
    const mime = img.mime.toLowerCase().replace('image/jpg', 'image/jpeg');
    if (!MIME.test(mime) || img.b64.length > MAX_IMAGE_B64 || total + img.b64.length > MAX_IMAGES_B64 || !/^[A-Za-z0-9+/=]*$/.test(img.b64)) continue;
    total += img.b64.length;
    images.push({ cid: img.cid.slice(0, 300), mime, b64: img.b64 });
  }
  const text = cut(m.text, 300_000);
  const rawHtml = typeof m.html === 'string' ? m.html : '';
  let html = '';
  if (rawHtml && rawHtml.length <= MAX_HTML_CLEAN) {
    const index = new Map(images.map((img, n) => [img.cid.replace(/^<|>$/g, ''), n]));
    html = sanitizeMail(rawHtml, cid => {
      const n = index.get(decodeURIComponentSafe(cid).replace(/^<|>$/g, ''));
      return n === undefined ? null : `/absagen/img/${m.gmail_id}/${n}`;
    });
    // A mail whose HTML says nothing readable (broken markup, all images) is shown as its text instead.
    if (text && html.replace(/<[^>]*>/g, '').replace(/&nbsp;|\s/g, '').length < 20) html = '';
  }
  return {
    gmail_id: m.gmail_id, thread_id: thread, received_at: new Date(at).toISOString(),
    from_header: cut(m.from, 1000), to_header: cut(m.to, 2000), cc_header: cut(m.cc, 2000),
    subject: cut(m.subject, 1000), date_header: cut(m.date_header, 200), snippet: cut(m.snippet, 500),
    body_text: text, body_html: html, attachments: JSON.stringify(attachments), images,
  };
}

function decodeURIComponentSafe(s) { try { return decodeURIComponent(s); } catch { return s; } }

// ---- who sent it ----------------------------------------------------------------

// Applicant-tracking systems and mail services send for many employers: their names say nothing about the company.
const ATS = new Set(['myworkday', 'workday', 'personio', 'softgarden', 'smartrecruiters', 'greenhouse', 'lever', 'hire', 'ashbyhq', 'teamtailor',
  'join', 'recruitee', 'successfactors', 'sapsf', 'concludis', 'indeed', 'indeedemail', 'hrworks', 'communication', 'jobylon', 'onlyfy',
  'dvinci', 'easy', 'icims', 'talent', 'workablemail', 'candidates', 'bamboohr', 'app', 'breezy', 'gmail', 'googlemail', 'guidecom',
  'connect', 'recruitmail', 'cc', 'easycruit', 'applytojob', 'xing', 'linkedin', 'workwise', 'jobvalley', 'mail', 'msg', 'mg', 'notification',
  'notifications', 'noreply', 'no', 'reply', 'jobs', 'job', 'careers', 'career', 'karriere', 'recruiting', 'recruitment', 'bewerbung',
  'bewerbungen', 'hr', 'info', 'kontakt', 'contact', 'team', 'www', 'email', 'e', 'de', 'com', 'net', 'org', 'eu', 'io', 'co', 'uk', 'at', 'ch']);
const STOP = new Set(['gmbh', 'mbh', 'ag', 'se', 'kg', 'co', 'ug', 'inc', 'ltd', 'llc', 'group', 'gruppe', 'the', 'und', 'and', 'der', 'die',
  'das', 'für', 'for', 'von', 'deutschland', 'germany', 'solutions', 'services', 'service', 'technologies', 'technology', 'systems', 'system',
  'recruiting', 'agency', 'casting', 'leipzig', 'berlin', 'consulting', 'engineering', 'international', 'europe', 'holding']);

const words = s => (String(s).toLowerCase().match(/[a-z0-9äöüß]+/g) ?? []);
const keyWords = s => words(s).filter(w => w.length >= 3 && !STOP.has(w));

export function sender(fromHeader) {
  const m = /^\s*"?([^"<]*?)"?\s*<([^>]+)>\s*$/.exec(fromHeader) || [null, '', String(fromHeader).trim()];
  const address = m[2].trim().toLowerCase();
  const [local = '', domain = ''] = address.split('@');
  const labels = domain.split('.').filter(Boolean);
  const orgLabel = labels.length >= 2 && !ATS.has(labels[labels.length - 2]) ? labels[labels.length - 2] : '';
  // Words that can name the employer: the display name, the address before "@", the domain parts that are not a mail service.
  const tokens = [...words(m[1]), ...words(local), ...labels.slice(0, -1).flatMap(words)].filter(w => !ATS.has(w));
  return { name: m[1].trim(), address, domain, orgLabel, tokens };
}

/** Does this log row's company appear in who sent the mail or in its subject? (Never the body: a body may name other firms.) */
export function companyMatches(company, mail) {
  const keys = keyWords(company);
  if (!keys.length) return false;
  const s = sender(mail.from_header);
  const hay = new Set([...s.tokens, ...words(mail.subject)]);
  const glued = s.tokens.filter(t => t.length >= 6);   // "zeissgroup", "energymeteo": company words run together
  const hit = k => hay.has(k) || (k.length >= 5 && glued.some(t => t.includes(k)));
  const hits = keys.filter(hit).length;
  return hits >= Math.min(2, keys.length);
}

/** How many of the log title's words (and reference numbers) the mail repeats. */
export function titleScore(title, mail) {
  const keys = new Set(keyWords(String(title).replace(/\((?:m|w|d|f|x|div|all genders)[^)]*\)/gi, ' ')));
  if (!keys.size) return 0;
  const hay = new Set([...words(mail.subject), ...words(mail.body_text.slice(0, 6000))]);
  let n = 0;
  for (const k of keys) if (hay.has(k)) n += /^\d{4,}$/.test(k) ? 3 : 1;
  return n;
}

const day = iso => iso.slice(0, 10);
const daysApart = (a, b) => Math.abs(Date.parse(a) - Date.parse(b)) / 86_400_000;
// Rows a rejection may close by itself. An interview is never closed automatically: that is Numa's call.
const OPEN = ['confirmed', 'unclear', 'portal_invitation'];
const SUFFIX = ' (Gmail label Absagen, automatic)';

const ev = (db, at, gmailId, kind, detail) => db.prepare('insert into mail_events (at, gmail_id, kind, detail) values (?, ?, ?, ?)')
  .bind(at, gmailId, kind, typeof detail === 'string' ? detail : JSON.stringify(detail));

/**
 * What a new rejection mail does to the e-mail log, as statements to run in the mail's transaction:
 *  - one row of the same company already marked rejected within 7 days (or picked by title): linked, nothing changes;
 *  - one open row (confirmed, unclear, portal invitation) of that company, dated on or before the mail: it becomes "rejected";
 *  - otherwise (none, several, or an interview): a new row "mail-<gmail_id>", so nothing is guessed onto the wrong application.
 * Returns { logId, statements }.
 */
export function planLog(db, log, mail, at) {
  if (day(mail.received_at) < LOG_SINCE) return { logId: null, effect: null, statements: [] };
  const same = log.filter(r => companyMatches(r.company, mail));
  let pick = null;
  if (same.length > 1) {
    const scored = same.map(r => [titleScore(r.title, mail), r]).sort((a, b) => b[0] - a[0]);
    if (scored[0][0] > 0 && scored[0][0] > scored[1][0]) pick = scored[0][1];
  }
  const pool = pick ? [pick] : same;
  const done = pool.filter(r => r.status === 'rejected' && (pick || (r.date && daysApart(r.date, mail.received_at) <= 7)));
  const open = pool.filter(r => OPEN.includes(r.status) && (!r.date || r.date <= day(mail.received_at)));
  if (done.length === 1 && !open.length) {
    return { logId: done[0].id, effect: null, statements: [ev(db, at, mail.gmail_id, 'log_linked', { id: done[0].id, unchanged: true })] };
  }
  if (open.length === 1 && !done.length && !pool.some(r => r.status === 'interview' && r !== open[0] && !pick)) {
    const r = open[0];
    const note = ((r.note ? r.note + ' · ' : '') + 'Rejection ' + day(mail.received_at) + SUFFIX).slice(0, 2000);
    const source = ((r.source ? r.source + ' + ' : '') + 'gmail-auto').slice(0, 300);
    return {
      logId: r.id,
      effect: { id: r.id, status: 'rejected', date: day(mail.received_at), note, source },
      statements: [
        db.prepare('update application_log set status = ?, date = ?, note = ?, source = ? where id = ?').bind('rejected', day(mail.received_at), note, source, r.id),
        ev(db, at, mail.gmail_id, 'log_linked', { id: r.id, before: { status: r.status, date: r.date, note: r.note, source: r.source },
          after: { status: 'rejected', date: day(mail.received_at), note, source } }),
      ],
    };
  }
  const s = sender(mail.from_header);
  const id = 'mail-' + mail.gmail_id;
  const generic = /^(no-?reply|notifications?|jobs?|careers?|karriere|recruiting|bewerbung(en)?|hr|talent acquisition|team)$/i;
  const company = (s.name && !generic.test(s.name)) ? s.name : (s.orgLabel || s.domain);
  const note = ('From the Gmail label Absagen (automatic). Sender: ' + s.address +
    (same.length ? ' · possible matches, not guessed: ' + same.map(r => r.id + ' (' + r.status + ')').join(', ') : '')).slice(0, 2000);
  return {
    logId: id,
    effect: { id, company: company.slice(0, 300), title: mail.subject.slice(0, 300), status: 'rejected', date: day(mail.received_at), note, source: 'gmail-auto' },
    statements: [
      db.prepare(`insert into application_log (id, cards, company, title, status, date, note, source)
        values (?, '[]', ?, ?, 'rejected', ?, ?, 'gmail-auto') on conflict(id) do nothing`)
        .bind(id, company.slice(0, 300), mail.subject.slice(0, 300), day(mail.received_at), note),
      ev(db, at, mail.gmail_id, 'log_appended', { id, candidates: same.map(r => r.id) }),
    ],
  };
}

function applyEffect(log, e) {
  const r = log.find(x => x.id === e.id);
  if (r) Object.assign(r, e); else log.push({ title: '', note: '', source: '', ...e });
}

const COLS = ['thread_id', 'received_at', 'from_header', 'to_header', 'cc_header', 'subject', 'date_header', 'snippet', 'body_text', 'body_html', 'attachments'];
const LOG_SELECT = 'select id, company, title, status, date, note, source from application_log';

function imageStatements(db, row) {
  return [db.prepare('delete from mail_images where gmail_id = ?').bind(row.gmail_id),
    ...row.images.map((img, n) => db.prepare('insert into mail_images (gmail_id, n, mime, data_b64) values (?, ?, ?, ?)').bind(row.gmail_id, n, img.mime, img.b64))];
}

export async function ingest(db, input) {
  const list = input?.messages;
  if (!Array.isArray(list) || !list.length || list.length > MAX_MESSAGES) throw new ApiError(400, 'invalid_messages');
  let log = null;
  const results = [];
  for (const m of list) {
    const gmailId = typeof m?.gmail_id === 'string' && ID.test(m.gmail_id) ? m.gmail_id : null;
    let row;
    try { row = cleanMessage(m); } catch (e) {
      results.push({ gmail_id: gmailId, status: 'refused', error: e.code ?? 'invalid', field: e.extra?.field });
      continue;
    }
    const at = new Date().toISOString();
    const old = await db.prepare('select gmail_id, label_present, log_id, ' + COLS.join(', ') + ' from mail_rejections where gmail_id = ?').bind(row.gmail_id).first();
    const needsLog = !old || (old.log_id === null && day(row.received_at) >= LOG_SINCE);
    let plan = { logId: old?.log_id ?? null, statements: [] };
    if (needsLog) {
      log ??= (await db.prepare(LOG_SELECT).all()).results;
      plan = planLog(db, log, row, at);
    }
    if (!old) {
      await db.batch([
        db.prepare(`insert into mail_rejections (gmail_id, ${COLS.join(', ')}, log_id, label_present, first_seen, updated_at)
          values (?, ${COLS.map(() => '?').join(', ')}, ?, 1, ?, ?)`).bind(row.gmail_id, ...COLS.map(c => row[c]), plan.logId, at, at),
        ...imageStatements(db, row),
        ev(db, at, row.gmail_id, 'ingested', { subject: row.subject.slice(0, 200), images: row.images.length }),
        ...plan.statements,
      ]);
      results.push({ gmail_id: row.gmail_id, status: 'stored', log_id: plan.logId });
    } else {
      const changed = COLS.filter(c => row[c] !== old[c]);
      if (!changed.length && old.label_present === 1 && !plan.statements.length) { results.push({ gmail_id: row.gmail_id, status: 'unchanged' }); continue; }
      await db.batch([
        db.prepare(`update mail_rejections set ${COLS.map(c => c + ' = ?').join(', ')}, log_id = ?, label_present = 1, updated_at = ? where gmail_id = ?`)
          .bind(...COLS.map(c => row[c]), plan.logId, at, row.gmail_id),
        ...(changed.length ? [...imageStatements(db, row), ev(db, at, row.gmail_id, 'updated', { fields: changed })] : []),
        ...(old.label_present !== 1 ? [ev(db, at, row.gmail_id, 'label_restored', '')] : []),
        ...plan.statements,
      ]);
      results.push({ gmail_id: row.gmail_id, status: 'updated', log_id: plan.logId });
    }
    if (plan.effect && log) applyEffect(log, plan.effect);   // keep the in-memory log current for the next mail
  }
  return { results };
}

/** Ids the server does not have yet, plus recent ones whose log step is still missing. */
export async function known(db, input) {
  const ids = validIds(input);
  const have = new Set();
  for (let i = 0; i < ids.length; i += 90) {             // D1: at most 100 bound parameters per query
    const part = ids.slice(i, i + 90);
    const { results } = await db.prepare(`select gmail_id from mail_rejections where gmail_id in (${part.map(() => '?').join(',')})
      and not (log_id is null and received_at >= ?)`).bind(...part, LOG_SINCE).all();
    for (const r of results) have.add(r.gmail_id);
  }
  return { missing: ids.filter(id => !have.has(id)) };
}

/**
 * The full list of ids that still carry the label. Mails missing from it are hidden and their automatic log change is undone;
 * mails back in it are shown again. Refuses an empty list, and a list that would hide more than max(5, 25 %) of the shown
 * mails at once, unless force is set (only the script's hand-run function sends force).
 */
export async function present(db, input) {
  const ids = new Set(validIds(input));
  if (!ids.size) throw new ApiError(409, 'empty_list');
  const { results } = await db.prepare('select gmail_id, label_present, log_id, received_at, from_header, subject, substr(body_text, 1, 6000) as body_text from mail_rejections').all();
  const shown = results.filter(r => r.label_present === 1);
  const toHide = shown.filter(r => !ids.has(r.gmail_id));
  const toRestore = results.filter(r => r.label_present !== 1 && ids.has(r.gmail_id));
  if (input.force !== true && toHide.length > Math.max(5, shown.length / 4)) {
    throw new ApiError(409, 'suspicious_shrink', { would_hide: toHide.length, shown: shown.length });
  }
  const at = new Date().toISOString();
  const statements = [];
  const withLog = toHide.filter(r => r.log_id);
  const hiding = new Set(toHide.map(r => r.gmail_id));
  const stillFed = new Set(results.filter(r => (r.label_present === 1 && !hiding.has(r.gmail_id)) || ids.has(r.gmail_id)).map(r => r.log_id).filter(Boolean));
  const lastEvent = new Map();
  const origin = new Map();     // row id -> the event that first changed it (an update with old values, or the row's creation)
  if (withLog.length) {
    const { results: evs } = await db.prepare(`select gmail_id, kind, detail from mail_events where kind in ('log_linked','log_appended','log_reverted') order by id`).all();
    for (const e of evs) {
      lastEvent.set(e.gmail_id, e);
      const d = JSON.parse(e.detail || '{}');
      if (e.kind === 'log_reverted') origin.delete(d.id);
      else if ((e.kind === 'log_appended' || d.before) && !origin.has(d.id)) origin.set(d.id, { ...e, d });
    }
  }
  const restoreLog = toRestore.length ? (await db.prepare(LOG_SELECT).all()).results : [];
  const rows = new Map((withLog.length ? (restoreLog.length ? restoreLog : (await db.prepare(LOG_SELECT).all()).results) : []).map(r => [r.id, r]));
  for (const r of toHide) {
    statements.push(db.prepare('update mail_rejections set label_present = 0, updated_at = ? where gmail_id = ?').bind(at, r.gmail_id),
      ev(db, at, r.gmail_id, 'label_removed', ''));
    const last = lastEvent.get(r.gmail_id);
    if (!last || last.kind === 'log_reverted') continue;
    const id = JSON.parse(last.detail || '{}').id;
    const cur = rows.get(id);
    if (!cur || stillFed.has(id)) continue;                  // another labelled mail still rejects this application: leave it
    // The undo uses the event that first changed the row, even if this mail only linked to it later.
    const e = origin.get(id);
    if (!e) { statements.push(db.prepare('update mail_rejections set log_id = null where gmail_id = ?').bind(r.gmail_id)); continue; }
    const d = e.d;
    if (e.kind === 'log_linked' && d.before && d.after && cur.status === d.after.status && cur.note === d.after.note) {
      statements.push(db.prepare('update application_log set status = ?, date = ?, note = ?, source = ? where id = ?')
        .bind(d.before.status, d.before.date ?? '', d.before.note ?? '', d.before.source ?? '', d.id),
        ev(db, at, r.gmail_id, 'log_reverted', { id: d.id, restored: d.before }));
      Object.assign(cur, d.before);
      origin.delete(d.id);
    } else if (e.kind === 'log_appended' && cur.source === 'gmail-auto' && cur.status === 'rejected' && d.id === 'mail-' + e.gmail_id) {
      statements.push(db.prepare("delete from application_log where id = ? and source = 'gmail-auto'").bind(d.id),
        ev(db, at, r.gmail_id, 'log_reverted', { id: d.id, removed: cur }));
      rows.delete(d.id);
      origin.delete(d.id);
    }
    statements.push(db.prepare('update mail_rejections set log_id = null where gmail_id = ?').bind(r.gmail_id));
  }
  // A mail whose label came back: shown again, and (from 1 Sep 2026 on) its log step is planned again right here.
  const log = [...rows.values()].length ? [...rows.values()] : restoreLog;
  for (const r of toRestore) {
    statements.push(db.prepare('update mail_rejections set label_present = 1, updated_at = ? where gmail_id = ?').bind(at, r.gmail_id),
      ev(db, at, r.gmail_id, 'label_restored', ''));
    if (r.log_id || day(r.received_at) < LOG_SINCE) continue;
    const plan = planLog(db, log, r, at);
    statements.push(...plan.statements, db.prepare('update mail_rejections set log_id = ? where gmail_id = ?').bind(plan.logId, r.gmail_id));
    if (plan.effect) applyEffect(log, plan.effect);
  }
  if (statements.length) await db.batch(statements);
  return { hidden: toHide.length, restored: toRestore.length };
}
