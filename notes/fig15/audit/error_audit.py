"""Fig. 15 error audit: every stored run against the exact continuum answer for the same packet.
Exact (walls, any N, with or without bias): transfer matrices through the continuum potential V(x) = sum of barriers V0 on
|x - c| < D/2 plus the bias ramp -Vb (x - xl)/(xr - xl) (clipped), the ramp cut into slices of 0.002 a (staircase converged),
T(k) = (q_R / k) |1/A|^2, averaged over the packet's Gaussian spread of wave numbers, sigma_k = 1/(2 sigma_x), 4001 points over
+-6 sigma_k. Discs and shells are not separable: no exact continuum answer exists, so they are listed with exact = null.
Writes notes/fig15/error_audit.json."""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "kaggle", "resonant-tunnelling"))
import rt3d2

def q_of(E, V):
    d = 2 * (E - V); d = np.where(np.abs(d) < 1e-12, 1e-12, d)   # E exactly at a step height: q = 0 would divide by zero
    return np.sqrt(d.astype(complex))

def T_exact_k(kk, sp, slice_=0.002):
    E = kk**2 / 2; xl, xr = rt3d2.extent(sp); Vb = sp.get("bias", 0.0) or 0.0
    # piecewise-constant layers on a fine x mesh between xl and xr (exact faces kept)
    faces = sorted({xl, xr} | {c + s * sp["D"] / 2 for c in rt3d2.centres(sp) for s in (-1, 1)})
    xs = [faces[0]]
    for a, b in zip(faces[:-1], faces[1:]):
        n = max(1, int(np.ceil((b - a) / slice_))) if Vb else 1
        xs += list(np.linspace(a, b, n + 1)[1:])
    xs = np.array(xs); xc = 0.5 * (xs[:-1] + xs[1:]); Ls = np.diff(xs)
    Vc = np.array([sp["V0"] if any(abs(x - c) < sp["D"] / 2 for c in rt3d2.centres(sp)) else 0.0 for x in xc])
    Vc = Vc - Vb * (xc - xl) / (xr - xl)
    Vs = [0.0] + list(Vc) + [-Vb]; Ls = [0.0] + list(Ls) + [0.0]
    qs = [q_of(E, V) for V in Vs]
    c0 = np.ones_like(E, complex); c1 = np.zeros_like(E, complex)
    for j in range(len(Vs) - 2, -1, -1):
        r = qs[j + 1] / qs[j]
        c0, c1 = 0.5 * ((1 + r) * c0 + (1 - r) * c1), 0.5 * ((1 - r) * c0 + (1 + r) * c1)
        if Ls[j] > 0: c0 = np.exp(-1j * qs[j] * Ls[j]) * c0; c1 = np.exp(1j * qs[j] * Ls[j]) * c1
    T = (qs[-1].real / qs[0].real) * np.abs(1 / c0)**2
    T[(E + Vb) <= 0] = 0
    return T

def exact_packet(sp, n=4001):
    sk = 1 / (2 * sp["sx"]); k0 = np.sqrt(2 * sp["E"]); kk = np.linspace(max(1e-4, k0 - 6 * sk), k0 + 6 * sk, n)
    w = np.exp(-(kk - k0)**2 / (2 * sk**2)); return float((w * T_exact_k(kk, sp)).sum() / w.sum())

if __name__ == "__main__":
    idx = json.load(open(os.path.join(ROOT, "public/data/resonant-tunnelling/2026-11-14/kaggle/index.json")))
    rows = []
    for i, r in enumerate(idx["runs"]):
        sp = r["spec"]; ex = exact_packet(sp) if sp["shape"] == "flat" else None
        tw = r.get("twin", {}).get("T"); t3 = r.get("T_far", {}).get("value")
        row = dict(file=r["file"], shape=sp["shape"], N=sp["N"], V0=sp["V0"], D=sp["D"], P=sp["P"], R=sp["R"], bias=sp["bias"],
                   sx=sp["sx"], E=sp["E"], exact=None if ex is None else round(ex, 6), twin=tw, T3d=t3)
        if ex is not None:
            for nm, v in (("twin", tw), ("T3d", t3)):
                if v is None: continue
                a = v - ex; row[f"abs_{nm}"] = round(a, 6); row[f"rel_{nm}"] = round(a / ex, 5) if ex > 1e-6 else None
                assert np.isfinite(ex), r['file']
                # the gate: |T - exact| <= max(0.005, 0.01 exact)
                row[f"pass_{nm}"] = bool(abs(a) <= max(0.005, 0.01 * ex))
        rows.append(row)
        if i % 500 == 0: print(i, flush=True)
    json.dump(dict(script="notes/fig15/audit/error_audit.py", doc=__doc__, gate="|T - exact| <= max(0.005, 0.01 * exact)", runs=rows),
              open(os.path.join(ROOT, "notes/fig15/error_audit.json"), "w"), separators=(",", ":"))
    W = [x for x in rows if x["exact"] is not None and x["T3d"] is not None]
    import collections
    def grp(f): 
        c = collections.defaultdict(lambda: [0, 0, 0, 0])
        for x in W:
            g = c[f(x)]; g[0] += 1; g[1] += abs(x["abs_T3d"]) > 0.01; g[2] += (x["rel_T3d"] is not None and abs(x["rel_T3d"]) > 0.02); g[3] += not x["pass_T3d"]
        return dict(c)
    print("walls with exact:", len(W), "| >0.01 abs:", sum(abs(x["abs_T3d"]) > 0.01 for x in W), "| >2 % rel:", sum(x["rel_T3d"] is not None and abs(x["rel_T3d"]) > 0.02 for x in W), "| fail gate:", sum(not x["pass_T3d"] for x in W))
    for nm, f in [("V0", lambda x: x["V0"]), ("D", lambda x: x["D"]), ("sx", lambda x: x["sx"]), ("N", lambda x: x["N"]), ("biased", lambda x: x["bias"] != 0)]:
        print(nm, "[n, >0.01, >2%, fail]", grp(f))
