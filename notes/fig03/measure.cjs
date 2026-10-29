// Fig. 3: measurements in headless Chromium on the built page, and the layout checks after the edit.
// Build first: cd /home/user/SiteTest && OUT_DIR=/tmp/fig03-dist npm run build
// Run: node notes/fig03/measure.cjs   (writes notes/fig03/measure-out.json)
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const ROOT = '/tmp/fig03-dist', PORT = 8603;
const PAGE = '/simulations/' + encodeURIComponent('Interactive Double-Slit Experiment Visualization.html');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (err, data) => {
        if (err) { res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(data);
    });
});

async function setSliders(page, v) {
    await page.evaluate((v) => {
        for (const id in v) { const el = document.getElementById(id); el.value = String(v[id]); el.dispatchEvent(new Event('input', { bubbles: true })); }
    }, v);
}
async function readStore(page) {
    return page.evaluate(() => {
        const ds = Sim.data.ds, g = (k) => ds.get(k);
        const px = Array.from(g('pt_x')), py = Array.from(g('pt_y'));
        // angle at P (index 3) between the paths from S1 (0) and S2 (1)
        const v1 = [px[3] - px[0], py[3] - py[0]], v2 = [px[3] - px[1], py[3] - py[1]];
        const L1 = g('L1'), L2 = g('L2');
        const gamma = Math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (L1 * L2)) * 180 / Math.PI;
        return { d: g('d'), alpha: g('alpha_deg'), b: g('b'), lambda: g('lambda'), L1, L2, ds: g('ds'), b_sin_a: g('b_sin_a'), ratio: g('ratio'),
            verdict: g('verdict'), m_x: Array.from(g('m_x')), m_theta: Array.from(g('m_theta')), gamma_deg: gamma, sin2half: Math.sin(gamma * Math.PI / 360) ** 2,
            readout_ratio: document.getElementById('r-m').textContent, readout_ds: document.getElementById('r-ds').textContent, readout_ff: document.getElementById('r-ff').textContent };
    });
}

async function layout(browser, w, h, tag) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto('http://127.0.0.1:' + PORT + PAGE, { waitUntil: 'load' });
    await page.waitForFunction(() => document.querySelectorAll('#paper .katex').length > 50, null, { timeout: 20000 });
    await page.waitForTimeout(800);
    // every fold: close all, then open each one by its own toggle, outer before inner
    const folds = await page.evaluate(async () => {
        const wait = (ms) => new Promise((r) => setTimeout(r, ms));
        const tool = (t) => Array.from(document.querySelectorAll('.fold-tool')).find((b) => b.textContent === t);
        tool('Collapse all').click(); await wait(100);
        const nodes = Array.from(document.querySelectorAll('[data-fold-level]'));
        const closedAfterCollapse = nodes.filter((n) => n.getAttribute('data-collapsed') === '1').length;
        const result = [];
        for (const lvl of ['1', '2']) {
            for (const n of nodes.filter((n) => n.getAttribute('data-fold-level') === lvl)) {
                const btn = n.querySelector(':scope > .fs-head .fs-toggle');
                if (n.getAttribute('data-collapsed') === '1') btn.click();
                await wait(450);
                const body = n.querySelector(':scope > .fold');
                result.push({ id: n.id || (n.querySelector('h3,h4') || {}).textContent, level: lvl, open: n.getAttribute('data-collapsed') === '0', aria: btn.getAttribute('aria-expanded'), height: Math.round(body.getBoundingClientRect().height) });
            }
        }
        tool('Expand all').click(); await wait(100);
        return { total: nodes.length, closedAfterCollapse, opened: result.filter((r) => r.open && r.aria === 'true' && r.height > 0).length, failures: result.filter((r) => !(r.open && r.aria === 'true' && r.height > 0)) };
    });
    await page.waitForTimeout(500);
    const checks = await page.evaluate(() => {
        const sw = document.documentElement.scrollWidth, cw = document.documentElement.clientWidth;
        const wide = Array.from(document.querySelectorAll('#paper *')).filter((e) => e.getBoundingClientRect().right > cw + 0.5 && !e.closest('.katex-display, .pfig__plate, svg')).map((e) => e.tagName + '.' + e.className).slice(0, 5);
        const refs = Array.from(document.querySelectorAll('#paper .prefs li')).map((li) => ({ text: li.textContent.slice(0, 60), links: Array.from(li.querySelectorAll('a')).map((a) => a.href) }));
        return { katexError: document.querySelectorAll('.katex-error').length, katexInPaper: document.querySelectorAll('#paper .katex').length, scrollWidth: sw, clientWidth: cw, sideways: sw - cw, wideInPaper: wide, refs };
    });
    // screenshots of the changed passages
    const shots = [];
    for (const [sel, name] of [['#p-adding .pbox', 'box5'], ['#p-adding p:has-text("The order of the steps matters")', 'cross'], ['#p-quantum p:has-text("The pattern needs both slits")', 'quantum'], ['#p-limits', 'limits']]) {
        const el = await page.$(sel);
        if (el) { const f = path.join(__dirname, 'shot-' + name + '-' + tag + '.png'); await el.screenshot({ path: f }); shots.push(f); }
    }
    await ctx.close();
    return { viewport: [w, h], errors, folds, checks, shots };
}

(async () => {
    await new Promise((r) => server.listen(PORT, '127.0.0.1', r));
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
    const out = {};
    // numbers, read from the page's own store
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto('http://127.0.0.1:' + PORT + PAGE, { waitUntil: 'load' });
    await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds);
    out.defaults = await readStore(page);
    out.ex51 = {};
    for (const a of [9.5, 10, 19.5, 20]) { await setSliders(page, { d: 200, b: 40, lambda: 13.5, alpha: a }); out.ex51[a] = await readStore(page); }
    await setSliders(page, { d: 100, b: 80, lambda: 13.5, alpha: 30 }); out.ex41_d100 = await readStore(page);
    await setSliders(page, { d: 300, b: 80, lambda: 13.5, alpha: 30 }); out.ex41_d300 = await readStore(page);
    // gamma over every slider setting of d, alpha, b (the page's own compute(), via the sliders, at a coarse grid)
    let gmin = 1e9, gmax = 0;
    for (const d of [100, 200, 300]) for (const b of [20, 40, 80]) for (const a of [0, 15, 30]) {
        await setSliders(page, { d, b, lambda: 13.5, alpha: a }); const s = await readStore(page); gmin = Math.min(gmin, s.gamma_deg); gmax = Math.max(gmax, s.gamma_deg);
    }
    out.gamma_grid = { gmin, gmax };
    await ctx.close();
    out.layout1440 = await layout(browser, 1440, 900, '1440');
    out.layout390 = await layout(browser, 390, 844, '390');
    await browser.close(); server.close();
    fs.writeFileSync(path.join(__dirname, 'measure-out.json'), JSON.stringify(out, null, 1));
    const s = (o) => ({ alpha: o.alpha, ratio: o.ratio.toFixed(4), readout: o.readout_ratio, verdict: o.verdict, gamma: o.gamma_deg.toFixed(3), sin2half: o.sin2half.toFixed(5) });
    console.log(JSON.stringify({ defaults: { ds: out.defaults.ds, ff: out.defaults.b_sin_a, m_x1: out.defaults.m_x[1], gamma: out.defaults.gamma_deg },
        ex51: Object.values(out.ex51).map(s), ex41: [out.ex41_d100.ds, out.ex41_d100.b_sin_a, out.ex41_d300.ds], gamma_grid: out.gamma_grid,
        l1440: { errors: out.layout1440.errors, folds: out.layout1440.folds, k: out.layout1440.checks.katexError, kp: out.layout1440.checks.katexInPaper, side: out.layout1440.checks.sideways, wide: out.layout1440.checks.wideInPaper },
        l390: { errors: out.layout390.errors, folds: out.layout390.folds, k: out.layout390.checks.katexError, side: out.layout390.checks.sideways, wide: out.layout390.checks.wideInPaper },
        refs: out.layout390.checks.refs }, null, 1));
})().catch((e) => { console.error(e); process.exit(1); });
