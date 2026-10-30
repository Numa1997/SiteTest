"""The frequency response behind section 8.2 of the notes, for its figure: where along the frequency axis the generator's power
comes from, for the 1 m second blade at its best brake for the shaking (0.5 % blade damping, 5 mm tip rms).

Uses L3_shake2.py's own model (linear_mats, device, gen_power, the blade's modal data) unchanged. Per angular frequency w:
  |H_e|^2      the bare blade's tip response per unit modal force, 1/((k_b - m_b w^2)^2 + (c_b w)^2)
  dP/dw        S_0 c |i w (chi - Phi' y)|^2, the generator's power density (its integral over the band is the harvest)
over 0.4 to 2.2 Hz, so that both the blade's mode (1.08 Hz) and the second blade's own swing (sqrt(R) Omega/2pi) show.
The harvest integrated over the band of L3_shake2.py (0.7 to 1.3 times the mode) is checked against L3_shake2.json.
Run: python3 -I L3_response.py   (writes L3_response.json; PASS/FAIL)
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import L3_shake2 as L3
import setup as S

HERE = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(HERE, 'L3_shake2.json')))
row = [r for r in ref['rows'] if r['zeta'] == 0.005 and r['sig_tip'] == 0.005 and r['device'].startswith('second blade')][0]
zeta, sig, c = row['zeta'], row['sig_tip'], row['c']
dev = L3.device(S.L_B)
(Mf, Gf, Kf, d), rows, _ = dev

def density(ws):
    """generator power per unit angular frequency, and the bare blade's |H_e|^2, on the grid ws (rad/s)"""
    M = np.array(Mf(L3.OM0, L3.RP, L3.PHI, L3.M_E, L3.K_E), float); G = np.array(Gf(L3.OM0, L3.RP, L3.PHI, L3.M_E, L3.K_E), float)
    K = np.array(Kf(L3.OM0, L3.RP, L3.PHI, L3.M_E, L3.K_E), float)
    R0 = rows[0].copy(); R0[0] = -L3.PHID
    C = c*np.outer(R0, R0) + np.diag([2*zeta*L3.W_E*L3.M_E] + [0]*(d - 1))
    band = L3.W_E*np.linspace(0.7, 1.3, 6001)
    He2b = 1/((L3.K_E - L3.M_E*band**2)**2 + (2*zeta*L3.W_E*L3.M_E*band)**2)
    S0 = sig**2/np.trapezoid(He2b, band)                     # as L3_shake2.gen_power: the bare blade has tip rms sig
    e0 = np.zeros(d); e0[0] = 1.0
    H = np.array([np.linalg.solve(K - w*w*M + 1j*w*(C + G), e0) for w in ws])
    dens = S0*c*np.abs(1j*ws*(H @ R0))**2
    He2 = 1/((L3.K_E - L3.M_E*ws**2)**2 + (2*zeta*L3.W_E*L3.M_E*ws)**2)
    return dens, He2, S0

band = L3.W_E*np.linspace(0.7, 1.3, 6001)
P_band = float(np.trapezoid(density(band)[0], band))
f = np.linspace(0.4, 2.2, 1801); ws = 2*math.pi*f
dens, He2, S0 = density(ws)
R = 1.5*L3.RP/S.L_B
f_own = math.sqrt(R)*L3.OM0/(2*math.pi)                     # the second blade's own swing, flicked: sqrt(R) per turn
out = dict(f_Hz=f.tolist(), dPdf_W_per_Hz=(dens*2*math.pi).tolist(), He2_rel=(He2/He2.max()).tolist(), f_mode=L3.W_E/(2*math.pi),
           f_own=f_own, c=c, zeta=zeta, sig_tip=sig, P_band_W=P_band, P_ref_W=row['P'])
json.dump(out, open(os.path.join(HERE, 'L3_response.json'), 'w'))

fails = 0
def check(name, ok):
    global fails
    print(('PASS ' if ok else 'FAIL ') + name); fails += 0 if ok else 1
check(f'harvest over the band {P_band*1e3:.4f} mW equals L3_shake2.json {row["P"]*1e3:.4f} mW', abs(P_band/row['P'] - 1) < 1e-6)
check(f'the second blade\'s own frequency {f_own:.3f} Hz lies above the mode {L3.W_E/(2*math.pi):.4f} Hz', f_own > L3.W_E/(2*math.pi))
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
