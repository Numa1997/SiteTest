"""Chapter 3 reference: acceleration, the relativistic wavelength, deceleration to the landing voltage. Mirrors physics/ch03.js.

    p^2 = 2 m e V (1 + e V / (2 m c^2)) = 2 m e V*,   lambda = h / p,   ang_mag = sqrt(V*_acc / V*_land)
"""
import math

from .core import C

INPUTS = ['V_acc', 'V_land']
OUTPUTS = ['E_0', 'lambda_e', 'gamma', 'V_star', 'V_star_land', 'lambda_land', 'ang_mag', 'lambda_curve']
MC2 = C['m_e'] * C['c'] ** 2


def vstar(V):
    return V * (1 + C['e'] * V / (2 * MC2))


def lam(V):
    return C['h'] / math.sqrt(2 * C['m_e'] * C['e'] * vstar(V))


def lam_nr(V):
    return C['h'] / math.sqrt(2 * C['m_e'] * C['e'] * V)


def compute(p):
    V, Vl = float(p['V_acc']), float(p['V_land'])
    curve = []
    for i in range(61):
        v = 10 ** (1 + 5 * i / 60)
        curve += [v, lam(v), lam_nr(v)]
    return dict(E_0=C['e'] * V, gamma=1 + C['e'] * V / MC2, V_star=vstar(V), lambda_e=lam(V), V_star_land=vstar(Vl),
                lambda_land=lam(Vl), ang_mag=math.sqrt(vstar(V) / vstar(Vl)), lambda_curve=curve)
