// The swing-up in a liquid, in the running page: set a machine and motor (MACH m0/m1/m2/L1/L2/F), a medium, press "Swing up from hanging",
// then report t, x, θ1, θ2 (deg, wrapped), mode every second, and the supervisor's log. Screenshots with SHOT=<prefix>.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const med of (process.env.MEDS || 'water').split(',')) {
    const pg = await b.newPage({ viewport: { width: +(process.env.W || 1100), height: 900 } });
    await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await pg.evaluate(([mach, m]) => { const [m0, m1, m2, L1, L2, F] = mach.split('/').map(Number), set = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); };
      set('m0', m0); set('m1', m1); set('m2', m2); set('L1', L1); set('L2', L2); set('Fmax', F);
      const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); }; e('med', m); }, [process.env.MACH || '1.5/2/2/0.2/0.25/200', med]);
    await pg.waitForTimeout(2500); await pg.click('#swing'); const tr = [];
    for (let i = 0; i < +(process.env.N || 20); i++) { await pg.waitForTimeout(1000);
      if (process.env.SHOT && (i === 3 || i === +(process.env.N || 20) - 1)) await pg.screenshot({ path: `${process.env.SHOT}-${med}-${i}.png` });
      if (process.env.GO && i === +process.env.GOAT) await pg.click('button[data-go="' + process.env.GO + '"]');
      tr.push(await pg.evaluate(() => [DIPC.t.toFixed(1), DIPC.s[0].toFixed(2), (DIPC.ds.get('th1w') * 57.3).toFixed(1), (DIPC.ds.get('th2w') * 57.3).toFixed(1), DIPC.mode, DIPC.W().toFixed(2), DIPC.Wred().toFixed(2), (DIPC.cLevel||0).toFixed(3), DIPC.ref.kind].join(' '))); }
    console.log(med, '\n ' + tr.join('\n '), '\n log', JSON.stringify(await pg.evaluate(() => DIPC.log.map(l => [l.ev, +l.t.toFixed(2), l.v]))));
    await pg.close(); }
  await b.close();
})();
