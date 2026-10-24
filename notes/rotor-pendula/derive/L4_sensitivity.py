"""L4 sensitivity (the gearhead drag the catalogue does not give, and the backdriven efficiency): the formula (7.6)-(7.7) of
L4_generator.py for the second blade with the friction torque x1, x2 and the efficiency at the sheet value or 0.5, best catalogue
ratio and load each time (L4_generator.best_for: swing <= 0.5 rad, peak torque within the gearhead's rating); also the peak
load voltage, the motor's peak speed and the swing's frequency.  Run: python3 -I L4_sensitivity.py   (writes L4_sensitivity.json)"""
import json, math, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import setup as S
import L4_generator as Gm
T0, RAT = Gm.T0, Gm.RATIOS
res = []
for v, Om, rp in S.mountings():
    for mult, eb in ((1, None), (2, None), (1, 0.5), (2, 0.5)):
        Gm.T0 = T0*mult; Gm.RATIOS = [(N, eb or eta, Jg) for N, eta, Jg in RAT]
        try:
            b, _ = Gm.best_for(Om, rp)
        finally:
            Gm.T0, Gm.RATIOS = T0, RAT
        RL = b['R_load']
        V = Gm.KE*b['N']*b['Theta']*Om*RL/(RL + Gm.RC)                 # peak load voltage: k_e N thetadot_peak R_L/(R_c + R_L)
        res.append(dict(wind=v, fric=mult, eta=eb, P_load=b['P_load'], N=b['N'], Theta=b['Theta'], V=V,
                        motor_rpm=b['N']*b['Theta']*Om*60/(2*math.pi), f_turn=Om/(2*math.pi)))
        print(f'{v:.0f} m/s: friction x{mult}, eta {eb or "sheet"}: load {b["P_load"]*1e3:.2f} mW (x{b["P_load"]/37.6e-6:.0f} sensor), N {b["N"]}, '
              f'swing {b["Theta"]:.3f} rad, load V peak {V:.3f} V, motor {res[-1]["motor_rpm"]:.0f} rpm')
json.dump(res, open(os.path.join(D, 'L4_sensitivity.json'), 'w'), indent=1)
