// Fig. 9 measurements in headless Chromium, on the built page.
// Build first: cd /home/user/SiteTest && OUT_DIR=/tmp/fig09-dist npm run build
// Run: node notes/fig09/measure.cjs [out.json] [shot-prefix]
'use strict';
const path = require('path'), fs = require('fs'), http = require('http');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = '/tmp/fig09-dist', PORT = 47109;
const OUT = process.argv[2] || path.join(__dirname, 'measure-out.json');
const SHOT = process.argv[3] || '/tmp/fig09-shot';
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json', '.png': 'image/png' };

const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    if (p.endsWith('/')) p += 'index.html';
    const f = path.join(ROOT, p);
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
});

async function run(browser, vw, vh, tag) {
    const ctx = await browser.newContext({ viewport: { width: vw, height: vh } });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(`http://127.0.0.1:${PORT}/simulations/driven-oscillator.html`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds && document.querySelector('#paper .katex'));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(600);
    const R = { viewport: `${vw}x${vh}` };
    Object.assign(R, await page.evaluate(() => {
        const ds = Sim.data.ds, g = n => ds.get(n);
        const o = {};
        ['k', 'c', 'X', 'phi_deg', 'tau', 'Q', 'fr', 'Win', 'Wloss', 'balance', 'err_max', 'Xm', 'solve_ms', 'win_T', 'box_w', 'eq_px', 'amp_px', 'G_drive', 'Gm_drive'].forEach(n => { o[n] = g(n); });
        const Es = g('Es'); o.dE = Es[Es.length - 1] - Es[0];
        o.eq_frac = g('eq_px') / g('box_w'); o.span_frac = 2 * g('amp_px') / g('box_w');
        o.Pavg_steady = 0.5 * g('c') * g('Omega') * g('Omega') * g('X') * g('X');
        const xs = g('xs'), ts = g('ts'); let b = 0, bt = 0;
        for (let n = 0; n < xs.length; n++) if (ts[n] <= 15 && Math.abs(xs[n]) > b) { b = Math.abs(xs[n]); bt = ts[n]; }
        o.first_swell = b; o.first_swell_t = bt;
        o.katex_errors = document.querySelectorAll('.katex-error').length;
        o.paper_katex = document.querySelectorAll('#paper .katex').length;
        o.tags = [...document.querySelectorAll('#paper .katex-display .tag')].map(t => t.textContent.trim());
        o.scrollW = document.documentElement.scrollWidth; o.clientW = document.documentElement.clientWidth;
        o.body_scrollW = document.body.scrollWidth;
        o.pref_links = [...document.querySelectorAll('#paper .prefs a')].map(a => a.href);
        return o;
    }));
    // solve time, ten more solves with the defaults
    const times = [];
    for (let i = 0; i < 10; i++) { await page.click('#solve'); times.push(await page.evaluate(() => Sim.data.ds.get('solve_ms'))); }
    R.solve_ms_10 = times; R.solve_ms_min = Math.min(...times); R.solve_ms_max = Math.max(...times);
    // every fold: close and open again
    R.folds = await page.evaluate(async () => {
        const btns = [...document.querySelectorAll('.fs-toggle')];
        const bad = []; let ok = 0;
        for (const b of btns) {
            const before = b.getAttribute('aria-expanded');
            if (before === 'true') { b.click(); await new Promise(r => setTimeout(r, 20)); }
            if (b.getAttribute('aria-expanded') !== 'false') { bad.push('no close: ' + b.closest('[data-fold-level]').textContent.slice(0, 40)); continue; }
            b.click(); await new Promise(r => setTimeout(r, 20));
            if (b.getAttribute('aria-expanded') === 'true') ok++; else bad.push('no open: ' + b.closest('[data-fold-level]').textContent.slice(0, 40));
        }
        return { total: btns.length, opened: ok, bad };
    });
    await page.waitForTimeout(800);
    R.folds.paper_heights = await page.evaluate(() => [...document.querySelectorAll('#paper .psec')].map(s => [s.id, Math.round(s.getBoundingClientRect().height)]));
    R.scroll_after_folds = await page.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
    // overflowing display equations (they scroll inside their box, the page must not)
    R.wide_displays = await page.evaluate(() => [...document.querySelectorAll('#paper .katex-display')].filter(d => d.scrollWidth > d.clientWidth + 1).map(d => (d.querySelector('.tag') || {}).textContent || '?'));
    // screenshots of the note sections touched
    for (const id of ['p-exact', 'p-resonance', 'p-control', 'p-start', 'p-energy', 'p-screen', 'p-limits']) {
        const el = await page.$('#' + id);
        await el.screenshot({ path: `${SHOT}-${tag}-${id}.png` });
    }
    // Exercise 6.1: zeta 0.01, then f = 0.20 Hz
    R.ex61 = {};
    for (const [z, f] of [[0.01, 0.45], [0.01, 0.20]]) {
        await page.evaluate(([z, f]) => {
            const set = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input')); };
            set('zeta', z); set('fd', f);
        }, [z, f]);
        await page.click('#solve');
        R.ex61[`z${z}_f${f}`] = await page.evaluate(() => {
            const ds = Sim.data.ds, xs = ds.get('xs'), ts = ds.get('ts');
            let m20 = 0, t20 = 0; for (let n = 0; n < xs.length; n++) if (ts[n] <= 20 && Math.abs(xs[n]) > m20) { m20 = Math.abs(xs[n]); t20 = ts[n]; }
            return { X: ds.get('X'), phi_deg: ds.get('phi_deg'), tau: ds.get('tau'), Xm: ds.get('Xm'), max_x_first20s: m20, at: t20, err_max: ds.get('err_max') };
        });
        await page.evaluate(() => { const s = document.getElementById('seek'); s.value = 1500; s.dispatchEvent(new Event('input')); document.getElementById('play').click(); });
        await page.waitForTimeout(300);
        await (await page.$('#stage')).screenshot({ path: `${SHOT}-${tag}-ex61-z${z}-f${f}.png` });
        await page.evaluate(() => document.getElementById('play').click());
    }
    R.errors = errors;
    await ctx.close();
    return R;
}

(async () => {
    await new Promise(r => server.listen(PORT, '127.0.0.1', r));
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
    const out = [];
    try {
        out.push(await run(browser, 1440, 900, 'desk'));
        out.push(await run(browser, 390, 844, 'phone'));
    } finally { await browser.close(); server.close(); }
    fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
    console.log(JSON.stringify(out, null, 1));
})();
