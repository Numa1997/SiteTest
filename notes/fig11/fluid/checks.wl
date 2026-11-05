(* Project 05, air and water: the Wolfram checks of section 13, as run on 5 November 2026 (one block per kernel call; the kernel is stateless). *)

(* 1. Stokeslet in the Stokes equations (31); bead-chain sum (Lauga & Powers 2009, eqs. 26-31) *)
X = {x, y, z}; r = Sqrt[X . X]; Fv = {F1, F2, F3};
u = (IdentityMatrix[3]/r + Outer[Times, X, X]/r^3) . Fv/(8 Pi mu); p = Fv . X/(4 Pi r^3);
res = Simplify[mu (D[#, {x, 2}] + D[#, {y, 2}] + D[#, {z, 2}]) & /@ u - Grad[p, X]]; div = Simplify[Div[u, X]];
intg = Integrate[1/Abs[s], {s, -L/2, -2 a}, Assumptions -> L > 4 a > 0] + Integrate[1/Abs[s], {s, 2 a, L/2}, Assumptions -> L > 4 a > 0];
{res, div, Simplify[intg], Simplify[{8 Pi mu/intg, 4 Pi mu/intg}]}
(* -> {{0,0,0}, 0, 2 Log[L/(4a)], {xi_perp, xi_par} with ratio 2} *)

(* 2. Generalised forces (35) of (33) on both rods, the power identity (36), upright rods in a breeze *)
q = {x, a, b}; qd = {xd, ad, bd};
r1[s_] := {x + s Sin[a], yh + s Cos[a]}; r2[s_] := {x + L1 Sin[a] + s Sin[b], yh + L1 Cos[a] + s Cos[b]};
vel[r_] := Sum[D[r, q[[i]]] qd[[i]], {i, 3}];
t1 = {Sin[a], Cos[a]}; n1 = {Cos[a], -Sin[a]}; t2 = {Sin[b], Cos[b]}; n2 = {Cos[b], -Sin[b]};
fLin[r_, t_, n_] := Module[{rel = vel[r] - {U, 0}}, -xiPar (rel . t) t - xiPerp (rel . n) n];
Qlin = Simplify[Table[Integrate[fLin[r1[s], t1, n1] . D[r1[s], q[[i]]], {s, 0, L1}] + Integrate[fLin[r2[s], t2, n2] . D[r2[s], q[[i]]], {s, 0, L2}], {i, 3}]];
P1 = Simplify[Integrate[fLin[r1[s], t1, n1] . vel[r1[s]], {s, 0, L1}] + Integrate[fLin[r2[s], t2, n2] . vel[r2[s]], {s, 0, L2}]];
{Simplify[Qlin /. {a -> 0, b -> 0, xd -> 0, ad -> 0, bd -> 0}], Simplify[Qlin . qd - P1]}
(* -> {{(L1 + L2) U xiPerp, L1 (L1 + 2 L2) U xiPerp/2, L2^2 U xiPerp/2}, 0} *)

(* 3. Which flows solve Navier-Stokes exactly (vorticity equation), divergence *)
vel2[psi_] := {D[psi, Y], -D[psi, X]}; vort[v_] := D[v[[2]], X] - D[v[[1]], Y];
nsres[v_] := Simplify[D[vort[v], t] + v . {D[vort[v], X], D[vort[v], Y]} - nu (D[vort[v], {X, 2}] + D[vort[v], {Y, 2}])];
tg = {U Sin[Pi X] Cos[Pi Y] Exp[-2 nu Pi^2 t], -U Cos[Pi X] Sin[Pi Y] Exp[-2 nu Pi^2 t]};
{Simplify[Div[tg, {X, Y}]], nsres[tg], nsres[vel2[U Y^2/4]], nsres[{U/3 X, -U/3 Y}], nsres[vel2[U 2 7/8 (Y/2)^(8/7)]]}
(* -> {0, 0, 0, 0, 39 2^(6/7) nu U/(343 Y^(20/7))}: the river profile is not a Navier-Stokes solution *)

(* 4. The fan (Bickley jet) and the swell *)
alpha = 6^(2/3)/(35/100); nuJ = U 6^(1/3)/(6 alpha^2);
psiB[xp_, yp_] := 6 nuJ alpha xp^(1/3) Tanh[alpha yp/xp^(2/3)]; fb = vel2[psiB[X + 6, Y - 8/10]];
blres = Simplify[fb[[1]] D[fb[[1]], X] + fb[[2]] D[fb[[1]], Y] - nuJ D[fb[[1]], {Y, 2}]];
hw = 67/10; kw = 2 Pi/20; om = Sqrt[981/100 kw Tanh[kw hw]];
wv = {om Cosh[kw Y]/Sinh[kw hw] Cos[kw X - om t], om Sinh[kw Y]/Sinh[kw hw] Sin[kw X - om t]};
{blres, N[fb[[1]] /. {X -> 0, Y -> 8/10, U -> 2}], Simplify[Div[wv, {X, Y}]], Simplify[vort[wv]], N[om]}
(* -> {0, 2., 0, 0, 1.72966} *)

(* 5. The gate: (35) by adaptive NIntegrate at a fixed test state (shown for the fan; the other flows as in README.md) *)
xv = 3/10; av = 4/10; bv = -3/10; xdv = 1/2; adv = 12/10; bdv = -8/10; tt = 17/10; U0 = 2; L1v = 1/2; L2v = 3/4; CH = 12/100;
flow["fan", X_, Y_, t_, nu_] := Module[{al = 6^(2/3)/(35/100), xp = Max[1/2, X + 6], nj, e}, nj = U0 6^(1/3)/(6 al^2); e = al (Y - 6/10)/xp^(2/3);
   {6 nj al^2 xp^(-1/3) Sech[e]^2, 2 nj al xp^(-2/3) (2 e Sech[e]^2 - Tanh[e])}];
frc[fld_, k_, s_, xi_, cq_, nu_] := Module[{th = If[k == 1, av, bv], tv, nv, P, V, F, w, wt, wn, fn, ft, fv},
   tv = {Sin[th], Cos[th]}; nv = {Cos[th], -Sin[th]};
   P = If[k == 1, {xv + s Sin[av], s Cos[av]}, {xv + L1v Sin[av] + s Sin[bv], L1v Cos[av] + s Cos[bv]}];
   V = If[k == 1, {xdv + s Cos[av] adv, -s Sin[av] adv}, {xdv + L1v Cos[av] adv + s Cos[bv] bdv, -L1v Sin[av] adv - s Sin[bv] bdv}];
   F = flow[fld, P[[1]], P[[2]], tt, nu]; w = V - F; wt = w . tv; wn = w . nv; fn = -xi wn - cq Abs[wn] wn; ft = -xi/2 wt; fv = ft tv + fn nv; {fv[[1]], fv[[2]], fn}];
q1[fld_, i_, s_?NumericQ, xi_, cq_, nu_] := Module[{f = frc[fld, 1, s, xi, cq, nu]}, {f[[1]], s f[[3]]}[[i]]];
q2[fld_, i_, s_?NumericQ, xi_, cq_, nu_] := Module[{f = frc[fld, 2, s, xi, cq, nu]}, {f[[1]], L1v (f[[1]] Cos[av] - f[[2]] Sin[av]), s f[[3]]}[[i]]];
cart[fld_, y_?NumericQ, nu_] := flow[fld, xv, -CH y, tt, nu][[1]];
opts = Sequence[WorkingPrecision -> 30, PrecisionGoal -> 13, MaxRecursion -> 40];
Qof[fld_, xi1_, xi2_, cq_, cl_, cc_, nu_] := Module[{Qr, um, wc},
  Qr = {NIntegrate[q1[fld, 1, s, xi1, cq, nu], {s, 0, L1v}, Evaluate[opts]] + NIntegrate[q2[fld, 1, s, xi2, cq, nu], {s, 0, L2v}, Evaluate[opts]],
        NIntegrate[q1[fld, 2, s, xi1, cq, nu], {s, 0, L1v}, Evaluate[opts]] + NIntegrate[q2[fld, 2, s, xi2, cq, nu], {s, 0, L2v}, Evaluate[opts]],
        NIntegrate[q2[fld, 3, s, xi2, cq, nu], {s, 0, L2v}, Evaluate[opts]]};
  um = NIntegrate[cart[fld, y, nu], {y, 0, 1}, Evaluate[opts]]; wc = xdv - um; Qr[[1]] += -cl wc - cc Abs[wc] wc; N[Qr, 15]];
air = SetPrecision[#, 30] & /@ {0.0000594265054278, 0.0000538456274232, 0.014208, 0.0000395212355822, 0.01818624, 0.000015625};
Qof["fan", Sequence @@ air]
(* -> {0.00352356781818455, 0.00213261470063140, 0.00112510608998566} *)

(* 6. Added mass (38): C_a of a cylinder and a sphere from the kinetic energy of potential flow *)
phiC = -U a^2 Cos[t]/r; gC = {D[phiC, r], D[phiC, t]/r};
TC = Simplify[1/2 rho Integrate[(gC . gC) r, {r, a, Infinity}, {t, 0, 2 Pi}, Assumptions -> a > 0 && U > 0]];
phiS = -U a^3 Cos[t]/(2 r^2); gS = {D[phiS, r], D[phiS, t]/r};
TS = Simplify[1/2 rho Integrate[(gS . gS) 2 Pi r^2 Sin[t], {r, a, Infinity}, {t, 0, Pi}, Assumptions -> a > 0 && U > 0]];
{2 TC/U^2/(rho Pi a^2), 2 TS/U^2/(rho 4/3 Pi a^3)}
(* -> {1, 1/2} *)

(* 7. The added-mass matrix, its velocity terms (Lagrange and Christoffel), energy, and the cart's Tuckerman kappa_x *)
q = {x, a, b}; qd = {xd, ad, bd};
v1n[s_] := xd Cos[a] + s ad;  v2n[s_] := xd Cos[b] + L1 Cos[a - b] ad + s bd;
Ta = Simplify[mu1/2 Integrate[v1n[s]^2, {s, 0, L1}] + mu2/2 Integrate[v2n[s]^2, {s, 0, L2}] + mc/2 xd^2];
Ma = Table[D[Ta, qd[[i]], qd[[j]]], {i, 3}, {j, 3}] // Simplify;
dt[f_] := D[f, x] xd + D[f, a] ad + D[f, b] bd;
Ca = Simplify[Table[dt[D[Ta, qd[[i]]]] - D[Ta, q[[i]]], {i, 3}]];
qdd = {xdd, add, bdd}; eq = Ma . qdd + Ca;
dTa = Simplify[dt[Ta] + Total[D[Ta, qd[[#]]] qdd[[#]] & /@ {1, 2, 3}] - (qd . eq)];
Chr = Simplify[Table[Sum[(D[Ma[[i, j]], q[[k]]] - 1/2 D[Ma[[j, k]], q[[i]]]) qd[[j]] qd[[k]], {j, 3}, {k, 3}], {i, 3}]];
{r1, r2, r3} = {18/100, 6/100, 10/100};
kx = NIntegrate[r1 r2 r3/Sqrt[(r1^2 + l)^3 (r2^2 + l) (r3^2 + l)], {l, 0, Infinity}, WorkingPrecision -> 30];
{Ca // InputForm, dTa, Simplify[Ca - Chr], N[kx, 16], N[kx/(2 - kx), 16]}
(* -> Ca as in addedC() of the page, 0, {0,0,0}, 0.2876184832457318, 0.1679640199521062 *)
