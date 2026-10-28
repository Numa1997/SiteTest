#!/usr/bin/env python3
"""Every number and table the lecture notes quote, computed here and written to numbers.json.

The theory sources write {{n:key}} for a number and {{table:key}} for a table; tools/build_theory.py substitutes them and
stops on any key that is not here.  So no number in the text is typed by hand.
The machine: a second blade (a thin uniform rod of mass m and length l) hinged at the 63 m tip of the NREL 5-MW blade.
Inputs: the formulas below, and the stored results of the models in data/ (copied from notes/rotor-pendula/derive/):
setup.json, sensor.json, design.json (the setup and the sizing rule); sizes.json (the range of sizes); L1_blade.json, L1_blade_checks.json (the full equation
at the three winds, engine checks); L1_chaos_blade.json; L2_scales.json, L2_run_nrel.json, L2_run_k2.json (gusts);
L3_sag_tip.json, L3_shake2.json (the mother blade's sag and shaking); L4_generator.json, L4_check_2000.json,
L4_sensitivity.json (the geared generator); mc_full.log (power_theorem_mc.py).  Run: python3 tools/make_numbers.py
"""
import json, math, pathlib, re
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT / 'data'
J = lambda name: json.load(open(D / name))
N = {}                       # key -> formatted string
T = {}                       # key -> HTML table

def f(x, d):
    return f'{x:.{d}f}'.replace('-', '−')
def sgn(x, d):
    return (f'{x:+.{d}f}').replace('-', '−')
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
def sig3(x):                 # three significant figures, plain digits, thin-space thousands
    d = 2 - math.floor(math.log10(abs(x)))
    return f'{x:.{d}f}' if d >= 0 else f'{round(x, d):,.0f}'.replace(',', ' ')
def sci(x, d=0):
    m, e = f'{x:.{d}e}'.split('e')
    return f'{m}·10{str(int(e)).translate(SUP)}'

# ---- the setup ------------------------------------------------------------------------------------------------------
S = J('setup.json')
g, rho, rp = S['G0'], S['RHO'], S['R_ROT']
m, l = S['M_B'], S['L_B']
I, mlc = m*l*l/3, m*l/2
LAM = S['LAM_STAR']; WINDS = [6.0, 8.0, 10.0]
Om = {v: LAM*v/rp for v in WINDS}
N['mB'] = f'{m:g}'; N['lB'] = f'{l:g}'; N['rho'] = f(rho, 3)
for v in WINDS:
    k = str(int(v))
    N[f'rpm_{k}'] = f(Om[v]*60/(2*math.pi), 2); N[f'vtip_{k}'] = f(Om[v]*rp, 1)
    Gam = Om[v]**2*rp/g
    N[f'Gam_{k}'] = f(Gam, 2); N[f'tilt_{k}'] = f(math.degrees(math.asin(1/Gam)), 1)
    N[f'G_{k}'] = f(mlc*g/(I*Om[v]**2), 2)
R = mlc*rp/I
N['R'] = f(R, 1); N['sqrtR'] = f(math.sqrt(R), 2); N['Rm1'] = f(R - 1, 1); N['Rm1_round'] = f'{round(R - 1, -1):.0f}'
N['R_round'] = f'{round(R):.0f}'
N['invGam_max'] = f(g/(Om[6.0]**2*rp), 2)
q8 = 0.5*rho*(Om[8.0]*rp)**2
N['q_8'] = f'{q8:.0f}'; N['mg'] = f(m*g, 2); N['air_area_cm2'] = f(m*g/q8*1e4, 1)
N['tau_star'] = f(mlc*g/math.sqrt(2), 2); N['mlg'] = f(mlc*g, 2)
N['sensor_uW'] = f(J('sensor.json')['need_uW'], 1)
N['sensor_20y_Wh'] = f(J('sensor.json')['need_uW']*1e-6*20*365.25*86400/3600, 1)   # twenty years of the minimal sensor
N['ceiling_frac'] = f(math.pi/(4*math.sqrt(2)), 3)
Pst = lambda O, gg=g, mm=m, ll=l: (mm*ll/2*gg)**2/(4*O*(mm*ll/2*rp - mm*ll*ll/3))

# ---- chapter 0 from scratch: the wind's power, Betz, the speed triangle at the tip ---------------------------------------
A_disc = math.pi*rp**2
N['disc_area'] = f'{A_disc:,.0f}'.replace(',', ' ')
N['pw_m2_8'] = f(0.5*rho*8.0**3, 0)
for v in WINDS:
    N[f'Pwind_{int(v)}'] = f(0.5*rho*A_disc*v**3/1e6, 2)
    N[f'PT_{int(v)}'] = f(0.5*rho*A_disc*v**3*S['CP_STAR']/1e6, 2)
N['cube_ratio'] = f((10/6)**3, 1)
N['door_mdot'] = f(rho*2*1*10, 1); N['door_P'] = f'{0.5*rho*2*1*10**3:,.0f}'.replace(',', ' ')   # the warm-up: a 2 m x 1 m doorway in 10 m/s
N['betz'] = f(16/27, 3); N['betz_pct'] = f(16/27*100, 0); N['cp_of_betz'] = f(S['CP_STAR']/(16/27)*100, 0)
ax8 = 8.0*(1 - 1/3); ut8 = Om[8.0]*rp
inflow = math.atan2(ax8, ut8)
N['ax8'] = f(ax8, 2); N['ut8'] = f(ut8, 1); N['app8'] = f(math.hypot(ax8, ut8), 1); N['inflow8'] = f(math.degrees(inflow), 1)
N['ld_min'] = f(1/math.tan(inflow), 1)
N['turn8_s'] = f(2*math.pi/Om[8.0], 1)
# chapter 0 problems: a storm at 12 m/s; a 2 m garden turbine at 6 m/s; the inflow angle halfway out, r = 31.5 m, at 8 m/s
N['p0_cube'] = f((12/8)**3, 2)
N['p0_small_wind'] = f(0.5*rho*math.pi*1.0**2*6.0**3, 0); N['p0_small_betz'] = f(0.5*rho*math.pi*1.0**2*6.0**3*16/27, 0)
N['p0_mid_inflow'] = f(math.degrees(math.atan2(ax8, Om[8.0]*rp/2)), 1); N['p0_mid_ut'] = f(Om[8.0]*rp/2, 1)
# a wind turbine from the side, not to scale (the nacelle drawn far too large so its inside shows): the parts, before the story
HUB_H, RPM_MAX, GEAR = 90, 12.1, 97                            # hub height (m), rated rotor speed (rpm), gearbox ratio: NREL/TP-500-38060, Table 1-1
W0, H0 = 600, 430
tb = [f'<svg viewBox="0 0 {W0} {H0}" style="width:100%;height:auto;max-width:{W0}px" role="img" aria-label="A wind turbine seen from the side. The wind comes from the left. A tower carries the nacelle; at its front the hub carries the blades. Inside the nacelle the main shaft runs from the hub to the gearbox, and a fast shaft from the gearbox to the generator. A small second blade is hinged at the tip of the upper blade.">',
      '<defs><marker id="ah0" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
      '<line x1="40" y1="410" x2="560" y2="410" stroke="#3f2c23" stroke-width="1.2"/>',
      '<polygon points="318,410 342,410 336,206 324,206" fill="#d8cfc0" stroke="#3f2c23" stroke-width="1.1"/>',
      '<text x="352" y="330" class="svgc">tower: the hub stands</text><text x="352" y="344" class="svgc">' + f'{HUB_H} m above the ground</text>',
      '<rect x="240" y="150" width="200" height="56" rx="10" fill="#f3ece0" stroke="#3f2c23" stroke-width="1.2" stroke-dasharray="5 3"/>',
      '<text x="452" y="182" class="svgd">nacelle</text>',
      '<rect x="232" y="174" width="68" height="8" fill="#8c7d6b" stroke="#3f2c23" stroke-width="0.8"/>',
      '<rect x="300" y="162" width="48" height="32" rx="3" fill="#e2cfa8" stroke="#3f2c23" stroke-width="1"/>',
      '<line x1="348" y1="178" x2="372" y2="178" stroke="#3f2c23" stroke-width="3"/>',
      '<rect x="372" y="164" width="52" height="28" rx="3" fill="#cfdde6" stroke="#3f2c23" stroke-width="1"/>',
      '<path d="M240,158 Q198,160 204,178 Q198,196 240,198 Z" fill="#e9ddc6" stroke="#3f2c23" stroke-width="1.2"/>',
      '<polygon points="219,170 231,170 228,30 224,30" fill="#efe6d6" stroke="#3f2c23" stroke-width="1.1"/>',
      '<polygon points="219,186 231,186 227,262 225,262" fill="#efe6d6" stroke="#3f2c23" stroke-width="1.1"/>',
      '<line x1="226" y1="30" x2="226" y2="16" stroke="#7d1d2f" stroke-width="3" stroke-linecap="round"/><circle cx="226" cy="30" r="2.6" fill="#fff" stroke="#3f2c23"/>',
      '<text x="236" y="22" class="svgc">hinge and second blade (section 0.5)</text>',
      '<text x="212" y="74" text-anchor="end" class="svgd">blade</text><text x="212" y="88" text-anchor="end" class="svgc">(the two others point</text><text x="212" y="100" text-anchor="end" class="svgc">down and overlap here)</text>',
      '<text x="196" y="182" text-anchor="end" class="svgd">hub</text>',
      '<line x1="270" y1="183" x2="270" y2="216" stroke="#3f2c23" stroke-width="0.8"/><text x="270" y="228" text-anchor="middle" class="svgc">main shaft,</text><text x="270" y="241" text-anchor="middle" class="svgc">slow</text>',
      '<line x1="324" y1="128" x2="324" y2="161" stroke="#3f2c23" stroke-width="0.8"/><text x="324" y="122" text-anchor="middle" class="svgc">gearbox</text>',
      '<line x1="398" y1="193" x2="398" y2="216" stroke="#3f2c23" stroke-width="0.8"/><text x="398" y="228" text-anchor="middle" class="svgc">generator</text>']
for y in (60, 130, 220, 300):
    tb.append(f'<line x1="60" y1="{y}" x2="150" y2="{y}" stroke="#33627f" stroke-width="2" marker-end="url(#ah0)"/>')
tb.append('<text x="105" y="52" text-anchor="middle" class="svgd">wind</text></svg>')
T['fig_turbine'] = ('<figure class="fig">' + ''.join(tb) +
    '<figcaption>Figure 1. A wind turbine seen from the side, not to scale: the nacelle is drawn far too large so that its inside can be seen. '
    'The wind comes from the left and turns the rotor, the hub with its three blades (seen from the side, the blade pointing up is a thin line, '
    'and the two pointing down overlap). The rotor turns the main shaft slowly; the gearbox makes the turning faster; the generator turns it into '
    f'electricity. For the 5 MW turbine of these notes the hub stands {HUB_H} m above the ground, the rotor turns at most about {RPM_MAX:.0f} times a '
    f'minute, and the gearbox speeds it up {GEAR} times (Jonkman et al. 2009). The machine of these notes sits at the tip of a blade.</figcaption></figure>')
# the triangle of speeds at the tip, 8 m/s, seen along the blade from its tip: the blade moves right, the wind blows down
# through the rotor (slowed by a third, the ideal rotor of section 0.2); the wind arrow is drawn EX times its length
EX, s5 = 3.0, 4.0                                             # exaggeration of the wind arrow; px per m/s
W5, H5 = 600, 330
ox, oy = 230, 120                                             # the blade piece
hx, hy = ut8*s5, ax8*s5*EX                                    # drawn components of the apparent wind
Tx, Ty = ox + hx, oy - hy                                     # where the apparent wind comes from (front, upwind)
ang_draw = math.degrees(math.atan2(hy, hx))
nrm = math.hypot(hx, hy); lxu, lyu = hy/nrm, hx/nrm           # lift: at right angles to the apparent wind, downwind and forward
L5 = 150
tri = [f'<svg viewBox="0 0 {W5} {H5}" style="width:100%;height:auto;max-width:{W5}px" role="img" aria-label="A piece of blade at the tip, seen along the blade. The blade moves to the right at {ut8:.1f} m/s, the wind blows down through the rotor at {ax8:.2f} m/s, so the air the blade meets, the apparent wind, comes almost head-on, {math.degrees(inflow):.1f} degrees off its path. The lift, at right angles to the apparent wind, points mostly downwind and leans slightly forward; its forward part turns the rotor.">',
       '<defs><marker id="ah5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
       # the speeds that add up to the apparent wind
       f'<line x1="{Tx:.1f}" y1="{Ty:.1f}" x2="{ox:.1f}" y2="{Ty:.1f}" stroke="#7d1d2f" stroke-width="2.2" marker-end="url(#ah5)"/>',
       f'<text x="{(Tx+ox)/2:.1f}" y="{Ty-10:.1f}" text-anchor="middle" class="svgc">air met because the blade moves: {ut8:.1f} m/s</text>',
       f'<line x1="{ox:.1f}" y1="{Ty:.1f}" x2="{ox:.1f}" y2="{oy-10:.1f}" stroke="#33627f" stroke-width="2.2" marker-end="url(#ah5)"/>',
       f'<text x="{ox-8:.1f}" y="{(Ty+oy)/2:.1f}" text-anchor="end" class="svgc">wind {ax8:.2f} m/s</text>',
       f'<text x="{ox-8:.1f}" y="{(Ty+oy)/2+14:.1f}" text-anchor="end" class="svgc">(drawn {EX:g}× long)</text>',
       f'<line x1="{Tx:.1f}" y1="{Ty:.1f}" x2="{ox+hx*0.06:.1f}" y2="{oy-hy*0.06:.1f}" stroke="#23160f" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#ah5)"/>',
       f'<text x="{Tx:.1f}" y="{Ty+95:.1f}" text-anchor="end" class="svgc">apparent wind, dashed:</text>',
       f'<text x="{Tx:.1f}" y="{Ty+109:.1f}" text-anchor="end" class="svgc">{math.hypot(ax8, ut8):.1f} m/s, {math.degrees(inflow):.1f}° off the path</text>']
# the blade piece: a slim wing section lying along the apparent wind, and its motion
ca, sa = hx/nrm, -hy/nrm
pts = []
for t in np.linspace(0, 2*math.pi, 40):
    u, w = 26*math.cos(t), 5*math.sin(t)*(1 + 0.6*math.cos(t))
    pts.append(f'{ox + u*ca - w*sa:.1f},{oy + u*sa + w*ca:.1f}')
tri.append(f'<polygon points="{" ".join(pts)}" fill="#e9ddc6" stroke="#3f2c23" stroke-width="1.2"/>')
tri.append(f'<line x1="{ox-180}" y1="{oy+50}" x2="{ox-70}" y2="{oy+50}" stroke="#3f2c23" stroke-width="1.4" marker-end="url(#ah5)"/>')
tri.append(f'<text x="{ox-125}" y="{oy+68}" text-anchor="middle" class="svgc">the blade moves this way</text>')
# the lift and its two parts
Lx, Ly = ox + lxu*L5, oy + lyu*L5
tri.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{Lx:.1f}" y2="{Ly:.1f}" stroke="#3c6a46" stroke-width="2.6" marker-end="url(#ah5)"/>')
tri.append(f'<text x="{Lx+10:.1f}" y="{Ly-6:.1f}" class="svgd">lift</text>')
tri.append(f'<line x1="{ox:.1f}" y1="{Ly:.1f}" x2="{Lx:.1f}" y2="{Ly:.1f}" stroke="#3c6a46" stroke-width="1.6" stroke-dasharray="3 3" marker-end="url(#ah5)"/>')
tri.append(f'<text x="{Lx+10:.1f}" y="{Ly+14:.1f}" class="svgc">its forward part (dotted) turns the rotor;</text>')
tri.append(f'<text x="{Lx+10:.1f}" y="{Ly+28:.1f}" class="svgc">the rest pushes the rotor downwind</text>')
tri.append('</svg>')
T['fig_triangle'] = ('<figure class="fig">' + ''.join(tri) +
    f'<figcaption>Figure 2. A piece of blade at the tip, seen along the blade from its tip, at 8 m/s. The blade moves to the right at {ut8:.1f} m/s, '
    f'so air streams at it, from the direction it moves in, at that speed; the wind, from upwind along the shaft, blows through the rotor at {ax8:.2f} m/s, slowed by a third (section 0.2). '
    f'Together they make the apparent wind, which comes in only {math.degrees(inflow):.1f}° off the blade\'s path; the wind arrow is drawn {EX:g} times '
    f'too long so that the angle can be seen (it is drawn at {ang_draw:.0f}°). The lift is at right angles to the apparent wind: mostly it pushes the rotor '
    f'downwind, but it leans forward by the same angle, and that forward part is what turns the rotor.</figcaption></figure>')
# ---- the three winds: small-swing theory and the full equation (L1_blade.json) ---------------------------------------
runs = J('L1_blade.json')
assert all(r['m'] == m and r['l'] == l for r in runs), 'L1_blade.json is for another second blade'
best = {r['wind']: r for r in runs if r['mult'] == 1.0}
rows = ['<p class="tcap">Table 1. The second blade at the three winds, at its best brake. At every wind $R = ' + f(R, 1) + '$ and $\\kappa^* = R - 1 = ' + f(R - 1, 1) + '$; '
        'full: the full nonlinear model of chapter 3 at the same brake.</p>'
        '<table class="mt"><thead><tr><th>wind</th><th>rotor</th><th>$G$</th><th>$c^*$ (N m s)</th>'
        '<th>$\\Theta^*$ (rad)</th><th>$P^*$ (2.5), mW</th><th>full, mW</th></tr></thead><tbody>']
errs = []; flat = []
for v in WINDS:
    G = mlc*g/(I*Om[v]**2); ks = R - 1; Th = G/(math.sqrt(2)*ks); P = Pst(Om[v]); full = best[v]['P']
    errs.append(abs(P/full - 1)); flat.append(mlc*g**2/(4*Om[v]*rp))
    N[f'flat_{int(v)}'] = f(flat[-1]*1e3, 1)
    rows.append(f'<tr><td>{v:.0f} m/s</td><td>{Om[v]*60/(2*math.pi):.2f} rpm</td><td>{G:.2f}</td>'
                f'<td>{ks*I*Om[v]:.1f}</td><td>{Th:.3f}</td><td>{P*1e3:.1f}</td><td>{full*1e3:.1f}</td></tr>')
rows.append('</tbody></table>')
T['winds'] = '\n'.join(rows)
N['lin_err_max'] = f(max(errs)*100, 2)
# chapter 2: the worked example at 8 m/s and the problems at 10 m/s, from the small-swing theory (2.2), (2.4), (2.5)
for v in WINDS:
    k = str(int(v)); Gv = mlc*g/(I*Om[v]**2); Thv = Gv/(math.sqrt(2)*(R - 1))
    N[f'Th_{k}'] = f(Thv, 3); N[f'Th_{k}_deg'] = f(math.degrees(Thv), 1); N[f'Th_{k}_cm'] = f(Thv*l*100, 0)
    N[f'cst_{k}'] = f((R - 1)*I*Om[v], 1); N[f'Pst_{k}'] = f(Pst(Om[v])*1e3, 0)
N['flat_err_max'] = f(max(abs(fl/Pst(Om[v]) - 1) for fl, v in zip(flat, WINDS))*100, 1)
N['P_low'] = f(best[10.0]['P']*1e3, 0); N['P_high'] = f(best[6.0]['P']*1e3, 0)
PT = lambda v: 0.5*rho*math.pi*rp**2*v**3*S['CP_STAR']
N['share_max'] = f(max(best[v]['P']/PT(v) for v in WINDS)*1e6, 2)
# chapter 1: the car warm-up (3 m/s^2), the outward pull at 8 m/s, the rotor's torques at 6 m/s, problems
N['p1_car'] = f(math.degrees(math.atan(3/g)), 1); N['p1_brake'] = f(math.degrees(math.atan(7/g)), 1)
N['acc8'] = f(Om[8.0]**2*rp, 1); N['acc8_om'] = f(Om[8.0], 3); N['acc8_om2'] = f(Om[8.0]**2, 3)
N['tq_lift'] = f(m*g*rp, 0); N['tq_harv6'] = f(best[6.0]['P']/Om[6.0], 3); N['tq_turb6'] = f(PT(6.0)/Om[6.0]/1e6, 2)
N['zeta_star'] = f((R - 1)/(2*math.sqrt(R)), 1)
N['p1_f8'] = f(Om[8.0]*math.sqrt(R)/(2*math.pi), 2); N['p1_fground'] = f(math.sqrt(mlc*g/I)/(2*math.pi), 2)
N['p1_sqrtGam8'] = f(math.sqrt(Om[8.0]**2*rp/g), 2)
N['p1_v_gam1'] = f(math.sqrt(g/rp)*rp/LAM, 2)
th6 = best[6.0]
N['Th_max'] = f(th6['Theta'], 3); N['Th_max_deg'] = f(math.degrees(th6['Theta']), 1)
G6 = mlc*g/(I*Om[6.0]**2)
lt = -G6**2/(4*R*(R - 1))
N['lean_theory'] = f(lt, 4); N['lean_deg'] = f(math.degrees(abs(lt)), 2); N['lean_run'] = f(th6['trail'], 4)
ck = J('L1_blade_checks.json')
N['relax_8'] = f(ck['relax_s'], 3); N['turn_8'] = f(ck['turn_s'], 2)
N['relax_slow8'] = f((R - 1)/(R*Om[8.0]), 2)
for r in J('L1_terms.json'): N[f"trm_th2_{int(r['wind'])}"] = '−' + f(abs(r['grav'] - r['param'])*100, 1)
# the real steady rotor speed under the turbine's own torque law (L2_steady.py)
for r in J('L2_steady.json'):
    k = str(int(r['wind'])); N[f'rpm_real_{k}'] = f(r['nrel']['rpm'], 2); N[f'lam_real_{k}'] = f(r['nrel']['lam'], 2)
    N[f'Preal_pct_{k}'] = ('+' if r['nrel']['P_ratio'] >= 1 else '−') + f(abs(r['nrel']['P_ratio'] - 1)*100, 0)
    N[f'Pst_real_{k}'] = f(Pst(r['nrel']['Om'])*1e3, 0)
# chapter 8: the air on the second blade (L5_air.py)
_A = J('L5_air.json')
N['air_W'] = f(_A['W'], 1); N['air_gam'] = f(_A['gam_deg'], 2); N['air_q'] = f'{_A["q"]:,.0f}'.replace(',', ' ')
N['air_du'] = f(_A['du_shear'], 2); N['air_dg'] = f(_A['dgam_shear_deg'], 2); N['air_dWt'] = f(_A['dW_tilt'], 2)
N['air_Re_rod'] = f'{round(_A["Re_rod"], -3):,.0f}'.replace(',', ' '); N['air_Re_wing'] = f'{round(_A["Re_wing"], -4):,.0f}'.replace(',', ' ')
N['air_d_rod'] = f(_A['d_rod']*1e3, 1); N['air_G'] = f(_A['G_torque'], 2)
for k, c in _A['cases'].items():
    N[f'air_{k}_Ft'] = ('+' if c['Ft'] >= 0 else '−') + f(abs(c['Ft']), 1); N[f'air_{k}_lean'] = ('+' if c['lean_deg'] >= 0 else '−') + f(abs(c['lean_deg']), 1)
    N[f'air_{k}_P'] = f'{abs(c["P_rotor"]):,.0f}'.replace(',', ' '); N[f'air_{k}_As'] = f(c['A_shear'], 2); N[f'air_{k}_At'] = f(c['A_tilt'], 2)
    N[f'air_{k}_lo'] = ('+' if c['ratio_lo'] >= 1 else '−') + f(abs(c['ratio_lo'] - 1)*100, 0); N[f'air_{k}_hi'] = ('+' if c['ratio_hi'] >= 1 else '−') + f(abs(c['ratio_hi'] - 1)*100, 0)
    N[f'air_{k}_cair'] = f(c['c_air'], 2)
N['air_mOm2rp'] = f(m*Om[8.0]**2*rp, 1)
N['lam_k2'] = f(J('L2_steady.json')[1]['k2']['lam'], 2)
# chapter 3: each neglected term alone, against the small-swing power, at the best brake (L1_terms.py)
for r in J('L1_terms.json'):
    k = str(int(r['wind']))
    for t in ('param', 'sin', 'grav', 'full'): N[f'trm_{t}_{k}'] = ('+' if r[t] >= 0 else '−') + f(abs(r[t])*100, 2); N['relax_slow10'] = f((R - 1)/(R*Om[10.0]), 2); N['om10'] = f(Om[10.0], 3)
# chapter 4: the white-noise shaking that would match gravity's best power at 8 m/s, and what it means as an acceleration over 0 to 10 Hz
S_match = 2*Pst(Om[8.0])/(0.75*m); N['S_match'] = f(S_match, 2); N['arms_match'] = f(math.sqrt(2*S_match*10), 1)
# chapter 7: how fast the hinge turns at the best brake (Omega Theta*)
N['w_hinge_lo'] = f(Om[10.0]*mlc*g/(I*Om[10.0]**2)/(math.sqrt(2)*(R - 1)), 2); N['w_hinge_hi'] = f(Om[6.0]*mlc*g/(I*Om[6.0]**2)/(math.sqrt(2)*(R - 1)), 2)
N['p3_bill'] = f(mlc*rp*Om[6.0]**3*abs(th6['trail'])*1e3, 0); N['P6_full'] = f(th6['P']*1e3, 0)                 # the slow root of mu^2 + kappa mu + R = 0 at the best brake, in seconds
for v in WINDS: N[f'lean_deg_{int(v)}'] = f(math.degrees((mlc*g/(I*Om[v]**2))**2/(4*R*(R - 1))), 2)
N['radau_order'] = f(ck['order_mean'], 1); N['newton_agree'] = sci(ck['newton_max_rel'])
N['scipy_agree'] = sci(ck['scipy_rel']); N['startup_err'] = sci(ck['startup_rel'])
N['bill_err'] = sci(ck['bill_max_rel'])
# a lump of the same mass at the end of a massless rod of the same length, against the uniform rod (3.4), at 8 m/s
Ppoint = (m*l*g)**2/(4*Om[8.0]*(m*l*rp - m*l*l))
N['rod_vs_point'] = f(Ppoint/Pst(Om[8.0]), 3)

def panel(w_, h_, l0, r0, t0, b0):
    return (lambda xv, x0, x1: l0 + (xv - x0)/(x1 - x0)*(w_ - l0 - r0)), (lambda yv, y0, y1: t0 + (1 - (yv - y0)/(y1 - y0))*(h_ - t0 - b0))   # plot frame: data to svg coordinates

# ---- figure: the turning frame's potential, a bowl whose bottom rocks once per turn (6 m/s, where the rocking is largest) ------
Gam6 = Om[6.0]**2*rp/g
W3, H3 = 560, 300
BX, BY = panel(W3, H3, 56, 150, 16, 48)
ths = np.linspace(-0.9, 0.9, 241)
u = lambda th, ph: -np.cos(th) + np.sin(ph + th)/Gam6          # U / [(m l/2) Omega^2 r_p]
umin, umax = -1.32, -0.35
bowl_cols = [('#7d1d2f', 0, 'φ = 0°, rising'), ('#b5681c', 90, 'φ = 90°, up'), ('#33627f', 180, 'φ = 180°, falling'), ('#3c6a46', 270, 'φ = 270°, down')]
svg = [f'<svg viewBox="0 0 {W3} {H3}" role="img" aria-label="The potential energy of the second blade in the turning frame against its angle, at four rotor angles at 6 m/s: four bowls of the same shape whose lowest points move left and right by about 17 degrees once per turn.">',
       f'<rect x="56" y="16" width="{W3-206}" height="{H3-64}" fill="#fff" stroke="#3f2c23"/>']
for v in (-45, -30, -15, 0, 15, 30, 45):
    X = BX(math.radians(v), -0.9, 0.9); svg.append(f'<line x1="{X:.1f}" y1="{H3-48}" x2="{X:.1f}" y2="{H3-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{H3-30}" text-anchor="middle" class="svgc">{v}°</text>')
mins = []
for c, phd, lab in bowl_cols:
    ph = math.radians(phd); uu = u(ths, ph)
    svg.append('<polyline points="' + ' '.join(f'{BX(t, -0.9, 0.9):.1f},{BY(v, umin, umax):.1f}' for t, v in zip(ths, uu)) + f'" fill="none" stroke="{c}" stroke-width="2"/>')
    t0 = math.atan2(-math.cos(ph)/Gam6, 1 - math.sin(ph)/Gam6)            # exact minimum: dU/dtheta = 0
    mins.append(t0)
    svg.append(f'<circle cx="{BX(t0, -0.9, 0.9):.1f}" cy="{BY(float(u(t0, ph)), umin, umax):.1f}" r="4.5" fill="{c}" stroke="#fff" stroke-width="1.2"/>')
for i, (c, phd, lab) in enumerate(bowl_cols):
    svg.append(f'<line x1="{W3-140}" y1="{40+i*20}" x2="{W3-122}" y2="{40+i*20}" stroke="{c}" stroke-width="2.4"/><text x="{W3-116}" y="{44+i*20}" class="svgc">{lab}</text>')
svg.append(f'<text x="{(56+W3-150)/2}" y="{H3-10}" text-anchor="middle" class="svgd">angle θ of the second blade from the mother blade\'s line</text>')
svg.append(f'<text x="18" y="{(16+H3-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 18 {(16+H3-48)/2})">potential energy U</text>')
svg.append('</svg>')
T['fig_bowl'] = ('<figure class="fig">' + ''.join(svg) +
    f'<figcaption>Figure 5. The second blade\'s potential energy (1.4) in the frame of the mother blade, at 6 m/s ($\\Gamma = {N["Gam_6"]}$), '
    f'at four positions of the rotor. The shape of the bowl is the centrifugal term and does not change; gravity tilts it, and its lowest point '
    f'(dots) swings between {N["tilt_6"]}° on one side and {N["tilt_6"]}° on the other, $\\arcsin(1/\\Gamma)$, and back, once per turn. The second blade is a marble in this bowl, '
    f'held in honey by the generator: it chases the moving bottom, and the generator takes energy from the chase.</figcaption></figure>')

# ---- figure: the universal brake curve P/P* = 2x/(1+x^2), x = kappa/kappa*, on a log axis ----------------------------
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
    f'<figcaption>Figure 6. The harvested power (2.3) over its maximum (2.5), against the brake over the best brake (2.4): '
    f'$\\bar P/P^* = 2x/(1+x^2)$ with $x = \\kappa/\\kappa^*$, the same curve at every wind and for every second blade. The top is flat: a brake '
    f'{2-math.sqrt(3):.2f} times the best, or {2+math.sqrt(3):.1f} times it, still gives half the power ($x = 2 \\mp \\sqrt3$).</figcaption></figure>')

# ---- figure: theory against the full equation (compare.json, from the page's own engine, tools/compare.js) -------------------
cp = J('compare.json')['winds']
WCOL = {6.0: '#7d1d2f', 8.0: '#b5681c', 10.0: '#33627f'}
W1, H1 = 380, 300
PX, PY = panel(W1, H1, 50, 14, 16, 48)
lx = lambda x: math.log10(x)
svgA = [f'<svg viewBox="0 0 {W1} {H1}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="Harvested power over its small-swing maximum against the brake over the best brake, 0.05 to 20, at 6, 8 and 10 m/s: lines from formula (2.3), dots from the full equation. The dots sit on the lines except at light brakes in weak wind, where they rise above.">',
        f'<rect x="50" y="16" width="{W1-64}" height="{H1-64}" fill="#fff" stroke="#3f2c23"/>']
for v, lab in ((0.05, '0.05'), (0.1, '0.1'), (1, '1'), (10, '10'), (20, '20')):
    X = PX(lx(v), lx(0.05), lx(20)); svgA.append(f'<line x1="{X:.1f}" y1="{H1-48}" x2="{X:.1f}" y2="{H1-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{H1-30}" text-anchor="middle" class="svgc">{lab}</text>')
for v in (0, 0.5, 1):
    Y = PY(v, 0, 1.12); svgA.append(f'<line x1="45" y1="{Y:.1f}" x2="50" y2="{Y:.1f}" stroke="#3f2c23"/><text x="41" y="{Y+4:.1f}" text-anchor="end" class="svgc">{v:g}</text>')
for w in cp:
    c = WCOL[w['wind']]; Ps = w['Pstar']
    xs = np.logspace(math.log10(0.05), math.log10(20), 160)
    pts = ' '.join(f'{PX(lx(x), lx(0.05), lx(20)):.1f},{PY(2*x/(1 + x*x), 0, 1.12):.1f}' for x in xs)
    if w['wind'] == 8.0:
        svgA.append(f'<polyline points="{pts}" fill="none" stroke="#3f2c23" stroke-width="1.6"/>')
    for sp in w['sweep']:
        svgA.append(f'<circle cx="{PX(lx(sp["x"]), lx(0.05), lx(20)):.1f}" cy="{PY(sp["P"]/Ps, 0, 1.12):.1f}" r="3" fill="{c}" fill-opacity="0.85"/>')
svgA.append(f'<text x="{(50+W1-14)/2}" y="{H1-10}" text-anchor="middle" class="svgd">brake over best brake, κ/κ*</text>')
svgA.append(f'<text x="14" y="{(16+H1-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 14 {(16+H1-48)/2})">P / P*</text>')
for i, w in enumerate(cp):
    svgA.append(f'<circle cx="{W1-110}" cy="{34+i*16}" r="3.5" fill="{WCOL[w["wind"]]}"/><text x="{W1-102}" y="{38+i*16}" class="svgc">{w["wind"]:.0f} m/s, full</text>')
svgA.append(f'<line x1="{W1-114}" y1="{82}" x2="{W1-104}" y2="{82}" stroke="#3f2c23" stroke-width="1.6"/><text x="{W1-102}" y="{86}" class="svgc">formula (2.3)</text>')
svgA.append('</svg>')
PX2, PY2 = panel(W1, H1, 50, 14, 16, 48)
qm = max(max(abs(q) for q in w['turn']['q']) for w in cp)*1.15
svgB = [f'<svg viewBox="0 0 {W1} {H1}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="One turn of the swing angle at the best brake, at 6, 8 and 10 m/s: the full equation as solid lines, the small-swing theory as dashed lines. They have the same shape and phase; the full solution sits slightly lower, by the mean trail.">',
        f'<rect x="50" y="16" width="{W1-64}" height="{H1-64}" fill="#fff" stroke="#3f2c23"/>',
        f'<line x1="50" y1="{PY2(0, -qm, qm):.1f}" x2="{W1-14}" y2="{PY2(0, -qm, qm):.1f}" stroke="#dccdb4"/>']
for v in (0, 90, 180, 270, 360):
    X = PX2(v, 0, 360); svgB.append(f'<line x1="{X:.1f}" y1="{H1-48}" x2="{X:.1f}" y2="{H1-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{H1-30}" text-anchor="middle" class="svgc">{v}°</text>')
for v in (-0.2, -0.1, 0, 0.1, 0.2):
    if abs(v) <= qm:
        Y = PY2(v, -qm, qm); svgB.append(f'<line x1="45" y1="{Y:.1f}" x2="50" y2="{Y:.1f}" stroke="#3f2c23"/><text x="41" y="{Y+4:.1f}" text-anchor="end" class="svgc">{v:g}</text>')
trace_rms = []
for w in cp:
    c = WCOL[w['wind']]; ph = np.array(w['turn']['phi']); q = np.array(w['turn']['q'])
    A = -w['G']/(w['R'] - 1 + 1j*w['kappaStar']); ql = np.real(A*np.exp(1j*(ph + w['phi0'])))
    qs, qls = q[:-1], ql[:-1]                                  # one turn: the last sample repeats the first (0 and 360 degrees)
    trace_rms.append((w['wind'], float(np.sqrt(np.mean((qs - qls)**2))), float(np.mean(qs)), float(np.sqrt(np.mean((qs - qs.mean() - qls)**2)))))
    deg = np.degrees(ph)
    svgB.append('<polyline points="' + ' '.join(f'{PX2(a, 0, 360):.1f},{PY2(b, -qm, qm):.1f}' for a, b in zip(deg, ql)) + f'" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    svgB.append('<polyline points="' + ' '.join(f'{PX2(a, 0, 360):.1f},{PY2(b, -qm, qm):.1f}' for a, b in zip(deg, q)) + f'" fill="none" stroke="{c}" stroke-width="2"/>')
svgB.append(f'<text x="{(50+W1-14)/2}" y="{H1-10}" text-anchor="middle" class="svgd">rotor angle φ (0° = mother blade horizontal, rising)</text>')
svgB.append(f'<text x="14" y="{(16+H1-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 14 {(16+H1-48)/2})">θ, rad</text>')
svgB.append(f'<line x1="{W1-128}" y1="30" x2="{W1-112}" y2="30" stroke="#3f2c23" stroke-width="2"/><text x="{W1-106}" y="34" class="svgc">full equation</text>')
svgB.append(f'<line x1="{W1-128}" y1="46" x2="{W1-112}" y2="46" stroke="#3f2c23" stroke-width="1.4" stroke-dasharray="5 4"/><text x="{W1-106}" y="50" class="svgc">theory (2.2)</text>')
svgB.append('</svg>')
w6 = cp[0]; dev6 = [sp['P']/sp['Plin'] - 1 for sp in w6['sweep']]
devs = [(w['wind'], max(sp['P']/sp['Plin'] - 1 for sp in w['sweep']), w['sweep'][0]['Theta']) for w in cp]
N['cmp_dev6'] = f(devs[0][1]*100, 0); N['cmp_th6'] = f(devs[0][2], 2)
N['cmp_dev10'] = f(devs[2][1]*100, 1); N['cmp_th10'] = f(devs[2][2], 2)
N['cmp_coef_lo'] = f(min(d/t**2 for _, d, t in devs), 1); N['cmp_coef_hi'] = f(max(d/t**2 for _, d, t in devs), 1)
N['cmp_star_dev'] = f(max(abs(min(w['sweep'], key=lambda sp: abs(math.log(sp['x'])))['P']/w['Pstar'] - 1) for w in cp)*100, 1)
N['cmp_rms6'] = f(trace_rms[0][1], 3); N['cmp_mean6'] = f(trace_rms[0][2], 4); N['cmp_rest6'] = f(trace_rms[0][3], 4)
N['cmp_amp6'] = f(abs(-w6['G']/(w6['R'] - 1 + 1j*w6['kappaStar'])), 3)
T['fig_compare'] = ('<figure class="fig"><div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' + ''.join(svgA) + ''.join(svgB) + '</div>'
    f'<figcaption>Figure 7. The small-swing theory against the full equation (1.6), solved by the simulation\'s own engine. '
    f'First panel: harvested power over its maximum $P^*$ (2.5), against the brake over the best brake. The line is formula (2.3), the same for every wind; '
    f'the dots are the full equation at 6 (wine), 8 (ochre) and 10 m/s (blue). Second panel: one turn of the swing at the best brake; '
    f'solid the full equation, dashed the theory (2.2). The two have the same shape and the same phase; the full swing is shifted down by its mean trail.</figcaption></figure>')

# ---- the trail is the bill: the second blade's pull on the hinge and its lever arm about the hub (drawn with the trail exaggerated)
EXT, th_d = 15, -math.radians(abs(float(N['lean_deg'])))*15
W8, H8 = 560, 312; hx8, hy8 = 70, 190; px8, py8 = 380, 190; L8 = 150
ex, ey = px8 + L8*math.cos(th_d), py8 - L8*math.sin(th_d)
cx8, cy8 = (px8 + ex)/2, (py8 + ey)/2
ux, uy = cx8 - hx8, cy8 - hy8; un = math.hypot(ux, uy); ux, uy = ux/un, uy/un
t8 = (hx8 - px8)*ux + (hy8 - py8)*uy; fx, fy = px8 + t8*ux, py8 + t8*uy     # foot of the perpendicular from the hub to the pull's line
tr = [f'<svg viewBox="0 0 {W8} {H8}" style="width:100%;height:auto;max-width:{W8}px" role="img" aria-label="The hub on the left, the mother blade running right to the hinge. The second blade leaves the hinge trailing below the mother blade line, against the rotation, which goes upward at the hinge. An arrow at the hinge shows the second blade pulling on it along the line from the hub to its centre of mass; that line passes a little below the hub, and the short gap is the lever arm.">',
      '<defs><marker id="ah8" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
      f'<line x1="{hx8}" y1="{hy8}" x2="{px8}" y2="{py8}" stroke="#6f665e" stroke-width="12" stroke-linecap="round" opacity="0.35"/>',
      f'<circle cx="{hx8}" cy="{hy8}" r="8" fill="#23160f"/><text x="{hx8}" y="{hy8+28}" text-anchor="middle" class="svgd">hub</text>',
      f'<text x="{(hx8+px8)/2}" y="{hy8+26}" text-anchor="middle" class="svgd">mother blade</text>',
      f'<line x1="{px8}" y1="{py8}" x2="{px8+L8+20}" y2="{py8}" stroke="#23160f" stroke-dasharray="3 3"/>',
      f'<line x1="{px8}" y1="{py8}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#7d1d2f" stroke-width="7" stroke-linecap="round"/>',
      f'<circle cx="{px8}" cy="{py8}" r="6" fill="#fff" stroke="#23160f" stroke-width="2"/><text x="{px8-8}" y="{py8+24}" text-anchor="end" class="svgd">hinge</text>',
      f'<circle cx="{cx8:.1f}" cy="{cy8:.1f}" r="3.4" fill="#fff" stroke="#23160f"/><text x="{cx8-8:.1f}" y="{cy8+16:.1f}" text-anchor="end" class="svgc">centre of mass</text>',
      f'<text x="{ex+4:.1f}" y="{ey+24:.1f}" text-anchor="end" class="svgc">second blade, trailing</text><text x="{ex+4:.1f}" y="{ey+38:.1f}" text-anchor="end" class="svgc">(drawn {EXT}× too far)</text>',
      f'<line x1="{px8}" y1="{py8-22}" x2="{px8}" y2="{py8-82}" stroke="#33627f" stroke-width="2" marker-end="url(#ah8)"/><text x="{px8+8}" y="{py8-66}" class="svgc">the rotor turns this way</text>',
      f'<line x1="{px8}" y1="{py8}" x2="{px8 + 120*ux:.1f}" y2="{py8 + 120*uy:.1f}" stroke="#3c6a46" stroke-width="2.6" marker-end="url(#ah8)"/>',
      f'<text x="392" y="{py8-26}" class="svgc">pull on the hinge, along</text><text x="392" y="{py8-12}" class="svgc">hub → centre of mass</text>',
      f'<line x1="{px8:.1f}" y1="{py8:.1f}" x2="{fx:.1f}" y2="{fy:.1f}" stroke="#3c6a46" stroke-width="1" stroke-dasharray="5 4"/>',
      f'<line x1="{hx8}" y1="{hy8}" x2="{fx:.1f}" y2="{fy:.1f}" stroke="#7d1d2f" stroke-width="2"/>',
      f'<text x="{hx8+12}" y="{(hy8+fy)/2+4:.1f}" class="svgc">lever arm</text></svg>']
T['fig_trail'] = ('<figure class="fig">' + ''.join(tr) +
    f'<figcaption>Figure 8. Why the trail is the bill. The second blade trails behind the mother blade\'s line, against the rotation; the trail is drawn '
    f'{EXT} times too large (at 6 m/s it is {N["lean_deg"]}°). Flung outwards, the second blade pulls on the hinge in the direction from the hub to its '
    'centre of mass (green). The pull\'s line, through the hinge, misses the hub by a small lever arm (wine), so the pull holds the rotor back, with the torque '
    f'$\\tfrac{{ml}}{{2}}r_p\\Omega^2\\sin\\theta$; on average {N["tq_harv6"]} N m at 6 m/s. The rotor pushes against it, and that steady push is the power it pays.</figcaption></figure>')
# ---- chaos (L1_chaos_blade.json) ---------------------------------------------------------------------------------------
ch = J('L1_chaos_blade.json')
lmax = max(max(o['lyap']) for o in ch); nstart = len(ch[0]['lyap'])
regular = lmax < 1e-3
krels = sorted({o['krel'] for o in ch}, reverse=True)
rows = [f'<p class="tcap">Table 2. The largest Lyapunov exponent per turn at each wind and brake, the largest over the {nstart} starting states tried; '
        'beside it the decay rate per turn of a small disturbance of the braked spring alone, $2\\pi\\,\\max\\,\\mathrm{Re}\\,\\mu$, where $\\mu$ are the two roots of $\\mu^2 + \\kappa\\mu + R = 0$.</p>'
        '<table class="mt"><thead><tr><th>wind</th><th>$G$</th><th>brake</th><th>$\\Lambda$ per turn</th><th>small-swing decay</th></tr></thead><tbody>']
for v in WINDS:
    for k in krels:
        o = next(o for o in ch if o['wind'] == v and o['krel'] == k)
        rows.append(f'<tr><td>{v:.0f} m/s</td><td>{o["G"]:.2f}</td><td>{k:g} $\\kappa^*$</td><td>{f(max(o["lyap"]), 2)}</td><td>{f(o["lin"], 2)}</td></tr>')
rows.append('</tbody></table>')
lin_gap = max(abs(max(o['lyap'])/o['lin'] - 1) for o in ch)
step_gap = max(abs(a/b - 1) for o in ch for a, b in zip(o['lyap'], o['lyap480']))     # relative: all exponents are far from zero
verdict = ('Every exponent is negative: every start, at every wind and brake, ends on the same regular, periodic swing. '
           if regular else 'Some exponents are positive: the motion there is chaotic. ')
verdict += (f'More than that, each exponent is the decay rate of a small disturbance of the braked centrifugal spring alone, to within {f(lin_gap*100, 1)} %: '
            'the motion forgets its start as fast as a linear, damped spring forgets a nudge. ')
T['chaos_text'] = (
    '<p>A pendulum driven periodically and braked can move chaotically: two copies started a hair apart drift apart exponentially, '
    'like two leaves dropped side by side into a stream. Our second blade is such a pendulum, (1.6), so the question must be asked. '
    'The rate of that drift is the <b>largest Lyapunov exponent</b> $\\Lambda$: start two copies $10^{-8}$ apart, follow them, rescale their '
    'separation back every quarter turn of the rotor, and divide the logarithm of the total growth by the number of turns. A regular, '
    'damped motion gives $\\Lambda < 0$; chaos gives $\\Lambda > 0$. Because chaos depends on where the motion starts, every case is run '
    f'from {nstart} different starts, the second blade at rest on the mother blade\'s line and {nstart - 1} at random angles and rates, some '
    'tumbling right over at first; and at the best brake and at a tenth and a hundredth of it, where a lightly braked swing has the most freedom.</p>'
    f'<div class="press"><div class="ctag">On our blade</div>' + '\n'.join(rows) + '\n' + verdict +
    f'Halving the step changes the exponents by at most {f(step_gap*100, 1)} % of their size. The physical reason is the centrifugal spring: at $R = {N["R"]}$ '
    f'it is {f(R/max(o["G"] for o in ch), 1)} to {f(R/min(o["G"] for o in ch), 1)} times stronger than gravity\'s push, so whatever the start, the second blade is pulled back '
    'to the mother blade\'s line and swings there in step with the push; chaos needs a spring and a push of similar strength, near resonance, '
    'and section 2.5 showed that a second blade never gets there.</div>')
N['chaos_regular'] = 'regular' if regular else 'chaotic in part'

# ---- power theorem Monte Carlo (the general theorem, run on a bob and a double pendulum) --------------------------------
log = (D / 'mc_full.log').read_text()
ratios = [abs(float(x) - 1)*100 for x in re.findall(r'ratio ([0-9.]+) \+-', log)]
N['mc_dev_max'] = f(max(ratios[1::2]), 2); N['mc_dev_min'] = f(min(ratios[1::2]), 2)
se = [float(x) for x in re.findall(r'ratio [0-9.]+ \+- ([0-9.]+)', log)][1::2]
N['mc_se_min'] = f(min(se)*100, 1); N['mc_se_max'] = f(max(se)*100, 1)
meff = re.findall(r'<m_eff>/M = ([0-9.]+)', log)
N['meff_single_large'] = f(float(meff[3]), 2); N['meff_double_chaos'] = f(float(meff[7]), 2)

# ---- gusts (L2) ---------------------------------------------------------------------------------------------------------
s_om = J('L2_scales.json')['sigOm']
N['sigOm'] = f(s_om*100, 1); N['jensen'] = f(s_om**2/2*100, 2)
N['store_s'] = f(0.5*4.38e7*Om[8.0]**2/PT(8.0), 0)          # seconds of its own output the rotor stores as kinetic energy, 8 m/s
eul = []
for law in ('nrel', 'k2'):
    d2 = J(f'L2_run_{law}.json'); mt = d2['mountings'][0]
    pt, pn, pu, P0 = np.array(mt['P_turb']), np.array(mt['P_noeuler']), np.array(mt['P_unif']), mt['P0']
    N[f'l2_{law}_tot'] = sgn(np.mean(pt - P0)/P0*100, 2); N[f'l2_{law}_wnd'] = sgn(np.mean(pn - pu)/P0*100, 2)
    N[f'l2_{law}_msh'] = sgn(np.mean(pu - P0)/P0*100, 2); N[f'l2_{law}_dOm'] = sgn((np.mean(mt['Om_mean'])/d2['Om0'] - 1)*100, 2)
    eul.append(abs(np.mean(pt - pn)/P0))
    N['l2_records'] = str(d2['NREC'])
N['l2_euler_parts'] = f(max(eul)*1e4, 0)
Om0 = J('L2_run_nrel.json')['Om0']
N['rpm_ctrl_8'] = f(Om0*60/(2*math.pi), 2); N['ctrl_vs_lam'] = f((1 - Om0/Om[8.0])*100, 1)

# ---- the mother blade's sag at the tip (L3_sag_tip.json) ------------------------------------------------------------------
sg = J('L3_sag_tip.json')['rows']
N['sag_lo_mm'] = f(min(x['w'] for x in sg)*1e3, 0); N['sag_hi_mm'] = f(max(x['w'] for x in sg)*1e3, 0)
N['sag_only_lo'] = f(min(x['sag_only'] for x in sg)*100, 1); N['sag_only_hi'] = f(max(x['sag_only'] for x in sg)*100, 1)
N['sag_tot_lo'] = sgn(min(x['total'] for x in sg)*100, 1); N['sag_tot_hi'] = sgn(max(x['total'] for x in sg)*100, 1)
N['sag_full_gap'] = f(max(abs(sg[0]['full_sag_only'] - sg[0]['sag_only']), abs(sg[0]['full_total'] - sg[0]['total']))*100, 1)

# ---- the mother blade's shaking (L3_shake2.json) -----------------------------------------------------------------------
sh = J('L3_shake2.json'); meta, sr = sh['meta'], sh['rows']
def pick(z, sgm, tuned):
    return next(r for r in sr if r['zeta'] == z and r['sig_tip'] == sgm and r['device'].startswith('tuned') == tuned)
N['sh_mb'] = f(meta['m_e'], 0); N['sh_dphi'] = f(meta['dPhi_p']*1e3, 1)
for sgm, key in ((0.005, '5'), (0.02, '20'), (0.1, '100')):
    a = pick(0.005, sgm, False)
    N[f'sh_one_{key}'] = sig3(a['P']*1e3)
N['sh_in_5'] = sig3(pick(0.005, 0.005, False)['P_in'])
N['sh_c_one'] = f(pick(0.005, 0.005, False)['c'], 2)
N['zeta_sh'] = f(pick(0.005, 0.005, False)['c']/(I*Om[8.0])/(2*math.sqrt(R)), 1)   # damping ratio of the second blade at the shaking's best brake
O0 = meta['Om0']; gt = g*math.cos(math.radians(5.0))
N['sh_cstar_one'] = f((mlc*rp/I - 1)*I*O0, 1)
N['grav_one'] = f(Pst(O0, gt)*1e3, 0)
N['rpm_O0'] = f(O0*60/(2*math.pi), 2)
_xs = pick(0.005, 0.005, False)['c']/((mlc*rp/I - 1)*I*O0); _gs = 2*_xs/(1 + _xs**2)*Pst(O0, gt)
N['sh_x'] = f(_xs, 3); N['grav_at_sh'] = f(_gs*1e3, 0); N['sh_tot_100'] = sig3((pick(0.005, 0.1, False)['P'] + _gs)*1e3)
we = 2*math.pi*meta['f_e']
N['freq_ratio'] = f(O0*math.sqrt(R)/we, 2)
Lt, mt_ = meta['L_tuned'], meta['m_tuned']
N['tu_L'] = f(Lt, 2); N['tu_m'] = f(mt_, 2)
for z, key in ((0.005, 'lo'), (0.03, 'hi')):
    tnd = pick(z, 0.005, True)
    N[f'tu_P_{key}'] = f(tnd['P']*1e3, 1); N[f'tu_Pw_{key}'] = f(tnd['P_wander']*1e3, 1)
    N[f'tu_share_{key}'] = f(tnd['P']/tnd['P_in']*100, 0); N[f'tu_q_{key}'] = f(tnd['q_rms'], 2)
    N[f'tu_tipcut_{key}'] = f((1 - tnd['x_rms']/0.005)*100, 0)
    N[f'tu_q20_{key}'] = f(pick(z, 0.02, True)['q_rms'], 2); N[f'tu_q100_{key}'] = f(pick(z, 0.1, True)['q_rms'], 2)
N['tu_mod_pct'] = f(gt/(2*O0**2*rp)*100, 1)
N['grav_tuned'] = f(Pst(O0, gt, mt_, Lt)*1e3, 0)

# ---- the geared generator (L4_generator.json: formula; L4_check_2000.json: full equation; L4_sensitivity.json) ---------
KT, KE, RC, JM, I0 = 0.0208, 0.02076, 1.53, 1.47e-6, 0.0402     # RE 25, part 339152 (typed_numbers.py)
T0 = KT*I0
csc1 = KT*KE/RC
cst = [(R - 1)*I*Om[v] for v in WINDS]
N['csc1'] = f'{csc1:.6f}'; N['cstar_min'] = f(min(cst), 1); N['cstar_max'] = f(max(cst), 1)
r2 = lambda x: float(f'{x:.2g}')
N['cstar_x'] = f'{r2(min(cst)/csc1):,.0f} to {r2(max(cst)/csc1):,.0f}'.replace(',', ' ')
N['Nneed_min'] = f(math.sqrt(min(cst)/csc1), 0); N['Nneed_max'] = f(math.sqrt(max(cst)/csc1), 0)
N['j_492'] = f((JM + 0.7e-7)*492**2/I, 2); N['T0_mNm'] = f(T0*1e3, 2)
N['fric_492'] = f(492*T0/0.6, 3); N['fricG_492'] = f(492*T0/0.6/(mlc*g)*100, 0)
N['Njam'] = f'{mlc*g*0.7/T0:,.0f}'.replace(',', ' '); N['Njam4'] = f'{mlc*g*0.6/T0:,.0f}'.replace(',', ' ')
gen = {r['wind']: r for r in J('L4_generator.json')}
chk = J('L4_check_2000.json')
full = {r['wind']: r for r in chk if r['kind'] == 'best' and r['mult'] == 1.0}
Nb = sorted({gen[v]['N'] for v in WINDS})
rows = ['<p class="tcap">Table 3. The maxon RE 25 with a GP 32 C gearhead in the hinge, at the ratio (' + ', '.join(f'{x:g}' for x in Nb) + ' : 1 at every wind) '
        'and load the formula (7.6)–(7.7) finds best. Swing and load are given as formula / full: the describing-function formula, and the '
        'full equation (7.8). Paid: what the rotor pays; the last two columns are the shares of it that reach the load and that friction takes.</p>'
        '<table class="mt"><thead><tr><th>wind</th><th>$R_L$, Ω</th><th>swing, rad</th>'
        '<th>load, mW</th><th>paid, mW</th><th>load</th><th>friction</th></tr></thead><tbody>']
for v in WINDS:
    a, b = gen[v], full[v]
    rows.append(f'<tr><td>{v:.0f} m/s</td><td>{a["R_load"]:.2f}</td>'
                f'<td>{a["Theta"]:.3f} / {b["Theta"]:.3f}</td><td>{a["P_load"]*1e3:.1f} / {b["P_load"]*1e3:.1f}</td><td>{b["P_paid"]*1e3:.1f}</td>'
                f'<td>{b["P_load"]/b["P_paid"]*100:.0f} %</td><td>{b["P_fric"]/b["P_paid"]*100:.0f} %</td></tr>')
rows.append('</tbody></table>')
T['generator'] = '\n'.join(rows)
need = J('sensor.json')['need_uW']*1e-6
loads = [full[v]['P_load'] for v in WINDS]
N['g4_min'] = f(min(loads)*1e3, 0); N['g4_max'] = f(max(loads)*1e3, 0)
_eff = [(gen[v]['kappa_e']/gen[v]['eta'] + 4*gen[v]['f']/(math.pi*gen[v]['Theta']))/(gen[v]['R'] - 1) for v in WINDS]
N['g4_brake_lo'] = f(min(_eff), 2); N['g4_brake_hi'] = f(max(_eff), 2)
_fr = [(2/math.pi)*gen[v]['f']*gen[v]['Theta']/(gen[v]['kappa_e']/gen[v]['eta']*gen[v]['Theta']**2/2 + (2/math.pi)*gen[v]['f']*gen[v]['Theta']) for v in WINDS]
N['g4_frg_lo'] = f(min(_fr)*100, 0); N['g4_frg_hi'] = f(max(_fr)*100, 0)
N['g4_th_max'] = f(max(max(gen[v]['Theta'], full[v]['Theta']) for v in WINDS), 2)   # the largest swing at the chosen settings
N['g4_margin'] = f'{min(loads)/need:,.0f}'.replace(',', ' ')
_mg = min(loads)/need; _e = 10**(len(str(int(_mg))) - 2); N['g4_margin_round'] = f'{int(_mg//_e*_e):,}'.replace(',', ' ')   # rounded down to two figures, for the prose
N['g4_share_min'] = f(min(full[v]['P_load']/Pst(Om[v]) for v in WINDS)*100, 0)
N['g4_share_max'] = f(max(full[v]['P_load']/Pst(Om[v]) for v in WINDS)*100, 0)
N['g4_eff_min'] = f(min(full[v]['P_load']/full[v]['P_paid'] for v in WINDS)*100, 0)
N['g4_eff_max'] = f(max(full[v]['P_load']/full[v]['P_paid'] for v in WINDS)*100, 0)
N['g4_fric_min'] = f(min(full[v]['P_fric']/full[v]['P_paid'] for v in WINDS)*100, 0)
N['g4_fric_max'] = f(max(full[v]['P_fric']/full[v]['P_paid'] for v in WINDS)*100, 0)
ce = [gen[v]['c_e']/((R - 1)*I*Om[v]) for v in WINDS]
N['ce_frac_min'] = f(min(ce), 2); N['ce_frac_max'] = f(max(ce), 2)
N['df_gap'] = f(max(abs(full[v]['P_load']/gen[v]['P_load'] - 1) for v in WINDS)*100, 1)
N['df_best'] = f(max(max(r['P_load'] for r in chk if r['kind'] == 'best' and r['wind'] == v)/full[v]['P_load'] - 1 for v in WINDS)*100, 1)
sens = J('L4_sensitivity.json')
for key, fr, eb in (('x2', 2, None), ('e5', 1, 0.5), ('x2e5', 2, 0.5)):
    P = [x['P_load'] for x in sens if x['fric'] == fr and x['eta'] == eb]
    N[f'sens_{key}_min'] = f(min(P)*1e3, 0); N[f'sens_{key}_max'] = f(max(P)*1e3, 0)
N['sens_margin'] = f'{min(x["P_load"] for x in sens if x["fric"] == 2 and x["eta"] == 0.5)/need:,.0f}'.replace(',', ' ')
base = [x for x in sens if x['fric'] == 1 and x['eta'] is None]
N['V_min'] = f(min(x['V'] for x in base), 2); N['V_max'] = f(max(x['V'] for x in base), 2)
N['f_turn_min'] = f(min(x['f_turn'] for x in base), 3); N['f_turn_max'] = f(max(x['f_turn'] for x in base), 3)
N['motor_rpm_max'] = f(max(x['motor_rpm'] for x in base), 0)
ds = J('design.json')
N['design_margin'] = f'{ds["margin"]:,.0f}'.replace(',', ' ')
rows = ['<p class="tcap">Table 4. The share of the best power $P^*$ the RE 25 + GP 32 C delivers to its load, against the mass of a 1 m second blade; '
        'mean over the three winds, and the ratio and load power at 8 m/s.</p><table class="mt"><thead><tr><th>mass (kg)</th><th>share of $P^*$</th>'
        '<th>ratio at 8 m/s</th><th>load at 8 m/s (mW)</th></tr></thead><tbody>']
for rr in ds['rows']:
    rows.append(f'<tr><td>{rr["m"]:g}</td><td>{rr["share"]*100:.1f} %</td><td>{rr["N"][1]:g}</td><td>{rr["P_load_W"][1]*1e3:.2f}</td></tr>')
rows.append('</tbody></table>')
T['sizing'] = '\n'.join(rows)
assert ds['pick'] == m, 'design.json picks another mass than setup.json'

# ---- the range of sizes (sizes.json): lengths 0.5 to 3 m, four mass densities ---------------------------------------------
zz = J('sizes.json'); zr = zz['rows']; mo = zz['mother']
rows = ['<p class="tcap">Table 5. The second blade over the range of real tip devices: length $l$, mass per length, mass $m$, first moment '
        '$ml/2$; the best power $P^*$ (2.5) at 6 and 10 m/s; the generator torque $\\tau^* = \\tfrac{ml}{2}g/\\sqrt2$ it must hold; the extra '
        'pull on the mother blade\'s tip at 10 m/s, $m\\Omega^2(r_p + l/2)$; and what the RE 25 + GP 32 C delivers to its load at 6 m/s. '
        'The row in bold is the size these notes use.</p>'
        '<table class="mt"><thead><tr><th>$l$, m</th><th>kg/m</th><th>$m$, kg</th><th>$ml/2$, kg m</th><th>$P^*$ 6 m/s, W</th><th>$P^*$ 10 m/s, W</th>'
        '<th>$\\tau^*$, N m</th><th>pull, kN</th><th>RE 25, mW</th></tr></thead><tbody>']
for r in zr:
    gl = r.get('gen_load_W'); gen = '–' if not gl or gl[0] is None else sig3(gl[0]*1e3)
    cells = [f"{r['l']:g}", f"{r['kg_per_m']:g}", f"{r['m']:g}", f"{r['m']*r['l']/2:g}", sig3(r['Pstar_W'][0]), sig3(r['Pstar_W'][2]),
             sig3(r['tau_star']), sig3(r['pull10_N']/1e3), gen]
    tr = ''.join(f'<td>{c}</td>' for c in cells)
    rows.append(f'<tr style="font-weight:600">{tr}</tr>' if (r['l'] == l and r['m'] == m) else f'<tr>{tr}</tr>')
rows.append('</tbody></table>')
T['sizes'] = '\n'.join(rows)
assert any(r['l'] == l and r['m'] == m for r in zr), 'sizes.json does not contain the size these notes use'
P6 = [r['Pstar_W'][0] for r in zr]
N['sz_P_lo'] = sig3(min(P6)*1e3); N['sz_P_hi'] = sig3(max(P6))
th = [r['Theta6'] for r in zr]; N['sz_th_lo'] = f(min(th), 3); N['sz_th_hi'] = f(max(th), 3)
N['sz_th_ref'] = f(g/(Om[6.0]**2*rp)/math.sqrt(2), 3)
tau = [r['tau_star'] for r in zr]; N['sz_tau_lo'] = sig3(min(tau)); N['sz_tau_hi'] = sig3(max(tau))
pulls = [r['pull10_N'] for r in zr]; N['sz_pull_max'] = sig3(max(pulls)/1e3); N['sz_pull_ours'] = sig3(next(r['pull10_N'] for r in zr if r['l'] == l and r['m'] == m)/1e3); N['sz_pull_ours_N'] = f(next(r['pull10_N'] for r in zr if r['l'] == l and r['m'] == m), 0)
big = [r['gen_load_W'][0] for r in zr if r['m']*r['l']/2 >= 0.5 - 1e-12 and r.get('gen_load_W') and r['gen_load_W'][0] is not None]
N['sz_plat_lo'] = sig3(min(big)*1e3); N['sz_plat_hi'] = sig3(max(big)*1e3)
N['sz_min_margin'] = f'{min(x for r in zr if r.get("gen_load_W") for x in r["gen_load_W"] if x)/need:,.0f}'.replace(',', ' ')   # every size, every wind
N['tip_kgm'] = f(mo['tip_kg_per_m'], 1); N['outer3_kg'] = f(mo['outer3_kg'], 0); N['outer3_pull'] = f(mo['outer3_pull10_N']/1e3, 1)

json.dump({'n': N, 'table': T}, open(ROOT / 'numbers.json', 'w'), indent=1, ensure_ascii=False)
print(f'{len(N)} numbers and {len(T)} tables written to numbers.json')
