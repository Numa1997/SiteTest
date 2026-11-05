"""Every number quoted in the Fig. 12 lecture note, computed from the page's own data (public/scripts/slosh-modes.js)
with the page's own formulas, plus the note's SVG figures (notes/fig12/figs/). Run from the repository root:
    python3 tools/fig12/note_numbers.py            -> notes/fig12/numbers.json and the SVGs
"""
import json, math, numpy as np, os
from scipy.special import jv, jnp_zeros
D_ = json.loads(open('public/scripts/slosh-modes.js').read().split('window.SLOSH_MODES = ', 1)[1].rstrip().rstrip(';'))
g = 9.81
P = dict(V=500, hf=0.018, T=6, mu6=2.06e-3, rho=1007, sig=0.045, ef=0.15, cs=1, gc=0.05, kf=1, wall=True)
U_F = 0.016
def muW(T): return 2.414e-5 * 10 ** (247.8 / (T + 273.15 - 140))
def fill(V):
    vs = D_['vols_mL']; i = max(0, min(len(vs) - 2, np.searchsorted(vs, V) - 1)); w = (V - vs[i]) / (vs[i + 1] - vs[i])
    A, B = D_['fills'][i], D_['fills'][i + 1]
    L = lambda a, b: a + w * (b - a)
    modes = [{k: (L(a[k], b[k]) if k in ('lam', 'Q', 'Iw', 'Ib', 'Is') else a[k]) for k in ('m', 'n', 'lam', 'Q', 'Iw', 'Ib', 'Is')} for a, b in zip(A['modes'], B['modes'])]
    return dict(zs=L(A['zs'], B['zs']), a=L(A['a'], B['a']), modes=modes)
def model(p, shape='tulip'):
    F = fill(p['V']); zf = D_['glass']['floor_mm'] / 1000; Dp = F['zs'] - zf
    if shape == 'cyl':
        a = F['a']; XI = {0: jnp_zeros(0, 2), 1: jnp_zeros(1, 3), 2: jnp_zeros(2, 2), 3: jnp_zeros(3, 1)}; ms = []
        for md in F['modes']:
            m = md['m']; xi = XI[m][md['n'] - 1]; k = xi / a; th = math.tanh(k * Dp); N = a * a / 2 * (1 - m * m / xi ** 2)
            S2 = math.sinh(2 * k * Dp); C2 = math.cosh(k * Dp) ** 2; lam = k * th
            Iw = a * (k * k * (S2 / (4 * k) - Dp / 2) + m * m / a ** 2 * (S2 / (4 * k) + Dp / 2)) / C2
            ms.append(dict(m=m, n=md['n'], lam=lam, Q=2 * a / (xi ** 2 - 1) if m == 1 else 0, Iw=Iw / (lam * N), Ib=k * k / C2 / lam, Is=k * k / lam))
        F = dict(F, modes=ms)
    mu = p['mu6'] * muW(p['T']) / muW(6); nu = mu / p['rho']; Mf = p['ef'] * p['rho'] * p['hf']
    out = []
    for md in F['modes']:
        lam = md['lam']; muf = Mf * lam / p['rho']
        om = math.sqrt((g * lam + p['sig'] * lam ** 3 / p['rho']) / (1 + muf)); sq = 0.5 * math.sqrt(nu * om / 2)
        gw = sq * (md['Iw'] + md['Ib']) if p['wall'] else 0; gs = p['cs'] * sq * md['Is']; gb = 2 * nu * lam ** 2; gc = p['gc']
        gf = p['kf'] * (U_F / F['a']) * (1 - math.exp(-lam * p['hf'])); gam = gw + gs + gb + gc + gf
        out.append(dict(md, om=om, f=om / 2 / math.pi, muf=muf, gw=gw, gs=gs, gb=gb, gc=gc, gf=gf, gam=gam, zeta=gam / om))
    return dict(F, D=Dp, nu=nu, mu=mu, Mf=Mf, modes=out)
N = {}
M0 = model(P); m11 = [m for m in M0['modes'] if m['m'] == 1 and m['n'] == 1][0]
N['zs_mm'] = M0['zs'] * 1e3; N['a_mm'] = M0['a'] * 1e3; N['D_mm'] = M0['D'] * 1e3; N['nu'] = M0['nu']; N['Mf'] = M0['Mf']
N['lam11'] = m11['lam']; N['f11'] = m11['f']; N['muf11'] = m11['muf']; N['Q11_mm'] = m11['Q'] * 1e3; N['kD'] = m11['lam'] * M0['D']
N['f11_bare'] = math.sqrt(g * m11['lam']) / 2 / math.pi
N['f11_cap'] = math.sqrt(g * m11['lam'] + P['sig'] * m11['lam'] ** 3 / P['rho']) / 2 / math.pi
N['cap_ratio'] = P['sig'] * m11['lam'] ** 2 / (P['rho'] * g)
for k in ('gw', 'gs', 'gb', 'gc', 'gf', 'gam', 'zeta'): N[k + '11'] = m11[k]
N['tau11'] = 1 / m11['gam']; N['t5pct'] = math.log(20) / m11['gam']
N['modes'] = [{k: m[k] for k in ('m', 'n', 'lam', 'f', 'gam', 'zeta', 'gw', 'gs', 'gb', 'gf')} for m in M0['modes']]
P0 = dict(P, hf=0.0); M1 = model(P0); n11 = [m for m in M1['modes'] if m['m'] == 1 and m['n'] == 1][0]
N['nohead'] = dict(f=n11['f'], gam=n11['gam'], tau=1 / n11['gam'], zeta=n11['zeta'], t5pct=math.log(20) / n11['gam'])
P2 = dict(P0, cs=0, gc=0); M2 = model(P2); c11 = [m for m in M2['modes'] if m['m'] == 1 and m['n'] == 1][0]
N['clean'] = dict(gam=c11['gam'], tau=1 / c11['gam'], zeta=c11['zeta'], gw=c11['gw'], gb=c11['gb'])
# cylinder of the same surface radius and depth
C = model(P, 'cyl'); c = [m for m in C['modes'] if m['m'] == 1 and m['n'] == 1][0]; N['cyl_f11'] = c['f']; N['cyl_lam11'] = c['lam']; N['cyl_Q11_mm'] = c['Q'] * 1e3
# log decrement: clean theory vs NASA SP-106 empirical fit, at the page's surface radius
a = M0['a']; nu = M0['nu']
N['delta_theory_coef'] = math.pi * math.sqrt(0.5) * (1 + 1 / 1.841183781 ** 2) / (1 - 1 / 1.841183781 ** 2) * (1.841183781) ** -0.25
N['delta_nasa'] = 4.98 * math.sqrt(nu) * a ** -0.75 * g ** -0.25
N['gam_nasa'] = N['delta_nasa'] * N['f11_bare']
# boundary layer thickness, Reynolds-type numbers
om = m11['om']; N['delta_stokes_mm'] = math.sqrt(2 * nu / om) * 1e3; N['decay_len_mm'] = 1e3 / m11['lam']
# resonant steady amplitude at the wall, shaker A sideways at f11
A = 0.2e-3; acc = A * om ** 2; N['A_res_mm'] = 1e3 * m11['lam'] * m11['Q'] * acc / (1 + m11['muf']) / (2 * m11['gam'] * om); N['acc_res'] = acc
# Faraday threshold at 2 f11: parametric gain beats damping when (Az w^2 / g) w/4 > gamma, w = 2 om
N['faraday_amin_mm'] = 1e3 * 4 * m11['zeta'] * g / (2 * om) ** 2
N['faraday_A2mm_gain'] = 2e-3 * (2 * om) ** 2 / g * om / 4 - m11['gam']
# walking: step frequency ~ 2 Hz, Mayer & Krechetnikov; ratio
N['V_brim'] = D_['glass']['V_brim_mL']
fs = []
for V in D_['vols_mL']:
    t = model(dict(P, V=V)); cy = model(dict(P, V=V), 'cyl'); h0 = model(dict(P, V=V, hf=0.0))
    pick = lambda MM: [m for m in MM['modes'] if m['m'] == 1 and m['n'] == 1][0]['f']
    fs.append((V, pick(t), pick(cy), pick(h0), t['a'] * 1e3, t['zs'] * 1e3))
N['f_vs_V'] = fs

# walking: steps at 1.6 Hz, second harmonic 3.2 Hz; steady response per unit sideways acceleration, with and without head
def resp(mm, Om):
    om = mm['om']; return mm['lam'] * mm['Q'] / (1 + mm['muf']) / math.sqrt((om**2 - Om**2)**2 + (2 * mm['gam'] * Om)**2)
Om2 = 2 * math.pi * 3.2
N['walk_resp_head'] = resp(m11, Om2); N['walk_resp_nohead'] = resp(n11, Om2); N['walk_ratio'] = N['walk_resp_head'] / N['walk_resp_nohead']
# the hand: a critically damped follower of rate Omega_h passes a motion at the slosh frequency with gain Omega_h^2/(Omega_h^2 + omega^2)
Oh = 22.0; N['hand_gain_f1'] = Oh**2 / (Oh**2 + m11['om']**2)
# steady sideways acceleration: the modes must add up to the tilted plane, sum_n Q_n psi_n(r) = r (wall-normalised), checked at the wall
F500 = [f for f in D_['fills'] if f['V_mL'] == 500][0]
N['tilt_sum_at_wall_over_R'] = sum(md['Q'] for md in F500['modes'] if md['m'] == 1) / F500['a']
N['walls_bulk_only_tau'] = 1 / N['clean']['gam']

# section 10: the waiter (tools/fig12/controller.py)
import sys as _s; _s.path.insert(0, 'tools/fig12'); import controller as Cw
Aw, Bw, mdw, infow = Cw.model(); Kw, Adw, Bdw = Cw.lqr(Aw, Bw)
ew, tw, Fw = Cw.carry(Aw, Bw, Kw, Adw, Bdw, infow, 0.20); eh3, th3, _ = Cw.carry(Aw, Bw, Kw, Adw, Bdw, infow, 0.20, mode='hand', Om=3, T=5); eh22, _, _ = Cw.carry(Aw, Bw, Kw, Adw, Bdw, infow, 0.20, mode='hand', Om=22, T=5)
N['w_M'] = infow['M']; N['w_ml'] = infow['ml']; N['w_Me'] = infow['Me']; N['w_m1_g'] = mdw[0]['msl'] * 1000; N['w_m2_g'] = mdw[1]['msl'] * 1000; N['w_m3_g'] = mdw[2]['msl'] * 1000
N['w_peak_mm'] = ew * 1000; N['w_settle'] = tw; N['w_Fmax'] = Fw; N['w_Imax'] = Fw / Cw.CAR['Bl']; N['w_hand3_mm'] = eh3 * 1000; N['w_hand22_mm'] = eh22 * 1000
N['w_tau_cl'] = -Cw.CAR['Ts'] / np.log(np.abs(np.linalg.eigvals(Adw - Bdw @ Kw)).max()); N['w_tau_open'] = 1 / mdw[0]['gam']
N['w_freeboard_mm'] = 160 - N['zs_mm'] - 18
xi = 1.841183781; N['m11_cyl_frac'] = 2 * math.tanh(xi * N['D_mm'] / N['a_mm']) / (xi * (xi**2 - 1)); N['m11_cyl_g'] = N['m11_cyl_frac'] * P['rho'] * math.pi * (N['a_mm'] / 1000)**3 * 1000
os.makedirs('notes/fig12/figs', exist_ok=True)
json.dump(N, open('notes/fig12/numbers.json', 'w'), indent=1)
for k, v in N.items():
    if not isinstance(v, (list, dict)): print(f'{k:16s} {v:.6g}')
print('no head', {k: round(v, 4) for k, v in N['nohead'].items()}); print('clean', {k: round(v, 4) for k, v in N['clean'].items()})
for m in N['modes']: print(f"  ({m['m']},{m['n']}) lam {m['lam']:8.2f}  f {m['f']:6.3f} Hz  gamma {m['gam']:.3f}/s  zeta {100*m['zeta']:.2f} %")
