# Check of §8.5 "Seeing the swing: two level probes and a Kalman filter", the edited end of §8.4, and Table 3

Page: `public/simulations/beer-slosh.html`, branch `claude/fig12-realtime-fluid`, uncommitted working tree, checked 6 November 2026.
Code: `public/scripts/stout-cart.js` (`Observer`, `World.readProbes`, `Cart.sample`, `Cart.lqrGains`), `public/scripts/stout-view.js`, and the page's own script.
No file except this one was changed.

How I checked:
- I re-derived the equations in SymPy 1.14. I recomputed A_d, B_d, Q_d, the LQR gains, the poles and the periodic Kalman gain independently: SciPy `expm`, direct quadrature, `solve_continuous_are`, and my own Kalman recursion. Script: `/tmp/claude-0/-home-user-SiteTest/91e62847-1a1a-5a7d-b603-4662585b11e7/scratchpad/tools/check.py`.
- I re-ran every cited command, plus the `control.sh` set, into `/tmp/claude-0/-home-user-SiteTest/91e62847-1a1a-5a7d-b603-4662585b11e7/scratchpad/runs/`. Every stored file in `notes/fig12/runs/observer-*.txt` and `control-3d-*.txt` reproduces exactly (only the wall-clock seconds differ).
- I ran an ideal-sensor variant of the live model (the observer's output replaced by the true v, q1, q̇1): `/tmp/claude-0/-home-user-SiteTest/91e62847-1a1a-5a7d-b603-4662585b11e7/scratchpad/tools/ideal.cjs`.
- I measured the slow-motion rate in headless Chromium, served by `notes/fig12/serve.cjs` with cross-origin isolation (`crossOriginIsolated` true, 4 cores): `/tmp/claude-0/-home-user-SiteTest/91e62847-1a1a-5a7d-b603-4662585b11e7/scratchpad/tools/slow.cjs`.

## Equations

| Item | Verdict |
|---|---|
| (53a) y_q = ½[η(r_p,0) − η(r_p,π)] + n_q = q + e + n_q | **confirmed.** SymPy gives η(R,θ) = q cosθ and a half difference of q. In the live model every mode n has J1(ξ1n)/J1(ξ1n) = 1 at the wall, so e = q2 + q3 (`ModalFluid.wallLift`, (55)). Code: `readProbes` gives y = ½(ef − eb) + n at r = Rz(h0) = 39.1 mm, θ = 0 (+x, the direction of travel) and π. Units: m. |
| (53b) A_z, B_z, G | **confirmed.** SymPy takes the Jacobians of v̇ = (b i − c_x v + F_d)/M_x and q̈ = −ω²q − 2ζωq̇ − βv̇ + a_q, and they equal the printed matrices. `Observer.design` has the same matrices. Units are consistent: W_F in N² s (force white noise), W_a in m² s⁻³ (acceleration white noise). **Omission:** the derivation takes a_z = 0 in (17). Over the bump the heave is large (study.cjs: a_z up to 9.3 m/s² on the 25 mm bump), so the parametric term ω²(a_z/g)q is not small. It belongs to a_q, but the text's list of what a_q covers does not name it. |
| (53c) A_d = e^{A_zT_s}, B_d = ∫e^{A_zs}ds B_z, Q_d = ∫e^{A_zs}GWGᵀe^{A_zᵀs}ds | **confirmed.** The exponential of [[A_z, B_z],[0, 0]]T_s matches quadrature to 1e-18. Q_d from Van Loan matches direct quadrature to a relative 3e-16. The A_d diagonal and Q_d diagonal reproduce the observer.cjs print. |
| Van Loan block statement: exp([[−A_z, GWGᵀ],[0, A_zᵀ]]T_s) has A_dᵀ in the lower right and A_d⁻¹Q_d in the upper right | **confirmed.** In general the upper-right block is ∫e^{−A(T−s)}GWGᵀe^{Aᵀs}ds = e^{−AT}Q_d. SymPy checks the scalar case symbolically (difference 0), and the 3×3 case agrees numerically (lower right − A_dᵀ: 6e-17). The code computes `Qd = Ad · F12`, which is consistent with this. |
| "ω T_s = 0.020" | **confirmed** for the 3D plant (0.0202). The live plant gives 0.0215. |
| "the data panel checks all three by integrating … with Runge–Kutta" | **confirmed.** The page script's `discrete()` integrates Φ' = AΦ, Γ' = ΦB and Q' = ΦGWGᵀΦᵀ by RK4 in 2000 substeps, and `C.Ad`, `C.Bd` and `C.Qd` use it. |
| (53d) prediction | **confirmed** against `Observer.update` (xp = A_d x + B_d u; Pp = A_d P A_dᵀ + Q_d). **Method caveat:** u is `cart.uPrev`, the measured current at the previous sample. The drive holds the command, not the current: in `Cart.step` the current relaxes to it with τ_i = 2 ms. So "holds the current in between" and "with i held" describe the model, not the plant. The zero-order hold on i is an approximation. |
| (53e) innovation, gain, update | **confirmed** against the code: H rows [0] or [0,1], S = HP⁻Hᵀ + R, L = P⁻HᵀS⁻¹. The scalar limit L = P⁻/(P⁻ + σ²) is confirmed (SymPy). |
| (53f) Joseph form, "equals (I − LH)P⁻ in exact arithmetic" | **confirmed.** For the optimal L, SymPy reduces the difference to zero for a general symmetric 3×3 P, with both the two-sensor H and the speed-only H. The code builds the Joseph form exactly and then symmetrises it. |
| Regulator on the estimate, "The current is (53) with the estimate in place of the state" | **wrong reference.** (53) is the Riccati equation. The control law is the unnumbered u = −K**x** of §8.4, with K from (53). The law i = i0 − K(v̂ − v0, q̂, q̂̇, ξ_i) matches `Cart.sample`. **Method note:** ξ_i integrates e = v0 − `this.vx`, the solver's true speed, not the encoder reading y_v. With Sensor noise on, the integral therefore does not see the encoder noise. "Which it knows exactly" holds only because it reads the true speed. |
| Separation principle sentence | **confirmed** as the standard LQG result. Strictly it holds for the linear model only. Here the LQR is a continuous-time design run at 1 ms on a plant (3D fluid, current lag) that the model does not describe exactly. |
| Breaking amplitude a = g/ω² = R/ξ11 = 21.2 mm, lean 42 mm | **Arithmetic confirmed:** R(h) = Rz(0.125 m) = 39.1 mm, ξ11 = 1.841184, so R/ξ11 = 21.24 mm. With the live ω = 2π·3.4207 Hz, g/ω² = 21.24 mm (tanh(ξh/R) = 0.99998). The lean 2a = 42.5 mm. **Caveats:** (i) g/ω² = R/ξ11 holds only for the deep cylinder. For the 3D plant's own 3.214 Hz, g/ω² = 24.1 mm (lean 48 mm), still below the 61 mm reached, so the conclusion stands. (ii) The threshold aω² = g is the linear estimate of the free-fall crest criterion. **Unverifiable here:** I did not read Taylor 1953. The nonlinear limiting standing wave (Penney & Price 1952, H/λ ≈ 0.218, ka ≈ 0.69) would put the limit lower, near 0.69·R/ξ11 ≈ 15 mm. |

## Numbers in §8.5

| Number | Verdict |
|---|---|
| Sensor noise 1 mm per probe, 0.2 mm/s on the speed, seeded | **confirmed.** `setNoise`: noiseQ 0.001 m, noiseV 0.0002 m/s; `Rng(seed 12)`. |
| Probes at rest: sd 0.08 mm about an offset of 0.39 mm | **confirmed.** `node tools/fig12/observer.cjs 3d` gives a y_q mean of 0.393 mm and sd of 0.075 mm (400 readings). |
| "a single swing fitted to the reading misses it by 1–2 mm rms" (linfit.cjs on linearity.cjs) | **wrong.** linfit.cjs fits the *lean* (front − back), not the reading y_q. The 3D misfits are 1.21, 2.04 and 2.37 mm for A = 0.5–2 m/s², and 3.79 and 6.53 mm for 4 and 6 m/s². On y_q, the quantity the sentence and σ_q refer to, that is 0.6–1.2 mm (A ≤ 2 m/s²), and up to 3.3 mm at 6 m/s². Command: `node tools/fig12/linfit.cjs notes/fig12/runs/linearity-3d-{a,b,c}.json`. |
| σ_q = 0.8 mm, σ_v = 2 mm/s, W_F = 0.5 N² s, W_a = 0.002 m² s⁻³ | **confirmed** (`World` sensor defaults). |
| W_F estimate: "a 25 mm bump changes the speed by about 0.1 m/s in 0.1 s on 2.5 kg, so W_F ≈ (0.25 N s)²/0.1 s" | **Arithmetic confirmed:** 2.5 × 0.1 = 0.25 N s, and 0.25²/0.1 = 0.625 N² s ≈ 0.5. M_x = 2.5016 kg. **Premise wrong:** in open loop (F_d acting alone) the 25 mm bump drops the speed by 0.30 m/s in about 0.11 s (1.000 → 0.700 m/s between t = 0.385 and 0.50 s, in `notes/fig12/runs/control-3d-bump25-off.json`, column v; live model 0.700–1.000 m/s from `MODAL=1 node tools/fig12/study.cjs 25 off 0`). That is an impulse of 0.75 N s, so W_F ≈ 0.75²/0.11 ≈ 5 N² s, ten times the chosen value. Under PI the drop is 0.05 m/s and under slosh feedback 0.01 m/s, so no case gives 0.1 m/s. |
| "a force of a few newtons within a tenth of a second" | **confirmed** as the meaning of W_F = 0.5: √(0.5/0.1) = 2.2 N. The real bump force peaks near 8 N (M_x × 3.3 m/s²). |
| W_a: "rate may drift by about 0.02 m/s over a period" | **confirmed.** √(W_a T) = 0.025 m/s (3.214 Hz) and 0.024 m/s (3.421 Hz). |
| Live plant ω = 2π × 3.421 s⁻¹, ζ = 0.0053 | **confirmed** (3.42067 Hz, 0.005349). |
| 3D plant 3.214 Hz, ζ = 0.008; 3 mm grid 3.263 Hz and 0.002 | **confirmed** as the constants in `World` (taken from §12; I did not re-measure them). |
| "A filter tuned to 3.42 Hz would drift out of phase with the 3D stout by a sixth of a swing every five swings" | **wrong.** (3.421 − 3.214) × 5/3.214 = **0.32 swing, about a third**, every five swings. A sixth is reached after about 2.6 swings. Even against the 3 mm grid (3.263 Hz) the drift is 0.24 swing. |
| β = 1.541 | **confirmed.** 2ξ tanh(ξh/R)/(ξ² − 1) = 1.54074 (observer.cjs prints 1.5407 for both plants). |
| P settles into a 5-sample cycle "after a few hundred samples" | **confirmed.** Gains are within 0.1 % of the cycle from sample 244 (my recursion). |
| Probe-sample gain 0.143 (q) and 2.19 s⁻¹ (q̇), 3D; 0.139 and 2.08 s⁻¹, live | **confirmed.** The run file gives 0.1429, 2.187 and 0.1394, 2.075, and the independent recursion gives 0.14292, 2.18669 and 0.13940, 2.07503. |
| Estimate sd 0.30 mm (q), 9.7 mm/s (q̇) | **confirmed:** 0.302 mm and 9.72 mm/s (3D), independently reproduced. |
| "averages about seven probe readings" | **confirmed.** 1/L_q = 7.00, and σ_q²/P_qq = (0.8/0.302)² = 7.00, so the posterior variance equals that of a mean of 7 readings (live: 7.17). Seven readings span 35 ms, about 0.11 of a 0.31 s period. |
| 3D gains K = (76.7, −1934, −41.3, −150), poles −11.3 ± 7.5j, ζ = 0.83 | **confirmed.** observer.cjs gives 76.69, −1934, −41.32, −150.0; poles −11.33 ± 7.54j, −2.57, −256.4; ζ = 0.832. SciPy CARE gives 76.686, −1933.99, −41.316, −150.000 and the same poles. |
| Fit window "the next 1.45 s", ζ = σ/√(σ² + ω_d²) | **confirmed** (control.cjs: t ∈ (t_on + 0.05, t_on + 1.5] s). Note that the scan constrains σ ≥ 0, so "ζ = 0.000" means the fit sat on its lower bound. |

## Table 3a (against `notes/fig12/runs/control-3d-*-on1-*.txt`, re-run identically with `ON=1 node tools/fig12/control.cjs 3d <push10|25> <off|speed|slosh> 0.004 3.5`)

| Cell | Verdict |
|---|---|
| Caption "rms lean in the last second of 3.5 s" | **confirmed:** T = 3.5 s in control.sh. |
| Push row, "lean 45 mm" | **confirmed:** peak 45.3 mm. |
| Push, open loop: ζ = 0.000, 15.7 mm | **confirmed:** 0.000, 15.69 mm. |
| Push, PI: ζ = 0.027, 15.1 mm | **confirmed:** 0.027, 15.13 mm. |
| Push, slosh: ζ = 0.70, 3.2 mm | **confirmed:** 0.702, 3.20 mm. The fitted frequency is 0.95 Hz, a heavily damped fit, not the 3.2 Hz swing. |
| Bump row, "lean 61 mm" | **confirmed:** 60.7 mm. |
| Bump, open loop: ζ = 0.012, 27.3 mm | **confirmed:** 0.012, 27.33 mm. |
| Bump, PI: "still swinging, 34.9 mm" | **wrong:** the run gives **ζ = 0.021, 44.1 mm** (residual rms 44.07 mm, 24.6 g spilled) in `control-3d-bump25-on1-speed.txt`. 34.9 mm (34.95) is the *live* model's open-loop residual for the 25 mm bump (`node tools/fig12/control.cjs modal 25 off 0.004 2.3`), so it looks copied from the wrong line. |
| Bump, slosh: ζ = 0.35, 5.8 mm | **confirmed:** 0.350, 5.82 mm. |

## The paragraph after Table 3a

| Claim | Verdict |
|---|---|
| Slosh on from the start, 25 mm bump: lean "stays below 3.2 mm" | **imprecise:** the largest lean is 3.2 mm (1.6 mm during, 3.2 mm after; `control-3d-bump25-slosh.txt`). It reaches 3.2 mm; it does not stay below it. |
| Open loop 61 mm, PI 35 mm | **confirmed:** 60.7 and 35.4 mm. |
| Estimate follows the probes to 0.7 mm rms | **confirmed:** 0.70 mm. |
| Command `ON=1 node tools/fig12/control.cjs 3d push10 slosh` | **wrong command for the table:** the default run length is 3.0 s, which gives a residual of **1.73 mm** (and an estimate error of 2.22 mm), not 3.2 mm. Table 3a needs `ON=1 node tools/fig12/control.cjs 3d push10 slosh 0.004 3.5` (as in `notes/fig12/runs/control.sh`). The second command, `node tools/fig12/control.cjs 3d 25 off,speed,slosh`, does reproduce 61/35/3.2/0.7. |
| "3–6 mm rms stays" | **confirmed** (3.20 and 5.82 mm). |
| "…a little above what the probes read at rest" | **wrong:** at rest the probes read a lean of 2 × 0.393 = 0.79 mm, with sd 0.15 mm. 3.2–5.8 mm is 4–7 times that, not "a little above". |
| Estimate misses the probes by 3.9 mm rms (bump) against 2.2 mm (push) | **confirmed:** 3.86 and 2.19 mm (whole run, including the open-loop second). |
| "the decay is slower (ζ = 0.35 against 0.70)" | **wrong as worded:** ζ is lower, but the envelope decays *faster* for the bump (σ = 9.42 s⁻¹ against 5.90 s⁻¹). The ratio is lower because the fitted frequency is higher (4.01 Hz against 0.95 Hz). Say "less damped per cycle", not "slower". |
| "its errors are of the size of the swing it is removing, not larger" | **unclear/unsupported:** the estimate errors (3.9 mm rms) are an order of magnitude *smaller* than the swing (a 61 mm lean). |

## Slow-motion paragraph

| Claim | Verdict |
|---|---|
| "about 0.31 s of motion per second on a 4-core computer (section 11)" | **unverifiable as stated (machine-dependent); not reproduced here.** In headless Chromium on this 4-core machine, with threads on and `?grid=4`, the mean was **0.236 s/s** over 20 s, and the readouts showed ×0.23–0.28. §11 itself says "roughly a third". |
| "SLOW MOTION ×0.27 in the figure, the rate … in the caption" | **confirmed** as behaviour. The figure showed "SLOW MOTION ×0.24", and the caption "slow motion ×0.24: 0.24 s simulated per s, measured on your computer". The live model shows "real time" (1.000 s/s) and no figure label. ×0.27 is within the range seen. |
| Controller's 1 ms samples run in simulated time | **confirmed:** `Cart.step` counts `tSample` in simulated time. |

## Probes, as drawn and as read

| Claim | Verdict |
|---|---|
| Dark strips with a white dot at the reading | **confirmed** (`stout-view.js`: strip rgba(28,21,24,0.75), white 3 px dot at η). |
| Probes read after every fluid step (5 ms); one sample in five | **confirmed:** `dtMax` = 1/200 on the page; `readProbes` runs at the end of `World.advance`'s step. Detail: the reading is fused at the next sample, 0.9 ms after the step ends (samples fall at 0.9, 1.9, … 4.9 ms within a step), and is treated as current. This is negligible. |
| r_p = R(h) | **confirmed**, with h the rest fill height h0 (`Rz(min(h0, zRim))`), not the current level after spilling. |

## The edited end of §8.4 and Table 3

| Item | Verdict |
|---|---|
| "the page uses that path in both models, so the regulator never reads the stout's state from the solver" | **confirmed:** the slosh branch of `Cart.sample` uses only `obs.update`'s output, and the slosh button is now enabled for 3D. Caveat: the integral ξ_i uses the solver's true speed (see above). |
| Table 3 leans (24.7, 7.6, 0.8, 0.5 / 73.9 + 9.9 g, 25.4, 5.9, 1.7 mm) | **confirmed:** `MODAL=1 node tools/fig12/study.cjs <10\|25> <off\|speed\|preview\|slosh> 0`. |
| Table 3 currents (0.40, 1.06, 1.01, 1.03 / 2.32, 2.16, 2.25 A) | **confirmed:** the values come from `node tools/fig12/control.cjs modal <10\|25> off,speed,preview,slosh 0.004 2.3` (max current). **Command caveat:** the command the note cites, study.cjs, does not print any current, so those values cannot be reproduced from it. |
| "ninefold", "fifteenfold" | **confirmed:** 7.6/0.8 = 9.5 and 7.6/0.5 = 15.2. |
| "with the swing read directly from the model, an ideal sensor, it was 0.4 and 1.3 mm" | **confirmed:** the current code with the observer's output replaced by the true (v, q1, q̇1) gives 0.42 and 1.29 mm (and 1.04 and 2.31 A, the old table's currents). |
| §8.4 unchanged numbers K = (75.0, −1939, −38.8, −150), poles −12.0 ± 8.8j, −2.6, −244, ζ 0.81 | **confirmed** (`observer.cjs modal`; SciPy CARE: 75.035, −1938.94, −38.813, −150; −12.011 ± 8.819j, −2.557, −243.95). |

## Errors found
1. Table 3a, PI after the 25 mm bump: "still swinging, 34.9 mm" should be **ζ = 0.021, 44.1 mm**. 34.9 is the live model's open-loop value.
2. "drift out of phase … by a sixth of a swing every five swings" should be **about a third (0.32 swing)**.
3. The W_F premise "a 25 mm bump changes the speed by about 0.1 m/s in 0.1 s" is wrong: the measured drop is 0.30 m/s in 0.11 s in open loop, which implies W_F ≈ 5 N² s. The arithmetic itself is right.
4. "a single swing fitted to the reading misses it by 1–2 mm rms": linfit.cjs measures the lean. On y_q the misfit is 0.6–1.2 mm (3D, A ≤ 2 m/s²); on the lean it is 1.2–2.4 mm.
5. The cited command `ON=1 … control.cjs 3d push10 slosh` runs 3.0 s and gives 1.73 mm. Table 3a needs the arguments `0.004 3.5`.
6. "3–6 mm rms … a little above what the probes read at rest": at rest the lean reads 0.79 mm, so this is 4–7 times that.
7. "the decay is slower (ζ = 0.35 against 0.70)": σ is larger for the bump (9.4 against 5.9 s⁻¹). The swing is less damped per cycle, not slower to decay.
8. "The current is (53) with the estimate…": (53) is the Riccati equation, not the control law.
9. Smaller points:
   - "stays below 3.2 mm" (the maximum is 3.2 mm).
   - "errors of the size of the swing" (they are about 10 times smaller).
   - The Table 3 current column cannot be reproduced from the cited study.cjs.
   - "holds the current" (the drive holds the command; the current lags with τ_i = 2 ms).
   - ξ_i integrates the true speed, not the encoder reading.
   - (53b) leaves out the heave term ω²(a_z/g)q without saying so.
   - 0.31 s/s is not reproduced here (0.24 s/s measured).
   - The breaking threshold is a linear estimate; Taylor 1953 was not read.
