(* Stage A, second route: the numbers of tools/fig12/control/derive.py evaluated again in Wolfram Language.
   Run in any Wolfram kernel; the output of 13 November 2026 is in derive.wl.out.txt. Nothing is simulated. *)
g = 981/100; R = 391/10000; h = 1/8;
xi = x /. FindRoot[D[BesselJ[1, x], x] == 0, {x, #}, WorkingPrecision -> 30] & /@ {18/10, 53/10, 85/10};
om[n_] := Sqrt[g xi[[n]]/R Tanh[xi[[n]] h/R]];
f = N[om /@ {1, 2, 3}/(2 Pi), 8];
(* the push r cos(theta) in J1 modes: c_n from the two integrals, against the closed form *)
cnum = Table[NIntegrate[r^2 BesselJ[1, xi[[n]] r], {r, 0, 1}, WorkingPrecision -> 25]/
    NIntegrate[r BesselJ[1, xi[[n]] r]^2, {r, 0, 1}, WorkingPrecision -> 25], {n, 3}];
cclosed = Table[2/((xi[[n]]^2 - 1) BesselJ[1, xi[[n]]]), {n, 3}];
beta = N[2 xi[[1]] Tanh[xi[[1]] h/R]/(xi[[1]]^2 - 1), 10];
(* plant *)
Mb = 3/2; mw = 3/10; Rw = 1/25; Iw = 24/100000; Ng = 10; Km = 1/50; Jm = 2/10^6; cx = 2; kS = 600; cS = 8; kt = 20000; ct = 5; Imax = 3; Ts = 1/1000;
b = Ng Km/Rw; massX[ml_] := Mb + ml + mw + (Iw + Ng^2 Jm)/Rw^2;
(* symbolic controllability *)
A4s = {{-c/M, 0, 0, 0}, {0, 0, 1, 0}, {be c/M, -w^2, -2 z w, 0}, {-1, 0, 0, 0}}; B4s = {bb/M, 0, -be bb/M, 0};
detC = Factor[Det[Transpose[NestList[A4s . # &, B4s, 3]]]];   (* (B, AB, A^2B, A^3B) by repeated products: MatrixPower of the singular A stays unevaluated at k = 0 *)
Av = {{0, 1, -1, 0}, {-ks/Ms, -cs/Ms, cs/Ms, 0}, {ks/mws, cs/mws, -(cs + cts)/mws, kts/mws}, {0, 0, -1, 0}};
A7 = ArrayFlatten[{{A4s[[1 ;; 3, 1 ;; 3]], 0}, {0, Av}}]; Bu = Join[{0, 0, 0}, {0, 1/Ms, -1/mws, 0}];
C7 = Transpose[NestList[A7 . # &, Bu, 6]];
rankUs = {MatrixRank[C7], Simplify[C7[[1 ;; 3]]] == ConstantArray[0, {3, 7}]};
lqr[wn_, zeta_, Mx_] := Module[{A, B, Q, Rr, K, P},
   A = N[{{-cx/Mx, 0, 0, 0}, {0, 0, 1, 0}, {beta cx/Mx, -wn^2, -2 zeta wn, 0}, {-1, 0, 0, 0}}, 30];
   B = N[{{b/Mx}, {0}, {-beta b/Mx}, {0}}, 30];
   Q = DiagonalMatrix[1/{5/100, 2/1000, 2/1000 wn, 2/100}^2]; Rr = {{1/Imax^2}};
   P = RiccatiSolve[{A, B}, {Q, Rr}]; K = Flatten[Inverse[Rr] . Transpose[B] . P];
   {K, Eigenvalues[A - B . {K}]}];
l1 = lqr[2 Pi 3214/1000, 8/1000, massX[4266/10000]];
l2 = lqr[om[1], 5348992643617189/10^18, massX[4266/10000]];
l3 = lqr[2 Pi 331/100, 18/1000, massX[4296/10000]];
susp[ml_] := Module[{Ms = Mb + ml, A, B, Ca, Da, wa, Q, Nc, Rr, P, K},
   A = N[{{0, 1, -1, 0}, {-kS/Ms, -cS/Ms, cS/Ms, 0}, {kS/mw, cS/mw, -(cS + ct)/mw, kt/mw}, {0, 0, -1, 0}}, 30];
   B = N[{{0}, {1/Ms}, {-1/mw}, {0}}, 30]; Ca = {-kS/Ms, -cS/Ms, cS/Ms, 0}; Da = 1/Ms; wa = 4;
   Q = wa Outer[Times, Ca, Ca] + DiagonalMatrix[{1/(1/100)^2, 0, 0, 1/(2/10000)^2}];
   Nc = Transpose[{wa Ca Da}]; Rr = {{wa Da^2 + 1/40^2}};
   P = RiccatiSolve[{A, B}, {N[Q, 30], N[Rr, 30], N[Nc, 30]}];
   K = Flatten[Inverse[Rr] . (Transpose[B] . P + Transpose[Nc])]; {K, Eigenvalues[A - B . {K}]}];
s1 = susp[4266/10000];
kal[wn_, zeta_, Mx_, every_] := Module[{A, B, G, W, E4, Ad, Bd, GWG, E6, Qd, P, L, Pp, H, Rm, S, Lk, II, sV = 2/1000, sQ = 8/10000, Lp, Pq},
   A = N[{{-cx/Mx, 0, 0}, {0, 0, 1}, {beta cx/Mx, -wn^2, -2 zeta wn}}, 30]; B = N[{b/Mx, 0, -beta b/Mx}, 30];
   G = N[{{1/Mx, 0}, {0, 0}, {-beta/Mx, 1}}, 30]; W = DiagonalMatrix[{1/2, 2/1000}];
   E4 = MatrixExp[Ts ArrayFlatten[{{A, Transpose[{B}]}, {ConstantArray[0, {1, 3}], {{0}}}}]];
   Ad = E4[[1 ;; 3, 1 ;; 3]]; Bd = E4[[1 ;; 3, 4]]; GWG = G . W . Transpose[G];
   E6 = MatrixExp[Ts ArrayFlatten[{{-A, GWG}, {ConstantArray[0, {3, 3}], Transpose[A]}}]];
   Qd = Ad . E6[[1 ;; 3, 4 ;; 6]]; Qd = (Qd + Transpose[Qd])/2;
   P = N[DiagonalMatrix[{sV^2, sQ^2, (sQ wn)^2}], 30];
   Do[Pp = Ad . P . Transpose[Ad] + Qd;
    H = If[Mod[k, every] == every - 1, IdentityMatrix[3][[{1, 2}]], IdentityMatrix[3][[{1}]]];
    Rm = If[Length[H] == 2, DiagonalMatrix[{sV^2, sQ^2}], {{sV^2}}];
    S = H . Pp . Transpose[H] + Rm; Lk = Pp . Transpose[H] . Inverse[S]; II = IdentityMatrix[3] - Lk . H;
    P = II . Pp . Transpose[II] + Lk . Rm . Transpose[Lk]; P = (P + Transpose[P])/2;
    If[Length[H] == 2, Lp = Lk; Pq = P], {k, 0, 5999}];
   {Ad, Bd, Diagonal[Qd], Lp, Sqrt[Pq[[2, 2]]]}];
k1 = kal[2 Pi 3214/1000, 8/1000, massX[4266/10000], 5];
k3 = kal[2 Pi 331/100, 18/1000, massX[4296/10000], 2];
nf[v_] := NumberForm[N[v], 7];
Column[{
  Row[{"zeros of J1': ", nf /@ xi}], Row[{"f11, f12, f13 (Hz): ", f}],
  Row[{"c_n integrals minus closed form: ", N[cnum - cclosed, 3]}], Row[{"shares 2/(xi^2-1): ", nf /@ (2/(xi^2 - 1))}],
  Row[{"beta: ", beta}], Row[{"M_x site, Kaggle: ", N[massX[4266/10000], 6], ", ", N[massX[4296/10000], 6]}],
  Row[{"controllability determinant: ", detC}], Row[{"from u_s: rank, rows (dv, q, q') all zero: ", rankUs}],
  Row[{"LQR 3.214 Hz: K = ", nf /@ l1[[1]], " poles ", nf /@ l1[[2]]}],
  Row[{"LQR live 3.421 Hz: K = ", nf /@ l2[[1]], " poles ", nf /@ l2[[2]]}],
  Row[{"LQR Kaggle 3.31 Hz: K = ", nf /@ l3[[1]], " poles ", nf /@ l3[[2]]}],
  Row[{"suspension: K_s = ", nf /@ s1[[1]], " poles ", nf /@ s1[[2]]}],
  Row[{"Kalman 3.214 Hz, probe every 5: A_d = ", Map[nf, k1[[1]], {2}], " B_d = ", nf /@ k1[[2]], " Q_d diag = ", nf /@ k1[[3]]}],
  Row[{"  gain at a probe sample (rows v, q, q'; columns speed, swing): ", Map[nf, k1[[4]], {2}], " sd q (mm): ", nf[1000 k1[[5]]]}],
  Row[{"Kalman Kaggle 3.31 Hz, probe every 2: gain ", Map[nf, k3[[4]], {2}], " sd q (mm): ", nf[1000 k3[[5]]]}]
  }]
