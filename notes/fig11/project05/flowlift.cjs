// Numa, 6 Nov 2026: "make the cart too heavy for the flow to move it, but move the arms". Can a flow lift the hanging rods?
// Heavy cart (m0 = 6 kg), motor off (u = 0), rods hanging with a 3° nudge, the page's own rk4 with the full fluid force (35), 30 s.
// Flows typed into "your own field": a stream across (u = U, v = 0) and a stream up (u = 0, v = U). Reports the rods' angles from upright.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const med of (process.env.MEDS || 'water,glycerol,honey').split(',')) for (const [name, fu, fv] of [['across', 'U', '0'], ['up', '0', 'U']]) for (const U of (process.env.US || '0.25,0.5,1,2').split(',').map(Number)) {
    const r = await pg.evaluate(([m, fu, fv, U]) => {
      const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); };
      set('m0', 6, 'input'); set('med', m, 'change'); set('flow', 'own', 'change'); set('own-u', fu, 'input'); set('own-u', fu, 'change'); set('own-v', fv, 'input'); set('own-v', fv, 'change'); set('Uf', U, 'input');
      const p = DIPC.p, deg = a => { a = ((a + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI; return a * 180 / Math.PI; };
      let s = [0, Math.PI - 0.05, Math.PI - 0.05, 0, 0, 0], t = 0; const pts = [], chk = DIPC.fieldV(p.fl.field, 0, -0.5, 0, p.fl.U, p.fl.nu);
      for (let n = 1; n <= 30000; n++) { s = DIPC.rk4(p, s, 0, 0.001, t); t += 0.001; if (n % 5000 === 0) pts.push([+t.toFixed(0), +deg(s[1]).toFixed(0), +deg(s[2]).toFixed(0), +s[0].toFixed(2)]); }
      return JSON.stringify({ field_at_0_m05: chk.map(v => +v.toFixed(2)), pts }); }, [med, fu, fv, U]);
    console.log(med.padEnd(9), name.padEnd(7), 'U', U, r); }
  await b.close();
})();
