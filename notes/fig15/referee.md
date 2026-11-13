# Fig. 15 · Resonant Tunnelling — referee report

Read as its two target readers (a maths-strong school student; a first/second-year physics
undergraduate), rendered and screenshotted section by section in headless Chromium from
`public/scripts/resonant-note.js` injected into `public/simulations/resonant-tunnelling.html`.
Judged against `notes/STANDARD.md` (section 4, and the 21 October "write it like a chapter of
Taylor" verdict).

## Overall

This is a strong note. It renders cleanly (KaTeX, the SVG figure, the tables and boxes all
display correctly). It does what the STANDARD asks: it motivates from everyday experience
(glass panes, an echo ringing between two walls), states the model and natural units, carries
the one running example E=1, V0=3, d=1 all the way through, sets key results apart in boxes,
gives numbered worked examples with the page's own numbers, and ends with a Problems box and
real, cited references. The voice is calm and Taylor-like, with almost none of the banned AI
tells (no rhetorical questions, no "it is not X, it is not Y", no stacked em-dashes). The
physics is, as far as I checked by hand, correct.

The problems below are therefore mostly local: two genuine content gaps (a number a reader
cannot reproduce in §6, an undefined symbol in §9), a figure-label inconsistency in §1, and a
handful of smaller skipped steps and polish items. None of them sink a section; several are
worth a one-line fix.

## Ranked — the places a reader gets lost or the writing drags

1. **§6, the energy-spread numbers do not reproduce and do not scale.** Sentence (Key-result
   box): *"a short pulse (σ₀=3, energy spread ≈0.12, far wider than Γ=0.040) transmits only
   T̄=0.10. Lengthen the pulse to σ₀=12 (spread ≈0.06) and T̄ rises to 0.33."* The text's own
   rule is "a Gaussian of width σ₀ in space is a Gaussian of width 1/(2σ₀) in k". From that,
   Δk = 1/(2σ₀) = 0.167 (σ₀=3) and 0.042 (σ₀=12); converting with ΔE ≈ k₀Δk, k₀=√2, gives
   ΔE ≈ 0.236 and 0.059. So the σ₀=12 value (0.06) matches, but the σ₀=3 value should be ≈0.24,
   not 0.12 — and the two quoted spreads (0.12, 0.06) differ by a factor 2 while σ₀ differs by a
   factor 4, so they cannot both follow the stated 1/(2σ₀) rule. A maths-strong reader who does
   the arithmetic the note invites gets a contradiction. Either give the formula that produces
   0.12 or correct the number.

2. **§9, the Fermi energy E_F is used but never defined.** It appears in the central device
   equation (15), the Tsu–Esaki formula, and again in Problem 4 ("raising E_F"), yet the prose
   never names it. The reader meets `e, m*, k_B, T` (all defined or standard) and then an
   undefined `E_F`. The sentence *"pulling the trapped level down through the sea of electrons
   that feed it from the left"* gestures at the Fermi sea but never says "the Fermi level E_F,
   the top of the filled electron states". One clause fixes it.

3. **§1, the figure labels `s` on the gap, but defines `s` as centre-to-centre.** The caption
   says *"their centres a distance s apart"* and the whole note uses "well width s−d"
   (=1.343), which only makes sense if s is centre-to-centre. But in the SVG the `s` arrow runs
   from x=296 to x=424 — the inner faces of the two barriers (barriers span 250–296 and
   424–470), i.e. the gap, whose width is s−d, not s. A careful reader looks at the arrow
   touching the two inner walls, reads "s", and then cannot square it with "centres a distance s
   apart" or with "well width s−d". The figure code is out of bounds, but the caption should at
   least say the arrow marks the well, or the arrow should reach the centres.

4. **§4, "the phase e^{iks} it picks up crossing the gap s".** Two snags for a physics-grad
   reader. First, s is not the gap (the gap is s−d), so "crossing the gap s" is wrong wording.
   Second, and deeper: a wave physically crosses a region of width s−d at wavenumber k₀, picking
   up phase k₀(s−d), yet the formula uses e^{iks}. The resolution is that t and r must be
   defined with their phases referenced to the barrier centres, so the extra phase is absorbed —
   but the note never says where the single-barrier t, r are phase-referenced, so the reader
   cannot see why e^{iks} (and not e^{ik(s−d)}) is right. One sentence fixing the phase
   convention would close the gap.

5. **§3, the key single-barrier result (8) is asserted, not derived.** The section is titled
   "One barrier: matching, the transfer matrix, and T" and is starred, so heavier algebra may be
   skipped — but it hands the reader (7) T=1/|w|² and then (8) T(E)=[1+V₀²sinh²(κd)/4E(V₀−E)]⁻¹
   with only *"carrying the matrix product through … yields the closed form"*. The matrix
   entries w, z are never written in terms of E, V₀, d, so the reader cannot connect (7) to (8),
   and (8) — the single most-used formula in the note — arrives as a quoted answer. A physics
   grad who wants to follow is effectively told "it can be shown". At minimum give |w|² explicitly
   so (7)→(8) is checkable.

6. **§5, "Γ=0.040 gives τ=1/Γ=25.1".** 1/0.040 = 25.0 exactly; the 25.1 comes from the true
   Γ≈0.0398, which has been rounded to 0.040 in the display. A sharp student does the division
   and finds 25.0, not 25.1. Either show Γ to another digit or write τ=25.0.

7. **§5, the jump (9)→(10) is not shown and Γ is never given a formula.** *"Expanding the
   denominator of (9) about the resonant energy E_r gives a Lorentzian"* — the expansion is
   skipped and Γ is only ever an operational FWHM (measured, =0.040). That is acceptable for the
   level, but the intuition built in §4 ("the denominator nearly vanishes") is never tied
   quantitatively to how *narrow* the peak is, so "sharp because the barriers are opaque" stays a
   slogan. A line relating Γ to r (or to t, the leak rate) would pay off the §4 setup.

8. **§8 reads inward, toward the project rather than the reader.** *"the honesty of the pipeline
   is the point"*, `recon.py`, *"every file names its parents … by their SHA-256, so its
   provenance is traceable"*. The STANDARD does ask for "the numerical method as the code really
   does it" and "equation to screen", so the section belongs — but the provenance/SHA-256
   bookkeeping is about the website, not about resonant tunnelling, and it sits between §7
   (many barriers) and §9 (the device), interrupting the physics thread. A reader after the
   physics skims or stalls here. Consider trimming the provenance sentence to the physics-relevant
   checks (Crank–Nicolson agreement, probability conservation).

9. **§9, "A bias voltage V tilts the whole landscape".** "landscape" is on the STANDARD's list
   of AI-tell words to avoid. "tilts the whole potential" says the same thing and is cleaner.

10. **φ is reused for two different things.** In §6 it is the packet's amplitude in k, φ(k); in
    §10 it is the metal work function φ. Taylor's "one symbol, one meaning" is mildly broken.
    The sections are far apart so no reader is confused mid-sentence, but a different letter for
    one of them would be tidy.

## Verdicts by section (against STANDARD §4)

- **§1 Two panes of glass — clear, leave the prose.** Excellent everyday-first motivation
  (Fabry–Pérot, the ringing echo with a lifetime). One defect: the figure's `s` arrow marks the
  gap while the caption defines `s` centre-to-centre (item 3). Caption-level fix only.

- **§2 The model + running example — clear.** Schrödinger equation stated, separation of
  variables shown, natural units justified, k and κ derived with the running numbers (κ=2,
  e⁻²≈0.135, 1/κ=0.5). Meets items 1–2 and the start of 3 well.

- **§3 One barrier (★) — needs a small fix.** Matching conditions well motivated (the
  "χ′ infinite" argument is exactly right). But the transfer-matrix product is never carried
  out and (8) is quoted (item 5). For a starred section this is borderline-acceptable, but the
  title promises a derivation the section does not deliver; give |w|².

- **§4 Two barriers, two ways — clear and the highlight of the note.** The path-sum / geometric
  series is the right pedagogy and Example 4.1 (the bounces accumulating to 99.7%) is a genuinely
  good worked example. Only the "phase e^{iks} crossing the gap s" wording needs the
  phase-convention clause (item 4).

- **§5 The sharp peak and trapped state — mostly clear.** Breit–Wigner stated, τ=ℏ/Γ with the
  lovely two-roads check (Γ from the energy curve, τ_fit from the time decay, both 25.1). Fix the
  25.0/25.1 arithmetic (item 6) and consider a line giving Γ a home (item 7). The music-note /
  excited-atom analogy at the end is apt and not overlong.

- **§6 A wave packet is not a single energy — clear in spirit, one number wrong.** This is the
  honest, distinctive section (peak is 100%, packet is less) and it earns its place. But the
  σ₀=3 energy spread is not reproducible from the stated rule and is inconsistent with the σ₀=12
  value (item 1) — the one real content error in the note.

- **§7 Many barriers (★) — clear for a starred section.** Cayley–Hamilton → Chebyshev → bands and
  gaps is correct and nicely compressed; the "two-cell baby of a superlattice" line lands. The
  transmission in terms of U_N is never written, so "hinges on ξ(E)" is asserted, but that is
  within the licence of a ★ section whose result (bands vs gaps) is restated plainly.

- **§8 From data to data — serviceable but drifts.** Satisfies items 5–6 (how the figure is
  built, equation-to-screen, the Crank–Nicolson cross-check, probability staying 1.000), but the
  provenance/SHA-256 material is project bookkeeping that interrupts the physics flow (item 8).

- **§9 The device — clear, with one undefined symbol and one banned word.** The NDR mechanism
  (level swept down through the Fermi sea, current rising then falling) is explained well and the
  GaAs unit-conversion table is exactly the "put the nanometres back" the STANDARD wants. But
  E_F is undefined (item 2) and "landscape" should go (item 9).

- **§10 A triangular barrier (★) — clear.** Good tie to field emission and the Electron Beam
  project; Fowler–Nordheim quoted and the Airy-function exact solution named. Appropriate for a
  closing starred section. (φ reused as work function — item 10.)

- **§11 Limits + Problems + references — clear and exemplary.** Honest list of what the
  one-electron, 1-D, coherent, rigid-barrier model drops; next models named (NEGF,
  Schrödinger–Poisson). The four Problems use the page's own numbers and build on the derived
  equations. References are real, specific and each carries its role.

## Reading quality

Does it motivate from experience first? Yes. Does it carry the running example throughout?
Yes, consistently (E=1, V0=3, d=1; κ=2; one-barrier T=6.3%; resonance at s=2.343; Γ=0.040;
τ=25.1; and the GaAs translation in §9). Does it read top-to-bottom like Taylor? Largely yes;
the only structural wrinkle is §8 sitting between the physics of §7 and §9. Nothing is
seriously over-long or repetitive — the glass/echo/ringing motifs in §1 build rather than
repeat, and the boxes and examples earn their space.
