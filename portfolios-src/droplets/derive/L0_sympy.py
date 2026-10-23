"""L0: one collector, continuous collection, Stokes speed, E = 1. SymPy derivations (route 1)."""
import sympy as sp
R, r, t, k, W, rho, E, R0, c, Rm, Nc = sp.symbols('R r t k W rho_w E R_0 c R_m N_c', positive=True)
M = sp.Rational(4,3)*sp.pi*rho*R**3
# continuous collection: dM/dt = E pi (R+r)^2 (v(R)-v(r)) W, Stokes v = k R^2
rhs = E*sp.pi*(R+r)**2*k*(R**2-r**2)*W
dRdt = sp.simplify(rhs/sp.diff(M,R))
print("dR/dt exact      =", sp.factor(dRdt))
print("dR/dt, r -> 0    =", sp.simplify(dRdt.subs(r,0)))
# r -> 0: dR/dt = c R^2, c = E k W/(4 rho)
Rt = sp.Function('R')
sol = sp.dsolve(sp.Eq(Rt(t).diff(t), c*Rt(t)**2), Rt(t), ics={Rt(0): R0})
print("R(t), r -> 0     =", sp.simplify(sol.rhs), "  blow-up t* =", sp.solve(sp.denom(sp.together(sol.rhs)), t))
# finite r: t = (4 rho/(E k W)) * int_{R0}^{R} R^2/((R+r)^3 (R-r)) dR
f = R**2/((R+r)**3*(R-r))
print("partial fractions:", sp.apart(f, R))
F = sp.integrate(sp.apart(f,R), R)
print("antiderivative   :", sp.simplify(F))
print("check d/dR       :", sp.simplify(sp.diff(F,R)-f))
# depletion, r << R: closed box, Nc identical collectors, W(R) = W0 - Nc*(4pi/3)rho (R^3 - R0^3) = Nc (4pi/3) rho (Rm^3 - R^3)
# dR/dt = (E k/(4 rho)) R^2 W(R) = (E k Nc pi/3) R^2 (Rm^3 - R^3)
g = 1/(R**2*(Rm**3-R**3))
G = sp.integrate(sp.apart(g, R), R)
print("depletion antiderivative of 1/(R^2 (Rm^3-R^3)):", sp.simplify(G))
print("check d/dR:", sp.simplify(sp.diff(G,R)-g))

# r -> 0 limit of the finite-r time (L0.4) gives (L0.3)
lim = sp.limit(F.subs(R, sp.Symbol('R1', positive=True)) - F.subs(R, R0), r, 0)
print("limit r->0 of F(R1)-F(R0):", sp.simplify(lim), "  (expected 1/R0 - 1/R1)")
# Closed box with finite r: the integrand R^2/((R+r)^3 (R-r) (Rm^3 - R^3)) is rational, so a closed form exists
# (logarithms and arctangents). SymPy's antiderivative of it failed its own derivative check by 2.8 % on
# 23 October 2026, so the study does not use it: the closed-box finite-r times come from two numerical routes
# (solve_ivp in L0_numbers.py and quad in L0_population.py / the check scripts).
