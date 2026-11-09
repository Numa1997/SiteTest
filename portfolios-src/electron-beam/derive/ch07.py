"""Chapter 7 derivation checks. Writes data/ch07/derive_results.json; the page shows the table.

    python3 portfolios-src/electron-beam/derive/ch07.py
"""
import json
import math
import pathlib
import sys

import sympy as sp

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from ref import ch07 as R  # noqa: E402
from ref.core import with_defaults  # noqa: E402

checks, nums = [], {}


def check(cid, title, ok, detail):
    checks.append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail})


# C1: compound Poisson. N ~ Poisson(n), each contributes K ~ Poisson(m): E = n m, Var = n (m + m^2) (law of total variance)
n, m = sp.symbols('n m', positive=True)
EK, VK = m, m                       # mean and variance of one Poisson(m)
EN, VN = n, n
mean = EN * EK
var = EN * VK + VN * EK ** 2
check('C1', 'counts per pixel: beam electrons Poisson with mean n̄, each giving a Poisson number of collected secondaries with mean m; the total has mean n̄m and variance n̄(m + m²)',
      sp.simplify(var - n * (m + m ** 2)) == 0 and sp.simplify(mean - n * m) == 0, 'law of total variance: E[N]Var[K] + Var[N]E[K]² = n̄m(1 + m)')

# C2: a 2-D Gaussian probe holds half its current inside the diameter 2 sqrt(2 ln 2) sigma, which is also its FWHM
s, r = sp.symbols('sigma r', positive=True)
frac = sp.integrate(sp.exp(-r ** 2 / (2 * s ** 2)) * r, (r, 0, sp.Symbol('R'))) / sp.integrate(sp.exp(-r ** 2 / (2 * s ** 2)) * r, (r, 0, sp.oo))
R50 = sp.solve(sp.Eq(frac, sp.Rational(1, 2)), sp.Symbol('R'))
fwhm = 2 * sp.sqrt(2 * sp.log(2)) * s
check('C2', 'a round Gaussian probe of standard deviation σ per axis holds half its current inside the diameter 2√(2 ln 2) σ = 2.355σ, equal to its FWHM, so σ_p = d_p/2.355',
      any(sp.simplify(2 * x - fwhm) == 0 for x in R50), 'half the current lies inside the radius R₅₀ = σ√(2 ln 2)')

# C3: the sidewall excess delta h (1/cos b - tan b) -> delta h as b -> 0, and equals delta (1/sin b - 1) w with w = h tan b
b_, h_, d_ = sp.symbols('beta h delta', positive=True)
ex1 = d_ * (1 / sp.sin(b_) - 1) * h_ * sp.tan(b_)
check('C3', 'secant law on the sidewall: the excess δ(1/sin β − 1)·h tan β equals δh(1/cos β − tan β) and tends to δh for a vertical wall',
      sp.simplify(ex1 - d_ * h_ * (1 / sp.cos(b_) - sp.tan(b_))) == 0 and sp.limit(ex1, b_, 0) == d_ * h_, 'limit β → 0: %s' % sp.sstr(sp.limit(ex1, b_, 0)))

# C4: the erf approximation (Abramowitz and Stegun 7.1.26) against math.erf
worst = max(abs(R.erf(x / 100) - math.erf(x / 100)) for x in range(-600, 601))
check('C4', 'the error function used for the blurred profile (Abramowitz and Stegun 7.1.26) against the library erf on −6 ≤ x ≤ 6', worst < 1.5e-7, 'largest difference %.1e' % worst)

# C5: the 1/sqrt law. sigma_CD against dwell time, current and lines averaged, in the high-count regime (slopes on log-log axes)
p0 = with_defaults(R.INPUTS)
def sig(**kw):
    return R.compute(dict(p0, **kw))['sigma_CD']
sl = {}
for k, a, b in (('t_d', 1e-6, 1e-5), ('I_p', 1e-10, 1e-9), ('N_px', 1024, 4096)):
    sl[k] = math.log(sig(**{k: b}) / sig(**{k: a})) / math.log(b / a)
check('C5', 'σ_CD falls as the inverse square root of the dwell time, the current and the number of lines averaged (log-log slopes, at high counts per pixel)',
      all(abs(v + 0.5) < 0.02 for v in sl.values()), ', '.join('%s %.3f' % kv for kv in sl.items()))
nums['slopes'] = sl

# C6: error propagation against the Monte Carlo of the same algorithm, at several settings
cmp = []
for kw in ({}, {'t_d': 1e-6}, {'t_d': 1e-8}, {'N_px': 128}, {'sidewall': 0.0, 'height': 5e-8, 'cd': 1.5e-8}):
    o = R.compute(dict(p0, **kw))
    cmp.append((kw, o['sigma_CD'], o['sigma_CD_mc']))
ratios = [b / a for _, a, b in cmp]
ob = R.compute(dict(p0, d_p=1.5e-8))
check('C6', 'σ_CD by first-order error propagation against the standard deviation of 4000 noisy repeats of the same measurement: within 20 % where the edges stand well out of the floor (the Monte Carlo carries about 1 %)',
      all(abs(x - 1) < 0.20 for x in ratios), '; '.join('%s: %.3f vs %.3f nm' % (json.dumps(kw) if kw else 'default', a * 1e9, b * 1e9) for kw, a, b in cmp)
      + '. Not within 20 %%: the 15 nm probe of Example 7.4 (edge contrast 14 %%), %.3f vs %.3f nm' % (ob['sigma_CD'] * 1e9, ob['sigma_CD_mc'] * 1e9))
nums['ep_vs_mc'] = [[json.dumps(kw), a, b] for kw, a, b in cmp]

# C7: the bias of the threshold method grows with the blur; with a sharp probe and no signal spread it tends to the bottom width
o0 = R.compute(p0)
osh = R.compute(dict(p0, d_p=1e-10, sig_core=1e-10, f_core=1.0, sig_halo=1e-10, px=2.5e-10))
bottom = p0['cd'] + p0['height'] * math.tan(p0['sidewall'])
check('C7', 'with a sharp probe and no spread of the signal the outer-flank threshold finds the bottom corners of the line (width CD + h tan β), within a pixel',
      abs(osh['CD_meas'] - bottom) < 2.5e-10, 'sharp: %.3f nm against the bottom width %.3f nm; default blur: %.2f nm for a true CD of %.1f nm' % (osh['CD_meas'] * 1e9, bottom * 1e9, o0['CD_meas'] * 1e9, p0['cd'] * 1e9))
nums['cd_sharp'], nums['bottom'], nums['cd_default'] = osh['CD_meas'], bottom, o0['CD_meas']

# C8: dose arithmetic
check('C8', 'dose: n̄ = I_p t_d / e electrons per pixel and D = I_p t_d / Δx² (1 C m⁻² = 100 µC cm⁻²)', abs(o0['dose'] * p0['px'] ** 2 / 1.602176634e-19 - o0['n_pe']) < 1e-9 * o0['n_pe'],
      'n̄ = %.3f, D = %.1f µC cm⁻²' % (o0['n_pe'], o0['dose'] * 100))

out = {'checks': checks, 'numbers': nums, 'summary': '%d of %d checks pass' % (sum(c['ok'] for c in checks), len(checks))}
(HERE / 'data' / 'ch07').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch07' / 'derive_results.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
if __name__ == '__main__':
    for c in checks:
        print(('PASS ' if c['ok'] else 'FAIL ') + c['id'] + ' ' + c['title'] + ' :: ' + c['detail'])
    print(out['summary'])
    sys.exit(0 if all(c['ok'] for c in checks) else 1)
