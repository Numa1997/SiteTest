// Phyein Usul's Worker (see wrangler.jsonc and docs/usul.md). The site is static files (assets); this script serves the large
// stored simulation files that assets do not hold:
//   - /r2/<key> from the R2 bucket bound as RUNS, with HTTP byte ranges, limited to four key families:
//       1. resonant-tunnelling/YYYY-MM-DD/runs/<name>.bin
//       2. sims/<sim>/YYYY-MM-DD-v<N>/<file>
//       3. data/<folder>/<more path>  (fig12, fig16, schrodinger-sphere, resonant-tunnelling, sims)
//       4. simulations/fig13/dive/<file>
//   - /rel/<tag>/<file> from GitHub releases (legacy path kept while pages still read it).
// Pages check every downloaded file or part against SHA-256 hashes in the repository index, so the Worker needs no trust logic.

const SEG = /^[A-Za-z0-9_-][A-Za-z0-9_.-]*$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const SIM = /^[a-z0-9_]+$/;
const SIM_RUN = /^\d{4}-\d{2}-\d{2}-v\d+$/;
const DATA_FOLDERS = new Set(['fig12', 'fig16', 'schrodinger-sphere', 'resonant-tunnelling', 'sims']);
const SINGLE_RANGE = /^bytes=(\d*)-(\d*)$/;

// Large simulation data made by the Kaggle line (docs/kaggle-sims.md, "Large data", since 23 November 2026) lives as files of a GitHub
// release of this repository, sims-<sim>-<date>. /rel/<tag>/<file> fetches it from GitHub and passes a Range request through, so a page
// downloads only the part it needs; the page checks every part's SHA-256 against the index in the repository.
const REL = /^(sims-[a-z0-9_]+-\d{4}-\d\d-\d\d)\/([A-Za-z0-9_.\-]+\.pack)$/;

async function release(request, path) {
  if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('method not allowed', { status: 405 });
  const m = REL.exec(decodeURIComponent(path));
  if (!m) return new Response('not found', { status: 404 });
  const ask = new Headers(), range = request.headers.get('range');
  if (range) ask.set('range', range);
  // GitHub now and then answers a release download with an error although the file is there (seen 23 November 2026: about one request
  // in twenty came back as 404 here). So: up to three tries, and if all fail the reader gets 502 with GitHub's own status in the
  // header x-upstream-status, not a 404 that would read as "no such file".
  let r = null;
  for (let k = 0; k < 3; k++) {
    r = await fetch(`https://github.com/Numa1997/SiteTest/releases/download/${m[1]}/${m[2]}`, { headers: ask, redirect: 'follow' });
    if (r.status === 200 || r.status === 206) break;
    await new Promise((done) => setTimeout(done, 300 * (k + 1)));
  }
  if (r.status !== 200 && r.status !== 206) return new Response('the stored file could not be fetched', { status: 502, headers: { 'x-upstream-status': String(r.status), 'cache-control': 'no-store' } });
  const h = new Headers();
  for (const k of ['content-length', 'content-range', 'accept-ranges', 'etag']) if (r.headers.get(k)) h.set(k, r.headers.get(k));
  h.set('content-type', 'application/octet-stream');
  h.set('x-content-type-options', 'nosniff');
  h.set('cache-control', 'public, max-age=31536000, immutable');   // a release file never changes: a new generation gets a new tag
  return new Response(request.method === 'HEAD' ? null : r.body, { status: r.status, headers: h });
}

function noStoreError(body, status, extra = {}) {
  return new Response(body, { status, headers: { ...extra, 'cache-control': 'no-store' } });
}

// Validate a decoded R2 key against the four allowed families and path-safety limits.
function isAllowedKey(key) {
  if (!key || key.length > 512 || key.includes('..') || key.includes('\\') || key.includes('%')) return false;
  const parts = key.split('/');
  if (parts.length > 8) return false;
  for (const part of parts) {
    if (!SEG.test(part)) return false;
  }
  if (parts[0] === 'resonant-tunnelling') {
    return parts.length === 4 && DATE.test(parts[1]) && parts[2] === 'runs' && parts[3].endsWith('.bin');
  }
  if (parts[0] === 'sims') {
    return parts.length === 4 && SIM.test(parts[1]) && SIM_RUN.test(parts[2]);
  }
  if (parts[0] === 'data') {
    return parts.length >= 3 && DATA_FOLDERS.has(parts[1]);
  }
  if (parts[0] === 'simulations') {
    return parts.length === 4 && parts[1] === 'fig13' && parts[2] === 'dive';
  }
  return false;
}

// Parse a single HTTP byte range ("bytes=a-b", "bytes=a-", or "bytes=-n"). Anything else returns null so the caller ignores it.
function parseSingleRange(header) {
  if (!header) return null;
  const m = SINGLE_RANGE.exec(header.trim());
  if (!m) return null;
  const [, rawStart, rawEnd] = m;
  if (!rawStart && !rawEnd) return null;
  if (!rawStart) {
    const suffix = Number(rawEnd);
    return Number.isSafeInteger(suffix) ? { suffix } : null;
  }
  const start = Number(rawStart);
  if (!Number.isSafeInteger(start)) return null;
  if (!rawEnd) return { start, end: null };
  const end = Number(rawEnd);
  if (!Number.isSafeInteger(end) || end < start) return null;
  return { start, end };
}

function isRangeUnsatisfiable(parsed, size) {
  if (size <= 0) return true;
  if (parsed.suffix !== undefined) return parsed.suffix <= 0;
  return parsed.start >= size;
}

// Resolve R2's returned .range ({offset, length} or {suffix}) and .size into inclusive byte bounds and part length.
function resolveRange(r2Range, size) {
  if (!r2Range || size <= 0) return null;
  if (r2Range.suffix !== undefined) {
    if (r2Range.suffix <= 0) return null;
    const length = Math.min(r2Range.suffix, size);
    return { first: size - length, last: size - 1, length };
  }
  const first = r2Range.offset ?? 0;
  if (first < 0 || first >= size) return null;
  const maxLength = size - first;
  const length = r2Range.length !== undefined ? Math.min(r2Range.length, maxLength) : maxLength;
  if (length <= 0) return null;
  return { first, last: first + length - 1, length };
}

function objectHeaders(obj, length) {
  const h = new Headers();
  obj.writeHttpMetadata(h);
  h.set('etag', obj.httpEtag);
  h.set('content-type', 'application/octet-stream');
  h.set('x-content-type-options', 'nosniff');
  h.set('accept-ranges', 'bytes');
  h.set('cache-control', 'public, max-age=31536000, immutable'); // a key is never overwritten: a new run gets a new address
  h.set('content-length', String(length));
  return h;
}

async function serveR2(request, env, rawKey) {
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return noStoreError('method not allowed', 405, { allow: 'GET, HEAD' });
  }
  let key;
  try {
    key = decodeURIComponent(rawKey);
  } catch {
    return noStoreError('not found', 404);
  }
  if (!isAllowedKey(key)) return noStoreError('not found', 404);

  if (request.method === 'HEAD') {
    const obj = await env.RUNS.head(key);
    if (!obj) return noStoreError('not found', 404);
    return new Response(null, { status: 200, headers: objectHeaders(obj, obj.size) });
  }

  const parsedRange = parseSingleRange(request.headers.get('range'));
  if (!parsedRange) {
    const obj = await env.RUNS.get(key);
    if (!obj) return noStoreError('not found', 404);
    return new Response(obj.body, { status: 200, headers: objectHeaders(obj, obj.size) });
  }

  // Suffix length 0 is never satisfiable; check head() directly so we can report the true size in 416 (or 404 if missing).
  if (parsedRange.suffix === 0) {
    const head = await env.RUNS.head(key);
    if (!head) return noStoreError('not found', 404);
    return noStoreError('range not satisfiable', 416, { 'content-range': `bytes */${head.size}` });
  }

  let obj;
  try {
    obj = await env.RUNS.get(key, { range: request.headers });
  } catch (err) {
    // R2 throws when a byte range starts at or past the object's size; head() gives the size needed for the 416 header.
    const head = await env.RUNS.head(key);
    if (!head) return noStoreError('not found', 404);
    if (isRangeUnsatisfiable(parsedRange, head.size)) {
      return noStoreError('range not satisfiable', 416, { 'content-range': `bytes */${head.size}` });
    }
    throw err;
  }
  if (!obj) return noStoreError('not found', 404);

  if (isRangeUnsatisfiable(parsedRange, obj.size)) {
    await obj.body?.cancel();
    return noStoreError('range not satisfiable', 416, { 'content-range': `bytes */${obj.size}` });
  }

  const part = resolveRange(obj.range, obj.size);
  if (!part) {
    // R2 returned the full object without a sub-range (for example if a conditional header invalidated the range).
    return new Response(obj.body, { status: 200, headers: objectHeaders(obj, obj.size) });
  }

  const h = objectHeaders(obj, part.length);
  h.set('content-range', `bytes ${part.first}-${part.last}/${obj.size}`);
  return new Response(obj.body, { status: 206, headers: h });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/rel/')) return release(request, url.pathname.slice(5));
    // Read the raw path before URL normalization so any unencoded ".." segment is rejected instead of collapsed.
    const rawPath = request.url.replace(/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\/[^/?#]*/, '').split(/[?#]/)[0];
    if (rawPath.startsWith('/r2/')) return serveR2(request, env, rawPath.slice(4));
    if (url.pathname.startsWith('/r2/')) return serveR2(request, env, url.pathname.slice(4));
    return env.ASSETS.fetch(request);
  },
};
