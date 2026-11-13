(* 01 Slosh mode (1,1), Stokes layer, wall damping. Upright cylinder approximating the tulip glass at the fill
   (radius 39.1 mm at the fill, depth 125 mm). Evaluated 13 Nov 2026 with the WolframLanguageEvaluator connector;
   output in 01_slosh_stokes_layer.out.txt. Stateless: self-contained. *)
(* (a) Stokes layer over a wall that slips past the inviscid flow with amplitude U: time-averaged dissipation per area *)
u[y_, t_] := U Exp[-y/d] Cos[w t - y/d];
diss = Simplify[mu/(2 Pi/w) Integrate[Integrate[D[u[y, t], y]^2, {y, 0, Infinity}, Assumptions -> d > 0], {t, 0, 2 Pi/w}], Assumptions -> {d > 0, w > 0}];
dissNu = Simplify[diss /. {d -> Sqrt[2 nu/w], mu -> rho nu}, Assumptions -> {nu > 0, w > 0, rho > 0}];
Print["Stokes-layer dissipation per area: ", diss, "  =  ", dissNu];
(* (b) mode (1,1): first root of J1' *)
j11 = N[x /. FindRoot[D[BesselJ[1, x], x] == 0, {x, 1.84}], 10];
g = 9.81; R = 0.0391; h = 0.125; nu = 2.06*^-3/1007; rho = 1007;
k = j11/R; w = Sqrt[g k Tanh[k h]];
Print["j11' root = ", j11, ", k = ", k, " 1/m, f11 = ", w/(2 Pi), " Hz, tanh(kh) = ", Tanh[k h]];
d = Sqrt[2 nu/w]; Print["Stokes layer delta = sqrt(2 nu/omega) = ", 1000 d, " mm"];
phi[r_, th_, z_] := BesselJ[1, k r] Cos[th] Cosh[k (z + h)]/Cosh[k h];
gr = {D[phi[r, th, z], r], D[phi[r, th, z], th]/r, D[phi[r, th, z], z]};
Ekin = rho/2 NIntegrate[(gr . gr) r, {r, 0, R}, {th, 0, 2 Pi}, {z, -h, 0}];   (* = total energy E, per unit A^2 *)
side = NIntegrate[((gr[[2]]^2 + gr[[3]]^2) /. r -> R) R, {th, 0, 2 Pi}, {z, -h, 0}];
bot = NIntegrate[((gr[[1]]^2 + gr[[2]]^2) /. z -> -h) r, {r, 0, R}, {th, 0, 2 Pi}];
D0 = rho/2 Sqrt[nu w/2];
gammaSide = D0 side/(2 Ekin); gammaBot = D0 bot/(2 Ekin);   (* amplitude decay rate = dissipation/(2E) *)
Print["decay rate of amplitude (1/s): side wall ", gammaSide, ", bottom ", gammaBot, ", total ", gammaSide + gammaBot];
Print["damping ratio zeta = gamma/omega = ", (gammaSide + gammaBot)/w];
top = NIntegrate[((gr[[1]]^2 + gr[[2]]^2) /. z -> 0) r, {r, 0, R}, {th, 0, 2 Pi}];
gammaTop = D0 top/(2 Ekin);
Print["extra decay with an inextensible surface (no-slip lid): ", gammaTop, " 1/s, zeta_top = ", gammaTop/w];
Print["coefficient C in zeta_wall = C sqrt(nu/(R^(3/2) g^(1/2))): ", (gammaSide + gammaBot)/w Sqrt[R^1.5 g^0.5/nu]];
