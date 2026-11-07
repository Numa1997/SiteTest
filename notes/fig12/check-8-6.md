# Check of note §8.6, "Which motions of the stout each motor and spring can reach, and how many we need"

Page `public/simulations/beer-slosh.html`, lines 544–572 (working tree of 7 Nov 2026, 00:35 UTC; HEAD 6ecbcfa).
Code checked: `public/scripts/stout-cart.js` (Cart.suspGains, the `'joint'` branch of Cart.sample, Observer.discretise/update),
`tools/fig12/springs.cjs`, `notes/fig12/runs/springs-*.txt`.

**State of the tree.** Another session was editing while this check ran. At 00:33 `stout-cart.js` gained a clip on the reduced
model's second-order coordinates (p0, p2, r2) in the breaking rule (NMFluid, around line 1303), and `springs.cjs` gained the column
"cancellation asked" (uncommitted). Every number below was recomputed on the tree as of 00:35. The md5 sums of `stout-cart.js` and
`springs.cjs` were the same before and after the reruns.

How the checks were done:
- Equations: SymPy 1.14 for the derivations, SciPy 1.18 `solve_continuous_are(..., s=N)` for the Riccati equation, written
  independently of the page's Euler Riccati flow (script `/tmp/claude-0/-home-user-SiteTest/6f129354-04b4-5b64-8b76-38fa05cdb63e/scratchpad/check86.py`).
- Numbers: every NM command the section quotes was rerun in Node. The bumps/ISO/setts run behind Table 3b was rerun too. The key
  cases were also run with the page's own scripts (`window.StoutCart`, `GUINNESS_GLASS`, `STOUT_NM`) in headless Chromium
  (Playwright, page served by `notes/fig12/serve.cjs`), with 0 page errors. Node and Chromium agree to the last printed digit.
  The 3D numbers come from `notes/fig12/runs/springs-3d-washboard.txt`; the 3D runs were not repeated. The 00:33 change touches only the reduced
  model, so it does not affect them.

## Findings that need a change

| # | Line | What the note says | What is wrong | Correct value or wording |
|---|------|--------------------|---------------|--------------------------|
| 1 | 572 | "lean 126 mm, 321 g spilled; 130 mm and 168 g without the cancellation" | The spill values are stale. `runs/springs-nm-nosusp.txt` was made before the 00:33 clip on p0, p2, r2. The current code gives different spills (Node and Chromium agree): `UMAX=0`: lean 125.8 mm, **186.0 g**, tyre off 13.6 %; `UMAX=0 NOCANCEL=1`: lean 130.0 mm, **162.4 g**. The leans and the 12.60 A still hold. | "lean 126 mm, 186 g spilled; 130 mm and 162 g without the cancellation". Regenerate `notes/fig12/runs/springs-nm-nosusp.txt`. |
| 2 | 557 | "On every other road and speed the joint design leans no more than the motor alone, within 0.1 mm (the washboard at 1.2 and 1.4 m/s: 1.0 against 0.9 mm and 0.8 against 0.7 mm)" | The claim rests on leans rounded to 0.1 mm. Unrounded, the washboard at 1.2 m/s gives 0.993 against 0.876 mm, a difference of 0.117 mm. That is more than 0.1 mm. At 1.4 m/s the difference is 0.812 − 0.727 = 0.085 mm. ISO D also leans more with the joint design (0.764 against 0.740 mm), but the list leaves it out. Also, the "other roads" were run only at 1 m/s, so "every … speed" claims more than was run. | "On the other roads (at 1 m/s) and the other washboard speeds the joint design leans at most 0.12 mm more than the motor alone (washboard 1.2 m/s: 0.99 against 0.88 mm; 1.4 m/s: 0.81 against 0.73 mm; ISO D: 0.76 against 0.74 mm)". |
| 3 | 570 | "A sideways push (a person's gait sways a cup sideways, section 15)" | Section 15 ("What the model leaves out") says nothing about gait or a sideways push. It lists "Pitch and roll of the cart" and the swirl on the processor. The cross-reference points to nothing. | Point to section 11.9 (the swing across the road and the swirl). Or add a sideways push and gait item to section 15's list. |
| 4 | 559 | Caption: "The reduced model of section 11.9 on rough roads at 1 m/s (washboard at 0.85 m/s), 6 s" | The last row, "Washboard, 3D solver", is not the reduced model, and it ran for 4 s, not 6 s (the command on line 557 ends in `0.85 4`). | Add to the caption: "last row: the 3D solver on the processor, 4 s". |
| 5 | 551 | "their half difference holds the modes odd in cos θ … their half sum, the modes even in θ (m = 0, 2)" | Every cos mθ mode is even in θ, so "even in θ" does not pick out m = 0, 2. Also, "odd in cos θ" is not a defined parity. At θ = 0 and π the factor cos mθ is 1 and (−1)^m (checked in SymPy). The difference therefore holds every odd m and the sum every even m, not only m = 0, 2. | "their half difference holds the modes of odd m (m = 1, the swing along the road, and m = 3, …); their half sum, those of even m (m = 0, 2, …); every sin mθ mode, the swing across the road among them, is invisible to both". |
| 6 | 557 / 572 | Table 3b rows for bumps, ISO D and setts; the 12.6 A on line 572 | No command is quoted for the run behind these rows. The 12.6 A is printed only by the uncommitted `springs.cjs` (the "cancellation asked" column). At HEAD the tool does not print it. | Quote `node tools/fig12/springs.cjs nm bumps10,bumps25,isoA,isoB,isoC,isoD,setts off,speed,slosh,slosh+sky,joint 1 6` (it reproduces `runs/springs-nm-bumps-iso.txt` exactly). Commit the tool together with the note. |

Minor wording points (no number is wrong):
- Line 554: "1.1 Hz" and "41.7 Hz" are undamped natural frequencies, |p|/2π. The damped frequencies are 0.79 Hz and 41.4 Hz. Writing "natural frequency" once would remove the ambiguity.
- Line 556: "(exact linearisation by feedback) … wherever q̂ = q". The cancellation also lags by the 2 ms current loop (τ_I), because (B3) sets the command, not the current. The suspension force follows its command with τ_U = 5 ms, and the LQR of (B2) leaves that lag out. Neither changes a result, but "exact" should say "up to the current loop's 2 ms lag".
- Line 556: the filter recomputes both A_d and B_d with ω²(1 + a_z/g). Q_d is kept, as the code's comment says. The note mentions only A_d. That is true but incomplete.
- Line 552/554: the stroke, the two vertical speeds and a_z are fed back as exact values. The tyre term d comes from the load cell, (N − N₀)/k_t, so it includes the tyre damper's share c_t(ż_a − v_w), and it is clipped when N = 0. The code's comment states this; the note does not. That is acceptable for a lecture note.

## Equations

| Item | Verdict |
|------|---------|
| (B1) q̈ + 2ζωq̇ + ω²(1 + a_z/g)q = −βa_x | **verified.** It is (54) for n = 1 (line 655). The stiffness term follows from ω² = (g + a_z)k tanh kh = ω₀²(1 + a_z/g), since SymPy gives a difference of 0. Every term has units of m/s² (β is dimensionless). Limits: a_z = 0 gives (17) with damping; a_z = −g (free fall) gives zero stiffness, as it should. The code matches: NMFluid's `-w*w*gf*q … - beta*ax`. |
| Text 549, forcing overlaps | **verified.** ∫₀^{2π} cos θ cos mθ dθ = π for m = 1 and 0 for m = 0, 2, 3, 4. ∫ cos θ sin mθ dθ = 0 for every m. ∫ cos mθ dθ = 0 for m ≥ 1. For m = 0, ∫₀^R J₀(ξr/R) r dr = R²J₁(ξ)/ξ, which is 0 exactly when J₀′(ξ) = 0, that is, for the volume-conserving modes. |
| Text 550, controllability | **verified** (within the stated linearisation about q = 0 on a level road). Block (v, q, q̇) from i: det of the controllability matrix = −b³β²ω²/M_x³, nonzero for β ≠ 0. With two modes (ζ = 0): det ∝ β₁²β₂²ω₁²ω₂²(ω₁² − ω₂²)², nonzero for distinct frequencies, as the note says. Block (s, v_b, v_w, d) from u: det = k_t²/(M_s²m_w⁴) ≠ 0. The plant is block-diagonal, so every Aⁿb_u has zeros in the swing's rows. |
| (B2) J_s and a_z = (−ks − c(v_b − v_w) + u)/M_s | **verified.** a_z matches `Ca`, `Da` in suspGains and M_s v_b′ in the model comment. The integrand is dimensionless. The cross-term Riccati equation and u = −R⁻¹(BᵀP + Nᵀ)y match the code (`G = PB + N`, `d = Q − GGᵀ/R + AᵀP + PA`, `K = (BᵀP + Nᵀ)/R`). With J = ∫(waa_z² + …), N = wa Caᵀ Da and R = wa Da² + 1/u_max², as in the code. Limit u_max → 0.01 N gives K_s → (−0.03, 0.008, −0.0008, 0.07), so the force vanishes. |
| K_s = (−502.6, 11.6, −6.1, 612.6) | **verified.** SciPy CARE: (−502.621, 11.632, −6.091, 612.630). The page's `suspGains()` gives the same in Node and in headless Chromium, to 1e-9. M_s = 1.5 + 0.42660 kg. Units are N/m, N s/m, N s/m and N/m, consistent with y = (m, m/s, m/s, m). |
| Closed-loop poles −4.9 ± 5.0j, 1.1 Hz, ζ 0.70 | **verified:** −4.937 ± 4.977j; |p| = 7.010 rad/s = 1.116 Hz; ζ = 0.704. |
| Poles −32 ± 260j, 41.7 Hz, 0.12 | **verified:** −31.98 ± 259.91j; |p|/2π = 41.68 Hz; ζ = 0.122. |
| "cancels 84 % of the spring (600 N/m)" | **verified:** 502.62/600 = 0.838. |
| tyre's static compression 1.1 mm | **verified:** (M_s + m_w)g/k_t = 2.2266 × 9.81/2·10⁴ = 1.092 mm. |
| (B3) i_par = −(M_xω²/βb)(a_z/g)q̂ | **verified.** −βb i_par/M_x = +ω²(a_z/g)q̂, so the residual against the parametric term with q̂ = q is 0 (SymPy). Units: kg·s⁻²·m/(N/A) = A. Limit a_z = 0 gives i_par = 0. The code (line 1597) matches: `-massX()*w²*(azMeas/g)*s[1]/(beta*b)`, with s[1] = q̂ and b = N_gear K_m/R_w = 5 N/A. |
| Text 556, filter uses ω²(1 + a_z/g) every sample | **verified** (see the minor point on B_d and Q_d). `obs.update(..., azMeas)` is called only for `'joint'`, and `discretise(az)` recomputes A_d and B_d. |

## Numbers

| Line | Number | Verdict |
|------|--------|---------|
| 554 | a_max 0.5, s_max 10 mm, d_max 0.2 mm, u_max 40 N | verified (`suspLimits` default; `Umax = 40`) |
| 554 | a_max 0.2 with d_max 1 mm: heave lower, wheel off the setts 2.6 %, lean grew | verified by measurement (no run file records it). Setts at 1 m/s, joint, `suspLimits {a:0.2,d:0.001}`: heave 0.474 against 0.769 m/s², tyre off 2.58 %, lean 6.60 against 5.24 mm (Chromium). |
| 557 | ripples pass at 2.8 Hz, the body's own bounce | verified: 0.85/0.30 = 2.83 Hz; √(k/M_s)/2π = 2.81 Hz; open-loop body pole with the tyre at 2.77 Hz |
| 557 | slosh only, 0.85 m/s: stroke 23 mm rms, 41.6 max, 11.1 with no controller, heave 7.6, wheel off 9.7 %, lean 103 mm, 75 g | verified (23.43, 41.6, 11.13, 7.56, 9.7 %, 102.6, 75.4) |
| 557 | joint: stroke 7.0 mm rms, force 3.9 N rms, heave 1.1, lean 1.0, nothing spilled | verified (6.96, 3.91, 1.118, 1.024, 0.0) |
| 557 | 3D slosh: stroke 28 mm rms, wheel off 19 %, lean 32 mm, 0.7 g | verified from the run file (28.22, 19.1 %, 32.1, 0.7) |
| 557 | 3D joint stroke 7.0, lean 5.4; skyhook 3.8 | verified from the run file (6.99, 5.4, 3.8) |
| 557 | within 0.1 mm; 1.0/0.9 and 0.8/0.7 | **wrong**, see finding 2 (0.117 mm at 1.2 m/s) |
| 557 | stroke 3.64 mm rms over a 10 mm bump with or without the slosh feedback; joint halves it | verified (speed 3.640, slosh 3.645; joint 1.702, ratio 0.47). In the 6 s run the cart crosses three 10 mm bumps (x = 1, 3, 5 m), not one. |
| 560 | Bump 10: 0.5, 3.64 / 0.5, 1.65 / 0.5, 1.70 | verified |
| 561 | Bump 25: 1.7, 9.26 / 1.5, 4.19 / 1.4, 4.33 | verified |
| 562 | ISO D: 0.7, 3.53 / 0.8, 3.46 / 0.8, 3.86 | verified |
| 563 | Setts: 5.3, 3.51 / 5.5, 1.64 / 5.2, 1.64 | verified |
| 564 | Washboard 0.85: 102.6, 23.4 / 1.1, 7.17 / 1.0, 6.96 | verified (23.43 is shown with one decimal and the other cells with two, but the value is right) |
| 565 | Washboard 3D: 32.1, 28.2 / 3.8, 7.21 / 5.4, 6.99 | verified from the run file; the caption is wrong for this row (finding 4) |
| 572 | lean 126 mm, 321 g; 130 mm, 168 g | **wrong, because** the current code gives 125.8 mm, 186.0 g and 130.0 mm, 162.4 g (finding 1) |
| 572 | up to 12.6 A, four times what the drive can give | verified (12.60 A; Imax 3 A; ratio 4.2); printed only by the uncommitted tool |
| 572 | with the suspension: lean 1.0 mm, 0 g, with or without the cancellation | verified (1.024 and 1.026 mm, 0.0 g both) |

## Method description against the code

| Claim | Verdict |
|-------|---------|
| Motor part = slosh LQR of §8.4 on the Kalman estimate plus i_par (line 556) | verified (lines 1596–1600 use the same `lqrGains()`, the same integral and anti-windup as `'slosh'`, plus `ipar`) |
| Suspension u = −K_s y, y = (s, v_b, v_w, d), clipped to ±40 N (lines 552–554) | verified (lines 1601–1608). d is measured as (N − N₀)/k_t (see the minor points). The force reaches the body through the 5 ms lag `tauU`, which the note does not mention. |
| a_z from the body accelerometer (line 551) | verified (`azMeas = this.azb`, taken at each sample, without noise) |
| "The page runs this as 'Motor + suspension (one LQR)'" | verified (button label in the page) |
| UMAX=0 removes the suspension's force; NOCANCEL=1 drops (B3) | verified (`Umax` clip in the joint branch; `parCancel === false` gives i_par = 0) |
| Quoted command for the washboard sweep | verified: it reproduces `runs/springs-nm-washboard.txt` exactly (apart from the wall-clock time) |
