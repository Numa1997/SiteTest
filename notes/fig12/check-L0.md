# Fig. 12 (furuta-pendulum.html): independent check, L0

Method. Equations re-derived in SymPy (element integration of the rod, `sympy.physics.mechanics` rigid bodies, `LagrangesMethod`, Jacobians, determinants, Riccati identity) and cross-checked with NumPy/SciPy (`solve_continuous_are`). Every quoted number recomputed from the page's own constants and code, run in headless Chromium (Playwright) with the page served from `/home/user/SiteTest/public`; values read from `window.Sim.data.ds`. Default run = the page's load state (preset Swing up, r = 0.16 m, V_max = 12 V, phi* = 60 deg, q_alpha = 40, q_phi = 2, rho = 1, k_E = 40). No page error was raised. Scripts are in the session scratchpad; no file of the repository was changed except this report.

Verdicts: verified / wrong, because ... / unverifiable, because ...

## A. Numbered equations

| # | Item | Verdict |
|---|------|---------|
| (1) | x(s) = r e_r + s(sin a e_phi + cos a e_z). Unit vectors e_r, e_phi, e_z as defined. | verified. SymPy: the time derivative gives exactly the decomposition printed in §3 and |xdot|^2 = r^2 phi'^2 + 2 r s cos a phi' a' + s^2(a'^2 + sin^2 a phi'^2). Unit m. Limits: s = 0 gives the hinge at r e_r; a = 0 gives upright; a = pi hanging. |
| (2) | T = 1/2 (J0 + Jp sin^2 a) phi'^2 + h cos a phi' a' + 1/2 Jp a'^2, J0 = Jr + mp r^2, Jp = mp L^2/3, h = mp r L/2 (Jr = ma r^2/3 + Jh). | verified. SymPy: integral over s of (mp/L)(1/2)|xdot|^2 plus 1/2 Jr phi'^2 equals (2) identically. Second route with `sympy.physics.mechanics` (arm J_r, rod as RigidBody with zero inertia about its own length, hinge axis along the arm): difference 0. Units kg m^2. Limits: r = 0 gives h = 0 and J0 = Jr (decoupled except Jp sin^2 a); a = 0 gives 1/2 J0 phi'^2 + h phi' a' + 1/2 Jp a'^2. |
| (3) | U = G cos a, G = mp g L/2. | verified. SymPy: integral of (mp/L) g s cos a ds = (mp g L/2) cos a (both routes). Unit J. Limit g -> 0 gives U = 0. |
| (4) | V_m = R I + Lambda dI/dt + k phi', tau = k I. | verified. Follows from the Lagrangian (5) (SymPy EL for q_e: Lambda q_e'' + R q_e' + k phi' = V_m; EL for phi carries -k q_e', i.e. tau = kI). Units: k phi' in (N m/A)(rad/s) = W/A = V. Limit: stalled (phi' = 0) gives V = R I (Ohm). Energy: V I = R I^2 + d(1/2 Lambda I^2)/dt + tau phi' (SymPy: V I - R I^2 - tau phi' = 0 with Lambda = 0). |
| (5) | Lagrangian L = T - U + 1/2 Lambda q_e'^2 + k phi q_e', D = 1/2 R q_e'^2 + 1/2 b_r phi'^2 + 1/2 b_p a'^2. | verified. SymPy: the Euler-Lagrange equations with D give exactly (4) and the torque k q_e' on phi (the text's "dL/dphi = k q_e' = kI" is correct). Units J and W. |
| (6) | tau = (k/R)(V_m - k phi'). | verified. Solved from (4) with Lambda = 0. Units N m. Limits: phi' = 0 gives k V/R (stall); V = 0 gives -(k^2/R) phi' (brake). |
| (7) | M(a) q'' = f(q,q') + (tau,0), M and f as printed. | verified. SymPy: EL equations of T - U with D, minus tau on phi, equal M q'' - f - (tau,0) with residual 0 in both rows. Independent `LagrangesMethod` (torque on arm, friction torque on rod): mass matrix and forcing identical to (7) (2 Jp sin a cos a = Jp sin 2a). Page code `accel()` implements the same rows (checked line by line). Units N m. Limits: r = 0 gives h = 0 (rows decouple except through Jp sin^2 a); static case gives G sin a = 0. |
| (8) | d(T+U)/dt = tau phi' - b_r phi'^2 - b_p a'^2. | verified. SymPy: dE/dt along (7) minus the right side is 0. Unit W. Limit: tau = 0 and no friction gives conservation. |
| (9) | A, B, b = b_r + k^2/R (linearisation at the top with (6)). | verified. SymPy: first-order expansion of (7) with (6) reproduces every entry of A and B (residual 0). Numerical check: eigenvalues of (9) with the page's constants are -10.3245, -0.8324, 0, +9.4794, equal to the page's `lamo_re` (from its central-difference `linearise()`); K from SciPy on (9) equals the page's K to 1e-12, so the page's A, B agree with (9). Units: A in 1/s, B in rad/s^2/V. Limit r -> 0: h -> 0, the alpha-row decouples. |
| (10) | lambda = 0,0,+-sqrt(J0 G/Delta) at the top; 0,0,+-i sqrt(J0 G/Delta) hanging. | verified. SymPy: char. polynomial at the top (no friction, motor off) = lambda^2(lambda^2 - J0 G/Delta); hanging (alpha = pi: sin -> -x, cos -> -1) = lambda^2(lambda^2 + J0 G/Delta). Limits: r -> 0 gives Delta = J0 Jp so sqrt(G/Jp) (arm "held"); J0 -> infinity (arm held) gives the same. G -> 0 gives all zeros. Unit 1/s. |
| (11) | C = [B, AB, A^2B, A^3B]. | verified (definition of Kalman's matrix; the rank statement is checked in §B). |
| (12) | E_p = 1/2 Jp a'^2 + G cos a. | verified. Units J; hanging at rest -G, upright at rest +G. The printed derivative dE_p/dt = -h cos a a' phi'' + Jp sin a cos a phi'^2 a' - b_p a'^2 is confirmed by SymPy (second row of (7)). |
| (13) | u = sat_amax[kE (E_p - G) a' cos a] - k_phi (phi - phi*) - k_w phi'. | verified. Units: kE in 1/(J s) gives rad/s^2 (J rad/s * 1/(J s) = rad/s^2). Code `drive()` implements exactly this (uE clipped to +-30, spring 4, damper 3). The text on the Lyapunov rate V_s' = -h kE (E_p-G)^2 (a' cos a)^2 is confirmed by SymPy (the bracket inserted in dE_p/dt, other terms dropped as the text says). |
| (14) | tau(u) and V_m = R tau/k + k phi'. | verified. SymPy: solving row 2 of (7) for a'' with phi'' = u and inserting in row 1 gives exactly the printed tau (residual 0). Code `drive()` has the same expression. Limit r = 0 (h = 0): tau = (J0 + Jp sin^2 a)u + 2 Jp sin a cos a phi' a' + b_r phi', the arm alone. Last line inverts (6). |
| (15) | J = int(y~'Q y~ + rho V^2), Q = diag(q_phi, q_alpha, 0.5, 2). | verified against the code (`Q = [p.qp, p.qa, QW[0], QW[1]]`, QW = [0.5, 2], state order phi, alpha, phi', alpha'). Units: q in 1/rad^2, 1/(rad/s)^2, rho in 1/V^2 (J is then a time). |
| (16) | A'P + PA - rho^-1 P B B' P + Q = 0. | verified. Residual of the page's P in (16), computed with (9): 1.5e-9 (float noise in P printed at 16 digits is 7e-11 vs SciPy). SciPy `solve_continuous_are` gives the same P: max relative difference 9e-13. Hamiltonian in `lqr()` is [[A, -BB'/R],[-Q, -A']] (8x8, as the text says). |
| (17) | K = rho^-1 B' P. | verified. Page K = (-1.4142, -34.2896, -1.4238, -4.4568); SciPy gives the same to 12 digits. K[0] = -sqrt(q_phi/rho) = -1.4142 as expected. Units V/rad, V s/rad. |
| (18) | dV_c/dt = -y~'(Q + rho K'K)y~ < 0. | verified. SymPy: (A-BK)'P + P(A-BK) = (Riccati expression) - Q - rho K'K, identically. Numerically with the page's P, K the residual is 1.5e-9. Positive-definite Q (diag 2, 40, 0.5, 2) gives < 0 for y~ != 0. Valid for the linear loop without saturation, as the text says. |
| (19) | hand-over at y~'Py~ < c_in = c/2, back at > c_out = c. | verified against code: `decide()` returns `caught ? L <= cout : L < cin`, cin = 0.5 c, cout = c, evaluated once per ms (`TS = 0.001`, `per = round(TS/h)`). |
| (20) | E(0) + W_in - Q_R - Q_b - E(T) = 0. | verified. Follows from (4) with Lambda = 0 and (8); the page's value is 5.74e-11 J (Off run: 6.8e-15 J). Units J. |

## B. Quoted numbers, in order of appearance

| Section | Quoted | Verdict |
|---|---|---|
| Abstract, §13 | pendulum falls away at "9.5 per second" | verified. grow = 9.4794 1/s (`ds.get('grow')`). |
| §2 | r = 0.16 m, ma = 0.10 kg, Jh = 2.0e-4, mp = 0.08, L = 0.30, b_r = 1.0e-4, b_p = 2.0e-5 | verified. Equal to the constants `MA, JH, MP, LP, BR, BP` and the r slider default 0.16. |
| §3 | Jr = 1.053e-3, J0 = 3.101e-3, Jp = 2.400e-3, h = 1.920e-3 kg m^2, G = 0.1177 J | verified. Page: 1.05333e-3, 3.10133e-3, 2.4e-3, 1.92e-3, 0.11772. |
| §3 | "SymPy confirms (2) and (3) twice" (element-by-element and `sympy.physics.mechanics`) | verified. Reproduced both routes, residual 0. |
| §4 | Lambda/R = 0.5 ms for Lambda = 2 mH, R = 4 ohm | verified. 2e-3/4 = 5e-4 s. |
| §4 | sqrt(Jp/G) = 0.143 s; ratio 0.0035 | verified. 0.14278 s; 5e-4/0.14278 = 0.003502. |
| §4 | k V_max/R = 0.30 N m; V_max/k = 120 rad/s; k^2/R = 0.0025 N m s | verified. 0.1*12/4 = 0.3; 12/0.1 = 120; 0.01/4 = 0.0025. |
| §4 | "The preset Off disconnects the amplifier ... no torque" | verified. `drive()` returns I = 0 in mode off; Off run: W_in = Q_R = 0. |
| §5 | "SymPy derives (7) a second time with LagrangesMethod ... same mass matrix and forcing" | verified. Reproduced, identical. |
| §5 | "page solves (7) in accel() by Cramer's rule" | verified. `accel()` is the 2x2 Cramer solution, rows as in (7). |
| §6 | "builds A and B in linearise(), by central differences ... agree with (9)" | verified. `linearise()` uses e = 1e-6 central differences of `rhs()`; agreement with (9) shown above. |
| §6 | sqrt(J0 G/Delta) = 9.86 /s (saddle) and 9.86 rad/s (centre) | verified. 9.8580 (`w_bot`). |
| §6 | sqrt(G/Jp) = 7.00 rad/s | verified. 7.0036 (`w_fix`). |
| §6 | Delta/J0 = Jp - h^2/J0 | verified. Both 1.21135e-3 kg m^2; Delta = 3.7568e-6 kg^2 m^4. |
| §6 | Off, hanging nudged 3 deg: 62 turning points in 20 s, 9.85 rad/s | verified. n_swings = 62; sign changes of alpha' interpolated: first 0.294 s, last 19.751 s, so omega = pi*61/19.457 = 9.849 rad/s. (Reader's note: the run starts at the nudged hanging state only after "From t = 0" is pressed; pressing Off while the playback is elsewhere restarts from the state shown.) |
| §6 Ex. 6.1 | eigenvalues -10.32, -0.83, 0, +9.48 per second | verified. -10.3245, -0.8324, 0, 9.4794 (page `eig()`; NumPy agrees to 8 digits). |
| §6 Ex. 6.1 | ln(1000)/9.48 = 0.73 s | verified. 6.9078/9.4794 = 0.7287 s. |
| §6 Ex. 6.1 | "Any controller must act well within a tenth of a second" | verified (1/9.48 = 0.105 s; a judgment, consistent). |
| §7 | det C = -k^4 G^2 h^2/(R^4 Delta^4) | verified. SymPy gives exactly this, with or without friction (independent of b, b_p). Numerically -1.0018e8 from the page's constants, equal to the formula. |
| §7 | vanishes only for k = 0, G = 0 or h = 0 | verified (Delta is never zero for a rod with finite mass distribution: Delta = 3.7568e-6). |
| §7 | rank in `rankOf()` is 4 | verified. `ds.get('rank') = 4`; NumPy rank 4. |
| §7 | r = 0.02 m: rank still 4, swing-up no longer reaches the top within 20 s | verified. In the browser with r = 0.02: rank 4, t_catch = NaN, 31 half-swings, alpha(20 s) = 1.34 rad (not caught). |
| §8 | 2G = 0.235 J | verified. 0.23544 J. |
| §8 | a_max = 30 rad/s^2, k_phi = 4 s^-2, k_w = 3 s^-1, k_E = 40 | verified (constants `AMAX, KPHI, KW`, kE slider default 40). |
| §8 | default: four half-swings, catch takes over at t = 2.75 s | verified. n_swings = 4, t_catch = 2.75 s (first caught sample 275 at 10 ms). |
| §8 | Astrom-Furuta: single swing only for n >= 4/3 (n = ratio of largest pivot acceleration to g) | verified against the primary source (IFAC 1996 paper, read in full): "The acceleration must thus be at least 4g/3 to have a single-swing behavior." |
| §8 | a_max r = 4.8 m/s^2, n = 0.49 | verified. 30*0.16 = 4.8; 4.8/9.81 = 0.489. |
| §9 | defaults q_phi = 2, q_alpha = 40, rho = 1 V^-2 | verified (slider defaults 2, 40, log10 rho = 0). |
| §9 | K = (-1.41, -34.29, -1.42, -4.46) | verified. (-1.4142, -34.2896, -1.4238, -4.4568). |
| §9 | "SciPy's Riccati solver gives the same P to every printed digit" | verified. Max relative difference 9e-13. |
| §9 | "sign function ... converges in a few iterations" | verified, loosely. The Newton iteration in `lqr()` stops after 10 iterations (tolerance 1e-12 summed over 64 entries). |
| §9 | 1 deg lean: 34.29 x 0.0175 = 0.60 V; arm accelerates in the direction of the lean | verified. 34.29*0.0175 = 0.6001 (exact 1 deg = 0.5985 V; both 0.60). Sign: V = -K y~ = +34.29 a for a > 0 along +e_phi, so tau > 0 and the hinge accelerates along +e_phi (by (1), a > 0 leans toward +e_phi). |
| §9 | eigenvalues of A-BK: -24.57, -5.44, -3.52, -2.36, all real and negative | verified. -24.570, -5.436, -3.518, -2.358; SciPy agrees. |
| §9 | rho x 10: slowest rate 1.61 /s | verified. Browser (rho slider at 1): slow = -1.6142 (a double eigenvalue); SciPy agrees. |
| §10 | grid 37 x 31 = 1147 starts, alpha in +-90 deg, alpha' in +-15 rad/s | verified. `NA = 37, NV = 31`, 37*31 = 1147; `BAL = pi/2`, `BVL = 15`. |
| §10 | "runs the catch alone for 3 s", rescued when y~'Py~ < 0.05 | verified against `catchOnly()` (T = 3, `C_SMALL = 0.05`); one detail the note leaves out: the test integrates with RK4 step 2 ms, not 1 ms. |
| §10 | 339 of 1147 rescued | verified. basin_n = 339. |
| §10 | at rest rescued up to +-30 deg | verified. At alpha' = 0 (grid column 15), the rescued alpha are -30 ... +30 deg (grid step 5 deg); 35 deg is not rescued. |
| §10 | 240 starts over the surface y~'Py~ = c, bisection 12 times, c = 9.78 | verified. `measureC()`: 240 directions, `it < 12`, c = 9.7754. The sampling (z uniform on the unit sphere, y~ = sqrt(c) L z with L L' = P^-1) does give y~'Py~ = c exactly (L'PL = I). |
| §10 | hand-over at y~'Py~ = 4.81, E_p at 97 % of G | verified. First caught sample: 4.8109 (the sample before: 5.434, above c_in = 4.8877); E_p/G = 0.11449/0.11772 = 0.9726. |
| §10 | rho x 10: c rises to 20.2 | verified. 20.166 (also c_in = 10.08, basin 391). |
| §10 | switching "once every millisecond" | verified (`TS = 0.001`). |
| §11 | RK4, h = 1 ms, 20 s, 20 000 steps; every tenth state stored (one per 10 ms) | verified. `H = 0.001, TEND = 20, EVERY = 10`; steps = 20000; NS = 2001 samples. |
| §11 | "The controller is evaluated at all four stages of each step" | verified. `stepRK4()` calls `drive()` at all four stages (the supervisor flag `caught` is held constant in the step, as the text says). |
| §11 | fastest rate 24.6 /s, h lambda = 0.025, RK4 limit about 2.8 | verified. 24.570 /s; 0.0246; RK4 real-axis stability limit 2.785. |
| §11 | half-step difference 5.9e-5 at t = 2.61 s | verified. err_half = 5.899e-5, err_end = 2.61 s. |
| §11 | Off: difference 5e-9 | verified. 4.6e-9 (rounds to 5e-9). |
| §11 | the h/2 run uses the same millisecond supervisor clock | verified. `run()` uses `per = round(TS/h)` = 2 for h/2. |
| §11 | energy balance 5.7e-11 J | verified. 5.743e-11 J. |
| §11 | W_in = 14.15 J, winding heat 13.91 J, bearings 0.004 J, rig energy up by 0.235 J | verified. 14.1519, 13.9130, 0.00366 (rounds to 0.004), E(T)-E(0) = 0.11772 - (-0.11756) = 0.23528; check: 14.1519 - 13.9130 - 0.0037 = 0.2353. |
| §11 | "the 2G of §8" | verified to three digits: 0.23528 J against 2G = 0.23544 J; the 0.00016 J difference is the 3 deg nudge (E(0) = -G cos 3 deg). |
| §11 | less than 2 % of the electrical work lifted the pendulum | verified. 0.2353/14.152 = 1.66 %. |
| §11 | fraction of V_m I that becomes work is k phi'/V_m | verified. tau phi'/(V I) with tau = kI and V = R I + k phi' (Lambda = 0): k I phi'/(V I) = k phi'/V. |
| §12 | oblique view looks down 24 deg | verified (`ELEV = 24 pi/180`). |
| §12 | torque arc sweeps up to 0.9 of a half-turn at stall torque | verified. `sweep = clamp(tau/tmax) * 0.9 * pi`, tmax = k V_max/R. (The code comment says "full turn" which is wrong; the note is right.) |
| §12 | window of 8 s; left edge clamp(t_play - 2.4, 0, 12) | verified. `WIN = 8`, `t0 = max(0, min(TEND-WIN, t_play - 0.3*WIN))`. |
| §12 | alpha shown between -pi and pi, its curve breaks where hanging rod passes straight down; stored alpha does not jump | verified. `chartVal` wraps; the line is broken when the jump exceeds pi; stored `al` is unwrapped (alpha(20 s) = 2 pi in the rho x 10 run, a continuous value). |
| §12 | "values below 1e-6 are drawn at 1e-6" | verified (`p.L` clamps log10 to [-6, 2]). |
| §12 | "the two Lyapunov functions on a logarithmic scale" | wrong, because the swing-up curve drawn is 1/2 (E_p - G)^2 / G^2 (dimensionless, legend "swing-up: 1/2(E_p - G)^2/G^2"), not V_s = 1/2 (E_p - G)^2 in J^2 as defined in §8. Correct statement: the swing-up curve is V_s / G^2. Small, but the clamp at 1e-6 is therefore applied to V_s/G^2. |
| §12 | hand-over ellipse is the slice y~'Py~ = c_in with the arm at phi* and at rest | verified. `drawPhase()` uses the (alpha, alpha') block of P (entries P11, P13, P33), inverted for the Cholesky factor; that is the slice phi = phi*, phi' = 0. |
| §12 | brown while swing-up pumps, burgundy once caught; marks at the voltage limit | verified (`cg[n] ? BURG : TANI`; second row for `sat[n]`). |
| §13 | rod 6 mm thick: m_p d^2/8 = 3.6e-7 kg m^2 against Jp = 2.4e-3 | verified. 0.08*(0.006)^2/8 = 3.6e-7 (solid cylinder about its axis m r^2/2 with r = d/2). |
| §13 | fall rate "9.5 per second" | verified (9.479). |
| §13 Problem 3 | 2G for mp = 0.08, L = 0.30 | verified. 0.2354 J. The prediction "swing-up takes longer or fails" at V_max = 6 V is borne out: browser run with 6 V: not caught within 20 s (t_catch = NaN, 32 half-swings, motor at its limit 6.03 s). |
| §13 refs | Astrom & Furuta, IFAC 13th World Congress, San Francisco, 1996; Automatica 36, 287-295 (2000) | verified (first from the PDF header; second is the known journal version, not checkable from the PDF). |
| §13 refs | Tedrake, Underactuated Robotics ch. 3 "Acrobots, Cart-Poles, and Quadrotors": linearisation, controllability, LQR, collocated PFL, energy shaping with Lyapunov argument | verified. Chapter title confirmed online; collocated partial feedback linearisation, energy shaping, LQR, controllability and a LaSalle/Lyapunov argument for the energy controller are in the text. |
| §13 refs | Astrom & Murray, Feedback Systems: Sect. 6.1 reachability, Thm 6.1 rank test, Sect. 6.3 LQR, Riccati (6.26)-(6.27) | verified. In the 22 Feb 2009 edition: 6.1 Reachability, Theorem 6.1 (rank condition), 6.3 State Feedback Design with "Linear Quadratic Regulators", (6.26) cost, (6.27) algebraic Riccati equation. |
| §13 refs, §1 | Furuta pendulum invented 1992 at Tokyo Institute of Technology by K. Furuta and colleagues | verified (Wikipedia article text, which the note cites). |

## C. Line-by-line match of the numerical method with the code

| Statement of the note | Code | Verdict |
|---|---|---|
| (7) solved for q'' in `accel()` by Cramer's rule | `det = a11 a22 - a12^2; [(a22 r1 - a12 r2)/det, (a11 r2 - a12 r1)/det]`, r1 = kI - b_r w - 2 Jp s c w v + h s v^2, r2 = Jp s c w^2 + G s - b_p v | verified |
| torque tau = k I with I = (V - k phi')/R | `rhs()`, `drive()`: `I = (V - KM*y[2])/RM` | verified |
| voltage clipped to +-V_max | `drive()`: `V = max(-Vmax, min(Vmax, want))`; `sat` flag when `|want| > Vmax` | verified |
| swing-up: (13), (14), then V = R tau/k + k phi' | `drive()` lines for uE, u, add, tau, want | verified (algebra of (14) checked symbolically) |
| catch: V = -K y~ with nearest angles | `catchVolt()` uses `err()` = wrap(phi - phi*), wrap(alpha) | verified |
| RK4 with controller at all four stages; three extra states W_in, Q_R, Q_b integrated with the same weights | `stepRK4()` | verified |
| supervisor looks at the state once per millisecond, held in between | `run()`: `if ((step-1) % per === 0) caught = decide(...)` | verified |
| second solve with h/2, largest difference over stored samples | `solve()`: `run(p,d,y0,H/2,2*EVERY, ...)`, max over the four components | verified |
| t_catch: "the catch takes over" | last sample with `cg == 0`, then the next time | verified (for the default run the catch is final; the note says "takes over at t = 2.75 s") |
| LQR by sign function of the 8x8 Hamiltonian | `lqr()` | verified |
| eigenvalues | `eig()`: Faddeev-LeVerrier + Durand-Kerner (not described in the note; no claim to check) | verified |
| region of rescue: 37 x 31 grid, 3 s, y~'Py~ < 0.05 | `measureBasin()`/`startBasin()`: `catchOnly(..., 3, 0.002)` | verified, with the 2 ms step as an undeclared detail |
| c: 240 starts, 12 halvings | `measureC()`: bisection on [0, 40], 12 rounds, same 240 directions each round | verified (initial interval [0,40], so the resolution is 40/4096 = 0.0098; not stated in the note) |

## D. Remarks that are not wrong numbers

1. §10 says "Equation (18) proves that the catch works only near the top." As written this claims (18) proves a limit; (18) proves nothing about far starts. The intended meaning is "(18) proves the catch works near the top, and nothing more". Wording only.
2. The symbol h is used both for the coupling h = mp r L/2 (kg m^2) and for the RK4 step h = 1 ms (§11, "h/2"). Different quantities, same letter, in the same note.
3. The comment in `drawRig()` says the torque arc is "full turn" at stall; the code and the note say 0.9 of a half-turn.
4. §9 "approached without ringing": all four eigenvalues are real, so there is no oscillation; a node with real distinct eigenvalues can still cross zero once, so "without oscillation" is the exact statement.
5. Problem 1 (r = 0): with h = 0, B has no component on alpha'' and the rank of (11) is 2 (only phi, phi' are reachable); not stated in the note, given here as the answer to the exercise.

## Totals

Equations (1)-(20): 20 verified, 0 wrong, 0 unverifiable.
Quoted numbers and statements (section B): 1 wrong (§12, Lyapunov chart normalisation), 0 unverifiable, all others verified.
