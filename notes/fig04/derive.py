# Fig. 4: symbolic checks of the steps added to the note (SymPy). Run: python3 -I notes/fig04/derive.py
import sympy as sp

# 1. Section 4.2: adiabatic bulk modulus. p V^gamma = C, B = -V dp/dV
V, C, g = sp.symbols('V C gamma', positive=True)
p = C / V**g
B = sp.simplify(-V * sp.diff(p, V))
print('B = -V dp/dV =', B, '; B / p =', sp.simplify(B / p))   # gamma * p

# 2. Section 4.2 note: density of dry air from the ideal-gas law, and the speed of sound
P0, T0, Rgas = 101325, 293.15, 8.314462618
for M in (0.02897, 0.028965):
    rho = P0 * M / (Rgas * T0)
    print(f'M = {M*1000:.3f} g/mol -> rho = {rho:.5f} kg/m^3, v = {(1.40*P0/rho)**0.5:.2f} m/s')
print('v with rho = 1.204:', (1.40 * P0 / 1.204) ** 0.5)
print('isothermal (Newton), B = p:', (P0 / 1.2043) ** 0.5)

# 3. Section 4.3: P-wave modulus. Uniaxial strain e along x, no sideways strain, isotropic Hooke's law
e, K, G = sp.symbols('epsilon K G', positive=True)
eps = sp.diag(e, 0, 0)
I3 = sp.eye(3)
tr = eps.trace()
sigma = K * tr * I3 + 2 * G * (eps - tr / 3 * I3)
print('sigma_xx =', sp.factor(sigma[0, 0]), '; volume part K*e, shape part', sp.simplify(sigma[0, 0] - K * e))
print('deviatoric strain diag:', [sp.simplify(x) for x in (eps - tr / 3 * I3).diagonal()])
print('v_P^2 - v_S^2 times rho =', sp.simplify(sigma[0, 0] / e - G))

# 4. Section 6: potential energy of a tilted piece, F times the extra length
s = sp.symbols('s')   # slope dxi/dX
print('sqrt(1+s^2) =', sp.series(sp.sqrt(1 + s**2), s, 0, 4))

# 5. Section 6: the conservation law (14) from the wave equation
X, t, mu, F = sp.symbols('X t mu F', positive=True)
xi = sp.Function('xi')(X, t)
e_den = mu / 2 * sp.diff(xi, t)**2 + F / 2 * sp.diff(xi, X)**2
P = -F * sp.diff(xi, X) * sp.diff(xi, t)
lhs = sp.diff(e_den, t) + sp.diff(P, X)
wave = mu * sp.diff(xi, t, 2) - F * sp.diff(xi, X, 2)
print('de/dt + dP/dX - xi_t*(wave eq) =', sp.simplify(sp.expand(lhs - sp.diff(xi, t) * wave)))

# 6. Section 5: span of the denser half, rest phases pi/2 .. 3pi/2
AL, k = sp.symbols('A_L k', positive=True)
lam = 2 * sp.pi / k
Xr, Xf = (sp.pi / 2) / k, (3 * sp.pi / 2) / k        # rear and front rest positions at wt = 0
span = (Xf + AL * sp.sin(k * Xf)) - (Xr + AL * sp.sin(k * Xr))
print('span =', sp.simplify(span), '; fraction of lambda =', sp.simplify(span / lam))
