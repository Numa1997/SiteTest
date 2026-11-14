"""Fig. 16: the pint as a few sloshing modes, coupled both ways to Fig. 12's cart, on the CPU.

The fluid of Fig. 12 (a million particles on the GPU) is replaced by the first N modes with one wave around the glass (cos theta),
each the equation the Fig. 12 note derives for the first (eqs. 11 and 26), with its own zero xi_n of J1':
    q_n'' + D_n(q_n') + w_n^2 (1 + a_z/g) q_n = -beta_n a_x                                      (M1)
q_n: mode n's height at the front wall [m]; a_x, a_z: the glass's acceleration along the road and upward;
w_n^2 = g k_n tanh(k_n h) / (1 + lambda_h k_n tanh(k_n h)), k_n = xi_n / R (note eq. 25, the head's mass);
beta_n = 2 xi_n tanh(k_n h) / ((xi_n^2 - 1)(1 + lambda_h k_n tanh(k_n h))) (note eqs. 11 and 26 with xi_n in place of xi_1).
The first mode's frequency is run 8's measured 2.915 Hz (free_full_1.5, ring 13); the others keep the theory's ratio to it.
D_n: the swing's friction, 2 zeta w_n q' (|q'| / (w_n qref))^(n_d - 1) (damping(); n_d = 2/3 is Cantat's sliding law of the head).
The stout pushes back on the cart (note eq. 30) with F_x = -dP/dt, P its momentum relative to the glass; for mode n,
P_n = rho integral of u_x dV = rho pi R^3 q_n' / xi_n^2 (the potential's flux through the wall; notes/fig16/model.md), so
    F_x = -sum_n gamma_n q_n'',  gamma_n = rho pi R^3 / xi_n^2                                      (M2)
What the stored rides call the tilt is twice the cos theta part of the surface on the ring r_m = R_fill - dx/2:
    tilt = 2 sum_n q_n J1(k_n r_m) / J1(xi_n)                                                      (M3)
The cart is Fig. 12's Cart class itself (tools/fig12/kaggle/stout_jax.py), imported unchanged, with its controllers, observer,
current lag, back-EMF, tyre and suspension; sub-steps of 0.1 ms inside "fluid" steps of DT, as make_advance does: the probes read
the wall height once per fluid step, the cart feels the stout's push of the previous fluid step. F_z (vertical push) is set to zero.
Nothing here is fitted to the controlled rides of run 10: they are the validation (validate.py)."""
import json, math, os, sys
import numpy as np
from scipy.special import j1

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax, jax.numpy as jnp
from jax import lax
import stout_jax as SJ

XI = [1.8412, 5.3314, 8.5363, 11.7060]       # zeros of J1' (DLMF table 10.21)
XI1 = XI[0]; FILL = 0.125; RHO = 1007.0; RHO_F = 272.0; G = 9.81
GLASS_R = np.array(json.load(open(os.path.join(ROOT, "tools", "fig12", "glass_profile.json")))["R"]); DZP = 0.0005
R_FILL = float(np.interp(FILL / DZP, np.arange(len(GLASS_R)), GLASS_R))
R_S = 0.0391                                   # the surface's radius run_b.py uses for beta
R_M = R_FILL - 0.0015 / 2                      # the ring the stored tilt is read on
LAM_H = SJ.PHI_F * SJ.HEAD0                    # m, the head's mass per area over rho (note eq. 25)
K1 = XI1 / R_S
BETA = 2 * XI1 * math.tanh(XI1 * FILL / R_S) / (XI1 ** 2 - 1)
HEAD_FAC = 1 + LAM_H * K1 * math.tanh(K1 * FILL)
BETA_H = BETA / HEAD_FAC
GAMMA_TH = RHO * math.pi * R_S ** 3 / XI1 ** 2
# the stout's push measured on the two gentle training rides (run 8, speed held): F_x against -q'' (q = tilt/2), least squares,
# gave 79.7 g (five bumps) and 71.7 g (one 25 mm bump), correlation 0.96 each; the cylinder's theory gives 55.8 g. The mean, 75.7 g,
# is used (gamma_check.py prints these numbers).
GAMMA_SCALE = 75.7e-3 / GAMMA_TH
# the swing with the head, measured by run 8 (free_full_1.5, ring 13), the plant run 10's controllers were designed on
PLANT8 = dict(f0=2.9152394311359466, zeta=0.4250231022393094)


def modes(N, f1=PLANT8["f0"], R=R_S, h=FILL, lam=LAM_H):
    """Frequency [Hz], drive beta_n, push gamma_n [kg] and ring weight J1(k_n r_m)/J1(xi_n) of the first N modes."""
    out = []
    for xi in XI[:N]:
        k = xi / R; th = math.tanh(k * h); fac = 1 + lam * k * th
        out.append(dict(xi=xi, f_th=math.sqrt(G * k * th / fac) / (2 * math.pi), beta=2 * xi * th / ((xi * xi - 1) * fac),
                        gamma=RHO * math.pi * R ** 3 / xi ** 2, ring=float(j1(k * R_M) / j1(xi))))
    s = f1 / out[0]["f_th"]
    for m in out: m["f"] = m["f_th"] * s
    return out


def _roads():
    src = open(os.path.join(ROOT, "tools", "fig12", "kaggle", "run_b.py")).read(); a = src.index("ROADS = {"); b = src.index("\n}\n", a) + 2
    return eval(src[a + len("ROADS = "):b])


ROADS = _roads()


def liquid_mass():
    """m_l as ride_extra sets it: the stout (429.583 g, stored books) plus the head (rho_f h_f times the glass's open area at the
    fill, read from the stored head volume: 91.314 mL)."""
    return 0.4295833 + RHO_F * 91.314e-6


def damping(w, zeta, n, qref, eps=1e-4):
    """The swing's friction per unit q: 2 zeta w q' (|q'| / (w qref))^(n - 1). n = 1: linear, zeta the damping ratio.
    n = 2/3: the head's edge sliding on the glass by Cantat's law (stress ~ Ca^(2/3), stout_jax.head_wall_stress), with zeta the
    damping ratio of a swing whose speed amplitude is w qref. eps regularises |q'| at rest (1e-4 m/s)."""
    def f(qd):
        s = jnp.sqrt(qd * qd + eps * eps)
        return 2 * zeta * w * qd * (s / (w * qref)) ** (n - 1)
    return f


def _setup(model):
    m = dict(N=1, f0=PLANT8["f0"], zeta=PLANT8["zeta"], zeta_hi=None, n=1.0, qref=0.005, beta_scale=1.0, gamma_scale=GAMMA_SCALE); m.update(model or {})
    md = modes(m["N"], f1=m["f0"])
    w = jnp.asarray([2 * math.pi * x["f"] for x in md]); be = jnp.asarray([x["beta"] * m["beta_scale"] for x in md])
    ga = jnp.asarray([x["gamma"] * m["gamma_scale"] for x in md]); rg = jnp.asarray([x["ring"] for x in md])
    zh = m["zeta"] if m["zeta_hi"] is None else m["zeta_hi"]
    ze = jnp.asarray([m["zeta"]] + [zh] * (m["N"] - 1))
    def damp(qd, eps=1e-4):
        s_ = jnp.sqrt(qd * qd + eps * eps)
        return 2 * ze * w * qd * (s_ / (w * m["qref"])) ** (m["n"] - 1)
    return m, md, w, be, ga, rg, damp


def free_swing(end=5.0, push=(0.3, 1.0, 0.146), model=None, DT=1e-4):
    """The glass held still and given one push a = pa sin(pi (t - t0)/T) (run_b.py's free_full_1.5): the tilt (M3) every DT."""
    m, md, w, be, ga, rg, damp = _setup(model); t0, pa, pT = push
    def body(c, k):
        q, qd = c; tm = k * DT + 0.5 * DT
        ax = jnp.where((tm >= t0) & (tm < t0 + pT), pa * jnp.sin(jnp.pi * (tm - t0) / pT), 0.0)
        qd = qd + DT * (-damp(qd) - w * w * q - be * ax); q = q + DT * qd
        return (q, qd), 2 * jnp.sum(rg * q)
    n = int(round(end / DT)); z = jnp.zeros(m["N"])
    _, T = jax.jit(lambda: lax.scan(body, (z, z), jnp.arange(n)))()
    return np.arange(1, n + 1) * DT, np.asarray(T)


def simulate(road, v0, ctrl, end, model=None, cart_params=None, DT=0.002, x0=0.5, ctrl_plant=None, susp=0):
    """One ride of the coupled cart + slosh model. Returns arrays sampled every fluid step (tilt as M3, wall = sum q_n)."""
    m, md, w, be, ga, rg, damp = _setup(model)
    cp = ctrl_plant or dict(w=2 * math.pi * PLANT8["f0"], zeta=PLANT8["zeta"], beta=BETA_H)
    P = dict(SJ.CART_COMMON, **(cart_params or {}))
    rt = SJ.road_table(ROADS[road] if isinstance(road, str) else road, Rw=P["Rw"], xmax=x0 + v0 * end * 1.3 + 2)
    cart = SJ.Cart(dict(P, v0=v0, ctrl=ctrl, susp=susp, plant=cp), rt)
    ml = liquid_mass(); c0 = cart.init(x0, ml)
    nsub = int(round(DT / 1e-4)); hc = DT / nsub

    def body(carry, _):
        c, q, qd, F, Pm = carry
        c = dict(c, py=jnp.sum(q), pfresh=jnp.ones((), jnp.float64))     # the wall probes read the surface the last step left
        def sub(k, cc):
            c_, q_, qd_ = cc
            c_ = cart.step(c_, hc, F, 0.0)
            qdd = -damp(qd_) - w * w * (1 + c_["azb"] / G) * q_ - be * c_["ax"]
            qd_ = qd_ + hc * qdd; q_ = q_ + hc * qd_                      # semi-implicit Euler at 0.1 ms
            return (c_, q_, qd_)
        c, q, qd = lax.fori_loop(0, nsub, sub, (c, q, qd))
        Pn = jnp.sum(ga * qd); Fn = -(Pn - Pm) / DT
        out = dict(t=c["t"], x=c["x"], v=c["vx"], i=c["i"], icmd=c["icmd"], tilt=2 * jnp.sum(rg * q), wall=jnp.sum(q), q=q,
                   qhat=c["oxh"][1], F=Fn, N=c["N"], zb=c["zb"], zw=c["zw"], us=c["us"], ax=c["ax"], azb=c["azb"])
        return (c, q, qd, Fn, Pn), out

    n = int(round(end / DT)); z = jnp.zeros(m["N"]); z0 = jnp.zeros((), jnp.float64)
    _, out = jax.jit(lambda c: lax.scan(body, (c, z, z, z0, z0), None, length=n))(c0)
    return {k: np.asarray(v) for k, v in out.items()}, dict(m, modes=md, K=np.asarray(cart.K).tolist(), ml=ml)


if __name__ == "__main__":
    print(f"R_fill {R_FILL:.4f} m, beta {BETA:.4f}, head factor {HEAD_FAC:.4f}, beta_h {BETA_H:.4f}, gamma {GAMMA_TH * 1e3:.2f} g")
    for x in modes(4): print({k: round(v, 4) for k, v in x.items()})
    o, m = simulate("one sharp 30 mm bump", 1.5, "joint", 4.0, model=dict(N=3))
    print("K", np.round(m["K"], 3), "max |tilt|", np.abs(o["tilt"]).max() * 1e3, "mm")
