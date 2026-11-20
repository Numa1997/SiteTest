"""Fig. 16 spill, step 1 of notes/spill/DERIVATION-flight-inversion.md section 9: the flight as one exact linear map.
Kaggle CPU, read-only on the stored ride, seconds.   python3 flight_map.py OUTDIR      (dataset fig16-guinness-cart-control attached)

THE FLIGHT EQUATION (stout_jax.py:381-391, frame_accel). Glass frame, x along the cart, z up, origin on the glass's inner floor;
the frame turns about y through S = (0, 0, zS) at rate om (positive from e_x towards e_z, nose up), al = d(om)/dt. X = x, Z = z - zS:
    dvx/dt = gx + al Z + om^2 X + 2 om vz,     dvz/dt = gz - al X + om^2 Z - 2 om vx,     dvy/dt = 0
Linear in s = (X, Z, vx, vz):  ds/dt = A(t) s + b(t),  A = [[0,0,1,0],[0,0,0,1],[om^2, al, 0, 2 om],[-al, om^2, -2 om, 0]],  b = (0,0,gx,gz).
Homogeneous form: d/dt [s; 1] = M [s; 1], M = [[A, b], [0, 0]]. Its fundamental matrix Phi(t) (5 x 5, Phi(t_0) = 1) is
    Phi = [[Psi, Psi p], [0, 1]],   Psi' = A Psi,   p(t) = integral of Psi^-1 b,
so eq. (1) of the note, s(t) = Psi(t) [Psi(t0)^-1 s0 + p(t) - p(t0)], is  [s(t); 1] = Phi(t) Phi(t0)^-1 [s0; 1]: two matrix products.

THE FRAME FROM THE STORED CART, IMPULSE-EXACT (note section 3; derived from cart4.py:199-222, 253-256). The stored gx, gz are point
samples at 60 per second and miss part of the kerb's shock. What the flight needs over a picture interval is the integral of b.
cart4.py: the glass axes in the road frame are e_x' = (cos th, sin th), e_z' = (-sin th, cos th); S = c + hg (-sin th, cos th), c the
deck centre (x, zc), hg = 0.122 m (cart4.py:61); the effective gravity at S in glass axes is (cart4.py:220-221)
    b = R^T g_S,   g_S = -G0 e_z - a_S,   R^T u = (u . e_x', u . e_z').
Velocity of S in the road frame: v_S = (v - hg om cos th,  vzc - hg om sin th)  (from the stored v = dx/dt, vzc, om, th).
Let w = R^T v_S. Because d e_x'/dt = om e_z' and d e_z'/dt = -om e_x':
    dw/dt = R^T a_S + om (w_z, -w_x)   =>   integral of R^T a_S dt = Delta w - integral of om (w_z, -w_x) dt.
Hence, exactly, over an interval [t_k, t_k+1]:
    I_k = integral of b dt = -G0 integral of (sin th, cos th) dt  -  Delta w  +  integral of om (w_z, -w_x) dt.
Delta w uses the stored states at the two pictures (exact, the shock included); the two remaining integrals have smooth integrands
(th continuous; om w at most a jump at the kerb) and are taken by the trapezoid rule. In the interval b is then the constant
I_k / dt_k. The pitch the same way: om(t) linear between the stored om, al_k = Delta om / dt_k (the rotation's impulse exact).
Stated (A2 of the note): inside one interval the shock's shape is not known; constant b moves a piece of liquid by at most
|Delta b| dt^2 / 8 against the true shape, reported below.

CHECKS (pass marks fixed here, before the run):
 C1  det Psi = 1 at every step: |det Psi - 1| < 1e-9 (tr A = 0, Liouville). RK4, step chosen so that ||A|| h <= 0.01.
 C2  om = 0, al = 0, b = const: (1) equals the parabola s0 + v0 t + b t^2 / 2; largest error < 1e-10 m, from t0 = 0.1 s to 0.4 s.
 C3  om = 5 rad/s const, al = 0, b = 0: (1) equals the inertial straight line seen from the turning frame,
     X(t) = r_I(t) . e_x'(om t), Z(t) = r_I(t) . e_z'(om t), r_I(t) = r_I0 + v_I0 t, v_I0 = vx e_x' + vz e_z' + om (X e_z' - Z e_x');
     largest error < 1e-9 m over 0.4 s. This fixes the sign convention against cart4.py's axes.
 C4  A s + b equals the stored solver's frame_accel (copied from stout_jax.py:381-391) for 1000 random states and frames: < 1e-12.
REPORTED, NO MARK: b (impulse-exact) against the stored gx, gz samples (rms, near the kerb), al_k against the stored al, Delta th against
the trapezoid of om, the position error bound |Delta b| dt^2/8, and (assumption A4) the mass of listed markers above the grid's top
inside the rim's radius (liquid that left through the top, not over the rim).
OUTPUT: flight_map.npz (t_pic, t_sub, Phi_sub (n, 5, 5), Phi_pic, b_int (I_k / dt_k), om, al_k, k_of_sub), REPORT.md, report.json,
rewritten after every block; a failing block is recorded and the next still runs."""
import glob, json, os, sys, time, traceback, urllib.request
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"; RIDE = os.environ.get("RIDE", "kerb_off")
G0, HG, FLOOR = 9.81, 0.122, 0.030; ZS = HG - FLOOR; DX = 0.0015; DZP = 0.0005          # cart4.py:53, :61, :76; run16.py:21
MD, REP, ERR = [], {}, []; T0 = time.time()


def say(s=""):
    print(s, flush=True); MD.append(s)


def flush():
    rep = dict(REP, errors=ERR)
    md = MD + (["\n## Block failures\n"] + [f"- `{e['block']}`: {e['error']}" for e in ERR] if ERR else [])
    open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(md) + "\n")
    json.dump(rep, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=lambda o: float(o) if np.ndim(o) == 0 else np.asarray(o).tolist())


def block(name, fn):
    t_ = time.time()
    try:
        fn(); print(f"[block {name}: done in {time.time() - t_:.2f} s]", flush=True)
    except Exception as e:
        ERR.append(dict(block=name, error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()))
        print(f"[block {name}: FAILED]\n{traceback.format_exc()}", flush=True)
    flush()


def M5(om, al, b):
    """The 5 x 5 generator [[A, b], [0, 0]]."""
    M = np.zeros((5, 5)); M[0, 2] = M[1, 3] = 1.0
    M[2, 0] = om * om; M[2, 1] = al; M[2, 3] = 2 * om; M[3, 0] = -al; M[3, 1] = om * om; M[3, 2] = -2 * om; M[2, 4], M[3, 4] = b
    return M


def propagate(tk, om_k, al_k, b_k, hmax=None, eps=0.01):
    """Phi on [tk[0], tk[-1]], RK4. In interval k: om(t) = om_k[k] + al_k[k] (t - tk[k]), al = al_k[k], b = b_k[k] (constant).
    Step: h <= eps / ||A|| (row-sum bound 1 + om^2 + |al| + 2|om|). Returns step times, Phi at each, and the interval of each."""
    Phi = np.eye(5); ts, Ps, ks = [tk[0]], [Phi.copy()], [0]
    for k in range(len(tk) - 1):
        d = tk[k + 1] - tk[k]; om_hi = max(abs(om_k[k]), abs(om_k[k] + al_k[k] * d))
        n = max(8, int(np.ceil(d * (1 + om_hi ** 2 + abs(al_k[k]) + 2 * om_hi) / eps)))
        if hmax: n = max(n, int(np.ceil(d / hmax)))
        h = d / n; f = lambda s_: M5(om_k[k] + al_k[k] * s_, al_k[k], b_k[k])
        for i in range(n):
            s_ = i * h; m1 = f(s_); m2 = f(s_ + h / 2); m4 = f(s_ + h)
            k1 = m1 @ Phi; k2 = m2 @ (Phi + h / 2 * k1); k3 = m2 @ (Phi + h / 2 * k2); k4 = m4 @ (Phi + h * k3)
            Phi = Phi + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); ts.append(tk[k] + s_ + h); Ps.append(Phi.copy()); ks.append(k)
    return np.array(ts), np.array(Ps), np.array(ks)


def carry(Pt, Pt0, s0):
    """Eq. (1): [s; 1] = Phi(t) Phi(t0)^-1 [s0; 1], for one or many states s0 (..., 4)."""
    S0 = np.concatenate([s0, np.ones(s0.shape[:-1] + (1,))], -1)
    return (Pt @ np.linalg.solve(Pt0, S0.T)).T[..., :4] if S0.ndim == 2 else (Pt @ np.linalg.solve(Pt0, S0))[:4]


D = {}


def load():
    Z = np.load(glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)[0])
    need = ("t", "v", "vzc", "om", "th", "gx", "gz")
    miss = [k for k in need if k not in Z.files]
    if miss: raise KeyError(f"stored ride lacks {miss}; has {sorted(Z.files)}")
    for k in need + tuple(k for k in ("al", "drops", "ndrops", "nfly", "mp") if k in Z.files): D[k] = np.asarray(Z[k])
    say(f"# Fig. 16, ride `{RIDE}`: the flight map (step 1 of DERIVATION-flight-inversion.md)\n")
    say(f"Stored ride: {len(D['t'])} pictures, t = {D['t'][0]:.4f} to {D['t'][-1]:.4f} s; keys used: {', '.join(sorted(D))}.")


def frame():
    t = D["t"].astype(float); v, vzc, om, th = (D[k].astype(float) for k in ("v", "vzc", "om", "th")); dt = np.diff(t)
    eX = np.stack([np.cos(th), np.sin(th)], 1); eZ = np.stack([-np.sin(th), np.cos(th)], 1)
    vS = np.stack([v - HG * om * np.cos(th), vzc - HG * om * np.sin(th)], 1)
    w = np.stack([(vS * eX).sum(1), (vS * eZ).sum(1)], 1)
    grav = -G0 * np.stack([np.sin(th), np.cos(th)], 1); rotw = om[:, None] * np.stack([w[:, 1], -w[:, 0]], 1)
    trap = lambda q: 0.5 * (q[1:] + q[:-1]) * dt[:, None]
    I = trap(grav) - np.diff(w, axis=0) + trap(rotw); b = I / dt[:, None]
    al_k = np.diff(om) / dt
    D.update(t=t, b=b, al_k=al_k, omf=om, dt=dt)
    gs = 0.5 * np.stack([D["gx"][1:] + D["gx"][:-1], D["gz"][1:] + D["gz"][:-1]], 1).astype(float); dif = b - gs
    kk = int(np.argmax(np.abs(np.diff(om)))); tk = t[kk]; near = np.abs(t[:-1] - tk) <= 0.1
    jump = np.r_[0.0, np.linalg.norm(np.diff(b, axis=0), axis=1)]; bound = jump * dt ** 2 / 8
    REP["frame"] = dict(kerb_interval=kk, kerb_t=float(tk), rms_b_minus_sampled=float(np.sqrt((dif ** 2).sum(1).mean())),
                        rms_near_kerb=float(np.sqrt((dif[near] ** 2).sum(1).mean())), max_b_minus_sampled=float(np.linalg.norm(dif, axis=1).max()),
                        max_position_bound_mm=float(bound.max() * 1e3), max_al_k=float(np.abs(al_k).max()))
    if "al" in D:
        ad = al_k - 0.5 * (D["al"][1:] + D["al"][:-1]); REP["frame"]["rms_al_k_minus_sampled"] = float(np.sqrt(np.mean(ad ** 2)))
    dth = np.diff(D["th"].astype(float)) - 0.5 * (om[1:] + om[:-1]) * dt; REP["frame"]["max_dtheta_minus_trapezoid_rad"] = float(np.abs(dth).max())
    f = REP["frame"]
    say("\n## The frame, impulse-exact (no pass mark)\n")
    say(f"b from the cart state against the stored gx, gz (interval means): rms {f['rms_b_minus_sampled']:.3f} m/s^2, within 0.1 s of the kerb "
        f"(t = {tk:.3f} s) {f['rms_near_kerb']:.3f} m/s^2, largest {f['max_b_minus_sampled']:.3f} m/s^2. Largest al_k {f['max_al_k']:.1f} rad/s^2"
        + (f"; rms al_k - stored al {f['rms_al_k_minus_sampled']:.2f} rad/s^2" if "rms_al_k_minus_sampled" in f else "")
        + f". Delta th - trapezoid of om: largest {f['max_dtheta_minus_trapezoid_rad']:.2e} rad. Position error bound of constant b in an "
        f"interval, |Delta b| dt^2/8: largest {f['max_position_bound_mm']:.2f} mm.")


def fmap():
    ts, Ps, ks = propagate(D["t"], D["omf"][:-1], D["al_k"], D["b"])
    pic = np.r_[0, np.where(np.diff(ks) != 0)[0], len(ts) - 1]      # last step of each interval = the next picture
    det = np.linalg.det(Ps[:, :4, :4]); e1 = float(np.abs(det - 1).max())
    D.update(ts=ts, Ps=Ps, ks=ks, pic=pic)
    REP["C1"] = dict(max_abs_det_minus_1=e1, steps=len(ts), PASS=e1 < 1e-9)
    say("\n## Checks (marks fixed before the run)\n")
    say(f"C1. det Psi = 1 (Liouville, tr A = 0): largest |det Psi - 1| = {e1:.2e} over {len(ts)} RK4 steps (mark 1e-9): **{'PASS' if e1 < 1e-9 else 'FAIL'}**")
    np.savez_compressed(os.path.join(OUT, "flight_map.npz"), t_pic=D["t"], t_sub=ts, Phi_sub=Ps, Phi_pic=Ps[pic], k_of_sub=ks, b_int=D["b"],
                        om=D["omf"], al_k=D["al_k"], zS=ZS, hg=HG)


def c2():
    tk = np.linspace(0.0, 0.4, 25); n = len(tk) - 1; bc = np.array([1.3, -9.81])
    ts, Ps, _ = propagate(tk, np.zeros(n), np.zeros(n), np.tile(bc, (n, 1)))
    rng = np.random.default_rng(2); s0 = rng.normal(0, [0.05, 0.05, 0.5, 0.5], (50, 4)); i0 = int(np.argmin(np.abs(ts - 0.1))); err = 0.0
    for i in range(i0, len(ts), 7):
        T = ts[i] - ts[i0]; s = carry(Ps[i], Ps[i0], s0)
        ex = s0[:, :2] + s0[:, 2:] * T + 0.5 * bc * T * T; err = max(err, float(np.abs(s[:, :2] - ex).max()))
    REP["C2"] = dict(max_err_m=err, PASS=err < 1e-10)
    say(f"C2. om = 0, constant b: eq. (1) against the parabola, t0 = {ts[i0]:.3f} s to 0.4 s, 50 states: largest error {err:.2e} m (mark 1e-10): **{'PASS' if err < 1e-10 else 'FAIL'}**")


def c3():
    W = 5.0; tk = np.linspace(0.0, 0.4, 25); n = len(tk) - 1
    ts, Ps, _ = propagate(tk, np.full(n, W), np.zeros(n), np.zeros((n, 2)))
    rng = np.random.default_rng(3); s0 = rng.normal(0, [0.05, 0.05, 0.5, 0.5], (50, 4)); err = 0.0
    X0, Z0, vx, vz = s0.T
    rI0 = np.stack([X0, Z0], 1)                                           # at t = 0 the axes are e_x' = (1, 0), e_z' = (0, 1)
    vI0 = np.stack([vx - W * Z0, vz + W * X0], 1)                         # vx e_x' + vz e_z' + om (X e_z' - Z e_x')
    for i in range(0, len(ts), 5):
        T = ts[i]; rI = rI0 + vI0 * T; ex_ = np.array([np.cos(W * T), np.sin(W * T)]); ez_ = np.array([-np.sin(W * T), np.cos(W * T)])
        s = carry(Ps[i], Ps[0], s0); err = max(err, float(np.abs(s[:, 0] - rI @ ex_).max()), float(np.abs(s[:, 1] - rI @ ez_).max()))
    REP["C3"] = dict(max_err_m=err, PASS=err < 1e-9)
    say(f"C3. om = {W} rad/s, b = 0: eq. (1) against the inertial straight line seen from the turning frame, 0.4 s, 50 states: largest error {err:.2e} m (mark 1e-9): **{'PASS' if err < 1e-9 else 'FAIL'}**")


def c4():
    def frame_accel(x, z, vx, vz, gx, gz, rot):                           # stout_jax.py:381-391, verbatim in numpy
        om, al, zS = rot; Z = z - zS
        return gx + al * Z + om * om * x + 2.0 * om * vz, gz - al * x + om * om * Z - 2.0 * om * vx
    rng = np.random.default_rng(4); err = 0.0
    for _ in range(1000):
        x, z, vx, vz = rng.normal(0, [0.1, 0.1, 1, 1]); om, al = rng.normal(0, [6, 300]); gx, gz = rng.normal(0, 15, 2)
        a = M5(om, al, (gx, gz)) @ np.array([x, z - ZS, vx, vz, 1.0]); f = frame_accel(x, z, vx, vz, gx, gz, (om, al, ZS))
        err = max(err, abs(a[2] - f[0]), abs(a[3] - f[1]))
    REP["C4"] = dict(max_err=float(err), PASS=err < 1e-12)
    say(f"C4. A s + b against the stored solver's frame_accel, 1000 random states and frames: largest difference {err:.2e} m/s^2 (mark 1e-12): **{'PASS' if err < 1e-12 else 'FAIL'}**")


def a4():
    if "drops" not in D: raise KeyError("no drops in the stored ride")
    js = urllib.request.urlopen("https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js", timeout=30).read().decode()
    Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); zrim = (len(Rp) - 1) * DZP; Rrim = float(Rp[-1])
    nz = int(np.ceil((zrim + 0.02) / DX)) + 2; ztop = -2 * DX + (nz - 1) * DX           # stout_jax.py:106-107 (Fig. 12 grid, body None)
    mp = float(D["mp"]); mass = []
    for k in range(len(D["drops"])):
        X = D["drops"][k].astype(float); X = X[np.isfinite(X).all(1)]
        w = float(D["ndrops"][k]) / max(len(X), 1) * mp; r = np.hypot(X[:, 0], X[:, 1])
        mass.append(float(((X[:, 2] >= ztop) & (r < Rrim)).sum() * w))
    mass = np.array(mass); km = int(np.argmax(mass))
    REP["A4"] = dict(zrim_m=zrim, Rrim_m=Rrim, grid_top_m=ztop, max_mass_g=float(mass[km] * 1e3), at_picture=km,
                     share_of_air_at_that_picture=float(mass[km] / max(float(D["nfly"][km]) * mp, 1e-30)) if "nfly" in D else None)
    a = REP["A4"]
    say(f"\nA4 (no mark): listed markers above the grid's top (z >= {ztop * 1e3:.1f} mm; rim at {zrim * 1e3:.1f} mm, radius {Rrim * 1e3:.1f} mm) "
        f"inside the rim's radius: largest {a['max_mass_g']:.3f} g at picture {km}"
        + (f", {100 * a['share_of_air_at_that_picture']:.2f} % of the liquid in the air then." if a["share_of_air_at_that_picture"] is not None else "."))


if __name__ == "__main__":                        # run as a script: every block; imported (source_twin.py): functions only
    for name, fn in (("load", load), ("frame", frame), ("flight_map_C1", fmap), ("C2_parabola", c2), ("C3_rotation", c3), ("C4_frame_accel", c4), ("A4_top", a4)):
        block(name, fn)
    say(f"\nWall time {time.time() - T0:.1f} s on Kaggle CPU."); flush()
    sys.exit(1 if ERR else 0)
