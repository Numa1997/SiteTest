"""The cart that carries the pint: a half-car (pitch-plane) model with the sloshing stout coupled in, built from a Lagrangian.

Coordinates (metres, radians, about the level rest state):
  x_c  position of the cart along the road (the reader pushes it; the stout pushes back),
  y_c  sideways position (a sideways push; the stout pushes back),
  z_b  heave of the body's centre of mass, up,
  psi  pitch of the body about y through its centre of mass: a point (x, z) of the body moves to (x + psi z, z - psi x),
       so positive psi puts the front (x > 0) down,
  z_f, z_r  heave of the front and rear wheels (unsprung masses),
  a_n  amplitude of sloshing mode n (the wave height at the rim where the mode is largest).
Struts at x = +l_f (front) and x = -l_r (rear): spring k, damper c, actuator force u (up on the body), tyre stiffness k_t
to the road heights z_rf(t), z_rr(t). The glass stands on the body at (d_g, h_g) from the centre of mass; its foot centre
O moves with  x_O = x_c + d_g + h_g psi,  z_O = z_b + h_g - d_g psi,  and turns with the body (tilt psi).

Liquid (from the note, section "The glass turns"): with the velocity potential
    Phi = xdot_O x + ydot_O y + zdot_O z + psidot chi_y + sum_n (adot_n / lam_n) Phi_n,
the kinetic energy is T = rho/2 int |grad Phi|^2 dV, which gives the mass matrix below (the Stokes-Joukowski inertia J_ry
for the rotation, the sloshing masses on the diagonal, the couplings rho Q N); the potential energy of the waves is
rho g/2 sum a_n^2 N_n (1 + sigma lam_n^2 / (rho g)), the tilt term - rho g psi sum_n a_n Q_xn N_n, and the rigid liquid's
weight at its centre of mass. The head adds its mass M_f per area to the surface: a_n's inertia is multiplied by (1 + kappa_n).
Damping: Rayleigh functions 1/2 c (strut rate)^2 for the struts and rho N_n/lam_n gamma_n adot_n^2 per mode.

The linear equations M qdd + C qd + K q = B u + E w, q = (x_c, y_c, z_b, psi, z_f, z_r, a_1..a_nx, b_1..b_ny),
u = (u_f, u_r, F_x, F_y, F_z) (two actuators, the reader's pushes), w = (z_rf, z_rr) road heights.
"""
import numpy as np

G_ACC = 9.81

DEFAULT = dict(
    M_b=25.0, J_b=2.0,            # body (tray, frame, glass) kg, kg m^2 about y through its centre of mass
    l_f=0.40, l_r=0.40,           # strut positions, m
    k=3000.0, c=120.0,            # each strut: N/m, N s/m  (heave 2.5 Hz, damping ratio about 0.22 with the stout)
    m_w=1.5, k_t=5.0e4, c_t=20.0, # each wheel: kg, tyre N/m, N s/m
    d_g=0.10, h_g=0.25,           # glass foot: ahead of the centre of mass, above it, m
    M_g=0.42,                     # the empty glass, kg (counted in M_b's rigid part separately)
    c_x=15.0, c_y=15.0,           # rolling and sideways resistance of the cart, N s/m
    Bl=20.0, I_max=5.0,           # each actuator: moving coil, N/A and A
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
    """Mass, damping and stiffness matrices and the input matrices, as numpy arrays."""
    mx, my = modes['x'], modes['y']; nx, ny = len(mx), len(my)
    n = 6 + nx + ny
    ix, iy, iz, ip, ifw, irw = range(6)
    ia = 6 + np.arange(nx); ib = 6 + nx + np.arange(ny)
    V = fill['V_liq']; m_l = rho * V; J_ry = rho * fill['J_ry']; J_rx = rho * fill['J_rx']
    zs = fill['zs']; zf = 0.008                                       # floor; the liquid's centre of mass above the foot, in the glass:
    # z_cm from the stored volume: approximate by the fill height's half plus the floor (the cavity widens upward; a few mm off; stated)
    z_cm_l = zf + 0.5 * (zs - zf) * 1.1
    M = np.zeros((n, n)); C = np.zeros((n, n)); K = np.zeros((n, n))
    # ---- rigid parts ----
    M_rig = P['M_b'] + 2 * P['m_w'] + P['M_g'] + m_l                 # everything moves along x and y together
    M[ix, ix] = M_rig; M[iy, iy] = M_rig
    C[ix, ix] = P['c_x']; C[iy, iy] = P['c_y']
    M_sprung = P['M_b'] + P['M_g'] + m_l
    M[iz, iz] = M_sprung
    # pitch inertia: body + glass as a point mass at (d_g, h_g + 0.08) + the liquid: Stokes-Joukowski about O plus the parallel axis
    # for the translation of O (x_O = ... + h_g psi, z_O = ... - d_g psi) handled through the coupling terms below
    hg_glass = P['h_g'] + 0.08
    J = P['J_b'] + P['M_g'] * (P['d_g'] ** 2 + hg_glass ** 2)
    M[ip, ip] = J
    # the liquid as the rigid translation of O plus the rotation about O: T = 1/2 m_l |v_O|^2 + 1/2 J_ry psidot^2 + m_l (v_O x omega) z_cm terms
    # v_O = (xdot_c + h_g psidot, zdot_b - d_g psidot); cross term from int grad(x xdot_O).grad(psidot chi) = xdot_O psidot V z_cm
    M[ix, ip] += m_l * P['h_g'] + m_l * z_cm_l; M[ip, ix] = M[ix, ip]
    M[iz, ip] += -m_l * P['d_g']; M[ip, iz] = M[iz, ip]
    M[ip, ip] += m_l * (P['h_g'] ** 2 + P['d_g'] ** 2) + J_ry + 2 * m_l * P['h_g'] * z_cm_l
    M[ifw, ifw] = P['m_w']; M[irw, irw] = P['m_w']
    # struts: deflection d_f = z_b - l_f psi - z_f, d_r = z_b + l_r psi - z_r
    for (l, s, iw) in ((P['l_f'], -1.0, ifw), (P['l_r'], +1.0, irw)):
        v = np.zeros(n); v[iz] = 1.0; v[ip] = s * l; v[iw] = -1.0
        K += P['k'] * np.outer(v, v); C += P['c'] * np.outer(v, v)
        K[iw, iw] += P['k_t']; C[iw, iw] += P['c_t']
    # gravity on the tilting sprung mass: a mass m at height h above the pitch axis has V = -m g h psi^2/2 (inverted pendulum)
    K[ip, ip] += -(P['M_g'] * hg_glass + m_l * (P['h_g'] + z_cm_l)) * g
    # ---- the stout ----
    for q, idx, mlist, dir_ in ((ix, ia, mx, 'x'), (iy, ib, my, 'y')):
        for k, md in enumerate(mlist):
            i = idx[k]; mu = rho * md['N'] / md['lam']                 # generalised mass of a_n (before the head)
            M[i, i] = mu * (1 + md['kappa'])
            C[i, i] = 2 * mu * (1 + md['kappa']) * md['gamma']     # gamma is the decay rate of the mode, head included
            K[i, i] = mu * md['w2'] * (1 + md['kappa'])               # rho g N (1 + sigma lam^2/(rho g))
            M[i, q] = M[q, i] = rho * md['Q'] * md['N']               # translation coupling
            if dir_ == 'x':
                M[i, ip] = M[ip, i] = rho * md['Q'] * md['N'] * P['h_g'] + rho * md['Qr'] * md['N']   # x_O carries h_g psi; rotation through chi_y
                K[i, ip] = K[ip, i] = -rho * g * md['Q'] * md['N']   # tilt: the liquid's weight along the tilted surface
    # inputs: u = (u_f, u_r, F_x, F_y, F_z), road w = (z_rf, z_rr)
    B = np.zeros((n, 5)); B[iz, 0] = 1; B[ip, 0] = -P['l_f']; B[ifw, 0] = -1
    B[iz, 1] = 1; B[ip, 1] = +P['l_r']; B[irw, 1] = -1
    B[ix, 2] = 1; B[iy, 3] = 1; B[iz, 4] = 1
    E = np.zeros((n, 2)); E[ifw, 0] = P['k_t']; E[irw, 1] = P['k_t']
    Ed = np.zeros((n, 2)); Ed[ifw, 0] = P['c_t']; Ed[irw, 1] = P['c_t']
    return dict(M=M, C=C, K=K, B=B, E=E, Ed=Ed, n=n, idx=dict(x=ix, y=iy, z=iz, psi=ip, zf=ifw, zr=irw, a=ia, b=ib), m_l=m_l, J_ry=J_ry, z_cm_l=z_cm_l)


def state_space(S):
    """xdot = A x + Bu u + Bw w, x = (q, qdot), w = (z_rf, z_rr, zdot_rf, zdot_rr)."""
    n = S['n']; Mi = np.linalg.inv(S['M'])
    A = np.zeros((2 * n, 2 * n)); A[:n, n:] = np.eye(n); A[n:, :n] = -Mi @ S['K']; A[n:, n:] = -Mi @ S['C']
    Bu = np.zeros((2 * n, S['B'].shape[1])); Bu[n:] = Mi @ S['B']
    Bw = np.zeros((2 * n, 4)); Bw[n:, :2] = Mi @ S['E']; Bw[n:, 2:] = Mi @ S['Ed']
    return A, Bu, Bw


def glass_kinematics(P, S, x, xdd):
    """Acceleration of the glass foot and the tilt from a state and its derivative: (xdd_O, ydd_O, zdd_O, psi, psidd)."""
    n = S['n']; I = S['idx']
    return (xdd[I['x']] + P['h_g'] * xdd[I['psi']], xdd[I['y']], xdd[I['z']] - P['d_g'] * xdd[I['psi']], x[I['psi']], xdd[I['psi']])
