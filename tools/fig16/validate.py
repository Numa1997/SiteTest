"""Fig. 16: compare the one-mode model (slosh_model.py) with the stored Fig. 12 rides, frame by frame.
Training set: run 8's three rides with the speed held (notebook version 8) and its free swing. Validation set: run 10's five
controlled rides (version 10), never used to set any number of the model.
Prints, per ride: the largest tilt (stored, model), the rms tilt error over the ride, the speed and current errors, the
correlation of the stored stout push F_x with the model's -gamma q''."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rides, slosh_model as SM

RIDES = [("run8", "ride_resonant"), ("run8", "ride_bump25"), ("run8", "ride_sharp30"),
         ("run10", "ride_resonant_joint"), ("run10", "ride_bump25_joint"), ("run10", "ride_sharp30_joint"),
         ("run10", "ride_sharp30_slosh"), ("run10", "ride_sharp30_preview")]


def stored(run, name):
    d = rides.load(rides.RUNS[run], name); T, _ = rides.tilt(d, SM.R_FILL)
    return d, T


def compare(run, name, model=None, verbose=True):
    d, T = stored(run, name)
    o, m = SM.simulate(d["road"], d["v0"], d["ctrl"], d["tarr"][-1] + 1e-9, model=model)
    t = d["tarr"]; k = np.clip(np.round(t / 0.002).astype(int) - 1, 0, len(o["t"]) - 1)
    Tm = o["tilt"][k]; vm = o["v"][k]; im = o["i"][k]
    res = dict(name=f"{run}/{name}", tilt_max=np.nanmax(np.abs(T)) * 1e3, tilt_max_m=np.abs(o["tilt"]).max() * 1e3,
               tilt_rms_err=np.sqrt(np.nanmean((T - Tm) ** 2)) * 1e3, tilt_rms=np.sqrt(np.nanmean(T ** 2)) * 1e3,
               v_err=np.abs(np.asarray(d["v"]) - vm).max(), i_err=np.sqrt(np.mean((np.asarray(d["i"]) - im) ** 2)),
               i_max=np.abs(d["i"]).max(), i_max_m=np.abs(o["i"]).max())
    if verbose:
        print(f"{res['name']:28s} tilt max {res['tilt_max']:6.2f} model {res['tilt_max_m']:6.2f} mm | rms {res['tilt_rms']:5.2f} err {res['tilt_rms_err']:5.2f} mm"
              f" | v err max {res['v_err']:.3f} m/s | i rms err {res['i_err']:.3f} A (max {res['i_max']:.2f} / {res['i_max_m']:.2f})")
    return res, d, T, o


if __name__ == "__main__":
    for run, name in RIDES: compare(run, name)
