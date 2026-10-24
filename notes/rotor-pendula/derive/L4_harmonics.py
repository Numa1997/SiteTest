"""L4: why the describing function misses the load power on the fast rotors. Integrate the full equation (as L4_check.py) at
two mountings, record one steady turn, and split the rod's angular speed theta' into harmonics of the turn: the share of the
mean square speed <theta'^2> carried by harmonics 2 and above, and the swing amplitude against a pure cosine.
Also: the part of the friction torque's first harmonic that is in step with the speed, against the describing function's 4f/pi.
Run: python3 -I L4_harmonics.py"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
from L4_generator import KT, KE, RC, JM, T0, m, L, g
res = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L4_generator.json')))
pick = [r for r in res if (r['rpm'], r['frac']) in ((200, 0.6), (100, 0.3), (8, 0.9), (400, 0.3))]
R = np.array([r['rp']/L for r in pick]); Om = np.array([r['Om'] for r in pick]); G = g/(Om**2*L)
N = np.array([float(r['N']) for r in pick]); eta = np.array([r['eta'] for r in pick])
j = (JM + np.array([r['Jg'] for r in pick]))*N**2/(m*L**2); ke = np.array([r['c_e'] for r in pick])/(m*L**2*Om)
f = N*T0/(eta*m*L**2*Om**2); eps = 1e-3*np.array([r['Theta'] for r in pick])
def F(t, Y):
    th, w = Y[:, 0], Y[:, 1]
    return np.stack([w, -((ke/eta)*w + f*np.tanh(w/eps) + R*np.sin(th) + G*np.cos(t + th))/(1 + j)], axis=1)
nst = 2048; h = 2*math.pi/nst; Y = np.zeros((len(pick), 2)); W = []; TH = []
for k in range(nst*41):
    Y, _ = radau_step(F, k*h, Y, h)
    if k >= nst*40:
        W.append(Y[:, 1].copy()); TH.append(Y[:, 0].copy())
W = np.array(W); TH = np.array(TH); out = []
for i, r in enumerate(pick):
    c = np.fft.rfft(W[:, i])/nst; p = 2*np.abs(c[1:])**2          # mean square of each harmonic (cos^2 average 1/2)
    tot = np.mean(W[:, i]**2)
    print(f"{r['rpm']:3d} rpm {r['frac']*100:.0f} %, N = {r['N']}: <theta'^2> = {tot:.3e}; harmonic 1 carries {p[0]/tot*100:.1f} %, "
          f"3: {p[2]/tot*100:.1f} %, 5: {p[4]/tot*100:.1f} %, even: {sum(p[1::2])/tot*100:.2f} %; "
          f"swing peak {np.max(np.abs(TH[:, i] - TH[:, i].mean())):.4f}, first-harmonic amplitude {2*abs(np.fft.rfft(TH[:, i])[1])/nst:.4f}, "
          f"formula {r['Theta']:.4f} rad; friction/gravity {f[i]/G[i]:.2f}, natural frequency {math.sqrt(R[i]/(1 + j[i])):.2f} per turn")
    fr = f[i]*np.tanh(W[:, i]/eps[i]); cf = np.fft.rfft(fr)[1]; cw = np.fft.rfft(W[:, i])[1]
    inph = (cf*np.conj(cw)).real/abs(cw)*2/nst                     # part of the friction's first harmonic in step with theta'
    print(f"      friction's first harmonic in step with the swing speed: {inph/(4*f[i]/math.pi):.3f} of the describing function's 4f/pi; "
          f"out of step: {((cf*np.conj(cw)).imag/abs(cw)*2/nst)/(4*f[i]/math.pi):+.3f}")
    out.append(dict(rpm=r['rpm'], frac=r['frac'], h3=float(p[2]/tot), Th1=float(2*abs(np.fft.rfft(TH[:, i])[1])/nst), Th_formula=r['Theta'],
                    inphase=float(inph/(4*f[i]/math.pi)), outphase=float(((cf*np.conj(cw)).imag/abs(cw)*2/nst)/(4*f[i]/math.pi))))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L4_harmonics.json'), 'w'), indent=1)
