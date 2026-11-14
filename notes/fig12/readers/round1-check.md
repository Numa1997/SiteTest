# Fig. 12 (Kaggle) lecture note: check, round 1

Page checked: `public/simulations/guinness-kaggle.html`, `<article id="paper">`, as at commit 81a1de2 (the note rewritten from run 10).
Checked against: `tools/fig12/kaggle/stout_jax.py`, `run_b.py`, `pack_ride.py`; the page's own scripts `guinness-jax-play.js` and
`stout-view2.js` (StoutRide); the stored files of `public/data/fig12/2026-11-14-run10/` (all ten SHA-256 fingerprints match
the index, computed in the browser); the run summaries `notes/fig12/jax/run8-check/run8-summary.json` and
`notes/fig12/jax/run10-check/run10-summary.json` (books, impulses, rest guard, energies, timings);
`notes/fig12/handoff-jax/portcheck.txt`; `public/scripts/guinness-glass.js`. `note_numbers.py` was not run; I read only its
`cart_alone` block and a few `put` lines, to find out how three disagreeing numbers had been defined (rows N56, N87, N95).

How each thing was checked:
- Equations: re-derived in SymPy 1.14 (symbolic identities, ODE and PDE residuals, limits) or checked numerically with mpmath
  and SciPy (Bessel integrals, energy integrals of the mode, Riccati residuals, Van Loan identity, Floquet multipliers).
  Units checked by hand.
- Stored data: the page was served by `notes/fig12/serve.cjs` and opened in headless Google Chrome (Playwright). In the page,
  each file was fetched, its SHA-256 computed, unpacked with the page's own `StoutRide.unpack`, and the surface read with
  the page's own `StoutRide.at` and `atInward` on the 64-point outer ring (R - dx/2) and the ring at 13/16 of it. These reads,
  the stored per-frame lists (t, v, i, icmd, us, ipar, qhat, yq, books) and the page's own table (`#cmp`) and readings
  (`r-v`, `r-sg`, `r-s`, `r-hg`, `r-h`, `r-d`, `r-i`, `r-u` at the last frame of every ride) were exported and analysed in Python.
  The damped-cosine fit was redone with my own least-squares code (SciPy `least_squares`, 72 starting guesses).
- Theory numbers: recomputed from the formulas with the code's constants and the glass table.
- Cart numbers (Table 4, section 12.3, Figure 4): the code's `Cart` class (JAX, float64, CPU) run alone with my own driver,
  pint frozen (F = 0, load 454.41 g), sub-steps of 0.1 ms, speed loop.
- Controller numbers: my own Riccati solutions (SciPy `solve_continuous_are`; the suspension's cross term removed by the
  shifted-LQR transform rather than SciPy's `s=` argument), my own Kalman covariance cycle (4000 samples, probe at every second),
  `quad_vec` integrals for B_d and Q_d, Floquet multipliers by `solve_ivp`.

Verdicts: "verified", "wrong, because ..." (with the correct value), "unverifiable, because ...".

## Equations

| # | Equation | Verdict |
|---|---|---|
| E1 | (1) Newton's law in the glass's frame, delta m x'' = F - delta m a_g | verified (moving the frame acceleration to the right; units N) |
| E2 | g_eff = g - a_g = (-a, 0, -(g + a_z)) (unnumbered) | verified |
| E3 | material derivative Du/Dt = du/dt + (u.grad)u (unnumbered) | verified |
| E4 | (2) Navier-Stokes in the glass's frame | verified (each term m/s^2; the viscous form mu lap u needs div u = 0, as stated) |
| E5 | (3) div u = 0 | verified |
| E6 | (4) kinematic surface condition | verified |
| E7 | (5) p = p_s on the surface | verified |
| E8 | 3.4 checks: p = p_s + rho g (h - z); tan alpha = a/(g + a_z); rigid load needs m(a_g - g) | verified (grad p = rho g_eff, surface normal to g_eff, -integral grad p dV = -m g_eff) |
| E9 | (6) unsteady Bernoulli, phi_t + p/rho + (g + a_z) z + a x = C(t) | verified (SymPy: grad of (6) returns the linearised, inviscid (2) with g_eff = -grad(a x + (g + a_z) z)) |
| E10 | separation of Laplace's equation for f(r) cos(theta) Z(z) (unnumbered) | verified (SymPy, exact) |
| E11 | (7) phi = cos wt cos theta J1(kr) cosh kz | verified (SymPy: Laplacian zero; d/dz = 0 at the floor; Y1 excluded on the axis) |
| E12 | (8) J1'(kR) = 0, xi = 1.8412 | verified (mpmath root 1.841183781) |
| E13 | (9) phi_tt + g phi_z = 0 at z = h | verified |
| E14 | (10) w11^2 = g k tanh kh | verified (SymPy solves (7) in (9) to exactly this; units s^-2) |
| E15 | c1 = 2R/((xi^2 - 1) J1(xi)), with int r^2 J1 = R^3 J2(xi)/xi, J2(xi) = J1(xi)/xi, int J1^2 r dr = R^2(1 - 1/xi^2) J1^2/2 | verified (mpmath quadrature: 0.171644 = 0.171644, 0.119347 = 0.119347, c1 1.438194 = 1.438194 for R = 1; orthogonality of J1(k1 r), J1(k2 r) 1e-15) |
| E16 | projected surface conditions q'/J1(xi) = k tanh kh phi1, phi1' + (g + a_z) q/J1(xi) + a c1 = 0 | verified |
| E17 | Bernoulli at the surface with a r cos theta (unnumbered, 4.2) | verified |
| E18 | (11) q'' + w11^2 (1 + a_z/g) q = -beta a, beta = 2 xi tanh(xi h/R)/(xi^2 - 1) | verified (SymPy from E16; static limit q = -0.837 R a/g against the exact R a/g) |
| E19 | (12) q_max = beta abs(dv)/w11 | verified (SymPy: q = -(beta dv/w) sin wt solves (11), q'(0) = -beta dv) |
| E20 | (13) q_max = (beta/w11) abs(integral a e^{j w t'} dt') | verified (Duhamel for (11) with a_z = 0) |
| E21 | (14), q = q0 e^{-zeta w t} cos(w_d t + psi), w_d = w sqrt(1 - zeta^2); sigma = Pi/2E, zeta = Pi/(2 E w) | verified (SymPy residual zero) |
| E22 | (15) Stokes layer, delta = sqrt(2 nu/w) | verified (SymPy: u - U cos wt satisfies the diffusion equation; u = 0 at the wall) |
| E23 | (16) tau_w = rho sqrt(nu w/2) U (cos wt - sin wt); in-phase power (1/2) rho sqrt(nu w/2) U^2; gradient sqrt2 (U/delta) e^{-d/delta} cos(wt - d/delta + pi/4); heat equals work | verified (SymPy, all four identities exact) |
| E24 | mode energy E = (1/2) rho B^2 k cosh sinh pi int J1^2 r dr = (pi rho B^2/4) k cosh kh sinh kh R^2 (1 - 1/xi^2) J1^2 | verified (volume integral of (1/2)abs(grad phi)^2 by quadrature equals the surface form: 1.129581 = 1.129581) |
| E25 | wall integral pi R B^2 J1^2 int (cosh^2/R^2 + k^2 sinh^2) dz | verified |
| E26 | (17) sigma_wall = sqrt(nu w/2)(xi^2 + 1)/(2R(xi^2 - 1)), zeta_wall = (delta/4R)(xi^2 + 1)/(xi^2 - 1); deep form 0.5575 nu^1/2 R^-3/4 g^-1/4 | verified (exact integrals for the pint give 0.110111 s^-1 against 0.110122 from the deep-glass formula; coefficient sqrt2/4 xi^-1/4 (xi^2+1)/(xi^2-1) = 0.55751; Bongarzone's m = 1 side-wall term reduces to the same factor) |
| E27 | (18) sigma_skin = sqrt(nu w/2)(k/2) coth kh; bulk 2 nu k^2 | verified (Pi/2E with int abs(grad_h phi)^2 = k^2 int phi^2; bulk rate is the standard result) |
| E28 | Sauter radius R32 = (1/2) d_bar e^{2 s^2} from log-normal moments | verified (SymPy: e^{3m+9s^2/2}/e^{2m+2s^2} = e^{m+s^2/2} e^{2s^2}) |
| E29 | (19) p_L, G0, tau_y (Voelp and Willenbacher) | verified against the code (`P_GEN`, `G_HEAD`, `TAU_Y`); the laws themselves are quoted, source not read in this check |
| E30 | (20) Tcholakova films and channels, Ca_f | verified against the code (`foam_flow_stress`, with (1 - Phi) = `PHI_F`); source not read |
| E31 | (21) Cantat edge stress, Ca_w | verified against the code (`head_wall_stress`, Z = 0.18, l/r_m = 0.004 by `np.interp` held at the 0.25 values); source not read |
| E32 | (22) h_eff = (3/5k)(1 - e^{-5 k h_f/3}) | verified (SymPy integral; Problem 4 limit 3/(5k)) |
| E33 | kappa = tau_edge(abs(w)) h_eff/abs(w) x (glass length)/(column area) (unnumbered) | verified (`acs * heff * head_wall_stress(ws) / max(abs(ws), 1e-3)`; wall area per cell volume = length/area) |
| E34 | (24) rho_f ((1/2) abs(g_eff,z) z+ + a_out z+) >= tau_y | verified (block: int rho_f g z dz / z+ = rho_f g z+/2; code `head_spill`) |
| E35 | (25) p_s = m_s (g_eff,z + dw/dt) | verified |
| E36 | (26) w^2 = g k tanh kh/(1 + lambda_h k tanh kh) | verified (SymPy from the two surface conditions with the head's inertia) |
| E37 | (27) (1 + lambda_h k tanh kh) q'' + w11^2 (1 + a_z/g) q = -beta a | verified (SymPy projection with the m_s q'' term) |
| E38 | (23) rho 2 dx (w' - w)/dt = div_h(h_f mu_f grad_h w') - kappa w' | verified against the code (`head_sheet`: m = rho Hb, Hb = 2 dx, implicit matrix diag = m + dt(cx + cy + ... + kap)) |
| E39 | yield balance q = h_f tau_y k/(rho g) (unnumbered) | verified (order-of-magnitude estimate; units m) |
| E40 | (28) M_x v' = b i - c_x v + F_d, M_x with (I_w + N_g^2 J_m)/R_w^2 | verified (code `massX`, `forces`) |
| E41 | (29) tau_i di/dt = i_reach - i, clip to +-I_max then to (+-V_max - E)/R_a | verified (code `forces`, `step`, exact exponential) |
| E42 | (30) -F_gs = m(g - a_g) - dP/dt | verified |
| E43 | (31) damped Mathieu; growth when epsilon > 4 zeta at Omega = 2w | verified (SymPy averaging, Problem 9: rates w(+-epsilon - 4 zeta)/4) |
| E44 | (32) APIC transfers; a linear field survives both hand-overs; sinc^2 = 1 - (kappa dx)^2/12 per hand-over | verified (SymPy: trilinear weights are a partition of unity, reproduce x and have gradient sum 1 and 0; series of sinc^2; code `p2g`, `g2p`) |
| E45 | (33) p_g = p_l(1 - 1/alpha) + p_s/alpha, alpha >= 0.05 | verified (SymPy; code clips theta to [0.05, 1]) |
| E46 | w'(alpha + m_s/(rho dx)) = alpha w* - (dt/(rho dx))(m_s g_eff,z - m_s w_h/dt - p_l) (unnumbered) | verified (SymPy) |
| E47 | (34) alpha -> alpha + m_s/(rho dx), p_s -> m_s(g_eff,z + (w* - w_h)/dt) | verified (SymPy: the plain update with these two changes equals E46 exactly; code `pressure`: `tLR + muF/dx`, `muF (geff_dt + vel[2] - w_old)`) |
| E48 | (35) chi = abs(x - x_bar) - r0, b_i = (1 - d^2/(2dx)^2)^3 | verified (code `level_set`) |
| E49 | (36) E_p(0) - E_p(t) = E_k(t) + D(t) | verified (no outside work with the glass held still) |
| E50 | (37) PI command | verified (code `Cart.sample`, ctrl 1) |
| E51 | (38) M_x dv'' + (c_x + b K_p) dv' + b K_i dv = 0; K_i = K_p w_c/4 gives a double root at -w_c/2 without drag | verified (SymPy) |
| E52 | loop gain L = b(K_p + K_i/jw)/(M_x jw + c_x), S = 1/(1 + L) (unnumbered) | verified (SymPy, closed-loop over open-loop response) |
| E53 | q_peak = (beta_h abs(dv)/w) e^{-zeta w t_p}, w_d t_p = arctan(sqrt(1 - zeta^2)/zeta) (unnumbered) | verified (SymPy: q' = 0 there; zeta -> 0 gives t_p = pi/2w and (12); Problem 12 exponent) |
| E54 | (39) preview i_cmd = i_PI + N0 z_a'(x + v tau_i)/b; lag = delay to first order | verified (SymPy series; code ctrl 2) |
| E55 | (40) F_a = -c_sky v_b | verified (code `susp`) |
| E56 | (41) A, B of the slosh model | verified (derivation and identical to code `slosh_lqr`) |
| E57 | (42) LQR cost | verified |
| E58 | (43) K = B^T X/r_u and the Riccati equation; abs(K4) = sqrt(Q44/r_u) = I_max/x_e,m | verified (Riccati residual 1e-9 of terms ~1e5; (4,4) entry argument uses only the zero fourth column of A; K4 = -150.000) |
| E59 | y_q = (eta_front - eta_back)/2 (unnumbered) | verified (code `probes`) |
| E60 | scalar Kalman blend L = C/(C + sigma^2), variance (1 - L)C (unnumbered) | verified (SymPy) |
| E61 | (44) A_z, B_z, G | verified (identical to code `observer_design`; first three rows of (41) with b i0 = c_x v0) |
| E62 | (45) A_d, B_d, Q_d | verified (B_d from the block exponential equals `quad_vec` to 2e-16) |
| E63 | (46) Van Loan, Q_d = A_d Phi(T_s) | verified (equals the direct quadrature to 1e-16, relative) |
| E64 | (47) prediction | verified (code `observe`: `Ad @ oxh + Bd * uPrev`, uPrev the current at the last sample) |
| E65 | (48) correction, Joseph form | verified (Joseph equals (I - LH)C for the optimal gain to 8e-17; code uses it) |
| E66 | swing with heave q'' + 2 zeta w q' + w^2(1 + a_z/g) q = -beta_h a (12.8, unnumbered) | verified |
| E67 | (49) i_par = -(M_x w^2/(beta_h b))(a_z/g) q_hat | verified (SymPy; code ctrl 4) |
| E68 | (50) body and wheel | verified (identical to code `susp_lqr` A, B) |
| E69 | (51) cost; a_z = (-k_s z_s - c_s(v_b - v_w) + F_a)/M_s; Q_s, N_s, R_s | verified (code `Ca`, `Da`, `N`, `R`) |
| E70 | (52) K_s = R_s^-1(B_s^T X_s + N_s^T) and its Riccati equation; completing the square | verified (shifted-LQR solution gives the same gains as the code to 8e-6) |
| E71 | numbering of (1)-(52) | wrong, because the numbers are not in order of appearance: (23) is printed in 6.6 after (24)-(27) of 6.4 and 6.5, and (31) in 11.4 after (32)-(36) of sections 8 and 9. Every number 1-52 occurs exactly once and every cross-reference points to the right equation |

## Numbers

| # | Where | Number(s) | Verdict |
|---|---|---|---|
| N1 | Abstract, 4, 11 | 3.421 Hz bare; 2.915 Hz with head; 13.9 mm; 82 N against 15 N | verified (see N20, N52, N63, N76) |
| N2 | 1 | 30 pictures a second; about a million parcels | verified (fps 30; 1,001,952 particles) |
| N3 | 2 | glass 149 x 76 mm drawing, scaled to 160 x 85 mm | unverifiable, because the source drawing was not opened (the glass table's header states the scaling) |
| N4 | 2 | floor radius 16.3 mm; 28.4 mm at 5 mm; widest 39.3 mm at z = 116 mm; rim 147.5 mm; R = 39.1 mm at 125 mm; changes by 0.29 mm in the top 20 mm | verified (glass table: 16.31, 28.43, 39.30 at 116.0, 147.5, 39.100; max - min over 105-125 mm 0.287) |
| N5 | 2 | stout 426.6 mL; head top 144 mm, 3.5 mm below the rim; stout surface 22.5 mm below the rim | verified (trapezoid volume 426.60 mL) |
| N6 | 2, Table 1 | rho 1007, mu 2.06 mPa s; Watamura 1006 and 2.03-2.23; settling 120 s; head 18-20 mm, 17.5/20.6/22.2 mm; d_bar 61 um, s 0.24; gamma 44.2, E_inf 18.7 mN/m | unverifiable, because the sources were not read in this check (all match the code's constants) |
| N7 | 2 | nu = 2.05e-6 m^2/s, about twice water | verified (2.0457e-6) |
| N8 | 2 | factor 1.122; R32 = 34.2 um, model 34 um | verified (1.12210, 34.224) |
| N9 | 2 | drained liquid fraction 0.36 bottom, 0.235 top; 25 to 110 minutes | unverifiable, because the drainage calculation is not in the code or the stored data |
| N10 | 2 | phi_l = 0.27; rho_f = 272 kg/m^3 | verified (271.89) |
| N11 | Ex. 2.1 | m_s = 5.17 kg/m^2; 50.7 Pa; 5.1 mm, lambda_h = 5.13 mm; disc 91.26 mL, 24.8 g; 429.6 g stout | verified (5.166, 50.68, 5.130, 91.255, 24.81; stored 429.583 g) |
| N12 | Ex. 3.1 | 0.88 m/s^2; 5.65 m/s^2 | verified (0.878, 5.645) |
| N13 | 4.1 | xi = 1.8412; k = 47.1 /m; 1/k = 21.2 mm | verified (47.089, 21.236) |
| N14 | Ex. 4.1 | xi h/R = 5.886; tanh = 0.99998; w^2 = 461.9; w = 21.49; f = 3.421 Hz; 0.292 s; kR = 5.331, 8.536; 5.82 and 7.37 Hz | verified (5.8861, 0.999985, 461.94, 21.493, 3.4207, 0.2923, 5.3314, 8.5363, 5.821, 7.365) |
| N15 | 4.2 | c1 J1(xi) = 0.837 R; beta = 1.541; 16 % | verified (0.83683, 1.54074) |
| N16 | 4.2 | q_max = 7.2 mm for 0.1 m/s | verified (7.169) |
| N17 | 4.2, 11.2, P7 | half-sine push 1.0 m/s^2, 0.146 s: 5.2 mm at the wall, 5.0 mm on the ring at 31.2 mm | verified (5.236 with T_p = 0.146 s exactly, 5.239 with pi/w; ring 4.978; r = 31.16 mm; push parameters (0.3, 1.0, 0.146) in `run_b.py`) |
| N18 | 5.1 | zeta = 0.0055 is about 3 % per swing | verified (3.4 %) |
| N19 | 5.2, Ex. 5.1 | w = 21.49 rad/s; delta = 0.436 mm (0.44); sqrt(nu w/2) = 4.69 mm/s; 0.047 Pa | verified (21.488, 0.4363, 4.688, 0.0472) |
| N20 | 5.3 | sigma_wall = 0.110 /s, zeta_wall = 0.0051; 0.918/R | verified (0.1101, 0.00512, 0.9184) |
| N21 | 5.3 | 0.5575; K = 3.50; 3.52 [5]; 5.23 [5]; 49 %; zeta = 0.0077 with K = 5.23 | verified for the arithmetic (0.55751, 3.503, 5.23/3.52 = 1.486, 0.00765); the quoted K values unverifiable, because source [5] was not read |
| N22 | 5.4 | sigma_skin 0.110 /s, zeta 0.0051; bulk 0.0091 /s, 0.0004 | verified (0.1104, 0.00514, 0.00907, 0.00042) |
| N23 | 5.4 key result | zeta = 0.0055; 8.4 s; 19.9 swings; lid 0.0107 | verified (0.005546, 8.39 s, 19.89, 0.01068) |
| N24 | 6.1 | 63.5 % jamming; Phi = 73 %; 2 gamma/R32 = 2600 Pa; Phi_c = 0.635 | verified (2600.0; Phi_c is the code's `PHI_C`) |
| N25 | Ex. 6.1 | p_L = 2400 Pa; 0.095; G0 = 166 Pa; tau_y = 5.4 Pa; sin alpha = 0.11, about 6 deg | verified (2400, 166.4, 5.415, 0.107, 6.1 deg) |
| N26 | 6.1 | tau_y 9.4 Pa at 0.24, 2.5 Pa at 0.30 | verified (9.375, 2.535) |
| N27 | 6.2 | Ca_f = 1.6e-5; films 7.5 Pa, channels 4.2 Pa; tau_v 11.7; tau 17.1 | verified (1.585e-5, 7.47, 4.25, 11.72, 17.14) |
| N28 | 6.2 | fits cover gas fractions 0.80 and above | unverifiable, because source [8] was not read |
| N29 | 6.3 | Z = 0.18, l/r_m = 0.004 at 0.25 | verified against the code's table; source not read |
| N30 | 6.3 | second term at most 1.5 % of the first; (21) gives 2.1, 9.7, 28, 45 Pa at 1, 10, 50, 100 mm/s; cap 20 to 223 Pa | verified (1.53 % at 1 mm/s; 2.10, 9.66, 28.2, 44.7; cap 19.9 to 223.3) |
| N31 | 6.3 | h_eff = 9.9 mm with 1/k = 21.2 mm | verified (9.873; the code uses `ell = Rfill/1.84118`) |
| N32 | 6.4 | 50.7 Pa at rest | verified |
| N33 | 6.4, Ex. 6.2 | wedge 8.1 mm; z+* = 4.1 mm; 7.6 mm; 2.0 mm at 5 m/s^2; about 3 times | verified (4 tau_y/(rho_f g) = 8.12; 4.06; 7.56; 2.01; 2.98) |
| N34 | 6.5 key result | 1.242; 0.897; 3.070 Hz; beta_h = 1.241 | verified (1.24156, 0.89746, 3.0699, 1.24097; equals the run-10 plant's 1.2409479 to 2e-5) |
| N35 | 6.5 | Sauret 3.1 Hz against 3.3 Hz | unverifiable, because source [10] was not read |
| N36 | 6.5 | thin layers about 6 % too strong with the head | verified (sqrt(3.42/3.070) = 1.055) |
| N37 | 6.6 | mu_f held below 0.05 /s at 123 Pa s | verified (122.8) |
| N38 | 6.6 | dx = 1.5 mm; rho 2 dx = 3.0 kg/m^2 | verified (3.02) |
| N39 | 6.6 | yield balance q = 0.5 mm | verified (0.49) |
| N40 | 7.1, Table 2 | all cart parameters; b = 5 N/A | verified (`CART_COMMON`) |
| N41 | 7.1, Ex. 7.1 | m_l = 454.4 g; M_s = 1.954 kg; turning parts 0.150 + 0.125 = 0.275 kg; M_x = 2.529 kg; 15 N, 5.93 m/s^2; 7.5 V, 2.25 A, 11.25 N; 0.6 A; N0 = 22.1 N; grip 17.7 N; 18.75 N | verified (454.41, 1.9544, 2.5294, 5.930, 22.116, 17.69) |
| N42 | 7.1 | body bounce 2.79 Hz | verified (2.789) |
| N43 | 7.2, Table 3 | slopes 0.251, 0.262, 0.785; the axle's steepest slope is the road's | verified (`road_table`: axle 0.2513, 0.2618, 0.7853 equal the road's) |
| N44 | 7.2, Table 3 | bumps 0.29 m apart; 3.448 Hz, 0.8 % faster; speeds 1.0, 1.0, 1.5 m/s; stored 8, 8, 4, 5 s; axle 1 m before the first bump; push at 0.3 s | verified (`run_b.py` ROADS and TASKS, `ride_extra` x0 = 0.5; 0.79 %; stored frames 241, 241, 121, 151) |
| N45 | 7.3 | one step 2 ms late; period 343 ms; 2.1 deg | verified (343.0 ms, 2.099 deg) |
| N46 | 8.1 | 57 x 57 x 114 = 370,386 cells | verified (`Geometry`: n = 57, nz = 114) |
| N47 | 8.1 | 1,001,952 particles; 0.429 mg; 0.93 mm; 126,399 cells; 7.93 per cell | verified (126,399.2 cells; 7.927; 0.933 mm) |
| N48 | 8.2 | k dx = 0.071; 8.3e-4 per step; 0.42 /s; zeta 0.019; more than three times | verified (0.07063, 8.32e-4, 0.416, 0.0193, 3.5 times) |
| N49 | 8.3 | nu dt/dx^2 = 0.0018, limit 1/6 | verified (0.00182) |
| N50 | 8.4 | tolerance 1e-05 of the largest right-hand side, at most 600 iterations | verified (`Stout` defaults, not overridden by `run_b.py`; the summaries show resmax 9.9999e-6 and at most 306 iterations) |
| N51 | 8.4 | lambda_h/dx = 3.4; lambda_h k = 10.7 at k = pi/dx | verified (3.42, 10.74) |
| N52 | 8.5 | 1,977 trusted columns | verified (count of r < R_fill - dx on the 57 x 57 grid; every stored frame of every file holds exactly 1,977 heights) |
| N53 | 8.5 | r0 = 0.9 dx and 0.505 dx; 0.68 cell; 1.5 cells | verified (code `rls`, `rread`, `surface`, `observe`) |
| N54 | 8.6 | dt = 2 ms, CFL 0.8, sub-steps 0.1 ms | verified (`make_advance`) |
| N55 | 8.6 | a ride step 84 to 93 ms | verified (rides used: 84.1-92.8 ms in the two summaries) |
| N56 | 8.6 | each simulated second cost 38 to 48 s | wrong, because the rides cost 43 to 48 s per simulated second (43.1-47.7 in the summaries, consistent with 84-93 ms a step at 510 steps a second); 38 s belongs to the pint at rest and the free swing (74 ms a step), which are not rides |
| N57 | 8.6 | a ride of 8 s about 6 minutes | verified (run_s 337.7-364.2 s) |
| N58 | 9 | largest stout discrepancy 0 particles | verified (books of the nine files that carry them; the run-6 free swing without head stores no books, but its stout in the glass is 429.583 g and its spill 0 in every frame) |
| N59 | 9 | head served 91.314 mL; largest discrepancy 1.3e-08 mL | verified (index head_err_ml_max up to 1.257e-8; the stored per-frame sums, rounded to 0.001 mL, add to 91.314 in every frame) |
| N60 | 9 | impulse book equals minus the final momentum to 9e-15 | verified (largest relative difference 8.69e-15, run 8 bump25; the eight rides of the note) |
| N61 | 9 | 2 s at rest; guard 0.75 mm and 0.375 mm; within 0.50 mm, 0.129 mm rms; nothing left | verified (run 8: 0.4978, 0.1292; run 10: 0.4975, 0.1292; spill 0) |
| N62 | 9 | energy fell by 25.4 uJ; 429.6 g sinking 6.0 um | verified (25.405 uJ; 6.03 um) |
| N63 | 10 | stored steps 0.02 mm, 0.1 mm, 0.1 mm, 0.1 mm^3 | verified (`pack_ride.py` QH, QHF, QD, QV) |
| N64 | 10 | playback: at most 0.1 s a frame; round(30 T); no blend; words at most 4 a second; SHA-256 refusal | verified (`guinness-jax-play.js`) |
| N65 | 10 | drops 0.43 mm^3; head fades below 1.5 mm; lean and tilt change by at most 0.02 mm when read from the rounded surface | verified (0.426 mm^3; `stout-view2.js` `hfm / 0.0015`; largest change 0.02 mm, free swing with head 7.60 against 7.58) |
| N66 | 11.1 | ring r = 13/16 (R - dx/2) = 31.2 mm; 64 angles | verified (31.16 mm) |
| N67 | 11.2 | without head: 3.330 Hz, natural 3.331 Hz, 2.6 % below 3.421; zeta 0.0160; method adds 0.0105, 1.9 times; about three times too fast; refit 3.331 Hz and 0.016 | verified (run fit 3.3302, 3.3306, 0.01601; my refit of the stored file 3.3302, 3.3306, 0.01601) |
| N68 | 11.2 | with head: 2.639 Hz; t_d = 0.128 s; 2.915 Hz; zeta 0.425; refit 2.917 and 0.425; 0.0105 is about 2 % | verified (run 2.6388, 2.9152, 0.4250; my refit 2.6404, t_d 0.1283, 2.9172, 0.4252; 0.0105/0.425 = 2.5 %) |
| N69 | 11.2 | k = 44.6 /m; 0.902; 3.004 Hz; 3.0 % lower; e-fold in 0.37 of a period; settles at -0.03 mm | verified (44.64, 0.9021, 3.004, 2.96 %, 0.374, fitted constant -0.027, mean after 1.5 s -0.028) |
| N70 | 11.2 key result | w = 18.32 rad/s | verified (18.317) |
| N71 | Table 4 | five bumps: 1.6 m/s^2; -0.7 to 20.0; 45 mm; 10 mm | verified (1.642; -0.670 to 19.953; 45.3; 10.5) |
| N72 | Table 4 | one bump: 1.0; 1.5 to 17.6; 8.5 mm; 7.1 mm | verified (1.041; 1.540 to 17.642; 8.54; 7.08) |
| N73 | Table 4 | kerb: 28.8; -2.4 to 20.6; 24 mm; 26 mm | verified (28.80; -2.414 to 20.611; 23.7; 25.9) |
| N74 | 11.3 | 2.0 times 22.5 mm; 18 % too fast; a quarter of a metre per second | verified (2.01; 18.3 %; 0.29 m/s in the cart-alone run) |
| N75 | 11.3 | "The single big bump would leave enough to break the head (Example 6.2)" | wrong, because with the head, the case in which there is a head to break, Table 4 gives an undamped swing of 7.1 mm, less than the 7.6 mm at which the head breaks; only the bare stout's 8.5 mm exceeds it |
| N76 | 11.4 | bare threshold 0.22 m/s^2 at 6.84 Hz; with head epsilon = 1.71 at Omega = 1.80 w, 16.8 m/s^2 at 5.2 Hz; roads at most 12 m/s^2 | wrong in one digit, because the lowest threshold lies at Omega = 1.81 w, 5.28 Hz (epsilon = 1.70911 there; 1.70931 at 1.80 w, so the minimum is very flat); 0.216, 6.84, 1.709, 16.77 and 12.2 m/s^2 are verified |
| N77 | 11.5, Table 5 | five bumps: tilt 13.6 mm | unverifiable, because the last digit depends on the unrounded value: the index gives 13.55 (already rounded to two places) and the stored, rounded surface gives 13.54; the page's own table also shows 13.6 |
| N78 | Table 5 | five bumps: lean 13.9; foam 0.01 mL from 1.50 s; 0 g; 0.94-1.05 m/s; 2.40 A | verified (13.89 index / 13.88 stored; 0.0097 from t = 1.500; 0.9435-1.0513; 2.402) |
| N79 | Table 5 | one bump: tilt 8.0; lean 8.9; 0; 0; 0.96-1.04 m/s; 2.00 A | verified (7.97/7.96; 8.94; 0.9623-1.0356; 1.999) |
| N80 | Table 5 | kerb: tilt 22.2; lean 24.3; 2.44 mL from 0.67 s; 0 g; 1.21-1.52 m/s; 2.98 A | verified (22.23; 24.26; 2.445 from t = 0.667; 1.2110-1.5171; 2.984) |
| N81 | 11.5 | lean about twice the 45 mm; 13.9 mm; 0.01 mL at 1.50 s; 8.9 mm, half less than 7.6 mm; kerb loses 0.29 m/s; 2.44 mL; 22.5 mm | verified (stored v from 1.5 to 1.211 m/s) |
| N82 | 11.5 box | versions 8 (commit 96e8a1d), 10 (58eea68), 6 (4c10527); the run-6 free swing unchanged by later head changes | verified (index entries; the diff of `stout_jax.py` 4c10527..96e8a1d touches the head's mass, the sheet switch, the probes and books, nothing on the path of the "wall" model) |
| N83 | 12.1, Table 6 | F_max 40 N, tau_u 5 ms, T_s 1 ms; sensors per controller | verified (code) |
| N84 | 12.2 | w_c = 2 pi x 8 Hz; M_x = 2.505 kg; K_p = 25.18; K_i = 316.4; 1 % heavier; roots -21.6 and -29.0 /s | verified (2.5046; 25.1788; 316.406, equal to `CART_COMMON`; 1.0 %; -21.58, -28.98) |
| N85 | Ex. 12.1 | 25.18 - 17.27j; 2 + 46.33j; L = -1.744 - 2.793j; 2.890; 0.346; 0.352; 35 % | verified (-1.7436 - 2.7925j; 2.8898; 0.3460; 0.3516) |
| N86 | 12.3 | N up to 105 N, 4.7 times static; up to 82 N within 42 ms; 20 ms above 15 N; 6 lift-offs, 92 ms; current 2.98 A; speed to 1.21 m/s | verified (104.85 N, 4.74; 82.3 N; span with a push above 1 N 43.0 ms at 0.1 ms resolution, 42 ms on a 1 ms grid; 20.4 ms; 6 and 91.9 ms; 2.977 A; 1.207 m/s) |
| N87 | 12.3, key result, Figure 4 | full forward current "from 4 ms before the wheel touches the kerb" to the top of the climb: speed falls to 1.29 m/s, a loss of 0.21 m/s | wrong, because (a) the current was commanded from the axle's x = 1.394 m, taken as 4 ms before x = 1.40 m, but the rim first touches the kerb at x = 1.437 m (the first point where `road_table` lifts the axle), so the current starts 29 ms early and first speeds the cart up to 1.576 m/s; the fall to 1.290 m/s is then a sudden loss of 0.29 m/s, not 0.21 (1.5 - 1.29 is not the loss). (b) With the current really commanded from 4 ms before the touch (x = 1.431 m) the cart reaches 1.506 m/s and falls to 1.227 m/s, a loss of 0.28 m/s. Either way the sudden loss is about 0.28 m/s |
| N88 | 12.3, key result | t_p = 68 ms; w_d = 16.58; 1.132; e^-0.531 = 0.588; beta_h dv/w = 14.2 mm; the wall rises 8.3 mm, more than 7.6 mm | wrong, because the loss is about 0.28 m/s (N87): beta_h dv/w = 19.0 mm and the first peak about 11.2 mm (not 14.2 and 8.3). The conclusion, more than the 7.6 mm at which the foam breaks, holds with a wider margin. t_p 68.3 ms, w_d 16.580, 1.1318, 0.5314 and 0.588 are verified |
| N89 | Figure 4 | time counted from the wheel's rim first touching the kerb | wrong, because the plot's zero is the moment the axle passes x = 1.40 m (t = 0.600 s); the rim first touches the kerb at x = 1.437 m, t = 0.625 s, 25 ms later |
| N90 | Ex. 12.2 | 3 mm ahead; 1.16 A; 3.47 A; 22.1 N against 105 N; 82 N, 16 A | verified (1.158, 3.473, 16.5) |
| N91 | 12.5 | c_sky = 47.6 N s/m; 0.70 against 0.12 | verified (47.636; passive 0.118) |
| N92 | 12.6 | Bryson limits 0.05 m/s, 2 mm, 2 mm x w, 2 cm, 3 A; K4 = 150 A/m | verified (code `slosh_lqr`) |
| N93 | Ex. 12.3 | K = (71.12, -1228.72, -40.50, -150.00); within 6e-03 of the stored gains; 7.1 A; +1.23 A; 0.40 A; 1.5 A | verified (71.1216, -1228.7227, -40.4996, -150.000; largest difference from the stored gains 6.04e-3) |
| N94 | 12.6 | open loop -7.79 +- 16.58j; closed -10.83 +- 7.03j, zeta 0.84; 39 % faster; -2.57 and -232 /s | verified (-7.785 +- 16.580j; -10.834 +- 7.026j; 0.839; 1.392; -2.571; -232.06) |
| N95 | 12.6 | bare design K = (75.0, -1937.8, -38.9, -150.0); decay 0.12 to 12.0 /s; about 101 times | verified with the unrounded zeta 0.005546 (75.04, -1937.81, -38.89; 0.119 to 12.01; 100.8). With zeta = 0.0055 as printed: K2 = -1937.9 and 101.6 times |
| N96 | 12.7 | W_F = 0.5 (0.22 N s in 0.1 s); W_a = 0.002 (0.026 m/s in a swing); sigma_v 2 mm/s; sigma_q 0.8 mm | verified (0.224; 0.0262; code defaults) |
| N97 | Ex. 12.4 | L = (0.953, -0.0038; -0.0006, 0.060; -1.172, 0.926); -9.5 mm/s and +11.7 mm/s; -1.23; 0.060 mm, 0.93 mm/s; 17 readings, 33 ms, a tenth of a swing; 2.0 mm/s, 0.20 mm, 6.9 mm/s | verified (0.9534, -0.00379; -0.00061, 0.0602; -1.1724, 0.9262; ratio -1.2297; 1/0.0602 = 16.6 readings; 1.953, 0.196, 6.886 after a probe sample) |
| N98 | 12.8 | 136.8 A/m; 335.5 s^-2; 0.70 A for 5 mm at 10 m/s^2 | verified (136.77, 335.51, 0.697) |
| N99 | 12.8 | a_m 0.5, z_m 10 mm, d_m 0.2 mm, F_m 40 N; static tyre compression 1.1 mm | verified (code; 1.106 mm) |
| N100 | Ex. 12.5 | K_s = (-501.22, 11.92, -6.34, 630.00); 84 %; 99 N/m; -1.93 +- 17.17j (2.75 Hz, 0.11) to -4.93 +- 4.98j (1.12 Hz, 0.70); hop 41.7 Hz, 0.08 to 0.12 | verified (-501.216, 11.923, -6.343, 630.004; 83.5 %; 98.8; 2.750 Hz, 0.112; 1.115 Hz, 0.704; 41.68/41.69 Hz, 0.083 and 0.124) |
| N101 | Table 7 | every limit and clock | verified (code) |
| N102 | 12.9 box | port check: 4e-13 A (speed, preview, skyhook), 6e-08 A (slosh, joint); suspension gains agree with the stored ones to 8e-06 | verified (portcheck.txt: icmd 2.30e-13, 4.18e-13, 8.66e-14; 6.34e-8, 6.39e-8; my K_s differs from the stored by 8.4e-6) |
| N103 | Table 8 | five bumps, joint: tilt 1.00, lean 1.03, 0, 0, 1.72 A, 0, 7.1 N | verified (index 1.00 and 1.03; stored surface 0.997 and 1.040, within the stated 0.02 mm; 1.720 A; 7.063 N) |
| N104 | Table 8 | one bump, joint: 1.03, 0.88, 0, 0, 1.65 A, 0, 7.9 N | verified (1.027, 0.880, 1.646, 7.926) |
| N105 | Table 8 | kerb, speed held: 22.2, 24.3, 2.44, 0, 2.98, 6 | verified (6 stored frames with abs(i_cmd) >= 3 A) |
| N106 | Table 8 | kerb, preview: 23.0, 23.9, 2.51, 0, 2.95, 6 | verified (23.03, 23.87/23.86, 2.507, 2.950, 6) |
| N107 | Table 8 | kerb, slosh LQR: 20.8, 21.8, 1.63, 0, 2.97, 6 | verified (20.81, 21.84, 1.626, 2.971, 6) |
| N108 | Table 8 | kerb, joint: 24.6, 25.4, 2.07, 0, 2.93, 5, 11.5 N | verified (24.55, 25.41/25.42, 2.074, 2.929, 5, 11.451) |
| N109 | Table 8 | "the table under the readings on the page shows the same numbers" | verified (headless Chrome: the page's table shows the same values, rounded to 0.1 mm for tilt and lean) |
| N110 | Figure 5 | bumps between about 0.8 and 2.3 s; joint within about a millimetre | verified (first contact 0.83 s, last bump left 2.33 s; joint largest lean 1.04 mm) |
| N111 | Figure 5 | "with the speed held the lean swings to more than ten millimetres at each bump" | wrong, because the largest lean near the five bumps is 7.5, 13.2, 13.9, 10.2 and 9.4 mm: the first and the last stay below ten millimetres |
| N112 | 12.10 | 13 and 10 times less; 1.72 and 1.65 A against 2.40 and 2.00 A; 7.1 and 7.9 N; cancellation current at most 0.016 A; filter 0.04 and 0.03 mm rms, probes 0.19 and 0.15 mm | verified (13.5, 10.1; 0.0156 and 0.0133 A; 0.037/0.034; 0.192/0.146) |
| N113 | Figure 6, 12.10 | wheel at the kerb at about 0.6 s | verified (0.625 s) |
| N114 | 12.10 | "the first surge is as large under each (Figure 6): leans of 23.9 (preview), 21.8 (slosh LQR) and 25.4 mm (joint) against 24.3 mm with the speed held" | wrong, because 24.3 and 23.9 mm are the back-swing at 0.87 s (lean -24.3 and -23.9 mm, back wall high), not the first surge. The first forward surges, at 0.67-0.70 s, are 22.2 mm (speed held), 21.2 mm (preview), 21.8 mm (slosh LQR) and 25.4 mm (joint). The Figure 6 caption ("about the same first peak") holds for 21-25 mm |
| N115 | 12.10, key result | foam 1.63 and 2.07 mL against 2.44 and 2.51 mL; no stout; cancellation current 0.904 A; filter 0.67 and 0.58 mm rms, probes 2.66 and 2.02 mm | verified (0.9043; 0.675, 0.578; 2.660, 2.022) |
| N116 | 12.10 key result | lean near one millimetre against 8.9 to 13.9 mm | verified |
| N117 | 13 | 2.6 %; 0.0105, about twice; about a fifth of the push | verified (15/82 = 0.18) |
| N118 | P2 | answers 19.9 swings and 19.3 s, for zeta = 0.0055 and w11 = 21.49 rad/s | wrong, because with the data the problem gives the answers are ln 2/(2 pi 0.0055) = 20.1 swings and ln 10/(0.0055 x 21.49) = 19.5 s; 19.9 and 19.3 follow only from the unrounded zeta = 0.005546 |
| N119 | P3 | R^{5/4}, 2.38 times | verified (2^1.25 = 2.378) |
| N120 | P5 | about 15 m/s^2 | verified (15.01) |
| N121 | P7 | j pi a_p/(2 w11); pi beta a_p/(2 w11^2) = 5.2 mm | verified (SymPy; 5.239) |
| N122 | P10 | 1.34 A | verified (1.338) |
| N123 | P11 | -2.0980 deg against -2.0990 deg; 0.99933 | verified (-2.09803, -2.09897, 0.999330) |
| N124 | P12 | 0.588; 0.991 | verified (0.5878, 0.9914) |
| N125 | 14 | quotes of sources [1]-[18] | unverifiable, because the sources were not read in this check |

## Statements of method

| # | Statement | Verdict |
|---|---|---|
| M1 | 1, 10: the page computes nothing physical; it plays stored pictures, checks fingerprints, round(30 T), no blend, readings as described, table click plays the ride | verified (`guinness-jax-play.js`; in headless Chrome all ten fingerprints match, the readings at the last frame equal the stored lists, e.g. kerb: 429.583 g, 2.44 mL, 345 drops and lumps, 0.60 A, 0.0 N) |
| M2 | 5.2: one fixed frequency 2 pi x 3.42 Hz; the stress rho sqrt(nu w/2) u_par on the glass area of each cell | verified (`OMEGA`, `friction`: u x exp(-gs a dt) with a = glass area per cell volume, integrated exactly over the step). Remark: the code brakes every face-velocity component in a cut cell, not only the part along the wall |
| M3 | 5.4: skin drag on the horizontal velocity of the top cells over one cell's area; absent without a head | verified (`skin` only in the "full" model; rate gs/dx on faces of the top liquid cells) |
| M4 | 6.3: tau_edge capped at tau_y + tau_v(v_s/2R32); sliding speed v_s e^{-kz'} through h_eff; abs(w) kept above 1 mm/s | verified (`head_wall_stress`, `heff`, `max(abs(ws), 1e-3)`) |
| M5 | 6.4: weight set to zero when g + a_z < 0; abs(g_eff,z) in the breaking rule; lumps fly until they land on the body or fall away | verified (`max(-gz, 0)` for the load and in `geff_dt`; `abs(gz)` in `head_spill`) |
| M6 | 6.6: head sheet on the top two cells, mass rho 2 dx, implicit, mu_f held below 0.05 /s, solved by conjugate gradients | verified (`head_sheet`: the correction goes on the two vertical faces of the top stout cell; 60 fixed CG iterations, which the note does not state) |
| M7 | 7.1, 7.3: grip clip +-mu_g N; road push -N z_a'; N >= 0; stout and head in M_x; F_n = -(P_n - P_{n-1})/dt_n booked and applied one step late | verified (`forces`, `make_advance`) |
| M8 | 8.1: two by two by two per cell, small random shift | verified (`seed_particles`, jitter 0.3 of the spacing) |
| M9 | 8.3: the ten steps and their order, frictions before gravity's kick | verified (`step`: prepare, viscosity, friction, kick, load, pressure, w_h, extrapolate 3 layers, g2p and move, head_spill) |
| M10 | 8.4: face weights, Jacobi-preconditioned CG on the pressure; head's mass in the pressure step; w_h set to the new face velocity | verified (`pressure`, `step`) |
| M11 | 8.5: level set, mirror images within two cells of the glass, two radii, highest zero in the top three cells, fallback 0.68 cell counted, capped columns left out, drop rule | verified (`level_set`, `surface`, `observe`) |
| M12 | 8.6: "the sums inside the conjugate gradients and the books of section 9 are kept in double precision" | wrong, because only the pressure CG sums in float64 (`dot` with `astype(F64)`); the head sheet's CG (step 4) sums `r * z` and `d * q` in float32. The books and the cart are float64 as stated |
| M13 | 9: four places for every particle counted in every stored picture; rest guard rules | verified (`nact + nfly + nlanded + nstuck`; `run_b.py` rest guard) |
| M14 | 10: "The largest lean and tilt in the table were read during the run from the surface before it was rounded for storage" | wrong, because they were read after the run, by `pack_ride.py`, from the run's unrounded heights restricted to the trusted columns; the run's own lean (`lean_max_mm_run`, from all columns) is different (for example 5.78 against 8.94 mm on the single bump). The size of the rounding effect (at most 0.02 mm) is right |
| M15 | 11.1: lean and tilt on the outermost ring, "at the radius R - dx/2", as the page reads the surface | wrong, because on that ring 28 of the 64 points have none of their four neighbouring columns among the trusted ones; the page's `atInward`, and `pack_ride.py`, then read them half a cell further in, at R - dx. The lean's two points (theta = 0 and pi) are read at R - dx/2; the tilt partly at R - dx |
| M16 | 11.2: free-swing fit from 0.1 s after the push, damped cosine plus a constant; w = sqrt(w_d^2 + 1/t_d^2), zeta = 1/(w t_d) | verified (`run_b.py` `fit_swing`; my refit of the stored files agrees) |
| M17 | 11.3: cart alone, pint frozen, speed loop every millisecond, sub-steps 0.1 ms, mean acceleration over each 2 ms step, then (13) | verified (my driver of the code's `Cart` reproduces every number of Table 4) |
| M18 | 12.2-12.8: controllers as described (PI with conditional integration; preview one lag ahead with the static load; slosh LQR on the filter estimate; joint adds (49) with the body's a_z, re-discretises A_d, B_d with w^2(1 + a_z/g), and the suspension LQR on (z_s, v_b, v_w, (N - N0)/k_t), clipped and lagged); filter predicts with the current measured at the last sample, corrects with the speed every sample and the probes at the first sample after a fluid step; probes at R - 2.5 dx and R - 4 dx extended to the wall; no noise | verified (`Cart.sample`, `observe`, `disc`, `probes`, `make_advance`) |
| M19 | 12.6: the stored controlled rides use w = 18.32, zeta = 0.425, beta_h = 1.241 | verified (run-10 summary plant: w 18.31699, zeta 0.42502, beta 1.24095) |
| M20 | 11.5 box and 14: every number printed by `note_numbers.py` | unverifiable, because I did not run it (by instruction); the numbers themselves are checked above |

## Counts

216 rows: 71 equations, 125 numbers or groups of numbers, 20 statements of method.

- verified: 195 (70 equations, 109 numbers or groups, 16 statements of method). Rows E29-E31, N21 and N29 are counted as
  verified: what they compute agrees with the code; the source each quotes was not read in this check.
- wrong: 13
  - E71 equations (23) and (31) are printed out of order
  - N56 the rides cost 43 to 48 s per simulated second, not 38 to 48
  - N75 the single bump does not break the head: 7.1 mm with the head is less than 7.6 mm
  - N76 the Floquet minimum is at 1.81 w (5.28 Hz), not 1.80 w (5.2 Hz); very flat, and epsilon 1.71 is right
  - N87 the early full current starts 29 ms before the touch, not 4 ms, and the sudden loss of speed is about 0.28 m/s, not 0.21
  - N88 so the first peak is about 11.2 mm, not 8.3 mm (19.0 mm, not 14.2 mm, before damping); the conclusion stands
  - N89 Figure 4's time zero is 25 ms before the rim first touches the kerb
  - N111 the first and fifth bumps give leans of 7.5 and 9.4 mm, not more than ten
  - N114 24.3 and 23.9 mm are the back-swing, not the first surge (the first surges are 22.2, 21.2, 21.8 and 25.4 mm)
  - N118 Problem 2: with zeta = 0.0055 the answers are 20.1 swings and 19.5 s
  - M12 the head sheet's conjugate gradients sum in float32
  - M14 the table's leans and tilts were read by `pack_ride.py` after the run, not during it
  - M15 28 of the 64 outer-ring points are read at R - dx, not R - dx/2
- unverifiable: 8 (N3, N6, N9, N28, N35 and N125: sources or calculations not available here; N77: only the last digit of the
  five-bump tilt; M20: `note_numbers.py` not run)

N87, N88 and N89 have one cause: the cart-alone experiment assumes that the rim touches the kerb when the axle is at
x = 1.40 m (the bump's start less the wheel's radius), but the rigid wheel rolling over the cosine bump first lifts at
x = 1.437 m. The key result of 12.3 and the caption of Figure 4 repeat the same numbers.
