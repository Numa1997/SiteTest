"""Transfer matrices for piecewise-constant potentials (hbar = m = 1). Fig. 15.
A region j has V_j on [x_j, x_{j+1}); psi = A_j e^{i q_j (x - x_j)} + B_j e^{-i q_j (x - x_j)}, q_j = sqrt(2 (E - V_j)) (complex below V_j).
Edges: psi and psi' continuous. Region 0 and the last region are V = 0 (leads), written with the global phase convention
psi = A e^{ikx} + B e^{-ikx} so that t and r are referred to x = 0."""
import numpy as np

def q_of(E, V):
    """Wave number in a flat region; where E = V exactly (q = 0, the two exponentials coincide) the gap is nudged by a
    negligible amount so the edge matrix stays finite, far below the rounding of any stored number."""
    d = np.asarray(E, float) - np.asarray(V, float)
    d = np.where(np.abs(d) < 1e-12, 1e-12, d)
    return np.sqrt(d.astype(complex) * 2)

def edge(q1, q2):
    """(A1, B1) on the left of an edge at local x = 0 from (A2, B2) on its right: [[1,1],[q1,-q1]] c1 = [[1,1],[q2,-q2]] c2."""
    return 0.5 * np.array([[1 + q2 / q1, 1 - q2 / q1], [1 - q2 / q1, 1 + q2 / q1]])

def flight(q, L):
    """Amplitudes at the start of a flat stretch of length L from those at its end."""
    return np.array([[np.exp(-1j * q * L), 0], [0, np.exp(1j * q * L)]])

def layers(segs):
    """segs: list of (x_left, x_right, V) for the non-zero barriers, sorted, not overlapping. Returns region list
    [(x_start, x_end, V)] covering (-inf, inf) with V = 0 between barriers."""
    regs = []; x = -np.inf
    for (l, r, V) in segs:
        if l > x: regs.append((x, l, 0.0))
        regs.append((l, r, V)); x = r
    regs.append((x, np.inf, 0.0))
    return regs

def solve(E, segs):
    """t, r and the amplitudes (A_j, B_j) of every region for incidence e^{ikx} from the left, at energy E > 0."""
    regs = layers(segs); k = np.sqrt(2 * E)
    qs = [q_of(E, V) for (_, _, V) in regs]
    # start in the last region with (A, B) = (1, 0) in local coordinates at its start x_N
    n = len(regs); amps = [None] * n; amps[-1] = np.array([1.0 + 0j, 0j])
    for j in range(n - 2, -1, -1):
        c_right_start = amps[j + 1]
        c_left_end = edge(qs[j], qs[j + 1]) @ c_right_start           # region j at its end x_{j+1}
        L = regs[j][1] - regs[j][0]
        amps[j] = flight(qs[j], L) @ c_left_end if np.isfinite(L) else c_left_end
    # region 0 is written at its end x_1: psi = A0 e^{ik(x - x1)} + B0 e^{-ik(x - x1)} -> global A = A0 e^{-ik x1}
    x1 = regs[0][1]; xN = regs[-1][0]
    A = amps[0][0] * np.exp(-1j * k * x1); B = amps[0][1] * np.exp(1j * k * x1)
    t = np.exp(-1j * k * xN) / A          # last region: 1 * e^{ik(x - xN)} = e^{-ik xN} e^{ikx}, normalised by A
    r = B / A
    scale = 1 / A
    return t, r, regs, qs, [c * scale for c in amps]

def psi_x(E, segs, x):
    """The stationary scattering state at energy E on the points x (incident e^{ikx} with unit amplitude)."""
    t, r, regs, qs, amps = solve(E, segs)
    out = np.zeros_like(x, complex)
    for j, (l, rr, V) in enumerate(regs):
        m = (x >= l) & (x < rr)
        if j == 0:
            xr = rr; out[m] = amps[0][0] * np.exp(1j * qs[0] * (x[m] - xr)) + amps[0][1] * np.exp(-1j * qs[0] * (x[m] - xr))
        else:
            out[m] = amps[j][0] * np.exp(1j * qs[j] * (x[m] - l)) + amps[j][1] * np.exp(-1j * qs[j] * (x[m] - l))
    return out, t, r

def double(V0, d, s):
    """Two barriers of height V0 and width d, centres at -s/2 and +s/2."""
    return [(-s / 2 - d / 2, -s / 2 + d / 2, V0), (s / 2 - d / 2, s / 2 + d / 2, V0)]
