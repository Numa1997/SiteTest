# Fig. 2 · Double pendulum · referee report

Blind reading of the lecture note in `public/simulations/Double Pendulum.html`, as a school student who is good at
mathematics and as a physics graduate. Not read: `plan.md`, `check.md`, any teacher report.

**How it was read.** Built with `OUT_DIR=/tmp/fig02-ref-dist npm run build` (rebuilt after the coordinator
said the page had changed; the built page is byte-identical to the working-tree file), served by a small Node static
server, opened in headless Chromium 1194 (Playwright) at 1440 × 900. All 15 folds report `data-collapsed="0"` after
*Expand all*. KaTeX rendered (134 formulas, no raw `\(`). Text read from the rendered DOM, with each formula's TeX
annotation. Screenshots in `notes/fig02/shots/`: `p-<section>-1440.png` is the whole section (pinned headers switched
off for the shot only), `p-<section>-1440-viewN.png` are window-sized frames, `p-head-1440.png` the title and abstract.

**Change since my first build.** Equations (5), (8), (9) and (13) are now broken over lines. Before, at 1440 px they
overflowed their boxes by 37, 331, 62 and 122 px, and in (8) the determinant `det = l₁l₂(m₁ + m₂ sin²δ) > 0` was cut off,
although the next sentence begins "The determinant can never vanish". Measured again on the current build: no display
equation overflows at 1440 px. (At 390 px thirteen displays scroll sideways, as KaTeX displays do on a phone; outside
this brief.)

Legend: **(A)** a reader genuinely gets lost, a step is skipped, a symbol is used before it is defined, a claim is wrong or
unsupported, a needed physical picture is missing. Only (A) decides the verdict. **(B)** taste. **(C)** longer or heavier
than its point needs.

---

## 01 · A pendulum on a pendulum — **clear**

The pen between two fingers, the swinging arm, the "two children on linked swings": exactly the sensory start the
standard asks for. Figure 1 defines every symbol it later needs.

(A) none.

(B)
- "a crane hook hanging from its cable" is a single pendulum; it is a double pendulum only with a load slung beneath the hook.
- "the computer solves them so accurately that over the first twenty seconds the energy stays fixed …" reads as if
  energy conservation proved accuracy; §06 later says it does not. The two sit a little at odds.
- "limits weather forecasts to about two weeks" has no source in 9.1. It is common knowledge, so this is taste.

(C) none.

## 02 · The model — **clear**

Assumptions, coordinates, degrees of freedom and the state are stated in plain words, with the page's values.

(A) none. (B) The default ratios (both 1) and the default start (120°, 150°, at rest) are given only later; one could
name them here. (C) none.

## 03 · Energy — **clear**

Each step is named (differentiate, square and add, the cosine identity, *mgy*). The train passenger and the
right-triangle case give the coupling term a real picture.

(A) none.

(B) The box and §07 call it "the *Drift* readout"; on the page it is labelled **Energy drift**.

(C) none.

## 04 · From energy to motion ★ — **clear**

I checked every line by hand: (5), p₁, the three derivatives in 4.2, (6), (7), the matrix and determinant of (8), the
three identities and the final form (9). All correct, and (9) is character for character what `deriv()` computes. The
physical reasons are there: rod forces do no work, so they drop out; each equation holds both accelerations because each
rod pushes on the other.

(A) none.

(B)
- δ means two things within three lines: the variation (δS, δθᵢ, δωᵢ) and then "δ = θ₁ − θ₂". A graduate copes; it is
  the one spot a careful student could trip.
- The Cramer's-rule sentence chains three identities and a parenthesis into one sentence, and the Cramer numerators
  themselves are not written. A graduate can fill them in, so this is taste for a ★ section.
- Hamilton's principle is stated as a principle, without motivation. That is fair for ★.

(C) none.

## 05 · Small swings: two normal modes — **needs work**

(A)
1. *"Substituting gives a solution only if the determinant of the combined matrix vanishes, 2(g/l − ω²)² = ω⁴, so"*
   This is the key step of a section **without** ★, and two things are missing. First, "the combined matrix" is never
   written down: it is (g/l)·diag(2, 1) − ω²·[[2, 1], [1, 1]], from (10) with θ̈ = −ω²θ. Second, the reason is not
   given: if the determinant were not zero, the only answer would be u₁ = u₂ = 0, a pendulum hanging still. A student
   who skipped §04, as the abstract allows, meets matrix language here with nothing to hold on to. One clause fixes it
   ("…otherwise the only solution is u₁ = u₂ = 0, no motion at all").

(B)
- ω returns with a new meaning. The sentence before (10) says "the ω² terms" (angular velocities); then "one common
  frequency ω" and ω∓ = 2.40, 5.79 rad/s are mode frequencies in the same units. Exercise 5.1 then talks about the
  angular-velocity sliders. A half-sentence saying that ω here is not ω₁, ω₂ would prevent a mix-up. "Frequency" for an
  angular frequency is also loose.
- θ̈ appears in (10) after §04 had called it α. The dot notation of (2) makes it guessable.
- (10) rests on (6) and (7) from the ★ section, so a reader who skipped ★ takes (10) on trust. That is acceptable.
- "Exercise 5.1 · on the figure above" comes right after the note's own Figure 2 (the mode sketch), while it means the
  simulation, which the page also calls "Fig. 2". "On the simulation above" would remove the double meaning.

Checked: ω∓ = 2.397 and 5.787 rad/s, periods 2.62 and 1.09 s, mode shapes ±√2, and ω₊/ω₋ = 1 + √2 is irrational. The
Figure 2 sketch draws 12° over 17° (ratio 1.42). All correct.

(C) none.

## 06 · Chaos — **needs work**

**Does §06 say WHY two nearby starts part ways? No.** The section shows *that* they part (Figure 3 and Exercise 6.1),
measures *how fast* (λ ≈ 1.4, then 1.45 per second, with the "×4.3 per second of forecast" reading), and says what
chaos is *not*. The only gesture at a cause is *"At larger angles the small-angle picture breaks down, and the nonlinear
sine and angular-speed terms matter."* That names the terms but gives no picture of what they do. Figure 3's most
striking contrast, the low-energy curve that never grows, is not explained either.

(A)
1. **Physical picture missing.** Quoted: *"At larger angles the small-angle picture breaks down, and the nonlinear sine
   and angular-speed terms matter. Some starts then show chaotic motion … The clearest sign is sensitive dependence on
   the starting state."* The section goes straight from here to measurement. A reader learns *that* and *how fast*,
   never *why*. Two or three plain sentences would supply it, and the measurements below support them:
   - *Small swings:* the equations are linear (§05), so the difference between two motions is itself a small swing
     that keeps its size. That is the flat lower curve of Figure 3. Measured with the page's equations and step: its
     largest value in 20 s is 1.44 mm, starting from 1 mm.
   - *Large swings:* the lower arm is carried up near the top again and again, and there it balances like a pencil on
     its tip. A hair more speed and it goes over; a hair less and it falls back. Each such moment magnifies the
     difference between the twins, and once one twin goes over while the other falls back, their motions are unrelated.
     Measured with the page's equations and step (default start, 2000 s, full-state separation shrunk back every 0.1 s):
     the separation grows at 2.2 per second while the lower rod is within 45° of straight up (19 % of the time, 29 % of
     the growth), against 1.44 per second on average and 0.6 per second when the rods are nearly in line. Growth comes
     in bursts: the fastest 10 % of steps carry 52 % of all stretching. So the picture should say "most strongly near
     the top", not "only there".
   The room can come from (C1) below, so the section need not grow.
2. *"The energy stays fixed while the trajectory wanders over everything that energy allows."* This is stronger than
   what is known or shown. It is the ergodic claim, and the double pendulum generally has a mixed phase space, with
   regular islands that a chaotic trajectory never enters. Nothing on the page supports it. "Over much of what that
   energy allows" is safe. One word.

(B)
- "Some starts then show chaotic motion, although high energy alone does not guarantee it." The reader is not told what
  else matters. A hedge, not an obstacle.
- "d" changes meaning mid-paragraph, from the distance between bobs to "the distance in the full state". The note does
  say "now". A graduate will also notice that a distance mixing rad and rad/s needs some scale; the limit does not
  depend on that choice, and half a clause could say so.
- *"Nor does a small energy drift guarantee more than itself"* is awkward wording. The clause after it makes the point
  well. "Predictability horizon" is used once and never defined, but it is clear from context.
- Exercise 6.1: "on the figure above" again means the simulation, not Figure 3 directly above.

(C)
- **C1.** In the second paragraph, from *"The proper calculation follows a tiny change of the whole state …"* through
  *"… so the rough reading was not far off."*: about 150 words plus the double-limit equation (12), all to say that a
  careful long run gives 1.45 per second, close to the 1.4 read off Figure 3. The sentences *"The 1.4 per second read off
  one pair of runs is a rough version of it: a finite stretch of time, and the distance between the lower bobs only, two
  of the four coordinates. It shows the sensitivity; it is not the full calculation."* restate the caveat twice. The
  whole paragraph does six jobs: fit, method, definition, caveat, practical meaning, and what chaos is not. The section
  spends its weight on method and none on the picture in (A1).
- **C2.** The closing sentence of this paragraph (a small drift does not make the positions true beyond the horizon) and
  the last bullet of §09 (after a few Lyapunov times the computed path is no longer the exact one) say the same thing.
  One of them is enough.

Checked: d first reaches 0.1 m at 4.06 s; a least-squares line through ln d up to then gives 1.39 per second; the
full-state exponent over 2000 s is 1.44 per second (the note's 1.45 is over 20 000 s); e^1.45 = 4.26 and e^14.5 = 1.98 × 10⁶.
All consistent with the note.

## 07 · Solving it step by step — **clear**

"Looks at the slope four times per step" is a good picture. Equation (13) matches `rk4()`. Error order, step size,
the measured drift and where the step fails (mass ratio 10) are all given, with a physical reason (the kick when the
rods straighten).

(A) none.

(B)
- Why RK4 was chosen is not said; the standard's item 5 asks for it. One clause would do.
- Numbers, re-run with the page's own `deriv`, `rk4` and `energy` code, extracted from the page:
  - The largest drift in the first 20 s, sampled at every step, is +5.00 × 10⁻⁸ at 8.67 s; the note says +4.7 × 10⁻⁸.
    The readout samples once per frame, which may explain the lower value.
  - The drift after 60 s is −7.2 × 10⁻⁸, which matches "about 7 × 10⁻⁸ a minute". After 600 s it is −8.0 × 10⁻⁷,
    where the note says "about −7 × 10⁻⁷"; the average rate is nearer 8 × 10⁻⁸ a minute.
  - With mass ratio 9.97, the drift reaches −3.66 × 10⁻⁴ within 20 s and peak |α| = 1388 rad/s². For equal masses the
    peak |α₁| is 75 rad/s². All of these match.
  Not reader obstacles, but the 10-minute figure's first digit is off.
- The second bullet is long (about 190 words), but every sentence carries a measured fact the standard asks for. It is
  dense but earns its place.

(C)
- **C3.** First bullet: *"Each frame advances by the real time elapsed multiplied by the Time scale, in steps of h, with
  a 600-step guard. The clock caps a frame at 0.05 s and the slider caps the Time scale at 1.5, so even including the
  carried remainder no more than 46 steps can be requested; the 600-step guard cannot act."* This is a code-audit
  detail: a reader is told about a guard that never acts, and "carried remainder" is undefined. Its point needs one
  sentence: each frame takes as many steps of h as the elapsed time times the Time scale requires, ten at normal speed.

## 08 · From metres to pixels — **clear**

Every drawn thing is tied to its symbol. The sign flip for screen y is explained. The trail's half-life (1.44 s) is
correct, and the bob sizes "as for balls of the same material" give a physical reason.

(A) none. (B) "− 34" in σ is an unexplained number; "a 34-pixel margin" would say what it is. (C) none.

## 09 · What the model leaves out — **needs work** (one small item)

(A)
1. *"After a few Lyapunov times the computed path is no longer the exact path from that start"*: "Lyapunov time" is
   never defined. §06 defines only the exponent λ, and a school student cannot know that the Lyapunov time is 1/λ ≈ 0.7 s.
   Fix with a parenthesis: "(1/λ ≈ 0.7 s)".

(B)
- "it is a faithful example of how the pendulum can move" and "Averages over many swings are usually robust" are
  plausible (shadowing), but unsupported.
- Strogatz is cited without a chapter.
- All three links open (HTTP 200: Google Books for Taylor and Strogatz, Elsevier for Landau–Lifshitz). Taylor's chapters
  7, 11 and 12 and Landau §5 problem 1 are the right places.

(C) see C2 (overlap with §06).

---

## Verdicts

| Section | Verdict | (A) |
|---|---|---|
| 01 A pendulum on a pendulum | clear | — |
| 02 The model | clear | — |
| 03 Energy | clear | — |
| 04 From energy to motion ★ | clear | — |
| 05 Small swings | needs work | determinant step: "combined matrix" not written, "only if" not explained |
| 06 Chaos | needs work | no physical picture of *why* nearby starts part; "wanders over everything that energy allows" overstated |
| 07 Solving it step by step | clear | — (C3 overloaded bullet) |
| 08 From metres to pixels | clear | — |
| 09 What the model leaves out | needs work | "Lyapunov time" undefined |

Every fix named above is a clause or a few sentences. In §06 the picture can replace part of C1 rather than add to it.
