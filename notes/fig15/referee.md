# Fig. 15 · referee report, round 4 (resonant tunnelling)

Read as rendered, at commit `6af5c32` (branch `claude/fig15-gen2-note`). `npm run build` (exit 0); `dist/` served on port 9910;
opened in headless Chrome at 1400 px and 390 px. All folds were opened, sticky headers were made static, and each of the 14 sections
was screenshotted. KaTeX: 0 `.katex-error`, 0 raw `\(` or `\[` left in the text, no console errors. The round-3 rendering faults
(literal `“` in §11, raw `\\(V_b=0.875\\)` in §13) are gone. At 390 px the wide displays switch to their broken-up narrow versions
and nothing overflows the page. The 3D panels are blank locally (the run files live on the remote store), as expected.
plan.md and check.md were not read.

Spot checks recomputed by hand: |r| = 0.925; (9) = 0.154; Example 3.1 (T = 6.4 × 10⁻³, a ratio of 22); −2 ln R = 0.3110 against
2T/√R = 0.3113, and the T³ order of their difference; Γ from (15) = 0.0699; 2L_eff/v = 4.55; (17) = 0.0633; τ/t_rt ≈ 3.2;
σ⊥(40) = 7.31; σ⊥(13) = 3.70; σ_E = 0.202; (19) = 0.218, and 0.0359 for d = 2 with the long packet; FWHM 0.119; the hard-box
column of the §7 table; (21) = 0.649; the V₀ = 1.5 row of the §8 table (T = 0.248, Γ₁₇ = 0.093); the ratios 22 and 24; the
phase step 0.59 rad; the run counts (they add up to 3739); the 8-bit rounding of 0.2 % and 0.012 rad; a = 2.75 nm; τ = 62 fs;
87 K; the supply-function state count and (30); the supply values 14 and 18; the products 1.04 and 0.74; τ_side = 2.28.
All agree with the note.

There are two readers. **S** is a school student who is good at mathematics. **G** is a physics graduate. Each mark gives the
section, the exact sentence, which reader gets lost, and why.

## Marks

### Whole page

1. **All sections, body text (S, G; design).** The note's paragraphs render in IBM Plex Sans (computed `font-family` of
   `#paper section p` and `.psec__lead`). Only the figure captions are in Latin Modern. On the Fig. 14 page (`schrodinger-sphere.html`)
   the same elements render in Latin Modern Roman. CLAUDE.md and STANDARD ("Latin Modern in notes") ask for the LaTeX look, so this
   note does not look like the lecture note next to it. The cause is in the page's styling, not in the note text.
2. **Further reading, §4 and §11: links (G).** "The one-dimensional formulas are checked in notes/fig15/derive.py. Every other number in
   this note is printed … by notes/fig15/gen2_numbers.py, which reads … public/data/resonant-tunnelling/2026-11-14/kaggle/index.json".
   The links point at `github.com/…/blob/main/…`, but `gen1_profile_check.py`, `gen2_numbers.py` and `index.json` are not on
   `origin/main` (checked after `git fetch`), so they return 404 until this branch is merged. `derive.py` is on main and works.
   STANDARD §4.8 asks for working links.
3. **§6, §7, §10, §12, §13: project status in the text (S, G).** Phrases such as "the best of the 5 long-packet runs filed so far",
   "they are due to be rerun", "1237 of them … are filed so far, after 5.9 hours on the clock", "to come" (eight cells of the §12 table),
   "the larger radii, still to come, will show the trend", "We quote them when all 500 are in" and "the runs at 0.75 … are still
   to come". These read as a lab log, not a textbook chapter. A reader cannot tell which claims are results and which are promises.
   Some claims also rest on the missing data (marks 39 and 41).
4. **§3, §4, §9, §13: run-in starred passages with no visible end (S).** "Why the matrix has this form★.", "The algebra★." and
   "The supply function★." begin in the middle of running text, and the reader who skips is not told where the starred passage ends.
   In §9, "The algebra★." starts in the middle of a paragraph and runs into "What (23) says.", which itself uses U_{N−1} and β from
   inside the star. The promise in §1, "their results are stated again in plain words just after", holds in §3 ("In plain words: …").
   It does not hold in §9, where the reader who skips meets the Chebyshev polynomials and Bloch waves anyway.

### §1 · Two panes of glass

5. **(S) "Reading the figures. The chips under The barriers choose the structure, … its shaded stretch marks where the current falls
   as the voltage rises."** This is one paragraph of about 330 words. It defines five panels, their colours, a ×4 rule, the absorbing
   border, the 1D twin, the thick and thin curves and the dashed disc curve before any of these ideas has been met (twin: §10;
   packet average: §6; border: §10). A first-time reader cannot hold all of it. It works as a legend the reader comes back to, but
   the note does not say so.
6. **(G) "This is a Fabry–Pérot interferometer, the heart of every laser cavity."** "Every" is too strong: ring lasers and
   distributed-feedback lasers have no two-mirror cavity. Also, the first sentences describe thin-film fringes from two unsilvered
   panes in reflection, which is a different set-up from the silvered Fabry–Pérot. The step from one to the other is quick.
7. **(S) Figure 1.** The label V₀ of the height arrow sits on the dashed energy line E and is crossed by it (screenshot of §1, at
   1400 px). In the drawing the arrow's two ends are not visibly tied to the barrier's base and top.

### §2 · The model in three dimensions

8. **(S) "Since they depend on different variables and add to zero, each can depend on t alone."** This is the key step of the
   separation, and it is stated without the reason. Hold t and y, z fixed and change x: only the first bracket could change, but the
   sum stays zero, so the first bracket does not depend on x. One sentence would fix it.
9. **(S) "$g\propto(1+it/2\sigma_\perp^2)^{-1/2}\exp[-y^2/4\sigma_\perp^2(1+it/2\sigma_\perp^2)]$"** In this inline form the reader
   cannot tell whether $(1+it/2\sigma_\perp^2)$ is in the denominator of the exponent. It is, but a student reading left to right
   puts it in the numerator.
10. **(S) "We use natural units, ħ = m = 1: lengths in a unit a …"** The note never says what a is for the 3D runs (§3 to §12).
    Only §13 fixes it, at 2.75 nm. A sentence saying that a is free and the results scale with it would close the gap.
11. **(G) STANDARD §4.2: the model's dimensionless numbers are scattered.** E/V₀ = 0.37 appears only in the Figure 1 caption,
    κd = 1.59 in the box, and σ_E/Γ ≈ 3 and R/σ⊥ only in §6 and §12. The regime of the model (when a barrier counts as thin or
    thick, when a packet is "long") is never stated in one place, with the page's values.
12. **(S) "Its narrow width holds a spread of sideways wave numbers 1/(2σ⊥)"** This is the first appearance of the uncertainty
    product of a Gaussian, given as a parenthesis ("the two standard deviations multiply to 1/2"). Fine for G. S gets no reason,
    no picture and no source.

### §3 · One barrier

13. **(S) "Adding and subtracting these two lines,"** To reach (5) the reader must first divide the second line by k₁. That step is
    silent, and it is what makes k₂/k₁ appear.
14. **(G) "Referring the outer amplitudes to the barrier's centre, x = 0, adds a phase: w = e^{ikd}[…], and in the same way
    γ = i … sinh κd (both checked against the numerical product)."** Neither the phase nor its source is shown. The text set up "each
    edge gets its own origin", so the reader needs to see which shifts of d/2 multiply which amplitude, and why γ gets no phase.
    "Checked against the numerical product" supports the result but is not a derivation. This is the silent step STANDARD §4.3 forbids.
15. **(S, inside ★) "The same matrix must link the conjugated pairs, which forces the second row to be the first row conjugated
    and swapped."** The two lines that show it (write the conjugate of (A,B) = M(C,D), and compare it with (B*,A*) = M(D*,C*)) are
    missing. The same holds for "which fixes |w|² − |γ|² = 1": the substitution that turns flux conservation into this identity is
    not shown, and neither is the vanishing of the cross terms in v(|A|² − |B|²).

### §4 · Two barriers, two ways

16. **(S) "whose top-left element is 1/t₂ (the same reasoning as 1 = w t for one barrier)"** This reasoning has not been given
    yet. It comes later in §3 (the paragraph after (7)), and t₂ is named here before it is defined in words, as the transmitted
    amplitude of the pair. The order works, but only just.
17. **(G) "This agrees with the matrix product to one part in 10⁹ (notes/fig15/derive.py)."** The matrix product itself is never
    written out, so the reader cannot repeat the check. A file path is not a derivation.

### §5 · The sharp peak and the trapped wave

18. **(S) "Then (13) becomes [(15)] … Γ = 2T/(√R θ′)."** The substitution is skipped: put sin²(θ/2) ≈ ¼θ′²(E − E_r)² into (13),
    get 1/[1 + Rθ′²(E − E_r)²/T²], and read off (Γ/2)² = T²/(Rθ′²). These are two lines, and they are the heart of the section.
19. **(S) "here r is close to −1, as for a hard wall, and this first resonance is the one at which about half a wavelength fits in
    the effective width of the well (the spacing of the barriers' inner faces plus the depth the wave reaches into each, 2.76 here …)"**
    The effective width is used here before it is defined, a paragraph later (L_eff = s − d + 2/κ). Also, "the depth the wave reaches
    into each" is 1/κ, but the sum 1.5 + 2(0.629) only works if that is said.
20. **(G) "For a thick barrier r is close to that of a single step up to V₀ …"** The running example has κd = 1.59 and e^{−κd} = 0.20,
    which is not thick. The 4.45 against 4.55 that follows shows the approximation is fair, but the text should say it is being
    stretched.
21. **(S) "And it adds the time the wave spends inside the barriers."** The referent of "it" (the phase 2ρ) is two sentences back.
    The "time inside the barrier" and the later "as if the step stood 1/κ further in" are the same thing said twice, and nothing
    says so.
22. **(S) "This is the law of every slow leak: a fixed fraction lost per unit time."** It comes right after τ = ħ/Γ (16), but it
    describes the exponential decay of the previous paragraph, not the reciprocity of (16). The antecedent is misplaced.
23. **(S) "after a time t (now a time again)"** In §3 and §4, t is the transmitted amplitude, in §2 it is time, and from §13 T is
    also a temperature. The note flags each switch, but in this section both meanings are live in the same paragraph (t_rt, t/t_rt,
    T). A separate symbol for the amplitude (for example τ_a, or t̃) would remove the clash.
24. **(S, ★) "A very wide gap★. … put u = tan(θ/2): the average becomes (1/π)∫du/[1 + (1+F)u²]"** The change of variables
    dθ = 2du/(1 + u²) and sin² = u²/(1 + u²) is skipped. It is starred, but G also has to do it on paper.

### §6 · A wave packet is not a single energy

25. **(S) "When σ_E ≫ Γ the packet's energy distribution is nearly flat across the peak, with height 1/(√(2π) σ_E)"** This value
    holds only if the packet is centred on the resonance (the "peak" in $\bar T_{\text{peak}}$), and nothing says so. The step from
    a Gaussian in k to one in E (Jacobian, small spread) is also only implied by "σ_E ≈ k₀σ_k".
26. **(S) "The figure's short packet has σ_x = 3, so σ_E = 0.202, about three times Γ = 0.0704."** This compares a standard
    deviation with a full width at half maximum. The note makes this distinction only in the next box ("though its full width at half
    maximum, 0.119, is still wider …"). The first comparison should already be like for like, or say that it is not.
27. **(G) "(these runs, made under an earlier rule for the run length, stopped more than 15 % before the present rule would end them,
    with a little of the wave still trapped; that changes the share by a few per cent, and they are due to be rerun)"** The direction of
    the change is not given. With the half-trapped rule of §11, stopping early can raise or lower the reported share. As it stands,
    0.51 against 0.499 cannot be read as agreement or as error.
28. **(S, G) The "Long packets" paragraph (about 330 words).** It mixes the physics result (a long packet passes 0.54 instead of 0.196)
    with run bookkeeping, a second structure (d = 2), a grid caveat and the spectroscopy remark. The physical point, a narrow
    resonance needs a narrow energy spread, is lost in the middle.

### §7 · A wider well sings lower

29. **(G) "With barriers of finite thickness these bound levels become the resonances, at almost the same energies: the barriers are
    thick enough that the wave in the well hardly feels where they end."** With e^{−κd} = 0.2 the wave does feel the far side (that is
    the tunnelling). The table supports "almost the same energies" (0.744 against 0.735), but the reason given is not the right one.
    The level is set by the near face, and the far face only lets it leak.
30. **(G) "Walls are an exact check, so this gap is an error of the grid, not of the theory; we have not traced why it is larger
    here."** The 12 % (against 6–8 % in §11) is left open. It also rests on a single run at E = 0.35, one of the 47-energy grid points
    rather than the resonance at 0.388, and the note does not say whether the off-resonance draining noted in §8 biases this fit.

### §8 · Taller and thicker barriers

31. **(S) "Since T ∝ e^{−2κd}, the width falls exponentially with κd"** The prefactor 16E(V₀ − E)/V₀² and the factor v/L_eff in
    (17) also change with V₀. "Exponentially" is right for d at fixed V₀. The text should say that for the V₀ rows the exponential
    dominates, but not alone.
32. **(G) "a straight line through the logarithm of its decay from t = 91 to the end gives 210, a lower bound rather than a measurement
    of τ"** The fit window (60 % to 5 % of the peak) is defined only in §11, three sections later. Here the reader does not know why
    the fit starts at t = 91.

### §9 · Three, five and ten barriers

33. **(S) "Everything about a row of identical barriers turns out to depend on one number, ξ, built from … by (22) below"** The
    number is introduced before its formula and before the reason it matters. For S, the pendulum picture of the previous paragraph
    is not tied to ξ anywhere: which pendulum quantity is ξ like?
34. **(G) "The off-diagonal element of P^N is U_{N−1} times that of P, whose square is |γ|² = |w|² − 1 = R/T."** It should say
    "squared modulus". Also, the transfer matrix of N barriers is M D M D … M, not (MD)^N. The parenthesis covers this, but only
    after the formula is used.
35. **(G) "there are exactly N − 1 energies where T_N = 1."** This should say "in each band". The statement also assumes ξ sweeps
    once from −1 to 1 across the band, which is true here but not argued.
36. **(G) "Outside it, |ξ| = cosh μ > 1, and U_{N−1} = sinh Nμ / sinh μ"** For ξ < −1 this needs ξ = −cosh μ and a sign
    (−1)^{N−1}. That is harmless for T_N, but it is stated as an identity.
37. **(S) Figure 2.** The strips have no y ticks. The caption says that the solid line is 0 and the dotted line 1, but the eye
    reads the solid line as an axis, so a reader cannot read a peak height off the picture.

### §10 · What was computed, and how

38. **(G) "Each half of the split is exact for every Fourier mode, however fast it turns (the fastest the grid holds, along a
    diagonal, turns by 0.59 rad per step); … we have not measured the time-step error on its own."** The 0.59 rad is given without
    saying why it matters (aliasing of the phase, or the commutator error of the fastest modes at the barrier edges). STANDARD §4.5
    asks for "the error the reader should expect, measured by running the page". The time-step error is admitted to be unmeasured,
    so §4.5 is only half met.

### §11 · How good the grid is

39. **(G) "A likely cause, which we have not separated further: … a Fourier method reads a sharp edge sampled every 0.5 a as a
    slightly softened one, a barrier of a slightly different shape"** In a split-step method the potential is applied point by point
    and is not softened. What changes is which k-modes can represent the evanescent decay. A softened edge would usually raise
    transmission, but the observed shift is to a narrower peak with a longer life, so the direction is not explained. This is an
    unsupported claim. Either run at 0.25 a once or say plainly that the cause is unknown.
40. **(S) "measured against each frame's own, shrinking peak the difference is up to 5.8 % during the collision and grows large late
    in the run, when little is left."** "Grows large" is not a number. Elsewhere the note measures everything.

### §12 · Discs and shells

41. **(G) "τ_side ∼ R/(ħ/(mR)) = mR²/ħ" (28).** This takes the trapped wave to fill the disc. But the packet is only about 3.7 wide
    at the barriers, so for R = 6, 9 and 12 the trapped wave's width is set by the packet, not by R. Its sideways speed is then about
    ħ/(mσ⊥), and τ_side ∼ mRσ⊥/ħ, which is linear in R, not quadratic. The "estimate (28), R²" column (36, 81, 144) and Problem 6
    ("how much longer … for discs of radius 6") depend on this choice, and the note does not discuss it.
42. **(S, G) Key result · finite barriers leak at the side: "and the larger radii, still to come, will show the trend. As R grows,
    (27) and (28) say the lifetime and the share through should approach the walls' values; the runs for the largest discs test it."**
    The "key result" rests on one radius (R = 2), and there the wave is "hardly trapped at all". The trend it states is a prediction,
    not a result. A key-result box should hold what was shown.
43. **(S) "the share that got through is 0.936" (discs of radius 2) and "when it reaches the barriers at t ≈ 13".** The packet's
    start x₀ is never given, so neither t ≈ 13 nor the claim of §2 "by t = 40 … has long passed the barriers" can be checked.
44. **(G) "In a real resonant-tunnelling diode the barriers are wide layers, so this leak does not matter; in a small quantum dot or a
    nanowire it does."** This claim has no support and no source.
45. **(S) Shells: "make a different trap: a hollow ball the wave can enter from any side, and in which it is caught inside the inner
    shell and in the gap between the shells."** No picture is given (none of Figures 1–3 shows the shells). The sentence "The packet,
    within about 3.7 of the axis, meets the shells head-on" needs the inner shell's size (inner radius 2.5 for R = 3) to make sense,
    and that is not given.

### §13 · The device

46. **(S) "On each side of the barriers the electrons fill the states one by one (…), up to an energy E_F, the Fermi energy: below it
    the states are full, above it empty. The tilt. A battery across the device …"** The run-in heading "The tilt." sits in the middle
    of a paragraph (screenshot of §13). The Fermi sea and the bias are two ideas, and they are merged into one block.
47. **(S) "In our units we quote the bias by the energy eV_b it gives an electron, in units of E_u, so eV_b and V_b are the same
    number."** In effect this sets e = 1 in a note whose units were ħ = m = 1. Then (32) writes "−V_b" where (31) wrote "−eV_b", in
    the same exponent. One symbol should be used throughout.
48. **(S) "Per unit area of the barriers there are 2 d²k⊥/(2π)² = (m*/πħ²) dE⊥ transverse states"** The step d²k⊥ = 2πk⊥dk⊥ =
    (2πm*/ħ²)dE⊥ is silent. The "d" of d²k is also the barrier thickness d, and the "x" of "x = E⊥/k_BT" is the flight coordinate.
    These reuses go unflagged in a note that flags t and T.
49. **(G) "With the exact single-energy T(E,V_b) the current peaks at V_b = 0.875 … a peak-to-valley ratio of 4.3."** No picture of
    J(V_b) is in the note. Fig. 15e is said to show it, but locally (and before all runs are in) the reader cannot check the exact
    curve's shape against the text.
50. **(S) "Roughly, the current is the area under the transmission peak times the supply at the level's energy."** This is a good
    physical picture. But the "area under the peak" of 0.103 at zero voltage is less than the Lorentzian πΓ/2 = 0.111 of §5, and
    nothing explains the difference (the tails, the energy cut-off at 0, or the exact shape).
51. **(G) "Resonant-tunnelling-diode oscillators have reached 1.92 THz at room temperature (Maekawa and co-workers, 2016), among the
    fastest electronic oscillators made."** The source is cited, which is good. "Among the fastest" is the note's own claim, and it
    is dated (2016) with no source.

### §14 · Limits and further reading

52. **(G) "Real electrons also pile up in the well and bend the very potential they move in; … it gives real diodes hysteresis"**
    This is a standard result, but no source is given. Further reading has none on space charge or bistability (for example Goldman,
    Tsui and Cunningham, PRL 58, 1256 (1987)), and none on the next model it names (self-consistent Schrödinger–Poisson, or NEGF).
53. **(S) Further reading lists only papers.** STANDARD §4.8 names textbook chapters and lecture notes. For a school student or a
    first-year reader, a chapter (for example Griffiths, *Introduction to Quantum Mechanics*, §2.6 on the finite square well and
    Problem 2.33 on the rectangular barrier, or Davies, *The Physics of Low-Dimensional Semiconductors*, ch. 5) is the natural next
    step, and none is given.
54. **(S) Problem 6, "Use (27) to find τ_side and compare with the estimate (28)."** The answer, 2.28, is already printed in the §12
    table, so the problem has no work left in it.

## Verdicts by section, against STANDARD §4

| § | Section | Verdict | Why (marks) |
|---|---|---|---|
| 1 | Two panes of glass | needs work (small) | The physical picture is strong (glass, echo); the figure legend overloads it (5); "every laser cavity" (6); Figure 1 label (7). |
| 2 | The model in 3D | needs work | The separation step is unexplained (8); the inline formula is ambiguous (9); the unit a is undefined for the runs (10); the regime and dimensionless numbers are not collected (11). |
| 3 | One barrier | needs work (small) | The physics is clear and the limits are checked; the phase of w and γ is not derived (14); small silent steps (13, 15). |
| 4 | Two barriers | clear, leave it | The path sum is excellent; only order and support nits (16, 17). |
| 5 | The sharp peak | needs work | The Lorentzian substitution is skipped (18); L_eff is used before it is defined (19); the thick-barrier approximation is stretched without saying so (20); a misplaced sentence (22); symbol clash (23). |
| 6 | Wave packet | needs work | The result is sound; σ_E is compared with Γ unlike to unlike (26); the long-packet paragraph is buried in bookkeeping (27, 28). |
| 7 | A wider well | needs work (small) | Good picture and table; the wrong reason for "almost the same energies" (29); the 12 % gap is left open (30). |
| 8 | Taller and thicker barriers | clear, leave it | Picture, table, key result and check all present; minor (31, 32). |
| 9 | Bands | needs work | The star boundary is unclear and the skipper is not served (4, 33); precision (34, 35, 36); Figure 2 axes (37). |
| 10 | What was computed | needs work (small) | Method described as the code does it; the time-step error is unmeasured (STANDARD §4.5) and 0.59 rad is unexplained (38); status text (3). |
| 11 | How good the grid is | needs work | The comparisons are good; the proposed cause is unsupported and possibly in the wrong direction (39); "grows large" (40). |
| 12 | Discs and shells | needs work | The table is mostly "to come" and the key result is a prediction (3, 42); the τ_side estimate is for the wrong width at large R (41); x₀ is missing (43); no picture of the shells (45). |
| 13 | The device | needs work (small) | Strong derivation and physical reading; layout of "The tilt." (46); e = 1 and V_b against eV_b (47); silent state-count step (48); the 0.103 area is unexplained (50). |
| 14 | Limits, reading | needs work (small) | Limits named well; no sources for space charge or the next model (52); no textbook chapters (53); links 404 until merge (2); Problem 6 is pre-answered (54). |

Page-wide: the body font is not Latin Modern (1), and run-status language runs through §6–§13 (3).
