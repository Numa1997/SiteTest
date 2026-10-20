// Figure eight radii from the exact curve: c_k = (1/L) ∮ z e^{-ik t(s)} ds with t = 2π s/L, periodic trapezoid rule in u
// (spectrally accurate for this smooth periodic integrand). Independent of the page's resampling. Run: node notes/fig08/eight_exact.cjs
'use strict';
const TAU = 2 * Math.PI, M = 1 << 18;
const x = u => 0.85 * Math.sin(u), y = u => 0.85 * Math.sin(u) * Math.cos(u);
const sp = u => Math.hypot(0.85 * Math.cos(u), 0.85 * Math.cos(2 * u));
const s = new Float64Array(M + 1); // arc length at u_i by trapezoid on the speed (accurate: periodic, smooth)
let L = 0; const v = []; for (let i = 0; i <= M; i++) v.push(sp(TAU * i / M));
for (let i = 1; i <= M; i++) { L += 0.5 * (v[i - 1] + v[i]) * TAU / M; s[i] = L; }
let mx = 0, my = 0; for (let i = 0; i < M; i++) { mx += x(TAU * i / M) * v[i]; my += y(TAU * i / M) * v[i]; } mx *= TAU / M / L; my *= TAU / M / L;
const out = [];
for (const k of [1, 10, 20, 30, 40, 60]) {
    let re = 0, im = 0;
    for (let i = 0; i < M; i++) { const u = TAU * i / M, t = TAU * s[i] / L, w = v[i] * TAU / M / L; const X = x(u) - mx, Y = y(u) - my, c = Math.cos(k * t), sn = Math.sin(k * t); re += (X * c + Y * sn) * w; im += (Y * c - X * sn) * w; }
    out.push([k, Math.hypot(re, im)]);
}
console.log(JSON.stringify({ L, radii: out }));
