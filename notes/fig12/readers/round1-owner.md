# Fig. 12 (Kaggle) lecture note: one reader's marks, round 1

Reader: the owner, BSc in physics (computational and theoretical), reading for pleasure from start to finish.
Page: `public/simulations/guinness-kaggle.html`, `<article id="paper">`, built with `npm run build` and read from `dist/`
over a local HTTP server in headless Chromium (Playwright, 1440 x 1000, "Expand all" pressed, every `details` open). I read
the text as rendered, with each KaTeX formula's source alongside, and looked at all six figures at 1.5x. I recomputed every
number I could from the text (Bessel projection, β, ω₁₁, Stokes layer, wall and skin damping, Sauter radius, foam laws (19)–(21),
h_eff, head-mass frequency (26)–(27), M_x, PI roots, sensitivity, first-peak formula, K₄, Example 12.3, Problems 3, 5, 7, 11, 12).
Where a number checked out I do not mark it. I did not read plan.md or check.md.

Kinds of mark: **[undef]** term or symbol used before it is defined · **[step]** a step is skipped · **[claim]** a claim
without its number or support · **[fwd]** forward reference · **[twice]** a sentence I had to read twice · **[fig]** a figure
whose drawing, labels or caption do not match the text · **[clash]** one symbol, two meanings · **[incons]** two places
disagree · **[wrong]** a wrong number or statement · **[picture]** the physical picture is missing · **[house]** notation or
project matter a reader cannot use.

---

## Header and abstract

1. **[wrong][incons]** Abstract: "the road pushes the cart back with up to 82 N while the motor can push with at most 15 N".
   At 1.5 m/s the drive gives at most (12 − 7.5)/2 = 2.25 A forward, 11.25 N (Example 7.1, Table 7: "at 1.5 m/s at most 2.25 A
   forward"). Figure 4's tan curve sits at about 11 N before the kerb and reaches 15 N only after the cart has slowed to about
   1.2 m/s. The same "15 N" returns in Key result 12.3 ("5.5 times the 15 N the motor can push with (3 A at 12 V)"),
   Key result 12.10 ("the motor's 15 N") and section 13 ("about a fifth of the push").
2. **[twice]** Abstract: "with its head the computed pint rocks 2.915 times a second". By 11.2 the swing rings at 2.639 Hz;
   2.915 Hz is the undamped natural frequency recovered from the fit. A heavily damped swing (ζ = 0.425) does not rock at its
   natural frequency. Same in Key result 11.2: "With its head it swings at 2.915 Hz".
3. **[picture]** Abstract and Table 3: "a sharp 30 mm bump taken at 1.5 m/s, a kerb". A kerb is a step. This road is a
   cosine hump 120 mm long. Minor, but "kerb" is then used as the hump's name throughout.

## 1 · A full pint on a moving cart

4. **[undef]** "The ride list names four: speed held only, road preview, slosh LQR and joint control." "LQR" is not expanded
   until 12.6.
5. **[incons][fwd]** "The table under the readings lists, for every ride, the largest lean of the surface". The table on the
   page has two columns, "tilt, mm" and "lean, mm". The note defines tilt only in 11.1, and the details box of section 10
   speaks of "The largest lean and tilt in the table" before that.
6. **[incons]** "the number of drops and lumps in the air". Section 10 says the count "includes those still flying and those
   come to rest on the cart's body". Those are not in the air. "Lumps" (of foam) are defined only in 6.4.

## 2 · The pint, measured

7. **[step]** "gives the glass as 149 mm tall and 76 mm wide ... scales it to ... 160 mm tall and 85 mm wide". The two
   ratios are 1.074 and 1.118. Was the drawing stretched more sideways than upward? Also, a 160 mm glass with its rim at
   z = 147.5 mm has a 12.5 mm base. Neither point is said.
8. **[twice]** "divided by the rate at which they slide apart". Layers slide past each other. The rate meant is the shear
   rate, the velocity difference per unit distance between layers. "Slide apart" reads as separation.
9. **[claim]** "about twice the value for water". This holds only against water at 20 °C (1.0 × 10⁻⁶ m²/s). At the stout's
   6 °C, water has about 1.5 × 10⁻⁶ m²/s, so the ratio is about 1.4.
10. **[claim]** "for bubbles of 34 µm in a column 19 mm tall that balance leaves a liquid fraction of 0.36 at the bottom and
    0.235 at the top. Reaching it takes 25 to 110 minutes". There is no equation and no source. This is the input on which
    τ_y depends most steeply (6.1), and the reader cannot check it.
11. **[picture]** Same sentence. A liquid fraction of 0.36 means a gas fraction of 0.64, which is Φ_c = 0.635 of (19). By the
    note's own estimate, the bottom of the head sits at the jamming point, with almost no yield stress. Section 6 never says
    that the lower part of the head is barely a solid.
12. **[twice]** "so its top stands at 144 mm, only 3.5 mm below the rim, and the stout's own surface is 22.5 mm below it".
    "It" could be the rim or the top of the head. It is the rim (147.5 − 125).
13. **[incons]** Example 2.1: "π R² h_f = 91.26 mL". Section 9: "the 91.314 mL served". The 0.05 mL gap is never explained
    (column areas against a disc? the glass widening above the fill?).
14. **[step]** Example 2.1: "the cart therefore carries 429.6 g of stout". Nothing in the example gives this. It comes from
    426.6 mL × 1007 kg/m³ in the paragraph above.

## 3 · A liquid in a shaken glass

15. **[wrong]** Example 3.1: "Steady pushes are not what spills a pint; sudden ones are". The example has just shown that a
    steady 0.88 m/s², under a tenth of g, brings the head to the rim. Example 6.2 implies that the foam breaks off at a steady
    ≈ 1.9 m/s² (7.6 mm at the wall). That is ordinary braking. The statement holds for the stout, not for the foam.
16. **[step]** 3.2: "For a liquid that cannot be compressed, adding the same contribution from every direction gives the
    friction force per unit volume μ∇²u". The graduate wants one line here: the general term is μ∇²u + μ∇(∇·u)/3, and the
    second part vanishes by (3).
17. **[picture]** 3.1: "Let the glass move without turning". A cart on one wheel would pitch over. 7.1 adds "like one corner
    of a car". The note never says what keeps the body level (a guide rail? a quarter-car rig?), so the reader wonders why
    pitching never enters.

## 4 · The rhythm of the surface ★

18. **[step]** 4.1: "(6) with p = 0 gives ∂φ/∂t + gη = 0". At z = h + η, (6) gives g(h + η). The constant gh is absorbed
    into C(t) without a word. One phrase would do.
19. **[twice]** 4.1: "here the flow is unsteady and small, so ∂φ/∂t replaces the velocity's square". Nothing replaces
    anything. The ½|∇φ|² term is dropped because it is second order, and ∂φ/∂t was in the unsteady law all along.
20. **[claim]** 4.2: "For Δv = −0.1 m/s, a change of speed you would hardly notice". The change happens "in a time much shorter
    than a swing", under about 30 ms. That is over 3 m/s², a jolt anyone would notice.
21. **[clash]** φ is the velocity potential, φ₁ (set as a different phi) the mode's amplitude, φ_ℓ the liquid fraction,
    and Φ the gas fraction. Later Φ is also a matrix block in (46) (mark 61). Two phi glyphs with different meanings sit in the same lines of 4.2.
22. **[twice]** 4.2: "a push of the form a = 1.0 m/s² × sin(πt'/T_p) lasting T_p = 0.146 s, half a period of the first
    mode". This is half a period of the bare stout. The same push starts the ride with the head, whose swing is slower, and
    the note never says why the push was tuned to the bare swing.

## 5 · Where the swing's energy goes

23. **[wrong]** Key result 5.4: "ζ = 0.0051 + 0.0004 = 0.0055: its amplitude falls by the factor e in 1/(ζω₁₁) = 8.4 s and
    halves in about 19.9 swings". With ζ = 0.0055 and ω₁₁ = 21.49 rad/s, the time is 8.46 s and the count is ln 2/(2π × 0.0055) = 20.1 swings.
    The printed numbers use an unrounded ζ ≈ 0.00555. Problem 2 states ζ = 0.0055 and gives the answers "19.9 swings;
    19.3 s". With the stated data the answers are 20.1 swings and 19.5 s.
24. **[claim][picture]** 5.4: "A clean surface without a head has no such skin in the model." Section 2 measured the stout's
    surface elasticity, E∞ = 18.7 mN/m. A protein film that resists stretching damps waves much as a lid does, and this is the
    usual explanation of why measured sloshing damping exceeds clean-surface theory. The note gives no reason to leave it
    out. It also bears on 11.2's verdict that the method makes the bare swing die "about three times too fast".
25. **[claim]** 5.4: "Under a head of foam the stout's surface cannot slide sideways freely: the model holds the head to vertical
    motion only ... so it acts on the stout like a lid". This is the model's choice, presented as a fact about the head. No
    observation or source says that a real head pins the surface sideways.
26. **[fig]** Figure 2: the black ωt = 0 curve runs through the label "one grid cell, 1.5 mm", the grey curve runs through
    "δ = 0.44 mm", and "ωt = π" sits on the bottom frame. The tick labels mix a hyphen ("-0.5") with a minus sign ("−1").
27. **[twice]** Figure 2 caption: "the outer flow is reached within about 2δ". At 2δ the difference is still e⁻² = 14 %, and the
    drawn curves overshoot to about 1.07 near d ≈ 1 mm. Say "to within 14 % by 2δ" or "within about 3δ".

## 6 · The head of foam

28. **[incons]** The equation numbers run out of order. 6.4 has (24), 6.5 has (25)–(27), and then 6.6 has (23). Likewise, (31)
    appears in 11.4 after (32)–(36) of sections 8–9. A reader looking for (23) or (31) searches backward and does not find it.
29. **[wrong]** 6.1: "The bubbles of the head fill Φ = 73 % of it, more than round spheres can". Ordered spheres fill 74 %. The
    claim is true only for randomly packed spheres (63.5 %), which is what the marbles sentence before it describes.
30. **[undef][fwd]** 6.3: "κ = ... × (length of glass in the column)/(area of the column)". The grid's "column" is defined
    only in 8.1. κ is reused in 8.2 as a wavenumber (mark 41).
31. **[clash]** 6.4: "g_eff,z = g + a_z is the vertical part of the effective gravity". By 3.1, g_eff = (−a, 0, −(g + a_z)).
    Its vertical component is −(g + a_z). The subscript z now names the magnitude with the opposite sign.
32. **[claim]** 6.4: "a wedge of foam sliding on the most dangerous plane through the rim's edge, the textbook estimate for a
    vertical cut in a material with a yield stress, would stand up to about twice the height, 8.1 mm at rest". No textbook is
    named and no formula is given. It is the critical height H_c = 4τ_y/(ρ_f g) of soil mechanics. It needs a source or the one-line wedge balance.
33. **[step]** 6.6: "Over its thickness h_f it then pushes on the stout with the force per unit area ∇_h·(h_f τ ∇_h w/|∇_h w|)".
    The expression appears without its reason. One sentence would supply it: shear stress τ on vertical planes, along the
    gradient of w, summed over the thickness, with the net force per area being its divergence.

## 7 · The cart and the roads

34. **[clash]** N is the tyre's load (7.1), N_g the gear ratio (Table 2), N the number of fluid steps in Σₙ₌₁ᴺ (7.3), and
    N_s the cost's cross term (12.8).
35. **[picture][incons]** 7.2: "The first road is built to be dangerous. ... 0.8 % faster than the bare stout's 3.421 Hz".
    Every ride on this road carries a head, which by 6.5 swings at 3.07 Hz (2.915 Hz computed). The road is 12–18 % off the
    pint that rides it, and only 11.3 says so ("the head's mass has detuned the dangerous road"). The ride's name, "Five
    20 mm bumps in step with the swing", misleads, and the reader wonders why the road was tuned to a stout without its head.
36. **[fwd]** 7.3: "at the swing's period of 343 ms". 343 ms is 1/2.915 Hz, measured only in 11.2. So far the theory has given
    292 ms (bare) and 326 ms (with the head).
37. **[claim]** 7.2: "this rounds off bumps shorter than the wheel, though on the roads here the axle's steepest slope stays the
    road's". For the kerb, the hump's radius of curvature at its top is L_b²/(2π²h_b) ≈ 24 mm, smaller than R_w = 40 mm, so
    the axle path is rounded there. The claim about the steepest slope is plausible but not shown.
38. **[incons]** 7.1: "The body bounces on its spring at √(k_s/M_s)/2π = 2.79 Hz". Example 12.5: "2.75 Hz". The second
    includes the tyre in series. Two numbers for the same bounce, with no comment.

## 8 · How the computer does it

39. **[claim]** 8.2: "The smoothing loss of the plain method now starts only at the curvature of the field, two orders higher
    in κΔx." No number is given for what APIC leaves. 11.2 then measures 0.0105 of extra damping from "the method", more than
    half of the plain-PIC 0.019 that APIC was said to remove. The note never says where the 0.0105 comes from (surface
    reconstruction, the reflection at the glass, time stepping?). The standard asks for the error and its cause.
40. **[step]** 8.4: "for a reason a short estimate shows: a load lagged by one step overshoots on every wave for which the
    head outweighs the stout the wave moves, λ_h k > 1". The estimate is promised but not shown.
41. **[clash]** 8.2: "For a velocity varying as e^{jκx} along one direction, with κ the wavenumber of the variation". Here j is
    the imaginary unit of (13), and in the same paragraph j is the face index (𝒲_jp, u_j). κ was the edge-drag coefficient
    of 6.3.
42. **[clash]** α is the tilt angle (3.4), the slope angle (Example 6.1) and the surface's fraction across a cell (8.4, (33)–(34)).
43. **[incons]** 8.3, step 9: "one that crosses the rim outside the glass's radius becomes a drop in free flight". 8.5: "A
    particle counts as a drop when it stands more than 1.5 cells above the surface of its own column and of the eight around
    it". These are two definitions of "drop", and the note does not say which one feeds the readings and the books.
44. **[wrong]** 8.6: "A step of a ride took 84 to 93 ms on the T4, so each simulated second cost 38 to 48 s". At 500 steps per
    simulated second this gives 42 to 46.5 s. The range does not follow from the step time (or more goes on than the steps).
45. **[twice]** 8.3: "each cell may hand on at most a sixth of its excess to each of its six neighbours". I read it twice. Say
    that the cell's own weight, 1 − 6νΔt/Δx², must not go negative.
46. **[house]** E-notation in prose: "1e-05" (8.4), "1.3e-08 mL" and "9e-15" (9), "6e-03" (Example 12.3), "4e-13", "6e-08",
    "8e-06" (box in 12.9). Hyphens are used as minus signs in "-0.03 mm" (11.2) and "-9.5 mm/s", "-1.23" (Example 12.4).

## 9 · The books

47. **[step][claim]** "Energy gives a sharp form of this ... E_p(0) − E_p(t) = E_k(t) + D(t)". The result paragraph reports only
    "The stout's kinetic plus potential energy fell by 25.4 µJ". D is never given, so (36) is never closed. Did the friction
    books record 25.4 µJ of heat, or is the energy lost somewhere else? "the particles settle very slightly into the lattice the
    pressure step prefers" is offered without support.

## 10 · What the page shows

No marks of its own beyond marks 5 and 46.

## 11 · What the computed rides show

48. **[wrong]** 11.3: "The single big bump would leave enough to break the head (Example 6.2) but not to spill stout." Table 4
    gives 7.1 mm with the head, below the 7.6 mm of Example 6.2. Only the bare stout's 8.5 mm passes it. Table 5 then shows
    0 mL of foam spilled on this road.
49. **[incons]** 11.5: "A tiny lump of foam, 0.01 mL, broke over the rim at 1.50 s". The lean there is 13.9 mm, a wall rise of
    about 7 mm, below the 7.6 mm of Example 6.2. A sentence is needed: the outward acceleration, the moment of g + a_z < 0 in
    Table 4 with the |g_eff,z| rule of (24), or a surface that is not a pure first mode.
50. **[house]** 11.2: "What should we expect for the frequency?" is a rhetorical question. The 11.4 heading "Can the heave pump
    the swing? ★" is a question as a heading. The 21 October verdict rules out both.
51. **[claim]** 11.2: "The computed 2.915 Hz is 3.0 % lower still." It is left there. A guess at the cause (the sheet's
    viscous drag? the head's mass taken one cell too low?) or a plain "unexplained" would help.
52. **[incons]** 11.3: "The kerb slows the cart by about a quarter of a metre per second". 11.5: "The cart loses 0.29 m/s".
    Table 5: "1.21–1.52 m/s" (0.31). Three numbers for one loss.
53. **[incons]** Box "Where the data come from": the speed-held rides come from notebook version 8 and the controlled rides from
    version 10, and Table 8 sets them side by side. The box says only that version 10's controllers use β_h. It does not say
    whether the stout and head model is the same in both versions. If the model changed, the comparison mixes two models.
54. **[fig]** Figure 3: the label "the push" is crossed by the grey curve. The y-axis label reads "q_ring (mm)" with a literal
    underscore, where the text has q with the subscript "ring".

## 12 · Five controllers

55. **[incons][picture]** 12.10, "The gentle roads": joint control cuts the lean 13 and 10 times. Yet 12.6 says the regulator
    adds only 39 % to the swing's decay rate, 12.10 says the cancellation current never exceeds 0.016 A, and 11.4 says the heave
    cannot pump the swing. Which part does the work: the regulator's push against the first surge, or the suspension? No
    stored ride separates them (there is no slosh-LQR ride on the bumps), so the chapter's best result has no physical
    explanation.
56. **[incons]** Table 6: joint control reads "the above; a body accelerometer; ...". "The above" includes the preview's "road's
    slope a little ahead". But 12.8 defines joint control as the slosh LQR plus (49) plus (52), with no preview.
57. **[fig][incons]** Figure 4, bottom: with full current commanded early, the dashed curve first climbs to about 1.57 m/s and
    then falls to 1.29 m/s. The road force (top) is zero until about 25 ms after "first touch". The text says "so that the
    current is already at its limit when the climb begins" and "The speed still falls, to 1.29 m/s: a loss of 0.21 m/s". The
    drop from the peak is 0.28 m/s. The 0.21 used in the first-peak estimate is the net change, which is right only because
    the early speed-up and the drop both fall well inside one swing. Say so, and say when the climb begins.
58. **[fig]** Figure 4, top: the caption says "Dashed grey: ±15 N", but I see only the +15 N line. The ticks 20, 0, −40, −80
    are unevenly spaced, and "-50" uses a hyphen where "−80" uses a minus.
59. **[fig]** Figure 5 caption: "with the speed held the lean swings to more than ten millimetres at each bump". The grey curve's
    positive peaks are about 2.7, 6.6, 8.4, 4.5 and 4.8 mm. Only two or three of its troughs pass −10 mm.
60. **[fig][claim]** Figure 6: from about 1.3 s to the end, all four curves sit near +2 to +4 mm, not at zero, with spikes
    (joint control to about 9 mm at 2.7 s). The text is silent. By 6.6 the head can hold a swing of about 0.5 mm (a lean of
    1 mm), and the free swing settled at −0.03 mm. Is this lost foam on the front side, drops over the trusted columns, or
    reading noise? The reader cannot tell.
61. **[clash]** Δv is a sudden change of speed in 4.2 and 12.3 and the speed error v − v₀ in 12.6, and the same speed error is
    δv in 12.2. Φ (the gas fraction) is a matrix block in (46). k is the wavenumber, the sample index in (45)–(48) and the
    summation index in 12.6. τ is also a time window in 12.7 ("over any time τ").
62. **[undef]** 12.3: "on a path of slope z_a′ its push along the road is −N z_a′". The axle's height z_a is never introduced
    as a symbol. 7.2 speaks of the axle only in words.
63. **[step]** 12.6: "The swing obeys (27) with its damping, q̈ = −ω²q − 2ζωq̇ − β_h a". The a_z term of (27) is dropped here
    without a word, and comes back only in 12.8.
64. **[twice]** 12.2: "the speed returns as fast as it can without overshooting". A double root is the fastest return without
    overshoot for a given ω_c, not "as fast as it can".
65. **[claim]** 12.2: "They were fixed for the cart carrying the stout without its head, M_x = 2.505 kg". Every ride carries
    the head, and no reason is given.
66. **[twice]** Example 12.4: "the filter lowers its speed by -9.5 mm/s" is a double negative. "(here -1.23 with the sign of a
    forward surge)" also needed a second reading.
67. **[twice]** 12.10: "the command at or beyond 3 A in 6 or so pictures". A picture lasts 1/30 s, which is an odd unit for a
    1 kHz command. Does it mean about 0.2 s at the limit? Figure 4 shows the full current for about 75 ms.
68. **[house][undef]** Box in 12.9: "a line-by-line port of those of the site's in-browser version of this figure
    (public/scripts/stout-cart.js: Cart.sample, ...)". The reader was never told there is an in-browser version. File and
    class names do not help someone reading the note.

## 13 · Limits, and the next model

69. **[claim]** "Drops. ... On these rides almost none leave the glass." Give the number. Tables 5 and 8 show 0 g of stout
    spilled, but not how many particles flew.

## 14 · Sources

70. **[house]** The citations [1]…[18] in the text are not links to the list. Sources 16, 17 and 18 are the first ones cited
    (sections 2–4) but are listed last. All eighteen entries carry working-looking links (arXiv, DOI, NASA NTRS, DLMF, Feynman
    Lectures, dimensions.com).

---

## Verdict per section, against notes/STANDARD.md

| § | Verdict | Why |
|---|---|---|
| 1 | clear, small fixes | Good everyday picture and a road map. Fix "LQR" and the tilt/lean table (marks 4–6). |
| 2 | needs work (small) | Every input has its source except the drainage estimate (10). Note that the head's base sits at jamming (11). Explain the 91.26/91.314 gap (13). |
| 3 | clear, one fix | A Taylor-like derivation with the checks the standard asks for. The conclusion of Example 3.1 is wrong for the foam (15). Add the pitch picture (17). |
| 4 | clear, leave apart from slips | Every step of the Bessel projection checks out (c₁, β = 1.541, 16 % steady-push check, (12), (13)). Fix marks 18–22. |
| 5 | needs work (small) | Stokes layer, wall and skin damping all check out and are compared with Miles/NASA. Fix the rounding in the Key result and Problem 2 (23). The bare surface's elasticity is missing physics (24). |
| 6 | needs work | Rich and sourced. Fix the equation numbering (28), the sign clash g_eff,z (31), the unsourced wedge (32) and 6.1's sphere claim (29). |
| 7 | needs work | The 15 N against 11.25 N error starts here and runs through the chapter (1). Add the one-wheel picture (17). The dangerous road is tuned to the wrong swing (35). |
| 8 | needs work (small) | The method is described as the code does it, with step sizes and stability. The cause of the measured extra damping is missing (39). Fix marks 40–46. |
| 9 | needs work (small) | The particle and impulse books are exact. The energy book is set up but not closed (47). |
| 10 | clear, leave | Equation to screen, and data against drawing, as the standard asks. |
| 11 | needs work | A wrong claim on the 25 mm bump (48), an unexplained foam break (49), rhetorical question (50). Otherwise a model of how to read numbers from stored data. |
| 12 | needs work | Thorough and correct in its algebra (PI, sensitivity, LQR, K₄, Kalman, Van Loan, suspension LQR all check). The mechanism of the 13x gain is unexplained (55). Fix two figure captions that do not match their plots (59, 60), Figure 4's timing (57), and the 15 N (1). |
| 13 | clear, one fix | The limits and the next model are named, with numbers. Give the drop count (69). |
| 14 | clear | Real sources with links and page/equation pointers. |

Number of marks: 70.
