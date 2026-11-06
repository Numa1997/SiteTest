// Is the rods' self-slowing the actuator-disc value f/(2 ρ b U)? Rods held upright in a uniform stream U, no cart.
// k = (U − ū_read) · 2 ρ b U / f̄  (f̄ the mean force per metre across the rods); actuator-disc theory: k = 1.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), U = +(process.env.U || 0.5);
const w = new T.World({ dx, U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0, 0, 0, 0, 0], nsub: 10 });
w.frozen = true; w.cartGone = true; w.selfField = false; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
while (w.t < 4 - 1e-9) w.step(null);
const p = w.mp, NP = T.NP; let us = 0, F = 0;
for (let o = 0; o < 4 * NP; o += 2) us += w.uS[o]; us /= 2 * NP;
for (let o = 0; o < 4 * NP; o += 2) F += w.impNew[o]; F /= (w.h * w.nsub);   // total x-force on the rods (N)
const fbar = F / (p.L1 + p.L2), law = (xi) => xi * U + p.cq * U * U, F0 = law(p.xi[0]) * p.L1 + law(p.xi[1]) * p.L2;
console.log(JSON.stringify({ med, dx, U, opt: process.env.OPT || 'base', ratio_drag_over_law: +(F / F0).toFixed(4), slowing_over_U: +((U - us) / U).toFixed(4), k_disc: +((U - us) * 2 * w.rho * w.b * U / fbar).toFixed(3) }));
