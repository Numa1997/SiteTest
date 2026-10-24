"""L3: random edgewise shaking with the second blade loading the mother blade (two-way). Linear frequency-domain theory.

Run: python3 -I L3_shake2.py   (writes L3_shake2.json; PASS/FAIL on the energy bound)
Coordinates: blade edgewise tip coordinate x (modal mass m_e, frequency w_e, damping zeta_e) and the second blade's angle.
The hinge sits at the tip (mode shape 1 there) and moves along the blade's tangent by u = Phi_p x and the blade section (with the generator's stator) turns by
beta = Phi'_p x (L3_sag.py).  The Lagrangian (rotor at uniform Omega, gravity left out: its 1P effect is in L3_sag.py) is
linearised by SymPy about rest; the turbulent modal force on the blade is white near w_e, scaled so that the blade WITHOUT the
second blade has tip rms sigma_tip.  Generator power = int S_F(w) w^2 |H_rel(w)|^2 c dw over the band.
Energy bound checked: the generator never takes more than the turbulent power fed into the blade.
"""
import json, math, os, sys
import numpy as np, sympy as sp
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrel5mw as T5
import setup as S

t = sp.symbols('t', real=True)
Om, rp, Pp, Pq, me, ke = sp.symbols('Omega r_p Phi_p Phid_p m_e k_e', real=True)

def linear_mats(n, ms, ls):
    """Return M, G, K (numeric functions of Omega) for the mother blade's edgewise mode x and a chain of n uniform rods
    (masses ms, lengths ls) hinged at the tip; each rod's kinetic and potential energy is integrated over its length."""
    x = sp.Function('x')(t); qs = [sp.Function(f'q{k}')(t) for k in range(n)]
    s_ = sp.symbols('s', positive=True)
    ms = [sp.nsimplify(v, rational=True) for v in ms]; ls = [sp.nsimplify(v, rational=True) for v in ls]   # exact: no float residue
    phi = Om*t
    er = sp.Matrix([sp.cos(phi), sp.sin(phi)]); et = sp.Matrix([-sp.sin(phi), sp.cos(phi)])
    base = rp*er + Pp*x*et
    T = me/2*x.diff(t)**2; V = ke/2*x**2
    for k in range(n):
        dirk = sp.Matrix([sp.cos(phi + qs[k]), sp.sin(phi + qs[k])])
        pos = base + s_*dirk
        v = pos.diff(t)
        T += sp.integrate((ms[k]/ls[k])*v.dot(v)/2, (s_, 0, ls[k]))
        base = base + ls[k]*dirk
    gen = [x] + qs
    Lg = T - V
    eqs = [sp.diff(Lg.diff(gq.diff(t)), t) - Lg.diff(gq) for gq in gen]
    eps = sp.symbols('eps')
    sub = {gq: eps*gq for gq in gen}
    lin = [sp.expand(sp.series(e.subs(sub).doit(), eps, 0, 2).removeO().subs(eps, 1)) for e in eqs]
    d = len(gen)
    Mm = sp.Matrix(d, d, lambda i, j: lin[i].coeff(gen[j].diff(t, 2)))
    Gm = sp.Matrix(d, d, lambda i, j: lin[i].coeff(gen[j].diff(t)))
    rest = [sp.expand(lin[i] - sum(Mm[i, j]*gen[j].diff(t, 2) + Gm[i, j]*gen[j].diff(t) for j in range(d))) for i in range(d)]
    Km = sp.Matrix(d, d, lambda i, j: rest[i].coeff(gen[j]))
    for i in range(d):
        leftover = sp.expand(rest[i] - sum(Km[i, j]*gen[j] for j in range(d)))
        fl = sp.lambdify((t, Om, rp, Pp, me, ke), leftover, 'numpy')
        assert abs(fl(0.37, 0.95, 50.0, 0.8, 1400.0, 6e4)) < 1e-12, leftover     # round-off only
    Mm, Gm, Km = [A.applyfunc(lambda e: sp.simplify(sp.trigsimp(e))) for A in (Mm, Gm, Km)]
    for A in (Mm, Gm, Km):
        assert t not in A.free_symbols, A          # uniform rotation: the linear matrices are constant
    f = lambda A: sp.lambdify((Om, rp, Pp, me, ke), A, 'numpy')
    return f(Mm), f(Gm), f(Km), d

g_ = 9.80665
tab = T5.blade_table(); Lb = T5.R_TIP - T5.R_HUB; xb = tab[:, 0]; mu = tab[:, 2]*T5.ADJ_BL_MS
phis = T5.edge_shape(xb); M_E = np.trapezoid(mu*phis**2, xb*Lb)
W_E = 2*math.pi*T5.F_EDGE_SYS; K_E = M_E*W_E**2
dshape = lambda xx: sum(cc*(k + 2)*xx**(k + 1) for k, cc in enumerate(T5.EDGE_SHAPE))
RP = S.R_ROT; XS = (RP - T5.R_HUB)/Lb; PHI = T5.edge_shape(XS); PHID = dshape(XS)/Lb
OM0 = 0.9494

def device(L, m=None):
    """the second blade: one uniform rod of length L (mass m, by default setup.M_B scaled with the length at its line density)."""
    m = S.M_B*L/S.L_B if m is None else m
    return linear_mats(1, [m], [L]), [np.array([0, 1.0])], [1.0]

def gen_power(dev, c, Om, sig_tip, zeta, ws, both=True):
    (Mf, Gf, Kf, d), rows, _ = dev
    M = np.array(Mf(Om, RP, PHI, M_E, K_E), float); G = np.array(Gf(Om, RP, PHI, M_E, K_E), float)
    K = np.array(Kf(Om, RP, PHI, M_E, K_E), float)
    # generator rows act on the relative velocity; the pivot generator sees q1 - beta, beta = PHID * x
    R0 = rows[0].copy(); R0[0] = -PHID
    Rs = [R0] + rows[1:]
    C = sum(c*np.outer(r, r) for r in Rs) + np.diag([2*zeta*W_E*M_E] + [0]*(d - 1))
    # white modal force of one-sided density S0, chosen so the bare blade has tip variance sig^2: sig^2 = S0 int |H_e|^2
    He2 = 1/((K_E - M_E*ws**2)**2 + (2*zeta*W_E*M_E*ws)**2)
    S0 = sig_tip**2/np.trapezoid(He2, ws)
    e0 = np.zeros(d); e0[0] = 1.0
    P = 0.0; Pin = 0.0
    H = np.array([np.linalg.solve(K - w*w*M + 1j*w*(C + G), e0) for w in ws])     # response to unit modal force
    vrel = np.array([sum(c*abs(1j*w*(r @ h))**2 for r in Rs) for w, h in zip(ws, H)])
    P = np.trapezoid(S0*vrel, ws)
    Pin = np.trapezoid(S0*np.real(1j*ws*H[:, 0]), ws)       # power the turbulent force feeds in: <F x'>
    xrms = math.sqrt(np.trapezoid(S0*np.abs(H[:, 0])**2, ws))
    qrms = math.sqrt(np.trapezoid(S0*np.abs(H[:, 1])**2, ws))      # rms of the (first) rod angle from the shaking
    gen_power.qrms = qrms
    return P, Pin, xrms

if __name__ == '__main__':
    L_t = 1.5*RP*OM0**2/W_E**2                      # Omega^2 R = omega_e^2 with R = 3 r_p/(2 l): the second blade tuned to the edgewise mode
    devs = {f'second blade ({S.L_B:g} m)': device(S.L_B), f'tuned second blade ({L_t:.2f} m)': device(L_t)}
    print(f'hinge at the tip: Phi = {PHI:.4f}, slope {PHID:.4f} /m; blade modal mass {M_E:.0f} kg; tuned second blade {L_t:.3f} m '
          f'(same line density, {S.M_B*L_t/S.L_B:.2f} kg)')
    out = []; fails = 0
    for zeta in (0.005, 0.03):
        ws = W_E*np.linspace(0.7, 1.3, 6001)
        for sig in (0.005, 0.02, 0.1):
            for name, dev in devs.items():
                r = minimize_scalar(lambda lc: -gen_power(dev, math.exp(lc), OM0, sig, zeta, ws)[0], bounds=(-14, 3),
                                    method='bounded', options={'xatol': 1e-4})
                c = math.exp(r.x); P, Pin, xr = gen_power(dev, c, OM0, sig, zeta, ws)
                Oms = OM0*(1 + 0.103*np.linspace(-3, 3, 25)); wts = np.exp(-0.5*np.linspace(-3, 3, 25)**2); wts /= wts.sum()
                Pw = float(np.sum(wts*np.array([gen_power(dev, c, O, sig, zeta, ws)[0] for O in Oms])))
                gen_power(dev, c, OM0, sig, zeta, ws)
                ok = P <= Pin*(1 + 1e-6)
                fails += not ok
                print(f"{'PASS' if ok else 'FAIL'} zeta {zeta*100:.1f} %, tip rms {sig:.3f} m, {name}: shaking harvest {P*1e3:9.3f} mW "
                      f"of {Pin*1e3:9.1f} mW fed into the blade; tip rms with device {xr*1e3:.2f} mm; with speed wander "
                      f"{Pw*1e3:9.3f} mW", flush=True)
                out.append(dict(zeta=zeta, sig_tip=sig, device=name, c=c, P=P, P_in=Pin, x_rms=xr, P_wander=Pw, q_rms=gen_power.qrms))
                print(f'      rod swing rms {gen_power.qrms:.3f} rad')
    meta = dict(m_e=M_E, f_e=T5.F_EDGE_SYS, Phi_p=PHI, dPhi_p=PHID, r_p=RP, Om0=OM0, L_tuned=L_t, m_tuned=S.M_B*L_t/S.L_B)
    json.dump(dict(meta=meta, rows=out), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L3_shake2.json'), 'w'), indent=1)
    print('ALL PASS' if fails == 0 else f'{fails} FAIL')
