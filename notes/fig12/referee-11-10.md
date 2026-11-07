# Fig. 12 · referee of §11.10 "The 3D solver on your graphics chip ★" (with §11.9 and section 14 for context)

Read blind, as rendered, by two readers: a school student who is good at mathematics, and a physics graduate who knows
Navier–Stokes, the Poisson pressure solve and conjugate gradients, but not GPU programming. Working tree of 7 November 2026,
`public/simulations/beer-slosh.html`, served from `public/` with `node notes/fig12/serve.cjs 8797`, opened as
`?grid=4` in headless Chromium at 1280 and 390 px (360 px for one check), every fold opened. KaTeX errors: 0. Page sideways
scroll: none. plan.md and check.md were not read. No question-and-answer form anywhere in §11.10.

Measured at 390 and 360 px (math column `.eq-rows__math`, table against its `.fs-body` box):

| Element | content width | box width | what the reader sees |
|---|---|---|---|
| (G1) at 390 px | 236 px | 220 px | the equation breaks into three rows; the fraction \(J_n/\Delta t\) sits on top of the \(D\) of \(D/(n\,\Delta t)\) (the two overlap); the last word reads "batc" |
| (G1) at 360 px | 236 px | 190 px | the same, more hidden |
| Table 6 at 390 px | 330 px | 323 px | the last column is cut ("Spillec", "chip /", "process", "1.6 / 1"), and so is the caption ("against tl", "from r", "spille") |
| Table 6 at 360 px | 330 px | 293 px | the same, 37 px lost |
| (G2) | fits at 390 and 360 px | | |

What the figure does, measured (the solver menu and the caption, `?grid=4` and no parameter): the menu offers "3D · your
graphics chip", "3D · processor, 4 mm", "3D · processor, 3 mm" and "Reduced model, not a fluid simulation". Without a
parameter the page tries the chip first ("your browser offers no WebGPU, so the stout runs on the processor (half glass, slow
motion)", 0.183 s simulated per s on this machine); with `?grid=4`, 0.123 s per s.

## Verdicts against `notes/STANDARD.md`

**§11.10 The 3D solver on your graphics chip: needs work.** By the items of the standard:
1. Picture: the opening (a processor is a few strong workers, a graphics chip thousands of weak ones) is good and works for
   the school student. The picture of the one physical gain, the whole glass that "can now swirl", is never shown (item 9).
2. Model: "What is solved" states it clearly. One claim in it is too strong ("no density error to report", item 6).
3. Derivation: only (G1) and (G2). (G1) has undefined symbols, an index the reader must guess, and a lag statement that is
   wrong by up to a factor of two (item 2). (G2) is derived in one line from \(dI = -\kappa I\,d\ell\): good, but it cannot
   give the ruby edge it is said to give (item 7).
4. Checks: Table 6, the quasi-static tilt and the bump run are real measurements, with commands. Three numbers in the prose
   are wrong or unsupported (item 1); differences of 8–14 % are called agreement without comment (item 5).
5. Method: the passes are listed and the one redesign (gather instead of scatter) is explained. Missing: why the chip's
   tolerance is 100 times looser, why CG runs in one group of 256 when the point was thousands of workers, and a
   like-for-like iteration count (item 4).
6. Equation to screen: "The picture" says how the chip draws; the seam with section 14 contradicts it on the head and on what
   runs by default (item 8). The reader is never told how to choose the chip solver (the menu is not named).
7. Limits: the rest drift is reported and its cause honestly marked as not established. The SwiftShader caveat is good.
8. Sources: [26] (matsuoka-601, Codrops and the Splash and WebGPU-Ocean repositories) is listed with working links and a
   note on what was read. The closing sentence of Sources ("Sources 3–6 and 8–11 were opened…") does not mention it.

Form: the labels (G1), (G2) sit outside the note's numbering, as (N1)–(N5) did in §11.9. Inline commands are set in the
browser's generic `monospace` (computed `font-family: monospace`), not IBM Plex Mono, and look larger than the text at
1280 px; this holds for the whole note, but §11.10 adds four of them to running prose.

**§11.9 (context): unchanged from `referee-11-9.md`.** §11.10 leans on it only for "softening … (section 11.9)" and the
breaking limit; both read fine from here.

**Section 14 What the picture shows (context): clear, except at the two seams of item 8 and the symbol \(D\) (item 3).**

## Items, in order of severity

1. **Three numbers in the prose are wrong or have no source.**
   - "at 50 frames a second a batch is 20 ms, a quarter of a radian of the 3.2 Hz swing": \(2\pi \times 3.2\ \text{Hz}
     \times 0.020\ \text{s} = 0.40\) rad, not 0.25. A sixteenth of a period, if that is what is meant.
   - "a step takes about 0.3 s, a hundred times slower than real time": a 5 ms step taking 0.3 s is 60 times slower.
   - "the stout's push on the cart is a ripple of about 0.08 m/s² (section 12)": section 12 contains no 0.08 m/s² (searched
     in the rendered text and in the page source; the number occurs only in §11.10). The nearest is "Example 4.2 … agrees with
     the cart's measured ripple to 1 %", which gives no size.
   - "in the free swing's frequency within 1 % at every amplitude": at 0.5 m/s², 3.194 against 3.160 Hz is 1.08 %.

   Fix: 0.4 rad (or "a sixteenth of a swing"); "sixty times"; point to where 0.08 m/s² is actually shown, or show it; "within
   about 1 %".

2. **(G1) cannot be read without guessing, and "late by at most one batch" is not what it says.**
   - Which step is step 0? The reader must infer that \(J_0\) is the last impulse read back before the batch, that the batch's
     steps are \(1,\dots,n\), and that in step \(i\) the cart was owed \(J_{i-1}\). One sentence fixes it.
   - \(F_\ell\): the subscript is never explained. Section 10.2 uses \(m_\ell\) (ℓ for liquid), and four paragraphs later
     §11.10 itself uses \(\ell\) for the thickness of stout in (G2).
   - \(n\) in \(D/(n\,\Delta t)\): the next batch has its own length ("as many as the frame lasted"), which need not equal
     this one's. Spread over which \(n\)?
   - Is \(F_\ell\) the force held through the whole next batch, so that the next batch's \(D\) is measured against \(J_n\)?
     The reader has to work it out.
   - Lag: the impulse \(J_1\), owed at step 2, is paid partly at step \(2n\) when \(D\) is spread evenly over the next batch.
     The worst lag is nearly two batches, the mean about one. "Late by at most one batch" should read "about one batch on
     average, at most two".
   - With the cap of 16 steps, one batch is 80 ms, 1.6 rad of the swing, not "little". When does the cap bite (slow chips,
     slow motion)? The reader who sees "slow motion" in the caption wants to know whether the coupling is then worse.
   - The check "with \(n = 1\) nothing is owed and the steps are those of section 10.2" is good and should stay: it is the
     limiting case the standard asks for.
   - Phone layout: at 390 px (G1) breaks so that \(J_n/\Delta t\) overlaps the \(D\) below it and "batch" is cut (table above).

3. **One symbol, several meanings.**
   - \(D\): the owed impulse in (G1); the depth in front of the camera in section 14, the camera §11.10's "The picture"
     sends the reader to; and "depth" is the key word of that paragraph.
   - \(\ell\): subscript of \(F_\ell\) in (G1), thickness in (G2), "liquid" in \(m_\ell\) of section 10.2.
   - \(J_i\): impulse here; Jacobian and Bessel \(J_1\) in §11.9.
   - \(\kappa\): absorption here; \(\kappa_1\) in (N4) of §11.9.
   - \(n\): steps in a batch here; mode index in (54) two subsections earlier.
   - "(1)–(9)" for the passes of one step, inside a paragraph that cites equations (4)–(5) and (45), and followed by
     "(9) evaluated for the tulip". "(4) particle-to-grid" and "(9) the sums the cart needs" read as equation numbers.
   - "A" in Table 6's header is not defined in §11.10 (it is the push of Table 5).

4. **The method has three unexplained choices that a graduate will stop at.**
   - Tolerance \(10^{-5}\) on the chip against \(10^{-7}\) on the processor. The reason (single precision carries about
     \(6\times10^{-8}\) relative error, so \(10^{-7}\) is out of reach) is one clause and is not given.
   - "it needs about 70–100 iterations a step instead of about 33": the two counts are at tolerances 100 times apart, so they
     do not compare the preconditioners. Say so, or give both at the same tolerance.
   - "the conjugate gradients in one group of 256 workers": the paragraph before argued that the chip wins by using
     thousands of workers. Why is CG confined to 256? (Presumably because each iteration needs two sums over all cells and one
     group can synchronise without going back to the browser.) One sentence.
   - "a chip can add floating-point numbers that way only in an order that changes from run to run": the school student
     needs the reason, that floating-point addition is not associative, \((a+b)+c \ne a+(b+c)\) in the last digit. The
     graduate knows that adding in fixed-point integers with atomic adds is order-independent, so "only" is too strong; say
     why gathering was preferred.
   - "a run repeats exactly on one device": true of the solver for a fixed batch length, but the batch length follows the
     frame rate, and the text measures that it changes the result (65.7 against 67.4 mm). The live figure therefore does not
     repeat from run to run. Say which is meant.
   - Jargon used once and not explained, for the school student who reads ★ anyway: "prefix sum", "scattering", "masks
     dilated twice by two cells", "their images in the wall", "three layers of extrapolation into the air". "Each line below"
     introduces a run-on paragraph, not lines.

5. **Differences called agreement, without a word.**
   - Bump in open loop: the chip leans 65.7 mm and spills 13.5 g, the processor 60.7 mm and 11.9 g. That is 8 % and 13 %, at
     the same grid, while Table 6 agrees to 1 %. The batch-of-1 run gives the same 65.7 mm, so batching is not the cause.
     The obvious candidate, the whole glass against the half with a mirror plane (a crest that wanders off the plane), is not
     mentioned.
   - With the speed loop the order reverses: chip 27.7 mm, processor 29.9 mm. No comment.
   - Quasi-static tilt: chip 5.1 % off, processor 2.0 %. Section 12 says this number scatters with the wall cells (+18 % at
     5 mm, −3 % at 2.5 mm); the reader should be told the 5.1 % is within that scatter, if it is.
   - Table 6 at 1 m/s²: free-swing amplitude 5.0 against 4.4 mm (14 %); at 6 m/s², 38.9 against 36.9 mm. The text says the
     solutions "agree in the push", which hides this.
   - "the glass's accelerations agree to the hundredth, 3.58 and 7.62 against 3.58 and 7.63 m/s²": which two accelerations
     (peak forward and peak vertical? peak and rms?) is not said.

6. **"No density error to report" is too strong, and the drift's cause has an untested rival.**
   - A particle method with a pressure solve stopped at a residual of \(10^{-5}\) does change volume slightly; section 12
     itself reads 125.14 mm against 125 mm poured on the processor. Say "no density error from compressibility", and give the
     chip's level at rest.
   - "Left alone, the chip's stout is not quite still … The likely cause is single precision": the 100-times looser
     tolerance and the Jacobi preconditioner are equally likely and are not mentioned. One run at \(10^{-6}\) on the chip
     would separate them; until then the sentence should name all three.
   - The drift numbers compare different times: "up to 14 mm/s within 2 s" against "3.2 mm/s after 1 s".

7. **(G2) cannot make the ruby edge.**
   - With one \(\kappa\) for all colours, \(e^{-\kappa\ell}\) only darkens one hue; thin stout is then light black, not ruby.
     Ruby needs red to be absorbed less than green and blue, three \(\kappa\)'s (or a colour ramp). The physical picture
     (stout passes red light, so its thin edge glows red against a lamp) is the one the school student would recognise, and it
     is missing.
   - The sphere radius is not given, so "the ratio of a particle's volume to its sphere's" has no number. "The normal follows
     from the smoothed depth" skips how (differences of neighbouring depths, then a cross product).
   - "chord": for the school student, "the length of the line of sight inside the sphere".

8. **Seams with §11.8 and section 14.**
   - What runs by default: §11.8 still says "The figure therefore runs, by default, a reduced model". Section 14 says the chip
     is "the default where the browser offers WebGPU", and the page agrees (measured above). §11.10 never says it is the
     default, nor that the menu item "3D · your graphics chip" chooses it. A reader of 11.8–11.10 in order meets three answers.
   - The head: §11.10 and section 14's chip paragraph paint "the top 12 mm of the stout below the computed surface"; section
     14's last paragraph lays "a cream layer 12 mm thick … on the computed surface". So the visible surface sits 12 mm lower on
     the chip than on the processor. If so, say it once; if not, one of the two sentences is wrong.
   - Section 14 says the probes, charts and data panel read the column heights on the chip too. §11.10's pass list ends with
     "(9) the sums the cart needs" and does not list column heights, and says the picture is made "without sending its
     particles back". The reader cannot tell where the column heights come from.

9. **The one physical gain is promised, not shown.**
   - "the stout can now swirl" is the reason to compute the whole glass. Nothing in §11.10 shows the chip's stout swirling,
     although §11.9 found swirl near \(f_{11}\) in the modal model. One run at resonance (or one sentence saying it was not
     tried) is the natural check.
   - The mechanism is missing too: the half-glass solver imposes the mirror symmetry of section 3.4, so it cannot leave the
     plane; the whole glass can, and its seed is round-off. One clause each.

10. **Loose ends.**
    - "Every number in this subsection was computed there [SwiftShader]": the processor columns of Table 6 were not. And the
        reader's chip may round differently from SwiftShader (fused multiply-adds), so "they are the solver's numbers" should
        say "on SwiftShader".
    - "about 0.3 s simulated per s on four cores": measured here, 0.18 (default fallback) and 0.12 (`?grid=4`) s per s. Give
        the machine or say "depends on the processor"; the caption measures it anyway.
    - Speed: the reader would like one sentence on what a real chip does (or that it was not measured), since the section
        is named for it.

Screenshots and scripts (not part of the repository):
`/tmp/claude-0/-home-user-SiteTest/6f129354-04b4-5b64-8b76-38fa05cdb63e/scratchpad/s1110/` (`s1110-1280-*.png`,
`s1110-390-*.png`, `g1-390.png`, `g1-360.png`, `tab6-390.png`, `tab6-360.png`, `fig-1280.png`); rendered text of §11.10 in
`/tmp/claude-0/-home-user-SiteTest/6f129354-04b4-5b64-8b76-38fa05cdb63e/scratchpad/t1110.txt`.
