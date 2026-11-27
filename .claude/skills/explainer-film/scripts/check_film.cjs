// Load a film page, print its length, scenes, checks and script errors, and save still frames.
//   node check_film.cjs URL OUTDIR [frame numbers ...] [--size 1080x1920]
// The page must be served over HTTP (python3 -m http.server 8766 at the repository root).
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const args = process.argv.slice(2), si = args.indexOf('--size'); let size = '1080x1920';
  if (si >= 0) { size = args[si + 1]; args.splice(si, 2); }
  const [url, outdir, ...frames] = args; const [VW, VH] = size.split('x').map(Number);
  if (!url || !outdir) { console.error('usage: node check_film.cjs URL OUTDIR [frames ...] [--size WxH]'); process.exit(2); }
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: VW, height: VH } }), errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('requestfailed', r => errs.push('request failed: ' + r.url()));
  await p.goto(url + (url.includes('?') ? '&' : '?') + 'film=1', { waitUntil: 'load' });
  await p.waitForFunction(() => window.__ready === true, null, { timeout: 90000 });
  const info = await p.evaluate(() => ({ frames: window.FILM.frames(), scenes: window.FILM.scenes || {}, checks: window.FILM.checks ? window.FILM.checks() : null }));
  console.log(`length: ${info.frames} frames = ${(info.frames / 30).toFixed(1)} s`);
  for (const [k, v] of Object.entries(info.scenes)) console.log(`  scene ${k.padEnd(10)} frames ${String(v[0]).padStart(5)} to ${String(v[1]).padStart(5)}  (${((v[1] - v[0]) / 30).toFixed(1)} s, middle ${Math.round((v[0] + v[1]) / 2)})`);
  let bad = 0;
  if (!info.checks) { console.log('NO CHECKS: the film must provide FILM.checks()'); bad++; }
  else for (const c of info.checks) { console.log(`  ${c.pass ? 'pass' : 'FAIL'}  ${c.name}: ${c.value}`); if (!c.pass) bad++; }
  for (const f of frames.map(Number)) { await p.evaluate(f => window.renderFrame(f), f); await p.screenshot({ path: `${outdir}/c${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 82 }); }
  console.log(`stills saved: ${frames.length}; script errors: ${errs.length ? errs.join(' | ') : 'none'}`);
  await b.close(); process.exit(bad || errs.length ? 1 : 0);
})();
