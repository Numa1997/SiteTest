"""Gate for plant.py, the one-wheel cart: the hand-assembled M, C, K against the Hessians of the Lagrangian written out in SymPy
(route 2), the modal row against the modal equation of the note (route 3, the boundary-value derivation, level tray):
   (1 + kappa) a'' + 2 gamma (1 + kappa) a' + omega^2 (1 + kappa) a = -lam Q x_O''
and the kick (route 4): for a cart rolling freely over a bump, the work of -N z_a' equals the change of M g z_a (energy).
Run: python3 tools/fig12/check_plant.py
"""
import sys, os, numpy as np, sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plant, road
P = dict(plant.DEFAULT); rho = 1007.0; g = plant.G_ACC
# a synthetic fill in the data file's format (numbers of the right size)
fill = dict(V_liq=5.0e-4, J_ry=1.4e-6, J_rx=1.4e-6, zs=0.144, modes=[
    dict(m=1, o='c', n=1, lam=47.0, N=1.6e-3, Qx=0.0327, Qy=0.0, Qrx=0.0, Qry=-0.0019),
    dict(m=1, o='s', n=1, lam=47.3, N=1.6e-3, Qx=0.0, Qy=0.0325, Qrx=0.0019, Qry=0.0)])
modes = plant.modal_params(fill, rho, 0.045, 0.3, lambda md: 0.6)
S = plant.assemble(P, fill, modes, rho)
M, C, K = S['M'], S['C'], S['K']
ok = True
sym = np.abs(M - M.T).max() + np.abs(K - K.T).max() + np.abs(C - C.T).max()
print(f'symmetry {sym:.1e}; M positive definite: {np.all(np.linalg.eigvalsh(M) > 0)}')
if sym > 1e-9 or not np.all(np.linalg.eigvalsh(M) > 0): ok = False

# ---- route 2: SymPy Lagrangian of the one-wheel cart, q = (x_c, z_b, z_w, a, b) ----
xc, zb, zw, a, b = q = sp.symbols('x_c z_b z_w a b')
vx, vz, vw, va, vb = qd = sp.symbols('vx vz vw va vb')
mx, my = modes['x'][0], modes['y'][0]
m_l = rho * fill['V_liq']
mu_x = rho * mx['N'] / mx['lam']; mu_y = rho * my['N'] / my['lam']
T = (sp.Rational(1, 2) * (P['M_b'] + P['M_g'] + m_l + P['m_w']) * vx ** 2      # everything moves along the road
     + sp.Rational(1, 2) * (P['M_b'] + P['M_g'] + m_l) * vz ** 2 + sp.Rational(1, 2) * P['m_w'] * vw ** 2
     + sp.Rational(1, 2) * mu_x * (1 + mx['kappa']) * va ** 2 + rho * mx['Q'] * mx['N'] * vx * va     # the x-mode and its coupling to x_O = x_c
     + sp.Rational(1, 2) * mu_y * (1 + my['kappa']) * vb ** 2)                                         # nothing in this plane drives the y-mode
V = (sp.Rational(1, 2) * P['k'] * (zb - zw) ** 2 + sp.Rational(1, 2) * P['k_t'] * zw ** 2
     + sp.Rational(1, 2) * mu_x * mx['w2'] * (1 + mx['kappa']) * a ** 2 + sp.Rational(1, 2) * mu_y * my['w2'] * (1 + my['kappa']) * b ** 2)
Dfun = (sp.Rational(1, 2) * P['c'] * (vz - vw) ** 2 + sp.Rational(1, 2) * P['c_t'] * vw ** 2 + sp.Rational(1, 2) * (P['c_x'] + P['c_d']) * vx ** 2
        + mu_x * (1 + mx['kappa']) * mx['gamma'] * va ** 2 + mu_y * (1 + my['kappa']) * my['gamma'] * vb ** 2)
M2 = np.array(sp.hessian(T, qd), float); K2 = np.array(sp.hessian(V, q), float); C2 = np.array(sp.hessian(Dfun, qd), float)
for name, A1, A2 in (('M', M, M2), ('C', C, C2), ('K', K, K2)):
    err = np.abs(A1 - A2).max() / np.abs(A2).max(); print(f'{name}: hand assembly vs SymPy Hessian, max rel diff {err:.1e}')
    if err > 1e-12: ok = False; print(np.round(A1 - A2, 6))

# ---- route 3: the modal row against the boundary-value modal equation (level tray: x_O'' = x_c'') ----
rng = np.random.default_rng(1); n = S['n']; qq = rng.normal(size=n); qd_ = rng.normal(size=n); qdd = rng.normal(size=n)
i = S['idx']['a'][0]; ix = S['idx']['x']; row = (M @ qdd + C @ qd_ + K @ qq)[i]
rhs = mu_x * ((1 + mx['kappa']) * qdd[i] + 2 * mx['gamma'] * (1 + mx['kappa']) * qd_[i] + mx['w2'] * (1 + mx['kappa']) * qq[i] + mx['lam'] * mx['Q'] * qdd[ix])
print(f"modal row vs the note's modal equation (12) with x_O'' = x_c'': {abs(row - rhs)/abs(rhs):.1e}")
if abs(row - rhs) / abs(rhs) > 1e-12: ok = False
print(f'x-row coupling rho Q N = {M[ix, i]:.5e}; heave row coupling to the mode = {M[S["idx"]["z"], i]:.1e} (zero: lifting the glass pushes no wave)')
if abs(M[ix, i] - rho * mx['Q'] * mx['N']) > 1e-12 or M[S['idx']['z'], i] != 0: ok = False

# ---- route 4: the kick, by energy. A rigid cart of mass Mt rolling freely over the bump, its weight on the road (N = Mt g), only the
# kick along the road: Mt X'' = -Mt g z_a'(X). Energy: 1/2 Mt X'^2 + Mt g z_a(X) is constant. Integrated by RK4 over the bump.
ax_ = road.Axle(road.PROFILES['bump'], 0.03, R=P['R_w']); Mt = S['M_tot']
def f(s): X, V_ = s; return np.array([V_, -g * ax_.slope(X)])
s = np.array([0.5, 1.5]); E0 = 0.5 * Mt * s[1] ** 2 + Mt * g * ax_(s[0]); h = 1e-4; Emax = 0.0; vmin = 9
while s[0] < 2.0:
    k1 = f(s); k2 = f(s + h / 2 * k1); k3 = f(s + h / 2 * k2); k4 = f(s + h * k3); s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    Emax = max(Emax, abs(0.5 * Mt * s[1] ** 2 + Mt * g * ax_(s[0]) - E0)); vmin = min(vmin, s[1])
print(f'free roll over the 30 mm bump at 1.5 m/s: energy drift {Emax / E0:.1e} of the total; slowest {vmin:.4f} m/s, '
      f'against sqrt(v^2 - 2 g h) = {np.sqrt(1.5 ** 2 - 2 * g * 0.03):.4f} m/s and the small-slope estimate v - g h/v = {1.5 - g * 0.03 / 1.5:.4f} m/s')
if Emax / E0 > 1e-4 or abs(vmin - np.sqrt(1.5 ** 2 - 2 * g * 0.03)) > 2e-3: ok = False

# ---- route 5: the envelope at a sharp step: before the edge the axle rises on the circle round it, z_a = sqrt(R^2 - d^2) - (R - h)... measured
P_ = dict(P); R = P_['R_w']; h_ = 0.02
st = road.Axle(lambda x, h: np.where(x >= 1.0, h, 0.0), h_, R=R)
for d in (0.06, 0.04, 0.02):
    exact = max(0.0, h_ + np.sqrt(R * R - d * d) - R) if d < R else 0.0
    got = st(1.0 - d); print(f'  step of {h_*1e3:.0f} mm, axle {d*1e3:.0f} mm before the edge: envelope {got*1e3:.3f} mm, circle round the edge {exact*1e3:.3f} mm')
    if abs(got - exact) > 2.1e-4: ok = False      # the 2 mm grid: the circle sampled at grid points
# ---- eigenfrequencies of the free system, as a sanity print
A, Bu, Bw = plant.state_space(S); ev = np.linalg.eigvals(A)
print('free motions (Hz, damping ratio):', sorted([(round(abs(e.imag) / 2 / np.pi, 3), round(-e.real / abs(e), 3)) for e in ev if e.imag > 0]))
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
