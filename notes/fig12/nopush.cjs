// diagnostic: the 10 mm bump with the stout's push on the cart switched off (fluid.momentum reads 0 to the coupling)
// node notes/fig12/nopush.cjs <speed|off> <1|0>   (1: the stout's push on the cart on, as on the page; 0: off)
const fs = require('fs'), path = require('path'), R = path.join(__dirname, '../../public/scripts/');
const L = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(R + f, 'utf8'))(m); return m.exports; };
const { World } = L('stout-cart.js'), G = L('guinness-glass.js');
const ctrl = process.argv[2], push = process.argv[3] === '1', b = []; for (let n = 0; n < 60; n++) b.push({ x: 1 + 2 * n, h: 0.01, L: 0.25 });
const w = new World({ fluid: { dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 }, road: { bumps: b, Rw: 0.04, xmin: -1, xmax: 125 }, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl }, dtMax: 1 / 200 });
if (!push) { w.fluid.momentum = () => [0, 0]; w.P = [0, 0]; }
const f = w.fluid, Rs = f.Rz(f.h0), rows = [];
while (w.t < 2.3 - 1e-9) { w.advance(1 / 200); f.columnHeights(); rows.push([w.t, w.lastAx, w.lastAz, (f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000]); }
const xi = 1.84118, beta = 2 * xi / (xi * xi - 1), om = 2 * Math.PI * 3.214;
let re = 0, im = 0; for (const r of rows) if (r[0] < 0.7) { re += r[1] * Math.cos(om * r[0]) * 0.005; im -= r[1] * Math.sin(om * r[0]) * 0.005; }
let Sc = 0, Ss = 0, cc = 0, ss = 0, cs = 0; for (const r of rows) { if (r[0] <= 0.8) continue; const c = Math.cos(om * r[0]), m = Math.sin(om * r[0]); Sc += r[3] * c; Ss += r[3] * m; cc += c * c; ss += m * m; cs += c * m; }
const D = cc * ss - cs * cs, A = (Sc * ss - Ss * cs) / D, B = (Ss * cc - Sc * cs) / D;
console.log(`${ctrl}, stout's push ${push ? 'on ' : 'off'}: max|a_x| ${Math.max(...rows.map(r => Math.abs(r[1]))).toFixed(2)} m/s^2; predicted 2q ${(2 * beta / om * Math.hypot(re, im) * 1000).toFixed(1)} mm; solver fitted ${Math.hypot(A, B).toFixed(1)} mm; peak lean ${Math.max(...rows.map(r => Math.abs(r[3]))).toFixed(1)} mm`);
