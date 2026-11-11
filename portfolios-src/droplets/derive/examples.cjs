// The numbers of the worked examples ("Example n.k") and method boxes in the lecture notes, each computed by the model's own
// functions. checks/check_numbers.cjs recomputes them and finds each in the text.
//   node derive/examples.cjs
'use strict';
const P = require('../physics.cjs'), fs = require('fs'), path = require('path');
const A = P.air(283.15, 85000), g = 9.81, rw = 1000;
const e = (x, d) => x.toExponential(d === undefined ? 3 : d), f = (x, d) => x.toFixed(d);
const out = {};

// ---- Example 1.1: one collector from 40 to 100 um
{ const k = P.stokesK(A), m8 = P.massOf(8e-6), W = 300e6 * m8, c = k * W / (4 * rw), R0 = 40e-6, ts = 1 / (c * R0);
  console.log(`1.1  rho_a ${f(A.rho, 4)}, mu ${e(A.mu)}; k = ${e(k, 4)}; m(8 um) = ${e(m8)} kg; W = ${e(W)} kg/m3; c = ${f(c, 2)} /m/s; t* = ${f(ts, 0)} s = ${f(ts / 60, 2)} min`);
  console.log(`     (1.3): t(100) = t*(1 - 0.4) = ${f(ts * 0.6 / 60, 2)} min; F(100) = ${f(P.L0F(100e-6, 8e-6), 1)} /m, F(40) = ${f(P.L0F(40e-6, 8e-6), 1)} /m, difference ${f(P.L0F(100e-6, 8e-6) - P.L0F(40e-6, 8e-6), 1)}; 4 rho/(kW) = ${f(4 * rw / (k * W), 5)} m s; t = ${f(P.L0time(40e-6, 100e-6, 8e-6, W, A) / 60, 2)} min; -1/R: ${f(-1 / 100e-6 + 1 / 40e-6, 0)}`); }

// ---- Example 2.1: the fall speed of a 40 um and an 8 um drop, as vBeard computes it
{ const B2 = [-3.18657, 0.992696, -1.53193e-3, -9.87059e-4, -5.78878e-4, 8.55176e-5, -3.27815e-6];
  const lam = 6.62e-8 * (A.mu / 1.818e-5) * (101325 / A.p) * Math.sqrt(A.T / 293.15);
  for (const a of [40e-6, 100e-6]) { const d = 2 * a, NDa = 4 * A.rho * (rw - A.rho) * g / (3 * A.mu * A.mu) * d ** 3, X = Math.log(NDa); let Y = 0; for (let k = 6; k >= 0; k--) Y = Y * X + B2[k];
    const csc = 1 + 2.51 * lam / d, Re = csc * Math.exp(Y), v = A.mu * Re / (A.rho * d);
    console.log(`2.1  a = ${a * 1e6} um: N_Da = ${f(NDa, 2)}, X = ${f(X, 3)}, sum = ${f(Y, 4)}, slip ${f(csc, 4)}, Re = ${f(Re, 3)}, v = ${f(v, 4)} m/s (vBeard ${f(P.vBeard(a, A), 4)}); Stokes: Re_S = N_Da/24 = ${f(NDa / 24, 3)}, v_S = ${f(P.vStokes(a, A), 4)}`); }
  const a = 8e-6, d = 2 * a, csc = 1 + 2.51 * lam / d;
  console.log(`2.1  mean free path ${e(lam)} m; 8 um: Stokes ${e(P.vStokes(a, A), 4)} m/s, slip factor ${f(csc, 4)}, v = ${e(P.vBeard(a, A), 4)} m/s`); }

// ---- Example 3.1: the collision efficiency of 40 um on 8 um, as pairEfficiency computes it
{ const R = 40e-6, r = 8e-6, U = P.vBeard(R, A), vr = P.vBeard(r, A), gs = g * (1 - A.rho / rw), tau = vr / gs, St = tau * U / R, S = vr / U, p = r / R, Re = 2 * R * A.rho * U / A.mu;
  const es = P.flowEfficiency('stokes', St, S, p, 200), ep = P.flowEfficiency('potential', St, S, p, 30), E = (es.E + ep.E * Re / 60) / (1 + Re / 60);
  console.log(`3.1  U = ${f(U, 4)}, v(r) = ${e(vr, 3)}, g* = ${f(gs, 4)}, tau = ${e(tau)} s, stopping distance tau U = ${f(tau * U * 1e6, 1)} um, St = ${f(St, 3)}, S = ${f(S, 4)}, p = ${p}, Re = ${f(Re, 3)}`);
  console.log(`     creeping: b_c = ${f(es.bc, 4)} R, E_S = ${f(es.E, 4)} (plain b_c^2/(1+p)^2 = ${f(es.bc ** 2 / (1 + p) ** 2, 4)}); potential: b_c = ${f(ep.bc, 4)}, E_P = ${f(ep.E, 4)} (plain ${f(ep.bc ** 2 / (1 + p) ** 2, 4)}); weight Re/60 = ${f(Re / 60, 4)}; E = ${f(E, 4)}; pairEfficiency ${f(P.pairEfficiency(R, r, A).E, 4)}`);
  // how many trajectories does the bisection take
  console.log(`     bisection: bracket 1.5(1+p) = ${f(1.8, 2)} halved until below 1e-7 (1+p): ${Math.ceil(Math.log2(1.5 / 1e-7))} halvings`); }

// ---- Example 4.1: Weber number of 40 on 8, and of 500 on 250
{ const sig = P.sigmaWater(A.T);
  for (const [a1, a2] of [[40e-6, 8e-6], [500e-6, 250e-6]]) { const m1 = P.massOf(a1), m2 = P.massOf(a2), mr = m1 * m2 / (m1 + m2), dv = P.vBeard(a1, A) - P.vBeard(a2, A), cke = 0.5 * mr * dv * dv, dc = 2 * Math.cbrt(a1 ** 3 + a2 ** 3), Es = Math.PI * sig * dc * dc, We = cke / Es;
    console.log(`4.1  ${a1 * 1e6}/${a2 * 1e6} um: m1 ${e(m1)}, m2 ${e(m2)}, mu_red ${e(mr)} kg, dv ${f(dv, 4)} m/s, CKE ${e(cke)} J, d_c ${f(dc * 1e6, 2)} um, pi sigma d_c^2 ${e(Es)} J, We ${e(We)}, E_coal ${f(Math.exp(-1.15 * We), 5)}; sigma ${f(sig, 5)}`); } }

// ---- Example 5.1: one pair of bins in one step of the scheme (8 bins per doubling, dt = 1 s)
{ const gr = P.makeGrid(8, 4e-3), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }], N = P.lognormalBins(gr, modes);
  const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json'))), ext = { speed: 'beard', eff: 'table', coal: 'law', tab };
  const i = 72, j = gr.r.findIndex(r => r >= 40e-6), K = P.kernel(gr.r[i], gr.r[j], A, ext), C = K * N[i] * N[j], xs = gr.x[i] + gr.x[j];
  let kk = j; while (gr.x[kk + 1] <= xs) kk++; const fr = (xs - gr.x[kk]) / (gr.x[kk + 1] - gr.x[kk]);
  console.log(`5.1  grid: n = ${gr.n} bins, x0 = ${e(gr.x[0])} kg, ratio of neighbouring radii 2^(1/24) = ${f(Math.pow(2, 1 / 24), 4)}; bin i = ${i}: r = ${f(gr.r[i] * 1e6, 3)} um, N_i = ${e(N[i])} /m3; bin j = ${j}: r = ${f(gr.r[j] * 1e6, 3)} um, N_j = ${e(N[j])} /m3`);
  console.log(`     K_ij = ${e(K)} m3/s (E = ${f(P.tableE(tab, gr.r[j], gr.r[i] / gr.r[j]), 4)}, dv = ${f(P.vBeard(gr.r[j], A) - P.vBeard(gr.r[i], A), 4)}); C = ${e(C)} mergers/m3 in 1 s = ${f(100 * C / N[j], 3)} % of N_j, ${e(C / N[i], 2)} of N_i; x* = x_i + x_j: r* = ${f(P.radiusOf(xs) * 1e6, 3)} um, between bin ${kk} (${f(gr.r[kk] * 1e6, 3)} um) and ${kk + 1} (${f(gr.r[kk + 1] * 1e6, 3)} um); f = ${f(fr, 4)}; x_i/x_j = ${f(gr.x[i] / gr.x[j], 5)}; (x_k+1 - x_k)/x_k = ${f(Math.pow(2, 1 / 8) - 1, 4)}`);
  console.log(`     net loss from bin j: f C = ${e(fr * C)} /m3; a collector in bin j catches ${f(K * N[i], 4)} droplets of bin i per second`); }

// ---- Example 6.1: the exact process in 10 cm^3 at the start
{ const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }], tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json'))), ext = { speed: 'beard', eff: 'table', coal: 'law', tab };
  const u = P.rng(1), rad = P.drawModes(modes, 10, u, 3), n = rad.length, V = 10e-6; let a0 = 0, acc = 0, add = 0, nc = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) { const K = P.kernel(rad[i], rad[j], A, ext) / V; a0 += K; const big = Math.max(rad[i], rad[j]) >= 20e-6, both = Math.min(rad[i], rad[j]) >= 20e-6; if (both) acc += K; else if (!big) add += K; }
  rad.forEach(r => { if (r >= 20e-6) nc++; });
  console.log(`6.1  10 cm3, seed 1: ${n} drops (${nc} collectors), ${n * (n - 1) / 2} pairs; total rate a0 = ${f(a0, 3)} /s, mean wait ${f(1 / a0, 3)} s; collector-collector share ${e(acc / a0, 2)}, droplet-droplet ${e(add / a0, 2)}; one collector-collector merger every ${f(1 / acc, 0)} s`);
  out.g = { a0, n, nc }; }

// ---- Example 7.1: Ayala's formula at eps = 100 cm2/s3 for 40 on 8
{ const a1 = 40e-6, a2 = 8e-6, eps = 1e-2, t1 = P.vBeard(a1, A) / g, t2 = P.vBeard(a2, A) / g, v1 = P.vBeard(a1, A), v2 = P.vBeard(a2, A), R = a1 + a2, nu = A.nu;
  const a0 = (11 + 7 * 2e4) / (205 + 2e4), tk = Math.sqrt(nu / eps), vk = Math.pow(nu * eps, 0.25), d = t1 - t2;
  const sh = R * R * eps / (15 * nu), ac = d * d * a0 * (vk / tk) ** 2, se = (v1 * t1 - v2 * t2) ** 2 * 2 * eps / (15 * nu), gr = Math.PI / 8 * d * d * g * g;
  const w = Math.sqrt(2 / Math.PI) * Math.sqrt(sh + ac + se + gr), wg = 0.5 * Math.abs(d) * g;
  console.log(`7.1  nu = ${e(nu)}, tau_K = ${f(tk * 1e3, 1)} ms, tau1 = ${f(t1 * 1e3, 2)} ms, tau2 = ${f(t2 * 1e3, 3)} ms; shear ${e(sh, 2)}, accel ${e(ac, 2)}, settling ${e(se, 2)}, gravity term ${e(gr, 2)} (m/s)^2; sigma_w = ${f(Math.sqrt(sh + ac + se) * 100, 2)} cm/s; <|w_r|> = ${f(w * 100, 3)} cm/s against still air ${f(wg * 100, 3)} cm/s; factor ${f(w / wg, 4)} (ayalaFactor ${f(P.ayalaFactor(a1, a2, A, eps), 4)}); acceleration scale eps^(3/4) nu^(-1/4) = ${f(Math.pow(eps, 0.75) * Math.pow(nu, -0.25), 2)} m/s2; (vk/tk)^2 = ${e((vk / tk) ** 2, 2)}`); }

// ---- Example 11: maximum entropy numbers at the start (N, M, mean mass)
{ const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }], gr = P.makeGrid(8, 4e-3), N = P.lognormalBins(gr, modes); let Nt = 0, M = 0; N.forEach((n, k) => { Nt += n; M += n * gr.x[k]; });
  console.log(`11   start: N = ${e(Nt)} /m3, M = ${e(M)} kg/m3, mean mass ${e(M / Nt)} kg = a sphere of ${f(P.radiusOf(M / Nt) * 1e6, 2)} um; beta = N/M = ${e(Nt / M)} /kg`); }

// ---- Example 12.1: one super-droplet pair in one step
{ const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json'))), ext = { speed: 'beard', eff: 'table', coal: 'law', tab };
  const dV = 50 ** 3, xid = 300e6 * dV / 96, xic = 1e6 * dV / 32, n = 128, K = P.kernel(40e-6, 8e-6, A, ext), sc = n * (n - 1) / 2 / Math.floor(n / 2), p = xid * K * 1 / dV * sc;
  console.log(`12.1 dV = ${e(dV)} m3; xi droplets ${e(xid)}, collectors ${e(xic)}; K(40,8) = ${e(K)} m3/s; pairs ${n * (n - 1) / 2}, tested ${Math.floor(n / 2)}, factor ${sc}; xi_j K dt/dV = ${e(xid * K / dV)}; p = ${f(p, 4)}; rNew for gamma = 1: ${f(Math.cbrt(40 ** 3 + 8 ** 3), 3)} um; real mergers per event xi_k = ${e(xic)}; ratio xi_j/xi_k = ${f(xid / xic, 0)}`);
  const s2 = Math.pow(1e-2 * 100, 2 / 3), TL = 2 * s2 / (6 * 1e-2), a = Math.exp(-1 / TL), b = Math.sqrt(s2 * (1 - a * a));
  console.log(`     OU step, dt = 1 s: sigma = ${f(Math.sqrt(s2), 3)} m/s, T_L = ${f(TL, 2)} s, memory factor ${f(a, 4)}, kick ${f(b, 4)} m/s; evaporation of a 100 um drop in 1 s outside: r^2 changes by ${e(2 * P.growthG(A) * -0.2 * P.ventilation(100e-6, A))} m2, r by ${f((Math.sqrt(1e-8 + 2 * P.growthG(A) * -0.2 * P.ventilation(100e-6, A)) - 1e-4) * 1e9, 2)} nm`); }
