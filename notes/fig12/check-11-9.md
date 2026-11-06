# Check of note §11.9 "The nonlinear live model: a swing that softens and swirls" and the last paragraph of §11.8

Checked 6 November 2026, 22:45–23:05 UTC, by a checker who did not write the note. The page changed while the check ran
(commits d80825d → 03728ed → 43b8a4a, the §11.9 text was rewritten after a referee). **The text checked is the one in
commit 43b8a4a** (`public/simulations/beer-slosh.html` sha256 e68f3e2d…; §11.8–11.9 unchanged since 22:53 UTC), with
`public/scripts/stout-cart.js` sha256 07e408cb… (it has the breaking cap) and `public/scripts/stout-nm.js` sha256 0189c245….
Items of the d80825d text that the brief asked about and that were since reworded are in the last section.

Verdicts: **confirmed**, **wrong** (with the correct value and the command), **unverifiable** (with the reason).

## How it was checked

- **Paper.** FLT = Faltinsen, Lukovsky & Timokha, JFM 804 (2016), read from `/tmp/claude-0/papers/flt2016.pdf` (eqs. 2.8–2.24,
  Table 1, Fig. 3, §3 eqs. 3.11–3.15, §4 eqs. 4.1–4.2, Fig. 7, the conclusions; pages rendered to check eq. 3.13b and the figures).
- **Coefficient script, rerun.** `tools/fig12/nm_coeffs.py 1 1.5 2 2.5 3.197` was run on a copy in the scratchpad (the script
  overwrites `public/scripts/stout-nm.js` and `notes/fig12/runs/nm_coeffs.json` when run; the repository copies were not
  touched). 4 min 18 s for five depths. The regenerated `stout-nm.js` is byte-identical to the repository's.
- **Independent derivation of d1, d2** (scratchpad `indep_d.py`): no Taylor expansion in ζ. The kinematic Jacobian
  D = ∂A_k/∂b_i and the kinetic matrix A_kl = ∫∇φ_k·∇φ_l are evaluated with exact z-integrals up to the actual surface at small
  finite amplitude, M = DᵀA⁻¹D formed numerically, and the s² growth of M_11 along p1 and along r1 extracted by Richardson
  extrapolation (s = 0.005, 0.0025). By rotation invariance (derived in SymPy, below) M_11(p1 = s) = μ + (a+b)s²,
  M_11(r1 = s) = μ + a s², d1 = (a+b)/μ, d2 = a/μ.
- **SymPy** (scratchpad `check_sympy.py`): (N3) from DḃΠ-relations; the most general rotation-invariant quartic kinetic energy
  of (p1, r1) (a two-parameter family); Lagrange's equations of it compared with (N4)/FLT 2.17a,b term by term; the quarter-turn
  map 2.17a → 2.17b; the most general invariant cubic coupling of (p1, r1) to (p2, r2) and p0, whose Lagrange equations give
  exactly the structure of FLT 2.18a–c and fix four reciprocity relations between d3…d10 that the script's numbers must obey.
- **FLT steady-state theory with the page's coefficients** (scratchpad `m1.py`, `flt_regimes.py`): m1, m3 by FLT 3.13a,b;
  backbone frequency; planar/swirl solutions by 4.1/4.2 and their stability by the 4 × 4 matrix C of 3.15. The transcription
  was validated by reproducing FLT Fig. 7 (h = 2, η1a = 0.02): U ≈ 0.925, H ≈ 0.985, P ≈ 1.045, |a| ≈ 0.11 and |b| ≈ 0.21 at
  H, against the figure's U ≈ 0.935, H ≈ 0.98, P ≈ 1.04, |a| ≈ 0.115, |b| ≈ 0.21 (the figure uses FLT's full mode set).
- **Page code in headless Chromium.** `python3 -m http.server -d public 8791` and scratchpad `chromium-check.cjs`
  (Playwright, HeadlessChrome 153) load `simulations/beer-slosh.html`, take `StoutCart`, `STOUT_NM`, `GUINNESS_GLASS` from the
  page, and run the loops of `linearity.cjs` + `linfit.cjs`, the `control.cjs` 25 mm bump, `swirl.cjs`, and a static-tilt run.
  Page errors: none. Every number agreed with the Node runs of the repository tools listed in each row (also run on the
  d80825d code without the breaking cap: identical, the cap never fires in these runs).
- 3D solver rerun for Table 5: `OUT=… node tools/fig12/linearity.cjs 3d <A>` for each A (about 15 s each).

## Equations

| Item | Verdict | Evidence |
|---|---|---|
| (N1) surface η − h = ψ0 p0 + ψ1(p1 cos θ + r1 sin θ) + ψ2(p2 cos 2θ + r2 sin 2θ), ψ_M = α_M J_M(k_M r), ∫r ψ_M² dr = 1 | confirmed | FLT (2.2)–(2.4), (2.22) with r1 = 0. cos²θ = ½(1 + cos 2θ) is why M = 0, 2 are the second-order families. Lengths in R, time in √(R/g): dimensionless. |
| k_M = 3.8317, 1.8412, 3.0542 (first zeros of J_M′) | confirmed | scipy `jn_zeros(1,1)`, `jnp_zeros(1,1)`, `jnp_zeros(2,1)`: 3.831706, 1.841184, 3.054237. |
| ψ1(1) = 1.6843 | confirmed | α1 J1(k1) = [2k²/(k²−1)]^½ = 1.684291 (analytic; script prints R1 = 1.6842906). |
| q1 = R ψ1(1) p1 is the q1 of (54); lean = 2(q1 + q2 + q3) | confirmed | `NMFluid.syncQ`; the lean in all tools is heightAt(R,0) − heightAt(−R,0), in which p0, p2 (even in θ → θ+π) and r1 (sin θ = 0) cancel exactly. |
| V = ½∬(η − h)² dA, exact for an upright wall | confirmed | ρg∬∫₋ₕ^{η−h} z dz dA = ½ρg∬(η−h)² dA − const; every mode has zero mean (∫r J0(k0 r)dr = J1(k0)/k0 = 0), so volume is conserved. |
| (N2) A_k = ∫_Ω φ_k dΩ, A_kl = ∫_Ω ∇φ_k·∇φ_l dΩ [17, 2.12–2.14] | confirmed | Equal to FLT's A^p (G^(0)) and A^pp (G^(1), G^(2)); each φ_k is harmonic, ∂_nφ_k = 0 on wall (J_M′(k_M) = 0) and floor (Z′(−h) = 0). |
| Kinematic condition D ḃ = A Π [17, 2.9], via Reynolds transport + Green's identity | confirmed | dA_k/dt = ∫_Σ φ_k V_n dS (φ_k fixed in space, walls fixed), V_n = ∂_nΦ, = ∫_Ω∇φ_k·∇Φ = Σ_l A_kl Π_l. FLT (2.9a,b) is the same equation. |
| (N3) K = ½ΠᵀAΠ = ½ḃᵀ DᵀA⁻¹D ḃ | confirmed | SymPy: ½ΠᵀAΠ − ½ḃᵀDᵀA⁻¹Dḃ simplifies to 0 for symmetric A (`check_sympy.py`). |
| L = K − V − (a_x/g)∬x(η − h)dA; sign of the fictitious-force term | confirmed | Potential of the inertial force −a_x per unit mass is +a_x x; ρa_x∫x dΩ = ρa_x∬x(η−h)dA + const. Static result: p1 = −P1 a_x/g, the front wall falls when the glass speeds up (correct physically; runs give negative lean for A > 0). |
| "K − V is the Lagrangian of Luke's principle once the kinematic condition holds [24]" | confirmed (up to a total time derivative) | Luke: L_L = −ρ∫(Φ_t + ½\|∇Φ\|² + gz)dΩ. ∫Φ_t dΩ = d/dt∫Φ dΩ − ∫_Σ Φ V_n dS, and with the (projected) kinematic condition ∫_Σ Φ V_n = Σ_k Π_k ∫_Σ φ_k V_n = Σ Π_k(AΠ)_k = 2K/ρ, exactly also in the truncated basis because Φ lies in the span of the test functions. So L_L = K − V − ρ d/dt∫Φ dΩ: same Euler–Lagrange equations. This is Miles (1976). [24] is listed as "not read for this note"; the statement itself is right. |
| Ordering p1, r1 ~ ε^{1/3}; p0, p2, r2 ~ ε^{2/3} [17, 2.16]; "keeping in each equation everything up to order ε" | confirmed | FLT (2.16). In the p0, p2, r2 equations no term of order ε exists: by the symmetry θ → θ + π (p1, r1 change sign, p0, p2, r2 do not) every term there has an even number of first-order factors, so order ε (odd count) vanishes; the script's cut at ε^{2/3} there is the same thing. |
| (N4) structure = FLT (2.17a): d1, d2 terms, couplings d3 (1.936), d4 (0.240), d5 (−2.312), d6 (0.043), forcing −0.9148 a_x/g | confirmed | Term by term against the script's p1 equation (h = 3.197): +1.93592 p̈1p2, ṗ1ṗ2, r̈1r2, ṙ1ṙ2; +0.23999 p1p̈2, r1r̈2; −2.31165 p0p̈1, ṗ0ṗ1; +0.04331 p̈0p1; κ11P1 = 0.914773. SymPy: Lagrange's equations of the general invariant quartic K give exactly the d1/d2 bracket of (N4) with d1 = (a+b)/μ, d2 = a/μ, and the quarter turn (p1→r1, r1→−p1, p2,r2→−p2,−r2) maps 2.17a onto 2.17b (difference 0). |
| (N5) p̈2 + 3.054 p2 = 1.208(ṗ1² − ṙ1²) − 0.398(p̈1p1 − r̈1r1); p̈0 + 3.832 p0 = −1.248(ṗ1² + ṙ1²) − 0.045(p̈1p1 + r̈1r1); "the like equation for r2" | confirmed | Script: p2 eq. d7 = −1.207610, d9 = 0.398113, σ2² = 3.054237; p0 eq. d8 = 1.247783, d10 = 0.045065, σ0² = 3.831706; r2 eq. has 2d7 ṗ1ṙ1 = −2.41522 and d9(p̈1r1 + r̈1p1): FLT (2.18b). Signs after moving to the right side are right. Reciprocity relations implied by the Lagrangian, μ1d4 = μ2d9, μ2d7 = μ2d9 − μ1d3/2, μ1d6 = μ0d10, μ0d8 = μ0d10 − μ1d5/2, hold to round-off at h = 1, 1.5, 3.197. |
| (N4)–(N5) are FLT 2.17–2.18 with Ir = 1 = Lukovsky's five-mode system, eq. 2.23 | confirmed | FLT §2.3: "Our computations with Iθ = 2 and Ir = 1 …" are compared with Lukovsky's (2.23) rescaled by (2.24). |
| Small-swing check: p̈1 + 1.8412 p1 = −0.9148 a_x/g; static tilt q1 = −3.335 mm per m/s², exactly −β1/ω1² of (17) | confirmed | Analytic (SymPy): wall height per a_x R/g = −P1ψ1(1) = −2/(ξ²−1) = −β1 g/(ω1² R). Number: 2·39.1/(2.38995·9.81) = 3.3354 mm. Chromium, page code, ramp to 1 m/s² and hold: q1 = −3.3354 mm in both `NMFluid` and `ModalFluid`. |
| d1p1²p̈1 is a mass that grows with the swing → softening; products with p0, p2 shift the frequency further | confirmed | Harmonic balance of the d1 terms alone gives ω² = σ1²/(1 + ½d1a²) (softening, d1 > 0). FLT's m1 = −½d1 + (couplings) = −0.782 − 1.102 = −1.884 at h = 3.197: the couplings soften in the same direction. |
| Units / limits | confirmed | All of (N1)–(N5) are dimensionless (R, √(R/g), a_x/g); the code converts with `axn = ax/g`, `ts = √(g/Rs)`. Small-amplitude limit = (54) for mode 1; deep-liquid limit, see the coefficient rows. |

## The coefficients

| Number / claim | Verdict | Evidence / command |
|---|---|---|
| FLT Table 1 (h = 1, r1 = 0, Ir = 1): d1 = 1.758023, d2 = −1.083355 | confirmed (paper) | FLT p. 619, Table 1, row Ir = 1. |
| "The script gives 1.758023 and −1.083355, every printed digit" | confirmed | Rerun: d1 1.758023, d2 −1.083355 (full: 1.7580233776, −1.0833546066). Independent exact-z route (`indep_d.py`): 1.758023, −1.083355. Command: `python3 tools/fig12/nm_coeffs.py 1` (run on a copy: it rewrites `stout-nm.js`). |
| p1ṙ1², p1r1r̈1, ṗ1r1ṙ1 have coefficients d1 − 2d2, d1 − d2, 2d2 | confirmed | h = 1: 3.924733, 2.841378, −2.166709 = d1−2d2, d1−d2, 2d2 to 6 digits; the same at 1.5, 2, 2.5, 3.197. Note: rotation invariance forces these combinations (SymPy), so this checks the script's Lagrange step and quadrature symmetry, not the integrals; the integrals are checked by Table 1. |
| The other coefficients (d3…d10) | confirmed against FLT Fig. 3 (graphical) | h = 1: d3 1.894, d4 0.166, d5 −2.323, d6 0.097, d7 −1.357, d8 1.376, d9 0.288, d10 0.106; FLT Fig. 3 at h = 1 reads ≈ 1.9, 0.2, −2.3, 0.1, −1.35, 1.4, 0.3, 0.1, and the trends to large h agree. |
| h/R = 125/39.1 = 3.197 | confirmed | `NMFluid` reports Rs = 39.100 mm at h0 = 125 mm; 125/39.1 = 3.1969. |
| σ1² = 1.8412 (3.421 Hz), d1 = 1.5633, d2 = −1.2106 | confirmed | Script: 1.841155, 1.563298, −1.210550. Independent: 1.8411554 (= k tanh kh), 1.563298, −1.210550. f = √(1.841155·9.81/0.0391)/2π = 3.4207 Hz. |
| κ11P1 = 0.9148 | confirmed | Script 0.914773; independent (∬xψ1cosθ dA)/μ1 = 0.914773 = k tanh(kh)·α1J1/k². |
| "from h/R = 1.5 on the coefficients change by under 2 %, the deep-liquid limit" | **wrong** for four of the ten | Between h = 1.5 and 3.197: σ1² 0.8 %, κ11P1 0.8 %, d1 1.8 %, d2 1.6 %, d3 0.4 %, d5 0.06 %, d7 1.8 %, d8 1.6 % (under 2 %), but d4 0.2286 → 0.2400 (4.8 %), d9 0.3821 → 0.3981 (4.0 %), d6 0.0518 → 0.0433 (16 %), d10 0.0543 → 0.0451 (17 %). The combination that sets the frequency shift, m1, changes 1.0 % (−1.8649 → −1.8837). Correct wording: "σ1², d1, d2 and the frequency-shift coefficient m1 change by under 2 %; the small couplings d6, d10 by up to 17 %". By h = 2.5 every coefficient is within 0.1 % of h = 3.197; the independent run at h = 10 gives d1 1.563236, d2 −1.210588. Command: `python3 tools/fig12/nm_coeffs.py 1.5 3.197`. |
| "~1 min per depth" (brief) | confirmed | 51 s per depth here. |
| [17]'s supplementary material "could not be reached for this note" | unverifiable | A statement about the author's access; not needed, since Table 1 and Fig. 3 are matched. |

## The live model: description against the code (`NMFluid`, `stout-cart.js` at 43b8a4a)

| Claim | Verdict | Code |
|---|---|---|
| Runs (N4)–(N5) with the generated coefficients | confirmed | `NMFluid` parses `STOUT_NM.eqs` (all monomials of the five equations). |
| Modes n = 2, 3 of (54) along the road added as before | confirmed | `step`: q[1], q[2] by the linear oscillator of `ModalFluid`. |
| Damping 2ζσḃ on each coordinate, ζ1 = 0.0053, others by the boundary-layer scaling | confirmed | `accel`: `rhs -= 2 zetaNM[i] sqrt(sig2[i]) bd[i]`, `zetaNM = z1 (σ1/σ)^½`; z1 = 5.23/(2π)·(ν/(g^½R^{3/2}))^½ = 0.00535. |
| Heave σ² → σ² max(0, 1 + a_z/g) | confirmed | `gf = Math.max(0, 1 + az/g)` multiplies the σ² term (the monomial equal to the coordinate) and the linear modes. |
| Each 0.5 ms substep solves a 5 × 5 system for the accelerations, then velocities, then positions (semi-implicit Euler, not exactly symplectic with a configuration-dependent mass) | confirmed | `n = ceil(dt/0.0005)`; Gaussian elimination with partial pivoting; `bd += ht·acc; b += ht·bd`. The remark on symplecticity is correct (symplectic Euler is symplectic in canonical (q, p), not in (b, ḃ) when M depends on b). |
| Surface drawn from (N1) over the whole glass | confirmed | `heightAt` and the page's drawing (`mH`, beer-slosh.html ≈ l. 1381) use all five coordinates plus q2, q3 on a full-glass grid (`ny = 2⌈R/dx⌉`). |
| The pour (56) uses the height at the wall at each angle; the crest's volume above the mean is shrunk by what poured out | confirmed | `wallAt(θ)` on 72 angles; `Vc = ∬max(0, η−h)dA` (12 × 48 midpoint), every coordinate and q2, q3 scaled by 1 − dV/Vc. |
| r1 starts at 10⁻⁵R (0.4 µm) | confirmed | `b[2] = 1e-5`; r1·R = 0.391 µm. (But see the swirl rows: the *wall* height of this seed is 0.66 µm.) |
| Push on the cart is (55) along the road; sideways and vertical pushes not passed | confirmed | `momentum()` returns [P_x, 0]; P_y kept in `this.Py` only; `World.advance` uses P[0], P[1]. |
| Probes, Kalman filter, LQR work unchanged; small-amplitude frequency is mode 1's | confirmed | `readProbes` uses `columnHeightAt` (= `heightAt`); `Observer` is built from mode 1 of (54) for both models; σ1² = k tanh kh equals (54)'s ω1² R/g. `control.cjs nm` runs all controllers. |
| Breaking cap: "clips the swing at 1.5 times the breaking amplitude (31.8 mm at the wall, a lean of 64 mm): coordinates and rates scaled back" | confirmed, one omission | `Acap = 1.5 Rs/ξ11` = 31.85 mm; if R ψ1(1)\|(p1, r1)\| > Acap all five b and ḃ are scaled by Acap/A1. Not said on the page: q2 and q3 are also clipped, each at the same 31.85 mm. "Lean of 64 mm" = 2 × 31.85 holds only without modes 2, 3. |
| "it touches none of the runs above" | confirmed | `breaks` = 0 in every Table 5 run, the 25 mm bump and the swirl runs (Chromium and Node); the same runs on the d80825d code without the cap give identical output. |
| "Driven harder still, the five equations run away" | confirmed | d80825d code (no cap), pour off, a_x = A sin(2πf t): A = 1 m/s² at 0.97 f11 reaches \|(p1, r1)\| = 7 × 10⁶; A = 2 m/s² at 1.00 f11 reaches 1760 (scratchpad `runaway.cjs`). With the cap: bounded at 0.484 (31.9 mm). |

## Table 5 and the numbers after it

Commands: `OUT=/tmp/x.json node tools/fig12/linearity.cjs nm 0.5,1,2,4,6`, the same with `modal` and `3d`, then
`node tools/fig12/linfit.cjs /tmp/x.json`. Chromium (page code) gives the same digits for the two models.

| Entry | Page | Rerun | Verdict |
|---|---|---|---|
| Peak lean, linear, A = 0.5/1/2/4/6 | 6.0 / 12.0 / 24.1 / 48.1 / 67.0 | 6.0 / 12.0 / 24.1 / 48.1 / 67.0 | confirmed |
| Peak lean, nonlinear | 6.0 / 12.0 / 23.9 / 46.9 / 61.3 | 6.0 / 12.0 / 23.9 / 46.9 / 61.3 | confirmed |
| Peak lean "during the push", 3D, A = 1/2/4/6 | 11.5 / 25.4 / 45.3 / 69.3 | 11.5 / 25.4 / 45.3 / 69.3 (all at t = 0.19–0.21 s) | confirmed |
| Peak lean "during the push", 3D, A = 0.5 | 5.9 | largest \|lean\| for t ≤ 0.3 s is **1.9 mm** (+1.85 mm at 0.25 s); the 5.9 mm is at t = 1.93 s, long after the push, a jump in an otherwise ±1.5 mm noisy series | **wrong**: the caption says "during the push"; `linearity.cjs` takes the maximum over the whole 2 s run. Correct entry 1.9 mm (or change the caption to "largest lean in 2 s"). The 3D solver barely responds to this push, consistent with the coupling 0.48 below. Check: `node -e` on `notes/fig12/runs/linearity-3d-a.json`, max \|lean\| for t ≤ 0.3. |
| Free swing, linear | 3.8, 7.5, 15.0, 30.0, 40.0 mm; 3.420 ×4, 3.418 Hz | same | confirmed |
| Free swing, nonlinear | 3.8, 7.5, 15.2, 30.0, 34.7 mm; 3.418, 3.410, 3.379, 3.291, 3.258 Hz | same | confirmed |
| Free swing, 3D | 2.1, 4.4, 14.7, 32.7, 36.9 mm; 3.160, 3.202, 3.194, 3.109, 3.056 Hz | same (fit misfits 1.2–6.5 mm rms) | confirmed |
| Theory behind the nonlinear frequencies | — | FLT backbone σ/σ11 = (1 − m1a²)^−½, m1 = −1.88365, a from the fitted amplitude: 3.418, 3.410, 3.379, 3.265, 3.217 Hz | confirmed: the model reproduces FLT's weakly nonlinear shift exactly where it should (first three); 3.291/3.258 at the two largest swings, where the swing decays and spills during the fit window. |
| Intro: 3D swing "slows from 3.20 to 3.06 Hz as it grows" | 3.202 → 3.056 | — | confirmed |
| "the nonlinear model slows by 4.7 % (3.418 to 3.258 Hz)" | 4.7 % | (3.418 − 3.258)/3.418 = 4.68 % | confirmed |
| "the 3D solver by 4.5 % … (3.202 to 3.056 Hz)" | 4.5 % | (3.202 − 3.056)/3.202 = 4.56 % | **wrong** (rounding): 4.6 %. |
| "the linear model not at all" | — | 3.420 → 3.418 Hz (0.06 %) | confirmed |
| Largest push spills 8.5 g (nonlinear), 12.2 g (3D), 5.0 g (linear) | — | 8.5, 12.2, 5.0 g | confirmed |
| 25 mm bump, open loop: nonlinear leans 50.8 mm, spills 16.1 g | — | `node tools/fig12/control.cjs nm 25 off 0.004 2.3`: peak 47.9 during, 50.8 after; 16.1 g (Chromium: 50.8 mm, 16.1 g) | confirmed |
| … (3D 60.7, linear 73.9) and spills (3D 11.9, linear 9.9) | — | `MODAL=1 node tools/fig12/study.cjs 25 off 0`: 73.9 mm, 9.9 g; stored 3D `notes/fig12/runs/study_25_off_0_0.004.txt`: 60.7 mm, 11.9 g | confirmed |
| 3D free swing weaker at small amplitude (2.1 against 3.8 mm) | — | 2.1 vs 3.8 | confirmed |
| One-oscillator coupling grows from 0.48 to 1.26 | — | `node tools/fig12/ident.cjs`: β = 0.482 (A 0.5), 0.709 (1), 1.261 (2) | confirmed ("the cause was not established": a hedge, fine) |
| Commands as printed | — | `linearity.cjs nm …` writes the JSON only with `OUT=notes/fig12/runs/linearity-nm.json`; as printed, the next command `linfit.cjs notes/fig12/runs/linearity-nm.json` reads the stored file, not the new run | minor: add `OUT=…`. `nm_coeffs.py` silently rewrites `public/scripts/stout-nm.js` (it reproduces it byte for byte). |

## The swirl

Command: `node tools/fig12/swirl.cjs 0.3 0.97,1.0,1.03,1.06 20`; longer runs and the seed in µm: scratchpad `swirl2.cjs`
(40 s); Chromium: `chromium-check.cjs`.

| Claim | Verdict | Evidence |
|---|---|---|
| Forcing 0.3 m/s²: displacement amplitude a/ω11² = 0.65 mm = 0.017 R | confirmed (number) | 0.3/(2π·3.4207)² = 0.649 mm; /39.1 mm = 0.0166. At 0.97–1.06 f11: 0.0177–0.0148 R. |
| … called a "sideways displacement amplitude" | **wrong** (word) | The shaking is along the road (a_x); "sideways" is the page's word for across the road (s1). Should read "a displacement amplitude along the road". |
| "the size of their worked example (0.02 R)" | confirmed | FLT Fig. 7: η1a = 0.02, h = 2. |
| At 0.97 and 1.00 f11 the sideways swing grows "from its 0.4 µm seed" | **wrong** (seed size) | The sideways swing as the page defines and stores it, s1 = R ψ1(1) r1, starts at 0.659 µm, not 0.4 µm (0.391 µm is r1·R, the coordinate, not the wall height). Chromium and `swirl2.cjs`: seed s1 = 0.659 µm. Say "from its 0.7 µm seed" or "from r1 = 10⁻⁵". |
| … to 18–20 mm within 12–15 s, as large as the swing along the road | confirmed | \|s1\| first reaches 18 mm at 11.98 s (0.97) and 15.39 s (1.00); then 16–21 mm alongside \|q1\| 16–19 mm. |
| At 1.03 and 1.06 f11 "it stays planar for the 20 s" | confirmed literally, misleading at 1.03 | At 1.06, \|s1\| peaks at 2.9 µm (8 s) and decays to 0.07 µm by 40 s: planar is stable. At 1.03, \|s1\| grows steadily, ×95 in 20 s (0.062 mm at 18–20 s) and to ≈ 10 mm by 40 s: the planar wave is unstable there too, only slower. |
| [17] places the stable swirl, in the steady state of a deep undamped tank, just above f11, with irregular sloshing below it | confirmed (approximately) | FLT Fig. 7 / §4: irregular between U ≈ 0.935 and H ≈ 0.98; only stable swirling between H and P ≈ 1.04; swirl and planar co-exist above P; planar only below U. FLT neglect damping ("The forthcoming analysis neglects the damping"). The stable swirl starts slightly below f11 (H ≈ 0.98). |
| "whether it is the steady swirl of [17] or its irregular regime was not established here" | can now be established | FLT's theory with the page's own coefficients (h = 3.197, m1 = −1.884, m3 = 3.306) and this forcing: U ≈ 0.925, H ≈ 0.985, P ≈ 1.035. So 0.97 f11 lies in FLT's irregular range (its run indeed shows \|q1\| dropping to 5 mm and \|s1\| wandering 12–21 mm), 1.00 and 1.03 in the swirl-only range (1.03: the slow growth above), 1.06 in the co-existence range (from rest: planar). The live model agrees with FLT's steady-state theory at all four frequencies. Command: `python3 flt_regimes.py notes/fig12/runs/nm_coeffs.json` (scratchpad). |

## Where it stops

| Claim | Verdict | Evidence |
|---|---|---|
| g/ω11² = R/ξ11 = 21.2 mm, a lean of 42 mm | confirmed (arithmetic) | R/(ξ tanh(ξh/R)) = 39.1/1.84118/0.99998 = 21.24 mm; lean 42.5 mm. |
| "there p1 = 0.32, and the wall amplitude is 0.54 R" | confirmed | 21.24/(39.1·1.6843) = 0.322; 21.24/39.1 = 0.543. |
| "A crest breaks when its downward acceleration reaches g" at that amplitude | unverifiable as stated; an upper estimate | It is the linear estimate of §8.5 (aω² = g, i.e. ka = 1), which §8.5 itself calls "a linear estimate"; here it is stated as fact. For two-dimensional standing waves the highest wave (Penney & Price 1952; Taylor 1953, the page's [16]) has H/λ ≈ 0.218, i.e. ka ≈ 0.68, which would put the onset nearer 14–15 mm at the wall. Not computed for a cylinder here; suggest "about 21 mm (linear estimate; real crests may break earlier)". |
| Beyond 21.2 mm its waves keep their smooth shape; numbers for 4 and 6 m/s² and the 25 mm bump are the model's | confirmed | Peak wall amplitudes: 23.5 mm (4 m/s²), 30.7 mm (6 m/s²), 25.4 mm (25 mm bump), all above 21.2; 2 m/s² stays at 12 mm. |
| The third-order modes that [17] adds "move the steady response by 5–15 % against the five-mode system" | **wrong in detail** | FLT conclusions: accounting for the *higher second- and third-order* modes (Ir up to 8) matters; the five-mode system, which omits them, "fails in accurately predicting the *experimental* steady-state response. The difference is approximately 5–15 %"; for elliptic forcing the five-mode branching differs from theirs by up to 5–10 %. So: the omitted modes are the higher radial second-order modes (p0j, p2j, r2j, j ≥ 2, which also change d1, d2: FLT Table 1) and the third-order modes; and the 5–15 % is the five-mode system against experiment. |
| The tulip is still replaced by the cylinder of its surface radius | confirmed | `NMFluid` uses Rs = R(h) and the cylinder coefficients. |

## Last paragraph of §11.8

| Claim | Verdict | Evidence |
|---|---|---|
| Table 4 live-model entries 24.7, 7.6, 73.9 mm / 9.9 g, 25.4 mm | confirmed | `MODAL=1 node tools/fig12/study.cjs 10 off 0` (24.7), `10 speed` (7.6), `25 off` (73.9, 9.9 g), `25 speed` (25.4). 3D entries from the stored runs: 25.0, 5.8, 60.7/11.9 g, 29.9. |
| "agrees with the 3D solver within 1 % where the swing is small and free" | **wrong** (marginally) | 10 mm open loop: 24.7 vs 25.0 mm = 1.2 %. (Sentence not part of this edit.) |
| "within about 20 % in lean and spilled mass where the swing is large or the speed loop holds the cart" | **wrong** for one row | 25 mm open: lean +21.7 %, spill −17 %; 25 mm PI: −15 %; but 10 mm PI: 7.6 vs 5.8 mm = +31 %. Correct: "within 15–31 %". (Not part of this edit.) |
| "It is linear: waves that soften, steepen or swirl are beyond it" | confirmed | `ModalFluid`: constant ω_n, m = 1 only, half-symmetric. |
| "Section 11.9 replaces its first mode by a nonlinear one, and that nonlinear model is now the figure's live model" (the edit) | confirmed | beer-slosh.html: `MODAL` is true unless `?grid=`/`?model=` asks otherwise, and the fluid is built with `modal: MODAL, nm: MODAL` → `NMFluid`. Strictly, mode 1 is replaced by five coordinates (p1, r1 and the driven p0, p2, r2); modes 2, 3 stay linear. |
| Command `MODAL=1 node tools/fig12/study.cjs …` | confirmed | `study.cjs` builds `modal: !!MODAL` without `nm`, so it still runs the linear model, which is what §11.8 describes. |

## Items of the d80825d wording asked about in the brief

- "for potential flow this L is Luke's variational principle with the kinematic condition built in (Miles)": right, in the
  sense derived above (equal up to a total time derivative once the kinematic condition holds; exact also in the truncated
  modal basis). The current wording "[24]" says the same.
- "(in the steady state the shift is set by one combination of them all, [17]'s m1, eq. 3.13a)": right; m1 = −1.88365 at
  h = 3.197, and the backbone it gives reproduces the model's 3.418/3.410/3.379 Hz.
- "this run … is driven harder relative to the damping": was wrong (FLT have no damping; their forcing 0.02 R is larger than
  this run's 0.017 R); removed in 43b8a4a.
- "so the grid damps small swings more than large ones. That is the grid's, not the stout's": was an unsupported causal claim;
  hedged in 43b8a4a.

## Errors, in short

1. Table 5, 3D peak lean at A = 0.5 m/s²: 5.9 mm is the maximum over 2 s (at t = 1.93 s); during the push it is 1.9 mm.
2. "the 3D solver by 4.5 %": 4.6 % (0.146/3.202).
3. "from h/R = 1.5 on the coefficients change by under 2 %": true for σ1², d1, d2, d3, d5, d7, d8, κ11P1, m1; not for d4 (4.8 %), d9 (4.0 %), d6 (16 %), d10 (17 %).
4. Swirl seed: the sideways swing s1 starts at 0.66 µm, not 0.4 µm (0.39 µm is r1·R).
5. "a sideways displacement amplitude": the forcing displacement is along the road.
6. 5–15 %: FLT's figure is the five-mode system against experiment, due to the omitted higher second-order and third-order modes, not "third-order modes against the five-mode system".
7. §11.8 (unedited sentences): "within 1 %" is 1.2 %; "about 20 %" is up to 31 % (10 mm, PI).
8. Not errors but worth a word: at 1.03 f11 the planar swing is unstable (s1 ×95 in 20 s, ≈10 mm by 40 s), as FLT's theory with the page's coefficients predicts; the breaking amplitude 21.2 mm is a linear upper estimate; the clip also caps q2, q3; `linearity.cjs` needs `OUT=` for the printed `linfit` command to read the new run.
