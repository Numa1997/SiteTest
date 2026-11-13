"""Fig. 12 on Kaggle: the damping of solver v2's free swing. Reads a free_swing_v2*.json (default: both files in
public/data/fig12/2026-11-12/) and fits, for each run, q = A exp(-t/tau) cos(w t + phi) + c + s t to the first mode read on
rings 16 and 13 of the stored surface, from 0.1 s after the push to the end (kaggle_decay.fit_decay). zeta = 1/(w tau).
Run: python3 tools/fig12/kaggle/free_swing_fit.py [file ...]   (numpy only)"""
import glob, json, os, sys
import numpy as np
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, ".."))
from kaggle_decay import fit_decay
files = sys.argv[1:] or sorted(glob.glob(os.path.join(here, "..", "..", "..", "public", "data", "fig12", "2026-11-12", "free_swing_v2*.json")))
for path in files:
    D = json.load(open(path)); t0 = D["settle"] + D["push_t"] + 0.1; print(os.path.basename(path))
    for r in D["runs"]:
        t = np.array(r["t"]); m = t > t0; out = []
        for k in ("q16", "q13"):
            f = fit_decay(t[m] - t[m][0], np.array(r[k])[m]); out.append(f"ring {k[1:]}: {f['f']:.3f} Hz, zeta {f['zeta']:.4f}, {f['A']:.2f} mm")
        print(f"  {r['dx'] * 1e3:.1f} mm {r['model']:18s} {r['wall_s'] / r['steps'] * 1e3:4.0f} ms a step | " + " | ".join(out))
