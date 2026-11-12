"""Writes pillar.ipynb: the Kaggle notebook (CPU, no GPU) of Fig. 14's pillar (a round column along z). It fetches pillar.py and
flat.py at the given commit, computes every run of the grid (9 energies x 13 heights, wells and the hard column included, x 5
radii = 585 runs) on all CPU cores, and files under /kaggle/working/<YYYY-MM-DD>/pillar/ one file per run in the 'SPHC' format
of the sphere, but the stored half-plane is the top view (x, y >= 0) at any z: 128 x 64 points 0.5 a apart, |phi| and arg phi
levels, 48 frames, probability curves. The header adds shape = 'pillar', plane = 'xy' and hard. gz.bin holds the free Gaussian
g(z, t) of psi(x, y, z) = phi(x, y) g(z): float32 [energy i][frame f][z = 0, 0.5, ... 31.5][re, im] (every run of one energy
has the same frame times), with its SHA-256 in index.json.
Usage: python3 build_pillar.py <commit>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-shapes/"
md0 = """# Fig. 14, pillar: a wave packet meets a round column (CPU)

The same 3D Gaussian packet as the sphere (σ₀ = 3, x₀ = −14, k₀ = √(2E), ħ = m = 1) meets a column V = V₀ for x² + y² < R²,
unbounded along z, or a hard column (ψ = 0 inside). V does not depend on z, so ψ(x, y, z, t) = φ(x, y, t) g(z, t) exactly: φ is
solved in 2D (split-step Fourier, 128² points, 0.5 a), g is the free Gaussian. 585 runs: 9 energies × 13 heights × 5 radii.
Files are filed under the generation date, with the SHA-256 of each in index.json."""
c1 = f'''import urllib.request, os, sys, time
BASE = "{BASE}"
for f in ("pillar.py", "flat.py", "check_pillar.py"):
    urllib.request.urlretrieve(BASE + f, f)
sys.path.insert(0, "."); T0 = time.time()
print("code from", BASE, "; cores", os.cpu_count())
'''
c2 = r'''exec(open("check_pillar.py").read())   # convergence in dt and the mirror check, printed into this notebook's log
'''
c3 = r'''import json, struct, zlib, hashlib, datetime, numpy as np
from multiprocessing import Pool
from pillar import run, HARD
from flat import gfree
GEN = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"); OUTD = f"/kaggle/working/{GEN}"; os.makedirs(OUTD + "/pillar", exist_ok=True)
Es = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
Vs = [-4.0, -2.0, -1.0, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, HARD]
Rs = [2.0, 3.0, 4.0, 5.0, 6.0]
jobs = [(i, j, k) for i in range(len(Es)) for j in range(len(Vs)) for k in range(len(Rs))]
def one(job):
    i, j, k = job; E, V0, R = Es[i], Vs[j], Rs[k]
    r = run(E, V0, R)
    pl = r["plane"]; amp = np.abs(pl); ph = np.angle(pl)
    a0 = amp[0].max()
    qa = np.clip(np.round(255 * amp / a0), 0, 255).astype(np.uint8)
    qp = (np.round((ph + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
    n, nx, nr = qa.shape
    head = dict(E=E, V0=V0, R=R, shape="pillar", plane="xy", hard=bool(r["hard"]), i=i, j=j, k=k, n=n, nx=nx, nr=nr, x0=-32.0, step=0.5,
                steps=int(r["steps"]), dt=r["dt"], wall=round(r["wall"], 2), device="cpu", curves=np.round(r["curves"], 6).tolist())
    hb = json.dumps(head, separators=(",", ":")).encode()
    body = b"SPHC" + struct.pack("<I", len(hb)) + hb + zlib.compress(qa.tobytes() + qp.tobytes(), 9)
    name = f"e{i}_v{j}_r{k}.bin"; open(f"{OUTD}/pillar/{name}", "wb").write(body)
    t, nm, b, ah, sy = r["curves"][-1]
    return dict(file=name, i=i, j=j, k=k, E=E, V0=V0, R=R, hard=bool(r["hard"]), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                steps=int(r["steps"]), dt=r["dt"], wall=head["wall"], behind=round(b, 6), ahead=round(ah, 6), norm_end=round(nm, 8))
TS = time.time()
with Pool(os.cpu_count()) as pool:
    runs = []
    for m, r in enumerate(pool.imap_unordered(one, jobs), 1):
        runs.append(r)
        if m % 45 == 0 or m == len(jobs): print(f"{m:3d}/{len(jobs)} runs, {time.time()-TS:.0f} s")
runs.sort(key=lambda r: r["file"])
from pillar import run as _r
zz = 0.5 * np.arange(64); G = np.zeros((len(Es), 48, 64, 2), np.float32)
for i, E in enumerate(Es):
    fdt = max(1, int(round(30.0 / np.sqrt(2 * E) / 0.0025)) // 47) * 0.0025
    for f in range(48):
        g = gfree(zz, f * fdt, 3.0); G[i, f, :, 0] = g.real; G[i, f, :, 1] = g.imag
gzb = G.tobytes(); open(OUTD + "/pillar/gz.bin", "wb").write(gzb)
json.dump(dict(generated=GEN, kind="plane", shape="pillar", Es=Es, Vs=Vs, Rs=Rs, hard_V0=HARD, L=64.0, N=128, dt=0.0025, hard_dt=0.0005,
               nframes=48, sigma0=3.0, x0=-14.0, travel=30.0, device="cpu", cores=os.cpu_count(), sweep_s=round(time.time() - TS, 1),
               gz=dict(file="gz.bin", sha256=hashlib.sha256(gzb).hexdigest(), shape=[len(Es), 48, 64, 2], z_step=0.5, what="free Gaussian g(z, t) per energy and frame, [re, im]"),
               method="Strang split-step Fourier, 2D; psi = phi(x, y) g(z); hard column by setting psi = 0 inside after every step",
               units="hbar = m = 1, lengths in the grid unit a", runs=runs), open(OUTD + "/index.json", "w"), separators=(",", ":"))
print(f"all {len(runs)} runs in {time.time()-TS:.0f} s; {sum(r['bytes'] for r in runs)/1e6:.1f} MB; done in {time.time()-T0:.0f} s")
'''
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="p0")]
for n, c in enumerate([c1, c2, c3]):
    cells.append(dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c, id=f"p{n+1}"))
nb = dict(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "pillar.ipynb"), "w").write(json.dumps(nb, indent=1))
print("pillar.ipynb written")
