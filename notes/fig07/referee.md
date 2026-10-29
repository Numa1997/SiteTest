# Fig. 7 · Phasor sums · referee report

Read blind, as rendered, by two readers at once: a school student who is good at mathematics and a physics graduate.
Judged against `notes/STANDARD.md`, above all "Numa's verdicts": only (A) items count toward a verdict; a section with no
(A) item is **clear** and should be left alone.

- **(A)** real obstacle: the reader gets lost, a step is skipped, a symbol is used before it is defined, a claim is wrong or unsupported, a needed physical picture is missing.
- **(B)** taste: could be better, but nobody gets lost.
- **(C)** overloaded: longer or heavier than the point it makes needs.

## How it was read

- Built into `/tmp/fig07-ref-dist` (`OUT_DIR=/tmp/fig07-ref-dist npm run build`), served by a small Node static
  server, opened in headless Chromium (Playwright, `/opt/pw-browsers/chromium-1194`) at 1440×900. *Expand all* clicked: 0 folds left
  closed, 350 KaTeX nodes rendered, 0 raw `\(` delimiters, 0 console errors.
- Screenshots, one per section, captured as full-page clips so the pinned fold headers do not cover the text:
  `notes/fig07/shots/ref-00-abstract-1440.png`, `ref-01-p-circles` … `ref-09-p-limits-1440.png`. The five note figures were also
  read at 2× resolution.
- Text read from the DOM, with each KaTeX node replaced by its TeX source, and every number in the note recomputed by hand.
- Checked on the running page: the canvas is 770 × 601 px at 1440 px and 356 × 356 px at 390 px (as §8 says). Exercise 5.1:
  *3-petal rose* gives 3.14 s and 3-fold; ten left-arrow presses give −2.1, 62.83 s, 61-fold, and *Final shape* shows 7000 samples.
  End of Exercise 4.1: ω₂ = 5.00 gives |z| = 2.197, ⟨|z|²⟩ = 2.420, 0-fold. All as stated.
- The further-reading links: OUP, Pearson and HUP answer to curl. The Feynman site refuses curl (403) but answers a browser-like
  fetch through Firecrawl: chapter 48 has the title "The Feynman Lectures on Physics Vol. I Ch. 48: Beats".

Every equation, (1) to (17), checks. So do the worked numbers: n = 3, 2, 4 for the roses; the phase turn π/(2n); 5.5 rad/s and
1.14 s; 2.2|cos(t/2 + 0.05)|; the zeros at 3.04, 9.32 and 15.61 s; 2.197; 12.57 s; g = 2, 0.1 and 0.01; 62.83 and 628.32 s;
61, 13 and 7 petals; M = 5 and 6; q = 5 and 3; 1.2824; 1.36 cos 5t + 0.18 cos 10t; 0.1024 and 2.8224; 4.828; 12.0 frames,
0.20 s, 56 frames; the 0.0007 chord error (normal acceleration at most 20, times Δt²/8) and 16× that; 132 px per unit,
0.09 px and 1.5 px; 21.5 Hz. The figures plot what their captions say.

---

## Abstract and §1 · Circles riding on circles

**(A)** None.

**(B)**
- "Each mismatch with the observations could be repaired with one more circle, which is why the scheme lasted so long." This is the
  popular story. Historians dispute that Ptolemaic models really grew by stacking epicycles. It is harmless as colour.

**(C)** None.

**Verdict: clear.**

## §2 · A turning arrow: Euler's formula

**(A)**
1. *Symbol used before it is defined* (minor). In 2.1: "(indeed \(\mathrm{d}|z|^2/\mathrm{d}\theta = 2\,\mathrm{Re}(\bar z\,iz) = 0\))".
   Neither \(\bar z\) nor \(\mathrm{Re}\) has been defined at this point. \(\bar z\) is first defined in §6 ("where \(\bar z\) is \(z\)
   reflected in the real axis"), and Re appears in prose only in §4.2. A school student meets two new symbols inside an "indeed"
   and assumes they missed something. The physical argument around the parenthesis (velocity at right angles to the string) is
   complete without it. Smallest fix: drop the parenthesis, or gloss both symbols in it (\(\bar z = x - iy\), the arrow reflected
   in the real axis; Re, the part along the real axis).

**(B)**
- "a quantity whose rate of change is a fixed number \(k\) times itself is the exponential \(e^{k\theta}\) … With \(k = i\) the two
  descriptions of the same motion must agree". The student knows this only for real \(k\). The step is really a definition of
  \(e^{i\theta}\), which the ★ series check in 2.2 then supports. This is acceptable as written, in Feynman's spirit.
- 2.3, at 1440 px: the colon after "stretch the arrow to a length \(A\)" wraps onto a line of its own (a site-wide KaTeX/punctuation break; see "Across the note").

**(C)** None.

**Verdict: needs work.** The only item is the one parenthesis in 2.1.

## §3 · The model: arms joined tip to tail

**(A)** None.

**(B)**
- "Each arm's angle is prescribed as \(\theta=\omega t+\varphi\)." The subscript \(k\) is missing, though the caption of Figure 2
  has \(\theta_k\).
- "actual linked rods would exert forces and torques on one another, and would not generally maintain these independent rates".
  This is true of free rods. But §1's own pictures, the Spirograph's gears and the motor-driven fairground ride, do hold the
  rates. A reader may notice the tension.
- 3.1: "\(z=e^{it}+e^{-it}=2\cos t\) stops at its ends and smoothly retraces a straight segment". The pen turns back through 180°
  there, which a graduate would call a degenerate cusp whose two branches coincide. "Smoothly" is the debatable word.
- Figure 2 caption: the comma before "\(\varphi = 0, 0, 0.5\ \mathrm{rad}\)" starts a line at 1440 px.
- The card's *Phase* slider runs from 0 to 6.28, so the presets' \(-\pi/2\) (quoted in §4.1) shows on the card as 4.71.

**(C)**
- The kinematics point takes three sentences ("Each arm's angle is prescribed … This constructs the curve geometrically; actual
  linked rods … Everything on the screen is kinematics, geometry in motion, without forces.") and is then repeated as the first
  bullet of §9. The last sentence alone says it. The register also stiffens here ("prescribed", "constructs", "maintain these
  independent rates").
- 3.1: "The pen stops, \(\dot z = 0\), only where these velocities cancel, so a stationary pen is possible there." The second half
  only restates the first. With the cusp caveat that follows, two sentences go to a side remark before the useful content (equal
  tip speeds, the Trefoil, the deltoid).

**Verdict: clear.**

## §4 · Two arms: roses and beats

**(A)**
1. *Contradictory rates for the beat; the step that reconciles them is missing* (the main obstacle in the note). The section opens:
   "Read (8) as an arrow that turns at the average rate \(\bar\omega\) while its length \(2A\cos(\Delta\omega\,t/2)\) swells and
   shrinks at half the difference rate." Then 4.2 says that |z| "rises and falls once every \(2\pi/|\Delta\omega| = 6.28\ \mathrm{s}\)",
   and that the loudness "swells and dies twice a second, at the difference of the two frequencies." A reader who takes the first
   sentence at its word predicts a beat period of \(4\pi/|\Delta\omega| = 12.57\ \mathrm{s}\) for the *Beating pair*, and the note
   says 6.28 s. Nothing says why both are right: the cosine runs at half the difference rate, but its size peaks twice in each of its
   cycles, at the crest and at the trough. This is the classic beats confusion, and Feynman ch. 48 (cited) addresses it.
   Smallest fix: one clause, at either place.
2. *Skipped step* (minor): "For a whole number \(n\) it has \(n\) petals if \(n\) is odd and \(2n\) if \(n\) is even; a negative
   \(r\) is drawn on the opposite side of the centre, which is how an odd \(n\) manages with \(n\) petals." The rule is stated and
   the mechanism only gestured at. The "how" is left to the reader. Turning by π flips the sign of \(\cos n\theta\) when \(n\) is odd,
   so each negative lobe, drawn on the far side, lands on a petal already drawn; for even \(n\) it lands between two petals.
   Smallest fix: that one clause.
3. *Skipped step / sign trap* (minor): "With unequal lengths the two arms and the line from the centre to the pen form a triangle,
   and the law of cosines gives \(|z|^2 = A_1^2 + A_2^2 + 2A_1A_2\cos(\dots)\)". The student knows the law as
   \(c^2 = a^2 + b^2 - 2ab\cos C\) and finds a plus sign. The angle inside the triangle at the joint is π minus the angle between the
   arms, so the sign flips. The note does not say so. Smallest fix: half a sentence.

**(B)**
- Box "One formula, two pictures": at 1440 px the full stop after \(2A\cos(\Delta\omega\,t/2)\) starts a line.
- "Their phases, \(-\pi/2\) and \(+\pi/2\), change the cosine in (8) into a sine". Formula (8) was written with zero phases. The
  phase form arrives only in (10), a few lines later, so the reader must take this on trust for a moment.
- Exercise 4.1 is headed "on the figure above" and says "(the caption under the figure shows \(t\))". Directly above it sits the
  static Figure 3, whose caption has no clock. The exercise means the live simulation (Fig. 7) at the top of the page. The reader
  works it out from "Press *Beating pair*", but only after a moment of looking at the wrong caption.

**(C)**
- The box's first sentence ("Two equal arms make a single arrow that turns at \(\bar\omega\) and has length
  \(2A\cos(\Delta\omega\,t/2)\).") repeats the paragraph immediately above it word for word in substance. The two-case sentences
  after it are the box's real content.

**Verdict: needs work** (A1 above all; A2 and A3 are one clause each).

## §5 · When the curve closes ★

**(A)** None.

**(B)**
- "the shortest time that repeats every listed active arm". "Active" is defined only in the next paragraph ("every listed arm with
  \(A > 0\)").
- "where \(\gcd\) is the largest \(g\) for which every \(\omega_k/g\) is a whole number". With negative frequencies (\(-2\)),
  "whole number" has to include negatives, and "gcd(4, 2)" silently drops the sign.
- "with two arms it passes, given time, as close as you like to every point of the ring". This is stated without support. It is
  fine for a ★ reader (Kronecker), but it is a bare claim.
- "So to find the pen's own shortest period, first add up the arms that share a frequency and drop any sum that vanishes." The note
  does not say why this is then enough: distinct exponentials are independent. A graduate would like the half-line.
- 5.1: \(M\) and \(p/q\) are built on \(\omega_1\). The note does not say that any other arm gives the same \(q\), because
  \(\omega_k/M\) differs from \(\omega_1/M\) by a whole number.
- At 1440 px the comma before "no \(T\) exists" starts a line.
- Exercise 5.1 has the same "on the figure above" ambiguity as Exercise 4.1: Figure 4 sits directly above it.

**(C)** None. The cancelling-arms paragraph earns its place, since it documents a real gap in the *Period* readout.

**Verdict: clear.**

## §6 · The average size of the curve

**(A)** None.

**(B)**
- The \(\langle\cdot\rangle_t\) bracket is never named as a time average. The prose around (15) makes it clear anyway.

**(C)** None.

**Verdict: clear.** This is a model section: the physical picture ("each cosine swings evenly about zero"), the formula, the worked
Star numbers, Figure 5, and the honest caveat about equal frequencies tied back to Exercise 4.1.

## §7 · How the page computes it

**(A)**
1. *Wrong claim.* 7.1: "The curves drawn in between are point-by-point blends of the old and the new curve, not curves that any
   set of phasors would draw." A blend \((1-\lambda)\sum(\text{old}) + \lambda\sum(\text{new})\) of two phasor sums sampled at the
   same \(t_i\) is itself a phasor sum, with the old arms shortened by \(1-\lambda\) and the new ones by \(\lambda\). The code blends
   index by index, at \(t_i = i\,T_\text{span}/n\), so this holds. When the span changes, it holds in the rescaled time \(i/n\).
   Linearity is the theme of the whole note, so a graduate stops here. The true point is that the in-between curves are not the
   curves of the in-between slider settings: moving ω from 2 to 3 does not pass through the ω = 2.5 curve. Smallest fix: change the
   phrase to "not the curve of any in-between setting of the cards".

**(B)**
- The symbol \(s\) is the *Speed* factor here ("advances \(t\) by \(\Delta t \cdot s\)") and the pixel scale in §8 (17). Likewise
  \(q_i\) (samples) here, and \(q\) in "q-fold" in §5.
- "at 4.00× speed, sixteen times more". The reason (the chord error grows as the square of the step, 4² = 16) is not given. A
  reader can take the number on trust, but five words would show it.
- "first-order low-pass filter with a time constant". Neither term is glossed for the school reader, although (16) makes the
  behaviour plain.

**(C)** None.

**Verdict: needs work** (one phrase in 7.1).

## §8 · From the plane to pixels, and from sound to radii

**(A)** None.

**(B)**
- "\(e \leftarrow e + 0.15\,(e_\text{raw} - e)\)": the letter \(e\), in a note about \(e^{i\theta}\), now stands for a band level.
- "smooths it over time with a constant of 0.8". This is a dimensionless blending factor, and a reader may read it as 0.8 s.
- "divides by 255 so that each level lies between 0 and 1". The bins have not been described as bytes from 0 to 255; the reader
  infers it from the division.
- "where ease is the *Bounce curve* chosen on the card". The control is named *Bounce curve*, one of its options is *Bounce*, and
  the default is *Linear*. A reader can take this to mean the Bounce easing is always used.

**(C)**
- The second paragraph ("The traced curve is burgundy and 1.8 px wide … twelve pieces whose opacity rises from 0.25 … a dot of
  radius 3 px … radius 5.5 px … 6 px pale-rose band") is mostly stroke widths and dot radii. The part the reader needs is which
  drawn thing is which symbol, and that the trail fades. That is about half the length.
- 8.1, from the beat bullet onward: the beat rule (35 %, 0.22, 280 ms, 10 frames, the median of 8 intervals) and the record/replay
  timing (50 ms, every third or fourth frame, 58 ms, Δt/50 ms) are a feature specification. The physics point of 8.1 is made in its
  first three sentences: the analyser finds the phasors in a sound, and three band levels scale the radii. It is acceptable as
  reference at the end of the note, but heavier than the point needs.

**Verdict: clear.**

## §9 · What the model leaves out

**(A)** None.

**(B)** None.

**(C)**
- The first bullet repeats §3's kinematics paragraph. The third bullet repeats, for the third time, the 0.01 rad/s and gcd point
  (§5 paragraph 3, the §7 bullet *Period and symmetry*). Each repetition is short, and the bullets suit a "limits" list. Mild.

**Verdict: clear.**

---

## Across the note (B)

- KaTeX and punctuation: at 1440 px a punctuation mark after inline maths sometimes wraps onto the start of the next line. Seen
  in 2.3 (":" alone on a line), the Figure 2 caption (", \(\varphi = …\)"), the §4 box (". If the arms…") and §5 (", no \(T\)
  exists"). This is a site-level typesetting matter (no break between maths and the following punctuation), not the note's
  wording.
- The exercise boxes say "on the figure above" while a static note figure stands directly above them. "On the simulation at the
  top" would remove the hesitation.

## Verdicts

| Section | Verdict | (A) items |
|---|---|---|
| Abstract, §1 Circles riding on circles | clear | none |
| §2 Euler's formula | needs work | \(\bar z\), Re used before defined (2.1 parenthesis) |
| §3 The model | clear | none |
| §4 Roses and beats | needs work | half vs. full difference rate (main); odd/even petals step; law-of-cosines sign |
| §5 When the curve closes ★ | clear | none |
| §6 Average size | clear | none |
| §7 How the page computes it | needs work | "not curves that any set of phasors would draw" is wrong |
| §8 Plane to pixels, sound to radii | clear | none |
| §9 What the model leaves out | clear | none |

Overall the note is clear, warm and correct. Its numbers check against the running page. Five small edits would clear every (A):
one parenthesis in §2, three clauses in §4 and one phrase in §7. None needs a new paragraph, figure or box. The (C) items are
optional trims, and leaving them is defensible under "a clear section is not touched".
