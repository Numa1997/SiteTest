(* L4 route 2, Wolfram Language 15.0.1: Golovin's solution via LaplaceTransform, (5.1)/(5.2) for K = b(m+m'), lever rule *)
ClearAll[u, z, p, T, s, nhat, b, m, mp, q, xk, xk1, xs, CC, nuk, nuk1];
dens = (1 - z)/(u Sqrt[z]) BesselI[1, 2 u Sqrt[z]] Exp[-(1 + z) u];
lt = Quiet@FullSimplify[LaplaceTransform[dens, u, p], 0 < z < 1 && p > 2 Sqrt[z]];
Print["LaplaceTransform of printed density: ", lt];
claimed = (1 - z)(s - Sqrt[s^2 - 4 z])/(2 z) /. s -> p + 1 + z;
Print["difference from (1-z)(s-Sqrt[s^2-4z])/(2z), s=p+1+z (numeric, 3 points): ", (lt - claimed) /. {{z -> 0.3, p -> 1.9 - 1.3}, {z -> 0.9, p -> 0.7}, {z -> 0.99, p -> 2.0}}];
Nh = claimed /. z -> 1 - Exp[-T];
Ntot = Limit[Nh, p -> 0, Assumptions -> T > 0];
pde = D[Nh, T] + Nh D[Nh, p] - D[Nh, p] Ntot + Nh;      (* N_T = - N N_p + N_p N(0,T) - N  (units b = L = 1) *)
Print["N(0,T) = ", Simplify[Ntot, T > 0], "; mass -N_p(0,T) = ", Simplify[-D[Nh, p] /. p -> 0, T > 0]];
Print["PDE residual numeric: ", Table[N[pde /. {p -> pv, T -> Tv}, 20], {pv, {0.05, 1, 6}}, {Tv, {0.3, 2.0}}]];
Print["PDE residual symbolic: ", FullSimplify[pde, T > 0 && p > 0]];
Print["initial condition: ", Limit[Nh, T -> 0, Assumptions -> p > 0]];
gain = 1/2 Integrate[b (mp + (m - mp)) Exp[-mp] Exp[-(m - mp)], {mp, 0, m}, Assumptions -> m > 0];
loss = Exp[-m] Integrate[b (m + mp) Exp[-mp], {mp, 0, Infinity}, Assumptions -> m > 0];
dn = Simplify[gain - loss];
Print["dn/dt = ", dn];
Do[Print["phi = ", ph[m], ": LHS = ", Simplify[Integrate[ph[m] dn, {m, 0, Infinity}, Assumptions -> b > 0 && q > 0]], "  RHS(5.2) = ", Simplify[1/2 Integrate[b (m + mp) Exp[-m] Exp[-mp] (ph[m + mp] - ph[m] - ph[mp]), {m, 0, Infinity}, {mp, 0, Infinity}, Assumptions -> b > 0 && q > 0]]], {ph, {Function[x, x], Function[x, 1], Function[x, x^2], Function[x, Exp[-q x]]}}];
Print["lever rule: ", Solve[{nuk + nuk1 == CC, xk nuk + xk1 nuk1 == xs CC}, {nuk, nuk1}] // Simplify];
