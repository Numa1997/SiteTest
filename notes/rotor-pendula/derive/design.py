"""Size the second blade (length setup.L_B = 1 m, a modelling choice): the mass of the 1-2-5 series at which the maxon RE 25 +
GP 32 C takes the largest share of the best power P*, averaged over the three winds (formula (7.6)-(7.7), L4_generator.py, best
catalogue ratio and load within the gearhead's continuous torque, swing <= 0.5 rad). Also reported: the sensor's margin at the
chosen mass with twice the catalogue friction and a gear efficiency of 50 %, which must be at least 10 at every wind.

Run: python3 -I design.py   (writes design.json; PASS if setup.M_B is that mass and the margin holds)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
import L4_generator as Gm

NEED = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensor.json')))['need_uW']*1e-6
SERIES = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]


def at_mass(mass, fric=1.0, eta_fix=None):
    Gm.m, Gm.L = mass, S.L_B
    T0, RAT = Gm.T0, Gm.RATIOS
    Gm.T0 = T0*fric
    if eta_fix:
        Gm.RATIOS = [(N, eta_fix, Jg) for N, eta, Jg in RAT]
    try:
        res = [(Gm.best_for(Om, rp)[0], S.pstar(Om, m=mass)) for v, Om, rp in S.mountings()]
    finally:
        Gm.T0, Gm.RATIOS = T0, RAT
    return res


rows = []
for mass in SERIES:
    r = at_mass(mass)
    share = sum(b['P_load']/p for b, p in r)/len(r)
    rows.append(dict(m=mass, share=share, P_load_W=[b['P_load'] for b, _ in r], N=[b['N'] for b, _ in r], Pstar_W=[p for _, p in r]))
    print(f'm = {mass:5.2f} kg: share of P* {share*100:5.1f} % (winds 6, 8, 10 m/s: '
          + ', '.join(f"{b['P_load']*1e3:.2f} mW at N {b['N']}" for b, _ in r) + ')')
pick = max(rows, key=lambda r: r['share'])['m']
pess = at_mass(pick, fric=2.0, eta_fix=0.5)
margin = min(b['P_load'] for b, _ in pess)/NEED
json.dump(dict(rows=rows, pick=pick, need_uW=NEED*1e6, pessimistic_W=[b['P_load'] for b, _ in pess], margin=margin),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'design.json'), 'w'), indent=1)
print(f'pessimistic (friction x2, gear 50 %) at {pick} kg: worst wind {min(b["P_load"] for b, _ in pess)*1e3:.2f} mW = {margin:.0f} x the sensor\'s {NEED*1e6:.1f} uW')
ok = pick == S.M_B and margin >= 10
print(('PASS' if ok else 'FAIL') + f' the best-matched mass is {pick} kg; setup.M_B = {S.M_B} kg; sensor margin {margin:.0f} >= 10')
raise SystemExit(0 if ok else 1)
