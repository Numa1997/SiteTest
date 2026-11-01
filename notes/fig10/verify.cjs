// Fig. 10, after the note edits: console errors, KaTeX errors, sideways scroll, folds, screenshots of the edited sections.
// Build first:  cd /home/user/SiteTest && OUT_DIR=/tmp/fig10-dist npm run build
// Run:          node notes/fig10/verify.cjs   (screenshots go to the folder given as the first argument, default /tmp/fig10-shots)
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = '/tmp/fig10-dist', PORT = 8711, SHOTS = process.argv[2] || '/tmp/fig10-shots';
fs.mkdirSync(SHOTS, { recursive: true });
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp' };
const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (err, data) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(data); });
});
(async () => {
    await new Promise(r => server.listen(PORT, r));
    const browser = await chromium.launch();
    const out = {};
    for (const [w, h] of [[1440, 900], [390, 844]]) {
        const page = await browser.newPage({ viewport: { width: w, height: h } });
        const errors = [];
        page.on('pageerror', e => errors.push(String(e)));
        page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
        page.on('requestfailed', r => errors.push('request failed: ' + r.url()));
        await page.goto('http://127.0.0.1:' + PORT + '/simulations/wind-turbine.html', { waitUntil: 'networkidle' });
        await page.waitForFunction(() => document.querySelectorAll('.paper .katex').length > 50 && window.Sim && Sim.data && Sim.data.ds.get('Eg_end') > 0);
        await page.waitForTimeout(500);
        const r = await page.evaluate(() => {
            const de = document.documentElement;
            const toggles = Array.from(document.querySelectorAll('.paper .fs-toggle, #walk .fs-toggle'));
            return {
                katex: document.querySelectorAll('.paper .katex').length,
                katexErrors: document.querySelectorAll('.katex-error').length,
                rawDelims: (document.querySelector('.paper').innerText.match(/\\\(|\\\[/g) || []).length,
                scrollW: de.scrollWidth, clientW: de.clientWidth, bodyScrollW: document.body.scrollWidth,
                widest: Array.from(document.querySelectorAll('.paper *')).filter(e => e.getBoundingClientRect().right > de.clientWidth + 0.5).map(e => e.tagName + '.' + e.className).slice(0, 5),
                toggles: toggles.length,
                tags: Array.from(document.querySelectorAll('.paper .katex-display .tag')).map(t => t.textContent.trim())
            };
        });
        // folds: collapse everything, then open each toggle in turn and check it is open and has height
        const folds = await page.evaluate(async () => {
            const sleep = ms => new Promise(r => setTimeout(r, ms));
            const all = Array.from(document.querySelectorAll('[data-fold-level]'));
            const res = { n: all.length, opened: 0, failed: [] };
            for (const node of all) {
                const btn = node.querySelector(':scope > .fs-head .fs-toggle');
                if (!btn) { res.failed.push('no toggle: ' + (node.id || node.className)); continue; }
                if (btn.getAttribute('aria-expanded') === 'true') { btn.click(); await sleep(30); }
                if (btn.getAttribute('aria-expanded') !== 'false') res.failed.push('did not close: ' + btn.getAttribute('data-label'));
                btn.click(); await sleep(400);
                const f = node.querySelector(':scope > .fold');
                const ok = btn.getAttribute('aria-expanded') === 'true' && f && f.getAttribute('data-open') === '1' && f.getBoundingClientRect().height > 0;
                if (ok) res.opened++; else res.failed.push('did not open: ' + btn.getAttribute('data-label'));
            }
            return res;
        });
        r.folds = folds;
        // screenshots of the edited sections
        for (const id of ['p-wind', 'p-betz', 'p-tsr', 'p-control', 'p-compare', 'p-solve', 'p-screen', 'p-limits']) {
            const el = await page.$('#' + id);
            if (el) await el.screenshot({ path: path.join(SHOTS, w + '-' + id + '.png') });
        }
        r.errors = errors;
        out[w + 'x' + h] = r;
        await page.close();
    }
    console.log(JSON.stringify(out, null, 1));
    await browser.close(); server.close();
})().catch(e => { console.error(e); process.exit(1); });
