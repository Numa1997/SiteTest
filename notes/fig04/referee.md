# Fig. 4 · referee report

Note: "Transverse and longitudinal waves: the pattern travels, the medium stays", in
`public/simulations/Transverse and longitudinal waves.html`. I read it as two readers at once: a school student who is
good at mathematics, and a physics graduate. The yardstick is `notes/STANDARD.md`, above all "Numa's verdicts": a clear
section is left alone. I did not read `plan.md`, `check.md` or any teacher report.

**How I read it.** I built the site with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig04-ref-dist npm run build` (the built page is
byte-identical to the source) and served it with a small Node static server. I opened it in headless Chromium 1194 at
1440 × 900, pressed *Expand all* (no fold stayed closed) and took screenshots of each section into `shots/`. Then I read
the rendered text, with KaTeX turned back into its TeX. There were no KaTeX errors, no console errors and no failed
requests. The fonts loaded are Instrument Serif 400, IBM Plex Sans and Mono, Latin Modern and KaTeX. One extra
screenshot, `p-energy-eq15.png`, shows equation (15), which the paged shots had hidden under the pinned header.

**What I checked against the page.**
- Every number quoted in the note, recomputed:
  - Ak = 0.7426, Aω = 81.7 px/s, atan(Ak) = 36.6°;
  - density 3.884 and 0.574 at the defaults; the denser half fills 26.4 %;
  - first-frame gaps 7.01 to 44.15 px;
  - the cap is 28.01 px at λ = 220 px, 14.0 px at 110 px and 12.7 px at 100 px;
  - the closest pair in Exercise 5.1 is 3.86 px;
  - a mass–spring chain is slower by 2.2 % (ratio 0.9779);
  - ρ_air = 1.2043 kg/m³ and v = 343.2 m/s.
- The canvas, measured: 770 × 481 at 1440 px and 356 × 374 at 390 px, so s = 1.134 and s = 0.4875.
- The readouts at the defaults: "110 px/s", "2.00 s", "26 px". The readout puts "(cap)" after the value when A_L < A.
- In the code: the time step is clamped at 0.05 s (`sim.js`); the reduced-motion start is paused; Frequency tops out at 2 Hz.
- The drawing constants: radii 4.5, 6.5 and 4 px; bar 56 px; band 68 px; 215 curve points; 65 gradient stops; 8 px crest
  offset.
- The sampling of the figures: Fig. 2 every 2.5 px and every 0.025 s, Fig. 3 every 0.025 s, Fig. 4 every 1 px.
- The four further-reading links. Feynman I-47 returns 403 to curl, which blocks bots, and 200 through Firecrawl; the
  other three return 200 directly.

All of these agree with the note. The physics is correct throughout. What follows is about the reader.

Legend: **(A)** a real obstacle, which counts toward the verdict · **(B)** taste · **(C)** overloaded: longer or heavier
than its point needs.

---

## 01 · The pattern travels, the medium stays

**(A)** None.

**(B)**
- "This is how we know that the Earth’s outer core is liquid metal." The S-wave shadow shows that the core is *liquid*.
  That it is *metal* comes from other evidence (density, the magnetic field). This is harmless in a picture section.

**(C)** None. Five short pictures: the stadium, the slinky, the guitar, the earthquake and the simulation. Each one is used
later.

**Verdict: clear.**

---

## 02 · The model

**(A)**
1. **A paragraph that contradicts the assumption list right after it, in words a school student does not have.**
   > "The page prescribes particle positions with a sinusoidal formula. The wave equations derived below describe small
   > slopes or small compression. The default wave is deliberately large: in the lower row, whose amplitude A_L equals A
   > at the default settings (Section 5 gives the rule), A_L k ≈ 0.743, so at the compressions neighbours close to about
   > a quarter of their rest spacing. The exact density follows from the map x = X + ξ, but this does not make that
   > prescribed motion a solution of nonlinear sound dynamics."

   The very next line is the first assumption: "The displacements are small enough for the medium to respond linearly:
   twice the push, twice the displacement." The reader is told in one breath that the model assumes small displacements
   and that the default wave is deliberately large. Nothing tells them which to believe, or what the large default means
   for what they see.
   - The words that carry the resolution are undefined for the target reader: "prescribes", "the map", "nonlinear sound
     dynamics", and "the wave equations derived below", which are not derived yet.
   - "Deliberately" is never explained. Presumably the large default is there so that the bunching shows.
   - A graduate can decode it: the page draws a kinematic formula, which is exact at any amplitude, while the physics
     behind it holds only for small slopes. A school student is lost here, and this section is not ★.

   The smallest fix is to say it plainly in two sentences. The page does not compute forces; it moves each particle by
   formula (1), which is what a real string or real air does when the wave is small (Section 4). The default is made
   large on purpose so that the bunching is easy to see, and a real medium would no longer follow (1) exactly at that
   size (Section 9). Then let the first bullet read as the assumption *behind (1)*.
2. **A claim that is wrong whenever the cap acts.**
   > "Both rows carry the same ξ and therefore travel at the same speed."

   The lower row carries A_L sin(kX − ωt) with A_L = min(A, 0.8/k), so at A = 26 px the rows differ for every
   λ < 204 px. The same section has just introduced A_L, and Exercise 3.1 points out the difference ("lowers its
   amplitude to 14 px"). A reader who notices is puzzled. Fix: "the same phase kX − ωt", or "the same ξ, up to the
   amplitude cap of Section 5".

**(B)**
- "The wavenumber k and the angular frequency ω are the same two quantities counted in radians". This reads as if k
  were λ in radians, but it is 1/λ in radians. Equation (1) directly above shows k = 2π/λ, so a reader recovers.
- The Fig. 1 caption uses ∂ξ/∂t one section before Section 3 explains differentiating at fixed X.
- *Outside the note:* the caption under the simulation writes ξ(x, t) = A sin(kx − ωt) with a lowercase x. In this
  note x = X + ξ is the *displaced* position, and the difference is exactly what matters in the lower row. A sharp
  reader comparing the two will wonder. The caption is page markup, not part of the note.

**(C)**
- The paragraph quoted in (A1) is heavier than its point, which is two plain sentences.

**Verdict: needs work** (A1, A2; both are fixed by rewording within the existing paragraph and bullet).

---

## 03 · One formula, two pictures

**(A)**
1. **The exercise teaches a classic misconception, and the correction sits in a ★ section the reader was told to skip.**
   > Exercise 3.1: "Set *Frequency* to 1.00 Hz: the period halves and the *Speed* readout doubles to 220 px/s. Now set
   > *Wavelength* to 110 px. The speed falls back to 110 px/s …"

   A section earlier the model said "No damping and no dispersion: … every wavelength travels at the same speed".
   Here the student watches the speed double with the frequency and change with the wavelength. In any real medium the
   opposite is true. v is fixed by the material, so raising f shortens λ and leaves v alone. "Double the frequency,
   double the speed" is exactly the misconception teachers try to remove.

   The note does explain this, but only in 4.4, which is ★: "On the page both f and λ are sliders and v follows from
   them, which amounts to choosing a new medium every time you move one." The abstract says ★ sections "can be skipped
   … without losing the thread", so the non-★ reader never meets that sentence.

   Smallest fix: one sentence after equation (2) or inside the exercise. For example: "In a real string or in air, v is
   set by the material, so raising f shortens λ; the page lets you set f and λ separately, as if you swapped the medium
   each time (Section 4.4)."

**(B)**
- "The last relation in (3) holds for any shape that moves to the right without changing". It is asserted here and
  proved in 4.4. It is a one-line chain rule, and the picture that follows ("the higher part behind a particle is about
  to arrive") carries it.

**(C)** None.

**Verdict: needs work** (A1, one sentence).

---

## 04 · Where the wave equation comes from ★

**(A)** None. Each step is stated with its physical meaning, the ★ tells the school student to skip it, and a graduate
follows every line.

**(B)**
- 4.1, "that is how a guitarist tunes a string, and why the thick strings sound low". The link from wave speed to pitch
  is skipped: the string's length fixes λ, so f = v/λ rises with v. Everyday experience fills the gap. In 4.4, though,
  "the source fixes the frequency, and the wavelength has no choice" runs the other way for "a real string". A guitar
  string is the case where the length picks λ. These are not contradictory (a driven string against a plucked one), but
  half a clause would keep the two from colliding.
- 4.1, F sin θ ≈ F ∂ξ/∂X silently uses sin θ ≈ tan θ. This is standard at ★ level.
- 4.2, the line "Density from the ideal-gas law with molar mass 28.97 g/mol at 293.15 K: 1.2043 kg/m³. Then
  √(1.40 × 101 325 / 1.204) = 343.2 m/s." It is set in small Plex Mono, like a computation receipt, in the middle of
  the derivation. It is correct and supports the 1.204. It could be one clause before (7) in the prose voice.
- 4.3, "resisted, by the usual rule for changes of shape, with 2G times its strain along the line". The factor 2,
  which is the whole of the 4/3, is asserted by appeal to "the usual rule". It comes from σ′ = 2Gε′; a shear by angle
  γ is a stretch γ/2 along one diagonal. A graduate knows this rule. Naming it would remove the "it can be shown"
  flavour.

**(C)**
- 4.3, the 4/3 G explanation is a single sentence of about 80 words, with nested semicolons and three appositive
  clauses:
  > "A strain ε along the line, with none across it, is the sum of two simpler ones: ε/3 in all three directions at once,
  > which changes only the volume, by the fraction ε, and is resisted with a stress Kε; and what is left, 2ε/3 along the
  > line and −ε/3 in each direction across it, which changes only the shape and is resisted, by the usual rule for
  > changes of shape, with 2G times its strain along the line, 2G · 2ε/3 = 4/3 Gε."

  The content is right and belongs in ★. Splitting it into three sentences would make it readable at a blackboard pace
  without adding anything.

**Verdict: clear.**

---

## 05 · Compressions and rarefactions

**(A)** None. Section 5 has the best physical reasoning in the note:
- "the particles just behind have been pushed forward and those just ahead pulled back, so both crowd towards the
  centre";
- the quarter-wavelength shift, made visible on the page;
- "no particle may move forward faster than the wave itself".

**(B)**
- "since the strain is ∂ξ/∂X = −u/v". The word "strain" is defined only in ★ 4.2. Here it comes with its formula, so
  it works as a definition in place.
- Exercise 5.1, "far beyond the small slopes that equation (4) assumed". Equation (4) is in the ★ section. A reader who
  skipped it does not know what (4) assumed. "far beyond the small slopes the wave equation assumes (Section 9)" would
  not depend on ★.

**(C)**
- The paragraph "Even so, the default wave is far from small …" makes one point, that the compressions are narrow and
  crowded and the rarefactions broad and thin, in four ways:
  1. the exact densities 3.88 and 0.574;
  2. the linear values 1.74 and 0.26;
  3. the 26 % fraction, with its three-sentence derivation;
  4. the gap range 7.0 to 44.1 px.

  The Fig. 4 caption then repeats 3.88, 0.574, 1.74 and 0.26 verbatim, and Section 8 repeats 3.88 and 0.574 a third
  time. One of (3) or (4), and the numbers in either the text or the caption, would carry the point.

**Verdict: clear.**

---

## 06 · Energy carried ★

**(A)** None.

**(B)**
- "Multiply the wave equation … by ∂ξ/∂t and use the product rule." The second product-rule identity is the
  non-obvious one: ξ_t ξ_XX = ∂_X(ξ_t ξ_X) − ∂_t(½ ξ_X²). A graduate can supply it. One displayed line would make the
  step fully visible.
- P is introduced by its formula and named "the power flowing past the point X". The Feynman picture is missing: the
  string on the left pulls the point sideways with force −F ∂ξ/∂X, and the point moves at ∂ξ/∂t, so force times velocity
  is P. The reader is not lost without it; it is the one physical picture this section could add.

**(C)** None.

**Verdict: clear.**

---

## 07 · How the page computes a frame

**(A)** None. Everything checks against the code:
- exact evaluation, with only rounding as error (the arrays are Float64);
- the accumulated phase and why it keeps the wave continuous under the Frequency slider;
- the stretch about X = 0 under the Wavelength slider;
- the 0.05 s clamp and the 0.63 rad bound at 2 Hz;
- the paused start under reduced motion.

**(B)**
- "The one quantity carried from frame to frame is the phase of the source". The model has no source and no ends
  (Section 2). It means the phase at X = 0. A reader can follow it.

**(C)** None.

**Verdict: clear.**

---

## 08 · From medium pixels to screen pixels

**(A)**
1. **A symbol that is never defined.**
   > "A transverse particle is drawn at height y_T − s ξ, with a minus sign because screen y points down."

   y_T appears nowhere else in the note. The previous sentence says "The rest line of the upper row lies at 30 % of
   the canvas height", so the reader can guess, but the symbol itself is not introduced. The walkthrough below the note
   does define it, as y_T = 0.3 H. Fix: "The rest line of the upper row, y_T, lies at 30 % …". This is minor.

**(B)**
- *Outside the note:* the Data panel calls the lower row's displacement **s** ("s = A_L sin(kX − ωt)", "x = X + s").
  It calls the scale s_px. The note and the walkthrough use s for the scale and ξ for both displacements. Section 7
  sends the reader to the Data panel, where s means something else. The data-store labels are out of bounds without
  Numa's yes, so this is only reported.

**(C)**
- The three bullets list drawing constants:
  - disc radii of 4.5, 6.5 and 4 px;
  - a 56 px bar and a 68 px band;
  - the 8 px crest offset;
  - 215 and 65 sample points.

  Which mark is which symbol (discs, rose lines, ticks, curve, triangles, bars, tint) is what the reader needs, and the
  paragraph "Where the picture and the stored numbers differ" makes the real point. The radii and offsets are code facts
  that belong in `docs/`. This is mild.

**Verdict: needs work** (A1, a four-character fix; otherwise clear).

---

## 09 · What the model leaves out

**(A)** None. Each limit is correct and has a number from the page:
- 36.6°;
- the steepening into a shock;
- v_L > v_T on a wire;
- Fig. 5 (water waves) as the dispersive next model;
- the 2.2 % mass–spring dispersion;
- polarisation.

All four further-reading links resolve, and the chapters named match the books.

**(B)**
- "ω ∝ |sin(ka/2)|" is a bare formula. In a limits section that points to the next model, that is acceptable.
- The last bullet, "Only the ratio A/λ fixes the shape.", repeats Section 2 word for word.

**(C)** None.

**Verdict: clear.**

---

## Summary

| § | Section | Verdict | (A) items |
|---|---|---|---|
| 1 | The pattern travels, the medium stays | clear | none |
| 2 | The model | needs work | the large-amplitude paragraph contradicts the first assumption and speaks in undefined terms; "Both rows carry the same ξ" is wrong when the cap acts |
| 3 | One formula, two pictures | needs work | Exercise 3.1 shows "double f, double v" with no warning; the "new medium" explanation lives only in ★ 4.4 |
| 4 | Where the wave equation comes from ★ | clear | none |
| 5 | Compressions and rarefactions | clear | none |
| 6 | Energy carried ★ | clear | none |
| 7 | How the page computes a frame | clear | none |
| 8 | From medium pixels to screen pixels | needs work (minor) | y_T is used but never defined |
| 9 | What the model leaves out | clear | none |

**(C) overloaded passages:**
- §2, the "prescribes … nonlinear sound dynamics" paragraph;
- §4.3, the 80-word 4/3 G sentence;
- §5, the lopsided-density paragraph and its verbatim repetition in the Fig. 4 caption (and again in §8);
- §8, the drawing-constant bullets (mild).

Every fix named above is a sentence or less. No section needs a new paragraph, figure or box.
