// Numbers for derive/ch08.py: runs the page's own modules in Node and prints JSON. node derive/ch08_probe.cjs
'use strict';
const path = require('path'), HERE = path.resolve(__dirname, '..');
const core = require(path.join(HERE, 'physics/core.js')), C = require(path.join(HERE, 'contract.json'));
const m2 = require(path.join(HERE, 'physics/ch02.js')), m4 = require(path.join(HERE, 'physics/ch04.js')), m5 = require(path.join(HERE, 'physics/ch05.js'));
const m6 = require(path.join(HERE, 'physics/ch06.js')), m7 = require(path.join(HERE, 'physics/ch07.js')), m8 = require(path.join(HERE, 'physics/ch08.js'));
const p = core.withDefaults(C, m8.inputs, {}), o = m8.compute(p), F = m8.FIX, out = { p, o: Object.assign({}, o) };
// 1. the chain by hand
const s = m2.compute({ r_t: p.r_t, V_ex: p.V_ex, phi: F.phi, T: F.T, p: p.p, t_clean: p.t_clean, k_f: F.k_f });
const L = m4.compute({ a_lens: p.a_lens, u_obj: F.u_obj, WD: p.WD, V_land: p.V_land });
const sp = m5.compute({ C_s: L.C_s, C_c: L.C_c, B_r: s.B_r, dE: s.dE, dE50: s.dE50, V_land: p.V_land, alpha: 5e-3, I_p: p.I_p, probe_convention: 'fw50' });
const y = m8.yields(p.material, p.V_land);
const mm = m7.compute({ d_p: sp.d_p_opt, I_p: p.I_p, t_d: p.t_d, N_px: p.N_px, eta_c: p.eta_c, cd: p.cd, pitch: F.pitch, height: F.height, sidewall: F.sidewall, px: F.px, t_ov: F.t_ov,
  delta_SE: y.delta, eta_BSE: y.eta, sig_core: y.core, f_core: y.fcore, sig_halo: y.halo });
out.hand = { d_p: sp.d_p_opt, sigma_CD: mm.sigma_CD, MPH: mm.MPH, C_c: L.C_c, C_s: L.C_s, B_r: s.B_r, d_v: s.d_v };
// 2. stored yields against fresh runs off the grid
out.yields = [1200, 4000, 12000].map(V => { const d = m6.compute({ material: 'Si', V_land: V }), t = m8.yields('Si', V); return { V, delta: d.delta_SE, udelta: d.u_delta, delta_t: t.delta, eta: d.eta_BSE, ueta: d.u_eta, eta_t: t.eta, core: d.sig_core, core_t: t.core, f: d.f_core, f_t: t.fcore, halo: d.sig_halo, halo_t: t.halo }; });
// 3. defocus: the axial ray with the excitation raised by eps crosses the axis earlier by dz; compare with 2 C_c eps
const Vs = p.V_land * (1 + core.C.e * p.V_land / (2 * core.C.m_e * core.C.c * core.C.c)), eta = core.C.e / (8 * core.C.m_e * Vs);
const L0 = m4.compute({ a_lens: p.a_lens, u_obj: F.u_obj, WD: p.WD, V_land: p.V_land });
out.defocus = [1e-5, 1e-4].map(eps => {
  const r = z => m4.paraxial(L0.B_0 * (1 + eps), p.a_lens, eta, -F.u_obj, z, 0, 1)[0];
  let z0 = p.WD * 0.98, z1 = p.WD * 1.02;
  for (let i = 0; i < 60; i++) { const zm = 0.5 * (z0 + z1); if (r(zm) > 0) z0 = zm; else z1 = zm; }
  const dz = p.WD - 0.5 * (z0 + z1);
  return { eps, dz, model: 2 * L0.C_c * eps };
});
// 4. the source grid: interpolated against direct chapter 2 runs at the same random draws
const rnd = core.rng(8082026), g = () => Math.sqrt(-2 * Math.log(1 - rnd())) * Math.cos(2 * Math.PI * rnd());
let worst = 0;
for (let n = 0; n < 40; n++) {
  const zr = g(), zp = g(); g(); g();
  const r = p.r_t * Math.exp(zr * Math.log(1 + p.tol_rt)), pr = p.p * Math.exp(zp * p.tol_p);
  const d = m2.compute({ r_t: r, V_ex: p.V_ex, phi: F.phi, T: F.T, p: pr, t_clean: p.t_clean, k_f: F.k_f });
  // interpolate the module's way through a fresh 5 x 5 grid
  const G = [];
  for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) G.push(m2.compute({ r_t: p.r_t * Math.exp((i - 2) * 1.5 * Math.log(1 + p.tol_rt)), V_ex: p.V_ex, phi: F.phi, T: F.T, p: p.p * Math.exp((j - 2) * 1.5 * p.tol_p), t_clean: p.t_clean, k_f: F.k_f }));
  const u = zr / 1.5 + 2, v = zp / 1.5 + 2, x = Math.min(4, Math.max(0, u)), yv = Math.min(4, Math.max(0, v)), i = Math.min(3, Math.floor(x)), j = Math.min(3, Math.floor(yv)), fx = x - i, fy = yv - j;
  const at = (a, b) => Math.log(G[5 * a + b].B_r);
  const Bi = Math.exp((1 - fx) * (1 - fy) * at(i, j) + fx * (1 - fy) * at(i + 1, j) + (1 - fx) * fy * at(i, j + 1) + fx * fy * at(i + 1, j + 1));
  if (Math.abs(zr) < 3 && Math.abs(zp) < 3) worst = Math.max(worst, Math.abs(Bi / d.B_r - 1));
  if (n === 4) break;                                                    // five samples are enough for the grid (each needs 26 runs)
}
out.grid_worst = worst;
// 5. the tolerance Monte Carlo with one source of error at a time
const none = { tol_rt: 0, tol_NI: 0, tol_p: 0, tol_z: 0 };
out.tol_each = {};
for (const k of ['tol_rt', 'tol_NI', 'tol_p', 'tol_z']) {
  const q = Object.assign({}, p, none, { [k]: p[k] }), r = m8.compute(q);
  out.tol_each[k] = { dp_sd: r.tol_dp_sd, cd_p95: r.tol_cd_p95, yield: r.tol_yield };
}
console.log(JSON.stringify(out));
