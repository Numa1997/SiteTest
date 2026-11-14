"""Fig. 16: the four-wheel cart (cart4.py) carrying the validated few-mode stout (tools/fig16/slosh_model.py, fit.json), used inside
the Kaggle notebook only to choose among a few weightings of the controller before the fluid rides. Nothing from here is shown as a
ride: the rides are Fig. 12's fluid solver (run16.py).
The modes live in the glass's frame: q_n'' + D_n(q_n') + w_n^2 (g_perp/g) q_n = beta_n g_x  (g_x, g_perp = -g_z from Cart4.forces),
and push back along the glass's x with F = -sum gamma_n q_n'' (notes/fig16/model.md, section 2)."""
import numpy as np
import jax, jax.numpy as jnp
from jax import lax
import slosh_model as SM, spill as SP

F64 = jnp.float64


def ride(cart, end, ml, DT=0.002, model=None, push=1.0):
    m, md, w, be, ga, rg, damp = SM._setup(dict(SM.fitted(), **(model or {})))
    c0 = cart.init(0.5, ml); nsub = int(round(DT / 1e-4)); hc = DT / nsub; n = int(round(end / DT)); N = m["N"]

    def body(carry, _):
        c, q, qd, F, Pm = carry
        c = dict(c, py=jnp.sum(q), pfresh=jnp.ones((), F64))
        def sub(k, cc):
            c_, q_, qd_ = cc
            c_ = cart.step(c_, hc, F, 0.0)
            qdd = -damp(qd_) - w * w * (-c_["gz"] / SM.G) * q_ + be * c_["gx"]
            qd_ = qd_ + hc * qdd; q_ = q_ + hc * qd_
            return (c_, q_, qd_)
        c, q, qd = lax.fori_loop(0, nsub, sub, (c, q, qd))
        Pn = jnp.sum(ga * qd); Fn = -(Pn - Pm) / DT * push
        out = dict(t=c["t"], x=c["x"], v=c["v"], tilt=2 * jnp.sum(rg * q), wall=jnp.sum(q), th=c["th"], ax=-c["gx"], azb=-c["gz"] - SM.G,
                   i=c["i"], uf=c["uf"], ur=c["ur"], sat=c["sat"], stop=jnp.maximum(c["stopf"], c["stopr"]), Nf=c["Nf"], Nr=c["Nr"])
        return (c, q, qd, Fn, Pn), out

    z = jnp.zeros(N, F64); z0 = jnp.zeros((), F64)
    _, out = jax.jit(lambda c: lax.scan(body, (c, z, z, z0, z0), None, length=n))(c0)
    o = {k: np.asarray(v) for k, v in out.items()}
    return o


def score(o, ws):
    V = SP.spill(o, ws)
    return dict(tilt_mm=float(np.abs(o["tilt"]).max() * 1e3), wall_mm=float(np.abs(o["wall"]).max() * 1e3), head_spill_ml=float(V[-1] * 1e6),
                pitch_deg=float(np.degrees(np.abs(o["th"] - o["th"][0]).max())), v_min=float(o["v"].min()), i_max=float(np.abs(o["i"]).max()),
                u_max=float(max(np.abs(o["uf"]).max(), np.abs(o["ur"]).max())), stop_N=float(o["stop"].max()), sat=float(o["sat"][-1]),
                airborne=bool((np.minimum(o["Nf"], o["Nr"]) <= 0).any()))
