"""Fig. 16: the four-wheel cart that carries the pint, and its control system, in JAX (float64), for Kaggle.

The machine (planar: both wheels of an axle meet the same road, as in Fig. 12, so the left and right halves move alike and are
lumped per axle). A deck, rigid, carries the glass clamped to its seat, the controller, the battery and the scanner; its centre of
mass moves along the road (x), up and down (z_c), and pitches (theta, nose-up positive). Two axles (front f, rear r), each two
wheels on swing arms hinged under the deck, so each axle moves up and down (z_f, z_r) relative to the deck. Per axle: a coil spring
over a damper (k, c), a voice-coil actuator in series with them (force u_f, u_r, each the two struts of that axle), bump stops at
+-s_max, and the tyres (k_t, c_t), which push but cannot pull. The rear wheels hold hub motors (current i, force n_m b i along the
road, limited by the current limit, the battery's voltage against back-EMF, and the tyres' grip mu N_r).

Equations of motion (Newton for the deck's centre and Euler for its pitch; derived in notes/fig16/model.md, section 4):
    M_x x''      = F_d - c_x x' + sum_i (-N_i z_a'(x_i)) + F_x^stout
    M_s z_c''    = F_sf + F_sr - M_s g + F_z^stout
    J theta''    = a_f F_sf - a_r F_sr + d (M_s x'' - F_x^stout) - h_s F_x^stout
    m_i z_i''    = -F_si + N_i - m_i g
    F_si = -k (s_i - L_0) - c s_i' + u_i + F_stop(s_i),  s_f = z_c + a_f sin(theta) - z_f,  s_r = z_c - a_r sin(theta) - z_r
    N_i  = max(0, k_t (z_a(x_i) - z_i) + c_t (z_a'(x_i) x' - z_i'))
M_s: the deck with everything on it, the stout and head included as a rigid load (their moving part pushes back through F^stout);
M_x adds the axles and the turning wheels. d: height of the deck's centre of mass above the arms' hinges (the horizontal forces of
the arms act there); h_s: height of the stout's centre above the deck's centre.

The glass, clamped to the deck, accelerates with the point S where the stout's first mode lives (height h_g above the deck's centre):
    a_S = (x'' - h_g theta'' cos(theta) - h_g theta'^2 sin(theta),  z_c'' - h_g theta'' sin(theta) + h_g theta'^2 cos(theta))
and the stout, computed in the glass's frame (axes e_x = (cos theta, sin theta), e_z = (-sin theta, cos theta)), feels the uniform
effective gravity g_eff = g - a_S resolved on those axes:
    g_x = -(g + a_Sz) sin(theta) - a_Sx cos(theta),   g_z = -(g + a_Sz) cos(theta) + a_Sx sin(theta)
This is what Fig. 12's solver takes each step (Stout.step(s, dt, gx, gz)); the fluid code is unchanged. Not included: the parts of the
rotating frame's forces that vary across the glass (theta'' r and theta'^2 r about S, Coriolis); at the pitch rates of these rides
they are a small fraction of g_eff (notes/fig16/model.md gives the bound).

The control system (sampled every T_s = 1 ms; design() below, from first principles):
  * the linear model of cart + deck + axles + the first sloshing mode (run 8's measured swing with the head: 2.915 Hz, zeta 0.425,
    beta_h 1.241, the plant run 10's controllers used), about steady cruising at v0;
  * optimal state feedback (LQR, discrete Riccati equation), inputs: drive force, front and rear actuator forces;
  * road preview: the scanner reads the road N_p = 250 samples (0.25 s) ahead; the optimal feed-forward of a known disturbance,
    u_ff = -sum_j K_j w(k + j), K_j = (R + B'PB)^-1 B' (A_cl')^j P E (Tomizuka's preview control);
  * the swing (q, q') estimated by a Kalman filter fed by the two level probes on the glass's wall (Fig. 12's probes, read once per
    fluid step) and the glass's acceleration from the IMU; the other states from the encoders, the IMU and the strut stroke sensors.
  * the force commands go to the drives: current i_cmd = F_d / (n_m b), clipped as the hardware clips them.
"""
import math
import numpy as np
import jax
import jax.numpy as jnp
from jax import lax

jax.config.update("jax_enable_x64", True)
F64 = jnp.float64
G0 = 9.81

# the machine (notes/fig16/model.md, section 4: where each number comes from)
CART4 = dict(
    Md=2.40,            # kg, deck + battery + controller + scanner + struts' upper halves + glass (0.40 kg); the stout and head add m_l
    J0=0.0215,          # kg m^2, the deck's pitch inertia without the pint (box 0.31 m x 0.08 m of 2.0 kg + glass at the axis)
    af=0.11, ar=0.11,   # m, the axles ahead of and behind the centre of mass (wheelbase 0.22 m)
    d=0.035,            # m, the deck's centre of mass above the arms' hinges
    hg=0.122,           # m, the stout's first-mode point above the deck's centre (seat 16 mm + glass foot 14 mm + 83 mm + 9 mm)
    hs=0.090,           # m, the stout's centre of mass above the deck's centre
    mf=0.60, mr=1.00,   # kg, each axle: two wheels, arms, uprights; the rear wheels hold the hub motors
    Rw=0.045,           # m, wheel radius
    Iw=0.0012,          # kg m^2, all four wheels with the motors' rotors, about their axles
    k=700.0, c=19.0,    # N/m, N s/m per axle (two struts): the deck bounces at 3.5 Hz, damping ratio 0.3
    smax=0.030, kstop=2.0e4,   # m, travel either side of the static stroke; N/m, the bump stops
    kt=16000.0, ct=8.0, # N/m, N s/m per axle (two tyres)
    cx=2.0, mu=0.8,     # N s/m, drag along the road; tyre grip
    nm=2, b=3.0, Imax=8.0, Vmax=24.0, Ra=0.6, tauI=0.002,   # hub motors: N/A each at the road, A, V, ohm, s
    Umax=50.0, tauU=0.003,     # N per axle (two voice coils of 25 N), s
    Ts=0.001, Np=250,   # s, controller sample; preview samples (0.25 s)
)
# the swing the controller is designed on: run 8's measured swing with the head (free_full_1.5, ring 13) and beta with the head's mass
PLANT_F0, PLANT_ZETA, PLANT_BETA = 2.9152394311359466, 0.4250231022393094, 1.2409479382789539
# Bryson weights (the largest acceptable value of each), the controller's tuning
WEIGHTS = dict(dv=0.05, xi=0.02, zc=0.010, vzc=0.20, th=0.08, om=1.5, zw=0.03, vzw=1.0, q=0.0005, qd=0.0005 * 2 * math.pi * PLANT_F0,
               stroke=0.020, Fd=40.0, u=40.0)


def statics(P, ml):
    """The cart standing on a flat road: masses, inertia, static loads and heights. Road level 0, axle at R_w + tyre squash."""
    Ms = P["Md"] + ml
    Mx = Ms + P["mf"] + P["mr"] + P["Iw"] / P["Rw"] ** 2
    J = P["J0"] + ml * P["hs"] ** 2
    Wf = Ms * G0 * P["ar"] / (P["af"] + P["ar"]); Wr = Ms * G0 * P["af"] / (P["af"] + P["ar"])     # the deck's weight on each axle
    Nf0, Nr0 = Wf + P["mf"] * G0, Wr + P["mr"] * G0
    zf0, zr0 = P["Rw"] - Nf0 / P["kt"], P["Rw"] - Nr0 / P["kt"]
    L0 = 0.120                                   # m, free stroke of the struts (corner above axle, unloaded)
    sf0, sr0 = L0 - Wf / P["k"], L0 - Wr / P["k"]
    zc0 = 0.5 * (zf0 + sf0 + zr0 + sr0)          # level deck: (z_f + s_f) = (z_r + s_r) to 0.1 mm with these loads; the mean is taken
    th0 = math.asin(((zf0 + sf0) - (zr0 + sr0)) / (P["af"] + P["ar"]))
    return dict(Ms=Ms, Mx=Mx, J=J, Wf=Wf, Wr=Wr, Nf0=Nf0, Nr0=Nr0, zf0=zf0, zr0=zr0, L0=L0, sf0=sf0, sr0=sr0, zc0=zc0, th0=th0)


def linear_model(P, S, v0):
    """x = (dv, xi, zc, vzc, th, om, zf, vzf, zr, vzr, q, qd) about cruise; u = (F_d, u_f, u_r); w = (z_af, z_af', z_ar, z_ar')
    (the axle-path height and its slope along the road, under each axle). Returns A, B, E (continuous)."""
    k, c, kt, ct, af, ar = P["k"], P["c"], P["kt"], P["ct"], P["af"], P["ar"]
    Ms, Mx, J, d, hg = S["Ms"], S["Mx"], S["J"], P["d"], P["hg"]
    w, z, be = 2 * math.pi * PLANT_F0, PLANT_ZETA, PLANT_BETA
    n, m, nw = 12, 3, 4
    # forces as linear maps of (x, u, w): rows give coefficients
    def vec(**kw):
        a = np.zeros(n + m + nw); idx = dict(dv=0, xi=1, zc=2, vzc=3, th=4, om=5, zf=6, vzf=7, zr=8, vzr=9, q=10, qd=11, Fd=12, uf=13, ur=14,
                                             zaf=15, saf=16, zar=17, sar=18)
        for key, val in kw.items(): a[idx[key]] += val
        return a
    Fsf = vec(zc=-k, th=-k * af, zf=k, vzc=-c, om=-c * af, vzf=c, uf=1.0)
    Fsr = vec(zc=-k, th=k * ar, zr=k, vzc=-c, om=c * ar, vzr=c, ur=1.0)
    Nf = vec(zaf=kt, zf=-kt, saf=ct * v0, vzf=-ct)
    Nr = vec(zar=kt, zr=-kt, sar=ct * v0, vzr=-ct)
    ax = (vec(Fd=1.0, dv=-P["cx"]) - S["Nf0"] * vec(saf=1.0) - S["Nr0"] * vec(sar=1.0)) / Mx
    az = (Fsf + Fsr) / Ms
    al = (af * Fsf - ar * Fsr + d * Ms * ax) / J
    azf = (-Fsf + Nf) / P["mf"]; azr = (-Fsr + Nr) / P["mr"]
    aeff = ax + G0 * vec(th=1.0) - hg * al            # the glass's sideways acceleration at S, gravity's share included (linear)
    qdd = vec(q=-w * w, qd=-2 * z * w) - be * aeff
    rows = [ax, vec(dv=1.0), vec(vzc=1.0), az, vec(om=1.0), al, vec(vzf=1.0), azf, vec(vzr=1.0), azr, vec(qd=1.0), qdd]
    M = np.array(rows)
    return M[:, :n], M[:, n:n + m], M[:, n + m:]


def c2d(A, B, E, Ts):
    from scipy.linalg import expm
    n = A.shape[0]; m = B.shape[1] + E.shape[1]
    Mx = np.zeros((n + m, n + m)); Mx[:n, :n] = A * Ts; Mx[:n, n:] = np.hstack([B, E]) * Ts
    Ed = expm(Mx)
    return Ed[:n, :n], Ed[:n, n:n + B.shape[1]], Ed[:n, n + B.shape[1]:]


def design(P, ml, v0, weights=None):
    """The controller: LQR gain K (3 x 12), preview gains Kp (Np x 3 x 4), and the Kalman gain of the swing's estimator."""
    from scipy.linalg import solve_discrete_are
    W = dict(WEIGHTS, **(weights or {}))
    S = statics(P, ml); A, B, E = linear_model(P, S, v0); Ad, Bd, Ed = c2d(A, B, E, P["Ts"])
    n = A.shape[0]
    # state weights, with the struts' strokes as extra outputs
    Cs = np.zeros((2, n)); Cs[0, [2, 4, 6]] = [1, P["af"], -1]; Cs[1, [2, 4, 8]] = [1, -P["ar"], -1]
    keys = ["dv", "xi", "zc", "vzc", "th", "om", "zw", "vzw", "zw", "vzw", "q", "qd"]
    Q = np.diag([1 / W[k] ** 2 for k in keys]) + Cs.T @ Cs / W["stroke"] ** 2
    R = np.diag([1 / W["Fd"] ** 2, 1 / W["u"] ** 2, 1 / W["u"] ** 2])
    Q = Q * P["Ts"]; R = R * P["Ts"]                   # the continuous cost, sampled
    X = solve_discrete_are(Ad, Bd, Q, R)
    G = np.linalg.solve(R + Bd.T @ X @ Bd, Bd.T)       # (R + B'PB)^-1 B'
    K = G @ X @ Ad
    Acl = Ad - Bd @ K
    Kp = np.zeros((P["Np"], 3, 4)); M = X @ Ed
    for j in range(P["Np"]):
        Kp[j] = G @ M; M = Acl.T @ M
    # the swing's Kalman filter on (q, q'), input a_eff from the IMU, measured q from the probes (each fluid step, about 2 ms)
    w, z, be = 2 * math.pi * PLANT_F0, PLANT_ZETA, PLANT_BETA
    As = np.array([[0, 1], [-w * w, -2 * z * w]]); Bs = np.array([[0], [-be]])
    Asd, Bsd, _ = c2d(As, Bs, np.zeros((2, 1)), P["Ts"])
    Wa, sq = 2.0, 0.0008                               # (m/s^2)^2 s of unmodelled push; m, probe noise (Fig. 12's sigma_q)
    Gd = Bsd / np.sqrt(P["Ts"])
    Pk = solve_discrete_are(Asd.T, np.array([[1.0], [0.0]]), Gd @ Gd.T * Wa * 2 + 1e-14 * np.eye(2), np.array([[sq * sq]]))
    Lk = (Pk @ np.array([[1.0], [0.0]]) / (Pk[0, 0] + sq * sq)).ravel()
    ev = np.linalg.eigvals(Acl)
    return dict(K=K, Kp=Kp, Ad=Ad, Bd=Bd, Ed=Ed, Asd=Asd, Bsd=Bsd.ravel(), Lk=Lk, S=S, A=A, B=B, E=E, Q=Q, R=R,
                poles=ev, slowest=float(np.max(np.abs(ev))), weights=W)


class Cart4:
    """The machine and its controller, stepped like Fig. 12's Cart: init(x0, ml) -> state dict; step(c, h, Fx, Fz) with the stout's
    push in the GLASS's frame (Fx, Fz along e_x, e_z); geff(c) -> (g_x, g_z) for the fluid; probes are handed in as c['py'], c['pfresh'].
    ctrl: 'off' (passive struts, the speed held by a PI loop on the drive, no preview: the same machine without its control system) or
    'full' (the control system above)."""

    def __init__(self, params, road, v0, ctrl="full", weights=None):
        self.P = dict(CART4, **(params or {})); self.v0 = float(v0); self.ctrl = ctrl; self.weights = weights
        self.xmin, self.h, za, self.zr = road
        self.za = jnp.asarray(za, F64); self.nza = len(za)

    def axle(self, x):
        f = (x - self.xmin) / self.h; j = jnp.clip(jnp.floor(f).astype(jnp.int32), 0, self.nza - 2); t = f - j
        A, B = self.za[j], self.za[j + 1]
        return A + t * (B - A), (B - A) / self.h

    def init(self, x0, ml):
        P = self.P; v0 = self.v0
        D = design(P, float(ml), v0, self.weights); self.D = D; S = D["S"]; self.S = S
        self.K = jnp.asarray(D["K"]); self.Kp = jnp.asarray(D["Kp"]); self.Asd = jnp.asarray(D["Asd"]); self.Bsd = jnp.asarray(D["Bsd"])
        self.Lk = jnp.asarray(D["Lk"]); self.jprev = jnp.arange(P["Np"], dtype=F64)
        # the speed loop of 'off': Fig. 12's PI, scaled to this cart's mass (crossover 8 Hz)
        wc = 2 * math.pi * 8.0; self.KpF = S["Mx"] * wc; self.KiF = self.KpF * wc / 4
        z = jnp.zeros((), F64)
        Fd0 = P["cx"] * v0
        c = dict(x=jnp.asarray(x0, F64), v=jnp.asarray(v0, F64), zc=jnp.asarray(S["zc0"], F64), vzc=z, th=jnp.asarray(S["th0"], F64), om=z,
                 zf=jnp.asarray(S["zf0"], F64), vzf=z, zr=jnp.asarray(S["zr0"], F64), vzr=z,
                 i=jnp.asarray(Fd0 / (P["nm"] * P["b"]), F64), icmd=jnp.asarray(Fd0 / (P["nm"] * P["b"]), F64), uf=z, ur=z, ufc=z, urc=z,
                 xi=z, tS=z, t=z, qh=jnp.zeros(2, F64), aeff=z, py=z, pfresh=z, Nf=z, Nr=z, Ff=z, Fr=z, ax=z, azc=z, al=z, gx=z, gz=jnp.asarray(-G0, F64),
                 Fdrive=z, sat=z, stopf=z, stopr=z)
        return self.forces(c, 0.0, 0.0)

    def forces(self, c, Fxg, Fzg):
        """Accelerations of every body for the present state (Fxg, Fzg: the stout's push in the glass's frame)."""
        P, S = self.P, self.S; af, ar = P["af"], P["ar"]
        st, ct_ = jnp.sin(c["th"]), jnp.cos(c["th"])
        Fx = Fxg * ct_ - Fzg * st; Fz = Fxg * st + Fzg * ct_          # the stout's push in the road's frame
        xf, xr = c["x"] + af * ct_, c["x"] - ar * ct_
        zaf, saf = self.axle(xf); zar, sar = self.axle(xr)
        Nf = jnp.maximum(P["kt"] * (zaf - c["zf"]) + P["ct"] * (saf * c["v"] - c["vzf"]), 0.0)
        Nr = jnp.maximum(P["kt"] * (zar - c["zr"]) + P["ct"] * (sar * c["v"] - c["vzr"]), 0.0)
        sf = c["zc"] + af * st - c["zf"]; sr = c["zc"] - ar * st - c["zr"]
        vsf = c["vzc"] + af * ct_ * c["om"] - c["vzf"]; vsr = c["vzc"] - ar * ct_ * c["om"] - c["vzr"]
        stop = lambda s, s0: -P["kstop"] * (jnp.maximum(s - s0 - P["smax"], 0.0) + jnp.minimum(s - s0 + P["smax"], 0.0))
        Stf, Str = stop(sf, S["sf0"]), stop(sr, S["sr0"])
        Fsf = -P["k"] * (sf - S["L0"]) - P["c"] * vsf + c["uf"] + Stf
        Fsr = -P["k"] * (sr - S["L0"]) - P["c"] * vsr + c["ur"] + Str
        Fm = jnp.clip(P["nm"] * P["b"] * c["i"], -P["mu"] * Nr, P["mu"] * Nr)
        ax = (Fm - P["cx"] * c["v"] - Nf * saf - Nr * sar + Fx) / S["Mx"]
        azc = (Fsf + Fsr - S["Ms"] * G0 + Fz) / S["Ms"]
        al = (af * ct_ * Fsf - ar * ct_ * Fsr + P["d"] * (S["Ms"] * ax - Fx) - P["hs"] * Fx) / S["J"]
        azf = (-Fsf + Nf - P["mf"] * G0) / P["mf"]; azr = (-Fsr + Nr - P["mr"] * G0) / P["mr"]
        hg = P["hg"]
        aSx = ax - hg * al * ct_ - hg * c["om"] ** 2 * st; aSz = azc - hg * al * st + hg * c["om"] ** 2 * ct_
        gx = -(G0 + aSz) * st - aSx * ct_; gz = -(G0 + aSz) * ct_ + aSx * st
        aeff = aSx * ct_ + (G0 + aSz) * st                          # = -g_x: the glass's sideways acceleration felt by the stout
        return dict(c, ax=ax, azc=azc, al=al, azf=azf, azr=azr, Nf=Nf, Nr=Nr, Ff=Fsf, Fr=Fsr, gx=gx, gz=gz, aeff=aeff, Fdrive=Fm,
                    stopf=jnp.abs(Stf), stopr=jnp.abs(Str), zaf=zaf, zar=zar)

    def sample(self, c):
        P, S, v0 = self.P, self.S, self.v0; Ts = P["Ts"]; b = P["nm"] * P["b"]
        # the swing's estimate: predict with the IMU's a_eff over the sample, correct with the probes when they are fresh
        qh = self.Asd @ c["qh"] + self.Bsd * c["aeff"]
        qh = jnp.where(c["pfresh"] > 0, qh + self.Lk * (c["py"] - qh[0]), qh)
        if self.ctrl == "off":
            e = v0 - c["v"]; Fc = P["cx"] * v0 + self.KpF * e + self.KiF * c["xi"]
            ic = Fc / b; xi = jnp.where(jnp.abs(ic) < P["Imax"], c["xi"] + e * Ts, c["xi"])
            return dict(c, qh=qh, icmd=ic, xi=xi, ufc=jnp.zeros((), F64), urc=jnp.zeros((), F64), pfresh=jnp.zeros((), F64))
        X = jnp.stack([c["v"] - v0, c["xi"], c["zc"] - S["zc0"], c["vzc"], c["th"] - S["th0"], c["om"], c["zf"] - S["zf0"], c["vzf"],
                       c["zr"] - S["zr0"], c["vzr"], qh[0], qh[1]])
        # the road ahead, read by the scanner: under the front and rear axles, every T_s at the present speed
        ct_ = jnp.cos(c["th"]); ds = jnp.maximum(c["v"], 0.05) * Ts * self.jprev
        zf_, sf_ = self.axle(c["x"] + P["af"] * ct_ + ds); zr_, sr_ = self.axle(c["x"] - P["ar"] * ct_ + ds)
        Wp = jnp.stack([zf_ - P["Rw"], sf_, zr_ - P["Rw"], sr_], 1)
        U = -self.K @ X - jnp.einsum("jab,jb->a", self.Kp, Wp)
        Fc = P["cx"] * v0 + U[0]; ic = Fc / b
        xi = c["xi"] + (c["v"] - v0) * Ts
        return dict(c, qh=qh, icmd=ic, xi=xi, ufc=U[1], urc=U[2], pfresh=jnp.zeros((), F64))

    def step(self, c, hh, Fxg, Fzg):
        P = self.P; tS = c["tS"] + hh; due = tS >= P["Ts"] - 1e-12
        c = lax.cond(due, lambda cc: self.sample(dict(cc, tS=tS - P["Ts"])), lambda cc: dict(cc, tS=tS), c)
        b = P["nm"] * P["b"]; E = P["b"] * c["v"]                     # back-EMF per motor (V), the same speed for both
        il = jnp.clip(jnp.clip(c["icmd"], -P["Imax"], P["Imax"]), (-P["Vmax"] - E) / P["Ra"], (P["Vmax"] - E) / P["Ra"])
        sat = (jnp.abs(c["icmd"] - il) > 1e-9).astype(F64)
        uf_ = jnp.clip(c["ufc"], -P["Umax"], P["Umax"]); ur_ = jnp.clip(c["urc"], -P["Umax"], P["Umax"])
        v = c["v"] + hh * c["ax"]; vzc = c["vzc"] + hh * c["azc"]; om = c["om"] + hh * c["al"]
        vzf = c["vzf"] + hh * c["azf"]; vzr = c["vzr"] + hh * c["azr"]
        c = dict(c, v=v, vzc=vzc, om=om, vzf=vzf, vzr=vzr, x=c["x"] + hh * v, zc=c["zc"] + hh * vzc, th=c["th"] + hh * om,
                 zf=c["zf"] + hh * vzf, zr=c["zr"] + hh * vzr, t=c["t"] + hh,
                 i=il + (c["i"] - il) * jnp.exp(-hh / P["tauI"]), uf=uf_ + (c["uf"] - uf_) * jnp.exp(-hh / P["tauU"]),
                 ur=ur_ + (c["ur"] - ur_) * jnp.exp(-hh / P["tauU"]), sat=jnp.maximum(c["sat"], sat))
        return self.forces(c, Fxg, Fzg)
