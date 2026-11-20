# Fig. 15, 3D generation 2 on Kaggle's GPUs: the run code each loader notebook fetches at a pinned commit (with rt3d2.py and tm.py).
# The job list (jobs()) is the whole parameter space; a notebook runs one shard of it (SHARD = (i, n): jobs i, i + n, ...), longest
# first, one worker thread per GPU. Every run is written the moment it finishes (an RT3C file and a line in runs.jsonl) and logged in
# one progress line (progress.log). At the end: index.json (SHA-256 of every file), timing.json, and one tar per shard.
# RT3C as in generation 1: 'RT3C', uint32 H, H bytes JSON header, zlib of: nf*nxs*nr |psi| levels (uint8, of each frame's own peak),
# as many arg-psi levels, nf*Nx float32 profile along x [, nf*Nx float32 profile of the 1D twin: walls only].
import subprocess, sys, time, json, os
T0 = time.time()
ROOT = globals().get("OUTROOT", "/kaggle/working"); os.makedirs(ROOT, exist_ok=True)
LOG = open(ROOT + "/progress.log", "a")
def say(*a):
    s = f"[{time.time()-T0:7.1f} s] " + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
import numpy as np
sys.path.insert(0, ".")
import tm

DT, NF, NS = 0.01, 200, 1.0e-9           # time step; frames per run; measured seconds per cell-step on a T4 (generation 1: 0.96-1.00 ns)
EGRID = [round(0.3 + 0.05 * i, 3) for i in range(47)]          # 0.30 ... 2.60
EBIAS = [round(0.1 + 0.05 * i, 3) for i in range(25)]          # 0.10 ... 1.30: the energies the diode's Fermi sea supplies
BIAS = [round(0.125 * i, 3) for i in range(20)]                # 0 ... 2.375


def spec(shape, N, V0, D, P, R, E, bias=0.0, sx=3.0, Nx=192):
    return dict(shape=shape, N=N, V0=V0, D=D, P=P, R=R, E=E, bias=bias, sx=sx, sp=3.0, Nx=Nx)


def name_of(s):
    return (f"{s['shape']}_N{s['N']}_V{s['V0']:g}_D{s['D']:g}_P{s['P']:g}_R{s['R']:g}_B{s['bias']:g}_s{s['sx']:g}_E{s['E']:.3f}.bin")


def resonances_1d(s, Emax=2.6):
    import rt3d2
    segs = rt3d2.segs_1d(s); E = np.linspace(0.05, Emax, 3000); T = np.array([abs(tm.solve(e, segs)[0])**2 for e in E])
    return [float(E[i]) for i in range(1, len(E) - 1) if T[i] > 0.6 and T[i] >= T[i - 1] and T[i] >= T[i + 1]]


def jobs():
    J = []
    shapes = [("flat", 0.0)] + [("coin", R) for R in (2.0, 4.0, 6.0, 9.0, 12.0)]
    for P in (2.5, 3.5, 4.5, 5.5):                                            # A: pairs, spacing sweep
        for sh, R in shapes:
            J += [(spec(sh, 2, 2.0, 1.0, P, R, E), "A") for E in EGRID]
    for R in (3.0, 5.0):                                                      # B: two shells
        for P in (2.5, 3.5):
            J += [(spec("shell", 2, 2.0, 1.0, P, R, E), "B") for E in EGRID]
    for V0, D, P in ((1.5, 1.0, 2.5), (3.0, 1.0, 2.5), (2.0, 1.5, 3.0), (2.0, 2.0, 3.5)):   # C: height and thickness
        for sh, R in (("flat", 0.0), ("coin", 6.0), ("coin", 12.0)):
            J += [(spec(sh, 2, V0, D, P, R, E), "C") for E in EGRID]
    for sh, R in shapes + [("shell", 3.0), ("shell", 5.0)]:                   # D: one barrier alone
        J += [(spec(sh, 1, 2.0, 1.0, 2.5, R, E), "D") for E in EGRID]
    for Nb in (3, 5, 10):                                                     # E: barriers in a row (superlattice)
        for sh, R in (("flat", 0.0), ("coin", 6.0), ("coin", 12.0)):
            J += [(spec(sh, Nb, 2.0, 1.0, 2.5, R, E, Nx=256 if Nb == 10 else 192), "E") for E in EGRID]
    for sh, R in (("flat", 0.0), ("coin", 6.0)):                              # F: the diode under bias
        for B in BIAS:
            J += [(spec(sh, 2, 2.0, 1.0, 2.5, R, E, bias=B), "F") for E in EBIAS]
    for sh, V0, D, P, R in (("flat", 2.0, 1.0, 2.5, 0.0), ("flat", 3.0, 1.0, 2.5, 0.0), ("flat", 2.0, 2.0, 3.5, 0.0), ("coin", 2.0, 1.0, 2.5, 12.0)):
        s0 = spec(sh, 2, V0, D, P, R, 1.0, sx=12.0, Nx=512)                   # G: long packets across each resonance below 2.2
        for Er in resonances_1d(s0, 2.2)[:2]:
            dE = np.sqrt(2 * Er) / 24
            J += [(spec(sh, 2, V0, D, P, R, round(float(Er + dE * u), 4), sx=12.0, Nx=512), "G") for u in np.linspace(-3, 3, 15)]
    return J


def cost(s, t_end):
    return s["Nx"] * 128 * 128 * round(t_end / DT) * NS


if __name__ == "__main__" and globals().get("BILL_ONLY"):
    pass
if globals().get("BILL_ONLY"):
    import rt3d2
    J = jobs(); tot = 0.0; by = {}
    for s, grp in J:
        c = cost(s, rt3d2.t_end_of(s, tm)); tot += c; by[grp] = by.get(grp, 0) + c
    BILL = dict(runs=len(J), device_hours=tot / 3600, by={k: round(v / 3600, 2) for k, v in by.items()})
else:
    CPU = globals().get("CPU")
    if not CPU: print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"], capture_output=True, text=True).stdout)
    def backend():
        r = subprocess.run([sys.executable, "-c", "import jax; print(jax.default_backend())"], capture_output=True, text=True)
        return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "none: " + r.stderr[-300:]
    b = backend(); say("jax backend before install:", b)
    if b != "gpu" and not CPU:
        say("installing jax[cuda12]"); subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]"], check=True)
        say("jax backend after install:", backend())
    import jax
    DEV = jax.devices(); say("devices:", DEV, "jax", jax.__version__)
    assert CPU or any(d.platform == "gpu" for d in DEV), "NO GPU: stopping so no quota is wasted on a CPU fallback"
    import rt3d2, threading, queue, datetime, hashlib, struct, zlib, traceback, tarfile
    GEN = globals().get("GEN", datetime.datetime.utcnow().strftime("%Y-%m-%d")); OUTD = f"{ROOT}/{GEN}/rt3d2"
    LIMIT_S = globals().get("LIMIT_S", 11.0 * 3600)
    J = jobs()
    if globals().get("JOBSEL") == "smoke":
        J = [(spec("flat", 2, 2.0, 1.0, 2.5, 0.0, 0.735), "A"), (spec("coin", 3, 2.0, 1.0, 2.5, 6.0, 0.9), "E"),
             (spec("flat", 2, 2.0, 1.0, 2.5, 0.0, 0.5, bias=0.75), "F"), (spec("shell", 2, 2.0, 1.0, 2.5, 3.0, 0.735), "B")]
    if globals().get("SHARD"):
        i, n = SHARD; J = J[i::n]
    tends = [rt3d2.t_end_of(s, tm) for s, _ in J]
    order = sorted(range(len(J)), key=lambda k: -cost(J[k][0], tends[k]))
    os.makedirs(OUTD, exist_ok=True)
    done_before = {l.split()[0] for l in open(OUTD + "/done.txt")} if os.path.exists(OUTD + "/done.txt") else set()
    tot = sum(cost(J[k][0], tends[k]) for k in order)
    ngpu = max(1, len([d for d in DEV if d.platform == "gpu"]))
    say(f"{len(J)} runs; cells x steps x {NS*1e9:.1f} ns = {tot/3600:.2f} device hours, on {ngpu} GPU(s) about {tot/ngpu/3600:.2f} h")
    Q = queue.Queue(); [Q.put(k) for k in order if name_of(J[k][0]) not in done_before]
    INDEX, DONE, LOCK, ERR = [], [0], threading.Lock(), []
    JL = open(OUTD + "/runs.jsonl", "a"); DL = open(OUTD + "/done.txt", "a")

    def T_packet(s):
        segs = rt3d2.segs_1d(s); k0 = np.sqrt(2 * s["E"]); sk = 1 / (2 * s["sx"])
        ks = np.linspace(max(k0 - 8 * sk, 0.01), k0 + 8 * sk, 1201); w = np.exp(-(ks - k0)**2 / (2 * sk**2)); w /= np.trapezoid(w, ks)
        return float(np.trapezoid(w * np.array([abs(tm.solve(k * k / 2, segs)[0])**2 for k in ks]), ks))

    def one(gs, dev, k):
        s, grp = J[k]; t_end = tends[k]
        g = gs.get(s["Nx"]) or gs.setdefault(s["Nx"], rt3d2.setup(s["Nx"], 128))
        r = rt3d2.run(g, s, t_end, dt=DT, nframes=NF)
        pk = [float(p) for p in r["peaks"]]
        head = dict(spec=s, group=grp, shape=s["shape"], E=s["E"], V0=s["V0"], D=s["D"], P=s["P"], N=s["N"], size=s["R"], bias=s["bias"],
                    sigma_x=s["sx"], sigma_perp=s["sp"], x0=r["x0"], centres=(rt3d2.centres(s) if s["shape"] != "shell" else None),
                    extent=rt3d2.extent(s), n=NF, nxs=r["nxs"], nr=64, x_first=r["x_first"], step=g["dx"], prof_x_first=float(g["x"][0]),
                    prof_nx=s["Nx"], steps=r["steps"], dt=DT, t_end=t_end, frame_dt=r["frame_dt"], wall=round(r["wall"], 2), device=str(dev),
                    peaks=[round(p / pk[0], 6) for p in pk], peak0=pk[0], curve_names=r["curve_names"],
                    curves=np.round(r["curves"], 7).tolist(), start_in_barrier=r["start_in_barrier"],
                    start_in_border=r["start_in_border"], box=[s["Nx"], 128, 128])
        body = r["amp"].tobytes() + r["phase"].tobytes() + r["prof"].astype(np.float32).tobytes()
        if s["shape"] == "flat":
            o = rt3d2.run1d(g, s, t_end, dt=DT, nframes=NF)
            p3 = r["prof"] / r["prof"].sum(1, keepdims=True); p1 = o["prof"] / o["prof"].sum(1, keepdims=True)
            head.update(has_1d=True, sep_check_max=float(np.abs(p3 - p1).max() / p1.max()), T_1d_splitstep=o["transmitted"],
                        R_1d_splitstep=o["reflected"], T_packet_exact=(T_packet(s) if not s["bias"] else None))
            body += o["prof"].astype(np.float32).tobytes()
        hb = json.dumps(head, separators=(",", ":")).encode()
        blob = b"RT3C" + struct.pack("<I", len(hb)) + hb + zlib.compress(body, 6)
        name = name_of(s); open(f"{OUTD}/{name}", "wb").write(blob)
        c = r["curves"][-1]
        rec = dict(file=name, group=grp, spec=s, bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(), steps=r["steps"],
                   wall=head["wall"], device=str(dev), end=dict(zip(r["curve_names"], [round(float(v), 6) for v in c])),
                   start_in_barrier=r["start_in_barrier"])
        for kk in ("sep_check_max", "T_1d_splitstep", "T_packet_exact"):
            if kk in head: rec[kk] = head[kk]
        with LOCK:
            DONE[0] += 1; INDEX.append(rec); JL.write(json.dumps(rec) + "\n"); JL.flush(); DL.write(name + "\n"); DL.flush()
            extra = (f", 3D vs 1D {head['sep_check_max']:.1e}, T 1D {head['T_1d_splitstep']:.4f}" if "sep_check_max" in head else "")
            say(f"{DONE[0]:4d}/{Q.qsize() + DONE[0]} {grp} {name} on {dev}: {r['steps']} steps, {r['wall']:.1f} s "
                f"({r['wall']/r['steps']/(s['Nx']*128*128)*1e9:.2f} ns/cell-step), {len(blob)/1e6:.2f} MB{extra}")

    def worker(dev):
        bad = 0; gs = {}
        with jax.default_device(dev):
            while bad < 3:
                if time.time() - T0 > LIMIT_S: return
                try: k = Q.get_nowait()
                except queue.Empty: return
                try: one(gs, dev, k); bad = 0
                except Exception as e:
                    bad += 1
                    with LOCK: ERR.append(dict(job=name_of(J[k][0]), error=repr(e)[:500]))
                    say("RUN FAILED", name_of(J[k][0]), "on", dev, repr(e)[:300]); say(traceback.format_exc()[-800:])

    DEVS = [d for d in jax.devices() if d.platform == "gpu"] or [jax.devices()[0]]
    TS = time.time()
    threads = [threading.Thread(target=worker, args=(d,)) for d in DEVS]
    [t.start() for t in threads]; [t.join() for t in threads]
    SWEEP_S = time.time() - TS; JL.close(); DL.close()
    left = []
    while True:
        try: left.append(name_of(J[Q.get_nowait()][0]))
        except queue.Empty: break
    say(f"{DONE[0]} runs in {SWEEP_S:.0f} s on {len(DEVS)} device(s); failed {len(ERR)}; not started {len(left)}")
    INDEX.sort(key=lambda r: r["file"])
    json.dump(dict(generated=GEN, kind="rt3d2", jobsel=globals().get("JOBSEL", "all"), shard=globals().get("SHARD"), dx=0.5, dt=DT,
                   nframes=NF, device=jax.devices()[0].device_kind, devices=len(DEVS), sweep_s=round(SWEEP_S, 1), failed=ERR,
                   not_started=left, method="Strang split-step Fourier, 3D, complex64; absorbing border sin^(1/8) in the outer tenth of each axis",
                   units="hbar = m = 1, lengths in the grid unit a", runs=INDEX), open(OUTD + "/index.json", "w"), separators=(",", ":"))
    files = sorted(f for f in os.listdir(OUTD) if f.endswith(".bin"))
    tname = f"{OUTD}/rt3d2_{globals().get('JOBSEL', 'all')}" + (f"_{SHARD[0]}of{SHARD[1]}" if globals().get("SHARD") else "") + ".tar"
    with tarfile.open(tname, "w") as tf:
        for f in files: tf.add(f"{OUTD}/{f}", arcname=f)
    with tarfile.open(tname) as tf: ok = len(tf.getnames()) == len(files)
    if ok:
        for f in files: os.remove(f"{OUTD}/{f}")
    say(len(files), "files ->", f"{os.path.basename(tname)} {os.path.getsize(tname)/1e6:.1f} MB", "ok" if ok else "TAR CHECK FAILED: files kept")
    json.dump(dict(total_s=round(time.time() - T0, 1), sweep_s=round(SWEEP_S, 1), devices=len(DEVS), runs_done=DONE[0], runs_planned=len(J),
                   failed=len(ERR), not_started=len(left), device_seconds_of_runs=round(sum(r["wall"] for r in INDEX), 1)),
              open(OUTD + "/timing.json", "w"))
    say(f"all done in {time.time()-T0:.0f} s")
