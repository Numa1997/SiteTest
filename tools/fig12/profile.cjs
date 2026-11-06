// Time one fluid step of the stout solver by phase: node tools/fig12/profile.cjs [dx] [steps]
// The tulip at 125 mm is pushed for 0.1 s (a sloshing surface), then [steps] steps are timed.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const dx = +(process.argv[2] || 0.004), N = +(process.argv[3] || 100), dt = 1 / 200;
const f = new Fluid({ dx, profile: G, h0: 0.125, H: G.R.length * G.dz + 0.03 });
for (let n = 0; n < 40; n++) f.step(dt, n < 20 ? 3 : 0, 0);
const phases = [['levelSet', () => f.levelSet()], ['p2g', () => f.p2g()], ['forces', () => f.forces(dt, 0, 0)],
  ['project', () => f.project(dt)], ['extrapolate', () => f.extrapolate(3)], ['g2p', () => f.g2p()], ['advect', () => f.advect(dt)]];
const T = phases.map(() => 0); let it = 0;
const now = () => Number(process.hrtime.bigint()) / 1e6;
for (let n = 0; n < N; n++) { phases.forEach(([, fn], i) => { const t = now(); fn(); T[i] += now() - t; }); f.t += dt; it += f.cgIters; }
const tot = T.reduce((a, b) => a + b, 0);
console.log(`dx ${dx * 1000} mm, ${f.np} particles, ${f.nc} cells: ${(tot / N).toFixed(2)} ms per step (${(dt * 1000 / (tot / N)).toFixed(2)} s simulated per s); CG ${(it / N).toFixed(1)} iterations`);
phases.forEach(([nm], i) => console.log(`  ${nm.padEnd(12)} ${(T[i] / N).toFixed(2)} ms`));
