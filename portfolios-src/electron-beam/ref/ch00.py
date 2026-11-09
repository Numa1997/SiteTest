"""Chapter 0 reference: the Abbe limit of light and the relativistic electron wavelength. Mirrors physics/ch00.js.

    d_opt    = lambda_opt / (2 NA)
    lambda_e = h / sqrt(2 m e V (1 + e V / (2 m c^2)))
"""
import numpy as np

from .core import C

INPUTS = ['V_acc', 'lambda_opt', 'NA', 'w_feat']
OUTPUTS = ['lambda_e', 'gamma', 'd_opt', 'ratio_opt', 'ratio_e']


def compute(p):
    eV = C['e'] * np.float64(p['V_acc'])                 # J
    mc2 = C['m_e'] * C['c'] ** 2                         # J
    gamma = 1 + eV / mc2
    pmom = np.sqrt(2 * C['m_e'] * eV * (1 + eV / (2 * mc2)))
    lambda_e = C['h'] / pmom
    d_opt = p['lambda_opt'] / (2 * p['NA'])
    return {'lambda_e': float(lambda_e), 'gamma': float(gamma), 'd_opt': float(d_opt),
            'ratio_opt': float(d_opt / p['w_feat']), 'ratio_e': float(lambda_e / p['w_feat'])}
