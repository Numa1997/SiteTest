"""Fig. 16: the three cart concepts on the three roads of Fig. 12, in the design simulator (cart16.py), with their robustness.
Writes tools/fig16/concepts.json and prints the table that notes/fig16/concepts.md quotes. CPU only; no new fluid data."""
import json, os, sys
import numpy as np
import cart16 as C, holder as H, slosh_model as SM, sweep as S

HERE = os.path.dirname(os.path.abspath(__file__))
ROADS = [("five bumps", "five 20 mm bumps in step with the swing", 1.0, 8.0), ("25 mm bump", "one 25 mm bump", 1.0, 8.0), ("kerb", "one sharp 30 mm bump", 1.5, 4.0)]
SIMS = {4.0: C.build(4.0), 8.0: C.build(8.0)}
MODE1 = SIMS[4.0][1]["modes"][0]


def hold(zp, **kw):
    p = H.pendulum(zp); d = dict(Mb=1.4, gimbal=1.0, mp=p["mp"], Lc=p["Lc"], IO=p["IO"], s_surf=p["s_surf"], tune=0.0); d.update(kw); return d


def concept(name):
    if name == "Fig. 12 cart, speed held": return dict(Mb=1.5 + S.ML)
    if name == "A tray":      # passive: a damped pendulum cradle on Fig. 12's drive, softer tyre, Fig. 12's preview
        return dict(S.chassis(0.04, 6000.0, "12V3A", 1, 1.5), **hold(0.30, cphi=0.1))
    if name == "B gimbal":    # active gimbal + 24 V drive + load-cell preview
        P = dict(S.chassis(0.06, 6000.0, "24V10A", 2, 1.5), **hold(0.20, tune=1.0, tauMax=0.5, cphi=0.002))
        md = dict(MODE1); md["s"] = P["s_surf"] + md["s_depth"]
        P["Kg"] = C.gimbal_lqr(dict(C.BASE, **P), md, qlim=0.001, philim=0.15); return P
    if name == "C muscle":    # no gimbal: big soft wheel, 24 V drive, load-cell preview
        return dict(S.chassis(0.10, 6000.0, "24V10A", 2, 1.5), Mb=1.5 + S.ML)
    raise KeyError(name)


def ride(P, road, v0, end, model=None):
    go = SIMS[end][0] if model is None else C.build(end, model=model)[0]
    o, Pf = go(dict(P, vk=v0), road, v0); m = C.metrics(o, Pf, S.WS)
    k = np.where(np.abs(o["phi"]) > np.radians(1))[0]; m["phi_settle_s"] = float(o["t"][k[-1]] - (1.5 - 0.5) / v0) if len(k) else 0.0
    return m


ROBUST = {   # what each test changes: the cart's parameters and/or the pint (the slosh model)
    "nominal": (lambda P: P, None),
    "no preview (a bump the map does not have)": (lambda P: dict(P, pv=0.0), None),
    "preview 10 mm late": (lambda P: dict(P, xerr=-0.010), None),
    "pint swings 10 % faster, 15 % harder to hold, half the friction": (lambda P: P, dict(SM.fitted(), f0=SM.PLANT8["f0"] * 1.1, beta_scale=1.15, zeta=SM.fitted()["zeta"] * 0.5)),
    "holder 15 % lighter to turn than the controller believes": (lambda P: dict(P, IO=P["IO"] * 0.85, IOc=P["IO"]) if P.get("gimbal") else P, None),
}

if __name__ == "__main__":
    out = dict(roads=[r[0] for r in ROADS], concepts={}, robust={}, params={})
    names = ["Fig. 12 cart, speed held", "A tray", "B gimbal", "C muscle"]
    for n in names:
        P = concept(n); out["params"][n] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in P.items()}; out["concepts"][n] = {}
        for short, road, v0, end in ROADS:
            m = ride(P, road, v0, end); out["concepts"][n][short] = m
            print(f"{n:26s} {short:11s} tilt {m['tilt_mm']:6.2f} mm  head spilled {m['spill_ml']:5.2f} mL  v {m['v_min']:.2f}-{m['v_max']:.2f}  road push {m['Fr_max_N']:5.1f} N  load {m['N_max_N']:5.0f} N"
                  f"  motor {m['F_motor_max_N']:5.1f} N, {m['i_max_A']:5.2f} of {m['i_lim_A']:.0f} A, short for {m['sat_ms']:3.0f} ms  holder {m['phi_max_deg']:4.1f} deg, {m['tau_max_Nm']:.2f} N m, still after {m['phi_settle_s']:.1f} s  stroke {m['stroke_mm']:4.1f} mm")
    print("robustness on the kerb: tilt mm / head spilled mL")
    for n in names[1:]:
        out["robust"][n] = {}
        for test, (f, model) in ROBUST.items():
            m = ride(f(concept(n)), ROADS[2][1], 1.5, 4.0, model=model); out["robust"][n][test] = m
            print(f"  {n:10s} {test:66s} {m['tilt_mm']:6.2f} / {m['spill_ml']:4.2f}   holder {m['phi_max_deg']:4.1f} deg, {m['tau_max_Nm']:.2f} N m")
    json.dump(out, open(os.path.join(HERE, "concepts.json"), "w"), indent=1)
