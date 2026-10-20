// Fig. 7: the numbers the note quotes, recomputed with the page's own sumAt() (phasor-sums.html L813-825).
// Run: node notes/fig07/numbers.cjs
'use strict';
const PI = Math.PI, TAU = 2 * PI;
function wrap(v) { return ((v % TAU) + TAU) % TAU; }
function sumAt(time, list) { let x = 0, y = 0; for (const p of list) { const a = p.freq * time + p.phase; x += p.amp * Math.cos(a); y += p.amp * Math.sin(a); } return { x, y }; }
const P = l => l.map(p => ({ amp: p[0], freq: p[1], phase: wrap(p[2] || 0) }));
const rose3 = P([[1, 4, -PI / 2], [1, -2, PI / 2]]), beat = P([[1.1, 5, 0], [1.1, 6, 0.1]]), star = P([[1, 1, 0], [0.5, -4, 0], [0.18, 6, 0]]);
const out = {};
// Fig. 3: |z| from (6) against (10), 0..20 s step 0.025
let e10 = 0; for (let i = 0; i <= 800; i++) { const t = i * 0.025, z = sumAt(t, beat); e10 = Math.max(e10, Math.abs(Math.hypot(z.x, z.y) - 2.2 * Math.abs(Math.cos(t / 2 + 0.05)))); }
out.fig3_max_diff_eq10 = e10;
out.fig3_zeros = [0, 1, 2].map(k => +(PI - 0.1 + 2 * PI * k).toFixed(3));
// Fig. 4: closure z(T) - z(0)
for (const [nm, L, T] of [['rose3', rose3, PI], ['star', star, TAU]]) { const a = sumAt(0, L), b = sumAt(1500 / 1500 * T, L); out['fig4_closure_' + nm] = Math.hypot(a.x - b.x, a.y - b.y); }
// Fig. 5: |z|^2 range for the Star
let mn = 1e9, mx = -1e9; for (let i = 0; i <= 1e6; i++) { const z = sumAt(i / 1e6 * TAU, star), r = z.x * z.x + z.y * z.y; mn = Math.min(mn, r); mx = Math.max(mx, r); }
out.fig5_min_max = [mn, mx];
// section 7: trail chord error for the 3-petal rose at speeds 1 and 4, 60 fps
function chordErr(L, h, T) { let worst = 0; for (let t0 = 0; t0 < T; t0 += h) { const a = sumAt(t0, L), b = sumAt(t0 + h, L), dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy); for (let j = 1; j < 20; j++) { const z = sumAt(t0 + h * j / 20, L); const dist = Math.abs((z.x - a.x) * dy - (z.y - a.y) * dx) / d; worst = Math.max(worst, dist); } } return worst; }
out.trail_err_speed1 = chordErr(rose3, 1 / 60, PI);
out.trail_err_speed4 = chordErr(rose3, 4 / 60, PI);
out.trail_err_px_1440 = [out.trail_err_speed1 * 132.22, out.trail_err_speed4 * 132.22];
// section 7.1: morph time constant and 1 % frames
const al = 0.08; out.morph_tau_frames = -1 / Math.log(1 - al); out.morph_1pc_frames = Math.ceil(Math.log(0.01) / Math.log(1 - al));
// section 4, Exercise 4.1
out.ex41 = { z0: Math.hypot(sumAt(0, beat).x, sumAt(0, beat).y), back: 2 * PI - 0.1, T55: TAU / 0.5, z2: 2.2 * Math.cos(0.05), z2sq: Math.pow(2.2 * Math.cos(0.05), 2) };
console.log(JSON.stringify(out, null, 1));
