# Referee report · Project 07, Chapter 2 "The source" (`#ch02`)

Read as two people at once: a school student who is good at mathematics, and a physics graduate who builds
electron-beam columns and is reading this as a job applicant's portfolio. Only Chapter 2 was read.

**How it was read (9 November 2026).** `python3 portfolios-src/electron-beam/build.py --site --out <scratch>` builds a page
byte-identical to `public/portfolios/electron-beam/index.html` (1 731 870 bytes; "3 of 10 chapters, 60 equations"), so
the served file is the current build. The page was opened in headless Chrome (Playwright, served from `public/`) at
1400 px and at 390 px. Every section 2.1 to 2.13 and every part inside it was opened with its own fold toggle, as a reader
would, and screenshotted whole; no console errors. KaTeX text was read from the rendered annotations. Numbers marked
"recomputed" were recomputed by me from the page's own formulas and inputs. `PLAN.md` and any check files were not read.

Verdicts use `notes/STANDARD.md`, section 4 (1 picture, 2 model, 3 derivation, 4 checks, 5 numerical method, 6 equation to
screen, 7 limits, 8 reading) and Numa's verdict of 21 October 2026 (Taylor's way: every step shown, every symbol defined
where it first appears, one symbol one meaning, ★ results restated unstarred, no headline hooks).

---

## The ten most serious places

1. **2.5, Example 2.4 and the symbol table: the stated result does not follow from the stated inputs.**
   "Then J₀ = (1.5414×10⁻⁶/4.5) × 4²/1.051² × e^{−10.66} A/nm², which is 1.13×10⁸ A/m²." With the inputs printed
   (v = 0.6538, t = 1.0515) this arithmetic gives **1.17×10⁸ A/m²** (recomputed). 1.13×10⁸ is what Forbes' approximate
   v = 0.656 gives. The next sentence, "The full integral … gives 1.16×10⁸ A/m², at 300 K", then reads as "temperature adds
   3 %", but with the correct J₀ the full 300 K integral is *below* the T = 0 formula (C11 itself says full/analytic =
   0.9958 at 4 V/nm). A graduate checks this example first; it fails.
2. **2.11: a wrong statement and a wrong explanation of brightness.** "ln J varies as F¹⁷ locally" — it is J, not ln J, that
   varies as F^{17.5} (∂lnJ/∂lnF = 17.5, section 2.10.3). Then: "electrons come out of a tiny patch … with a small
   transverse energy (0.17 eV). A large current density on a tiny area, with a narrow distribution of angles, is a high
   brightness." Brightness is per unit area, so the size of the patch does not enter it; and section 2.8 says the opposite
   about the transverse energy: "the cold source wins by its current density … at similar transverse energy" (0.168 eV
   cold, 0.155 eV Schottky). The summary section contradicts the derivation it summarises.
3. **2.12/2.13: the first hand-over number rests on a calculation the chapter never describes.** The emission current
   I_e (9.53×10⁻⁸ A), the "effective emitting area of 820 nm²" (2.10, 2.11) and the Fowler–Nordheim plot of the
   simulation all come from "the current of the cap integral", with "the cosine law F(ϑ) = F₀ cos ϑ". This appears only in
   the equation-to-screen table and in "Where the drawing differs from the model", after the numbers have been used.
   No equation, no assumption about where the cap ends, no number of quadrature points. More generally the chapter has no
   numerical-method passage at all (STANDARD item 5): how the master integral J = e∫N D dw is evaluated (grid, limits,
   step, measured error), how ΔE is found, how the fit of 2.9 is done (least squares in ln I? weights? which parameters
   free?) are not stated anywhere. Only "Gauss–Legendre quadrature (48 points)" for v(f) is given.
4. **2.9: the "check against a measurement" fits two free numbers to a near-straight line, and the one internal test it
   could make is not made.** "A model that has not met a measurement is a story. Here it meets one." The fit frees ζ and the
   emitting area A, and 2.9.1 concedes φ is not tested and r is not predicted. What the model *could* predict is A: with the
   chapter's own cosine-law cap, J ∝ cosⁿϑ with n ≈ ∂lnJ/∂lnF, so A ≈ 2πr²/(n+1). This reproduces the page's own 820 nm² at
   r = 50 nm (gives 849 nm²). At the fit's r = 132 nm and F ≈ 2.2 V/nm, n ≈ 31 and A ≈ 3.4×10³ nm² (my estimate) against
   the fitted **781 nm²**, about 4× smaller. That is the place where the model meets the data, and it is not discussed.
   Also, 2.2 says "the current in section 2.9 is predicted only to a factor, not to a percent", but 2.9 never predicts an
   absolute current (A is fitted), so the sentence has nothing to point to.
5. **2.8: the brightness, the number a column builder cares most about, is never compared with anything, and its
   convention is not stated.** "Chapter 3 shows (Liouville) that B/V does not change" and "is dealt with in chapter 3, where
   we put published values next to ours". Chapter 3 is on the page as "In preparation. This chapter has not been written
   yet." So the justification for B_r and the only external comparison both point to an empty chapter. The hand-over gives
   B_r = J/(π⟨ε_t⟩) and d_v = 2r√(⟨ε_t⟩/eV) with the *mean* transverse energy; a column builder needs to know whether these
   are to be read as Gaussian, FWHM or FW50 quantities (practical brightness conventions differ by factors of about 2), and
   chapter 3 will inherit whatever is meant. The model's B_r (2.2×10⁸ cold, 1.7×10⁷ Schottky) should be set against at
   least one published reduced brightness here, with conditions.
6. **Whole chapter: one symbol, several meanings, sometimes in the same equation.** `k` is the field factor in (2.1)
   ("F = V/(kr)") and Boltzmann's constant in kT from (2.13) on; both appear in the same simulation panel. `d` is the energy
   0.175 eV and the differential in the same line (2.16): "1/d = −dG/dw". `κ` is the decay constant κ(x) (2.7), the
   constant κ_e (2.3, never defined), and the shank-capture factor κ (2.33). `a` is the FN constant (2.20), the lattice
   constant (2.10.1) and the adsorption rate (2.33). `b` is the second FN constant and the impact parameter (2.31). `f` is
   the scaled field and the Maxwell–Boltzmann distribution (2.32), and "−f(w)" is the Fermi function in check C4. `s` is
   the sticking coefficient and s(f) (2.23). `t` is t(f) and time. `ρ` is a radial distance (2.1.2) and a current ratio
   (2.10.3). `Δφ` is the Schottky lowering and the adsorbate shift Δφ_ads. A student loses the thread at each reuse.
7. **2.10.5 and the simulation: the flash is not a tungsten flash, and the model's time course is not Cho's.** "A flash of
   5 s at 1000 K therefore removes everything", with one E_d = 1.9 eV and ν₀ = 10¹³ s⁻¹ "chosen so that hydrogen-like
   adsorbates leave … near 700 K". The simulation offers CO and N₂ as residual gases with the same E_d, so CO leaves at
   1000 K too; cold-field-emission guns are flashed far hotter (around 2000 K and above) precisely because CO and oxygen do
   not leave at 1000 K. A column builder will stop here. Separately, 2.10.4 describes Cho's current as staying "near its
   initial value for a time τ₉₀ … and then falls quickly", while the patch model (Fig. 2.8) falls from t = 0; only the
   scaling pτ₉₀ = const is tested, and the shape disagreement is not said. Also 2.10.1: "at 10⁻⁴ Pa a clean surface is
   covered in a fraction of a second" against its own table, which says 1 s (H₂) and 3 s (CO).
8. **2.2 and 2.3: the steps a student needs are skipped, and one explanation reads the wrong way round.**
   "(One might expect e²/(8πε₀x), the energy of the real pair at separation 2x. It is twice as large, …)": "It" reads as
   the true energy, which is half, not twice. The top of the barrier is given ("Setting dU/dx = 0 gives … x_m = √(Q₀/(eF)),
   where U_max = φ − Δφ") without the one line U_max = φ − 2√(eFQ₀) that produces (2.6). In 2.3.2 "U − w =
   eF(x − x₁)(x₂ − x)/x" is not shown, and the central claim "a correction factor that depends only on f" is asserted, not
   shown (it needs the scaling x → x·φ/(eF)). Cross-reference wrong: "the exponent in Example 2.2 is 10.7" — Example 2.2 has
   no exponent; it is Example 2.3.
9. **2.12: two of the four figure panels say something other than what they show.** Fig. 2.9b: "rose: covered tip". The
   rose line lies about 6.2 below the clean line in ln(I/V²), which is ln ρ = ln 0.0021, a *fully* covered tip (θ = 1);
   the current state (θ = 18–24 % in my runs, I/I₀ ≈ 0.8) is the solid wine line, which the caption does not name.
   Fig. 2.9c names only "grey: clean tip". The readout "Reduced brightness B_r 1.77×10⁸" has no unit. The lead says "The
   numbers beside it are the ones handed to chapter 3", but they sit below the figure, and they change as simulated time
   passes (I_e 7.20×10⁻⁸ to 7.77×10⁻⁸ A in my two runs against 9.53×10⁻⁸ A in the 2.13 table): which state does chapter 3
   receive?
10. **2.13 and elsewhere: working-process traces in a portfolio.** "The four numbers of the contract (PLAN.md, section 6)",
    "`notes/electron-beam/ch02/check_parity.py`", "`handover()` in `physics/ch02.js` and `ref/ch02.py`", "(the planning
    session read it on 9 November 2026)", "which I cite from the two papers above and did not open" (one "I" in a "we"
    text), raw program output in prose ("A_R = 1.20173e+06", "ratio of the two currents 1+2.3e−05"), and a checks table set
    in ASCII ("x = phi(1 ∓ sqrt(1-f))/(2eF)", "e^{-G_F}") with C18 missing between C17 and C19 under "19 of 19 checks
    pass". A hiring reader sees a notebook, not a finished chapter. The two company sources behind the chapter's framing
    are the weakest: the Applied Materials press release was "not re-opened for this chapter", yet it carries "The cold
    source that Applied Materials describes publicly for its electron-beam metrology column is of the third kind; the
    Schottky source of the second kind is its main competitor" (2.1, no citation at that point; "main competitor" has no
    source at all) and "a single atom" (2.10).

---

## Section by section

### Chapter lead

- "Assumed, not measured: the field factor k, the work functions, the desorption energy and the effect of an adsorbate."
  Also assumed: ν₀ = 10¹³ s⁻¹, the Schottky operating field 0.5 V/nm; and κs is fitted, not measured. The list is
  incomplete.
- The lead lists the hand-over as "emission current, reduced brightness, energy spread, virtual source size"; 2.7 calls
  ΔE "the first of the four numbers we hand over". Same four, two orders.

### 2.1 A needle, a wall and a leak

Student: the door-handle spark and the lightning rod are a good picture; the bowl-of-water image of the work function
works. Graduate: F = V/(kr) is fine, k = 5 is attributed.

- "The cold source that Applied Materials describes publicly … the Schottky source of the second kind is its main
  competitor." No citation where it stands; "main competitor" is unsupported anywhere (see 10 above).
- "This is folded into one dimensionless factor k, of order unity to several" — the reader is not told what sets k (cone
  angle, shank, anode distance), so cannot judge k = 5 for a 50 nm tip at 1000 V. One sentence would do.
- Example 2.1: clear and checked (4.0 V/nm; 1/129 of the atomic field; 1.125 nm). Fig. 2.1 is clear; its label "electrons
  leave the apex" is crossed by a dashed field line.
- Picture missing for the student: why a *sphere's* field is V/r is derived, but why charge crowds at a sharp point
  (the step from "the field grows with that crowding" to F = V/r) is left to the formula.

**Verdict: clear, leave it** (apart from the unsupported company sentence, which should carry its source or go).

### 2.2 The wall an electron sees

- "The conduction electrons rearrange until the field just outside the surface is perpendicular to it." The student is
  not told why a mirror charge reproduces this (the surface is an equipotential, and the mirror charge makes the plane an
  equipotential). No sketch of the image charge; one small figure or one sentence would carry it.
- "It is twice as large" — ambiguous, reads the wrong way (see 8 above). The reason given ("as the electron moves away the
  induced charge … rearranges, and only half of the pair's energy is stored in the field outside the surface") mixes two
  explanations; either one, stated cleanly, is enough.
- Skipped step: from dU/dx = −eF + Q₀/x² = 0 to Δφ = 2√(eFQ₀) = √(e³F/(4πε₀)); the reader gets x_m and Δφ but not the line
  between them. Similarly f = 4eFQ₀/φ² equals e³F/(4πε₀φ²) only after substituting Q₀; one "=" step would help.
- "The derivation … was checked symbolically (checks C1 and C2 in section 2.13)" — fine for the graduate, but it stands in
  place of the step for the student.
- Example 2.2: "x₂ − x₁ = 1.04 − 0.087 ≈ 0.95 nm" mixes 1.038 and 1.04; trivial.
- Fig. 2.2: the legend sits on the F = 2 V/nm curve ("F = 0 (image only)" and "F = 2 V/nm" are struck through by it).
- "It is one of the reasons the current in section 2.9 is predicted only to a factor, not to a percent." Unsupported:
  2.9 fits the area and never predicts an absolute current (see 4 above).
- Graduate: the barrier is planar; at r = 50 nm the curvature correction is small, at the 15 nm of the Ayari tip it is not.
  Worth one clause here or in 2.13.2 with the name of the curved-barrier treatment.

**Verdict: needs work** (the factor-of-two sentence, the missing U_max step, the unsupported forward claim, the legend).

### 2.3 Leaking through: the WKB transmission

- Physical picture: "A wave that meets a barrier … does not stop at the edge … what is left at the far side leaves as an
  electron." For the school student this is the first meeting with tunnelling and a wave function; there is no picture of
  the wave decaying in the wall (a sketch over Fig. 2.2 would do it), and "leaves as an electron" is vague.
- (2.7) The Schrödinger equation is dropped in unexplained for the student and is not starred, though it is heavier than the
  starred 2.3.2.
- "The probability of finding the electron, |ψ|², falls by the square of that factor between the two turning points" —
  "that factor" has no clear antecedent (the exponential in (2.8)). "The transmission probability is taken as this ratio"
  — the graduate wants to hear that this is the standard JWKB result with a prefactor ≈ 1 for this barrier, not an ad hoc
  choice.
- "the missing prefactor is a factor of order one that is absorbed in the uncertainty named in section 2.9" — 2.9 names no
  such uncertainty.
- "the exponent in Example 2.2 is 10.7" — wrong example (it is 2.3).
- "with the constant 2κ_e = 10.246 eV^{-1/2} nm^{-1}" — κ_e is never defined, and κ is already κ(x).
- 2.3.2 ★: "U − w = eF(x − x₁)(x₂ − x)/x" and "depends only on f" are asserted (see 8 above). "which has no singularity" —
  the original integrand has none either; what the substitution removes is the square-root behaviour at the end points
  that spoils Gauss–Legendre. Say that.
- The ★ result v(f) and (2.12) are used unstarred in 2.5, but the plain statement "v(f) is the factor by which the image
  charge shrinks the exponent; v ≈ 0.65 here" is only in the 2.5 table. Restate it after the starred part.
- Example 2.3: "Of every 42532 electrons that arrive at the wall one gets out." True only for electrons at the Fermi level
  with zero transverse energy; electrons below it see a thicker wall. Five significant figures on an estimate the text calls
  order-of-one uncertain. "multiplies the transmission by e^{16.30−10.66} = 283" — e^{5.64} = 281; the difference is
  rounding of the shown numbers, but the shown arithmetic does not give the shown answer.
- Fig. 2.3: the legend overlaps the t(f) curve ("v(f) ≈ 1 − f + (f/6) ln f" is struck through); the solid and dashed v(f)
  curves coincide to the eye, so "dashed" cannot be seen. Caption: "of section section 2.5".

**Verdict: needs work.**

### 2.4 Counting the electrons that arrive: the supply function

- Student: "A momentum cell of size d³p holds 2d³p/h³ electron states" — why h³ (one state per h³ of phase space, per unit
  volume) is not said; "per unit volume" is missing from the sentence. This is the hardest idea of the chapter for a school
  student and it is neither explained nor starred.
- "the transverse momentum element is dp_y dp_z = π d(p_t²) = 2πm dε_t" — the polar-coordinate step (2πp_t dp_t) is
  skipped.
- "The check C4 verifies the derivative that defines it." Unclear what "the derivative that defines it" is; say
  "d/dw[kT ln(1 + e^{−w/kT})] = −𝓕(w)".
- Key result box and the stated hidden assumption (D depends only on w) are good.

**Verdict: needs work** (small: two missing explanations for the student; the graduate is served).

### 2.5 The Fowler–Nordheim equation

- "the equation that the experimenters of the 1950s used to count nothing but volts and amperes" — the phrase does not
  parse; presumably "with nothing but a voltmeter and an ammeter".
- (2.16) "1/d = −dG/dw" — d as a quantity and as a differential in one equation.
- "d is the decay length of the electron's states in energy: d is an energy, 0.175 eV at the working point." "Decay length
  in energy" will lose the student; say "the energy over which the transmission falls by a factor e". Also, the formula
  just given, d = 2F/(3b√φ), is the t = 1 case and gives 0.184 eV; 0.175 eV is d with t = 1.0515. The sentence pairs one
  formula with the other number.
- Key result box: "a = e²/(8πh)" while (2.20) has e³/(8πh); the missing e is absorbed by φ in eV, which the box says only
  by implication. A student will think one of them is a misprint. "It is exact within the model … at T = 0" — it is the
  first-order expansion of G about the Fermi level, not exact; the next paragraph's comparison with the full integral shows
  it.
- Example 2.4 and the table entry "1.13×10⁸": wrong from the shown inputs (see 1 above).
- Limiting case: "At about f ≈ 0.8 the derivation fails … because electrons at the Fermi level can fly over the barrier
  top." By (2.5) the top reaches the Fermi level at f = 1, not 0.8; what fails near 0.8 is the linear expansion of G. As
  written it contradicts 2.2.
- 2.5.3 ★: clear and complete; boundary-term condition stated. Good.
- 2.5.4: "Plotted against 1/V, the right-hand side is a straight line to a good approximation." The intercept term contains
  t²(f), which also changes with V; the slope formula ignores it silently. Say so, and quantify "good" (the curvature over
  a typical range).
- (2.22) ζ ("voltage conversion length") is well introduced.

**Verdict: needs work** (the example, the f ≈ 0.8 sentence, "exact", the d/0.175 mismatch).

### 2.6 Heat helps: Richardson–Dushman and Schottky emission

- Clear derivation. "For electrons with w above the top of the barrier, D ≈ 1" — also say D ≈ 0 below it is assumed; the
  16 % excess is then explained as tunnelling, which is good.
- "A_R = 1.20173e+06 A m⁻²K⁻²" — program output format in prose.
- Graduate: the theoretical A_R is about twice the measured Richardson constant of tungsten; the Schottky current depends
  on it linearly. One sentence of limit.
- The Schottky preset's r = 500 nm, V = 2000 V, k = 8 are only revealed in the 2.13 table; here "we choose k so that this
  holds" leaves the reader without the geometry.
- Fig. 2.4: legend overlaps the F = 4 V/nm curve ("F = 0.5 V/nm" struck through); y ticks mix "10000, 1000, 100" with
  "10⁵, 10⁶"; dots are said to be the full integral, but they are joined by lines and the line style is not explained.
- 2.6.1: "(check C11: against the analytic Fowler–Nordheim formula …)" — which analytic formula, (2.20) at T = 0 or with
  (2.21)? The ratios in C11 only make sense if it is (2.20) × (2.21), or if the Example 2.4 number is wrong; say which.

**Verdict: clear, leave it** apart from the number format and the figure legend.

### 2.7 How wide is the energy: the spread ΔE

- "(the second relation … follows from integrating (2.14) by parts" — it follows from exchanging the order of integration
  (w and ε); calling it "by parts" will send the student looking for a u dv that is not there. "ratio of the two currents
  1+2.3e−05" — program output in prose.
- "The peak is at ε* = kT ln[kT/(d − kT)] when d > 2kT" — the peak exists for d > kT; d > 2kT is the condition for it to
  lie below the Fermi level. "−0.046 eV" here, "−0.0453" in C13.
- "Because d ∝ F/√φ" — with t(f) dropped; fine as a scaling, say so.
- Fig. 2.5 is plotted against "energy relative to the peak", so the reader cannot see what the text discusses (peak below
  the Fermi level; Schottky peak 0.15 eV above the barrier top). Plot against energy relative to the Fermi level, or mark
  both reference levels.
- "Against published values": honest and well bounded. "Both widen the measured distribution (inference, not tested
  here)" — the graduate expects the Boersch effect to be named here (it is named only in 2.13.2).

**Verdict: needs work** (small: "by parts", the peak condition, Fig. 2.5's abscissa).

### 2.8 Brightness and the virtual source

- "Chapter 3 shows (Liouville)" and "is dealt with in chapter 3" — chapter 3 is empty on the page (see 5 above).
- 2.8.1: "An electron with transverse energy ε_t that has been accelerated to the energy eV moves at a small angle α to the
  axis with α² ≈ ε_t/(eV)" — true for acceleration in a uniform field, where p_t is conserved. 2.8.2 then switches to a
  radial field, where p_t is not conserved and L is. The two pictures are used side by side without saying which one the
  brightness formula assumes. The result B_r = eJ/(π⟨ε_t⟩) is the standard Langmuir-type result and deserves its source.
- "with j per joule, so ej is per electronvolt" — e·j is per volt (A m⁻² V⁻¹); "per electronvolt" is wrong as written and
  is the step a student uses to get the units of B_r.
- "(integrate e^{−G_F} e^{w/d} up to w = −ε_t and compare with (2.19))" — the one step that gives j(ε_t) = (J/d)e^{−ε_t/d}
  is left as an instruction; show the two lines.
- 2.8.2: "the model has a perfectly radial field, no extractor lens and an emitting patch of zero size. All three would
  increase d_v". In a perfectly radial field every radial path points back to the centre wherever it starts on the sphere,
  so the patch size does not enter at all; the model does not assume a zero-size patch (it uses 820 nm² elsewhere). The
  third reason should go or be restated.
- d_v definition: "We define the virtual source diameter as d_v = 2r√(⟨ε_t⟩/(eV))" — which width is this (rms, FWHM,
  FW50)? Chapter 3 needs to know (see 5 above).
- C17 check of the asymptote is good and concrete.

**Verdict: needs work.**

### 2.9 Checking the model against a published tungsten tip

- "A model that has not met a measurement is a story." A headline hook (Numa's rule 3); plain "We now compare the model
  with a measurement" does the job.
- Data description is careful and sourced; good.
- The test itself: two fitted numbers, φ untested, r not predicted, A not compared with the model's own prediction (see 4).
- "The deviations look irregular." Fig. 2.6 (right) shows runs of same-sign residuals (mostly negative from about 1380 to
  1490 V, positive from 1500 to 1540 V). Either say they are runs and attribute them to drift during the sweep, or give a
  number (autocorrelation, runs test). "so the model has no deviation to explain that the measurement does not already
  contain (inference)" — fair once that is done.
- "The fit places the data at f = 0.142 to 0.176 … at the lower edge of the range that Forbes and co-workers call
  physically reasonable … 0.15 ≤ f ≤ 0.45" — the lower part of the data, 0.142 to 0.15, is *outside* that range. Say so.
- "The radius. The fit gives a tip of 130 nm radius if k = 5, against 15 nm initially." A factor 9 is the most striking
  number in the section; "It does not contradict the model" is too quick. Either k is not 5 for this tip, or the tip
  blunted ninefold; the reader should be told which the authors favour and what it does to the k = 5 used for the presets.
- Fig. 2.6 left: the legend's last entry sits on the x axis line.

**Verdict: needs work.**

### 2.10 Vacuum and contamination

- 2.10.1: clear derivation of the Hertz–Knudsen flux. "N_s = 1/a²" with a the bcc lattice constant is the density of a
  (100) plane; say which plane (the emitting planes of a ⟨111⟩ or ⟨310⟩ tip differ). Symbol `a` is reused two
  equations later for the adsorption rate. "at 10⁻⁴ Pa a clean surface is covered in a fraction of a second" contradicts
  the table (1 s, 3 s).
- "at 10⁻⁹ Pa, which is the figure that Applied Materials gives for its columns (it states 'well below 1×10⁻¹¹ millibar'
  …)" — from a source "not re-opened for this chapter". Also "well below 10⁻⁹ Pa" is not "10⁻⁹ Pa".
- 2.10.2: "t* ≈ θ*N_s/(κsΦ)" — the step ln(1 − θ*) ≈ −θ* for small θ* (5 % error at θ* = 0.1) is skipped.
- 2.10.3: the model-assumption box is honest. "We take Δφ_ads = 1.0 eV" — a graduate will ask for the measured work-function
  change of hydrogen on tungsten, which is smaller; the choice drives ρ = 0.0021 and so the whole current decline. Give one
  literature value next to it, or say none was found.
- "A field higher by 10 % raises it by 4.9" — fine, but with ∂lnJ/∂lnF = 17.5 the reader computes 1.1^{17.5} = 5.3 and
  wonders; one clause ("the derivative itself falls as F rises") closes it.
- 2.10.4: Cho's plateau-then-drop against the model's immediate decline is not stated (see 7). Fig. 2.7 legend says
  "s = 0.54" where the fitted number is κs.
- 2.10.5: "The values E_d = 1.9 eV and u₀ = 10¹³ s⁻¹" — u₀ should be ν₀. Flash temperature and gas species (see 7). The
  flash-interval table is clear.
- "One atom." Good, honest arithmetic (1/8201). "see section section 2.13". For a portfolio, the paragraph tests a
  company's public sentence and reports that the model "does not reproduce the claim"; the model's limit is stated, which
  is right, but a reader from the industry will notice the framing.
- Typography: the superscript "⁰" of "10⁻¹⁰" in both tables is set in a fallback glyph of a different size.

**Verdict: needs work.**

### 2.11 Why the cold tip is bright but fragile

- "ln J varies as F¹⁷ locally" — wrong (see 2). "a tiny patch" and "small transverse energy" as the cause of brightness
  contradict 2.8 (see 2).
- "our effective emitting area is 820 nm², 5 % of the hemisphere, 15708 nm²" — the area comes from the undescribed cap
  integral (see 3); two numbers in two typefaces in one clause.
- "the current falls by 10 % in a few hours" at 10⁻⁹ Pa — recomputed 4.8 h with κs = 0.54; give the number.
- "A Schottky emitter is hot, the adsorbates leave as fast as they come" — follows from (2.33) at 1800 K but no k_d value is
  given; one number would support it.

**Verdict: needs work.**

### 2.12 The source on your screen

- Figure captions of 2.9b and 2.9c, the B_r unit, "beside it", the changing hand-over numbers (see 9).
- Fig. 2.9a: the label "anode 0 V" is drawn across the anode bar.
- Equation-to-screen table: "current of the cap integral" is used before it is defined (see 3). The rest of the table is
  clear and is what STANDARD item 6 asks for.
- "nothing is integrated while it plays, the whole run is computed at once (the rate equation has an exact solution) and
  replayed" — good; it would help to say the same for the emission integrals (are they recomputed per slider move? with
  what grid?).
- The simulation starts running on load; the 2.9d "now" line moves while the reader reads the caption.

**Verdict: needs work.**

### 2.13 Hand-over, limits and checks

- Process traces and file paths (see 10). For a reader outside the repository "PLAN.md, section 6", "derive/ch02.py",
  "data/ch02/ayari2023_w111_iv.csv" and "paramIV4d.txt" are dead ends; link the public data set (the Zenodo DOI is given
  in the sources) and drop internal names.
- Hand-over table: clear. Add the convention for B_r and d_v (see 5) and say whether the numbers are for the clean tip.
- 2.13.2 lists the omissions well but does not name the next, more complete model (STANDARD item 7): e.g. a curved-barrier
  treatment, a general thermal-field formulation, a field solver for k, a Monte Carlo for the Boersch effect.
- Checks table: ASCII mathematics, C18 missing, "J^-1" dangling at the end of C8's detail. At 390 px the "detail" column is
  cut off at the right edge of the screen (the table is 420 px wide in a 390 px page that does not scroll), and 16 display
  equations of the chapter scroll sideways with their equation numbers off screen ((2.3), (2.5), (2.6), (2.9) to (2.11),
  (2.14), (2.16), (2.17), (2.20), (2.24), (2.26), (2.28), (2.32) to (2.34)).
- Problems: three, with answers; recomputed, all three answers are right.
- Sources: each says what was read, which is good practice. Missing for the graduate: Fowler and Nordheim (1928) and
  Murphy and Good (1956) are named in the text ("Murphy and Good form") but not listed; no textbook or review on electron
  sources (a column builder expects at least one standard review of cold-field and Schottky sources with measured
  brightness and energy spread). Dolan and Dyke is "Read: abstract, introduction, the section on the work function", yet
  2.6.1 credits them with a numerical result from the body of the paper. Forbes (2006) is cited for v(f) "good to 0.0024"
  without being opened; it is disclosed, but the claim is then stated in the text as Forbes' finding.

**Verdict: needs work.**

---

## Across the chapter

- **Numerical method (STANDARD 5) is missing as a passage.** See 3. One short section before 2.12 would cover the master
  integral, the cap integral, the energy-distribution width, and the fit.
- **★ is used unevenly.** 2.3.2 and 2.5.3 are starred; 2.3's Schrödinger/WKB step, 2.4's phase-space counting and 2.8's
  brightness derivation are as heavy and are not.
- **Figures.** Legends sit on curves in Figs. 2.2, 2.3 and 2.4; the anode label is crossed in 2.9a; Fig. 2.5 discards the
  energy reference the text talks about.
- **Precision.** Many numbers carry more figures than the model (42532 electrons, 8201 sites, 15708 nm², 1.2000 eV); the
  chapter itself says the prefactor is uncertain by a factor of order one.
- **Portfolio reading.** The physics is mostly right and the honesty about assumptions ("a model assumption", "inference,
  not tested here") is a strength a hiring reader will notice. What undercuts it is the wrong example number in 2.5, the
  contradiction in 2.11, the empty chapter 3 behind the brightness, the internal file names, and the flash at 1000 K.

## Verdicts

| section | verdict |
| --- | --- |
| lead | needs work (small: incomplete list of assumptions) |
| 2.1 | clear, leave it (company sentence needs its source) |
| 2.2 | needs work |
| 2.3 | needs work |
| 2.4 | needs work (small) |
| 2.5 | needs work |
| 2.6 | clear, leave it (number format, figure legend) |
| 2.7 | needs work (small) |
| 2.8 | needs work |
| 2.9 | needs work |
| 2.10 | needs work |
| 2.11 | needs work |
| 2.12 | needs work |
| 2.13 | needs work |
