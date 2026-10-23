(* L7 route 2, Wolfram Language 15.0.1 *)
ClearAll[al, A, C, K0, gam, x, y];
F[K0_] := al A (1 - Exp[-(C K0/(al A))^gam]);
Print["hard hit: ", Limit[1 - Exp[-y], y -> Infinity], "; K0->0: ", Limit[1 - Exp[-y], y -> 0], "; series of 1-Exp[-y]: ", Series[1 - Exp[-y], {y, 0, 3}]];
Print["dF/dK0: ", Simplify[D[F[K0], K0], Assumptions -> {al > 0, A > 0, C > 0, K0 > 0, 0 < gam < 1}]];
Print["local exponent dlnF/dlnK0: ", Simplify[D[Log[F[K0]], K0] K0, Assumptions -> {al > 0, A > 0, C > 0, K0 > 0, 0 < gam < 1}], "   -> at small x: ", Limit[Simplify[D[Log[F[K0]], K0] K0 /. K0 -> x al A/C, Assumptions -> {al > 0, A > 0, C > 0, x > 0}], x -> 0, Assumptions -> {0 < gam < 1}]];
rho = 900.; m1 = 4/3 Pi (40*^-6)^3 rho; m2 = 4/3 Pi (8*^-6)^3 rho;
k0 = 1/2 m1 m2/(m1 + m2) (0.1726 - 0.0076)^2;
T = 263.15; a0 = 3.78*^4 (1 + 0.0079/(5*^-4)^1.5); Aval = a0/3 + Max[2 a0/3 - a0 Abs[T - 258]/9, 0];
alv = Pi (16*^-6)^2; aA = alv Aval; Cv = 6.3*^6;
Print["K0 = ", k0, " J ; alpha A = ", aA, " ; C K0 = ", Cv k0, " ; F = ", aA (1 - Exp[-(Cv k0/aA)^0.3]), " ; 1/F = ", 1/(aA (1 - Exp[-(Cv k0/aA)^0.3]))];
Print["old rule fragments: ", 0.001 m1/(4/3 Pi (5*^-6)^3 rho)];
Print["thesis liquid fraction at -10 C: ", Sum[{98.9, 4.291, -0.318, -0.02623, -6.398*^-4, -5.279*^-6}[[j + 1]] (-10.)^j, {j, 0, 5}], " %"]
