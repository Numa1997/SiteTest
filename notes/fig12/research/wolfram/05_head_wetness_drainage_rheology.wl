(* 05 Liquid fraction of the head (equilibrium profile), how fast it drains, and its stiffness, yield stress and effective viscosity.
   Evaluated 13 Nov 2026 (WolframLanguageEvaluator, three calls; the first used the protected symbol Pi and failed for the profile,
   so the profile and diffusivity were re-run with Posm). Output in 05_head_wetness_drainage_rheology.out.txt.
   Inputs (files in sources/):
   R32 = 34 um (wolfram/04, from Watamura 2019 SI Fig. S2; Watamura & Sugiyama 2024 give 59 +- 15 um diameter); gamma = 0.045 N/m;
   rho = 1007; mu = 2.06e-3.
   Osmotic pressure (forel2016-softmatter12.txt, quoting Maestro 2013 / Hoehler 2008): Pi = K (gam/R)(ec - e)^2/Sqrt[e], e = liquid fraction,
     K = 3.2, ec = 0.36 (disordered polydisperse) or K = 7.3, ec = 0.26 (ordered monodisperse). Column equilibrium dPi/dz = rho g (1 - e).
   Permeability, rigid protein interfaces: k = R^2 e^2/300 (boulogne2023-langmuir-si.txt: kappa Kp = 0.16 x 0.02; koehler2000-langmuir16.txt).
   Modulus G0 = a (gam/R) Phi (Phi - 0.64), a = 1.4 (saintjalmes-durian1999: 0.51/0.365) to 1.64 (mason1995: 0.6/0.365).
   Yield tau_y = 0.51 (gam/R)(Phi - 0.62)^2 (mason1996-jcis179 p.443). Flow above yield: tcholakova2008-pre78 (films + menisci). *)
gam = 0.045; rho = 1007; mu = 2.06*^-3; g = 9.81; R = 34*^-6; hf = 0.019;
Posm[e_, K_, ec_] := K gam/R (ec - e)^2/Sqrt[e];
dPosm[e_, K_, ec_] := K gam/R (-2 (ec - e)/Sqrt[e] - (ec - e)^2/(2 e^1.5));
prof[K_, ec_] := Module[{tab, inv}, tab = Table[{NIntegrate[-dPosm[x, K, ec]/(rho g (1 - x)), {x, e, ec}], e}, {e, Subdivide[0.02, ec - 10^-6, 400]}];
   inv = Interpolation[Reverse[tab], InterpolationOrder -> 1]; Table[{zz 1000, inv[zz]}, {zz, {0.001, 0.002, 0.005, 0.010, 0.015, 0.019}}]];
Print["K=3.2, ec=0.36 (disordered): {height mm, liquid fraction} = ", prof[3.2, 0.36]];
Print["K=7.3, ec=0.26 (ordered):    {height mm, liquid fraction} = ", prof[7.3, 0.26]];
Do[With[{k = R^2 e^2/300, dP = Abs[dPosm[e, 3.2, 0.36]]},
   Print["e = ", e, ": gravity drainage speed = ", 10^6 k rho g/mu, " um/s (H/v = ", hf/(k rho g/mu)/60, " min); capillary diffusivity = ", k dP/mu, " m^2/s (H^2/D = ", hf^2/(k dP/mu)/60, " min)"]], {e, {0.25, 0.30, 0.34}}];
Print["Ronteltap N2 beer foam (R ~ 100 um) drains in 633-757 s; scaled by (100/34)^2 = ", (100/34.)^2, " -> ", 633 (100/34.)^2/60, "-", 757 (100/34.)^2/60, " min"];
Do[Module[{Phi = 1 - e, rf = rho e, G14, G16, ty, tauf, etaeff},
   G14 = 1.4 gam/R Phi (Phi - 0.64); G16 = 1.64 gam/R Phi (Phi - 0.64); ty = If[Phi > 0.62, 0.51 gam/R (Phi - 0.62)^2, 0];
   Print["e = ", e, " (Phi ", Phi, "), rho_f = ", rf, ": G0 = ", Max[G14, 0], "-", Max[G16, 0], " Pa; tau_y = ", ty, " Pa; Bi(1 m/s2) = ", ty/(rf 1 hf), "; Bi(10 m/s2) = ", ty/(rf 10 hf)];
   Do[With[{Ca = mu gd R/gam}, tauf = gam/R (0.7 Ca^0.47 Phi^(5/6)/(1 - Phi)^0.5 + 8 Ca^0.7 Phi^(5/6)/(1 - Phi)^0.15); etaeff = (ty + tauf)/gd;
      Print["   shear rate ", gd, " 1/s: viscous stress ", tauf, " Pa; effective viscosity = ", etaeff, " Pa s = ", etaeff/mu, " x stout; wave damping time 1/(2 nu k^2), k = 47/m: ", 1/(2 (etaeff/rf) 47.09^2), " s"]], {gd, {1, 10, 30}}];
   Print["   viscous-capillary breakup time of a 10 mm lump, eta L/gamma = ", ((ty + gam/R (0.7 (mu 10 R/gam)^0.47 Phi^(5/6)/(1 - Phi)^0.5))/10) 0.01/gam, " s"]],
 {e, {0.22, 0.27, 0.30, 0.34}}];
