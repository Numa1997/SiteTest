"""Fig. 15, 3D: the exact one-dimensional numbers that check the 3D Kaggle runs (V0 = 2, D = 1, S = 2.5, the geometry of rt3d.py).

For two infinite walls the 3D wave separates, psi = chi(x) g(y) g(z), so the motion along the flight IS the 1D problem: the
transfer-matrix numbers below are then exact for the 3D walls (up to the grid; see notes/fig15/grid_test2.py). For discs and
shells there is no such rule; there these curves are the limit the discs approach as their radius grows.

Writes public/data/resonant-tunnelling/<date>/derived/exact-1d.json:
  T(E) of the pair and of one barrier (plane waves), the packet average Tbar(E) for the stored pulse (sigma0 = 3), the
  resonances (E_r, Gamma from the half-height width, tau = 1/Gamma), the current-voltage curve (Tsu-Esaki, iv.py with V0 = 2)
  and the real-units block (GaAs / AlGaAs).
Usage: python3 exact1d.py <out.json>
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm import solve, double
import iv
from scipy import constants as C

V0, D, S, SIG0 = 2.0, 1.0, 2.5, 3.0
iv.V0 = V0; iv.D = D                                             # iv.py's module constants: the 3D geometry


def T_of(E, segs):
    return abs(solve(E, segs)[0])**2


def tbar(E0, segs, nk=801):
    """The pulse exp(-(x - x0)^2 / (4 sigma0^2) + i k0 x) holds the wave numbers |phi(k)|^2 ~ exp(-(k - k0)^2 / (2 sigma_k^2)),
    sigma_k = 1 / (2 sigma0). Tbar = Int |phi|^2 T(k) dk over k > 0 (negative k carry < 1e-6 of the pulse here)."""
    k0 = np.sqrt(2 * E0); sk = 1 / (2 * SIG0)
    k = np.linspace(max(1e-4, k0 - 7 * sk), k0 + 7 * sk, nk); w = np.exp(-(k - k0)**2 / (2 * sk**2))
    T = np.array([T_of(kk**2 / 2, segs) for kk in k])
    return float(np.trapezoid(w * T, k) / np.trapezoid(w, k))


def resonances(segs, Emax=1.95):
    """The peaks of T(E) below the barrier top, where T is sharp; above it T stays high and no half-height width exists."""
    E = np.linspace(0.02, Emax, 8000); T = np.array([T_of(e, segs) for e in E]); out = []
    for i in range(1, len(E) - 1):
        if T[i] > T[i - 1] and T[i] >= T[i + 1] and T[i] > 0.5:
            from scipy.optimize import minimize_scalar, brentq
            m = minimize_scalar(lambda e: -T_of(e, segs), bracket=(E[i - 1], E[i], E[i + 1])); Er = float(m.x); Tr = T_of(Er, segs)
            f = lambda e: T_of(e, segs) - Tr / 2
            lo = Er - 0.01
            while f(lo) > 0 and lo > 0.011: lo -= 0.01
            hi = Er + 0.01
            while f(hi) > 0 and hi < Emax + 1: hi += 0.01
            if f(lo) > 0 or f(hi) > 0: continue
            El = brentq(f, lo, Er); Eh = brentq(f, Er, hi); G = Eh - El
            out.append(dict(E=Er, T=Tr, Gamma=G, tau=1 / G, El=El, Er=Eh))
    return out


def main(path):
    pair = double(V0, D, S); one = [(-S / 2 - D / 2, -S / 2 + D / 2, V0)]
    E = np.round(np.linspace(0.02, 3.0, 1491), 5)
    Tp = [T_of(e, pair) for e in E]; T1 = [T_of(e, one) for e in E]
    Eb = np.round(np.arange(0.3, 2.1001, 0.025), 4)
    Tbp = [tbar(e, pair) for e in Eb]; Tb1 = [tbar(e, one) for e in Eb]
    res = resonances(pair)
    EF, kT = 1.0, 0.05                                          # the Fermi sea fills to E_F = 1.0 E_u, above the first resonance (0.735)
    Vs, J = iv.iv_curve(S, EF=EF, kT=kT, Vmax=2.5, nV=101)
    pk = vl = None
    for i in range(1, len(J) - 1):
        if pk is None and Vs[i] > 0.05 and J[i] > J[i - 1] and J[i] >= J[i + 1]: pk = i
        if pk is not None and vl is None and i > pk and J[i] < J[i - 1] and J[i] <= J[i + 1]: vl = i
    ivb = dict(EF=EF, kT=kT, V=np.round(Vs, 5).tolist(), J=np.round(J, 8).tolist(), V_peak=float(Vs[pk]), J_peak=float(J[pk]),
               V_valley=float(Vs[vl]) if vl else None, J_valley=float(J[vl]) if vl else None,
               pvr=float(J[pk] / J[vl]) if vl and J[vl] > 0 else None)
    # real units: V0 = 2 E_u is the AlGaAs conduction-band offset, 0.30 eV (Al0.35Ga0.65As; Vurgaftman, Meyer & Ram-Mohan 2001)
    MSTAR = 0.067 * C.m_e; Eu = 0.30 / V0; EuJ = Eu * C.e; a = C.hbar / np.sqrt(MSTAR * EuJ); a_nm = a * 1e9; tu = C.hbar / EuJ
    pref = (C.e * MSTAR * kT * EuJ) / (2 * np.pi**2 * C.hbar**3)
    r0 = res[0]
    rows = [["length unit a", f"{a_nm:.2f} nm"], ["barrier width d", f"{D * a_nm:.2f} nm"], ["well width (s − d)", f"{(S - D) * a_nm:.2f} nm"],
            ["barrier height V₀", f"{V0 * Eu * 1000:.0f} meV"], ["energy unit ħ²/m*a²", f"{Eu * 1000:.0f} meV"],
            ["first resonance", f"{r0['E'] * Eu * 1000:.0f} meV"], ["resonance width Γ", f"{r0['Gamma'] * Eu * 1000:.1f} meV"],
            ["lifetime τ = ħ/Γ", f"{r0['tau'] * tu * 1e15:.0f} fs"], ["peak current J_p", f"{pref * EuJ * ivb['J_peak'] / 1e7:.0f} kA/cm²"],
            ["peak voltage", f"{ivb['V_peak'] * Eu * 1000:.0f} mV"], ["peak-to-valley ratio", f"{ivb['pvr']:.1f}" if ivb['pvr'] else "—"],
            ["effective mass m*", "0.067 mₑ"]]
    ru = dict(rows=rows, Eu_eV=Eu, a_nm=a_nm, t_u_fs=tu * 1e15, T_kelvin=kT * EuJ / C.k,
              note=(f"These follow from one choice: the barrier height V₀ = 2 is the AlGaAs conduction-band offset, about 0.30 eV for "
                    f"Al₀.₃₅Ga₀.₆₅As (Vurgaftman, Meyer & Ram-Mohan, J. Appl. Phys. 89, 5815, 2001). That fixes the energy unit at "
                    f"{Eu * 1000:.0f} meV and, with m* = 0.067 mₑ, the length unit at {a_nm:.2f} nm. The electrons in the emitter fill every state up to the Fermi energy, "
                    f"{EF * Eu * 1000:.0f} meV; T = {kT * EuJ / C.k:.0f} K."))
    out = dict(role="exact check of the 3D runs: one-dimensional transfer matrices for the same barriers (exact for the walls, "
                    "by separation of variables; the limit of large discs)",
               script="tools/kaggle/resonant-tunnelling/exact1d.py", V0=V0, D=D, S=S, sigma0=SIG0,
               T_E=dict(E=E.tolist(), pair=np.round(Tp, 7).tolist(), one=np.round(T1, 7).tolist()),
               Tbar=dict(E=Eb.tolist(), pair=np.round(Tbp, 6).tolist(), one=np.round(Tb1, 6).tolist()),
               resonances=res, iv=ivb, real_units=ru)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), separators=(",", ":"), ensure_ascii=False)
    print("resonances:", [(round(r['E'], 4), round(r['Gamma'], 4), round(r['tau'], 2)) for r in res])
    print("Tbar pair at 0.735:", Tbp[list(Eb).index(0.725)], "...; I-V peak", ivb['V_peak'], ivb['J_peak'], "valley", ivb['V_valley'], "PVR", ivb['pvr'])
    for r in rows: print(r)


if __name__ == "__main__":
    main(sys.argv[1])
