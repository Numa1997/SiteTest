"""Compare recon.py with the Crank-Nicolson solve of cn.py, frame by frame, for a few runs. Usage: python3 check_cn.py out.json"""
import json, sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recon, cn
from tm import double
CASES = [(1.0, 2.343, 3.0), (1.0, 2.343, 12.0), (1.0, 3.454, 3.0), (0.5, 6.0, 3.0), (2.5, 3.454, 3.0), (1.7329, 3.454, 12.0)]
res = []
for E, s, s0 in CASES:
    h, body, fr, xv, times = recon.run(E, s, s0)
    for dx, dt in ((0.025, 0.005), (0.0125, 0.0025)):
        T0 = time.time(); c = cn.run(E, double(recon.V0, recon.D, s), s0, h["x0"], times, dx=dx, dt=dt, xv=xv)
        d = c["frames"] - fr
        l2 = np.sqrt(np.sum(np.abs(d)**2, 1) * recon.DX)          # per frame, on the stored window
        row = dict(E=E, s=s, sigma0=s0, dx=dx, dt=dt, seconds=round(time.time() - T0, 1), L2_max=float(l2.max()), L2_end=float(l2[-1]),
                   abs_max=float(np.abs(d).max()), peak=float(np.abs(fr).max()), cn_norm_drift=float(np.abs(c["norm"] - c["norm"][0]).max()))
        res.append(row); print(row, flush=True)
json.dump(res, open(sys.argv[1], "w"), indent=1)
