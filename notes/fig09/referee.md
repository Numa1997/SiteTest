# Fig. 9 · Driven oscillator · referee report

Read blind, as rendered, as two readers at once: a school student good at mathematics and a physics graduate.
Judged against `notes/STANDARD.md`, above all "Numa's verdicts". Only (A) counts toward a verdict.

**How it was read.** Built with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig09-ref-dist npm run build` (the built page is byte-identical
to `public/simulations/driven-oscillator.html`), served by a small Node static server, opened in headless Chromium 1194 at
1440 × 900, *Expand all* pressed. 164 KaTeX formulas rendered, 0 KaTeX errors, 0 console errors. The rendered text was read with
every formula replaced by its TeX source. Screenshots in `notes/fig09/shots/`: `NN-<id>.png` is the whole section with the
pinned headers released (the pinned header otherwise covers part of Fig. 2 and the lead of §6 in an element shot);
`NN-<id>-view.png` is the 1440 × 900 window as a reader scrolls to the section; `00-head.png` is the title and abstract.

**Numbers checked against the running page** (dataset read in Chromium, default settings): X = 0.4819 m, φ = 25.35°,
τ = 6.366 s, f_r = 0.49875 Hz, f_d = 0.4994 Hz (beat 20.25 s), first swell 0.596 m at t = 7.99 s, W_in = 19.032 J,
W_loss = 17.926 J, E(T) − E(0) = 1.106 J, energy balance 1.27 × 10⁻¹², RK4 vs exact 5.3 × 10⁻¹² m, ⟨P⟩ = 0.292 W, rest at
367.7 px of 770 px (47.8 %), span 2 × 77.44 px (20.1 %), window 8.89 s. Solve took 16.0 ms on this machine (the note says
9.5–12.4 ms and "depends on the machine"; consistent). Exercise 4.1 run: 1.013 m at ζ = 0.05, 0.253 m at ζ = 0.2, factor 4.0.
(6a) and the C₁, C₂ formulas checked by hand. Every number in the note is right.

**Links.** Taylor (Google Books) 200, French (Routledge) 200, Åström and Murray PDF 200 (8.6 MB). The two Feynman Lectures
links give 403 from this container (Cloudflare blocks the data-centre address, in curl and in Chromium); read through
Firecrawl instead, `I_24.html` answers 200 with "Vol. I Ch. 24: Transients" (24-1 energy of an oscillator, 24-2 damped
oscillations). Not a broken link.

---

## 01 · A push from outside

**(A)** None. The swing, the washing machine, the loudspeaker and the Millennium Bridge give the picture before any symbol;
input, output and plant are defined in plain words; Figure 1 names every symbol of (1).

**(B)** "A loudspeaker cone follows the music only because it was designed so that its own rhythm lies far from the notes it
plays." Roughly right (the cone works above its resonance), though above resonance it is the cone's acceleration, not its
displacement, that follows the force. Fine as everyday motivation.

**(C)** None.

**Verdict: clear.**

## 02 · The model

**(A)**
- "The *natural frequency* \(\omega_0 = \sqrt{k/m}\) is the undamped natural angular frequency; with underdamping, free ringing
  instead occurs at \(\omega_d=\omega_0\sqrt{1-\zeta^2}\); the *damping ratio* \(\zeta = c/(2\sqrt{km})\) says how quickly the
  ringing dies, …" ζ is used in the ω_d clause before it is defined later in the same sentence, and "underdamping" appears
  nowhere before this point (the note first gives it a range, ζ ≤ 0.9, in §10). The sentence also promises "two numbers
  with a direct meaning" and then gives three (ω₀, ω_d, ζ). A school student reading in order meets an undefined symbol in
  the sentence that is supposed to define the symbols. ω_d is not needed here: §3.2 derives it and §6 defines f_d where it
  is used. Smallest fix: delete the clause "is the undamped natural angular frequency; with underdamping, free ringing
  instead occurs at ω_d = …;" so the sentence reads as two definitions.

**(B)**
- "Dividing (1) by \(m\)" relies on \(c/m = 2\zeta\omega_0\), which the reader must work out. One line, easy.
- "the double pendulum of Fig. 2": the site's Fig. 2, not this note's Figure 2 (the resonance curves). The site's
  convention ("Fig. N" for simulations, "Figure N" in notes) is consistent, so leave it.

**(C)** The same ω_d clause: a patch that makes the defining sentence heavier and repeats what §3.2 derives.

**Verdict: needs work** (one clause).

## 03 · The exact solution ★

**(A)**
- "Adding such a ringing to the steady state and demanding \(x(0) = \dot x(0) = 0\) fixes its two constants: at \(t = 0\) the
  two conditions read \(X\cos\varphi + C_1 = 0\) and \(X\Omega\sin\varphi - \zeta\omega_0 C_1 + \omega_d C_2 = 0\), so"
  C₁ and C₂ appear before the form they multiply. That form, \(e^{-t/\tau}(C_1\cos\omega_d t + C_2\sin\omega_d t)\), is
  shown only afterwards, inside (5). The reader cannot check the second condition, and cannot even tell that "−ζω₀C₁"
  comes from differentiating the decaying exponential, until after it has been used. Smallest fix: write the ringing once,
  where it is introduced ("Adding such a ringing, \(e^{-t/\tau}(C_1\cos\omega_d t + C_2\sin\omega_d t)\), to the steady
  state …").

**(B)**
- "Equation (2) is linear, so its solutions add." Strictly, two solutions of the driven equation do not add to a third. The
  next sentence says what is meant (particular + free), so nobody is lost.
- "write the force as the real part of \(\tfrac{F_0}{m}e^{i\Omega t}\)": that is the force per unit mass.
- "At first the block rings at its own frequency": at first both rhythms are present, as §6 says correctly. "Also rings" would
  match.
- The non-★ sections 4 and 6 use (3), (4), (5) and C₁. A reader who skips this ★ section, as the abstract invites, has to come
  back for the results. That is the usual ★ contract (skip the derivation, use the result), so it works.

**(C)** The paragraph "At the drive frequency, acceleration is \(-\Omega^2\) times displacement. … The physical denominator
\(k-m\Omega^2+ic\Omega\) keeps these contributions together. Dividing by \(m\) gives the form in (3)." The first two sentences
give each term its physical meaning (spring and inertia oppose; the damper is a quarter cycle out). That is worth keeping.
The last two add nothing ("keeps these contributions together" says no more than the formula) and read like a patch.

**Verdict: needs work** (one clause in §3.2).

## 04 · Resonance and phase

**(A)** None. The slow-drive and fast-drive limits, the cancellation at Ω = ω₀, the Q = amplification reading of (6), the
completed square (6a) with its consequence ζ ≥ 1/√2 → no peak (which the page shows: its Bode caption says "no resonance
peak (ζ ≥ 0.71)"), and the 90° phase as "the force is largest when the block is fastest" are all present and correct.
Figure 2 matches (4).

**(B)** "(6a)" is an odd label in a note numbered (1)–(8). Taste.

**(C)** None. The (6a) passage is short and earns its place: it explains a caption on the page.

**Verdict: clear.**

## 05 · The control engineer's view ★

**(A)**
- "\(X(s) = G(s)\,F(s)\)" followed three sentences later by "\(G(i\Omega) = X e^{-i\varphi}/F_0\)". In one section, X is
  the Laplace transform of x(t) and also the steady amplitude of (4). F(s) and F₀ have the same problem, more mildly. Neither
  X(s) nor F(s) is named as a transform. A reader is invited to set X(iΩ) equal to the amplitude, which is wrong (the transform
  of the driven motion has poles at ±iΩ). Smallest fix: one clause naming them ("where X(s) and F(s) are the transforms of
  x(t) and F(t), not the amplitude X of (4)"), or a different letter for the transform.

**(B)**
- "the *Bode plot*, the second figure on this page": this means the panel under the animation. The note's own Figure 2 is
  the same plot, normalised, so either reading works.
- "on logarithmic axes": only the frequency and amplitude axes are logarithmic; the phase axis is linear.

**Rendering defect** (not a reading obstacle, so not counted in the verdict): in Figure 3 the label
`G(s) = 1 / (ms² + cs + k)` runs from x = 296 to x = 499 in the viewBox, but the plant box ends at x = 446. The box's right
edge strikes through the "c" of "cs" and the text runs onto the output arrow (shot `05-p-control.png`; measured with getBBox
at 1440 px and 390 px). Widening the `rect` (e.g. width 172 → 236 with the output line moved to start at its new edge) or
shortening the label fixes it.

**(C)** None.

**Verdict: needs work** (one clause; plus the figure defect).

## 06 · The start: beats and decay

**(A)** None. Two guitar strings out of tune give the picture, f_d is defined in the sentence that uses it, and every number
(20.25 s, 0.596 m at 8.0 s, τ = 6.4 s, ±0.482 m, 4.76 ×) matches the stored run. Exercise 6.1 works as written (checked: at
ζ = 0.01 the beats last the minute; at f = 0.20 Hz the ringing rides on the drive).

**(B)** "(with \(f_0\) in its place the estimate is 20 s, close enough at this weak damping)": an aside, but Exercise 6.1
uses \(1/|f-f_0|\), so it pays for itself.

**(C)** None.

**Verdict: clear.**

## 07 · Where the energy goes

**(A)** None. In, out and stored energy are named in words. The steady-state "sloshing" picture gives ⟨P⟩ = ½cΩ²X², and the
run's own W_in, W_loss and ΔE close the balance.

**(B)** For the graduate, (8) is "multiply (1) by \(\dot x\) and integrate". The verbal energy argument is a valid derivation,
so nothing is missing. 19.03 − 17.93 = 1.10 against the quoted 1.11 J is rounding (1.106 J).

**(C)** None.

**Verdict: clear.**

## 08 · Solve first, then play

**(A)** None. The integrator, step, step count, what is stored, how often, how a frame picks a row, and the measured error are
all stated and match the code.

**(B)**
- "Unlike the earlier figures": this means the earlier simulations (Figs. 1–8), not this note's Figures 1–4.
- STANDARD §4.5 also asks why RK4 and h = 1 ms, and where it fails. Not said. The measured 5 × 10⁻¹² m makes the case without
  words, so adding them is optional.

**(C)** "Measured in headless Chromium, the default solve took 9.5–12.4 ms; the time depends on the machine." This is lab-notebook
detail. The status line already shows the reader their own time (16.0 ms here).

**Verdict: clear.**

## 09 · On screen

**(A)**
- "The largest displacement is drawn as \(0.11W_0\) either side of rest." What this means for the reader is never said: the
  drawing is rescaled for every run (`sc = amp / xmax` in `geom()`), so every run's largest swing fills the same width.
  Exercise 4.1 asks the reader to find "the factor by which the amplitude fell" from ζ = 0.05 to 0.2. On screen the block
  swings exactly as far in both runs (77.44 px each side, checked). Only the ruler under the block changes, from ±1.01 m to
  ±0.25 m, and the note never mentions that ruler. A reader watching the block concludes nothing changed. This is the one place
  where the drawing differs from the model (STANDARD §4.6), and the note does not say it in words. Smallest fix: one sentence
  ("so every run fills the same span; the ruler under the block gives the metres").

**(B)**
- \(x_\mathrm{wall}\) and \(b_\mathrm{block}\) are never defined. They can be guessed from their subscripts, and they go
  away if (C) is taken.
- The rest of the paragraph (force arrow, dial and its shadow, the window and its 8.9 s, the overview strip, the Bode dot
  and ring) is good equation-to-screen mapping and matches what is drawn.

**(C)** The first three sentences: a pixel formula with three layout symbols and percentages measured on two canvas widths
(47.8 % / 50.0 %, 20.1 % / 19.4 %). They are far heavier than the point, which is that the block rests near the middle and
its largest swing spans about a fifth of the width. Replacing them with the sentence in (A) would make the paragraph shorter
and clearer at once.

**Verdict: needs work** (one sentence; the overload is the same spot).

## 10 · What the model leaves out

**(A)** None. Each limit (nonlinear spring, dry friction, ideal driver, ζ ≤ 0.9) is stated with its physical consequence.
§1's bridge gives the feedback case.

**(B)** "the resonance peak bends and can jump" is cryptic for a school student. Naming the next model (the Duffing
oscillator) in two words would meet STANDARD §4.7 exactly. Optional.

**Further reading:** all four sources are real, the chapters named are the right ones, and the links work (see the
Links paragraph above).

**(C)** None.

**Verdict: clear.**

---

## Summary

| § | Section | Verdict | (A) |
|---|---|---|---|
| 1 | A push from outside | clear | none |
| 2 | The model | needs work | ζ and "underdamping" used before definition in the ω_d clause |
| 3 ★ | The exact solution | needs work | C₁, C₂ used before the ringing form they multiply |
| 4 | Resonance and phase | clear | none |
| 5 ★ | The control engineer's view | needs work | X means both the transform X(s) and the amplitude X |
| 6 | The start: beats and decay | clear | none |
| 7 | Where the energy goes | clear | none |
| 8 | Solve first, then play | clear | none |
| 9 | On screen | needs work | per-run rescaling of the drawing never said; misleads Exercise 4.1 |
| 10 | What the model leaves out | clear | none |

Each (A) is fixed by one clause or one sentence. No section needs new paragraphs, figures or boxes. Separate from the
verdicts, Figure 3's label overflows its box.
