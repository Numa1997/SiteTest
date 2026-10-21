// Fig. 3 numbers, computed with the page's own formulas (page:620-634, 708-718, 754-772).
// Run: node notes/fig03/check.cjs
'use strict';
const DEG = Math.PI / 180, X0 = 300, Y0 = 370;
function compute(d, adeg, b) {
    const a = adeg * DEG;
    const S1 = { x: X0 - b / 2, y: Y0 }, S2 = { x: X0 + b / 2, y: Y0 };
    const P = { x: X0 - d * Math.tan(a), y: Y0 - d };
    const L1 = Math.hypot(S1.x - P.x, S1.y - P.y), L2 = Math.hypot(S2.x - P.x, S2.y - P.y);
    const ds = 2 * b * d * Math.tan(a) / (L1 + L2);
    // angle between the two paths at P
    const v1 = { x: P.x - S1.x, y: P.y - S1.y }, v2 = { x: P.x - S2.x, y: P.y - S2.y };
    const gamma = Math.acos((v1.x * v2.x + v1.y * v2.y) / (L1 * L2));
    return { L1, L2, ds, ff: b * Math.sin(a), gamma, r: d / Math.cos(a) };
}
const out = {};
const g = compute(200, 20, 40);
out.defaults = { L1: g.L1, L2: g.L2, ds: g.ds, ff: g.ff, rel: (g.ff - g.ds) / g.ds, errLam: (g.ff - g.ds) / 13.5,
    corr5: g.ff * (1 - 40 * 40 * Math.cos(20 * DEG) ** 2 / (8 * g.r * g.r)), gamma_deg: g.gamma / DEG };
// Figure 2 caption: where the shortcut is within 1 %
let d1 = null; for (let d = 1; d <= 300; d += 0.01) { const q = compute(d, 20, 40); if ((q.ff - q.ds) / q.ds <= 0.01) { d1 = d; break; } }
const q100 = compute(100, 20, 40);
out.fig2 = { d_1pct: d1, r_over_b: d1 / Math.cos(20 * DEG) / 40, rel_at_100: (q100.ff - q100.ds) / q100.ds };
// Exercise 4.1
const e1 = compute(100, 30, 80), e3 = compute(300, 30, 80);
out.ex41 = { ds100: e1.ds, ff: e1.ff, rel: (e1.ff - e1.ds) / e1.ds, err100: e1.ff - e1.ds, ds300: e3.ds, err300: e3.ff - e3.ds, drop: (e1.ff - e1.ds) / (e3.ff - e3.ds), b_over_r: 80 / e1.r };
// Exercise 5.1: ratio at slider steps, verdicts
function verdict(ratio) { const f = ratio - Math.floor(ratio); if (f < 0.08 || f > 0.92) return 'C m=' + Math.round(ratio); if (Math.abs(f - 0.5) < 0.08) return 'D'; return 'P ' + Math.cos(Math.PI * ratio) ** 2; }
out.ex51 = {};
for (const a of [9, 9.5, 10, 10.5, 19, 19.5, 20, 20.5]) { const q = compute(200, a, 40), r = q.ds / 13.5; out.ex51[a] = [r.toFixed(4), verdict(r)]; }
function root(f, lo, hi) { for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (f(lo) * f(m) <= 0) hi = m; else lo = m; } return (lo + hi) / 2; }
out.ex51.far = [Math.asin(13.5 / 80) / DEG, Math.asin(13.5 / 40) / DEG];
out.ex51.exact200 = [root(a => compute(200, a, 40).ds - 6.75, 5, 15), root(a => compute(200, a, 40).ds - 13.5, 15, 25)];
out.ex51.exact100 = root(a => compute(100, a, 40).ds - 13.5, 15, 25);
// fringe spacing (9) and the page's first-fringe crossing m_x[1] = d tan(theta_1)
out.eq9 = { lamdb: 13.5 * 200 / 40, x1: 200 * Math.tan(Math.asin(13.5 / 40)), x1exact: 200 * Math.tan(out.ex51.exact200[1] * DEG),
    tan_over_sin: Math.tan(Math.asin(13.5 / 40)) / (13.5 / 40), HeNe_mm: 633e-9 * 1 / 0.25e-3 * 1e3 };
// Section 10: dark fringe for the defaults
const ad = out.ex51.exact200[0], dk = compute(200, ad, 40);
const amp = Math.sqrt(dk.L1 / dk.L2);
out.limits = { alpha_dark: ad, L1: dk.L1, L2: dk.L2, ampdiff: 1 - amp, Imin: ((1 - amp) / (1 + amp)) ** 2,
    gamma_deg: dk.gamma / DEG, sin2half: Math.sin(dk.gamma / 2) ** 2, tan2half: Math.tan(dk.gamma / 2) ** 2,
    gamma_lawcos_deg: Math.acos((dk.L1 ** 2 + dk.L2 ** 2 - 1600) / (2 * dk.L1 * dk.L2)) / DEG,
    gamma_alpha10: compute(200, 10, 40).gamma / DEG, gamma_far_est_deg: 40 * Math.cos(ad * DEG) / (200 / Math.cos(ad * DEG)) / DEG };
// gamma range over all slider settings
let gmin = 1e9, gmax = 0, gw = null;
for (let d = 100; d <= 300; d++) for (let a = 0; a <= 30; a += 0.5) for (let b = 20; b <= 80; b++) { const q = compute(d, a, b).gamma / DEG; if (q > gmax) { gmax = q; gw = [d, a, b]; } if (q < gmin) gmin = q; }
out.gammaRange = { gmin, gmax, gw };
// Section 6
function env(w, th, lam) { const be = Math.PI * w * Math.sin(th) / lam; return be === 0 ? 1 : (Math.sin(be) / be) ** 2; }
out.width = { e8_30: env(8, 30 * DEG, 13.5), e8_90: env(8, 90 * DEG, 13.5), e8_t1: env(8, Math.asin(13.5 / 40), 13.5), e20_t1: env(20, Math.asin(13.5 / 40), 13.5), t2: Math.asin(27 / 40) / DEG };
// Section 7: expected counts by (12) on -30..30 deg
function Ifar(th) { return Math.cos(Math.PI * 40 * Math.sin(th) / 13.5) ** 2; }
function integ(a, b) { const n = 200000; let s = 0; for (let i = 0; i < n; i++) { const t = a + (b - a) * (i + 0.5) / n; s += Ifar(t); } return s * (b - a) / n; }
const Z = integ(-30 * DEG, 30 * DEG), td = Math.asin(13.5 / 80);
out.dots = { centre: 2000 * integ(-1 * DEG, 1 * DEG) / Z, dark: 2000 * 2 * integ(td - 1 * DEG, td + 1 * DEG) / Z, td_deg: td / DEG };
// Section 8: samples per fringe at b=80, lambda=8
out.samples = Math.asin(8 / 80) / DEG / 0.1;
// Section 7 de Broglie
const h = 6.62607015e-34, me = 9.1093837015e-31, e = 1.602176634e-19;
out.deBroglie = { lam_nm: h / Math.sqrt(2 * me * e * 100) * 1e9, ratio: 550 / (h / Math.sqrt(2 * me * e * 100) * 1e9) };
// Section 9
out.scale = { b_over_lam: 40 / 13.5, slits_um: 40 / 13.5 * 0.633, lab_waves: 0.25e-3 / 633e-9, lab_theta1: Math.asin(633e-9 / 0.25e-3) / DEG, slow: 3e8 / 550e-9 / 0.8 };
// max |ds - (L2-L1)| over every slider setting
let worst = 0; for (let d = 100; d <= 300; d++) for (let a = 0; a <= 30; a += 0.5) for (let b = 20; b <= 80; b++) { const q = compute(d, a, b); worst = Math.max(worst, Math.abs(q.ds - (q.L2 - q.L1))); }
out.cancel = worst;
console.log(JSON.stringify(out, null, 1));
