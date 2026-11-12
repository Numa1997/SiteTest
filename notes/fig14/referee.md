# Referee report · Fig. 14, "A wave packet meets a sphere: the Schrödinger equation in three dimensions"

Page: `public/simulations/schrodinger-sphere.html`, version of commit `0c22270` (12 November 2026, 21:38 UTC). I built the site with
`OUT_DIR=<scratch>/dist npm run build`, served the build locally and opened it in headless Chromium (Playwright). I pressed "Expand all"
and switched off the pinned fold headers so each slice reads cleanly. I took screenshots of the whole note at 1400 px (19 slices) and
390 px (32 slices), and checked 1024 px for overflow. I also ran the figure itself: I paused it at the last frame of the default run,
switched through the four views and the three barrier buttons, and read the readouts and the "Where these numbers come from" box. I read
the text from the rendered page, with the KaTeX source of every formula. I did not read `plan.md` or `check.md`.

Two readers speak below. **S** is a school student who is good at mathematics. **G** is a physics graduate. Each point gives the section and
the sentence, then the reason. I recomputed every number I quote, in Python or by hand, or read it from the running page or from
`public/data/schrodinger-sphere/2026-11-12/*/index.json`.

What I checked and found correct: the derivation of (14) step by step (C, D, the elimination of r, the cosh/sinh form, the E → V₀
limit). Example 4.1 (T = 2.50 × 10⁻⁷; the largest E < V₀ value 1.34 × 10⁻³; T = 0.495 above the barrier). Example 2.1 (7.62 eV,
8.64 × 10⁻¹⁷ s, 1.14 fs). The normalisation of (7) and σ_k = 1/(2σ₀). Equation (9) and 2.541 667. The Gaussian integral and Re(1/α) of
3.3. Example 3.1 (3.716 a, 5.78 a). The fractions 0.589 and 0.359 of (15) and (16). The 0.113 above-barrier fraction: a non-central χ²
with 3 degrees of freedom gives 0.11328. The coefficients of (19): with random Hermitian 6 × 6 matrices the remainder falls as Δt⁴.
Also [V,[V,T]] = −|∇V|², the mask values of (20), n_target = 1342, s = 28, 1316 steps, and Example 6.1. Table 2 matches the stored
half-plane index to the digits printed.

---

## The most important problems first

1. **The note describes a different run from the one the page shows by default (sections 5.2, 7.2, 8, 9).** At the defaults (E = 2.5,
   V₀ = 3, R = 4), the figure plays the true-3D generation `wave3d/e4_v5_r2.bin`. I paused it on the last frame. The caption reads
   "t = 13.33 · frame 32 of 32" and the source box reads "1333 steps of Δt = 0.01". The readouts are **0.239, 0.633, 0.123, 0.0048**.
   Section 9 says: "with the defaults at the last frame they read 0.239, 0.631, 0.126 and 0.0039". Section 8 says "It stores 48 frames …
   the run ends after 1316 steps at t = 13.16". Figure 2 says "at the 48 stored times. The same curves are drawn live in Fig. 14b of the
   page". All of these numbers belong to the half-plane generation (`2026-11-12/index.json`, 48 frames). At R = 4 the page never plays
   that generation. The graph's own axis label, "t = 13.3 →", contradicts the note's 13.16 on screen. A reader who checks the note
   against the figure, as section 9 invites, finds every number slightly wrong.
   Fix: say in section 8 that two sphere generations exist: 405 half-plane runs with 48 frames, and 81 true-3D runs at R = 4 with 32
   frames, a stride of 43 steps and an end at t = 13.33. Then quote the readouts the page actually shows, or say that Figure 2 and
   Table 2 come from the half-plane runs.

2. **The one-dimensional comparison uses one energy, but the packet has many (sections 1, 4, 5).** The headline contrast is "only 2.5 parts
   in ten million get through" (section 1). Section 5 repeats it: "63 % … against 2.5 × 10⁻⁷ for the slab". So do Example 5.1 ("The
   one-dimensional slab gives 0.000 025 %") and the dotted curve of Figure 3. The number is (14) at the single energy E = 2.5. The note
   stresses that the packet has an energy spread (3.2: width about 0.37; 5.2: "11 % of the default packet has more energy than
   V₀ = 3"). The note's own packet average, equation (24), gives a different answer for the same slab (d = 8, V₀ = 3). I computed
   T_packet = ∫|φ(k)|² T(k²/2) dk = **0.041**, not 2.5 × 10⁻⁷. In one dimension, 10 % of the packet lies above the barrier and much of it
   passes. The conclusion survives: 0.04 is still far below 0.63. But "wrong by orders of magnitude, because it forbids the side roads"
   (5.2) is not true for packets: the factor is about 15, not 10⁶. A G reader will catch this at once, because (24) sits in the same
   note. Fix: state the packet-averaged slab value next to the monochromatic one in section 1, Example 4.1, section 5 and Table 2, or
   say plainly that the guide is a single-energy reference. The guide readout itself prints "T = 0.000" (see section 9 below).

3. **A wrong statement about the crests (3.3, Key result · the free packet).** The box says: "The crests inside the packet move at the
   phase velocity ω/k₀ = k₀/2, half as fast: they appear at the back of the packet, run forward through it and fade at the front." The
   crests are slower than the envelope, so seen from the packet they drift backwards. They appear at the **front**, move back through
   the packet and fade at the **back**. The sentence describes deep-water waves, where the phase velocity is twice the group velocity,
   which is the opposite case. The reader can see it on the page in the Sheets view: the wine sheets slip backwards through the packet.

4. **Section 9.1 describes barriers the page does not offer as described.** (a) "Under Barrier the sphere can be replaced by a round
   pillar": in the built page the Pillar button is disabled with the tooltip "Not stored yet". No pillar generation is in
   `generations.json`, yet the note quotes "about 4 % of the probability over a run" and "less than 10⁻³" for it. (b) "a flat wall
   |x| < a/2": the wall has five thicknesses (0.5, 1, 1.5, 2, 3) on the slider, labelled "Wall thickness a". So **a** means both the
   unit of length and the wall thickness; the canvas caption reads "wall a = 1 a thick". (c) "or a well (V₀ < 0)": the stored wells are
   for the wall only (V₀ = −4, −2, −1). For the sphere, the V₀ slider offers −4, −2, −1 and "hard" stops that are not computed. They fall
   back to the live preview, or to "Not computed yet: the hard sphere needs new GPU runs". Section 8.1 lists the out-of-grid values as
   "E up to 6, V₀ up to 12, R from 1 to 8" and does not mention them.

5. **The ★ promise is broken in 3.3 and 4.2.** The abstract says: "Paragraphs marked ★ carry extra mathematics; you can skip them,
   because their results are restated without the star." But the ★ sits on the subsection headings 3.3 and 4.2. Everything inside
   them is therefore skippable: the Key result boxes with (11) and (14), Example 3.1, Example 4.1 and the plain-words paragraph "Why
   does the packet spread?". Sections 5, 7, 9 and the Problems all use (11) and (14). No unstarred passage restates them. Section 6.3
   does it right with its "In words:" paragraph. Fix: put the ★ on the derivation paragraphs only, or move the Key result boxes and
   examples out of the starred subsections.

6. **Example 7.1 overstates the checks.** "Three tests tell us that the stored runs solve (4)." The second test is "P_behind + P_inside
   + P_ahead + P_lost = 1 by construction". An identity that holds by construction tests nothing. The text then concludes "The
   probabilities on the page are good to about two parts in a thousand", one sentence after it gives the grid error as "up to
   3 × 10⁻³". The grid test was also run on one case only (E = 2, 6.3). The fastest packet, E = 4.5, has 4.2 points per wavelength (6.1),
   where the grid error must be larger, and it was not measured. G will also notice what is missing: no check against an independent
   3D result, such as hard-sphere partial waves at k₀R ≈ 9, which section 10 names as "the next model". Fix: drop the identity as a
   "test", give the error as "a few parts in a thousand" (or measure E = 4.5 on 256³), and say what is not checked.

---

## Section by section

### Front matter and section 1 · A ball, a wall and a pillar

- **S, Figure 1 caption.** The caption uses \(x_0 = -14\,a\), \(\sigma_0 = 3\,a\), \(k_0\), \(R\), "the grid unit" a and "128³
  points, Δx = 0.5 a" (in the plot). All of these are defined only in sections 2.2, 2.3 and 6.1. A first reader does not know what *a*
  is. Fix: one clause, "lengths in a unit a, defined in section 2", or move the figure to the end of 2.3.
- **S, paragraph 3.** "13 % still beside it": "beside" is only made precise in 5.2, where the note itself warns: "Note that the slab
  'inside' is |x| ≤ R across the whole box, not the sphere itself." The words "behind, inside, ahead" are the page's main readouts. Say
  in section 1 that they are slabs of space cut by the planes x = ±R.
- **G, paragraph 3.** "only 2.5 parts in ten million get through": see main point 2.
- **Physical picture.** The tennis ball and the harbour pillar are good, everyday pictures, and they come before any symbol. They meet
  standard item 1.
- **Rendering.** In Figure 1 the label "k0" is not set as a subscript (it reads k0 on the baseline) and touches the arrowhead. The label
  "packet at x₀ = −14" runs into the dashed line x = −R.

**Verdict: clear, with small fixes.** Define *a* before Figure 1 and qualify the 2.5 × 10⁻⁷.

### Section 2 · The model

- **S, 2.1.** "A complex number has a size and an angle, ψ = |ψ| e^{iφ}." Nothing says why the wave must be complex, or what the *i* in
  (2) does. A student who is good at mathematics will stop here. One physical sentence would carry them: the *i* makes the equation
  turn the phase like a clock hand instead of making the wave grow or shrink, and that is why the total probability stays fixed. That
  sentence would also prepare the Key result of 6.2.
- **S, 2.1.** "The right-hand side is the total energy acting on the wave". "Energy acting on" is not a meaning a student can use. Say
  instead: the right-hand side is the energy operator, kinetic plus potential, applied to ψ.
- **S, 2.1.** \(\mathrm d^3 r\) (a small volume) is used without a word.
- **S, 2.2, the step to (4).** "The unit of time is then m a²/ħ and the unit of energy ħ²/(m a²) … and (2) becomes (4)." The
  substitution x = a x̃, t = (m a²/ħ) t̃, V = (ħ²/m a²) Ṽ is skipped. One line would show where both units come from. That line would also
  be the dimensional check that standard item 4 asks for. The note never does a dimensional check once the units are set to 1.
- **S, 2.2.** "a unit a of our choosing, the grid unit". Section 6.1 then sets Δx = 0.5 a: the grid spacing is half a "grid unit". Call
  *a* "the unit of length", or explain the name.
- **S, Example 2.1.** "The default packet energy E = 2.5" and "the default barrier V₀ = 3": E is defined only in 2.3 ("the packet energy
  chosen with the slider"). "The sphere of radius 4a is 0.4 nm across its radius" should read "has a radius of 0.4 nm".
- **S/G, Table 1.** The row "phase turns across the packet, k₀σ₀ = 6.71" is wrong as labelled: 6.71 is in radians over one width, which
  is 1.07 turns. Write "phase change across one width (radians)".
- **G, standard item 2.** The assumptions are stated only in section 10: one particle, no spin, non-relativistic, a static potential
  with a sharp edge. The model section should state them, with one number for the regime. For the 19 eV electron of Example 2.1,
  v/c ≈ 0.009, so (2) holds.
- **Rendering.** The caption of Table 1 breaks after "combinations of E", so the next line starts with ", V₀". At 390 px the line
  "m = 0, 0.775, …" of 7.1 sticks out 15 px, and the hidden KaTeX MathML in 2.1 and 2.2 makes the whole page scroll sideways by 14 px
  (scrollWidth 404 at a 390 px viewport).

**Verdict: needs work, small.** Add the physical reason for *i*, the units step, the assumptions, the Table 1 label, and define E before
Example 2.1.

### Section 3 · A packet in free flight

- **Error, 3.3 Key result.** The crests: see main point 3.
- **S, opening paragraph.** "its wave moves at one speed while its crests move at another": "its wave" should be "the packet as a
  whole (its envelope)". Otherwise the sentence says the wave moves at a different speed from the wave.
- **S, (8).** σ_x appears for the first time in (8) and is never defined. The reader has met only σ₀. Write σ_x = σ₀ at t = 0.
- **S, 3.2.** "The mean of k_x² over (7) is k₀² + σ_k²": this uses ⟨(k₀+q)²⟩ = k₀² + 2k₀⟨q⟩ + ⟨q²⟩ with ⟨q⟩ = 0. That step is
  skipped, and the angle brackets ⟨ ⟩ for an average are not introduced.
- **S, 3.2.** "the width of the energy distribution along x: roughly k₀σ_k". Skipped step: E = k²/2, so a small change dk changes E by
  k dk. One clause would do.
- **S, 3.3.** "∝" (proportional to) is used without a word. "Taking x₀ = 0 for brevity" is fine, but then "Its centre has moved to
  x = k₀t" should add "(x₀ + k₀t in general)", because Example 3.1 immediately uses x₀ = −14.
- **G, 3.3.** The prefactor √(π/α) also depends on t; dropping it behind "∝" is right but deserves "(the prefactor keeps the norm
  1)".
- **Voice (21 October verdict, item 3).** "Why does the packet spread?" opens a paragraph with a rhetorical question, which the house
  rules forbid. Write instead: "The packet spreads because its waves have different wave numbers …".
- **★.** See main point 5: (11) and Example 3.1 are inside the starred subsection.
- **Physical picture.** The picture "fast components run ahead, slow ones fall behind" is good.

**Verdict: needs work.** Correct the crest sentence, define σ_x, add the two skipped steps, and move the Key result out of the ★.

### Section 4 · A wall in one dimension

- **S, 4.1.** "(12) is the equation of a simple harmonic oscillator in space": say why. u'' = −k'²u has the same form as ẍ = −ω²x, so
  its solutions are sines in x as an oscillator's are in t. The phrase is a good bridge for a school student but is left unexplained.
- **S, 4.1.** k' = √(2(E − V)) uses V, but (13) switches to V₀. Use one symbol.
- **Physical picture, 4.1.** The evanescent wave has no everyday picture. Light that is totally reflected inside glass still reaches a short way
  beyond the surface. Look through the side of a glass of water at the fingers holding it: the glass looks silver, except where the
  ridges of the skin touch it. There the evanescent light is taken up and the reflection breaks (frustrated total internal reflection,
  the optical cousin of tunnelling). This is the natural picture, and it costs one sentence.
- **S, 4.2.** "Taking the square of the size and using cosh² = 1 + sinh²" hides a second identity:
  (κ² − k²)² + 4k²κ² = (κ² + k²)². Without it, a student cannot get from the line before to the displayed T.
- **S/G, symbols.** In 4.2, *t* is the transmission amplitude, but *t* is time everywhere else, including e^{−iEt} two lines earlier.
  *T* is the transmission probability here and the kinetic-energy operator \(\hat T\) in 6.2. Use τ_t or 𝓉, or call the amplitude
  *s*. This breaks the Taylor rule of one symbol, one meaning.
- **G, 4.2.** "T = |t|², because the transmitted wave has the same wave number, and so the same speed". That is true, but the
  probability current j = Im(ψ*∇ψ) is never introduced, and it is what makes the statement right in general. It is also what section 5
  counts. One sentence in 2.1 would serve 4.2, 5 and 7.
- **G, 4.2.** "(Both branches were checked … against the page's own function T1D …)": T1D is a code name. The reader does not know it.
- **G, Example 4.1 / main point 2.** The example is about a single energy, and the packet average is never given here.
- **Rendering, 1400 px.** In the unnumbered display "2ik = …" the second line's numerator "t e^{ikd}" overlaps the first line's
  denominator "2κ" (seen in the 1400 px screenshot of section 4.2). At 390 px, (14) breaks into seven lines with "(E" and "< V₀)" split
  across lines, and it is hard to read.

**Verdict: needs work, small.** The derivation is complete and correct apart from the hidden identity. Rename *t* and *T*, add the
evanescent picture, and fix the overlapping display.

### Section 5 · A sphere in three dimensions

- **Main point 2** applies to the opening paragraph, Table 2, Figure 3 and Example 5.1.
- **G, 5.2, "The reason is the harbour pillar of section 1."** Bending into the shadow explains why more probability goes *ahead*. It
  does not explain why less goes *behind*, which is the larger of the two differences (0.073 against 0.054). In the slab bookkeeping,
  the diffracted wave that fills the shadow comes from wave that would have gone ahead anyway. The missing backscatter needs its own
  argument, or the sentence should say only what it shows. Example: reflection from a curved soft surface with a 1 a penetration depth
  acts like a smaller sphere, and the energy tail passes over the top.
- **G, 5.2, the softness paragraph.** "the packet's spread of energies … means that 11 % of the default packet has more energy than
  V₀ = 3". The classical cloud has exactly the same spread of energies, by construction (5.1, "exactly the distribution of position
  and momentum that (5) describes"). Yet its "behind" barely moves between V₀ = 3 and 8 (0.312 against 0.316). So the energy spread
  cannot be what separates the wave from the balls. Only the penetration-depth part of the argument is quantum. Say so, or drop the 11 %
  from this paragraph.
- **S, 5.2.** "computed exactly from the non-central χ² distribution". A school student has never met this distribution. Either explain
  it in one clause (the distribution of |k|² when each component is a bell curve), or say "computed numerically".
- **G, 5.2.** "Only for very high walls does the wave approach the hard-sphere answer from below." Which hard-sphere answer: the
  classical 0.316, the geometric 0.359, or a quantum hard sphere? No hard-sphere run exists (the page reports "Not computed yet"). The
  claim is unsupported.
- **G, Table 2 caption.** "Classical counts include balls that have flown into the border region; the quantum values exclude what the
  border has absorbed (0.4 % to 7 % here)". The differences being explained are 0.03 to 0.11. An accounting difference of up to 7 % (run
  2.5, 8, 6: 6.9 % lost) is the same size, so the comparison is not like with like in that row. Also, the range is 0.07 % to 6.9 %:
  run (4.5, 4, 2) lost 0.0007.
- **S, 5.1.** "four balls in ten miss the sphere altogether": this is true of the starting positions. It ignores the sideways spread of
  velocities on the way in (σ ≈ 3.16 a by the time the packet arrives). Add one clause.
- **S, Figure 3 caption.** "oscillates above the barrier": on this plot the horizontal axis is V₀, so "above the barrier" (E > V₀) is the
  *left* side, and a student reads "above" as "to the right / higher V₀". Write "for V₀ < E".
- **Rendering.** In Figure 2 the "ahead" curve runs through the legend entry "lost" and hides its dotted swatch.
- **Physical picture.** The picture is strong: the ball reflected like light from a polished ball, and the side roads.

**Verdict: needs work, the most important section.** Its central comparison (main point 2), its explanation of "less behind" and its
softness argument each need a correction or a qualifier.

### Section 6 · The split-step Fourier method

- **S, 6.1.** "in about N log₂ N operations instead of N²": in 3D the number of points is N³. The count for one transform of the whole
  grid is N³ log₂ N³. Say which N.
- **S, 6.2.** "Over a short time Δt the exact solution is ψ(t + Δt) = e^{−iĤΔt}ψ(t)." The exponential of an operator is not defined
  for S, as a power series or as "apply to each plane wave". Nor is it said that the formula is exact for any Δt, not only a short one.
- **S, 6.2.** "Each half of Ĥ alone is easy": "half" here means each of the two parts, and four lines later "half a kick" means half a
  time step. Write "each part of Ĥ".
- **G, 6.2.** "In the chemistry literature this scheme is called the split-step Fourier method, after Feit, Fleck and Steiger (1982)". The
  name is older and comes from optics and acoustics: Hardin and Tappert (SIAM Review 15, 1973) used "split-step Fourier" for the
  nonlinear Schrödinger equation. Feit, Fleck and Steiger worked at Livermore on optics, not chemistry. The note says honestly that it
  relies on reference 3 for this. Better to drop "chemistry" and the attribution of the name, or check it.
- **G, 6.2.** "rounding in single precision has a small bias": a measured fact (3.3 × 10⁻⁴ in 1500 steps) given an unsupported cause.
  Either say "we measured a steady loss whose cause we have not traced", or name the cause.
- **S, 6.3.** "At the page's Δt = 0.01 the error of the wave function is therefore about 4/3 × 7.45 × 10⁻⁵". The 4/3 is a skipped step:
  if e(Δt) = CΔt², then e(Δt) − e(Δt/2) = ¾ e(Δt). One clause.
- **G, 6.3.** "For the sphere, V jumps at the surface, so the whole splitting error sits on the sphere's surface". For a true step, |∇V|²
  is the square of a delta function, and the BCH expansion is only formal. On the grid V is a staircase of finite steps, which is why the
  measured ratio is 4.0. One sentence would answer the objection a graduate will raise.
- **Voice.** "How far is (18) from the exact e^{−iĤΔt}?" (opening of 6.3) is a rhetorical question, and the title "Example 6.1 · is the
  step short enough?" is a question. The house rules forbid both.
- **G, Example 6.1.** "Unlike the explicit schemes of many textbooks, the split step stays stable for any Δt". True, but "explicit
  schemes" and their stability limit are not named. One example (forward Euler, or the Δt < Δx² limit) would make the contrast mean
  something.
- **Standard item 5.** Integrator, order, step, why it was chosen, where it fails and the measured error are all present, measured and
  correct. This is the strongest section of the note.

**Verdict: clear, with small fixes.** Fix the 4/3 step, the history sentence, the two questions and the discontinuous-V remark.

### Section 7 · The border and the checks

- **Main point 6** (Example 7.1).
- **G, 7.1.** "a sudden edge would itself reflect the wave". The note never measures how much the mask (20) itself reflects, though it
  measures everything else. One number would close the gap: the reflection of a free packet sent into the frame. Equation (20) (the
  eighth root of a sine) has no source either. Absorbing masks of this kind go back to Kosloff and Kosloff, J. Comput. Phys. 63 (1986);
  if no source was opened, say the form was chosen by hand.
- **S, 7.1.** "falls to 0 over the outer W = 12 points" (text) against "the outer 12 cells" (Figure 1). Use one word.
- **S/G, symbol.** The mask is m(x); *m* is the particle's mass in (2) and in 2.2.
- **S, 7.2.** "At the end of the run P_lost = 0.0039". On screen at the defaults it reads 0.0048 (main point 1).

**Verdict: needs work.** Fix Example 7.1 (main point 6), add one number for the mask's own reflection, and rename the mask.

### Section 8 · Computed once, played back

- **Main point 1**: the 48-frame description does not hold for the R = 4 runs the page shows by default.
- **Number out of date.** "On the website the 405 files take 46.4 MB". I measured the 405 half-plane files at **62.7 MB**. The 46.4 MB
  dates from commit `1d340bf` ("amplitude only"). The site also holds the true-3D runs (101.0 MB) and the flat-wall runs (52.1 MB).
- **Contradiction with section 9.** Section 8 says: "the phase picture computed with them stays with the Kaggle notebook". Section 9 says
  the page keeps "p, the phase arg ψ in 256 steps" for every point. One of the two is stale.
- **S, 8.** ⌊ ⌋ (floor) and "round" are used without a word, and \(\bar y\) in the σ_y formula is not defined (the mean of y).
- **8.1.** The list of out-of-grid stops leaves out V₀ < 0 and "hard" for the sphere (main point 4c). The popup about "kaggle-bridge …
  not switched on yet" that a reader meets there is not mentioned anywhere in the note.
- **G, 8.1.** "for E > 3.05": with k₀ + 4σ_k = k₀ + 2/3 exactly, the threshold is E > 3.06; 3.05 comes from rounding 0.667 to 0.67.
  Problem 10.6 asks the reader to "show" 3.05.

**Verdict: needs work.** Correct the facts: the two sphere generations, the data sizes, and phase stored or not.

### Section 9 · From the equation to the screen

- **Main points 1 and 4.**
- **Wrong reference.** "both the starting packet (5) and the potential (2) are unchanged by any rotation about the x axis": the
  potential is (3).
- **S, paragraph 1.** "q = round(255 |ψ|/|ψ|_peak)" and "p": *q* was k − k₀ in 3.3, and *p* is momentum in 3.1. Later the text says
  "Re ψ … differs … by 0.9 levels of 127 in the root mean square and 17 at worst". "Levels of 127" is never defined. Presumably Re ψ is
  stored as a signed level from −127 to 127, but the paragraph has only described 0–255 for |ψ|.
- **S, paragraph 2.** "Fog is the earlier view": earlier than what? A first-time reader has never seen another version of the page.
  Write "Fog draws the wave as coloured mist …".
- **S, paragraph 2.** "the distance between neighbouring wine sheets is one wavelength 2π/k₀". This is true in the incoming packet.
  Near the sphere the reflected wave overlaps, and the packet is chirped by its spreading. Add "in the incoming packet".
- **Equation to screen, missing pieces (standard item 6):**
  1. Fig. 14b has a vertical line that marks the current time. The note does not mention it.
  2. The "Read values" probe (click to pin, Esc to stop) is not described: what it reads, and where its numbers come from.
  3. In the Surface view, colour also encodes Re ψ (the caption on the canvas says "height and colour: Re ψ in the plane z = 0"). The
     note mentions only height.
  4. The pink translucent ball ("glass sphere R = 4 a" on the canvas), the dashed flight axis and the floor grid with its shadow are not
     named. Say that the ball is the surface |r| = R, and that the shadow and lighting are decoration only.
  5. In the Sheets view at late times, ragged fragments with holes appear near the edges of the box. The paragraph "Three things differ
     from the model" should say what they are (iso-surfaces of low-amplitude noise, or the box edge cutting the sheets).
- **The guide readout.** "The guide line evaluates (14) for a slab of thickness 2R". On screen it prints "E < V₀, forbidden classically ·
  T = 0.000". The reader cannot see the 2.5 × 10⁻⁷ of Example 4.1 there, and (main point 2) the packet value would be 0.041.
- **9.1, symbols.** φ (varphi) is the phase in 2.1 and the pillar's wave function in (22). φ (phi) is the Fourier weight in (7). χ is
  the wall's wave function and also the χ² distribution of 5.2. *g* depends on t, but the text says "weighted by g(z)".
- **9.1, typography.** In \(g(z,t)\) the expression "it/2σ₀²" reads as (it/2)·σ₀²; write \(it/(2\sigma_0^2)\).
- **9.1, S.** "Substituting (22) into (4) and dividing by φg shows it: the two sides separate term by term." Write the one line; it is the
  whole argument.
- **9.1, G.** "Crank–Nicolson … keeps the norm exactly because the two factors are each other's complex conjugates". For operators the
  word is Hermitian adjoints. The norm is kept because the Cayley form (1 + iΔtĤ/2)⁻¹(1 − iΔtĤ/2) is unitary when Ĥ is Hermitian. The
  superscript n in χⁿ (the time level) is not defined.
- **9.1, G.** "A hard wall lets through at most 10⁻⁶". With the points inside removed and ψ = 0 on both faces, the exact answer is 0.
  Where does 10⁻⁶ come from: the fourth-order stencil reaching across, or rounding? Unexplained.
- **9.1, G.** "For the pillar, ψ is set to zero inside after every step. That removes … about 4 % of the probability over a run". A 4 %
  numerical loss is twenty times the accuracy claimed in 7.1. If it comes from the projection after each step, it should shrink with
  Δt. "Halving the time step changes the probability ahead … by less than 10⁻³" does not say what happens to the 4 %.
- **9.1, missing definition.** For the wall, "behind / inside / ahead" are not defined. The stored index uses |x| ≤ a/2 (Rs = 0.25 … 1.5);
  the reader sees "inside" peak at 0.13 for a 1 a wall with no explanation.
- **9.1, missing number.** "in the 510 stored runs that end with less than 0.002 of the probability inside the wall": the reader is never
  told that there are 585 wall runs (9 E × 13 V₀ × 5 thicknesses, including wells and the hard wall).

**Verdict: needs work, major.** The default readouts are wrong, the pillar text describes a barrier that is switched off, *a* has a double
meaning, and several elements on screen are not mapped to symbols.

### Section 10 · What the model leaves out, Problems, Further reading

- **Limits (standard item 7).** These are clear and honest: spin, Dirac, many electrons, measurement, the finite box, and the next model
  (stationary scattering, partial waves, ℓ ≈ kR ≈ 9). Leave them.
- **S, paragraph 1.** "a smooth edge reflects less than a sharp one": add "for E > V₀". For E < V₀ the wave is reflected either way,
  apart from tunnelling. Problem 10.5 already restricts to E > V₀.
- **Problem 10.2.** "compare σ_y with σ_free in the data panel": σ_free is not defined in the note.
- **Further reading (standard item 8).** The standard admits "only real sources you opened and read". Reference 4 says of itself: "Only
  their publisher records could be opened for this note (the full texts are behind paywalls)". That is honest, but it breaks the rule.
  Either keep the two papers only as the history sentence's source with that caveat moved into 6.2, or replace them with an open source
  that was read. There is also no source for the absorbing mask, for the classical-cloud comparison, or for partial-wave scattering of a
  sphere beyond the two textbooks.
- All five links resolve to the right records: Cambridge (2), arXiv 2401.01722, and the DOIs 10.1016/0021-9991(82)90091-2 and
  10.1137/0705041. Their targets were not opened here.

**Verdict: clear, leave it**, apart from the reference-4 rule and σ_free.

---

## Verdicts against `notes/STANDARD.md`, one line each

| Section | Verdict | Standard items failing |
|---|---|---|
| 1 A ball, a wall and a pillar | clear, small fixes | 2 (symbols in Fig. 1 before definition), main point 2 |
| 2 The model | needs work, small | 1 (no picture for the complex *i*), 2 (assumptions deferred to §10), 3 (units step skipped), 4 (no dimensional check) |
| 3 A packet in free flight | needs work | correctness (crest direction), 3 (σ_x undefined, two skipped steps), ★ rule, no rhetorical questions |
| 4 A wall in one dimension | needs work, small | 3 (hidden identity), one symbol one meaning (t, T), 1 (no picture for evanescence), ★ rule, rendering |
| 5 A sphere in three dimensions | needs work, major | correctness of the 1D comparison (main point 2), unsupported claims (less behind, softness, hard-sphere limit), like-with-like accounting |
| 6 Split-step Fourier | clear, small fixes | 3 (the 4/3 step), history claim, no rhetorical questions |
| 7 Border and checks | needs work | 4 (a "check" that holds by construction; accuracy overstated), 5 (mask reflection unmeasured) |
| 8 Computed once | needs work | correctness (sizes, frames, phase), 6 (out-of-grid stops) |
| 9 Equation to screen | needs work, major | 6 (default readouts, unmapped elements, guide prints 0.000), 9.1 describes a disabled pillar, *a* double meaning |
| 10 Limits, Problems, Reading | clear, leave it | 8 (reference 4 not read) |

## Rendering faults seen in the screenshots

- 1400 px, 4.2: the two lines of the unnumbered "2ik = …" display overlap: "t e^{ikd}" sits on "2κ".
- 1400 px, Figure 2: the "ahead" curve crosses the legend and hides the "lost" swatch.
- 1400 px, Figure 1: "k0" is not subscripted and touches the arrowhead. "packet at x₀ = −14" runs into the dashed line.
- 1400 px, Table 1 caption: a line starts with ", V₀".
- 390 px: the page scrolls sideways by 14 px (scrollWidth 404). The cause is KaTeX's hidden MathML in 2.1 and 2.2, plus the mask list in
  7.1, which overflows by 15 px. Equation (14) breaks into seven lines, with "(E" / "< V₀)" split.
- No KaTeX errors and no console errors (only WebGL "GPU stall due to ReadPixels" performance warnings).
