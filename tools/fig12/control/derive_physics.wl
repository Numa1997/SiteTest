(* Stage A, physics and loop: the four blocks run in the Wolfram connector on 13 November 2026 (output: derive_physics.out.txt).
   Each block is self-contained (the cloud kernel keeps nothing between calls). *)

(* ---- Block 1: the sloshing mode from the Lagrangian ---- *)
Clear[a, q, t]; $Assumptions = {R > 0, h > 0, xi > 0, rho > 0, g > 0, r >= 0, z >= 0};
k = xi/R; J1x = BesselJ[1, xi];
phi[r_, th_, z_] := a[t] BesselJ[1, k r] Cos[th] Cosh[k z]/Cosh[k h];
eta[r_, th_] := q[t] BesselJ[1, k r]/J1x Cos[th];
aSol = Solve[D[eta[r, th], t] == (D[phi[r, th, z], z] /. z -> h), a[t]][[1, 1]] // Simplify;
use = BesselJ[0, xi] -> BesselJ[1, xi]/xi;
I2 = Simplify[(Integrate[r BesselJ[1, k r]^2, {r, 0, R}] /. use)];
I3 = Simplify[(Integrate[r^2 BesselJ[1, k r], {r, 0, R}] /. use) /. BesselJ[2, xi] -> 2 BesselJ[1, xi]/xi - BesselJ[0, xi] /. use];
T = Simplify[rho/2 Pi (a[t]^2 k Tanh[k h]) I2 /. aSol];
V = Simplify[rho/2 (g + az) Pi q[t]^2 I2/J1x^2 + rho ax Pi q[t] I3/J1x];
Px = Simplify[rho Pi R Integrate[a[t] BesselJ[1, xi] Cosh[k z]/Cosh[k h], {z, 0, h}] /. aSol];
L = T - V; eq = Simplify[D[D[L, q'[t]], t] - D[L, q[t]] == 0]; sol = Solve[eq, q''[t]][[1, 1, 2]] // Simplify;
mn = Simplify[2 Coefficient[T, q'[t]^2]]; omega2 = Simplify[-Coefficient[sol /. {ax -> 0, az -> 0}, q[t]]]; beta = Simplify[-Coefficient[sol, ax]];
{mn, omega2, Simplify[-Coefficient[sol /. ax -> 0, q[t]]/omega2], beta, Simplify[Px/q'[t]], Simplify[rho Pi I3/J1x],
 Simplify[beta - 2 xi Tanh[xi h/R]/(xi^2 - 1)], Simplify[Px/q'[t] - rho Pi R^3/xi^2], Simplify[rho Pi I3/J1x - Px/q'[t]]}

(* ---- Block 2: cart and mode as one Lagrangian; the push back the controller's model leaves out ---- *)
Lg = 1/2 Mx x'[t]^2 + Pc x'[t] q'[t] + 1/2 mn q'[t]^2 - 1/2 mn w^2 q[t]^2;
Qx = bb i[t] - cx x'[t]; Qq = -2 z w mn q'[t];
s = Solve[{D[D[Lg, x'[t]], t] - D[Lg, x[t]] == Qx, D[D[Lg, q'[t]], t] - D[Lg, q[t]] == Qq}, {x''[t], q''[t]}][[1]] // Simplify;
{x''[t] /. s, Simplify[(q''[t] /. s) - (-w^2 q[t] - 2 z w q'[t] - (Pc/mn) (x''[t] /. s))]}
(* numbers: see the session's call; Afull and Asite as in Block 3 below with and without Pc *)

(* ---- Block 3: the motor loop as one sampled system; margins ---- *)
Ts = 1/1000; tauI = 2/1000; xi1 = x0 /. FindRoot[D[BesselJ[1, x0], x0] == 0, {x0, 1.84}, WorkingPrecision -> 20];
rho = 1007; R = 0.0391; h = 0.125; Pc = rho Pi R^3/xi1^2; mn = Pi R^3 rho (xi1^2 - 1) Coth[h xi1/R]/(2 xi1^3); be = Pc/mn;
Mx = 3/2 + 0.4296 + 3/10 + (24/100000 + 100 2/10^6)/(1/25)^2; b = 5; cx = 2; w = 2 Pi 3.31; z = 0.018; Meff = Mx - Pc be;
Ac = N[{{-cx/Meff, Pc w^2/Meff, 2 z w Pc/Meff, b/Meff}, {0, 0, 1, 0}, {be cx/Meff, -w^2 - be Pc w^2/Meff, -2 z w (1 + be Pc/Meff), -be b/Meff}, {0, 0, 0, -1/tauI}}];
Bc = N[{0, 0, 0, 1/tauI}];
E5 = MatrixExp[Ts ArrayFlatten[{{Ac, Transpose[{Bc}]}, {ConstantArray[0, {1, 4}], {{0}}}}]]; Phi = E5[[1 ;; 4, 1 ;; 4]]; Gam = E5[[1 ;; 4, 5]];
Am = N[{{-cx/Mx, 0, 0, 0}, {0, 0, 1, 0}, {be cx/Mx, -w^2, -2 z w, 0}, {-1, 0, 0, 0}}]; Bm = N[{{b/Mx}, {0}, {-be b/Mx}, {0}}];
K = Flatten[9 Transpose[Bm] . RiccatiSolve[{Am, Bm}, {DiagonalMatrix[1/{0.05, 0.002, 0.002 w, 0.02}^2], {{1/9}}}]];
A3 = Am[[1 ;; 3, 1 ;; 3]]; B3 = Flatten[Bm[[1 ;; 3]]]; G = N[{{1/Mx, 0}, {0, 0}, {-be/Mx, 1}}]; W = DiagonalMatrix[{0.5, 0.002}];
E4 = MatrixExp[Ts ArrayFlatten[{{A3, Transpose[{B3}]}, {ConstantArray[0, {1, 3}], {{0}}}}]]; Ad = E4[[1 ;; 3, 1 ;; 3]]; Bd = E4[[1 ;; 3, 4]];
E6 = MatrixExp[Ts ArrayFlatten[{{-A3, G . W . Transpose[G]}, {ConstantArray[0, {3, 3}], Transpose[A3]}}]]; Qd = Ad . E6[[1 ;; 3, 4 ;; 6]]; Qd = (Qd + Transpose[Qd])/2;
sV = 0.002; sQ = 0.0008; P = DiagonalMatrix[{sV^2, sQ^2, (sQ w)^2}];
Do[Pp = Ad . P . Transpose[Ad] + Qd; H = If[OddQ[k], IdentityMatrix[3][[{1, 2}]], IdentityMatrix[3][[{1}]]];
  Rm = If[Length[H] == 2, DiagonalMatrix[{sV^2, sQ^2}], {{sV^2}}]; S = H . Pp . Transpose[H] + Rm; Lk = Pp . Transpose[H] . Inverse[S];
  II = IdentityMatrix[3] - Lk . H; P = II . Pp . Transpose[II] + Lk . Rm . Transpose[Lk]; P = (P + Transpose[P])/2;
  If[Length[H] == 2, Lp = Lk; Hp = H, L1 = Lk; H1 = H], {k, 0, 3999}];
Y = Array[y, 8];
step[L_, H_] := Module[{zpost, icmd}, zpost = (IdentityMatrix[3] - L . H) . (Ad . Y[[6 ;; 8]] + Bd Y[[4]]) + L . H . Y[[1 ;; 3]];
   icmd = -K . Join[zpost, {Y[[5]]}]; D[Join[Phi . Y[[1 ;; 4]] + Gam icmd, {Y[[5]] - Ts Y[[1]]}, zpost], {Y}]];
ev = Eigenvalues[step[Lp, Hp] . step[L1, H1]];
Aol = Module[{zpost}, zpost = (IdentityMatrix[3] - Lp . Hp) . (Ad . Y[[6 ;; 8]] + Bd Y[[4]]) + Lp . Hp . Y[[1 ;; 3]];
   {D[Join[Phi . Y[[1 ;; 4]], {Y[[5]] - Ts Y[[1]]}, zpost], {Y}], D[-K . Join[zpost, {Y[[5]]}], {Y}]}];
Bol = Join[Gam, {0}, {0, 0, 0}];
Lz[om_] := -(Aol[[2]] . Inverse[Exp[I om Ts] IdentityMatrix[8] - Aol[[1]]] . Bol);
{Max[Abs[ev]], SortBy[Log[ev]/(2 Ts), Re], Lz /@ {254.}, Abs[Lz[945.]]}

(* ---- Block 4: Mathieu threshold; symplectic Euler of the cart ---- *)
w = 2 Pi 3.31;
mono[eps_?NumericQ, zeta_?NumericQ, Om_?NumericQ] := Module[{T = 2 Pi/Om, s},
   s = NDSolveValue[{q''[t] + 2 zeta w q'[t] + w^2 (1 + eps Cos[Om t]) q[t] == 0, q[0] == #[[1]], q'[0] == #[[2]]}, {q[T], q'[T]}, {t, 0, T},
       PrecisionGoal -> 12, AccuracyGoal -> 14, MaxSteps -> 10^6] & /@ {{1, 0}, {0, 1}};
   Max[Abs[Eigenvalues[Transpose[s]]]]];
thr[zeta_] := eps /. FindRoot[mono[eps, zeta, 2 w] == 1, {eps, 4 zeta, 3 zeta, 5 zeta}];
Ms = 1.5 + 0.4296; mw = 0.3; k = 600; c = 8; kt = 20000; ct = 5; hh = 10^-4;
Mm = DiagonalMatrix[{Ms, mw}]; Kk = {{k, -k}, {-k, k + kt}}; Cc = {{c, -c}, {-c, c + ct}};
Acont = ArrayFlatten[{{0, IdentityMatrix[2]}, {-Inverse[Mm] . Kk, -Inverse[Mm] . Cc}}];
Fv = IdentityMatrix[2] - hh Inverse[Mm] . Cc; Fx = -hh Inverse[Mm] . Kk;
SE = ArrayFlatten[{{IdentityMatrix[2] + hh Fx, hh Fv}, {Fx, Fv}}];
{thr /@ {0.0053, 0.018, 0.025}, SortBy[Eigenvalues[N[Acont]], Im], SortBy[Log[Eigenvalues[N[SE]]]/hh, Im]}
