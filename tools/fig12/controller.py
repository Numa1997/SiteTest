"""Fig. 12, the waiter: a carriage under the glass, driven by a moving-coil motor, and an LQR controller that carries the
pint to a target without letting the head over the rim. Offline design and gate; the page computes the same gains live.

Model, per horizontal axis (x shown; y is the same with the sin copies):
  carriage + glass + stout:  M x'' + rho*pi*sum_n Q_n N_n a_n'' = F          (linear momentum of carriage, glass and liquid)
  modes (m = 1, n = 1..3):    a_n'' + 2 g_n a_n' + w_n^2 a_n = -(lam_n Q_n/(1+mu_n)) x''
  motor:                      F = B l I, |I| <= I_max, I held for one sample T_s (zero-order hold)
State s = (x - r, x', a_1, a_1', a_2, a_2', a_3, a_3'); cost sum (q_x (x-r)^2 + q_v x'^2 + q_e eta_w^2 + rho_F F^2) per sample,
eta_w = a_1 + a_2 + a_3 the rise of the stout at the wall in the direction of motion.
Run: python3 tools/fig12/controller.py   -> prints the model, gains, closed-loop poles and a 15 cm carry, hand versus waiter."""
import json, math, numpy as np
from scipy.linalg import expm, solve_discrete_are
D_ = json.loads(open('public/scripts/slosh-modes.js').read().split('window.SLOSH_MODES = ', 1)[1].rstrip().rstrip(';'))
g = 9.81
P = dict(V=500, hf=0.018, rho=1007, sig=0.045, ef=0.15, mu6=2.06e-3, T=6, cs=1, gc=0.05, kf=1)
CAR = dict(Mc=0.60, mg=0.42, Bl=12.0, Imax=2.5, Ts=0.01)          # carriage kg, empty glass kg, motor N/A, current A, sample s
W = dict(qx=1.0 / 0.02 ** 2, qv=0.0, qe=1.0 / 0.001 ** 2, rF=1.0 / 2.0 ** 2)   # Bryson: 2 cm off the path, 1 mm at the wall, 2 N
WR = 3.0                                                                          # rad/s: speed of the planned path (critically damped)
def muW(T): return 2.414e-5 * 10 ** (247.8 / (T + 273.15 - 140))
def simpson(y, x):
    y, x = np.asarray(y), np.asarray(x); h = x[1] - x[0]; n = len(x) - 1; assert n % 2 == 0
    return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())
def modes(p):
    vs = D_['vols_mL']; i = max(0, min(len(vs) - 2, np.searchsorted(vs, p['V']) - 1)); w = (p['V'] - vs[i]) / (vs[i + 1] - vs[i])
    A, B = D_['fills'][i], D_['fills'][i + 1]; a = A['a'] + w * (B['a'] - A['a'])
    nu = p['mu6'] * muW(p['T']) / muW(6) / p['rho']; Mf = p['ef'] * p['rho'] * p['hf']; out = []
    for ma, mb in zip(A['modes'], B['modes']):
        if ma['m'] != 1: continue
        L = lambda k: ma[k] + w * (mb[k] - ma[k]); lam = L('lam'); Q = L('Q')
        f = np.array(ma['f']) + w * (np.array(mb['f']) - np.array(ma['f'])); r = np.linspace(0, a, len(f)); N = simpson(f * f * r, r)
        muf = Mf * lam / p['rho']; om = math.sqrt((g * lam + p['sig'] * lam ** 3 / p['rho']) / (1 + muf)); sq = 0.5 * math.sqrt(nu * om / 2)
        gam = sq * (L('Iw') + L('Ib')) + p['cs'] * sq * L('Is') + 2 * nu * lam ** 2 + p['gc'] + p['kf'] * (0.016 / a) * (1 - math.exp(-lam * p['hf']))
        out.append(dict(n=ma['n'], lam=lam, Q=Q, N=N, om=om, gam=gam, muf=muf, msl=p['rho'] * math.pi * lam * Q * Q * N / (1 + muf)))
    return out, a, p['rho'] * p['V'] * 1e-6
def model(p=P, car=CAR):
    md, a, ml = modes(p); M = car['Mc'] + car['mg'] + ml; Msl = sum(m['msl'] for m in md); Me = M - Msl
    n = 2 + 2 * len(md); A = np.zeros((n, n)); Bv = np.zeros(n)
    # x'' = (F + sum rho pi Q N (2 g a' + w^2 a)) / Me ; a_n'' = -2 g a_n' - w^2 a_n - c_n x''
    A[0, 1] = 1
    for k, m in enumerate(md):
        c = p['rho'] * math.pi * m['Q'] * m['N']; i = 2 + 2 * k
        A[1, i] += c * m['om'] ** 2 / Me; A[1, i + 1] += c * 2 * m['gam'] / Me
    Bv[1] = 1 / Me
    for k, m in enumerate(md):
        i = 2 + 2 * k; cn = m['lam'] * m['Q'] / (1 + m['muf'])
        A[i, i + 1] = 1; A[i + 1, i] = -m['om'] ** 2; A[i + 1, i + 1] = -2 * m['gam']
        A[i + 1, :] += -cn * A[1, :]; Bv[i + 1] += -cn * Bv[1]
    return A, Bv.reshape(-1, 1), md, dict(M=M, Msl=Msl, Me=Me, ml=ml, a=a)
def zoh(A, B, T):
    n = A.shape[0]; E = expm(np.block([[A, B], [np.zeros((1, n + 1))]]) * T); return E[:n, :n], E[:n, n:]
def lqr(A, B, car=CAR, w=W):
    Ad, Bd = zoh(A, B, car['Ts']); n = A.shape[0]
    C = np.zeros((3, n)); C[0, 0] = 1; C[1, 1] = 1; C[2, 2::2] = 1           # x - r, x', eta_w
    Q = C.T @ np.diag([w['qx'], w['qv'], w['qe']]) @ C; R = np.array([[w['rF']]])
    S = solve_discrete_are(Ad, Bd, Q, R); K = np.linalg.solve(R + Bd.T @ S @ Bd, Bd.T @ S @ Ad)
    return K, Ad, Bd
def carry(A, B, K, Ad, Bd, info, dist=0.15, T=4.0, mode='waiter', Om=22.0, car=CAR, Wr=WR):
    """The target jumps by dist at t = 0. waiter: a planned path r(t) (critically damped, rate Wr) with feedforward M r'' and the
    sampled LQR on the error from the path, current-limited; hand: the page's critically damped follower of rate Om, no feedback."""
    n = A.shape[0]; y = np.zeros(n); Fmax = car['Bl'] * car['Imax']; h = 1e-3; per = round(car['Ts'] / h)
    r = rv = 0.0; F = 0.0; eta = []; xs = []; Fs = []
    for k in range(int(T / h)):
        if mode == 'waiter':
            if k % per == 0:
                ra = Wr * Wr * (dist - r) - 2 * Wr * rv; e = y.copy(); e[0] -= r; e[1] -= rv
                F = float(np.clip(-(K @ e)[0] + info['M'] * ra, -Fmax, Fmax))
            ra = Wr * Wr * (dist - r) - 2 * Wr * rv; rv += ra * h; r += rv * h
            f = lambda z: A @ z + B[:, 0] * F
        else:
            def f(z):
                xdd = Om * Om * (dist - z[0]) - 2 * Om * z[1]; F_ = info['Me'] * (xdd - A[1, 2:] @ z[2:])
                return A @ z + B[:, 0] * F_
        k1 = f(y); k2 = f(y + h / 2 * k1); k3 = f(y + h / 2 * k2); k4 = f(y + h * k3); y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        eta.append(y[2::2].sum()); xs.append(y[0] - dist); Fs.append(F)
    eta = np.abs(np.array(eta)); xs = np.array(xs)
    settle = next((i * h for i in range(len(xs)) if np.all(np.abs(xs[i:]) < 0.002)), None)
    return eta.max(), settle, max(map(abs, Fs))
if __name__ == '__main__':
    A, B, md, info = model(); K, Ad, Bd = lqr(A, B)
    print(f"M = {info['M']:.3f} kg (stout {info['ml']:.3f} kg), sloshing mass sum m_n = {info['Msl']*1000:.1f} g, effective {info['Me']:.3f} kg")
    for m in md: print(f"  mode (1,{m['n']}): f {m['om']/2/math.pi:.3f} Hz, gamma {m['gam']:.3f}/s, N {m['N']:.4e} m^2, Q {m['Q']*1e3:.3f} mm, sloshing mass {m['msl']*1000:.1f} g")
    print('K =', np.array2string(K[0], precision=4))
    ev = np.linalg.eigvals(Ad - Bd @ K); print('closed-loop |z| max', np.abs(ev).max().round(5), ' slowest time constant', round(-CAR['Ts'] / np.log(np.abs(ev).max()), 3), 's')
    for d in (0.10, 0.20):
        ew, tw, Fw = carry(A, B, K, Ad, Bd, info, d)
        print(f"  carry {d*100:.0f} cm: waiter peak wave {ew*1000:.2f} mm, settles (2 mm) in {tw:.2f} s, largest force {Fw:.2f} N")
        for Om in (3, 22):
            eh, th, _ = carry(A, B, K, Ad, Bd, info, d, mode='hand', Om=Om, T=5); print(f"      hand Omega {Om}: peak {eh*1000:.2f} mm, settles {th:.2f} s")
