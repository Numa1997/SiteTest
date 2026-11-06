"""Linear sloshing modes of the sculpted glass in three dimensions, by the finite-element method.

The cavity is not a body of revolution (the two sculpted panels), so the potential cannot be split into cos(m theta)
parts. We solve the full Steklov problem instead:
    Laplace Phi = 0 in the liquid, d_n Phi = 0 on wall and floor, d_z Phi = lam Phi on the mean free surface z = zs,
weak form  int grad Phi . grad v dV = lam int_S Phi v dS,
on a mesh of 27-node (triquadratic, Q2) hexahedra mapped from (s, theta, zeta): r = s R_i(z, theta), the axis s = 0
collapsed to one node per level. The elements are curved (isoparametric), so the wall is the real wall, not chords.
The interior is condensed out (Schur complement) and the dense symmetric problem on the surface nodes is solved.

Also solved on the same mesh: the Stokes-Joukowski potentials chi_x, chi_y of a rotation of the glass about the x or y
axis through the foot centre O (Laplace chi = 0, d_n chi = (e x r).n on the whole boundary, free surface included):
the flow of the liquid when the glass turns, as if the liquid were frozen under a rigid lid. They give the forcing of
each mode by an angular acceleration and the moment the sloshing liquid puts back on the glass (notes: the derivation
in the page's note, section "The glass turns").

Per mode: lam, the surface shape on the (s, theta) grid, the forcing coefficients Q_x, Q_y (translation), Q_rx, Q_ry
(rotation), N = int psi^2 dS, and the damping integrals Iw (wall), Ib (floor), Is (surface) of |grad_t Phi|^2, with
E = int |grad Phi|^2 dV (= lam N by Green's identity, a check).
Units: metres. The mode shapes are normalised to max |psi| = 1 on the rim, so the amplitude a_n is the wave height
at the rim where this mode is largest.
"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla, scipy.linalg as sla

GP = np.array([-np.sqrt(3 / 5), 0.0, np.sqrt(3 / 5)]); GW = np.array([5 / 9, 8 / 9, 5 / 9])

def _l1(x):   # quadratic Lagrange on [-1, 1] at nodes -1, 0, 1, and derivatives
    return np.array([x * (x - 1) / 2, 1 - x * x, x * (x + 1) / 2]), np.array([x - 0.5, -2 * x, x + 0.5])

def _basis3():
    """Values and gradients of the 27 Q2 shape functions at the 27 Gauss points. Local node (a, b, c) -> index a + 3b + 9c."""
    N = np.zeros((27, 27)); dN = np.zeros((27, 27, 3)); W = np.zeros(27); g = 0
    for kc, zc in enumerate(GP):
        for kb, yb in enumerate(GP):
            for ka, xa in enumerate(GP):
                la, dla = _l1(xa); lb, dlb = _l1(yb); lc, dlc = _l1(zc)
                for c in range(3):
                    for b in range(3):
                        for a in range(3):
                            i = a + 3 * b + 9 * c
                            N[g, i] = la[a] * lb[b] * lc[c]
                            dN[g, i] = [dla[a] * lb[b] * lc[c], la[a] * dlb[b] * lc[c], la[a] * lb[b] * dlc[c]]
                W[g] = GW[ka] * GW[kb] * GW[kc]; g += 1
    return N, dN, W

def _basis2():
    """The 9 Q2 shape functions of a face at the 9 Gauss points. Local node (a, b) -> a + 3b."""
    N = np.zeros((9, 9)); dN = np.zeros((9, 9, 2)); W = np.zeros(9); g = 0
    for kb, yb in enumerate(GP):
        for ka, xa in enumerate(GP):
            la, dla = _l1(xa); lb, dlb = _l1(yb)
            for b in range(3):
                for a in range(3):
                    N[g, a + 3 * b] = la[a] * lb[b]; dN[g, a + 3 * b] = [dla[a] * lb[b], la[a] * dlb[b]]
            W[g] = GW[ka] * GW[kb]; g += 1
    return N, dN, W

N3, dN3, W3 = _basis3(); N2, dN2, W2 = _basis2()


class Mesh:
    def __init__(self, Rfun, zf, zs, Ns=6, Nt=24, Nz=16, grade=2.0):
        """Rfun(z, theta) -> inner radius (m). Nodes (i, j, k): i = 0..2Ns radial, j = 0..2Nt-1 around, k = 0..2Nz up."""
        self.Rfun, self.zf, self.zs = Rfun, zf, zs
        ni, nj, nk = 2 * Ns + 1, 2 * Nt, 2 * Nz + 1
        S = np.linspace(0, 1, ni); TH = 2 * np.pi * np.arange(nj) / nj
        zeta = np.linspace(0, 1, nk); Z = zf + (zs - zf) * (1 - (1 - zeta) ** grade)
        # node ids: axis nodes (i = 0) share one id per level k
        ids = np.zeros((ni, nj, nk), int); n = 0
        for k in range(nk):
            ids[0, :, k] = n; n += 1
            for i in range(1, ni):
                for j in range(nj): ids[i, j, k] = n; n += 1
        X = np.zeros((n, 3))
        for k in range(nk):
            X[ids[0, 0, k]] = [0, 0, Z[k]]
            for i in range(1, ni):
                r = S[i] * Rfun(Z[k], TH); X[ids[i, :, k], 0] = r * np.cos(TH); X[ids[i, :, k], 1] = r * np.sin(TH); X[ids[i, :, k], 2] = Z[k]
        self.ids, self.X, self.S, self.TH, self.Z = ids, X, S, TH, Z
        self.Ns, self.Nt, self.Nz = Ns, Nt, Nz
        E = []
        for ez in range(Nz):
            for et in range(Nt):
                for es in range(Ns):
                    E.append([ids[2 * es + a, (2 * et + b) % nj, 2 * ez + c] for c in range(3) for b in range(3) for a in range(3)])
        self.E = np.array(E); self.n = n
        self.surf = ids[:, :, -1]            # (ni, nj) node ids on the free surface (axis repeated)
        self.surf_ids = np.unique(self.surf)
        # faces for boundary integrals: each a list of 9 node ids (local (a,b) -> a + 3b) and a parametrisation sign
        self.faces = {'wall': [], 'floor': [], 'surface': []}
        for ez in range(Nz):
            for et in range(Nt):
                self.faces['wall'].append([ids[-1, (2 * et + b) % nj, 2 * ez + c] for c in range(3) for b in range(3)])        # (theta, z)
        for et in range(Nt):
            for es in range(Ns):
                self.faces['floor'].append([ids[2 * es + a, (2 * et + b) % nj, 0] for b in range(3) for a in range(3)])         # (s, theta) at zf
                self.faces['surface'].append([ids[2 * es + a, (2 * et + b) % nj, -1] for b in range(3) for a in range(3)])      # (s, theta) at zs
        for key in self.faces: self.faces[key] = np.array(self.faces[key])

    # ---- volume assembly ----
    def stiffness(self):
        E, X = self.E, self.X
        Xe = X[E]                                                  # (ne, 27, 3)
        J = np.einsum('gia,eid->egad', dN3, Xe)                    # (ne, 27g, 3 (xi), 3 (x)): J[a, d] = d x_d / d xi_a
        detJ = np.linalg.det(J); Ji = np.linalg.inv(J)             # (ne, g), (ne, g, 3, 3)
        assert (detJ > 0).all(), 'inverted element'
        G = np.einsum('gia,egba->egib', dN3, Ji)                   # grad_b N_i = sum_a dN_i/dxi_a (J^-1)_{ba}, (ne, g, 27, 3)
        Ke = np.einsum('g,eg,egib,egjb->eij', W3, detJ, G, G)      # (ne, 27, 27)
        rows = np.repeat(E, 27, axis=1).ravel(); cols = np.tile(E, (1, 27)).ravel()
        K = sp.csr_matrix((Ke.ravel(), (rows, cols)), shape=(self.n, self.n)); K.sum_duplicates()
        self._G, self._detJ = G, detJ
        return K

    def _face_geom(self, F):
        Xf = self.X[F]                                             # (nf, 9, 3)
        T = np.einsum('gia,eid->egad', dN2, Xf)                    # (nf, 9g, 2, 3): tangent vectors d x / d u, d x / d v
        nvec = np.cross(T[:, :, 0, :], T[:, :, 1, :])              # (nf, g, 3), |n| = dS / du dv
        return Xf, T, nvec

    def surface_mass(self):
        F = self.faces['surface']; Xf, T, nvec = self._face_geom(F); dS = np.linalg.norm(nvec, axis=2)
        Me = np.einsum('g,eg,gi,gj->eij', W2, dS, N2, N2)
        rows = np.repeat(F, 9, axis=1).ravel(); cols = np.tile(F, (1, 9)).ravel()
        M = sp.csr_matrix((Me.ravel(), (rows, cols)), shape=(self.n, self.n)); M.sum_duplicates(); return M

    def boundary_rhs(self, axis):
        """b_i = int_boundary N_i (e_axis x r) . n dS over wall, floor and surface, outward normal."""
        b = np.zeros(self.n); e = np.zeros(3); e[axis] = 1.0
        for key, sign in (('wall', +1), ('floor', -1), ('surface', +1)):
            F = self.faces[key]; Xf, T, nvec = self._face_geom(F)
            # orientation: wall faces parametrised (theta, z): d/dtheta x d/dz points outward; floor (s, theta): d/ds x d/dtheta points up (inward) -> sign -1; surface: up = outward
            xg = np.einsum('gi,eid->egd', N2, Xf)                   # points (nf, g, 3)
            om = np.cross(e, xg)                                    # (e x r)
            flux = sign * np.einsum('egd,egd->eg', om, nvec)        # (e x r).n dS/dudv
            be = np.einsum('g,eg,gi->ei', W2, flux, N2)
            np.add.at(b, F.ravel(), be.ravel())
        return b

    def face_integral_grad_t2(self, Phi, key):
        """int_face |grad_t Phi|^2 dS with the tangential gradient from the volume elements (wall) or the face itself."""
        F = self.faces[key]; Xf, T, nvec = self._face_geom(F); dS = np.linalg.norm(nvec, axis=2)
        # tangential gradient from the face parametrisation: grad_t Phi = g^{ab} (d Phi/d u_b) t_a
        dPhi = np.einsum('gia,ei->ega', dN2, Phi[F])                # (nf, g, 2)
        gab = np.einsum('egad,egbd->egab', T, T)                    # metric (nf, g, 2, 2)
        ginv = np.linalg.inv(gab)
        q = np.einsum('ega,egab,egb->eg', dPhi, ginv, dPhi)         # |grad_t Phi|^2
        return float(np.einsum('g,eg,eg->', W2, dS, q))

    def surface_integral(self, f):
        """int_S f dS for nodal f (on surface nodes)."""
        F = self.faces['surface']; Xf, T, nvec = self._face_geom(F); dS = np.linalg.norm(nvec, axis=2)
        return float(np.einsum('g,eg,gi,ei->', W2, dS, N2, f[F]))

    def volume_energy(self, Phi):
        return float(np.einsum('g,eg,egib,egib->', W3, self._detJ, np.einsum('egib,ei->egb', self._G, Phi[self.E])[..., None] * 0 + np.einsum('egib,ei->egb', self._G, Phi[self.E])[:, :, None, :], np.ones((1, 1, 1, 1)))) if False else self._energy(Phi)

    def _energy(self, Phi):
        g = np.einsum('egib,ei->egb', self._G, Phi[self.E])         # grad Phi at Gauss points (ne, g, 3)
        return float(np.einsum('g,eg,egb,egb->', W3, self._detJ, g, g))


def solve(Rfun, zf, zs, nmodes=14, Ns=6, Nt=24, Nz=16, grade=2.0):
    """Returns the mesh and a list of modes sorted by lam; each with Phi (all nodes), lam, and the coefficients."""
    M = Mesh(Rfun, zf, zs, Ns, Nt, Nz, grade)
    K = M.stiffness(); Ms = M.surface_mass()
    S_ = M.surf_ids; I_ = np.setdiff1d(np.arange(M.n), S_)
    KII = K[I_][:, I_].tocsc(); KIS = K[I_][:, S_].toarray(); KSS = K[S_][:, S_].toarray()
    lu = spla.splu(KII); Y = lu.solve(KIS)
    Sch = KSS - KIS.T @ Y; Sch = 0.5 * (Sch + Sch.T)
    MsS = Ms[S_][:, S_].toarray()
    lam, V = sla.eigh(Sch, MsS)
    X = M.X; xs, ys = X[S_, 0], X[S_, 1]
    rim = np.isclose(np.hypot(xs, ys), M.Rfun(zs, np.arctan2(ys, xs)), rtol=1e-6)   # surface nodes on the wall
    modes = []
    for k in range(len(lam)):
        if lam[k] < 1e-3: continue                                  # the constant mode is no wave
        Phi = np.zeros(M.n); Phi[S_] = V[:, k]; Phi[I_] = -Y @ V[:, k]
        # max |psi| = 1 on the rim, positive there: the maximum of the rim ring's trigonometric interpolant (a mode of the
        # round glass may be oriented between two nodes; the sampled maximum would then be low by up to 1 - cos(pi/2Nt))
        ring = Phi[M.ids[-1, :, -1]]; nj = len(ring); fine = np.fft.irfft(np.fft.rfft(ring), 64 * nj) * (64 * nj / nj)
        c = 1.0 / np.abs(fine).max()
        # sign: the dominant Fourier component of the rim is positive (cos k theta for a cos-type mode, sin for a sin-type),
        # so that the same mode keeps the same sign from one fill to the next and interpolation between fills is sound
        F = np.fft.rfft(ring) / nj; amp = np.abs(F); amp[0] *= 0.5; kd = int(np.argmax(amp)); re, im = F[kd].real, -F[kd].imag
        if (re if abs(re) >= abs(im) else im) < 0: c = -c
        Phi *= c
        modes.append(dict(lam=float(lam[k]), Phi=Phi))
        if len(modes) == nmodes: break
    # Stokes-Joukowski potentials: K chi = b, singular (constant); fix the mean by a one-node pin and re-centre
    chis = {}
    for axis, name in ((0, 'rx'), (1, 'ry')):
        b = M.boundary_rhs(axis)
        assert abs(b.sum()) < 1e-9 * np.abs(b).sum(), 'incompatible Neumann data'
        Kp = K.tolil(); Kp[0, :] = 0; Kp[0, 0] = 1.0; bp = b.copy(); bp[0] = 0.0
        chi = spla.spsolve(Kp.tocsc(), bp)
        chi -= M.surface_integral(chi) / M.surface_integral(np.ones(M.n))
        chis[name] = chi
    # coefficients
    S_x = M.surface_integral(X[:, 0] * 0 + X[:, 0]) if False else None
    for md in modes:
        Phi = md['Phi']; psi2 = M.surface_integral(Phi * Phi)
        md['N'] = psi2
        md['Qx'] = M.surface_integral(Phi * X[:, 0]) / psi2
        md['Qy'] = M.surface_integral(Phi * X[:, 1]) / psi2
        md['Qrx'] = M.surface_integral(Phi * chis['rx']) / psi2
        md['Qry'] = M.surface_integral(Phi * chis['ry']) / psi2
        md['E'] = M._energy(Phi)
        md['Iw'] = M.face_integral_grad_t2(Phi, 'wall'); md['Ib'] = M.face_integral_grad_t2(Phi, 'floor'); md['Is'] = M.face_integral_grad_t2(Phi, 'surface')
    # rigid parts: the frozen liquid's volume and the Stokes-Joukowski inertia for each axis
    vol = float(np.einsum('g,eg->', W3, M._detJ))
    Jsj = {name: M._energy(chi) for name, chi in chis.items()}
    return M, modes, chis, dict(V=vol, Jsj=Jsj)


# ---- helpers for the data file: labelling, Fourier components in theta, nodal gradients ----
def nodal_gradient(M, Phi):
    """grad Phi at every node, averaged over the elements that share it (Q2 shape-function gradients at the node)."""
    loc = np.array([[a - 1, b - 1, c - 1] for c in range(3) for b in range(3) for a in range(3)], float)
    dN = np.zeros((27, 27, 3))                              # [node position p, shape i, xi-direction a]
    for p, (xa, yb, zc) in enumerate(loc):
        la, dla = _l1(xa); lb, dlb = _l1(yb); lc, dlc = _l1(zc)
        for c in range(3):
            for b in range(3):
                for a in range(3):
                    dN[p, a + 3 * b + 9 * c] = [dla[a] * lb[b] * lc[c], la[a] * dlb[b] * lc[c], la[a] * lb[b] * dlc[c]]
    Xe = M.X[M.E]; J = np.einsum('pia,eid->epad', dN, Xe)
    det = np.linalg.det(J)
    good = det > 1e-12 * np.abs(det).max()                  # the collapsed axis nodes have a singular Jacobian: skip them there
    Ji = np.zeros_like(J); Ji[good] = np.linalg.inv(J[good])
    G = np.einsum('pia,epba->epib', dN, Ji)                 # grad N_i at node position p of element e
    g = np.einsum('epib,ei->epb', G, Phi[M.E])              # grad Phi (ne, 27, 3)
    out = np.zeros((M.n, 3)); cnt = np.zeros(M.n)
    for p in range(27):
        np.add.at(out, M.E[:, p], g[:, p] * good[:, p, None]); np.add.at(cnt, M.E[:, p], good[:, p])
    cnt[cnt == 0] = 1; return out / cnt[:, None]


def ring_fourier(vals, nj, kmax):
    """Cosine and sine components of a ring of nj equally spaced samples: f(theta) = sum c_k cos k theta + s_k sin k theta."""
    th = 2 * np.pi * np.arange(nj) / nj; c = []; s = []
    for k in range(kmax + 1):
        norm = nj if k == 0 else nj / 2
        c.append(float(np.sum(vals * np.cos(k * th)) / norm)); s.append(float(np.sum(vals * np.sin(k * th)) / norm) if k > 0 else 0.0)
    return np.array(c), np.array(s)


def label(M, Phi, kmax=8):
    """(m, 'c' or 's', purity): the dominant azimuthal number of the mode on the rim, its orientation, and the share of the rim
    energy in that single component (1 for a body of revolution)."""
    rim = Phi[M.ids[-1, :, -1]]; c, s = ring_fourier(rim, 2 * M.Nt, kmax)
    pw = c * c + s * s; pw[0] = c[0] * c[0] * 2
    k = int(np.argmax(pw)); orient = 'c' if abs(c[k]) >= abs(s[k]) else 's'
    return k, orient, float(pw[k] / pw.sum())


def surface_components(M, Phi, ks):
    """For each k in ks: the cos and sin coefficients of psi(s, theta) on the surface, at the 2Ns+1 radial nodes."""
    out = {}
    for k in ks:
        ck = []; sk = []
        for i in range(2 * M.Ns + 1):
            ring = Phi[M.ids[i, :, -1]]; c, s = ring_fourier(ring, 2 * M.Nt, k); ck.append(c[k]); sk.append(s[k])
        out[k] = (np.array(ck), np.array(sk))
    return out


def field_components(M, Phi, ks, zlevels):
    """Phi and its (r, z) gradient as theta-Fourier components on the (s, z) node grid, for the levels k in zlevels.
    Returns dict k -> arrays (nlev, 2Ns+1, 3, 2): [.., 0] = Phi, [.., 1] = dPhi/dr, [.., 2] = dPhi/dz; last axis cos/sin."""
    g = nodal_gradient(M, Phi); th = M.TH
    gr = g[:, 0] * np.cos(th[None, :]).ravel()[0] if False else None
    out = {k: np.zeros((len(zlevels), 2 * M.Ns + 1, 3, 2)) for k in ks}
    for li, kz in enumerate(zlevels):
        for i in range(2 * M.Ns + 1):
            ids = M.ids[i, :, kz]; cth, sth = np.cos(th), np.sin(th)
            vals = [Phi[ids], g[ids, 0] * cth + g[ids, 1] * sth, g[ids, 2]]      # Phi, d/dr, d/dz around the ring
            for q in range(3):
                c, s = ring_fourier(vals[q], 2 * M.Nt, max(ks))
                for k in ks: out[k][li, i, q] = [c[k], s[k]]
    return out
