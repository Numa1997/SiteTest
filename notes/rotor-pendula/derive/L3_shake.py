"""L3: random edgewise shaking of the blade, the main test. Linear frequency-domain theory (exact for the linear response).

Run: python3 -I L3_shake.py   (writes L3_shake.json; prints the comparison)
Blade: first edgewise mode of the NREL 5-MW, f_e = 1.0793 Hz, total damping zeta_e (swept 0.5, 1, 3 %), driven by broadband
turbulent forcing, so its tip motion is narrowband: tip rms sigma_tip (swept 0.005, 0.02, 0.1 m; no measured value exists,
dossier-edgewise.md). Pivot at 90 % of the rotor radius, edgewise mode shape Phi_p = 0.823: the pivot's tangential acceleration
has the one-sided spectrum S_a(w) = Phi_p^2 sigma_tip^2 w^4 |H_e(w)|^2 / int |H_e|^2, H_e = 1/(w_e^2 - w^2 + 2i zeta_e w_e w).
Rotor at uniform Omega (steady 8 m/s, 0.9494 rad/s), gravity g cos 5 deg.
Devices, all 0.1 kg: Sol's single (L = 0.2 m); the double of equal mass and reach (0.05 kg + 0.05 kg, 0.1 m + 0.1 m, equal
generators); a single tuned to the blade mode, Omega sqrt(r_p/L) = w_e, L = 1.11 m.  Each at the brake that maximises its
TOTAL power (gravity + shaking).
Linear model (relative angles q, mass matrix M, centrifugal stiffness K, generator matrix C, base-acceleration vector f):
  M q'' + C q' + K q = f_g cos(Omega t) + f a(t)  ->  power = (1/2) Omega^2 z_g^* C z_g + int S_a(w) w^2 z(w)^* C z(w) dw
Rotor-speed wander (L2: sigma_Omega/Omega = 0.103) detunes the tuned single: its total power is also averaged over a Gaussian
spread of Omega (quasi-static), with c held fixed.
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar
g = 9.80665*math.cos(math.radians(5.0))
OM = 0.9494; we = 2*math.pi*1.0793; PHI = 0.8232; rp = 0.9*63.0

def matrices(kind, L, Om):
    if kind == 'single':
        M = np.array([[0.1*L**2]]); K = Om**2*np.array([[0.1*L*rp]]); f = -np.array([0.1*L])
        Cs = lambda c: np.array([[c]])
    else:
        m1 = m2 = 0.05; l1 = l2 = L/2
        A = (m1 + m2)*l1**2; B = m2*l2**2; D = m2*l1*l2
        M = np.array([[A, D], [D, B]]); K = Om**2*np.array([[(m1 + m2)*l1*rp + D, -D], [-D, m2*l2*rp + D]])
        f = -np.array([(m1 + m2)*l1, m2*l2])
        Cs = lambda c: c*np.array([[2.0, -1.0], [-1.0, 1.0]])
    return M, K, f, Cs

def power(kind, L, c, Om, sig_tip, zeta, ws):
    M, K, f, Cs = matrices(kind, L, Om); C = Cs(c)
    # gravity: force g f cos(Om t) (gravity's tangential push on each mass, as the base acceleration term with a = g cos)
    z = np.linalg.solve(K - Om**2*M + 1j*Om*C, g*f)
    Pg = 0.5*Om**2*np.real(np.conj(z) @ C @ z)
    if sig_tip == 0:
        return Pg, 0.0
    He2 = 1/((we**2 - ws**2)**2 + (2*zeta*we*ws)**2)
    Sa = (PHI*sig_tip)**2*ws**4*He2/np.trapezoid(He2, ws)
    Pe = 0.0
    zz = np.array([np.linalg.solve(K - w*w*M + 1j*w*C, f) for w in ws])
    integrand = Sa*ws**2*np.real(np.einsum('wi,ij,wj->w', np.conj(zz), C, zz))
    Pe = np.trapezoid(integrand, ws)
    return Pg, Pe

def best(kind, L, Om, sig, zeta, ws):
    r = minimize_scalar(lambda lc: -sum(power(kind, L, math.exp(lc), Om, sig, zeta, ws)), bounds=(-12, 4), method='bounded',
                        options={'xatol': 1e-5})
    c = math.exp(r.x)
    return c, power(kind, L, c, Om, sig, zeta, ws)

L_tuned = rp*OM**2/we**2
out = dict(L_tuned=L_tuned, rows=[])
print(f'tuned single needs L = {L_tuned:.3f} m (own frequency {OM*math.sqrt(rp/L_tuned)/(2*math.pi):.4f} Hz)')
for zeta in (0.005, 0.01, 0.03):
    ws = we*np.linspace(0.5, 1.5, 20001)
    for sig in (0.0, 0.005, 0.02, 0.1):
        line = f'zeta_e {zeta*100:.1f} %, tip rms {sig:.3f} m (pivot accel rms {PHI*sig*we**2:.2f} m/s^2): '
        row = dict(zeta=zeta, sig_tip=sig)
        for name, kind, L in (('Sol single', 'single', 0.2), ('double', 'double', 0.2), ('tuned single', 'single', L_tuned)):
            c, (Pg, Pe) = best(kind, L, OM, sig, zeta, ws)
            row[name] = dict(c=c, Pg=Pg, Pe=Pe)
            line += f'{name} {1e3*(Pg + Pe):.3f} mW (shaking {1e3*Pe:.3f}); '
        # tuned single with the rotor speed wandering, c held at its best for the mean speed
        c = row['tuned single']['c']
        Oms = OM*(1 + 0.103*np.linspace(-3, 3, 61)); wts = np.exp(-0.5*np.linspace(-3, 3, 61)**2); wts /= wts.sum()
        tot = np.array([sum(power('single', L_tuned, c, O, sig, zeta, ws)) for O in Oms])
        row['tuned_wander_mean'] = float(np.sum(wts*tot))
        line += f'tuned with speed wander {1e3*row["tuned_wander_mean"]:.3f} mW'
        print(line, flush=True)
        out['rows'].append(row)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L3_shake.json'), 'w'), indent=1)
