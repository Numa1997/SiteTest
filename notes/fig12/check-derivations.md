# Fig. 12 · independent check of the lecture note (derivations, units, numbers, method)

Page: `public/simulations/beer-slosh.html` (note = `<article id="paper">`, physics script in the same file), data `public/scripts/slosh-modes.js`.
Checked 5 November 2026 against commit `7c455d8` plus the working tree. `notes/fig12/plan.md` was not read.

**How.** Each equation was derived again in SymPy 1.14, then checked numerically in SciPy 1.18. Every number on the page was recomputed from the page's own code. That code was loaded in headless Chrome (Playwright, `/usr/bin/google-chrome`, page served from `public/` on localhost). The store `Sim.data.ds` and the hooks `window.SLOSH.step/seed/etaWall` were read after the page's sliders and buttons were driven.
`tools/fig12/check_cylinder.py` was run with `python3 -B` so that it wrote nothing. `notes/fig12/gate.cjs` was copied to the scratchpad, pointed at Chrome, and run with its output written there. No repository file except this one was changed.
Three sources were opened to check the constants the note quotes from them: Sauret et al. (arXiv:1411.6542), Irvine's tutorial, and `tools/fig12/glass.glb`.
Wolfram Language was not available here (`wolframscript` is not installed). Claims that rest on Wolfram alone are marked unverifiable. All of them were re-checked in SciPy.

Defaults used throughout: V = 500 mL, tulip, h_f = 18 mm, T = 6 °C, μ₆ = 2.06 mPa·s, ρ = 1007 kg/m³, σ = 45 mN/m, ε_f = 0.15, c_s = 1, γ_c = 0.05 s⁻¹, k_f = 1.

## Summary

- All 18 numbered equations are verified, including their units and limiting cases.
- Three equations need small caveats:
  - (11) treats surface tension as if the mode were a deep Bessel mode.
  - (16) reuses the letter E for an integral that is not the energy of (14).
  - The bulk rate 2νλ² is the open-water value. In a cylinder the exact value is 1.88νk², a 0.1 % effect on the total.
- The items I was asked to look at closely are all correct:
  - the dynamic boundary condition (6);
  - the modal equation (12), with λQ/(1+μ_f) and the definition of Q;
  - the head added mass (11);
  - the Stokes-layer dissipation (15)–(16);
  - the coefficient 3.50 in (17), which is 3.5029;
  - the Faraday rate εω/4 (Floquet rate / (εω/4) = 0.9967 even at ε = 0.339) and the threshold (13);
  - Q = 2a/(ξ²−1).
- **Wrong (5 items):**
  1. The integrator's Faraday growth rates in §6 ("0.6 per second in the first two seconds … 1.1 per second from the fifth second"). The page's integrator, the gate script and an independent SciPy run all agree. The amplitude first *falls* about tenfold to a minimum near t = 1.5 s, then grows at 1.21 s⁻¹ from about t = 2 s on.
  2. The viscosity fall from 6 to 20 °C is 31 %, not 32 %.
  3. 568 mL fills the glass to 151.9 mm, not 152.0 mm. `glass.py` interpolates on a staircase, which biases the height up.
  4. "Agree … to 7×10⁻⁵" is true for mode (1,1) only. Other modes are off by up to 3×10⁻³.
  5. The Figure 2 curves cross at about 475 mL (z_s ≈ 132.5 mm), not at the widest point (121 mm, ≈ 415 mL).
- **Method text against the code:** the note matches the code, with three small gaps:
  - the shaker is eased in over 0.3 s, which the note does not say;
  - "scaled to the present one" for the cut fields means the arrows are placed on the present fill, but their values are not rescaled;
  - the automatic "calm" reset at |a| > 2a is not mentioned.

## A. Numbered equations

| # | Item | Independent result | Verdict |
|---|---|---|---|
| (1) | Navier–Stokes in the glass frame with −ρ a_g | Standard. In a frame that translates without turning, the only extra force is −ρ a_g. Every term has units N/m³. | verified |
| (2) | g − a_g = −∇Ψ, Ψ = (g+z̈)z + ẍx + ÿy | SymPy: g − a_g + ∇Ψ = 0 identically. Units m²/s². | verified |
| (3) | ∂ω/∂t = ∇×(u×ω) + ν∇²ω | SymPy confirms the identity (u·∇)u = ∇(u²/2) − u×ω for a general field. The curls of ∇p and ∇Ψ vanish because ρ is constant, which gives (3). Every right-hand term contains ω. | verified |
| (4) | δ = √(2ν/ω) | SymPy: u = U[cos ωt − e^{−s/δ}cos(ωt − s/δ)] solves u_t = νu_ss with u(0) = 0 exactly when δ = √(2ν/ω). Units m. ν→0 gives δ→0. One wording point: δ is the diffusion length over a time 1/ω, not over a whole period; over one period vorticity spreads about √(2π)·δ ≈ 2.5δ. The formula is right; the sentence is loose. | verified (formula); wording loose |
| (5) | Unsteady Bernoulli φ_t + ½\|∇φ\|² + p/ρ + Ψ = C(t) | Follows from (1) when u = ∇φ, ω = 0 and μ∇²∇φ = μ∇(∇²φ) = 0. | verified |
| (6) | φ_t + (g+z̈)η + ẍx + ÿy = 0 at z = z_s | Put p = p_air and Ψ at z_s+η into (5) and drop ½\|∇φ\|². The remaining term (g+z̈)z_s is a function of time only, so it goes into φ. All terms m²/s². Keeping z̈η while dropping \|∇φ\|² is consistent, because z̈ is an O(1) parametric coefficient. | verified |
| (7) | φ = A J_m(kr)cos mθ cosh k(z+D)/cosh kD cos ωt | SymPy for m = 0, 1, 2: the Laplacian residual is 0 and ∂_zφ(−D) = 0. Finite on the axis. | verified |
| (8) | ω² = g k tanh kD, k = ξ_mn/a | SymPy: φ_tt + gφ_z = 0 at z = 0 gives this exactly. Shallow limit gives gk²D; deep limit gives gk. | verified |
| (9) | Meridional Laplace with −m²Φ/r²; ∂_nΦ = 0 on the glass; ∂_zΦ = λΦ at the surface, λ = ω²/g | Follows from φ = Φ cos mθ cos ωt and (8)'s surface condition −ω²Φ + gΦ_z = 0. | verified |
| (10) | Weak form ∫∫(Φ_rψ_r + Φ_zψ_z + m²Φψ/r²) r dr dz = λ∫₀^a Φψ r dr | SymPy: (strong form)·ψr − (weak integrand) = ∂_r(rΦ_rψ) + ∂_z(rΦ_zψ) exactly. The divergence theorem then leaves only the surface flux λΦ. The axis term vanishes through the factor r. The program is 16×40 P2 elements with Schur condensation and a symmetric `eigh` (`modes.py` lines 6–7 and 73–75), as the note says. | verified |
| (11) | ω² = (gλ + σλ³/ρ)/(1+μ_f), μ_f = M_fλ/ρ | Newton's law for the head layer adds M_fη̈ to the surface pressure. Its static part M_f(g+z̈) is uniform and goes into φ. Surface tension adds −σ∇²η. Projecting onto the mode, SymPy reproduces (11) exactly **if −∇_h²f = λ²f**. That holds for a deep cylinder (k = λ, tanh kD = 1.0000 here). For the tulip, the σ term is an approximation (λ² stands in for the horizontal wavenumber squared). It is a 1 % term, so the effect is negligible. Units 1/s², μ_f dimensionless. Limits: M_f, σ → 0 gives gλ; large λ gives capillary waves. The note's reading of μ_f as the head mass over the mass of a stout layer 1/λ deep is right. | verified (σ term exact for deep cylinder, approximate for the tulip) |
| (12) | ä + 2γȧ + ω²(1+z̈/g)a = −λQ ẍ/(1+μ_f), Q = ∫f r²dr / ∫f² r dr | Insert η = a f cos mθ and φ = (ȧ/λ)Φ cos mθ into (6) with the head term. Multiply by f_k cos mθ r and integrate; ∫cos²θ dθ = π on both sides, so the angular factors cancel. SymPy: (1+μ)ä/λ + (g+z̈)a + Qẍ = 0 is identical to (12). λQ/(1+μ_f) is correct and Q is correctly defined; units: λQẍ is m/s². Static-tilt limit: (12) gives a_n = −Q_nẍ/g, so η = −(ẍ/g)Σ Q_n f_n cos θ. With 60 Bessel modes, Σ Q_n f_n(r)/r = 1.000 ± 0.0005 inside the glass, which is the exact tilted plane, with or without the head. Only m = 1 is forced, since ∫cos mθ cos θ = 0 otherwise. The code (`deriv`) multiplies only the gravity part by (1+z̈/g): `O2 = (λ(g+AZ) + σλ³/ρ)/(1+μ)`. That is the physically right split, and it matches the note's remark that σ is left out of (12). | verified |
| (13) | εω/4 > γ ⟺ A > 4ζg/Ω² | z = A sin Ωt gives 1 + z̈/g = 1 − ε sin Ωt with ε = AΩ²/g, which is correct. A Floquet computation of ä + ω²(1 − ε sin 2ωt)a = 0 (SciPy, rtol 1e-12) gives rate/(εω/4) = 1.0000, 0.9999 and 0.9997 at ε = 0.01, 0.05 and 0.1, and 0.9967 at ε = 0.339. Algebra: εω/4 > γ gives A > 4γg/(ωΩ²) = 4ζg/Ω². Units m. The page's integrator with the shaker at exactly 2f₁ (σ split included) gives late growth rates of −0.0015 s⁻¹ at 0.58 mm and +0.0156 s⁻¹ at 0.60 mm, so the threshold lies between them. | verified |
| (14) | γ = P̄/(2E) | dE/dt = −P̄ and E ∝ e^{−2γt}. E = kinetic energy as the surface passes level = total energy. | verified |
| (15) | P̄_w = (ρ/2)√(νω/2) ∫\|∇_tφ\|² dS | SymPy: the period average of (∂u/∂s)² is (U²/δ²)e^{−2s/δ} (the note is right). Its integral is U²/(2δ). Then μU²/(2δ) ÷ [(ρ/2)√(νω/2)U²] = 1 exactly. This agrees with Landau–Lifshitz §24, √(ηρω/8)·v₀². Units W/m² per area. | verified |
| (16) | γ_w = ½√(νω/2)(I_w+I_b)/E, I_w = ∫(Φ_ℓ² + m²Φ²/r²) r dℓ | Correct, provided E here means the θ-free integral ∫∫\|∇Φ\|² r dr dz = λ∫f² r dr (Green's identity, which is right). It is **not** the energy E of (14); the note reuses the letter. The θ-averages (π for m ≥ 1, 2π for m = 0) cancel in the ratio. Units: I/E is 1/m, times √(νω) gives 1/s. Deep-cylinder check, m = 1: I_w/E = (1+1/ξ²)/[a(1−1/ξ²)] = 1.83683/a, the same from the elementary integrals and from the code's `cylinder()` formula. The code's Iw, Ib, Is formulas in `cylinder()` were rederived (∫sinh² = S₂/4k − D/2, ∫cosh² = S₂/4k + D/2, ∫J_m² r dr = a²/2·(1−m²/ξ²)J_m²): all correct. | verified (notation caveat: E in (16) ≠ E in (14)) |
| (17) | Δ₁₁ = 3.50 ν^½ a^−¾ g^−¼ (theory); 4.98 (tanks) | Δ = 2πγ/ω with the deep-cylinder ω = √(gξ/a) and no head gives Δ/(ν^½a^−¾g^−¼) = π(ξ²+1)/(√2·ξ^¼(ξ²−1)) = **3.50292** (SymPy, ξ = 1.841184). Dimensionless. The 4.98 is confirmed in Irvine's tutorial (Eq. 2, "for h/a > 1", log decrement). 4.98/3.5029 = 1.4217, so "1.42" is right. | verified |
| (18) | γ_f = k_f(U_f/a)(1 − e^{−λh_f}), U_f = 1.6 cm/s | Wall area per volume is 2πah/(πa²h) = 2/a, against 2/w in a slot, so the mapping wγ_f → aγ_f is consistent. Sauret et al. (arXiv v2, p. 11): "w/τ_f∞ = 1.6 ± 0.3 cm s⁻¹" from the exponential trend (best fit 3.1). Their 1/τ is an amplitude rate (η₀e^{−t/τ}), so it matches the page's γ. Their saturation length is ξ_cD ≈ 17 mm, the same order as 1/λ ≈ 21 mm, so (1 − e^{−λh_f}) is a reasonable transfer. Limits: h_f → 0 gives 0; h_f → ∞ gives U_f/a. Units 1/s. | verified (transfer to a round glass is, as the note says, an inference) |
| — | Bulk damping γ_b = 2νλ² | Exact for a mode that decays as e^{kz} with no side walls: ∫e_ije_ij dV = ½∮∂_n\|∇φ\|²dS gives 2νk². In a deep cylinder the wall term lowers it. For (1,1) the exact irrotational value is **1.877 νk²**, found two ways that agree to 5 digits: a 3-D quadrature and the surface identity. Effect at the default pint: 0.00914 → 0.0086 s⁻¹, i.e. 0.1 % of γ = 0.497. | verified as the deep-water value the note names; in a cylinder it is 6 % high, which is negligible |
| — | Q = 2a/(ξ²−1) for a cylinder | ∫₀^a r²J₁(kr)dr = a²J₂(ξ)/k, ∫₀^a rJ₁²dr = (a²/2)(1−1/ξ²)J₁²(ξ), and J₂(ξ) = J₁(ξ)/ξ at a zero of J₁′ (residual 2e−16). Together they give Q = 2a/(ξ²−1). Quadrature confirms it to 8 digits for ξ₁₁, ξ₁₂ and ξ₁₃. With f = J₁(kr) unnormalised, 2a/((ξ²−1)J₁(ξ)) = 0.057528 m at a = 40 mm, and `check_cylinder.py` prints FEM 0.057528. | verified |
| — | Resonant amplitude a_n = λQAω²/[(1+μ_f)2γω] | (12) at Ω = ω gives \|a\| = F/(2γω) exactly. | verified |
| — | Kinematic condition ∂_tη = ∂_zφ, and φ = Σ(ȧ_n/λ_n)Φ_n | ∂_zΦ = λΦ at the surface, so ∂_zφ = Σȧ_n f_n = ∂_tη. | verified |

## B. Numbers in the note

Page values were read from the store in Chrome. "nj" means `notes/fig12/numbers.json`.

| Where | Note says | Recomputed | Verdict |
|---|---|---|---|
| Abstract, §7 | settles in ~6 s with head, ~11 s without | t₅% = ln20/γ = 6.029 s; without head 11.065 s | verified |
| §1 | rocks about 3 times a second | f₁ = 3.2438 Hz | verified |
| §2 | 0.393 mm/px | `glass.py`: S = 160/(449.0 − 41.5) = 0.39264. The pixel rows of the ellipse centres need the photograph, which is not in the repository. | verified (arithmetic); unverifiable, because the pixel rows need the photograph |
| §2 | smoothed to 0.2 mm | `UnivariateSpline(..., s = n·0.2²)` | verified |
| §2 | widest diameter 84.1 mm, 1 % below 85 | 2·max R_outer = 84.14 mm; (85 − 84.14)/85 = 1.0 % | verified |
| §2 | wall 2.0 mm, base 8 mm | `wall_mm` 2.0, `floor_mm` 8.0 (inputs) | verified (as used) |
| §2 | 603.7 mL to the brim | ∫πR_i²dz on the page profile gives 603.70 mL (603.72 on the 0.5 mm profile) | verified |
| §2 | 568 mL fills to **152.0 mm**, 8 mm below the rim | Proper interpolation gives **151.92 mm** on both the 0.5 mm and the 2 mm profile, i.e. 8.1 mm below the rim. `glass.py` gets 151.99 because `vol(h)` only counts grid points ≤ h, a staircase on a 0.5 mm grid that biases heights upward. (The same bug writes `z_500_mm` = 137.95 into `glass_profile.json`; the page itself uses the correct 137.54.) | wrong, because the correct height is 151.9 mm (8 mm below the rim still holds) |
| §2 | Blender mesh 96 sides, 603.3 mL | `tools/fig12/glass.glb`, mesh `glass_inner`: 96 distinct angles; closing the open top loop gives 603.29 mL | verified |
| §2 | factor (96/2π)sin(2π/96) = 0.99929; 0.4 mL | 0.999286; 603.7 × (1 − 0.999286) = 0.43 mL | verified |
| Fig. 1 | waist 27 mm, widest 121 mm, rim 78 mm | Inner minimum by parabola through the 26/28/30 mm samples at 27.1 mm; maximum R at the 120 and 122 mm samples (equal), i.e. 121; rim outer diameter 78.05 mm | verified |
| §2 table | ρ 1007, μ₆ 2.06 mPa·s, σ 45 mN/m, h_f 18 mm, ε_f 0.15 | Same values in `P` in the page script | verified (as used); the source values are citations not re-read here |
| §2 table | Vogel scaling gives a **32 %** fall from 6 to 20 °C | `muWater(20)/muWater(6)` = 0.6874, a **31.3 %** fall (page store: μ = 1.416 mPa·s at 20 °C) | wrong, because the fall is 31 % |
| §2 | ν = 2.05×10⁻⁶ m²/s, twice water at room temperature | 2.0457×10⁻⁶; ratio to water at 20 °C = 2.04 | verified |
| §2 | M_f = 2.72 kg/m² | 0.15 × 1007 × 0.018 = 2.7189 | verified |
| §3 | ω = 20.4 rad/s, δ = 0.45 mm, about 1 % of the radius | ω₁ = 20.3815; δ = 0.4480 mm; δ/a = 1.14 % | verified |
| §4 | ξ₁₁ 1.8412, ξ₂₁ 3.0542, ξ₀₁ 3.8317, ξ₁₂ 5.3314 | SciPy `jnp_zeros`: 1.841183781, 3.054236928, 3.831705970, 5.331442774. These match the page's `XI` table, which also holds ξ₁₃ 8.536316366, ξ₂₂ 6.706133194, ξ₃₁ 4.201188941 and ξ₀₂ 7.015586670, all correct. | verified (SciPy); the Wolfram agreement is unverifiable, because Wolfram is not installed |
| Ex. 4.1 | k₁₁ = 46.03 m⁻¹, tanh = 1.000, ω₁₁ = 21.25 rad/s, f₁₁ = 3.382 Hz | 46.0296; tanh(4.580) = 0.99979; ω = 21.2475 with tanh (21.2498 for √(9.81 × 46.03)); f = 3.3816 | verified (Wolfram part unverifiable, as above) |
| Ex. 4.1 | kD = 6.1 in our pint | λ₁₁D = 47.268 × 0.129539 = 6.123. With k = ξ/a it is 6.047. "6.1" follows from λ, the tulip's analogue of k. | verified (it is λD; ξD/a gives 6.0) |
| §4 key result | pendulum length a/1.84 ≈ 21 mm | 39.441/1.8412 = 21.4 mm | verified |
| §5 | cylinder 40×100 mm: λ₁₁ FEM 46.02036, exact 46.02035, rel. error 3×10⁻⁷ | Ran `check_cylinder.py`: FEM 46.020361, exact 46.020349 (SciPy), error 2.74×10⁻⁷ | verified |
| §5 | worst of nine modes (0,3), 2.4×10⁻⁴; halving the cells reduces every error | (0,3): 2.39×10⁻⁴ on 16×40. Every one of the nine errors is smaller on 16×40 than on 8×20. | verified |
| §5 | damping integrals agree with exact Bessel integrals to 7×10⁻⁵ | `modes.integrals` on the production mesh (16×40) against the exact formulas: (1,1) I_w/E 3.1×10⁻⁵, I_s/E 1.3×10⁻⁷, I_b/E < 10⁻³ of a 0.0185 m⁻¹ term. But (2,1) I_w is off 1.0×10⁻⁴, (1,2) 1.3×10⁻³, (2,2) 2.2×10⁻³, (0,1) 5.1×10⁻⁴ and (0,2) 3.0×10⁻³. | wrong, because it holds for (1,1) only; over the kept modes the wall integral agrees to 3×10⁻³ (the Wolfram cross-check itself is unverifiable here) |
| §5 | tulip 3.14 vs straight 3.25 Hz at 300 mL; 3.37 vs 3.30 at 590 mL | Page store, shape buttons, with head: 3.1433 vs 3.2517; 3.3744 vs 3.3036 | verified |
| Fig. 2 | curves cross near the widest point, where the wall is vertical | Tulip-with-head minus straight-with-head changes sign between 470 and 480 mL (z_s 131.5 → 133.5 mm). The wall is vertical at z = 121 mm, which the surface reaches at ≈ 415 mL (`wall_slope` changes sign between 410 and 420 mL). | wrong, because the crossing is at ≈ 475 mL, z_s ≈ 132.5 mm, about 12 mm and 60 mL above the widest point |
| §5 | σ raises ω² by σλ²/(ρg) = 1.0 % | 0.045 × 47.268²/(1007 × 9.81) = 0.01018 | verified |
| §5 | μ_f,11 = 0.128; head lowers f₁ from 3.445 to 3.244 Hz | 0.12762; 3.4446 → 3.2438 | verified |
| Ex. 5.1 | z_s 137.5 mm, a 39.4 mm, D 129.5 mm; λ₁₁ 47.27 m⁻¹; 3.427 → 3.445 → 3.244 Hz | 137.539, 39.441, 129.539 mm; 47.2684; 3.4272, 3.4446, 3.2438. My own volume integral of the profile gives z_s = 137.54 mm and a = 39.44 mm. | verified |
| §6 | Q coupling, stored Q₁₁ | 0.032454 m stored; Simpson on the 25 stored f samples gives 0.032460. f(a) = 1.000 for every mode. | verified |
| Ex. 6.1 | A = 0.2 mm at f₁ = 3.24 Hz; Aω² = 0.083 m/s² < g/100 | The button sets f = 3.24 Hz (toFixed(2)) and A = 0.2 mm. Aω² = 0.0829 m/s² (0.0831 at the exact f₁) = 0.0085 g. | verified |
| Ex. 6.1 | steady wave at the wall 5.6 mm, 28× the shaking | Formula: 5.567 mm. Page RK4 after 34–40 s: a₁₁ = 5.567 mm, max η at the wall 5.572 mm. Ratio 27.9. | verified |
| §6 | Faraday threshold A = 0.58 mm at Ω = 2ω₁ | 4ζg/Ω² = 0.5758 mm (0.5816 mm with the code's σ split); page integrator threshold between 0.58 and 0.60 mm | verified |
| §6 | 2 mm at 2f₁: (13) predicts a net growth of 1.2 s⁻¹ | Button: f = 6.49 Hz, A = 2 mm, ε = 0.339; εω/4 − γ = 1.2305 (1.213 with the σ split) | verified |
| §6 | page integrator: grows at **0.6 s⁻¹ in the first two seconds**, at **1.1 s⁻¹ from the fifth second on** | Page integrator (button, then `S.step` × 12 000) and the note's own `gate.cjs` (z, 2 mm, 2f₁, 12 s) agree. Amplitude √(a² + (ȧ/ω)²) of (1,1) falls from 1.13 µm to a minimum ≈ 0.11 µm at t ≈ 1.5 s (fit 0–2 s: **−1.28 s⁻¹**). From t ≈ 2 s it grows at **1.206 s⁻¹** (2–5 s), **1.208 s⁻¹** (5–12 s); window maxima in `gate.cjs` give 1.24 s⁻¹. An independent SciPy `solve_ivp` of the same single-mode equation, including the 0.3 s ease-in, gives the same: minimum at 1.50 s, −1.284 / 1.206 / 1.208 s⁻¹. Cause: the seed has ȧ = 0, which projects almost wholly onto the decaying Floquet solution (energy gain ∝ −cos 2φ, φ = 0). | wrong, because the amplitude falls ≈ tenfold (at ≈ 1.3 s⁻¹) during the first 1.5 s, then grows at 1.21 s⁻¹ from about the second second on, in agreement with (13)'s 1.2 s⁻¹ |
| §6 | seed of about a micrometre | `seed()`: 10⁻⁶ sin(1.7k + 0.3), amplitudes ≤ 1 µm, ȧ = 0 | verified |
| §6 | hand follower ẍ = Ω_h²(x_hand − x) − 2Ω_hẋ | `deriv`: identical, Ω_h = 22 rad/s by default | verified |
| §6 | steps 1–2.5 Hz; coffee 2.6–4.3 Hz [2] | Citation not re-read | unverifiable, because the source (Mayer & Krechetnikov) was not reopened for this check |
| §7 | γ/ω is 2 to 4 % | ζ over the 8 kept modes: 2.44 % – 3.49 % | verified |
| §7 | Δ ratio 1.42 | 4.98/3.5029 = 1.4217 | verified |
| §7 | Miles: damping exceeds wall theory by factors of up to 2 or 3 [5] | The note itself says only the abstract was read | unverifiable, because Miles (1967) is behind a paywall and was not opened here |
| §7 | skin at c_s = 1 takes about as much as the wall | γ_s = 0.1054, γ_w = 0.0999 s⁻¹ (ratio 1.05) | verified |
| §7 | bulk 0.009 s⁻¹, 2 % of the total | 2νλ² = 0.00914 s⁻¹; 1.8 % of 0.4969 | verified (exact cylinder value 0.0086, see A) |
| §7 | γ_c default 0.05 s⁻¹, within the 0.05–0.25 s⁻¹ of [7] | Code 0.05. The source range was not re-read. | verified (as used); the source range is unverifiable here |
| §7 | wγ_f = 1.6 ± 0.3 cm/s [1] | Sauret et al. arXiv:1411.6542v2, p. 11: "w/τ_f∞ = 1.6 ± 0.3 cm s⁻¹" | verified |
| Fig. 3 | head takes almost half | γ_f/γ = 0.2324/0.4969 = 46.8 % | verified |
| §7 key result | γ = 0.50 s⁻¹; 1/e in 2.0 s; 5 % in 6.0 s | 0.49691; 2.012 s; 6.029 s | verified |
| §7 key result | without head 0.27 s⁻¹, 3.7 s, 11.1 s | h_f = 0 in the page: 0.27075; 3.693 s; 11.065 s | verified |
| §7 key result | clean walls alone 8.9 s to 1/e | h_f = 0, c_s = 0, γ_c = 0: γ = 0.11216 → 8.916 s. This includes the bulk term (0.0091); walls alone would give 9.71 s. | verified (it is "walls + bulk") |
| §7 key result | everything else at least doubles it | 0.497/0.112 = 4.4 with head; 0.271/0.112 = 2.4 without | verified |
| Fig. 4 | at 480 mL, 1/λ = 21 mm; 63 % lost at one decay length | λ₁₁(480 mL) = 46.533, so 1/λ = 21.49 mm; 1 − 1/e = 63.2 % | verified |
| §9 | 30 fills 300–590 mL; 8 shapes; 14 oscillators; f_n at 25 radii; fields for 6 fills on 12×20 | `vols_mL` 30 entries; `keep` 8; 2 + 6×2 = 14; f length 25; fields at 360/420/480/520/560/590 mL, 720 = 3×12×20 values each | verified |
| §9 | (1,3) at about 6.4 Hz; ωh = 0.04 | 6.4298 Hz; ωh = 0.0404 | verified |
| §9 | RK4 stability limit \|ωh\| < 2.8 | \|R(iθ)\| = 1 at θ = 2√2 = 2.828 | verified |
| §9 | phase error per step ~ (ωh)⁵/120 ≈ 10⁻⁹ | arg R(iθ) − θ = −8.96×10⁻¹⁰, against θ⁵/120 = 8.97×10⁻¹⁰ | verified |
| §9 | arrows longer than 34 px cut short and drawn pink | `Lm = 34`, colour `#e2a2aa` | verified |
| §9 | 3D surface at 16 radii × 72 angles | `NRr = 16` (16 radial intervals, 17 rings), `NT = 72` | verified |
| §4/§9 | warning when the wall wave exceeds a fifth of the radius; warning when g + z̈ < 0 | `aMax > 0.2*geo.a`; `ge < 0` | verified |

## C. Numerical method: note against code, line by line

| Note | Code | Verdict |
|---|---|---|
| RK4, fixed h = 1 ms, integrates the hand follower and the 14 equations (12) | `step()`: classical RK4, `h = 1e-3`, state = 6 glass coordinates + 2·NK amplitudes + 2·NK rates. The two `sin` slots of the m = 0 shapes are frozen (`out[is] = 0`, `out[vs] = 0`), so 14 oscillators really evolve. | verified. Aside: those two frozen slots keep their seeded ≈ 1 µm values in the `a_osc` store, though nothing reads them. |
| as many steps as real time has passed, capped at 50 ms per frame | `n = Math.round(dt/h)`; `sim.js` clock: `dt = Math.min((ts − last)/1000, 0.05)` | verified |
| (12) as written, σ term kept | `O2 = (λ(g+AZ) + σλ³/ρ)/(1+μ_f)`, `Fc = −λQ·AX/(1+μ_f)` for m = 1 only, the sin copy with AY, damping `2γ` | verified |
| shaker x = A sin Ωt (sideways) / z = A sin Ωt (vertical) | `shakerPos = A(1 − e^{−t/0.3}) sin Ωt`, and `shakerAcc` is its exact second derivative, including the envelope terms | wrong, because the code eases the shaker in over τ = 0.3 s and the note does not say so. This affects the first second of the Faraday run and of Example 6.1, not the steady values. |
| damping formulas (16), γ_s, 2νλ², γ_c, (18), with ω from (11) | `setup()`: `sq = ½√(νω/2)` with ω = `omA` (with head); `gw = sq(Iw+Ib)`, `gs = c_s·sq·Is`, `gb = 2νλ²`, `gc = P.gc`, `gf = k_f(U_F/a)(1 − e^{−λh_f})`, `U_F = 0.016` | verified |
| (11) in the code | `omA = √((gλ + σλ³/ρ)/(1 + M_fλ/ρ))`, `M_f = ε_fρh_f` | verified |
| μ(T) by Vogel scaling | `muWater(T) = 2.414e−5·10^{247.8/(T+273.15−140)}`, `μ = μ₆·μ_w(T)/μ_w(6)` | verified |
| interpolation between fills; Bessel quantities for the straight glass | `interpTulip()`: linear in V between neighbouring fills for λ, Q, Iw, Ib, Is and f. `cylinder()`: λ = k tanh kD, Q = 2a/(ξ²−1), exact Iw/Ib/Is, J_m by a 64-point trapezoid (spectrally accurate). | verified |
| the cut uses the fields of the nearest of six fills, "scaled to the present one" | `interpTulip` picks the nearest `field_vols_mL`; `gridPos` places the grid on the present depth and R_i(z); the field values themselves are **not** rescaled (`fieldAt` also divides u_θ by the present a, not R_i(z)) | wrong, because "scaled" overstates it: only positions follow the present fill; the velocities are those of the stored fill |
| head drawn with constant thickness | 3D: top at z + h_f, clipped 6 mm above the rim | verified (the clip is not mentioned) |
| stout see-through while arrows show | `stoutMat.opacity = xray ? 0.55 : 0.94` | verified |
| (not in note) | Clock: if any \|a\| > 2a, the page re-seeds ("the stout was calmed") | omission: not described in the note's method section |

## Scratch files (not part of the repository)

- `/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/derive.py` (SymPy/SciPy derivations)
- `/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/bulk2.py` (exact cylinder bulk damping)
- `/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/page.cjs` and `/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/an.py` (page measurements in Chrome and their analysis)
- `/tmp/claude-0/-home-user-SiteTest/0935aa8a-1d41-50fc-be37-f46e7857f37a/scratchpad/gate_z.json` (output of the note's own `gate.cjs`)
