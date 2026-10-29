// Fig. 8 measurements in headless Chromium, from the page's own store (Sim.data.ds) after driving its controls.
// Build first: OUT_DIR=/tmp/fig08-dist npm run build. Run: node notes/fig08/measure.cjs [/tmp/fig08-dist]
'use strict';
const http = require('http'), fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = process.argv[2] || '/tmp/fig08-dist';
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
});
const pageSrc = fs.readFileSync(path.join(__dirname, '../../public/simulations/draw-decompose.html'), 'utf8');
const dftSrc = pageSrc.slice(pageSrc.indexOf('function dft(z) {'), pageSrc.indexOf('function chainAt(time, n) {'));

(async () => {
    await new Promise(r => server.listen(0, r));
    const url = 'http://127.0.0.1:' + server.address().port + '/simulations/draw-decompose.html';
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
    const R = {};
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds && Sim.data.ds.dims.k === 120);
    await page.waitForTimeout(500);

    R.measured = await page.evaluate(async (dftSrc) => {
        const ds = Sim.data.ds, out = {};
        const setK = k => { const el = document.getElementById('K'); el.value = k; el.dispatchEvent(new Event('input')); };
        const preset = s => document.querySelector('[data-shape="' + s + '"]').click();
        const amp = k => { const CK = ds.get('c_k'), CA = ds.get('c_amp'); for (let i = 0; i < CK.length; i++) if (CK[i] === k) return CA[i]; return null; };
        const txt = id => document.getElementById(id).textContent;
        const sweep = () => { let worst = 0, at = 0; const rel = {}; for (let K = 1; K <= 120; K++) { setK(K); const e = ds.get('err'), p = ds.get('errP'), d = Math.abs(e - p) / e; if (d > worst) { worst = d; at = K; } rel[K] = e / Math.sqrt(ds.get('E')); } return { worst, at, rel }; };
        // heart (loaded at start)
        preset('heart'); setK(24);
        out.heart = { L: ds.get('L'), step: ds.get('step'), E: ds.get('E'), err24: ds.get('err'), errP24: ds.get('errP'), cap24_text: txt('r-cap'), err24_text: txt('r-err'), errp24_text: txt('r-errp'), k2c: [10, 20, 30].map(k => k * k * amp(k)) };
        setK(1); out.heart.K1 = { cap_text: txt('r-cap'), cap: ds.get('cap'), k1: ds.get('c_k')[0], rel: ds.get('err') / Math.sqrt(ds.get('E')) };
        setK(120); out.heart.K120 = { err: ds.get('err'), rel: ds.get('err') / Math.sqrt(ds.get('E')) };
        const hs = sweep(); out.heart.sweep_worst_rel_diff = hs.worst; out.heart.sweep_worst_at = hs.at;
        out.heart.rel = { 10: hs.rel[10], 24: hs.rel[24], 50: hs.rel[50], 80: hs.rel[80], 120: hs.rel[120] };
        // square
        preset('square'); setK(1);
        out.square = { E: ds.get('E'), L: ds.get('L'), K1_cap_text: txt('r-cap'), K1_err_text: txt('r-err'), radii: [1, -3, 5, 2, -1].map(k => [k, amp(k)]) };
        setK(4); out.square.K4_first = Array.from(ds.get('c_k')).slice(0, 4);
        { const sp = Sim.data.ds; out.square.K4_spec_y_burgundy = Array.from(sp.get('c_k')).slice(0, 4); }
        // open wave
        preset('wave');
        out.wave = { kc10: 10 * amp(10), L: ds.get('L') };
        setK(24); out.wave.rel24 = ds.get('err') / Math.sqrt(ds.get('E'));
        setK(50); out.wave.rel50 = ds.get('err') / Math.sqrt(ds.get('E'));
        setK(120); out.wave.rel120 = ds.get('err') / Math.sqrt(ds.get('E'));
        // figure eight
        preset('eight'); setK(120);
        out.eight = { step: ds.get('step'), c60: [amp(60), amp(-60)], rel120: ds.get('err') / Math.sqrt(ds.get('E')) };
        // timing: the whole decomposition (preset click: param, decompose, rebuild, readouts, spectrum) and dft() alone
        setK(24);
        const times = []; for (let i = 0; i < 40; i++) { const t0 = performance.now(); preset('heart'); times.push(performance.now() - t0); }
        times.sort((a, b) => a - b);
        const dft = new Function('TAU', 'KMAX', dftSrc + '; return dft;')(2 * Math.PI, 60);
        const X = ds.get('z_x'), Y = ds.get('z_y'), z = Array.from(X).map((x, i) => ({ x, y: Y[i] }));
        const td = []; for (let i = 0; i < 40; i++) { const t0 = performance.now(); dft(z); td.push(performance.now() - t0); }
        td.sort((a, b) => a - b);
        out.timing_ms = { decompose_median: times[20], decompose_min: times[0], dft_median: td[20], dft_min: td[0] };
        // the dft copy run here gives the store's coefficients exactly
        const c = dft(z); out.dft_copy_matches_store = c.every((q, i) => q.amp === ds.get('c_amp')[i] && q.k === ds.get('c_k')[i]);
        return out;
    }, dftSrc);
    R.console_errors = errors.slice();
    await browser.close();
    server.close();
    console.log(JSON.stringify(R, null, 1));
    fs.writeFileSync(path.join(__dirname, 'measure-out.json'), JSON.stringify(R, null, 1));
})();
