# Fig. 12 (Kaggle) lecture note: check, round 0

Page checked: `public/simulations/guinness-kaggle.html`, `<article id="paper">` (as at commit 0f79231).
Checked against: `tools/fig12/kaggle/stout_jax.py`, `run_b.py`, `pack_ride.py`, `check_run.py`, `portcheck/`; the stored run
`public/data/fig12/2026-11-13-run8/` (index-jax.json and the ten ride files, all SHA-256 fingerprints match); run 6/7 files in
`public/data/fig12/2026-11-13/`; `notes/fig12/jax/run8-check/`. No other file in `notes/fig12/` was read.

How each thing was checked:
- Equations: re-derived in SymPy/mpmath (Laplace residual, boundary conditions, Bessel integrals, Stokes layer PDE, energy
  integrals, dispersion with a mass-loaded surface, ghost-fluid algebra, PI loop, Riccati (4,4) entry, cross-term LQR), plus units.
- Theory numbers: recomputed in Python from the formulas and the code's own constants (`CART_COMMON`, `HEAD0`, `GAMMA`, ...).
- Geometry and seeding: the code's own `Geometry` and `seed_particles` run on the glass table of `guinness-glass.js`.
- Cart numbers (Example 6.1, Figure 4, section 11.2): the code's `Cart` class run alone (JAX on CPU) with the pint frozen
  (F = 0, load 0.4544 kg), sub-steps of 0.1 ms.
- Controller numbers: the code's `slosh_lqr`, `susp_lqr`, `observer_design`; the Kalman covariance cycle iterated; the ten-state
  sampled loop composed exactly over one 2 ms cycle; Floquet multipliers of the damped Mathieu equation.
- Port check: `portcheck/cart_jax.py` (with `cart_js.cjs` under node) run on a scratch copy.
- Ride numbers: decoded from the stored ride files (zlib/base64, running sum of the height differences) and read as
  `pack_ride.py` and the page read them (outer ring at R - dx/2, 64 angles, bilinear, trusted columns only); free swings
  refitted with the run's own `fit_swing`.
- Playback: the page served locally and driven in headless Chromium (Chrome 153) over the DevTools protocol, run 8 files.
- One fluid step from rest: `Stout.step` run on CPU on the full 1.5 mm grid.

Scratch scripts and logs: `/tmp/claude-0/-home-user-SiteTest/912f9bc9-5665-53b0-8977-798ace78df59/scratchpad/`.

## A. Numbered (and key unnumbered) equations

| # | Item | Verdict |
|---|------|---------|
| E1 | (1) Navier-Stokes in the glass's frame, body force g - a_g | verified (translating frame, no rotation term needed; units m/s^2 throughout) |
| E2 | nu = mu/rho = 2.05e-6 m^2/s | verified (2.0457e-6) |
| E3 | (2) phi = cos wt cos th J1(kr) cosh kz | verified: SymPy Laplacian residual 0; d(phi)/dz = 0 at z = 0 |
| E4 | (3) J1'(kR) = 0, xi = 1.8412 | verified (first zero of J1': 1.841184) |
| E5 | (4) phi_tt + g phi_z = 0 at z = h | verified (kinematic + linear Bernoulli, eta eliminated) |
| E6 | (5) w^2 = (g xi/R) tanh(xi h/R) | verified (SymPy solve of (2) in (4)); limit h >> R gives width-only frequency, as stated |
| E7 | Bernoulli with glass acceleration (unnumbered) | verified (potential of g - a_g is a x + (g + a_z) z) |
| E8 | c1 = 2R/((xi^2-1) J1(xi)) and its two integrals | verified (mpmath quadrature equals R^3 J1/xi^2 and R^2/2 (1-1/xi^2) J1^2; c1 J1(xi) = 0.837 R) |
| E9 | modal equations q'/J1 = k tanh kh Q, Q' + (g+a_z) q/J1 + a c1 = 0 | verified (projection of kinematic and Bernoulli conditions) |
| E10 | (6) q'' + w^2(1 + a_z/g) q = -beta a, beta = 2 xi tanh/(xi^2-1) = 1.541 | verified (SymPy reduction; beta = 1.5407); sign (forward push lowers the front) correct; matches eq. (17) of beer-slosh.html |
| E11 | (7) Stokes layer u(y,t), delta = sqrt(2 nu/w) | verified (diffusion residual 0, u(0) = 0, u -> U cos wt) |
| E12 | (8) tau_w = rho sqrt(nu w/2) U (cos wt - sin wt) | verified; in-phase part removes (1/2) rho sqrt(nu w/2) U^2 per area, quadrature part does no work, and the dissipation integral through the layer gives the same (SymPy) |
| E13 | E = (pi rho B^2/4) k cosh kh sinh kh R^2 (1 - 1/xi^2) J1^2 | verified (surface form of kinetic energy; units J) |
| E14 | wall integral of u_th^2 + u_z^2 | verified |
| E15 | (9) sigma_wall, zeta_wall = (delta/4R)(xi^2+1)/(xi^2-1) | verified (SymPy, deep-glass limit); exact integrals at h = 125 mm give 0.11011 vs 0.11012 s^-1 |
| E16 | engineering form zeta = 0.5575 nu^1/2 R^-3/4 g^-1/4, K = 3.50 | verified (0.55751, K = 3.503) |
| E17 | (10) sigma_skin = sqrt(nu w/2)(k/2) coth kh | verified (SymPy, with the stated Green identity) |
| E18 | (11) p_L, G0, tau_y of Voelp and Willenbacher | unverifiable as a derivation, because it is an empirical law of [3] (source not opened here); the code implements it exactly (`P_GEN`, `G_HEAD`, `TAU_Y`) |
| E19 | (12) Tcholakova viscous stress | unverifiable as a derivation, because it is the fitted law of [8]; `foam_flow_stress` matches it term by term (Phi = 0.73, 1 - Phi = 0.27) |
| E20 | (13) implicit head sheet | verified for units (Pa both sides) and against `head_sheet` (mass rho 2 dx, implicit in w', mu_f from the old velocity, kappa = wall area per volume x h_eff x tau_edge/|w|) |
| E21 | (14) Cantat wall stress | unverifiable as a derivation, because it is the fit of [9]; `head_wall_stress` matches (Ca = mu v/gamma, cap at shear rate v/2R32) |
| E22 | h_eff = (3 ell/5)(1 - e^{-5 h_f/3 ell}) | verified (SymPy); thick-head limit 3 ell/5 (Problem 12.4); code `heff` = 0.6 ell (...) |
| E23 | (15) spill rule | verified as a balance (units Pa) and against `head_spill`, with the caveat in M14 |
| E24 | (15a) p_s = m_s (g_eff + dw/dt) | verified (Newton's law for a carried layer) |
| E25 | (15b) w^2 = g k tanh kh /(1 + m_s k tanh kh/rho) | verified (SymPy: kinematic + mass-loaded Bernoulli) |
| E26 | (16) F = -dP/dt; -F_gs = -m a_g - dP/dt + m g | verified (SymPy); code: `F = -(P - P_prev)/dt`, impulse book `imp += F dt` |
| E27 | (17) APIC transfers | verified against `p2g`/`g2p` (val = w (v + C.(x_j - x_p)), C = sum grad w u_j); form as in [11] |
| E28 | (18) ghost pressure p_g = p_l(1 - 1/alpha) + p_s/alpha, alpha >= 0.05 | verified (SymPy; code clips alpha to [0.05, 1]) |
| E29 | (18a) alpha -> alpha + m_s/(rho dx), p_s -> m_s(g_eff + (w* - w_h)/dt) | verified (SymPy: eliminating w' and p_s gives exactly this; code `tLR + muF/dx`, load `muF (geff_dt + w* - w_old)`) |
| E30 | (19) Zhu-Bridson level set | verified against `level_set` (kernel (1 - d^2/(2dx)^2)^3 within 2 dx, mirror images within 2 dx of the glass) |
| E31 | (20) E_p(0) - E_p(t) = E_k + D | verified (no external work with the glass held still) |
| E32 | (21) M_x v' = b i - c_x v + F_d, M_x incl. (I_w + N_g^2 J_m)/R_w^2 | verified (kinetic energy of the turning parts; code `massX`) |
| E33 | (22) current lag with clipping | verified against `Cart.forces`/`Cart.step` (clip to +-I_max, then to the voltage window; exact exponential over each sub-step) |
| E34 | (23) PI with integral xi | verified against `Cart.sample` (anti-windup: integrate only while |i_cmd| < I_max) |
| E35 | (24) M_x dv'' + (c_x + b K_p) dv' + b K_i dv = 0 | verified (SymPy); with K_i = K_p w_c/4, c_x = 0: double root -w_c/2 |
| E36 | (25) preview current | verified (first-order lag = delay to O(tau s); code reads the axle slope at x + v tau_i) |
| E37 | (26) A, B of the four-state model | verified (SymPy; equals `slosh_lqr`) |
| E38 | (27), (28) LQR cost and Riccati gain | verified (standard; code `solve_continuous_are`, K = B^T P/r) |
| E39 | |K4| = sqrt(Q44/r) = I_max/xi_m = 150 A/m | verified (SymPy: (4,4) entry of A^T P + P A is 0 because column 4 of A is zero) |
| E40 | (29) filter model z = (v, q, q') with G | verified (from (21) and (6) with b i0 = c_x v0; code `observer_design`) |
| E41 | (30) A_d, B_d, Q_d | verified (Van Loan Q_d equals direct quadrature to 3e-16 relative; B_d likewise) |
| E42 | (31) block exponential and F(t) | verified (derivative of e^{Mt}; Q_d = A_d F(T_s) as in the code) |
| E43 | (32), (33) predict/correct, Joseph form | verified (Joseph form equals (I - LH)C- to 1e-16 for the optimal gain; code `Cart.observe`) |
| E44 | one-number blend L = C/(C + sigma^2) | verified |
| E45 | heave equation with damping and (34) i_par = -(M_x w^2/(beta b))(a_z/g) q_hat | verified (SymPy); code `ipar` |
| E46 | quarter-car equations (unnumbered) | verified against `susp_lqr` A and B |
| E47 | (35) cost with cross term; completing the square | verified (SymPy difference 0) |
| E48 | (36) K_s = R^-1 (B^T P + N^T), Riccati with Gamma | verified (standard cross-term LQR; code `solve_continuous_are(..., s=N)`) |
| E49 | q_peak = (beta dv/w) e^{-zeta w t_p}, w_d t_p = atan(sqrt(1-zeta^2)/zeta) | verified (derivation; zeta -> 0 limit gives Example 3.2) |
| E50 | P_c = rho pi R^3/xi^2 (momentum of the mode per unit q') | verified (SymPy from P_x = rho closed-surface integral of phi n_x) |
| E51 | y_q = (eta_front - eta_back)/2 | verified (code `probes`: heights at R - 2.5 dx and R - 4 dx, extended linearly to R) |
| E52 | free-swing fit: w0 = sqrt(w^2 + 1/t_d^2), zeta = 1/(w0 t_d) | verified (exact for q = e^{-t/t_d} cos wt; code `fit_swing`) |
| E53 | parametric threshold eps = 4 zeta at Omega = 2 w | verified (first order; Floquet gives 0.0428 for zeta = 0.0107, = 4 zeta) |

## B. Numbers

### Sections 1-2 (glass, stout, head)

| # | Number | Verdict |
|---|--------|---------|
| N1 | R(z) table in 0.5 mm steps; floor R = 16.3 mm; widest 39.3 mm at 116 mm; rim 147.5 mm | verified (296 entries of `guinness-glass.js`) |
| N2 | catalogue 160 mm tall, 85 mm wide | unverifiable, because it is the catalogue's outer size, not in the code (inner widest diameter is 78.6 mm) |
| N3 | fill 125 mm, R = 39.1 mm; top 20 mm vary by 0.29 mm | verified (0.287 mm) |
| N4 | 426.6 mL, 429.6 g | verified (426.597 mL; 429.583 g, also in every ride's books) |
| N5 | head 19 mm; top at 144 mm, 3.5 mm below rim | verified |
| N6 | source values: rho 1007, mu 2.06 mPa s [1]; 1006, 2.03-2.23 [2]; 120 s [1]; head 18-20 mm, 17.5/20.6/22.2 mm [4]; 61 um [2]; gamma 44.2, E 18.7 mN/m [3]; Phi_c 0.635 | unverifiable, because quoted from the sources, which this check did not open; the code uses the same values |
| N7 | R32 = 34 um; liquid fraction 0.27 (from the project's research notes) | unverifiable, because derived in notes this check may not read; code uses 34e-6 and 0.27 |
| N8 | rho_f = 272 kg/m^3 | verified (271.9) |
| N9 | Table 1 line numbers "lines 33-57" | verified (constants at lines 33-57 of `stout_jax.py`) |
| N10 | Example 2.1: 50.7 Pa; d = 5.1 mm | verified (50.68 Pa; 5.13 mm) |
| N11 | 2217 columns, 91.31 mL, disc 91.26 mL, 24.8 g | verified (code `afill`: 2217, 91.314 mL; pi R^2 h_f = 91.255 mL; 24.83 g) |

### Section 3

| # | Number | Verdict |
|---|--------|---------|
| N12 | 1/k = 21 mm | verified (21.24) |
| N13 | xi h/R = 5.886, tanh = 0.99998 | verified |
| N14 | w^2 = 461.9 s^-2, w = 21.49 rad/s, f = 3.421 Hz, 0.292 s | verified (461.94, 21.493, 3.4207, 0.2923) |
| N15 | next modes kR = 5.331, 8.536; 5.821, 7.365 Hz | verified |
| N16 | 0.837 R | verified (0.8368) |
| N17 | beta = 1.541 | verified (1.5407) |
| N18 | 0.88 m/s^2 for 3.5 mm; 5.65 m/s^2 for 22.5 mm | verified (0.878; 5.645) |
| N19 | kick of 0.1 m/s: 7.2 mm | verified (7.17) |
| N20 | bumps 0.29 m apart at 1 m/s: 3.448 /s, 0.8 % above f11 | verified |

### Section 4

| # | Number | Verdict |
|---|--------|---------|
| N21 | w = 2 pi 3.42 = 21.49; delta = 0.436 mm (0.44), a third of a cell | verified (code `OMEGA`; 0.4363 mm = 0.29 cell) |
| N22 | sqrt(nu w/2) = 4.69 mm/s; 0.047 Pa at 10 mm/s | verified |
| N23 | sigma_wall = 0.110 s^-1, zeta_wall = 0.0051; exact integrals same to three digits | verified (0.11012, 0.005125; exact 0.11011) |
| N24 | side-wall factor 0.918 | verified |
| N25a | K = 3.50; 5.23 is 50 % more; zeta = 0.0077 with K = 5.23 | verified (3.503; 49 %; 0.00765) |
| N25b | Miles's K = 3.52 and the experiments' K = 5.23 [5]; Silveira and Abramson repeat both [6] | unverifiable, because quoted from [5] and [6], not opened here |
| N26 | zeta_skin = 0.0051 | verified (0.00514) |
| N27 | bulk 2 nu k^2 = 0.009 s^-1, zeta 0.0004 | verified (0.00907; 0.00042) |
| N28 | total zeta 0.0051 + 0.0051 + 0.0004 = 0.0107 | verified (0.01068) |
| N29 | 1/(zeta w11) = 4.4 s; halves in 10 swings | verified (4.35 s; 10.3 swings) |

### Section 5

| # | Number | Verdict |
|---|--------|---------|
| N30 | marbles jam at about 64 %; bubbles fill 73 % | verified (1 - 0.27; random close packing ~0.64) |
| N31 | p_L = 2400 Pa; Phi - Phi_c = 0.095; G0 = 166 Pa; tau_y = 5.4 Pa; a tenth of the weight | verified (2400; 166.44; 5.415; 0.107) |
| N32 | gamma_dot = 10 /s: Ca = 1.6e-5; films 7.5 Pa; corners 4.2 Pa; tau_v = 11.7; tau = 17.1 Pa | verified (1.585e-5; 7.47; 4.25; 11.72; 17.14) |
| N33 | Tcholakova fits cover Phi >= 0.80 | unverifiable, because it is a statement about [8] |
| N34 | dx = 1.5 mm; rho 2 dx = 3.0 kg/m^2 | verified (3.02) |
| N35 | mu_f held below 0.05 /s at 123 Pa s | verified (`eta`: 122.8 Pa s) |
| N36 | yield balance q = 0.019 x 5.4 x 47.1/(1007 x 9.81) = 0.5 mm | verified (0.49) |
| N37 | Z = 0.18, l/r_m = 0.004 at liquid fraction 0.25, held at 0.27 | verified against the code (`np.interp` clamps at the 0.25 table values; the table values themselves are quotes of [9]) |
| N38 | (14) gives 2.1, 9.7, 28, 45 Pa at 1, 10, 50, 100 mm/s; cap 20 to 223 Pa | verified (2.10, 9.66, 28.2, 44.7; cap 19.9-223.3) |
| N39 | ell = R/xi = 21.2 mm; h_eff = 9.9 mm | verified (21.24; 9.87) |
| N40 | 50.7 Pa at rest | verified |
| N41 | eps* = 4.1 mm; 3.5 + 4.1 = 7.6 mm; 2.0 mm at 5 m/s^2; stout at 22.5 mm, three times higher | verified (4.06; 7.56; 2.01; 22.5/7.6 = 3.0) |
| N42 | m_s = 5.17 kg/m^2 | verified (5.166) |
| N43 | k = 47.1 /m; rho/k = 21.4 kg/m^2; m_s k/rho = 0.24; 1/sqrt(1.24) = 0.897; 3.421 -> 3.07 Hz | verified (47.09; 21.38; 0.2416; 0.8975; 3.070) |
| N44 | Sauret: 3.1 Hz against 3.3 Hz | unverifiable, because quoted from [10] |

### Section 6

| # | Number | Verdict |
|---|--------|---------|
| N45 | cart: 1.5 kg, 600 N/m, 8 N s/m, 0.3 kg, 40 mm, 20 kN/m, 10:1, 5 N/A, 3 A, 1 ms | verified (`CART_COMMON`; b = N_g K_m/R_w = 5) |
| N46 | Table 2 roads, speeds, durations; bumps from 1.5 m, cart from 0.5 m; push 1.0 m/s^2 sin(pi t'/0.146 s) from 0.3 s | verified (`ROADS`, `TASKS`, `make_advance`, `ride_extra`) |
| N47 | push lasts half a period of the first mode | verified (pi/w11 = 0.1462 s) |
| N48 | the cart feels the push one step, about 2 ms, late | verified (`ex["F"]` from the previous fluid step) |
| N49 | impulse check to one part in a thousand | verified (`check_run.py` tolerance 1e-3 relative + 1e-7) |
| N50 | Example 6.1 five bumps: 1.6 m/s^2; g + a_z from -0.7 to 20.0; 45 mm | verified (1.642; -0.670 to 19.953; 45.3 mm) |
| N51 | kerb: 28.8 m/s^2; speed 1.50 -> 1.21; -2.4 to 20.6; 24 mm | verified (28.80; 1.520 -> 1.207; -2.41 to 20.61; 23.7 mm) |
| N52 | one 25 mm bump: 1.0 m/s^2; 1.5 to 17.6; 8.5 mm | verified (1.041; 1.54 to 17.64; 8.54 mm) |
| N53 | 45 mm twice the 22.5 mm; kerb stops the cart by 0.29 m/s | verified (0.31 m/s from the 1.52 peak, 0.29 from 1.50) |

### Section 7

| # | Number | Verdict |
|---|--------|---------|
| N54 | 57 x 57 x 114 = 370,386 cells, 1.5 mm | verified (`Geometry`) |
| N55 | 1,001,952 particles; 126,399 cells' worth; 7.93 per cell; 0.429 mg; 0.93 mm | verified (`seed_particles`: 1,001,952; 126,399.2; 7.927; 0.42875 mg; 0.933 mm) |
| N56 | nu dt/dx^2 = 0.0018, limit 1/6 | verified (0.00182) |
| N57 | CG tolerance 1e-5 of the largest right side, at most 600 iterations | verified (`tol`, `maxit`, max-norm test) |
| N58 | run 3 at rest: 90 iterations per step on average, 226 at most | unverifiable, because run 3's data are not among the stored files |
| N59 | m_s/(rho dx) = 3.4 | verified (3.42) |
| N60 | shortest wave k = pi/dx: m_s k/rho = 10.7 | verified (10.74) |
| N61a | 6 mm test: k = 35.2 /m from 2.958 Hz; prediction 2.722 Hz; 2.737 Hz is 0.5 % above | verified (35.21; 2.7223; 0.54 %) |
| N61b | 6 mm test measured 2.958, 2.737 and 2.905 Hz, a swing a third as large; 4 mm rest test 59 and 61 uJ | unverifiable, because those CPU runs are not stored |
| N62 | weighted mean 0.505 dx below the top (0.5054 dx) | verified (0.5054 dx with layers h apart; 0.5053 dx with the code's hz = fill/167) |
| N63 | 40 positions: r0 = 0.505 dx reads 0.001 to 0.063 cell low; r0 = 0.9 dx reads 0.52 to 0.56 cell (0.8 mm) high | verified (-0.063 to -0.001; +0.521 to +0.558). Note the code comment in `Stout.__init__`/`surface` states a different range (-0.09..+0.02 cell); the note's numbers are the ones reproduced here |
| N64 | fallback: body's top less 0.68 cell | verified (`surface`) |
| N65a | tulip widest at 116 mm (39.3 mm) | verified |
| N65b | run 4 read edge columns at 120 mm, 5 mm low; 84 dark dots | unverifiable, because run 4 is not stored |
| N66 | drop rule: more than 1.5 dx above its column and the eight around | verified (`observe`) |
| N67 | dt = 2 ms, shorter when a particle would cross 0.8 cell; 16 steps of 2 ms + one of 1.33 ms; 17 steps per picture | verified (`make_advance`; 1020/2040/2550/4080 steps per 2/4/5/8 s in the summaries = 17 per picture) |
| N68a | cart sub-steps 0.1 ms; float32 fluid, float64 CG sums, books and cart | verified (code) |
| N68b | the T4 is 32 times slower in double precision | unverifiable, because it is a hardware datum not in the repository (the code comment says the same) |
| N69 | run 3: 72.6 ms per step | unverifiable, because run 3 is not stored |

### Section 8 (pint at rest)

| # | Number | Verdict |
|---|--------|---------|
| N70 | gravity's kick dt g = 19.6 mm/s | verified (19.62) |
| N71 | guard limits 0.75 mm, 0.375 mm, no loss | verified (`run_b.py` `REST_MAX_CELLS`, `REST_RMS_CELLS`) |
| N72a | 1977 columns more than one cell inside the glass | verified (code geometry, and 1977 trusted columns in every stored ride file) |
| N72b | run 3: 4.62 mm worst, 0.484 mm rms, 108 columns off | unverifiable, because run 3 is not stored |
| N73 | Table 3 and Figure 3 (run 3 books at 0.1/0.5/1/2 s; 629, 3, 774, 626 uJ; 648 of 774; 0.15 mm sinking) | unverifiable, because run 3's stored data are not among the files available here; internal arithmetic checks (629 - 3 = 626; 10.4 + 0.8 + 46.3 = 57.5; 102.0 + 23.2 + 648.5 = 773.7) hold |
| N74 | head on 2129 columns, 88 more at the edge | verified (code geometry: 2129 centres inside at the fill; 88 more with an open face) |
| N75 | 50.7 Pa over 1.5 mm = 34 kPa/m, 3.4 times rho g; equilibrium 5.1 mm higher | verified (33.8 kPa/m; 3.42; 5.13 mm) |
| N76 | run 3's code, one step from rest: 30.3 mm/s, 0.2 mm below the surface | unverifiable, because run 3's code was not rerun (commit not named) |
| N77 | fixed code, one step from rest: 0.76 mm/s at the corner, same as `inviscid` | verified (rerun on CPU, full 1.5 mm grid: fixed code without the head's mass 0.757 mm/s at r = 38.6 mm, z = 124.8 mm; `inviscid` 0.757 mm/s at the same particle). With run 8's code (head's mass) the full model gives 0.18 mm/s |
| N78 | first 0.1 s: run 3's code 2.3, 0.37, 57.2 uJ vs T4 2.4, 0.32, 57.5 | unverifiable, because run 3's code was not rerun and its T4 data are not stored |
| N79 | first 0.1 s, fixed code: 0.27, 0.005, 0.033 uJ; 1700-fold; settle 0.06 um; 0.04 uJ appear | verified by rerunning the fixed code (run 8's `Stout` with `head_mass=False`, full 1.5 mm grid, CPU) for 0.1 s from rest: potential energy lost 0.269 uJ, kinetic 0.0051 uJ, booked 0.0324 uJ (glass 0.0010, skin 0.0048, head 0.0266); motion plus heat 0.037 uJ (the note's 0.04); 57.5/0.0324 = 1770-fold (about 1700); mean settling 0.067 um. The note's 0.033 uJ and 0.06 um differ from this rerun in the last digit, within float32 scatter between machines |

### Section 9 (playback)

| # | Number | Verdict |
|---|--------|---------|
| N80 | 57 x 57 columns; steps 0.02 mm (diff-coded), 0.1 mm, 0.1 mm, 0.1 mm^3; SHA-256 per file | verified (`pack_ride.py`; all 10 fingerprints and sizes match the index, also checked by the page in Chromium: 10 of 10) |
| N81 | clock advances by real time, at most 0.1 s; frame round(30 T); no blend; stops at the end | verified (code `tick`; headless Chromium, run 8 default ride: 570 of 570 sampled frames had k = round(30 T); clock 1.0000 s per s; stopped at T = 8.00 s on picture 241 of 241) |
| N82 | "152 to 174 sampled pictures" of an earlier run | unverifiable, because those were samples of an earlier run's files; the same property holds on run 8 files (N81) |
| N83 | words changed 11 times in 3 s (at most four per second) | verified (re-measured: 11 changes in 3 s; code rewrites after more than 250 ms) |
| N84 | stout reading 0.429 mg per particle, shown to 1 mg; head in glass summed on the GPU | verified (`fmt(stout_g, 3)` g; `vhead` in `observe`) |
| N85 | four particle counts add up to 1,001,952 | verified (books: largest error 0 particles in every task) |
| N86 | mesh 14 rings x 96 angles; head fades below 1.5 mm; drops 1.1 mm radius; lumps balls of their volume | verified (`stout-view2.js`: nr = 14, nth = 96, hfm/0.0015, 0.0011, cbrt(3V/4pi)) |

### Section 10 (results)

| # | Number | Verdict |
|---|--------|---------|
| N87 | expectations 3.421 Hz; 0.897; about 3.07 Hz; zeta 0.011; 0.5 mm; 7.6 and 22.5 mm; 45, 24, 8.5 mm | verified (as above) |
| N88 | ring r = (13/16)(R - dx/2) = 31.2 mm; q_ring = (2/64) sum eta cos th | verified (31.16 mm; code `polar`, `q13`) |
| N89 | undamped push: 5.2 mm at the wall, 5.0 mm on the ring | verified (5.24 mm; J1 ratio 0.9506: 4.98 mm) |
| N90 | run 8: 9 tasks, 2285 s; commit 96e8a1d, version 8; preview version 9, commit 726d51a; run 6 version 6, commit 4c10527 | verified (sum of run_s + compile_s = 2285.2 s; index entries) |
| N91 | budget 2500 s | unverifiable, because the notebook cell sets `BUDGET_S` from a placeholder (`__BUDGET__`) and the run's value is not stored (the script default is 2450) |
| N92 | books: 1,001,952 particles; 91.314 mL served, to within 1.3e-8 mL | verified (largest head-book error 1.257e-8 mL, kerb with slosh regulator) |
| N93 | rest: within 0.50 mm in all 1977 columns; 0.129 mm rms; no fallback; nothing lost | verified (rest guard: 0.4978 mm, 0.1292 mm, fallback 0) |
| N94 | rest books after 2 s: 25.7, 0.34, 8.1 uJ (0.34, 3.92, 3.87); 17.3 uJ to the method | unverifiable, because the rest task's per-picture books (rest.npz) are not among the stored files; the summary keeps only E_k + E_p at 0 and 2 s (`energy_J`), whose change, -25.4 uJ, agrees with 25.7 - 0.34 = 25.36 uJ. A CPU rerun of 2 s was started and stopped (about 165 s per picture, some 3 h); 25.7 - 0.34 - 8.1 = 17.3 holds |
| N95 | run 6 rest books 24.5, 0.33, 8.4 uJ | unverifiable, because run 6's rest task is not among the stored files |
| N96 | no head (run 6): "rings at 3.331 Hz", natural frequency 3.331 Hz | wrong, because the fit gives a ringing frequency of 3.3302 Hz, i.e. 3.330 Hz (run 6 index and my refit of the stored file: f = 3.33022, f0 = 3.33065); the natural frequency 3.331 Hz is right |
| N97 | 2.6 % below 3.421 Hz; zeta 0.0160; 0.0051 + 0.0004 = 0.0055; method adds about 0.0105, twice the physics; 4.63 mm vs 5.0 mm | verified (2.64 %; 0.01601; 0.0105 = 1.9 x 0.0055; A = 4.625 mm) |
| N98 | with head: rings 2.639 Hz, decays in 0.128 s, natural 2.915 Hz, zeta 0.425 | verified (run 8 summary: 2.6388, 2.9152, 0.4250; t_d = 0.1284 s. A refit of the stored page file, rounded to 0.02 mm and trusted columns only, gives 2.640, 2.917, 0.4252, 0.128 s) |
| N99 | k = w^2/g = 44.7 /m on the 3.331 Hz grid | wrong, because (2 pi x 3.3306)^2/9.81 = 44.64 /m, i.e. 44.6 /m (44.65 even with 3.331 Hz); m_s k/rho = 0.229 and the factor 0.902 are right |
| N100 | 0.229; 1/sqrt(1.229) = 0.902; run 6 with weight only 3.278 Hz; expected 2.957 Hz; 2.915 is 1.4 % lower | verified (0.2290; 0.9020; refit of run 6's stored file 3.2776 Hz; 2.9568 Hz; 1.41 %) |
| N101 | e-folding in about a third of a period, gone within one | verified (0.128 s vs period 0.343-0.379 s) |
| N102 | after 1.5 s cos th part -0.03 mm (-0.05 to -0.01) | verified (stored file: mean -0.028, range -0.048 to -0.006 mm) |
| N103 | five bumps, speed loop: tilt 13.6 mm (Table 4, Table 8, section 10 "never passes 13.6 mm", section 11.9 "tilts 13.6") | wrong, because the stored file gives 13.54 mm, i.e. 13.5 mm; 13.6 comes from the run's unrounded heights (index `tilt_max_mm` 13.55), not from the stored data the captions name |
| N104 | Table 4 five bumps: lean 13.9; head 0.01 mL from 1.50 s; no stout; speed 0.943-1.051; 84.1 ms, 138 iterations | verified (13.88; 0.0097 mL, first in picture 45 = 1.50 s; 0.9435-1.0513; 84.1 ms, 137.6) |
| N105 | Table 4 kerb: tilt 22.2, lean 24.3, head 2.44 mL from 0.67 s, no stout, 1.211-1.517 m/s, 88.5 ms, 133 iterations | verified (22.23; 24.26; 2.445 mL; picture 20 = 0.667 s; 1.2110-1.5171; 88.5; 133.2) |
| N106 | Table 4 one bump: tilt 8.0, lean 8.9, nothing spilled, 0.962-1.036, 86.1 ms, 151 iterations | verified (7.96; 8.94; 0.9623-1.0356; 151.3) |
| N107 | Table 4 run 6 brackets: 15.1/17.3; 27.6/34.1/4.08 mL; 9.0/10.6 | verified from run 6's stored files (15.08/17.34; 27.64/34.08/4.079; 9.04/10.64) |
| N108 | run 6 kerb stout 0.008 g | unverifiable, because run 6's file stores the spill only to 0.01 g (it reads 0.01 g; 0.008 g would round to it) |
| N109 | rides: 90 mm lean without friction; 0.31 m/s loss; 345 lumps; impulses 2.0e-6, 2.3e-6, 1.6e-6 N s | verified (2 x 45; 1.517 - 1.211 = 0.306; 345 lumps in the last picture; 2.04e-6, 2.31e-6, 1.58e-6) |
| N110 | head's mass: lean -20 % (five bumps), -16 % (one bump), -29 % (kerb); head spill 40 % less | verified (0.801, 0.840, 0.712; 2.44/4.08 = 0.60) |
| N111 | 11 % slower, 2.915 vs 3.278; bumps 3.4 /s; 1 + m_s k/rho = 1.24; beta/(1 + ...); wall 1/sqrt(1.24), about 10 % less | verified (0.889; 0.897) |
| N112a | 101 iterations a step at rest; ride steps 83-89 ms (run 8) against 79-93 ms (run 6) | verified (101.5; 82.8-88.5; 78.6-93.1) |
| N112b | 44 iterations a step at rest in run 6 | unverifiable, because run 6's rest task is not stored |

### Section 11 (controllers)

| # | Number | Verdict |
|---|--------|---------|
| N113 | b = 5 N/A; T_s = 1 ms | verified |
| N114 | Example 11.1: m_l = 0.4544 kg; 0.150 + 0.125 = 0.275 kg; M_x = 2.529 kg; 15 N; 5.93 m/s^2; e = 7.5 V; 2.25 A, 11.25 N, 4.45 m/s^2; 9.75 A; i0 = 0.6 A; N0 = 22.1 N; grip 17.7 N; 18.75 N | verified (all) |
| N115 | kerb slope pi h_b/L = 0.785 | verified (axle path max slope 0.7853) |
| N116 | tyre load 105 N; two blows within 44 ms, 82 N and 24 N; 20 ms above 15 N | verified (104.9 N; 82.3 and 24.1 N; 43.1 ms; 20.4 ms) |
| N117 | wheel leaves the road six times, 92 ms, in the next 0.17 s | verified (six spells, 91.9 ms, last ending 0.167 s after the first blow) |
| N118 | speed loop asks 8.0 A; current reaches 2.98 A; 1.50 -> 1.21 m/s | verified (8.04 A; 2.977 A; 1.207 m/s; the stored run: 8.006 A command, 2.984 A) |
| N119 | full forward current from 4 ms before the climb: speed falls to 1.23 m/s | verified (1.227 m/s) |
| N120 | no-lag bound min(b i_max(v), mu N) over the 44 ms still loses 0.25 m/s; dv = 0.2515 m/s used below | unverifiable, because the note does not say how the bound was run; two reconstructions with the code's cart (motor at min(b i_max(v), mu N) during the 44 ms of the two blows, speed loop otherwise; or that force integrated along the speed-loop trajectory) give 0.264-0.265 m/s, not 0.2515. "At least 0.25 m/s" (key result) holds |
| N121 | w = 18.32 rad/s, w_d = 16.58, t_p = 1.132/16.58 = 68 ms; 1.541/1.242 = 1.241; 17.0 mm; e^-0.531 = 0.588; q_peak = 10.0 mm | verified from dv = 0.2515 (17.04 mm; 0.5878; 10.02 mm); with my 0.264 m/s, 10.5 mm. Either way above 7.6 mm |
| N122 | 82 N five times the motor; a fifth of the push (section 12) | verified (5.5; 0.18) |
| N123 | w_c = 2 pi 8 Hz; M_x = 2.505 kg; K_p = 25.18, K_i = 316.4 | verified (2.5046 kg; 25.1788; 316.406; equal to `CART_COMMON`) |
| N124 | with the head 1 % heavier; 7.92 Hz; roots -21.6 and -29.0 /s | verified (7.921; -21.58, -28.98) |
| N125 | Example 11.2: 25.18 - 17.27j; 2 + 46.33j; L = -1.744 - 2.793j; 2.890; 0.346; with lag and half sample 0.352; 35 % | verified |
| N126 | preview 3 mm ahead; slopes 0.251 and 0.262; 1.16 A; 3.47 A; 105 N; 82 N worth 16 A | verified (axle path slopes 0.2513, 0.2618; 1.158; 3.47; 16.4) |
| N127 | Bryson limits 0.05 m/s, 2 mm, 2 mm w, 2 cm, 3 A | verified (`slosh_lqr`) |
| N128 | |K4| = 150 A/m | verified (-150.000) |
| N129 | plant 2.915 Hz, w = 18.32, zeta = 0.425, beta = 1.541 | verified (summary `plant`) |
| N130 | with beta = 1.241: K = (71.12, -1228.72, -40.50, -150.00), within 10 % | verified (71.12, -1228.72, -40.50, -150.00; largest change 9.7 %) |
| N131 | Example 11.4: K = (74.00, -1295.01, -44.87, -150.00); 7.4 A; +1.30 A; 0.45 A; 1.5 A | verified |
| N132 | open-loop pair -7.79 +- 16.58j, 2.64 Hz; closed -10.82 +- 4.61j, zeta 0.92; -2.62; -275 | verified (-7.785 +- 16.580j; -10.820 +- 4.605j; 0.920; -2.616; -275.0) |
| N133 | bare stout design K = (74.96, -1927.1, -38.86, -150.0); decay 0.23 -> 12.0 /s, 52 times; with the head 39 % | verified (74.96, -1927.05, -38.86; 0.230 -> 12.01; 52.2; 10.82/7.79 = 1.39) |
| N134 | Key result "the head already decays it at 9.6 s^-1, and the regulator adds 29 %" | wrong, because with run 8's plant the head decays the swing at zeta w = 0.425 x 18.32 = 7.79 s^-1 and the regulator takes it to 10.82 s^-1, adding 39 % (as the paragraph above says); 9.6 s^-1 is run 6's plant (0.467 x 2 pi 3.278 = 9.62) |
| N135 | probes at R = 39.1 mm; R - 2.5 dx and R - 4 dx | verified |
| N136 | W_F = 0.5 N^2 s (0.22 N s in 0.1 s); W_a = 0.002 m^2 s^-3 (about 0.025 m/s per swing); sigma_v = 2 mm/s; sigma_q = 0.8 mm | verified (0.224; 0.026 m/s over 0.343 s) |
| N137 | Example 11.5: L = [[0.953, -0.0047], [-0.0008, 0.060], [-1.456, 0.926]]; 9.5 and 14.6 mm/s, 1.53; 0.060 mm and 0.93 mm/s; 17 readings, 33 ms; 2.0 mm/s, 0.20 mm, 7.1 mm/s | verified (L = [[0.9534, -0.00470], [-0.00075, 0.0603], [-1.4556, 0.9265]]; 1.527; 16.6; 33.2 ms; 1.95, 0.196, 7.12) |
| N138 | ten-state loop: largest eigenvalue 0.9948; swing -10.79 +- 4.61j; filter -23.3 +- 27.4j; lag -207 +- 304j; probes 1 ms early -10.76 +- 4.55j; under 1 % | verified (0.99477; -10.79 +- 4.61j; -23.34 +- 27.38j; -206.6 +- 304.0j; -10.76 +- 4.55j; 0.3 % and 0.6 %) |
| N139 | M_x w^2/(beta b) = 2.529 x 424.2/(1.541 x 5) = 139.3 A/m; 0.71 A for 5 mm at 10 m/s^2 | wrong, because 424.2 s^-2 is run 6's plant (2 pi x 3.278 Hz)^2; with the plant of this design (w = 18.32 rad/s, w^2 = 335.5 s^-2) the factor is 110.2 A/m and the example 0.56 A |
| N140 | parametric threshold bare 0.42 m/s^2 at 6.84 Hz; with head eps = 1.71 at 1.81 w, 16.8 m/s^2 at 5.3 Hz | verified (0.420; 6.842; Floquet: 1.709 at 1.81 w, 16.77 m/s^2, 5.28 Hz) |
| N141 | roads shake by +-8 to +-12 m/s^2 | verified (a_z from Example 6.1: -8.3..+7.8, -10.5..+10.1, -12.2..+10.8) |
| N142 | k = 600, c = 8, k_t = 20 kN/m, c_t = 5; a_m 0.5, s_m 10 mm, delta_m 0.2 mm, u_m 40 N; static tyre compression 1.1 mm | verified (1.106 mm) |
| N143 | Example 11.6: M_s = 1.954 kg; gains -501.22, 11.92, -6.34, 630.00; 84 %; 99 N/m; body -1.93 +- 17.17j (2.75 Hz, 0.11) -> -4.93 +- 4.98j (1.12 Hz, 0.70); wheel 41.7 Hz, 0.08 -> 0.12 | verified (all; 1.115 Hz, 0.704; 41.68/41.69 Hz, 0.083 -> 0.124) |
| N144 | active force clipped +-40 N, lag 5 ms | verified (`Umax`, `tauU`) |
| N145 | Table 6 limits and clocks | verified (each row against `CART_COMMON`, `Cart`, `make_advance`) |
| N146 | port check: 454.5 g; y_q = 4 mm sin wt e^{-t/2 s}; 3 s every 2 ms; speed, preview, skyhook to 4e-13 A; slosh and joint 3e-8 A current, 6e-8 A command; gains differ in the 7th digit; Ks 630.06 at 454.5 g vs 630.00 at 454.4 g, others < 0.01 | verified (rerun: 3.6e-13 A current and 4.2e-13 A command; 2.3e-8/3.3e-8 A; 6.3e-8/6.4e-8 A; -1206.6987 vs -1206.6986; 630.061 vs 630.004; others differ by 0.005, 0.001, 0.001) |
| N147 | one-mode model: P_c = rho pi R^3/xi^2 = 0.0558 kg | verified (0.05578) |
| N148 | Table 7, five bumps: speed loop 10.3 mm; slosh 1.2 mm; joint 1.0 mm, 1.73 A; stroke 8.4 vs 3.3 mm rms; heave of the joint design +-2.4 m/s^2; cancellation current below 0.02 A | verified with my reconstruction of the model described in 11.9 (10.30; 1.19; 1.00 mm, 1.71 A; 8.35 vs 3.32 mm; -2.39..+2.30; 0.011 A) |
| N149 | Table 7, remaining entries (preview 1.9 mm/2.24 A, slosh 2.41 A, speed 2.46 A on five bumps; all kerb entries 23.4/22.3/22.9/23.8 mm, 2.99/2.95/2.98/2.94 A; one bump 7.3/1.6/1.2/1.1 mm, 2.01/1.88/1.91/1.77 A); heave +-10.5 m/s^2 under the speed loop | unverifiable, because the one-mode coupling code is not in `tools/fig12/kaggle/` and the description leaves details open; my reconstruction (cart of the code, 2 ms steps cut to the frames, exact swing over each step, push -P_c dq'/dt one step late) gives five bumps preview 2.07 mm/2.25 A, slosh 2.35 A, speed 2.40 A; kerb 20.5/19.5/20.1/22.8 mm, 2.98/2.95/2.97/2.93 A; one bump 7.42/1.68/1.19/1.11 mm, 2.00/1.84/1.83/1.64 A; heave -10.25..+9.67 m/s^2. Closest matches are on the gentle roads; the kerb leans differ by up to 3 mm |
| N150 | kerb: command at or beyond 3 A in 4 to 6 pictures (model) | verified (reconstruction: 6, 6, 6, 5) |
| N151 | lean 22 mm = wall rise 11 mm > 7.6 mm | verified |
| N152a | Table 8, five bumps joint: tilt 0.89 mm | verified (0.892) |
| N152b | Table 8 and text, five bumps joint: lean 0.95 mm | wrong, because the stored file gives 0.94 mm; 0.95 is the run's unrounded value (index `lean_max_mm`), while the caption says "read from the stored files" |
| N153 | Table 8, five bumps joint: no spill; 1.71 A; 0 pictures at 3 A; 7.1 N | verified (1.708 A; 7.063 N) |
| N154 | Table 8, one bump joint: tilt 0.93, lean 0.76; 1.64 A; 0; 7.9 N | verified (0.931; 0.760; 1.640; 7.925) |
| N155 | Table 8, kerb: speed 22.2/24.3/2.44/2.98/6; preview 22.7/21.2/2.46/2.95/6; slosh 20.8/21.8/1.65/2.97/5; joint 24.5/25.4/2.00/2.93/5/11.4 N; no stout | verified (22.23/24.26/2.445/2.984/6; 22.70/21.18/2.463/2.950/6; 20.80/21.84/1.654/2.971/5; 24.54/25.38/1.995/2.929/5/11.45) |
| N156 | gentle roads: 1.0 and 1.1 mm predicted; fifteen and twelve times less; 0.011 A cancellation | verified (13.89/0.95 = 14.6; 8.94/0.76 = 11.8; 0.0113 and 0.0100 A) |
| N157 | filter vs probes rms 0.03 mm on both gentle roads; probes 0.17 and 0.13 mm | verified (0.033, 0.031; 0.166, 0.132) |
| N158 | run's own lean 5.4 mm on the single bump with joint control | verified (index `lean_max_mm_run` 5.39) |
| N159 | run 7: 1.05 and 0.89 mm | wrong, because run 7's stored files give 1.06 and 0.90 mm; 1.05 and 0.89 are the unrounded values in that index |
| N160 | kerb: 5 or 6 pictures at the limit; filter vs probes 0.75 (joint), 0.67 (slosh), probes 2.7 and 2.1 mm | verified (0.748, 0.674; 2.69, 2.11) |
| N161 | Key result: near 1 mm vs 8 to 14 mm; 15 N; 1.7, 2.0 vs 2.4 mL | verified |

### Section 12 and problems

| # | Number | Verdict |
|---|--------|---------|
| N162 | wedge of foam: twice the height, 8.1 mm at rest | verified (Culmann/Rankine H_c = 4 c/gamma vs 2 tau_y/(rho_f g): factor 2; 8.12 mm) |
| N163 | drop 0.43 mm^3 | verified (0.426 mm^3) |
| N164 | 12.2: 10.3 swings; 10.0 s | verified (10.31; 10.01 s) |
| N165 | 12.3: R^{5/4}, 2.38 times | verified (2.378) |
| N166 | 12.5: about 15 m/s^2 | verified (15.0) |
| N167 | 12.7: integral pi/(2w); A = 5.2 mm | verified (SymPy; 5.24 mm) |
| N168 | 12.9: 1.36 A | wrong, because with the design's w = 18.32 rad/s the factor is 110.2 A/m and 110.2 x (12/9.81) x 0.008 = 1.08 A (1.36 A uses run 6's 3.278 Hz) |
| N169 | 12.10: -2.0980 deg against -2.0990 deg; 0.99933 | verified with the unrounded f0 = 2.9152 Hz (-2.09803, -2.09897; with 2.915 Hz exactly the last digits are -2.0979 and -2.0988); magnitude 0.99933 |
| N170 | 12.11: 0.588; 0.983 | verified (0.5878; 0.9834) |

## C. Description of the method against the code

| # | Statement | Verdict |
|---|-----------|---------|
| M1 | 7.2 order of one step: p2g, level set and heights, viscosity, thin layers, gravity kick, head weight and mass, pressure, extrapolation 3 cells, g2p and move, head break | verified (`Stout.step` with `prepare`: exactly this order; the head's velocity w_h is updated right after the pressure step) |
| M2 | 7.2 step 4: glass drag u -> u e^{-sqrt(nu w/2) lambda dt}, skin drag on top cells, head sheet; each booked | verified (`friction`) |
| M3 | 7.2 step 9: particles crossing the glass put back; crossing the rim outside the radius become drops | verified (`g2p`) |
| M4 | 7.3 cut-cell face weights, CG with diagonal preconditioner, tolerance, 600 iterations | verified (`pressure`) |
| M5 | 7.3 ghost fluid (18), alpha >= 0.05, and (18a) Robin form; w_h kept per column and set to the new velocity of the face the surface crosses | verified |
| M6 | 7.4 level set: two radii, body top from 0.9 dx, highest zero of 0.505 dx field in the body's top three cells, fallback 0.68 cell counted; capped columns left out; drop rule | verified (`surface`, `observe`) |
| M7 | 7.5 time step and frames | verified (`make_advance`) |
| M8 | 5.3 head sheet solved by conjugate gradients on the columns | verified (60 fixed CG iterations, `head_sheet`; the note does not give the count) |
| M9 | 5.4 kappa = tau_edge h_eff/|w| times glass length per column area; v_s = |w| | verified (`acs * heff * head_wall_stress(ws)/max(|ws|, 1e-3)`; the 1 mm/s floor is not mentioned) |
| M10 | 6 effective gravity from the glass's acceleration averaged over the step; cart mass includes stout and head | verified (`ax = (vx - vx0)/dt`; `ml = rho V nact/N + mhead` after each step) |
| M11 | 6 impulse book and one-step lag | verified |
| M12 | 4.1, 4.3 drags as in-phase Stokes stress on cut-cell glass area and on top cells over one cell's area | verified (`gs * af`, `gs/dx`) |
| M13 | 10 item 2 and 3: free-swing fit from 0.1 s after the push on ring 13; lean and tilt on the outer ring from trusted columns | verified (`run_b.py` fit window; `pack_ride.py` LEAN, TILT). The free-swing fit itself is done on the run's `polar` (all columns, nanmean fill), not on the stored page file; the note's "the run samples the stored surface" is correct in that sense |
| M14 | 5.5 and 7.2: head's pressure rho_f h_f g_eff with g_eff = g + a_z; spill rule (15) with g_eff | wrong, because incomplete: the code clips the effective gravity at zero for the head's weight and for the mass term (`jnp.maximum(-gz, 0.0)`), and uses its absolute value in the spill rule (`jnp.abs(gz)`); the note itself says g + a_z < 0 occurs on the bumps (Example 6.1), so this case is reached and the note should say what the code does there |
| M15 | 9 playback and readings | verified (`guinness-jax-play.js`: SHA-256 check, min(0.1 s, real time), round(30 T), no blend, stop and "Ride again", words every > 250 ms; readings as described) |
| M16 | 11 controllers (Table 5, 6): PI with conditional integration; preview reads the slope one lag ahead with the static load; slosh LQR on the filter estimate, integral only while |i_cmd| < 3 A; joint adds (34) and the suspension LQR on (s, v_b, v_w, (N - N0)/k_t), clipped and lagged; filter predicts with the current measured at the last sample, corrects with speed every sample and probes at the first sample after a fluid step, Joseph form; joint re-discretises A_d, B_d with w^2(1 + a_z/g) | verified (`Cart.sample`, `observe`, `disc`, `forces`, `step`) |
| M17 | 11.5 the run stops before any controlled ride if the free swing is not one clean damped mode | verified (`PLANT_FROM_RUN` check in `run_b.py`) |
| M18 | 11.5 run 8 uses beta = 1.541 | verified (`BETA_HEAD` is off for `RUNSET=run8`; summary plant beta 1.5407) |

## Counts

248 rows (53 equations, 177 numbers or groups of numbers, 18 statements of method):

- verified: 213
- wrong: 9 (N96 ringing 3.330 Hz, not 3.331; N99 k = 44.6 /m, not 44.7; N103 tilt 13.5 mm, not 13.6; N134 key result
  7.79 s^-1 and 39 %, not 9.6 s^-1 and 29 %; N139 cancellation factor 110.2 A/m and 0.56 A, not 139.3 A/m and 0.71 A;
  N152b lean 0.94 mm, not 0.95; N159 run 7 leans 1.06 and 0.90 mm, not 1.05 and 0.89; N168 Problem 12.9 answer 1.08 A,
  not 1.36 A; M14 the clipping of g_eff in the head's pressure and spill rule is not described)
- unverifiable: 26 (mostly quotes of sources, and runs 3, 4, 6 and CPU tests whose data are not stored; N120 the no-lag
  bound, N149 most of Table 7)

The three wrong numbers of N134, N139 and N168 have one cause: they were computed with run 6's plant (3.278 Hz,
zeta 0.467) and not updated to run 8's (2.915 Hz, zeta 0.425). N103, N152b and N159 have another: the leans and tilts in
the index were computed before the heights were rounded to 0.02 mm for storage, so the stored files give the last digit
differently.
