# Fig. 15 · referee report on the corrected note (resonant tunnelling)

Read as rendered at commit `960a5df` (branch `claude/fig15-note-corrected`). `npm run build` exit 0; `dist/` served on
port 9963; opened in headless Chromium (Playwright 1.63) at 1400 px; "Expand all" pressed; each of the 14 `section.psec`
screenshotted; the text extracted with every KaTeX formula replaced by its TeX source. 0 KaTeX errors, 0 console errors.
Two readers: a school student good at mathematics, and a physics graduate. Numbers were checked by hand against the
note's own inputs; no computation was launched. plan.md and check.md were not read.

Marks are given as location · quote · problem. Errors come first, then places where a reader gets lost, then small points.

## A. Errors (a sentence that is false for the numbers shown, or a rendering fault)

1. **§10 "The step", and §11 below the audit table.** "section 11 shows that a step four times smaller changes the first
   batch's results by nothing to three digits" and "A smaller time step and a box twice as long change nothing to three
   digits". The §11 table's third row reads 0.187 on the first grid and **0.185** at Δt = 0.0025, so the third digit
   changes. Either say "by at most 0.002" or give the row to the precision at which it holds.

2. **§10, equation (25e).** It renders as "max(0.005,**;** 0.01 T_ref)", with a stray semicolon. In
   `public/scripts/resonant-note.js` line 269 the JS string has `\;`, which JavaScript turns into a bare `;`. It needs `\\;`.

3. **§12, Key result box.** "the difference itself stays near 0.02 from radius 12 to 6". From the table: 0.205 − 0.159 =
   0.046; 0.254 − 0.205 = 0.049; 0.448 − 0.405 = 0.043 (walls: 0.197 − 0.153 = 0.044). The difference stays near
   **0.045**, not 0.02.

4. **§12 "Shells", single-shell comparison.** "58.1 (radius 3 …) and ≥ 166 (radius 5 …): as long as the pairs below at
   radius 3, and longer than them at radius 5. So the long life comes from the closed shell itself, and a second shell
   around it does not lengthen it". The table gives 59 for (R = 3, s = 2.5), but **≥ 104** for (R = 3, s = 3.5). That is
   nearly twice the single shell's 58.1, so for s = 3.5 the second shell does lengthen the life. Two paragraphs later the
   note says the same thing: "The wider spacing, s = 3.5, holds the wave longer, as section 7 leads us to expect". The
   two statements contradict each other. "At radius 5 it lets the wave out sooner" is only supported for s = 2.5
   (100 < 166). For s = 3.5 it compares two lower bounds (≥ 119 against ≥ 166), and that settles nothing.

5. **§6 "Long packets", table and the sentence before it.** "For walls every run is the exact solution of section 10, so
   its share through must equal the exact average (18) for its packet … their agreement checks both". The table then shows
   differences of up to 1.1 × 10⁻³ (running example), 1.4 × 10⁻³ (V₀ = 3) and 5.7 × 10⁻⁴ (0.0346 against 0.0351,
   d = 2). That is several hundred times the accuracy §10 claims for (25a/25b): 3.0 × 10⁻⁶ from the k-step, at most
   2.1 × 10⁻⁵ of start-tail, c₋ "nearly zero". The short packets agree (§9: 0.174 against 0.174, 0.0351 against 0.0351). A
   reader told the two "must be equal" and shown a gap 400 times the stated error is left with no explanation. Either
   name the cause of the 10⁻³ gap, or drop "must equal" and "checks both". Two smaller faults in the same place: the
   "exact average" column gives 0.54 to two digits beside 0.539. And "every run is the exact solution" is not true for
   the pictures of the 170 kept wall runs (§10: "A kept run's picture and curves are still the first batch's"). Only
   their *share* is exact.

6. **§8 against §11, direction of the packet-spread bias on a fitted lifetime.** §8: "the parts of the packet off
   resonance are still draining faster, and a fit that sees only that stretch reads short". §11: "the rule itself reads
   about 1 % long, because the packet is not a single energy". The same cause is given for opposite signs and never
   reconciled. One sentence saying which effect wins when (a short window early in the decay against a full 60 %→5 %
   window) would settle it.

7. **§12 table caption.** "A lifetime marked * comes from a kept first-batch run". No entry in the table carries a *. Either
   a kept disc run in the table is unmarked (745 discs were kept, so this is possible at E = 0.75), or the sentence
   should go.

8. **§11 and §14 "for discs and shells right to about 0.0019".** The 0.0019 comes from §10's convergence tests "on the
   discs tested". For shells §10 reports only a 32-bit against 64-bit comparison on "the one shell checked" (0.0012). No
   shell convergence test is reported, so the bound is not supported for shells.

## B. Where a reader gets lost (skipped steps, symbols before definition, unsupported claims, missing picture)

### Sections 10 and 11 (new)

9. **§10, (25a).** "The factor k/k_R is there because a state that arrives from the right carries its flux at the speed
   k_R, not k, so it is counted with the weight k/k_R". For the graduate this is not the reason. The weight is the
   Jacobian dk_R/dk = k/k_R that turns the right-incoming states' natural measure dk_R/2π into dk/2π, because
   k_R² = k² + 2eV_b. The flux story does not produce k/k_R by itself. The student is given a rule he cannot check. The
   graduate will also ask about the right-incoming states with k_R < √(2eV_b), which are totally reflected under bias and
   have no real k. They are missing from (25a). Say they are negligible for a packet that starts on the left, and why.

10. **§10, (25a) line.** "k_R = √(k² + 2eV_b)". This is the first appearance of e and V_b. They are defined only in §13
    ("Here −e is the electron's charge and V_b the voltage"). The bracket "(section 13)" points forward, but a reader
    still meets two undefined symbols.

11. **§10 "The step".** "the fastest wave the grid can hold … turns its phase by k²Δt/2 = 0.2 rad per step …, by 0.6 rad;
    the waves the runs actually carry … turn by less than about 0.05 rad per step." The paragraph has just said that the
    kinetic step "is exact on its own". The reader is not told why phase-per-step matters: does it control the splitting
    error, aliasing, or nothing? Without that sentence the three numbers have no point.

12. **§10 "The correction: discs and shells".** The numerical method is not given with the page's values as STANDARD
    item 5 asks. The (x, ρ) runs have no stated time step, no radial point spacing or count, and no rule for averaging
    cells in ρ. Only the x-cell (0.0625 a) and the radial ranges are given. "on the discs tested" does not say how many
    discs, or which.

13. **§10 (25d) for shells.** "P_R the probability still in the box beyond the last face, P_M the probability between the
    first and last face at any ρ". For two concentric spherical shells, "the last face" is not defined. Is it a plane
    x = R + s + d/2, or the outer sphere? So the reader cannot tell what T_ref means for a shell. See also mark 21.

14. **§10 "The check, and what was kept".** "The walls under a voltage were computed by the same exact method; no second,
    independent calculation has checked them." Any first-batch biased-wall run that passed (25e) was checked by an
    independent (grid) calculation. Say how many biased-wall runs were kept, or say "no calculation as accurate".

15. **§1 "Reading the figures" against §10.** Fig. 15b's "same problem solved in one dimension on the same grid is dashed
    in black", the "grey bands at the ends … where the computation absorbs waves", and "divided by the total still in the
    box" all describe the first grid. §10 says that 918 wall runs have no grid, no box and no absorbing border. The
    reader is not told what the dashed twin, the grey bands and the dotted "whole box" curve of Fig. 15c show for a
    rebuilt wall run, or for an (x, ρ) run.

16. **§11 "What moved the resonances", physical picture missing.** "the Fourier step (25) reads that staircase as a
    barrier of a slightly different shape". §10 has just said that the faces lie halfway between grid points, so the
    two-point staircase is exactly 1 a thick. The reader expects no error, and is given no reason why the error lowers
    the resonance (a wider well) rather than raising it. The 0.071 a is worked backwards from the measured shift, not
    explained. One sentence of mechanism is needed: what band-limited (Fourier) interpolation does to a two-point step,
    and which way it moves the effective inner faces.

17. **§11, audit table and the paragraph after it.** "with the barrier still drawn by points it does not approach the
    exact value, because the barrier's edges jump from point to point". At Δx = 0.25 "by points" gives 0.23, while cell
    averages at the same Δx give 0.0368. A reader cannot see why two drawings at one spacing differ by a factor of 6
    unless told how many points (what width) the point-drawn barrier covers at Δx = 0.25 and 0.125. Give the drawn widths.

18. **§11 "The 3D run is its 1D twin" against "Lifetimes".** The profiles agree to 1.8 × 10⁻⁴ of the peak, but the
    lifetimes differ: "15.1 in 3D and 15.3 in its twin". The next sentence (the side border) is the reason, but it is not
    tied to this gap. Say "the 0.2 is the side border's share" or similar.

19. **§11 "Lifetimes".** "The staircase moves and narrows the resonance, which lengthens the lifetime". The step "lowered
    resonance → narrower" is the §7 argument (slower electron, larger κ). Cite it. Also, 15.1 and 15.3 are compared with
    ħ/Γ = 14.2, not with the rule's own reading on exact runs, 14.4. Against 14.4 the staircase effect is 5–6 %, not
    6–8 %.

20. **§11 resonance position.** "the V₀ = 3 resonance lies at 0.878 exactly", while §8's table and §6's long-packet row use
    0.877 / 0.8773. If 0.878 is the peak of the packet-averaged sweep rather than E_r, say so. Then "lowers the resonance
    by 5.8 %": with the printed numbers (0.878 → 0.828) it is 5.7 %. With 0.877 it is 5.6 %.

### Section 12

21. **§12 Shells, physical picture.** "much of it is reflected, or tunnels straight through … four crossings in all". At
    E = 0.30 one barrier passes about 5 %, so four crossings pass about 10⁻⁵. Yet the shell table gives
    T_ref = 0.47–0.68. The reader needs to be told where that share comes from: the part of the packet outside the outer
    shell (about a quarter for σ⊥ ≈ 3.6 and outer radius 6), and waves bent round the ball, since the wavelength 8.1 is
    comparable to the ball. As written, the paragraph suggests that little gets through.

22. **§12 Shells, "≥" against run length.** §10: shell runs last the flight plus three times a lifetime capped at 30. The
    ≥ rule is "the fit window reaches the end of the run before the trapped wave has drained for even one lifetime". The
    run length of the shell runs is not given. So the reader cannot see why 100 (R = 5, s = 2.5) counts as a measurement
    while 104 and 119 are lower bounds, and a window of 100 or more looks hard to reach under a 90-unit tail. State the
    shell runs' lengths, or mark 100 as ≥ as well.

23. **§12, (28) and the table.** "agree with it to within a factor of about 3". The ratios are 2.3, 2.7, 1.3, 0.41 and
    0.54. That is fair, but (28) uses the starting σ⊥ = 3 for a trapped wave whose width by (3) keeps growing (about 5.8
    at t ≈ 30). The R² → R crossover therefore sits at a larger R than the table's "R min(R, 3)" puts it. One clause
    would do.

### Sections 6–9, 13 (true for the numbers, but the reader trips)

24. **§6 "Long packets".** "The long packet … passes 0.539 at the resonance, against 0.196 for the short packet: far more,
    as (19) says." (19) needs σ_E ≫ Γ. Here σ_E/Γ = 0.7, and (19) would give about 0.87. (19) gives only the trend here,
    not the number.

25. **§6 Key result.** "One barrier alone passes 0.149 of the same packet". §12's table gives 0.153 for one wall. They
    differ because one is at E_r = 0.735 and the other at E = 0.75, but neither says so.

26. **§7 last paragraph, §8 last paragraph, §9 last paragraph.** "one of the kept runs (section 10) … its file and
    curves are the first batch's", "a kept first-batch run", "the first grid's side border", "the staircase error of
    section 11". These are forward references to terms defined three or four sections later. A student reading in order
    meets "kept", "first batch", "first grid" and "staircase" without a definition. A half-sentence gloss on first use
    (in §6 or §7) would fix it.

27. **§9 Key result.** "the pair's resonance 0.735 sits where ξ = 0 …, the middle of the band's range of ξ (in energy the
    band's midpoint is 0.773)". True and checked, but the student needs one clause saying why the energy midpoint is not
    the ξ-midpoint (ξ is not linear in E).

28. **§13 "The current".** "As the voltage grows the net flow at each energy grows, and once eV_b is several k_BT it levels
    off … As the voltage rises the level sweeps down through them". "them" has no antecedent in the previous sentence
    (it means the filled states two sentences back). And "levels off at its largest value" is misleading at a fixed
    energy: the largest value, (E_F − E)/k_BT, itself grows as the level sinks, which the later paragraph uses ("14.2 …
    to 18").

29. **§13 "The current from the runs".** "Two things make it differ from the exact curve, and the page says both." The
    first follows (packet smoothing). The second sentence ("Each T̄_i is the run's T_ref …") is not a difference for
    walls. The real second cause, sampling at 0.05 against a peak 0.07 wide, comes three sentences later in a different
    argument. Put the two causes side by side.

30. **§13.** "A packet's energies spread over about 0.202". This is σ_E at E = 0.735. At the energies that carry the diode
    current near its peak (the level at 0.29) σ_E = k₀/(2σ_x) ≈ 0.13. The argument that the sum "cannot miss the peak"
    still holds (0.13 > 0.05), but the number quoted is not the one in play.

### Symbols with two meanings (STANDARD and the 21 October verdict: one symbol, one meaning)

31. ρ is the reflection phase in §5 (12) and the distance from the axis in §10 (25c, 25d) and §11. φ is the transmission
    phase in §9 (22) and the azimuth in §10. φ(k) (varphi) is the packet spectrum in §6. R is the reflection coefficient
    and also a disc or shell radius in §12 (flagged there). P_R uses R as "right" in the same section that uses R as a
    radius. t is an amplitude and a time (flagged). T is a transmission and a temperature (flagged). The flags help, but
    ρ and φ are not flagged at all.

## C. Small points

32. §11: "off by a median of 0.014 for walls and 0.013 for discs, and by up to 0.44 and 0.44" reads like a typo. Write
    "and by up to 0.44 for each".
33. §11 table header: "first grid (" breaks with the bracket alone at the line end.
34. Equation numbers (25), (25a)…(25f), (26). The section 11 equation is (25f), which reads as a patch. Renumber in
    order if the page allows.
35. §11 "(files in the repository, notes/fig15/audit/)" and the closing note's `gen1_profile_check.py` and
    `2026-11-13/kaggle/index.json` are not links, while derive.py and gen2_numbers.py are. The GitHub links point to
    `main`, where these files may not exist until merge.
36. §10 "fades over many steps": with the sin^(1/8) profile the factor is already 0.958 per step at the border's middle,
    so the wave is gone within a few hundred steps there. "Many" is fair, but a number would help the student.
37. §10 (26): "two frames of a wave that turns by about E Δt_f between them". Give Δt_f (run length / 200, so 0.15 to
    2.7) so the reader sees that the turn is up to about 2 rad.

## Verdict per section against notes/STANDARD.md

| § | Verdict | Reason |
|---|---|---|
| 1 Two panes of glass | clear, leave it | Picture first, controls explained. Only mark 15 (what the grid elements mean for rebuilt runs). |
| 2 The model in 3D | clear, leave it | Separation shown step by step; σ⊥(40) = 7.3 and k, κ, e^(−κd) check. |
| 3 One barrier | clear, leave it | Every number (6.95, 0.144, 0.925, 6.4 × 10⁻³, 22.5, 0.154) checks; limits given. |
| 4 Two barriers | clear, leave it | Table of partial sums checks to the last digit ((1 − R^(ν+1))²). |
| 5 Sharp peak, trapped wave | clear, leave it | ρ = −3.03, n = 0, Γ = 0.0699, 0.3108/0.3111, τ = 14.2, 0.0633 all check. |
| 6 Packets | needs work | Marks 5, 24, 25: "must equal … checks both" against a 10⁻³ gap; (19) misapplied to the long packet. |
| 7 Wider well | needs work (small) | All table numbers check; mark 26 (undefined "kept / first batch / first grid"). |
| 8 Taller, thicker | needs work (small) | Every row of the table checks against (8) and (17); mark 6 (sign of the packet-spread bias) and mark 26. |
| 9 Bands | clear, small fix | Algebra and peaks consistent (N = 5 and N = 10 share their ξ = ±0.809, ±0.309 peaks); marks 26, 27. |
| 10 What was computed | needs work | Marks 1, 2, 9–15: false "nothing to three digits", (25e) typo, k/k_R reason, e and V_b before definition, (x, ρ) method values missing, shell T_ref undefined. All run counts check (3739, 3697, 1088, 2327, 282, 170 + 918, 745 + 1582). |
| 11 First grid | needs work | Marks 1, 6, 16–20: Δt claim false for row 3, no mechanism for the sign of the staircase shift, 0.878 against 0.877, lifetime bias sign. |
| 12 Discs and shells | needs work | Marks 3, 4, 7, 21–23: "difference near 0.02" is 0.045; the shell conclusion contradicts its own table; dangling *; T_ref of shells unexplained. τ_side column and ratios 1.29 / 1.11 / 1 check. |
| 13 The device | clear, small fixes | a = 2.75 nm, 110 meV, 10.6 meV, 62 fs, 87 K, 131 / 274 mV, supply 14.2 / 18, products 1.03 / 0.73, Fig. 3 to scale all check; marks 10, 28–30. |
| 14 Limits, reading | clear, small fix | 313 = 72 + 241 checks; mark 8 (0.0019 for shells unsupported); references have working DOI links. |
