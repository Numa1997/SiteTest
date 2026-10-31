// Every page at every address a reader can use, and every link of every page, on a running site (docs/performance.md, change 6).
// node tools/perf/addresses.cjs <base URL> <built folder> [out.json]      e.g. node tools/perf/addresses.cjs https://phyeinusul.com dist
// 1. Each page of <built folder> is asked for at its .html address (the one every link uses) and at the short forms readers have
//    seen since 20 October 2026: x, x/, and for a folder's index.html folder/ and folder. Each answer is followed hop by hop (curl)
//    and must end in 200 with the bytes of that very page (SHA-256) and the security policy header.
// 2. Each page is opened in Chromium: no request of the site may fail and no script may report an error (Cloudflare's analytics
//    beacon, which the security policy blocks, is left out); every link the finished page holds must end in 200.
// Exits 1 on any failure. The address the page sees (location.pathname) is printed for the first pages, for the stored-fold keys.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), crypto = require('crypto');
const { execFileSync } = require('child_process');
const [base, dist, out] = process.argv.slice(2);
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const pages = []; (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f.endsWith('.html')) pages.push('/' + path.relative(dist, p).split(path.sep).join('/')); } })(dist);
const byHash = {}; for (const p of pages) byHash[sha(fs.readFileSync(path.join(dist, p)))] = p;
const tmp = path.join(require('os').tmpdir(), 'addresses-body');
function get(u) { // one request, no redirect following: status, Location, the security policy header, the body's page
  // the last header block is the site's answer (a proxy on the way prints its own "200 Connection established" block first)
  const blocks = execFileSync('curl', ['-s', '-o', tmp, '-D', '-', '--max-time', '30', u]).toString().split(/\r?\n\r?\n/).filter(b => /^HTTP\//.test(b));
  const h = blocks[blocks.length - 1] || '';
  const status = +(/^HTTP\/[\d.]+ (\d+)/.exec(h) || [])[1] || 0, loc = (/^location: *(.+?)\r?$/mi.exec(h) || [])[1];
  return { status, loc, csp: /^content-security-policy:/mi.test(h), page: status === 200 ? byHash[sha(fs.readFileSync(tmp))] || '(other bytes)' : null };
}
function follow(u) { const hops = []; for (let i = 0; i < 6; i++) { const r = get(u); hops.push(r.status); if (r.status >= 300 && r.status < 400 && r.loc) { u = new URL(r.loc, u).href; continue; } return { ...r, hops, final: u.slice(base.length) }; } return { status: 'loop', hops }; }
const forms = p => { if (p === '/index.html') return [p, '/']; if (p.endsWith('/index.html')) { const f = p.slice(0, -10); return [p, f, f.slice(0, -1)]; } const s = p.slice(0, -5); return [p, s, s + '/']; };
(async () => {
  const res = { addresses: [], pages: [], links: {} }; let bad = 0;
  for (const p of pages) for (const a of forms(p)) { const r = follow(base + encodeURI(a)); const ok = r.status === 200 && r.page === p && r.csp; if (!ok) bad++; res.addresses.push({ page: p, asked: a, ok, ...r }); }
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); const links = new Set();
  for (const p of pages) {
    const pg = await ctx.newPage(); const failed = [], errs = [];
    pg.on('response', r => { if (r.url().startsWith(base) && r.status() >= 400) failed.push(r.status() + ' ' + r.url().slice(base.length)); });
    pg.on('requestfailed', r => { if (r.url().startsWith(base)) failed.push('failed ' + r.url().slice(base.length)); });
    pg.on('console', m => { if (m.type() === 'error' && !/cloudflareinsights/.test(m.text())) errs.push(m.text().slice(0, 140)); });
    pg.on('pageerror', e => errs.push('pageerror ' + String(e).slice(0, 140)));
    await pg.goto(base + encodeURI(p), { waitUntil: 'load', timeout: 90000 }).catch(e => errs.push('goto ' + e.message.slice(0, 80)));
    await pg.waitForTimeout(1200);
    const seen = await pg.evaluate(() => ({ path: location.pathname, links: [...document.querySelectorAll('a[href], iframe[src]')].map(a => a.href && a.href.baseVal !== undefined ? new URL(a.href.baseVal, location.href).href : String(a.href || a.src)) })).catch(() => ({ path: '?', links: [] }));
    for (const l of seen.links) if (l.startsWith(base)) links.add(l.split('#')[0]);
    if (failed.length || errs.length) bad++;
    res.pages.push({ page: p, path: decodeURIComponent(seen.path), failed: [...new Set(failed)], errs: [...new Set(errs)] }); await pg.close();
  }
  await b.close();
  for (const l of links) { const r = follow(l); res.links[l.slice(base.length)] = r; if (r.status !== 200) bad++; }
  if (out) fs.writeFileSync(out, JSON.stringify(res, null, 1));
  const A = res.addresses, L = Object.values(res.links);
  console.log(`${pages.length} pages · addresses: ${A.filter(a => a.ok).length} of ${A.length} right (asked at .html: ${A.filter(a => a.asked.endsWith('.html')).map(a => a.hops.length - 1).reduce((x, y) => x + y, 0)} redirects in all) · pages with a failed request or error: ${res.pages.filter(p => p.failed.length || p.errs.length).length} · links: ${L.length}, ${L.filter(r => r.status === 200).length} reach 200, ${L.filter(r => r.hops.length > 1).length} through a redirect`);
  for (const a of A.filter(a => !a.ok)) console.log(`  WRONG  ${a.asked} -> ${a.hops.join(' > ')} ${a.final || ''} ${a.page || ''}${a.csp === false && a.status === 200 ? ' (no security policy header)' : ''}`);
  for (const p of res.pages.filter(p => p.failed.length || p.errs.length)) console.log(`  PAGE   ${p.page} ${JSON.stringify(p.failed.slice(0, 3))} ${JSON.stringify(p.errs.slice(0, 2))}`);
  for (const [l, r] of Object.entries(res.links).filter(([, r]) => r.status !== 200)) console.log(`  LINK   ${l} -> ${r.hops.join(' > ')}`);
  console.log('  the address pages see: ' + res.pages.slice(0, 3).map(p => p.path).join(', ') + ' …');
  process.exit(bad ? 1 : 0);
})();
