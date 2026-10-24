"""Size the bob: the smallest mass of the 1-2-5 series (rod 0.1 m) whose worst mounting still gives the sensor ten times its need
through the real generator (formula (7.6)-(7.7), L4_generator.py, best catalogue ratio and load, swing <= 0.5 rad), with twice
the catalogue friction and a gear efficiency of 50 %.

Run: python3 -I design.py   (writes design.json; PASS if setup.M is that mass)
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
import L4_generator as Gm

NEED = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensor.json')))['need_uW']*1e-6
T0_SHEET = Gm.T0


def best_load(Om, rp, fric_mult, eta_fix):
    Gm.T0 = T0_SHEET*fric_mult
    best = 0.0
    for N, eta, Jg in Gm.RATIOS:
        e = eta_fix or eta
        ce = Gm.best_brake(Om, rp, N, e, Jg)
        if ce is not None:
            best = max(best, Gm.powers(Om, rp, N, e, Jg, ce)['P_load'])
    Gm.T0 = T0_SHEET
    return best


series = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
rows = []
for m in series:
    Gm.m, Gm.L = m, S.L
    worst = min(best_load(Om, rp, 2, 0.5) for v, f, Om, rp in S.mountings())
    rows.append(dict(m=m, worst_W=worst, times_need=worst/NEED))
    print(f'M = {m:5.2f} kg: worst mounting {worst*1e3:7.3f} mW = {worst/NEED:6.1f} x the need (friction x2, gear 50 %)')
pick = next(r['m'] for r in rows if r['times_need'] >= 10)
json.dump(dict(rows=rows, pick=pick, need_uW=NEED*1e6), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'design.json'), 'w'), indent=1)
ok = pick == S.M
print(('PASS' if ok else 'FAIL') + f' smallest mass meeting 10 x the need: {pick} kg; setup.M = {S.M} kg')
raise SystemExit(0 if ok else 1)
