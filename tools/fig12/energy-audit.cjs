// Where does the 3D solver's energy go? node tools/fig12/energy-audit.cjs <fill mm> [T s] [dx m]   OUT=file.json
// The glass is tilted and released as in decay-3d.cjs (a_x ramped to 1.5 m/s^2 over 0.6 s, held to 1 s, dropped), wall
// friction off, viscosity 2.05e-6 m^2/s. Fluid.step is replayed stage by stage (the same calls in the same order) and the
// stout's mechanical energy (whole glass, 2 x the half glass) is measured between the stages:
//   particles: kinetic sum m_p (|v_p|^2 + (dx^2/4) sum_c |C_c|^2) / 2 (APIC: the affine part's energy, trilinear inertia
//              dx^2/4 per component) and potential sum m_p g z_p
//   grid:      kinetic sum over faces of m_f u_f^2 / 2, m_f = m_p x (the face's P2G weight sum)
// and booked per mechanism, each step, after the release (t >= 1.2 s):
//   p2g      particle kinetic energy -> grid kinetic energy (the transfer's loss)
//   grid     forces + projection (+ viscosity): gravity's input, the pressure's work, the viscous loss
//   g2p      grid kinetic energy -> particle kinetic energy
//   motion   the particles' potential energy change while they move with their velocity (gravity's return)
//   wall     the potential energy change when collide() puts particles back inside the glass
//   spill    the energy of the particles that left over the rim
// grid + motion is the gravity-pressure cycle: zero for an exact scheme in a closed glass at rest.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const h0 = +process.argv[2] / 1000, T = +(process.argv[3] || 6), dx = +(process.argv[4] || 0.004), dt = +(process.env.DT || 0.005), A = process.env.A != null ? +process.env.A : 1.5;
if (!(h0 > 0)) throw new Error('usage: energy-audit.cjs <fill mm> [T] [dx]');
const force = (t) => (t < 0.6 ? A * 0.5 * (1 - Math.cos(Math.PI * t / 0.6)) : t < 1.0 ? A : 0);
// VC: the solver's volume correction strength (Fluid option volumeCorrection, off by default); RELAX: particle relaxation
const f = new Fluid({ dx, profile: G, h0, H: (G.R.length - 1) * G.dz + 0.03, nu: 2.05e-6, volumeCorrection: +(process.env.VC || 0), relax: +(process.env.RELAX || 0), flip: +(process.env.FLIP || 0), densityProjection: +(process.env.DP || 0), quadratic: process.env.Q === '1' });
const W = 2 * f.mp, I = dx * dx / 4;
const keP = () => { let k = 0; const C = f.pc; for (let p = 0; p < f.np; p++) { let a = 0; for (let c = 0; c < 3; c++) a += C[c][0][p] ** 2 + C[c][1][p] ** 2 + C[c][2][p] ** 2; k += f.pu[p] ** 2 + f.pv[p] ** 2 + f.pw[p] ** 2 + I * a; } return 0.5 * W * k; };
const keLin = () => { let k = 0; for (let p = 0; p < f.np; p++) k += f.pu[p] ** 2 + f.pv[p] ** 2 + f.pw[p] ** 2; return 0.5 * W * k; };
const peP = () => { let s = 0; for (let p = 0; p < f.np; p++) s += f.pz[p]; return W * f.g * s; };
const keG = () => { let k = 0; for (const [a, m] of [[f.u, f.mu], [f.v, f.mv], [f.w, f.mw]]) for (let n = 0; n < a.length; n++) if (m[n] > 1e-9) k += m[n] * a[n] * a[n]; return 0.5 * W * k; };
const book = { p2g: 0, grid: 0, g2p: 0, motion: 0, wall: 0, spill: 0 }, series = [];
const Rs = f.Rz(Math.min(h0, f.zRim)), t0 = Date.now();
for (let n = 0; n * dt < T - 1e-9; n++) {
  const t = n * dt, ax = force(t + 0.5 * dt), on = t >= 1.2;
  const e0k = keP(), e0p = peP();
  f.levelSet(); f.p2g();
  const g1 = keG();
  f.forces(dt, ax, 0); if (f.volumeCorrection > 0) f.density(); f.project(dt);
  const g2 = keG();
  f.extrapolate(3); f.g2p();
  const e1k = keP();
  if (f.pool) f.pool.run(4, f.np, dt, 0); else f.advectRange(dt, 0, f.np);
  const e2p = peP();
  // the particles about to spill: their energy leaves with them
  let es = 0; for (let p = 0; p < f.np; p++) { const r2 = f.px[p] ** 2 + f.py[p] ** 2; if (f.pz[p] > f.zRim && r2 > f.Rrim * f.Rrim) es += W * (0.5 * (f.pu[p] ** 2 + f.pv[p] ** 2 + f.pw[p] ** 2) + f.g * f.pz[p]); }
  const e2k = keP(), eBefore = e2k + e2p;
  f.collide();
  const e3 = keP() + peP();
  if (f.relaxStrength > 0) f.relax(f.relaxStrength);
  f.t += dt;
  if (on) { book.p2g += g1 - e0k; book.grid += g2 - g1; book.g2p += e1k - g2; book.motion += e2p - e0p; book.wall += e3 - (eBefore - es); book.spill -= es; }
  if (n % 4 === 3) { f.columnHeights(); series.push([+(t + dt).toFixed(3), e3, keP(), keLin(), (f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000]); }
}
const S = series.filter((s) => s[0] >= 1.2), Tw = S[S.length - 1][0] - S[0][0], uW = (x) => (1e6 * x / Tw).toFixed(2);
console.log(`energy audit, fill ${h0 * 1000} mm, dx ${dx * 1000} mm, free swing ${S[0][0]}-${S[S.length - 1][0]} s (${((Date.now() - t0) / 1000).toFixed(0)} s to compute)`);
console.log(`total mechanical energy: ${(1e6 * (S[S.length - 1][1] - S[0][1])).toFixed(1)} uJ over the window (${uW(S[S.length - 1][1] - S[0][1])} uW)`);
console.log(`per mechanism (uW, negative = lost): p2g ${uW(book.p2g)}, grid ${uW(book.grid)}, g2p ${uW(book.g2p)}, motion ${uW(book.motion)}, wall ${uW(book.wall)}, spill ${uW(book.spill)}; grid + motion ${uW(book.grid + book.motion)}; sum ${uW(Object.values(book).reduce((a, b) => a + b))}`);
const zc = (s) => s[1]; console.log(`centre of mass: falls ${(1e6 * (S[0][1] - S[S.length - 1][1]) / (W * f.np * f.g)).toFixed(1)} um over the window (from the energy)`);
console.log(`kinetic energy (particles, with the affine part): ${(1e6 * S[0][2]).toFixed(1)} -> ${(1e6 * S[S.length - 1][2]).toFixed(1)} uJ`);
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ h0, dx, book, window: Tw, series }));
