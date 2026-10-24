// L8b: vapour ripening of the warm cloud in a closed saturated volume, the gradient descent of surface free energy.
// Pure water, and drops each holding the salt of a dry ammonium sulfate particle. 10 cm^3 (3010 drops), modes cut at 3 sigma_g.
//   node tools/run_ripening.cjs [--json]      writes data/ripening.json
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const EN = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'energy.json')));
const t50 = EN.warm.t50, t90 = EN.warm.t90;
const recAt = [0, Math.round(t50), Math.round(t90), 1800, 3600, 3 * 3600, 6 * 3600, 12 * 3600, 86400];
// salt: van 't Hoff factor i = 3, M_s = 0.13214 kg/mol, rho_s = 1770 kg/m^3; b = 3 i M_w m_s / (4 pi rho_w M_s)
const bSalt = rd => 3 * 3 * 0.018015 * (4 / 3 * Math.PI * rd ** 3 * 1770) / (4 * Math.PI * 1000 * 0.13214);
const out = { recAt, t50, t90, a: P.kelvinA(A), G: P.growthG(A), bSalt: bSalt(0.05e-6), cases: {} };
for (const [name, bfun] of [['pure', null], ['salt', () => bSalt(0.05e-6)]]) {
  const runs = [];
  for (let s = 1; s <= 3; s++) {
    const u = P.rng(700 + s), radii = P.drawModes(modes, 10, u, 3), t0 = Date.now();
    const R = P.ripen(radii, A, { tEnd: 86400, recAt, b: bfun || undefined });
    runs.push(R.rec.map(q => ({ t: q.t, alive: q.alive, F: q.F / R.rec[0].F, M: q.M, rmean3: q.rmean3,
      r: s === 1 ? q.r.map(v => +(v * 1e6).toFixed(3)) : undefined })));
    console.log(`${name} seed ${700 + s}: ${R.steps} steps [${((Date.now() - t0) / 1000).toFixed(1)} s]: ` + R.rec.map(q => `${(q.t / 60).toFixed(1)} min F ${(q.F / R.rec[0].F).toFixed(3)} n ${q.alive}`).join('; '));
  }
  out.cases[name] = runs;
}
// late-time growth of the cube of the mean radius against Lifshitz-Slyozov-Wagner's (4/9) G a (pure water)
const pr = out.cases.pure[0], i12 = pr.findIndex(q => q.t === 12 * 3600), i24 = pr.findIndex(q => q.t === 86400);
out.lsw = { measured: (pr[i24].rmean3 ** 3 - pr[i12].rmean3 ** 3) / (12 * 3600), theory: 4 / 9 * out.G * out.a };
console.log(`r^3 growth 12-24 h: ${out.lsw.measured.toExponential(3)} m^3/s against LSW (4/9) G a = ${out.lsw.theory.toExponential(3)} (ratio ${(out.lsw.measured / out.lsw.theory).toFixed(2)}); collection lowers F to ${(EN.warm.recs.find(q => Math.abs(q.t - 810) < 6).Es / EN.warm.Es0).toFixed(3)} by t90`);
if (process.argv.includes('--json')) fs.writeFileSync(path.join(__dirname, '..', 'data', 'ripening.json'), JSON.stringify(out));
