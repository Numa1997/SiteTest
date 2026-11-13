"""Gate B1 on Kaggle's GPU: the JAX port (cartctl.py) against the site's own reduced model (ref_series.json, from
stout-cart.js through tools/fig12/control/ref_series.cjs), six controllers over one 10 mm bump at 1 m/s, 2.3 s.
Also: the time per ride on the GPU, and jax.grad of the largest lean with respect to the LQR weight on q through a whole
ride (the gradient the tuning stage will use), checked against a central finite difference.
Writes /kaggle/working/<date>/b1.json the moment each part exists."""
import json, os, time, datetime
import numpy as np
import jax, jax.numpy as jnp
import cartctl as C

DATE = datetime.datetime.utcnow().strftime("%Y-%m-%d")
OUT = f"/kaggle/working/{DATE}" if os.path.isdir("/kaggle/working") else os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)
res = {"device": str(jax.devices()[0]), "x64": bool(jax.config.jax_enable_x64), "runs": {}}


def save():
    json.dump(res, open(f"{OUT}/b1.json", "w"), indent=1)


def log(msg):
    line = f"{datetime.datetime.utcnow():%H:%M:%S} UTC  {msg}"
    print(line, flush=True)
    open(f"{OUT}/progress.log", "a").write(line + "\n")


ref = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref_series.json")))
cs = ref["consts"]
r = cs["road"]
za = C.road_table(r["bumps"] + [{"x": 1.0 + 2 * n, "h": ref["bump"], "L": 0.25} for n in range(6, 60)], r["Rw"], r["xmin"], r["xmax"], r["h"])
zt = np.array([float(C.axle(jnp.asarray(za), r["xmin"], r["h"], x)[0]) for x in r["test_x"]])
res["road_max_abs_diff_m"] = float(np.max(np.abs(zt - np.array(r["test_za"]))))
log(f"device {res['device']}; road table against the JS: largest difference {res['road_max_abs_diff_m']:.3e} m")
save()
fl = cs["fluid"]
F = dict(w=jnp.asarray(fl["w"]), zeta=jnp.asarray(fl["zeta"]), beta=jnp.asarray(fl["beta"]), Pc=jnp.asarray(fl["Pc"]),
         g=9.81, ml=fl["mLiquid"])
cols = ref["cols"]
CODES = {"off": 0, "speed": 1, "preview": 2, "slosh": 3, "joint": 4}
for key, run in ref["runs"].items():
    name, susp = key.split("+")[0], 1 if "+" in key else 0
    P = C.make_params(cs, CODES[name], susp, run["K"], run["Ks"], run["plant"], za, run["ml"])
    f = jax.jit(lambda: C.ride(P, F, cs["cart"]["x0"], ref["T"]))
    t0 = time.time(); rows = np.asarray(f()); t1 = time.time(); rows = np.asarray(f()); t2 = time.time()
    R = np.asarray(run["rows"])
    n = min(len(R), len(rows))
    err = {c: float(np.max(np.abs(rows[:n, j] - R[:n, j]))) for j, c in enumerate(cols)}
    lean = float(np.max(np.abs(rows[:, -1])) * 1e3)
    res["runs"][key] = {"rows_jax": len(rows), "rows_js": len(R), "lean_max_mm_jax": lean, "lean_max_mm_js": run["lean_max_mm"],
                        "max_abs_err": err, "compile_plus_run_s": t1 - t0, "run_s": t2 - t1}
    log(f"{key:16s} lean {lean:7.3f} mm (JS {run['lean_max_mm']:7.3f}); worst errors: x {err['x']:.1e} m, i {err['i']:.1e} A, "
        f"q1 {err['q1']:.1e} m, zh_q {err['zh_q']:.1e} m; run {t2 - t1:.2f} s")
    save()

# the gradient the tuning will use: d(largest |lean|)/d(log weight on q), through the whole ride, slosh controller
run = ref["runs"]["slosh"]
pl = run["plant"]
Mx = float(C.massX(cs["cart"], run["ml"]))


def gains(logwq):
    w, z, be = pl["w"], pl["zeta"], pl["beta"]
    b, cx = 5.0, 2.0
    A = jnp.array([[-cx / Mx, 0, 0, 0], [0, 0, 1, 0], [be * cx / Mx, -w * w, -2 * z * w, 0], [-1.0, 0, 0, 0]])
    B = jnp.array([[b / Mx], [0], [-be * b / Mx], [0]])
    Q = jnp.diag(jnp.array([1 / 0.05 ** 2, jnp.exp(logwq) / 0.002 ** 2, 1 / (0.002 * w) ** 2, 1 / 0.02 ** 2]))
    # differentiable continuous Riccati: Newton-Kleinman iterations from the site's gains (each a Lyapunov solve)
    K = jnp.asarray(run["K"])[None, :]
    for _ in range(30):                     # (A - BK)'P + P(A - BK) + Q + K'RK = 0, R = 1/I_max^2 = 1/9; K = R^-1 B'P
        Acl = A - B @ K
        M = jnp.kron(jnp.eye(4), Acl.T) + jnp.kron(Acl.T, jnp.eye(4))
        Pm = jnp.linalg.solve(M, -(Q + K.T @ K / 9.0).reshape(-1)).reshape(4, 4)
        K = 9.0 * B.T @ Pm
    return K[0]


def peak_lean(logwq):
    P = C.make_params(cs, 3, 0, gains(logwq), run["Ks"], pl, za, run["ml"])
    rows = C.ride(P, F, cs["cart"]["x0"], ref["T"])
    lean = rows[:, -1]
    return jnp.sqrt(jnp.mean(lean ** 2)) * 1e3          # rms lean in mm (smooth, unlike the max)


Kchk = np.asarray(gains(0.0))
res["newton_kleinman_K_vs_site"] = float(np.max(np.abs(Kchk - np.asarray(run["K"]))))
g = jax.jit(jax.value_and_grad(peak_lean))
t0 = time.time(); v, dg = g(0.0); t1 = time.time()
eps = 1e-3
fd = (float(jax.jit(peak_lean)(eps)) - float(jax.jit(peak_lean)(-eps))) / (2 * eps)
res["grad"] = {"rms_lean_mm": float(v), "d_drms_dlogwq_ad": float(dg), "fd": fd, "rel_diff": abs(float(dg) - fd) / max(abs(fd), 1e-30),
               "time_s": t1 - t0}
log(f"gradient through the ride: rms lean {float(v):.4f} mm, d/dlog(w_q) AD {float(dg):.6e}, FD {fd:.6e}; K check {res['newton_kleinman_K_vs_site']:.1e}")
save()
log("done")
