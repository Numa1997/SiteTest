"""Fig. 12 in JAX: pack one ride computed on Kaggle (a .npz written by run_b.py) into the page's file, public/data/fig12/<date>/<name>.json.
Nothing is computed here: the arrays are rounded to the stated steps, packed and written; index.json lists each file with its SHA-256.

The file (JSON): the cart's lists per stored frame, and four packed blocks (base64 of zlib):
  H    int16 [frames][n][n]  the stout's surface in each column of the solver's grid, in steps of qH above the glass's inner floor
                             (-32768: no stout in that column), stored as differences from the frame before (first frame as is)
  hf   uint8 [frames][n][n]  thickness of the head of foam on that column, in steps of qhf
  drops int16 [sum nd][3]    the drops of stout in the air in each frame (nd[frame] of them), x, y, z in the glass's frame, steps of qd
  lumps int16 [sum nl][4]    the lumps of head in the air (nl[frame] of them): x, y, z in steps of qd, volume in steps of qv
Run: python3 tools/fig12/kaggle/pack_ride.py <ride.npz> <summary.json> <task name> <date> <notebook version> <commit>"""
import base64, hashlib, json, os, sys, zlib
import numpy as np

src, summary_path, name, date, version, commit = sys.argv[1:7]
here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.normpath(os.path.join(here, "..", "..", "..", "public", "data", "fig12", date)); os.makedirs(out_dir, exist_ok=True)
Z = np.load(src); S = json.load(open(summary_path)); task = next(t for t in S["tasks"] if t["name"] == name)
QH, QHF, QD, QV = 2e-5, 1e-4, 1e-4, 1e-10          # m, m, m, m^3 (0.1 mm^3)
pk = lambda a: base64.b64encode(zlib.compress(np.ascontiguousarray(a).tobytes(), 9)).decode()

H = Z["H"].astype(np.float64); nf, n, _ = H.shape
Hq = np.where(np.isfinite(H), np.clip(np.round(H / QH), -32767, 32767), -32768).astype(np.int16)
Hd = Hq.copy(); Hd[1:] = (Hq[1:].astype(np.int32) - Hq[:-1].astype(np.int32)).astype(np.int16)      # wraps modulo 2^16, undone by a running sum
hf = np.clip(np.round(Z["hf"].astype(np.float64) / QHF), 0, 255).astype(np.uint8)


def cloud(arr, extra=None):
    """Rows of arr[frame] with a finite z, as int16 in steps of QD; returns the per-frame counts and the packed rows."""
    counts, rows = [], []
    for f in range(nf):
        a = arr[f].astype(np.float64); ok = np.isfinite(a[:, 2]) & (a[:, 2] > -0.25)
        if extra is not None: ok &= extra[f] > 0
        q = np.clip(np.round(a[ok] / QD), -32767, 32767)
        if extra is not None: q = np.concatenate([q, np.clip(np.round(extra[f][ok] / QV), 0, 32767)[:, None]], 1)
        counts.append(int(ok.sum())); rows.append(q.astype(np.int16))
    return counts, (np.concatenate(rows) if rows else np.zeros((0, 3), np.int16))


nd, drops = cloud(Z["drops"]); nl, lumps = cloud(Z["lumps"], Z["lumpvol"])
r5 = lambda a, k: [round(float(v), k) for v in a]
out = dict(name=name, generated=date, n=int(n), frames=int(nf), fps=30, dx=float(Z["dx"]), x0=float(Z["x0"]), fill=float(Z["fill"]),
           qH=QH, qhf=QHF, qd=QD, qv=QV, t=r5(Z["t"], 4),
           mp=float(Z["mp"]), particles=int(Z["N"]), stout_g=r5(Z["nact"] * float(Z["mp"]) * 1e3, 2),
           spill_g=r5((int(Z["N"]) - Z["nact"]) * float(Z["mp"]) * 1e3, 2), head_spill_ml=r5(Z["foam_spill"] * 1e6, 3),
           head=task.get("head"), head_ml=task.get("head_ml"), task={k: task[k] for k in ("kind", "model", "dx", "end") if k in task},
           nd=nd, nl=nl, H=pk(Hd), hf=pk(hf), drops=pk(drops), lumps=pk(lumps))
if "x" in Z.files:
    src_run = open(os.path.join(here, "run_b.py")).read(); a = src_run.index("ROADS = {"); b = src_run.index("\n}\n", a) + 2
    ROADS = eval(src_run[a + len("ROADS = "):b])            # the roads as run_b.py defines them (cosine bumps: centre x, height h, length L)
    out.update(bumps=ROADS[task["road"]]["bumps"], v0=task.get("v0"), road=task.get("road"), x=r5(Z["x"], 5), v=r5(Z["v"], 4), zb=r5(Z["zb"], 6), zw=r5(Z["zw"], 6),
               i=r5(Z["i"], 4), Fx=r5(Z["Fx"], 4), Fz=r5(Z["Fz"], 4), ctrl=task.get("ctrl", "speed"))
    for k, nd_ in (("icmd", 4), ("us", 3), ("qhat", 6), ("yq", 6), ("ipar", 4)):   # the controller's signals (run 7 on)
        if k in Z.files and len(Z[k]) == nf: out[k] = r5(Z[k], nd_)
dst = os.path.join(out_dir, name + ".json")
json.dump(out, open(dst, "w"), separators=(",", ":"))
b = open(dst, "rb").read(); sha = hashlib.sha256(b).hexdigest()
idx_path = os.path.join(out_dir, "index-jax.json")
idx = json.load(open(idx_path)) if os.path.exists(idx_path) else dict(
    about="Fig. 12 computed in JAX on Kaggle's GPU: the stout, its head of foam and the cart, one file per ride.", generated=date,
    kaggle=dict(notebook="numakoudsie/guinness-on-a-cart-stout-in-jax", url="https://www.kaggle.com/code/numakoudsie/guinness-on-a-cart-stout-in-jax",
                version=int(version), machine=S.get("device")), code=f"tools/fig12/kaggle/stout_jax.py and run_b.py at SiteTest commit {commit}", files=[])
CTRL_LABEL = {"speed": "speed held only", "preview": "road preview", "slosh": "slosh LQR", "joint": "joint control"}
label = (f"{task['road'][0].upper()}{task['road'][1:]}, {task['v0']:.1f} m/s · {CTRL_LABEL[task.get('ctrl', 'speed')]}" if task["kind"] == "ride"
         else ("Standing still, one push" if task["push"][1] > 0 else "Standing still") + ("" if task["model"] == "full" else ", no head"))
idx["files"] = [f for f in idx["files"] if f["path"] != name + ".json"] + [dict(
    path=name + ".json", label=label, kind=task["kind"], default=(name == "ride_resonant_joint"), bytes=len(b), sha256=sha, frames=int(nf), seconds=round((nf - 1) / 30, 3),
    road=task.get("road"), v0=task.get("v0"), ctrl=task.get("ctrl", "speed") if task["kind"] == "ride" else None, kaggle_version=int(version), commit=commit,
    measured=dict({k: task.get(k) for k in ("steps", "ms_per_step", "its_per_step", "run_s", "cells", "particles", "spilled_g", "head_spilled_ml", "lean_max_mm", "control")},
                  i_max_stored_A=(round(float(np.abs(Z["i"]).max()), 3) if "i" in Z.files else None)))]
idx["files"].sort(key=lambda f: (f["kind"] != "ride", f["path"]))
json.dump(idx, open(idx_path, "w"), indent=1)
print(dst, len(b), sha)
