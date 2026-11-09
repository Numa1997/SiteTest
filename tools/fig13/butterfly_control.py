"""Can a motor at the top pivot catch the double pendulum out of chaos and hold it on the butterfly?

Method (skill phyein-usul-first-principles-control, section 8, for a periodic orbit instead of a resting point):
  plant      Hamilton's equations of hunt.rhs with a torque tau(t) of a motor between the support and the upper rod. In the
             Lagrangian the motor enters as a generalised force on theta1: dp1/dt gains + tau (Q1 = tau, Q2 = 0).
  target     the butterfly orbit s*(t) (gift/orbit24.json), period T, sampled at M points a lap.
  linearise  along the orbit: over each step h = T/M, ds_{k+1} = Phi_k ds_k + B_k tau_k (variational equations, exact Jacobian).
  check      controllability of the lap map (rank of [B, Phi B, ...] collected over one lap).
  design     periodic LQR: cost sum(ds^T Q ds + R tau^2); the periodic Riccati equation iterated backwards over laps to a
             fixed point gives gains K_k, tau_k = -K_k ds_k.
  phases     1 pump: tau = sat(kE (E* - E) dtheta1/dt) raises the energy to E* (dE/dt = tau dtheta1/dt);
             2 catch: once close to the orbit (distance to the nearest orbit point, phase free), tau = sat(-K_k ds) with the
               reference re-indexed to the nearest point of the lap each step (the clock of the orbit follows the pendulum).
  verify     on the full nonlinear equations, RK4 at the same step, torque held constant over a step (zero-order hold).

    python3 tools/fig13/butterfly_control.py OUTDIR
"""
import sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import solve_discrete_are
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from butterfly_physics import COEF, F, P1, P2, T, N, jacobian_fn, RTOL, ATOL
from hunt import energy

M = 2400                       # steps a lap
H = T / M                      # s
E_STAR = energy(COEF, [0, 0, P1, P2])
Q = np.diag([1.0, 1.0, 0.05, 0.05])     # weights: angles in rad, momenta in kg m^2/s
R_TAU = 1e-3                             # weight on torque, per (N m)^2
TAU_MAX = 60.0                           # N m: motor limit (both phases)


def orbit_and_linearisation():
    J = jacobian_fn()
    def g(t, y):
        s = y[:4]; Phi = y[4:20].reshape(4, 4)
        Js = np.array(J(*s), float)
        return np.concatenate([F(t, s), (Js @ Phi).ravel(), Js @ y[20:] + np.array([0, 0, 1.0, 0])])
    S = np.zeros((M + 1, 4)); PHI = np.zeros((M, 4, 4)); B = np.zeros((M, 4))
    s = np.array([0, 0, P1, P2], float); S[0] = s
    for k in range(M):
        y0 = np.concatenate([s, np.eye(4).ravel(), np.zeros(4)])
        y = solve_ivp(g, (0, H), y0, method='DOP853', rtol=1e-11, atol=1e-12).y[:, -1]
        s = y[:4]; S[k + 1] = s; PHI[k] = y[4:20].reshape(4, 4); B[k] = y[20:]
    return S, PHI, B


def periodic_lqr(PHI, B, laps=40):
    P = np.eye(4) * 0
    K = np.zeros((M, 4))
    for lap in range(laps):
        Pold = P.copy()
        for k in range(M - 1, -1, -1):
            A, b = PHI[k], B[k][:, None]
            S = R_TAU + (b.T @ P @ b)[0, 0]
            K[k] = (b.T @ P @ A)[0] / S
            P = Q * H + A.T @ P @ A - (A.T @ P @ b) @ (b.T @ P @ A) / S
        if lap and np.abs(P - Pold).max() < 1e-9 * np.abs(P).max(): break
    return K, P, lap


def controllability(PHI, B):
    """Reachable directions in one lap: the lap map's controllability Gramian, Phi(T, t_k) B_k summed."""
    W = np.zeros((4, 4)); Ph = np.eye(4)
    for k in range(M - 1, -1, -1):
        v = Ph @ B[k]; W += np.outer(v, v) * H; Ph = Ph @ PHI[k]
    return np.linalg.eigvalsh(W)


def rk4(s, tau):
    def f(s): d = np.array(F(0, s)); d[2] += tau; return d
    a = f(s); b = f(s + .5 * H * a); c = f(s + .5 * H * b); d = f(s + H * c)
    return s + H / 6 * (a + 2 * b + 2 * c + d)


def unwrap_ref(S, k, s):
    """Orbit point k shifted by whole turns so that its angles are nearest the pendulum's."""
    r = S[k].copy()
    for i in (0, 1): r[i] += 2 * math.pi * round((s[i] - r[i]) / (2 * math.pi))
    return r


def nearest(S, s, k_guess, window):
    ks = (k_guess + np.arange(-window, window + 1)) % M
    best, kb = 1e9, k_guess
    for k in ks:
        d = s - unwrap_ref(S, k, s); v = d @ Q @ d
        if v < best: best, kb = v, k
    return kb, math.sqrt(best)


def run(S, K, s0, seconds, kE=0.02, catch_at=0.6, log_every=10):
    s = np.array(s0, float); k = 0; mode = 'pump'; out = []
    k, dist = nearest(S, s, 0, M // 2)
    for i in range(int(seconds / H)):
        E = energy(COEF, s)
        if mode == 'pump':
            w1 = F(0, s)[0]
            tau = float(np.clip(kE * (E_STAR - E) * w1, -TAU_MAX, TAU_MAX))
            if i % 20 == 0:
                k, dist = nearest(S, s, k, M // 2)
                if dist < catch_at and abs(E - E_STAR) < 5: mode = 'catch'
        if mode == 'catch':
            k, dist = nearest(S, s, (k + 1) % M, 30)
            ds = s - unwrap_ref(S, k, s)
            tau = float(np.clip(-K[k] @ ds, -TAU_MAX, TAU_MAX))
        if i % log_every == 0:
            out.append((i * H, E, dist, tau, mode == 'catch', *s))
        s = rk4(s, tau)
        if not np.all(np.isfinite(s)) or abs(s[2]) > 1e4: break
    return np.array(out)


def main(outdir):
    import pathlib; out = pathlib.Path(outdir); out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    S, PHI, B = orbit_and_linearisation()
    Mlap = np.eye(4)
    for k in range(M): Mlap = PHI[k] @ Mlap
    mult = np.linalg.eigvals(Mlap)
    print('orbit + linearisation %.0f s; lap multipliers %s; closure %s' % (time.time() - t0, np.round(mult, 5), np.round(S[-1] - S[0] - [0, 2 * math.pi * N, 0, 0], 8)))
    gram = controllability(PHI, B)
    print('controllability Gramian eigenvalues (one lap):', gram)
    K, P, laps = periodic_lqr(PHI, B)
    print('periodic LQR converged after %d laps; |K| from %.1f to %.1f N m per unit error' % (laps, np.abs(K).max(1).min(), np.abs(K).max(1).max()))
    # closed-loop lap map: should have all multipliers inside the unit circle (except none: the flow direction is controlled too)
    Mc = np.eye(4)
    for k in range(M): Mc = (PHI[k] - np.outer(B[k], K[k])) @ Mc
    print('closed-loop lap multipliers', np.round(np.abs(np.linalg.eigvals(Mc)), 5))
    np.savez(out / 'control_design.npz', S=S, K=K, B=B)
    res = {}
    r = run(S, K, S[0] + [0.1, -0.1, 0, 0], 15, catch_at=10)          # nudged 0.1 rad: orbit-following LQR from the start
    res['nudge 0.1 rad'] = dict(dist_at_5s=float(r[np.argmin(abs(r[:, 0] - 5)), 2]), dist_end=float(r[-1, 2]), tau_max=float(np.abs(r[:, 3]).max()))
    print('nudge 0.1 rad:', res['nudge 0.1 rad'])
    for p in ((2.0, 4.0), (3.0, 6.0), (5.0, -3.0), (-2.0, 5.0), (1.0, 8.0), (0.0, 0.5), (-4.0, 3.0)):
        r, tm = pump_wait_catch(S, K, [0, 0, *p], 300)
        c = r[r[:, 4] == 2]
        res['pump-wait-catch from p = %s' % (p,)] = dict(E0=energy(COEF, [0, 0, *p]), times=tm, caught=bool(len(c)),
            dist_end=float(c[-1, 2]) if len(c) else None, catch_tau_max=float(np.abs(c[:, 3]).max()) if len(c) else None)
        print(p, res['pump-wait-catch from p = %s' % (p,)])
    json.dump(dict(M=M, Q=np.diag(Q).tolist(), R=R_TAU, tau_max=TAU_MAX, multipliers=[str(m) for m in mult], gramian=gram.tolist(), runs=res),
              open(out / 'control.json', 'w'), indent=1)



def track(S, K, s0, k0, seconds, log_every=10):
    """Time-locked tracking: the reference runs on its own clock from orbit point k0 (no re-indexing)."""
    s = np.array(s0, float); out = []
    for i in range(int(seconds / H)):
        k = (k0 + i) % M
        ref = S[k] + np.array([0, 2 * math.pi * N * ((k0 + i) // M), 0, 0])
        ds = s - ref
        tau = float(np.clip(-K[k] @ ds, -TAU_MAX, TAU_MAX))
        if i % log_every == 0: out.append((i * H, energy(COEF, s), math.sqrt(ds @ Q @ ds), tau, 1, *s))
        s = rk4(s, tau)
        if not np.all(np.isfinite(s)) or abs(s[2]) > 1e4: break
    return np.array(out)


def periodic_lqr_transverse(S, PHI, B, laps=60):
    """Orbital (phase-free) design: the cost sees only the error across the orbit, not along it (the timing of the lap).
    Q_k = Pi_k^T Q Pi_k with Pi_k the Q-orthogonal projection that removes the flow direction f(s*_k)."""
    P = np.zeros((4, 4)); K = np.zeros((M, 4)); Qs = []
    for k in range(M):
        f = np.array(F(0, S[k])); Pi = np.eye(4) - np.outer(f, f @ Q) / (f @ Q @ f); Qs.append(Pi.T @ Q @ Pi)
    for lap in range(laps):
        Pold = P.copy()
        for k in range(M - 1, -1, -1):
            A, b = PHI[k], B[k][:, None]
            Sg = R_TAU + (b.T @ P @ b)[0, 0]
            K[k] = (b.T @ P @ A)[0] / Sg
            P = Qs[k] * H + A.T @ P @ A - (A.T @ P @ b) @ (b.T @ P @ A) / Sg
            P = 0.5 * (P + P.T)
        if lap and np.abs(P - Pold).max() < 1e-9 * np.abs(P).max(): break
    return K, P, lap


def pump_wait_catch(S, K, s0, seconds, kE=0.02, e_tol=0.5, catch_at=0.12, log_every=10):
    """1 pump the energy to E* (tau = sat(kE (E* - E) dtheta1/dt)); 2 wait, motor off, watching the distance to the nearest
    orbit point; 3 when it falls below catch_at, catch with the orbit-following LQR. Returns the log and the switch times."""
    s = np.array(s0, float); mode = 'pump'; out = []; k = 0; dist = 9.0; times = {}
    for i in range(int(seconds / H)):
        E = energy(COEF, s); tau = 0.0
        if mode == 'pump':
            tau = float(np.clip(kE * (E_STAR - E) * F(0, s)[0], -TAU_MAX, TAU_MAX))
            if abs(E - E_STAR) < e_tol: mode = 'wait'; times['wait'] = i * H; k, dist = nearest(S, s, 0, M // 2)
        elif mode == 'wait':
            if i % 4 == 0:
                k, dist = nearest(S, s, (k + 4) % M, 40)
                if i % 400 == 0: k, dist = nearest(S, s, k, M // 2)
            if dist < catch_at: mode = 'catch'; times['catch'] = i * H
        if mode == 'catch':
            k, dist = nearest(S, s, (k + 1) % M, 30)
            tau = float(np.clip(-K[k] @ (s - unwrap_ref(S, k, s)), -TAU_MAX, TAU_MAX))
        if i % log_every == 0: out.append((i * H, E, dist, tau, {'pump': 0, 'wait': 1, 'catch': 2}[mode], *s))
        s = rk4(s, tau)
    return np.array(out), times


if __name__ == '__main__':
    main(sys.argv[1])
