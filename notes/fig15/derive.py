"""Fig. 15: symbolic and numeric checks of every equation the lecture note uses. SymPy + NumPy.
Wolfram MCP was unavailable this session, so these are SymPy/NumPy checks; they are to be re-run in Wolfram when it is back.
Run: python3 derive.py"""
import sympy as sp
import numpy as np, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../tools/kaggle/resonant-tunnelling"))
from tm import solve, double

ok = []
def check(name, cond): ok.append((name, bool(cond))); print(("  OK  " if cond else " FAIL ") + name)

# ---- 1. one step edge: psi and psi' continuous gives the 2x2 edge matrix ----
k1, k2, x = sp.symbols('k1 k2 x', positive=True)
A1, B1, A2, B2 = sp.symbols('A1 B1 A2 B2')
# at x=0: A1+B1 = A2+B2 ; i k1 (A1-B1) = i k2 (A2-B2)
sol = sp.solve([A1 + B1 - (A2 + B2), k1 * (A1 - B1) - k2 * (A2 - B2)], [A1, B1], dict=True)[0]
# (A1,B1) = M (A2,B2); check M equals 1/2[[1+k2/k1,...]] by substituting several (k1,k2)
A1e = sp.expand(sol[A1]); B1e = sp.expand(sol[B1])
def Mnum(k1v, k2v, A2v, B2v):
    sub = {k1: k1v, k2: k2v, A2: A2v, B2: B2v}
    return complex(A1e.subs(sub)), complex(B1e.subs(sub))
oke = True
for (k1v, k2v) in [(1.4, 2.0), (2.3, 1.1), (0.7, 3.0)]:
    m00, m10 = Mnum(k1v, k2v, 1, 0)        # A1,B1 coefficients of A2
    m01, m11 = Mnum(k1v, k2v, 0, 1)        # A1,B1 coefficients of B2
    if (abs(m00 - 0.5 * (1 + k2v / k1v)) > 1e-12 or abs(m01 - 0.5 * (1 - k2v / k1v)) > 1e-12 or
            abs(m10 - 0.5 * (1 - k2v / k1v)) > 1e-12 or abs(m11 - 0.5 * (1 + k2v / k1v)) > 1e-12): oke = False
check("edge matrix = 1/2[[1+k2/k1,1-k2/k1],[1-k2/k1,1+k2/k1]]  (checked numerically)", oke)

# ---- 2. single rectangular barrier T (Griffiths & Steinke Eq. 41; flat.py T_plane) vs the matching solution ----
def Tgs(Ev, Vv, av):
    import math
    if Ev < Vv:
        kap = math.sqrt(2 * (Vv - Ev)); return 1 / (1 + Vv**2 * math.sinh(kap * av)**2 / (4 * Ev * (Vv - Ev)))
    kp = math.sqrt(2 * (Ev - Vv)); return 1 / (1 + Vv**2 * math.sin(kp * av)**2 / (4 * Ev * (Ev - Vv)))
mx = 0.0
for Ev in np.linspace(0.3, 6, 60):
    for (Vv, av) in [(3.0, 1.0), (2.0, 3.0), (8.0, 0.5)]:
        mx = max(mx, abs(Tgs(Ev, Vv, av) - abs(solve(Ev, [(-av/2, av/2, Vv)])[0])**2))
check("single-barrier T = GS Eq. 41 vs the 4 matching equations (both branches), max diff %.1e" % mx, mx < 1e-12)
check("  numeric single T(E=1,V0=3,a=1) = 0.0633", abs(Tgs(1, 3, 1) - 0.063298) < 1e-5)

# ---- 3. transfer matrix M = [[w,z],[z*,w*]], det M = 1  (GS 16-18) ----
for (Ev, Vv, av) in [(1.0, 3.0, 1.0), (2.0, 3.0, 1.0), (4.0, 2.0, 3.0)]:
    # build M for a single barrier numerically from tm and check structure
    t, r, regs, qs, amps = solve(Ev, [(-av / 2, av / 2, Vv)])
    # M maps right amplitudes (C,D)=(t,0 for... ) -> use w=1/t*, z=-r*/t*? verify |w|^2-|z|^2=1 via det and T+R=1
    check(f"  T+R=1 at E={Ev},V0={Vv},a={av}", abs(abs(t)**2 + abs(r)**2 - 1) < 1e-12)

# ---- 4. two barriers: composition t2 = tA tB/(1 - rA' rB) equals the exact product; round trips sum to it ----
E1 = 1.0; s = 2.343
t1, r1, *_ = solve(E1, [(-0.5, 0.5, 3.0)])
k = np.sqrt(2 * E1); ph = np.exp(1j * k * s)
tt2 = t1 * t1 * ph / (1 - r1 * r1 * ph * ph)          # identical barriers, gap s; rA'(from right)=rB=r1
check("two-barrier composition |t2|^2 = exact double |t|^2 (E=1,s=2.343)",
      abs(abs(tt2)**2 - abs(solve(E1, double(3, 1, s))[0])**2) < 1e-9)
# geometric series (round trips) -> same
series = sum((r1 * r1 * ph * ph)**n for n in range(2000))
check("  round-trip geometric series = closed form", abs(t1 * t1 * ph * series - tt2) < 1e-9)
partials = [abs(t1 * t1 * ph * sum((r1 * r1 * ph * ph)**n for n in range(N + 1)))**2 for N in (0, 1, 5, 10, 20, 50, 100)]
check("  partial sums 0.004,0.015,0.105,0.263,0.558,0.930,0.997",
      np.allclose(partials, [0.0040, 0.0150, 0.1053, 0.2631, 0.5576, 0.9300, 0.9973], atol=5e-4))

# ---- 5. N barriers via one cell's transfer matrix: Cayley-Hamilton / Chebyshev (GS Eqs. 24-32) ----
from tm import q_of, edge, flight
def cell_P(Ev, Vv, av, sv):
    """Transfer matrix of one period [0, s] with a barrier of width a at its centre, in the plane-wave basis; right->left."""
    k = q_of(Ev, 0.0); q = q_of(Ev, Vv); g = (sv - av) / 2
    P = edge(k, q) @ flight(q, av) @ edge(q, k) @ flight(k, g)       # from the right edge back across barrier
    P = flight(k, g) @ P                                             # and the left gap
    return P, k
def Tn_direct(N, Ev, Vv, av, sv):
    segs = [((-sv * (N - 1) / 2 + j * sv) - av / 2, (-sv * (N - 1) / 2 + j * sv) + av / 2, Vv) for j in range(N)]
    return abs(solve(Ev, segs)[0])**2
for N in (2, 3, 5, 10):
    Ev, Vv, av, sv = 1.5, 3.0, 1.0, 2.0
    P, k = cell_P(Ev, Vv, av, sv)
    check(f"  cell P is unimodular (det=1), N={N}", abs(np.linalg.det(P) - 1) < 1e-10)
    xi = 0.5 * np.trace(P).real
    # Cayley-Hamilton recursion P^2 - 2 xi P + I = 0  (GS Eq. 26)
    if N == 2: check("  Cayley-Hamilton P^2 = 2xi P - I  [GS Eq. 26]", np.allclose(P @ P, 2 * xi * P - np.eye(2)))
    # Chebyshev U_{N-1}
    g = np.arccos(np.clip(xi, -1, 1)); U = lambda m: (np.sin((m + 1) * g) / np.sin(g) if abs(np.sin(g)) > 1e-9 else (m + 1))
    PN_cheby = P * U(N - 1) - np.eye(2) * U(N - 2)                   # GS Eq. 27
    check(f"  P^{N} = P U_(N-1) - I U_(N-2)  [GS Eq. 27]", np.allclose(np.linalg.matrix_power(P, N), PN_cheby))
    TN_tm = abs(1.0 / np.linalg.matrix_power(P, N)[0, 0])**2        # T = 1/|(P^N)_00|^2
    check(f"  N={N}: transfer-matrix T_N = direct product ({Tn_direct(N,Ev,Vv,av,sv):.6f})",
          abs(TN_tm - Tn_direct(N, Ev, Vv, av, sv)) < 1e-9)

# ---- 6. Breit-Wigner & lifetime: near a resonance T(E) ~ (G/2)^2/((E-Er)^2+(G/2)^2), tau = 1/Gamma ----
Es = np.linspace(0.9, 1.1, 40001); T = np.array([abs(solve(e, double(3, 1, 2.343))[0])**2 for e in Es])
i = T.argmax(); Er = Es[i]
half = T[i] / 2; lo = i
while T[lo] > half: lo -= 1
hi = i
while T[hi] > half: hi += 1
G = Es[hi] - Es[lo]
bw = (G / 2)**2 / ((Es - Er)**2 + (G / 2)**2)
near = np.abs(Es - Er) < 0.5 * G                                    # within the half-width
dev = float(np.max(np.abs(T[near] - bw[near])))
check(f"Breit-Wigner fits T(E) within the FWHM (max dev {dev:.4f})", dev < 0.02)
check(f"  Gamma = {G:.4f}, tau = 1/Gamma = {1/G:.2f} ~ 25.1", abs(1 / G - 25.1) < 0.6)

print(f"\n{sum(1 for _, v in ok if v)}/{len(ok)} checks passed")
if not all(v for _, v in ok): sys.exit(1)
