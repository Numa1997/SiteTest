// Fig. 4 after the edits: console errors, KaTeX errors, sideways scroll, every fold opens, screenshots of the edited spots.
// Run: node notes/fig04/verify.cjs   (after: OUT_DIR=/tmp/fig04-dist npm run build)
'use strict';
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = '/tmp/fig04-dist', OUT = '/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig04-shots';
fs.mkdirSync(OUT, { recursive: true });
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, s) => {
    const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
    fs.readFile(p, (e, b) => { if (e) { s.writeHead(404); s.end(); return; } s.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); s.end(b); });
});
const SPOTS = ['the price of not bulging', 'At rest that half', 'set <em>Particles</em> to 40', 'tilted to the slope', 'Section 5 gives the rule', 'any particle in the upper row', 'raises the pressure by', 'the last at its end', 'Free online edition'];
(async () => {
    await new Promise(r => server.listen(0, '127.0.0.1', r));
    const browser = await chromium.launch();
    const R = {};
    for (const [w, h] of [[1440, 900], [390, 844]]) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h } });
        const pg = await ctx.newPage(), errors = [];
        pg.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
        pg.on('pageerror', e => errors.push(String(e)));
        await pg.goto('http://127.0.0.1:' + server.address().port + '/simulations/' + encodeURIComponent('Transverse and longitudinal waves.html'));
        await pg.waitForFunction(() => document.querySelectorAll('#paper .katex').length > 20 && document.querySelector('.fold-tool'), null, { timeout: 20000 });
        await pg.waitForTimeout(1500);
        // close everything, then open each fold by its own toggle, outer before inner
        await pg.evaluate(() => [...document.querySelectorAll('.fold-tool')].find(b => b.textContent === 'Collapse all').click());
        await pg.waitForTimeout(300);
        const n = await pg.evaluate(() => document.querySelectorAll('[data-fold-level]').length);
        const failed = [];
        for (let i = 0; i < n; i++) {
            const ok = await pg.evaluate(async i => {
                const node = document.querySelectorAll('[data-fold-level]')[i];
                const btn = node.querySelector(':scope > .fs-head .fs-toggle');
                if (node.getAttribute('data-collapsed') !== '0') btn.click();
                await new Promise(r => setTimeout(r, 450));
                const body = node.querySelector(':scope > .fold');
                return { id: node.id || node.querySelector('h3,h4') && node.querySelector('h3,h4').textContent.slice(0, 40), open: node.getAttribute('data-collapsed') === '0', h: body ? body.getBoundingClientRect().height : 0, inert: body ? body.hasAttribute('inert') : true };
            }, i);
            if (!ok.open || ok.h < 10 || ok.inert) failed.push(ok);
        }
        const r = await pg.evaluate(() => ({
            katex: document.querySelectorAll('#paper .katex').length, katexErr: document.querySelectorAll('.katex-error').length,
            sideways: document.documentElement.scrollWidth - window.innerWidth,
            wideKids: [...document.querySelectorAll('#paper .katex-display, #paper p, #paper li')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX === 'visible').length,
            refs: [...document.querySelectorAll('#paper .prefs li')].map(li => [...li.querySelectorAll('a')].map(a => a.href)),
            }));
        R[w] = Object.assign(r, { folds: n, foldsFailed: failed, errors });
        // screenshots of the edited spots, all folds open
        let k = 0;
        for (const s of SPOTS) {
            const plain = s.replace(/<[^>]+>/g, '').replace(/\\\(.*$/, '').trim();
            const loc = pg.locator('#paper p, #paper li', { hasText: plain.length > 6 ? plain : 'Free online edition' }).first();
            if (await loc.count()) { await loc.scrollIntoViewIfNeeded(); await pg.waitForTimeout(150); await loc.screenshot({ path: path.join(OUT, `w${w}-${++k}.png`) }); }
        }
        await ctx.close();
    }
    await browser.close(); server.close();
    console.log(JSON.stringify(R, null, 1));
})().catch(e => { console.error(e); process.exit(1); });
