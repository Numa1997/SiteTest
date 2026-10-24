"""Rerun of the L1 map cells that diverged numerically (G = 70 and 200, R = 1, 2, 5), with 4x the steps per turn.
Run: python3 -I L1_map_g70.py   (writes L1_map_g70.json; reports non-finite members, chaos, power)"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import L1_map as M
M.GS = [70, 200]
out = []
for R in (1, 2, 5):
    base = max(100, int(math.ceil(6*math.sqrt(M.omega_fast(R)**2 + 4*200))))
    orig = M.omega_fast
    M.omega_fast = lambda r, o=orig: 4*math.sqrt(o(r)**2 + 4*200)/1.0   # n = 6*4*sqrt(...): four times the steps
    res = M.run_R(R)
    M.omega_fast = orig
    bad = [m for m in res['members'] if not (math.isfinite(m['P']) and math.isfinite(m['lyap']))]
    ch = [m for m in res['members'] if math.isfinite(m['lyap']) and m['lyap'] > 0.01]
    print(f'R = {R}: {res["n_per_turn"]} steps/turn (was {base - base % 4}), non-finite {len(bad)}, chaotic {len(ch)}/{len(res["members"])}', flush=True)
    out.append(res)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_map_g70.json'), 'w'))
