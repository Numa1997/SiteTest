# Fig. 15, 3D runs on Kaggle's GPUs: the run code the notebook's loader fetches at a pinned commit (with rt3d.py and tm.py).
# Writes every run the moment it finishes (an 'RT3C' file and a line in runs.jsonl), prints one progress line per run
# (progress.log), and at the end index.json (SHA-256 of every file), timing.json and one tar of all runs.
# File 'RT3C' (little-endian): 'RT3C', uint32 H, H bytes JSON header, one zlib stream: nf*nxs*nr |psi| levels (uint8, of each
# frame's own peak, `peaks`), as many arg-psi levels, then nf*Nx float32 probability profile along x [then nf*Nx float32 of the
# 1D twin, flat walls only]. Index of the plane: f*nxs*nr + i*nr + j, x = x_first + i*step, y = j*step >= 0, z = 0.
import subprocess, sys, time, json, os
T0 = time.time()
ROOT = globals().get("OUTROOT", "/kaggle/working"); os.makedirs(ROOT, exist_ok=True)
LOG = open(ROOT + "/progress.log", "a")
def say(*a):
    s = f"[{time.time()-T0:7.1f} s] " + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
CPU = globals().get("CPU")
if not CPU: print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"], capture_output=True, text=True).stdout)
def backend():
    r = subprocess.run([sys.executable, "-c", "import jax; print(jax.default_backend())"], capture_output=True, text=True)
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "none: " + r.stderr[-300:]
b = backend(); say("jax backend before install:", b)
if b != "gpu" and not CPU:
    say("installing jax[cuda12]")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]"], check=True)
    say("jax backend after install:", backend())
import jax
DEV = jax.devices()
say("devices:", DEV, "jax", jax.__version__)
assert CPU or any(d.platform == "gpu" for d in DEV), "NO GPU: stopping so no quota is wasted on a CPU fallback"
sys.path.insert(0, ".")
import rt3d, tm
import threading, queue, datetime, hashlib, struct, zlib, traceback, tarfile, numpy as np
GEN = datetime.datetime.utcnow().strftime("%Y-%m-%d"); OUTD = f"{ROOT}/{GEN}/rt3d"
NX, N, DT, NF = globals().get("NX", 192), globals().get("NG", 128), 0.01, globals().get("NF", 200)
LIMIT_S = 8400
E_DOUBLE = sorted({round(0.4 + 0.1 * i, 2) for i in range(17)} | {0.735})
E_SINGLE = [0.4, 0.735, 1.0, 1.5, 2.0]
GROUPS = dict(dflat=dict(sizes=[0.0], Es=E_DOUBLE), dcoin=dict(sizes=[2.0, 4.0, 6.0], Es=E_DOUBLE), dshell=dict(sizes=[3.0], Es=E_DOUBLE),
              sflat=dict(sizes=[0.0], Es=E_SINGLE), scoin=dict(sizes=[2.0, 4.0, 6.0], Es=E_SINGLE), sshell=dict(sizes=[3.0], Es=E_SINGLE))
jobs = [(sh, E, s) for sh, G in GROUPS.items() for s in G["sizes"] for E in G["Es"]]
JOBSEL = globals().get("JOBSEL", "all")
if JOBSEL == "smoke": jobs = [("dflat", 0.735, 0.0), ("dcoin", 0.735, 4.0)]
if globals().get("ONLY"): jobs = [j for j in jobs if j[0] in ONLY]
jobs.sort(key=lambda j: -rt3d.t_end_of(j[1]))                        # long runs first
if globals().get("SHARD"): jobs = jobs[SHARD[0]::SHARD[1]]
os.makedirs(OUTD, exist_ok=True)
steps_of = lambda E: int(round(rt3d.t_end_of(E) / DT))
total = sum(steps_of(E) for _, E, _ in jobs)
say(f"{len(jobs)} runs; cells x steps x time per cell-step = {NX*N*N} x {total} x 1.2e-9 s = {NX*N*N*total*1.2e-9/3600:.2f} GPU hours "
    f"(1.2 ns per cell-step measured on a T4 for Fig. 14); on {max(1, len([d for d in DEV if d.platform == 'gpu']))} GPU(s) about "
    f"{NX*N*N*total*1.2e-9/max(1, len([d for d in DEV if d.platform == 'gpu']))/60:.0f} min")
Q = queue.Queue(); [Q.put(j) for j in jobs]
INDEX, DONE, LOCK, ERR = [], [0], threading.Lock(), []
JL = open(OUTD + "/runs.jsonl", "a")
def T_packet(segs, E):
    k0 = np.sqrt(2 * E); ks = np.linspace(max(k0 - 8 / (2 * rt3d.SIG0), 0.01), k0 + 8 / (2 * rt3d.SIG0), 2001)
    w = np.exp(-2 * rt3d.SIG0**2 * (ks - k0)**2); w /= np.trapezoid(w, ks)
    return float(np.trapezoid(w * np.array([abs(tm.solve(k * k / 2, segs)[0])**2 for k in ks]), ks))
def one(g, dev, sh, E, size):
    r = rt3d.run(g, sh, E, size, dt=DT, nframes=NF)
    pk = [float(p) for p in r["peaks"]]
    head = dict(shape=sh, E=E, V0=r["V0"], size=size, D=rt3d.D, S=rt3d.S, x0=rt3d.X0, sigma0=rt3d.SIG0, n=NF, nxs=r["nxs"], nr=N // 2,
                x_first=r["x_first"], step=g["dx"], prof_x_first=float(g["x"][0]), prof_nx=NX, steps=r["steps"], dt=DT,
                frame_dt=r["frame_dt"], wall=round(r["wall"], 2), device=str(dev), peaks=[round(p / pk[0], 6) for p in pk],
                peak0=pk[0], curve_names=r["curve_names"], curves=np.round(r["curves"], 7).tolist(),
                start_in_barrier=r["start_in_barrier"], start_in_border=r["start_in_border"], box=[NX, N, N])
    body = r["amp"].tobytes() + r["phase"].tobytes() + r["prof"].astype(np.float32).tobytes()
    if sh in ("dflat", "sflat"):
        o = rt3d.run1d(g, E, single=(sh == "sflat"), dt=DT, nframes=NF)
        p3 = r["prof"] / r["prof"].sum(1, keepdims=True); p1 = o["prof"] / o["prof"].sum(1, keepdims=True)
        segs = [(-rt3d.D / 2, rt3d.D / 2, r["V0"])] if sh == "sflat" else tm.double(r["V0"], rt3d.D, rt3d.S)
        head.update(has_1d=True, sep_check_max=float(np.abs(p3 - p1).max() / p1.max()), T_1d_splitstep=o["transmitted"],
                    R_1d_splitstep=o["reflected"], T_packet_exact=T_packet(segs, E))
        body += o["prof"].astype(np.float32).tobytes()
    hb = json.dumps(head, separators=(",", ":")).encode()
    blob = b"RT3C" + struct.pack("<I", len(hb)) + hb + zlib.compress(body, 6)
    name = f"{sh}_R{size:g}_E{E:.3f}.bin"
    open(f"{OUTD}/{name}", "wb").write(blob)
    c = r["curves"][-1]
    rec = dict(file=name, shape=sh, E=E, size=size, bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(), steps=r["steps"],
               wall=head["wall"], device=str(dev), end=dict(zip(r["curve_names"], [round(float(v), 6) for v in c])),
               start_in_barrier=r["start_in_barrier"])
    for k in ("sep_check_max", "T_1d_splitstep", "T_packet_exact"):
        if k in head: rec[k] = head[k]
    with LOCK:
        DONE[0] += 1; INDEX.append(rec); JL.write(json.dumps(rec) + "\n"); JL.flush()
        extra = (f", 3D vs 1D twin {head['sep_check_max']:.1e}, T 1D {head['T_1d_splitstep']:.4f} exact {head['T_packet_exact']:.4f}"
                 if "sep_check_max" in head else "")
        say(f"{DONE[0]:3d}/{len(jobs)} {sh} R={size:g} E={E} on {dev}: {r['steps']} steps, {r['wall']:.1f} s "
            f"({r['wall']/r['steps']/(NX*N*N)*1e9:.2f} ns per cell-step), {len(blob)/1e3:.0f} kB, end {rec['end']}{extra}")
def worker(dev):
    bad = 0
    with jax.default_device(dev):
        g = rt3d.setup(NX, N)
        while bad < 3:
            if time.time() - T0 > LIMIT_S: return
            try: sh, E, size = Q.get_nowait()
            except queue.Empty: return
            try: one(g, dev, sh, E, size); bad = 0
            except Exception as e:
                bad += 1
                with LOCK: ERR.append(dict(job=[sh, E, size], error=repr(e)[:500]))
                say("RUN FAILED", sh, E, size, "on", dev, repr(e)[:300]); say(traceback.format_exc()[-800:])
DEVS = [d for d in jax.devices() if d.platform == "gpu"] or [jax.devices()[0]]
TS = time.time()
threads = [threading.Thread(target=worker, args=(d,)) for d in DEVS]
[t.start() for t in threads]; [t.join() for t in threads]
SWEEP_S = time.time() - TS; JL.close()
left = []
while True:
    try: left.append(list(Q.get_nowait()))
    except queue.Empty: break
say(f"{DONE[0]} of {len(jobs)} runs in {SWEEP_S:.0f} s on {len(DEVS)} device(s); failed {len(ERR)}; not started {len(left)}")
INDEX.sort(key=lambda r: r["file"])
json.dump(dict(generated=GEN, kind="rt3d", jobsel=JOBSEL, shard=globals().get("SHARD"), box=[NX, N, N], dx=0.5, dt=DT, nframes=NF,
               V0=rt3d.V0_DEF, D=rt3d.D, S=rt3d.S, packet=dict(x0=rt3d.X0, sigma0=rt3d.SIG0), groups=GROUPS,
               device=jax.devices()[0].device_kind, devices=len(DEVS), sweep_s=round(SWEEP_S, 1), failed=ERR, not_started=left,
               method="Strang split-step Fourier, 3D, complex64; absorbing border sin^(1/8) in the outer tenth of each axis",
               units="hbar = m = 1, lengths in the grid unit a", runs=INDEX), open(OUTD + "/index.json", "w"), separators=(",", ":"))
files = sorted(f for f in os.listdir(OUTD) if f.endswith(".bin"))
with tarfile.open(f"{OUTD}/rt3d.tar", "w") as tf:
    for f in files: tf.add(f"{OUTD}/{f}", arcname=f)
with tarfile.open(f"{OUTD}/rt3d.tar") as tf: ok = len(tf.getnames()) == len(files)
if ok:
    for f in files: os.remove(f"{OUTD}/{f}")
say(len(files), "files ->", f"rt3d.tar {os.path.getsize(f'{OUTD}/rt3d.tar')/1e6:.1f} MB", "ok" if ok else "TAR CHECK FAILED: files kept")
json.dump(dict(total_s=round(time.time() - T0, 1), sweep_s=round(SWEEP_S, 1), devices=len(DEVS), runs_done=DONE[0], runs_planned=len(jobs),
               failed=len(ERR), not_started=len(left), device_seconds_of_runs=round(sum(r["wall"] for r in INDEX), 1),
               steps_total=int(sum(r["steps"] for r in INDEX))), open(OUTD + "/timing.json", "w"))
say(f"all done in {time.time()-T0:.0f} s")
