"""Chapter 4 derivation checks (SymPy) and numerical cross-checks of the lens solver. Writes data/ch04/derive_results.json.

    python3 portfolios-src/electron-beam/derive/ch04.py
"""
import json
import math
import pathlib
import sys

import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from ref import ch04 as R  # noqa: E402
from ref.core import with_defaults  # noqa: E402

checks = []


def check(cid, title, ok, detail):
    checks.append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail})


z, r, a, B0, k, mu0, NI = sp.symbols('z r a B_0 k mu_0 NI', positive=True)
Bf = sp.Function('B')(z)

# L1: Ampere along the axis for the bell field
Bg = B0 / (1 + (z / a) ** 2)
check('L1', '∫B dz over the axis = πaB₀, so Ampère (∮B·dl = μ₀NI, the return path far away) gives B₀ = μ₀NI/(πa)',
      sp.simplify(sp.integrate(Bg, (z, -sp.oo, sp.oo)) - sp.pi * a * B0) == 0, '∫ B₀/(1+z²/a²) dz = πaB₀')

# L2: the off-axis expansion satisfies div B = 0 and curl B = 0 to the order kept
Bz = Bf - r ** 2 / 4 * sp.diff(Bf, z, 2) + r ** 4 / 64 * sp.diff(Bf, z, 4)
Br = -r / 2 * sp.diff(Bf, z) + r ** 3 / 16 * sp.diff(Bf, z, 3)
div = sp.expand(sp.diff(r * Br, r) / r + sp.diff(Bz, z))
curl = sp.expand(sp.diff(Br, z) - sp.diff(Bz, r))
check('L2', 'B_z = B − r²B″/4 + r⁴B⁗/64, B_r = −rB′/2 + r³B‴/16 satisfy div B = 0 and curl B = 0 up to the next order',
      sp.Poly(div, r).degree() >= 4 and all(sp.simplify(div.coeff(r, n)) == 0 for n in range(4)) and all(sp.simplify(curl.coeff(r, n)) == 0 for n in range(4)),
      'in div B and curl B the coefficients of r⁰, r¹, r² and r³ are all 0; what remains starts at order r⁴')

# L3: derivatives of the bell field used by the code
u = z / a
d1, d2, d3 = (sp.diff(Bg, z, n) for n in (1, 2, 3))
code = (-2 * B0 * u / (a * (1 + u ** 2) ** 2), B0 * (6 * u ** 2 - 2) / (a ** 2 * (1 + u ** 2) ** 3), 24 * B0 * u * (1 - u ** 2) / (a ** 3 * (1 + u ** 2) ** 4))
check('L3', 'B′, B″, B‴ of the bell field as coded in physics/ch04.js', all(sp.simplify(x - y) == 0 for x, y in zip((d1, d2, d3), code)), 'differences simplify to 0')

# L4: Busch: canonical angular momentum p_theta = gamma m r^2 thetadot + q r A_theta, A_theta = r B/2 near the axis.
g, m, e, thd = sp.symbols('gamma m e thetadot', positive=True)
q = -e
ptheta = g * m * r ** 2 * thd + q * r * (r * Bf / 2)
sol = sp.solve(sp.Eq(ptheta, 0), thd)[0]
check('L4', 'Busch: an electron that starts on the axis (p_θ = 0) turns at θ̇ = eB/(2γm), the Larmor rate', sp.simplify(sol - e * Bf / (2 * g * m)) == 0,
      'solving p_θ = 0 for θ̇ gives eB(z)/(2γm)')

# L5: in the frame turning at the Larmor rate the radial force is -e^2 B^2 r / (4 gamma m), so r'' = -(e^2 B^2 / 4 p^2) r = -(e/8mV*) B^2 r
p, Vs = sp.symbols('p V^*', positive=True)
check('L5', 'e²B²/(4p²) with p² = 2meV* equals eB²/(8mV*)', sp.simplify((e ** 2 * Bf ** 2 / (4 * p ** 2)).subs(p, sp.sqrt(2 * m * e * Vs)) - e * Bf ** 2 / (8 * m * Vs)) == 0,
      'the coefficient η B² of the paraxial equation')

# L6: Glaser's exact solution, z = a cot(phi), r = sin(omega (pi - phi)) / sin(phi), omega^2 = 1 + k^2
ph = sp.symbols('phi', positive=True)
w = sp.sqrt(1 + k ** 2)
rr = sp.sin(w * (sp.pi - ph)) / sp.sin(ph)
zz = a * sp.cot(ph)
dzdph = sp.diff(zz, ph)
r1 = sp.diff(rr, ph) / dzdph
r2 = sp.diff(r1, ph) / dzdph
resid = sp.simplify(r2 + k ** 2 * a ** 2 / (a ** 2 + zz ** 2) ** 2 * rr)
check('L6', 'r = sin(ω(π−ψ))/sin ψ with z = a cot ψ (any constant factor) solves r″ + k²a²r/(a²+z²)² = 0 when ω² = 1 + k²', resid == 0, 'residual simplifies to 0')

# L7: focal length from it: far behind the lens r -> sin(omega pi) z/(omega a) + ..., so f = -omega a / sin(omega pi); thin-lens limit
f_ex = -w * a / sp.sin(w * sp.pi)
lim = sp.limit(f_ex * k ** 2, k, 0)
check('L7', 'f = −ωa/sin(ωπ); for a weak lens 1/f → πk²/(2a) = η∫B²dz (the thin-lens formula)', sp.simplify(lim - 2 * a / sp.pi) == 0,
      'k²f → 2a/π as k → 0; η∫B²dz = ηB₀²aπ/2 = πk²/(2a)')

# L8: any paraxial ray, also a skew one. w = x + i y obeys w'' = i kappa (2 B w' + B' w) with kappa = e/(2p) (q = -e, d/dt = v d/dz);
# in the frame turned by theta(z), theta' = kappa B, the substitution w = u exp(i theta) gives u'' = -kappa^2 B^2 u, and kappa^2 = e/(8 m V*)
kap = sp.symbols('kappa', positive=True)
uf = sp.Function('u')(z)
th = sp.Function('theta')(z)
wf = uf * sp.exp(sp.I * th)
lhs = sp.diff(wf, z, 2) - sp.I * kap * (2 * Bf * sp.diff(wf, z) + sp.diff(Bf, z) * wf)
res8 = sp.simplify((lhs * sp.exp(-sp.I * th)).subs(sp.Derivative(th, (z, 2)), kap * sp.diff(Bf, z)).subs(sp.Derivative(th, z), kap * Bf) - (sp.diff(uf, z, 2) + kap ** 2 * Bf ** 2 * uf))
xx, yy, vx, vy, vv = sp.symbols('x y v_x v_y v', real=True)
Bvec = sp.Matrix([-xx * sp.diff(Bf, z) / 2, -yy * sp.diff(Bf, z) / 2, Bf])
F = sp.Matrix([vx, vy, vv]).cross(Bvec)
Fw = sp.expand(F[0] + sp.I * F[1])
target = sp.expand(-sp.I * (Bf * (vx + sp.I * vy) + vv * sp.diff(Bf, z) / 2 * (xx + sp.I * yy)))
check('L8', 'all paraxial rays, skew ones too: with w = x + iy the transverse Lorentz force is (v×B)ₓ + i(v×B)ᵧ = −i[B ẇ + (vB′/2)w]; in the frame turned by θ′ = (e/2p)B, w = u e^{iθ} gives u″ = −(e/2p)²B²u',
      sp.simplify(Fw - target) == 0 and res8 == 0, 'force identity and the rotating-frame equation both simplify to 0')

# ---- numerical cross-checks at the contract defaults
p0 = with_defaults(R.INPUTS)
out = R.compute(p0)
f_formula = -out['omega_G'] * p0['a_lens'] / math.sin(out['omega_G'] * math.pi)
check('N1', 'focal length traced by the solver equals Glaser’s exact −ωa/sin(ωπ) (the solver starts its parallel ray at z = −2000a, which costs about 1/2000² relative)', abs(out['f'] / f_formula - 1) < 1e-6,
      'traced %.7f mm, formula %.7f mm' % (out['f'] * 1e3, f_formula * 1e3))

# fine paraxial ray, for the aberration integrals (own RK4, 80 000 steps in t)
a_, u_, wd_ = p0['a_lens'], p0['u_obj'], p0['WD']
Vs_ = R.vstar(p0['V_land'])
eta = R.E / (8 * R.ME * Vs_)
B0_ = out['B_0']
N = 80000
t = np.linspace(math.atan(-u_ / a_), math.atan(wd_ / a_), N + 1)
hstep = t[1] - t[0]


def rhs(tt, y):
    zz_ = a_ * np.tan(tt)
    dz = a_ / np.cos(tt) ** 2
    B = B0_ / (1 + (zz_ / a_) ** 2)
    return np.array([y[1] * dz, -eta * B * B * y[0] * dz])


Y = np.zeros((N + 1, 2))
Y[0] = (0.0, 1.0)
for i in range(N):
    y0 = Y[i]
    k1 = rhs(t[i], y0)
    k2 = rhs(t[i] + hstep / 2, y0 + hstep / 2 * k1)
    k3 = rhs(t[i] + hstep / 2, y0 + hstep / 2 * k2)
    k4 = rhs(t[i] + hstep, y0 + hstep * k3)
    Y[i + 1] = y0 + hstep / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
zg = a_ * np.tan(t)
M = 1 / abs(Y[-1, 1])
hh, hp = Y[:, 0] * M, Y[:, 1] * M                       # the ray normalised to unit slope at the image
Bv, B1v, _, _ = R.glaser(zg, B0_, a_)
em = R.E / R.ME
Cc_int = eta * np.trapezoid(Bv ** 2 * hh ** 2, zg)
Cs_int = em / (128 * Vs_) * np.trapezoid(3 * em / Vs_ * Bv ** 4 * hh ** 4 + 8 * B1v ** 2 * hh ** 4 - 8 * Bv ** 2 * hh ** 2 * hp ** 2, zg)
check('N2', 'C_c from the solver (paraxial ray at V*(1 ± 10⁻⁴)) equals the perturbation integral η∫B²h²dz (h: unit slope at the image)',
      abs(out['C_c'] / Cc_int - 1) < 1e-4, 'solver %.6f mm, integral %.6f mm' % (out['C_c'] * 1e3, Cc_int * 1e3))
check('N3', 'C_s from tracing rays through the third-order field equals the aberration integral (e/128mV*)∫[3(e/mV*)B⁴h⁴ + 8B′²h⁴ − 8B²h²h′²]dz',
      abs(out['C_s'] / Cs_int - 1) < 1e-5, 'traced %.5f mm, integral %.5f mm, ratio %.6f' % (out['C_s'] * 1e3, Cs_int * 1e3, out['C_s'] / Cs_int))
# image rotation from the Larmor rate integrated
th_int = math.sqrt(R.E / (8 * R.ME * Vs_)) * np.trapezoid(Bv, zg)
check('N4', 'image rotation √(e/8mV*)∫B dz from object to wafer: closed form in the solver against quadrature', abs(out['theta_rot'] / th_int - 1) < 1e-6,
      'solver %.6f rad, quadrature %.6f rad' % (out['theta_rot'], th_int))
# scaling of the traced miss with the angle
pm = math.sqrt(2 * R.ME * R.E * Vs_)
xe, ye = R.ray3d(B0_, a_, -R.E / pm, -u_, wd_, 1e-9)
rat = []
for ai in (1e-3, 2e-3, 4e-3, 8e-3):
    x, y = R.ray3d(B0_, a_, -R.E / pm, -u_, wd_, ai * M)
    rat.append(math.hypot(x - ai * M / 1e-9 * xe, y - ai * M / 1e-9 * ye) / ai ** 3)
check('N5', 'the traced miss grows as α³ (miss/α³ constant to 0.02 % from 1 to 8 mrad)', max(rat) / min(rat) - 1 < 2e-4,
      'miss/α³ = ' + ', '.join('%.5f mm' % (x * 1e3) for x in rat))

res = {'checks': checks, 'summary': '%d of %d checks pass' % (sum(c['ok'] for c in checks), len(checks)),
       'numbers': {'Cs_integral': Cs_int, 'Cc_integral': Cc_int, 'f_formula': f_formula, 'cs_over_a3': rat}}
(HERE / 'data' / 'ch04').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch04' / 'derive_results.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
if __name__ == '__main__':
    for c in checks:
        print(('PASS ' if c['ok'] else 'FAIL ') + c['id'] + ' ' + c['title'] + ' :: ' + c['detail'])
    print(res['summary'])
    sys.exit(0 if all(c['ok'] for c in checks) else 1)
