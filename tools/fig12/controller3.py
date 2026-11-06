"""The active suspension of the one-wheel cart: offline reference for the page.

Plant: plant.py (states x = (q, qdot)), the one actuator u in the strut, disturbance w = the road height and its rate under
the wheel, plus the road's kick -N z_r' applied as a force (the product of the tyre load and the slope, not in the linear
matrices). Controller: discrete LQR on the zero-order-hold model over T_s of the suspension alone, in its own coordinates
    x = (d, w, a_n | xdot_c, zdot_b, zdot_w, adot_n): strut and tyre deflections, the x-modes, and the rates,
with two actuators, the strut's u_s and the drive motor's u_m, and the cost
    J = sum_i [ eta_rim^2 / s_eta^2 + w^2 / s_w^2 + zdot_b^2 / s_v^2 + u_s^2 / s_u^2 + u_m^2 / s_m^2 ].
In the linear part the strut cannot reach the stout at all (the tray stays level; the modes couple to x only): the strut
buys comfort (zdot_b) and road holding (w, hence a steady tyre load and a smaller kick), and only the motor, which pushes
along the road, can calm the slosh once the kick has hit. A skyhook damper on the strut (u_s = -c_sky zdot_b) with the plain
drive is the simple comparison.
Scenarios (speed bump at walking speed, cobbles, kerb, rough) run with RK4 at 1 ms, passive / skyhook / LQR, reporting the
peak wave height at the rim.
Run: python3 tools/fig12/controller3.py <slosh-modes.js> [V_mL]
"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plant, road
from scipy.linalg import expm, solve_discrete_are

G = plant.G_ACC

def load_modes(path):
    s = open(path).read(); return json.loads(s[s.index('{'):s.rindex('}') + 1])

def zoh(A, B, T):
    n, m = A.shape[0], B.shape[1]; F = expm(np.block([[A, B], [np.zeros((m, n + m))]]) * T)
    return F[:n, :n], F[:n, n:]

def dlqr_iter(Ad, Bd, Q, R, iters=6000, tol=1e-12):
    """Discrete Riccati equation by iteration (what the page does), checked against scipy's solver."""
    P = Q.copy()
    for _ in range(iters):
        S_ = R + Bd.T @ P @ Bd; K = np.linalg.solve(S_, Bd.T @ P @ Ad)
        Pn = Q + Ad.T @ P @ (Ad - Bd @ K)
        if np.abs(Pn - P).max() < tol * max(1.0, np.abs(Pn).max()): P = Pn; break
        P = Pn
    S_ = R + Bd.T @ P @ Bd; K = np.linalg.solve(S_, Bd.T @ P @ Ad); return K, P

def design(P, fill, modes, rho, Ts=0.01, s_eta=0.0005, s_w=0.001, s_v=0.05, s_u=20.0, s_m=20.0):
    """The page's design(): the cart in the suspension's own coordinates (Hrovat 1997) with the stout added,
    x = (d, w, a_n | xdot_c, zdot_b, zdot_w, adot_n): strut deflection z_b - z_w, tyre deflection w = z_w - z_r, the x-modes, and
    the rates; two actuators, u = (u_s in the strut, u_m the drive motor's extra force along the road). The road enters only as a
    disturbance (its rate under the wheel, and the kick). The cart's position along the road is not a state: the motor holds its
    speed, not a timetable. A and B by probing the linear map with unit vectors, as the page does.
    Cost eta_rim^2/s_eta^2 + w^2/s_w^2 + zdot_b^2/s_v^2 + u_s^2/s_u^2 + u_m^2/s_m^2, eta_rim = sum a_n psi_n(rim, 0)."""
    S = plant.assemble(P, fill, modes, rho); I = S['idx']; Mi = np.linalg.inv(S['M']); Km, Cm = S['K'], S['C']
    ax = list(I['a']); nx = len(ax); npos = 2 + nx; n = npos + 3 + nx; NQ = S['n']
    ix, iz, iw = I['x'], I['z'], I['w']
    def dyn(x, us, um):
        d, w = x[0], x[1]; vx, vb, vw = x[npos], x[npos + 1], x[npos + 2]; dd = vb - vw
        F = np.zeros(NQ)
        F[ix] = -(P['c_x'] + P['c_d']) * vx + um
        F[iz] = -P['k'] * d - P['c'] * dd + us
        F[iw] = P['k'] * d + P['c'] * dd - us - P['k_t'] * w - P['c_t'] * vw     # the tyre's rate term with the road rate dropped (unknown to the controller)
        for k, i in enumerate(ax): F[i] = -Km[i, i] * x[2 + k] - Cm[i, i] * x[npos + 3 + k]
        acc = Mi @ F; out = np.zeros(n)
        out[0], out[1] = dd, vw; out[2:2 + nx] = x[npos + 3:npos + 3 + nx]
        out[npos], out[npos + 1], out[npos + 2] = acc[ix], acc[iz], acc[iw]; out[npos + 3:] = acc[ax]; return out
    A = np.zeros((n, n)); B2 = np.zeros((n, 2)); e = np.zeros(n)
    for j in range(n): e[j] = 1; A[:, j] = dyn(e, 0, 0); e[j] = 0
    B2[:, 0] = dyn(e, 1, 0); B2[:, 1] = dyn(e, 0, 1)
    h = np.zeros(n)
    for k, md in enumerate(modes['x']): h[2 + k] = md['rim_front']
    Q = np.outer(h, h) / s_eta ** 2; Q[1, 1] += 1 / s_w ** 2; Q[npos + 1, npos + 1] += 1 / s_v ** 2
    R = np.diag([1 / s_u ** 2, 1 / s_m ** 2])
    Ad, Bd = zoh(A, B2, Ts)
    K, Pm = dlqr_iter(Ad, Bd, Q, R)
    Pr = solve_discrete_are(Ad, Bd, Q, R); Kr = np.linalg.solve(R + Bd.T @ Pr @ Bd, Bd.T @ Pr @ Ad)
    Af, Buf, Bwf = plant.state_space(S)
    hfull = np.zeros(2 * NQ)
    for k, md in enumerate(modes['x']): hfull[I['a'][k]] = md['rim_front']
    ev = np.linalg.eigvals(Ad - Bd @ K)
    return dict(S=S, A=Af, Bu=Buf, Bw=Bwf, Ad=Ad, Bd=Bd, K_sub=K, K_scipy=Kr, h=hfull, Ts=Ts, Q=Q, R=R, tau=-Ts / np.log(np.abs(ev).max()), ax=ax, npos=npos, n=n,
                rho_N=([rho * m['N'] for m in modes['x']], [rho * m['N'] for m in modes['y']]))

def ctl_state(D, P, x, zr):
    """The controller's state from the plant state and the road under the wheel (the page's ctlState())."""
    S = D['S']; I = S['idx']; n = S['n']; npos = D['npos']; xs = np.zeros(D['n'])
    xs[0] = x[I['z']] - x[I['w']]; xs[1] = x[I['w']] - zr
    xs[npos], xs[npos + 1], xs[npos + 2] = x[n + I['x']], x[n + I['z']], x[n + I['w']]
    for k, i in enumerate(D['ax']): xs[2 + k] = x[i]; xs[npos + 3 + k] = x[n + i]
    return xs

def simulate(D, P, scenario, v=1.5, T=8.0, dt=1e-3, law='lqr', c_sky=300.0, Fmax=None, push=None, h_road=0.03, kick_on=True, pump_on=True):
    """RK4 at dt; the controller samples every Ts (ZOH). The wheel sees z_r(X) at X = v t + x_c, with the cart moving at speed v
    along x (x_c is the push coordinate about the uniform motion). Returns time series of the states, u, the rim wave, the road,
    the tyre load and the kick."""
    S, A, Bu, Bw = D['S'], D['A'], D['Bu'], D['Bw']; n = S['n']; I = S['idx']
    ax_ = road.Axle(road.PROFILES[scenario], h_road, R=P['R_w'])          # the axle's path over this road: the envelope under the wheel
    zr, slope = ax_, ax_.slope
    Fmax = Fmax or P['Bl'] * P['I_max']
    x = np.zeros(2 * n); t = 0.0; nT = int(round(T / dt)); hold = int(round(D['Ts'] / dt)); u = np.zeros(2)
    out = dict(t=[], x=[], u=[], eta=[], zr=[], za=[], azb=[], N=[], kick=[]); xdd_max = 0.0   # the cart's acceleration along the road, its largest at any step (the 10-ms samples would smooth the held forces)
    lag = {'az': 0.0}                                  # z_O'' from the previous evaluation, as the page lags it by one substep
    Mi = np.linalg.inv(S['M']); modes_N = np.zeros(n)
    for k, i in enumerate(I['a']): modes_N[i] = D['rho_N'][0][k]
    for k, i in enumerate(I['b']): modes_N[i] = D['rho_N'][1][k]
    def f(t, x, u):
        X = v * t + x[I['x']]; vv = v + x[n + I['x']]; z = zr(X); sl = slope(X); zd = vv * sl
        uu = np.zeros(4); uu[0] = u[0]; uu[1] = u[1]
        if push is not None and push[1] <= t < push[2]: uu[1 + push[0]] = push[3]
        Fk, N, Fw = plant.kick(P, S, x[:n], x[n:], z, zd, sl)
        if kick_on: uu[1] += Fk
        uu[3] = Fw
        dx = A @ x + Bu @ uu + Bw @ np.array([z, zd])
        if pump_on:
            azc = max(-0.8 * G, lag['az']); dx[n:] -= Mi @ (modes_N * azc * x[:n])   # the parametric term: rho N z_O'' a_n on every mode, clamped at -0.8 g
        return dx
    for k in range(nT):
        if k % hold == 0:
            if law == 'lqr': u = -D['K_sub'] @ ctl_state(D, P, x, zr(v * t + x[I['x']]))
            elif law == 'skyhook': u = np.array([-c_sky * x[n + I['z']], 0.0])
            else: u = np.zeros(2)
            u = np.clip(u, -Fmax, Fmax)
        k1 = f(t, x, u); k2 = f(t + dt / 2, x + dt / 2 * k1, u); k3 = f(t + dt / 2, x + dt / 2 * k2, u); k4 = f(t + dt, x + dt * k3, u)
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += dt
        lag['az'] = k1[n + I['z']]; xdd_max = max(xdd_max, abs(k1[n + I['x']]))
        if k % 10 == 0:
            X = v * t + x[I['x']]; z = zr(X); sl = slope(X); Fk, N, Fw = plant.kick(P, S, x[:n], x[n:], z, (v + x[n + I['x']]) * sl, sl)
            out['t'].append(t); out['x'].append(x.copy()); out['u'].append(u.copy()); out['eta'].append(float(D['h'] @ x))
            out['zr'].append(ax_.road(X)); out['za'].append(z); out['azb'].append(float(f(t, x, u)[n + I['z']])); out['N'].append(N); out['kick'].append(Fk)
    for k in out: out[k] = np.array(out[k])
    out['xdd_max'] = xdd_max
    return out

if __name__ == '__main__':
    data = load_modes(sys.argv[1]); V = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    fill = [f for f in data['fills'] if f['V_mL'] == V][0]
    rho, sigma, M_f, nu = 1007.0, 0.045, 0.15 * 1007.0 * 0.018, 2.06e-3 / 1007.0
    def gamma_fn(md):     # the page's damping sum for one mode, head included (wall + floor + surface skin + interior + contact line + foam)
        lam = md['lam']; kappa = M_f * lam / rho; w = np.sqrt((G * lam + sigma * lam ** 3 / rho) / (1 + kappa))
        sq = 0.5 * np.sqrt(nu * w / 2)                 # the page's setup(): Iw, Ib, Is are stored divided by E
        gw = sq * (md['Iw'] + md['Ib']); gs = sq * md['Is']
        gv = 2 * nu * lam ** 2; gc = 0.05; gf = 1.0 * (0.016 / fill['a']) * (1 - np.exp(-lam * 0.018))
        return gw + gs + gv + gc + gf
    modes = plant.modal_params(fill, rho, sigma, M_f, gamma_fn)
    for md, raw in zip(modes['x'], [m for m in fill['modes'] if m['m'] == 1 and m['o'] == 'c']):
        md['rim_front'] = sum(raw['psi'][k][0][-1] for k in raw['psi'])
    P = dict(plant.DEFAULT)
    D = design(P, fill, modes, rho)
    print(f"V = {V} mL: x-modes {[round(np.sqrt(m['w2'])/2/np.pi, 3) for m in modes['x']]} Hz, gamma {[round(m['gamma'], 3) for m in modes['x']]} 1/s")
    print(f"K (iteration) vs scipy: max rel diff {np.abs(D['K_sub'] - D['K_scipy']).max() / np.abs(D['K_scipy']).max():.1e}; K_s = {np.round(D['K_sub'][0], 2).tolist()}; K_m = {np.round(D['K_sub'][1], 2).tolist()}")
    print(f"closed loop: slowest time constant {D['tau']:.4f} s; static tyre load {D['S']['M_tot'] * G:.1f} N")
    for sc, h in (('bump', 0.03), ('cobbles', 0.006), ('kerb', 0.02), ('random', 0.013)):
        line = f'  {sc:8s}'
        for law in ('passive', 'skyhook', 'lqr'):
            o = simulate(D, P, sc, law=law, T=6.0, h_road=h)
            line += f" | {law}: rim {np.abs(o['eta']).max()*1e3:5.2f} mm, N {o['N'].min():.0f}..{o['N'].max():.0f} N, kick {np.abs(o['kick']).max():.1f} N, body {np.abs(o['azb']).max():.2f} m/s2, |u_s| {np.abs(o['u'][:, 0]).max():.0f} N, |u_m| {np.abs(o['u'][:, 1]).max():.0f} N"
        print(line)
