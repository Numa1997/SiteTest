"""Fig. 16: pack one ride computed on Kaggle (a .npz written by run16.py) into the page's file, public/data/fig16/<date>/<name>.json, in
Fig. 12's format (tools/fig12/kaggle/pack_ride.py: the stout's surface H on the solver's columns as int16 differences, the head's
thickness hf, drops and lumps) plus the four-wheel cart's pose and its control signals per stored frame. Nothing is computed here:
arrays are rounded to stated steps, packed and written; index-16.json lists each file with its SHA-256.
Run: python3 tools/fig16/kaggle/pack16.py <ride.npz> <summary.json> <task name> <date folder> <notebook version> <commit>"""
import base64, hashlib, json, os, sys
import numpy as np

src, summary_path, name, date, version, commit = sys.argv[1:7]
here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.normpath(os.path.join(here, "..", "..", "..", "public", "data", "fig16", date)); os.makedirs(out_dir, exist_ok=True)
Z = np.load(src); S = json.load(open(summary_path)); task = next(t for t in S["tasks"] if t["name"] == name)
QH, QHF, QD, QV = 2e-5, 1e-4, 1e-4, 1e-10
pk = lambda a: base64.b64encode(__import__("zlib").compress(np.ascontiguousarray(a).tobytes(), 9)).decode()

H = Z["H"].astype(np.float64); nf, n, _ = H.shape
DXc, X0c, RF = float(Z["dx"]), float(Z["x0"]), float(Z["Rfill"])
cc_ = X0c + (np.arange(n) + 0.5) * DXc; RC = np.hypot(*np.meshgrid(cc_, cc_, indexing="ij"))
H = np.where(np.isfinite(H) & (RC < RF - DXc)[None], H, np.nan)        # the trusted columns, as pack_ride.py keeps them


def ring(Hs, r, th):
    """pack_ride.ring: the stored surface at radius r, angle th, bilinear over the trusted columns, stepping inward by half a cell."""
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


TH = 2 * np.pi * np.arange(64) / 64
RING = np.stack([ring(H, RF - 0.5 * DXc, th) for th in TH], 1)
LEAN = (RING[:, 0] - RING[:, 32]) * 1e3; TILT = 2 * (2 / 64) * (RING * np.cos(TH)[None]).sum(1) * 1e3
Hq = np.where(np.isfinite(H), np.clip(np.round(H / QH), -32767, 32767), -32768).astype(np.int16)
Hd = Hq.copy(); Hd[1:] = (Hq[1:].astype(np.int32) - Hq[:-1].astype(np.int32)).astype(np.int16)
hf = np.clip(np.round(Z["hf"].astype(np.float64) / QHF), 0, 255).astype(np.uint8)


def cloud(arr, extra=None):
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
out = dict(name=name, generated=date, n=int(n), frames=int(nf), fps=30, dx=DXc, x0=X0c, fill=float(Z["fill"]), qH=QH, qhf=QHF, qd=QD, qv=QV, t=r5(Z["t"], 4),
           mp=float(Z["mp"]), particles=int(Z["N"]), stout_g=r5(Z["nact"] * float(Z["mp"]) * 1e3, 3), spill_g=r5((int(Z["N"]) - Z["nact"]) * float(Z["mp"]) * 1e3, 3),
           head_spill_ml=r5(Z["foam_spill"] * 1e6, 3), head_glass_ml=r5(Z["vhead"] * 1e6, 3), books=task.get("books"),
           task={k: task[k] for k in ("kind", "end", "dx", "ctrl", "road", "v0") if k in task}, nd=nd, nl=nl, H=pk(Hd), hf=pk(hf), drops=pk(drops), lumps=pk(lumps),
           lean_mm=r5(LEAN, 3), tilt_mm=r5(TILT, 3))
if "x" in Z.files:
    srcb = open(os.path.join(here, "..", "..", "fig12", "kaggle", "run_b.py")).read(); a = srcb.index("ROADS = {"); b = srcb.index("\n}\n", a) + 2
    ROADS = eval(srcb[a + len("ROADS = "):b])
    out.update(bumps=ROADS[task["road"]]["bumps"], v0=task["v0"], road=task["road"], ctrl=task["ctrl"], cart=S.get("cart"), weights=task.get("weights"),
               # the cart, per stored frame: position and speed; the deck's centre height and pitch (rad); the axles' heights; the motor
               # current and its command (A); the actuators' forces (N); the tyre loads (N); the strut forces (N); the glass's sideways
               # acceleration felt by the stout (m/s^2); the probes' reading and the Kalman estimate of the swing (m)
               x=r5(Z["x"], 5), v=r5(Z["v"], 4), zc=r5(Z["zc"], 6), th=r5(Z["th"], 6), zf=r5(Z["zf"], 6), zr=r5(Z["zr"], 6), i=r5(Z["i"], 4), icmd=r5(Z["icmd"], 4),
               uf=r5(Z["uf"], 3), ur=r5(Z["ur"], 3), Nf=r5(Z["Nf"], 3), Nr=r5(Z["Nr"], 3), Ff=r5(Z["Ff"], 3), Fr=r5(Z["Fr"], 3), aeff=r5(Z["aeff"], 4),
               yq=r5(Z["py"], 6), qhat=r5(Z["qh"], 6), gx=r5(Z["gx"], 4), gz=r5(Z["gz"], 4), Fx=r5(Z["Fx"], 4), Fz=r5(Z["Fz"], 4))
dst = os.path.join(out_dir, name + ".json"); json.dump(out, open(dst, "w"), separators=(",", ":"))
bts = open(dst, "rb").read(); sha = hashlib.sha256(bts).hexdigest()
idx_path = os.path.join(out_dir, "index-16.json")
idx = json.load(open(idx_path)) if os.path.exists(idx_path) else dict(
    about="Fig. 16 computed in JAX on Kaggle's GPU: Fig. 12's pint (stout, head of foam) on the four-wheel cart with its control system, one file per ride.",
    generated=date, kaggle=dict(notebook="numakoudsie/fig-16-guinness-cart-with-control", url="https://www.kaggle.com/code/numakoudsie/fig-16-guinness-cart-with-control",
                                version=int(version), machine=S.get("device")),
    code=f"tools/fig16/kaggle/cart4.py, run16.py and tools/fig12/kaggle/stout_jax.py at SiteTest commit {commit}", design=S.get("design"), files=[])
CT = {"full": "control system on", "off": "control system off"}
label = f"{task['road'][0].upper()}{task['road'][1:]}, {task['v0']:.1f} m/s · {CT[task['ctrl']]}" if task["kind"] == "ride" else "Standing still"
m = {k: task.get(k) for k in ("steps", "ms_per_step", "run_s", "spilled_g", "head_spilled_ml", "books", "pitch_max_deg", "i_max_A", "u_max_N", "current_limited", "bump_stop_N", "v_range")}
m.update(lean_max_mm=round(float(np.nanmax(np.abs(LEAN))), 2), tilt_max_mm=round(float(np.nanmax(np.abs(TILT))), 2))
idx["files"] = [f for f in idx["files"] if f["path"] != name + ".json"] + [dict(path=name + ".json", label=label, kind=task["kind"], ctrl=task.get("ctrl"), road=task.get("road"),
                                                                              v0=task.get("v0"), bytes=len(bts), sha256=sha, frames=int(nf), seconds=round((nf - 1) / 30, 3), measured=m)]
idx["files"].sort(key=lambda f: (f["kind"] != "ride", f["path"]))
json.dump(idx, open(idx_path, "w"), indent=1)
print(dst, len(bts), sha, "tilt max", m["tilt_max_mm"], "mm, head spilled", m["head_spilled_ml"], "mL")
