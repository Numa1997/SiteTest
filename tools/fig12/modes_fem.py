#!/usr/bin/env python3
"""Linear sloshing modes of the Guinness tulip pint (Fig. 12), by the finite element method.

    python3 tools/fig12/modes_fem.py check            # the cylinder against its exact answer, and a convergence table
    python3 tools/fig12/modes_fem.py tulip [h_mm ...] # the tulip at the given fill heights (default 125)

The problem (Faltinsen & Timokha, "Sloshing", 2009, ch. 4-5; Ibrahim, "Liquid Sloshing Dynamics", 2005, ch. 2):
the liquid at rest fills r <= R(z), 0 <= z <= h. Small motions without vorticity have a velocity potential phi with
    Laplace's equation          div grad phi = 0                 in the liquid,
    no flow through the glass   d phi / dn = 0                   on the wall and the floor,
    free surface                d phi / dz = kappa phi           on z = h,   kappa = omega^2 / g.
The glass is round, so phi = Phi(r, z) cos(m theta). Multiplying by a test function Psi(r, z) cos(m theta), integrating over
the liquid and integrating by parts (Green's first identity) leaves, after the common factor pi,
    int_A (Phi_r Psi_r + Phi_z Psi_z + m^2 Phi Psi / r^2) r dr dz  =  kappa int_0^R(h) Phi Psi r dr   (at z = h),
a generalised eigenproblem K x = kappa M x on the meridian section A. For m >= 1 the potential vanishes on the axis
(Phi ~ r^m); for m = 0 the axis needs nothing. M lives on the surface only, so the unknowns inside are eliminated
(Schur complement S = K_ss - K_si K_ii^-1 K_is, the discrete Dirichlet-to-Neumann map) and S x = kappa M_ss x is solved densely.
Frequencies f = sqrt(g kappa) / (2 pi). The surface elevation of a mode is proportional to Phi(r, h) cos(m theta).

Mesh: a structured triangle mesh of the unit square mapped to r = s R(z), z = t h, graded towards the free surface
(where the modes live); quadratic (P2) or linear (P1) elements. Two element orders on refined meshes are the two routes:
they must converge to the same numbers, and on the cylinder to the exact ones, k tanh(k h) with k = j'_mn / R
(j'_mn the zeros of the derivative of the Bessel function J_m).
"""
import sys, re, os, json
import numpy as np, scipy.linalg as sla, scipy.sparse.linalg as spla
from scipy.special import jnp_zeros
from skfem import MeshTri, Basis, FacetBasis, ElementTriP1, ElementTriP2, BilinearForm, Functional
from skfem.helpers import dot, grad

G = 9.81
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def glass():
    """dz and R(z) of the measured tulip, from public/scripts/guinness-glass.js (the page's own data)."""
    t = open(os.path.join(ROOT, 'public', 'scripts', 'guinness-glass.js')).read()
    dz = float(re.search(r'dz:\s*([0-9.e-]+)', t).group(1))
    R = np.array([float(v) for v in re.search(r'R:\s*\[([^\]]*)\]', t).group(1).split(',')])
    return dz, R


def profile_fn(dz, R):
    zz = dz * np.arange(len(R))
    return lambda z: np.interp(z, zz, R)


def solve(Rf, h, m, nr=24, nz=48, order=2, grade=2.0, nmodes=6):
    """Modes of harmonic m for the liquid r <= Rf(z), z <= h. Returns frequencies (Hz), kappa, and the surface shapes."""
    s = np.linspace(0, 1, nr + 1)
    t = 1 - (1 - np.linspace(0, 1, nz + 1)) ** grade        # cells shrink towards the surface t = 1
    mesh = MeshTri.init_tensor(s, t)
    p = mesh.p.copy(); z = p[1] * h; p[0] = p[0] * Rf(z); p[1] = z
    mesh = MeshTri(p, mesh.t)
    E = ElementTriP2() if order == 2 else ElementTriP1()
    ib = Basis(mesh, E)

    @BilinearForm
    def kform(u, v, w):
        r = w.x[0]
        return (dot(grad(u), grad(v)) + m * m * u * v / r ** 2) * r

    @BilinearForm
    def mform(u, v, w):
        return u * v * w.x[0]

    K = kform.assemble(ib)
    top = mesh.facets_satisfying(lambda x: x[1] > h * (1 - 1e-9))
    fb = FacetBasis(mesh, E, facets=top)
    M = mform.assemble(fb)
    sdofs = ib.get_dofs(top).flatten()
    axis = ib.get_dofs(lambda x: x[0] < 1e-12).flatten() if m >= 1 else np.array([], dtype=int)
    sdofs = np.setdiff1d(sdofs, axis)
    n = K.shape[0]
    inner = np.setdiff1d(np.arange(n), np.concatenate([sdofs, axis]))
    K = K.tocsr()
    Kss = K[sdofs][:, sdofs].toarray(); Ksi = K[sdofs][:, inner]; Kii = K[inner][:, inner].tocsc()
    lu = spla.splu(Kii)
    X = lu.solve(Ksi.T.toarray())
    S = Kss - Ksi @ X
    S = 0.5 * (S + S.T)
    Mss = M.tocsr()[sdofs][:, sdofs].toarray()
    kap, V = sla.eigh(S, Mss)
    keep = kap > 1e-8 * max(1.0, abs(kap).max())             # m = 0: drop the constant (no motion)
    kap, V = kap[keep][:nmodes], V[:, keep][:, :nmodes]
    r_s = ib.doflocs[0, sdofs]; o = np.argsort(r_s)
    # Friction in the wall's Stokes layer (Landau & Lifshitz, Fluid Mechanics, sec. 24): per unit area the mean heat is
    # (rho/2) sqrt(nu omega/2) |U_t|^2, U_t the slip the potential flow would have at the wall. Over a swing of energy
    # (rho/2) int |grad phi|^2 dV this gives the damping ratio zeta = (1/2) sqrt(nu/(2 omega)) Lambda, with
    # Lambda = int_wall |grad_t phi|^2 dS / int |grad phi|^2 dV (1/m). The angular integrals are equal on both sides.
    wall = mesh.facets_satisfying(lambda x: (x[1] < h * (1 - 1e-9)) & (x[0] > 1e-9 * h), boundaries_only=True)
    fbw = FacetBasis(mesh, E, facets=wall)

    @Functional
    def wform(w):
        u = w['u']; tr, tz = -w.n[1], w.n[0]; r = w.x[0]
        gt = u.grad[0] * tr + u.grad[1] * tz
        return (gt ** 2 + m * m * u.value ** 2 / r ** 2) * r
    shapes, c, lam = [], [], []
    for j in range(V.shape[1]):
        v = V[:, j] / V[o[-1], j]                              # the surface shape e_n, 1 at the wall
        shapes.append(v[o])
        # c_n = int x e_n dS / int e_n^2 dS (m = 1; the angular integrals give pi on both sides): with this, a push a_x drives
        # beta_n'' + omega_n^2 (1 + a_z/g) beta_n = -kappa_n c_n a_x, and a steady push tilts the surface by sum c_n e_n = x
        c.append(float(v @ Mss @ r_s / (v @ Mss @ v)) if m == 1 else 0.0)
        x = np.zeros(n); x[sdofs] = v; x[inner] = -X @ v
        lam.append(float(wform.assemble(fbw, u=fbw.interpolate(x)) / (x @ K @ x)))
    f = np.sqrt(G * kap) / (2 * np.pi)
    return dict(f=f, kappa=kap, r=r_s[o], shapes=shapes, c=np.array(c), Lam=np.array(lam), ndof=n, nsurf=len(sdofs))


def zeta(out, nu):
    w = 2 * np.pi * out['f']
    return 0.5 * np.sqrt(nu / (2 * w)) * out['Lam']


def exact_cyl(R, h, m, n):
    k = jnp_zeros(m, n) / R
    return np.sqrt(G * k * np.tanh(k * h)) / (2 * np.pi)


def check():
    R, h = 0.040, 0.100
    print('Cylinder R = 40 mm, h = 100 mm (the page note checks the 3D solver on the same case: 3.382 Hz).')
    print('Exact f_mn = sqrt(g k tanh kh)/2pi, k = jp_mn/R:')
    for m in (0, 1, 2):
        print(f'  m = {m}: ' + ', '.join(f'{v:.5f}' for v in exact_cyl(R, h, m, 3)) + ' Hz')
    Rf = lambda z: np.full_like(z, R)
    print('Finite elements, relative error of the first three modes (m = 1, then m = 0 and 2 on the finest mesh):')
    ex = exact_cyl(R, h, 1, 3)
    for order in (1, 2):
        prev = None
        for nr, nz in ((6, 12), (12, 24), (24, 48), (48, 96)):
            out = solve(Rf, h, 1, nr, nz, order)
            err = out['f'][:3] / ex - 1
            rate = '' if prev is None else '  order ' + ', '.join(f'{np.log2(abs(a / b)):.2f}' for a, b in zip(prev, err))
            print(f'  P{order} {nr:2d} x {nz:3d} ({out["ndof"]:6d} unknowns): ' + ', '.join(f'{e:+.2e}' for e in err) + rate)
            prev = err
    for m in (0, 2):
        out = solve(Rf, h, m, 48, 96, 2); ex2 = exact_cyl(R, h, m, 3)
        print(f'  P2 48 x 96, m = {m}: ' + ', '.join(f'{a:.5f} ({a / b - 1:+.1e})' for a, b in zip(out['f'][:3], ex2)))
    r = solve(Rf, h, 1, 48, 96, 2)
    from scipy.special import jv
    k = jnp_zeros(1, 1)[0] / R
    ex_shape = jv(1, k * r['r']) / jv(1, k * R)
    print(f'  surface shape of mode (1,1) against J1(kr)/J1(kR): largest difference {np.abs(r["shapes"][0] - ex_shape).max():.1e}')
    xi = jnp_zeros(1, 6); r6 = solve(Rf, h, 1, 48, 96, 2, nmodes=6)
    print('  c_n / R (exact 2/(xi^2 - 1)): ' + ', '.join(f'{a / R:.6f} ({b:.6f})' for a, b in zip(r6['c'], 2 / (xi ** 2 - 1))))
    r40 = solve(Rf, h, 1, 48, 96, 2, nmodes=40)
    print(f'  static tilt: sum of c_n e_n(R) over {len(r40["c"])} modes = {r40["c"].sum() / R:.5f} R (exact 1)')
    print('Wall friction (laminar Stokes layer). Deep cylinder, h = 10 R: Lambda R must be (xi^2 + 1)/(xi^2 - 1) (derived by hand),')
    print('and the log decrement 2 pi zeta / (nu^1/2 R^-3/4 g^-1/4) must be Miles K = 3.52 (Stephens et al. 1962, eq. 3):')
    for nr, nz in ((12, 24), (24, 48), (48, 96)):
        d = solve(Rf, 10 * R, 1, nr, nz, 2, grade=3.0, nmodes=3)
        K = 2 * np.pi * zeta(d, 1e-6)[0] / (1e-6 ** 0.5 * R ** -0.75 * G ** -0.25)
        print(f'  P2 {nr} x {nz}: Lambda R = ' + ', '.join(f'{a * R:.5f}' for a in d['Lam']) + ' (exact '
              + ', '.join(f'{(x * x + 1) / (x * x - 1):.5f}' for x in jnp_zeros(1, 3)) + f'); K = {K:.4f}')
    d = solve(Rf, h, 1, 48, 96, 2, nmodes=1)
    print(f'  the page note\'s cylinder (h = 100 mm), water nu = 1e-6: zeta = {zeta(d, 1e-6)[0]:.5f} (floor included)')


def tulip(hs):
    dz, Rarr = glass(); Rf = profile_fn(dz, Rarr)
    res = {}
    for hmm in hs:
        h = hmm / 1000
        row = {'h_mm': hmm, 'R_surface_mm': float(Rf(np.array([h]))[0] * 1000)}
        for m in (0, 1, 2):
            a = solve(Rf, h, m, 24, 48, 2); b = solve(Rf, h, m, 48, 96, 2)
            row[f'm{m}'] = [float(x) for x in b['f'][:4]]
            row[f'm{m}_mesh_change'] = [float(x) for x in (b['f'][:4] / a['f'][:4] - 1)]
        Rs = row['R_surface_mm'] / 1000
        row['cyl_same_surface_radius_m1'] = [float(x) for x in exact_cyl(Rs, h, 1, 3)]
        c40 = solve(Rf, h, 1, 48, 96, 2, nmodes=40)
        row['m1_c_mm'] = [float(x * 1000) for x in c40['c'][:6]]
        row['m1_c_sum_over_R'] = float(c40['c'].sum() / Rs)
        row['m1_static_wall_mm_per_ms2'] = float(-c40['c'][0] / G * 1000)
        row['m1_Lambda_per_m'] = [float(x) for x in c40['Lam'][:6]]
        row['m1_zeta_water'] = [float(x) for x in zeta(c40, 1e-6)[:6]]
        row['m1_shapes'] = {'r_mm': [float(x * 1000) for x in c40['r']], 'e': [[float(x) for x in e] for e in c40['shapes'][:6]]}
        res[hmm] = row
        print(f'h = {hmm} mm, surface radius {row["R_surface_mm"]:.2f} mm')
        for m in (0, 1, 2):
            print(f'  m = {m}: ' + ', '.join(f'{x:.4f}' for x in row[f"m{m}"]) + ' Hz   (change from mesh 24x48 to 48x96: '
                  + ', '.join(f'{x:+.1e}' for x in row[f"m{m}_mesh_change"]) + ')')
        print('  a cylinder of the surface radius, m = 1: ' + ', '.join(f'{x:.4f}' for x in row['cyl_same_surface_radius_m1']) + ' Hz')
        print('  m = 1 push coefficients c_n (mm): ' + ', '.join(f'{x:.3f}' for x in row['m1_c_mm'])
              + f'; sum over 40 modes = {row["m1_c_sum_over_R"]:.5f} R(h); steady wall rise of mode 1: {row["m1_static_wall_mm_per_ms2"]:.3f} mm per m/s^2')
        print('  m = 1 wall friction, damping ratio with water (nu = 1e-6): ' + ', '.join(f'{x:.5f}' for x in row['m1_zeta_water']))
    return res


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if what == 'check':
        check()
    else:
        out = tulip([float(x) for x in sys.argv[2:]] or [125.0])
        if os.environ.get('OUT'):
            json.dump(out, open(os.environ['OUT'], 'w'), indent=1)
