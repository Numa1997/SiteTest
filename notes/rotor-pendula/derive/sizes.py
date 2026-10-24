"""Sizes of the second blade: what the model gives over the range of real tip devices.

Range (sources in README.md): length 0.5 to 3 m (retrofit tip extensions are 1, 2 or 3 m; pivoting tip brakes 5-20 % of the
radius on small stall turbines); mass per length 1, 3, 10, 30 kg/m (a light hollow sensor blade; light composite; the NREL
5-MW blade's own tip, 10.3 kg/m at 61.5 m; the same blade about 1 m inboard, 42-49 kg/m, rounded down).
For each size: P* (2.5) at 6, 8, 10 m/s (the full equation is within 0.3 % of it at 1 kg on 1 m); the swing Theta* at 6 m/s
(small-swing (2.2), which depends on the wind only, not on the size); the brake constant c* and the generator torque
tau* = (m l/2) g/sqrt 2 it must hold; the extra centrifugal pull on the mother blade's tip at 10 m/s, m Omega^2 (r_p + l/2);
and what the catalogue maxon RE 25 + GP 32 C delivers to its load (formula (7.6)-(7.7), L4_generator.best_for, within the
gearhead's continuous torque and a swing of 0.5 rad), or that it cannot.
Run: python3 -I sizes.py   (seconds; writes sizes.json)
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
import L4_generator as Gm

g, rp = S.G0, S.R_ROT
NEED = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensor.json')))['need_uW']*1e-6
out = []
for l in (0.5, 1.0, 2.0, 3.0):
    for lam in (1.0, 3.0, 10.0, 30.0):
        m = lam*l; I, mlc = m*l*l/3, m*l/2
        row = dict(l=l, kg_per_m=lam, m=m, R=mlc*rp/I)
        row['Pstar_W'] = [mlc**2*g**2/(4*Om*(mlc*rp - I)) for v, Om, _ in S.mountings()]
        Om6 = S.omega(6.0); G6 = mlc*g/(I*Om6**2); row['Theta6'] = G6/(math.sqrt(2)*(row['R'] - 1))
        Om8 = S.omega(8.0); row['cstar8'] = (mlc*rp - I)*Om8
        row['tau_star'] = mlc*g/math.sqrt(2)
        Om10 = S.omega(10.0); row['pull10_N'] = m*Om10**2*(rp + l/2)
        Gm.m, Gm.L = m, l
        try:
            best = [Gm.best_for(Om, r_)[0] for v, Om, r_ in S.mountings()]
            row['gen_load_W'] = [b['P_load'] if b and b.get('within_rating', True) else None for b in best]
            row['gen_N'] = [b['N'] if b else None for b in best]
        except Exception as e:
            row['gen_load_W'] = None; row['gen_err'] = str(e)[:80]
        out.append(row)
Gm.m, Gm.L = S.M_B, S.L_B
# the mother blade itself near its tip (OpenFAST blade file, as in nrel5mw.py): mass per length, and the outer 3 m's mass and pull
import numpy as np
L_ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'NRELOffshrBsline5MW_Blade.dat')).read().splitlines()
i0 = [k for k, t in enumerate(L_) if 'BlFract' in t][0] + 2
a = np.array([[float(x) for x in L_[k].split()[:3]] for k in range(i0, i0 + 49)])
span = rp - S.R_HUB; s_ = a[:, 0]*span; mu = a[:, 2]; sel = s_ >= span - 3.0 - 1e-9
trap = lambda y, x: float(np.sum((y[1:] + y[:-1])/2*np.diff(x)))
mother = dict(tip_kg_per_m=float(mu[-1]), outer3_kg=trap(mu[sel], s_[sel]),
              outer3_pull10_N=trap(mu[sel]*S.omega(10.0)**2*(S.R_HUB + s_[sel]), s_[sel]))
print(f"mother blade: {mother['tip_kg_per_m']:.1f} kg/m at the tip; outer 3 m {mother['outer3_kg']:.0f} kg, pulling "
      f"{mother['outer3_pull10_N']/1e3:.1f} kN at 10 m/s")
print(f"{'l (m)':>5} {'kg/m':>5} {'m (kg)':>6} {'P* 6/8/10 m/s (W)':>22} {'Theta6':>6} {'c*8 (N m s)':>11} {'tau* (N m)':>10} "
      f"{'pull10 (kN)':>11}  RE 25 + GP 32 C to load (mW), ratio")
for r in out:
    P = '/'.join(f'{p:.3g}' for p in r['Pstar_W'])
    gl = r.get('gen_load_W')
    gen = ('/'.join('—' if x is None else f'{x*1e3:.3g}' for x in gl) + f"  N {r['gen_N'][1]}") if gl else 'cannot: ' + r.get('gen_err', '')
    print(f"{r['l']:5.1f} {r['kg_per_m']:5.0f} {r['m']:6.1f} {P:>22} {r['Theta6']:6.3f} {r['cstar8']:11.1f} {r['tau_star']:10.2f} "
          f"{r['pull10_N']/1e3:11.2f}  {gen}")
json.dump(dict(rows=out, need_W=NEED, mother=mother), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sizes.json'), 'w'), indent=1)
