# Fig. 15 · referee report (resonant tunnelling)

Read as rendered: `npm run build`, served from `dist/` on port 9417, opened in headless Chrome at 1400 px, every section
unfolded with its toggle, the "What is rounded…" box opened, and each section screenshotted with the sticky section header
made static so that nothing is hidden. The note's KaTeX renders cleanly (no raw TeX, no overflow at 1400 px). Two readers:
**S**, a school student who is good at mathematics, and **G**, a physics graduate. plan.md and check.md were not read.

Each mark gives the section, the exact sentence, who gets lost (S, G or both) and why.

## Marks

### Abstract

1. "We build it from the Schrödinger equation with no skipped steps: …" (S, G). The claim is not true. The product that gives
   (7) is skipped (mark 10), as are the separation argument (mark 4) and the phase average in section 5 (mark 21). Either do
   those steps or soften the claim.

### 01 · Two panes of glass

2. "At some colours they cancel the straight-through beam and the pair reflects strongly; at others they reinforce it and
   the pair turns almost perfectly clear." (G). This overstates the effect. Bare glass reflects about 4 % per surface, so the
   fringes of two plain panes are faint, and the pair never "reflects strongly". A strong Fabry–Pérot needs mirrors that
   reflect well, and that is exactly the point of the electron case (R = 0.856). The picture should say that the panes give
   faint fringes and that silvering them makes the fringes sharp.
3. Figure 1 is not to scale vertically, and the caption does not say so. The dashed line *E* is drawn at about half of *V*₀,
   but 0.735/2 = 0.37. In the same section, "the slider under *The diode*" should name the slider by its label, "Voltage
   across the barriers"; section 10 calls it "the Voltage slider".

### 02 · The model in three dimensions

4. "substituting into (1) and dividing by χgg gives three pieces, each depending on one coordinate. They are satisfied
   separately by" (G, and S is lost). This is the key step of the whole check, and it is skipped. After dividing, a function
   of (x,t) plus one of (y,t) plus one of (z,t) adds up to zero. So each must be a function of t alone, and that function is
   a phase that can be absorbed. Say this in one sentence. Also say why the same g serves for y and z (the start packet is
   round), and that the z equation is the same as the y equation; (2) prints only y.
5. "Its narrow width holds a spread of sideways wave numbers 1/(2σ⊥), so its parts drift apart, and solving the second
   equation of (2) gives the width at time t," (S). Equation (3) is a bare formula: the solving is not shown and the passage
   is not starred. Either star it, or give the one-line picture: the width grows as σ_v·t, with σ_v = ħ/(2mσ⊥), added in
   quadrature to σ⊥.
6. "With σ⊥ = 3 the packet is 7.3 wide by t = 40" (S). "Wide" here means σ⊥, but section 12 says "about 2σ⊥ = 6 wide". Use
   one meaning of width.
7. Units (G). The text sets ħ = m = 1 ("Equation (1) becomes i∂ₜψ = …"), yet (3), (16), (17), (21) and (28) bring ħ and m
   back. A reader cannot tell which equations are in natural units. Say once that ħ and m are kept in the key formulas to show
   their dimensions. Standard 4 asks for a dimensional check, and no equation gets one in the text.

### 03 · One barrier ★

8. "If χ jumped, χ′ would be infinite; if χ′ jumped, χ″ would be, and the equation would demand an infinite energy." (G).
   This is loose. A jump in χ′ puts a delta function into χ″, and the equation could balance it only with a delta-function
   potential, which a finite step does not have. Say "an infinite potential".
9. "Between two edges the wave only travels, which multiplies a right-mover by e^{ikℓ} and a left-mover by e^{−ikℓ} over a
   length ℓ" (G). Matrix (5) maps right-side amplitudes to left-side ones, so its travel matrix is diag(e^{−ikℓ}, e^{ikℓ}),
   which is the form section 9 uses. As written, the sentence gives the opposite sign. It also never says that (5) assumes the
   edge at x = 0, and that the travel matrix is what moves the origin to the next edge.
10. "Carrying out the product for a square barrier (with the amplitudes referred to the barrier's centre) gives" (S, G). This
    is the central "it can be shown" of the note, and standard 3 forbids it. The product is not shown, and only |w|² comes out,
    not w. The phase of w is needed later as φ in (22), and the phase of z as ρ in (12). Show the product, at least in the ★
    passage, and give w and z themselves.
11. "The form follows for any real potential: reversing time and conjugating ψ leaves the equation unchanged, which pairs the
    rows; and probability is conserved, which fixes the determinant." (S lost; G wants one line more). Say what "pairs the
    rows" means: if (A,B)→(C,D) is a solution, so is (B*,A*)→(D*,C*). Also say that the determinant is 1 only because k is
    the same on both sides; section 13 breaks this (mark 37).
12. "Example 3.1 … twenty times smaller." Section 8 says "22 times more opaque" for the same pair. Use one number:
    0.144/0.00657 = 22.
13. "this is why a scanning tunnelling microscope can feel a single atom on a surface." (G). This is a claim with no source.
    It is fine as colour, but it needs a reference or the factor (about e^{−2κ·0.1 nm} per ångström).

### 04 · Two barriers, two ways

14. "Or it can pass the first, reflect off the second, reflect off the back of the first and then pass the second" (G). The
    back of the first barrier reflects with r′, not r. It equals r only because the barrier is symmetric and its phases are
    referred to its centre. Say so; otherwise r² in (10) is unexplained.
15. "This agrees with the matrix product to one part in 10⁹ (notes/fig15/derive.py)." (S, G). This is a repository path in
    the reader's text, with no link, and the reader cannot open it. The same applies to the closing note of section 14 and to
    the file name in section 7 (mark 26). Link the files, or move the paths to a source note.
16. "For thin leaks, 1 − √(RₐR_b) ≈ (Tₐ + T_b)/2, so" (S). "Thin leaks" is undefined (it means small T), and the one-line
    expansion √((1−Tₐ)(1−T_b)) ≈ 1 − (Tₐ+T_b)/2 is skipped. Also say that t² becomes tₐt_b along with r² → rₐr_b, and give
    where the peak formula T_aT_b/(1−√(R_aR_b))² comes from: the resonant phase makes the denominator |1−√(R_aR_b)|.

### 05 · The sharp peak and the trapped wave

17. "The travel part of θ gives ħ d(2ks)/dE = 2s/v, because dE/dk = ħv: the time to cross the well and back at the group
    velocity." (G, and S is lost two lines later). 2s/v is the time to travel twice the centre spacing, not to cross the
    well, which is s − d wide. The −2d/v is hidden in ρ, because ρ is referred to the barrier centre (ρ_centre = ρ_face − kd).
    Without this, "L_eff = s − d + 2/κ" appears from nowhere. Show the split: 2ρ = 2ρ_face − 2kd, and ħ dρ_face/dE = 2/(κv)
    for a step (the 1/κ penetration).
18. "Each round trip the wave hits two barriers and loses a share T at each, so its probability falls at the rate
    1/τ = 2T/t_rt, as e^{−t/τ}. Put t_rt = ħθ′ into (15) with √R ≈ 1:" (G). Here R = 0.856 and √R = 0.925, so this is an 8 %
    approximation. Yet (16) is then stated as an exact equality and used as one ("τ = ħ/Γ = 14.2"). The exact statement comes
    from the pole of t₂ at E_r − iΓ/2, and that is never mentioned. Either state that τ = ħ/Γ is exact for the decay of the
    pole and that the leaky-bucket count is an estimate, or write ≈. Also, the loss per round trip is 1 − R², which equals 2T
    only to first order in T.
19. "Between resonances sin²(θ/2) is near 1 and T₂ ≈ T²/4R" (S). It is near 1 only midway between resonances, and the
    approximation also needs T ≪ 1. Say "midway between".
20. "A leaky bucket gives the same law in words: the narrower the hole, the slower it drains." The analogy is repeated and
    sharpened in section 8 (mark 28), where it is physically wrong.
21. "The average of 1/(1 + F sin²(θ/2)) over a full turn is 1/√(1+F), and with F = 4R/T² this is T/(1+R) = T/(2 − T)." (S,
    G). The integral is quoted, not done, and the algebra (1−R)² + 4R = (1+R)² is skipped. One line each.
22. "That is just what two independent half-silvered mirrors pass when we add probabilities instead of amplitudes" (S, G).
    These mirrors are not half-silvered (T = 0.144). Say "two partly silvered mirrors", and give the incoherent sum
    T²/(1 − R²) that the sentence describes.
23. Standard 4 asks for a check of (13) or (15) in a limit. None is given here. For example, T → 1 gives no resonance, and
    T → 0 gives δ-function peaks at the bound levels of section 7.

### 06 · A wave packet is not a single energy

24. "with |φ(k)|² the packet's spread of wave numbers." (S). φ is not defined. Say that it is the Fourier amplitude of the
    start packet, normalised so that ∫|φ|²dk = 1, and that it is a Gaussian of width σ_k.
25. "Its energy spread is four times narrower, σ_E = 0.051, now narrower than the peak of the running example." (G). This
    compares a standard deviation with a full width. The packet's FWHM in energy is 2.355 × 0.051 = 0.12, which is wider than
    Γ = 0.070. This is also why the long packet gets only 0.54, not about 1. Compare like with like.
26. "For the thick barriers, d = 2, the long packet passes only 0.0225: ΔE = 0.051 is still much wider than Γ = 0.00291.
    Equation (19) says the same in numbers: for d = 2 it gives 0.0359, and the exact average is 0.035." (G). The run gives
    0.0225 against an exact 0.035, a 36 % shortfall, and the text says nothing about it. The likely cause is in section 8: the
    run (213 time units) is shorter than τ = 344, so most of the trapped part has not yet leaked when the share is read. Say
    so here. A new symbol, ΔE, also appears for what was called σ_E.
27. "For the running example the best of the 5 long-packet runs filed so far passes 0.51 of the packet" (S). "Filed so far"
    is progress-report language in a textbook chapter. The same holds for "runs so far" (section 12), "1237 of them … are
    filed so far" (section 10), the "to come" cells (mark 44) and "built from 170 of the 500 planned runs" (section 13).
    These numbers will go stale. Either move them to one dated status line, or let the page fill them in from the index.

### 07 · A wider well sings lower

28. "Treat the wave as if it were reflected by hard walls standing 1/κ inside each barrier. Then … E_n ≈ n²π²ħ²/2mL_eff²."
    (G). Equation (21) is never evaluated with the page's numbers. For the running example L_eff = 2.76 gives E₁ = 0.65
    against 0.735, which is 12 % low. The table gives the hard box and the finite well but not (21). Add the column, or quote
    the number, so that the reader knows how rough "the trend" is. Also say that κ depends on E, which makes (21) implicit.
29. "The finite well matches the resonances to a few thousandths" (G). For s = 3.5 the second level is 1.445 against the
    resonance 1.486, an error of 0.04. The sentence is true only for the first level.
30. Table: the finite well lists three levels for L = 3.5 and L = 4.5 (third: 1.878 and 1.377), but the resonance column lists
    only two, with no explanation. These levels are below V₀ = 2, so the resonances should exist (broad near the top). The
    page offers the spacing s = 3 as a chip, but the table skips it. The precision is uneven ("0.16" next to "0.162").
31. "(even states)", "(odd states)" (S). Both terms are used without definition: say that cos is even and sin is odd about the
    well's centre. The odd-state relation is not derived (the text derives only the even one).
32. "measures a lifetime of 65.2 (file flat_N2_V2_D1_P3.5_R0_B0_s3_E0.350.bin), against the exact 1/Γ = 58.3: a little
    longer, as section 11 finds for the running example." (S, G). A raw file name sits in the prose. The notation switches from
    ħ/Γ to 1/Γ. And the gap is 12 %, against the 6–8 % of section 11, so "as section 11 finds" understates it.

### 08 · Taller and thicker barriers

33. "Poke a hole in the bottom of a bucket of water and it drains. … The water level falls by the same law each time, a fixed
    fraction per second; only the fraction changes." (G). This is physically wrong. A bucket with a hole drains by Torricelli's
    law: the outflow goes as √h, the level falls linearly in √h, and it reaches zero in a finite time. It is not exponential.
    A fixed fraction per second needs an outflow proportional to the amount left: a capacitor through a resistor, a slow leak
    through a long narrow tube (viscous flow), or radioactive decay. Replace the picture; section 5 uses it too.
34. "A taller barrier raises it a little (0.877 at V₀ = 3)" (S). From 0.735 to 0.877 is a 19 % rise. That is not "a little",
    and it sits next to "hardly moves".
35. "The 3D run at E = 0.7 shows what such a lifetime means in practice. The run lasts 213 time units, less than one lifetime,
    … a straight line … gives 210." (S, G). The sentence does not say which barriers this run used; the reader must guess d = 2
    (τ = 344). Also say why E = 0.7 rather than the resonance 0.744: it is the nearest stored energy. And say that the fitted
    210 is therefore not a measurement of τ.

### 09 · Three, five and ten barriers

36. "must be an eigenvector of P with eigenvalue e^{iqs}, and that requires cos qs = ξ(E)." (S). The step is skipped. Since
    det P = 1, the eigenvalues satisfy λ + 1/λ = tr P = 2ξ, so λ = e^{±iqs} gives cos qs = ξ. One line.
37. Figure 2 caption: "above it lies a gap, 1.126 wide, up to the second band at 2.082." (G). The second band begins above the
    barrier top V₀ = 2, where κ is imaginary. Equations (4) and (7)–(9) are written for E < V₀ only, and the note never says
    how T is computed above the top (κ → ik′, sinh → sin). The runs reach E = 2.6, and the last paragraph mentions "the top of
    the barriers" in passing. One sentence is needed.
38. "the pair's resonance 0.735 is its middle." (G). It is the middle in ξ (ξ = 0), not in energy: the band runs from 0.59 to
    0.955, whose midpoint is 0.77. Say "the centre of the band in ξ".
39. "Equation (23) agrees with the direct product of transfer matrices to 2.3e-12" (S). This is code notation in typeset text;
    write 2.3 × 10⁻¹².

### 10 · What was computed, and how

40. "e^{−ik²Δt/2}", "with an error of order Δt³ per step." (S, G). Here k is the 3D wave vector of the Fourier grid, but k has
    meant √(2E) since (4). The symbol 𝓕 is not defined (say "Fourier transform"). Standard 5 also asks for the global order
    (Δt² over a run), why Δt = 0.01 was chosen (k_max = 2π on a 0.5 a grid gives a kinetic phase of 0.2 rad per step), where
    the method fails, and the splitting error measured on its own. Section 11 measures only the total grid error.
41. "ψ(t_f + τ) = e^{−iEτ}[…], u = τ/Δt_f" (S, G). τ is the lifetime everywhere else. Use another letter for the time since
    the stored frame.
42. "3739 runs in seven groups: pairs of walls and of discs of radius 2, 4, 6, 9 and 12 at four spacings (1128 runs); … the
    diode under 20 voltages (1000)" (S). The page offers five spacings (including s = 3) and disc radii 3 and 5 as chips, and
    the counts do not tell the reader why. Twenty voltages times 25 energies is 500, not 1000; section 13 reveals that the
    second 500 is discs of radius 6. Say so here.
43. "about one nanosecond per point." (S). Per point per step? Say which.

### 11 · How good the grid is

44. "Profile against profile, the grid wave differs from the exact one by 3–4 % of the peak during the collision" (G). The note
    never says how the "exact" time-dependent profile was computed. The exact theory in the note is stationary, (8)–(18).
    Name the reference solution.
45. "A likely cause, which we have not separated further: each barrier is only two grid points thick …" (G). Section 14 then
    states it as fact: "a grid 0.5 a apart makes the barriers a little too opaque". Hedge in both places or neither.
    Measuring it would be better still: a single 1D twin at 0.25 a decides it.
46. "A grid twice as fine would cost eight times the points and twice the steps" (G). This is unsupported. The split-step
    method is unitary for any Δt, but for the same phase accuracy k_max²Δt must stay fixed, which means four times the steps,
    not two.
47. "The measurements below were made on the running example in the first set of runs (115 runs …), all on the resonant run
    E = 0.735" (S). The page's energy slider steps by 0.05 (0.30 to 2.60), so the reader cannot select the run these numbers
    describe. Say that E = 0.735 is not among the current stored energies.

### 12 · Discs and shells

48. "Shrink the walls to discs of radius R" (S, G). R has been the reflection coefficient since (8), and it appears together
    with T in (13), (15) and (23). Here it becomes a radius, in (28), in the tables and in Problem 6. One symbol, one meaning:
    use ρ_d or a for the radius (a is taken too), for instance R_d.
49. "The runs at E = 0.65, the stored energy nearest the resonance, measure it" (G). The stored energies are 0.30 + 0.05 n,
    so 0.75 is nearer to 0.735 than 0.65 is. If the disc resonance sits lower, say so and why. Lateral confinement should
    raise it, not lower it. The "walls" row (15.1) is the E = 0.735 lifetime from the older runs of section 11, not a run at
    0.65, so the row is not a like-for-like baseline.
50. "Key result · … As R grows, the lifetime and the share through both approach the walls' values." (G). The table has a
    lifetime for one radius only (R = 2); every other cell reads "to come". A key result is stated without the data that
    would support it. The table also leaves the "share through, one disc" cell for walls as "—", although section 6 gives it
    (0.149).
51. "Shells. Two spherical shells about the origin, of radii R and R + s, make a different trap: a hollow ball the wave can
    enter from any side. … because a wave inside a closed shell can only leave through the shell" (S, G). The text does not
    say where the wave is trapped: inside the inner shell, or in the spherical gap between the two. Section 10 stores
    "inside and between the shells". The shell height and thickness for these runs are not given. A graduate would also want
    one sentence on the shell's own levels (spherical Bessel functions, the l = 0 level of a ball of radius R).

### 13 · The device

52. Title: "a diode whose current runs backwards" (S). The current never runs backwards. It falls while the voltage rises, as
    the text itself says ("negative differential resistance"). The title teaches the wrong picture.
53. "Electrons in GaAs move as free particles with an effective mass m* = 0.067 mₑ" (S). There is no picture of why a crystal
    electron acts lighter (the periodic lattice potential is folded into the mass). One sentence is enough. (G): AlGaAs has a
    different mass (about 0.096 mₑ at 35 %), and the matching rule becomes continuity of χ′/m (BenDaniel–Duke). The model
    uses one mass throughout, and section 14 does not list this.
54. "A battery across the device holds the right side lower than the left by an energy eV (e the electron's charge, V the
    voltage; in our units we write the energy simply as V)." (S, G). In (29) the letter V now denotes both the potential
    V(x) and the voltage, inside the same equation, beside V₀. Use U for the bias energy, or V_b. Also, "e the electron's
    charge" should read "e the elementary charge"; the electron's charge is −e.
55. "the electron meets the first barrier with less energy below its top than the second, so the first is more opaque." (S).
    The wording reads backwards. The electron is further below the top of the first barrier, because the second barrier's
    top has been lowered by the ramp. "Less energy below its top" suggests it is closer to the top.
56. (G) Under bias the wave number on the right is k_R = √(2(E+V)) ≠ k_L. The transmission is then (k_R/k_L)|t|², and
    |w|² − |z|² = 1 in (6) no longer holds as stated. The text cites "the matrices of section 3" for the staircase without
    noting this.
57. Figure 3: the trapped "level" is drawn as a sloping line parallel to the tilted well floor. An energy level is a single
    energy and should be horizontal. The shading under the emitter also continues below the band edge.
58. "With the exact single-energy T(E,V) the current peaks at V = 0.875 and has its valley at 1.825" (S). The voltages are
    left in natural units. Give them in volts (0.875 → 131 mV, 1.825 → 274 mV), as the table does for the other quantities.
59. "For two walls the curve built from the runs climbs to its top near V = 0.5 and falls to its valley at V = 1.375, a
    peak-to-valley ratio of 5." (G). Smoothing over the packet's spread should lower the peak-to-valley ratio, yet the runs
    give 5 against the exact 4.3, and they peak at 0.5 against 0.875. The text explains neither. It is probably the 170/500
    runs filed, which leaves gaps in the trapezoid sum. Say so, or leave the comparison out until the batch is complete.
60. "Resonant-tunnelling-diode oscillators are the fastest purely electronic oscillators that work at room temperature, near
    2 THz." (G). The cited paper (Maekawa 2016) supports 1.92 THz. "Fastest" needs the source to say so, or a softer word.

### 14 · What the model leaves out

61. "and it makes real current curves lopsided." (G). This is vague. The known effects of charge build-up in the well are a
    shifted peak and intrinsic bistability (hysteresis) in the NDR region; name them. Standard 7 also asks for "the next,
    more complete model". The section names effects but no model: self-consistent Schrödinger–Poisson, sequential versus
    coherent tunnelling, the non-equilibrium Green's function or Wigner-function treatments.
62. Further reading: the note has no links at all. The DOM of `#paper` contains zero `<a>` elements. Standard 8 requires "each
    with a working link" (DOIs exist for all five). The reading list also has no textbook a school student or first-year
    student could open; a chapter of Griffiths's *Introduction to Quantum Mechanics* or Davies's *The Physics of
    Low-Dimensional Semiconductors* would fill that gap.
63. Problems: Problem 1 asks the reader to "derive (9)" from (8), which the text has just done in one line. Problem 6 asks for
    τ_side "for each disc radius the runs have computed", which today is one radius.

### Whole note

64. Type. The body paragraphs render in IBM Plex Sans and only the captions in Latin Modern. STANDARD.md ("Latin Modern in
    notes") and CLAUDE.md ("lecture notes set like a LaTeX document (Latin Modern text …)") ask for Latin Modern text. If this
    comes from the shared `paper.css`, it is not this note's to fix, but the referee notes it.
65. The running energy 0.735 is not a stored energy (the slider offers 0.70 and 0.75, and opens at 0.65). Section 1 should
    tell the reader which slider position is "the running example" and why it is off the resonance by 0.015.

## Verdict per section (against STANDARD.md §4 and the 21 October verdict)

| § | Title | Verdict | Main reasons (marks) |
|---|---|---|---|
| Abstract | — | needs work | false "no skipped steps" claim (1) |
| 01 | Two panes of glass | needs work, small | picture good but overstated for plain glass (2); figure scale and slider name (3) |
| 02 | Model in 3D | needs work | separation step skipped (4); (3) bare formula, unstarred (5); width meaning (6); units and no dimensional check (7) |
| 03 | One barrier ★ | needs work | the product giving (7) is skipped, the core "it can be shown" (10); travel-matrix sign (9); continuity argument loose (8); determinant caveat (11) |
| 04 | Two barriers | clear, with fixes | strong physics and Example 4.1 is excellent; needs r′ = r (14), the inaccessible file path (15), the (11) steps (16) |
| 05 | Sharp peak | needs work | 2s/v vs. well width and the origin of L_eff (17); τ = ħ/Γ stated exactly from an 8 % approximation (18); phase average unstated (21); no limit check (23) |
| 06 | Packets | needs work | φ undefined (24); σ compared with FWHM (25); unexplained 36 % run shortfall (26); status language (27) |
| 07 | Wider well | needs work | (21) never evaluated (12 % off) (28); "few thousandths" false for level 2 (29); missing third resonances, s = 3 missing (30) |
| 08 | Taller, thicker | needs work | bucket analogy physically wrong (33); unidentified run (35) |
| 09 | Bands | clear, with fixes | best section of the note; one skipped eigenvalue line (36), the above-barrier band (37), "middle" (38) |
| 10 | Computation | needs work | standard 5 only partly met: no global order, no justification for Δt, no separate error (40); τ and k reused (40, 41); run counts unexplained (42) |
| 11 | Grid quality | clear, with fixes | honest and measured; reference solution unnamed (44), the hedge contradicted in §14 (45), cost claim (46) |
| 12 | Discs and shells | needs work | R reused for a radius (48); "nearest energy" wrong (49); key result unsupported by the data shown (50); shell trap location unclear (51) |
| 13 | Device | needs work | V means two things in (29) (54); backwards wording (55); unequal k under bias (56); sloped level in Fig. 3 (57); run curve vs exact unexplained (59); misleading title (52) |
| 14 | Limits and reading | needs work | no "next model" named (61); no links at all (62) |

Standard items met across the note: 1 (pictures from experience: swing, bottle, coupled pendulums, echo; all good except
the bucket), 2 (model and the page's numbers), 6 (equation to screen: "Reading the figures" and the open box are good).
Partly met: 3 (derivation; key steps skipped at (2), (7), the phase average, L_eff), 4 (limits for (8) only; no dimensional
check), 5 (method described, error not separated), 7 (limits listed, no next model). Not met: 8 (no working links).
