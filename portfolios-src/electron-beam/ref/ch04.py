"""Chapter 4 reference: a round magnetic lens with Glaser's bell-shaped field, focused on the wafer; its focal length, magnification,
image rotation and the aberration coefficients C_s and C_c measured by ray tracing. Mirrors physics/ch04.js.

    B(z) = B0 / (1 + (z/a)^2),   B0 = mu0 NI / (pi a)           (Ampere: the line integral of B along the axis is mu0 NI)
    paraxial ray, rotating frame:  r'' = -eta B(z)^2 r,   eta = e / (8 m V*)
    off-axis field (div B = 0, curl B = 0):  B_z = B - r^2 B''/4,   B_r = -r B'/2 + r^3 B'''/16
    exact ray in a static magnetic field, z as the variable (speed constant):
        x'' = (q/p) s [ x' y' B_x - (1 + x'^2) B_y + y' B_z ],   y'' = (q/p) s [ (1 + y'^2) B_x - x' y' B_y - x' B_z ],   s = sqrt(1 + x'^2 + y'^2)
    The integration variable is t with z = a tan t, so that the steps crowd into the lens and the long field-free stretches cost little.
    Lens centre at z = 0, object (a crossover or the source image) at z = -u_obj on the axis, wafer at z = +WD.
"""
import math

from .core import C

INPUTS = ['a_lens', 'u_obj', 'WD', 'V_land']
OUTPUTS = ['NI', 'B_0', 'M', 'f', 'C_s', 'C_c', 'theta_rot', 'omega_G', 'lens_ray']
NSTEP = 6000
E, ME, MU0 = C['e'], C['m_e'], C['mu0']


def vstar(V):
    return V * (1 + E * V / (2 * ME * C['c'] ** 2))


def glaser(z, B0, a):
    """B and its first three derivatives on the axis."""
    u = z / a
    q = 1 + u * u
    return (B0 / q, -2 * B0 * u / (a * q * q), B0 * (6 * u * u - 2) / (a * a * q ** 3), 24 * B0 * u * (1 - u * u) / (a ** 3 * q ** 4))


def _grid(a, z0, z1):
    t0, t1 = math.atan(z0 / a), math.atan(z1 / a)
    return t0, (t1 - t0) / NSTEP


def paraxial(B0, a, eta, z0, z1, r0, rp0, record=None):
    """RK4 of r'' = -eta B^2 r in t (z = a tan t); returns (r, r') at z1."""
    t0, h = _grid(a, z0, z1)

    def f(t, y):
        z = a * math.tan(t)
        dz = a / math.cos(t) ** 2
        B = B0 / (1 + (z / a) ** 2)
        return (y[1] * dz, -eta * B * B * y[0] * dz)
    y = (r0, rp0)
    t = t0
    for i in range(NSTEP):
        if record is not None and i % 20 == 0:
            record.extend([a * math.tan(t), y[0]])
        k1 = f(t, y)
        k2 = f(t + h / 2, (y[0] + h / 2 * k1[0], y[1] + h / 2 * k1[1]))
        k3 = f(t + h / 2, (y[0] + h / 2 * k2[0], y[1] + h / 2 * k2[1]))
        k4 = f(t + h, (y[0] + h * k3[0], y[1] + h * k3[1]))
        y = (y[0] + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), y[1] + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
        t += h
    if record is not None:
        record.extend([a * math.tan(t), y[0]])
    return y


def ray3d(B0, a, qp, z0, z1, xp0):
    """Exact ray (third-order field) from the axis point z0 with slope xp0 in the x-z plane; returns (x, y) at z1."""
    t0, h = _grid(a, z0, z1)

    def f(t, s):
        x, y, xp, yp = s
        z = a * math.tan(t)
        dz = a / math.cos(t) ** 2
        B, B1, B2, B3 = glaser(z, B0, a)
        r2 = x * x + y * y
        Bz = B - r2 * B2 / 4
        Brr = -B1 / 2 + r2 * B3 / 16                       # B_r / r
        Bx, By = Brr * x, Brr * y
        w = math.sqrt(1 + xp * xp + yp * yp)
        xpp = qp * w * (xp * yp * Bx - (1 + xp * xp) * By + yp * Bz)
        ypp = qp * w * ((1 + yp * yp) * Bx - xp * yp * By - xp * Bz)
        return (xp * dz, yp * dz, xpp * dz, ypp * dz)
    s = (0.0, 0.0, xp0, 0.0)
    t = t0
    for _ in range(NSTEP):
        k1 = f(t, s)
        k2 = f(t + h / 2, tuple(s[i] + h / 2 * k1[i] for i in range(4)))
        k3 = f(t + h / 2, tuple(s[i] + h / 2 * k2[i] for i in range(4)))
        k4 = f(t + h, tuple(s[i] + h * k3[i] for i in range(4)))
        s = tuple(s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4))
        t += h
    return s[0], s[1]


def focus_B0(a, eta, u, wd):
    """The peak field that brings the axial ray from z = -u back to the axis at z = +wd (first crossing), by bisection."""
    lo, hi = 0.0, math.sqrt(3 / eta) / a          # omega^2 = 1 + eta B0^2 a^2 = 4 at hi: beyond the first-crossing regime
    for _ in range(60):
        mid = (lo + hi) / 2
        r, _ = paraxial(mid, a, eta, -u, wd, 0.0, 1.0)
        if r > 0:
            lo = mid                               # not yet crossed: stronger lens needed
        else:
            hi = mid
    return (lo + hi) / 2


def compute(p):
    a, u, wd = p['a_lens'], p['u_obj'], p['WD']
    Vs = vstar(p['V_land'])
    eta = E / (8 * ME * Vs)
    pmom = math.sqrt(2 * ME * E * Vs)
    B0 = focus_B0(a, eta, u, wd)
    NI = B0 * math.pi * a / MU0
    # magnification from the angles of the axial ray (Lagrange: same voltage on both sides)
    ray = []
    _, rp_i = paraxial(B0, a, eta, -u, wd, 0.0, 1.0, ray)
    M = 1.0 / abs(rp_i)
    # focal length: a ray parallel to the axis far before the lens, its slope far behind
    zfar = 2000 * a
    _, rp_far = paraxial(B0, a, eta, -zfar, zfar, 1.0, 0.0)
    f = -1.0 / rp_far
    omega = math.sqrt(1 + eta * B0 * B0 * a * a)
    theta = math.sqrt(E / (8 * ME * Vs)) * B0 * a * (math.atan(wd / a) + math.atan(u / a))
    # spherical aberration: miss at the paraxial image plane, linear (defocus) part removed with a tiny ray, two angles to remove alpha^5
    qp = -E / pmom
    eps = 1e-7
    xe, ye = ray3d(B0, a, qp, -u, wd, eps)
    miss = []
    for ai in (2e-3, 4e-3):
        ao = ai * M                            # object angle: M = alpha_o / alpha_i (Lagrange, same voltage)
        x, y = ray3d(B0, a, qp, -u, wd, ao)
        k = ao / eps
        miss.append(math.hypot(x - k * xe, y - k * ye))
    a1, a2 = 2e-3, 4e-3
    Cs = (miss[0] * a2 ** 5 - miss[1] * a1 ** 5) / (a1 ** 3 * a2 ** 5 - a2 ** 3 * a1 ** 5)
    # chromatic aberration: paraxial miss for a relative voltage change delta, central difference
    d = 1e-4
    rpl, _ = paraxial(B0, a, eta / (1 + d), -u, wd, 0.0, 1.0)
    rmi, _ = paraxial(B0, a, eta / (1 - d), -u, wd, 0.0, 1.0)
    Cc = abs((rpl - rmi) / (2 * d)) * M        # per unit image angle: r is per unit object slope, alpha_i = alpha_o / M
    return dict(NI=NI, B_0=B0, M=M, f=f, C_s=Cs, C_c=Cc, theta_rot=theta, omega_G=omega, lens_ray=ray)
