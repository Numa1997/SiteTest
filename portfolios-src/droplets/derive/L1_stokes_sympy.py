"""Stokes drag on a sphere from the stream function: E^4 psi = 0, no slip, pressure and shear on the surface, the force."""
import sympy as sp
r, th, a, U, mu = sp.symbols('r theta a U mu', positive=True)
psi = sp.Rational(1,2)*U*sp.sin(th)**2*(r**2 - sp.Rational(3,2)*a*r + a**3/(2*r))
E2 = lambda f: sp.diff(f, r, 2) + sp.sin(th)/r**2*sp.diff(sp.diff(f, th)/sp.sin(th), th)
print("E^4 psi =", sp.simplify(E2(E2(psi))))
ur = sp.diff(psi, th)/(r**2*sp.sin(th)); ut = -sp.diff(psi, r)/(r*sp.sin(th))
print("no slip at r=a:", sp.simplify(ur.subs(r, a)), sp.simplify(ut.subs(r, a)), "; far field u_r ->", sp.limit(ur, r, sp.oo))
# pressure from the r-component of the creeping-flow momentum equation in terms of psi: dp/dr = mu/(r^2 sin th) d(E^2 psi)/d th
dpdr = mu/(r**2*sp.sin(th))*sp.diff(E2(psi), th)
p = sp.integrate(dpdr, (r, sp.oo, r))   # p - p_inf
print("p - p_inf =", sp.simplify(p))
# shear stress tau_r_theta = mu (r d/dr(u_t/r) + (1/r) d u_r/d th) at r = a
tau = mu*(r*sp.diff(ut/r, r) + sp.diff(ur, th)/r)
taua = sp.simplify(tau.subs(r, a)); pa = sp.simplify(p.subs(r, a))
print("tau_r_theta(a) =", taua, "; normal viscous stress at a:", sp.simplify((2*mu*sp.diff(ur, r)).subs(r, a)))
# force along +z (flow direction): -p cos th + tau sin(th)... with outward normal e_r: f_z = (-p) cos th - tau_rth sin th ... sign: tau acts along e_theta, e_theta_z = -sin th
Fp = sp.integrate((-pa)*sp.cos(th)*2*sp.pi*a**2*sp.sin(th), (th, 0, sp.pi))
Fs = sp.integrate((taua)*(-sp.sin(th))*2*sp.pi*a**2*sp.sin(th), (th, 0, sp.pi))
print("pressure drag", sp.simplify(Fp), " shear drag", sp.simplify(Fs), " total", sp.simplify(Fp+Fs))
