"""Gate 2, level L1 (chapter 2), route 2 (numerical): finite differences and quadrature, no symbolic algebra.
(a) stream function (2.1) differentiated numerically -> velocity; compare with textbook Cartesian Stokes-flow field
(b) viscous stress by finite differences; drag on spheres of several radii by quadrature  -> 6 pi mu a U
(c) (2.3): integrate m dv/dt = weight - buoyancy - 6 pi mu a v and compare terminal speed with k a^2
(d) (2.5) and (2.4) against the model's drag curve (Beard) through physics.cjs outputs (see L1_model_dump.cjs)"""
import numpy as np, json, subprocess
from scipy.integrate import solve_ivp, quad
U, a, mu = 0.37, 1.3, 0.81
psi = lambda r, th: 0.5 * U * np.sin(th)**2 * (r**2 - 1.5 * a * r + a**3 / (2 * r))
def u_from_psi(r, th, h=1e-6):
    dpsi_dth = (psi(r, th + h) - psi(r, th - h)) / (2 * h)
    dpsi_dr = (psi(r + h, th) - psi(r - h, th)) / (2 * h)
    ur = dpsi_dth / (r**2 * np.sin(th)); ut = -dpsi_dr / (r * np.sin(th))
    return ur, ut
def u_cart_from_psi(X):
    x, y, z = X; r = np.sqrt(x*x + y*y + z*z); th = np.arccos(z / r); rho = np.hypot(x, y)
    ur, ut = u_from_psi(r, th)
    # unit vectors: e_r = X/r ; e_th = (cos th cos ph, cos th sin ph, -sin th)
    cph, sph = x / rho, y / rho
    return ur * np.array([x, y, z]) / r + ut * np.array([np.cos(th) * cph, np.cos(th) * sph, -np.sin(th)])
def u_text(X):
    X = np.asarray(X, float); r = np.linalg.norm(X); ez = np.array([0, 0, 1.0]); z = X[2]
    return U * ez - 0.75 * a * U * (ez / r + z * X / r**3) - 0.25 * a**3 * U * (ez / r**3 - 3 * z * X / r**5)
rng = np.random.default_rng(7)
print('(a) velocity from numerically differentiated (2.1) vs textbook Cartesian field, 6 random points outside the sphere')
for _ in range(6):
    X = rng.normal(size=3); X *= rng.uniform(1.0, 5.0) * a / np.linalg.norm(X)
    d = u_cart_from_psi(X) - u_text(X)
    print('   |X|/a = %.2f  max|diff| = %.2e  (|u| = %.3f)' % (np.linalg.norm(X) / a, np.abs(d).max(), np.linalg.norm(u_text(X))))
print('   no-slip: |u| on r = a at 5 random angles:', [float('%.1e' % np.linalg.norm(u_text(a * v / np.linalg.norm(v)))) for v in rng.normal(size=(5, 3))])
print('   far field: u(100a)/U =', u_text(np.array([30.0, 40.0, 50.0]) * a / np.sqrt(5000) * 100).round(4) / U)

def p_text(X):
    X = np.asarray(X, float); return -1.5 * mu * U * a * X[2] / np.linalg.norm(X)**3
def stress(X, h=1e-5):
    G = np.zeros((3, 3))
    for j in range(3):
        e = np.zeros(3); e[j] = h
        G[:, j] = (u_text(X + e) - u_text(X - e)) / (2 * h)       # G[i,j] = du_i/dx_j
    return -p_text(X) * np.eye(3) + mu * (G + G.T)
def force_on_sphere(s, n_th=200):
    # Gauss-Legendre in cos(theta); axisymmetry lets us take phi = 0 and multiply by 2 pi (check F_x = 0 separately with phi samples)
    xs, ws = np.polynomial.legendre.leggauss(n_th)
    F = np.zeros(3)
    for c, w in zip(xs, ws):
        sn = np.sqrt(1 - c * c)
        for ph, wph in zip(np.linspace(0, 2 * np.pi, 8, endpoint=False), [2 * np.pi / 8] * 8):
            n = np.array([sn * np.cos(ph), sn * np.sin(ph), c])
            F += stress(s * n) @ n * s * s * w * wph
    return F
print('(b) drag by quadrature of the numerically differentiated stress (analytic velocity field, finite-difference gradient), 6 pi mu a U =', 6 * np.pi * mu * a * U)
for s in [1.0, 1.5, 3.0, 8.0]:
    F = force_on_sphere(s * a)
    print('   sphere r = %.1f a : F = (%.2e, %.2e, %.8f)  ratio F_z/(6 pi mu a U) = %.8f' % (s, F[0], F[1], F[2], F[2] / (6 * np.pi * mu * a * U)))
# pressure and viscous part separately on r = a
xs, ws = np.polynomial.legendre.leggauss(200)
Fp = sum(-p_text(a * np.array([np.sqrt(1 - c * c), 0, c])) * c * a * a * w * 2 * np.pi for c, w in zip(xs, ws))
print('   pressure part on r = a: %.8f  (2 pi mu a U = %.8f) ;  viscous part = total - pressure = %.8f (4 pi mu a U = %.8f)' % (Fp, 2 * np.pi * mu * a * U, force_on_sphere(a)[2] - Fp, 4 * np.pi * mu * a * U))

print('(c) (2.3): equation of motion m dv/dt = (m - m_displaced) g - 6 pi mu a v, a = 20 um water drop in air')
mu_a, rho_a, rho_w, g, a_ = 1.8e-5, 1.2, 1000.0, 9.81, 20e-6
m_ = 4 / 3 * np.pi * a_**3 * rho_w
sol = solve_ivp(lambda t, v: ((m_ - 4 / 3 * np.pi * a_**3 * rho_a) * g - 6 * np.pi * mu_a * a_ * v[0]) / m_, [0, 0.05], [0.0], rtol=1e-10, atol=1e-14)
k = 2 * (rho_w - rho_a) * g / (9 * mu_a)
tau = 2 * rho_w * a_**2 / (9 * mu_a)
print('   v(t=50 ms) = %.8e m/s ; k a^2 = %.8e m/s ; relaxation time m/(6 pi mu a) = %.3e s (ODE reached %.6f of terminal after 50 ms = %.0f tau)' % (sol.y[0, -1], k * a_**2, tau, sol.y[0, -1] / (k * a_**2), 0.05 / tau))
