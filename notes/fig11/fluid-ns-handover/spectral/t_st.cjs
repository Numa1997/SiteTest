// Schäfer & Turek (1996) 2D-1 (Re 20, steady) and 2D-2 (Re 100, periodic) with the penalized pseudo-spectral solver.
// Benchmark coordinates xb in [0, 2.2], yb in [0, 0.41]; cylinder D = 0.1 at (0.2, 0.2). Periodic box: a sponge of length LS
// upstream of the inlet sets the parabolic inflow and absorbs the wake; walls are penalized bodies.
const { NS, Body } = require('./ns2.cjs');
const CASE = process.env.CASE || '2D-1', N = +(process.env.N || 512), H = 0.41, D = 0.1, nu = 1e-3;
const Um = CASE === '2D-1' ? 0.3 : 1.5, Umean = 2 * Um / 3;
const LS = 0.36, Lx = 2.2 + LS, dx = Lx / N, M = Math.round(0.64 / dx / 16) * 16, Ly = M * dx, wallLo = (Ly - H) / 2;
const INR = !!process.env.INRHS, ETA = +(process.env.ETA || (INR ? 2e-4 : 1e-4));
const ns = new NS({ N, M, Lx, Ly, nu, eta: ETA, etaSp: 0.02, cfl: +(process.env.CFL || 0.6), mix: !!process.env.MIX, penNoDeal: !!process.env.NODEAL, expPen: !!process.env.EXPPEN, inRhs: INR, dtMax: INR ? 2 * ETA : 1e-2 });
const xb = (x) => x - LS, yb = (y) => y - wallLo;
const prof = (y) => { const s = yb(y); return s > 0 && s < H ? 4 * Um * s * (H - s) / (H * H) : 0; };
ns.Ux = Umean * H / Ly; ns.Uy = 0;                     // the mean of u over any cross-section of the periodic box
const INLET = !!process.env.INLET;   // INLET: full sponge strength up to the inlet x_b = 0 (a Dirichlet inlet), ramping up from the outlet side
ns.setSponge((x, y) => { const s = x < LS ? (INLET ? (x < LS / 2 ? Math.pow(Math.sin(Math.PI * x / LS), 2) : 1) : Math.pow(Math.sin(Math.PI * x / LS), 2)) : 0; return [s, prof(y) - ns.Ux, 0]; });
const DEL = +(process.env.DEL || 1) * dx;
const RAMP = !!process.env.RAMP;
const walls = new Body(ns, { delta: DEL, ramp: RAMP, sdf: (X, Y) => { const s = yb(Y); return Math.min(s, H - s); }, xc: 0, yc: 0 });
const cyl = new Body(ns, { delta: DEL, ramp: RAMP, sdf: (X, Y) => Math.hypot(X, Y) - D / 2, xc: LS + 0.2, yc: wallLo + 0.2 });
ns.bodies = [walls, cyl];
ns.setOmega((x, y) => 0);                               // start from the mean flow; the sponge and walls build the profile
const T = +(process.env.T || (CASE === '2D-1' ? 12 : 12)), t0 = Date.now(); let k = 0, hist = [];
while (ns.t < T) {
  const dt = ns.step(); k++;
  const cD = 2 * cyl.F[0] / (Umean * Umean * D), cL = 2 * cyl.F[1] / (Umean * Umean * D);
  hist.push([ns.t, cD, cL]);
  if (k % 200 === 0) console.log(`t=${ns.t.toFixed(3)} dt=${dt.toExponential(2)} cD=${cD.toFixed(5)} cL=${cL.toFixed(5)} ${((Date.now() - t0) / k).toFixed(0)} ms/step`);
}
// recirculation length: where u on the axis y=0.2 behind the cylinder turns positive
ns.velocity(ns.wr, ns.wi); const j0 = Math.floor((wallLo + 0.2) / dx - 0.5); let La = null;
const uAx = (i) => 0.5 * (ns.u[j0 * N + i] + ns.u[(j0 + 1) * N + i]);
for (let i = Math.ceil((LS + 0.25) / dx); i < N - 1; i++) { if (uAx(i) < 0 && uAx(i + 1) >= 0) { const x0 = ns.X(i), x1 = ns.X(i + 1); La = xb(x0 + (x1 - x0) * (-uAx(i)) / (uAx(i + 1) - uAx(i))) - 0.25; break; } }
const last = hist.slice(-Math.floor(hist.length / 4));
const cDmax = Math.max(...last.map(h => h[1])), cLmax = Math.max(...last.map(h => h[2]));
// Strouhal number from upward zero crossings of cL in the last quarter
let zc = []; for (let i = 1; i < last.length; i++) if (last[i - 1][2] < 0 && last[i][2] >= 0) zc.push(last[i - 1][0] + (last[i][0] - last[i - 1][0]) * (-last[i - 1][2]) / (last[i][2] - last[i - 1][2]));
const St = zc.length > 2 ? D / Umean / ((zc[zc.length - 1] - zc[0]) / (zc.length - 1)) : null;
console.log(JSON.stringify({ CASE, N, M, dx, D_over_dx: D / dx, eta: ns.eta, steps: k, final_cD: hist[hist.length - 1][1], final_cL: hist[hist.length - 1][2], La, cDmax, cLmax, St, minutes: (Date.now() - t0) / 60000 }));
require('fs').writeFileSync(`st_${CASE}_${N}_${process.env.MIX?'mix':'pen'}_${process.env.DEL||1}_${RAMP?'ramp':'erf'}_${process.env.CFL||0.6}_${INR?'inrhs'+ETA:'split'}.json`, JSON.stringify(hist.filter((h, i) => i % 5 === 0)));
