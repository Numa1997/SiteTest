(* L6 route 2, Wolfram Language 15.0.1 *)
ClearAll[nu, eps, R, d, g, a0, A2, tK, aa, bb];
Print["Solve exponents (nu^aa eps^bb has dimension of time): ", Solve[{2 aa + 2 bb == 0, -aa - 3 bb == 1}, {aa, bb}]];
vk = (nu eps)^(1/4); tk = Sqrt[nu/eps];
sig2 = R^2 eps/(15 nu) + d^2 a0 (vk/tk)^2 + A2 2 eps/(15 nu);
ratio = Sqrt[2/Pi] Sqrt[sig2 + Pi/8 d^2 g^2]/(d g/2);
assum = {nu > 0, d > 0, g > 0, R > 0, A2 > 0, a0 > 0};
Print["limit eps->0: ", Limit[ratio, eps -> 0, Direction -> "FromAbove", Assumptions -> assum]];
Print["(ratio-1)/eps at eps->0: ", Simplify[Limit[(ratio - 1)/eps, eps -> 0, Direction -> "FromAbove", Assumptions -> assum]]];
exact[b_?NumericQ] := (1/2) NIntegrate[Sqrt[2/Pi] (Exp[-(b mu)^2] + Sqrt[Pi] (b mu) Erf[b mu]), {mu, -1, 1}, WorkingPrecision -> 20, PrecisionGoal -> 10];
apx[b_] := Sqrt[2/Pi] Sqrt[1 + Pi/8 (b Sqrt[2])^2];
Print["max over b in {0.05,0.2,0.5,1,1.27,2,4,10,30}: ", Max[Table[Abs[apx[bb]/exact[bb] - 1], {bb, {0.05, 0.2, 0.5, 1, 1.27, 2, 4, 10, 30}}]], "   at b=1.27: ", apx[1.27]/exact[1.27] - 1];
Print["tau_K at nu=1.6935e-5, eps=1e-2: ", Sqrt[1.6935*^-5/1*^-2], " s"]
