# Fig. 3 · referee report on the lecture note

Page: `public/simulations/Interactive Double-Slit Experiment Visualization.html`, note "Two slits, one wave: how a path
difference draws light and dark". I read it blind, as a school student who is good at mathematics and as a physics
graduate, against `notes/STANDARD.md` and Numa's verdicts. Only (A) items count toward a verdict. (A) means a real
obstacle: the reader gets lost, a step is skipped, a symbol is used before it is defined, a claim is unsupported or wrong,
or a physical picture is missing where it is needed. (B) means a matter of taste. A section with no (A) item is "clear".

**How I read it.** I built the site with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig03-ref-dist npm run build` (the built page is
byte-identical to the source page) and served it with a small Node static server. I opened it in headless Chromium
(Playwright, 1440 × 900), pressed "Expand all" and read the rendered text, with KaTeX source pulled from the annotations.
I screenshotted each section into `notes/fig03/shots/`: `00-head-abstract.png`, `NN-<id>.png` (whole section) and
`NN-<id>-vpK.png` (viewport tiles). 359 KaTeX nodes rendered, with no console errors.

**Numbers recomputed.** I recomputed every worked number in the note in Python and checked the code facts in sections 8–9
against the page script. All of them hold: the defaults (L₁, L₂, δs, b sin α, equation (5)); Exercise 4.1 (38.27, 39.80,
1.73 → 0.20, 8.69-fold, b/r = 0.693); the Fig. 2 thresholds (1 % at d = 125 px, 1.55 % at d = 100 px); Exercise 5.1
(9.72°/19.72°, 9.76°/19.81°, 20.04°, and the readouts 0.49/0.51 and 0.99/1.01); the envelope values (0.74, 0.26, 0.88,
0.41, 42.45°); the Fig. 5 expectations (130.9 and 2.25); the electron wavelength (0.1226 nm, ×4486); the section 10 numbers
(1.6 %, 6.9 × 10⁻⁵, γ = 11.1°, 0.94 %); the verdict tolerances (0.938, 0.062); and 57 samples per fringe. The direct
difference L₂ − L₁ and form (3) differ by at most 6.8 × 10⁻¹⁴ px over the slider grid, inside the note's bound of
1.4 × 10⁻¹³ px. The reference links work. Pearson and Wiley return 200. Caltech's Feynman site and the Royal Society DOI
return 403 to curl, which is a bot wall: the Feynman I-29 page loads through Firecrawl with the title "Ch. 29:
Interference", and the DOI resolves to royalsocietypublishing.org.

---

## Abstract and header

(A) none.

(B) None worth raising.

**Verdict: clear.**

## 1 · Bright and dark from one source

(A) none. The section opens with loudspeakers, soap films and a CD, then gives Young's slip of card with the right numbers
(1/30 inch = 0.85 mm, the bright middle of the shadow, the bands vanishing when one edge is blocked). This is the physical
picture the standard asks for.

(B)
- The title says "one source", but the first example has two loudspeakers. The point (one tone, two emitters in step) only
  becomes clear with Young's single hole. This is harmless.

**Verdict: clear.**

## 2 · The model

(A) none. Every symbol is defined before equation (1). The assumptions are listed. The pixel unit is explained.

(B)
- Standard item 2 asks for the dimensionless numbers at the page's values. The note says that only b/λ and d/b matter, but
  gives b/λ = 2.96 only in section 9 and d/b = 5 nowhere. The default λ = 13.5 px is first stated in Exercise 5.1, yet
  4.1 ("0.0039 λ") and section 5 ("67.5 px") already use it. Adding "λ = 13.5 px" to the defaults listed in section 3
  would cover this.
- "Phase" is used without a word of picture ("how far through its cycle the wave is"). A good school student will manage.

**Verdict: clear.**

## 3 · The exact path difference

(A) none. Pythagoras, then the difference-of-squares trick, each step said. The checks at α = 0 and at the defaults are
given. The paragraph on cancellation is honest about what the rearrangement buys.

(B) none.

**Verdict: clear.**

## 4 · The far field (with 4.1 ★ and Exercise 4.1)

(A) none. The algebraic route (L₁ + L₂ ≈ 2r) and the geometric route (Fig. 1, right) both work, and the figure shows
both α's.

(B)
- 4.1 ★: in "only odd powers of ε survive in the difference; to third order in b/r they are r(ε − ½εβ + ⅛ε³)", the
  factor 2 from taking the difference and the origin of −½εβ (the cross term of u²) are left to the reader. The last step
  to equation (5) uses 1 − sin²α = cos²α. A graduate fills all of this in a minute, so it is not an obstacle.
- β means b²/(4r²) here and πw sin θ/λ in section 6. Each is defined where it is used.
- The text says "Figure 2 follows the error", but Fig. 2 plots the two path differences on a 0–15 px scale. Beyond
  d ≈ 80 px the gap (0.2 px at d = 100) cannot be seen. The caption gives the numbers, so nothing is lost.

**Verdict: clear.**

## 5 · Adding the two waves (with Exercise 5.1)

(A)
1. "At the page’s defaults it gives λd/b = 67.5 px along the observation line."
   The previous sentence says that equation (9) needs small angles, sin θ ≈ tan θ ≈ θ. At the defaults the first bright
   fringe is at θ ≈ 20°, which is not small. The page shows the problem: with the default sliders the readouts say
   δs/λ = 1.01 and "Constructive · bright fringe, m = 1". So P sits on the first bright fringe, at d tan 20° = 72.8 px
   from the centre line. The exact first bright fringe on the observation line is at 200 tan 19.81° = 72.0 px. A student
   who checks the figure finds the bright fringe 72 px out, after reading 67.5 px. A graduate sees the small-angle formula
   applied at 20° straight after the warning. As written, the number is wrong for what it names, the fringe spacing on the
   observation line. (The page's data panel itself labels `fringe_px` "small angles".)
   Smallest fix: one clause, e.g. "… 67.5 px, the small-angle estimate; at 20° the angles are no longer small, and the
   first bright fringe lies 72 px from the centre, where P sits at the defaults."

(B)
- Why the camera records the square of the field (the energy of a wave goes as the square of its swing, like a pendulum's
  energy goes as the square of its amplitude) is stated, not pictured. This is the step a school student is most likely
  to ask about. It is the closest (B) to an (A), and one clause would cover it.
- y now names the position along the screen (y_m, Δy here; dy in section 7). In section 2 and Fig. 1, y points away from
  the wall and the screen runs along x. Each use is defined in place, so this is only a notation clash. Writing x_m and Δx
  would remove it.
- A new symbol D appears for the screen distance and then gives way to the page's d in the same paragraph. Readable.
- "the amplitude 2E₀ cos(Δφ/2)" can be negative. Fig. 3 writes |cos|. This is a nicety.

**Verdict: needs work** (one item, one clause).

## 6 · Slits with a width ★

(A) none. Equations (10)–(11) follow for a graduate. The missing-order example and the 8 px gap remark are correct and
useful.

(B)
- "the wave from x′ has a path shorter by x′ sin θ". With the note's own geometry (P on the side of S₁, at negative x), a
  source at x′ > 0 has a longer path. The sign does not matter for a symmetric slit, but a careful graduate will notice.
- The Fig. 4 caption says the first fringe "is cut to 0.41" at 19.72°. The plotted burgundy peak is about 0.44 near 18°,
  because the envelope pulls it inwards. Both statements are true, but the reader sees a peak that is not at 19.72°.

**Verdict: clear.**

## 7 · One particle at a time

(A)
1. "The field E of Section 5 predicts the same fringes, because its two parts add with the same path difference and the
   same cross term; but E is not that amplitude. It is the classical account of light made of very many photons, and it
   gets the single-photon pattern right here because, for two slits, both sums have the same shape."
   The words "for two slits" suggest that the classical field and the single-photon pattern agree by a coincidence that
   only holds for two slits. They don't need such luck. For one photon in any linear optical arrangement, the chance of a
   click at a place is proportional to the classical intensity there. Both waves obey the same wave rule with the same
   wavelength, so any arrangement of openings gives the same pattern. (This is the standard quantum-optics result: the
   counting rate is ⟨E⁻E⁺⟩, and for a one-photon state it is the squared modulus of the mode's classical field.) The
   sentence also raises "E is not that amplitude" and leaves the reader with no picture of how the two are related. A
   school student is left unsure whether the wave picture of section 5 can be trusted for single photons. A graduate meets
   an unsupported and misleading restriction.
   Smallest fix: replace the last clause with the general reason, e.g. "… and it gets the single-photon pattern right
   because both obey the same wave rule: the classical intensity says how many photons arrive at each place, and for one
   photon it says how likely it is to arrive there. This holds for any arrangement of slits, not only two."

(B)
- p is the probability density p(θ) and, three paragraphs later, the momentum. f is the frequency here and the fractional
  part in section 8. Each is defined in place.
- The experimental claims (single-electron build-up, neutrons, atoms, C₆₀) have no source in Further reading. A real,
  opened reference such as Tonomura et al. (1989) or Arndt et al. (1999) would back the sentence. This is not an obstacle.
- p = √(2mₑeV) is non-relativistic. That is fine at 100 V and could say so in two words.
- In the model a point slit gives a flat "single-slit pattern". The phrase "pile up as one single-slit pattern" might make
  a reader expect structure. This is harmless.

**Verdict: needs work** (one item, one sentence).

## 8 · How the page computes

(A) none. Every statement matches the page script: closed formulas, Q = P + L₁û, the 0.08 tolerance and its intensity
bands, 301 samples, the dashed exact curve at x = d tan θ, phase += 0.8 Δt.

(B) none.

**Verdict: clear.**

## 9 · From lengths to pixels

(A) none. The SVG geometry (600 × 440, wall at y = 370, x = 300, 8-unit gaps, thresholds 0.05 px and 0.2°, maxR 430,
opacity 0.55(1 − r/430), plot 500 × 118) matches the code. The scale comparison (2.96 wavelengths, 1.88 µm, 395
wavelengths, 0.145°) is a good "equation to screen" check.

(B)
- r without a subscript in "0.55 (1 − r/430)" is the wavelet radius, not |MP|. This is clear from the context.

**Verdict: clear.**

## 10 · What the model leaves out (with 10.1 Further reading)

(A) none. Each limit comes with a number at the defaults (unequal amplitudes 7 × 10⁻⁵, polarisation 0.9 %), and the
next model is named. The four references are real, correctly cited (chapters checked), and linked.

(B) none.

**Verdict: clear.**

---

## Summary

| Section | Verdict | (A) items |
|---|---|---|
| Abstract | clear | — |
| 1 Bright and dark from one source | clear | — |
| 2 The model | clear | — |
| 3 The exact path difference | clear | — |
| 4 The far field (4.1 ★, Ex. 4.1) | clear | — |
| 5 Adding the two waves (Ex. 5.1) | needs work | "67.5 px along the observation line" applies the small-angle formula at 20°; the page puts the fringe at 72 px |
| 6 Slits with a width ★ | clear | — |
| 7 One particle at a time | needs work | "for two slits, both sums have the same shape": an unsupported, misleading restriction; the agreement is general |
| 8 How the page computes | clear | — |
| 9 From lengths to pixels | clear | — |
| 10 What the model leaves out | clear | — |

Two (A) items in the whole note. Each is fixed by one clause or one sentence. Everything else should stay as it is.
