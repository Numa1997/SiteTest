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
const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
const sci = (x, d = 1) => { const [m, e] = x.toExponential(d).split('e'); return `${m}·10${String(+e).split('').map(c => SUP[c]).join('')}`; };
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

const NEED = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'sensor.json'), 'utf8')).need_uW * 1e-6;
const turbineW = v => 0.5 * 1.225 * Math.PI * CONST.rTip ** 2 * v ** 3 * 0.482;    // P_T at peak Cp (notes section 0.3)

// ---- 1. The best brake at 8 m/s, pivot 30 % ----------------------------------------------------------------------------
{
  const base = { wind: 8, frac: 0.3, pend: 'single' };
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
    s1_R: sig(md.R, 4), s1_rpm: sig(md.rpm, 3), s1_kstar: sig(md.kappaStar, 4), s1_cstar: sig(md.kappaStar * md.cUnit, 3),
    s1_Om: sig(md.Om, 4), s1_rp: sig(md.rp, 3), s1_G: sig(md.G, 3), s1_Pstar: sig(mW(md.Pstar), 4),
    s1_peak_mult: f(Math.exp(lm), 2), s1_peak_P: sig(mW(peak.P_mean), 4),
    s1_P1: sig(mW(at1.P_mean), 4), s1_gain: sig((peak.P_mean / at1.P_mean - 1) * 100, 2),
    s1_P03_pct: f(p03 / peak.P_mean * 100, 0), s1_P3_pct: f(p3 / peak.P_mean * 100, 0),
    s1_band_lo: f(half[0].m, 2), s1_band_hi: f(half[half.length - 1].m, 2),
    s1_lag: f(deg(lag.delta), 1), s1_Theta: sig(at1.Theta, 3), s1_Theta_lin: sig(md.G / Math.hypot(md.R - 1, md.kappaStar), 3),
    s1_below_star: sig(Math.abs(at1.P_mean / md.Pstar - 1) * 100, 2),
  });
  t.s1 = sweep.filter((s, i) => i % 4 === 0 || i === sweep.length - 1).map(s =>
    `<tr><td>${f(s.m, 2)} κ*</td><td>${sig(mW(s.Pf), 4)} mW</td><td>${sig(mW(s.P), 4)} mW</td></tr>`).join('');
  raw.s1 = { sweep, peakMult: Math.exp(lm), peakP: peak.P_mean, P1: at1.P_mean, lagDeg: deg(lag.delta) };
}

// ---- 2. The trail is the bill: 6 m/s, pivot 30 % ------------------------------------------------------------------------
{
  const md = makeModel({ wind: 6, frac: 0.3 });
  const o = simulate({ wind: 6, frac: 0.3 });
  const { m, L } = CONST.single;
  const Pbill = -m * md.rp * L * md.Om ** 3 * o.trail;
  const trailTheory = -(md.G ** 2) / (4 * md.R * (md.R - 1));
  const Pexact = -m * md.rp * L * md.Om ** 3 * o.trailSin;          // the same identity with <sin theta>: exact for a steady motion
  Object.assign(n, {
    s2_Om: sig(md.Om, 4), s2_rp: sig(md.rp, 4), s2_R: sig(md.R, 4), s2_G: sig(md.G, 3),
    s2_trail: sig(o.trail, 3), s2_trail_deg_abs: f(Math.abs(deg(o.trail)), 1), s2_trail_theory: sig(trailTheory, 3),
    s2_P: sig(mW(o.P_mean), 4), s2_Pbill: sig(mW(Pbill), 4), s2_diff: sig(Math.abs(Pbill / o.P_mean - 1) * 100, 2),
    s2_Theta: sig(o.Theta, 3), s2_mrpLO3: sig(m * md.rp * L * md.Om ** 3, 4),
    s2_sin: sig(o.trailSin, 3), s2_Pexact: sig(mW(Pexact), 4), s2_exact_diff: sci(Math.abs(Pexact / o.P_mean - 1)),
  });
  raw.s2 = { trail: o.trail, trailSin: o.trailSin, P: o.P_mean, Pbill, Pexact, trailTheory };
}

// ---- 3. One rod or two: the 3/4 rule -------------------------------------------------------------------------------------
{
  const rows = [];
  const { m1, m2, l1, l2 } = CONST.double, M = m1 + m2, lc = (m1 * l1 + m2 * (l1 + l2)) / M, Ip = m1 * l1 * l1 + m2 * (l1 + l2) ** 2;
  const { m, L } = CONST.single;
  for (const wind of CONST.winds) {
    const s = simulate({ wind, frac: 0.3, pend: 'single' }), d = simulate({ wind, frac: 0.3, pend: 'double' });
    const md = makeModel({ wind, frac: 0.3, pend: 'double' });
    const rp = md.rp, Om = md.Om, g = CONST.g;
    const lock = ((M * lc * g) ** 2 / (4 * Om * (M * lc * rp - Ip))) / ((m * L * g) ** 2 / (4 * Om * (m * L * rp - m * L * L)));
    rows.push({ wind, Ps: s.P_mean, Pd: d.P_mean, ratio: d.P_mean / s.P_mean, lock, kd: md.kappaStar, R: md.R });
  }
  t.s3 = rows.map(r => `<tr><td>${r.wind} m/s</td><td>${sig(mW(r.Ps), 4)}</td><td>${sig(mW(r.Pd), 4)}</td><td>${f(r.ratio, 3)}</td><td>${f(r.lock, 3)}</td></tr>`).join('');
  const r8 = rows.find(r => r.wind === 8);
  Object.assign(n, {
    s3_M: String(M), s3_lc: sig(lc, 3), s3_lcL: f(lc / (l1 + l2), 2), s3_Ip: sig(Ip, 3),
    s3_ratio8: f(r8.ratio, 3), s3_lock8: f(r8.lock, 3), s3_kd8: sig(r8.kd, 4), s3_Rm1_8: sig(r8.R - 1, 4),
    s3_flex8: sig((1 - r8.ratio / r8.lock) * 100, 2),
  });
  raw.s3 = rows;
}

// ---- 4. More wind, less from the pendulum ---------------------------------------------------------------------------------
{
  const rows = [];
  for (const wind of CONST.winds) {
    const md = makeModel({ wind, frac: 0.3 }), o = simulate({ wind, frac: 0.3 });
    rows.push({ wind, rpm: md.rpm, R: md.R, G: md.G, P: o.P_mean, Pstar: md.Pstar, PT: turbineW(wind) });
  }
  t.s4 = rows.map(r => `<tr><td>${r.wind} m/s</td><td>${sig(r.rpm, 3)} rpm</td><td>${sig(r.R, 3)}</td><td>${sig(r.G, 3)}</td><td>${sig(mW(r.Pstar), 4)}</td><td>${sig(mW(r.P), 4)}</td><td>${sig(r.PT / 1e6, 3)}</td></tr>`).join('');
  const a = rows[0], b = rows[rows.length - 1];
  Object.assign(n, {
    s4_P6: sig(mW(a.P), 4), s4_P10: sig(mW(b.P), 4), s4_fall: f(a.P / b.P, 2), s4_Tgrow: f(b.PT / a.PT, 2),
    s4_share_fall: f((a.P / a.PT) / (b.P / b.PT), 1),
  });
  raw.s4 = rows;
}

// ---- 5. The geared generator at 6 m/s, pivot 30 % -------------------------------------------------------------------------
{
  const rows = [];
  const ideal = simulate({ wind: 6, frac: 0.3 });
  const mgL = CONST.single.m * CONST.g * CONST.single.L;
  for (const N of [51, 111, 190, 246, 492]) {
    const o = simulate({ wind: 6, frac: 0.3, gen: 'geared', N }), md = o.model;
    rows.push({ N, RL: md.RL, j: md.j, fG: md.frictionTorque / mgL, jammed: o.jammed,
      load: o.P_load, paid: o.P_paid, fric: o.P_fric, Th: o.thetaAbsMax, eta: md.eta, fT: md.frictionTorque });
  }
  t.s5 = rows.map(r => r.jammed
    ? `<tr><td>${r.N}</td><td>–</td><td>${sig(r.j, 3)}</td><td>${f(r.fG * 100, 0)} %</td><td colspan="4" class="wrap">jams: friction above gravity's largest torque</td></tr>`
    : `<tr><td>${r.N}</td><td>${sig(r.RL, 3)}</td><td>${sig(r.j, 3)}</td><td>${f(r.fG * 100, 0)} %</td><td>${sig(mW(r.load), 3)}</td><td>${sig(mW(r.paid), 3)}</td><td>${f(r.fric / r.paid * 100, 0)} %</td><td>${f(r.Th, 3)}</td></tr>`).join('');
  const b = rows.filter(r => !r.jammed).reduce((p, q) => (q.load > p.load ? q : p));
  const r492 = rows.find(r => r.N === 492);
  Object.assign(n, {
    s5_ideal: sig(mW(ideal.P_mean), 4), s5_best_N: String(b.N), s5_best_load: sig(mW(b.load), 3),
    s5_best_share: f(b.load / ideal.P_mean * 100, 0), s5_best_eff: f(b.load / b.paid * 100, 0),
    s5_492_fric: sig(r492.fT, 3), s5_mgL: sig(mgL, 3), s5_492_fG: f(r492.fG * 100, 0),
    s5_Njam: f(mgL * 0.70 / CONST.motor.T0, 0),
    s5_best_Th: f(b.Th, 2), s5_190_load: sig(mW(rows.find(r => r.N === 190).load), 3), s5_190_Th: f(rows.find(r => r.N === 190).Th, 2),
  });
  raw.s5 = rows;
}

// ---- 6. The weakest mounting: 10 m/s, pivot 90 % ------------------------------------------------------------------------
{
  const rows = [];
  const ideal = simulate({ wind: 10, frac: 0.9 });
  for (const N of [51, 111]) {
    const o = simulate({ wind: 10, frac: 0.9, gen: 'geared', N });
    rows.push({ N, RL: o.model.RL, Th: o.thetaAbsMax, load: o.P_load, paid: o.P_paid, fric: o.P_fric, R: o.model.R });
  }
  t.s6 = rows.map(r => `<tr><td>${r.N}</td><td>${sig(r.RL, 3)}</td><td>${sig(r.Th, 3)}</td><td>${sig(mW(r.load), 3)}</td><td>${sig(mW(r.paid), 3)}</td><td>${sig(mW(r.fric), 3)}</td></tr>`).join('');
  const b = rows.reduce((p, q) => (q.load > p.load ? q : p));
  Object.assign(n, {
    s6_R: sig(b.R, 3), s6_ideal: sig(mW(ideal.P_mean), 3), s6_best_N: String(b.N), s6_load: sig(mW(b.load), 3),
    s6_times: f(b.load / NEED, 0), s6_Th: sig(b.Th, 2), s6_play: f(b.Th / (0.5 * Math.PI / 180), 0), s6_need: f(NEED * 1e6, 1),
  });
  raw.s6 = rows;
}

const out = { generated: new Date().toISOString().slice(0, 10), seconds: Math.round((Date.now() - T0) / 1000), n, t, raw };
fs.writeFileSync(path.join(__dirname, '..', 'data', 'sim_solutions.json'), JSON.stringify(out, null, 1));
console.log(`data/sim_solutions.json: ${Object.keys(n).length} numbers, ${Object.keys(t).length} tables, ${out.seconds} s`);
for (const k of Object.keys(n)) console.log(k.padEnd(16), n[k]);
