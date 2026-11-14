# Fig. 12 note, round 2: derivation and number check

Checked on 14 November 2026: the lecture note `<article id="paper">` of `public/simulations/guinness-kaggle.html` (as built from
`notes/fig12/note/paper.html` by `build_note.py`). The checker did not write the note and did not read `notes/fig12/readers/`.

**How it was checked**

- **Equations.** Each one was re-derived in SymPy 1.14: the symbolic identity, or the solution put back into its equation. Bessel
  integrals and energy integrals were checked by quadrature. Units and limiting cases were checked by hand.
- **Numbers.** Every number was recomputed in my own scripts, without running or importing `note_numbers.py`:
  - **Theory:** from the glass table `public/scripts/guinness-glass.js` and the constants of `tools/fig12/kaggle/stout_jax.py`.
  - **Stored rides:** my own decoder for the stored files in `public/data/fig12/2026-11-14-run10/` (int16 differences, running sum
    mod 2^16), my own ring reader and my own bounded least-squares refits.
  - **Cart alone:** my own driver around `stout_jax.Cart` on the CPU (sub-steps of 0.1 ms, frozen pint of 454.41 g).
  - **Controllers:** my own Riccati solver (Hamiltonian stable subspace), my own Kalman cycle, my own construction of (50)-(52), my
    own quadrature for A_d, B_d and Q_d, and a Floquet search with `solve_ivp` and Brent's method.
  - **Run records:** the impulse, rest and timing numbers come from the run summaries `notes/fig12/jax/run8-check/run8-summary.json`
    and `run10-check/run10-summary.json`.
- **In headless Chromium:**
  - The page was served locally and loaded with Playwright and Chrome. All 10 files pass the SHA-256 check in the browser, and the
    page reports no errors.
  - The page's ride table matches Table 8 to its one-decimal rounding.
  - The readings at stored picture 22 of the kerb ride equal the stored values: 1.31 m/s, 429.583 g, 90.06 mL, 1.26 mL, 200
    drops and lumps, 2.73 A.
- **Port check.** It was re-run from a copy in the scratchpad: the same 2.30e-13 / 4.18e-13 / 6.34e-8 / 6.39e-8 A as the stored
  record. No repository file changed (`git status` is clean).
- **Method text.** Sections 5, 6, 8, 9, 10 and 12 were read against `stout_jax.py`, `run_b.py`, `pack_ride.py`,
  `guinness-jax-play.js` and `stout-view2.js`.

Verdicts: **verified**, **wrong, because …** (with the correct value), **unverifiable, because …**. A "remark" after "verified"
records a small point that does not change the result.

---

## A. Numbered equations

| # | Equation | Verdict |
|---|---|---|
| (1) | δm ẍ = F − δm a_g | verified (SymPy: Newton in the road frame, X_g'' moved to the right). |
| (2) | Navier–Stokes in the glass's frame | verified. Each term is in m/s². The viscous term follows: μ∇²u + ⅓μ∇(∇·u) loses its second part because ∇·(∇×A) = 0 for any divergence-free field. The hydrostatic, steady-push and rigid-load limits of 3.4 all follow (SymPy). |
| (3) | ∇·u = 0 | verified. |
| (4) | Kinematic surface condition | verified: it is D(z − h − η)/Dt = 0 written out. |
| (5) | p = p_s at the surface | verified as the model's condition. Remark: surface tension is left out. For the bare stout it would multiply ω₁₁² by 1 + γk²/(ρg) = 1.0099, which is +0.5 % in frequency (3.438 Hz instead of 3.421 Hz). Section 13 does not list this. |
| (6) | Unsteady Bernoulli | verified. SymPy: u_t − (−∇(p/ρ) + g_eff) is the gradient of the bracket. |
| (7) | φ = cos ωt cos θ J₁(kr) cosh kz | verified: it satisfies Laplace's equation in cylindrical coordinates, and ∂φ/∂z = 0 on the floor. |
| (8) | J₁′(kR) = 0, ξ = 1.8412 | verified: ξ = 1.841184 (scipy `jnp_zeros`). |
| (9) | φ_tt + gφ_z = 0 at z = h | verified (from η_t = φ_z and φ_t + gη = 0). |
| (10) | ω₁₁² = gk tanh kh | verified (SymPy, by putting (7) into (9)). Units: s⁻². Limits: deep water gives gk; shallow water, tanh kh → kh, gives gk²h. |
| (11) | q̈ + ω₁₁²(1 + a_z/g)q = −βa, β = 2ξ tanh(ξh/R)/(ξ² − 1) | verified. SymPy, from the two projected surface conditions. c₁ = 2R/((ξ² − 1)J₁(ξ)) checked by quadrature (0.0562334 both ways). J₂(ξ) = J₁(ξ)/ξ holds. Steady limit: q = −0.837 Ra/g. |
| (12) | q_max = β\|Δv\|/ω₁₁ | verified: q = −(βΔv/ω)sin ωt solves the equation with q̇(0) = −βΔv. |
| (13) | q_max = (β/ω₁₁)\|∫a e^{jω₁₁t′}dt′\| | verified (Duhamel). Problem 7's integral jπa_p/(2ω) holds exactly (SymPy). |
| (14) | Damped oscillator | verified: q₀e^{−ζωt}cos(ω_d t + ψ) solves it. |
| (15) | Stokes layer | verified: it solves u′_t = νu′_dd with δ_s = √(2ν/ω) and takes the right value at the wall. |
| (16) | τ_w = ρ√(νω/2)U(cos ωt − sin ωt) | verified (SymPy). Problem 1: the in-phase part averages to ½ρ√(νω/2)U²; the quadrature part does no work. The heat in the layer, μU²/(2δ_s), is the same. |
| (17) | σ_wall = √(νω/2)(ξ² + 1)/(2R(ξ² − 1)) | verified. The exact integrals for the deep glass give σ = 0.11011 s⁻¹, against 0.11012 s⁻¹ from the formula. The ζ form equals δ_s/(4R)·(ξ² + 1)/(ξ² − 1) (SymPy). Units: s⁻¹. |
| (18) | σ_skin = √(νω/2)(k/2)coth kh | verified: ∫\|∇_hφ\|²dA = k²∫φ²dA (ratio 1.0000000000 by quadrature), and the energy balance reproduces the formula. |
| (19) | p_L, G₀, τ_y laws | Algebra and units (Pa) verified. The laws themselves are unverifiable, because they are quoted from Völp & Willenbacher [5], which was not re-read here. |
| (20) | Tcholakova viscous stress | Units verified: Ca_f is dimensionless and the result is in units of γ/R₃₂. Matches `foam_flow_stress` term by term. The law is unverifiable, because it is quoted from [11]. |
| (21) | Cantat wall stress | Units verified; matches `head_wall_stress` (slide branch). The law and Z, l/r_m are unverifiable, because they are quoted from [12]. |
| (22) | h_eff = (3/(5k))(1 − e^{−5kh_f/3}) | verified (SymPy). Limit h_f → ∞ gives 3/(5k) (Problem 4). Matches `Stout.heff`. |
| (23) | ρ_f(½\|g′\|z₊ + a_out z₊) ≥ τ_y | verified: the dam force ∫ρ_f g′z dz = ½ρ_f g′z₊². Matches `head_spill`, which uses \|g_z\| and max(a_out, 0). |
| (24) | p_s = m_s(g′ + dw/dt) | verified. Matches the Robin load in `pressure` with g′ clipped at 0. |
| (25) | ω² = gk tanh kh/(1 + λ_h k tanh kh) | verified. SymPy: the travelling-wave substitution gives both conditions, and the determinant gives (25). The limit λ_h → 0 gives (10). |
| (26) | (1 + λ_h k tanh kh)q̈ + ω₁₁²(1 + a_z/g)q = −βa | verified (SymPy, projection with the head's inertia term). |
| (27) | Head sheet, implicit | verified as the equation the code solves. `head_sheet`: diag = ρ2Δx + Δt(Σc + κ), coupling c = h_f μ_f/Δx², κ = a_c h_eff τ_edge/max(\|w\|, 1 mm/s). Units: Pa on both sides. See M8 for where the force is applied. |
| (28) | M_x v̇ = bi − c_x v + F_d, M_x = 2.529 kg | verified. 1.5 + 0.45441 + 0.3 + 0.150 + 0.125 = 2.5294 kg. Matches `Cart.forces` and `massX`. |
| (29) | τ_i di/dt = i_reach − i | verified. The code integrates it exactly over each sub-step, with clipping to ±I_max and then to (±V_max − E)/R_a. |
| (30) | −F_gs = m(g − a_g) − dP/dt | verified (momentum balance). Problem 6's telescoping holds, and the code books F_n = −(P_n − P_{n−1})/Δt_n. |
| (31) | APIC transfers | verified against `p2g` and `g2p`. The linear-field reproduction argument is correct. |
| (32) | Ghost pressure p_g = p_l(1 − 1/α) + p_s/α, α ≥ 0.05 | verified (SymPy). The code clips α to [0.05, 1]. |
| (33) | α → α + m_s/(ρΔx), p_s → m_s(g′ + (w* − w_h)/Δt) | verified. SymPy: the unnumbered intermediate equation and the substitution rule give the same w′. |
| (34) | Level set χ = \|x − x̄\| − r₀ with b_i = (1 − d²/(2Δx)²)³ | verified against `level_set`. Remark: χ is evaluated only in a band of cells near the surface; elsewhere the code sets ±2Δx. |
| (35) | E_p(0) − E_p(t) = E_k + D | verified as the energy statement for a still glass. It cannot be closed from the stored files, as the note itself says (D was not kept). |
| (36) | Damped Mathieu equation; growth when ε > 4ζ at Ω = 2ω | verified. SymPy averaging gives the matrix [[−ζω, −εω/4], [−εω/4, −ζω]], with eigenvalues ±εω/4 − ζω (Problem 9). Numerically, the Floquet threshold for the bare stout at Ω = 2ω is ε = 0.0222 = 4ζ. |
| (37) | PI speed loop | verified against `Cart.sample` (ctrl 1). |
| (38) | M_x δv̈ + (c_x + bK_p)δv̇ + bK_iδv = 0 | verified (SymPy). With c_x = 0, K_p = M_xω_c/b and K_i = K_pω_c/4 it gives a double root at −ω_c/2. |
| (39) | i_cmd = i_PI + N₀z_a′(x + vτ_i)/b | verified against `sample` (ctrl 2). SymPy: 1/(1 + jωτ) and e^{−jωτ} agree to first order. |
| (40) | F_a = −c_sky v_b | verified (`susp` branch). |
| (41) | A, B of the slosh model | verified, entry by entry, against `slosh_lqr`. |
| (42) | LQR cost with Bryson weights | verified (Q = diag(1/0.05², 1/0.002², 1/(0.002ω)², 1/0.02²), r = 1/9). |
| (43) | K = BᵀX/r_u and the Riccati equation | verified. My Hamiltonian solution has residual 3e-15. The step from the HJB argument to δi = −BᵀXx/r is correct. K₄ = I_max/x_e,m = 150 exactly. |
| (44) | Filter model A_z, B_z, G | verified against `observer_design`. |
| (45) | A_d, B_d, Q_d | verified: direct quadrature agrees with the code's block exponentials to 2e-12 (B_d) and 8e-12 (Q_d). |
| (46) | Van Loan block exponential | verified: the Γ equation and Q_d = A_dΓ(T_s) hold, as derived and numerically. |
| (47) | Predict | verified against `Cart.observe`, which predicts with the current measured at the previous sample (`uPrev`). |
| (48) | Correct, Joseph form | verified against `Cart.observe`. Remark: the note's "probe at every second sample" is the 2 ms case. The shortened last step before each picture (1.33 ms) breaks the two-sample cycle once per picture. |
| (49) | i_par = −(M_xω²/(β_h b))(a_z/g)q̂ | verified (SymPy) and against the code (`ipar`). Units: A. |
| (50) | Quarter-car equations | verified, row by row, against `susp_lqr`'s A_s and B_s. |
| (51) | Cost J_s | verified: Q, cross term Y and R as in `susp_lqr`. |
| (52) | Completed-square LQR | verified. My shifted-LQR solution reproduces the stored K_s, and the residual of (52) is 5e-15. |

## B. Unnumbered equations

| Id | Equation | Verdict |
|---|---|---|
| U1 | R = 39.1 mm | verified: R(125 mm) = 39.100 mm from `guinness-glass.js`. |
| U2 | ν = μ/ρ = 2.05e-6 m²/s | verified: 2.0457e-6. "About twice water": 2.05 against about 1.0e-6. |
| U3 | R₃₂ = ½d̄e^{2s²} = 34.2 µm | verified: the moment algebra holds (ratio e^{2s²} = 1.1221), giving 34.22 µm. |
| U4 | g_eff = (−a, 0, −(g + a_z)) | verified. |
| U5 | Material derivative | verified (definition). |
| U6 | Separated Laplace equation and Bessel equation of order 1 | verified (it follows from (7)). |
| U7 | c₁ = 2R/((ξ² − 1)J₁(ξ)), and c₁J₁(ξ) = 0.837R | verified: quadrature and closed form agree; 2/(ξ² − 1) = 0.8368. |
| U8 | Projected conditions q̇/J₁ = k tanh kh Υ, … | verified (they give (11), SymPy). |
| U9 | Surface condition with drive (4.2) | verified. |
| U10 | σ = Π/(2E_s), ζ = Π/(2E_sω) | verified (energy ∝ amplitude²). |
| U11 | E_s for mode (7) | verified: the closed form equals the quadrature (437.299 both, per unit ρB²). |
| U12 | Wall integral of u_θ² + u_z² | verified: the angular integrals each give π, with dS = R dθ dz; the deep-glass z-integral is e^{2kh}(1/R² + k²)/(8k). |
| U13 | ζ_wall = 0.5575ν^½R^{−¾}g^{−¼}, K_Λ = 3.50 | verified (SymPy scaling; coefficient 0.55751, K_Λ = 3.5029). |
| U14 | Gradient in the Stokes layer, ⟨(∂u/∂d)²⟩ = U²/δ²·e^{−2d/δ} | verified (SymPy). |
| U15 | E_s = ¼πρgR²(1 − 1/ξ²)q² | verified (quadrature 8.3625 = formula, per q²). |
| U16 | ζ_edge = Π/(2E_sω) ∝ q^{−1/3} | verified (Π ∝ q^{5/3}, E ∝ q²). |
| U17 | κ = τ_edge h_eff/\|w\| × length/area | verified against `head_sheet` (a_c is wall area per cell volume, which equals perimeter/column area). |
| U18 | Finite-time stop, v̇ ∝ −v^{2/3} | verified: d(v^{1/3})/dt is constant. |
| U19 | Wedge: z₊ = 4τ_y/(ρ_f g sin 2ϑ) | verified (SymPy). It is lowest at 45°, giving 8.1 mm. |
| U20 | q = h_fτ_yk/(ρg) = 0.5 mm | verified: 0.490 mm, so the lean is 2q = 0.98 mm, "about 1.0 mm". |
| U21 | Intermediate pressure-step equation before (33) | verified (SymPy). |
| U22 | q_peak = (β_h\|Δv\|/ω)e^{−ζωt_p}, ω_d t_p = arctan(√(1 − ζ²)/ζ) | verified (SymPy). The limit ζ → 0 gives (12). |
| U23 | y_q = ½(η_front − η_back) | verified against `Stout.probes` (front and back read at R − 2.5Δx and R − 4Δx, extended straight to the wall). |
| U24 | Kalman scalar blend L = C⁻/(C⁻ + V_y), variance (1 − L)C⁻ | verified (SymPy). |
| U25 | Heave form of the swing in 12.8 | verified (it is (26) with damping). |

## C. Numbers

### Abstract, sections 1–2

| Number(s) | Verdict |
|---|---|
| "about a million" parcels; 30 pictures a second | verified (1,001,952 particles, fps 30). |
| Abstract and conclusions: 3.421 Hz; 2.915 Hz; "about a millimetre"; 13.9 mm; 30 mm kerb at 1.5 m/s; 82 N; 11.25 N; foam over the rim under every controller; no stout spilled | verified (see the rows below). spill_g = 0 in every frame of every file. |
| Glass 149 × 76 mm drawing, scaled to 160 × 85 mm | The scaling is verified in `tools/fig12/glass_profile.py` (sz = 160/149.2, sr = 85/(2 r_o,max)). The drawing's own figures are unverifiable, because the dimensions.com source was not re-read. |
| Base 12.5 mm; floor radius 16.3 mm; 28.4 mm at 5 mm; widest 39.3 mm at 116 mm; rim 147.5 mm; fill 125 mm; R = 39.1 mm; change 0.29 mm over the top 20 mm | verified (12.50; 16.31; 28.43; 39.299 at 116.0; 147.5; 39.100; 0.287). |
| Stout 426.6 mL; head 19 mm; head top 144 mm, 3.5 mm below the rim; stout 22.5 mm below the rim | verified (426.597 mL by quadrature). |
| ρ = 1007, μ = 2.06 mPa s at 6 °C; Watamura 1006, 2.03–2.23; settling 120 s; 18–20 mm spec; 17.5/20.6/22.2 mm; d̄ = 61 µm, s = 0.24; γ = 44.2 and E_∞ = 18.7 mN/m | unverifiable, because these are quoted from sources [2]–[5], which were not re-read. They are the values used in the code. |
| Drainage estimate 0.36 / 0.235, 25–110 min | unverifiable, because they come from the project's research note (not checked here). |
| ν = 2.05e-6; e^{2s²} = 1.122; R₃₂ = 34.2 → 34 µm; ρ_f = 272 kg/m³ | verified (271.89). |
| Example 2.1: m_s = 5.17 kg/m²; m_s g = 50.7 Pa; 5.1 mm; λ_h = 5.13 mm; disc 91.26 mL; grid head 91.314 mL (+0.06 %), 24.8 g; 429.6 g; 454.4 g | verified (5.166; 50.68; 91.255 mL; stored head_ml0 = 91.314; 91.314/91.255 − 1 = 0.064 %; 24.83 g; 429.583 g from the books; 454.41 g). |

### Sections 3–4

| Number(s) | Verdict |
|---|---|
| Ex. 3.1: a = 0.88 m/s² for 3.5 mm; 5.65 m/s² for 22.5 mm | verified (0.878; 5.645). |
| ξh/R = 5.886; tanh = 0.99998; ω₁₁² = 461.9 s⁻²; ω₁₁ = 21.49 rad/s; f₁₁ = 3.421 Hz; 0.292 s | verified (5.8861; 0.999985; 461.94; 21.4927; 3.4207; 0.2923). |
| k = 47.1 m⁻¹; 1/k = 21.2 mm | verified (47.089; 21.236). |
| Next modes kR = 5.331, 8.536 → 5.82, 7.37 Hz | verified (5.3314, 8.5363; 5.821, 7.365). |
| β = 1.541; 0.837R; the one-mode answer 16 % smaller | verified (1.5407; 0.8368; 16.3 %). |
| Δv = −0.1 m/s → 7.2 mm | verified (7.17). |
| Push T_p = 0.146 s, half period; 5.2 mm at the wall, 5.0 mm on the ring; Problem 7: 5.2 mm | verified (half period 0.1462 s; (13) gives 5.236 mm, Problem 7's closed form 5.239 mm; on the ring at 31.16 mm, 4.98 mm). |

### Sections 5–6

| Number(s) | Verdict |
|---|---|
| ζ = 0.0055 → "about 3 % per swing" | verified (3.4 %). |
| ω = 21.49; δ_s = 0.436 (0.44) mm; √(νω/2) = 4.69 mm/s; 0.047 Pa | verified (21.488; 0.4363; 4.688; 0.0472). |
| e^{−2} ≈ 14 % at 2δ_s, 5 % at 3δ_s | verified (13.5 %, 5.0 %). |
| σ_wall = 0.110 s⁻¹, ζ_wall = 0.0051; factor 0.918/R | verified (0.11012; 0.00512; 0.9184). |
| K_Λ = 3.50 against 3.52; 5.23 is 49 % more; ζ = 0.0077 with 5.23 | 3.50 and 49 % verified (3.503; 48.6 %); 0.0077 verified (0.00765). The 3.52 and 5.23 themselves are unverifiable, because they are quoted from [9]. |
| σ_skin = 0.110 s⁻¹, ζ_skin = 0.0051; bulk 2νk² = 0.0091 s⁻¹, ζ = 0.0004 | verified (0.11038; 0.00514; 0.00907; 0.00042). |
| Key result 5.4: 0.0055; 8.5 s; 20.1 swings; lid 0.0107; ratio 1.002; both about 0.92 | verified with ζ = 0.0055 as stated (8.46 s; 20.06). Unrounded ζ = 0.005547 would give 8.4 s and 19.9 swings. Lid 0.01068; 1.0024; 0.918 and 0.921. |
| Problem 2: 20.1 swings, 19.5 s; Problem 3: 2.38 | verified (20.06; 19.48 s; 2^{5/4} = 2.378). |
| 6.1: Φ = 73 %; Φ_c = 0.635; 64 %, 74 %; 2γ/R₃₂ = 2600 Pa; p_L = 2400 Pa; G₀ = 166 Pa; τ_y = 5.4 Pa; Φ − Φ_c = 0.095 | verified (2600; 2400; 166.4; 5.415). The packing fractions are standard values. |
| sin α = 0.11, about 6°; τ_y = 9.4 / 5.4 / 2.5 Pa at φ_ℓ = 0.24 / 0.27 / 0.30 | verified (0.107, 6.1°; 9.375, 5.415, 2.535). |
| 6.2: Ca_f = 1.6e-5; 7.5 + 4.2 = 11.7 Pa; τ = 17.1 Pa | verified (1.585e-5; 7.47 + 4.25 = 11.72; 17.14). |
| 6.3: Z = 0.18, l/r_m = 0.004 (as used); second term at most 1.5 %; 2.1 / 9.7 / 28 / 45 Pa; cap 20 to 223 Pa | verified (1.53 % of the first term at 1 mm/s; 2.10, 9.66, 28.2, 44.7; cap 19.9 to 223.3). The source values are unverifiable, because they come from [12]. |
| h_eff = 9.9 mm; C_e = 206.7 Pa(s/m)^{2/3}; ⟨\|sin\|^{5/3}⟩ = 0.536; ∮\|cos\|^{5/3} = 3.365 | verified (9.873; 206.68; 0.5356; 3.3652). |
| ζ_edge = 0.62 (1 mm), 0.36 (5 mm); "65 to 111 times" | verified (0.618; 0.362; 65.2 and 111.5). Text slip in the same sentence: "of section 5.4.of section 5." has a duplicated phrase (editorial, not physics). |
| Ex. 6.2: z₊* = 4.1 mm; 7.6 mm; 1.9 m/s²; 2.0 mm at 5 m/s²; "about 3 times"; wedge 8.1 mm | verified (4.060; 7.560; 1.897; 2.011; 2.98; 8.121). |
| Problem 5: about 15 m/s² | verified (15.01). |
| 6.5: 1.242; 0.897; 3.421 → 3.070 Hz; β_h = 1.241 | verified (1.24156; 0.89746; 3.0699; 1.24097). |
| Sauret 3.1 Hz against 3.3 Hz | unverifiable, because it is quoted from [13]. |
| Layers brake "about 6 % too strongly" with the head | verified (√(3.42/3.070) − 1 = 5.5 %). |
| 6.6: μ_f floor 123 Pa s at 0.05 s⁻¹; ρ2Δx = 3.0 kg/m² | verified (122.77; 3.021). |

### Section 7

| Number(s) | Verdict |
|---|---|
| Table 2 (all entries); b = 5 N/A | verified against `CART_COMMON` (N_gK_m/R_w = 5). |
| M_s = 1.954 kg; turning parts 0.150 + 0.125 = 0.275 kg; M_x = 2.529 kg | verified. |
| Ex. 7.1: 15 N; 5.93 m/s²; 7.5 V; 2.25 A, 11.25 N; 0.6 A; N₀ = 22.1 N; 17.7 N; 18.75 N | verified (5.930; 22.116; 17.69). |
| Body 2.79 Hz; 2.75 Hz with the tyre | verified (2.789; 2.7495 from the eigenvalues of A_s). |
| Kerb crest curvature radius 24 mm < R_w; steepest axle slopes 0.251 / 0.262 / 0.785 equal the road's | verified (24.3 mm; the `road_table` axle slopes 0.25132 / 0.26179 / 0.78531 equal the road's own maxima). |
| Table 3: roads, speeds, durations; start 1 m before the first bump; push at 0.3 s | verified against `run_b.py` (ROADS, TASKS, push = (0.3, 1.0, 0.146)) and `ride_extra(x0 = 0.5)`. |
| Bumps 0.29 m apart: 3.448 Hz, 0.8 % above 3.421 Hz | verified (3.4483; 0.81 %). |
| 7.3: head-loaded period about 326 ms; a phase of a few degrees | verified (theory 325.7 ms, 2.2°; with the computed 2.915 Hz, 343 ms and 2.1°). |

### Sections 8–10

| Number(s) | Verdict |
|---|---|
| Grid 57 × 57 × 114 = 370,386; 1.5 mm; 1,001,952 particles; 0.429 mg; 0.93 mm; 126,399 cells' worth; 7.93 per cell | verified (Geometry formulas; mp = 4.2875e-7 kg; d = 0.933 mm; 126,399.2; 7.927). |
| kΔx = 0.071; 8.3e-4 per step | verified (0.0706; 8.32e-4). |
| "at 2 ms a step the swing would decay at 0.42 s⁻¹, a damping ratio of 0.019, more than three times the stout's own friction" | **wrong, because** a loss of the fraction f = 8.3e-4 of the velocity per step damps the amplitude at f/(2Δt), not f/Δt: only the kinetic half of the swing's energy is hit. A direct simulation of an oscillator with that velocity loss gives an amplitude decay rate of 0.208 s⁻¹. Correct: about **0.21 s⁻¹, ζ ≈ 0.0097, about 1.8 times** the stout's own 0.0055. Further, for the swing's potential flow every velocity component is harmonic. In 3D the tent smoothing's leading term (Δx²/12)∇²u then vanishes (cos kx and cosh kz factors 0.999584 × 1.000416 = 0.99999997), so even 0.21 s⁻¹ is an upper bound for the bulk. The 1D argument fits only the surface and boundary cells. |
| ν Δt/Δx² = 0.0018; limit 1/6 | verified (0.00182). |
| CG tolerance 1e-5 of the largest right side; at most 600 iterations | verified (`Stout(tol = 1e-5, maxit = 600)`; residual max\|r\| < tol·max\|b\|). |
| λ_h/Δx = 3.4; λ_h k = 10.7 at k = π/Δx | verified (3.42; 10.74). |
| r₀ = 0.9Δx and 0.505Δx; "the weighted mean lies 0.505Δx below the top of a flat seeded layer" | verified: my evaluation over the code's seed lattice (h = Δx/2, h_z = 0.7485 mm) gives 0.5053–0.5054Δx. |
| Fallback 0.68 cell; "no column needed it in the stored rides' rest test" | verified (`fallback_columns_max = 0` in the rest guard of run 8, and of run 10). |
| Drops: more than 1.5 cells above the surface of the column and of the eight around it | verified (`observe`). |
| 1,977 trusted columns | verified: 1,977 columns with r < R − Δx, and exactly these hold stored heights in every file. |
| Δt = 2 ms; CFL 0.8; last step shortened; cart sub-steps 0.1 ms; float32 / float64 split | verified (`make_advance`, `pressure`, `head_sheet` (float32 sums), `Cart` (float64)). |
| NVIDIA Tesla T4; 84 to 93 ms a step; 43 to 48 s per simulated second; "a ride of 8 s about 6 minutes" | verified against the stored run records (ride ms/step 84.1–92.8; s/s 43.1–47.7; 8 × 47.7 s = 6.4 min). Unverifiable as timings in themselves, because they cannot be re-measured without the GPU. |
| Books, stout: "every stored picture of every ride … largest discrepancy 0 particles" | verified for the 9 files that store books (`stout_err_particles_max = 0`). Unverifiable for `free_wall_1.5.json`, because that file (version 6) stores no books (`books: null`). Its stout reading is 429.583 g in every frame and spill_g = 0, which is consistent. |
| Books, head: largest discrepancy 1.3e-8 mL | verified (max 1.257e-8, in `ride_sharp30_preview`). |
| Impulse against momentum: at most 9e-15 | verified (stored rides: max 8.69e-15, ride_bump25 of run 8; run 10's rides ≤ 2.1e-15). |
| Rest test: limits 0.75 / 0.375 mm; 0.50 mm; 0.129 mm; nothing left the glass; 25.4 µJ; 429.6 g; 6.0 µm | verified (run 8: 0.4978, 0.1292, 25.41 µJ, 6.03 µm; run 10 gives the same to 0.03 µJ). |
| 10: storage steps 0.02 mm, 0.1 mm, 0.1 mm, 0.1 mm³; SHA-256 per file | verified (qH, qhf, qd, qv in every file; all 10 hashes verified in the browser). |
| Playback: clock step capped at 0.1 s; picture round(30T); no blend; stops at the end; words at most 4 per second | verified in `guinness-jax-play.js` (Math.min(0.1, …), Math.round(T·fps), > 250 ms) and in headless Chromium. |
| Drawing: bilinear over stored columns, missing ones left out; outer ring at the wall; head fades below 1.5 mm; drop 0.43 mm³; lumps by volume | verified in `stout-view2.js` (`at`, `atInward`, hfm/0.0015, radius ∛(3V/4π)). |
| Lean and tilt from the unrounded surface change by at most 0.02 mm when read from the stored surface | verified (my reading of the stored files: max \|Δlean\| = 0.020 mm, max \|Δtilt\| = 0.007 mm). |

### Section 11

| Number(s) | Verdict |
|---|---|
| Ring r = (13/16)(R − Δx/2) = 31.2 mm; 64 angles; fit from 0.1 s after the push | verified (31.16 mm; fit start t = 0.567 s). |
| Without head: 3.330 Hz, 3.331 Hz natural, 2.6 % below 3.421; ζ = 0.0160; method adds 0.0105 = 1.9 times; "about three times too fast"; refit 3.331 Hz and 0.016 | verified. Stored fit: 3.3302 / 3.3306 / 0.01601. My bounded refit of the stored file: 3.3302 / 3.3306 / 0.0160. 2.63 %; 0.01046; 1.89; 2.9. |
| First swings without the head a little smaller than 5.0 mm on the ring | verified (largest \|q_ring\| 4.78 mm). |
| With head: 2.639 Hz, t_d = 0.128 s, 2.915 Hz, ζ = 0.425; refit 2.917 and 0.425; the method's loss "about 2 %" | verified. Stored fit: 2.6388 / 0.1284 / 2.9152 / 0.4250. My refit: 2.6404 / 0.1283 / 2.9172 / 0.4252. 0.0105/0.425 = 2.5 %. |
| Fitted swing 2.3 mm at the wall; ζ_edge = 0.47, 11 % above 0.425 | verified (2.26 mm; 0.471; +10.9 %). |
| k = 44.6 m⁻¹ on the grid; 0.902; 3.004 Hz; computed 3.0 % lower | verified (44.64; 0.9021; 3.0046; 2.98 %). |
| e-fold in 0.37 of a period; tail −0.03 mm after 1.5 s | verified (0.374; −0.028 mm). |
| ω = 18.32 rad/s, ζ = 0.425, β_h = 1.241 | verified (stored plant w = 18.31699, beta = 1.24095). |
| Table 4 (cart alone): 1.6 m/s², −0.7 to 20.0, 45 mm, 10 mm; 1.0, 1.5 to 17.6, 8.5, 7.1; 28.8, −2.4 to 20.6, 24, 26 | verified (my driver: 1.64, −0.67 to 19.95, 45.3, 10.5; 1.04, 1.54 to 17.64, 8.54, 7.08; 28.80, −2.41 to 20.61, 23.7, 25.9). |
| 45 mm is 2.0 times 22.5 mm; the bumps 18 % too fast for the head's swing; kerb speed drop 0.29 m/s; 7.1 mm below 7.6 mm | verified (2.01; 3.448/2.915 = 1.183; 0.293). |
| 11.4: threshold 0.22 m/s² at 6.84 Hz (bare); ε = 1.71 at 1.81ω, 16.8 m/s² at 5.28 Hz; vertical acceleration within ±12 m/s² | verified (0.218 at 6.841; my own Floquet search gives 1.7091 at 1.810ω, 16.77 m/s², 5.277 Hz; max \|a_z\| = 12.2 m/s²). |
| Table 5: tilt / lean 13.6 / 13.9, 8.0 / 8.9, 22.2 / 24.3 mm; foam 0.01 mL from 1.50 s, 0, 2.44 mL from 0.67 s; stout 0; speeds 0.94–1.05, 0.96–1.04, 1.21–1.52; currents 2.40, 2.00, 2.98 A | verified from the stored files (13.54 / 13.88; 7.96 / 8.94; 22.23 / 24.26; 0.0097 mL at 1.500 s; 2.445 mL at 0.667 s; 0.944–1.051; 0.962–1.036; 1.211–1.517; 2.402, 1.999, 2.984). |
| 1.40 s: back wall up 8.1 mm, front down 5.8 mm; lump over the back rim | verified (+8.10 / −5.78 mm; the first lump at x = −37 mm, which is the back). |
| Kerb foam over the front rim | verified (the first 157 lumps at x = +21 to +38 mm). |
| Single bump: wall rises about half of 8.9 mm, below 7.6 mm | verified. |

### Section 12

| Number(s) | Verdict |
|---|---|
| T_s = 1 ms; F_max = 40 N; τ_u = 5 ms | verified (`CART_COMMON`). |
| ω_c = 2π × 8 Hz; M_x = 2.505 kg without head; K_p = 25.18; K_i = 316.4; 1 % heavier; roots −21.6, −29.0 s⁻¹ | verified (2.5046; 25.1788; 316.406; 0.99 %; −21.58, −28.98). |
| Ex. 12.1: 25.18 − 17.27j; 2 + 46.33j; L = −1.744 − 2.793j; \|1 + L\| = 2.890; \|S\| = 0.346; 0.352 with lag and half-sample delay; 35 % | verified (−1.7436 − 2.7925j; 2.8898; 0.3460; 0.3516). |
| 12.3 (cart alone, kerb): 11.25 N; 15 N; slope 0.785; N up to 105 N, 4.7 times; up to 82 N within 42 ms; over 15 N for 20 ms; 6 times in the air, 92 ms | verified (104.9 N, 4.74; 82.3 N; 20.4 ms; 6 events, 91.9 ms). The 42 ms is 43.0 ms at my 0.1 ms resolution (42 ms at 1 ms sampling). The push peaks 5.7 ms after first touch. |
| Speed loop: 2.98 A; 1.5 → 1.21 m/s; early full current: up to 1.51, down to 1.23 m/s, loss 0.28 m/s | verified (2.977 A; 1.207; 1.5059, 1.227, 0.279). |
| x = 1.437 m at first touch | verified (1.4370). |
| Kick: ω_d = 16.58; t_p = 1.132/16.58 = 68 ms; 18.9 mm; e^{−0.531} = 0.588; 11.1 mm | verified (16.580; 1.1318; 68.3 ms; 18.97; 0.5878; 11.15). |
| Key result 12.3: 7.3 times; 92 ms; 0.28 m/s; about 11.1 mm | verified (7.32). |
| Ex. 12.2: 2 mm and 3 mm ahead; 1.16 A; 3.47 A; 105 N, 82 N, 16 A | verified (1.158; 3.474; 16.5 A). |
| Skyhook c_sky = 47.6 N s/m; ζ 0.70 instead of 0.12 | verified (47.636; 0.117–0.118). |
| Bryson limits 0.05 m/s, 2 mm, 2 mm × ω, 2 cm, 3 A; \|K₄\| = 150 A/m | verified. |
| Ex. 12.3: K = (71.12, −1228.72, −40.50, −150.00); within 6e-3 of the stored gains; 7.1 A; +1.23 A; 0.40 A; 1.5 A | verified (my Riccati solution 71.1216, −1228.7227, −40.4996, −150.0000; max difference 6.04e-3 from the stored gains). |
| Eigenvalues −7.79 ± 16.58j → −10.83 ± 7.03j, ζ = 0.84, 39 % faster; −2.57 and −232 s⁻¹ | verified (−10.834 ± 7.026j; 0.839; 39.2 %; −2.571; −232.06). |
| Bare design K = (75.0, −1937.8, −38.9, −150.0); 0.12 → 12.0 s⁻¹; about 101 times | verified (75.04, −1937.81, −38.89; 0.119 → 12.01; 100.8). |
| W_F = 0.5 N² s → 0.22 N s in 0.1 s; W_a = 0.002 → 0.026 m/s per swing; σ_v = 2 mm/s, σ_q = 0.8 mm | verified (0.224; 0.0262). |
| Ex. 12.4: L = [[0.953, −0.0038], [−0.0006, 0.060], [−1.172, 0.926]]; 9.5 and 11.7 mm/s; 1.23 against 1.241; 0.060 mm and 0.93 mm/s; 17 readings, 33 ms, a tenth of a swing; 2.0 mm/s, 0.20 mm, 6.9 mm/s | verified (my steady two-sample cycle: 0.9534, −0.00379, −0.000606, 0.0602, −1.1724, 0.9262; ratio 1.230; 16.6 readings; 33.2 ms against a period of 343 ms; sd 1.95 mm/s, 0.196 mm, 6.89 mm/s). |
| 12.8: M_xω²/(β_h b) = 2.529 × 335.5/(1.241 × 5) = 136.8 A/m; 0.70 A; Problem 10: 1.34 A | verified (136.77; 0.697; 1.338). |
| Static tyre compression 1.1 mm; a_m = 0.5, z_m = 10 mm, d_m = 0.2 mm, F_m = 40 N | verified (1.106 mm). |
| Ex. 12.5: K_s = (−501.22, 11.92, −6.34, 630.00); 84 %; 99 N/m; −1.93 ± 17.17j (2.75 Hz, 0.11) → −4.93 ± 4.98j (1.12 Hz, 0.70); wheel hop 41.7 Hz, 0.08 → 0.12 | verified (−501.2157, 11.9232, −6.3428, 630.0044; 83.5 %; 98.8; 2.750, 0.112; 1.115, 0.704; 41.68 / 41.69 Hz, 0.083 → 0.124). |
| Port check: 4e-13 A (speed, preview, skyhook), 6e-8 A (slosh, joint); suspension gains agree with the stored ones to 8e-6 | verified: re-run gives 4.18e-13 and 6.39e-8 A; K_s difference 8.4e-6. |
| Problem 11: −2.0980° against −2.0990°, 0.99933 | verified (−2.09803, −2.09897, 0.999330). |
| Problem 12: 0.588; 0.991 | verified (0.5878; 0.9914). |
| Table 8, gentle roads: joint 1.00 / 1.03 mm, 0, 0, 1.72 A, 0, 7.1 N; 1.03 / 0.88 mm, 1.65 A, 7.9 N | verified (tilt 1.00, lean 1.04 from the stored surface, 1.03 from the index; 1.03 / 0.88; 1.720; 1.646; 7.06 N; 7.93 N). |
| Table 8, kerb: preview 23.0 / 23.9, 2.51 mL, 2.95 A, 6; slosh 20.8 / 21.8, 1.63, 2.97, 6; joint 24.6 / 25.4, 2.07, 2.93, 5, 11.5 N; speed held 22.2 / 24.3, 2.44, 2.98, 6 | verified (23.03 / 23.86; 2.507; 2.950; 6 \| 20.81 / 21.84; 1.626; 2.971; 6 \| 24.55 / 25.42; 2.074; 2.929; 5; 11.45 \| 22.23 / 24.26; 2.445; 2.984; 6). |
| 12.10, gentle: "about 13 and 10 times less"; 1.72 / 1.65 against 2.40 / 2.00 A; ≤ 0.016 A cancellation; filter 0.04 / 0.03 mm rms against probe 0.19 / 0.15 mm | verified (13.5 and 10.2; 0.0156 A; 0.037 / 0.034; 0.192 / 0.146). |
| Fig. 5: bumps under the wheel between about 0.8 and 2.3 s | verified (0.835 to 2.324 s). |
| Fig. 6: wheel at the kerb at about 0.62 s; first forward peaks within a tenth of a second | verified (0.625 s; peaks at 0.67–0.70 s). |
| Fig. 6: "and swing back almost as far" | **wrong, because** this holds only for speed held (+22.2 / −24.3 mm) and preview (+21.2 / −23.9 mm). Slosh LQR swings back only to −12.4 mm after +21.8 mm, and joint control to −17.0 mm after +25.4 mm. The regulators do cut the swing back. |
| 12.10 kerb: "the command at or beyond 3 A in 6 or 6 stored pictures, about 200 to 200 ms" | **wrong, because** the four kerb rides have 6 (speed held), 6 (preview), 6 (slosh LQR) and 5 (joint) such pictures (Table 8 itself says 5 for joint). Correct: **"5 or 6 stored pictures, about 170 to 200 ms"**. |
| Kerb first surge: 21.2 (preview), 21.8 (slosh), 25.4 (joint) against 22.2 mm | verified (21.18, 21.84, 25.42, 22.24; max lean for t ≤ 0.8 s). |
| "The largest leans of Table 8 can come from the swing back, a quarter of a second later" | verified with a remark: for speed held and preview the largest \|lean\| is the swing back at 0.87 s, 0.20 s after the surge at 0.67 s ("a fifth" rather than "a quarter"). For slosh and joint the largest is the surge. |
| Foam 1.63 / 2.07 / 2.44 / 2.51 mL; no stout | verified. |
| Late lean 1.8 and 2.5 mm (slosh, joint); speed back at 1.5 m/s; cancellation current 0.904 A; filter against probe 0.67 / 0.58 mm rms against 2.66 / 2.02 mm | verified (1.79, 2.50 mean over t ≥ 1.5 s; 0.9043 A; 0.675 / 0.578; 2.659 / 2.022). |
| 13: 2.6 %; ζ ≈ 0.0105; "about 0.14 of the push"; at most 11 drops | verified (0.137; max nd = 11 in ride_sharp30). |

## D. Descriptions of the method against the code

| Id | Description in the note | Verdict |
|---|---|---|
| M1 | 8.3, order of the steps (p2g → surface → viscosity → thin layers → gravity kick → head load → pressure → extrapolation 3 cells → g2p and move → foam break) | verified line by line in `Stout.step`, `prepare` and `make_advance`. The kick is added after `friction`, as the note says. |
| M2 | 8.3 step 3, viscosity "1 − 6νΔt/Δx² times its old value plus νΔt/Δx² times each of six neighbours" | verified for interior faces. Remark: the code includes only neighbours that are open and hold mass, so faces at the glass and the surface have fewer than six. |
| M3 | 5.2: "on the area of glass in each cell it applies the stress ρ√(νω/2)u_∥, with u_∥ the sliding velocity on the grid" | **wrong in detail, because** `friction` multiplies every face-velocity component (u, v and w) on faces next to cut cells by exp(−√(νω/2)·a·Δt), the wall-normal one included, not only the part along the glass. Correct description: the drag acts on the full face velocity in the cells the glass cuts. The in-phase energy argument holds only for the tangential part. |
| M4 | 5.4: skin drag on the horizontal velocity of the top cells "whenever the head is present" | verified with a remark: the skin is switched on with the "full" model (the head model) and acts on every column's top cells. It keeps acting on a column whose head has broken off, which only happens if the whole head stood above the rim. |
| M5 | 6.6: μ_f held at its value at 0.05 s⁻¹; implicit solve by conjugate gradients | verified (`eta(max(g, 0.05))`). Remark: a fixed 60 Jacobi-preconditioned iterations, not run to a tolerance. |
| M6 | 6.3: κ with \|w\| kept above 1 mm/s; cap at τ_y + τ_v at shear rate v_s/(2R₃₂); Z and l/r_m held at the 0.25 values | verified (`head_sheet`, `head_wall_stress`, `np.interp` clamps at 0.25). |
| M7 | 6.4: weight zero when g′ < 0; break rule with \|g′\| and outward push; lumps fly under g_eff until they land on the body or fall away | verified (`step`: max(−g_z, 0); `head_spill`). |
| M8 | 6.6: "the head's forces act on the top two cells of stout … the layer the surface lies in and the one below" | **wrong in detail, because** the code adds the sheet's change dw to the two vertical-velocity faces that bound the top liquid cell: the face below it (shared with the second cell) and the face above it (at the air). The mass ρ2Δx is these two faces' share. Correct description: the two w-faces below and above the top stout cell. |
| M9 | 8.4: Batty face weights; Jacobi-preconditioned CG to max residual < 1e-5 max\|b\|, ≤ 600 iterations; ghost condition with α ≥ 0.05; head inertia via (33); w_h set to the new surface-face velocity | verified (`pressure`, `step`). |
| M10 | 8.5: level set (34), mirror images within 2Δx of the glass, r₀ = 0.9Δx and 0.505Δx, body found from the first field and surface from the second in the top 3 cells, fallback 0.68 cell | verified (`level_set`, `surface`). Remark: the mirror is radial at the particle's own height (r → 2R(z) − r), close to but not exactly "the nearest point" on a sloping wall. |
| M11 | 8.3 step 9: a particle that would cross the glass is put back; above the rim and outside its radius it is spilled and flies | verified (`g2p`). |
| M12 | 7.3: F_n = −(P_n − P_{n−1})/Δt_n from the particles; the impulse book; the cart uses the previous step's push during its sub-steps | verified (`make_advance` ride branch: F computed after `S.step`, used in the next step's `cart.step` loop). |
| M13 | 7.1–7.2: cart forces, grip clip ±μ_gN, N ≥ 0, axle as the highest point of the rolled wheel | verified (`Cart.forces`, `road_table`). |
| M14 | 11.3 and 12.3: the cart alone with a frozen pint, current set every millisecond, sub-steps 0.1 ms, mean acceleration over 2 ms | verified by re-running it (numbers above). |
| M15 | 11.1: lean on the ring R − Δx/2 with the half-cell inward step; tilt 2·(2/64)Σ η cos θ; free-swing fit on ring 13 from 0.1 s after the push; ω = √(ω_d² + 1/t_d²), ζ = 1/(ωt_d) | verified (`pack_ride.py` ring/LEAN/TILT; `run_b.py` `fit_swing`). |
| M16 | 12.2: integral frozen while \|i_cmd\| ≥ I_max; gains fixed for the bare-stout cart | verified (`sample`; `CART_COMMON` K_p, K_i reproduced from M_x = 2.5046 kg). |
| M17 | 12.4: preview reads z_a′ at x + vτ_i with N₀ = (M_s + m_w)g | verified. |
| M18 | 12.6: "the controllers of the stored rides use the swing the computed stout actually has, measured in the same run before the controlled rides" | **wrong, because** all five controlled rides come from notebook version 10 (run 10). Run 10's task list (`run_b.py`, RUNSET run10: rest plus the five rides) has no free swing. The plant stored with each controlled ride reads `"measured": "run 8's free_full_1.5, ring 13 (notebook version 8)"`. Correct: the plant (ω = 18.32 rad/s, ζ = 0.425) was measured in run 8 (version 8) with the same solver code, and given to run 10. β_h = 1.241 was applied in run 10. |
| M19 | 12.7: probes at R − 2.5Δx and R − 4Δx extended to the wall, read once per fluid step and used at the next sample; no noise; filter starts at rest at v₀ | verified (`probes`, `make_advance` with `pfresh`, `Cart.init`). |
| M20 | 12.8: joint control = slosh LQR on the estimate + i_par + susp LQR, clipped to ±40 N with 5 ms lag; filter re-discretised each sample with ω²(1 + a_z/g) | verified (`sample` ctrl 4, `disc`, `step`). |
| M21 | 12.9 box: the controllers are a port of `stout-cart.js` | verified (port check re-run, numbers above). |
| M22 | "Where the data come from": versions 8 / 10 / 6 and commits 96e8a1d / 58eea68 / 4c10527; `stout_jax.py` unchanged between 96e8a1d and 58eea68; the later changes cannot change the headless free swing | verified. The index commits match. `git diff 96e8a1d 58eea68 -- stout_jax.py` is empty, and also empty up to HEAD. The diff from 4c10527 to 96e8a1d touches only the head's mass, the sheet switch, the probes and `prepare` refactor, and the cart and controllers, none of which acts in the `wall` model. |
| M23 | 10: page playback, fingerprint check, table and readings | verified in headless Chromium (see the top of this file). Remark: if `crypto.subtle` is unavailable (plain-http non-localhost), the page skips the check rather than refusing the file. |

## Counts

Each row has one verdict. Rows with mixed parts are counted by their weakest part:

- "wrong" if any part is wrong;
- otherwise "unverifiable" if any part is unverifiable;
- otherwise "verified".

| Part | Rows | verified | wrong | unverifiable |
|---|---|---|---|---|
| A. Numbered equations (1)–(52) | 52 | 49 | 0 | 3 ((19), (20), (21): the laws are quoted from sources) |
| B. Unnumbered equations | 25 | 25 | 0 | 0 |
| C. Numbers and groups of numbers | 113 | 102 | 3 | 8 (quoted source values; the drawing's dimensions; GPU timings; books of free_wall_1.5) |
| D. Method descriptions | 23 | 20 | 3 | 0 |
| **Total** | **213** | **196** | **6** | **11** |

**The six wrong items:**

1. **8.2, plain-PIC loss.** The swing would decay at about 0.21 s⁻¹ (ζ ≈ 0.0097, about 1.8 times the stout's own friction), not 0.42 s⁻¹, ζ = 0.019, "more than three times". In 3D the leading term even vanishes for the swing's potential flow.
2. **12.10, kerb.** "6 or 6 stored pictures, about 200 to 200 ms" should be "5 or 6 stored pictures, about 170 to 200 ms".
3. **Fig. 6 caption.** "swing back almost as far" is true only for speed held and preview. Slosh LQR swings back to −12.4 mm after +21.8 mm; joint control to −17.0 mm after +25.4 mm.
4. **5.2, wall drag.** The code damps all face-velocity components in cut cells, not only u_∥.
5. **6.6, sheet faces.** The sheet's change goes to the two w-faces below and above the top stout cell, not to "the top two cells".
6. **12.6, plant.** The plant was measured in run 8 (notebook version 8), not "in the same run" as the controlled rides (run 10).

**Smaller points:**

- The duplicated phrase "of section 5.4.of section 5." in 6.3.
- Surface tension is left out of (5) and (10). It would add +0.5 % to f₁₁.
- `free_wall_1.5.json` stores no books, so the "every stored picture of every ride" books claim cannot be checked for that one file.
- The swing back is 0.20 s after the surge, not a quarter of a second.
