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
lam_, Cs_ = sp.symbols('lambda C_s', positive=True)
ca = float(sp.simplify((aopt / (lam_ / Cs_) ** sp.Rational(1, 4)).subs({A: sp.Rational(122, 100) * lam_, Bc: Cs_ / 2})))
cd = float(sp.simplify((sp.sqrt(dmin2) / (lam_ ** sp.Rational(3, 4) * Cs_ ** sp.Rational(1, 4))).subs({A: sp.Rational(122, 100) * lam_, Bc: Cs_ / 2})))
check('P1', 'quadrature of A/α and Bα³ is smallest at α⁸ = A²/(3B²), where d² = (4/3)·3^(1/4)·A^(3/2)B^(1/2)',
      sp.simplify(aopt ** 8 - A ** 2 / (3 * Bc ** 2)) == 0 and sp.simplify(dmin2 - sp.Rational(4, 3) * 3 ** sp.Rational(1, 4) * A ** sp.Rational(3, 2) * Bc ** sp.Rational(1, 2)) == 0,
      'α_opt = (A²/3B²)^(1/8); with A = 1.22λ and B = C_s/2 (computed here): α_opt = %.4f (λ/C_s)^(1/4), d_min = %.4f λ^(3/4) C_s^(1/4)' % (ca, cd))
nums['P1_alpha_coef'], nums['P1_d_coef'] = ca, cd
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

# P6: Bronsgeest's I_AI = 1.08e-18 B from their Eqs. 6 and 19. Eq. 19 prints d_A = 0.66e-9 / (alpha sqrt(V)) (m, V); setting d_I = d_A in Eq. 6
# gives I_AI = (pi^2/4)(0.66e-9)^2 B. In units of lambda: 0.66e-9 sqrt(V)... lambda sqrt(V) = h / sqrt(2 m e) = 1.226e-9 m V^(1/2), so d_A = 0.538 lambda/alpha
lamV = C['h'] / math.sqrt(2 * C['m_e'] * C['e'])          # lambda * sqrt(V), non-relativistic, m V^(1/2)
I_AI = (math.pi ** 2 / 4) * 0.66e-9 ** 2
cA = 0.66e-9 / lamV
check('P6', 'Bronsgeest et al. quote I_AI = 1.08×10⁻¹⁸ B (source image as large as the diffraction disc); their Eqs. 6 and 19 reproduce it, and their Eq. 19 is d_A = 0.54 λ/α',
      abs(I_AI / 1.08e-18 - 1) < 5e-3 and abs(cA - 0.54) < 5e-3, 'Eqs. 6 and 19 give I_AI = %.4e B; 0.66 nm·V½ / (λ√V) = %.4f, so Eq. 19 is d_A = %.3f λ/α' % (I_AI, cA, cA))
nums['I_AI_coef'], nums['dA_coef_eq19'] = I_AI, cA

# P9: the half-current diameter of the Airy pattern, from its encircled current 1 - J0(v)^2 - J1(v)^2 with v = 2 pi alpha r / lambda
from scipy.special import j0, j1  # noqa: E402
from scipy.optimize import brentq  # noqa: E402
v50 = brentq(lambda v: 1 - j0(v) ** 2 - j1(v) ** 2 - 0.5, 0.5, 3.0)
cA50 = v50 / math.pi
fr066 = 1 - j0(0.66 * math.pi) ** 2 - j1(0.66 * math.pi) ** 2
check('P7', 'the diameter of the Airy disc that holds half the current is 0.535 λ/α (Eq. 19’s 0.54); a diameter of 0.66 λ/α would hold %.0f %%' % (100 * fr066),
      abs(cA50 - 0.535) < 1e-3, 'encircled current 1 − J₀² − J₁² = ½ at v = %.4f; d₅₀ = v/π · λ/α = %.4f λ/α' % (v50, cA50))
nums['airy_fw50_coef'], nums['airy_frac_066'] = cA50, fr066

# P10: the FW50 of spherical aberration at its best plane is 0.18 C_s alpha^3 (rays filling the aperture uniformly, the current in each ring prop. to alpha')
u = np.sqrt((np.arange(200000) + 0.5) / 200000)          # alpha'/alpha, uniform in area
best10 = (1e9, 0)
for dz in np.linspace(-1.0, 0.0, 2001):                  # units C_s = alpha = 1
    rr = np.abs(u * dz + u ** 3)
    w50 = 2 * np.median(rr)
    if w50 < best10[0]:
        best10 = (w50, dz)
check('P8', 'the half-current diameter of spherical aberration, at the plane where it is smallest, is 0.18 C_sα³ (Eq. 21)', abs(best10[0] - 0.18) < 5e-3,
      'smallest d₅₀ = %.4f C_sα³ at Δz = %.3f C_sα² (2001 planes, 200 000 rays uniform over the aperture)' % best10)
nums['sph_fw50_coef'] = best10[0]

# P7: FW50 of chapter 2's energy distribution (its module's own interpolated value) against a fine resampling of the same distribution
c2 = R2.compute(with_defaults(['r_t', 'V_ex', 'phi', 'T', 'p', 't_clean', 'k_f'], {'t_clean': 0.0}))
pp = with_defaults(['V_ex', 'r_t', 'k_f', 'phi', 'T'])
m = R2.emission_model(R2.tip_field(pp['V_ex'], pp['r_t'], pp['k_f']), pp['phi'], pp['T'])
w, P = np.asarray(m['w']), np.asarray(m['P'])
wf = np.linspace(w[0], w[-1], 16 * len(w))
Pf = np.interp(wf, w, P)
cdf = np.concatenate([[0], np.cumsum(0.5 * (Pf[1:] + Pf[:-1]) * np.diff(wf))])
cdf /= cdf[-1]
xs = np.interp(cdf + 0.5, cdf, wf, right=np.nan)
fw50_fine = np.nanmin(xs - wf) / R2.eV
fw50 = c2['dE50'] / R2.eV
fwhm = c2['dE'] / R2.eV
check('P9', 'FW50 (narrowest interval holding half the electrons) of chapter 2’s cold energy distribution: the module’s value against a 16 times finer resampling',
      abs(fw50 / fw50_fine - 1) < 5e-3, 'module FW50 %.4f eV, resampled %.4f eV; FWHM %.4f eV; FW50/FWHM %.3f' % (fw50, fw50_fine, fwhm, fw50 / fwhm))
nums['fw50_eV'], nums['fwhm_eV'], nums['fw50_over_fwhm'] = fw50, fwhm, fw50 / fwhm

# P8: Joy's worked example (Cs = Cc = 5 mm, 1 keV, dE = 0.7 eV, terms in quadrature with 0.61 lambda/alpha) gives about 18 nm at 5 mrad
Vj = R.vstar(1000.0)
lj = C['h'] / math.sqrt(2 * C['m_e'] * C['e'] * Vj)
aj = 5e-3
dj = math.sqrt((5e-3 * aj * 0.7 / Vj) ** 2 + (0.61 * lj / aj) ** 2 + (0.5 * 5e-3 * aj ** 3) ** 2)
joyf = lambda al: math.sqrt((5e-3 * al * 0.7 / Vj) ** 2 + (0.61 * lj / al) ** 2 + (0.5 * 5e-3 * al ** 3) ** 2)
ajs = np.exp(np.linspace(math.log(1e-3), math.log(2e-2), 20001))
dj_all = np.array([joyf(x) for x in ajs])
aj_opt, dj_opt = ajs[np.argmin(dj_all)], dj_all.min()
check('P10', 'Joy (2006) worked example: C_s = C_c = 5 mm, 1 keV, ΔE = 0.7 eV, α = 5 mrad, his three terms in quadrature give “about 18 nm”', abs(dj * 1e9 - 18) < 0.5,
      'recomputed %.2f nm at 5 mrad; his formulas are smallest at %.2f mrad, %.2f nm' % (dj * 1e9, aj_opt * 1e3, dj_opt * 1e9))
nums['joy_aopt_mrad'], nums['joy_dopt_nm'] = aj_opt * 1e3, dj_opt * 1e9
nums['joy_nm'] = dj * 1e9

out = {'checks': checks, 'numbers': nums, 'summary': '%d of %d checks pass' % (sum(c['ok'] for c in checks), len(checks))}
(HERE / 'data' / 'ch05').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch05' / 'derive_results.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
if __name__ == '__main__':
    for c in checks:
        print(('PASS ' if c['ok'] else 'FAIL ') + c['id'] + ' ' + c['title'] + ' :: ' + c['detail'])
    print(out['summary'])
    sys.exit(0 if all(c['ok'] for c in checks) else 1)
