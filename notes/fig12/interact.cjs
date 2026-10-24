// Fig. 12 interaction test: a scripted drag of the pendulum returns to the goal; hovering with Read values off changes nothing.
// Usage: node notes/fig12/interact.cjs [width] [lang]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const W = +(process.argv[2] || 1400), lang = process.argv[3] || '', port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: 1000 } });
  const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()); });
  await page.goto(`http://localhost:${port}/${lang ? lang + '/' : ''}simulations/furuta-pendulum.html`, { waitUntil: 'load' });
  await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('basin_n') > 0, null, { timeout: 30000 });
  // go to the end of the run: the pendulum is up and caught
  await page.evaluate(() => { const s = document.getElementById('seek'); s.value = 1900; s.dispatchEvent(new Event('input')); document.getElementById('play').click(); });
  const g = k => page.evaluate(k => Sim.data.ds.get(k), k);
  const before = { al: await g('al_now'), caught: await g('caught_now') };
  // hover with Read values off: sweep the pointer across the rig; nothing may change
  const rig = await page.$('#rig'); await rig.scrollIntoViewIfNeeded(); let bb = await rig.boundingBox();
  const shot0 = await rig.screenshot();
  for (let k = 0; k <= 30; k++) await page.mouse.move(bb.x + bb.width * k / 30, bb.y + bb.height * 0.4 + 30 * Math.sin(k));
  const shot1 = await rig.screenshot();
  const same = Buffer.compare(shot0, shot1) === 0;
  bb = await rig.boundingBox();
  // grab the knob, push the pendulum 50° over, hold, let go
  const ex = await g('end_px'), ey = await g('end_py'), tx = await g('tip_px'), ty = await g('tip_py');
  console.log('knob', ex, ey, 'bb', JSON.stringify(bb), await page.evaluate(([x, y]) => { const e = document.elementFromPoint(x, y); return e ? e.tagName + '#' + e.id + '.' + e.className : null; }, [bb.x + ex, bb.y + ey]));
  await page.mouse.move(bb.x + ex, bb.y + ey); await page.mouse.down();
  for (let k = 1; k <= 12; k++) { await page.mouse.move(bb.x + ex + (k / 12) * 0.75 * (tx - ex + 220), bb.y + ey + (k / 12) * 0.6 * (ty - ey)); await page.waitForTimeout(30); }
  await page.waitForTimeout(300);
  const held = { what: await g('grabbed'), al: await g('al_now') };
  await page.mouse.up(); await page.waitForTimeout(400);
  const after = await page.evaluate(() => { const d = Sim.data.ds; return { released: d.get('released'), y0: Array.from(d.get('y0s')), t_catch: d.get('t_catch'), t_settle: d.get('t_settle'), alEnd: d.get('al')[2000], phEnd: d.get('ph')[2000], phs: d.get('phs'), status: document.getElementById('status').textContent }; });
  const wrap = a => a - 2 * Math.PI * Math.floor((a + Math.PI) / (2 * Math.PI));
  const ok = same && held.what !== 'nothing' && Math.abs(wrap(held.al)) > 0.3 && after.released && isFinite(after.t_settle) && Math.abs(wrap(after.alEnd)) < 0.01 && Math.abs(wrap(after.phEnd - after.phs)) < 0.01;
  console.log(JSON.stringify({ W, lang, hoverUnchanged: same, before, held, after, errs }, null, 0));
  console.log(ok ? 'PASS drag returns to the goal; hover changes nothing' : 'FAIL');
  await page.screenshot({ path: path.join(__dirname, `shots/after-drag-${W}${lang ? '-' + lang : ''}.png`), fullPage: false });
  await browser.close(); server.close(); process.exit(ok ? 0 : 1);
})();
