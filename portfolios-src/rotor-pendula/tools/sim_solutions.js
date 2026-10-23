#!/usr/bin/env node
// Computes every number of the worked solutions of rotor_sim.html with the page's own physics block (tools/physics_block.js)
// and writes data/sim_solutions.json: { n: { key: text }, t: { key: table rows (HTML) }, raw: {...} }.
// tools/build_sim.py puts them into the page (<span data-n="key"> and <tbody data-t="key">). Nothing is typed by hand.
// Usage: node tools/sim_solutions.js     (about a minute)
const fs = require('fs');
const path = require('path');
const { loadPhysics } = require('./physics_block');
const { simulate, makeModel, CONST } = loadPhysics();

const n = {}, t = {}, raw = {};
const mW = x => x * 1e3;
const f = (x, d) => { const s = Number(x).toFixed(d); return s.startsWith('-') ? '−' + s.slice(1) : s; };
const sig = (x, k = 3) => {                       // k significant figures, plain notation, Unicode minus
  if (x === 0) return '0';
  const d = Math.max(0, k - 1 - Math.floor(Math.log10(Math.abs(x))));
  return f(x, d);
};
const deg = r => r * 180 / Math.PI;
/** First harmonic of the recorded swing over whole turns: theta ~ a cos(phi) + b sin(phi) + mean = -Theta cos(phi - delta). */
function lagOf(rec) {
  const nn = rec.framesPerTurn * rec.turns;
  let a = 0, b = 0;
  for (let k = 0; k < nn; k++) { a += rec.q1[k] * Math.cos(rec.phi[k]); b += rec.q1[k] * Math.sin(rec.phi[k]); }
  a *= 2 / nn; b *= 2 / nn;
  return { delta: Math.atan2(-b, -a), Theta1: Math.hypot(a, b) };
}
function goldenMax(fn, a, b, tol) {
  const r = (Math.sqrt(5) - 1) / 2, cache = new Map();
  const F = x => { if (!cache.has(x)) cache.set(x, fn(x)); return cache.get(x); };
  let x1 = b - r * (b - a), x2 = a + r * (b - a);
  while (b - a > tol) {
    if (F(x1) < F(x2)) { a = x1; x1 = x2; x2 = a + r * (b - a); } else { b = x2; x2 = x1; x1 = b - r * (b - a); }
  }
  return 0.5 * (a + b);
}
const T0 = Date.now();

// ---- 1. The best brake at 20 rpm, pivot 30 % ---------------------------------------------------------------------------
{
  const base = { rpm: 20, frac: 0.3, pend: 'single' };
  const md = makeModel(base);
  const mults = [];
  for (let i = 0; i <= 20; i++) mults.push(0.3 * Math.pow(10, i / 20));      // 0.3 .. 3, log-spaced
  const sweep = mults.map(m => ({ m, P: simulate({ ...base, brake: m }).P_mean, Pf: md.linearPower(m * md.kappaStar) }));
  const lm = goldenMax(x => simulate({ ...base, brake: Math.exp(x) }).P_mean, Math.log(0.5), Math.log(2), 2e-3);
  const peak = simulate({ ...base, brake: Math.exp(lm) });
  const at1 = simulate({ ...base, brake: 1 });
  const lag = lagOf(at1.rec);
  const p03 = sweep[0].P, p3 = sweep[sweep.length - 1].P;
  const half = sweep.filter(s => s.P >= 0.9 * peak.P_mean);
  Object.assign(n, {
    s1_R: sig(md.R, 4), s1_Rm1: sig(md.R - 1, 4), s1_kstar: sig(md.kappaStar, 4), s1_cstar: sig(md.kappaStar * md.cUnit, 3),
    s1_Om: sig(md.Om, 4), s1_rp: sig(md.rp, 3), s1_G: sig(md.G, 3), s1_Pstar: sig(mW(md.Pstar), 4),
    s1_peak_mult: f(Math.exp(lm), 2), s1_peak_kappa: sig(Math.exp(lm) * md.kappaStar, 3), s1_peak_P: sig(mW(peak.P_mean), 4),
    s1_P1: sig(mW(at1.P_mean), 4), s1_gain: sig((peak.P_mean / at1.P_mean - 1) * 100, 2),
    s1_P03: sig(mW(p03), 3), s1_P3: sig(mW(p3), 3), s1_P03_pct: f(p03 / peak.P_mean * 100, 0), s1_P3_pct: f(p3 / peak.P_mean * 100, 0),
    s1_band_lo: f(half[0].m, 2), s1_band_hi: f(half[half.length - 1].m, 2),
    s1_lag: f(deg(lag.delta), 1), s1_Theta: sig(at1.Theta, 3), s1_Theta_lin: sig(md.G / Math.hypot(md.R - 1, md.kappaStar), 3),
    s1_full_vs_star: sig((at1.P_mean / md.Pstar - 1) * 100, 2),
  });
  t.s1 = sweep.filter((s, i) => i % 4 === 0 || i === sweep.length - 1).map(s =>
    `<tr><td>${f(s.m, 2)} κ*</td><td>${sig(mW(s.Pf), 4)} mW</td><td>${sig(mW(s.P), 4)} mW</td></tr>`).join('');
  raw.s1 = { sweep, peakMult: Math.exp(lm), peakP: peak.P_mean, P1: at1.P_mean, lagDeg: deg(lag.delta) };
}

// ---- 2. The trail is the bill: 8 rpm, pivot 30 % ------------------------------------------------------------------------
{
  const md = makeModel({ rpm: 8, frac: 0.3 });
  const o = simulate({ rpm: 8, frac: 0.3 });
  const { m, L } = CONST.single;
  const Pbill = -m * md.rp * L * md.Om ** 3 * o.trail;
  const trailTheory = -(md.G ** 2) / (4 * md.R * (md.R - 1));
  Object.assign(n, {
    s2_Om: sig(md.Om, 4), s2_rp: sig(md.rp, 4), s2_R: sig(md.R, 4), s2_G: sig(md.G, 3),
    s2_trail: sig(o.trail, 3), s2_trail_deg: f(deg(o.trail), 1), s2_trail_theory: sig(trailTheory, 3),
    s2_P: sig(mW(o.P_mean), 4), s2_Pbill: sig(mW(Pbill), 4), s2_diff: sig(Math.abs(Pbill / o.P_mean - 1) * 100, 2),
    s2_Theta: sig(o.Theta, 3), s2_mrpLO3: sig(m * md.rp * L * md.Om ** 3, 4),
  });
  raw.s2 = { trail: o.trail, P: o.P_mean, Pbill, trailTheory };
}

// ---- 3. One rod or two: the 3/4 rule -------------------------------------------------------------------------------------
{
  const rows = [];
  const { m1, m2, l1, l2 } = CONST.double, M = m1 + m2, lc = (m1 * l1 + m2 * (l1 + l2)) / M, Ip = m1 * l1 * l1 + m2 * (l1 + l2) ** 2;
  const { m, L } = CONST.single;
  for (const rpm of [400, 100, 20, 8]) {
    const s = simulate({ rpm, frac: 0.3, pend: 'single' }), d = simulate({ rpm, frac: 0.3, pend: 'double' });
    const md = makeModel({ rpm, frac: 0.3, pend: 'double' });
    const rp = md.rp, Om = md.Om, g = CONST.g;
    const lock = ((M * lc * g) ** 2 / (4 * Om * (M * lc * rp - Ip))) / ((m * L * g) ** 2 / (4 * Om * (m * L * rp - m * L * L)));
    rows.push({ rpm, Ps: s.P_mean, Pd: d.P_mean, ratio: d.P_mean / s.P_mean, lock, kd: md.kappaStar, R: md.R });
  }
  t.s3 = rows.map(r => `<tr><td>${r.rpm} rpm</td><td>${sig(mW(r.Ps), 4)}</td><td>${sig(mW(r.Pd), 4)}</td><td>${f(r.ratio, 3)}</td><td>${f(r.lock, 3)}</td></tr>`).join('');
  const r20 = rows.find(r => r.rpm === 20), r400 = rows.find(r => r.rpm === 400), r8 = rows.find(r => r.rpm === 8);
  Object.assign(n, {
    s3_lc: f(lc, 2), s3_lcL: f(lc / (l1 + l2), 2), s3_Ip: sig(Ip, 3),
    s3_ratio20: f(r20.ratio, 3), s3_lock20: f(r20.lock, 3), s3_ratio400: f(r400.ratio, 3), s3_lock400: f(r400.lock, 3),
    s3_ratio8: f(r8.ratio, 3), s3_lock8: f(r8.lock, 3), s3_kd20: sig(r20.kd, 4), s3_R20: sig(r20.R, 4),
    s3_flex20: sig((1 - r20.ratio / r20.lock) * 100, 2),
  });
  raw.s3 = rows;
}

// ---- 4. Large rotors give the same power at the same blade fraction -------------------------------------------------------
{
  const rows = [];
  for (const rpm of [20, 14, 8, 400]) {
    const md = makeModel({ rpm, frac: 0.3 }), o = simulate({ rpm, frac: 0.3 });
    rows.push({ rpm, Om: md.Om, rTip: md.rTip, rp: md.rp, R: md.R, G: md.G, P: o.P_mean, Pstar: md.Pstar });
  }
  t.s4 = rows.map(r => `<tr><td>${r.rpm} rpm</td><td>${sig(r.rTip, 3)} m</td><td>${sig(r.rp, 3)} m</td><td>${sig(r.R, 3)}</td><td>${sig(mW(r.Pstar), 4)}</td><td>${sig(mW(r.P), 4)}</td></tr>`).join('');
  const big = rows.filter(r => r.rpm !== 400), Ps = big.map(r => r.P);
  const { m, L } = CONST.single, g = CONST.g, V = 0.3 * CONST.tipSpeed;
  Object.assign(n, {
    s4_Pmin: sig(mW(Math.min(...Ps)), 4), s4_Pmax: sig(mW(Math.max(...Ps)), 4),
    s4_spread: sig((Math.max(...Ps) / Math.min(...Ps) - 1) * 100, 2), s4_V: f(V, 1),
    s4_Plimit: sig(mW(m * L * g * g / (4 * V)), 4), s4_P400: sig(mW(rows[3].P), 4),
  });
  raw.s4 = rows;
}

// ---- 5. The geared generator at 8 rpm, pivot 30 % -------------------------------------------------------------------------
{
  const rows = [];
  const ideal = simulate({ rpm: 8, frac: 0.3 });
  for (const N of [33, 51, 111, 190]) {
    const o = simulate({ rpm: 8, frac: 0.3, gen: 'geared', N }), md = o.model;
    rows.push({ N, RL: md.RL, j: md.j, fG: md.frictionTorque / (CONST.single.m * CONST.g * CONST.single.L), jammed: o.jammed,
      load: o.P_load, paid: o.P_paid, fric: o.P_fric, Th: o.thetaAbsMax, eta: md.eta });
  }
  t.s5 = rows.map(r => r.jammed
    ? `<tr><td>${r.N}</td><td>–</td><td>${sig(r.j, 3)}</td><td>${f(r.fG * 100, 0)} %</td><td colspan="4">jams: friction above gravity's largest torque</td></tr>`
    : `<tr><td>${r.N}</td><td>${sig(r.RL, 3)}</td><td>${sig(r.j, 3)}</td><td>${f(r.fG * 100, 0)} %</td><td>${sig(mW(r.load), 3)}</td><td>${sig(mW(r.paid), 3)}</td><td>${f(r.fric / r.paid * 100, 0)} %</td><td>${f(r.Th, 3)}</td></tr>`).join('');
  const b = rows.reduce((p, q) => (q.load > p.load ? q : p));
  const r51 = rows.find(r => r.N === 51), r190 = rows.find(r => r.N === 190);
  Object.assign(n, {
    s5_ideal: sig(mW(ideal.P_mean), 4), s5_best_N: String(b.N), s5_best_load: sig(mW(b.load), 3),
    s5_best_share: f(b.load / ideal.P_mean * 100, 0), s5_best_eff: f(b.load / b.paid * 100, 0),
    s5_51_load: sig(mW(r51.load), 3), s5_51_paid: sig(mW(r51.paid), 3),
    s5_190_fric: sig(r190.fG * CONST.single.m * CONST.g * CONST.single.L, 3), s5_mgL: sig(CONST.single.m * CONST.g * CONST.single.L, 3),
    s5_190_fG: f(r190.fG * 100, 0), s5_Njam: f(CONST.single.m * CONST.g * CONST.single.L * 0.70 / CONST.motor.T0, 0),
  });
  raw.s5 = rows;
}

// ---- 6. The fast rotor's fragile numbers: 400 rpm, pivot 30 % ------------------------------------------------------------
{
  const base = { rpm: 400, frac: 0.3, gen: 'geared' };
  const o33 = simulate({ ...base, N: 33 }), o51 = simulate({ ...base, N: 51 });
  const md51 = o51.model, md33 = o33.model;
  const parts = (o) => { const md = o.model, elec = o.P_load / md.keep; return { coil: elec - o.P_load, gear: o.P_paid - elec - o.P_fric }; };
  const p51 = parts(o51), p33 = parts(o33);
  // the best load resistor for the ratio 51 in the full equation (golden section in log R_L)
  const lr = goldenMax(x => simulate({ ...base, N: 51, RL: Math.exp(x) }).P_load, Math.log(3), Math.log(1000), 0.02);
  const b51 = simulate({ ...base, N: 51, RL: Math.exp(lr) }), pb = parts(b51);
  const near = [0.29, 0.31].map(fr => simulate({ rpm: 400, frac: fr, gen: 'geared', N: 51, RL: md51.RL }));
  const ideal = simulate({ rpm: 400, frac: 0.3 });
  Object.assign(n, {
    s6_Rm1: f(md51.R - 1, 3), s6_j51: f(md51.j, 3), s6_j33: f(md33.j, 3), s6_net51: f(md51.R - 1 - md51.j, 4), s6_net33: f(md33.R - 1 - md33.j, 3),
    s6_Pstar: sig(mW(md51.Pstar), 3), s6_ideal: sig(mW(ideal.P_mean), 3),
    s6_RL51: f(md51.RL, 0), s6_form_Th: sig(md51.formula.Theta, 2), s6_form_load: sig(md51.formula.P_load, 2),
    s6_51_load: sig(mW(o51.P_load), 3), s6_51_paid: sig(mW(o51.P_paid), 3), s6_51_gear: sig(mW(p51.gear), 3),
    s6_51_fric: sig(mW(o51.P_fric), 3), s6_51_Th: sig(o51.thetaAbsMax, 3), s6_51_gear_pct: f(p51.gear / o51.P_paid * 100, 0),
    s6_33_RL: sig(md33.RL, 3), s6_33_load: sig(mW(o33.P_load), 3), s6_33_paid: sig(mW(o33.P_paid), 3), s6_33_gear: sig(mW(p33.gear), 3),
    s6_33_Th: sig(o33.thetaAbsMax, 3), s6_33_share: f(o33.P_load / md33.Pstar * 100, 0),
    s6_b51_RL: sig(Math.exp(lr), 2), s6_b51_load: sig(mW(b51.P_load), 3), s6_b51_paid: sig(mW(b51.P_paid), 3), s6_b51_gear: sig(mW(pb.gear), 3),
    s6_b51_Th: sig(b51.thetaAbsMax, 3),
    s6_29_load: sig(mW(near[0].P_load), 3), s6_31_load: sig(mW(near[1].P_load), 3),
  });
  t.s6 = [
    ['33', md33.RL, o33, p33], ['51', md51.RL, o51, p51], ['51', Math.exp(lr), b51, pb],
  ].map(([N, RL, o, p]) => `<tr><td>${N}</td><td>${sig(RL, 3)}</td><td>${sig(o.thetaAbsMax, 3)}</td><td>${sig(mW(o.P_load), 3)}</td><td>${sig(mW(o.P_paid), 3)}</td><td>${sig(mW(o.P_fric), 3)}</td><td>${sig(mW(p.gear), 3)}</td></tr>`).join('');
  raw.s6 = { o33: { load: o33.P_load, paid: o33.P_paid }, o51: { load: o51.P_load, paid: o51.P_paid, RL: md51.RL }, best51: { RL: Math.exp(lr), load: b51.P_load } };
}

const out = { generated: new Date().toISOString().slice(0, 10), seconds: Math.round((Date.now() - T0) / 1000), n, t, raw };
fs.writeFileSync(path.join(__dirname, '..', 'data', 'sim_solutions.json'), JSON.stringify(out, null, 1));
console.log(`data/sim_solutions.json: ${Object.keys(n).length} numbers, ${Object.keys(t).length} tables, ${out.seconds} s`);
for (const k of Object.keys(n)) console.log(k.padEnd(16), n[k]);
