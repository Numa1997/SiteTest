"""Continuous spill: which difference makes the pint at rest sink on Fig. 16's set-up (19 Nov 2026, GPU checks 2 and 3: the read
surface fell 9.6 mm in 0.3 s while no stout was lost; the 2 mm smoke test with Fig. 12's body and the "wall" model had held it).
Runs the pint at rest for REST seconds (default 0.3) with the glass held still, gx = 0, gz = -9.81, dt = 2 ms (as smoke_cpu.py), for:
  A  Fig. 12's body (0.11, 0.06, -0.014), model "wall"   (the set-up that passed, now on the rectangular grid)
  B  Fig. 12's body, model "full" (head, skin)
  C  Fig. 16's deck (0.155, 0.062, -0.030), model "wall"
  D  Fig. 16's deck, model "full"
  E  old model (no body), model "full"                    (the baseline every stored ride used)
  F  as D with the surface tension off
and prints, at the end: the median read surface, its range, the particles' mean height (at the start and end), particles below the
cavity floor and outside the cavity, active particles. Kaggle (GPU or CPU); nothing runs outside Kaggle.
Run from the repository's root:  python3 tools/spill/rest_variants.py OUTDIR   (env DX default 0.002, REST default 0.3, ONLY e.g. "A,D")"""
import json, os, sys, time
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax  # noqa: E402
import stout_jax as SJ  # noqa: E402
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
R = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")])
DZP, FILL = 0.0005, 0.125
dx = float(os.environ.get("DX", "0.002")); REST = float(os.environ.get("REST", "0.3"))
F12 = (SJ.BODY_HALF[0], SJ.BODY_HALF[1], SJ.BODY_TOP); F16 = (0.155, 0.062, -0.030)
CASES = dict(A=(F12, "wall"), B=(F12, "full"), C=(F16, "wall"), D=(F16, "full"), E=(None, "full"),
             F=(F16, "full", "no tension"))      # F: D with the surface tension switched off (19 Nov 2026: is it what settles the pint?)
only = os.environ.get("ONLY"); rep = {"dx_mm": dx * 1e3, "rest_s": REST, "device": str(jax.devices()[0])}
for key, case in CASES.items():
    body, model = case[0], case[1]
    if only and key not in only.split(","): continue
    t0 = time.time()
    G = SJ.Geometry(R, DZP, FILL, dx, body=body)
    S = SJ.Stout(G, model=model, K_frac=1.0 if body else 0.62, M_drops=4096); S.gamma = 0.0 if len(case) > 2 else S.gamma; s = S.init_state(); N = S.N
    step = jax.jit(lambda s, dt, gx, gz: S.step(s, dt, gx, gz))
    z0 = float(np.asarray(s["xp"])[:, 2].mean()); t = 0.0; dt = 0.002
    while t < REST - 1e-9: s, d = step(s, dt, 0.0, -9.81); t += dt
    o = S.observe(s); H = np.asarray(o["H"]); Hc = H[np.isfinite(H)]
    X = np.asarray(s["xp"]); act = np.asarray(s["act"]); rr = np.hypot(X[:, 0], X[:, 1])
    Rr = np.interp(np.clip(X[:, 2], 0, G.zrim) / DZP, np.arange(len(R)), R)
    r = dict(body=body, model=model, grid=[G.nx, G.ny, G.nz], particles=N, active=int(act.sum()),
             surface_median_mm=round(float(np.median(Hc)) * 1e3, 2), surface_range_mm=[round(float(Hc.min()) * 1e3, 2), round(float(Hc.max()) * 1e3, 2)],
             mean_z_mm=[round(z0 * 1e3, 2), round(float(X[act, 2].mean()) * 1e3, 2)], below_floor=int((act & (X[:, 2] < 0)).sum()),
             outside_cavity=int((act & ~((X[:, 2] > 0) & (rr < Rr))).sum()), wall_s=round(time.time() - t0, 1))
    rep[key] = r; print(key, json.dumps(r), flush=True)
json.dump(rep, open(os.path.join(OUT, "rest_variants.json"), "w"), indent=1, default=str)
