# Droplet Collection notes: independent check of derivation steps and method boxes

Checked 2026-11-11 against `portfolios-src/droplets/text/*.src.html` and `physics.cjs`. Air `P.air(283.15, 85000)`.
Tools: SymPy re-derivation (scratch script `s1.py`), Node runs of `physics.cjs` (`n1.cjs` to `n4.cjs`), stored `data/ripening.json`, `data/etab_warm.json`.
Verdicts: CORRECT, or WRONG with the quoted text, the fault and the fix. Minor points that are not errors are listed separately.

## 1. book-10, sections 10.2 and 10.4

| item | verdict | notes |
|---|---|---|
| (10.4) derivation: air gains u_s abs(dA)/T, surface takes -(dsigma/dT) abs(dA), sum = sigma abs(dA)/T | CORRECT | Sign bookkeeping is right: the destroyed surface entropy enters as +(dsigma/dT)abs(dA), and u_s + T dsigma/dT = sigma. Units J/K. Limit: sigma = 0 gives dS = 0. |
| u_s = 0.115 J/m^2, 1.56 sigma; 8.0e-11 J; 7.1e-5 K; 1.32e10 k_B | CORRECT | sigma = 0.074221, dsigma/dT = -1.456e-4 J/(m^2 K) (IAPWS in code) give u_s = 0.11545, ratio 1.555; heat 8.05e-11 J; dT = 7.10e-5 K (c_w = 4192); dS/k_B = 1.324e10. |
| (10.5) mu_i = dF_s/dm_i = 2 sigma/(rho_w r_i) = R_v T a/r_i, a = 1.14 nm | CORRECT | SymPy: d(sigma 4 pi r^2)/dm = 2 sigma/(rho_w r). a = 1.1360 nm (`kelvinA`). Units J/kg. Limit r to infinity gives mu = 0. |
| mu(8 um) = 18.6 J/kg, mu(40 um) = 3.7 J/kg, heights 1.89 m, 0.38 m | CORRECT | 18.555, 3.711 J/kg; 1.891 m, 0.378 m. |
| Vapour potential mu_bar = R_v T s | CORRECT, asserted | It is R_v T ln(1+s) to first order in s. The text states it without the ln. Listed below as an unjustified step. |
| (10.6) dm/dt = 4 pi rho_w r G f_v (s - a/r) | CORRECT | This is Rogers and Yau's r dr/dt = G(s - a/r) times 4 pi rho_w r. Units kg/s. G = 9.7257e-11 m^2/s. Conduction share 61.6 %, diffusion 38.4 %, G with diffusion only = 2.533e-10 (2.60 times): all as quoted. |
| (10.7) dm_i/dt = -M_i(mu_i - mu_bar), M_i = 4 pi rho_w r_i G f_v/(R_v T) | CORRECT | Substitution checked. Units kg^2/(J s). |
| Step 3 numbers: 9.4 g/m^3 vapour, 1.1 g/m^3 water | CORRECT | rho_v,sat = 9.39 g/m^3; M0 = 1.109 g/m^3 (class run). |
| (10.8) mu_bar = sum M mu / sum M; r_c = a/s = sum r f / sum f | CORRECT | SymPy solve of sum M_i(mu_i - mu_bar) = 0. It matches `ripen().sat()`: s = a sum(w r f / r)/sum(w r f). |
| Claim "with f_v = 1, r_c is the mean radius" | CORRECT | With f = 1, r_c = sum r_i / N, the number-weighted arithmetic mean. Recomputed for the truncated two-mode cloud with ventilation: r_c = 8.3136 um, mean 8.3039 um, s = 1.3664e-4 (as quoted: 8.31, 8.30, 0.0137 %). |
| Key result: drops above r_c grow, below shrink | CORRECT | The sign of dm/dt is the sign of (1/r_c - 1/r), whatever f_v is. Pure water only, as stated. |
| (10.9) dF_s/dt = sum (mu_i - mu_bar) mdot_i = -sum M_i (mu_i - mu_bar)^2 <= 0 | CORRECT | SymPy: the difference is identically 0. Units W. Limit: all mu_i equal gives 0. It rests on sum mdot = 0 (vapour store neglected), which is stated. |
| dS/dt = -dF_s/dt / T | CORRECT | Follows from (10.4) at fixed T. |
| (10.10) R = sum mdot^2/(2M) + sum mu mdot - mu_bar sum mdot; dR/dmdot_i = 0 gives (10.7) | CORRECT | SymPy: mdot_i = -M_i(mu_i - mu_bar). The Hessian is diag(1/M_i) > 0, so it is a minimum. "Half the dissipation" holds: at the solution sum mdot^2/M = sum M(mu - mu_bar)^2 = T dS/dt. |
| (10.11) dr/dt = (G f_v a/r)(1/r_c - 1/r) | CORRECT | Divide (10.6) by 4 pi rho_w r^2 and put s = a/r_c. Units m/s. |
| Maximum of dr/dt is G a/(4 r_c^2) at r = 2 r_c (f_v = 1) | CORRECT | SymPy: d/dr = 0 at r = 2 r_c, value Ga/(4 r_c^2). Also checked: r much larger than r_c gives Ga/(r r_c), which goes as 1/r; r to 0 gives -Ga/r^2, so the drop vanishes in finite time. |
| (10.12) tau ~ r_c^3/(G a) | CORRECT (order of magnitude) | The rate at r = 2 r_c is Ga/(4 r_c^2) and at r = r_c/2 it is -2Ga/r_c^2, so "about Ga/r_c^2" holds to a factor of 4. tau = 5194 s = 1.443 h (quoted 1.44 h). |
| Table "first step, drop by drop" (dr/dt, dm/dt, share per hour) | CORRECT | Recomputed with code f_v and r_c = 8.3136 um. 5 um: -6.34 um/h, -5.53e-16 kg/s. 8 um: -0.235 um/h, -5.24e-17 kg/s, -8.80 %. 12 um: +1.227 um/h, +6.17e-16 kg/s, +30.7 %. 40 um: +1.010 um/h, +5.64e-15 kg/s, +7.58 %. Collector/12 um ratio 9.15. 43.3 % growing; 129.4 droplets/cm^3 above r_c; water in transit 85.2 % to droplets and 14.8 % to collectors. |
| Ledger table (r_c, drops left, water passed, droplet/collector water, F left) | CORRECT | Every cell matches `data/ripening.json` classes.rec at 0, 1 h, 6 h, 1 d. For example, 1 h: r_c 9.050 um, 212.1/cm^3, moved 13.74 %, 70.18/29.82 %, F 86.92 %. -dF/dt at start is 4.59e-7 W/m^3. |
| "r_c^3 grows at (4/9)Ga; between 12 and 24 h ours grows 1.8 times faster" | CORRECT | From the class run r_c: 1.83. Caveat: `ripening.json` field `lsw.measured` (run_ripening.cjs line 79) stores the growth of the cube of the mean-cube radius `rmean3`, a different quantity. Its ratio is 3.20. The text is right; that stored field does not support it. |

## 2. book-02, "Stokes' drag, derived", method box, Example 2.1

| item | verdict | notes |
|---|---|---|
| Step 1, creeping-flow equations | CORRECT | Dropping rho_a (u.grad)u. |
| Step 2, stream-function velocities; far field psi = (1/2) U r^2 sin^2 theta gives u_r = U cos theta, u_theta = -U sin theta; 2 pi psi is the volume flux | CORRECT | SymPy. theta is measured from the downstream direction, and this is used consistently later. |
| Step 3, E^2 operator and E^2 E^2 psi = 0 | CORRECT (the curl step is asserted, and the text says so) | |
| Step 4, E^2(sin^2 theta f) = sin^2 theta (f'' - 2f/r^2); powers n(n-1)-2 = (n-2)(n+1), (n-2)(n-3)-2 = (n-1)(n-4), giving n = 2, -1, 4, 1 | CORRECT | SymPy. |
| Step 5, f(a) = 0 and f'(a) = 0 give C = -3Ua/4, D = Ua^3/4 | CORRECT | SymPy solve. |
| (2.1) psi, u_r, u_theta | CORRECT | SymPy: E^4 psi = 0, both velocities match, no slip at r = a. "15 % slower at 10 radii": u_r/U = 0.8505. |
| Step 6, tau_r theta(a) = -(3/2) mu U sin theta / a; the other shear term vanishes; 2 mu du_r/dr = 0 at r = a | CORRECT | Full tau_r theta = mu(r d(u_theta/r)/dr + (1/r) du_r/dtheta) computed. |
| Step 6, p - p_inf = -(3/2) mu U a cos theta / r^2 | CORRECT | SymPy: both components of grad p = mu lap u hold (vector Laplacian in spherical coordinates). Higher upstream (cos theta < 0): right. |
| Step 7, sign conventions (inward normal stream-wise part -cos theta; shear direction e_theta, stream-wise part -sin theta) | CORRECT | The integrand from traction sigma.e_r . e_z equals the text's two integrands term by term. |
| Step 7 integrals and (2.2): F_p = 2 pi mu a U, F_s = 4 pi mu a U, F = 6 pi mu a U | CORRECT | SymPy. |
| (2.3) v = 2(rho_w - rho_a) g a^2/(9 mu) | CORRECT | |
| Re of Stokes speed = 4 rho_a (rho_w - rho_a) g a^3/(9 mu^2); Re = 1 at 41.0 um; 1.23 m/s and Re 15 at 100 um | CORRECT | 40.99 um; 1.2296 m/s, Re 14.5. |
| (2.5) N_Da = 4 rho_a (rho_w - rho_a) g d^3/(3 mu^2); C_D = 24/Re returns (2.3) | CORRECT | SymPy. |
| Method box vs `vBeard` | CORRECT | Every step matches line for line: C_sc = 1 + 2.51 lambda/d (line 74); d < 19 um uses C_sc k a^2 (line 75); X = ln N_Da (line 77); Horner sum of B2 (line 78); Re = C_sc e^Y and v = mu Re/(rho_a d) (line 79); third fit at d >= 1.07 mm (lines 81-84), without C_sc, which also matches "replaces steps 3 and 4". The code also sends non-water particles (ice) to regime 2 at all sizes. The box is about water drops, so this is not an error. |
| Example 2.1 | CORRECT | lambda = 7.555e-8 m; C_sc = 1.00237; N_Da = 22.305; X = 3.1048; Y = -0.18081; Re = 0.83657; v = 0.17709 m/s; Stokes Re 0.9294, v 0.19674 (11.1 %). 100 um: N_Da 348.51, Re 8.594, v 0.72767, N_Da/24 14.52. 8 um: 7.869e-3 times 1.01185 = 7.963e-3 m/s. |

## 3. book-11, (11.2) and (11.3)

| item | verdict | notes |
|---|---|---|
| Step 1, variations dH, dN, dM | CORRECT | |
| Step 2, stationarity of H - alpha N - beta M gives n = e^(-1-alpha) e^(-beta m) | CORRECT | The step to "maximum" is asserted: the second variation -int dn^2/n < 0 is not given (see the unjustified-steps list). |
| Step 3 and (11.2): N = C/beta, M = C/beta^2, beta = N/M, C = N^2/M | CORRECT | SymPy. Units 1/(kg m^3). Mean mass 3.708e-12 kg is a 9.60 um sphere. |
| (11.3) N = N0/(1 + K N0 t/2) from dN/dt = -(1/2) K N^2 | CORRECT | SymPy dsolve. Limit t = 0 gives N0. Units: K N0 t is dimensionless. |

## 4. book-03, method box "collision efficiency of one pair" vs `trajHits`, `flowEfficiency`, `pairEfficiency`; (3.1) to (3.2)

| item | verdict | notes |
|---|---|---|
| (3.1) to (3.2) non-dimensionalisation | CORRECT | dv/dt = (U^2/R) dw/ds; divide by U; tau g* = v(r) gives S. dx/dt = v gives dy/ds = w. St = tau U/R. |
| Step 1, the four numbers | CORRECT | `pairEfficiency` lines 210-211. The code also returns E = 0 when S >= 1 (line 212), which the box does not say. |
| Step 2, start at Z (200 creeping, 30 potential), moving with the air less settling | CORRECT | Line 110: y[2] = a_x, y[3] = a_z - S. Line 213: Z = 200 and 30. |
| Step 3, error control: "A step is accepted only if that error is below 10^-7 of the partner's distance from the collector's surface" | WRONG (incomplete) | Code line 126: the position tolerance is 1e-9 + 1e-7 min(dist, 10). That is an absolute floor of 1e-9, and the distance is capped at 10 radii, so at the 200-radius start the tolerance is 1e-6, not 2e-5. The two velocity components are also controlled, with tolerance 1e-8 + 1e-7 abs(w). The step size changes by 0.9 err^(-1/5), clamped to [0.2, 4]. Corrected sentence: "A step is accepted only if, for each position component, the error is below 10^-9 + 10^-7 times the distance to the surface (counted at most as 10 radii), and for each velocity component below 10^-8 + 10^-7 times its size." Also not stated: for St < 10^-3 the code integrates the inertia-free first-order equation dy/ds = u_hat - S e_z (lines 107, 114). Stopping rule (contact at 1+p; miss when z > 1+p) is CORRECT (lines 131-132). |
| Step 4, "A partner at b = 1.5(1+p) must miss" | WRONG (incomplete) | Code line 160: `while (trajHits(..., hi, Z)) hi *= 1.5`. If it hits, the bracket is widened, not assumed. "On the axis" is b = 1e-6 in the code (line 159). Halving until the width is below 1e-7(1+p) gives 24 halvings from 1.5(1+p): correct (log2(1.5e7) = 23.8). For 40/8 um no widening occurs in either flow, and none occurred in a scan of 24 pairs from 20 um to 3 mm. Fix: "...must miss; if it does not, the offset is multiplied by 1.5 until it does." |
| Step 5, E = (2 psi_hat(b_c,-Z) - S b_c^2)/((1-S)(1+p)^2) | CORRECT | Line 166, the same expression. The flux derivation is correct: partners move with the air minus S; 2 pi psi_hat is the air volume flux through the disc; the geometric reference flux is pi(1+p)^2(1-S). Limit psi_hat to (1/2) b^2 recovers (3.5). |
| Step 6, Langmuir weight | CORRECT | Line 214. |
| Step 7, 64 by 40 table, log spaced, p > 0.6 held at 0.6 | CORRECT | `makeTable` defaults; `tableE` clamp. Table entries with p >= 0.999 are set to 0 (line 225); the clamp makes this unused. |
| Example 3.1 | CORRECT | g* = 9.7997; tau = 0.81255 ms; tau U = 143.9 um; St = 3.597; S = 0.04496; Re = 0.8366; b_c = 0.69986 and 1.09868; E_S = 0.33747, E_P = 0.83823, plain (3.5) creeping 0.34015; E = 0.34436. Starting at 400 radii: E_S = 0.337458, a change of 1.6e-5 (claim: < 1e-4). |

## 5. Method boxes of chapters 5, 6, 12

| item | verdict | notes |
|---|---|---|
| book-05 box vs `sceStep` | CORRECT | Pair order i <= j with the smaller bin first (lines 378-380). C formulas (389, 391). Bin search x_k <= x* < x_{k+1} (386-388). Caps N_i, N_j/f when k = j, N_i/2 when i = j (389, 392-395). Take out (399). Lever deposit or overflow (400-404). In place. Grid size 289 at s = 8 confirmed. Not in the box: a final clip of negative N to 0 (415-416); the overflow test is x* >= x_last (kk >= n-1), meaning "at or above the last grid mass", which matches "beyond the last bin" closely enough. Example 5.1 recomputed: N_72 = 1.549e7, N_128 = 6.314e4, K = 4.3532e-10, dv = 0.17160, E = 0.34589, C = 425.74, 0.674 %, r* = 40.422 um, f = 0.08632, net 36.75, 1/f = 11.58. |
| book-06 box vs `gillespieRun` | CORRECT | Four classes per doubling of radius (line 556, 563). K* = pi(hi_a + hi_b)^2 max dv max E (times 1 + 1e-9) (573-575). The proposal rate uses n_a^2/(2V) for a = b (581), as the box writes it; picking the same drop twice is rejected (609); this is exact (a given pair is proposed at 2/n_a^2 of K* n_a^2/(2V), so its rate is K*/V). Wait -ln u/a* (599). Class pair, then uniform members (604-608). Accept if u2 < K/K* (612). Merge and update terms (617-622). The code comment at line 526 says "half n_a(n_a - 1) for a = b", which contradicts the code; the text agrees with the code. Pair counts in Example 6.1 (4 528 545; 45) check. |
| book-12 box, mean motion: "successive over-relaxation: every grid value is replaced again and again by the average of its four neighbours plus the source, until nothing changes" | WRONG (minor) | `cellFlow` line 786-787: psi += 1.9 (avg + h^2 omega/4 - psi), i.e. over-relaxed with omega = 1.9, not replaced by the average. It stops when the largest change is below 1e-10 h^2 or after 4000 sweeps. psi is free only at nodes whose eight neighbours are all inside the outline (776-779), which is stricter than (12.2)'s "psi = 0 on and outside the outline". Fix: "each grid value is moved 1.9 times the way toward the average of its four neighbours plus the source, sweep after sweep, until the largest change is below 10^-10 h^2; psi is held at zero at every node with a neighbour outside the outline". The source sign (psi = (sum + h^2 omega)/4 for lap psi = -omega) is CORRECT. |
| book-12 box, start: 96 droplet and 32 collector super-droplets per cell | CORRECT for the published runs; differs from the page | `makeCloud` defaults to perCell [24, 8] (line 811). `tools/run_cloud.cjs` line 13 passes [96, 32]. The live page (`app.js` line 391) runs [24, 8]. The box says "as the model takes it" without saying which. |
| book-12 box, steps 1 to 9 vs `move` and `step` | CORRECT | OU update with the drift only where epsilon varies (854-857). Advect with U at the old position, then mirror and reverse the eddy component at all four walls (859-862). Fall (863). Ground (873). Evaporation r^2 += 2GSf_v dt, removed below 1 um (r^2 < 1e-12) (876-881). Cells (887). Fisher-Yates shuffle and floor(n/2) pairs (891-892). p from (12.5) with the larger multiplicity as j (896-898). gamma = floor(p) + Bernoulli(frac), capped at floor(xi_j/xi_k) (899-900). Merge radius and xi update; equal split when j is emptied (901, 911-912). Example 12.1: K = 4.2052e-10, xi_j K dt/dV = 1.314e-3, factor 127, p = 0.167; e^(-1/33.33) = 0.9704; kick 0.2413; 40 to 40.106 um; 100 um loses 6.04e-11 m^2 of r^2 = 0.30 um. |

## 6. Problem 9

| item | verdict | notes |
|---|---|---|
| r_c = 8 um, s = 0.0142 %, a = 1.136 nm | CORRECT | s = 1.4200e-4. |
| dr/dt = -2.76 and +0.99 um/h | CORRECT | -2.762, +0.994. Equal and opposite mass rates, as the "thicker shell" sentence implies. |
| Lifetime 29.4 min (with ventilation 29.3-29.5) | CORRECT | Integrating (10.11) with r_c = (r1+r2)/2 and r1^3 + r2^3 = 1216 um^3: 29.39 min; with code f_v: 29.38 min. |
| Bound r^3/(3Ga) = 10.9 min | CORRECT | 10.86 min. It is a lower bound because s > 0 slows the shrinking. |
| Final 10.67 um; F falls to 83.8 % | CORRECT | 10.674 um; 1216^(2/3)/136 = 0.8377. |

## Steps asserted without justification

- book-02 step 4: "nothing on a sphere can introduce another angular shape". The reason (the equation is linear and separable, the boundary data are proportional to sin^2 theta, and the solution is unique) is not given.
- book-02 step 3: the curl giving E^2 E^2 psi = 0 (the text says so openly).
- book-02 step 6: the size of the pressure term, "putting it into the radial momentum equation fixes its size". The result is right (SymPy), but the substitution is not shown.
- book-10 step 2: mu_bar = R_v T s, the linearised form of R_v T ln(1+s), with no reason given.
- book-10 step 3: that s changes only in its fourth decimal, so the vapour is not a store (true here: 9.4 g/m^3 times about 1e-4 is about 1e-3 g/m^3).
- book-10 step 4: "every drop lowers the free energy". This holds only after mu_bar times the sum of mdot is subtracted; a growing drop's own term mu_i mdot_i is positive.
- book-11 step 2: it is stated to be a maximum, but only stationarity is shown. H is concave, so it is a maximum. Also, ln n of a dimensional density depends on units; the text touches on this only later ("choice of variable").

## Symbols used for two things inside one chapter, or before definition

- Chapter 3: the collector radius is R throughout, but the potential-flow stream function is written psi = (1/2) U sin^2 theta (r^2 - a^3/r) with a (carried over from chapter 2). It should read R^3/r.
- Chapter 11: M is the total water in 11.3 and (11.2), while the 11.1 method box uses M_i for the vapour mobility of (10.7).
- Chapter 3: s is the dimensionless time in (3.2), and S is the settling ratio. They are distinct but easily confused; s is also the supersaturation in chapters 10 and 12 (other chapters, so not a clash).
- No symbol is used before its definition in the sections checked. Chapter 10 states its re-use of mu explicitly.

## Unit errors

None found. Checked dimensionally: (2.1) to (2.5), (3.2), (10.4) to (10.12), (11.2), (11.3), (12.5).
