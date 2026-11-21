"""Step 4, tests 4.1-4.3 (21 Nov 2026, notes/spill/STATE-projection-fix.md; instruction section 6, B.5): the head of foam as an
elasto-viscoplastic solid, alone, in a periodic slab 8 x 8 x 24 cells (dx = 1.5 mm) on a no-slip floor, gravity tilted by alpha.
Kaggle CPU only; nothing runs outside Kaggle. Run from the repository's root:  python3 tools/spill/step4_slab.py OUTDIR
(env SUBRUN = "smoke" (20 steps per test) or "full"; ONLY e.g. "4.1,4.3").

What is the same code as the pint's (stout_jax.py): the return map evp_return_map, the stress evp_tau, the constants G_HEAD, TAU_Y,
EVP_A1, EVP_A2, RHO_HEAD, the staggered (MAC) trilinear weights and the APIC transfers of Stout.p2g / Stout.g2p, written here with
periodic x and y. What is the slab's own: a laterally uniform slab on a floor moves only along x, u = u(z, t); incompressibility then
gives w = 0 exactly (dw/dz = 0 with w(0) = 0) and the pressure exactly carries the normal part of gravity, rho g cos(alpha). So the
slab solves the x and y momentum with the tangential gravity g sin(alpha) and the foam's stress, and holds w = 0: the pressure step and
the variable density are not tested here (they are in 4.4 and 4.5). No-slip floor at z = 0: a layer of faces lies on the floor and holds u = 0 with those
below it (standard MPM sticky wall). The top (z = h) is free: no grid mass above it, so the stress force there is the traction-free one of the particles.

Exact references (computed below, and checked against the instruction's numbers): shear wave speed c_s = sqrt(G / rho_h), period of
the first mode T1 = 4 h / c_s; static top displacement u_s = tau_b h / (2 G) (tau(z) = tau_b (1 - z/h), strain tau / G); plug flow
above yield: tau(z) - tau_y = tau_v(gdot(z)) below z_y = h (1 - tau_y / tau_b), v(h) = integral of gdot from 0 to z_y."""
import json, math, os, sys, time, datetime, traceback
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import stout_jax as SJ  # noqa: E402
F32 = jnp.float32
SUB = os.environ.get("SUBRUN", "smoke"); ONLY = os.environ.get("ONLY")
RAMP = os.environ.get("RAMP", "linear")   # 4.2's load ramp: "linear" over 0.25 s (v2), or "cos": half-cosine over a whole number of T1 (v3)
DXE = float(os.environ.get("DX", "0.0015"))
TAG = "" if DXE == 0.0015 else f"_dx{DXE * 1e3:g}mm"          # file-name tag for other grids
VOUT = os.path.join(OUT, "step4"); os.makedirs(VOUT, exist_ok=True)
T0 = time.time()


def say(m):
    line = f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}"
    print(line, flush=True); open(os.path.join(VOUT, f"progress_{SUB}.log"), "a").write(line + "\n")


# ---------------------------------------------------------------- parameters (SI), every one named
DX = DXE; NX = NY = 8; NZ = int(round(24 * 0.0015 / DX)); Z0 = -2.5 * DX   # faces of layer k = 2 lie exactly on the floor (z = 0)
H = 0.019                                                    # m, head thickness (HEAD0)
G = SJ.G_HEAD; TAU_Y = SJ.TAU_Y; A1, A2 = SJ.EVP_A1, SJ.EVP_A2; RHO_H = SJ.RHO_HEAD; GRAV = 9.81
CS = math.sqrt(G / RHO_H); DT_EL = 0.40 * DX / CS; DT_MAX = 2e-3
PPC = 2; SEED = 1
M_FLOOR = 0.05 * RHO_H * DX ** 3                            # kg: the deviatoric force divides by max(M_f, M_FLOOR) (instruction B.3.5)
LX, LY = NX * DX, NY * DX


def tau_v(g):
    return A1 * g ** 0.47 + A2 * g ** 0.70


def plug_reference(tau_b, n=4001):
    """v(h) and the profile of the exact steady flow: below z_y, tau_v(gdot) = tau_b (1 - z/h) - tau_y (bisection), above it a plug."""
    zy = H * (1.0 - TAU_Y / tau_b); z = np.linspace(0.0, zy, n); rhs = tau_b * (1.0 - z / H) - TAU_Y
    lo = np.zeros(n); hi = np.full(n, 1e3)
    for _ in range(200):
        mid = 0.5 * (lo + hi); big = tau_v(mid) > rhs; hi = np.where(big, mid, hi); lo = np.where(big, lo, mid)
    gd = 0.5 * (lo + hi); v = np.concatenate([[0.0], np.cumsum(0.5 * (gd[1:] + gd[:-1]) * np.diff(z))])
    return dict(z_y=zy, v_h=float(v[-1]), z=z, v=v)


def seed():
    """The head on the pint's lattice: PPC^2 points per cell across (spacing h_l = dx / PPC), layers every hz = H / round(H / h_l) from
    0 to H, jittered sideways by at most 0.3 h_l and in height by at most 0.3 hz (as stout_jax.seed_particles)."""
    rng = np.random.default_rng(SEED); hl = DX / PPC; nzl = int(round(H / hl)); hz = H / nzl
    xs = hl * (np.arange(NX * PPC) + 0.5); X, Y = np.meshgrid(xs, xs, indexing="ij")
    P = np.concatenate([np.stack([X.ravel(), Y.ravel(), np.full(X.size, z)], 1) for z in hz * (np.arange(nzl) + 0.5)])
    P[:, :2] += rng.uniform(-0.3 * hl, 0.3 * hl, (len(P), 2)); P[:, 2] += rng.uniform(-0.3 * hz, 0.3 * hz, len(P))
    return P.astype(np.float32), hz, nzl


P0, HZ, NZL = seed(); NP = len(P0); VP = LX * LY * H / NP; MP = RHO_H * VP
CORN = jnp.asarray(np.array([(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)], np.int32))
ORG = jnp.asarray([0.0, 0.0, Z0], F32)


def corners(X, comp):
    """Stout._corners with periodic x, y: (8, N) flat index into a (NX, NY, NZ) face array, valid mask, weights, weight gradients
    (8, N, 3) in 1/m, and the offsets (corner - position) in m. comp 0: u faces (x = i dx), comp 1: v faces (y = j dx)."""
    g = (X - ORG) / DX; off = jnp.full(3, 0.5, F32).at[comp].set(0.0)
    gg = g - off; base = jnp.floor(gg).astype(jnp.int32); fr = gg - base
    node = base[None] + CORN[:, None, :]; cf = CORN.astype(F32)[:, None, :]
    wv = jnp.where(cf > 0, fr[None], 1 - fr[None]); w = wv[..., 0] * wv[..., 1] * wv[..., 2]
    sg = 2.0 * cf - 1.0
    gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1) / DX
    ix = jnp.mod(node[..., 0], NX); iy = jnp.mod(node[..., 1], NY); iz = node[..., 2]
    ok = (iz >= 0) & (iz < NZ); fl = jnp.where(ok, (ix * NY + iy) * NZ + iz, 0)
    return fl, ok, w, gw, (cf - fr[None]) * DX


def mirror_floor(f):
    """No-slip at z = 0 (v2, 21 Nov 14:06 UTC): the faces on the floor (k = 2, z = 0) and below it hold u = 0. v1 put the faces at
    z = -dx/2 and +dx/2 and mirrored them (u(-z) = -u(z)): the first face above the floor then took the wall's support from only half a
    cell of particles, so the bottom layer carried twice the stress (full run v1: s_max 8.5 Pa against 2 tau_b = 4.33 Pa in 4.1)."""
    return f.at[:, :, :3].set(0.0)


def step(st, dt, gx):
    X, V, C, be = st["x"], st["v"], st["C"], st["be"]
    tau = SJ.sym_unpack(SJ.evp_tau(be, G))                                           # (N, 3, 3) Kirchhoff stress
    size = NX * NY * NZ; vel = []
    for comp in (0, 1):
        fl, ok, w, gw, dpos = corners(X, comp)
        mom = w * MP * (V[None, :, comp] + jnp.sum(C[None, :, comp, :] * dpos, -1))
        fdev = -VP * jnp.sum(tau[None, :, comp, :] * gw, -1)                       # -sum V_p tau_{comp, a} d w / d x_a
        upd = jnp.stack([jnp.where(ok, mom, 0.0), jnp.where(ok, w * MP, 0.0), jnp.where(ok, w, 0.0), jnp.where(ok, fdev, 0.0)], -1).reshape(-1, 4)
        acc = jnp.zeros((size, 4), F32).at[fl.reshape(-1)].add(upd).reshape(NX, NY, NZ, 4)
        m = acc[..., 1]; occ = acc[..., 2] > 1e-6                                     # occupancy by the sum of weights, never by mass
        gc = gx if comp == 0 else 0.0
        u = jnp.where(occ, acc[..., 0] / jnp.where(occ, m, 1.0) + dt * gc + dt * acc[..., 3] / jnp.maximum(m, M_FLOOR), 0.0)
        vel.append(mirror_floor(u))
    vs, Cs = [], []
    for comp in (0, 1):
        fl, ok, w, gw, _ = corners(X, comp)
        val = jnp.where(ok, vel[comp].reshape(-1)[fl], 0.0)
        vs.append(jnp.sum(w * val, 0)); Cs.append(jnp.sum(val[..., None] * gw, 0))
    Vn = jnp.stack([vs[0], vs[1], jnp.zeros_like(vs[0])], -1)
    Cn = jnp.stack([Cs[0], Cs[1], jnp.zeros_like(Cs[0])], 1)                            # w = 0: no third row
    Xn = X + dt * Vn; Xn = Xn.at[:, 0].set(jnp.mod(Xn[:, 0], LX)).at[:, 1].set(jnp.mod(Xn[:, 1], LY))
    ben, y, gp, s_new, det, res = SJ.evp_return_map(be, Cn, dt, G, TAU_Y, A1, A2)
    st = dict(x=Xn.astype(F32), v=Vn.astype(F32), C=Cn.astype(F32), be=ben, disp=st["disp"] + dt * Vn[:, 0])
    diag = dict(n_yielded=jnp.sum(y), gp_max=jnp.max(gp), s_max=jnp.max(s_new), det_dev=jnp.max(jnp.abs(det - 1.0)), res_max=jnp.max(res),
                vmax=jnp.max(jnp.abs(Vn)))
    return st, diag


step_j = jax.jit(step)
ZP = jnp.asarray(P0[:, 2])
TOP = jnp.asarray(P0[:, 2] > H - HZ)                                                    # the top layer of particles
LAYER = jnp.asarray(np.clip((P0[:, 2] / HZ).astype(int), 0, NZL - 1))


def obs(st):
    d = st["disp"]; v = st["v"][:, 0]
    lay_u = jnp.zeros(NZL).at[LAYER].add(d) / jnp.zeros(NZL).at[LAYER].add(1.0)
    lay_v = jnp.zeros(NZL).at[LAYER].add(v) / jnp.zeros(NZL).at[LAYER].add(1.0)
    return dict(u_top=jnp.mean(jnp.where(TOP, d, 0.0)) * NP / jnp.sum(TOP), v_top=jnp.mean(jnp.where(TOP, v, 0.0)) * NP / jnp.sum(TOP), lay_u=lay_u, lay_v=lay_v)


obs_j = jax.jit(obs)


def run(label, frac, T, ramp, ramp_kind="linear"):
    tau_b = frac * TAU_Y; alpha = math.asin(tau_b / (RHO_H * GRAV * H)); gx_full = GRAV * math.sin(alpha)
    st = dict(x=jnp.asarray(P0), v=jnp.zeros((NP, 3), F32), C=jnp.zeros((NP, 3, 3), F32),
              be=jnp.tile(jnp.asarray([1, 1, 1, 0, 0, 0], F32), (NP, 1)), disp=jnp.zeros(NP, F32))
    say(f"{label}: tau_b {tau_b:.4f} Pa = {frac} tau_y, alpha {math.degrees(alpha):.4f} deg, g_x {gx_full:.5f} m/s^2, ramp {ramp} s, T {T} s, "
        f"N {NP}, layers {NZL} (hz {HZ * 1e3:.3f} mm), dt_el {DT_EL:.4e} s")
    fh = open(os.path.join(VOUT, f"slab_{label}{TAG}_{SUB}.jsonl"), "w")
    t = 0.0; k = 0; ts, ut, vt, rows = [], [], [], []; agg = dict(n_yielded_max=0, det_dev_max=0.0, res_max=0.0, gp_max=0.0, s_max=0.0, vmax=0.0)
    nmax = 20 if SUB == "smoke" else 10 ** 9; prof = []
    while t < T - 1e-12 and k < nmax:
        vmax = agg["vmax"] if k else 0.0
        dt = min(DT_MAX, DT_EL, 0.8 * DX / max(vmax, 1e-12), T - t)
        if ramp <= 0: ramp_f = 1.0
        elif ramp_kind == "cos": ramp_f = 0.5 * (1.0 - math.cos(math.pi * min(1.0, (t + dt) / ramp)))
        else: ramp_f = min(1.0, (t + dt) / ramp)
        st, d = step_j(st, dt, gx_full * ramp_f); t += dt; k += 1
        d = {kk: float(v) for kk, v in d.items()}; o = obs_j(st)
        agg["n_yielded_max"] = max(agg["n_yielded_max"], int(d["n_yielded"])); agg["vmax"] = d["vmax"]
        for kk in ("det_dev", "res_max", "gp_max", "s_max"):
            key = kk if kk.endswith("_max") else kk + "_max"; agg[key] = max(agg[key], d[kk])
        ts.append(t); ut.append(float(o["u_top"])); vt.append(float(o["v_top"]))
        if k % 10 == 0 or k < 3:
            row = dict(step=k, t=t, dt=dt, gx=gx_full * ramp_f, u_top=ut[-1], v_top=vt[-1], **d); fh.write(json.dumps(row) + "\n"); fh.flush()
        if k % 100 == 0 or (label == "4.3" and t > 0.4 - 1e-9):
            prof.append(dict(t=t, u=np.asarray(o["lay_u"]).tolist(), v=np.asarray(o["lay_v"]).tolist()))
        if k % 500 == 0: say(f"{label}: step {k}  t {t:.4f}  u_top {ut[-1]:.4e} m  v_top {vt[-1]:.4e} m/s  yielded {int(d['n_yielded'])}  det_dev {d['det_dev']:.2e}")
    fh.close()
    ts, ut, vt = np.array(ts), np.array(ut), np.array(vt)
    out = dict(label=label, sub=SUB, steps=k, t_end=t, tau_b_pa=tau_b, frac=frac, alpha_deg=math.degrees(alpha), g_x=gx_full, ramp_s=ramp, N=NP,
               layers=NZL, hz_m=HZ, dt_rule="dt = min(2e-3, 0.8 dx / vmax, 0.40 dx / c_s)", dt_el=DT_EL, c_s=CS, G=G, tau_y=TAU_Y, A1=A1, A2=A2,
               rho_h=RHO_H, tau_v_10=tau_v(10.0), **agg)
    np.savez(os.path.join(VOUT, f"slab_{label}{TAG}_{SUB}_series.npz"), t=ts, u_top=ut, v_top=vt)
    json.dump(prof, open(os.path.join(VOUT, f"slab_{label}{TAG}_{SUB}_profiles.json"), "w"))
    return out, ts, ut, vt, prof


def fit_period(t, u, T1):
    from scipy.optimize import curve_fit
    fun = lambda t, A, w, ph, c: A * np.cos(w * t + ph) + c
    best = None
    for ph in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        try:
            p, _ = curve_fit(fun, t, u, p0=[0.5 * np.ptp(u), 2 * np.pi / T1, ph, u.mean()], maxfev=20000)
            r = np.sum((fun(t, *p) - u) ** 2)
            if best is None or r < best[1]: best = (p, r)
        except Exception:
            pass
    A, w, ph, c = best[0]; T = 2 * np.pi / abs(w)
    up = np.nonzero((u[:-1] - c < 0) & (u[1:] - c >= 0))[0]                                  # up-crossings of the fitted mean
    tz = t[up] - (u[up] - c) / (u[up + 1] - u[up]) * (t[up + 1] - t[up])
    return dict(T_fit=float(T), A_fit=float(abs(A)), c_fit=float(c), rms=float(np.sqrt(best[1] / len(t))),
                T_upcross=float(np.mean(np.diff(tz))) if len(tz) > 1 else None, n_upcross=int(len(tz)))


results = {}
say(f"start {SUB}: device {jax.devices()[0]}, G {G:.3f} Pa, tau_y {TAU_Y:.4f} Pa, A1 {A1:.5f}, A2 {A2:.5f}, tau_v(10/s) {tau_v(10.0):.4f} Pa, "
    f"rho_h {RHO_H:.3f}, c_s {CS:.5f} m/s, T1 {4 * H / CS:.5e} s, dt_el {DT_EL:.4e} s")
T1 = 4 * H / CS

if not ONLY or "4.1" in ONLY:
    try:
        o, ts, ut, vt, _ = run("4.1", 0.4, 0.5, 0.0)
        us = o["tau_b_pa"] * H / (2 * G); o["u_static_ref"] = us; o["T1_ref"] = T1
        if SUB == "full":
            F = fit_period(ts, ut, T1); o["fit"] = F
            ncyc = int(ts[-1] // F["T_fit"]); m = ts <= ncyc * F["T_fit"]; trap = getattr(np, "trapezoid", None) or np.trapz; o["u_cycle_mean"] = float(trap(ut[m], ts[m]) / ts[m][-1]); o["n_cycles"] = ncyc
            o["pass_marks"] = dict(n_yielded_zero=o["n_yielded_max"] == 0, T1_within_5pct=bool(9.228e-2 <= F["T_fit"] <= 1.020e-1),
                                   u_mean_within_8pct=bool(1.137e-4 <= o["u_cycle_mean"] <= 1.335e-4), det_dev_lt_1e5=o["det_dev_max"] < 1e-5)
            o["pass_marks_all"] = all(o["pass_marks"].values())
        results["4.1"] = o; json.dump(o, open(os.path.join(VOUT, f"slab_4.1{TAG}_{SUB}_summary.json"), "w"), indent=1, default=str)
        say(f"4.1 done: {json.dumps(o, default=str)}")
    except Exception as ex:
        say(f"4.1 FAILED: {ex!r}"); traceback.print_exc()

if not ONLY or "4.2" in ONLY:
    try:
        if RAMP == "cos":   # v3 (owner, 21 Nov): half-cosine over n whole periods, n = ceil(0.25 s / T1) = 3; predicted ringing 1/(4 n^2 - 1) u_s
            n_rp = math.ceil(0.25 / T1); o, ts, ut, vt, _ = run("4.2", 0.7, 4.0, n_rp * T1, "cos")
            o["ramp_kind"] = "half-cosine"; o["ramp_periods"] = n_rp; o["ringing_predicted"] = o["tau_b_pa"] * H / (2 * G) / (4 * n_rp ** 2 - 1)
        else:
            o, ts, ut, vt, _ = run("4.2", 0.7, 4.0, 0.25); o["ramp_kind"] = "linear"
        us = o["tau_b_pa"] * H / (2 * G); o["u_static_ref"] = us
        if SUB == "full":
            u05 = float(np.interp(0.5, ts, ut)); u40 = float(ut[-1])
            o["u_h_0p5"] = u05; o["u_h_4p0"] = u40; o["creep"] = abs(u40 - u05)
            # supplementary (not a mark): means over whole periods T1 ending at 4.0 s and starting at 0.5 s; the predicted ringing
            # left by a linear ramp of 0.25 s in an undamped column is u_s |sin(w Tr / 2)| / (w Tr / 2) = 0.12 u_s
            m1 = ts >= 4.0 - 2 * T1; m0 = (ts >= 0.5) & (ts <= 0.5 + 2 * T1)
            o["u_mean_last_2T1"] = float(ut[m1].mean()); o["u_mean_from_0p5_2T1"] = float(ut[m0].mean()); o["creep_of_means"] = abs(o["u_mean_last_2T1"] - o["u_mean_from_0p5_2T1"])
            o["ringing_amp_after_0p5"] = float(0.5 * np.ptp(ut[ts >= 0.5]))
            o["pass_marks"] = dict(n_yielded_zero=o["n_yielded_max"] == 0, creep_lt_5e5=o["creep"] < 5e-5, u_4p0_within_10pct=bool(1.948e-4 <= u40 <= 2.380e-4))
            o["pass_marks_all"] = all(o["pass_marks"].values())
        results["4.2"] = o; json.dump(o, open(os.path.join(VOUT, f"slab_4.2{TAG}_{SUB}_summary.json"), "w"), indent=1, default=str)
        say(f"4.2 done: {json.dumps(o, default=str)}")
    except Exception as ex:
        say(f"4.2 FAILED: {ex!r}"); traceback.print_exc()

if not ONLY or "4.3" in ONLY:
    try:
        o, ts, ut, vt, prof = run("4.3", 1.5, 0.5, 0.0)
        ref = plug_reference(o["tau_b_pa"]); o["z_y_ref"] = ref["z_y"]; o["v_h_ref"] = ref["v_h"]
        if SUB == "full":
            m = ts >= 0.4; vh = float(vt[m].mean()); o["v_h_0p4_0p5"] = vh; o["v_h_std"] = float(vt[m].std())
            zl = HZ * (np.arange(NZL) + 0.5); late = [p for p in prof if p["t"] >= 0.4 - 1e-9]
            vprof = np.mean([p["v"] for p in late], 0); o["v_profile_z_m"] = zl.tolist(); o["v_profile"] = vprof.tolist()
            o["v_ref_profile"] = np.interp(zl, np.concatenate([ref["z"], [H]]), np.concatenate([ref["v"], [ref["v_h"]]])).tolist()
            vzy = float(np.interp(ref["z_y"] + DX, zl, vprof)); o["v_zy_plus_dx"] = vzy; o["uniformity"] = abs(vprof[-1] - vzy) / max(abs(vprof[-1]), 1e-30)
            o["pass_marks"] = dict(v_h_within_12pct=bool(1.247e-3 <= vh <= 1.587e-3), plug_uniform_lt_5pct=o["uniformity"] < 0.05)
            o["pass_marks_all"] = all(o["pass_marks"].values())
        results["4.3"] = o; json.dump(o, open(os.path.join(VOUT, f"slab_4.3{TAG}_{SUB}_summary.json"), "w"), indent=1, default=str)
        say(f"4.3 done: {json.dumps(o, default=str)}")
    except Exception as ex:
        say(f"4.3 FAILED: {ex!r}"); traceback.print_exc()

json.dump(results, open(os.path.join(VOUT, f"slab{TAG}_{SUB}_all.json"), "w"), indent=1, default=str)
say("all done")
