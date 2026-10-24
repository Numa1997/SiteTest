"""The setup of the study, defined once; every script imports it.

The machine: a second blade hinged at the tip of a wind-turbine blade, turning in the rotor plane, braked at its hinge.
Turbine: NREL 5-MW reference (Jonkman et al. 2009, NREL/TP-500-38060): rotor radius 63 m (Table 1-1), hub radius 1.5 m, peak
power coefficient 0.482 at tip-speed ratio 7.55 (Table 7-2); dossier-turbine.md. In region 2 the controller holds the rotor at
that tip-speed ratio, so a steady wind v gives Omega = 7.55 v / 63 m. Three steady winds, 6, 8 and 10 m/s, span region 2 (6 m/s
gives 6.9 rpm, the cut-in rotor speed; 10 m/s gives 11.4 rpm, below the rated 12.1 rpm).
The second blade: a thin uniform rod, length L_B and mass M_B, hinged at the tip, r_p = 63 m. L_B = 1 m is a modelling choice;
M_B is sized in design.py: the mass of the 1-2-5 series at which the maxon RE 25 + GP 32 C takes the largest share of the best
power P*, averaged over the three winds. design.py checks that M_B below is that mass.
Air on the second blade is left out (stated on the page); at the tip the hinge moves at 45 to 76 m/s (7.55 v).
"""
import math

G0 = 9.80665                       # standard gravity, m/s^2
RHO = 1.225                        # air density, kg/m^3 (IEC standard air)
R_ROT = 63.0                       # NREL 5-MW rotor radius, m: the hinge sits here
R_HUB = 1.5                        # hub radius, m
LAM_STAR = 7.55                    # tip-speed ratio of peak Cp
CP_STAR = 0.482                    # peak power coefficient
WINDS = (6.0, 8.0, 10.0)           # steady winds, m/s

L_B = 1.0                          # second blade's length, m (modelling choice)
M_B = 1.0                          # second blade's mass, kg (design.py)
I_B = M_B*L_B**2/3                 # its inertia about the hinge, kg m^2
MLC = M_B*L_B/2                    # its first moment about the hinge, kg m


def omega(v):
    """Rotor speed in region 2 at steady wind v, rad/s."""
    return LAM_STAR*v/R_ROT


def rpm(v):
    return omega(v)*60/(2*math.pi)


def turbine_power(v):
    """Mechanical power the rotor takes from the wind at peak Cp, W."""
    return 0.5*RHO*math.pi*R_ROT**2*v**3*CP_STAR


def mountings():
    """The three runs: (wind, Omega, hinge radius)."""
    return [(v, omega(v), R_ROT) for v in WINDS]


def pstar(Om, m=None, l=None, rp=R_ROT):
    """Best small-swing power of the second blade at its best brake, W: (m l/2)^2 g^2 / [4 Om ((m l/2) r_p - I)]."""
    m = M_B if m is None else m; l = L_B if l is None else l
    mlc, I = m*l/2, m*l*l/3
    return mlc**2*G0**2/(4*Om*abs(mlc*rp - I))


if __name__ == '__main__':
    import json, os
    out = dict(G0=G0, RHO=RHO, R_ROT=R_ROT, R_HUB=R_HUB, LAM_STAR=LAM_STAR, CP_STAR=CP_STAR, WINDS=WINDS, M_B=M_B, L_B=L_B,
               I_B=I_B, MLC=MLC, rpm={str(int(v)): rpm(v) for v in WINDS}, omega={str(int(v)): omega(v) for v in WINDS},
               v_tip={str(int(v)): omega(v)*R_ROT for v in WINDS}, power_W={str(int(v)): turbine_power(v) for v in WINDS},
               Pstar_W={str(int(v)): pstar(omega(v)) for v in WINDS})
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.json'), 'w'), indent=1)
    for v in WINDS:
        print(f'{v:.0f} m/s: {rpm(v):.3f} rpm, hinge at {omega(v)*R_ROT:.1f} m/s, turbine {turbine_power(v)/1e6:.2f} MW, P* {pstar(omega(v))*1e3:.2f} mW')
