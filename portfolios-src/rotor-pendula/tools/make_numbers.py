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
class _Once(dict):           # a table or figure key may be set only once: two figures under one key would show one of them twice
    def __setitem__(self, k, v):
        if k in self:
            raise SystemExit(f'table key set twice: {k}')
        super().__setitem__(k, v)
T = _Once()                  # key -> HTML table or figure; a figure's caption starts 'Figure {{fig:key}}.', numbered by tools/build_theory.py

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
      '<text x="236" y="22" class="svgc">hinge and second blade (section 1.1)</text>',
      '<text x="212" y="74" text-anchor="end" class="svgd">blade</text><text x="212" y="88" text-anchor="end" class="svgc">(the two others point</text><text x="212" y="100" text-anchor="end" class="svgc">down and overlap here)</text>',
      '<text x="196" y="182" text-anchor="end" class="svgd">hub</text>',
      '<line x1="270" y1="183" x2="270" y2="216" stroke="#3f2c23" stroke-width="0.8"/><text x="270" y="228" text-anchor="middle" class="svgc">main shaft,</text><text x="270" y="241" text-anchor="middle" class="svgc">slow</text>',
      '<line x1="324" y1="128" x2="324" y2="161" stroke="#3f2c23" stroke-width="0.8"/><text x="324" y="122" text-anchor="middle" class="svgc">gearbox</text>',
      '<line x1="398" y1="193" x2="398" y2="216" stroke="#3f2c23" stroke-width="0.8"/><text x="398" y="228" text-anchor="middle" class="svgc">generator</text>']
for y in (60, 130, 220, 300):
    tb.append(f'<line x1="60" y1="{y}" x2="150" y2="{y}" stroke="#33627f" stroke-width="2" marker-end="url(#ah0)"/>')
tb.append('<text x="105" y="52" text-anchor="middle" class="svgd">wind</text></svg>')
T['fig_turbine'] = ('<figure class="fig">' + ''.join(tb) +
    '<figcaption>Figure {{fig:turbine}}. A wind turbine seen from the side, not to scale: the nacelle is drawn far too large so that its inside can be seen. '
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
    f'<figcaption>Figure {{{{fig:speeds}}}}. A piece of blade at the tip, seen along the blade from its tip, at 8 m/s. The blade moves to the right at {ut8:.1f} m/s, '
    f'so air streams at it, from the direction it moves in, at that speed; the wind, from upwind along the shaft, blows through the rotor at {ax8:.2f} m/s, slowed by a third (section 6.2). '
    f'Together they make the apparent wind, which comes in only {math.degrees(inflow):.1f}° off the blade\'s path; the wind arrow is drawn {EX:g} times '
    f'too long so that the angle can be seen (it is drawn at {ang_draw:.0f}°). The lift is at right angles to the apparent wind: mostly it pushes the rotor '
    f'downwind, but it leans forward by the same angle, and that forward part is what turns the rotor.</figcaption></figure>')
# ---- the three winds: small-swing theory and the full equation (L1_blade.json) ---------------------------------------
runs = J('L1_blade.json')
assert all(r['m'] == m and r['l'] == l for r in runs), 'L1_blade.json is for another second blade'
best = {r['wind']: r for r in runs if r['mult'] == 1.0}
rows = ['<p class="tcap">Table 2. The second blade at the three winds, at its best brake. At every wind $R = ' + f(R, 1) + '$ and $\\kappa^* = R - 1 = ' + f(R - 1, 1) + '$; '
        'full: the full nonlinear equation of chapter 4 at the same brake.</p>'
        '<table class="mt"><thead><tr><th>wind</th><th>rotor</th><th>$G$</th><th>$c^*$ (N m s)</th>'
        '<th>$\\Theta^*$ (rad)</th><th>$P^*$ (3.5), mW</th><th>full, mW</th></tr></thead><tbody>']
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
# chapter 2: the worked example at 8 m/s and the problems at 10 m/s, from the small-swing theory (3.2), (2.4), (2.5)
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
_ks = R - 1; mu_slow = -_ks/2 + math.sqrt(_ks**2/4 - R); mu_fast = -_ks/2 - math.sqrt(_ks**2/4 - R)     # roots of mu^2 + kappa* mu + R = 0
N['relax_slow8'] = f(1/(abs(mu_slow)*Om[8.0]), 2)          # a displaced swing creeps back in this time, s (exact slow root)
for r in J('L1_terms.json'): N[f"trm_th2_{int(r['wind'])}"] = f((r['grav'] - r['param'])*100, 1)      # the rest of gravity's term: all of it less the rocking
N['p4_hmax_inv'] = f(math.pi*abs(mu_fast), 0)            # forward Euler is stable below 2/|mu_fast| rad of rotor angle: 1/(pi |mu_fast|) of a turn
# the real steady rotor speed under the turbine's own torque law (L2_steady.py)
for r in J('L2_steady.json'):
    k = str(int(r['wind'])); N[f'rpm_real_{k}'] = f(r['nrel']['rpm'], 2); N[f'lam_real_{k}'] = f(r['nrel']['lam'], 2)
    N[f'Preal_pct_{k}'] = ('+' if r['nrel']['P_ratio'] >= 1 else '−') + f(abs(r['nrel']['P_ratio'] - 1)*100, 0)
    N[f'Pst_real_{k}'] = f(Pst(r['nrel']['Om'])*1e3, 0)
# chapter 8: the air on the second blade (L5_air.py); a3: the wind slowed by a third at the tip, a0: not slowed
_A = J('L5_air.json'); _r3, _r0 = _A['runs']['a3'], _A['runs']['a0']
sg_ = lambda x, d: ('+' if x >= 0 else '−') + f(abs(x), d)
N['air_W'] = f(_r3['W'], 1); N['air_gam'] = f(_r3['gam_deg'], 2); N['air_gam0'] = f(_r0['gam_deg'], 2); N['air_q'] = f'{_r3["q"]:,.0f}'.replace(',', ' ')
N['air_du'] = f(_r3['du'], 2); N['air_dg'] = f(_r3['dgam_deg'], 2); N['air_dWt'] = f(_A['dW_tilt'], 2)
N['air_Re_rod'] = f'{round(_r3["Re_rod"], -3):,.0f}'.replace(',', ' '); N['air_Re_wing'] = f'{round(_r3["Re_wing"], -4):,.0f}'.replace(',', ' ')
N['air_d_rod'] = f(_A['d_rod']*1e3, 1); N['air_G'] = f(_A['G_torque'], 2)
for ak, rr in (('3', _r3), ('0', _r0)):
    for k, c in rr['cases'].items():
        N[f'air_{k}{ak}_Ft'] = sg_(c['Ft'], 1); N[f'air_{k}{ak}_lean'] = sg_(c['lean_deg'], 1); N[f'air_{k}{ak}_FG'] = f(abs(c['F_over_G']), 2)
        N[f'air_{k}{ak}_P'] = f'{abs(c["P_rotor"]):,.0f}'.replace(',', ' '); N[f'air_{k}{ak}_As'] = sg_(c['A_shear'], 2); N[f'air_{k}{ak}_At'] = sg_(c['A_tilt'], 2)
        N[f'air_{k}{ak}_pct'] = sg_((c['ratio'] - 1)*100, 0); N[f'air_{k}{ak}_cair'] = sg_(c['c_air'], 3); N[f'air_{k}{ak}_x'] = f(c['ratio'], 2)
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

# ---- figure: the apparent gravity at the hinge, in units of g: the outward pull Gamma plus gravity circling its end (6 m/s) ----------
Gq = Om[6.0]**2*rp/g; UQ = 86.0; hxq, hyq = 56, 150; txq = hxq + Gq*UQ
svgq = [f'<svg viewBox="0 0 560 300" role="img" aria-label="The apparent gravity at the hinge, seen from the mother blade at 6 metres per second. A long arrow from the hinge points out along the mother blade: the outward pull, 3.3 times gravity. Around its end a circle of radius one: gravity, which goes round once per turn. The sum of the two points from the hinge to a point on the circle; it tilts furthest from the mother blade, by arcsine of one over Gamma, along the two tangents from the hinge to the circle.">',
        '<defs><marker id="ahq" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
        f'<circle cx="{txq:.1f}" cy="{hyq}" r="{UQ}" fill="none" stroke="#dccdb4" stroke-width="1.6"/>',
        f'<line x1="{hxq}" y1="{hyq}" x2="{txq:.1f}" y2="{hyq}" stroke="#33627f" stroke-width="3" marker-end="url(#ahq)"/>',
        f'<text x="{hxq+150}" y="{hyq+17}" text-anchor="middle" class="svgc">outward pull, Γ = {N["Gam_6"]}</text>']
ft = math.asin(1/Gq)
for sgn_ in (1, -1):
    gx_, gy_ = -1/Gq, -math.cos(ft)*sgn_                     # gravity at the tangent rotor angles, in the frame of the mother blade
    ex_, ey_ = txq + gx_*UQ, hyq - gy_*UQ
    svgq.append(f'<line x1="{txq:.1f}" y1="{hyq}" x2="{ex_:.1f}" y2="{ey_:.1f}" stroke="#b5681c" stroke-width="2.2" marker-end="url(#ahq)"/>')
    svgq.append(f'<line x1="{hxq}" y1="{hyq}" x2="{ex_:.1f}" y2="{ey_:.1f}" stroke="#7d1d2f" stroke-width="2.6" marker-end="url(#ahq)"/>')
for phd, lab in ((0, 'φ = 0°'), (90, '90°'), (180, '180°'), (270, '270°')):
    ph_ = math.radians(phd); px_, py_ = txq - math.sin(ph_)*UQ, hyq + math.cos(ph_)*UQ
    svgq.append(f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="3.2" fill="#3f2c23"/>')
    dx_ = {0: 8, 90: -6, 180: 8, 270: 8}[phd]; dy_ = {0: 16, 90: -7, 180: -8, 270: 4}[phd]
    svgq.append(f'<text x="{px_+dx_:.1f}" y="{py_+dy_:.1f}" text-anchor="{"end" if phd == 90 else "start"}" class="svgc">{lab}</text>')
svgq.append(f'<path d="M{hxq+70} {hyq} A70 70 0 0 0 {hxq+70*math.cos(ft):.1f} {hyq-70*math.sin(ft):.1f}" fill="none" stroke="#3f2c23"/>')
svgq.append(f'<text x="{hxq+96}" y="{hyq-20}" class="svgc">arcsin(1/Γ) = {N["tilt_6"]}°</text>')
svgq.append(f'<circle cx="{hxq}" cy="{hyq}" r="5" fill="#fff" stroke="#23160f" stroke-width="2"/><text x="{hxq}" y="{hyq+22}" text-anchor="middle" class="svgd">hinge</text>')
svgq.append(f'<line x1="400" y1="34" x2="418" y2="34" stroke="#b5681c" stroke-width="2.2"/><text x="424" y="38" class="svgc">gravity, 1</text>')
svgq.append(f'<line x1="400" y1="52" x2="418" y2="52" stroke="#7d1d2f" stroke-width="2.6"/><text x="424" y="56" class="svgc">apparent gravity</text>')
svgq.append('</svg>')
T['fig_geff'] = ('<figure class="fig">' + ''.join(svgq) +
    f'<figcaption>Figure {{{{fig:geff}}}}. The pulls on every kilogram of the second blade, seen from the mother blade at 6 m/s, in units of $g$. The outward pull (blue), '
    f'$\\Gamma$ = {N["Gam_6"]} times gravity, points out along the mother blade; gravity (ochre), of length 1, goes round its end once per turn, the dots marking where it points '
    f'at four rotor angles $\\varphi$. Their sum (wine), the apparent gravity, tilts furthest from the mother blade along the two tangents from the hinge to the circle: '
    f'by $\\arcsin(1/\\Gamma)$ = {N["tilt_6"]}°, at $\\sin\\varphi = 1/\\Gamma$.</figcaption></figure>')

# ---- figure: the turning frame's potential, a bowl whose bottom rocks once per turn (6 m/s, where the rocking is largest) ------
Gam6 = Om[6.0]**2*rp/g
W3, H3 = 560, 300
BX, BY = panel(W3, H3, 56, 150, 16, 48)
ths = np.linspace(-0.9, 0.9, 241)
u = lambda th, ph: -np.cos(th) + np.sin(ph + th)/Gam6          # U / [(m l/2) Omega^2 r_p]
umin, umax = -1.32, -0.35
bowl_cols = [('#7d1d2f', 0, 'φ = 0°, rising'), ('#b5681c', 90, 'φ = 90°, up'), ('#33627f', 180, 'φ = 180°, falling'), ('#3c6a46', 270, 'φ = 270°, down')]
svg = [f'<svg viewBox="0 0 {W3} {H3}" role="img" aria-label="The potential energy of the second blade in the turning frame against its angle, at four rotor angles at 6 m/s: four bowls whose lowest points move left and right by about 17 degrees once per turn, shallower when the mother blade points up and deeper when it points down.">',
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
    f'<figcaption>Figure {{{{fig:bowl}}}}. The second blade\'s potential energy (2.3) in the frame of the mother blade, at 6 m/s ($\\Gamma = {N["Gam_6"]}$), '
    f'at four positions of the rotor. Gravity tilts the bowl, and it also makes it shallower when the mother blade points up and deeper when it points down '
    f'(its stiffness at the bottom, $A$ of (1.10), runs from $R - G$ to $R + G$: ×{math.sqrt(1 - 2/Gam6 + 1/Gam6**2):.2f} to ×{math.sqrt(1 + 2/Gam6 + 1/Gam6**2):.2f} of $R$). Its lowest point '
    f'(dots, at the four positions drawn) swings to and fro once per turn; its extremes, {N["tilt_6"]}° to either side, $\\arcsin(1/\\Gamma)$, come at $\\sin\\varphi = 1/\\Gamma$, between the positions drawn.</figcaption></figure>')

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
    f'<figcaption>Figure {{{{fig:brake}}}}. The harvested power (3.3) over its maximum (3.5), against the brake over the best brake (3.4): '
    f'$\\bar P/P^* = 2x/(1+x^2)$ with $x = \\kappa/\\kappa^*$, the same curve at every wind and for every second blade. The top is flat: a brake '
    f'{2-math.sqrt(3):.2f} times the best, or {2+math.sqrt(3):.1f} times it, still gives half the power ($x = 2 \\mp \\sqrt3$).</figcaption></figure>')

# ---- figure: turning arrows and the triangle of torques on Thales' circle (section 3.2) ------------------------------------------
W7, H7 = 380, 300
# left: two arrows turning once per turn, gravity's push and the swing 45 degrees behind it, and their shadows over one turn
cx7, cy7, r7 = 92, 140, 62
ph7 = math.radians(40); dl7 = math.radians(45); rs7 = 0.62*r7
ax = lambda a, rr: (cx7 + rr*math.cos(a), cy7 - rr*math.sin(a))
pP, pS = ax(ph7, r7), ax(ph7 - dl7, rs7)
X0, X1, Yc = 176, 366, cy7
svgT1 = [f'<svg viewBox="0 0 {W7} {H7}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="Left, a circle with two arrows from its centre: a long one for gravity\'s push and a shorter one for the swing, forty-five degrees behind it. Both turn once per turn. Their shadows on the horizontal axis are drawn on the right over one turn as two waves; the swing\'s wave peaks an eighth of a turn after the push\'s.">',
          '<defs><marker id="ah7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
          f'<circle cx="{cx7}" cy="{cy7}" r="{r7}" fill="none" stroke="#dccdb4"/><circle cx="{cx7}" cy="{cy7}" r="{rs7:.1f}" fill="none" stroke="#dccdb4" stroke-dasharray="3 3"/>',
          f'<line x1="{cx7-r7-12}" y1="{cy7}" x2="{cx7+r7+12}" y2="{cy7}" stroke="#3f2c23" stroke-width="0.8"/>',
          f'<line x1="{cx7}" y1="{cy7}" x2="{pP[0]:.1f}" y2="{pP[1]:.1f}" stroke="#b5681c" stroke-width="3" marker-end="url(#ah7)"/>',
          f'<line x1="{cx7}" y1="{cy7}" x2="{pS[0]:.1f}" y2="{pS[1]:.1f}" stroke="#7d1d2f" stroke-width="3" marker-end="url(#ah7)"/>',
          f'<line x1="{pP[0]:.1f}" y1="{pP[1]:.1f}" x2="{pP[0]:.1f}" y2="{cy7}" stroke="#b5681c" stroke-dasharray="2 3"/>',
          f'<line x1="{pS[0]:.1f}" y1="{pS[1]:.1f}" x2="{pS[0]:.1f}" y2="{cy7}" stroke="#7d1d2f" stroke-dasharray="2 3"/>',
          f'<path d="M{cx7+28*math.cos(ph7):.1f} {cy7-28*math.sin(ph7):.1f} A28 28 0 0 1 {cx7+28*math.cos(ph7-dl7):.1f} {cy7-28*math.sin(ph7-dl7):.1f}" fill="none" stroke="#3f2c23"/>',
          f'<text x="{cx7+33}" y="{cy7-12}" class="svgd" font-style="italic">δ</text>',
          f'<text x="{pP[0]-6:.1f}" y="{pP[1]-8:.1f}" text-anchor="middle" class="svgc">push</text><text x="{pS[0]+6:.1f}" y="{pS[1]+16:.1f}" class="svgc">swing</text>',
          f'<path d="M{cx7-36} {cy7+82} A40 40 0 0 0 {cx7+36} {cy7+82}" fill="none" stroke="#33627f" stroke-width="1.4" marker-end="url(#ah7)" transform="rotate(180 {cx7} {cy7+64})"/>',
          f'<text x="{cx7}" y="{cy7+100}" text-anchor="middle" class="svgc">once per turn</text>',
          f'<rect x="{X0}" y="{cy7-74}" width="{X1-X0}" height="148" fill="#fff" stroke="#3f2c23"/>',
          f'<line x1="{X0}" y1="{Yc}" x2="{X1}" y2="{Yc}" stroke="#dccdb4"/>']
ph = np.linspace(0, 2*math.pi, 181)
for amp, lag, col in ((r7, 0, '#b5681c'), (rs7, dl7, '#7d1d2f')):
    svgT1.append('<polyline points="' + ' '.join(f'{X0 + (X1-X0)*a/(2*math.pi):.1f},{Yc - amp*math.cos(a - lag):.1f}' for a in ph) + f'" fill="none" stroke="{col}" stroke-width="2"/>')
for v in (0, 90, 180, 270, 360):
    X = X0 + (X1-X0)*v/360; svgT1.append(f'<line x1="{X:.1f}" y1="{cy7+74}" x2="{X:.1f}" y2="{cy7+79}" stroke="#3f2c23"/><text x="{X:.1f}" y="{cy7+92}" text-anchor="middle" class="svgc">{v}°</text>')
svgT1.append(f'<text x="{(X0+X1)/2}" y="{cy7+108}" text-anchor="middle" class="svgd">the shadows, over one turn φ</text>')
svgT1.append(f'<text x="{(X0+X1)/2}" y="{cy7-82}" text-anchor="middle" class="svgc">the swing peaks δ after the push</text></svg>')
# right: Thales' circle. Hypotenuse = gravity's push G; the right angle sits on the circle; legs = (R-1) Theta and kappa Theta
Ox, Oy, Lh = 340, 236, 300              # the push's tail on the right, its head on the left: drawn so that the swing lags, as in the first panel
Qx = Ox - Lh
svgT2 = [f'<svg viewBox="0 0 {W7} {H7}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="A horizontal arrow for gravity\'s push with a half circle on it. Three right triangles stand on the arrow, their right-angled corners on the half circle, for a brake a third of the best, the best, and three times the best. The best one, shaded, is the tallest: its two short sides are equal and its corner is at the top of the circle.">',
         '<defs><marker id="ah7b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
         f'<path d="M{Qx} {Oy} A{Lh/2} {Lh/2} 0 0 1 {Ox} {Oy}" fill="none" stroke="#dccdb4" stroke-width="1.4"/>']
tri = [(1/3, '#33627f', 'κ = κ*/3'), (1.0, '#7d1d2f', 'κ = κ*'), (3.0, '#3c6a46', 'κ = 3κ*')]
svgT2.append(f'<polygon points="{Ox},{Oy} {Ox - Lh/2:.1f},{Oy - Lh/2:.1f} {Qx},{Oy}" fill="#f3dfdb" stroke="none"/>')        # the best triangle, shaded under all lines
for x, col, lab in tri:
    d = math.atan(x); Px, Py = Ox - Lh*math.cos(d)**2, Oy - Lh*math.cos(d)*math.sin(d)
    if x == 1.0:
        svgT2.append(f'<line x1="{Px:.1f}" y1="{Py:.1f}" x2="{Px:.1f}" y2="{Oy}" stroke="#3f2c23" stroke-dasharray="3 3"/>')
        svgT2.append(f'<text x="{Px+6:.1f}" y="{Oy-8}" class="svgc">h ∝ power</text>')
        mx, my = Ox + 0.62*(Px - Ox), Oy + 0.62*(Py - Oy); svgT2.append(f'<text x="{mx-12:.1f}" y="{my+16:.1f}" text-anchor="end" class="svgc">(R−1)Θ</text>')
        mx, my = Qx + 0.62*(Px - Qx), Oy + 0.62*(Py - Oy); svgT2.append(f'<text x="{mx+12:.1f}" y="{my+16:.1f}" class="svgc">κΘ</text>')
        sq = 9; ux_, uy_ = (Ox - Px), (Oy - Py); n1 = math.hypot(ux_, uy_); vx_, vy_ = (Qx - Px), (Oy - Py); n2 = math.hypot(vx_, vy_)
        a1 = (Px + sq*ux_/n1, Py + sq*uy_/n1); a2 = (a1[0] + sq*vx_/n2, a1[1] + sq*vy_/n2); a3 = (Px + sq*vx_/n2, Py + sq*vy_/n2)
        svgT2.append(f'<polyline points="{a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f} {a3[0]:.1f},{a3[1]:.1f}" fill="none" stroke="#3f2c23"/>')
    svgT2.append(f'<polyline points="{Ox},{Oy} {Px:.1f},{Py:.1f} {Qx},{Oy}" fill="none" stroke="{col}" stroke-width="{2.6 if x == 1.0 else 1.6}"/>')
    svgT2.append(f'<circle cx="{Px:.1f}" cy="{Py:.1f}" r="3.2" fill="{col}"/>')
for i, (x, col, lab) in enumerate(tri):
    svgT2.append(f'<line x1="16" y1="{24+i*16}" x2="32" y2="{24+i*16}" stroke="{col}" stroke-width="2.2"/><text x="36" y="{28+i*16}" class="svgc">{lab}</text>')
svgT2.append(f'<line x1="{Ox}" y1="{Oy}" x2="{Qx}" y2="{Oy}" stroke="#b5681c" stroke-width="3" marker-end="url(#ah7b)"/>')
svgT2.append(f'<text x="{(Ox+Qx)/2}" y="{Oy+22}" text-anchor="middle" class="svgd">gravity\'s push, G</text>')
svgT2.append(f'<path d="M{Ox-46} {Oy} A46 46 0 0 1 {Ox-46*math.cos(math.radians(45)):.1f} {Oy-46*math.sin(math.radians(45)):.1f}" fill="none" stroke="#3f2c23"/><text x="{Ox-52}" y="{Oy-14}" text-anchor="end" class="svgd" font-style="italic">δ</text>')
svgT2.append(f'<text x="{(Ox+Qx)/2}" y="{Oy+42}" text-anchor="middle" class="svgc">every right angle on the half circle (Thales)</text></svg>')
T['fig_torques'] = ('<figure class="fig"><div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' + ''.join(svgT1) + ''.join(svgT2) + '</div>'
    '<figcaption>Figure {{fig:torques}}. Torques as turning arrows. First panel: anything that varies once per turn, as $\\cos(\\varphi - \\delta)$, is the shadow of an arrow turning once per turn; '
    'the swing\'s arrow (wine) runs the angle $\\delta$ behind the push\'s (ochre), and so its shadow peaks $\\delta$ later. Second panel: the triangle of torques (3.2), drawn tip to tail: the push runs right to left, the stiffness side leaves its tail, the brake side ends at its head. '
    'The torque of the net stiffness, $(R-1)\\Theta$, lies along the swing; the brake\'s, $\\kappa\\Theta$, at right angles to it; together they balance gravity\'s push $G$. '
    'The right angle always sits on the half circle over $G$ (Thales), and the power is proportional to the triangle\'s height. The tallest triangle is the isosceles one: the best brake, $\\kappa^* = R - 1$, $\\delta = 45°$.</figcaption></figure>')

# ---- figure: theory against the full equation (compare.json, from the page's own engine, tools/compare.js) -------------------
cp = J('compare.json')['winds']
WCOL = {6.0: '#7d1d2f', 8.0: '#b5681c', 10.0: '#33627f'}
W1, H1 = 380, 300
PX, PY = panel(W1, H1, 50, 14, 16, 48)
lx = lambda x: math.log10(x)
svgA = [f'<svg viewBox="0 0 {W1} {H1}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="Harvested power over its small-swing maximum against the brake over the best brake, 0.05 to 20, at 6, 8 and 10 m/s: lines from formula (3.3), dots from the full equation. The dots sit on the lines except at light brakes in weak wind, where they rise above.">',
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
svgA.append(f'<line x1="{W1-114}" y1="{82}" x2="{W1-104}" y2="{82}" stroke="#3f2c23" stroke-width="1.6"/><text x="{W1-102}" y="{86}" class="svgc">formula (3.3)</text>')
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
svgB.append(f'<line x1="{W1-128}" y1="46" x2="{W1-112}" y2="46" stroke="#3f2c23" stroke-width="1.4" stroke-dasharray="5 4"/><text x="{W1-106}" y="50" class="svgc">theory (3.2)</text>')
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
    f'<figcaption>Figure {{{{fig:compare}}}}. The small-swing theory against the full equation (1.8), solved by the simulation\'s own engine. '
    f'First panel: harvested power over its maximum $P^*$ (3.5), against the brake over the best brake. The line is formula (3.3), the same for every wind; '
    f'the dots are the full equation at 6 (wine), 8 (ochre) and 10 m/s (blue). Second panel: one turn of the swing at the best brake; '
    f'solid the full equation, dashed the theory (3.2). The two have the same shape and the same phase; the full swing is shifted down by its mean trail.</figcaption></figure>')

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
    f'<figcaption>Figure {{{{fig:trail}}}}. Why the trail is the bill. The second blade trails behind the mother blade\'s line, against the rotation; the trail is drawn '
    f'{EXT} times too large (at 6 m/s it is {N["lean_deg"]}°). Flung outwards, the second blade pulls on the hinge in the direction from the hub to its '
    'centre of mass (green). The pull\'s line, through the hinge, misses the hub by a small lever arm (wine), so the pull holds the rotor back, with the torque '
    f'$\\tfrac{{ml}}{{2}}r_p\\Omega^2\\sin\\theta$; on average {N["tq_harv6"]} N m at 6 m/s. The rotor pushes against it, and that steady push is the power it pays.</figcaption></figure>')
# ---- chaos (L1_chaos_blade.json) ---------------------------------------------------------------------------------------
ch = J('L1_chaos_blade.json')
lmax = max(max(o['lyap']) for o in ch); nstart = len(ch[0]['lyap'])
regular = lmax < 1e-3
krels = sorted({o['krel'] for o in ch}, reverse=True)
rows = [f'<p class="tcap">Table 1. The largest Lyapunov exponent per turn at each wind and brake, the largest over the {nstart} starting states tried; '
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
            'the motion forgets its start as fast as a linear, damped spring forgets a nudge. That a tenth of the best brake forgets faster than the best one, and a hundredth more slowly again, is explained in section 4.1: forgetting is fastest at critical damping, and the best brake lies about five times above it. ')
T['chaos_text'] = (
    f'<div class="press"><div class="ctag">The second blade, braked</div>The full equation (1.8) at each wind, at the best brake $\\kappa^*$ of chapter 3 and at a tenth and a hundredth of it, '
    f'each from {nstart} starts: the second blade at rest on the mother blade\'s line and {nstart - 1} at random '
    'angles and rates, some tumbling right over at first. The exponent comes from two copies $10^{-8}$ apart, rescaled every quarter turn.\n' + '\n'.join(rows) + '\n' + verdict +
    f'Halving the step changes the exponents by at most {f(step_gap*100, 1)} % of their size.</div>')
N['chaos_regular'] = 'regular' if regular else 'chaotic in part'

# ---- power theorem Monte Carlo (the general theorem, run on a bob and a double pendulum) --------------------------------
log = (D / 'mc_full.log').read_text()
ratios = [abs(float(x) - 1)*100 for x in re.findall(r'ratio ([0-9.]+) \+-', log)]
N['mc_dev_max'] = f(max(ratios[1::2]), 2); N['mc_dev_min'] = f(min(ratios[1::2]), 2)
se = [float(x) for x in re.findall(r'ratio [0-9.]+ \+- ([0-9.]+)', log)][1::2]
N['mc_se_min'] = f(min(se)*100, 1); N['mc_se_max'] = f(max(se)*100, 1)
meff = re.findall(r'<m_eff>/M = ([0-9.]+)', log)
N['meff_single_large'] = f(float(meff[3]), 2); N['meff_double_chaos'] = f(float(meff[7]), 2)
N['meff_gentle_min'] = f(min(float(meff[k]) for k in (0, 1, 4, 5)), 2)          # the gentle runs of the bob and the double pendulum

# ---- gusts (L2) ---------------------------------------------------------------------------------------------------------
s_om = J('L2_scales.json')['sigOm']
N['sigOm'] = f(s_om*100, 1); N['jensen'] = f(s_om**2/2*100, 2)
_sk2 = J('L2_scales.json')['sigOm_k2']; N['sigOm_k2'] = f(_sk2*100, 1); N['jensen_k2'] = f(_sk2**2/2*100, 2)   # the same records under the pure square law
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
        'and load the formula (5.6)–(5.7) finds best. Swing amplitude and load are given as formula / full: the describing-function formula, and the '
        'full equation (5.8), whose amplitude is half its peak-to-peak swing (its mean, the trail of section 4.2, is left out). Paid: what the rotor pays; the last two columns are the shares of it that reach the load and that friction takes.</p>'
        '<table class="mt"><thead><tr><th>wind</th><th>$R_L$, Ω</th><th>amplitude, rad</th>'
        '<th>load, mW</th><th>paid, mW</th><th>load</th><th>friction</th></tr></thead><tbody>']
for v in WINDS:
    a, b = gen[v], full[v]
    rows.append(f'<tr><td>{v:.0f} m/s</td><td>{a["R_load"]:.2f}</td>'
                f'<td>{a["Theta"]:.3f} / {b["Theta_amp"]:.3f}</td><td>{a["P_load"]*1e3:.1f} / {b["P_load"]*1e3:.1f}</td><td>{b["P_paid"]*1e3:.1f}</td>'
                f'<td>{b["P_load"]/b["P_paid"]*100:.0f} %</td><td>{b["P_fric"]/b["P_paid"]*100:.0f} %</td></tr>')
rows.append('</tbody></table>')
T['generator'] = '\n'.join(rows)
need = J('sensor.json')['need_uW']*1e-6
loads = [full[v]['P_load'] for v in WINDS]
N['g4_min'] = f(min(loads)*1e3, 0); N['g4_max'] = f(max(loads)*1e3, 0)
_eff = [(gen[v]['kappa_e']/gen[v]['eta'] + 4*gen[v]['f']/(math.pi*gen[v]['Theta']))/(gen[v]['R'] - 1 - gen[v]['j']) for v in WINDS]   # against the best brake with the motor's inertia, R - 1 - j
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
# figure: where the rotor's payment goes, from the full equation (5.8) at each wind's best ratio and load. The coil and the load carry the
# same current, so the coil takes the load's power times R_c/R_L; the gearhead takes what is left (the energy book of the run closes).
flow = {}
for v in WINDS:
    b = full[v]; coil = b['P_load']*RC/b['R_load']
    flow[v] = {'load': b['P_load'], 'coil': coil, 'friction': b['P_fric'], 'gears': b['P_paid'] - b['P_load'] - coil - b['P_fric'], 'paid': b['P_paid']}
    assert flow[v]['gears'] > 0
N['g4_coil_lo'] = f(min(flow[v]['coil']/flow[v]['paid'] for v in WINDS)*100, 0); N['g4_coil_hi'] = f(max(flow[v]['coil']/flow[v]['paid'] for v in WINDS)*100, 0)
N['g4_gear_lo'] = f(min(flow[v]['gears']/flow[v]['paid'] for v in WINDS)*100, 0); N['g4_gear_hi'] = f(max(flow[v]['gears']/flow[v]['paid'] for v in WINDS)*100, 0)
FW, FH, fl, fr_ = 560, 230, 70, 64
pmax = max(flow[v]['paid'] for v in WINDS)*1e3
FX = lambda mw: fl + mw/pmax*(FW - fl - fr_)
cols = [('load', '#3c6a46', 'load'), ('coil', '#33627f', 'coil'), ('friction', '#b5681c', 'friction'), ('gears', '#8b8079', 'gearhead')]
svgf = [f'<svg viewBox="0 0 {FW} {FH}" role="img" aria-label="Where the power the rotor pays goes, at 6, 8 and 10 metres per second, as three stacked horizontal bars in milliwatts: the load, the coil, the motor\'s friction and the gearhead. The gearhead and the load take the largest shares, the coil the smallest.">']
for i, v in enumerate(WINDS):
    y0 = 24 + i*52; x = fl
    svgf.append(f'<text x="{fl-8}" y="{y0+21}" text-anchor="end" class="svgc">{v:.0f} m/s</text>')
    for k, c, lab in cols:
        w_ = FX(flow[v][k]*1e3) - fl
        svgf.append(f'<rect x="{x:.1f}" y="{y0}" width="{w_:.1f}" height="30" fill="{c}"/>')
        if w_ > 34:
            svgf.append(f'<text x="{x + w_/2:.1f}" y="{y0+19}" text-anchor="middle" class="svgc" style="fill:#fff">{flow[v][k]*1e3:.0f}</text>')
        x += w_
    svgf.append(f'<text x="{x+4:.1f}" y="{y0+19}" class="svgc">{flow[v]["paid"]*1e3:.0f} mW</text>')
for j, (k, c, lab) in enumerate(cols):
    svgf.append(f'<rect x="{fl + j*110}" y="{FH-34}" width="12" height="12" fill="{c}"/><text x="{fl + j*110 + 17}" y="{FH-24}" class="svgc">{lab}</text>')
svgf.append('</svg>')
T['fig_flow'] = ('<figure class="fig">' + ''.join(svgf) +
    f'<figcaption>Figure {{{{fig:flow}}}}. Where the rotor\'s payment goes, in mW, through the RE 25 and the GP 32 C at 492 : 1, from the full equation (5.8) at each wind\'s best load. '
    f'The load gets {N["g4_eff_min"]} to {N["g4_eff_max"]} %, the coil {N["g4_coil_lo"]} to {N["g4_coil_hi"]} % (the same current flows through both, so the coil takes the load\'s power times $R_c/R_L$), '
    f'the motor\'s friction {N["g4_fric_min"]} to {N["g4_fric_max"]} %, and the gearhead the rest, ' + (f'{N["g4_gear_lo"]} %' if N['g4_gear_lo'] == N['g4_gear_hi'] else f'{N["g4_gear_lo"]} to {N["g4_gear_hi"]} %') + ' at every wind.</figcaption></figure>')
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
        '$ml/2$; the best power $P^*$ (3.5) at 6 and 10 m/s; the generator torque $\\tau^* = \\tfrac{ml}{2}g/\\sqrt2$ it must hold; the extra '
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
N['kgm_1m_in'] = f(mo['kg_per_m_1m_in'], 0); N['tip_kgm'] = f(mo['tip_kg_per_m'], 1); N['outer3_kg'] = f(mo['outer3_kg'], 0); N['outer3_pull'] = f(mo['outer3_pull10_N']/1e3, 1)

# ---- chapter 1: the double pendulum free and held (L0_double.json, tools/double_pendulum.js on the site's Fig. 2 engine) ------
dp = J('L0_double.json')
fr = dp['free']
N['invGam_min'] = f(g/(Om[10.0]**2*rp), 2)
N['dp_free_T'] = f'{fr["T"]:.0f}'; N['dp_free_drift'] = sci(fr['energy_drift_J'], 0)
N['dp_free_settle'] = f(max(abs(x - fr['lyap_per_s']) for t_, x in fr['running'] if t_ >= fr['T']/2), 2)      # how much the estimate moves over the last half of the run
N['dp_free_lyap'] = f(fr['lyap_per_s'], 2); N['dp_free_efold'] = f(1/fr['lyap_per_s'], 2)
tw = fr['twin_1e9']
N['dp_free_1m'] = f(next(t for t, sp in zip(tw['t'], tw['sep']) if sp >= 1.0), 0)
rod = dp['driven']['rod_63m']['sweep']; thr = dp['driven']['threshold']
reg = [x for r in rod if r['Gamma'] >= 3.3 for x in r['lyap'] if x < thr] + [x for r in dp['turbine'] for x in r['unbraked'] if x < thr]
N['dp_rod_reg_max'] = f(max(reg), 3)
bm = [max(o['lyap']) for o in J('L1_chaos_blade.json') if o['krel'] == 1.0]          # the braked exponents of Table 1 (Radau IIA); tools/double_pendulum.js agrees by RK4
N['dp_braked_lo'] = f(min(bm), 2); N['dp_braked_hi'] = f(max(bm), 2)
N['dp_red_gap'] = sci(dp['reduction']['worst_energy_gap_J'], 0)
eqa = dp['driven']['equal_arms']['sweep']
W2, H2 = 380, 300
# left: the free pendulum's twins drift apart
PXa, PYa = panel(W2, H2, 54, 14, 16, 48)
svgL = [f'<svg viewBox="0 0 {W2} {H2}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="The free double pendulum of the site\'s Fig. 2: the distance between the lower bobs of two copies, started 0.000000001 and 0.001 radian apart, against time over 30 seconds on a logarithmic axis. Both rise along a straight line until they reach about a metre, then stay there.">',
        f'<rect x="54" y="16" width="{W2-68}" height="{H2-64}" fill="#fff" stroke="#3f2c23"/>']
for e in (-9, -6, -3, 0):
    Yv = PYa(e, -10, 1); svgL.append(f'<line x1="49" y1="{Yv:.1f}" x2="54" y2="{Yv:.1f}" stroke="#3f2c23"/><text x="45" y="{Yv+4:.1f}" text-anchor="end" class="svgc">1e{e}</text>')
for tt in (0, 10, 20, 30):
    Xv = PXa(tt, 0, 30); svgL.append(f'<line x1="{Xv:.1f}" y1="{H2-48}" x2="{Xv:.1f}" y2="{H2-43}" stroke="#3f2c23"/><text x="{Xv:.1f}" y="{H2-30}" text-anchor="middle" class="svgc">{tt} s</text>')
for key, col in (('twin_1e9', '#7d1d2f'), ('twin_1e3', '#b5681c')):
    tw = fr[key]
    pts = ' '.join(f'{PXa(t, 0, 30):.1f},{PYa(math.log10(max(sp, 1e-10)), -10, 1):.1f}' for t, sp in zip(tw['t'], tw['sep']))
    svgL.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.6"/>')
lam = fr['lyap_per_s']; t0 = 2.0; s0 = next(sp for t, sp in zip(fr['twin_1e9']['t'], fr['twin_1e9']['sep']) if t >= t0)
dT = 8.0
svgL.append(f'<line x1="{PXa(t0, 0, 30):.1f}" y1="{PYa(math.log10(s0) + 1, -10, 1):.1f}" x2="{PXa(t0 + dT, 0, 30):.1f}" y2="{PYa(math.log10(s0) + 1 + lam*dT/math.log(10), -10, 1):.1f}" stroke="#3f2c23" stroke-dasharray="4 3"/>')
svgL.append(f'<line x1="{W2-170}" y1="{H2-112}" x2="{W2-158}" y2="{H2-112}" stroke="#7d1d2f" stroke-width="2"/><text x="{W2-154}" y="{H2-108}" class="svgc">started 10⁻⁹ rad apart</text>')
svgL.append(f'<line x1="{W2-170}" y1="{H2-96}" x2="{W2-158}" y2="{H2-96}" stroke="#b5681c" stroke-width="2"/><text x="{W2-154}" y="{H2-92}" class="svgc">started 10⁻³ rad apart</text>')
svgL.append(f'<line x1="{W2-170}" y1="{H2-80}" x2="{W2-158}" y2="{H2-80}" stroke="#3f2c23" stroke-dasharray="4 3"/><text x="{W2-154}" y="{H2-76}" class="svgc">slope Λ = {N["dp_free_lyap"]} /s</text>')
svgL.append(f'<text x="{(54+W2-14)/2}" y="{H2-10}" text-anchor="middle" class="svgd">time, free double pendulum</text>')
svgL.append(f'<text x="14" y="{(16+H2-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 14 {(16+H2-48)/2})">distance between the lower bobs, m</text></svg>')
# right: how many of nine starts end chaotic, the first arm held
PXb, PYb = panel(W2, H2, 44, 14, 16, 48)
gx = lambda G_: math.log10(G_)
svgR = [f'<svg viewBox="0 0 {W2} {H2}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="The first arm held to a steady turning: how many of nine starts end chaotic, against the outward pull at the hinge in units of gravity from 0.1 to 30. Equal arms: between one and six at every value. A 1 m rod on a 63 m arm: nine of nine near 1, falling to two of nine, the two starts near the inverted position, from about 3.3 up. With the best brake, none, at the turbine\'s three winds.">',
        f'<rect x="44" y="16" width="{W2-58}" height="{H2-64}" fill="#fff" stroke="#3f2c23"/>']
xa, xb = gx(0.1), gx(31.62)
svgR.append(f'<rect x="{PXb(gx(dp["turbine"][0]["Gamma"]), xa, xb):.1f}" y="16" width="{PXb(gx(dp["turbine"][2]["Gamma"]), xa, xb) - PXb(gx(dp["turbine"][0]["Gamma"]), xa, xb):.1f}" height="{H2-64}" fill="#f3dfdb"/>')
svgR.append(f'<text x="{(PXb(gx(dp["turbine"][0]["Gamma"]), xa, xb) + PXb(gx(dp["turbine"][2]["Gamma"]), xa, xb))/2:.1f}" y="30" text-anchor="middle" class="svgc">turbine, 6–10 m/s</text>')
for v_, lab in ((0.1, '0.1'), (1, '1'), (10, '10'), (30, '30')):
    Xv = PXb(gx(v_), xa, xb); svgR.append(f'<line x1="{Xv:.1f}" y1="{H2-48}" x2="{Xv:.1f}" y2="{H2-43}" stroke="#3f2c23"/><text x="{Xv:.1f}" y="{H2-30}" text-anchor="middle" class="svgc">{lab}</text>')
for v_ in (0, 3, 6, 9):
    Yv = PYb(v_, -0.4, 9.6); svgR.append(f'<line x1="39" y1="{Yv:.1f}" x2="44" y2="{Yv:.1f}" stroke="#3f2c23"/><text x="35" y="{Yv+4:.1f}" text-anchor="end" class="svgc">{v_}</text>')
for sweep, col in ((eqa, '#b5681c'), (rod, '#7d1d2f')):
    pts = ' '.join(f'{PXb(gx(r["Gamma"]), xa, xb):.1f},{PYb(r["n_chaotic"], -0.4, 9.6):.1f}' for r in sweep)
    svgR.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.6"/>')
    svgR += [f'<circle cx="{PXb(gx(r["Gamma"]), xa, xb):.1f}" cy="{PYb(r["n_chaotic"], -0.4, 9.6):.1f}" r="2.6" fill="{col}"/>' for r in sweep]
for r in dp['turbine']:
    nb_ = sum(1 for x in [r['braked_max']] if x > thr)
    svgR.append(f'<rect x="{PXb(gx(r["Gamma"]), xa, xb)-3.5:.1f}" y="{PYb(nb_, -0.4, 9.6)-3.5:.1f}" width="7" height="7" fill="#3c6a46"/>')
svgR.append(f'<line x1="52" y1="40" x2="64" y2="40" stroke="#b5681c" stroke-width="2"/><text x="68" y="44" class="svgc">equal arms, no brake</text>')
svgR.append(f'<line x1="52" y1="56" x2="64" y2="56" stroke="#7d1d2f" stroke-width="2"/><text x="68" y="60" class="svgc">1 m rod at 63 m, no brake</text>')
svgR.append(f'<rect x="54.5" y="68.5" width="7" height="7" fill="#3c6a46"/><text x="68" y="76" class="svgc">the same, best brake</text>')
svgR.append(f'<text x="{(44+W2-14)/2}" y="{H2-10}" text-anchor="middle" class="svgd">outward pull over gravity, Γ = Ω²r/g</text>')
svgR.append(f'<text x="12" y="{(16+H2-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 12 {(16+H2-48)/2})">chaotic starts, of 9</text></svg>')
_g6 = dp['turbine'][0]['Gamma']                                   # the 6 m/s run; the sweep's grid points on either side of it
_sw_lo = max((x for x in rod if x['Gamma'] < _g6), key=lambda x: x['Gamma']); _sw_hi = min((x for x in rod if x['Gamma'] > _g6), key=lambda x: x['Gamma'])
T['fig_double'] = ('<figure class="fig"><div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' + ''.join(svgL) + ''.join(svgR) + '</div>'
    f'<figcaption>Figure {{{{fig:double}}}}. The double pendulum, free and held. Left: the site\'s own double pendulum (Fig. 2 of the simulations, its code run unchanged), '
    f'two copies started $10^{{-9}}$ and $10^{{-3}}$ rad apart from 120° and 150°; their lower bobs drift apart as $e^{{\\Lambda t}}$ with $\\Lambda$ = {N["dp_free_lyap"]} per second, until they are as far apart as the pendulum allows. '
    f'Right: the first arm held to a steady turning, with $\\Gamma$ the outward pull at its end in units of gravity; of nine starts spread over angle and rate, how many end chaotic (a largest Lyapunov exponent above {thr} per turn over 400 turns). '
    f'Equal arms sit at resonance, $R = 1$, and stay chaotic from some starts at every $\\Gamma$. The second blade of these notes, $R$ = {N["R"]}, keeps only the two starts near the top of its spring\'s hill from the turbine\'s lightest wind up ($\\Gamma$ = {N["Gam_6"]} at 6 m/s, where the run at the turbine\'s own settings finds two; the sweep\'s nearest points, {_sw_lo["Gamma"]:.2f} and {_sw_hi["Gamma"]:.2f}, find {_sw_lo["n_chaotic"]} and {_sw_hi["n_chaotic"]}), '
    'and with the best brake (squares, at the turbine\'s three winds) none at all.</figcaption></figure>')

# ---- chapter 1, section 1.5: the moving hilltop, and once-per-turn snapshots (L0_double.json 'poincare', tools/double_pendulum.js) -----
ps = dp['poincare']; pr = ps['rod']; pe = ps['equal']
R6, G6, thb6, A06 = pr['R'], pr['G'], pr['theta_b'], pr['A0']
EU = I*Om[6.0]**2                                        # the energy unit of (1.8) at 6 m/s, I Omega^2, J
N['ps_EU'] = f(EU, 3)
N['ps_A_lo'] = f(R6 - G6, 1); N['ps_A_hi'] = f(R6 + G6, 1); N['ps_A0'] = f(A06, 1)
N['ps_hill_lo'] = f(2*(R6 - G6)*EU, 1); N['ps_hill_hi'] = f(2*(R6 + G6)*EU, 1)             # barrier 2A I Omega^2, J
N['ps_geff_lo'] = f(Om[6.0]**2*rp - g, 1); N['ps_geff_hi'] = f(Om[6.0]**2*rp + g, 1)       # the apparent gravity at the hinge, m/s^2
N['ps_w_lo'] = f(math.sqrt(R6 - G6), 2); N['ps_w_hi'] = f(math.sqrt(R6 + G6), 2)           # small-swing rate per turn in the deepest and shallowest bowl
N['ps_thb_deg'] = f(math.degrees(thb6), 1)
N['ps_Jin'] = f(pr['pred']['J_in'], 1); N['ps_Jout'] = f(pr['pred']['J_out'], 1)
N['ps_Jsep_lo'] = f(8*math.sqrt(R6 - G6)/math.pi, 1); N['ps_Jsep_hi'] = f(8*math.sqrt(R6 + G6)/math.pi, 1)
N['ps_amp_pred'] = f(math.degrees(pr['pred']['amp_in']), 0)
amp_r = [x - thb6 for x in pr['meas']['right']]; amp_l = [thb6 - x for x in pr['meas']['left']]
N['ps_amp_meas_lo'] = f(math.degrees(min(sum(amp_r)/2, sum(amp_l)/2)), 0); N['ps_amp_meas_hi'] = f(math.degrees(max(sum(amp_r)/2, sum(amp_l)/2)), 0)
N['ps_win_pred'] = f(pr['pred']['w_in'], 1); N['ps_wout_pred'] = f(pr['pred']['w_out'], 1)
N['ps_win_meas'] = f((sum(pr['meas']['w_in_up']) - sum(pr['meas']['w_in_down']))/4, 1)
N['ps_wout_meas_lo'] = f(min(sum(pr['meas']['w_out_up'])/2, -sum(pr['meas']['w_out_down'])/2), 1)
N['ps_wout_meas_hi'] = f(max(sum(pr['meas']['w_out_up'])/2, -sum(pr['meas']['w_out_down'])/2), 1)
N['ps_win_rads'] = f(pr['pred']['w_in']*Om[6.0], 1); N['ps_wout_rads'] = f(pr['pred']['w_out']*Om[6.0], 1)
N['ps_turn6'] = f(2*math.pi/Om[6.0], 2)
lyc = [o['lyap'] for o in pr['orbits'] if o['lyap'] > pr['meas']['threshold']]
lyr = [o['lyap'] for o in pr['orbits'] if o['lyap'] <= pr['meas']['threshold']]
N['ps_lyap_ch_lo'] = f(min(lyc), 2); N['ps_lyap_ch_hi'] = f(max(lyc), 2); N['ps_lyap_reg_max'] = f(max(lyr), 2)
N['ps_lyap_eq'] = f(pe['orbits'][0]['lyap'], 2)
N['ps_period_3'] = f(next(T_ for a, T_ in pr['period_turns'] if a == 3), 2)                # a swing of 3 rad lasts this many turns
N['ps_thr'] = f(pr['meas']['threshold'], 1)
N['dp_gain_1000'] = f(math.log(1000)/fr['lyap_per_s'], 1)                                  # what a thousand times better start buys, s
N['dp_horizon'] = f(math.log(1/1e-9)/fr['lyap_per_s'], 1)
N['dp_free_double'] = f(math.log(2)/fr['lyap_per_s'], 2)

# figure: the landscape (1.10) over the whole circle at four rotor angles, in joules at 6 m/s
W5, H5 = 560, 300
LX, LY = panel(W5, H5, 58, 150, 16, 48)
tl = np.linspace(-math.pi, math.pi, 361)
ulo, uhi = -24.0, 24.0
svg5 = [f'<svg viewBox="0 0 {W5} {H5}" role="img" aria-label="The potential energy of the second blade over the whole circle at 6 metres per second, at four positions of the rotor: a bowl near zero degrees and a hill near one hundred and eighty degrees. The hill\'s top is highest when the mother blade points down and lowest when it points up; a shaded band marks the range of hilltop heights over a turn.">',
        f'<rect x="58" y="16" width="{W5-208}" height="{H5-64}" fill="#fff" stroke="#3f2c23"/>',
        f'<rect x="58" y="{LY((R6 + G6)*EU, ulo, uhi):.1f}" width="{W5-208}" height="{LY((R6 - G6)*EU, ulo, uhi) - LY((R6 + G6)*EU, ulo, uhi):.1f}" fill="#f3dfdb"/>']
for v in (-180, -90, 0, 90, 180):
    X = LX(math.radians(v), -math.pi, math.pi); svg5.append(f'<line x1="{X:.1f}" y1="{H5-48}" x2="{X:.1f}" y2="{H5-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{H5-30}" text-anchor="middle" class="svgc">{v}°</text>')
for v in (-20, -10, 0, 10, 20):
    Y = LY(v, ulo, uhi); svg5.append(f'<line x1="53" y1="{Y:.1f}" x2="58" y2="{Y:.1f}" stroke="#3f2c23"/><text x="49" y="{Y+4:.1f}" text-anchor="end" class="svgc">{v}</text>')
for c, phd, lab in bowl_cols:
    ph = math.radians(phd); A = math.sqrt(R6*R6 - 2*R6*G6*math.sin(ph) + G6*G6); tb = math.atan2(-G6*math.cos(ph), R6 - G6*math.sin(ph))
    uu = EU*(-R6*np.cos(tl) + G6*np.sin(ph + tl))
    svg5.append('<polyline points="' + ' '.join(f'{LX(t, -math.pi, math.pi):.1f},{LY(v, ulo, uhi):.1f}' for t, v in zip(tl, uu)) + f'" fill="none" stroke="{c}" stroke-width="2"/>')
    ttop = math.atan2(math.sin(tb + math.pi), math.cos(tb + math.pi))
    svg5.append(f'<circle cx="{LX(ttop, -math.pi, math.pi):.1f}" cy="{LY(A*EU, ulo, uhi):.1f}" r="4.5" fill="{c}" stroke="#fff" stroke-width="1.2"/>')
for i, (c, phd, lab) in enumerate(bowl_cols):
    svg5.append(f'<line x1="{W5-142}" y1="{40+i*20}" x2="{W5-124}" y2="{40+i*20}" stroke="{c}" stroke-width="2.4"/><text x="{W5-118}" y="{44+i*20}" class="svgc">{lab}</text>')
svg5.append(f'<rect x="{W5-142}" y="{128}" width="18" height="10" fill="#f3dfdb"/><text x="{W5-118}" y="{137}" class="svgc">hilltop heights</text><text x="{W5-118}" y="{151}" class="svgc">over a turn</text>')
svg5.append(f'<text x="{(58+W5-150)/2}" y="{H5-10}" text-anchor="middle" class="svgd">angle θ of the second blade from the mother blade\'s line</text>')
svg5.append(f'<text x="16" y="{(16+H5-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 16 {(16+H5-48)/2})">potential energy U, J</text></svg>')
T['fig_hill'] = ('<figure class="fig">' + ''.join(svg5) +
    f'<figcaption>Figure {{{{fig:hill}}}}. The landscape (1.10) of the second blade at 6 m/s, drawn in joules, $U = I\\Omega^2u$ (chapter 2 meets it again as (2.3)), over the whole circle, at four positions of the rotor. A bowl at the mother blade\'s line '
    f'and a hill on the far side, where the second blade points back at the hub. The hill is lowest, {N["ps_hill_lo"]} J above the bowl\'s bottom, when the mother blade points up, '
    f'and highest, {N["ps_hill_hi"]} J, when it points down; the shaded band is the range of its top over a turn. The second blade\'s energy unit here is $I\\Omega^2$ = {N["ps_EU"]} J.</figcaption></figure>')

# figure: the snapshots, equal arms against the rod of the notes
def dots(orbits, X, Y, x0, x1, y0, y1, every, n):
    d = []
    for o in orbits:
        for th, w in o['pts'][:n:every]:
            if y0 <= w <= y1:
                d.append(f'M{X(th, x0, x1):.0f} {Y(w, y0, y1):.0f}h0')          # whole units of the 380-wide frame: a dot is 1.7 wide
    return ''.join(d)
W6, H6 = 380, 320
def snap_panel(pp, wlim, label, extra, nreg, nch):
    PXs, PYs = panel(W6, H6, 46, 12, 16, 48)
    reg = [o for o in pp['orbits'] if o['lyap'] <= pr['meas']['threshold']]; cha = [o for o in pp['orbits'] if o['lyap'] > pr['meas']['threshold']]
    s = [f'<svg viewBox="0 0 {W6} {H6}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="{label}">',
         f'<rect x="46" y="16" width="{W6-58}" height="{H6-64}" fill="#fff" stroke="#3f2c23"/>']
    for v in (-180, -90, 0, 90, 180):
        X = PXs(math.radians(v), -math.pi, math.pi); s.append(f'<line x1="{X:.1f}" y1="{H6-48}" x2="{X:.1f}" y2="{H6-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{H6-30}" text-anchor="middle" class="svgc">{v}°</text>')
    for v in wlim[2]:
        Y = PYs(v, wlim[0], wlim[1]); s.append(f'<line x1="41" y1="{Y:.1f}" x2="46" y2="{Y:.1f}" stroke="#3f2c23"/><text x="37" y="{Y+4:.1f}" text-anchor="end" class="svgc">{v:g}</text>')
    s.append(f'<path d="{dots(cha, PXs, PYs, -math.pi, math.pi, wlim[0], wlim[1], 1, nch)}" stroke="#7d1d2f" stroke-width="1.7" stroke-linecap="round" fill="none"/>')
    s.append(f'<path d="{dots(reg, PXs, PYs, -math.pi, math.pi, wlim[0], wlim[1], 1, nreg)}" stroke="#23160f" stroke-width="1.5" stroke-linecap="round" fill="none"/>')
    s += extra(PXs, PYs)
    s.append(f'<text x="{(46+W6-12)/2}" y="{H6-10}" text-anchor="middle" class="svgd">angle θ, once per turn</text>')
    s.append(f'<text x="12" y="{(16+H6-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 12 {(16+H6-48)/2})">rate θ′ = dθ/dφ</text></svg>')
    return s
def no_extra(PXs, PYs): return []
wl_eq = (-3.6, 3.6, (-3, -2, -1, 0, 1, 2, 3))
svgE = snap_panel(pe, wl_eq, 'Once-per-turn snapshots of the equal-armed double pendulum with its first arm held, at an outward pull four times gravity: one chaotic orbit fills most of the plane with scattered dots; a few closed curves form an island near 60 degrees, and smooth bands at the top and bottom are tumbling motions.', no_extra, 120, 2000)
wl_rod = (-32, 32, (-30, -20, -10, 0, 10, 20, 30))
def rod_extra(PXs, PYs):
    a = pr['pred']['amp_in']; E = pr['pred']['E_out']; e = []
    th = np.linspace(thb6 - a, thb6 + a, 241); w = np.sqrt(np.maximum(0, 2*A06*(np.cos(th - thb6) - math.cos(a))))
    for sg in (1, -1):
        e.append('<polyline points="' + ' '.join(f'{PXs(t, -math.pi, math.pi):.1f},{PYs(sg*v, -32, 32):.1f}' for t, v in zip(th, w)) + '" fill="none" stroke="#b5681c" stroke-width="1.8" stroke-dasharray="5 3"/>')
    th = np.linspace(-math.pi, math.pi, 241); w = np.sqrt(2*(E + A06*np.cos(th - thb6)))
    for sg in (1, -1):
        e.append('<polyline points="' + ' '.join(f'{PXs(t, -math.pi, math.pi):.1f},{PYs(sg*v, -32, 32):.1f}' for t, v in zip(th, w)) + '" fill="none" stroke="#b5681c" stroke-width="1.8" stroke-dasharray="5 3"/>')
    e.append(f'<line x1="{W6-150}" y1="28" x2="{W6-132}" y2="28" stroke="#b5681c" stroke-width="1.8" stroke-dasharray="5 3"/><text x="{W6-128}" y="32" class="svgc">band (1.12)</text>')
    return e
svgP = snap_panel(pr, wl_rod, 'Once-per-turn snapshots of the second blade of these notes at 6 metres per second, no brake: nested closed rings fill the bowl around a point near minus 17 degrees; a thin ring of scattered dots surrounds them where the swing nearly reaches the hilltop; smooth bands above and below are tumbling motions. Dashed curves mark the estimated edges of the chaotic band, which hug it.', rod_extra, 120, 1000)
legend = (f'<div style="display:flex;gap:18px;justify-content:center;flex-wrap:wrap;font:11px var(--f-mono);color:var(--muted)">'
          '<span><span style="color:#23160f">●</span> regular orbits</span><span><span style="color:#7d1d2f">●</span> chaotic orbits</span></div>')
T['fig_snap'] = ('<figure class="fig"><div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' + ''.join(svgE) + ''.join(svgP) + '</div>' + legend +
    f'<figcaption>Figure {{{{fig:snap}}}}. Snapshots taken once per turn, each time the mother blade passes the horizontal rising, of the held pendulum with no brake (a Poincaré section). Wine: orbits whose largest Lyapunov exponent exceeds {N["ps_thr"]} per turn; ink: the rest, all below {N["ps_lyap_reg_max"]}. '
    f'First panel: equal arms, $R = 1$, at $\\Gamma = 4$. One orbit (wine, 2000 of its {len(pe["orbits"][0]["pts"])} turns drawn) wanders over most of the plane; its Lyapunov exponent is {N["ps_lyap_eq"]} per turn. Only an island of closed curves and the fast tumbling motions are regular. '
    f'Second panel: the 1 m rod at the 63 m tip at 6 m/s, $R$ = {N["R"]}, $\\Gamma$ = {N["Gam_6"]}. Every swing in the bowl draws a closed ring; only a thin band, where the swing almost reaches the hilltop, is chaotic, '
    f'with exponents {N["ps_lyap_ch_lo"]} to {N["ps_lyap_ch_hi"]} per turn. The dashed curves are the edges of that band as estimate (1.12) puts them, drawn with nothing fitted.</figcaption></figure>')

# ---- chapter 6: the turbulent field (L6_wind.json, notes/rotor-pendula/derive/L6_wind.py) -------------------------------------
wf = J('L6_wind.json'); wc = J('wind_check.json')
U8 = 8.0
N['shear_bot'] = f(U8*(27/90)**0.2, 1); N['shear_top'] = f(U8*(153/90)**0.2, 1)
N['wf_sig_u'] = f(wf['sigma_u'], 2); N['wf_fcorner'] = f(U8/(6*wf['L'][0]), 4)
fh = (0.5**-1.5 - 1)*U8/(6*wf['L'][0])                  # the integral of (6.6) from 0 to f is sigma^2 [1 - (1 + 6 f L/U)^(-2/3)]
N['wf_fhalf'] = f(fh, 4); N['wf_thalf'] = f(round(1/fh, -1), 0)
SK_ = lambda fq: 4*wf['L'][0]/U8/(1 + 6*fq*wf['L'][0]/U8)**(5/3)
N['wf_band_pct'] = f(100*sum(SK_(k/256)/256 for k in range(1, 256)), 0)
# figure: the spectrum of u at the hub, 8 m/s class A: the Kaimal model (6.6), the same scaled over the kept band (what the synthesis aims
# at), and the forty records' periodogram averaged in log bands (L6_wind.json 'u_spectrum')
band = sum(SK_(k/256)/256 for k in range(1, 256))                 # share of sigma^2 between 1/256 and 1 Hz (the record's band)
sig2 = wf['sigma_u']**2
SW, SH = 560, 320
SX, SY = panel(SW, SH, 64, 18, 16, 48)
lfx = lambda fq: math.log10(fq); lsy = lambda y: math.log10(y)
fx0, fx1, sy0, sy1 = math.log10(0.003), math.log10(1.0), math.log10(0.1), math.log10(1000)
svgS = [f'<svg viewBox="0 0 {SW} {SH}" role="img" aria-label="The spectrum of the wind along the shaft at the hub, 8 metres per second, turbulence class A, on logarithmic axes from 0.003 to 1 hertz: flat at low frequency, then falling as f to the minus five thirds above about 0.004 hertz. The Kaimal model, the model scaled over the record\'s band, and the dots measured from forty synthesised records, which lie on the scaled line.">',
        f'<rect x="64" y="16" width="{SW-82}" height="{SH-64}" fill="#fff" stroke="#3f2c23"/>']
for fq, lab in ((0.003, '0.003'), (0.01, '0.01'), (0.03, '0.03'), (0.1, '0.1'), (0.3, '0.3'), (1.0, '1')):
    X = SX(lfx(fq), fx0, fx1); svgS.append(f'<line x1="{X:.1f}" y1="{SH-48}" x2="{X:.1f}" y2="{SH-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{SH-30}" text-anchor="middle" class="svgc">{lab}</text>')
for yv in (0.1, 1, 10, 100, 1000):
    Y = SY(lsy(yv), sy0, sy1); svgS.append(f'<line x1="59" y1="{Y:.1f}" x2="64" y2="{Y:.1f}" stroke="#3f2c23"/><text x="55" y="{Y+4:.1f}" text-anchor="end" class="svgc">{yv:g}</text>')
fqs = np.logspace(math.log10(0.003), 0, 160)
kai = [sig2*SK_(q) for q in fqs]
kai_in = [(q, v) for q, v in zip(fqs, kai) if v >= 0.1]                  # inside the frame
svgS.append('<polyline points="' + ' '.join(f'{SX(lfx(q), fx0, fx1):.1f},{SY(lsy(v), sy0, sy1):.1f}' for q, v in kai_in) + '" fill="none" stroke="#3f2c23" stroke-width="1.4" stroke-dasharray="5 4"/>')
inb = [(q, v/band) for q, v in zip(fqs, kai) if q >= 1/256 and v/band >= 0.1]
svgS.append('<polyline points="' + ' '.join(f'{SX(lfx(q), fx0, fx1):.1f},{SY(lsy(v), sy0, sy1):.1f}' for q, v in inb) + '" fill="none" stroke="#33627f" stroke-width="2.2"/>')
for q, v in wf['u_spectrum']:
    svgS.append(f'<circle cx="{SX(lfx(q), fx0, fx1):.1f}" cy="{SY(lsy(v), sy0, sy1):.1f}" r="4" fill="#7d1d2f"/>')
fc = U8/(6*wf['L'][0])
for fq, lab, dy in ((fc, 'U/(6L)', 0), (fh, 'half the variance below', 14)):
    X = SX(lfx(fq), fx0, fx1); svgS.append(f'<line x1="{X:.1f}" y1="16" x2="{X:.1f}" y2="{SH-48}" stroke="#dccdb4" stroke-dasharray="3 3"/><text x="{X+4:.1f}" y="{30+dy}" class="svgc">{lab}</text>')
q1, q2 = 0.05, 0.4; v1 = 3.0
svgS.append(f'<line x1="{SX(lfx(q1), fx0, fx1):.1f}" y1="{SY(lsy(v1), sy0, sy1):.1f}" x2="{SX(lfx(q2), fx0, fx1):.1f}" y2="{SY(lsy(v1*(q2/q1)**(-5/3)), sy0, sy1):.1f}" stroke="#b5681c" stroke-width="1.6"/>')
svgS.append(f'<text x="{SX(lfx(0.02), fx0, fx1):.1f}" y="{SY(lsy(1.6), sy0, sy1):.1f}" class="svgc">slope −5/3</text>')
svgS.append(f'<line x1="{SW-206}" y1="30" x2="{SW-190}" y2="30" stroke="#3f2c23" stroke-width="1.4" stroke-dasharray="5 4"/><text x="{SW-186}" y="34" class="svgc">Kaimal (6.6)</text>')
svgS.append(f'<line x1="{SW-206}" y1="48" x2="{SW-190}" y2="48" stroke="#33627f" stroke-width="2.2"/><text x="{SW-186}" y="52" class="svgc">scaled to the band</text>')
svgS.append(f'<circle cx="{SW-198}" cy="66" r="4" fill="#7d1d2f"/><text x="{SW-186}" y="70" class="svgc">40 synthesised records</text>')
svgS.append(f'<text x="{(64+SW-18)/2}" y="{SH-10}" text-anchor="middle" class="svgd">frequency f, Hz</text>')
svgS.append(f'<text x="16" y="{(16+SH-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 16 {(16+SH-48)/2})">S(f), (m/s)² per Hz</text></svg>')
T['fig_spectrum'] = ('<figure class="fig">' + ''.join(svgS) +
    f'<figcaption>Figure {{{{fig:spectrum}}}}. How the gusts along the shaft share their variance among frequencies, at the hub, 8 m/s, class A ($\\sigma_u$ = {N["wf_sig_u"]} m/s). '
    f'Dashed, the Kaimal model (6.6): flat below $U/(6L_u)$ = {N["wf_fcorner"]} Hz, falling as $f^{{-5/3}}$ above. Blue, the same scaled up by 1/{band:.2f} over the 255 frequencies that a record 256 s long can hold (section 6.4 builds it), 1/256 to 255/256 Hz, '
    f'so that they carry all of $\\sigma_u^2$: what the synthesis (6.8) aims at. Dots, the periodogram of forty synthesised records, averaged in bands. Half the variance lies below {N["wf_fhalf"]} Hz.</figcaption></figure>')

# figure: the Betz stream tube at a = 1/3, and the power coefficient against a
BW, BH = 380, 280
svgB1 = [f'<svg viewBox="0 0 {BW} {BH}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="The stream tube through an ideal rotor seen from the side: air arrives from the left at speed v in a narrow tube, slows to two thirds of v at the rotor disc, and leaves at one third of v in a tube three times the area it had far upstream, twice that of the disc.">',
         '<defs><marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>']
a_ = 1/3; r_up, r_d, r_w = math.sqrt(1 - a_), 1.0, math.sqrt((1 - a_)/(1 - 2*a_))      # radii from A_up v = A v(1-a) = A_w v(1-2a)
cxb, cyb, sc = 190, 120, 62
xs_ = np.linspace(20, 360, 120)
rad = lambda x: math.sqrt((1 - a_)/(1 - a_*(1 + ((x - cxb)/sc)/math.hypot((x - cxb)/sc, 1))))   # area from the actuator disc's speed on its axis, v[1 - a(1 + xi/sqrt(1 + xi^2))]
for sg in (1, -1):
    svgB1.append('<polyline points="' + ' '.join(f'{x:.1f},{cyb - sg*sc*rad(x):.1f}' for x in xs_) + '" fill="none" stroke="#33627f" stroke-width="1.6"/>')
svgB1.append(f'<rect x="{cxb-3}" y="{cyb-sc-6}" width="6" height="{2*sc+12}" fill="#7d1d2f"/><text x="{cxb}" y="{cyb+sc+26}" text-anchor="middle" class="svgc">rotor disc, area A</text>')
for x0, v_, lab in ((44, 1.0, 'v'), (cxb + 14, 1 - a_, 'v(1−a)'), (300, 1 - 2*a_, 'v(1−2a)')):
    svgB1.append(f'<line x1="{x0}" y1="{cyb}" x2="{x0 + 50*v_:.1f}" y2="{cyb}" stroke="#23160f" stroke-width="2.2" marker-end="url(#ahb)"/><text x="{x0}" y="{cyb-10}" class="svgc">{lab}</text>')
svgB1.append(f'<text x="{BW/2}" y="{BH-14}" text-anchor="middle" class="svgd">the stream tube at a = 1/3</text></svg>')
PXb2, PYb2 = panel(BW, BH, 46, 14, 16, 48)
svgB2 = [f'<svg viewBox="0 0 {BW} {BH}" style="flex:1 1 300px;min-width:0;max-width:460px" role="img" aria-label="The power coefficient 4 a times one minus a squared against a from 0 to one half: a hump rising to 16 over 27 at a equals one third. A dashed line marks the 5 megawatt turbine\'s best, 0.482.">',
         f'<rect x="46" y="16" width="{BW-60}" height="{BH-64}" fill="#fff" stroke="#3f2c23"/>']
aa = np.linspace(0, 0.5, 101)
svgB2.append('<polyline points="' + ' '.join(f'{PXb2(x, 0, 0.5):.1f},{PYb2(4*x*(1-x)**2, 0, 0.65):.1f}' for x in aa) + '" fill="none" stroke="#7d1d2f" stroke-width="2.4"/>')
svgB2.append(f'<line x1="46" y1="{PYb2(S["CP_STAR"], 0, 0.65):.1f}" x2="{BW-14}" y2="{PYb2(S["CP_STAR"], 0, 0.65):.1f}" stroke="#33627f" stroke-dasharray="5 4"/><text x="{BW-20}" y="{PYb2(S["CP_STAR"], 0, 0.65)+16:.1f}" text-anchor="end" class="svgc">NREL 5 MW: {S["CP_STAR"]}</text>')
svgB2.append(f'<circle cx="{PXb2(1/3, 0, 0.5):.1f}" cy="{PYb2(16/27, 0, 0.65):.1f}" r="4" fill="#7d1d2f"/><text x="{PXb2(1/3, 0, 0.5):.1f}" y="{PYb2(16/27, 0, 0.65)-10:.1f}" text-anchor="middle" class="svgc">16/27 at a = 1/3</text>')
for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
    X = PXb2(v, 0, 0.5); svgB2.append(f'<line x1="{X:.1f}" y1="{BH-48}" x2="{X:.1f}" y2="{BH-43}" stroke="#3f2c23"/><text x="{X:.1f}" y="{BH-30}" text-anchor="middle" class="svgc">{v:g}</text>')
for v in (0, 0.2, 0.4, 0.6):
    Y = PYb2(v, 0, 0.65); svgB2.append(f'<line x1="41" y1="{Y:.1f}" x2="46" y2="{Y:.1f}" stroke="#3f2c23"/><text x="37" y="{Y+4:.1f}" text-anchor="end" class="svgc">{v:g}</text>')
svgB2.append(f'<text x="{(46+BW-14)/2}" y="{BH-10}" text-anchor="middle" class="svgd">slowing at the disc, a</text>')
svgB2.append(f'<text x="14" y="{(16+BH-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 14 {(16+BH-48)/2})">power coefficient C_p</text></svg>')
# ---- figure: the rotor's two torques against its speed (L2_torque.json from notes/rotor-pendula/derive/L2_torque_curve.py) -----------
tq = J('L2_torque.json'); TW, TH = 560, 330
PXt, PYt = panel(TW, TH, 58, 16, 16, 50); rlo, rhi, qhi = 5.5, 11.5, 4.0
svgT = [f'<svg viewBox="0 0 {TW} {TH}" role="img" aria-label="The rotor\'s two torques against its speed, from 5.5 to 11.5 turns a minute. The main generator\'s torque law: zero below 6.9 rpm, a straight ramp up to 8.98 rpm, then the square law k Omega squared; the pure square law is drawn dashed below the ramp. The wind\'s torque at 6, 8 and 10 metres per second falls slowly with speed. Where a wind curve meets the torque law the rotor runs steadily: at 6 m/s on the ramp, at 7.91 rpm, faster than the square law\'s 6.80 rpm; at 8 and 10 m/s on the square law.">',
        f'<rect x="58" y="16" width="{TW-74}" height="{TH-66}" fill="#fff" stroke="#3f2c23"/>',
        f'<rect x="{PXt(tq["ramp"]["start_rpm"], rlo, rhi):.1f}" y="17" width="{PXt(tq["ramp"]["end_rpm"], rlo, rhi) - PXt(tq["ramp"]["start_rpm"], rlo, rhi):.1f}" height="{TH-68}" fill="#f3ece0"/>',
        f'<text x="{(PXt(tq["ramp"]["start_rpm"], rlo, rhi) + PXt(tq["ramp"]["end_rpm"], rlo, rhi))/2:.1f}" y="32" text-anchor="middle" class="svgc">the ramp</text>']
pl = lambda ys, col, w, dash='': ('<polyline points="' + ' '.join(f'{PXt(r, rlo, rhi):.1f},{PYt(min(q/1e6, qhi), 0, qhi):.1f}' for r, q in zip(tq['rpm'], ys)) +
                                  f'" fill="none" stroke="{col}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
for vk, lab in (('6.0', '6 m/s'), ('8.0', '8 m/s'), ('10.0', '10 m/s')):
    svgT.append(pl(tq['Q_aero'][vk], '#33627f', 1.4))
    ylab = tq['Q_aero'][vk][12]/1e6
    svgT.append(f'<text x="{PXt(tq["rpm"][12], rlo, rhi):.1f}" y="{PYt(ylab, 0, qhi) - 11:.1f}" class="svgc" fill="#33627f">wind, {lab}</text>')
svgT.append(pl(tq['Q_k2'], '#3f2c23', 1.3, '5 4'))
svgT.append(pl(tq['Q_gen'], '#7d1d2f', 2.6))
for vk in ('6.0', '8.0', '10.0'):
    for law, col in (('nrel', '#7d1d2f'), ('k2', '#3f2c23')):
        r_ = tq['cross'][vk][law]
        if r_ is None or (law == 'k2' and vk != '6.0'):
            continue
        q_ = float(np.interp(r_, tq['rpm'], tq['Q_aero'][vk]))/1e6
        svgT.append(f'<circle cx="{PXt(r_, rlo, rhi):.1f}" cy="{PYt(q_, 0, qhi):.1f}" r="4" fill="{col if law == "nrel" else "#fff"}" stroke="{col}" stroke-width="1.6"/>')
for r in (6, 7, 8, 9, 10, 11):
    X = PXt(r, rlo, rhi); svgT.append(f'<line x1="{X:.1f}" y1="{TH-50}" x2="{X:.1f}" y2="{TH-45}" stroke="#3f2c23"/><text x="{X:.1f}" y="{TH-32}" text-anchor="middle" class="svgc">{r}</text>')
for q in (0, 1, 2, 3, 4):
    Y = PYt(q, 0, qhi); svgT.append(f'<line x1="53" y1="{Y:.1f}" x2="58" y2="{Y:.1f}" stroke="#3f2c23"/><text x="49" y="{Y+4:.1f}" text-anchor="end" class="svgc">{q}</text>')
svgT.append(f'<line x1="{TW-190}" y1="{TH-120}" x2="{TW-176}" y2="{TH-120}" stroke="#7d1d2f" stroke-width="2.6"/><text x="{TW-172}" y="{TH-116}" class="svgc">torque law (NREL)</text>')
svgT.append(f'<line x1="{TW-190}" y1="{TH-104}" x2="{TW-176}" y2="{TH-104}" stroke="#3f2c23" stroke-dasharray="5 4"/><text x="{TW-172}" y="{TH-100}" class="svgc">pure square law kΩ²</text>')
svgT.append(f'<text x="{(58+TW-16)/2}" y="{TH-10}" text-anchor="middle" class="svgd">rotor speed, turns a minute</text>')
svgT.append(f'<text x="16" y="{(16+TH-50)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 16 {(16+TH-50)/2})">torque on the rotor, MN m</text></svg>')
T['fig_torque'] = ('<figure class="fig">' + ''.join(svgT) +
    f'<figcaption>Figure {{{{fig:torque}}}}. The rotor\'s two torques against its speed. Wine: the main generator\'s torque law, zero below {tq["ramp"]["start_rpm"]:.2f} rpm, '
    f'a straight ramp (shaded) up to {tq["ramp"]["end_rpm"]:.2f} rpm, then the square law $k\\Omega^2$; dashed, the pure square law continued downwards. Blue: the wind\'s torque '
    f'$Q_{{\\rm aero}}$ at 6, 8 and 10 m/s, from NREL\'s $C_p$ table. The rotor runs steadily where the two meet (dots): at 8 and 10 m/s on the square law, at '
    f'{tq["cross"]["8.0"]["nrel"]:.2f} and {tq["cross"]["10.0"]["nrel"]:.2f} rpm; at 6 m/s on the ramp, at {tq["cross"]["6.0"]["nrel"]:.2f} rpm, faster than the '
    f'{tq["cross"]["6.0"]["k2"]:.2f} rpm (open dot) the square law alone would give. A gust or a lull moves the wind\'s curve up or down. Just above the ramp, a lull drops the '
    f'rotor onto the ramp, whose torque falls steeply as the speed drops, so the rotor slows less than it speeds up in an equal gust: its mean speed rises.</figcaption></figure>')
T['fig_betz'] = ('<figure class="fig"><div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' + ''.join(svgB1) + ''.join(svgB2) + '</div>'
    '<figcaption>Figure {{fig:betz}}. The Betz limit. First panel: the air that passes the rotor, seen from the side, at the best slowing $a = 1/3$. The same mass flows through every '
    'cross-section, so where the air is slower the tube is wider: far upstream it has $1-a$ = 2/3 of the disc\'s area, far downstream $(1-a)/(1-2a)$ = 2 of it, three times its upstream area (the arrows are to scale; the tube between follows the speed an ideal disc induces along its axis). '
    'Second panel: the power coefficient (6.2), $C_p = 4a(1-a)^2$, with its maximum 16/27 (6.3) and the 5 MW turbine\'s best.</figcaption></figure>')
N['wf_var_u'] = f(wf['var_hub_u'], 2); N['wf_sig2_u'] = f(wf['sigma_u']**2, 2); N['wf_var_se'] = f(wf['var_hub_se_u'], 2)
N['wf_spec_dev'] = f(wf['spec_dev_max']*100, 0)
N['wf_var_eff'] = f(wf['var_eff'], 2); N['wf_var_chi'] = f(wf['var_eff_chi'], 2)
gs = {r['shape']: r for r in wf['gusty_8A']}; cs = {r['shape']: r for r in wf['calm_8']}
N['wf_om_sd'] = f(gs['none']['Om_sd']/gs['none']['Om_mean']*100, 1)
_st8 = [r for r in J('L6_wind.json')['steady'] if r['U'] == 8.0][0]
N['wf_rpm_calm8'] = f(_st8['Om0']*60/(2*math.pi), 2); N['wf_vbar8'] = f(_st8['vbar'], 2)   # steady sheared wind at 8 m/s: the disc-averaged wind and the rotor speed it sets
N['wf_P_none'] = f(gs['none']['P_mean']*1e3, 0); N['wf_P_calm'] = f(cs['none']['P_mean']*1e3, 0)
N['wf_P_none_pct'] = f(abs(gs['none']['P_mean']/cs['none']['P_mean'] - 1)*100, 1)
N['wf_P_sym'] = f(gs['streamlined']['P_mean']*1e3, 0); N['wf_P_wing'] = f(gs['wing']['P_mean']*1e3, 0)
N['wf_calm_none'] = f(cs['none']['P_mean']*1e3, 0); N['wf_calm_none_err'] = f(abs(cs['none']['P_mean']/cs['none']['P_star'] - 1)*100, 1)
for k, key in (('streamlined', 'sym'), ('wing', 'wing')):
    N[f'wf_calm_{key}'] = f(cs[k]['P_mean']*1e3, 0); N[f'wf_calm_{key}_pct'] = sgn((cs[k]['P_mean']/cs['none']['P_mean'] - 1)*100, 0)
    N[f'wf_calm_{key}_lean'] = f(math.degrees(cs[k]['th_mean']), 1)
N['wf_wing_gust_pct'] = f((gs['wing']['P_mean']/cs['wing']['P_mean'] - 1)*100, 0)
N['wf_sym_gust_pct'] = f((gs['streamlined']['P_mean']/cs['streamlined']['P_mean'] - 1)*100, 0)
N['wf_none_gust_pct'] = f((gs['none']['P_mean']/cs['none']['P_mean'] - 1)*100, 1)
N['wf_book'] = sci(wc['book_worst_rel'], 0)
# the wing's torque about the hinge for 1 m/s more wind along the shaft (quasi-steady (7.1), C_L = 1 + 2 pi (gamma - gamma_0), chord 0.1 m, l = 1 m)
Ut8, Ua8 = Om[8.0]*rp, 8.0*math.cos(math.radians(5))*(2/3)
def Ftw(Ua):
    gm = math.atan2(Ua, Ut8); g0 = math.atan2(Ua8, Ut8); CL = 1 + 2*math.pi*(gm - g0)
    return 0.5*rho*(Ut8**2 + Ua**2)*0.1*l*(CL*math.sin(gm) - 0.01*math.cos(gm))
dtau = (Ftw(Ua8 + math.cos(math.radians(5))*(2/3)) - Ftw(Ua8))*l/2
N['wf_wing_dtau'] = f(dtau, 1); N['wf_wing_dtau_frac'] = f(dtau/(mlc*g), 2)
N['p6_coh_f'] = f(U8*math.log(2)/(12*12.6), 3); N['p6_coh_L'] = f(12*12.6/math.log(2), 0)
# the figure: one instant of the field over the disc, and the coherences the synthesis gives back
sn = wf['snapshot']; W6, H6 = 380, 330
cx6, cy6, sc6 = 190, 165, 2.2
lim6 = 2*wf['sigma_u']
def cm6(v):
    a_ = max(-1.0, min(1.0, v/lim6)); s_ = abs(a_)**0.85; end = (51, 98, 127) if a_ < 0 else (125, 29, 47); mid = (252, 248, 240)
    return 'rgb(' + ','.join(str(round(mid[c] + (end[c] - mid[c])*s_)) for c in range(3)) + ')'
svgW = [f'<svg viewBox="0 0 {W6} {H6}" style="flex:1 1 300px;min-width:0;max-width:440px" role="img" aria-label="One instant of the synthesised wind over the rotor disc, seen from upwind, at 8 m/s, class A: squares coloured by how much faster (wine) or slower (blue) than its mean at that height the wind blows along the shaft, with arrows for the wind across the disc. Patches tens of metres wide are faster or slower together.">',
        f'<defs><clipPath id="disc6"><circle cx="{cx6}" cy="{cy6}" r="{63*sc6}"/></clipPath><marker id="aw6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#23160f"/></marker></defs>',
        f'<rect x="0" y="0" width="{W6}" height="{H6}" fill="#fff"/><g clip-path="url(#disc6)">']
for p_ in range(len(sn['u'])):
    yy, zz_ = sn['y'][p_], sn['z'][p_]
    svgW.append(f'<rect x="{cx6 + (yy - 6.3)*sc6:.1f}" y="{cy6 - (zz_ + 6.3)*sc6:.1f}" width="{12.6*sc6 + 0.4:.1f}" height="{12.6*sc6 + 0.4:.1f}" fill="{cm6(sn["u"][p_])}"/>')
svgW.append('</g>')
svgW.append(f'<circle cx="{cx6}" cy="{cy6}" r="{63*sc6}" fill="none" stroke="#3f2c23"/>')
for p_ in range(len(sn['u'])):
    yy, zz_ = sn['y'][p_], sn['z'][p_]
    if math.hypot(yy, zz_) <= 63:
        x0_, y0_ = cx6 + yy*sc6, cy6 - zz_*sc6
        svgW.append(f'<line x1="{x0_:.1f}" y1="{y0_:.1f}" x2="{x0_ + 3*sn["v"][p_]*sc6:.1f}" y2="{y0_ - 3*sn["w"][p_]*sc6:.1f}" stroke="#23160f" stroke-width="1" marker-end="url(#aw6)"/>')
svgW.append(f'<text x="{W6/2}" y="{H6-10}" text-anchor="middle" class="svgd">the disc from upwind, 126 m across; colour ±{lim6:.1f} m/s</text></svg>')
PXc, PYc = panel(W6, H6, 48, 14, 16, 48)
fa, fb_ = math.log10(0.004), math.log10(0.6)
svgC = [f'<svg viewBox="0 0 {W6} {H6}" style="flex:1 1 300px;min-width:0;max-width:440px" role="img" aria-label="Coherence against frequency from 0.004 to 0.6 hertz, for points 12.6 and 25.2 metres apart: the model curves of the along-shaft and crosswind gusts, falling from near one to near zero, and dots from forty synthesised records lying on them.">',
        f'<rect x="48" y="16" width="{W6-62}" height="{H6-64}" fill="#fff" stroke="#3f2c23"/>']
for v_, lab in ((0.01, '0.01'), (0.1, '0.1'), (0.5, '0.5')):
    Xv = PXc(math.log10(v_), fa, fb_); svgC.append(f'<line x1="{Xv:.1f}" y1="{H6-48}" x2="{Xv:.1f}" y2="{H6-43}" stroke="#3f2c23"/><text x="{Xv:.1f}" y="{H6-30}" text-anchor="middle" class="svgc">{lab}</text>')
for v_ in (0, 0.5, 1):
    Yv = PYc(v_, -0.05, 1.05); svgC.append(f'<line x1="43" y1="{Yv:.1f}" x2="48" y2="{Yv:.1f}" stroke="#3f2c23"/><text x="39" y="{Yv+4:.1f}" text-anchor="end" class="svgc">{v_:g}</text>')
fgrid = np.logspace(fa, fb_, 120)
for cv in wf['coh_curves']:
    comp = 0 if cv['comp'] == 'u' else 1; r_ = cv['r']
    col = '#7d1d2f' if comp == 0 else '#33627f'; dash = '' if r_ < 13 else ' stroke-dasharray="5 3"'
    if comp == 0:
        mod = np.exp(-12*np.sqrt((fgrid*r_/U8)**2 + (0.12*r_/wf['Lc'])**2))
    else:
        mod = np.exp(-0.75*fgrid*r_)
    svgC.append('<polyline points="' + ' '.join(f'{PXc(math.log10(fv), fa, fb_):.1f},{PYc(mv, -0.05, 1.05):.1f}' for fv, mv in zip(fgrid, mod)) + f'" fill="none" stroke="{col}" stroke-width="1.6"{dash}/>')
    svgC += [f'<circle cx="{PXc(math.log10(fv), fa, fb_):.1f}" cy="{PYc(cvv, -0.05, 1.05):.1f}" r="2.8" fill="{col}" fill-opacity="0.8"/>' for fv, cvv in cv['points'] if fa <= math.log10(fv) <= fb_]
svgC.append(f'<line x1="{W6-150}" y1="30" x2="{W6-136}" y2="30" stroke="#7d1d2f" stroke-width="2"/><text x="{W6-132}" y="34" class="svgc">u, 12.6 m</text>')
svgC.append(f'<line x1="{W6-150}" y1="46" x2="{W6-136}" y2="46" stroke="#7d1d2f" stroke-width="2" stroke-dasharray="5 3"/><text x="{W6-132}" y="50" class="svgc">u, 25.2 m</text>')
svgC.append(f'<line x1="{W6-150}" y1="62" x2="{W6-136}" y2="62" stroke="#33627f" stroke-width="2"/><text x="{W6-132}" y="66" class="svgc">v, 12.6 m</text>')
svgC.append(f'<line x1="{W6-150}" y1="78" x2="{W6-136}" y2="78" stroke="#33627f" stroke-width="2" stroke-dasharray="5 3"/><text x="{W6-132}" y="82" class="svgc">v, 25.2 m</text>')
svgC.append(f'<text x="{(48+W6-14)/2}" y="{H6-10}" text-anchor="middle" class="svgd">frequency, Hz</text>')
svgC.append(f'<text x="14" y="{(16+H6-48)/2}" text-anchor="middle" class="svgd" transform="rotate(-90 14 {(16+H6-48)/2})">coherence</text></svg>')
T['fig_wind'] = ('<figure class="fig"><div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' + ''.join(svgW) + ''.join(svgC) + '</div>'
    '<figcaption>Figure {{fig:wind}}. The synthesised wind at 8 m/s, turbulence class A. Left: one instant of the first record over the rotor disc, seen from upwind, as the grid stores it; '
    'colour is the gust along the shaft, wine faster and blue slower than the mean at that height, and arrows are the wind across the disc, 3 m of drawing per m/s. '
    'Right: what the synthesis gives back. Lines are the coherences put in, (6.7) for $u$ and the smooth-model default for $v$, for points 12.6 and 25.2 m apart; '
    'dots are measured from forty records. Slow gusts are shared across the disc, quick ones are not. The Wind tab animates this field.</figcaption></figure>')

json.dump({'n': N, 'table': T}, open(ROOT / 'numbers.json', 'w'), indent=1, ensure_ascii=False)
print(f'{len(N)} numbers and {len(T)} tables written to numbers.json')
