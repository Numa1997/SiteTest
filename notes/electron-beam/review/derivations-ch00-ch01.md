# Check of chapters 0 and 1: equations, units, limits, numbers, method

Page: `public/portfolios/electron-beam/index.html`, elements `#ch00` and `#ch01` (as built on 9 November 2026, 20:16).
Sources read: `portfolios-src/electron-beam/text/ch00.py`, `text/ch01.py`, `physics/ch00.js`, `physics/ch01.js`, `ref/ch00.py`, `ref/ch01.py`, `ref/core.py`, `derive/ch01.py`, `contract.json`, `data/ch01/thomson1897.json`.

How it was checked.

- **Equations.** Each one was derived again in SymPy 1.14 from its premises. The script is my own and does not use `derive/ch01.py`. Units and limiting cases were then checked by hand. `derive/ch01.py` was also run, and all 23 of its checks pass.
- **Numbers, three ways.**
  1. I loaded the built page in headless Chromium (Playwright) and read the rendered text of `#ch00` and `#ch01`.
  2. Inside that page, I ran every declared number through the page's own `window.EB.ch00.compute` / `EB.ch01.compute`, using the inputs given in `text/ch0N.py`. Every expression was evaluated in the same browser and formatted with `EB.core.fmt`. All 436 declared numbers reproduce the strings the page prints. So the pipeline is faithful, and every error below is an error of physics or of convention, not of transcription.
  3. Independently, I recomputed the numbers with mpmath at 30 digits from my own formulas. For the plate deflection I used the exact closed-form relativistic motion in a uniform transverse field.
- **Sources.** Thomson (1897) was read in the Giunta transcription. IRDS 2022 *More Moore* and *Lithography* were read from the IEEE PDFs (Table MM-7 is an image on PDF page 13; I rendered it and read it). The Applied Materials pages could not be read: the direct fetch got 403 "Access Denied", and the Wayback Machine connection was reset.

## Status: the page was rebuilt while this check ran

Another session changed `text/ch01.py` (20:28) and `physics/ch00.js`, and rebuilt the page (20:33). I read the rebuilt page in Chromium again and recomputed its numbers from its own code.

**Fixed in the 20:33 build.** These now print exactly the corrected values given below:

- E2 to E6: 0.01795 m; 0.39 %; 1.577 × 10⁻⁴ %; 1.7479 × 10¹¹ C/kg; 0.08330 rad; 0.62 %; 0.99380; 1.2 × 10⁻¹⁴; 0.99769.
- E7: Figure 1.1 is now drawn from `plate_path(-E_TUBE, ...)`, so the path bends up, towards the positive upper plate.
- E13: the chapter 0 simulation caption now says "smallest period (pitch)".
- E1, partly. `text/ch01.py` now passes −E and −B_p to the solver. The simulation slider labels in `contract.json` still say E is "along +y in chapter 1" and B "along +z in chapter 1", but §1.3 puts them along −y and −z. Still open.

**Still open in the 20:33 build.** E8, E9, E10, E11, E12, the slider-label part of E1, and the minor points m1 to m13. m3 now reads "+1.58 × 10⁻⁸ µm"; the label point stands.

The tables below record the build of 20:16 that this check started from. Where a cell says "wrong, because of E1", the 20:33 build prints the correct value given in that cell.

## Summary of errors

| # | where | what is wrong | correct |
|---|---|---|---|
| E1 | §1.3 vs `physics/ch01.js` (root cause of E2 to E7) | The text puts E = (0,−E,0) and B = (0,0,−B_p), so the electron is pushed towards **+y**, the upper (positive) plate. The solver, `contract.json` and the simulation's slider labels ("along +y in chapter 1", "along +z in chapter 1") put E along **+y** and B along **+z**. The electron then goes to **−y**. The prose uses the solver's `y_end` and `theta_end` without changing their sign. | Use one convention. Either take −y_end and −theta_end in `text/ch01.py`, or state the solver's convention in §1.3 (upper plate negative) and correct the slider labels. |
| E2 | Example 1.1 | "the solver … puts the spot at y_s = −0.01795 m" | y_s = **+0.01795 m** (exact relativistic motion: 0.0179518 m) |
| E3 | Example 1.1 | "The gap of −200 %" | **+0.39 %** (0.3915 %), which is γ − 1 = 0.391 %, as the text then argues |
| E4 | Example 1.1 | "within 200.0 % of the solver" | within **1.577 × 10⁻⁴ %** (0.00016 %) |
| E5 | §1.9.1 | e/m = θE/(B²l) = "−1.7479 × 10¹¹ C/kg" from θ = "−0.08330 rad"; "returns it to 200 %"; "measured ratio −0.99380"; "to 2.0"; "brings the ratio to −0.99769" | e/m = **1.7479 × 10¹¹ C/kg** from θ = **0.08330 rad**. It returns e/m to **0.62 %**. The ratio is **0.99380**, and the product of the two factors matches it to **1.2 × 10⁻¹⁴**, which is rounding. Multiplying by γ gives **0.99769**. |
| E6 | §1.9.2, last paragraph | "against the 200 % deficit of the idealised model" | **0.62 %** deficit |
| E7 | Figure 1.1 | The caption says the path "bends towards the positive plate". By the text's own convention (y towards the upper plate, upper plate positive) that is upwards. The drawn path bends **down**, because it is the solver's −y path drawn without a sign change. The plates carry no polarity mark. | Flip the drawn path, or mark the lower plate as positive. |
| E8 | Example 1.2 | "A deflection goes as 1/v², so a calculation that uses ½mv² is off by 8.9 % for the column electron and by 0.59 % for the electron of the 2 kV tube." The text's own (relativistic) result is tan θ = eEl/(γmv²), not eEl/(mv²). The factor γ largely cancels the speed error: γmv² = eV(2+ε)/(1+ε), whereas a ½mv² calculation gives 2eV. | A fully non-relativistic deflection is **too small by 2.8 %** at 30 kV and **by 0.19 %** at 2 kV. The factor is (1+ε/2)/(1+ε). The page's own solver, run in Chromium, gives −2.77 % and −0.195 %. The 0.59 % also contradicts Example 1.1, where the gap is 0.39 % (relativistic v, no γ) or −0.19 % (v_NR). |
| E9 | §1.8.3, "RK4 energy, predicted" column | The prediction sin²χ(1−(\|R\|²)^{20N}) is the relative loss of **u²** (momentum squared), not of the kinetic energy K = (γ−1)mc² that the "RK4 energy" column measures. To first order ΔK/K = (γ+1)/(2γ)·Δ(u²)/u², a factor 0.998 at 2 kV. | Predicted ΔK/K = **0.0137, 4.39 × 10⁻⁴, 1.38 × 10⁻⁵, 4.31 × 10⁻⁷, 1.35 × 10⁻⁸, 4.21 × 10⁻¹⁰** for N = 16 … 512. These agree with the measured column to 2 × 10⁻⁴ relative. The printed 0.0138, 4.40 × 10⁻⁴, 4.32 × 10⁻⁷ and 4.22 × 10⁻¹⁰ are wrong in the last digit. |
| E10 | eq. (1.21), the sentence before it | "One RK4 step multiplies w by … R(iθ) = 1 + iθ − θ²/2 − iθ³/6 + θ⁴/24 … The true factor e^{−iθ}". For ẇ = −iΩw the step factor is R(−iθ) = 1 − iθ − θ²/2 + iθ³/6 + θ⁴/24, the conjugate of what is printed. The printed polynomial approximates e^{+iθ}, not the e^{−iθ} named next to it. | Write R(−iθ) and compare it with e^{−iθ} (phase lag arg R + θ = −(θ⁵/120 − θ⁷/336)). Alternatively, keep R(iθ) and compare it with e^{iθ}. \|R\|² and the size of the phase error in (1.21) are unchanged. |
| E11 | §1.9.2 | "Why the second method is low by a factor of two is not stated in the paper text that we read." Thomson does name a bias, in the paragraph right after his second table: "no allowance has been made for the magnetic force due to the coil in the region outside the plates … the effective value of H will be smaller than the value used … so that the values of m/e are larger … than they would be if this correction were applied". That is the direction of the deficit in e/m. | Quote Thomson's own correction, the reversed coil field outside the plates. He does not size it. |
| E12 | §1.6, text after (1.14) | The reference renders as the literal italic text "eq:loop": "the sum of two terms *eq:loop* vanish there". The cause is that `‹eq:loop›` sits inside `\( \)` in `text/ch01.py`. | "(1.13)" |
| E13 | Chapter 0 simulation caption | "the smallest half-pitch light can resolve". The readout is d_opt = λ/(2NA), which (0.1), Figure 0.1 and `contract.json` all call the smallest **period (pitch)**. | "the smallest period (pitch) light can resolve" |

Minor points (wording or presentation, no wrong result):

- **m1.** Simulation readout labels are set in small capitals, so λ prints as **Λ**, d_opt as D_OPT, w as W, r_g as R_G and x_end as X_END. Screenshot of the chapter 0 readouts: "Λ 38.8 pm", "Λ/W 0.00388". Capital Λ is a different symbol.
- **m2.** Figure 1.4 says "Boris: rounding noise, about 1e-16". The Boris |ΔK/K| values are 2 to 6 × 10⁻¹⁵ in the page module and 0 to 4 × 10⁻¹⁵ in `ref/ch01.py`, which draws the figure. At N = 64 the reference gives exactly 0, which is drawn at the 1e-18 floor.
- **m3.** Example 1.1, "The computed spot with that field on is at y_s = −1.58 × 10⁻⁸ µm". That is y at the plate exit (`y_end`). The spot on the screen, y_end + tan θ_end·L, is −1.4 × 10⁻⁷ µm. Both are zero to rounding.
- **m4.** §1.8.3 says the "predicted" columns are the accumulated phase errors 20N(θ − 2 arctan θ/2) and 20N(θ − arg R). The code prints the chord 2 sin(δ/2) of that phase, which is a distance in units of r_L, not the phase.
  - With the radius factor of (1.24) included, the Boris prediction 2 sin(δ/2)·√(1+(π/N)²) equals the measured error to 10⁻¹¹ relative for every N. The quoted "0.12 %" at N = 64 is exactly √(1+(π/64)²) − 1.
- **m5.** "for RK4 the prediction is within a few per cent". The gaps are 9.6 %, 6.8 %, 4.1 %, 2.6 %, 1.7 % and 1.3 % (N = 16 … 512), so "within 10 %" is accurate.
- **m6.** Example 1.2, "The speed error reaches 1 % at V = 6900 V". The sentence before it defines the error as v_NR/v − 1, which reaches 1 % at **6830 V**. 6900 V (6901 V) is where v/v_NR = 0.99, the criterion of Problem 2.
- **m7.** §1.8.1, "the electron has lost half its energy after 867 turns". The 867 is when u⊥² halves. That equals half the kinetic energy only for motion at a right angle to B and v ≪ c.
- **m8.** The N column of the §1.8.3 table prints "16.0", "32.0", "64.0" (3 significant figures applied to an integer).
- **m9.** Ω is signed (negative for the electron) in (1.15), but Figure 1.3's L = 2πv∥/Ω and the θ = Ωh of (1.21) treat it as positive. Should be |Ω|.
- **m10.** §1.10 calls `ref/ch01.py` "an independent NumPy implementation". It is a line-by-line mirror of the same algorithm and convention, so it could not catch E1.
- **m11.** §1.10.1 says the product of the two factors "matches the measured ratio". With the run stopped at t = l/v₀ (not at x = l), p_y = eEl/v₀ exactly. So θ_sim = arctan(eEl/(γmv₀²)) holds identically in the solver, and the match is an identity, not a test.
- **m12.** §1.6, "uniform over a region that is long compared with the offset" is unclear. What is meant: the first three derivatives vanish, so the deviation is of fourth order in z/R; SymPy gives d⁴B/dz⁴ ≠ 0.
- **m13.** `derive/ch01.py` D12a checks (2π/Ω)·v∥ = 2πv∥/Ω, an identity of notation, not a derivation.

---

## A. Equations

Verdicts follow re-derivation in SymPy (script `mysym.py` in the session scratchpad), a check of units, and the limits listed.

| eq. | statement (short) | derivation | units | limiting cases | verdict |
|---|---|---|---|---|---|
| grating step, §0.2 | p(sin θ_m − sin θ_i) = mλ/n; with θ_i = α and m = −1, the order enters while sin α − λ/(np) ≥ −sin α | solved for p: p ≥ λ/(2n sin α) | — | — | verified |
| (0.1) | p_min = λ/(2NA) | follows from the step above with NA = n sin α | m | NA → n gives λ/(2n) (immersion ceiling) | verified |
| (0.2) | λ = h/√(2meV(1 + eV/2mc²)) | from (pc)² = T(T+2mc²), T = eV. Also checked (γmv c)² = T(T+2mc²) with T = (γ−1)mc². | m | ε → 0 gives h/√(2meV); ε ≫ 1 gives hc/eV | verified. "as chapter 1 derives in §1.5": §1.5 gives (pc)² = T(T+2mc²) via D2b and states (1.12); acceptable. `physics/ch00.js` says chapter 3 derives it, a small inconsistency of cross-reference. |
| (1.1) | y = eEx²/(2mv₀²), tan θ = eEl/(mv₀²) | y = ½a(x/v₀)², dy/dx at x = l | m; dimensionless | non-relativistic by construction; valid for γ → 1 | verified |
| D5a statement, §1.3.1 | tangent at x = l meets the axis at l/2 | l − y(l)/y′(l) = l/2 | — | — | verified |
| (1.2) | y_s = (l/2 + L) tan θ, L = x_s − x_p − l | y(l) + L tan θ = (l/2 + L) tan θ, since y(l) = (l/2) tan θ | m | L = 0 gives y(l) | verified |
| (1.3) | r_L = mv/(eB), Ω = eB/m, f = Ω/2π | mv²/r = evB | m, s⁻¹ | non-relativistic case of (1.17) | verified |
| sin φ = l/r_L, φ ≈ eBl/(mv₀), §1.3.2 | entry at right angles to the radius | — | — | l ≪ r_L | verified |
| (1.4) | θ = (e/m)El/v₀² = (e/m)B²l/E ⇒ e/m = θE/(B²l) | v₀ = E/B substituted, solved for e/m | C/kg | small angle (tan θ ≈ θ), non-relativistic | verified. Thomson's m/e = H²l/(Fθ) checked against the transcription. |
| (1.5) | L₀ = −mc²/γ = −mc²√(1 − v²/c²) | series −mc² + ½mv² + mv⁴/(8c²) | J | v ≪ c gives ½mv² + const | verified |
| ∂L₀/∂v_i, unnumbered §1.4.1 | = γmv_i | SymPy derivative | kg m/s | — | verified |
| (1.6) | L = −mc²/γ − qφ + q v·A | −q∫A_μdx^μ with A^μ = (φ/c, A), metric (+,−,−,−), gives (−qφ + qA·v)dt | J | A = 0, φ = 0 gives (1.5) | verified |
| (1.7) | p = γmv + qA | ∂L/∂v for all three components | kg m/s | A = 0 gives γmv | verified |
| EL x-component, unnumbered §1.4.3 | d(γmv_x)/dt = −q∂_xφ − q∂_tA_x + q[v_y(∂_xA_y − ∂_yA_x) + v_z(∂_xA_z − ∂_zA_x)] | identical to ∂L/∂x − q dA_x/dt with the convective derivative | N | — | verified; B_z and B_y components as stated, also verified |
| (1.8) | d(γmv)/dt = q(E + v × B) | Euler–Lagrange in all three components with E = −∇φ − ∂_tA and B = ∇ × A | N | v ≪ c gives Newton plus Lorentz | verified |
| H, unnumbered §1.5.1 | H = γmv² + mc²/γ + qφ = γmc² + qφ | p·v − L | J | v = 0 gives mc² + qφ | verified |
| (1.9) | H = √(m²c⁴ + c²\|p − qA\|²) + qφ | squares agree identically and both sides are positive for v < c | J | A = φ = 0 gives E² = m²c⁴ + p²c² | verified |
| dH/dt = ∂H/∂t, §1.5.2 | Hamilton's equations | — | — | static fields: H conserved | verified |
| (1.10) | (γ−1)mc² − eφ = const ⇒ γ = 1 + eV/mc², v = c√(1 − 1/γ²) | from H = γmc² + qφ with q = −e, φ = 0 at the cathode | — | V → 0 gives γ → 1 and ½mv² = eV | verified |
| d(γmc²)/dt = v·d(γmv)/dt = qE·v, §1.5.2 | D3a, D3b | own derivation from E² = p²c² + m²c⁴ | W | — | verified |
| (γ−1)mc² series, §1.5.3 | = ½mv² + (3/8)mv⁴/c² + … | series | J | — | verified |
| (1.11) | v/v_NR = 1 − ¾ε + (23/32)ε² − … | exact closed form v/v_NR = √(1+ε/2)/(1+ε), then series | — | ε → 0 gives 1; ε → ∞ gives 1/√(2ε) | verified |
| (1.12) | λ = h/√(2meV(1+eV/2mc²)) = λ_NR(1 − ε/4 + …) | series of (1+ε/2)^(−1/2) = 1 − ε/4 + 3ε²/32 | m | as (0.2) | verified |
| (1.13) | B(z) = μ₀NIR²/(2(R²+z²)^{3/2}) | Biot–Savart integral of μ₀I dℓ/(4πr²)·(R/r) round the loop | T | z = 0 gives μ₀NI/(2R); z ≫ R gives the dipole μ₀NIR²/(2z³) | verified |
| inline, §1.6 | 2μ₀NIR²/[2(5R²/4)^{3/2}] = (4/5)^{3/2}μ₀NI/R | algebra | T | — | verified |
| (1.14) | B = (4/5)^{3/2}μ₀NI/R; dB/dz = d²B/dz² = 0 at the midpoint | sum of two (1.13) at ±R/2, derivatives | T | d³B/dz³ = 0 by symmetry; d⁴B/dz⁴ = −27648√5 μ₀NI/(3125R⁵) ≠ 0 | verified (wording m12) |
| B = μ₀nI, §1.6 | long solenoid, Ampère | standard | T | — | verified |
| (1.15) | du/dt = Ω u × b̂, Ω = qB/(γm) | from (1.8) with γ constant | s⁻¹ | — | verified (sign usage m9) |
| ẇ = −iΩw, §1.7 | w = u_x + iu_y | du_x/dt = Ωu_y, du_y/dt = −Ωu_x | — | — | verified |
| (1.16) | u⊥(t) and r(t) of the helix | du/dt = Ω u × ẑ, dr/dt = u/γ, r(0) = 0, all checked | m/s, m | Ω → 0 gives a straight line r = ut/γ | verified |
| r_L = \|u⊥0\|/(γ\|Ω\|), §1.7 | circle about the centre (u⊥0 × b̂)/(γΩ) | (x − x_c)² + (y − y_c)² checked | m | — | verified |
| (1.17) | r_L = γmv⊥/(eB) = p⊥/(eB), T = 2πγm/(eB), pitch = v∥T | from \|u⊥\| = γv⊥ and \|Ω\| = eB/(γm) | m, s | γ → 1 gives (1.3) | verified |
| (1.18) | L = v∥T = 2πγmv∥/(eB) | from (1.17) | m | spread in v∥ is second order in α | verified |
| (1.19) | ṙ = u/γ, u̇ = (q/m)(E + (u/γ) × B), γ = √(1 + u²/c²) | (1.8) with u = γv; γ(u) identical to (1 − v²/c²)^(−1/2) | — | — | verified |
| (1.20) | classical RK4 | standard (Hairer, Nørsett and Wanner §II.1) | — | — | verified |
| (1.21) | \|R\|² = 1 − θ⁶/72 + θ⁸/576; θ − arg R = θ⁵/120 − θ⁷/336 + … | \|R(±iθ)\|² expanded; arg R(iθ) series | — | θ → 0 gives 1 | equation verified. The sentence before it is **wrong, because** of the sign of the step factor (E10). |
| (1.22) | Boris u⁻, u′, u⁺, u_{n+1/2} with a = qh/(2m), t = aB/γ⁻, s = 2t/(1+t²) | planar form: u⁻ × t = (u_y t, −u_x t) and u⁺ as printed both verified; 1 − st = (1−t²)/(1+t²) = cos φ, s = sin φ; \|u⁺\| = \|u⁻\| for t in any direction | — | — | verified |
| Problem 3 hint | \|u′\|² = \|u⁻\|²(1+t²) for u⁻ ⊥ t | algebra | — | — | verified |
| (1.23) | Ωh − 2 arctan(Ωh/2) = (Ωh)³/12 − (Ωh)⁵/80 + … | series; next term +(Ωh)⁷/448 | — | h → 0 gives 0 | verified |
| (1.24) | r_Boris = r_L√(1 + (Ωh/2)²) | chord Ωh·r_L, turning angle 2 arctan(Ωh/2), circumradius chord/(2 sin(φ/2)) | m | h → 0 gives r_L. Confirmed numerically: measured Boris error = 2 sin(δ/2)·√(1+(π/N)²) to 10⁻¹¹. | verified |
| Larmor, §1.2 | P = e²a²/(6πε₀c³) | standard SI form (Jackson ch. 14) | W | non-relativistic form; β = 0.088 here | verified |
| relativistic tan θ = eEl/(γmv²), Example 1.1 | p_y = eEt, p_x = γmv constant | exact for a run of fixed duration t = l/v₀. With a stop at x = l, t is longer by 9 × 10⁻⁶ relative (exact closed-form motion), a 0.00085 % effect on y_s. | — | — | verified |

## B. Numbers, chapter 0

Columns: "page" is the rendered string; "Chromium" is the page's own code run in headless Chromium; "independent" is my own mpmath computation.

| number | page | Chromium | independent | verdict |
|---|---|---|---|---|
| pitch 2025 | 20 nm | 20 | IRDS 2022 Table MM-7 (p. 7): 2025 = G45M20, M0 pitch 20 nm | verified |
| line width (half-pitch) | 10 nm | 10 | 20/2 | verified |
| Si lattice constant | 0.543 nm | 0.543 | 5.431020511 × 10⁻¹⁰ m (CODATA 2018) | verified |
| Si nearest neighbour a√3/4 | 0.235 nm | 0.235 | 0.2351701 nm | verified |
| atoms across 10 nm | 43 | 43 | 42.52 | verified ("about") |
| hydrogen atom "a tenth of a nanometre" | — | — | Bohr diameter 0.106 nm | verified |
| λ ArF | 193 nm | 193 | given | verified |
| NA ArF | 1.35 | 1.35 | assumption of the figure, below n_water(193 nm) ≈ 1.44 | verified |
| p_min ArF | 71.5 nm | 71.5 | 71.481 nm | verified |
| ratio to pitch | 3.6 | 3.6 | 3.574 | verified |
| λ EUV | 13.5 nm | 13.5 | IRDS Lithography: "13.5nm wavelength" | verified |
| NA 0.33 / 0.55 | 0.33 / 0.55 | 0.33 / 0.55 | IRDS Lithography, read | verified |
| p_min EUV 0.33 | 20.5 nm | 20.5 | 20.4545 nm | verified |
| p_min EUV 0.55 | 12.3 nm | 12.3 | 12.2727 nm | verified |
| quoted "12 nm" half-pitch "optically resolvable by 0.33 NA optics" | 12 nm | — | IRDS 2022 Lithography §3, word for word | verified |
| half-pitch by (0.1) | 10.2 nm | 10.2 | 10.227 nm, below 12 nm, so consistent | verified |
| Abbe citation 9, 413, 1873 | — | — | Arch. mikrosk. Anat. 9, 413–468 (1873) | verified |
| h | 6.62607015 × 10⁻³⁴ J s | — | CODATA 2018, exact | verified |
| λ at 1 kV | 38.8 pm | 38.8 | 38.76403 pm | verified |
| λ at 30 kV | 6.98 pm | 6.98 | 6.979082 pm | verified |
| λ(1 kV)/a_Si | 0.071 | 0.071 | 0.071375 | verified |
| pitch/λ(30 kV) | 2866 | 2866 | 2865.71 | verified |
| proton/electron mass | 1836 | — | 1836.15267343 | verified |
| 1 pm = 10⁻³ nm | — | — | unit | verified |
| Figure 0.1 labels | 71.5 nm, 20.5 nm, 12.3 nm, 20 nm, 543 pm, 38.8 pm, 6.98 pm | `ref/ch00.py` | as above | verified |
| AMAT "100 million", "95%", "1,500°C", "10X", "1×10 – 11" mbar, "two to three orders of magnitude" | — | — | — | unverifiable, because the Applied Materials pages return 403 "Access Denied" to automated fetches and the Wayback Machine connection was reset. Not tried further: a spoofed user agent was refused as bot-check circumvention. |
| 10⁻¹¹ mbar = 10⁻⁹ Pa | — | — | 1 mbar = 100 Pa | verified |
| Chapter 0 simulation readouts (defaults V = 1 kV, λ = 193 nm, NA = 0.95, w = 10 nm) | 38.8 pm; 102 nm; 10.2; 0.00388 | same | 38.76 pm; 101.58 nm; 10.16; 0.003876 | numbers verified; caption **wrong** (E13); labels m1 |

## C. Numbers, chapter 1 prose

| place | number | page | Chromium | independent | verdict |
|---|---|---|---|---|---|
| Fig. 1.1 | vertical stretch | 1.3 | 1.3 | 2.6 px/mm across ÷ 2 px/mm along, from `svg_tube` | verified |
| Fig. 1.1 | V_p | 100 V | 100 | given | verified (bend direction: E7) |
| §1.1, §1.2 | Thomson's plates 5 cm × 2 cm, 1.5 cm apart; scale pasted on the tube | — | — | Thomson (1897), transcription, word for word | verified |
| §1.2 | e, m | 1.602176634 × 10⁻¹⁹ C; 9.10938370 × 10⁻³¹ kg | — | CODATA 2018 (m = 9.1093837015 × 10⁻³¹, rounded to 9 figures) | verified |
| §1.2 | d/l | 0.3 | 0.3 | 15/50 | verified |
| §1.2 | V_a | 2000 V | 2000 | given | verified |
| §1.2 | ε at 2 kV | 0.00391 | 0.00391 | 0.0039139 | verified |
| §1.2 | v/c at 2 kV | 0.08822 | 0.08822 | 0.0882161 | verified |
| §1.2 | ε at 30 kV | 0.0587 | 0.0587 | 0.0587085 | verified |
| §1.2 | v/c at 30 kV | 0.328 | 0.328 | 0.328376 | verified |
| §1.2 | a = eE/m | 1.17 × 10¹⁵ m/s² | same | 1.1725467 × 10¹⁵ | verified |
| §1.2 | Larmor P | 7.85 × 10⁻²⁴ W | same | 7.84818 × 10⁻²⁴ W | verified |
| §1.2 | t in plates | 1.89 × 10⁻⁹ s | same | 1.890607 × 10⁻⁹ s | verified |
| §1.2 | radiated fraction | 4.6 × 10⁻¹⁷ | same | 4.6305 × 10⁻¹⁷ | verified |
| §1.2 | λ at 2 kV | 2.74 × 10⁻¹¹ m | same | 2.739692 × 10⁻¹¹ m | verified |
| §1.2 | λ/d | 1.8 × 10⁻⁹ | same | 1.82646 × 10⁻⁹ | verified |
| §1.2 | r_L in balancing field | 0.599 m | 0.599 | 0.598830 m | verified |
| §1.2 | r_L/l | 12.0 | 12.0 | 11.9766 | verified |
| §1.2 | "a few millimetres" at 4 mT | — | — | 2.26 mm at α = 60 mrad | verified |
| Ex. 1.1 | v₀ non-relativistic | 2.652 × 10⁷ m/s | same | 2.6524102 × 10⁷ | verified |
| Ex. 1.1 | v₀ relativistic | 2.645 × 10⁷ m/s | same | 2.6446534 × 10⁷ | verified |
| Ex. 1.1 | E | 6667 V/m | same | 6666.67 | verified |
| Ex. 1.1 | a | 1.173 × 10¹⁵ m/s² | same | 1.172547 × 10¹⁵ | verified |
| Ex. 1.1 | t | 1.891 × 10⁻⁹ s | same | 1.890607 × 10⁻⁹ | verified |
| Ex. 1.1 | v_y at exit | 2.217 × 10⁶ m/s | same | 2.216825 × 10⁶ | verified |
| Ex. 1.1 | ½at² | 0.002096 m | same | 0.00209557 | verified |
| Ex. 1.1 | tan θ by (1.1) with relativistic v₀ | 0.08382 | same | 0.0838229 | verified |
| Ex. 1.1 | L = 0.19 m | 0.19 | — | 0.30 − 0.06 − 0.05 | verified |
| Ex. 1.1 | y_s by (1.2) | 0.01802 m | same | 0.0180219 | verified |
| Ex. 1.1 | y_s from the solver | **−0.01795 m** | −0.01795 (y_end + tan θ_end·L, solver sign) | +0.0179516 (exact motion stopped at t = l/v₀); +0.0179518 (exact, stopped at x = l) | **wrong, because** the solver's −y is used as the text's +y (E1). Correct: **0.01795 m**. |
| Ex. 1.1 | gap | **−200 %** | −200 | +0.3916 % | **wrong, because** of E1. Correct: **0.39 %**. |
| Ex. 1.1 | γ at 2 kV | 1.00391 | same | 1.0039139 | verified |
| Ex. 1.1 | tan θ with γ | 0.08350 | same | 0.0834961 (= tan of the exact solver angle) | verified |
| Ex. 1.1 | y_s with γ | 0.01795 m | same | 0.0179517 | verified |
| Ex. 1.1 | agreement with the solver | **200.0 %** | 200.0 | 1.577 × 10⁻⁴ % | **wrong, because** of E1. Correct: **1.577 × 10⁻⁴ %**. |
| Ex. 1.1 | B = E/v₀ | 2.521 × 10⁻⁴ T | same | 2.520809 × 10⁻⁴ | verified |
| Ex. 1.1 | spot with both fields | −1.58 × 10⁻⁸ µm | same (`y_end` at the plate exit) | screen spot −1.36 × 10⁻⁷ µm | verified as "zero"; label m3 |
| Fig. 1.2 | B_p | 2.521 × 10⁻⁴ T | same | as above | verified |
| Fig. 1.2 | axis 50–300 mm, plates 60–110 mm, 5 mm bar | — | — | XP = 0.06, l = 0.05, `_panel` scale | verified |
| §1.4 | "a third of the speed of light" at 30 kV | — | — | 0.328 | verified |
| Ex. 1.2 | γ at 30 kV | 1.0587 | same | 1.0587085 | verified |
| Ex. 1.2 | v | 9.844 × 10⁷ m/s | same | 9.844470 × 10⁷ | verified |
| Ex. 1.2 | v/c | 0.328 | same | 0.328376 | verified |
| Ex. 1.2 | v_NR | 1.027 × 10⁸ m/s | same | 1.0272741 × 10⁸ | verified |
| Ex. 1.2 | v_NR too large by | 4.4 % | same | 4.3504 % | verified |
| Ex. 1.2 | λ | 6.98 pm | same | 6.97908 | verified |
| Ex. 1.2 | V where the speed error is 1 % | 6900 V | 6901 | 6901 V for v/v_NR = 0.99; 6832 V for v_NR/v = 1.01 | verified for the criterion of Problem 2; see m6 |
| Ex. 1.2 | deflection error, 30 kV | **8.9 %** | 8.89 ((v_NR/v)² − 1) | −2.773 % (closed form (1+ε/2)/(1+ε) − 1, and the page's own solver in Chromium: −2.7726 %) | **wrong, because** a ½mv² calculation also drops γ (E8). Correct: **−2.8 %** (too small). |
| Ex. 1.2 | deflection error, 2 kV | **0.59 %** | 0.587 | −0.1949 % (closed form and page solver) | **wrong, because** of E8. Correct: **−0.19 %**. |
| §1.6 | Helmholtz example, N = 100, R = 50 mm, I = 1 A | 0.00180 T | same | 1.798353 × 10⁻³ T | verified |
| §1.6 | Thomson calibrated with a small coil and a ballistic galvanometer | — | — | transcription: galvanometer "kick" method; mean H over l = 60 ι | verified |
| §1.7 | focus L at 2 kV, 4 mT | 0.2367 m | same | 0.2366909 m | verified |
| §1.7 | r_L at α = 60 mrad | 0.00226 m | same | 2.262948 × 10⁻³ | verified |
| Fig. 1.3 | six copies at 60° | — | `svg_helix` | symmetry about B | verified |
| §1.8.1 | RK4 loss per turn, N = 16 | 0.080 % | same | 0.079897 % | verified |
| §1.8.1 | turns to half, N = 16 | 867 | same | 867.20 | verified as u⊥² halving (m7) |
| §1.8.1 | turns to 1 % loss, N = 64 | 12600 | same | 12643 | verified |
| §1.8.2 | Boris radius factor, N = 16 | 1.0191 | same | 1.0190943 | verified |
| §1.8.2 | Boris radius factor, N = 64 | 1.0012 | same | 1.0012041 | verified |
| §1.8.2 | Qin et al., PoP 20, 084503 (2013) | — | — | "Why is Boris algorithm so good?", Phys. Plasmas 20, 084503 (2013) | verified |
| §1.8.3 | r_L test (2 kV, 10 mT, χ = 1.2) | 0.01407 m | same | 0.01406948 | verified |
| §1.8.3 | T test | 3.586 × 10⁻⁹ s | same | 3.586369 × 10⁻⁹ | verified |
| §1.8.3 | Boris position slope | −2.00 | −1.9995 | expected −2 | verified |
| §1.8.3 | RK4 position slope | −3.98 | −3.9808 | expected −4 | verified |
| §1.8.3 | RK4 energy slope | −5.00 | −4.9992 | expected −5 | verified |
| §1.8.3 | Boris prediction gap at N = 64 | 0.12 % | 0.1203 | = √(1+(π/64)²) − 1 = 0.1204 % exactly | verified (see m4) |
| §1.8.3 | RK4 prediction "within a few per cent" | — | — | 9.6, 6.8, 4.1, 2.6, 1.7, 1.3 % | wrong in wording at N ≤ 32 (m5) |
| §1.8.3 | "energy of Boris stays at the noise of 64-bit arithmetic" | noise | 2–6 × 10⁻¹⁵ | — | verified |
| Fig. 1.4 | "about 1e-16" | — | `ref`: 0 to 4 × 10⁻¹⁵ | — | **wrong, because** the values are of order 10⁻¹⁵ (m2) |
| Key result | RK4 error, N = 64 | 9.31 × 10⁻⁵ | same | consistent with the analytic phase estimate 9.69 × 10⁻⁵ to 4 % | verified |
| Key result | Boris error, N = 64 | 0.101 | 0.10086 | 2 sin(δ/2)·√(1+(π/64)²) = 0.1008649 | verified |
| Ex. 1.3 | RK4 field evaluations, N = 16 | 64 | 64 | 4 × 16 | verified |
| Ex. 1.3 | RK4 error, N = 16 | 0.0215 | 0.02149 | analytic phase estimate 0.0235 | verified |
| Ex. 1.3 | Boris error, N = 64 | 0.101 | as above | as above | verified |
| Ex. 1.3 | RK4 energy loss, N = 16 | 1.37 % | 1.3748 | 1.37499 % (u² loss with the relativistic factor) | verified |
| §1.9 | "a tenth of a period … visible within a few turns" | — | — | N = 10: \|R\|² = 1 − 8.1 × 10⁻⁴ per step, 0.81 % per turn | verified |
| §1.9.1 | B | 2.521 × 10⁻⁴ T | same | as Ex. 1.1 | verified |
| §1.9.1 | e/m inferred | **−1.7479 × 10¹¹ C/kg** | −1.7479 × 10¹¹ | +1.747909 × 10¹¹ | **wrong, because** of E1. Correct: **1.7479 × 10¹¹ C/kg**. |
| §1.9.1 | θ of the simulated path | **−0.08330 rad** | −0.08330 | +0.0833029 (exact closed form at t = l/v₀) | **wrong, because** of E1. Correct: **0.08330 rad**. |
| §1.9.1 | e/m used | 1.7588 × 10¹¹ C/kg | same | 1.75882001 × 10¹¹ | verified |
| §1.9.1 | "returns it to" | **200 %** | 199.4 | 0.6204 % | **wrong, because** of E1. Correct: **0.62 %**. |
| §1.9.1 | γ | 1.00391 | same | 1.0039139 | verified |
| §1.9.1 | 1/γ | 0.99610 | same | 0.9961014 | verified |
| §1.9.1 | y = tan θ | 0.08350 | same | 0.0834961 | verified |
| §1.9.1 | arctan y / y | 0.99769 | same | 0.9976858 | verified |
| §1.9.1 | product | 0.99380 | same | 0.9937962 | verified |
| §1.9.1 | measured ratio | **−0.99380** | −0.99380 | +0.9937962 | **wrong, because** of E1. Correct: **0.99380**. |
| §1.9.1 | match "to" | **2.0** | 1.988 | 1.2 × 10⁻¹⁴ | **wrong, because** of E1. Correct: **1.2 × 10⁻¹⁴** (identity, m11). |
| §1.9.1 | ratio × γ | **−0.99769** | −0.99769 | +0.9976858 | **wrong, because** of E1. Correct: **0.99769**. |
| §1.9.2 | Phil. Mag. 44, 293 | — | — | 44, 293–316 (1897) | verified |
| §1.9.2 | rows typed in | 26 and 7 | 26, 7 | transcription: 12 + 11 + 3 rows; 7 rows | verified |
| §1.9.2 | m/e = I²Q/2W, I = Hρ | — | — | transcription | verified |
| §1.9.2 | 1 g/abC = 10⁻⁴ kg/C | — | — | 1 abC = 10 C | verified |
| §1.9.2 | method 1, minimum ratio | 0.57 | 0.5686 | m/e = 1.0 × 10⁻⁷ gives 0.56856 | verified |
| §1.9.2 | method 1, maximum ratio | 1.78 | 1.7768 | m/e = 0.32 × 10⁻⁷ | verified |
| §1.9.2 | method 1, mean | 1.19 | 1.1897 | from the 26 printed m/e | verified |
| §1.9.2 | tubes 1 and 2 | 1.26 | 1.2573 | — | verified |
| §1.9.2 | tube 3 | 0.67 | 0.6708 | — | verified |
| §1.9.2 | method 2 range | 0.38 to 0.52 | 0.379, 0.517 | m/e = 1.5 and 1.1 × 10⁻⁷ | verified |
| §1.9.2 | method 2 mean | 0.45 | 0.4486 | — | verified |
| §1.9.2 | Thomson: tubes 1, 2 too large in e/m (leakage); ρ uncertain by about 20 per cent | — | — | transcription: "values of m/e … from Tubes 1 and 2 are too small, in consequence of the leakage"; "about 20 per cent" | verified |
| §1.9.2 | "not stated in the paper text" | — | — | Thomson names the reversed coil field outside the plates as a bias making m/e too large | **wrong, because** of E11 |
| §1.9.2 | 10⁻⁷ against 10⁻⁴ for the hydrogen ion; Lenard | — | — | transcription | verified |
| §1.9.2 | spread of method 1 | 3.1 | 3.125 | 1.7768/0.5686 | verified |
| §1.9.2 | idealised model deficit | **200 %** | 199.4 | 0.62 % | **wrong, because** of E1. Correct: **0.62 %**. |
| §1.9.2 | median deviation | 1.4 % | 1.407 | recomputed from the JSON rows, which match the transcription | verified |
| §1.9.2 | largest deviation of the good rows | 8.1 % | 8.063 | — | verified |
| §1.9.2 | factor of the bad row | 9.99 | 9.994 | 205²/(2 × 6 × 10¹²) = 3.50 × 10⁻⁹ against 0.35 × 10⁻⁷ | verified |
| §1.9.2 | W/Q = 6 × 10¹¹ fits m/e and v | — | — | m/e = 3.50 × 10⁻⁸; v = 2W/(QI) = 5.85 × 10⁹ ≈ 6 × 10⁹ | verified |
| §1.10 | 23 SymPy checks PASS | — | `derive/ch01.py` run: all pass | own re-derivation (section A) | verified (D12a is trivial, m13) |
| §1.11 | radiated fraction | 4.6 × 10⁻¹⁷ | same | as §1.2 | verified |
| Problem 2 | exact voltage | 6900 V | 6901 | 6901.47 V; the approximation 1 − ¾ε = 0.99 gives 6813 V | verified |
| Problem 4 | r_L at 30 kV, 1 mT | 0.593 m | same | 0.5925805 | verified |
| Problem 4 | N_min for 0.1 % | 70.2 | 70.23 | π/√(1.001² − 1) = 70.2306, so 71 steps | verified |
| Sources | Tiesinga et al., RMP 93, 025010 (2021) | — | — | CODATA 2018 paper | verified |
| Ch. 1 simulation defaults (E = 10 kV/m, B = 1 mT, v₀ = 10 Mm/s, θ₀ = 60°) | r_g 49.3 mm, Ω_c 1.76 × 10⁸ rad/s | same | 49.24 mm; 1.7588 × 10⁸ | verified (labels m1; slider wording E1) |

## D. The table of §1.5, cell by cell

The V column (0.100 … 100 kV) holds givens.

| cell | page | Chromium | independent | verdict |
|---|---|---|---|---|
| V = 0.1 kV, ε | 1.96 × 10⁻⁴ | 1.96 × 10⁻⁴ | 0.00019569512 | verified |
| V = 0.1 kV, v/c | 0.01978 | 0.01978 | 0.019780682 | verified |
| V = 0.1 kV, v/v_NR | 0.9999 | 0.9999 | 0.99985326 | verified |
| V = 0.1 kV, λ (pm) | 122.6 | 122.6 | 122.6366 | verified |
| V = 0.1 kV, λ/λ_NR | 1.000 | 1.000 | 0.99995108 | verified |
| V = 0.5 kV, ε | 9.78 × 10⁻⁴ | 9.78 × 10⁻⁴ | 0.00097847559 | verified |
| V = 0.5 kV, v/c | 0.04421 | 0.04421 | 0.044205007 | verified |
| V = 0.5 kV, v/v_NR | 0.9993 | 0.9993 | 0.99926683 | verified |
| V = 0.5 kV, λ (pm) | 54.83 | 54.83 | 54.834025 | verified |
| V = 0.5 kV, λ/λ_NR | 0.9998 | 0.9998 | 0.99975547 | verified |
| V = 1 kV, ε | 0.00196 | 0.00196 | 0.0019569512 | verified |
| V = 1 kV, v/c | 0.06247 | 0.06247 | 0.062469539 | verified |
| V = 1 kV, v/v_NR | 0.9985 | 0.9985 | 0.99853503 | verified |
| V = 1 kV, λ (pm) | 38.76 | 38.76 | 38.764034 | verified |
| V = 1 kV, λ/λ_NR | 0.9995 | 0.9995 | 0.99951112 | verified |
| V = 2 kV, ε | 0.00391 | 0.00391 | 0.0039139024 | verified |
| V = 2 kV, v/c | 0.08822 | 0.08822 | 0.088216141 | verified |
| V = 2 kV, v/v_NR | 0.9971 | 0.9971 | 0.99707554 | verified |
| V = 2 kV, λ (pm) | 27.40 | 27.40 | 27.396924 | verified |
| V = 2 kV, λ/λ_NR | 0.9990 | 0.9990 | 0.99902296 | verified |
| V = 10 kV, ε | 0.0196 | 0.0196 | 0.019569512 | verified |
| V = 10 kV, v/c | 0.1950 | 0.1950 | 0.19498561 | verified |
| V = 10 kV, v/v_NR | 0.9856 | 0.9856 | 0.9855929 | verified |
| V = 10 kV, λ (pm) | 12.20 | 12.20 | 12.204695 | verified |
| V = 10 kV, λ/λ_NR | 0.9951 | 0.9951 | 0.99514323 | verified |
| V = 30 kV, ε | 0.0587 | 0.0587 | 0.058708536 | verified |
| V = 30 kV, v/c | 0.3284 | 0.3284 | 0.32837618 | verified |
| V = 30 kV, v/v_NR | 0.9583 | 0.9583 | 0.95831 | verified |
| V = 30 kV, λ (pm) | 6.979 | 6.979 | 6.9790816 | verified |
| V = 30 kV, λ/λ_NR | 0.9856 | 0.9856 | 0.98563829 | verified |
| V = 100 kV, ε | 0.196 | 0.196 | 0.19569512 | verified |
| V = 100 kV, v/c | 0.5482 | 0.5482 | 0.54822086 | verified |
| V = 100 kV, v/v_NR | 0.8763 | 0.8763 | 0.87629547 | verified |
| V = 100 kV, λ (pm) | 3.701 | 3.701 | 3.7014366 | verified |
| V = 100 kV, λ/λ_NR | 0.9544 | 0.9544 | 0.95439681 | verified |

## E. The table of §1.8.3, cell by cell

The page and Chromium agree in every cell.

- "Independent" for the Boris error is the closed form 2 sin(δ/2)·√(1+(π/N)²), with δ = 20N(θ − 2 arctan θ/2).
- For the RK4 error there is no closed form here. The cell is verified by recomputation and by its agreement in trend with the phase estimate.
- For the energy it is the exact relativistic ΔK/K implied by \|R\|².
- The N column prints 16.0, 32.0, 64.0 (m8).

| N | column | page | independent | verdict |
|---|---|---|---|---|
| 16 | Boris error | 1.45 | 1.4467957 | verified |
| 16 | Boris predicted | 1.42 | 2 sin(δ/2) = 1.41969 | verified as computed (definition m4) |
| 16 | RK4 error | 0.0215 | estimate 0.0235 | verified |
| 16 | RK4 predicted | 0.0235 | 0.023546 | verified as computed |
| 16 | RK4 energy | 0.0137 | 0.0137499 | verified |
| 16 | RK4 energy predicted | **0.0138** | 0.0137499 | **wrong, because** E9. Correct: **0.0137**. |
| 16 | Boris energy | noise | −4.0 × 10⁻¹⁵ | verified |
| 32 | Boris error | 0.401 | 0.4006361 | verified |
| 32 | Boris predicted | 0.399 | 0.398719 | verified as computed |
| 32 | RK4 error | 0.00144 | estimate 0.00154 | verified |
| 32 | RK4 predicted | 0.00154 | 0.0015351 | verified as computed |
| 32 | RK4 energy | 4.39 × 10⁻⁴ | 4.39380 × 10⁻⁴ | verified |
| 32 | RK4 energy predicted | **4.40 × 10⁻⁴** | 4.39380 × 10⁻⁴ | **wrong, because** E9. Correct: **4.39 × 10⁻⁴**. |
| 32 | Boris energy | noise | −3.1 × 10⁻¹⁵ | verified |
| 64 | Boris error | 0.101 | 0.1008649 | verified |
| 64 | Boris predicted | 0.101 | 0.1007436 | verified as computed |
| 64 | RK4 error | 9.31 × 10⁻⁵ | estimate 9.69 × 10⁻⁵ | verified |
| 64 | RK4 predicted | 9.69 × 10⁻⁵ | 9.6946 × 10⁻⁵ | verified as computed |
| 64 | RK4 energy | 1.38 × 10⁻⁵ | 1.37839 × 10⁻⁵ | verified |
| 64 | RK4 energy predicted | 1.38 × 10⁻⁵ | 1.37839 × 10⁻⁵ | verified (the printed digits happen to agree; formula E9) |
| 64 | Boris energy | noise | 3.6 × 10⁻¹⁵ | verified |
| 128 | Boris error | 0.0252 | 0.0252308 | verified |
| 128 | Boris predicted | 0.0252 | 0.0252232 | verified as computed |
| 128 | RK4 error | 5.92 × 10⁻⁶ | estimate 6.07 × 10⁻⁶ | verified |
| 128 | RK4 predicted | 6.07 × 10⁻⁶ | 6.0748 × 10⁻⁶ | verified as computed |
| 128 | RK4 energy | 4.31 × 10⁻⁷ | 4.31139 × 10⁻⁷ | verified |
| 128 | RK4 energy predicted | **4.32 × 10⁻⁷** | 4.31139 × 10⁻⁷ | **wrong, because** E9. Correct: **4.31 × 10⁻⁷**. |
| 128 | Boris energy | noise | −2.0 × 10⁻¹⁵ | verified |
| 256 | Boris error | 0.00631 | 0.00630814 | verified |
| 256 | Boris predicted | 0.00631 | 0.00630766 | verified as computed |
| 256 | RK4 error | 3.74 × 10⁻⁷ | estimate 3.80 × 10⁻⁷ | verified |
| 256 | RK4 predicted | 3.80 × 10⁻⁷ | 3.7992 × 10⁻⁷ | verified as computed |
| 256 | RK4 energy | 1.35 × 10⁻⁸ | 1.34761 × 10⁻⁸ | verified |
| 256 | RK4 energy predicted | 1.35 × 10⁻⁸ | 1.34761 × 10⁻⁸ | verified (digits agree; formula E9) |
| 256 | Boris energy | noise | −5.6 × 10⁻¹⁵ | verified |
| 512 | Boris error | 0.00158 | 0.00157705 | verified |
| 512 | Boris predicted | 0.00158 | 0.00157702 | verified as computed |
| 512 | RK4 error | 2.34 × 10⁻⁸ | estimate 2.37 × 10⁻⁸ | verified |
| 512 | RK4 predicted | 2.37 × 10⁻⁸ | 2.3749 × 10⁻⁸ | verified as computed |
| 512 | RK4 energy | 4.21 × 10⁻¹⁰ | 4.21088 × 10⁻¹⁰ | verified |
| 512 | RK4 energy predicted | **4.22 × 10⁻¹⁰** | 4.21088 × 10⁻¹⁰ | **wrong, because** E9. Correct: **4.21 × 10⁻¹⁰**. |
| 512 | Boris energy | noise | 2.0 × 10⁻¹⁵ | verified |

## F. Numerical method: the text against `physics/ch01.js`, line by line

| text says | code does | verdict |
|---|---|---|
| State (r, u), u = γv; (1.19) | `rhs`: v = u/γ, du/dt = (q/m)(E + v × B), with `gammaOf(u) = √(1 + u·u/c²)` | verified |
| RK4 (1.20): four slopes, weights 1, 2, 2, 1 | `rk4Step`: k1…k4 on u. The r-slopes are v(u) at the same stages, as RK4 on the joint system requires, since uniform fields do not depend on r. | verified |
| "four evaluations of the fields per step" | four `rhs` calls per step | verified |
| Boris (1.22): a = qh/(2m); u⁻ = u + aE; t = aB/γ⁻; s = 2t/(1+t²); u′ = u⁻ + u⁻ × t; u⁺ = u⁻ + u′ × s; + aE | `borisKick`: identical, statement for statement | verified |
| r_{n+1} = r_n + h u_{n+1/2}/γ_{n+1/2} | `r = add(r, scale(uh, h/gammaOf(uh)))` | verified |
| "u lives at the half steps" | Start: `uh = borisKick(u, E, B, −h/2)` (back half step). End: `u = borisKick(uh, E, B, h/2)` to bring u to the final whole step. | verified; the two synchronising half kicks are not mentioned in the text |
| "one field evaluation per step" | one `borisKick` per step | verified |
| Time step h | `n = ceil(t_run/dt)`, `h = t_run/n`. The step used is t_run/n, not dt. The test passes dt = T/N·(1 + 10⁻⁹) so that n = 20N and h = T/N exactly. | verified (not stated in the text) |
| Energy change "relative change of the kinetic energy" | `energy_drift = gammaM1(u)/gammaM1(u0) − 1`, with γ − 1 = u²/(c²(1+γ)) and no cancellation | verified |
| r_L, Ω quoted as the test's gyroradius and frequency | `r_g`, `omega_c` are analytic (γ₀mv₀ sin θ₀/(eB), eB/(γ₀m)), not measured from the path | verified (analytic, as the text implies) |
| Exact helix for the error | `text/ch01.py`: the exact position after 20 turns is (0, 0, v₀ cos χ·20T) | verified against (1.16) |
| Field directions: text E = (0,−E,0), B = (0,0,−B_p) | `E = [0, p.E_field, 0]`, `B = [0, 0, p.B_field]` | **wrong, because** the conventions differ and the prose does not convert (E1) |
| "measured on the path after the plates", Example 1.1 "the solver puts the spot" | The run stops at the time t_run = l/v₀ (x_end = 0.0499995 m, not 0.05). The spot is `y_end + tan(theta_end)·L`. | verified up to the sign. The stop at fixed time makes the §1.9.1 decomposition exact (m11). |
| §1.10: "independent NumPy implementation" | `ref/ch01.py` header: "Mirrors physics/ch01.js line by line" | overstated (m10) |
