# Referee report · Project 07, Chapter 4 "The lens" (`#ch04`)

Read as two people at once: a school student who is good at mathematics, and a physics graduate who designs electron-optical
columns and is reading this as a job applicant's portfolio. Only Chapter 4 and its simulation `#sim-ch04` were read.

**How it was read (9 November 2026).** The page was built with `python3 portfolios-src/electron-beam/build.py --site --out
<scratchpad>`. The page changed while I was reading it: commit `e113ab0` ("chapter 4 fixes after its derivation check")
arrived during the review. Everything below was re-checked on the second build, which is byte-identical to the served
`public/portfolios/electron-beam/index.html` ("6 of 10 chapters, 82 equations"; `cmp` reports no difference). The page was
served from `public/` and opened in headless Chromium (Playwright) at 1400 px and 390 px, and at device scale 2 for the
simulation. Chapter 4 has no folds: sections 4.1 to 4.8 and the simulation all render open. Each was screenshotted whole.
There were no console errors at either width. KaTeX was read from the rendered `aria-label`s. The simulation was driven
through its four sliders (nine settings, listed under "Simulation"). I also called the page's own module
(`EB.ch04.compute`) and scanned 1 728 slider settings with it. "Recomputed" numbers are mine: I wrote an independent SciPy
solver (adaptive RK45 at rtol 1e-12; CODATA constants) for the Glaser paraxial ray, the focus condition, M, the rotation,
the C_c integral and the C_s integral (4.11). `PLAN.md` and the check files were not read.

**Fixed while I was reading.** The first build said "it is outwards where B rises and inwards where it falls". That has the
sign of B_r = −rB′/2 backwards. The current text reads "it points inwards where B rises along z". The pointer of
Problem 1 (from (4.9) to (4.8)) and the 10⁻⁷ / 10⁻⁹ mismatch with the code were fixed too. Those three findings are not
repeated below.

Verdicts are against `notes/STANDARD.md`, section 4 (1 picture, 2 model, 3 derivation, 4 checks, 5 numerical method,
6 equation to screen, 7 limits, 8 reading). They also apply Numa's verdict of 21 October 2026: Taylor's way, every step
shown, every symbol defined where it first appears, one symbol one meaning, and the results of a ★ passage restated
unstarred.

**What is good, first.** Every number in the chapter reproduces. My independent solver gives NI = 345.8 A,
B₀ = 69.166 mT, k² = 0.5255, ω = 1.2351, f = 3.6691 mm, M = 0.01803 (1/M = 55.47), θ_rot = 1.8438 rad = 105.6°,
C_c = 2.84759 mm and C_s = 4.18897 mm. At 30 kV it gives NI = 2147.8 A, a factor 6.21052. At WD = 5 mm it gives C_s = 12.912 mm,
C_c = 4.650 mm and f = 5.295 mm. At a = 1 mm, WD = 2 mm it gives C_s = 3.788 mm, C_c = 1.845 mm and NI = 294.6 A. The page's
module gives C_s and C_c the same to 10 digits at 100 V, 800 V, 5 kV and 30 kV, as the B²/V\* scaling demands. The field
expansion (4.2), the Busch algebra and the step to (4.7) are correct. So are the asymptotics of Glaser's solution and the
weak-lens limit. The C_c perturbation integral and its agreement with the solver are a real, well-chosen check. The chapter
is in good shape on algebra and arithmetic. What it lacks is mostly physical: what the numbers mean for a real objective.

---

## The ten most serious places

1. **4.5, Example 4.1 and the simulation's f readout: the wafer sits inside the lens field, and the chapter never says
   so.** "the wafer 3 mm behind its centre … The focal length is f = 3.669 mm, 1.83 times a." The student is told that a
   lens of focal length 3.67 mm images an object 200 mm away onto a plane only 3.00 mm behind the lens centre, and is
   not told how that can be. Recomputed: the asymptotic focal point lies at z_F = −f cos(ωπ) = 2.713 mm. The image-side
   principal plane lies at −0.956 mm (the principal planes are crossed). The thin-lens equation from these cardinal
   elements puts the image at 2.78 mm, not 3.00 mm. The reason is that B(WD)/B₀ = 1/(1 + 1.5²) = 0.31: the wafer sits in
   21 mT, a third of the peak. This is an immersion objective. Its asymptotic f (4.9) is not the focal length that sets
   the image, because the ray never leaves the field. A column designer sees this at once. It also has consequences the
   chapter does not mention: the field at the specimen, the rotation continuing past the wafer, and the secondary-electron
   paths. The simulation then shows "f = 3.67 mm" beside "WD = 3.00 mm" with no comment. One paragraph is needed: f is
   the asymptotic focal length measured from the principal plane; the wafer is in the field; here is what that means.

2. **Simulation: when focusing is impossible it fails silently, and the caption still says it succeeded.** `focusB0`
   brackets the bisection at k² ≤ 3 (ω ≤ 2). When focusing needs more than that, it returns the bracket end. At
   a = 20 mm, WD = 0.50 mm, u = 10 mm, the panel shows "NI 827 A, f 8.00 × 10¹⁰ mm, C_s 16.8 mm, M 1.57". The drawn ray
   crosses the axis before the wafer and misses it (screenshot `sim-w1400-a20_wd0.5_u10.png`). At a = 20 mm, WD = 20 mm,
   u = 10 mm it shows "M 2.53" and "C_s 303 mm" for a lens that is not focused at all. The caption still says "The
   excitation NI is solved so that the ray meets the axis at the wafer." Of 1 728 settings on a 12 × 12 × 12 grid over the
   slider ranges, 117 (6.8 %) are pinned at ω = 2. 827 A is exactly the answer to Problem 1. In those cases C_s, C_c and M
   are numbers about nothing. The panel must say "no focus" or limit the sliders. And "M" is called a demagnification
   in 4.8, yet it reads 1.57 here.

3. **The slider "V_land … (after any retarding field)" contradicts the model, and so does the hand-over.** The lens is
   computed with η = e/(8mV\*) at the landing voltage. With a retarding field the electrons pass through the objective
   at the column voltage and slow down only after it. That is the whole point of chapter 3's Example 3.2 (5 kV in the
   column, 800 V at the wafer). So either the slider means "the beam voltage inside the lens, with no retarding field", or
   the computation is wrong for the case its label names. Example 4.3 then concludes "at 800 V the chromatic blur
   dominates, which is why low-voltage columns care so much about the energy spread". It never says that the standard
   remedy, which chapter 3 itself introduced, is to *not* run the objective at 800 V. 4.8 hands chapter 5 "the landing
   voltage of chapter 3" as though it were the lens voltage.

4. **4.2: Ampère's law is applied with B where it needs H, and the conclusion about iron is wrong.** "close the loop far
   away, through the iron or outside, where the field is negligible … Real lenses lose some of NI in the iron and
   saturate at large excitation; (4.4) is the ideal of iron with infinite permeability." Inside the iron B is large. It
   is H that is small, and only when μ → ∞. Close the loop instead at infinity, which needs no iron at all.
   ∮H·dl = NI then gives ∫B_z dz = μ₀NI over the whole axis *exactly*, whatever the permeability and whatever the
   saturation, as long as the axis runs in vacuum. Iron losses and saturation do not reduce the integral. They change
   the *shape* of B(z): the field broadens, a grows, and B₀ = μ₀NI/(πa) falls through a. This is a standard result, and
   a lens designer will check it.

5. **4.3: the derivation covers only meridional rays, but the Key result claims all paraxial rays.** The radial equation
   is derived for electrons with p_θ = 0, in polar coordinates (r, θ). The Key result then states, for every paraxial ray,
   "In the frame turning at the Larmor rate eB/(2γm), paraxial rays obey r″ = −ηB²r". Skew rays, for example rays from
   an off-axis object point, have p_θ ≠ 0. The step that covers them is missing: in the frame rotating at the Larmor
   rate, the Cartesian coordinates X and Y each obey X″ = −ηB²X. That step is also what gives the image rotation the text
   asserts ("The image is therefore rotated"). Next, "Here r is the distance from the axis measured in the frame that
   turns with the electron." A distance from the axis does not depend on the frame. And r can cross zero (Example 4.1),
   which a polar radius cannot. What obeys (4.7) is the signed rotating-frame coordinate X. Finally, "every ray through
   the same axial point at the same small angle behaves the same way, scaled" says the opposite of what linearity
   gives: rays from one axial point at *different* small angles are scaled copies, and so they meet at one image point.

6. **4.4 ★: the key step of Glaser's solution is missing, and the starred results are used unstarred.** "Glaser's
   substitution z = a cot φ … turns the equation into one with constant coefficients." It does not. One also needs
   r = y/sin φ, after which y_φφ + ω²y = 0. Without it neither the student nor the graduate can reproduce (4.8), and
   "check L6 confirms the equation symbolically" replaces the step. The whole section is starred. Yet k², ω, (4.9)
   and the thin-lens formula 1/f = η∫B²dz are used in Example 4.1 ("ω = 1.235, k² = 0.525"), in the simulation's f and
   in the Problems. The unstarred Key result box of 4.3 restates none of them. A reader who skips ★ meets ω undefined.
   Also, f is not said to be measured from a principal plane (see item 1).

7. **4.6 and the chapter as a whole: sources (STANDARD 8).** "For C_s the textbook aberration integral, as quoted from
   Hawkes and Kasper in the lens-design literature (we did not open the book), is (4.11)". For a portfolio this is the
   worst sentence in the chapter. It names a book without an edition, chapter or page. It cites "the lens-design
   literature" without naming any paper. And it tells the reader the author did not read the source. The numerical
   agreement (4.18897 against 4.18897 mm) shows the formula is right, so the fix is to cite a text that was actually
   read (for example Reimer's *Transmission Electron Microscopy*, or Hawkes & Kasper vol. 1, with the chapter). Busch's
   theorem has no citation. Glaser (1941) and Scherzer (1936) are cited inline without a title, DOI or link. The chapter
   has no `.prefs` reference list.

8. **4.6 ★: the C_c "short proof" skips its only real step, and the C_s mechanism is half told.** "Changing η by −ηδ adds
   a source term to (4.7); the response at the image, found with the Green's function built from h and a second ray, is
   Δr = δαη∫B²h²dz." The second ray is never defined. The Wronskian that normalises the Green's function is never
   written. The result is stated, not derived, and a student cannot do this step alone. Two to four lines would do it
   (variation of parameters with h and a ray g having g(image) = 1). Separately: "A real ray at angle α feels the higher
   terms of (4.2)". The B⁴h⁴ term of (4.11) does not come from the field expansion. It comes from the non-linear
   kinematics, that is, the rotation and ż ≠ v at large angle. Saying only "higher terms of the field" misleads the
   graduate. The integration limits of (4.11) (object to wafer, the field past the wafer cut off) are not stated either.

9. **Example 4.3 and Example 4.2: two claims a column designer would correct.** (a) "For a beam of 5 mrad … at 800 V the
   chromatic blur dominates". At 800 V, λ = 43.34 pm, so λ/α = 8.67 nm and 0.61λ/α = 5.29 nm at 5 mrad (recomputed).
   Diffraction is larger than both the chromatic miss (3.83 nm) and the spherical miss (0.52 nm). The sentence is true
   only between C_s and C_c, and should say so. (b) "Real lenses differ here, because the iron saturates near a tesla."
   Soft iron saturates near 2 T, and FeCo pole pieces near 2.3 T. And the lens of Example 4.2 needs only B₀ = 0.430 T on
   the axis at 30 kV (recomputed). The sentence implies that this lens is affected at 30 kV, and it is not. Give the
   pole-tip field that limits real objectives, and say at what excitation this geometry would reach it.

10. **Figure 4.1: the iron circuit is drawn closed, and the picture the text describes is not in it.** The yoke is a
    closed rectangle around the coil, with one stub per side pointing at the axis. There is no break in the bore wall.
    A closed iron shell keeps the flux inside the iron, so the figure does not show the one thing that makes a lens:
    the gap through which the flux leaks onto the axis. A real pole-piece lens has two pole pieces separated along z,
    with the gap between them. The 4.1 text is about field lines that "converge towards it, and on the way out they
    spread", about B_r, about the azimuthal kick and the electron's turning. None of these is drawn: no field line, no
    B_r arrow, no electron path. The labels collide: "B(z), largest in the gap" runs through the yoke outline ("larg|est
    in"), and "field lines leave the iron at the gap and cross the axis region; the lens is the gap" runs across the
    lower yoke and coil ("ir|on", "t|he lens"). At 390 px the label text is 8 px high and cannot be read (measured).

Close behind:
- 4.8 claims "none changes the scaling laws found here". Example 4.2 itself says saturation breaks B₀ ∝ √V\*, and a
  retarding field overlapping the objective changes C_c greatly.
- "the demagnification M that turns the virtual source into a source image" (4.8) conflicts with 4.5. There the
  objective's object is already "a small source image (or a crossover)", and M = 0.018 is a magnification, not a
  demagnification.

---

## Section by section

### Chapter lead
- "Maxwell\\'s equations", "Busch\\'s theorem", "Glaser\\'s bell-shaped lens" render with visible backslashes at every
  width ("Maxwell\'s"). It is the same build escaping bug as in chapter 3, in the first lines the reader sees.
- "the field lines that bulge out of its gap first twist the electron" is a fair one-line summary.

**Verdict:** needs work (typo bug).

### 4.1 From the helix to a lens
- The opening from the helix of §1.7 is good. A uniform field images point to point, a short field gives a short kick,
  and a kick proportional to r is a convex lens. This meets STANDARD 1.
- "a uniform field images a point onto a point". It is worth saying that the image is at unit magnification. That is the
  second reason a long solenoid is useless as an objective, and it sets up why the objective of 4.5 demagnifies.
- The current text (after `e113ab0`): "on the way into the gap they converge towards it, and on the way out they spread
  again". This is correct now. "Converge towards it": "it" reads as "the gap", but what is meant is "the axis". Say "the axis".
- "The twist comes first, and the twist turned by the axial field is the focusing push." Good, and it is the right
  physical picture. But it needs Figure 4.1 to show it (item 10).
- "That is exactly what a convex glass lens does to light". It does, except that a glass lens does not rotate the
  image. One clause ("…and, unlike glass, it also turns the image; §4.3") would prevent a surprise later.
- Figure 4.1: item 10.

**Verdict:** needs work (figure).

### 4.2 The field near the axis
- The series expansion is complete, and each order is shown. A school student can follow it. Recomputed: c₁ = −B′/2,
  b₂ = −B″/4, c₃ = B‴/16 are all correct.
- "One more order of each gives c₃ = B‴/16". Only c₃ is given. b₄ = B⁗/64 appears in check L2 but not in the text or
  in (4.2). Either give both or say "one more order of the first equation".
- "the one function a lens designer measures or computes". A good sentence.
- Glaser's field: "It is a fair description of a real pole-piece lens". This is unsupported. The bell's 1/z² tails are
  much longer than the near-exponential fall-off of a real pole-piece field. That matters here, because the object is
  at 100a and the wafer at 1.5a. Give a source, or one sentence on where the bell fits and where it does not.
- Ampère and the iron: item 4.
- (4.4) uses N and I, but neither is defined before "the current enclosed by N turns carrying I". That is fine. The
  unit of NI ("A", ampere-turns) is not said, though the student will see "346 A" and think of the coil current.

**Verdict:** needs work (Ampère with B instead of H; the iron conclusion; one unsupported claim).

### 4.3 Busch's theorem and the paraxial ray equation
- The Lagrangian route to p_θ is the natural one (STANDARD 3), and the algebra to r̈ = −(eB/2γm)²r is correct.
  "Half of the magnetic push is used up keeping the electron on its turning path; the other half focuses" is an
  excellent physical sentence.
- One symbol, one meaning: bold **p** = γm**v** + q**A** is the canonical momentum here. Five lines later "p = γmv" is the
  kinetic momentum. In a magnetic lens these differ, and the difference is the subject of the section.
- "the angular component of canonical momentum is conserved: p_θ = γmr²θ̇ + q rA_θ". That is r times the θ-component,
  that is, the canonical *angular momentum* (units J s), not a component of **p**. Name it so.
- (4.5) uses φ (`\varphi`) for the scalar potential in L. 4.4 uses φ for Glaser's angle, and 4.7 uses φ for the
  potential again. Three meanings in one chapter.
- Two display equations (the radial equation of motion and r̈ = …) are unnumbered, against the house rule.
- Meridional and skew rays, "r is the distance … in the frame that turns", and "at the same small angle": item 5.
- "For paraxial rays ż ≈ v". Say why: both the radial and the azimuthal velocities are small near the axis (rθ̇ ∝ r).
- No dimensional check of η: η = e/(8mV\*) has units T⁻² m⁻², so ηB² is m⁻², as r″/r must be. It is one line, and STANDARD 4
  asks for it.
- Key result: "the same lens focuses a beam of four times the voltage at twice the current". Strictly four times V\*
  (at 30 kV the difference is 3 %). The rotation formula is correct (recomputed 1.8438 rad).

**Verdict:** needs work (the skew-ray step; one false sentence about linearity; symbol clashes).

### 4.4 Glaser's exact solution ★
- The missing step r = y/sin φ, and the starred results used unstarred: item 6.
- The asymptotics are right and shown, and the slope, f and the weak-lens limit all check (recomputed). "The square
  explains why a lens cannot tell north from south" is a good physical remark. Add that the *rotation* does change sign
  with the current, since it goes with ∫B dz, not with ∫B².
- "the same NI spread over half the length gives twice the ∫B²". This is correct for a fixed NI and a weak lens.
  Say that it is the weak-lens statement.
- f is defined by the exit slope of a parallel ray, that is, measured from the image-side principal plane. The text never
  says where that plane is. That is the missing piece of item 1: here it lies 0.96 mm *before* the centre.

**Verdict:** needs work.

### 4.5 The objective lens, focused on the wafer
- The operator's picture ("focuses by turning the lens current") and the solver doing the same is a good bridge from the
  model to the code (STANDARD 5).
- "The integration runs in the variable t with z = a tan t". The letter t is time in 4.3 (θ̇ = dθ/dt, ∫θ̇ dt). Use
  another letter.
- Numerical method (STANDARD 5): the number of steps (6000) and of bisections (60) appear only in 4.8. The bisection
  bracket (k² ≤ 3), which is exactly where the method fails (item 2), is not stated anywhere. The step size in z at the
  lens centre for the default lens, and the error to expect, are not given. Check N1 (traced and exact f agree to
  1.4 × 10⁻⁷) is that error and should be quoted here.
- "Liouville's theorem of chapter 3 at one voltage says that the product of the image size and the beam angle is fixed (the
  Lagrange invariant)". Chapter 3's Liouville is about canonical momenta, and in a magnetic field these are not the
  slopes. The clean argument fits in one line and stays in this chapter: the Wronskian h g′ − g h′ of two solutions of
  (4.7) is constant. Using it would also justify that M is read from rotating-frame slopes.
- Example 4.1: all numbers check (recomputed, above). "(by (4.4), μ₀NI/(πa) = 69.2 mT)" repeats the number it has just
  given. The wafer inside the field and f > WD: item 1.
- Example 4.2: the scaling argument is clean and correct (factor 6.21052, recomputed). "the iron saturates near a tesla":
  item 9.

**Verdict:** needs work (item 1; the method is half-described).

### 4.6 Why a round lens is never perfect: C_s and C_c
- The heading renders as "C_s and C_c" with raw underscores, at both widths.
- "as a glass ball does: rays through the rim cross the axis before the paraxial image". This is the right picture.
- Definitions: "δ" is a relative change of V\*, but Example 4.3 uses ΔE/E with E = eV. At 800 V the difference is
  negligible. At 30 kV, dV\*/V\* = (1 + 2εV)/(1 + εV) · dV/V, which differs by about 3 %. Say which convention C_c uses.
- Scherzer's theorem: the statement and conditions are right in substance. Name the "no singularities, fields
  continuous" condition as well, or say "smooth". "No arrangement of coils and iron of that kind can cancel them" is
  good. Note that the solver computes Δr with `Math.hypot`, so it cannot see the *sign* of C_s. Scherzer's positivity
  is quoted, not checked.
- "How we measure them": now clear after `e113ab0` ("the tiny linear part left by the discretisation"). "C₅α⁵": C₅ is
  not named ("the fifth-order coefficient").
- The C_c proof and the C_s mechanism: item 8. The unread source: item 7.
- "★" appears in the middle of the paragraph "How we check them." It does not say where the starred passage ends, so a
  skipping reader does not know whether (4.11) and the paragraph after it are starred.
- "The two methods have nothing in common but the field". The integral uses h from the same paraxial integrator, so
  they share the paraxial ray as well. That is still a good check. Phrase it accurately.
- Example 4.3: the numbers check (0.524 nm, 3.83 nm; WD 5 mm: 12.9, 4.65, f 5.30; a 1 mm: 3.79, 1.84, 295 A,
  recomputed). Diffraction is omitted from "dominates": item 9. "of the order of the focal length, as for most real
  objectives" is plausible but has no source. "0.215 eV spread" does not say whether it is a FWHM, FW50 or rms width.

**Verdict:** needs work.

### 4.7 Electric lenses, briefly
- The expansion φ = ϕ − (r²/4)ϕ″ and E_r = (r/2)ϕ″ are correct. As a pointer section it is the right length.
- "converging or diverging depending on the sign". The graduate will want the known result: an electrostatic lens
  between two field-free regions is always converging. Only a field that ends on an electrode (a single aperture) can
  diverge, with f ≈ 4V/(E₂ − E₁) (Davisson–Calbick). One clause and one number would turn this into physics.
- "The retarding field of chapter 3 is such a lens." This is correct, but chapter 3 (3.3) modelled it as having "no lens
  action". The two chapters should point at each other, with the size of the effect (a few mm of focal length at the
  numbers of Example 3.2).
- "their paraxial equation contains ϕ′ and ϕ″ besides ϕ and is solved in the same way" is a statement without the
  equation. Give it in one line (non-relativistic: r″ + (ϕ′/2ϕ)r′ + (ϕ″/4ϕ)r = 0), or drop "solved in the same way".
- φ versus ϕ: the symbol clash with 4.4 (see 4.3).

**Verdict:** needs work (minor).

### 4.8 Checks, hand-over and limits
- The checks table is a strength in substance. In form it is not fit for a portfolio: the "detail" column prints raw
  SymPy (`r**4*Derivative(B(z), (z, 5))/64`, `e*B(z)/(2*gamma*m)`) and raw ASCII subscripts ("B_z", "p_θ", "C_c").
  At 390 px the detail column lies off-screen in a horizontal scroll (table 479 px in a 358 px wrapper).
- "they agree to about 10⁻¹¹ in every output (parity check)". This compares two copies of the same algorithm. It shows
  the port is faithful, not that the answer is accurate. Say so, and point to N1 for accuracy.
- Hand-over: the "landing voltage" and "demagnification M" problems are items 3 and "close behind".
- "What the model leaves out": a good list, but it lacks the wafer immersed in the field (item 1), and space charge
  is not mentioned. "none changes the scaling laws found here" is contradicted by Example 4.2 itself.
- Problems: after `e113ab0`, Problem 1 points to (4.8) and asks why (4.9) diverges, which is good. The answer
  (ω = 2, NI = 826 A, recomputed) is exactly the simulation's silent bisection limit (item 2). Problem 3: recomputed
  α = 10.1 mrad, blur 4.30 nm. Fine.
- No reference list (item 7).

**Verdict:** needs work.

### Simulation · The objective lens, focused on the wafer
Settings tried: default; 30 kV; 100 V; a = 20 mm, WD = 0.5 mm, u = 10 mm; a = 0.2 mm, WD = 20 mm; a = 20 mm,
WD = 20 mm, u = 10 mm; WD = 5 mm; a = 1 mm with WD = 2 mm; u = 10 mm. Screenshots in the scratchpad (`shots/v2/sim-*.png`).
- Good: the default readouts match the text and my recomputation. The canvas does not react to the pointer (frames
  compared before and after moving the pointer across it: identical), as the house rule requires. There are no console
  errors.
- Silent focus failure: item 2.
- The V_land label contradicts the model: item 3.
- Equation to screen (STANDARD 6) is missing. The caption does not say that the ray's height is normalised to its largest
  excursion in view (from the code: `sc * rec / rmax`), so the vertical scale is arbitrary. At the default setting the
  lower ray runs straight through the drawn coil (1400 px and 390 px). A real 5 mrad image-side ray is about 18 µm from
  the axis inside a 2 mm lens. The caption should also say that the z axis is linear from −6a, so the object is far
  off-canvas; that the drawn ray is the rotating-frame paraxial ray (the real electron spirals); and that two mirror
  rays are drawn although the caption says "the axial ray".
- The readout "f" is the asymptotic focal length and not the operative one (item 1). The readouts do not show B₀ or ω,
  though Example 4.1 quotes both.
- Moving V_land changes only NI, by design (B²/V\* scaling). One sentence in the caption would stop the reader from
  thinking the other readouts are frozen.
- Layout: at a = 20 mm the coil and the "B(z), dashed" label are clipped at the right edge. At 390 px "B(z), dashe" is
  clipped at the default, and "wafer" is crossed by the ray. The sliders sit below the drawing at 390 px, so the
  drawing is off-screen while one drags.
- Slider resolution: the log slider moves V_land in 0.57 % steps, so 800 V cannot be set exactly once moved
  (0.802 kV), and WD cannot return to exactly 3.00 mm (C_s then reads 4.20 mm, not 4.19). This is a small point, but the
  text compares "4.19 mm against 4.19 mm".

**Verdict:** needs work (a silent wrong answer in about 7 % of its slider space; the drawing does not explain its scales).

---

## Verdict summary (STANDARD 4, items 1–8)

| | 1 picture | 2 model | 3 derivation | 4 checks | 5 method | 6 eq. → screen | 7 limits | 8 reading |
|---|---|---|---|---|---|---|---|---|
| lead | – | – | – | – | – | – | – | – |
| 4.1 | good text, figure wrong | – | – | – | – | – | – | – |
| 4.2 | good | stated | complete; Ampère wrong | L1, L2 | – | – | iron claim wrong | Glaser inline only |
| 4.3 | good | paraxial stated | meridional only | no units check | – | – | – | Busch uncited |
| 4.4 ★ | good | – | key step missing | weak-lens limit good | – | – | – | – |
| 4.5 | good | immersion unstated | – | numbers check | half-described | f misleading | – | – |
| 4.6 | good | – | C_c step skipped | strong (N2, N3) | described | – | – | unread source |
| 4.7 | adequate | – | pointer only | – | – | – | – | – |
| 4.8 | – | – | – | table raw | parity ≠ accuracy | – | list good, one false claim | no `.prefs` |
| sim | – | V_land label wrong | – | matches text | silent failure | scales unstated | – | – |

Every section: **needs work**. None needs rewriting from scratch. The algebra and the numbers are sound. The work is
mainly six paragraphs of physics (items 1, 3, 4, 5, 8, 9), one missing step (item 6), the references (item 7), the
simulation's failure mode (item 2) and Figure 4.1 (item 10).
