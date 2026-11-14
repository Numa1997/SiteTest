"""Fig. 12 in JAX: the result checks (notes/fig12/handoff-jax/02-launch-gates.md, gate E) on one downloaded run.
Reads summary.json and the .npz files of a run folder; prints PASS or FAIL per check and, per ride, the frames worth looking at
(rest, mid-ride, the first spill, the end). Computes nothing physical: it only reads what Kaggle stored.
Run: python3 tools/fig12/kaggle/check_run.py <run folder>"""
import json, sys
from pathlib import Path
import numpy as np

run = Path(sys.argv[1]); S = json.load(open(run / "summary.json")); ok_all = True


def check(name, ok, detail):
    global ok_all
    print(f"{'PASS' if ok else 'FAIL'}  {name}  ({detail})"); ok_all = ok_all and ok


print("device", S.get("device"), "jax", S.get("jax"))
for t in S["tasks"]:
    name = t["name"]; print(f"\n== {name}: {t['kind']}, {t['end']} s, {t['steps']} steps, {t['ms_per_step']} ms a step, run {t['run_s']} s")
    check("near-surface list never full", t["nselmax"] < t["K"], f"{t['nselmax']} of {t['K']}")
    check("pressure residual small", t["resmax"] < 1e-3, f"largest {t['resmax']:.2e}")
    if t.get("books"):   # run 8 on: the books of every stored frame
        B = t["books"]
        check("stout books: glass + air + cart + ground = poured, every frame", B["stout_err_particles_max"] == 0, f"largest error {B['stout_err_particles_max']} particles")
        check("head books: glass + broken off = served, every frame", B["head_err_ml_max"] < 1e-3, f"largest error {B['head_err_ml_max']:.2e} mL")
    if name == "rest":
        g = t.get("rest_guard", {})
        check("rest guard", bool(g) and g["max_dev_mm"] < g["limit_max_mm"] and g["rms_dev_mm"] < g["limit_rms_mm"] and g["head_spilled_ml"] == 0 and g["spilled_g"] == 0, str(g))
        continue
    Z = np.load(run / f"{name}.npz")
    nd = Z["ndrops"]; check("drop list never full", int(nd.max()) < 16384, f"largest {int(nd.max())}")
    for b in ("ewall", "eskin", "efoam"):
        check(f"energy book {b} never negative", float(Z[b].min()) >= -1e-9, f"end {float(Z[b][-1]):.3e} J")
    if t["kind"] == "ride":
        iv = t["impulse_vs_momentum"]
        check("impulse on the cart = minus the stout's momentum", abs(iv["impulse_x"] + iv["momentum_x_end"]) < 1e-3 * max(1e-6, abs(iv["momentum_x_end"])) + 1e-7, str(iv))
        sp = (Z["N"] - Z["nact"]) * float(Z["mp"]) * 1e3; hs = Z["foam_spill"] * 1e6; tt = Z["t"]
        first = int(np.argmax((sp > 0) | (hs > 0))) if ((sp > 0) | (hs > 0)).any() else None
        print(f"   spilled {sp[-1]:.2f} g of stout, {hs[-1]:.2f} mL of head; lean up to {t['lean_max_mm']:.1f} mm; speed {t['v_range']}")
        print(f"   frames to look at: 0, {len(tt) // 2} (mid), {first} (first spill), {len(tt) - 1} (end)")
    else:
        f13 = t.get("fit_ring13") or {}
        if f13.get("f"):
            # run 4's summary gave zeta' = 1/(tau w_d); the natural frequency is w0 = w_d sqrt(1 + zeta'^2), zeta = zeta'/sqrt(1 + zeta'^2)
            f0 = f13.get("f0") or f13["f"] * (1 + f13["zeta"] ** 2) ** 0.5
            z = f13["zeta"] if "f0" in f13 else f13["zeta"] / (1 + f13["zeta"] ** 2) ** 0.5
            print(f"   free swing: rings at {f13['f']:.3f} Hz, natural frequency {f0:.3f} Hz, damping ratio {z:.4f}, amplitude {f13['A_mm']:.2f} mm, fit rms {f13['rms_mm']:.3f} mm")
            if t["model"] != "full":
                # Gate E: the solver's own swing (no head) against the theory of the bare stout, 3.421 Hz
                check("natural frequency within 3 % of 3.421 Hz", abs(f0 / 3.421 - 1) < 0.03, f"{f0:.3f} Hz")
            elif t.get("head_mass"):
                # run 8: the head's mass lowers the first mode by 1/sqrt(1 + m_s k/rho) (note eq. 15b), k read from run 6's swing
                # without the head on the same grid (3.331 Hz: k = 44.66 1/m, m_s/rho = 5.13 mm, factor 0.902), applied to run 6's swing
                # with the head's weight only (3.278 Hz): 2.957 Hz
                check("natural frequency with the head's mass within 3 % of 2.957 Hz", abs(f0 / 2.957 - 1) < 0.03, f"{f0:.3f} Hz")
            else:
                # with the head (weight, no inertia in this model) the swing's natural frequency is the bare stout's; Gate C predicted
                # that the head stops the swing within about one period (zeta of order 0.5)
                print(f"   Gate C: the head should stop the swing within about one period; here e-folding in {1 / (z * 2 * 3.14159265 * f0):.3f} s, "
                      f"{1 / (z * 2 * 3.14159265 * f0) * f0:.2f} periods")
print("\nALL", "PASS" if ok_all else "FAIL")
