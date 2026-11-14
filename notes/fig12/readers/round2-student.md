# Fig. 12 note, round 2: a strong student's marks

Reader: a strong final-year school student or first-year physics undergraduate, reading the whole note slowly, with a
physics graduate reading over the shoulder for the starred parts.

How it was read: `npm run build` on commit `2034121`, `dist/` served over a local HTTP server, the page
`simulations/guinness-kaggle.html` opened in headless Chromium (Playwright, 1300 × 1000), "Expand all" pressed, and every
`section.psec` of `<article id="paper">` and each of the 6 figures and 8 tables screenshotted. The KaTeX source of every formula
was read from the rendered page. No KaTeX errors on the page. I did not read plan.md, check.md or any other file in
`notes/fig12/readers/`.

I recomputed every worked number in the note: Examples 2.1, 3.1, 4.1, 5.1, 6.1, 6.2, 7.1, 12.1 to 12.5; the free-swing fit;
ζ_edge = 0.62 at 1 mm; τ_v = 11.7 Pa; h_eff = 9.9 mm; the Floquet numbers; Problems 2, 3, 5, 7, 10, 11, 12. I also re-derived
c₁, β, (17), (25), (33), the K₄ = 150 A/m check, the q_peak formula and i_par. They are all right to the digits printed. The
marks below are about reading, not arithmetic, except where I say otherwise.

Kinds of mark: **undefined** (term or symbol used before it is defined, or never defined), **two meanings** (one symbol,
two things), **figure** (axes, colours or meaning unclear), **skipped step**, **no number** (claim without its number or
support), **forward ref** (needs a later section to make sense), **read twice** (a sentence I had to read again),
**error** (wrong or self-contradictory as printed), **no picture** (the physical picture is missing).

---

## Abstract and §1 A full pint on a moving cart

1. §1, "two measures, the tilt and the lean, both defined in section 11.1". **Forward ref / two meanings.** The lean is first
   defined in §4.1 ("the height at the front wall minus the height at the back, is then 2q"), at the wall. §11.1 defines it
   again on the ring at R − Δx/2. The pointer sends the reader 10 sections ahead for a word that §4.1 already defines
   differently.
2. §1, "A controller is a rule, run by a small computer on the cart a thousand times a second". Fine as a picture. But the ride
   list names four controllers and the abstract says "five controllers". It takes until §12.5 ("No stored ride uses it on its
   own") to learn that the fifth, the skyhook, never rides alone. **Read twice.** Say it here in half a sentence.

Verdict against STANDARD (picture, model, plan): **clear, leave it.** The waiter and the coffee are the right picture. Mark 1
is a one-word fix.

## §2 The pint, measured

3. "What matters for a foam is the ratio of the bubbles' total volume to their total surface: the surface, through its tension,
   holds the energy that resists deformation, and the volume sets how much space that surface has to fill". **Read twice.** The
   second half ("how much space that surface has to fill") does not tell a student why the ratio, rather than the mean
   diameter, is the right size. One plainer clause would do: the stress scale is γ divided by a length, and the length that
   counts is volume over surface.
4. "For a log-normal distribution ⟨dⁿ⟩ = e^{n m_d + n²s²/2}". **Skipped step.** A school student has not met the moments of a
   log-normal. One line would do: ln d is Gaussian, so ⟨e^{n ln d}⟩ is the Gaussian's moment-generating function.
5. "The project's own calculation of that balance (in the research notes kept with the code,
   notes/fig12/research/data-for-solver.md; not a measurement and not a published value)". **No number / undefined.** The
   reader cannot open a repository path, and the drainage balance it rests on is not sketched. The note's most sensitive input,
   φ_ℓ (see §6.1), rests on a calculation the reader cannot see.
6. "Near its bottom the head is then barely a solid (section 6.1 shows why)". **Forward ref.** It is acceptable, but "solid" for
   a foam is a surprise at this point. §6's lead sentence ("a solid that can flow") would help if it came here.
7. Example 2.1, "On the computer's grid the head is laid on the open area of each column". **Undefined.** "Column" and "open
   area" are defined only in §8.1 and §8.5.
8. Symbols. **Two meanings.** In the same section d̄ is the bubble diameter and d_s is a depth of stout. In §5.2, d is the
   distance from the glass, and in §12.8 d_t is the tyre's compression. Also s is the log-normal width here, and s(t) is used in
   Problem 9 and s′ in (45). Small, but a reader keeping a symbol list stops.

Verdict: **clear, leave it**, except marks 5 and 7. Table 1 is exactly what STANDARD item 2 asks for.

## §3 A liquid in a shaken glass

9. §3.1, "Let the glass's position along the road and its height being X_g(t)". **Error (grammar).** "being" should be "be".
   I read the sentence twice before I saw that X_g is the definition.
10. §3.2, "In three dimensions the friction force per unit volume of a liquid like water is μ∇²u + ⅓μ∇(∇·u)". **Skipped step /
    no support for the student.** The 1-D slab argument is lovely. The jump to 3-D, with a ⅓ that is then thrown away, is only
    cited ([6, 41-2]). Either drop the ⅓ term, since (3) kills it anyway, or say in words where it comes from.
11. §3.2, "for a liquid that cannot be compressed the second term vanishes by (3) below". **Forward ref.** (3) is two
    paragraphs later. Fine, but the order could be swapped: derive (3) first, then the friction.
12. §3.3, "p = p_s at z = h + η … zero for a bare surface". **No number / model not stated.** Surface tension at the free
    surface is dropped without a word, although γ = 44.2 mN/m was carefully measured in §2. The Bond number
    ρgR²/γ ≈ 340 (my number) says it is safe. STANDARD item 2 asks for the dimensionless numbers with the page's values, and
    this one is missing.
13. §3.4, "the glass would have to supply the force −∫∇p dV = −m g_eff". **Skipped step (small).** It uses ρ∫dV = m, and it
    assumes that the glass supplies the whole pressure force. The free-surface load p_s (the head) is silently left out. One
    clause would fix it.
14. §3.4, "inclined by the angle ϑ". **Two meanings.** ϑ is the surface's tilt here, the wedge's plane angle in §6.4, and θ (a
    near-identical glyph) is the azimuth from §4.1 on.

Verdict: **clear, leave it** (marks 9, 12 and 14 are one-line fixes). The braking bus and the effective gravity give the
physical picture. The derivations are complete enough for a student to follow. The three checks are what STANDARD item 4 asks
for.

## §4 The rhythm of the surface ★

15. §4.1, "The flow of a surface wave fades with depth over a distance comparable to its wavelength, here a few centimetres".
    **Error / read twice.** Two paragraphs later the note says the fading depth is 1/k = 21.2 mm. The wavelength 2π/k is
    13.3 cm, the height of the whole glass. "Comparable to its wavelength, a few centimetres" is wrong on both counts. It should
    say "over a depth of about 1/k, here about 2 cm".
16. §4.1, "The last term depends only on z and the rest only on r, so each must be a constant; we call it k²". **Read twice.**
    The z-term equals +k² and the r-part equals −k². "We call it k²" leaves the sign of the other part for the reader to find.
17. (10), "ω₁₁". **Undefined.** The subscript "11" is never explained. A reader guesses "first, first". §5.3 later speaks of
    "m waves around the glass", which is the m in (m, n) = (1, 1), but that is never connected to the subscript.
18. §4.1, "Bessel's equation of order one. Its two solutions are the Bessel functions J₁(kr) and Y₁(kr)". **No picture.** The
    section is starred, so a school student may skip it. But nowhere in the note, starred or not, is the mode drawn: no
    sketch of J₁(kr) cos θ, of the surface tipping about its nodal line, or of the flow fading as cosh kz. The word "mode"
    carries the whole chapter. A small surface plot or a cross-section with arrows is the one figure the note lacks most.
19. §4.2, "The two surface conditions, projected on this mode, become …". **Skipped step.** "Projected" means: multiply by
    J₁(kr) r, integrate, and use orthogonality, so that r is replaced by c₁J₁(kr). Half a sentence would save the student.
20. (13), "q_max = (β/ω₁₁)|∫a(t′)e^{jω₁₁t′}dt′|". **Skipped step.** The step from "the swings simply add" (a sum of
    sin ω(t − t′)) to the modulus of a complex integral is not shown. It needs sin ω(t − t′) = Im[e^{jωt}e^{−jωt′}] and the
    remark that the modulus of the sum of phasors is the amplitude. A graduate supplies it. A student does not.
21. §4.2, "it is then a little shorter than half that swing's period, which changes its effect only slightly". **No number.**
    0.146 s against half of 1/2.915 Hz = 0.172 s is 15 % shorter. By how much does it change the swing left behind? The note
    gives numbers everywhere else.
22. §4.2, "(Problem 7)". **Forward ref** to the Problems box at the very end. That is acceptable, but the 5.2 mm could be
    checked in one line here: the integral is jT_p/2.

Verdict: **needs work, small.** The derivation is complete and right, and the two Key result boxes do restate it plainly (★
rule met). Missing: the picture of the mode (mark 18) and the false "wavelength" sentence (mark 15).

## §5 Where the swing's energy goes

23. §5.1, "for the stout's own damping ratio of section 5.4, ζ = 0.0055". **Forward ref.** It is used in 5.1 and derived three
    subsections later. Acceptable, but say "which we shall find in 5.4".
24. §5.1, (14) uses a bare ω. **Two meanings (mild).** From here on ω means the natural frequency of whatever swing is in hand:
    ω₁₁, then ω_h, then the computed 18.32 rad/s in §12. The note says so once ("with ω the natural angular frequency"), and that
    is fine. But in §5.2 ω becomes the forcing frequency of the Stokes layer, fixed at 2π × 3.42 Hz.
25. §5.2, "the difference u′ = u∥ − U cos ωt obeys (2), with x∥ the distance along the wall, as the diffusion equation
    ∂u′/∂t = ν∂²u′/∂d²". **Read twice / skipped step.** It does not say which terms of (2) were dropped (the non-linear term, the
    effective gravity, the derivatives along the wall), or why the pressure gradient cancels out of the difference. It is the
    key physical step of the Stokes layer.
26. Figure 2. **Figure.** The x-axis title "distance from the glass, d (mm)" is printed on top of the label "◂ one grid cell,
    1.5 mm ▸". The two overlap and neither can be read (seen in the screenshot at 2.5× scale). The label "ωt = π" is cut by the
    lower frame, and "ωt = 0" and "δₛ = 0.44 mm" sit on the curves. The caption names no colours. The labels "ωt = π/2" and
    "ωt = 3π/2" sit at the right edge, where both curves are at zero, so the reader cannot tell which curve is which.
27. §5.3, "This is the classical result for smooth, laminar flow". **Undefined.** "Laminar" is used here and in §13, and never
    defined.
28. §5.3, "the decrement is K_Λ ν^{1/2}R^{−3/4}g^{−1/4}". **Undefined.** The subscript Λ is unexplained, and "Miles", to whom
    the theory is credited, has no reference.
29. §5.4, "σ_skin = … = 0.110 s⁻¹, ζ_skin = 0.0051". **Read twice.** The same two numbers as the wall's, to three digits. The
    Key result box does explain the coincidence. The paragraph that derives (18) does not, and there the reader suspects a
    copy error.
30. §5.4, "The calculation of 5.3, now with the horizontal velocity on the plane z = h … gives Π/2E_s = √(νω/2)(k/2)coth kh".
    **Skipped step.** §5.4 is not starred, but this step is compressed more than anything in the starred §5.3. Either star it or
    show the two lines.
31. §5.4, "The model holds the head of foam to vertical motion only (section 6), a choice of the model rather than an
    observation". **Forward ref / no picture.** The reader meets "the head is a lid" before meeting the head. One sentence of
    picture would help: the foam cannot slide on the stout, so the stout just under it must shear.

Verdict: **needs work, small** (marks 25, 26, 30). The energy-balance route σ = Π/2E_s is the right tool and is well
explained. The check that the heat in the layer equals the wall's work is exactly what STANDARD asks for.

## §6 The head of foam

32. §6.1, "Völp and Willenbacher showed that for foams whose bubble surfaces are stiffened by proteins the right scale also
    contains the surface's elasticity, the generalized Laplace pressure". **Undefined.** "Laplace pressure" (the pressure jump
    2γ/r across a curved surface) is never named as such. The sentence before calls it "the pressure inside a bubble". Name it
    there.
33. §6.3, "At the head's frequency (section 6.5) it is 0.62 for a swing of 1 mm". **Forward ref.** The head's frequency is
    derived two subsections later. It also leaves open which frequency: 3.070 Hz (theory) or 2.915 Hz (computed)? Because
    ζ_edge ∝ ω^{2/3}, the two differ by about 3 %. My check: 0.62 comes out at 3.070 Hz.
34. §6.3, "65 to 111 times the stout's own friction of section 5.4.of section 5." **Error (typo).** It reads "of section 5.4.of
    section 5." Delete "of section 5."
35. §6.3, "κ = τ_edge(|w|) h_eff/|w| × (length of glass along that strip of surface)/(area of the strip)". **Undefined.** Which
    strip? It is presumably the wall column of the grid, but grid columns are not yet defined (§8.1), and the formula in words
    leaves the student unsure what is being divided by what.
36. §6.3, "Cantat worked out the friction of bubbles sliding on a wet wall … the stress on the wall at the sliding speed v_s".
    **No picture.** The note has a figure of the glass and of the Stokes layer, but nothing showing the head's edge sliding up
    and down the wet glass, which §6.3 says is the strongest brake in the chapter. A sentence of everyday picture (a squeegee on
    a wet window, or a wet sponge dragged on glass) would carry it.
37. §6.4, "And the pseudo-force of an outward acceleration a_out of the glass pulls the block outward". **Error / read twice.**
    The pseudo-force is −m a_g. It pulls the block outward when the glass accelerates inward, away from that side. As written,
    an "outward acceleration of the glass" would push the block in. Define a_out as the outward part of −a_g (or of
    g_eff), or say "an acceleration of the glass away from that side".
38. §6.4, the wedge, "inclined at the angle ϑ". **Two meanings** (see mark 14): the third use of ϑ/θ.
39. §6.5, "Take a small wave η = η₀ cos(kx − ωt) … with the potential of section 4 below it". **Read twice.** §4 used a
    standing wave in a cylinder. Here the wave is a plane travelling wave. It works because only k matters, but a student needs
    to be told so ("the head's mass changes only the surface condition, so a plane wave of the same k gives the same factor").
40. §6.5 end, "with the head those layers brake the swing about 6 % too strongly". **Read twice.** The 6 % uses the theory's
    3.070 Hz. The computed headed swing (§11.2) is 2.915 Hz, which gives √(3.42/2.915) − 1 = 8 %. Say which one.
41. §6.6, "In a swing neighbouring columns move at different speeds". **Undefined / forward ref.** "Columns" (of the grid) are
    defined in §8.1. Here it reads as columns of foam, which is a different picture.
42. §6.6, "∇_h·(h_f μ_f ∇_h w′) − κw′ … Δt the time step". **Forward ref (mild).** The value of Δt (2 ms) is only given in §8.
43. §6.6, "the conjugate-gradient method, an iteration that improves a trial solution step by step and needs only products of
    the matrix with vectors". **Fine here**, but §8.6 defines it a second time in different words. One of the two can go.

Verdict: **needs work.** The physics is the heart of the note and the derivations are sound (I re-derived (25), (23), the
wedge and ζ_edge). The unstarred results are restated ("In plain words", Key result 6.5), so the ★ rule is met. Fix marks 34
and 37 (an error and a typo). Add the picture of the sliding edge (mark 36). Settle which frequency §6 uses (marks 33, 40).

## §7 The cart and the roads

44. §7.1, "the road and the stout push with a force we collect in F_d". **Forward ref / no picture.** How a road can push a cart
    *backward* (the slope of the road tilting the tyre's push) is the key to the whole kerb story. It is explained only in
    §12.3. One sentence here, "on a bump the road pushes at right angles to the slope, so partly backward", would plant it where
    F_d is introduced.
45. §7.1, "it produces the voltage ℰ = bv against its supply (b is also 5 V per m/s)". **No support.** Why the push per ampere
    and the volts per m/s are the same number (energy conservation: b i v = ℰ i) is the kind of step a student needs once.
46. Table 2, "drag along the road, c_x". **Undefined.** It is never said what physical drag this is (rolling resistance? air? a
    model choice?).
47. §7.1, the symbol m_ℓ for "the stout and its head". **Two meanings (mild).** ℓ was "liquid" in φ_ℓ, and m alone is the
    stout's mass in §3.4 and §7.3, without the head. In §6 m_s is the head's mass *per unit area*, and in §7.1 M_s is the mass
    on the spring. m_s and M_s side by side are easy to confuse.
48. §7.2, "on all three roads the axle's steepest slope stays the road's (Table 3)". **No number.** Table 3 gives the road's
    slope only, not the axle's. So the claim is not shown in the table cited.
49. §7.3, "F_n = −(P_n − P_{n−1})/Δt_n". **Read twice.** The subscript n on Δt_n says the step varies, but the fact that it
    does (shortened for fast particles and before each picture) is given only in §8.6.
50. §7.3, "at the head-loaded swing's period, about 326 ms". **Two numbers.** 326 ms is the theory's 3.070 Hz. The note's own
    measured headed swing, which §11 and §12 use throughout, is 2.915 Hz, a period of 343 ms. Pick one, or name both.

Verdict: **clear, leave it**, apart from marks 44 and 50. Table 2, Example 7.1 and the momentum book of §7.3 are exemplary.

## §8 How the computer does it

51. §8.2, "averaging cos k(x + s) over the tent of half-width Δx (whose Fourier transform is …)". ★, so acceptable. The plain
    restatement exists ("In plain words: the particles carry not only a velocity but its slope"). **Fine.**
52. §8.2, "The smoothing loss of the plain method now starts only at the curvature of the field, two orders higher in kΔx".
    **No support.** It is stated, not shown, and has no number for the swing. "Negligible" should carry its number: (kΔx)⁴ ≈
    2.5 × 10⁻⁵, times some factor.
53. §8.3, the step list: "the particles take their velocities back, (31), and move". **Undefined (STANDARD item 5).** How do the
    particles move (forward Euler? a higher-order scheme?), and what is the order in time of the whole fluid step? §8.4 gives the
    surface condition's order in space ("second order"), but the integrator's order in time is never stated. STANDARD 5 asks
    for "integrator, order, step size".
54. §8.5, "(no column needed it in the stored rides' rest test)". **Forward ref / undefined.** The "rest test" is defined in §9.
55. §8.5, "In each column the code finds the top of the stout from the first field and then the highest zero of the second in
    the top three cells". **Read twice.** "First field" and "second field" are the χ with r₀ = 0.9Δx and with r₀ = 0.505Δx, but
    the sentence before speaks of "two radii", not "two fields". Say "from χ with the larger radius … the smaller radius".
56. §8.4, "until the largest residual is below 10⁻⁵". **Undefined.** "Residual" is never defined (for the student: how far each
    equation is from being satisfied). The same goes for "preconditioned by dividing each equation by its diagonal".
57. §8 as a whole. **No picture.** A section about a staggered grid, particles two by two by two in a cell, cut cells and a level
    set has no figure. One schematic cell (pressure at the centre, u_x on the x-faces, eight particles, the glass cutting a
    corner) would replace a paragraph of words.

Verdict: **needs work, small.** The method is described as the code does it, with the page's values (1.5 mm, 2 ms,
νΔt/Δx² = 0.0018, 84 to 93 ms a step). The order explanation of steps 4 and 5 is excellent. STANDARD 5 still wants the time
order (mark 53). The section would also gain from one schematic (mark 57).

## §9 The books

58. "The heat D booked by the frictions in that test was not kept with the stored runs, so (35) cannot be closed here". This is
    honest. A careful reader notices, though, that the section titled "The energy of a pint at rest" ends without its
    energy balance. **No number** for D. If D could be printed from the next run, the check would be closed.

Verdict: **clear, leave it.** The particle count with zero tolerance, and the impulse book to 9 × 10⁻¹⁵, are exactly the
"conserved quantity" check of STANDARD 4.

## §10 What the page shows

59. "SHA-256 fingerprint, a 64-digit number". **Error (small).** It is 64 *hexadecimal* digits (256 bits). As written, a
    student thinks of a 64-digit decimal number.

Verdict: **clear, leave it.** The open box "What is data and what is drawing" is exactly STANDARD item 6.

## §11 What the computed rides show

60. §11.1, "The lean is the height of the surface at the front of the glass minus its height at the back, read on the outermost
    ring … at the radius R − Δx/2". **Two meanings** (see mark 1). §4.1 defined the lean at the wall as 2q. Say here that this
    is §4.1's lean, read 0.75 mm inside the wall.
61. §11.1, "at r = 13/16 (R − Δx/2) = 31.2 mm". **Read twice.** Why 13/16? "A little inside" is 7 mm inside. The fraction
    looks arbitrary unless the reason is given (presumably the largest ring whose points all lie in trusted columns).
62. §11.2, "Its first swings without the head are a little smaller than that". **No number.** Figure 3 shows a first peak of
    about 4.3 mm against the 5.0 mm predicted, 14 % smaller. Give the number.
63. §11.2, "for that size the edge friction alone predicts ζ_edge = 0.47". **Read twice.** It does not say at which frequency
    (see mark 33). 0.62 × 2.3^{−1/3} = 0.47 uses 3.070 Hz. At the measured 2.915 Hz it would be 0.45, 6 % above the measured
    0.425 rather than 11 %.
64. Figure 3. **Figure.** The y-axis title "q (ring), mm" is printed on top of the label "the push". The two overlap and neither
    reads cleanly (seen at 2.5×).
65. §11.3, Table 4, column "Swing, bare / Swing, with head". **Read twice.** It is not said in the table whether "swing" is q
    (the height at the wall) or the lean (2q). The text then compares 45 mm with "the 22.5 mm that brings the stout to the rim",
    so it is q, but the reader must work that out.
66. §11.4, "we followed (36) numerically over one period … this is Floquet's method … the lowest threshold is ε = 1.71". ★, and
    restated plainly ("The heave cannot pump this pint's swing"). **Fine.** The graduate might want to know that ε > 1 means
    the effective gravity changes sign for part of the cycle, so the linear model is outside its regime there. One clause.
67. §11.5, "The kerb … the lean of 24.3 mm means a rise of about half that". Fine. But the swings here reach q ≈ 12 mm against
    R = 39 mm. **No number / limit not stated.** The linear (small-swing) theory of §4 is used for amplitudes that are a third
    of the radius, and §13 does not list non-linearity of the swing among the limits.

Verdict: **clear, leave it**, except marks 62 to 64. This is the strongest section of the note: theory against computation,
with the gaps named (2.6 %, the 0.0105 of the method, the unexplained 3.0 %).

## §12 Five controllers

68. §12.2, "with the loop closed the cart's acceleration is S = 1/(1 + 𝓛) times what it would be without it". **Skipped step.**
    It is one line of algebra (M_x jω V = F − b(K_p + K_i/jω)V), and that line is the whole idea of feedback. Show it.
69. Example 12.1, "With the current lag and the half-sample delay of a command held for 1 ms". **Undefined.** Why a command
    held for one sample acts like a delay of half a sample (zero-order hold) is never said.
70. §12.2, "for this ω_c the speed returns as fast as it can without overshooting". **Read twice.** It means critically damped
    at that ω_c. "As fast as it can" sounds like a statement about the motor.
71. §12.3, "the push along the road is −N z_a′ for a push N mostly upward". **Read twice.** Is N the full push at right angles to
    the path, or its vertical part? With the slope at 0.785 (38°), "mostly upward" is a 25 % difference. The formula −N z_a′ is
    exact if N is the vertical part. Say so.
72. Figure 4 caption, "Grey bands: the wheel in the air". **Figure.** The bands are cream or beige (#ece6dc), not grey, and the
    caption also has "Dashed grey" lines, so the reader looks for grey bands and does not find them. "Dashed wine" also means
    two different things in the two panels (the motor's delivered push on top, the speed with full current below).
73. Figure 4 caption, "when the axle has reached x = 1.437 m". **Undefined.** The origin of x is never stated. §7.2 says only
    that the axle starts "1 m before the centre of the first bump". If x = 0 is the start, the kerb's centre is at x = 1 m, and
    1.437 m is past it, which contradicts the label. So x must be measured from somewhere else.
74. §12.4, "This is feedforward from a disturbance known in advance". **Fine.** The delay-versus-lag comparison to first order
    is a nice touch.
75. §12.5, "Such a damper calms the body's bounce without passing the road's shocks on to it, as a damper between body and
    wheel would". **No support.** It is the defining property of the skyhook and is stated without the one-line reason (a
    damper on the relative speed passes on the wheel's speed; one on the absolute speed does not).
76. §12.6, "where X is the symmetric, positive definite solution of the second equation, the algebraic Riccati equation".
    ★ and acceptable. The "idea behind it is short" paragraph is a fair sketch. The Key result restates it plainly. **Fine.**
77. §12.7, "a signal whose integral over any time T_w has the variance W T_w". A good plain definition of white noise. **Fine.**
    But "the swing's rate drifting by about 0.026 m/s within one swing" uses the 0.343 s period without saying so.
78. §12.8, "Choosing it to equal ω²(a_z/g)q, the parametric term carried to the right". **Read twice.** "It" grammatically
    refers to the current δi, but what is set equal to ω²(a_z/g)q is the added right-hand side −β_h bδi/M_x.
79. Box "The controllers are the site's own", "(notes/fig12/handoff-jax/portcheck.txt)". **Undefined for the reader.** It is a
    repository path, not a source a reader can open from the page.
80. §12.10, "the command at or beyond 3 A in 6 or 6 stored pictures, about 200 to 200 ms". **Error (template residue).** "6 or
    6" and "200 to 200" are a range whose two ends came out equal. Table 8 also shows 6, 6, 6 and **5** for the four kerb
    controllers, so "6 or 6" is also wrong for joint control (5 pictures, 167 ms).
81. §12.10, "the first forward surge is about as large under each (Figure 6): 21.2 mm (preview), 21.8 mm (slosh LQR) and
    25.4 mm (joint) against 22.2 mm with the speed held. (The largest leans of Table 8 can come from the swing back, a quarter
    of a second later.)" **Error / read twice.** 21.8 and 25.4 are exactly the *largest leans* of Table 8 for the LQR and
    joint control. 22.2 is the *tilt*, not the lean, of the speed-held ride. 21.2 appears nowhere in Table 8. The reader cannot
    tell whether these four are leans or tilts, first peaks or largest values. The parenthesis then says the Table 8 values may
    be the swing back, which contradicts the numbers just quoted. In Figure 6 the largest |lean| of the speed-held and
    preview rides is the swing back (about −24 mm), but for joint control it is the first forward peak (about 25 mm). State
    which quantity each number is.
82. Figure 6 caption, "(section 12.10)". **Read twice.** The figure is inside §12.10 and points to §12.10.
83. Figure 5 and Table 8. **Read twice.** Table 8 gives the speed-held lean as "13.9 mm", while Figure 5 shows that largest lean
    at −13.9 mm (back higher). The tables give largest |lean| without saying "in size". The caption's "up to 13.9 mm" is the same.
84. §12.10, "joint control leaves the largest first surge of all … its cancellation current reached 0.904 A in the jolt".
    Honest. **No number** for how much that current alone would move the swing, which would be a one-line estimate with
    Example 12.3's gains.

Verdict: **needs work.** The waiter's habits are a good picture, and Examples 12.1 to 12.5 turn every matrix into something a
student can feel ("a swing 1 mm high … adds +1.23 A, a forward push"). The § 12.3 "what no controller can do" argument is the
best physics in the chapter. Marks 80 and 81 are factual defects in the results paragraph and must be fixed. Marks 68, 71 and
73 are small but stop a careful reader.

## §13 Limits, and the next model

85. "The thin layers … enter as stresses fitted to the laminar theory at one frequency". **Error (word).** They are *derived*
    from the laminar theory (§5.2), not fitted.
86. Missing limit. **No number.** The swing is treated as linear (§4: "for small motions") up to q ≈ 12 mm in a glass of radius
    39 mm, and the Floquet threshold is at ε = 1.71, where the effective gravity reverses. Neither is listed as a limit (see
    marks 66 and 67). STANDARD 7 asks for the limits that would change what we see.
87. Problem 6, "telescopes to −P_N". **Two meanings / inconsistency.** §7.3 calls the last step n_e and writes −P_{n_e}. N is
    also the tyre's load.

Verdict: **clear, leave it** (add mark 86 in one sentence). The "next model" paragraph names a concrete hardware lesson (0.14
of the push) and a concrete method (MPC). The Problems box exists and its answers check.

## §14 Sources

88. Source 17, "2nd ed. (2021); read in the online edition, version 3.1.5 of 24 July 2020". **Read twice.** It cites a 2021
    edition but says it was read in a 2020 version. Fine if intended, but it reads as a contradiction.
89. "Sources 2, 3, 4, 8, 10, 11, 12 and 13 were read in extracts of their full texts kept with the project's research notes".
    STANDARD 8 says "only real sources you opened and read". **Flag for the lead**, not the student: eight of eighteen sources
    are declared as read in extracts.

All 22 links resolve to the expected hosts (arXiv, doi.org, NASA NTRS, DLMF, Feynman Lectures, the authors' pages). I did not
fetch them.

Verdict: **clear, leave it** (STANDARD 8 met for the links; mark 89 for the lead to judge).

---

## Symbols with more than one meaning (collected)

- **j**: the imaginary unit in (13), (15), §12; also the face index in (31) (u_j, W_jp).
- **i**: the motor current; also the particle index in (34) (x_i, b_i). §4.2 says "we write j and not i, which will be an
  electric current", and then (34) uses i as an index anyway.
- **φ / Φ / φ_ℓ**: the velocity potential, the gas fraction and the liquid fraction. Three φ's.
- **τ**: a stress (τ_w, τ_y, τ_v, τ_edge) and a time constant (τ_i, τ_u).
- **ϑ / θ**: the azimuth, the surface tilt (§3.4) and the wedge angle (§6.4).
- **σ**: the decay rate (§5); a standard deviation (σ_v, σ_q, §12.7).
- **λ**: λ_h, a length (§2, §6.5); λ, the eigenvalues (§12.6).
- **m_s / M_s**: the head's mass per unit area / the mass on the spring.
- **C**: the Bernoulli constant, C_e, the APIC gradient C_p, the covariance C and C⁻.
- **d**: the bubble diameter d̄, the depth d_s, the distance from the glass d, the tyre compression d_t.
- **N**: the tyre's load, the gear ratio N_g, and P_N in Problem 6.
- **p**: the pressure; also the particle index (m_p, u_p, W_jp).
- **b**: the push per ampere; also the weights b_i in (34).

None of these is wrong in its own paragraph. Together they break the house rule "one symbol one meaning" (STANDARD, verdict
of 21 October, item 2). The ones that will actually stop a reader are j, i, ϑ and τ.

## Figures (collected)

- Fig. 1: clear.
- Fig. 2: the x-axis title overlaps the grid-cell label; "ωt = π" is clipped; the curves' colours are not named; the π/2 and
  3π/2 labels are ambiguous (mark 26).
- Fig. 3: the y-axis title overlaps "the push" (mark 64).
- Fig. 4: the "grey bands" are beige; "dashed wine" has two meanings; x = 1.437 m has no origin (marks 72, 73).
- Fig. 5: clear. The largest lean is negative, while the table gives magnitudes (mark 83).
- Fig. 6: clear in itself, but the text's numbers about it are inconsistent (mark 81).
- Missing figures that the reader needs: the first mode's shape (mark 18), the head's edge on the glass (mark 36), one grid cell
  with its particles (mark 57).

## Verdicts per section against notes/STANDARD.md

| § | Title | Verdict |
|---|---|---|
| 1 | A full pint on a moving cart | clear, leave it |
| 2 | The pint, measured | clear, leave it (marks 5, 7) |
| 3 | A liquid in a shaken glass | clear, leave it (marks 9, 12, 14) |
| 4 | The rhythm of the surface ★ | needs work, small: mark 15 (wrong sentence), mark 18 (no mode picture) |
| 5 | Where the swing's energy goes | needs work, small: marks 25, 26, 30 |
| 6 | The head of foam | needs work: marks 34, 37 (error and typo), 36 (picture), 33/40 (which frequency) |
| 7 | The cart and the roads | clear, leave it (marks 44, 50) |
| 8 | How the computer does it | needs work, small: mark 53 (time order, STANDARD 5), mark 57 |
| 9 | The books | clear, leave it |
| 10 | What the page shows | clear, leave it |
| 11 | What the computed rides show | clear, leave it (marks 62 to 64) |
| 12 | Five controllers | needs work: marks 80, 81 (factual defects), 68, 71, 73 |
| 13 | Limits, and the next model | clear, leave it (mark 86) |
| 14 | Sources | clear, leave it (mark 89 for the lead) |

The ★ rule is met throughout: every starred passage (§4, §5.2, §5.3, §6.5, §6.6, §8.2, the head's mass in §8.4, §11.4,
§12.6 to §12.8) ends with a plain restatement or a Key result box.

**Must fix (errors as printed):** marks 15, 34, 37, 80, 81, 85.

**Number of marks: 89.**
