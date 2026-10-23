"""Numerical engine for pendula on a turning blade (L1-L3), vectorised over an ensemble with numpy.

Equations (L1_double.py, physical time, relative rod angles q_i from the blade's outward radial direction, absolute angle
phi + q_i; A = (m1+m2) l1^2, B = m2 l2^2, D = m2 l1 l2, d = q1 - q2):
  A q1'' + D cos d q2'' = -D sin d (Om + q2')^2 - (m1+m2) l1 [Om^2 r_p sin q1 + g cos(phi + q1)]
                          - Omd [(m1+m2) l1 (l1 + r_p cos q1) + D cos d] - a_e (m1+m2) l1 cos q1 - c0 q1' + c1 (q2' - q1')
  B q2'' + D cos d q1'' =  D sin d (Om + q1')^2 - m2 l2 [Om^2 r_p sin q2 + g cos(phi + q2)]
                          - Omd m2 l2 [l1 cos d + l2 + r_p cos q2] - a_e m2 l2 cos q2 - c1 (q2' - q1')
  single pendulum (mass m on length l): m l^2 q'' = -m l [Om^2 r_p sin q + g cos(phi + q)] - Omd m l (l + r_p cos q)
                                                   - a_e m l cos q - c q'
  Om(t), Omd(t): rotor speed and its rate; a_e(t): edgewise acceleration of the pivot along the blade's tangent (L3).
The generators make the equations stiff: a heavily braked double pendulum has a relaxation mode some thousands of times faster
than its swing.  Scheme: three-stage Radau IIA collocation (order 5, stage order 3, L-stable; Hairer & Wanner, Solving ODEs II,
section IV.5), fixed step, simplified Newton iterations with a finite-difference Jacobian, vectorised over the ensemble.
The harvested energy E is carried as an extra state, E' = generator power, so it is integrated to the same order.
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

class Single:
    """Single pendulum of mass m on length l, generator c on q'.  State block: q, w."""
    n = 1
    def __init__(self, m, l, rp, c, g=9.80665):
        self.m, self.l, self.rp, self.c, self.g = m, l, rp, c, g
    def acc(self, q, w, phi, Om, Omd, ae):
        q1 = q[..., 0]; w1 = w[..., 0]; m, l, rp, g = self.m, self.l, self.rp, self.g
        f = (-m*l*(Om**2*rp*np.sin(q1) + g*np.cos(phi + q1)) - Omd*m*l*(l + rp*np.cos(q1)) - ae*m*l*np.cos(q1)
             - self.c*w1)
        return (f/(m*l**2))[..., None], self.c*w1**2
    def reaction_t(self, q, w, a, phi, Om, Omd, ae):
        """tangential force the bob exerts on the pivot (blade frame), for the blade's edgewise mode (L3)."""
        raise NotImplementedError

class Double:
    """Double pendulum, generators c0 (pivot, on q1') and c1 (hinge, on q2' - q1').  State block: q1, q2, w1, w2."""
    n = 2
    def __init__(self, m1, m2, l1, l2, rp, c0, c1, g=9.80665):
        self.m1, self.m2, self.l1, self.l2, self.rp, self.c0, self.c1, self.g = m1, m2, l1, l2, rp, c0, c1, g
        self.Mt = m1 + m2; self.A = self.Mt*l1**2; self.B = m2*l2**2; self.D = m2*l1*l2
    def acc(self, q, w, phi, Om, Omd, ae):
        q1, q2 = q[..., 0], q[..., 1]; w1, w2 = w[..., 0], w[..., 1]
        d = q1 - q2; cd, sd = np.cos(d), np.sin(d)
        Mt, l1, l2, rp, g, D, m2 = self.Mt, self.l1, self.l2, self.rp, self.g, self.D, self.m2
        tq0 = self.c0*w1; tq1 = self.c1*(w2 - w1)
        f1 = (-D*sd*(Om + w2)**2 - Mt*l1*(Om**2*rp*np.sin(q1) + g*np.cos(phi + q1))
              - Omd*(Mt*l1*(l1 + rp*np.cos(q1)) + D*cd) - ae*Mt*l1*np.cos(q1) - tq0 + tq1)
        f2 = (D*sd*(Om + w1)**2 - m2*l2*(Om**2*rp*np.sin(q2) + g*np.cos(phi + q2))
              - Omd*m2*l2*(l1*cd + l2 + rp*np.cos(q2)) - ae*m2*l2*np.cos(q2) - tq1)
        M12 = D*cd; det = self.A*self.B - M12**2
        a1 = (self.B*f1 - M12*f2)/det; a2 = (self.A*f2 - M12*f1)/det
        return np.stack([a1, a2], axis=-1), self.c0*w1**2 + self.c1*(w2 - w1)**2

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
        if np.max(np.abs(dZ)/(1.0 + np.abs(Z))) < tol:
            break
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
