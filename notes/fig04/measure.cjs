// Fig. 4 measurements, scratch. Part 1 replays the page's own formulas in Node (copied from
// public/simulations/Transverse and longitudinal waves.html: longAmp L799, readouts L801-813, draw L834-961,
// clock in scripts/sim.js L175-196). Part 2 opens the built page in headless Chromium and reads the data store.
// Run: node notes/fig04/measure.cjs   (after: APPDEPLOY_VITE_OUT_DIR=/tmp/fig04-dist npm run build)
'use strict';
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
const LENGTH = 640, R = {};

// ---------- part 1: the page's formulas ----------
function longAmp(A, lam) { return Math.min(A, 0.8 * lam / (2 * Math.PI)); }
function positions(A, lam, N, omegaT) {            // lower row, x = X + AL sin(kX - wt), as page L926-928
    const k = 2 * Math.PI / lam, AL = longAmp(A, lam), x = [];
    for (let i = 0; i < N; i++) { const X = i * LENGTH / (N - 1); x.push(X + AL * Math.sin(k * X - omegaT)); }
    return x;
}
function gaps(x) { const g = []; for (let i = 1; i < x.length; i++) g.push(x[i] - x[i - 1]); return g; }
function minGapOverPeriod(A, lam, N) {              // smallest neighbour gap over one period, 20000 phases
    let m = Infinity;
    for (let j = 0; j < 20000; j++) m = Math.min(m, ...gaps(positions(A, lam, N, 2 * Math.PI * j / 20000)));
    return m;
}
function minGapFormula(A, lam, N) {                 // a - 2 AL sin(ka/2), the closed form
    const a = LENGTH / (N - 1), k = 2 * Math.PI / lam; return a - 2 * longAmp(A, lam) * Math.sin(k * a / 2);
}
// defaults
const g0 = gaps(positions(26, 220, 26, 0));
R.default_first_frame_gap_min_px = Math.min(...g0);
R.default_first_frame_gap_max_px = Math.max(...g0);
R.default_min_gap_over_period_px = minGapOverPeriod(26, 220, 26);
R.default_ALk = longAmp(26, 220) * 2 * Math.PI / 220;
R.default_cap_px = 0.8 * 220 / (2 * Math.PI);
R.default_Aomega = 26 * 2 * Math.PI * 0.5;
R.rho_max = 1 / (1 - R.default_ALk); R.rho_min = 1 / (1 + R.default_ALk);
R.denser_half_fraction_formula = 0.5 - R.default_ALk / Math.PI;
// the same fraction measured: fine rest grid, actual positions of the part where cos(phase) < 0 at wt = 0
(function () {
    const k = 2 * Math.PI / 220, AL = longAmp(26, 220); let lo = Infinity, hi = -Infinity;
    for (let X = 0; X <= 220; X += 0.001) { const ph = k * X; if (Math.cos(ph) < 0) { const x = X + AL * Math.sin(ph); lo = Math.min(lo, x); hi = Math.max(hi, x); } }
    R.denser_half_fraction_measured = (hi - lo) / 220;
})();
// Exercise 3.1: f = 1 Hz, lambda = 110 px, A = 26 px
R.ex31_AL_px = longAmp(26, 110);
R.ex31_upper_top_speed = 26 * 2 * Math.PI * 1;
R.ex31_lower_top_speed = longAmp(26, 110) * 2 * Math.PI * 1;
R.ex31_lower_top_speed_at_220 = longAmp(26, 220) * 2 * Math.PI * 1;
// Exercise 5.1: A = 29, lambda = 100 px
R.ex51_cap_px = 0.8 * 100 / (2 * Math.PI);
R.ex51_readout = longAmp(29, 100).toFixed(0) + ' px' + (longAmp(29, 100) < 29 ? ' (cap)' : '');
R.ex51_readout_A28_220 = longAmp(28, 220).toFixed(0) + ' px' + (longAmp(28, 220) < 28 ? ' (cap)' : '');
R.ex51_readout_A29_220 = longAmp(29, 220).toFixed(0) + ' px' + (longAmp(29, 220) < 29 ? ' (cap)' : '');
R.ex51_Ak_upper = 29 * 2 * Math.PI / 100;
R.ex51_min_gap_N26_px = minGapOverPeriod(29, 100, 26);
R.ex51_min_gap_N26_formula_px = minGapFormula(29, 100, 26);
R.ex51_min_gap_N40_px = minGapOverPeriod(29, 100, 40);
R.ex51_min_gap_N40_formula_px = minGapFormula(29, 100, 40);
R.ex51_rest_spacing_N40 = LENGTH / 39;
R.ex51_min_over_rest_N40 = R.ex51_min_gap_N40_px / R.ex51_rest_spacing_N40;
// curve points and gradient stops, counted from the loops of draw()
let nCurve = 0; for (let X = 0; X <= LENGTH; X += 3) nCurve++; nCurve++;      // L868-872: loop + final lineTo
let nStops = 0; for (let X = 0; X <= LENGTH; X += LENGTH / 64) nStops++;       // L911
R.curve_points = nCurve; R.gradient_stops = nStops;
// Section 9 numbers
R.slope_angle_deg = Math.atan(R.default_ALk) * 180 / Math.PI;
R.chain_slowdown_percent = (1 - Math.sin(Math.PI * 25.6 / 220) / (Math.PI * 25.6 / 220)) * 100;
// Section 7: largest phase step at the top frequency
R.max_phase_step_rad = 2 * Math.PI * 2 * 0.05;

// Figure 1 (first SVG plate): bead centres x = 40 + X, upper y = 124 - xi, lower x = 40 + X + xi
// Figure 4 (fifth SVG plate): dots x = 64 + 0.99067 X, y = 254 - 56.2 rho (grid line 0 at y = 254)
(function () {
    const html = fs.readFileSync(path.join(__dirname, '../../public/simulations/Transverse and longitudinal waves.html'), 'utf8');
    const svgs = html.split('<svg').slice(1).map(s => s.split('</svg>')[0]);
    const k = 2 * Math.PI / 220;
    const circ = svgs[0].match(/<circle cx="([\d.]+)" cy="([\d.]+)"/g).map(c => c.match(/[\d.]+/g).map(Number));
    let worst = 0;
    const up = circ.filter(c => c[1] < 200), lowc = circ.filter(c => c[1] > 200);
    up.forEach((c, i) => { const X = i * 25.6, xi = 26 * Math.sin(k * X); worst = Math.max(worst, Math.abs(c[0] - 40 - X), Math.abs(c[1] - (124 - xi))); });
    lowc.forEach((c, i) => { const X = i * 25.6, xi = 26 * Math.sin(k * X); worst = Math.max(worst, Math.abs(c[0] - 40 - X - xi)); });
    R.fig1_beads = up.length + '+' + lowc.length; R.fig1_worst_px = worst;
    const d4 = (svgs[4].match(/<circle cx="([\d.]+)" cy="([\d.]+)"/g) || []).map(c => c.match(/[\d.]+/g).map(Number));
    let w4 = 0, sx = (658.4 - 64) / 600, sy = (258 - 201.8);
    d4.forEach((c, i) => { const X = i * 25.6, rho = 1 / (1 + 26 * k * Math.cos(k * X)); w4 = Math.max(w4, Math.abs(c[0] - (64 + sx * X)), Math.abs(c[1] - (254 - sy * rho))); });
    R.fig4_dots = d4.length; R.fig4_worst_px = w4;
})();

// ---------- part 2: the built page in headless Chromium ----------
const ROOT = '/tmp/fig04-dist', TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json', '.png': 'image/png' };
const server = http.createServer((q, s) => {
    const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
    fs.readFile(p, (e, b) => { if (e) { s.writeHead(404); s.end(); return; } s.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); s.end(b); });
});
async function page(browser, w, h, reduce) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: reduce ? 'reduce' : 'no-preference' });
    const pg = await ctx.newPage(), errors = [];
    pg.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    pg.on('pageerror', e => errors.push(String(e)));
    await pg.goto('http://127.0.0.1:' + server.address().port + '/simulations/' + encodeURIComponent('Transverse and longitudinal waves.html'));
    await pg.waitForFunction(() => window.Sim && Sim.data && document.querySelectorAll('#paper .katex').length > 20, null, { timeout: 20000 });
    await pg.waitForTimeout(800);
    return { ctx, pg, errors };
}
async function setSlider(pg, id, v) {
    await pg.evaluate(([id, v]) => { const el = document.getElementById(id); el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); }, [id, v]);
    await pg.waitForTimeout(150);
}
(async () => {
    await new Promise(r => server.listen(0, '127.0.0.1', r));
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
    for (const [w, h] of [[1440, 900], [390, 844]]) {
        const { ctx, pg, errors } = await page(browser, w, h, true);   // reduced motion: clock starts paused at wt = 0
        const r = await pg.evaluate(() => {
            const ds = Sim.data.ds, x = Array.from(ds.get('xL')), g = [];
            for (let i = 1; i < x.length; i++) g.push(x[i] - x[i - 1]);
            return { box_w: ds.get('box_w'), box_h: ds.get('box_h'), s_px: ds.get('s_px'), omegaT: ds.get('omegaT'), playing: ds.get('playing'),
                k: ds.get('k'), AL: ds.get('AL'), ALk: ds.get('ALk'), Aomega: ds.get('Aomega'), follow: ds.get('follow'), X_follow: ds.get('X')[ds.get('follow')],
                rho_max: Math.max.apply(null, ds.get('rho')), gap_min: Math.min.apply(null, g), gap_max: Math.max.apply(null, g),
                readout_al: document.getElementById('r-al').textContent, play_label: document.getElementById('play').textContent,
                katex: document.querySelectorAll('#paper .katex').length, katexErr: document.querySelectorAll('.katex-error').length,
                sideways: document.documentElement.scrollWidth - window.innerWidth };
        });
        // count the burgundy curve's points and the gradient stops in one real frame
        const cnt = await pg.evaluate(() => new Promise(res => {
            const P = CanvasRenderingContext2D.prototype, G = CanvasGradient.prototype, o = { m: P.moveTo, l: P.lineTo, s: P.stroke, b: P.beginPath, a: G.addColorStop };
            let n = 0, curve = 0, stops = 0;
            P.beginPath = function () { n = 0; return o.b.apply(this, arguments); };
            P.moveTo = function () { n++; return o.m.apply(this, arguments); };
            P.lineTo = function () { n++; return o.l.apply(this, arguments); };
            P.stroke = function () { if (this.strokeStyle === 'rgba(122, 31, 43, 0.45)' || /0\.45\)$/.test(this.strokeStyle)) curve = Math.max(curve, n); return o.s.apply(this, arguments); };
            G.addColorStop = function () { stops++; return o.a.apply(this, arguments); };
            requestAnimationFrame(() => requestAnimationFrame(() => { Object.assign(P, { moveTo: o.m, lineTo: o.l, stroke: o.s, beginPath: o.b }); G.addColorStop = o.a; res({ curve, stopsPerFrame: stops }); }));
        }));
        R['page_' + w] = Object.assign(r, cnt, { errors: errors.length });
        if (w === 1440) {
            // Exercise 3.1 in the page: f = 1, lambda = 110
            await setSlider(pg, 'freq', 1); await setSlider(pg, 'lambda', 110);
            R.page_ex31 = await pg.evaluate(() => { const ds = Sim.data.ds; return { AL: ds.get('AL'), readout: document.getElementById('r-al').textContent, v: document.getElementById('r-v').textContent, T: document.getElementById('r-t').textContent, upperTop: ds.get('Aomega'), lowerTop: ds.get('AL') * ds.get('omega') }; });
            await setSlider(pg, 'freq', 0.5); await setSlider(pg, 'lambda', 220);
            // Exercise 5.1: A 28, 29 at 220; then lambda 100
            await setSlider(pg, 'amp', 28); const r28 = await pg.evaluate(() => document.getElementById('r-al').textContent);
            await setSlider(pg, 'amp', 29); const r29 = await pg.evaluate(() => document.getElementById('r-al').textContent);
            await setSlider(pg, 'lambda', 100); const r100 = await pg.evaluate(() => document.getElementById('r-al').textContent);
            // play one period and track the smallest neighbour gap, with 26 and with 40 particles
            const track = async () => pg.evaluate(() => new Promise(res => {
                const ds = Sim.data.ds; let m = Infinity, frames = 0; const t0 = performance.now();
                Sim.data.play();
                (function f() { const x = ds.get('xL'); for (let i = 1; i < x.length; i++) m = Math.min(m, x[i] - x[i - 1]); frames++;
                    if (performance.now() - t0 < 2200) requestAnimationFrame(f); else res({ min_gap_px: m, frames, rest: x[1] - x[0] + 0 }); })();
            }));
            const g26 = await track();
            await setSlider(pg, 'count', 40); await pg.waitForTimeout(200);
            const g40 = await track();
            R.page_ex51 = { A28_220: r28, A29_220: r29, A29_100: r100, min_gap_N26: g26.min_gap_px, frames26: g26.frames, min_gap_N40: g40.min_gap_px, frames40: g40.frames };
        }
        await ctx.close();
    }
    await browser.close(); server.close();
    fs.writeFileSync(path.join(__dirname, 'measure-out.json'), JSON.stringify(R, null, 1));
    console.log(JSON.stringify(R, null, 1));
})().catch(e => { console.error(e); process.exit(1); });
