# Referee report · Project 07, Chapter 8 "The whole machine" (`#ch08`)

I read this as two people at once: a school student who is good at mathematics, and a physics graduate who knows electron
columns. I read only Chapter 8 and its simulation module `physics/ch08.js`.

**How it was read (9 November 2026).** I ran
`PYTHONDONTWRITEBYTECODE=1 python3 portfolios-src/electron-beam/build.py --site --out <scratchpad>/…/index.html`. The build
reported "9 of 10 chapters, 100 equations". `cmp` against `public/portfolios/electron-beam/index.html` shows no difference,
so the served file is the current build. I served `public/` locally and opened the page in headless Chromium (Playwright)
at 1400 px and 390 px, and at device scale 2 for the canvas. Chapter 8 has no folds. Its five sections 8.1 to 8.5 and the
simulation all render open, and I screenshotted each one whole at both widths. There were no console errors. I read KaTeX
from the rendered annotations.

I drove the simulation `#sim-ch08` through its sliders: r_t to 52.5 nm, V_ex in single slider steps, and V_land at 2.06,
2.46, 2.94, 3.51 and 10 kV. I also ran the page's own module (`physics/ch08.js`, with `ch02`, `ch04`, `ch05` and `ch07`)
in Node from the scratchpad. That gave the full process-window grid, the sensitivities at full precision, the stored
chapter-6 yields along the voltage axis, and the tolerance Monte Carlo under 20 different seeds (I patched `core.rng` in
memory only). "Measured" below means one of these runs. Nothing was written into the repository except this file.

Verdicts are judged against `notes/STANDARD.md` section 4: (1) picture, (2) model, (3) derivation, (4) checks,
(5) numerical method, (6) equation to screen, (7) limits, (8) further reading. They also follow Numa's verdict of
21 October 2026: Taylor's way, every step shown, every symbol defined where it first appears, one symbol with one meaning.

---

## The ten most serious places

1. **8.4, Example 8.3 reads its own numbers backwards.** "Higher voltage helps too in this model: at 1 pA, 0.45 nm at
   1.4 kV." Two sentences earlier, the same example gives 0.37 nm at 0.5 kV and 1 pA. So 0.45 nm at 1.4 kV is *worse*. The
   quoted number disproves the claim it is meant to support. Section 8.2 also says the opposite at the default: σ_CD
   answers V_land with **+0.52**, so it rises with voltage at 800 V.

   Measured along 1 pA, σ_CD (nm) is:

   | V (kV) | 0.50 | 0.60 | 0.71 | 0.85 | 1.02 | 1.21 | 1.45 | 1.73 | 2.06 | 2.46 | 2.94 | 3.51 | 4.19 | 5.00 |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   | σ_CD | 0.365 | 0.329 | 0.332 | 0.362 | 0.426 | 0.427 | 0.445 | 0.459 | **0.524** | **0.232** | **0.306** | **0.095** | 0.072 | 0.063 |

   Precision gets worse from about 0.6 kV to 2 kV. Then it jumps by factors of 2 to 3 between neighbouring grid points, in
   both directions. At 10 pA the pattern is the same: 0.108 nm at 0.7 kV, 0.157 at 2.0, 0.074 at 2.46, 0.094 at 2.94 and
   0.043 at 3.2. The text should describe what the map shows. Low voltage is best up to about 2 kV. Above that, the model's
   result is jagged and depends on item 2.

2. **8.4: the "edges steepen" explanation rests on a chapter-6 fit value that has stopped being physical.** "The sharp core
   of the secondary signal narrows with voltage while the halo moves out into a uniform background, so the edges in the
   model steepen."

   The stored silicon table in `ch08.js` gives a core width of 1.26 nm at 0.5 kV. It *grows* to 2.31 nm at 1 kV, stays
   near 2.1 to 2.3 nm up to 2 kV, and then collapses: 0.72 nm at 3 kV, 0.15 nm at 5 kV, 0.031 nm at 7 kV, and **0.0016 nm
   at 10 to 30 kV**. Check W2 prints it as "core 0.00 vs 0.00 nm". A secondary-electron "core" of 1.6 pm is smaller than an
   atom. It cannot be smaller than the secondaries' own escape range, which is about a nanometre. Its value has hit a floor
   of the fit.

   So the narrowing holds only above about 2 kV, and the very small σ_CD at 3 to 5 kV comes from a core width below 1 nm.
   That is not credible. W2 checks only δ and η against fresh runs. It does not check the core and halo widths, which
   decide the whole voltage axis of the window (core 2.30 against 2.49 nm at 1.2 kV is printed but not tested). A physics
   graduate would trust none of the window above 2 kV until this is fixed in chapter 6 or flagged here.

3. **Problem 3 cannot be done in the simulation, and the simulation never shows the chapter's key result.** "In the
   simulation, find the extraction voltage that restores the default current after the tip radius has grown by 5 %."

   In `compute()` the "nominal source" is `nom = src(q)`, the source at the *present* slider values. The current
   `I_beam = I_p·(B_r d_v²)/(B_r d_v²)_nom` is therefore always exactly I_p. Measured in the browser: with r_t moved to
   52.5 nm the readout I stays at **10.0 pA**, and σ_CD goes from 0.113 to 0.114 nm. The text says a 1 % blunter tip loses
   about 15 % of its current. By the module at fixed condensers, a 5 % blunter tip halves the current (×0.465) and raises
   σ_CD by 45 %. A reader who tries it on the sliders sees nothing happen.

   The fixed-condenser current exists only inside the sensitivity table and the tolerance Monte Carlo. Moving V_ex also
   leaves I at 10.0 pA. The V_ex slider is linear from 300 V to 8 kV over 1000 steps, so one step is 7.7 V, which is 0.77 %
   of V_ex. That is a 12 % change of current per step, so the answer (1046.9 V by the module; the table's estimate
   1000·1.05^(15.29/16.29) = 1046.9 V) could not be set even if the readout responded.

4. **The fixed-condenser current and the "aperture always at α_opt" rule describe two different machines (graduate).**
   8.3: "with the condensers left at their setting the current scales as B_r d_v² (brightness times source area, at the same
   magnification) and the source image as d_v." Current is brightness × area × *solid angle* × V\*. The solid angle is
   missing from the sentence.

   The module re-optimises the aperture angle at every setting. Measured: S(α_opt, r_t) = +0.36 and
   S(α_opt, V_ex) = −0.34. Chapter 5 then turns the current into a source image d_I = √(4I/(π²B_rV\*α²)), which goes as
   d_v/α, not as d_v. With fixed condensers *and* a fixed aperture, α would stay put and the probe would leave the optimum.
   With a re-optimised aperture, the current would change as α².

   In the tolerance Monte Carlo the aperture is re-optimised for every random draw of tip radius and pressure. A real
   aperture is a hole in a plate and does not follow a wobble. This makes the tolerance result optimistic. The text should
   say which machine it models, and why.

5. **8.2 contradicts the tolerance model it then builds.** "That is why a cold-field-emission gun is run at constant
   current, with the extraction voltage adjusted as the tip changes." If the gun is regulated, a tip-radius wobble does not
   pass into the current with S = −15. Yet 8.3 lets it do exactly that, and that is where nearly all the precision failures
   come from: tip radius alone gives a yield of 0.890, while lens, pressure and height alone each give 1.000 (measured). The
   reader needs one sentence saying whether the 3 % spread is between tips, between days, or within one image. They also
   need to know why regulation does not remove it (for example, the regulation acts on total emission, not on the
   brightness through the aperture). The claim about constant-current operation also has no source.

6. **The Key result misstates what the table shows.** "The optics and the scan settings follow power laws with exponents
   near one half." From the table: d_p answers V_land with −0.75, the lens half-width with 0.067 and WD with 0.44, and σ_CD
   answers η_c with **−0.21**. Only t_d and N give −0.5, and that is by construction. η_c is a scan or detector setting, and
   a student who has just learnt the counting law expects −0.5 for it. The text never mentions the −0.21.

   The physical picture is missing. Each beam electron makes a random number of signal electrons, so part of the noise is
   the beam's own shot noise, and collecting a larger share of the signal cannot remove that part. In 8.2 the −0.75 also
   deserves its one line, because it is exact (measured −0.7498). At the optimum where diffraction and the chromatic disc
   balance, d ∝ (λ·C_cΔE/eV)^{1/2} ∝ (V^{−1/2}·V^{−1})^{1/2} = V^{−3/4}. That is the "one small number worked" STANDARD
   item 4 asks for, and it is the best check in the chapter. The phrase "the probe current is by far the most sensitive
   quantity" is also loose: sensitivity belongs to a pair of input and output, not to a quantity.

7. **8.4 "More current always helps, by the counting law" is not what the numbers quoted with it show.** At 0.5 kV the
   precision goes from 0.37 to 0.019 nm over a factor of 1000 in current. That is a factor of 19, not √1000 = 32, because
   the probe grows from 5.7 to 8.7 nm (measured). At 5 kV the factor is 9.5. At 3.5 to 4.2 kV, more current *worsens* the
   precision above about 0.35 nA. Measured at 4.19 kV: 0.0075 nm at 350 pA, 0.0077 at 600 pA, 0.0112 at 1 nA. "Always" is
   false. The reason (the source image grows as √I, and σ_CD grows roughly in proportion to d_p, see item 6) needs a
   sentence.

   The example also quotes **0.0066 nm**. A precision of 7 pm is a thirtieth of the silicon bond length, and nothing in the
   text tells the reader that such numbers come from shot noise alone. There is no vibration, drift, stage noise or line-edge
   roughness. A school student will take 0.0066 nm at face value.

8. **The tolerance Monte Carlo has no stated statistical error (STANDARD 5).** With 300 draws and a fixed seed, I measured
   the page's own statistics under 20 other seeds:

   | quantity | over 20 seeds |
   |---|---|
   | yield | 0.880 ± 0.015 (range 0.853 to 0.913) |
   | sd(d_p) | 0.098 ± 0.008 nm |
   | 95th percentile of σ_CD | 0.167 ± 0.005 nm |

   Example 8.2 compares "87 %" (all four errors) with "89 %" (tip alone). That difference is about one seed-to-seed standard
   deviation. It is meaningful only because both use common random numbers, and the text says neither. One sentence giving
   the ±1.5 % is enough.

   The tolerance result can also be checked from the table, and the chapter misses the chance. The tip-only yield follows
   from S(σ_CD, r_t) = 7.33. The spread of ln σ_CD is 7.33·ln 1.03 = 0.217. The spec margin is
   ln(0.15/0.1132)/0.217 = 1.30 standard deviations. The predicted yield is 0.903, against the Monte Carlo's 0.890. That is
   the natural Example 8.2 and it joins sections 8.2 and 8.3.

9. **No figure, no picture of the chain, no further reading (STANDARD 1, 6, 8).** The chapter's whole subject is a chain of
   five modules, but there is no diagram of it. The reader has to hold "chapter 2 gives B_r, ΔE_50, d_v; chapter 4 gives C_s,
   C_c; …" in their head from one long sentence. A block diagram (tip → source → lens → probe → wafer → signal → width, with
   the symbols passed along each arrow) is the one figure the chapter cannot do without.

   There is no everyday physical picture either. The opening is abstract ("Turn one knob and everything downstream moves").
   There is no `.prefs` list and no source for any of these claims:

   - CFE guns run at constant current;
   - 300 µC cm⁻² is "about the dose that exposes a sensitive resist";
   - lithographers' process windows;
   - tolerance analysis.

   On the dose: at landing energies near 1 kV the beam's energy is deposited in a thin layer, so resists expose at area
   doses far below their 50 to 100 kV values. "Sensitive resist" at 300 µC cm⁻² needs a source or a rewording.

10. **The simulation's screen is not tied to the text's symbols, and several readouts are never defined (STANDARD 6).**

    - **Readouts.** They carry symbols only, with no words and no tooltip: "Y 0.867", "s_{d_p} 0.101 nm",
      "σ_CD,95 0.167 nm", "δ 0.747", "Ṅ_m 3510 per hour". The text never names Y, s_{d_p} or σ_CD,95. Y is also the
      secondary-plus-backscatter yield of chapter 7, so here one letter means two things.
    - **Slider names.** The text writes ε for the excitation drift, but the slider is "s_I". The text says "specification",
      and the slider is "σ_spec … (largest acceptable sigma_CD)", with a raw `sigma_CD`.
    - **The map.** It has no colour bar. The wine and grey shading covers only about one decade (`(log10 v − log10 spec + 1)/2`
      is clipped to [0, 1]). Over most of the map, σ_CD values from 0.006 to 0.15 nm look nearly the same, and the
      "darker grey ones miss it more" are hard to tell apart (measured alpha 0.23 to 0.31). No value in Example 8.3 can be
      read off the page.
    - **The present-setting dot.** It disappears without notice when V_land leaves 0.5 to 5 kV or I_p leaves 1 pA to 1 nA.
      The sliders run from 0.1 to 30 kV and from 0.1 pA to 10 nA. Measured at 10 kV: no dot, and no word.
    - **Placement.** 8.1 says "The simulation below", and 8.4 says "The left panel of the simulation shows". The simulation
      sits after 8.5, below the checks table and the Problems: 1 900 px further down at 1400 px, about 4 000 px at 390 px.

---

## Close behind

- **8.2 "−0.48 for the current, a little less than −0.5".** −0.48 is *greater* than −0.5. Write "a little smaller in size".
  The arithmetic behind it is worth one clause: −0.5 from counting, plus S(d_p, I_p) × S(σ_CD, d_p) ≈ 0.023 × 1 ≈ +0.02.
- **8.2: the table shows that σ_CD grows in proportion to the probe, and the text never says so.** WD gives 0.44 on d_p and
  0.44 on σ_CD. The lens half-width gives 0.067 and 0.068. So S(σ_CD, d_p) ≈ 1. That one fact explains the r_t row
  (7.33 ≈ −0.48·(−15.29) − 0.31·1), the lens-drift result in 8.3 ("costs little precision": 2 % in d_p gives 2 % in σ_CD),
  and the saturation at high current (item 7).
- **8.2 "the probe current answers the tip radius with −15 and the extraction voltage with 16: the field at the apex is
  V_ex/(k r_t)".** k is not defined in this chapter. If the field depended only on V_ex/r_t, the two numbers would be equal
  and opposite. They differ by exactly 1.00 (−15.29 and +16.29 on the canvas). Measured: B_r answers ±16.36 symmetrically.
  The difference comes from d_v ∝ r_t^{0.535}, which enters squared in B_r d_v². A graduate will ask why; one clause
  answers it. "Almost as steeply as an exponential" is vague. Fowler–Nordheim gives ∂ln J/∂ln F ≈ 2 + b φ^{3/2} v/F, and a
  number from chapter 2 belongs here.
- **8.2: the "1 % blunts" example and the linear picture.** "S=16 means sixteen per cent more" is the small-change limit.
  Measured, a 1 % blunter tip gives I × 0.858 (−14.2 %), and a 5 % blunter tip gives × 0.465, not −76 %. Problem 1 asks
  the reader to propagate a 3 % spread through S = −15 linearly (a 46 % spread), where linearisation is poor: the
  ±1σ factors are 0.64 and 1.57. Say that the linear rule holds in the logarithm, and only for small spreads.
- **8.2, the d_p column, r_t row −0.31, V_ex row +0.34.** A blunter tip gives a *smaller* probe. A student stops here. The
  reason is that at fixed condensers less current means a smaller source image. Say it. (Part of the number is also the
  α re-optimisation of item 4.)
- **8.2, the I column.** I answers V_land with 0 and I_p with 1.0 by construction (I = I_p × source ratio). Say so, or the
  zeros look like a physical result. Two currents are named on one table: the row "probe current I_p" is the requested
  setting, and the column "I" is the delivered current. Define both in one sentence.
- **8.2 "rate … −0.026 for the dwell time".** The table also shows −0.051 for N, twice the dwell-time value, because the
  frame time is N²t_d. The text says nothing about this. "the one-second overhead" is t_ov from chapter 7 and is not
  named here.
- **8.1, Example 8.1: "A 20 nm line … reads 26.3 nm".** A 6.3 nm (32 %) bias is passed over in silence. One clause
  ("the bias of chapter 7, from the blurred edge peaks") keeps the student from thinking the machine is broken. The bias
  also changes along the window (26.7 nm at 0.5 kV, 22.4 nm at 5 kV, measured), and 8.4 never mentions it.
- **8.1 "These numbers equal those of the separate chapters with the same inputs (checks W1 and W2)."** W2 compares
  interpolated chapter-6 yields with fresh Monte Carlo runs within 3 statistical errors. It is not an equality. W1 is a
  plumbing test (the same code called two ways), and the text should say so.
- **8.1: symbols named only by symbol.** B_r (reduced brightness), ΔE_50, d_v, C_s and C_c (spherical and chromatic
  aberration coefficients), α_opt, FW50 and "sharp core" all appear in this chapter without their names. A reader coming in
  from the table of contents needs the words once.
- **8.3: the sentence "Two of the errors act through the source: the tip radius and the pressure change B_r, ΔE_50 and d_v,
  and with the condensers…"** is a garden path: the reader parses "the pressure change" as a noun. Split it into two
  sentences.
- **8.3: (8.2) has steps skipped and symbols undefined.** "The lens strength goes as B²/V\*". In this sentence B is the
  lens field. Throughout the book B_r is brightness, so one letter has two meanings here. V\* (the relativistically
  corrected voltage) and "excitation" (ampere-turns NI, with B ∝ NI) are not defined here. The weak-lens result
  1/f ∝ ∫B²dz / V\* needs its chapter-4 equation number. "C_c is the focus shift per relative change of V\*" is a
  definition the student has not seen in this form; tie it to chapter 4's d_C = C_c α ΔE/(eV\*). The value of C_c is never
  given, so the reader cannot check "57.0 nm for ε = 10⁻⁵". It is C_c = 2.85 mm (measured; and C_s = 4.19 mm). The sign
  (a stronger lens focuses earlier, check W3) is in the table but not in the text.
- **8.3 "a simple rule that is exact for neither shape".** "Neither" of which two shapes? The reader must guess the probe
  profile and the uniform disc. Chapter 5 combines blur terms with a 1.3-power sum, and here a plain quadrature is used, so
  the book uses two rules. "Uniform disc" also assumes a uniformly filled aperture. A graduate would add that defocus
  enters σ_CD only to second order (√(d_p² + 2α²Δz²)). That is why 20 nm of wafer height costs only 0.008 nm of probe:
  √2 × 8.67 mrad × 20 nm = 0.245 nm, added in quadrature to 4.11 nm. This one worked line would replace a surprise with
  understanding.
- **8.3 "the natural logarithm of the gun pressure with a spread of 0.5".** Say what that means: a factor e^{0.5} ≈ 1.65 up
  or down. "Each is normal" is also not quite what the code does. The tip radius is drawn log-normal
  (r = r_t·1.03^z), and the 5 × 5 grid spans ±3σ and clamps beyond. "check W4: within 0.5 % of direct runs" checks B_r
  only (5 samples), not ΔE_50 or d_v.
- **8.3, Example 8.2 "the probe varies by 0.10 nm (standard deviation)".** The defocus terms only ever enlarge the probe,
  so the distribution is one-sided. A mean shift alongside the standard deviation would describe it better.
- **8.3 "Alignment, which the plan of this project listed".** This is a remark about the project's plan, not physics. The
  reader has not seen the plan.
- **8.4 "each with the aperture at its best angle".** That is fine for a map of operating points. But C_s and C_c come from
  `lens(q)` computed at V_land = 800 V for every point. I measured them as independent of V for this magnetic lens
  (C_s 4.18897 mm and C_c 2.84759 mm at 0.5, 0.8 and 5 kV), which is correct when the lens is refocused to the same WD.
  The text should say so in a clause, because the limits paragraph mentions a "coupling of landing voltage and lens".
- **8.4 "above which one image would put more than the allowed charge".** Dose here is an area density, not a charge. Say
  that it does not depend on N, so averaging more lines costs time but not dose.
- **8.5 "Chapter 8 has no Python twin".** That is project jargon; the reader does not know what a twin is. The claim "adds
  no physics of its own beyond (8.2) and the current at fixed condensers" also leaves out the √2 α|Δz| quadrature rule.
- **8.5 "the correlations between errors (a blunter tip is also a cooler one at the same current)".** "Cooler" is undefined
  (it means a smaller energy spread?). The example is not a correlation between two errors. The model *already* includes
  it (measured S(ΔE_50, r_t) = −0.68). A real example of a left-out correlation would be one between the tip radius and the
  pressure, or between the lens drift and the wafer height.
- **Problem 1, last sentence: "compare with what the Monte Carlo would give if the current were the only thing that
  changed".** The page shows no current spread. The Monte Carlo reports only s_{d_p}, σ_CD,95 and Y, so the comparison
  cannot be made from the page.
- **Typography seen on the page.** The HTML sensitivity table prints raw underscores: "d_p", "σ_CD", "tip radius r_t",
  "V_ex", "V_land", "I_p", "t_d", "η_c". The checks table prints "σ_CD", "C_c", "B_r", "2C_cε", "t_frame", "ε = 1e-05"
  and hyphen-minus "-0.500". The canvas prints "d_p", "σ_CD", "I_p", "V_land", "η_c", and the slider label "sigma_CD". In a
  note set like LaTeX these should be KaTeX or Unicode subscripts. 8.3 mixes "10⁻⁵" (Unicode superscripts, which render in
  a different glyph) with 10<sup>−9</sup>. The text gives σ_CD "0.11 nm" and "3500 measurements per hour" while the
  readouts show 0.113 nm and 3510: the same quantity to two different precisions on one screen.

---

## Section by section

### Chapter lead

Clear. It promises three questions and a check, and the chapter delivers them in that order. **Verdict: clear, leave it.**

### 8.1 One chain from tip to number

- The chain is stated in words only, in one 90-word sentence with nine symbols. There is no diagram and no everyday
  picture. An assembly line or a relay team would do; so would a short "what a technician sees" paragraph: the emission
  current slowly decays after a flash, the operator raises V_ex, and the image gets noisier.
- B_r, ΔE_50, d_v, C_s, C_c, α_opt, FW50 and "sharp core" are not named.
- "The simulation below" is about 1 900 px below at 1400 px.
- Example 8.1: the 26.3 nm reading of a 20 nm line is unexplained (see Close behind).
- "These numbers equal …" overstates W2.

| STANDARD | verdict |
|---|---|
| 1 picture | needs work: no figure of the chain, no everyday picture |
| 2 model | partly: the modules are named; the two additions (fixed condensers, aperture at α_opt) are stated without their conflict (item 4) |
| 6 equation to screen | needs work: simulation not where "below" says |
| overall | **needs work** |

### 8.2 Which inputs matter: the sensitivity table

- (8.1) is defined well, and the power-law reading is the right one for a student.
- The table is the core of the chapter and the text explains about half of it. Not explained:
  - the d_p column's −0.31 and +0.34;
  - the −1 asymmetry between r_t and V_ex;
  - η_c's −0.21;
  - N's −0.051;
  - the zeros of the I column, which are there by construction;
  - S(σ_CD, d_p) ≈ 1, which unlocks most of the rest.
- "a little less than −0.5" is wrong as written.
- k in V_ex/(k r_t) is undefined.
- The constant-current claim contradicts 8.3 and has no source.
- The Key result's "exponents near one half" is not what the table shows.
- The best available check, d_p ∝ V^{−3/4} (measured −0.7498), is not made.

| STANDARD | verdict |
|---|---|
| 2 model | adequate |
| 3 derivation | needs work: the scalings behind −15, −0.75, −0.21 are asserted, not derived |
| 4 checks | needs work: the V^{−3/4} and counting-law checks are available and unused |
| 5 numerical method | adequate: central differences ±1 %; I measured the step-size dependence as negligible (S(I, r_t) −15.2928 / −15.2923 / −15.2792 at h = 0.1 %, 1 %, 5 %) |
| overall | **needs work** |

### 8.3 Wobbles of a real machine: the tolerance Monte Carlo

- The opening paragraph has a good physical picture (no two tips alike, a drifting lens current, a wafer never where focus
  was set), and its assumptions are labelled honestly as assumptions.
- (8.2) has skipped steps and undefined symbols (B, V\*, excitation), and C_c's value is missing.
- The fixed-condenser current omits the solid angle, and the aperture follows each draw (item 4).
- The Monte Carlo's statistical error is not given (item 8).
- The table's prediction of the tip-only yield (0.903 against 0.890) is not used.
- The second-order effect of defocus, which is why height and drift cost so little, is not explained.
- Example 8.2's numbers reproduce exactly from the module: 0.0383, 0.0872 and 0.0082 nm; 0.890; pressure 0.0000 nm.

| STANDARD | verdict |
|---|---|
| 1 picture | good |
| 2 model | needs work: aperture behaviour, log-normal draws, grid clamp |
| 3 derivation | needs work |
| 4 checks | partly: W3 confirms (8.2) to 1e-5 relative; the yield prediction is missing |
| 5 numerical method | needs work: no error bars |
| overall | **needs work** |

### 8.4 Which settings work: the measurement window

- The lithography analogy is apt.
- Example 8.3 contradicts its own numbers (item 1) and 8.2's +0.52.
- It rests on a sub-ångström core width (item 2).
- It claims "always" where the module shows otherwise (item 7).
- It quotes 7 pm precisions without saying what is missing.
- The dose arithmetic (30 pA) is right: 3 C m⁻² × 10⁻¹⁸ m² / 10⁻⁷ s = 3 × 10⁻¹¹ A. The "sensitive resist" claim needs a
  source.
- The last sentence (charging, damage, signal depth) is the best physical paragraph in the chapter.
- The map cannot be read quantitatively: no colour bar, about one decade of shading, no probe.

| STANDARD | verdict |
|---|---|
| 1 picture | adequate |
| 4 checks | needs work |
| 6 equation to screen | needs work |
| 7 limits | good final sentence, but the window's own numerical artefacts are not named |
| overall | **needs work (the most serious section)** |

### 8.5 Checks and limits

- The checks table is useful, and every row passes as printed. But:
  - W1 is plumbing;
  - W2 leaves the core and halo untested, which are the inputs that matter most for 8.4;
  - W4 tests B_r only.
- "Python twin" is jargon.
- The limits paragraph is honest about assumed spreads. Its correlation example is confused, and it leaves out what the
  map most needs said: shot noise is the only noise.
- Problems: Problem 2 is good. Problem 1's last sentence cannot be answered from the page. Problem 3 cannot be done in the
  simulation (item 3).
- There are no further readings (STANDARD 8).

| STANDARD | verdict |
|---|---|
| 4 checks | partly |
| 7 limits | partly |
| 8 reading | missing |
| overall | **needs work** |

### Simulation `#sim-ch08`

- It renders at both widths with no errors. At 390 px the map and table stack cleanly.
- Measured cost: a full `compute()` is about 1.1 s at first load and about 0.1 s when only V_land changes (Node). With r_t
  changed it is about 0.55 s. In Chromium, a 20-step drag of I_p gave a worst frame gap of 184 ms.
- Equation-to-screen gaps, all in item 10:
  - readouts without words;
  - Y defined nowhere;
  - s_I against ε;
  - no colour bar;
  - the dot vanishes off-map;
  - raw underscores.
- I and r_t sliders: see item 3. The I readout cannot change, so the simulation cannot show the chapter's headline
  sensitivity.

| STANDARD | verdict |
|---|---|
| 5 numerical method | the code matches the text's description (14 × 14 grid, 300 draws, 5 × 5 bilinear grid in ln r, ln p, seed fixed) |
| 6 equation to screen | needs work |
| overall | **needs work** |

---

## Verdict summary

| section | verdict | the one thing to fix first |
|---|---|---|
| lead | clear, leave it | — |
| 8.1 | needs work | a diagram of the chain; name the symbols |
| 8.2 | needs work | explain the d_p, η_c, N columns; fix "a little less than −0.5"; replace the Key result's "near one half"; add d_p ∝ V^{−3/4} |
| 8.3 | needs work | state the aperture and condenser model consistently; give the Monte Carlo error; use the table to predict the tip-only yield |
| 8.4 | needs work (most serious) | rewrite Example 8.3 to match the map; flag the sub-nm core above 2 kV and shot-noise-only precision |
| 8.5 | needs work | a further-reading list; make Problems 1 and 3 answerable |
| simulation | needs work | make the I readout respond to r_t and V_ex (a fixed nominal source), or drop Problem 3; label the readouts in words |
