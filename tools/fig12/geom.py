"""The Guinness Gravity pint glass as a surface R(z, theta): the tulip profile from a dimensioned drawing, plus the two
sculpted panels of the lower body ("curves inspired by the harp", Diageo 2010) that make the cavity two-fold symmetric
about its axis instead of a body of revolution.

Profile: `profile_drawing.csv`, the elevation outline of dimensions.com's "Irish Imperial Pint Glass" (height 149 mm,
3" diameter as drawn, a 473 mL glass), scaled here to the published imperial glass: H = 160 mm tall, widest outer
diameter D_MAX = 85 mm. The two scalings differ by 4 % (160/149 = 1.074 in z, 85/81.5 = 1.043 in r); we use both, so
the glass is a slightly stretched copy of the drawing. Marked as a modelling choice in the note.

Panels (the user's "one part is a little deeper than the other, and the same on the opposite side"): on the front and
the back, inside a V-shaped crease that starts near the foot at the centre line and sweeps up to the sides at about half
height, the wall is recessed by A_PANEL. Seen in product photographs (Guinness webstore, Amazon listing of the official
glass); the depth A_PANEL = 2.0 mm is estimated from those photographs, not measured, and is the one number here that
is an opinion. The crease is a smooth step of angular width W_CREASE.

Coordinates: z up from the foot plane (mm), theta from the front centre line (rad). R_outer(z, theta) and R_inner.
"""
import os, numpy as np
from scipy.interpolate import UnivariateSpline

H, D_MAX, T_W, Z_F = 160.0, 85.0, 2.0, 8.0          # mm: height, widest outer diameter, wall, cavity floor above the foot
A_PANEL, W_CREASE = 2.0, np.radians(6.0)            # mm, rad
Z_V0, Z_V1, Z_FADE0, Z_V2 = 16.0, 80.0, 60.0, 100.0  # mm: bottom of the V, height where its arms reach the sides, start and end of the fade

_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profile_drawing.csv')
_d = np.loadtxt(_csv, delimiter=',')
_h_units = _d[:, 0]; _r_units = 0.5 * (_d[:, 1] + _d[:, 2])
_H_UNITS = 462.6                                     # total height of the drawing, units (rim line to foot line)
_sz = H / _H_UNITS; _sr = (D_MAX / 2) / _r_units.max()
_z = _h_units * _sz; _r = _r_units * _sr
_o = np.argsort(_z); _z, _r = _z[_o], _r[_o]
_spl = UnivariateSpline(_z, _r, s=len(_z) * 0.05 ** 2, k=3)   # 0.05 mm rms: the drawing is vector, only its sampling is noisy


def R0(z):
    """Outer radius of the body of revolution, mm, for z in [0, H]."""
    z = np.asarray(z, dtype=float)
    return _spl(np.clip(z, _z.min(), _z.max()))


def panel(z, theta):
    """Recess weight in [0, 1]: 1 inside the sculpted panel (front and back), 0 on the round wall."""
    z = np.asarray(z, dtype=float); theta = np.asarray(theta, dtype=float)
    t = np.abs(np.remainder(theta + np.pi / 2, np.pi) - np.pi / 2)      # angle from the nearer centre line, 0..pi/2 (two-fold)
    u = np.clip((z - Z_V0) / (Z_V1 - Z_V0), 0.0, 1.0)
    th_v = (np.pi / 2 - W_CREASE) * np.sqrt(u)                           # half-width of the V at height z; a round strip stays at the sides
    w = W_CREASE + np.clip((z - Z_FADE0) / (Z_V2 - Z_FADE0), 0.0, 1.0) * (np.radians(60) - W_CREASE)   # the crease softens as it rises
    step = 0.5 * (1 + np.tanh((th_v - t) / (w / 2)))                     # inside the V
    fade = np.clip((Z_V2 - z) / (Z_V2 - Z_FADE0), 0.0, 1.0)              # the recess blends into the round body between Z_FADE0 and Z_V2
    low = 0.5 * (1 + np.tanh((z - Z_V0) / 2.0))                          # no recess below the V
    return step * fade * low


def R_outer(z, theta):
    return R0(z) - A_PANEL * panel(z, theta)


def R_inner(z, theta):
    """Inner radius: the wall is T_W thick, measured normal to the profile of revolution (the panel recess is carried inward unchanged)."""
    z = np.asarray(z, dtype=float)
    dz = 0.25; slope = (R0(z + dz) - R0(z - dz)) / (2 * dz)
    return R0(z) - T_W * np.sqrt(1 + slope ** 2) - A_PANEL * panel(z, theta)


def cavity_volume(h, nz=2001, nt=256):
    """Cavity volume below height h (mm^3), by quadrature in (z, theta)."""
    zq = np.linspace(Z_F, h, nz); tq = (np.arange(nt) + 0.5) * 2 * np.pi / nt
    Ri = R_inner(zq[:, None], tq[None, :])
    return np.trapezoid(0.5 * np.mean(Ri ** 2, axis=1) * 2 * np.pi, zq)


if __name__ == '__main__':
    zz = np.arange(0, H + 1e-9, 0.5)
    print(f'outer: foot {2*R0(0):.1f}, waist {2*R0(zz[(zz>15)&(zz<60)]).min():.1f} at z = {zz[(zz>15)&(zz<60)][np.argmin(R0(zz[(zz>15)&(zz<60)]))]:.1f}, '
          f'widest {2*R0(zz).max():.1f} at z = {zz[np.argmax(R0(zz))]:.1f}, rim {2*R0(H):.1f} mm')
    Vb = cavity_volume(H); print(f'brim {Vb/1e3:.1f} mL')
    hs = np.arange(Z_F + 1, H, 0.25); Vs = np.array([cavity_volume(h, nz=401, nt=64) for h in hs])
    print(f'568 mL at z = {np.interp(568e3, Vs, hs):.1f} mm; 500 mL at z = {np.interp(500e3, Vs, hs):.1f} mm')
    print(f'panel: max recess {A_PANEL} mm; cross-section at z = 50 mm: R_in front {R_inner(50, 0):.2f}, side {R_inner(50, np.pi/2):.2f} mm')
