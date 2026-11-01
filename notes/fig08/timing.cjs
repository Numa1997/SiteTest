// Fig. 8 section 4.3: time of one decomposition (a preset click) in fresh pages, first and later clicks, 1440 x 900.
'use strict';
const http = require('http'), fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = process.argv[2] || '/tmp/fig08-dist';
const server = http.createServer((req, res) => { const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': p.endsWith('.html') ? 'text/html' : p.endsWith('.js') ? 'text/javascript' : p.endsWith('.css') ? 'text/css' : 'application/octet-stream' }); res.end(d); }); });
(async () => {
    await new Promise(r => server.listen(0, r));
    const url = 'http://127.0.0.1:' + server.address().port + '/simulations/draw-decompose.html';
    const browser = await chromium.launch();
    const runs = [];
    for (let r = 0; r < 5; r++) {
        const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
        await page.goto(url, { waitUntil: 'load' });
        await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds && Sim.data.ds.dims.k === 120);
        runs.push(await page.evaluate(() => ['square', 'heart', 'star', 'eight', 'heart', 'heart'].map(s => { const t0 = performance.now(); document.querySelector('[data-shape="' + s + '"]').click(); return +(performance.now() - t0).toFixed(1); })));
        await page.close();
    }
    console.log(JSON.stringify(runs));
    await browser.close(); server.close();
})();
