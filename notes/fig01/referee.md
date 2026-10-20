# Fig. 1 · referee report (blind reading)

Page: `public/simulations/Circular Wave Interference Visualization.html`, lecture note "Circular waves that add up to a straight one".
Read as it renders: built with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig01-ref-dist npm run build` (rebuilt on resume, 20 Oct 2026 ~17:00;
the rendered text was identical to the first reading), served by a small Node static server, opened in headless Chromium
(Playwright, 1440 × 900), "Expand all" pressed: 304 KaTeX formulas rendered, 0 KaTeX errors, no raw `\(`, no closed fold
inside the note, no console errors. Read as two readers: a school student good at mathematics, and a physics graduate.
I did not read `plan.md`, `check.md` or any teacher report.

Screenshots in `notes/fig01/shots/`: `00-head.png`, `01-pond.png` … `10-limits.png` (sections 6 and 7 in two parts each), and
three frames of the simulation itself, `sim-reset.png`, `sim-line16-30px.png`, `sim-line16-64px.png`, to test what the
exercises say the reader will see.

Numbers checked by recomputing them (Python, from the page's formulas and the code's constants): field height 360.5 px
(canvas 770 × 346.5 css px, rounded by `Sim.canvas2d` to 347), centre row y = 181.4 px and h = 169.1 px; crest speed 1.55 v,
46 px spacing (sec. 4); 26 and 14 calm lines, residue 0.071 / 0.162 (sec. 5); side lobe 0.220, angles 42.04°, 63.2°, 79.2°,
2.40°, 5.12°, far-field check 2.2 × 10⁻³ at 10⁶ px and 6.3 × 10⁻⁵ at 10⁷ px (sec. 6); D²/λ = 15 053 px; every range in the
Figure 4 paragraph (0.009–0.829, 0.036–0.765, 0.119–0.168, 0.050, 0.013–0.387, peaks every 43–46 px); (17) = 0.142 against
0.141 and 0.140; the five heights 0.076 … 0.173 (sec. 7); 1/(8kr) = 0.010 rad two wavelengths out (sec. 3); 0.1^0.8 = 0.158,
2/255 (sec. 9). Code claims checked in the page script: Line of 16 positions, Reset, Add 5 random (1/6 to 5/6 of the width),
Δt cap 0.05 s, grid rule, colour table and its three colours, dot radius 5.5 px. All agree, except the one noted under
section 6 (B). Further-reading links: Pearson, Internet Archive, Wiley and the Born & Wolf DOI answer 200; the two Feynman
links answer 403 to curl and to headless Chromium (Cloudflare bot check), so they could not be opened from here.

Legend. (A) a real obstacle: the reader gets lost, a step is skipped, a symbol is used before it is defined, a claim is
wrong or unsupported, a needed physical picture is missing. Only (A) sets the verdict. (B) taste. (C) overloaded: longer
or heavier than its point needs.

---

## Head and abstract

(A) none.

(B) The promise "Sections marked ★ carry the heavier mathematics and can be skipped on a first reading without losing the
thread" is broken twice; see the (A) items under sections 4 and 7. The abstract itself is fine.

Verdict: **clear**.

## 1 · Pebbles in a row

(A) none. The pond, the harbour, the concert line array and the phased array come before any symbol; Figure 1 is clear
and its labels are readable.

(B)
- "inside the harbour that strip of water behaves like a row of sources and sends the waves on in curved fronts": coming
  right after a paragraph about a row that makes a *straight* ripple, a school student may wonder whether this example
  agrees or disagrees. One word ("a short row") would make it a contrast on purpose.
- The two questions Huygens "leaves open" are answered later (section 6 box, section 7, 7.1), but the note never says
  "this answers the first question". See section 7 (B).

Verdict: **clear**.

## 2 · The model

(A) none.

(B)
- "A word on what the figure is, before the physics.": the reader has just seen *Figure 1* (Huygens' construction); here
  "the figure" means the simulation. Clear by the next sentence.
- "the path-difference picture below" points vaguely; it is Figure 2, right.
- "so no dispersion relation ties them together": "dispersion relation" is used before it is explained; the clause still
  reads ("set separately").
- Assumption 2, "The medium is non-dispersive: every wave travels at the same speed \(v = f\lambda\)", leans on the same
  idea that section 10 gets wrong; see section 10 (A).
- "\(\psi\) … the signed field shown by the colours": saying once "the height of the water above its rest level" would help
  the school student; section 9 later says "signed height".

Verdict: **clear**.

## 3 · One source, one ring ★

(A) none for the reader this section is written for (the graduate). The energy argument for \(1/\sqrt r\) is a good
physical picture.

(B)
- "the wave equation turns into (3)": the step that each time derivative of \(e^{-i\omega t}\) brings down \(-i\omega\) is
  silent; a graduate fills it at once.
- \(J_0\), \(Y_0\) are named but not introduced; fine for ★.
- The ★ on the whole section also hides the plain parts: the energy reason for \(1/\sqrt r\) (which section 2 already
  quotes) and the page's own ring (5) in 3.1. This is the cause of item A1 below.

(C) "The asymptotic form needs \(kr \gg 1\). At \(\lambda = 30\ \mathrm{px}\), \(kr = 1\) at … ; the first correction is a
phase lag of \(1/(8kr)\) radians, 0.01 rad two wavelengths from a source and smaller beyond, with a still smaller error in
the height, so the form holds everywhere on screen except within a few pixels of each source." One long sentence of
error analysis for a formula (4) that the page never uses (it draws (5)). Its point, "(4) is good beyond a few pixels
from a source", fits in one clause.

Verdict: **clear**.

## 4 · Adding the rings

(A)
- **A1. Symbols defined only inside the skipped ★ section.** "\(\psi(x, y, t) = \frac{1}{N}\sum_{i=1}^{N} a_i\cos(k r_i -
  \omega t)\). (6)" and "Since every \(a_i \le 1\), \(|\psi|\) can never exceed 1." A school student who skips section 3 as
  the abstract invites has never met \(a_i = e^{-\gamma r_i/R}\), \(R\), \(k = 2\pi/\lambda\) or \(\omega = 2\pi f\):
  they are defined only in ★ section 3 and its part 3.1 (equation (5)). Section 2 introduced \(f\), \(\lambda\), \(\gamma\)
  as sliders, but not these. The reader is lost at the first equation of the first unstarred section after the ★.
  Smallest fix: one clause after (6), "where \(k = 2\pi/\lambda\), \(\omega = 2\pi f\), and \(a_i = e^{-\gamma r_i/R}\) is
  the height of ring \(i\) at its distance \(r_i\), (5)". (Or put the ★ on the Bessel part only and leave 3.1 unstarred.)

(B) The scissors aside on crest speed (1.55 v) is useful: it heads off a real confusion for a reader who times the crests
on screen. Leave it.

Verdict: **needs work** (A1 only, one clause).

## 5 · Two sources: calm hyperbolae

(A) none. The trigonometric identity, the envelope, the hyperbola, the count of calm lines and the damping residue all
follow step by step, and the numbers are right.

(B) Exercise 5.1 says "Press Reset, then Pause. Count the cream calm lines that start from the bottom edge". Along the
stretch between the two sources \(\bar r\) is nearly constant (exactly \(s/2\) on the source line), so if the pause catches
the moment when \(\cos(k\bar r - \omega t) = 0\) there, the whole bottom strip is cream and there is nothing to count
(in `sim-reset.png` the moment was a good one). Counting while it runs, where the calm lines are the only parts that stay
cream, avoids this.

Verdict: **clear**.

## 6 · A row: one beam and its side beams ★

(A) none inside the section for its graduate reader; the geometric series, the removable \(0/0\), the beam edges, the
grating lobes and the steering delay (14) are all derived and correct. (Its ★ causes A2, listed under section 7, where the
reader gets lost.)

(B)
- \(F(\theta)\) first appears as "\(|F(\theta)| = \ldots\)" in (12) without "\(F(\theta) =\)" in front of the sum, and the
  common factor \(e^{ikr_0}\) is dropped silently. It is defined two paragraphs later ("\(|F|\) is the amplitude far away
  in the direction \(\theta\) …"). Writing "\(F(\theta) =\)" in front of the sum fixes both.
- "Between two neighbouring full beams lie \(N - 2\) weak side lobes" is stated without the one-line reason (\(N - 1\)
  zeros of \(\sin(N\beta/2)\) between two full beams).
- "side beams" (the full-strength grating lobes) and "side lobes" (the weak ones) are near-homonyms; a school student can
  mix them up.
- "(… at the default \(\gamma\) it changes the result (12) by at most 0.03.)": the normalisation is not stated. With the
  arrows scaled to their mean length I get 0.032 on a 0.1° grid but 0.040 on a 0.01° grid (the largest change sits on the
  steep flank of the 42° beam, near 39°); with source 0 as reference it is 0.12. "about 0.04" with "arrows scaled to their
  mean length" would be exact.
- Exercise 6.1 says the tilted crests are "heading out at about 42° to either side"; section 7 then says "42° is the
  direction in which the side beams are heading, not a line one can read off the picture". Both are true (the tilt of the
  crests is visible, a separate beam is not; `sim-line16-30px.png` shows the chequerboard), but a reader who just did the
  exercise may feel contradicted. A few words in section 7 ("the tilt of the crests shows it, but no separate beam") remove
  the clash.

(C) Two side remarks sit inside the derivation, exactly where the reader needs the main line: the parenthetical about
damping between \(\beta\) and the series, and the grey check note ("Checked against the page's own sum (6) with
\(\gamma = 0\) at a distance of 10⁶ px: …") between (12) and the sentence that says what \(|F|\) is. The reader meets
\(|F(\theta)|\), is told it was verified at 10⁶ and 10⁷ px, and only then learns what it means. Moving the check note after
the \(|F|\) paragraph, or into the Figure 3 caption, keeps every word and restores the order.

Verdict: **clear**.

## 7 · Near the row: the front straightens

(A)
- **A2. The unstarred section rests on the starred one.** Section 6 carries ★ on its heading, so the abstract tells the
  school student to skip it; section 7 then opens with "Equation (12) holds only very far away. … a path that (11)
  neglects", says "the beams of Figure 3 have not yet separated, and 42° is the direction in which the side beams are
  heading", and ends with "Near the row the straight-ahead wave and the two side waves of (13) overlap … every
  \(\lambda/\sin\theta_1 = s\)". (11), (12), (13), \(\theta_1\), the side beams and the rule "closer than one wavelength"
  all live only in the skipped section; the reader is lost in the first sentence and again in the last paragraph. Smallest
  fix, either one: take the ★ off the section 6 heading (its only heavy step is the geometric sum (12); the beam directions
  \(\sin\theta_m = m\lambda/s\) and the box are school-level), or open section 7 with one sentence recalling the box of
  section 6 (a row sends a beam straight out and, when \(s \ge \lambda\), side beams at \(\sin\theta_m = m\lambda/s\)).

(B)
- "the ends of a row of length \(D\) are further away than its middle by about \(D^2/(8r)\)": the one-line Pythagoras step
  is left out; it is the same expansion as (16) a page later.
- 7.1: the damping factor of each source is taken out of the integral as \(e^{-\gamma h/R}\) silently (inside the Fresnel
  zone it varies by under 2 %).
- "The factor \(\sqrt h\) in (17) is an artefact of the page's damping": it is an artefact of the page's *missing*
  \(1/\sqrt r\) (it is there at \(\gamma = 0\) too); the next two sentences make this clear, so it is only wording.
- 7.1 is where the first of Huygens' open questions of section 1 ("why the wavelets themselves are invisible") is
  answered — the arrows of distant sources cancel, only a Fresnel zone builds the front — but the note never says so, and
  the answer sits only in a ★ part. One clause tying it back would close the loop the introduction opened.
- The Figure 4 paragraph and the Figure 4 caption say the same thing twice (two and four sources leave fringes, sixteen
  merge); mild, leave it.

Verdict: **needs work** (A2 only, one ★ or one sentence).

## 8 · Two maps and a turning phase

(A) none. The split (18), what triggers a rebuild, the frame update, the grid rule with measured sizes, the sampling
(7.2 points per wavelength at 16 px) and the float32 storage are all stated as the code does them.

(B)
- \(P\) now counts grid points ("\(2NP\) cosines and sines for \(P\) points"); in sections 2 and 7.1 \(P\) is a point of the
  field.
- One clause saying that nothing is stepped in time (the page evaluates the closed form (6), so there is no step size and
  no accumulated error) would answer the graduate's first question about "the integrator"; it can be read between the
  lines already.

Verdict: **clear**.

## 9 · From numbers to colours

(A) none. Where the drawing differs from the store (smoothing, the 256-step table, the power 0.8, the clip) is said, and
which drawn thing is which symbol is clear.

(B) none.

Verdict: **clear**.

## 10 · What the model leaves out

(A)
- **A3. The dispersion bullet offers a false contrast.** "Real water waves are dispersive: their speed depends on their
  wavelength (Fig. 5). Here every wave moves at \(v = f\lambda\)." The second sentence is meant as the difference, but
  \(v = f\lambda\) holds for real water waves too; it is the definition of the phase speed of any periodic wave. What the
  page leaves out is that in water the frequency fixes the wavelength (and longer waves run faster), while here \(f\) and
  \(\lambda\) are two free sliders. A graduate stops here; a school student learns that "\(v = f\lambda\)" marks a
  non-dispersive medium, which is wrong. Also "(Fig. 5)" is plain text: the note has Figures 1–4 only, so the reader looks
  for a Figure 5 that is not there (it means the site's Fig. 5, the water-wave page). Smallest fix: "Real water waves are
  dispersive: the frequency fixes the wavelength, and longer waves run faster (Fig. 5 of this site). Here \(f\) and
  \(\lambda\) are set separately." Section 2's first paragraph already says this correctly.

(B)
- "The row radiates downwards as strongly as upwards … Huygens' wavelets share this flaw": for a real row of pebbles the
  downward wave is real, not a flaw; it is a flaw only when the row stands for Huygens' wavelets on a front. Saying so in
  a few words would stop a reader's pond experience from arguing with the sentence.
- Further reading: real, relevant chapters; the Feynman links could not be opened from this machine (see the top).

Verdict: **needs work** (A3 only, one sentence).

---

## Summary

| Section | Verdict | (A) | (C) |
|---|---|---|---|
| Head and abstract | clear | — | — |
| 1 Pebbles in a row | clear | — | — |
| 2 The model | clear | — | — |
| 3 One source, one ring ★ | clear | — | C1: the \(1/(8kr)\) validity sentence |
| 4 Adding the rings | needs work | A1: \(a_i\), \(k\), \(\omega\), \(R\) defined only in ★ section 3 | — |
| 5 Two sources | clear | — | — |
| 6 A row ★ | clear | — (its ★ causes A2) | C2: two asides inside the derivation, check note before the meaning of \(\lvert F\rvert\) |
| 7 Near the row | needs work | A2: rests on (11)–(13) and Figure 3 of ★ section 6 | — |
| 8 Two maps | clear | — | — |
| 9 Numbers to colours | clear | — | — |
| 10 Limits | needs work | A3: "Here every wave moves at \(v = f\lambda\)" is no contrast; dangling "(Fig. 5)" | — |

Seven of eleven parts are clear and should be left alone. The three (A) items are each fixed by one clause, one sentence
or moving one ★; none needs a new section, figure or box. Every number checked agrees, except "at most 0.03" in
section 6 (0.040 on a fine grid, normalisation unstated; a (B) item).
