"""Fig. 15 correction, walls: the exact transmitted share of every stored wall run (1,088), and the gate.

T_ref = T_inf of exact_wall.Exact: the share of the run's own start packet that ends beyond the last face, from the exact stationary
states (no time grid, no barrier sampling). Beside it, T_w: the transmission averaged over |G(k)|^2 (the packet's spectrum), as in
the coordinator's mytm.packet_T; the two differ only by the start packet's tail inside the barriers (start_in_barrier).
Gate (provisional): |T_run - T_ref| <= max(0.005, 0.01 T_ref), T_run = the index's T_far (what the page shows for discs) and, for
walls, the run's 1D twin T (what the page shows for walls).
Usage: python3 wall_T_all.py <out.json> [nproc]
"""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exact_wall as ew
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
IDX = os.path.join(ROOT, "public/data/resonant-tunnelling/2026-11-14/kaggle/index.json")


def gate(Trun, Tref):
    return abs(Trun - Tref) <= max(0.005, 0.01 * Tref)


def one(r):
    sp = r["spec"]; t0 = time.time()
    X = ew.Exact(sp, np.array([0.0]), dk=5e-4, nslice=2000)
    out = dict(file=r["file"], spec=sp, T_ref=X.T_inf, T_w=X.T_packet_weights, carried=X.carried,
               T_far=r["T_far"]["value"] if r.get("T_far") else None,
               T_twin=r["twin"]["T"] if r.get("twin") else None, start_in_barrier=r["start_in_barrier"], s=round(time.time() - t0, 2))
    out["pass_far"] = gate(out["T_far"], out["T_ref"]) if out["T_far"] is not None else None
    out["pass_twin"] = gate(out["T_twin"], out["T_ref"]) if out["T_twin"] is not None else None
    return out


if __name__ == "__main__":
    d = json.load(open(IDX)); W = [r for r in d["runs"] if r["spec"]["shape"] == "flat"]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    with Pool(n) as p: res = p.map(one, W, chunksize=4)
    json.dump(res, open(sys.argv[1], "w"))
    for lab, sel in (("all", lambda s: True), ("unbiased", lambda s: not s["bias"]), ("biased", lambda s: bool(s["bias"])),
                     ("single", lambda s: s["N"] == 1)):
        R = [x for x in res if sel(x["spec"])]
        e = np.array([abs(x["T_far"] - x["T_ref"]) for x in R])
        print(f"{lab}: {len(R)} runs; T_far fails {sum(not x['pass_far'] for x in R)}, twin T fails {sum(not x['pass_twin'] for x in R)};"
              f" |T_far - T_ref| median {np.median(e):.4f}, max {e.max():.4f}")
