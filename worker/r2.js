// Phyein Usul's Worker (see wrangler.jsonc and docs/usul.md). The site is static files (assets); this script only answers what
// the assets do not hold: the large stored simulation runs, kept in the R2 bucket bound as RUNS and served under /r2/<key>.
// Fig. 15 (resonant tunnelling, generation 2) is the first user: about 3700 run files, several GB, too large for the repository.
// The page checks every file's SHA-256 against its index in the repository, so the bucket needs no trust of its own.
const KEY = /^resonant-tunnelling\/\d{4}-\d\d-\d\d\/runs\/[A-Za-z0-9_.\-]+\.bin$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/r2/')) {
      if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('method not allowed', { status: 405 });
      const key = decodeURIComponent(url.pathname.slice(4));
      if (!KEY.test(key)) return new Response('not found', { status: 404 });
      const obj = await env.RUNS.get(key);
      if (!obj) return new Response('not found', { status: 404 });
      const h = new Headers();
      obj.writeHttpMetadata(h);
      h.set('etag', obj.httpEtag);
      h.set('content-type', 'application/octet-stream');
      h.set('x-content-type-options', 'nosniff');
      h.set('cache-control', 'public, max-age=31536000, immutable');   // a run file never changes: a new run gets a new name
      return new Response(request.method === 'HEAD' ? null : obj.body, { headers: h });
    }
    return env.ASSETS.fetch(request);
  },
};
