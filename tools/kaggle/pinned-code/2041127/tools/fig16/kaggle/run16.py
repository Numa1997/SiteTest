"""Fig. 16 on Kaggle's GPU: Fig. 12's pint (stout_jax.Stout, the full model with the head and its mass, unchanged) carried by the
four-wheel cart of cart4.py with its control system, over Fig. 12's roads. Writes to /kaggle/working/<date>/: one .npz per task,
summary.json, design.json, progress.log. The structure follows tools/fig12/kaggle/run_b.py (tasks, budget, books, the rest guard).

Order of the tasks (if the budget runs short, what is done is whole):
  rest       the pint standing still for 2 s: the guard (flat and full, or the session stops)
  design     on the CPU, in seconds: the controller for a few weightings, each tried on the kerb with the validated few-mode stout
             (modal4.py); the weighting with the least head spilled, then the least wall rise, is used for every ride below
  kerb_full  the kerb (Fig. 12's one sharp 30 mm bump) at 1.5 m/s with the control system
  kerb_off   the same machine with its control system off (passive struts, speed held by a PI loop)
  resonant_full, bump25_full   the two gentle roads of Fig. 12 at 1.0 m/s with the control system
Environment: GLASS_JSON (as run_b.py), BUDGET_S, CODECHECK (6 mm grid, two frames per task: the smoke test), NB_WORK."""
import os, sys, json, time, datetime, math
from pathlib import Path
import numpy as np
import jax, jax.numpy as jnp
from jax import lax
from stout_jax import Geometry, Stout, road_table, make_advance, F64, I32, HEAD0, PHI_F
import cart4 as C4

R = json.load(open(os.environ["GLASS_JSON"]))["R"]; DZP = 0.0005
FILL, RHO, FPS = 0.125, 1007.0, 30
BUDGET_S = float(os.environ.get("BUDGET_S", "2000")); CODECHECK = bool(os.environ.get("CODECHECK"))
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
WORK = Path(os.environ.get("NB_WORK", "/kaggle/working")) / STAMP; WORK.mkdir(parents=True, exist_ok=True)
T0 = time.time()
REST_MAX_CELLS, REST_RMS_CELLS = 0.5, 0.25


def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc):%H:%M:%S} UTC {(time.time() - T0) / 60:5.1f} min  {msg}"
    print(line, flush=True)
    with open(WORK / "progress.log", "a") as f: f.write(line + "\n")


_src = open(os.path.join(os.path.dirname(os.path.abspath(C4.__file__)), "..", "..", "fig12", "kaggle", "run_b.py")).read()
_a = _src.index("ROADS = {"); _b = _src.index("\n}\n", _a) + 2
ROADS = eval(_src[_a + len("ROADS = "):_b])       # Fig. 12's roads, exactly as run_b.py defines them
KERB, RES, B25 = "one sharp 30 mm bump", "five 20 mm bumps in step with the swing", "one 25 mm bump"
dx0 = 0.006 if CODECHECK else 0.0015
end_ = lambda e: 2 / FPS if CODECHECK else e
TASKS = [dict(name="rest", kind="free", end=end_(2.0)),
         dict(name="design", kind="design"),
         dict(name="kerb_full", kind="ride", road=KERB, v0=1.5, ctrl="full", end=end_(4.0)),
         dict(name="kerb_off", kind="ride", road=KERB, v0=1.5, ctrl="off", end=end_(4.0)),
         dict(name="resonant_full", kind="ride", road=RES, v0=1.0, ctrl="full", end=end_(8.0)),
         dict(name="bump25_full", kind="ride", road=B25, v0=1.0, ctrl="full", end=end_(8.0))]
if os.environ.get("ONLY"): TASKS = [t for t in TASKS if t["name"] in os.environ["ONLY"].split(",") + ["rest", "design"]]
summary = dict(generated=STAMP, device=jax.devices()[0].device_kind, jax=jax.__version__, fill=FILL, rho=RHO, fps=FPS, cart=C4.CART4,
               plant=dict(f0=C4.PLANT_F0, zeta=C4.PLANT_ZETA, beta=C4.PLANT_BETA), tasks=[])
WEIGHTS = None


def save_summary(): json.dump(summary, open(WORK / "summary.json", "w"), indent=1, default=float)


def make_advance16(S, cart, cfl=0.8, dtmax=0.002):
    """make_advance of stout_jax.py, ride branch, for the four-wheel cart: the probes read the surface the last step left; the cart is
    sub-stepped at 0.1 ms with the stout's push of the last step (in the glass's frame); the stout then steps with the glass's
    effective gravity g_eff = (g_x, g_z) in the glass's frame, averaged over the sub-steps (Cart4.forces)."""
    dx = S.dx

    def body(c):
        s, t, ex, st = c
        dt = jnp.minimum(jnp.minimum(dtmax, cfl * dx / jnp.maximum(ex["vmax"], 1e-6)), ex["t_end"] - t)
        prep = S.prepare(s)
        cs = dict(ex["cart"], py=S.probes(prep["H"]), pfresh=jnp.where(ex["probeOk"], 1.0, ex["cart"]["pfresh"]))
        nsub = jnp.maximum(1, jnp.round(dt / 1e-4).astype(I32)); hc = dt / nsub
        def sub(k, a):
            cc, gxs, gzs = a; cc = cart.step(cc, hc, ex["F"][0], ex["F"][1]); return (cc, gxs + cc["gx"], gzs + cc["gz"])
        cs, gxs, gzs = lax.fori_loop(0, nsub, sub, (cs, jnp.zeros((), F64), jnp.zeros((), F64)))
        gx, gz = gxs / nsub, gzs / nsub
        s, d = S.step(s, dt, gx, gz, prep=prep)
        P = d["mom"] * S.mp
        F = jnp.where(ex["haveP"], -(P - ex["P"]) / dt, 0.0)
        ex = dict(ex, cart=cs, P=P, F=jnp.stack([F[0], F[2]]), haveP=jnp.ones((), bool), vmax=d["vmax"].astype(F64),
                  imp=ex["imp"] + jnp.stack([F[0], F[2]]) * dt, probeOk=jnp.ones((), bool), gx=gx, gz=gz)
        st = dict(steps=st["steps"] + 1, its=st["its"] + d["it"], itmax=jnp.maximum(st["itmax"], d["it"]),
                  resmax=jnp.maximum(st["resmax"], d["res"].astype(F64)), nselmax=jnp.maximum(st["nselmax"], d["nsel"]))
        return s, t + dt, ex, st

    def advance(s, t, ex):
        st = dict(steps=jnp.zeros((), I32), its=jnp.zeros((), I32), itmax=jnp.zeros((), I32), resmax=jnp.zeros((), F64), nselmax=jnp.zeros((), I32))
        s, t, ex, st = lax.while_loop(lambda c: c[1] < c[2]["t_end"] - 1e-9, body, (s, t, ex, st))
        return S.resort(s), t, ex, st

    return jax.jit(advance)


def run_design():
    """The controller's weighting, chosen on the CPU with the validated few-mode stout on the kerb (modal4.py)."""
    global WEIGHTS
    import modal4, slosh_model as SM
    ws = json.load(open(os.path.join(os.path.dirname(os.path.abspath(SM.__file__)), "validation.json")))["ws_mm"] * 1e-3
    ml = SM.liquid_mass(); out = []
    cands = [dict(), dict(q=0.001), dict(q=0.00025), dict(q=0.0005, th=0.15, stroke=0.025), dict(q=0.0005, u=60.0)]
    if CODECHECK: cands = cands[:2]
    with jax.default_device(jax.devices("cpu")[0]):
        rt = road_table(ROADS[KERB], Rw=C4.CART4["Rw"], xmax=0.5 + 1.5 * 4.0 * 1.3 + 2)
        for wgt in cands:
            T1 = time.time(); cart = C4.Cart4({}, rt, 1.5, "full", weights=wgt); o = modal4.ride(cart, 1.0 if CODECHECK else 4.0, ml)
            sc = modal4.score(o, ws); sc.update(weights=wgt, slowest_pole=cart.D["slowest"], seconds=round(time.time() - T1, 1)); out.append(sc)
            log(f"  design {wgt}: head spilled {sc['head_spill_ml']:.2f} mL, wall {sc['wall_mm']:.2f} mm, tilt {sc['tilt_mm']:.2f} mm, pitch {sc['pitch_deg']:.1f} deg, "
                f"current {sc['i_max']:.1f} A, actuators {sc['u_max']:.1f} N, bump stop {sc['stop_N']:.0f} N, {sc['seconds']} s")
        cart = C4.Cart4({}, rt, 1.5, "off"); o = modal4.ride(cart, 1.0 if CODECHECK else 4.0, ml); off = modal4.score(o, ws)
        log(f"  design, control off: head spilled {off['head_spill_ml']:.2f} mL, wall {off['wall_mm']:.2f} mm, tilt {off['tilt_mm']:.2f} mm")
    best = min(out, key=lambda r: (round(r["head_spill_ml"], 2), r["wall_mm"]))
    WEIGHTS = best["weights"]
    json.dump(dict(candidates=out, off=off, chosen=WEIGHTS, ws_mm=ws * 1e3), open(WORK / "design.json", "w"), indent=1, default=float)
    summary["design"] = dict(chosen=WEIGHTS, candidates=out, off=off); save_summary()
    log(f"design: chosen weighting {WEIGHTS}")


measured = {}
for task in TASKS:
    name = task["name"]
    if task["kind"] == "design":
        run_design(); continue
    rate = measured.get(dx0) or (250.0 if not CODECHECK else 20.0)
    est = rate * task["end"] + 90
    if time.time() - T0 + est > BUDGET_S:
        log(f"skip {name}: needs about {est:.0f} s, {BUDGET_S - (time.time() - T0):.0f} s left in the budget"); continue
    log(f"start {name}: grid {dx0 * 1e3:.1f} mm, {task['end']:.3f} s of stout; about {est:.0f} s")
    G = Geometry(R, DZP, FILL, dx0); S = Stout(G, model="full", rho=RHO, head_mass=True)
    s = S.init_state(); t = jnp.zeros((), F64)
    ml = S.rho * S.V + S.rho_f * HEAD0 * float(np.sum(np.asarray(S.afill))) * S.dx ** 2
    if task["kind"] == "free":
        adv = make_advance(S, "free", push=(0.3, 0.0, 0.146)); ex = dict(vmax=jnp.zeros((), F64), t_end=jnp.zeros((), F64))
    else:
        rt = road_table(ROADS[task["road"]], Rw=C4.CART4["Rw"], xmax=0.5 + task["v0"] * max(task["end"], 1.0) * 1.3 + 2)
        cart = C4.Cart4({}, rt, task["v0"], task["ctrl"], weights=WEIGHTS)
        adv = make_advance16(S, cart)
        ex = dict(cart=cart.init(0.5, ml), P=jnp.zeros(3, F64), F=jnp.zeros(2, F64), haveP=jnp.ones((), bool), vmax=jnp.zeros((), F64),
                  imp=jnp.zeros(2, F64), t_end=jnp.zeros((), F64), probeOk=jnp.zeros((), bool), gx=jnp.zeros((), F64), gz=jnp.asarray(-9.81, F64))
    obs = jax.jit(S.observe); pol = jax.jit(S.polar)
    KC = ("x", "v", "zc", "th", "zf", "zr", "i", "icmd", "uf", "ur", "ufc", "urc", "Nf", "Nr", "Ff", "Fr", "Fdrive", "aeff", "py", "sat", "stopf", "stopr", "vzc", "om")
    rec = {k: [] for k in ("t", "H", "nfallback", "polar", "drops", "ndrops", "nfly", "nlanded", "nstuck", "nact", "KE", "PE", "Px", "ewall", "efoam", "eskin",
                           "hf", "lumps", "lumpvol", "foam_spill", "vhead", "steps", "its", "itmax", "resmax", "nselmax", "wall_s", "Fx", "Fz", "gx", "gz", "qh", "qhd") + KC}

    def record(s, t, ex, st, wall):
        o = obs(s); P = pol(o["H"])
        rec["t"].append(float(t)); rec["H"].append(np.asarray(o["H"])); rec["polar"].append(np.asarray(P))
        rec["drops"].append(np.asarray(o["drops"]).astype(np.float16))
        for k in ("nfallback", "ndrops", "nfly", "nlanded", "nstuck", "nact", "KE", "PE", "Px", "ewall", "efoam", "eskin", "foam_spill", "vhead"): rec[k].append(float(o[k]))
        rec["hf"].append(np.asarray(o["hf"]).astype(np.float16)); rec["lumps"].append(np.asarray(o["lumps"]).astype(np.float16))
        rec["lumpvol"].append(np.asarray(o["lumpvol"]).astype(np.float32))
        for k in ("steps", "its", "itmax", "resmax", "nselmax"): rec[k].append(float(st[k]) if st is not None else 0.0)
        rec["wall_s"].append(wall)
        if task["kind"] == "ride":
            c = ex["cart"]
            for k in KC: rec[k].append(float(c[k]))
            rec["qh"].append(float(c["qh"][0])); rec["qhd"].append(float(c["qh"][1]))
            rec["Fx"].append(float(ex["F"][0])); rec["Fz"].append(float(ex["F"][1])); rec["gx"].append(float(ex["gx"])); rec["gz"].append(float(ex["gz"]))

    record(s, t, ex, None, 0.0)
    Tc = time.time(); comp_s = None; Tlast = time.time(); steps = 0; its = 0; nf = int(round(task["end"] * FPS))
    for f in range(1, nf + 1):
        ex = dict(ex, t_end=jnp.asarray(f / FPS, F64))
        T1 = time.time(); s, t, ex, st = adv(s, t, ex); jax.block_until_ready(s["xp"]); w = time.time() - T1
        if comp_s is None: comp_s = w
        steps += int(st["steps"]); its += int(st["its"])
        record(s, t, ex, st, w)
        if int(st["nselmax"]) >= S.K: log(f"  STOP frame {f}: surface list full"); break
        if int(rec["ndrops"][-1]) >= S.M: log(f"  STOP frame {f}: drop list full"); break
        if not np.isfinite(rec["KE"][-1]) or rec["KE"][-1] > 10: log(f"  STOP: kinetic energy {rec['KE'][-1]} J at t = {float(t):.3f} s"); break
        if task["kind"] == "ride" and not np.isfinite(rec["x"][-1]): log("  STOP: the cart's state is not finite"); break
        if time.time() - Tlast > 60:
            Tlast = time.time(); el = Tlast - Tc - comp_s
            log(f"  {float(t):.2f} of {task['end']} s; {steps:,} steps; {el / max(steps - int(st['steps']), 1) * 1e3:.0f} ms a step; "
                f"head spilled {rec['foam_spill'][-1] * 1e6:.2f} mL; stout spilled {S.N - rec['nact'][-1]:,} particles")
    wall = time.time() - Tc; run_s = wall - comp_s; measured[dx0] = run_s / max(float(t) - 1 / FPS, 1e-6)
    out = {k: np.array(v) for k, v in rec.items() if len(v)}
    np.savez_compressed(WORK / f"{name}.npz", **out, dx=dx0, fill=FILL, x0=G.x0, n=G.n, Rfill=G.Rfill, mp=S.mp, N=S.N)
    foam0 = float(np.asarray(S.init_state()["foam0"])); nsum = out["nact"] + out["nfly"] + out["nlanded"] + out["nstuck"]
    info = dict(task, cells=G.n * G.n * G.nz, particles=S.N, mp=S.mp, steps=steps, compile_s=round(comp_s, 1), run_s=round(run_s, 1),
                ms_per_step=round(run_s / max(steps - 1, 1) * 1e3, 1), its_per_step=round(its / max(steps, 1), 1), itmax=int(out["itmax"].max()),
                spilled_g=round((S.N - out["nact"][-1]) * S.mp * 1e3, 3), head_spilled_ml=round(float(out["foam_spill"][-1]) * 1e6, 3), dx=dx0,
                books=dict(stout_particles=S.N, stout_err_particles_max=int(np.abs(nsum - S.N).max()), head_ml0=round(foam0 * 1e6, 4),
                           head_glass_ml_end=round(float(out["vhead"][-1]) * 1e6, 4), head_off_ml_end=round(float(out["foam_spill"][-1]) * 1e6, 4),
                           head_err_ml_max=float(np.abs(out["vhead"] + out["foam_spill"] - foam0).max() * 1e6)))
    pol_arr = out["polar"]
    if task["kind"] == "ride":
        th = 2 * np.pi * np.arange(pol_arr.shape[2]) / pol_arr.shape[2]
        tilt = 2 * (2 / len(th)) * (pol_arr[:, 16] * np.cos(th)).sum(1) * 1e3
        info.update(tilt_max_mm_run=float(np.nanmax(np.abs(tilt))), v_range=[float(out["v"].min()), float(out["v"].max())],
                    pitch_max_deg=float(np.degrees(np.abs(out["th"] - out["th"][0]).max())), i_max_A=float(np.abs(out["i"]).max()),
                    u_max_N=float(max(np.abs(out["uf"]).max(), np.abs(out["ur"]).max())), current_limited=bool(out["sat"].max() > 0),
                    bump_stop_N=float(max(out["stopf"].max(), out["stopr"].max())), weights=WEIGHTS if task["ctrl"] == "full" else None,
                    gains=dict(K=np.asarray(cart.K).tolist(), poles_max_abs=cart.D["slowest"]),
                    impulse_vs_momentum=dict(impulse_x=float(np.asarray(ex["imp"][0])), momentum_x_end=float(np.asarray(ex["P"][0]))))
    if name == "rest":
        inside = np.hypot(*np.meshgrid(G.x0 + (np.arange(G.n) + 0.5) * dx0, G.x0 + (np.arange(G.n) + 0.5) * dx0, indexing="ij")) < G.Rfill - dx0
        Hl = out["H"][-1][inside]; devc = np.abs(Hl - FILL) * 1e3
        g_ = dict(max_dev_mm=float(np.nanmax(devc)), rms_dev_mm=float(np.sqrt(np.nanmean(devc ** 2))), columns_without_value=int((~np.isfinite(Hl)).sum()),
                  head_spilled_ml=info["head_spilled_ml"], spilled_g=info["spilled_g"], limit_max_mm=REST_MAX_CELLS * dx0 * 1e3, limit_rms_mm=REST_RMS_CELLS * dx0 * 1e3)
        info["rest_guard"] = g_
        ok = g_["max_dev_mm"] < g_["limit_max_mm"] and g_["rms_dev_mm"] < g_["limit_rms_mm"] and g_["columns_without_value"] == 0 and g_["head_spilled_ml"] == 0 and g_["spilled_g"] == 0
        log(f"rest guard: {'PASS' if ok else 'FAIL'} {g_}")
        summary["tasks"].append(info); save_summary()
        if not ok and not CODECHECK: log("STOP: the pint at rest is not flat and full; no ride is computed"); raise SystemExit(0)
        continue
    summary["tasks"].append(info); save_summary()
    log(f"done {name}: {steps:,} steps, compile {comp_s:.0f} s, {info['ms_per_step']} ms a step; head spilled {info['head_spilled_ml']} mL, stout spilled "
        f"{info['spilled_g']} g; books: {info['books']['stout_err_particles_max']} particles, head {info['books']['head_err_ml_max']:.1e} mL"
        + (f"; tilt {info['tilt_max_mm_run']:.2f} mm, pitch {info['pitch_max_deg']:.1f} deg, current {info['i_max_A']:.2f} A, actuators {info['u_max_N']:.1f} N" if task["kind"] == "ride" else ""))
log("all done")
