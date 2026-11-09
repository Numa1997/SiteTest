"""The butterfly orbit studied physically: what the machine does, how hard it works, and whether it survives a nudge.

Machine (all SI): two equal uniform rods, m = 1 kg, l = 1 m each, g = 9.8 m/s^2, frictionless pivots; angles th1, th2 from
straight down; conjugate momenta p1, p2 (hunt.py, chaos_map.coefficients). Butterfly: both rods hanging straight down, struck
with p = (P1, P2) below; it returns after T (gift/orbit24.json, butterfly.py).

Measured here:
  1. the strike as angular velocities; tip speed; the force on the top bearing (from the centre-of-mass acceleration)
  2. stability from the exact variational (linearised) equations over one lap: the Floquet multipliers. The earlier trace
     (hunt_inspect.floquet_trace, finite differences, eps 1e-6) is within 0.01 of 2, where butterfly.stability() calls it
     'neutral': it could not tell stable from unstable.
  3. twins: the butterfly and a copy struck 1 part in 10^6 differently, run side by side for many laps; the same for a
     low-energy strike, as a chaotic reference
  4. a long run of slightly mis-struck butterflies: does the pattern keep its shape (petal directions bounded) or break up

    python3 tools/fig13/butterfly_physics.py OUTDIR
"""
import sys, json, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from chaos_map import coefficients
from hunt import rhs, energy, BASE

G = 9.8
M, L = BASE['m1'], BASE['l1']
assert BASE['m1'] == BASE['m2'] and BASE['l1'] == BASE['l2'] and BASE['model'] == 'rods'
ORB = json.load(open(__file__.rsplit('/', 1)[0] + '/gift/orbit24.json'))
P1, P2, T, N = ORB['p1'], ORB['p2'], ORB['T'], ORB['N']
RTOL, ATOL = 1e-12, 1e-13
COEF = coefficients(dict(BASE, g=G))
F = rhs(COEF)


def jacobian_fn():
    """d(rhs)/d(state), exact (SymPy), for the variational equations."""
    A, B, C, U1, U2 = COEF
    q1, q2, p1, p2 = sp.symbols('q1 q2 p1 p2')
    c, s = sp.cos(q1 - q2), sp.sin(q1 - q2)
    det = A * B - C ** 2 * c ** 2
    w1 = (B * p1 - C * c * p2) / det
    w2 = (A * p2 - C * c * p1) / det
    e = C * w1 * w2 * s
    f = sp.Matrix([w1, w2, -e - U1 * sp.sin(q1), e - U2 * sp.sin(q2)])
    return sp.lambdify((q1, q2, p1, p2), f.jacobian([q1, q2, p1, p2]), 'numpy')


def monodromy():
    J = jacobian_fn()
    def g(t, y):
        s = y[:4]; Phi = y[4:].reshape(4, 4)
        return np.concatenate([F(t, s), (np.array(J(*s), float) @ Phi).ravel()])
    y0 = np.concatenate([[0, 0, P1, P2], np.eye(4).ravel()])
    sol = solve_ivp(g, (0, T), y0, method='DOP853', rtol=RTOL, atol=ATOL)
    end = sol.y[:, -1]
    closure = end[:4] - np.array([0, 2 * math.pi * N * np.sign(P2), P1, P2])
    return end[4:].reshape(4, 4), closure


def lap(n=20001):
    t = np.linspace(0, T, n)
    s = solve_ivp(F, (0, T), [0, 0, P1, P2], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=t, dense_output=True)
    return t, s.y


def physical(t, y):
    q1, q2, p1, p2 = y
    A, B, C, U1, U2 = COEF
    w = np.array([F(0, y[:, k])[:2] for k in range(y.shape[1])]).T
    w1, w2 = w
    tip = L * np.array([np.sin(q1) + np.sin(q2), -np.cos(q1) - np.cos(q2)])          # x, height (up), m
    vtip = L * np.hypot(np.cos(q1) * w1 + np.cos(q2) * w2, np.sin(q1) * w1 + np.sin(q2) * w2)
    # centre of mass of the two rods (each 1 kg): rod 1 centre at (l/2) e1, rod 2 centre at l e1 + (l/2) e2
    cm = 0.5 * (L * 0.5 * np.array([np.sin(q1), -np.cos(q1)]) + L * np.array([np.sin(q1) + 0.5 * np.sin(q2), -np.cos(q1) - 0.5 * np.cos(q2)]))
    dt = t[1] - t[0]
    acc = np.gradient(np.gradient(cm, dt, axis=1), dt, axis=1)
    Mtot = 2 * M
    Fpivot = Mtot * acc - Mtot * np.array([[0.0], [-G]])        # force the bearing exerts on the pendulum, N
    Fmag = np.hypot(*Fpivot)
    KE = np.array([energy(COEF, y[:, k]) for k in range(y.shape[1])]) + U1 * np.cos(q1) + U2 * np.cos(q2)
    PE = -U1 * np.cos(q1) - U2 * np.cos(q2)
    D = q2 - q1
    return dict(w1=w1, w2=w2, tip=tip, vtip=vtip, Fmag=Fmag, KE=KE, PE=PE, D=D)


def twins(p, dp, laps, n_per_lap=400):
    """Two pendulums struck p and p + dp: separation of their tips (m) and of their states, sampled n_per_lap times a lap."""
    tt = np.linspace(0, laps * T, laps * n_per_lap + 1)
    a = solve_ivp(F, (0, tt[-1]), [0, 0, *p], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tt).y
    b = solve_ivp(F, (0, tt[-1]), [0, 0, p[0] + dp[0], p[1] + dp[1]], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tt).y
    tipa = np.array([np.sin(a[0]) + np.sin(a[1]), -np.cos(a[0]) - np.cos(a[1])])
    tipb = np.array([np.sin(b[0]) + np.sin(b[1]), -np.cos(b[0]) - np.cos(b[1])])
    return tt, np.hypot(*(tipa - tipb)), a, b


def petals(p, laps):
    """Direction of each petal (arm straight, D = 2 pi n) from straight down, degrees, over many laps."""
    sgn = 1.0
    ev = lambda t, y: math.sin(0.5 * (y[1] - y[0]))
    ev.direction = 0
    sol = solve_ivp(F, (0, laps * T), [0, 0, *p], method='DOP853', rtol=1e-10, atol=1e-11, events=ev)
    ye = sol.y_events[0]
    keep = np.cos(0.5 * (ye[:, 1] - ye[:, 0])) ** 2 > 0.5      # sin(D/2) = 0 at D = 2 pi n (cos^2 = 1), not D = pi (2n+1)
    return sol.t_events[0][keep], np.degrees([math.remainder(v, 2 * math.pi) for v in ye[keep, 0]])


def main(out):
    import pathlib; out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    R = {}
    A, B, C, U1, U2 = COEF
    w0 = F(0, [0, 0, P1, P2])
    R['strike'] = dict(p1=P1, p2=P2, w1=w0[0], w2=w0[1], E=energy(COEF, [0, 0, P1, P2]), T=T, N=N)
    Mo, closure = monodromy()
    ev = np.linalg.eigvals(Mo)
    R['closure'] = closure.tolist(); R['multipliers'] = sorted(ev.tolist(), key=lambda z: -abs(z)); R['trace4'] = float(np.trace(Mo).real)
    R['detM'] = float(np.linalg.det(Mo))
    t, y = lap()
    ph = physical(t, y)
    R['lap'] = dict(w1_range=[float(ph['w1'].min()), float(ph['w1'].max())], w2_range=[float(ph['w2'].min()), float(ph['w2'].max())],
                    th1_range_deg=[float(np.degrees(y[0].min())), float(np.degrees(y[0].max()))],
                    vtip_range=[float(ph['vtip'].min()), float(ph['vtip'].max())],
                    F_pivot_max_N=float(ph['Fmag'][50:-50].max()), F_pivot_mean_N=float(ph['Fmag'][50:-50].mean()),
                    weight_N=2 * M * G, KE_range=[float(ph['KE'].min()), float(ph['KE'].max())], PE_range=[float(ph['PE'].min()), float(ph['PE'].max())],
                    D_turns=float((y[1, -1] - y[0, -1]) / (2 * math.pi)), int_w1sq=float(np.trapezoid(ph['w1'] ** 2, t)),
                    int_Dsq=float(np.trapezoid(np.gradient(ph['D'], t) ** 2, t)))
    print(json.dumps(R, indent=1, default=str))
    np.savez(out / 'lap.npz', t=t, y=y, **{k: v for k, v in ph.items()})
    json.dump(R, open(out / 'physics.json', 'w'), indent=1, default=str)



# ---- 5. Which strikes make a butterfly: a map of strike space (both rods hanging still, struck with p1, p2) ----------------
from numba import njit, prange
from chaos_map import rk4


@njit(parallel=True)
def classify(P1s, P2s, steps, h, dth, A, B, C, U1, U2):
    """Per strike: twin gap (mean state distance of a twin started dth away in th1, capped at 1), how far the upper rod
    wanders (max |th1|, rad), and the net turns of the elbow D = th2 - th1. Over steps*h seconds."""
    n = P1s.size
    gap = np.empty(n); th1max = np.empty(n); dturns = np.empty(n)
    for k in prange(n):
        q1 = 0.0; q2 = 0.0; p1 = P1s[k]; p2 = P2s[k]
        r1 = dth; r2 = 0.0; s1 = P1s[k]; s2 = P2s[k]
        acc = 0.0; m = 0.0
        for i in range(steps):
            q1, q2, p1, p2 = rk4(q1, q2, p1, p2, h, A, B, C, U1, U2)
            r1, r2, s1, s2 = rk4(r1, r2, s1, s2, h, A, B, C, U1, U2)
            d = np.sqrt((q1 - r1) ** 2 + (q2 - r2) ** 2 + (p1 - s1) ** 2 + (p2 - s2) ** 2)
            acc += min(d, 1.0)
            m = max(m, abs(q1))
        gap[k] = acc / steps; th1max[k] = m; dturns[k] = (q2 - q1) / (2 * np.pi)
    return gap, th1max, dturns


def strike_map(n1, n2, p1lim, p2lim, seconds, h=2.5e-4):
    p1 = np.linspace(*p1lim, n1); p2 = np.linspace(*p2lim, n2)
    G1, G2 = np.meshgrid(p1, p2)
    gap, th1max, dturns = classify(G1.ravel(), G2.ravel(), int(seconds / h), h, 1e-6, *COEF)
    sh = (n2, n1)
    return p1, p2, gap.reshape(sh), th1max.reshape(sh), dturns.reshape(sh)


if __name__ == '__main__':
    main(sys.argv[1])
