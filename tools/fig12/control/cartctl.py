"""The cart, its drive, its sensors and every controller of Fig. 12, in JAX (float64), for Kaggle's GPU.

A line-by-line port of Cart.forces / Cart.step / Cart.sample / Observer.update and World.advance of
public/scripts/stout-cart.js, so that the controller can run inside the time loop of any fluid model: here the linear
three-mode stout (ModalFluid, Stage B1); later the 3D JAX solver (Stage B2), which only replaces `fluid_step`.

State: one flat dict of jnp scalars and small arrays (a pytree), advanced by `lax.scan` over fluid steps; inside each fluid
step `lax.fori_loop` over cart steps of h_c = 0.1 ms; the controller samples every T_s = 1 ms (counted exactly as the JS
does, with t_sample += h_c and the test t_sample >= T_s - 1e-12). Every operation is differentiable (clips are jnp.clip,
the sample is lax.cond), so jax.grad can tune weights through a whole ride.

Controllers (ctrl codes): 0 off, 1 speed (PI with anti-windup), 2 preview (PI + road feed-forward one current lag ahead),
3 slosh (LQR with integral on the Kalman estimate), 4 joint (slosh LQR + heave cancellation + suspension LQR).
Skyhook (susp = 1) adds to 0-3, as in the JS. Units SI throughout.
"""
import jax
import jax.numpy as jnp
import numpy as np
from jax import lax
from jax.scipy.linalg import expm

jax.config.update("jax_enable_x64", True)

OFF, SPEED, PREVIEW, SLOSH, JOINT = 0, 1, 2, 3, 4


# ------------------------------------------------------------------------------------------------------------- road
def road_table(bumps, Rw, xmin, xmax, h):
    """Road.build: the axle height z_a(x) of a rigid wheel of radius Rw over cosine bumps, every h (numpy, once)."""
    n = int(round((xmax - xmin) / h)) + 1
    x = xmin + h * np.arange(n)
    zr = np.zeros(n)
    for b in bumps:
        s = (x - b["x"]) / b["L"]
        m = (s > -0.5) & (s < 0.5)
        zr[m] += 0.5 * b["h"] * (1 + np.cos(2 * np.pi * s[m]))
    m = int(np.ceil(Rw / h))
    za = np.full(n, -1e9)
    for d in range(-m, m + 1):
        s = d * h
        if abs(s) > Rw:
            continue
        sh = np.full(n, -1e9)
        if d >= 0:
            sh[: n - d] = zr[d:]
        else:
            sh[-d:] = zr[: n + d]
        za = np.maximum(za, sh + np.sqrt(Rw * Rw - s * s))
    return za


def axle(za, xmin, h, x):
    """Road.axle: [z_a, dz_a/dx] by linear interpolation of the table."""
    f = (x - xmin) / h
    i = jnp.clip(jnp.floor(f), 0, za.shape[0] - 2).astype(jnp.int32)
    t = f - i
    a, b = za[i], za[i + 1]
    return a + t * (b - a), (b - a) / h


# ------------------------------------------------------------------------------------------------------- parameters
def make_params(consts, ctrl, susp, K, Ks, plant, za, ml):
    """Everything constant over a ride, as a dict of jnp arrays (static ints kept as python ints)."""
    c, o = consts["cart"], consts["obs"]
    P = {k: jnp.float64(v) for k, v in c.items()}
    P["b"] = jnp.float64(c["Ngear"] * c["Km"] / c["Rw"])
    P["K"] = jnp.asarray(K, jnp.float64)
    P["Ks"] = jnp.asarray(Ks, jnp.float64)
    P["Ad"] = jnp.asarray(o["Ad"], jnp.float64)
    P["Bd"] = jnp.asarray(o["Bd"], jnp.float64)
    P["Qd"] = jnp.asarray(o["Qd"], jnp.float64)
    P["sigV"], P["sigQ"] = jnp.float64(o["sigV"]), jnp.float64(o["sigQ"])
    P["pw"], P["pzeta"], P["pbeta"] = jnp.float64(plant["w"]), jnp.float64(plant["zeta"]), jnp.float64(plant["beta"])
    P["za"] = jnp.asarray(za, jnp.float64)
    r = consts["road"]
    P["road_xmin"], P["road_h"] = jnp.float64(r["xmin"]), jnp.float64(r["h"])
    P["ctrl"], P["susp"] = ctrl, susp
    P["obs_Mx"] = massX(P, ml)          # the filter is designed once, at the start, with the full glass
    return P


def massX(P, ml):
    return P["Mb"] + ml + P["mw"] + (P["Iw"] + P["Ngear"] ** 2 * P["Jm"]) / P["Rw"] ** 2


# ------------------------------------------------------------------------------------------------------------- cart
def forces(P, S, Fx, Fz):
    """Cart.forces: every force at the present state, with the stout's reaction (Fx, Fz)."""
    g, ml = P["g"], S["ml"]
    Ms = P["Mb"] + ml
    za, dza = axle(P["za"], P["road_xmin"], P["road_h"], S["x"])
    vza = dza * S["vx"]
    N = jnp.maximum(P["kt"] * (za - S["zw"]) + P["ct"] * (vza - S["vzw"]), 0.0)
    Fs = -P["k"] * (S["zb"] - S["zw"] - P["Ls"]) - P["c"] * (S["vzb"] - S["vzw"]) + S["us"]
    Mx = massX(P, ml)
    Fm0 = P["b"] * S["i"]
    Fgrip = P["mu"] * N
    Fmotor = jnp.clip(Fm0, -Fgrip, Fgrip)
    Froad = -N * dza
    ax = (Froad + Fmotor - P["cx"] * S["vx"] + Fx) / Mx
    azb = (Fs - Ms * g + Fz) / Ms
    azw = (-Fs - P["mw"] * g + N) / P["mw"]
    emf = P["Km"] * P["Ngear"] * S["vx"] / P["Rw"]
    ilim = jnp.clip(S["icmd"], -P["Imax"], P["Imax"])
    ilim = jnp.clip(ilim, (-P["Vmax"] - emf) / P["Ra"], (P["Vmax"] - emf) / P["Ra"])
    return dict(S, ax=ax, azb=azb, azw=azw, ireach=ilim, N=N, Fs=Fs, za_now=za, dza_now=dza, Fmotor=Fmotor,
                slip=(Fmotor != Fm0).astype(jnp.float64), Vm=P["Ra"] * S["i"] + emf, emf=emf)


def observer_update(P, S, u, yv, yq, fresh, az):
    """Observer.update: predict with the current held over the sample, correct with the speed and (when fresh) the probes.
    az: the measured heave for the joint controller (A_d, B_d recomputed with w^2 (1 + az/g)); 0 elsewhere."""
    w, z, be, Mx, b, cx, Ts = P["pw"], P["pzeta"], P["pbeta"], P["obs_Mx"], P["b"], P["cx"], P["Ts"]

    def recompute(_):
        w2 = w * w * (1 + az / 9.81)
        A = jnp.array([[-cx / Mx, 0.0, 0.0], [0.0, 0.0, 1.0], [be * cx / Mx, -w2, -2 * z * w]])
        B = jnp.array([b / Mx, 0.0, -be * b / Mx])
        M4 = jnp.zeros((4, 4)).at[:3, :3].set(A * Ts).at[:3, 3].set(B * Ts)
        E4 = expm(M4)
        return E4[:3, :3], E4[:3, 3]

    Ad, Bd = lax.cond(az != 0.0, recompute, lambda _: (P["Ad"], P["Bd"]), None)
    x, Pm = S["zh"], S["Pk"]
    xp = Ad @ x + Bd * u
    Pp = Ad @ Pm @ Ad.T + P["Qd"]
    # joint update with H = rows (speed) or (speed, swing); written for both, the swing row switched by `fresh`
    Rv, Rq = P["sigV"] ** 2, P["sigQ"] ** 2

    def two(_):
        H = jnp.array([[1.0, 0, 0], [0, 1.0, 0]])
        Sm = H @ Pp @ H.T + jnp.diag(jnp.array([Rv, Rq]))
        L = Pp @ H.T @ jnp.linalg.inv(Sm)
        nu = jnp.array([yv, yq]) - H @ xp
        IKH = jnp.eye(3) - L @ H
        Pn = IKH @ Pp @ IKH.T + L @ jnp.diag(jnp.array([Rv, Rq])) @ L.T
        return xp + L @ nu, Pn, L, nu

    def one(_):
        H = jnp.array([[1.0, 0, 0]])
        Sm = H @ Pp @ H.T + Rv
        L = Pp @ H.T / Sm[0, 0]
        nu = jnp.array([yv - xp[0]])
        IKH = jnp.eye(3) - L @ H
        Pn = IKH @ Pp @ IKH.T + Rv * (L @ L.T)
        L2 = jnp.concatenate([L, jnp.zeros((3, 1))], axis=1)
        return xp + L[:, 0] * nu[0], Pn, L2, jnp.array([nu[0], 0.0])

    xn, Pn, L, nu = lax.cond(fresh, two, one, None)
    Pn = 0.5 * (Pn + Pn.T)
    return dict(S, zh=xn, Pk=Pn, L=L, nu=nu, zh_pri=xp)


def sample(P, S):
    """Cart.sample: the sensors, the observer, the motor current command and the suspension force command."""
    b, ctrl = P["b"], P["ctrl"]
    i0 = P["cx"] * P["v0"] / b
    e = P["v0"] - S["vx"]
    yv = S["vx"] + S["noise_v"]
    yq, fresh = S["probe_y"], S["probe_fresh"]
    S = dict(S, probe_fresh=jnp.bool_(False))
    az_meas = S["azb"]
    S = observer_update(P, S, S["uPrev"], yv, yq, fresh, az_meas if ctrl == JOINT else jnp.float64(0.0))
    S = dict(S, uPrev=S["i"], az_meas=az_meas)
    s = S["zh"]
    K = P["K"]
    if ctrl in (SPEED, PREVIEW):
        ic = i0 + P["Kp"] * e + P["Ki"] * S["xi"]
        if ctrl == PREVIEW:
            _, ahead = axle(P["za"], P["road_xmin"], P["road_h"], S["x"] + S["vx"] * P["tauI"])
            ic = ic + (P["Mb"] + S["ml"] + P["mw"]) * P["g"] * ahead / b
        ipar = jnp.float64(0.0)
    elif ctrl == SLOSH:
        ic = i0 - (K[0] * (s[0] - P["v0"]) + K[1] * s[1] + K[2] * s[2] + K[3] * S["xi"])
        ipar = jnp.float64(0.0)
    elif ctrl == JOINT:
        ipar = -massX(P, S["ml"]) * P["pw"] ** 2 * (az_meas / P["g"]) * s[1] / (P["pbeta"] * b)
        ic = i0 - (K[0] * (s[0] - P["v0"]) + K[1] * s[1] + K[2] * s[2] + K[3] * S["xi"]) + ipar
    else:
        ic, ipar = i0, jnp.float64(0.0)
    if ctrl in (SPEED, PREVIEW, SLOSH, JOINT):   # anti-windup: integrate only while the command is not saturated
        xi = jnp.where(jnp.abs(ic) < P["Imax"], S["xi"] + e * P["Ts"], S["xi"])
    else:
        xi = S["xi"]
    if ctrl == JOINT:
        Ms = P["Mb"] + S["ml"]
        s0 = P["Ls"] - Ms * P["g"] / P["k"]
        N0 = (Ms + P["mw"]) * P["g"]
        y = jnp.array([S["zb"] - S["zw"] - s0, S["vzb"], S["vzw"], (S["N"] - N0) / P["kt"]])
        u = jnp.clip(-(P["Ks"] @ y), -P["Umax"], P["Umax"])
    elif P["susp"]:
        u = jnp.clip(-P["csky"] * S["vzb"], -P["Umax"], P["Umax"])
    else:
        u = jnp.float64(0.0)
    return dict(S, icmd=ic, xi=xi, uscmd=u, ipar=ipar)


def cart_step(P, S, hc, Fx, Fz):
    """Cart.step: sample when due, symplectic Euler for the mechanics, exact first-order lags for current and force."""
    tS = S["tSample"] + hc
    due = tS >= P["Ts"] - 1e-12
    S = dict(S, tSample=jnp.where(due, tS - P["Ts"], tS))
    S = lax.cond(due, lambda S_: forces(P, sample(P, S_), Fx, Fz), lambda S_: S_, S)
    vx = S["vx"] + hc * S["ax"]
    vzb = S["vzb"] + hc * S["azb"]
    vzw = S["vzw"] + hc * S["azw"]
    ei, eu = jnp.exp(-hc / P["tauI"]), jnp.exp(-hc / P["tauU"])
    S = dict(S, vx=vx, vzb=vzb, vzw=vzw, x=S["x"] + hc * vx, zb=S["zb"] + hc * vzb, zw=S["zw"] + hc * vzw,
             i=S["ireach"] + (S["i"] - S["ireach"]) * ei, us=S["uscmd"] + (S["us"] - S["uscmd"]) * eu, t=S["t"] + hc)
    return forces(P, S, Fx, Fz)


def cart_reset(P, x0, ml):
    """Cart.reset + the World constructor's observer start: static deflections, the drag-balancing current, filter at rest."""
    g, Ms = P["g"], P["Mb"] + ml
    za, _ = axle(P["za"], P["road_xmin"], P["road_h"], x0)
    zw = za - (Ms + P["mw"]) * g / P["kt"]
    zb = zw + P["Ls"] - Ms * g / P["k"]
    i = P["cx"] * P["v0"] / P["b"]
    f0 = jnp.float64(0.0)
    S = dict(x=jnp.float64(x0), vx=P["v0"], zb=zb, zw=zw, vzb=f0, vzw=f0, t=f0, i=i, icmd=i, xi=f0, us=f0, uscmd=f0,
             tSample=f0, ml=jnp.float64(ml), uPrev=i, ipar=f0, az_meas=f0, noise_v=f0,
             zh=jnp.array([P["v0"], 0.0, 0.0]), Pk=jnp.diag(jnp.array([P["sigV"], P["sigQ"], P["sigQ"] * P["pw"]]) ** 2),
             zh_pri=jnp.array([P["v0"], 0.0, 0.0]), L=jnp.zeros((3, 2)), nu=jnp.zeros(2),
             probe_y=f0, probe_fresh=jnp.bool_(False))
    return forces(P, S, f0, f0)


# ------------------------------------------------------------------------------------------- the linear three-mode stout
def modal_init(F):
    return dict(q=jnp.zeros(3), qd=jnp.zeros(3))


def modal_step(F, Q, dt, ax, az):
    """ModalFluid.step without the pour (Stage B1 runs below the rim): symplectic Euler in substeps of at most 0.5 ms."""
    n = int(np.ceil(dt / 0.0005))       # as the JS: 10 substeps for 5 ms, 4 for 2 ms
    hs = dt / n
    gf = 1 + az / F["g"]
    w, z, be = F["w"], F["zeta"], F["beta"]

    def body(_, qs):
        q, qd = qs
        qd = qd + hs * (-w * w * gf * q - 2 * z * w * qd - be * ax)
        return q + hs * qd, qd

    q, qd = lax.fori_loop(0, n, body, (Q["q"], Q["qd"]))
    return dict(Q, q=q, qd=qd)


def modal_momentum(F, Q):
    return jnp.sum(F["Pc"] * Q["qd"])


def modal_probe(F, Q):
    """World.readProbes on ModalFluid: (eta(R_s, 0) - eta(-R_s, 0)) / 2 = q1 + q2 + q3 (J1(xi_n)/J1(xi_n) = 1 at the wall)."""
    return jnp.sum(Q["q"])


# --------------------------------------------------------------------------------------------------------- coupling
def ride(P, F, x0, T, dt=0.005, hcart=1e-4):
    """World.advance in equal fluid steps dt: n cart steps with the stout's push held, the glass's mean acceleration over
    the step drives the stout, the stout's momentum change goes back to the cart as an impulse. One row per fluid step."""
    nsteps = int(round(T / dt))
    ncart = max(1, int(round(dt / hcart)))
    hc = dt / ncart
    S0 = cart_reset(P, x0, F["ml"])
    Q0 = modal_init(F)

    def fluid_step(carry, _):
        S, Q, Pm, Fx = carry
        vx0, vz0 = S["vx"], S["vzb"]
        S = lax.fori_loop(0, ncart, lambda _, S_: cart_step(P, S_, hc, Fx, 0.0), S)
        ax, az = (S["vx"] - vx0) / dt, (S["vzb"] - vz0) / dt
        Q = modal_step(F, Q, dt, ax, az)
        Pn = modal_momentum(F, Q)
        J = -(Pn - Pm)
        Fx = J / dt
        S = forces(P, S, Fx, 0.0)
        S = dict(S, probe_y=modal_probe(F, Q), probe_fresh=jnp.bool_(True))
        row = jnp.stack([S["t"], S["x"], S["vx"], S["zb"], S["vzb"], S["zw"], S["vzw"], S["i"], S["icmd"], S["us"],
                         Q["q"][0], Q["q"][1], Q["q"][2], Q["qd"][0], Q["qd"][1], Q["qd"][2],
                         S["zh"][0], S["zh"][1], S["zh"][2], S["probe_y"], ax, az, 2 * jnp.sum(Q["q"])])
        return (S, Q, Pn, Fx), row

    (S, Q, _, _), rows = lax.scan(fluid_step, (S0, Q0, jnp.float64(0.0), jnp.float64(0.0)), None, length=nsteps)
    row0 = jnp.stack([S0["t"], S0["x"], S0["vx"], S0["zb"], S0["vzb"], S0["zw"], S0["vzw"], S0["i"], S0["icmd"], S0["us"],
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, S0["zh"][0], S0["zh"][1], S0["zh"][2], 0.0, 0.0, 0.0, 0.0])
    return jnp.concatenate([row0[None], rows], axis=0)
