// Fig. 14 in headless Chromium: the store with the defaults at the first and last stored frame, the frame clock, the
// canvas, and the note's health (KaTeX errors, equation tags, overflow, console errors) at two widths.
// Build first (OUT_DIR=<dir> npm run build), serve <dir> on 127.0.0.1:8714, then: node notes/fig14/page.cjs
'use strict';
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const URL = 'http://127.0.0.1:8714/simulations/schrodinger-sphere.html';
const KEYS = ['E', 'V0', 'R', 'k0', 'stored', 'source', 'file', 'sha_ok', 'steps', 'wall', 't', 'frame', 'ready', 'norm', 'behind', 'ahead', 'inside', 'lost', 'sigma_y', 'sigma_free', 'T1D'];
(async () => {
    const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
    const out = {};
    for (const [w, h] of [[1440, 900], [390, 844]]) {
        const page = await browser.newPage({ viewport: { width: w, height: h } }), errors = [];
        page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
        page.on('pageerror', e => errors.push('pageerror: ' + e.message));
        await page.goto(URL, { waitUntil: 'load' });
        await page.waitForFunction(() => window.__fig14 && window.__fig14.ds.get('source') === 'kaggle' && window.__fig14.ds.get('sha_ok') === true, null, { timeout: 60000 });
        const r = { errors };
        r.first = await page.evaluate(K => { const f = window.__fig14; f.play(false); f.setT(0); return new Promise(res => requestAnimationFrame(() => requestAnimationFrame(() => res(Object.fromEntries(K.map(k => [k, f.ds.get(k)])))))); }, KEYS);
        r.last = await page.evaluate(K => { const f = window.__fig14; f.setT(1e9); return new Promise(res => setTimeout(() => res(Object.fromEntries(K.map(k => [k, f.ds.get(k)]))), 400)); }, KEYS);
        r.mid = await page.evaluate(K => { const f = window.__fig14; f.setT(0.28 * 23.5); return new Promise(res => setTimeout(() => res(Object.fromEntries(K.map(k => [k, f.ds.get(k)]))), 400)); }, KEYS);
        r.readouts = await page.evaluate(() => ['r-b', 'r-a', 'r-i', 'r-l', 'r-g', 'cap-t', 'cap-p', 'src-t'].map(id => [id, document.getElementById(id).textContent]));
        r.canvas = await page.evaluate(() => { const c = document.getElementById('field'), b = c.getBoundingClientRect(); return { css_w: b.width, css_h: b.height, px_w: c.width, px_h: c.height, px_per_a: b.width / 64 }; });
        r.health = await page.evaluate(() => ({
            katex_errors: document.querySelectorAll('#paper .katex-error').length,
            tags: [...document.querySelectorAll('#paper .katex .tag')].map(t => t.textContent),
            scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
            sections: document.querySelectorAll('#paper section.psec').length, figs: document.querySelectorAll('#paper .pfig').length,
            boxes: [...document.querySelectorAll('#paper .pbox__t')].map(b => b.textContent),
            wide: [...document.querySelectorAll('#paper .katex-display, #paper .pfig, #paper .ptab')].filter(e => e.scrollWidth > e.clientWidth + 1).length,
            paperW: document.getElementById('paper').getBoundingClientRect().width }));
        out[w + 'x' + h] = r;
        if (w === 1440) {
            await page.evaluate(() => { const f = window.__fig14; f.setT(0.28 * 23); });
            await page.waitForTimeout(400);
            await page.locator('#stage').screenshot({ path: __dirname + '/shot-stage-1440.png' });
            await page.locator('#paper').screenshot({ path: __dirname + '/shot-paper-1440.png' });
        }
        await page.close();
    }
    await browser.close();
    require('fs').writeFileSync(__dirname + '/page-out.json', JSON.stringify(out, null, 1));
    console.log(JSON.stringify(out, null, 1));
})();
