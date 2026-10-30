"""The two torques on the rotor against its speed, for the torque-law figure of section 6.5 of the notes.

Q_gen(Omega): the NREL baseline torque law on the low-speed shaft (nrel5mw.gen_torque_lss: zero below 670 generator rpm, a linear
ramp to 871 rpm, then k w^2), and the pure square law k Omega^2 for comparison. Q_aero(v, Omega) at pitch 0 from the ROSCO C_p
table (turbulence.q_aero) at the winds 6, 7, 8, 9, 10 m/s. Where Q_aero = Q_gen the rotor runs steadily; the crossings are
written too, so the figure and the text can say where the rotor sits.
Run: python3 -I L2_torque_curve.py   (writes L2_torque.json; PASS/FAIL)
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrel5mw as T5
import turbulence as TB

HERE = os.path.dirname(os.path.abspath(__file__))
rpm = np.linspace(5.5, 11.5, 241)
Om = rpm*2*math.pi/60
qg = np.array([T5.gen_torque_lss(o)[0] for o in Om])
TB.TORQUE_LAW = 'k2'; qk = np.array([TB.gen_torque(o) for o in Om]); TB.TORQUE_LAW = 'nrel'
winds = [6.0, 7.0, 8.0, 9.0, 10.0]
qa = {v: np.array([float(TB.q_aero(v, o)) for o in Om]) for v in winds}

def crossing(a, b):
    d = a - b
    i = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    if len(i) == 0:
        return None
    i = i[-1]; t = d[i]/(d[i] - d[i + 1])
    return float(rpm[i] + t*(rpm[i + 1] - rpm[i]))

cross = {str(v): dict(nrel=crossing(qa[v], qg), k2=crossing(qa[v], qk)) for v in winds}
ramp = dict(start_rpm=T5.GEN_R1/T5.N_GEAR, end_rpm=T5.GEN_R2/T5.N_GEAR)
out = dict(rpm=rpm.tolist(), Q_gen=qg.tolist(), Q_k2=qk.tolist(), Q_aero={str(v): qa[v].tolist() for v in winds}, cross=cross, ramp=ramp)
json.dump(out, open(os.path.join(HERE, 'L2_torque.json'), 'w'))

fails = 0
def check(name, ok):
    global fails
    print(('PASS ' if ok else 'FAIL ') + name); fails += 0 if ok else 1
check('ramp from 6.9 to 8.98 rpm', abs(ramp['start_rpm'] - 670/97) < 1e-9 and abs(ramp['end_rpm'] - 871/97) < 1e-9)
check('8 m/s: the NREL law and the square law cross the wind at the same speed (above the ramp)', abs(cross['8.0']['nrel'] - cross['8.0']['k2']) < 1e-3)
check('6 m/s: the NREL law crosses on the ramp, faster than the square law', cross['6.0']['nrel'] > cross['6.0']['k2'] and cross['6.0']['nrel'] < ramp['end_rpm'])
print({k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in cross.items()})
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
