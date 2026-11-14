# Fig. 12 (Kaggle) lecture note: one reader's marks, round 0

Reader: BSc in physics (computational and theoretical), reading for pleasure from start to finish.
Page: `public/simulations/guinness-kaggle.html`, `<article id="paper">`, built with `vite build` and read in headless
Chromium (google-chrome, 1440 x 1100) with every section expanded. I checked the figures, tables, equation numbers (1)–(36),
KaTeX (1257 formulas, no render errors) and the four SVG figures as they render. I recomputed every number I could
from the text. Where a number checked out, I do not mark it. Each mark gives the section, the exact words, and why I stopped.

Kinds of mark: **[undef]** term or symbol used before it is defined, or never defined · **[step]** a step in a derivation
is skipped · **[claim]** a claim with no number or no support · **[fwd]** forward reference · **[twice]** I had to read the
sentence twice · **[fig]** the figure and the text do not match · **[clash]** one symbol has two meanings · **[incons]**
two places in the note disagree · **[picture]** the physical picture is missing · **[house]** project history, file names or
code names that a reader of the note cannot use.

---

## Header and abstract

1. **[undef][fwd]** Abstract: "1.4 % below what (15b) predicts". An equation number in the abstract points into section 5.6.
   The abstract should give the prediction itself (2.957 Hz) or say "the theory with the head's mass".
2. **[undef]** Abstract: "under the site's joint control", "under the slosh regulator". Neither name means anything yet.
   They are defined only in section 11. The figure's ride list calls them "joint control" and "slosh LQR", and the
   note calls them "joint design" and "slosh regulator" (see mark 112).
3. **[undef]** Abstract: "a damping ratio of 0.011". The term is defined only in section 4.2. One plain gloss in the abstract
   would help, for example "the swing loses about 7 % of its height per swing".
4. **[twice]** Abstract: "three thin layers the computer's grid cannot see". The grid has not been mentioned yet. The
   sentence before speaks of "a million particles", so a reader asks: which grid?
5. **[incons]** Hero line above the figure: "The same pint and cart as Fig. 12". The page's own kicker says
   "Fig. 12 · computed on Kaggle", and the site nav highlights 12. Two pages are both called "Fig. 12", and the note
   then cites "the Fig. 12 note [14]" as a separate work (marks 21, 47, 79). I could not tell at first which Fig. 12 was meant.

## 1 · A full pint on a bumpy floor

6. **[fig]** "The figure above shows a pint of stout in the Guinness tulip glass on a one-wheel cart". The figure has no
   number, and the note's own Figure 1 is something else (the glass section). Call it "the animation above the note" or give it a label.
7. **[twice]** "about a million small parcels of stout in the measured glass". "Measured" by whom? Section 2 says the
   shape comes from a scaled section drawing, not a measurement.
8. **[house]** "through a test that stopped a run on 13 November 2026". A date in a lecture note's road map. It reads like
   a lab diary, and it does nothing for a reader who meets the subject for the first time.
9. **[undef][fwd]** "Section 11 puts the site's controllers into the same loop". Which controllers? This is the first
   time controllers are mentioned. One clause on what they are would help (a motor speed loop, a regulator that watches the stout, an active suspension).

## 2 · The pint, measured

10. **[claim]** "taken from a section drawing of the glass scaled to its catalogue size". Whose drawing? No source is
    given, although every other input in Table 1 has one.
11. **[fig]** Figure 1, label "widest, 39.3 mm at 116 mm". The label sits at about z = 60 mm (SVG y = 227, which is
    (365 - 227)/2.3 = 60 mm). At that height the drawn glass is near its narrowest. The widest point, z = 116 mm, is at
    y = 98, up beside the head. With no leader line, the label points to the wrong place.
12. **[fig][twice]** "The inner floor is 32.6 mm across (R = 16.3 mm)" and Figure 1's label "floor, 16.3 mm". In the
    drawing the inner radius jumps from 16.3 mm at z = 0 to about 28 mm by z = 5 mm (path points 397.5 → 424.4 px at
    2.3 px/mm). The flat floor is 32.6 mm, but the stout's bottom is a rounded bowl about 56 mm wide. The text's "narrow
    foot" and the picture do not match at first sight. Also, the label says "16.3 mm" and does not say this is a radius.
13. **[claim]** "which the project's research notes derive from that distribution as R_32 = 34 µm". The reader cannot see
    those notes. Give the distribution (or its parameters) and the one-line calculation, or cite where it is published.
14. **[claim]** "0.27, a value derived in the same notes from how a 19 mm column of such bubbles drains, not a
    measurement". The same problem: an input to every foam law in section 5 rests on a derivation the reader cannot see.
    It matters, because Φ - Φ_c = 0.095 is small and τ_y goes as its square. A liquid fraction of 0.30 would cut τ_y by more than half.
15. **[claim]** "Völp and Willenbacher measured both on degassed Guinness at 20 °C". The stout is served at 6 °C (the
    previous paragraph). The note does not say whether γ and E_∞ change between 6 and 20 °C, or why the difference can be ignored.
16. **[undef]** "dilatational elasticity E_∞". The subscript ∞ is never explained (high-frequency limit?).
17. **[house]** Table 1 caption "(tools/fig12/kaggle/stout_jax.py, lines 33–57)" and source cell "the glass's table,
    guinness-glass.js". These are file paths, not sources a reader can follow from the note.
18. **[undef][fwd]** Example 2.1: "On the computer's grid the head covers the open part of 2217 columns". The grid, its
    columns and "the open part" are defined only in sections 7–8. On a first reading this sentence means nothing.

## 3 · The rhythm of the surface ★

19. **[fwd]** "(section 6 explains what that frame adds)" and "over 1/k = 21 mm (see (3) below)". Two forward
    references in the first paragraphs. The second is easy to remove by giving 1/k = R/ξ in words.
20. **[step]** "Here J_1 is the Bessel function of order one; it solves the radial part of Laplace's equation for a cos θ
    dependence". Separation of variables is assumed, and the reason for J_1 rather than Y_1 is not stated (Y_1 is
    singular on the axis). A graduate fills this in. A school reader, whom the byline invites, cannot.
21. **[incons][twice]** "This is the equation (17) of the Fig. 12 note [14, section 4]." This page is Fig. 12. The
    sentence makes sense only after you find, in the sources, that [14] is another page (beer-slosh.html) with the same figure number.
22. **[incons]** Example 3.2: "A steady push tilts the whole surface at right angles to the effective gravity, and the wall
    rises by Ra/g." The one-mode equation (6) just derived gives, for a steady push, q = βa/ω₁₁² = 2Ra/((ξ²-1)g) = 0.837 Ra/g.
    The note uses the exact answer, Ra/g, without saying that it differs from (6) by 16 %, or why (the higher modes carry the rest of the straight line r).
23. **[twice]** "stays at rest along the line across the glass". Which line? It is the nodal diameter at θ = ±π/2. Say so.
24. **[incons][fwd]** "One more number makes the five-bump road of section 6 dangerous ... 3.448 times a second, 0.8 %
    faster than f_11." This is true for the bare stout. The pint on this page has a head, and its swing is at 2.915 Hz, so
    the bumps come 18 % faster than the swing. Section 10 says so later ("the road no longer pushes in step"). Here the
    claim stands without that qualification, and the reader is set up to expect a resonance the computed pint does not have.

## 4 · Three thin layers

25. **[undef]** 4.1: "the layer is δ = 0.44 mm thick, a third of one grid cell". The cell size (1.5 mm) is given only in
    the paragraph after Figure 2.
26. **[incons][claim]** 4.1: "With the stout's ν and the frequency the code uses, ω = 2π × 3.42 Hz" and "for a swing at ω it
    removes the same energy as the true layer". The pint with its head swings at 2.915 Hz, where the true coefficient
    √(νω/2) is 8 % smaller. Does the code keep 3.42 Hz for every ride? The note does not say what the mismatch costs.
27. **[claim]** 4.1: "Integrating the viscous dissipation μ(∂u/∂y)² through the whole layer gives the same mean power ... as it
    must." This is stated, not shown. One line would do.
28. **[fwd]** 4.1: "lowers the frequency by the fraction ζ_wall of 4.2 below".
29. **[claim]** 4.3: "Either way the surface behaves like a lid". No number shows that E_∞ = 18.7 mN/m is large enough
    to make the surface immobile for this swing. The bare-stout damping (the key result 0.0107) counts a full skin layer
    of 0.0051, half the total, so everything rests on this assumption. A Marangoni-number estimate or a source is needed.
30. **[step]** 4.3: "The same calculation as in 4.2, now with the horizontal velocity at z = h, gives (10)". It is short, but
    the reader must redo it to see where coth kh comes from. One line (Π/E = √(νω/2) k coth kh) would close it.
31. **[claim]** 4.2: "our side-wall factor ... = 0.918 is theirs for a mode with one wave around the glass". Bongarzone's
    eq. (17) is cited, but the reader cannot see the match without the paper. Quote their expression once.
32. **[picture]** 4.2 last paragraph: experiments give K = 5.23, 50 % more than laminar theory, "with K = 5.23 the pint's wall
    damping would be ζ = 0.0077". The code uses the laminar value. The note does not say here which value the code uses or
    why. (Section 12 mentions the contact line, but not this choice.)

## 5 · The head of foam

33. **[clash]** 5.1: "The natural scale of the resulting stress is the pressure inside a bubble, about γ/R." R is the
    glass's radius everywhere else in the note. The bubble radius is R_32. (Also, the Laplace pressure of a bubble is 2γ/r; "about" hides a factor of 2.)
34. **[picture][twice]** Example 5.1: "the head can carry about a tenth of its weight in shear before it flows". The text
    compares a shear stress with a normal stress per area, and I had to stop to find the picture. One sentence would give
    it: a layer of thickness h_f on a slope α slides when ρ_f g h_f sin α > τ_y, so the head would hold on slopes up to about 6°.
35. **[claim]** 5.1: the laws (11) are quoted from Völp and Willenbacher, but their range in gas fraction is not given.
    5.2 does give the range for (12) ("0.80 and above"). Is Φ = 0.73, only 0.095 above jamming, inside the range of (11)?
36. **[twice]** 5.2: "the films give 7.5 Pa and the corners 4.2 Pa". Equation (12) does not say which term is films and
    which is corners. The reader has to guess that the first term is films.
37. **[claim]** 5.2: "our head, at 0.73, lies a little beyond that range". 0.73 against a lower limit of 0.80 is not "a
    little" for a law in powers of (1 - Φ). How large could the error be?
38. **[clash]** 5.3: "at the vertical velocity w(x, y)". In 4.1, y was the distance from the glass and u the velocity in
    the layer. Now x, y are horizontal coordinates. Later u is the x component on the grid (17), the current deviation (11.5) and the active force u_s (11.7).
39. **[step][twice]** 5.3: "the code solves for the new vertical velocity w' of the top two cells of stout, which carry
    the head's forces". Why two cells? Why does the sheet's inertia in (13) use the stout's ρ·2Δx and not the head's own
    mass ρ_f h_f? (The head's mass is added later, in 5.6 and 7.3, but here the reader does not know that yet.)
40. **[fwd][undef]** 5.3: "the pressure step then passes the change down into the stout". "The pressure step" is first
    explained in 7.3.
41. **[claim]** 5.4: "Z = 0.18 and l/r_m = 0.004, her fitted values at liquid fraction 0.25 (held at 0.27)". A contact length
    250 times smaller than the meniscus radius is surprising and is not explained. "(held at 0.27)" I read twice: does it mean "used unchanged at our liquid fraction of 0.27"?
42. **[clash]** 5.4: "Ca = μ v_s/γ" in (14), while 5.2 defined Ca = μ γ̇ R_32/γ. Two capillary numbers share one symbol.
43. **[step]** 5.4: "The power lost per unit area of glass, τ_edge v_s, then goes as v_s^{5/3}". This holds only if the
    second, Ca^{1/3}, term of (14) is dropped. It is small (l/r_m = 0.004), but the note does not say so.
44. **[twice]** 5.4: "κ in (13) is τ_edge h_eff/|w| times the length of glass per area of column, with v_s = |w|". I read it
    twice. Say first that the head's edge slides up and down the glass as the surface rocks, so the sliding speed is the vertical w.
45. **[step][twice]** 5.5, (15): "ρ_f(g_eff ε/2 + a_out ε) ≥ τ_y". The text calls the first term "the stress of the part's own
    weight averaged over its free face". The weight term halves, but the inertial term does not, and a normal load is
    compared with a shear strength. Here the reader needs a sketch of the overhang and the plane it breaks on. (Section 12
    then gives a wedge estimate that is twice as tall, which raises the same question.)
46. **[clash][twice]** 5.6: "Take a small wave η = a cos(kx - ωt)". Here a is the wave's amplitude. In (6) and in sections 6
    and 11, a is the glass's acceleration. Then: "the head adds m_s k/ρ = 0.24 to it". The sentence before speaks of a mass
    ρ/k per area. The head adds m_s = 5.17 kg/m², which is 0.24 of it, not 0.24 kg/m².

## 6 · The cart, and who pushes whom

47. **[incons]** "It is the one-wheel cart of Fig. 12 [14, sections 6–8]". The same self-reference as mark 21.
48. **[twice]** "a body of 1.5 kg on a spring of 600 N/m". Does 1.5 kg include the glass? The pint? Section 11.2 settles it
    ("M_b = 1.5 kg is the body with the glass"), but here the reader cannot tell, and the next paragraph adds the stout's
    mass "in the cart's mass".
49. **[picture]** The cart's body on its spring has its own bounce frequency, √(600/1.954)/2π ≈ 2.8 Hz (Example 11.6 later
    gives 2.75 Hz). That is near the slosh frequency with the head (2.915 Hz). The note never says that the body's bounce
    and the stout's swing sit almost on top of each other, or whether this matters.
50. **[undef]** "a speed loop measures the speed every millisecond and sets the current". Gains, and what "holds the
    speed" means, come only in 11.3. Here it is used as if known.
51. **[claim]** "the stout's momentum relative to the glass P". The head moves up and down with the surface and has mass
    (5.6). Is the head's momentum in P? (16) and the impulse book speak only of the stout.
52. **[incons][twice]** "check_run.py tests that the two agree to one part in a thousand". Section 10 then reports absolute
    differences, "2.0 × 10⁻⁶ ... N s", with no momentum to compare against. One part in a thousand of what?
53. **[picture]** "it feels the stout's push one step, about 2 ms, late". What does a 2 ms lag do to a 343 ms swing? It is a
    phase of about 2°, so it can pump or drain energy. One sentence would answer it (section 12 repeats the fact but not the effect).
54. **[house]** "run 8 takes the pint at rest first, then the free swing ... (run_b.py, RUNSET=run8)". Run numbers, a
    script and an environment variable in the text. The reader does not yet know what runs 3, 4, 6, 7, 8 and 9 are, and
    must keep a ledger of them through the rest of the note.
55. **[undef]** Table 2: "pushed along the road by 1.0 m/s² sin(πt'/0.146 s) for 0.146 s from 0.3 s". t' is not
    defined (time since 0.3 s?).
56. **[twice]** Table 2: "glass held still, pushed along the road". Held still, yet pushed. Say "glass held at rest, then
    given one push", or "speed 0" will confuse.
57. **[claim]** "The push of the free swing lasts half a period of the first mode, which puts the most energy into it for a
    given strength." For a half-sine pulse of a given peak acceleration, a longer pulse adds more. The claim is true only
    for a single lobe with fixed peak and fixed sign. Say what "for a given strength" holds fixed.
58. **[picture]** Example 6.1, "the swing an undamped first mode would keep", computed from a(t) along the road only. The
    same table shows g + a_z from -0.7 to 20 m/s², and the note has just said a vertical acceleration changes the restoring
    force. The note should say here that A ignores the vertical (parametric) effect, and why that is safe (11.7 shows it is).
59. **[twice]** "The kerb stops the cart by 0.29 m/s". It slows the cart by 0.29 m/s.

## 7 · How the computer does it

60. **[twice]** 7.1: "seeded two by two by two in every cell it fills (126,399 cells' worth, so 7.93 per cell)". Eight per
    cell, yet 7.93 per cell. Only after a moment do you see that "cells' worth" means the fill volume divided by a cell,
    and that cut cells get fewer.
61. **[clash]** 7.1, (17): "For the component along the road, u". See mark 38. A fourth meaning of u.
62. **[house]** 7.2: "One fluid step of the code (Stout.step)", and later "Stout.probes", "slosh_lqr", "observer_design",
    "World in stout-cart.js", "PLANT and PLANT_FROM_RUN", "frames_current_limited", "pack_ride.py", "CART_COMMON, Cart and
    make_advance". These are code names. The lecture-note reader cannot use them.
63. **[fwd]** 7.2 step 2: "the liquid's level set is built from the particles (7.4)". The term is defined two subsections later.
64. **[fwd][undef]** 7.3: "at rest run 3 needed 90 iterations per step on average". Run 3 is introduced only in section 8,
    as the failed run. Why quote a failed run's cost here?
65. **[step]** 7.3, (18a): "Solving them shows that the face behaves exactly as in (18), with two changes". I did the
    algebra and it holds, but it takes half a page. Give the one intermediate line, w'(α + M) = αw* - (Δt/ρΔx)(m_s g - m_s w_h/Δt - p_l).
66. **[claim]** 7.3: "Without the head's mass the swing has its own frequency of 2.958 Hz on that grid". On the 6 mm grid
    the bare swing is 14 % below 3.421 Hz. This is not remarked on. (It is fine for a test of the ratio, but the reader wonders.)
67. **[twice]** 7.3: "A pint at rest on a 4 mm grid lost the same potential energy in 1.5 s with and without the mass, 59 and
    61 µJ." Why is this reported? The point (adding the head's inertia does not make a resting pint move) is left to the reader.
68. **[twice][house]** 7.4, the long paragraph: "a column where that field finds none takes the body's top less 0.68
    cell and is counted"; "the tulip is widest at 116 mm (39.3 mm across the radius)"; "run 4 read them at 120 mm, 5 mm
    low"; "where run 4 showed 84 dark dots along the glass". This one paragraph holds six separate rules and two
    debugging stories. Where does 0.68 come from? "Across the radius" is not a phrase. Run 4 is never introduced.
69. **[undef]** 7.4: "Particles within two cells of the glass are mirrored in it". Mirrored how, in a curved wall?
70. **[picture]** 7.5: "At rest run 3 took 72.6 ms per step on the T4." With 2 ms steps that is 36 times slower than real
    time, so an 8 s ride takes about 5 minutes. One sentence would turn the number into a picture.

## 8 · A pint at rest must stay at rest

71. **[twice]** "In the computer the balance is just as exact: gravity's kick in step 5 ... the pressure of step 7". The
    steps are numbered in the rendered list (good), but "step 5" and "step 7" sit a full screen below the list, and the
    list does not show numbers next to the text referring to them. I scrolled back.
72. **[house]** "On 13 November 2026 the guard stopped run 3." Again a date.
73. **[twice]** "On this computer we took one step of 2 ms from rest". Which computer? Is it the reader's, the author's
    CPU, or the T4? Later: "We repeated the test on this computer ... against 2.4, 0.32 and 57.5 µJ there."
74. **[claim]** "The fix is to let the stresses act on the velocity the stout actually has, the last step's, which is free
    of divergence". Step 1 of 7.2 first transfers particle velocities to the grid. That transfer is not divergence-free
    in general. So which velocity do the stresses act on: the grid velocity after the transfer, or the last projected one?
75. **[claim]** "and the rest is taken by the method itself, by the pressure step and the transfers between particles and
    grid, which keep no book of their own". This is plausible but not measured. Has anyone measured how the 0.23 µJ splits between the two?

## 9 · Playing the stored rides

76. **[claim]** "We checked this in a browser without a screen (headless Chromium) on the built page with the packed files
    of an earlier run, which have the same form". So the playback of the rides this page actually plays (run 8) was not
    the one checked. Say so plainly, or check run 8's files.
77. **[twice]** "added up in double precision on the GPU in every picture (run 8 on)". "Run 8 on" means "from run 8
    onwards". On a first reading it looks like a typo.
78. **[house]** "(index-jax.json)" in the fingerprint sentence.

## 10 · What the computed rides show

79. **[incons][twice]** "Run 6, with the head's weight and friction but not its mass, gave 3.278 Hz". Table 2 says only
    "the free swing without the head is run 6's". So run 6 computed both a headless swing and a swing with a massless
    head, and only one of them is used here. It took me three readings to sort out which run has which head.
80. **[twice]** "What we expect": "the head's mass should lower that by the factor 0.897 of (15b), to about 3.07 Hz". The
    result paragraph then compares 2.915 Hz with 2.957 Hz, a different baseline (3.278 Hz, run 6's swing with a massless
    head on this grid). Against the stated expectation of 3.07 Hz the result is 5 % low, not 1.4 %. The switch of baseline
    is correct, but it is not announced.
81. **[incons]** "The swing still falls by the factor e in about a third of a period and is gone within one, as section
    5.3 predicted from the head's yield stress." Section 5.3 predicted that swings below about 0.5 mm stop in finite time.
    It did not predict a decay within one period for a 5 mm swing.
82. **[claim]** Swing without the head: "the method itself adds about 0.0105, twice the physics it is meant to carry". This
    is an important finding, and the note moves on. What does it mean for the rides? The thin-layer model of section 4 is
    then a minority of the damping. Section 12 does not come back to it as a limit with a number.
83. **[house]** "run 8 (Kaggle notebook version 8, 13 and 14 November 2026, code at commit 96e8a1d) ... (version 9, commit
    726d51a) ... (version 6, commit 4c10527)". Provenance belongs in a footnote or a box. In the running text it buries the physics.
84. **[fwd][undef]** "Its budget of 2500 s ran out before the kerb with the road preview ... its controller designed on the
    swing run 8 measured". "Road preview" and "its controller designed on the swing" mean nothing until section 11.
85. **[twice]** "In all three rides the impulse booked on the cart equals minus the stout's final momentum to rounding,
    2.0×10⁻⁶, 2.3×10⁻⁶ and 1.6×10⁻⁶ N s." Are these the differences, or the momenta? If differences, compared with what size of momentum?
86. **[clash][twice]** "so the swing's equation becomes q̈ + ω²q = -βa/(1 + m_s k/ρ)". Here ω is the head-loaded frequency.
    In (6) the same letter meant the bare ω₁₁. The paragraph then says "with the slower swing (Example 3.2) the wall rises
    1/√1.24 ... less". I had to rebuild the argument (rate ÷1.24, amplitude = rate/ω', ω' = ω/√1.24) to see where the square root comes from.
87. **[incons]** "The run also costs more: ... a step of the rides takes 83 to 89 ms against 79 to 93 ms." The second range
    contains the first. The numbers do not show that it costs more per step.

## 11 · Holding the stout still: the controllers

88. **[incons]** Intro: "Run 8 computes the others inside the same loop as the stout". After Table 5: "Run 6 drove all its
    rides with the speed loop. Run 7 computes the joint design on the same three roads, and the slosh regulator and the
    road preview on the kerb." 11.9 and Table 8 then say run 8 (and version 9) computed them. The paragraph after Table 5
    contradicts the intro and the results.
89. **[incons]** Table 5 and the intro: "They are the controllers of the page of Fig. 12 [14, sections 8 and 9]". See marks 5 and 21.
90. **[undef]** 11.2: "c_x = 2 N s/m the coefficient of the drag". Section 6's description of the cart had no drag.
    I_w = 0.00024 kg m² and J_m = 2×10⁻⁶ kg m² appear only as bare numbers inside Example 11.1, with no name or source.
91. **[twice]** 11.2: "on a path of slope z_a' its push along the road is -N z_a' ... On the kerb the slope reaches π h_b/L =
    0.785". π h_b/L is the road's largest slope. The axle's path is rounded by the 40 mm wheel (section 6), so it is gentler
    on a 120 mm kerb. Which slope enters, the road's or the axle's? Example 11.3 also calls 0.251 "the axle's path", but it is the road's π h_b/L.
92. **[incons]** 11.2: "gives the swing at once the rate q̇ = βΔv". Example 3.2 has "the jump -βΔv". The sign changes
    without comment (the sign of Δv is not stated either).
93. **[twice]** 11.2: "the kick drives the swing with β/(1 + m_s k/ρ) = 1.541/1.242". 1.242 uses the theory's k = 47.1 m⁻¹,
    while section 10 just used the grid's k = 44.7 m⁻¹ (1.229) for the same correction. Pick one and say why.
94. **[clash]** 11.3, (23): "ξ = ∫(v_0 - v) dt'". ξ was the Bessel zero 1.8412, and it appears inside β, which sits in the
    same matrix (26) as this new ξ. This is the worst symbol clash in the note.
95. **[clash]** 11.3: "Take s = jω, with j² = -1". In 4.1 the imaginary unit was i. Here j is right because i is the current, but the switch is not flagged.
96. **[house][claim]** 11.5: "The rule of the site, written in its coupling code (World in stout-cart.js), is to give the
    controller 'the first sloshing mode as each model has it'". A design rule is quoted from a code comment. The physical
    argument comes three sentences later and stands on its own. The quotation adds nothing.
97. **[fwd]** 11.5: "with it (28) would give K = (71.12, -1228.72, -40.50, -150.00), within 10 % of the gains used". The
    gains used are given only in Example 11.4, below.
98. **[incons]** 11.5: "With the head the improvement is 39 %" (7.79 → 10.82 s⁻¹, which checks). The key result directly
    after says: "The head already decays it at 9.6 s⁻¹, and the regulator adds 29 %." The two disagree on both numbers. 1/t_d
    = 1/0.128 s = 7.8 s⁻¹, so I cannot find where 9.6 comes from.
99. **[twice]** 11.6: "No noise is added to these readings in the rides, as on the site by default". Does "as on the
    site" mean the site also adds none by default, or that the site adds some? I read it both ways.
100. **[claim]** 11.6: "each probe takes the heights at R - 2.5Δx and R - 4Δx ... and extends the straight line through them
     to R". This is a linear extrapolation of J_1(kr) near its maximum, where it is flat. That is fine, but how large is the
     resulting error in q? The filter trusts the probes to 0.8 mm. Is that number linked to this error?
101. **[incons]** 11.7: "Its size: M_x ω²/(βb) = 2.529 × 424.2/(1.541 × 5) = 139.3 A/m". 424.2 s⁻² is ω² for 3.278 Hz (run 6's
     plant). 11.5 says the controllers of run 8 use ω = 18.32 rad/s, ω² = 335.6 s⁻², which gives 110.2 A/m and 0.56 A
     (not 0.71 A) in the example. Problem 12.9's answer (1.36 A) uses the same 139.3.
102. **[clash]** 11.7: "With k = 600 N/m and c = 8 N s/m the spring and its damper". k was the wavenumber through sections 3–5
     and 11.2. c_t = 5 N s/m (tyre damping) appears here for the first time.
103. **[undef]** 11.8: "The speed loop, the preview and the skyhook of Fig. 12 agree to 4×10⁻¹³ A". "Skyhook" is never defined
     in this note, and it is not one of the four controllers of Table 5.
104. **[house]** 11.8: the port check paragraph ("class Cart with slosh_lqr, susp_lqr and observer_design in stout_jax.py,
     against Cart.sample, Cart.lqrGains ... tools/fig12/kaggle/portcheck/"). This is a software audit, and it is useful to the
     project. In a lecture note it should be a collapsed box or an appendix.
105. **[step][claim]** 11.9: "with the momentum P_c q̇, P_c = ρπR³/ξ² = 0.0558 kg". The coefficient is quoted with no
     derivation. It is the one new piece of physics in the coupling model. It needs at least the integral it comes from (ρ∮φ n_x dS for the mode).
106. **[claim]** 11.9: "the free swing that sets the model's damping is 2 mm high". Section 10 said the push leaves 5.0 mm
     undamped on the ring. Where does 2 mm come from?
107. **[twice]** 11.9: "The joint design also more than halves the spring's stroke (8.4 against 3.3 mm root mean square on the
     five bumps)". The order is reversed from the sentence: the joint design is 3.3 and the speed loop is 8.4. Give it as "3.3 against 8.4".
108. **[twice]** 11.9: "The filter followed the probes to 0.03 mm root mean square on both roads, where the probes themselves
     read 0.17 and 0.13 mm." "Read 0.17 mm" means the r.m.s. of the probe signal? Say "where the probe signal itself had an r.m.s. of".
109. **[picture]** Table 8, kerb: the joint design leaves the largest tilt (24.5 mm) and lean (25.4 mm) of all four, worse
     than the speed loop. The text says "the swing stays as large" and passes on. The reader wants one sentence on why the
     best design on gentle roads is the worst on the kerb (the active suspension? the cancellation current saturating?).

## 12 · Limits, and the next model

110. **[claim]** "Until run 8 the model gave the head weight but no inertia, and a computed pint with a head rocked faster
     than a real one." Faster than which real one? No measurement of a real pint's swing frequency is cited. Sauret's cell
     is not a pint.
111. **[twice]** "Problems" sits inside section 12, "Limits, and the next model", and is numbered 12.1–12.11. That looks
     like subsections of section 12. Problems usually stand as their own unnumbered part, or after the chapter.
     Small: 12.10's answers "-2.0980° against -2.0990°". I get -2.0979° and -2.0988° (ωτ_i = 0.036631). The difference is in the fourth decimal, but an answer key should reproduce.

## Figure on screen against the text

112. **[fig]** The ride list and the table above the note say "joint control", "slosh LQR", "One sharp 30 mm bump",
     "Standing still, one push". The note says "joint design", "slosh regulator", "kerb", "free swing". A reader who
     moves between the note and the figure has to translate each one.
113. **[fig]** Readings panel: "All six numbers are stored with every picture". The panel shows eight readings (speed, stout
     in, stout spilled, head in, head spilled, drops and lumps, motor current, active force), and section 9 describes all eight.
114. **[fig]** Figure 4: the legend inside the plot has "dashed grey: ±15 N, the drive's 3 A", which the caption does not
     mention. At this size the "dotted" curve (the most the motor could give) cannot be told from the wine curve (the
     motor's push as delivered) wherever the two coincide, which is most of the plot.

## Sources

115. **[incons]** [14]: "The lecture note of Fig. 12 on this site", linked to beer-slosh.html. This is the source behind marks
     5, 21, 47 and 89. Give the other page its own name in the text, for example "the in-browser note of Fig. 12".
116. **[claim]** Closing paragraph: "Sources 1, 2, 4, 6, 7, 8, 9 and 10 were read in the project's extracts of their full texts
     ... (notes/fig12/research/sources/)". This is a folder in the repository, not something a reader of the page can open.
     It also means that two key inputs (R_32 and the liquid fraction, marks 13–14) rest on files the reader cannot reach.

---

## General impressions (not counted as marks)

- Sections 3–5 are a pleasure. The derivations are complete enough to follow with a pencil, and every number I recomputed
  (about 120 of them) came out right, except those flagged in marks 22, 98, 101 and 111.
- Sections 7, 8, 10 and 11 alternate between physics and the project's history (run numbers 3, 4, 6, 7, 8, 9; versions;
  commits; dates; file and function names). A reader has to keep a ledger of the runs to follow the argument. One table
  "Runs used in this note" near the start, plus moving code names and port checks into collapsed boxes, would remove most of the house marks.
- The byline promises readers "from school to the second year of university". Sections 7.4, 11.5–11.8 and much of 10 are
  graduate-level numerical and control material, without a ★ and without the "results restated without it" that the byline promises.

Number of marks: 116.
