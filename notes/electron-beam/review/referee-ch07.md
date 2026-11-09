# Referee report · Project 07, Chapter 7 "Detect and measure" (`#ch07`)

Read as two people at once: a school student who is good at mathematics, and a physics graduate who knows CD-SEM metrology
and is reading this as a job applicant's portfolio. Only Chapter 7 and its simulation `#sim-ch07` were read
(`text/ch07.py`, `physics/ch07.js`). `PLAN.md` and the check files were not read.

**How it was read (9 November 2026).** I built the page with `python3 portfolios-src/electron-beam/build.py --site --out
<scratchpad>/index.html` ("8 of 10 chapters, 96 equations"). My build differs from the served
`public/portfolios/electron-beam/index.html` only inside chapter 6 and the inlined `ch06.js`. Those come from uncommitted chapter 6
edits by another session in the working tree. Chapter 7's markup is identical in both builds, so I reviewed the served file
(HEAD `78fbab0`). I served `public/` locally and opened it in headless Chromium (Playwright) at 1400 px and at 390 px. The
simulation was also shot at device scale 2. Chapter 7 has no folds: sections 7.1 to 7.7 and the simulation all render open,
and I screenshotted each one whole at both widths. There were no console errors. I read KaTeX from the rendered page. I drove
the simulation through `EB.sims.ch07.set` at 8 settings, and I called the module (`EB.ch07.compute`, through Node) at about
40 more. Where this report says a number was "measured", it is the module's output. Where it says "recomputed", I worked it
out by hand or chained in chapter 5's module.

**One source could not be checked.** The Applied Materials product page cited in 7.3 and 7.6 returned 403 (Akamai "Access
Denied") to curl. The Wayback Machine copy (snapshot 12 May 2026) reset the connection three times. I did not try to get
past the bot check, so I have not verified the two quotations. The project's own source record
(`sources/applied-public.md`, §3) lists both quotations under "Verified earlier by the planning session … not re-read by
me". The page, however, says "read 9 November 2026". Someone who did read it should confirm that date.

Verdicts are judged against `notes/STANDARD.md` §4 (1 picture, 2 model, 3 derivation, 4 checks, 5 numerical method,
6 equation to screen, 7 limits, 8 reading) and Numa's verdict of 21 October 2026. That verdict asks for Taylor's way of
teaching: every step shown, every symbol defined where it first appears, one symbol with one meaning, ★ results restated
unstarred, and no question-form headings.

**What is good, first.** The chapter is short, it reads in order, and its central idea is right and well placed: precision is
bought with electrons, and electrons cost time and dose. Every number in the text reproduces from the module:
n̄ = 6.242, SNR = 1.878, CD_m = 28.563 nm, σ_CD = 0.2714 nm and 0.2850 nm (Monte Carlo, MC), D = 100 µC cm⁻², 3508 per hour.
At 1 µs: 0.0858 nm, a ratio of 3.163, 1000 µC cm⁻², 2852 per hour. For the fin: 4.24, 24.65 nm, 0.194 nm. For the blunt probe:
28.99 nm and 1.886 nm. The dose arithmetic (1 C m⁻² = 100 µC cm⁻²), the excess (7.1) and its β → 0 limit, the compound-Poisson
variance (7.3), the FW50-to-σ conversion and the Applied arithmetic (36 µs, 730 per image) are all correct. Three things
are honest and well judged: bias is separated from scatter, "our rate and the claim measure different things" is said
plainly, and "Whether secondaries really follow Poisson statistics we did not verify" is stated openly. The weaknesses
fall into four groups. Two of the three Problems are wrong. One symbol is used for three things. The text never gives the
yields, blur or escape depth, though every result depends on them. And the comparison of propagation with Monte Carlo is
claimed more generally than the module supports.

---

## The ten most serious places

1. **Problem 2 has no answer of the kind it asks for.** "find the dwell time that gives the most measurements per hour at a
   required σ_CD when the number of lines N can be chosen freely, and explain why the answer depends on t_ov." From (7.5),
   a fixed σ_CD at fixed I_p fixes the product t_d N = K. The time per site in (7.6) is then N²t_d + t_ov = NK + t_ov. That
   is smallest at the smallest N (the longest dwell), and t_ov, an added constant, cannot move the minimum. Measured: at
   t_d N fixed, σ_CD = 0.2714 nm for every N from 64 to 1024, while the scan time doubles with each doubling of N. The
   problem asks the student to explain a dependence that does not exist. A related point: the module never checks that
   the square image N·Δx is wider than one period. At the N slider's minimum (32), the field is 32 nm, narrower than the
   40 nm pitch, and the panel still reads a width (σ_CD = 1.09 nm, no warning).

2. **Problem 1's premise is false at the page's own defaults.** "Why does the module's error propagation give more than √2
   times this for the width?" Recomputed from `setup()` and `yieldAt()`: at the right edge, σ_S/|S′| = 0.212 nm, so √2 times
   that is 0.300 nm. The module gives σ_CD = 0.271 nm, which is *less*. Linear interpolation between two pixels averages
   their noise (weights 1−f and f), and that more than offsets the noise of the peak and floor levels. With 5 nm pixels the
   module gives 0.101 nm against √2 × 0.204 = 0.289 nm. The "more than" holds only for the blunt probe (1.886 against 1.708)
   and narrowly for the fin (0.194 against 0.209, so not there either). The same imprecision is in the text of 7.5: "Near a
   crossing the derivative is 1/|S′|". That is the derivative with respect to a uniform shift of the profile near the
   crossing, not with respect to one pixel. For one pixel it is (1−f)/|S′| or f/|S′|.

3. **One symbol, three meanings: N.** In 7.3 N is the count in one pixel ("⟨N⟩ = n̄m, Var N"). In 7.5 it is the number of
   lines averaged ("divided by the number of lines averaged, N"), and (7.4) uses both in one fraction: "Var N_i / N". In 7.6
   it is the pixels per line, inside N²t_d, where it is never named and the student must infer N = 512 from "512 by 512".
   In check C1 it is a fourth thing, the number of beam electrons ("E[N]Var[K] + Var[N]E[K]²", with K undefined). In the
   sentence "the 1/√N law of counting statistics" a student cannot tell which N is meant. Other clashes of the same kind:
   **b** is a wall end in (7.2) and the floor level in 7.4. **n** (the number of pixels in f(S₁,…,S_n)) sits beside n̄ (beam
   electrons per pixel). **f** is a function here and the focal length in chapter 4. **η** is the backscatter coefficient
   here, **η_c** the collection fraction, and η = e/(8mV\*) in chapter 4. Numa's rule is one symbol, one meaning.

4. **The model's actual numbers are missing from the text (STANDARD 2).** The text never states δ = 0.76, η = 0.24,
   σ_s = 3.9 nm, the escape depth λ_s, σ_p = 2.25 nm or σ_b = 4.50 nm (recomputed). Every result in the chapter depends on
   them. The reader is told "a blur of a few nanometres" and "chapter 6's δ". The flat yield is Y = δ + η = 1.00, so
   m = 0.50 on the floor, and the student needs that to check SNR = 1.9. The dimensionless numbers that decide the regime are
   also missing. The blur is σ_b/space = 0.23 of the 20 nm space. The sampling is σ_b/Δx = 4.5 pixels per blur width. The
   aspect ratio is h/space = 1.5, which matters for shadowing (item 8). The excess is spread over only w = h tan β = 1.05 nm,
   which is barely one pixel. The bottom width CD + h tan β = 21.05 nm appears in 7.4 without that formula. The formula
   only appears in the checks table (C7).

5. **The chapter overstates the Monte Carlo agreement (STANDARD 5).** 7.5: "at five settings they agree within 10 % (check
   C6), the Monte Carlo being slightly larger, as the curvature of the profile near the threshold makes it." Measured with
   the module:

   | setting | propagation (nm) | MC (nm) | MC/prop |
   |---|---|---|---|
   | default | 0.2714 | 0.2850 | 1.05 |
   | Example 7.3, 15 nm probe | 1.886 | 1.678 | **0.89** |
   | β = 15° (slider max) | 0.474 | 0.403 | **0.85** |
   | h = 1 nm | 4.645 | 3.972 | **0.86** |
   | Δx = 0.5 nm | 0.308 | 0.262 | **0.85** |
   | pitch 400 nm | 0.264 | 0.247 | 0.94 |

   The chapter's own Example 7.3 is outside 10 %, and the sign is opposite to the one claimed. The sentence must say that
   the 10 % holds at the five checked settings, give the MC's own 2 % uncertainty (now only in the table), and drop the
   curvature explanation, which nothing on the page supports. The more likely non-linearity is that the noisy profile's
   maximum, and which pixel holds it, jumps. The finite-difference derivative at the noise-free profile cannot see that.
   The MC is also not an independent check of (7.3): it draws *Gaussian* noise with the variance of (7.3). It tests the
   linearisation of the rule, not the noise model. The text says this only in the limits list ("The Gaussian approximation
   of the noise in the Monte Carlo"). It should be said where the MC is introduced.

6. **The Key result's dose claim is wrong for N, and the module shows the scaling law fails across pixel size.** "Halving
   it needs four times the electrons: four times the scan time or the current, and four times the dose on the wafer." Dose
   is D = I_p t_d/Δx² (C8). It does not depend on N. Averaging four times as many lines along a longer line costs four
   times the time and *no* extra dose per area. Separately, σ_CD ∝ (I_p t_d N)^{-1/2} is true only at fixed pixel size,
   and pixel size is a slider. Measured at fixed n̄: Δx = 0.25 nm gives 0.255 nm, 1 nm gives 0.271, 3 nm gives 0.175 and
   5 nm gives 0.101, while the bias jumps between 28.4 and 31.7 nm. Measured at equal electrons per nanometre of profile
   (t_d ∝ Δx): 0.5 nm gives 0.435 nm, 1 nm gives 0.271, 2 nm gives 0.155 and 5 nm gives 0.045. Coarse, undersampled pixels
   give a ten times "better" width from the same electrons. The reason is that the rule uses only the few pixels at each
   crossing and at the levels, so finer pixels spread the electrons over pixels it never reads. "Precision is bought with
   electrons" needs the qualifier "in the pixels the rule reads, at a fixed pixel size". Δx against σ_b (sampling) needs one
   sentence. Nothing in the chapter mentions the pixel size beyond its default.

7. **Problem 3 and the I_p slider: the probe does not grow with current, though the label says it does.** The slider reads
   "I_p probe current asked of the column (chapter 5 sets the source-image size from it)". In this simulation d_p is an
   independent slider. Moving I_p leaves it at 5.30 nm (`app.js` builds p from the contract defaults and nothing links
   them). Measured with the probe held at 5.3 nm, σ_CD = 0.1 nm needs I_p ≈ 73 pA and 730 µC cm⁻². Recomputed with chapter 5's
   module chained in, 73 pA gives d_p = 6.21 nm and σ_CD = 0.115 nm, and 0.1 nm needs about 110 pA and about 1100 µC cm⁻².
   That is 50 % more current and dose. Example 7.3 does say "at the same current" for its blunt probe. But Problem 3 asks
   for an answer the page gives in a way that is unphysical, and the label tells the reader the opposite of what happens.
   The d_p label also leaks a variable name: "in the convention named by 'probe_convention'". There is no such control in
   this simulation, and (7.2)'s σ_p = d_p/2.355 holds only for FW50.

8. **The physical model of the edge omits the effects a metrologist expects first (STANDARD 1, 2, 7).** (a) *Secant law
   near grazing.* "on a near-vertical wall it is many times the flat value". At the default β = 2°, 1/sin β = 28.7. The
   secant law is an approximation for moderate tilt. Near grazing, the primary's interaction volume leaves the wall and the
   yield saturates. The chapter keeps only the integral (δh, finite), which is defensible, but it should say so and give the
   regime (λ_s against the primary range at 800 V). (b) *The edge effect.* Near the top corner, secondaries escape through
   two surfaces. This, together with the tilt, is the classic cause of bright edges, and it is not mentioned. (c)
   *Shadowing in the trench.* With h/space = 1.5, secondaries from the floor and from the foot of the wall are partly
   intercepted by the neighbouring line. The model takes the floor yield equal to the flat δ. (d) *Material.* What the line
   is made of is never said. The simulation caption says "chapter 6's silicon", so the model is silicon lines on a silicon
   floor. A resist line on silicon would add material contrast. (e) *Detection.* "counts" assumes an ideal counting
   detector. Real CD-SEM detectors are analogue (scintillator and photomultiplier, or in-lens), and their gain noise adds to
   (7.3). None of (b) to (e) is in "What the model leaves out".

9. **7.4 and Example 7.3: large biases with no physical picture.** "With the default blur the flanks move outwards and the
   rule reads 28.6 nm for a line whose true CD is 20 nm: a bias of 8.6 nm." The student is not told why the flank moves
   out, or by how much it should. One sentence gives the picture: each edge peak is a blurred spike at the wall, its outer
   half-height point sits about one σ_b outside the bottom corner, and here σ_b = 4.5 nm, so each edge moves out by
   (28.56 − 21.05)/2 = 3.76 nm ≈ 0.84 σ_b. The neighbouring walls' tails also raise the floor (the floor window starts only
   4.5 nm from the wall foot, i.e. 1 σ_b). Example 7.3's fin reads **24.6 nm for a 15.0 nm line**, a bias of 9.6 nm (64 %),
   and the text passes over it in silence. "A larger probe costs twice, in bias and in precision" reads to a student as "costs
   double". In fact the bias rises by 0.4 nm (28.6 to 29.0) while σ_CD rises seven-fold (0.27 to 1.89 nm), because the
   single-line SNR falls to 0.25 (measured, not stated). Say the SNR, and say "in two ways".

10. **Simulation, equation to screen (STANDARD 6, and the house rule that drawing and store differences are said on the
    page).** (a) *The section is not to scale vertically.* The code draws the height as at most 44 px whatever h is, while
    x is to scale. The default line, 30 nm high and 20 nm wide, is drawn as a flat mesa about 160 px wide and 40 px high,
    and the 2° walls look about 13° from vertical (measured, 1400 px: ww = 9.2 px over 40 px of height). At β = 15° the walls
    look about 45°. The caption says "the line in section below" and nothing about scale. (b) *The dots are not counts.*
    The "one noisy scan line" is drawn from Gaussian noise. It gives non-integer values and negative values that the drawing
    clamps to 0. At I_p = 0.1 pA a row of dots sits on the zero line. (7.3) is Poisson. (c) *Dots outside the plot.* The
    drawing clamps at 1.3 × the axis top, so noisy dots appear above the plot frame at both widths. (d) *The dashed edges
    come from the noise-free profile* (`out.CD_meas`), not from the dark "mean of N lines" curve they are drawn over. The
    caption ("the edges the threshold algorithm finds") lets the reader assume the latter. (e) *A stopped simulation
    shows stale numbers.* At h = 0 (the slider's minimum) or d_p = 50 nm, the panel prints "This simulation stopped: …".
    The canvas and all seven readouts keep the previous setting's values (`app.js` updates them only on success). At h = 0
    the message is also wrong: "the space is narrower than a few pixels or the edges are blurred into each other". In fact
    the line has no height and there is nothing to see. (f) The wine, dark and dots are not tied to symbols: the caption
    should say that wine is n̄η_cY(x) from (7.2)–(7.3), dark is S_i, and dashed is CD_m.

---

## Close behind

- **Further reading (STANDARD 8): there is no `.prefs` list at all.** The only sources are a vendor product page (which I
  could not open) and "Abramowitz and Stegun's formula 7.1.26", cited with no link (DLMF has a free equivalent). The secant
  law, the compound-Poisson noise of secondary-electron detection, threshold edge rules, model-based CD metrology and
  reference metrology all have standard sources. Candidates the author should open and read before citing (I did not open
  them for this review): L. Reimer, *Scanning Electron Microscopy*, 2nd ed., Springer 1998 (chapters on SE yield against
  tilt and on noise); J. S. Villarrubia, A. E. Vladár, M. T. Postek, "Scanning electron microscope dimensional metrology
  using a model-based library", *Surf. Interface Anal.* 37 (2005) 951; Postek and Vladár's chapter on CD-SEM metrology in the
  *Handbook of Silicon Semiconductor Metrology*. For the claim that the beam's own electrons are Poisson, see Kiesel, Renz
  and Hasselbach, *Nature* 418 (2002) 392, which shows that free-electron antibunching is tiny at these degeneracies.
- **7.3 "where the graininess of charge, a quantum fact, enters".** Discreteness of charge plus independent emission gives
  Poisson statistics classically. Calling it "a quantum fact" invites the graduate's objection that quantum statistics would
  make field-emitted electrons slightly *sub*-Poissonian (antibunched). Better: electrons leave the tip independently, so
  their arrivals are Poisson, and the degeneracy of the beam is far too small for quantum statistics to matter.
- **7.3, the step to (7.3) is skipped.** "by the law of total variance (check C1)". A school student does not know that law.
  Two lines would do it, and they belong in the text: Var N = E[n]·Var k + Var n·(E k)² = n̄·m + n̄·m². The thinning step is
  also unstated: Poisson(Y) secondaries, each collected with probability η_c, give Poisson(η_cY). Y includes η, and a
  backscattered electron is 0 or 1 per primary, which is Bernoulli rather than Poisson. Say that it is lumped in.
- **7.3 Example 7.1, "which collects 3200 electrons per position across".** 6.24 × 512 = 3196 is the number of *beam*
  electrons. The number *collected* is that times m, about 1600 on the floor and about 4700 at the peak. "collects" mixes up
  the two.
- **7.3 Example 7.1, "the order of the dose that exposes an electron-beam resist, which is why resists shrink under a
  metrology beam".** This is a causal claim without support. The resists measured in fabs and known to shrink under CD-SEM
  beams are 193 nm (ArF) photoresists, not electron-beam resists. Give a source or soften it to "comparable to".
- **7.3, "SNR … the contrast-to-noise ratio".** The symbol says signal-to-noise, the words say contrast-to-noise, and the
  contract calls it "signal-to-noise ratio of the edge contrast". Pick one.
- **7.2, "a line of width CD at half its height h stands on the floor".** It can be read as "h is the half height". Say "a
  line of height h whose width at half height is the CD".
- **7.2, (7.2) is undefined for a vertical wall** (w = 0 in the denominator), yet Example 7.3 uses vertical walls. The module
  switches to a Gaussian line source. One clause in the text would cover it ("for w → 0 the bracket over w becomes the
  Gaussian density").
- **7.2, symbols used before or without definition:** δ is "chapter 6's δ" and never called the secondary-electron yield in
  words. η is never called the backscatter coefficient. FW50 is not expanded. a < b is not stated. Y is the *total* yield (secondaries plus backscattered), which matters for m = η_cY in 7.3.
- **7.5, symbols undefined:** S_i (the averaged count in pixel i) and n (the number of pixels per period, 40 at the default)
  are never defined. The step "Every term in (7.4) scales as 1/(n̄N)" skips the reason, which is one line: the profile scales
  as n̄, so ∂f/∂S_i scales as 1/n̄ and its square as 1/n̄², while Var N_i/N scales as n̄/N.
- **7.5, heading "How precise is a width?"** This is a question-form heading. CLAUDE.md says "No question-and-answer format
  anywhere", and the 21 October verdict says "no rhetorical questions". Use, for example, "The precision of a width".
- **7.5, "steep edges give precise widths".** This is right, but "steep" here means a steep *profile* S′, not a steep wall.
  For the student who has just read about steep walls, the word is ambiguous.
- **7.6, (7.6) introduces N without saying it is 512 pixels per line and that the image is square** (the slider label
  says so, the text does not). Ṅ_m is a fourth use of N.
- **7.7, the checks table prints raw SymPy:** "R₅₀ = [-sqrt(2)*sigma*sqrt(log(2)), sqrt(2)*sigma*sqrt(log(2))]",
  "m\*n\*(m + 1)", "sigma_p = d_p/2.355". This is code in a lecture note. It also defines Δx (C8), which the body text never
  introduces.
- **7.7, limits.** The list is good, but it lacks items (b)–(e) of the eighth serious place above, the I_p–d_p coupling, and pixel
  sampling. "the next, more complete model" is named only as "a three-dimensional simulation". Name one (for example a
  Monte Carlo of the line in the style of chapter 6, or NIST's JMONSEL), with a source.
- **Figure 7.1.** The θ arc starts *at* the top corner of the block (`M470 60 A …`), so it marks no angle between two
  lines, and θ cannot be read off the drawing. θ should be drawn between the wall and the horizontal. Labels overrun the
  outlines: "escape laye|r" crosses the right edge of the left block, and "more S|E" crosses the right edge of the right
  block. At 390 px the labels are 8.5 px high (measured: 16 px in a 640-unit viewBox drawn 340 px wide), too small to read.
  The wall is drawn at 45° and called "steep", while the chapter's line has 2° walls. A second sketch (or a sentence) for
  the near-vertical case, where the beam runs down the wall's escape layer for the full height h, would give the physical
  picture behind "adds as much signal as a flat strip of width h". That is the most striking result of 7.2.
- **Phone layout of the simulation.** The module asks for `aspectPhone: '4 / 5'`, but at 390 px the canvas measures
  334 × 209 px (16:10). At I_p = 0.1 pA the tick label "0.059" runs into the rotated axis title "counts per pixel".
- **The 30 kV remark in 7.2** ("at 30 kV this model would wash the edges out") is right, but it gives no number. One clause
  with chapter 6's σ_s at 30 kV would support it.
- **Everyday picture (STANDARD 1).** 7.1 begins with a fab tool, not with human experience. A grainy photograph taken in dim
  light is exactly shot noise, and it would make 7.3 click for the school reader. The reason edges glow (more surface near
  the beam) can be felt with a torch skimming a wall. These would be one sentence each, not new sections.

---

## Verdict per section (against `notes/STANDARD.md` §4 and the 21 October verdict)

| section | verdict | what decides it |
|---|---|---|
| Lead | clear, leave it | — |
| 7.1 Reading a width from an image | **needs work** | Figure 7.1: θ is not marked, labels overrun the outlines, 8.5 px labels at 390 px. λ_s has no value. The secant law near grazing has no regime stated. No everyday picture (1, 2, 6). |
| 7.2 The expected profile | **needs work** | δ, η, σ_s, σ_p, σ_b, w and the bottom width have no values. b clashes with 7.4. (7.2) is undefined at β = 0. "at half its height h" is ambiguous. Shadowing, edge effect and material are not stated as assumptions (2, 3, 7). |
| 7.3 Counting electrons | **needs work** | The law-of-total-variance and thinning steps are skipped. N means counts here and lines later. "collects 3200" means beam electrons. The resist-shrink claim is unsupported. "quantum fact" (3, 8). |
| 7.4 Finding the edges | **needs work (small)** | The rule is described well. Missing: why the flank moves out by about σ_b (the 8.6 nm bias with no picture), the formula CD + h tan β in the text, and b reused (1, 3). |
| 7.5 The precision of a width | **needs work** | N, n, S_i, f are undefined or clash. "1/\|S′\|" is wrong per pixel. The MC "slightly larger … curvature" claim is contradicted at Example 7.3's own setting. Key result: dose does not scale with N, and the law fails across Δx. Example 7.3: the 64 % fin bias is uncommented, and "costs twice" is ambiguous. The heading is a question (3, 4, 5). |
| 7.6 Measurements per hour | clear apart from one symbol | N in (7.6) is undefined and is the third meaning of N. Otherwise the arithmetic and the honesty about the vendor claim are good. |
| 7.7 Checks, hand-over and limits | **needs work** | Problems 1 and 2 are wrong, and Problem 3 depends on a coupling the simulation lacks. The checks table shows raw SymPy. Limits miss shadowing, edge effect, analogue detection and pixel sampling. No reference list (5, 7, 8). |
| Simulation | **needs work** | The section is not to scale vertically. The dots are Gaussian and clamped. Dots are drawn outside the frame. The dashed edges come from the noise-free profile. A stopped simulation leaves stale numbers, with a wrong message at h = 0. The I_p label claims a coupling that does not exist. A variable name leaks into the d_p label. N = 32 gives a field narrower than one period with no warning (6). |

Against the eight items of STANDARD §4, chapter by chapter:
1 picture: partly (the fab motivation is good; no human-scale picture; Figure 7.1 is defective).
2 model: partly (the assumptions are named, the values and dimensionless numbers are missing).
3 derivation: partly (two skipped steps in 7.3 and 7.5).
4 checks: good (C1–C8, limiting case β → 0, worked numbers), but the text has no dimensional check.
5 numerical method: partly (finite differences and the MC are described; step size and MC error appear only in the table;
the 10 % agreement is over-generalised).
6 equation to screen: weak (see the tenth serious place).
7 limits: good start, important gaps.
8 reading: missing.

Files used for this review (all in the scratchpad): screenshots `w1400-*.png`, `w390-*.png`, `sim-*.png`, `montage1.png`,
`montage2.png`; scripts `shots.cjs`, `sim.cjs`, `sim2.cjs`, `meas.cjs`, `mod.cjs`; folder
`/tmp/claude-0/-home-user-SiteTest/c8b76f47-83f6-5259-bec8-4485c7f5a448/scratchpad/ch07/`.
