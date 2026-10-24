"""Numerical engine for the second blade on a turning blade (L1-L4), vectorised over an ensemble with numpy.
The machine is RigidBlade: a thin uniform rod of mass m and length l, hinged at radius r_p (the 63 m tip of the NREL 5-MW
blade) and turning in the rotor plane by q from the blade's outward radial direction (absolute angle phi + q):
  I q'' = -(m l/2) [Om^2 r_p sin q + g cos(phi + q)] - Omd (I + (m l/2) r_p cos q) - a_e (m l/2) cos q - c q',   I = m l^2/3
  Om(t), Omd(t): rotor speed and its rate; a_e(t): edgewise acceleration of the hinge along the blade's tangent (L3).
The brake makes the equation stiff: at the best brake a disturbance of the swing relaxes some hundreds of times faster than
the rotor turns.  Scheme: three-stage Radau IIA collocation (order 5, stage order 3, L-stable; Hairer & Wanner, Solving ODEs
II, section IV.5), fixed step, simplified Newton iterations with a finite-difference Jacobian, vectorised over the ensemble.
The harvested energy E is carried as an extra state, E' = generator power, so it is integrated to the same order.
(The point and double pendula of the earlier study, Single and Double, were removed with the scripts that used them.)
"""
import numpy as np

S6 = np.sqrt(6.0)
RA = np.array([[(88 - 7*S6)/360, (296 - 169*S6)/1800, (-2 + 3*S6)/225],
               [(296 + 169*S6)/1800, (88 + 7*S6)/360, (-2 - 3*S6)/225],
               [(16 - S6)/36, (16 + S6)/36, 1/9]])
RC = np.array([(4 - S6)/10, (4 + S6)/10, 1.0])
RB = RA[2]
# order conditions (fail loudly if a coefficient is mistyped): quadrature order 5, stage order 3
for k in range(5):
    assert abs(RB @ RC**k - 1/(k + 1)) < 1e-14
for k in range(3):
    assert np.max(np.abs(RA @ RC**k - RC**(k + 1)/(k + 1))) < 1e-14

class RigidBlade:
    """The second blade: a thin uniform rod of mass m and length l hinged at radius r_p, brake c on q'.  State block: q, w.
    I q'' = -(m l/2)[Om^2 r_p sin q + g cos(phi + q)] - Omd (I + (m l/2) r_p cos q) - a_e (m l/2) cos q - c q',  I = m l^2/3
    (blade.py derives it twice)."""
    n = 1
    def __init__(self, m, l, rp, c, g=9.80665):
        self.m, self.l, self.rp, self.c, self.g = m, l, rp, c, g
        self.I, self.mlc = m*l**2/3, m*l/2
    def acc(self, q, w, phi, Om, Omd, ae):
        q1 = q[..., 0]; w1 = w[..., 0]; I, mlc, rp, g = self.I, self.mlc, self.rp, self.g
        f = (-mlc*(Om**2*rp*np.sin(q1) + g*np.cos(phi + q1)) - Omd*(I + mlc*rp*np.cos(q1)) - ae*mlc*np.cos(q1) - self.c*w1)
        return (f/I)[..., None], self.c*w1**2

def pendulum_rhs(sys_, rotor=None, Om=None, edge=None):
    """F(t, Y) for Y = [q (n), w (n), E] per member; rotor(t) -> (phi, Om, Omd) (default uniform at Om), edge(t) -> a_e."""
    n = sys_.n
    def F(t, Y):
        if rotor is None:
            ph, O, Od = Om*t, Om, 0.0
        else:
            ph, O, Od = rotor(t)
        ae = 0.0 if edge is None else edge(t)
        q = Y[..., :n]; w = Y[..., n:2*n]
        a, P = sys_.acc(q, w, ph, O, Od, ae)
        return np.concatenate([w, a, P[..., None]], axis=-1)
    return F

def radau_step(F, t, Y, h, tol=1e-12, maxit=12, J=None, eps=1e-7):
    """One fixed step of 3-stage Radau IIA for the batch Y (N, d).  Simplified Newton with the Jacobian at (t, Y).
    Returns the new state and the number of Newton iterations used (max over the batch)."""
    N, d = Y.shape
    F0 = F(t, Y)
    if J is None:                                   # finite-difference Jacobian, forward, per member: (N, d, d)
        J = np.empty((N, d, d))
        for j in range(d):
            dy = eps*np.maximum(1.0, np.abs(Y[:, j]))
            Yp = Y.copy(); Yp[:, j] += dy
            J[:, :, j] = (F(t, Yp) - F0)/dy[:, None]
    # Newton matrix  I - h (A kron J): (N, 3d, 3d)
    Mbig = np.zeros((N, 3*d, 3*d))
    for i in range(3):
        for k in range(3):
            Mbig[:, i*d:(i + 1)*d, k*d:(k + 1)*d] = (i == k)*np.eye(d) - h*RA[i, k]*J
    # LU once per step: solve with the same matrix in every iteration via explicit inverse (small, batched)
    Minv = np.linalg.inv(Mbig)
    Z = (h*RC[None, :, None])*F0[:, None, :]          # starting guess: Z_i = c_i h F(y_n)
    it = 0
    for it in range(1, maxit + 1):
        Fz = np.stack([F(t + RC[i]*h, Y + Z[:, i]) for i in range(3)], axis=1)     # (N, 3, d)
        G = Z - h*np.einsum('ik,nkd->nid', RA, Fz)
        dZ = -np.einsum('nab,nb->na', Minv, G.reshape(N, 3*d)).reshape(N, 3, d)
        Z = Z + dZ
        err = np.max(np.abs(dZ)/(1.0 + np.abs(Z)))
        if err < tol:
            break
    radau_step.last_err = err                         # the last Newton correction, relative: read by L4_check.py
    return Y + Z[:, 2], it                            # stiffly accurate: y_{n+1} = y_n + Z_3

def integrate(F, Y0, t0, t1, h, record_every=None, lyap=None):
    """Integrate with fixed step h.  record_every: store Y every that many steps.
    lyap: None or (d0, n_ren, idx, t_from[, weights]): Y0 holds base members first and perturbed copies second (same order);
    every n_ren steps the separation in the components idx (each multiplied by its weight) is measured, logged after t_from,
    and renormalised to d0."""
    Y = np.array(Y0, float)
    nsteps = int(round((t1 - t0)/h))
    rec = []; maxit = 0
    if lyap is not None:
        d0, n_ren, idx, t_from = lyap[:4]
        wts = np.asarray(lyap[4], float) if len(lyap) > 4 else np.ones(len(idx))
        Nb = Y.shape[0]//2; lsum = np.zeros(Nb); Tl = 0.0
    for k in range(nsteps):
        t = t0 + k*h
        Y, it = radau_step(F, t, Y, h)
        maxit = max(maxit, it)
        if record_every and (k + 1) % record_every == 0:
            rec.append((t + h, Y.copy()))
        if lyap is not None and (k + 1) % n_ren == 0:
            base, pert = Y[:Nb], Y[Nb:]
            dv = pert[:, idx] - base[:, idx]
            dist = np.sqrt(np.sum((dv*wts)**2, axis=1))
            if t + h > t_from:
                lsum += np.log(dist/d0); Tl += n_ren*h
            pert = pert.copy(); pert[:, idx] = base[:, idx] + dv*(d0/dist)[:, None]
            Y = np.concatenate([base, pert])
    out = {'Y': Y, 'rec': rec, 'maxit': maxit}
    if lyap is not None:
        out['lyap'] = lsum/max(Tl, 1e-300)
    return out
