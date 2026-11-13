"""Turn the dimensionless numbers (hbar = m = 1) into real units for a GaAs / AlGaAs resonant-tunnelling diode, and write a
'real_units' block into curves.json for the page's panel.

Anchor: the barrier height V0 = 3 (dimensionless) is the AlGaAs conduction-band offset. For Al_x Ga_{1-x} As with x about 0.35
the offset is near 0.30 eV (65 % of the direct band-gap difference; Vurgaftman, Meyer & Ram-Mohan, J. Appl. Phys. 89, 5815
(2001), Table and the 0.6-0.7 rule). So E_u = hbar^2/(m* a^2) = 0.30/3 = 0.10 eV fixes the length unit a; the effective mass is
m* = 0.067 m_e (GaAs, same review).

Tsu-Esaki prefactor for the current density: J = (e m* k_B T)/(2 pi^2 hbar^3) Int T N dE. In units E_u the stored J (iv.py) is
the integral Int T N d(E/E_u); the physical current is J_phys = (e m* k_B T)/(2 pi^2 hbar^3) * E_u * J_stored.
Usage: python3 real_units.py curves.json
"""
import json, sys
import numpy as np
from scipy import constants as C

ME = C.m_e; HBAR = C.hbar; E = C.e; EV = C.e
MSTAR = 0.067 * ME
V0_DIM = 3.0
OFFSET_EV = 0.30                                     # AlGaAs conduction-band offset at x ~ 0.35
Eu = OFFSET_EV / V0_DIM                               # energy unit, eV
Eu_J = Eu * EV
a = HBAR / np.sqrt(2 * MSTAR * Eu_J)                 # since E_u = hbar^2/(m* a^2) -> a = hbar/sqrt(m* E_u) ... check below
# E_u = hbar^2/(m* a^2)  =>  a = hbar / sqrt(m* E_u_J)
a = HBAR / np.sqrt(MSTAR * Eu_J)
a_nm = a * 1e9
t_u = HBAR / Eu_J                                     # time unit, s
kT_dim = 0.05                                         # the Fermi temperature used in iv.py (0.05 E_u)
T_kelvin = kT_dim * Eu_J / C.k

cur = json.load(open(sys.argv[1]))
d = cur["d"]; V0 = cur["V0"]
g0 = cur["geometries"][0]                             # the resonant pair
res = g0["resonances"][0]
iv = g0["iv"]
# current density prefactor
pref = (E * MSTAR * (kT_dim * Eu_J)) / (2 * np.pi**2 * HBAR**3)     # A/m^2 per unit of (J_stored * E_u) ... see note
Jphys_peak = pref * Eu_J * iv["J_peak"]               # A/m^2
Jphys_valley = pref * Eu_J * iv["J_valley"]
to_kAcm2 = 1.0 / 1e7                                  # 1 kA/cm^2 = 1e7 A/m^2

rows = [
    ["length unit a", f"{a_nm:.2f} nm"],
    ["barrier width d", f"{d * a_nm:.2f} nm"],
    ["well width (s − d)", f"{(g0['s'] - d) * a_nm:.2f} nm"],
    ["barrier height V₀", f"{V0 * Eu * 1000:.0f} meV"],
    ["energy unit ħ²/m*a²", f"{Eu * 1000:.1f} meV"],
    ["first resonance", f"{res['E'] * Eu * 1000:.0f} meV"],
    ["resonance width Γ", f"{res['Gamma'] * Eu * 1000:.1f} meV"],
    ["lifetime τ = ħ/Γ", f"{res['tau'] * t_u * 1e15:.0f} fs"],
    ["peak current J_p", f"{Jphys_peak * to_kAcm2:.1f} kA/cm²"],
    ["peak voltage", f"{iv['V_peak'] * Eu * 1000:.0f} mV"],
    ["peak-to-valley ratio", f"{iv['pvr']:.1f}"],
    ["effective mass m*", "0.067 mₑ"],
]
cur["real_units"] = dict(
    rows=rows, Eu_eV=Eu, a_nm=a_nm, t_u_fs=t_u * 1e15, T_kelvin=T_kelvin,
    note="These follow from one choice: the barrier height V₀ = 3 is the AlGaAs conduction-band offset, about "
         "0.30 eV for Al₀.₃₅Ga₀.₆₅As (Vurgaftman, Meyer &amp; Ram-Mohan, J. Appl. Phys. 89, 5815, 2001). "
         "That fixes the energy unit at " + f"{Eu*1000:.0f}" + " meV and, with m* = 0.067 mₑ, the length unit at "
         + f"{a_nm:.2f}" + " nm. The Fermi sea is at " + f"{1.4*Eu*1000:.0f}" + " meV and T = "
         + f"{T_kelvin:.0f}" + " K.")
json.dump(cur, open(sys.argv[1], "w"), separators=(",", ":"))
print("a =", round(a_nm, 3), "nm; E_u =", round(Eu * 1000, 1), "meV; t_u =", round(t_u * 1e15, 2), "fs; T =", round(T_kelvin), "K")
print("barrier", round(d * a_nm, 2), "nm; well", round((g0['s'] - d) * a_nm, 2), "nm; resonance", round(res['E'] * Eu * 1000), "meV; Gamma", round(res['Gamma'] * Eu * 1000, 1), "meV; tau", round(res['tau'] * t_u * 1e15), "fs")
print("J_peak", round(Jphys_peak * to_kAcm2, 2), "kA/cm^2; V_peak", round(iv['V_peak'] * Eu * 1000), "mV; PVR", round(iv['pvr'], 1))
