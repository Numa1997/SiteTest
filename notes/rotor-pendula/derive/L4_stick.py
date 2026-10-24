"""L4: does the rod stick, and what voltage does the load see?  The full equation
(L4_full.py) at the settings of L4_scan.py, 2000 steps per turn, 60 turns to settle and 3 recorded: the fraction of the turn
with |theta'| below 1 % of its largest value, the EMF and the load voltage at their peaks, the motor speed.
Run: python3 -I L4_stick.py"""
import glob, json, math, os, sys
import numpy as np
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from engine import radau_step
from L4_generator import KT, KE, RC, JM, T0, m, L, g
from L4_full import make_rhs
gen = {(r['rpm'], r['frac']): r for r in json.load(open(os.path.join(D, 'L4_generator.json')))}
rows = [x for p in glob.glob(os.path.join(D, 'L4_scan_[0-9].json')) for x in json.load(open(p))]
rows = sorted(rows, key=lambda r: (r['wind'], r['frac']))
n=len(rows)
Om = np.array([gen[(r['rpm'], r['frac'])]['Om'] for r in rows]); rp = np.array([gen[(r['rpm'], r['frac'])]['rp'] for r in rows])
R = rp/L; G = g/(Om**2*L); Nn = np.array([float(r['N']) for r in rows]); eta = np.array([r['eta'] for r in rows])
j = (JM + np.array([r['Jg'] for r in rows]))*Nn**2/(m*L**2)
ce = np.array([r['c_e'] for r in rows]); ke = ce/(m*L**2*Om); f0 = Nn*T0/(m*L**2*Om**2)
keep = 1 - ce/(Nn**2*KT*KE/RC); sc = np.array([max(r['Theta'], 1e-2) for r in rows])
F = make_rhs(R, G, j, f0, ke, eta, keep, 1e-3*sc, 1e-3*G*sc)
nst=2000; settle, meas = 60, 3
h = 2*math.pi/nst; Y = np.zeros((n, 5))
W=[];TH=[]
for k in range(nst*(settle + meas)):
    if k == nst*settle: Y0 = Y.copy()
    Y, _ = radau_step(F, k*h, Y, h)
    if k >= nst*settle: W.append(Y[:,1].copy()); TH.append(Y[:,0].copy())
W=np.array(W); TH=np.array(TH)
u = m*L**2*Om**3; T = 2*math.pi*meas
Pl = (Y[:, 2] - Y0[:, 2])/T*u
out=[]
for i,r in enumerate(rows):
    th=TH[:,i]; w=W[:,i]; amp=0.5*(th.max()-th.min()); wmax=np.abs(w).max()
    stuck=np.mean(np.abs(w)<0.01*wmax)
    out.append(dict(wind=r['wind'], rpm=r['rpm'], frac=r['frac'], stuck=float(stuck), V_load_peak=float(KE*Nn[i]*wmax*Om[i]*r['R_load']/(RC+r['R_load'])), motor_rpm=float(Nn[i]*wmax*Om[i]*60/2/math.pi)))
    RL=r['R_load']; Vpk = KE*Nn[i]*wmax*Om[i]*RL/(RC+RL); emf=KE*Nn[i]*wmax*Om[i]
    print(f"{r['wind']:.0f} m/s {r['frac']}: N {r['N']} f/G {f0[i]/(eta[i]*G[i]):.2f} swing p-p/2 {amp:.4f} rad, (1+j)*amp {(1+j[i])*amp:.3f} vs f/eta {f0[i]/eta[i]:.3f}; "
          f"time with |w|<1% max: {stuck*100:.1f} %; load {Pl[i]*1e3:.3f} mW; EMF peak {emf*1e3:.0f} mV, load V peak {Vpk*1e3:.0f} mV, R_L {RL:.2f}; motor peak rpm {Nn[i]*wmax*Om[i]*60/2/math.pi:.0f}")
json.dump(out, open(os.path.join(D, 'L4_stick.json'), 'w'), indent=1)
