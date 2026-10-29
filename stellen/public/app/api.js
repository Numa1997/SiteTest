// Every request the page makes, in one place. Same-origin fetch: the browser
// sends the Cloudflare Access cookie by itself, so the page holds no token.
// Replaces Physik Radar's AppDeploy client (transport.js, marks-repo.js, added-repo.js).

export class ApiFailure extends Error {
  constructor(status, data) { super(data?.error ?? 'http_' + status); this.status = status; this.data = data ?? {}; }
}

async function call(method, path, payload) {
  let res;
  try {
    res = await fetch(path, {
      method,
      credentials: 'same-origin',
      redirect: 'manual',   // an expired Access session answers with a redirect to the sign-in page
      headers: payload === undefined ? { Accept: 'application/json' } : { Accept: 'application/json', 'Content-Type': 'application/json' },
      body: payload === undefined ? undefined : JSON.stringify(payload),
    });
  } catch {
    throw new ApiFailure(0, { error: 'network' });
  }
  if (res.type === 'opaqueredirect' || (res.status >= 300 && res.status < 400)) throw new ApiFailure(401, { error: 'session_expired' });
  let data = null;
  try { data = await res.json(); } catch { data = null; }
  if (!res.ok) throw new ApiFailure(res.status, data);
  if (data === null) throw new ApiFailure(res.status, { error: 'session_expired' });  // an HTML sign-in page instead of JSON
  return data;
}

let cached, pending;
/** The list, rules, e-mail log, catalogue and hand-added postings. Reused for 3 s. */
export function readDossier(force = false) {
  if (!force && cached && Date.now() - cached.at < 3000) return Promise.resolve(cached.data);
  if (pending) return pending;
  pending = call('GET', '/api/dossier').then(data => { cached = { at: Date.now(), data }; return data; })
    .finally(() => { pending = null; });
  return pending;
}

export async function loadMarks() {
  const { marks } = await call('GET', '/api/marks');
  return new Map(marks.map(m => [m.item_id, m]));
}

// Saves for the same card go out one at a time. The server replaces a
// card's whole record on each save, so two saves to one card in flight at
// once could let the second erase the first; queued, each one starts from
// the result of the one before. Different cards still save in parallel.
const queues = new Map();
function oneAtATime(key, task) {
  const next = (queues.get(key) || Promise.resolve()).catch(() => {}).then(task);
  queues.set(key, next);
  const cleanup = () => { if (queues.get(key) === next) queues.delete(key); };
  next.then(cleanup, cleanup);
  return next;
}

export const saveMark = (itemId, patch) =>
  oneAtATime(itemId, async () => (await call('PUT', '/api/marks/' + encodeURIComponent(itemId), patch)).mark);

export const addPosting = async input => (await call('POST', '/api/added', input)).posting;
export const deleteAdded = itemId => call('DELETE', '/api/added/' + encodeURIComponent(itemId));

/** Re-reads the list every minute while the tab is visible, and on return to the tab. */
export function watchData(onUpdate) {
  let stopped = false, busy = false, signature = '';
  async function tick() {
    if (stopped || busy || document.hidden) return;
    busy = true;
    try {
      const next = await readDossier(true);
      const s = JSON.stringify(next);
      if (s !== signature) { signature = s; onUpdate(next); }
    } catch { /* keep the last good view during a short outage */ }
    finally { busy = false; }
  }
  const visible = () => { if (!document.hidden) tick(); };
  document.addEventListener('visibilitychange', visible);
  const interval = setInterval(tick, 60000);
  return () => { stopped = true; clearInterval(interval); document.removeEventListener('visibilitychange', visible); };
}

/** Cloudflare Access ends the session here. */
export const SIGN_OUT_URL = '/cdn-cgi/access/logout';
