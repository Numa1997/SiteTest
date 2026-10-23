"""L3 derivation: pendulum on a blade that bends edgewise.  The pivot is displaced along the blade's tangent by u(t) and the
blade section (which carries the generator's stator) is rotated by beta(t); the rotor turns at phi = Omega t.
Run: python3 -I L3_sag.py   (prints the linearised equation and its forcing terms; PASS/FAIL)

Rod absolute angle phi + theta (theta from the undeformed blade's outward direction); generator torque -c (thetadot - betadot).
Linearised in theta, u, beta, the equation must reduce to L0 (2.1) when u = beta = 0.
Quasi-static 1P sag: u = -w cos(phi) (the blade sags along gravity's tangential component), beta = -w' cos(phi),
with w the sag amplitude at the pivot and w' its slope along the blade.
"""
import sys
import sympy as sp
fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
t = sp.symbols('t', real=True)
m, L, rp, g, W, c = sp.symbols('m L r_p g Omega c', positive=True)
th = sp.Function('theta')(t); u = sp.Function('u')(t); be = sp.Function('beta')(t)
phi = W*t
er = sp.Matrix([sp.cos(phi), sp.sin(phi)]); et = sp.Matrix([-sp.sin(phi), sp.cos(phi)])
pos = rp*er + u*et + L*sp.Matrix([sp.cos(phi + th), sp.sin(phi + th)])
v = pos.diff(t)
T = m/2*v.dot(v); V = m*g*pos[1]
Lg = T - V
F = c/2*(th.diff(t) - be.diff(t))**2
EL = sp.diff(Lg.diff(th.diff(t)), t) - Lg.diff(th) + F.diff(th.diff(t))
# linearise in theta, u, beta (all small) -- keep first order in each
eps = sp.symbols('epsilon')
lin = EL.subs({th: eps*th, u: eps*u, be: eps*be}).doit()
lin = sp.series(lin, eps, 0, 2).removeO().subs(eps, 1)
lin = sp.expand(sp.simplify(lin/(m*L**2)))
print('linearised equation / (m L^2) = 0 with')
print('  ', sp.collect(lin, [th.diff(t, 2), th.diff(t), th, u.diff(t, 2), u, be.diff(t)]))
# check against L0 when u = beta = 0: theta'' + c/(mL^2) theta' + (r_p/L) Omega^2 theta - (g/L) theta sin(phi) = -(g/L) cos(phi)
l0 = th.diff(t, 2) + c/(m*L**2)*th.diff(t) + rp/L*W**2*th - g/L*th*sp.sin(phi) + g/L*sp.cos(phi)
check('u = beta = 0 gives L0 (2.1) with its parametric term', sp.simplify(lin.subs({u: 0, be: 0}).doit() - l0) == 0)
# the pivot terms: coefficient of u and u''
cu = sp.simplify(lin.coeff(u.diff(t, 2))); cu0 = sp.simplify((lin - lin.coeff(u.diff(t, 2))*u.diff(t, 2)).subs({th: 0, be: 0}).doit().coeff(u))
print('   coefficient of u\'\':', cu, '  coefficient of u:', cu0)
# quasi-static sag at 1P: u = -w cos(phi), beta = -wp cos(phi)
w, wp = sp.symbols('w wp', real=True)
forcing = sp.simplify((lin.subs({th: 0}).doit()).subs({u: -w*sp.cos(phi), be: -wp*sp.cos(phi)}).doit())
print('   total forcing (theta = 0):', sp.simplify(sp.expand_trig(forcing)))
target = (g/L + 2*W**2*w/L)*sp.cos(phi) + c/(m*L**2)*(-wp*W*sp.sin(phi))
check('forcing = (g + 2 Omega^2 w)/L cos(phi) + (c/mL^2) * d(beta)/dt-term: sag adds 2 Omega^2 w to g, section rotation drives through the generator',
      sp.simplify(sp.expand_trig(forcing - target)) == 0)
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
