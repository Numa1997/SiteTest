// Fig. 2 measurements, scratch. The physics lines are copied from public/simulations/Double Pendulum.html
// (deriv L479-487, rk4 L488-498, energy L499-504, the clock loop L698-722), with the page's constants.
// Run: node notes/fig02/measure.cjs
'use strict';
const fs = require('fs');
const g = 9.81, m1 = 1, l1 = 1, EPS = 0.001, H = 1 / 600;
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
function bob2(s) { return [l1 * Math.sin(s[0]) + l2 * Math.sin(s[1]), -l1 * Math.cos(s[0]) - l2 * Math.cos(s[1])]; }
const rad = Math.PI / 180;
const R = {};

// 1. Figure 3: twin separation, both starts, sampled every 30 steps (0.05 s) for 20 s
function sepRun(th1deg, th2deg, T) {
    let a = [th1deg * rad, th2deg * rad, 0, 0], b = [a[0] + EPS, a[1], 0, 0];
    const t = [0], d = [Math.hypot(...bob2(a).map((v, i) => v - bob2(b)[i]))];
    const N = Math.round(T / H);
    for (let k = 1; k <= N; k++) {
        a = rk4(a, H); b = rk4(b, H);
        if (k % 30 === 0) { const p = bob2(a), q = bob2(b); t.push(k * H); d.push(Math.hypot(p[0] - q[0], p[1] - q[1])); }
    }
    return { t, d };
}
const lo = sepRun(10, 10, 20), hi = sepRun(120, 150, 20);
// compare with the SVG path: x = 64 + 31.7 t, y = 274 - (log10 d + 4) * 51.2
const svg = JSON.parse(fs.readFileSync(__dirname + '/fig3_svg_points.json'));
function cmp(run, pts) {
    let worst = 0;
    for (let i = 0; i < pts.length; i++) {
        const y = 274 - (Math.log10(run.d[i]) + 4) * 51.2;
        const x = 64 + 31.7 * run.t[i];
        if (y > 274 || pts[i][1] > 274) continue; // clipped dips to zero
        worst = Math.max(worst, Math.abs(y - pts[i][1]), Math.abs(x - pts[i][0]));
    }
    return worst;
}
R.fig3_svg_worst_px_low = cmp(lo, svg[0]);
R.fig3_svg_worst_px_high = cmp(hi, svg[1]);
R.low_max_d_m = Math.max(...lo.d);
R.low_max_d_at_s = lo.t[lo.d.indexOf(R.low_max_d_m)];
const i01 = hi.d.findIndex(v => v >= 0.1);
R.high_first_reaches_0p1m_s = hi.t[i01];
R.high_d_at_5s = hi.d[hi.t.findIndex(v => Math.abs(v - 5) < 1e-9)];
R.high_d_at_4s = hi.d[hi.t.findIndex(v => Math.abs(v - 4) < 1e-9)];
// least-squares slope of ln d against t on several windows
function fit(run, t0, t1) {
    let n = 0, sx = 0, sy = 0, sxx = 0, sxy = 0;
    for (let i = 0; i < run.t.length; i++) if (run.t[i] >= t0 - 1e-9 && run.t[i] <= t1 + 1e-9) {
        const x = run.t[i], y = Math.log(run.d[i]); n++; sx += x; sy += y; sxx += x * x; sxy += x * y;
    }
    return (n * sxy - sx * sy) / (n * sxx - sx * sx);
}
R.fit_ln_d_0_to_reach0p1 = fit(hi, 0, R.high_first_reaches_0p1m_s);
R.fit_ln_d_1_to_4 = fit(hi, 1, 4);
R.fit_ln_d_1p3_to_4 = fit(hi, 1.3, 4);
R.fit_ln_d_0_to_4 = fit(hi, 0, 4);
R.fit_ln_d_0_to_3 = fit(hi, 0, 3);
R.fit_ln_d_0_to_5 = fit(hi, 0, 5);
R.fit_ln_d_0p5_to_4 = fit(hi, 0.5, 4);
R.endpoints_ln100_over_reach = Math.log(0.1 / 1e-3) / R.high_first_reaches_0p1m_s;
// minimum of d between 0 and 2 s
let mn = 1, mnT = 0; for (let i = 0; i < hi.t.length; i++) if (hi.t[i] <= 2 && hi.d[i] < mn) { mn = hi.d[i]; mnT = hi.t[i]; }
R.high_min_d_0_2s = mn; R.high_min_d_at = mnT;

// 2. energy drift of the default start, as the page measures it: once per frame after 10 steps (60 frames/s)
function driftRun(state, Tsec, every) {
    const E0 = energy(state), Es = (m1 + m2) * g * l1 + m2 * g * l2;
    let s = state.slice(), mx = -Infinity, mxT = 0, mnv = Infinity, mnT = 0, maxAbs = 0;
    const N = Math.round(Tsec / H);
    const samples = [];
    for (let k = 1; k <= N; k++) {
        s = rk4(s, H);
        if (k % 10 === 0) {
            const e = (energy(s) - E0) / Es;
            if (e > mx) { mx = e; mxT = k * H; }
            if (e < mnv) { mnv = e; mnT = k * H; }
            maxAbs = Math.max(maxAbs, Math.abs(e));
            if (every && k % every === 0) samples.push([+(k * H).toFixed(3), e]);
        }
    }
    return { E0, Es, max: mx, maxT: mxT, min: mnv, minT: mnT, maxAbs, samples, final: (energy(s) - E0) / Es };
}
const def = [120 * rad, 150 * rad, 0, 0];
const d20 = driftRun(def, 20);
R.drift20 = { E0: d20.E0, Escale: d20.Es, max: d20.max, maxT: d20.maxT, min: d20.min, minT: d20.minT, relToE0_maxAbs: d20.maxAbs * d20.Es / Math.abs(d20.E0) };
const dLong = driftRun(def, 600, 600 * 60);
R.drift600 = { max: dLong.max, maxT: dLong.maxT, min: dLong.min, minT: dLong.minT, maxAbs: dLong.maxAbs, final: dLong.final, perMinute: dLong.samples };

// 3. halving the step: the error at t = 4 s and 10 s, h against h/2 against h/4 (the fixed-time h^4 claim)
function stateAt(s0, h, T) { let s = s0.slice(); const N = Math.round(T / h); for (let k = 0; k < N; k++) s = rk4(s, h); return s; }
function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3]); }
for (const T of [1, 4, 10]) {
    const a = stateAt(def, H, T), b = stateAt(def, H / 2, T), c = stateAt(def, H / 4, T), ref = stateAt(def, H / 16, T);
    R['err_T' + T] = { h: dist(a, ref), h2: dist(b, ref), h4: dist(c, ref), ratio_h_h2: dist(a, ref) / dist(b, ref) };
}

// 4. largest Lyapunov exponent of the default start (Benettin): renormalise a 1e-8 full-state perturbation every 0.1 s
function lyap(s0, T, d0, renorm) {
    let a = s0.slice(), b = s0.map((v, i) => v + (i === 0 ? d0 : 0)), sum = 0;
    const N = Math.round(T / H), every = Math.round(renorm / H);
    const trace = [];
    for (let k = 1; k <= N; k++) {
        a = rk4(a, H); b = rk4(b, H);
        if (k % every === 0) {
            const dd = dist(a, b); sum += Math.log(dd / d0);
            b = a.map((v, i) => v + (b[i] - v) * d0 / dd);
            if (k % Math.round(100 / H) === 0) trace.push([k * H, sum / (k * H)]);
        }
    }
    return { lambda: sum / T, trace };
}
const L = lyap(def, 1000, 1e-8, 0.1);
R.lyapunov_default_1000s = L.lambda; R.lyapunov_trace = L.trace;
const L20 = lyap(def, 20, 1e-8, 0.1); R.lyapunov_default_first20s = L20.lambda;
const L4 = lyap(def, 4, 1e-8, 0.1); R.lyapunov_default_first4s = L4.lambda;

fs.writeFileSync(__dirname + '/measure-out.json', JSON.stringify(R, null, 1));
console.log(JSON.stringify(R, null, 1));
