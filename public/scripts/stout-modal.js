/* Fig. 12: the stout as the computed sloshing modes of the real tulip glass, for the page's live model.
 *
 * Every number here comes from public/data/fig12/modes.json, written on GitHub's runners by tools/fig12/modes_fem.py (finite
 * elements on the measured glass, for fill heights 30-145 mm every 2.5 mm). Nothing in this file is a cylinder formula.
 *
 * Linear theory (Faltinsen & Timokha, "Sloshing", 2009, ch. 5; derived in the lecture note): in the glass's frame the stout
 * feels gravity g + a_z downwards and a uniform push -a_x along the road. Without vorticity its surface is a sum of the glass's
 * own shapes, eta = h + sum_n q_n(t) e_n(r) cos(theta), e_n = 1 at the wall, and each wall height q_n obeys
 *     q_n'' + 2 zeta_n w_n q_n' + w_n^2 (1 + a_z/g) q_n = -(w_n^2/g) c_n a_x.
 * w_n, c_n and e_n are the finite-element results; a steady push tilts the surface into the plane eta = h - (a_x/g) x
 * (sum_n c_n e_n = r). Heave (a_z) changes gravity, so it scales every stiffness: on a still surface it does nothing, on a
 * swinging one it pumps (Mathieu). The stout's momentum relative to the glass is rho sum_n Ix_n q_n' (only the surface moves
 * the centre of mass), so its push on the cart is minus the rate of change of that (World in stout-cart.js).
 * Friction, each term from its source and computed over the finite-element mode (all off with o.friction = false):
 *   wall and floor  zeta_wall = (1/2) sqrt(nu/(2 w)) Lam    laminar Stokes layer (Landau & Lifshitz, Fluid Mechanics, sec. 24)
 *   surface skin    zeta_skin = skin (1/2) sqrt(nu/(2 w)) LamS   an inextensible (protein-covered) surface (Lamb 1932, Art. 351);
 *                   skin = the covered fraction, 0 (clean) to 1
 *   bulk            zeta_bulk = nu Bk / w    viscous strain of the potential flow (Lamb's dissipation integral)
 *   contact line    zetaCL (an added ratio, from measurements)
 *   foam head       a friction force at the wall, Viola, Brun, Dollet & Gallaire (Phys. Fluids 28, 091701, 2016) eq. 7.3:
 *                   q'' = ... - alpha w^(4/3) R^(1/3) V |V|^(n-1),  V = the wall's vertical speed = sum_n q_n'
 *                   (every mode has e_n(R) = 1, so each feels the same generalised force, divided by its own modal mass);
 *                   alpha from o.foam (see foamAlpha). nu: the stout's, 2.05e-6 m^2/s at 6 C (Benilov et al., Am. J. Phys.
 *                   81, 88, 2013, eq. 1: 2.06 mPa s, 1007 kg/m^3, measured).
 *
 * The class has the interface of ModalFluid in stout-cart.js, so World (cart, motor, controller, probes, observer) drives it
 * unchanged: new StoutCart.World({ fluidInstance: new StoutModal.TulipModes({ data, profile, h0 }), ... }).
 * SI units. Runs in the browser (window.StoutModal) and in Node (require).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.StoutModal = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // linear interpolation of the data at fill height h: index i and weight t between levels i and i + 1 (clamped at the ends)
  function bracket(hs, h) {
    if (h <= hs[0]) return [0, 0];
    const n = hs.length - 1;
    if (h >= hs[n]) return [n - 1, 1];
    let i = Math.min(n - 1, Math.floor((h - hs[0]) / (hs[1] - hs[0])));
    while (i > 0 && hs[i] > h) i--;
    while (i < n - 1 && hs[i + 1] < h) i++;
    return [i, (h - hs[i]) / (hs[i + 1] - hs[i])];
  }
  const lerp = (a, b, t) => a + (b - a) * t;

  function TulipModes(o) {
    o = o || {};
    if (!o.data) throw new Error('TulipModes needs the computed modes (public/data/fig12/modes.json) as o.data');
    this.data = o.data; this.modal = true;
    this.hsData = o.data.h.map((x) => x / 1000);
    this.profile = o.profile;
    const P = this.profile.R; this.zRim = (P.length - 1) * this.profile.dz; this.R = Math.max.apply(null, P); this.Rrim = P[P.length - 1];
    this.h0 = o.h0 || 0.125; this.rho = o.rho || 1000; this.g = o.g || o.data.g || 9.81;
    this.friction = o.friction !== false;
    this.nu = o.nu != null ? o.nu : 2.05e-6;                      // the stout's kinematic viscosity, m^2/s (Benilov et al. 2013)
    this.skin = o.skin != null ? o.skin : 0;                       // covered fraction of the surface (0 clean, 1 inextensible)
    this.zetaCL = o.zetaCL || 0;
    this.zetaExtra = o.zetaExtra || 0;                             // for checks only
    this.foam = Object.assign({ h: 0, n: 2 / 3, alpha: null }, o.foam || {});
    this.N = Math.min(o.nModes || 4, o.data.levels[0].m1.f.length);
    this.NR = o.data.NR;
    this.Cd = o.Cd != null ? o.Cd : 0.62;                          // weir discharge coefficient (Francis; see ModalFluid)
    this.dx = o.dx || 0.004; this.H = this.zRim + 0.03;
    this.h = this.h0; this.V = this.volumeTo(this.h0); this.V0 = this.V; this.mLiquid = this.rho * this.V;
    this.q = new Float64Array(this.N); this.qd = new Float64Array(this.N);
    this.e = []; for (let n = 0; n < this.N; n++) this.e.push(new Float64Array(this.NR));
    this.t = 0; this.np = 0; this.npStart = 0; this.mp = 0; this.spilled = 0; this.spillNow = 0; this.spillPx = 0; this.spillPz = 0;
    this.spillList = []; this.spillV = 0; this.spillRate = 0; this.cgIters = 0;
    // the column grid of the 3D solver (half glass), filled from the modes, so the page's store and drawing read alike
    const dx = this.dx; this.nx = 2 * Math.ceil(this.R / dx); this.ny = Math.ceil(this.R / dx); this.x0 = -(this.nx / 2) * dx;
    this.colH = new Float64Array(this.nx * this.ny);
    const F = Float64Array; this.px = new F(0); this.py = new F(0); this.pz = new F(0);
    this.modes();
  }
  // the glass, as the 3D solver has it (the same measured profile, linear between its 0.5 mm points)
  TulipModes.prototype.Rz = function (z) {
    if (z > this.zRim) return 10;
    const P = this.profile.R, f = (z < 0 ? 0 : z) / this.profile.dz, i = Math.floor(f);
    if (i >= P.length - 1) return P[P.length - 1];
    return P[i] + (f - i) * (P[i + 1] - P[i]);
  };
  TulipModes.prototype.volumeTo = function (h) {
    const n = Math.max(1, Math.round(h / 5e-5)), d = h / n; let v = 0;
    for (let k = 0; k <= n; k++) { const r = this.Rz(k * d); v += (k === 0 || k === n ? 0.5 : 1) * Math.PI * r * r * d; }
    return v;
  };
  TulipModes.prototype.heightOf = function (V) { let a = 0, b = this.zRim; for (let k = 0; k < 50; k++) { const m = 0.5 * (a + b); if (this.volumeTo(m) < V) a = m; else b = m; } return 0.5 * (a + b); };

  // the modes' constants at the present fill height, interpolated between the computed levels
  TulipModes.prototype.modes = function () {
    const [i, t] = bracket(this.hsData, this.h), A = this.data.levels[i].m1, B = this.data.levels[i + 1 > this.data.levels.length - 1 ? i : i + 1].m1;
    this.Rs = lerp(this.data.R_surface[i], this.data.R_surface[Math.min(i + 1, this.data.R_surface.length - 1)], t);
    this.w = []; this.beta = []; this.zeta = []; this.Pc = []; this.c = []; this.Vc = []; this.zetaWall = []; this.zetaSkin = []; this.zetaBulk = []; this.M = [];
    for (let n = 0; n < this.N; n++) {
      const w = 2 * Math.PI * lerp(A.f[n], B.f[n], t), c = lerp(A.c[n], B.c[n], t), Lam = lerp(A.Lam[n], B.Lam[n], t);
      this.w.push(w); this.c.push(c);
      this.beta.push(w * w / this.g * c);                          // the push per unit a_x (the plant's beta, as in ModalFluid)
      this.Pc.push(this.rho * lerp(A.Ix[n], B.Ix[n], t));         // momentum per unit q_n'
      this.Vc.push(lerp(A.Vc[n], B.Vc[n], t));                     // crest volume on the high half per unit q_n
      this.M.push(this.rho * lerp(A.Ix[n], B.Ix[n], t) / c);        // modal mass: momentum per unit q' over the push coefficient
      const zw = 0.5 * Math.sqrt(this.nu / (2 * w)) * Lam;
      const zs = A.LamS ? 0.5 * Math.sqrt(this.nu / (2 * w)) * lerp(A.LamS[n], B.LamS[n], t) : 0;
      const zb = A.Bk ? this.nu * lerp(A.Bk[n], B.Bk[n], t) / w : 0;
      this.zetaWall.push(zw); this.zetaSkin.push(zs); this.zetaBulk.push(zb);
      this.zeta.push(this.friction ? zw + this.skin * zs + zb + this.zetaCL + this.zetaExtra : this.zetaExtra);
      const e = this.e[n];
      for (let j = 0; j < this.NR; j++) e[j] = lerp(A.e[n][j], B.e[n][j], t);
    }
    this.alpha = this.friction ? this.foamAlpha() : 0;
  };
  // The foam's coefficient alpha (dimensionless) in Viola et al.'s law, for mobile bubble surfaces (friction of the wall
  // Plateau borders ~ gamma Ca^(2/3), Cantat 2013). Beer's surfaces count as mobile: their dilatational modulus is 5-25 mN/m
  // (Wierenga et al. 2023, 24 lagers), below the 30-100 mN/m where foams turn rigid (Denkov et al. 2009). o.foam.alpha sets alpha
  // directly; otherwise:
  //   - Viola et al.'s measurements (soap foam, d = 0.25 mm, gamma = 31.5 mN/m, water, R = 37.05 mm; alpha = 0.010, 0.013, 0.016,
  //     0.023, 0.030 for h = 2.5, 3.3, 4, 5, 6.5 mm), fitted through zero against the effective thickness below: 5.36 per metre
  //     of h_eff (scatter +-20 %);
  //   - depth: the bubbles' speed falls as exp(-z/l) below the surface, l = R/xi_11 (Sauret et al. 2015; Viola's alpha still grew
  //     at 26 bubble layers), and the friction power of a layer as speed^(n+1), so h_eff = l/(n+1) (1 - exp(-(n+1) h/l)), n = 2/3;
  //   - Viola et al.'s scaling alpha ~ (h/d) gamma^(1/3) mu^(2/3) / (rho R^(5/3) g^(2/3)) to the stout's head: bubbles d = 0.2 mm
  //     (fresh nitrogen beer foam, mean radius about 0.1 mm, Ronteltap 1989), gamma = 45 mN/m (beers 38-48 mN/m), the stout's mu, rho.
  TulipModes.prototype.foamAlpha = function () {
    const F = this.foam; if (F.alpha != null) return F.alpha; if (!(F.h > 0)) return 0;
    const n = 2 / 3, d = F.d || 0.2e-3, gam = F.gamma || 0.045, mu = this.nu * this.rho, R = this.Rs;
    const l = R / 1.8412, heff = l / (n + 1) * (1 - Math.exp(-(n + 1) * F.h / l));
    return 5.36 * heff * (0.25e-3 / d) * Math.pow(gam / 0.0315, 1 / 3) * Math.pow(mu / 1.0e-3, 2 / 3) * (1000 / this.rho) * Math.pow(R / 0.03705, -5 / 3);
  };

  // e_n at radius r (linear between the NR points r_j = R(h) j/(NR - 1); beyond R(h) the wall value)
  TulipModes.prototype.shapeAt = function (n, r) {
    const s = Math.min(1, r / this.Rs) * (this.NR - 1), j = Math.min(this.NR - 2, Math.floor(s)), u = s - j, e = this.e[n];
    return e[j] + u * (e[j + 1] - e[j]);
  };
  // the surface height above the floor at (x, y) in the glass frame (x along the road)
  TulipModes.prototype.heightAt = function (x, y) {
    const r = Math.hypot(x, y); if (r < 1e-12) return this.h;
    const c = x / r; let s = 0;
    for (let n = 0; n < this.N; n++) s += this.q[n] * this.shapeAt(n, r);
    return this.h + s * c;
  };
  TulipModes.prototype.columnHeightAt = TulipModes.prototype.heightAt;
  TulipModes.prototype.columnHeights = function () {
    const nx = this.nx, ny = this.ny, dx = this.dx, H = this.colH;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) H[i + nx * j] = this.heightAt(this.x0 + (i + 0.5) * dx, (j + 0.5) * dx);
    return H;
  };
  TulipModes.prototype.levelSet = function () {};
  TulipModes.prototype.wallLift = function () { let s = 0; for (let n = 0; n < this.N; n++) s += this.q[n]; return s; };
  TulipModes.prototype.momentum = function () { let p = 0; for (let n = 0; n < this.N; n++) p += this.Pc[n] * this.qd[n]; return [p, 0]; };
  TulipModes.prototype.liquidMass = function () { return this.rho * this.V; };
  TulipModes.prototype.maxSpeed = function () { return 0; };
  // the mechanical energy of the swing (kinetic + potential, relative to rest), J: for the books and the damping checks.
  // Mode n: (1/2) M_n (q_n'^2 + w_n^2 q_n^2) with the modal mass M_n = rho Ix_n / c_n (the momentum per unit q' over the push)
  TulipModes.prototype.energy = function () {
    let E = 0; for (let n = 0; n < this.N; n++) { const M = this.Pc[n] / this.c[n]; E += 0.5 * M * (this.qd[n] * this.qd[n] + this.w[n] * this.w[n] * this.q[n] * this.q[n]); }
    return E;
  };

  // one step dt with the glass's acceleration (ax, az): the modes by symplectic Euler in substeps of at most 0.5 ms, then the
  // pour over the rim (the weir law of ModalFluid with the tulip's crest volume)
  TulipModes.prototype.step = function (dt, ax, az) {
    // effective gravity g + a_z, never below zero: a glass falling faster than g (a_z < -g) would leave the stout floating
    // free of its floor, which no linear model describes; the same limit as NMFluid in stout-cart.js
    const ns = Math.max(1, Math.ceil(dt / 0.0005 - 1e-9)), hs = dt / ns, gf = Math.max(0, 1 + az / this.g), N = this.N;
    // the foam's friction is a force at the wall: Q = -M_1 alpha w_1^(4/3) R^(1/3) V|V|^(n-1) on every mode (its wall value is 1)
    const Kf = this.alpha > 0 ? this.M[0] * this.alpha * Math.pow(this.w[0], 4 / 3) * Math.cbrt(this.Rs) : 0, nf = this.foam.n;
    let Pv = 0, Pf = 0;
    for (let s = 0; s < ns; s++) {
      let V = 0; for (let m = 0; m < N; m++) V += this.qd[m];
      const Q = Kf > 0 && V !== 0 ? -Kf * V * Math.pow(Math.abs(V), nf - 1) : 0;
      Pf -= Q * V * hs;
      for (let m = 0; m < N; m++) {
        const w = this.w[m], fv = 2 * this.zeta[m] * w * this.qd[m];
        Pv += this.M[m] * fv * this.qd[m] * hs;
        this.qd[m] += hs * (-w * w * gf * this.q[m] - fv - this.beta[m] * ax + Q / this.M[m]);
        this.q[m] += hs * this.qd[m];
      }
    }
    this.Pvisc = Pv / dt; this.Pfoam = Pf / dt;                   // mean power taken by viscosity and by the foam over the step, W
    const Q = this.wallLift(), g = this.g;
    let dV = 0, dPx = 0;
    if (this.h + Math.abs(Q) > this.zRim) {
      const K = 72;
      for (let k = 0; k < K; k++) {
        const th = 2 * Math.PI * (k + 0.5) / K, D = this.h + Q * Math.cos(th) - this.zRim;
        if (D <= 0) continue;
        const qw = this.Cd * (2 / 3) * Math.sqrt(2 * g) * Math.pow(D, 1.5), dVk = qw * this.Rrim * (2 * Math.PI / K) * dt;
        dV += dVk; dPx += this.rho * dVk * Math.sqrt(2 * g * D) * Math.cos(th);
      }
      dV = Math.min(dV, 0.5 * this.V);
      let Vc = 0; for (let m = 0; m < N; m++) Vc += this.Vc[m] * this.q[m];
      const f = Math.abs(Vc) > 1e-12 ? Math.max(0, 1 - dV / Math.abs(Vc)) : 1;
      for (let m = 0; m < N; m++) { this.q[m] *= f; this.qd[m] *= f; }
      this.V -= dV; this.h = this.heightOf(this.V); this.modes();
    }
    this.spillNow = dV > 0 ? 1 : 0; this.spillV += dV; this.spillRate = dV / dt; this.spillPx = dPx; this.spillPz = 0;
    this.t += dt;
  };
  // change the fill (the reader's slider): the volume to height h, the modes there, the swing kept
  TulipModes.prototype.setFill = function (h) { this.h = h; this.V = this.volumeTo(h); this.mLiquid = this.rho * this.V; this.modes(); };

  // A fixed-step driver: the page hands it the real time of each frame; it advances the world in exact steps of `step`
  // seconds (1 ms), so the simulated history never depends on the frame rate: every device computes the same steps. At most
  // maxSteps a frame (a stalled tab does not try to catch up); the time it gives up is counted in `dropped`.
  function FixedStepper(world, o) {
    o = o || {};
    this.world = world; this.step = o.step || 0.001; this.maxSteps = o.maxSteps || 100;
    this.acc = 0; this.dropped = 0; this.steps = 0;
  }
  FixedStepper.prototype.advance = function (dtReal) {
    this.acc += dtReal;
    let n = Math.floor(this.acc / this.step + 1e-9);
    if (n > this.maxSteps) { this.dropped += (n - this.maxSteps) * this.step; this.acc -= (n - this.maxSteps) * this.step; n = this.maxSteps; }
    for (let k = 0; k < n; k++) this.world.advance(this.step);
    this.acc -= n * this.step; this.steps += n;
    return n;
  };

  return { TulipModes, FixedStepper, bracket };
});
