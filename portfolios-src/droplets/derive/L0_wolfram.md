# L0: the Wolfram Language check (second route)

Run on 23 October 2026 through the Wolfram connector's evaluator (a stateless Wolfram Language kernel), independently of
`L0_sympy.py`. Input:

```wolfram
m = (4/3) Pi rho R[t]^3;
eq = D[m, t] == e Pi (R[t] + r)^2 k (R[t]^2 - r^2) w;
dRdt = Simplify[Solve[eq, R'[t]][[1, 1, 2]]];
s0 = DSolve[{R'[t] == c R[t]^2, R[0] == R0}, R[t], t];
fin = Integrate[x^2/((x + r)^3 (x - r)), {x, R0, R1}, Assumptions -> R1 > R0 > r > 0];
dep = Integrate[1/(x^2 (Rm^3 - x^3)), x];
{dRdt, s0, Simplify[Limit[fin, r -> 0]], Simplify[D[dep, x] - 1/(x^2 (Rm^3 - x^3))]}
```

Output (the kernel also printed warnings about undefined global symbols and an internal message from the limit, which do not
affect the four results):

```
{-1/4*(e*k*w*(r - R[t])*(r + R[t])^3)/(rho*R[t]^2), {{R[t] -> -(R0/(-1 + c*R0*t))}}, R0^(-1) - R1^(-1), 0}
```

What it confirms:
1. dR/dt = (E k W / 4ρ_w)(R + r)³(R − r)/R², equation (L0.2).
2. R(t) = R₀/(1 − cR₀t) for dR/dt = cR², equation (L0.3).
3. The finite-r time integral tends to 1/R₀ − 1/R₁ as r → 0: (L0.4) reduces to (L0.3).
4. Wolfram's own antiderivative of 1/(R²(R_m³ − R³)) differentiates back to the integrand. This confirms that the integral has an
   elementary closed form; the printed G of (L0.5) itself is checked by SymPy (`L0_sympy.py`) and by the Gate-1 skeptic's Wolfram rerun
   (`notes/droplets/skeptic-G1-L0-r2.md`), not by this item.
