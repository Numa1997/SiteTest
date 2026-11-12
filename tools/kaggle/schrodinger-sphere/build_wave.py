"""Writes wave3d.ipynb: the Kaggle notebook of the 3D wave generation of Fig. 14. On both GPUs it computes the 81 runs at R = 4
(9 energies x 9 barrier heights) on 128^3 points and stores, per run, 32 frames of the wave itself, Re psi, on the grid points
of the box x in [-24, 24), y and z in [-16, 16) (96 x 64 x 64 points, 0.5 a apart, every computed point, nothing averaged), as
int8 levels of the first frame's peak |psi|, with the probability curves from the whole psi.
File (little-endian): 'SPHW', uint32 header length H, H bytes of JSON header (E, V0, R, i, j, k, n, shape, x0, y0, z0, step, kind,
L, steps, dt, wall, device, curves [[t, norm, behind, ahead, sigma_y] per frame]), then one zlib stream of n*96*64*64 bytes,
each the int8 level plus 128, frame-major, then x, y, z. Files under /kaggle/working/<YYYY-MM-DD>/wave3d/, index.json with SHA-256.
Usage: python3 build_wave.py <commit>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-sphere/"
smoke = json.load(open(os.path.join(HERE, "smoke.ipynb")))
c1 = smoke["cells"][1]["source"]
md0 = """# Schrödinger sphere: the 3D wave (GPU, JAX)

An electron wave packet meets a sphere of raised potential, solved in 3D (split-step Fourier, 128³ points, ħ = m = 1). For
the 81 runs at R = 4 (9 energies × 9 barrier heights) every one of 32 frames stores the wave itself, Re ψ, on every computed
point of the box x ∈ [−24, 24), y, z ∈ [−16, 16), for the website's 3D view. Files are filed under the generation date."""
c2 = f'''import urllib.request
BASE = "{BASE}"
urllib.request.urlretrieve(BASE + "solver.py", "solver.py")
exec(open("solver.py").read())
say("code from", BASE)
'''
c3 = r'''import threading, queue, datetime, hashlib, struct, zlib
GEN = datetime.datetime.utcnow().strftime("%Y-%m-%d"); OUTD = f"/kaggle/working/{GEN}"; os.makedirs(OUTD + "/wave3d", exist_ok=True)
N, L, DT, NF, S0 = 128, 64.0, 0.01, 32, 3.0
WAVE = (slice(16, 112), slice(32, 96), slice(32, 96))      # x -24..24, y and z -16..16 at 0.5 a: every computed point
Es = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
Vs = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
K = 2   # index of R = 4 in [2, 3, 4, 5, 6]
jobs = sorted(((i, j) for i in range(len(Es)) for j in range(len(Vs))), key=lambda t: Es[t[0]])
total_steps = sum(round(30 / np.sqrt(2 * Es[i]) / DT) for i, j in jobs)
say(f"{len(jobs)} runs, about {total_steps} steps; 2.6 ms per step measured at 128^3 on one T4 -> about {total_steps*2.6e-3/60:.1f} min on one GPU")
Q = queue.Queue(); [Q.put(j) for j in jobs]
INDEX, DONE, LOCK, ERR = [], [0], threading.Lock(), []
def worker(dev):
    try:
        with jax.default_device(dev):
            g = setup(N, L)
            while True:
                try: i, j = Q.get_nowait()
                except queue.Empty: return
                r = run(g, E=Es[i], V0=Vs[j], R=4.0, sigma0=S0, dt=DT, nframes=NF, out=8, wave=WAVE)
                w = r["wave"]
                head = dict(E=r["E"], V0=r["V0"], R=r["R"], i=i, j=j, k=K, n=NF, shape=list(w.shape[1:]), x0=-24.0, y0=-16.0, z0=-16.0, step=0.5,
                            kind="re", L=L, steps=int(r["steps"]), dt=DT, wall=round(float(r["wall"]), 2), device=str(dev), curves=np.round(r["curves"], 6).tolist())
                hb = json.dumps(head, separators=(",", ":")).encode()
                body = b"SPHW" + struct.pack("<I", len(hb)) + hb + zlib.compress((w.astype(np.int16) + 128).astype(np.uint8).tobytes(), 9)
                name = f"e{i}_v{j}_r{K}.bin"
                open(OUTD + "/wave3d/" + name, "wb").write(body)
                with LOCK:
                    DONE[0] += 1; t, n, b, a, sy = r["curves"][-1]
                    INDEX.append(dict(file=name, i=i, j=j, k=K, E=r["E"], V0=r["V0"], R=r["R"], bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                                      steps=int(r["steps"]), wall=head["wall"], behind=round(float(b), 5), ahead=round(float(a), 5), norm_end=round(float(n), 6), device=str(dev)))
                    say(f"{DONE[0]:3d}/{len(jobs)} E={Es[i]} V0={Vs[j]} on {dev}: {r['steps']} steps, {r['wall']:.1f} s, {len(body)/1e6:.2f} MB, ahead {a:.3f}")
    except Exception as e:
        ERR.append(repr(e)); say("WORKER ERROR", dev, repr(e))
DEVS = [d for d in jax.devices() if d.platform == "gpu"]
TS = time.time()
threads = [threading.Thread(target=worker, args=(d,)) for d in DEVS]
[t.start() for t in threads]; [t.join() for t in threads]
assert not ERR and DONE[0] == len(jobs), (ERR, DONE)
SWEEP_S = time.time() - TS
INDEX.sort(key=lambda r: r["file"])
json.dump(dict(generated=GEN, kind="wave", Es=Es, Vs=Vs, Rs=[4.0], N=N, L=L, dt=DT, nframes=NF, shape=[96, 64, 64], x0=-24.0, y0=-16.0, z0=-16.0, step=0.5,
               sigma0=S0, x0_packet=-14.0, travel=30.0, device=jax.devices()[0].device_kind, gpus=len(DEVS), sweep_s=round(SWEEP_S, 1), runs=INDEX),
          open(OUTD + "/index.json", "w"), indent=0)
say(f"all {len(jobs)} runs in {SWEEP_S:.0f} s on {len(DEVS)} GPU(s); stored {sum(r['bytes'] for r in INDEX)/1e6:.0f} MB; done in {time.time()-T0:.0f} s")
'''
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="w0")]
for n, c in enumerate([c1, c2, c3]):
    cells.append(dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c, id=f"w{n+1}"))
nb = dict(cells=cells, metadata=smoke["metadata"], nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "wave3d.ipynb"), "w").write(json.dumps(nb))
print("notebook bytes", len(json.dumps(nb)))
