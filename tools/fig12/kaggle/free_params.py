import os, sys, json, time, re, subprocess, datetime, math
from pathlib import Path
import numpy as np
# Free swing tests of solver v2 (13 November 2026): how fast the stout's first sloshing mode dies in a glass held still,
# after one short push, with each piece of physics switched on in turn:
#   v1        the solver of the stored rides (12 Nov), for comparison
#   inviscid  v2 with no friction at all: the loss of the numbers alone
#   wall      v2 with the stout's viscosity and the glass's boundary layer
#   full      v2 with the head of foam rubbing the glass too
PLAN = os.environ.get("NB_PLAN", "0.003:inviscid,wall;0.002:inviscid,wall;0.0015:inviscid,wall,full,v1")
RUNS = [(float(g), m) for part in PLAN.split(";") for g, ms in [part.split(":")] for m in ms.split(",")]
FILL = 0.125               # m, stout height in the glass (the website's fill)
RHO = 1007.0               # kg/m^3, Guinness (Benilov, Cummins & Lee 2013)
PPC = 2                    # particles per cell along each axis (8 per cell), as in the rides
SETTLE = 0.3               # s at rest first (the seeded lattice relaxes)
PUSH_A, PUSH_T = 1.0, 0.146   # m/s^2 and s: one half-sine push along x, half a period of the first mode (3.42 Hz)
FREE = float(os.environ.get("NB_FREE", "4.554"))   # s of free swing after the push (5 s in all)
FPS = 30
MS_STEP = {0.003: 18, 0.002: 62, 0.0015: 145}   # ms per 2 ms step on Kaggle's T4: v1 measured 123 at 1.5 mm (rides, 12 Nov) + 18 % for the level set, others scaled by cells
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
WORK = Path(os.environ.get("NB_WORK", "/kaggle/working")) / STAMP; WORK.mkdir(parents=True, exist_ok=True); T0 = time.time()

def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc):%H:%M:%S} UTC  {(time.time() - T0) / 60:5.1f} min  {msg}"
    print(line, flush=True)
    with open(WORK / "progress.log", "a") as f: f.write(line + "\n")

steps = (SETTLE + PUSH_T + FREE) / 0.002
print("What the machine does: holds the pint still, gives it one short push, and lets the stout swing freely,")
print("once for each grid and piece of physics, recording the stout's energy, momentum and surface 30 times a second.")
for g, m in RUNS: print(f"grid {g * 1e3:.1f} mm, {m}: {steps:,.0f} steps x {MS_STEP.get(g, 145)} ms = {steps * MS_STEP.get(g, 145) / 6e4:.1f} min")
print(f"total about {sum(steps * MS_STEP.get(g, 145) for g, m in RUNS) / 6e4:.1f} min, plus about 2 min to start")
