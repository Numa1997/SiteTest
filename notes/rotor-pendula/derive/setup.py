"""The setup of the notes, defined once; every script imports it.

Turbine: NREL 5-MW reference (Jonkman et al. 2009, NREL/TP-500-38060): rotor radius 63 m (Table 1-1), peak power coefficient
0.482 at tip-speed ratio 7.55 (Table 7-2).  In region 2 the controller holds the rotor at that tip-speed ratio, so a steady wind v
gives Omega = 7.55 v / 63 m.  Three steady winds, 6, 8 and 10 m/s, span region 2 (6 m/s gives 6.9 rpm, the turbine's cut-in rotor
speed; 10 m/s gives 11.4 rpm, below the rated 12.1 rpm).  Pivots at 30, 60 and 90 % of the rotor radius.

Pendulum: a rod of L = 0.1 m (the whole device fits in a box about 0.2 m across, inside the blade shell at all three pivots: the
thinnest section, at 90 %, is 0.41 m thick and 2.26 m wide, dossier-turbine.md).  The bob's mass M is sized in design.py: the
smallest mass of the 1-2-5 series whose worst mounting still gives the sensor ten times its need through the real generator,
with twice the catalogue friction and a gear efficiency of 50 %.  design.py checks that the value below is that mass.
Double pendulum: the same mass and reach split in two, M/2 on L/2 and M/2 on L/2.
"""
import math

G0 = 9.80665                       # standard gravity, m/s^2
RHO = 1.225                        # air density, kg/m^3 (IEC standard air)
R_ROT = 63.0                       # NREL 5-MW rotor radius, m
LAM_STAR = 7.55                    # tip-speed ratio of peak Cp
CP_STAR = 0.482                    # peak power coefficient
WINDS = (6.0, 8.0, 10.0)           # steady winds, m/s
FRACS = (0.3, 0.6, 0.9)            # pivot at these fractions of the rotor radius

M = 0.5                            # bob mass, kg (design.py)
L = 0.1                            # rod length, m


def omega(v):
    """Rotor speed in region 2 at steady wind v, rad/s."""
    return LAM_STAR*v/R_ROT


def rpm(v):
    return omega(v)*60/(2*math.pi)


def turbine_power(v):
    """Mechanical power the rotor takes from the wind at peak Cp, W."""
    return 0.5*RHO*math.pi*R_ROT**2*v**3*CP_STAR


def mountings():
    """The nine mountings: (wind, fraction, Omega, pivot radius)."""
    return [(v, f, omega(v), f*R_ROT) for v in WINDS for f in FRACS]


if __name__ == '__main__':
    import json, os
    out = dict(G0=G0, RHO=RHO, R_ROT=R_ROT, LAM_STAR=LAM_STAR, CP_STAR=CP_STAR, WINDS=WINDS, FRACS=FRACS, M=M, L=L,
               rpm={str(int(v)): rpm(v) for v in WINDS}, power_W={str(int(v)): turbine_power(v) for v in WINDS})
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.json'), 'w'), indent=1)
    print(', '.join(f'{v:.0f} m/s: {rpm(v):.2f} rpm, turbine {turbine_power(v)/1e6:.2f} MW' for v in WINDS))
