// The closed-form numbers of the Fig. 12 lecture note, from the page's own constants: node tools/fig12/theory.cjs
// Sloshing (linear potential theory, the equivalent spring-mass), dimensionless groups, the quarter car, the drive and its
// PI loop, the skyhook. Nothing here is used by the page; these are the yardsticks the note derives and the solver is checked
// against. Every constant is read from the page's code (stout-cart.js defaults and the World options in beer-slosh.html).
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const G = load('guinness-glass.js'), { Cart, Road } = load('stout-cart.js');
const out = (k, v, u, note) => console.log(`${k.padEnd(34)} ${typeof v === 'number' ? (Math.abs(v) >= 1e4 || (Math.abs(v) < 1e-3 && v !== 0) ? v.toExponential(4) : v.toPrecision(6)) : v} ${u || ''}${note ? '   ' + note : ''}`);

// Bessel J0, J1 by their power series (enough terms for x < 10)
const J = (n, x) => { let s = 0, t = Math.pow(x / 2, n); for (let k = 1; k <= n; k++) t /= k; for (let k = 0; k < 40; k++) { s += t; t *= -(x * x / 4) / ((k + 1) * (k + 1 + n)); } return s; };
const dJ1 = (x) => J(0, x) - J(1, x) / x;
// first zero of J1'(x) by bisection on [1.5, 2.2]
let a = 1.5, b = 2.2; for (let k = 0; k < 80; k++) { const m = 0.5 * (a + b); if (dJ1(a) * dJ1(m) <= 0) b = m; else a = m; }
const xi = 0.5 * (a + b);
console.log('--- linear sloshing, upright circular cylinder');
out('xi_11 (first zero of J1\')', xi, '', `J1(xi) = ${J(1, xi).toFixed(6)}, J2(xi) = ${(2 / xi * J(1, xi) - J(0, xi)).toFixed(6)} = J1/xi ${(J(1, xi) / xi).toFixed(6)}`);
const g = 9.81, rho = 1000, nu = 1e-6, sigma = 0.072;
const f11 = (R, h) => Math.sqrt(g * xi / R * Math.tanh(xi * h / R)) / (2 * Math.PI);
out('f11 cylinder R 40 mm, h 100 mm', f11(0.04, 0.10), 'Hz', 'the solver check (cylfreq)');
out('  tanh(xi h/R)', Math.tanh(xi * 0.10 / 0.04), '', 'deep: tanh -> 1');
out('f11 same R, deep (h -> inf)', Math.sqrt(g * xi / 0.04) / (2 * Math.PI), 'Hz');

// the tulip: inner radius R(z) from the measured profile
const Rz = (z) => { const P = G.R, f = Math.max(0, z) / G.dz, i = Math.floor(f); if (i >= P.length - 1) return P[P.length - 1]; return P[i] + (f - i) * (P[i + 1] - P[i]); };
const vol = (h) => { const n = Math.round(h / 5e-5), d = h / n; let v = 0; for (let k = 0; k <= n; k++) { const r = Rz(k * d); v += (k === 0 || k === n ? 0.5 : 1) * Math.PI * r * r * d; } return v; };
const h0 = 0.125, Rs = Rz(h0), V = vol(h0), ml = rho * V;
console.log('--- the tulip at the fill height');
out('R(h0), surface radius', Rs * 1000, 'mm');
out('dR/dz at h0', (Rz(h0 + 0.0005) - Rz(h0 - 0.0005)) / 0.001, '');
out('V(h0), m_l', V * 1e6, 'ml', `${(ml * 1000).toFixed(1)} g`);
out('f11 of a cylinder of radius R(h0)', f11(Rs, h0), 'Hz', 'yardstick only: the tulip is not a cylinder');
// quasi-static tilt: centre of mass shift for a plane surface of slope -a/g, first order: x_c = -(a/g) I / V, I = pi R^4/4
const A = 2.0;
out('tilt a = 2 m/s^2: slope a/g', A / g, '', `angle ${(Math.atan(A / g) * 180 / Math.PI).toFixed(2)} deg`);
out('  wall rise R(h0) a/g', Rs * A / g * 1000, 'mm');
out('  x_c tulip, -(a/g) pi R^4/(4V)', -(A / g) * Math.PI * Rs ** 4 / 4 / V * 1000, 'mm');
out('  x_c cylinder R 40, h 100', -(A / g) * Math.PI * 0.04 ** 4 / 4 / (Math.PI * 0.04 ** 2 * 0.10) * 1000, 'mm', '= -(a/g) R^2/(4h)');

// equivalent spring-mass (first mode): m1/m = 2R tanh(xi h/R) / (xi (xi^2 - 1) h)
console.log('--- equivalent spring-mass of the first mode');
const m1cyl = 2 * 0.04 * Math.tanh(xi * 0.10 / 0.04) / (xi * (xi * xi - 1) * 0.10);
out('m1/m cylinder R 40 h 100', m1cyl, '', `m = ${(rho * Math.PI * 0.0016 * 0.1 * 1000).toFixed(1)} g, m1 = ${(m1cyl * rho * Math.PI * 0.0016 * 0.1 * 1000).toFixed(1)} g`);
const m1deep = 2 * Math.PI * rho * Rs ** 3 / (xi * (xi * xi - 1));
out('m1 deep limit 2 pi rho R^3/(xi(xi^2-1)), R(h0)', m1deep * 1000, 'g', `${(100 * m1deep / ml).toFixed(1)} % of the pint (inference: the tulip is deep, h0/R = ${(h0 / Rs).toFixed(2)})`);
out('mode-1 share of the wall rise 2/(xi^2-1)', 2 / (xi * xi - 1), '');
out('P = (rho pi R^3/xi^2) d(eta_w)/dt: coefficient', rho * Math.PI * Rs ** 3 / xi ** 2 * 1000, 'g', 'relative momentum per wall speed, tulip surface radius');

console.log('--- dimensionless groups (tulip surface radius unless said)');
const k1 = xi / Rs, w1 = 2 * Math.PI * 3.263;
out('Bond rho g / (sigma k^2), R 40 mm', rho * g / (sigma * (xi / 0.04) ** 2), '', `correction sqrt(1 + 1/Bo) - 1 = ${(100 * (Math.sqrt(1 + sigma * (xi / 0.04) ** 2 / (rho * g)) - 1)).toFixed(2)} %`);
out('Bond, R(h0)', rho * g / (sigma * k1 ** 2), '', `correction ${(100 * (Math.sqrt(1 + sigma * k1 * k1 / (rho * g)) - 1)).toFixed(2)} %`);
out('capillary length sqrt(sigma/(rho g))', Math.sqrt(sigma / (rho * g)) * 1000, 'mm');
out('omega (tulip, 3.263 Hz measured at 3 mm)', w1, 'rad/s');
out('Stokes layer delta = sqrt(2 nu/omega)', Math.sqrt(2 * nu / w1) * 1000, 'mm');
out('sqrt(nu/(omega R^2))', Math.sqrt(nu / (w1 * Rs * Rs)), '');
out('oscillatory Reynolds omega R^2/nu', w1 * Rs * Rs / nu, '');
out('Galilei-type sqrt(g R^3)/nu', Math.sqrt(g * Rs ** 3) / nu, '');
out('sqrt(nu/(g^(1/2) R^(3/2)))', Math.sqrt(nu / (Math.sqrt(g) * Math.pow(Rs, 1.5))), '');

console.log('--- the cart (page options: Rw 0.04 m, Ls 0.135 m; Cart defaults otherwise)');
const road = new Road({ bumps: [{ x: 1, h: 0.01, L: 0.25 }], Rw: 0.04, xmin: -1, xmax: 3 });
const c = new Cart({ x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ml, road });
const Ms = c.Mb + c.ml, Mx = c.massX(), bF = c.bForce();
out('M_s = M_b + m_l', Ms, 'kg'); out('I_w / R_w^2 (disc)', c.Iw / c.Rw ** 2, 'kg'); out('N_g^2 J_m / R_w^2', c.Ngear ** 2 * c.Jm / c.Rw ** 2, 'kg');
out('M_x', Mx, 'kg');
out('body alone sqrt(k/M_s)/2pi', Math.sqrt(c.k / Ms) / (2 * Math.PI), 'Hz', `zeta = c/(2 sqrt(k Ms)) = ${(c.c / (2 * Math.sqrt(c.k * Ms))).toFixed(4)}`);
out('wheel alone sqrt((k+kt)/m_w)/2pi', Math.sqrt((c.k + c.kt) / c.mw) / (2 * Math.PI), 'Hz');
{ // undamped two-mass eigenfrequencies: Ms zb'' = -k(zb - zw), mw zw'' = k(zb - zw) - kt zw
  const A11 = c.k / Ms, A12 = -c.k / Ms, A21 = -c.k / c.mw, A22 = (c.k + c.kt) / c.mw, tr = A11 + A22, det = A11 * A22 - A12 * A21;
  const l1 = 0.5 * (tr - Math.sqrt(tr * tr - 4 * det)), l2 = 0.5 * (tr + Math.sqrt(tr * tr - 4 * det));
  out('quarter car, undamped: body mode', Math.sqrt(l1) / (2 * Math.PI), 'Hz'); out('quarter car, undamped: wheel mode', Math.sqrt(l2) / (2 * Math.PI), 'Hz');
}
out('static spring sag M_s g / k', Ms * g / c.k * 1000, 'mm'); out('static tyre sag (M_s + m_w) g / k_t', (Ms + c.mw) * g / c.kt * 1000, 'mm');
// the envelope over a 10 mm bump: largest slope and the time to cross
let smax = 0, xs = 0; for (let x = 0.7; x < 1.3; x += 1e-4) { const s = road.axle(x)[1]; if (Math.abs(s) > Math.abs(smax)) { smax = s; xs = x; } }
out('10 mm bump: max |z_a\'|', Math.abs(smax), '', `at x = ${xs.toFixed(4)} m; the road itself: pi h/L = ${(Math.PI * 0.01 / 0.25).toFixed(4)}`);
out('  -N z_a\' with N = (M_s+m_w) g', (Ms + c.mw) * g * Math.abs(smax), 'N', `/ M_x = ${((Ms + c.mw) * g * Math.abs(smax) / Mx).toFixed(3)} m/s^2 (static load only, an estimate)`);
let x0 = null, x1 = null; for (let x = 0.5; x < 1.5; x += 1e-4) { const s = road.axle(x)[0] - road.axle(0)[0]; if (s > 1e-7 && x0 === null) x0 = x; if (s > 1e-7) x1 = x; }
out('  axle path length of the bump', (x1 - x0), 'm', `crossing time at 1 m/s ${(x1 - x0).toFixed(3)} s; slosh period 1/3.263 Hz = ${(1 / 3.263).toFixed(3)} s`);

console.log('--- drive and speed loop');
out('b = N_g K_m / R_w', bF, 'N/A'); out('i_0 = c_x v_0 / b at 1 m/s', c.cx * 1 / bF, 'A');
out('back-EMF at 1 m/s, K_m N_g v / R_w', c.Km * c.Ngear * 1 / c.Rw, 'V'); out('no-load speed V_max R_w/(K_m N_g)', c.Vmax * c.Rw / (c.Km * c.Ngear), 'm/s');
out('current the voltage allows at 1 m/s', (c.Vmax - c.Km * c.Ngear / c.Rw) / c.Ra, 'A', `(I_max = ${c.Imax} A binds first; F_max = ${(bF * c.Imax).toFixed(1)} N, ${(bF * c.Imax / Mx).toFixed(2)} m/s^2)`);
out('mechanical time constant M_x/c_x', Mx / c.cx, 's');
out('motor: R_a/(K_m N_g/R_w)^2 = damping it adds when shorted', (c.Km * c.Ngear / c.Rw) ** 2 / c.Ra, 'N s/m', '(voltage drive; this page drives current)');
out('omega_c', c.wc, 'rad/s'); out('K_p = M_x omega_c / b', c.Kp, 'A/(m/s)'); out('K_i = K_p omega_c / 4', c.Ki, 'A/m');
{ // closed loop, lags ignored: M_x s^2 + (c_x + b K_p) s + b K_i = 0
  const a2 = Mx, a1 = c.cx + bF * c.Kp, a0 = bF * c.Ki, D = a1 * a1 - 4 * a2 * a0;
  const r1 = (-a1 + Math.sqrt(Math.max(0, D))) / (2 * a2), r2 = (-a1 - Math.sqrt(Math.max(0, D))) / (2 * a2);
  out('closed-loop poles (no lags)', `${r1.toFixed(3)}, ${r2.toFixed(3)}`, '1/s', `(-omega_c/2 = ${(-c.wc / 2).toFixed(3)} double, if c_x = 0); zeta = ${(a1 / (2 * Math.sqrt(a0 * a2))).toFixed(4)}`);
  // loop gain L(jw) = b (K_p jw + K_i) / (jw (M_x jw + c_x)) * lags; crossover and phase margin
  const L = (w, lag) => { const re = -Mx * w * w, im = c.cx * w;   // jw(Mx jw + cx) = -Mx w^2 + j cx w
    const nr = bF * c.Ki, ni = bF * c.Kp * w, d2 = re * re + im * im;
    let Lr = (nr * re + ni * im) / d2, Li = (ni * re - nr * im) / d2;
    if (lag) { const ph = -Math.atan(w * c.tauI) - w * c.Ts / 2 - Math.atan(w * 1e-4 / 2), mag = 1 / Math.sqrt(1 + (w * c.tauI) ** 2); const cr = Math.cos(ph) * mag, ci = Math.sin(ph) * mag; [Lr, Li] = [Lr * cr - Li * ci, Lr * ci + Li * cr]; }
    return [Lr, Li]; };
  for (const lag of [false, true]) {
    let lo = 1, hi = 1000; for (let k = 0; k < 100; k++) { const m = Math.sqrt(lo * hi), [r, i] = L(m, lag); if (Math.hypot(r, i) > 1) lo = m; else hi = m; }
    const [r, i] = L(lo, lag);
    out(lag ? 'crossover, with lags tau_i, T_s/2' : 'crossover (no lags)', lo / (2 * Math.PI), 'Hz', `phase margin ${(180 + Math.atan2(i, r) * 180 / Math.PI).toFixed(1)} deg`);
  }
  // sensitivity at the slosh frequency: the share of a disturbance force's acceleration the loop lets through
  for (const f of [3.263, 3.214]) { const w = 2 * Math.PI * f, [r, i] = L(w, true); const s = 1 / Math.hypot(1 + r, i);
    out(`|S(j omega)| at ${f} Hz`, s, '', 'a_closed / a_open for the same disturbance force, with lags'); }
}

console.log('--- skyhook');
out('c_sky = 2 * 0.7 sqrt(k M_s)', c.csky, 'N s/m');
out('zeta passive c/(2 sqrt(k M_s))', c.c / (2 * Math.sqrt(c.k * Ms)), ''); out('zeta with skyhook (c + c_sky)/(2 sqrt(k M_s))', (c.c + c.csky) / (2 * Math.sqrt(c.k * Ms)), '');
{ const wn = Math.sqrt(c.k / Ms), T = (w, cb, cs) => Math.hypot(c.k, w * cb) / Math.hypot(c.k - Ms * w * w, w * (cb + cs));
  let mp = 0, ms = 0; for (let w = 0.1; w < 200; w += 0.01) { mp = Math.max(mp, T(w, c.c, 0)); ms = Math.max(ms, T(w, c.c, c.csky)); }
  out('peak |z_b/z_w| passive (rigid tyre)', mp, ''); out('peak |z_b/z_w| skyhook (ideal)', ms, '');
  const w = 2 * Math.PI * 10; out('at 10 Hz: passive / skyhook / passive c+c_sky', `${T(w, c.c, 0).toFixed(4)} / ${T(w, c.c, c.csky).toFixed(4)} / ${T(w, c.c + c.csky, 0).toFixed(4)}`, '', 'skyhook does not stiffen the high-frequency path');
}

console.log('--- numerics');
out('nu dt / dx^2 at dt 5 ms, dx 4 mm', nu * 0.005 / 0.004 ** 2, '', 'explicit diffusion is stable below 1/6');
out('CFL speed 0.8 dx / dt, dx 4 mm', 0.8 * 0.004 / 0.005, 'm/s', 'a faster particle shortens the step');
out('sqrt(dx/g), dx 4 mm', Math.sqrt(0.004 / g) * 1000, 'ms');
out('steps per slosh period', 1 / 3.263 / 0.005, '');

console.log('--- viscous damping of the first mode, deep cylinder (Abramson SP-106 eq. 4.10b; Stephens et al. NASA TN D-1367 eq. 3)');
for (const [lab, R] of [['R 40 mm', 0.04], ['R(h0) tulip', Rs]]) {
  const B = Math.sqrt(nu / (Math.sqrt(g) * Math.pow(R, 1.5)));
  out(`nu^1/2 R^-3/4 g^-1/4, ${lab}`, B, '', `zeta = K B / 2pi: Miles K = 3.52 -> ${(3.52 * B / (2 * Math.PI)).toFixed(4)}; experiment K = 5.23 -> ${(5.23 * B / (2 * Math.PI)).toFixed(4)}`);
}
