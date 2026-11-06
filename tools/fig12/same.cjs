// Fingerprint of the solver's state after 1 s with a push: node tools/fig12/same.cjs [dx]
// An optimisation that keeps the arithmetic must print the same numbers, to the last digit.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const dx = +(process.argv[2] || 0.004), dt = 1 / 200;
const f = new Fluid({ dx, profile: G, h0: 0.125, H: G.R.length * G.dz + 0.03 });
let it = 0;
for (let n = 0; n < 200; n++) { f.step(dt, n < 24 ? 25 * Math.sin(Math.PI * n / 24) : 0, n < 24 ? 3 : 0); it += f.cgIters; }
const h = crypto.createHash('sha256');
for (const a of [f.px, f.py, f.pz, f.pu, f.pv, f.pw, f.phi, f.q]) h.update(Buffer.from(a.buffer, a.byteOffset, (a === f.phi || a === f.q ? a.length : f.np) * 8));
console.log(`np ${f.np}, spilled ${f.spilled}, CG iterations ${it}, x[0] ${f.px[0]}, u[0] ${f.pu[0]}, sha256 ${h.digest('hex').slice(0, 16)}`);
