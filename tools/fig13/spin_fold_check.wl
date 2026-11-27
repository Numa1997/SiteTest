(* Fig. 13: the spin-and-fold transformation, derived from the Lagrangian and checked symbolically.
   Run in the Wolfram Language. Results (27 November 2026) are quoted in docs/simulations/fig13-momentum-spirographs.md. *)

(* 1. two equal uniform rods, mass m, length l, angles from the downward vertical *)
c1 = (l/2) {Sin[t1[t]], -Cos[t1[t]]};
c2 = l {Sin[t1[t]], -Cos[t1[t]]} + (l/2) {Sin[t2[t]], -Cos[t2[t]]};
Ic = m l^2/12;
Tkin = Simplify[1/2 m D[c1, t].D[c1, t] + 1/2 Ic t1'[t]^2 + 1/2 m D[c2, t].D[c2, t] + 1/2 Ic t2'[t]^2];
V = m g (c1[[2]] + c2[[2]]);
w = {t1'[t], t2'[t]};
Mth = Simplify[D[Tkin, {w, 2}]];                                   (* {{4/3, Cos[t1-t2]/2}, {Cos[t1-t2]/2, 1/3}} for m = l = 1 *)
M0 = Mth /. {t1[t] -> 0, t2[t] -> 0} /. {m -> 1, l -> 1};
G = Inverse[M0]/2;
Kp = Expand[{p1, p2}.G.{p1, p2}];                                  (* 6 p1^2/7 - 18 p1 p2/7 + 24 p2^2/7 *)
Is = Total[M0, 2]; If0 = M0[[1, 1]] + M0[[2, 2]] - 2 M0[[1, 2]]; mu = Det[M0]/Is;   (* 8/3, 2/3, 7/96 *)
om = Inverse[M0].{p1, p2};
X = (p1 + p2)/Sqrt[2 Is]; Y = Sqrt[mu/2] (om[[2]] - om[[1]]);
T = Simplify[D[{X, Y}, {{p1, p2}}]];                               (* {{Sqrt[3]/4, Sqrt[3]/4}, {-5 Sqrt[3/7]/4, 11 Sqrt[3/7]/4}} *)
Print[{"K - X^2 - Y^2", Simplify[Kp - X^2 - Y^2]}];                (* 0 *)
Print[{"det T", Simplify[Det[T]], "T inverse", Simplify[Inverse[T]]}];   (* 3/Sqrt[7]; {{11/(4 Sqrt[3]), -Sqrt[7/3]/4}, {5/(4 Sqrt[3]), Sqrt[7/3]/4}} *)
R = CholeskyDecomposition[G]; Dg = DiagonalMatrix[Diagonal[R]]; S = Simplify[Inverse[Dg].R]; Q = Simplify[T.Inverse[R]];
Print[{"T = Q.D.S", "shear S", S, "stretch D", Dg, "rotation Q", Q, N[ArcTan[Q[[1, 1]], Q[[2, 1]]]/Degree, 8]}];
   (* S = {{1, -3/2}, {0, 1}};  D = diag(Sqrt[6/7], Sqrt[3/2]);  Q = rotation by -62.114433 degrees *)
Print[{"angle between the p1 and p2 axes measured by energy, degrees", N[ArcCos[G[[1, 2]]/Sqrt[G[[1, 1]] G[[2, 2]]]]/Degree, 8]}];   (* 138.59038 *)
Print[{"tilt of the energy ellipses, degrees", N[ArcTan[2 G[[1, 2]]/(G[[1, 1]] - G[[2, 2]])]/2/Degree, 8]}];                        (* 22.5 *)
lash = Solve[Kp == (p1 + p2)^2/(2 If0) /. p2 -> 1, p1];             (* p1 = 19 -+ 4 Sqrt[21] *)
Print[{"streaks, degrees from the spin axis", N[ArcTan[#[[1]], #[[2]]]/Degree, 10] & /@ ((T.{#, 1}) & /@ (p1 /. lash))}];          (* 60, -60 *)
Print[{"d(p1+p2)/dt", Simplify[D[Tkin - V, t1[t]] + D[Tkin - V, t2[t]]] /. {m -> 1, l -> 1}}];   (* -g (3 Sin[t1] + Sin[t2])/2: zero without gravity *)

(* 2. any double pendulum, M = {{A, C}, {C, B}} at the hanging position *)
Clear[M, G, Kp, om, X, Y, Is, If0, mu];
M = {{A, C}, {C, B}}; G = Simplify[Inverse[M]/2]; Kp = {p1, p2}.G.{p1, p2}; om = Inverse[M].{p1, p2};
Is = A + B + 2 C; If0 = A + B - 2 C; mu = (A B - C^2)/Is;
X = (p1 + p2)/Sqrt[2 Is]; Y = Sqrt[mu/2] (om[[2]] - om[[1]]);
Print[{"general K - X^2 - Y^2", Simplify[Kp - X^2 - Y^2, Assumptions -> A > 0 && B > 0 && A B > C^2 && A + B + 2 C > 0]}];   (* 0 *)
Print[{"K minus the completed square with shear C/B", Simplify[Kp - (G[[1, 1]] (p1 - (C/B) p2)^2 + (1/(2 B)) p2^2)]}];            (* 0 *)
Print[{"p1 - (C/B) p2 in speeds", Simplify[(p1 - (C/B) p2) /. Thread[{p1, p2} -> M.{w1, w2}]]}];                                  (* (A - C^2/B) w1 *)
Print[{"streaks: cos^2 of the angle from the spin axis", If0/Is}];                                                               (* (A + B - 2C)/(A + B + 2C) *)

(* 3. what p1 and p2 are: angular momenta, integrated along two uniform rods (m = l = 1) *)
r1[s_] := s {Sin[t1[t]], -Cos[t1[t]]}; r2[s_] := {Sin[t1[t]], -Cos[t1[t]]} + s {Sin[t2[t]], -Cos[t2[t]]};
cross[a_, b_] := a[[1]] b[[2]] - a[[2]] b[[1]];
Ltot = Integrate[cross[r1[s], D[r1[s], t]], {s, 0, 1}] + Integrate[cross[r2[s], D[r2[s], t]], {s, 0, 1}];
Lelbow = Integrate[cross[r2[s] - r2[0], D[r2[s], t]], {s, 0, 1}];
Tk = 1/2 Integrate[D[r1[s], t].D[r1[s], t], {s, 0, 1}] + 1/2 Integrate[D[r2[s], t].D[r2[s], t], {s, 0, 1}];
Print[{"total angular momentum about the pin minus (p1 + p2)", Simplify[Ltot - D[Tk, t1'[t]] - D[Tk, t2'[t]]]}];   (* 0 *)
Print[{"angular momentum of the lower rod about the elbow minus p2", Simplify[Lelbow - D[Tk, t2'[t]]]}];           (* 0 *)
