"""Fig. 16: the design simulator. A cart with (optionally) a gimballed holder, carrying the validated slosh model (slosh_model.py,
fit.json), on the CPU. Used to compare cart concepts; the final rides are computed in the full fluid solver.

The machine (planar, as Fig. 12's: one wheel, no pitch of the chassis):
  x, v        the cart along the road; z_w the axle, z_b the body on its suspension (quarter car: tyre k_t, c_t that cannot pull;
              suspension k, c and an optional active force u_s);
  phi         the holder's tilt about a pivot on the body, top forward positive (gimbal = 1), with the pivot's torque tau;
              the pendulum (glass + liquid + cradle): mass m_p, centre of mass L_c below the pivot, moment of inertia I_O about it.
Lagrange's equations for (x, z_b, phi), solved as a 3 x 3 system every sub-step (0.1 ms):
  M_x x''  - m_p L_c cos(phi) phi''            = F_road + F_motor - F_drag - m_p L_c sin(phi) phi'^2
  M_s z_b'' + m_p L_c sin(phi) phi''           = F_susp - M_s g - m_p L_c cos(phi) phi'^2
  I_O phi'' - m_p L_c cos(phi) x'' + m_p L_c sin(phi) z_b'' = tau - c_phi phi' - m_p g L_c sin(phi)
The stout in the glass's frame: mode n has its equivalent mass s_n below the pivot (s_n = s_surf + (2/k_n) tanh(k_n h/2), the
height of the mechanical analogue, e.g. Dodge 2000, ch. 3), and feels
  a_eff,n = x'' cos(phi) - (g + z_b'') sin(phi) - phi'' s_n        (the glass's sideways acceleration at that point)
  g_perp,n = (g + z_b'') cos(phi) + x'' sin(phi) + phi'^2 s_n      (the effective gravity along the glass's axis)
  q_n'' + D_n(q_n') + w_n^2 (g_perp,n / g) q_n = -beta_n a_eff,n
The motor: b = N_g K_m / R_w newtons per ampere; current lag tau_i towards the command clipped to +-I_max and to the supply's
(+-V_max - b v)/R_a; grip mu N. The road: stout_jax.road_table (the axle path of a rigid wheel of radius R_w).

Controllers (sampled at 1 kHz, full state known at this concept stage; the estimator comes with the chosen concept):
  drive   speed PI with anti-windup about a speed profile v_ref(x); + preview: the current that cancels the road's push,
          N z_a'(x + v tau_i)/b with N the tyre load (pv = 1: the static load, as Fig. 12; pv = 2: the measured load);
  gimbal  tau = (I_O/s_1 - m_p L_c) A - K_g . (phi, phi', q_1, q_1'), A = x'' cos(phi) - (g + z_b'') sin(phi), which is what an
          accelerometer on the holder at the pivot reads along the glass's x. The first term makes the holder a pendulum whose
          centre of oscillation is the first mode's point; K_g is an LQR on that tuned plant (gimbal_lqr);
  susp    skyhook, u_s = -c_sky z_b' (optional)."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jax, jax.numpy as jnp
from jax import lax
import slosh_model as SM, stout_jax as SJ

G = 9.81
F12 = dict(SJ.CART_COMMON)   # Fig. 12's cart

BASE = dict(
    # chassis and wheel
    Mb=1.5 - 0.0, mw=0.3, Rw=0.04, Iw=0.00024, k=600.0, c=8.0, kt=20000.0, ct=5.0, Ls=0.135, cx=2.0, mu=0.8,
    # motor
    Ngear=10.0, Km=0.02, Ra=2.0, Jm=2e-6, Vmax=12.0, Imax=3.0, tauI=0.002,
    # drive controller
    Kp=F12["Kp"], Ki=F12["Ki"], pv=0.0, xerr=0.0,
    # suspension actuator
    csky=0.0, Umax=40.0, tauU=0.005,
    # gimbal (off by default: the glass is fixed to the body and its mass is in Mb)
    gimbal=0.0, mp=0.0, Lc=0.0, IO=1.0, s_surf=0.0, cphi=0.0, tauMax=0.0, tauT=0.003, tune=1.0, phiMax=0.6, IOc=-1.0,
    Kg=(0.0, 0.0, 0.0, 0.0),
    # speed profile: v0 everywhere, lowered smoothly to vk between xk0 and xk1 (ramps of length Lramp)
    v0=1.0, vk=1.0, xk0=1e9, xk1=1e9, Lramp=0.3,
)


def mode_depth(md, h=SM.FILL):
    """Depth below the free surface of each mode's equivalent mass: (2/k_n) tanh(k_n h/2)."""
    return [2 * SM.R_S / m["xi"] * math.tanh(m["xi"] * h / (2 * SM.R_S)) for m in md]


def gimbal_lqr(P, mode, qlim=0.001, philim=0.15, ratelim=3.0):
    """LQR for the pivot's torque on y = (phi, phi', q1, q1'), on the plant with the tuning torque applied (the holder then swings
    as a pendulum of length s_1): phi'' = (d - g phi)/s_1 + tau/I_O, q1'' = -2 zeta w q1' - w^2 q1 + beta s_1 tau/I_O (d: the
    cart's acceleration). Bryson weights: q1 to qlim, phi to philim, phi' to ratelim, tau to tauMax."""
    import scipy.linalg as sl
    w, z, be = 2 * math.pi * mode["f"], mode["zeta_lin"], mode["beta"]; s1 = mode["s"]; IO = P["IO"]
    A = np.array([[0, 1, 0, 0], [-G / s1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -w * w, -2 * z * w]])
    B = np.array([[0.0], [1 / IO], [0.0], [be * s1 / IO]])
    Q = np.diag([1 / philim ** 2, 1 / ratelim ** 2, 1 / qlim ** 2, 1 / (qlim * w) ** 2]); R = np.array([[1 / P["tauMax"] ** 2]])
    X = sl.solve_continuous_are(A, B, Q, R)
    return tuple(float(v) for v in (B.T @ X / R[0, 0]).ravel())


def build(end, DT=0.002, model=None):
    """Compile one simulator for rides of `end` seconds. Returns run(params, road_table) -> arrays every DT."""
    m, md, w, be, ga, rg, damp = SM._setup(model or SM.fitted())
    dep = jnp.asarray(mode_depth(md)); nsub = int(round(DT / 1e-4)); hc = DT / nsub; n = int(round(end / DT)); N = m["N"]
    Ts = 1e-3; ksamp = int(round(Ts / hc))

    def run(P, xmin, hroad, za):
        nza = za.shape[0]
        def axle(x):
            f = (x - xmin) / hroad; j = jnp.clip(jnp.floor(f).astype(jnp.int32), 0, nza - 2); t = f - j
            return za[j] + t * (za[j + 1] - za[j]), (za[j + 1] - za[j]) / hroad
        b = P["Ngear"] * P["Km"] / P["Rw"]
        gim = P["gimbal"]
        Ms = P["Mb"] + P["mp"]                                   # on the suspension (liquid is in mp with a gimbal, in Mb without)
        Mx = Ms + P["mw"] + (P["Iw"] + P["Ngear"] ** 2 * P["Jm"]) / P["Rw"] ** 2
        mL = P["mp"] * P["Lc"] * gim
        s_n = P["s_surf"] + dep                                  # each mode's point below the pivot
        N0 = (Ms + P["mw"]) * G

        def vref(x):
            sm = lambda u: 0.5 - 0.5 * jnp.cos(jnp.pi * jnp.clip(u, 0.0, 1.0))
            dip = sm((x - (P["xk0"] - P["Lramp"])) / P["Lramp"]) * (1 - sm((x - P["xk1"]) / P["Lramp"]))
            return P["v0"] - (P["v0"] - P["vk"]) * dip

        def accel(s, F):
            """The 3 x 3 system; returns x'', z_b'', phi'', z_w'', N, road push, motor push."""
            a, d = axle(s["x"])
            Nw = jnp.maximum(P["kt"] * (a - s["zw"]) + P["ct"] * (d * s["v"] - s["vzw"]), 0.0)
            FS = -P["k"] * (s["zb"] - s["zw"] - P["Ls"]) - P["c"] * (s["vzb"] - s["vzw"]) + s["us"]
            Fm = jnp.clip(b * s["i"], -P["mu"] * Nw, P["mu"] * Nw); Fr = -Nw * d
            Fx = Fr + Fm - P["cx"] * s["v"] + F
            cp, sp = jnp.cos(s["phi"]), jnp.sin(s["phi"])
            r1 = Fx - mL * sp * s["om"] ** 2
            r2 = FS - Ms * G - mL * cp * s["om"] ** 2
            r3 = s["tau"] - P["cphi"] * s["om"] - mL * G * sp
            # eliminate phi'' (gimbal locked: phi'' = 0, the rows decouple)
            M = jnp.array([[Mx, 0.0, -mL * cp], [0.0, Ms, mL * sp], [-mL * cp, mL * sp, P["IO"]]])
            sol = jnp.linalg.solve(M, jnp.stack([r1, r2, r3]))
            ax, az, al = sol[0], sol[1], sol[2] * gim
            azw = (-FS - P["mw"] * G + Nw) / P["mw"]
            return ax, az, al, azw, Nw, Fr, Fm, d

        def control(s, ax, az, Nw):
            e = vref(s["x"]) - s["v"]
            i0 = P["cx"] * vref(s["x"]) / b
            ic = i0 + P["Kp"] * e + P["Ki"] * s["xi"]
            _, dpre = axle(s["x"] + s["v"] * P["tauI"] + P["xerr"])     # xerr: the preview's error in where the road is
            ic = ic + jnp.where(P["pv"] > 1.5, Nw, N0) * dpre / b * jnp.where(P["pv"] > 0.5, 1.0, 0.0)
            xi = jnp.where(jnp.abs(ic) < P["Imax"], s["xi"] + e * Ts, s["xi"])
            us = jnp.clip(-P["csky"] * s["vzb"], -P["Umax"], P["Umax"])
            A = ax * jnp.cos(s["phi"]) - (G + az) * jnp.sin(s["phi"])
            Kg = P["Kg"]
            IOc = jnp.where(P["IOc"] > 0, P["IOc"], P["IO"])                # the moment of inertia the controller believes
            tau = P["tune"] * (IOc / s_n[0] - P["mp"] * P["Lc"]) * A - (Kg[0] * s["phi"] + Kg[1] * s["om"] + Kg[2] * s["q"][0] + Kg[3] * s["qd"][0])
            tau = jnp.clip(tau, -P["tauMax"], P["tauMax"]) * gim
            return dict(s, icmd=ic, xi=xi, uscmd=us, taucmd=tau)

        def sub(k, carry):
            s, F = carry
            ax, az, al, azw, Nw, Fr, Fm, d = accel(s, F)
            s = lax.cond(k % ksamp == 0, lambda ss: control(ss, ax, az, Nw), lambda ss: ss, s)
            E = b * s["v"]
            il = jnp.clip(jnp.clip(s["icmd"], -P["Imax"], P["Imax"]), (-P["Vmax"] - E) / P["Ra"], (P["Vmax"] - E) / P["Ra"])
            aeff = ax * jnp.cos(s["phi"]) - (G + az) * jnp.sin(s["phi"]) - al * s_n
            gper = (G + az) * jnp.cos(s["phi"]) + ax * jnp.sin(s["phi"]) + s["om"] ** 2 * s_n
            qdd = -damp(s["qd"]) - w * w * (gper / G) * s["q"] - be * aeff
            qd = s["qd"] + hc * qdd; q = s["q"] + hc * qd
            v = s["v"] + hc * ax; vzb = s["vzb"] + hc * az; vzw = s["vzw"] + hc * azw; om = s["om"] + hc * al
            phi = jnp.clip(s["phi"] + hc * om, -P["phiMax"], P["phiMax"])
            om = jnp.where(jnp.abs(phi) >= P["phiMax"], 0.0, om)          # the stop (inelastic)
            s = dict(s, x=s["x"] + hc * v, v=v, zb=s["zb"] + hc * vzb, vzb=vzb, zw=s["zw"] + hc * vzw, vzw=vzw, phi=phi, om=om, q=q, qd=qd,
                     i=il + (s["i"] - il) * jnp.exp(-hc / P["tauI"]), us=s["uscmd"] + (s["us"] - s["uscmd"]) * jnp.exp(-hc / P["tauU"]),
                     tau=s["taucmd"] + (s["tau"] - s["taucmd"]) * jnp.exp(-hc / P["tauT"]), t=s["t"] + hc,
                     # running records of the step: largest road push and tyre load, the surface's sideways and normal specific force
                     Frmax=jnp.maximum(s["Frmax"], jnp.abs(Fr)), Nmax=jnp.maximum(s["Nmax"], Nw), air=s["air"] + hc * (Nw <= 0),
                     aS=ax * jnp.cos(s["phi"]) - (G + az) * jnp.sin(s["phi"]) - al * P["s_surf"], gS=gper[0], ax=ax, az=az)
            return (s, F)

        def body(carry, _):
            s, F, Pm = carry
            s, _ = lax.fori_loop(0, nsub, sub, (s, F))
            Pn = jnp.sum(ga * s["qd"]); Fn = -(Pn - Pm) / DT * jnp.cos(s["phi"])
            out = dict(t=s["t"], x=s["x"], v=s["v"], i=s["i"], icmd=s["icmd"], tilt=2 * jnp.sum(rg * s["q"]), wall=jnp.sum(s["q"]), phi=s["phi"],
                       om=s["om"], tau=s["tau"], zb=s["zb"], zw=s["zw"], us=s["us"], ax=s["aS"], azb=s["gS"] - G, axc=s["ax"], azc=s["az"],
                       Frmax=s["Frmax"], Nmax=s["Nmax"], air=s["air"], vref=vref(s["x"]), ilim=jnp.minimum(P["Imax"], (P["Vmax"] - b * s["v"]) / P["Ra"]))
            return (s, Fn, Pn), out

        a0, _ = axle(jnp.asarray(0.5)); z = jnp.zeros(()); zN = jnp.zeros(N)
        zw0 = a0 - (Ms + P["mw"]) * G / P["kt"]; zb0 = zw0 + P["Ls"] - Ms * G / P["k"]
        i0 = P["cx"] * P["v0"] / b
        s0 = dict(x=jnp.asarray(0.5), v=P["v0"] + z, zb=zb0, vzb=z, zw=zw0, vzw=z, phi=z, om=z, q=zN, qd=zN, i=i0 + z, icmd=i0 + z, xi=z, us=z, uscmd=z,
                  tau=z, taucmd=z, t=z, Frmax=z, Nmax=z, air=z, aS=z, gS=z + G, ax=z, az=z)
        _, out = lax.scan(body, (s0, z, z), None, length=n)
        return out

    jrun = jax.jit(run)
    info = dict(model=m, modes=[dict(x, s_depth=float(d), zeta_lin=m["zeta"]) for x, d in zip(md, mode_depth(md))])

    def go(params, road, v0):
        P = dict(BASE, **params); P["v0"] = v0; P.setdefault("vk", v0)
        if "vk" not in params: P["vk"] = v0
        rt = SJ.road_table(SM.ROADS[road] if isinstance(road, str) else road, Rw=P["Rw"], xmax=0.5 + v0 * end * 1.3 + 2)
        Pj = {k: jnp.asarray(v, jnp.float64) for k, v in P.items()}
        o = jrun(Pj, jnp.asarray(rt[0]), jnp.asarray(rt[1]), jnp.asarray(rt[2]))
        return {k: np.asarray(v) for k, v in o.items()}, P

    return go, info


def metrics(o, P, ws):
    import spill as SP
    V = SP.spill(o, ws)
    b = P["Ngear"] * P["Km"] / P["Rw"]
    return dict(tilt_mm=float(np.abs(o["tilt"]).max() * 1e3), wall_mm=float(np.abs(o["wall"]).max() * 1e3), spill_ml=float(V[-1] * 1e6),
                v_min=float(o["v"].min()), v_max=float(o["v"].max()), Fr_max_N=float(o["Frmax"][-1]), N_max_N=float(o["Nmax"][-1]), air_ms=float(o["air"][-1] * 1e3),
                i_max_A=float(np.abs(o["i"]).max()), i_lim_A=float(P["Imax"]), F_motor_max_N=float(np.abs(o["i"]).max() * b),
                sat_ms=float((np.abs(o["icmd"]) > o["ilim"] + 1e-9).sum() * 2.0),
                phi_max_deg=float(np.degrees(np.abs(o["phi"]).max())), tau_max_Nm=float(np.abs(o["tau"]).max()),
                stroke_mm=float((np.ptp(o["zb"] - o["zw"])) * 1e3), az_body=float(np.abs(o["azc"]).max()), t_end=float(o["t"][-1]), x_end=float(o["x"][-1]))


if __name__ == "__main__":
    # check: Fig. 12's cart in this simulator against slosh_model.simulate (the validated one), speed held, the kerb
    go, info = build(4.0)
    o, P = go({}, "one sharp 30 mm bump", 1.5)
    ml = SM.liquid_mass(); o2, _ = SM.simulate("one sharp 30 mm bump", 1.5, "speed", 4.0, model=SM.fitted())
    o, P = go(dict(Mb=1.5 + ml), "one sharp 30 mm bump", 1.5)
    print("this simulator: tilt max %.2f mm, v min %.3f, i max %.2f | slosh_model: tilt max %.2f mm, v min %.3f, i max %.2f" % (
        np.abs(o["tilt"]).max() * 1e3, o["v"].min(), np.abs(o["i"]).max(), np.abs(o2["tilt"]).max() * 1e3, o2["v"].min(), np.abs(o2["i"]).max()))
    print("rms difference of the tilt histories: %.3f mm" % (np.sqrt(np.mean((o["tilt"] - o2["tilt"]) ** 2)) * 1e3))
