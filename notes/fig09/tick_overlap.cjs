// Measures the overlap of the last time-tick label with "t (s)" in the window chart (drawWindow, page L783-L785),
// at zeta = 0.01, f = 0.20 Hz, stored sample 1500, 1440 x 900. Run after measure.cjs's build: node notes/fig09/tick_overlap.cjs
'use strict';
const path = require('path'), fs = require('fs'), http = require('http'), { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = '/tmp/fig09-dist', PORT = 47110;
const server = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': f.endsWith('.html') ? 'text/html' : f.endsWith('.js') ? 'text/javascript' : f.endsWith('.css') ? 'text/css' : f.endsWith('.woff2') ? 'font/woff2' : 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
(async () => {
    await new Promise(r => server.listen(PORT, '127.0.0.1', r));
    const b = await chromium.launch();
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(`http://127.0.0.1:${PORT}/simulations/driven-oscillator.html`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const out = await p.evaluate(() => {
        const set = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input')); };
        set('zeta', 0.01); set('fd', 0.2); document.getElementById('solve').click();
        document.getElementById('play').click();
        set('seek', 1500);
        const ds = Sim.data.ds, w = ds.get('box_w'), L = 62, R = w - 20, t0 = ds.get('win_t0'), Tw = ds.get('win_T');
        const c = document.createElement('canvas').getContext('2d'); c.font = Sim.theme.mono;
        const x20 = L + (20 - t0) / Tw * (R - L), w20 = c.measureText('20').width, wts = c.measureText('t (s)').width;
        return { box_w: w, R, t0, Tw, x_tick20: x20, drawn: x20 < R - 34, label20_right: x20 + w20 / 2, ts_left: R - wts, overlap_px: x20 + w20 / 2 - (R - wts) };
    });
    console.log(JSON.stringify(out));
    await b.close(); server.close();
})();
