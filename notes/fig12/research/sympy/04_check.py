"""Check of Wolfram 04 (log-normal Sauter diameter, Stokes settling, LLD film, meniscus height). Run: python3 04_check.py"""
import math
s = math.log(82/47)/(2*math.sqrt(2*math.log(2))); m = 61*math.exp(-s**2/2)
print('sigma = %.4f, median = %.2f um, D32 = %.2f um' % (s, m, m*math.exp(2.5*s**2)))
rho, mu, g, gam = 1007, 2.06e-3, 9.81, 0.045
for D in (61e-6, 122e-6):
    U = rho*g*D**2/(18*mu); print('D = %.0f um: U = %.3f mm/s, t = %.1f s' % (D*1e6, U*1e3, 0.125/U))
lc = math.sqrt(gam/(rho*g)); print('lc = %.4f mm' % (lc*1e3))
for V in (0.001, 0.1):
    Ca = mu*V/gam; h = 0.946*lc*Ca**(2/3); print('V=%.3f: h = %.2f um, rigid %.2f um' % (V, h*1e6, h*4**(2/3)*1e6))
for th in (30, 40):
    print('theta %d: meniscus %.3f mm' % (th, lc*math.sqrt(2*(1-math.sin(math.radians(th))))*1e3))
