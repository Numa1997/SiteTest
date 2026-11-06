"""The active suspension that keeps the pint level: offline reference for the page.

Plant: plant.py (states x = (q, qdot), 2n), inputs u = (u_f, u_r) the two strut actuators, disturbance w = road heights and
their rates at the two wheels. Controller: discrete LQR on the zero-order-hold model over T_s, cost
    J = sum_k [ eta_rim^2 / s_eta^2 + zdd_b^2 / s_a^2 + psi^2 / s_psi^2 + (u_f^2 + u_r^2) / s_u^2 ],
eta_rim = the wave height at the front of the rim from the x-modes (sum a_n psi_n at the rim) plus the tilt's own
contribution (the surface stays horizontal while the rim tilts: psi * a), so the cost is on what spills.
A skyhook damper (u = -c_sky zdot_b, split to the struts) is the simple comparison.
Also: the scenarios (speed bump at walking speed, cobbles, kerb) run with RK4 at 1 ms, passive / skyhook / LQR,
reporting the peak wave height at the rim and the head's margin to the rim.
Run: python3 tools/fig12/controller3.py <slosh-modes.js> [V_mL]
"""
import sys, os, json, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plant, road
from scipy.linalg import expm, solve_discrete_are

def load_modes(path):
    s = open(path).read(); return json.loads(s[s.index('{'):s.rindex('}') + 1])

def zoh(A, B, T):
    n, m = A.shape[0], B.shape[1]; F = expm(np.block([[A, B], [np.zeros((m, n + m))]]) * T)
    return F[:n, :n], F[:n, n:]

def dlqr_iter(Ad, Bd, Q, R, iters=4000, tol=1e-12):
    """Discrete Riccati equation by iteration (what the page does), checked against scipy's solver."""
    P = Q.copy()
    for _ in range(iters):
        S_ = R + Bd.T @ P @ Bd; K = np.linalg.solve(S_, Bd.T @ P @ Ad)
        Pn = Q + Ad.T @ P @ (Ad - Bd @ K)
        if np.abs(Pn - P).max() < tol * max(1.0, np.abs(Pn).max()): P = Pn; break
        P = Pn
    S_ = R + Bd.T @ P @ Bd; K = np.linalg.solve(S_, Bd.T @ P @ Ad); return K, P

def design(P, fill, modes, rho, Ts=0.01, s_eta=0.001, s_psi=0.01, s_v=0.05, s_u=20.0):
    """The page's design(): the model in suspension coordinates (Hrovat 1997), x = (d_f, d_r, zeta_f, zeta_r, psi, a_n | xdot_c, zdot_b,
    psidot, zdot_f, zdot_r, adot_n): strut deflections, tyre deflections, tilt, the x-modes, and the rates; the road enters only as a
    disturbance through the tyre-deflection rates. A and B by probing the linear map with unit vectors, as the page does.
    Cost eta_rim^2/s_eta^2 + psi^2/s_psi^2 + zdot_b^2/s_v^2 + |u|^2/s_u^2, eta_rim = sum a_n psi_n(rim, 0)."""
    S = plant.assemble(P, fill, modes, rho); I = S['idx']; Mi = np.linalg.inv(S['M']); Km, Cm = S['K'], S['C']
    ax = list(I['a']); nx = len(ax); npos = 4 + nx; n = npos + 5 + nx; NQ = S['n']; Lw = P['l_f'] + P['l_r']
    ix, iz, ip, ifw, irw = I['x'], I['z'], I['psi'], I['zf'], I['zr']
    Kg = -(P['M_g'] * (P['h_g'] + 0.08) + S['m_l'] * (P['h_g'] + S['z_cm_l'])) * 9.81
    def dyn(x, uf, ur):
        df, dr, zf, zr = x[:4]; psi = (dr - df + zr - zf) / Lw; vx, vzb, vpsi, vzf, vzr = x[npos:npos + 5]
        ddf = vzb - P['l_f'] * vpsi - vzf; ddr = vzb + P['l_r'] * vpsi - vzr
        F = np.zeros(NQ)
        F[ix] = -P['c_x'] * vx
        F[iz] = -P['k'] * (df + dr) - P['c'] * (ddf + ddr) + uf + ur
        F[ip] = P['k'] * (P['l_f'] * df - P['l_r'] * dr) + P['c'] * (P['l_f'] * ddf - P['l_r'] * ddr) - Kg * psi - P['l_f'] * uf + P['l_r'] * ur
        F[ifw] = P['k'] * df + P['c'] * ddf - P['k_t'] * zf - P['c_t'] * vzf - uf
        F[irw] = P['k'] * dr + P['c'] * ddr - P['k_t'] * zr - P['c_t'] * vzr - ur
        for k, i in enumerate(ax):
            F[ip] -= Km[ip, i] * x[4 + k]; F[i] = -Km[i, i] * x[4 + k] - Cm[i, i] * x[npos + 5 + k] - Km[i, ip] * psi
        acc = Mi @ F; out = np.zeros(n)
        out[0], out[1], out[2], out[3] = ddf, ddr, vzf, vzr; out[4:4 + nx] = x[npos + 5:npos + 5 + nx]
        out[npos], out[npos + 1], out[npos + 2], out[npos + 3], out[npos + 4] = acc[ix], acc[iz], acc[ip], acc[ifw], acc[irw]
        out[npos + 5:] = acc[ax]; return out
    A = np.zeros((n, n)); B2 = np.zeros((n, 2)); e = np.zeros(n)
    for j in range(n): e[j] = 1; A[:, j] = dyn(e, 0, 0); e[j] = 0
    B2[:, 0] = dyn(e, 1, 0); B2[:, 1] = dyn(e, 0, 1)
    h = np.zeros(n)
    for k, md in enumerate(modes['x']): h[4 + k] = md['rim_front']
    rp = np.zeros(n); rp[:4] = [-1 / Lw, 1 / Lw, -1 / Lw, 1 / Lw]
    Q = np.outer(h, h) / s_eta ** 2 + np.outer(rp, rp) / s_psi ** 2; Q[npos + 1, npos + 1] += 1 / s_v ** 2; R = np.eye(2) / s_u ** 2
    Ad, Bd = zoh(A, B2, Ts)
    K, Pm = dlqr_iter(Ad, Bd, Q, R)
    Pr = solve_discrete_are(Ad, Bd, Q, R); Kr = np.linalg.solve(R + Bd.T @ Pr @ Bd, Bd.T @ Pr @ Ad)
    Af, Buf, Bwf = plant.state_space(S)
    hfull = np.zeros(2 * NQ)
    for k, md in enumerate(modes['x']): hfull[I['a'][k]] = md['rim_front']
    ev = np.linalg.eigvals(Ad - Bd @ K)
    return dict(S=S, A=Af, Bu=Buf, Bw=Bwf, Ad=Ad, Bd=Bd, K_sub=K, K_scipy=Kr, h=hfull, Ts=Ts, Q=Q, R=R, tau=-Ts / np.log(np.abs(ev).max()), ax=ax, npos=npos, n=n,
                rho_N=([rho * m['N'] for m in modes['x']], [rho * m['N'] for m in modes['y']]))

def ctl_state(D, P, x, zrf, zrr):
    """The controller's state from the plant state and the road under the wheels (the page's ctlState())."""
    S = D['S']; I = S['idx']; n = S['n']; npos = D['npos']; xs = np.zeros(D['n'])
    xs[0] = x[I['z']] - P['l_f'] * x[I['psi']] - x[I['zf']]; xs[1] = x[I['z']] + P['l_r'] * x[I['psi']] - x[I['zr']]
    xs[2] = x[I['zf']] - zrf; xs[3] = x[I['zr']] - zrr
    xs[npos], xs[npos + 1], xs[npos + 2], xs[npos + 3], xs[npos + 4] = x[n + I['x']], x[n + I['z']], x[n + I['psi']], x[n + I['zf']], x[n + I['zr']]
    for k, i in enumerate(D['ax']): xs[4 + k] = x[i]; xs[npos + 5 + k] = x[n + i]
    return xs

def simulate(D, P, scenario, v=1.5, T=8.0, dt=1e-3, law='lqr', c_sky=400.0, Fmax=None, push=None, h_road=0.03):
    """RK4 at dt; the controller samples every Ts (ZOH). Road: both wheels see z_r(x_wheel) with the cart moving at speed v along x
    (x_c is the push coordinate about the uniform motion). Returns time series of the states, u, the rim wave and the road."""
    S, A, Bu, Bw = D['S'], D['A'], D['Bu'], D['Bw']; n = S['n']; I = S['idx']
    prof = road.PROFILES[scenario]
    zr = lambda x: prof(np.array([x]), h=h_road)[0]              # h_road: the feature's height; for 'random' the highest point in the first 3 m (the page's slider default is 13 mm)
    Fmax = Fmax or P['Bl'] * P['I_max']
    x = np.zeros(2 * n); t = 0.0; nT = int(round(T / dt)); hold = int(round(D['Ts'] / dt)); u = np.zeros(2)
    out = dict(t=[], x=[], u=[], eta=[], zrf=[], zrr=[], azb=[])
    lag = {'az': 0.0}                                  # z_O'' from the previous evaluation, as the page lags it by one substep
    Mi = np.linalg.inv(S['M']); modes_N = np.zeros(n)
    for k, i in enumerate(I['a']): modes_N[i] = D['rho_N'][0][k]
    for k, i in enumerate(I['b']): modes_N[i] = D['rho_N'][1][k]
    def f(t, x, u):
        xf = v * t + P['l_f'] + x[I['x']]; xr = v * t - P['l_r'] + x[I['x']]
        vv = v + x[n + I['x']]; w = np.array([zr(xf), zr(xr), vv * (zr(xf + 1e-4) - zr(xf - 1e-4)) / 2e-4, vv * (zr(xr + 1e-4) - zr(xr - 1e-4)) / 2e-4])   # the wheels ride the road at the cart's speed, push included
        uu = np.zeros(5); uu[:2] = u
        if push is not None and push[1] <= t < push[2]: uu[2 + push[0]] = push[3]
        dx = A @ x + Bu @ uu + Bw @ w
        azc = max(-0.8 * 9.81, lag['az']); dx[n:] -= Mi @ (modes_N * azc * x[:n])   # the parametric term: rho N z_O'' a_n on every mode, clamped at -0.8 g
        return dx
    for k in range(nT):
        if k % hold == 0:
            if law == 'lqr': xf_ = v * t + P['l_f'] + x[I['x']]; xr_ = v * t - P['l_r'] + x[I['x']]; u = -D['K_sub'] @ ctl_state(D, P, x, zr(xf_), zr(xr_))
            elif law == 'skyhook': u = np.array([-c_sky * (x[n + I['z']] - P['l_f'] * x[n + I['psi']]), -c_sky * (x[n + I['z']] + P['l_r'] * x[n + I['psi']])])
            else: u = np.zeros(2)
            u = np.clip(u, -Fmax, Fmax)
        k1 = f(t, x, u); k2 = f(t + dt / 2, x + dt / 2 * k1, u); k3 = f(t + dt / 2, x + dt / 2 * k2, u); k4 = f(t + dt, x + dt * k3, u)
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += dt
        lag['az'] = k1[n + I['z']] - P['d_g'] * k1[n + I['psi']]
        if k % 10 == 0:
            out['t'].append(t); out['x'].append(x.copy()); out['u'].append(u.copy()); out['eta'].append(float(D['h'] @ x))
            out['zrf'].append(zr(v * t + P['l_f'])); out['zrr'].append(zr(v * t - P['l_r'])); out['azb'].append(float(f(t, x, u)[n + I['z']]))
    for k in out: out[k] = np.array(out[k])
    return out

if __name__ == '__main__':
    data = load_modes(sys.argv[1]); V = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    fill = [f for f in data['fills'] if f['V_mL'] == V][0]
    rho, sigma, M_f, nu = 1007.0, 0.045, 0.3, 2.0e-6
    g = 9.81
    def gamma_fn(md):     # the page's damping sum for one mode, head included (wall + floor + surface skin + interior + contact line + foam)
        lam = md['lam']; kappa = M_f * lam / rho; w = np.sqrt((g * lam + sigma * lam ** 3 / rho) / (1 + kappa))
        sq = 0.5 * np.sqrt(nu * w / 2)                 # the page's setup(): Iw, Ib, Is are stored divided by E
        gw = sq * (md['Iw'] + md['Ib']); gs = sq * md['Is']
        gv = 2 * nu * lam ** 2; gc = 0.05; gf = 1.0 * (0.016 / fill['a']) * (1 - np.exp(-lam * 0.018))
        return gw + gs + gv + gc + gf
    modes = plant.modal_params(fill, rho, sigma, M_f, gamma_fn)
    # rim value at the front (theta = 0) of each x-mode: sum over its cos components at s = 1
    for md, raw in zip(modes['x'], [m for m in fill['modes'] if m['m'] == 1 and m['o'] == 'c']):
        md['rim_front'] = sum(raw['psi'][k][0][-1] for k in raw['psi'])
    P = dict(plant.DEFAULT)
    P['I_max'] = 8.0
    D = design(P, fill, modes, rho)
    print(f"V = {V} mL: x-modes {[round(np.sqrt(m['w2'])/2/np.pi, 3) for m in modes['x']]} Hz, gamma {[round(m['gamma'], 3) for m in modes['x']]} 1/s")
    print(f"K (iteration) vs scipy: max rel diff {np.abs(D['K_sub'] - D['K_scipy']).max() / np.abs(D['K_scipy']).max():.1e}; K_f = {np.round(D['K_sub'][0], 3).tolist()}")
    print(f"closed loop: slowest time constant {D['tau']:.4f} s")
    rim_margin = (160e-3 + 0.005 - fill['zs'] - 0.018)      # head top to the dome limit, 18 mm head, 5 mm dome
    for sc in ('bump', 'cobbles', 'kerb'):
        line = f'  {sc:8s}'
        for law in ('passive', 'skyhook', 'lqr'):
            o = simulate(D, P, sc, law=law, T=6.0)
            line += f" | {law}: peak rim wave {np.abs(o['eta']).max()*1e3:5.1f} mm (margin {rim_margin*1e3:.1f} mm), peak body acc {np.abs(o['azb']).max():.2f} m/s2, max |u| {np.abs(o['u']).max():.0f} N"
        print(line)
