#!/usr/bin/env node
// Computes every number of the worked solutions of rotor_sim.html with the page's own physics block (tools/physics_block.js)
// and writes data/sim_solutions.json: { n: { key: text }, t: { key: table rows (HTML) }, raw: {...} }.
// tools/build_sim.py puts them into the page (<span data-n="key"> and <tbody data-t="key">). Nothing is typed by hand.
// The machine: a second blade (a uniform rod, CONST.blade) hinged at the 63 m tip of the NREL 5 MW blade, at steady winds.
// Usage: node tools/sim_solutions.js     (a few minutes)
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
const { m, l } = CONST.blade, g = CONST.g;
const WINDS = CONST.winds;

// ---- 1. The best brake at 8 m/s ------------------------------------------------------------------------------------------
{
  const base = { wind: 8 };
  const md = makeModel(base);
  const mults = [];
  for (let i = 0; i <= 20; i++) mults.push(0.3 * Math.pow(10, i / 20));      // 0.3 .. 3, log-spaced
  const sweep = mults.map(k => ({ m: k, P: simulate({ ...base, brake: k }).P_mean, Pf: md.linearPower(k * md.kappaStar) }));
  const lm = goldenMax(x => simulate({ ...base, brake: Math.exp(x) }).P_mean, Math.log(0.5), Math.log(2), 2e-3);
  const peak = simulate({ ...base, brake: Math.exp(lm) });
  const at1 = simulate({ ...base, brake: 1 });
  const lag = lagOf(at1.rec);
  const p03 = sweep[0].P, p3 = sweep[sweep.length - 1].P;
  const band = sweep.filter(s => s.P >= 0.9 * peak.P_mean);
  Object.assign(n, {
    s1_Om: sig(md.Om, 4), s1_rpm: sig(md.rpm, 3), s1_vtip: sig(md.Om * md.rp, 3), s1_R: sig(md.R, 3), s1_G: sig(md.G, 3),
    s1_kstar: sig(md.kappaStar, 3), s1_cstar: sig(md.kappaStar * md.cUnit, 3), s1_Pstar: sig(mW(md.Pstar), 4),
    s1_crit: sig(2 * Math.sqrt(md.R), 3),
    s1_peak_mult: f(Math.exp(lm), 2), s1_peak_P: sig(mW(peak.P_mean), 4),
    s1_P1: sig(mW(at1.P_mean), 4), s1_gain: sig((peak.P_mean / at1.P_mean - 1) * 100, 2),
    s1_P03_pct: f(p03 / peak.P_mean * 100, 0), s1_P3_pct: f(p3 / peak.P_mean * 100, 0),
    s1_band_lo: f(band[0].m, 2), s1_band_hi: f(band[band.length - 1].m, 2),
    s1_lag: f(deg(lag.delta), 1), s1_Theta: sig(at1.Theta, 3), s1_Theta_lin: sig(md.G / Math.hypot(md.R - 1, md.kappaStar), 3),
    s1_below_star: sig(Math.abs(at1.P_mean / md.Pstar - 1) * 100, 2),
  });
  t.s1 = sweep.filter((s, i) => i % 4 === 0 || i === sweep.length - 1).map(s =>
    `<tr><td>${f(s.m, 2)} κ*</td><td>${sig(mW(s.Pf), 4)} mW</td><td>${sig(mW(s.P), 4)} mW</td></tr>`).join('');
  raw.s1 = { sweep, peakMult: Math.exp(lm), peakP: peak.P_mean, P1: at1.P_mean, lagDeg: deg(lag.delta) };
}

// ---- 2. The trail is the bill: 6 m/s, where the swing is largest -----------------------------------------------------------
{
  const md = makeModel({ wind: 6 });
  const o = simulate({ wind: 6 });
  const fac = md.mlc * md.rp * md.Om ** 3;
  const Pbill = -fac * o.trail;
  const trailTheory = -(md.G ** 2) / (4 * md.R * (md.R - 1));
  const Pexact = -fac * o.trailSin;                                  // the identity with <sin theta>: exact for a steady motion
  Object.assign(n, {
    s2_Om: sig(md.Om, 4), s2_R: sig(md.R, 3), s2_G: sig(md.G, 3), s2_Theta: sig(o.Theta, 3),
    s2_trail: sig(o.trail, 3), s2_trail_deg_abs: f(Math.abs(deg(o.trail)), 2), s2_trail_theory: sig(trailTheory, 3),
    s2_fac: sig(fac, 4), s2_P: sig(mW(o.P_mean), 4), s2_Pbill: sig(mW(Pbill), 4), s2_diff: sig(Math.abs(Pbill / o.P_mean - 1) * 100, 2),
    s2_sin: sig(o.trailSin, 4), s2_Pexact: sig(mW(Pexact), 4), s2_exact_diff: sci(Math.abs(Pexact / o.P_mean - 1)),
    s2_cm_mm: sig(Math.abs(o.trailSin) * md.l / 2 * 1e3, 2),
  });
  raw.s2 = { trail: o.trail, trailSin: o.trailSin, P: o.P_mean, Pbill, Pexact, trailTheory };
}

// ---- 3. The three winds: the faster the hinge, the less ------------------------------------------------------------------
{
  const rows = WINDS.map(v => {
    const md = makeModel({ wind: v }), o = simulate({ wind: v });
    const vtip = md.Om * md.rp, flat = md.mlc * g * g / (4 * vtip);
    return { v, rpm: md.rpm, vtip, G: md.G, Pstar: md.Pstar, P: o.P_mean, flat, Theta: o.Theta };
  });
  t.s3 = rows.map(r => `<tr><td>${r.v} m/s</td><td>${sig(r.rpm, 3)} rpm</td><td>${sig(r.vtip, 3)} m/s</td><td>${sig(r.G, 3)}</td><td>${sig(r.Theta, 3)}</td><td>${sig(mW(r.flat), 4)}</td><td>${sig(mW(r.Pstar), 4)}</td><td>${sig(mW(r.P), 4)}</td></tr>`).join('');
  const a = rows[0], b = rows[rows.length - 1];
  Object.assign(n, {
    s3_v_ratio: f(b.vtip / a.vtip, 3), s3_P_ratio: f(a.P / b.P, 3), s3_flat_gap: sig(Math.max(...rows.map(r => Math.abs(r.flat / r.Pstar - 1))) * 100, 2),
    s3_lo: sig(mW(b.P), 3), s3_hi: sig(mW(a.P), 3), s3_rl: f(CONST.rRot / l, 0),
  });
  raw.s3 = rows;
}

// ---- 4. How hard the generator must brake, and how hard it must hold --------------------------------------------------------
{
  const rows = WINDS.map(v => {
    const md = makeModel({ wind: v }), o = simulate({ wind: v });
    let wmax = 0;
    for (const w of o.rec.w1) wmax = Math.max(wmax, Math.abs(w));
    return { v, c: md.c, approx: md.mlc * md.rp * md.Om, tau: md.c * wmax, tauStar: md.tauStar, wmax };
  });
  t.s4 = rows.map(r => `<tr><td>${r.v} m/s</td><td>${sig(r.c, 3)}</td><td>${sig(r.approx, 3)}</td><td>${sig(r.wmax, 3)}</td><td>${sig(r.tau, 3)}</td></tr>`).join('');
  Object.assign(n, {
    s4_tauStar: sig(rows[0].tauStar, 3), s4_mgl: sig(m * g * l / 2, 3),
    s4_tau_min: sig(Math.min(...rows.map(r => r.tau)), 3), s4_tau_max: sig(Math.max(...rows.map(r => r.tau)), 3),
    s4_c_gap: sig(Math.max(...rows.map(r => Math.abs(r.approx / r.c - 1))) * 100, 2),
  });
  raw.s4 = rows;
}

// ---- 5. Which gear ratio, at 8 m/s -----------------------------------------------------------------------------------------
{
  const ideal = simulate({ wind: 8 }), mdI = makeModel({ wind: 8 });
  const rows = [51, 111, 190, 246, 492].map(N => {
    const o = simulate({ wind: 8, gen: 'geared', N }), md = o.model;
    return { N, csc: md.csc, RL: md.RL, j: md.j, fG: md.frictionTorque / md.mgL, jammed: o.jammed, load: o.P_load, paid: o.P_paid, fric: o.P_fric, Th: o.Theta };
  });
  t.s5 = rows.map(r => r.jammed
    ? `<tr><td>${r.N}</td><td>${sig(r.csc, 3)}</td><td>–</td><td>${f(r.fG * 100, 0)} %</td><td colspan="4" class="wrap">jams: friction above gravity's largest torque</td></tr>`
    : `<tr><td>${r.N}</td><td>${sig(r.csc, 3)}</td><td>${sig(r.RL, 3)}</td><td>${f(r.fG * 100, 0)} %</td><td>${sig(mW(r.load), 3)}</td><td>${sig(mW(r.paid), 3)}</td><td>${f(r.fric / r.paid * 100, 0)} %</td><td>${sig(r.Th, 3)}</td></tr>`).join('');
  const b = rows.reduce((p, q) => (q.load > p.load ? q : p)), r51 = rows[0];
  Object.assign(n, {
    s5_ideal: sig(mW(ideal.P_mean), 4), s5_cstar: sig(mdI.c, 3), s5_csc1: sig(CONST.motor.kt * CONST.motor.ke / CONST.motor.Rc * 1e3, 3),
    s5_Nneed: f(Math.sqrt(mdI.c / (CONST.motor.kt * CONST.motor.ke / CONST.motor.Rc)), 0),
    s5_best_N: String(b.N), s5_best_load: sig(mW(b.load), 3), s5_best_share: f(b.load / ideal.P_mean * 100, 0), s5_best_eff: f(b.load / b.paid * 100, 0),
    s5_best_j: sig(b.j, 3), s5_best_fG: f(b.fG * 100, 0), s5_51_csc: sig(r51.csc, 2), s5_51_load: sig(mW(r51.load), 2),
  });
  raw.s5 = rows;
}

// ---- 6. Where the power goes: the ratio 492 at the three winds --------------------------------------------------------------
{
  const need = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'sensor.json'))).need_uW * 1e-6;   // the sensor node (derive/sensor.py)
  const rows = WINDS.map(v => {
    const o = simulate({ wind: v, gen: 'geared', N: 492 }), md = o.model, elec = o.P_load / md.keep;
    return { v, Pstar: md.Pstar, load: o.P_load, coil: elec - o.P_load, fric: o.P_fric, gear: o.P_paid - elec - o.P_fric, paid: o.P_paid };
  });
  t.s6 = rows.map(r => `<tr><td>${r.v} m/s</td><td>${sig(mW(r.paid), 3)}</td><td>${sig(mW(r.load), 3)}</td><td>${sig(mW(r.coil), 3)}</td><td>${sig(mW(r.gear), 3)}</td><td>${sig(mW(r.fric), 3)}</td></tr>`).join('');
  const pct = k => rows.map(r => r[k] / r.paid * 100);
  const rng = k => { const lo = f(Math.min(...pct(k)), 0), hi = f(Math.max(...pct(k)), 0); return lo === hi ? lo : `${lo} to ${hi}`; };
  Object.assign(n, {
    s6_load: rng('load'), s6_gear: rng('gear'), s6_fric: rng('fric'),
    s6_min_load: sig(mW(Math.min(...rows.map(r => r.load))), 3), s6_need: sig(need * 1e6, 3),
    s6_margin: f(Math.min(...rows.map(r => r.load)) / need, 0),
  });
  raw.s6 = rows;
}

const out = { generated: new Date().toISOString().slice(0, 10), seconds: Math.round((Date.now() - T0) / 1000), n, t, raw };
fs.writeFileSync(path.join(__dirname, '..', 'data', 'sim_solutions.json'), JSON.stringify(out, null, 1));
console.log(`data/sim_solutions.json: ${Object.keys(n).length} numbers, ${Object.keys(t).length} tables, ${out.seconds} s`);
for (const k of Object.keys(n)) console.log(k.padEnd(16), n[k]);
