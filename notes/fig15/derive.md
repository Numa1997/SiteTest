# Fig. 15 — equation checks (SymPy + NumPy)

Wolfram MCP was unavailable this session; these are SymPy/NumPy checks, to be re-run in Wolfram when it is back.
Run: `python3 derive.py`. Griffiths & Steinke (2001) read in full; equation numbers refer to it.

```
  OK  edge matrix = 1/2[[1+k2/k1,1-k2/k1],[1-k2/k1,1+k2/k1]]  (checked numerically)
  OK  single-barrier T = GS Eq. 41 vs the 4 matching equations (both branches), max diff 6.7e-16
  OK    numeric single T(E=1,V0=3,a=1) = 0.0633
  OK    T+R=1 at E=1.0,V0=3.0,a=1.0
  OK    T+R=1 at E=2.0,V0=3.0,a=1.0
  OK    T+R=1 at E=4.0,V0=2.0,a=3.0
  OK  two-barrier composition |t2|^2 = exact double |t|^2 (E=1,s=2.343)
  OK    round-trip geometric series = closed form
  OK    partial sums 0.004,0.015,0.105,0.263,0.558,0.930,0.997
  OK    cell P is unimodular (det=1), N=2
  OK    Cayley-Hamilton P^2 = 2xi P - I  [GS Eq. 26]
  OK    P^2 = P U_(N-1) - I U_(N-2)  [GS Eq. 27]
  OK    N=2: transfer-matrix T_N = direct product (0.132190)
  OK    cell P is unimodular (det=1), N=3
  OK    P^3 = P U_(N-1) - I U_(N-2)  [GS Eq. 27]
  OK    N=3: transfer-matrix T_N = direct product (0.896557)
  OK    cell P is unimodular (det=1), N=5
  OK    P^5 = P U_(N-1) - I U_(N-2)  [GS Eq. 27]
  OK    N=5: transfer-matrix T_N = direct product (0.152672)
  OK    cell P is unimodular (det=1), N=10
  OK    P^10 = P U_(N-1) - I U_(N-2)  [GS Eq. 27]
  OK    N=10: transfer-matrix T_N = direct product (0.096521)
  OK  Breit-Wigner fits T(E) within the FWHM (max dev 0.0178)
  OK    Gamma = 0.0398, tau = 1/Gamma = 25.15 ~ 25.1

24/24 checks passed
```
