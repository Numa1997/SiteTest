"""Power theorem (brief 4.3): a pendulum chain whose pivot is shaken along a unit vector e with white-noise acceleration
a(t), <a(t) a(t')> = S delta(t - t'), takes on average the power (S/2) <b^T M(q)^-1 b> from the shaking, whatever the
stiffness, damping, gravity, nonlinearity or chaos; and b^T M^-1 b <= total mass, with equality only when every rod is
perpendicular to e.

Run: python3 -I power_theorem.py   (symbolic part; prints PASS/FAIL, exit 1 on any FAIL)
The Monte Carlo check is power_theorem_mc.py.

Part A  generalised force of the shaking:  -a(t) b(q),  b_k = sum_i m_i e . dx_i/dq_k = dPhi/dq_k,  Phi = M_tot e . x_cm
Part B  Ito's rule on H(q, p) = (p - A)^T M^-1 (p - A)/2 + V: the noise adds (S/2) b^T (d^2H/dp^2) b = (S/2) b^T M^-1 b
        to the mean energy rate; its coefficient depends on q only, so Ito and Stratonovich agree
Part C  M_tot - b^T M^-1 b as an explicit sum of squares for the single and the double pendulum
"""
import sys
import sympy as sp

fails = 0
def check(name, expr):
    global fails
    ok = sp.simplify(expr) == 0
    fails += (not ok)
    print(('PASS ' if ok else 'FAIL ') + name)


def trig_zero(expr, angles):
    """Exact test that a trigonometric expression vanishes identically: expand every angle into its own sin and cos,
    substitute the half-angle (Weierstrass) parametrisation, and cancel the resulting rational function."""
    e = sp.expand_trig(expr)
    for a in angles:
        tt = sp.Symbol('tau_' + str(a), real=True)
        e = e.subs({sp.sin(a): 2*tt/(1 + tt**2), sp.cos(a): (1 - tt**2)/(1 + tt**2)})
    return sp.cancel(sp.together(e))

t = sp.symbols('t', real=True)
X = sp.Function('X')(t)                       # pivot displacement along e
ex, ey = sp.symbols('e_x e_y', real=True)     # e = (e_x, e_y), unit
g = sp.symbols('g', positive=True)

def chain(n):
    """n-link planar pendulum, absolute rod angles psi_k from the downward vertical, pivot at X(t) e."""
    ms = sp.symbols(f'm1:{n+1}', positive=True)
    Ls = sp.symbols(f'L1:{n+1}', positive=True)
    psi = [sp.Function(f'psi{k+1}')(t) for k in range(n)]
    pos, x, y = [], X*ex, X*ey
    for k in range(n):
        x = x + Ls[k]*sp.sin(psi[k]); y = y - Ls[k]*sp.cos(psi[k])
        pos.append((x, y))
    return ms, Ls, psi, pos

for n in (1, 2):
    ms, Ls, psi, pos = chain(n)
    Mtot = sum(ms)
    T = sum(m/2*(sp.diff(px, t)**2 + sp.diff(py, t)**2) for m, (px, py) in zip(ms, pos))
    V = sum(m*g*py for m, (px, py) in zip(ms, pos))
    Lag = T - V
    q = psi; qd = [sp.diff(s, t) for s in q]
    # the same chain with the pivot held still
    T0 = T.subs(X, 0).doit(); V0 = V.subs(X, 0)
    # Part A: EL(with shaking) - EL(pivot still) = Xddot * b_k
    Phi = sum(m*(px*ex + py*ey) for m, (px, py) in zip(ms, pos)).subs(X, 0)   # M_tot e . x_cm (pivot at origin)
    b = [sp.diff(Phi, s) for s in q]
    for k in range(n):
        EL = sp.diff(sp.diff(Lag, qd[k]), t) - sp.diff(Lag, q[k])
        EL0 = sp.diff(sp.diff(T0 - V0, qd[k]), t) - sp.diff(T0 - V0, q[k])
        resid = sp.expand(EL - EL0 - sp.diff(X, t, 2)*b[k])
        # e is a unit vector: the X-velocity cross terms cancel identically, no need of e_x^2 + e_y^2 = 1 here
        check(f'A  n={n}: shaking enters coordinate psi{k+1} only as -Xddot*b_{k+1}, b = grad(M_tot e.x_cm)', resid)
    # mass matrix
    Mmat = sp.Matrix(n, n, lambda i, j: sp.diff(T0, qd[i], qd[j]))
    Mmat = sp.simplify(Mmat)
    # Part B: Hamiltonian kinetic part p^T M^-1 p / 2 (with or without a gyroscopic vector A, d^2H/dp^2 = M^-1)
    ps = sp.symbols(f'p1:{n+1}', real=True)
    A = sp.symbols(f'A1:{n+1}', real=True)
    pv = sp.Matrix(ps); Av = sp.Matrix(A)
    Minv = Mmat.inv()
    H = ((pv - Av).T*Minv*(pv - Av))[0]/2
    hess = sp.Matrix(n, n, lambda i, j: sp.diff(H, ps[i], ps[j]))
    bv = sp.Matrix(b)
    ito = (bv.T*hess*bv)[0]/2
    meff = sp.simplify((bv.T*Minv*bv)[0])
    check(f'B  n={n}: Ito term (1/2) b^T (d2H/dp2) b = (1/2) b^T M^-1 b, also with a gyroscopic vector A', sp.simplify(ito - meff/2))
    # the noise coefficient -b(q) sqrt(S) multiplies dW in dp only and depends on q only: Ito = Stratonovich
    # (the Wong-Zakai drift (1/2) sum_j sigma_j d sigma/d p_j vanishes because d b/d p = 0)
    check(f'B  n={n}: noise coefficient independent of p (Ito = Stratonovich)', sum(sp.diff(bk, s) for bk in b for s in ps))
    # Part C: M_tot - m_eff as a sum of squares, with e = (cos a, sin a)
    al = sp.symbols('alpha', real=True)
    s_ = [sp.symbols(f's{k+1}', real=True) for k in range(n)]
    sub = {ex: sp.cos(al), ey: sp.sin(al)}
    sub.update({psi[k]: s_[k] for k in range(n)})
    deficit = sp.simplify((Mtot - meff).subs(sub))
    if n == 1:
        m1 = ms[0]
        target = m1*sp.sin(s_[0] - al)**2          # m (e . rod)^2, rod direction (sin psi, -cos psi): the mass pulled along the rod
        check('C  n=1: M - m_eff = m (e . rod direction)^2 >= 0, zero iff the rod is perpendicular to e', deficit - target)
    else:
        m1, m2 = ms
        D = m1 + m2*sp.sin(s_[0] - s_[1])**2      # det M / (m2 L1^2 L2^2) > 0
        u1 = sp.sin(s_[0] - al); u2 = sp.sin(s_[1] - al)   # e . rod_k, rod direction (sin psi_k, -cos psi_k)
        # sum of squares from the projection picture: M - m_eff = |(1 - P) w|^2 with w = (sqrt(m1) e, sqrt(m2) e) and P the
        # mass-weighted projector on the velocities the chain can have. Turning psi1 with the absolute psi2 held fixed moves
        # BOTH masses by L1 t1, so
        #   M - m_eff = m1 (e.r1)^2 + m1 m2 (e.r2 + sin(psi1 - psi2) e.t1)^2 / (m1 + m2 sin^2(psi1 - psi2))
        w1 = sp.cos(s_[0] - al)                              # e . t1, t1 = (cos psi1, sin psi1) the swing direction of rod 1
        Dl = s_[0] - s_[1]
        cand = m1*u1**2 + m1*m2*(u2 + sp.sin(Dl)*w1)**2/(m1 + m2*sp.sin(Dl)**2)
        check('C  n=2: M - m_eff = m1 (e.r1)^2 + m1 m2 (e.r2 + sin(psi1-psi2) e.t1)^2/(m1 + m2 sin^2(psi1-psi2)) >= 0',
              trig_zero(deficit - cand, [al, s_[0], s_[1]]))
        # equality iff the TOP rod is perpendicular to e, whatever the lower rod does (corrects brief 4.3, "every rod")
        check('C  n=2: m_eff = M_tot whenever rod 1 is perpendicular to e (psi1 = alpha), for ANY psi2',
              sp.simplify(deficit.subs(s_[0], al)))
        check('C  n=2: m_eff = M_tot also when both rods are perpendicular to e (psi1 = alpha, psi2 = alpha + pi)',
              sp.simplify(deficit.subs({s_[0]: al, s_[1]: al + sp.pi})))
        import random
        random.seed(1); worst = float('inf')
        f = sp.lambdify((m1, m2, al, s_[0], s_[1]), deficit, 'math')
        for _ in range(20000):
            worst = min(worst, f(random.uniform(.01, 1), random.uniform(.01, 1), random.uniform(-3, 3),
                                 random.uniform(-6, 6), random.uniform(-6, 6)))
        print(f'   min of M - m_eff over 20000 random states and masses: {worst:.3e} (>= 0)')
    print(f'   n={n}: m_eff = {sp.simplify(meff.subs(sub))}')

print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
