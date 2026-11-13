"""Writes shapes3d.ipynb: the one Kaggle GPU notebook for every case of Fig. 14 that needs true 3D and was not computed yet.
On both GPUs of the session, 128^3 points each (tools/kaggle/schrodinger-shapes/solver3d.py):
  sphere  9 energies x 4 heights (wells -4, -2, -1 and the hard ball) x 5 radii           = 180 runs
  coin    9 x 13 heights (wells, 0 ... 8, hard) x 5 radii, thickness 1 a                  = 585
  tube    9 x 13 x 5 radii, wall 1 a thick                                                = 585
  soff    spherical wave from the side onto a ball R = 4:      9 x 4 heights (-2, 2, 6, hard) =  36
  sslab   spherical wave onto a flat wall d = 1:               9 x 4                          =  36
  spil    spherical wave onto a pillar R = 4 (also the 3D wave Re psi, every 2nd frame): 9 x 4 =  36
Every run is written the moment it finishes (a 'SPHC' file as the website reads it, and a line in runs.jsonl), so a crash
loses nothing; a failing run is logged and skipped; no new run starts after LIMIT_S seconds. At the end the files of each
shape go into one tar and index.json (with SHA-256 of every file) is written.
File 'SPHC' (little-endian): 'SPHC', uint32 H, H bytes JSON header, one zlib stream of n*nx*nr |psi| levels then as many
arg-psi levels, index f*nx*nr + i*nr + r (x = x0 + i*step, y = r*step >= 0, z = 0); levels are of each frame's own peak, the
header's `peaks`. File 'SPHW' (spil only): Re psi on 96 x 64 x 64 points, int8 + 128, levels of each stored frame's peak (`wpeaks`).
The notebook is a one-line loader; the code that runs is shapes3d_run.py (written here too) and solver3d.py at the pinned commit.
Usage: python3 build_shapes3d.py <commit>   (commit: one that already holds solver3d.py and shapes3d_run.py)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-shapes/"
smoke = json.load(open(os.path.join(HERE, "..", "schrodinger-sphere", "smoke.ipynb")))
c1 = smoke["cells"][1]["source"]          # GPU check: stops at once if there is no GPU
md0 = ("# Schrodinger, Fig. 14: the remaining 3D cases (GPU, JAX). An electron wave meets a barrier, solved in 3D (split-step Fourier, 128^3 points, hbar = m = 1): "
       "the coin and the tube, the wells and the hard ball, and a spherical wave from the side onto a ball, a flat wall and a pillar. 1458 runs on both GPUs. "
       "Each run is written when it finishes; index.json lists them with SHA-256. The code is fetched from the website's repository at a pinned commit and printed below.")
c3 = r'''import threading, queue, datetime, hashlib, struct, zlib, traceback, numpy as np
GEN = datetime.datetime.utcnow().strftime("%Y-%m-%d"); OUTD = f"/kaggle/working/{GEN}/shapes3d"
N, L, DT, NF = 128, 64.0, 0.01, 48
LIMIT_S = 8400                                              # no new run starts after this many seconds
WAVE = (slice(16, 112), slice(32, 96), slice(32, 96))       # x -24..24, y and z -16..16 at 0.5 a
HARD = 1e6                                                  # the grid's name for the hard wall; the solver uses HARD_V
Es = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
V13 = [-4.0, -2.0, -1.0, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, HARD]
GROUPS = dict(
    sphere=dict(Vs=[-4.0, -2.0, -1.0, HARD], sizes=[2.0, 3.0, 4.0, 5.0, 6.0]),
    coin=dict(Vs=V13, sizes=[2.0, 3.0, 4.0, 5.0, 6.0]),
    tube=dict(Vs=V13, sizes=[2.0, 3.0, 4.0, 5.0, 6.0]),
    soff=dict(Vs=[-2.0, 2.0, 6.0, HARD], sizes=[4.0]),
    sslab=dict(Vs=[-2.0, 2.0, 6.0, HARD], sizes=[1.0]),
    spil=dict(Vs=[-2.0, 2.0, 6.0, HARD], sizes=[4.0]))
def nsteps(shape, i, j):
    tr = 22.0 if shape in SHELLS else 30.0
    return round(tr / np.sqrt(2 * Es[i]) / DT) * (HARD_SUB if GROUPS[shape]["Vs"][j] >= HARD else 1)
jobs = [(sh, i, j, k) for sh, G in GROUPS.items() for i in range(len(Es)) for j in range(len(G["Vs"])) for k in range(len(G["sizes"]))]
jobs.sort(key=lambda t: -nsteps(t[0], t[1], t[2]))          # long runs first
for sh in GROUPS: os.makedirs(f"{OUTD}/{sh}", exist_ok=True)
total_steps = sum(nsteps(sh, i, j) for sh, i, j, k in jobs)
say(f"{len(jobs)} runs; cells x steps x time per cell-step = {N**3} x {total_steps} x 1.2e-9 s = {N**3*total_steps*1.2e-9/3600:.2f} GPU hours "
    f"(1.2 ns measured on a T4 over the 405 sphere runs of 2026-11-12); on two GPUs about {N**3*total_steps*1.2e-9/2/60:.0f} min")
Q = queue.Queue(); [Q.put(j) for j in jobs]
INDEX, DONE, LOCK, ERR, SKIPPED = [], [0], threading.Lock(), [], [0]
JL = open(OUTD + "/runs.jsonl", "a")
def pack(head, body_bytes, magic):
    hb = json.dumps(head, separators=(",", ":")).encode()
    return magic + struct.pack("<I", len(hb)) + hb + zlib.compress(body_bytes, 9)
def one(g, dev, sh, i, j, k):
    G = GROUPS[sh]; V0 = G["Vs"][j]; size = G["sizes"][k]; hard = V0 >= HARD
    r = run3(g, sh, Es[i], V0, size, hard=hard, dt=DT, nframes=NF, wave=WAVE if sh == "spil" else None)
    cv = np.round(r["curves"], 6).tolist(); pk = [float(p) for p in r["peaks"]]
    head = dict(E=Es[i], V0=V0, R=size, size=size, shape=sh, hard=hard, i=i, j=j, k=k, n=NF, nx=N, nr=N // 2, x0=-L / 2, step=L / N,
                steps=int(r["steps"]), dt=r["dt"], frame_dt=r["frame_dt"], wall=round(float(r["wall"]), 2), device=str(dev),
                wave="shell" if sh in SHELLS else "packet", peaks=[round(p / pk[0], 6) for p in pk], curves=cv)
    if hard: head["hard_V"] = HARD_V
    if sh in SHELLS: head.update(src_x=SRC_X, shell_r0=SH_R0, shell_sigma0=SH_S0)
    if sh == "coin": head["thickness"] = COIN_A
    if sh == "tube": head["wall_thickness"] = TUBE_W
    body = pack(head, r["amp"].tobytes() + r["phase"].tobytes(), b"SPHC")
    name = f"{sh}/e{i}_v{j}_s{k}.bin"
    open(f"{OUTD}/{name}", "wb").write(body)
    t, n, b, a, sy = r["curves"][-1]
    rec = dict(file=name, shape=sh, i=i, j=j, k=k, E=Es[i], V0=V0, size=size, hard=hard, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
               steps=int(r["steps"]), dt=r["dt"], wall=head["wall"], behind=round(float(b), 6), ahead=round(float(a), 6), norm_end=round(float(n), 6), device=str(dev))
    if r["wave"] is not None:
        w = r["wave"]; fr = r["wframes"]
        wh = dict(E=Es[i], V0=V0, R=size, shape=sh, hard=hard, i=i, j=j, k=k, n=int(w.shape[0]), dims=list(w.shape[1:]), x0=-24.0, y0=-16.0, z0=-16.0, step=0.5,
                  kind="re", L=L, steps=int(r["steps"]), dt=r["dt"], wall=head["wall"], device=str(dev), frames=fr,
                  wscale=[round(p / pk[0], 6) for p in r["wpeaks"]], curves=[cv[f] for f in fr])
        wb = pack(wh, (w.astype(np.int16) + 128).astype(np.uint8).tobytes(), b"SPHW")
        wname = f"{sh}/w_e{i}_v{j}_s{k}.bin"
        open(f"{OUTD}/{wname}", "wb").write(wb)
        rec.update(wave_file=wname, wave_bytes=len(wb), wave_sha256=hashlib.sha256(wb).hexdigest())
    with LOCK:
        DONE[0] += 1; INDEX.append(rec); JL.write(json.dumps(rec) + "\n"); JL.flush()
        say(f"{DONE[0]:4d}/{len(jobs)} {sh} E={Es[i]} V0={'hard' if hard else V0} size={size} on {dev}: {r['steps']} steps, {r['wall']:.1f} s, {len(body)/1e3:.0f} kB, norm {n:.3f}, ahead {a:.3f}")
def worker(dev):
    bad = 0
    with jax.default_device(dev):
        g = setup(N, L)
        while bad < 5:
            if time.time() - T0 > LIMIT_S:
                with LOCK: SKIPPED[0] = 1
                return
            try: sh, i, j, k = Q.get_nowait()
            except queue.Empty: return
            try:
                one(g, dev, sh, i, j, k); bad = 0
            except Exception as e:
                bad += 1
                with LOCK: ERR.append(dict(job=[sh, i, j, k], error=repr(e)[:500]))
                say("RUN FAILED", sh, i, j, k, "on", dev, repr(e)[:300]); say(traceback.format_exc()[-600:])
DEVS = [d for d in jax.devices() if d.platform == "gpu"]
TS = time.time()
threads = [threading.Thread(target=worker, args=(d,)) for d in DEVS]
[t.start() for t in threads]; [t.join() for t in threads]
SWEEP_S = time.time() - TS; JL.close()
say(f"{DONE[0]} of {len(jobs)} runs in {SWEEP_S:.0f} s on {len(DEVS)} GPU(s); failed {len(ERR)}; not started {Q.qsize()}")
'''
c4 = r'''# ---- the index, one tar per shape, timing ----
import tarfile
INDEX.sort(key=lambda r: r["file"])
left = []
while True:
    try: left.append(list(Q.get_nowait()))
    except queue.Empty: break
idx = dict(generated=GEN, kind="shapes3d", N=N, L=L, dt=DT, nframes=NF, Es=Es, hard_V0=HARD, hard_V=HARD_V, hard_substeps=HARD_SUB,
           groups={sh: dict(Vs=G["Vs"], sizes=G["sizes"]) for sh, G in GROUPS.items()}, coin_thickness=COIN_A, tube_wall=TUBE_W,
           shell=dict(src_x=SRC_X, r0=SH_R0, sigma0=SH_S0, travel=22.0), packet=dict(x0=-14.0, sigma0=3.0, travel=30.0),
           device=jax.devices()[0].device_kind, gpus=len(DEVS), sweep_s=round(SWEEP_S, 1), failed=ERR, not_started=left,
           method="Strang split-step Fourier, 3D; hard wall: height 200 with a step four times shorter (no probability removed)",
           units="hbar = m = 1, lengths in the grid unit a", runs=INDEX)
json.dump(idx, open(OUTD + "/index.json", "w"), separators=(",", ":"))
for sh in GROUPS:
    files = sorted(os.listdir(f"{OUTD}/{sh}"))
    try:
        with tarfile.open(f"{OUTD}/{sh}.tar", "w") as tf:
            for f in files: tf.add(f"{OUTD}/{sh}/{f}", arcname=f"{sh}/{f}")
        with tarfile.open(f"{OUTD}/{sh}.tar") as tf: ok = len(tf.getnames()) == len(files)
        if ok:
            for f in files: os.remove(f"{OUTD}/{sh}/{f}")
            os.rmdir(f"{OUTD}/{sh}")
        say(sh, len(files), "files ->", f"{sh}.tar", f"{os.path.getsize(f'{OUTD}/{sh}.tar')/1e6:.1f} MB", "ok" if ok else "TAR CHECK FAILED: files kept")
    except Exception as e:
        say("TAR FAILED", sh, repr(e)[:300], "(the files stay as they are)")
json.dump(dict(total_s=round(time.time() - T0, 1), sweep_s=round(SWEEP_S, 1), gpus=len(DEVS), runs_done=DONE[0], runs_planned=len(jobs),
               failed=len(ERR), not_started=len(left), gpu_seconds_of_runs=round(sum(r["wall"] for r in INDEX), 1),
               steps_total=int(sum(r["steps"] for r in INDEX))), open(OUTD + "/timing.json", "w"))
say(f"all done in {time.time()-T0:.0f} s")
'''
# The notebook itself is a short loader: it fetches solver3d.py and shapes3d_run.py (the three cells above as one file) from
# the website's repository at the pinned commit, prints the code into its log and runs it. So the code that ran is the code in git.
run_py = "\n".join([c1, 'exec(open("solver3d.py").read())\nsay("solver3d.py and shapes3d_run.py from the repository, as fetched by the loader cell")\n', c3, c4])
open(os.path.join(HERE, "shapes3d_run.py"), "w").write(run_py)
if os.environ.get("FLAT"):   # the run file and the solver as one file, for a name check: FLAT=out.py python3 build_shapes3d.py; python3 -m pyflakes out.py
    open(os.environ["FLAT"], "w").write(run_py.replace('exec(open("solver3d.py").read())', open(os.path.join(HERE, "solver3d.py")).read()))
loader = ("import urllib.request; B = '" + BASE + "'; [urllib.request.urlretrieve(B + f, f) for f in ('solver3d.py', 'shapes3d_run.py')]; "
          "print(open('shapes3d_run.py').read()); exec(open('shapes3d_run.py').read())")
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="s0"),
         dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=loader, id="s1")]
nb = dict(cells=cells, metadata=smoke["metadata"], nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "shapes3d.ipynb"), "w").write(json.dumps(nb))
print("notebook bytes", len(json.dumps(nb)), "run file bytes", len(run_py))
