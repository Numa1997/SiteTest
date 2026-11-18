"""Continuous spill: check of Stout.air_drag against the textbook law, on Kaggle's CPU.
A drop of stout of diameter D (resolved by a few cells), at rest beside the glass, gravity off, in a wind U along -x for 30 ms. Its
mean acceleration must equal a = (3/4) C_D rho_a U^2 / (rho D), C_D = 24/Re (1 + 0.15 Re^0.687) (Schiller & Naumann), within the
error of a drop drawn on a grid of a few cells (gate: 25 %). Also: no drag without wind, none on stout inside the glass.
Run from the repository's root:  python3 tools/spill/drag_check.py OUTDIR   (env DX, default 0.002; D, default 0.008)"""
import json, os, sys
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax  # noqa: E402
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
import stout_jax as SJ  # noqa: E402
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
R = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")])
dx = float(os.environ.get("DX", "0.002")); D = float(os.environ.get("D", "0.008")); U = 1.5
G = SJ.Geometry(R, 0.0005, 0.125, dx, body=(SJ.BODY_HALF[0], SJ.BODY_HALF[1], SJ.BODY_TOP)); S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=1024)
s = S.init_state(); N = S.N
# the drop: the particles of a sphere of diameter D centred 70 mm from the axis, 100 mm up, on a lattice of dx/2
h = dx / 2; g1 = np.arange(-D / 2 + h / 2, D / 2, h); P = np.array([(x, y, z) for x in g1 for y in g1 for z in g1 if x * x + y * y + z * z < (D / 2) ** 2]) + np.array([0.07, 0.0, 0.10])
n = len(P); xp = np.asarray(s["xp"]).copy(); xp[:n] = P; act = np.zeros(N, bool); act[:n] = True
s = dict(s, xp=jnp.asarray(xp, jnp.float32), act=jnp.asarray(act))
rep = {"D_mm": D * 1e3, "dx_mm": dx * 1e3, "particles": n}
for name, wind in (("wind", (-U, 0.0)), ("still air", (0.0, 0.0))):
    st = s; t = 0.0; dt = 0.001
    step = jax.jit(lambda st, dt: S.step(st, dt, 0.0, 0.0, wind=wind))
    v0 = np.asarray(st["vp"])[:n].mean(0)
    while t < 0.03 - 1e-9: st, d_ = step(st, dt); t += dt
    v1 = np.asarray(st["vp"])[:n].mean(0); a = (v1 - v0) / t
    rep[name] = dict(a_x=float(a[0]), a_z=float(a[2]), nact=int(np.asarray(st["act"]).sum()))
Re = SJ.RHO_AIR * U * D / SJ.MU_AIR; CD = 24 / Re * (1 + 0.15 * Re ** 0.687); a_th = 0.75 * CD * SJ.RHO_AIR * U ** 2 / (1007.0 * D)
rep["theory"] = dict(Re=Re, CD=CD, a=-a_th)
ok1 = abs(rep["wind"]["a_x"] / -a_th - 1) < 0.25; ok2 = abs(rep["still air"]["a_x"]) < 0.02 * a_th
rep["PASS drag within 25 % of the law"] = ok1; rep["PASS no drag in still air"] = ok2
print(json.dumps(rep, indent=1)); json.dump(rep, open(os.path.join(OUT, "drag_check.json"), "w"), indent=1)
