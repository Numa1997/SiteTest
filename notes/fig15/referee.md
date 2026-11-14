# Fig. 15 · referee report, round 7 (resonant tunnelling)

Read as rendered, at commit `75bbc77` (branch `claude/fig15-gen2-note`). `npm run build` (exit 0 on the second try; the
first stopped in `rimraf` while clearing `dist/`); `dist/` served on port 9711; opened in headless Chromium (Playwright,
Google Chrome) at 1400 px and 390 px; every fold opened, sticky and fixed elements made static, each of the 14 sections
screenshotted at both widths, and the note's text extracted with each KaTeX formula replaced by its TeX source. KaTeX:
964 formulas, 0 errors. Text font in the note: Latin Modern; labels Plex Mono. All five references and the four script
links carry working-looking `href`s (DOIs and GitHub `main`; the GitHub ones may 404 until merge, as expected). The 3D
panel was not judged. `plan.md` and `check.md` were not read.

Two readers: S, a school student good at mathematics; G, a physics graduate. Each mark names the section, quotes the
sentence, and says who gets lost and why.

## Marks

### Header and section 1 · Two panes of glass

1. **§1, Reading the figures.** "Its height is the real part of the complex wave ψ or the probability density |ψ|² (section 2) (the chips under *Show*), on one scale for the whole run, so that the largest value the run reaches is height 1 (the height chips multiply it by 1, 3 or 10); …" — Contradicts the page: the note under the height chips says "One scale for the whole run: the start packet's peak is height 1." The data store calls the scale "the run's largest |ψ| on the stored plane". One wording must go. The sentence also stacks two parentheses in a row, and it does not say whether the |ψ|² view is scaled by the square of that peak.
2. **§1, Reading the figures (the whole paragraph).** About 400 words that act as a reference card, with nine forward references to sections 2, 5, 6, 10, 12 and 13 and terms not yet defined ("one-dimensional twin", "absorbing border", "fitted exponential decay"). S, reading in order, is lost by the third sentence. It would read better as a collapsible box, or split by panel.
3. **§1, Reading the figures.** "between them (wine, drawn four times taller, and labelled so, whenever its largest value over the whole run is below 0.25)" — It is unclear whose largest value is meant, the wine curve's or the box total's.
4. **§1.** "The electron is a wave; a thin barrier is a partly silvered mirror for it; …" — S is given the wave nature as a bare fact. One clause pointing to the double slit (Fig. 3 of this site) or to electron diffraction would ground it.
5. **§1, Figure 1 caption (rendering).** At 1400 px a line starts with a lone comma: "… E = 0.735 / , the energy at which this pair resonates." The same KaTeX line break appears in the Figure 2 caption: "|ξ| ≤ 1 / , from 0.59 to 0.955." A non-breaking join between the formula and the comma is needed.

### Section 2 · The model in three dimensions

6. **§2.** "Try a product, ψ=χ(x,t) g(y,t) g(z,t), … so we may choose each bracket to be zero." together with "Since the equation has only one solution for a given start, it stays a product for all time" — For G the logic runs the wrong way. The bracket argument assumes ψ is a product at every time and derives (2). What is needed is the converse: if χ solves the first equation of (2) and g the second, their product solves (1) (substitute it), it equals ψ₀ at t = 0, and uniqueness finishes the proof. The phase-removal step "Such a function f(t) can be removed … e^{+i∫f dt}" can then go.
7. **§2.** "Our packet starts as a Gaussian, ψ₀∝…, centred at x₀, 14 before the first barrier face (a packet starts 4σₓ before the face when that is more than 14; for the long packet of section 6, σₓ=12, that is 48), with length σₓ along the flight and width σ⊥ across it (…; both 3 for the figure's usual short packet; section 6 adds a long one), which is such a product." — The main point, "which is such a product", arrives some 70 words after its subject. S loses the thread. Split it into two or three sentences.
8. **§2.** "the second equation of (2) has the solution g∝(1+it/2σ⊥²)^{-1/2}exp[…] (substitute it to check)." — For S this is a formula from nowhere. "Substitute to check" is the "it can be shown" that STANDARD §4.3 forbids. At least name the route: the Fourier transform of the Gaussian, with each mode evolving by e^{−ik²t/2}.
9. **§2.** "they add up to a lump of finite length that moves at the group velocity v=dω/dk=ħk₀/m" — "group velocity" is defined only by a formula. S needs one sentence on why a sum of waves moves at dω/dk rather than ω/k (for example two close waves beating, with the beat moving at Δω/Δk).
10. **§2, box "Our running example".** "And the ratio of the short packet's spread of energies to the width of the resonance (both defined in sections 5 and 6), σ_E/Γ=2.9" — Two symbols are used three sections before they are defined. Acceptable as a forward reference, but STANDARD §4.2 asks for the model's dimensionless numbers. The one that sets *where* the resonance lies (well width over half-wavelength, L_eff/(λ/2) = 2.76/2.59) is missing here and appears only inside a parenthesis in §5.

### Section 3 · One barrier

11. **§3, ★ passage.** "and in the same way γ=i(κ²+k²)/(2kκ) sinh κd (both checked against the numerical product)." — For G this is a silent step. The off-diagonal product is not shown, and neither is the reason why moving the reference to the barrier's centre gives w a phase e^{ikd} but leaves γ without one (the two shifts cancel for the element that links A to D). One line each.
12. **§3, ★ passage.** "the probability current j=(ħ/m) Im(χ*χ′), which for Ae^{ikx}+Be^{−ikx} is v(|A|²−|B|²)" — The current is used, not derived. S has no idea where it comes from. One sentence would do: it is what makes ∂|ψ|²/∂t + ∂j/∂x = 0 hold, as the flow of water does.
13. **§3, ★ passage.** "(The letter γ is used because z is a coordinate.)" — Meaningless to the reader, who never saw z proposed for this element. Delete it, or say "rather than the usual z".
14. **§3.** "(Here t is an amplitude, not a time; which is meant is always clear from the context.)" — This breaks the house rule "one symbol, one meaning" (STANDARD, 21 October verdict, item 2), and §5 then needs "(now a time again)". The same holds for T as transmission and, in §13, temperature ("in k_BT only, T is the temperature"), and R as reflection and, in §12, radius ("in this section R is a radius"). Three overloaded letters in one note. Suggest τ-free names: 𝓉 or t_A for the amplitude, a for the disc radius (a is taken, so perhaps ρ_d or R_d), Θ or k_BΘ for temperature.
15. **§3, Example 3.1.** "Tunnelling is ferociously sensitive to width." — "Ferociously" is the dramatic voice the 21 October verdict rules out. "very sensitive" or a number (22 times for a factor 2) is enough.

### Section 4 · Two barriers, two ways

16. **§4.** "In the figure you see this pile-up: on resonance a tall, narrow lump of probability grows between the walls (Fig. 15b) before it drains away." — This is not supported for what the reader will actually see. No run is stored at 0.735 (Figure 1 caption), and §6 says the short packet "mostly reflects even on resonance". Give the trapped share the run at 0.70 or 0.75 reaches, so the reader knows how tall "tall" is.
17. **§4.** "This agrees with the matrix product to one part in 10⁹ (notes/fig15/derive.py)." — A repository path in running prose. It is linked, but S reads it as code noise. Put it in a footnote style or the closing source line, as §14 already does.

### Section 5 · The sharp peak and the trapped wave

18. **§5.** "The phase ρ is fixed only up to whole turns, so the value of n depends on how we count. Taking ρ between −π and π gives ρ=−3.03 and n=0 for this resonance; the box formula (21) of section 7 counts the same lowest state as n=1." — S has just been told that n counts resonances, and now the first one is n = 0 here and n = 1 two sections later. Either fix one counting for the whole note, or drop the n value and keep only "the first resonance".
19. **§5.** The sentence "Here r is close to −1, as for a hard wall, and this first resonance is the one at which about half a wavelength fits in the effective width of the well (the distance between the barriers' inner faces, 1.5, plus about 1/κ=0.63 into each barrier, 2.76 in all, against a half-wavelength of 2.59; the next paragraphs make this effective width precise)." — L_eff is first used here, inside a parenthesis, and only justified in the ★ part of the next paragraph. The physical picture (the wave leaks 1/κ into each wall) deserves its own plain sentence before the numbers.
20. **§5, "The width is the inverse of the time trapped."** The whole paragraph, about 400 words with a ★ passage opening and closing in its middle. S, who skips the ★, has to find "(End of ★.)" inside a paragraph. Split it at the ★ boundaries, as §3 and §9 do.
21. **§5.** "for small T the two numerators −2 ln R and 2T/√R agree up to terms of order T³" — A claim without its step. Two lines show it: −2 ln(1−T)=2T+T²+⅔T³+…, and 2T(1−T)^{−1/2}=2T+T²+¾T³+…. Otherwise S takes it on trust, and G cannot see at once that the order is right.
22. **§5.** "after a time t (now a time again) it has made t/t_rt round trips" — This is a consequence of mark 14.

### Section 6 · A wave packet is not a single energy

23. **§6, "Long packets."** "For the running example the best of the 5 long-packet runs computed so far (of 15 planned for this structure) passes 0.51 of the packet at E=0.713, where the exact average for this packet is 0.5. Just below the peak the grid passes a little more than the exact theory (section 11); and these runs stopped with 0.0286 still trapped, half of which would still have passed, because they were made under an earlier, shorter rule for the run length and are due to be rerun." — This is a project status report inside a textbook paragraph ("computed so far", "planned", "due to be rerun", "not yet filed"). It also leaves a puzzle: if 0.014 more would still have passed, the run would end at about 0.524, above the exact 0.5. The reader is told two corrections pull in opposite directions but not that their sum is the result. The physics this paragraph has to carry is one sentence: a σₓ = 12 packet passes about half of the resonance, against a fifth for σₓ = 3. Move the bookkeeping to a fold or to the box of §11.
24. **§6.** "The run stops 509 time units after it starts, about one lifetime after the trapped wave peaks, and ends with 0.00736 still between the walls; half of that would still leave forward, which accounts for about two fifths of the shortfall; and σ_E=0.051 is still much wider than Γ, and so narrow a peak is also very sensitive to the small shift the grid gives it (section 11)." — Three causes, chained with semicolons, in one sentence. S cannot tell which one matters. State the shortfall (0.0225 against 0.0319), then the causes one per sentence, each with its share.
25. **§6.** "T̄=∫|φ(k)|² T₂(k) dk" — T₂ was defined as a function of E in (13) and (15). Write T₂(E(k)) or say so once.

### Section 7 · A wider well sings lower

26. **§7, table (390 px).** The table is wider than the column (427 px against 325 px). It scrolls sideways, but nothing shows this: the Γ and τ columns are simply cut off on a phone. The same applies to the tables of §8 (458 against 325) and §12 (408 against 325). A fade or a "scroll →" cue is needed (a house-style question, not a note edit).
27. **§7.** "the levels are set mostly by the well and its two inner faces; the outer faces change them only through the small wave that reaches them, a share of about e^{−2κd}=0.04" — This explains why the shift is small but not its sign: the resonance, 0.735, is *below* the finite-well level, 0.744. One clause would tell G which way the open outer face pulls the level.

### Section 8 · Taller and thicker barriers

28. **§8.** "The resonance energy hardly moves when the barriers change, because the well does not change: 0.735, 0.742 and 0.744 for d=1, 1.5 and 2. A taller barrier raises it noticeably (0.877 at V₀=3), …" — The first sentence says "when the barriers change" and the next contradicts it. Say "when the barriers thicken".
29. **§8.** "… to the end gives 210, a lower bound rather than a measurement of τ: early in the decay the parts of the packet off resonance are still draining faster, and a fit that sees only that stretch reads short." — The reason given supports "reads short", not "a lower bound". A truncated fit is not a bound in the mathematical sense. Say "an underestimate".

### Section 9 · Three, five and ten barriers

30. **§9, Key result.** "the pair's resonance 0.735 sits where ξ=0, the middle of the band's range of ξ" — Stated, not shown. The one-line proof is already on the page: by (23) with N = 2, U₁ = 2ξ, so T₂ = 1 exactly when ξ = 0. Say it. (G may also want the link to §5: for a symmetric barrier r/t is purely imaginary, so ρ = φ ± π/2 and θ = 2πn is the same as cos(ks+φ) = 0.)
31. **§9, ★.** "half its trace is ξ≡½ tr P = Re(w e^{−iks}) = cos(ks+φ)/√T" — The two equalities are not shown. The trace is w e^{−iks} + w* e^{iks}, and w = 1/t = e^{−iφ}/√T. One line.
32. **§9, Figure 2.** The strips have no y ticks; the caption carries the scale ("each strip from 0 to 1"), which is acceptable. The caption line break: see mark 5.
33. **§9.** "These runs fall short of the exact values by more than the pair does; a possible cause, not tested, is that ten barriers repeat the small error of each barrier's shape on the grid (section 11) ten times." — The runs give 0.129 against 0.158 in the band (18 % low) and 0.0218 against 0.032 in the gap (32 % low). An untested guess in a textbook is weak support. Either test it (the 1D twin at Δx = 0.25 is cheap) or say plainly that the cause is not known.

### Section 10 · What was computed, and how

34. **§10.** "Each half of the split is exact for every Fourier mode; the error of the split comes only from the places where the potential changes" — The first clause is muddled: the V half has nothing to do with Fourier modes. G wants the real reason: the error term is the commutator [K,V], and [∇², V]ψ = (∇²V)ψ + 2∇V·∇ψ, which is zero wherever V is flat, so the error sits at the barrier faces.
35. **§10.** "we have not measured the time-step error on its own." — STANDARD §4.5 asks for "the error the reader should expect, measured by running the page". A 1D twin rerun at Δt = 0.005 settles it in seconds. The same holds for the grid, see mark 38.
36. **§10.** The grid's resolution is never compared with the physics it must resolve. With Δx = 0.5: 10 points per wavelength at resonance (λ = 5.18), but the decay length inside a barrier, 1/κ = 0.63, is only 1.3 grid spacings, and κd, which sets T exponentially, is carried by two points. That is the most likely cause of the 6–8 % lifetime error, and it belongs here, as the "where it fails" of STANDARD §4.5.
37. **§10.** "each step it multiplies the wave by a factor that falls smoothly from 1 to 0" — G cannot tell what the absorber does: the profile (cos², polynomial, …) and how much it reflects at the resonance energy are not given. Taken literally, a factor that reaches 0 *each step* is not a gentle absorber. Say what the factor is at the outer edge per unit time.
38. **§10, The runs.** "The runs are computed in six parts on two T4 GPUs each; 1237 of them, from the first 2 parts, are filed so far, after 5.9 hours on the clock." Also "about one nanosecond of GPU time per grid point per time step" — Project status and a performance figure with no source. Move the status into the data panel or the doc. The timing needs its measurement (which notebook, which run).

### Section 11 · How good the grid is

39. **§11.** "A grid twice as fine would cost eight times the points, and more steps; we kept Fig. 14's grid so the two figures can be compared directly." — This is the reason not to rerun in 3D, but for walls the 1D twin *is* the computation and costs nothing. Without one convergence point (the twin at Δx = 0.25 and 0.125), "a possible cause, which we have not tested" stays a guess. G expects this check on a page whose stated purpose is that "walls … check the computation".
40. **§11.** "For walls this reading gave 0.179 against the twin's 0.186, a 4 % gap, which comes from the half-trapped rule." — Unsupported. The reader is not told why splitting what is still trapped half-and-half loses 4 %, or how that was established.
41. **§11.** The paragraph that defines the fit window and the share-through rule ("The lifetime is fitted where …") comes after the box "What this means for the figure", but §5, §8 and §13 point to it as "the rule of section 11". Put the definitions first and the conclusions after.

### Section 12 · Discs and shells

42. **§12, table.** Four of six rows read "to come" in every measured column, and "one disc" is filled for radii 6 and 4 but not 2. Together with the Key result, "and the larger radii, still to come, will show the trend", and "the runs for the largest discs test it", the section's main claim, that the lifetime and share approach the walls' values as R grows, rests on data that is not there. Either state it as the prediction of (27) and (28) only, or wait for the runs.
43. **§12.** "The fitted lifetime belongs to the resonance the packet feeds … : walls give 15.1 at E=0.65 … The runs at E=0.65 measure it (walls of this structure are computed so far at 0.65, not yet at 0.70 or 0.75, which lie nearer the resonance)" — More status in the body (see mark 23).
44. **§12.** "the runs at radius 2 already show a lifetime far below that of walls, shorter even than one round trip, so there the wave is hardly trapped at all" — If the wave is "hardly trapped", the exponential fit that gives τ = 1.99 and τ_side = 2.28 from (27) is close to meaningless. Say so, or show that the decay is in fact exponential over the fit window.
45. **§12, Shells.** "We give no model of the shells here: a wave held in a spherical well has its own family of levels, a subject for another note." — For G one sentence would connect the shells to the rest of the note. For the spherically symmetric part (l = 0), u = rψ obeys the same 1D equation on r > 0 with two barriers, so the s-wave levels are those of §7 with a hard wall at r = 0. Without it the four lifetimes in the table have no theory at all (STANDARD §4.3).
46. **§12, Shells.** "The packet, within about 3.6 of the axis, meets the shells head-on: much of it is reflected or passes through both shells, and a part tunnels through the outer shell, …" — A packet going straight through crosses four shell walls, not two. "Passes through both shells" will make S picture two crossings.

### Section 13 · The device

47. **§13.** "The products, 1.04 at V_b=0.875 and 0.74 at 1.25 (in the units of (32)), show the turn." — This points forward to an equation the reader has not reached. Name the unit here (e m* k_BT E_u/(2π²ħ³)) or say "in arbitrary units".
48. **§13.** S_i in (32) contains "V_b" where (31) has "eV_b". The note says the two are the same number in these units, but the reader switching between the two equations sees the e vanish. Write eV_b in both.
49. **§13, The current from the runs.** "So far 170 of the 500 runs for two walls are filed, about a third of the energies at each voltage, and a different third at neighbouring voltages (the same third comes back every 0.75 in voltage). … We quote them when all 500 are in." — Status reporting again. The curve the reader sees in Fig. 15e is, by the note's own words, more about "which runs are filed than about the diode". A sentence in the figure's own note would serve better than a paragraph in the lecture.
50. **§13, Figure 3 (rendering).** The label "level" sits on top of the slate level line, and the subscripts in "V_b", "E_F − eV_b" are set in the SVG text font, not as the note's maths. Energies were checked against the caption (E_F = 1, V_b = 0.8, level at about 0.33, collector filled to 0.2): they are to scale as claimed.
51. **§13.** "(The mass in AlGaAs differs a little; we use one mass throughout. A more careful treatment matches χ′/m*, not χ′, at each edge.)" — G will accept this. S will not know why the slope condition changes. Half a sentence would do: the current j ∝ Im(χ*χ′)/m* must be continuous.

### Section 14 · Limits and further reading

52. **§14.** "The next, more complete model solves the Schrödinger and Poisson equations together and lets the electrons scatter as they cross." — Give it its name (self-consistent non-equilibrium Green's functions, or at least "Schrödinger–Poisson with scattering") and one source the reader can open. As written, G cannot follow it up.
53. **§14, Problems.** Problem 6: "Check your answers against the table when those runs are in." — A textbook problem cannot depend on data not yet produced. Rewrite it against (27) and (28) only.
54. **§14, Further reading.** All five are research papers. S has nothing at the level of the note. One textbook chapter on tunnelling and transfer matrices (for example Griffiths, *Introduction to Quantum Mechanics*, §2.5–2.6 and Problem 2.53; or Davies, *The Physics of Low-Dimensional Semiconductors*, ch. 5 on resonant tunnelling) would serve the stated reader. It must be opened and read before it is cited (STANDARD §4.8).

## Verdicts per section (against STANDARD.md §4 and the 21 October verdict)

| § | Title | Verdict | Reason in one line |
|---|---|---|---|
| 1 | Two panes of glass | needs work | The picture is good. The figure-reading paragraph is a 400-word reference card (2, 3) and contradicts the page's height note (1); caption comma (5). |
| 2 | Model in three dimensions | needs work | The separation proof runs the wrong way (6); one 70-word sentence (7); a solution given with "substitute to check" (8). |
| 3 | One barrier | needs work, small | Derivation sound and checked (numbers reproduce). γ step silent (11); overloaded t, T and R (14); one aside and one adverb (13, 15). |
| 4 | Two barriers, two ways | clear, with one fix | The path sum and Example 4.1 are the best teaching in the note; the "tall lump" claim is unsupported (16). |
| 5 | Sharp peak, trapped wave | needs work | n = 0 and n = 1 for the same state (18); L_eff arrives in a parenthesis (19); a ★ opens and closes inside one paragraph (20); one unshown expansion (21). |
| 6 | Packet is not one energy | needs work | (19) and the key result are clear; the "Long packets" paragraph is a status report with three causes in one sentence (23, 24). |
| 7 | A wider well sings lower | clear, leave it | Picture, (20), (21), table and honest 3D gap all in order; only the sign of the shift (27) and phone table (26). |
| 8 | Taller and thicker barriers | clear, with two word fixes | Leak model, table and key result sound; "when the barriers change" (28), "lower bound" (29). |
| 9 | Three, five and ten barriers | needs work, small | Chebyshev and Bloch derivation good; "ξ = 0 at the pair's resonance" is unshown (30); trace step (31); untested guess (33). |
| 10 | What was computed | needs work | Method clear, but STANDARD §4.5 is not met: no measured Δt error (35), no resolution argument (36), absorber unspecified (37), status and timing without source (38). |
| 11 | How good the grid is | needs work | Honest and measured against theory, but there is no convergence point (39), one unsupported cause (40), and the definitions come after their use (41). |
| 12 | Discs and shells | needs work | The side-leak estimate is good physics, but the table and key result rest on runs "to come" (42, 44), and the shells have no model (45). |
| 13 | The device | clear in its physics, needs small fixes | Tilt, supply function (31) and the peak-before-the-bottom argument check numerically (131 mV, 274 mV, 62 fs, 87 K, 2.75 nm all reproduce); forward unit reference (47), e dropped (48), status paragraph (49). |
| 14 | Limits and reading | needs work, small | Limits named, but the next model has no name or source (52); a problem depends on missing data (53); no textbook-level reading (54). |

## Numbers recomputed by this referee (all agree with the note)

k = 1.212, κ = 1.591, sinh κd = 2.352, |w|² = 6.95, T = 0.144; Example 3.1, T = 6.4 × 10⁻³ (ratio 22.5); (9) gives 0.154;
L_eff = 2.757; (21) gives 0.649; hard box 2.193; Γ from (15) 0.0700; (17) 0.0632; −2 ln R = 0.311 = 2T/√R; σ_E = 0.202,
σ_E/Γ = 2.87; (19) gives 0.218; long packet σ_E = 0.0505, FWHM 0.119; (19) for d = 2 gives 0.036; σ⊥(40) = 7.3, σ⊥(12) = 3.6;
a = 2.75 nm, ħ/E_u = 4.39 fs, Γ = 10.6 meV, τ = 62 fs, k_BT = 0.05 ↔ 87 K; supply 14.2 and 18.0; products 1.04 and 0.74;
run counts 1128 + 188 + 564 + 376 + 423 + 1000 + 60 = 3739; group sizes 24, 4, 12, 8, 9 structures × 47 energies.
