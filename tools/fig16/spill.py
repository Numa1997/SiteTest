"""Fig. 16: the head of foam spilled, from the slosh model's wall height, by the solver's own rule (stout_jax.Stout.head_spill).

At the angle theta round the rim the surface stands eta = wall(t) cos(theta) above the fill (the cos theta modes of slosh_model.py).
The head's top is then e = eta + h_f(theta) - (z_rim - fill) above the rim. The part above the rim breaks off whole once
    rho_f (|g + a_z| e / 2 + a_out e) >= tau_y,     a_out = -a_x cos(theta)  (the outward push in the glass's frame)      (S1)
and leaves; the head there is thinned by what broke off (h_f -= min(e, h_f)). The volume is cut x the area of the strip of head at the
wall that can break, w_s R dtheta. w_s is the only unknown: it is set so that run 8's kerb ride with the speed held (2.44 mL) is
matched, and nothing else (validate.py checks it on the other rides)."""
import json, math, os
import numpy as np
import slosh_model as SM, stout_jax as SJ

Z_RIM = (len(SM.GLASS_R) - 1) * SM.DZP
R_RIM = float(SM.GLASS_R[-1])
NTH = 64


def spill(o, ws, hf0=SJ.HEAD0, rho_f=SM.RHO_F, tau_y=SJ.TAU_Y, R=SM.R_FILL):
    th = 2 * np.pi * (np.arange(NTH) + 0.5) / NTH; c = np.cos(th)
    hf = np.full(NTH, hf0); vol = 0.0; V = np.zeros(len(o["t"]))
    for k in range(len(o["t"])):
        eta = o["wall"][k] * c
        e = eta + hf - (Z_RIM - SM.FILL)
        aout = np.maximum(-o["ax"][k] * c, 0.0)
        fail = (e > 0) & (hf > 0) & (rho_f * (abs(SM.G + o["azb"][k]) * 0.5 + aout) * e >= tau_y)
        cut = np.where(fail, np.minimum(e, hf), 0.0)
        hf -= cut; vol += cut.sum() * ws * R * (2 * np.pi / NTH); V[k] = vol
    return V


if __name__ == "__main__":
    print(f"z_rim {Z_RIM * 1e3:.2f} mm, rim radius {R_RIM * 1e3:.2f} mm, head top below rim {(Z_RIM - SM.FILL - SJ.HEAD0) * 1e3:.2f} mm, "
          f"e* at rest {SJ.TAU_Y / (SM.RHO_F * SM.G / 2) * 1e3:.2f} mm")
