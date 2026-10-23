# Gate 2 check of the lecture note "Pendula on a Turning Blade" (round 1)

Page checked: `rotor_notes_r3.html` (scratchpad), byte-identical to `portfolios-src/rotor-pendula/rotor_notes.html`.
Opened in headless Chromium (Playwright): 0 KaTeX errors, 0 unfilled `{{…}}` placeholders, no console errors, 29 numbered
equations (1.1–8.1), 2 figures, 9 chapters, 4 tables. The page's only script is the progress bar and an equation-width fitter;
no number on the page is computed in the browser, so "the page's own code" for numbers is `tools/make_numbers.py` plus the
derive scripts. I recomputed the numbers with my own code instead (constants retyped, nothing imported from the study):
SymPy for every equation; SciPy `solve_ivp` (DOP853, Radau, LSODA) for the dynamics; my own double-pendulum Lagrangian;
my own implementation of (7.6)–(7.8); my own Euler–Maruyama Monte Carlo for chapter 4. Primary sources read: maxon product
pages for RE 25 part 339152 and GP 32 C parts 166933/166938/166939/166944; Jonkman et al. 2009 (NREL/TP-500-38060, OSTI copy);
TI CC2652R datasheet (SWRS207J). Scripts: scratchpad `chk/` (s1–s8, t1–t4, g1–g4, n1, mc1, pw.js).

Verdicts: **right 111, wrong 7, unclear 13** (131 rows: 35 equation rows, 96 number rows).

## Equations

| # | Item | Note's claim | My result | Verdict | How checked |
|---|---|---|---|---|---|
| 1 | (1.1) bob position | x = r_p cosφ + L cos(φ+θ), y = … | same | right | definition, used as input of the SymPy Lagrangian |
| 2 | (1.2) kinetic energy | T = ½m[r_p²φ̇² + L²(φ̇+θ̇)² + 2r_pLφ̇(φ̇+θ̇)cosθ] | identical | right | SymPy: differentiate (1.1), simplify T − (1.2) = 0 |
| 3 | ∂L/∂θ̇, ∂L/∂θ (printed lines) | as printed | identical | right | SymPy |
| 4 | (1.3) equation of motion | mL²(θ̈+φ̈) + mr_pL(φ̈cosθ + φ̇²sinθ) + mgL cos(φ+θ) + cθ̇ = 0 | identical; also identical to Newton's torque balance about the pivot in the inertial frame | right | SymPy, two routes |
| 5 | (1.3) units / stopped-rotor limit | N m; φ̇=φ̈=0 gives damped pendulum, ω² = g/L | confirmed | right | dimensions; substitution |
| 6 | (1.4) energy balance | dE/dt = τ_rot φ̇ − cθ̇² | identical after eliminating θ̈ with (1.3) | right | SymPy |
| 7 | (1.5) blade-angle form, R, G, κ | θ'' + κθ' + R sinθ + G cos(φ+θ) = 0 | identical (division by mL²Ω²) | right | SymPy |
| 8 | (2.1) linearised equation | θ'' + κθ' + Rθ = −G cosφ | follows from (1.5) dropping −Gθ sinφ | right | SymPy series |
| 9 | (2.2) swing, amplitude, lag | (R−1+iκ)A = −G; Θ = G/√((R−1)²+κ²); tanδ = κ/(R−1) | solves (2.1) to 1e-15 at random parameters; −Θcos(φ−δ) form equal | right | SymPy + numeric spot checks |
| 10 | (2.3) mean power | mL²Ω³ κG²/(2[(R−1)²+κ²]) | identical | right | SymPy |
| 11 | (2.4) best brake | κ* = \|R−1\|, δ = 45° | dP/dκ = 0 gives ±(R−1); tanδ = 1 | right | SymPy |
| 12 | (2.5) P* and units | mLg²/(4Ω\|r_p−L\|), W | identical; units W | right | SymPy, sympy.physics.units |
| 13 | (2.5) limits | g→0 gives 0; diverges at r_p = L (√R = 1) | confirmed | right | inspection |
| 14 | Fig. 2 curve | P/P* = 2x/(1+x²); half power at x = 2∓√3 (0.27, 3.7) | identical; 0.268, 3.73 | right | SymPy solve |
| 15 | (2.6) large rotor | P* ≈ mLg²/(4Ωr_p) | leading term of (2.5) for r_p ≫ L | right | SymPy limit |
| 16 | (2.7) tilted hinge | x'' + κx' + (R cosα − sin²α − G cosα sinφ)x = −G cosφ | identical | right | own 3-D SymPy Lagrangian, hinge axis n = cosα e_z + sinα e_r, linearised |
| 17 | (3.1) mean trail balance | Rθ̄ = G⟨θ sinφ⟩ | follows from averaging (1.5) with the 2nd-order gravity term | right | hand + SymPy average |
| 18 | ⟨θ sinφ⟩, sinδ | −½Θ sinδ; sinδ = κΘ/G | confirmed | right | SymPy integral |
| 19 | (3.2) trail | θ̄ = −κΘ²/(2R); at κ*: −G²/(4R(R−1)) | identical | right | numeric spot checks (residual 0) |
| 20 | (3.3) trail identity | P̄ = −m r_p L Ω³ θ̄ for every brake | identical | right | SymPy/numeric; also τ̄_rot = mgL⟨cos(φ+θ)⟩ since ∂L/∂φ = −mg(r_p cosφ + L cos(φ+θ)) |
| 21 | (3.4) locked double / rigid body | P*_rigid = (Mℓ_c g)²/(4Ω(Mℓ_c r_p − I_p)) | identical; reduces to (2.5); units W | right | own rigid-body Lagrangian in SymPy, best c = \|K−IΩ²\|/Ω |
| 22 | (4.1) generalised force | Q_k = −a b_k, b_k = Σ m_i ê·∂x_i/∂q_k | virtual work of −m_i a ê | right | hand |
| 23 | (4.2) noise power | P_in = (S/2)⟨b^T M⁻¹ b⟩ | E[ΔK]/dt = S b²/(2M) for the single (= S m(ê·t̂)²/2); Itô = Stratonovich since b depends on q only | right | SymPy second-order expansion; own MC (row 70) |
| 24 | (4.3) m_eff ≤ M_total | Rayleigh max + weighted Cauchy–Schwarz | chain valid; max over 2·10⁵ random double-pendulum states = 0.100000 kg = M_total | right | hand + numeric |
| 25 | (4.4) ceiling | P_in ≤ (S/2)M_total; equality for top rod ⊥ shaking | m_eff = 0.1 kg exactly for q1 ⊥ ê, any q2 | right | numeric |
| 26 | (7.1) brake constant | c_e = N²k_tk_e/(R_c+R_L) | confirmed (ratio enters in voltage and torque) | right | hand |
| 27 | (7.2) load share | P_load = c_e(1 − c_e/c_sc)⟨θ̇²⟩ | 1 − c_e/c_sc = R_L/(R_c+R_L) | right | hand |
| 28 | (7.3) reflected inertia | j = JN²/(mL²) | confirmed; cross term JΩNθ̇ is a total derivative at steady Ω | right | hand |
| 29 | (7.4) geared equation, f/G | f = NT₀/(ηmL²Ω²), f/G = NT₀/(ηmgL) | confirmed | right | hand |
| 30 | (7.5) describing function | κ_f = 4f/(πΘ) | first harmonic of square wave = 4f/π | right | Fourier coefficient |
| 31 | (7.6) quadratic | Θ²(R−1−j)² + (κ_eΘ/η + 4f/π)² = G²; positive root iff 4f/π < G | confirmed (product of roots ∝ (4f/π)² − G²) | right | hand; my formula code reproduces the stored formula values (7.981, 1.801, 41.153 mW) |
| 32 | (7.7) powers | P_load and P_rotor as printed; ⟨\|θ'\|⟩ = 2Θ/π | confirmed; losses removed → (2.2), (2.3) | right | hand |
| 33 | (7.8) full geared equation | k = η^(−sgn(xθ')); unique θ'' | confirmed; kx is increasing in θ'' | right | hand; my own solver (brentq) |
| 34 | (8.1) ceiling | P̄ ≤ mgL⟨\|θ̇⟩ | blade-frame balance θ̇·(1.3) = d/dt[½mL²θ̇² − mr_pLΩ²cosθ] + cθ̇² + mgL cos(φ+θ)θ̇ (SymPy: 0) | right | SymPy |
| 35 | P* as fraction of (8.1) | π/(4√2) = 0.56 | 0.5554 | right | arithmetic |

## Numbers

| # | Item | Note's claim | My result | Verdict | How checked |
|---|---|---|---|---|---|
| 36 | rotor radii 56/Ω | 1.34, 2.67, 5.35, 26.74, 38.20, 66.85 m; "1.3 to 5.3", "27 to 67" | 1.337, 2.674, 5.348, 26.74, 38.20, 66.85 | right | arithmetic |
| 37 | pivots | 0.401 … 60.161 m | same | right | arithmetic |
| 38 | Γ range | 1.44 to 215 | 1.435 to 215.3 | right | own table |
| 39 | tilt 1/Γ, max | 0.27°, up to 44° | 0.266°; asin(1/Γ_min) = 44.2° (exact max tilt of the summed pull) | right | geometry |
| 40 | R, G ranges | 2.01–301; 0.028–69.9 | 2.005–300.8; 0.02795–69.86 | right | arithmetic |
| 41 | √R range | 1.42 to 17.3 | 1.416 to 17.34 | right | arithmetic |
| 42 | G/R max | 0.70 | 0.697 | right | arithmetic |
| 43 | Table 1: R, G, Γ, Θ*, P* (18 rows) | as printed | all 18 rows identical to the printed digits | right | own script n1.py |
| 44 | Table 1: full model (18 rows, incl. ¹ rows) | 57.09 … 9.55 | my DOP853 integration of (1.5) at Sol's brakes (60 turns settle, 40 measure): all 18 identical to 2 decimals (e.g. 28.72, 28.99, 9.55) | right | t1.py |
| 45 | Table 1: double, mW (18 rows) | 36.26 … 7.03 | my own SymPy double-pendulum Lagrangian + SciPy Radau: all 18 identical (36.2571 … 7.0259) | right | t1.py double |
| 46 | Table 1: double ÷ single | 0.635 … 0.735 | 0.6351 … 0.7354 | right | from rows 44–45 |
| 47 | Sol's double brake = linear optimum | "the one value that maximises its small-swing power" | my linear double optimum equals Sol's c to 5 digits (400/30, 20/60, 8/90) | right | t2.py |
| 48 | closed form vs full | within 0.68 % | max 0.679 % (8 rpm 30 %) | right | n1.py |
| 49 | max swing | 0.50 rad (29°) | 0.498 rad = 28.5° | right | arithmetic |
| 50 | (2.6) flat values | 28.62, 14.31, 9.54 mW; runs 28.72–29.28, 14.32–14.48, 9.55–9.62 | 28.622, 14.311, 9.541; runs as stated | right | arithmetic + row 44 |
| 51 | torque at optimum | mgL/√2 = 0.1387 N m | 0.13869 | right | SymPy (c*ΩΘ* simplifies to mgL/√2) |
| 52 | mechanical power range | 9.55 to 57.1 mW | 9.554 to 57.086 | right | row 44 |
| 53 | turbine share | 7.2 parts in 100 000, at 400 rpm 30 % | 7.20e-5 (P_T = 792 W) | right | arithmetic |
| 54 | sensor need | 37.6 µW | CC2652R datasheet: MCU 3.4 mA + TX 0 dBm 7.0 mA for 1 ms each at 3.0 V, standby 0.94 µA → 34.0 µW; + ADXL362 1.8 µA at 2.0 V (3.6 µW) → 37.6 µW. ADXL362 figure from memory (analog.com unreachable) | right | primary source (TI); one input unread |
| 55 | margin, worst mounting | 127 times (half lost) | 127.0 | right | arithmetic |
| 56 | tilt α, sensitivity | 43.0°, 2.4/rad; 89.6°, 301/rad; 0.1° moves stiffness by half | 43.04°, 2.37; 89.62°, 300.8; 0.525 | right | SymPy nsolve |
| 57 | Θ²/4 push change, ~6 % | Θ²/4 of the push | in-phase first harmonic of −½Gθ²cosφ = −Θ²/4 · G at κ*; 0.498²/4 = 6.2 % | right | SymPy Fourier |
| 58 | Radau IIA description | 3-stage, 5th order; halving step → ~30× smaller error; 6 parts in 10¹³ vs independent solver | engine.py is fixed-step 3-stage Radau IIA (order conditions asserted); log: orders 4.90–4.95 (2^4.9 ≈ 30), 6.1e-13 vs DOP853 | right | code read line by line + log; outputs reproduced by my third solver |
| 59 | explicit-method cost | tens of thousands of steps per turn | fastest relaxation 9 900 s⁻¹ at 8 rpm 90 %; RK4 needs ≈ 26 700 steps/turn | right | eigenvalues of M⁻¹C |
| 60 | trail, slowest rotor | (3.2): −0.123 rad, 7.0°; full model −0.128 | −0.1226, 7.02°; my full model at κ*: −0.1283 (at Sol's brake −0.1293) | right | t1b.py. Note: this value is typed by hand in make_numbers.py (see row 126) |
| 61 | next largest trail | 2.3° | 2.31° (14 rpm 30 %) | right | arithmetic |
| 62 | fast rotors' trail | "never exceeds 0.05°" | max 0.0508° (100 rpm, 30 %) | wrong, because the maximum is 0.051°, slightly above 0.05° (say "about 0.05°") | arithmetic |
| 63 | locked double | ℓ_c = 0.75L; 0.643 to 0.750 of single | 0.75; 0.6433 to 0.7496 | right | (3.4) evaluated |
| 64 | hinge cost | further 1.3 to 1.9 % | 1.28 to 1.90 % | right | rows 45, 63 |
| 65 | chaos group setup | R = 1, r_p = 0.2 m, Ω = 4, G = 3.06; κ = 0.938, 1.375, 1.875, 2.812; threshold 0.04 s⁻¹ | G = 3.0646; κ = 0.9375 … 2.8125; 0.01×4 | right | arithmetic |
| 66 | chaos group c = 0.015, 0.022 | 262.5 mW, Λ = −1.707; 378.9 mW, Λ = −0.602 | 262.46, −1.707; 378.92, −0.602 (own solver, from rest, 100+200 turns, Benettin 1e-8, quarter-turn renormalisation) | right | t3.py |
| 67 | chaos group c = 0.030, 0.045 | 16/16 chaotic, 236–253 mW, Λ 0.10–0.19; 115–119 mW, Λ −0.01 to 0.01 | from rest: 241.6 mW, Λ = 0.127 (chaotic); 118.3 mW, Λ = 0.012 | right (one start each; other 15 starts not rerun) | t3.py |
| 68 | "all these powers are four to seven times the best real mounting" | 4 to 7 × 57.09 mW | 262.5/378.9/236–253 mW are 4.1–6.6×, but 115–119 mW is 2.0–2.1× | wrong, because the c = 0.045 row is only about 2× the best mounting; the range is 2.0 to 6.6× | arithmetic |
| 69 | settling time | Λ = −0.006 s⁻¹ ≈ a hundred turns | 1/0.006 s = 106 turns | right | arithmetic |
| 70 | map: κ* at R = 1 | 0.128; "fifteen times heavier" (1.875) | 0.1283 (own linearised double); ratio 14.6 | right | t2.py |
| 71 | map: 480 runs; chaos only at R = 1, G = 1 | table | 6×5×2×8 = 480. Spot checks (own solver): R=1,G=1 at κ* and κ*/10, 4 starts: all chaotic (Λ 0.13–0.27/rad); R=2,G=1 at κ* and κ*/10, 3 starts: all regular | right (spot-checked 7 of 480) | t4.py |
| 72 | map: other 28 cells all 0/16 | table | not rerun | unclear, because only R = 1 and 2 at G = 1 were re-run | — |
| 73 | MC: gentle swing | S = 0.028 m²/s³ gives swings of 0.05 rad | rms 0.049–0.0505 rad (linear theory and my MC) | right | mc1.py |
| 74 | MC: violent single m_eff | ⟨m_eff⟩ = 0.48 M | 0.478 | right | own Euler–Maruyama, 1000 runs, 20 s + 40 s |
| 75 | MC agreement | within 0.22–0.65 % at SE 0.4–0.7 % | my single runs: −0.02 % (SE 0.41 %), −0.71 % (SE 0.43 %); theorem confirmed, their exact percentages not reproducible from my runs | unclear, because their ensembles were not rerun | mc1.py |
| 76 | MC: tumbling double | ⟨m_eff⟩ = 0.55; ~100 tumbles per 40 s | not rerun | unclear, because I did not run the double MC | — |
| 77 | edgewise frequency | 1.08 Hz; 1.0793 Hz in Jonkman Table 9-1 | Table 9-1 mode 7, FAST: 1.0793 Hz | right | primary source (OSTI copy) |
| 78 | NREL 5 MW rotor | 126 m; 61.5 m blade | 126 m (Table 1-1); 61.5 m (Table 2-2) | right | primary source |
| 79 | rotor + generator inertia | 4.38e7 kg m² | 3 blades (11 776 047 + 2·1.5·363 231 + 17 740·1.5²)·cos²2.5° + 115 926 + 534.116·97² = 4.38e7 | right | primary-source tables |
| 80 | steady speed at 8 m/s | 9.07 rpm | 9.065 rpm (K = 0.0255764 N m/rpm², ROSCO Cp table at β = 0); generator 879 rpm, just above the 871 rpm Region-2 kink | right | own root solve |
| 81 | IEC class A σ at 8 m/s | 1.86 m/s | 0.16(0.75·8 + 5.6) = 1.856 | right | formula |
| 82 | rotor speed wander | 10.3 % | not rerun (turbulence + drivetrain simulation) | unclear, because the 40 records were not regenerated; value is typed by hand in make_numbers.py | — |
| 83 | Euler terms | about 2 parts in 10 000 | not rerun | unclear, because not reproduced | — |
| 84 | Jensen curve | P(Ω)/P(Ω₀) = 2/(1+Ω²/Ω₀²); convex; gain ≈ s²/2 | derived from (2.3) at fixed c and R−1 ≈ R; f''(1) = 1, f ≈ 1 − ε + ε²/2 | right | hand |
| 85 | Jensen number | s²/2 = 0.53 % | 0.530 % | right | arithmetic |
| 86 | square-law controller gains | 0.52–0.75 %; +0.58–0.68 %; −0.04 to +0.10 % | not rerun | unclear, because not reproduced | — |
| 87 | full controller | −2.03 %; mean speed +2.6 % | consistent: −2.6 % + 0.53 % ≈ −2.1 %; not rerun | unclear, because not reproduced | — |
| 88 | moving pivot term | adds 2Ω²w to g; rotation enters through the brake, a quarter turn out of step | forcing g + 2Ω²\|w\| on cosφ; stator rotation gives cΩs·sinφ | right | own SymPy Lagrangian with moving pivot and rotating stator |
| 89 | sag-only gains | 1.0, 6.0, 14.5 % | own nonlinear runs with the note's w, w′: +1.03, +6.01, +14.49 %; linear theory +1.17, +6.19, +14.69 % (the printed values are the nonlinear ones) | right | s8.py |
| 90 | net sag change (mode shape) | −0.4, −0.8, +0.5 % (lower/upper ends of ranges) | own nonlinear: −0.40, −0.77, +0.49 %; linear −0.30, −0.63, +0.66 %; agree within 0.2 pp as stated | right | s8.py |
| 91 | net sag ranges incl. static bend | −0.4 to −0.3; −0.8 to +0.1; +0.5 to +2.1 % | consistent with the stored static-bend runs (−0.26/−0.28, +0.09/+0.06, +1.99/+2.06 %); static runs not redone | unclear, because the static-bend power runs were not repeated | data file |
| 92 | tip sag and w | 47 cm; w = 31 to 384 mm | modal-shape estimate; my direct static integration of the blade table (g cos5°, ×1.02 for 1P): tip 43 cm, w = 37/170/362 mm | unclear, because the value depends on the shape model; my static route gives 43 cm | s7.py |
| 93 | tuned rod length | 1.11 m, 5.6× | 1.111 m, 5.56× | right | L = r_pΩ²/ω_e² |
| 94 | Sol's rod vs blade frequency | 2.4 times | 2.36 | right | arithmetic |
| 95 | R at 90 % | near 280 | 283.5 | right | arithmetic |
| 96 | gravity modulation | ±G/2R = ±9.6 % | 9.59 % (g), 9.56 % (g cos5°) | right | arithmetic |
| 97 | blade damping | 0.5 % | 0.477 % (Table 2-2) | right | primary source |
| 98 | gravity power at 90 % | 8.9 mW (Sol), 50 mW (tuned) | 8.90 / 50.2 mW with g cos5° (8.96 / 50.6 with g) | right | (2.5) |
| 99 | shaking powers | 0.11 W; 0.057, 0.912, 22.8 mW; double 0.71× | internally consistent (∝ amplitude²: 0.057·16 = 0.912, ·400 = 22.8); coupled model not rerun | unclear, because not reproduced | — |
| 100 | tuned rod numbers | 19.1 mW, 17 %, 9 %, 7.8 mW, 0.26 rad, 2.8 mW, 1.06 rad | 19.1/110 = 17 % consistent; model not rerun | unclear, because not reproduced | — |
| 101 | blade width | some 2.3 m | not checked against chord table | unclear, because not checked | — |
| 102 | RE 25 constants | R_c 1.53 Ω, k_t 20.8 mN m/A, 460 rpm/V, J 14.7 g cm², I₀ 40.2 mA at 10 900 rpm | all as on maxon product page 339152 | right | primary source |
| 103 | k_e | 60/(2π·460) = 0.02076 V s | 0.020759 | right | arithmetic |
| 104 | coil time constant | 0.12 ms | 0.186 mH / 1.53 Ω = 0.122 ms | right | primary source |
| 105 | c_sc without gearbox | 0.00028 N m s | 0.000282 | right | arithmetic |
| 106 | c* range | 0.17 to 1.00 N m s | 0.168 to 1.005 | right | arithmetic |
| 107 | "over a thousand times more" | c*/c_sc > 1000 | 597 to 3560 | wrong, because at the low end (400 rpm, 30 %) c* is only about 600 times c_sc; correct: "600 to 3 600 times" | arithmetic |
| 108 | ratio needed | at least 25 to 60 | √597 = 24.4, √3560 = 59.7 | right | arithmetic |
| 109 | "a small motor is built to give a few hundredths of that torque" | few hundredths of 0.1387 N m | RE 25 339152 nominal (max continuous) torque 30.4 mN m = 0.22 of 0.1387 N m | wrong, because the motor's continuous torque is about a fifth of the pendulum's torque, not a few hundredths | maxon product page |
| 110 | GP 32 C data | 80/75/70/60 % by stages; 0.7–1.5 g cm²; 51:1 three stages; 8000 rpm limit; backlash 1° | product pages: 14:1 and 33:1 two stages 75 %, 0.8 g cm², 0.8°; 51:1 and 111:1 three stages 70 %, 0.7 g cm², 1°; 8000 rpm. (1- and 4-stage pages not read) | right | primary source |
| 111 | j for 33, 51, 111 | 0.42, 1.00 (111 not printed) | 0.4220, 1.0014, 4.7436 | right | (7.3) |
| 112 | T₀ | ≈ k_tI₀ = 0.84 mN m | 0.836 | right | arithmetic |
| 113 | friction at 51:1 | 0.061 N m, 31 % of mgL = 0.196 N m | 0.0609 N m, 31.1 %, mgL = 0.19613 | right | arithmetic |
| 114 | jamming ratio | 164 (three-stage); 190, 246, 492 useless | 0.7·mgL/T₀ = 164.2; four-stage (η 0.6) 140.7; describing-function limit 129 | right | arithmetic |
| 115 | Table 2, 8 rpm 30 % | N 51, R_L 7.2 Ω, swing 0.446, rotor 27.28, (7.7) 7.98, full 8.34 mW, 29 % | 0.4460, 27.283, 7.981, 8.338 mW, 28.8 % | right | own (7.8) integration (LSODA, brentq for θ'', tanh bands 1e-3, 100+20 turns) |
| 116 | Table 2, 20 rpm 90 % | N 51, R_L 3.0 Ω, 0.061, 8.89, 1.80, 1.84 mW, 19 % | 0.0607, 8.886, 1.801, 1.840 mW, 19.1 % | right | same |
| 117 | Table 2, other rows re-run | 400/30, 400/90, 200/60 and the other 7 large-rotor rows | all match to the printed digits (e.g. 400/30: 0.037, 116.29, 41.15, 48.80, 85 %) | right | same |
| 118 | large-rotor summary | load 1.8–9.0 mW; 19–31 % of P*; 21–31 % of rotor; friction 33–39 % | 1.786–9.033; 18.7–30.8 %; 20.5–30.7 %; 33.0–38.8 % | right | rows 115–117 |
| 119 | sensor margin | at least 47 times | 1.786/0.0376 = 47.5 | right | arithmetic |
| 120 | formula vs full | within 9 % (large); fast: full 18 to 40 % more | +9.0 % (20/30); +18.6 % (400/30), +40.0 % (200/60) | right | rows 115–117 |
| 121 | "ratio 51 wins at 17 of 18" | from the full-equation scan | table consistent; my formula alone picks 33 at 400/30 and 14/30 and 111 at 400/90; full scan not rerun | unclear, because the full-equation scan over ratios was not repeated | g3.py |
| 122 | play marks | ±0.0087 rad; † at 2, ‡ at 7 mountings | 0.5° = 0.00873; counts 2 and 7 from the swings | right | arithmetic |
| 123 | sensitivity | ×2: 0.89–5.4; ×3: 0.48–2.5; η 0.5: 1.03–5.4; both: 0.41–2.0 mW; ≥ ~10× sensor; ratio moves to 33 or 14 | 0.893–5.436; 0.481–2.541; 1.026–5.416; 0.406–1.986; 10.8×; 33 and 14 | right | own formula optimisation g3.py |
| 124 | load voltage | "peaks at 88 to 326 mV" | full equation (8 rpm 30 % … 20 rpm 90 %): peak load voltage 553 mV … 130 mV; range over the 9 large rotors 130–553 mV. The rod sticks for 24–28 % of each turn (stick–slip), so peak speed is 1.5–1.7× the sine estimate the note uses (k_eNΩ·max\|θ\|·R_L/(R_L+R_c)) | wrong, because the swing is not sinusoidal; the full equation gives peaks of about 130 to 550 mV | g1.py, g2.py |
| 125 | voltage frequency | 0.13 to 0.33 Hz | 8/60, 20/60 | right | arithmetic |
| 126 | §0.4 "none typed in by hand" | every On-our-blade number computed from the model | make_numbers.py types '−0.128', '37.6' and '10.3' by hand, and takes 42.8/38 from the simulation page's file | wrong, because three numbers are typed in by hand (the −0.128 value itself is correct, row 60) | code read |
| 127 | §7.4 method description: smoothing | "each sign is smoothed over a band of a thousandth of the swing" | code: band = 1e-3 × max(swing, 0.01 rad) for sgn θ', and 1e-3 × G × that for sgn(xθ'); at 2 mountings the floor applies. Search over 14/33/51/111, factors 0.25–4 (capped at 0.98 c_sc), steady = halves within 1 %, swing < 0.5 rad, motor ≤ 8000 rpm: matches | wrong, because the band has a 0.01 rad floor and the power-direction band is scaled by G (minor; results unaffected at my check, rows 115–117) | L4_full.py, L4_scan.py, L4_check.py read line by line |
| 128 | §7.5 resonance | 51:1: R−1−j = 0.0040; 443 mW = 7.8 P* without gear loss on the inertia; with it at most 42.8 mW at 38 Ω | 0.00397; my v2 run 443.2 mW (7.76×); my v3 runs: 32.8, 40.4, 42.7, 41.3, 37.0 mW at 15, 25, 38, 55, 80 Ω | right | g4.py |
| 129 | §7.5 ratio 33 | j 0.42, net stiffness 1.01 → 0.58, rotor 116 mW (2× P* = 57.1), load 48.8 mW, 85 %, swing 0.037 | 0.4220, 1.0054 → 0.5834, 116.29, 48.80, 85.5 %, 0.0368 | right | g1.py |
| 130 | §0.2 "lose more than that, mostly to friction" | losses > half, mostly friction | load is 21–31 % of rotor power; friction is the largest single loss (≈ 47–49 % of losses), gears next, coil smallest | right | rows 115–116 energy split |
| 131 | §2.5/3.4 resonance power | several hundred mW, several times the best mounting | 263–379 mW regular, 4.6–6.6× | right | row 66 |

## Answers (23 October 2026)

1. Trail on the fast rotors: "stays at or below 0.051°" (key printed to three decimals).
2. Chaos powers: "2.0 to 6.6 times" (computed; fixed before this report arrived, in the r3 revision).
3. c* against c_sc: "600 to 3600 times" (computed, rounded to hundreds).
4. Motor torque: "a fraction of that torque (the RE 25's rated torque, 30.4 mN m, is about a fifth of it)".
5. Load voltage: now the full equation's peaks, 130 to 553 mV (L4_stick.json); the sticking (25–29 % of a turn) is stated.
6. "None typed in by hand": §0.4 now says the few inputs typed by hand are listed with their sources and a script checks every
   number. The −0.128 and 10.3 % are now computed (L0_r2.json, L2_scales.json, written by the scripts that compute them);
   37.6 µW is an input (Sol's sensor budget), marked as such.
7. Smoothing band described as in the code: a thousandth of the swing or of 0.01 rad, times G for the power's sign.
Unclear rows: the tip sag is now quoted as 43 to 47 cm (modal and static shapes); the other unclear rows were not rerun by the
checker and stay as computed by the study's scripts.
