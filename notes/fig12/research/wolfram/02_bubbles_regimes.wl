(* 02 Bubbles in the stout: slip velocity, response time, regime numbers. Evaluated 13 Nov 2026 (WolframLanguageEvaluator).
   Bubble of negligible mass, rigid (surfactant-coated) sphere of radius a, Stokes drag, added-mass coefficient 1/2.
   Glass frame: G = g - a_glass (effective gravity vector), A = Du/Dt of the liquid. *)
sol = Solve[0 == rho (4/3 Pi a^3) (A - G) + 6 Pi mu a (u - v), v][[1]];
Print["steady slip v - u = ", Simplify[(v /. sol) - u], "  (A = Du/Dt, G = effective gravity vector)"];
tau = Simplify[(rho/2 (4/3 Pi a^3))/(6 Pi mu a)]; Print["relaxation time of the slip (added mass / drag) = ", tau];
rho = 1007; mu = 2.06*^-3; g = 9.81; H = 0.125;
Do[Module[{U = 2 a^2 rho g/(9 mu), t = rho a^2/(9 mu)},
  Print["a = ", a 10^6, " um: Stokes rise U = ", 1000 U, " mm/s, Re = ", rho U 2 a/mu, ", tau = ", 10^6 t, " us, time to rise 125 mm = ", H/U, " s"]],
 {a, {45*^-6, 50*^-6, 61*^-6}}];
Print["slip speed scales with |g - a_glass|: range factor ", {(9.81 - 10)/9.81, (9.81 + 10)/9.81}];
c = 1480; Print["acoustic transit time H/c = ", 10^6 H/c, " us"];
Print["pressure swing rho a H for a = 10 m/s^2: ", rho 10 H, " Pa = ", rho 10 H/101325 100, " % of 1 atm"];
Print["water hammer rho c dv for dv = 0.1 m/s (glass knocked, sub-0.1 ms stop): ", rho c 0.1/1000, " kPa"];
Do[Print["alpha = ", al, ": rho_m = ", (1 - al) rho, " kg/m3, mu_m(Einstein, rigid spheres) = ", 1000 mu (1 + 5/2 al), " mPa s"], {al, {0.02, 0.05}}];
NN = Sqrt[g 0.02/0.05]; Print["buoyancy frequency N = ", NN, " rad/s vs slosh omega = 21.49 rad/s; N/omega = ", NN/21.49];
Print["Richardson-like ratio alpha g H / U^2 for U = 0.1 m/s, alpha=0.02: ", 0.02 g H/0.1^2];
nu = mu/rho; w = 2 Pi 3.42; R = 0.0391;
Print["Re of slosh (U=0.1 m/s, L=R) = ", 0.1 R/nu, ";  Womersley R sqrt(omega/nu) = ", R Sqrt[w/nu]];
Print["viscous diffusion time R^2/nu = ", R^2/nu, " s"];
