(* L1 route 2, Wolfram Language. Cartesian/cylindrical route: stream function -> Cartesian velocity -> Stokes equations -> traction integral *)
ClearAll[x, y, z, rho, a, U, mu, s, th, ph];
rr[x_, y_, z_] := Sqrt[x^2 + y^2 + z^2];
psi = (1/2) U (rho^2/(rho^2 + z^2)) ((rho^2 + z^2) - (3/2) a Sqrt[rho^2 + z^2] + a^3/(2 Sqrt[rho^2 + z^2]));   (* printed (2.1) with sin^2 = rho^2/r^2 *)
uz0 = D[psi, rho]/rho; urho0 = -D[psi, z]/rho;      (* u_z = (1/rho) dpsi/drho, u_rho = -(1/rho) dpsi/dz  (axisymmetric Stokes stream function) *)
sub = {rho -> Sqrt[x^2 + y^2]};
ux = Simplify[(urho0 x/rho) /. sub, Assumptions -> a > 0]; uy = Simplify[(urho0 y/rho) /. sub, Assumptions -> a > 0]; uz = Simplify[uz0 /. sub, Assumptions -> a > 0];
u = {ux, uy, uz};
R = rr[x, y, z];
utext = U {0, 0, 1} - 3 a U/4 ({0, 0, 1}/R + z {x, y, z}/R^3) - a^3 U/4 ({0, 0, 1}/R^3 - 3 z {x, y, z}/R^5);   (* textbook Cartesian Stokes-flow field *)
Print["velocity from (2.1) minus textbook Cartesian form (random point): ", Simplify[(u - utext) /. {x -> 0.7, y -> -1.3, z -> 2.1, a -> 1.1, U -> 0.9}]];
p = -(3/2) mu U a z/R^3;                                  (* printed p - p_inf, since cos(theta)/r^2 = z/r^3 *)
Print["div u = ", FullSimplify[Div[u, {x, y, z}] /. {a -> 1.1, U -> 0.9}]];
resid = Grad[p, {x, y, z}] - mu (Laplacian[#, {x, y, z}] & /@ u);
Print["Stokes residual grad p - mu lap u at 3 points: ", (resid /. {x -> 0.7, y -> -1.3, z -> 2.1, a -> 1.1, U -> 0.9, mu -> 0.8}), (resid /. {x -> -1.2, y -> 0.4, z -> -0.9, a -> 1.1, U -> 0.9, mu -> 0.8}), (resid /. {x -> 3.1, y -> 0.2, z -> 0.5, a -> 1.1, U -> 0.9, mu -> 0.8})];
Print["Symbolic residual: ", FullSimplify[resid, Assumptions -> a > 0 && mu > 0]];
(* no slip *)
Print["u on the sphere r = a (symbolic): ", FullSimplify[(u /. {x -> a Sin[th] Cos[ph], y -> a Sin[th] Sin[ph], z -> a Cos[th]}), Assumptions -> a > 0 && 0 < th < Pi]];
(* traction and force *)
grad = Transpose[Grad[#, {x, y, z}] & /@ u];   (* grad[[i,j]] = d u_i / d x_j *)
sig = -p IdentityMatrix[3] + mu (grad + Transpose[grad]);
force[s_] := Module[{pt = {x -> s Sin[th] Cos[ph], y -> s Sin[th] Sin[ph], z -> s Cos[th]}, nrm},
  nrm = {Sin[th] Cos[ph], Sin[th] Sin[ph], Cos[th]};
  Integrate[Simplify[(sig /. pt) . nrm s^2 Sin[th]], {th, 0, Pi}, {ph, 0, 2 Pi}, Assumptions -> s > 0 && a > 0 && mu > 0]];
Print["Force on r = a (symbolic):       ", Simplify[force[a], Assumptions -> a > 0 && mu > 0]];
Print["Force through r = 2a (symbolic):  ", Simplify[force[2 a], Assumptions -> a > 0 && mu > 0]];
(* pressure and shear parts on r = a *)
nrm = {Sin[th] Cos[ph], Sin[th] Sin[ph], Cos[th]};
pt = {x -> a Sin[th] Cos[ph], y -> a Sin[th] Sin[ph], z -> a Cos[th]};
Fp = Integrate[Simplify[(-p /. pt) Cos[th] a^2 Sin[th]], {th, 0, Pi}, {ph, 0, 2 Pi}, Assumptions -> a > 0];
Fs = Integrate[Simplify[((mu (grad + Transpose[grad]) /. pt) . nrm)[[3]] a^2 Sin[th]], {th, 0, Pi}, {ph, 0, 2 Pi}, Assumptions -> a > 0 && mu > 0];
Print["pressure part F_p = ", Simplify[Fp, Assumptions -> mu > 0], "   viscous part F_v = ", Simplify[Fs, Assumptions -> mu > 0]];
(* (2.3), (2.4), (2.5) *)
Print["(2.3) Solve: ", Solve[6 Pi mu a v == 4/3 Pi a^3 (rw - ra) g, v]];
Print["(2.5) C_D Re^2 from (2.4): ", Simplify[(Solve[4/3 Pi a^3 (rw - ra) g == 1/2 ra v^2 Pi a^2 CD, CD][[1, 1, 2]]) (ra v 2 a/mu)^2]];
Re0 = ra v d/mu;
Print["(2.5) Stokes: C_D = 24/Re -> v = ", Simplify[Solve[(24/Re0) Re0^2 == 4 ra (rw - ra) g d^3/(3 mu^2), v][[1, 1, 2]] /. d -> 2 a, Assumptions -> a > 0 && mu > 0 && ra > 0], "   difference from (2.3): ", Simplify[(Solve[(24/Re0) Re0^2 == 4 ra (rw - ra) g d^3/(3 mu^2), v][[1, 1, 2]] /. d -> 2 a) - 2 (rw - ra) g a^2/(9 mu)]]
Print["Buckingham null space of dimension matrix for (F,a,v,rho_a,mu): ", NullSpace[{{1, 0, 0, 1, 1}, {1, 1, 1, -3, -1}, {-2, 0, -1, 0, -1}}]]
