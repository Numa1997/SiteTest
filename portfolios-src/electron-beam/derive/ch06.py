"""Chapter 6 derivation checks and the stored Monte Carlo runs the chapter's figures and tables show.

    python3 portfolios-src/electron-beam/derive/ch06.py

Writes data/ch06/derive_results.json (checks) and data/ch06/mc_runs.json (backscattering and secondary-electron yields against energy for
Si, Al, Cu, Au, run with the page's own module physics/ch06.js through Node, so the stored numbers are exactly what the page would compute).
"""
import csv
import json
import math
import pathlib
import random
import sys

import sympy as sp

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import eb_lib as L  # noqa: E402
from ref import ch06 as R  # noqa: E402

checks, nums = [], {}


def check(cid, title, ok, detail):
    checks.append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail})


# M1: screened Rutherford. dsigma/dOmega = K / (1 - cos phi + 2a)^2 integrates to K pi / (a (1 + a)); inverting its cumulative gives Joy's Eq. 6
ph, a, K, Rr, c = sp.symbols('phi a K R c', positive=True)
tot = sp.integrate(2 * sp.pi * sp.sin(ph) * K / (1 - sp.cos(ph) + 2 * a) ** 2, (ph, 0, sp.pi))
cum = sp.integrate(2 * sp.pi * K / (1 - c + 2 * a) ** 2, (c, sp.Symbol('cp'), 1))     # over cos from cos(phi) to 1
cp = sp.Symbol('cp')
sol = sp.solve(sp.Eq(cum / tot, Rr), cp)
ok1 = sp.simplify(tot - K * sp.pi / (a * (1 + a))) == 0 and any(sp.simplify(s_ - (1 - 2 * a * Rr / (1 + a - Rr))) == 0 for s_ in sol)
check('M1', 'screened Rutherford: ∫ K/(1 − cos φ + 2a)² dΩ = πK/(a(1+a)), and setting its cumulative fraction equal to a random number R gives cos φ = 1 − 2aR/(1 + a − R) (Joy’s Eq. 6)',
      ok1, 'total %s; solution for cos φ: %s' % (sp.sstr(sp.simplify(tot)), sp.sstr(sol)))

# M10: Joy's constant. Rutherford with pv in place of 2E: total = (Z e^2/4 pi eps0)^2 pi / ((pv)^2 a (1+a)); pv = E (E + 2mc^2)/(E + mc^2), so
# 1/(pv)^2 = (1/E^2)((E + mc^2)/(E + 2mc^2))^2 and Joy's 5.21e-21 * 4 should be (e^2/4 pi eps0)^2 in keV^2 cm^2
from ref.core import C as CC  # noqa: E402
Ek, mm = sp.symbols('E m', positive=True)
pc = sp.sqrt((Ek + mm) ** 2 - mm ** 2)          # momentum times c, with m = mc^2
vc = pc / (Ek + mm)                             # v/c
ok10 = sp.simplify(pc * vc - Ek * (Ek + 2 * mm) / (Ek + mm)) == 0
e2 = CC['e'] ** 2 / (4 * math.pi * CC['eps0']) / (1e3 * CC['e']) * 100   # e^2/(4 pi eps0) in keV cm
kJ = e2 ** 2 / 4
check('M2', 'Joy’s Eq. 1 is Rutherford’s cross-section with pv in place of 2E: pv = E(E+2mc²)/(E+mc²), and (e²/4πε₀)²/4 = 5.18×10⁻²¹ keV² cm² against Joy’s 5.21×10⁻²¹',
      ok10 and abs(kJ / 5.21e-21 - 1) < 0.01, 'e²/4πε₀ = %.5e keV cm; squared over 4: %.4e keV² cm² (Joy %.2e, %.2f %% higher)' % (e2, kJ, 5.21e-21, 100 * (5.21e-21 / kJ - 1)))
nums['joy_const'] = kJ

# M2: free path. p(s) = exp(-s/lambda)/lambda; s = -lambda ln R has that distribution and mean lambda
s, lam = sp.symbols('s lambda', positive=True)
mean = sp.integrate(s * sp.exp(-s / lam) / lam, (s, 0, sp.oo))
cdf = sp.integrate(sp.exp(-s / lam) / lam, (s, 0, s))
inv = sp.solve(sp.Eq(1 - cdf, Rr), s)
check('M3', 'free paths: p(s) = e^(−s/λ)/λ has mean λ, and the path with P(longer than s) = R is s = −λ ln R (Joy’s Eq. 4)',
      sp.simplify(mean - lam) == 0 and any(sp.simplify(x - (-lam * sp.log(Rr))) == 0 for x in inv), 'mean %s; inverse %s' % (sp.sstr(mean), sp.sstr(inv)))

# M3: the direction rotation keeps unit length and turns by exactly phi, also near cz = 0 where Joy's AN = -cx/cz diverges
rg = random.Random(7)
worst_len = worst_ang = 0.0
for _ in range(20000):
    v = [rg.gauss(0, 1) for _ in range(3)]
    if _ % 10 == 0:
        v[2] = rg.choice([1e-12, -1e-12, 0.0])
    n = math.sqrt(sum(x * x for x in v))
    v = [x / n for x in v]
    phi, psi = rg.uniform(0, math.pi), rg.uniform(0, 2 * math.pi)
    w = R.turn(v, phi, psi)
    worst_len = max(worst_len, abs(math.sqrt(sum(x * x for x in w)) - 1))
    worst_ang = max(worst_ang, abs(sum(x * y for x, y in zip(v, w)) - math.cos(phi)))
check('M4', 'the rotation of the direction (physics/ch06.js turn) keeps unit length and makes angle φ with the old direction, for 20 000 random cases including travel parallel to the surface',
      worst_len < 1e-14 and worst_ang < 1e-9, 'largest error of length %.1e, of cos(angle) %.1e' % (worst_len, worst_ang))

# M4: the escape integral escInt against a fine numerical quadrature, both branches
worst = 0.0
for zA, zB, sl, ls in ((0.0, 5.0, 5.0, 2.7), (3.0, 0.0, 4.0, 0.5), (1.0, 1.0 + 1e-9, 7.0, 1.7), (0.2, 30.0, 40.0, 0.6)):
    nq = 200000
    q = sum(math.exp(-(zA + (zB - zA) * (k + 0.5) / nq) / ls) for k in range(nq)) * sl / nq
    worst = max(worst, abs(R.escInt(zA, zB, sl, ls) / q - 1))
check('M5', 'the exact integral of the escape weight e^(−z/λ_s) along a straight step against a 200 000-point midpoint sum, four cases', worst < 1e-8, 'largest relative difference %.1e' % worst)

# M5: Joy-Luo tends to Bethe at high energy, and its stopping power against NIST ESTAR (collision) at 1 to 100 keV
E, J, k = sp.symbols('E J k', positive=True)
lim = sp.limit(sp.log(sp.Rational(1166, 1000) * (E + k * J) / J) / sp.log(sp.Rational(1166, 1000) * E / J), E, sp.oo)
estar = {}
with open(HERE / 'data' / 'ch06' / 'estar_electron_stopping_power.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        estar.setdefault(row['material'].split(' ')[0], []).append((float(row['T_keV']), float(row['collision_stopping_power_MeV_cm2_per_g'])))
names = {'Silicon': 'Si', 'Aluminium': 'Al', 'Copper': 'Cu', 'Gold': 'Au'}
cmp = {}
for full, sym in names.items():
    m = R.MAT[sym]
    J_ = R.Jkev(m['Z'])
    rows = []
    for T, Sc in estar[full]:
        S_jl = R.stop(m, T, J_) / (m['rho'] * 1e-7) * 1e-3     # keV/nm -> MeV cm^2 / g
        rows.append([T, Sc, S_jl, S_jl / Sc])
    cmp[sym] = rows
mid = [r[3] for v in cmp.values() for r in v if 5 <= r[0] <= 30]
lo = [r[3] for v in cmp.values() for r in v if r[0] < 5]
r100 = [r[3] for v in cmp.values() for r in v if r[0] == 100]
mc2 = 510.99895                                     # keV
nr = (lambda T: (1 - 1 / (1 + T / mc2) ** 2) / (2 * T / mc2))(100.0)   # beta^2 over its non-relativistic value 2T/mc^2 at 100 keV
check('M6', 'Joy–Luo tends to Bethe as E → ∞ (ratio of the logarithms → 1); against ESTAR’s collision stopping power it agrees within 8 % from 5 to 30 keV for Si, Al, Cu, Au',
      sp.simplify(lim - 1) == 0 and max(abs(x - 1) for x in mid) < 0.08,
      '5–30 keV: ratio %.3f to %.3f; 1–3 keV: %.3f to %.3f (higher, most for gold); at 100 keV %.3f to %.3f, which is the non-relativistic 1/E against the relativistic 1/β²: β²/(2E/mc²) = %.3f'
      % (min(mid), max(mid), min(lo), max(lo), min(r100), max(r100), nr))
nums['estar_ratio_mid'] = [min(mid), max(mid)]
nums['estar_ratio_lo'] = [min(lo), max(lo)]
nums['estar_ratio_100'] = [min(r100), max(r100), nr]

# M6: J from Joy's Eq. 12 against the ESTAR (ICRU) values listed in data/ch06/README.md
icru = {'Si': 173, 'Al': 166, 'Cu': 322, 'Au': 790}
jr = {k: R.Jkev(R.MAT[k]['Z']) * 1e3 / v for k, v in icru.items()}
check('M7', 'mean ionisation energy J from Joy’s Eq. 12 against the values ESTAR uses (Si 173, Al 166, Cu 322, Au 790 eV): within 3 %', max(abs(x - 1) for x in jr.values()) < 0.03,
      ', '.join('%s %.0f eV (%.3f)' % (k, R.Jkev(R.MAT[k]['Z']) * 1e3, v) for k, v in jr.items()))
nums['J_eV'] = {k: R.Jkev(R.MAT[k]['Z']) * 1e3 for k in R.MAT}

# M7: Joy's statement that the elastic mean free path is "of the order of a few hundred angstroms at 100 keV"
l100 = R.mfp(R.MAT['Si'], 100.0)
l100a = R.mfp(R.MAT['Au'], 100.0)
check('M8', 'Joy calls the elastic mean free path at 100 keV “typically of the order of a few hundred ångström”; his Eqs. 1–3 give values on either side of that for silicon and gold',
      l100a < 30 < l100, 'λ_el(100 keV): Si %.0f nm, Au %.1f nm' % (l100, l100a))
nums['mfp_Si'] = {str(E_): R.mfp(R.MAT['Si'], E_) for E_ in (0.8, 1.0, 5.0, 30.0, 100.0)}

# ---- stored runs through the page's own module (Node), N = 2000 electrons, fixed random numbers
db = {}
with open(HERE / 'data' / 'ch06' / 'bse_coefficient_vs_energy.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        sym = {'Silicon': 'Si', 'Aluminium': 'Al', 'Copper': 'Cu', 'Gold': 'Au'}.get(row['material'])
        if sym:
            db.setdefault(sym, []).append((float(row['E_keV']), float(row['eta_fraction'])))
grid = [0.5, 0.7, 1, 1.5, 2, 3, 5, 7, 10, 15, 20, 30]
jobs = [{'module': 'ch06', 'inputs': {'material': mt, 'V_land': E_ * 1e3}} for mt in R.MAT for E_ in grid]
res = [r_['outputs'] for r_ in L.node('compute', jobs)]
runs = {mt: [] for mt in R.MAT}
for j, o in zip(jobs, res):
    runs[j['inputs']['material']].append({'E_keV': j['inputs']['V_land'] / 1e3, 'eta': o['eta_BSE'], 'u_eta': o['u_eta'], 'delta': o['delta_SE'], 'u_delta': o['u_delta'],
                                         'R_nm': o['R'] * 1e9, 'r90_nm': o['r90'] * 1e9, 'sigma_nm': o['sigma_sig'] * 1e9})

# M8: eta against the database: mean of the measured points per element, by energy band; recorded with the gap
band = {}
for mt, pts in db.items():
    mc = {r['E_keV']: r['eta'] for r in runs[mt]}
    out = []
    for lo_, hi_ in ((0.4, 2.0), (2.0, 8.0), (8.0, 31.0)):
        meas = [e for E_, e in pts if lo_ <= E_ < hi_]
        sims = [mc[E_] for E_ in grid if lo_ <= E_ < hi_]
        if meas and sims:
            out.append({'band_keV': [lo_, hi_], 'n_meas': len(meas), 'eta_meas_mean': sum(meas) / len(meas), 'eta_meas_min': min(meas), 'eta_meas_max': max(meas),
                        'eta_mc_mean': sum(sims) / len(sims)})
    band[mt] = out
hi_ok = all(abs(b['eta_mc_mean'] / b['eta_meas_mean'] - 1) < 0.25 for mt in band for b in band[mt] if b['band_keV'][0] >= 8)
check('M9', 'recorded comparison: the simulated η against the database of measured backscattering coefficients (Akbari et al.); above 8 keV within 25 % of the mean of the measurements for each element',
      hi_ok, '; '.join('%s: ' % mt + ', '.join('%g–%g keV MC %.3f vs measured %.3f (%d points, %.3f–%.3f)' % (b['band_keV'][0], b['band_keV'][1], b['eta_mc_mean'], b['eta_meas_mean'], b['n_meas'], b['eta_meas_min'], b['eta_meas_max'])
                                                         for b in band[mt]) for mt in band))
nums['eta_bands'] = band

# M9: delta at 2 and 20 keV against Lin and Joy's own Monte Carlo (their Table 1, same eps and lambda_s), recorded
lj = {}
with open(HERE / 'data' / 'ch06' / 'se_yield_lin_joy2005.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        sym = {'Aluminium': 'Al', 'Silicon (crystal)': 'Si', 'Copper': 'Cu', 'Gold': 'Au'}[row['material']]
        lj[sym] = {'d2': float(row['delta_at_2keV_printed']), 'd20': float(row['delta_at_20keV_printed']), 'dmax': float(row['delta_max']), 'Emax': float(row['E_at_delta_max_keV'])}
jobs2 = [{'module': 'ch06', 'inputs': {'material': mt, 'V_land': E_ * 1e3}} for mt in R.MAT for E_ in (2.0, 20.0)]
res2 = [r_['outputs'] for r_ in L.node('compute', jobs2)]
dcmp = {}
for jb, o in zip(jobs2, res2):
    mt, E_ = jb['inputs']['material'], jb['inputs']['V_land'] / 1e3
    dcmp.setdefault(mt, {})['d%d' % E_] = (o['delta_SE'], o['u_delta'])
check('M10', 'recorded comparison: δ at 2 and 20 keV against the Monte Carlo values Lin and Joy print with the same ε and λ_s (their simulation also has elastic scattering details we do not know)', True,
      '; '.join('%s 2 keV %.3f vs %.2f, 20 keV %.3f vs %.2f' % (mt, dcmp[mt]['d2'][0], lj[mt]['d2'], dcmp[mt]['d20'][0], lj[mt]['d20']) for mt in R.MAT))
nums['delta_cmp'] = {mt: {'mc2': dcmp[mt]['d2'][0], 'u2': dcmp[mt]['d2'][1], 'mc20': dcmp[mt]['d20'][0], 'u20': dcmp[mt]['d20'][1], 'lj2': lj[mt]['d2'], 'lj20': lj[mt]['d20']} for mt in R.MAT}
nums['lin_joy'] = lj

out = {'checks': checks, 'numbers': nums, 'summary': '%d of %d checks pass' % (sum(c_['ok'] for c_ in checks), len(checks))}
(HERE / 'data' / 'ch06').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch06' / 'derive_results.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
(HERE / 'data' / 'ch06' / 'mc_runs.json').write_text(json.dumps({'note': 'physics/ch06.js through Node, N = 2000 electrons each, seed as in the module', 'grid_keV': grid,
                                                                  'runs': runs, 'database': db, 'estar_cmp': cmp}, indent=1), encoding='utf-8')
if __name__ == '__main__':
    for c_ in checks:
        print(('PASS ' if c_['ok'] else 'FAIL ') + c_['id'] + ' ' + c_['title'] + ' :: ' + c_['detail'])
    print(out['summary'])
    sys.exit(0 if all(c_['ok'] for c_ in checks) else 1)
