"""Fig. 2, the double pendulum, computed once on Kaggle's GPU: every start the page's sliders can reach on a grid, with its chaos twin.

The setup. A massless rigid rod of length l1 hangs from a fixed pivot and carries a point mass m1; a second rod of length l2 hangs
from that mass and carries a point mass m2. Both swing in one vertical plane, without friction or air; gravity g points down.
theta1, theta2 (rad) are the rods' angles from the downward vertical, counter-clockwise positive; omega1, omega2 (rad/s) their
rates. With delta = theta1 - theta2, Lagrange's equations give the angular accelerations (the page's lecture note, equation (9)):

    D      = 2 m1 + m2 - m2 cos(2 delta)                                                            [kg]
    alpha1 = [-g (2 m1 + m2) sin theta1 - m2 g sin(theta1 - 2 theta2)
              - 2 sin(delta) m2 (omega2^2 l2 + omega1^2 l1 cos delta)] / (l1 D)                      [rad/s^2]
    alpha2 = 2 sin(delta) [omega1^2 l1 (m1 + m2) + g (m1 + m2) cos theta1 + omega2^2 l2 m2 cos delta] / (l2 D)

and the energy E = 1/2 (m1+m2) l1^2 omega1^2 + 1/2 m2 l2^2 omega2^2 + m2 l1 l2 omega1 omega2 cos(delta)
                   - (m1+m2) g l1 cos theta1 - m2 g l2 cos theta2 stays constant.

Method: exactly the page's own, so the stored motion is the motion the live page computes. Fourth-order Runge-Kutta with the
fixed step H = 1/600 s, in 64-bit numbers, the same formulas in the same order as deriv() and rk4() of
public/simulations/Double Pendulum.html (main branch, 23 November 2026). All starts of one mass-length cell are advanced
together on the GPU (JAX, jit, lax.scan); the state is recorded every 5 steps (120 times a second).

The grid (every slider of the page keeps its range):
    ln(m2/m1) in LN_M (5 values, the mass slider's ends, middle and quarter points), ln(l2/l1) in LN_L (5 values),
    theta1, theta2 every 15 degrees (24 values each), omega1, omega2 in W0 (5 values each): 5*5*24*24*5*5 = 360 000 starts,
    each with its twin, started with theta1 + EPS. Nothing is random: the sliders pick the start, so no seed is needed.

Output, in out_dir (this module is the engine behind tools/sims/double_pendulum.py; the engine's registry stores the packs in a
GitHub release and commits the rest, docs/kaggle-sims.md "Large data"):
    dp_<i><j>.pack          one pack per mass-length cell: the 24 x 5 runs files of that cell, one after the other
    dp_<i><j>_<k>_<w>.bin   (inside a pack) mass index i, length index j, theta1 index k (two digits), omega1 index w: b"DPN2", uint32 header
                            length, JSON header, then int16 little-endian frames; runs in the order theta2 index, then omega2
                            index (24 x 5 = 120 runs), N rows each, columns COLS (state, accelerations, twin angles, log10 of
                            the twin distance). Angles wrapped to [-pi, pi) in steps of 1e-4 rad; omega and alpha in the file's
                            own steps (header "scale"); log10 d in steps of 2e-4, clipped to +-6.5.
                            The frame rate of a file is the lowest of FPS_CHOICES at which no angle turns more than DTH_MAX
                            between frames and the cubic the page draws between frames stays within INTERP_TOL (TWIN_TOL for
                            the twin) x (l1 + l2) of the recorded 120 Hz path.
    double_pendulum.json    parameters, grid, every runs file with its pack, offset, bytes, SHA-256 and frame rate, and the checks.
Checks: energy drift of every run; the GPU result against a plain NumPy copy of the page's RK4 (same operations) and against
SciPy's DOP853 at rtol 1e-12 for the default start (how long they agree within 1 mm); the small-swing normal-mode periods; the
growth rate of the twin distance; the interpolation error.
Usage: python3 dp_engine.py <out_dir> [--smoke]"""
import hashlib, json, math, os, struct, sys, time
import numpy as np

# ---- parameters (SI) ----
G, M1, L1 = 9.81, 1.0, 1.0            # m/s^2, kg, m (the page's g, m1, l1)
EPS = 1e-3                            # rad, head start of the chaos twin in theta1 (the page's EPS)
H = 1 / 600                           # s, the page's RK4 step
LN_M = (-2.3, -1.15, 0.0, 1.15, 2.3)  # ln(m2/m1): m2 = 0.100, 0.317, 1, 3.16, 9.97 kg
LN_L = (-1.6, -0.8, 0.0, 0.8, 1.6)    # ln(l2/l1): l2 = 0.202, 0.449, 1, 2.23, 4.95 m
TH_DEG = tuple(range(-165, 181, 15))  # starting angles, degrees (-180 is the same position as 180)
W0 = (-5.0, -2.5, 0.0, 2.5, 5.0)      # rad/s, starting angular velocities (the page's slider range)
T_RUN = 20.0                          # s, length of every stored run
REC = 5                               # RK4 steps per recorded state (120 per second)
FPS_CHOICES = (20, 24, 30, 40, 60, 120)
DTH_MAX = 1.0                         # rad, largest turn of an angle between two stored frames
INTERP_TOL, TWIN_TOL = 2e-3, 4e-3     # largest distance of the drawn cubic from the recorded path, in units of l1 + l2
COLS = ["th1", "th2", "w1", "w2", "a1", "a2", "th1_t", "th2_t", "log10d"]
A_STEP, LD_STEP = 1e-4, 2e-4
NICE = (1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 0.1, 0.2, 0.5, 1.0)

def log(out, *a):
    print(time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a), flush=True)   # the Kaggle log; nothing extra in out_dir

# ---- the page's equations, in NumPy (host) ----
def accel(t1, t2, o1, o2, m2, l2):
    d = t1 - t2; den = 2 * M1 + m2 - m2 * np.cos(2 * d)
    a1 = (-G * (2 * M1 + m2) * np.sin(t1) - m2 * G * np.sin(t1 - 2 * t2) - 2 * np.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * np.cos(d))) / (L1 * den)
    a2 = (2 * np.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * np.cos(t1) + o2 * o2 * l2 * m2 * np.cos(d))) / (l2 * den)
    return a1, a2

def energy(t1, t2, o1, o2, m2, l2):
    return (0.5 * (M1 + m2) * L1 * L1 * o1 * o1 + 0.5 * m2 * l2 * l2 * o2 * o2 + m2 * L1 * l2 * o1 * o2 * np.cos(t1 - t2)
            - (M1 + m2) * G * L1 * np.cos(t1) - m2 * G * l2 * np.cos(t2))

def bob2(t1, t2, l2):
    return L1 * np.sin(t1) + l2 * np.sin(t2), -L1 * np.cos(t1) - l2 * np.cos(t2)

def rk4_numpy(s, m2, l2, n):
    """A plain copy of the page's rk4(): the same operations in the same order, one start, n steps; returns every REC-th state."""
    s = list(s); out = [list(s)]
    def deriv(s):
        t1, t2, o1, o2 = s; d = t1 - t2; den = 2 * M1 + m2 - m2 * math.cos(2 * d)
        a1 = (-G * (2 * M1 + m2) * math.sin(t1) - m2 * G * math.sin(t1 - 2 * t2) - 2 * math.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * math.cos(d))) / (L1 * den)
        a2 = (2 * math.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * math.cos(t1) + o2 * o2 * l2 * m2 * math.cos(d))) / (l2 * den)
        return [o1, o2, a1, a2]
    for k in range(n):
        k1 = deriv(s); s2 = [s[i] + H / 2 * k1[i] for i in range(4)]; k2 = deriv(s2); s3 = [s[i] + H / 2 * k2[i] for i in range(4)]
        k3 = deriv(s3); s4 = [s[i] + H * k3[i] for i in range(4)]; k4 = deriv(s4)
        s = [s[i] + H / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]
        if (k + 1) % REC == 0: out.append(list(s))
    return np.array(out)

# ---- the GPU integrator ----
def make_gpu():
    """JAX on the GPU, in 64-bit. If the Kaggle image's JAX does not see the GPU, install the CUDA build; stop if it still does not."""
    import subprocess
    probe = [sys.executable, "-c", "import jax; print(jax.default_backend())"]
    if subprocess.run(probe, capture_output=True, text=True).stdout.strip() != "gpu":
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]"], check=True)
        if subprocess.run(probe, capture_output=True, text=True).stdout.strip() != "gpu": raise SystemExit("no GPU seen by JAX: stopping before any computing")
    import jax, jax.numpy as jnp
    jax.config.update("jax_enable_x64", True)
    def deriv(s, m2, l2):
        t1, t2, o1, o2 = s[0], s[1], s[2], s[3]; d = t1 - t2; den = 2 * M1 + m2 - m2 * jnp.cos(2 * d)
        a1 = (-G * (2 * M1 + m2) * jnp.sin(t1) - m2 * G * jnp.sin(t1 - 2 * t2) - 2 * jnp.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * jnp.cos(d))) / (L1 * den)
        a2 = (2 * jnp.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * jnp.cos(t1) + o2 * o2 * l2 * m2 * jnp.cos(d))) / (l2 * den)
        return jnp.stack([o1, o2, a1, a2])
    def rk4(s, m2, l2):
        k1 = deriv(s, m2, l2); k2 = deriv(s + H / 2 * k1, m2, l2); k3 = deriv(s + H / 2 * k2, m2, l2); k4 = deriv(s + H * k3, m2, l2)
        return s + H / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    def record(s, m2, l2):
        s = jax.lax.fori_loop(0, REC, lambda i, q: rk4(q, m2, l2), s)
        return s, s
    @jax.jit
    def run(s0, m2, l2):   # s0: (4, B); returns (n_rec + 1, 4, B)
        n = int(round(T_RUN / H)) // REC
        _, ys = jax.lax.scan(lambda s, _: record(s, m2, l2), s0, None, length=n)
        return jnp.concatenate([s0[None], ys], axis=0)
    return jax, run

# ---- from recorded states to stored frames ----
def wrap(a): return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi
def nice(mx): return next(s for s in NICE if mx / s <= 32000)

def herm_err(th, om, stride, l2, twin=False):
    """Largest distance (m) of the lower bob drawn from every stride-th recorded state (cubic per frame pair) from the recorded path.
    th, om: (runs, n, 2) continuous angles and rates at 120 Hz. The twin takes its slopes from neighbouring frames."""
    n = th.shape[1]; idx = np.arange(0, n, stride); idx = idx if idx[-1] == n - 1 else np.append(idx, n - 1)
    if len(idx) < 3 or stride == 1: return 0.0
    P = th[:, idx]; h = stride / 120
    if twin:
        pm = np.concatenate([2 * P[:, :1] - P[:, 1:2], P[:, :-1]], 1); pp = np.concatenate([P[:, 1:], 2 * P[:, -1:] - P[:, -2:-1]], 1); Msl = (pp - pm) / 2
    else:
        Msl = om[:, idx] * h
    worst = 0.0
    for q in range(1, stride):
        u = q / stride; sel = idx[:-1] + q; ok = sel < idx[1:]
        if not ok.any(): continue
        h00, h10, h01, h11 = 2*u**3 - 3*u**2 + 1, u**3 - 2*u**2 + u, -2*u**3 + 3*u**2, u**3 - u**2
        A = h00 * P[:, :-1] + h10 * Msl[:, :-1] + h01 * P[:, 1:] + h11 * Msl[:, 1:]
        x, y = bob2(A[..., 0], A[..., 1], l2); X, Y = bob2(th[:, sel, 0], th[:, sel, 1], l2)
        worst = max(worst, float(np.hypot(x - X, y - Y)[:, ok].max()))
    return worst

def make_file(i, j, k, w, Ym, Yt, m2, l2):
    """Ym, Yt: recorded states (runs, n, 4) of the 120 runs (theta2 x omega2) of this file, main and twin."""
    th, om, tht = Ym[..., :2], Ym[..., 2:], Yt[..., :2]
    wmax = float(max(np.abs(om).max(), np.abs(Yt[..., 2:]).max()))
    for fps in FPS_CHOICES:
        st = 120 // fps
        if wmax / fps > DTH_MAX and fps != FPS_CHOICES[-1]: continue
        e1 = herm_err(th, om, st, l2); e2 = herm_err(tht, Yt[..., 2:], st, l2, True)
        if (e1 <= INTERP_TOL * (L1 + l2) and e2 <= TWIN_TOL * (L1 + l2)) or fps == FPS_CHOICES[-1]: break
    st = 120 // fps; sel = np.arange(0, Ym.shape[1], st)
    Fm, Ft = Ym[:, sel], Yt[:, sel]
    a1, a2 = accel(Fm[..., 0], Fm[..., 1], Fm[..., 2], Fm[..., 3], m2, l2)
    x, y = bob2(Fm[..., 0], Fm[..., 1], l2); xt, yt = bob2(Ft[..., 0], Ft[..., 1], l2)
    ld = np.clip(np.log10(np.maximum(np.hypot(x - xt, y - yt), 1e-300)), -6.5, 6.5)
    sw, sa = nice(np.abs(Fm[..., 2:]).max()), nice(max(np.abs(a1).max(), np.abs(a2).max()))
    C = np.stack([np.round(wrap(Fm[..., 0]) / A_STEP), np.round(wrap(Fm[..., 1]) / A_STEP), np.round(Fm[..., 2] / sw), np.round(Fm[..., 3] / sw),
                  np.round(a1 / sa), np.round(a2 / sa), np.round(wrap(Ft[..., 0]) / A_STEP), np.round(wrap(Ft[..., 1]) / A_STEP), np.round(ld / LD_STEP)], -1)
    assert np.abs(C).max() <= 32767
    S = (M1 + m2) * G * L1 + m2 * G * l2
    E = energy(Ym[..., 0], Ym[..., 1], Ym[..., 2], Ym[..., 3], m2, l2); Et = energy(Yt[..., 0], Yt[..., 1], Yt[..., 2], Yt[..., 3], m2, l2)
    runs = [dict(th2_deg=TH_DEG[r // len(W0)], w2=W0[r % len(W0)], E0=float(E[r, 0]), drift_max=float(np.abs(E[r] - E[r, 0]).max() / S),
                 twin_drift_max=float(np.abs(Et[r] - Et[r, 0]).max() / S), d_end=float(10 ** ld[r, -1])) for r in range(Ym.shape[0])]
    hdr = dict(model="double_pendulum", version=2, method="RK4, h = 1/600 s, float64 (the page's own)", file="dp_%d%d_%02d_%d.bin" % (i, j, k, w),
               cell=dict(i=i, j=j, ln_m=LN_M[i], ln_l=LN_L[j], m2=m2, l2=l2), m1=M1, l1=L1, g=G, eps=EPS, th1_deg=TH_DEG[k], w1=W0[w],
               th2_deg=list(TH_DEG), w2=list(W0), order="theta2 index, then omega2 index", fps=fps, frames=len(sel), T=T_RUN, S=S,
               columns=COLS, scale=dict(th=A_STEP, w=sw, a=sa, log10d=LD_STEP), interp_max_m=e1, interp_twin_max_m=e2, runs=runs)
    hb = json.dumps(hdr, separators=(",", ":")).encode()
    return hdr["file"], b"DPN2" + struct.pack("<I", len(hb)) + hb + C.astype("<i2").tobytes(), hdr

def checks(out):
    """Checks that do not depend on the grid (CPU, small)."""
    from scipy.integrate import solve_ivp
    ck = {}; n = int(round(T_RUN / H)); y0 = [math.radians(120), math.radians(150), 0.0, 0.0]
    R = rk4_numpy(y0, 1.0, 1.0, n); tt = np.arange(R.shape[0]) * REC * H
    def f(t, s):
        a1, a2 = accel(s[0], s[1], s[2], s[3], 1.0, 1.0); return [s[2], s[3], a1, a2]
    ref = solve_ivp(f, (0, T_RUN), y0, method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True).sol(tt)
    xa, ya = bob2(R[:, 0], R[:, 1], 1); xb, yb = bob2(ref[0], ref[1], 1); dd = np.hypot(xa - xb, ya - yb); bad = np.where(dd > 1e-3)[0]
    ck["rk4_vs_dop853_default"] = dict(agree_1mm_s=float(tt[bad[0]]) if bad.size else T_RUN, max_diff_first_5s_m=float(dd[tt < 5].max()))
    E = energy(R[:, 0], R[:, 1], R[:, 2], R[:, 3], 1, 1); ck["rk4_default_drift_max"] = float(np.abs(E - E[0]).max() / (3 * G))
    modes = {}
    for name, r, w, deg in (("slow", math.sqrt(2), math.sqrt(G * (2 - math.sqrt(2))), 0.5), ("fast", -math.sqrt(2), math.sqrt(G * (2 + math.sqrt(2))), 0.5),
                            ("slow_half", math.sqrt(2), math.sqrt(G * (2 - math.sqrt(2))), 0.25), ("fast_half", -math.sqrt(2), math.sqrt(G * (2 + math.sqrt(2))), 0.25)):
        a = math.radians(deg); Q = rk4_numpy([a, r * a, 0, 0], 1.0, 1.0, n); th = Q[:, 0]; t = np.arange(len(th)) * REC * H
        up = np.where((th[:-1] < 0) & (th[1:] >= 0))[0]; tc = t[up] - th[up] * (t[up + 1] - t[up]) / (th[up + 1] - th[up])
        P = float(np.mean(np.diff(tc))); modes[name] = dict(amplitude_deg=deg, period_s=P, theory_s=2 * math.pi / w, rel_diff=P * w / (2 * math.pi) - 1)
    ck["small_swings"] = modes
    Tw = rk4_numpy([y0[0] + EPS] + y0[1:], 1.0, 1.0, n); xt, yt = bob2(Tw[:, 0], Tw[:, 1], 1); d = np.hypot(xa - xt, ya - yt)
    stop = int(np.argmax(d > 0.1)); lam = float(np.polyfit(tt[:stop], np.log(d[:stop]), 1)[0]) if stop > 10 else float("nan")
    ck["twin_default"] = dict(lyapunov_fit_per_s=lam, d_passes_0_1m_s=float(tt[stop]) if stop else None)
    return ck, R

def run(out, smoke=False):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    jax, step_all = make_gpu(); dev = jax.devices(); log(out, "devices", dev)
    if smoke: LNM, LNL, TH, WW = (2,), (2,), (19,), (2, 3)          # the default cell, theta1 = 120 degrees, omega1 = 0 and 2.5
    else: LNM, LNL, TH, WW = range(len(LN_M)), range(len(LN_L)), range(len(TH_DEG)), range(len(W0))
    ck, Rnp = checks(out); log(out, "cpu checks done", json.dumps(ck))
    files, sizes, gpu_s = {}, 0, 0.0
    for i in LNM:
        for j in LNL:
            m2, l2 = M1 * math.exp(LN_M[i]), L1 * math.exp(LN_L[j])
            starts = [(math.radians(TH_DEG[k]), math.radians(t2), W0[w], w2) for k in TH for w in WW for t2 in TH_DEG for w2 in W0]
            S0 = np.array(starts).T; S0t = S0.copy(); S0t[0] += EPS
            tg = time.time(); Y = np.asarray(step_all(np.concatenate([S0, S0t], 1), m2, l2)); gpu_s += time.time() - tg   # (n, 4, 2B)
            B = S0.shape[1]; Ym = Y[:, :, :B].transpose(2, 0, 1); Yt = Y[:, :, B:].transpose(2, 0, 1); del Y
            if i == 2 and j == 2 and 19 in TH:   # the default start, 120 / 150 degrees from rest, against the NumPy copy of the page
                r = [n_ for n_, s in enumerate(starts) if abs(s[0] - math.radians(120)) < 1e-12 and abs(s[1] - math.radians(150)) < 1e-12 and s[2] == 0 and s[3] == 0]
                if r:
                    G2 = Ym[r[0]]; xa, ya = bob2(G2[:, 0], G2[:, 1], 1); xb, yb = bob2(Rnp[:, 0], Rnp[:, 1], 1); dd = np.hypot(xa - xb, ya - yb)
                    bad = np.where(dd > 1e-3)[0]; tt = np.arange(len(dd)) * REC * H
                    ck["gpu_vs_numpy_page_rk4_default"] = dict(max_diff_first_5s_m=float(dd[tt < 5].max()), agree_1mm_s=float(tt[bad[0]]) if bad.size else T_RUN,
                                                              identical_first_frames=int(np.argmax(dd > 0)) if (dd > 0).any() else len(dd))
            per = len(TH_DEG) * len(W0); pack = "dp_%d%d.pack" % (i, j); off = 0
            with open(os.path.join(out, pack), "wb") as fp:
                for q, (k, w) in enumerate([(k, w) for k in TH for w in WW]):
                    name, b, h = make_file(i, j, k, w, Ym[q * per:(q + 1) * per], Yt[q * per:(q + 1) * per], m2, l2)
                    fp.write(b); sizes += len(b)
                    files[name] = dict(pack=pack, offset=off, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), fps=h["fps"], drift_max=max(r_["drift_max"] for r_ in h["runs"]),
                                       interp=h["interp_max_m"] / (L1 + l2), interp_twin=h["interp_twin_max_m"] / (L1 + l2))
                    off += len(b)
            del Ym, Yt
            log(out, f"cell m={i} l={j}: {B} starts + twins, files so far {len(files)}, {sizes/1e9:.3f} GB, gpu {gpu_s:.1f} s, wall {time.time()-t0:.0f} s")
    ck["energy_drift_max_all"] = max(v["drift_max"] for v in files.values())
    ck["interp_max_rel"] = max(v["interp"] for v in files.values()); ck["interp_twin_max_rel"] = max(v["interp_twin"] for v in files.values())
    ck["frame_rates"] = sorted(set(v["fps"] for v in files.values()))
    summary = dict(model="double_pendulum", version=2, smoke=smoke, method="RK4, h = 1/600 s, float64, the page's own formulas and order; JAX on GPU",
                   params=dict(g=G, m1=M1, l1=L1, eps=EPS, h=H, ln_m=LN_M, ln_l=LN_L, th_deg=TH_DEG, w0=W0, T_run=T_RUN, rec_hz=120,
                               fps_choices=FPS_CHOICES, dth_max=DTH_MAX, interp_tol=INTERP_TOL, twin_tol=TWIN_TOL, columns=COLS),
                   device=str(dev), files=files, bytes=sizes, checks=ck, gpu_s=gpu_s, wall_s=time.time() - t0)
    json.dump(summary, open(os.path.join(out, "double_pendulum.json"), "w"), separators=(",", ":"))
    log(out, "done", len(files), "files", sizes, "bytes", f"wall {time.time()-t0:.0f} s")
    return summary

if __name__ == "__main__":
    run(sys.argv[1], "--smoke" in sys.argv)
