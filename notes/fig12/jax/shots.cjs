// Fig. 12 in JAX: screenshots of the drawing test page (notes/fig12/jax/view-test.html) for given frames of a packed ride.
// Run from the repository root with a static server on port 8765 (python3 -m http.server 8765):
//   node notes/fig12/jax/shots.cjs <ride json path under the root> <out dir> <frame> [<frame> ...]
const { chromium } = require('playwright');
(async () => {
  const [ride, out, ...frames] = process.argv.slice(2);
  const b = await chromium.launch(), p = await (await b.newContext({ viewport: { width: 920, height: 900 }, deviceScaleFactor: 1 })).newPage();
  const errs = []; p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); }); p.on('pageerror', (e) => errs.push(e.message));
  for (const k of frames) {
    await p.goto(`http://localhost:8765/notes/fig12/jax/view-test.html?ride=/${ride}&k=${k}&w=900&h=840&dpr=1`);
    await p.waitForFunction('window.done === true', null, { timeout: 60000 });
    console.log(k, await p.textContent('#log'));
    await p.locator('#cv').screenshot({ path: `${out}/f${String(k).padStart(3, '0')}.png` });
  }
  if (errs.length) console.log('ERRORS', errs);
  await b.close();
})();
