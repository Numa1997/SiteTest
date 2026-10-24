"""L3: the mother blade sags edgewise under its own weight, once per turn, and the hinge at its tip rides on that sag.
Size of the effect on the second blade's power (setup.py), by two shape models and two routes.

Run: python3 -I L3_sag_tip.py   (writes L3_sag_tip.json; PASS/FAIL)
Linear theory (L3_sag.py): theta'' + kappa theta' + R theta = -(G + 3 w/l) cos(phi) + kappa beta',  beta = -w' cos(phi), the
generator taking c <(thetadot - betadot)^2>.  1P sag at the hinge w and the slope w' there, amplified by 1/(1 - (Omega/omega_e)^2):
  shape model A: first edgewise mode (nrel5mw.py: OpenFAST blade table, mode shape, frequency): x_tip = (int mu Phi dr) g / k_e;
  shape model B: the static bend integrated from the same table (shear, moment, curvature M/EI, slope, deflection), once with the
                 edgewise stiffness alone and once with the in-plane compliance projected through the structural twist.
Second route: the full nonlinear equation of the rod with the hinge displaced by u = -w cos(phi) and the tip section turned by
beta = -w' cos(phi) (Lagrangian in SymPy, integrated with the Radau IIA engine), against the linear numbers of shape model A.
In-plane gravity g cos 5 deg (shaft tilt).  Rotor at 8 m/s.
"""
import json, math, os, sys
import numpy as np, sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrel5mw as T5
import setup as S
from engine import radau_step

fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)

gg = S.G0*math.cos(math.radians(5.0)); mm, ll = S.M_B, S.L_B; II, MLC = mm*ll**2/3, mm*ll/2
Om = S.omega(8.0); rp = S.R_ROT
tab = T5.blade_table(); Lb = T5.R_TIP - T5.R_HUB; x = tab[:, 0]; mu = tab[:, 2]*T5.ADJ_BL_MS
om_e = 2*math.pi*T5.F_EDGE_SYS; amp = 1/(1 - (Om/om_e)**2)
R = MLC*rp/II; G = MLC*gg/(II*Om**2); kap = R - 1

def P_lin(w, wp):
    """mean power over the ideal brake's best (unit I Omega^3), theta = Re[A e^{i phi}], beta = Re[-wp e^{i phi}]."""
    B = -wp; A = (-(G + 3*w/ll) + kap*1j*B)/(R - 1 + 1j*kap)
    return kap*abs(A - B)**2/2

out = []
# shape model A: the first edgewise mode
ph = T5.edge_shape(x); m_e = np.trapezoid(mu*ph**2, x*Lb); g_e = np.trapezoid(mu*ph, x*Lb)
x_tip = g_e*gg/(m_e*om_e**2)*amp
dshape = lambda xx: sum(cc*(k + 2)*xx**(k + 1) for k, cc in enumerate(T5.EDGE_SHAPE))
xs = (rp - T5.R_HUB)/Lb
wA, wpA = T5.edge_shape(xs)*x_tip, dshape(xs)*x_tip/Lb
P0 = P_lin(0, 0)
out.append(dict(model='first edgewise mode', w=wA, wp=wpA, x_tip=x_tip, sag_only=P_lin(wA, 0)/P0 - 1, total=P_lin(wA, wpA)/P0 - 1))
# shape model B: static bend from the table
r = T5.R_HUB + x*Lb; tw = np.radians(tab[:, 1]); EIf, EIe = tab[:, 3], tab[:, 4]
def cum_tip(f):
    o = np.zeros_like(f)
    for i in range(len(f) - 2, -1, -1): o[i] = o[i + 1] + 0.5*(f[i] + f[i + 1])*(r[i + 1] - r[i])
    return o
def cum_root(f):
    o = np.zeros_like(f)
    for i in range(1, len(f)): o[i] = o[i - 1] + 0.5*(f[i] + f[i - 1])*(r[i] - r[i - 1])
    return o
Mb = cum_tip(cum_tip(mu*gg))
for lab, comp in (('static bend, edgewise stiffness', 1/EIe), ('static bend, twist-projected', np.cos(tw)**2/EIe + np.sin(tw)**2/EIf)):
    slope = cum_root(Mb*comp)*amp; w = cum_root(slope/amp)*amp
    wi, si = float(np.interp(rp, r, w)), float(np.interp(rp, r, slope))
    out.append(dict(model=lab, w=wi, wp=si, x_tip=float(w[-1]), sag_only=P_lin(wi, 0)/P0 - 1, total=P_lin(wi, si)/P0 - 1))
for o in out:
    print(f"   {o['model']}: sag at the hinge {o['w']*1e3:.1f} mm, slope {o['wp']*1e3:.2f} mrad; power: sag in the drive {o['sag_only']*100:+.3f} %, "
          f"with the section's turn {o['total']*100:+.3f} %")
check('both shape models agree on the sign of the total change', len({math.copysign(1, o['total']) for o in out}) == 1)

# second route: the full nonlinear equation of the rod with u = -w cos(phi), beta = -w' cos(phi)
t, s = sp.symbols('t s', real=True)
m, l, rps, g, W, c, w, wp = sp.symbols('m l r_p g Omega c w wp', real=True)
th = sp.Function('theta')(t)
phi = W*t; u = -w*sp.cos(phi); be = -wp*sp.cos(phi)
er = sp.Matrix([sp.cos(phi), sp.sin(phi)]); et = sp.Matrix([-sp.sin(phi), sp.cos(phi)])
pos = rps*er + u*et + s*sp.Matrix([sp.cos(phi + th), sp.sin(phi + th)])
v = pos.diff(t); Lg = sp.integrate((m/l)*v.dot(v)/2, (s, 0, l)) - sp.integrate((m/l)*g*pos[1], (s, 0, l))
EL = sp.diff(Lg.diff(th.diff(t)), t) - Lg.diff(th) + c*(th.diff(t) - be.diff(t))
A_, q, qd = sp.symbols('A q qd')
acc = sp.solve(EL.subs(th.diff(t, 2), A_).subs(th.diff(t), qd).subs(th, q), A_)[0]
f_acc = sp.lambdify((t, q, qd, m, l, rps, g, W, c, w, wp), acc, 'numpy')
f_pw = sp.lambdify((t, q, qd, m, l, rps, g, W, c, w, wp), c*(qd - be.diff(t))**2, 'numpy')
cv = kap*II*Om
res = []
for ww, wwp in ((0, 0), (wA, 0), (wA, wpA)):
    args = (mm, ll, rp, gg, Om, cv, ww, wwp)
    Fn = lambda tt, Y: np.stack([Y[:, 1], f_acc(tt, Y[:, 0], Y[:, 1], *args), f_pw(tt, Y[:, 0], Y[:, 1], *args)], axis=1)
    Tt = 2*math.pi/Om; h = Tt/200; Y = np.zeros((1, 3))
    for k in range(200*60):
        if k == 200*40: E0 = Y[0, 2]
        Y, _ = radau_step(Fn, k*h, Y, h)
    res.append((Y[0, 2] - E0)/(200*20*h))
d_sag, d_tot = res[1]/res[0] - 1, res[2]/res[0] - 1
print(f'   full equation (shape model A): sag in the drive {d_sag*100:+.3f} %, with the section\'s turn {d_tot*100:+.3f} %; rigid-blade power {res[0]*1e3:.3f} mW')
# the linear theory drops -G theta sin(phi) (first order in theta, G not small) and the nonlinear terms: about 1 % of the power, so
# about 1 % of any change it describes. The limit: 2 % of the sag's own effect on the drive (0.37 percentage point here).
lim = 0.02*abs(out[0]['sag_only'])
check(f'the full equation agrees with the linear theory within 2 % of the sag\'s effect ({lim*100:.2f} percentage point), sag only and total',
      abs(d_sag - out[0]['sag_only']) < lim and abs(d_tot - out[0]['total']) < lim)
out[0].update(full_sag_only=d_sag, full_total=d_tot, P_rigid=res[0])
json.dump(dict(rows=out, Om=Om, amp=amp, rp=rp), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L3_sag_tip.json'), 'w'), indent=1)
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
