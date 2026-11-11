// The numbers of the step-by-step passages added to sections 6.3, 6.4, 9, 10.1, 10.2 and 10.3 (11 November 2026), from the model and
// its stored runs. checks/check_numbers.cjs recomputes them.   node derive/examples2.cjs
'use strict';
const P = require('../physics.cjs'), fs = require('fs'), path = require('path');
const D = f => JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', f)));
const A = P.air(283.15, 85000), g = 9.81, RW = 1000, T = A.T, kB = P.K_B, sig = P.sigmaWater(T);
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const e = (x, d) => x.toExponential(d === undefined ? 3 : d), f = (x, d) => x.toFixed(d);
const modeMass = md => md.N * 4 / 3 * Math.PI * RW * Math.pow(md.rg, 3) * Math.exp(4.5 * Math.log(md.sg) ** 2);
const tab = D('etab_warm.json'), S = D('stochastic.json'), B = D('bridge.json').s16;

// ---- 6.3, example: capture alone
{ const Wd = modeMass(modes[0]), R0 = 40e-6 * 1.2 ** 3, n = (100 ** 3 - 69 ** 3) / 512;
  const rate = RR => P.tableE(tab, RR, 8e-6 / RR, 'clamp') * Math.PI * (RR + 8e-6) ** 2 * (P.vBeard(RR, A) - P.vBeard(8e-6, A)) * Wd / (4 * Math.PI * RR * RR * RW);
  let R = 69e-6, t = 0; const h = 0.05; while (R < 100e-6) { R += h * rate(R); t += h; }
  console.log(`6.3  largest collector ${f(R0 * 1e6, 2)} um; droplet water W_d = ${e(Wd)} kg/m3; dR/dt at 69 um ${f(rate(69e-6) * 1e6 * 60, 3)} um/min (E ${f(P.tableE(tab, 69e-6, 8 / 69, 'clamp'), 3)}, dv ${f(P.vBeard(69e-6, A) - P.vBeard(8e-6, A), 4)}), at 100 um ${f(rate(100e-6) * 1e6 * 60, 3)} um/min; time ${f(t, 0)} s; captures ${f(n, 1)}; relative spread 1/sqrt(n) = ${f(100 / Math.sqrt(n), 1)} %`); }
// ---- 6.3, (6.1) evaluated
{ const at = V => { let mx = 0; for (let i = 0; i < B.t.length; i++) { mx = Math.max(mx, B.N100[i]); if (V * mx >= Math.LN2) return B.t[i]; } return null; };
  console.log(`6.3  n100 needed: 1 m3 ${f(Math.LN2, 3)}, 1000 cm3 ${f(Math.LN2 / 1e-3, 0)}, 100 cm3 ${f(Math.LN2 / 1e-4, 0)} per m3; reached at ${at(1)} s, ${at(1e-3)} s, ${at(1e-4)} s (16 bins per doubling, records every 5 s)`);
  const i = B.t.indexOf(175); console.log(`     at 175 s: n100 = ${f(B.N100[i], 1)} per m3`); }
// ---- 6.4: pair counts and the mean field at 10 min
{ for (const V of [1, 10, 100, 1000]) { const n = Math.round(1e6 * V * 1e-6); console.log(`6.4  ${V} cm3: ${n} collectors; exact pairs ${n * (n - 1) / 2}, mean field ${n * n / 2}; ratio ${f((n - 1) / n, 3)}`); }
  const i600 = B.t.indexOf(600); console.log(`     collection equation (truncated modes, 16 bins per doubling): F40 at 600 s = ${f(B.F40[i600], 3)}; at 0: ${f(B.F40[0], 3)}`);
  const F10 = V => S.V[V].reduce((a, q) => a + q.F40[10], 0) / S.V[V].length, F0 = V => S.V[V].reduce((a, q) => a + q.F40[0], 0) / S.V[V].length;
  console.log(`     exact, average F40 at 0: ${['1', '10', '100', '1000'].map(F0).map(v => f(v, 3)).join(', ')}; at 10 min: ${['1', '10', '100', '1000'].map(F10).map(v => f(v, 3)).join(', ')}`);
  const share = S.V['1'].filter(q => q.F40[0] > 0).length / S.V['1'].length; console.log(`     1 cm3: share of runs whose collector starts >= 40 um ${f(share, 3)} (${S.V['1'].length} runs)`);
  // expected F40(0) in 1 cm3 from the cut lognormal: E[r^3 ; r >= 40]/(E water per cm3)
  const nz = 200000; let s3 = 0, s3h = 0, sw = 0, ls = Math.log(1.2);
  for (let i = 0; i < nz; i++) { const z = -3 + 6 * (i + 0.5) / nz, w = Math.exp(-z * z / 2), r3 = Math.exp(3 * ls * z); sw += w; s3 += w * r3; if (z >= 0) s3h += w * r3; }
  const mc = 4 / 3 * Math.PI * RW * (40e-6) ** 3 * s3 / sw, mch = 4 / 3 * Math.PI * RW * (40e-6) ** 3 * s3h / sw;
  const nzd = 200000; let sd = 0, swd = 0; const lsd = Math.log(1.25); for (let i = 0; i < nzd; i++) { const z = -3 + 6 * (i + 0.5) / nzd, w = Math.exp(-z * z / 2); swd += w; sd += w * Math.exp(3 * lsd * z); }
  const md = 300 * 4 / 3 * Math.PI * RW * (8e-6) ** 3 * sd / swd;
  console.log(`     cut modes per cm3: droplet water ${e(md)} kg, collector water ${e(mc)} kg (above 40 um part ${e(mch)}); F40(0) of the mean field ${f(mc * 0 + mch / (md + mc), 3)}; if the collector is always present ${f(mc / (md + mc), 3)}`); }
// ---- chapter 9: condensation in rising saturated air
{ const T0 = T, p0 = A.p, Rd = 287.05, Rv = 461.5, cp = 1005, L = 2.477e6, eps = Rd / Rv, es = 611.2 * Math.exp(17.67 * (T0 - 273.15) / (T0 - 29.65));
  const qs = eps * es / (p0 - es), Gm = g * (1 + L * qs / (Rd * T0)) / (cp + L * L * qs * eps / (Rd * T0 * T0)), dqdz = (cp * Gm - g) / L, rho = A.rho;
  console.log(`9    e_s ${f(es, 1)} Pa, q_s ${f(qs * 1e3, 3)} g/kg, dry lapse ${f(g / cp * 1e3, 2)} K/km, moist lapse ${f(Gm * 1e3, 2)} K/km; dq_s/dz ${f(dqdz * 1e6, 3)} g/kg per km; condensed ${f(-rho * dqdz * 1e6, 3)} g/m3 per km; at 0.5 and 2 m/s: ${f(-rho * dqdz * 0.5 * 60 * 1e3, 3)} and ${f(-rho * dqdz * 2 * 60 * 1e3, 3)} g/m3 per min`);
  const EN = D('energy.json'), wr = EN.warm.recs, W0 = EN.warm.W0;
  const r60 = wr.find(q => q.t === 60), F0 = wr[0].wat[1] + wr[0].wat[2], F60 = r60.wat[1] + r60.wat[2];
  console.log(`     collection in the first minute moves ${f((F60 - F0) * 1e3, 3)} g/m3 into the collector and drizzle classes (W0 ${f(W0 * 1e3, 3)} g/m3)`); }
// ---- 10.1: one capture, and F_s at the start
{ const A4 = r => 4 * Math.PI * r * r, R = 40e-6, r = 8e-6, Rn = Math.cbrt(R ** 3 + r ** 3), dA = A4(R) + A4(r) - A4(Rn), dF = sig * dA;
  const m1 = P.massOf(R), m2 = P.massOf(r), cke = 0.5 * m1 * m2 / (m1 + m2) * (P.vBeard(R, A) - P.vBeard(r, A)) ** 2;
  console.log(`10.1 capture: R_new ${f(Rn * 1e6, 4)} um; surfaces ${e(A4(R))} + ${e(A4(r))} -> ${e(A4(Rn))} m2; destroyed ${e(dA)} m2 = ${f(100 * dA / A4(r), 1)} % of the droplet's; dF ${e(dF)} J; CKE ${e(cke)} J; ratio ${f(dF / cke, 0)}; series 1 - 2/3 p + p^4/9 at p = 0.2: ${f(100 * (1 - 2 / 3 * 0.2 + 0.2 ** 4 / 9), 2)} %`);
  const r2 = md => md.N * 4 * Math.PI * md.rg ** 2 * Math.exp(2 * Math.log(md.sg) ** 2), Fd = sig * r2(modes[0]), Fc = sig * r2(modes[1]);
  console.log(`     F_s(0) smooth modes: droplets ${e(Fd)} J/m3 (<r^2> = ${f(Math.sqrt(r2(modes[0]) / modes[0].N / (4 * Math.PI)) * 1e6, 3)} um squared-mean radius), collectors ${e(Fc)}; total ${f(Fd + Fc, 4)}, droplet share ${f(100 * Fd / (Fd + Fc), 1)} %; exp(2 ln^2 1.25) = ${f(Math.exp(2 * Math.log(1.25) ** 2), 4)}`);
  const EN = D('energy.json'); console.log(`     stored: E_s0 ${f(EN.warm.Es0, 5)} J/m3; rises ${EN.warm.rises}`); }
// ---- 10.2: the heat of one capture
{ const dsdT = (P.sigmaWater(T + 0.01) - P.sigmaWater(T - 0.01)) / 0.02, us = sig - T * dsdT, A4 = r => 4 * Math.PI * r * r, R = 40e-6, r = 8e-6, dA = A4(R) + A4(r) - A4(Math.cbrt(R ** 3 + r ** 3));
  const Q = us * dA, m = P.massOf(R) + P.massOf(r), nuw = 1.307e-6;
  console.log(`10.2 dsigma/dT ${e(dsdT)} N/(m K); -T dsigma/dT ${f(-T * dsdT, 4)}; u_s ${f(us, 4)} J/m2 (${f(us / sig, 3)} sigma); Q ${e(Q)} J; m ${e(m)} kg; dT ${e(Q / (m * 4192))} K; Lamb r^2/(5 nu_w) at 40 um ${e(R * R / (5 * nuw))} s; entropy sigma dA/T ${e(sig * dA / T)} J/K = ${e(sig * dA / T / kB)} k_B; air gains ${e(Q / T)}, surface takes ${e(-dsdT * dA)}`);
  const EN = D('energy.json'); console.log(`     gravity at start Pg0 ${e(EN.warm.Pg0)} W/m3; rho_a eps ${e(A.rho * 1e-2)} W/m3; E_s0/Pg0 ${f(EN.warm.Es0 / EN.warm.Pg0, 1)} s; collector share of Pg0: ${(() => { const gr = P.makeGrid(8, 4e-3), N = P.lognormalBins(gr, [modes[1]]), gs = g * (1 - A.rho / RW); let p = 0; N.forEach((n, k) => p += n * gr.x[k] * gs * P.vBeard(gr.r[k], A)); return f(100 * p / EN.warm.Pg0, 1); })()} %`); }
// ---- 10.3: the translational entropy of a droplet
{ const h = 6.62607015e-34, m8 = P.massOf(8e-6), lam = h / Math.sqrt(2 * Math.PI * m8 * kB * T), n = 301e6, x = 1 / (n * lam ** 3);
  console.log(`10.3 m ${e(m8)} kg; 2 pi m kB T ${e(2 * Math.PI * m8 * kB * T)}; lambda ${e(lam)} m; volume per drop 1/n ${e(1 / n)} m3 (a cube of ${f(Math.cbrt(1 / n) * 1e6, 0)} um); lambda^3 ${e(lam ** 3)}; ratio ${e(x)}; ln ${f(Math.log(x), 2)}; + 5/2 = ${f(Math.log(x) + 2.5, 2)}; surface entropy of the capture / this ${e(1.32e10 / (Math.log(x) + 2.5), 2)}`); }
