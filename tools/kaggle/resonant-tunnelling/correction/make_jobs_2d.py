"""Writes jobs_2d.json: every stored disc and shell run of generation 2 (2,609), with what the 2D rerun needs to match its stored
file (spec, frame step, frame count, last frame time, the parent's SHA-256) and a cost estimate (fine cells x steps).
Usage: python3 make_jobs_2d.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, "..", "..", "..", "..", "public/data/resonant-tunnelling/2026-11-14/kaggle/index.json")
d = json.load(open(IDX)); J = []
for r in d["runs"]:
    sp = r["spec"]
    if sp["shape"] == "flat": continue
    steps = int(round(r["frame_dt"] / 0.01)) * 199
    J.append(dict(file=r["file"], sha256=r["sha256"], spec=sp, group=r["group"], n=200, frame_dt=r["frame_dt"], t_end=r["t_end"],
                  steps=steps, cost=sp["Nx"] * 2 / 0.0625 * 256 * steps))
json.dump(J, open(os.path.join(HERE, "jobs_2d.json"), "w"), separators=(",", ":"))
print(len(J), "jobs;", sum(j["steps"] for j in J), "steps;", round(sum(j["cost"] for j in J) / 1e12, 2), "e12 cell-steps")
