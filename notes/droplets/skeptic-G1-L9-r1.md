# Skeptic, Gate 1, L9 (then numbered L8), round 1 (blind)

Contract read: `notes/droplets/contract-L8.md`. Numbers: `portfolios-src/droplets/derive/L8_scales.cjs` (run with node), recomputed in my own
Python (`recompute.py`, `ks_box.py` in the session scratchpad). Fall speeds from `physics.cjs` vBeard at 10 °C and 850 hPa (ν = 1.6935 × 10⁻⁵ m²/s).
Nothing else in the repository was read except `physics.cjs` (air, vBeard, ayalaFactor).

## Verdict: FAIL (round 1)

The scale argument of section 2 is right, and its numbers check to three figures. The Saffman–Turner formula is right. But the tool
cannot answer the question as designed, for three reasons:

1. **The tool is known to fail in this range.** The one paper that compares kinematic simulation (KS) with DNS directly for
   collision rates (Voßkuhle et al. 2014, which I read in full) finds that the two agree only as St → 0. For St ≳ 0.3 the KS
   collision rate is more than ten times too low, and the clustering at larger St is too low by orders of magnitude. All our pairs
   have St from 0.1 to 1.7.
2. **A 1 cm box (12 η) leaves out most of the small-scale physics.** I built the contract's field and measured it. It holds 28 % of
   the velocity-gradient variance, and its fluid acceleration is 8 to 20 times too small. That removes the very term that makes Γ
   differ from 1. Test 4 will fail by a factor of about 5 in Γ − 1.
3. **The counting rule and the ghost approximation can each bias Γ by as much as the effect being measured.**

Both biases push Γ towards 1, which is the direction the section 7 prediction expects. So that prediction cannot fail for the right
reason.

A route to PASS exists (objections 1, 2, 7, 8, 11 and 12 below). It needs a validation step against DNS with gravity before any Γ is
believed, and a box of at least 60 η.

## Objections

| # | Severity | Claim quoted | Problem | Fix I would accept |
|---|---|---|---|---|
| 1 | **fatal** | §5: "it is known in the literature to misjudge clustering against DNS (scout to quantify)"; §3 "Air: a kinematic simulation (Fung et al. 1992)" | **What I read:** Voßkuhle, Pumir, Lévêque & Wilkinson (2014, J. Turbulence; arXiv:1402.5915), full text. They use the same KS form, the same ω = λ√(k³E), λ = 0.5 and ghost collisions, with no gravity. Their findings: KS and DNS rates agree only as St → 0. At St ≳ 0.3 the KS rate is lower by "more than one order of magnitude" (Fig. 1). Their g(2a) in KS is "too low by orders of magnitude at larger Stokes number" (Fig. 2). They conclude that "only DNS evaluations should be considered reliable". They blame the missing sweeping of small eddies, which makes caustics form more slowly. **Why it matters here:** our St values are 0.1–0.24 (20/18), 0.44–0.88 (40), and 0.64–1.7 (60/50), so every pair sits in their failure range. The failure is a bias towards Γ = 1, the same direction as the §7 prediction. **One mitigating point the contract should argue, not assume:** our drops settle fast (Sv = v_T/u_K = 9–17 for 50–60 µm). A drop crosses an η-eddy in η/v_T ≈ 2.4 ms, much shorter than τ_K = 41 ms, so the missing eddy motion may matter less than in their gravity-free runs. Nobody has tested this. | Put the KS/DNS gap in §2 and §5 as the main limitation, with the numbers above. Add a **validation test before any Γ is believed**: reproduce a published DNS kernel ratio *with gravity* at matching St, Sv and a/η, with a threshold written now (for example Γ − 1 within a factor 1.5). Candidates: (a) Wang, Ayala, Rosa & Grabowski 2008 (NJP 10, 075013), 18/20 µm. Their abstract gives total enhancement 2 and 7 and an efficiency part of 1.6 and 4 at 100 and 400 cm²/s³, so the geometric part is about **1.25 and 1.75**. That is exactly the Γ of this level for 20/18. (b) Ayala et al. 2008 Part 1 DNS kinematic kernels, 10–60 µm with gravity. Open both papers and quote the table values. Also write what happens if the validation fails: L8 then becomes the level that shows *why* a random-wave field misses inertial collisions, and the drizzle consequence takes Γ from DNS. |
| 2 | **fatal** | §3: "The flow is periodic in a cube of side L = 1 cm (12 η at ε = 10⁻²)"; §5: "the kernel needs only the small scales" | **The box cuts off the dissipation range.** "Small scales" for the gradient means wavelengths of about 8–60 η. The Pao dissipation spectrum peaks at kη = 0.19, a wavelength of 33 η, and the box (k_Lη = 0.52) cannot hold it. **Measured** in a lattice KS with the contract's spectrum, k up to 2/η, 3 realisations: ⟨(∂u/∂x)²⟩/(ε/15ν) = **0.28** at 10⁻² and 0.45 at 4 × 10⁻² (L = 1 cm). It is 0.68 at L = 3 cm and 0.85 at L = 5 cm. The rms fluid acceleration per component is **0.12 u_K/τ_K** at 1 cm and 0.70 at 5 cm. Real turbulence gives √a₀ u_K/τ_K = 1.5–2.6 u_K/τ_K (a₀ = 2.3 at Re_λ ≈ 100, 7 at the cloud value used by L6). The drops' different responses to fluid acceleration, |τ₁ − τ₂|·a, give a speed difference of **13 % of the gravitational Δv at 10⁻² and 37 % at 4 × 10⁻²**. Both figures equal a_rms/g, the same for every pair. In the 1 cm KS that term is down by a factor of 8–20. Putting the KS statistics into the L6 relative-velocity formula (erf form) gives Γ(40/8) = **1.008 at 10⁻² and 1.05 at 4 × 10⁻²**, against 1.046 and 1.25 with real acceleration. Test 4 therefore fails by a factor of about 5 in Γ − 1, before any code is written. The gradient check of §3 also fails (0.28). | L ≥ 60 η (5 cm at 10⁻², 3.5 cm at 4 × 10⁻²). Report the measured gradient variance *and* the measured acceleration variance against DNS values at the stated Re_λ. Rescale nothing silently. Redo the cost: about 1.4 × 10⁴ lattice modes at 5 cm, or an FFT grid with interpolation. Even at 5 cm the acceleration is 2–4 times too small, so the residual KS deficit must be priced on the page. |
| 3 | must-fix | §3: "frequencies ωₙ = λ √(k³E(k)) (unsteadiness parameter λ ≈ 0.5)" | With the dissipation-damped E(k), the *smallest* eddies live *longest*. Measured mode lifetimes 1/ω run from 4 τ_K (kη ≈ 0.5) to 16.5 τ_K (kη = 2). The small scales are nearly frozen, which reverses Kolmogorov's picture. λ is also a hidden O(1) knob: Voßkuhle et al. 2014 (Table 1, St = 1.5, L/η = 64) find the rate falls from 6.3 to 2.6 as λ goes from 0.01 to 2. | Use ωₙ = λ ε^{1/3} kₙ^{2/3} (the undamped K41 eddy rate). Scan λ ∈ {0.25, 0.5, 1, 2} and report the spread as model uncertainty on Γ. |
| 4 | must-fix | §3: "E(k) = 1.5 ε^{2/3} k^{−5/3} exp(−1.5 β (kη)^{4/3})"; §8 "the model spectrum (Pope 2000, chapter 6)" | This is Pao's (1965) spectrum, not Pope's model spectrum, whose cut-off is exp(−β{[(kη)⁴ + c_η⁴]^{1/4} − c_η}) with β = 5.2. If Pope's β = 5.2 went into the contract's formula, the exponent would be 7.8 (kη)^{4/3} and the spectrum would no longer give ε. With C = β = 1.5 (exponent 2.25 (kη)^{4/3}), Pao's form satisfies 2ν∫k²E dk = ε exactly (checked analytically: ∫x^{1/3}e^{−2.25x^{4/3}}dx = 1/3). | Name Pao, fix β = 1.5 in words, and print the normalisation check. |
| 5 | must-fix | §3: "periodic in a cube of side L" | A Fung-type KS (random or log-spaced kₙ) is not periodic. When a drop wraps across the boundary it enters a different field, and pairs that straddle the boundary see a spurious velocity jump. | Put kₙ on the lattice 2πn/L (125 independent modes at 1 cm and 1.4 × 10⁴ at 5 cm, counted) and use minimum-image pair distances. Or say how the drops are wrapped. |
| 6 | must-fix | §5: "recirculation in the periodic box repeats the field every L/v_T = 0.06 s" | That figure uses the 40 µm speed. For 60 µm, L/v_T = **29 ms**, and for 50 µm 39 ms. The lowest mode lives 166 ms (λ = 0.5), so a 60 µm drop crosses a nearly frozen pattern about 6 times. The pair falls along nearly the same line, so both drops see the same repeated forcing. | Tilt gravity along a direction irrational to the lattice, enlarge the box (objection 2), and pre-state the doubling-L tolerance (for example a change of no more than 1σ). |
| 7 | must-fix | §3: "A contact is counted when the closest approach of two drops within a step ... is below R + r" | As written, this counts every step a ghost pair spends overlapped. For 20/18 at 10⁻² the overlap lasts 2(R + r)/Δv = 8.4 ms = 4 steps (8 steps at 4 × 10⁻²), so contacts are overcounted 4 to 8 times. | Count only inward crossings: separation ≥ R + r at the start of the step and the straight-line minimum < R + r, with the minimum image. Test 1 should be written so that it would catch this bug. |
| 8 | must-fix | §3: "ghost collisions (drops pass through each other, so concentrations stay steady)"; §5: "overcounts contacts" | Voßkuhle, Lévêque, Wilkinson & Pumir 2013 (PRE 88, 063008). I read the abstract and quoted passages via ar5iv, not the full figures. The ghost approximation overestimates the rate of *first* contacts by about 15 % as St → 0, falling as St grows. That is the same size as the effect Γ is meant to detect (the §7 threshold is 1.2). Still-air gravity has no re-contacts, so the bias sits only in the numerator of Γ. | Keep a per-pair contact history and report Γ_ghost and Γ_first, where a repeat contact of the same pair is not counted. Use Γ_first for coalescence and the drizzle runs. |
| 9 | must-fix | §6.2: "Saffman–Turner kernel √(8π/15)(R + r)³/τ_K within 10 %" | **The formula is right.** K = 2πa²⟨\|w_r\|⟩, w_r Gaussian with σ_r = a√(ε/15ν), and ⟨\|w_r\|⟩ = √(2/π)σ_r give √(8π/15)a³/τ_K = 1.294 a³(ε/ν)^{1/2} (re-derived). Voßkuhle et al. 2014 (eq. 5) give the same and call it exact as St → 0 for ghost counting. But KS gradients are Gaussian (measured skewness of ∂u/∂x from +0.02 to +0.16, about 0), so in KS the formula is exact once the *measured* gradient variance is used. 10 % is too loose a tolerance. Comparing with ε/(15ν) fails by objection 2. In real turbulence the gradient is skewed (about −0.5), so the formula is approximate there; that is literature knowledge I have not measured here. | Compare with √(8π/15)a³·√(15⟨(∂u/∂x)²⟩_meas) within 2σ (statistical), with g = 0 and τ → 0. Ghost drops let N rise freely: the Saffman–Turner rate in 1 cm³ at 10⁹ m⁻³ is 42/s for 60/50 and 1.7/s for 20/18, so raise N. |
| 10 | must-fix | §1 and §6.4: "Ayala's formula applies: Γ = 1.056 at ε = 10⁻² m²/s³, 1.281 at 4 × 10⁻²" | `physics.cjs` ayalaFactor uses the interpolation √(2/π)√(σ² + (π/8)Δv²) with g₁₂ = 1. Ayala's Gaussian (erf) form with the same σ gives **1.046 and 1.250**, so Γ − 1 is 20 % and 12 % smaller. Ayala's full kernel also has g₁₂. The precision is also too low: with Γ − 1 ≈ 0.05, "standard errors of a few per cent" do not resolve test 4 at 10⁻². | Call it "the L6 interpolation of Ayala's relative velocity, g₁₂ = 1" and give both values. Require SE(Γ) ≤ 1 % from the spread over realisations, not Poisson. |
| 11 | must-fix | §7: "Γ < 1.2: the shear difference at contact (2.7 mm/s) is 3 % ... If Γ ≥ 1.5 ..." | (a) The range 1.2 ≤ Γ < 1.5 is left undefined. (b) The argument uses only shear. It leaves out the acceleration term (13 % of Δv, so Γ − 1 ≈ (σ/Δv)² ≈ 0.02 in the large-Δv limit). It also leaves out the gravity–shear term, which makes L6's own formula, extended to 60/50, give **Γ = 1.35** (1.31 in erf form). The contract must say why that extension is wrong: v_Tτ_p = 12 mm and 7 mm, much longer than η, so the linear-shear basis fails. (c) The real reason clustering is weak is never given. The species separate by Δv τ_K/η = **4.4 η** per Kolmogorov time, so their clusters decorrelate. (d) The settling parameter Sv = v_T/u_K (17 and 13) is never computed, though it decides the gravity regime. (e) Because of objections 1 and 2, the instrument is biased towards the prediction. | Write the prediction as a number with a two-sided band, argued from all three terms and Sv. My estimate: Γ(60/50, 10⁻²) ≈ 1.02, band 0.95–1.10. Say what is done in each range. Make the prediction against the *validated* instrument (objection 1). Give at least the sign of Γ − 1 at 4 × 10⁻², or explain why not. |
| 12 | must-fix | §1: "the measured Γ for near-equal collector pairs, put into the exact stochastic runs of L5, gives the turbulent first-drizzle time ... the number chapter 7 says is missing" | Three pairs do not make a kernel K(R, r). The level also leaves out turbulent collision efficiency, which for 18/20 µm is the *larger* factor (1.6 and 4 against a geometric 1.25 and 1.75, from the Wang 2008 abstract). The "missing number" would still lack its largest part. | State how Γ is spread over (R, r), or limit the claim to a sensitivity run (Γ applied to pairs r/R > 0.6). Carry still-air efficiency with its price, and give Wang's efficiency factor as an upper bracket. |
| 13 | minor | §3: "Linear drag is used up to St ≈ 2 (drop Reynolds number below 2 here)"; §5: "drop Re ≤ 1.5 for r ≤ 60 µm" | Re(60 µm) = **2.46** and Re(50 µm) = 1.53. "St ≈ 2" is not a drag criterion. At Re 2.5 the linearised drag along the fall gives a response time about 13 % shorter than v_T/g* (my Schiller–Naumann estimate). Sideways it is exact to first order. | Correct the numbers. State that the response is anisotropic, or use nonlinear drag, which costs little. |
| 14 | must-fix | §3: "with u frozen during the step (Δt = τ_K/20)" | A 60 µm drop falls **0.86 η per step** at 10⁻² (0.61 η at 4 × 10⁻²). The field it sees changes on η/v_T = 2.4 ms ≈ Δt. A frozen-u exponential step is first order in that. | Δt ≤ min(τ_K/20, 0.1 η/v_T,max), or u at the predicted midpoint (second order). Halve Δt and report the observed order (method 4.8). |
| 15 | minor | §2: "0.03 to 0.19 Kolmogorov lengths"; "0.3 to 5 mm/s"; "0.1 % to 8 %" | These ranges include ε = 10⁻³, which the script prints but the study does not use. At 10⁻² and 4 × 10⁻²: a/η 0.046–0.19, a/τ_K 0.92–5.35 mm/s, Saffman–Turner/gravity 0.28 %–8.4 %. | Use the study's ε range, or say why 10⁻³ is shown. |
| 16 | must-fix | §3: "ten independent flow realisations per case: standard errors of a few per cent" | 20/18 gives only 41 still-air contacts/s in 1 cm³. Ghost contacts are correlated (objection 8), so Poisson errors are too small. | Errors from the realisation spread. Raise N, because ghost drops allow it and contacts grow as N². Print the target SE per pair. |
| 17 | minor | §6.3: "mean fall speed ... reported" | There is no threshold. | Report ⟨v_z⟩ − v_T with SE. Any change above 2 % of v_T is explained and compared with the DNS settling enhancement at the same St and Sv. |
| 18 | minor | §4 rejected alternatives | The cheapest honest alternative is missing: take Γ from published DNS (Ayala 2008 Part 1 tables, Wang 2008, Rosa et al. 2013) and spend the level on showing *why* it differs from 1. | List it and say why it is rejected or adopted. |
| 19 | minor | whole contract | There is no opening Fermi estimate for 40/8 or 20/18 (method 4.1). | 40/8: 1.05 and 1.25 (erf form). 20/18: about 1.25 and 1.75 (DNS, geometric part, if the full Wang paper confirms the abstract). |
| 20 | minor | readability | ε needs an everyday scale. St, Sv and "ghost collision" each need a picture, and so do "sling/caustics" (a drop thrown out of a spinning eddy overtaking a neighbour). Sv does not appear at all. | Add one sentence and one picture for each, in that order. |

## Recomputed numbers (own Python; vBeard from physics.cjs)

Air: ρ = 1.0458 kg/m³, μ = 1.7711 × 10⁻⁵ Pa s, ν = 1.6935 × 10⁻⁵ m²/s, g* = g(1 − ρ_a/ρ_w).
Beard speeds (m/s): 8 µm 0.00796, 18 µm 0.0395, 20 µm 0.0485, 40 µm 0.1771, 50 µm 0.2592, 60 µm 0.3478.

| ε (m²/s³) | η (mm) | τ_K (ms) | u_K (mm/s) | L/η at 1 cm |
|---|---|---|---|---|
| 10⁻² | 0.835 | 41.15 | 20.29 | 12.0 |
| 4 × 10⁻² | 0.590 | 20.58 | 28.69 | 16.9 |

| pair, ε | a/η | Δv_g (mm/s) | a/τ_K (mm/s) | St | Sv | K_g (m³/s) | K_ST (m³/s) | K_ST/K_g | L6 interp Γ | erf-form Γ | Re |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40/8, 10⁻² | 0.057 | 169.1 | 1.17 | 0.439/0.020 | 8.7/0.4 | 1.224e-9 | 3.48e-12 | 0.0028 | 1.056 | 1.046 | 0.84/0.01 |
| 60/50, 10⁻² | 0.132 | 88.6 | 2.67 | 0.863/0.643 | 17.1/12.8 | 3.369e-9 | 4.19e-11 | 0.0124 | (1.346 if not cut) | (1.312) | 2.46/1.53 |
| 20/18, 10⁻² | 0.046 | 9.0 | 0.92 | 0.120/0.098 | 2.4/1.9 | 4.09e-11 | 1.73e-12 | 0.0422 | (1.031) | (1.025) | 0.11/0.08 |
| 40/8, 4×10⁻² | 0.081 | 169.1 | 2.33 | 0.878/0.039 | 6.2/0.3 | 1.224e-9 | 6.96e-12 | 0.0057 | 1.281 | 1.250 | — |
| 60/50, 4×10⁻² | 0.186 | 88.6 | 5.35 | 1.725/1.286 | 12.1/9.0 | 3.369e-9 | 8.37e-11 | 0.0249 | (2.10) | (2.07) | — |
| 20/18, 4×10⁻² | 0.064 | 9.0 | 1.85 | 0.240/0.196 | 1.7/1.4 | 4.09e-11 | 3.45e-12 | 0.0843 | (1.195) | (1.168) | — |

All agree with `L8_scales.cjs` to the printed digits. Values in brackets are outside the formula's range, shown only to support
objection 11.

Further numbers:
- **Differential acceleration** |τ₁ − τ₂|√a₀ u_K/τ_K as a fraction of Δv_g = √a₀ (u_K/τ_K)/g. It is 0.13 at 10⁻² and 0.37 at 4 × 10⁻² (a₀ = 7), the same for every pair.
- **Measured KS box** (lattice modes, Pao spectrum, k ≤ 2/η, λ = 0.5, 3 realisations):

  | ε, L | independent modes | gradient variance / (ε/15ν) | acceleration rms per component (u_K/τ_K) |
  |---|---|---|---|
  | 10⁻², 1 cm | 125 | 0.28 | 0.12 |
  | 4 × 10⁻², 1 cm | 345 | 0.45 | 0.27 |
  | 10⁻², 3 cm | 3 117 | 0.68 | 0.45 |
  | 10⁻², 5 cm | 14 495 | 0.85 | 0.70 |

  Mode lifetimes are 4–17 τ_K.
- **Still-air contact rates** in 1 cm³ at 10⁹ m⁻³ each: 1224/s (40/8), 3369/s (60/50), 41/s (20/18).
- **Recurrence** L/v_T at L = 1 cm: 29 ms (60 µm), 56 ms (40 µm), 206 ms (20 µm). The lowest mode's lifetime is 166 ms.
- **Δv τ_K/η** (how far the two species separate in one τ_K, in units of η): 8.3 (40/8), 4.4 (60/50) and 0.4 (20/18) at 10⁻².

## The six thresholds (section 7.3, applied to the contract)

| Threshold | Result | Why |
|---|---|---|
| Motivated | FAIL | The picture and the shear mechanism are good. The mechanisms that decide the answer (differential acceleration, clustering against Sv, slings) carry no number (objections 2, 11). |
| Honest | FAIL | The KS/DNS gap is understated (1). The ghost bias is not priced (8). The drizzle consequence leaves out the efficiency factor (12). The Re claim is wrong (13). |
| Derived | PASS with fixes | Every section 2 number and the Saffman–Turner formula check by two routes. The "Ayala" value is an interpolation with g₁₂ = 1 (10). |
| Checked | PASS with fixes | The script reproduces. The ranges mix in ε = 10⁻³ (15). The 0.06 s recurrence is for the wrong drop (6). |
| Sourced | FAIL | The spectrum is wrongly attributed (4). The KS–DNS literature that decides the method was not consulted (1). The Wang 2008 numbers come from an abstract and should be read in full. |
| Readable | PASS with minor fixes | A strong second-year student follows section 2. Sv, ε and ghost collisions need pictures (20). |

## Sources: what I read and what I only saw in an abstract

- **Read in full** (arXiv preprint text): Voßkuhle, Pumir, Lévêque, Wilkinson, "Collision rate for suspensions at large Stokes numbers – comparing Navier-Stokes and synthetic turbulence", J. Turbulence 2014, arXiv:1402.5915.
- **Abstract and quoted passages only** (ar5iv; figures not seen): Voßkuhle, Lévêque, Wilkinson, Pumir, "Multiple collisions in turbulent flows", PRE 88, 063008 (2013), arXiv:1310.1521.
- **Abstract only:**
  - Wang, Ayala, Rosa, Grabowski, NJP 10, 075013 (2008): the factors 2 and 7 total, 1.6 and 4 efficiency, for 18/20 µm.
  - Rosa et al., NJP 15, 045032 (2013): gravity changes collision statistics above about 20–30 µm; Re_λ dependence saturates.
  - Thomson & Devenish, JFM 526 (2005): KS lacks sweeping, wrong pair dispersion.
  - Chen, Goto & Vassilicos, JFM 553 (2006): KS clustering arises through a different mechanism.
  - Voßkuhle et al., JFM 2014, arXiv:1307.6853: the sling effect dominates at significant inertia.
- **Not opened, cited from knowledge** (should be opened before use): Fung et al. 1992; Pao 1965; Pope 2000 chapter 6 (the 8–60 η dissipation range); Ayala et al. 2008 Parts 1 and 2; Wang & Maxey 1993.
