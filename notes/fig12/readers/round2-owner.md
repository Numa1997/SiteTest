# Fig. 12 · round 2 · the owner's reading

Reader: BSc in physics (computational and theoretical), reading the note on
`public/simulations/guinness-kaggle.html` (`<article id="paper">`) for pleasure, start to finish.

How it was read: `npm run build`, `dist/` served over a local HTTP server, the page opened in headless Chromium (Playwright,
1400 × 1000), "Expand all" clicked, all `<details>` opened. The rendered text was extracted with the KaTeX sources, and every
figure, table, list and box was screenshotted and looked at. No page errors. Every number I could recompute from the note's own
inputs was recomputed (Python/SciPy): the sloshing frequencies, β, c₁, the Stokes-layer numbers, ζ_wall, ζ_skin, the bulk rate,
K_Λ, R₃₂, p_L, G₀, τ_y, τ_v, C_e, the edge damping ratio (0.62 and 0.36 reproduce at 3.070 Hz), h_eff, the wedge, the head-mass
frequency shift, the cart masses and limits, the crest radius, the PI roots and sensitivity, the q_peak numbers, the Floquet
threshold (ε = 1.709 at Ω = 1.81 ω, reproduced), the slosh-LQR gains and eigenvalues, the suspension gains and eigenvalues,
and the answers to Problems 2, 3, 5, 7, 10, 11, 12. They agree with the note except where a mark below says otherwise.

Kinds of mark: **undefined** (term or symbol used before or without definition), **two meanings** (one symbol, two things),
**figure** (axes, colours or meaning unclear or not matching the text), **skipped step**, **unsupported** (claim without its
number or support), **forward** (forward reference that makes me stop), **reread** (sentence I had to read twice),
**wrong** (wrong number, equation or text), **picture** (the physical picture is missing or misleading).

---

## Abstract and section 1 · A full pint on a moving cart

No marks. The pub, the coffee and the waiter do their job; the plan of the chapter is clear.

## Section 2 · The pint, measured

1. "On top lies the head of foam, 19 mm thick, so its top stands at 144 mm, only 3.5 mm below the rim, and the stout's own
   surface is 22.5 mm below it." **reread.** "it" could be the top of the head (then 19 mm) or the rim (22.5 mm). Only the
   arithmetic tells which. Say "below the rim".
2. "What matters for a foam is the ratio of the bubbles' total volume to their total surface: the surface, through its tension,
   holds the energy that resists deformation, and the volume sets how much space that surface has to fill" **reread.** I read
   it twice and still do not see why this ratio and not, say, the mean radius. One sentence would do: the stress scale is
   γ × (surface per volume), and surface per volume of a foam is 3/R₃₂.
3. "⟨dⁿ⟩ = e^{n m_d + n²s²/2}" **undefined.** ⟨ ⟩ (the mean over the size distribution) is never named; a school reader meets
   the angle brackets here for the first time.
4. "We take φ_ℓ = 0.27, near the middle of that column" **unsupported.** The column runs from 0.235 to 0.36; its arithmetic
   middle is about 0.30. If 0.27 is the value at mid-height of a non-linear profile, say so. Because τ_y moves from 5.4 to
   2.5 Pa between 0.27 and 0.30 (section 6.1), this choice matters.
5. "(in the research notes kept with the code, notes/fig12/research/data-for-solver.md; not a measurement and not a published
   value)" **unsupported.** A reader of the page cannot open a repository file; the note gives neither the equation balanced nor
   its inputs. Either give the balance in two lines or cite it as unpublished without the path.
6. "On the computer's grid the head is laid on the open area of each column" (Example 2.1) **forward / undefined.** "Column"
   and "open area" are defined only in section 8.1/8.4.
7. Table 1 · "The inputs of the model and where they come from" **figure.** Table 1 is never referred to in the text; Table 2
   is referred to first (7.1).

## Section 3 · A liquid in a shaken glass

8. "Let the glass's position along the road and its height being X_g(t)" **wrong** (grammar). "be".
9. "In three dimensions the friction force per unit volume of a liquid like water is μ∇²u + ⅓μ∇(∇·u)" **skipped step.** The
   one-dimensional slab argument is shown, then the 3-D form is given bare; the ⅓ term appears and vanishes with no physical
   word (zero bulk viscosity). Since it vanishes at once, either drop it or say in one clause where it comes from.
10. "for a liquid that cannot be compressed the second term vanishes by (3) below" **forward.** Small, but equation (3) is
    used before it is derived; the incompressibility paragraph could come first.
11. "And the pressure there equals whatever presses on the surface from above, p_s: zero for a bare surface" (eq. 5)
    **unsupported / picture.** Surface tension is dropped from the free-surface condition without a word, although γ =
    44.2 mN/m is in Table 1. With the pint's numbers the Bond number ρgR²/γ ≈ 340 and the capillary correction to ω² is
    γk²/(ρg) ≈ 1.0 %, about +0.5 % on f₁₁, i.e. 3.421 → about 3.44 Hz. The frequency is then quoted to four figures. One
    sentence with the Bond number would settle it (the STANDARD asks for the dimensionless numbers with the page's values).
    The meniscus and the moving contact line are also never mentioned until 5.3's last paragraph.
12. "inclined by the angle ϑ with tanϑ = a/(g + a_z)" **two meanings.** ϑ is used again in 6.4 for the wedge's plane, and
    the azimuth is θ. ϑ and θ are hard to tell apart in Latin Modern. Three angles, two glyphs.

## Section 4 · The rhythm of the surface ★

13. "A reader who skips the derivations will find the results restated in the two Key result boxes." **wrong.** The section
    has three Key result boxes (the first sloshing frequency, the driven swing, a sudden push).
14. "For small motions we also drop (u·∇)u, which is a product of two small velocities" **unsupported.** "Small" is never
    given a number. The parameter is kq (or q/R): in the rides q reaches about 7 mm on the five bumps (kq ≈ 0.33) and about
    12 mm at the kerb (kq ≈ 0.57); Table 4's "45 mm" bare swing is kq ≈ 2.1, far outside the linear theory that produced it.
    The model's regime of validity is missing; it is needed before Tables 4 and 5 are read against (11) and (13).
15. "(we write j and not i, which will be an electric current)" **two meanings** (in practice). i is kept for the current, but
    then (34) uses i as a particle index (x_i, b_i), and (31) uses j as a face index (u_j, 𝒲_jp) after j was the imaginary
    unit. See also mark 40.

## Section 5 · Where the swing's energy goes

16. "for the stout's own damping ratio of section 5.4, ζ = 0.0055" **forward.** Harmless, but a number from three
    subsections ahead.
17. "so the difference u′ = u∥ − U cos ωt obeys (2), with x∥ the distance along the wall, as the diffusion equation"
    **reread.** x∥ is defined after it has been used in the previous clause, and "obeys (2) … as the diffusion equation" is
    hard to parse. Better: "Inserted into (2), with x∥ the distance along the wall, this difference obeys the diffusion
    equation …".
18. Figure 2 **figure.** Two x-axis labels are drawn at the same height and overlap: "◂ one grid cell, 1.5 mm ▸" (centred at
    0.75 mm) runs into "distance from the glass, d (mm)" (centred at 1 mm); on screen it reads "◂ one griddistand, 1.5 from
    the glass, d (mm)".
19. Figure 2 **figure.** The curve labels are placed against their curves. The wine curve (ωt = π/2) is the one that dips
    below zero, the tan curve (ωt = 3π/2) the one that bulges above (correct by (15)). But the wine label "ωt = π/2" sits
    above the zero line and the tan label "ωt = 3π/2" below it, at the right edge where both curves are already zero. By
    position I first paired them the wrong way round. The ωt = 0 curve also overshoots 1 (to about 1.07). The caption says
    every curve "approaches the outer flow … within a few δ_s" and does not mention the overshoot, which is a real feature
    of (15) worth one clause.
20. "Bongarzone and Gallaire give the damping of a mode with m waves around the glass" **two meanings.** m was the stout's
    mass (3.4) and will be again (7.3); here it is an azimuthal number.

## Section 6 · The head of foam

21. "With m_s g = 50.7 Pa the head holds on slopes up to sin α = 0.11, about 6°. That is why it keeps its shape when the glass
    is tilted gently and gives way under a jolt." **picture.** When a glass is tilted gently, the stout's surface stays level,
    so the head is not put on a slope; the slope picture explains what τ_y means but not the "That is why". What the yield
    stress resists in a tilted glass is the wall dragging the head's edge. The sentence makes a physics reader stop.
22. "At the head's frequency (section 6.5) it is 0.62 for a swing of 1 mm" **forward.** The frequency (3.070 Hz) is derived
    two subsections later; the reader cannot check 0.62 here. (It does reproduce at 3.070 Hz.)
23. "65 to 111 times the stout's own friction of section 5.4.of section 5." **wrong** (text). A duplicated fragment: "of
    section 5.4.of section 5." Also 0.62/0.00555 = 112, not 111 (small).
24. "× (length of glass along that strip of surface)/(area of the strip)" (κ, after (22)) **undefined.** Which strip? Of what
    width? Presumably one grid column at the wall, but columns are defined only in section 8.
25. "And the pseudo-force of an outward acceleration a_out of the glass pulls the block outward" **wrong / reread.** The
    pseudo-force is −δm a_g; it points outward when the glass accelerates *inward* (away from that rim). In Example 3.1 the
    foam goes over the back rim when the cart speeds up forward. As written the sign is reversed. Define a_out as the outward
    component of −a_g, or say "an acceleration of the glass away from that side".
26. "A more careful one lets a wedge of foam slide on a plane through the rim's edge inclined at the angle ϑ" **two meanings.**
    See mark 12.
27. "In a swing neighbouring columns move at different speeds" (6.6) and "the top two cells of stout in each vertical stack
    of cells (section 8)" **forward / undefined.** Grid columns and cells again before section 8.
28. "a head of foam can hold the stout tilted by about half a millimetre at the wall, a lean of about 1.0 mm" **unsupported**
    (mildly). The text itself says it is an order-of-magnitude balance with a factor-of-unity "of order"; later (11.2, 12.10)
    this 1.0 mm is used as if it were a number to compare against measured offsets (−0.03 mm, 1.8 and 2.5 mm). Keep the
    "order of" with it when it is reused.
29. "the true coefficient √(νω/2) is smaller, so with the head those layers brake the swing about 6 % too strongly" **wrong**
    (small). Against the theory's 3.070 Hz, √(3.42/3.07) = 1.055, 5.5 %; against the computed 2.915 Hz (11.2), 8 %. Say which.
30. "φ_ℓ" (liquid fraction) next to "φ" (velocity potential, section 4) and "Φ" (gas fraction) **two meanings.** Three phis
    for two different things in neighbouring sections.

## Section 7 · The cart and the roads

31. "drag along the road c_x = 2 N s/m" (Table 2) **picture.** What drag: rolling resistance, bearings, air? A word on what
    it stands for.
32. "at the head-loaded swing's period, about 326 ms" **wrong** (choice of number). 326 ms is the theory's 3.070 Hz; the
    computed swing the rest of the chapter uses (and the controllers are designed for) is 2.915 Hz, 343 ms.
33. "The cart takes each step's push into its own sub-steps during the next fluid step" **forward.** The 0.1 ms sub-steps are
    introduced only in 8.6.
34. Figure 4 caption, "when the axle has reached x = 1.437 m" **undefined.** The origin of x is never given; Table 3 says only
    that each ride starts "1 m before the centre of the first bump". Without x_b the number 1.437 means nothing; give the
    bump's centre (it appears to be 1.5 m, start at 0.5 m).

## Section 8 · How the computer does it

35. "so the system has a few hundred thousand unknowns" **wrong.** The unknowns are the stout's cells, about 126 000 (126 399
    cells of volume, a little more with cut cells), not the 370 386 cells of the box.
36. "The conjugate-gradient method improves a trial solution of a symmetric linear system along a sequence of directions …"
    (8.6) **reread.** This definition sits in the middle of a paragraph on the time step and precision, after the method has
    been used in 6.6 and 8.4. It belongs where CG first appears (6.6).
37. "the sums inside the pressure solver's conjugate gradients and the books of section 9 are kept in double precision, the
    head sheet's in single" **reread.** "the head sheet's" what — its sums, its solve?
38. "in the rare column where the second finds none, it takes the top less 0.68 of a cell, a fixed offset of the code, and
    counts the column (no column needed it in the stored rides' rest test)" **reread.** "counts the column" means tallies it;
    and "no column needed it in the rest test" says nothing about the rides themselves.
39. "Each step therefore removes the fraction (kΔx)²/6 of such a motion, as a strong viscosity would" (8.2) and then "The
    smoothing loss of the plain method now starts only at the curvature of the field, two orders higher in kΔx, and is
    negligible for the swing." **unsupported.** The APIC claim is given without its number; the measured method damping
    (0.0105, 11.2) is the same size as the plain-PIC estimate (0.019), so a reader wants to know how much of it APIC
    actually removed.
40. "u_j = Σ_p m_p 𝒲_jp u_p / Σ_p m_p 𝒲_jp" (8.2), "b_i … x_i" (34) **two meanings.** p was pressure and is now the particle
    index; j was the imaginary unit and is now the face index; i is the current and is now a particle index in (34), while
    (31) used p for the same particles.

## Section 9 · The books

41. "The heat D booked by the frictions in that test was not kept with the stored runs, so (35) cannot be closed here; what is
    kept says that the pint at rest moved by a few micrometres and lost a few tens of microjoules, which is the scale of the
    test's resolution." **unsupported.** Equation (35) is set up and then not used; "the scale of the test's resolution" has
    no number behind it. Either give a resolution (e.g. what 0.02 mm surface quantisation or float32 rounding is worth in
    µJ) or say plainly that the energy book is not available.

## Section 10 · What the page shows

No marks. The "What is data and what is drawing" fold is exactly what a reader needs.

## Section 11 · What the computed rides show

42. "The lean is the height of the surface at the front of the glass minus its height at the back, read on the outermost
    ring … at the radius R − Δx/2 … where a point of the ring falls beside the trusted columns, it is read half a cell
    further in" **reread.** Trusted columns have centres more than one cell inside the glass (8.5), i.e. at r < R − 1.5 mm, so
    the ring at R − 0.75 mm lies outside all of them; it is not clear what "beside" and "half a cell further in" do there.
43. Tables 5 and 8, "largest tilt and lean" **undefined.** Signed or absolute? The kerb's 24.3 mm (speed held) is the swing
    back (Figure 6 shows it at about −24 mm), so it is the largest absolute value. Say so in 11.1.
44. "the fitted swing measured 2.3 mm at the wall, and for that size the edge friction alone predicts ζ_edge = 0.47"
    **undefined / reread.** The swing decays to nothing within a period; which 2.3 mm: q₀ of the fit, the first peak? And
    0.47 is the value at 3.070 Hz; at the measured 2.915 Hz section 6.3's formula gives 0.45 (6 % above 0.425, not 11 %).
45. "Against this damping the method's own loss, 0.0105, is about 2 %." **wrong / unsupported.** 0.0105/0.425 = 2.5 %. And
    the method's loss was measured on the bare stout (free surface); under the head the top layer is a lid, so it is an
    assumption that the same 0.0105 applies. Say it is assumed.
46. "with the head the kerb's swing is even a little larger than the bare stout's, because the kerb's short, hard push
    contains as much at the slower swing's frequency, and β_h/ω differs little from β/ω₁₁" **unsupported** (does not add
    up). β_h/ω = 0.0677 s is 6 % smaller than β/ω₁₁ = 0.0717 s. If the push contained "as much" at both frequencies the head's
    swing would be 6 % smaller, not 8 % larger (26 vs 24 mm). The push must contain about 15 % more at 2.915 Hz than at
    3.421 Hz; give that number (|∫a e^{jωt}dt| at the two frequencies).
47. "trusts the speed sensor to σ_v = 2 mm/s and the probes to σ_q = 0.8 mm" (12.7) **two meanings.** σ was the decay rate
    of section 5 (σ_wall, σ_skin) and is now a standard deviation. Placed here because 11 re-uses ζ = σ/ω; the clash is
    met in 12.7.
48. "The free swing without the head comes from version 6 (commit 4c10527); without a head, the later changes to the head's
    model cannot change it." **unsupported.** That covers changes to the head; it does not say whether anything else (step
    order, friction, probes, surface reading) changed between versions 6 and 8. One clause stating that the stout's code is
    otherwise the same would close it.
49. "tools/fig12/kaggle/stout_jax.py … public/data/fig12/2026-11-14-run10/ … index-jax.json … note_numbers.py …
    build_note.py" (the "Where the data come from" fold) **picture** (form). Repository paths and commit hashes in a lecture
    note are unreadable to the page's reader; a link to the repository would serve better. Minor; it is inside a fold.

## Section 12 · Five controllers

50. "The third habit uses what the first two ignore: the waiter watches the drink." (12.6) **reread.** The waiter's habits
    were listed as pace, easing in, hand against the rocking, knees. By 12.6 the knees (skyhook, 12.5) have already been
    built, so "third" and "the first two" no longer match the order of the subsections.
51. "with |Δv| = 0.28 m/s, β_h|Δv|/ω = 1.241 × 0.28/18.32 = 18.9 mm" **wrong** (rounding). 1.241 × 0.28 / 18.32 = 19.0 mm.
    The product 11.1 mm is unaffected.
52. "a sudden loss of 0.28 m/s within a few hundredths of a second, much less than a swing's period" **unsupported** (mild).
    Figure 4 shows the speed falling over about 40 ms, an eighth of the 343 ms period, with ζ = 0.425 acting during it. The
    impulse approximation then overestimates the peak somewhat; a sentence on the size of that error would complete the
    estimate.
53. "The controllers of the stored rides use the swing the computed stout actually has, measured in the same run before the
    controlled rides: ω = 18.32 rad/s and ζ = 0.425 (section 11.2)" **wrong / reread.** The provenance fold of 11.5 says the
    free swing with the head comes from version 8 and the controlled rides from version 10. "In the same run" contradicts
    that unless version 10 measured the swing again; say which.
54. "with everything the model does not know gathered in f = (F_d, a_q)" (44), then "z[n] = A_d z[n−1] + B_d i[n−1] + f[n]"
    (45) **two meanings.** f is a 2-vector of continuous disturbances in (44) and a 3-vector of discrete state noise with
    covariance Q_d in (45). f was also the radial function of (7) and f₁₁ a frequency.
55. "Choosing it to equal ω²(a_z/g) q, the parametric term carried to the right" (12.8) **reread.** "it" is the current's
    contribution to the right side, −β_h b δi/M_x, not δi itself; written as is, the units do not match.
56. "Its regulator works on the body and the wheel about their resting state" (12.8) / Table 6, "the tyre's load" **reread**
    (small). The table says joint control reads the tyre's load; the regulator uses the tyre's compression d_t. Same thing
    through k_t, but say so.
57. 12.9 "Every limit and every clock" **figure / form.** The subsection is a bare table with no sentence, and Table 7 is
    never referred to anywhere in the text.
58. "Which part of joint control does the work? No stored ride separates them" (12.10) **reread** (form). A rhetorical
    question, which the house standard rules out.
59. "What is left is the motor's regulator: reading the swing through the probes, it pushes against each surge as it begins"
    (12.10) **unsupported** (physics). The inference skips the suspension's effect on the horizontal jolt. By 12.3 the road's
    push along the road is −N z_a′, proportional to the tyre's load N; joint control's suspension softens the body's spring
    to 99 N/m and keeps the tyre loaded (Example 12.5), which changes N on every bump and therefore the backward jolt itself.
    The lower peak current under joint control (1.72 vs 2.40 A) fits that too. The suspension cannot be dismissed by the
    heave argument of 11.4 alone.
60. "Every one of them asked for the full current through the jolt, the command at or beyond 3 A in 6 or 6 stored pictures,
    about 200 to 200 ms" **wrong** (text). Garbled template fill. Table 8 gives 6, 6, 6 and 5 pictures, i.e. "5 or 6 stored
    pictures, about 170 to 200 ms".
61. "the first forward surge is about as large under each (Figure 6): 21.2 mm (preview), 21.8 mm (slosh LQR) and 25.4 mm
    (joint) against 22.2 mm with the speed held" **wrong / reread.** The numbers mix measures. 21.8 and 25.4 are Table 8's
    *leans*; 22.2 is the speed-held *tilt* (its lean is 24.3); 21.2 is in neither table. Name the measure and give all four
    first forward peaks in the same one.
62. Figure 6 caption, "all four curves rise to nearly the same first forward peak … and swing back almost as far"
    **figure.** On the plot the swing back reaches about −24 mm with the speed held and the preview, but only about −12 mm
    under the slosh LQR and −17 mm under joint control. That difference is the clearest effect of control at the kerb and
    the caption hides it.
63. "the head can hold a lean of about 1.0 mm (6.6), the same order, and we have not traced the rest" **unsupported.** See
    mark 28; it is an order-of-magnitude number being compared with 1.8 and 2.5 mm. Also, a regulator with integral action
    on the speed still lets a steady lean stand. The reader wonders why the regulator's q-gain (1229 A/m, i.e. 2–3 A for 2 mm)
    does not act on it. Was it the filter's estimate q̂ that did not see the offset?

## Section 13 · Limits, and the next model

64. The limits list leaves out three assumptions the note made. **unsupported** (missing). (a) Surface tension and the
    contact line in the free-surface condition (mark 11). (b) The linear, small-swing theory used for Tables 4 and the
    controllers, at kq up to about 0.6 in the rides (mark 14). (c) The guided body that neither pitches nor rolls (3.1),
    which for a one-wheeled cart is the largest idealisation of all.

## Section 14 · Sources and the Problems box

65. Problem 6, "telescopes to −P_N" **two meanings.** Section 7.3 called the last step n_e and wrote −P_{n_e}; N is the tyre
    load.
66. Source [5], "the prefactors a_d = 1, k_d = 0.25" **undefined.** Neither a_d nor k_d appears in the text; (19) shows 1
    and 0.25 as bare numbers. Name them where (19) is written or drop them here.
67. Source [1], "(tools/fig12/glass_profile.py)" **picture** (form). Same as mark 49: a repository path in a reference list.

---

## Figures in one place

Figure 1: clear. Figure 2: marks 18, 19. Figure 3: **figure**: the y-axis title "q (ring), mm" and the band label "the push"
are drawn on top of each other at the top left ("q (ring)the push") (mark 68). Figure 4: clear apart from the missing origin
of x (mark 34). Figure 5: clear. Figure 6: mark 62.

68. Figure 3 **figure.** Overlapping labels, as just described.

## Verdict per section against notes/STANDARD.md

| § | Verdict | Why |
|---|---|---|
| 1 | clear, leave it | Picture from experience first, the page and its controls explained, plan of the chapter. |
| 2 | needs small work | Numbers sourced and recomputable; marks 1–7 (ambiguous "it", the R₃₂ sentence, φ_ℓ "middle", repository path). |
| 3 | needs small work | Derivation complete and physical; missing the capillary assumption with its Bond number (11), grammar (8), ϑ (12). |
| 4 | needs small work | The best section: every step there, checked against 3.4. Needs the small-amplitude regime (14) and the box count (13). |
| 5 | clear, two fixes | Stokes layer, energy method and literature check are textbook-grade. Fix the x∥ sentence (17) and Figure 2 (18, 19). |
| 6 | needs work | Physics sound and numbers reproduce, but one wrong sign (25), one misleading picture (21), a typo (23), undefined "strip" (24). |
| 7 | clear, small fixes | Model and limits stated with numbers; period (32), origin of x (34). |
| 8 | needs small work | Method as the code does it, with values and stability numbers; index letters collide (40), unknown count wrong (35), CG definition misplaced (36). |
| 9 | needs small work | Books convincing; the energy check is set up and then not closed (41). |
| 10 | clear, leave it | Equation to screen, with data versus drawing spelled out. |
| 11 | needs work | Measurement honest and well read; the kerb-with-head reasoning does not add up (46); lean sign (43); 2.5 % (45). |
| 12 | needs work | Design derivations complete and reproduce exactly; 12.10 has garbled text (60), mixed measures (61), a rhetorical question (58), a caption that hides the main kerb result (62), and an inference that ignores the suspension's effect on the road's push (59). |
| 13 | needs small work | Honest limits and a good next model; three assumptions missing (64). |
| 14 | clear | Sources real, linked, specific to page and equation; marks 66, 67 are small. |

## Number of marks

68 marks.
