"""Writes full.ipynb (the copy in git is the notebook as run on 2026-11-12, version 1; since then the builder files every output
under the generation date, /kaggle/working/<YYYY-MM-DD>/, as the storage rule asks), the Kaggle notebook that computes every run of the grid (9 energies x 9 barrier heights x 5 radii
= 405 runs at 128^3 cells) on both GPUs of the session, stores each run as runs/e{i}_v{j}_r{k}.json, and writes a
preview panel with 45 of them (R = 4, every other energy).
Usage: python3 build_full.py <commit>  (the notebook fetches solver.py, pack.py, panel_template.html at that commit)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-sphere/"
smoke = json.load(open(os.path.join(HERE, "smoke.ipynb")))
c1 = smoke["cells"][1]["source"]          # GPU check (same as the smoke test)
md0 = """# Schrödinger sphere: the full grid of runs (GPU, JAX)

A wave packet meets a sphere of raised potential, solved in 3D (split-step Fourier, 128³ cells, ħ = m = 1).
Every combination of 9 packet energies E, 9 barrier heights V₀ and 5 sphere radii R is computed: 405 runs, shared
between the two GPUs. Each run is stored in `runs/` as a small JSON file (frames of |ψ| and arg ψ in the plane z = 0,
zlib + base64, and the probability curves). `index.json` lists them. The panel under the last cell is a preview with
45 runs (R = 4, every other energy); the website loads every run from the stored files."""
c2 = f'''# the solver, the packer and the panel, fetched from the website's repository at commit {COMMIT}
import urllib.request
BASE = "{BASE}"
for f in ("solver.py", "pack.py", "panel_template.html"):
    urllib.request.urlretrieve(BASE + f, f)
exec(open("solver.py").read()); exec(open("pack.py").read())
TEMPLATE = open("panel_template.html").read()
say("code from", BASE)
'''
c3 = r'''# ---- the grid: every run, on both GPUs ----
import threading, queue
N, L, DT, OUT, NF, S0 = 128, 64.0, 0.01, 128, 48, 3.0
Es = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
Vs = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
Rs = [2.0, 3.0, 4.0, 5.0, 6.0]
import datetime
GEN = datetime.datetime.utcnow().strftime("%Y-%m-%d")      # the generation date: every output is filed under it (docs/kaggle-pipeline.md, "Storage")
OUTD = f"/kaggle/working/{GEN}"
os.makedirs(OUTD + "/runs", exist_ok=True)
jobs = sorted(((i, j, k) for i in range(len(Es)) for j in range(len(Vs)) for k in range(len(Rs))), key=lambda t: Es[t[0]])  # slow ones first
total_steps = sum(round(30 / np.sqrt(2 * Es[i]) / DT) for i, j, k in jobs)
say(f"{len(jobs)} runs, about {total_steps} steps; measured 2.6 ms per step at 128^3 on one T4 -> about {total_steps*2.6e-3/60:.0f} min on one GPU")
Q = queue.Queue(); [Q.put(j) for j in jobs]
INDEX, DONE, LOCK, ERR = [], [0], threading.Lock(), []
def worker(dev):
    try:
        with jax.default_device(dev):
            g = setup(N, L)
            while True:
                try: i, j, k = Q.get_nowait()
                except queue.Empty: return
                r = run(g, E=Es[i], V0=Vs[j], R=Rs[k], sigma0=S0, dt=DT, nframes=NF, out=OUT)
                rec = dict(E=r["E"], V0=r["V0"], R=r["R"], i=i, j=j, k=k, n=int(r["amp"].shape[0]), steps=int(r["steps"]),
                           wall=round(float(r["wall"]), 2), device=str(dev), amp=b64z(r["amp"]), ph=b64z(r["phase"]),
                           c=np.round(r["curves"], 6).tolist())
                name = f"e{i}_v{j}_r{k}.json"
                with open(OUTD + "/runs/" + name, "w") as f: json.dump(rec, f, separators=(",", ":"))
                with LOCK:
                    DONE[0] += 1; t, n, b, a, sy = r["curves"][-1]
                    INDEX.append(dict(file=name, E=r["E"], V0=r["V0"], R=r["R"], steps=int(r["steps"]), wall=rec["wall"],
                                      behind=round(float(b), 5), ahead=round(float(a), 5), norm_end=round(float(n), 6), device=str(dev)))
                    say(f"{DONE[0]:3d}/{len(jobs)} E={Es[i]} V0={Vs[j]} R={Rs[k]} on {dev}: {r['steps']} steps, {r['wall']:.1f} s, ahead {a:.3f}")
    except Exception as e:
        ERR.append(repr(e)); say("WORKER ERROR", dev, repr(e))
DEVS = [d for d in jax.devices() if d.platform == "gpu"]
TS = time.time()
threads = [threading.Thread(target=worker, args=(d,)) for d in DEVS]
[t.start() for t in threads]; [t.join() for t in threads]
assert not ERR and DONE[0] == len(jobs), (ERR, DONE)
SWEEP_S = time.time() - TS
INDEX.sort(key=lambda r: r["file"])
json.dump(dict(generated=GEN, Es=Es, Vs=Vs, Rs=Rs, N=N, L=L, dt=DT, out=OUT, nframes=NF, sigma0=S0, device=jax.devices()[0].device_kind,
               gpus=len(DEVS), sweep_s=round(SWEEP_S, 1), runs=INDEX), open(OUTD + "/index.json", "w"), indent=0)
say(f"all {len(jobs)} runs in {SWEEP_S:.0f} s on {len(DEVS)} GPU(s); stored {sum(os.path.getsize(OUTD+'/runs/'+r['file']) for r in INDEX)/1e6:.0f} MB")
'''
c4 = r'''# ---- preview panel: 45 runs (R = 4, every other energy), read back from the stored files ----
recs = []
for r in INDEX:
    if r["R"] == 4.0 and Es.index(r["E"]) % 2 == 0:
        d = json.load(open(OUTD + "/runs/" + r["file"]))
        recs.append(d)
R4 = [dict(id=n, i=d["i"], j=d["j"], k=d["k"], E=d["E"], V0=d["V0"], R=d["R"], n=d["n"], steps=d["steps"], wall=d["wall"], amp=d["amp"], ph=d["ph"], c=d["c"]) for n, d in enumerate(recs)]
D = dict(Es=Es, Vs=Vs, Rs=Rs, out=OUT, L=L, dt=DT, s0=S0, cells=f"{N}³", device="Kaggle " + jax.devices()[0].device_kind, start=dict(sE=4, sV=5, sR=2), runs=R4)
page = (TEMPLATE.replace("__DATA__", json.dumps(D, separators=(",", ":"))).replace("__CELLS__", f"{N}³ = {N**3:,}".replace(",", " "))
        .replace("__DT__", f"Δt = {DT}").replace("__L__", f"{L:g} a").replace("__NF__", str(NF)).replace("__OUT__", str(OUT))
        .replace("Hollow dots: not computed yet.", "Hollow dots: computed and stored in runs/, but not inside this preview file (it holds R = 4 and every other energy only)."))
open(OUTD + "/schrodinger_sphere_preview.html", "w").write(page)
json.dump(dict(total_s=round(time.time() - T0, 1), sweep_s=round(SWEEP_S, 1), gpus=len(DEVS)), open(OUTD + "/timing.json", "w"))
say(f"preview panel {len(page)/1e6:.1f} MB; all done in {time.time()-T0:.0f} s")
import html as _h
from IPython.display import HTML, display
display(HTML(f'<iframe srcdoc="{_h.escape(page)}" style="width:100%;height:1250px;border:0"></iframe>'))
'''
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="f0")]
for n, c in enumerate([c1, c2, c3, c4]):
    cells.append(dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c, id=f"f{n+1}"))
nb = dict(cells=cells, metadata=smoke["metadata"], nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "full.ipynb"), "w").write(json.dumps(nb))
print("notebook bytes", len(json.dumps(nb)))
