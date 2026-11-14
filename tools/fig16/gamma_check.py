"""Fig. 16: the stout's push on the cart against the swing, from the stored training rides (run 8, speed held).
F_x (stored per frame, the run's -dP/dt) is regressed on -q'' with q = tilt/2 (rides.py), by least squares through zero, from 0.3 s on."""
import numpy as np, rides, slosh_model as SM
for run, name in [("run8", "ride_resonant"), ("run8", "ride_bump25"), ("run8", "ride_sharp30")]:
    d = rides.load(rides.RUNS[run], name); T, _ = rides.tilt(d, SM.R_FILL); t = d["tarr"]; F = np.array(d["Fx"])
    qdd = np.gradient(np.gradient(T / 2, t), t); m = np.isfinite(qdd) & (t > 0.3)
    g = -np.sum(F[m] * qdd[m]) / np.sum(qdd[m] ** 2); r = np.corrcoef(F[m], -qdd[m])[0, 1]
    print(f"{name:16s} gamma {g * 1e3:5.1f} g (cylinder theory {SM.GAMMA_TH * 1e3:.1f} g), correlation {r:.2f}")
