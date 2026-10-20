# Fig. 9: SymPy checks of every step the note shows (sections 3, 4, 5, 7). Run: python3 notes/fig09/derive.py
import sympy as sp
t, w0, W, z, F, m = sp.symbols('t omega0 Omega zeta F0 m', positive=True)
s, u = sp.symbols('s u')
# 3.1 the denominator D = w0^2 - W^2 + 2 i z w0 W, Z = (F/m)/D; |Z| and the phase lag phi = arg D
D = w0**2 - W**2 + 2*sp.I*z*w0*W
Z = (F/m)/D
print('|Z|^2 == (F/m)^2/|D|^2:', sp.simplify(sp.Abs(Z)**2 - (F/m)**2/((w0**2-W**2)**2 + (2*z*w0*W)**2)) == 0)
# arg Z = -arg D checked numerically in arg_check below (SymPy cannot simplify arg symbolically)
# the steady solution x_p = X cos(W t - phi) solves (2)
X = (F/m)/sp.sqrt((w0**2-W**2)**2 + (2*z*w0*W)**2)
phi = sp.atan2(2*z*w0*W, w0**2 - W**2)
xp = X*sp.cos(W*t - phi)
res = sp.diff(xp, t, 2) + 2*z*w0*sp.diff(xp, t) + w0**2*xp - (F/m)*sp.cos(W*t)
print('x_p solves (2):', sp.simplify(sp.expand_trig(res.rewrite(sp.cos))) == 0 or abs(sp.N(res.subs({w0: 3.1, W: 2.8, z: 0.05, F: 1, m: 1, t: 1.234}))) < 1e-12)
# 3.2 characteristic equation and roots
roots = sp.solve(s**2 + 2*z*w0*s + w0**2, s)
print('roots:', roots)
# C1, C2 from x(0) = 0, x'(0) = 0
C1, C2 = sp.symbols('C1 C2'); ph, A = sp.symbols('varphi X', positive=True)
wd = w0*sp.sqrt(1 - z**2)
x = A*sp.cos(W*t - ph) + sp.exp(-z*w0*t)*(C1*sp.cos(wd*t) + C2*sp.sin(wd*t))
cond0 = sp.simplify(x.subs(t, 0)); cond1 = sp.simplify(sp.diff(x, t).subs(t, 0))
print('x(0)  =', cond0); print("x'(0) =", sp.expand(cond1))
sol = sp.solve([cond0, cond1], [C1, C2])
print('C1 =', sol[C1], ' C2 - note form =', sp.simplify(sol[C2] - (z*w0*sol[C1] - A*W*sp.sin(ph))/wd))
# 4 completing the square in u = W^2
lhs = (w0**2 - u)**2 + 4*z**2*w0**2*u
rhs = (u - w0**2*(1 - 2*z**2))**2 + 4*z**2*(1 - z**2)*w0**4
print('(6a) identity:', sp.expand(lhs - rhs) == 0)
print('X at W = w0 equals F/(2 z k):', sp.simplify(X.subs(W, w0) - F/(2*z*m*w0**2)) == 0)
# 5 poles of G(s) = 1/(m s^2 + c s + k) with c = 2 z m w0, k = m w0^2
print('poles:', sp.solve(m*s**2 + 2*z*m*w0*s + m*w0**2, s))
# 7 mean power: <c v^2> over a period = c W^2 X^2 / 2
c = 2*z*m*w0
v = sp.diff(xp, t)
Pm = sp.simplify(sp.integrate((c*v**2).subs({}), (t, 0, 2*sp.pi/W)) * W/(2*sp.pi))
print('<P_loss> - c W^2 X^2/2 =', sp.simplify(Pm - c*W**2*X**2/2))
Pin = sp.integrate(F*sp.cos(W*t)*v, (t, 0, 2*sp.pi/W)) * W/(2*sp.pi)
print('<P_in> - <P_loss> (numeric) =', sp.N((Pin - c*W**2*X**2/2).subs({w0: sp.pi, W: 0.9*sp.pi, z: 0.05, F: 1, m: 1})))
# numbers for the defaults
vals = {w0: sp.pi, z: sp.Rational(1, 20)}
print('f_r =', sp.N(0.5*sp.sqrt(1 - 2*sp.Rational(1, 400))), 'Hz;  peak height X_max/(F0/k) =', sp.N(1/(2*sp.Rational(1, 20)*sp.sqrt(1 - sp.Rational(1, 400)))))
print('root at defaults:', [sp.N(r.subs(vals)) for r in roots], ' 1/tau =', sp.N(sp.Rational(1, 20)*sp.pi))
# arg check, numerically over random parameters
import cmath, math, random
random.seed(9); worst = 0
for _ in range(2000):
    a = random.uniform(0.5, 10); b = random.uniform(0.05, 12); q = random.uniform(0.01, 0.9)
    Dn = complex(a*a - b*b, 2*q*a*b); p = math.atan2(2*q*a*b, a*a - b*b)
    worst = max(worst, abs(cmath.phase(1/Dn) + p), abs(cmath.phase(Dn) - p)); assert 0 < p < math.pi
print('arg_check: arg D = phi = -arg Z, worst', worst, '; phi in (0, pi) always')
