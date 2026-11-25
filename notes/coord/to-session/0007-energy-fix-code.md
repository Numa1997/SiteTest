# 0007: the energy fix for 4.5 (work-consistent return map + objective increment), from the coordinator, 25 Nov 2026

Neon could not answer the 0006 request; the owner asked the coordinator to solve it and give it to you directly. Rules of 0006 stand:
you write no code and run nothing. Paste the four blocks below EXACTLY, commit under the owner's identity, push, report. The Kaggle test
run is launched by the coordinator through the connector after your commit; do not launch it.

## Diagnosis (short)
Fact (0004 audit, 3 mm): the foam's constitutive work 0.856 mJ is 3.09 x the kinetic energy its stress force removes from the grid
(0.277 mJ). Inference, by construction of the code: F_dev = -sum_p V_p tau_p . grad w_fp, so the kick removes exactly
dt sum_p V_p tau_p : C_p(u_k), where C_p(u_k) is the P2G-stencil gradient of u_k = (M_f / max(M_f, m_floor)) x the kick's midpoint
velocity on the kicked faces (0 elsewhere). The return map is instead driven by C from the FINAL, projected and extrapolated velocity,
which carries deformation the stress force never acted on (pressure, friction, transfer, extrapolation across the free surface where
the whole head sits). Driving the return map with C(u_k) at the P2G positions makes trial elastic work = force work to first order in
dt: the books close by construction. This is the update-stress-first ordering with the exact adjoint stencil. The Hughes-Winget
increment f = (I - dt C/2)^-1 (I + dt C/2) is orthogonal for pure spin, so rotation makes no stress (the rotation check).
Not fixed now: the +0.088 mJ the gravity+pressure step adds (6.8 % of -dE_mech); it is measured again in the test, decided after.
Risk (Inference): with u_k = 0 on closed wall faces the foam next to the wall shears against zero; the motion marks (f_d, zeta) at
1.5 mm decide whether that is acceptable.

## Block 1: tools/fig12/kaggle/stout_jax.py, replaces the module function evp_return_map (signature gains hw=False)
```python
def evp_return_map(be6, C, dt, G=G_HEAD, tau_y=TAU_Y, A1=EVP_A1, A2=EVP_A2, n_gp=6, n_c=5, hw=False):
    """One backward-Euler step of the elasto-viscoplastic head, per particle. be6 (N, 6) float32, C (N, 3, 3) the velocity gradient
    (C[i, a] = d u_i / d x_a). Returns be6_new, yielded (bool), gp (1/s), s_new (Pa), det(be_new), the relative residual of the
    gp equation after n_gp Newton steps. Newton in u = gp^0.47 on h(u) = G dt u^(1/0.47) + A2 u^(0.70/0.47) + A1 u - (s_tr - tau_y),
    from u0 = min((s_tr - tau_y)/A1, ((s_tr - tau_y)/(G dt))^0.47), an upper bound of the root (h is convex and increasing), so the
    iterates fall monotonically onto it. det(D + c I) = 1 by Newton on c^3 - I2 c + I3 - 1 = 0 from c0 = 1 + sqrt(4 I2 / 3) (above
    the largest root, the cubic convex beyond it: monotone)."""
    if hw:   # 25 Nov 2026 (flag evp_hw): Hughes-Winget increment f = (I - dt C / 2)^-1 (I + dt C / 2); for a pure rotation C = W it is
        # exactly orthogonal, so be = I stays I and spin makes no stress (f = I + dt C grows s by G (W dt)^2 / sqrt 3 per step)
        I3h = jnp.eye(3, dtype=F32)[None]
        f = jnp.linalg.solve(I3h - 0.5 * dt * C, I3h + 0.5 * dt * C)
    else:
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

## Block 2: tools/fig12/kaggle/stout_jax.py, NEW method of class Stout, insert directly above Stout.step
```python
    def evp_grad(self, X, vel):
        """25 Nov 2026 (flag evp_consistent): the velocity gradient C[i, a] = sum over the 8 MAC corners of u_i grad_a w, at positions X,
        with exactly the weights and weight gradients P2G uses for F_dev. With vel = the kick's velocity (see step), sum_p V_p tau_p : C_p
        equals the kinetic energy the F_dev kick takes from the grid divided by dt: the return map then works on the deformation the
        stress force acted on (the discrete adjoint), so the foam cannot dissipate energy the flow never gave it."""
        dx = self.dx; g = (X - self.origin) / dx; Cs = []
        for comp in range(3):
            fl, ok, w, wv, cf, fr = self._corners(g, comp, self.fshape[comp])
            val = jnp.where(ok, vel[comp].reshape(-1)[fl], 0.0)
            sg = 2.0 * cf - 1.0
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1)
            Cs.append(jnp.sum(val[..., None] * gw, 0) / dx)
        return jnp.stack(Cs, 1)
```

## Block 3: tools/fig12/kaggle/stout_jax.py, replaces Stout.step (whole method)
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
            v_bk = vel
            vel = [jnp.where((self.th[c] > 0) & (mass[c] > 1e-6), vel[c] + dt * ex["Fdev"][c] / jnp.maximum(ex["M"][c], self.m_floor), vel[c]).astype(F32)
                   for c in range(3)]
            if aud: au.append(vel)
            if getattr(self, "evp_consistent", False):   # the kick's work-conjugate velocity: (M / max(M, m_floor)) x the kick's midpoint
                # velocity on the kicked faces, 0 elsewhere; then sum_f u_k . F_dev dt is exactly the kick's kinetic-energy change
                uk = [jnp.where((self.th[c] > 0) & (mass[c] > 1e-6), ex["M"][c] / jnp.maximum(ex["M"][c], self.m_floor) * 0.5 * (v_bk[c] + vel[c]), 0.0).astype(F32)
                      for c in range(3)]
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
            if getattr(self, "evp_consistent", False):   # the gradient of the kick's velocity at the P2G positions (step start)
                ben, yl, gp, s_new, det, rres = evp_return_map(s["be"], self.evp_grad(s0["xp"], uk), dt, hw=getattr(self, "evp_hw", False))
            else:
                ben, yl, gp, s_new, det, rres = evp_return_map(s["be"], s["C"], dt, hw=getattr(self, "evp_hw", False))
            hd = s["is_head"] & s["act"]
            if aud: s, adiag = self._audit_evp(s0, s, au, vel, mass, ex, dt, gz, ben, yl, gp, s_new, hd)
            s = dict(s, be=jnp.where(hd[:, None], ben, s["be"]))
            mpart = s["pmass"].astype(F64)
            okf = [(self.th[c] > 0) & (mass[c] > 1e-6) for c in range(3)]
            n_floor = sum(jnp.sum(okf[c] & (ex["M"][c] < self.m_floor), dtype=I32) for c in range(3))           # diagnostic: faces where
            n_floor_head = sum(jnp.sum(okf[c] & (ex["M"][c] < self.m_floor) & (ex["fh"][c] > 0.5), dtype=I32) for c in range(3))  # m_floor acts
            e_plastic = jnp.sum(jnp.where(hd & yl, s["pvol"].astype(F64) * s_new.astype(F64) * gp.astype(F64), 0.0)) * dt   # sum V_p s gp dt (J)
            evd = dict(e_wall_stout=ew_s, e_wall_foam=ew_f, e_plastic=e_plastic, n_yielded=jnp.sum(hd & yl, dtype=I32), gp_max=jnp.max(jnp.where(hd, gp, 0.0)), s_max=jnp.max(jnp.where(hd, s_new, 0.0)),
                       det_min=jnp.min(jnp.where(hd, det, 1.0)), det_max=jnp.max(jnp.where(hd, det, 1.0)), rm_res=jnp.max(jnp.where(hd, rres, 0.0)),
                       mom_phys=jnp.sum(jnp.where(s["act"][:, None], mpart[:, None] * s["vp"].astype(F64), 0.0), 0), n_floor=n_floor, n_floor_head=n_floor_head)
            if aud: evd.update(adiag)
        if self.head: s = self.head_spill(s, H, dt, gx, gz, rot)
        s = dict(s, p=p, ewall=s["ewall"] + ew, eskin=s["eskin"] + es, efoam=s["efoam"] + ef)
        vmax = jnp.max(jnp.where(s["act"][:, None], jnp.abs(s["vp"]), 0.0))
        mhead = self.rho_f * jnp.sum((s["hf"] * self.afill).astype(F64)) * self.dx ** 2
        diag = dict(it=it, res=res, res_abs=res_abs, bnorm=bnorm, conv=(res < self.tol) | (res_abs < self.atol), mom=mom, nact=jnp.sum(s["act"], dtype=I32),
                    nsel=nsel, vmax=vmax, mhead=mhead, **evd)
        return s, diag
```
Flags (attributes, read with getattr, default off): Stout.evp_consistent (return map driven by the kick's gradient) and Stout.evp_hw
(Hughes-Winget increment). With both off every computed array is the same as before, bit for bit.

## Block 4: tools/spill/audit_0004.py, replaces the whole file (env EVPFIX=1 turns both flags on for the slosh and the rotation check,
outputs to audit_0004_fix/)
```python
"""Instruction 0004 (23 Nov 2026): the energy-closure audit of test 4.5, measurement only. Kaggle CPU. Run from the repository's root:
    python3 tools/spill/audit_0004.py OUTDIR      (env SUBRUN = "smoke" or "full"; DX default 0.003; ONLY e.g. "rot,slab,ident,slosh")
Blocks, each guarded, results to OUTDIR/audit_0004/:
  rot    the rigid-rotation check: one particle, C = Omega (rotation about z, D = 0), Omega 30 rad/s, dt 7.67e-4 s, 1000 steps from
         be = I, through stout_jax.evp_return_map: max s and E_plastic per unit volume (V = 1 m^3).
  slab   test (a): tools/spill/step4_slab.py, 4.3 case C1 (h 0.018 m, dx 1.5 mm, tau_b 1.5 tau_y, no vertical jitter, 2.0 s) with
         EAUDIT=1 (window 1.0-2.0 s).
  ident  the default path is unchanged: N_IDENT steps of the 4.5 set-up at DX with stout_jax at 5acb718 (tools/fig12/kaggle/
         stout_jax_5acb718.py, embedded by the launcher) and with the current stout_jax, audit off: every state array compared bit for bit.
  slosh  tests (b), (c), (d)-ledger: the 4.5 set-up (Fig. 16 deck, model "wall", head_mode "evp", gamma 0, side visibility, solid
         extension, wall guard, lip 1.25 mm) at DX, the same push (3.4 m/s^2 half-sine 0.15 s from 0.05 s), dt = min(2e-3, 0.8 dx / vmax,
         0.40 dx / c_s), never cut, to the first step with t >= 1.0 s, with S.audit = True (stout_jax.Stout._audit_evp); per-step JSONL."""
import json, os, sys, time, math, datetime, subprocess, traceback, importlib.util, hashlib
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
KDIR = os.path.join(ROOT, "tools", "fig12", "kaggle"); sys.path.insert(0, KDIR)
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import stout_jax as SJ  # noqa: E402
EVPFIX = os.environ.get("EVPFIX", "0") == "1"   # 25 Nov 2026: Stout.evp_consistent and evp_hw on (the energy fix, instruction 0007)
SUB = os.environ.get("SUBRUN", "smoke"); DXA = float(os.environ.get("DX", "0.003")); ONLY = os.environ.get("ONLY", "rot,slab,ident,slosh").split(",")
VOUT = os.path.join(OUT, "audit_0004_fix" if EVPFIX else "audit_0004"); os.makedirs(VOUT, exist_ok=True)
T0 = time.time()
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
RG = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); DZP, FILL = 0.0005, 0.125; F16 = (0.155, 0.062, -0.030)


def say(m):
    line = f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}"
    print(line, flush=True); open(os.path.join(VOUT, f"progress_{SUB}.log"), "a").write(line + "\n")


def dump(name, obj):
    json.dump(obj, open(os.path.join(VOUT, name), "w"), indent=1, default=str)


def setup(mod, dxd, audit):
    G = mod.Geometry(RG, DZP, FILL, dxd, body=F16, top=0.08, lip=0.00125)
    S = mod.Stout(G, model="wall", K_frac=1.0, M_drops=4096, head_mode="evp"); S.gamma = 0.0
    S.enable_side_vis(); info = S.enable_ls_extend(); S.wall_guard = True
    if audit: S.audit = True; S.diag_g2p = True
    if audit and EVPFIX: S.evp_consistent = True; S.evp_hw = True
    s = S.init_state()
    if audit: s = dict(s, be_cell=jnp.tile(jnp.asarray([1, 1, 1, 0, 0, 0], jnp.float32), (S.N, 1)))
    return G, S, s, info


say(f"start {SUB}: DX {DXA}, blocks {ONLY}, device {jax.devices()[0]}, jax {jax.__version__}")

# ------------------------------------------------------------------------------------------------ rot
if "rot" in ONLY:
    try:
        Om, dt, n = 30.0, 7.67e-4, 1000
        C = jnp.asarray([[[0.0, -Om, 0.0], [Om, 0.0, 0.0], [0.0, 0.0, 0.0]]], jnp.float32)
        be = jnp.asarray([[1, 1, 1, 0, 0, 0]], jnp.float32); rm = jax.jit(lambda b: SJ.evp_return_map(b, C, dt, hw=EVPFIX))
        smax = 0.0; epl = 0.0; first_yield = None; rows = []
        for k in range(1, n + 1):
            be, y, gp, s_new, det, res = rm(be)
            sv = float(s_new[0]); smax = max(smax, sv); e = float(y[0]) * sv * float(gp[0]) * dt; epl += e
            if bool(y[0]) and first_yield is None: first_yield = k
            if k % 50 == 0 or k <= 3: rows.append(dict(step=k, s=sv, yielded=bool(y[0]), gp=float(gp[0]), E_plastic_cum=epl, det=float(det[0])))
        pred = SJ.G_HEAD * (Om * dt) ** 2 / math.sqrt(3.0)
        out = dict(Omega=Om, dt=dt, steps=n, V_p_m3=1.0, max_s_rot_Pa=smax, E_plastic_rot_J_per_m3=epl, first_yield_step=first_yield, tau_y=SJ.TAU_Y,
                   predicted_s_increment_per_step_Pa=pred, rows=rows,
                   pass_marks=dict(max_s_rot_lt_0p05_tau_y=bool(smax < 0.05 * SJ.TAU_Y), E_plastic_rot_eq_0=bool(epl == 0.0)))
        dump("rotation_check.json", out); say(f"rot: max_s {smax:.4f} Pa, E_plastic {epl:.4e} J/m^3, first yield step {first_yield}")
    except Exception as ex:
        say(f"rot FAILED: {ex!r}"); traceback.print_exc(); dump("rotation_check.json", dict(error=repr(ex)))

# ------------------------------------------------------------------------------------------------ slab (test a)
if "slab" in ONLY:
    try:
        env = dict(os.environ, JAX_PLATFORMS="cpu", SUBRUN=SUB, ONLY="4.3", HH="0.018", JITZ="0", T43="2.0", DX="0.0015", FRAC43="1.5", EAUDIT="1")
        if SUB == "smoke": env.update(EAUD_T0="0.005", EAUD_T1="0.012")
        say(f"slab: step4_slab.py C1 with EAUDIT=1 ({SUB})")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "spill", "step4_slab.py"), VOUT], env=env, capture_output=True, text=True)
        open(os.path.join(VOUT, f"slab_{SUB}.log"), "w").write(r.stdout + r.stderr); say(f"slab rc {r.returncode}")
    except Exception as ex:
        say(f"slab FAILED: {ex!r}"); traceback.print_exc()

# ------------------------------------------------------------------------------------------------ ident (default path unchanged)
if "ident" in ONLY:
    try:
        p_old = os.path.join(KDIR, "stout_jax_5acb718.py")
        spec = importlib.util.spec_from_file_location("stout_jax_5acb718", p_old); SO = importlib.util.module_from_spec(spec); spec.loader.exec_module(SO)
        IDX = float(os.environ.get("IDENT_DX", str(DXA))); nid = int(os.environ.get("N_IDENT", "3")); hashes = {}
        for tag, mod, au_ in (("old_5acb718", SO, False), ("new_audit_off", SJ, False), ("new_audit_on", SJ, True)):
            G, S, s, _ = setup(mod, IDX, au_)
            prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt, gx: S.step(s, dt, gx, -9.81, prep=pr))
            cs = math.sqrt(mod.G_HEAD / mod.RHO_HEAD); dt_el = 0.40 * IDX / cs; t = 0.0; vmax = 0.0
            for k in range(nid):
                dt = min(2e-3, dt_el, 0.8 * IDX / max(vmax, 1e-12)); s, d = step(s, prep(s), dt, 0.0); t += dt; vmax = float(d["vmax"])
            hashes[tag] = {kk: hashlib.sha256(np.ascontiguousarray(np.asarray(v)).tobytes()).hexdigest() for kk, v in sorted(s.items())}
            say(f"ident {tag}: {nid} steps, t {t:.6f}")
        same = {kk: hashes["old_5acb718"][kk] == hashes["new_audit_off"].get(kk) for kk in hashes["old_5acb718"]}
        mot = ("xp", "vp", "C", "be", "act", "p", "wh")
        out_on = {kk: hashes["old_5acb718"][kk] == hashes["new_audit_on"].get(kk) for kk in mot}
        out = dict(audit_on_motion_identical=out_on, steps=nid, dx=IDX, old_sha256_of_file=hashlib.sha256(open(p_old, "rb").read()).hexdigest(), keys=same, all_identical=all(same.values()),
                   extra_keys_new=sorted(set(hashes["new_audit_off"]) - set(hashes["old_5acb718"])))
        dump("default_path_identity.json", out); say(f"ident: all identical {out['all_identical']}")
    except Exception as ex:
        say(f"ident FAILED: {ex!r}"); traceback.print_exc(); dump("default_path_identity.json", dict(error=repr(ex)))

# ------------------------------------------------------------------------------------------------ slosh (tests b, c, d-ledger)
if "slosh" in ONLY:
    rows = []
    try:
        PA, PT, P0, T = 3.4, 0.15, 0.05, 1.0
        G, S, s, info = setup(SJ, DXA, True)
        cs = math.sqrt(SJ.G_HEAD / SJ.RHO_HEAD); dt_el = 0.40 * DXA / cs
        say(f"slosh: grid {G.nx} x {G.ny} x {G.nz}, N {S.N} (stout {S.N_stout}, head {S.N_head}), m_stout0 {S.m_stout0:.6f} kg, m_head0 {S.m_head0:.6f} kg, "
            f"V_head {S.V_head:.4e} m^3, m_floor {S.m_floor:.4e} kg, dt_el {dt_el:.4e} s")
        prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt, gx: S.step(s, dt, gx, -9.81, prep=pr))
        f6 = lambda v: float(v)
        KE0 = 0.5 * float(jnp.sum(s["pmass"].astype(jnp.float64) * jnp.sum(s["vp"].astype(jnp.float64) ** 2, 1)))
        PE00 = 9.81 * float(jnp.sum(s["pmass"].astype(jnp.float64) * s["xp"][:, 2].astype(jnp.float64)))
        rows.append(dict(step=0, t=0.0, KE_p=KE0, PE=PE00, U_el=0.0))
        fh = open(os.path.join(VOUT, f"slosh_audit_{SUB}.jsonl"), "w"); fh.write(json.dumps(rows[0]) + "\n")
        t = 0.0; k = 0; vmax = 0.0; nmax = 5 if SUB == "smoke" else 10 ** 9; tc = time.time()
        keys = ("dE_P2G", "dE_visc", "dE_wall", "dE_dev", "dE_grav_proj", "dE_G2P_coll", "dE_mech", "W_sg_mfloor", "E_drop", "W_trial",
                "E_pl_mfloor", "E_pl_wall", "E_pl_interior", "E_pl_cellD")
        while t < T - 1e-12 and k < nmax:
            dt = min(2e-3, dt_el, 0.8 * DXA / max(vmax, 1e-12))
            tm = t + 0.5 * dt; gx = PA * math.sin(math.pi * (tm - P0) / PT) if P0 <= tm < P0 + PT else 0.0
            s, d = step(s, prep(s), dt, gx); t += dt; k += 1; vmax = float(d["vmax"])
            row = dict(step=k, t=t, dt=dt, gx=gx, it=int(d["it"]), res=f6(d["res"]), conv=bool(d["conv"]), KE_p=f6(d["aud_KE_p"]), PE=f6(d["aud_PE"]),
                       U_el=f6(d["aud_U_el"]), e_plastic=f6(d["e_plastic"]), e_wall_foam=f6(d["e_wall_foam"]), e_wall_stout=f6(d["e_wall_stout"]),
                       **{k_: f6(d["aud_" + k_]) for k_ in keys}, n_yielded=int(d["n_yielded"]), ny_mfloor=int(d["aud_ny_mfloor"]), ny_wall=int(d["aud_ny_wall"]),
                       ny_interior=int(d["aud_ny_interior"]), ny_cellD=int(d["aud_ny_cellD"]), n_head_mfloor=int(d["aud_n_head_mfloor"]),
                       n_head_wall=int(d["aud_n_head_wall"]), n_floor=int(d["n_floor"]), s_max=f6(d["s_max"]), s_max_cellD=f6(d["aud_s_max_cellD"]),
                       det_min=f6(d["det_min"]), det_max=f6(d["det_max"]), n_gone=int(d["aud_n_gone"]), vmax=vmax, wall_s=round(time.time() - tc, 2))
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or k % 50 == 0: say(f"slosh: step {k}  t {t:.4f}  gx {gx:.3f}  it {row['it']}  KE {row['KE_p']:.4e}  U_el {row['U_el']:.4e}  "
                                         f"yielded {row['n_yielded']}  ({row['wall_s']:.0f} s)")
        fh.close(); say(f"slosh: {k} steps to t {t:.5f} in {time.time() - tc:.0f} s")
    except Exception as ex:
        say(f"slosh FAILED at step {len(rows)}: {ex!r}"); traceback.print_exc()
    try:   # the window's numbers (Neon section 5) and the marks (STATE-projection-fix.md, "0004 step 5")
        ta, tb = (0.2, 1.0) if SUB == "full" else (rows[2]["t"], rows[-1]["t"])
        ia = next(i for i, r in enumerate(rows) if r["t"] >= ta - 1e-12); ib = next(i for i, r in enumerate(rows) if r["t"] >= tb - 1e-12)
        W = lambda key: sum(r[key] for r in rows[ia + 1:ib + 1]); A, B = rows[ia], rows[ib]
        dKE = B["KE_p"] - A["KE_p"]; dPE = B["PE"] - A["PE"]; dU = B["U_el"] - A["U_el"]; dEm = dKE + dPE; dEt = dEm + dU
        Ep, Ewf, Ews = W("e_plastic"), W("e_wall_foam"), W("e_wall_stout"); Ev = -W("dE_visc"); Wsg = -W("dE_dev"); Wc = dU + Ep
        sinks = Ep + Ewf + Ews; sinks_all = sinks + Ev; led = sum(W(k_) for k_ in ("dE_P2G", "dE_visc", "dE_wall", "dE_dev", "dE_grav_proj", "dE_G2P_coll"))
        r_ = lambda x, y: x / y if y else float("nan")
        tab = dict(t_a=A["t"], t_b=B["t"], step_a=A["step"], step_b=B["step"], minus_dKE=-dKE, minus_dPE=-dPE, minus_dU_el=-dU, minus_dE_mech=-dEm, minus_dE_tot=-dEt,
                   PE_drift_tb_minus_0=B["PE"] - rows[0]["PE"], U_el_a=A["U_el"], U_el_b=B["U_el"], U_el_min=min(r["U_el"] for r in rows),
                   E_plastic=Ep, E_drop=W("E_drop"), W_trial=W("W_trial"), E_wall_foam=Ewf, E_wall_stout=Ews, E_visc_stout=Ev, W_stress_grid=Wsg,
                   W_stress_grid_on_mfloor_faces=W("W_sg_mfloor"), W_constit=Wc, W_constit_over_W_stress_grid=r_(Wc, max(Wsg, 1e-12)),
                   E_plastic_mfloor=W("E_pl_mfloor"), E_plastic_wall=W("E_pl_wall"), E_plastic_interior=W("E_pl_interior"), E_plastic_cellD=W("E_pl_cellD"),
                   E_plastic_minus_cellD=Ep - W("E_pl_cellD"), E_num=-dEt - sinks_all, sinks_logged=sinks, sinks_all=sinks_all,
                   sinks_over_minus_dE_mech=r_(sinks, -dEm), r_tot=r_(sinks, -dEt), closure_all_over_minus_dE_tot=r_(sinks_all, -dEt),
                   ledger=dict(dE_P2G=W("dE_P2G"), dE_visc=W("dE_visc"), dE_wall=W("dE_wall"), dE_dev=W("dE_dev"), dE_grav_proj=W("dE_grav_proj"),
                               dE_G2P_coll=W("dE_G2P_coll"), sum=led, dE_mech_stores=dEm, dE_mech_steps=W("dE_mech")),
                   n_floor_max_window=max(r["n_floor"] for r in rows[ia + 1:ib + 1]), n_gone_total=sum(r.get("n_gone", 0) for r in rows))
        pm = dict(b_U_el_min_ge_m1e12=bool(tab["U_el_min"] >= -1.0e-12), b_U_el_a_gt_b=bool(A["U_el"] > B["U_el"]),
                  b_alone_explains=bool(tab["sinks_over_minus_dE_mech"] > 1.25 and tab["r_tot"] <= 1.02 and abs(tab["r_tot"] - 1.0) < 0.25),
                  b_partial_only_r_tot_gt_1p05=bool(tab["r_tot"] > 1.05),
                  c_adjoint_within_5pct=bool(abs(Wc / max(Wsg, 1.0e-12) - 1.0) < 0.05), c_proved_ratio_gt_1p15=bool(Wc / max(Wsg, 1.0e-12) > 1.15),
                  d_telescoping_lt_1e7=bool(abs(led - dEm) < 1.0e-7), d_wall_logger_within_2pct=bool(abs(r_(-W("dE_wall"), Ewf + Ews) - 1.0) < 0.02),
                  d_grav_proj_le_2pct=bool(W("dE_grav_proj") <= 0.02 * (-dEm)), d_G2P_coll_le_2pct=bool(W("dE_G2P_coll") <= 0.02 * (-dEm)))
        tab["telescoping_abs_J"] = abs(led - dEm); tab["wall_logger_ratio"] = r_(-W("dE_wall"), Ewf + Ews)
        dump(f"slosh_audit_{SUB}_summary.json", dict(sub=SUB, dx=DXA, steps=len(rows) - 1, window_requested=[ta, tb], table=tab, pass_marks=pm))
        say(f"slosh window: {json.dumps(tab)}"); say(f"slosh marks: {json.dumps(pm)}")
    except Exception as ex:
        say(f"slosh summary FAILED: {ex!r}"); traceback.print_exc()
say("all done")
```

## Pass marks, fixed now (coordinator), each reachable by construction
- ident (fix off): every state array equal to 5acb718 bit for bit. Reachable: with the flags off, no operation changes.
- rot (fix on): max_s_rot < 0.05 tau_y (0.27 Pa) and E_plastic_rot == 0. Reachable: the HW increment is orthogonal for C = W, so be = I
  stays I up to float32 rounding (s of order G x 1e-6 = 2e-4 Pa), below yield, so no plastic work.
- adjoint (fix on, 3 mm slosh, window 0.2-1.0 s): abs(W_constit / W_stress_grid - 1) < 0.10. Reachable: W_stress_grid = dt sum V tau^n :
  C(u_k) exactly; W_constit differs only by second-order terms (backward Euler undercounts by G (gp dt)^2 / 2, measured 1.1 % in the
  slab; tau within the step vs tau^n; U_el is small, 0.015 mJ).
- report raw (no mark): sinks / (-dE_mech), sinks / (-dE_tot), E_num, the ledger, f_d and zeta at 3 mm, fix on vs off.
(The audit's E_drop and the cell shadow still read s["C"]; with the fix on they are diagnostics of the old kinematics, ignore them.)

## Do
0. Ack. 1. Paste blocks 1-4 exactly; if any old text is not where these blocks say, stop and report what differs. 2. Commit, push.
3. Report in 0007-report.md: the commit hash, what went where, nothing else. Then wait; the coordinator launches the test.
