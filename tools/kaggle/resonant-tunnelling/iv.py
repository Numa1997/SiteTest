"""Fig. 15, Step B4 (part): the current-voltage curve of the double-barrier diode, by the Tsu-Esaki formula.

Under a bias V the potential is a staircase: the two barriers sit on a line that drops by eV across the device (emitter at 0,
collector at -eV). We treat the ramp as many flat steps and compose their transfer matrices (tm.py), and check that the answer
stops changing as the steps get finer. The transmission with unequal leads is current-conserving: T = Re(q_R)/q_L * |t|^2.

Tsu & Esaki, Appl. Phys. Lett. 22, 562 (1973): the current per area is
    J(V) = (e m* k_B T) / (2 pi^2 hbar^3) Int_0^inf T(E_x, V) N(E_x, V) dE_x,
    N = ln[(1 + exp((E_F - E_x)/k_B T)) / (1 + exp((E_F - E_x - eV)/k_B T))]   (the supply function),
E_x the energy of motion along the device. Assumptions, stated for the note: coherent transport (one T, no scattering in the
well), no charge build-up (the bias drops linearly), parabolic bands, a thermal Fermi sea in each lead.

In dimensionless units (hbar = m = 1) energies are in E_u = hbar^2/(m a^2); a bias V is in E_u too (eV -> V). The real-units
panel (real_units.py) turns E_u, a and J_u into eV, nm and kA/cm^2. Usage: python3 iv.py SCRATCH/curves.json [--check]
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm import q_of, edge, flight, double

V0, D = 3.0, 1.0


def T_biased(E, s, Vb, nper=100):
    """Transmission at longitudinal energy E through the two barriers on a ramp that drops by Vb across the device (emitter
    V = 0 on the left, collector V = -Vb on the right), U(x) = -Vb (x - xl)/Lwin + V0 inside a barrier. The potential is
    smooth (linear) except at the four barrier faces, so we staircase each of the three pieces (barrier, well, barrier) with
    nper flat cells and keep the faces as exact region edges. Current-conserving T = Re(q_R)/q_L * |t|^2."""
    xl = -s / 2 - D / 2; xr = s / 2 + D / 2; Lwin = xr - xl
    faces = [xl, -s / 2 + D / 2, s / 2 - D / 2, xr]           # b1 right, well right, b2 right
    def Uramp(x): return -Vb * (x - xl) / Lwin
    Vs = [0.0]; Ls = [0.0]
    for p in range(3):                                        # three smooth pieces
        a, b = faces[p], faces[p + 1]; inbar = (p != 1)
        xs = np.linspace(a, b, nper + 1); xc = 0.5 * (xs[:-1] + xs[1:])
        for k in range(nper):
            Vs.append(Uramp(xc[k]) + (V0 if inbar else 0.0)); Ls.append((b - a) / nper)
    Vs.append(-Vb); Ls.append(0.0)
    Vs = np.array(Vs); qs = q_of(E, Vs)
    c = np.array([1.0 + 0j, 0j])
    for j in range(len(Vs) - 2, -1, -1):
        c = edge(qs[j], qs[j + 1]) @ c
        if Ls[j] > 0: c = flight(qs[j], Ls[j]) @ c
    A = c[0]; qL, qR = qs[0], qs[-1]
    if E <= 0 or E + Vb <= 0: return 0.0
    return float((qR.real / qL.real) * abs(1.0 / A)**2)


def T_biased_vec(Es, s, Vb, nper=80):
    """Transmission for an ARRAY of longitudinal energies at one bias, vectorized over energy. Same model as T_biased."""
    Es = np.asarray(Es, float); nE = Es.size
    xl = -s / 2 - D / 2; xr = s / 2 + D / 2; Lwin = xr - xl
    faces = [xl, -s / 2 + D / 2, s / 2 - D / 2, xr]
    def Uramp(x): return -Vb * (x - xl) / Lwin
    Vs = [np.zeros(nE)]; Ls = [0.0]
    for pp in range(3):
        a, b = faces[pp], faces[pp + 1]; inbar = (pp != 1)
        xs = np.linspace(a, b, nper + 1); xc = 0.5 * (xs[:-1] + xs[1:])
        for k in range(nper):
            Vs.append(np.full(nE, Uramp(xc[k]) + (V0 if inbar else 0.0))); Ls.append((b - a) / nper)
    Vs.append(np.full(nE, -Vb)); Ls.append(0.0)
    qs = [q_of(Es, V) for V in Vs]                 # each (nE,) complex
    # propagate c = (2, nE) from the right lead
    c0 = np.ones(nE, complex); c1 = np.zeros(nE, complex)
    for j in range(len(Vs) - 2, -1, -1):
        q1, q2 = qs[j], qs[j + 1]; r = q2 / q1
        n0 = 0.5 * ((1 + r) * c0 + (1 - r) * c1); n1 = 0.5 * ((1 - r) * c0 + (1 + r) * c1)
        c0, c1 = n0, n1
        if Ls[j] > 0:
            c0 = np.exp(-1j * q1 * Ls[j]) * c0; c1 = np.exp(1j * q1 * Ls[j]) * c1
    A = c0; qL, qR = qs[0], qs[-1]
    T = (qR.real / qL.real) * np.abs(1.0 / A)**2
    T[(Es <= 0) | (Es + Vb <= 0)] = 0.0
    return T


def supply(Ex, EF, Vb, kT):
    a = (EF - Ex) / kT; b = (EF - Ex - Vb) / kT
    return np.log1p(np.exp(np.clip(a, -60, 60))) - np.log1p(np.exp(np.clip(b, -60, 60)))


def iv_curve(s, EF=1.4, kT=0.05, Vmax=3.0, nV=91, nE=700, nstep=80):
    Vs = np.linspace(0, Vmax, nV); J = np.empty(nV)
    Ex = np.linspace(1e-4, EF + 8 * kT + 0.5, nE)
    for i, Vb in enumerate(Vs):
        Tt = T_biased_vec(Ex, s, Vb)
        J[i] = np.trapezoid(Tt * supply(Ex, EF, Vb, kT), Ex)
    return Vs, J


if __name__ == "__main__":
    curves_path = sys.argv[1]; check = "--check" in sys.argv
    if check:
        s = 2.343
        for nst in (40, 80, 140, 280):
            print(f"nstep {nst}: T(E=1,V=0.3) = {T_biased(1.0, s, 0.3, nst):.6f}, T(E=0.5,V=0.6) = {T_biased(0.5, s, 0.6, nst):.6f}")
        # zero bias must match the unbiased solver
        from tm import solve
        print("zero-bias staircase vs exact:", T_biased(1.0, s, 0.0, 280), abs(solve(1.0, double(V0, D, s))[0])**2)
        sys.exit()
    cur = json.load(open(curves_path))
    EF, kT = 1.4, 0.05
    out = []
    for g in cur["geometries"]:
        Vs, J = iv_curve(g["s"], EF=EF, kT=kT)
        # peak and valley (first maximum, following minimum)
        dJ = np.diff(J); pk = None; vl = None
        for i in range(1, len(J) - 1):
            if J[i] > J[i - 1] and J[i] >= J[i + 1] and pk is None and Vs[i] > 0.1: pk = i
            if pk is not None and i > pk and J[i] < J[i - 1] and J[i] <= J[i + 1] and vl is None: vl = i
        g["iv"] = dict(EF=EF, kT=kT, V=np.round(Vs, 5).tolist(), J=np.round(J, 8).tolist(),
                       V_peak=(float(Vs[pk]) if pk else None), J_peak=(float(J[pk]) if pk else None),
                       V_valley=(float(Vs[vl]) if vl else None), J_valley=(float(J[vl]) if vl else None),
                       pvr=(float(J[pk] / J[vl]) if pk and vl and J[vl] > 0 else None))
        print(f"s={g['s']}: peak V={g['iv']['V_peak']} J={g['iv']['J_peak']}, valley V={g['iv']['V_valley']} J={g['iv']['J_valley']}, PVR={g['iv']['pvr']}")
    json.dump(cur, open(curves_path, "w"), separators=(",", ":"))
    print("iv curves written into", curves_path)
