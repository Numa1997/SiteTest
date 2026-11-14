"""Fig. 16: fit the slosh model's friction to the TRAINING rides only (run 8: the free swing with the head and the three rides with the
speed held). Free numbers: zeta (first mode, at the speed amplitude w qref, qref = 5 mm), n (the friction's power of the speed),
zeta_hi (the higher modes). Everything else is theory or run 8's measured frequency. The loss is the sum over the four training
records of the mean square tilt error, each divided by the record's own mean square tilt (so the gentle rides count as much as the kerb).
Writes tools/fig16/fit.json."""
import json, os, sys, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rides, slosh_model as SM

N = int(os.environ.get("NMODES", "3"))
TRAIN = [("run8", "ride_resonant"), ("run8", "ride_bump25"), ("run8", "ride_sharp30")]
FREE = rides.load(rides.RUNS["run8"], "free_full_1.5"); FREE_T, _ = rides.tilt(FREE, SM.R_FILL)
STORED = {n: (lambda d: (d, rides.tilt(d, SM.R_FILL)[0]))(rides.load(rides.RUNS[r], n)) for r, n in TRAIN}
PROG = os.environ.get("CLAUDE_PROGRESS_SH")


def loss(p, verbose=False):
    zeta, n, zhi = p
    if not (0.02 < zeta < 2 and 0.2 < n < 1.6 and 0.02 < zhi < 3): return 1e3
    mod = dict(N=N, zeta=zeta, n=n, zeta_hi=zhi)
    t, T = SM.free_swing(model=mod); Tm = np.interp(FREE["tarr"], t, T)
    errs = [np.nanmean((FREE_T - Tm) ** 2) / np.nanmean(FREE_T ** 2)]
    for name, (d, Ts) in STORED.items():
        o, _ = SM.simulate(d["road"], d["v0"], d["ctrl"], d["tarr"][-1] + 1e-9, model=mod)
        k = np.clip(np.round(d["tarr"] / 0.002).astype(int) - 1, 0, len(o["t"]) - 1)
        errs.append(np.nanmean((Ts - o["tilt"][k]) ** 2) / np.nanmean(Ts ** 2))
    if verbose: print(np.round(p, 4), np.round(errs, 4))
    return float(np.sum(errs))


if __name__ == "__main__":
    t0 = time.time(); calls = [0]
    def f(p):
        calls[0] += 1
        if PROG and calls[0] % 5 == 0: os.system(f'bash "{PROG}" -n fig16-fit {min(calls[0], 120)}/120 "loss evaluations" >/dev/null 2>&1')
        return loss(p)
    best = None
    for p0 in ([0.425, 1.0, 0.425], [0.35, 0.667, 0.35]):
        r = minimize(f, p0, method="Nelder-Mead", options=dict(maxfev=55, xatol=2e-3, fatol=1e-4))
        if best is None or r.fun < best.fun: best = r
    loss(best.x, verbose=True)
    lin = minimize(lambda p: loss([p[0], 1.0, p[1]]), [0.425, 0.425], method="Nelder-Mead", options=dict(maxfev=40))
    out = dict(N=N, zeta=float(best.x[0]), n=float(best.x[1]), zeta_hi=float(best.x[2]), loss=float(best.fun),
               linear=dict(zeta=float(lin.x[0]), zeta_hi=float(lin.x[1]), loss=float(lin.fun)), qref=0.005,
               train=["run8/free_full_1.5"] + [f"{r}/{n}" for r, n in TRAIN], seconds=round(time.time() - t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fit.json"), "w"), indent=1)
    if PROG: os.system(f'bash "{PROG}" -n fig16-fit done >/dev/null 2>&1')
    print(out)
