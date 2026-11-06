# Check of section 6.7, "Rough roads, the tyre's grip, and shaking from below" (Fig. 12, beer-slosh.html)

Checked 6 November 2026 on branch `claude/fig12-realtime-fluid`, against `public/scripts/stout-cart.js` (Road.profile, Road.zr,
Cart.forces), `tools/fig12/roads.cjs`, `tools/fig12/study.cjs` and `notes/fig12/phase1.md` §3, §6. The page was not edited.
`plan.md` was not read.

How the checks were run (scripts in the session scratchpad, not in the repository):

- SymPy (`sym.py`): the variance of (R1), the integrals behind the expected rms, the averaging of (R3), the threshold (R4).
- Node, loading the page's own `stout-cart.js` (`grip.cjs`): `Road.rms` for every road, and every bump run (10 and 25 mm,
  live `nm` model and `modal`, open loop / PI speed / slosh feedback, 2.3 s) with `Cart.forces` wrapped so that every
  step's tyre load N, raw motor push b·i and slip flag are recorded.
- Headless Chromium (Playwright, the page served from `public/`): the Road menu switched through all six roads, reading
  `Fig12.world.cart.road.rms`, `c.mu`, `f_body = √(k/(M_b + m_ℓ))/2π`, and the live fluid's `zeta[0]`.
- Re-runs: `node tools/fig12/roads.cjs nm` (13.7 s) and `node tools/fig12/study.cjs 25 speed 0` (8.9 s).

## Equations

| Item | Verdict |
|---|---|
| (R1) z_r = Σ √(2Δn G_d(n_i)) cos(2πn_i x + φ_i), n_i = iΔn, Δn = 1/L | verified. SymPy: the mean of (a cos(2πix/L + φ))² over L is a²/2, cross terms i ≠ j vanish, so a_i = √(2Δn G_d) gives a_i²/2 = G_d Δn and the variance is Σ G_d Δn. Units: G_d in m³, Δn in 1/m, so a_i is in m. The code (`Road.profile`, the `iso` branch) does this exactly: amp = √(2·dn·G0·(n/n0)^−2), phases 2π·rng.u(), dn = 1/(xmax − xmin) = 1/126. |
| Variance statement "Σ G_d Δn ≈ ∫ G_d dn" | verified as a statement. But see the next two rows: for this road the sum and the integral differ by 11 % in variance. |
| "The page sums from 0.011 to 10 cycles/m" | wrong, because the loop starts at k = ceil(0.011/Δn) = ceil(1.386) = 2, so the first wave is at n = 2/126 = 0.0159 cycles/m (63 m long), not 0.011 (91 m). The upper end, 10 cycles/m (k = 1260), is right. Shown in Node and in Chromium (`n_first` = 0.015873). |
| (R2) \|F_m\| ≤ μN, F_m = clip(b i, −μN, μN), μ = 0.8 | verified. `Cart.forces`: `Fgrip = mu*N`, `Fmotor` clipped to ±Fgrip, `slip = 1` when clipped. N is set to 0 when negative, so a wheel in the air pushes nothing. μ = 0.8 read in Chromium. The text's description (wheel spin not modelled, motor tied to the cart's speed) matches the code comment and the code. |
| (R3) q̈ + 2ζωq̇ + ω²(1 + a_z/g)q = 0 | verified. g → g + a_z in ω² = g k tanh(kh) gives the factor. The code uses the same factor (`gf = 1 + az/g`, `stout-cart.js:1149`; clipped at 0 in free fall at :1265, :1286). Units: a_z/g has no dimension. Limit a_z = 0: the damped oscillator of (16). |
| Averaging: q = c cos ωt + s sin ωt, ċ = −ζωc − ¼εωs, ṡ = −ζωs − ¼εωc | verified. SymPy, variation of parameters (ċ cos + ṡ sin = 0), averaged over one period with a_z = A cos 2ωt: exactly these two equations, signs included. |
| "c − s grows like e^{(ε/4 − ζ)ωt}" | verified. Eigenvalues of the slow-flow matrix: (ε/4 − ζ)ω for the eigenvector (1, −1), that is c − s, and −(ε/4 + ζ)ω for c + s. |
| (R4) A > 4ζg | verified. Threshold ε/4 = ζ, so A = 4ζg. Limits: ζ = 0 gives threshold 0 (exact tuning, undamped), as Mathieu predicts. It agrees with the textbook growth rate hω/4 for ω²(1 + h cos 2ωt). |
| (R4) 4 × 0.0053 × 9.81 = 0.21 m/s² | verified. 0.2080 m/s². With the code's own ζ₁ = 0.005349 (read in Chromium): 0.2099 m/s². |
| (R4) 2f₁₁ = 6.84 Hz | verified. f₁₁ = 3.421 Hz (phase1 §3; the page's status line reads 3.42 Hz in Chromium), 2f₁₁ = 6.842 Hz. |
| Washboard z_r = (H/2)(1 − cos 2πx/λ), λ = 0.30 m, H = 20 mm | verified against the code. Its rms about the mean is H/(2√2) = 7.07 mm; the code gives 7.04 mm (ramp in). |
| Setts: 150 mm stones, 20 mm joints, tops uniform ±4 mm, 2 mm crown, joints 10 mm deep | verified against the code (P = 0.170, S = 0.150, 0.004·(2u − 1), 0.002·(1 − (2u/S − 1)²), −0.010). |
| Ramp in over 0.5–1 m, road shifted to pass through 0 at 1 m | verified against the code (raised-cosine `ramp`, `z1 = zt` at x = 1 m subtracted before the ramp). |

## Key result box

| Item | Verdict |
|---|---|
| Pumped above 0.21 m/s² at 6.84 Hz | verified (see R4). |
| "a fiftieth of g" | verified as rounding: 0.21/9.81 = 0.0214 = 1/47. |
| Road wavelength 14.6 cm at 1 m/s | verified. v/(2f₁₁) = 1/6.842 = 0.1462 m. |
| "the size of a sett" | verified against the page's own setts: 150 mm stone + 20 mm joint = 170 mm pitch, 150 mm stone. |

## Numbers in the text

| Number | Verdict |
|---|---|
| Expected rms (∫G_d dn)^½, 0.011–10 cycles/m: 3.8, 7.6, 15.3, 30.5 mm | verified as the integral: 3.812, 7.624, 15.247, 30.494 mm (SymPy). Also in phase1 §6. |
| Measured rms of the seeded roads: 3.6, 7.3, 14.5, 29.0 mm | verified. `Road.rms` = 3.63, 7.26, 14.51, 29.02 mm, the same in Node and in Chromium, and as printed in `roads-nm.txt`. |
| "(one realisation each)" as the reason for 3.6 against 3.8 | wrong, because the n_i are whole multiples of 1/L, so the cosines are orthogonal over the road and the mean square of the sum is Σa_i²/2 whatever the phases: it is not random. The expected rms of the sum the code builds (k = 2 to 1260) is 3.60, 7.21, 14.41, 28.83 mm (`grip.cjs`, and `sym.py`). The road's 3.63 … 29.02 mm differ from these by under 1 %, from the ramp and the shift to z(1 m) = 0. The gap to 3.8 … 30.5 mm comes from the sum starting at 0.0159 cycles/m and from the sum of G_dΔn not being the integral (Σ1/k² from k = 2 is 0.644, the integral from 1.386 is 0.721). It does not come from chance. |
| Class means G_d(n₀) = 16, 64, 256, 1024 × 10⁻⁶ m³, n₀ = 0.1, w = 2 | verified against the code (`Road.GD`, n0) and phase1 §6. The source [18] was not read: unverifiable against the paper itself in this check. |
| "Real paved roads are mostly A to C [20]" | verified against phase1 §6 (A 18 %, B 58 %, C 23 %, D 1 %). [20] itself was not read. |
| Laboratory ripples 50–500 mm [21], a surveyed road 20.6 mm [22], setts 15 × 15 cm, 12–30 mm joints [23] | consistent with phase1 §6. The papers were not read: unverifiable here. |
| Smallest tyre load on the bumps 4.4 N | verified. 3D solver (`study.cjs 25 speed 0`, re-run): 4.42 N. Live model: 4.36 N (PI speed), 4.38 N (slosh), 6.94 N (open loop); 10 mm bump about 15.0 N. |
| 4.4 N "holds 3.5 N" | verified. 0.8 × 4.42 = 3.54 N. |
| "more than the PI loop asks then"; "on the bumps the clip never acts" | verified. At the step with the smallest load the raw push \|b i\| is 0.54 N (PI) and 0.75 N (slosh). Across every step of every bump run (2 models × 2 bumps × 3 controllers, 25 760 steps each), the largest \|b i\|/(μN) is 0.51 and the slip flag is never set. |
| `study.cjs 25 speed 0` still gives 29.9 mm | verified. Re-run: dw 29.9 mm (t 0.94 s), the same line as `runs/study_25_speed_0_0.004.txt`. |
| Setts: wheel off the road 1–2 % of the time, at the grip limit 2–4 % | verified against `roads-nm.txt`: off the road 1.3, 2.0, 1.9 %; at the grip limit 1.8, 3.7, 4.0 % (1.8 rounds to 2). |
| Band rms at 1 m/s: A 0.017, B 0.034, C 0.064, D 0.142 m/s² | verified (open-loop rows of `roads-nm.txt`). The speed and slosh rows give 0.035 (B), 0.068–0.069 (C), 0.134–0.136 (D). The text quotes only open loop and does not say so. |
| Setts 0.034–0.090, washboard 0.13–0.15 m/s² | verified (0.090, 0.034, 0.037; 0.132, 0.151, 0.139). |
| "multiply by √2 for the amplitude" | verified. `roads.cjs` sums 2\|X\|²/N² per bin, the mean square of a sine. So √band is an rms, and amplitude = √2 × rms. Note on the method: the bins are 6.5 Hz + k/4.5 s (6.50, 6.72, 6.94, 7.17 Hz). 6.5 Hz is not a whole multiple of 1/4.5 s, so the bins are not the DFT's orthogonal ones and leak a little. The numbers are estimates, as the text implies. |
| 0.142 × √2 = 0.20 m/s² | verified (0.2008). |
| "Only class D and the washboard reach the threshold's order" | verified. Amplitudes: D 0.20, washboard 0.19–0.21, setts at most 0.13, C 0.09–0.10 m/s². |
| Body bounce 2.8 Hz (section 6.5) | verified. The page says 2.8 Hz, not 2.6 Hz. f_body = √(k/M_s)/2π = √(600/1.9266)/2π = 2.809 Hz, read in Chromium from the page's own cart. The coupled bounce of (31), Example 6.1, is 2.77 Hz. Both round to 2.8. |
| Road in band before the suspension: 0.36 and 0.72 m/s² for C and D | verified. (2π)⁴G_d(n₀)n₀²(f₂³ − f₁³)/3 at v = 1 m/s, 6.5–7.2 Hz: 0.362 and 0.724 m/s² (A 0.091, B 0.181), as in phase1 §6. |
| "Six seconds at 1 m/s, the live model" (Table 2a caption) | verified. `roads.cjs` defaults: T = 6 s, v0 = 1 m/s, model `nm`. |
| Washboard ripples pass 3.3 times a second | verified. 1/0.30 = 3.33 Hz, against f₁₁ = 3.42 Hz. |
| Open loop "loses a quarter of itself in six seconds" | verified. 105.7 g of m_ℓ,0 = 426.6 g (M_s − M_b, read in Chromium) = 0.248. |
| PI still spills 60 g; slosh feedback lean 3 mm, nothing spilled | verified (60.1 g; 3.0 mm, 0.0 g). |
| v = λf₁₁ = 1.03 m/s | verified. 0.30 × 3.421 = 1.026 m/s. |
| "the swing reaches the breaking limit (section 11.9), where the live model clips it" | unverifiable within the 20-minute limit. The clipping code in stout-nm / NMFluid was not traced. |
| "Faster or slower than 1 m/s the washboard is far milder" | unverifiable. No run at other speeds is given, and none was made in the time limit. `node tools/fig12/roads.cjs nm washboard off,speed,slosh <v0>` would test it. |

## Table 2a against `notes/fig12/runs/roads-nm.txt`

The run file was reproduced exactly: a fresh `node tools/fig12/roads.cjs nm` matches all 18 lines, apart from the timing field.

| Row | Page: open loop / PI / slosh | Run file | Verdict |
|---|---|---|---|
| ISO A (3.6 mm rms) | 7.6 / 2.2 / 0.1 mm | 7.6 / 2.2 / 0.1, rms 3.6 | verified |
| ISO B (7.3 mm) | 15.6 / 4.3 / 0.2 | 15.6 / 4.3 / 0.2, rms 7.3 | verified |
| ISO C (14.5 mm) | 28.9 / 8.4 / 0.4 | 28.9 / 8.4 / 0.4, rms 14.5 | verified |
| ISO D (29.0 mm) | 39.5, 1.2 g / 15.6 / 0.7 | 39.5, 1.2 g / 15.6, 0 g / 0.7, 0 g; rms 29.0 | verified |
| Washboard (λ 0.30 m) | 66.7, 105.7 g / 81.4, 60.1 g / 3.0, 0 g | identical | verified |
| Setts | 18.8 / 16.2 / 5.3 | 18.8 / 16.2 / 5.3, no spill | verified |

## Errors

1. "The page sums from 0.011 to 10 cycles/m": the code's first wave is at 2/L = 0.0159 cycles/m (k = ceil(0.011 × 126) = 2), not 0.011.
   Command: `node -e "console.log(Math.ceil(0.011*126)/126)"`.
2. "(one realisation each)" is the wrong reason for the measured 3.6/7.3/14.5/29.0 mm against the expected 3.8/7.6/15.3/30.5 mm.
   With n_i = i/L the rms of the road does not depend on the random phases. The sum the code builds is expected to give
   3.60/7.21/14.41/28.83 mm, and it does, to within 1 % (from the ramp and the shift). The gap to the integral comes from the band
   starting at 0.0159 cycles/m and from the sum not being the integral. It does not come from chance.
3. Minor, not wrong: the band values quoted for B, C and D (0.034, 0.064, 0.142) are the open-loop runs. The speed and slosh runs give
   0.035, 0.068–0.069 and 0.134–0.136. The text does not say which column it quotes.

Everything else in 6.7 checks out: (R2)–(R4), the factor ¼, the signs, 0.21 m/s², 6.84 Hz, 14.6 cm, 1.03 m/s, 4.4 N and 3.5 N
(the grip never binds on the bumps), 29.9 mm, Table 2a, and 2.8 Hz.
