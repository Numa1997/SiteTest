#!/usr/bin/env python3
"""Linear sloshing modes of the Guinness tulip pint (Fig. 12), by the finite element method.

    python3 tools/fig12/modes_fem.py check            # the cylinder against its exact answer, and a convergence table
    python3 tools/fig12/modes_fem.py tulip [h_mm ...] # the tulip at the given fill heights (default 125)
    python3 tools/fig12/modes_fem.py sweep [out.json] # every fill height 30-145 mm in 2.5 mm steps: the page's data file
                                                      # (default public/data/fig12/modes.json)

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
    # The surface skin (Lamb 1932, Art. 351): a protein- or film-covered surface is inextensible, so the tangential velocity there
    # is brought to rest across a Stokes layer of its own: Lam_s = int_surface |grad_h phi|^2 dS / int |grad phi|^2 dV, same factor.
    @Functional
    def sform(w):
        u = w['u']; r = w.x[0]
        return (u.grad[0] ** 2 + m * m * u.value ** 2 / r ** 2) * r
    # Bulk viscous loss of the potential flow: the strain rate is the Hessian H of phi, mean heat mu int |H|^2 dV, so
    # zeta_bulk = nu Bk / omega with Bk = int |H|^2 dV / int |grad phi|^2 dV. For phi = Phi(r, z) cos(m theta), |H|^2 averaged
    # over theta (the same angular factor as the energy) is
    #   Phi_rr^2 + Phi_zz^2 + 2 Phi_rz^2 + (Phi_r/r - m^2 Phi/r^2)^2 + 2 m^2 (Phi_r/r - Phi/r^2)^2 + 2 m^2 Phi_z^2 / r^2.
    # Lagrange elements carry no second derivatives: the gradient is projected onto the same P2 space (L2 projection) and
    # differentiated again; the mixed derivative is the mean of d(Phi_r)/dz and d(Phi_z)/dr
    @Functional
    def hform(w):
        u, gr, gz = w['u'], w['gr'], w['gz']; r = w.x[0]; P, Pr, Pz = u.value, u.grad[0], u.grad[1]
        Hrr, Hzz, Hrz = gr.grad[0], gz.grad[1], 0.5 * (gr.grad[1] + gz.grad[0])
        return (Hrr ** 2 + Hzz ** 2 + 2 * Hrz ** 2 + (Pr / r - m * m * P / r ** 2) ** 2
                + 2 * m * m * (Pr / r - P / r ** 2) ** 2 + 2 * m * m * Pz ** 2 / r ** 2) * r
    fbs = FacetBasis(mesh, E, facets=top)

    @BilinearForm
    def mass(u, v, w):
        return u * v
    from skfem import LinearForm
    @LinearForm
    def proj_r(v, w):
        return w['u'].grad[0] * v
    @LinearForm
    def proj_z(v, w):
        return w['u'].grad[1] * v
    Mlu = spla.splu(mass.assemble(ib).tocsc())
    shapes, c, lam, ix, vc, lams, bk = [], [], [], [], [], [], []
    for j in range(V.shape[1]):
        v = V[:, j] / V[o[-1], j]                              # the surface shape e_n, 1 at the wall
        shapes.append(v[o])
        # c_n = int x e_n dS / int e_n^2 dS (m = 1; the angular integrals give pi on both sides): with this, a push a_x drives
        # beta_n'' + omega_n^2 (1 + a_z/g) beta_n = -kappa_n c_n a_x, and a steady push tilts the surface by sum c_n e_n = x
        c.append(float(v @ Mss @ r_s / (v @ Mss @ v)) if m == 1 else 0.0)
        # Ix = int x e cos(theta) dS = pi int r^2 e dr: the stout's momentum relative to the glass is rho sum Ix_n q_n' (mass
        # conservation: only the surface moves the centre of mass); Vc = int_{high half} e cos(theta) dS = 2 int e r dr: the
        # volume of the crest above the rest level per unit wall height (for the pour over the rim)
        ix.append(float(np.pi * v @ Mss @ r_s) if m == 1 else 0.0); vc.append(float(2 * v @ Mss @ np.ones_like(r_s)))
        x = np.zeros(n); x[sdofs] = v; x[inner] = -X @ v
        en = x @ K @ x
        lam.append(float(wform.assemble(fbw, u=fbw.interpolate(x)) / en))
        lams.append(float(sform.assemble(fbs, u=fbs.interpolate(x)) / en))
        ux = ib.interpolate(x)
        gr = Mlu.solve(proj_r.assemble(ib, u=ux)); gz = Mlu.solve(proj_z.assemble(ib, u=ux))
        bk.append(float(hform.assemble(ib, u=ux, gr=ib.interpolate(gr), gz=ib.interpolate(gz)) / en))
    f = np.sqrt(G * kap) / (2 * np.pi)
    return dict(f=f, kappa=kap, r=r_s[o], shapes=shapes, c=np.array(c), Lam=np.array(lam), LamS=np.array(lams), Bk=np.array(bk), Ix=np.array(ix), Vc=np.array(vc), ndof=n, nsurf=len(sdofs))


def zeta(out, nu, part='wall'):
    w = 2 * np.pi * out['f']
    if part == 'wall': return 0.5 * np.sqrt(nu / (2 * w)) * out['Lam']
    if part == 'skin': return 0.5 * np.sqrt(nu / (2 * w)) * out['LamS']
    if part == 'bulk': return nu * out['Bk'] / w
    raise ValueError(part)


def bessel_ratios(R, h, m, n=1, N=400):
    """Independent check: the surface-skin and bulk ratios of the cylinder's exact mode J_m(kr) cosh(kz) cos(m th) (floor
    z = 0, surface z = h), by Gauss quadrature of its analytic derivatives."""
    from scipy.special import jv, jvp
    k = jnp_zeros(m, n)[-1] / R
    xr, wr = np.polynomial.legendre.leggauss(N); r = 0.5 * R * (xr + 1); wr = 0.5 * R * wr
    xz, wz = np.polynomial.legendre.leggauss(N); z = 0.5 * h * (xz + 1); wz = 0.5 * h * wz
    rr, zz = np.meshgrid(r, z, indexing='ij'); W = np.outer(wr, wz) * rr
    J, Jp = jv(m, k * rr), jvp(m, k * rr); x = k * rr
    Jpp = -Jp / x - (1 - m * m / x ** 2) * J
    C, S = np.cosh(k * zz), np.sinh(k * zz)
    P, Pr, Pz = J * C, k * Jp * C, k * J * S
    Prr, Pzz, Prz = k * k * Jpp * C, k * k * J * C, k * k * Jp * S
    en = np.sum(W * (Pr ** 2 + Pz ** 2 + m * m * P ** 2 / rr ** 2))
    H2 = (Prr ** 2 + Pzz ** 2 + 2 * Prz ** 2 + (Pr / rr - m * m * P / rr ** 2) ** 2 + 2 * m * m * (Pr / rr - P / rr ** 2) ** 2 + 2 * m * m * Pz ** 2 / rr ** 2)
    rs = r; Js, Jps = jv(m, k * rs) * np.cosh(k * h), k * jvp(m, k * rs) * np.cosh(k * h)
    skin = np.sum(wr * rs * (Jps ** 2 + m * m * Js ** 2 / rs ** 2))
    return skin / en, np.sum(W * H2) / en


def exact_cyl(R, h, m, n):
    k = jnp_zeros(m, n) / R
    return np.sqrt(G * k * np.tanh(k * h)) / (2 * np.pi)


def check():
    """Prints the checks and returns the list of failures (empty: pass). Tolerances: frequencies 1e-6, push coefficients 1e-4,
    the deep-tank wall friction 1e-3 relative, the static tilt sum within the 40-mode tail (0.5 %)."""
    fails = []
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
    if abs(err[0]) > 1e-6: fails.append(f'f11 error {err[0]:.1e}')
    for m in (0, 2):
        out = solve(Rf, h, m, 48, 96, 2); ex2 = exact_cyl(R, h, m, 3)
        if abs(out['f'][0] / ex2[0] - 1) > 1e-6: fails.append(f'm={m} f error')
        print(f'  P2 48 x 96, m = {m}: ' + ', '.join(f'{a:.5f} ({a / b - 1:+.1e})' for a, b in zip(out['f'][:3], ex2)))
    r = solve(Rf, h, 1, 48, 96, 2)
    from scipy.special import jv
    k = jnp_zeros(1, 1)[0] / R
    ex_shape = jv(1, k * r['r']) / jv(1, k * R)
    print(f'  surface shape of mode (1,1) against J1(kr)/J1(kR): largest difference {np.abs(r["shapes"][0] - ex_shape).max():.1e}')
    if np.abs(r['shapes'][0] - ex_shape).max() > 1e-5: fails.append('shape')
    xi = jnp_zeros(1, 6); r6 = solve(Rf, h, 1, 48, 96, 2, nmodes=6)
    print('  c_n / R (exact 2/(xi^2 - 1)): ' + ', '.join(f'{a / R:.6f} ({b:.6f})' for a, b in zip(r6['c'], 2 / (xi ** 2 - 1))))
    if np.abs(r6['c'][:3] / R / (2 / (xi[:3] ** 2 - 1)) - 1).max() > 1e-4: fails.append('push coefficients')
    from scipy.integrate import quad
    from scipy.special import j1
    ix_ex = np.pi * R ** 3 / xi[:3] ** 2
    vc_ex = np.array([2 * R * R * quad(lambda u: j1(x * u) * u, 0, 1)[0] / j1(x) for x in xi[:3]])
    print('  Ix (exact pi R^3/xi^2): ' + ', '.join(f'{a:.4e} ({b:.4e})' for a, b in zip(r6['Ix'], ix_ex))
          + ';  Vc (exact 2 R^2 int J1(xi s) s ds / J1(xi)): ' + ', '.join(f'{a:.4e} ({b:.4e})' for a, b in zip(r6['Vc'], vc_ex)))
    if np.abs(r6['Ix'][:3] / ix_ex - 1).max() > 1e-4 or np.abs(r6['Vc'][:3] / vc_ex - 1).max() > 1e-4: fails.append('Ix or Vc')
    r40 = solve(Rf, h, 1, 48, 96, 2, nmodes=40)
    if not 0.990 < r40['c'].sum() / R <= 1.0: fails.append('static tilt')
    print(f'  static tilt: sum of c_n e_n(R) over {len(r40["c"])} modes = {r40["c"].sum() / R:.5f} R (exact 1)')
    print('Wall friction (laminar Stokes layer). Deep cylinder, h = 10 R: Lambda R must be (xi^2 + 1)/(xi^2 - 1) (derived by hand),')
    print('and the log decrement 2 pi zeta / (nu^1/2 R^-3/4 g^-1/4) must be Miles K = 3.52 (Stephens et al. 1962, eq. 3):')
    for nr, nz in ((12, 24), (24, 48), (48, 96)):
        d = solve(Rf, 10 * R, 1, nr, nz, 2, grade=3.0, nmodes=3)
        K = 2 * np.pi * zeta(d, 1e-6)[0] / (1e-6 ** 0.5 * R ** -0.75 * G ** -0.25)
        print(f'  P2 {nr} x {nz}: Lambda R = ' + ', '.join(f'{a * R:.5f}' for a in d['Lam']) + ' (exact '
              + ', '.join(f'{(x * x + 1) / (x * x - 1):.5f}' for x in jnp_zeros(1, 3)) + f'); K = {K:.4f}')
    if abs(d['Lam'][0] * R / ((xi[0] ** 2 + 1) / (xi[0] ** 2 - 1)) - 1) > 1e-3: fails.append('wall friction')
    print('Surface skin and bulk loss on the cylinder (h = 100 mm), finite elements against the exact Bessel mode:')
    for m in (1, 0, 2):
        ex_s, ex_b = bessel_ratios(R, h, m)
        for nr, nz in ((24, 48), (48, 96), (96, 192)):
            d = solve(Rf, h, m, nr, nz, 2, nmodes=1)
            print(f'  m = {m}, P2 {nr} x {nz}: skin {d["LamS"][0]:.5f} (exact {ex_s:.5f}) 1/m, bulk {d["Bk"][0]:.3f} (exact {ex_b:.3f}) 1/m^2')
        if abs(d['LamS'][0] / ex_s - 1) > 1e-4 or abs(d['Bk'][0] / ex_b - 1) > 2e-3: fails.append(f'skin or bulk m={m}')
    k1 = jnp_zeros(1, 1)[0] / R
    print(f'  deep-water bulk 2 k^2 = {2 * k1 * k1:.3f} 1/m^2 (m = 1; the cylinder differs by its wall and depth)')
    d = solve(Rf, h, 1, 48, 96, 2, nmodes=1)
    print(f'  the page note\'s cylinder (h = 100 mm), water nu = 1e-6: zeta = {zeta(d, 1e-6)[0]:.5f} (floor included)')
    return fails


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


def sweep(path):
    """The page's data: for each fill height, harmonics m = 0, 1, 2, the first modes' frequency f (Hz), surface curvature
    kappa = omega^2/g (1/m), push coefficient c (m, m = 1 only), wall-friction factor Lam (1/m; zeta = sqrt(nu/(2 omega)) Lam / 2)
    and surface shape e(r) on NR points r = R(h) j/(NR-1), 1 at the wall. Mesh 48 x 96 P2; the 24 x 48 change is recorded."""
    dz, Rarr = glass(); Rf = profile_fn(dz, Rarr)
    NR, NM = 33, {0: 4, 1: 6, 2: 4}
    hs = [round(30 + 2.5 * k, 1) for k in range(47)]
    out = {'about': 'Fig. 12 linear sloshing modes of the Guinness tulip, by tools/fig12/modes_fem.py sweep (finite elements, P2, '
                    'mesh 48 x 96 on the meridian section). Elevation of mode (m, n): beta(t) e(r) cos(m theta). '
                    'm = 1 obeys beta\'\' + 2 zeta omega beta\' + omega^2 (1 + a_z/g) beta = -(omega^2/g) c a_x. '
                    'Surface-skin factor LamS (1/m; zeta_skin = sqrt(nu/(2 omega)) LamS / 2, an inextensible surface, Lamb 1932 Art. 351); bulk factor Bk (1/m^2; zeta_bulk = nu Bk / omega). Momentum relative to the glass rho sum Ix q\'; crest volume on the high half per unit wall height Vc. Wall-friction damping zeta = (1/2) sqrt(nu/(2 omega)) Lam (laminar Stokes layer). '
                    'Lengths in m, frequencies in Hz.',
           'g': G, 'glass_profile': 'public/scripts/guinness-glass.js', 'NR': NR, 'h': hs, 'R_surface': [], 'levels': []}
    worst = 0.0
    for h_mm in hs:
        h = h_mm / 1000; lev = {}
        out['R_surface'].append(round(float(Rf(np.array([h]))[0]), 7))
        for m, nm in NM.items():
            b = solve(Rf, h, m, 48, 96, 2, nmodes=max(nm, 40 if m == 1 else nm))
            a = solve(Rf, h, m, 24, 48, 2, nmodes=nm)
            worst = max(worst, float(np.abs(b['f'][:nm] / a['f'][:nm] - 1).max()))
            rr = np.linspace(0, b['r'][-1], NR)
            lev[f'm{m}'] = {'f': [round(float(x), 6) for x in b['f'][:nm]], 'kappa': [round(float(x), 5) for x in b['kappa'][:nm]],
                            'Lam': [round(float(x), 4) for x in b['Lam'][:nm]],
                            'LamS': [round(float(x), 4) for x in b['LamS'][:nm]], 'Bk': [round(float(x), 2) for x in b['Bk'][:nm]],
                            'e': [[round(float(x), 5) for x in np.interp(rr, b['r'], e)] for e in b['shapes'][:nm]]}
            if m == 1:
                lev['m1']['c'] = [round(float(x), 8) for x in b['c'][:nm]]
                lev['m1']['c_sum_40_over_R'] = round(float(b['c'].sum() / b['r'][-1]), 5)
            lev[f'm{m}']['Ix'] = [float(f'{x:.6e}') for x in b['Ix'][:nm]]
            lev[f'm{m}']['Vc'] = [float(f'{x:.6e}') for x in b['Vc'][:nm]]
        out['levels'].append(lev)
        print(f'h {h_mm:5.1f} mm  R {out["R_surface"][-1] * 1000:5.2f} mm  f11 {lev["m1"]["f"][0]:.4f} Hz  f01 {lev["m0"]["f"][0]:.4f}  '
              f'f21 {lev["m2"]["f"][0]:.4f}  c1 {lev["m1"]["c"][0] * 1000:.3f} mm  zeta11 (water) '
              f'{0.5 * np.sqrt(1e-6 / (2 * 2 * np.pi * lev["m1"]["f"][0])) * lev["m1"]["Lam"][0]:.5f}', flush=True)
    out['mesh_change_worst'] = worst
    print(f'largest change of any listed frequency from mesh 24 x 48 to 48 x 96: {worst:.1e}')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, 'w'), separators=(',', ':'))
    print(f'wrote {path}: {os.path.getsize(path)} bytes')


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if what == 'check':
        f = check()
        print('CHECK ' + ('PASSED' if not f else 'FAILED: ' + '; '.join(f)))
        sys.exit(1 if f else 0)
    elif what == 'sweep':
        sweep(sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'public', 'data', 'fig12', 'modes.json'))
    else:
        out = tulip([float(x) for x in sys.argv[2:]] or [125.0])
        if os.environ.get('OUT'):
            json.dump(out, open(os.environ['OUT'], 'w'), indent=1)
