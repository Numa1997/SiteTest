"""Fig. 16: the lever study. Hundreds of cart variants over the kerb (one sharp 30 mm bump at 1.5 m/s) in the design simulator
(cart16.py), on the CPU. Writes tools/fig16/sweep.json: one row per variant with its metrics (cart16.metrics).
Levers: wheel radius, tyre stiffness, motor (Fig. 12's 12 V / 3 A or a 24 V / 10 A drive), road preview (off, static load, measured
load), slowing before the kerb, and the holder (fixed; free pendulum at four pivot heights; pendulum with the tuning torque)."""
import itertools, json, os, sys, time
import numpy as np
import cart16 as C, holder as H, slosh_model as SM

HERE = os.path.dirname(os.path.abspath(__file__)); PROG = os.environ.get("CLAUDE_PROGRESS_SH")
WS = json.load(open(os.path.join(HERE, "validation.json")))["ws_mm"] * 1e-3
ML = SM.liquid_mass(); KERB = "one sharp 30 mm bump"; XK = 1.5
FORCE_KP, FORCE_KI = C.F12["Kp"] * 5.0, C.F12["Ki"] * 5.0        # Fig. 12's speed loop as force per speed error (b = 5 N/A)
WHEELS = {0.04: 0.30, 0.06: 0.45, 0.08: 0.60, 0.10: 0.80}        # radius -> mass, kg (solid disc inertia)
MOTORS = {"12V3A": dict(Km=0.02, Ra=2.0, Vmax=12.0, Imax=3.0, Jm=2e-6, bN=5.0),      # Fig. 12's, 15 N at stall
          "24V10A": dict(Km=0.03, Ra=0.6, Vmax=24.0, Imax=10.0, Jm=5e-6, bN=4.0)}     # 40 N, 34 A allowed by the supply at 1.5 m/s


def chassis(Rw=0.04, kt=20000.0, motor="12V3A", pv=0, vk=1.5, k=600.0, c=8.0, csky=0.0):
    mo = dict(MOTORS[motor]); b = mo.pop("bN"); mw = WHEELS[Rw]
    return dict(Rw=Rw, mw=mw, Iw=0.5 * mw * Rw * Rw, kt=kt, ct=5.0 * (kt / 20000.0) ** 0.5, k=k, c=c, csky=csky, Ngear=b * Rw / mo["Km"], **mo,
                Kp=FORCE_KP / b, Ki=FORCE_KI / b, pv=float(pv), vk=vk, xk0=XK - 0.10, xk1=XK + 0.10, Lramp=0.45)


def holder(kind):
    if kind == "fixed": return dict(Mb=1.5 + ML)
    zp = float(kind.split("@")[1]) * 1e-3; p = H.pendulum(zp)
    d = dict(Mb=1.4, gimbal=1.0, cphi=0.002, mp=p["mp"], Lc=p["Lc"], IO=p["IO"], s_surf=p["s_surf"], tune=0.0)
    if kind.startswith("tuned"): d.update(tune=1.0, tauMax=0.5)
    return d


if __name__ == "__main__":
    go, info = C.build(4.0); rows = []; t0 = time.time()
    grid = list(itertools.product([0.04, 0.06, 0.08, 0.10], [20000.0, 6000.0], ["12V3A", "24V10A"], [0, 1, 2], [1.5, 1.0],
                                  ["fixed", "free@200", "free@300", "tuned@250"]))
    for n, (Rw, kt, mo, pv, vk, hd) in enumerate(grid):
        P = dict(chassis(Rw, kt, mo, pv, vk), **holder(hd)); o, Pf = go(P, KERB, 1.5); m = C.metrics(o, Pf, WS)
        rows.append(dict(Rw=Rw, kt=kt, motor=mo, pv=pv, vk=vk, holder=hd, **m))
        if PROG and n % 8 == 0: os.system(f'bash "{PROG}" -n fig16-sweep {n + 1}/{len(grid)} "cart variants on the kerb" >/dev/null 2>&1')
    json.dump(dict(road=KERB, v0=1.5, seconds=round(time.time() - t0), rows=rows), open(os.path.join(HERE, "sweep.json"), "w"), indent=0)
    if PROG: os.system(f'bash "{PROG}" -n fig16-sweep done >/dev/null 2>&1')
    print(len(rows), "variants in", round(time.time() - t0), "s")
