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
            print(f"   free swing: {f13['f']:.3f} Hz, damping ratio {f13['zeta']:.4f}, amplitude {f13['A_mm']:.2f} mm, fit rms {f13['rms_mm']:.3f} mm")
            check("swing frequency within 3 % of 3.42 Hz", abs(f13["f"] / 3.42 - 1) < 0.03, f"{f13['f']:.3f} Hz")
print("\nALL", "PASS" if ok_all else "FAIL")
