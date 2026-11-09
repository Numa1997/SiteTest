"""Chapter 5 reference: probe size against beam angle for an asked probe current, two conventions; mirrors physics/ch05.js.

    d_I = sqrt(4 I_p / (pi^2 B_pr V* alpha^2)),  B_pr = B_r / ln 2
    fw50: d_A = 0.54 lam/alpha, d_S = 0.18 C_s alpha^3, d_C = 0.6 C_c (dE50/eV*) alpha, d_p = sqrt(((d_A^4+d_S^4)^(1.3/4) + d_I^1.3)^(2/1.3) + d_C^2)
    rss:  d_A = 1.22 lam/alpha, d_S = 0.5 C_s alpha^3, d_C = C_c (dE/eV*) alpha,   d_p = sqrt(d_A^2 + d_S^2 + d_C^2 + d_I^2)
"""
import math

from .core import C

INPUTS = ['C_s', 'C_c', 'B_r', 'dE', 'dE50', 'V_land', 'alpha', 'I_p', 'probe_convention']
OUTPUTS = ['d_p', 'd_I', 'd_A', 'd_S', 'd_C', 'alpha_opt', 'd_p_opt', 'spot_curve']


def vstar(V):
    return V * (1 + C['e'] * V / (2 * C['m_e'] * C['c'] ** 2))


def terms(p, alpha):
    Vs = vstar(p['V_land'])
    lam = C['h'] / math.sqrt(2 * C['m_e'] * C['e'] * Vs)
    rel = p['dE'] / (C['e'] * Vs)
    Bpr = p['B_r'] / math.log(2)
    dI = math.sqrt(4 * p['I_p'] / (math.pi * math.pi * Bpr * Vs * alpha * alpha))
    if p['probe_convention'] == 'rss':
        dA, dS, dC = 1.22 * lam / alpha, 0.5 * p['C_s'] * alpha ** 3, p['C_c'] * rel * alpha
        dp = math.sqrt(dA * dA + dS * dS + dC * dC + dI * dI)
    else:
        dA, dS, dC = 0.54 * lam / alpha, 0.18 * p['C_s'] * alpha ** 3, 0.6 * p['C_c'] * (p['dE50'] / (C['e'] * Vs)) * alpha
        inner = (dA ** 4 + dS ** 4) ** (1.3 / 4) + dI ** 1.3
        dp = math.sqrt(inner ** (2 / 1.3) + dC * dC)
    return dict(dA=dA, dS=dS, dC=dC, dI=dI, dp=dp)


def optimum(p):
    lo, hi = math.log(1e-4), math.log(1e-1)
    g = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
    f1, f2 = terms(p, math.exp(x1))['dp'], terms(p, math.exp(x2))['dp']
    for _ in range(80):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - g * (hi - lo)
            f1 = terms(p, math.exp(x1))['dp']
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + g * (hi - lo)
            f2 = terms(p, math.exp(x2))['dp']
    return math.exp((lo + hi) / 2)


def compute(p):
    t = terms(p, p['alpha'])
    aopt = optimum(p)
    curve = []
    for i in range(61):
        a = 1e-4 * 1000 ** (i / 60)
        q = terms(p, a)
        curve += [a, q['dA'], q['dS'], q['dC'], q['dI'], q['dp']]
    return dict(d_p=t['dp'], d_I=t['dI'], d_A=t['dA'], d_S=t['dS'], d_C=t['dC'], alpha_opt=aopt, d_p_opt=terms(p, aopt)['dp'], spot_curve=curve)
