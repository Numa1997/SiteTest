# Fig. 12 (Kaggle), round 0: the student reader

Reader: a strong final-year school student or first-year physics undergraduate (calculus, Newton's laws, simple harmonic
motion; no fluid dynamics, no control theory). A physics graduate's eye is used where noted ("grad").

How it was read: `npm run build`. Then the page was opened in headless Chromium (Playwright, system Chrome) at 1400 × 1000.
I clicked "Expand all" and read the whole `<article id="paper">` as it renders: the text, the four figures, the nine tables
and the boxes. Each figure and table was also captured on its own. KaTeX: 0 render errors. At 1400 px no display or table is
wider than its column. At 390 px, Tables 2, 4, 7, 8 and the Example 6.1 table are wider than the column. I did not check
whether they scroll sideways.

Note on the build: `dist/` has no `data/fig12/`. Served from `dist/`, the figure above the note shows "data not loaded:
Failed to execute 'json' on 'Response': Unexpected end of JSON input". So I served `public/` instead, and the stored rides
loaded and played. This may be on purpose (the data could be deployed another way), but it is worth checking.

Each mark gives: the section, the exact words, and why I stopped. A one-line verdict against `notes/STANDARD.md` §4 and the
21 October verdict closes each section.

---

## Above the note (the figure the note keeps calling "the figure above")

1. **Hero and §1:** "The same pint and cart as Fig. 12". The eyebrow says "Fig. 12 computed on Kaggle", the reference list
   has "The lecture note of Fig. 12 on this site" [14], and §3.2 says "the equation (17) of the Fig. 12 note". The page
   I am reading is itself labelled Fig. 12, so I cannot tell which Fig. 12 is meant at each point. The note never says in
   one sentence that there is a sister page, computed in the browser, with its own note.
2. **Ride buttons vs the note's names.** The buttons say "speed held only", "joint control", "slosh LQR" and "road
   preview". The note says "speed loop", "joint design", "slosh regulator" and "road preview". "LQR" is not defined until
   §11.5. I had to guess that "joint control" means "joint design".
3. **Reading "drops and lumps in the air"** (panel label) vs §9: "in flight, or come to rest on the cart's body". The label
   says "in the air" but the count also includes lumps resting on the cart.
4. **Run panel:** two buttons both read "Ride again". After the ride, the time slider shows "8.00 of 8.0 s", but its filled
   bar stops about halfway along. I cannot match either to the §9 text "at the end of the stored time it stops and offers
   to ride again".

## Abstract

5. "the first two together give a damping ratio of 0.011". "Damping ratio" is used before it is defined (§4.2). Also, wall
   plus skin is 0.0102; it is 0.011 only with the bulk added (§4.3). A careful reader adds it up and gets a different number.
6. "1.4 % below what (15b) predicts". This is an equation number in an abstract, before any equation exists.
7. "the site's joint control", "the slosh regulator". Both names are used here with no gloss.

Verdict: needs work. The abstract is a dense list of results, and its terms (damping ratio, yield stress, joint control)
come before their definitions.

## 1 · A full pint on a bumpy floor

8. "Section 7 ... a test that stopped a run on 13 November 2026". A "run" and why a run can be "stopped" mean nothing yet.
   The reader also does not yet know there were several runs (3, 4, 6, 7, 8, version 9), and keeping them apart becomes the
   main difficulty later (see mark 66).

Verdict: clear, leave it. The everyday picture of carrying a pint is good. Only the "run" vocabulary needs one sentence.

## 2 · The pint, measured

9. "the project's research notes derive from that distribution as R₃₂ = 34 µm". This is a claim whose support the reader
   cannot see. Turning a mean diameter of 61 µm into a Sauter radius of 34 µm needs the shape of the distribution, which is
   not given.
10. "liquid fraction ... 0.27, a value derived in the same notes from how a 19 mm column of such bubbles drains, not a
    measurement". The derivation is not shown and not cited. Yet Φ = 0.73 drives G₀ and τ_y in §5, which depend strongly on
    Φ − Φ_c = 0.095. A change of 0.02 in the liquid fraction moves τ_y by about 40 %. That sensitivity is never said.
11. "Völp and Willenbacher measured both on degassed Guinness at 20 °C". The stout is served at 6 °C (§2, first
    paragraph). Grad: nothing says whether γ and E_∞ change between 20 °C and 6 °C.
12. Example 2.1: "On the computer's grid the head covers the open part of 2217 columns". Grid, "columns" and "open part"
    are first explained in §7.1 and §8. This is a forward reference that a student cannot decode here.
13. Example 2.1: "91.31 mL in all, against πR²h_f = 91.26 mL for a flat disc". Why the grid's volume is larger, and
    whether 0.05 mL matters, is not said.
14. Figure 1: the labels "floor, 16.3 mm" and "widest, 39.3 mm at 116 mm" do not say radius or diameter. The text says
    the floor is "32.6 mm across (R = 16.3 mm)", so the label is a radius, but on the drawing it reads like a width.
    Also, the label "R" sits in the cream head band, above a short wine line at 125 mm. It took me a moment to see that R
    is the half-width at the fill, not something about the head.

Verdict: needs work (marks 9, 10, 12). The model inputs are stated with sources, which is good. The two derived numbers
need their derivation or a citation.

## 3 · The rhythm of the surface ★

15. Lead: "a sum of standing waves, the modes of the glass". "Mode" is used as if known. A school student knows standing
    waves on a string, but not "modes of a glass". One sentence linking the two would do.
16. "the Navier–Stokes equations ... (1)". The physical reading that follows is good. But "∇", "∇²" and "(u·∇)u" are not
    explained for a reader who has never met vector calculus. A school student stops at the first line of (1).
17. 3.1: "its flow fades with depth over 1/k = 21 mm (see (3) below)". k is used before it is defined. This is a forward
    reference in the first sentence of the subsection.
18. 3.1: "Kelvin's circulation theorem", "the gradient of a potential", "Laplace's equation". These are three new ideas in
    one sentence, with no picture of what irrotational flow means.
19. 3.1: "J₁ is the Bessel function of order one; it solves the radial part of Laplace's equation". Bessel's equation is
    never written, and there is no sketch of J₁. A student has no way to see why J₁′(kR) = 0 has its first root at 1.8412.
20. 3.1: "Bernoulli's law ∂φ/∂t + gη = 0". A student knows steady Bernoulli (p + ½ρv² + ρgz = const). This unsteady,
    linearised form is new, and the step from one to the other is skipped.
21. 3.1, after Example 3.1: "rises at the front wall (θ = 0), falls by as much at the back wall". This is the first and
    only physical picture of the mode, and there is no figure of the tipped surface J₁(kr) cos θ. Figure 1 shows the
    glass at rest. A picture of the first mode is the one figure this section needs.
22. 3.2: "orthogonal with the weight r". This is the Sturm–Liouville idea, stated with no reason. It is starred, but the
    unstarred restatement does not explain what "β" means physically either.
23. Example 3.2: "A steady push tilts the whole surface at right angles to the effective gravity, and the wall rises by
    Ra/g". Grad: by (6), a steady a gives the first mode q = βa/ω² = 0.837 Ra/g. The other 16 % sits in higher modes. The
    example then uses Ra/g (0.88 m/s²) right after deriving 0.837. A reader comparing the two stops here.
24. Example 3.2: "By (6) it gives q̇ the jump −βΔv". Compare §11.2: "gives the swing at once the rate q̇ = βΔv". The
    sign flips between the two (§11.2 means a loss of speed, but it does not say Δv < 0 there).
25. "One more number makes the five-bump road of section 6 dangerous. Its bumps are 0.29 m apart". This is a forward
    reference to a road that has not been described yet.

Verdict: needs work. The derivation is complete and checks out (I re-derived (5), c₁, β = 1.541 and the 3.421 Hz). But the
unstarred reader gets no picture of the mode (mark 21), and the "starred" boundary does not hold: the intro paragraph with
(1) is unstarred but needs vector calculus.

## 4 · Three thin layers

26. 4.1: "Try u′ = Re[û e^{iωt − (1+i)y/δ}]". A complex trial solution is fine for a grad. The section is starred, but the
    unstarred result (δ = √(2ν/ω), a third of a grid cell) is restated only inside the derivation, not in a Key-result box.
27. 4.1: "lowers the frequency by the fraction ζ_wall of 4.2 below, half a per cent". ζ_wall is a symbol from the next
    subsection.
28. 4.2: "Take the mode (2) with amplitude B in φ". Equation (2) has no amplitude, so B appears from nowhere.
29. 4.2: "By the divergence theorem this volume integral equals the surface integral ½ρ∮φ ∂φ/∂n dS". The step uses
    ∇²φ = 0, which is not said. ∂/∂n is not defined.
30. 4.2: "A useful check is the form engineers use ... ζ_wall = 0.5575 ν^{1/2} R^{−3/4} g^{−1/4}". The constant 0.5575 is
    not derived. One line is needed: put ω = √(gξ/R) into (9).
31. 4.3: "the surface behaves like a lid". This is the key assumption for the skin damping, and it has no number. Is
    E_∞ = 18.7 mN/m stiff enough to make the surface inextensible at 3.4 Hz? Grad: the standard criterion compares E_∞
    with ρ(νω)^{1/2}/k or similar, and it is not checked.
32. 4.3: "The same calculation as in 4.2, now with the horizontal velocity at z = h, gives σ_skin = ..., ζ_skin = 0.0051".
    This is a skipped step, and the result equals ζ_wall to four digits. I stopped to ask whether this was a copy error. It
    is a near-coincidence: k/2 = ξ/(2R) against (ξ²+1)/(2R(ξ²−1)), that is 1.841 against 1.837. One sentence saying so
    would stop every reader here.
33. Key result: "halves in ln 2/(2πζ) = 10 swings". Correct (10.3). Problem 12.2 then says 10.3, so the box and the
    problem round differently.

Verdict: needs work (marks 27, 31, 32). The physics of the Stokes layer and Figure 2 are clear, and Figure 2 matches (7).

## 5 · The head of foam

34. 5.1: "two laws describe their measurements [3, conclusions]". The 0.25 prefactor and the Φ(Φ − Φ_c) form are
    empirical fits. That is said only in the Sources list ("the prefactors a_d = 1, k_d = 0.25"), not here.
35. 5.2: "the films give 7.5 Pa and the corners 4.2 Pa". (12) does not label which term is films and which is corners.
36. 5.2 vs 5.4: "Ca = μγ̇R₃₂/γ" (12) and "Ca = μv_s/γ" (14). One symbol has two definitions.
37. 5.3: "w(x, y)". In 4.1, y was the distance from the glass. Here it is a horizontal coordinate.
38. 5.3: "the head between them is sheared on vertical planes at the rate γ̇ = |∇w|, and over its thickness h_f it resists
    with the force per unit area of surface ∇·(h_f τ ∇w/|∇w|)". The force law is stated, not derived. A small sketch (two
    columns, the head between them) would carry it.
39. 5.3: "in one implicit step", "solved by conjugate gradients". These are two methods named with no explanation. They
    come back in 7.3, also unexplained.
40. 5.3: "the friction of the head's edge on the glass (5.4 below)". κ is defined in the next subsection.
41. 5.3: "The head resists a swing of wavenumber k with a force per area of order h_f τ_y k". The order-of-magnitude step
    is skipped. Why one factor of k and not k²? The 0.5 mm that follows is used again in §10.
42. 5.4: "The coefficient κ in (13) is τ_edge h_eff/|w| times the length of glass per area of column". I had to read
    this twice. "Length of glass per area of column" is a new quantity with no symbol and no value.
43. 5.5: "(15) ρ_f(g_eff ε/2 + a_out ε) ≥ τ_y". There is no picture of the part above the rim. Which face is "its free
    face"? Which is "its base"? Why does the weight term carry ½ and the inertial term not? A cross-section sketch is
    needed.
44. 5.6: "The first part is the weight of 5.5". I read this as "a weight of 5.5 (Pa?)" before seeing that it means
    section 5.5.
45. 5.6: "η = a cos(kx − ωt)". The symbol a was the glass's acceleration in (6) and Example 3.2, and it is again in §6 and
    §11. Here it is a wave amplitude.
46. 5.6: "ρ/k = 21.4 kg/m², the head adds m_s k/ρ = 0.24 to it". It mixes an absolute mass (21.4 kg/m²) with a
    relative one (0.24). What is meant: the head adds 5.17 kg/m², which is 0.24 of it.
47. 5.6: the step "give together (15b)" is skipped. It is short, but it is the result §10 tests at 1.4 %.

Verdict: needs work (marks 36, 38, 41, 43, 45). There are good physical pictures (marbles, tray). Section 5.6 is starred,
but its result (the head slows the swing by a tenth) is restated unstarred in §10, which is good.

## 6 · The cart, and who pushes whom

48. "a speed loop measures the speed every millisecond and sets the current". This is fine for now, but "speed loop", "PI"
    and "speed held" are three names for one thing across the page (see mark 2).
49. "rounds off short, sharp bumps". There is no picture or number for how much the 40 mm wheel rounds the 0.12 m kerb.
    This matters later, because §11.2 uses the road's own slope πh_b/L = 0.785 for the axle path (mark 74).
50. "the result check check_run.py tests". The page names code files (check_run.py, run_b.py, RUNSET=run8, Stout.step,
    pack_ride.py, frames_current_limited, slosh_lqr, observer_design, CART_COMMON...) in the body text throughout §§6–11. A
    student cannot open them, and they break the prose. In a textbook chapter they belong in a footnote or a single "code"
    paragraph.
51. Table 2: "glass held still, pushed along the road by 1.0 m/s² sin(πt′/0.146 s)". "Held still" and "pushed" contradict
    each other on a first reading. t′ is not defined (time since 0.3 s?).
52. Table 2 caption: "(run 8, 13 and 14 November 2026; the free swing without the head is run 6's)". Run 6 has not been
    introduced. What run 6 is, and how it differs from run 8, is told only piecemeal in §10.
53. "A = (ω₁₁/g)(2R/(ξ² − 1))|∫a(t)e^{iω₁₁t}dt|". This is the "superposition of kicks", stated and not derived. It is
    left as Problem 12.7, but here it carries Example 6.1's 45 mm, 24 mm and 8.5 mm.
54. Example 6.1: "the range of the effective gravity g + a_z: −0.7 to 20.0 m/s²". The picture of the stout feeling
    negative gravity is given after the table, which is good. But "−0.7" means the glass falls faster than free fall
    (the body is pulled down by the spring). That deserves its physical reason.

Verdict: needs work (marks 50, 51, 52). The "who pushes whom" derivation (16) is a model of clarity.

## 7 · How the computer does it

55. 7.1: "seeded two by two by two in every cell it fills (126,399 cells' worth, so 7.93 per cell)". Eight per cell, but
    7.93 per cell? The reader must guess that cut cells at the glass get fewer. "Cells' worth" is unclear.
56. 7.1: "the usual staggered arrangement". It is usual to whom? One small 2-D sketch of a cell with p at the centre and
    u, w on faces would remove three sentences of reading-twice.
57. 7.1, (17): "W_jp the trilinear weight ... the product of three tent functions". This is a good definition. But c_p
    and "a small linear velocity field" have no picture, and APIC is the one method choice the note defends ("keeps the
    swing from being damped"), yet that claim is not measured. §10 later finds the method adds ζ ≈ 0.0105, twice the
    physics.
58. 7.2, step 2: "the liquid's level set is built from the particles (7.4)". "Level set" is used before 7.4 defines it.
59. 7.2, step 3: "far below the limit 1/6 for three dimensions". The stability limit is stated without source or reason.
60. 7.3: "a discrete Poisson equation for p with seven unknowns per row". A student does not know what a "row" is here.
    "Preconditioned by the diagonal" and "conjugate gradients" are not explained (mark 39).
61. 7.3: "(18) ... α ≥ 0.05". Why clamp at 0.05? What breaks below it?
62. 7.3: "Solving them shows that the face behaves exactly as in (18), with two changes: (18a)". The algebra is skipped
    and the subsection is not starred. It is two linear equations, and the three lines that solve them should be shown.
63. 7.3: "(15b) predicts 2.958/√(1 + 0.00513 × 35.2)". The bare number 0.00513 is m_s/ρ in metres. It is not named.
64. 7.4: "run 4 read them at 120 mm, 5 mm low ... where run 4 showed 84 dark dots along the glass". Run 4 is never
    introduced.
65. 7.4: "the tulip is widest at 116 mm (39.3 mm across the radius), so a few columns at the edge have their centre inside
    the glass lower down but outside it at the fill". I had to read this sentence three times. "39.3 mm across the radius"
    is a strange phrase (it is the radius). The geometry (the glass narrows by 0.2 mm between 116 and 125 mm) needs a
    small sketch, or at least the radii at both heights side by side.
66. 7.4–7.5: by now the reader has met runs 3 and 4 and will meet runs 6, 7 and 8 and "version 9". There is no table of
    runs (what changed in each, which page data comes from which). This is the single biggest source of getting lost in
    §§7–11.
67. 7.5: "the Tesla T4 is 32 times slower in double". "T4" is used as if known. It is a GPU model; say so once.

Verdict: needs work (marks 56, 58, 62, 65, 66). Section 7 meets standard item 5 (method, step, why, cost) better than most
notes. But it is the densest part of the chapter, and it has no figure at all.

## 8 · A pint at rest must stay at rest

68. "a guard stops the whole session". "Session" and "guard" are new words for the code's check. This is fine, but say
    once that the guard is code in the run.
69. "The pressure step takes back the full kick everywhere, so at those faces it took back more than was left". I had to
    read this twice. Why the pressure takes back exactly the full kick (and not the braked one) is the crux, and it relies
    on 7.3's hydrostatic property. One sentence pointing back to 7.3 at this point would help.
70. "exactly as much as the same code with every friction and the head switched off (its model inviscid)". "Its model
    inviscid" reads like a code flag, not English.
71. "the rest is taken by the method itself, by the pressure step and the transfers between particles and grid, which keep
    no book of their own". This is a claim without support. In §10 the same remainder is 17.3 of 25.7 µJ, two thirds of
    the loss. The grad wants to know how this was attributed, or that it is a residual by definition.

Verdict: clear, with small fixes (69, 71). Table 3 and Figure 3 agree. The story of the two faults is the best-taught part
of the note.

## 9 · Playing the stored rides

72. "We checked this ... with the packed files of an earlier run, which have the same form". The playback claims are
    supported by a test on different data from what the page now plays. It is honest, but a reader asks why not run 8.

Verdict: clear, leave it (apart from mark 3 on the label). Standard item 6 (equation to screen) is met well here.

## 10 · What the computed rides show

73. "on the ring at r = (13/16)(R − Δx/2) = 31.2 mm". Why 13/16? "q_ring = (2/64)Σ η cos θ". Why 2/64? This is the
    discrete Fourier projection; one clause would do. "5.2 mm at the wall, 5.0 mm on that ring": the factor
    J₁(kr)/J₁(ξ) behind 5.0 is not given.
74. "Run 6, with the head's weight and friction but not its mass, gave 3.278 Hz". Run 6 also gave "the swing without the
    head". So run 6 has two free swings, but Table 2 lists only one task from run 6. I could not keep this straight.
75. "The swing still falls by the factor e in about a third of a period and is gone within one, as section 5.3 predicted
    from the head's yield stress". §5.3 predicted that swings below about 0.5 mm stop, not that a 5 mm swing loses most of
    its energy within one period. The support does not match the claim.
76. Table 4 caption: "for a pure first mode both are twice the swing at the wall". Tilt is read on "the outer ring",
    which is inside the wall, so for a pure mode tilt = 2q·J₁(kr)/J₁(ξ) < 2q. (Grad.) Table 4 indeed shows tilt < lean on
    all three roads.
77. "The run also costs more: ... a step of the rides takes 83 to 89 ms against 79 to 93 ms". The two ranges overlap, and
    the old range is wider at both ends. The numbers do not support "costs more" for the rides (the 101 against 44
    iterations at rest does).
78. "Its budget of 2500 s ran out before the kerb with the road preview, which was computed alone with the same code
    (version 9, commit 726d51a), its controller designed on the swing run 8 measured". This is a forward reference to
    controllers (§11), and commit hashes sit in the body text. I had to read it twice.

Verdict: needs work (marks 73, 75, 77, 66). "What we expect" before "what was computed" is exactly right, and every
number I checked (2.915 Hz, ζ = 0.425, 0.902 × 3.278, the 20 %, 16 %, 29 % and 40 %) recomputes from the stated inputs.

## 11 · Holding the stout still: the controllers

79. Intro: "Run 8 computes the others inside the same loop as the stout" vs 11.1: "Run 6 drove all its rides with the
    speed loop. Run 7 computes the joint design on the same three roads, and the slosh regulator and the road preview on
    the kerb." These are two different runs credited with the same rides. Table 8 says run 8. The 11.1 sentence reads as
    left over from an earlier draft.
80. 11.2, (21): "I_w" and "J_m" are named but given no values. The values appear only inside Example 11.1's arithmetic
    as 0.00024 and 2 × 10⁻⁶, unlabelled.
81. 11.2: "the motor's back-EMF e = b v". Back-EMF is not explained for a school student (a motor is also a generator).
82. 11.2: "on a path of slope z_a′ its push along the road is −N z_a′". z_a (the axle's height) is never defined. "On
    the kerb the slope reaches πh_b/L = 0.785" is the road's slope. §6 says the axle path is rounded by the 40 mm wheel,
    so the axle's slope is smaller (mark 49). Which one is it?
83. 11.2: "Now follow a sudden loss of 0.25 m/s into the stout ... 1.241 × 0.2515/18.32". Where did 0.2515 come from? The
    text said 0.25.
84. 11.3, (23): "ξ = ∫(v₀ − v) dt′". ξ already means 1.8412 (3) and appears in β, ℓ = R/ξ and P_c = ρπR³/ξ² in the same
    chapter. In §11.9 both meanings are in play. This is the worst symbol clash in the note.
85. 11.3: "K_p = M_xω_c/b makes the loop's gain fall to about one at ... the crossover". "Loop's gain" and "crossover" are
    used before L(s) is defined two paragraphs later.
86. 11.3: "for a signal e^{st}". s is complex, which a student meets here for the first time, and then Example 11.2 uses
    j where §4.1 used i for √−1.
87. 11.5: "algebraic Riccati equation", "Riccati flow", "symmetric, positive definite solution". This is starred, so
    acceptable. But the unstarred Key result after 11.5 (mark 89) is where the reader who skipped lands, and it has a
    wrong number.
88. 11.5: "within 10 % of the gains used". This is honest. But the reader is left unsure whether the design is right; one
    clause on what a 10 % gain change does to the eigenvalues would close it.
89. **Key result "the head has done most of the regulator's work": "The head already decays it at 9.6 s⁻¹, and the
    regulator adds 29 %."** The text just above gives the head's decay rate as ζω = 7.79 s⁻¹ (and 1/t_d = 7.8 s⁻¹ in §10),
    with the regulator moving it to 10.82 s⁻¹, "the improvement is 39 %". 9.6 s⁻¹ appears nowhere else, and 29 % does not
    match 39 %. Either the box or the paragraph is wrong.
90. 11.6: "variation-of-constants formula", "Van Loan's method", "Joseph's form", "unit circle". These are four named
    techniques. It is starred, and the single-number Kalman explanation ("one number, two opinions") is excellent, so the
    unstarred reader is served.
91. 11.6, "Estimate and regulator together": "a single linear map of ten states". It is not said which ten states (four
    plant, three filter, one integral, current, held command?).
92. **11.7: "M_xω²/(βb) = 2.529 × 424.2/(1.541 × 5) = 139.3 A/m".** ω² = 424.2 s⁻² is ω = 20.6 rad/s = 3.278 Hz, run
    6's swing. But 11.5 says the controller uses run 8's ω = 18.32 rad/s (ω² = 335.6), which gives 110 A/m. The 0.71 A that
    follows and the answer to Problem 12.9 (1.36 A) both use 139.3. Either the text or the code's plant is not what the note
    says.
93. 11.7: "A parametric term pumps a swing only when it beats at about twice the swing's frequency". There is no picture
    (a child pumping a swing by standing and squatting is the everyday one, and the note used the playground swing in §3).
    The threshold "ε = 4ζ" is cited to [14], not derived. This is acceptable for ★, but the result is used to dismiss the
    heave entirely.
94. 11.7: "Floquet's method". Named and not explained, even in one clause ("follow the swing over one period of the
    heave and see whether it grows").
95. 11.7: "s, v_b, v_w, δ". δ was the Stokes-layer thickness in §4. Here it is the tyre compression.
96. 11.8: "The speed loop, the preview and the skyhook of Fig. 12 agree". "Skyhook" is never defined in this note.
97. 11.9: "with the momentum P_c q̇, P_c = ρπR³/ξ² = 0.0558 kg". P_c is new and not derived. Why is the momentum of
    the first mode proportional to q̇ with that constant?
98. 11.9, gentle roads: "The filter followed the probes to 0.03 mm root mean square on both roads, where the probes
    themselves read 0.17 and 0.13 mm". "The probes themselves read" what? The r.m.s. of y_q? I read this twice.
99. 11.9: "(The run's own lean, read from every column, gave 5.4 mm on the single bump with the joint design: a column cut
    by the glass ... read too low. Read from the trusted columns, as here and on the page, it does not appear.)" This
    parenthesis reopens a reading problem in the middle of the result. A reader now doubts every lean in Table 8.
100. 11.9, kerb: the joint design leaves the largest tilt (24.5 mm, against 22.2 under the speed loop) yet spills less
     head (2.00 against 2.44 mL). The note gives no physical reason. A reader expects a larger swing to spill more.

Verdict: needs work (marks 79, 84, 89, 92 are errors or contradictions; 82, 97 are undefined or underived). The waiter
picture is a good everyday anchor, and §11.2's "what no controller can prevent" is the clearest physics argument in the
chapter. But at nine subsections, 21 equations and nine boxes, §11 is longer than §§3–5 together, and it is far beyond
the stated reader (control theory up to LQR, Kalman and Riccati).

## 12 · Limits, and the next model

101. "a wedge of foam sliding on the most dangerous plane through the rim's edge, the textbook estimate for a vertical cut
     in a material with a yield stress, would stand up to twice the height". "The textbook estimate" has no source, and
     there is no sketch.
102. Problems 12.7: "show that |∫a e^{iωt} dt| ≈ π/(2ω)". For a half-sine of exactly half a period, the result is exact,
     a₀π/(2ω) (the unit a₀ = 1 m/s² is dropped). "≈" invites a hunt for an approximation that is not there.
103. Problem 12.10: "(Answers: −2.0980° against −2.0990°)". I get −2.0985° and −2.0993° with ω = 2π × 2.915 and
     τ = 2 ms. Trivial, but the problem asks for four decimals.

Verdict: clear, leave it (apart from 101). The limits are specific and quantified, and the Problems use the page's own
numbers.

## 13 · Sources

104. "Sources 1, 2, 4, 6, 7, 8, 9 and 10 were read in the project's extracts of their full texts ...
     (notes/fig12/research/sources/)". This points the reader to a repository path that a site visitor cannot open.
     (Every one of the 16 entries does carry a link; I counted them in the page source.)

Verdict: clear; only the repository path in the closing paragraph is no use to a site reader.

---

## Overall, for this reader

- §§1, 2, 8, 9 and 12 carry a school student well. §3 needs a picture of the first mode. §§5, 7, 10 and 11 lose this
  reader, mostly through forward references, names used before they are defined, run numbers, and code file names in the
  prose.
- Hard errors or contradictions to fix first: mark 89 (9.6 s⁻¹ / 29 % against 7.79 s⁻¹ / 39 %), mark 92 (ω² = 424.2 is
  run 6's swing, not run 8's), mark 79 (run 7 against run 8 for the controlled rides), mark 24 (sign of the kick), mark 77
  ("costs more" against overlapping ranges) and mark 75 (support does not match the claim).
- Symbol clashes: ξ (mark 84), a (45), δ (95), y (37) and Ca (36). These break the "one symbol, one meaning" rule of the
  21 October verdict.
- Missing pictures: the first mode's surface (21), the spill geometry of (15) (43), the staggered cell (56) and the
  edge-column geometry (65).

Marks: 104.
