# Fig. 12 · referee of §11.9 "The nonlinear live model: a swing that softens and swirls ★" (with §11.8 for context)

Read blind, as rendered, by a reader who knows Lagrangian mechanics, the Bessel functions of section 4 and basic perturbation
theory, but not nonlinear sloshing. Working tree of 6 November 2026, `public/simulations/beer-slosh.html`, served from `public/`
with `notes/fig12/serve.cjs` and opened in headless Chromium at 1280 and 390 px. KaTeX errors: 0. Page sideways scroll: none.
plan.md and check.md were not read.

Measured at 390 px (the width of the math column inside each display box, `.eq-rows__math`):

| Element | content width | box width | what the reader sees |
|---|---|---|---|
| (N4) | 246 px | 221 px | the `=` before \(-\kappa_1P_1a_x\) sits in the hidden 25 px; the equation reads "(products with \(p_0,p_2,r_2\)) \(-\kappa_1P_1a_x\)" |
| (N2) | 239 px | 221 px | 18 px hidden, no visible loss |
| Table 5 | 318 px | 299 px | the 3D column is cut ("3.16(", "3.20", "3.10") and so is the caption ("push c…", "amplituc…") |
| (55), §11.8, at 360 px | 223 px | 195 px | hidden overflow (fits at 390 px) |

No question-and-answer form anywhere in §11.8–11.9.

## Verdicts against `notes/STANDARD.md`

**§11.8 The live model: clear except for one point.** The model, the frequencies, the damping, the weir law with its derivation
and source, and Table 4 are all stated, and the agreement with the 3D solver is measured. The exception is the seam with §11.9
(item 10): the subsection opens by calling itself what "the figure runs, by default" and closes by saying that is no longer true.

**§11.9 The nonlinear live model: needs work.** By the items of the standard:
1. Picture: the opening is good (a glass of water shaken at its own frequency). The two effects it promises are never explained
   physically (item 6).
2. Model: the regime and the page's dimensionless numbers are missing. The small parameter is never given a value (item 5).
3. Derivation: the central step, the kinematic condition in modal form, is cited, not shown (item 2). The final equation (N4)
   has undefined symbols and hidden terms (item 1).
4. Checks: the check of \(d_1, d_2\) against [17]'s Table 1 is good. Missing: the linear limit back to (54), and a theoretical
   frequency–amplitude curve to set beside Table 5 (items 1, 6).
5. Method: the integrator and step are named; there is no measured error for the nonlinear system.
6. Equation to screen: the surface comes from (N1) and the cart push from (55). Acceptable.
7. Limits: "Where it stops" is good. The swirl result is left in open conflict with [17] (item 7).
8. Sources: [17] is in the list. Luke, Miles, Narimanov, Moiseev and Lukovsky are named but not listed (item 10).

Form: there is no "Key result" box, and the labels (N1)–(N5) sit outside the note's own numbering (54)–(56).

## Items, in order of severity

1. **(N4), the equation the page runs, cannot be read as printed.**
   - \(\kappa_1\) and \(P_1\) in the forcing term \(-\kappa_1P_1a_x\) are defined nowhere on the page. \(P_1\) also clashes
     with the potential amplitudes \(P_k\) two paragraphs earlier and with the momentum \(P_x\) of (55).
   - \(\sigma_1, \sigma_2\) appear before any definition. Only later does the reader infer that \(\sigma_1\) is \(\omega_{11}\)
     in units of \(\sqrt{g/R}\) ("\(\sigma_1^2 = 1.8412\)").
   - (N5) shows \(d_7, d_9\), so the reader goes looking for \(d_3\)–\(d_6\) and \(d_8\).
   - "(products with \(p_0, p_2, r_2\))" hides the very terms the next paragraph says shift the frequency.
   - Nothing links \(p_1\), a coefficient of the normalised \(R_1 = \alpha_1J_1\), to the wall height \(q\) of (54)/(55) or to
     the "lean" of Table 5.
   - Nothing shows that (N4) reduces to (54) when the swing is small, the obvious limiting case.

   Fix: one sentence defining \(\kappa_1P_1\); the relation \(q = R\,\alpha_1J_1(\xi_{11})\,p_1\); the linear limit written
   out; the hidden products shown, or at least the ones that matter.
2. **The key step of the derivation is cited, not shown.**
   - "The surface moves with the liquid …, which in modal form reads \(J\dot{\boldsymbol\beta} = A\mathbf P\)
     [17, eq. 2.9]" is the step a ★ reader most needs.
   - It takes three lines: note that \(A_k = \int_{Q(t)}\phi_k\,dQ\). Differentiate with the moving surface
     (Reynolds transport), use \(\partial\Phi/\partial n = 0\) on the wall, and apply Green's first identity.
   - Also undefined at that point: \(\phi_k\) (lower case in (N2), capital \(\Phi\) in the text), \(T_k(\theta)\), \(P_k\),
     \(Q(t)\) and \(dQ\).
   - \(T = \tfrac12\mathbf P^TA\mathbf P\) needs its one-line origin, \(T = \tfrac12\int|\nabla\Phi|^2dQ\) with \(\rho = 1\).
   - The units of mass in the dimensionless scheme are never stated, so \(V = \tfrac12\iint\zeta^2dA\) has lost \(\rho g\)
     without comment.
3. **Phone layout (390 px): the equals sign of (N4) is invisible.**
   - It sits in a 25 px hidden sideways scroll with no cue that one exists. The reader sees a sum of terms followed by
     \(-\kappa_1P_1a_x\), which looks like one more term, not a right-hand side.
   - Table 5 is also cut on the right, both the 3D column and the caption. (N2) overflows by 18 px.
   - Measurements are in the table above.
4. **One symbol, several meanings, and silent switches from section 4.**
   - \(\zeta\) is the surface in (N1) and the damping ratio three paragraphs later ("damping \(2\zeta\sigma\dot\beta\),
     \(\zeta_1 = 0.0053\)").
   - \(R\) is the radius, and \(R_0, R_1, R_2\) are radial functions.
   - \(J\) is the Jacobian, and \(J_M\) are Bessel functions.
   - \(T\) is the kinetic energy, and \(T_k\) the angular factors.
   - \(\boldsymbol\beta\) is the coordinate vector, \(\beta_n\) the forcing coefficients of (54), and \(\beta\) the "coupling"
     fitted to the 3D solver.
   - [17]'s \(m_1\) (the frequency-shift coefficient) clashes with section 4's sloshing mass \(m_1\), eq. (19).
   - \(k\) is both a wavenumber and a mode index ("\(k_k\)").
   - Switched without a word, all from section 4 and §11.8: the surface \(\eta\) becomes \(\zeta\); the origin of \(z\) moves
     from the floor to the mean surface (compare \(Z = \cosh kz\) with \(Z_k = \cosh k_k(z+h)/\cosh k_kh\)); \(\omega_{11}\)
     becomes \(\sigma_1\); \(q_1\) becomes \(p_1\).
5. **The ordering is asserted, not explained, and never given the page's numbers.**
   - "If the forcing is of order \(\epsilon\), the swing is of order \(\epsilon^{1/3}\)" needs its reason. At resonance it is
     the cubic term, not damping, that balances the forcing, so \(p_1^3 \sim \epsilon\).
   - The reader is never told how large \(\epsilon\) or \(p_1\) are on this page.
   - At the breaking amplitude the "small" swing is \(21.2/39.1 = 0.54\,R\). At the largest push of Table 5 the peak wall
     amplitude is about \(61.3/2/39.1 = 0.78\,R\).
   - One sentence stating these values belongs in "The model, stated".
6. **The physical picture of both promised effects is missing, and "slows as it grows" is stated too widely.**
   - Softening: the text says only that the products "shift the swing's frequency with its size". The reader can see in (N4)
     that \(d_1p_1^2\ddot p_1\) acts as a mass that grows with the amplitude; the note never says so.
   - Swirl: the planar swing becomes unstable, a seed grows, and the motion settles into a rotating wave. All the reader is
     told is "Swirl comes from the \(d_2\) terms."
   - The opening says every glass "slows as it grows". Softening holds only above a critical depth; shallow tanks harden. The
     glass at \(h/R = 3.2\) is deep, and saying so is one clause.
   - The theory's frequency–amplitude relation (\(m_1\) of [17], eq. 3.13a) is named but given no value for this glass. The
     4.7 % softening in Table 5 therefore has no analytic number beside it, although that is the check the section most
     invites.
7. **The swirl result is left in open conflict with the source.**
   - The model swirls at 0.97 and 1.00 \(f_{11}\) and stays planar at 1.03 and 1.06. The text says [17] places stable swirl
     "just above \(f_{11}\)", then that "whether its frequency ranges match [17]'s was not established here."
   - A reader cannot tell whether the model's swirl is right.
   - The forcing is never put in [17]'s dimensionless form. The table's 0.3 m/s² at 3.42 Hz is a displacement amplitude of
     \(a/\omega^2 = 0.65\) mm, \(0.017\,R\). Without that number the comparison cannot even be attempted.
   - "At its own frequency" contradicts the four-frequency scan in the same sentence.
8. **Small skipped steps that stop the reader.**
   - "\(p_0\) and \((p_2, r_2)\) are what their product makes" needs \(\cos^2\theta = \tfrac12(1 + \cos2\theta)\) and
     \(\sin\theta\cos\theta = \tfrac12\sin2\theta\). That is why only \(M = 0\) and \(M = 2\) appear.
   - "\(k_0 = 3.8317\), the first zero of \(J_0'\)" skips the zero at the origin; the reason is that the uniform rise is
     excluded by volume conservation.
   - "The remaining cubic terms of (N4) have exactly the combinations \(d_1 - 2d_2\), \(d_1 - d_2\) and \(2d_2\)": these
     combinations cannot be found in (N4) as displayed. They are the coefficients of \(p_1\dot r_1^2\), \(p_1r_1\ddot r_1\)
     and \(r_1\dot p_1\dot r_1\) once (N4) is multiplied out, and the text should say so.
9. **An inference without support in the paragraph after Table 5.**
   - The sentence is: "Fitted as one oscillator its coupling \(\beta\) grows with the amplitude, from 0.48 to 1.26, so the
     grid damps small swings more than large ones. That is the grid's, not the stout's."
   - A forcing coefficient that grows is not a damping rate, so the "so" does not follow.
   - No grid-refinement run is cited to show the effect is the grid's.
   - The 3D frequency at the smallest push (3.160 Hz) is below the one at 1 m/s² (3.202 Hz). That breaks the softening trend
     the paragraph relies on, and the paragraph does not mention it.
10. **The seam with §11.8, and loose claims.**
    - §11.8 opens "The figure therefore runs, by default, a reduced model" under the title "The live model", then ends
      "since 7 November 2026 that is the figure's live model" for §11.9's model. That is a changelog entry in a textbook,
      dated after today (6 November 2026).
    - "Fully nonlinear modal equations" overstates a five-mode truncation.
    - "Steps by the symplectic Euler rule": with a configuration-dependent mass matrix \(M(\boldsymbol\beta)\), stepping
      velocities rather than canonical momenta is not symplectic. Either drop the word or step \(M\dot{\boldsymbol\beta}\).
    - Luke's principle, Miles, Narimanov, Moiseev and Lukovsky are cited by name but have no entry in Sources (16).

Screenshots and scripts (not part of the repository):
`/tmp/claude-0/-home-user-SiteTest/91e62847-1a1a-5a7d-b603-4662585b11e7/scratchpad/s119/` (`s119-1280-*.png`,
`s119-390-*.png`, `n4crop.png`).
