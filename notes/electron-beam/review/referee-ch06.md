# Referee report · Project 07, Chapter 6 "Scan and hit" (`#ch06`)

I read this as two people at once: a school student who is good at mathematics, and a physics graduate. I read only Chapter 6
and its simulation (`physics/ch06.js`). I did not read `PLAN.md` or any check file.

**How it was read (9 November 2026).** `python3 portfolios-src/electron-beam/build.py --site --out <scratchpad>/ch06/index.html`
built "7 of 10 chapters, 90 equations, 12 figures, 649 numbers". `cmp` found it byte-identical to
`public/portfolios/electron-beam/index.html`, so the served file is the current build.

- **Rendering.** I served `public/` locally and opened `#ch06` in headless Chromium (Playwright) at 1400 px and 390 px. The
  chapter has no folds: sections 6.1 to 6.7, Figures 6.1 and 6.2, the stopping-power table, the checks table and `#sim-ch06`
  all render open. I screenshotted each one, and found no console or page errors. I read the KaTeX from the rendered
  `aria-label`s.
- **The simulation.** I drove it through its menu and slider: Si and Au at the default, 100 V, 30 kV, and slider steps 364, 365
  and 366. I moved the pointer across the canvas: nothing changes, which is correct. I timed the updates.
- **Recomputed numbers.** Numbers marked "recomputed" are mine. I got them by calling the page's own module (`physics/ch06.js`)
  in Node, with CODATA constants. The universal-law values come from the constants in `data/ch06/se_yield_lin_joy2005.csv`.

Verdicts are against `notes/STANDARD.md`, section 4: (1) picture, (2) model, (3) derivation, (4) checks, (5) numerical method,
(6) equation to screen, (7) limits, (8) reading. They also apply Numa's verdict of 21 October 2026: Taylor's way, every step
shown, every symbol defined where it first appears, one symbol with one meaning.

---

## The twelve most serious places

1. **Example 6.1: the sum δ + η reads as gold's.** The text says "Gold at the same voltage gives η = 0.65 and δ = 1.5 (the η too
   high, as above). Together δ + η = 1.0: about as many electrons leave as arrive."
   - "Together" follows the gold sentence, but gold gives 0.65 + 1.49 = **2.14**. The 1.0 is silicon's: 0.243 + 0.762 = 1.005
     (recomputed).
   - A student adds the two numbers just above, gets 2.15, and is lost.
   - "So at this voltage even an insulating surface would charge little" does not follow. An insulator has its own δ and η, not
     silicon's. The sentence is true only for a material with silicon's yields.
   - The one line that explains charging is missing: the net current into the sample is I(1 − δ − η).
   - The text also never says that 800 V *is* this model's second crossover for silicon. δ + η is 1.116 at 500 V, 1.005 at
     800 V and 0.953 at 900 V (recomputed). That coincidence is probably why the default was chosen, and Problem 3 asks for it.

2. **6.3: the reason for the continuous energy loss fails at the default.** The text says "A single loss is usually tens of
   electronvolts, small against keV, and there are many of them per mean free path."
   - In silicon at 800 eV, (6.5) gives |dE/ds| = 21.2 eV/nm. One elastic mean free path is 1.02 nm, so the loss per path is
     **21.6 eV** (recomputed).
   - The free-electron plasmon of silicon is 16.6 eV (recomputed, 4 valence electrons per atom). So there is about one loss per
     mean free path, not "many".
   - The sentence holds at 30 kV (57 eV per 35 nm path), not at the chapter's default.
   - The approximation also needs its name, the continuous-slowing-down approximation (CSDA). Its cost, no energy straggling,
     belongs in the limits.

3. **6.2 and 6.5: the success for silicon and aluminium is partly built in, and the text does not say so.**
   - 6.2 says the screening parameter a is "fitted so that simulated backscattering agrees with experiment".
   - 6.5 then presents the agreement of η with measurements for Si and Al as a test passed: "So the model is honest for silicon
     and aluminium". In the same way, ε and λ_s were fitted by Lin and Joy to measured δ curves, so the 800 eV agreement of δ
     with the universal law is also partly by construction.
   - The graduate also wants the validity number of the screened-Rutherford (first Born) form, Zα/β ≪ 1 (Z the atomic number,
     α the fine-structure constant, β = v/c). It is **1.83 for silicon at 800 eV** and **10.3 for gold** (recomputed). Both are
     outside the regime, silicon included. That one number would explain why gold fails and why silicon only works because of
     the fit.

4. **6.5 and Figure 6.1: the trend for gold has the wrong sign, and the text describes it only as "too generous".**
   - The figure shows measured η for gold rising with energy, from about 0.34 (0.4–2 keV) to 0.49 (8–31 keV). The simulation
     falls, from 0.645 to 0.564 (check M9).
   - A model that gets the slope wrong is not just "too generous".
   - The cause is stated as fact ("That is the failure Joy predicts … the Mott cross-section differs from Rutherford's") with no
     source and no number.
   - The text also does not mention that low-energy η is very sensitive to the surface (contamination, oxide). The database
     spread for gold at 0.4–2 keV is 0.245 to 0.419, a factor 1.7, so part of the gap may sit in the data.

5. **6.5, the secondary yield: the comparison chosen is the one that makes the gap look like the other side's problem.**
   - The text says "At higher energy ours is smaller: at 20 keV 0.054 against their 0.080 for silicon, and 0.18 against 0.37 for
     gold … the difference must lie in parts of their simulation the paper does not give."
   - Lin and Joy's *own universal law*, the fit to measurements, gives 0.090 for Si and **0.138 for Au** at 20 keV (from the
     CSV's constants). Their printed Monte Carlo for gold, 0.37, is 2.7 times their own law. Against the law, our gold value
     0.175 is 27 % *high*, not low.
   - "Must lie" is unsupported.
   - The text also does not say that gold at 800 eV gives δ = 1.49 against the law's **1.16** (recomputed from δ_max = 1.28,
     E_max = 0.5 keV), 28 % high. Example 6.1 flags only η for gold.
   - The universal law itself (the formula with 1.28, 0.67 and 1.614) and the values of δ_max and E_max are never written, so
     neither reader can reproduce the dashed curves or the "0.76" it is said to agree with.

6. **6.6 and the hand-over: σ_s is one rms number for a two-part signal.**
   - The text says σ_s "is what blurs an edge in the image beyond the size of the probe." Example 6.2 then says, rightly, that at
     30 kV "the sharp secondaries made by the incoming beam are still there … but they ride on a broad halo."
   - An rms is set by the halo. At 30 kV, σ_s = 1.4 µm does not describe how an edge blurs: the sharp part is still about the
     probe size.
   - Handing chapter 7 a single σ_s as if it were a blur width is wrong for any voltage where the halo carries much of the
     signal.
   - The simulation already separates the secondaries made on the way in from those made by electrons leaving. It should report
     the fractions, or the profile.
   - It is also never said how σ_s combines with the probe size (quadrature?), nor what that size is. "the same order as the
     probe of chapter 5" has no number.

7. **Gold at 800 eV: the free path is shorter than the distance between atoms.**
   - λ_el(Au, 0.8 keV) = **0.091 nm**. The atomic spacing n^(−1/3) is 0.257 nm. The same holds for silicon at the slider's
     100 V: 0.15 nm against 0.27 nm (recomputed).
   - A random free path shorter than the gap between atoms means the picture of independent collisions on scattered atoms has
     broken down. This is the plainest physical reason why Example 6.3 cannot be trusted, and the text never states it.
   - The simulation panel's slider also runs down to **100 V** (measured) with no warning. Joy says his model is unsuitable below
     1 keV, and at 100 V the 50 eV cut-off removes half the energy.

8. **6.4 and the panel: uncertainties are promised but not shown.**
   - 6.4 says of u_η and u_δ: "Both are readouts of the simulation, and the text quotes them." The panel's readouts are η, δ, R,
     r_90 and σ_s. u_η and u_δ are not among them (`ui.readouts` in `ch06.js`).
   - The caption says "their statistical uncertainty is stated in the text". The text gives it only for the default.
   - 6.7 promises chapter 7 the three numbers "with their statistical errors". σ_s has no error estimate anywhere. With 8000
     electrons instead of 2000 it moves from 3.94 to 4.00 nm (recomputed), so about 2 %.

9. **6.7, the checks table marks discrepancies "pass".**
   - **M10** records δ against Lin and Joy at 20 keV: Si 0.054 against 0.08, Al 0.099 against 0.19, Cu 0.113 against 0.24, Au
     0.175 against 0.37, all off by a factor 1.5 to 2.1. The verdict is "pass".
   - **M9** passes because its criterion only looks above 8 keV. At low energy gold is off by 88 %.
   - **M8** passes because the two values (105 nm and 8.9 nm) lie "on either side" of Joy's "a few hundred ångström". That
     tests nothing.
   - A reader takes "pass" to mean "agrees". Use "recorded" for comparisons that are only recorded.

10. **6.2: no derivation of the cross-section the whole chapter rests on.** STANDARD 3 asks for the derivation from first
    principles. The chapter gives (6.1) as "Rutherford's calculation of this two-body problem gives …". Four places need it:
    - **Rutherford itself (★).** The impact parameter b and the angle are related by tan(φ/2) = Ze²/(4πε₀ p v b), and
      dσ = b db dψ.
    - **The screened form.** The Wentzel potential e^(−r/r_s)/r in the Born approximation gives exactly (1 − cos φ + 2a)^(−2),
      with a = (ħ/2p r_s)². That is the physical meaning of a, which the text only calls "fitted".
    - **The step to (6.3).** The integral ∫dΩ/(1 − cos φ + 2a)² = π/(a(1 + a)) is one line: 2π∫dμ/(1 − μ + 2a)² from −1 to 1.
      It is left to "check M1".
    - **The step to (6.6).** The cumulative fraction (1 + a)x/(x + 2a), with x = 1 − cos φ, set equal to R₂ gives (6.6).
      6.4 says only "solving gives Joy's Eq. 6 (check M1)".

    A student cannot rebuild any of these from the page.

11. **6.3: Bethe's formula is presented, not derived, and two numbers come from nowhere.**
    - **78 500 is 2π(e²/4πε₀)²N_A** = 78 457 keV² cm² mol⁻¹ (recomputed). The text derives the analogous constant 5.21×10⁻²¹ in
      6.2 but not this one.
    - **1.166 is √(e/2)** = 1.1658. It is never named.
    - **The 1/E step is skipped.** The picture ("takes up momentum, the more the slower the charge passes, hence the 1/E") jumps
      from momentum to energy. The missing link: Δp ∝ 1/(b v), and the energy given is Δp²/2m ∝ 1/v² ∝ 1/E.
    - **ρZ/A is not explained.** N_A ρ Z/A is the number of atomic electrons per volume, the targets of the pulse.
    - **The table units are not converted.** The table is in MeV cm² g⁻¹ but (6.5) is in keV/cm. The student is not told to
      divide by ρ.

12. **Rendering: Eq. (6.3) does not fit.**
    - **At 1400 px** the display is 773 px wide in a 717 px box (measured). The final exponent "²" of ((E + 511)/(E + 1024)) is
      clipped and sits against the number "(6.3)".
    - **At 390 px** the box is 315 px wide and the formula 707 px. More than half, including the whole numerical form, is hidden
      behind a horizontal scroll with no visible cue.
    - **The figures at 390 px.** The SVGs (viewBox 640 wide) scale to 358 px. Their 16-unit Plex Mono labels become about 9 px,
      and the Fig. 6.1 legend and tick labels are hard to read.

---

## Section by section

### Chapter lead
Clear. It says what the chapter does and against what it is compared.

### 6.1 Into the wafer
- **"such a hit turns it without taking away more than about one part in 10 000 of its energy".** A skipped step. The largest
  fraction a head-on hit gives a heavy nucleus is 4m/M = 7.8×10⁻⁵ (recomputed with M/m = 51 200). One line would show it.
- **The same number answers a promise.** Chapter 0's screenshot, seen while loading the page, says an electron "mostly does not
  [knock atoms out] (chapter 6)". The largest energy given to a silicon nucleus at 800 eV is **0.063 eV** (recomputed), far
  below the roughly 10–20 eV needed to displace an atom. Chapter 6 never states this, so chapter 0's forward reference goes
  unanswered.
- **The marble picture has only one kind of collision** ("heavier balls"). The energy loss, to electrons of the *same* mass, has
  no picture here.
- **"those born within a few nanometres of the surface can escape".** Fine. Later λ_s is 0.5 nm for gold, so "a few" covers a
  factor of five.

**Verdict: needs small work.** The picture is good and the terms are defined in place. Add the 4m/M line, the displacement
number and the electron-electron half of the picture.

### 6.2 Turning: the screened Rutherford cross-section
- **"gives the probability of a turn into the solid angle dΩ as an effective target area".** The student gets lost here. Say
  what the area is: the area the electron must aim at, per atom, to be turned into dΩ.
- **"which in the non-relativistic case, pv = 2E".** Skipped step: pv = mv² = 2E. Also show that (1 − cos φ)² = 4 sin⁴(φ/2),
  which turns (6.1) into the textbook form with 16E².
- **"writes the screening as a shift of the denominator … fitted so that".** No physical meaning is given for a (see place 10).
  Bishop (1976) and Berger–Seltzer are cited in the text but are missing from the sources, and were not read.
- **Units.** (6.2) writes E/keV, but (6.3) then says "with E in keV". Use one convention.
- **"Integrating over all directions (check M1)".** The one-line integral is missing (place 10).
- **"Rutherford's formula treats the electron as a classical particle in a point-charge field and ignores its spin."**
  Misleading for the graduate. The Rutherford form is also the exact non-relativistic quantum result for a pure Coulomb field.
  What fails at low E and high Z is the Born treatment of the screened field (Zα/β not small) together with spin. Give Zα/β with
  the page's values (place 3).
- **"For light elements and energies of several keV that is adequate".** No support. At 2 keV, Zα/β for silicon is still 1.16.
- **Symbols.** n = N_Aρ/A is defined and then not used.

**Verdict: needs work** (derivation and model validity).

### 6.3 Slowing down: the stopping power
- **"there are many of them per mean free path".** Wrong at the default (place 2).
- **(6.5).** The origins of 78 500 and 1.166 are missing, the 1/E step is skipped, and ρZ/A is unexplained (place 11).
- **"by their measurements, fits stopping powers down to about 50 eV" against "neither number is a measurement".** These read as
  contradictory. Joy–Luo is a fit *to* measurements, so the 1 keV gold ratio of 2.31 against ESTAR says something about ESTAR's
  validity too. Say which you believe.
- **The table.** It has no number, title or caption. Its units do not match (6.5) (place 11). Gold's ESTAR value *rises* from
  12.2 at 1 keV to 17.1 at 2 keV, which surprises a student. One clause is needed: Bethe's logarithm goes to zero as E
  approaches J.
- **"the true stopping power goes as 1/β², not as 1/E".** Fine for the graduate. A student needs one clause: 1/E = 2/(mv²)
  non-relativistically, and the 1/v² survives relativistically.

**Verdict: needs work.**

### 6.4 The Monte Carlo loop
- **"the law of a constant hazard".** Jargon. One sentence would do: the chance of a hit in the next ds is ds/λ_el whatever
  happened before, so P(no hit over s) = e^(−s/λ_el).
- **"the same trick applied to the angular distribution … solving gives Joy's Eq. 6".** The cumulative function is not written
  (place 10).
- **"The unit vector of motion is turned by φ and ψ about itself."** A student is lost: a vector turned about itself does not
  move. Say instead that it is tilted by φ from its old direction, in the azimuth ψ around that direction.
- **"two unit vectors ê₁,₂ perpendicular to c, built from c".** Symbols used without definition. The code uses
  ê₁ = (c_x c_z, c_y c_z, −(1 − c_z²))/√(1 − c_z²) and ê₂ = (−c_y, c_x, 0)/√(1 − c_z²). It also has a separate branch for
  |c_z| > 0.99999, which every electron takes on its first turn. Neither is stated.
- **"(parity check: about 10⁻⁹ …)".** About 10⁻⁹ of what? A relative difference in r_90 and V_int, according to the module.
- **STANDARD 5 is only half met.**
  - The step is event-driven (the free path), which is good. But the energy update uses |dE/ds| at the *start* of each step, a
    first-order (Euler) step in energy, and the text never says so.
  - The error of that step, and the effect of the 50 eV cut-off, are not estimated.
  - The binning of r_90 (4000 bins to 3R) is not mentioned.
  - The page reuses the same random streams at every voltage. The Monte Carlo lines in Figures 6.1 and 6.2 therefore look
    smoother than ±0.01 would allow. Say so, or the reader trusts the smoothness.
  - Measured on the page: from 2000 to 8000 electrons, η at the default moves 0.2435 → 0.2514, inside ±0.0096. r_90 moves 0.5 %
    and σ_s 1.5 % (recomputed).
- **"Both are readouts of the simulation".** False for the panel (place 8).
- **The symbol R.** In the Key result box, R is a random number. On the panel, "R" is the Kanaya–Okayama range, which the text
  calls R_KO. One symbol has two meanings.

**Verdict: needs work** (method error, two definitions, one false sentence). The structure of the loop is clear and good.

### 6.5 What comes back: η and δ
- **Backscattering paragraph.** See places 3 and 4.
  - "the agreement is within the spread of the measurements at all energies" is true per band (M9), but the band means hide the
    0.4 keV ends.
  - `data/ch06/README.md gives its provenance` is a repository path the web reader cannot open, and the Akbari data DOI is not
    a link.
- **Figure 6.1.** The circles take the colour of their element, but the legend says only "circles: measurements". The Al label
  is covered by circles at the right edge. Al (grey) and Au (near-black) are close in tone.
- **Secondary-electron paragraph.**
  - **The escape law ½e^(−z/λ_s).** "half of them start towards the surface, and on the way they are absorbed with the escape
    depth λ_s" pictures straight-down escape. Electrons leaving at an angle travel z/cos θ. Say that λ_s is an effective depth
    that absorbs angle and surface barrier.
  - **ε.** ε = 90 eV per secondary in silicon will puzzle a student who knows that a silicon electron–hole pair costs about
    3.6 eV. One sentence should say that ε is an effective constant, fitted.
  - **"exactly for each straight piece (check M5)".** The integral sλ_s/Δz (e^(−z_A/λ_s) − e^(−z_B/λ_s)) is one line and is not
    shown.
- **Figure 6.2 paragraph.** See place 5. The universal law is unwritten, δ_max and E_max are not given, the comparison with the
  law at 20 keV is omitted, and "must lie" is unsupported. At 2 keV, our gold value (1.049) is *larger* than Lin and Joy's
  (0.94), so "at higher energy ours is smaller" holds only at 20 keV.
- **Example 6.1.** See place 1.

**Verdict: needs work.** This is the section most likely to mislead the graduate.

### 6.6 How far the electrons go
- **"we use the formula as Goldstein et al. quote it, not the original".** The sources say Goldstein was read as "abstract only".
  So (6.7) rests on two sources, neither opened. That breaks STANDARD 8. The numbers check: R_KO for Si at 0.8 keV is 21.9 nm,
  and for Au 3.97 nm (recomputed).
- **"The power 1.67 is the integral of the stopping power".** Garbled. Write instead: the exponent comes from integrating
  ds = dE/|dE/ds|. Problem 2 contains the right statement.
- **The range is not compared with the model's own path.** Joy–Luo's continuous path length is 25.5 nm in Si at 800 eV against
  R_KO = 21.9 nm, but **11.0 nm in Au against 3.97 nm** (recomputed). The two models of range disagree by a factor 2.8 for gold.
  The panel draws R_KO as the dashed arc over paths from a different stopping law, with no comment.
- **"That is the whole case for low-voltage metrology in one line."** A headline-style hook, which the voice rule forbids. It is
  also an overclaim.
- **V_int = ⅔πr_90³.** It is defined, but the real volume in silicon at 30 kV is pear-shaped, not hemispherical. The
  "9 × 10⁷ times larger" in Example 6.2 is a ratio of hemispheres. That is true by definition and weak as physics.
- **σ_s and "what blurs an edge".** See place 6.
- **Example 6.2.** "the beam deposits its energy deep in the device … the damage": damage is never defined in the chapter (resist
  exposure? trapped charge in oxide?). "the same order as the probe of chapter 5" needs the number.
- **Example 6.3.** Correct as far as it goes. The free-path argument of place 7 is the missing physical reason.

**Verdict: needs work.**

### 6.7 Checks, hand-over and limits
- **The checks table.** See place 9.
  - The detail column prints raw SymPy (`total pi*K/(a*(a + 1))`, `[-lambda*log(R)]`, `λ_el(100 keV)`) and plain-text maths
    (`e^(−s/λ)/λ`) on a page that typesets everything else in KaTeX.
  - **K in M1 is never defined.**
  - The checks are cited as M1 to M10 from 6.2 onwards, but the table sits at the end. That is acceptable, but each first
    citation would help with a link.
- **"What chapter 7 receives."** "with their statistical errors": σ_s has none (place 8). The probe is treated as a point at
  normal incidence, and that assumption should be handed over too.
- **"What the model leaves out."** A good list. Three things to add:
  - The CSDA itself (place 2).
  - The free-path-below-atom-spacing breakdown (place 7).
  - The point, normal-incidence probe.

  STANDARD 7 also asks for "the next, more complete model". Mott is named, but no source for it is given (for example the
  ELSEPA code and its paper). The same holds for a dielectric-function model of the discrete losses.
- **Problems.**
  - Problem 1 says "show that half of the elastic turns are smaller than the angle with 1 − cos φ = 2a". From (6.6) with
    R₂ = ½, the exact median is 1 − cos φ = **2a/(1 + 2a)**. As set, the student is asked to prove something slightly false.
    Write "≈", or ask for the exact form.
  - Problems 2 and 3 are good. The slider reaches 0.5 to 5 kV.
- **Sources.** STANDARD 8 asks for a working link to each source. Only the two Scanning Microscopy papers are linked. The DOIs of
  Lin and Joy and of Akbari (paper and data), and NIST ESTAR, are plain text. Goldstein is "abstract only", and Kanaya–Okayama
  was "not opened".

**Verdict: needs work.**

### Simulation · Electrons in the wafer
Measured in Chromium.
- **What works.** The canvas does not react to the pointer. There are no console errors. Si and Au at the default reproduce the
  text (η 0.243, δ 0.762, R 21.9 nm, r_90 14.4 nm, σ_s 3.94 nm).
- **The default is not on the slider grid.** The text's 800 V shows only at load. Slider steps 364, 365 and 366 give 0.797,
  0.802 and 0.807 kV. Once the reader touches the slider, the text's numbers cannot be found again (δ becomes 0.761, R 22.0 nm,
  r_90 14.5 nm).
- **The range runs from 0.100 to 30.0 kV.** Nothing on the panel says the model is outside its stated validity below 1 keV, and
  meaningless near 100 V (place 7).
- **At 30 kV the readouts show "9310 nm", "6550 nm" and "1410 nm"**, while the text says 9.3 µm, 6.5 µm and 1.4 µm.
- **Updates are slow.** One update takes about 0.15 s at 0.8 kV in Si and 0.5 to 0.7 s at 30 kV (Si and Au). A run of 20 slider
  input events from about 2.6 to 30 kV took 4.1 s, so dragging is jerky.
- **The readouts.** "R" clashes with the random number R in the text (6.4). u_η and u_δ are not shown (place 8).
- **The caption explains the drawing well:** paths, arc, band. Four things are missing:
  - The 40 paths are the first 40 of 2000, projected onto the x–z plane, so their lateral spread looks smaller than in 3-D.
  - The band is 3λ_s deep because e^(−3) = 5 %. That is one clause.
  - Neither r_90 nor σ_s, the two numbers the text builds on, is drawn.
  - The dashed arc comes from a different stopping law than the paths (6.6).
- **The control label.** "after any retarding field": a retarding field is never introduced in this chapter.

**Verdict: needs small work.**

---

## Verdicts against STANDARD.md §4

| section | (1) picture | (2) model | (3) derivation | (4) checks | (5) method | (6) eq→screen | (7) limits | (8) reading | verdict |
|---|---|---|---|---|---|---|---|---|---|
| lead | yes | n/a | n/a | n/a | n/a | n/a | n/a | n/a | clear |
| 6.1 | good (marbles); electron–electron half missing | stated | 4m/M step skipped | none | n/a | n/a | n/a | Joy, Lin–Joy named | needs small work |
| 6.2 | weak (no picture of screening) | regime missing (Zα/β) | Rutherford, screening, integral all skipped | dimensional constant checked (M2) | n/a | n/a | Mott named | Bishop not read | needs work |
| 6.3 | good (pulse) but 1/E step skipped | CSDA unnamed; its justification fails at 800 eV | 78 500, 1.166 unexplained | ESTAR table: good | n/a | n/a | relativistic limit: good | ESTAR not linked | needs work |
| 6.4 | adequate | statistics stated | CDF inversion for (6.6) skipped; ê₁,₂ undefined | M3, M4 | Euler energy step, cut-off and binning errors not stated | n/a | n/a | n/a | needs work |
| 6.5 | missing for ε, λ_s | fitted parameters not acknowledged as fitted | universal law not written | comparisons present but framed one-sidedly | common random numbers not stated | Fig 6.1 legend incomplete | Mott attribution unsupported | data README not reachable | needs work |
| 6.6 | missing for 1.67 | hemisphere, rms | integral garbled in text, correct in Problem 2 | numbers check | n/a | arc and paths from different laws | σ_s two-part signal | KO source not read | needs work |
| 6.7 | n/a | n/a | n/a | "pass" misused (M8–M10); raw SymPy | n/a | n/a | good list; next model unsourced | links missing | needs work |
| simulation | good drawing | n/a | n/a | n/a | slow updates | R clash; r_90, σ_s not drawn; units | no validity warning | n/a | needs small work |

**Taylor's form.** Present: numbered equations, a Key result box, three worked examples with the page's numbers, and Problems at
the end. Missing: Key result boxes for (6.3), (6.5) and (6.7), which are the chapter's main formulas. No ★ derivation anywhere:
the chapter has no heavy passage at all, because the heavy passages were left out rather than starred.

**Typeface and house style.** As specified: Latin Modern text, Instrument Serif h3 at 38 px (27 px on the phone), Plex Mono table
headers and figure labels, wine accent, no foreign font.
