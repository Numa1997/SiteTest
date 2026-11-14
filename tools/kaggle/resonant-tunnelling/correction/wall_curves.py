"""Fig. 15 correction, walls: the curve gate (D2) for the wall runs that pass the T gate.

For each run: download the stored file over HTTPS (SHA-256 checked against the index), build the exact chi at the stored frame
times (exact_wall.Exact), and compare
  - the trapped share between the walls, P_well(t): stored curve vs exact, at every stored frame;
  - the probability along x, p(x, t) = Int |psi|^2 dy dz, on the box interior (|x| < inner half-length): L1 distance
    Int |p_run - p_exact| dx at every stored frame (the share of probability drawn in the wrong place);
  - the lifetime tau refitted (file_rt3d2.fit_tau) from both curves.
Writes one record per run. Usage: python3 wall_curves.py <walls_T.json> <out.json> [nproc]
"""
import os, sys, json, hashlib, urllib.request, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import exact_wall as ew, read_rt3d
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
IDX = json.load(open(os.path.join(ROOT, "public/data/resonant-tunnelling/2026-11-14/kaggle/index.json")))
BY = {r["file"]: r for r in IDX["runs"]}; BASE = "https://phyeinusul.com/r2/" + IDX["runs_base"]
CACHE = os.environ.get("RUNCACHE", "/tmp/rt3d_runs")


def fetch(name):
    os.makedirs(CACHE, exist_ok=True); p = os.path.join(CACHE, name)
    if os.path.exists(p):
        b = open(p, "rb").read()
        if hashlib.sha256(b).hexdigest() == BY[name]["sha256"]: return b
    import subprocess
    for a in range(5):
        r = subprocess.run(["curl", "-sSf", "--max-time", "120", "-o", p + ".part", BASE + name])
        if r.returncode == 0: break
        time.sleep(2 * (a + 1))
    b = open(p + ".part", "rb").read(); os.remove(p + ".part")
    assert hashlib.sha256(b).hexdigest() == BY[name]["sha256"], "SHA-256 mismatch " + name
    open(p, "wb").write(b); return b


def fit_tau(t, P):
    i = int(np.argmax(P)); pk = P[i]
    if pk < 1e-4: return None
    m = np.zeros(len(P), bool); m[i:] = True; m &= (P <= 0.6 * pk) & (P >= 0.05 * pk)
    j = np.where(m)[0]
    if len(j) < 6: return None
    j = j[: np.argmax(np.diff(np.r_[j, 10**9]) > 1) + 1]
    if len(j) < 6: return None
    sl, _ = np.polyfit(t[j], np.log(P[j]), 1)
    return None if sl >= 0 else float(-1 / sl)


def one(name):
    h, amp, ph, prof, p1 = read_rt3d.read(fetch(name)); sp = h["spec"]
    xs = h["prof_x_first"] + np.arange(h["prof_nx"]) * h["step"]; t = np.arange(h["n"]) * h["frame_dt"]
    X = ew.Exact(sp, xs); chi = X.chi(t).T; pe = np.abs(chi)**2
    c = np.array(h["curves"]); C = {n: c[:, i] for i, n in enumerate(h["curve_names"])}
    inner = (h["prof_nx"] // 2 - max(4, h["prof_nx"] // 10)) * h["step"]; I = np.abs(xs) < inner
    L1 = (np.abs(prof[:, I] - pe[:, I]).sum(1) * h["step"])
    L1_twin = (np.abs(p1[:, I] - pe[:, I]).sum(1) * h["step"]) if p1 is not None else None
    # the shape alone, as the page draws it (each curve divided by its own total in the box interior)
    nr = prof[:, I] / (prof[:, I].sum(1, keepdims=True) * h["step"]); ne = pe[:, I] / (pe[:, I].sum(1, keepdims=True) * h["step"])
    L1n = np.abs(nr - ne).sum(1) * h["step"] * pe[:, I].sum(1) * h["step"]    # weighted by the exact share in the interior
    out = dict(file=name, spec=sp, t_end=float(t[-1]), L1_max=float(L1.max()), L1_frame=int(L1.argmax()), L1_shape_max=float(L1n.max()),
               L1_twin_max=float(L1_twin.max()) if L1_twin is not None else None,
               norm_drift=float(1 - (prof.sum(1) / p1.sum(1))[np.argmax(t > 0)]) if p1 is not None else None)
    if "well" in C:
        R = X.regions(t); we = R["well"]; ws = C["well"]
        d = np.abs(ws - we)
        out.update(well_peak_exact=float(we.max()), well_peak_run=float(ws.max()), well_dmax=float(d.max()), well_dmax_t=float(t[d.argmax()]),
                   well_end_ratio=float(ws[-1] / we[-1]) if we[-1] > 1e-9 else None,
                   tau_run=fit_tau(t, ws), tau_exact=fit_tau(t, we), closure=float(np.abs(R["closure"] - 1).max()))
    return out


if __name__ == "__main__":
    T = json.load(open(sys.argv[1])); names = [x["file"] for x in T if x["pass_far"]]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    with Pool(n) as p: res = p.map(one, names, chunksize=2)
    json.dump(res, open(sys.argv[2], "w"))
    print(len(res), "runs")
