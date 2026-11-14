"""Fig. 16: compare the slosh model (slosh_model.py, as fit.py left it) with the stored Fig. 12 rides, frame by frame.
Training set: run 8's three rides with the speed held (notebook version 8) and its free swing: the friction's three numbers
(fit.py), the push coefficient (gamma_check.py) and the spill strip's width w_s (here, on run 8's kerb ride alone) come from them.
Validation set: run 10's five controlled rides (version 10), never used to set any number of the model.
Prints per ride: largest tilt (stored, model), rms tilt error, largest speed error, rms current error, head spilled (stored, model).
Writes tools/fig16/validation.json; --plot also draws notes/fig16/validation.png."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rides, slosh_model as SM, spill as SP

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = [("run8", "ride_resonant"), ("run8", "ride_bump25"), ("run8", "ride_sharp30")]
VALID = [("run10", "ride_resonant_joint"), ("run10", "ride_bump25_joint"), ("run10", "ride_sharp30_joint"),
         ("run10", "ride_sharp30_slosh"), ("run10", "ride_sharp30_preview")]


def compare(run, name, model=None, ws=None):
    d = rides.load(rides.RUNS[run], name); T, _ = rides.tilt(d, SM.R_FILL)
    o, m = SM.simulate(d["road"], d["v0"], d["ctrl"], d["tarr"][-1] + 1e-9, model=model or SM.fitted())
    t = d["tarr"]; k = np.clip(np.round(t / 0.002).astype(int) - 1, 0, len(o["t"]) - 1)
    Tm = o["tilt"][k]
    res = dict(name=f"{run}/{name}", ctrl=d["ctrl"], tilt_max_mm=float(np.nanmax(np.abs(T)) * 1e3), tilt_max_model_mm=float(np.abs(o["tilt"]).max() * 1e3),
               tilt_rms_mm=float(np.sqrt(np.nanmean(T ** 2)) * 1e3), tilt_rms_err_mm=float(np.sqrt(np.nanmean((T - Tm) ** 2)) * 1e3),
               v_err_max=float(np.abs(np.asarray(d["v"]) - o["v"][k]).max()), v_min=float(np.min(d["v"])), v_min_model=float(o["v"].min()),
               i_rms_err_A=float(np.sqrt(np.mean((np.asarray(d["i"]) - o["i"][k]) ** 2))), i_max_A=float(np.abs(d["i"]).max()), i_max_model_A=float(np.abs(o["i"]).max()),
               head_spill_ml=float(d["head_spill_ml"][-1]))
    if ws is not None: res["head_spill_model_ml"] = float(SP.spill(o, ws)[-1] * 1e6)
    return res, d, T, o


def show(r):
    print(f"{r['name']:28s} tilt max {r['tilt_max_mm']:6.2f} / {r['tilt_max_model_mm']:6.2f} mm | rms err {r['tilt_rms_err_mm']:5.2f} of {r['tilt_rms_mm']:5.2f} mm"
          f" | v err {r['v_err_max']:.3f} m/s | i err {r['i_rms_err_A']:.3f} A | head spilled {r['head_spill_ml']:.2f} / {r.get('head_spill_model_ml', float('nan')):.2f} mL")


if __name__ == "__main__":
    # the spill strip's width from run 8's kerb ride with the speed held, by bisection (the spill grows with w_s)
    _, d, T, o = compare("run8", "ride_sharp30")
    unit = SP.spill(o, 1.0)[-1]; ws = float(d["head_spill_ml"][-1] * 1e-6 / unit) if unit > 0 else float("nan")
    print(f"spill strip width w_s = {ws * 1e3:.2f} mm (from run 8's kerb, speed held: {d['head_spill_ml'][-1]} mL)")
    out = dict(model=SM.fitted(), gamma_g=SM.GAMMA_TH * SM.GAMMA_SCALE * 1e3, ws_mm=ws * 1e3, train=[], valid=[]); keep = {}
    for key, S in (("train", TRAIN), ("valid", VALID)):
        print(key.upper())
        for run, name in S:
            r, d, T, o = compare(run, name, ws=ws); show(r); out[key].append(r); keep[name] = (d, T, o)
    json.dump(out, open(os.path.join(HERE, "validation.json"), "w"), indent=1)
    if "--plot" in sys.argv:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(len(keep), 3, figsize=(15, 2.6 * len(keep)))
        for row, (name, (d, T, o)) in zip(ax, keep.items()):
            lim = (0.4, 2.5) if "sharp" in name else (0.5, 3.5)
            row[0].plot(d["tarr"], T * 1e3, "k.-", ms=3, label="stored"); row[0].plot(o["t"], o["tilt"] * 1e3, "r", label="model"); row[0].set_ylabel("tilt, mm")
            row[1].plot(d["tarr"], d["v"], "k.-", ms=3); row[1].plot(o["t"], o["v"], "r"); row[1].set_ylabel("speed, m/s")
            row[2].plot(d["tarr"], d["i"], "k.-", ms=3); row[2].plot(o["t"], o["i"], "r", lw=0.7); row[2].set_ylabel("current, A")
            for a in row: a.set_xlim(*lim); a.grid(alpha=0.3)
            row[0].set_title(name + " (" + d["ctrl"] + ")", fontsize=9, loc="left"); row[0].legend(fontsize=7)
        plt.tight_layout(); plt.savefig(os.path.join(HERE, "..", "..", "notes", "fig16", "validation.png"), dpi=75)
