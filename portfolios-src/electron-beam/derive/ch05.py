"""Chapter 5 derivation checks (SymPy and numerics). Writes data/ch05/derive_results.json; the page shows the table.

    python3 portfolios-src/electron-beam/derive/ch05.py
"""
import importlib.util
import json
import math
import pathlib
import sys

import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from ref import ch05 as R  # noqa: E402
from ref.core import C, with_defaults  # noqa: E402

_s = importlib.util.spec_from_file_location('r2', HERE / 'ref' / 'ch02.py')
R2 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R2)

checks, nums = [], {}


def check(cid, title, ok, detail):
    checks.append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail})


a, A, Bc, K = sp.symbols('alpha A B K', positive=True)
# P1: diffraction (A/alpha) and spherical (B alpha^3) in quadrature
f = (A / a) ** 2 + (B_ := Bc * a ** 3) ** 2
aopt = sp.solve(sp.diff(f, a), a)
aopt = [x for x in aopt if x.is_positive][0]
dmin2 = sp.simplify(f.subs(a, aopt))
check('P1', 'quadrature of A/α and Bα³ is smallest at α⁸ = A²/(3B²), where d² = (4/3)·3^(1/4)·A^(3/2)B^(1/2)',
      sp.simplify(aopt ** 8 - A ** 2 / (3 * Bc ** 2)) == 0 and sp.simplify(dmin2 - sp.Rational(4, 3) * 3 ** sp.Rational(1, 4) * A ** sp.Rational(3, 2) * Bc ** sp.Rational(1, 2)) == 0,
      'α_opt = (A²/3B²)^(1/8); with A = 1.22λ, B = C_s/2: α_opt ≈ 1.0(λ/C_s)^(1/4), d_min ≈ 0.93 λ^(3/4) C_s^(1/4)')
# P2: diffraction and chromatic in quadrature
g = (A / a) ** 2 + (K * a) ** 2
ao2 = [x for x in sp.solve(sp.diff(g, a), a) if x.is_positive][0]
check('P2', 'quadrature of A/α and Kα is smallest at α = √(A/K), where d = √(2AK)', sp.simplify(ao2 - sp.sqrt(A / K)) == 0 and sp.simplify(g.subs(a, ao2) - 2 * A * K) == 0,
      'K = C_c ΔE/(eV*): at low voltage the optimum is set by chromatic aberration and diffraction')

# P3: the disc of least confusion of spherical aberration has diameter C_s alpha^3 / 2 (rays filling the cone up to alpha), at a defocus of -3/4 C_s alpha^2
Cs, al = 1.0, 1.0
ang = np.linspace(-al, al, 20001)
best = (1e9, 0)
for dz in np.linspace(-1.0, 0.0, 4001):
    r = ang * dz + Cs * ang ** 3            # radial miss in a plane dz from the paraxial image (units: Cs = alpha = 1)
    wdt = r.max() - r.min()
    if wdt < best[0]:
        best = (wdt, dz)
check('P3', 'brute force: the narrowest beam cross-section of rays r = α′Δz + C_sα′³ (|α′| ≤ α) is C_sα³/2 wide, at Δz = −¾C_sα²',
      abs(best[0] - 0.5) < 1e-3 and abs(best[1] + 0.75) < 1e-3, 'width %.4f C_sα³ at Δz = %.4f C_sα² (scanned 4001 planes, 20001 rays)' % best)

# P4: numeric optimum of the module equals the closed form of P1 when only diffraction and spherical remain (rss, I_p and C_c tiny)
p = with_defaults(R.INPUTS)
q = dict(p, probe_convention='rss', I_p=1e-30, C_c=1e-12)
Vs = R.vstar(p['V_land'])
lam = C['h'] / math.sqrt(2 * C['m_e'] * C['e'] * Vs)
Aa, Bb = 1.22 * lam, 0.5 * p['C_s']
ao_cf = (Aa ** 2 / (3 * Bb ** 2)) ** 0.125
ao_num = R.optimum(q)
check('P4', 'the solver’s golden-section optimum equals the closed form of P1 (rss, no chromatic term, no source image)', abs(ao_num / ao_cf - 1) < 1e-7,
      'numeric %.6f mrad, closed form %.6f mrad' % (ao_num * 1e3, ao_cf * 1e3))
q2 = dict(p, probe_convention='rss', I_p=1e-30, C_s=1e-12)
K_ = p['C_c'] * p['dE'] / (C['e'] * Vs)
ao2_num = R.optimum(q2)
check('P5', 'and the closed form of P2 when only diffraction and chromatic remain', abs(ao2_num / math.sqrt(Aa / K_) - 1) < 1e-7,
      'numeric %.6f mrad, closed form %.6f mrad' % (ao2_num * 1e3, math.sqrt(Aa / K_) * 1e3))
nums['aopt_sph_cf_mrad'] = ao_cf * 1e3
nums['aopt_chr_cf_mrad'] = math.sqrt(Aa / K_) * 1e3

# P6: Bronsgeest's I_AI = 1.08e-18 B against their own Eqs. 6 and 19
B_, I_, d_ = sp.symbols('B I d', positive=True)
lamV = (C['h'] ** 2 / (2 * C['m_e'] * C['e']))           # lambda^2 V (non-relativistic), m^2 V
I_AI = (math.pi ** 2 / 4) * 0.66 ** 2 * lamV          # I_p with d_I = d_A, per unit brightness
I_AI12 = (math.pi ** 2 / 4) * 0.66 ** 2 * (1.2e-9) ** 2            # with their rounded lambda = 1.2 nm / sqrt(V)
check('P6', 'recorded, not a test: Bronsgeest et al. quote I_AI = 1.08×10⁻¹⁸ B (source image as large as the diffraction disc); their Eqs. 6 and 19 give (π²/4)(0.66)²λ²V B',
      True, 'Eqs. 6 and 19 give %.3e B (exact λ) or %.3e B (their 1.2 nm·V½); the quoted value is %.3f of the latter, close to ln 2 = 0.693, as if it counted only the current inside the FW50 disc' % (I_AI, I_AI12, 1.08e-18 / I_AI12))
nums['I_AI_coef'] = I_AI

# P7: FW50 width of chapter 2's energy distribution against its FWHM (cold working point of the contract defaults)
m = R2.emission_model(4e9, 4.5 * R2.eV, 300.0)
w, P = np.asarray(m['w']), np.asarray(m['P'])
cdf = np.concatenate([[0], np.cumsum(0.5 * (P[1:] + P[:-1]) * np.diff(w))])
cdf /= cdf[-1]
best = 1e9
for i in range(len(w)):
    j = np.searchsorted(cdf, cdf[i] + 0.5)
    if j >= len(w):
        break
    best = min(best, w[j] - w[i])
fw50 = best / R2.eV
fwhm = m['fwhm'] / R2.eV
check('P7', 'FW50 (narrowest interval holding half the electrons) of chapter 2’s cold energy distribution against its FWHM', True,
      'FW50 %.4f eV, FWHM %.4f eV, ratio %.3f' % (fw50, fwhm, fw50 / fwhm))
nums['fw50_eV'], nums['fwhm_eV'], nums['fw50_over_fwhm'] = fw50, fwhm, fw50 / fwhm

# P8: Joy's worked example (Cs = Cc = 5 mm, 1 keV, dE = 0.7 eV, terms in quadrature with 0.61 lambda/alpha) gives about 18 nm at 5 mrad
Vj = R.vstar(1000.0)
lj = C['h'] / math.sqrt(2 * C['m_e'] * C['e'] * Vj)
aj = 5e-3
dj = math.sqrt((5e-3 * aj * 0.7 / Vj) ** 2 + (0.61 * lj / aj) ** 2 + (0.5 * 5e-3 * aj ** 3) ** 2)
check('P8', 'Joy (2006) worked example: C_s = C_c = 5 mm, 1 keV, ΔE = 0.7 eV, α = 5 mrad, his three terms in quadrature give “about 18 nm”', abs(dj * 1e9 - 18) < 0.5,
      'recomputed %.2f nm' % (dj * 1e9))
nums['joy_nm'] = dj * 1e9

out = {'checks': checks, 'numbers': nums, 'summary': '%d of %d checks pass' % (sum(c['ok'] for c in checks), len(checks))}
(HERE / 'data' / 'ch05').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch05' / 'derive_results.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
if __name__ == '__main__':
    for c in checks:
        print(('PASS ' if c['ok'] else 'FAIL ') + c['id'] + ' ' + c['title'] + ' :: ' + c['detail'])
    print(out['summary'])
    sys.exit(0 if all(c['ok'] for c in checks) else 1)
