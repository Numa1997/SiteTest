"""The Electron Beam, from Tip to Measurement · text/ch01.py · chapter 1, A free electron in fields.

The words, figures and quoted numbers of chapter 1, in the form eb_lib.py builds (the dict CH at the end). Session S3.

Every number the prose quotes is declared in NUMS below as a module output (physics/ch01.js, physics/ch00.js, run through
the page's own JavaScript by the build and through ref/ch01.py by checks/check_numbers.py) or as an expression of other numbers.
Quantities that are givens of the problem (the plate gap, the anode voltage) or constants of nature (CODATA 2018, from ref/core.py) are
named numbers too. The prose is written in a plainer markup, kept from the first draft of the chapter, and converted at import time
by `convert()`: \\( \\) and \\[ \\] to $ $ and $$ $$, equation labels, figure places, and each ‹n:name|digits› to a {{num:..}} or {{numtex:..}}
with that many significant figures. Figures are drawn here from the same reference solver (ref/ch01.py) and the data in data/ch01/.
"""
import importlib.util
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
if EB not in sys.path:
    sys.path.insert(0, EB)
from ref import ch00 as R0, ch01 as R, core as RC  # noqa: E402

C = RC.C


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DERIVE = _load('eb_derive_ch01', os.path.join('..', 'derive', 'ch01.py'))
DATA = json.load(open(os.path.join(EB, 'data', 'ch01', 'thomson1897.json'), encoding='utf-8'))

# ============================================================================================================ numbers
NUMS = {}


def mod(name, inputs, out, module='ch01', scale=1, sig=3):
    NUMS[name] = {'module': module, 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, scale=1, sig=3):
    """A given of the problem or a constant: a name for a typed value, with its source in the comment at the call."""
    ex(name, repr(float(value)), {}, scale, sig)


# --- constants of nature (CODATA 2018, as in ref/core.py)
for _n, _k in (('c_', 'c'), ('e_', 'e'), ('m_', 'm_e'), ('h_', 'h'), ('eps0_', 'eps0'), ('mu0_', 'mu0')):
    const(_n, C[_k])
ex('e_over_m', 'e/m', {'e': 'e_', 'm': 'm_'})

# --- the tube of the worked example: the anode voltage, the plates (Thomson's plates were about 5 cm long and 1.5 cm apart), the drift to the screen
VA, VP, D_GAP, L_PL, L_DRIFT = 2000.0, 100.0, 0.015, 0.05, 0.19      # givens of the model tube
const('Va', VA, sig=4)
const('Vp', VP)
const('d_gap', D_GAP)
const('l_pl', L_PL)
const('L_drift', L_DRIFT)

VS = (100, 500, 1000, 2000, 10000, 30000, 100000)
for _V in VS:
    mod('gamma_%d' % _V, {'V_acc': float(_V)}, 'gamma', module='ch00', sig=5)
    mod('lambda_%d' % _V, {'V_acc': float(_V)}, 'lambda_e', module='ch00')
    ex('eVmc2_%d' % _V, 'g-1', {'g': 'gamma_%d' % _V})
    ex('beta_%d' % _V, 'sqrt(1-1/g**2)', {'g': 'gamma_%d' % _V}, sig=4)
    ex('v_%d' % _V, 'c*b', {'c': 'c_', 'b': 'beta_%d' % _V})
    ex('v_nr_%d' % _V, 'c*sqrt(2*x)', {'c': 'c_', 'x': 'eVmc2_%d' % _V})
    ex('vratio_%d' % _V, 'v/vn', {'v': 'v_%d' % _V, 'vn': 'v_nr_%d' % _V}, sig=4)
    ex('lampm_%d' % _V, 'l', {'l': 'lambda_%d' % _V}, scale=1e12, sig=4)
    ex('lambda_nr_%d' % _V, 'h/sqrt(2*m*e*%r)' % float(_V), {'h': 'h_', 'm': 'm_', 'e': 'e_'})
    ex('lamratio_%d' % _V, 'l/ln', {'l': 'lambda_%d' % _V, 'ln': 'lambda_nr_%d' % _V}, sig=4)
    const('Vk_%d' % _V, _V / 1000.0)

V0 = R.speed_from_V(VA)                                     # speed after the gun (energy relation, section 5); a module input
E_TUBE = VP / D_GAP
T_PL = L_PL / V0
ex('E_tube', 'V/d', {'V': 'Vp', 'd': 'd_gap'}, sig=4)
ex('a_y', 'em*E', {'em': 'e_over_m', 'E': 'E_tube'}, sig=4)
ex('t_plates', 'l/v', {'l': 'l_pl', 'v': 'v_2000'}, sig=4)
ex('vy_exit', 'a*t', {'a': 'a_y', 't': 't_plates'}, sig=4)
ex('y_exit', 'a*t**2/2', {'a': 'a_y', 't': 't_plates'}, sig=4)
ex('theta_nr', 'em*E*l/v**2', {'em': 'e_over_m', 'E': 'E_tube', 'l': 'l_pl', 'v': 'v_2000'}, sig=4)
ex('y_screen_nr', 't*(l/2+L)', {'t': 'theta_nr', 'l': 'l_pl', 'L': 'L_drift'}, sig=4)
TH_IN = dict(E_field=E_TUBE, B_field=0.0, v_0=V0, theta_0=math.pi / 2, dt=2e-12, integrator='boris', t_run=T_PL)
mod('th_y_end', TH_IN, 'y_end')
mod('theta_sim', TH_IN, 'theta_end', sig=4)
ex('y_screen_sim', 'y+tan(t)*L', {'y': 'th_y_end', 't': 'theta_sim', 'L': 'L_drift'}, sig=4)
ex('ys_gap_pct', '100*(a/b-1)', {'a': 'y_screen_nr', 'b': 'y_screen_sim'}, sig=2)
ex('tan_theta_rel', 'x/g', {'x': 'theta_nr', 'g': 'gamma_2000'}, sig=4)
ex('y_screen_rel', 't*(l/2+L)', {'t': 'tan_theta_rel', 'l': 'l_pl', 'L': 'L_drift'}, sig=4)
ex('ys_rel_gap', '100*fabs(a/b-1)', {'a': 'y_screen_rel', 'b': 'y_screen_sim'}, sig=2)
ex('B_balance', 'E/v', {'E': 'E_tube', 'v': 'v_2000'}, sig=4)
BAL_IN = dict(TH_IN, B_field=E_TUBE / V0)
mod('yboth_um', BAL_IN, 'y_end', scale=1e6)
mod('rL_balance', dict(TH_IN, E_field=0.0, B_field=E_TUBE / V0), 'r_g')
ex('rL_over_l', 'r/l', {'r': 'rL_balance', 'l': 'l_pl'})
ex('d_over_l', 'd/l', {'d': 'd_gap', 'l': 'l_pl'}, sig=1)
ex('lambda_over_gap', 'l/d', {'l': 'lambda_2000', 'd': 'd_gap'}, sig=2)
ex('larmor_P', 'e**2*a**2/(6*pi*eps*c**3)', {'e': 'e_', 'a': 'a_y', 'eps': 'eps0_', 'c': 'c_'})
ex('larmor_ratio', 'P*t/(e*V)', {'P': 'larmor_P', 't': 't_plates', 'e': 'e_', 'V': 'Va'}, sig=2)
ex('vdev_30k', '100*(a/b-1)', {'a': 'v_nr_30000', 'b': 'v_30000'}, sig=2)
ex('vdev_2k', '100*(a/b-1)', {'a': 'v_nr_2000', 'b': 'v_2000'}, sig=2)
ex('defl_dev_30k', '100*((a/b)**2-1)', {'a': 'v_nr_30000', 'b': 'v_30000'}, sig=2)
ex('defl_dev_2k', '100*((a/b)**2-1)', {'a': 'v_nr_2000', 'b': 'v_2000'}, sig=2)
# the voltage at which v/v_NR = r: r^2 (1 + eps)^2 = 1 + eps/2, solved for eps, then V = eps m c^2 / e
_r = 0.99                                                    # the 1 % criterion, a given
ex('V_1pct', '((-(2*%(r)r**2-0.5)+sqrt((2*%(r)r**2-0.5)**2-4*%(r)r**2*(%(r)r**2-1)))/(2*%(r)r**2))*m*c**2/e'.replace('%(r)r', repr(_r)),
   {'m': 'm_', 'c': 'c_', 'e': 'e_'})
ex('helm_example', '(4/5)**1.5*mu*100*1.0/0.05', {'mu': 'mu0_'})
HEL_IN = dict(E_field=0.0, B_field=4e-3, v_0=V0, theta_0=0.06, dt=4e-12, integrator='boris', t_run=2.4e-8)
mod('rL_4mT_alpha06', HEL_IN, 'r_g')
mod('omega_4mT', HEL_IN, 'omega_c', sig=4)
ex('focus_L_2000_4mT', '2*pi*v*cos(0.06)/w', {'v': 'v_2000', 'w': 'omega_4mT'}, sig=4)
mod('rL_30k_1mT', dict(TH_IN, E_field=0.0, B_field=1e-3, v_0=R.speed_from_V(30000.0)), 'r_g')

# --- the integrator test: 20 turns of an electron of 2 kV at the angle 1.2 rad to B = 10 mT, N steps per turn, against the exact helix
B_T, CHI, TURNS = 0.01, 1.2, 20
_g0 = 1.0 / math.sqrt(1.0 - (V0 / C['c']) ** 2)
T_PY = 2 * math.pi / (C['e'] * B_T / (_g0 * C['m_e']))
NS = (16, 32, 64, 128, 256, 512)
_vpar = V0 * math.cos(CHI)


def _test_in(N, method):
    return dict(E_field=0.0, B_field=B_T, v_0=V0, theta_0=CHI, dt=T_PY / N * (1 + 1e-9), integrator=method, t_run=TURNS * T_PY)


mod('rL_test', _test_in(16, 'boris'), 'r_g', sig=4)
mod('omega_test', _test_in(16, 'boris'), 'omega_c')
ex('T_test', '2*pi/w', {'w': 'omega_test'}, sig=4)
_RK = '(1-th**6/72+th**8/576)'
for _N in NS:
    const('Ns_%d' % _N, _N, sig=3)
    for _m in ('boris', 'rk4'):
        _in = _test_in(_N, _m)
        for _o in ('x_end', 'y_end', 'z_end', 'energy_drift'):
            mod('t_%s_%d_%s' % (_m, _N, _o), _in, _o)
        ex('tst_%s_%d_err' % (_m, _N), 'sqrt(x**2+y**2+(z-%r)**2)/rg' % (_vpar * TURNS * T_PY),
           {'x': 't_%s_%d_x_end' % (_m, _N), 'y': 't_%s_%d_y_end' % (_m, _N), 'z': 't_%s_%d_z_end' % (_m, _N), 'rg': 'rL_test'})
    ex('tst_rk4_%d_loss' % _N, '-d', {'d': 't_rk4_%d_energy_drift' % _N})
    _th = '(2*pi/%d)' % _N
    ex('pbe_%d' % _N, '2*sin(%d*%d*(%s-2*atan(%s/2))/2)' % (TURNS, _N, _th, _th))
    ex('pre_%d' % _N, '2*sin(%d*%d*(%s-atan((%s-%s**3/6)/(1-%s**2/2+%s**4/24)))/2)' % (TURNS, _N, _th, _th, _th, _th, _th))
    ex('pe_rk4_%d' % _N, 'sin(%r)**2*(1-%s**%d)' % (CHI, _RK.replace('th', _th), TURNS * _N))
    ex('boris_factor_%d' % _N, 'sqrt(1+(pi/%d)**2)' % _N, sig=5)
ex('slope_boris_pos', 'log(b/a)/log(4)', {'a': 'tst_boris_64_err', 'b': 'tst_boris_256_err'})
ex('slope_rk4_pos', 'log(b/a)/log(4)', {'a': 'tst_rk4_64_err', 'b': 'tst_rk4_256_err'})
ex('slope_rk4_energy', 'log(b/a)/log(4)', {'a': 'tst_rk4_64_loss', 'b': 'tst_rk4_256_loss'})
ex('pred_gap_boris_64_pct', '100*fabs(p/m-1)', {'p': 'pbe_64', 'm': 'tst_boris_64_err'}, sig=2)
ex('rk4_loss_per_turn_16_pct', '100*(1-%s**16)' % _RK.replace('th', '(2*pi/16)'), sig=2)
ex('rk4_half_turns_16', 'log(0.5)/(16*log(%s))' % _RK.replace('th', '(2*pi/16)'))
ex('rk4_turns_1pct_loss_64', 'log(0.99)/(64*log(%s))' % _RK.replace('th', '(2*pi/64)'))
ex('work_rk4_16', '4*16', sig=2)
ex('boris_Nmin_01pct', 'pi/sqrt(1.001**2-1)')
ex('tst_rk4_16_loss_pct', '100*x', {'x': 'tst_rk4_16_loss'}, sig=3)

# --- Thomson's e/m: the method run on the simulated tube, and the corrections that explain its small deficit
ex('em_inferred', 'th*E/(B**2*l)', {'th': 'theta_sim', 'E': 'E_tube', 'B': 'B_balance', 'l': 'l_pl'}, sig=5)
ex('em_ratio', 'a/b', {'a': 'em_inferred', 'b': 'e_over_m'}, sig=5)
ex('em_ratio_dev', '100*(1-r)', {'r': 'em_ratio'}, sig=2)
ex('gamma_factor', '1/g', {'g': 'gamma_2000'}, sig=5)
ex('atan_factor', 'atan(y)/y', {'y': 'tan_theta_rel'}, sig=5)
ex('em_pred_decomp', 'a*b', {'a': 'gamma_factor', 'b': 'atan_factor'}, sig=5)
ex('decomp_gap', 'fabs(a-b)', {'a': 'em_pred_decomp', 'b': 'em_ratio'}, sig=2)
ex('em_ratio_rel_corrected', 'r*g', {'r': 'em_ratio', 'g': 'gamma_2000'}, sig=5)

# --- Thomson (1897), digitised in data/ch01/thomson1897.json (his two tables, in CGS electromagnetic units); statistics computed here from the data
_m1 = [r for r in DATA['method1_heat']['rows']]
_m2 = [r for r in DATA['method2_crossed']['rows']]
_em = lambda moe: 1.0 / (1e-4 * moe) / (C['e'] / C['m_e'])        # e/m in SI over the CODATA value, from m/e in g/abC
_r1 = [_em(r[4]) for r in _m1]
_r12 = [_em(r[4]) for r in _m1 if r[0] in (1, 2)]
_r3 = [_em(r[4]) for r in _m1 if r[0] == 3]
_r2 = [_em(r[6]) for r in _m2]
# the table's internal arithmetic: m/e = I^2 Q / (2 W) against the printed m/e, row by row
_dev = [abs((r[3] ** 2 / (2 * r[2])) / r[4] - 1) for r in _m1]
_good = sorted(d for d in _dev if d < 0.5)
const('n_m1', len(_m1), sig=2)
const('n_m2', len(_m2), sig=1)
const('m1_min_ratio', min(_r1))
const('m1_max_ratio', max(_r1))
const('m1_mean_ratio', sum(_r1) / len(_r1))
const('m1_tube12_ratio', sum(_r12) / len(_r12))
const('m1_tube3_ratio', sum(_r3) / len(_r3))
const('m2_min_ratio', min(_r2))
const('m2_max_ratio', max(_r2))
const('m2_mean_ratio', sum(_r2) / len(_r2))
ex('m1_spread', 'a/b', {'a': 'm1_max_ratio', 'b': 'm1_min_ratio'}, sig=2)
import statistics
const('m1_median_dev_pct', 100 * statistics.median(_good), sig=2)
const('m1_good_maxdev_pct', 100 * max(_good), sig=2)
_bad = [(r[3] ** 2 / (2 * r[2])) / r[4] for r in _m1 if abs((r[3] ** 2 / (2 * r[2])) / r[4] - 1) > 0.5]
const('m1_bad_ratio', 1.0 / _bad[0], sig=3)             # the printed W/Q against the one that m/e and v imply, in the one inconsistent row
const('ystretch', 2600.0 / 2000.0, sig=2)

_variants = {}


def num_name(key, sig):
    """The name of key printed with `sig` significant figures (a derived number, declared on first use)."""
    if key not in NUMS:
        raise KeyError('text/ch01.py: number %r is used in the prose but not declared in NUMS' % key)
    name = '%s_s%d' % (key, sig)
    if name not in NUMS:
        NUMS[name] = {'expr': 'x', 'of': {'x': key}, 'scale': NUMS[key].get('scale', 1), 'sig': sig}
    return name


# ============================================================================================================ figures
# Drawn here, from the reference solver ref/ch01.py (which physics/ch01.js reproduces to rounding, checks/check_parity.py) and from
# the digitised data. The tube drawings use 2 px per mm along the tube and 2.6 px per mm across it.
XP, XS = 0.06, 0.30                                          # where the plates begin, where the screen is (m)


def _thin(pts, n=300):
    pts = list(pts)
    if len(pts) <= n:
        return pts
    k = int(math.ceil(len(pts) / n))
    out = pts[::k]
    if out[-1] is not pts[-1]:
        out.append(pts[-1])
    return out


def _tx(x, y, s, cls='lbl', anchor='start', extra=''):
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s" %s>%s</text>' % (cls, x, y, anchor, extra, s)


def plate_path(E, B):
    """The electron of the worked example through the plates and on to the screen: a list of (x, y) in metres, from the cathode."""
    out = R.compute(dict(TH_IN, E_field=E, B_field=B))
    tr = out['trajectory']
    pts = [(0.0, 0.0), (XP, 0.0)] + [(XP + tr[i], tr[i + 1]) for i in range(0, len(tr), 3)]
    xe, ye = XP + out['x_end'], out['y_end']
    pts.append((XS, ye + math.tan(out['theta_end']) * (XS - xe)))
    return _thin(pts)


def svg_tube():
    X = lambda x: 40 + (x + 0.005) * 2000
    Y = lambda y: 150 - y * 2600
    s = ['<svg viewBox="0 0 760 300" role="img" aria-label="Cross-section of the cathode-ray tube: cathode, anode with a slit, deflection plates, coils, screen, and the path of one electron.">',
         '<rect width="760" height="300" fill="#fff"/>']
    s.append('<path d="M%.0f %.0f L%.0f %.0f L%.0f %.0f L%.0f %.0f Q%.0f %.0f %.0f %.0f L%.0f %.0f L%.0f %.0f L%.0f %.0f Z" fill="#fbf8f3" stroke="#8b8079" stroke-width="1.4"/>' % (
        X(-0.004), Y(0.016), X(0.035), Y(0.016), X(0.05), Y(0.045), X(0.30), Y(0.045), X(0.305), Y(0), X(0.30), Y(-0.045), X(0.05), Y(-0.045), X(0.035), Y(-0.016), X(-0.004), Y(-0.016)))
    s.append('<rect x="%.1f" y="%.1f" width="5" height="%.1f" fill="#1c1518"/>' % (X(-0.003), Y(0.008), Y(-0.008) - Y(0.008)))
    s.append('<path d="M%.1f %.1f l-14 6 M%.1f %.1f l-14 -6" stroke="#7a1f2b" stroke-width="1.4" fill="none"/>' % (X(-0.003), Y(0.004), X(-0.003), Y(-0.004)))
    s.append('<rect x="%.1f" y="%.1f" width="6" height="%.1f" fill="#5a504b"/><rect x="%.1f" y="%.1f" width="6" height="%.1f" fill="#5a504b"/>' % (
        X(0.02) - 3, Y(0.014), Y(0.0012) - Y(0.014), X(0.02) - 3, Y(-0.0012), Y(-0.014) - Y(-0.0012)))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="#1c1518"/><rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="#1c1518"/>' % (
        X(XP), Y(D_GAP / 2) - 4, X(XP + L_PL) - X(XP), X(XP), Y(-D_GAP / 2), X(XP + L_PL) - X(XP)))
    cx, rx = X(XP + L_PL / 2), (X(XP + L_PL) - X(XP)) / 2
    s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="7" fill="none" stroke="#7a1f2b" stroke-width="3"/><ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="7" fill="none" stroke="#7a1f2b" stroke-width="3"/>' % (cx, Y(0.047), rx, cx, Y(-0.047), rx))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3a8a5a" stroke-width="3"/>' % (X(XS), Y(0.045), X(XS), Y(-0.045)))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#cdc1ae" stroke-dasharray="4 4"/>' % (X(0), Y(0), X(XS), Y(0)))
    s.append('<polyline points="%s" fill="none" stroke="#7a1f2b" stroke-width="2"/>' % ' '.join('%.1f,%.1f' % (X(x), Y(y)) for x, y in plate_path(E_TUBE, 0.0)))
    lab = lambda x, y, t, a='middle': s.append(_tx(x, y, t, 'lbl', a))
    lab(X(0), Y(-0.012) + 18, 'cathode C')
    lab(X(0.02), Y(0.016) - 7, 'anode A')
    lab(X(0.085), Y(-0.0075) + 24, 'plates')
    lab(cx, Y(-0.047) + 24, 'coils (Helmholtz pair)')
    lab(X(XS), Y(0.045) - 8, 'phosphor screen', 'end')
    ya = 104
    s.append('<g stroke="#8b8079" stroke-width="1"><line x1="%.1f" y1="%d" x2="%.1f" y2="%d"/><line x1="%.1f" y1="%d" x2="%.1f" y2="%d"/><line x1="%.1f" y1="%d" x2="%.1f" y2="%d"/></g>' % (
        X(XP), ya, X(XP + L_PL), ya, X(XP), ya - 4, X(XP), ya + 4, X(XP + L_PL), ya - 4, X(XP + L_PL), ya + 4))
    s.append(_tx(cx, ya - 8, '<tspan class="m">l</tspan>', 'lbl', 'middle'))
    s.append('<g stroke="#8b8079"><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/></g>' % (
        X(XP + L_PL) + 12, Y(D_GAP / 2), X(XP + L_PL) + 12, Y(-D_GAP / 2), X(XP + L_PL) + 8, Y(D_GAP / 2), X(XP + L_PL) + 16, Y(D_GAP / 2), X(XP + L_PL) + 8, Y(-D_GAP / 2), X(XP + L_PL) + 16, Y(-D_GAP / 2)))
    s.append(_tx(X(XP + L_PL) + 20, Y(0) + 4, '<tspan class="m">d</tspan>', 'lbl'))
    s.append(_tx(X(XS) - 6, Y(0) + 18, '<tspan class="m">x</tspan><tspan class="mu" font-size="12" dy="4">s</tspan>', 'lbl', 'end'))
    s.append('</svg>')
    return ''.join(s)


def _panel(pts, title, x0, w, h, ymax=0.022):
    X = lambda x: x0 + (x - 0.05) / 0.25 * w
    Y = lambda y: 10 + h / 2 - y / ymax * h / 2
    g = ['<rect x="%.1f" y="10" width="%.1f" height="%.1f" fill="#fff" stroke="#cdc1ae"/>' % (x0, w, h),
         '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#cdc1ae" stroke-dasharray="4 4"/>' % (x0, Y(0), x0 + w, Y(0)),
         '<rect x="%.1f" y="%.1f" width="%.1f" height="3" fill="#1c1518"/><rect x="%.1f" y="%.1f" width="%.1f" height="3" fill="#1c1518"/>' % (
             X(XP), Y(D_GAP / 2) - 3, X(XP + L_PL) - X(XP), X(XP), Y(-D_GAP / 2), X(XP + L_PL) - X(XP)),
         '<line x1="%.1f" y1="10" x2="%.1f" y2="%.1f" stroke="#e6dfd2"/><line x1="%.1f" y1="10" x2="%.1f" y2="%.1f" stroke="#e6dfd2"/>' % (X(XP), X(XP), 10 + h, X(XP + L_PL), X(XP + L_PL), 10 + h),
         '<polyline points="%s" fill="none" stroke="#7a1f2b" stroke-width="2"/>' % ' '.join('%.1f,%.1f' % (X(x), min(max(Y(y), 10), 10 + h)) for x, y in pts if x >= 0.05),
         _tx(x0 + 6, 26, title, 'lbl')]
    ys = 5e-3 / ymax * h / 2
    yb = 10 + h - 14
    g.append('<g stroke="#7a1f2b"><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/></g>' % (
        x0 + w - 12, yb, x0 + w - 12, yb - ys, x0 + w - 16, yb, x0 + w - 8, yb, x0 + w - 16, yb - ys, x0 + w - 8, yb - ys))
    g.append(_tx(x0 + w - 18, yb - ys / 2 + 4, '5 mm', 'tick', 'end'))
    return ''.join(g)


def svg_motions():
    w, h = 230, 190
    Bb = E_TUBE / V0
    s = ['<svg viewBox="0 0 780 230" role="img" aria-label="Three computed electron paths: a parabola in an electric field, a circular arc in a magnetic field, a straight line when the two forces balance.">',
         '<rect width="780" height="230" fill="#fff"/>',
         _panel(plate_path(E_TUBE, 0.0), 'E only: parabola', 20, w, h),
         _panel(plate_path(0.0, Bb), 'B only: circle', 275, w, h),
         _panel(plate_path(E_TUBE, Bb), 'E and B balanced: line', 530, w, h),
         _tx(20, 222, 'x from 50 mm to 300 mm (plates 60 mm to 110 mm, grey lines); vertical axis stretched', 'tick'), '</svg>']
    return ''.join(s)


def svg_helix():
    """Six electrons from one point at 60 mrad to B (4 mT, 2 kV): the module's path, and the same path turned about B in steps of 60 degrees."""
    out = R.compute(dict(HEL_IN, t_run=1.05 * 2 * math.pi / R.compute(HEL_IN)['omega_c'], dt=4e-12))
    tr = out['trajectory']
    pts = [(tr[i], tr[i + 1], tr[i + 2]) for i in range(0, len(tr), 3)]
    Lf = 2 * math.pi * V0 * math.cos(0.06) / R.compute(HEL_IN)['omega_c']
    Zx = lambda z: 40 + z / 0.26 * 460
    Yx = lambda t: 110 - t / 0.0045 * 80
    s = ['<svg viewBox="0 0 760 230" role="img" aria-label="Electrons leaving one point at a small angle to a uniform magnetic field spiral round the field and meet it again after one turn.">',
         '<rect width="760" height="230" fill="#fff"/>', '<rect x="40" y="10" width="460" height="200" fill="#fff" stroke="#cdc1ae"/>',
         '<line x1="40" y1="110" x2="500" y2="110" stroke="#cdc1ae" stroke-dasharray="4 4"/>']
    for k in range(6):
        a = k * math.pi / 3
        side = [(z, x * math.cos(a) - y * math.sin(a)) for x, y, z in pts]
        s.append('<polyline points="%s" fill="none" stroke="#7a1f2b" stroke-width="1.5" opacity="0.8"/>' % ' '.join('%.1f,%.1f' % (Zx(z), Yx(t)) for z, t in _thin(side)))
    s.append('<line x1="%.1f" y1="12" x2="%.1f" y2="208" stroke="#3a8a5a" stroke-dasharray="3 3"/>' % (Zx(Lf), Zx(Lf)))
    s.append(_tx(Zx(Lf), 226, '<tspan class="m">L</tspan> = 2π<tspan class="m">v</tspan><tspan class="mu" font-size="12" dy="4">∥</tspan><tspan dy="-4">/Ω</tspan>', 'lbl', 'middle'))
    s.append(_tx(40, 226, 'start', 'lbl', 'start'))
    cx, cy, es = 640, 110, 80 / 0.0045
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" stroke="#cdc1ae"/>' % (cx, cy, 0.0045 * es))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#cdc1ae" stroke-dasharray="3 3"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#cdc1ae" stroke-dasharray="3 3"/>' % (cx - 90, cy, cx + 90, cy, cx, cy - 90, cx, cy + 90))
    for k in range(6):
        a = k * math.pi / 3
        ring = [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y, z in pts]
        s.append('<polyline points="%s" fill="none" stroke="#7a1f2b" stroke-width="1.2" opacity="0.8"/>' % ' '.join('%.1f,%.1f' % (cx + u * es, cy - v * es) for u, v in _thin(ring)))
    s.append(_tx(cx, 226, 'end view: six circles through the axis', 'lbl', 'middle'))
    s.append('</svg>')
    return ''.join(s)


def svg_integrators():
    """Error against the exact helix, and energy error, for both integrators, as a function of steps per turn (20 turns, 2 kV, 10 mT)."""
    Ns = (8, 16, 32, 64, 128, 256, 512)
    rg = R.compute(_test_in(16, 'boris'))['r_g']
    res = {}
    for m in ('boris', 'rk4'):
        for N in Ns:
            o = R.compute(_test_in(N, m))
            err = math.sqrt(o['x_end'] ** 2 + o['y_end'] ** 2 + (o['z_end'] - _vpar * TURNS * T_PY) ** 2) / rg
            res[(m, N)] = (err, abs(o['energy_drift']))
    W, H = 900, 330
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Position error and energy error of the Boris pusher and of Runge-Kutta 4 against steps per turn, on logarithmic axes.">' % (W, H),
         '<rect width="%d" height="%d" fill="#fff"/>' % (W, H)]

    def panel(x0, title, idx, lo, hi, floor_note=None):
        w, h, y0 = 370, 240, 40
        lx = lambda n: x0 + math.log10(n / 6.0) / math.log10(700 / 6.0) * w
        ly = lambda e: y0 + h - (math.log10(max(e, 10 ** lo)) - lo) / (hi - lo) * h
        g = ['<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" stroke="#cdc1ae"/>' % (x0, y0, w, h), _tx(x0, y0 - 12, title, 'lbl')]
        for e in range(lo, hi + 1, 2):
            g.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#f0ebe3"/>' % (x0, x0 + w, ly(10 ** e), ly(10 ** e)))
            g.append(_tx(x0 - 6, ly(10 ** e) + 4, '1e%d' % e if e else '1', 'tick', 'end'))
        for n in (8, 16, 32, 64, 128, 256, 512):
            g.append(_tx(lx(n), y0 + h + 15, str(n), 'tick', 'middle'))
        g.append(_tx(x0 + w / 2, y0 + h + 32, 'steps per turn  N', 'lbl', 'middle'))
        for m, col, dash in (('boris', '#7a1f2b', ''), ('rk4', '#1c1518', '6 3')):
            pts = ' '.join('%.1f,%.1f' % (lx(N), ly(res[(m, N)][idx])) for N in Ns)
            g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="%s"/>' % (pts, col, dash))
            for N in Ns:
                g.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (lx(N), ly(res[(m, N)][idx]), col))
        g.append(_tx(x0 + w - 6, y0 + 16, '● Boris', 'lbl', 'end', 'fill="#7a1f2b"'))
        g.append(_tx(x0 + w - 6, y0 + 31, '● RK4', 'lbl', 'end', 'fill="#1c1518"'))
        if floor_note:
            g.append(_tx(x0 + 8, y0 + h - 8, floor_note, 'tick'))
        return ''.join(g)
    s.append(panel(70, 'position error / gyroradius after 20 turns', 0, -10, 2))
    s.append(panel(500, 'energy error |ΔK/K| over the run', 1, -18, 0, 'Boris: rounding noise, about 1e-16'))
    s.append('</svg>')
    return ''.join(s)


def svg_thomson1897():
    """Every e/m value of Thomson's two tables (SI) against CODATA 2018."""
    emc = C['e'] / C['m_e']
    em = lambda moe: 1.0 / (1e-4 * moe)
    rows = [('method 1, tubes 1 and 2', [em(r[4]) for r in _m1 if r[0] in (1, 2)], '#1c1518'),
            ('method 1, tube 3', [em(r[4]) for r in _m1 if r[0] == 3], '#8b8079'),
            ('method 2, crossed fields', [em(r[6]) for r in _m2], '#7a1f2b')]
    s = ['<svg viewBox="0 0 760 330" role="img" aria-label="Thomson 1897 values of e/m from two methods, plotted against the CODATA value.">', '<rect width="760" height="330" fill="#fff"/>']
    x0, w, xmax = 215, 520, 4.2e11
    X = lambda v: x0 + v / xmax * w
    for i, (lab, vals, col) in enumerate(rows):
        y = 70 + i * 70
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e6dfd2"/>' % (x0, y, x0 + w, y))
        s.append(_tx(x0 - 10, y + 4, lab, 'lbl', 'end'))
        seen = {}
        for v in vals:
            k = round(v / 1e9)
            seen[k] = seen.get(k, 0) + 1
            s.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" fill-opacity="0.75" stroke="#fff"/>' % (X(v), y - (seen[k] - 1) * 9, col))
        s.append('<path d="M%.1f %d l-5 12 h10 z" fill="%s"/>' % (X(sum(vals) / len(vals)), y + 8, col))
    s.append('<line x1="%.1f" y1="20" x2="%.1f" y2="270" stroke="#3a8a5a" stroke-width="2"/>' % (X(emc), X(emc)))
    s.append(_tx(X(emc) + 6, 30, 'CODATA 2018: %.3f × 10¹¹ C/kg' % (emc / 1e11), 'lbl'))
    for t in (0, 1, 2, 3, 4):
        s.append('<line x1="%.1f" y1="270" x2="%.1f" y2="276" stroke="#6f655f"/>' % (X(t * 1e11), X(t * 1e11)))
        s.append(_tx(X(t * 1e11), 292, '%d' % t, 'tick', 'middle'))
    s.append('<line x1="%.1f" y1="270" x2="%.1f" y2="270" stroke="#6f655f"/>' % (x0, x0 + w))
    s.append(_tx(x0 + w / 2, 316, 'e/m  in units of 10¹¹ C/kg    (triangles: mean of each row)', 'lbl', 'middle'))
    s.append('</svg>')
    return ''.join(s)


FIG_SVG = {'tube1': svg_tube, 'motions': svg_motions, 'helix': svg_helix, 'integrators': svg_integrators, 'th1897': svg_thomson1897}


# ============================================================================================================ the prose
def sections():
    """The sections of the chapter, as (anchor, number, title, html) tuples; html uses the placeholders described above."""
    S = []

    S.append(('c1-beam', 1, 'A beam you can bend', r'''
<p class="psec__lead">Switch on an old cathode-ray television in a dark room and bring a bar magnet close to the glass. The picture twists, colours smear, and when you take the magnet away it settles back. Nothing touched the screen. The magnet reached through the glass and pushed on something invisible inside, and the push changed with the direction the something was moving.</p>
<p>That something is a beam of electrons. In 1897 J. J. Thomson built a tube like the one drawn in ‹fig:tube1›, pumped it until almost nothing was left inside, and did with a battery and two coils what the magnet does to the television. His goal was to find out what the beam was made of. The same two handles, an electric field and a magnetic field, steer the electrons in every electron microscope and in the measuring machine this project is working towards. The whole of chapters 2 to 8 rests on one question that we answer in this chapter for the simplest case: <em>where does a single electron go when we know the fields?</em></p>
<p>We first meet the parts. At the left of ‹fig:tube1› the <em>cathode</em> C, a metal electrode, lets electrons escape from its surface (in Thomson's tube a plate in a rarefied gas, from which the discharge itself pulled them; in a television tube a heated strip). Our model starts the electron at rest at the cathode, however it got out. A little way along, a plate with a slit, the <em>anode</em> A, is held at a positive voltage \(V_a\) relative to the cathode, so the electrons are pulled towards it, pass through the slit and carry on in the dark as a thin beam. They fly between two parallel metal plates of length \(l\), a distance \(d\) apart, which we can connect to a battery, so that a voltage \(V_p\) makes an electric field between them. Two coils outside the glass can add a magnetic field over the same stretch. At the far end a screen coated with a phosphor glows where the electrons arrive, and a ruler on the glass reads the position of the spot. Thomson's plates were about 5 cm long, 2 cm broad and 1.5 cm apart, and he read the spot's position from a scale pasted on the tube; we take plates with the same \(l\) and \(d\).</p>
<figure class="pfig">
  <div class="pfig__plate">‹SVG:tube1›</div>
  <figcaption>‹F tube1›The tube of this chapter, drawn from the model's own numbers (the horizontal axis is true to scale, the vertical axis is stretched by a factor ‹n:ystretch|2›). The red line is the path of one electron computed by the solver of ‹s:numerics›, with the plates at \(V_p=\)‹n:Vp|3›&nbsp;V and no magnetic field: it bends towards the positive plate. Symbols: \(V_a\) anode voltage, \(l\) and \(d\) plate length and gap, \(x_s\) the position of the screen.</figcaption>
</figure>
<p>Three results will come out of this chapter, and each one is used later. First, the <em>force law</em> that tells an electron what a given electric and magnetic field do to it, derived from a Lagrangian so that it holds at any speed and in any field shape. Second, the <em>energy relation</em> that tells us how fast an electron is after falling through a voltage; the gun of chapter 3 is this relation. Third, a <em>numerical integrator</em> that follows the electron through fields too complicated for pencil and paper, whose errors we measure against an exact solution; chapter 4 uses it to trace rays through lenses.</p>
'''))

    S.append(('c1-model', 2, 'The model and where it holds', r'''
<p>We keep only what makes the tube a tube. The electron is a <em>point particle</em> with charge \(q=-e\) and rest mass \(m\); we write \(e=1.602\,176\,634\times10^{-19}\ \mathrm{C}\) and \(m=9.109\,383\,70\times10^{-31}\ \mathrm{kg}\) (CODATA 2018). The electric field \(\mathbf E\) and the magnetic field \(\mathbf B\) are <em>given</em> and do not change in time. The beam is so thin that its electrons do not push on each other, so one electron stands for all. The tube is empty: Thomson needed a very good vacuum because stray gas, made conducting by the beam, shorted out the field between his plates and the spot crept back to the middle, a behaviour he describes in his paper.</p>
<p>Between the plates the field is uniform, \(E=V_p/d\), and zero outside; behind the anode of the gun the field is uniform as well, \(E=V_a/x_a\) for \(0\lt x\lt x_a\). Real plates have fringe fields at their edges, and for plates with \(d/l=\)‹n:d_over_l|1› these reach well into the gap. This is the largest simplification of the tube model. Chapter 4 replaces it by a numerical solution of Laplace's equation for plates and lenses. Here it keeps the algebra visible.</p>
<p>Three questions tell us whether the simplest physics will do, and each has a number for the tube at \(V_a=\)‹n:Va|4›&nbsp;V that we can compute rather than argue about.</p>
<ul>
<li><em>Is the electron fast enough for relativity to matter?</em> Falling through \(V_a\) it gains the energy \(eV_a\), which is \(\epsilon=eV_a/mc^2=\)‹n:eVmc2_2000|3› of its rest energy, and it flies at \(v/c=\)‹n:beta_2000|4›. Relativity is a small correction here (‹s:nr›) but not a negligible one at the 30 kV of a column, where \(\epsilon=\)‹n:eVmc2_30000|3› and \(v/c=\)‹n:beta_30000|3›.</li>
<li><em>Does the electron radiate away its energy as it is accelerated?</em> A charge with acceleration \(a\) radiates the power \(P=e^2a^2/(6\pi\varepsilon_0c^3)\) (Larmor; Jackson, <em>Classical Electrodynamics</em>, ch. 14). Between the plates \(a=eE/m=\)‹n:a_y|3›&nbsp;m/s², so \(P=\)‹n:larmor_P|3›&nbsp;W. In the \(t=\)‹n:t_plates|3›&nbsp;s that the electron spends there it radiates a fraction ‹n:larmor_ratio|2› of its kinetic energy. We ignore radiation.</li>
<li><em>Is a trajectory a meaningful thing for a quantum object?</em> The wavelength of the electron, \(\lambda=\)‹n:lambda_2000|3›&nbsp;m (‹s:nr›), is ‹n:lambda_over_gap|2› of the plate gap. As long as the fields change over distances much larger than \(\lambda\), the wave packet follows the classical path. We use classical mechanics.</li>
</ul>
<p>Two more numbers describe the geometry. The gyroradius in the balancing field of ‹s:newton› is \(r_L=\)‹n:rL_balance|3›&nbsp;m, ‹n:rL_over_l|3› times the plate length, so the magnetic bend over the plates is small; in the 4 mT solenoid of ‹s:helix› it is a few millimetres and the electron circles visibly.</p>
'''))

    S.append(('c1-newton', 3, 'Slow electrons: the pencil-and-paper version', r'''
<p class="psec__lead">A ball thrown across a room falls along a parabola; a ball tied to a string and swung overhead goes round in a circle; a swimmer pushed by a cross-current and swimming against it at the right speed goes straight. The electron in the tube does all three.</p>
<p>We work with Newton's law \(m\,\mathrm d\mathbf v/\mathrm dt=\mathbf F\) and the force on a charge \(q\) in electric and magnetic fields, the Lorentz force \(\mathbf F=q(\mathbf E+\mathbf v\times\mathbf B)\), which ‹s:lagrange› derives and generalises. For the electron \(q=-e\). Let \(x\) point along the tube, \(y\) towards the upper plate and \(z\) out of the page, so \(\mathbf v=(v_x,v_y,0)\).</p>
<h4><span class="psub__n">3.1</span>An electric field: the parabola</h4>
<p>Between the plates the field points along \(y\), \(\mathbf E=(0,-E,0)\) with \(E=V_p/d\), because the field points from the positive plate to the negative one and we call the upper plate positive for \(V_p>0\). The force on the electron is \(\mathbf F=-e\mathbf E=(0,+eE,0)\): it is pushed <em>towards the positive plate</em>, which is what Thomson saw. The force has no \(x\) component, so \(v_x\) stays at the entrance value \(v_0\), and the time spent between the plates is \(t=x/v_0\) after a distance \(x\). Along \(y\) the acceleration is \(a=eE/m\) and the electron starts with \(v_y=0\), so</p>
‹E par›y(x)=\tfrac12 a\,t^2=\frac{eE}{2m v_0^2}\,x^2 ,\qquad \tan\theta=\frac{v_y}{v_x}=\frac{eE\,l}{m v_0^2}‹/E›
<p>The first equation is a parabola, the second gives the angle \(\theta\) of the path against the axis as the electron leaves the plates after the length \(l\). Behind the plates there is no force, and the electron flies on in a straight line. A line with slope \(\tan\theta\) that touches the parabola at \(x=l\) meets the axis at \(x=l-y(l)/y'(l)=l-\tfrac12 l=l/2\): the electron seems to come from the <em>centre of the plates</em> (checked by SymPy, D5a). With a distance \(L\) from the plate end to the screen the spot is therefore at</p>
‹E ys›y_s=\left(\tfrac12 l+L\right)\tan\theta ,\qquad L=x_s-x_p-l .‹/E›
<h4><span class="psub__n">3.2</span>A magnetic field: the circle</h4>
<p>With only a magnetic field \(\mathbf B=(0,0,-B_p)\), pointing into the page for \(B_p>0\), the force \(-e\,\mathbf v\times\mathbf B\) is at right angles to \(\mathbf v\) at every instant. A force at right angles to the velocity changes the direction but not the length of \(\mathbf v\): the speed \(v\) stays constant. The electron therefore moves on a circle, held on it by a centripetal force. A circle of radius \(r\) at speed \(v\) needs the force \(mv^2/r\); the magnetic force is \(evB\); equating,</p>
‹E circle›r_L=\frac{m v}{eB},\qquad \Omega=\frac{v}{r_L}=\frac{eB}{m},\qquad f=\frac{\Omega}{2\pi} .‹/E›
<p>\(r_L\) is the <em>gyroradius</em> (or Larmor radius), \(\Omega\) the <em>cyclotron angular frequency</em>. The time for one turn, \(2\pi/\Omega\), does not depend on the speed, only on \(B\): a fast electron makes a big circle and a slow one a small circle in the same time. Over the plates the electron turns by the angle \(\varphi\) with \(\sin\varphi=l/r_L\); for \(l\ll r_L\) this gives \(\varphi\approx eBl/(mv_0)\).</p>
<h4><span class="psub__n">3.3</span>Both fields: Thomson's measurement of \(e/m\)</h4>
<p>The electric force on the electron points towards the positive plate; for our orientation of \(\mathbf B\) the magnetic force points the other way. If the two are equal, \(eE=evB\), the beam goes straight on. That fixes the speed, \(v_0=E/B\), without our knowing \(e\) or \(m\) separately. Insert it into the angle ‹eq:par› with \(\tan\theta\approx\theta\):</p>
‹E em›\theta=\frac{e}{m}\,\frac{E\,l}{v_0^{2}}=\frac{e}{m}\,\frac{B^2 l}{E}\quad\Longrightarrow\quad \frac{e}{m}=\frac{\theta\,E}{B^{2}\,l} .‹/E›
<p>Every quantity on the right can be measured with a ruler, a voltmeter and an ammeter: the deflection \(\theta\) of the spot with the field off, the field \(E=V_p/d\), and the magnetic field \(B\) that brings the spot back to the axis. This is Thomson's second method (‹s:thomson›); his equation \(m/e=H^2 l/(F\theta)\) is ‹eq:em› written upside down, with his \(H\) and \(F\) for \(B\) and \(E\).</p>
<div class="pbox pbox--ex"><span class="pbox__t">‹X ex_tube› · the default tube</span>
<p>Take \(V_a=\)‹n:Va|4›&nbsp;V, \(V_p=\)‹n:Vp|3›&nbsp;V, \(d=15\ \mathrm{mm}\), \(l=50\ \mathrm{mm}\). Non-relativistically the electron leaves the gun with \(v_0=\sqrt{2eV_a/m}=\)‹n:v_nr_2000|4›&nbsp;m/s; the relativistic value of ‹s:nr› is ‹n:v_2000|4›&nbsp;m/s, which we use from here on. The field is \(E=V_p/d=\)‹n:E_tube|4›&nbsp;V/m, the acceleration \(a=eE/m=\)‹n:a_y|4›&nbsp;m/s², the time in the plates \(t=l/v_0=\)‹n:t_plates|4›&nbsp;s, the sideways speed at the exit \(v_y=at=\)‹n:vy_exit|4›&nbsp;m/s and the displacement there \(\tfrac12at^2=\)‹n:y_exit|4›&nbsp;m. The angle follows from ‹eq:par›, \(\tan\theta=\)‹n:theta_nr|4›, and with \(L=x_s-x_p-l=0.19\ \mathrm{m}\) the spot is at \(y_s=\)‹n:y_screen_nr|4›&nbsp;m by ‹eq:ys›. The solver of ‹s:numerics›, which integrates the full relativistic equation of motion, puts the spot at \(y_s=\)‹n:y_screen_sim|4›&nbsp;m. The gap of ‹n:ys_gap_pct|2›&nbsp;% is not a numerical error. It is the Lorentz factor \(\gamma=\)‹n:gamma_2000|6› of ‹s:nr›: the sideways momentum grows as \(p_y=eEt\) while \(p_x=\gamma mv_x\) stays put, so \(\tan\theta=eEl/(\gamma mv^2)\), with \(v\) the relativistic speed. That gives \(\tan\theta=\)‹n:tan_theta_rel|4› and a spot at \(y_s=\)‹n:y_screen_rel|4›&nbsp;m, within ‹n:ys_rel_gap|4›&nbsp;% of the solver.</p>
<p>The balancing field is \(B=E/v_0=\)‹n:B_balance|4›&nbsp;T. The computed spot with that field on is at \(y_s=\)‹n:yboth_um|3›&nbsp;µm, zero to the resolution of the integration.</p></div>
<figure class="pfig">
  <div class="pfig__plate">‹SVG:motions›</div>
  <figcaption>‹F motions›The three motions, computed by the solver of ‹s:numerics› with the default tube. Left: electric field only, a parabola between the grey lines and a straight line after them. Middle: magnetic field only, with the strength \(B_p=E/v_0=\)‹n:B_balance|4›&nbsp;T of the right-hand panel, a circular arc bending the other way. Right: both fields, a straight line. The vertical axis is stretched; the red bar is 5 mm.</figcaption>
</figure>
'''))
    return S


def sections_b():
    S = []
    S.append(('c1-lagrange', 4, 'From Newton to a Lagrangian ★', r'''
<p class="psec__lead">Newton's law with the Lorentz force is enough for the slow electron of ‹s:newton›. It stops being enough in two places. The electron of a 30 kV column moves at a third of the speed of light, where \(\tfrac12mv^2\) is no longer its energy. And the magnetic lenses of chapter 4 are not uniform fields: there the vector potential of the field, not only the field itself, decides what is conserved. A Lagrangian handles both, so we derive the force law from one. The passage is marked ★ because it is the heavier algebra of the chapter; ‹eq:lorentz› and ‹eq:canon›, with their meaning, are all a reader needs from it.</p>
<h4><span class="psub__n">4.1</span>The free particle</h4>
<p>Hamilton's principle says that the path a particle takes between two events is the one for which the <em>action</em> \(S=\int L\,\mathrm dt\) does not change to first order when the path is varied; the function \(L\) is the <em>Lagrangian</em>. For a free particle the only quantity that all observers, however they move, agree on along a path is the <em>proper time</em> \(\tau\), the time shown by a clock carried with the particle. Its increment is \(\mathrm d\tau=\mathrm dt\sqrt{1-v^2/c^2}=\mathrm dt/\gamma\) with \(\gamma=(1-v^2/c^2)^{-1/2}\). The simplest action built from it is \(S=-mc^2\int\mathrm d\tau\) (Landau and Lifshitz, <em>The Classical Theory of Fields</em>, §8; Jackson ch. 12), hence</p>
‹E lfree›L_0=-\frac{mc^2}{\gamma}=-mc^2\sqrt{1-\frac{v^2}{c^2}} .‹/E›
<p>For \(v\ll c\) the square root is \(1-v^2/2c^2-v^4/8c^4-\dots\), so \(L_0\approx-mc^2+\tfrac12mv^2\): up to a constant that does not influence the motion, the kinetic energy of Newton. The momentum conjugate to the velocity is \(\partial L_0/\partial v_i\). With \(\partial(v^2)/\partial v_i=2v_i\),</p>
\[ \frac{\partial L_0}{\partial v_i}=-mc^2\cdot\tfrac12\left(1-\frac{v^2}{c^2}\right)^{-1/2}\cdot\left(-\frac{2v_i}{c^2}\right)=\gamma m v_i , \]
<p>the relativistic momentum \(\mathbf p=\gamma m\mathbf v\).</p>
<h4><span class="psub__n">4.2</span>Adding the fields</h4>
<p>A charge \(q\) in an electrostatic potential \(\varphi\) has the potential energy \(q\varphi\), which enters \(L\) with a minus sign just as \(V\) does in \(L=T-V\). The magnetic field enters through the vector potential \(\mathbf A\), defined by \(\mathbf B=\nabla\times\mathbf A\), together with \(\mathbf E=-\nabla\varphi-\partial\mathbf A/\partial t\). The two terms \(-q\varphi+q\,\mathbf v\cdot\mathbf A\) are the time-and-space components of one four-vector product \(-q\int A_\mu\,\mathrm dx^\mu\), the only invariant that is linear in the potentials (Jackson §12.1; Landau and Lifshitz §16). We adopt it as the form of the interaction, and we test it by its consequences in the next subsection, which must give the Lorentz force and nothing else:</p>
‹E lag›L=-\frac{mc^2}{\gamma}-q\varphi+q\,\mathbf v\cdot\mathbf A,\qquad q=-e .‹/E›
<p>The <em>canonical momentum</em>, the derivative of \(L\) with respect to the velocity, is the free-particle momentum plus a term from the field:</p>
<div class="pbox"><span class="pbox__t">Key result · canonical momentum</span>
‹E canon›\mathbf p=\frac{\partial L}{\partial\mathbf v}=\gamma m\mathbf v+q\mathbf A .‹/E›
<p>The part \(\gamma m\mathbf v\) is the <em>kinetic momentum</em>: it is what a collision would transfer. The part \(q\mathbf A\) belongs to the field, and it depends on the choice of gauge (adding the gradient of any function to \(\mathbf A\) does not change \(\mathbf B\)). Chapter 4 will use \(\mathbf p\), not \(\gamma m\mathbf v\), where a symmetry of the lens fixes a conserved quantity.</p></div>
<h4><span class="psub__n">4.3</span>The Euler–Lagrange equation gives the Lorentz force</h4>
<p>Hamilton's principle becomes, coordinate by coordinate, the Euler–Lagrange equation \(\dfrac{\mathrm d}{\mathrm dt}\dfrac{\partial L}{\partial v_x}=\dfrac{\partial L}{\partial x}\) (the same equation as in the pendulum note of the simulations part of this site, derived there by varying the path). We write out the \(x\) component. The left side needs the time derivative of \(\gamma mv_x+qA_x\). \(A_x\) depends on the position, which changes along the path, and on time directly, so the chain rule gives \(\dfrac{\mathrm dA_x}{\mathrm dt}=\dfrac{\partial A_x}{\partial t}+v_x\dfrac{\partial A_x}{\partial x}+v_y\dfrac{\partial A_x}{\partial y}+v_z\dfrac{\partial A_x}{\partial z}\). The right side, the derivative of \(L\) with respect to \(x\) at fixed velocity, is \(-q\,\partial_x\varphi+q\,(v_x\partial_xA_x+v_y\partial_xA_y+v_z\partial_xA_z)\). Moving the \(A_x\) term across,</p>
\[ \frac{\mathrm d(\gamma mv_x)}{\mathrm dt}=-q\frac{\partial\varphi}{\partial x}-q\frac{\partial A_x}{\partial t}+q\Big[v_y\Big(\frac{\partial A_y}{\partial x}-\frac{\partial A_x}{\partial y}\Big)+v_z\Big(\frac{\partial A_z}{\partial x}-\frac{\partial A_x}{\partial z}\Big)\Big] . \]
<p>The terms \(v_x\partial_xA_x\) have cancelled between the two sides. The first two terms on the right are \(qE_x\). The brackets are components of \(\mathbf B=\nabla\times\mathbf A\): \(B_z=\partial_xA_y-\partial_yA_x\) and \(B_y=\partial_zA_x-\partial_xA_z\), so the last term is \(q\,(v_yB_z-v_zB_y)=q\,(\mathbf v\times\mathbf B)_x\). The \(y\) and \(z\) components follow by cyclic exchange of the letters.</p>
<div class="pbox"><span class="pbox__t">Key result · the force law of the whole project</span>
‹E lorentz›\frac{\mathrm d(\gamma m\mathbf v)}{\mathrm dt}=q\left(\mathbf E+\mathbf v\times\mathbf B\right),\qquad q=-e,\quad \gamma=\left(1-\frac{v^2}{c^2}\right)^{-1/2} .‹/E›
<p>The rate of change of the <em>relativistic</em> momentum equals the Lorentz force. For \(v\ll c\) it is Newton's law that ‹s:newton› used. The same steps were repeated for all three components by SymPy (checks D1a and D1b, ‹s:algebra›).</p></div>
'''))

    S.append(('c1-nr', 5, 'Energy, and why a magnetic field does no work', r'''
<h4><span class="psub__n">5.1</span>The Hamiltonian ★</h4>
<p>The <em>Hamiltonian</em> is \(H=\mathbf p\cdot\mathbf v-L\), the energy expressed through the canonical variables. With ‹eq:canon› and ‹eq:lag› the term \(q\,\mathbf v\cdot\mathbf A\) appears once with each sign and drops out:</p>
\[ H=\gamma mv^2+\frac{mc^2}{\gamma}+q\varphi=\gamma mc^2\Big(\frac{v^2}{c^2}+\frac1{\gamma^2}\Big)+q\varphi=\gamma mc^2+q\varphi , \]
<p>because \(1/\gamma^2=1-v^2/c^2\). The kinetic momentum is \(\gamma m\mathbf v=\mathbf p-q\mathbf A\), and \((\gamma mc^2)^2=m^2c^4+c^2|\gamma m\mathbf v|^2\) (check D2b), so as a function of the canonical momentum</p>
‹E ham›H(\mathbf r,\mathbf p,t)=\sqrt{m^2c^4+c^2\,|\mathbf p-q\mathbf A|^2}+q\varphi .‹/E›
<h4><span class="psub__n">5.2</span>Energy conservation</h4>
<p>Hamilton's equations give \(\mathrm dH/\mathrm dt=\partial H/\partial t\): the Hamiltonian changes along the path only through an explicit time dependence of the fields. In the static fields of this chapter there is none, so \(H\) is constant. Since \(H=\gamma mc^2+q\varphi\) and the electron's charge is \(-e\),</p>
<div class="pbox"><span class="pbox__t">Key result · energy and the gun</span>
‹E energy›(\gamma-1)\,mc^2-e\,\varphi(\mathbf r)=\text{const}\quad\Longrightarrow\quad \gamma=1+\frac{eV}{mc^2},\qquad v=c\sqrt{1-\frac1{\gamma^2}}‹/E›
<p>The second form is for an electron that starts at rest at the cathode, \(\varphi=0\), and has fallen through the potential difference \(V\): the energy it has gained is exactly \(eV\), and that is the definition of the unit <em>electron volt</em>. The speed follows from \(\gamma\).</p></div>
<p>The magnetic field never appears in \(H=\gamma mc^2+q\varphi\), so it cannot change the energy. The reason is also visible in the force: \(\mathbf v\cdot(q\,\mathbf v\times\mathbf B)=0\), a force at right angles to the motion does no work (SymPy D3b), and the energy theorem \(\mathrm d(\gamma mc^2)/\mathrm dt=\mathbf v\cdot\mathrm d(\gamma m\mathbf v)/\mathrm dt\) (D3a) then gives \(\mathrm d(\gamma mc^2)/\mathrm dt=q\,\mathbf E\cdot\mathbf v\) with no \(\mathbf B\) in it. Think of a stone swung on a string: the string pulls inwards at all times, the stone's speed does not change, the string's tension does no work. A magnetic field is such a string, and the electron's energy is only changed by electric fields. That is why a magnetic lens can focus without changing the beam energy, which chapter 4 exploits.</p>
<h4><span class="psub__n">5.3</span>The non-relativistic limit and the size of the correction</h4>
<p>For \(v\ll c\) the series of \(\gamma\) gives \((\gamma-1)mc^2=\tfrac12mv^2+\tfrac38mv^4/c^2+\dots\) (SymPy D4b), so the first term of ‹eq:energy› reduces to \(eV=\tfrac12mv^2\), the \(v_{NR}=\sqrt{2eV/m}\) that ‹ex:ex_tube› used. Write \(\epsilon=eV/mc^2\). Solving ‹eq:energy› for the speed and comparing with \(v_{NR}\) (D4a):</p>
‹E vratio›\frac{v}{v_{NR}}=1-\tfrac34\,\epsilon+\tfrac{23}{32}\,\epsilon^{2}-\dots‹/E›
<p>The non-relativistic speed is therefore too large by about three quarters of \(\epsilon\). The wave behaves the same way. With the de Broglie relation \(\lambda=h/p\) and the momentum from \((pc)^2=T(T+2mc^2)\) for a kinetic energy \(T=eV\),</p>
‹E lam›\lambda=\frac{h}{\sqrt{2meV\,\left(1+\dfrac{eV}{2mc^2}\right)}}=\lambda_{NR}\left(1-\tfrac14\epsilon+\dots\right) ,\qquad \lambda_{NR}=\frac{h}{\sqrt{2meV}} .‹/E›
<table class="ptab"><thead><tr><th>\(V\) (kV)</th><th>\(\epsilon=eV/mc^2\)</th><th>\(v/c\)</th><th>\(v/v_{NR}\)</th><th>\(\lambda\) (pm)</th><th>\(\lambda/\lambda_{NR}\)</th></tr></thead><tbody>
‹TABLE:nr›
</tbody></table>
<div class="pbox pbox--ex"><span class="pbox__t">‹X ex_30kv› · a 30 kV column</span>
<p>At \(V=30\ \mathrm{kV}\) the electron has \(\gamma=\)‹n:gamma_30000|5›, \(v=\)‹n:v_30000|4›&nbsp;m/s, \(v/c=\)‹n:beta_30000|3›. The non-relativistic formula gives \(v_{NR}=\)‹n:v_nr_30000|4›&nbsp;m/s, too large by ‹n:vdev_30k|2›&nbsp;%, and \(\lambda=\)‹n:lampm_30000|3›&nbsp;pm. The speed error reaches 1 % at \(V=\)‹n:V_1pct|3›&nbsp;V. A deflection goes as \(1/v^2\), so a calculation that uses \(\tfrac12mv^2\) is off by ‹n:defl_dev_30k|2›&nbsp;% for the column electron and by ‹n:defl_dev_2k|2›&nbsp;% for the electron of the 2 kV tube.</p></div>
'''))

    S.append(('c1-fields', 6, 'Where the fields come from', r'''
<p>Three field sources are enough for the tube; chapter 4 adds the lens.</p>
<p><em>Parallel plates.</em> Two large parallel plates a distance \(d\) apart at potential difference \(V\) have a potential that rises linearly from one to the other, \(\varphi(y)=Vy/d\), so \(\mathbf E=-\nabla\varphi\) is uniform with magnitude \(V/d\). This is the field of the gun between cathode and anode (\(V=V_a\), \(d=x_a\)) and of the deflection plates (\(V=V_p\)). It neglects the edges, where the field leaks out.</p>
<p><em>A pair of coils.</em> A circular loop of radius \(R\) carrying the current \(I\) produces on its axis, a distance \(z\) from its centre, a field along the axis. The Biot–Savart law says that a length \(\mathrm d\ell\) of the wire contributes \(\mathrm dB=\mu_0I\,\mathrm d\ell\,/(4\pi r^2)\) at the distance \(r=\sqrt{R^2+z^2}\), at right angles to the line to the point. By symmetry the components at right angles to the axis cancel round the loop; the axial component carries the factor \(R/r\). Integrating round the circumference \(2\pi R\), and taking \(N\) turns,</p>
‹E loop›B(z)=\frac{\mu_0 N I R^2}{2\left(R^2+z^2\right)^{3/2}} .‹/E›
<p>Two such coils a distance \(R\) apart, with the current in the same sense, form a <em>Helmholtz pair</em>. At the midpoint each coil is \(R/2\) away, and the two add to \(B=2\mu_0NIR^2/\big[2(5R^2/4)^{3/2}\big]\):</p>
‹E helm›B=\left(\tfrac45\right)^{3/2}\frac{\mu_0 N I}{R} ,\qquad \frac{\mathrm dB}{\mathrm dz}=\frac{\mathrm d^2B}{\mathrm dz^2}=0\ \text{at the midpoint}‹/E›
<p>The derivatives of the sum of two terms \(‹eq:loop›\) vanish there (SymPy D11a, D11b), so the field is uniform over a region that is long compared with the offset. For \(N=100\) turns of radius \(R=50\ \mathrm{mm}\) at \(I=1\ \mathrm A\), ‹eq:helm› gives \(B=\)‹n:helm_example|3›&nbsp;T; Thomson's coils were of this type, and he calibrated their field with a small coil and a ballistic galvanometer rather than from a formula.</p>
<p><em>A long solenoid.</em> Ampère's law applied to a long coil with \(n\) turns per metre gives a uniform axial field \(B=\mu_0nI\) inside. The model of ‹s:helix› just sets \(B_\parallel\) as a number.</p>
<p>In every case the electron model reads the field from a function of position and, in later chapters, from a numerical solution. Textbook for these formulas: Griffiths, <em>Introduction to Electrodynamics</em>, ch. 5.</p>
'''))

    S.append(('c1-helix', 7, 'A uniform axial field: the helix', r'''
<p class="psec__lead">A ball rolled round the inside of a funnel winds round and round while it moves along the axis. A uniform magnetic field along the tube does the same to an electron that does not start exactly on the axis.</p>
<p>Let the field point along \(\hat{\mathbf b}\), constant in space, with no electric field. By ‹s:nr› the energy stays constant, hence so does \(\gamma\), and the equation of motion ‹eq:lorentz› for \(\mathbf u=\gamma\mathbf v\) becomes the linear equation</p>
‹E helixeq›\frac{\mathrm d\mathbf u}{\mathrm dt}=\Omega\,\mathbf u\times\hat{\mathbf b},\qquad \Omega=\frac{qB}{\gamma m}\ \ (\text{negative for the electron}) .‹/E›
<p>Split \(\mathbf u\) into the part \(u_\parallel\) along \(\hat{\mathbf b}\) and the part \(\mathbf u_\perp\) across it. The cross product has no component along \(\hat{\mathbf b}\), so \(u_\parallel\) stays constant. Take \(\hat{\mathbf b}=\hat{\mathbf z}\) and combine the two transverse components into one complex number \(w=u_x+\mathrm iu_y\). Then \(\mathrm dw/\mathrm dt=\Omega(u_y-\mathrm iu_x)=-\mathrm i\Omega w\), whose solution is \(w=w_0\,\mathrm e^{-\mathrm i\Omega t}\): a vector of fixed length that turns with the angular frequency \(\Omega\). In real form, with the electron at the origin at \(t=0\) and \(\gamma\) constant,</p>
‹E helixsol›\mathbf u_\perp(t)=\mathbf u_{\perp0}\cos\Omega t+\left(\mathbf u_{\perp0}\times\hat{\mathbf b}\right)\sin\Omega t,\qquad \mathbf r(t)=\frac1\gamma\Big[u_\parallel t\,\hat{\mathbf b}+\mathbf u_{\perp0}\frac{\sin\Omega t}{\Omega}+\left(\mathbf u_{\perp0}\times\hat{\mathbf b}\right)\frac{1-\cos\Omega t}{\Omega}\Big] .‹/E›
<p>Differentiating shows that this solves ‹eq:helixeq› and \(\dot{\mathbf r}=\mathbf u/\gamma\) (SymPy D7a, D7b). The transverse motion is a circle through the starting point of radius \(r_L=|\mathbf u_{\perp0}|/(\gamma|\Omega|)\) (D7c), which is</p>
<div class="pbox"><span class="pbox__t">Key result · gyroradius and the helix</span>
‹E rl›r_L=\frac{\gamma m v_\perp}{eB}=\frac{p_\perp}{eB},\qquad T=\frac{2\pi}{|\Omega|}=\frac{2\pi\gamma m}{eB},\qquad \text{pitch}=v_\parallel T .‹/E›
<p>Slow electrons give back ‹eq:circle›. The relativistic factor \(\gamma\) lengthens the period: a fast electron needs a little longer for a turn. Combined with the steady motion along the field the path is a <em>helix</em> of radius \(r_L\) and pitch \(v_\parallel T\).</p></div>
<p>Now send electrons from one point of the axis in slightly different directions, each making a small angle \(\alpha\) with the axis. They have almost the same \(v_\parallel\) and the same period \(T\), whatever their \(\alpha\), so after one turn all of them are back on the axis, at the same distance</p>
‹E focus›L=v_\parallel T=\frac{2\pi\gamma m v_\parallel}{eB} .‹/E›
<p>This is a lens. Electrons spread out from a point and reunite at another point, because they all need the same time to complete a turn. With \(V_a=\)‹n:Va|4›&nbsp;V and \(B_\parallel=4\ \mathrm{mT}\), ‹eq:focus› gives \(L=\)‹n:focus_L_2000_4mT|4›&nbsp;m; an electron leaving at \(\alpha=60\ \mathrm{mrad}\) circles with \(r_L=\)‹n:rL_4mT_alpha06|3›&nbsp;m. ‹fig:helix› shows six of them. A real magnetic lens, chapter 4, is a short coil whose field rises and falls along the axis, and it twists the beam by the angle it gains while crossing: this helix is its seed.</p>
<figure class="pfig">
  <div class="pfig__plate">‹SVG:helix›</div>
  <figcaption>‹F helix›One electron of \(V_a=2\) kV in \(B_\parallel=4\) mT at \(\alpha=60\) mrad to the field, computed by the solver of the chapter, and the same path turned about \(\mathbf B\) in steps of \(60^\circ\), which the symmetry of the field allows: six electrons leaving one point in six directions. Left: side view, the vertical axis stretched. Right: end view, six circles that all pass through the axis. The dashed line marks the focus at \(L=2\pi v_\parallel/\Omega\).</figcaption>
</figure>
'''))
    return S


def sections_c():
    S = []
    S.append(('c1-numerics', 8, 'Following the electron on a computer: Runge–Kutta and Boris', r'''
<p class="psec__lead">Pencil and paper solve a uniform field. A lens, a plate with fringe fields or a gun with space charge need a computer that moves the electron a short time step \(h\) at a time. Two methods do the work in this project, and they fail in different ways.</p>
<p>The state of the electron is \((\mathbf r,\mathbf u)\) with \(\mathbf u=\gamma\mathbf v\). ‹eq:lorentz› written for it reads</p>
‹E ode›\dot{\mathbf r}=\frac{\mathbf u}{\gamma},\qquad \dot{\mathbf u}=\frac{q}{m}\Big(\mathbf E(\mathbf r)+\frac{\mathbf u}{\gamma}\times\mathbf B(\mathbf r)\Big),\qquad \gamma=\sqrt{1+\frac{|\mathbf u|^2}{c^2}} ,‹/E›
<p>which is the form both integrators advance. We test both against the exact helix of ‹eq:helixsol›, because there the right answer is known for every time.</p>
<h4><span class="psub__n">8.1</span>Classical Runge–Kutta (RK4)</h4>
<p>For \(\dot{\mathbf y}=\mathbf f(\mathbf y)\) the classical fourth-order step uses four slopes, one at the start, two at the midpoint (the second improved by the first) and one at the end, and combines them with weights \(1,2,2,1\):</p>
‹E rk4›\mathbf y_{n+1}=\mathbf y_n+\frac h6\left(\mathbf k_1+2\mathbf k_2+2\mathbf k_3+\mathbf k_4\right),\quad \mathbf k_1=\mathbf f(\mathbf y_n),\ \mathbf k_2=\mathbf f(\mathbf y_n+\tfrac h2\mathbf k_1),\ \mathbf k_3=\mathbf f(\mathbf y_n+\tfrac h2\mathbf k_2),\ \mathbf k_4=\mathbf f(\mathbf y_n+h\mathbf k_3) .‹/E›
<p>Its local error per step is of order \(h^5\) and, accumulated over \(1/h\) steps, its global error is of order \(h^4\) (Hairer, Nørsett and Wanner, <em>Solving Ordinary Differential Equations I</em>, §II.1 for the order conditions). It needs four evaluations of the fields per step.</p>
<p>What RK4 does to a rotation we can compute exactly, because the magnetic motion is the linear equation \(\dot w=-\mathrm i\Omega w\). One RK4 step multiplies \(w\) by the polynomial of the exponential, \(R(\mathrm i\theta)=1+\mathrm i\theta-\theta^2/2-\mathrm i\theta^3/6+\theta^4/24\) with \(\theta=\Omega h\). The true factor \(\mathrm e^{-\mathrm i\theta}\) has length 1. The length of \(R\) is, by expanding (SymPy D10a),</p>
‹E rk4amp›|R|^2=1-\frac{\theta^6}{72}+\frac{\theta^8}{576},\qquad \theta-\arg R=\frac{\theta^5}{120}-\frac{\theta^7}{336}+\dots‹/E›
<p>The first expression is smaller than 1: every step shrinks the circle a little. The electron <em>loses energy</em> to the method although nothing in the physics takes any. With \(N=2\pi/\theta\) steps per turn the loss in \(n\) turns is \(1-|R|^{2Nn}\) of \(u_\perp^2\) (D10b gives the phase error). For \(N=16\) the loss is ‹n:rk4_loss_per_turn_16_pct|2›&nbsp;% per turn, and the electron has lost half its energy after ‹n:rk4_half_turns_16|3› turns. For \(N=64\) it takes ‹n:rk4_turns_1pct_loss_64|3› turns to lose 1 %.</p>
<h4><span class="psub__n">8.2</span>The Boris pusher ★</h4>
<p>Boris (1970) gave the method that plasma and beam codes still use. It splits the step into what the electric field does, a push, and what the magnetic field does, a rotation. The electric push is applied in two halves, before and after the rotation, which makes the scheme symmetric in time and therefore of second order. The velocity \(\mathbf u\) lives at the half steps and the position at the whole steps (leapfrog), and with \(a=qh/(2m)\):</p>
‹E boris›\mathbf u^-=\mathbf u_{n-1/2}+a\mathbf E,\qquad \mathbf u'=\mathbf u^-+\mathbf u^-\times\mathbf t,\qquad \mathbf u^+=\mathbf u^-+\mathbf u'\times\mathbf s,\qquad \mathbf u_{n+1/2}=\mathbf u^++a\mathbf E ,‹/E›
<p>with \(\mathbf t=a\mathbf B/\gamma^-\), \(\gamma^-=\sqrt{1+|\mathbf u^-|^2/c^2}\) and \(\mathbf s=2\mathbf t/(1+t^2)\); then \(\mathbf r_{n+1}=\mathbf r_n+h\,\mathbf u_{n+1/2}/\gamma_{n+1/2}\). The two middle steps are the rotation. We show what they do in the plane normal to \(\mathbf B\), with \(\mathbf t=t\,\hat{\mathbf z}\) and \(\mathbf u^-=(u_x,u_y)\). Then \(\mathbf u^-\times\mathbf t=(u_yt,-u_xt)\), so \(\mathbf u'=(u_x+tu_y,\ u_y-tu_x)\), and with \(\mathbf s=s\,\hat{\mathbf z}\), \(s=2t/(1+t^2)\),</p>
\[ u^+_x=u_x(1-st)+s\,u_y,\qquad u^+_y=u_y(1-st)-s\,u_x . \]
<p>Because \(1-st=(1-t^2)/(1+t^2)\), the pair \((1-st,\ s)\) is \((\cos\varphi,\sin\varphi)\) with \(t=\tan(\varphi/2)\): the two steps turn the vector by exactly the angle \(\varphi\) (SymPy D8c; for \(\mathbf t\) in any direction D8a shows the same with Rodrigues' rotation formula). A rotation does not change a length, so \(|\mathbf u^+|=|\mathbf u^-|\) exactly (D8b). The true angle per step is \(\Omega h\); Boris turns by \(\varphi=2\arctan(\Omega h/2)\), which differs by</p>
‹E borisphase›\Omega h-2\arctan\frac{\Omega h}2=\frac{(\Omega h)^3}{12}-\frac{(\Omega h)^5}{80}+\dots‹/E›
<p>per step (D9b). That is a <em>phase error</em>: the electron goes round slightly too slowly, and the error grows with the number of turns, of order \(h^2\) in all. The <em>energy</em> is another matter. In a pure magnetic field the rotation keeps \(|\mathbf u|\) exactly, so the energy does not drift however many turns are computed. The position update uses the chord \(h\,\mathbf v\), not the arc, so the path is a regular polygon with turning angle \(\varphi\) and chord \(h v=(\Omega h)\,r_L\); the polygon's circumscribed circle has radius \(\text{chord}/2\sin(\varphi/2)\), that is</p>
‹E borisr›r_{\text{Boris}}=r_L\sqrt{1+\left(\frac{\Omega h}{2}\right)^2}‹/E›
<p>(D9a). The radius is off by a fixed fraction and does not drift: ‹n:boris_factor_16|5› of \(r_L\) at 16 steps per turn, ‹n:boris_factor_64|5› at 64. With an electric field present the energy is not exactly constant, but the error stays bounded and does not grow in time; Qin and co-workers (<em>Physics of Plasmas</em> 20, 084503, 2013) explain why, from the fact that the step preserves phase-space volume.</p>
<h4><span class="psub__n">8.3</span>Both against the exact helix</h4>
<p>We start an electron of \(V=2\ \mathrm{kV}\) in \(B=10\ \mathrm{mT}\) at \(\chi=1.2\) rad to the field, so that it circles with \(r_L=\)‹n:rL_test|4›&nbsp;m, and follow it for 20 turns of period \(T=\)‹n:T_test|4›&nbsp;s with \(N\) steps per turn. The table gives the distance between computed and exact position after 20 turns in units of \(r_L\) and the relative change of the kinetic energy over the run (for RK4 the loss, for Boris the signed noise). The "predicted" columns are not fits: the Boris phase error accumulated over \(20N\) steps is \(20N\,(\theta-2\arctan\frac\theta2)\), the RK4 one \(20N(\theta-\arg R)\), and the RK4 energy loss is \(\sin^2\chi\,\big(1-(|R|^2)^{20N}\big)\) from ‹eq:rk4amp› (only the transverse part of \(\mathbf u\) shrinks).</p>
<table class="ptab"><thead><tr><th>\(N\)</th><th>Boris, error</th><th>Boris, predicted</th><th>RK4, error</th><th>RK4, predicted</th><th>RK4 energy</th><th>RK4 energy, predicted</th><th>Boris energy</th></tr></thead><tbody>
‹TABLE:tests›
</tbody></table>
<p>The position error of Boris falls with slope ‹n:slope_boris_pos|3› in \(\log N\) (between \(N=64\) and \(256\)), as \(h^2\) predicts; the RK4 error falls with slope ‹n:slope_rk4_pos|3›, as \(h^4\) predicts; the RK4 energy error falls with slope ‹n:slope_rk4_energy|3›, one power faster than the position error, as ‹eq:rk4amp› predicts. The energy of Boris stays at the noise of 64-bit arithmetic in every case, the last column. At \(N=64\) the predicted position error of Boris is within ‹n:pred_gap_boris_64_pct|2›&nbsp;% of the measured one, and the prediction improves with \(N\); for RK4 the prediction is within a few per cent, because its total error is not only phase error.</p>
<figure class="pfig">
  <div class="pfig__plate">‹SVG:integrators›</div>
  <figcaption>‹F integrators›The test of the table as a picture, computed with the reference solver <code>ref/ch01.py</code>: the distance from the exact helix after 20 turns, in gyroradii (left), and the change of the kinetic energy over the run (right), against the number of steps per turn. Both axes are logarithmic. The error of Boris falls with slope −2, that of RK4 with slope −4 (position) and −5 (energy); the energy of Boris stays at the noise of 64-bit arithmetic.</figcaption>
</figure>
<div class="pbox"><span class="pbox__t">Key result · which to use</span>
<p><strong>RK4</strong> is much more accurate per step: at \(N=64\) its error is ‹n:tst_rk4_64_err|3› of \(r_L\), against ‹n:tst_boris_64_err|3› for Boris. But RK4 loses energy steadily, at a rate set by \(\Omega h\). <strong>Boris</strong> uses one field evaluation per step instead of four, keeps the energy and the radius bounded however long it runs, and its error is a phase error that does not distort the shape of the orbit. We use RK4 for short paths where accuracy counts and Boris for the many-turn paths of later chapters, and we check each result against the other.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">‹X ex_equalwork› · the same work</span>
<p>RK4 at \(N=16\) uses ‹n:work_rk4_16|2› field evaluations per turn; Boris at \(N=64\) uses 64. At that equal cost the RK4 error after 20 turns is ‹n:tst_rk4_16_err|3› of \(r_L\) and the Boris error ‹n:tst_boris_64_err|3›: RK4 is ahead in position. It has paid for it with ‹n:tst_rk4_16_loss_pct|3›&nbsp;% of its energy; Boris none.</p></div>
'''))

    S.append(('c1-thomson', 9, 'Thomson\'s tube, simulated and compared with Thomson\'s data', r'''
<p>The simulation at the end of the chapter follows the electron of ‹s:numerics› through uniform fields, with every symbol of the chapter a slider. With \(B\) at zero and \(E\) at the value of the worked example the path is the parabola of ‹fig:motions›. With \(E\) at zero and the velocity at a right angle to \(B\) it is the circle; at a small angle to \(B\), the helix of ‹s:helix›. With \(E=vB\) and a right angle between them the electron goes straight on, Thomson's balance. The integrator and its time step are sliders too, so the errors of ‹s:numerics› can be provoked by hand: a step of a tenth of a period makes the energy error of RK4 visible within a few turns.</p>
<h4><span class="psub__n">9.1</span>The method recovers \(e/m\) from the simulation</h4>
<p>We repeat Thomson's second method on the computer. The deflection with only the electric field is measured on the path <em>after</em> the plates; the magnetic field that brings the spot back to the axis is \(B=E/v_0=\)‹n:B_balance|4›&nbsp;T; and ‹eq:em› gives \(e/m=\theta E/(B^2l)=\)‹n:em_inferred|5›&nbsp;C/kg, from the angle \(\theta=\)‹n:theta_sim|4›&nbsp;rad of the simulated path. The value the simulation was run with is \(e/m=\)‹n:e_over_m|5›&nbsp;C/kg. The method returns it to ‹n:em_ratio_dev|2›&nbsp;%. The deficit has a known cause, and it is the physics of ‹s:nr› showing through. ‹eq:em› assumes a small angle and a non-relativistic electron. With the relativistic momentum the angle of the path is \(\theta=\arctan\big(eEl/(\gamma mv^2)\big)\), as in ‹s:newton› after the correction for \(\gamma\). So the measured \(\theta\) is smaller than \(eEl/mv^2\) by two factors: the electron is heavier by \(\gamma=\)‹n:gamma_2000|6›, which costs \(1/\gamma=\)‹n:gamma_factor|5›; and an angle is smaller than its tangent \(y=\)‹n:tan_theta_rel|4›, which costs \(\arctan y/y=\)‹n:atan_factor|5›. Their product ‹n:em_pred_decomp|5› matches the measured ratio ‹n:em_ratio|5› to ‹n:decomp_gap|2›. Multiplying the inferred value by \(\gamma\) alone brings the ratio to ‹n:em_ratio_rel_corrected|5›, and the remainder is the arctangent.</p>
<h4><span class="psub__n">9.2</span>Thomson's own numbers</h4>
<p>The 1897 paper (J. J. Thomson, <em>Philosophical Magazine</em> 44, 293) gives two tables of \(m/e\) in CGS electromagnetic units, from two methods. The first measures the energy the beam deposits on a thermocouple and the charge it brings into a cylinder, and the radius of its path in a magnetic field; it gives \(m/e=I^2Q/2W\) with \(I=H\rho\). The second is the crossed-field method of ‹s:newton›. We typed in all ‹n:n_m1|2› rows of the first table and all ‹n:n_m2|1› of the second, from the transcription of C. J. Giunta (Le Moyne College) of the original, converted them to SI (\(1\ \mathrm{g/abC}=10^{-4}\ \mathrm{kg/C}\)), and plot \(e/m\) in ‹fig:th1897› (data and provenance: <code>data/ch01/thomson1897.json</code>).</p>
<figure class="pfig">
  <div class="pfig__plate">‹SVG:th1897›</div>
  <figcaption>‹F th1897›Every value of \(e/m\) in Thomson's two tables (1897) against the CODATA 2018 value (green). Each dot is a row of his tables. Triangles mark the mean of each row. The first method was run on three tubes; his tube 3 has small circular holes in place of slits.</figcaption>
</figure>
<p>The result is a plain statement of how far an early measurement lies from the modern one. The first method gives \(e/m\) between ‹n:m1_min_ratio|2› and ‹n:m1_max_ratio|3› times CODATA, with a mean of ‹n:m1_mean_ratio|3› (tubes 1 and 2: ‹n:m1_tube12_ratio|3›; tube 3: ‹n:m1_tube3_ratio|2›). The second method gives ‹n:m2_min_ratio|2› to ‹n:m2_max_ratio|2› times CODATA, mean ‹n:m2_mean_ratio|2›: the value of \(e/m\) is too small by a factor of about two. In his text Thomson says that he judges the first-method values for tubes 1 and 2 too large in \(e/m\), because charge leaks from the inner cylinder through the conducting gas, and that the uncertainty of the radius \(\rho\) alone is about 20 per cent. The data show the first part: tubes 1 and 2 lie above CODATA, tube 3 below. Why the second method is low by a factor of two is not stated in the paper text that we read, and we have not tested a cause: a non-uniform or badly calibrated \(B\) over the plates and fringe fields at their edges (‹s:model›) are candidates. The point that the paper does support is the one he drew: all gases and electrode metals give the same \(m/e\), of order \(10^{-7}\) in his units, about a thousandth of \(10^{-4}\), the smallest value known before, that of the hydrogen ion in electrolysis. He notes that the smallness of \(m/e\) may come from a small \(m\) or a large \(e\), and argues from Lenard's measurements that the carriers are small compared with ordinary molecules.</p>
<p>Our simulation recovers \(e/m\) because it contains none of the things that troubled the experiment: no gas, a perfectly uniform field, no uncertainty in the field's strength or the beam's path. Comparing a model with data teaches something only where the two differ by more than the data's own scatter. Thomson's rows of the first method spread over a factor ‹n:m1_spread|2›, and the second method sits a factor of two from the truth, against the ‹n:em_ratio_dev|2›&nbsp;% deficit of the idealised model, which has a known cause. We also checked Thomson's arithmetic. His columns obey \(m/e=I^2Q/2W\) in all rows of the first table but one, with a median deviation of ‹n:m1_median_dev_pct|2›&nbsp;% and a largest deviation of ‹n:m1_good_maxdev_pct|2›&nbsp;%, the size of the rounding of a one- or two-digit entry. In one row (hydrogen, tube 1, \(W/Q\) printed as \(6\times10^{12}\)) the printed \(W/Q\) disagrees by a factor of ‹n:m1_bad_ratio|3› with the same row's \(m/e\) and \(v\); the \(m/e\) and \(v\) agree with \(W/Q=6\times10^{11}\), so the transcription or the original has a misprint in that cell. We used the printed \(m/e\) column throughout.</p>
'''))

    S.append(('c1-algebra', 10, 'Checked by computer algebra', r'''
<p>Every derivation of this chapter was repeated by SymPy, as an identity in exact algebra: the claim is built from the symbols of the text and the difference of the two sides must simplify to zero. The table is the output of <code>derive/ch01.py</code>, run when this page is built. A claim is never marked PASS because a number looked right; the checks use no numbers.</p>
<table class="ptab"><thead><tr><th>check</th><th>result</th><th>claim</th></tr></thead><tbody>
‹TABLE:sympy›
</tbody></table>
<p>The numbers of the chapter were checked the other way round. The module of the page, <code>physics/ch01.js</code>, and an independent NumPy implementation, <code>ref/ch01.py</code>, are run on the same cases by <code>checks/check_parity.py</code>, and every number quoted in the prose is computed by both (<code>checks/check_numbers.py</code>): the printed strings must be identical. The two are float64 and use the same algorithm, so what remains is rounding. The energy change of a run is a difference of two nearly equal numbers; it is compared with an absolute floor that the module states, and every other output agrees to rounding.</p>
'''))

    S.append(('c1-limits', 11, 'What the model leaves out, and what we pass on', r'''
<p>The model has a short list of things it does not contain. <em>Fringe fields</em> of the plates (‹s:model›): the largest error of the tube model, repaired by a field solver in chapter 4. <em>Space charge</em>: electrons repel each other, and at the currents of an electron column the repulsion widens the beam; chapter 5 returns to it. <em>The source</em>: the electron here starts at rest from a point; a real cathode emits a spread of energies and directions, and chapter 2 describes them. <em>Spin and radiation</em>: negligible here, with ‹n:larmor_ratio|2› of the energy radiated. <em>Gas</em>: a vacuum. The next, more complete model for an electron in given fields is a field solver for \(\mathbf E,\mathbf B\) from the electrodes and coils, with the same pusher; chapter 4 builds it for the lens.</p>
<div class="pbox"><span class="pbox__t">Hand-over to chapter 2</span>
<p>Chapter 2 receives from this chapter: (1) the force law ‹eq:lorentz› with \(q=-e\), the one equation that moves every electron in the project; (2) the energy relation ‹eq:energy›, so that an electron that starts at rest at a surface and falls through \(V\) has \(\gamma=1+eV/mc^2\), which chapter 3 turns into the gun; (3) the Boris and RK4 steppers of <code>physics/ch01.js</code>, with the measured error laws of ‹s:numerics›, to follow electrons through any given field; (4) the helix ‹eq:helixsol› as the seed of the magnetic lens of chapter 4. Chapter 2 supplies the other end of the column: how many electrons leave the tip per second, with what spread of energy, from how small a spot. The electron of this chapter, that leaves a point at rest, becomes there a stream with a current and a brightness.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span>
<ol>
<li>Show that the straight line leaving the plates, traced backwards, meets the axis at the centre of the plates (SymPy D5a does it; do it by hand from ‹eq:par›).</li>
<li>For which anode voltage does the relativistic speed fall 1 % below the non-relativistic one? (Solve \(v/v_{NR}\approx1-\tfrac34\epsilon=0.99\); the exact answer of the code is ‹n:V_1pct|3›&nbsp;V.)</li>
<li>Show that \(\mathbf u^+\) in ‹eq:boris› has the same length as \(\mathbf u^-\) for an arbitrary direction of \(\mathbf t\), starting from \(|\mathbf u'|^2=|\mathbf u^-|^2(1+t^2)\) when \(\mathbf u^-\perp\mathbf t\).</li>
<li>An electron of 30 kV in a field of 1 mT has \(r_L=\)‹n:rL_30k_1mT|3›&nbsp;m (use ‹eq:rl›). How many field evaluations per turn does Boris need to keep its radius within 0.1 % of \(r_L\) (‹eq:borisr›)? Answer: at least ‹n:boris_Nmin_01pct|3› steps, which is rounded up to the next whole number.</li>
</ol></div>
<h4><span class="psub__n">11.1</span>Sources</h4>
<p>Opened and read in the course of writing this chapter: J. J. Thomson, <em>Cathode Rays</em>, Phil. Mag. 44 (1897) 293, in C. J. Giunta's transcription (<code>https://web.lemoyne.edu/~giunta/thomson1897.html</code>); the IEEE International Roadmap for Devices and Systems 2022, <em>More Moore</em> (Table MM-7) and <em>Lithography</em>; the public product page and press release of Applied Materials cited in chapter 0. The CODATA 2018 value \(e/m_e\) is from Tiesinga et al., Rev. Mod. Phys. 93, 025010 (2021). The formulas of the derivations are the standard ones and were re-derived above and checked by SymPy; the textbooks they follow, named where they occur, were not re-read for this chapter: Jackson, <em>Classical Electrodynamics</em>, ch. 12 and 14; Landau and Lifshitz, <em>The Classical Theory of Fields</em>, §§8, 16, 17; Griffiths, <em>Introduction to Electrodynamics</em>, ch. 5; Hairer, Nørsett and Wanner, <em>Solving Ordinary Differential Equations I</em>, §II.1; J. P. Boris, <em>Proc. 4th Conf. Numerical Simulation of Plasmas</em> (1970); Qin et al., <em>Phys. Plasmas</em> 20, 084503 (2013).</p>
'''))
    return S



# ============================================================================================================ conversion of the prose
FIGS = {}
_EXN = {}
USED_NUMS = set()


def _tables():
    nr = '\n'.join('<tr><td>‹n:Vk_%d|3›</td><td>‹n:eVmc2_%d|3›</td><td>‹n:beta_%d|4›</td><td>‹n:vratio_%d|4›</td><td>‹n:lampm_%d|4›</td><td>‹n:lamratio_%d|4›</td></tr>' % ((V,) * 6) for V in VS)
    tests = '\n'.join('<tr><td>‹n:Ns_%d|3›</td><td>‹n:tst_boris_%d_err|3›</td><td>‹n:pbe_%d|3›</td><td>‹n:tst_rk4_%d_err|3›</td><td>‹n:pre_%d|3›</td>'
                      '<td>‹n:tst_rk4_%d_loss|3›</td><td>‹n:pe_rk4_%d|3›</td><td>noise</td></tr>' % ((N,) * 7) for N in NS)
    import sympy
    rows = DERIVE.run()
    sy = '\n'.join('<tr><td><code>%s</code></td><td>%s</td><td>$%s$</td></tr>' % (r['label'], 'PASS' if r['ok'] else '<b>FAIL</b>', r['tex']) for r in rows)
    return nr, tests, sy, sympy.__version__


T_NR, T_TESTS, T_SYMPY, SYMPY_V = _tables()


def _number_markup(html):
    """‹n:name|digits› becomes {{numtex:..}} inside maths and {{num:..}} in prose, with that many significant figures."""
    parts = re.split(r'(\$\$.*?\$\$|\$[^$]*?\$)', html, flags=re.S)
    pat = re.compile(r'‹n:([^|›]+)\|(\d+)›')

    def one(tex):
        def f(m):
            name = num_name(m.group(1), int(m.group(2)))
            USED_NUMS.add(name)
            return '{{%s:%s}}' % ('numtex' if tex else 'num', name)
        return f
    for i, p in enumerate(parts):
        parts[i] = pat.sub(one(i % 2 == 1), p)
    return ''.join(parts)



def _inline_sqrt(tex):
    """In running text a radical is written (..)^{1/2}: a wide inline radical draws an SVG tail that the page check counts as overflow."""
    while True:
        i = tex.find('\\sqrt{')
        if i < 0:
            return tex
        j, depth = i + 6, 1
        while depth:
            depth += {'{': 1, '}': -1}.get(tex[j], 0)
            j += 1
        tex = tex[:i] + '\\left(' + tex[i + 6:j - 1] + '\\right)^{1/2}' + tex[j:]


def _inline_math(html):
    parts = re.split(r'(\$\$.*?\$\$|\$[^$]*?\$)', html, flags=re.S)
    for i, p in enumerate(parts):
        if i % 2 == 1 and not p.startswith('$$'):
            parts[i] = '$' + _inline_sqrt(p[1:-1]) + '$'
    return ''.join(parts)


def _text(html):
    html = html.replace('‹TABLE:nr›', T_NR).replace('‹TABLE:tests›', T_TESTS).replace('‹TABLE:sympy›', T_SYMPY).replace('‹SYMPY›', SYMPY_V)
    html = re.sub(r'<span class="psub__n">[^<]*</span>', '', html)
    html = re.sub(r'section ‹s:([a-z0-9_]+)›', r'{{sec:ch01-\1}}', html)
    html = re.sub(r'‹s:([a-z0-9_]+)›', r'{{sec:ch01-\1}}', html)
    html = re.sub(r'‹E ([a-z0-9_]+)›(.*?)‹/E›', lambda m: '$$%s \\label{%s}$$' % (m.group(2).strip(), m.group(1)), html, flags=re.S)
    html = re.sub(r'\\\[(.*?)\\\]', lambda m: '$$%s \\notag$$' % m.group(1).strip(), html, flags=re.S)
    html = re.sub(r'\\\((.*?)\\\)', lambda m: '$%s$' % m.group(1), html, flags=re.S)
    html = re.sub(r'‹eq:([a-z0-9_]+)›', r'{{eq:\1}}', html)
    html = re.sub(r'‹fig:([a-z0-9_]+)›', r'{{fig:\1}}', html)

    def exdef(m):
        _EXN[m.group(1)] = len(_EXN) + 1
        return 'Example 1.%d' % _EXN[m.group(1)]
    html = re.sub(r'‹X ([a-z0-9_]+)›', exdef, html)
    html = re.sub(r'‹ex:([a-z0-9_]+)›', lambda m: 'Example 1.%d' % _EXN[m.group(1)], html)
    html = re.sub(r'<code>(.*?)</code>', lambda m: '<code>' + m.group(1).replace('/', '/<wbr>') + '</code>', html)   # long paths may break
    return _number_markup(_inline_math(html))


FIGBLK = re.compile(r'<figure class="pfig">\s*<div class="pfig__plate">‹SVG:([a-z0-9_]+)›</div>\s*<figcaption>‹F ([a-z0-9_]+)›(.*?)</figcaption>\s*</figure>', re.S)


def convert(html):
    def fig(m):
        FIGS[m.group(2)] = {'svg': FIG_SVG[m.group(1)](), 'caption': None, '_cap': m.group(3)}
        return '{{figure:%s}}' % m.group(2)
    html = FIGBLK.sub(fig, html)
    return _text(html)


def _closure(names):
    seen = set()
    stack = list(names)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(NUMS[n].get('of', {}).values())
    return seen


def _build():
    secs = sections() + sections_b() + sections_c()
    out = []
    for anchor, num, title, html in secs:
        out.append({'id': anchor[3:], 'title': title.replace('★', '').strip(), 'html': convert(html), 'star': '★' in title})
    for f in FIGS.values():
        f['caption'] = _text(f.pop('_cap'))
    return out


SECTIONS = _build()
NUMBERS = {k: NUMS[k] for k in sorted(_closure(USED_NUMS))}

# Typed values in the prose, each with what it is. Numbers computed by the page are never listed here (check_numbers.py would not need them).
LITERALS = {}


def lit(phrase, reason):
    LITERALS[phrase] = reason


# Typed values in the prose: sources quoted, citations, givens of the worked examples, the labels of worked examples. Each says what it is.
lit('1.5 cm', 'Thomson (1897): his plates were about 5 cm long, 2 cm broad and 1.5 cm apart, quoted from the paper')
lit('30 kV', 'the column voltage of a typical electron-beam instrument, a given of the examples')
lit('2 kV tube', 'the anode voltage of the model tube of the worked example, a given of the problem')
lit('4 mT', 'the solenoid field of the helix example, a given of the problem')
lit('1 mT', 'the field of problem 4, a given of the problem')
lit('0.1 %', 'the tolerance asked for in problem 4, a given of the problem')
lit('Example 1.1', 'the label of the first worked example')
lit('Example 1.2', 'the label of the second worked example')
lit('Example 1.3', 'the label of the third worked example')
lit('ch. 12', 'chapter of Jackson, Classical Electrodynamics, cited for the relativistic Lagrangian')
lit('ch. 14', 'chapter of Jackson, Classical Electrodynamics, cited for the Larmor formula')
lit('ch. 12 and 14', 'chapters of Jackson, Classical Electrodynamics, cited for the Lagrangian and the Larmor formula')
lit('§12.1', 'section of Jackson, Classical Electrodynamics, cited for the Lagrangian of a charge')
lit('§16', 'section of Landau and Lifshitz, The Classical Theory of Fields, cited for the action of a charge')
lit('§§8, 16, 17', 'sections of Landau and Lifshitz, The Classical Theory of Fields, cited')
lit('20, 084503, 2013', 'Qin et al., Physics of Plasmas, volume 20, article 084503 (2013), cited')
lit('20, 084503', 'Qin et al., Physics of Plasmas, volume 20, article 084503 (2013), cited')
lit('20 turns', 'the number of turns of the integrator test, a given of the test')
lit('64-bit', 'the word length of double-precision arithmetic')
lit('16 steps per turn', 'the step count of the example, a given of the example')
lit('at 64', 'the step count of the comparison, a given of the example')
lit('uses 64', 'the number of field evaluations of Boris at 64 steps per turn: one per step, by the definition of the method')
lit('44, 293', 'Thomson, Philosophical Magazine volume 44, first page 293 (1897), cited')
lit('44 (1897) 293,', 'Thomson, Philosophical Magazine volume 44, 1897, first page 293, cited')
lit('20 per cent', 'Thomson (1897) states that the uncertainty of the radius of curvature alone is about 20 per cent, quoted from the paper')
lit('93, 025010', 'Tiesinga et al., Reviews of Modern Physics, volume 93, article 025010 (2021): the CODATA 2018 constants, cited')
lit('1.602\\,176\\,634\\times10^{-19}', 'the elementary charge in coulomb, CODATA 2018 (exact)')
lit('9.109\\,383\\,70\\times10^{-31}', 'the electron mass in kg, CODATA 2018 (rounded as printed in the source)')
lit('0.19\\ \\mathrm{m}', 'the length from the plates to the screen, x_s - x_p - l, a given of the tube')
lit('\\chi=1.2', 'the angle of the electron to the field in the integrator test, a given of the test')
lit('=0.99', 'the criterion of problem 2, a given of the problem')
lit('10^{-4}', 'the unit conversion 1 g/abC = 1e-4 kg/C (CGS electromagnetic units to SI), and the hydrogen-ion value quoted from Thomson')
lit('10^{-7}', 'the order of m/e in Thomson (1897), in grams per abcoulomb, quoted from the paper')
lit('6\\times10^{12}', 'the printed value of W/Q in one row of Thomson (1897), quoted from the paper (it looks like a misprint, see the text)')
lit('6\\times10^{11}', 'the value of W/Q that the same row implies, derived in the text from its m/e and v')
lit('5 mm', 'the length of the red scale bar of the figure')
lit('−11', 'the exponent of the vacuum pressure quoted from the press release of Applied Materials, in millibar')
lit('30 kV', 'the second voltage of the examples, a given of the problem')


CH = {
    'title': 'A free electron in fields',
    'sections': SECTIONS,
    'figures': FIGS,
    'numbers': NUMBERS,
    'literals': LITERALS,
}
