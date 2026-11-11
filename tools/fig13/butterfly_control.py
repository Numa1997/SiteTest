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
    Qd = np.diag(Q).copy(); Astar = swing_reach_of_orbit(S); rng = np.random.default_rng(1); held = []
    # A quick test of this Python controller only. The counts the page quotes (300 random starts) come from the page's own
    # controller, run by tools/fig13/catch_stats.cjs; this loop is not their source.
    for n in range(30):                                                  # catch from anywhere: 30 random strikes, 900 s each at most
        p = rng.uniform(-8, 8, 2)
        log, _, tm, hops = catch_anywhere(np.array([0, 0, *p]), S, K, Qd, H, 900.0, E_STAR, Astar, *SETTINGS, TAU_MAX, np.array(COEF), 10)
        ok = bool(log[-1, 5] == 2 and log[-1, 3] < 0.01); held.append((float(p[0]), float(p[1]), ok, float(tm[2]) if ok else None, int(hops)))
        print('strike (%.2f, %.2f): %s' % (p[0], p[1], ('caught at %.0f s after %d misses' % (tm[2], hops)) if ok else 'not caught in 900 s'))
    res['catch from anywhere'] = held
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


# ---- 4. Catch from anywhere: pump the energy AND steer the slow swing, then wait, then catch (compiled, 9 Nov 2026) --------
# Picture (P = p1 + p2, the total angular momentum, is the slow pendulum's momentum): the butterfly is a slow pendulum (the upper rod, swinging +-156.7 deg) carrying a fast spinner (the lower rod).
# One motor at the top pin reaches both: a torque along P feeds or brakes the swing (dP/dt = tau - gravity's torque); a torque that follows the full dtheta1/dt changes the total energy. Holding the energy at E* while the swing is
# steered to its target moves energy between swing and spin. With both right, the pendulum is on a motion next to the
# butterfly; the motor waits until the free motion passes close, then the orbit-following LQR catches it.
from numba import njit
from chaos_map import rk4 as rk4n


@njit
def _energy(s, A, B, C, U1, U2):
    c = np.cos(s[0] - s[1]); det = A * B - C * C * c * c
    return 0.5 * (B * s[2] ** 2 - 2 * C * c * s[2] * s[3] + A * s[3] ** 2) / det - U1 * np.cos(s[0]) - U2 * np.cos(s[1])


@njit
def _w1(s, A, B, C):
    c = np.cos(s[0] - s[1]); return (B * s[2] - C * c * s[3]) / (A * B - C * C * c * c)


@njit
def _nearest(S, Qd, s, kg, window, M, sg):
    """Nearest point of the butterfly (sg = +1) or of its mirror image (sg = -1: every angle and momentum negated, the same
    drawing flipped left to right, held by the same gains with the torque reversed)."""
    best = 1e18; kb = kg
    for j in range(-window, window + 1):
        k = (kg + j) % M
        v = 0.0
        for i in range(4):
            d = s[i] - sg * S[k, i]
            if i < 2: d -= 2 * np.pi * np.round(d / (2 * np.pi))
            v += Qd[i] * d * d
        if v < best: best = v; kb = k
    return kb, np.sqrt(best)


@njit
def _nearest2(S, Qd, s, kg, window, M, sg):
    """Search both the butterfly and its mirror when window is wide; keep the current one otherwise."""
    if window < M // 2: k, d = _nearest(S, Qd, s, kg, window, M, sg); return k, d, sg
    k1, d1 = _nearest(S, Qd, s, kg, window, M, 1.0); k2, d2 = _nearest(S, Qd, s, kg, window, M, -1.0)
    return (k1, d1, 1.0) if d1 <= d2 else (k2, d2, -1.0)


@njit
def catch_anywhere(s0, S, K, Qd, h, seconds, Estar, Astar, kE, kA, kI, kB, Pmin_lim, wait_max, steer_max, win, e_tol, a_tol, catch_at, lock_at, tau_max, coef, log_every):
    A_, B_, C_, U1, U2 = coef
    M = S.shape[0] - 1
    n = int(seconds / h); nl = n // log_every + 1
    log = np.zeros((nl, 10))     # t, E, A_est, dist, tau, mode, th1, th2, p1 ; then p2 stored separately
    p2log = np.zeros(nl)
    s = s0.copy(); mode = 0; k = 0; dist = 9.0; sg = 1.0; zA = 0.0; zE = 0.0
    nb = int(win / h); hist = np.zeros(nb) + abs(s0[2] + s0[3]); hi = 0; Aest = 0.0; t_mode = np.zeros(3); hops = 0; t_hop = -1.0; Pmin = 0.0; t_steer = 0.0; drain = False; E_low = 60.0; locked = False
    for i in range(n):
        E = _energy(s, A_, B_, C_, U1, U2); w1 = _w1(s, A_, B_, C_)
        Ptot = s[2] + s[3]                                        # the slow pendulum's momentum: dP/dt = tau - gravity's torque
        hist[hi] = abs(Ptot); hi = (hi + 1) % nb
        if i % 50 == 0: Aest = hist.max(); Pmin = hist.min()      # the swing's reach and its lowest |P| over the last win seconds
        tau = 0.0
        if mode == 0 and i * h - t_steer > steer_max:             # steering has not settled: shove
            hops += 1; t_hop = i * h; t_steer = i * h; zA = 0.0; zE = 0.0; drain = True
        if mode == 0 and t_hop >= 0 and drain:                    # a miss: drain back down into chaos (to E_low), then try again
            tau = kE * (E_low - E) * w1
            if E < E_low + 5.0 or i * h - t_hop > 6.0: drain = False; t_steer = i * h
        elif mode == 0:                                           # pump and steer
            if i * h > win and Pmin < Pmin_lim: zA += h * (Astar - Aest); zE += h * (Estar - E)       # memories: no steady error (PI, as Fig. 9)
            tau = (kE * (Estar - E) + kI * 0.05 * zE) * w1 + ((kA * (Astar - Aest) + kI * zA) if Pmin < Pmin_lim else -kB * (Pmin - Pmin_lim)) * Ptot   # energy in; reach fed or braked along P;
            # going round (|P| never dips, the butterfly's dips to 1.23 each swing) is braked until the upper rod swings
            if i * h > win and not drain and i * h - t_steer > win and Pmin < Pmin_lim and abs(E - Estar) < e_tol and abs(Aest - Astar) < a_tol:
                mode = 1; t_mode[1] = i * h; k, dist, sg = _nearest2(S, Qd, s, 0, M // 2, M, sg)
        elif mode == 1:                                           # wait, motor off
            if i % 4 == 0:
                k, dist, sg = _nearest2(S, Qd, s, (k + 4) % M, 40, M, sg)
                if i % 400 == 0: k, dist, sg = _nearest2(S, Qd, s, k, M // 2, M, sg)
            if dist < catch_at: mode = 2; t_mode[2] = i * h
            elif i * h - t_mode[1] > wait_max:                    # waited in vain: shove it onto another motion, steer again
                mode = 0; hops += 1; t_hop = i * h; t_steer = i * h; zA = 0.0; zE = 0.0; drain = True
        if mode == 2:                                             # catch and hold
            if locked:                                            # near: follow the orbit's own clock (the gains were designed for it)
                k = (k + 1) % M
                ds = s - sg * S[k]
                for j in range(2): ds[j] -= 2 * np.pi * np.round(ds[j] / (2 * np.pi))
                dist = 0.0
                for j in range(4): dist += Qd[j] * ds[j] * ds[j]
                dist = np.sqrt(dist)
            else:                                                 # still coming in: re-index to the nearest point each step
                k, dist, sg = _nearest2(S, Qd, s, (k + 1) % M, 30, M, sg)
                if dist < lock_at: locked = True
            ds = s - sg * S[k]
            for j in range(2): ds[j] -= 2 * np.pi * np.round(ds[j] / (2 * np.pi))
            tau = 0.0
            for j in range(4): tau -= K[k, j] * ds[j]
            if dist > 1.0:                                        # the catch slipped: a miss; drain into chaos and try again
                mode = 0; hops += 1; t_hop = i * h; t_steer = i * h; zA = 0.0; zE = 0.0; drain = True; tau = 0.0; locked = False
        tau = min(tau_max, max(-tau_max, tau))
        if i % log_every == 0:
            r = i // log_every
            log[r, 0] = i * h; log[r, 1] = E; log[r, 2] = Aest; log[r, 3] = dist; log[r, 4] = tau; log[r, 5] = mode
            log[r, 6] = s[0]; log[r, 7] = s[1]; log[r, 8] = s[2]; log[r, 9] = sg; p2log[r] = s[3]
        q1, q2, p1, p2 = s[0], s[1], s[2], s[3]                   # four RK4 sub-steps of h/4 (one control step, torque held):
        for sub in range(4):                                      # at h the free orbit drifts 2e-3 a lap, at h/4 4e-6 (measured 11 Nov 2026)
            p1 += 0.125 * h * tau                                 # torque as a kick split around each sub-step (2nd order)
            q1, q2, p1, p2 = rk4n(q1, q2, p1, p2, 0.25 * h, A_, B_, C_, U1, U2)
            p1 += 0.125 * h * tau
        s[0] = q1; s[1] = q2; s[2] = p1; s[3] = p2
    return log[:n // log_every], p2log[:n // log_every], t_mode, hops


def swing_reach_of_orbit(S):
    """The steering target: the largest |P| = |p1 + p2| on the butterfly."""
    return float(np.abs(S[:, 2] + S[:, 3]).max())


def film_data(p, t_free, seconds, out, log_every=4, hold_laps=2.0, free_laps=3.0):
    """The run shown in the catch film (gift/catch.html): both rods hanging still, struck with p, swinging freely (chaos) for
    t_free seconds, then the controller of section 4 (catch_anywhere, settings below) for the given seconds; every log_every
    steps: t, th1, th2, tau, E, distance, mode (-1 free, 0 pump/steer, 1 wait, 2 catch). Also the butterfly (one lap)."""
    S, PHI, B = orbit_and_linearisation()
    K, _, _ = periodic_lqr(PHI, B)
    Qd = np.diag(Q).copy(); Astar = swing_reach_of_orbit(S)
    s = np.array([0, 0, *p], float); free = []
    tt0 = np.arange(0, int(round(t_free / H)), log_every) * H
    sol0 = solve_ivp(F, (0, int(round(t_free / H)) * H), s, method='DOP853', rtol=RTOL, atol=ATOL, t_eval=np.append(tt0, int(round(t_free / H)) * H))
    for j, tj in enumerate(tt0): free.append((tj, energy(COEF, sol0.y[:, j]), 9.0, 0.0, -1, sol0.y[0, j], sol0.y[1, j]))
    s = sol0.y[:, -1].copy()
    t0 = int(round(t_free / H)) * H
    log, p2, tm, hops = catch_anywhere(s, S, K, Qd, H, seconds, E_STAR, Astar, *SETTINGS, TAU_MAX, np.array(COEF), log_every)
    free = np.array(free); log = log.copy(); log[:, 0] += t0; tm = tm + t0
    # let go: after hold_laps laps of holding, the motor switches off; free_laps laps of free motion (mode 3)
    keep = log[:, 0] <= tm[2] + hold_laps * T; log, p2 = log[keep], p2[keep]
    s = np.array([log[-1, 6], log[-1, 7], log[-1, 8], p2[-1]]); tr = log[-1, 0]; rel = []
    tt = np.arange(1, int(round(free_laps * T / (H * log_every))) + 1) * H * log_every       # free motion: DOP853 (RK4 at step H drifts 2e-3 a lap)
    sol = solve_ivp(F, (0, tt[-1]), s, method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tt)
    Qd1 = Qd.copy()
    for j, tj in enumerate(tt):
        y = sol.y[:, j]
        if j % 25 == 0: k, dd, sg = _nearest2(S, Qd1, y, 0, M // 2, M, 1.0)
        rel.append((tr + tj, energy(COEF, y), 0.0, dd, 0.0, 3, y[0], y[1]))
    rel = np.array(rel)
    log = np.vstack([log[:, :8], rel])
    log = np.vstack([np.column_stack([free[:, 0], free[:, 1], np.zeros(len(free)), free[:, 2], free[:, 3], free[:, 4], free[:, 5], free[:, 6]]),
                     log])
    r = lambda a, d: [round(float(v), d) for v in a]
    json.dump(dict(p=list(p), t_free=t0, release_t=float(tr), kt=KT, h=H * log_every, E_star=E_STAR, T=T, tau_max=TAU_MAX, catch_t=float(tm[2]), wait_t=float(tm[1]), hops=int(hops),
                   t=r(log[:, 0], 4), th1=r(log[:, 6], 5), th2=r(log[:, 7], 5), tau=r(log[:, 4], 3), E=r(log[:, 1], 2), dist=r(log[:, 3], 4),
                   mode=[int(m) for m in log[:, 5]], orbit_th1=r(S[::4, 0], 5), orbit_th2=r(S[::4, 1], 5)), open(out, 'w'), separators=(',', ':'))
    return tm, hops


# kE, kA, kI, kB, Pmin_lim, wait_max (s), steer_max (s), window (s), e_tol (J), a_tol (kg m^2/s), catch_at: the working settings
# (30 random strikes p in [-8, 8]^2, accurate integration: 28 caught and held within 900 s, 22 within 300 s; 9 November 2026)
KT = 2.5   # N m per A: torque constant assumed for the film's motor (a direct-drive torque motor; 60 N m at 24 A)
SETTINGS = (0.01, 0.05, 0.005, 0.0, 1e9, 12.0, 12.0, 3.0, 5.0, 3.0, 0.6, -1.0)   # as pendulum.js; its statistics: tools/fig13/catch_stats.cjs (this file's own 30-strike test in main() predates these settings)
