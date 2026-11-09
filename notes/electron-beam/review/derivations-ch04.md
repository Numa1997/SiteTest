# Chapter 4 "The lens": derivation and number check

Reviewer's check of `public/portfolios/electron-beam/index.html`, `#ch04` (source `portfolios-src/electron-beam/text/ch04.py`;
solver `physics/ch04.js`, twin `ref/ch04.py`, checks `derive/ch04.py`, `data/ch04/derive_results.json`). 9 November 2026.

How it was checked:
- Equations re-derived in SymPy 1.14 (my own scripts, not `derive/ch04.py`): field expansion by matching powers of r; Glaser's ray and
  its asymptotes; Busch and the radial equation solved from the stated equations of motion; the z-as-variable equation of motion
  solved from the Lorentz force; units with `sympy.physics.units`.
- Numbers recomputed by running the page's own `EB.ch04.compute` and `EB.ch03.compute` in headless Chromium 153 (Playwright), on the
  built page served from `public/`. No page errors. Every value shown in `#ch04` was read back from the DOM and compared.
- Independent numerics with SciPy (DOP853, rtol 1e-13), sharing nothing with the solver but the constants and the bell field:
  focusing by Brent's method; f from the exact Glaser solution (mpmath); C_c and C_s from the integrals with `quad`; C_s also from
  a full Lorentz-force trace in time, in the lab frame, through the third-order field.
- Browser against Python reference, four cases (default, 30 kV, WD 5 mm, a 1 mm/WD 2 mm): largest relative difference 9.3e-12.

## Errors found (summary)

1. **§4.2, sentence after (4.2): sign of the radial field is reversed.** The page says B_r "is outwards where B rises and inwards where
   it falls". From (4.2), B_r = -(r/2)B'(z): where B rises along z (entering the gap, B' > 0) B_r < 0, i.e. **inwards**; where B falls
   (leaving the gap) it is **outwards**. The field lines converge onto the gap and spread out behind it. (The §4.1 picture, "the field
   lines bulge outwards near the gap", fits the same mistake; near the axis the lines are pinched towards the axis at the gap.)
2. **Problem 1 points to the wrong equation.** "From (4.9), find ω for which a parallel ray crosses the axis exactly at the lens
   centre." (4.9) is the asymptotic focal length; at the answer, ω = 2, it is infinite (telescopic lens), and using the asymptote
   instead gives ω = 1.5, which is wrong (the real ray then crosses at z = a/√3). The crossing follows from (4.8): r = 0 at
   φ = π − π/ω, which is the centre (φ = π/2) for **ω = 2, k² = 3**, i.e. B₀ = √(3/η)/a = 165 mT and **NI = π√(3/η)/μ₀ = 826 A** at
   800 V (independent of a). Read "From (4.8)".
3. **The C_s measurement carries a bias from its "tiny" ray, so the traced 4.18893 mm and the claim about the gap are off.** The solver
   removes the linear part by subtracting k·(x_e, y_e) from a ray of object slope ε = 1e-7 (image angle ε/M = 5.5e-6 rad). At the
   paraxial image that ray's position (3.6e-19, -6.5e-19 m) is not its linear part (which is about zero, since the wafer is the paraxial
   image) but its own third-order miss, C_s(ε/M)³. Scaled by k = α_o/ε this subtracts C_s ε²/M² · α = 1.29e-13 m · α, a spurious
   linear term. It lowers miss/α³ by 1.29e-13/α² m: 1.3e-4 mm at 1 mrad, 3.2e-5 mm at 2 mrad, 8e-6 mm at 4 mrad, and the two-angle fit
   by 4.0e-5 mm. Measured: with ε = 1e-9 or 1e-10, or with no subtraction at all, the same code gives **C_s = 4.18897 mm**
   (4.1889678), equal to the integral (4.11) (4.1889678 mm) to 1e-7; my Lorentz-force trace gives the same. So: the printed traced value
   4.18893 mm is what the code returns, but the correct traced value of this field model is 4.18897 mm; the sentence "their agreement
   to a few parts in a hundred thousand checks both" credits the methods with a gap that is a defect of the subtraction, not of either
   method; and in check N5 the low first value (4.18885 mm at 1 mrad) is the same artefact (corrected: 4.18898, 4.18900, 4.18911,
   4.18952 mm). The 3-digit values the reader uses (4.19 mm, 12.9 mm, 3.79 mm) do not change. Fix: ε ≤ 1e-9, or drop the subtraction.

No other equation or number is wrong. Remarks that are not errors are in the last column of the tables.

## Equations

| Item | Verdict | Notes |
|---|---|---|
| (4.1) div B = 0, curl B = 0 in cylindrical coordinates, axisymmetric, B_θ = 0 | verified | (1/r)∂(rB_r)/∂r + ∂B_z/∂z and ∂B_r/∂z − ∂B_z/∂r are the r- and θ-components; correct for a current-free static region. |
| Step c₁ = −B′/2 (order r⁰ of the first equation) | verified | SymPy: c1 = −B′/2. |
| Step b₂ = −B″/4 (order r¹ of the second) | verified | SymPy: c1′ − 2b2 = 0, b2 = −B″/4. |
| Step c₃ = B‴/16 | verified | SymPy from order r² of the first equation, 4c3 + b2′ = 0. Only the first equation is needed at this order ("one more order of each" is harmless). |
| (4.2) B_z = B − r²B″/4, B_r = −rB′/2 + r³B‴/16 | verified | Consistent with check L2 (residual r⁴B⁽⁵⁾/64 in div B when the r⁴ term of B_z is kept). |
| Sentence "B_r is outwards where B rises and inwards where it falls" | wrong, because B_r = −rB′/2 is inwards (negative) where B rises along z and outwards where it falls | Error 1. |
| (4.3) Glaser field B₀/(1+(z/a)²); "a = half-width at half maximum" | verified | B(a) = B₀/2. Citation Glaser, Z. Physik 117, 285 (1941): matches the standard citation; paper not opened here. |
| ∫B dz = πaB₀ | verified | SymPy. |
| (4.4) B₀ = μ₀NI/(πa) | verified | Units T = (T·m/A)·A/m. Remark: the law used is ∮H·dl = NI; on a return path through high-permeability iron B is large but H ≈ 0, so "where the field is negligible" should read "where H is negligible". The result is unchanged. |
| (4.5) p_θ = γmr²θ̇ + q r A_θ conserved | verified | Canonical angular momentum of L = −mc²/γ − qφ + q v·A with ∂L/∂θ = 0. |
| A_θ = rB/2 from Stokes | verified | Paraxial (B uniform over the small circle). |
| (4.6) θ̇ = eB/(2γm) for p_θ = 0, q = −e | verified | SymPy; half the cyclotron rate eB/(γm). |
| θ_rot = ∫θ̇ dt = (e/2p)∫B dz = √(e/8mV*)∫B dz | verified | SymPy: e/(2√(2meV*)) = √(e/(8mV*)). Dimensionless (C·T·m/(kg·m/s)). |
| Radial force q(v_θB_z − v_zB_θ) = q r θ̇ B | verified | |
| γm(r̈ − rθ̇²) = −e r θ̇ B and r̈ = −(eB/2γm)² r (unnumbered) | verified | SymPy: −e²B²r/(2γm) + e²B²r/(4γm) = −e²B²r/(4γm); "half the push focuses" is right. |
| (4.7) r″ = −(e²B²/4p²) r = −ηB²r, η = e/(8mV*) | verified | SymPy with d/dt = v d/dz, p = γmv, p² = 2meV* (relativistically exact, V* = V(1 + eV/2mc²)). Units of ηB²: m⁻². Remark: the distance from the axis is the same in every frame; what the turning frame provides is transverse coordinates X, Y (which may be negative) obeying the same equation. |
| Key result box: strength ∝ B²/V*; "four times the voltage at twice the current"; θ_rot formula | verified | Strictly "four times V*" (0.2 % difference at 800 V → 3.2 kV). |
| k² = ηB₀²a², equation r″ + k²a²r/(a²+z²)² = 0 | verified | B² = B₀²a⁴/(a²+z²)². |
| z = a cot φ maps z: −∞ → +∞ onto φ: π → 0 | verified | |
| (4.8) r = sin(ω(π−φ))/(ω sin φ), ω = √(1+k²) | verified | SymPy residual 0 (also for sin(ωφ)/sin φ and cos(ωφ)/sin φ, the general solution). r → 1 and r′ → 0 as φ → π: the parallel ray at unit height. |
| Asymptote r ≈ sin(ωπ) z/(ωa) − cos(ωπ) | verified | SymPy: r − (that line) → 0 as φ → 0. |
| (4.9) f = −ωa/sin(ωπ) | verified | Slope sin(ωπ)/(ωa) = −1/f. Exact Glaser ray (mpmath) between ±2000a gives the solver's f to 2e-10. At ω = 2 the lens is telescopic (ray (4.8) = −cos φ, f infinite). |
| "For 1 < ω < 2 ... one crossing, converging" | verified | Zeros at φ = π − nπ/ω; exactly one in (0, π) for 1 < ω < 2; sin(ωπ) < 0 there. |
| Weak lens: sin(ωπ) ≈ −πk²/2, 1/f → πk²/(2a) = η∫B²dz | verified | SymPy series and limit k²f → 2a/π; η∫B²dz = ηπB₀²a/2. |
| "Same NI over half the length gives twice ∫B²" | verified | ∫B² = (μ₀NI)²/(2πa). |
| M = α_object/α_image from the Lagrange invariant at one voltage | verified | yα conserved at constant V*; the code takes |M| (the image is inverted). |
| (4.10) Δr_s = C_s α³, α at the image | verified | Odd in α, so next term α⁵ as stated. Positivity: Scherzer 1936 (Z. Physik 101, 593; standard citation, paper not opened). |
| Δr_c = C_c α δ, lens strength η/(1+δ) for V*(1+δ) | verified | η ∝ 1/V*. Remark: δ is ΔV*/V*, which is 1.0008 × ΔE/E at 800 V; Example 4.3 uses ΔE/E; no visible effect. |
| Green's-function result C_c = η∫B²h²dz (h(z_o) = 0, unit slope at the image) | verified | Derived: ρ″ + ηB²ρ = ηB²αh, W = −g(z_i), ρ(z_i) = αη∫B²h²dz. Numerically: quad of the integral 2.847594 mm = SciPy central difference 2.847594 mm = solver 2.847594 mm. |
| (4.11) C_s = (e/128mV*)∫[(3e/mV*)B⁴h⁴ + 8B′²h⁴ − 8B²h²h′²]dz | verified | Units: length. Not re-derived symbolically (a full third-order perturbation calculation); verified numerically instead: my quad 4.1889678 mm equals an independent Lorentz-force trace (lab frame, time variable) 4.1889272 mm with the solver's ε, and the solver's own trace with ε ≤ 1e-9 gives 4.1889678 mm. Same agreement for WD 5 mm (12.91194) and a 1 mm (3.78780). h vanishes at both ends, so no boundary terms are lost although the wafer sits in the field (B there is 0.31 B₀). |
| Electric lens: φ(r,z) = ϕ − r²ϕ″/4, E_r = rϕ″/2 | verified | SymPy from Laplace's equation. |
| z-as-variable equation of motion in ch04.js/ref (x″ = (q/p)s[x′y′B_x − (1+x′²)B_y + y′B_z], y″ analogous) | verified | SymPy: solved from d(x′/s)/dz = (q/p)(y′B_z − B_y) etc. |
| Code B′, B″, B‴ of the bell field | verified | SymPy derivatives equal the coded forms. |
| Problem 1 "From (4.9) ..." | wrong, because the crossing of the real ray follows from (4.8): ω = 2, k² = 3, NI = π√(3/η)/μ₀ = 826 A at 800 V; (4.9) is infinite there | Error 2. |
| Problems 2, 3 | verified | 2 follows from (4.7); 3 is well posed (Δr_d ≈ λ/α is an order-of-magnitude form). |

## Numbers (page value, read from the DOM in Chromium; recomputed from the page's own code)

| Number on page | Page | Recomputed (page code in Chromium) | Independent | Verdict |
|---|---|---|---|---|
| NI, default | 346 A | 345.8324 A | 345.8324 A (Brent + DOP853; B₀ rel. 3e-10) | verified |
| B₀ | 69.2 mT | 69.16648 mT | 69.16648 mT | verified |
| μ₀NI/(πa) | 69.2 mT | 69.16648 mT | | verified |
| ω | 1.235 | 1.2351016 | 1.2351016 | verified |
| k² | 0.525 | 0.5254761 | | verified |
| f | 3.669 mm | 3.6690797 mm | 3.6690797 mm (exact Glaser ray from ±2000a) | verified |
| f/a | 1.83 | 1.83454 | | verified |
| 1/M | 55.5 | 55.4728 | | verified |
| M | 0.0180 | 0.01802685 | 0.01802686 (rel. 3e-8) | verified |
| 50 nm × M | 0.90 nm | 0.9013 nm | | verified |
| θ_rot | 1.84 rad | 1.8438417 rad | 1.8438417 rad | verified |
| θ_rot in degrees | 106° | 105.644° | | verified |
| NI at 30 kV | 2150 A | 2147.800 A | | verified (B₀ = 0.430 T) |
| NI ratio | 6.211 | 6.2105227 | | verified |
| √(V*₃₀ₖ/V*₈₀₀) | 6.211 | 6.2105227 (V* = 800.62622 V, 30880.628 V from ch03 module) | | verified; equals the NI ratio to 1e-15, as the scaling says |
| C_s at 30 kV, default | 4.19 mm, 4.19 mm | 4.188928 mm both | | verified |
| θ_rot at 30 kV | 1.84 rad | 1.8438417 rad | | verified |
| C_c, solver (6 digits) | 2.84759 mm | 2.8475940 mm | 2.8475940 mm (FD) | verified |
| C_c integral | 2.84759 mm | 2.8475940 mm (derive JSON) | 2.8475940 mm (quad) | verified |
| C_s integral | 4.18897 mm | 4.1889678 mm (derive JSON) | 4.1889678 mm (quad) | verified |
| C_s traced (6 digits) | 4.18893 mm | 4.1889275 mm | 4.1889678 mm with ε ≤ 1e-9; Lorentz trace with the solver's ε 4.1889272 | wrong, because the subtraction ray's own third-order miss biases the fit by −4.0e-5 mm; the traced value of this field is 4.18897 mm (error 3) |
| "agreement to a few parts in a hundred thousand" | 1.0e-5 | ratio 0.999990 | 1 − 1e-7 after the fix | wrong, because the 1e-5 gap is the bias of error 3, not the accuracy of either method |
| f traced / Glaser (7 digits) | 3.669080, 3.669080 mm | 3.66907970, 3.66908018 mm | | verified; gap 1.3e-7 relative, fully explained by the finite start (exact Glaser ray from ±2000a: 3.66907969 mm). The page prints equal numbers and then speaks of "the small gap", which the reader cannot see; the N1 title's "about 1/2000²" (2.5e-7) is the right order. |
| α³ scaling "to 0.02 % between 1 and 8 mrad" (N5) | 0.02 % | spread 0.016 % | 0.013 % after the fix | verified (bound holds); the 1 mrad value is depressed by error 3 |
| C_s, C_c default | 4.19 mm, 2.85 mm | 4.188928, 2.847594 mm | | verified |
| C_sα³ at 5 mrad | 0.52 nm | 0.5236 nm | | verified |
| C_cα ΔE/E, 0.215 eV at 800 V | 3.8 nm | 3.826 nm | | verified; 0.215 eV is chapter 3's `ch03.cold_dE` (FWHM), typed in by hand in text/ch04.py rather than read from the store |
| WD 5 mm: C_s, C_c, f | 12.9, 4.65, 5.30 mm | 12.91189, 4.650323, 5.295327 mm | C_s 12.91194, C_c 4.650323 | verified |
| a 1 mm, WD 2 mm: C_s, C_c, NI | 3.79, 1.84 mm, 295 A | 3.787701, 1.844981 mm, 294.632 A | C_s 3.78780, C_c 1.844981 | verified |
| Check table N1–N5 values (from derive JSON) | as printed | reproduced by ref/ch04.py | | verified (N3 and N5 carry error 3) |
| Parity "about 10⁻¹¹" | 1e-11 | max 9.3e-12 (browser vs Python, 4 cases) | | verified |
| 6000 RK4 steps, 60 bisection steps | | NSTEP = 6000, 60 iterations in both files | | verified |
| Simulation readouts at defaults | 346 A, 3.67 mm, 4.19 mm, 2.85 mm, 0.0180, 106 deg | same | | verified |

## Numerical method: text against code, line by line

| Text says | Code (physics/ch04.js = ref/ch04.py) | Verdict |
|---|---|---|
| Object at u before the centre, wafer WD behind, paraxial ray from the axis at the object | `paraxial(B0,a,eta,-u,wd,0,1)` | verified |
| B₀ adjusted by bisection until the ray crosses the axis at the wafer | `focusB0`: 60 halvings of [0, √(3/η)/a] (ω = 2 at the top, so the first crossing), sign of r(WD) | verified |
| Variable t with z = a tan t, classical RK4, fixed number of steps | `grid`, `f` multiplies by dz/dt = a/cos²t; RK4, NSTEP = 6000 | verified |
| M from the slopes of the same ray at both ends | `M = 1/|r'(WD)|` with r'(−u) = 1 | verified |
| f: parallel ray started at a finite distance | ±2000a, r = 1, r′ = 0, f = −1/r′ | verified |
| θ_rot = √(e/8mV*)∫B dz along the path | closed form B₀a(atan(WD/a) + atan(u/a)), object to wafer | verified |
| Exact equation of motion, z as variable, constant speed, field (4.2) to third order in r | `ray3d`: B_z to r², B_r to r³, the z-form equation above, q/p = −e/p | verified |
| Rays launched at image angles 2 and 4 mrad | object slope α_i·M (paraxial conversion; slope vs angle differs at fifth order and goes into C₅) | verified |
| Miss at the paraxial image, linear part removed with a 10⁻⁷ rad ray | `hypot(x − k·x_e, y − k·y_e)` at WD, ε = 1e-7 is the **object** slope (image angle 5.5e-6 rad) | wrong, because the 1e-7 ray's own cubic miss is what is removed, not a linear part (error 3); also the text should say the 10⁻⁷ is the object-side slope |
| Solve Δr = C_sα³ + C₅α⁵ | closed-form two-point solution, checked | verified |
| C_c: paraxial ray at V*(1 ± 10⁻⁴), central difference | η/(1 ± 1e-4), |Δr|/(2δ)·M (M converts object slope to image angle) | verified |
| C_s, C_c referred to the image | yes (α at the wafer) | verified |

## Minor, outside the page text
- `LITERALS` in text/ch04.py labels "5 mm", "1 mm" and "5 mrad" as givens of "Example 4.2"; they belong to Example 4.3. Not visible to the reader.
