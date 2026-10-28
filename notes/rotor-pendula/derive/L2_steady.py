"""Where does the NREL 5 MW rotor really turn in a steady wind? The notes hold it at the best tip-speed ratio lambda* = 7.55
(Omega = lambda* v / r). This script balances the wind's torque (ROSCO C_p table, pitch 0) against the turbine's own
torque law, the full baseline law and the pure square law k Omega^2, at 6, 8 and 10 m/s, and says what the real speed
does to the second blade's best power, which goes as 1/Omega on a long rotor (2.7) and exactly as (2.5).
Run: python3 -I L2_steady.py   (seconds; writes L2_steady.json)
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import brentq
import setup as S
import turbulence as TB
out = []
for v, Om_lam, rp in S.mountings():
    row = dict(wind=v, Om_lam=Om_lam)
    for law in ('nrel', 'k2'):
        TB.TORQUE_LAW = law
        Om = brentq(lambda O: TB.q_aero(v, O) - TB.gen_torque(O), 0.3, 1.6)
        row[law] = dict(Om=Om, rpm=Om*60/(2*math.pi), lam=Om*S.R_ROT/v, cp=float(TB.cp(Om*S.R_ROT/v)),
                        P_ratio=S.pstar(Om)/S.pstar(Om_lam))
    out.append(row)
    print(f"{v:.0f} m/s: lambda* gives {Om_lam*60/2/math.pi:.2f} rpm; full law {row['nrel']['rpm']:.2f} rpm (lambda {row['nrel']['lam']:.2f}, "
          f"P*/P*(lambda*) = {row['nrel']['P_ratio']:.3f}); square law {row['k2']['rpm']:.2f} rpm (lambda {row['k2']['lam']:.2f})")
TB.TORQUE_LAW = 'nrel'
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L2_steady.json'), 'w'), indent=1)
