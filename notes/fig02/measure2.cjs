// Fig. 2 measurements, part 2: Lyapunov robustness, drift limits. Same physics lines as measure.cjs (copied from the page).
// Run: node notes/fig02/measure2.cjs
'use strict';
const g = 9.81, m1 = 1, l1 = 1, H = 1 / 600;
let m2 = 1, l2 = 1;
function deriv(s) {
    var t1 = s[0], t2 = s[1], o1 = s[2], o2 = s[3], d = t1 - t2;
    var den = 2 * m1 + m2 - m2 * Math.cos(2 * d);
    var a1 = (-g * (2 * m1 + m2) * Math.sin(t1) - m2 * g * Math.sin(t1 - 2 * t2)
        - 2 * Math.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * l1 * Math.cos(d))) / (l1 * den);
    var a2 = (2 * Math.sin(d) * (o1 * o1 * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1)
        + o2 * o2 * l2 * m2 * Math.cos(d))) / (l2 * den);
    return [o1, o2, a1, a2];
}
function rk4(s, h) {
    var k1 = deriv(s), i, s2 = [], s3 = [], s4 = [], out = [];
    for (i = 0; i < 4; i++) s2[i] = s[i] + h / 2 * k1[i];
    var k2 = deriv(s2);
    for (i = 0; i < 4; i++) s3[i] = s[i] + h / 2 * k2[i];
    var k3 = deriv(s3);
    for (i = 0; i < 4; i++) s4[i] = s[i] + h * k3[i];
    var k4 = deriv(s4);
    for (i = 0; i < 4; i++) out[i] = s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
    return out;
}
function energy(s) {
    var kin = 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3]
        + m2 * l1 * l2 * s[2] * s[3] * Math.cos(s[0] - s[1]);
    var pot = -(m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
    return kin + pot;
}
const rad = Math.PI / 180, def = [120 * rad, 150 * rad, 0, 0];
function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3]); }
const R = {};

// drift: every step, and the first frame (10 steps) where |eps| > 1e-7
(function () {
    const E0 = energy(def), Es = (m1 + m2) * g * l1 + m2 * g * l2;
    let s = def.slice(), mx = -1, mxT = 0, first = null;
    for (let k = 1; k <= 600 * 600; k++) {
        s = rk4(s, H);
        const e = (energy(s) - E0) / Es;
        if (k <= 20 * 600 && e > mx) { mx = e; mxT = k * H; }
        if (first === null && k % 10 === 0 && Math.abs(e) > 1e-7) first = k * H;
    }
    R.drift_every_step_max_20s = [mx, mxT];
    R.first_frame_abs_eps_over_1e7_s = first;
})();

// Lyapunov exponent, Benettin, varied settings
function lyap(s0, T, d0, renorm, dir, h) {
    h = h || H;
    let a = s0.slice(), b = s0.map((v, i) => v + d0 * dir[i]), sum = 0;
    const N = Math.round(T / h), every = Math.round(renorm / h);
    for (let k = 1; k <= N; k++) {
        a = rk4(a, h); b = rk4(b, h);
        if (k % every === 0) { const dd = dist(a, b); sum += Math.log(dd / d0); b = a.map((v, i) => v + (b[i] - v) * d0 / dd); }
    }
    return sum / T;
}
const n4 = Math.hypot(1, 1, 1, 1);
R.lyap = {
    'T1000_d1e-8_r0.1_dirTh1': lyap(def, 1000, 1e-8, 0.1, [1, 0, 0, 0]),
    'T1000_d1e-8_r0.05_dirTh1': lyap(def, 1000, 1e-8, 0.05, [1, 0, 0, 0]),
    'T1000_d1e-8_r0.5_dirTh1': lyap(def, 1000, 1e-8, 0.5, [1, 0, 0, 0]),
    'T1000_d1e-6_r0.1_dirAll': lyap(def, 1000, 1e-6, 0.1, [1 / n4, 1 / n4, 1 / n4, 1 / n4]),
    'T1000_d1e-8_r0.1_dirW2': lyap(def, 1000, 1e-8, 0.1, [0, 0, 0, 1]),
    'T1000_h/2': lyap(def, 1000, 1e-8, 0.1, [1, 0, 0, 0], H / 2),
    'T4000_d1e-8_r0.1_dirTh1': lyap(def, 4000, 1e-8, 0.1, [1, 0, 0, 0])
};

// drift at the slider extremes, 20 s; ratios e^(+-2.3), e^(+-1.6); angles and velocities at their limits
let worst = { eps: 0 };
const mr = [-2.3, 0, 2.3], lr = [-1.6, 0, 1.6], ang = [-180, -90, 0, 90, 120, 150, 180], vel = [-5, 0, 5];
for (const a of mr) for (const b of lr) for (const t1 of [120, 180, 90]) for (const t2 of [150, 180, -90]) for (const o1 of vel) for (const o2 of vel) {
    m2 = m1 * Math.exp(a); l2 = l1 * Math.exp(b);
    let s = [t1 * rad, t2 * rad, o1, o2];
    const E0 = energy(s), Es = (m1 + m2) * g * l1 + m2 * g * l2;
    let mx = 0;
    for (let k = 1; k <= 20 * 600; k++) { s = rk4(s, H); if (k % 10 === 0) mx = Math.max(mx, Math.abs((energy(s) - E0) / Es)); }
    if (mx > worst.eps) worst = { eps: mx, m2, l2, t1, t2, o1, o2 };
}
R.worst_drift_20s_over_grid = worst;
console.log(JSON.stringify(R, null, 1));
