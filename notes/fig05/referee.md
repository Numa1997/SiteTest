# Fig. 5 · referee report on the lecture note of `water-wave.html`

Read blind, 20 October 2026, as two readers at once: a school student who is good at mathematics, and a physics graduate.
I read the page as it renders on branch `claude/physics-notes-rewrite-cwctkk`. I did not read `plan.md`, `check.md` or any
teacher report. The verdicts follow `notes/STANDARD.md`, "Numa's verdicts". Only (A) items count: places where a reader gets lost,
a step is skipped, a symbol is used before it is defined, a claim is wrong or unsupported, or a physical picture is missing where it
is needed. (B) items are matters of taste. A section with no (A) item is "clear".

## How the note was read

- Built with `OUT_DIR=/tmp/fig05-ref-dist npm run build` and served by a small Node static server on
  `localhost:8765`. Opened in headless Chromium 1194 through Playwright at 1440 × 900 and pressed "Expand all". All 10 sections
  open, with 337 KaTeX formulas, 0 KaTeX errors and 0 console errors.
- Screenshots in `notes/fig05/shots/`:
  - `00-head.png`: the title and abstract.
  - `01-gull.png` … `10-limits.png`: one per section at full height, captured as page clips so the pinned section header stays
    at the top of its section. A plain element shot lets the header lie over the text.
  - `fig1@2x.png` … `fig4@2x.png`: the four figures at device scale 2.
- The text was read from the rendered DOM, with each KaTeX node replaced by its TeX source.
- Checks:
  - Every number in the note recomputed.
  - Figure 4 recomputed with my own RK4.
  - Exercise 5.1, Exercise 6.1 and the cap example in 6.2 driven on the page, with the readouts compared.
  - The drawing claims of Sections 08 and 09 compared with the page's script and with `scripts/sim.js`.
  - The five reading-list links opened. curl gets 403 from three hosts, which is bot-blocking. Firecrawl gets 200 for all five,
    and the titles match the citations.

## Section by section

### 01 A gull on the swell

**(A)** None.

**(B)** None. The gull, the bottle, the diver and the storm swell give the three facts the note later derives, in the order it derives them.

**Verdict: clear.**

### 02 The model

**(A1) Figure 1 uses symbols before they are defined, and one of them is never defined.** Figure 1 labels the water
"∇²φ = 0 / in the water" and the lower edge "∇φ → 0 as z → −∞". φ is first defined in Section 03. ∇² is not defined anywhere
in the note: equation (4) is written out as ∂²φ/∂x² + ∂²φ/∂z² = 0 and is never named ∇²φ. The caption says nothing about these
two labels: "The model. The wave travels to the right at speed c; the calm surface is the line z = 0 and the moving surface is
η(x,t). Dashed circles are the paths of water parcels …". A school student meets two symbols he cannot read in a section with
no ★, and nothing tells him that they come later.
Smallest fix: one clause in the caption, e.g. "the two labels in the water are Laplace's equation (4) and the deep-water
condition (9), met in Sections 03 and 04."

**(B)**
- Figure 1 writes the potential as φ (curly, `\varphi`), while the text writes ϕ (KaTeX `\phi`). It is the same quantity in two glyphs.
- Figure 1 is drawn at ak = 0.59, while the text gives the default as 0.58. The caption already says "close to the page's default", so this is fine.
- Figure 1 checked against (17): the crest parcel is at the top of its circle and the parcel a quarter wavelength ahead is left of
  its centre and rising. The trough parcel is at the bottom and the last one is right of its centre and sinking. The layers are
  λ/6 apart and the radii shrink by 2.84 per step, against the stated e^{π/3} = 2.85.

**Verdict: needs work** (A1 only: one caption clause).

### 03 Potential flow: Laplace's equation

**(A)** None.

**(B)**
- "The spin of a small parcel of water is measured by its vorticity, ∂u/∂z − ∂w/∂x, twice its angular velocity" is the only
  formula in the section without a picture. The box gave one for (1). A clause would do it: if the water above a parcel moves
  forward faster than the water below, ∂u/∂z > 0 and the parcel is rolled over.
- "Equation (2) holds automatically if both velocity components are slopes of a single function φ" gives the easy direction.
  "One unknown function now replaces two" leans on the converse: every flow without spin has such a φ. Read as a trial form that
  turns out to work, it is not wrong, but a graduate may want the converse named.
- "the value of φ at any point is the average of its values on any circle drawn around that point" is the mean-value property,
  stated without support. It is an aside, so this does not matter.
- The Kelvin argument is right as given: pressure from a smooth field acts through the centroid, and the centroid is the centre
  of mass when the density is uniform.

**Verdict: clear.**

### 04 Three conditions at the edges ★

**(A)** None.

**(B)**
- 4.2: from (7) to (8), the term gz becomes gη because the bracket is taken at the surface, z = η. The text says "At the surface
  the pressure is the air pressure …" and then "again moving the condition from z = η to z = 0". A careful student who puts z = 0
  into gz gets 0 and may ask where gη came from. A half-clause would close it: "at the surface z = η, so gz becomes gη". The graduate,
  for whom ★ is written, will not stumble.
- 4.2: "Dropping the small term ½|∇φ|², of order (aω)²" does not say what the term is small against. In 4.1 the same move says
  "ak times smaller", and here too the term is ak times ∂φ/∂t ~ ag.
- 4.2: the identity (u·∇)u = ∇(½|u|²) is stated for irrotational flow without proof. In two dimensions one line shows it:
  u u_x + w u_z = u u_x + w w_x by (2). ∇ and ẑ are not defined, which is standard for the ★ reader.
- 4.3 is an equation with no sentence before it. The heading, "Deep water stays still", carries the meaning.

**Verdict: clear.**

### 05 Gravity sets the pace: the dispersion relation

**(A)** None.

**(B)**
- A school student who skips Section 04, as the abstract invites, meets "Condition (6) needs …", "condition (9) forbids it" and
  "Only the dynamic condition (8) is left" as bare numbers. He can scroll back to three short equations, and "There is a simple
  picture behind (13)" gives the physics, so he is not lost. A few words where each is cited, e.g. "(8), the surface pressure is
  the air's", would make skipping painless.
- The "simple picture" sets the largest push, g·ak, equal to the full centripetal acceleration aω². That is right because the
  surface is steepest where the parcel is at the side of its circle, so its whole acceleration there is horizontal. One clause
  saying so would answer the graduate's "why compare the maxima?".
- The numbers all check:
  - ω = 4.869 rad/s and f = 0.7749 Hz.
  - c = 2.015 m/s and T = 1.290 s.
  - The 100 m swell: 12.49 m/s and 8.00 s.
  - The 16 s swell: λ = 399.7 m, c_g = 12.49 m/s and 44.5 h, printed as "about 44".
  - The 8 s swell: 6.245 m/s and 89.0 h.
  - Every table row.
- Exercise 5.1 driven on the page:
  - Phase speed c goes 1.37 → 2.50 m/s and Period T goes 0.88 → 1.60 s.
  - The Frequency slider follows (0.77 → 1.14 → 0.62 Hz) and is greyed out.
  - With dispersion off, at 260 px and 0.50 Hz, the readout is 1.30 m/s.

**Verdict: clear.**

### 06 Every parcel runs in a circle

**(A)** None.

**(B)**
- 6.2: in "The dashed line in the figure marks the orbit centres, not this average", "the figure" can be read as Figure 1 or as
  the page's figure. Both have such a line, so either reading is true.
- 6.2, read with Section 09: the drawn surface averages ½a²k = 7.0 px below the dashed line that Section 09 calls "the calm level",
  so the drawn sea holds a little less water than the calm one. The note says honestly that the line marks the orbit centres, but
  a graduate may still ask where the water went. One sentence would answer: at second order the surface orbits are centred ½a²k
  above the calm level, which first-order theory cannot show.
- 6.2: (17), read as exact, is Gerstner's wave: the same formulas with the same ω² = gk. The note says the trochoid is Gerstner's
  shape but not that the page's whole motion, taken literally, is Gerstner's flow. A clause would sharpen the closing sentence.
- "the steepest wave water can hold is about 0.14 wavelengths high" has no source. Kundu, chapter 8, already in the list, could carry it.
- The numbers all check:
  - aω = 1.169 m/s.
  - e^{−π} = 4.32 %, and e^{−2π} = 0.187 %, or 1/535.
  - The layers are at 25.8, 6.7, 1.7 and 0.45 % of the surface orbit, with radii 24, 6.20, 1.60, 0.41 and 0.11 px.
  - The diver: 4.3 % and 73.0 %.
  - ½ − ak/π = 31.5 % and ½a²k = 6.96 px.
  - The cap: a requested ak of 1.21 is held at 37.2 px.
- Driven on the page:
  - Deepest orbit reads 3.0 % at 400 px, 0.0 % at 120 px and 0.4 % at 260 px.
  - With A = 50 px, Steepness ak reads "0.90 (cap)".

**Verdict: clear.**

### 07 Stokes drift: the circles do not quite close ★

**(A)** None.

**(B)**
- This is the most useful (B) in the note. "The picture is this. Under a crest the parcel is at the top of its circle, where the
  forward flow is a little stronger because e^{kz} is larger; under a trough it is at the bottom, where the backward flow is a
  little weaker. Forward wins …" explains only the ζ ∂u/∂z term (cos²θ), which is half of (21). The other half, the sin²θ term,
  has a picture too: when the parcel is at the side of its circle, it is shifted towards the nearest crest, where the flow is
  forward. A graduate who sets the picture beside (20) will find a factor of two unaccounted for. One clause would fix it.
- Figure 4 reproduced independently: RK4 at 4000 steps per period, loop tops found by bisection on w = 0, averaged over 10 loops.
  | Case | My result | Printed |
  |---|---|---|
  | One loop | 1.0432 T | 1.043 T |
  | Advance per loop | 11.24 cm | 11.2 cm |
  | Mean speed | 83.49 mm/s, against (21) 80.59 mm/s | 0.0835 m/s |
  | Gap, ak = 0.2 | 3.59 % | 3.6 % |
  | Gap, ak = 0.1 | 0.93 % | 0.93 % |
  | Gap, ak = 0.05 | 0.24 % | 0.24 % |
  | z₀ = −0.56 m | 5.394 against 5.381 mm/s | 5.39 against 5.38 mm/s |
- The other numbers check: a = 8.28 cm, U_S T = 10.4 cm, and 0.678 m/s at the default steepness.

**Verdict: clear.**

### 08 Computing the picture

**(A2) A symbol is used before it is defined.** "the rest position X₀ = 30 + (W_field − 60) i/(N − 1) px and the depth
z₀ = −56 j px, where N is set by Particles per layer;" W_field is used here but defined only in Section 09: "The drawing has field
width W_field = 800 px = 8 m, or 400 px = 4 m when the canvas is narrower than 560 screen pixels …". Until the next section the
reader cannot picture where the columns sit, which is 30 px in from each edge of an 800 px field.
Smallest fix: "(W_field = 800 px, Section 09)" in the bullet.

**(B)**
- "Only the phase is accumulated" is followed two sentences later by "Nothing is integrated, so nothing accumulates error". The
  phase sum is itself an integration, though exact for constant f up to rounding. "Nothing else is integrated" would remove the
  apparent contradiction.
- The clock caps Δt at 0.05 s (`scripts/sim.js`, line 179). Below 20 frames per second, the page's time, and with it the wave,
  runs slower than the wall clock. A reader who times the period with a watch on a slow machine will measure more than 1.29 s.
  This is not mentioned; one clause in Section 08 or 09 would cover it.
- k changes from rad/m (Sections 02–07) to rad/px here, and the text says so: "The page measures λ in pixels, so k = 2π/λ is in
  radians per pixel". The letter A is used twice, for the constant in (11) and for the slider amplitude here, and each is defined
  where it is used.
- Code check: all as the script does it.
  - X₀, z₀, r, θ, ξ, ζ, u and w.
  - a = min(A, 0.9/k).
  - f from (13) at full precision, with the slider showing it in 0.01 Hz steps.
  - 18 × 5 = 90 parcels.
  - 307 surface points on the wide canvas and 174 on the narrow one.

**Verdict: needs work** (A2 only: one parenthesis).

### 09 From metres to pixels

**(A)** None.

**(B)**
- H is the canvas height here and the trough-to-crest height in 6.2. Each is defined where it is used.
- The 7 px offset of the mean surface (see Section 06 above) is one more place where the drawing and the "calm level" differ.
  It is stated in 6.2, not in this section's list of "three small ways".
- Code check: all as the script does it.
  - (23), with the 28 % rule and the 34 px margin.
  - The surface line every 3 px, from −60 to W_field + 60.
  - The tint from 36 % to 5 %.
  - Dots of 3.8 and 3.1 px, or 6 and 5 px in the followed column.
  - The followed column at i = 8, which is X₀ = 378.2 px on the wide field and 190 px on the narrow one.
  - Orbits drawn only while r·s > 1.2 px.
  - Rows below h − 8 px stored but not drawn.

**Verdict: clear.**

### 10 What the model leaves out

**(A)** None.

**(B)**
- There is no lead sentence; the list starts at once. Taste.
- The numbers check:
  - tanh π = 0.9963, so the wave is 0.19 % slower.
  - λ_min = 1.71 cm and c_min = 0.231 m/s.
  - 1 + ½(0.2)² = 1.02.
  - 1/(2νk²) = 85 600 s = 23.8 h.
- All five links open, and each matches its citation:
  - Feynman I-51, section 51-4 "Surface waves".
  - The OUP product page for Acheson.
  - Acheson chapter 3, "Waves", whose abstract is about a group of waves crossing a pond.
  - Kundu, 6th edition, chapter 8, "Gravity Waves".
  - Elsevier's page for Landau and Lifshitz.

**Verdict: clear.**

## Summary

| Section | Verdict | (A) items |
|---|---|---|
| 01 A gull on the swell | clear | — |
| 02 The model | needs work | A1: Figure 1 labels ∇²φ = 0 and ∇φ → 0 before φ is defined; ∇² is never defined; the caption is silent |
| 03 Potential flow | clear | — |
| 04 Conditions at the edges ★ | clear | — |
| 05 Gravity sets the pace | clear | — |
| 06 Every parcel runs in a circle | clear | — |
| 07 Stokes drift ★ | clear | — |
| 08 Computing the picture | needs work | A2: W_field used one section before it is defined |
| 09 From metres to pixels | clear | — |
| 10 What the model leaves out | clear | — |

The note is clear, well pictured and correct, and every number I checked agrees with the page. Each of the two (A) items is
fixed by a few words: a caption clause and a parenthesis. Of the (B) items, two deserve the lead's eye: the half-told Stokes
picture in Section 07, and the gz → gη step in 4.2.
