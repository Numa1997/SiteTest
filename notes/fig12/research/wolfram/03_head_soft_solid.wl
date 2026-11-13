(* 03 The head as a soft solid: modulus, yield stress, regime numbers for the cart, wall friction, floating-layer estimate.
   Evaluated 13 Nov 2026 (WolframLanguageEvaluator). Output in 03_head_soft_solid.out.txt.
   Formulas as quoted in Costa 2012 (thesis, sources/costa2012-thesis.txt, citing Hoehler & Cohen-Addad 2005):
   G0 = 1.4 (gam/R) Phi (Phi - Phic), tauy = ay (gam/R) (Phi - Phic)^2, Phic = 0.64, ay in [0.5, 1]; Phi = gas fraction = 1 - phil.
   Wall friction: Cantat 2013 (sources/cantat2013-pof25.txt), f = xi gam Ca^(2/3) per unit length of Plateau border, xi = 6.82 (sliding). *)
gam = 0.045; rhol = 1007; phic = 0.64; hf = 0.019; g = 9.81; mu = 2.06*^-3;
G0[R_, phl_] := 1.4 gam/R (1 - phl) ((1 - phl) - phic);
ty[R_, phl_, ay_] := ay gam/R ((1 - phl) - phic)^2;
rows = Flatten[Table[With[{rf = rhol phl, G = G0[R, phl], t1 = ty[R, phl, 0.5], t2 = ty[R, phl, 1.0]},
     {R 10^6, phl, rf, Round[G, 0.1], {Round[t1, 0.1], Round[t2, 0.1]},
      Round[{t1, t2}/(rf 10 hf), 0.01], Round[{t1, t2}/(rf 1 hf), 0.1], Round[{t1, t2}/(rf g hf), 0.01],
      Round[1000 {t1, t2}/(rf 10), 0.1], Round[1000 hf/Sqrt[G/rf], 0.1]}],
    {R, {50*^-6, 100*^-6}}, {phl, {0.05, 0.1, 0.2, 0.3}}], 1];
Print[TableForm[rows, TableHeadings -> {None, {"R um", "phi_l", "rho_f", "G0 Pa", "tau_y Pa (ay .5,1)", "Bi at 10 m/s2", "Bi at 1 m/s2", "Bi own weight", "lump L*=tau_y/(rho_f 10) mm", "shear-wave crossing h/c ms"}}]];
Print["stout drop scale sqrt(gam/(rho 10)) = ", 1000 Sqrt[gam/(rhol 10)], " mm"];
Do[With[{Ca = mu V/gam}, Print["V = ", V, " m/s: Ca = ", Ca, ", f = ", 6.82 gam Ca^(2/3), " N/m, wall stress ~ f/R (R=50um) = ", 6.82 gam Ca^(2/3)/50*^-6, " Pa, (R=100um) = ", 6.82 gam Ca^(2/3)/100*^-6, " Pa"]], {V, {0.001, 0.01, 0.05, 0.1, 0.3}}];
k = 47.0891;
Do[Module[{m = rhol phl hf, E = 3 G0[R, phl], Dm}, Dm = E hf^3/(12 (1 - 0.25));
   Print["R=", R 10^6, " phi_l=", phl, ": m k/rho = ", m k/rhol, ", D k^4/(rho g) = ", Dm k^4/(rhol g), ", f/f0 (plate-on-fluid estimate) = ", Sqrt[(1 + Dm k^4/(rhol g))/(1 + m k/rhol Tanh[k 0.125])]]],
  {R, {50*^-6, 100*^-6}}, {phl, {0.1, 0.2, 0.3}}];
(* 03b Viola et al. 2016 oscillator integrated directly, X in metres, their fitted w0, sigma, R *)
w0 = 22.0; sig = 9.8*^-3; Rv = 0.03705;
Do[Module[{sol, env, tst},
   sol = NDSolveValue[{x''[t] + w0^2 x[t] == -2 sig w0 x'[t] - al w0^(4/3) Rv^(1/3) Sign[x'[t]] Abs[x'[t]]^(2/3), x[0] == 0.005, x'[0] == 0}, x, {t, 0, 30}, MaxStepSize -> 0.002, Method -> "StiffnessSwitching"];
   env = Table[{t, Max[Abs[sol[#]] & /@ Range[t, t + 0.3, 0.005]]}, {t, 0, 29, 0.5}];
   tst = SelectFirst[env, #[[2]] < 0.05*^-3 &];
   Print["alpha = ", al, ": amplitude below 0.05 mm after ", tst[[1]], " s; amplitude at 2 s, 4 s: ", 1000 {env[[5, 2]], env[[9, 2]]}, " mm"]],
 {al, {0, 0.010, 0.030}}];
