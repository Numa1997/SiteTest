# Referee report · Project 07, Chapter 3 "Acceleration, brightness, energy spread" (`#ch03`)

Read as two people at once: a school student who is good at mathematics, and a physics graduate who builds
electron-beam columns and is reading this as a job applicant's portfolio. Only Chapter 3 was read.

**How it was read (9 November 2026).** `python3 portfolios-src/electron-beam/build.py --site --out <scratchpad>` builds a page
byte-identical to `public/portfolios/electron-beam/index.html` ("4 of 10 chapters, 68 equations"; `cmp` reports no
difference), so the served file is the current build. The page was served from `public/` and opened in headless Chromium
(Playwright) at 1400 px and 390 px, also at device scale 2 for the simulation. Chapter 3 has no folds: all eight sections
3.1 to 3.8 render open, and each one was screenshotted whole. No console errors. KaTeX was read from the rendered
`aria-label`s. The simulation `#sim-ch03` was driven with its two sliders (default 1 kV / 0.8 kV; 8.85 kV / 0.80 kV;
0.50 kV / 17 kV). Numbers marked "recomputed" are mine, from CODATA constants and the page's own formulas and inputs.
`PLAN.md` and the check files were not read.

Verdicts are against `notes/STANDARD.md`, section 4 (1 picture, 2 model, 3 derivation, 4 checks, 5 numerical method, 6 equation
to screen, 7 limits, 8 reading), and Numa's verdict of 21 October 2026: Taylor's way, every step shown, every symbol
defined where it first appears, one symbol one meaning, ★ results restated unstarred.

---

## The ten most serious places

1. **3.7: the text contradicts its own table.** "both gaps lie within the factor of two the table itself carries." The
   table gives model/book = **3.4** for the cold source. That is not within a factor of two. Worse, the comparison is between
   the wrong quantities: the model column is the *practical* brightness `B_pr` (already ×1/ln 2 = ×1.44), and the book
   column is Williams & Carter's plain brightness divided by V\*, which carries no FW50 convention. Compared like for like
   (model `B_r` against book `B/V*`), the ratios become 2.4 (cold) and **0.37** (Schottky) (recomputed). Then the Schottky
   value falls outside a factor of two, not the cold one. A column builder checks this table first.

2. **3.5: the reader is told "the column can never raise brightness" (3.4) and then "B_pr = 1.4427 B_r" (3.8), with no
   sentence to reconcile the two.** A practical brightness above the peak phase-space density looks like a breach of
   Liouville. It is not: it comes from the definition (total current divided by the area of the *half-current* disk, so it
   counts current that lies outside that disk). The chapter says "our derivation shows where it comes from" and quotes
   Bronsgeest's "a surprising, new result". It never says why it is *not* a paradox. Problem 3 (the top hat gives ×2) is
   the clearest proof that it is only a convention, but it is left as an exercise.

3. **3.2, Example 3.1: a false statement.** "at 300 kV the electron is half-way between the two limits". The exact
   λ = 1.969 pm is *smaller* than both limits: the non-relativistic h/√(2meV) = 2.239 pm and the photon-like hc/eV = 4.133 pm
   (recomputed). The exact λ = hc/√(E_k² + 2E_k mc²) always lies below both. It is between nothing.

4. **3.3, Example 3.2: misleading on diffraction, and the real payoff of deceleration is never given.** "The wavelength
   grows from 17.3 pm in the column to 43.3 pm at the wafer, which is what sets the diffraction limit there." Both λ and α
   scale as 1/p. The angle grows by 2.505 and the wavelength by 2.505 (recomputed), so the diffraction disc ∝ λ/α is
   *unchanged* by the retarding field. That is the nicest physics in the section, and the text implies the opposite. The
   section also does not say what deceleration actually buys a column builder: lower aberration coefficients of the
   combined retarding-objective lens. "This is not a loss … a spot that is smaller in angle at the column energy is simply
   larger in angle at the wafer" mixes up spot (a size) and angle.

5. **3.3: "no lens action of the retarding field itself" is put as a modelling choice, but at the page's own numbers it is
   not small.** A retarding field has to begin and end somewhere, and where its strength changes along z it has a radial
   component E_r = −(r/2) dE_z/dz. That is an aperture lens. For Example 3.2 (5 kV to 800 V over, say, 1 mm), the
   Davisson–Calbick estimate f ≈ 4V/ΔE_z gives about 5 mm (my estimate, gap assumed). That is the scale of a working
   distance. So the angle factor (3.4) is not the whole story; a sentence and a number are needed. The limits paragraph of
   3.8 names "the overlap with the objective", but not this.

6. **3.4 (★): the Liouville derivation is too narrow for the claim it supports, and "exactly" contradicts a small-angle
   step.** The Hamiltonian H = −√(P² − (p_x − qA_x)²) has one transverse coordinate and drops the −qA_z term. A round
   magnetic lens has an azimuthal A that couples x and y (Larmor rotation), so "the second, y, is the same calculation" is
   wrong for the lenses chapter 4 will use. Only the 4-volume dx dy dp_x dp_y is conserved, not the x and y areas
   separately. Also, p_x there is the *canonical* momentum. It equals the kinetic momentum (and so gives the angle) only
   where A = 0, and the text never says so. Finally, dΩ = d²p⊥/p² is a small-angle step, yet D6 claims "B/V\* is the same
   at every plane of the column (exactly, relativistically)". The conclusion is right. The argument and the word
   "exactly" are not.

7. **3.5, Example 3.3: the "same spot" cannot exist at these numbers.** "Land at 800 V …, form a source image of d = 1 nm
   with α = 5 mrad, and (3.7) gives I_p = 15 pA". At 800 V, λ = 43.3 pm, so the diffraction disc alone is
   0.54 λ/α ≈ 4.7 nm FW50 (0.61 λ/α ≈ 5.3 nm) (recomputed). A 1 nm probe at 5 mrad and 800 V is impossible. The example has
   to say that d is the geometric source image only, or pick an α where it is consistent. A column builder sees this at
   once.

8. **3.5: an unsupported key claim.** "the virtual source of a field emitter has a Gaussian profile, brightest at the
   centre." The whole ×1/ln 2 rests on this. There is no reason given and no reference beyond the authors' names, yet the
   reason is in the chapter's reach: the exponential transverse-energy distribution of chapter 2 is a Gaussian in p⊥, and
   tracing back to the virtual source maps p⊥ onto position. One sentence would tie 3.5 to chapter 2. Also,
   "B_r = e j(ε_t=0)/π": `j` is never defined in this chapter. The gloss "the current from an infinitesimal area … into an
   infinitesimal solid angle" describes dI, not a brightness.

9. **Whole chapter: no reference list (STANDARD item 8).** Bronsgeest, Barth, Swanson and Kruit (2008) carry the central
   result (3.7)/(3.8), their "Eq. 6", "Eqs. 15 and 16", the factor 2 "upper limit" of Problem 3, and the 3×10⁸ threshold
   in 3.7. Williams & Carter carry the whole of 3.7. Neither has a journal, edition, page, DOI or link anywhere on the page.
   The only `.prefs` list on the page belongs to chapter 2 and contains neither. The data file
   `data/ch02/source_properties_williams_carter.csv` is named but not linked. "The librarian of this project digitised
   them" is an internal role a reader of a portfolio does not know.

10. **3.7: a threshold applied outside its stated range, and without units.** "Bronsgeest et al. note that for Schottky
    sources the interactions become important above a practical brightness of about 3×10⁸; … The cold source at
    3.13 × 10⁸ would sit above that mark". The number has no unit (A m⁻² sr⁻¹ V⁻¹ presumably). It is stated for Schottky
    sources and then used for a cold source. And "above" means 4 % above, inside the factor-of-two uncertainty the same
    paragraph asserts. Also, the model ΔE (0.215, 0.43 eV) and the book ΔE (0.3, 0.7 eV) are compared without saying
    whether either is a FWHM, a FW50 or an rms width.

Close behind: the simulation's drawing (S below) is unreadable at every width tried, and its caption says "Left … Right"
for a layout that is stacked top and bottom.

---

## Section by section

### Chapter lead
- "Liouville\\'s theorem" renders with a visible backslash ("Liouville\'s") at every width. It is a build escaping bug, in
  the first line a reader sees.
- The lead promises "the angle change when the beam is slowed before the wafer", but the angle change (3.4) is only part of
  what slowing does (see 4, 5).

**Verdict:** needs work (one typo).

### 3.1 The gun: a step in potential
- Picture: the marble on a smooth slide is good and earns its place (STANDARD 1 met).
- `E_0 = (γ−1)mc² = eV` (3.1). In relativity E₀ almost always means the rest energy mc². Using it for the kinetic energy
  will trip a graduate. Use `E_k` or `T`. Also, γ is defined in (3.1) but was used ("γmc²") a line earlier, with only a
  pointer to §1.5.
- "arrives where the potential is higher by V". The power supply fixes the difference of *Fermi levels* (electrochemical
  potentials), not of vacuum electrostatic potentials. These differ by the contact potential (work-function difference,
  a few volts). An electron at the tip's Fermi level reaches the anode with eV − W_anode measured from the anode's
  vacuum level. At 1 kV that is a few parts in 10³ in energy. Meanwhile Example 3.1 quotes V\* = 1000.98 V and a
  relativistic error of 0.049 %, which is ten times smaller. One sentence on the reference level is needed, or the extra
  digits should go.
- "an extractor … whose voltage V_ex pulls the electrons out by tunnelling". A voltage does not pull. It sets the apex
  field (via the tip radius and geometry of chapter 2), and the field thins the barrier. The next sentence says this
  better, so the first can simply be fixed.
- "The two knobs do different jobs." Largely true, but the extractor–anode gap is itself an electrostatic lens whose
  strength depends on V_acc/V_ex. It moves the virtual source and adds aberrations. 3.8 lists "the gun's own lens action"
  as left out; say it here in a clause, so the "different jobs" claim is not read as exact.
- The frame is never stated: the tip is at 0 and the anode at +V. Real columns usually ground the column and put the tip at
  −V. A column builder will translate this, but the student needs the sentence.
- Figure 3.1 (1400 px and 390 px): the extractor bar hides the F of "Fermi level" ("( ermi level)"). The retarding-plate bar
  runs through "wafer: U = −eV_land" ("waf r"), the eV_land arrow crosses that label, and the bar overprints "plate". The
  labels use raw ASCII underscores (`eV_acc`, `eV_land`) where the text has typeset subscripts.
- "Measured from the Fermi level, every electron then gains exactly eV; the spread is carried along unchanged." Clear and
  right; it sets up 3.6.

**Verdict:** needs work (symbol E₀, reference level of V, figure label collisions).

### 3.2 Momentum and wavelength, exactly
- The derivation of (3.2) is complete and every step is shown. Good Taylor-style work.
- "every non-relativistic formula of electron optics in which V stands for p²/(2me) becomes exact when V is replaced by
  V\*". Read literally this is a tautology. Read as intended it is too strong: the relativistic paraxial equation of an
  *electrostatic* lens has extra factors (1 + 2εV)/(1 + εV) multiplying V″. It is not just V → V\*. Restrict the claim
  to formulas that depend only on |p| (wavelength, magnetic rigidity, refractive index ∝ √V\*).
- "In every formula below, the beam voltage means V\*." But 3.6 then uses ΔE/(eV) with plain V, and the table in 3.8
  writes "B V\*". It is consistent in practice, but the rule should say energy *spread ratios* use eV.
- Example 3.1: all numbers check (recomputed: 1000.98 V, 38.76 pm, 1.02935, 1.05871, 6.979 pm, 3.701 pm, 1.969 pm,
  4.13 pm; one per cent at 20.5 kV). The final claim "half-way between the two limits" is false (item 3 above).
- Typesetting is mixed inside one example: "At 1 kV", then "At V = 30000 V", then "V = 3.00 × 10⁵ V".
- The limits check of (3.3) is good (STANDARD 4). But "Both limits are verified symbolically (check D2 in §3.8)" sends the
  student to a table instead of showing the one line (for x ≪ 1 the bracket → 1; for x ≫ 1, p → eV/c).

**Verdict:** needs work (one false sentence, one over-strong claim).

### 3.3 Landing softly: deceleration before the wafer
- The motivation paragraph (stiff fast beam, gentle slow beam) is a real physical picture. The ball rolling up a ramp
  that keeps its sideways push is apt.
- "the lens aberrations that grow with the relative energy spread ΔE/E (chapter 5) are smaller". Smaller *where*? The
  reader needs to be told that the objective's chromatic blur goes with ΔE/E at the energy *inside the lens*. That is why
  running fast and landing slow helps. Without it, the student cannot see why one would bother.
- (3.4) uses tan α = p⊥/p_z and p_z ≈ p. The exact statement is sin α_land / sin α = p_acc/p_land: the electron-optical
  Snell's law with refractive index ∝ √V\*. Naming it would give the graduate the picture (refraction at a potential
  step) and make the small-angle step explicit.
- "(check D4). A beam slowed down opens up." The sentence starts with a parenthesis. That is a layout artefact.
- "a spot that is smaller in angle … simply larger in angle at the wafer". A spot has a size, a beam has an angle.
  Rewrite.
- Example 3.2: numbers check (2.51; 17.30 and 43.34 pm; 1.118, recomputed). "which is what sets the diffraction limit
  there" is misleading, because λ/α is invariant (item 4).
- The model paragraph is honest ("paraxial, uniform field, no fringe fields, no lens action"). It needs one number to show
  how big the neglected aperture lens is (item 5).
- The text, Figure 3.1 and "retarding plate" all assume V_land < V_acc. The simulation lets V_land run above V (0.496 kV
  gun, 17.0 kV landing: α_land/α = 0.170). That is a booster, not a retarding field. Either clamp the slider or say in
  one sentence that the same formula covers acceleration after the column.

**Verdict:** needs work.

### 3.4 Brightness, and why the column cannot raise it ★
- The magnifying-glass picture is right and well chosen.
- **The whole section is starred, including the definition of B (3.5), the definition of B_r (3.6) and the Key result
  box.** Numa's rule: "the results of any starred passage are restated unstarred". A student who skips ★ arrives at 3.5
  without the definition of brightness or reduced brightness, and 3.5 uses both on its first line. Star only the
  Hamiltonian passage, or restate (3.5), (3.6) and the key result outside it.
- The Hamiltonian is too narrow for "every plane of the column, whatever lenses" (item 6). Also "P(x,z) is the total
  momentum the potential allows at that point" is used without a formula. Give P = √[(E − qφ)²/c² − m²c²].
- The step from "dA d²p⊥ is conserved" to "B/p² is conserved" leaves out the sentence that does the work: the *same*
  electrons, hence the same dI, pass through the patch at both planes, so B = dI/(dA dΩ) = dI p²/(dA d²p⊥) ∝ p². D6's
  detail "B/p² = dI/K" names this with an undefined K.
- "A flow with no divergence … can be stretched into a long thin streak (a focus)". A focus is narrow in x and wide in
  p_x, an upright ellipse. Figure 3.2's "plane 2: a focus, same area" is the plane-1 ellipse rotated by 65° (SVG:
  `rx=22 ry=90 rotate(-25)`). It is tilted, which shows a converging or diverging beam, not a waist. Draw the waist
  upright, or relabel it "after a lens". The caption's "A lens shears and rotates the patch" is fine. Axis labels are raw
  `p_x`.
- "Without collisions between the beam's electrons". The smooth mean-field part (space charge) does conserve phase-space
  density. Only the stochastic part (Boersch, trajectory displacement) does not. "Collisions" is the right word only if
  that is what is meant; say so, because 3.8 lists "space charge" among the violators.
- "This is why chapter 2 spent so long on the tip." A good closing line.

**Verdict:** needs work (★ placement breaks the skip rule; derivation narrower than its claim; figure mislabelled).

### 3.5 From brightness to probe current
- First sentence: `j` is undefined here, and the gloss describes a current, not a brightness (item 8).
- "the virtual source of a field emitter has a Gaussian profile". Unsupported, though derivable from chapter 2 (item 8).
- (3.7): the derivation of the Gaussian-to-FW50 factor is clean and short, and a school student can follow it. But (3.7)
  itself is quoted, not derived, and it hides an assumption: the current is spread *uniformly* over the cone πα². That
  holds because the aperture takes a small central part of a broad emission cone. Say it.
- The meaning of B_pr > B_r is not explained, against 3.4's "can never raise it" (item 2).
- "It holds as long as the electrons do not push each other between the tip and the extractor." Good, and it is the right
  limit.
- Example 3.3: I_p = 15.46 pA and 96.5 electrons per µs (recomputed). The factor 13 and the 1.2 pA check. The geometry is
  physically inconsistent with 800 V (item 7).
- "Chapter 7 shows that a few thousand electrons per pixel are needed" and "the trade-off of chapter 0" point forward to
  a chapter marked "In preparation". To a reader today it is an unsupported claim. Give the number with its reason (shot
  noise: an edge contrast C needs N ≳ (k/C)² electrons, the Rose criterion) or drop it.

**Verdict:** needs work.

### 3.6 Energy spread through the column
- The argument (each electron gains eV, so differences are kept) is complete and simple. The numbers check (2.15×10⁻⁴,
  2.69×10⁻⁴).
- ΔE is not defined as FWHM, FW50 or rms, here or in the 3.7 table. Chapter 5 will multiply it into a chromatic blur, and
  the convention changes that blur by a factor of order 1.5 to 2.
- "Both grow with the current and are the reason why practical brightness stops rising at high emission current." The
  Boersch effect widens the *energy* distribution. Only trajectory displacement (lateral) lowers brightness. Say which one
  does what.
- "the numbers here are lower bounds". Agreed, and supply ripple (named in 3.8) belongs in the same sentence.

**Verdict:** clear apart from the missing width convention. Small fix.

### 3.7 The model next to published source data
- Items 1, 9 and 10. Also:
- "Williams and Carter (Transmission Electron Microscopy, ch. 5, Table 5.1)" gives no edition or year. Table numbering
  differs between the 1996 and 2009 editions.
- "They are round textbook numbers, good to a factor of about two". Whose estimate is "a factor of about two"? If it is
  the author's, say so. If it is the book's, cite the page.
- "That is the direction we expect: … the book's values belong to operating guns, which add the Boersch broadening". This
  is plausible and labelled as expectation, which is fine. But a cold-FE spread of 0.3 eV and an intrinsic 0.215 eV FWHM
  would need *some* number for the Boersch addition, or a vendor or paper value, to count as a check rather than a story.
- For a column builder, one modern measured value (cold FE B_r of order 10⁸–10⁹, Schottky about 10⁸ A m⁻² sr⁻¹ V⁻¹, from a
  paper the author has opened) would carry more weight than a textbook table of round numbers. As it stands, the only
  external check of the chapter's headline number is a factor-of-two table that the text misreads.

**Verdict:** needs work (the conclusion does not follow from the table).

### 3.8 Checks, hand-over and limits
- The check table is a good idea and is honest about what each check verifies. But:
  - D3 detail prints raw SymPy: "-x\*\*2/32 + x/4 + 1"; D7 prints "1/log(2)" and ends in a dangling "= 1.4427 ×".
  - D3 writes "√(1 + eV/2mc²) = 1 + eV/(4mc²) − …": a series needs ≈ or "+ O(x³)".
  - D6: "exactly, relativistically" (see item 6), and K is undefined.
  - D5: "for arbitrary P(x, z) and A(x, z)". Only A_x(x, z) is in the Hamiltonian (item 6).
  - The table uses raw underscores (α_land, p_acc, V\*_acc, I_p) instead of typeset subscripts.
  - At 390 px the table scrolls sideways and the "detail" column is cut off at the right edge, with no visible cue
    (`.ptab-wrap` 516 px in a 358 px box, measured).
- "they agree to the last bits of a 64-bit number (the parity check states a tolerance of 10⁻¹⁴)". 10⁻¹⁴ is about 45 ulp
  at unit size, not "the last bits". Say "to 10⁻¹⁴ relative".
- STANDARD 5 (numerical method): the chapter evaluates closed formulas only, so a short statement that there is no
  integrator, and that every number is a closed-form evaluation, would settle it. The paragraph nearly says this.
- Hand-over: lists V\*_acc, V\*_land, λ, the angle factor and (3.7). Missing are the source-image (virtual source) size and
  the ΔE convention, which chapter 5 needs as much as B_pr.
- Limits: a good list. "The next, more complete model would trace electrons through a computed gun field with their
  mutual forces (a Monte Carlo of Coulomb interactions)" names the next model, as STANDARD 7 asks.
- Problems: well chosen. Problem 3 should be promoted to one sentence in 3.5 (item 2). Its "which is the upper limit
  Bronsgeest et al. quote" needs the reference (item 9).

**Verdict:** needs work (presentation of the check table; two overclaims inside it).

### S Simulation · Acceleration and landing (`#sim-ch03`)
- At 1400 px and at 390 px the stage stacks the gun drawing *above* the wavelength plot. The caption says "Left: the gun
  drawn … Right: the electron wavelength". That is wrong at both widths tested.
- The gun drawing is a strip about 60 px high. The labels "extractor", "anode: +1000 V" and "wafer: lands at 800 V"
  overprint the plates and each other, and the "wafer" label sits on the middle plate, not the bottom one. The beam is
  drawn as a "W" rising from the apex to the extractor plane and fanning out sideways. It does not show "the beam
  narrowing to the anode and opening again if it is slowed". At 8.85 kV / 0.80 kV, where α_land/α = 3.34, nothing in the
  drawing visibly opens.
- At the default (1 kV, 800 V) the "column" and "landing" markers on the λ plot coincide, and their labels overprint into
  an unreadable "leolumn". The legend text "λ without relativity (dashed)" runs across the curve. The plot has no y-axis
  title. The dashed non-relativistic curve separates from the exact one only above about 100 kV, so on the default view
  the reader cannot see the effect the readout boxes report.
- The readouts are right (1.00 kV, 38.8 pm, 43.3 pm, 1.12; also 8.93 kV, 13.0 pm, 3.34; all recomputed). But "V\* 1.00 kV"
  to three figures hides the 0.1 % correction that is the point of V\*. Four or five significant figures, or showing
  V\*/V, would make the box say something.
- The landing slider exceeds the gun voltage without comment (see 3.3).
- STANDARD 6 (equation to screen): there is no paragraph saying which drawn element is which symbol, or where the drawing
  departs from the model (no field, no trajectories integrated: it is a cartoon).

**Verdict:** needs work. As it renders it weakens the chapter for a reader judging an applicant.

---

## Summary of verdicts

| section | verdict | main reason |
|---|---|---|
| lead | needs work | "Liouville\\'s" typo |
| 3.1 | needs work | E₀ for kinetic energy; reference level of V vs quoted digits; Fig. 3.1 label collisions |
| 3.2 | needs work | "half-way between the two limits" false; V→V\* claim too strong |
| 3.3 | needs work | λ/α invariance missed and contradicted; aperture-lens effect not sized; payoff of deceleration unstated |
| 3.4 ★ | needs work | definitions and key result only inside ★; 1-D Hamiltonian vs magnetic lenses; "exactly" vs small angle; Fig. 3.2 "focus" |
| 3.5 | needs work | B_pr > B_r not reconciled with Liouville; Gaussian virtual source unsupported; `j` undefined; Example 3.3 below diffraction limit |
| 3.6 | nearly clear | width convention of ΔE; Boersch vs trajectory displacement |
| 3.7 | needs work | text contradicts table; B_pr compared with B/V\*; threshold misapplied, unitless; no references |
| 3.8 | needs work | raw SymPy in table; D5/D6 overclaims; no Further reading |
| simulation | needs work | caption wrong for layout; drawing unreadable; overprinted labels |

STANDARD items across the chapter: 1 picture met (marble, ramp, magnifying glass, ink drop). 2 model stated per section
(good). 3 derivation mostly complete, with gaps at 3.4 and 3.5. 4 checks present (limits, symbolic table) but two checks
overclaim. 5 not applicable, yet not said. 6 missing for the simulation. 7 limits met. 8 **missing**: chapter 3 has no
reference list.
