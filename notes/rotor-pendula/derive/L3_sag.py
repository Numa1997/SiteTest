"""L3 derivation: the second blade on a mother blade that bends edgewise.  The hinge is displaced along the blade's tangent by
u(t) and the blade section at the tip (which carries the generator's stator) is turned by beta(t); the rotor turns at phi = Omega t.
Run: python3 -I L3_sag.py   (prints the linearised equation and its forcing terms; PASS/FAIL)

The second blade: a rod of mass m, length l, I = m l^2/3, first moment m l/2; absolute angle phi + theta (theta from the
undeformed blade's outward direction); generator torque -c (thetadot - betadot).
Linearised in theta, u, beta, the equation must reduce to the small-swing equation of chapter 2 when u = beta = 0.
Quasi-static 1P sag: u = -w cos(phi) (the blade sags along gravity's tangential component), beta = -w' cos(phi), with w the
sag at the hinge and w' the slope of the bent blade there.
"""
import sys
import sympy as sp
fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
t, s = sp.symbols('t s', real=True)
m, l, rp, g, W, c = sp.symbols('m l r_p g Omega c', positive=True)
I, mlc = m*l**2/3, m*l/2
th = sp.Function('theta')(t); u = sp.Function('u')(t); be = sp.Function('beta')(t)
phi = W*t
er = sp.Matrix([sp.cos(phi), sp.sin(phi)]); et = sp.Matrix([-sp.sin(phi), sp.cos(phi)])
pos = rp*er + u*et + s*sp.Matrix([sp.cos(phi + th), sp.sin(phi + th)])
v = pos.diff(t)
T = sp.integrate((m/l)*v.dot(v)/2, (s, 0, l)); V = sp.integrate((m/l)*g*pos[1], (s, 0, l))
Lg = T - V
F = c/2*(th.diff(t) - be.diff(t))**2
EL = sp.diff(Lg.diff(th.diff(t)), t) - Lg.diff(th) + F.diff(th.diff(t))
eps = sp.symbols('epsilon')
lin = EL.subs({th: eps*th, u: eps*u, be: eps*be}).doit()
lin = sp.series(lin, eps, 0, 2).removeO().subs(eps, 1)
lin = sp.expand(sp.simplify(lin/I))
print('linearised equation / I = 0 with')
print('  ', sp.collect(lin, [th.diff(t, 2), th.diff(t), th, u.diff(t, 2), u, be.diff(t)]))
R = mlc*rp/I; Gt = mlc*g/I                                            # R and G Omega^2 (time form)
l0 = th.diff(t, 2) + c/I*th.diff(t) + R*W**2*th - Gt*th*sp.sin(phi) + Gt*sp.cos(phi)
check('u = beta = 0 gives the small-swing equation of chapter 2 with its parametric term', sp.simplify(lin.subs({u: 0, be: 0}).doit() - l0) == 0)
w, wp = sp.symbols('w wp', real=True)
forcing = sp.simplify((lin.subs({th: 0}).doit()).subs({u: -w*sp.cos(phi), be: -wp*sp.cos(phi)}).doit())
print('   total forcing (theta = 0):', sp.simplify(sp.expand_trig(forcing)))
target = (mlc/I)*(g + 2*W**2*w)*sp.cos(phi) + c/I*(-wp*W*sp.sin(phi))
check('forcing = (m l/2)(g + 2 Omega^2 w)/I cos(phi) + (c/I) beta-term: the sag adds 2 Omega^2 w to g (as for the point pendulum), '
      'the section\'s turn drives through the generator', sp.simplify(sp.expand_trig(forcing - target)) == 0)
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
