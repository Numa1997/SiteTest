"""Writes flat.ipynb: the Kaggle notebook (CPU, no GPU) of Fig. 14's flat wall. It fetches flat.py at the given commit,
computes every run of the grid (9 energies x 13 barrier heights, wells and the hard wall included, x 5 thicknesses = 585 runs)
on all CPU cores, and files under /kaggle/working/<YYYY-MM-DD>/flat/ one file per run in the website's 'SPHC' format
(tools/kaggle/schrodinger-sphere/to_site_axisym.py: the half-plane rho >= 0 through the flight axis, 128 x 64 points 0.5 a
apart, |psi| and arg psi levels, 48 frames, probability curves), plus index.json with the SHA-256 of every file.
The header adds shape = 'slab', a (thickness), hard (true for psi = 0 in the slab), T_packet (the exact packet transmission)
and R = a/2, so that 'behind' (x < -R) and 'ahead' (x > R) mean the same as for the sphere.
Usage: python3 build_flat.py <commit>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-shapes/"
md0 = """# Fig. 14, flat wall: a wave packet meets a slab (CPU)

The same 3D Gaussian packet as the sphere (σ₀ = 3, x₀ = −14, k₀ = √(2E), ħ = m = 1) meets a slab V = V₀ for |x| < a/2, or a hard
wall (ψ = 0 in the slab). V depends on x only, so ψ(x, y, z, t) = χ(x, t) g(y, t) g(z, t) exactly: χ is solved in 1D
(Crank–Nicolson, fourth-order Laplacian), g is the free Gaussian. 585 runs: 9 energies × 13 heights (wells, barriers, hard wall) × 5 thicknesses.
Files are filed under the generation date, with the SHA-256 of each in index.json."""
c1 = f'''import urllib.request, os, sys, time
BASE = "{BASE}"
for f in ("flat.py", "check_flat.py"):
    urllib.request.urlretrieve(BASE + f, f)
sys.path.insert(0, "."); T0 = time.time()
print("code from", BASE, "; cores", os.cpu_count())
'''
c2 = r'''import subprocess; print(subprocess.run([sys.executable, "-c", "import sympy"], capture_output=True).returncode == 0 or subprocess.run([sys.executable, "-m", "pip", "install", "-q", "sympy"]).returncode)
exec(open("check_flat.py").read())   # the formula checks, printed into this notebook's log
'''
c3 = r'''import json, struct, zlib, hashlib, datetime, numpy as np
from multiprocessing import Pool
from flat import run, T_packet, HARD
GEN = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"); OUTD = f"/kaggle/working/{GEN}"; os.makedirs(OUTD + "/flat", exist_ok=True)
Es = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
Vs = [-4.0, -2.0, -1.0, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, HARD]
As = [0.5, 1.0, 1.5, 2.0, 3.0]
jobs = [(i, j, k) for i in range(len(Es)) for j in range(len(Vs)) for k in range(len(As))]
def one(job):
    i, j, k = job; E, V0, a = Es[i], Vs[j], As[k]
    r = run(E, V0, a)
    pl = r["plane"]; amp = np.abs(pl); ph = np.angle(pl)
    a0 = amp[0].max()
    qa = np.clip(np.round(255 * amp / a0), 0, 255).astype(np.uint8)
    qp = (np.round((ph + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
    n, nx, nr = qa.shape
    Tp = T_packet(E, V0, a)
    head = dict(E=E, V0=V0, R=a / 2, a=a, shape="slab", hard=bool(r["hard"]), i=i, j=j, k=k, n=n, nx=nx, nr=nr, x0=-32.0, step=0.5,
                steps=int(r["steps"]), dt=r["dt"], dx=r["dx"], wall=round(r["wall"], 2), device="cpu", T_packet=round(Tp, 6),
                curves=np.round(r["curves"], 6).tolist())
    hb = json.dumps(head, separators=(",", ":")).encode()
    body = b"SPHC" + struct.pack("<I", len(hb)) + hb + zlib.compress(qa.tobytes() + qp.tobytes(), 9)
    name = f"e{i}_v{j}_a{k}.bin"; open(f"{OUTD}/flat/{name}", "wb").write(body)
    t, nm, b, ah, sy = r["curves"][-1]
    return dict(file=name, i=i, j=j, k=k, E=E, V0=V0, a=a, R=a / 2, hard=bool(r["hard"]), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                steps=int(r["steps"]), wall=head["wall"], behind=round(b, 6), ahead=round(ah, 6), norm_end=round(nm, 8), T_packet=round(Tp, 6))
TS = time.time()
with Pool(os.cpu_count()) as pool:
    runs = []
    for m, r in enumerate(pool.imap_unordered(one, jobs), 1):
        runs.append(r)
        if m % 45 == 0 or m == len(jobs): print(f"{m:3d}/{len(jobs)} runs, {time.time()-TS:.0f} s")
runs.sort(key=lambda r: r["file"])
dev = max(abs(r["ahead"] - r["T_packet"]) for r in runs if not r["hard"])
json.dump(dict(generated=GEN, kind="axisym", shape="slab", Es=Es, Vs=Vs, As=As, Rs=[a / 2 for a in As], hard_V0=HARD, L=64.0, dt=0.01, dx=0.05, X=200.0,
               nframes=48, sigma0=3.0, x0=-14.0, travel=30.0, device="cpu", cores=os.cpu_count(), sweep_s=round(time.time() - TS, 1),
               method="Crank-Nicolson, fourth-order Laplacian, 1D; psi = chi(x) g(y) g(z)", largest_ahead_minus_T_packet=round(dev, 6),
               units="hbar = m = 1, lengths in the grid unit a", runs=runs), open(OUTD + "/index.json", "w"), separators=(",", ":"))
print(f"all {len(runs)} runs in {time.time()-TS:.0f} s; {sum(r['bytes'] for r in runs)/1e6:.1f} MB; largest |ahead - T_packet| {dev:.5f}; done in {time.time()-T0:.0f} s")
'''
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="f0")]
for n, c in enumerate([c1, c2, c3]):
    cells.append(dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c, id=f"f{n+1}"))
nb = dict(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "flat.ipynb"), "w").write(json.dumps(nb, indent=1))
print("flat.ipynb written")
