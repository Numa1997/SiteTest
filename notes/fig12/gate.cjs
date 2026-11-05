// Run the page's own integrator for a scripted shake and dump what SciPy needs. node notes/fig12/gate.cjs <out.json> <shake x|z> <A_mm> <f_Hz|f1|2f1> <seconds>
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [out, shake, A, fq, T] = process.argv.slice(2); const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html'); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(([shake, A, fq, T]) => { const S = window.SLOSH; document.getElementById('play').click();   // pause the live clock
    S.P.shake = shake; S.P.A = A / 1000; const k11 = S.M.findIndex(m => m.m === 1 && m.n === 1);
    S.P.f = fq === 'f1' ? S.omA[k11] / 2 / Math.PI : fq === '2f1' ? S.omA[k11] / Math.PI : +fq;
    S.seed(); S.resetShake(); const t0 = S.t; const NK = S.M.length, a0 = Array.from(S.aO), samples = [];
    // the page's tShake restarts with the button; the gate starts it here by stepping from a fresh shaker clock
    const n = Math.round(T / 1e-3); for (let i = 0; i < n; i++) { S.step(); if ((i + 1) % 100 === 0) samples.push([S.t - t0, Array.from(S.aO)]); }
    return { NK, k11, m: S.M.map(x => x.m), lam: Array.from(S.lamA), Q: Array.from(S.QA), gam: Array.from(S.gam), muf: Array.from(S.muA), sig: S.P.sig, rho: S.P.rho, f: S.P.f, A: S.P.A, shake, a0, samples, tShake0: null };
  }, [shake, +A, fq, +T]); fs.writeFileSync(out, JSON.stringify(r)); await b.close(); })();
