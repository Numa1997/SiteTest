"""Fig. 12's solver on Kaggle's GPU: the numerical damping of the method at the production grid (1.5 mm) and finer (1.0 mm)
(notes/guinness-rebuild/audit.md item F). The stout alone, no friction, no head (model "inviscid", so every loss is the method's),
pushed along x by 1 m/s^2 for 0.146 s after 0.3 s, then left to swing for 2.5 s; the swing is the cos(theta) part of ring 13 of the
stored surface, fitted with run_b.py's own fit_swing. 07-diagnosis.md measured 0.0782 (6 mm), 0.0433 (4.5 mm), 0.0254 (3 mm) on the
CPU and extrapolated 0.006 to 0.010 at 1.5 mm. Writes /kaggle/working/damping/damping.json and progress.log.
Environment: GLASS_JSON, CODECHECK (6 mm, 0.4 s: the smoke test)."""
import os, json, time, math, datetime
from pathlib import Path
import numpy as np
import jax, jax.numpy as jnp
from stout_jax import Geometry, Stout, make_advance, F64

R = json.load(open(os.environ["GLASS_JSON"]))["R"]; FILL = 0.125; FPS = 60
CODECHECK = bool(os.environ.get("CODECHECK"))
WORK = Path("/kaggle/working/damping"); WORK.mkdir(parents=True, exist_ok=True); T0 = time.time()
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_b.py")).read()
_a = _src.index("def fit_swing"); _b = _src.index("\n\n\n", _a); exec(_src[_a:_b])        # run_b.py's fit_swing, unchanged


def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc):%H:%M:%S} UTC {(time.time() - T0) / 60:5.1f} min  {msg}"
    print(line, flush=True); open(WORK / "progress.log", "a").write(line + "\n")


GRIDS = [0.006] if CODECHECK else [0.0015, 0.0010]
END = 0.4 if CODECHECK else 2.9
out = dict(model="inviscid", push=(0.3, 1.0, 0.146), fps=FPS, runs=[])
for dx in GRIDS:
    G = Geometry(R, 0.0005, FILL, dx); S = Stout(G, model="inviscid")
    s = S.init_state(); t = jnp.zeros((), F64)
    adv = make_advance(S, "free", push=(0.3, 1.0, 0.146)); ex = dict(vmax=jnp.zeros((), F64), t_end=jnp.zeros((), F64))
    pol = jax.jit(S.polar); obs = jax.jit(S.observe)
    log(f"start dx {dx * 1e3:.1f} mm: {S.N:,} particles, grid {G.n} x {G.n} x {G.nz}")
    ts, q13, steps = [], [], 0; Tc = time.time()
    for f in range(1, int(round(END * FPS)) + 1):
        ex = dict(ex, t_end=jnp.asarray(f / FPS, F64)); s, t, ex, st = adv(s, t, ex); steps += int(st["steps"])
        P = np.asarray(pol(obs(s)["H"])); th = 2 * np.pi * np.arange(P.shape[1]) / P.shape[1]
        ts.append(float(t)); q13.append(float(2 / len(th) * (P[13] * np.cos(th)).sum()))
        if f % 30 == 0: log(f"  {float(t):.2f} s, {steps:,} steps, {(time.time() - Tc) / steps * 1e3:.0f} ms a step")
    ts, q13 = np.array(ts), np.array(q13); m = ts > 0.3 + 0.146 + 0.1
    F = fit_swing(ts[m] - ts[m][0], q13[m]) if m.sum() > 30 else {}
    run = dict(dx_mm=dx * 1e3, particles=S.N, steps=steps, ms_per_step=round((time.time() - Tc) / max(steps, 1) * 1e3, 1), fit_ring13=F, t=ts.tolist(), q13_mm=(q13 * 1e3).tolist())
    out["runs"].append(run); json.dump(out, open(WORK / "damping.json", "w"))
    log(f"done dx {dx * 1e3:.1f} mm: zeta {F.get('zeta')}, f0 {F.get('f0')} Hz, amplitude {F.get('A_mm')} mm, fit rms {F.get('rms_mm')} mm")
log("all done")
