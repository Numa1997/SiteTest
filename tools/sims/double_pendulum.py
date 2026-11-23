"""Fig. 2, the double pendulum: the reference model whose stored runs the page plays (docs/simulations/fig02-double-pendulum.md).

The setup. A rigid, massless rod of length l1 hangs from a fixed pivot and carries a point mass m1 at its end; a second rod of
length l2 hangs from that mass and carries a point mass m2. Everything moves in one vertical plane, without friction or air.
Gravity g points down. The two angles theta1, theta2 (rad) are measured from the downward vertical, counter-clockwise positive;
omega1, omega2 (rad/s) are their rates of change. With delta = theta1 - theta2, Lagrange's equations solved for the two angular
accelerations (the lecture note, equation (9)) are

    D = 2 m1 + m2 - m2 cos(2 delta)                                                          [kg]
    alpha1 = [-g (2 m1 + m2) sin theta1 - m2 g sin(theta1 - 2 theta2)
              - 2 sin(delta) m2 (omega2^2 l2 + omega1^2 l1 cos delta)] / (l1 D)               [rad/s^2]
    alpha2 = 2 sin(delta) [omega1^2 l1 (m1 + m2) + g (m1 + m2) cos theta1
              + omega2^2 l2 m2 cos delta] / (l2 D)                                            [rad/s^2]

and the energy, which the motion keeps constant (note, (3) and (4)), is

    E = 1/2 (m1 + m2) l1^2 omega1^2 + 1/2 m2 l2^2 omega2^2 + m2 l1 l2 omega1 omega2 cos(delta)
        - (m1 + m2) g l1 cos theta1 - m2 g l2 cos theta2                                     [J]

The grid. m1 = 1 kg, l1 = 1 m. The page's sliders hold ln(m2/m1) and ln(l2/l1); the model computes the three values of each at
the ends and the middle of the sliders' ranges, and every start released from rest (omega1 = omega2 = 0) with both angles on the
page's protractor marks, every 30 degrees: 3 x 3 x 12 x 12 = 1296 runs. Each run is also computed for the chaos twin, started with
theta1 + EPS. Nothing is random, so no seed is needed: the reader's sliders choose the start.

Integration: SciPy's DOP853 (an explicit Runge-Kutta method of order 8 that picks its own step), rtol 1e-10, atol 1e-12, for T_RUN
seconds; its continuous solution is sampled at the frames. The frame rate of each file is the smallest in FPS_CHOICES for which no
angle turns by more than DTH_MAX between frames and the cubic the page draws between frames (from the angles and angular velocities
of two neighbouring frames) stays within INTERP_TOL x (l1 + l2) of the true path of the lower bob, measured at 600 points a second;
for the twin, whose angular velocities are not stored, the page takes the slopes from the neighbouring frames and the bound is
TWIN_TOL x (l1 + l2).

Output, in out_dir:
  dp_<i><j>_<k>.bin   one file per mass index i, length index j (0, 1, 2) and starting angle theta1 index k (0..11): b"DPN1",
                      a uint32 header length, a JSON header (the cell, the frame rate, the column scales, one entry per run with
                      its start, its energy and its checks), then int16 little-endian frames, run after run (theta2 index 0..11),
                      T_RUN x fps + 1 rows each, columns COLS (the state, the accelerations, the twin's two angles, log10 of the twin
                      distance): angles wrapped to [-pi, pi) in 1e-4 rad, angular velocities and
                      accelerations in the file's own units (header "scale"), log10 of the twin distance (m) in 2e-4.
  double_pendulum.json the parameters, the grid, the file names and the checks of the whole generation.
Checks (in double_pendulum.json): the largest energy error of all runs; the same runs at 100 times tighter tolerances (how long
the two agree); the small-swing limit (the two normal-mode periods); the browser's former method (RK4, h = 1/600 s) against this
model for the page's default start; the growth rate of the twin distance.
Usage: python3 double_pendulum.py [out_dir]"""
import json, math, os, struct, sys, time
import numpy as np
from scipy.integrate import solve_ivp

# ---- parameters (SI) ----
G, M1, L1 = 9.81, 1.0, 1.0            # m/s^2, kg, m
EPS = 1e-3                            # rad, head start of the chaos twin in theta1
LN_M = (-2.3, 0.0, 2.3)               # ln(m2/m1): the mass slider's ends and middle (m2 = 0.100, 1, 9.97 kg)
LN_L = (-1.6, 0.0, 1.6)               # ln(l2/l1): the length slider's ends and middle (l2 = 0.202, 1, 4.95 m)
TH_DEG = tuple(range(-150, 181, 30))  # starting angles, degrees (-180 is the same as 180)
T_RUN = 20.0                          # s, length of every stored run
RTOL, ATOL = 1e-10, 1e-12             # DOP853 tolerances
FPS_CHOICES = (20, 25, 30, 40, 50, 60, 75, 100, 120)
DTH_MAX = 1.0                         # rad, largest turn of an angle between two frames
INTERP_TOL = 2e-3                     # largest distance of the drawn cubic from the true lower bob, in units of l1 + l2
TWIN_TOL = 4e-3                       # the same for the twin, whose cubic takes its slopes from the neighbouring frames
COLS = ["th1", "th2", "w1", "w2", "a1", "a2", "th1_t", "th2_t", "log10d"]
A_STEP = 1e-4                         # rad per unit of a stored angle
LD_STEP = 2e-4                        # per unit of the stored log10 of the twin distance (range +-6.5)
NICE = (1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 0.1, 0.2, 0.5, 1.0)

def accel(s, m2, l2):
    """The two angular accelerations (rad/s^2) of the state s = (theta1, theta2, omega1, omega2); s may hold many states."""
    t1, t2, o1, o2 = s[0], s[1], s[2], s[3]; d = t1 - t2
    den = 2 * M1 + m2 - m2 * np.cos(2 * d)
    a1 = (-G * (2 * M1 + m2) * np.sin(t1) - m2 * G * np.sin(t1 - 2 * t2) - 2 * np.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * np.cos(d))) / (L1 * den)
    a2 = (2 * np.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * np.cos(t1) + o2 * o2 * l2 * m2 * np.cos(d))) / (l2 * den)
    return a1, a2

def rhs_factory(m2, l2):
    c1, c2, c3 = G * (2 * M1 + m2), m2 * G, G * (M1 + m2)
    sin, cos = math.sin, math.cos
    def f(t, s):
        t1, t2, o1, o2 = s; d = t1 - t2; sd, cd = sin(d), cos(d); den = 2 * M1 + m2 - m2 * cos(2 * d)
        return [o1, o2, (-c1 * sin(t1) - c2 * sin(t1 - 2 * t2) - 2 * sd * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * cd)) / (L1 * den),
                2 * sd * (o1 * o1 * L1 * (M1 + m2) + c3 * cos(t1) + o2 * o2 * l2 * m2 * cd) / (l2 * den)]
    return f

def energy(s, m2, l2):
    t1, t2, o1, o2 = s[0], s[1], s[2], s[3]
    return (0.5 * (M1 + m2) * L1 * L1 * o1 * o1 + 0.5 * m2 * l2 * l2 * o2 * o2 + m2 * L1 * l2 * o1 * o2 * np.cos(t1 - t2)
            - (M1 + m2) * G * L1 * np.cos(t1) - m2 * G * l2 * np.cos(t2))

def bob2(th1, th2, l2):
    return L1 * np.sin(th1) + l2 * np.sin(th2), -L1 * np.cos(th1) - l2 * np.cos(th2)

def solve(m2, l2, y0, rtol=RTOL, atol=ATOL):
    return solve_ivp(rhs_factory(m2, l2), (0, T_RUN), y0, method="DOP853", rtol=rtol, atol=atol, dense_output=True)

def hermite(F, h, u):
    """The page's drawing between two frames: the cubic through angle p0, p1 with rates m0, m1 (F = p0, p1, m0, m1)."""
    p0, p1, m0, m1 = F
    return (2 * u**3 - 3 * u**2 + 1) * p0 + (u**3 - 2 * u**2 + u) * h * m0 + (-2 * u**3 + 3 * u**2) * p1 + (u**3 - u**2) * h * m1

def slopes(p, fps):
    """The twin's rates as the page estimates them from its stored angles alone: (next - previous) / 2 frames (Catmull-Rom)."""
    pm = np.concatenate(([2 * p[0] - p[1]], p[:-1])); pp = np.concatenate((p[1:], [2 * p[-1] - p[-2]]))
    return (pp - pm) / 2 * fps

def interp_error(sol, fps, l2, twin=False):
    """Largest distance (m) between the lower bob drawn from frames at this rate and the model's own continuous solution.
    The main pendulum is drawn with its stored angular velocities; the twin (twin=True) with slopes from its neighbouring frames."""
    tt = np.arange(0, T_RUN, 1 / 600); Y = sol(tt); tf = np.arange(int(round(T_RUN * fps)) + 1) / fps; Fr = sol(tf)
    if twin: Fr = np.array([Fr[0], Fr[1], slopes(Fr[0], fps), slopes(Fr[1], fps)])
    k = np.minimum((tt * fps).astype(int), len(tf) - 2); u = tt * fps - k; h = 1 / fps
    a = hermite((Fr[0][k], Fr[0][k + 1], Fr[2][k], Fr[2][k + 1]), h, u); b = hermite((Fr[1][k], Fr[1][k + 1], Fr[3][k], Fr[3][k + 1]), h, u)
    x, y = bob2(a, b, l2); X, Yy = bob2(Y[0], Y[1], l2)
    return float(np.hypot(x - X, y - Yy).max())

def nice(mx, top=32000):
    return next(s for s in NICE if mx / s <= top)

def wrap(a):
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi

def one_file(job):
    """All twelve runs (theta2 = -150..180 degrees) of one cell and one theta1, with their twins; returns (name, bytes, header)."""
    i, j, k = job; m2, l2 = M1 * math.exp(LN_M[i]), L1 * math.exp(LN_L[j]); th1 = math.radians(TH_DEG[k])
    sols, twins, runs = [], [], []
    for th2d in TH_DEG:
        y0 = [th1, math.radians(th2d), 0.0, 0.0]; s = solve(m2, l2, y0); tw = solve(m2, l2, [th1 + EPS] + y0[1:])
        sols.append(s); twins.append(tw)
    wmax = max(float(np.abs(q.y[2:]).max()) for q in sols + twins)
    fps = next(f for f in FPS_CHOICES if wmax / f <= DTH_MAX)
    while True:   # raise the rate until the drawn cubic follows the true path closely enough
        err = max(interp_error(q.sol, fps, l2) for q in sols); err_t = max(interp_error(q.sol, fps, l2, True) for q in twins)
        if (err <= INTERP_TOL * (L1 + l2) and err_t <= TWIN_TOL * (L1 + l2)) or fps == FPS_CHOICES[-1]: break
        fps = FPS_CHOICES[FPS_CHOICES.index(fps) + 1]
    nf = int(round(T_RUN * fps)); tf = np.arange(nf + 1) / fps
    raw = []
    for th2d, s, tw in zip(TH_DEG, sols, twins):
        Y, Z = s.sol(tf), tw.sol(tf); a1, a2 = accel(Y, m2, l2)
        x, y = bob2(Y[0], Y[1], l2); xt, yt = bob2(Z[0], Z[1], l2); d = np.hypot(x - xt, y - yt)
        E = energy(Y, m2, l2); Ed = energy(s.y, m2, l2); S = (M1 + m2) * G * L1 + m2 * G * l2
        raw.append((Y, Z, a1, a2, np.log10(d)))
        runs.append(dict(th2_deg=th2d, E0=float(E[0]), S=S, drift_max=float(np.abs(Ed - Ed[0]).max() / S),
                         drift_end=float((E[-1] - E[0]) / S), twin_drift_max=float(np.abs(energy(tw.y, m2, l2) - energy(tw.y[:, :1], m2, l2)[0]).max() / S),
                         steps=int(s.t.size - 1), nfev=int(s.nfev), d_end=float(d[-1])))
    sc_w = nice(max(np.abs(r[0][2:]).max() for r in raw))
    sc_a = nice(max(max(np.abs(r[2]).max(), np.abs(r[3]).max()) for r in raw))
    rows = []
    for Y, Z, a1, a2, ld in raw:
        c = np.stack([np.round(wrap(Y[0]) / A_STEP), np.round(wrap(Y[1]) / A_STEP), np.round(Y[2] / sc_w), np.round(Y[3] / sc_w),
                      np.round(a1 / sc_a), np.round(a2 / sc_a), np.round(wrap(Z[0]) / A_STEP), np.round(wrap(Z[1]) / A_STEP),
                      np.round(ld / LD_STEP)], axis=1)
        assert np.abs(c).max() <= 32767
        rows.append(c.astype("<i2"))
    # what storing as int16 costs: the largest rounding of each quantity
    q = dict(angle_rad=A_STEP / 2, omega_rad_s=sc_w / 2, alpha_rad_s2=sc_a / 2, log10d=LD_STEP / 2)
    hdr = dict(model="double_pendulum", version=1, file="dp_%d%d_%02d.bin" % (i, j, k), cell=dict(i=i, j=j, ln_m=LN_M[i], ln_l=LN_L[j], m2=m2, l2=l2),
               m1=M1, l1=L1, g=G, eps=EPS, th1_deg=TH_DEG[k], th2_deg=list(TH_DEG), w0=[0.0, 0.0], fps=fps, frames=nf + 1, T=T_RUN,
               columns=COLS, scale=dict(th=A_STEP, w=sc_w, a=sc_a, log10d=LD_STEP), quantisation=q, interp_max_m=err, interp_twin_max_m=err_t, runs=runs)
    hb = json.dumps(hdr, separators=(",", ":")).encode()
    return hdr["file"], b"DPN1" + struct.pack("<I", len(hb)) + hb + b"".join(r.tobytes() for r in rows), hdr

def checks(files):
    """The checks of the whole generation, beyond the energy of each run."""
    out = {}
    # 1. the small-swing limit: equal masses and rods, released 0.5 and 0.25 degrees out in each normal-mode shape (note, section 5);
    #    the gap to the linear theory should shrink four times when the amplitude halves, as the first nonlinear correction does
    w_slow, w_fast = math.sqrt(G / L1 * (2 - math.sqrt(2))), math.sqrt(G / L1 * (2 + math.sqrt(2)))
    modes = {}
    for name, r, w, deg in (("slow", math.sqrt(2), w_slow, 0.5), ("fast", -math.sqrt(2), w_fast, 0.5), ("slow_half", math.sqrt(2), w_slow, 0.25), ("fast_half", -math.sqrt(2), w_fast, 0.25)):
        a = math.radians(deg); s = solve_ivp(rhs_factory(1.0, 1.0), (0, 20), [a, r * a, 0, 0], method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)
        tt = np.linspace(0, 20, 200001); th = s.sol(tt)[0]; up = np.where((th[:-1] < 0) & (th[1:] >= 0))[0]
        tc = tt[up] - th[up] * (tt[up + 1] - tt[up]) / (th[up + 1] - th[up]); P = float(np.mean(np.diff(tc)))
        modes[name] = dict(amplitude_deg=deg, period_model_s=P, period_theory_s=2 * math.pi / w, rel_diff=P * w / (2 * math.pi) - 1)
    out["small_swings"] = modes
    # 2. tolerance: the default cell's default theta1 row at 100 times tighter tolerances; how long the two runs agree
    m2, l2 = 1.0, 1.0; agree = []
    for th2d in TH_DEG:
        y0 = [math.radians(120), math.radians(th2d), 0, 0]; a = solve(m2, l2, y0); b = solve(m2, l2, y0, 1e-12, 1e-14)
        tt = np.arange(0, T_RUN, 1 / 600); A, B = a.sol(tt), b.sol(tt); xa, ya = bob2(A[0], A[1], l2); xb, yb = bob2(B[0], B[1], l2)
        dd = np.hypot(xa - xb, ya - yb); bad = np.where(dd > 1e-3)[0]
        agree.append(dict(th2_deg=th2d, agree_1mm_s=float(tt[bad[0]]) if bad.size else T_RUN, max_diff_first_5s_m=float(dd[tt < 5].max())))
    out["tolerance_rtol1e-12_vs_1e-10_theta1_120"] = agree
    # 3. the browser's former method: RK4 at h = 1/600 s for the page's default start, against this model
    y = np.array([math.radians(120), math.radians(150), 0.0, 0.0]); f = rhs_factory(1.0, 1.0); h = 1 / 600; n = int(T_RUN * 600)
    ref = solve(1.0, 1.0, list(y)); R = np.empty((n + 1, 4)); R[0] = y; E0 = energy(y, 1, 1)
    for i in range(n):
        k1 = np.array(f(0, y)); k2 = np.array(f(0, y + h / 2 * k1)); k3 = np.array(f(0, y + h / 2 * k2)); k4 = np.array(f(0, y + h * k3))
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); R[i + 1] = y
    tt = np.arange(n + 1) * h; Q = ref.sol(tt); xr, yr = bob2(R[:, 0], R[:, 1], 1); xq, yq = bob2(Q[0], Q[1], 1); dd = np.hypot(xr - xq, yr - yq)
    bad = np.where(dd > 1e-3)[0]; Er = energy(R.T, 1, 1)
    out["browser_rk4_default_start"] = dict(agree_1mm_s=float(tt[bad[0]]) if bad.size else T_RUN, max_diff_first_5s_m=float(dd[tt < 5].max()),
                                           rk4_drift_max=float(np.abs(Er - E0).max() / (2 * G + G)), steps=n)
    # 4. chaos: growth rate of the twin distance for the default start, a straight-line fit of ln d between 1e-3 and 1e-1 m
    tw = solve(1.0, 1.0, [math.radians(120) + EPS, math.radians(150), 0, 0]); tt = np.arange(0, T_RUN, 1 / 600)
    A, B = ref.sol(tt), tw.sol(tt); xa, ya = bob2(A[0], A[1], 1); xb, yb = bob2(B[0], B[1], 1); d = np.hypot(xa - xb, ya - yb)
    stop = np.argmax(d > 0.1); sel = slice(0, stop) if stop else slice(None); lam = float(np.polyfit(tt[sel], np.log(d[sel]), 1)[0])
    out["twin_default_start"] = dict(lyapunov_fit_per_s=lam, fit_until_s=float(tt[stop]) if stop else T_RUN, d_at_10s_m=float(d[np.searchsorted(tt, 10)]))
    # 5. every run: energy
    allr = [r for h in files for r in h["runs"]]
    out["energy"] = dict(runs=len(allr), drift_max=max(r["drift_max"] for r in allr), twin_drift_max=max(r["twin_drift_max"] for r in allr))
    out["frame_rates"] = {h["file"]: h["fps"] for h in files}
    out["interp_max_rel"] = max(h["interp_max_m"] / (L1 + h["cell"]["l2"]) for h in files)
    out["interp_twin_max_rel"] = max(h["interp_twin_max_m"] / (L1 + h["cell"]["l2"]) for h in files)
    return out

def run(out_dir=".", jobs=None, procs=None):
    t0 = time.time(); os.makedirs(out_dir, exist_ok=True)
    jobs = jobs or [(i, j, k) for i in range(len(LN_M)) for j in range(len(LN_L)) for k in range(len(TH_DEG))]
    procs = procs or os.cpu_count() or 1
    if procs > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(procs) as pool: res = pool.map(one_file, jobs, chunksize=1)
    else:
        res = [one_file(j) for j in jobs]
    hdrs = []
    for name, b, h in res:
        open(os.path.join(out_dir, name), "wb").write(b); hdrs.append(h)
    ck = checks(hdrs)
    summary = dict(model="double_pendulum", version=1, about="Fig. 2, the double pendulum, computed once: every start of the grid and its chaos twin. "
                   "File dp_<i><j>_<k>.bin holds mass index i, length index j and starting angle theta1 index k; its header says how to read it.",
                   params=dict(g=G, m1=M1, l1=L1, eps=EPS, ln_m=LN_M, ln_l=LN_L, th_deg=TH_DEG, w0=[0, 0], T_run=T_RUN, rtol=RTOL, atol=ATOL,
                               fps_choices=FPS_CHOICES, dth_max=DTH_MAX, interp_tol=INTERP_TOL, twin_tol=TWIN_TOL, columns=COLS),
                   files=sorted(h["file"] for h in hdrs), bytes=sum(len(b) for _, b, _ in res), checks=ck, wall_s=time.time() - t0)
    json.dump(summary, open(os.path.join(out_dir, "double_pendulum.json"), "w"), indent=1)
    print(json.dumps(dict(files=len(hdrs), bytes=summary["bytes"], energy=ck["energy"], fps=sorted(set(ck["frame_rates"].values())),
                          small_swings=ck["small_swings"], rk4=ck["browser_rk4_default_start"], twin=ck["twin_default_start"], wall_s=summary["wall_s"]), indent=1))
    return summary

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")
