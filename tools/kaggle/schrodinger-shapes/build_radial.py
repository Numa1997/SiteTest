"""Writes radial.ipynb: the Kaggle notebook (CPU, no GPU) of Fig. 14's spherical waves. It fetches radial.py and flat.py at the
given commit and computes 1170 runs on all CPU cores: 2 kinds ('out': a shell leaving the centre through a spherical shell wall
at radius 16 of thickness d; 'in': a shell closing in on a ball of radius R at the centre) x 9 energies x 13 heights (wells and a
hard wall included) x 5 sizes. Each run is filed under /kaggle/working/<YYYY-MM-DD>/radial/ as 'SPHR' (little-endian): 'SPHR',
uint32 header length H, H bytes JSON header (E, V0, size, kind, hard, n, nr, rstep, peaks [largest |psi| per frame], steps, dt,
wall, T_packet for 'out', curves [[t, norm, P(r below the barrier), P(r above it), mean r] per frame]), then one zlib stream:
n*nr bytes |psi| levels (0..255 of that frame's peak) and n*nr bytes arg psi levels (0..255 for -pi..pi, 0 where |psi| < 3
levels), psi(r) at r = 0, 0.5, ... 48. index.json lists every file with its SHA-256.
Usage: python3 build_radial.py <commit>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-shapes/"
md0 = """# Fig. 14, spherical waves (CPU)

A wave whose crests are spheres about the origin: a shell leaving the centre through a spherical shell wall, or a shell closing in
on a ball at the centre. With l = 0, u = r psi solves the 1D equation on the half-line with u(0) = 0, so each run is exact in 1D
(Crank–Nicolson, fourth-order Laplacian). 1170 runs. Files are filed under the generation date, with the SHA-256 of each in index.json."""
c1 = f'''import urllib.request, os, sys, time
BASE = "{BASE}"
for f in ("radial.py", "flat.py"):
    urllib.request.urlretrieve(BASE + f, f)
sys.path.insert(0, "."); T0 = time.time()
print("code from", BASE, "; cores", os.cpu_count())
'''
c2 = r'''import json, struct, zlib, hashlib, datetime, numpy as np
from multiprocessing import Pool
from radial import run, HARD
from flat import T_packet
GEN = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"); OUTD = f"/kaggle/working/{GEN}"; os.makedirs(OUTD + "/radial", exist_ok=True)
Es = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
Vs = [-4.0, -2.0, -1.0, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, HARD]
SIZES = {"out": [0.5, 1.0, 1.5, 2.0, 3.0], "in": [2.0, 3.0, 4.0, 5.0, 6.0]}
jobs = [(kd, i, j, k) for kd in ("out", "in") for i in range(len(Es)) for j in range(len(Vs)) for k in range(5)]
def one(job):
    kd, i, j, k = job; E, V0, size = Es[i], Vs[j], SIZES[kd][k]
    r = run(E, V0, size, kd)
    pr = r["profile"]; amp = np.abs(pr); ph = np.angle(pr); peaks = amp.max(axis=1)
    qa = np.clip(np.round(255 * amp / peaks[:, None]), 0, 255).astype(np.uint8)
    qp = (np.round((ph + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
    n, nr = qa.shape
    Tp = T_packet(E, V0, size, s0=2.0) if kd == "out" else None
    head = dict(E=E, V0=V0, size=size, kind=kd, hard=bool(r["hard"]), i=i, j=j, k=k, n=n, nr=nr, rstep=0.5, peaks=[float(f"{p:.6g}") for p in peaks],
                steps=int(r["steps"]), dt=r["dt"], dx=r["dx"], wall=round(r["wall"], 2), device="cpu", T_packet=None if Tp is None else round(Tp, 6),
                curves=np.round(r["curves"], 6).tolist())
    hb = json.dumps(head, separators=(",", ":")).encode()
    body = b"SPHR" + struct.pack("<I", len(hb)) + hb + zlib.compress(qa.tobytes() + qp.tobytes(), 9)
    name = f"{kd}_e{i}_v{j}_s{k}.bin"; open(f"{OUTD}/radial/{name}", "wb").write(body)
    t, nm, lo, hi, rm = r["curves"][-1]
    return dict(file=name, kind=kd, i=i, j=j, k=k, E=E, V0=V0, size=size, hard=bool(r["hard"]), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                steps=int(r["steps"]), wall=head["wall"], low=round(lo, 6), high=round(hi, 6), norm_end=round(nm, 8), T_packet=head["T_packet"])
TS = time.time()
with Pool(os.cpu_count()) as pool:
    runs = []
    for m, rr in enumerate(pool.imap_unordered(one, jobs), 1):
        runs.append(rr)
        if m % 90 == 0 or m == len(jobs): print(f"{m:4d}/{len(jobs)} runs, {time.time()-TS:.0f} s")
runs.sort(key=lambda r: r["file"])
outs = [r for r in runs if r["kind"] == "out" and not r["hard"]]
fin = [r for r in outs if r["norm_end"] - r["low"] - r["high"] < 0.002]
dev = max(abs(r["high"] - r["T_packet"]) for r in fin)
json.dump(dict(generated=GEN, kind="radial", shape="spherical", Es=Es, Vs=Vs, sizes=SIZES, hard_V0=HARD, dt=0.01, dx=0.05, X=200.0, nframes=48, nr=97, rstep=0.5,
               sigma0=2.0, r0={"out": 6.0, "in": 28.0}, wall_radius_out=16.0, travel={"out": 24.0, "in": 40.0}, device="cpu", cores=os.cpu_count(),
               sweep_s=round(time.time() - TS, 1), method="u = r psi, l = 0: Crank-Nicolson, fourth-order Laplacian, odd extension for u(0) = 0",
               check=dict(finished_out_runs=len(fin), largest_high_minus_T_packet=round(dev, 6)),
               units="hbar = m = 1, lengths in the unit a", runs=runs), open(OUTD + "/index.json", "w"), separators=(",", ":"))
print(f"all {len(runs)} runs in {time.time()-TS:.0f} s; {sum(r['bytes'] for r in runs)/1e6:.1f} MB; finished 'out' runs: {len(fin)}, largest |P(beyond the wall) - T_packet| {dev:.5f}; done in {time.time()-T0:.0f} s")
'''
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="r0")]
for n, c in enumerate([c1, c2]):
    cells.append(dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c, id=f"r{n+1}"))
nb = dict(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "radial.ipynb"), "w").write(json.dumps(nb, indent=1))
print("radial.ipynb written")
