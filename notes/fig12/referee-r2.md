# Fig. 12 · referee report, round 2

Page: the frozen copy `scratchpad/r2/public/simulations/beer-slosh.html`, served at
`http://localhost:8766/simulations/beer-slosh.html`; the lecture note "Sloshing in a pint glass" (`<article class="paper" id="paper">`).
Read as two people at once: **S**, a school student who is good at mathematics, and **G**, a physics graduate. Judged against
`notes/STANDARD.md` (section 4, and Numa's verdict of 21 October 2026: Taylor's *Classical Mechanics* as the model).

How it was read: opened in headless Chromium (Playwright, SwiftShader WebGL) at 1440 × 900 and 390 × 844; all 35 folds of the
note opened (9 sections, 26 parts); each section screenshotted whole, in 1400 px slices (23 images, kept in the session
scratchpad `ref2/`). KaTeX errors: 0. Console and page errors: none. Horizontal overflow at 390 px: none. The note was read
fresh first and this report's sections A and B were drafted before `referee-r1.md` was opened; section C then checks every
round-1 point against the page. `plan.md`, `check.md` and `check-derivations.md` were not read. Numbers marked "checks" were
recomputed by hand from the note's own inputs; Q₁₁ = 0.03245 m, ω of mode (1,3) = 40.40 rad/s and the readouts
(f₁ 3.244 Hz, ζ₁ 2.44 %, 1/e in 2.01 s) were read from the running page's data store.

Tags: **[S]** a school student gets lost; **[G]** a graduate objects; **[both]**.

---

## A. Problems that run through the note

**A1. Three outright errors a careful reader will catch.**
1. Section 3, Key result box: "u = ∇φ: the flow runs **downhill** on the landscape φ." A gradient points uphill; with
   u = +∇φ the flow runs *uphill* on φ (downhill on −φ). [both] Either say "uphill" or drop the image.
2. Section 3, "The model in one place": "depth over **wave length** λD = 6.1". λ is not a wavelength. It is the eigenvalue
   k tanh kD of (8), a wavenumber in m⁻¹, and it is not yet defined at this point. λD is depth times wavenumber, i.e. depth
   over (wavelength/2π). The letter λ, which S and G both read as "wavelength", makes this worse. [both]
3. Section 5, "The head and the surface tension": "In (6) this adds (M_f/ρ) η̈ = (M_f λ/ρ) ∂²_t φ for a mode". The two sides
   have different units: (M_f/ρ) η̈ is m²/s² (like ∂_tφ), (M_fλ/ρ) ∂²_tφ is m²/s³. With ∂_tη = λφ, η̈ = λ ∂_tφ, so the term is
   (M_fλ/ρ) ∂_tφ; differentiating (6) once in time then gives ∂²_tφ (1 + M_fλ/ρ) + gλφ = 0, which is what the note writes
   next. The end result (11) is right; the line leading to it is not, and the missing "differentiate in time" is exactly the
   step S needs. [both]

**A2. The ★ promise is kept better, but not fully.** The byline now says the ★ parts "use vector calculus and Bessel
functions, and their results are restated without them".
- The unstarred text of section 3 still uses ∇p, ∇²**u**, (**u**·∇)**u**, ∇·**u** = 0, and the Key result uses ∇²φ = 0. Each
  term now gets a physical meaning (good), but ∇ itself, and the partial derivative ∂, are never named. [S] One sentence at
  first use would do: "∂/∂x is a derivative with the other coordinates held fixed; ∇p is the vector of the three such
  derivatives of p, pointing the way p rises fastest; ∇² is the sum of the three second derivatives."
- Section 4 (unstarred) uses J_m and its zeros; this is fine with the picture given ("a cosine whose swings weaken").
- Section 6 (unstarred) says the modes are orthogonal "a consequence of (10) being symmetric", but (10) lives in a ★ part.
  The skipping reader is sent into the part he was told he could skip. [S]
- The Faraday threshold (13) and its numbers (0.58 mm, ε = 0.34, 1.2 s⁻¹) appear only inside the ★ part "Pumping: Faraday's
  waves". The unstarred Key result "two ways in" says pumping "can only amplify a slosh that is already there" but not
  *when* it does. Problem 3 then asks S to use (13). Restate the threshold in one unstarred sentence (gain εω/4 must beat the
  damping γ; for the default pint, 0.58 mm at 2f₁).

**A3. One symbol, one meaning: much better, five clashes left.** [both]

| Symbol | Meanings now |
|---|---|
| Z | height above the foot (sec. 2 on) and the separated depth function Z(z) in "Where (7) comes from ★" (Z″ = k²Z, Z′(−D) = 0) |
| n | radial mode number (sec. 4 on) and the normal direction in ∂φ/∂n (sec. 4, (9), the wall terms) |
| b | I_b = floor ("bottom") integral in (16); γ_b = interior ("bulk") damping a few paragraphs later |
| a | wall amplitude a_n everywhere in the text; the legend of Figure 2 says "straight glass of the same **a** and D", where a is the surface radius R (the data store's old name). Undefined for the reader |
| C, P, S, E | C(t) in (5) and the amplitude C in (7); P(t), S(t) slow amplitudes (sec. 6) and P̄ power, dS surface element (sec. 7); E energy in (14), then "E stands for ∬|∇Φ|² r dr dz" in (16) (said openly, but still two meanings in one part) |

**A4. Checks (STANDARD §4 item 4).** The steady-tilt check, the cylinder benchmark, the deep limit, the Q closed form and the
energy method are all there. No explicit dimensional check of a derived equation is shown; a one-line check of (11) or (12)
would have caught A1.3.

---

## B. Section by section

### 1 · Carrying a pint

- The opening (walk, rocking grows, dies away, "a driven, damped oscillator") is the standard's item 1 done well, for both
  readers.
- "How claims are marked … Everything else is derived on the page." A few unmarked statements are neither derived nor
  sourced: "2.0 mm, a typical value for a toughened pint glass" (sec. 2), "a pint glass must hold its pint with room to spare"
  (sec. 2), "Beer is full of proteins that gather at the surface" (sec. 7), "A strongly driven slosh in a round glass can also
  turn into a swirl" (sec. 9). Either tag or source them, or soften the box's last sentence.

**Verdict: clear, leave it** (the box's last sentence is the only issue, and it is fixed elsewhere).

### 2 · The glass and the stout

- The photograph method is now explained step by step, the wall thickness is honestly an assumption, the Vogel formula is
  written. Good.
- "Two checks then say the result is the real glass." [G] Overclaimed. The 84.1 vs 85 mm check tests the outer silhouette,
  fine. The volume check cannot confirm the cavity: the assumed wall thickness moves the brim volume by about 2πR × 152 mm
  ≈ 38 mL per millimetre, and the 8 ± 3 mm floor by another ≈ 8 mL per mm. With a 3 mm wall the brim volume would be ≈ 566 mL.
  So "603.7 mL to the brim" is a consequence of the 2.0 mm assumption, not a test of it. And "a pint glass must hold its pint
  with room to spare" is unsourced; the glass is listed as CE marked 568 mL [8], which a reader may take for a brim measure
  holding 568 mL at the brim. Say what the volume shows and what it cannot, and give the effect of the wall assumption on the
  frequency (f ∝ R^(−1/2): ±1 mm of wall is about ±1.3 % in f₁).
- Figure 1: label "widest: 84.1 mm across, Z = 120 mm"; caption "the widest point 121 mm up". Pick one. [S]
- Blender appears twice (abstract, here) only as a volume cross-check; a reader may wonder what role it plays (the 3D view's
  mesh?). Half a sentence. Minor.
- Numbers check: ν = 2.05 × 10⁻⁶ m²/s, M_f = 2.72 kg/m², Vogel ratio 0.688 (31 % fall), 96-gon factor and 0.4 mL.

**Verdict: needs work, small** (the volume "check", Fig. 1 label vs caption).

### 3 · A fluid in a moving glass

- The train-and-coffee lead, the lab-frame step "written in the room and then with ρẍ_g moved to the right-hand side", the
  meaning of every term of (1), the small-box picture of ∇·u = 0, the units of Ψ: all now there and good.
- Key result box: "the flow runs downhill on the landscape φ" is wrong (A1.1).
- "The model in one place": a good addition; "depth over wave length λD" is wrong and λ is undefined here (A1.2). κ₁₁ and ζ₁₁
  are also used before definition; the box says so ("Each is defined where it first appears below"), which is acceptable.
- ∇ and ∂ never introduced for S (A2).
- ★ curl part: complete for G (division by ρ, the identity, curl and Laplacian commuting, settled pint, Stokes solution).
- "the distance vorticity diffuses in a time 1/ω" (δ = √(2ν/ω)) is a factor √2 loose against √(νt); acceptable as an order of
  magnitude, and the exact Stokes statement precedes it.
- δ = 0.45 mm, 1.1 % of R: checks.

**Verdict: needs work, small** (the "downhill" sign, "wave length λD", one sentence introducing ∂ and ∇).

### 4 · Linear sloshing in a straight glass

- The z origin now moves with a sentence that says so; the three boundary conditions read well; the steady-push check
  (tan α = ẍ_g/g, "the coffee on the braking train") is the best new paragraph in the note for S.
- "the page warns when the wave at the wall exceeds a fifth of the radius" (and sec. 9: "our choice of a safe bound") [G]:
  for mode (1,1) a wall amplitude of R/5 means a surface slope of about a·k ≈ 0.2 × 1.84 ≈ 0.37 near the wall, which is not
  small. "Safe" needs a reason, or the bound should be stated as the slope it corresponds to.
- "Where (7) comes from ★": steps shown, Y_m dismissed with a reason. Z(z) clashes with Z the height (A3).
- "J_m … behaves like a cosine whose swings weaken as r grows": fine for S (J₁ starts at zero like a sine; "a wave whose swings
  weaken" would be exact).
- The nodal-circle count is now correct (n − 1 for m ≥ 1, n for m = 0).
- Example 4.1: numbers check (0.500 L, 46.03 m⁻¹, 0.9998, 21.25 rad/s, 3.382 Hz; tanh 3 = 0.995 → 0.25 %). The example uses
  the criterion on kD and then "in our pint λD = 6.1": one clause that λ ≈ k when deep. [S]
- Key result (pendulum of length R/1.84 ≈ 21 mm): checks, and is the right picture.

**Verdict: needs work, small** (the one-fifth bound, the Z and n clashes).

### 5 · The real glass, by finite elements

- The FEM part is now ★ with a plain restatement before it; the axis condition, the surface radius R = R_i(Z_s), the element
  type (two quadratic triangles per cell) and the 16-fold convergence are all in. Good.
- Head term: the dimension error and the skipped "differentiate in time" (A1.3).
- Surface tension: "For a mode it multiplies η by λ² (exactly so in a straight glass, approximately in the tulip)" [G]. Not
  exact in a straight glass of finite depth: there −∇²_h η = k²η, and λ² = k² tanh² kD. The standard result is
  ω² = (gk + σk³/ρ) tanh kD, which equals (gλ + σλ³/ρ) only when tanh kD = 1. Here tanh = 0.9998, so the number is unaffected;
  say "exactly so in a deep straight glass". Also the sign: the extra pressure is +σλ²η for a mode (the text says "multiplies
  η by λ²", which leaves S to work out that −∇² turns into +λ²).
- "What the tulip shape does": the with-head comparison is now labelled. The INFERENCE ("more room to swing … a heavier bob")
  is plausible but hand-waved [G]; the natural argument is already on the page: by (10) λ is a ratio of kinetic to potential
  energy (a Rayleigh quotient), so a shape that lets the same surface motion carry more kinetic energy has a lower λ. One
  sentence would turn the inference into a derivation.
- "Below the widest point the wall leans outward as it rises": true only between the waist (27 mm) and the widest point;
  harmless for fills ≥ 300 mL, but say "between the waist and the widest point".
- Figure 2: legend "same a and D" (A3). Caption sentence "about 12 mm above the widest point of the glass, where the tulip's
  wall is vertical (dotted line; the surface reaches it at 415 mL)" parses as if the wall were vertical at 475 mL. Split it:
  "The dotted line marks the widest point (wall vertical), reached at 415 mL; the curves cross 60 mL later, …". [S]
- "agree … to 3 × 10⁻⁵ … and to 3 × 10⁻³": relative errors, presumably; say so.
- Numbers check: σλ²/(ρg) = 0.0102, 3.427 → 3.445 → 3.244 Hz, κ₁₁ = ε_f h_f λ = 0.128.

**Verdict: needs work, small** (A1.3, "exactly so", Fig. 2 legend and caption).

### 6 · Driving the modes: hand and shaker

- The projection now shows ẍ_g x = ẍ_g r cos θ and the θ-integral that keeps m = 1 only; the sign of (12) is interpreted; ζ is
  defined in the unstarred part; Ω_h = 22 rad/s and its 54 % transmission are given; the heel-strike picture for harmonics is
  there. (12) checks: projecting (6) with the head term gives ä(1 + κ)/λ + g(1 + z̈/g)a = −Qẍ.
- "Put both sums into (6)": the head term of section 5 must be in (6) for the 1/(1 + κ_n) of (12) to appear; say "(6) with the
  head term of section 5". [S]
- "orthogonal on the surface (a consequence of (10) being symmetric)": points into ★ (A2).
- Checks paragraph: the derivation of Q = 2R/(ξ² − 1) checks. Then "reproduces it to six digits, in the form
  2R/((ξ² − 1)J₁(ξ)) = 0.057528 m that belongs to the scaling ψ = J₁(kr)" [both]: the note's own scaling is ψ = 1 at the wall,
  for which Q = 2R/(ξ² − 1) = 0.033473 m at R = 40 mm. Quoting the number in another scaling is a detour that makes S think
  there are two Q's. Quote 0.033473 m.
- "with ä = ȧ = 0, (12) gives a_n = −Q_n ẍ_g/g (head aside)": the head does not need to be set aside; λ/(1 + κ) divided by
  ω² = gλ/(1 + κ) cancels it exactly (σ aside). [G] "93 % of the tilt at the wall": the cylinder gives 0.837 + 0.073 + 0.028 =
  0.938, consistent.
- Resonance: the balance 2γωa = λQAω²/(1 + κ) is now shown. "The damping ratio ζ_n = γ_n/ω_n … measures how much of its energy
  a mode loses per radian of swing" [G]: the energy falls by 2γ per unit time, so per radian the fractional energy loss is
  2ζ; ζ is the fractional *amplitude* loss per radian. Fix the word.
- Example 6.1 [S]: the reader cannot reproduce 5.6 mm, because Q₁₁ of the tulip is never quoted. Give it and do the
  arithmetic: a = λQAω/[2γ(1 + κ)] = 47.27 × 0.03245 m × 0.2 mm × 20.38 s⁻¹ / (2 × 0.497 s⁻¹ × 1.128) = 5.6 mm (checks).
  Also say where "28 times" comes from: 1/(2ζ) ≈ 20 times the push factor λQ/(1 + κ) ≈ 1.36.
- ★ Faraday: the averaging is now shown and checks (Ṗ, Ṡ, ⟨sin² cos²⟩ = 1/8, A > 4ζg/Ω² = 0.58 mm, ε = 0.339, growth
  1.73 − 0.50 = 1.23 s⁻¹). The "tenfold fall" explanation is now right for how the page seeds: the code starts every mode at
  rest (velocity 0) and the drive at phase 0, so the seed is pure P. "Its strongest instability lies at Ω = 2ω" is asserted;
  the averaging shows instability there but not that it is the strongest (the widest tongue at small ε). Half a clause or a
  citation (Landau & Lifshitz, *Mechanics*, §27). [G]
- Missing everyday picture for pumping [S]: a child on a swing who stands and squats twice per swing pumps it exactly this
  way; STANDARD item 1 names the swing.
- "The hand": "reaches the glass at Ω_h²/(Ω_h² + ω²)" [S]: the modulus of the critically damped follower's response,
  |Ω_h²/(Ω_h² − ω² + 2iΩ_hω)| = Ω_h²/(Ω_h² + ω²), is stated without the line that gives it. Checks: 484/899 = 0.54.

**Verdict: needs work, small to moderate** (ζ "energy per radian", Example 6.1 not reproducible, Q quoted in a foreign
scaling, Faraday threshold only in ★, head term in the projection).

### 7 · Where the energy goes

- Energy method (14): clear. ★ Stokes layer: every step shown and correct; (15), (16) check; I_w/E = 1.837/R and the Δ₁₁ line
  (3.50) now show the missing step from round 1.
- "Dividing by 2E and using Green's identity ∫|∇Φ|²dV = λ∫ψ²dS for the energy" and then "Here E stands for ∬|∇Φ|² r dr dz"
  [G]: Green's identity is mentioned but not used in what is printed. Either say the program evaluates E as λ∫ψ² r dr, or drop
  the identity. "the energy (14)": E is defined in the sentence before (14), not in it.
- The skin: I_s defined; c_s = 1 marked OPINION. Good.
- ★ Interior: the surface-integral step is shown, 0.009 s⁻¹ and 2 % check, 1.88 vs 2 is 6 %. "the damping of waves on deep open
  water": a classic result, uncited (Lamb, *Hydrodynamics*, §348–349; Landau & Lifshitz, *Fluid Mechanics*, §25). Subscript b
  clashes with I_b (A3).
- Contact line: the rate transfer and the possible double count are now discussed honestly. "No first-principles formula for
  a stout under a head exists" [G]: a universal negative; "none is known to us" is what can be said.
- The head: the INFERENCE paragraph reconciles the lifted mass (sec. 5) with the 1/λ-deep friction layer. Good. The saturating
  factor uses λ where Sauret et al.'s depth is 1/k; say λ ≈ k for a deep mode. "the much finer bubbles of a stout's head" and
  "it could be off by a factor of three either way" are unsourced and untagged; tag the second OPINION. γ_f = 0.232 s⁻¹ checks.
- Figure 3: subscripts render; numbers sum (0.496 ≈ 0.497). Caption: "The table in the panel beside the figure" means the data
  panel beside the simulation, not beside Figure 3; say "beside the simulation". [S]
- Key result: 2.0 s, 6.0 s, 3.7 s, 11.1 s, 8.9 s check; "walls and the interior" now correct.
- Closing invitation (film a pint, count the swings): good.

**Verdict: needs work, small** (Green's identity line, "no formula exists", untagged factor-of-three, Fig. 3 caption).

### 8 · The velocity field in the cut

- Clear and physical. 480 mL is explained, the rings are explained, d is defined, 1/λ = 21 mm and 63 % check. "Laplace's
  equation trades variation along the surface for variation with depth" remains the best sentence for S.
- "The figure under the glass" (first sentence) vs "Figure 4" two paragraphs later: S may think they are the same. Say "the
  cut under the 3D view".
- Figure 4: arrows in the top centimetre are still dense and small at 1440 px; directions are readable only with effort.
  Minor.

**Verdict: clear, leave it.**

### 9 · On the screen, and what is left out

- Lead paragraph now present. Numerical method: integrator, order, step, why RK4, stability limit, per-step phase error
  (0.04⁵/120 ≈ 8.5 × 10⁻¹⁰), measured error over 8 s (5 × 10⁻⁸), the 50 ms cap and what it means, the reason for keeping
  m ≠ 1 modes: all there. (1,3) is indeed the fastest kept mode (40.4 rad/s on the page). This part meets item 5.
- Equation to screen: complete for the readouts. "'Head top to rim, now' is the rim height minus the highest point of the
  head, Z_s + η_max + h_f": the formula is the highest point, not the difference; write 160 mm − (Z_s + η_max + h_f). [S]
- Where the drawing differs: good.
- Limits: the glass tilt is now named; "the bending of the resonance curve" added. The swirl is still unsourced [G]
  (e.g. Miles, J. Fluid Mech. 149, 1984; Royon-Lebeaud, Hopfinger & Cartellier, J. Fluid Mech. 577, 2007, which the authors
  should open before citing). The one-fifth bound: see section 4.
- "Reproducing the numbers": `tools/fig12/` is named but not linked; the site is public and the repository is on GitHub, so
  a working link is possible (STANDARD item 8: "each with a working link").
- Problems: Problem 4 is now the right question (the head detunes f₁ toward 2 × 1.6 Hz and can make the slosh larger).
  Problem 3 depends on (13), which only ★ readers have seen (A2).
- Sources: every entry has a link and an honest reading note. Still no textbook chapter for the textbook physics the note
  uses (Stokes layer, deep-water damping 2νk², Mathieu instability, Bessel modes), which STANDARD item 8 lists first.
  [5] abstract only, [6] secondary, Keulegan abstract only and [11] "read in part" are honestly labelled; the specific claims
  they carry are now worded as "the abstract reports". Acceptable, but one opened textbook would strengthen section 7 most.

**Verdict: needs work, small** (head-to-rim formula, swirl source, link to the scripts, a textbook in the sources).

---

## C. Round-1 points, one by one

R = resolved, P = partly resolved, U = unresolved, n/a = outside the note.

| Round-1 point | Now | Status |
|---|---|---|
| A1 stated reader vs unstarred maths | byline rewritten; FEM, separation, interior now ★; terms of (1) explained; but ∂ and ∇ never introduced, and unstarred sec. 6 leans on ★ (10) | P |
| A2 ★ rule: Key result and (5) inside ★ | both now in the unstarred part "The flow outside the layers" | R |
| A2 ζ defined only in ★ | defined in unstarred "Resonance and the damping ratio" | R (new gap: threshold (13) only in ★, see A2 above) |
| A3 ω vorticity vs frequency | vorticity is now **w** | R |
| A3 z with three origins | z fixed to the glass, origin move announced in sec. 4, glass position z_g | R |
| A3 ẍ vs x | glass acceleration ẍ_g throughout | R |
| A3 a, A, f, μ, k, U reused | radius R, amplitude C, shape ψ_n, added mass κ_n, index j, c_f, u_f | R (residue: "a" in Fig. 2 legend; new clashes Z, n, b, C, P/S/E) |
| A3 λ used before definition ("kD = 6.1") | Example 4.1 now after (8); but the model box uses λD before (8) and calls it "wave length" | P |
| A4 model never stated in one place | "The model in one place" box with the dimensionless numbers | R (but A1.2) |
| A5 "the brief", repository paths as citations | gone; only `tools/fig12/` in sec. 9, not as a citation | R |
| A6 steady-tilt check, dimensional check | tilt check added; units of Ψ and Q stated; no dimensional check of a derived equation | P |
| §1 "imperial" | "20-imperial-ounce" | R |
| §1 controller "later chapter" vs header | "the next chapter of this figure"; header outside the note | R / n/a |
| §2 wall thickness from a silhouette | now an assumption, stated as such | R (but the volume "check" now overclaims, see §2) |
| §2 "lined glass" unsourced | removed; replaced by "a pint glass must hold its pint with room to spare", also unsourced | P |
| §2 "smoothed to 0.2 mm" | spline tolerance explained | R |
| §2 Vogel equation not written | written | R |
| §2 h_f "firm enough" on a snippet | "read only in part. Fairly sure." | R |
| §2 Fig. 1 label contrast | label moved outside the stout | R (new: 120 vs 121 mm) |
| §3 "weaker when it is lowered" wrong | "weaker when it accelerates downward" | R |
| §3 lab-to-glass step | shown | R |
| §3 terms of (1) | each explained | R |
| §3 ∇·u picture | small box | R |
| §3 Ψ units and meaning | J/kg = m²/s², effective gravity | R |
| §3 "faster than free fall" | "accelerated downward faster than a falling stone" | R |
| §3 ★ curl steps | division by ρ, identity, commuting stated | R |
| §3 "settled pint" | said, with the bubble circulation | R |
| §3 δ "in one period" | Stokes solution, "in a time 1/ω" | R |
| §3 C(t) absorbed: why | half sentence added | R |
| §4 "moving the constant into φ" | "everything that depends on time alone" | R |
| §4 wave slope defined | yes | R |
| §4 separation of variables, Bessel | ★ part with Laplacian, Bessel's equation, Y_m; picture of J_m | R |
| §4 e^{iωt} vs cos ωt | cos throughout | R |
| §4 elimination and (8) steps | shown | R |
| §4 nodal circles wrong | corrected | R |
| §4 no picture of modes | m = 0, 1, 2 described; pointer to the 3D view | R |
| §4 D = 99.5 mm unexplained | holds 0.500 L (implicit); sec. 5 still uses a second, 100 mm cylinder | P (minor) |
| §4 "kD > 3" reason | tanh 3 = 0.995, 0.3 % | R |
| §5 FEM part unstarred | ★, with plain restatement | R |
| §5 λ = ω²/g origin | "the last condition is ∂²_tφ + g∂_zφ = 0 … with φ ∝ cos ωt" | R |
| §5 axis condition | Φ = 0 on the axis for m ≥ 1 | R |
| §5 upper limit of (10) | R = R_i(Z_s) | R |
| §5 element type | two quadratic triangles per cell | R |
| §5 convergence factor | 16-fold, fourth order | R |
| §5 with-head numbers unlabelled | "With 18 mm of head on both" | R |
| §5 surface tension picture; λ³ exact only for cylinder; contact-line condition | drum skin; "slide freely"; but "exactly so in a straight glass" is still exact only when deep | P |
| §5 step to (11) skipped | step written, with a unit error (A1.3) | P |
| §5 μ_f reuses μ | κ_n | R |
| §5 eq. (9) collides at 390 px | narrow layout now wraps (9) into four lines, no overlap; the break after "−" is awkward but readable | R |
| §6 m = 1 selection | ẍ_g r cos θ and the θ-integral shown | R |
| §6 sign of (12) | interpreted | R |
| §6 "of the brief", J₁(ξ) normalisation | "brief" gone; the other scaling is now named but still quoted instead of the note's own | P |
| §6 resonance step | shown | R |
| §6 ★ averaging not shown | shown | R |
| §6 ε ≪ 1 vs ε = 0.34 | said, with the measured 1.21 s⁻¹ | R |
| §6 "tenfold" explanation | rewritten for a seed at rest; the page does seed at rest with the drive at phase 0, so it now holds | R |
| §6 Faraday 1831 unsourced | sentence removed | R |
| §6 Ω_h never given | 22 rad/s, 54 % at the slosh frequency | R |
| §6 harmonics of walking | heel-strike picture | R |
| §6 stage caption without 1/(1 + μ_f) | caption now prints −λ_nQ_n/(1 + κ_n) ẍ_g, identical to (12) | R (n/a for the note) |
| §7 Miles abstract-only carrying claims | now "the abstract of Miles's paper reports" | R |
| §7 I_s undefined | defined | R |
| §7 c_s = 1 from abstract-only source | OPINION | R |
| §7 bulk: e_ij e_ij, 2νλ² step, Lamb | ★, explicit sum, step shown; still uncited | P |
| §7 contact-line rate transfer, double count | both discussed | R |
| §7 head saturation vs rigid layer | INFERENCE paragraph | R |
| §7 stout bubble size unsourced | still unsourced ("much finer bubbles") | U |
| §7 Fig. 3 raw underscores and units | real subscripts, s⁻¹ | R |
| §7 "clean walls alone" | "walls and the interior" | R |
| §8 why 480 mL | caption and sec. 9 | R |
| §8 when rings appear | explained | R |
| §8 d undefined | defined in the caption | R |
| §8 small arrows | unchanged | U (minor) |
| §9 no lead | lead added | R |
| §9 why RK4; measured error; 50 ms meaning | all added | R |
| §9 why m ≠ 1 modes kept | explained | R |
| §9 readout mapping | "Equation to screen" | R (one formula wrong way round, see §9) |
| §9 swirl and one-fifth unsourced | one-fifth now "our choice"; swirl still unsourced | P |
| §9 "perfectly smooth" | removed | R |
| §9 glass tilt missing | named | R |
| §9 Problem 4 false premise | rewritten correctly | R |
| §9 Problem 3 "2 f₁" in text | maths | R |
| §9 sources quality, no textbook | honest labels; still no textbook chapter | P |

Of the 83 round-1 points in this table: 70 resolved (two of them, the page header and the stage caption, lie outside the note), 11 partly resolved, 2 unresolved (both minor).

---

## D. Verdicts

| § | Title | Verdict | Main reasons |
|---|---|---|---|
| 1 | Carrying a pint | clear, leave it | (box's "Everything else is derived" is fixed by tagging elsewhere) |
| 2 | The glass and the stout | needs work, small | the volume "check" depends on the assumed wall; Fig. 1 120 vs 121 mm |
| 3 | A fluid in a moving glass | needs work, small | "runs downhill" is the wrong sign; "depth over wave length λD"; ∂ and ∇ never introduced |
| 4 | Linear sloshing in a straight glass | needs work, small | the R/5 "safe" bound is slope ≈ 0.37; Z and n clashes |
| 5 | The real glass, by finite elements | needs work, small | unit error in the head step to (11); "exactly so in a straight glass"; Fig. 2 legend "a" and caption sentence |
| 6 | Driving the modes | needs work, small to moderate | ζ "energy per radian" off by 2; Example 6.1 needs Q₁₁; Q quoted in a foreign scaling; threshold (13) only in ★; head term in the projection unsaid |
| 7 | Where the energy goes | needs work, small | Green's identity line; "no formula exists"; untagged factor-of-three; Fig. 3 caption "beside the figure" |
| 8 | The velocity field in the cut | clear, leave it | "the figure under the glass" vs Figure 4, minor |
| 9 | On the screen, and what is left out | needs work, small | head-to-rim formula; swirl unsourced; scripts not linked; no textbook in the sources |

The note has improved a great deal since round 1: the structure, the ★ layering, the model box, the checks and the numerical
section now meet the standard, and every number I recomputed reproduces. What remains are three real errors (the "downhill"
sign, λ called a wavelength, the unit slip in the head term), a few one-sentence gaps for S (∂ and ∇, the Faraday threshold
outside ★, the Q₁₁ value), and a handful of claims that need a tag or a source. All are sentence-level fixes; no section
needs restructuring.
