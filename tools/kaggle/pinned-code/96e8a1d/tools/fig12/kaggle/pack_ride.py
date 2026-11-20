"""Fig. 12 in JAX: pack one ride computed on Kaggle (a .npz written by run_b.py) into the page's file, public/data/fig12/<date>/<name>.json.
Nothing is computed here: the arrays are rounded to the stated steps, packed and written; index.json lists each file with its SHA-256.

The file (JSON): the cart's lists per stored frame, and four packed blocks (base64 of zlib):
  H    int16 [frames][n][n]  the stout's surface in each column of the solver's grid, in steps of qH above the glass's inner floor
                             (-32768: no stout in that column), stored as differences from the frame before (first frame as is)
  hf   uint8 [frames][n][n]  thickness of the head of foam on that column, in steps of qhf
  drops int16 [sum nd][3]    the drops of stout in the air in each frame (nd[frame] of them), x, y, z in the glass's frame, steps of qd
  lumps int16 [sum nl][4]    the lumps of head in the air (nl[frame] of them): x, y, z in steps of qd, volume in steps of qv
Run: python3 tools/fig12/kaggle/pack_ride.py <ride.npz> <summary.json> <task name> <data folder> <notebook version> <commit>
(data folder: the folder under public/data/fig12/, e.g. 2026-11-13 for runs 6 and 7, 2026-11-14-run8 for run 8)"""
import base64, hashlib, json, os, sys, zlib
import numpy as np

src, summary_path, name, date, version, commit = sys.argv[1:7]
here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.normpath(os.path.join(here, "..", "..", "..", "public", "data", "fig12", date)); os.makedirs(out_dir, exist_ok=True)
Z = np.load(src); S = json.load(open(summary_path)); task = next(t for t in S["tasks"] if t["name"] == name)
QH, QHF, QD, QV = 2e-5, 1e-4, 1e-4, 1e-10          # m, m, m, m^3 (0.1 mm^3)
pk = lambda a: base64.b64encode(zlib.compress(np.ascontiguousarray(a).tobytes(), 9)).decode()

H = Z["H"].astype(np.float64); nf, n, _ = H.shape
# Only the columns the run's rest guard trusts are stored for the page: those whose centre lies more than one cell inside the
# glass at the fill (r < R_fill - dx). The columns at the glass are cut by it; some read their surface far too low (run 7's
# controlled 25 mm bump: one column at x = 39.0 mm read 6.65 mm low at 5.83 s, and the two-point lean took it up). Leaving
# them out, the page draws the surface from the trusted columns out to the glass, and every reading below uses the same set.
DXc, X0c, RF = float(Z["dx"]), float(Z["x0"]), float(Z["Rfill"])
cc_ = X0c + (np.arange(n) + 0.5) * DXc; RC = np.hypot(*np.meshgrid(cc_, cc_, indexing="ij"))
H = np.where(np.isfinite(H) & (RC < RF - DXc)[None], H, np.nan)


def ring(Hs, r, th):
    """The stored surface at radius r and angle th in every frame, read as the page reads it (StoutRide.at and atInward of
    stout-view2.js): bilinear over the four columns around the point, leaving out columns without a value, stepping inward
    by half a cell until one has a value."""
    out = np.full(Hs.shape[0], np.nan); q = r
    while q > 0 and np.isnan(out).any():
        fx = (q * np.cos(th) - X0c) / DXc - 0.5; fy = (q * np.sin(th) - X0c) / DXc - 0.5
        i, j = int(np.floor(fx)), int(np.floor(fy)); tx, ty = fx - i, fy - j; num = np.zeros(Hs.shape[0]); den = np.zeros(Hs.shape[0])
        for a, b_, w in ((0, 0, (1 - tx) * (1 - ty)), (1, 0, tx * (1 - ty)), (0, 1, (1 - tx) * ty), (1, 1, tx * ty)):
            ii, jj = i + a, j + b_
            if 0 <= ii < n and 0 <= jj < n:
                v = Hs[:, ii, jj]; ok = np.isfinite(v); num += np.where(ok, w * np.nan_to_num(v), 0.0); den += np.where(ok, w, 0.0)
        val = np.where(den > 1e-6, num / np.maximum(den, 1e-12), np.nan); out = np.where(np.isnan(out), val, out); q -= 0.5 * DXc
    return out


R16 = RF - 0.5 * DXc; TH = 2 * np.pi * np.arange(64) / 64
RING = np.stack([ring(H, R16, th) for th in TH], 1)                       # [frames][64], the outer ring as the page reads it
LEAN = (RING[:, 0] - RING[:, 32]) * 1e3; TILT = 2 * (2 / 64) * (RING * np.cos(TH)[None]).sum(1) * 1e3
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
           # the books per frame, as the run counted them: stout in the glass (particles still in it times their mass, to 1 mg, 2.3
           # particles) and out of it; head in the glass (its thickness summed over the columns on the GPU, run 8 on) and broken off
           mp=float(Z["mp"]), particles=int(Z["N"]), stout_g=r5(Z["nact"] * float(Z["mp"]) * 1e3, 3),
           spill_g=r5((int(Z["N"]) - Z["nact"]) * float(Z["mp"]) * 1e3, 3), head_spill_ml=r5(Z["foam_spill"] * 1e6, 3),
           head_glass_ml=(r5(Z["vhead"] * 1e6, 3) if "vhead" in Z.files else None), books=task.get("books"), plant=task.get("plant"),
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
    measured=dict({k: task.get(k) for k in ("steps", "ms_per_step", "its_per_step", "run_s", "cells", "particles", "spilled_g", "head_spilled_ml", "control", "books", "head_mass", "fit_ring13")},
                  i_max_stored_A=(round(float(np.abs(Z["i"]).max()), 3) if "i" in Z.files else None),
                  # on the outer ring (R_fill - dx/2) from the trusted columns, as the page reads them: the lean (front wall minus back)
                  # and the tilt (twice the cos(theta) part, 2 (2/64) sum eta cos theta). lean_max_mm_run: the run's own lean, which
                  # included the columns at the glass (run_b.py)
                  lean_max_mm_run=task.get("lean_max_mm"), lean_max_mm=round(float(np.nanmax(np.abs(LEAN))), 2), tilt_max_mm=round(float(np.nanmax(np.abs(TILT))), 2)))]
idx["files"].sort(key=lambda f: (f["kind"] != "ride", f["path"]))
json.dump(idx, open(idx_path, "w"), indent=1)
print(dst, len(b), sha)
