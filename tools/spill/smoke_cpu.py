"""Continuous spill (notes/spill/STATE.md): smoke test of stout_jax.py's continuous model on Kaggle's CPU, on a coarse grid.
Run from the repository's root in a Kaggle notebook:  python3 tools/spill/smoke_cpu.py OUTDIR
Checks, each printed PASS or FAIL, and OUTDIR/smoke.json:
  1. the old geometry (body None) is unchanged: open fractions and wall areas equal to main's stout_jax.py bit for bit;
  2. the continuous geometry: the solids where they belong (glass wall, foot, deck), open air around them, the wall area of the
     glass's outside near 2 pi R per unit height;
  3. a pint at rest for 0.3 s (dx 4 mm): no particle leaves the cavity, none lost, the surface stays level;
  4. a hard sideways shove (5 g for 0.15 s, then free): stout goes over the rim, runs down the outside, lands on the body;
     the books close (particles in the computation + particles fallen off = N), nothing NaN, speeds bounded."""
import importlib.util, json, math, os, sys, time
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax  # noqa: E402
jax.config.update("jax_enable_x64", True)
import stout_jax as SJ  # noqa: E402

rep = {}; log = open(os.path.join(OUT, "smoke.log"), "w")
def say(m): print(m, flush=True); log.write(m + "\n"); log.flush()
def check(name, ok, info=""):
    rep[name] = dict(ok=bool(ok), info=info); say(f"{'PASS' if ok else 'FAIL'}  {name}  {info}")

js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
R = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); DZP = 0.0005; FILL = 0.125

# 1. old geometry unchanged
old_path = os.environ.get("OLD_SOLVER")
if old_path and os.path.exists(old_path):
    spec = importlib.util.spec_from_file_location("old_sj", old_path); OS = importlib.util.module_from_spec(spec); spec.loader.exec_module(OS)
    a, b = OS.Geometry(R, DZP, FILL, 0.004), SJ.Geometry(R, DZP, FILL, 0.004)
    same = all(np.array_equal(getattr(a, k), getattr(b, k)) for k in ("thu", "thv", "thw", "ac", "au", "av", "aw", "cav_inner", "wallcut", "cavc"))
    check("old geometry unchanged", same, f"n {a.n}={b.n}, nz {a.nz}={b.nz}")
else:
    check("old geometry unchanged", False, "OLD_SOLVER not given")

# 2. continuous geometry
dx = float(os.environ.get("DX", "0.004")); REST = float(os.environ.get("REST", "2.0")); body = (SJ.BODY_HALF[0], SJ.BODY_HALF[1], SJ.BODY_TOP)
t0 = time.time(); G = SJ.Geometry(R, DZP, FILL, dx, body=body); say(f"continuous geometry: n {G.n}, nz {G.nz}, {G.n * G.n * G.nz} cells, built in {time.time() - t0:.1f} s")
pts = {"in the cavity": (0, 0, 0.05, False), "in the glass wall": (float(G.Rz(0.08)) + 0.001, 0, 0.08, True),
       "outside the glass": (float(G.Rz(0.08)) + 0.006, 0, 0.08, False), "in the foot": (0, 0, -0.007, True),
       "the body": (0.09, 0.0, SJ.BODY_TOP - 0.002, True), "air beside the body": (0, 0.09, SJ.BODY_TOP - 0.002, False)}
ok = all(bool(G.solid(np.array(x), np.array(y), np.array(z))) == want for (x, y, z, want) in pts.values())
check("solids where they belong", ok, json.dumps({k: bool(G.solid(np.array(v[0]), np.array(v[1]), np.array(v[2]))) for k, v in pts.items()}))
k = int((0.08 - G.z0) / dx); Aout = 2 * math.pi * (float(G.Rz(0.08)) + G.WALL) * dx; Ain = 2 * math.pi * float(G.Rz(0.08)) * dx
layer = G.ac[:, :, k].sum() * dx ** 3
check("wall area of one layer near 2 pi (R_in + R_out) dx", abs(layer / (Aout + Ain) - 1) < 0.25, f"{layer * 1e6:.1f} vs {(Aout + Ain) * 1e6:.1f} mm^2")

# 3. a pint at rest
S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096); s = S.init_state(); N = S.N
step = jax.jit(lambda s, dt, gx, gz: S.step(s, dt, gx, gz))
t = 0.0; dt = 0.002
while t < REST - 1e-9: s, d = step(s, dt, 0.0, -9.81); t += dt
o = S.observe(s); H = np.asarray(o["H"]); Hc = H[np.isfinite(H)]
check("at rest: none lost, none outside", int(o["nact"]) == N and int(o["nfly"]) == 0, f"active {int(o['nact'])}/{N}, outside {int(o['nfly'])}")
check("at rest: surface at the fill, level within 0.5 mm", Hc.size > 0 and Hc.max() - Hc.min() < 0.0005 and abs(np.median(Hc) - 0.125) < 0.001, f"H {Hc.min() * 1e3:.2f}..{Hc.max() * 1e3:.2f} mm, median {np.median(Hc) * 1e3:.2f}")

# 4. a hard shove
hist = []
while t < REST + 1.2 - 1e-9:
    gx = 5 * 9.81 if t < REST + 0.15 else 0.0
    s, d = step(s, dt, gx, -9.81); t += dt
    if abs(t / 0.05 - round(t / 0.05)) < 1e-6:
        o = S.observe(s); X = np.asarray(s["xp"]); act = np.asarray(s["act"])
        hist.append(dict(t=round(t, 3), active=int(o["nact"]), outside=int(o["nfly"]), fallen=int(o["nlanded"]),
                         on_body=int(np.sum(act & (X[:, 2] < SJ.BODY_TOP + 2 * dx))), vmax=float(d["vmax"]), it=int(d["it"])))
        say(json.dumps(hist[-1]))
fin = hist[-1]; Xf = np.asarray(s["xp"])
check("shove: stout went over the rim and down the outside", max(h["outside"] for h in hist) > 0, f"max outside {max(h['outside'] for h in hist)}")
check("shove: books close (active + fallen = N)", fin["active"] + fin["fallen"] == N, f"{fin['active']} + {fin['fallen']} = {N}")
check("shove: no NaN, speeds bounded", np.isfinite(Xf).all() and max(h["vmax"] for h in hist) < 10.0, f"vmax {max(h['vmax'] for h in hist):.2f} m/s")
check("shove: some stout on the body", max(h["on_body"] for h in hist) > 0, f"max on body {max(h['on_body'] for h in hist)}")
rep["history"] = hist
json.dump(rep, open(os.path.join(OUT, "smoke.json"), "w"), indent=1)
fails = [k for k, v in rep.items() if isinstance(v, dict) and not v.get("ok", True)]
say(f"done: {len(fails)} FAIL {fails}")
