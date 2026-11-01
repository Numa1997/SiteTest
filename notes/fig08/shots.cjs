// Screenshots of the edited paragraphs of the Fig. 8 note, found by their text. Run: node notes/fig08/shots.cjs [/tmp/fig08-dist]
'use strict';
const http = require('http'), fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = process.argv[2] || '/tmp/fig08-dist', SHOTS = process.env.SHOTS || '/tmp/fig08-shots';
fs.mkdirSync(SHOTS, { recursive: true });
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp' };
const server = http.createServer((req, res) => { const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(d); }); });
(async () => {
    await new Promise(r => server.listen(0, r));
    const url = 'http://127.0.0.1:' + server.address().port + '/simulations/draw-decompose.html';
    const browser = await chromium.launch();
    for (const [w, h] of [[1440, 900], [390, 844]]) {
        const page = await browser.newPage({ viewport: { width: w, height: h } });
        await page.goto(url, { waitUntil: 'load' });
        await page.waitForTimeout(1500);
        for (const [k, t] of Object.entries({ s2: 'equivalence is not exact', s41: 'trading places', fig3: 'still left to add', s61: 'quarter loop apart', eight: 'seven to nine times smaller', refs: 'readable online' })) {
            const el = page.locator('#paper p, #paper figcaption, #paper li').filter({ hasText: t }).first();
            await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(150);
            await el.screenshot({ path: path.join(SHOTS, w + '-' + k + '.png') });
        }
        await page.close();
    }
    await browser.close(); server.close();
})();
