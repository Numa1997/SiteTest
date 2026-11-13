(* 04 Verification by the session "Guinness cart page rebuild", 13 Nov 2026 (WolframLanguageEvaluator; stateless, three separate calls).
   (a) wall damping of mode (1,1), Bongarzone & Gallaire 2022 eq. 17 in SI, for the pint. *)
jj = x /. FindRoot[D[BesselJ[1, x], x] == 0, {x, 1.84}];
gg = 9.81; RR = 0.0391; HH = 0.125/RR; nuS = 2.06*^-3/1007;
Rey = Sqrt[gg RR^3]/nuS; ww = Sqrt[jj Tanh[jj HH]]; toSI = Sqrt[gg/RR];
side = Sqrt[ww/(2 Rey)] (1/2 (1 + 1/jj^2)/(1 - 1/jj^2) - jj HH/Sinh[2 jj HH]);
bulk = 2 jj^2/Rey; bottom = Sqrt[ww/(2 Rey)] jj/Sinh[2 jj HH];
surfc = Sqrt[ww/(2 Rey)] jj Cosh[jj HH]^2/Sinh[2 jj HH];
Print["omega = ", ww toSI, " rad/s, f = ", ww toSI/(2 Pi), " Hz, Re = ", Rey];
Print["decay rates 1/s: side ", side toSI, ", bulk ", bulk toSI, ", bottom ", bottom toSI, ", inextensible surface ", surfc toSI];
Print["zeta: side ", side/ww, ", side+bulk ", (side + bulk)/ww, ", side+bulk+inextensible surface ", (side + bulk + surfc)/ww];

(* (b) falsification test: Cantat 2013's wall friction law predicts Viola et al. 2016's measured alpha (nothing fitted to Viola).
   Mode (1,1): eta = X J1(kr)/J1(kR) cos(theta); K = rho g pi Int (J1(kr)/J1(kR))^2 r dr; M = K/w0^2; wall stress C|v|^(2/3);
   generalised force C h R |X'|^(2/3) Int|cos|^(5/3); Viola's form alpha w0^(4/3) R^(1/3) |X'|^(2/3). *)
j = x /. FindRoot[D[BesselJ[1, x], x] == 0, {x, 1.84}];
Ith = NIntegrate[Abs[Cos[t]]^(5/3), {t, 0, 2 Pi}];
alphaPred[R_, rho_, mu_, gam_, rb_, xi_, Z_, h_] := Module[{k = j/R, g = 9.81, w0, K, M, C},
  w0 = Sqrt[g k]; K = rho g Pi NIntegrate[(BesselJ[1, k r]/BesselJ[1, k R])^2 r, {r, 0, R}];
  M = K/w0^2; C = Z (gam/rb) xi (mu/gam)^(2/3); C h R Ith/(M w0^(4/3) R^(1/3))];
princenZ[phi_] := 2/Pi Sqrt[1 - 3.2/((1 - phi)/phi + 7.7)^0.5];
Do[Print["h = ", h 1000, " mm: alpha predicted with Z_theo ", alphaPred[0.03705, 1000, 1.0*^-3, 0.0315, 0.125*^-3, 4.94, princenZ[0.25], h],
   ", with Z_fit 0.18 ", alphaPred[0.03705, 1000, 1.0*^-3, 0.0315, 0.125*^-3, 4.94, 0.18, h]], {h, {0.0025, 0.0033, 0.004, 0.005, 0.0065}}];
Print["Viola measured: 0.010, 0.013, 0.016, 0.023, 0.030"];

(* (c) the same law for the Guinness head in the pint (stiff surfaces: xi = 6.82 and 0.94 (l/r_m) Ca^(1/3); Cantat's fits of Z and
   l/r_m against liquid fraction; sliding speed decays upward over ell = 1/k (Sauret 2015)). *)
Ith53 = NIntegrate[Abs[Cos[t]]^(5/3), {t, 0, 2 Pi}]; Ith43 = NIntegrate[Abs[Cos[t]]^(4/3), {t, 0, 2 Pi}];
rho = 1007; mu = 2.06*^-3; gam = 0.045; g = 9.81; k = jj/RR; w0 = Sqrt[g k]; ell = 1/k; hf = 0.019;
K = rho g Pi NIntegrate[(BesselJ[1, k r]/BesselJ[1, k RR])^2 r, {r, 0, RR}]; M = K/w0^2;
h23 = 3 ell/5 (1 - Exp[-5 hf/(3 ell)]); h13 = 3 ell/4 (1 - Exp[-4 hf/(3 ell)]);
tab = {{0.10, 0.6, 0.5}, {0.15, 0.44, 0.25}, {0.20, 0.32, 0.09}, {0.25, 0.18, 0.004}};
Do[Module[{phi = row[[1]], Z = row[[2]], lr = row[[3]], a23, a13},
   a23 = Z (gam/rb) 6.82 (mu/gam)^(2/3) h23 RR Ith53/M; a13 = Z (gam/rb) 0.94 lr (mu/gam)^(1/3) h13 RR Ith43/M;
   Print["phi_l = ", phi, ", R = ", rb 10^6, " um: Viola-form alpha = ", a23/(w0^(4/3) RR^(1/3)), "; Ca^(1/3) coefficient = ", a13]],
  {rb, {25*^-6, 50*^-6, 100*^-6}}, {row, tab}];
