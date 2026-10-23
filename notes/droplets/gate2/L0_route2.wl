(* L0 route 2, Wolfram Language (run in the Wolfram evaluator; Version 15.0.1) *)
ClearAll[R, r, k, W, rho, E0, t, R0, c, vR, vr, a, n];
vol = Integrate[1, {x, -(R + r), R + r}, {y, -Sqrt[(R + r)^2 - x^2], Sqrt[(R + r)^2 - x^2]}, {z, 0, (vR - vr) dt}, Assumptions -> R > 0 && r > 0 && vR > vr > 0 && dt > 0];
md = 4/3 Pi rho r^3;
dMdt = Simplify[E0 (W/md) vol md/dt];
Print["(1.1) swept-tube mass rate: ", dMdt, "   equal to printed: ", Simplify[dMdt - E0 Pi (R + r)^2 (vR - vr) W] === 0];
rhs12 = Simplify[(dMdt /. {vR -> k R^2, vr -> k r^2})/(4 Pi rho R^2)];
Print["(1.2) minus printed: ", Simplify[rhs12 - E0 k W/(4 rho) (R + r)^3 (R - r)/R^2]];
sol = DSolve[{Rf'[t] == c Rf[t]^2, Rf[0] == R0}, Rf[t], t];
Print["(1.3) DSolve: ", sol, "  match printed: ", FullSimplify[(Rf[t] /. First[sol]) - R0/(1 - c R0 t)] === 0];
Print["(1.3) pole at t = ", Solve[1 - c R0 t == 0, t]];
F[R_] := Log[(R - r)/(R + r)]/(8 r) - (3 R + 2 r)/(4 (R + r)^2);
Print["(1.4) F'(R) - R^2/((R+r)^3 (R-r)) = ", Simplify[D[F[R], R] - R^2/((R + r)^3 (R - r))]];
Print["(1.4) Integrate: ", Simplify[Integrate[R^2/((R + r)^3 (R - r)), R]]];
Print["(1.4) Limit r->0 of F: ", Limit[F[R], r -> 0], "   Limit R->Infinity of F: ", Limit[F[R], R -> Infinity, Assumptions -> R > r > 0]];
Print["(1.4) numeric t(40->100 um), r=8 um, k=1.2296e8, W=0.6434e-3, rho=1000, min: ",
  N[4*1000/(1.2296*^8*0.643398*^-3) (F[100*^-6] - F[40*^-6]) /. r -> 8*^-6, 12]/60]
