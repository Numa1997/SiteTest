"""Linear sloshing modes of an axisymmetric glass by the finite-element method.

Potential phi = Phi(r,z) cos(m theta). Laplace's equation in the liquid, d_n Phi = 0 on wall and floor,
d_z Phi = lam Phi on the mean free surface z = zs (lam = omega^2/g). Weak form, per azimuthal number m:
   int (Phi_r psi_r + Phi_z psi_z + m^2/r^2 Phi psi) r dr dz  =  lam int_surface Phi psi r dr
Quadratic (P2) triangles on a mesh mapped from (s, z), r = s R_i(z). The interior is condensed out
(Schur complement), leaving a dense symmetric eigenproblem on the surface nodes.
Also returns, per mode, the integrals the damping and forcing terms need (see notes/fig12/derivation.md).
"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla, scipy.linalg as sla

# 7-point Gauss rule on the reference triangle (degree 5)
_a, _b = 0.059715871789770, 0.470142064105115
_c, _d = 0.797426985353087, 0.101286507323456
QP = np.array([[1/3, 1/3], [_b, _b], [_a, _b], [_b, _a], [_d, _d], [_c, _d], [_d, _c]])
QW = np.array([0.225, *[0.132394152788506]*3, *[0.125939180544827]*3]) / 2
G3 = np.array([-np.sqrt(3/5), 0, np.sqrt(3/5)]); W3 = np.array([5/9, 8/9, 5/9])

def p2(xi, eta):
    l1, l2, l3 = 1 - xi - eta, xi, eta
    N = np.array([l1*(2*l1-1), l2*(2*l2-1), l3*(2*l3-1), 4*l1*l2, 4*l2*l3, 4*l3*l1])
    dN = np.array([[-(4*l1-1), -(4*l1-1)], [4*l2-1, 0], [0, 4*l3-1],
                   [4*(l1-l2), -4*l2], [4*l3, 4*l2], [-4*l3, 4*(l1-l3)]])
    return N, dN

def mesh(Rfun, z0, zs, ns, nz, grade=2.0):
    """P2 mesh of 0<=r<=R(z), z0<=z<=zs; nodes graded towards the surface (where modes live)."""
    S = np.linspace(0, 1, 2*ns+1)
    t = np.linspace(0, 1, 2*nz+1); Z = zs - (zs - z0) * (1 - t)**grade      # dense near zs
    Z = z0 + (zs - z0) * (1 - (1 - t)**grade)
    idx = np.arange(len(S)*len(Z)).reshape(len(Z), len(S))
    zz, ss = np.meshgrid(Z, S, indexing='ij')
    X = np.c_[(ss*Rfun(zz)).ravel(), zz.ravel()]
    tris = []
    for i in range(0, 2*nz, 2):
        for j in range(0, 2*ns, 2):
            a, b, c, d = idx[i, j], idx[i, j+2], idx[i+2, j+2], idx[i+2, j]
            tris.append([a, b, c, idx[i, j+1], idx[i+1, j+2], idx[i+1, j+1]])
            tris.append([a, c, d, idx[i+1, j+1], idx[i+2, j+1], idx[i+1, j]])
    # straight-sided P2: mid-edge nodes moved to the midpoints in physical space
    T = np.array(tris)
    for (p, q, mid) in [(0, 1, 3), (1, 2, 4), (2, 0, 5)]:
        X[T[:, mid]] = 0.5*(X[T[:, p]] + X[T[:, q]])
    return X, T, idx

def solve(Rfun, z0, zs, m, nmodes=3, ns=16, nz=40):
    X, T, idx = mesh(Rfun, z0, zs, ns, nz)
    n = len(X); rows, cols, vals = [], [], []
    for tri in T:
        P = X[tri]; J = np.array([P[1,:2]-P[0,:2], P[2,:2]-P[0,:2]]).T
        detJ = abs(np.linalg.det(J)); Ji = np.linalg.inv(J)
        Ke = np.zeros((6, 6))
        for (xi, eta), w in zip(QP, QW):
            N, dN = p2(xi, eta); g = dN @ Ji
            r = N @ P[:, 0]
            Ke += w*detJ*(r*(g @ g.T) + (m*m/r)*np.outer(N, N))
        rows += np.repeat(tri, 6).tolist(); cols += np.tile(tri, 6).tolist(); vals += Ke.ravel().tolist()
    K = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
    top = idx[-1]                                    # surface nodes, r from 0 to R(zs)
    rs = X[top, 0]; Ms = np.zeros((len(top), len(top)))
    for e in range(0, len(top)-1, 2):
        a, b = rs[e], rs[e+2]; h = b - a
        for x, w in zip(G3, W3):
            s = (x+1)/2; r = a + h*s
            N = np.array([2*(s-.5)*(s-1), 4*s*(1-s), 2*s*(s-.5)])
            Ms[e:e+3, e:e+3] += w*h/2*r*np.outer(N, N)
    fixed = np.array([], int)
    if m >= 1: fixed = idx[:, 0]                     # Phi = 0 on the axis
    free = np.setdiff1d(np.arange(n), fixed)
    S_ = np.intersect1d(top, free); I_ = np.setdiff1d(free, S_)
    pos = {v: k for k, v in enumerate(top)}; sel = [pos[v] for v in S_]
    KII = K[I_][:, I_].tocsc(); KIS = K[I_][:, S_].toarray(); KSS = K[S_][:, S_].toarray()
    lu = spla.splu(KII); Y = lu.solve(KIS)
    Sch = KSS - KIS.T @ Y; Sch = 0.5*(Sch + Sch.T)
    lam, V = sla.eigh(Sch, Ms[np.ix_(sel, sel)])
    out = []
    for k in range(len(lam)):
        if lam[k] < 1e-6 * (1/max(rs)): continue    # the constant (m = 0) mode is no wave
        Phi = np.zeros(n); Phi[S_] = V[:, k]; Phi[I_] = -Y @ V[:, k]
        f = Phi[top]
        if f[np.argmax(np.abs(f))] < 0: Phi, f = -Phi, -f
        nrm = np.sqrt(f @ Ms @ f); Phi /= nrm; f /= nrm          # int f^2 r dr = 1
        out.append(dict(m=m, lam=lam[k], Phi=Phi, f=f, rs=rs))
        if len(out) == nmodes: break
    return X, T, idx, out

def surf_int(rs, f, wfun):
    """int f(r) w(r) dr along the surface with the P2 interpolation of f and 3-point Gauss."""
    tot = 0.0
    for e in range(0, len(rs)-1, 2):
        a, b = rs[e], rs[e+2]; h = b - a
        for x, w in zip(G3, W3):
            s = (x+1)/2; r = a + h*s
            N = np.array([2*(s-.5)*(s-1), 4*s*(1-s), 2*s*(s-.5)])
            tot += w*h/2*(N @ f[e:e+3])*wfun(r)
    return tot

def grad_at(X, T, Phi, pts):
    """Phi and its (r,z) gradient at arbitrary points (by locating the containing triangle)."""
    res = np.full((len(pts), 3), np.nan)
    P0 = X[T[:, 0]]; P1 = X[T[:, 1]]; P2_ = X[T[:, 2]]
    for k, (r, z) in enumerate(pts):
        J00 = P1[:, 0]-P0[:, 0]; J01 = P2_[:, 0]-P0[:, 0]; J10 = P1[:, 1]-P0[:, 1]; J11 = P2_[:, 1]-P0[:, 1]
        det = J00*J11 - J01*J10
        xi = ((r-P0[:, 0])*J11 - (z-P0[:, 1])*J01)/det; eta = (-(r-P0[:, 0])*J10 + (z-P0[:, 1])*J00)/det
        ok = np.where((xi > -1e-9) & (eta > -1e-9) & (xi+eta < 1+1e-9))[0]
        if not len(ok): continue
        e = ok[0]; tri = T[e]; P = X[tri]
        J = np.array([P[1]-P[0], P[2]-P[0]]).T; Ji = np.linalg.inv(J)
        N, dN = p2(xi[e], eta[e]); g = (dN @ Ji).T @ Phi[tri]
        res[k] = [N @ Phi[tri], g[0], g[1]]
    return res

def integrals(X, T, idx, mode, Rfun, z0, zs):
    """Integrals per mode with f normalised so that int_0^a f^2 r dr = 1 (theta factors cancel):
       E  = int (|grad Phi|^2 + m^2 Phi^2/r^2) r dr dz  (= lam by Green's identity, a check)
       Iw = int_wall (Phi_l^2 + m^2 Phi^2/r^2) r dl ; Ib = floor ; Is = surface ; Px = int f r^2 dr (m=1)."""
    m, Phi = mode['m'], mode['Phi']
    E = 0.0
    for tri in T:
        P = X[tri]; J = np.array([P[1]-P[0], P[2]-P[0]]).T; detJ = abs(np.linalg.det(J)); Ji = np.linalg.inv(J)
        for (xi, eta), w in zip(QP, QW):
            N, dN = p2(xi, eta); g = (dN @ Ji).T @ Phi[tri]; r = N @ P[:, 0]; ph = N @ Phi[tri]
            E += w*detJ*(r*(g @ g) + m*m*ph*ph/r)
    def line(pts_fn, a, b, npts=400):
        u = np.linspace(a, b, npts); P = np.array([pts_fn(t) for t in u])
        G = grad_at(X, T, Phi, P); tot = 0.0; vals = []
        for k in range(npts):
            r = P[k, 0]
            if k == 0: tvec = P[1]-P[0]
            elif k == npts-1: tvec = P[-1]-P[-2]
            else: tvec = P[k+1]-P[k-1]
            tvec = tvec/np.linalg.norm(tvec)
            dl = (G[k, 1]*tvec[0] + G[k, 2]*tvec[1])
            vals.append((dl*dl + (m*m*G[k, 0]**2/r**2 if r > 1e-12 else 0.0))*r)
        L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
        return np.trapezoid(np.array(vals), L)
    def chain(nodes):
        """Integrate along mesh boundary nodes (the straight chords the mesh really has)."""
        P = X[nodes]; tot = 0.0
        for a_, b_ in zip(P[:-1], P[1:]):
            L = np.linalg.norm(b_ - a_); tvec = (b_ - a_)/L
            c_ = 0.5*(a_ + b_); inward = np.array([-(c_[0]) , 0.0])*1e-9
            q = np.array([a_ + (b_ - a_)*(x+1)/2 for x in G3]) + inward
            q[:, 0] = np.maximum(q[:, 0], 1e-9)
            G = grad_at(X, T, Phi, q)
            for k in range(3):
                r = q[k, 0]; dl = G[k, 1]*tvec[0] + G[k, 2]*tvec[1]
                tot += W3[k]*L/2*(dl*dl + m*m*G[k, 0]**2/r**2)*r
        return tot
    Iw = chain(idx[:, -1][::-1][::-1])
    Ib = chain(idx[0, :])
    Is = chain(idx[-1, :])
    rs, f = mode['rs'], mode['f']
    Px = surf_int(rs, f, lambda r: r*r) if m == 1 else 0.0
    return dict(E=E, Iw=Iw, Ib=Ib, Is=Is, Px=Px)
