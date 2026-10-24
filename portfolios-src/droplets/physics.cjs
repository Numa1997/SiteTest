/* Droplet Collection: the model. Plain JavaScript, no DOM. Node runs it with require(); build.py inlines the
   block between PHYSICS-BEGIN and PHYSICS-END into the page, where it defines the global PHYS.
   SI units throughout (m, kg, s, Pa, K). Each section names the ladder level it belongs to. */
/*PHYSICS-BEGIN*/
var PHYS = (function () {
  'use strict';
  var G0 = 9.81;            // m/s², standard gravity (rounded as in the thesis)
  var RHO_W = 1000.0;       // kg/m³, liquid water (the thesis's value; 999.7 at 10 °C, a 0.03 % difference)
  var RHO_I = 900.0;        // kg/m³, ice spheres (the thesis's value)
  var R_D = 287.05;         // J/(kg K), gas constant of dry air
  var K_B = 1.380649e-23;   // J/K, Boltzmann's constant

  // ---------------------------------------------------------------- the air (all levels)
  // Ideal-gas density and Sutherland's viscosity law with the thesis's constants (thesis eq. 20).
  function air(T, p) {
    var rho = p / (R_D * T);
    var mu = 1.72e-5 * Math.pow(T / 273, 1.5) * (273 + 120) / (T + 120);
    return { T: T, p: p, rho: rho, mu: mu, nu: mu / rho };
  }
  // Surface tension of water, IAPWS (2014) release: sigma = B tau^mu (1 + b tau), tau = 1 - T/Tc.
  function sigmaWater(T) {
    var tau = 1 - T / 647.096;
    return 0.2358 * Math.pow(tau, 1.256) * (1 - 0.625 * tau);
  }
  function massOf(r, rho) { return 4 / 3 * Math.PI * (rho || RHO_W) * r * r * r; }
  function radiusOf(m, rho) { return Math.cbrt(3 * m / (4 * Math.PI * (rho || RHO_W))); }

  // ---------------------------------------------------------------- L0: Stokes fall speed, one collector
  // Weight less buoyancy against Stokes drag 6 pi mu a v:  v = k a²,  k = 2 (rho_p - rho_a) g / (9 mu).
  function stokesK(A, rhoP) { return 2 * ((rhoP || RHO_W) - A.rho) * G0 / (9 * A.mu); }
  function vStokes(a, A, rhoP) { return stokesK(A, rhoP) * a * a; }
  function tauP(a, A, rhoP) { return 2 * (rhoP || RHO_W) * a * a / (9 * A.mu); }
  function reynolds(a, v, A) { return 2 * a * A.rho * v / A.mu; }

  // Open cloud, E constant, finite droplet radius r:  dR/dt = (E k W / 4 rho_w) (R + r)^3 (R - r) / R^2   (L0.2)
  // t(R) = (4 rho_w / E k W) [F(R) - F(R0)],  F(R) = ln((R - r)/(R + r))/(8 r) - (3R + 2r)/(4 (R + r)^2)   (L0.4)
  function L0F(R, r) { return Math.log((R - r) / (R + r)) / (8 * r) - (3 * R + 2 * r) / (4 * (R + r) * (R + r)); }
  function L0time(R0, R1, r, W, A, E) {
    var k = stokesK(A), e = E === undefined ? 1 : E;
    return 4 * RHO_W / (e * k * W) * (L0F(R1, r) - L0F(R0, r));
  }
  function L0blowup(R0, r, W, A, E) {      // R -> infinity: F -> 0
    var k = stokesK(A), e = E === undefined ? 1 : E;
    return 4 * RHO_W / (e * k * W) * (0 - L0F(R0, r));
  }
  function L0radius(t, R0, W, A, E) {      // r << R:  R(t) = R0 / (1 - c R0 t), c = E k W / (4 rho_w)   (L0.3)
    var c = (E === undefined ? 1 : E) * stokesK(A) * W / (4 * RHO_W);
    var d = 1 - c * R0 * t;
    return d > 0 ? R0 / d : Infinity;
  }
  // Closed box, Nc identical collectors, r << R:  dR/dt = (pi E k Nc / 3) R^2 (Rm^3 - R^3)   (L0.5)
  function L0box(R0, Nc, W0, A, E) {
    var Rm = Math.cbrt(R0 * R0 * R0 + W0 / (Nc * 4 / 3 * Math.PI * RHO_W));
    var Acoef = Math.PI * (E === undefined ? 1 : E) * stokesK(A) * Nc / 3;
    function G(R) {          // antiderivative of 1/(R^2 (Rm^3 - R^3)), real form (SymPy, Wolfram)
      var s3 = Math.sqrt(3);
      return (R * (-2 * Math.log(Rm - R) + Math.log(R * R + R * Rm + Rm * Rm) - 2 * s3 * Math.atan(s3 * (2 * R + Rm) / (3 * Rm))) / 6 - Rm) / (R * Math.pow(Rm, 4));
    }
    return {
      Rm: Rm,
      timeTo: function (R) { return (G(R) - G(R0)) / Acoef; },
      fraction: function (R) { return Math.pow(R / Rm, 3); }
    };
  }

  // ---------------------------------------------------------------- L1: Beard (1976) terminal speed
  // Regime 1 (d < 19 um): Stokes with slip. Regime 2 (19 um - 1.07 mm, and all ice): ln(Re/Csc) = sum b_k (ln N_Da)^k.
  // Regime 3 (liquid, d >= 1.07 mm): Re = N_P^(1/6) exp(sum c_k Y^k), Y = ln(Bo N_P^(1/6)). a is the radius.
  var B2 = [-3.18657, 0.992696, -1.53193e-3, -9.87059e-4, -5.78878e-4, 8.55176e-5, -3.27815e-6];
  var B3 = [-5.00015, 5.23778, -2.04914, 0.475294, -0.0542819, 0.00238449];
  function meanFreePath(A) { return 6.62e-8 * (A.mu / 1.818e-5) * (101325 / A.p) * Math.sqrt(A.T / 293.15); }
  function vBeard(a, A, rhoP) {
    rhoP = rhoP || RHO_W;
    var d = 2 * a, dr = rhoP - A.rho, csc = 1 + 2.51 * meanFreePath(A) / d, k, Y, X;
    if (d < 19e-6) return dr * G0 / (18 * A.mu) * csc * d * d;
    if (d < 1.07e-3 || rhoP !== RHO_W) {
      X = Math.log(4 * A.rho * dr * G0 / (3 * A.mu * A.mu) * d * d * d);
      Y = 0; for (k = 6; k >= 0; k--) Y = Y * X + B2[k];
      return A.mu * csc * Math.exp(Y) / (A.rho * d);
    }
    var s = sigmaWater(A.T), Bo = 4 * dr * G0 * d * d / (3 * s), NP = s * s * s * A.rho * A.rho / (Math.pow(A.mu, 4) * dr * G0);
    X = Math.log(Bo * Math.pow(NP, 1 / 6));
    Y = 0; for (k = 5; k >= 0; k--) Y = Y * X + B3[k];
    return A.mu * Math.pow(NP, 1 / 6) * Math.exp(Y) / (A.rho * d);
  }
  function vTerminal(a, A, law, rhoP) { return law === 'stokes' ? vStokes(a, A, rhoP) : vBeard(a, A, rhoP); }

  // ---------------------------------------------------------------- L2: collision efficiency from trajectories
  // Collector frame, lengths in R, speeds in U = v(R), time in R/U. Partner: dy/ds = w, St dw/ds = a(y) - w - S e_z,
  // St = tau U / R, S = v(r)/U, tau = v(r)/g* (drag-corrected). Contact at |y| = 1 + p. Superposition (collector's flow only).
  function flowA(flow, x, z, out) {
    var q2 = x * x + z * z, q = Math.sqrt(q2), q3 = q2 * q, c = z / q, s = x / q, ur, ut;
    if (flow === 'potential') { ur = c * (1 - 1 / q3); ut = -s * (1 + 0.5 / q3); }
    else { ur = c * (1 - 1.5 / q + 0.5 / q3); ut = -s * (1 - 0.75 / q - 0.25 / q3); }
    out[0] = ur * s + ut * c; out[1] = ur * c - ut * s;
  }
  function psi(flow, x, z) {
    var q = Math.sqrt(x * x + z * z), s = x / q;
    return 0.5 * q * q * s * s * (flow === 'potential' ? 1 - 1 / (q * q * q) : 1 - 1.5 / q + 0.5 / (q * q * q));
  }
  var DA = [[], [1 / 5], [3 / 40, 9 / 40], [44 / 45, -56 / 15, 32 / 9], [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
    [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656], [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84]];
  var DB5 = [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0];
  var DB4 = [5179 / 57600, 0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40];
  // One Dormand-Prince trajectory: returns true if the partner touches the collector.
  function trajHits(flow, St, S, p, b, Z) {
    var rc = 1 + p, aa = [0, 0], inertialess = St < 1e-3, nd = inertialess ? 2 : 4;
    var y = new Float64Array(4), yi = new Float64Array(4), y5 = new Float64Array(4), k = [], i, j, d, n;
    for (i = 0; i < 7; i++) k.push(new Float64Array(4));
    y[0] = b; y[1] = -Z; flowA(flow, y[0], y[1], aa); y[2] = aa[0]; y[3] = aa[1] - S;
    var h = inertialess ? 0.05 : 0.02 * St;
    function f(yy, out) {
      flowA(flow, yy[0], yy[1], aa);
      if (inertialess) { out[0] = aa[0]; out[1] = aa[1] - S; }
      else { out[0] = yy[2]; out[1] = yy[3]; out[2] = (aa[0] - yy[2]) / St; out[3] = (aa[1] - yy[3] - S) / St; }
    }
    for (n = 0; n < 5e6; n++) {
      for (i = 0; i < 7; i++) {
        for (d = 0; d < nd; d++) { yi[d] = y[d]; for (j = 0; j < i; j++) yi[d] += h * DA[i][j] * k[j][d]; }
        f(yi, k[i]);
      }
      var dist0 = Math.sqrt(y[0] * y[0] + y[1] * y[1]) - rc, err = 0;
      for (d = 0; d < nd; d++) {
        var e = 0; y5[d] = y[d];
        for (i = 0; i < 7; i++) { y5[d] += h * DB5[i] * k[i][d]; e += h * (DB5[i] - DB4[i]) * k[i][d]; }
        var sc = d < 2 ? 1e-9 + 1e-7 * Math.max(0, Math.min(Math.abs(dist0), 10)) : 1e-8 + 1e-7 * Math.abs(y[d]);
        err = Math.max(err, Math.abs(e) / sc);
      }
      if (err <= 1) {
        for (d = 0; d < nd; d++) y[d] = y5[d];
        if (Math.sqrt(y[0] * y[0] + y[1] * y[1]) <= rc) return true;
        if (y[1] > rc) return false;
      }
      h *= Math.min(4, Math.max(0.2, 0.9 * Math.pow(1 / (err + 1e-300), 0.2)));
    }
    throw new Error('trajectory did not finish');
  }
  // The path of one partner (for drawing): fixed-step RK4 in the scaled variables, from z = -Z, stopping at contact or above the
  // collector. Returns { x: [...], z: [...], hit }.
  function trajPath(flow, St, S, p, b, Z, maxPts) {
    var rc = 1 + p, aa = [0, 0], y = [b, -Z, 0, 0], xs = [], zs = [], n;
    flowA(flow, b, -Z, aa); y[2] = aa[0]; y[3] = aa[1] - S;
    function f(q) { flowA(flow, q[0], q[1], aa); return St < 1e-3 ? [aa[0], aa[1] - S, 0, 0] : [q[2], q[3], (aa[0] - q[2]) / St, (aa[1] - q[3] - S) / St]; }
    for (n = 0; n < 400000; n++) {
      var gap = Math.sqrt(y[0] * y[0] + y[1] * y[1]) - rc, h = Math.min(0.05, 0.02 * Math.max(gap, 0.02)); if (St >= 1e-3) h = Math.min(h, 0.1 * St);
      if (n % 4 === 0) { xs.push(y[0]); zs.push(y[1]); }
      var k1 = f(y), y2 = y.map(function (v, i) { return v + h / 2 * k1[i]; }), k2 = f(y2), y3 = y.map(function (v, i) { return v + h / 2 * k2[i]; }), k3 = f(y3);
      var y4 = y.map(function (v, i) { return v + h * k3[i]; }), k4 = f(y4);
      y = y.map(function (v, i) { return v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]); });
      if (St < 1e-3) { flowA(flow, y[0], y[1], aa); y[2] = aa[0]; y[3] = aa[1] - S; }
      if (Math.sqrt(y[0] * y[0] + y[1] * y[1]) <= rc) { xs.push(y[0]); zs.push(y[1]); return { x: xs, z: zs, hit: true }; }
      if (y[1] > (maxPts || 3)) { xs.push(y[0]); zs.push(y[1]); return { x: xs, z: zs, hit: false }; }
    }
    return { x: xs, z: zs, hit: false };
  }
  // Efficiency in one flow: bisection on the start offset b, then the partner flux through the start disc.
  function flowEfficiency(flow, St, S, p, Z) {
    var rc = 1 + p, lo = 0, hi = rc * 1.5, it;
    if (!trajHits(flow, St, S, p, 1e-6, Z)) return { E: 0, bc: 0 };
    while (trajHits(flow, St, S, p, hi, Z)) hi *= 1.5;
    for (it = 0; it < 60 && hi - lo > 1e-7 * rc; it++) {
      var mid = 0.5 * (lo + hi);
      if (trajHits(flow, St, S, p, mid, Z)) lo = mid; else hi = mid;
    }
    var bc = 0.5 * (lo + hi);
    return { E: 2 * (psi(flow, bc, -Z) - 0.5 * S * bc * bc) / ((1 - S) * rc * rc), bc: bc };
  }
  // Critical Stokes number of a point partner (p = 0, S = 0) on the upstream axis, in log variables xi = ln(gap), u = w/gap.
  function axisHits(flow, St, Z) {
    var A0 = function (q) { return flow === 'potential' ? -(1 - 1 / (q * q * q)) : -(1 - 1.5 / q + 0.5 / (q * q * q)); };
    var cOf = function (xi) { var eta = Math.exp(xi); return eta > 1e-6 ? A0(1 + eta) / eta : (flow === 'potential' ? -3 + 6 * eta : -1.5 * eta); };
    var y = [Math.log(Z), 0], h = 1e-3 * St, n, i, j, d, k = [];
    y[1] = cOf(y[0]);
    var f = function (yy) { return [yy[1], (cOf(yy[0]) - yy[1]) / St - yy[1] * yy[1]]; };
    for (n = 0; n < 2e7; n++) {
      k = [];
      for (i = 0; i < 7; i++) {
        var yi = [y[0], y[1]];
        for (j = 0; j < i; j++) for (d = 0; d < 2; d++) yi[d] += h * DA[i][j] * k[j][d];
        k.push(f(yi));
      }
      var y5 = [y[0], y[1]], err = 0;
      for (d = 0; d < 2; d++) {
        var e = 0;
        for (i = 0; i < 7; i++) { y5[d] += h * DB5[i] * k[i][d]; e += h * (DB5[i] - DB4[i]) * k[i][d]; }
        err = Math.max(err, Math.abs(e) / (1e-10 + 1e-10 * Math.abs(y[d])));
      }
      if (err <= 1) {
        y = y5;
        if (y[1] < -1e6 / St) return true;
        var eta = Math.exp(y[0]), c = cOf(y[0]), disc = 1 + 4 * St * c;
        if (flow !== 'potential' && eta < 1e-3) {
          if (y[1] < -1 / St) return true;
          if (disc >= 0 && y[1] > (-1 - Math.sqrt(disc)) / (2 * St)) return false;
        }
        if (flow === 'potential' && eta < 1e-8) return disc < 0 ? true : y[1] < (-1 - Math.sqrt(disc)) / (2 * St);
      }
      h *= Math.min(4, Math.max(0.2, 0.9 * Math.pow(1 / (err + 1e-300), 0.2)));
    }
    throw new Error('axis trajectory did not finish');
  }
  function criticalStokes(flow, Z) {
    var lo = flow === 'potential' ? 0.02 : 0.5, hi = flow === 'potential' ? 0.3 : 3, it;
    for (it = 0; it < 45; it++) { var mid = 0.5 * (lo + hi); if (axisHits(flow, mid, Z || 100)) hi = mid; else lo = mid; }
    return 0.5 * (lo + hi);
  }
  // Efficiency of a collector (radius R, density rhoR) for a partner (r, rhoP) in air A, Langmuir's interpolation in Re.
  function pairEfficiency(R, r, A, rhoR, rhoP) {
    rhoR = rhoR || RHO_W; rhoP = rhoP || RHO_W;
    var U = vBeard(R, A, rhoR), vr = vBeard(r, A, rhoP), gs = G0 * (1 - A.rho / rhoP);
    var St = vr / gs * U / R, S = vr / U, p = r / R, Re = 2 * R * A.rho * U / A.mu;
    if (S >= 1) return { E: 0, ES: 0, EP: 0, St: St, S: S, Re: Re };
    var es = flowEfficiency('stokes', St, S, p, 200).E, ep = flowEfficiency('potential', St, S, p, 30).E;
    return { E: (es + ep * Re / 60) / (1 + Re / 60), ES: es, EP: ep, St: St, S: S, Re: Re };
  }
  // The table: E on nR collector radii (log-spaced Rmin..Rmax) x np ratios (log-spaced pmin..pmax).
  function makeTable(A, o) {
    o = o || {};
    var nR = o.nR || 64, np = o.np || 40, Rmin = o.Rmin || 2e-6, Rmax = o.Rmax || 4e-3, pmin = o.pmin || 0.002, pmax = o.pmax || 1;
    var lnR = [], lnp = [], E = [], ES = [], EP = [], ReT = [], i, j;
    for (i = 0; i < nR; i++) lnR.push(Math.log(Rmin) + i * Math.log(Rmax / Rmin) / (nR - 1));
    for (j = 0; j < np; j++) lnp.push(Math.log(pmin) + j * Math.log(pmax / pmin) / (np - 1));
    for (i = 0; i < nR; i++) for (j = 0; j < np; j++) {
      var R = Math.exp(lnR[i]), p = Math.exp(lnp[j]);
      var pe = p >= 0.999 ? { E: 0, ES: 0, EP: 0, Re: 0 } : pairEfficiency(R, p * R, A, o.rhoR, o.rhoP);
      E.push(pe.E);
      if (o.split) { ES.push(pe.ES); EP.push(pe.EP); ReT.push(pe.Re); }   // the two flow limits kept apart (crossover studies)
    }
    var out = { T: A.T, p: A.p, rhoR: o.rhoR || RHO_W, rhoP: o.rhoP || RHO_W, lnR: lnR, lnp: lnp, E: E, version: 'L2-superposition-1' };
    if (o.split) { out.ES = ES; out.EP = EP; out.Re = ReT; }
    return out;
  }
  // Bilinear interpolation in (ln R, ln p), clamped at the edges; near: 'clamp' holds p > 0.6 at 0.6,
  // 'one' sets E = 1 above p = 0.6 for collectors of 40 um or more (the near-equal bracket).
  function tableE(tab, R, p, near) {
    if (p > 0.6) { if (near === 'one' && R >= 40e-6) return 1; p = 0.6; }
    var x = Math.log(R), y = Math.log(p), nR = tab.lnR.length, np = tab.lnp.length;
    var fx = (x - tab.lnR[0]) / (tab.lnR[1] - tab.lnR[0]), fy = (y - tab.lnp[0]) / (tab.lnp[1] - tab.lnp[0]);
    fx = Math.max(0, Math.min(nR - 1 - 1e-12, fx)); fy = Math.max(0, Math.min(np - 1 - 1e-12, fy));
    var i = Math.floor(fx), j = Math.floor(fy), a = fx - i, b = fy - j;
    var E = tab.E;
    return (1 - a) * (1 - b) * E[i * np + j] + a * (1 - b) * E[(i + 1) * np + j] + (1 - a) * b * E[i * np + j + 1] + a * b * E[(i + 1) * np + j + 1];
  }

  // ---------------------------------------------------------------- L3: coalescence
  // We = CKE / (pi sigma d_c^2), CKE = (1/2) mu_red dv^2; E_coal = exp(-1.15 We) (the thesis's law; Straub et al. 2010's form).
  function weber(a1, a2, dv, sigma, rho1, rho2) {
    var m1 = massOf(a1, rho1), m2 = massOf(a2, rho2), dc2 = Math.pow(8 * (a1 * a1 * a1 + a2 * a2 * a2), 2 / 3);
    return 0.5 * m1 * m2 / (m1 + m2) * dv * dv / (Math.PI * sigma * dc2);
  }
  function eCoal(a1, a2, dv, sigma) { return Math.exp(-1.15 * weber(a1, a2, dv, sigma)); }

  // ---------------------------------------------------------------- the kernel (L0-L3 assembled)
  // o: { speed: 'stokes'|'beard', eff: 'one'|'table'|'hall', coal: 'one'|'law', near: 'clamp'|'one', tab, hall, hallBelow }
  // hallBelow (m): with eff 'table', use Hall's values for collectors smaller than this (a test of L2's prediction 3)
  function kernel(a1, a2, A, o) {
    if (o.constant) return o.constant;   // L8 contrast: every pair equally likely (the energy-only Monte Carlo)
    var R = Math.max(a1, a2), r = Math.min(a1, a2);
    var vR = vTerminal(R, A, o.speed), vr = vTerminal(r, A, o.speed), dv = Math.abs(vR - vr);
    if (dv === 0) return 0;
    var E = 1;
    if (o.eff === 'table') E = (o.hallBelow && R < o.hallBelow) ? hallE(o.hall, R, r / R) : tableE(o.tab, R, r / R, o.near);
    else if (o.eff === 'hall') E = hallE(o.hall, R, r / R);
    var Ec = o.coal === 'law' ? eCoal(R, r, dv, sigmaWater(A.T)) : 1;
    return Math.PI * (R + r) * (R + r) * dv * E * Ec * (o.eps ? ayalaFactor(R, r, A, o.eps) : 1);
  }
  // Hall (1980) Table 1 (OCR reading in the dossier): rows collector radius (um), columns r/R = 0.05..1.00; bilinear in R and p,
  // R clamped to 10-300 um, E = 1 above 300 um (Hall's own rule), p below 0.05 scaled linearly to 0 at p = 0.
  function hallE(h, R, p) {
    var Rum = R * 1e6, rows = h.R, cols = h.p, i, j;
    if (Rum >= 300) return 1;
    Rum = Math.max(rows[0], Rum);
    for (i = 0; i < rows.length - 2 && rows[i + 1] < Rum; i++);
    var a = (Rum - rows[i]) / (rows[i + 1] - rows[i]);
    var pc = Math.min(Math.max(p, cols[0]), cols[cols.length - 1]);
    for (j = 0; j < cols.length - 2 && cols[j + 1] < pc; j++);
    var b = (pc - cols[j]) / (cols[j + 1] - cols[j]), E = h.E;
    var v = (1 - a) * (1 - b) * E[i][j] + a * (1 - b) * E[i + 1][j] + (1 - a) * b * E[i][j + 1] + a * b * E[i + 1][j + 1];
    return p < cols[0] ? v * p / cols[0] : v;
  }

  // ---------------------------------------------------------------- L6: turbulence, a stated check
  // Ayala, Rosa and Wang (2008, Part 2), weak-inertia radial relative velocity, radial distribution function taken as 1 (valid for
  // size ratios above about 1.3); returns the factor by which turbulence of dissipation rate eps (m^2/s^3) multiplies the
  // gravitational geometric kernel. Rlambda = 2e4 (cloud value), a0 = (11 + 7 Rl)/(205 + Rl).
  function ayalaFactor(a1, a2, A, eps) {
    var g = G0, t1 = vBeard(a1, A) / g, t2 = vBeard(a2, A) / g, v1 = vBeard(a1, A), v2 = vBeard(a2, A), R = a1 + a2, nu = A.nu;
    var Rl = 2e4, a0 = (11 + 7 * Rl) / (205 + Rl), tk = Math.sqrt(nu / eps), vk = Math.pow(nu * eps, 0.25), d = t1 - t2;
    // outside the theory's range the factor is set to 1 (gravity alone): near-equal pairs (r/R > 0.6, where sedimentation does not
    // dominate), drops above 60 um (the range of its DNS, 10-60 um), Stokes numbers above 1 (the weak-inertia expansion)
    if (d === 0 || Math.min(a1, a2) / Math.max(a1, a2) > 0.6 || Math.max(a1, a2) > 60e-6 || Math.max(t1, t2) / tk > 1) return 1;
    var s2 = R * R * eps / (15 * nu) + d * d * a0 * (vk / tk) * (vk / tk) + Math.pow(v1 * t1 - v2 * t2, 2) * 2 * eps / (15 * nu);
    var w = Math.sqrt(2 / Math.PI) * Math.sqrt(s2 + Math.PI / 8 * d * d * g * g), wg = 0.5 * Math.abs(d) * g;
    return w / wg;
  }

  // ---------------------------------------------------------------- L4: the SCE on a logarithmic mass grid
  function makeGrid(s, rTop) {
    var x0 = massOf(1e-6), xTop = massOf(rTop || 4e-3), x = [], k;
    for (k = 0; ; k++) { var xk = x0 * Math.pow(2, k / s); x.push(xk); if (xk >= xTop) break; }
    var r = x.map(function (m) { return radiusOf(m); });
    return { s: s, x: x, r: r, n: x.length, dlnr: Math.LN2 / (3 * s) };
  }
  // Lognormal number distribution in r: dN/dln r = N0/(sqrt(2 pi) ln sg) exp(-ln^2(r/rg)/(2 ln^2 sg)); bin number = density x dln r.
  // trunc (in units of ln sg, 0 = none) cuts each mode at |ln(r/rg)| <= trunc ln sg and rescales it to keep its number N.
  function lognormalBins(grid, modes, rhoP, trunc) {
    var N = new Float64Array(grid.n), k, m;
    for (m = 0; m < modes.length; m++) {
      var md = modes[m], ls = Math.log(md.sg), part = new Float64Array(grid.n), sum = 0;
      for (k = 0; k < grid.n; k++) {
        var z = Math.log(radiusOf(grid.x[k], rhoP) / md.rg) / ls;
        if (trunc && Math.abs(z) > trunc) continue;
        part[k] = md.N / (Math.sqrt(2 * Math.PI) * ls) * Math.exp(-z * z / 2) * grid.dlnr; sum += part[k];
      }
      var sc = trunc ? md.N / sum : 1;
      for (k = 0; k < grid.n; k++) N[k] += part[k] * sc;
    }
    return N;
  }
  function kernelMatrix(grid, A, o) {
    var n = grid.n, K = new Float64Array(n * n), i, j;
    for (i = 0; i < n; i++) for (j = i; j < n; j++) { var v = kernel(grid.r[i], grid.r[j], A, o); K[i * n + j] = v; K[j * n + i] = v; }
    return K;
  }
  // ---------------------------------------------------------------- L8: energy, entropy and who eats whom (diagnostics only)
  // Surface of a sphere 4 pi r^2 = (36 pi)^(1/3) rho_w^(-2/3) m^(2/3); E_s = sigma times the sum over drops. The ledger keeps, per
  // channel (class of the larger partner, class of the smaller), the mergers, the water eaten (the smaller partner's) and the surface
  // energy released by the exact product; the gateway water whose product crosses the top cut from a larger partner below it, by the
  // smaller partner's class (gate: the exact product crosses the cut; gateBin: the water the lever rule puts into top-class bins, which
  // closes the binned budget); the droplet-mode water per bin (tag); the overflow's exact surface (its drops never merge again).
  var SURF = Math.pow(36 * Math.PI, 1 / 3) * Math.pow(RHO_W, -2 / 3);
  function makeLedger(grid, cuts, tag0) {
    var n = grid.n, nc = cuts.length + 1, cls = new Int8Array(n), k, c, xTop = massOf(cuts[cuts.length - 1]);
    for (k = 0; k < n; k++) { c = 0; while (c < cuts.length && grid.r[k] >= cuts[c]) c++; cls[k] = c; }
    return { nc: nc, cls: cls, cuts: cuts, xTop: xTop, mergers: new Float64Array(nc * nc), eaten: new Float64Array(nc * nc),
      released: new Float64Array(nc * nc), gate: new Float64Array(nc), gateBin: new Float64Array(nc), tag: tag0 ? Float64Array.from(tag0) : null, overTag: 0, overS: 0,
      x23: grid.x.map(function (v) { return Math.pow(v, 2 / 3); }) };
  }
  function ledgerAdd(led, i, j, C, xi, xj, xs) {
    var a = led.cls[j] * led.nc + led.cls[i];
    led.mergers[a] += C; led.eaten[a] += C * xi;
    led.released[a] += C * (led.x23[i] + led.x23[j] - Math.pow(xs, 2 / 3));   // in kg^(2/3) per m^3: times sigma SURF for J/m^3
    if (xj < led.xTop && xs >= led.xTop) led.gate[led.cls[i]] += C * xs;
  }
  function surfaceSum(led, N) { var S = led.overS, k; for (k = 0; k < N.length; k++) S += N[k] * led.x23[k]; return S; }
  // Maximum entropy at fixed number N and water M (prior uniform in mass): n = (N^2/M) exp(-N m/M); with <ln m> fixed as well: the
  // gamma n = N lam^nu m^(nu-1) exp(-lam m)/Gamma(nu), nu/lam = M/N, psi(nu) - ln nu = <ln m> - ln(M/N). Bin water n(x_k) x_k^2 ln2/s
  // as in the Golovin test; the overflow (drops above the grid, counted at their mean mass) is compared with the shape's water beyond
  // the grid. Spectrum error eps = sum |M_k - M_k^ME| / M (0 for equal shapes, 2 for shapes with no overlap).
  function digamma(xv) { var r = 0; while (xv < 6) { r -= 1 / xv; xv += 1; } var f = 1 / (xv * xv); return r + Math.log(xv) - 0.5 / xv - f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f / 132)))); }
  function lnGamma(z) {
    var c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7], xx, tt, i;
    if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lnGamma(1 - z);
    z -= 1; xx = c[0]; for (i = 1; i < 9; i++) xx += c[i] / (z + i); tt = z + 7.5;
    return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(tt) - tt + Math.log(xx);
  }
  function maxentCompare(grid, N, over) {
    var n = grid.n, w = Math.LN2 / grid.s, k, Nt = over.N, Mt = over.M, L = 0;
    for (k = 0; k < n; k++) { Nt += N[k]; Mt += N[k] * grid.x[k]; L += N[k] * Math.log(grid.x[k]); }
    if (over.N > 0) L += over.N * Math.log(over.M / over.N);
    var mbar = Mt / Nt, cc = L / Nt - Math.log(mbar), lo = 1e-6, hi = 1e8, it, nu, lam;
    for (it = 0; it < 200; it++) { nu = Math.sqrt(lo * hi); if (digamma(nu) - Math.log(nu) < cc) lo = nu; else hi = nu; }
    nu = Math.sqrt(lo * hi); lam = nu / mbar;
    var Me = new Float64Array(n), Mg = new Float64Array(n), se = 0, sg = 0, eE = 0, eG = 0, lnZ = lnGamma(nu);
    for (k = 0; k < n; k++) {
      var xk = grid.x[k], Mk = N[k] * xk;
      Me[k] = Nt / mbar * Math.exp(-xk / mbar) * xk * xk * w;
      Mg[k] = Math.exp(Math.log(Nt) + nu * Math.log(lam) + (nu + 1) * Math.log(xk) - lam * xk - lnZ) * w;
      se += Me[k]; sg += Mg[k]; eE += Math.abs(Mk - Me[k]); eG += Math.abs(Mk - Mg[k]);
    }
    eE += Math.abs(over.M - Math.max(0, Mt - se)); eG += Math.abs(over.M - Math.max(0, Mt - sg));
    return { N: Nt, M: Mt, mbar: mbar, nu: nu, lam: lam, epsExp: eE / Mt, epsGamma: eG / Mt, Mexp: Me, Mgamma: Mg };
  }
  // One SCE step: pairs i <= j, smaller bin first, in place; two-bin deposit (number and mass of products); limiter; overflow.
  // State: N (number per m^3 per bin), over {N, M}; returns the number of rounding fixes.
  function sceStep(grid, K, N, over, dt, onlyPairs, led) {
    var n = grid.n, x = grid.x, i, j, fixes = 0, lastK = n - 1, fi = 0, fj = 0;
    for (i = 0; i < n; i++) {
      if (N[i] <= 0) continue;
      for (j = i; j < n; j++) {
        if (N[j] <= 0 || N[i] <= 0) continue;
        if (onlyPairs && !onlyPairs(i, j)) continue;
        var Kij = K[i * n + j]; if (Kij <= 0) continue;
        var C, xs = x[i] + x[j], kk, f;
        // bin of the product: x_kk <= xs < x_kk+1
        kk = j + Math.floor(Math.log(xs / x[j]) / Math.LN2 * grid.s);
        while (kk + 1 < n && x[kk + 1] <= xs) kk++;
        while (kk > j && x[kk] > xs) kk--;
        if (i === j) { C = 0.5 * Kij * N[i] * N[i] * dt; if (C > 0.5 * N[i]) C = 0.5 * N[i]; }
        else {
          C = Kij * N[i] * N[j] * dt;
          if (C > N[i]) C = N[i];
          f = kk < lastK ? (xs - x[kk]) / (x[kk + 1] - x[kk]) : 1;
          var capj = (kk === j && kk < lastK) ? N[j] / Math.max(f, 1e-300) : N[j];
          if (C > capj) C = capj;
        }
        if (C <= 0) continue;
        if (led) { fi = led.tag && N[i] > 0 ? led.tag[i] / (N[i] * x[i]) : 0; fj = led.tag && N[j] > 0 ? led.tag[j] / (N[j] * x[j]) : 0; ledgerAdd(led, i, j, C, x[i], x[j], xs); }
        if (i === j) N[i] -= 2 * C; else { N[i] -= C; N[j] -= C; }
        if (kk >= lastK) { over.N += C; over.M += C * xs; if (led) { led.overS += C * Math.pow(xs, 2 / 3); if (led.tag) led.overTag += C * (x[i] * fi + x[j] * fj); } }
        else {
          f = (xs - x[kk]) / (x[kk + 1] - x[kk]);
          N[kk] += (1 - f) * C; N[kk + 1] += f * C;
        }
        if (led && led.cls[j] < led.nc - 1) {   // binned gateway: water a pair below the top class deposits into top-class bins
          var top = led.nc - 1, wtop = 0;
          if (kk >= lastK) wtop = C * xs; else { if (led.cls[kk] === top) wtop += (1 - f) * C * x[kk]; if (led.cls[kk + 1] === top) wtop += f * C * x[kk + 1]; }
          led.gateBin[led.cls[i]] += wtop;
        }
        if (led && led.tag) {      // the droplet-mode water rides with the water: removed from i and j, deposited as the lever rule splits the product
          var Pt = C * (x[i] * fi + x[j] * fj);
          led.tag[i] -= C * x[i] * fi; led.tag[j] -= C * x[j] * fj;
          if (kk < lastK) { led.tag[kk] += (1 - f) * C * x[kk] * Pt / (C * xs); led.tag[kk + 1] += f * C * x[kk + 1] * Pt / (C * xs); }
        }
        if (N[i] < 0) { N[i] = 0; fixes++; }
        if (N[j] < 0) { N[j] = 0; fixes++; }
      }
    }
    return fixes;
  }
  function moments(grid, N, over) {
    var M = 0, Nt = 0, k;
    for (k = 0; k < grid.n; k++) { M += N[k] * grid.x[k]; Nt += N[k]; }
    return { M: M, N: Nt, Mall: M + over.M, Nall: Nt + over.N };
  }
  // A full SCE run: records F40 (in-grid mass at r >= 40 um over the initial mass) every recordEvery s, and snapshots.
  function sceRun(grid, A, kopt, modes, o) {
    o = o || {};
    var dt = o.dt || 1, tEnd = o.tEnd || 3600, rec = o.recordEvery || 60;
    var K = o.K || kernelMatrix(grid, A, kopt);
    var N = o.N0 ? Float64Array.from(o.N0) : lognormalBins(grid, modes, undefined, o.trunc), over = { N: 0, M: 0 };
    var M0 = moments(grid, N, over).M, out = { t: [], F40: [], F100: [], N100: [], N1mm: [], over: [], drift: [], snaps: {} };
    var k40 = grid.r.findIndex(function (r) { return r >= 40e-6; }), k100 = grid.r.findIndex(function (r) { return r >= 100e-6; });
    var k1mm = grid.r.findIndex(function (r) { return r >= 1e-3; }), fixes = 0, steps = Math.round(tEnd / dt), st;
    var snapAt = o.snapAt || [0, 600, 1200, 1800, 3600];
    function record(t) {
      var m40 = 0, m100 = 0, n100 = 0, n1 = 0, k;
      for (k = k40; k < grid.n; k++) m40 += N[k] * grid.x[k];
      for (k = k100; k < grid.n; k++) m100 += N[k] * grid.x[k];
      for (k = k100; k < grid.n; k++) n100 += N[k];
      for (k = k1mm; k < grid.n; k++) n1 += N[k];
      var mo = moments(grid, N, over);
      out.t.push(t); out.F40.push(m40 / M0); out.F100.push((m100 + over.M) / M0); out.N100.push(n100 + over.N); out.N1mm.push(n1 + over.N);
      out.over.push(over.M / M0); out.drift.push(mo.Mall / M0 - 1);
      if (snapAt.indexOf(Math.round(t)) >= 0) out.snaps[Math.round(t)] = Array.from(N);
      if (o.onRecord) o.onRecord(t, N, over, o.ledger);
    }
    record(0);
    for (st = 1; st <= steps; st++) {
      var S0 = o.ledger ? surfaceSum(o.ledger, N) : 0;
      fixes += sceStep(grid, K, N, over, dt, o.onlyPairs, o.ledger);
      if (o.ledger) { var S1 = surfaceSum(o.ledger, N); if (S1 > S0) { o.ledger.rises = (o.ledger.rises || 0) + 1; o.ledger.maxRise = Math.max(o.ledger.maxRise || 0, (S1 - S0) / S0); } }
      var t = st * dt;
      if (Math.abs(t / rec - Math.round(t / rec)) < 1e-9) record(t);
    }
    out.fixes = fixes; out.M0 = M0; out.N = N; out.overflow = over;
    out.tq = function (q) { for (var i = 0; i < out.F40.length; i++) if (out.F40[i] >= q) return out.t[i]; return null; };
    return out;
  }
  // The thesis's GCE: collector classes (fixed number, growing mass) sweep pool classes (fixed mass, depleting number).
  function gceRun(grid, A, kopt, modes, o) {
    o = o || {};
    var dt = o.dt || 1, tEnd = o.tEnd || 3600, rec = o.recordEvery || 60, k, c, pidx;
    var Nd = lognormalBins(grid, [modes[0]]), Nc = lognormalBins(grid, [modes[1]]);
    var col = [], pool = [];
    for (k = 0; k < grid.n; k++) {
      if (Nc[k] > 1e-12 * modes[1].N) col.push({ N: Nc[k], m: grid.x[k] });
      if (Nd[k] > 1e-12 * modes[0].N) pool.push({ n: Nd[k], x: grid.x[k], r: grid.r[k] });
    }
    var M0 = 0; col.forEach(function (q) { M0 += q.N * q.m; }); pool.forEach(function (q) { M0 += q.n * q.x; });
    var out = { t: [], F40: [] }, steps = Math.round(tEnd / dt), st;
    function record(t) {
      var m40 = 0;
      col.forEach(function (q) { if (radiusOf(q.m) >= 40e-6) m40 += q.N * q.m; });
      pool.forEach(function (q) { if (q.r >= 40e-6) m40 += q.n * q.x; });
      out.t.push(t); out.F40.push(m40 / M0);
    }
    record(0);
    for (st = 1; st <= steps; st++) {
      // each pool class depletes exactly, n -> n exp(-sum_c N_c K_cp dt); its lost water goes to the collectors in
      // proportion to N_c K_cp, so the water books close to rounding
      var dm = new Float64Array(col.length), Kcp = new Float64Array(col.length);
      for (pidx = 0; pidx < pool.length; pidx++) {
        var rate = 0;
        for (c = 0; c < col.length; c++) {
          var Rc = radiusOf(col[c].m);
          Kcp[c] = pool[pidx].r < Rc ? kernel(Rc, pool[pidx].r, A, kopt) : 0;
          rate += col[c].N * Kcp[c];
        }
        if (rate <= 0) continue;
        var nNew = pool[pidx].n * Math.exp(-rate * dt), lostM = (pool[pidx].n - nNew) * pool[pidx].x;
        pool[pidx].n = nNew;
        for (c = 0; c < col.length; c++) dm[c] += lostM * col[c].N * Kcp[c] / rate;   // water per m^3 of air to collector class c
      }
      for (c = 0; c < col.length; c++) col[c].m += dm[c] / col[c].N;
      var t = st * dt;
      if (Math.abs(t / rec - Math.round(t / rec)) < 1e-9) record(t);
    }
    out.M0 = M0;
    out.tq = function (q) { for (var i = 0; i < out.F40.length; i++) if (out.F40[i] >= q) return out.t[i]; return null; };
    return out;
  }
  // Golovin's exact solution for the sum kernel K = b (m + m'), exponential start n(m,0) = (N0/mbar) exp(-m/mbar):
  // n(m,t) = (N0/mbar) (1 - z)/(u sqrt z) I1(2 u sqrt z) exp(-(1 + z) u), u = m/mbar, z = 1 - exp(-b L t), L = N0 mbar.
  function besselI1e(xv) {   // I1(x) exp(-x), Abramowitz and Stegun 9.8.3 and 9.8.4
    var ax = Math.abs(xv), y, ans;
    if (ax < 3.75) {
      y = (xv / 3.75) * (xv / 3.75);
      ans = ax * (0.5 + y * (0.87890594 + y * (0.51498869 + y * (0.15084934 + y * (0.02658733 + y * (0.00301532 + y * 0.00032411))))));
      return ans * Math.exp(-ax);
    }
    y = 3.75 / ax;
    ans = 0.39894228 + y * (-0.03988024 + y * (-0.00362018 + y * (0.00163801 + y * (-0.01031555 + y * (0.02282967 + y * (-0.02895312 + y * (0.01787654 - y * 0.00420059)))))));
    return ans / Math.sqrt(ax);
  }
  function golovinDensity(m, t, b, N0, mbar) {
    var L = N0 * mbar, z = 1 - Math.exp(-b * L * t), u = m / mbar;
    if (z < 1e-12) return N0 / mbar * Math.exp(-u);
    var arg = 2 * u * Math.sqrt(z);
    return N0 / mbar * (1 - z) / (u * Math.sqrt(z)) * besselI1e(arg) * Math.exp(arg - (1 + z) * u);
  }

  // ---------------------------------------------------------------- L5: the stochastic process, sampled exactly
  // Gillespie (1975), method B (proposals accepted with probability K_ij / K*), with the particles grouped in size classes
  // and one majorant K*_ab per class pair: proposals form a Poisson process of rate A* = sum_ab K*_ab n_a n_b / V (half
  // n_a (n_a - 1) for a = b); a proposed pair is accepted with probability K_ij / K*_ab. Thinning makes the accepted events
  // exactly the coalescence process of the master equation. The bound K_ij <= K*_ab is checked at every proposal.
  function rng(seed) {      // mulberry32: a small, seeded, reproducible generator of uniforms in (0, 1)
    var a = seed >>> 0;
    return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return (((t ^ (t >>> 14)) >>> 0) + 1) / 4294967297; };
  }
  function gaussian(u) { var u1 = u(), u2 = u(); return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2); }
  // Draw radii from lognormal modes; trunc (in units of ln sg) cuts each mode at rg sg^trunc (0 = no cut).
  function drawModes(modes, V, u, trunc) {
    var r = [], m, i;
    for (m = 0; m < modes.length; m++) {
      var md = modes[m], n = Math.round(md.N * V * 1e-6), ls = Math.log(md.sg);   // N per m^3, V in cm^3
      for (i = 0; i < n; i++) { var z; do { z = gaussian(u); } while (trunc && Math.abs(z) > trunc); r.push(md.rg * Math.exp(ls * z)); }
    }
    return r;
  }
  // Upper bound of the efficiency table over all pairs with collector in [R1, R2] and partner in [r1, r2]: the table is
  // piecewise bilinear in (ln R, ln p), so its maximum over the bounding rectangle lies at a corner, an edge crossing of a
  // grid line, or an interior node; all are evaluated.
  function tableMax(tab, R1, R2, r1, r2, near) {
    var p1 = r1 / R2, p2 = Math.min(r2 / R1, 1), xs = [Math.log(R1), Math.log(R2)], ys = [Math.log(Math.max(p1, 1e-9)), Math.log(Math.min(p2, 0.6))], best = 0, i, j;
    if (near === 'one' && p2 > 0.6 && R2 >= 40e-6) return 1;
    if (ys[1] < ys[0]) ys[1] = ys[0];
    var gx = tab.lnR.filter(function (v) { return v > xs[0] && v < xs[1]; }), gy = tab.lnp.filter(function (v) { return v > ys[0] && v < ys[1]; });
    var X = xs.concat(gx), Y = ys.concat(gy);
    for (i = 0; i < X.length; i++) for (j = 0; j < Y.length; j++) best = Math.max(best, tableE(tab, Math.exp(X[i]), Math.exp(Y[j]), near));
    return best;
  }
  function gillespieRun(V, radii, A, kopt, o) {
    o = o || {};
    var u = o.u || rng(o.seed || 1), tEnd = o.tEnd || 3600, rec = o.recordEvery || 60, perDoubling = o.classesPerDoubling || 4;
    var Vm = V * 1e-6;                               // V in cm^3 -> m^3
    var np = radii.length, cap = np + 8, r = new Float64Array(cap), v = new Float64Array(cap), cls = new Int32Array(cap), slot = new Int32Array(cap), big = new Int32Array(cap);
    var rMin = 0.5e-6, B = Math.ceil(Math.log(8e-3 / rMin) / Math.LN2 * perDoubling) + 1;
    var lists = [], counts = new Float64Array(B), a, b, i;
    var lo = [], hi = [], vlo = [], vhi = [];
    for (a = 0; a < B; a++) {
      lists.push([]); lo.push(rMin * Math.pow(2, a / perDoubling)); hi.push(rMin * Math.pow(2, (a + 1) / perDoubling));
      vlo.push(vTerminal(lo[a], A, kopt.speed)); vhi.push(vTerminal(hi[a], A, kopt.speed));
    }
    function clsOf(x) { return Math.max(0, Math.min(B - 1, Math.floor(Math.log(x / rMin) / Math.LN2 * perDoubling))); }
    function add(id) { var c = clsOf(r[id]); cls[id] = c; slot[id] = lists[c].length; lists[c].push(id); counts[c]++; }
    function remove(id) { var c = cls[id], L = lists[c], last = L[L.length - 1]; L[slot[id]] = last; slot[last] = slot[id]; L.pop(); counts[c]--; }
    for (i = 0; i < np; i++) { r[i] = radii[i]; v[i] = vTerminal(r[i], A, kopt.speed); add(i); }
    // class-pair majorants of the kernel
    var Kmax = new Float64Array(B * B);
    for (a = 0; a < B; a++) for (b = a; b < B; b++) {
      var dvmax = Math.max(vhi[b] - vlo[a], vhi[a] - vlo[b], 0), E = 1;
      if (kopt.eff === 'table') E = Math.max(tableMax(kopt.tab, lo[b], hi[b], lo[a], hi[a], kopt.near), tableMax(kopt.tab, lo[a], hi[a], lo[b], hi[b], kopt.near));
      var km = kopt.constant ? kopt.constant : Math.PI * Math.pow(hi[a] + hi[b], 2) * dvmax * E * (1 + 1e-9);
      Kmax[a * B + b] = km; Kmax[b * B + a] = km;
    }
    var rate = new Float64Array(B * B), rowSum = new Float64Array(B), total = 0;
    // same class: ordered proposals (i, j) uniform among n_a^2 (i = j rejected), so a given pair is proposed with probability
  // 2/n_a^2 at the class rate K* n_a^2/(2V): accepted rate K*/V x (K/K*) = K/V, exactly the pair's rate
  function pairRate(a, b) { return a === b ? Kmax[a * B + a] * counts[a] * counts[a] / (2 * Vm) : Kmax[a * B + b] * counts[a] * counts[b] / Vm; }
    function rebuildRow(a) { var s = 0; for (var bb = a; bb < B; bb++) { rate[a * B + bb] = pairRate(a, bb); s += rate[a * B + bb]; } total += s - rowSum[a]; rowSum[a] = s; }
    function touch(c) { for (var aa = 0; aa <= c; aa++) { var old = rate[aa * B + c], nw = pairRate(aa, c); rate[aa * B + c] = nw; rowSum[aa] += nw - old; total += nw - old; } if (c < B - 1) rebuildRow(c); }
    for (a = 0; a < B; a++) rebuildRow(a);
    total = 0; for (a = 0; a < B; a++) total += rowSum[a];
    var t = 0, nextRec = 0, mass0 = 0, events = 0, proposals = 0, violations = 0;
    for (i = 0; i < np; i++) mass0 += massOf(r[i]);
    var out = { t: [], F40: [], rmax: [], n100: [], first100: null, first1mm: null, firstR: o.firstR || [100e-6, 1e-3], firsts: {}, seed: o.seed || 1 };
    var alive = np;
    function record(tt) {
      var m40 = 0, rmx = 0, n100 = 0;
      for (var c = 0; c < B; c++) { var L = lists[c]; for (var q = 0; q < L.length; q++) { var rr = r[L[q]]; if (rr >= 40e-6) m40 += massOf(rr); if (rr > rmx) rmx = rr; if (rr >= 100e-6) n100++; } }
      out.t.push(tt); out.F40.push(m40 / mass0); out.rmax.push(rmx); out.n100.push(n100);
    }
    var rmaxNow = 0; for (i = 0; i < np; i++) rmaxNow = Math.max(rmaxNow, r[i]);
    for (var fq = 0; fq < out.firstR.length; fq++) if (rmaxNow >= out.firstR[fq]) out.firsts[out.firstR[fq]] = 0;
    while (true) {
      if (total <= 0) { while (nextRec <= tEnd) { record(nextRec); nextRec += rec; } break; }
      var dt = -Math.log(u()) / total;
      while (t + dt >= nextRec && nextRec <= tEnd) { record(nextRec); nextRec += rec; }
      t += dt; if (t > tEnd) break;
      proposals++;
      // choose the class pair, then two members, then accept with K / K*
      var target = u() * total, aa = 0;
      while (aa < B - 1 && target > rowSum[aa]) { target -= rowSum[aa]; aa++; }
      var bb = aa; while (bb < B - 1 && target > rate[aa * B + bb]) { target -= rate[aa * B + bb]; bb++; }
      var La = lists[aa], Lb = lists[bb]; if (!La.length || !Lb.length) continue;
      var id1 = La[Math.floor(u() * La.length)], id2 = Lb[Math.floor(u() * Lb.length)];
      if (id1 === id2) continue;                   // same particle: a proposal of the a = b class that is not a pair; rejected
      var K = kernel(r[id1], r[id2], A, kopt), Ks = Kmax[aa * B + bb];
      if (K > Ks) { violations++; if (violations > 10) throw new Error('majorant violated'); }
      if (u() >= K / Ks) continue;
      // merge: id2 absorbs id1
      events++;
      if (o.onEvent) o.onEvent(r[id1], r[id2], t, alive);
      var c1 = cls[id1], c2 = cls[id2];
      remove(id1); remove(id2);
      big[id2] += big[id1] + (Math.min(r[id1], r[id2]) >= 30e-6 ? 1 : 0);   // mergers with a partner of 30 um or more in its history
      r[id2] = Math.cbrt(r[id1] * r[id1] * r[id1] + r[id2] * r[id2] * r[id2]); v[id2] = vTerminal(r[id2], A, kopt.speed);
      add(id2); alive--;
      var c3 = cls[id2];
      touch(c1); if (c2 !== c1) touch(c2); if (c3 !== c1 && c3 !== c2) touch(c3);
      for (var fq2 = 0; fq2 < out.firstR.length; fq2++) { var th = out.firstR[fq2]; if (out.firsts[th] === undefined && r[id2] >= th) { out.firsts[th] = t; out['bigMerges' + th] = big[id2]; } }
    }
    out.events = events; out.proposals = proposals; out.violations = violations; out.alive = alive;
    return out;
  }

  // ---------------------------------------------------------------- L8b: vapour ripening, the gradient descent of surface free energy
  // In a closed saturated volume drops exchange water through the vapour. A drop of radius r holds its water with chemical potential
  // (per kg, relative to flat pure water) mu = R_v T (a/r - b/r^3): a = 2 sigma/(rho_w R_v T) the Kelvin length (curvature), b the solute
  // term (Raoult). Each drop's mass changes as dm/dt = 4 pi rho_w r G f_v (s - a/r + b/r^3), s the supersaturation, which the closed
  // volume sets so that the water in drops is conserved. That is dm_i/dt = -M_i (mu_i - mu_bar), M_i = 4 pi rho_w r_i G f_v / (R_v T):
  // a gradient flow of the free energy F = sum (sigma 4 pi r^2 + solute terms) at fixed water, with dF/dt = -sum M_i (mu_i - mu_bar)^2.
  function ventilation(r, A) {   // Pruppacher and Klett (1997) 13-60, 13-61 with X = Sc^(1/3) Re^(1/2); Sc of vapour in air
    var Dv = 2.11e-5 * Math.pow(A.T / 273.15, 1.94) * (101325 / A.p), Re = 2 * r * A.rho * vBeard(r, A) / A.mu, X = Math.pow(A.nu / Dv, 1 / 3) * Math.sqrt(Re);
    return X < 1.4 ? 1 + 0.108 * X * X : 0.78 + 0.308 * X;
  }
  function kelvinA(A) { return 2 * sigmaWater(A.T) / (RHO_W * 461.5 * A.T); }
  function ripen(radii, A, o) {
    o = o || {};
    var n = radii.length, r = Float64Array.from(radii), b = new Float64Array(n), a = kelvinA(A), G = growthG(A), i, t = 0, out = [];
    var bOf = o.b || function () { return 0; }, fv = o.vent === false ? function () { return 1; } : function (rr) { return ventilation(rr, A); };
    for (i = 0; i < n; i++) b[i] = bOf(i, r[i]);
    var rmin = o.rmin || 0.05e-6, tEnd = o.tEnd || 86400, recAt = (o.recAt || [0, 600, 3600, 6 * 3600, 21600, 86400]).slice(), M0 = 0, steps = 0;
    for (i = 0; i < n; i++) M0 += massOf(r[i]);
    var fvc = new Float64Array(n); for (i = 0; i < n; i++) fvc[i] = fv(r[i]);
    function F() { var f = 0; for (var k = 0; k < n; k++) if (r[k] > 0) f += sigmaWater(A.T) * 4 * Math.PI * r[k] * r[k]; return f; }
    function rec() { var alive = 0, m = 0, r3 = 0; for (var k = 0; k < n; k++) if (r[k] > 0) { alive++; m += massOf(r[k]); r3 += r[k] * r[k] * r[k]; }
      out.push({ t: t, alive: alive, F: F(), M: m / M0, rmean3: Math.cbrt(r3 / Math.max(1, alive)), r: Array.from(r) }); }
    while (recAt.length && recAt[0] <= 0) { rec(); recAt.shift(); }
    var dm = new Float64Array(n);
    while (t < tEnd) {
      // s from conservation: sum 4 pi rho r G f (s - a/r + b/r^3) = 0
      var num = 0, den = 0;
      for (i = 0; i < n; i++) if (r[i] > 0) { var w = r[i] * fvc[i]; num += w * (a / r[i] - b[i] / (r[i] * r[i] * r[i])); den += w; }
      var sv = num / den, dt = Math.min(o.dtMax || 120, recAt.length ? recAt[0] - t : tEnd - t);
      for (i = 0; i < n; i++) if (r[i] > 0) {
        dm[i] = 4 * Math.PI * RHO_W * r[i] * G * fvc[i] * (sv - a / r[i] + b[i] / (r[i] * r[i] * r[i]));
        if (dm[i] < 0) dt = Math.min(dt, 0.2 * massOf(r[i]) / -dm[i]);
      }
      dt = Math.max(dt, 1e-3);
      var lost = 0;
      for (i = 0; i < n; i++) if (r[i] > 0) {
        var mi = massOf(r[i]) + dm[i] * dt;
        if (mi <= massOf(rmin) && b[i] === 0) { lost += mi; r[i] = 0; } else r[i] = radiusOf(Math.max(mi, 1e-30));
      }
      if (lost !== 0) {   // a vanishing drop's last water goes to the vapour and back to the others, in proportion to their uptake
        var up = 0; for (i = 0; i < n; i++) if (r[i] > 0 && dm[i] > 0) up += dm[i];
        if (up > 0) for (i = 0; i < n; i++) if (r[i] > 0 && dm[i] > 0) r[i] = radiusOf(massOf(r[i]) + lost * dm[i] / up);
      }
      if (++steps % 50 === 0) for (i = 0; i < n; i++) if (r[i] > 0) fvc[i] = fv(r[i]);
      t += dt;
      while (recAt.length && t >= recAt[0] - 1e-9) { rec(); recAt.shift(); }
    }
    return { rec: out, steps: steps, a: a, G: G };
  }

  // ---------------------------------------------------------------- L10: a cloud with a shape
  // A vertical slice (x, z) of Lx by Lz metres holding super-droplets (Shima et al. 2009), each standing for xi real drops of one radius at
  // one place. A drop moves with dX/dt = U(X) + u' - v_T(r) e_z.
  // U: a steady overturning motion inside the cloud, from a stream function psi that vanishes on the cloud's outline (the mean wind
  //    never crosses it): grad^2 psi = -omega inside, psi = 0 outside, omega the vorticity of a two-cell overturning (rising in the
  //    middle), solved on a 25 m grid and interpolated bilinearly, so U = (psi_z, -psi_x) is exactly divergence-free; scaled so that the
  //    fastest updraft is W0.
  // u': the stochastic element, the eddies the mean motion does not hold. Per component an Ornstein-Uhlenbeck velocity of variance
  //    sig2 = (eps Le)^(2/3) (Kolmogorov scaling for eddies up to the size Le, a parameter) and memory T_L = 2 sig2/(C0 eps), C0 = 6,
  //    with the drift that keeps evenly spread air evenly spread where eps varies (the well-mixed condition in two dimensions):
  //    a_i = (1/2) d_i sig2 + u'_i ((u' + U) . grad sig2)/(2 sig2).
  // Inside the cloud the air is saturated; outside it a drop evaporates, dr^2/dt = 2 G S f_v(r), f_v the ventilation factor.
  // In each 50 m cell, pairs collide by Shima's random-pair Monte Carlo with the kernel of chapters 1-4. Drops falling through the
  // ground are rain; air reflects at every wall.
  var SHAPE_BOX = { box: [-400, 400, 300, 1100], disc: [-451, 451, 249, 1151], tower: [-225, 225, 300, 1400], cumulus: [-560, 560, 300, 1350] };
  function shapeFn(name, Lx, Lz, opt) {
    var cx = Lx / 2;
    if (name === 'box') return function (x, z) { return Math.abs(x - cx) < 400 && z > 300 && z < 1100; };
    if (name === 'disc') return function (x, z) { return (x - cx) * (x - cx) + (z - 700) * (z - 700) < 451 * 451; };
    if (name === 'tower') return function (x, z) { return Math.abs(x - cx) < 225 && z > 300 && z < 1400; };
    if (name === 'random') return randomOutline(Lx, Lz, opt || {}).inside;
    // cumulus: a flat base at 300 m and a cauliflower top, the union of five discs and a slab
    var bumps = [[cx - 330, 620, 230], [cx - 120, 820, 270], [cx + 140, 900, 300], [cx + 360, 680, 220], [cx + 30, 1120, 230]];
    return function (x, z) {
      if (z < 300) return false;
      if (Math.abs(x - cx) < 520 && z < 640) return true;
      for (var i = 0; i < bumps.length; i++) { var b = bumps[i]; if ((x - b[0]) * (x - b[0]) + (z - b[1]) * (z - b[1]) < b[2] * b[2]) return true; }
      return false;
    };
  }
  // An outline drawn by chance: R(theta) = R0 exp(sum_k c_k cos(k theta + phi_k)), k = 2..12, c_k = rough g_k / k (g_k standard normal),
  // a flat base at zb; R0 chosen so the area is `area`. rough = 0 is a disc cut flat at its base.
  function randomOutline(Lx, Lz, o) {
    var u = rng(o.seed || 1), rough = o.rough || 0, area = o.area || 0.64e6, zb = o.zb || 300, cx = Lx / 2, K = [], k;
    for (k = 2; k <= 12; k++) K.push([k, rough * gaussian(u) / k, 2 * Math.PI * u()]);
    function rad(th) { var s = 0; for (var i = 0; i < K.length; i++) s += K[i][1] * Math.cos(K[i][0] * th + K[i][2]); return Math.exp(s); }
    var R0 = 450, zc;
    function inside0(x, z, R, zcc) { if (z < zb) return false; var dx = x - cx, dz = z - zcc, rr = Math.sqrt(dx * dx + dz * dz); return rr < R * rad(Math.atan2(dz, dx)); }
    function areaOf(R) { var zcc = zb + 0.55 * R, n = 0; for (var x = 2.5; x < Lx; x += 5) for (var z = 2.5; z < Lz; z += 5) if (inside0(x, z, R, zcc)) n++; return n * 25; }
    var lo = 100, hi = 900;
    for (k = 0; k < 30; k++) { var mid = 0.5 * (lo + hi); if (areaOf(mid) < area) lo = mid; else hi = mid; }
    R0 = 0.5 * (lo + hi); zc = zb + 0.55 * R0;
    return { inside: function (x, z) { return inside0(x, z, R0, zc); }, R0: R0, zc: zc, perimeter: null };
  }
  // Perimeter of any outline by Crofton's formula: L = (1/2) int_0^pi int n(p, theta) dp dtheta, n the crossings of the line (p, theta)
  function perimeter(inside, Lx, Lz, d) {
    d = d || 2; var nd = 24, Ltot = 0, D = Math.sqrt(Lx * Lx + Lz * Lz), cx = Lx / 2, cz = Lz / 2, a, p, s;
    for (a = 0; a < nd; a++) {
      var th = Math.PI * (a + 0.5) / nd, c = Math.cos(th), sn = Math.sin(th), cross = 0;
      for (p = -D / 2; p < D / 2; p += d) {
        var prev = null;
        for (s = -D / 2; s < D / 2; s += d / 2) {
          var x = cx + p * c - s * sn, z = cz + p * sn + s * c;
          var v = x >= 0 && x <= Lx && z >= 0 && z <= Lz && inside(x, z);
          if (prev !== null && v !== prev) cross++; prev = v;
        }
      }
      Ltot += cross * d;
    }
    return 0.5 * Ltot * Math.PI / nd;
  }
  function growthG(A) {     // G of dr^2/dt = 2 G S (Rogers and Yau 1989, eq. 7.17 with 7.18): heat conduction and vapour diffusion
    var L = 2.477e6, Rv = 461.5, Kt = 2.48e-2, T = A.T, es = 611.2 * Math.exp(17.67 * (T - 273.15) / (T - 29.65));
    var Dv = 2.11e-5 * Math.pow(T / 273.15, 1.94) * (101325 / A.p);
    var Fk = (L / (Rv * T) - 1) * L * RHO_W / (Kt * T), Fd = RHO_W * Rv * T / (Dv * es);
    return 1 / (Fk + Fd);
  }
  // The mean motion: solve grad^2 psi = -omega on a grid of spacing hg, psi = 0 at nodes outside the cloud (successive over-relaxation)
  function cellFlow(inside, Lx, Lz, W0, hg) {
    hg = hg || 25; var nx = Math.round(Lx / hg) + 1, nz = Math.round(Lz / hg) + 1, inn = new Uint8Array(nx * nz), psi = new Float64Array(nx * nz), i, j;
    var xa = 1e9, xb = -1e9, za = 1e9, zb = -1e9;
    var raw = new Uint8Array(nx * nz);
    for (i = 0; i < nx; i++) for (j = 0; j < nz; j++) if (inside(i * hg, j * hg)) raw[i * nz + j] = 1;
    // psi is free only at nodes whose eight neighbours are all inside: the wind then lives in grid squares that lie wholly in the cloud
    for (i = 1; i < nx - 1; i++) for (j = 1; j < nz - 1; j++) {
      var ok = 1; for (var di = -1; di <= 1; di++) for (var dj = -1; dj <= 1; dj++) if (!raw[(i + di) * nz + j + dj]) ok = 0;
      if (ok) { inn[i * nz + j] = 1; xa = Math.min(xa, i * hg); xb = Math.max(xb, i * hg); za = Math.min(za, j * hg); zb = Math.max(zb, j * hg); }
    }
    var Lc = xb - xa, Hc = zb - za, om = new Float64Array(nx * nz);
    for (i = 0; i < nx; i++) for (j = 0; j < nz; j++) if (inn[i * nz + j]) om[i * nz + j] = Math.sin(2 * Math.PI * (i * hg - xa) / Lc) * Math.sin(Math.PI * (j * hg - za) / Hc);
    for (var it = 0; it < 4000; it++) {
      var res = 0;
      for (i = 1; i < nx - 1; i++) for (j = 1; j < nz - 1; j++) {
        var q = i * nz + j; if (!inn[q]) continue;
        var nw = 0.25 * (psi[q - nz] + psi[q + nz] + psi[q - 1] + psi[q + 1] + hg * hg * om[q]), dlt = nw - psi[q];
        psi[q] += 1.9 * dlt; res = Math.max(res, Math.abs(dlt));
      }
      if (res < 1e-10 * hg * hg && it > 50) break;
    }
    var wmax = 0;
    for (i = 1; i < nx; i++) for (j = 0; j < nz; j++) wmax = Math.max(wmax, -(psi[i * nz + j] - psi[(i - 1) * nz + j]) / hg);
    var sc = W0 > 0 && wmax > 0 ? W0 / wmax : 0;
    for (i = 0; i < psi.length; i++) psi[i] *= sc;
    // bilinear psi; U = (d psi/dz, -d psi/dx) inside each grid square: divergence-free, normal velocity continuous across squares
    function flow(x, z, out) {
      var fx = x / hg, fz = z / hg, i0 = Math.floor(fx), j0 = Math.floor(fz);
      if (i0 < 0 || j0 < 0 || i0 >= nx - 1 || j0 >= nz - 1) { out[0] = 0; out[1] = 0; return; }
      var a = fx - i0, b = fz - j0, p00 = psi[i0 * nz + j0], p10 = psi[(i0 + 1) * nz + j0], p01 = psi[i0 * nz + j0 + 1], p11 = psi[(i0 + 1) * nz + j0 + 1];
      out[0] = ((1 - a) * (p01 - p00) + a * (p11 - p10)) / hg;
      out[1] = -((1 - b) * (p10 - p00) + b * (p11 - p01)) / hg;
    }
    return { flow: flow, psi: psi, nx: nx, nz: nz, hg: hg, inn: inn, Lc: Lc, Hc: Hc, za: za };
  }
  function makeCloud(A, kopt, o) {
    o = o || {};
    var Lx = o.Lx || 2000, Lz = o.Lz || 1500, h = o.h || 50, nx = Math.round(Lx / h), nz = Math.round(Lz / h), u = o.u || rng(o.seed || 1);
    var inside = o.inside || shapeFn(o.shape || 'cumulus', Lx, Lz, o.outline), W0 = o.W0 === undefined ? 1 : o.W0;
    var epsC = o.eps === undefined ? 1e-2 : o.eps, epsB = o.epsOut === undefined ? epsC : o.epsOut, peaked = !!o.peaked, Le = o.Le || 100;
    var cx = Lx / 2, cz = o.cz || 750, Rb = o.Rb || 500;
    var modes = o.modes || [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }], per = o.perCell || [24, 8];
    var C0 = 6, dV = h * h * h, G = growthG(A), S = o.S === undefined ? -0.2 : o.S, stoch = o.stochastic !== false, vent = o.vent !== false;
    function epsAt(x, z) { if (!peaked) return epsC; var q = ((x - cx) * (x - cx) + (z - cz) * (z - cz)) / (Rb * Rb); return epsB + (epsC - epsB) * Math.exp(-q); }
    function sig2At(x, z) { return Math.pow(epsAt(x, z) * Le, 2 / 3); }
    function gradSig2(x, z, out) { var d = 1; out[0] = (sig2At(x + d, z) - sig2At(x - d, z)) / (2 * d); out[1] = (sig2At(x, z + d) - sig2At(x, z - d)) / (2 * d); }
    var CF = o.box ? null : cellFlow(inside, Lx, Lz, W0, 25), flow = CF ? CF.flow : function (x, z, out) { out[0] = 0; out[1] = 0; };
    // regions on the 25 m grid: 0 updraft core (mean wind rising faster than W0/2), 1 flank, 2 edge band (inside, within 100 m of the
    // outline), 3 clear air above the base, 4 below the base
    var hgR = 25, nxR = Math.round(Lx / hgR), nzR = Math.round(Lz / hgR), reg = new Int8Array(nxR * nzR), zbase = 1e9, i, j, k, vv = [0, 0];
    var insideCells = [], outsideCells = [];
    for (i = 0; i < nxR; i++) for (j = 0; j < nzR; j++) { var xq = (i + 0.5) * hgR, zq = (j + 0.5) * hgR; if (inside(xq, zq)) { insideCells.push([xq, zq, i * nzR + j]); zbase = Math.min(zbase, zq - hgR / 2); } else outsideCells.push([xq, zq]); }
    for (i = 0; i < nxR; i++) for (j = 0; j < nzR; j++) { var zq2 = (j + 0.5) * hgR; reg[i * nzR + j] = zq2 < zbase ? 4 : 3; }
    insideCells.forEach(function (c) {
      var dmin = 1e9; for (var q = 0; q < outsideCells.length; q++) { var dx = outsideCells[q][0] - c[0], dz = outsideCells[q][1] - c[1]; if (Math.abs(dx) < 140 && Math.abs(dz) < 140) dmin = Math.min(dmin, Math.sqrt(dx * dx + dz * dz)); }
      flow(c[0], c[1], vv);
      reg[c[2]] = dmin < 100 + hgR / 2 ? 2 : (vv[1] > 0.5 * W0 && W0 > 0 ? 0 : 1);
    });
    function regionAt(x, z) { var a = Math.min(nxR - 1, Math.max(0, Math.floor(x / hgR))), b = Math.min(nzR - 1, Math.max(0, Math.floor(z / hgR))); return reg[a * nzR + b]; }
    var clsOf = function (r) { return r < 20e-6 ? 0 : r < 100e-6 ? 1 : 2; };
    var NR = 5, led = { mergers: new Float64Array(NR * 9), eaten: new Float64Array(NR * 9), released: new Float64Array(NR * 9) };
    var sd = [], ls = modes.map(function (m) { return Math.log(m.sg); }), id = 0;
    var initR = new Float64Array(3), fate = { rainR: new Float64Array(3), evapR: new Float64Array(3), initC: {}, rainC: {}, evapC: {} };
    for (i = 0; i < nx; i++) for (j = 0; j < nz; j++) {
      var xc = (i + 0.5) * h, zc = (j + 0.5) * h;
      if (!o.uniformStart && !inside(xc, zc)) continue;     // uniformStart: fill the whole slice (the well-mixed test)
      for (var mi = 0; mi < modes.length; mi++) for (k = 0; k < per[mi]; k++) {
        var x, z, tries = 0; do { x = (i + u()) * h; z = (j + u()) * h; tries++; } while (!o.uniformStart && !inside(x, z) && tries < 50);
        var zz; do { zz = gaussian(u); } while (Math.abs(zz) > 3);
        var s2 = sig2At(x, z), sg = Math.sqrt(s2), r0 = modes[mi].rg * Math.exp(ls[mi] * zz), xi = modes[mi].N * dV / per[mi];
        var rg0 = Math.min(2, regionAt(x, z)), c100 = Math.floor(x / 100) + ',' + Math.floor(z / 100), tg = {}; tg[c100] = 1;
        var tr = new Float64Array(3); tr[rg0] = 1; initR[rg0] += xi * massOf(r0); fate.initC[c100] = (fate.initC[c100] || 0) + xi * massOf(r0);
        sd.push({ id: id++, x: x, z: z, r: r0, xi: xi, ux: stoch ? sg * gaussian(u) : 0, uz: stoch ? sg * gaussian(u) : 0, coll: mi === 1, t100: -1, tagR: tr, tagC: tg });
      }
    }
    var st = { t: 0, sd: sd, rain: 0, rainN: 0, evap: 0, evapN: 0, evapBelow: 0, M0: 0, N0: 0, first100: null, Lx: Lx, Lz: Lz, h: h, nx: nx, nz: nz, inside: inside, W0: W0, Le: Le,
      epsAt: epsAt, sig2At: sig2At, flow: flow, cell: CF, G: G, S: S, stochastic: stoch, mergers: 0, gamEvents: 0, gamMany: 0, rainLog: [], bornLog: [],
      led: led, regionAt: regionAt, reg: reg, nxR: nxR, nzR: nzR, zbase: zbase, initR: initR, fate: fate, paths: {} };
    sd.forEach(function (q) { st.M0 += q.xi * massOf(q.r); st.N0 += q.xi; });   // N0: drops at the start, for the number book
    if (o.track) o.track.forEach(function (tid) { st.paths[tid] = []; });
    var vf = [0, 0], gr = [0, 0];
    function addTag(map, tagC, m) { for (var key in tagC) map[key] = (map[key] || 0) + m * tagC[key]; }
    function move(q, dt) {
      if (stoch) {
        var e = epsAt(q.x, q.z), s2 = sig2At(q.x, q.z), TL = 2 * s2 / (C0 * e), a = Math.exp(-dt / TL), b = Math.sqrt(s2 * (1 - a * a));
        var ax = 0, az = 0;
        if (peaked && !o.noDrift) { gradSig2(q.x, q.z, gr); flow(q.x, q.z, vf); var proj = ((q.ux + vf[0]) * gr[0] + (q.uz + vf[1]) * gr[1]) / (2 * s2); ax = 0.5 * gr[0] + q.ux * proj; az = 0.5 * gr[1] + q.uz * proj; }
        q.ux = q.ux * a + b * gaussian(u) + ax * dt; q.uz = q.uz * a + b * gaussian(u) + az * dt;
      }
      flow(q.x, q.z, vf);
      q.x += (vf[0] + q.ux) * dt; q.z += (vf[1] + q.uz) * dt;
      if (q.x < 0) { q.x = -q.x; q.ux = -q.ux; } if (q.x > Lx) { q.x = 2 * Lx - q.x; q.ux = -q.ux; }
      if (q.z > Lz) { q.z = 2 * Lz - q.z; q.uz = -q.uz; } if (q.z < 0) { q.z = -q.z; q.uz = -q.uz; }
      q.z -= vTerminal(q.r, A, kopt.speed) * dt;
    }
    st.move = move;
    st.step = function (dt) {
      var q, n = st.sd.length, keep = [], c;
      for (c = 0; c < n; c++) {
        q = st.sd[c];
        if (o.box) { keep.push(q); continue; }      // the well-mixed box: no motion (the test against the collection equation)
        move(q, dt);
        if (st.paths[q.id]) st.paths[q.id].push([Math.round(q.x), Math.round(q.z), +(q.r * 1e6).toFixed(1)]);
        if (q.z < 0) { var m = q.xi * massOf(q.r); st.rain += m; st.rainN += q.xi; st.rainLog.push([st.t, q.x, q.r, q.xi, q.coll ? 1 : 0]);
          for (k = 0; k < 3; k++) fate.rainR[k] += m * q.tagR[k]; addTag(fate.rainC, q.tagC, m); continue; }
        if (S !== 0 && !inside(q.x, q.z)) {
          var r2 = q.r * q.r + 2 * G * S * (vent ? ventilation(q.r, A) : 1) * dt, dm, gone = r2 < 1e-12;
          dm = q.xi * (massOf(q.r) - (gone ? 0 : massOf(Math.sqrt(r2))));
          st.evap += dm; if (q.z < st.zbase) st.evapBelow += dm;
          for (k = 0; k < 3; k++) fate.evapR[k] += dm * q.tagR[k]; addTag(fate.evapC, q.tagC, dm);
          if (gone) { st.evapN += q.xi; continue; }   // evapN: drops that evaporated completely
          q.r = Math.sqrt(r2);
        }
        keep.push(q);
      }
      st.sd = keep; n = keep.length;
      var cells = {};
      for (c = 0; c < n; c++) { q = st.sd[c]; var key = Math.min(nx - 1, Math.floor(q.x / h)) * nz + Math.min(nz - 1, Math.floor(q.z / h)); (cells[key] || (cells[key] = [])).push(q); }
      var dead = false;
      for (var ky in cells) {
        var L = cells[ky], ns = L.length; if (ns < 2) continue;
        for (c = ns - 1; c > 0; c--) { var jj = Math.floor(u() * (c + 1)), tmp = L[c]; L[c] = L[jj]; L[jj] = tmp; }
        var half = Math.floor(ns / 2), scale = ns * (ns - 1) / 2 / half, cxk = (Math.floor(ky / nz) + 0.5) * h, czk = (ky % nz + 0.5) * h, rgn = regionAt(cxk, czk);
        var kl = kopt.eps === 'local' ? Object.assign({}, kopt, { eps: epsAt(cxk, czk) }) : kopt;
        for (c = 0; c < half; c++) {
          var p1 = L[2 * c], p2 = L[2 * c + 1];
          if (p1.xi < p2.xi) { var t2 = p1; p1 = p2; p2 = t2; }       // p1 has the larger multiplicity
          if (p2.xi <= 0 || p1.xi <= 0) continue;
          var pr = scale * p1.xi * kernel(p1.r, p2.r, A, kl) * dt / dV;
          var gam = Math.floor(pr) + (u() < pr - Math.floor(pr) ? 1 : 0); if (gam === 0) continue;
          gam = Math.min(gam, Math.floor(p1.xi / p2.xi)); if (gam === 0) continue;
          var rNew = Math.cbrt(gam * p1.r * p1.r * p1.r + p2.r * p2.r * p2.r), real = gam * p2.xi;   // real mergers: each p2 drop swallows gam p1 drops
          st.mergers += real; st.gamEvents++; if (gam > 1) st.gamMany++;
          var big = Math.max(p1.r, p2.r), sml = Math.min(p1.r, p2.r), ch = rgn * 9 + clsOf(big) * 3 + clsOf(sml);
          led.mergers[ch] += real; led.eaten[ch] += real * massOf(sml);
          led.released[ch] += p2.xi * sigmaWater(A.T) * 4 * Math.PI * (gam * p1.r * p1.r + p2.r * p2.r - rNew * rNew);
          var m1 = gam * massOf(p1.r), m2 = massOf(p2.r), w1 = m1 / (m1 + m2), w2 = 1 - w1, tR = new Float64Array(3), tC = {}, kk;
          for (kk = 0; kk < 3; kk++) tR[kk] = w1 * p1.tagR[kk] + w2 * p2.tagR[kk];
          for (kk in p1.tagC) tC[kk] = (tC[kk] || 0) + w1 * p1.tagC[kk];
          for (kk in p2.tagC) tC[kk] = (tC[kk] || 0) + w2 * p2.tagC[kk];
          var coll = p1.coll || p2.coll;
          if (p1.xi - gam * p2.xi > 0) { p1.xi -= gam * p2.xi; p2.r = rNew; p2.tagR = tR; p2.tagC = tC; p2.coll = coll; }
          else { var h2 = Math.floor(p2.xi / 2); p1.xi = h2; p2.xi -= h2; p1.r = rNew; p2.r = rNew; p1.tagR = tR; p2.tagR = Float64Array.from(tR); p1.tagC = tC; p2.tagC = Object.assign({}, tC); p1.coll = coll; p2.coll = coll; if (p1.xi <= 0) dead = true; }
          [p1, p2].forEach(function (qq) { if (qq.r >= 100e-6 && qq.t100 < 0 && qq.xi > 0) { qq.t100 = st.t + dt; st.bornLog.push([Math.round(qq.x), Math.round(qq.z), st.t + dt, qq.xi]); if (!st.first100) st.first100 = { t: st.t + dt, x: qq.x, z: qq.z }; } });
        }
      }
      if (dead) st.sd = st.sd.filter(function (qq) { return qq.xi > 0; });
      st.t += dt;
    };
    st.census = function () {
      var M = 0, M40 = 0, M100 = 0, Min = 0;
      st.sd.forEach(function (q) { var m = q.xi * massOf(q.r); M += m; if (q.r >= 40e-6) M40 += m; if (q.r >= 100e-6) M100 += m; if (inside(q.x, q.z)) Min += m; });
      return { t: st.t, M: M, M40: M40, M100: M100, Min: Min, rain: st.rain, evap: st.evap, evapBelow: st.evapBelow, n: st.sd.length };
    };
    st.regionCensus = function () {   // water in each class (droplets, collectors, drizzle) in each region, and each region's spectrum
      var W = new Float64Array(NR * 3), spec = [];
      for (var g = 0; g < NR; g++) spec.push({});
      st.sd.forEach(function (q) { var rg = regionAt(q.x, q.z), m = q.xi * massOf(q.r); W[rg * 3 + clsOf(q.r)] += m; var b = Math.round(Math.log2(massOf(q.r) / massOf(1e-6)) * 8); spec[rg][b] = (spec[rg][b] || 0) + q.xi; });
      return { W: W, spec: spec };
    };
    return st;
  }

  return {
    shapeFn: shapeFn, randomOutline: randomOutline, perimeter: perimeter, cellFlow: cellFlow, growthG: growthG, makeCloud: makeCloud, ventilation: ventilation, kelvinA: kelvinA, ripen: ripen,
    G0: G0, RHO_W: RHO_W, RHO_I: RHO_I, R_D: R_D, K_B: K_B,
    air: air, sigmaWater: sigmaWater, massOf: massOf, radiusOf: radiusOf,
    stokesK: stokesK, vStokes: vStokes, tauP: tauP, reynolds: reynolds,
    L0F: L0F, L0time: L0time, L0blowup: L0blowup, L0radius: L0radius, L0box: L0box,
    meanFreePath: meanFreePath, vBeard: vBeard, vTerminal: vTerminal,
    flowA: flowA, psi: psi, trajHits: trajHits, trajPath: trajPath, flowEfficiency: flowEfficiency, axisHits: axisHits, criticalStokes: criticalStokes,
    pairEfficiency: pairEfficiency, makeTable: makeTable, tableE: tableE, hallE: hallE,
    weber: weber, eCoal: eCoal, kernel: kernel,
    makeGrid: makeGrid, lognormalBins: lognormalBins, kernelMatrix: kernelMatrix, sceStep: sceStep, moments: moments,
    sceRun: sceRun, gceRun: gceRun, besselI1e: besselI1e, golovinDensity: golovinDensity,
    SURF: SURF, makeLedger: makeLedger, ledgerAdd: ledgerAdd, surfaceSum: surfaceSum, digamma: digamma, lnGamma: lnGamma, maxentCompare: maxentCompare,
    ayalaFactor: ayalaFactor, rng: rng, gaussian: gaussian, drawModes: drawModes, tableMax: tableMax, gillespieRun: gillespieRun
  };
})();
/*PHYSICS-END*/
if (typeof module !== 'undefined') module.exports = PHYS;
