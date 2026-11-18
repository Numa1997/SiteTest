"""Continuous spill: why the pint at rest fails in smoke_cpu.py (surface read 23-28 mm instead of 125 mm on the 4 mm grid).
Runs the pint at rest for 0.3 s in three set-ups and prints, every 0.05 s: the particles' mean and top height, the surface read
(min, max), pressure iterations, particles outside the cavity. Set-ups: A old geometry (body None) in the new code; B the
continuous geometry without surface tension; C the continuous geometry with it. Kaggle CPU:  python3 tools/spill/rest_diag.py OUT"""
import json, os, sys
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax  # noqa: E402
jax.config.update("jax_enable_x64", True)
import stout_jax as SJ  # noqa: E402
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
R = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")])
DX = float(os.environ.get("DX", "0.004")); res = {}
for name, body, gam in (("A old geometry", None, None), ("B continuous, no tension", (0.11, 0.06, SJ.BODY_TOP), 0.0), ("C continuous, tension", (0.11, 0.06, SJ.BODY_TOP), None)):
    G = SJ.Geometry(R, 0.0005, 0.125, DX, body=body); S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096)
    if gam is not None: S.gamma = gam
    s = S.init_state(); step = jax.jit(lambda s, dt: S.step(s, dt, 0.0, -9.81)); t = 0.0; rows = []
    z0 = np.asarray(s["xp"])[:, 2]; rows.append(dict(t=0.0, zmean=float(z0.mean() * 1e3), ztop=float(np.percentile(z0, 99.9) * 1e3)))
    while t < 0.3 - 1e-9:
        s, d = step(s, 0.002); t += 0.002
        if abs(t / 0.05 - round(t / 0.05)) < 1e-6:
            o = S.observe(s); H = np.asarray(o["H"]); Hc = H[np.isfinite(H)]; z = np.asarray(s["xp"])[:, 2][np.asarray(s["act"])]
            rows.append(dict(t=round(t, 3), zmean=float(z.mean() * 1e3), ztop=float(np.percentile(z, 99.9) * 1e3), Hmin=float(Hc.min() * 1e3) if Hc.size else None,
                             Hmax=float(Hc.max() * 1e3) if Hc.size else None, ncol=int(Hc.size), it=int(d["it"]), res=float(d["res"]), outside=int(o["nfly"]), nact=int(o["nact"])))
    res[name] = rows; print(name); [print(" ", json.dumps(r)) for r in rows]
json.dump(res, open(os.path.join(OUT, "rest_diag.json"), "w"), indent=1)
