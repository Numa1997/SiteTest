# Fig. 12 in JAX on Kaggle's GPU, first run (13 Nov 2026): the stout at rest, its free swing, and two rides that spill.
# Writes to /kaggle/working/<date>/: one .npz per task (surface, drops, cart, books, every frame), summary.json, progress.log.
# Each task is started only if the time measured so far says it ends inside BUDGET_S.
import os, json, time, datetime
from pathlib import Path
import numpy as np
import jax, jax.numpy as jnp
from stout_jax import Geometry, Stout, Cart, CART_COMMON, road_table, make_advance, ride_extra, F64, RBUB, PHI_F, GAMMA, E_INF, G_HEAD, TAU_Y, Z_WALL, LR_WALL

R = json.load(open(os.environ["GLASS_JSON"]))["R"]; DZP = 0.0005
FILL, RHO, FPS = 0.125, 1007.0, 30
BUDGET_S = float(os.environ.get("BUDGET_S", "2450"))
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
WORK = Path(os.environ.get("NB_WORK", "/kaggle/working")) / STAMP; WORK.mkdir(parents=True, exist_ok=True)
T0 = time.time()


def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc):%H:%M:%S} UTC {(time.time() - T0) / 60:5.1f} min  {msg}"
    print(line, flush=True)
    with open(WORK / "progress.log", "a") as f: f.write(line + "\n")


ROADS = {
    # one tall bump, 25 mm high and 0.30 m long: at 1 m/s it lasts 0.3 s, about one period of the stout's first swing
    "one 25 mm bump": {"kind": "bumps", "bumps": [{"x": 1.5, "h": 0.025, "L": 0.30}]},
    # five 20 mm bumps 0.29 m apart: at 1 m/s they come 3.4 times a second, in step with the swing (3.42 Hz)
    "five 20 mm bumps in step with the swing": {"kind": "bumps", "bumps": [{"x": 1.5 + 0.29 * i, "h": 0.020, "L": 0.25} for i in range(5)]},
    # one short, sharp bump, 30 mm high and 0.12 m long, taken at 1.5 m/s: a kerb-like jolt
    "one sharp 30 mm bump": {"kind": "bumps", "bumps": [{"x": 1.5, "h": 0.030, "L": 0.12}]},
}
TASKS = [   # third run (13 Nov 2026): the head as a sheet that resists shear; surface read-out corrected
    dict(name="rest", kind="free", dx=0.0015, model="full", end=2.0, push=(0.3, 0.0, 0.146)),
    dict(name="ride_resonant", kind="ride", dx=0.0015, model="full", end=8.0, road="five 20 mm bumps in step with the swing", v0=1.0),
    dict(name="free_full_1.5", kind="free", dx=0.0015, model="full", end=5.0, push=(0.3, 1.0, 0.146)),
    dict(name="ride_sharp30", kind="ride", dx=0.0015, model="full", end=4.0, road="one sharp 30 mm bump", v0=1.5),
    dict(name="ride_bump25", kind="ride", dx=0.0015, model="full", end=8.0, road="one 25 mm bump", v0=1.0),
]
if os.environ.get("CODECHECK"):   # a check of this script only: two frames on a 6 mm grid, results thrown away
    TASKS = [dict(t, dx=0.006, end=2 / FPS) for t in TASKS[:4]]
measured = {}   # dx -> seconds per simulated second (fluid), from finished tasks
summary = dict(generated=STAMP, device=jax.devices()[0].device_kind, jax=jax.__version__, fill=FILL, rho=RHO, fps=FPS, tasks=[])


def fit_swing(t, q):
    """q = A exp(-t/tau) cos(w t + phi) + c, least squares (scipy); returns frequency (Hz) and damping ratio."""
    from scipy.optimize import curve_fit
    f0 = 3.4; A0 = float(np.max(np.abs(q - q.mean())))
    fun = lambda t, A, tau, w, ph, c: A * np.exp(-t / tau) * np.cos(w * t + ph) + c
    best = None
    for ph in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        try:
            p, _ = curve_fit(fun, t, q, p0=[A0, 5.0, 2 * np.pi * f0, ph, q.mean()], maxfev=20000)
            r = np.sum((fun(t, *p) - q) ** 2)
            if best is None or r < best[1]: best = (p, r)
        except Exception:
            pass
    if best is None: return dict(f=None, zeta=None)
    A, tau, w, ph, c = best[0]
    return dict(f=float(abs(w) / (2 * np.pi)), zeta=float(1 / (abs(w) * tau)), A_mm=float(abs(A) * 1e3), rms_mm=float(np.sqrt(best[1] / len(t)) * 1e3))


for task in TASKS:
    name, dx = task["name"], task["dx"]
    rate = measured.get(dx) or (max(measured.values()) * (0.0015 / dx) ** 3 if measured else 250.0)
    est = rate * task["end"] + 90
    if time.time() - T0 + est > BUDGET_S:
        log(f"skip {name}: needs about {est:.0f} s, {BUDGET_S - (time.time() - T0):.0f} s left in the budget"); continue
    log(f"start {name}: grid {dx * 1e3:.1f} mm, {task['model']}, {task['end']} s of stout; about {est:.0f} s")
    G = Geometry(R, DZP, FILL, dx); S = Stout(G, model=task["model"], rho=RHO)
    log(f"  {G.n} x {G.n} x {G.nz} = {G.n * G.n * G.nz:,} cells, {S.N:,} particles, stout {S.rho * S.V * 1e3:.1f} g; "
        f"glass area in the cells {G.area_cells * 1e4:.1f} cm^2 (profile {G.area_profile * 1e4:.1f})")
    s = S.init_state(); t = jnp.zeros((), F64)
    if task["kind"] == "free":
        adv = make_advance(S, "free", push=task["push"]); ex = dict(vmax=jnp.zeros((), F64), t_end=jnp.zeros((), F64))
    else:
        road = road_table(ROADS[task["road"]], xmax=0.5 + task["v0"] * task["end"] * 1.3 + 2)
        cart = Cart(dict(CART_COMMON, v0=task["v0"], ctrl=1, susp=0), road)
        adv = make_advance(S, "ride", cart=cart); ex = ride_extra(S, cart)
    obs = jax.jit(S.observe); pol = jax.jit(S.polar)
    nf = int(round(task["end"] * FPS)); rec = {k: [] for k in ("t", "H", "polar", "drops", "ndrops", "nfly", "nlanded", "nstuck", "nact", "KE", "PE", "Px",
                                                              "ewall", "efoam", "eskin", "hf", "lumps", "lumpvol", "foam_spill", "steps", "its", "itmax", "resmax", "nselmax", "wall_s",
                                                              "x", "v", "zb", "zw", "i", "Nwheel", "Fx", "Fz")}

    def record(s, t, ex, st, wall):
        o = obs(s); P = pol(o["H"])
        rec["t"].append(float(t)); rec["H"].append(np.asarray(o["H"])); rec["polar"].append(np.asarray(P))
        rec["drops"].append(np.asarray(o["drops"]).astype(np.float16))
        for k in ("ndrops", "nfly", "nlanded", "nstuck", "nact", "KE", "PE", "Px", "ewall", "efoam", "eskin", "foam_spill"): rec[k].append(float(o[k]))
        rec["hf"].append(np.asarray(o["hf"]).astype(np.float16)); rec["lumps"].append(np.asarray(o["lumps"]).astype(np.float16))
        rec["lumpvol"].append(np.asarray(o["lumpvol"]).astype(np.float32))
        for k in ("steps", "its", "itmax", "resmax", "nselmax"): rec[k].append(float(st[k]) if st is not None else 0.0)
        rec["wall_s"].append(wall)
        if task["kind"] == "ride":
            c = ex["cart"]
            for k, kk in (("x", "x"), ("v", "vx"), ("zb", "zb"), ("zw", "zw"), ("i", "i"), ("Nwheel", "N")): rec[k].append(float(c[kk]))
            rec["Fx"].append(float(ex["F"][0])); rec["Fz"].append(float(ex["F"][1]))

    record(s, t, ex, None, 0.0)
    Tc = time.time(); comp_s = None; Tlast = time.time(); steps = 0; its = 0
    for f in range(1, nf + 1):
        ex = dict(ex, t_end=jnp.asarray(f / FPS, F64))
        T1 = time.time(); s, t, ex, st = adv(s, t, ex); jax.block_until_ready(s["xp"]); w = time.time() - T1
        if comp_s is None: comp_s = w        # the first frame includes compiling
        steps += int(st["steps"]); its += int(st["its"])
        record(s, t, ex, st, w)
        if int(st["nselmax"]) >= S.K: log(f"  STOP frame {f}: {int(st['nselmax'])} particles near the surface, the list holds {S.K}"); break
        if int(rec["ndrops"][-1]) >= S.M: log(f"  STOP frame {f}: {int(rec['ndrops'][-1])} drops, the list holds {S.M}"); break
        if not np.isfinite(rec["KE"][-1]) or rec["KE"][-1] > 10: log(f"  STOP: kinetic energy {rec['KE'][-1]} J at t = {float(t):.3f} s"); break
        if time.time() - Tlast > 60:
            Tlast = time.time(); el = Tlast - Tc - comp_s
            log(f"  {float(t):.2f} of {task['end']} s; {steps:,} steps; {el / max(steps - int(st['steps']), 1) * 1e3:.0f} ms a step; "
                f"{its / steps:.0f} pressure iterations a step; spilled {S.N - rec['nact'][-1]:,} particles")
    wall = time.time() - Tc; run_s = wall - comp_s
    rate_now = run_s / max(float(t) - 1 / FPS, 1e-6); measured[dx] = rate_now
    out = {k: np.array(v) for k, v in rec.items() if len(v)}
    np.savez_compressed(WORK / f"{name}.npz", **out, dx=dx, fill=FILL, x0=G.x0, n=G.n, Rfill=G.Rfill, mp=S.mp, N=S.N)
    pol_arr = out["polar"]; tt = out["t"]
    info = dict(task, cells=G.n * G.n * G.nz, particles=S.N, mp=S.mp, steps=steps, compile_s=round(comp_s, 1), run_s=round(run_s, 1),
                ms_per_step=round(run_s / max(steps - 1, 1) * 1e3, 1), its_per_step=round(its / max(steps, 1), 1),
                itmax=int(out["itmax"].max()), resmax=float(out["resmax"].max()), nselmax=int(out["nselmax"].max()), K=S.K,
                s_per_simulated_s=round(rate_now, 1), spilled_g=round((S.N - out["nact"][-1]) * S.mp * 1e3, 2),
                drops_max=int(out["ndrops"].max()), volume_kept=float(out["nact"][-1] / S.N),
                head_spilled_ml=round(float(out["foam_spill"][-1]) * 1e6, 2), head_ml=round(float(np.asarray(S.init_state()["foam0"])) * 1e6, 1),
                head=dict(R32=RBUB, phi_l=PHI_F, gamma=GAMMA, E_inf=E_INF, G0=G_HEAD, tau_y=TAU_Y, Z=Z_WALL, lr=LR_WALL))
    dev = (pol_arr - FILL) * 1e3
    if task["kind"] == "free":
        th = 2 * np.pi * np.arange(pol_arr.shape[2]) / pol_arr.shape[2]
        q13 = 2 / len(th) * (pol_arr[:, 13] * np.cos(th)).sum(1); q16 = 2 / len(th) * (pol_arr[:, 16] * np.cos(th)).sum(1)
        info["max_dev_mm"] = float(np.nanmax(np.abs(dev))); info["max_dev_last_s_mm"] = float(np.nanmax(np.abs(dev[tt > tt[-1] - 1])))
        if task["push"][1] > 0 and (tt > task["push"][0] + task["push"][2] + 0.1).sum() > 30:
            m = tt > task["push"][0] + task["push"][2] + 0.1
            info["fit_ring13"] = fit_swing(tt[m] - tt[m][0], q13[m]); info["fit_ring16"] = fit_swing(tt[m] - tt[m][0], q16[m])
        E = out["KE"] + out["PE"]; info["energy_J"] = [float(E[0]), float(E[-1])]
    else:
        lean = (pol_arr[:, 16, 0] - pol_arr[:, 16, 32]) * 1e3
        info["lean_max_mm"] = float(np.nanmax(np.abs(lean))); info["v_range"] = [float(out["v"].min()), float(out["v"].max())]
        info["impulse_vs_momentum"] = dict(impulse_x=float(np.asarray(ex["imp"][0])), momentum_x_end=float(np.asarray(ex["P"][0])))
    summary["tasks"].append(info)
    json.dump(summary, open(WORK / "summary.json", "w"), indent=1)
    log(f"done {name}: {steps:,} steps, compile {comp_s:.0f} s, {info['ms_per_step']} ms a step, {info['its_per_step']} pressure iterations a step; "
        f"spilled {info['spilled_g']} g; " + (f"fit {info.get('fit_ring13')}" if task["kind"] == "free" else f"lean up to {info['lean_max_mm']:.1f} mm"))
log("all done")
