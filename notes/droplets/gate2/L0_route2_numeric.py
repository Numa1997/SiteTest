"""Gate 2, level L0 (chapter 1), route 2 (numerical, SciPy/NumPy): no symbolic algebra is used here."""
import numpy as np
from scipy.integrate import solve_ivp, quad
rng = np.random.default_rng(12345)
k, rho, E = 1.2296e8, 1000.0, 1.0
W = 300e6 * 4 / 3 * np.pi * (8e-6)**3 * rho            # kg/m3, from 300 droplets of 8 um per cm3
r = 8e-6; R0 = 40e-6
print('W = %.6g kg/m3' % W)

print('== (1.1) Monte Carlo of the swept tube (no formula used for the count)')
R = 40e-6; vR, vr = k * R**2, k * r**2
dv = vR - vr
n = W / (4 / 3 * np.pi * rho * r**3)                   # droplets per m3
# a thin box (side 2(R+r)*1.5 in x,y ; length dv*T in z) with Poisson(n V) uniformly placed droplet centres;
# collector sits at x=y=0 and the droplets stream past at relative speed dv: count centres closer than R+r at the moment they cross z=0
T = 500.0                                              # s, gives ~200 hits per trial (box length dv*T ~ 95 m)
side = 3 * (R + r); L = dv * T
Vbox = side * side * L
trials = 400
Mdot_mc = []
for _ in range(trials):
    N = rng.poisson(n * Vbox)
    x = rng.uniform(-side / 2, side / 2, N); y = rng.uniform(-side / 2, side / 2, N)
    hits = np.sum(x**2 + y**2 <= (R + r)**2)           # every droplet of the box passes the plane z=0 within T
    Mdot_mc.append(hits * (4 / 3 * np.pi * rho * r**3) / T)
Mdot_mc = np.array(Mdot_mc)
Mdot_formula = E * np.pi * (R + r)**2 * dv * W
print('  dM/dt MC mean = %.5e +- %.1e kg/s ; formula (1.1) = %.5e kg/s ; ratio %.4f' % (Mdot_mc.mean(), Mdot_mc.std() / np.sqrt(trials), Mdot_formula, Mdot_mc.mean() / Mdot_formula))

print('== (1.2): dR/dt from (1.1) by finite difference vs printed (1.2) at several R')
for R in [20e-6, 40e-6, 100e-6, 300e-6]:
    Mdot = lambda RR: E * np.pi * (RR + r)**2 * (k * RR**2 - k * r**2) * W
    M = lambda RR: 4 / 3 * np.pi * rho * RR**3
    h = 1e-9 * R
    dMdR = (M(R + h) - M(R - h)) / (2 * h)
    lhs = Mdot(R) / dMdR
    rhs = E * k * W / (4 * rho) * (R + r)**3 * (R - r) / R**2
    print('  R = %5.0f um : dR/dt (1.1)/(dM/dR) = %.8e ; (1.2) = %.8e ; rel diff %.1e' % (R * 1e6, lhs, rhs, abs(lhs / rhs - 1)))

print('== (1.3) vs numerical integration of the r<<R equation, and of (1.2) with r -> tiny')
c = E * k * W / (4 * rho)
tstar = 1 / (c * R0)
for rr in [r, 1e-12]:
    f = lambda t, y: E * k * W / (4 * rho) * (y + rr)**3 * (y - rr) / y**2
    ev = lambda t, y: y[0] - 1e-2; ev.terminal = True
    sol = solve_ivp(f, [0, 0.99 * tstar], [R0], rtol=1e-12, atol=1e-16, dense_output=True)
    for frac in [0.2, 0.5, 0.9]:
        t = frac * tstar
        num = sol.sol(t)[0]; closed = R0 / (1 - c * R0 * t)
        print('  r = %.0e : t = %.2f t*  R_num = %.6e  R(1.3) = %.6e  rel diff %.1e' % (rr, frac, num, closed, abs(num / closed - 1)))

print('== (1.4) vs numerical integration of (1.2) with finite r = 8 um')
f = lambda t, y: E * k * W / (4 * rho) * (y + r)**3 * (y - r) / y**2
hit = lambda t, y: y[0] - 100e-6; hit.terminal = True
sol = solve_ivp(f, [0, 3600], [R0], rtol=1e-12, atol=1e-16, events=hit)
t_num = sol.t_events[0][0]
F = lambda RR: np.log((RR - r) / (RR + r)) / (8 * r) - (3 * RR + 2 * r) / (4 * (RR + r)**2)
t_14 = 4 * rho / (E * k * W) * (F(100e-6) - F(R0))
t_quad = quad(lambda RR: 4 * rho / (E * k * W) * RR**2 / ((RR + r)**3 * (RR - r)), R0, 100e-6, epsabs=0, epsrel=1e-13)[0]
print('  t(40->100 um): ODE %.6f s ; (1.4) %.6f s ; quadrature of dt/dR %.6f s ; (1.4) in min %.4f' % (t_num, t_14, t_quad, t_14 / 60))
# the runaway: integrate until R = 10 m, compare with 4 rho/(EkW) * (-F(R0))
hit2 = lambda t, y: y[0] - 1.0; hit2.terminal = True
sol2 = solve_ivp(f, [0, 3600], [R0], rtol=1e-12, atol=1e-18, events=hit2)
print('  blow-up (R -> 1 m by ODE) %.4f min ; (1.4) with F(oo)=0 -> %.4f min ; (1.3) t* %.4f min' % (sol2.t_events[0][0] / 60, 4 * rho / (E * k * W) * (0 - F(R0)) / 60, tstar / 60))
print('  F(R) -> -1/R as r -> 0 : F(1e-4, r=1e-12) = %.6e vs -1/R = %.6e' % (F.__call__(1e-4) if False else (np.log((1e-4 - 1e-12) / (1e-4 + 1e-12)) / (8e-12) - (3e-4 + 2e-12) / (4 * (1e-4 + 1e-12)**2)), -1 / 1e-4))
