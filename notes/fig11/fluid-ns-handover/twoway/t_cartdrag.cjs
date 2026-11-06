// T2: the cart held still in a stream U, alone (no rods). Mean drag over the last 2 s against the independent spectral solver
// (spectral/RESULTS.md, same box 3.0 × 1.6 m, cart 1.1 m from the inlet, centred in height): glycerol U 0.5 → 7.2 N, U 2 → 79.9 N.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', U = +(process.env.U || 0.5), dx = +(process.env.DX || 0.025), dur = +(process.env.DUR || 6);
const ny = Math.round(1.6 / dx / 8) * 8, nx = Math.round(3.0 / dx / 8) * 8;
const w = new T.World({ dx, nx, ny, x0: -1.1, y0: -0.06 - ny * dx / 2, U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, nsub: +(process.env.NSUB || 5) });
w.frozen = true; w.noRods = true;
for (let c = 0; c < w.v.length; c++) { const i = c % w.nx, j = Math.floor(c / w.nx), X = w.xv(i), Y = w.yv(j); w.v[c] += 0.5 * 0.1 * Math.exp(-((X - 0.4) ** 2 + (Y + 0.06) ** 2) / 0.01); }   // a small kick behind the cart to break the symmetry
const hist = []; while (w.t < dur - 1e-9) { w.step(null); hist.push([w.t, w.Q0]); }
const last = hist.filter(h => h[0] > dur - 2), mean = last.reduce((s, h) => s + h[1], 0) / last.length, sd = Math.sqrt(last.reduce((s, h) => s + (h[1] - mean) ** 2, 0) / last.length);
console.log(JSON.stringify({ med, U, dx, grid: [nx, ny], Re_h: +(U * 0.12 / w.nu).toFixed(0), drag_N: +mean.toFixed(2), drag_sd_N: +sd.toFixed(2), CD_2D: +(mean / (0.5 * w.rho * U * U * 0.12 * 0.2)).toFixed(3) }));
