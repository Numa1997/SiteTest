// The machine in still glycerol (or MED), the page's glycerol gains, sampled every 10 ms; prints the books.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../waterlily/pageparams.json');
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), U = +(process.env.U || 0), dur = +(process.env.DUR || 4);
const Kg = P[med].K, mach = { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med };
const w = new T.World({ dx, U, machine: mach, s: [0, +(process.env.TH1 || 0.08), +(process.env.TH2 || -0.05), 0, 0, 0], nsub: 5 });
let uh = 0, tNext = 0; const ctrl = (s, t) => { if (t >= tNext - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tNext += 0.01; } return uh; };
const p = w.mp, E0 = T.energy(p, w.s) , KE0 = w.KE(); let t0 = Date.now();
const P0 = w.momX() + T.momX(p, w.s);
for (let n = 1; n * 0.005 <= dur + 1e-9; n++) {
  w.step(ctrl);
  if (n % 40 === 0) { const B = w.book, E = T.energy(p, w.s), KE = w.KE();
    // energy book: motor work = Δ(machine E) + Δ(fluid KE) + rod dissipation below grid - (fluid KE changes by operator that are not physical exchanges)
    console.log(JSON.stringify({ t: +w.t.toFixed(2), x: +w.s[0].toFixed(4), th1: +w.s[1].toFixed(4), th2: +w.s[2].toFixed(4), u: +w.u_m.toFixed(2), Fc: +w.Fc.toFixed(3), Kx: +w.Kx.toFixed(1), its: [w.its0, w.itsx], div: +w.maxDiv().toExponential(1),
      Wm: +B.Wm.toFixed(4), dEm: +(E - E0).toFixed(4), dKEf: +(KE - KE0).toFixed(4), Drod: +B.Drod.toFixed(4), Eadv: +B.Eadv.toFixed(4), Ediff: +B.Ediff.toFixed(4), Eproj: +B.Eproj.toFixed(4), Erod: +B.Erod.toFixed(4), Ecart: +B.Ecart.toFixed(4),
      umax: +Math.max(...w.u.map(Math.abs)).toFixed(3), ms: +((Date.now() - t0) / n).toFixed(1) })); }
  if (!(Math.abs(w.s[1]) < 1.5)) { console.log('fell/NaN at', w.t); break; }
}
