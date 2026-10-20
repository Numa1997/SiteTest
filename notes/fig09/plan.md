# Fig. 9 · Driven oscillator · plan

Page `public/simulations/driven-oscillator.html`, note L140–L453 (before any edit). Judged against notes/STANDARD.md §4,
with Numa's verdicts first: a clear section is not touched; where something is missing, the smallest change.

## Verdicts

| § | Section | Verdict |
|---|---|---|
| Abstract | | clear, leave it |
| 1 | A push from outside | clear, leave it. Swing, washing machine, loudspeaker, Millennium Bridge as the counter-example; Figure 1 defines m, k, c, F, x. |
| 2 | The model | clear, leave it. Forces, Newton, ω0, ζ, (1)→(2) (c/m = 2ζω0 is one line of algebra), default k and c (measured 9.8696 N/m, 0.31416 kg/s). |
| 3.1 | The steady state ★ | **needs work.** L218 "The modulus and argument of Z give the amplitude and the phase lag …" jumps from (3) to (4): it does not say that dividing by the denominator divides by its length and turns back by its angle, so φ is the angle of the denominator; `atan2` is used without a word for a school reader; and taking the real part of the complex solution is never justified (it works because every coefficient of (2) is real). |
| 3.2 | The transient ★ | **needs work.** L221 "The free equation has solutions that ring at … ωd … and die away with … τ" is asserted, and so is "demanding x(0) = ẋ(0) = 0 fixes its two constants". This is the one place where the meaning of the damping ratio (ζ = 1 is where ringing stops) can be derived, and it is not. |
| 4 | Resonance and phase | **needs work.** L320 "The true maximum sits slightly below ω0, at Ωr = ω0√(1−2ζ²) … for ζ ≥ 1/√2 there is no peak at all" is asserted without a step. Also a unit slip: Ωr is an angular frequency, but "which is 0.4987 Hz" is fr. The rest (static limit, inertia limit, (6), Q, phase story, Exercise 4.1) is clear. |
| 5 | The control engineer's view ★ | **needs work, one word.** L332 "their real part is the decay rate 1/τ": the real part of the poles is −ζω0 = −1/τ. The rest is clear and, after the 3.2 addition, the poles are the roots the reader has already met. |
| 6 | The start: beats and decay | text clear, leave it (numbers re-measured: beat 20.25 s, first swell 0.596 m at 7.99 s). **Exercise 6.1 needs work:** L409 "set f = 0.20 Hz, far from resonance, and use equation (5) to explain why the transient hardly shows" is wrong for this page. F = F0 cos Ωt switches on at full strength at t = 0, so C1 = −X cos φ ≈ −X: at ζ = 0.01, f = 0.20 Hz the ringing starts 1.00005 times as large as the steady motion, |x| reaches 0.224 m = 1.85 X at t = 5 s, and 15 % of the ringing is still there at 60 s (Node copy of the page code, `physics.cjs`). |
| 7 | Where the energy goes | **needs work, one clause.** L417 "Averaging over one period, ⟨Pin⟩ = ⟨Ploss⟩ = ½ c Ω² X²": the ½ and the Ω² come from nowhere for a school reader (speed amplitude ΩX, mean of sin² = ½). Numbers re-measured: 0.2917 W, 19.032 J, 17.926 J, 1.106 J, 1.27×10⁻¹². |
| 8 | Solve first, then play | clear, leave it. Matches the code line for line (RK4, 60 000 steps of 1 ms, every tenth state, 6 001 rows, nearest row, no interpolation). The solve time is hedged ("depends on the machine"); I re-measure it but do not change it. |
| 9 | On screen | **needs work.** L433 "Below, the stored run is drawn over its full 60 s, dark up to the present sample and pale after it, with F(t)/k dashed in burgundy and ±X dashed in rose" does not match the code: the dashed F/k and ±X, and x dark/pale, belong to a moving window chart, `win_T` = clamp(4/f, 6 s, 20 s) wide (L832), which the note never mentions; the 60 s strip under it (L810–L829) has no ±X and a solid F/k. Rest-position and span percentages re-measured. |
| 10 | What the model leaves out | clear, leave it. |
| 10.1 | Further reading | **needs work.** None of the three items has a link. |

## Changes (only these)

1. **3.1, L218.** Replace the one sentence with two short ones: dividing by a complex number divides by its length and
   turns back by its angle, so X = (F0/m)/|denominator| and φ is the denominator's angle, between 0° and 180° because its
   imaginary part 2ζω0Ω is positive (atan2(y, x) is the name in code for the angle of the point (x, y)); the coefficients of
   (2) are real, so the real part of the complex solution is the real motion X cos(Ωt − φ). No new equation.
2. **3.2, L221.** Before "Adding one to the steady state": try e^{st} in the free equation, s² + 2ζω0 s + ω0² = 0,
   s = −ζω0 ± iω0√(1−ζ²); real part → decay with τ, imaginary part → ringing at ωd; at ζ = 1 the root's imaginary part
   is zero and the ringing is gone. After it: the two starting conditions written out (X cos φ + C1 = 0 and
   XΩ sin φ − ζω0 C1 + ωd C2 = 0). Inline maths, no new display equation.
3. **4, L320.** Complete the square in Ω² as a new display equation `\tag{6a}`, then read off Ωr and the ζ ≥ 1/√2 case
   (bracket cannot vanish; the smallest denominator is at Ω = 0). Write "that is fr = 0.4987 Hz".
4. **5, L332.** "their real part is the decay rate 1/τ" → "their real part is −1/τ, the decay rate with a minus sign".
5. **6, Exercise 6.1, L409.** Replace the wrong last sentence by a correct one: at f = 0.20 Hz there are no slow beats, but
   the block's own ringing rides on the slow drive; use C1 of (5) to explain why it starts as large as the steady motion.
6. **7, L417.** Add the clause: the speed swings with amplitude ΩX and the square of a sine averages to one half.
7. **9, L433.** Replace the one wrong sentence: a window chart follows the present sample (4 drive periods, kept between 6 and
   20 s: 8.9 s with the defaults) with x dark/pale, F/k dashed burgundy, ±X dashed rose; under it a strip of the whole
   60 s with the window shaded.
8. **10.1.** Add a link to each item (pages opened: Google Books for Taylor, Routledge/CRC for French, the authors'
   electronic edition PDF for Åström & Murray, chapter 8 "Transfer Functions", 8.4 "The Bode Plot"), and one open item
   that a school student can read in full and that follows the same route as §3 and §7: Feynman Lectures Vol. I ch. 23
   (Resonance) and ch. 24 (Transients). The publisher page of Taylor (uscibooks.aip.org) did not open (connection reset
   through the proxy, 503 to WebFetch, tunnel error in Firecrawl); Google Books gives the same bibliographic data.

No equation is renumbered; the walkthrough and `<head>`, code and taps are untouched.

## Measurements (and how)

- `notes/fig09/physics.cjs`: the page's `steady()`, `exact()`, `accel()` and solve loop copied verbatim, run in Node:
  defaults, Exercise 4.1, Exercise 6.1 (both parts), first swell, transient size.
- `notes/fig09/derive.py`: SymPy checks of every step added (|Z|, arg, the roots, C1 and C2, the completed square (6a),
  X(ω0), the poles, ⟨P⟩).
- `notes/fig09/measure.cjs`: build to /tmp/fig09-dist, serve, Playwright + Chromium at 1440×900 and 390×844: the store
  after load (k, c, X, φ, τ, fr, Win, Wloss, balance, err_max, solve_ms, win_T, box_w, eq_px, amp_px), the Exercise 6.1 run
  through the sliders and Solve, then console errors, `.katex-error`, horizontal scroll, every fold opens.

## Outcome (after the edits)

- Changes 1–8 made as planned, all between `<article class="paper" id="paper">` and `</article>` (page L218, L221,
  L320–L322 with the new `\tag{6a}`, L334, L411, L419, L435, L448–L451). The page grew by 3 lines; every code line moved
  by +3. The doc's 177 line anchors were shifted (`shift_doc_links.py`) and checked to land on the same text as before.
- Chromium, 1440×900 and 390×844 (`measure-out.json`, baseline in `measure-before.json`): no console errors, no
  `.katex-error`, tags (1)–(6), (6a), (7), (8); scrollWidth = clientWidth (1440, 390) before and after opening the folds;
  14 of 14 folds close and open. On the phone, (3)–(8) and (6a) scroll inside their own box, as (3)–(8) already did.
- Store with the defaults, both widths: k = 9.8696 N/m, c = 0.31416 kg/s, X = 0.48194 m, φ = 25.346°, τ = 6.366 s,
  fr = 0.49875 Hz, win_T = 8.889 s, Win = 19.0317 J, Wloss = 17.9256 J, E(T) − E(0) = 1.1061 J, balance 1.27×10⁻¹²,
  err_max 5.26×10⁻¹² m, first swell 0.5962 m at 7.99 s; canvas 770 px (rest 47.8 %, span 20.1 %) and 356 px (50.0 %,
  19.4 %). Solve time this session: 3.1–34 ms for repeated solves, 18–86 ms for the first solve at load, with other agents
  building at the same time; the note's hedged "9.5–12.4 ms … depends on the machine" was left alone.
- Exercise 6.1 in the page: ζ = 0.01, f = 0.45 Hz: |x| reaches 0.919 m at 8.97 s; f = 0.20 Hz: X = 0.1206 m, |x| reaches
  0.2237 m at 5.00 s, "Measured, last 10 s" 0.1420 m (the ringing is still there at the end).
- New code bug found (report only): in the window chart the last time-tick label can overlap "t (s)": the label test
  `g.wx(v) < p.R - 34` (page L783) does not allow for the widths of the two labels; at ζ = 0.01, f = 0.20 Hz, sample 1500,
  1440 px, "20" ends 5.2 px inside "t (s)" (`tick_overlap.cjs`).
