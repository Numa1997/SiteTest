// The server of Stellenrecherche (Numa's job search record), a Cloudflare Worker.
// Static files in public/ are served by Cloudflare directly; only /api/*
// reaches this code (wrangler.jsonc: assets.run_worker_first). Every route
// needs the owner (src/access.js). The data lives in D1 (schema.sql).
//
//   GET    /api/dossier          the list, the rules, the e-mail log, the catalogue, the added postings
//   GET    /api/marks            what Numa did with each card
//   PUT    /api/marks/:item      change one mark (fields in src/validate.js)
//   DELETE /api/marks/:item      forget one mark
//   POST   /api/added            add a posting by hand
//   DELETE /api/added/:item      delete a hand-added posting
//   GET    /api/me               the signed-in e-mail
//   POST   /api/ingest/known|rejections|present   the Gmail script only (service token; src/mail.js)
//   GET    /absagen, /absagen/part, /absagen/img/:id/:n   the rejection e-mails as a page you can print (src/absagen.js)
import { requireOwner, requireService } from './access.js';
import { ingest, known, present, MAX_INGEST_BODY } from './mail.js';
import { renderShell, renderPart, renderImage } from './absagen.js';
import { ApiError, validItem, validAddedId, validPatch, cleanPosting, MARK_FIELDS } from './validate.js';
import { CATEGORIES, BOARDS, AREAS } from './catalog.js';

const MAX_BODY = 64 * 1024;
const MAX_ROWS = 5000;

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
  },
});

async function body(request, max = MAX_BODY) {
  if (!/^application\/json\b/i.test(request.headers.get('Content-Type') ?? '')) throw new ApiError(415, 'json_required');
  const declared = Number(request.headers.get('Content-Length') ?? 0);
  if (declared > max) throw new ApiError(413, 'too_large');
  const text = await request.text();
  if (text.length > max) throw new ApiError(413, 'too_large');
  try { return JSON.parse(text); } catch { throw new ApiError(400, 'bad_json'); }
}

// A change must come from this site's own page: a browser always sends
// Origin on PUT, POST and DELETE, and another site cannot fake it.
function sameOrigin(request) {
  const origin = request.headers.get('Origin');
  if (origin && origin !== new URL(request.url).origin) throw new ApiError(403, 'forbidden_origin');
}

// ---- rows <-> objects -------------------------------------------------------

function markOut(row) {
  const mark = { item_id: row.item_id };
  for (const k of MARK_FIELDS) {
    if (row[k] === null || row[k] === undefined) { if (k === 'outcome') mark.outcome = null; continue; }
    if (k === 'snapshot') mark.snapshot = JSON.parse(row.snapshot);
    else if (k === 'removed') mark.removed = row.removed === 1;
    else mark[k] = row[k];
  }
  mark.updated_at = row.updated_at;
  return mark;
}

function markIn(mark) {
  return [
    mark.item_id,
    mark.outcome ?? null, mark.outcome_at ?? null,
    mark.stage ?? null, mark.stage_at ?? null,
    mark.round ?? null,
    mark.removed === undefined || mark.removed === null ? null : (mark.removed ? 1 : 0),
    mark.note ?? null,
    mark.snapshot === undefined || mark.snapshot === null ? null : JSON.stringify(mark.snapshot),
    mark.updated_at,
  ];
}

const UPSERT_MARK = `insert into marks (item_id, outcome, outcome_at, stage, stage_at, round, removed, note, snapshot, updated_at)
  values (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)
  on conflict(item_id) do update set outcome = ?2, outcome_at = ?3, stage = ?4, stage_at = ?5, round = ?6,
    removed = ?7, note = ?8, snapshot = ?9, updated_at = ?10`;

// ---- routes -----------------------------------------------------------------

async function dossier(db) {
  const [postings, meta, log, added] = await db.batch([
    db.prepare(`select n, title, title_original, company, city, location_group, category, employment, url,
      eligibility_quote_de, eligibility_en, salary, note, note_de, added_on, removed_on, removed_why
      from postings order by n desc`),
    db.prepare('select key, value from meta'),
    db.prepare('select id, cards, company, title, status, date, note, source from application_log'),
    db.prepare('select item_id, url, title, company, city, area, category, added_at from added order by added_at desc'),
  ]);
  return {
    postings: postings.results,
    meta: Object.fromEntries(meta.results.map(r => [r.key, JSON.parse(r.value)])),
    applicationLog: log.results.map(r => ({ ...r, cards: JSON.parse(r.cards) })),
    added: added.results,
    categories: CATEGORIES,
    boards: BOARDS,
    areas: AREAS,
  };
}

async function putMark(db, itemId, patch) {
  if (!validItem(itemId) || !validPatch(patch)) throw new ApiError(400, 'invalid_mark');
  const row = await db.prepare('select * from marks where item_id = ?').bind(itemId).first();
  if (!row) {
    const { n } = await db.prepare('select count(*) as n from marks').first();
    if (n >= MAX_ROWS) throw new ApiError(400, 'capacity');
  }
  const mark = { ...(row ? markOut(row) : { item_id: itemId }), ...patch, updated_at: new Date().toISOString() };
  await db.prepare(UPSERT_MARK).bind(...markIn(mark)).run();
  return markOut(await db.prepare('select * from marks where item_id = ?').bind(itemId).first());
}

async function addPosting(db, input) {
  const posting = cleanPosting(input);
  const { n } = await db.prepare('select count(*) as n from added').first();
  if (n >= MAX_ROWS) throw new ApiError(400, 'capacity');
  const at = new Date();
  // The id is the time in milliseconds; if two land in the same millisecond, the next free one.
  let stamp = at.getTime();
  while (await db.prepare('select 1 from added where item_id = ?').bind('a' + stamp).first()) stamp++;
  const record = { item_id: 'a' + stamp, ...posting, company: posting.company ?? '', added_at: at.toISOString() };
  await db.prepare(`insert into added (item_id, url, title, company, city, area, category, added_at)
    values (?, ?, ?, ?, ?, ?, ?, ?)`)
    .bind(record.item_id, record.url, record.title, record.company, record.city, record.area, record.category, record.added_at).run();
  return record;
}

async function api(request, env) {
  const url = new URL(request.url);
  const method = request.method;
  const path = url.pathname.replace(/\/+$/, '');
  if (method !== 'GET' && method !== 'HEAD') sameOrigin(request);
  // The Gmail script's routes: its service token only, never a browser session.
  if (path.startsWith('/api/ingest/')) {
    if (method !== 'POST') throw new ApiError(405, 'method_not_allowed');
    await requireService(request, env);
    const input = await body(request, MAX_INGEST_BODY);
    if (path === '/api/ingest/known') return json(await known(env.DB, input));
    if (path === '/api/ingest/rejections') return json(await ingest(env.DB, input));
    if (path === '/api/ingest/present') return json(await present(env.DB, input));
    throw new ApiError(404, 'not_found');
  }
  const email = await requireOwner(request, env);
  const db = env.DB;
  const tail = (prefix) => (path.startsWith(prefix + '/') ? decodeURIComponent(path.slice(prefix.length + 1)) : null);

  if (method === 'GET' && path === '/api/me') return json({ email });
  if (method === 'GET' && path === '/api/dossier') return json(await dossier(db));
  if (method === 'GET' && path === '/api/marks') {
    const { results } = await db.prepare('select * from marks').all();
    return json({ marks: results.map(markOut) });
  }
  const markId = tail('/api/marks');
  if (method === 'PUT' && markId !== null) return json({ mark: await putMark(db, markId, await body(request)) });
  if (method === 'DELETE' && markId !== null) {
    if (!validItem(markId)) throw new ApiError(400, 'invalid_item');
    await db.prepare('delete from marks where item_id = ?').bind(markId).run();
    return json({ ok: true });
  }
  if (method === 'POST' && path === '/api/added') return json({ posting: await addPosting(db, await body(request)) });
  const addedId = tail('/api/added');
  if (method === 'DELETE' && addedId !== null) {
    if (!validAddedId(addedId)) throw new ApiError(400, 'invalid_item');
    await db.prepare('delete from added where item_id = ?').bind(addedId).run();
    return json({ ok: true });
  }
  throw new ApiError(404, 'not_found');
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/absagen' || url.pathname.startsWith('/absagen/')) {
      const plain = (status, text) => new Response(text, { status, headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' } });
      if (request.method !== 'GET' && request.method !== 'HEAD') return plain(405, 'Method not allowed');
      try {
        await requireOwner(request, env);
        const p = url.pathname.replace(/\/+$/, '');
        if (p === '/absagen') return await renderShell(env.DB, url);
        if (p === '/absagen/part') return await renderPart(env.DB, url);
        const img = /^\/absagen\/img\/([0-9a-f]{8,32})\/(\d{1,2})$/.exec(p);
        if (img) return await renderImage(env.DB, img[1], Number(img[2]));
        return plain(404, 'Not found');
      } catch (error) {
        if (error instanceof ApiError) return plain(error.status, error.status === 503 ? 'Not configured.' : 'No access.');
        console.error('absagen', error);
        return plain(500, 'Server error.');
      }
    }
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(request);
    try {
      return await api(request, env);
    } catch (error) {
      if (error instanceof ApiError) return json({ error: error.code, ...error.extra }, error.status);
      console.error('api error', error);
      return json({ error: 'server' }, 500);
    }
  },
};
