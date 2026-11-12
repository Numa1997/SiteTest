"""Checks of the formulas flat.py uses, done here rather than trusted from memory.
1. T_plane against a direct solution of the four matching equations at the two faces (plane wave, slab of width a).
2. gfree solves the free equation i g_t = -(1/2) g_yy (SymPy), and g(y) g(z) = g(0) g(rho).
3. The solver's packet transmission against T_packet."""
import numpy as np, sympy as sp
from flat import T_plane, T_packet, gfree, run, HARD
def T_match(E, V0, a):
    k = np.sqrt(2 * E + 0j); q = np.sqrt(2 * (E - V0) + 0j)
    # psi = e^{ikx} + r e^{-ikx} (x < 0); A e^{iqx} + B e^{-iqx} (0 < x < a); t e^{ikx} (x > a); unknowns r, A, B, t
    M = np.array([[-1, 1, 1, 0], [1j * k, 1j * q, -1j * q, 0],
                  [0, np.exp(1j * q * a), np.exp(-1j * q * a), -np.exp(1j * k * a)],
                  [0, 1j * q * np.exp(1j * q * a), -1j * q * np.exp(-1j * q * a), -1j * k * np.exp(1j * k * a)]])
    rhs = np.array([1, 1j * k, 0, 0])
    r, A, B, t = np.linalg.solve(M, rhs)
    return abs(t)**2
worst = 0
for E in np.linspace(0.05, 6, 120):
    for V0 in (-4, -2, -1, 0.5, 1, 1.5, 2, 3, 4, 6, 8):
        for a in (0.5, 1, 1.5, 2, 3):
            if abs(E - V0) < 1e-9: continue
            worst = max(worst, abs(T_match(E, V0, a) - T_plane(np.array([E]), V0, a)[0]))
print(f"1. T_plane vs the matching equations: largest difference {worst:.2e} over 120 x 11 x 5 cases")
y, z, t, s = sp.symbols('y z t s', positive=True)
c = 1 + sp.I * t / (2 * s**2)
g = (2 * sp.pi * s**2) ** sp.Rational(-1, 4) * c ** sp.Rational(-1, 2) * sp.exp(-y**2 / (4 * s**2 * c))
res = sp.simplify(sp.I * sp.diff(g, t) + sp.diff(g, y, 2) / 2)
norm0 = sp.simplify(sp.integrate((g * sp.conjugate(g)).subs(t, 0), (y, -sp.oo, sp.oo)))
print("2. residual of i g_t + g_yy / 2:", res, "; norm at t = 0:", norm0)
yy, zz = 1.3, -0.7; print("   g(y) g(z) - g(0) g(rho):", abs(gfree(yy, 2.0, 3) * gfree(zz, 2.0, 3) - gfree(0, 2.0, 3) * gfree(np.hypot(yy, zz), 2.0, 3)))
for E, V0, a in [(2.0, 3.0, 1.0), (0.5, 0.5, 0.5), (4.5, 8.0, 0.5), (1.0, -4.0, 3.0), (2.0, HARD, 1.0)]:
    r = run(E, V0, a); _, n, b, ah, _ = r['curves'][-1]
    print(f"3. E={E} V0={'hard' if V0 >= HARD else V0} a={a}: ahead {ah:.5f}, T_packet {T_packet(E, V0, a):.5f}, norm {n:.8f}")
