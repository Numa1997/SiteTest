"""Fig. 16: mass properties of what the gimbal carries, from the measured glass profile (tools/fig12/glass_profile.json).
The stout and its head as a frozen body (their mass, centre of mass and moment of inertia from the profile); the glass as a shell
of uniform wall thickness with a solid foot; a cradle ring. Assumptions (not measured): glass mass 0.40 kg (a tulip pint glass),
foot 14 mm thick (stout_jax.BODY_TOP). The liquid is taken to turn with the glass as a rigid body; a liquid without friction turns
less than that, so I_O here is an upper bound (the tuning study in concepts.py varies it)."""
import math, numpy as np
import slosh_model as SM, stout_jax as SJ

R = SM.GLASS_R; z = np.arange(len(R)) * SM.DZP


def liquid():
    m = z <= SM.FILL; zz = z[m]; rr = R[m]; dz = SM.DZP
    dm = SM.RHO * math.pi * rr ** 2 * dz; M = dm.sum(); zc = (dm * zz).sum() / M
    Ic = (dm * (rr ** 2 / 4 + (zz - zc) ** 2)).sum()
    # the head: a disc of foam on the surface
    mh = SM.RHO_F * math.pi * SM.R_FILL ** 2 * SJ.HEAD0; zh = SM.FILL + SJ.HEAD0 / 2
    Mt = M + mh; zt = (M * zc + mh * zh) / Mt
    It = Ic + M * (zc - zt) ** 2 + mh * (SM.R_FILL ** 2 / 4 + SJ.HEAD0 ** 2 / 12 + (zh - zt) ** 2)
    return Mt, zt, It


def glass(mass=0.40, foot=0.014):
    # foot: a solid disc below the inner floor; wall: a shell following the profile; their shares by volume of glass, wall 3 mm
    tw = 0.003; ds = np.hypot(np.diff(R), SM.DZP); rm = 0.5 * (R[1:] + R[:-1]); zm = 0.5 * (z[1:] + z[:-1])
    vw = 2 * math.pi * rm * ds * tw; vf = math.pi * 0.032 ** 2 * foot
    rho = mass / (vw.sum() + vf)
    mw = rho * vw; mf = rho * vf; zf = -foot / 2
    zc = ((mw * zm).sum() + mf * zf) / mass
    Ic = (mw * (rm ** 2 / 2 + (zm - zc) ** 2)).sum() + mf * (0.032 ** 2 / 4 + foot ** 2 / 12 + (zf - zc) ** 2)
    return mass, zc, Ic


def pendulum(z_pivot, cradle=0.15, z_cradle=None, r_cradle=0.05, trim=0.0, z_trim=0.0):
    """Glass + liquid + a cradle ring (mass `cradle` at height z_cradle, default the pivot) + a trim mass. Heights above the glass's
    inner floor. Returns m_p, L_c (centre of mass below the pivot), I_O (about the pivot), s_surf (the surface below the pivot)."""
    parts = [liquid(), glass(), (cradle, z_pivot if z_cradle is None else z_cradle, cradle * r_cradle ** 2 / 2), (trim, z_trim, 0.0)]
    M = sum(p[0] for p in parts); zc = sum(p[0] * p[1] for p in parts) / M
    IO = sum(p[2] + p[0] * (p[1] - z_pivot) ** 2 for p in parts)
    return dict(mp=M, Lc=z_pivot - zc, IO=IO, s_surf=z_pivot - SM.FILL, Leq=IO / (M * (z_pivot - zc)), zcm=zc)


if __name__ == "__main__":
    L = liquid(); print("liquid (stout + head): %.4f kg, centre %.1f mm above the floor, I %.3e kg m^2" % (L[0], L[1] * 1e3, L[2]))
    Gl = glass(); print("glass: %.2f kg, centre %.1f mm, I %.3e kg m^2" % (Gl[0], Gl[1] * 1e3, Gl[2]))
    d1 = 2 * SM.R_S / SM.XI1 * math.tanh(SM.XI1 * SM.FILL / (2 * SM.R_S))
    print("first mode's point: %.1f mm below the surface, %.1f mm above the floor" % (d1 * 1e3, (SM.FILL - d1) * 1e3))
    for zp in (0.10, 0.125, 0.15, 0.20, 0.25, 0.30):
        p = pendulum(zp); print("pivot %3.0f mm: m_p %.3f kg, L_c %5.1f mm, L_eq %5.1f mm, first mode's point %5.1f mm below the pivot, T %.2f s" % (
            zp * 1e3, p["mp"], p["Lc"] * 1e3, p["Leq"] * 1e3, (p["s_surf"] + d1) * 1e3, 2 * math.pi * math.sqrt(p["Leq"] / 9.81)))
