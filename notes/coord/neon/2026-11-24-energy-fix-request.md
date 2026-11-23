# Request to Neon: make the foam's stress force and its return map work-consistent (energy fix for test 4.5)

You are asked for a diagnosis and complete code. Everything you need is below; nothing else is available to you.

## 1. The system
A pint of stout (Newtonian liquid, rho 1007 kg/m^3) with a 19 mm foam head in a glass, simulated in JAX (single file
`tools/fig12/kaggle/stout_jax.py`, class `Stout`). Hybrid particle-grid (APIC) on a MAC grid, dx = 1.5 mm production, 3 mm for tests.
About 1.2 M particles at 1.5 mm (stout 1 001 952, head 213 048); 149 596 at 3 mm (stout 123 188, head 26 408). Particle state float32,
energy sums float64 (jax_enable_x64 is on). Incompressible: a PCG pressure projection each step on cut cells (Batty et al. 2007 face
fractions `self.th[c]`), ghost-fluid free surface p = 0.
The head is an elasto-viscoplastic (EVP) foam carried on the same particles (`s["is_head"]`): isochoric elastic left Cauchy-Green
tensor be (packed (N, 6): xx, yy, zz, then the three off-diagonals), Kirchhoff stress tau = G dev(be), von Mises yield, Tcholakova
viscous law above yield: s = tau_y + A1 gp^0.47 + A2 gp^0.70. Backward-Euler return map with f = I + dt C, where C is the particle's
APIC velocity gradient (C[i, a] = d u_i / d x_a).
Parameters: G = 166.44 Pa; tau_y = 5.415 Pa; A1 = 2.5317, A2 = 0.84793 (SI, gp in 1/s); rho_head = 271.89 kg/m^3; elastic step limit
dt_el = 0.40 dx / sqrt(G / rho_head) (7.67e-4 s at 1.5 mm, 1.53e-3 s at 3 mm); dt = min(2e-3, 0.8 dx / vmax, dt_el), never cut.
m_floor = 0.05 rho_head dx^3 (mass floor on face masses). Wall friction of the foam (Cantat) and a Stokes layer of the stout act in
`friction_evp` (energy logged exactly). Stout viscosity in `viscosity`.

## 2. The test and the failure (Fact, measured)
Test 4.5: free slosh. Half-sine lateral push 3.4 m/s^2 for 0.15 s from t = 0.05 s, then free to 1.5 s. Energy window 0.2-1.0 s.
At 1.5 mm (GPU run, 23 Nov): f_d 2.815 Hz, zeta 0.143 (both pass); but
  -dE_mech (KE + PE) = 1.260 mJ, logged sinks: E_plastic 1.580, E_wall_foam 0.313, E_wall_stout 0.014 mJ; sinks / -dE_mech = 1.514.
  E_plastic = sum over steps and yielded head particles of V_p s_new gp dt.
Audit (Kaggle CPU, 3 mm, same push, window 0.2009-1.0015 s, instrumented, solver unchanged; mJ):
  -dKE 0.0370, -dPE 1.2618, -dU_el 0.0153 (U_el = sum_head V_p (G/2)(tr be - 3)), -dE_mech 1.2988, -dE_tot 1.3141
  E_plastic 0.8711, E_drop 0.9033 (= sum V (G/2)(tr be_trial - tr be_new)), E_wall_foam 0.5103, E_wall_stout 0.0869, E_visc_stout 0.0091
  W_stress_grid 0.2771 (grid kinetic energy removed by the F_dev kick: sum 0.5 M_f (u_before^2 - u_after^2) over occupied open faces)
  W_constit = dU_el + E_plastic = 0.8558; W_constit / W_stress_grid = 3.088
  E_plastic split: particles touching a face with M_f < m_floor 0.0960; within 1.5 dx of the wall 0.2345; interior 0.5406 (62 %)
  Shadow return map driven by f = I + dt D_cell (symmetric cell-centred strain rate of the same final grid velocity, no rotation):
    E_plastic_cellD 0.9190 (within 5.5 % of E_plastic): rotation is not the main cause at 3 mm.
  Sub-step grid-energy ledger (window sums; they telescope to dE_mech within 2.5e-16 J):
    dE_P2G +2.5058, dE_visc -0.0091, dE_wall -0.5971, dE_dev -0.2771, dE_grav_proj +0.0878, dE_G2P_coll -3.0091
  sinks / -dE_mech = 1.130; with U_el, sinks / -dE_tot = 1.117. E_num = -0.163 mJ.
  The pressure + gravity sub-step ADDS +0.088 mJ over the window (6.8 % of -dE_mech).
Slab check (4.3 plug flow, periodic, steady, 1.5 mm): E_plastic / W_grav = 1.0019, E_plastic / E_drop = 0.9891 (the e_plastic line
and the factor-1 convention s gp are right).
Rotation check (one particle, C = pure rotation 30 rad/s, dt 7.67e-4 s, from be = I): s grows 0.051 Pa per step, yields at step 108,
max s 7.48 Pa, E_plastic 1.89 J/m^3 after 1000 steps (f = I + dt C is not objective).
Grid dependence: sinks / -dE_mech is 1.514 at 1.5 mm and 1.130 at 3 mm. Not explained.

## 3. The step order in Stout.step (Fact)
P2G (p2g_evp: momentum, masses, and F_dev from tau at the step's start) -> normalize -> viscosity -> friction_evp -> F_dev kick
u += dt F_dev / max(M_f, m_floor) on faces with th > 0 and weight > 1e-6 -> body_force (gravity) -> pressure projection -> extrapolate
the velocity 3 layers into unknown faces (per side of the glass wall) -> G2P (new particle velocity and C from the FINAL extrapolated
velocity) -> evp_return_map(be, C_new, dt) for head particles -> be updated.

## 4. The code it touches (verbatim, file tools/fig12/kaggle/stout_jax.py)

### evp_tau and evp_return_map (module level)
```python
def evp_tau(be6, G=G_HEAD):
    """Kirchhoff stress G dev(be), packed (N, 6)."""
    tr = (be6[..., 0] + be6[..., 1] + be6[..., 2]) / 3.0
    return G * (be6 - jnp.stack([tr, tr, tr, 0.0 * tr, 0.0 * tr, 0.0 * tr], -1))


def evp_return_map(be6, C, dt, G=G_HEAD, tau_y=TAU_Y, A1=EVP_A1, A2=EVP_A2, n_gp=6, n_c=5):
    """One backward-Euler step of the elasto-viscoplastic head, per particle. be6 (N, 6) float32, C (N, 3, 3) the velocity gradient
    (C[i, a] = d u_i / d x_a). Returns be6_new, yielded (bool), gp (1/s), s_new (Pa), det(be_new), the relative residual of the
    gp equation after n_gp Newton steps. Newton in u = gp^0.47 on h(u) = G dt u^(1/0.47) + A2 u^(0.70/0.47) + A1 u - (s_tr - tau_y),
    from u0 = min((s_tr - tau_y)/A1, ((s_tr - tau_y)/(G dt))^0.47), an upper bound of the root (h is convex and increasing), so the
    iterates fall monotonically onto it. det(D + c I) = 1 by Newton on c^3 - I2 c + I3 - 1 = 0 from c0 = 1 + sqrt(4 I2 / 3) (above
    the largest root, the cubic convex beyond it: monotone)."""
    f = jnp.eye(3, dtype=F32)[None] + dt * C
    B = sym_unpack(be6); Bt = f @ B @ jnp.swapaxes(f, -1, -2)
    Bt = Bt / jnp.cbrt(jnp.maximum(det3(Bt), 1e-30))[..., None, None]
    tr = jnp.trace(Bt, axis1=-2, axis2=-1) / 3.0; I3m = jnp.eye(3, dtype=F32)[None]
    D = Bt - tr[..., None, None] * I3m
    s_tr = G * jnp.sqrt(0.5 * jnp.sum(D * D, (-2, -1)))
    y = s_tr > tau_y
    rhs = jnp.maximum(s_tr - tau_y, 0.0)
    e1 = 1.0 / 0.47; e2 = 0.70 / 0.47
    u = jnp.minimum(rhs / A1, (rhs / (G * dt)) ** 0.47)
    for _ in range(n_gp):
        h = G * dt * u ** e1 + A2 * u ** e2 + A1 * u - rhs
        dh = G * dt * e1 * u ** (e1 - 1.0) + A2 * e2 * u ** (e2 - 1.0) + A1
        u = jnp.maximum(u - h / dh, 0.0)
    gp = jnp.where(y, u ** e1, 0.0)
    res = jnp.where(y, jnp.abs(G * dt * gp + A2 * u ** e2 + A1 * u - rhs) / jnp.maximum(rhs, 1e-30), 0.0)
    s_new = jnp.where(y, tau_y + A1 * gp ** 0.47 + A2 * gp ** 0.70, s_tr)
    Db = jnp.where(y[..., None, None], (s_new / jnp.maximum(s_tr, 1e-30))[..., None, None] * D, D)
    I2 = 0.5 * jnp.sum(Db * Db, (-2, -1)); I3 = det3(Db)
    c = 1.0 + jnp.sqrt(4.0 * I2 / 3.0)
    for _ in range(n_c):
        c = c - (c ** 3 - I2 * c + I3 - 1.0) / (3.0 * c * c - I2)
    Bn = jnp.where(y[..., None, None], Db + c[..., None, None] * I3m, Bt)
    return sym_pack(Bn).astype(F32), y, gp.astype(F32), s_new.astype(F32), det3(Bn), res

```

### Stout.p2g_evp
```python
    def p2g_evp(self, s):
        """Step 4, head_mode "evp": p2g with two materials. Per face: momentum, mass M (kg), the sum of weights (occupancy, returned as
        `mass` so every occupancy test stays a weight test), volume V_f and the head's volume V_hf (m^3), and the explicit deviatoric
        force F_dev = -sum over head particles of V_p tau_p . grad w (N). `vel` is returned as (momentum / M) x (sum of weights), so that
        normalize_force (vel / sum of weights) gives the mass-weighted velocity."""
        dx = self.dx; X, V, C, act, ish = s["xp"], s["vp"], s["C"], s["act"], s["is_head"]
        g = (X - self.origin) / dx
        ci = jnp.floor(g).astype(I32); cfl, cok = self.flat(ci, self.dims)
        cnt = jnp.zeros(math.prod(self.dims), I32).at[cfl].add((cok & act).astype(I32)).reshape(self.dims)
        mpart = s["pmass"]; vpart = s["pvol"]                                  # per particle (state), so resort keeps them
        tau = sym_unpack(jnp.where(ish[:, None], evp_tau(s["be"]), 0.0))
        vel, mass, ex = [], [], dict(M=[], Vf=[], Vh=[], Fdev=[])
        for comp in range(3):
            shape = self.fshape[comp]
            fl, ok, w, wv, cf, fr = self._corners(g, comp, shape)
            dpos = (cf - fr[None]) * dx
            val = w * (V[None, :, comp] + jnp.sum(C[None, :, comp, :] * dpos, -1))
            sg = 2.0 * cf - 1.0
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1) / dx
            fdev = -vpart[None] * jnp.sum(tau[None, :, comp, :] * gw, -1)
            m = ok & act[None]
            cols = [val * mpart[None], w * mpart[None], w, w * vpart[None], w * jnp.where(ish, vpart, 0.0)[None], fdev]
            upd = jnp.stack([jnp.where(m, c_, 0.0) for c_ in cols], -1).reshape(-1, 6)
            acc = jnp.zeros((math.prod(shape), 6), F32).at[fl.reshape(-1)].add(upd)
            M_ = acc[:, 1].reshape(shape); ws = acc[:, 2].reshape(shape)
            vel.append(jnp.where(M_ > 0, acc[:, 0].reshape(shape) / jnp.where(M_ > 0, M_, 1.0), 0.0) * ws); mass.append(ws)
            ex["M"].append(M_); ex["Vf"].append(acc[:, 3].reshape(shape)); ex["Vh"].append(acc[:, 4].reshape(shape)); ex["Fdev"].append(acc[:, 5].reshape(shape))
        # face density rho_f = clip(M / V_f, rho_h, rho); faces with no volume take the stout's; beta = rho / rho_f; head fraction f_h
        ex["rho_f"] = [jnp.where(vf > 0, jnp.clip(M_ / jnp.where(vf > 0, vf, 1.0), RHO_HEAD, self.rho), self.rho).astype(F32) for M_, vf in zip(ex["M"], ex["Vf"])]
        ex["beta"] = [(self.rho / r).astype(F32) for r in ex["rho_f"]]
        ex["fh"] = [jnp.where(vf > 0, jnp.clip(vh / jnp.where(vf > 0, vf, 1.0), 0.0, 1.0), 0.0).astype(F32) for vh, vf in zip(ex["Vh"], ex["Vf"])]
        return vel, mass, cnt, ex

```

### Stout.extrapolate and Stout.g2p (the C computation; g2p then calls _g2p_cont for the continuous model, which keeps C)
```python
    def extrapolate(self, vel, known, layers=3):
        out = []
        for f, k in zip(vel, known):
            for _ in range(layers):
                s = jnp.zeros_like(f); c = jnp.zeros(f.shape, F32)
                for ax in range(3):
                    for d in (-1, 1):
                        kk = sh(k, d, ax, False); s = s + jnp.where(kk, sh(f, d, ax, 0.0), 0.0); c = c + kk
                f = jnp.where(k, f, jnp.where(c > 0, s / jnp.maximum(c, 1.0), 0.0)); k = k | (c > 0)
            out.append(f)
        return out

    # ---------------------------------------------------------------- grid to particles, move, glass, rim (Taichi g2p)
    def g2p(self, s, vel, dt, gx, gz, rot=None, uc=None, vel_out=None):
        dx = self.dx; G = self.G; X, act = s["xp"], s["act"]
        g = (X - self.origin) / dx; vs, Cs, us = [], [], []
        if vel_out is not None: pin = self.p_side(X)   # Step 2: vel is the cavity side's copy, vel_out the outside's
        for comp in range(3):
            fl, ok, w, wv, cf, fr = self._corners(g, comp, self.fshape[comp])
            val = jnp.where(ok, vel[comp].reshape(-1)[fl], 0.0)                    # (8, N)
            if vel_out is not None:
                val = jnp.where(pin[None, :], val, jnp.where(ok, vel_out[comp].reshape(-1)[fl], 0.0))
            vs.append(jnp.sum(w * val, 0))
            if uc is not None: us.append(jnp.sum(w * jnp.where(ok, uc[comp].reshape(-1)[fl], 0.0), 0))
            sg = 2.0 * cf - 1.0                                                     # d(weight)/d(fraction) signs
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1)
            Cs.append(jnp.sum(val[..., None] * gw, 0) / dx)
        newv = jnp.stack(vs, -1); C = jnp.stack(Cs, 1)
        Xn = X + dt * (newv if uc is None else newv + jnp.stack(us, -1))     # the volume correction's drift moves the particle, not its velocity
        if self.cont: return self._g2p_cont(s, X, Xn, newv, C, act, dt, gx, gz, rot)
        below = Xn[:, 2] < 0.1 * dx
        Xn = Xn.at[:, 2].set(jnp.where(below, 0.1 * dx, Xn[:, 2]))
        newv = newv.at[:, 2].set(jnp.where(below & (newv[:, 2] < 0), 0.0, newv[:, 2]))
```

### Stout.step (whole function up to the return map; the lines with `aud`/`au` are a read-only audit, default off)
```python
    def step(self, s, dt, gx, gz, prep=None, rot=None, wind=None):
        """rot = (om, al, zS): the glass also turns (Fig. 16); None: the glass only translates (Fig. 12, unchanged)."""
        dt = jnp.asarray(dt, F32); gx = jnp.asarray(gx, F32); gz = jnp.asarray(gz, F32)
        if rot is not None: rot = tuple(jnp.asarray(r, F32) for r in rot)
        pr = self.prepare(s) if prep is None else prep
        aud = self.evp and self.audit; s0 = s
        vel, mass = pr["vel"], pr["mass"]
        # 13 Nov 2026, run 3: gravity's kick of this step (dt g) was added before the viscous and thin-layer stresses, so the glass's
        # Stokes layer and the head braked gravity itself: a pint at rest lost 0.63 mJ of potential energy in 2 s, the books
        # counted 0.77 mJ "dissipated", and the stout stirred (up to 3.7 mm/s). The stresses now act on the velocity the stout
        # has (the last step's, free of divergence); the body force is added after them, just before the pressure step.
        vel = self.normalize_force(vel, mass, dt, 0.0, 0.0)
        # the head's vertical velocity as the step starts: its own, kept from the last step (the particles' hand-over smooths
        # the stout's velocity at the surface, and the head's momentum equation must close step by step)
        w_old = jnp.broadcast_to(s["wh"][:, :, None], vel[2].shape)
        ph, liq, nsel, H = pr["ph"], pr["liq"], pr["nsel"], pr["H"]
        ex = pr.get("ex") if self.evp else None
        if aud: au = [vel]
        if self.nu > 0: vel = self.viscosity(vel, mass, dt, fh=None if ex is None else ex["fh"])
        if aud: au.append(vel)
        z = jnp.zeros((), F64); ew = es = ef = z
        if self.evp:   # Step 4: the glass's stress (stout and head), then the head's deviatoric force u += dt F_dev / max(M_f, m_floor)
            vel, ew_s, ew_f = self.friction_evp(vel, mass, dt, ex); ew = ew_s + ew_f
            if aud: au.append(vel)
            vel = [jnp.where((self.th[c] > 0) & (mass[c] > 1e-6), vel[c] + dt * ex["Fdev"][c] / jnp.maximum(ex["M"][c], self.m_floor), vel[c]).astype(F32)
                   for c in range(3)]
            if aud: au.append(vel)
        elif self.gs > 0 or self.skin or self.head: vel, ew, es, ef = self.friction(vel, mass, ph, liq, dt, s["hf"])
        vel = self.body_force(vel, mass, dt, gx, gz, rot)
        if self.cont and wind is not None: vel = self.air_drag(vel, mass, pr["ph"], pr["liq"], dt, wind, beta=None if ex is None else ex["beta"])
        # the head's weight on the surface (verification.md item 4), in the solver's pressure units (Pa x dt / rho); with rot, the
        # vertical field of each column at the fill height
        gzh = gz if rot is None else self.frame_accel(self.colx, self.G.fill, 0.0, 0.0, gx, gz, rot)[1]
        ps = (self.rho_f * s["hf"] * jnp.maximum(-gzh, 0.0) * dt / self.rho).astype(F32) if self.head else jnp.zeros((self.nx, self.ny), F32)
        mu = (self.rho_f * s["hf"] / self.rho).astype(F32) if (self.head and self.head_mass) else None
        gdt = jnp.maximum(-gzh, 0.0) * dt
        if rot is not None: gdt = gdt[:, :, None]
        uc = None
        if self.vol_corr > 0:   # the volume correction moves positions only (Kugelstadt et al. 2019): its own projection of a zero velocity field
            # the gate (run 4b): the correction acts only while the whole pint has swollen by more than 4 % (fully from 8 %); run 4 without
            # it stirred the pint at rest at 1.5 mm (rest guard: 1.54 mm, limit 0.75 mm)
            gate = jnp.clip((self.swelling(liq, s["act"]) - 0.04) / 0.04, 0.0, 1.0).astype(F32)
            src = self.volume_source(pr["cnt"], liq, dt, gate); zf = [jnp.zeros_like(v) for v in vel]
            uc, kc, _, _, _, _, _ = self.pressure(zf, ph, liq, jnp.zeros_like(s["p"]), jnp.zeros((self.nx, self.ny), F32), src=src)
            uc = self.extrapolate(uc, kc)
        pst = self.tension(ph, s["hf"], dt) if self.cont else None
        vel, known, p, it, res, res_abs, bnorm = self.pressure(vel, ph, liq, s["p"], ps, mu=mu, w_old=w_old, geff_dt=gdt, pst=pst,
                                               beta=None if ex is None else ex["beta"])
        if aud: au.append(vel)
        if mu is not None:   # the head's new vertical velocity: that of the face its surface crosses (liquid below, air above)
            sf = self._surf_faces(ph, liq); nsf = jnp.sum(sf, 2)
            wh = jnp.where(nsf > 0, jnp.sum(jnp.where(sf, vel[2], 0.0), 2) / jnp.maximum(nsf, 1), s["wh"]).astype(F32)
            s = dict(s, wh=wh)
        if self.side_vis:   # Step 2: one extrapolated copy per side of the glass below the rim (see enable_side_vis)
            vel_out = self.extrapolate(vel, [k & (~fs | ~fb) for k, fs, fb in zip(known, self.fside, self.fbelow)])
            vel = self.extrapolate(vel, [k & (fs | ~fb) for k, fs, fb in zip(known, self.fside, self.fbelow)])
        else:
            vel = self.extrapolate(vel, known); vel_out = None
        s, mom = self.g2p(s, vel, dt, gx, gz, rot, uc=uc, vel_out=vel_out)
        evd = {}
        if self.evp:   # Step 4: the head's return map, after G2P, with the APIC velocity gradient C of the new step
            ben, yl, gp, s_new, det, rres = evp_return_map(s["be"], s["C"], dt)
            hd = s["is_head"] & s["act"]
            if aud: s, adiag = self._audit_evp(s0, s, au, vel, mass, ex, dt, gz, ben, yl, gp, s_new, hd)
            s = dict(s, be=jnp.where(hd[:, None], ben, s["be"]))
            mpart = s["pmass"].astype(F64)
            okf = [(self.th[c] > 0) & (mass[c] > 1e-6) for c in range(3)]
```

## 5. What I ask you for
A. Diagnosis, with derivation: which grid velocity must drive the return map (C or a strain rate) so that the constitutive work
   W_constit equals the work F_dev takes from the grid, step by step (discrete adjoint). Treat: USF vs USL (stress update before or after
   the grid solve); the faces where the velocity is extrapolated or masked (unknown faces, th = 0, the mass floor); and an objective rate
   (e.g. f = exp(dt W) applied as a rotation, or a midpoint / Hughes-Winget update) so pure rotation gives no stress. Say which of these
   explains the measured ratio 3.09 and the 1.5 mm vs 3 mm difference, and mark each statement Fact, Inference or Opinion.
B. Whether the +0.088 mJ from the gravity + pressure sub-step needs a fix now, and why.
C. Complete code: each changed function in full, headed with its path and the function it replaces (e.g. "tools/fig12/kaggle/
   stout_jax.py, replaces Stout.step"). No diffs, no "...", no placeholders. New behaviour behind a flag on Stout (attribute, default
   off); with the flag off, the default path must stay bit for bit unchanged (keep every existing line and its order). Keep the audit
   lines (`aud`, `au`, `_audit_evp`) working.
D. One complete Kaggle CPU test notebook script (a single Python file) that runs the 3 mm slosh to 1.0 s with the flag ON and OFF and
   writes JSON. It may assume the repository files are written under /kaggle/working/repo by an embedding header I add (paths
   tools/fig12/kaggle/stout_jax.py, public/scripts/guinness-glass.js). The set-up must equal this one:
     G = SJ.Geometry(R, 0.0005, 0.125, dx, body=(0.155, 0.062, -0.030), top=0.08, lip=0.00125)  (R from guinness-glass.js "R: [...]")
     S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096, head_mode="evp"); S.gamma = 0.0
     S.enable_side_vis(); S.enable_ls_extend(); S.wall_guard = True; s = S.init_state()
     step: s, d = S.step(s, dt, gx, -9.81, prep=S.prepare(s)), jitted; gx = 3.4 sin(pi (t_mid - 0.05) / 0.15) for 0.05 <= t_mid < 0.20.
   Log per step: KE, PE, U_el, E_plastic, E_wall_foam, E_wall_stout, W_stress_grid, W_constit (S.audit = True and S.diag_g2p = True give
   these; the state then needs s["be_cell"] = identity packed [1,1,1,0,0,0] per particle).
E. Pass marks for the fix, fixed now and each shown reachable by construction, written with abs( ) (no vertical bars), e.g. on
   W_constit / W_stress_grid, on sinks / -dE_tot, and on the rotation check. The 4.5 marks stay unchanged:
   f_d in [2.70, 3.15] Hz; zeta over 0.2-1.2 s in [0.13, 0.33]; zeta 0.6-1.2 s > zeta 0.2-0.6 s; abs(sinks / (-dE_mech) - 1) < 0.25
   and -dE_mech >= sinks within 2 %; books < 1e-6; 0 real crossings; 0 in solid; it < 600; converged.
F. No tuning of any physical parameter (G, tau_y, A1, A2, friction, m_floor stay).
G. One sentence: the physical picture of why the fix works.
