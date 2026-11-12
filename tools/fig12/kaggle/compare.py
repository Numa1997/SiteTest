"""Fig. 12: compare one case run on two machines (Kaggle against the GitHub runner, or any two), column by column.

    python3 tools/fig12/kaggle/compare.py <run folder A> <run folder B>

Each folder holds the layout of notes/fig12/of-runs/<case>/: stoutMonitor.dat.gz, case.json, walltime.
The monitor columns are t mass KE PE Px Py Pz outVolume h_front h_back h_left h_right (handoff, section 9). The time
steps are adaptive, so the two runs may not share their time points: B is interpolated linearly onto A's times
inside the common interval, and the rows where both have the same time are also compared exactly. For each column
the largest difference is printed absolutely and relative to the largest magnitude of that column in A. Then both
runs go through tools/fig12/of/analyse_swing.py (swing runs) and the frequency, damping and mass books are set side
by side, with the wall times. Exit code 0 always: this reports, the reader judges.
"""
import gzip, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "of"))
import analyse_swing  # noqa: E402

COLS = "t mass KE PE Px Py Pz outVolume h_front h_back h_left h_right".split()


def load(folder):
    p = os.path.join(folder, "stoutMonitor.dat.gz")
    m = analyse_swing.load(p)
    case = json.load(open(os.path.join(folder, "case.json")))
    wall = os.path.join(folder, "walltime")
    return p, m, case, (float(open(wall).read()) if os.path.exists(wall) else None)


def main(a, b):
    pa, A, ca, wa = load(a)
    pb, B, cb, wb = load(b)
    for k in set(ca) | set(cb):
        if k != "name" and ca.get(k) != cb.get(k):
            print(f"note: parameter {k} differs: {ca.get(k)} against {cb.get(k)}")
    print(f"A {a}: {len(A)} rows to t = {A[-1, 0]:.4f} s; solver wall time {wa} s")
    print(f"B {b}: {len(B)} rows to t = {B[-1, 0]:.4f} s; solver wall time {wb} s")
    t0, t1 = max(A[0, 0], B[0, 0]), min(A[-1, 0], B[-1, 0])
    sel = (A[:, 0] >= t0) & (A[:, 0] <= t1)
    same_t = np.intersect1d(A[:, 0], B[:, 0])
    print(f"common interval {t0:.4f}-{t1:.4f} s; {sel.sum()} rows of A inside it; {len(same_t)} time points shared exactly")
    print(f"{'column':10s} {'largest |A-B|':>14s} {'relative':>10s} {'at t (s)':>9s}   {'same-time rows: largest |A-B|':>30s}")
    worst = {}
    ia = np.searchsorted(A[:, 0], same_t); ib = np.searchsorted(B[:, 0], same_t)
    for j, name in enumerate(COLS[1:A.shape[1]], start=1):
        bi = np.interp(A[sel, 0], B[:, 0], B[:, j])
        d = np.abs(A[sel, j] - bi)
        k = int(np.argmax(d)); scale = np.max(np.abs(A[:, j])) or 1.0
        exact = np.max(np.abs(A[ia, j] - B[ib, j])) if len(same_t) else float("nan")
        worst[name] = dict(abs=float(d[k]), rel=float(d[k] / scale), t=float(A[sel, 0][k]), same_time_abs=float(exact))
        print(f"{name:10s} {d[k]:14.4e} {d[k] / scale:10.2e} {A[sel, 0][k]:9.4f}   {exact:30.4e}")
    if ca.get("forcing") == "tilt":
        for label, p in (("A", pa), ("B", pb)):
            try:
                r = analyse_swing.analyse(p)
                print(f"{label}: swing {r['f']:.5f} Hz, damping ratio {r['zeta']:.5f}, largest lean {r['lean_max']:.3f} mm")
            except Exception as e:  # a short test run has no swing to fit
                print(f"{label}: no swing analysis ({e})")
    return worst


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
