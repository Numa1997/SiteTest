"""Gate for plant.py: the hand-assembled M, C, K against the Hessians of the Lagrangian written out in SymPy (route 2),
and the modal row against the modal equation of the note (route 3, the boundary-value derivation):
   (1 + kappa) a'' + 2 gamma (1 + kappa) a' + omega^2 (1 + kappa) a = -lam [Q (x_O'' - g psi) + Q_r psi'']
Run: python3 tools/fig12/check_plant.py
"""
import sys, os, numpy as np, sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plant
P = dict(plant.DEFAULT); rho = 1007.0; g = 9.81
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

# ---- route 2: SymPy Lagrangian ----
xc, yc, zb, ps, zf, zr, a, b = q = sp.symbols('x_c y_c z_b psi z_f z_r a b')
vx, vy, vz, vp, vf, vr, va, vb = qd = sp.symbols('vx vy vz vp vf vr va vb')
mx, my = modes['x'][0], modes['y'][0]
m_l = rho * fill['V_liq']; J_ry = rho * fill['J_ry']; zcm = S['z_cm_l']; hgg = P['h_g'] + 0.08
xO_d = vx + P['h_g'] * vp; zO_d = vz - P['d_g'] * vp; yO_d = vy
mu_x = rho * mx['N'] / mx['lam']; mu_y = rho * my['N'] / my['lam']
T = (sp.Rational(1, 2) * (P['M_b'] + 2 * P['m_w'] + P['M_g'] + m_l) * (vx ** 2 + vy ** 2)      # everything along the road and sideways (the liquid's x-part is in xO below: subtract it)
     - sp.Rational(1, 2) * m_l * vx ** 2
     + sp.Rational(1, 2) * (P['M_b'] + P['M_g']) * vz ** 2 + sp.Rational(1, 2) * P['J_b'] * vp ** 2
     + sp.Rational(1, 2) * P['M_g'] * ((P['h_g'] + 0.08) ** 2 + P['d_g'] ** 2) * vp ** 2        # the glass as a point mass on the body
     + sp.Rational(1, 2) * P['m_w'] * (vf ** 2 + vr ** 2)
     + sp.Rational(1, 2) * m_l * (xO_d ** 2 + zO_d ** 2) + sp.Rational(1, 2) * J_ry * vp ** 2 + m_l * zcm * xO_d * vp     # the frozen liquid
     + sp.Rational(1, 2) * mu_x * (1 + mx['kappa']) * va ** 2 + rho * mx['Q'] * mx['N'] * xO_d * va + rho * mx['Qr'] * mx['N'] * vp * va
     + sp.Rational(1, 2) * mu_y * (1 + my['kappa']) * vb ** 2 + rho * my['Q'] * my['N'] * yO_d * vb)
df = zb - P['l_f'] * ps - zf; dr = zb + P['l_r'] * ps - zr
V = (sp.Rational(1, 2) * P['k'] * (df ** 2 + dr ** 2) + sp.Rational(1, 2) * P['k_t'] * (zf ** 2 + zr ** 2)
     - sp.Rational(1, 2) * g * (P['M_g'] * hgg + m_l * (P['h_g'] + zcm)) * ps ** 2
     + sp.Rational(1, 2) * mu_x * mx['w2'] * (1 + mx['kappa']) * a ** 2 - rho * g * mx['Q'] * mx['N'] * ps * a
     + sp.Rational(1, 2) * mu_y * my['w2'] * (1 + my['kappa']) * b ** 2)
Dfun = (sp.Rational(1, 2) * P['c'] * ((vz - P['l_f'] * vp - vf) ** 2 + (vz + P['l_r'] * vp - vr) ** 2) + sp.Rational(1, 2) * P['c_t'] * (vf ** 2 + vr ** 2)
        + sp.Rational(1, 2) * P['c_x'] * vx ** 2 + sp.Rational(1, 2) * P['c_y'] * vy ** 2
        + mu_x * (1 + mx['kappa']) * mx['gamma'] * va ** 2 + mu_y * (1 + my['kappa']) * my['gamma'] * vb ** 2)
M2 = np.array(sp.hessian(T, qd), float); K2 = np.array(sp.hessian(V, q), float); C2 = np.array(sp.hessian(Dfun, qd), float)
for name, A1, A2 in (('M', M, M2), ('C', C, C2), ('K', K, K2)):
    err = np.abs(A1 - A2).max() / np.abs(A2).max(); print(f'{name}: hand assembly vs SymPy Hessian, max rel diff {err:.1e}')
    if err > 1e-12: ok = False; print(np.round(A1 - A2, 6))

# ---- route 3: the modal row against the boundary-value modal equation ----
rng = np.random.default_rng(1); qq = rng.normal(size=8); qd_ = rng.normal(size=8); qdd = rng.normal(size=8)
i = S['idx']['a'][0]; ip = S['idx']['psi']; row = (M @ qdd + C @ qd_ + K @ qq)[i]
xO_dd = qdd[0] + P['h_g'] * qdd[ip]; psi = qq[ip]; psidd = qdd[ip]
rhs = mu_x * ((1 + mx['kappa']) * qdd[i] + 2 * mx['gamma'] * (1 + mx['kappa']) * qd_[i] + mx['w2'] * (1 + mx['kappa']) * qq[i]
              + mx['lam'] * (mx['Q'] * (xO_dd - g * psi) + mx['Qr'] * psidd))
print(f'modal row vs the note\'s modal equation: {abs(row - rhs)/abs(rhs):.1e}')
if abs(row - rhs) / abs(rhs) > 1e-12: ok = False
# ---- route 4: the stout's push back: the x-row's liquid terms equal -rho sum Q N a'' (the momentum of the waves)
ix = S['idx']['x']; push = M[ix, i] * qdd[i]; print(f'x-row coupling rho Q N = {M[ix, i]:.5e}, pitch-row coupling {M[ip, i]:.5e} (= rho N (Q h_g + Q_r))')
if abs(M[ix, i] - rho * mx['Q'] * mx['N']) > 1e-12 or abs(M[ip, i] - rho * mx['N'] * (mx['Q'] * P['h_g'] + mx['Qr'])) > 1e-12: ok = False
# ---- eigenfrequencies of the free system, as a sanity print
A, Bu, Bw = plant.state_space(S); ev = np.linalg.eigvals(A)
print('free motions (Hz, damping ratio):', sorted([(round(abs(e.imag) / 2 / np.pi, 3), round(-e.real / abs(e), 3)) for e in ev if e.imag > 0]))
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
