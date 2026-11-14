# Fig. 12 (Kaggle), round 1: the student reader

Reader: a strong final-year school student or first-year physics undergraduate (calculus, Newton's laws, simple harmonic
motion, a little complex numbers; no fluid dynamics, no control theory). Where a physics graduate would stop for a different
reason, the mark says "grad".

How it was read: `npm run build` (exit 0). `dist/` was served over a small local HTTP server and
`/simulations/guinness-kaggle.html` opened in headless Chromium (Playwright) at 1400 × 1000. I clicked "Expand all" and read
the whole `<article id="paper">` as it renders: 14 sections, 6 figures, 8 tables, the boxes and the Problems. Each section
and each figure and table was also captured on its own and looked at. KaTeX: 0 render errors at 1400 px and at 390 px. Every
number I could recompute with a pocket calculator from numbers printed earlier in the note I did recompute; where it
agreed I say nothing. I did not read plan.md or check.md.

Each mark gives the section, the exact words, the kind of mark, and why I stopped. Kinds: **undefined** (term or symbol used
before or without a definition), **two meanings** (one symbol for two things), **figure**, **skipped step**, **no number**
(a claim without its number or source), **forward** (needs something not yet read), **twice** (a sentence I had to read
twice), **picture** (the physical picture is missing), **inconsistent** (two numbers in the note that disagree). A verdict
against `notes/STANDARD.md` §4 closes each section.

---

## Across the whole note

1. **Equation numbers out of order.** The rendered order is (1)…(22), (24), (25), (26), (27), **(23)**, (28)…(30), (32)…(36),
   **(31)**, (37)…(52). (23) sits in 6.6 after (24)–(27) of 6.4–6.5, and (31) sits in 11.4 after (36) of section 9. Kind:
   twice. Looking back for "(23)" I searched the wrong place first.
2. **α has three meanings:** the tilt angle of the surface (3.4, "tilted by the angle α"), the slope angle under the head
   (Example 6.1, "a slope of angle α"), and the fraction of the way from a stout cell centre to an air cell centre (8.4,
   "at the fraction α of the way"). Kind: two meanings.
3. **j has two meanings in one paragraph** (8.2): "a face then receives … u_j = Σ_p m_p 𝒲_jp u_p …" (j = index of a face) and
   three sentences later "For a velocity varying as e^{jκx}" (j = imaginary unit, defined in 4.2). Kind: two meanings.
4. **κ has two meanings:** the head's edge-drag coefficient (6.3, "a drag κw") and the wavenumber of a velocity variation
   (8.2, "with κ the wavenumber of the variation"). Kind: two meanings.
5. **Φ has two meanings:** the gas fraction of the foam (2, "the gas fraction Φ = 1 − φ_ℓ"; used throughout 6) and the
   upper-right block of the Van Loan matrix exponential (12.7, eq. (46), "Φ(t)"). Kind: two meanings.
6. **E has two meanings:** the dilatational elasticity of the stout's surface (2, "E, the dilatational elasticity, is
   E_∞") and the energy of the swing (5.1, "from a swing of energy E"; 5.3). Kind: two meanings.
7. **φ, φ_ℓ and φ₁:** φ is the velocity potential (4.1), φ_ℓ the liquid fraction (2, 6.1), φ₁ (varphi) the mode amplitude
   of the potential (4.2). In print φ and φ_ℓ look like the same letter with a subscript. Kind: two meanings.
8. **Z has two meanings:** the vertical part of the mode, Z(z) (4.1, "Z'' = k²Z"), and Cantat's fitted friction prefactor
   (6.3, eq. (21), "Z = 0.18"). Kind: two meanings.
9. **δ is a length and a "small change":** the Stokes-layer thickness δ = √(2ν/ω) (5.2), but also δm, δV, δx (3.1–3.2) and δv,
   δi (12.2, 12.6) as small deviations. In 12.2 "M_x δv̇ = b δi − c_x δv" sits next to section 5's δ = 0.44 mm in my head.
   Kind: two meanings (minor).
10. **τ is a stress and a time:** τ, τ_y, τ_v, τ_w, τ_edge are stresses (5, 6); τ_i, τ_u are time lags (7, 12); τ is also "any
    time τ" in the white-noise definition (12.7). Kind: two meanings (minor).
11. **σ is a decay rate and a standard deviation:** σ = ζω (5.1), σ_wall, σ_skin; then σ² "a reading y, with variance σ²",
    σ_v, σ_q (12.7). Kind: two meanings (minor).
12. **K, L, C, N, m, B, λ, Q reused.** K = 3.50 (5.3, log decrement constant) and K the gain row (12.6); L_b bump length (7.2)
    and L, L_k the Kalman gain (12.7); C(t) Bernoulli constant (4.1), C_p APIC gradient (8.2), C covariance (12.7); N tyre load
    (7.1), N number of steps (7.3), N_s cross term (12.8); m stout mass (3.4, 7.3) and m "waves around the glass" (5.3,
    Bongarzone); B mode amplitude (5.3) and B input matrix (12.6); λ_h a length (2) and λ an eigenvalue (12.6); Q weights
    (12.6), Q_d noise covariance (12.7). Each is defined where it appears, so none of them stopped me for long, but together
    they make the second half harder to scan. Kind: two meanings (minor).
13. **Computer notation for small numbers:** "below 1e-05 of the largest right-hand side" (8.4), "1.3e-08 mL" (9), "9e-15" (9),
    "to within 6e-03 A" (Example 12.3), "4e-13 A", "6e-08 A", "8e-06" (12.9 box), "-0.03 mm" with a hyphen (11.2), "lowers
    its speed by -9.5 mm/s" (Example 12.4). A school reader reads 1e-05 as "1 times e minus 05". Kind: twice.
14. **Starred results not restated outside the star.** The by-line promises "every starred result is restated in plain
    words after it". This holds for 4 (two Key result boxes), 5.3 (Key result of 5.4), 6.5 (Key result box) and 12.6 (Key
    result box). It does not hold for: section 4's sudden-change results (12) and (13), which come after the last Key result
    box of 4 and are used in 11.3, 11.5 and 12.3; 6.6 (the 0.5 mm "locking" estimate); 8.2 (that APIC removes the 0.019
    smoothing loss); 11.4 (the heave cannot pump the swing); 12.7 (what the filter achieves); 12.8 (what joint control is).
    Kind: skipped step. See the section marks.

## Abstract and §1 · A full pint on a moving cart

15. **§1:** "The ride list names four: speed held only, road preview, slosh LQR and joint control." "LQR" is first spelled
    out in 12.6 ("This is the linear quadratic regulator, LQR"). Kind: undefined / forward.
16. **§1:** "and a fifth, the skyhook". No hint what a skyhook is until 12.5. Kind: forward (a half-sentence picture, "a
    damper hung from the sky", would do).
17. **Abstract:** "the head of foam, which turns out to be the strongest brake: with its head the computed pint rocks
    2.915 times a second and stops within about one swing". Section 6 derives what the head's friction is made of but never
    turns it into a damping ratio to compare with; the claim rests only on the computed ride of 11.2. Kind: no number (see
    mark 49).
18. **Abstract:** "five controllers for its motor and its suspension … foam goes over the rim under every controller".
    Only four were ridden on the kerb; the skyhook has no ride of its own (Table 6). Kind: twice.

Verdict §1: **clear, leave it** apart from marks 15 and 16. The picture from the pub and the waiter is exactly what
STANDARD §4.1 asks for.

## §2 · The pint, measured

19. "scales it to the size retailers list for the Guinness imperial pint, 160 mm tall and 85 mm wide". The drawing is
    149 × 76 mm, so the height is scaled by 1.074 and the width by 1.118: two different factors. Is it scaled separately in
    height and width? And the rim is at z = 147.5 mm above the inner floor, not 160 mm: the difference (base, wall) is not
    said. Kind: twice.
20. "The stout fills 426.6 mL" plus the head's 91.26 mL (Example 2.1) is 518 mL, with the head 3.5 mm below the rim. An
    imperial pint is 568 mL. A reader who knows that asks whether the glass is too small or the pour short. Kind: picture
    (one clause would settle it).
21. "the cart therefore carries 429.6 g of stout". The text gave 426.6 mL; the step 426.6 mL × 1.007 g/mL = 429.6 g is
    silent, and 426.6 vs 429.6 looks like a typo at first. Kind: skipped step / twice.
22. "for bubbles of 34 µm in a column 19 mm tall that balance leaves a liquid fraction of 0.36 at the bottom and 0.235 at
    the top. Reaching it takes 25 to 110 minutes". Neither the balance nor the times are derived or cited, and they decide
    φ_ℓ, on which τ_y depends steeply (6.1). Kind: no number / no source.
23. "until the pull of gravity is balanced by the suction of the curved films". Which films? The channels between bubbles are
    meant (they are named "channels where three bubbles meet" only in 6.2). Kind: undefined.
24. "it is expressed by the Sauter radius R₃₂ = ½⟨d³⟩/⟨d²⟩ … because the surface stores the energy". Which energy (surface
    energy, γ times area) is not said, and the ½ (diameter → radius) is not said. Kind: skipped step (small).
25. "Nitrogen … dissolves poorly and diffuses slowly, so these bubbles hardly grow in the few minutes we care about." No
    number or source. Kind: no number.
26. "How quickly a difference of velocity spreads through the liquid by friction is measured instead by the kinematic
    viscosity". Why dividing by ρ gives a spreading rate (m²/s, a diffusivity) is not said; it becomes clear only in 5.2.
    Kind: picture (minor).
27. Figure 1: the cream head is drawn flat-topped across the full width, and the label "R" sits on the red surface line; both
    readable. The figure is clear. No mark beyond 19.

Verdict §2: **needs work**, small: marks 19, 21 and 22 (the liquid fraction is the one input the note itself says matters
most, and its estimate has no source or derivation on the page).

## §3 · A liquid in a shaken glass

28. 3.2: "For a liquid that cannot be compressed, adding the same contribution from every direction gives the friction
    force per unit volume μ∇²u". Incompressibility is introduced only two paragraphs later (eq. (3)), and why it is needed
    here (a ∇(∇·u) term drops) is not said. Kind: forward / skipped step (grad).
29. 3.2: "Effective gravity, ρ g_eff δV." A bare sentence fragment after two full paragraphs on pressure and friction;
    I read it twice to see it is the third item of the list. Kind: twice (minor).
30. Example 3.1: "To lift the back wall by 3.5 mm, enough to bring the top of the head to the rim". This assumes the head
    tilts with the stout as a rigid layer; that is the model (6.4), but it is not yet stated. Kind: forward (minor).

Verdict §3: **clear, leave it** (28 is one clause).

## §4 · The rhythm of the surface ★

31. The whole section is starred, but its last part ("A sudden change of speed", eq. (12), and "Many small kicks", eq. (13))
    is the physics the rest of the note uses most (11.3, Table 4, 11.5, 12.3). It comes after the last Key result box and is
    not restated. A school reader who skips ★ as invited loses "a sudden change of speed Δv starts a swing of height
    β|Δv|/ω". Kind: skipped step (structure). A third Key result box after (12)–(13) would fix it.
32. 4.1: "Laplace's equation in these coordinates, divided by φ, reads (1/f)(f'' + f'/r) − 1/r² + Z''/Z = 0". The Laplacian in
    cylindrical coordinates is never written, so where −1/r² comes from (∂²/∂θ² of cos θ, divided by r²) is a skipped step.
    Kind: skipped step.
33. 4.1: "the momentum equation integrates to the time-dependent form of Bernoulli's law". The step (write g_eff as
    ∇(g_eff·x), take ∇ outside, integrate) is one line and is not shown. Kind: skipped step (minor).
34. 4.1: "(6) with p = 0 gives ∂φ/∂t + gη = 0". (6) gives g(h + η); that the constant gh is absorbed into C(t) is not said
    here (it was said once, about C(t), a paragraph earlier). Kind: skipped step (minor).
35. 4.2: "The numerator uses ∫₀ᴿ r²J₁(kr) dr = R³J₂(ξ)/ξ". This rests on d/dx[x²J₂(x)] = x²J₁(x), which is not quoted.
    Kind: skipped step (grad; fine under ★, but cite DLMF 10.6 for it).
36. 4.2, eq. (13): "e^{jω₁₁t'} … where j is the imaginary unit". Defined right after use; fine. But "leaves an undamped swing
    of 5.2 mm at the wall (Problem 7)" sends the reader to the last page for a number used now. Kind: forward (minor).
37. 4.2: "For Δv = −0.1 m/s, a change of speed you would hardly notice". No support; a 0.1 m/s jolt in a fraction of a
    second is about 1 m/s², which one does notice. Kind: no number (minor).

Verdict §4: **clear derivation; needs one structural fix** (mark 31). The Bessel-mode derivation, the projection and the
steady-push check (16 % to higher modes) are exactly the "every step with its meaning" of STANDARD §4.3.

## §5 · Where the swing's energy goes

38. 5.1: "for the stout's own damping ratio of section 5.4, ζ = 0.0055". Forward, but harmless. And "if friction removes the
    mean power Π from a swing of energy E" — E was the surface elasticity in §2 (mark 6).
39. 5.2: "The pressure gradient that drives the outer flow, −∂p/∂x_∥ = …". x_∥ (the coordinate along the wall) is not
    defined, and why (2) reduces to a pure diffusion equation for u' (the nonlinear term vanishes for flow parallel to a
    flat wall) is not said. Kind: undefined / skipped step.
40. 5.2: "We try u' = Re[û e^{jωt − (1+j)d/δ}]". "Re" is not defined for a school reader. Kind: undefined (minor).
41. Figure 2: the label "one grid cell, 1.5 mm" is printed across the black ωt = 0 curve near d = 0.7–1.1 mm and is hard to
    read. The ωt = 0 curve overshoots to about 1.07 before settling at 1; the caption's "the outer flow is reached within
    about 2δ" does not mention the overshoot. Kind: figure.
42. 5.3: "(17) becomes ζ_wall = 0.5575 ν^{1/2} R^{−3/4} g^{−1/4}". The number 0.5575 = √2 (ξ²+1)/(4 ξ^{1/4}(ξ²−1)) is not
    shown. Kind: skipped step (minor).
43. 5.4 vs 5.3: σ_wall = 0.110 s⁻¹ and σ_skin = 0.110 s⁻¹, ζ = 0.0051 both. Identical to three digits from two different
    formulas: (ξ²+1)/(2R(ξ²−1)) = 23.5 m⁻¹ and (k/2) coth kh = 23.55 m⁻¹. Coincidence or physics? The note does not say.
    Kind: twice.
44. Key result 5.4: "falls by the factor e in 1/(ζω₁₁) = 8.4 s and halves in about 19.9 swings". With the printed ζ = 0.0055
    and ω₁₁ = 21.49 I get 8.46 s and 20.1 swings. The note's numbers use the unrounded ζ (≈ 0.00555). Problem 2 repeats this:
    "(Answers: 19.9 swings; 19.3 s.)" — from the problem's own data, ζ = 0.0055, a student gets 20.1 swings and 19.5 s and will
    think they made a mistake. Kind: inconsistent.
45. 5.4: "A surface held as a lid adds the skin, ζ = 0.0107". 0.0051 + 0.0051 + 0.0004 = 0.0106 with the printed values.
    Same rounding issue. Kind: inconsistent (minor).

Verdict §5: **clear, needs small fixes** (44 and the Problem 2 answers, 39, 41). The Stokes layer picture ("the sliding
reverses before friction can reach further") is good.

## §6 · The head of foam

46. 6.1, eq. (19): "two laws describe their measurements". The laws G₀ = p_L Φ(Φ−Φ_c) and τ_y = 0.25 p_L (Φ−Φ_c)² are quoted
    with no picture of why the stiffness vanishes at jamming. One sentence would do ("at Φ_c the bubbles just touch, so
    there is nothing to compress"). Kind: picture.
47. 6.3: "for stiff surfaces, with her fitted prefactor". "Stiff surfaces" (bubble surfaces that do not stretch along the
    wall) is not explained, and Z is a bare fitting number with no meaning given. Kind: undefined.
48. 6.3: "Per unit area of the stout's surface, the edge friction acts in the columns that touch the glass". "Columns" (of
    the computer's grid) are defined only in 8.1. Kind: forward.
49. **6 as a whole: no predicted damping for the head.** The section builds the head's yield stress, flow law, wall friction
    and sheet, but never turns them into a damping ratio ζ for the swing (as 5.3 does for the wall). So when 11.2 measures
    ζ = 0.425, the reader has nothing to compare it with, and the abstract's "the strongest brake" (mark 17) has no theory
    behind it. The only number is the 6.6 estimate that swings below about 0.5 mm cannot shear the head. Kind: no number /
    picture. This is the largest gap in the note.
50. 6.4: "a wedge of foam sliding on the most dangerous plane through the rim's edge, the textbook estimate for a vertical
    cut in a material with a yield stress, would stand up to about twice the height, 8.1 mm at rest". Which textbook? No
    source and no derivation. Kind: no number / no source.
51. 6.4: "Its own pressure pushes outward on its free outer face". Why a foam, which we were just told is a solid, has a
    hydrostatic pressure inside it is not said. Kind: twice (grad).
52. 6.3: "like dry friction, it stops a small motion in a finite time instead of letting it fade for ever". A claim the
    reader can accept from τ ∝ v^{2/3}, but the step (a force that does not vanish as fast as v brings v to zero in finite
    time) is not shown. Kind: skipped step (minor).
53. 6.6: "Over its thickness h_f it then pushes on the stout with the force per unit area ∇_h·(h_f τ ∇_h w/|∇_h w|)". Stated,
    not derived; the reader cannot see why a divergence appears. Kind: skipped step (★, grad).
54. 6.6: "A swing much smaller than this at the wall cannot shear the head, and stops". This is the one result of 6.6 and it
    is not restated outside the star; it is also what explains the "−0.03 mm" residual tilt in 11.2. Kind: skipped step
    (mark 14).
55. 6.6, typesetting: after "w(x, y)" the comma wraps to the start of the next line (", and never sideways"). Kind: figure
    (typesetting, minor).

Verdict §6: **needs work.** Marks 49 (a theoretical damping ratio for the head, even an order of magnitude), 50 (a source
for the 8.1 mm), 47, 48.

## §7 · The cart and the roads

56. 7.2: "The wheel touches the road with its whole rim". It touches at one point at a time; "any point of its rim can touch"
    is meant. Kind: twice.
57. 7.3: "so it feels the stout's push one step, 2 ms, late; at the swing's period of 343 ms". Which swing? 343 ms is the
    computed swing with the head (2.915 Hz), measured only in 11.2; the bare swing of §4 has 292 ms. Kind: forward.
58. 7.3: "an approximation whose error is of the size of the head's share of the swing's momentum". No number. With
    λ_h k = 0.24 from 6.5, a number is at hand. Kind: no number (minor).
59. Table 3: in the "Standing still, one push" row the Speed and Stored columns render as "0" and "5 s" run together
    ("05 s" in the text flow). Kind: figure (minor).
60. Table 2: "24 × 10⁻⁵ kg m²" is an odd way to write 2.4 × 10⁻⁴; "2 Ω" in italic. Kind: figure (minor).

Verdict §7: **clear, leave it**, apart from 57.

## §8 · How the computer does it

61. 8.2 (★): "the hand-over to the grid multiplies it by (sin(κΔx/2)/(κΔx/2))²". Where the sinc² comes from (the Fourier
    transform of the tent function) is not said. Kind: skipped step (★, grad).
62. 8.2: the result "APIC removes this loss" is not restated outside the star, and 11.2 then finds the method still adds
    ζ ≈ 0.0105, half of the 0.019 that 8.2 says plain PIC would add. Where does the remaining 0.0105 come from (curvature
    of the field, the free surface, the level set, the pressure solve)? No picture is offered anywhere. Kind: picture.
63. 8.4: "a discrete form of Poisson's equation ∇²p = (ρ/Δt)∇·u". Here u is the velocity before the pressure step; the same
    symbol is the true (divergence-free) velocity in (3). Kind: two meanings (minor).
64. 8.4: "the second-order boundary condition Batty and co-workers use". "Second-order" (error falling as Δx²) is not
    explained. Kind: undefined (minor).
65. 8.4, "The head's mass in the pressure step": this is the heaviest algebra in §8 and is not starred, while 8.2 is. Kind:
    structure.
66. 8.4: "a load lagged by one step overshoots on every wave for which the head outweighs the stout the wave moves,
    λ_h k > 1". "A short estimate shows" — but the estimate is not shown. Kind: skipped step.
67. 8.5: "in the rare column where the second finds none, it takes the top less 0.68 of a cell and counts the column".
    "Counts" — counts it for what? (Presumably a tally of fallback columns.) Kind: twice.
68. 8.6: "the conjugate-gradient method used in steps 4 and 7 improves a trial solution …". The method was already
    described in 6.6, and 8.4 says "met in section 6.6". The explanation appears twice. Kind: minor.

Verdict §8: **clear in its picture (particles and grid, the order of steps, the "pint would stir itself" argument is
excellent); needs small work**: 62, 66, 65.

## §9 · The books

69. "Together they must equal the 91.314 mL served." Example 2.1 gave the head as "π R² h_f = 91.26 mL". Which is it, and why
    do they differ (the grid's open areas in the columns, I guess)? Kind: inconsistent.
70. "E_p(0) − E_p(t) = E_k(t) + D(t) … for a pint at rest all three terms should be zero." Then: "The stout's kinetic plus
    potential energy fell by 25.4 µJ in those 2 s". How much of that is booked as heat D, and does (36) balance? The
    equation is set up and then not checked with numbers. Kind: no number.
71. "the particles settle very slightly into the lattice the pressure step prefers". What lattice, and why does the
    pressure step prefer one? Kind: picture.

Verdict §9: **needs small work**: 69, 70.

## §10 · What the page shows

72. "the reddish edge of the stout where light passes through little of it". Should be "where it is thin, so light passes
    through"; as written it reads backwards. Kind: twice (minor).

Verdict §10: **clear, leave it.** The "What is data and what is drawing" box is what CLAUDE.md asks for.

## §11 · What the computed rides show

73. 11.2: "By (13) that push would leave a bare, undamped first mode swinging with 5.2 mm at the wall, 5.0 mm on the ring we
    read." The conversion (multiply by J₁(k r_ring)/J₁(ξ) = 0.955) is not given. Kind: skipped step.
74. 11.2, Figure 3: the bare curve's first peak is about 4.4 mm and first trough about −4.8 mm, against the 5.0 mm predicted
    for the ring. Not commented. Also the label "the push" is printed across the grey curve. Kind: figure.
75. 11.2: "the grid of 1.5 mm carries the swing a little slowly". Why a grid lowers the frequency (the surface, or the
    effective radius, shifted by part of a cell?) is not said. Kind: picture.
76. 11.2: "What should we expect for the frequency?" A rhetorical question; the 21 October verdict forbids them. The
    heading "11.4 Can the heave pump the swing? ★" is a question too. Kind: voice.
77. 11.2: "The computed 2.915 Hz is 3.0 % lower still." Left unexplained, and section 6 offers no damping estimate to judge
    0.425 against (mark 49). Kind: picture / no number.
78. 11.3: "We ran the cart of the code alone … with its motor current set every millisecond to hold the speed, as in the
    rides named 'speed held only'". The speed loop is built only in 12.2. Kind: forward (minor; 11.5 says so for itself).
79. 11.4: "The roads here shake the glass by at most 12 m/s²". From Table 4, g + a_z runs from −2.4 to 20.6 m/s², so
    |a_z| ≤ 12.2 m/s². The reader must do this; one clause would. Kind: skipped step (minor).
80. 11.4: the result "the heave cannot pump this pint's swing" stands only inside the starred subsection; 12.8 relies on it.
    Kind: skipped step (mark 14).
81. 11.5, five bumps: "A tiny lump of foam, 0.01 mL, broke over the rim at 1.50 s." The lean is 13.9 mm, so the wall rises
    about 7 mm, below the 7.6 mm of Example 6.2 at which foam breaks off. Why did it break? (Outward acceleration lowers the
    threshold, or the surface is not a pure first mode, so one point rises more than half the lean.) Not said. Kind:
    inconsistent / picture.
82. Table 4, kerb: "Swing, with head 26 mm" is larger than "Swing, bare 24 mm". Every other row has the head reducing the
    swing. The text says "near the stout's rim height either way" but not why the head's swing is larger here (lower
    frequency, so a sudden jolt's kick β_h|Δv|/ω_h is not much smaller). Kind: twice.

Verdict §11: **needs work**: 49/77 (no theory to compare ζ = 0.425 with), 81, 73, 76.

## §12 · Five controllers

83. 12.2: "They were fixed for the cart carrying the stout without its head, M_x = 2.505 kg". Why design for the cart
    without its head when every ride has the head? Kind: twice.
84. 12.2: "ω_c = 2π × 8 Hz, which makes the loop answer well above the stout's swing". What "answer" means (the loop's
    bandwidth) is not said. Kind: undefined (minor).
85. 12.3: "on a path of slope z_a' its push along the road is −N z_a'". z_a (the height of the axle) is never defined; the
    reader meets only z_r, the road. And why the horizontal part of a force normal to the path is exactly N z_a' (N being the
    vertical part) is not said. Kind: undefined / skipped step.
86. 12.3 with Figure 4: "The speed still falls, to 1.29 m/s: a loss of 0.21 m/s". In Figure 4 the dashed wine curve first
    rises to about 1.57 m/s (full current from 4 ms before the touch) before falling to 1.29, so the sudden loss in the jolt is
    about 0.28 m/s, not 0.21. The 8.3 mm estimate uses 0.21. Kind: inconsistent.
87. Figure 4: the thin wine line (the motor's push as delivered) lies almost everywhere under the thick tan line and cannot be
    seen. Kind: figure.
88. Example 12.2: "At 1.5 m/s the preview reads the road vτ_i = 3 mm ahead. The axle's path is at most 0.251 steep on the
    five bumps". The five bumps and the single bump are ridden at 1.0 m/s (look-ahead 2 mm). Kind: inconsistent (minor).
89. 12.6: "We look for the feedback δi = −Kx … in the sense that it makes J … as small as possible." Good. But "The idea
    behind it is short. If xᵀXx is the least cost still to come …" packs a dynamic-programming argument into two sentences.
    Fine under ★; the plain result is restated in the Key result box. No mark beyond this note.
90. 12.6: "The two level probes on the glass (12.7)". Forward, acknowledged. Minor.
91. Example 12.4: "the filter lowers its speed by -9.5 mm/s and at once raises the swing's rate by 11.7 mm/s … by about β_h
    times as much (here -1.23 with the sign of a forward surge)". "Lowers by −9.5" is a double negative, and "−1.23 with
    the sign of a forward surge" I had to read three times to see it is the ratio 11.7/(−9.5). Kind: twice.
92. 12.7: "Both are modelled as white noise". Good definition. But "a_q is what the one-mode model gets wrong about the
    swing" has units of acceleration of q (m/s²), not said. Kind: undefined (minor).
93. 12.8: "a swing of that size would unload it" (the tyre's 1.1 mm static compression). "Swing" has meant the stout's
    rocking throughout; here it means the wheel's vertical motion. Kind: two meanings.
94. 12.10: the gentle roads. Joint control cuts the lean 13-fold, but it does three things at once (slosh LQR on the motor,
    the cancellation (49), the suspension (52)), and no gentle-road ride uses the slosh LQR alone. The reader cannot tell
    which of the three did the work; the cancellation current is tiny (0.016 A), so it is the LQR or the suspension. One
    sentence saying which (or that it is not known) would close it. Kind: picture.
95. 12.10, kerb: "the first surge is as large under each (Figure 6): leans of 23.9 (preview), 21.8 (slosh LQR) and 25.4 mm
    (joint)". These are the largest leans of Table 8, which need not be the first surge. Figure 6 shows the curves differ
    mostly at the second peak near 1.0 s (preview and speed loop reach ~20 mm there, the slosh LQR much less). Kind: twice.
96. 12.9 box: "agree to 4e-13 A … 6e-08 A … 8e-06". See mark 13.

Verdict §12: **clear for its size, needs small fixes**: 86 (the Δv used for the 8.3 mm), 85, 94, 91. The waiter's habits are
the right picture; 12.3's "what no controller can do" is the best argument in the note.

## §13 · Limits, and the next model

97. "Drops … On these rides almost none leave the glass." The stout spilled is 0 g in every ride (Tables 5, 8); "almost
    none" asks for the number (how many particles were drops at most). Kind: no number.
98. Problems: see mark 44 for Problem 2's answers.

Verdict §13: **clear, leave it** (one number in 97).

## §14 · Sources

99. [14]: "2nd ed., Princeton University Press (2021), version 3.1.5 of 24 July 2020". A version dated a year before the
    edition; the link is the 24 July 2020 public PDF. Say "the authors' online version 3.1.5 of 24 July 2020 of the 2nd
    edition". Kind: twice (minor).
100. All 18 sources carry a link (checked in the rendered HTML). No mark.

Verdict §14: **clear, leave it.**

---

## Summary of verdicts against STANDARD §4

| Section | Verdict | The marks that matter |
|---|---|---|
| Abstract, 1 | clear, leave it | 15, 16 |
| 2 | needs work (small) | 19, 21, 22 |
| 3 | clear, leave it | 28 |
| 4 ★ | clear; one structural fix | 31, 32 |
| 5 | clear; small fixes | 39, 41, 44 |
| 6 | **needs work** | 49, 50, 47, 48 |
| 7 | clear, leave it | 57 |
| 8 | clear picture; small work | 62, 65, 66 |
| 9 | needs small work | 69, 70 |
| 10 | clear, leave it | — |
| 11 | **needs work** | 49/77, 81, 73, 76 |
| 12 | clear; small fixes | 86, 85, 94, 91 |
| 13 | clear, leave it | 97 |
| 14 | clear, leave it | 99 |

The two largest gaps: section 6 never predicts how strongly the head damps the swing, so the note's headline result
(ζ = 0.425, "the strongest brake") is measured but never explained; and the sudden-kick result (12)–(13), which the whole
second half uses, sits unrestated inside the starred section 4.

**Number of marks: 95.** The list has 100 numbered items; 27, 89 and 100 are "no mark", and 96 and 98 only point back to
marks 13 and 44. 54 and 80 are kept as marks because they name the missing restatement in their own sections.
