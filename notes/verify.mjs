// Lead's check of the ten simulation pages after the note repairs.
// For each page at 1440 × 900 and 390 × 844: console and page errors, KaTeX errors, sideways scroll, every fold of the
// note opening, numbered equations present, and (at desktop width) display equations wider than their box, whose number
// would then sit outside the visible part.
// Usage: APPDEPLOY_VITE_OUT_DIR=/tmp/lead-dist npm run build && node notes/verify.mjs /tmp/lead-dist [fig numbers…]
import { createRequire } from 'module';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const [dist, ...only] = process.argv.slice(2);
const PAGES = [
  [1, 'Circular Wave Interference Visualization.html'], [2, 'Double Pendulum.html'],
  [3, 'Interactive Double-Slit Experiment Visualization.html'], [4, 'Transverse and longitudinal waves.html'],
  [5, 'water-wave.html'], [6, 'wave-interference.html'], [7, 'phasor-sums.html'], [8, 'draw-decompose.html'],
  [9, 'driven-oscillator.html'], [10, 'wind-turbine.html']].filter(([n]) => !only.length || only.includes(String(n)));
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((q, r) => {
  const p = path.join(dist, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); });
}).listen(0);
const port = server.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
let bad = 0;
for (const [fig, file] of PAGES) {
  for (const [vw, vh, tag] of [[1440, 900, 'desk'], [390, 844, 'phone']]) {
    const page = await browser.newPage({ viewport: { width: vw, height: vh } });
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => errs.push(String(e)));
    await page.goto(`http://localhost:${port}/simulations/${encodeURIComponent(file)}`, { waitUntil: 'load' });
    await page.waitForFunction(() => document.querySelector('.paper.is-typeset'), null, { timeout: 15000 }).catch(() => errs.push('note never typeset'));
    await page.waitForTimeout(600);
    await page.evaluate(() => { const b = [...document.querySelectorAll('.fold-tool')].find(x => /expand/i.test(x.textContent)); if (b) b.click(); });
    await page.waitForTimeout(500);
    const r = await page.evaluate((desk) => {
      const p = document.querySelector('#paper');
      const tags = [...p.querySelectorAll('.katex-display .tag')].map(t => t.textContent.trim());
      const wide = desk ? [...p.querySelectorAll('.katex-display')].filter(d => d.scrollWidth > d.clientWidth + 1)
        .map(d => (d.querySelector('.tag') || { textContent: '(untagged)' }).textContent.trim() + ` ${d.scrollWidth}/${d.clientWidth}px`) : [];
      const closed = [...p.querySelectorAll('.fsec')].filter(s => !s.classList.contains('is-open') && s.getAttribute('aria-expanded') !== 'true' && s.querySelector('.fold') && getComputedStyle(s.querySelector('.fold')).gridTemplateRows === '0px').length;
      return {
        katexErr: document.querySelectorAll('.katex-error').length,
        sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        tags, wide, closed, refs: p.querySelectorAll('.prefs li').length, refLinks: p.querySelectorAll('.prefs li a[href]').length
      };
    }, tag === 'desk');
    const ok = !errs.length && !r.katexErr && r.sideways <= 0 && !r.wide.length && !r.closed;
    if (!ok) bad++;
    console.log(`Fig ${fig} ${tag}: ${ok ? 'ok' : 'PROBLEM'} · errors ${errs.length}${errs.length ? ' ' + errs.slice(0, 2).join(' | ') : ''} · katexErr ${r.katexErr} · sideways ${r.sideways}px · closed folds ${r.closed} · eqs ${r.tags.length} (${r.tags[0] || ''}…${r.tags[r.tags.length - 1] || ''}) · refs ${r.refs}, linked ${r.refLinks}${r.wide.length ? ' · WIDE: ' + r.wide.join(', ') : ''}`);
    await page.close();
  }
}
await browser.close(); server.close();
process.exit(bad ? 1 : 0);
