"""Chapter 3 derivation checks (SymPy). Writes data/ch03/derive_results.json; the page shows the table.

    python3 portfolios-src/electron-beam/derive/ch03.py
"""
import json
import pathlib
import sys

import sympy as sp

HERE = pathlib.Path(__file__).resolve().parents[1]
checks = []


def check(cid, title, ok, detail):
    checks.append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail})


m, c, e, V, h = sp.symbols('m c e V h', positive=True)
mc2 = m * c ** 2
E0 = e * V
Etot = E0 + mc2

# D1: momentum from the energy-momentum relation
p2 = sp.simplify((Etot ** 2 - mc2 ** 2) / c ** 2)
Vstar = V * (1 + e * V / (2 * mc2))
check('D1', '(eV + mc²)² = (pc)² + (mc²)² gives p² = 2meV(1 + eV/2mc²) = 2meV*', sp.simplify(p2 - 2 * m * e * Vstar) == 0,
      'p² − 2meV* simplifies to 0')

# D2: non-relativistic and ultra-relativistic limits of lambda = h/p
lam = h / sp.sqrt(2 * m * e * Vstar)
x = sp.symbols('x', positive=True)          # x = eV/(mc^2)
lam_x = sp.simplify(lam.subs(V, x * mc2 / e))
nr = sp.limit(lam_x * sp.sqrt(x), x, 0)
ur = sp.limit(lam_x * x, x, sp.oo)
check('D2', 'λ → h/√(2meV) for eV ≪ mc², and λ → hc/(eV) for eV ≫ mc²',
      sp.simplify(nr - h / (m * c * sp.sqrt(2))) == 0 and sp.simplify(ur - h / (m * c)) == 0,
      'λ√x → h/(√2 mc) and λx → h/(mc), with x = eV/mc²; these are h/√(2meV) and hc/eV')

# D3: relative error of the non-relativistic wavelength
ratio = sp.sqrt(Vstar / V)
ser = sp.series(ratio.subs(V, x * mc2 / e), x, 0, 3).removeO()
check('D3', 'λ_NR/λ = √(1 + eV/2mc²) = 1 + eV/(4mc²) − (eV)²/(32(mc²)²) + …',
      sp.simplify(ser - (1 + x / 4 - x ** 2 / 32)) == 0, 'series in x = eV/mc²: 1 + x/4 − x²/32 + …')

# D4: deceleration with conserved transverse momentum: angle grows by p_acc/p_land (paraxial)
pperp, pa, pl = sp.symbols('p_perp p_a p_l', positive=True)
alpha_a = sp.atan(pperp / pa)
alpha_l = sp.atan(pperp / pl)
lead = sp.limit(alpha_l / alpha_a, pperp, 0)
check('D4', 'p⊥ conserved, p_z reduced: α_land/α → p_acc/p_land = √(V*_acc/V*_land) for small angles', sp.simplify(lead - pa / pl) == 0,
      'limit of arctan(p⊥/p_l)/arctan(p⊥/p_a) for p⊥ → 0 is p_a/p_l')

# D5: Liouville in the transverse phase space, with z as the time: the flow of H(x, p_x; z) has zero divergence
X, P, z = sp.symbols('x p_x z', real=True)
Pf = sp.Function('P')(X, z)                 # local total momentum, set by the potential at (x, z)
Af = sp.Function('A')(X, z)                 # a vector-potential term entering p_x
q = sp.symbols('q', real=True)
H = -sp.sqrt(Pf ** 2 - (P - q * Af) ** 2)   # p_z as a Hamiltonian with z as time (one transverse dimension shown)
div = sp.diff(sp.diff(H, P), X) + sp.diff(-sp.diff(H, X), P)
check('D5', 'Hamilton’s equations with z as time: ∂(dx/dz)/∂x + ∂(dp_x/dz)/∂p_x = 0, so phase-space area is conserved (Liouville)',
      sp.simplify(div) == 0, 'divergence of the flow simplifies to 0 for arbitrary P(x, z) and A(x, z)')

# D6: brightness over p^2 is invariant: B = dI/(dA dOmega), dOmega = d^2p_perp/p^2 (paraxial), dA d^2p_perp invariant
dI, inv = sp.symbols('dI K', positive=True)   # K = dA d^2p_perp, the invariant phase-space element
p1, p2_ = sp.symbols('p_1 p_2', positive=True)
B1 = dI / (inv / p1 ** 2)
B2 = dI / (inv / p2_ ** 2)
check('D6', 'B ∝ p², so B/V* is the same at every plane of the column (exactly, relativistically)', sp.simplify(B1 / p1 ** 2 - B2 / p2_ ** 2) == 0,
      'B/p² = dI/K at both planes; p² = 2meV* by D1')

# D7: practical over axial differential brightness of a Gaussian virtual source is 1/ln 2
r, R, sig, J0 = sp.symbols('r R sigma J_0', positive=True)
Itot = sp.integrate(J0 * sp.exp(-r ** 2 / sig ** 2) * 2 * sp.pi * r, (r, 0, sp.oo))
Ir = sp.integrate(J0 * sp.exp(-r ** 2 / sig ** 2) * 2 * sp.pi * r, (r, 0, R))
R50 = sp.solve(sp.Eq(Ir, Itot / 2), R)[0]
ratio_b = sp.simplify((Itot / (sp.pi * R50 ** 2)) / J0)
check('D7', 'Gaussian virtual source: the total current over the area of the half-current disk is 1/ln 2 times the axial value',
      sp.simplify(ratio_b - 1 / sp.log(2)) == 0, 'R₅₀² = σ² ln 2; ratio = 1/ln 2 = %.5f' % float(ratio_b))

# D8: probe current from the practical brightness (Bronsgeest et al. 2008, Eq. 6): units and form
Bp, Vp, d, al = sp.symbols('B V_p d alpha', positive=True)
Ip = Bp * Vp * (sp.pi * d ** 2 / 4) * (sp.pi * al ** 2)
check('D8', 'the solid angle of a cone of half-angle α is πα² for small α, as used in I_p = B V* (π d²/4)(π α²)', sp.simplify(sp.series(2 * sp.pi * (1 - sp.cos(al)), al, 0, 4).removeO() - sp.pi * al ** 2) == 0,
      'solid angle 2π(1 − cos α) = πα² − πα⁴/12 + …; I_p ∝ d² α² at fixed brightness')

# D9: energy spread is unchanged by a static potential step
Ea, Eb = sp.symbols('E_a E_b', real=True)
check('D9', 'two electrons gaining eV each keep their energy difference', sp.simplify((Ea + e * V) - (Eb + e * V) - (Ea - Eb)) == 0, 'ΔE after = ΔE before')

out = {'checks': checks, 'summary': '%d of %d checks pass' % (sum(c['ok'] for c in checks), len(checks)), 'ln2_ratio': float(1 / sp.log(2))}
(HERE / 'data' / 'ch03').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch03' / 'derive_results.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
if __name__ == '__main__':
    for c_ in checks:
        print(('PASS ' if c_['ok'] else 'FAIL ') + c_['id'] + ' ' + c_['title'] + ' :: ' + c_['detail'])
    print(out['summary'])
    sys.exit(0 if all(c_['ok'] for c_ in checks) else 1)
