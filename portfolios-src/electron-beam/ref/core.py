"""Constants, units and number formatting of the Python reference; mirrors physics/core.js value for value.

Constants: CODATA 2018 (E. Tiesinga et al., Rev. Mod. Phys. 93, 025010 (2021); https://physics.nist.gov/cuu/Constants/).
c, h, e, k_B and N_A are exact since the SI redefinition of 20 May 2019. checks/check_parity.py fails if a value here differs
from physics/core.js by more than one part in 10^15.
"""
import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parents[1]

C = {
    'c': 299792458.0,            # m/s (exact)
    'h': 6.62607015e-34,         # J s (exact)
    'e': 1.602176634e-19,        # C (exact)
    'k_B': 1.380649e-23,         # J/K (exact)
    'N_A': 6.02214076e23,        # 1/mol (exact)
    'm_e': 9.1093837015e-31,     # kg
    'eps0': 8.8541878128e-12,    # F/m
    'mu0': 1.25663706212e-6,     # N/A^2
    'u': 1.66053906660e-27,      # kg
    'a0': 5.29177210903e-11,     # m
    'alpha_fs': 7.2973525693e-3,  # 1
}
D = {
    'hbar': C['h'] / (2 * math.pi),
    'e_over_m': C['e'] / C['m_e'],
    'mc2': C['m_e'] * C['c'] * C['c'],
    'mc2_eV': C['m_e'] * C['c'] * C['c'] / C['e'],
    'A_R': 4 * math.pi * C['m_e'] * C['e'] * C['k_B'] ** 2 / C['h'] ** 3,
}
U = {
    'eV': C['e'], 'keV': 1e3 * C['e'],
    'nm': 1e-9, 'pm': 1e-12, 'um': 1e-6, 'mm': 1e-3,
    'mbar': 100.0, 'Torr': 101325 / 760, 'hour': 3600.0, 'deg': math.pi / 180, 'zeroC': 273.15,
}

SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def fmt(x, sig=3):
    """x to `sig` significant figures: plain decimals between 1e-3 and 1e5, otherwise 'm × 10ⁿ'. Same rule as core.js fmt."""
    if not math.isfinite(x):
        return str(x)
    if x == 0:
        return '0'
    neg = x < 0
    x = abs(x)
    e = math.floor(math.log10(x))
    m = x / 10 ** e
    ms = '%.*f' % (sig - 1, m)
    if float(ms) >= 10:
        e += 1
        m /= 10
        ms = '%.*f' % (sig - 1, m)
    if -3 <= e < 5:
        s = '%.*f' % (max(0, sig - 1 - e), float(ms) * 10 ** e)
    else:
        s = ms + ' × 10' + str(e).translate(SUP)
    return ('−' if neg else '') + s


def fmt_tex(x, sig=3):
    """The same number as TeX: 3.70, or 1.23\\times10^{-9}."""
    s = fmt(x, sig)
    if ' × 10' in s:
        m, ex = s.split(' × 10')
        ex = ex.translate(str.maketrans('⁻⁰¹²³⁴⁵⁶⁷⁸⁹', '-0123456789'))
        return m.replace('−', '-') + r'\times10^{' + ex + '}'
    return s.replace('−', '-')


def contract():
    return json.loads((HERE / 'contract.json').read_text(encoding='utf-8'))


def with_defaults(names, p=None):
    """Fill a module's inputs with the contract defaults, as core.js withDefaults does."""
    sym = contract()['symbols']
    out = {}
    for k in names:
        if k not in sym:
            raise KeyError('symbol not in contract.json: ' + k)
        out[k] = (p or {}).get(k, sym[k].get('default'))
        if out[k] is None:
            raise KeyError('no value and no default for ' + k)
    return out
