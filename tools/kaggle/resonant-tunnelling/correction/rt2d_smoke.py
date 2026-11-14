"""Fig. 15 correction: the Kaggle T4 smoke test of the 2D (x, rho) solver. It measures the step time for the bill and checks:
  A. wall limit: a disc wider than the rho range (R = 1000) against the exact walls (T_exact given, from exact_wall.py);
  B. convergence on 3 stored runs: hx 0.125 / 0.0625 / 0.03125, Nr 256 / 384 at Rmax 64, Rmax 64 / 96, dt 0.01 / 0.005,
     box 2x / 3x, complex64 / complex128 (the norm drift and the T difference);
  C. rt3d2's drawing at 0.5 a (V0 on x points strictly inside, the azimuthal average of the Cartesian staircase disc, the stored
     box, rho range 32 a with a 6.4 a border): the RT3C files are written, and T_far and the curves are compared on the CPU with
     the stored 3D files.
Every result is one line in progress.log and one record in smoke.jsonl, written as it ends.
"""
import os, sys, json, time
import numpy as np
SMOKE = []
exec(open("rt2d_run.py").read().split('if __name__ == "__main__" or globals().get("RUN"):')[0])
J = {j["file"]: j for j in json.load(open("jobs_2d.json"))}
OUTD = ROOT + "/smoke"; os.makedirs(OUTD, exist_ok=True); SJ = open(OUTD + "/smoke.jsonl", "a")
say("devices:", jax.devices(), "jax", jax.__version__)
BASE = dict(hx=0.0625, Nr=256, Rmax=64.0, Wr=12.0, dt=0.01, box_factor=2.0)


def go(tag, sp, t_end, grid, dtype="c64", frame_dt=None, write=None):
    global GRID, DTYPE
    t0 = time.time()
    if write:
        GRID = dict(grid); DTYPE = dtype
        blob, head, o = one(write, jax.devices()[0]); open(f"{OUTD}/{write['file']}", "wb").write(blob)
    else:
        o = aj.run(sp, t_end, hx=grid["hx"], Lx=sp["Nx"] * 0.5 * grid["box_factor"], Nr=grid["Nr"], Rmax=grid["Rmax"], Wr=grid["Wr"],
                   dt=grid["dt"], nframes=40, frame_dt=frame_dt, dtype=dtype, box_half=0.5 * sp["Nx"] * 0.5, rule=grid.get("rule", "cell"))
    rec = dict(tag=tag, spec=sp, grid=grid, dtype=dtype, T=o["T"], T_unc=o["T_unc"], drift=o["drift"], steps=o["steps"],
               wall=round(time.time() - t0, 2), s_per_step=o["s_per_step"], cells=o["cells"])
    SJ.write(json.dumps(rec) + "\n"); SJ.flush()
    say(f"{tag}: T {o['T']:.6f} +- {o['T_unc']:.1e} drift {o['drift']:.1e} {o['steps']} steps {o['s_per_step']*1e3:.3f} ms/step "
        f"cells {o['cells']} wall {time.time()-t0:.1f} s")


# A. wall limit (T_exact from exact_wall.py, box 2x)
wall = dict(shape="coin", N=2, V0=2.0, D=1.0, P=2.5, R=1000.0, E=0.75, bias=0.0, sx=3.0, sp=3.0, Nx=192)
go("A wall-limit N2 E0.75 (exact 0.196820)", wall, 100.0, BASE)
go("A wall-limit N2 E0.75 c128", wall, 100.0, BASE, "c128")
wall10 = dict(wall, N=10, E=0.9, Nx=256)
go("A wall-limit N10 E0.9 (exact 0.166225)", wall10, 220.89, BASE)
wallb = dict(wall, bias=2.125, E=0.5)
go("A wall-limit bias 2.125 E0.5 (exact 0.039048)", wallb, 85.57, BASE)

# B. convergence on three stored runs
picks = ["coin_N2_V2_D1_P2.5_R6_B0_s3_E0.750.bin", "coin_N10_V2_D1_P2.5_R12_B0_s3_E0.900.bin", "shell_N2_V2_D1_P2.5_R3_B0_s3_E0.750.bin"]
for f in picks:
    j = J[f]; sp = j["spec"]; te = j["t_end"]
    go(f"B {f} base", sp, te, BASE)
    go(f"B {f} c128", sp, te, BASE, "c128")
    for k, v in (("hx", 0.125), ("hx", 0.03125), ("Nr", 384), ("dt", 0.005), ("box_factor", 3.0)):
        go(f"B {f} {k}={v}", sp, te, dict(BASE, **{k: v}))
    go(f"B {f} Rmax96 Nr384", sp, te, dict(BASE, Rmax=96.0, Nr=384))

# C. rt3d2's drawing at 0.5 a on three stored runs, written as RT3C for the CPU comparison
RULE = dict(hx=0.5, Nr=64, Rmax=32.0, Wr=6.4, dt=0.01, box_factor=1.0, rule="rt3d2")
for f in ["coin_N2_V2_D1_P2.5_R6_B0_s3_E0.750.bin", "coin_N2_V2_D1_P2.5_R12_B0_s3_E1.200.bin", "shell_N2_V2_D1_P2.5_R5_B0_s3_E0.750.bin"]:
    go(f"C {f} rt3d2 rules", J[f]["spec"], J[f]["t_end"], RULE, write=J[f])

# the bill's step time: the production grid on the three box sizes
for f in [k for k in J if J[k]["spec"]["Nx"] == 256][:1] + [k for k in J if J[k]["spec"]["Nx"] == 512][:1]:
    go(f"T {f} production grid", J[f]["spec"], min(J[f]["t_end"], 30.0), BASE)
say("smoke done")
