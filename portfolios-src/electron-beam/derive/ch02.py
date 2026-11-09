"""Project 07 · chapter 2 · symbolic and numerical checks of every formula derived on the page.

    python3 derive/ch02.py            runs every check, prints PASS/FAIL lines, writes data/ch02/derive_results.json

text/ch02.py reads that file: the check table on the page, and the numbers quoted in the text that come from these checks,
are the output of this script. Each check is either an exact SymPy identity or a numerical test against the quadrature in ref/ch02.py.
"""
import json, math, os, sys
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
import importlib.util
_spec = importlib.util.spec_from_file_location('eb_ref_ch02', os.path.join(EB, 'ref', 'ch02.py'))   # same stem as this file: load by path
R = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(R)

OUT = {'checks': [], 'numbers': {}}


def check(cid, title, ok, detail):
    OUT['checks'].append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + cid + '  ' + title + '  |  ' + detail)
    return ok


pos = dict(positive=True)
e, m, hb, eps0, F, phi, x, kT, w, d, h, hP = sp.symbols('e m hbar epsilon_0 F phi x kT w d h h_P', **pos)

# ------------------------------------------------------------------ C1: the Schottky-Nordheim barrier, its roots and the scaled field f
Q0 = e ** 2 / (16 * sp.pi * eps0)
U = phi - e * F * x - Q0 / x
roots = sp.solve(sp.Eq(U, 0), x)
disc = sp.simplify(phi ** 2 - 4 * e * F * Q0)
f_sym = sp.simplify(4 * e * F * Q0 / phi ** 2)
ok = sp.simplify(f_sym - e ** 3 * F / (4 * sp.pi * eps0 * phi ** 2)) == 0
r_minus = (phi - sp.sqrt(disc)) / (2 * e * F)
ok &= all(sp.simplify(U.subs(x, r)) == 0 for r in (r_minus, (phi + sp.sqrt(disc)) / (2 * e * F)))
check('C1', 'roots of U(x)=0 are x = phi(1 ∓ sqrt(1-f))/(2eF) with f = e^3 F/(4 pi eps0 phi^2)', ok, 'exact (SymPy): U vanishes at both roots; discriminant = phi^2 (1 - f)')

# ------------------------------------------------------------------ C2: Schottky lowering is the maximum of the barrier
xm = sp.solve(sp.diff(U, x), x)[0]
Umax = sp.simplify(U.subs(x, xm))
ok = sp.simplify(Umax - (phi - sp.sqrt(e ** 3 * F / (4 * sp.pi * eps0)))) == 0
dphi_eV = R.schottky_lowering(1e9) / R.eV
check('C2', 'barrier maximum: x_m = sqrt(Q0/eF), U_max = phi - sqrt(e^3 F/(4 pi eps0))', ok,
      f'exact; Δφ = {dphi_eV:.4f} eV at F = 1 V/nm (= 1.1999 eV (V/nm)^-1/2 × sqrt(F), Forbes constant c = 1.199985)')
OUT['numbers']['dphi_1Vnm_eV'] = dphi_eV
OUT['numbers']['cS_eV_per_sqrtVnm'] = dphi_eV

# ------------------------------------------------------------------ C3: triangular barrier, WKB exponent and the constant b
Gtri = 2 / hb * sp.integrate(sp.sqrt(2 * m * (phi - e * F * x)), (x, 0, phi / (e * F)))
b_sym = 4 * sp.sqrt(2 * m) / (3 * hb * e)
ok = sp.simplify(Gtri - b_sym * phi ** sp.Rational(3, 2) / F) == 0
b_SI = R.bFN
b_eV = b_SI * (R.eV ** 1.5) / 1e9
check('C3', 'triangular barrier: G = (2/ħ)∫sqrt(2m(φ-eFx))dx = b φ^{3/2}/F with b = 4 sqrt(2m)/(3 ħ e)', ok,
      f'exact; b = {b_eV:.6f} eV^-3/2 V/nm (Forbes: 6.830890)')
OUT['numbers']['b_eV_Vnm'] = b_eV

# ------------------------------------------------------------------ C4: supply function
E, mu = sp.symbols('E mu', real=True)
lhs = sp.diff(kT * sp.log(1 + sp.exp(-w / kT)), w)
ok = sp.simplify(lhs + 1 / (1 + sp.exp(w / kT))) == 0           # d/dw [kT ln(1+e^{-w/kT})] = -f(w)  so  ∫_w^∞ f dE = kT ln(1+e^{-w/kT})
pref = sp.simplify(2 * sp.pi * 2 * m / h ** 3 - 4 * sp.pi * m / h ** 3) == 0      # 2 spins x pi x 2m / h^3
ok &= pref
check('C4', 'supply function N(w) = (4 pi m kT/h^3) ln(1+e^{-w/kT})', ok, 'exact: derivative of kT ln(1+e^{-w/kT}) is -f(w); spin 2 × d^2p_t = pi·2m dε_t gives 4πm/h^3')

# ------------------------------------------------------------------ C5: zero-temperature current density, linearised exponent
Iint = sp.integrate((-w) * sp.exp(w / d), (w, -sp.oo, 0))
ok = sp.simplify(Iint - d ** 2) == 0
t = sp.symbols('t', positive=True)
d_expr = hb * e * F / (2 * sp.sqrt(2 * m * phi) * t)
J0 = 4 * sp.pi * m * e * d_expr ** 2 / h ** 3
J0_target = e ** 3 * F ** 2 / (8 * sp.pi * h * phi * t ** 2)
ok &= sp.simplify((J0 - J0_target).subs(hb, h / (2 * sp.pi))) == 0
check('C5', 'T=0: J = e (4πm/h^3) d^2 e^{-G_F} with d = ħeF/(2 sqrt(2mφ) t) equals e^3F^2/(8π h φ t^2) e^{-G_F}', ok, 'exact: ∫(-w)e^{w/d}dw = d^2, then algebra with ħ = h/2π')

# ------------------------------------------------------------------ C6: t = v - (4/3) f v'  gives Forbes' t(f); and dG/dφ identity
f = sp.symbols('f', positive=True)
vF = 1 - f + f * sp.log(f) / 6
tF_sym = sp.simplify(vF - sp.Rational(4, 3) * f * sp.diff(vF, f))
ok = sp.simplify(tF_sym - (1 + f / 9 - f * sp.log(f) / 18)) == 0
c, Fs, ph = sp.symbols('c F_s phi_s', positive=True)
vv = sp.Function('v')
G = sp.symbols('b', positive=True) * ph ** sp.Rational(3, 2) * vv(c * Fs / ph ** 2) / Fs
dG = sp.diff(G, ph)
fexpr = c * Fs / ph ** 2
vp = sp.Subs(sp.diff(vv(sp.Symbol('z')), sp.Symbol('z')), sp.Symbol('z'), fexpr).doit()
target = sp.Rational(3, 2) * sp.symbols('b', positive=True) * sp.sqrt(ph) / Fs * (vv(fexpr) - sp.Rational(4, 3) * fexpr * vp)
ok &= sp.simplify(sp.expand(dG - target)) == 0
check('C6', 'dG/dφ = (3/2) b sqrt(φ) t(f)/F with t = v - (4/3) f dv/df; for v = 1 - f + (f/6) ln f this is t = 1 + f/9 - (f/18) ln f', ok, 'exact (chain rule, f ∝ F/φ^2)')

# ------------------------------------------------------------------ C6b: slope of the FN plot: d/d(1/V)[ (1/V) v(c/(1/V)) ] = v - f v' = s(f) = 1 - f/6 for Forbes' v
X_, c_ = sp.symbols('X c', positive=True)
fX = c_ / X_                                    # f = c V = c / X with X = 1/V
vX = 1 - fX + fX * sp.log(fX) / 6
sX = sp.simplify(sp.diff(X_ * vX, X_))
ok = sp.simplify(sX - (1 - fX / 6)) == 0
check('C6b', 'FN plot slope: d[(1/V) v(f)]/d(1/V) = v - f v\' = s(f) = 1 - f/6 for v = 1 - f + (f/6) ln f (f ∝ V)', ok, 'exact (SymPy); the slope of ln(I/V^2) against 1/V is -b φ^{3/2} ζ s(f)')

# ------------------------------------------------------------------ C7: numerical: exact v(f) from the quadrature, Forbes' approximation error, and the slope identity
fs = np.linspace(0.005, 0.995, 199)
err = max(abs(R.v_exact(x_) - R.v_forbes(x_)) for x_ in fs)
relerr = max(abs(R.v_exact(x_) - R.v_forbes(x_)) / R.v_exact(x_) for x_ in fs)
ok = abs(err - 0.0024) < 0.0002 and R.v_exact(1e-6) > 0.99999 and abs(R.v_exact(0.999)) < 0.01
check('C7', 'quadrature v(f) against Forbes 2006 approximation 1 - f + (f/6) ln f', ok, f'max |Δv| = {err:.5f} (Forbes quotes 0.0024); v(10^-6) = {R.v_exact(1e-6):.6f} -> 1; v(1) = 0')
OUT['numbers']['v_max_abs_err'] = err
OUT['numbers']['v_284'] = R.v_exact(0.284)
OUT['numbers']['vF_284'] = R.v_forbes(0.284)
# numerical dG/dphi vs formula
phi0, F0 = 4.5 * R.eV, 4e9
dphi_step = 1e-4 * R.eV
num = (R.barrier_G(F0, phi0 + dphi_step, 64) - R.barrier_G(F0, phi0 - dphi_step, 64)) / (2 * dphi_step)
f0 = R.scaled_field(F0, phi0)
frm = 1.5 * R.bFN * math.sqrt(phi0) / F0 * (R.v_exact(f0) - 4 / 3 * f0 * (R.v_exact(f0 + 1e-5) - R.v_exact(f0 - 1e-5)) / 2e-5)
frm_F06 = 1.5 * R.bFN * math.sqrt(phi0) / F0 * R.t_forbes(f0)
check('C8', 'numerical dG/dφ (central difference of the quadrature) equals (3/2) b sqrt(φ) t(f)/F', abs(num / frm - 1) < 1e-4 and abs(num / frm_F06 - 1) < 5e-3,
      f'F = 4 V/nm, φ = 4.5 eV: {num:.6e} vs exact t {frm:.6e} (agree to {abs(num / frm - 1):.1e}) vs Forbes t(f) {frm_F06:.6e} (the approximation t(f) is {abs(frm_F06 / frm - 1) * 100:.2f} % off) J^-1')
OUT['numbers']['t_approx_err_284'] = abs(frm_F06 / frm - 1)
OUT['numbers']['t_exact_agree'] = abs(num / frm - 1)

# ------------------------------------------------------------------ C9: temperature factor, Murphy-Good: J(T)/J(0) = (pi kT/d)/sin(pi kT/d)
mp.mp.dps = 30
kTv, dv = mp.mpf('0.0259'), mp.mpf('0.18')
num = mp.quad(lambda ww: mp.log(1 + mp.e ** (-ww / kTv)) * mp.e ** (ww / dv), [-40 * dv, 0, 40 * kTv])
closed = dv * mp.pi / mp.sin(mp.pi * kTv / dv)
ok = abs(num / closed - 1) < 1e-6
check('C9', '∫ ln(1+e^{-w/kT}) e^{w/d} dw = π d / sin(π kT/d)  (so J(T)/J(0) = (π kT/d)/sin(π kT/d))', ok, f'mpmath quadrature {mp.nstr(num, 10)} vs closed form {mp.nstr(closed, 10)} (kT=25.9 meV, d=0.18 eV)')

# ------------------------------------------------------------------ C10: Richardson-Dushman
AR = 4 * math.pi * R.me * R.e * R.kB ** 2 / R.h ** 3
Tn, ph_ = sp.symbols('T phi_w', positive=True)
kBs = sp.symbols('k_B', positive=True)
thermionic = sp.integrate(4 * sp.pi * m * kBs * Tn / h ** 3 * sp.exp(-w / (kBs * Tn)), (w, ph_, sp.oo))   # ln(1+z) ≈ z for w >> kT
ok = sp.simplify(thermionic - 4 * sp.pi * m * (kBs * Tn) ** 2 / h ** 3 * sp.exp(-ph_ / (kBs * Tn))) == 0 and abs(AR / 1.2017e6 - 1) < 1e-3
check('C10', 'thermionic limit (D=1 above the top): J = A_R T^2 exp(-φ/kT), A_R = 4π m e k_B^2/h^3', ok, f'A_R = {AR / 1e6:.5f}×10⁶ A m⁻² K⁻² (textbook 1.2017×10⁶)')
OUT['numbers']['A_R'] = AR

# ------------------------------------------------------------------ C11: unified model against analytic limits (cold FN and Richardson-Schottky)
rows = []
for Fnm in (3.0, 4.0, 5.0):
    mdl = R.emission_model(Fnm * 1e9, 4.5 * R.eV, 300)
    rows.append((Fnm, mdl['J'], R.j_fn(Fnm * 1e9, 4.5 * R.eV, 300)))
worst_cfe = max(abs(a / b - 1) for _, a, b in rows[1:])
th = R.emission_model(1e8, 4.5 * R.eV, 2800)
rs = R.j_schottky(1e8, 2800, 4.5 * R.eV)
check('C11', 'full integral model (exact WKB, any T) against the analytic FN formula and against Richardson-Schottky', worst_cfe < 0.03 and abs(th['J'] / rs - 1) < 0.02,
      f'cold, 300 K, 4-5 V/nm: full/analytic = ' + ', '.join(f'{a / b:.4f}' for _, a, b in rows) + f' (3, 4, 5 V/nm); 2800 K, 0.1 V/nm: full/RS = {th["J"] / rs:.4f}')
OUT['numbers']['cfe_ratio_3'], OUT['numbers']['cfe_ratio_4'], OUT['numbers']['cfe_ratio_5'] = [a / b for _, a, b in rows]
OUT['numbers']['thermionic_ratio'] = th['J'] / rs

# ------------------------------------------------------------------ C12: integration by parts, current from supply function equals current from energy distribution
mdl = R.emission_model(4e9, 4.5 * R.eV, 300)
rat = mdl['J_check'] / mdl['J']
OUT['numbers']['C12_ratio'] = rat
check('C12', 'J = e∫N(w)D(w)dw equals e(4πm/h^3)∫P(ε)dε  (integration by parts: P = f(ε)∫^ε D dw)', abs(rat - 1) < 1e-4, f'ratio {rat:.6f} at 4 V/nm, 300 K')

# ------------------------------------------------------------------ C13: energy spread
d_ = mdl['d'] / R.eV
kT_ = R.kB * 300 / R.eV
eps = np.linspace(-1.5, 0.5, 400001)
Pn = np.exp(eps / d_) / (1 + np.exp(eps / kT_))
ip = Pn.argmax(); half = Pn[ip] / 2
lft = eps[:ip][np.argmax(Pn[:ip] >= half)]
rgt = eps[ip:][np.argmax(Pn[ip:] <= half)]
fwhm_lin = rgt - lft
peak_eps = kT_ * math.log(kT_ / (d_ - kT_))
check('C13', 'energy distribution of the cold source: P(ε) ∝ e^{ε/d}/(1+e^{ε/kT}), peak at ε = kT ln(kT/(d-kT)), FWHM from its two half-height roots',
      abs(fwhm_lin * R.eV / mdl['fwhm'] - 1) < 0.03 and abs(eps[ip] - peak_eps) < 1e-4,
      f'linearised exponent: FWHM {fwhm_lin:.4f} eV, peak {eps[ip]:.4f} eV (formula {peak_eps:.4f}); full model: {mdl["fwhm"] / R.eV:.4f} eV')
OUT['numbers']['fwhm_cfe_linear_eV'] = fwhm_lin
OUT['numbers']['fwhm_cfe_full_eV'] = mdl['fwhm'] / R.eV
OUT['numbers']['d_cfe_eV'] = d_
OUT['numbers']['peak_cfe_eV'] = peak_eps

# ------------------------------------------------------------------ C14: brightness
Br_cold = mdl['J'] / (math.pi * d_)     # A m^-2 sr^-1 V^-1 : B_r = J / (pi d[eV]) in the cold limit
check('C14', 'reduced brightness B_r = (e/π) j(ε_t=0); cold limit j(ε_t) = (J/d)e^{-ε_t/d} gives B_r = J/(π d[eV])', abs(Br_cold / mdl['B_r'] - 1) < 0.06,
      f'4 V/nm: J/(π d) = {Br_cold:.4e}, full model {mdl["B_r"]:.4e} A m^-2 sr^-1 V^-1 (ratio {Br_cold / mdl["B_r"]:.3f})')
OUT['numbers']['Br_cold_formula'] = Br_cold
OUT['numbers']['Br_cold_model'] = mdl['B_r']

# ------------------------------------------------------------------ C15: Hertz-Knudsen from the Maxwell-Boltzmann distribution
n_, mg, T_ = sp.symbols('n m_g T', positive=True)
vx, vy, vz = sp.symbols('v_x v_y v_z', real=True)
fMB = (mg / (2 * sp.pi * kBs * T_)) ** sp.Rational(3, 2) * sp.exp(-mg * (vx ** 2 + vy ** 2 + vz ** 2) / (2 * kBs * T_))
flux = n_ * sp.integrate(sp.integrate(sp.integrate(vx * fMB, (vy, -sp.oo, sp.oo)), (vz, -sp.oo, sp.oo)), (vx, 0, sp.oo))
ok = sp.simplify(flux - n_ * sp.sqrt(kBs * T_ / (2 * sp.pi * mg))) == 0
ok &= sp.simplify((n_ * sp.sqrt(kBs * T_ / (2 * sp.pi * mg))).subs(n_, sp.Symbol('p') / (kBs * T_)) - sp.Symbol('p') / sp.sqrt(2 * sp.pi * mg * kBs * T_)) == 0
check('C15', 'Hertz-Knudsen flux Φ = n sqrt(kT/2πm) = p/sqrt(2π m kT) from the Maxwell-Boltzmann distribution', ok, 'exact: ∫_{v_x>0} v_x f d^3v, then n = p/kT')
phi_CO = R.hk_flux(1e-9, 300, 28.0)
phi_H2 = R.hk_flux(1e-9, 300, 2.016)
OUT['numbers']['flux_CO_1e-9Pa'] = phi_CO
OUT['numbers']['flux_H2_1e-9Pa'] = phi_H2
Ns = 1.0e19
OUT['numbers']['t_ML_CO_1e-9Pa_s'] = Ns / phi_CO
OUT['numbers']['t_ML_H2_1e-9Pa_s'] = Ns / phi_H2
a_lat = 0.3165e-9
OUT['numbers']['Ns_W_lattice'] = 1 / a_lat ** 2

# ------------------------------------------------------------------ C16: coverage rate equation
th = sp.Function('theta')
tt, a, kd, th0 = sp.symbols('t a k_d theta_0', positive=True)
sol = sp.dsolve(sp.Eq(th(tt).diff(tt), a * (1 - th(tt)) - kd * th(tt)), th(tt), ics={th(0): th0})
mine = a / (a + kd) + (th0 - a / (a + kd)) * sp.exp(-(a + kd) * tt)
ok = sp.simplify(sol.rhs - mine) == 0
check('C16', 'dθ/dt = a(1-θ) - k_d θ has the solution θ(t) = θ∞ + (θ0 - θ∞) e^{-(a+k_d)t}, θ∞ = a/(a+k_d)', ok, 'exact (SymPy dsolve)')

# ------------------------------------------------------------------ C17: asymptote of a trajectory in a radial 1/r potential (impact parameter), numerical
def asymptote_impact(r0_nm, eps_t_eV, V, E_r_eV=0.5):
    """Trajectory of an electron leaving a sphere of radius r0 (potential energy U = eV r0/r, 0 at infinity) with radial kinetic energy E_r and
    transverse energy eps_t; RK4 in the plane; returns the distance of the final straight line from the centre and the exact L/p_inf."""
    r0 = r0_nm * 1e-9
    K_ = R.e * V * r0
    Et, Er = eps_t_eV * R.eV, E_r_eV * R.eV
    mass = R.me
    L = r0 * math.sqrt(2 * mass * Et)
    p_inf = math.sqrt(2 * mass * (R.e * V + Er + Et))
    pos = np.array([r0, 0.0])
    vel = np.array([math.sqrt(2 * Er / mass), L / (mass * r0)])
    def acc(p):
        rr = np.hypot(*p)
        return (K_ / rr ** 3) * p / mass
    steps = 0
    while np.hypot(*pos) < 2e-3:                 # out to 2 mm: the remaining potential energy e V r0/r is then 0.025 eV of 1000 eV
        dt = 2e-3 * np.hypot(*pos) / np.hypot(*vel)
        steps += 1
        k1v = acc(pos); k1x = vel
        k2v = acc(pos + 0.5 * dt * k1x); k2x = vel + 0.5 * dt * k1v
        k3v = acc(pos + 0.5 * dt * k2x); k3x = vel + 0.5 * dt * k2v
        k4v = acc(pos + dt * k3x); k4x = vel + dt * k3v
        pos = pos + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x); vel = vel + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return abs(pos[0] * vel[1] - pos[1] * vel[0]) / np.hypot(*vel), L / p_inf

b_num, b_exact = asymptote_impact(50, 0.2, 1000.0)
b_formula = 50e-9 * math.sqrt(0.2 / 1000.0)
check('C17', 'impact parameter of the asymptote of a trajectory in a radial 1/r potential: b = L/p∞ = r sqrt(ε_t/(eV)) for eV >> ε_t (angular momentum conservation)',
      abs(b_num / b_exact - 1) < 1e-4 and abs(b_formula / b_exact - 1) < 1e-3,
      f'RK4 trajectory, r = 50 nm, ε_t = 0.2 eV, V = 1000 V: b = {b_num * 1e9:.5f} nm; L/p∞ = {b_exact * 1e9:.5f} nm; r sqrt(ε_t/eV) = {b_formula * 1e9:.5f} nm')
OUT['numbers']['b_asymptote_nm'] = b_num * 1e9
OUT['numbers']['b_exact_nm'] = b_exact * 1e9

# ------------------------------------------------------------------ the model's own numbers for the two sources and the default tip (for the text)
CFE = dict(V=1000.0, r=50e-9, k=5.0, phi=4.5 * R.eV, T=300.0)
hoC = R.handover(CFE['V'], CFE['r'], CFE['k'], CFE['phi'], CFE['T'])
SCH = dict(V=2000.0, r=0.5e-6, k=8.0, phi=2.9 * R.eV, T=1800.0)   # k chosen so that the apex field is 0.5 V/nm: an assumed operating point
hoS = R.handover(SCH['V'], SCH['r'], SCH['k'], SCH['phi'], SCH['T'])
OUT['numbers']['handover_cfe'] = hoC
OUT['numbers']['handover_schottky'] = hoS
OUT['numbers']['preset_cfe'] = CFE
OUT['numbers']['preset_schottky'] = SCH
print('hand-over, CFE preset     :', {k_: (round(v_, 4) if isinstance(v_, float) and abs(v_) > 1e-3 and abs(v_) < 1e3 else v_) for k_, v_ in hoC.items()})
print('hand-over, Schottky preset:', {k_: v_ for k_, v_ in hoS.items()})

# ------------------------------------------------------------------ overlay: Ayari et al. 2023, W<111> tip
d_ = R.load_ayari(os.path.join(EB, 'data', 'ch02', 'ayari2023_w111_iv.csv'))
m4 = (d_['run'] == 4) & (d_['sweep'] == 'down')
V4, I4 = d_['V_V'][m4], d_['I_nA'][m4] * 1e-9
slope, icpt = np.polyfit(1 / V4, np.log(I4 * 1e9 / V4 ** 2), 1)
fits = {}
for ph_ev in (4.0, 4.5, 5.0, 5.5):
    ft = R.fit_tip(V4, I4, phi_eV=ph_ev)
    Fv = V4 / ft['zeta']
    fits[ph_ev] = dict(zeta_nm=ft['zeta'] * 1e9, r_nm=ft['zeta'] * 1e9 / 5, A_nm2=ft['A'] * 1e18, rms=ft['rms_lnI'],
                       f_lo=R.scaled_field(Fv.min(), ph_ev * R.eV), f_hi=R.scaled_field(Fv.max(), ph_ev * R.eV),
                       F_lo=Fv.min() * 1e-9, F_hi=Fv.max() * 1e-9)
ft = R.fit_tip(V4, I4, phi_eV=4.5)
Jm = np.array([R.j_fn(v / ft['zeta'], 4.5 * R.eV, 300) for v in V4])
res = np.log(I4) - np.log(ft['A'] * Jm)
J0m = np.array([R.j_fn(v / ft['zeta'], 4.5 * R.eV, 0) for v in V4])
allfits = []
for run in range(1, 6):
    for sw in ('up', 'down'):
        mm = (d_['run'] == run) & (d_['sweep'] == sw)
        f_ = R.fit_tip(d_['V_V'][mm], d_['I_nA'][mm] * 1e-9)
        allfits.append(dict(run=run, sweep=sw, zeta_nm=f_['zeta'] * 1e9, A_nm2=f_['A'] * 1e18, rms=f_['rms_lnI']))
# drift: current at the same voltage, 1470 V, in successive up/down sweeps (the order in time of the sweeps is 1u,1d,2u,...)
seq = [(r, s) for r in range(1, 6) for s in ('up', 'down')]
I1470 = []
for r, s in seq:
    mm = (d_['run'] == r) & (d_['sweep'] == s) & (np.isclose(d_['V_V'], 1470.0))
    I1470.append(float(d_['I_nA'][mm][0]))
OUT['numbers']['ayari'] = dict(fn_slope_V=float(slope), fn_intercept=float(icpt), fits=fits, resid_max=float(np.abs(res).max()), resid_rms=float(res.std()),
                               resid_vs_V=[(float(v), float(r_)) for v, r_ in zip(V4, res)],
                               tcorr_lo=float((Jm / J0m).min()), tcorr_hi=float((Jm / J0m).max()), allfits=allfits, I1470_nA=I1470,
                               V=[float(v) for v in V4], I_nA=[float(i * 1e9) for i in I4])
check('C19', 'published tungsten-tip data (Ayari et al. 2023, run 4 down): plain FN line reproduces the authors’ slope and intercept; model fit with φ = 4.5 eV',
      abs(slope + 41339) < 1 and abs(icpt - 4.57) < 0.02,
      f'FN slope {slope:.1f} V, intercept {icpt:.3f} (authors: 41339 ± 73 V, 4.57 ± 0.05); model fit: ζ = {fits[4.5]["zeta_nm"]:.1f} nm, '
      f'A = {fits[4.5]["A_nm2"]:.0f} nm², rms ln I = {fits[4.5]["rms"]:.4f}, largest residual {np.abs(res).max():.3f}')

# ------------------------------------------------------------------ time to monolayer table, pressure scan (for the figure and the text)
scan = []
for pPa in (1e-4, 1e-6, 1e-8, 1e-9, 1e-10):
    scan.append(dict(p=pPa, t_ML_CO=Ns / R.hk_flux(pPa, 300, 28.0), t_ML_H2=Ns / R.hk_flux(pPa, 300, 2.016)))
OUT['numbers']['ml_scan'] = scan
# Cho et al. 2014: pressure x damping time
cho = [dict(p=2e-8, tau90_min=15.0), dict(p=2.5e-9, tau90_min=105.0), dict(p=7e-10, tau90_min=450.0)]
for c_ in cho:
    c_['p_tau'] = c_['p'] * c_['tau90_min']
OUT['numbers']['cho'] = cho
OUT['numbers']['cho_C_CH_Pa_min'] = 1.93e-7
print('--- Cho et al. 2014: p·τ90 =', ', '.join(f"{c_['p_tau']:.2e}" for c_ in cho), 'Pa·min')

n_pass = sum(c_['ok'] for c_ in OUT['checks'])
OUT['summary'] = f'{n_pass} of {len(OUT["checks"])} checks pass'
print(OUT['summary'])
with open(os.path.join(EB, 'data', 'ch02', 'derive_results.json'), 'w') as fh:
    json.dump(OUT, fh, indent=1, default=float)
sys.exit(0 if n_pass == len(OUT['checks']) else 1)
