/**
 * Absagen → stellen.phyeinusul.com : READ-ONLY sync (Google Apps Script, runs in Numa's own Google account).
 *
 * What it does: every 15 minutes it looks at incoming mail carrying the Gmail label "Absagen", asks the job-list
 * server which of those it does not have yet, and sends those, one mail per request: the headers, the mail's HTML,
 * the plain text, and the images the mail carries inside itself (src="cid:…"). The server cleans the HTML and
 * stores it; the page never contacts a sender.
 * The LABELLING itself is done by Gmail's own filters (gmail-filters.xml), not by this script.
 * Mail labelled "uncertain rejection" is NEVER sent anywhere: it is a review queue inside Gmail. Moving such a
 * mail to "Absagen" (one click) is what releases it to the job-list page.
 *
 * What it can NOT do: the manifest grants only gmail.readonly, so this code cannot send, delete, move or label
 * mail even if it tried. It talks to exactly one address, ENDPOINT. It does not download images from other
 * servers (no tracking pixels are triggered).
 *
 * Script properties (Project Settings → Script properties), typed in by Numa, never sent through a chat:
 *   ENDPOINT                https://stellen.phyeinusul.com/api/ingest
 *   CF_ACCESS_CLIENT_ID     the service token's Client ID   (Cloudflare Zero Trust)
 *   CF_ACCESS_CLIENT_SECRET the service token's Client Secret
 */

const LABEL = 'Absagen';
const BASE_Q = 'label:' + LABEL + ' -from:me -in:chats';   // never your own messages
const MAX_HTML = 120 * 1000;           // longer HTML is not sent (the server shows the text instead); same limit as the server
const MAX_IMG_BYTES = 300 * 1024;      // one inline image (server limit: 420,000 base64 characters)
const MAX_IMGS_BYTES = 600 * 1024;     // all inline images of one mail (server limit: 840,000 base64 characters)
const TIME_BUDGET_MS = 4 * 60 * 1000;  // Apps Script stops a run at 6 minutes; stop starting new mails after 4

function prop_(k) {
  const v = PropertiesService.getScriptProperties().getProperty(k);
  if (!v) throw new Error('Missing script property ' + k);
  return v;
}

/** POST JSON to the server through Cloudflare Access with the service token. Returns { code, data }. */
function call_(path, body) {
  const base = prop_('ENDPOINT').replace(/\/+$/, '');
  const res = UrlFetchApp.fetch(base + path, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'CF-Access-Client-Id': prop_('CF_ACCESS_CLIENT_ID'),
      'CF-Access-Client-Secret': prop_('CF_ACCESS_CLIENT_SECRET'),
    },
    payload: JSON.stringify(body),
    muteHttpExceptions: true,
    followRedirects: false,             // a redirect would mean Access refused us: fail loudly
  });
  const code = res.getResponseCode();
  let data = null;
  try { data = JSON.parse(res.getContentText()); } catch (e) { /* not JSON */ }
  return { code: code, data: data, text: res.getContentText().slice(0, 300) };
}

function must_(path, body) {
  const r = call_(path, body);
  if (r.code !== 200) throw new Error('Server answered ' + r.code + ' on ' + path + ': ' + r.text);
  return r.data;
}

/** Ids the server refused (a mail it will never accept); kept so one bad mail cannot stall the sync. */
function skipped_() {
  try { return JSON.parse(PropertiesService.getScriptProperties().getProperty('SKIPPED') || '[]'); } catch (e) { return []; }
}
function skip_(id, why) {
  const s = skipped_().filter(x => x.id !== id);
  s.push({ id: id, why: String(why).slice(0, 120), at: new Date().toISOString() });
  PropertiesService.getScriptProperties().setProperty('SKIPPED', JSON.stringify(s.slice(-300)));
  console.warn('Skipped ' + id + ': ' + why);
}

/** Counts failed runs per mail (kept across runs); returns the new count. */
function failures_(id) {
  const p = PropertiesService.getScriptProperties();
  let f = {}; try { f = JSON.parse(p.getProperty('FAILS') || '{}'); } catch (e) { f = {}; }
  f[id] = (f[id] || 0) + 1;
  const keys = Object.keys(f); if (keys.length > 200) keys.slice(0, keys.length - 200).forEach(k => delete f[k]);
  p.setProperty('FAILS', JSON.stringify(f));
  return f[id];
}
function clearFailures_(id) {
  const p = PropertiesService.getScriptProperties();
  let f = {}; try { f = JSON.parse(p.getProperty('FAILS') || '{}'); } catch (e) { return; }
  if (f[id]) { delete f[id]; p.setProperty('FAILS', JSON.stringify(f)); }
}

/** Gmail message ids matching a query, newest first, following page tokens. */
function listIds_(q, max) {
  const out = []; let pageToken;
  do {
    const r = Gmail.Users.Messages.list('me', { q: q, maxResults: 100, pageToken: pageToken });
    (r.messages || []).forEach(m => out.push(m.id));
    pageToken = r.nextPageToken;
  } while (pageToken && out.length < max);
  return out.slice(0, max);
}

function headerMap_(part) {
  const h = {}; (part.headers || []).forEach(x => h[x.name.toLowerCase()] = x.value);
  return h;
}

/** A text part in its own character set (e.g. ISO-8859-1), not blindly as UTF-8. */
function partText_(part) {
  const ct = headerMap_(part)['content-type'] || '';
  const cs = ((ct.match(/charset="?([^";\s]+)"?/i) || [])[1] || 'UTF-8').toUpperCase();
  const bytes = Utilities.base64DecodeWebSafe(part.body.data);
  try { return Utilities.newBlob(bytes).getDataAsString(cs); } catch (e) { return Utilities.newBlob(bytes).getDataAsString('UTF-8'); }
}

/** Walk the MIME tree: the HTML, the text, inline images by Content-ID, attachment names. */
function walk_(part, acc) {
  const mt = (part.mimeType || '').toLowerCase();
  const h = headerMap_(part);
  if (part.parts) { part.parts.forEach(p => walk_(p, acc)); return; }
  if (mt === 'text/html' && part.body && part.body.data && !acc.html) acc.html = partText_(part);
  else if (mt === 'text/plain' && part.body && part.body.data && !acc.text) acc.text = partText_(part);
  else if (/^image\/(png|jpe?g|gif|webp)$/.test(mt) && h['content-id']) {
    acc.inline.push({ cid: h['content-id'].replace(/[<>]/g, ''), mime: mt.replace('image/jpg', 'image/jpeg'), attachmentId: part.body && part.body.attachmentId, data: part.body && part.body.data });
  }
  if (part.filename && part.body && part.body.attachmentId && !h['content-id']) acc.attachments.push(part.filename);
}

/** One message → what the server stores. */
function record_(id) {
  const m = Gmail.Users.Messages.get('me', id, { format: 'full' });
  const h = headerMap_(m.payload);
  const acc = { html: '', text: '', inline: [], attachments: [] };
  walk_(m.payload, acc);
  const images = [];
  let used = 0;
  acc.inline.forEach(p => {
    try {
      const data = p.data || Gmail.Users.Messages.Attachments.get('me', id, p.attachmentId).data;
      const bytes = Utilities.base64DecodeWebSafe(data);
      if (bytes.length > MAX_IMG_BYTES || used + bytes.length > MAX_IMGS_BYTES) return;
      used += bytes.length;
      images.push({ cid: p.cid, mime: p.mime, b64: Utilities.base64Encode(bytes) });
    } catch (e) { /* an unreadable image is left out; the page shows the mail without it */ }
  });
  return {
    gmail_id: m.id, thread_id: m.threadId, received_at: new Date(Number(m.internalDate)).toISOString(),
    from: h['from'] || '', to: (h['to'] || '').slice(0, 2000), cc: (h['cc'] || '').slice(0, 2000),
    subject: (h['subject'] || '').slice(0, 1000), date_header: (h['date'] || '').slice(0, 200), labels: [LABEL],
    snippet: (m.snippet || '').slice(0, 500), text: (acc.text || '').slice(0, 300000),
    html: acc.html && acc.html.length <= MAX_HTML ? acc.html : '', attachments: acc.attachments.slice(0, 50), images: images,
  };
}

function push_(ids, deadline) {
  const skip = new Set(skipped_().map(x => x.id));
  const missing = (must_('/known', { gmail_ids: ids }).missing || []).filter(id => !skip.has(id));
  let sent = 0, refused = 0, light = 0;
  for (let i = 0; i < missing.length && Date.now() < deadline; i++) {
    let rec;
    try { rec = record_(missing[i]); } catch (e) { skip_(missing[i], 'read failed: ' + e); refused++; continue; }
    let r = call_('/rejections', { messages: [rec] });
    if (r.code >= 300 && r.code < 400) throw new Error('Redirected (' + r.code + '): Cloudflare Access did not accept the service token');
    if (r.code >= 500 || r.code === 413) {
      // The server failed on this mail. A passing hiccup heals on the next run; after 3 failed runs it is sent as text only.
      if (failures_(missing[i]) < 3) { console.warn('Server ' + r.code + ' on ' + missing[i] + '; will retry next run'); continue; }
      r = call_('/rejections', { messages: [Object.assign({}, rec, { html: '', images: [] })] });
      if (r.code === 200) light++;
    }
    const res = r.data && r.data.results && r.data.results[0];
    if (r.code === 200 && res && res.status !== 'refused') { sent++; clearFailures_(missing[i]); continue; }
    if (r.code === 401 || r.code === 403 || r.code === 429 || r.code === 503 || r.code >= 500) throw new Error('Server answered ' + r.code + ': ' + r.text);  // sign-in, setup or server trouble: stop, retry next run
    skip_(missing[i], r.code + ' ' + (res ? JSON.stringify(res) : r.text));   // the server refused this mail for good: listed, the others go on
    refused++;
  }
  return { checked: ids.length, missing: missing.length, sent: sent, text_only: light, refused: refused };
}

function locked_(fn) {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) { console.log('Another run is busy; skipping this one.'); return; }
  try { fn(); } finally { lock.releaseLock(); }
}

/** Every 15 minutes (installed by install()). */
function syncRecent() {
  locked_(() => {
    const deadline = Date.now() + TIME_BUDGET_MS;
    console.log(JSON.stringify(push_(listIds_(BASE_Q + ' newer_than:7d', 200), deadline)));
  });
}

/** One-time history, oldest first: run by hand, then install() keeps it going hourly until done. Resumable. */
function backfill() {
  locked_(() => {
    const deadline = Date.now() + TIME_BUDGET_MS;
    const r = push_(listIds_(BASE_Q, 5000).reverse(), deadline);
    console.log(JSON.stringify(r));
    if (r.sent + r.refused === r.missing) {
      PropertiesService.getScriptProperties().setProperty('BACKFILL_DONE', new Date().toISOString());
      ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'backfill').forEach(t => ScriptApp.deleteTrigger(t));
    }
  });
}

/** Weekly: the server learns which mails still carry the label; mails that lost it are hidden and their log change undone. */
function reconcile() {
  locked_(() => console.log(JSON.stringify(must_('/present', { gmail_ids: listIds_(BASE_Q, 5000) }))));
}

/** By hand only, after you deliberately removed the label from many mails at once (the weekly run refuses to hide more than a quarter). */
function reconcileForce() {
  locked_(() => console.log(JSON.stringify(must_('/present', { gmail_ids: listIds_(BASE_Q, 5000), force: true }))));
}

/** Run once by hand: creates the triggers (idempotent). */
function install() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('syncRecent').timeBased().everyMinutes(15).create();
  ScriptApp.newTrigger('reconcile').timeBased().everyWeeks(1).onWeekDay(ScriptApp.WeekDay.SUNDAY).atHour(6).create();
  if (!PropertiesService.getScriptProperties().getProperty('BACKFILL_DONE')) ScriptApp.newTrigger('backfill').timeBased().everyHours(1).create();
}

/** Off switch: removes all triggers. */
function uninstall() { ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t)); }

/** Shows which mails the server refused, and why (View → Logs). */
function showSkipped() { console.log(JSON.stringify(skipped_(), null, 1)); }
