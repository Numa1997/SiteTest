"""Gate 2, level L0 (chapter 1), route 1: SymPy. Equations (1.1)-(1.4). Own derivation from what the text says each follows from."""
import sympy as sp
from dims import *
R, r, k, W, rho, E, t, R0, c, Rm = sp.symbols('R r k W rho_w E t R_0 c R_m', positive=True)
Rf = sp.Function('R')
print('== (1.1) swept tube, from first principles')
# number density of droplets n = W / m_d ; tube cross-section pi (R+r)^2 ; relative speed v(R)-v(r) ; fraction E sticks
vR, vr = sp.symbols('v_R v_r', positive=True)
md = sp.Rational(4, 3) * sp.pi * rho * r**3
n = W / md
dMdt = E * n * sp.pi * (R + r)**2 * (vR - vr) * md        # droplets swept per second times mass of one
print('  derived dM/dt =', sp.simplify(dMdt), ' ; printed: E*pi*(R+r)^2*(vR-vr)*W ->',
      sp.simplify(dMdt - E * sp.pi * (R + r)**2 * (vR - vr) * W) == 0)
same('dM/dt', ONE * m**2 * speed * dens, kg / s)
M = 4 * sp.pi / 3 * rho * R**3
print('  M = 4pi/3 rho R^3 ; dM/dR =', sp.diff(M, R), '(= 4 pi rho R^2 : used by the text)')
print('  limit W->0 : dM/dt ->', sp.limit(dMdt.subs(W, 0), R, 1), '; sign: positive for vR>vr (R>r), zero at R=r under Stokes')

print('\n== (1.2) insert Stokes v(a)=k a^2 and dM/dt = 4 pi rho R^2 dR/dt')
rhs = E * sp.pi * (R + r)**2 * (k * R**2 - k * r**2) * W / (4 * sp.pi * rho * R**2)
printed12 = E * k * W / (4 * rho) * (R + r)**3 * (R - r) / R**2
print('  difference derived - printed =', sp.simplify(rhs - printed12))
# k = 2 (rho_w - rho_a) g /(9 mu): kg/m3 * m/s2 / (kg/(m s)) = 1/(m s)
kd = dens * accel / visc
same('k = 2 drho g /(9 mu)  [expected 1/(m s)]', kd, D(0, -1, -1))
same('dR/dt = E k W/rho (R+r)^3 (R-r)/R^2 /4', kd * (dens / dens) * m**3 * m / m**2, speed)
print('  limit r<<R : lim_{r->0} dR/dt / R^2 =', sp.limit(printed12 / R**2, r, 0), ' (= E k W/(4 rho) = c)')

print('\n== (1.3) separable ODE dR/dt = c R^2')
sol = sp.dsolve(sp.Eq(Rf(t).diff(t), c * Rf(t)**2), Rf(t), ics={Rf(0): R0})
print('  dsolve:', sol)
R13 = R0 / (1 - c * R0 * t)
print('  printed form satisfies ODE:', sp.simplify(R13.diff(t) - c * R13**2) == 0, '; R(0)=R0:', R13.subs(t, 0) == R0)
print('  blow-up time (denominator zero):', sp.solve(1 - c * R0 * t, t), ' printed t* = 1/(c R0)')
same('c R0 t', kd * m * s, ONE)
print('  limit W->0 (c->0): R(t) ->', sp.limit(R13, c, 0))
print('  t = t*(1 - R0/R):', sp.simplify(sp.solve(sp.Eq(R, R13), t)[0] - (1 / (c * R0)) * (1 - R0 / R)) == 0)
print('  40->60 um fraction of t*:', sp.Rational(1) - sp.Rational(40, 60), ' ; 40->100:', 1 - sp.Rational(40, 100))
print('  powers of R: area R^2 * speed R^2 / (mass per dR ~ R^2) -> R^2')

print('\n== (1.4) partial fractions: F\'(R) must equal R^2/((R+r)^3 (R-r))')
F = sp.log((R - r) / (R + r)) / (8 * r) - (3 * R + 2 * r) / (4 * (R + r)**2)
integrand = R**2 / ((R + r)**3 * (R - r))      # dt/dR = (4 rho / E k W) * integrand   from (1.2)
print('  dF/dR - integrand =', sp.simplify(sp.diff(F, R) - integrand))
print('  independent: apart(integrand) =', sp.apart(integrand, R))
print('  sympy integrate gives:', sp.simplify(sp.integrate(integrand, R)))
print('  limit r->0 of F:', sp.limit(F, r, 0), ' (expected -1/R)')
print('  limit R->oo of F:', sp.limit(F, R, sp.oo), ' (so blow-up time = -F(R0)*4rho/(EkW))')
tR = 4 * rho / (E * k * W) * (F - F.subs(R, R0))
print('  r->0 : t(R) =', sp.simplify(sp.limit(tR, r, 0)), ' ; compare (1.3) t = 4rho/(EkW)*(1/R0-1/R)')
print('  sign: dF/dR = R^2/((R+r)^3 (R-r)) > 0 for R>r>0, so t increases with R')
print('\n== numbers quoted in the text, from the printed formulas only (k as printed 1.2296e8)')
kv, Wv, rhov, rv = 1.2296e8, 0.643e-3, 1000.0, 8e-6
Fn = sp.lambdify((R, r), F, 'mpmath')
import mpmath as mp
mp.mp.dps = 30
def tt(R1, R0_): return 4 * rhov / (kv * Wv) * (Fn(R1, rv) - Fn(R0_, rv))
cv = kv * Wv / (4 * rhov)
print('  t(40->100) by (1.4) = %.4f min (text 9.96)' % (tt(100e-6, 40e-6) / 60))
print('  t(40->100) by (1.3) = %.4f min (text 12.64)' % ((1 / (cv * 40e-6)) * (1 - 0.4) / 60))
print('  t* = %.4f min (text 21.1)' % (1 / (cv * 40e-6) / 60))
print('  blow-up with finite r : %.3f min' % (4 * rhov / (kv * Wv) * (0 - Fn(40e-6, rv)) / 60))
print('  Rm = (R0^3 + 300 r^3)^(1/3) = %.3f um (text 60.15)' % (((40.0**3 + 300 * 8.0**3)) ** (1 / 3)))
print('  W = 300e6 * 4/3 pi (8e-6)^3 * 1000 = %.4f g/m3 (text 0.643)' % (300e6 * 4 / 3 * 3.141592653589793 * (8e-6)**3 * 1000 * 1e3))
