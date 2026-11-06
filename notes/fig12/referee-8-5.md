# Referee report · Fig. 12, subsection 8.5 "Seeing the swing: two level probes and a Kalman filter" (with 8.4 as context)

Read blind, as rendered, by a reader who knows ODEs, linear algebra and basic probability and has never met a Kalman filter.
No plan or check file was read. Nothing but this file was changed.

**How it was read.** Working tree of 6 November 2026, `public/` served with `notes/fig12/serve.cjs` (the `_headers` of the live
site), opened in headless Chromium at 1280 × 900 and 390 × 844, "Expand all" pressed. Section 8 shows 0 KaTeX errors and no
sideways scroll. Screenshots are in the session scratchpad
(`/tmp/claude-0/-home-user-SiteTest/91e62847-1a1a-5a7d-b603-4662585b11e7/scratchpad/shots/`: `desk-00…08.png` for 8.4–8.5 at
1280 px, `phone-00…15.png` and `ph-eq-50…53f.png` at 390 px, `stage-slosh-live.png` for the figure running with slosh feedback).
Arithmetic was rechecked in Python; the results are quoted where they matter.

Severity: **A** wrong or misleading as printed; **B** the target reader gets lost here; **C** polish.

---

## Verdicts against `notes/STANDARD.md`

| Standard item | 8.4 (context) | 8.5 |
|---|---|---|
| 1 Physical picture | Thin. "The first knows the road. The second knows the stout." is good; the LQR has no picture (what the gains do to the glass is said only after the poles). | Good for the probes (the hand that feels the stout front and back; the capacitive strip). Missing for the filter itself: the "trust the model or trust the sensor" idea arrives only in the last clause of a long paragraph. |
| 2 Model stated | Yes, as the matrix (51). Symbols from (35) and (17) are not recalled. | Mostly: one mode, linear, white Gaussian noise. The noise levels the filter assumes are not reasoned (see B6). |
| 3 Derivation, no silent step | `K = B^TP/r` and (53) are bare results. | The discretisation (53c), \(Q_d\), the covariance step (53d) and the gain (53e) are all bare. Not starred, though this is the heaviest material in section 8. |
| 4 Checks | Damping ratio of the poles, yes. | No limiting case of the gain, no check that 0.30 mm = 0.8 mm/√7. One number does not check (A3). |
| 5 Numerical method as the code does it | Riccati flow, yes. | Yes: 1 ms sample, exact exponential, Van Loan, Joseph form, the five-sample cycle. Good. |
| 6 Equation to screen | Table 3 only. | The strips and white dots are named and the figure shows them (checked). The lean chart "probes · estimate" and the portrait "estimate \(\hat q\), \(\hat{\dot q}/\omega\)" that the figure draws in this mode are not mentioned. |
| 7 Limits | n/a | Present and honest (one mode, breaking). Two numbers in it do not hold together (A3, A4). |
| 8 Sources | Bryson's rule uncited. | Kalman 1960 and Taylor 1953 are cited in the text but are **not** in section 16; Van Loan, Joseph, the separation principle have no source at all. |
| 21 Oct verdict (Taylor style: one symbol one meaning, Key result box, worked example, ★, no Q&A) | Needs work. | Needs work: seven symbol collisions (A2), no Key result box, no worked example, no ★, one Q&A-style lead ("Why these formulas: …"). |

**8.4: needs work (small).** **8.5: needs work.** The content is right in its large lines and the probe picture is good; the
reader gets lost on the order of the Kalman material, on reused symbols, on one wrong cross-reference, and on the phone layout of
the displays.

---

## 8.5 paragraph by paragraph

### Opening paragraph (the probes)

- **B.** "at the radius of the surface, \(r_p = R(h)\)": \(R(h)\) and \(h\) are not recalled. The reader of 8.5 needs "the glass's
  radius at the height \(h\) of the still surface (section 2)".
- **B (physical picture missing).** Why *two* probes and the *half difference*? The physical reason is the best one in the
  section and is never said: one probe also sees the whole level rise and fall (the bounce, the axisymmetric modes, the stout
  lost to a spill); the difference of front and back cancels all of that and keeps only the side-to-side swing.
- **C.** "a capacitive strip does exactly this" — good. "the white dot on each is the height it reads now" — checked in the
  running figure; it holds.

### "The measurement." and (53a)

- **A2 (symbol).** \(J_1(\xi)\): \(\xi\) here is the first zero of \(J_1'\) (it is \(\xi_{11}\) later in the same section, and
  \(\xi_i\) is the integral of the speed error in 8.4 and 8.5). Three meanings of \(\xi\) inside the reader's path.
- **B (skipped step).** "at the wall, \(r = R\), it is \(q\cos\theta\)" needs "because \(kR = \xi\)". Also, that mode shape is the
  upright cylinder's of section 4; the probes are on a tulip glass. One clause should say the half difference is still the
  mode's amplitude there, or how \(q\) is defined for the tulip.
- **B.** "\(q_2 + q_3\) at the wall in the live model": why exactly \(q_2 + q_3\) (each mode normalised to its wall height) is not
  said, and "the live model" is not defined anywhere before this point in the note except a table caption in 8.4 (see B10).
- **B.** "in the live model, (55)": a forward reference to an equation the reader has not met.
- **B6 (claims without reason).** "adds Gaussian errors of 1 mm to each probe reading and 0.2 mm/s to the speed" — say
  "standard deviation". Then "The filter assumes \(\sigma_q = 0.8\) mm and \(\sigma_v = 2\) mm/s." The reader computes: 1 mm on
  each probe gives \(1/\sqrt2 = 0.71\) mm on the half difference; the one-mode miss \(e\) is "1–2 mm rms". Why 0.8 and not ~2?
  And why \(\sigma_v\) ten times the noise actually added? No reason is given for either.
- **B.** "about an offset of 0.39 mm": why does the stout lean 0.39 mm at rest (grid asymmetry?), and does the filter see it as a
  swing? Not said.
- **B (model mismatch unspoken).** \(e\) is the higher modes, i.e. an oscillation at other frequencies, not white noise. The filter
  treats it as white (the second row of \(H\) is \((0,1,0)\), which ignores \(e\)). One sentence should own that.

### "The model the filter carries." and (53b)

- **B (silent step).** "the speed itself rather than its error, so the set speed does not enter": going from \((\delta v, \delta i)\)
  to \((v, i)\) is exact only if \(b\,i_0 = c_x v_0\) (the open-loop current balances a drag that is linear in speed). Say so, or say
  where any remainder goes (into \(F_d\)).
- **C.** "The first and third rows of (51) give" — the second row (\(\dot q = \dot q\)) is used too.
- **B.** \(M_x, c_x, b, \beta, \gamma\) are not recalled in 8.4 or 8.5; the reader must go back to (35) and (17). One line in 8.4
  ("\(M_x\) the mass that moves along the road, \(c_x\) its drag coefficient, \(b\) the motor's force per ampere, \(\beta\) how
  strongly the glass's acceleration drives mode 1") fixes both subsections.
- **B7 (undefined term).** "white noise of intensities \(W_F = 0.5\ \mathrm{N^2\,s}\)": "intensity" of continuous white noise is not
  defined (\(\langle w(t)w(t')\rangle = W\delta(t-t')\)), and the rule the two justifications use is not stated: an impulse
  accumulated over a time \(\tau\) has variance \(W\tau\), so \(W \approx (\Delta p)^2/\tau\) and a rate drifts by \(\sqrt{W_a T}\).
  With that sentence both checks become readable (they are right: 0.625 N² s; 0.025 m/s per period).
- **B.** "on 2.5 kg": is that \(M_x\)? Say so.
- **A2 (symbol).** \(W\) appears in (53c) as a matrix (\(GWG^T\)) but is only ever given as two scalars \(W_F, W_a\). Write
  \(W = \mathrm{diag}(W_F, W_a)\).
- **C.** "the bump first shows up as a jump in the speed, and the filter infers at once the swing that this push must start" —
  the best physical sentence of the section. Keep it.

### The parameters

- **A3 (number does not check).** "A filter tuned to the continuum's 3.42 Hz would drift out of phase with the 3D stout by a
  sixth of a swing every five swings." With 3.421 and 3.214 Hz, five periods of the 3D stout last 1.556 s, and the slip is
  \(0.207 \times 1.556 = 0.32\) of a period: a third, not a sixth. It is a sixth only if "swing" means half a period, which the
  note nowhere says (elsewhere "swing" is the whole oscillation).
- **C.** "the tulip on the 4 mm grid": "tulip" (the glass) is jargon to someone who opens 8.5 directly.

### "Exactly over one sample." and (53c), Van Loan

- **B (silent step).** (53c) is given without the one line that produces it: variation of constants,
  \(\mathbf z(t_k) = e^{A_zT_s}\mathbf z(t_{k-1}) + \int_0^{T_s} e^{A_z s}\,[B_z i + G\mathbf w(t_k - s)]\,ds\), and for \(Q_d\) that the
  double integral collapses because \(\mathbf w\) is white. The reader knows ODEs; this is exactly the step they can follow.
- **A2 (symbol).** \(\mathbf w_k\) in (53c) is a 3-vector increment of the state with covariance \(Q_d\); \(\mathbf w\) in (53b)
  is a 2-vector \((F_d, a_q)\) in N and m/s². Same letter, different object and units.
- **B (notation).** "\(\exp\big[\begin{smallmatrix}A_z & B_z\\0&0\end{smallmatrix}\big]T_s\)" reads as \(\exp(M)\cdot T_s\); write
  \(\exp(M T_s)\). The two inline `smallmatrix` blocks are too small to read on both screens; in the Van Loan one the
  superscript of \(GWG^T\) touches the bracket (desk-05.png, phone-09.png). These two block matrices want a display line.
- **B.** "the data panel checks all three by integrating the matrix equations again with Runge–Kutta" — which matrix equations
  (\(\dot\Phi = A_z\Phi\), …)? Not said.
- **C.** "the exact form costs nothing and leaves no doubt" — filler.
- **Standard (★).** This paragraph and Van Loan are graduate material in an unstarred subsection; star them and restate the
  result (\(A_d \approx I + A_zT_s\), \(Q_d \approx GWG^TT_s\)) unstarred.

### "Predict, then correct." (53d)–(53f)

- **B3 (order; the main teaching problem).** The reader who has never met a Kalman filter gets the full matrix recursion first,
  and the idea that makes it click last, in one clause: "(53e) is the familiar weighted average of two Gaussians: with one state
  and one sensor, \(L = P^-/(P^- + \sigma^2)\)". It is not familiar to this reader. The scalar case should come *before* (53d):
  a prediction with variance \(P^-\), a reading with variance \(\sigma^2\), the mix of least variance moves toward the reading by
  \(P^-/(P^-+\sigma^2)\) and has variance \(P^-\sigma^2/(P^-+\sigma^2)\); the two limits (\(\sigma\to0\): believe the probe;
  \(\sigma\to\infty\): ignore it). Then the matrix equations are that, in three dimensions. A worked example with the page's
  \(\sigma_q = 0.8\) mm would also give the "Example 8.x" the 21 October verdict asks for.
- **A2 (symbol).** \(P\) is the Riccati solution in (53) of 8.4 and the error covariance here, two paragraphs apart.
  \(R\) is the glass's radius (\(r = R\), \(R(h)\), \(R/\xi_{11}\)) and the measurement covariance \(R = \mathrm{diag}(\ldots)\) in
  the same subsection. \(r\) is the radius, \(r_p\), and the LQR effort weight. \(Q\) (LQR weight) and \(Q_d\) (noise covariance)
  invite the same confusion.
- **B.** "its covariance \(P\), the uncertainty it believes it has": covariance *of what*? Say \(P = \mathrm{E}[(\mathbf z-\hat{\mathbf z})(\mathbf z-\hat{\mathbf z})^T]\).
- **B (silent step).** \(P^-_k = A_dP_{k-1}A_d^T + Q_d\) needs the one probability fact the reader has:
  \(\mathrm{cov}(A\mathbf x + \mathbf w) = A\,\mathrm{cov}(\mathbf x)A^T + \mathrm{cov}(\mathbf w)\) for independent \(\mathbf x, \mathbf w\).
- **C.** \(\mathbf y_k\) is never written out: \(\mathbf y_k = y_v\) or \((y_v, y_q)\).
- **C.** The superscript minus ("before the reading") is never named.
- **Q&A form.** "Why these formulas: for a linear model with Gaussian noise, …" is a question-and-answer lead. Rephrase as a
  statement.
- **Standard (sources).** "Kalman's 1960 result" and "Joseph's form" are cited in words only; neither is in section 16.
- **A (equation numbering).** Hanging the filter on the Riccati equation's number (53a–53f) tells the reader these are
  sub-cases of (53). They are not.

### The steady gains

- **B8 (misleading picture).** "The filter thus averages about seven probe readings: it smooths the probes' noise without lagging
  a swing of 0.3 s period by much." A plain average of seven readings spans 35 ms, about 40° of a 3.2 Hz swing: that *is* a large
  lag. The Kalman estimate does not lag because the prediction step carries the oscillation forward between readings. That is
  the reason, and it is the whole point of using a model; it should be said.
- **C (check missed).** \(0.8\ \mathrm{mm}/\sqrt7 = 0.30\) mm, the standard deviation quoted. Say so: it confirms the "seven
  readings" reading.
- **C.** "settles into a cycle of five samples" — add "because \(H\) changes every fifth sample".

### "The regulator on the estimate."

- **A1 (wrong cross-reference).** "The current is (53) with the estimate in place of the state" — (53) is the algebraic Riccati
  equation. The control law \(u = -K\mathbf x\) of 8.4 has no number. Number it and cite that.
- **B (claim without support).** "\(\xi_i\) being the controller's own integral, which it knows exactly": 8.4 defines
  \(\xi_i = \int(v_0 - \dot x)\,dt\) with the *true* speed, and the controller only has \(y_v = v + n_v\). It is exact only if it
  integrates encoder counts (distance) rather than speed. Say which.
- **C.** \(K\,(\hat v - v_0, \hat q, \hat{\dot q}, \xi_i)\) multiplies a row tuple; write the column or a transpose.
- **B (graduate).** "the cost (52) splits into the cost with perfect state knowledge plus a term set by the filter alone": with
  noise, (52) is infinite. The statement holds for the expected cost per unit time. Also: the optimality is for the model, not
  for the 3D stout (one mode, \(e\) not white), which the reader will ask about after the next paragraph. No source given.
- **C.** The estimator's own poles are not given, so the reader cannot see that the filter is faster than the regulator it feeds.

### "What it does to the 3D stout." and Table 3a

- **B9 (lean vs swing, factor 2).** Figure 2 of 8.3 defines the lean as front minus back, i.e. \(2q\) at the wall; \(y_q\) is
  *half* that. "Fit … to the probes' lean", "the filter's estimate follows the probes' lean to 0.7 mm rms", Table 3a's "lean
  45 mm", "a lean of 42 mm": the reader cannot tell which quantity each number is.
- **B.** The test is introduced with the 25 mm bump only; Table 3a's first row is a 10 N push for 0.3 s, never introduced.
- **B.** "Open loop stays: ζ = 0.000" and "0.012" against the grid's ζ = 0.008 quoted a paragraph earlier: unexplained.
- **B.** "PI switched on: still swinging, 34.9 mm" for the bump is *worse* than open loop (27.3 mm). A striking result with no
  word of explanation.
- **C.** Column head "Open loop stays" is hard to parse; the fit window "the next 1.45 s" and the caption's "last second of 3.5 s"
  are two windows the reader must reconcile.
- **B.** Three rms misses of estimate against probes appear: 0.7 mm ("on from the start"), 2.2 mm ("for the push"), 3.9 mm ("the
  bump"). Which run each belongs to is not clear.
- **A4 (contradiction).** "The swing does not die to nothing: 3–6 mm rms stays, a little above what the probes read at rest" —
  at rest the probes read 0.39 ± 0.08 mm (opening paragraphs). 3–6 mm is ten times that, not "a little above".
- **A3' (wrong frequency for the limit).** "at an amplitude \(a = g/\omega^2 = R/\xi_{11} = 21.2\) mm, a lean of 42 mm" uses the
  continuum's 3.421 Hz. The 3D stout under discussion swings at 3.214 Hz, for which \(g/\omega^2 = 24.1\) mm, a lean of 48 mm. As
  printed, the push case (lean 45 mm), offered as the well-behaved one, is already past the breaking limit. Also
  \(g/\omega^2 = R/\xi_{11}\) holds only for \(\tanh(\xi h/R) = 1\); say "deep stout".
- **A2 (symbol).** In this paragraph \(a\) and \(b\) are fit coefficients; \(b\) is the motor constant in (53b) a page up, and
  \(a\) is next used as the wave amplitude (\(a\omega^2 = g\)).
- **B (physical picture missing).** "A wave whose crest accelerates downward faster than \(g\) breaks": why \(g\)? The surface at
  the crest is pulled down by gravity alone, so it cannot fall faster than free fall; when the swing asks for more, the crest
  parts from the wave. One sentence.
- **C (sentence).** "The regulator still calms the stout, because its errors are of the size of the swing it is removing, not
  larger." Vague; what errors, measured how?
- **Standard (sources).** "(Taylor 1953)" is not in section 16.

### "Slow motion."

- **B (parse).** "so with the 3D model the figure runs in slow motion and says so: *SLOW MOTION ×0.27* in the figure, the rate
  measured on your computer, in the caption." Two places, two numbers (0.31 in the text, 0.27 in the example) and the reader
  cannot tell that 0.27 is only an example. Split the sentence; say the number shown depends on the computer.
- **C.** This paragraph is about the display, not about seeing the swing; it would sit better in section 14.

### Phone layout (390 px)

- **A5.** KaTeX breaks the displays across lines at operators, and on the phone this produces misreadings:
  (53a) ends its second line with "\(+\)" and the third line reads "\(n_q = q + e + n_q\)" (ph-eq-53a.png);
  (53e) breaks inside \((HP_k^-H^T +\) / \(R)^{-1}\) (ph-eq-53e.png); (53b) puts "\(B_z\)" at a line end and "\(= \frac{b}{M_x}(\ldots)\)"
  on the next, likewise \(G\) (ph-eq-53b.png); (53c) strands "\(+\)" before \(\mathbf w_k\) (ph-eq-53c.png). Split each into
  separate displays or aligned rows so each line is a whole statement.

### Equation to screen

- **B.** With slosh feedback on, the figure draws a lean chart "probes · estimate" and a portrait "estimate \(\hat q\),
  \(\hat{\dot q}/\omega\)" (stage-slosh-live.png). 8.5 never points to them; one sentence would let the reader watch the filter
  work.

---

## 8.4 (context only)

- **B.** \(K = B^TP/r\) and (53) are given as results with no reason or ★ derivation (Taylor's way: at least the variational idea,
  or a starred sketch and a source).
- **B.** \(M_x, c_x, b, \beta, \tau_i, z_a'\) are not recalled (see 8.5 above).
- **C.** "Here \(2\zeta\omega\) is written in the matrix as one entry." Its purpose is unclear; delete or explain.
- **C.** "(Cart.lqrGains, 0.2 s)": 0.2 s of integration time or of computing time?
- **B10.** "the page uses that path in both models": "both models" (live modal model and 3D solver) are not defined before this
  sentence in the note's own text.
- **C.** Bryson's rule has no source.
- Numbers checked: ninefold (7.6/0.8) and fifteenfold (7.6/0.5) hold; damping ratios 0.81 and 0.83 hold.

---

## Top items, in order of severity

1. **A1** "The current is (53) with the estimate in place of the state": (53) is the Riccati equation; the control law has no number. The 53a–53f numbering also makes the filter look like part of (53).
2. **A5** Phone layout: (53a) wraps so that a line reads "\(n_q = q + e + n_q\)"; (53e), (53b), (53c) also break mid-expression.
3. **A2** Seven reused symbols on the reader's path: \(R\) (radius / noise covariance), \(P\) (Riccati / error covariance), \(\xi, \xi_{11}, \xi_i\), \(b\) and \(a\) (motor constant, amplitude / fit coefficients), \(\mathbf w\) vs \(\mathbf w_k\), \(r\); \(W\) used as a matrix but never defined as one.
4. **A3 / A3' / A4** Numbers that do not hold together: "a sixth of a swing every five swings" (it is a third); a breaking limit taken from the continuum's 3.421 Hz (lean 42 mm) for the 3D stout at 3.214 Hz (lean 48 mm), which puts the "good" 45 mm push past breaking; "3–6 mm … a little above what the probes read at rest" (0.39 mm).
5. **B3** The Kalman filter is taught backwards: the matrix recursion first, the scalar idea last in one clause called "familiar"; (53c), \(Q_d\), (53d) and (53e) are bare; no ★, no Key result, no worked example.
6. **B8** "averages about seven probe readings … without lagging much": a seven-reading average lags about 40°; the reason the filter does not lag (the model's prediction) is missing.
7. **B6 / B7** Noise choices without reasons (\(\sigma_q = 0.8\) mm vs 0.71 mm plus 1–2 mm of \(e\); \(\sigma_v\) ten times the added noise); white-noise "intensity" undefined; \(e\) is coloured, treated as white.
8. **B9** Lean (front minus back, \(2q\)) and swing (\(q\)) are used interchangeably in the numbers and Table 3a.
9. **Sources** Kalman 1960 and Taylor 1953 cited in the text, absent from section 16; Van Loan, Joseph, Bryson, separation principle unsourced.
10. Smaller: "\(\xi_i\) … which it knows exactly" unsupported; "the set speed does not enter" hides \(b i_0 = c_x v_0\); Table 3a's push row and PI-worse-than-open-loop unexplained; "Why these formulas:" is Q&A form; the figure's probe/estimate chart and portrait are not mentioned; the Slow-motion sentence does not parse.
