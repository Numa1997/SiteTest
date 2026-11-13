(* 04 Head bubble size, settling check, gas balance of the head, lacing film, meniscus height vs contact angle.
   Evaluated 13 Nov 2026 (WolframLanguageEvaluator). Output in 04_head_bubbles_settling_lacing.out.txt.
   Inputs: Watamura et al. 2019 SI Fig. S2 read off the rendered page (half-maximum near 47 and 82 um, mode near 62 um,
   mean 61 um from the text); Benilov 2012 settling ~120 s; Landau-Levich-Derjaguin prefactor 0.946 (rigid factor 4^(2/3)). *)
rho = 1007; mu = 2.06*^-3; g = 9.81; gam = 0.045;
sig[d1_, d2_] := Log[d2/d1]/(2 Sqrt[2 Log[2]]);
s0 = sig[47., 82.]; Print["log-normal sigma from FWHM = ", s0];
Do[Module[{m = 61 Exp[-s^2/2]}, Print["sigma=", s, ": median=", m, " um, D32 (Sauter) = ", m Exp[5 s^2/2], " um, R32 = ", m Exp[5 s^2/2]/2, " um"]], {s, {0.19, s0, 0.29}}];
U[D_, al_, n_] := (rho g D^2/(18 mu)) (1 - al)^n;
Do[Print["D = ", D 10^6, " um: U = ", 1000 U[D, 0, 0], " mm/s; t(125 mm) free = ", 0.125/U[D, 0, 0], " s; hindered (alpha 0.08, n 5) = ", 0.125/U[D, 0.08, 5], " s"], {D, {54*^-6, 61*^-6, 68*^-6, 94*^-6, 122*^-6}}];
Print["measured settling (Benilov 2012 p.2): about 120 s"];
Do[Print["alpha0 = ", a0, ": head thickness for Phi = 0.64/0.75 with H_l = 106 mm: ", 1000 a0 0.106/0.64, " / ", 1000 a0 0.106/0.75, " mm"], {a0, {0.02, 0.08, 0.10, 0.15}}];
lc = Sqrt[gam/(rho g)]; Print["capillary length = ", 1000 lc, " mm"];
Do[With[{Ca = mu V/gam}, Print["V = ", V, " m/s: Ca = ", Ca, "; h_LLD (mobile, 0.946 lc Ca^(2/3)) = ", 10^6 0.946 lc Ca^(2/3), " um; rigid (x 4^(2/3)) = ", 10^6 4^(2/3) 0.946 lc Ca^(2/3), " um"]], {V, {0.001, 0.005, 0.02, 0.1}}];
Do[Print["theta = ", th, " deg: meniscus height = ", 1000 lc Sqrt[2 (1 - Sin[th Degree])], " mm"], {th, {0, 20, 30, 40, 50, 60}}];
