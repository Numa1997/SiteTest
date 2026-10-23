#!/usr/bin/env python3
"""Every number and table the lecture notes quote, computed here and written to numbers.json.

The theory sources write {{n:key}} for a number and {{table:key}} for a table; tools/build_theory.py substitutes them and
stops on any key that is not here.  So no number in the text is typed by hand.
Inputs: the formulas below, and the stored results of the nonlinear runs in data/ (copied from notes/rotor-pendula/derive/:
L1_mountings.json from L1_engine_check.py, L1_chaos.json, L1_map.json and L1_map_g70.json, mc_full.log from
power_theorem_mc.py).  Run: python3 tools/make_numbers.py
"""
import json, math, pathlib, re
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT / 'data'
g = 9.80665                  # standard gravity, as in Sol's study
m, L = 0.1, 0.2              # the single pendulum: bob and rod
N = {}                       # key -> formatted string
T = {}                       # key -> HTML table

def f(x, d):
    return f'{x:.{d}f}'

# ---- the 18 mountings -------------------------------------------------------------------------------------------
runs = json.load(open(D / 'L1_mountings.json'))
rows = []
for r in sorted(runs, key=lambda r: (-r['rpm'], r['pct'])):
    Om, rp = r['Om'], r['rp']
    R = rp/L; G = g/(Om**2*L); Gam = R/G
    Pstar = m*L*g**2/(4*Om*abs(rp - L))
    Th = G/(math.sqrt(2)*abs(R - 1))
    Rrot = 56.0/Om
    rows.append(dict(rpm=r['rpm'], pct=r['pct'], Rrot=Rrot, rp=rp, R=R, G=G, Gam=Gam, Pstar=Pstar, Th=Th,
                     Ps=r['P_single'], Pd=r['P_double'], ratio=r['P_double']/r['P_single'],
                     share=r['P_single']/(0.5*1.225*math.pi*Rrot**2*8.0**3*0.45)))
N['R_min'] = f(min(x['R'] for x in rows), 2); N['R_max'] = f(max(x['R'] for x in rows), 0)
N['G_min'] = f(min(x['G'] for x in rows), 3); N['G_max'] = f(max(x['G'] for x in rows), 1)
N['Gam_min'] = f(min(x['Gam'] for x in rows), 2); N['Gam_max'] = f(max(x['Gam'] for x in rows), 0)
N['P_sol_min'] = f(min(x['Ps'] for x in rows)*1e3, 2); N['P_sol_max'] = f(max(x['Ps'] for x in rows)*1e3, 1)
N['ratio_min'] = f(min(x['ratio'] for x in rows), 3); N['ratio_max'] = f(max(x['ratio'] for x in rows), 3)
N['Th_min'] = f(min(x['Th'] for x in rows), 3); N['Th_max'] = f(max(x['Th'] for x in rows), 2)
N['Th_max_deg'] = f(math.degrees(max(x['Th'] for x in rows)), 0)
N['lin_err_max'] = f(max(abs(x['Pstar']/x['Ps'] - 1) for x in rows)*100, 2)
N['share_max'] = f'{max(x["share"] for x in rows)*1e5:.1f}'
N['torque_star'] = f(m*g*L/math.sqrt(2), 4)
best = max(rows, key=lambda x: x['Ps'])
N['P_best'] = f(best['Ps']*1e3, 1); N['Pstar_best'] = f(best['Pstar']*1e3, 2)
N['ratio_f_min'] = f(min(x['R'] for x in rows)**0.5, 2)
N['ratio_f_max'] = f(max(x['R'] for x in rows)**0.5, 1)
N['sensor_uW'] = '37.6'
N['margin_min'] = f'{min(x["Ps"] for x in rows)/(2*37.6e-6):.0f}'      # mechanical power over twice the sensor need
tr = ['<p class="tcap">Table 1. Sol\'s 18 mountings. ¹ At these two mountings Sol\'s brake is the best one found by a nonlinear search, not $\\kappa^*$.</p><table class="mt"><thead><tr><th>rotor</th><th>pivot</th><th>$R$</th><th>$G$</th><th>$\\Gamma$</th>'
      '<th>$\\Theta^*$ (rad)</th><th>$P^*$ (2.5), mW</th><th>full model, mW</th><th>double, mW</th><th>double ÷ single</th></tr></thead><tbody>']
for x in rows:
    tr.append(f'<tr><td>{x["rpm"]} rpm, {x["Rrot"]:.2f} m</td><td>{x["pct"]} %, {x["rp"]:.3f} m</td><td>{x["R"]:.2f}</td>'
              f'<td>{x["G"]:.3g}</td><td>{x["Gam"]:.3g}</td><td>{x["Th"]:.3f}</td><td>{x["Pstar"]*1e3:.2f}</td>'
              f'<td>{x["Ps"]*1e3:.2f}{"¹" if x["rpm"] in (8, 14) and x["pct"] == 30 else ""}</td><td>{x["Pd"]*1e3:.2f}</td><td>{x["ratio"]:.3f}</td></tr>')
tr.append('</tbody></table>')
T['mountings'] = '\n'.join(tr)

# ---- large-rotor limit r_p >> L: P* -> m L g^2/(4 f lambda_T v), independent of the rotor speed ----------------------
for fr in (30, 60, 90):
    N[f'flat_{fr}'] = f(m*L*g**2/(4*fr/100*56.0)*1e3, 2)
    big = [x for x in rows if x['pct'] == fr and x['rpm'] <= 20]
    N[f'flat_runs_{fr}'] = f'{min(x["Ps"] for x in big)*1e3:.2f}–{max(x["Ps"] for x in big)*1e3:.2f}'

# ---- the locked double: a rigid body with its centre of mass at 3/4 of the reach -------------------------------------
Mlc, Ip = 0.05*0.1 + 0.05*0.2, 0.05*0.1**2 + 0.05*0.2**2
lock = [((Mlc*g)**2/(4*x['rpm']*2*math.pi/60*(Mlc*x['rp'] - Ip)))/x['Pstar'] for x in rows]
N['lock_min'] = f(min(lock), 3); N['lock_max'] = f(max(lock), 3)
N['lc_frac'] = f(Mlc/(0.1*L), 2)
N['flex_cost_max'] = f(max(1 - x['ratio']/l for x, l in zip(rows, lock))*100, 1)
N['flex_cost_min'] = f(min(1 - x['ratio']/l for x, l in zip(rows, lock))*100, 1)

# ---- mean lean at the most nonlinear mounting ------------------------------------------------------------------------
w = max(rows, key=lambda x: x['Th'])
N['lean_theory'] = f(-w['G']**2/(4*w['R']*(w['R'] - 1)), 3)
N['lean_run'] = '−0.128'     # integrated, notes/rotor-pendula/derive/L0_r2.py (PASS within 10 %)
N['lean_deg'] = f(math.degrees(abs(w['G']**2/(4*w['R']*(w['R'] - 1)))), 1)
leans = sorted(math.degrees(x['G']**2/(4*x['R']*(x['R'] - 1))) for x in rows)
N['lean_next_deg'] = f(leans[-2], 1)
N['lean_small_deg'] = f(max(math.degrees(x['G']**2/(4*x['R']*(x['R'] - 1))) for x in rows if x['rpm'] >= 100), 2)

# ---- tilted hinge --------------------------------------------------------------------------------------------------
for key, R in (('fast', min(x['R'] for x in rows)), ('slow', max(x['R'] for x in rows))):
    cs = (-R + math.sqrt(R*R + 8))/2; a = math.acos(cs)
    N[f'tilt_{key}'] = f(math.degrees(a), 1)
    N[f'tilt_sens_{key}'] = f(abs(-R*math.sin(a) - math.sin(2*a)), 0 if R > 10 else 1)

# ---- Sol's chaos group ---------------------------------------------------------------------------------------------
ch = json.load(open(D / 'L1_chaos.json'))
tr = ['<table class="mt"><thead><tr><th>$c$ (N m s)</th><th>$\\kappa$</th><th>chaotic starts</th><th>mean power, mW</th>'
      '<th>largest Lyapunov exponent $\\Lambda$, s⁻¹</th></tr></thead><tbody>']
for gr in ch['groups']:
    P = np.array(gr['P'])*1e3; lam = np.array(gr['lyap'])
    nch = int(np.sum(lam > 0.01*ch['Om']))
    ps = f'{P.mean():.1f}' if P.std() < 0.05 else f'{P.min():.0f}–{P.max():.0f}'
    ls = f'{lam.mean():.3f}' if lam.std() < 1e-3 else f'{lam.min():.2f} to {lam.max():.2f}'
    tr.append(f'<tr><td>{gr["c"]:.3f}</td><td>{gr["c"]/(0.1*0.04*ch["Om"]):.3f}</td><td>{nch} of {len(P)}</td><td>{ps}</td><td>{ls}</td></tr>')
    N[f'chaos_P_{int(round(gr["c"]*1000))}'] = ps
tr.append('</tbody></table>')
T['chaos'] = '\n'.join(tr)
N['chaos_thr'] = f(0.01*ch['Om'], 2); N['chaos_Om'] = f(ch['Om'], 0)
N['chaos_nic'] = str(len(ch['groups'][0]['P'])); N['chaos_turns'] = str(ch['MEAS'])

# ---- chaos map -----------------------------------------------------------------------------------------------------
mp = json.load(open(D / 'L1_map.json')); fix = {g_['R']: g_ for g_ in json.load(open(D / 'L1_map_g70.json'))}
cells = {}
for gr in mp['groups']:
    for mb in gr['members']:
        if mb['G'] == 70 and gr['R'] in fix:
            continue
        cells.setdefault((gr['R'], mb['G']), []).append(mb)
    if gr['R'] in fix:
        for mb in fix[gr['R']]['members']:
            cells.setdefault((gr['R'], mb['G']), []).append(mb)
assert all(math.isfinite(mb['lyap']) for v in cells.values() for mb in v)
Gs = sorted({k[1] for k in cells}); Rs = sorted({k[0] for k in cells})
tr = ['<table class="mt"><thead><tr><th>$R$ \\ $G$</th>' + ''.join(f'<th>{G:g}</th>' for G in Gs) + '</tr></thead><tbody>']
for R in Rs:
    tds = []
    for G in Gs:
        v = cells[(R, G)]; n_ch = sum(mb['lyap'] > 0.01 for mb in v)
        tds.append(f'<td>{n_ch}/{len(v)}</td>')
    tr.append(f'<tr><th>{R:g}</th>' + ''.join(tds) + '</tr>')
tr.append('</tbody></table>')
T['chaosmap'] = '\n'.join(tr)
N['map_kstar_R1'] = f(next(g_['kappa_star'] for g_ in mp['groups'] if g_['R'] == 1), 3)
N['chaos_kappa_30'] = f(0.030/(0.1*0.04*4.0), 3)
N['map_members'] = str(sum(len(v) for v in cells.values()))
N['map_chaotic'] = str(sum(mb['lyap'] > 0.01 for v in cells.values() for mb in v))

# ---- power theorem Monte Carlo ----------------------------------------------------------------------------------------
log = (D / 'mc_full.log').read_text()
ratios = [abs(float(x) - 1)*100 for x in re.findall(r'ratio ([0-9.]+) \+-', log)]
N['mc_dev_max'] = f(max(ratios[1::2]), 2); N['mc_dev_min'] = f(min(ratios[1::2]), 2)
meff = re.findall(r'<m_eff>/M = ([0-9.]+)', log)
N['meff_single_large'] = f(float(meff[3]), 2); N['meff_double_chaos'] = f(float(meff[7]), 2)

# ---- turbulent wind, preliminary (L2): the rotor's wandering, at the same mean rotor speed ---------------------------
l2 = json.load(open(D / 'L2_run.json'))
wand = []
for mt in l2['mountings']:
    pn, pu = np.array(mt['P_noeuler']), np.array(mt['P_unif'])
    wand.append(np.mean((pn - pu)/mt['P0'])*100)
N['wander_min'] = f(min(wand), 2); N['wander_max'] = f(max(wand), 2); N['l2_records'] = str(l2['NREC'])

# ---- figure: the universal brake curve P/P* = 2x/(1+x^2), x = kappa/kappa*, on a log axis ----------------------
W_, H_, l_, r_, t_, b_ = 560, 300, 58, 20, 18, 46
xs = np.logspace(-2, 2, 241)
def X(x): return l_ + (math.log10(x) + 2)/4*(W_ - l_ - r_)
def Y(y): return t_ + (1 - y)*(H_ - t_ - b_)
pts = ' '.join(f'{X(x):.1f},{Y(2*x/(1 + x*x)):.1f}' for x in xs)
ticks = ''.join(f'<line x1="{X(v):.1f}" y1="{H_-b_}" x2="{X(v):.1f}" y2="{H_-b_+5}" stroke="#3f2c23"/><text x="{X(v):.1f}" y="{H_-b_+19}" text-anchor="middle" class="svgc">{lab}</text>'
                for v, lab in ((0.01, '0.01'), (0.1, '0.1'), (1, '1'), (10, '10'), (100, '100')))
ticks += ''.join(f'<line x1="{l_-5}" y1="{Y(v):.1f}" x2="{l_}" y2="{Y(v):.1f}" stroke="#3f2c23"/><text x="{l_-9}" y="{Y(v)+4:.1f}" text-anchor="end" class="svgc">{v:g}</text>'
                 for v in (0, 0.5, 1))
T['fig_brake'] = (f'<figure class="fig"><svg viewBox="0 0 {W_} {H_}" role="img" aria-label="Harvested power over its maximum against the brake over the best brake, on a logarithmic axis from 0.01 to 100: a single hump, zero at both ends, peaking at 1 where the brake equals the best brake; half the maximum is reached at about 0.27 and 3.7.">'
    f'<rect x="{l_}" y="{t_}" width="{W_-l_-r_}" height="{H_-t_-b_}" fill="#fff" stroke="#3f2c23"/>'
    f'<line x1="{X(1):.1f}" y1="{t_}" x2="{X(1):.1f}" y2="{H_-b_}" stroke="#dccdb4" stroke-dasharray="4 4"/>'
    f'<line x1="{l_}" y1="{Y(0.5):.1f}" x2="{W_-r_}" y2="{Y(0.5):.1f}" stroke="#dccdb4" stroke-dasharray="4 4"/>'
    f'<polyline points="{pts}" fill="none" stroke="#7d1d2f" stroke-width="2.4"/>{ticks}'
    f'<text x="{(l_+W_-r_)/2}" y="{H_-8}" text-anchor="middle" class="svgd">brake over best brake, κ/κ*</text>'
    f'<text x="16" y="{(t_+H_-b_)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 16 {(t_+H_-b_)/2})">P / P*</text></svg>'
    f'<figcaption>Figure 2. The harvested power (2.3) over its maximum (2.5), against the brake over the best brake (2.4): '
    f'$\\bar P/P^* = 2x/(1+x^2)$ with $x = \\kappa/\\kappa^*$, the same curve at every mounting. The top is flat: a brake '
    f'{2-math.sqrt(3):.2f} times the best, or {2+math.sqrt(3):.1f} times it, still gives half the power ($x = 2 \\mp \\sqrt3$).</figcaption></figure>')

# ---- turbine power for the share (Sol's assumptions) and the trail identity ---------------------------------------
N['tilt_max_deg'] = f(math.degrees(math.asin(1/min(x['Gam'] for x in rows))), 0)
N['tilt_min_deg'] = f(math.degrees(1/max(x['Gam'] for x in rows)), 2)
N['invG_max'] = f(1/min(x['Gam'] for x in rows), 2)
N['cp_sol'] = '0.45'; N['rho'] = '1.225'
bestshare = max(rows, key=lambda x: x['share'])
N['share_where'] = f'{bestshare["rpm"]} rpm, pivot at {bestshare["pct"]} %'

# ---- L2 both torque laws ------------------------------------------------------------------------------------------
for law in ('nrel', 'k2'):
    d2 = json.load(open(D / f'L2_run_{law}.json'))
    tot = []; wnd = []; msh = []
    for mt in d2['mountings']:
        pt, pn, pu = np.array(mt['P_turb']), np.array(mt['P_noeuler']), np.array(mt['P_unif'])
        tot.append(np.mean((pt - mt['P0'])/mt['P0'])*100); wnd.append(np.mean((pn - pu)/mt['P0'])*100)
        msh.append(np.mean((pu - mt['P0'])/mt['P0'])*100)
    N[f'l2_{law}_tot_min'] = f(min(tot), 2); N[f'l2_{law}_tot_max'] = f(max(tot), 2)
    N[f'l2_{law}_wnd_min'] = f(min(wnd), 2); N[f'l2_{law}_wnd_max'] = f(max(wnd), 2)
    N[f'l2_{law}_msh_min'] = f(min(msh), 2); N[f'l2_{law}_msh_max'] = f(max(msh), 2)
N['jensen'] = f(0.103**2/2*100, 2); N['sigOm'] = '10.3'

# ---- L3 sag ---------------------------------------------------------------------------------------------------------
sag = json.load(open(D / 'L3_sag.json'))
N['sag_tip_cm'] = f(sag[0]['x_tip']*100, 0)
for sg in sag:
    k = int(round(sg['frac']*100))
    N[f'sag_w_{k}'] = f(sg['w']*1000, 0); N[f'sag_only_{k}'] = f(sg['sag_only'], 1); N[f'sag_tot_{k}'] = f'{sg["total"]:+.1f}'

# ---- L3 shaking (two-way) -------------------------------------------------------------------------------------------
sh = json.load(open(D / 'L3_shake2.json'))
def pick(z, sgm, dev):
    return next(r for r in sh if r['zeta'] == z and r['sig_tip'] == sgm and r['device'].startswith(dev))
for sgm, key in ((0.005, '5'), (0.02, '20'), (0.1, '100')):
    a = pick(0.005, sgm, 'Sol'); b = pick(0.005, sgm, 'double')
    N[f'sh_sol_{key}'] = f'{a["P"]*1e3:.3g}'; N[f'sh_dbl_{key}'] = f'{b["P"]*1e3:.3g}'
    N[f'sh_in_{key}'] = f'{a["P_in"]:.3g}'
N['sh_ratio'] = f(pick(0.005, 0.1, 'double')['P']/pick(0.005, 0.1, 'Sol')['P'], 2)
for z, key in ((0.005, 'lo'), (0.03, 'hi')):
    tnd = pick(z, 0.005, 'tuned')
    N[f'tu_P_{key}'] = f(tnd['P']*1e3, 1); N[f'tu_Pw_{key}'] = f(tnd['P_wander']*1e3, 1)
    N[f'tu_share_{key}'] = f(tnd['P']/tnd['P_in']*100, 0); N[f'tu_q_{key}'] = f(tnd['q_rms'], 2)
    N[f'tu_tipcut_{key}'] = f((1 - tnd['x_rms']/0.005)*100, 0)
    N[f'tu_q20_{key}'] = f(pick(z, 0.02, 'tuned')['q_rms'], 2)
N['tu_L'] = f(0.9*63.0*0.9494**2/(2*math.pi*1.0793)**2, 2)
N['zeta_struct'] = '0.48'
gt = 9.80665*math.cos(math.radians(5.0)); Om5 = 0.9494; rp9 = 0.9*63.0
N['grav_sol90'] = f(m*0.2*gt**2/(4*Om5*(rp9 - 0.2))*1e3, 1)
Lt = rp9*Om5**2/(2*math.pi*1.0793)**2
N['grav_tuned90'] = f(m*Lt*gt**2/(4*Om5*(rp9 - Lt))*1e3, 0)
N['tu_len_ratio'] = f(Lt/0.2, 1)

# ---- L4: the geared generator (maxon RE 25 + GP 32 C), chapter 7 ---------------------------------------------------------
# formula (7.6)-(7.7): L4_generator.json; full equation (7.4) at the same settings: L4_check_2000.json (4000 steps agree to 0.5 %);
# full-equation scan of nearby settings: L4_scan.json
g4 = json.load(open(D / 'L4_generator.json'))
full = {(c['rpm'], c['frac']): c for c in json.load(open(D / 'L4_check_2000.json'))}
scan = {(c['rpm'], c['frac']): c for c in json.load(open(D / 'L4_scan.json'))}
KT, KE, RC, JM, I0 = 0.0208, 0.02076, 1.53, 1.47e-6, 0.0402
T0 = KT*I0; mgL = m*g*L
for r in g4:
    c = full[(r['rpm'], r['frac'])]; r['PlF'] = c['P_load_full']; r['PpF'] = c['P_paid_full']; r['ThF'] = c['Theta_full']
    r['gap'] = c['P_load_full']/r['P_load'] - 1
    sc = scan[(r['rpm'], r['frac'])]; r['scan'] = sc['P_load_best']/sc['P_load_formula_setting'] - 1      # same step size on both sides
N['csc1'] = f'{KT*KE/RC:.5f}'
cst = [m*L**2*x['rpm']*2*math.pi/60*abs(x['R'] - 1) for x in rows]
N['cstar_min'] = f(min(cst), 2); N['cstar_max'] = f(max(cst), 2)
N['Nneed_min'] = str(math.ceil(math.sqrt(min(cst)/(KT*KE/RC)))); N['Nneed_max'] = str(math.ceil(math.sqrt(max(cst)/(KT*KE/RC))))
N['j_33'] = f((JM + 0.8e-7)*33**2/(m*L**2), 2); N['j_51'] = f((JM + 0.7e-7)*51**2/(m*L**2), 2); N['j_111'] = f((JM + 0.7e-7)*111**2/(m*L**2), 2)
N['T0_mNm'] = f(T0*1e3, 2); N['mgL'] = f(mgL, 3)
N['fric_51'] = f(51*T0/0.70, 3); N['fricG_51'] = f(51*T0/0.70/mgL*100, 0); N['fricG_111'] = f(111*T0/0.70/mgL*100, 0)
N['Njam'] = str(int(0.70*mgL/T0)); N['Njam_df'] = str(int(math.pi/4*0.70*mgL/T0))
N['ceiling_frac'] = f(math.pi/(4*math.sqrt(2)), 2)
N['g4_min'] = f(min(r['PlF'] for r in g4)*1e3, 1); N['g4_max'] = f(max(r['PlF'] for r in g4)*1e3, 0)
N['g4_margin'] = str(int(min(r['PlF'] for r in g4)/37.6e-6))
big = [r for r in g4 if r['rpm'] <= 20]
N['g4_big_min'] = f(min(r['PlF'] for r in big)*1e3, 1); N['g4_big_max'] = f(max(r['PlF'] for r in big)*1e3, 1)
N['g4_big_share_min'] = f(min(r['PlF']/r['Pstar'] for r in big)*100, 0); N['g4_big_share_max'] = f(max(r['PlF']/r['Pstar'] for r in big)*100, 0)
N['g4_big_eff_min'] = f(min(r['PlF']/r['PpF'] for r in big)*100, 0); N['g4_big_eff_max'] = f(max(r['PlF']/r['PpF'] for r in big)*100, 0)
def split(r):                                    # shares of what the rotor pays, from (7.7): friction, gears, coil, load
    ke, eta, Th, fr, x = r['kappa_e'], r['eta'], r['Theta'], r['f'], r['at_short']
    parts = [fr*2/math.pi*Th, ke*(1/eta - 1)*Th**2/2, ke*x*Th**2/2, ke*(1 - x)*Th**2/2]
    return [p/sum(parts) for p in parts]
sp = [split(r) for r in big]
for k, nm in enumerate(('fric', 'gear', 'coil', 'load')):
    N[f'split_{nm}_min'] = f(min(q[k] for q in sp)*100, 0); N[f'split_{nm}_max'] = f(max(q[k] for q in sp)*100, 0)
N['ratio_count_51'] = str(sum(r['N'] == 51 for r in g4))
gp = [r['gap'] for r in g4]
N['df_gap_max'] = f(max(gp)*100, 0); N['df_gap_big'] = f(max(abs(r['gap']) for r in big)*100, 0)
N['df_gap_min'] = f(min(gp)*100, 1)
N['scan_gain_rest'] = f(max(r['scan'] for r in g4 if (r['rpm'], r['frac']) != (400, 0.3))*100, 1)
hm = [x for x in json.load(open(D / 'L4_harmonics.json')) if x['rpm'] in (100, 200)]
N['h3_pct'] = f'{min(x["h3"] for x in hm)*100:.1f} to {max(x["h3"] for x in hm)*100:.1f}'
N['outph_min'] = f(min(x['outphase'] for x in hm)*100, 0); N['outph_max'] = f(max(x['outphase'] for x in hm)*100, 0)
N['th1_gain'] = f(max(x['Th1']/x['Th_formula'] - 1 for x in hm)*100, 0)
N['thF_drop_big'] = f(max(1 - r['ThF']/r['Theta'] for r in big)*100, 0)
for key, (rpm, fr) in (('t30', (400, 0.3)), ('t90', (400, 0.9))):
    r = next(x for x in g4 if x['rpm'] == rpm and abs(x['frac'] - fr) < 1e-9)
    N[f'{key}_N'] = str(r['N']); N[f'{key}_s0'] = f(r['R'] - 1, 2); N[f'{key}_s1'] = f(r['R'] - 1 - r['j'], 2)
    N[f'{key}_paid'] = f(r['PpF']*1e3, 0); N[f'{key}_Pstar'] = f(r['Pstar']*1e3, 1); N[f'{key}_load'] = f(r['PlF']*1e3, 1)
    N[f'{key}_share'] = f(r['PlF']/r['Pstar']*100, 0); N[f'{key}_times'] = f(r['PpF']/r['Pstar'], 0)
tr = ['<p class="tcap">Table 2. The maxon RE 25 motor with a GP 32 C gearhead at each mounting: the catalogue ratio and load resistor that give the load the most power by (7.6) and (7.7), the swing and the power the rotor pays in the full equation (7.4), and the power at the load by both routes and as a share of $P^*$. Mounting: rotor speed, pivot as a fraction of the blade.</p>'
      '<table class="mt"><thead><tr><th>mounting</th><th>$P^*$, mW</th><th>$N$</th><th>$R_L$, Ω</th><th>swing, rad</th>'
      '<th>rotor pays, mW</th><th>load by (7.7), mW</th><th>load, full, mW</th><th>÷ $P^*$</th></tr></thead><tbody>']
for r in sorted(g4, key=lambda r: (-r['rpm'], r['frac'])):
    tr.append(f'<tr><td>{r["rpm"]} rpm, {int(round(r["frac"]*100))} %</td><td>{r["Pstar"]*1e3:.2f}</td><td>{r["N"]}</td><td>{r["R_load"]:.1f}</td>'
              f'<td>{r["ThF"]:.3f}</td><td>{r["PpF"]*1e3:.2f}</td><td>{r["P_load"]*1e3:.2f}</td><td>{r["PlF"]*1e3:.2f}</td><td>{r["PlF"]/r["Pstar"]*100:.0f} %</td></tr>')
tr.append('</tbody></table>')
T['generator'] = '\n'.join(tr)

(ROOT / 'numbers.json').write_text(json.dumps({'n': N, 'table': T}, ensure_ascii=False, indent=1))
print(f'wrote numbers.json: {len(N)} numbers, {len(T)} tables')
