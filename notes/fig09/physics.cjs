// Fig. 9 measurements in Node. The physics lines are copied verbatim from
// public/simulations/driven-oscillator.html: constants L470, steady() L553-556, exact() L557-560,
// accel() L563-565, the solve loop L568-597. Run: node notes/fig09/physics.cjs
'use strict';
var M = 1, H = 0.001, TEND = 60, EVERY = 10, NS = TEND / H / EVERY + 1;
function steady(w0, z, W, F) {
    var X = (F / M) / Math.sqrt(Math.pow(w0 * w0 - W * W, 2) + Math.pow(2 * z * w0 * W, 2));
    return { X: X, phi: Math.atan2(2 * z * w0 * W, w0 * w0 - W * W) };
}
function exact(t, w0, z, W, st) {
    var wd = w0 * Math.sqrt(1 - z * z), C1 = -st.X * Math.cos(st.phi), C2 = (z * w0 * C1 - st.X * W * Math.sin(st.phi)) / wd;
    return st.X * Math.cos(W * t - st.phi) + Math.exp(-z * w0 * t) * (C1 * Math.cos(wd * t) + C2 * Math.sin(wd * t));
}
function accel(t, x, v, p) {
    return (p.F0 * Math.cos(p.W * t) - p.c * v - p.k * x) / M;
}
function solve(f0v, zv, F0v, fdv, Hh) {
    var Hs = Hh || H, ev = Math.round(0.01 / Hs), nsteps = Math.round(TEND / Hs);
    var w0 = 2 * Math.PI * f0v, p = { k: M * w0 * w0, c: 2 * zv * M * w0, W: 2 * Math.PI * fdv, F0: F0v };
    var ts = [], xs = [], vs = [], Es = [];
    var t = 0, x = 0, v = 0, win = 0, wloss = 0, step;
    for (step = 0; step <= nsteps; step++) {
        if (step % ev === 0) { ts.push(t); xs.push(x); vs.push(v); Es.push(0.5 * M * v * v + 0.5 * p.k * x * x); }
        if (step === nsteps) break;
        var a1 = accel(t, x, v, p), x2 = x + 0.5 * Hs * v, v2 = v + 0.5 * Hs * a1;
        var a2 = accel(t + 0.5 * Hs, x2, v2, p), x3 = x + 0.5 * Hs * v2, v3 = v + 0.5 * Hs * a2;
        var a3 = accel(t + 0.5 * Hs, x3, v3, p), x4 = x + Hs * v3, v4 = v + Hs * a3;
        var a4 = accel(t + Hs, x4, v4, p);
        var Fa = p.F0 * Math.cos(p.W * t), Fm = p.F0 * Math.cos(p.W * (t + 0.5 * Hs)), Fb = p.F0 * Math.cos(p.W * (t + Hs));
        win += Hs / 6 * (Fa * v + 2 * Fm * v2 + 2 * Fm * v3 + Fb * v4);
        wloss += Hs / 6 * p.c * (v * v + 2 * v2 * v2 + 2 * v3 * v3 + v4 * v4);
        x += Hs / 6 * (v + 2 * v2 + 2 * v3 + v4);
        v += Hs / 6 * (a1 + 2 * a2 + 2 * a3 + a4);
        t = (step + 1) * Hs;
    }
    var st = steady(w0, zv, p.W, p.F0), err = 0, xm = 0;
    for (var n = 0; n < ts.length; n++) {
        err = Math.max(err, Math.abs(xs[n] - exact(ts[n], w0, zv, p.W, st)));
        if (ts[n] >= TEND - 10) xm = Math.max(xm, Math.abs(xs[n]));
    }
    var wd = w0 * Math.sqrt(1 - zv * zv), C1 = -st.X * Math.cos(st.phi), C2 = (zv * w0 * C1 - st.X * p.W * Math.sin(st.phi)) / wd;
    return { w0: w0, p: p, st: st, ts: ts, xs: xs, vs: vs, Es: Es, win: win, wloss: wloss, err: err, xm: xm, C1: C1, C2: C2, wd: wd,
        balance: Math.abs(Es[Es.length - 1] - Es[0] - (win - wloss)) / win };
}
module.exports = { solve: solve, steady: steady, exact: exact };
if (require.main === module) {
    var R = {};
    var d = solve(0.5, 0.05, 1, 0.45);
    R.k = d.p.k; R.c = d.p.c; R.X = d.st.X; R.phi_deg = d.st.phi * 180 / Math.PI; R.tau = 1 / (0.05 * d.w0);
    R.Fk = 1 / d.p.k; R.X_over_Fk = d.st.X / (1 / d.p.k);
    R.fd_damped = d.wd / (2 * Math.PI); R.beat = 1 / Math.abs(0.45 - R.fd_damped);
    R.fr = 0.5 * Math.sqrt(1 - 2 * 0.05 * 0.05);
    R.Q = 1 / (2 * 0.05); R.X_at_res = R.Q / d.p.k;
    R.Pavg = 0.5 * d.p.c * d.p.W * d.p.W * d.st.X * d.st.X;
    R.Win = d.win; R.Wloss = d.wloss; R.dE = d.Es[d.Es.length - 1] - d.Es[0]; R.balance = d.balance; R.err = d.err; R.Xm = d.xm;
    // first swell: largest |x| in the first 15 s, and when
    var best = 0, bt = 0; for (var n = 0; n < d.ts.length; n++) if (d.ts[n] <= 15 && Math.abs(d.xs[n]) > best) { best = Math.abs(d.xs[n]); bt = d.ts[n]; }
    R.first_swell_m = best; R.first_swell_t = bt;
    // transient after 30 s
    R.transient_amp_0 = Math.hypot(d.C1, d.C2); R.transient_amp_30s = R.transient_amp_0 * Math.exp(-30 / R.tau);
    // the decay roots s = -zeta w0 +- i w0 sqrt(1 - zeta^2)
    R.root_re = -0.05 * d.w0; R.root_im = d.w0 * Math.sqrt(1 - 0.0025);
    // Exercise 6.1, second part: zeta = 0.01, f = 0.20 Hz
    var e = solve(0.5, 0.01, 1, 0.20);
    R.ex61_X = e.st.X; R.ex61_phi_deg = e.st.phi * 180 / Math.PI; R.ex61_C1 = e.C1; R.ex61_C2 = e.C2;
    R.ex61_transient_amp = Math.hypot(e.C1, e.C2); R.ex61_ratio_transient_to_X = R.ex61_transient_amp / e.st.X;
    R.ex61_tau = 1 / (0.01 * e.w0); R.ex61_transient_left_at_60s = Math.exp(-60 / R.ex61_tau);
    var mx = 0, mt = 0; for (n = 0; n < e.ts.length; n++) if (e.ts[n] <= 20 && Math.abs(e.xs[n]) > mx) { mx = Math.abs(e.xs[n]); mt = e.ts[n]; }
    R.ex61_max_abs_x_first20s = mx; R.ex61_max_at = mt; R.ex61_Xm_last10s = e.xm;
    // same at the default damping, for comparison
    var e5 = solve(0.5, 0.05, 1, 0.20); R.ex61_zeta005_ratio = Math.hypot(e5.C1, e5.C2) / e5.st.X;
    // Exercise 6.1 first part: zeta = 0.01, f = 0.45
    var b = solve(0.5, 0.01, 1, 0.45); R.ex61a_tau = 1 / (0.01 * b.w0); R.ex61a_beat_damped = 1 / Math.abs(0.45 - b.wd / (2 * Math.PI));
    // Exercise 4.1: f = f0 = 0.5, zeta 0.05 and 0.2
    var r1 = solve(0.5, 0.05, 1, 0.5), r2 = solve(0.5, 0.2, 1, 0.5);
    R.ex41_Xm_z005 = r1.xm; R.ex41_QF0k = 10 / r1.p.k; R.ex41_phi = r1.st.phi * 180 / Math.PI; R.ex41_Xm_z02 = r2.xm; R.ex41_factor = r1.xm / r2.xm;
    console.log(JSON.stringify(R, null, 1));
}
