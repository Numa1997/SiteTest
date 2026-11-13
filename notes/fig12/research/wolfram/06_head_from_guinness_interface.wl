(* 06 Head rheology from Guinness's own interface. Evaluated 13 Nov 2026 (WolframLanguageEvaluator).
   Law: Voelp & Willenbacher, Soft Matter 17, 3937 (2021), eqs. 8-9 (sources/voelp-willenbacher2021-softmatter17.txt):
   G0 = ad (sigma + 2 Einf)/R32 Phi (Phi - phic), tau_y = kd (sigma + 2 Einf)/R32 (Phi - phic)^2, ad = 1, kd = 0.25, phic = 0.635.
   Guinness, degassed, 20 C, pendant drop: sigma = 44.2 mN/m, Einf = 18.7 mN/m (their Table 2 as quoted by the owner's Gemini search;
   Table 1 listing "Guinness stout beer | Degassed; at 20 C" read by us). R32 = 34 um (wolfram/04). *)
s = 0.0442; Ei = 0.0187; R = 34*^-6; rho = 1007; hf = 0.019; pc = 0.635;
Print["generalized Laplace pressure (s + 2 Einf)/R32 = ", (s + 2 Ei)/R, " Pa  (plain s/R = ", s/R, " Pa)"];
Do[Module[{Phi = 1 - e, G, ty, rf = rho e},
   G = 1 (s + 2 Ei)/R Phi (Phi - pc); ty = 0.25 (s + 2 Ei)/R (Phi - pc)^2;
   Print["e = ", e, ": G0 = ", G, " Pa; tau_y = ", ty, " Pa; Bi(1 m/s2) = ", ty/(rf hf), "; Bi(10 m/s2) = ", ty/(rf 10 hf),
    "; shear-wave crossing time of 19 mm = ", 1000 hf/Sqrt[Max[G, 10^-9]/rf], " ms"]], {e, {0.22, 0.24, 0.27, 0.30, 0.34}}];
