"""Chapter 1 reference: one electron in uniform E (+y) and B (+z). Mirrors physics/ch01.js line by line, in NumPy float64.

    d(gamma m v)/dt = q (E + v x B),  q = -e;   u = gamma v;   dr/dt = u/gamma;   du/dt = (q/m)(E + (u/gamma) x B)

Integrators: 'boris' (Boris 1970: half electric kick, rotation u' = u + u x t, u+ = u + u' x s, half electric kick) and 'rk4'.
Also here, for the figures and the number expressions of text/ch01.py: the exact helix of a pure magnetic field and the error laws of
the two integrators (exact phase errors of the Boris rotation and of the RK4 step on a rotation).
"""
import math

import numpy as np

from .core import C

INPUTS = ['E_field', 'B_field', 'v_0', 'theta_0', 'dt', 'integrator', 't_run']
OUTPUTS = ['r_g', 'omega_c', 'energy_drift', 'trajectory', 'x_end', 'y_end', 'z_end', 'theta_end']
Q = -C['e']
MAX_STEPS = 400000
MAX_POINTS = 300


def gamma_of(u):
    return math.sqrt(1.0 + float(np.dot(u, u)) / (C['c'] * C['c']))


def gamma_minus_1(u):
    """gamma - 1 = u^2 / (c^2 (1 + gamma)): no cancellation."""
    return float(np.dot(u, u)) / (C['c'] ** 2 * (1.0 + gamma_of(u)))


def boris_kick(u, E, B, h):
    a = Q * h / (2.0 * C['m_e'])
    um = u + a * E
    t = a * B / gamma_of(um)
    s = 2.0 * t / (1.0 + np.dot(t, t))
    up = um + np.cross(um, t)
    uplus = um + np.cross(up, s)
    return uplus + a * E


def _rhs(u, E, B):
    g = gamma_of(u)
    v = u / g
    return v, (Q / C['m_e']) * (E + np.cross(v, B))


def rk4_step(r, u, h, E, B):
    k1 = _rhs(u, E, B)
    k2 = _rhs(u + 0.5 * h * k1[1], E, B)
    k3 = _rhs(u + 0.5 * h * k2[1], E, B)
    k4 = _rhs(u + h * k3[1], E, B)
    return (r + h / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            u + h / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))


def compute(p):
    E = np.array([0.0, p['E_field'], 0.0])
    B = np.array([0.0, 0.0, p['B_field']])
    g0 = 1.0 / math.sqrt(1.0 - (p['v_0'] / C['c']) ** 2)
    u = np.array([g0 * p['v_0'] * math.sin(p['theta_0']), 0.0, g0 * p['v_0'] * math.cos(p['theta_0'])])
    u0 = u.copy()
    n = min(MAX_STEPS, max(1, math.ceil(p['t_run'] / p['dt'])))
    h = p['t_run'] / n
    stride = max(1, math.ceil(n / MAX_POINTS))
    r = np.zeros(3)
    path = [0.0, 0.0, 0.0]
    uh = None
    boris = p['integrator'] == 'boris'
    if boris:
        uh = boris_kick(u, E, B, -h / 2.0)
    for i in range(1, n + 1):
        if boris:
            uh = boris_kick(uh, E, B, h)
            r = r + h * uh / gamma_of(uh)
        else:
            r, u = rk4_step(r, u, h, E, B)
        if i % stride == 0 or i == n:
            path.extend((float(r[0]), float(r[1]), float(r[2])))
    if boris:
        u = boris_kick(uh, E, B, h / 2.0)
    g1 = gamma_of(u)
    v = u / g1
    return {
        'r_g': g0 * C['m_e'] * p['v_0'] * math.sin(p['theta_0']) / (C['e'] * p['B_field']) if p['B_field'] > 0 else 0.0,
        'omega_c': C['e'] * p['B_field'] / (g0 * C['m_e']),
        'energy_drift': gamma_minus_1(u) / gamma_minus_1(u0) - 1.0,
        'trajectory': path,
        'x_end': float(r[0]), 'y_end': float(r[1]), 'z_end': float(r[2]),
        'theta_end': math.atan2(float(v[1]), float(v[0])),
    }


# ---------------------------------------------------------------------------------------------- helpers for the text and figures
def gamma_from_V(V):
    """After falling through V volts from rest: (gamma - 1) m c^2 = e V."""
    return 1.0 + C['e'] * V / (C['m_e'] * C['c'] ** 2)


def speed_from_V(V):
    g = gamma_from_V(V)
    return C['c'] * math.sqrt(1.0 - 1.0 / g ** 2)


def lambda_E(V):
    T = C['e'] * V
    return C['h'] * C['c'] / math.sqrt(T * (T + 2.0 * C['m_e'] * C['c'] ** 2))


def helix_exact(v0, B, theta0, t):
    """Exact position after time t of the electron of compute() with E = 0: a helix about B (along z), started at the origin."""
    g = 1.0 / math.sqrt(1.0 - (v0 / C['c']) ** 2)
    Om = Q * B / (g * C['m_e'])
    uperp = g * v0 * math.sin(theta0)
    upar = g * v0 * math.cos(theta0)
    S, Co = math.sin(Om * t), math.cos(Om * t)
    return np.array([uperp * S / (g * Om), -uperp * (1.0 - Co) / (g * Om), upar * t / g])


def rk4_amp2(theta):
    """|R(i theta)|^2 for one RK4 step on a rotation by theta: the factor on the squared radius."""
    return 1.0 - theta ** 6 / 72.0 + theta ** 8 / 576.0


def phase_error_boris(theta):
    return theta - 2.0 * math.atan(theta / 2.0)


def phase_error_rk4(theta):
    return theta - math.atan2(theta - theta ** 3 / 6.0, 1.0 - theta ** 2 / 2.0 + theta ** 4 / 24.0)


def circle_fit(p):
    """Kasa least-squares circle through points (n, 2): radius."""
    p = np.asarray(p, float)
    x = p[:, 0] - p[:, 0].mean()
    y = p[:, 1] - p[:, 1].mean()
    A = np.column_stack([x, y, np.ones_like(x)])
    sol = np.linalg.lstsq(A, x * x + y * y, rcond=None)[0]
    return math.sqrt(sol[2] + (sol[0] / 2.0) ** 2 + (sol[1] / 2.0) ** 2)
