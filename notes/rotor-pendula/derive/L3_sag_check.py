"""L3 sag, second route: the full nonlinear equation from the same Lagrangian (no linearisation), integrated with the
Radau IIA engine, pivot displaced by u = -w cos(phi) and section rotated by beta = -w' cos(phi); generator on theta - beta.
Run: python3 -I L3_sag_check.py   (PASS if the nonlinear power changes agree with the linear ones within 0.3 percentage points)
"""
import math, os, sys
import numpy as np, sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
import nrel5mw as T5
t = sp.symbols('t', real=True)
m, L, rp, g, W, c, w, wp = sp.symbols('m L r_p g Omega c w wp', real=True)
th = sp.Function('theta')(t)
phi = W*t; u = -w*sp.cos(phi); be = -wp*sp.cos(phi)
er = sp.Matrix([sp.cos(phi), sp.sin(phi)]); et = sp.Matrix([-sp.sin(phi), sp.cos(phi)])
pos = rp*er + u*et + L*sp.Matrix([sp.cos(phi + th), sp.sin(phi + th)])
v = pos.diff(t); T = m/2*v.dot(v); V = m*g*pos[1]; Lg = T - V
F = c/2*(th.diff(t) - be.diff(t))**2
EL = sp.diff(Lg.diff(th.diff(t)), t) - Lg.diff(th) + F.diff(th.diff(t))
A, q, qd = sp.symbols('A q qd')
e = EL.subs(th.diff(t, 2), A).subs(th.diff(t), qd).subs(th, q)
acc = sp.solve(e, A)[0]
pw = (c*(qd - be.diff(t))**2)
f_acc = sp.lambdify((t, q, qd, m, L, rp, g, W, c, w, wp), acc, 'numpy')
f_pw = sp.lambdify((t, q, qd, m, L, rp, g, W, c, w, wp), pw, 'numpy')
gg = 9.80665*math.cos(math.radians(5.0)); mm, LL, Om = 0.1, 0.2, 0.9494
lin = {0.3: (-0.30, 1.17), 0.6: (-0.63, 6.19), 0.9: (0.66, 14.69)}    # from L3_sag_numbers.py: (with rotation, sag only)
tab = T5.blade_table(); Lb = T5.R_TIP - T5.R_HUB; x = tab[:, 0]; mu = tab[:, 2]*T5.ADJ_BL_MS
ph = T5.edge_shape(x); m_e = np.trapezoid(mu*ph**2, x*Lb); g_e = np.trapezoid(mu*ph, x*Lb)
om_e = 2*math.pi*T5.F_EDGE_SYS; x_tip = g_e*gg/(m_e*om_e**2)/(1 - (Om/om_e)**2)
dshape = lambda xx: sum(cc*(k + 2)*xx**(k + 1) for k, cc in enumerate(T5.EDGE_SHAPE))
fails = 0
for frac in (0.3, 0.6, 0.9):
    rpv = frac*T5.R_TIP; xs = (rpv - T5.R_HUB)/Lb
    wv = T5.edge_shape(xs)*x_tip; wpv = dshape(xs)*x_tip/Lb
    cv = mm*LL**2*Om*(rpv/LL - 1)
    res = []
    for (ww, wwp) in ((0, 0), (wv, 0), (wv, wpv)):
        args = (mm, LL, rpv, gg, Om, cv, ww, wwp)
        def Fn(tt, Y):
            return np.stack([Y[:, 1], f_acc(tt, Y[:, 0], Y[:, 1], *args), f_pw(tt, Y[:, 0], Y[:, 1], *args)], axis=1)
        Tt = 2*math.pi/Om; h = Tt/100; Y = np.zeros((1, 3))
        for k in range(6000):
            if k == 4000: E0 = Y[0, 2]
            Y, _ = radau_step(Fn, k*h, Y, h)
        res.append((Y[0, 2] - E0)/(2000*h))
    d_sag = (res[1]/res[0] - 1)*100; d_tot = (res[2]/res[0] - 1)*100
    ok = abs(d_sag - lin[frac][1]) < 0.3 and abs(d_tot - lin[frac][0]) < 0.3
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} pivot {frac*100:.0f} %: nonlinear sag only {d_sag:+.2f} % (linear {lin[frac][1]:+.2f}), "
          f"with section rotation {d_tot:+.2f} % (linear {lin[frac][0]:+.2f}); rigid-blade power {res[0]*1e3:.3f} mW")
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
