// Fig. 8 after the edits: at 1440 x 900 and 390 x 844, console errors, .katex-error, sideways scroll, every fold opens;
// screenshots of the edited paragraphs. Run: node notes/fig08/verify.cjs [/tmp/fig08-dist]
'use strict';
const http = require('http'), fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = process.argv[2] || '/tmp/fig08-dist';
const SHOTS = process.env.SHOTS || '/tmp/fig08-shots';
fs.mkdirSync(SHOTS, { recursive: true });
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.webp': 'image/webp' };
const server = http.createServer((req, res) => { const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(d); }); });
(async () => {
    await new Promise(r => server.listen(0, r));
    const url = 'http://127.0.0.1:' + server.address().port + '/simulations/draw-decompose.html';
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
    const out = {};
    for (const [w, h] of [[1440, 900], [390, 844]]) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h } });
        const page = await ctx.newPage();
        const errors = [], failed = [];
        page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
        page.on('pageerror', e => errors.push(String(e)));
        page.on('requestfailed', r => failed.push(r.url()));
        await page.goto(url, { waitUntil: 'load' });
        await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds && Sim.data.ds.dims.k === 120);
        await page.waitForTimeout(1200);
        // every fold: close it, then open it again, and check it is open with a body of nonzero height
        const nFolds = await page.evaluate(() => document.querySelectorAll('[data-fold-level]').length);
        const folds = [];
        for (let i = 0; i < nFolds; i++) {
            const r = await page.evaluate(async (i) => {
                const node = document.querySelectorAll('[data-fold-level]')[i];
                const btn = node.querySelector(':scope > .fs-head .fs-toggle');
                const wait = ms => new Promise(r => setTimeout(r, ms));
                const label = (node.querySelector(':scope > .fs-head') || node).textContent.trim().slice(0, 40);
                if (!btn) return { i, label, ok: false, why: 'no toggle' };
                btn.click(); await wait(450);
                const closed = node.getAttribute('data-collapsed') === '1';
                btn.click(); await wait(500);
                const fold = node.querySelector(':scope > .fold');
                const open = node.getAttribute('data-collapsed') === '0' && fold.getAttribute('data-open') === '1' && !fold.hasAttribute('inert');
                const hgt = fold.getBoundingClientRect().height;
                return { i, label, closed, open, height: Math.round(hgt), ok: closed && open && hgt > 0 };
            }, i);
            folds.push(r);
        }
        const res = await page.evaluate(() => ({
            katex_errors: document.querySelectorAll('.katex-error').length,
            katex_count: document.querySelectorAll('#paper .katex').length,
            sideways_px: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            body_sideways_px: document.body.scrollWidth - document.body.clientWidth,
            refs: Array.from(document.querySelectorAll('#paper .prefs li a')).map(a => a.href),
            display_eqs: document.querySelectorAll('#paper .katex-display').length,
            tags: Array.from(document.querySelectorAll('#paper .katex-display .tag')).map(t => t.textContent).join(' ')
        }));
        out[w + 'x' + h] = Object.assign(res, { console_errors: errors, failed_requests: failed, folds_total: folds.length, folds_failed: folds.filter(f => !f.ok) });
        // screenshots of the edited paragraphs
        const targets = { s2: '#p-model p:nth-of-type(3)', s41: '#p-dft p:nth-of-type(4)', fig3: '#p-energy figure:nth-of-type(1) figcaption', s61: '#p-decay h4 + p', s61b: '#p-decay h4 + p + .katex-display + p + p + p', refs: '#p-limits .prefs' };
        for (const [k, sel] of Object.entries(targets)) {
            const el = await page.$(sel);
            if (el) { await el.scrollIntoViewIfNeeded(); await el.screenshot({ path: path.join(SHOTS, w + '-' + k + '.png') }); }
            else out[w + 'x' + h]['missing_' + k] = sel;
        }
        await ctx.close();
    }
    console.log(JSON.stringify(out, null, 1));
    await browser.close(); server.close();
})();
