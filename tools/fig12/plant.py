"""The cart that carries the pint: a quarter-car (one wheel) with the sloshing stout coupled in, built from a Lagrangian.

Coordinates (metres, about the level rest state, the cart travelling at its steady speed v along x):
  x_c  position of the cart along the road about that steady travel (the road's kick and the reader's push move it; the
       stout pushes back),
  z_b  heave of the body (tray, frame, glass and stout), up; the tray is guided and stays level, so the glass never tilts,
  z_w  heave of the wheel (the unsprung mass),
  a_n  amplitude of sloshing mode n (the wave height at the rim where the mode is largest).
One strut between body and wheel: spring k, damper c, actuator force u (up on the body, down on the wheel). The tyre is a
spring k_t with a little damping c_t between the wheel and the road height z_r(X) under it, X = v t + x_c. The glass stands
on the tray with its foot centre O at height h_g above the body's mass centre: x_O = x_c, z_O = z_b + h_g.

Where the slosh comes from (the note, section 10). The road pushes on the wheel along the normal to its surface. With the
tyre load N (the vertical tyre force, k_t zeta + c_t zeta', zeta = z_r - z_w) and the road slope z_r'(X), the horizontal
part of that push is -N z_r': uphill it brakes the cart, downhill it shoves it on. That sideways kick is what the stout
feels (a tilt of the effective gravity, the coupling rho Q_n N_n of the modal equation (12) with xdd_O = xdd_c), and the
body's vertical acceleration pumps the modes (the parametric term). The kick is a product of two things that change,
N and z_r', so it is not in the linear matrices: simulate() applies it as a force, and the design works with the linear
part, in which the slosh is not reachable from the strut at all. The controller holds the body still and the tyre load
steady; the pint is saved because the fluctuating part of N, (M_body) zdd_b + m_w zdd_w, loses its body share.

The drive holds the speed: a force -c_d xdot_c about the steady travel (a cruise control, or a hand), and rolling
resistance c_x. Liquid: potential Phi = xdot_O x + zdot_O z + sum_n (adot_n / lam_n) Phi_n gives T = rho/2 int |grad Phi|^2,
hence the couplings rho Q_n N_n between x_c and the x-modes and the modal masses (rho N_n / lam_n)(1 + kappa_n) with the
head; the waves' potential energy rho g/2 sum a_n^2 N_n (1 + sigma lam_n^2 / rho g). Rayleigh: 1/2 c d'^2 for the strut,
1/2 c_t zeta'^2 for the tyre, 1/2 (c_x + c_d) xdot_c^2, and (rho N_n / lam_n)(1 + kappa_n) gamma_n adot_n^2 per mode.

The linear equations M qdd + C qd + K q = B u + E w: q = (x_c, z_b, z_w, a_1..a_nx, b_1..b_ny), u = (u_s, F_x, F_z, F_w) (the
strut actuator, the reader's push along x and down on the body, and the lift-off correction on the wheel: when the linear tyre
would pull, N < 0, F_w = -N cancels it), w = (z_a, zdot_a) the axle's road height and its rate (road.Axle: the envelope of the
road under the wheel's circle, so that a sharp kerb is met by the rim, not by a point).
The y-type modes b_n are carried for the store; nothing in this plane drives them.
"""
import numpy as np

G_ACC = 9.81

DEFAULT = dict(
    M_b=10.0,                     # body: tray, frame, posts (the glass and the stout are added), kg
    k=3000.0, c=60.0,             # the strut: N/m, N s/m  (heave 2.6 Hz with the pint, damping ratio 0.17)
    m_w=1.5, k_t=5.0e4, c_t=20.0, # the wheel: kg, tyre N/m, N s/m
    h_g=0.25,                     # glass foot above the body's mass centre, m (the tray's height)
    M_g=0.42,                     # the empty glass, kg
    c_x=5.0, c_d=200.0,           # rolling resistance and the drive's speed holding, N s/m
    Bl=20.0, I_max=8.0,           # each actuator (strut and drive motor): moving coil, N/A and A
    R_w=0.08,                     # the wheel's radius, m (its rim rolls on the road; the axle follows the envelope)
)


def modal_params(fill, rho, sigma, M_f, gamma_fn, g=G_ACC):
    """From one fill of SLOSH_MODES (format 3): lists of x-type (o = 'c', m = 1) and y-type (o = 's', m = 1) modes with
    lam, N, Qx|Qy, Qry, kappa, omega^2, gamma. gamma_fn(mode) -> damping rate (1/s)."""
    out = {'x': [], 'y': []}
    for md in fill['modes']:
        if md['m'] != 1: continue
        kappa = M_f * md['lam'] / rho
        w2 = (g * md['lam'] + sigma * md['lam'] ** 3 / rho) / (1 + kappa)
        rec = dict(lam=md['lam'], N=md['N'], Q=md['Qx'] if md['o'] == 'c' else md['Qy'], Qr=md['Qry'] if md['o'] == 'c' else md['Qrx'],
                   kappa=kappa, w2=w2, gamma=gamma_fn(md), n=md['n'])
        out['x' if md['o'] == 'c' else 'y'].append(rec)
    return out


def assemble(P, fill, modes, rho, g=G_ACC):
    """Mass, damping and stiffness matrices and the input matrices, as numpy arrays (the linear part; the kick is in forces())."""
    mx, my = modes['x'], modes['y']; nx, ny = len(mx), len(my)
    n = 3 + nx + ny
    ix, iz, iw = range(3)
    ia = 3 + np.arange(nx); ib = 3 + nx + np.arange(ny)
    V = fill['V_liq']; m_l = rho * V
    M = np.zeros((n, n)); C = np.zeros((n, n)); K = np.zeros((n, n))
    # ---- rigid parts ----
    M_s = P['M_b'] + P['M_g'] + m_l                                  # the sprung mass: body, glass, stout
    M_tot = M_s + P['m_w']                                           # everything moves along x together
    M[ix, ix] = M_tot; C[ix, ix] = P['c_x'] + P['c_d']
    M[iz, iz] = M_s; M[iw, iw] = P['m_w']
    # the strut: deflection d = z_b - z_w
    v = np.zeros(n); v[iz] = 1.0; v[iw] = -1.0
    K += P['k'] * np.outer(v, v); C += P['c'] * np.outer(v, v)
    # the tyre's linear part: zeta = z_r - z_w, force k_t zeta + c_t zeta' up on the wheel
    K[iw, iw] += P['k_t']; C[iw, iw] += P['c_t']
    # ---- the stout ----
    for q, idx, mlist in ((ix, ia, mx), (None, ib, my)):
        for k, md in enumerate(mlist):
            i = idx[k]; mu = rho * md['N'] / md['lam']                 # generalised mass of a_n (before the head)
            M[i, i] = mu * (1 + md['kappa'])
            C[i, i] = 2 * mu * (1 + md['kappa']) * md['gamma']     # gamma is the decay rate of the mode, head included
            K[i, i] = mu * md['w2'] * (1 + md['kappa'])               # rho g N (1 + sigma lam^2/(rho g))
            if q is not None: M[i, q] = M[q, i] = rho * md['Q'] * md['N']   # translation coupling, both ways
    # inputs: u = (actuator, F_x, F_z); road w = (z_r, zdot_r) through the tyre's linear part
    B = np.zeros((n, 4)); B[iz, 0] = 1; B[iw, 0] = -1; B[ix, 1] = 1; B[iz, 2] = 1; B[iw, 3] = 1   # the fourth input: an extra force on the wheel (the lift-off correction)
    E = np.zeros((n, 2)); E[iw, 0] = P['k_t']; E[iw, 1] = P['c_t']
    return dict(M=M, C=C, K=K, B=B, E=E, n=n, idx=dict(x=ix, z=iz, w=iw, a=ia, b=ib), m_l=m_l, M_s=M_s, M_tot=M_tot)


def tyre_load(P, S, q, qd, zr, zrd, static=False):
    """The vertical tyre force N (its fluctuating part about the static load; with static=True the whole load)."""
    I = S['idx']; N = P['k_t'] * (zr - q[I['w']]) + P['c_t'] * (zrd - qd[I['w']])
    return N + (S['M_tot'] * G_ACC if static else 0.0)


def kick(P, S, q, qd, zr, zrd, slope):
    """The road's horizontal push on the wheel, -N z_a'(X), with the full tyre load N (static plus fluctuating), and the lift-off
    correction: a tyre that would pull (N < 0) has left the road and pushes nothing, so F_w = -N is added on the wheel.
    Returns (kick, N clamped, F_w)."""
    N = tyre_load(P, S, q, qd, zr, zrd, static=True)
    Fw = -N if N < 0 else 0.0
    N = max(N, 0.0)
    return -N * slope, N, Fw


def state_space(S):
    """xdot = A x + Bu u + Bw w for the linear part, x = (q, qdot), w = (z_r, zdot_r)."""
    n = S['n']; Mi = np.linalg.inv(S['M'])
    A = np.zeros((2 * n, 2 * n)); A[:n, n:] = np.eye(n); A[n:, :n] = -Mi @ S['K']; A[n:, n:] = -Mi @ S['C']
    Bu = np.zeros((2 * n, S['B'].shape[1])); Bu[n:] = Mi @ S['B']
    Bw = np.zeros((2 * n, 2)); Bw[n:] = Mi @ S['E']
    return A, Bu, Bw
