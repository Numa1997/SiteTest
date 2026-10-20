// Fig. 2 in headless Chromium: page health at two sizes, and the numbers the note quotes, read from the page's own store.
// Serve dist/ first (python3 -m http.server 8702 --directory dist), then: node notes/fig02/chromium.cjs [health|drift|long|mass|twin|shots]
'use strict';
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const URL = 'http://127.0.0.1:8702/simulations/Double%20Pendulum.html';
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const mode = process.argv[2] || 'health';

async function open(browser, w, h, fake) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    if (fake) await page.clock.install({ time: 0 });
    await page.goto(URL, { waitUntil: 'load' });
    return { page, errors };
}
// collect the store every frame, after the page's own frame callback has run
const HOOK = `(() => { window.__rec = { max: -Infinity, maxT: 0, min: Infinity, minT: 0, maxAbs: 0, firstOver: null, samples: [], sepFirst01: null, frames: 0, w1max: 0 };
  const ds = Sim.data.ds;
  function f() { const e = ds.get('drift'), t = ds.get('t'), r = window.__rec; r.frames++; r.w1max = Math.max(r.w1max, Math.abs(ds.get('w1')));
    if (e > r.max) { r.max = e; r.maxT = t; } if (e < r.min) { r.min = e; r.minT = t; }
    if (Math.abs(e) > r.maxAbs) r.maxAbs = Math.abs(e);
    if (r.firstOver === null && Math.abs(e) > 1e-7) r.firstOver = t;
    const s = ds.get('sep'); if (s !== undefined && r.sepFirst01 === null && s >= 0.1) r.sepFirst01 = t;
    if (r.samples.length === 0 || t - r.samples[r.samples.length - 1][0] >= (window.__every || 60)) r.samples.push([t, e, s]);
    requestAnimationFrame(f); }
  requestAnimationFrame(f); })()`;

(async () => {
    const browser = await chromium.launch({ executablePath: EXE });
    if (mode === 'health' || mode === 'shots') {
        for (const [w, h] of [[1440, 900], [390, 844]]) {
            const { page, errors } = await open(browser, w, h, false);
            await page.waitForTimeout(2500);
            const r = await page.evaluate(() => ({
                katex: document.querySelectorAll('#paper .katex').length,
                katexErrors: document.querySelectorAll('.katex-error').length,
                scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
                bodyScrollW: document.body.scrollWidth,
                eqNumbers: Array.from(document.querySelectorAll('#paper .katex-display .tag')).map(e => e.textContent.trim()),
                refs: Array.from(document.querySelectorAll('#paper .prefs a')).map(a => a.href),
                scale: Sim.data.ds.get('scale'), ox: Sim.data.ds.get('ox'), oy: Sim.data.ds.get('oy'),
                wide: Array.from(document.querySelectorAll('#paper *')).filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1 && getComputedStyle(e).overflowX === 'visible' && !e.closest('.katex-display')).slice(0, 5).map(e => e.tagName + '.' + e.className)
            }));
            console.log(w + 'x' + h, JSON.stringify(r), 'console errors:', JSON.stringify(errors));
            if (mode === 'shots') {
                for (const id of ['p-lagrange', 'p-chaos', 'p-rk4', 'p-screen', 'p-limits']) {
                    const el = await page.$('#' + id);
                    await el.scrollIntoViewIfNeeded();
                    await page.waitForTimeout(300);
                    await el.screenshot({ path: `/home/user/SiteTest/notes/fig02/shot-${id}-${w}.png` });
                }
            }
            await page.close();
        }
    }
    if (mode === 'drift') { // real clock, about 21 s of the default start
        const { page, errors } = await open(browser, 1440, 900, false);
        await page.evaluate(HOOK);
        await page.waitForTimeout(21500);
        const r = await page.evaluate(() => ({ rec: window.__rec, t: Sim.data.ds.get('t'), n: Sim.data.ds.get('n'), fps: Sim.data.ds.get('fps'), E: Sim.data.ds.get('E'), readout: document.getElementById('r-drift').textContent }));
        console.log('real clock:', JSON.stringify({ max: r.rec.max, maxT: r.rec.maxT, min: r.rec.min, minT: r.rec.minT, frames: r.rec.frames, t: r.t, n: r.n, fps: r.fps, E: r.E, readout: r.readout }), 'errors:', errors.length);
    }
    if (mode === 'long') { // fake clock: rAF every 16 ms; ten simulated minutes of the default start
        const { page, errors } = await open(browser, 1440, 900, true);
        await page.clock.runFor(100);
        await page.evaluate('window.__every = 60;' + HOOK);
        for (let k = 0; k < 10; k++) await page.clock.runFor(60000);
        const r = await page.evaluate(() => ({ rec: window.__rec, t: Sim.data.ds.get('t'), drift: Sim.data.ds.get('drift'), readout: document.getElementById('r-drift').textContent }));
        console.log('fake clock, default start:', JSON.stringify({ t: r.t, drift: r.drift, readout: r.readout, max20: null, firstOver1e7: r.rec.firstOver, samples: r.rec.samples.map(s => [+s[0].toFixed(2), s[1]]) }), 'errors:', errors.length);
    }
    if (mode === 'mass') { // fake clock; mass ratio at its top, everything else default, 20 s
        const { page, errors } = await open(browser, 1440, 900, true);
        await page.clock.runFor(100);
        await page.evaluate(() => { const s = document.getElementById('mass'); s.value = '2.3'; s.dispatchEvent(new Event('input', { bubbles: true })); });
        await page.evaluate(HOOK);
        await page.clock.runFor(20000);
        let r = await page.evaluate(() => ({ rec: window.__rec, t: Sim.data.ds.get('t'), m2: Sim.data.ds.get('m2'), readout: document.getElementById('r-drift').textContent }));
        console.log('mass ratio 10:', JSON.stringify({ m2: r.m2, t: r.t, w1max: r.rec.w1max, maxAbs: r.rec.maxAbs, max: r.rec.max, min: r.rec.min, readout: r.readout }), 'errors:', errors.length);
        // every slider at its far end
        await page.evaluate(() => { for (const [id, v] of [['length', '1.6'], ['th1', '90'], ['th2', '-90'], ['w1', '5'], ['w2', '-5']]) { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); } });
        await page.evaluate(HOOK);
        await page.clock.runFor(20000);
        r = await page.evaluate(() => ({ rec: window.__rec, t: Sim.data.ds.get('t'), m2: Sim.data.ds.get('m2'), l2: Sim.data.ds.get('l2'), readout: document.getElementById('r-drift').textContent }));
        console.log('far corner:', JSON.stringify({ m2: r.m2, l2: r.l2, t: r.t, maxAbs: r.rec.maxAbs, readout: r.readout }), 'errors:', errors.length);
    }
    if (mode === 'twin') { // fake clock; twin on from the default start
        const { page, errors } = await open(browser, 1440, 900, true);
        await page.clock.runFor(100);
        await page.evaluate(() => { document.getElementById('twin').click(); document.getElementById('restart').click(); });
        await page.evaluate('window.__every = 0.5;' + HOOK);
        await page.clock.runFor(6000);
        const r = await page.evaluate(() => ({ rec: window.__rec, t: Sim.data.ds.get('t') }));
        console.log('twin, default start:', JSON.stringify({ firstSep01_t: r.rec.sepFirst01, samples: r.rec.samples.map(s => [+s[0].toFixed(3), s[2]]) }), 'errors:', errors.length);
    }
    await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
