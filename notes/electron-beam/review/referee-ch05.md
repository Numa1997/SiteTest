# Referee report · Project 07, Chapter 5 "The spot" (`#ch05`)

Read as two people at once: a school student who is good at mathematics, and a physics graduate who designs
electron-beam columns and is reading this as a job applicant's portfolio. Only Chapter 5 and its simulation were read.

**How it was read (9 November 2026).** `python3 portfolios-src/electron-beam/build.py --site --out <scratchpad>/ch05/index.html`
built "6 of 10 chapters, 82 equations, 10 figures". `cmp` found it byte-identical to `public/portfolios/electron-beam/index.html`,
so the served file is the current build. I served `public/` locally and opened the page in headless Chromium (Playwright) at
1400 px and 390 px, also at device scale 2. Chapter 5 has no folds: its five sections (5.1 to 5.5), Figure 5.1 and the
simulation `#sim-ch05` all render open. I screenshotted each one whole, and found no console or page errors. I read the KaTeX
from the rendered `aria-label`s. I drove the simulation through its menu and sliders: the defaults, `rss`, α = 0.1 mrad and
30 mrad, 30 kV with C_s = C_c = 0.1 mm and 0.1 pA, and the worst corner (100 V, 20 mm, 10 nA, 2 eV, 10⁶). I also moved the
pointer across the canvas: it does not react, which is correct. "Recomputed" numbers are mine. They come from `ref/ch05.py`,
`ref/ch02.py` and `ref/ch04.py` run on the page's own inputs, from CODATA constants, and from SciPy for the Airy integral.
I did not read `PLAN.md` or the check files.

**Primary source.** I could not open Bronsgeest et al. (2008). I tried four roads: the TU Delft repository file and record
(connection reset through the proxy); the AIP PDF (403); OpenAlex (record and abstract only); and Semantic Scholar, which
points to the same blocked AIP PDF. Where a finding below rests on that paper, it rests on arithmetic, not on the text.

Verdicts are against `notes/STANDARD.md`, section 4: (1) picture, (2) model, (3) derivation, (4) checks, (5) numerical method,
(6) equation to screen, (7) limits, (8) reading. They also apply Numa's verdict of 21 October 2026: Taylor's way, every step
shown, every symbol defined where it first appears, one symbol with one meaning.

---

## The ten most serious places

1. **5.4 and check P6: the explanation of the Bronsgeest disagreement is probably wrong, and with it the diffraction
   coefficient that sets every example.** The text says "while their own Eqs. 6 and 19 give a value larger by a factor close to
   $1/\ln2$ (check P6), as if the quoted number counted only the current inside the FW50 disc."
   - The source image equals the diffraction disc when I_AI = (π²/4) c² λ²V B, where c is the diffraction coefficient. With
     the exact λ²V = 1.5041×10⁻¹⁸ m² V, the old Barth–Kruit coefficient **c = 0.54 gives 1.082×10⁻¹⁸ B**. That is
     Bronsgeest's quoted 1.08×10⁻¹⁸ to 0.2 %. The chapter's c = 0.66 gives 1.617×10⁻¹⁸ (recomputed).
   - The ratio with the exact λ is 0.669 = (0.54/0.66)². That is not ln 2 = 0.693. The chapter reaches 0.698 ≈ ln 2 only by
     switching to the rounded constant "1.2 nm·V½".
   - The FW50 of an in-focus Airy disc is **0.535 λ/α** (I found the 50 % encircled-energy point at v = 1.680). That supports
     0.54, not 0.66.
   - So either Bronsgeest's Eq. 19 really reads 0.66 and has a reason the chapter does not give, or (5.3) carries the wrong
     coefficient. In every default example diffraction is the largest or co-largest term. A 22 % error there moves d_p by
     roughly 10 to 20 %.
   - A column designer will know 0.54 by heart and will stop at (5.3).

2. **5.1: chapter 4's hand-over is dropped, and the column it implies is never named.** The text says "For a given current, a
   wider cone needs a smaller source image, which the condenser lenses provide by demagnifying the source more."
   - Chapter 4 hands over the magnification M = 0.0180. Chapter 2's cold source has d_v = 1.30 nm (both recomputed).
   - Example 5.1's d_I = 0.812 nm therefore means a total magnification of **0.63**. The condensers would have to *magnify*
     the source about 35 times relative to the objective alone.
   - With chapter 4's M alone, d_I = 0.023 nm and the current at 5 mrad is about 8 fA, not 10 pA.
   - The chapter makes I_p a free knob and never says what the column must do to deliver it. The chain from chapter to
     chapter, which is the point of the portfolio, breaks here.

3. **5.5, check P1: two wrong coefficients, marked "pass".** The table says "with A = 1.22λ, B = C_s/2: α_opt ≈
   1.0(λ/C_s)^(1/4), d_min ≈ 0.93 λ^(3/4) C_s^(1/4)".
   - The correct values are **1.09** and **1.29** (recomputed).
   - Check: 1.09 × (λ/C_s)^¼ at 800 V gives 10.99 mrad, the P4 value. 1.29 λ^¾ C_s^¼ gives 5.56 nm, the directly computed
     minimum; 0.93 would give 4.0 nm.
   - The string is typed by hand in `derive/ch05.py` (line 38), not computed. The "pass" belongs to the symbolic identity
     beside it.

4. **5.3, Example 5.2: two claims the page's own numbers contradict.** The text says "A thousand times the current costs a
   factor of a few in size, and at large current the source image takes over."
   - From 1 pA to 1 nA the spot grows 5.16 → 7.38 nm, a factor of **1.43**, not "a few".
   - At 1 nA the terms are d_C = 5.16 nm, d_I = 3.61 nm and d_A = 2.54 nm. Chromatic aberration still leads. The source
     image overtakes it only near 10 nA (8.61 against 6.84 nm) (recomputed).

5. **5.5, Problem 3: a false premise.** The problem says "even though the chromatic term enters both with similar weight."
   - The Schottky preset of Figure 5.1 has ΔE = 0.425 eV, twice the cold 0.215 eV. Its B_r is 1.67×10⁷ against 2.17×10⁸.
   - At 0.1 pA the Schottky spot is 7.26 nm against 5.13 nm. The source image is negligible there (0.26 nm), so the
     difference *is* the chromatic term.
   - The chapter also never states the preset's values, so a reader cannot reproduce Figure 5.1.

6. **5.3: the regime of the default column is never named, and the wrong closed form is quoted for it.**
   - The text says "it reproduces the closed form of P1 to seven digits, 10.99 mrad for the default lens". But the default
     optimum (8.13 mrad) is a **diffraction–chromatic balance**: d_A = 3.52 nm, d_C = 3.73 nm, d_S = 0.41 nm. That is the P2
     regime, and C_s barely matters at 800 V.
   - That is the design lesson of the chapter, and it is left for the reader to dig out of a table.
   - Example 5.2 then frames the better lens as "at low voltage the lens, not the source, sets the spot". At 10 pA the source
     never set it (d_I = 0.50 of 5.27 nm). What the example shows is that cutting C_c 28 times moves the balance to diffraction
     against spherical aberration, at 28 mrad.

7. **5.2: the central formula comes with no picture and from a paper not read, and it is cut off on screen.**
   - The text says "Barth and Kruit we know only from its abstract and from Bronsgeest's use of it." It never says why
     diffraction and spherical aberration combine with power 4, the source image with power 1.3, and chromatic aberration in
     quadrature, or what the coefficients 0.66, 0.18 and 0.6 are.
   - Equation (5.3) overflows its box at **1400 px** (scrollWidth 767 against 717 px; measured). The definition of d_C ends
     at "0.6 C_c Δ/e" under the equation number. At 390 px, (5.1), (5.2) and (5.3) all scroll sideways.

8. **5.4: the comparison with real lenses is put too kindly for this reader.**
   - The text says "Our bell-field objective, 4.19 and 2.85 mm at a 3 mm working distance, sits inside that range, at the
     conventional end." In the chapter's own CSV it is the second-worst of eleven rows. It is twice the C_s of the
     "uncorrected CD-SEM column" row (2 mm at 1 keV, CEOS).
   - The resulting 5.3 nm spot at 800 V is never set beside the nanometre-scale resolution that low-voltage SEMs are sold
     with. That is my general knowledge, not checked here.
   - On Joy, the text says "so his 18 nm is a choice of a larger angle for more current". That is an interpretation put into
     Joy's mouth without support.
   - Joy's 0.61 λ/α is a radius used as a diameter. The data README says so; the page does not, although (5.2) uses 1.22.

9. **5.1 to 5.3: symbols undefined in the chapter, and steps skipped.**
   - λ is never defined: at which voltage, and relativistic or not? The code uses h/√(2meV*) at the landing voltage.
   - V\*, B_r and "virtual source" are taken from earlier chapters without a one-line reminder. A and B appear in the prose
     without their values (1.22λ and C_s/2 appear only in the table).
   - "λ/α" gets no physical reason. The uncertainty picture would do it in one line: transverse momentum ≈ pα, so
     Δx ≈ h/(pα) = λ/α.
   - "C_cα ΔE/(eV\*)" gets no reason either. It comes from f ∝ V/B², so Δf/f = ΔV/V, and the miss is α Δf.
   - The derivative step is skipped: −2A²/α³ + 6B²α⁵ = 0.
   - "half as wide as the miss C_sα³ there" mixes a radius (the miss) with a diameter (the disc). The disc is a quarter of
     the Gaussian-plane blur diameter 2C_sα³.

10. **Simulation `#sim-ch05`: the drawing and its controls let the reader down.**
    - The α slider runs from 0.1 to 30 mrad, but the plot runs from 0.5 to 50 mrad. Below 0.5 mrad the **"now" marker
      vanishes** while the readout still says 303 nm (measured at 0.1 mrad).
    - The menu label is raw ASCII ("0.5 C_s alpha^3", "C_c alpha dE/E"). The ΔE slider calls its value a FWHM, but in `fw50`
      mode it is used as an FW50.
    - The y-tick "10000 nm" is clipped to "0000 nm". The legend sits on top of the curves.
    - The readouts omit d_A, d_S and d_C, which the text quotes.
    - The sliders and Figure 5.1 run to 10 nA at 800 V with no word that Coulomb interactions dominate there. Chapter 5's own
      source, as the bibliography reports it, warns of them in Schottky beams at much lower brightness.

---

## Section by section

### Chapter lead
"This chapter adds the four blurs in the classic way and in the FW50 way of Barth and Kruit". "The four blurs" and "FW50" are
used before they are defined; a school student does not yet know what either is. One clause would fix it: "the diameter
holding half the current". Otherwise the lead is a clear plan of the chapter.
**Verdict: clear apart from FW50 used undefined.**

### 5.1 Four blurs on one spot
- **Picture (1).** The burning-glass sun dot is a good everyday picture, and it carries three of the four blurs (finite sun,
  imperfect glass, waves). Chromatic aberration is not in the picture, even though light gives the example for free: the
  coloured fringe of a cheap magnifier.
- **Undefined symbols.** "cannot be focused tighter than about λ/α": λ is undefined in this chapter, and no reason is given.
  V\*, B_r and "virtual source" need one-line reminders. "B_pr = B_r/ln 2 the practical brightness" is stated with no reminder
  of why the factor is 1/ln 2 (chapter 3).
- **No reasons for the misses.** "miss by C_sα³" and "miss by C_cα ΔE/(eV\*)" do not say in which plane, nor whether the miss
  is a radius or a diameter. The chromatic miss gets no one-line reason (f ∝ V/B²).
- **Equation (5.1).** It is fine as a definition of current = brightness × area × solid angle. The text does not say that d_I
  here is the FW50 diameter. That is why B_pr appears, and it matters later for the `rss` mode.
- **The column is never shown.** "which the condenser lenses provide by demagnifying the source more": see top-10 item 2. The
  default numbers need a total magnification of 0.63 against chapter 4's 0.018. The chapter should state the source size (1.30
  nm) and the magnification that its I_p implies, and say how the column sets it.
- "the spot size is what we pay": good line.

**Verdict: needs work.** It needs λ defined, the reasons for λ/α and the chromatic miss, radius against diameter, and the link
to chapter 4's M and chapter 2's d_v.

### 5.2 How the blurs add
- "The four blurs are not independent shapes that could be laid side by side." This is vague for a student. Say that the probe
  is the source image smeared by the point blur, and that only for Gaussians do the squared widths add.
- **Equation (5.2).** "half as wide as the miss C_sα³ there (check P3 finds this factor ½ by brute force)": the radius against
  diameter confusion of top-10 item 9. "The chromatic term is the spread of focus across the energy width": a spread of focus
  is a length along the axis. The step "focal spread C_c ΔE/E, times α, gives the disc" is missing.
- "an Airy disc to its first zero holds 84 % of the current": correct (0.838, recomputed).
- **The FW50 rule (5.3).**
  - No physical picture of the root-power sum: why power 4 for diffraction with spherical aberration, why 1.3 for the source
    image, why chromatic aberration in quadrature last.
  - No source for the coefficients beyond "as Bronsgeest et al. give them". The in-focus Airy FW50 is 0.535 λ/α, so 0.66 needs
    a sentence (top-10 item 1).
  - "We read that paper in full; Barth and Kruit we know only from its abstract": honest. But for a job portfolio, building the
    central formula on an unread paper is a weakness a hiring reader will notice.
- "FW50 = 1.76 times the 25–75 % edge width": consistent with a Gaussian (1.746, recomputed).
- **The ΔE convention.** "wider by a factor 0.743⁻¹": write "1.35 times wider". "so our chromatic term is on the safe side by
  that much" is true for the cold source only. For the Schottky curve of Figure 5.1, a near-Gaussian distribution, FW50/FWHM
  falls towards 0.573, so its chromatic term is overstated by up to 1.75. The figure's comparison is affected and the text does
  not say so.
- **The `rss` mode** uses the same FW50-based d_I (from B_pr) as `fw50`, so the classic sum mixes conventions. Say so, or use
  B_r there.
- **Display.** (5.3) is cut at 1400 px (measured), see top-10 item 7.
- The Key result box is good.

**Verdict: needs work.** It needs a physical picture of the root-power sum, the source of the coefficients, a radius against
diameter fix, the Schottky ΔE caveat, and an equation that fits its box.

### 5.3 The best angle (with Examples 5.1 to 5.3 and Figure 5.1)
- **The derivative step is missing.** "setting the derivative of A²/α² + B²α⁶ to zero gives α⁸ = A²/(3B²)": one line would
  show it.
- **Symbols.** A and B are undefined in the prose. The letter A also means 1.22λ in the classic convention and 0.66λ in FW50.
- "the optimum angle grows only as the fourth root of λ/C_s, which is why a lens twice as bad costs so little in angle": the
  more useful statement is that the *spot* grows only as C_s^¼.
- **Wording.** "With the chromatic term and the current switched off": "the current switched off" will puzzle a student. Say
  "I_p → 0, so d_I = 0", and add that this check is in the classic convention.
- **Wrong regime quoted.** The P1 number "10.99 mrad for the default lens" is not the regime of the default column; see top-10
  item 6.
- **Example 5.1.** The numbers reproduce exactly (d_A 5.72, d_S 0.0943, d_C 2.29, d_I 0.812, d_p 6.48 nm; optimum 8.13 mrad,
  5.27 nm; `rss` 11.3 and 9.08 nm at 8.14 mrad). "the two conventions measure different things" is true. Most of the 1.7 comes
  from the diffraction coefficient alone (1.22 against 0.66, a factor 1.85), and saying so would be the useful sentence. The
  example should also name the balance at the optimum: d_A ≈ d_C, with d_S negligible.
- **Example 5.2.**
  - "A thousand times the current costs a factor of a few in size": the factor is 1.43. "at large current the source image
    takes over": not at 1 nA (top-10 item 4).
  - "An immersion-type objective with C_s = 0.2 mm and C_c = 0.1 mm (calculated values of Tsuno et al., 1995 …)". In the CSV,
    this row is "Combined lens with specimen immersed in the electrostatic field", read from the abstract at 1 keV. That is a
    retarding-field compound lens, a different column. Say so.
  - 1.25 nm at 27.7 mrad is recomputed. At 28 mrad, whether third-order aberration theory still holds deserves a clause.
- **Example 5.3.** "with the same lens geometry (excited for the higher voltage, chapter 4)" assumes that C_s and C_c in metres
  are unchanged when NI scales with √V\*. That is true for an unsaturated lens; state it. NI rises from 346 to about 2150
  ampere-turns (recomputed); worth a number. The 0.64 nm at 8.28 mrad is recomputed. Here the balance is diffraction against
  spherical aberration (0.556 and 0.429 nm), the P1 regime. Naming it would close the loop with the two closed forms.
- **Figure 5.1.** It is clear and in the house style, but the Schottky preset (B_r = 1.67×10⁷, ΔE = 0.425 eV) is never stated.
  The curves run to 10 nA at 800 V with no Coulomb caveat on the figure.

**Verdict: needs work.** It needs the derivative step, A and B defined, the regime of each example named, Example 5.2
corrected, and the preset stated.

### 5.4 Our lens and spot next to published values
- "run from 0.17 to 5 mm in C_s and are mostly of the order of the working distance". Seven of the eleven rows are under 1 mm,
  and none of those gives a working distance. "mostly of the order of the working distance" is Joy's rule of thumb, not what
  the table shows.
- "sits inside that range, at the conventional end": see top-10 item 8.
- "These are values read from abstracts, excerpts and a manufacturer's table, not measurements we could check": honest and
  good.
- **Joy.**
  - "at his own optimum, the smaller angle where diffraction and chromatic blur are equal, the sum is smaller": "his own
    optimum" reads as Joy's 4 to 5 mrad, while the text means 2.6 mrad. No number is given (the data README has 12.9 nm at
    2.6 mrad).
  - "so his 18 nm is a choice of a larger angle for more current": unsupported.
  - Joy's 0.61 λ/α is a radius used as a diameter, a factor of 2 against (5.2), and the page does not say so.
- **Bronsgeest.** "as if the quoted number counted only the current inside the FW50 disc": see top-10 item 1. The
  0.54-coefficient explanation fits to 0.2 % and should be tested before the ln 2 story is printed. "B" in "1.08×10⁻¹⁸ B" is
  not said to be the practical brightness or the reduced brightness.
- **Scherzer.** The paragraph is clear and correct in outline. Name the conditions (round, static, free of space charge) once.
- **No links.** No reference in the chapter is a link, and `data/ch05/objective_lens_cs_cc.csv` is a file path the reader of
  the site cannot open.

**Verdict: needs work.** It needs the comparison with the CD-SEM row, the Bronsgeest arithmetic, the Joy convention, and links.

### 5.5 Checks, hand-over and limits
- **The table.**
  - The mathematics is plain ASCII ("λ^(3/4)", "C_s", "√(2AK)"), not KaTeX, beside a KaTeX body. At 390 px the "detail"
    column is hidden behind a sideways scroll.
  - P1's detail is wrong (top-10 item 3).
  - P6 says "recorded, not a test", yet its result column says "pass". Write "recorded".
  - P3 is a good brute-force check, and the radius against diameter wording should match it.
- **Parity.** "agree to 10⁻¹⁵ in the closed formulas and to about 10⁻¹²": fine.
- **Hand-over.** "What chapters 7 and 8 receive": d_p and I_p. It should also hand over the implied total magnification (item
  2), so that later chapters cannot contradict chapter 4.
- **Limits (7).** A good list: wave optics, condenser and gun aberrations, misalignment, Coulomb, vibration, stray fields, scan
  step. Missing:
  - the overlap of the retarding field with the objective (chapter 4 names it; chapter 5's slider says "after any retarding
    field", yet the lens model has none);
  - the limit on current set by the source's angular intensity and the aperture at the gun;
  - higher-order (fifth-order) aberrations at 20 to 30 mrad.
- **Next model.** None is named for the probe: the wave-optical point-spread function convolved with the source image, which
  is what Barth–Kruit fitted.
- **Problems.**
  - 1 is fine.
  - 2 contradicts itself: "at the optimum angle … at a fixed angle".
  - 3 has a false premise (top-10 item 5).
- **Further reading (8).** There is none. The chapter has no reading list and no working link to any source.

**Verdict: needs work.** It needs the P1 fix, typeset table mathematics, the problems fixed, a reading list with links, and
the missing limits.

### S · Simulation "Probe size against beam angle" (`#sim-ch05`)
- **What works.**
  - It draws, and it reacts to every control. No console errors.
  - The pointer does not change the canvas (checked by moving across it and comparing the drawn image).
  - The readouts match `ref/ch05.py` at every setting I tried.
  - The log–log plot with the four parts and a "now" and "optimum" dot is the right picture for this chapter.
- **Defects (measured).**
  - The α slider spans 0.1 to 30 mrad, the plot 0.5 to 50 mrad. Below 0.5 mrad the "now" dot is drawn outside the plot area
    and disappears (seen at 0.1 mrad).
  - At the worst corner the tick "10000 nm" is clipped to "0000 nm"; it should switch to µm. The I_p readout shows "10000 pA"
    instead of 10.0 nA.
  - The legend overlaps the probe and diffraction curves at the default setting.
  - The plot is 406 × 304 CSS px at a 1400 px window. The chromatic line (light pink) has low contrast.
  - The golden-section search runs over 0.1 to 100 mrad and does not flag an optimum at the edge of that range.
- **Words.**
  - The convention menu's label is raw ASCII ("'rss' the classic quadrature sum of 0.5 C_s alpha^3 …").
  - The ΔE slider says "full width at half maximum", but `fw50` uses it as an FW50.
  - The I_p slider says "(chapter 5 sets the source-image size from it)" inside chapter 5.
  - B_r's unit is shown as "A m^-2 sr^-1 V^-1".
- **Equation to screen (6).**
  - The caption does not say that in `fw50` mode the drawn parts are the FW50-coefficient terms and the probe is *not* their
    sum. A reader adding the curves by eye will not get the wine line.
  - There are no readouts for d_A, d_S and d_C, which Example 5.1 quotes.
  - Nothing warns that above about 1 nA at 800 V Coulomb interactions, which the model leaves out, dominate.

**Verdict: needs work.** The physics is right; the range, labels, legend and readouts need fixing.

---

## Summary of verdicts

| Section | Verdict | Main reason |
|---|---|---|
| Lead | clear, one fix | FW50 used before it is defined |
| 5.1 | needs work | λ undefined; λ/α and the chromatic miss unexplained; chapter 4's M dropped, implied magnification 0.63 |
| 5.2 | needs work | root-power sum without picture or read source; 0.66 against 0.535 λ/α; (5.3) cut at 1400 px; Schottky ΔE caveat |
| 5.3 | needs work | derivative step; A, B undefined; regime of the default not named; Example 5.2's "factor of a few" and "source image takes over" wrong |
| 5.4 | needs work | Bronsgeest ln 2 story against the 0.54 coefficient; the lens is second-worst in its own table; Joy's interpretation unsupported |
| 5.5 | needs work | P1 coefficients 1.0 and 0.93 should be 1.09 and 1.29; P6 "pass"; Problems 2 and 3; no reading list or links |
| Simulation | needs work | "now" dot lost below 0.5 mrad; ASCII labels; legend overlap; clipped ticks; no readouts for the parts; no Coulomb warning |

Against the standard: picture (1) is good in 5.1 and absent from 5.2 on. The model (2) is stated, but its regime is not named
with the page's values. The derivation (3) skips steps. The checks (4) exist, but P1 is wrong and P6 is mislabelled. The
numerical method (5) is stated briefly, which is adequate. Equation to screen (6) is weak. Limits (7) are good, with three gaps.
Further reading (8) is missing.
