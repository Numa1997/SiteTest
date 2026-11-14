"""Fig. 15 correction, walls: one pass over every stored wall run (1,088).

Per run: download the stored file (SHA-256 checked), build the exact chi at the stored frame times (exact_wall.Exact), write the
rebuilt RT3C file (rebuild_wall.write; the parent's name and SHA-256 in its header), and measure the curve gate against the stored
file: trapped share P_well(t), the x-profile (L1, and L1 of the shape as the page draws it), the lifetime refitted from both.
Usage: python3 rebuild_walls_all.py <walls_T.json> <out dir for rebuilt files> <out.json> [nproc]
"""
import os, sys, json, hashlib, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import read_rt3d, rebuild_wall as rw
from wall_curves import fetch, fit_tau, BY

OUT = None


def one(name):
    t0 = time.time()
    h, amp, ph, prof, p1 = read_rt3d.read(fetch(name))
    slab, pr, pr1, curves, cn, X, extra = rw.from_exact(h)
    head = dict(method="exact: psi = chi(x,t) h(y,t) h(z,t); chi by superposition of the stationary scattering states "
                "(tools/kaggle/resonant-tunnelling/correction/exact_wall.py); no time grid, no barrier sampling",
                parent=dict(file=name, sha256=BY[name]["sha256"]), T_ref=X.T_inf, T_spectrum_weighted=X.T_packet_weights,
                carried=X.carried, closure_max=float(np.abs(extra["closure"] - 1).max()),
                regions="left, right, norm: inside the box |x| <= box half-length; left_line, right_line: whole line",
                extra_curves=dict(left_line=np.round(extra["left_line"], 7).tolist(), right_line=np.round(extra["right_line"], 7).tolist()),
                device="cpu (exact)", wall=None, has_1d=True, sep_check_max=0.0, T_1d_splitstep=None, R_1d_splitstep=None,
                T_packet_exact=X.T_packet_weights)
    blob, A, P, peaks = rw.write(h, slab, pr, pr1, curves, cn, head)
    open(os.path.join(OUT, name), "wb").write(blob)
    t = np.arange(h["n"]) * h["frame_dt"]; xs = h["prof_x_first"] + np.arange(h["prof_nx"]) * h["step"]
    inner = (h["prof_nx"] // 2 - max(4, h["prof_nx"] // 10)) * h["step"]; I = np.abs(xs) < inner
    L1 = np.abs(prof[:, I] - pr[:, I]).sum(1) * h["step"]
    nr = prof[:, I] / (prof[:, I].sum(1, keepdims=True) * h["step"]); ne = pr[:, I] / (pr[:, I].sum(1, keepdims=True) * h["step"])
    L1s = np.abs(nr - ne).sum(1) * h["step"] * pr[:, I].sum(1) * h["step"]
    c = np.array(h["curves"]); C = {n: c[:, i] for i, n in enumerate(h["curve_names"])}
    rec = dict(file=name, spec=h["spec"], T_ref=X.T_inf, sha256_rebuilt=hashlib.sha256(blob).hexdigest(), bytes=len(blob),
               closure_max=head["closure_max"], carried=X.carried, L1_max=float(L1.max()), L1_shape_max=float(L1s.max()),
               norm_end_run=float(C["norm"][-1]), s=round(time.time() - t0, 1))
    if "well" in C:
        we = curves[:, cn.index("well")]; ws = C["well"]; d = np.abs(ws - we)
        rec.update(well_peak_exact=float(we.max()), well_peak_run=float(ws.max()), well_dmax=float(d.max()),
                   well_dmax_rel_peak=float(d.max() / max(we.max(), 1e-12)), tau_run=fit_tau(t, ws), tau_exact=fit_tau(t, we))
    return rec


def init(o):
    global OUT; OUT = o


if __name__ == "__main__":
    T = json.load(open(sys.argv[1])); os.makedirs(sys.argv[2], exist_ok=True)
    names = [x["file"] for x in sorted(T, key=lambda x: not x["pass_far"])]     # the 170 passing first (curve gate), then the rest
    done = {}
    if os.path.exists(sys.argv[3]):
        for l in open(sys.argv[3]): r = json.loads(l); done[r["file"]] = r
    todo = [n for n in names if n not in done]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    with Pool(n, initializer=init, initargs=(sys.argv[2],)) as p, open(sys.argv[3], "a") as f:
        for k, r in enumerate(p.imap_unordered(one, todo, chunksize=1)):
            f.write(json.dumps(r) + "\n"); f.flush()
            if k % 25 == 0: print(k + len(done), "/", len(names), r["file"], r["s"], "s", flush=True)
    print("done")
