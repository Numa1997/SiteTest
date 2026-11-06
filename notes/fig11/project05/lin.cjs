const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(() => { const s = document.getElementById('med'); s.value = 'honey'; s.dispatchEvent(new Event('change', { bubbles: true }));
    const p = DIPC.p, L = DIPC.linear(p), out = [], o = new Float64Array(6), full = new Float64Array(6);
    for (let j = 0; j < 6; j++) { const x = [0, 0, 0, 0, 0, 0]; x[j] = 1e-5; DIPC.rhsF(p, x, 0, o); const ax = L.A.map(row => row.reduce((t, a, k) => t + a * x[k], 0));
      const rr = DIPC.rhs(p, x, 0, 0); out.push('dir ' + j + ' rhsF ' + Array.from(o).map(v => v.toExponential(2)).join(' ') + ' | A·x ' + ax.map(v => v.toExponential(2)).join(' ') + ' | rhs ' + Array.from(rr).map(v => v.toExponential(2)).join(' ')); }
    return out; });
  console.log(r.join('\n')); await b.close();
})();
