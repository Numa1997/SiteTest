"""Fig. 15 correction: radial-range convergence of the shells in the (x, rho) solver (Kaggle GPU).
The smoke test (17ffd02, 14 Nov) found the shells NOT converged at the base grid: Rmax 64 -> 96 moved T of
shell_N2_V2_D1_P2.5_R3_B0_s3_E0.750 from 0.6125 to 0.6220. Here four shells (R 3 and 5, N 1 and 2, low and high E) run at
Rmax 64 / 96 / 128 / 160 / 192 a (Nr scaled with Rmax so the radial step stays 0.25 a; rho border 12 a, then 24 a), complex64,
plus the widest grid in complex128 on one shell. The grid for the production shells is the smallest Rmax whose T differs from
the next wider one by < 0.002 on every shell. One line per run in progress.log and shellconv.jsonl (and the live tracker).
"""
import os, sys, json, time
import numpy as np
exec(open("rt2d_run.py").read().split('if __name__ == "__main__" or globals().get("RUN"):')[0])
J = {j["file"]: j for j in json.load(open("jobs_2d.json"))}
OUTD = ROOT + "/shellconv"; os.makedirs(OUTD, exist_ok=True); SJ = open(OUTD + "/shellconv.jsonl", "a")
say("devices:", jax.devices(), "jax", jax.__version__, "shell convergence")
BASE = dict(hx=0.0625, Nr=256, Rmax=64.0, Wr=12.0, dt=0.01, box_factor=2.0)
PICKS = ["shell_N2_V2_D1_P2.5_R3_B0_s3_E0.750.bin", "shell_N2_V2_D1_P2.5_R5_B0_s3_E0.300.bin",
         "shell_N1_V2_D1_P2.5_R3_B0_s3_E1.500.bin", "shell_N1_V2_D1_P2.5_R5_B0_s3_E0.750.bin"]
PICKS = [f for f in PICKS if f in J] or [f for f in J if J[f]["spec"]["shape"] == "shell"][:4]


def go(tag, sp, t_end, grid, dtype="c64"):
    t0 = time.time()
    o = aj.run(sp, t_end, hx=grid["hx"], Lx=sp["Nx"] * 0.5 * grid["box_factor"], Nr=grid["Nr"], Rmax=grid["Rmax"], Wr=grid["Wr"],
               dt=grid["dt"], nframes=40, dtype=dtype, box_half=0.5 * sp["Nx"] * 0.5, rule=grid.get("rule", "cell"))
    rec = dict(tag=tag, spec=sp, grid=grid, dtype=dtype, T=o["T"], T_unc=o["T_unc"], drift=o["drift"], steps=o["steps"],
               wall=round(time.time() - t0, 2), s_per_step=o["s_per_step"], cells=o["cells"])
    SJ.write(json.dumps(rec) + "\n"); SJ.flush()
    say(f"S {tag}: T {o['T']:.6f} +- {o['T_unc']:.1e} drift {o['drift']:.1e} {o['steps']} steps {o['s_per_step']*1e3:.3f} ms/step "
        f"cells {o['cells']} wall {time.time()-t0:.1f} s")
    return o["T"]


RES = {}
for f in PICKS:
    j = J[f]; sp = j["spec"]; te = j["t_end"]; RES[f] = {}
    for Rmax in (64.0, 96.0, 128.0, 160.0, 192.0):
        g = dict(BASE, Rmax=Rmax, Nr=int(4 * Rmax), Wr=12.0 if Rmax <= 96 else 24.0)
        RES[f][Rmax] = go(f"{f} Rmax {Rmax:g} Nr {g['Nr']} Wr {g['Wr']:g}", sp, te, g)
    say(f"S {f} T(Rmax): " + ", ".join(f"{k:g}: {v:.5f}" for k, v in RES[f].items()))
go(f"{PICKS[0]} Rmax 160 c128", J[PICKS[0]]["spec"], J[PICKS[0]]["t_end"], dict(BASE, Rmax=160.0, Nr=640, Wr=24.0), "c128")
ok = None
for Rmax in (64.0, 96.0, 128.0, 160.0):
    nxt = {64.0: 96.0, 96.0: 128.0, 128.0: 160.0, 160.0: 192.0}[Rmax]
    if all(abs(RES[f][Rmax] - RES[f][nxt]) < 0.002 for f in PICKS): ok = Rmax; break
json.dump(dict(T=RES, converged_Rmax=ok), open(OUTD + "/shellconv_summary.json", "w"), indent=1)
say(f"S shellconv done: smallest converged Rmax = {ok}")
