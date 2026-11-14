"""Fig. 15 correction: the 2,609 disc and shell runs recomputed in the exact (x, rho) reduction (axisym_jax.py), on Kaggle's GPUs.

Each job is a stored generation-2 run (jobs_2d.json, made from the index by make_jobs_2d.py): its spec, frame times and the stored
file's output layout. The new file is written in the stored RT3C layout, so the page plays it unchanged:
  |psi| and arg psi on z = 0, y >= 0 (= psi(x, rho = |y|)) on the stored 0.5 a points, 8-bit levels of each frame's own peak;
  the x-profile (Int |psi|^2 2 pi rho drho) on the stored x points; the stored region curves (inside the stored box);
  in the header: T_ref (share beyond the last face, counting what the borders absorbed, by side), its undecided half T_unc,
  the norm drift, the solver grid, and the parent file's SHA-256.
Globals a loader sets: OUTROOT, GEN, SHARD = (i, n), JOBSEL ('smoke' or 'all'), DTYPE ('c64' | 'c128'), GRID (dict of solver
settings), LIMIT_S. Progress: one line per run in progress.log, written the moment the run ends.
"""
import os, sys, json, time, hashlib, struct, zlib, threading, queue, tarfile, traceback
import numpy as np
T0 = time.time()
ROOT = globals().get("OUTROOT", "/kaggle/working"); os.makedirs(ROOT, exist_ok=True)
LOG = open(ROOT + "/progress.log", "a")
def say(*a):
    s = f"[{time.time()-T0:7.1f} s] " + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
sys.path.insert(0, ".")
import jax
print(jax.devices())
if not globals().get("CPU") and jax.default_backend() != "gpu":
    say("NO GPU BACKEND"); raise SystemExit("NO GPU BACKEND")
import axisym as ax, axisym_jax as aj

GRID = dict(hx=0.0625, Nr=256, Rmax=64.0, Wr=12.0, dt=0.01, box_factor=2.0)
GRID.update(globals().get("GRID", {}))
DTYPE = globals().get("DTYPE", "c64")


def layout(Nx):
    x = (np.arange(Nx) - Nx // 2) * 0.5; inner = (Nx // 2 - max(4, Nx // 10)) * 0.5
    i0 = int(np.searchsorted(x, -inner)); i1 = int(np.searchsorted(x, inner))
    return x, i0, i1


def quantize(sl, ph):
    pk = float(sl.max()) or 1.0
    qa = np.clip(np.round(255 * sl / pk), 0, 255).astype(np.uint8)
    qp = (np.round((ph + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
    return qa, qp, pk


def one(job, dev):
    sp = job["spec"]; x, i0, i1 = layout(sp["Nx"]); n = job["n"]
    o = aj.run(sp, job["t_end"], hx=GRID["hx"], Lx=sp["Nx"] * 0.5 * GRID["box_factor"], Nr=GRID["Nr"], Rmax=GRID["Rmax"],
               Wr=GRID["Wr"], dt=GRID["dt"], nframes=n, frame_dt=job["frame_dt"], dtype=DTYPE, out_x=x,
               out_rho=np.arange(64) * 0.5, box_half=0.5 * sp["Nx"] * 0.5, rule=GRID.get("rule", "cell"))
    F = o["frames"]                                     # (n, Nx, 64): psi on the stored points
    A, P, pk = [], [], []
    for f in range(n):
        s = F[f, i0:i1]; qa, qp, p = quantize(np.abs(s), np.angle(s)); A.append(qa); P.append(qp); pk.append(p)
    C = o["curves"]; names = o["names"]
    keep = ["t", "norm"] + (["core", "gap", "out"] if sp["shape"] == "shell" else ["left", "right", "well"])
    keep = [k for k in keep if k in names]
    curves = C[:, [names.index(k) for k in keep]]
    extra = {k: np.round(C[:, names.index(k)], 7).tolist() for k in ("absL", "absR", "absM", "total")}
    head = dict(spec=sp, group=job["group"], shape=sp["shape"], E=sp["E"], V0=sp["V0"], D=sp["D"], P=sp["P"], N=sp["N"], size=sp["R"],
                bias=sp["bias"], sigma_x=sp["sx"], sigma_perp=sp["sp"], x0=ax.x0_of(sp),
                centres=(ax.centres(sp) if sp["shape"] != "shell" else None), extent=list(ax.extent(sp)), n=n, nxs=i1 - i0, nr=64,
                x_first=float(x[i0]), step=0.5, prof_x_first=float(x[0]), prof_nx=sp["Nx"], steps=o["steps"], dt=GRID["dt"],
                t_end=float(C[-1, 0]), frame_dt=o["frame_dt"], wall=round(o["wall"], 2), device=str(dev),
                peaks=[round(p / pk[0], 6) for p in pk], peak0=pk[0], curve_names=keep, curves=np.round(curves, 7).tolist(),
                box=[sp["Nx"], 128, 128], method="exact axisymmetric reduction (m = 0) in (x, rho): Strang split-step, FFT in x, "
                "order-0 quasi-discrete Hankel transform in rho, cell-averaged V (tools/kaggle/resonant-tunnelling/correction/axisym_jax.py)",
                grid=dict(GRID, dtype=DTYPE), parent=dict(file=job["file"], sha256=job["sha256"]), T_ref=o["T"], T_unc=o["T_unc"],
                drift=o["drift"], extra_curves=extra)
    body = np.array(A).tobytes() + np.array(P).tobytes() + np.asarray(o["profs"], np.float32).tobytes()
    hb = json.dumps(head, separators=(",", ":")).encode()
    blob = b"RT3C" + struct.pack("<I", len(hb)) + hb + zlib.compress(body, 6)
    return blob, head, o


if __name__ == "__main__" or globals().get("RUN"):
    say("devices:", jax.devices(), "jax", jax.__version__, "dtype", DTYPE, "grid", GRID)
    J = json.load(open(globals().get("JOBS", "jobs_2d.json")))
    if globals().get("JOBSEL") == "smoke": J = [j for j in J if j["file"] in SMOKE]
    elif globals().get("SHARD"): i, nsh = SHARD; J = J[i::nsh]
    GEN = globals().get("GEN", "2026-11-14b"); OUTD = f"{ROOT}/{GEN}/rt2d"; os.makedirs(OUTD, exist_ok=True)
    done = {l.split()[0] for l in open(OUTD + "/done.txt")} if os.path.exists(OUTD + "/done.txt") else set()
    Q = queue.Queue(); [Q.put(j) for j in sorted(J, key=lambda j: -j["cost"]) if j["file"] not in done]
    LOCK = threading.Lock(); JL = open(OUTD + "/runs.jsonl", "a"); DL = open(OUTD + "/done.txt", "a"); CNT = [0]; ERR = []
    LIMIT_S = globals().get("LIMIT_S", 11.0 * 3600)

    def worker(dev):
        with jax.default_device(dev):
            while time.time() - T0 < LIMIT_S:
                try: j = Q.get_nowait()
                except queue.Empty: return
                try:
                    blob, head, o = one(j, dev)
                    open(f"{OUTD}/{j['file']}", "wb").write(blob)
                    rec = dict(file=j["file"], spec=j["spec"], sha256=hashlib.sha256(blob).hexdigest(), bytes=len(blob), T_ref=o["T"],
                               T_unc=o["T_unc"], drift=o["drift"], steps=o["steps"], wall=round(o["wall"], 2),
                               s_per_step=o["s_per_step"], cells=o["cells"], device=str(dev))
                    with LOCK:
                        CNT[0] += 1; JL.write(json.dumps(rec) + "\n"); JL.flush(); DL.write(j["file"] + "\n"); DL.flush()
                        say(f"{CNT[0]}/{len(J)} {j['file']} on {dev}: T {o['T']:.5f} +- {o['T_unc']:.1e}, drift {o['drift']:.1e}, "
                            f"{o['steps']} steps, {o['wall']:.1f} s ({o['s_per_step']*1e3:.3f} ms/step)")
                except Exception as e:
                    with LOCK: ERR.append(dict(file=j["file"], error=repr(e)[:400]))
                    say("RUN FAILED", j["file"], repr(e)[:300]); say(traceback.format_exc()[-600:])

    devs = [d for d in jax.devices() if d.platform == "gpu"] or [jax.devices()[0]]
    th = [threading.Thread(target=worker, args=(d,)) for d in devs]; [t.start() for t in th]; [t.join() for t in th]
    JL.close(); DL.close()
    say(f"{CNT[0]} runs done, {len(ERR)} failed, {Q.qsize()} not started, {time.time()-T0:.0f} s")
    files = sorted(f for f in os.listdir(OUTD) if f.endswith(".bin"))
    tname = f"{OUTD}/rt2d_{globals().get('JOBSEL', 'all')}" + (f"_{SHARD[0]}of{SHARD[1]}" if globals().get("SHARD") else "") + ".tar"
    with tarfile.open(tname, "w") as tf:
        for f in files: tf.add(f"{OUTD}/{f}", arcname=f)
    json.dump(dict(failed=ERR, done=CNT[0], total_s=round(time.time() - T0, 1)), open(OUTD + "/summary.json", "w"))
    say("tar", os.path.basename(tname), round(os.path.getsize(tname) / 1e6, 1), "MB")
