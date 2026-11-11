# Ledger of the book: what each chapter opens with, introduces, promises and hands over

Kept by V (voice session). Written in step 0 from the text as it stood on `eb/finisher` (5455de1); each chapter's entry is updated
when V hands that chapter over. V reads this file before editing every chapter. Term definitions and their places: `TERMS.md`.

## ch00 · The goal
- **Opening picture.** A chip of billions of switches, one bad one spoils it; reading a coin in the dark with a fingertip (too wide)
  against a needle (the electron beam).
- **Terms introduced.** pitch, half-pitch, numerical aperture, Abbe limit, de Broglie wavelength (formula quoted, derived in ch01),
  beam half-angle α (named), shot noise (picture), brightness (named), landing energy, cold field emission (quoted), BSE (named).
- **Promises.** ch01 derives the wavelength formula (§1.5); ch04–05: electron lenses are worse than glass; ch05 balances diffraction
  against aberrations; ch06: ions damage, electrons mostly do not; SE carry shape, BSE material; ch02–08 follow the trade-offs of
  spot, current, gentleness and speed quantitatively; the physics must explain why a cold tip is bright but fragile, why 10⁻⁹ Pa
  matters, why a high-energy mode sees deeper.
- **Hand-over.** The road table (now subjects, not questions); last sentence "We start with the electron itself."
- **Voice pass (6ffc3a8).** Beam half-angle α defined in §0.3 ("the half-angle of the cone in which the beam converges on the
  wafer"); shot noise and brightness named in §0.4; the four demands now one paragraph, their link through the source a second.

## ch01 · The electron in given fields
- **Opening picture.** A bar magnet bent the picture of an old cathode-ray television; Thomson's tube.
- **Terms introduced.** cathode, anode, $V_a$, point particle, Lorentz force, Lorentz factor γ, ε = eV/mc², Lagrangian, action, proper
  time, canonical and kinetic momentum, Hamiltonian, electronvolt, gyroradius, cyclotron frequency, helix, Helmholtz pair, RK4, Boris
  pusher, phase error.
- **Promises.** ch04 uses the canonical momentum and the helix (seed of the magnetic lens); ch03 turns the energy relation into the
  gun; ch04 traces rays with the integrator; ch05 returns to space charge; ch02 describes the real cathode's spread.
- **Hand-over.** Box "Hand-over to chapter 2": force law, energy relation, steppers, helix; chapter 2 supplies the other end of the
  column, "a stream with a current and a brightness".
- **Voice pass.** The guiding problem stated, not asked ("where a single electron goes when the fields are known"); gyroradius
  given its meaning at first use in §1.2; "electronvolt" (one word) as in ch02; Thomson's own causes in a paragraph of their own;
  problems phrased as tasks. Last paragraph unchanged in content: the hand-over box to chapter 2.

## ch02 · The source
- **Opening picture.** Every beam starts at a piece of metal; the spark from a fingertip on a dry winter day, the lightning rod; the
  work function as the rim of a bowl of water.
- **Terms introduced.** Fermi level, work function, the three emission kinds, apex field and $k$, image force, Schottky–Nordheim barrier,
  scaled field, Schottky lowering, WKB exponent and transmission, $v(f)$, $t(f)$, $s(f)$, supply function, normal and transverse energy,
  Fowler–Nordheim equation, decay width $d$, voltage conversion length, FN plot, Richardson–Dushman, total-energy distribution, energy
  spread ΔE (FWHM), brightness, reduced brightness $B_r$ (as B/V), virtual source $d_v$, Hertz–Knudsen flux, coverage, Langmuir
  kinetics, flash cleaning, cold and Schottky presets, working point.
- **Promises.** ch03 proves the conservation of $B_r$ (Liouville) and compares published brightness; ch05 turns ΔE into the chromatic
  blur; the one-atom claim of Applied Materials is a stated limit.
- **Hand-over.** Table of four numbers to chapter 3 (I_e, B_r, ΔE, d_v) for the two presets; limits; checks; problems; sources.
- **Voice pass.** The electronvolt now a pointer to chapter 1; brightness and reduced brightness set in italics at their
  definition (§2.8); the decay width $d$ named and given its meaning (the transmission falls by e per $d$ below the Fermi
  level); "your screen", "you move" and the one "I" removed; the long vacuum, Schottky-preset, residence-time and patch-model
  sentences split. No typed numeral added (checks/list_legacy_numerals.py before and after).

## ch03 · Acceleration, brightness, energy spread
- **Opening picture.** A marble let go at the top of a smooth slide.
- **Terms introduced.** extractor and $V_\mathrm{ex}$, $V_\mathrm{acc}$, $V_\mathrm{land}$, $V^*$ (beam voltage), retarding field,
  Liouville's theorem, $B_r=B/V^*$ exactly, practical brightness, FW50, probe current $I_p$, Boersch effect.
- **Promises.** ch05: chromatic blur ∝ ΔE/eV; ch07: a few thousand electrons per pixel; ch04: the retarding field and the objective
  overlap (outside the project).
- **Hand-over.** "What chapter 4 and chapter 5 receive": $V^*$, the angle factor, $I_p$ with $B_\mathrm{pr}=B_r/\ln2$.
- **Voice pass.** Opening now ties the marble to "the electrons that chapter 2 drew from the tip"; brightness and reduced
  brightness are pointers to chapter 2 (reduced brightness "now exact, with the beam voltage in place of $V$"); "beam voltage"
  named at the definition of $V^*$; FW50 and probe current marked at their definition (§3.5); the two rhetorical questions
  removed; a duplicated sentence in §3.7 removed.

## ch04 · The lens
- **Opening picture.** The helix of chapter 1 shortened to a coil in an iron shell; the convex glass lens.
- **Terms introduced.** axial field $B(z)$, Glaser's bell field, Busch's theorem, Larmor rate, paraxial ray equation, η, image rotation,
  lens strength $k^2$ and ω, focal length, objective, working distance, magnification, $C_s$, $C_c$, Scherzer's theorem, Airy disc.
- **Promises.** ch05 chooses the beam angle to balance diffraction against the aberrations.
- **Hand-over.** "What chapter 5 receives": $C_s$, $C_c$ at the wafer; $M$ reported but not handed on.
- **Voice pass.** Opens with "The beam that leaves the gun of chapter 3 must now be focused into a spot"; the radial field
  $B_r$ is told apart from the reduced brightness at first use (doubt 2 answered in prose, maths unchanged); the solver's
  integrator is "the RK4 method of chapter 1"; the comma splice in Example 4.1 fixed; the aberration measurement told step by
  step. Ex. 4.3 still ends "chapter 5 shows how the beam angle is then chosen to balance diffraction against these blurs".

## ch05 · The spot
- **Opening picture.** Sunlight focused by a magnifying glass makes a dot, never a point.
- **Terms introduced.** source image $d_I$, disc of least confusion, root-power sum, $d_p$, $d_A$, $d_S$, $d_C$, $\Delta E_{50}$,
  optimum angle, CD-SEM (with CD named forward to ch07).
- **Promises.** ch06 measures the deeper, harder hit at 30 kV; chapter 7 defines CD.
- **Hand-over.** "What chapters 7 and 8 receive": $d_p$, $I_p$, the angle.
- **Voice pass.** Brightness, reduced brightness, beam voltage and FW50 are now reminders with pointers to chapters 2 and 3,
  not second definitions; the diffraction wavelength sentence untangled ({{num:lam800}} pm belongs to λ, not to $V^*$);
  long sentences on chromatic blur, the checked coefficients, published lenses and image resolution split.

## ch06 · Scan and hit
- **Opening picture.** Marbles thrown into a box of heavier balls.
- **Terms introduced.** elastic/inelastic collision, BSE and η, SE and δ, Monte Carlo, scanning, field of view, pixel, dwell time,
  cross-section, impact parameter, screening parameter, elastic mean free path, Sommerfeld parameter, Mott cross-section, stopping
  power, mean ionisation energy, plasmon, escape depth, universal yield law, Kanaya–Okayama range, $r_{90}$, interaction volume,
  lateral spread, core width, core fraction, halo width.
- **Promises.** ch07 counts the electrons of a pixel; ch07 blurs edges with core and halo.
- **Hand-over.** "What chapter 7 receives": δ, η, core width, core fraction, halo width, with errors.

## ch07 · Detect and measure
- **Opening picture.** A metrology tool reading a width over and over; lines look like their own outlines.
- **Terms introduced.** CD, secant law, sidewall angle, expected profile, shot noise law, collection fraction, SNR of one line, dose,
  threshold rule, floor level, bias, $\sigma_\mathrm{CD}$, error propagation and Monte Carlo check, $N$ lines, overhead, measurements per hour.
- **Promises.** ch08 joins everything.
- **Hand-over.** "What chapter 8 receives": $\sigma_\mathrm{CD}$, bias, dose, rate as functions of all inputs.

## ch08 · The whole machine
- **Opening picture.** A long train of gears; a slip at the first gear passed on to the last.
- **Terms introduced.** normalised sensitivity, tolerance Monte Carlo, measurement window (process window of lithography as picture).
- **Hand-over.** Checks and limits; no explicit bridge to ch09.

## ch09 · The column in one view
- Prose summary with pointers; no new terms. Last paragraph: the misread Airy coefficient and "checking against the physics".

## guide · Reading guide (four boxes above chapter 0)
- shows, models, leaves out, numbers.

## Doubts (physics or claims; listed, not fixed)
1. ch06 §6.7: "The range grows almost as the square of the energy." The Kanaya–Okayama law quoted just above has the exponent 1.67,
   and ch09 says "roughly as its five-thirds power". AUDIT §8 records this as fixed, but the sentence is still in ch06. Coordinator to decide.
2. ch04 §4.1–4.2 uses $B_r$ for the radial field component, the same symbol as the reduced brightness of ch02, ch03, ch05 and ch08.
   Inside maths; not changed. Since the ch04 voice pass the prose says so at first use.
3. ch02 §2.8 defines $B_r=B/V$ ("non-relativistically"), ch03 §3.4 $B_r=B/V^*$. Consistent (ch02 says chapter 3 shows it), noted for
   the guard.
4. ch07 calls the contrast-to-noise ratio "SNR". Name inside text and maths; left.
