"""L0 extensions: the tilted hinge and the mean lean, in SymPy and by integration.

Run: python3 -I L0_r2.py   (PASS/FAIL; exit 1 on any FAIL)
1. Tilted hinge: hinge axis turned from the shaft axis towards the blade axis by alpha; the bob swings in the plane normal to it.
   Claimed linear equation (blade-angle time): x'' + (R cos(a) - sin(a)^2 - G cos(a) sin(phi)) x = -G cos(phi)  [+ damping].
2. Mean lean of the straight pendulum at second order: theta_bar = -G^2/(4 R (R-1)) at kappa = R - 1, against integration with
   the pivot at 30 % at the three winds of setup.py (the largest swings).
"""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, sympy as sp
fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name, flush=True)

t = sp.symbols('t', real=True)
m, L, rp, g, W, a = sp.symbols('m L r_p g Omega alpha', positive=True)
x = sp.Function('x')(t)
# rotating frame: e_r (blade axis, outward), e_t (tangential), e_z (shaft). Hinge axis n = cos(a) e_z + sin(a) e_r.
# bob position relative to pivot: L [cos x * u + sin x * v], u = e_r cos... choose u = in-plane unit normal to n: u = -sin(a) e_z + cos(a) e_r,
# v = n x u = e_t ; at x = 0 the rod points along u (outward, tilted out of the rotor plane by a).
phi = W*t
er = sp.Matrix([sp.cos(phi), sp.sin(phi), 0]); et = sp.Matrix([-sp.sin(phi), sp.cos(phi), 0]); ez = sp.Matrix([0, 0, 1])
u = -sp.sin(a)*ez + sp.cos(a)*er
pos = rp*er + L*(sp.cos(x)*u + sp.sin(x)*et)
vel = pos.diff(t)
T = m/2*vel.dot(vel); V = m*g*pos[1]
Lag = T - V
EL = sp.diff(Lag.diff(x.diff(t)), t) - Lag.diff(x)
# blade-angle time: x(t) = X(phi); linearise in X
X, Xp, Xpp, s = sp.symbols('X Xp Xpp s', real=True)
e = EL.subs({x.diff(t, 2): W**2*Xpp, x.diff(t): W*Xp}).subs(x, X).subs(t, s/W)
e = sp.expand(e/(m*L**2*W**2))
lin = sp.series(e, X, 0, 2).removeO()
R, G = rp/L, g/(W**2*L)
claim = Xpp + (R*sp.cos(a) - sp.sin(a)**2 - G*sp.cos(a)*sp.sin(s))*X + G*sp.cos(s)
check('tilted hinge, linear: x\'\' + (R cos a - sin^2 a - G cos a sin phi) x = -G cos phi', sp.simplify(sp.expand_trig(lin - claim)) == 0)
# tuning angle that makes the stiffness 1 (order-1 resonance): R cos a - sin^2 a = 1 -> cos a = (-R + sqrt(R^2 + 8))/2 ... solve
import setup as S
for (Rv, lab) in ((S.FRACS[0]*S.R_ROT/S.L, '30 %'), (S.FRACS[-1]*S.R_ROT/S.L, '90 %')):
    cs = (-Rv + math.sqrt(Rv*Rv + 8))/2   # cos^2 a + R cos a - 2 = 0
    print(f'   stiffness 1 at {lab}: alpha = {math.degrees(math.acos(cs)):.1f} deg; d(stiffness)/d(alpha) = '
          f'{-Rv*math.sin(math.acos(cs)) - math.sin(2*math.acos(cs)):.1f} per rad')
# 2. mean lean by integration (straight pendulum, kappa = R - 1), engine, pivot at 30 % at each wind of setup.py
from engine import Single, pendulum_rhs, integrate
leans = {}
for v in S.WINDS:
    Om = S.omega(v); rpv = S.FRACS[0]*S.R_ROT; gv = S.G0; Rv = rpv/S.L; Gv = gv/(Om**2*S.L)
    ss = Single(S.M, S.L, rpv, S.M*S.L**2*Om*(Rv - 1))
    F = pendulum_rhs(ss, Om=Om); Tt = 2*math.pi/Om
    r = integrate(F, np.zeros((1, 3)), 0, 60*Tt, Tt/200)
    r = integrate(F, r['Y'], 60*Tt, 61*Tt, Tt/200, record_every=1)
    lean = np.mean([y[0, 0] for _, y in r['rec']])
    th = -Gv**2/(4*Rv*(Rv - 1)); sw = Gv/(math.sqrt(2)*(Rv - 1))
    leans[str(int(v))] = dict(run=float(lean), theory=float(th), swing=float(sw))
    print(f'   mean lean at {v:.0f} m/s, 30 % (small-swing amplitude {sw:.2f} rad): integration {lean:.4f} rad, second-order theory {th:.4f} rad '
          f'({(lean/th - 1)*100:+.1f} %)')
gaps = [abs(leans[k]['run']/leans[k]['theory'] - 1) for k in sorted(leans, key=int)]
check('the second-order trail approaches the full model as the swing shrinks (gap falls with wind speed, below 5 % at 10 m/s)',
      gaps[0] > gaps[1] > gaps[2] and gaps[2] < 0.05)
import json as _json
_json.dump(leans, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L0_r2.json'), 'w'), indent=1)
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
