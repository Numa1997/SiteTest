(* L2 route 2, Wolfram Language 15.0.1 *)
ClearAll[St, kappa, eta, s, p, b, eta0];
roots = kappa /. Solve[St kappa^2 + kappa + 3 == 0, kappa];
Print["roots: ", roots, "   printed form difference: ", Simplify[roots - {(-1 - Sqrt[1 - 12 St])/(2 St), (-1 + Sqrt[1 - 12 St])/(2 St)}]];
Print["discriminant zero at St = ", Solve[Discriminant[St kappa^2 + kappa + 3, kappa] == 0, St]];
sol[Stv_] := DSolve[{Stv eta''[s] + eta'[s] + 3 eta[s] == 0, eta[0] == 1, eta'[0] == -3}, eta[s], s][[1, 1, 2]];   (* slaved start *)
Do[Print["St = ", stv, ": eta(s) = ", N[sol[stv], 6], " ; first zero: ", Quiet[Check[s /. FindRoot[sol[stv], {s, 2}], "none found"]], "; min over (0,60) of eta = ", NMinimize[{sol[stv], 0 <= s <= 60}, s][[1]]], {stv, {0.05, 0.08, 1/12., 0.09, 0.2}}];
(* nonlinear potential-flow axis equation in log variables xi = Log[eta], u = eta'/eta; event u < -1000 = the partner reaches the surface *)
axisEnd[stv_] := Module[{c, sl},
  c[xi_] := If[Exp[xi] > 10^-6, -(1 - (1 + Exp[xi])^-3)/Exp[xi], -3 + 6 Exp[xi]];
  sl = NDSolve[{xi'[t] == u[t], u'[t] == (c[xi[t]] - u[t])/stv - u[t]^2, xi[0] == Log[29.], u[0] == -(1 - 30.^-3)/29.,
    WhenEvent[u[t] < -1000, "StopIntegration"]}, {xi, u}, {t, 0, 400}, Method -> "StiffnessSwitching", AccuracyGoal -> 12, PrecisionGoal -> 10, MaxSteps -> 10^7];
  sl[[1, 1, 2, 0, 1, 1, 2]]];   (* upper end of the solution's domain (failed on this version when printed: read the InterpolatingFunction domain instead) *)
