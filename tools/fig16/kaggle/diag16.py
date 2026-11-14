"""Fig. 16, diagnostics on Kaggle's CPU (no GPU quota): the four-wheel cart (cart4.py) with the validated few-mode stout (modal4.py)
on Fig. 12's three roads, control on and off. Writes /kaggle/working/diag/: diag.json (per ride: the largest pitch, heave, stroke,
tyre loads, time in the air, bump-stop force, the smallest effective gravity along the glass, the wall rise, head spilled), one .npz
per ride with the histories, and diag.png (pitch, effective gravity, wall rise, tyre loads, current, actuators against time)."""
import os, json, time
import numpy as np
import jax
jax.config.update("jax_platform_name", "cpu")
import jax.numpy as jnp
from jax import lax
import cart4 as C4, modal4, slosh_model as SM
from stout_jax import road_table

OUT = "/kaggle/working/diag"; os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(os.path.dirname(os.path.abspath(C4.__file__)), "..", "..", "fig12", "kaggle", "run_b.py")).read()
a = src.index("ROADS = {"); b = src.index("\n}\n", a) + 2; ROADS = eval(src[a + len("ROADS = "):b])
WS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(SM.__file__)), "validation.json")))["ws_mm"] * 1e-3
ML = SM.liquid_mass()
RIDES = [("kerb", "one sharp 30 mm bump", 1.5, 4.0), ("five bumps", "five 20 mm bumps in step with the swing", 1.0, 8.0), ("25 mm bump", "one 25 mm bump", 1.0, 8.0)]


def ride_full(cart, end, DT=0.002, model=None, push=1.0):
    """modal4.ride, keeping every cart signal needed to diagnose."""
    m, md, w, be, ga, rg, damp = SM._setup(dict(SM.fitted(), **(model or {})))
    c0 = cart.init(0.5, ML); nsub = int(round(DT / 1e-4)); hc = DT / nsub; n = int(round(end / DT))
    def body(carry, _):
        c, q, qd, F, Pm = carry
        c = dict(c, py=jnp.sum(q), pfresh=jnp.ones((), jnp.float64))
        def sub(k, cc):
            c_, q_, qd_ = cc; c_ = cart.step(c_, hc, F, 0.0)
            qdd = -damp(qd_) - w * w * (-c_["gz"] / SM.G) * q_ + be * c_["gx"]
            qd_ = qd_ + hc * qdd; return (c_, q_ + hc * qd_, qd_)
        c, q, qd = lax.fori_loop(0, nsub, sub, (c, q, qd))
        Pn = jnp.sum(ga * qd); Fn = -(Pn - Pm) / DT * push
        out = {k: c[k] for k in ("t", "x", "v", "zc", "th", "om", "zf", "zr", "i", "icmd", "uf", "ur", "Nf", "Nr", "gx", "gz", "stopf", "stopr", "zaf", "zar", "ax", "azc", "al")}
        out.update(wall=jnp.sum(q), tilt=2 * jnp.sum(rg * q), qhat=c["qh"][0], azb=-c["gz"] - SM.G)
        out["ax_glass"] = -c["gx"]
        return (c, q, qd, Fn, Pn), out
    z = jnp.zeros(m["N"]); z0 = jnp.zeros(())
    _, out = jax.jit(lambda c: lax.scan(body, (c, z, z, z0, z0), None, length=n))(c0)
    return {k: np.asarray(v) for k, v in out.items()}


res = {}; hist = {}
for short, road, v0, end in RIDES:
    rt = road_table(ROADS[road], Rw=C4.CART4["Rw"], xmax=0.5 + v0 * end * 1.3 + 2)
    for ctrl, var, model, push in (("full", "measured push", None, 1.0), ("off", "measured push", None, 1.0), ("off", "no push", None, 0.0),
                                   ("off", "theory push", dict(gamma_scale=1.0), 1.0), ("full", "theory push", dict(gamma_scale=1.0), 1.0)):
        T1 = time.time(); cart = C4.Cart4({}, rt, v0, ctrl); o = ride_full(cart, end, model=model, push=push); ctrl_ = ctrl; ctrl = f"{ctrl_}, {var}"
        S = cart.S; sf = o["zc"] + C4.CART4["af"] * np.sin(o["th"]) - o["zf"] - S["sf0"]; sr = o["zc"] - C4.CART4["ar"] * np.sin(o["th"]) - o["zr"] - S["sr0"]
        o["ax"] = o["ax_glass"]
        V = __import__("spill").spill(o, WS)
        r = dict(pitch_deg=float(np.degrees(np.abs(o["th"] - o["th"][0]).max())), heave_mm=float(np.abs(o["zc"] - o["zc"][0]).max() * 1e3),
                 stroke_mm=float(max(np.abs(sf).max(), np.abs(sr).max()) * 1e3), Nf_max=float(o["Nf"].max()), Nr_max=float(o["Nr"].max()),
                 air_ms=float(((o["Nf"] <= 0) | (o["Nr"] <= 0)).sum() * 2.0), stop_N=float(max(o["stopf"].max(), o["stopr"].max())),
                 g_perp_min=float((-o["gz"]).min()), g_perp_max=float((-o["gz"]).max()), a_glass_max=float(np.abs(o["ax_glass"]).max()),
                 wall_mm=float(np.abs(o["wall"]).max() * 1e3), tilt_mm=float(np.abs(o["tilt"]).max() * 1e3), head_spill_ml=float(V[-1] * 1e6),
                 v_min=float(o["v"].min()), v_max=float(o["v"].max()), i_max=float(np.abs(o["i"]).max()), u_max=float(max(np.abs(o["uf"]).max(), np.abs(o["ur"]).max())),
                 finite=bool(np.all(np.isfinite(o["wall"]))), seconds=round(time.time() - T1, 1),
                 first_bad_t=float(o["t"][np.argmax(np.abs(o["wall"]) > 0.03)]) if (np.abs(o["wall"]) > 0.03).any() else None)
        res[f"{short} / {ctrl}"] = r; hist[f"{short}/{ctrl}"] = o
        np.savez_compressed(os.path.join(OUT, f"{short}_{ctrl}".replace(' ', '_').replace(',', '') + ".npz"), **o)
        print(f"{short:10s} {ctrl:4s}", json.dumps(r), flush=True)
json.dump(dict(rides=res, cart=C4.CART4, statics={k: float(v) for k, v in C4.statics(C4.CART4, ML).items()}), open(os.path.join(OUT, "diag.json"), "w"), indent=1)

import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
keys = ["kerb/off, measured push", "kerb/off, theory push", "kerb/off, no push", "kerb/full, theory push"]
fig, ax = plt.subplots(6, 4, figsize=(24, 16), sharex="col")
for j, k in enumerate(keys):
    o = hist[k]; t = o["t"]; lim = (0.4, 2.5)
    ax[0, j].plot(t, np.degrees(o["th"] - o["th"][0])); ax[0, j].set_ylabel("deck pitch, deg")
    ax[1, j].plot(t, -o["gz"], label="g along the glass's axis"); ax[1, j].plot(t, o["ax_glass"], label="sideways push on the stout"); ax[1, j].legend(fontsize=7); ax[1, j].set_ylabel("m/s^2")
    ax[2, j].plot(t, o["wall"] * 1e3, label="wall (model)"); ax[2, j].plot(t, o["qhat"] * 1e3, "--", label="Kalman estimate"); ax[2, j].legend(fontsize=7); ax[2, j].set_ylabel("mm")
    ax[3, j].plot(t, o["Nf"], label="front tyres"); ax[3, j].plot(t, o["Nr"], label="rear tyres"); ax[3, j].plot(t, o["stopf"], ":", label="front stop"); ax[3, j].plot(t, o["stopr"], ":", label="rear stop"); ax[3, j].legend(fontsize=7); ax[3, j].set_ylabel("N")
    ax[4, j].plot(t, o["i"], label="motor current"); ax[4, j].plot(t, o["icmd"], ":", label="command"); ax[4, j].legend(fontsize=7); ax[4, j].set_ylabel("A")
    ax[5, j].plot(t, o["uf"], label="front actuators"); ax[5, j].plot(t, o["ur"], label="rear actuators"); ax[5, j].legend(fontsize=7); ax[5, j].set_ylabel("N"); ax[5, j].set_xlabel("time, s")
    ax[0, j].set_title(k)
    for a_ in ax[:, j]: a_.set_xlim(*lim); a_.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "diag.png"), dpi=70)
print("done")
