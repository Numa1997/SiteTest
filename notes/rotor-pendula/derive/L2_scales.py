"""L2 scales, before any pendulum run: the rotor-effective wind and the rotor's response over IEC class A records at 8 m/s.

Run: python3 -I L2_scales.py   (prints numbers; PASS/FAIL on the synthesis checks; exit 1 on any FAIL)
"""
import math, sys
import numpy as np
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turbulence as W

fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
V = 8.0; sig = W.iec_sigma(V)
print(f'IEC class A (I_ref 0.16) at V = {V} m/s: sigma_1 = {sig:.3f} m/s, I = {sig/V:.3f}; L_u = {W.L_U:.1f} m; '
      f'integral time L_u/V = {W.L_U/V:.1f} s')
f0 = 1/600
frac = (1 + 6*f0*W.L_U/V)**(-2/3)
print(f'fraction of the Kaimal variance above 1/600 Hz: {frac:.3f} (so an unscaled 10-min record has sigma = {sig*math.sqrt(frac):.3f} m/s)')
# disc-pair distribution check: integrates to 1, mean distance 128 R/(45 pi)
R = 63.0; r = (np.arange(20000) + 0.5)*(2*R/20000); p = W.disc_pair_pdf(r, R)*(2*R/20000)
check(f'disk line picking pdf integrates to 1 ({p.sum():.6f}) and has mean 128R/(45 pi) = {128*R/(45*math.pi):.3f} m ({(p*r).sum():.3f})',
      abs(p.sum() - 1) < 1e-4 and abs((p*r).sum()/(128*R/(45*math.pi)) - 1) < 1e-4)
rng = np.random.default_rng(1)
NP = 2000000
pts = np.sqrt(rng.random((2, NP)))*R; ang = rng.random((2, NP))*2*math.pi
xy = np.stack([pts*np.cos(ang), pts*np.sin(ang)], -1)
dd = np.linalg.norm(xy[0] - xy[1], axis=-1)
for f in (0.0, 0.01, 0.05):
    mc = np.mean(np.exp(-12*np.sqrt((f*dd/V)**2 + (0.12*dd/W.L_C)**2)))
    print(f'   chi({f} Hz) = {W.chi(f, V)[0]:.4f} (Monte Carlo over random pairs: {mc:.4f})')
ok = True
for f in (0.0, 0.01, 0.05):
    e = np.exp(-12*np.sqrt((f*dd/V)**2 + (0.12*dd/W.L_C)**2)); se = e.std()/math.sqrt(NP)
    ok &= abs(W.chi(f, V)[0] - e.mean()) < 3*se
check('chi(f) from the pair pdf = Monte Carlo over 2 million random point pairs within 3 standard errors (3 frequencies)', ok)
# records
N = 200
Vh = W.synth(V, sig, nrec=N, seed=7, rotor_eff=False)
Ve = W.synth(V, sig, nrec=N, seed=7, rotor_eff=True)
sh = Vh.std(axis=1); se = Ve.std(axis=1)
print(f'{N} records: hub-point sigma {sh.mean():.3f} +- {sh.std():.3f} m/s (target {sig:.3f}); rotor-effective sigma '
      f'{se.mean():.3f} +- {se.std():.3f} m/s; record means exactly {Vh.mean(axis=1).min():.6f}..{Vh.mean(axis=1).max():.6f}')
check(f'hub-point record variance averages sigma_1^2 (ratio {np.mean(sh**2)/sig**2:.4f}, 200 records, within 3 %)',
      abs(np.mean(sh**2)/sig**2 - 1) < 0.03)
# rotor response: two passes of each periodic record, second measured
ts, Om, Od = W.rotor_only(Ve, 0.1, 0.9494, 1200.0)
Om2 = Om[:, ts >= 600]; Od2 = Od[:, ts >= 600]
s = Om2.std(axis=1)/Om2.mean(axis=1)
eps = Od2/Om2**2
print(f'rotor over the measured 10 min: mean Omega {Om2.mean():.4f} rad/s ({Om2.mean()*60/2/math.pi:.2f} rpm), '
      f'sigma_Omega/Omega = {s.mean():.3f} +- {s.std():.3f}; range {Om2.min()*60/2/math.pi:.2f} .. {Om2.max()*60/2/math.pi:.2f} rpm')
print(f'eps = Omega_dot/Omega^2: rms {np.sqrt(np.mean(eps**2)):.4f}, max |eps| {np.max(np.abs(eps)):.4f}')
print(f'time at rated speed (ideal pitch active): {np.mean(Om2 >= W.OM_RATED - 1e-9)*100:.2f} %; below region 2 (9.0 rpm): '
      f'{np.mean(Om2 < 871/97*2*math.pi/60)*100:.1f} %')
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
