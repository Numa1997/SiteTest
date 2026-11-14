"""Fig. 15 correction, plan B: which stored discs and shells must be recomputed in complex128.

For every stored disc and shell (2,609), T_ref comes from the (x, rho) recompute (complex64; discs on the base grid, shells at
Rmax 160; records in notes/fig15/correction/rt2d_runs/). T_old is the stored run's T:
  discs  : the stored index's T_far;
  shells : P_out / P_box at the T_far frame rule, read from the stored file (SHA-256 checked; file_corrected.shell_T_old).
Gate: |T_old - T_ref| <= max(0.005, 1 % of T_ref).
complex64's own uncertainty: T moves by <= 6e-4 against complex128 and <= 0.0019 under grid refinement (smoke test, 14 Nov), so a
run is decided only when it clears the gate edge by 0.002 on the right side:
  "keep"       : |error| <= gate - 0.002   (passes even if T_ref were off by 0.002);
  "recompute"  : otherwise (fails, or too close to the edge to call): recomputed in complex128 on the same grid.
Usage: python3 classify_2d.py <stored index.json> <rt2d_runs dir> <out dir>
Writes recompute_2d.json (the job list, same format as jobs_2d.json) and classify_2d_summary.json; one line per run in classify.log.
"""
import json, os, sys, glob, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from file_corrected import shell_T_old

MARGIN = 0.002


def main(index, runs_dir, out, jobs="jobs_2d.json", base="https://phyeinusul.com/r2/resonant-tunnelling/2026-11-14/runs/"):
    os.makedirs(out, exist_ok=True); log = open(os.path.join(out, "classify.log"), "w")
    OLD = {r["file"]: r for r in json.load(open(index))["runs"]}
    NEW = {}
    for f in sorted(glob.glob(os.path.join(runs_dir, "*.jsonl"))):
        for l in open(f):
            r = json.loads(l); NEW[r["file"]] = r
    J = {j["file"]: j for j in json.load(open(jobs))}
    rows, redo = [], []
    t0 = time.time()
    for k, (name, n) in enumerate(sorted(NEW.items())):
        o = OLD[name]; shape = o["spec"]["shape"]; T_ref = float(n["T_ref"])
        gate = max(0.005, 0.01 * abs(T_ref)); why = None
        try:
            T_old = shell_T_old(o, base) if shape == "shell" else float(o["T_far"]["value"])
        except Exception as e:                                     # unreadable stored file: recompute, never guess
            T_old = None; why = repr(e)[:200]
        if T_old is None:
            status = "recompute"
            row = dict(file=name, shape=shape, T_old=None, T_ref=round(T_ref, 7), error=None, gate=round(gate, 6), passes=False,
                       status="recompute", why=why, drift=n.get("drift"), T_unc=n.get("T_unc"))
        else:
            err = T_old - T_ref
            status = "keep" if abs(err) <= gate - MARGIN else "recompute"
            row = dict(file=name, shape=shape, T_old=round(T_old, 6), T_ref=round(T_ref, 7), error=round(err, 7), gate=round(gate, 6),
                       passes=abs(err) <= gate, status=status, drift=n.get("drift"), T_unc=n.get("T_unc"))
        rows.append(row)
        if status == "recompute": redo.append(J[name])
        log.write(json.dumps(row) + "\n"); log.flush()
        if k % 100 == 0: print(f"{k}/{len(NEW)} {time.time()-t0:.0f} s", flush=True)
    json.dump(redo, open(os.path.join(out, "recompute_2d.json"), "w"))
    S = {}
    for shape in ("coin", "shell"):
        R = [r for r in rows if r["shape"] == shape]
        if not R: continue
        e = np.abs([r["error"] for r in R if r["error"] is not None] or [0.0])
        S[shape] = dict(n=len(R), passes=sum(r["passes"] for r in R), keep=sum(r["status"] == "keep" for r in R),
                        recompute=sum(r["status"] == "recompute" for r in R), unreadable=sum(r["T_old"] is None for r in R), err_median=float(np.median(e)), err_max=float(e.max()),
                        recompute_steps=int(sum(J[r["file"]]["steps"] for r in R if r["status"] == "recompute")))
    json.dump(dict(summary=S, margin=MARGIN, rows=rows), open(os.path.join(out, "classify_2d_summary.json"), "w"), indent=1)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
