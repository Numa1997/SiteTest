"""Every number quoted in the Fig. 12 lecture note, computed from the page's own data (public/scripts/slosh-modes.js, format 3),
the geometry module (geom.py), the plant (plant.py) and the controller reference (controller3.py), with the page's own formulas.
Run from the repository root:
    python3 tools/fig12/note_numbers.py [slosh-modes.js]   -> notes/fig12/numbers.json
"""
import json, math, os, sys, numpy as np
sys.path.insert(0, 'tools/fig12')
import geom as G, plant, controller3 as C
from scipy.special import jnp_zeros
MPATH = sys.argv[1] if len(sys.argv) > 1 else 'public/scripts/slosh-modes.js'
D_ = C.load_modes(MPATH)
g = 9.81
P = dict(V=500, hf=0.018, hd=0.008, T=6, mu6=2.06e-3, rho=1007, sig=0.045, ef=0.15, cs=1, gc=0.05, kf=1, wall=True)
U_F = 0.016
def muW(T): return 2.414e-5 * 10 ** (247.8 / (T + 273.15 - 140))
def key(m): return (m['m'], m['o'], m['n'])
def fill(V):
    vs = D_['vols_mL']; i = max(0, min(len(vs) - 2, int(np.searchsorted(vs, V)) - 1)); w = (V - vs[i]) / (vs[i + 1] - vs[i])
    A, B = D_['fills'][i], D_['fills'][i + 1]; Bm = {key(b): b for b in B['modes']}
    L = lambda a, b: a + w * (b - a)
    modes = []
    for a in A['modes']:
        b = Bm.get(key(a), a)
        md = {k: a[k] for k in ('m', 'o', 'n')}
        for k in ('lam', 'N', 'Qx', 'Qy', 'Qrx', 'Qry', 'Iw', 'Ib', 'Is', 'pur'): md[k] = L(a[k], b[k])
        md['rim_front'] = sum(L(a['psi'][kk][0][-1], b['psi'][kk][0][-1]) for kk in a['psi'])
        modes.append(md)
    return dict(V_mL=V, zs=L(A['zs'], B['zs']), a=L(A['a'], B['a']), V_liq=L(A['V_liq'], B['V_liq']), J_ry=L(A['J_ry'], B['J_ry']), J_rx=L(A['J_rx'], B['J_rx']), modes=modes)
def model(p, shape='glass'):
    F = fill(p['V']); zf = D_['glass']['floor_mm'] / 1000; Dp = F['zs'] - zf
    if shape == 'cyl':
        a = F['a']; XI = {0: jnp_zeros(0, 2), 1: jnp_zeros(1, 3), 2: jnp_zeros(2, 2), 3: jnp_zeros(3, 2)}; ms = []
        for md in F['modes']:
            m = md['m']; xi = XI[m][md['n'] - 1]; k = xi / a; th = math.tanh(k * Dp); N1 = a * a / 2 * (1 - m * m / xi ** 2); N = (2 if m == 0 else 1) * math.pi * N1
            S2 = math.sinh(2 * k * Dp); C2 = math.cosh(k * Dp) ** 2; lam = k * th; E = lam * N
            Iw = (2 if m == 0 else 1) * math.pi * a * (k * k * (S2 / (4 * k) - Dp / 2) + m * m / a ** 2 * (S2 / (4 * k) + Dp / 2)) / C2
            ms.append(dict(md, lam=lam, N=N, Qx=2 * a / (xi ** 2 - 1) if (m == 1 and md['o'] == 'c') else 0, Qy=2 * a / (xi ** 2 - 1) if (m == 1 and md['o'] == 's') else 0, Qry=0, Qrx=0,
                           Iw=Iw / E, Ib=(2 if m == 0 else 1) * math.pi * k * k * N1 / C2 / E, Is=(2 if m == 0 else 1) * math.pi * k * k * N1 / E, pur=1))
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
def pick(MM, o='c', m=1, n=1): return [x for x in MM['modes'] if x['m'] == m and x['o'] == o and x['n'] == n][0]
N = {}
# ---- the glass (geom.py) ----
zz = np.arange(0, G.H + 1e-9, 0.5); Ro = G.R0(zz); w_ = (zz > 15) & (zz < 60)
N['glass'] = dict(H=G.H, D_max=2 * Ro.max(), z_widest=float(zz[np.argmax(Ro)]), D_waist=float(2 * Ro[w_].min()), z_waist=float(zz[w_][np.argmin(Ro[w_])]), D_rim=float(2 * G.R0(G.H)), D_foot=float(2 * G.R0(0)),
                  wall=G.T_W, floor=G.Z_F, A_panel=G.A_PANEL, V_brim=G.cavity_volume(G.H) / 1e3, scale_z=G.H / G._H_UNITS, scale_r=(G.D_MAX / 2) / G._r_units.max())
hs = np.arange(G.Z_F + 1, G.H + 1e-9, 0.25); Vs = np.array([G.cavity_volume(h, nz=401, nt=64) for h in hs])
N['glass']['z_568'] = float(np.interp(568e3, Vs, hs)); N['glass']['z_500'] = float(np.interp(500e3, Vs, hs))
N['glass']['V_brim_round'] = float(np.trapezoid(np.pi * G.R_inner(np.linspace(G.Z_F, G.H, 2001), np.pi / 2) ** 2, np.linspace(G.Z_F, G.H, 2001)) / 1e3)   # the body of revolution alone, no panels
N['glass']['R_in_50_front'] = float(G.R_inner(50, 0)); N['glass']['R_in_50_side'] = float(G.R_inner(50, np.pi / 2))
# ---- the default pint ----
M0 = model(P); m11 = pick(M0); m11y = pick(M0, 's')
N['zs_mm'] = M0['zs'] * 1e3; N['a_mm'] = M0['a'] * 1e3; N['D_mm'] = M0['D'] * 1e3; N['nu'] = M0['nu']; N['Mf'] = M0['Mf']; N['m_liq'] = P['rho'] * M0['V_liq']
N['lam11'] = m11['lam']; N['lam11y'] = m11y['lam']; N['f11'] = m11['f']; N['f11y'] = m11y['f']; N['split_pct'] = 100 * (m11y['f'] - m11['f']) / m11['f']
N['muf11'] = m11['muf']; N['Q11_mm'] = m11['Qx'] * 1e3; N['Qry11_mm2'] = m11['Qry'] * 1e6; N['N11'] = m11['N']; N['pur11'] = m11['pur']; N['kD'] = m11['lam'] * M0['D']
N['f11_bare'] = math.sqrt(g * m11['lam']) / 2 / math.pi
N['f11_cap'] = math.sqrt(g * m11['lam'] + P['sig'] * m11['lam'] ** 3 / P['rho']) / 2 / math.pi
N['cap_ratio'] = P['sig'] * m11['lam'] ** 2 / (P['rho'] * g)
for k in ('gw', 'gs', 'gb', 'gc', 'gf', 'gam', 'zeta'): N[k + '11'] = m11[k]
N['tau11'] = 1 / m11['gam']; N['t5pct'] = math.log(20) / m11['gam']
N['modes'] = [{k: m[k] for k in ('m', 'o', 'n', 'lam', 'f', 'gam', 'zeta', 'gw', 'gs', 'gb', 'gf', 'pur')} for m in M0['modes']]
P0 = dict(P, hf=0.0); M1 = model(P0); n11 = pick(M1)
N['nohead'] = dict(f=n11['f'], gam=n11['gam'], tau=1 / n11['gam'], zeta=n11['zeta'], t5pct=math.log(20) / n11['gam'])
P2 = dict(P0, cs=0, gc=0); M2 = model(P2); c11 = pick(M2)
N['clean'] = dict(gam=c11['gam'], tau=1 / c11['gam'], zeta=c11['zeta'], gw=c11['gw'], gb=c11['gb'])
Cy = model(P, 'cyl'); c = pick(Cy); N['cyl_f11'] = c['f']; N['cyl_lam11'] = c['lam']; N['cyl_Q11_mm'] = c['Qx'] * 1e3
a = M0['a']; nu = M0['nu']
N['delta_theory_coef'] = math.pi * math.sqrt(0.5) * (1 + 1 / 1.841183781 ** 2) / (1 - 1 / 1.841183781 ** 2) * (1.841183781) ** -0.25
N['delta_nasa'] = 4.98 * math.sqrt(nu) * a ** -0.75 * g ** -0.25; N['gam_nasa'] = N['delta_nasa'] * N['f11_bare']
om = m11['om']; N['delta_stokes_mm'] = math.sqrt(2 * nu / om) * 1e3; N['decay_len_mm'] = 1e3 / m11['lam']; N['om11'] = om
N['faraday_amin_mm'] = 1e3 * 4 * m11['zeta'] * g / (2 * om) ** 2
N['V_brim'] = D_['glass']['V_brim_mL']
fs = []
for V in D_['vols_mL']:
    t = model(dict(P, V=V)); cy = model(dict(P, V=V), 'cyl'); h0 = model(dict(P, V=V, hf=0.0))
    fs.append((V, pick(t)['f'], pick(cy)['f'], pick(h0)['f'], pick(t, 's')['f'], t['a'] * 1e3, t['zs'] * 1e3))
N['f_vs_V'] = fs
N['tilt_sum_at_wall_over_R'] = sum(md['Qx'] * md['rim_front'] for md in M0['modes'] if md['m'] == 1 and md['o'] == 'c') / M0['a']
xi = 1.841183781; N['m11_cyl_frac'] = 2 * math.tanh(xi * N['D_mm'] / N['a_mm']) / (xi * (xi ** 2 - 1))
# ---- the cart (plant.py) and the control (controller3.py) ----
F500 = fill(500)
def gamma_fn(md):
    lam = md['lam']; kappa = M0['Mf'] * lam / P['rho']; w = math.sqrt((g * lam + P['sig'] * lam ** 3 / P['rho']) / (1 + kappa)); sq = 0.5 * math.sqrt(nu * w / 2)
    return sq * (md['Iw'] + md['Ib']) + sq * md['Is'] + 2 * nu * lam ** 2 + P['gc'] + (U_F / F500['a']) * (1 - math.exp(-lam * P['hf']))
modes = plant.modal_params(F500, P['rho'], P['sig'], M0['Mf'], gamma_fn)
for md, raw in zip(modes['x'], [m for m in F500['modes'] if m['m'] == 1 and m['o'] == 'c']): md['rim_front'] = raw['rim_front']
Pc = dict(plant.DEFAULT); Pc['I_max'] = 8.0
S = plant.assemble(Pc, F500, modes, P['rho'])
Ms = Pc['M_b'] + Pc['M_g'] + S['m_l']
N['cart'] = dict(M_b=Pc['M_b'], J_b=Pc['J_b'], k=Pc['k'], c=Pc['c'], m_w=Pc['m_w'], k_t=Pc['k_t'], c_t=Pc['c_t'], l_f=Pc['l_f'], l_r=Pc['l_r'], d_g=Pc['d_g'], h_g=Pc['h_g'], M_g=Pc['M_g'], c_x=Pc['c_x'], Bl=Pc['Bl'], I_max=Pc['I_max'], F_max=Pc['Bl'] * Pc['I_max'],
               M_sprung=Ms, m_l=S['m_l'], J_sj=S['J_ry'], J_rigid_foot=S['m_l'] * (S['z_cm_l'] ** 2) * 0 + P['rho'] * F500['V_liq'] * 0, z_cm_l=S['z_cm_l'],
               f_heave=math.sqrt(2 * Pc['k'] / Ms) / (2 * math.pi), f_pitch=math.sqrt(Pc['k'] * (Pc['l_f'] ** 2 + Pc['l_r'] ** 2) / S['M'][S['idx']['psi'], S['idx']['psi']]) / (2 * math.pi),
               f_hop=math.sqrt((Pc['k_t'] + Pc['k']) / Pc['m_w']) / (2 * math.pi), J_pitch_total=S['M'][S['idx']['psi'], S['idx']['psi']],
               zeta_heave=(2 * Pc['c']) / (2 * math.sqrt(2 * Pc['k'] * Ms)))
A, Bu, Bw = plant.state_space(S); ev = np.linalg.eigvals(A)
N['cart']['free_modes'] = sorted([(round(abs(e.imag) / 2 / math.pi, 3), round(-e.real / abs(e), 3)) for e in ev if e.imag > 1e-6])
N['cart']['m_slosh_g'] = [1e3 * P['rho'] * md['Q'] ** 2 * md['N'] * md['lam'] / (1 + md['kappa']) for md in modes['x']]
D = C.design(Pc, F500, modes, P['rho'], Ts=0.01, s_eta=0.0005, s_psi=0.01, s_v=0.05, s_u=20.0)
N['ctl'] = dict(tau_cl=D['tau'], n=D['n'], K_f=D['K_sub'][0].tolist(), K_r=D['K_sub'][1].tolist(), Ts=0.01, s_eta=0.0005, s_psi=0.01, s_v=0.05, s_u=20.0, runs={})
for sc, hgt in (('bump', 0.03), ('cobbles', 0.006), ('kerb', 0.02)):
    N['ctl']['runs'][sc] = {}
    for law in ('passive', 'skyhook', 'lqr'):
        o = C.simulate(D, Pc, sc, v=1.5, T=6.0, law=law, h_road=hgt)
        N['ctl']['runs'][sc][law] = dict(peak_mm=float(np.abs(o['eta']).max() * 1e3), maxU=float(np.abs(o['u']).max()), maxPsi_deg=float(np.abs(o['x'][:, S['idx']['psi']]).max() * 180 / math.pi), maxAz=float(np.abs(o['azb']).max()),
                                         over_mm=float((F500['zs'] + np.abs(o['eta']).max() + P['hf'] - 0.160) * 1e3), t_peak=float(o['t'][np.argmax(np.abs(o['eta']))]))
N['ctl']['dome_mm'] = P['hd'] * 1e3; N['ctl']['head_top_rest_mm'] = (F500['zs'] + P['hf'] - 0.160) * 1e3
os.makedirs('notes/fig12/figs', exist_ok=True)
json.dump(N, open('notes/fig12/numbers.json', 'w'), indent=1)
for k, v in N.items():
    if not isinstance(v, (list, dict)): print(f'{k:16s} {v:.6g}')
print('glass', {k: round(v, 3) for k, v in N['glass'].items()})
print('no head', {k: round(v, 4) for k, v in N['nohead'].items()}); print('clean', {k: round(v, 4) for k, v in N['clean'].items()})
print('cart', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in N['cart'].items()})
print('ctl tau', round(N['ctl']['tau_cl'], 4), 'runs:'); [print(' ', sc, {law: {k: round(v, 2) for k, v in r.items()} for law, r in d.items()}) for sc, d in N['ctl']['runs'].items()]
for m in N['modes']: print(f"  ({m['m']},{m['o']},{m['n']}) lam {m['lam']:8.2f}  f {m['f']:6.3f} Hz  gamma {m['gam']:.3f}/s  zeta {100*m['zeta']:.2f} %  purity {m['pur']:.4f}")
