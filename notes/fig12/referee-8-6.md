# Referee report · Fig. 12, note §8.6 "Which motions of the stout each motor and spring can reach, and how many we need ★"

Read as rendered: built with `vite build` into a scratch folder, served locally, opened in headless Chromium (Playwright) at
1280 × 900 and at 390 × 900 (2× pixels), with every fold of the note opened, and screenshotted from the 8.6 heading to the start
of §9 (`#p-susp`). KaTeX errors on the page: 0. At 390 px, Table 1 and Table 2 (earlier sections) are wider than their box.
Nothing in §8.6 overflows. Background read: §3, §4.5 (17), §6.1–6.7, §8.4, §8.5, §9, §11.8 (54), §11.9 (N1–N5), §15.
I did not read plan.md or check.md.

Two readers speak below. **S** is a school student who is good at mathematics. **G** is a physics graduate.
I checked numbers against the page code (`public/scripts/stout-cart.js`, `Cart.prototype.sample` and `suspGains`) and against the
stored runs in `notes/fig12/runs/springs-*.txt`. I also re-solved the suspension Riccati equation with SciPy, using the code's
A, B, Q, N and R.

---

## 1 · Paragraph by paragraph

### Opening (the coffee carrier)

- "When you step down from a kerb, your knees bend so the cup does not drop with your body." **S and G:** This picture works
  against the section's own physics. Two sentences later the note says a vertical push leaves a flat surface flat. So why do the
  knees matter? The real reason is missing. Stepping down puts the body briefly close to free fall, so a_z → −g and the apparent
  gravity 1 + a_z/g goes to zero: the coffee stops being held down. The knees keep a_z small. Say that in one clause, because it
  is exactly the mechanism of the washboard failure later (§6.7: "gravity in the glass's frame swings between nearly zero and
  twice g").
- "They are different jobs because the two jolts act on the liquid in different ways." Fine as a promise, but the promised reason
  only arrives in the next paragraph. Fine.

### "Two ways to shake a liquid" (B1)

- "Its first sloshing mode obeys (54)". **Forward reference.** (54) is in §11.8, three sections later. A reader of §8 knows the
  same equation as (17) (§4.5) and (R3) (§6.7). Cite (17) and (R3), or say "(17) with damping; written for every mode as (54)
  in §11.8".
- In (B1), ω, ζ and β have no subscript. Earlier the note wrote ω₁₁ (17) and ω₁ / ζ₁, and β changes value between the cylinder,
  the live model and the 3D grid. One clause is needed: "ω, ζ, β of mode 1 (3.421 Hz, 0.0053, 1.541 in the live model; 3.214 Hz
  on the 4 mm grid)".
- "a vertical acceleration acts on the liquid exactly like a change of g". Correct. The step that makes it obvious is not written:
  in the glass's frame the body force is −(g + a_z) ẑ, so g appears only as g + a_z. One line would do.
- "Section 6.7 showed what a parametric drive does when it beats at twice the swing's frequency". **S:** "beats" already has a
  meaning in this subject (two tones beating). Use "when it shakes at".

### "Which modes each push reaches"

- **Symbol used before it is defined:** ψ_mn(r). It appears nowhere else on the page. §4.5 writes the mode shape only for
  m = 1 as J₁(kr). Define it: ψ_mn(r) = J_m(ξ_mn r/R), the radial shape of mode (m, n).
- "enters the forcing of mode (m, n) through the overlap ∬ x ψ_mn cos mθ dA (section 4.5)". §4.5 never uses the word
  "overlap" and never writes this general integral. It does it only for (1, 1). Say "the projection of §4.5, done for any
  (m, n)".
- **Skipped case.** "∫cos θ cos mθ dθ = 0 unless m = 1" covers only the cos mθ family. The next sentence also rules out the swing
  across the road (sin θ). That needs ∫cos θ sin mθ dθ = 0 for every m. Add it.
- "whose overlap ∬ψ_mn cos mθ dA vanishes for every mode that conserves volume". **S and G:** every sloshing mode conserves
  volume, so "every mode that conserves volume" reads as if some do not. The physical step is also missing: a vertical
  acceleration is the same everywhere on the surface, so it projects onto ∬η dA, the change of volume, which is zero. Write
  that.
- "They are reached only through the nonlinear terms of (N4)–(N5) ... or parametrically." Another forward reference (§11.9).
  "Parametrically" is also loose: a parametric drive multiplies a swing that is already there. It cannot start a mode from
  rest. Say "or, once already present, pumped parametrically".

### "Which actuator reaches which" (controllability)

- **Symbol clashes. One symbol should have one meaning, and here several do not:**
  - u is the suspension force here. In §8.4 and §8.5, eq. (51)–(52) and (K7), u = δi is the motor current. §6.3 called the
    suspension force u_s. Both meanings sit in the same subsection, because "the slosh LQR of section 8.4" is reused.
  - A and B here are the matrices of a plant that is never written. A in (51) is a different matrix.
  - N in the Riccati equation is the cross-weight. N is the tyre load in (23), and §8.4 uses N̂.
  - R is the effort weight. R is the glass radius in (17) and (54).
  - Q is the state weight. Q_Y is the generalised force in §6.3.
  - d is the tyre compression. Bold **d** is the filter's disturbance in (K3).
  - s is the stroke. s is the Laplace variable in (38) and an integration variable in (K4).
  - **y** is the suspension state. y_q and y_v are measurements in (K1).
  - "the Kalman test for controllability" sits right after the Kalman filter of §8.5. **S** will think it is part of the
    filter. Add "(the same Kalman, a different result)".
- **The suspension block's A and B are never shown.** The reader is asked to accept that "its column of B and every power of A
  times it have zeros in the swing's rows", but never sees the matrix. The code (`suspGains`) has a 4×4 A and
  B = (0, 1/M_s, −1/m_w, 0) in y = (s, v_b, v_w, d). Write them, or write the combined 8-state block-diagonal A and B, so the
  zero pattern can be seen.
- "Linearised about a still stout, q = 0, the parametric term vanishes". **G:** the reason it drops is that ω²(a_z/g)q is a
  product of two small deviations, so it is second order. That is not the same as "q = 0". Say "is a product of two small
  quantities and drops out at first order".
- "the plant splits into two blocks". **Unsupported on a sloped road.** The road's push (24) is F_road = −N z_a′. N, the tyre
  load, is set by the suspension through (23) and (29). So on any slope, which is every bump, every ripple and every sett, the
  suspension force changes a_x. §8.4 says so itself: "only the error −(N − N̂) z_a′ reaches the cart, the part of the tyre load
  that the body's bounce adds". The blocks split only on a flat road, z_a′ = 0. Say so. As written, "Each disturbance has its
  own actuator" is too strong.
- "the swing is not controllable from the suspension ... The suspension can only change how strongly the road pumps a swing that
  the motor did not prevent." **G:** true for the linearisation, and false for the real (bilinear) system. Once q ≠ 0, the term
  ω²(a_z/g)q lets the suspension take energy out of the swing. Modulating a_z at 2ω with the opposite phase to Faraday pumping
  (the power term −ω²(a_z/g)q q̇ of §6.7 with its sign reversed) damps the swing parametrically. With 40 N on 1.93 kg the
  actuator can reach |a_z| ≈ 20 m/s², about 2g, so this is not small. One sentence should separate "not controllable in the
  linearisation" from "cannot act on the swing".
- "Conversely the motor cannot remove a_z at all: no current changes the body's height." **G:** true at any one instant, but the
  motor sets the speed, and the speed sets the frequency at which the road feeds the body. The section's own failure is a speed
  effect: 0.85 m/s puts the ripples at the 2.8 Hz bounce. The runs show the motor already moves the spring a great deal on the
  washboard: stroke rms 7.5 → 14.2 mm at 0.7 m/s and 11.1 → 23.4 mm at 0.85 m/s, open loop → slosh feedback
  (`springs-nm-washboard.txt`). So "no current changes the body's height" is contradicted by the table one paragraph later. See
  "Does it work?".
- "(for every mode n with β_n ≠ 0 and distinct frequencies)". Correct (I checked: rank 4 for the 4-state block of (51) with
  the page's numbers). But the LQR of §8.4 is designed on mode 1 only. Modes 2 and 3 are controllable and uncontrolled. Say so,
  because (B3) pushes along x and so also drives modes 2 and 3 through β₂ and β₃.
- "the road's slope pushes along x, in the motor's channel (which is why the slosh feedback of section 8.4 can cancel it)".
  "Cancel" is the word §8.4 uses for road *preview*. Feedback reduces the push's effect; it does not cancel it. Use "can fight
  it".

### "Which sensor sees which"

- "their half difference holds the modes odd in cos θ". **S:** "odd in cos θ" has no clear meaning. What is meant is "odd under
  θ → θ + π", that is odd m (m = 1, 3, …). Likewise "even in θ (m = 0, 2)" means even m. Half the sum also contains the fill
  level h.
- **Sensors left out.** The suspension LQR is full-state feedback on y = (s, v_b, v_w, d). The code reads "the stroke (a
  potentiometer), the two vertical speeds (accelerometers, integrated), the tyre's compression from the axle's load cell,
  d = (N − N₀)/k_t (the tyre damper's share ... left in it: a sensor error)", all of them exact and noise-free. This paragraph
  promises to list what sees what, yet names only the probes, the encoder and the accelerometer. Four more sensors (and the
  sensor error the code itself admits) belong here. §15 does say "the speed and body-speed sensors are ideal". The accelerometer
  is ideal too (`this.azMeas = this.azb`, no noise even with the noise switch on). Say so.

### "One design for both" (B2), (B3)

- "The cost of (52) is extended by the heave." **S:** "heave" (vertical acceleration of the glass) has not been defined at this
  point. §6.7 uses it without defining it either. Define it here: heave = a_z, the glass's vertical acceleration.
- **"One design" / "one LQR" is not what is computed.** The motor's gains are the unchanged slosh LQR of §8.4 (`lqrGains`). The
  suspension's gains come from a separate Riccati solve (`suspGains`). The two costs add, and the linearised plant is
  block-diagonal, so the joint optimum is just the two separate optima. That is a fine result and worth one sentence. But the
  heading "One design for both", the phrase "is extended", and the button "Motor + suspension (one LQR)" suggest a single joint
  solve that couples the two. The only coupling is (B3), which is not an LQR term. State this plainly.
- **Skipped step: Q, N, R from (B2).** "Because a_z contains u, the cost has a cross term". Correct, but the reader must build Q, N
  and R alone. One line: write a_z = C**y** + Du with C = (−k, −c, c, 0)/M_s and D = 1/M_s. Then
  Q = CᵀC/a²_max + diag(1/s²_max, 0, 0, 1/d²_max), N = CᵀD/a²_max, R = D²/a²_max + 1/u²_max. This is exactly what `suspGains`
  does.
- **The Riccati equation and u = −K_s y are set inline.** At 390 px they wrap across four lines, with "= −K_s y" alone at the
  start of a line. The K_s vector runs to the column edge, and its ";" wraps by itself. This is a key equation and should be a
  numbered display.
- K_s = (−502.6, 11.6, −6.1, 612.6). Re-solved with SciPy from the code's matrices: (−502.60, 11.64, −6.09, 612.88). Poles
  −4.94 ± 4.98j (1.116 Hz, ζ = 0.704) and −31.98 ± 259.9j (41.68 Hz, ζ = 0.122). These all agree, except that the last gain is
  612.9, not 612.6. That is the page's Riccati-flow stopping tolerance, 0.04 %. Either print 612.9 or name the gap.
- "the active force cancels 84 % of the spring". **Skipped sign step.** With u = −K_s y and K₁ = −502.6 N/m, u = +502.6 s
  pushes the parts apart as the stroke grows, against the spring's −600 s. The net is 97 N/m, and √(97/1.927)/2π = 1.13 Hz,
  which is the 1.1 Hz body pole above. That one-line check ties two numbers the reader otherwise takes on trust.
- "while the tyre-load term keeps the wheel on the road". No mechanism is given. **S** cannot see how +612.6 N/m on d does that.
  One clause: when the tyre is squeezed more than at rest, the actuator eases off the axle, and when it unloads, the actuator
  pushes the axle down onto the road.
- "d_max = 0.2 mm (the tyre's static compression is 1.1 mm; a swing of its size unloads the tyre and the drive loses its grip)".
  (a) "Swing" here means an oscillation of the tyre's compression. In this note "swing" means the stout's slosh, so the word is
  ambiguous. (b) The reason given supports 1.1 mm, not 0.2 mm. Why one fifth? The next sentence half answers (d_max = 1 mm let
  the wheel leave the setts 2.6 % of the time), but it does not give the joint design's own airborne fraction with the final
  weights. The runs give it: setts 0.9 %, washboard 0 %. Quote those.
- "The weights were chosen by measurement: a_max = 0.2 m/s² with d_max = 1 mm held the heave lower but ... the lean there grew."
  Grew from what to what? No numbers and no command.
- **Model limit not stated.** A stroke of 41.6 mm (slosh feedback, washboard) is more than the spring's static compression of
  31.5 mm (§6.5), so the spring passes its free length. The model has no bump stops or rebound stops. A real suspension would hit
  them. One clause.
- (B3) Verified: −β·(b/M_x)·i_par = +ω²(a_z/g) q̂, which cancels the parametric term when q̂ = q. **G:** "exact" holds only in
  continuous time with the true q. The current follows the command with the drive's 2 ms lag τ_i (§7, (34)), a_z is sampled
  every 1 ms, and i_par is clipped by the 3 A drive limit. Say "exact in the model, up to the drive's lag and limit".
  i_par also pushes the cart along x, so it disturbs the speed (which the integral then fights) and modes 2 and 3. Neither side
  effect is mentioned.
- "The Kalman filter of section 8.5 uses the same model: its A_d is recomputed every sample with ω²(1 + a_z/g)". **This
  contradicts §8.5**, which says "The heave is left out of (K3) ... which the filter does not track." Both are true, in
  different modes (the code passes a_z to the filter only when `ctrl === 'joint'`). One of the two sentences must say "except
  in the joint design (§8.6)". Also, is Q_d recomputed too, or only A_d and B_d? The data panel recomputes A_d and B_d. Say
  which.

### "Does it work?" and Table 3b

- "the slosh feedback alone fails: the spring resonates, its stroke reaches 23 mm rms ... (11.1 mm rms with no controller at
  all)". **The most striking fact of the section is left unexplained.** The motor controller doubles the spring's stroke compared
  with doing nothing. The runs show the same at 0.7 m/s (7.5 → 14.2 mm) and 1.0 m/s (13.9 → 19.0 mm). This contradicts the
  previous paragraph ("no current changes the body's height"). It also contradicts the later claim "the motor alone leaves the
  spring as it was", which holds on the bumps but not on the washboard. **G** wants the mechanism. Plausibly: in open loop the
  cart's speed swings over the ripples (§6.7 says so), which smears the excitation frequency. A controller that holds the speed
  steady holds the ripple frequency exactly on the 2.8 Hz bounce. Whatever the cause, it needs a sentence and ideally a
  measurement.
- "the stout leans 103 mm and 75 g spill". **Unflagged: outside the model.** §11.9 "Where it stops" and §6.7 say the live model
  stops being valid at breaking, a wall amplitude of 21.2 mm (lean 42 mm), and that past it "the spills are the model's, not the
  stout's". 103 mm is 2.5 times past that. The 3D solver gives 32 mm. "Agrees in kind, not in size" is fair, but the reason for
  the factor of 3 (the reduced model is beyond its range) should be stated, not left for the reader to find.
- **Comparison missing:** in this run the slosh feedback (103 mm, 75 g) is *worse than no controller at all* (50.0 mm, 42 g in
  `springs-nm-washboard.txt`; §6.7 states "more than open loop's 42 g"). The 3D run also has an open-loop line (63 mm, 31 g)
  that the note leaves out. A reader of §8.6 alone does not learn that the controller makes things worse.
- "The 3D solver ... with the joint design ... the lean 5.4 mm, a little more than with the skyhook (3.8 mm)." Look at the table
  as a whole. On every road the plain skyhook of §9 does as well as the joint design (washboard 1.1 against 1.0 mm). In 3D it
  does better (3.8 against 5.4 mm). Its stroke is similar, and on ISO D it is lower (3.46 against 3.86 mm). **The section never
  says what the joint design buys over "slosh + skyhook".** The runs suggest a lower heave (1.12 against 1.41 m/s²) and the
  tyre-load term. Say so. Otherwise the reader concludes the extra machinery is not needed, and the Key result's "one active
  force across the one suspension spring" is met by the simpler skyhook anyway.
- Table 3b also uses "skyhook" from §9, which comes *after* this subsection. Section order: the active suspension and its
  actuator are introduced in §9 (and as u_s in §6.3). §8.6 uses both before §9 explains them. Add "(section 9)" at the first
  mention of "active suspension", or move §8.6 after §9.
- "On every other road and speed the joint design leans no more than the motor alone, within 0.1 mm". True, and it undersells
  the result: at 0.7 and 1.0 m/s on the washboard the motor alone leans 1.5 and 3.0 mm, the joint 1.0 and 1.0 mm. ISO D's
  stroke rises with the joint design (3.53 → 3.86 mm rms, max 9.4 → 11.3 mm). The text only reports where stroke falls.
- Table 3b caption: "The reduced model of section 11.9 ... 6 s", but the last row is the 3D solver over 4 s. Split the caption
  or mark the row. Column heading "Slosh" in the table, "slosh feedback alone" and "the motor alone" in the text all mean the
  same controller. Use one name.
- The numbers I checked against the run files all match: 23.4/41.6/11.1 mm, 7.6 m/s², 9.7 %, 102.6 mm, 75.4 g; joint 6.96 mm,
  3.9 N, 1.12 m/s², 1.0 mm; 3D 28.2 mm, 19.1 %, 32.1 mm, 0.7 g, 6.99 mm, 5.4 mm, 3.8 mm; UMAX = 0: 125.8 mm/321 g,
  130.0 mm/168 g, 12.60 A.

### Key result box

- "Each needs its own actuator". **The section's own evidence says otherwise.** (B3) shows the motor *can* cancel the parametric
  channel's effect on the swing. The failure with u_max = 0 is a matter of size: 12.6 A asked against 3 A available. It is not
  a matter of structure. So "needs its own actuator" means "needs one with enough authority, because the motor's would have to be
  four times larger". Say that. It is a stronger and more honest statement.
- "and one each is enough". Supported only for the swing along the road, at linear order, on the roads tested. **G:** a single
  force between body and wheel cannot change the body's response at the tyre-only frequency √(k_t/m_w)/2π = 41.1 Hz (the
  quarter-car "invariant point"; Hedrick & Butsuen). That frequency is far above the slosh band, so "enough" holds where it
  matters, but the claim should name its band.
- "Mathematically the cart is a quarter car with two springs, the suspension and the tyre; neither more springs nor more motors
  are needed". **Non sequitur.** How many springs the cart has says nothing about how many actuators are needed. Either give the
  argument (one input per independent disturbance channel, from the controllability split) or drop the sentence.
- "A sideways push (a person's gait sways a cup sideways, section 15)". **Broken cross-reference.** §15 says nothing about gait,
  sideways sway or lateral motion. Its only related item is "swirl and any motion that breaks the mirror symmetry".
- **★ rule.** Standard, verdict of 21 October, point 4: results of a starred passage are restated unstarred. Nothing outside §8.6
  (not §13, not §14) mentions the joint design, yet the page has a button for it ("Motor + suspension (one LQR)"). A reader who
  skips ★ never learns what that button does. One unstarred sentence in §14, or in §8.4's closing paragraph, would fix this.

### Closing paragraph

- "130 mm and 168 g without the cancellation". **Uninterpreted, and against the grain:** without the suspension, the
  cancellation *doubles* the spill (321 g against 168 g). The likely reason is that (B3) saturates the 3 A drive and takes current
  the slosh LQR needed. One sentence.
- "The deeper question, whether to control the stout at all or to stop the road from reaching it, has the answer of the coffee
  carrier". This is a headline-style turn of the kind the 21 October verdict lists as an AI tell ("deeper question"). Plain form:
  "So the cart does what the coffee carrier does: both, each with the actuator that reaches its channel."
- Commands: `UMAX=0 node tools/fig12/springs.cjs nm washboard joint 0.85` and the `NOCANCEL=1` variant match the header lines
  of `notes/fig12/runs/springs-nm-nosusp.txt`.

---

## 2 · Verdict against notes/STANDARD.md

| # | Standard item | Verdict | Why |
|---|---|---|---|
| 1 | Physical picture from experience | **Needs work** | The coffee carrier is good, but the kerb half points the wrong way (a vertical push does nothing to a flat surface). Name the near free fall (g_eff → 0). There is no picture for why holding the speed makes the spring resonate. |
| 2 | Model stated, regime, numbers | **Needs work** | Flat-road condition for the block split not stated. Linearisation used for "not controllable" not separated from the bilinear truth. Ideal sensors of the suspension not stated. No bump stops. The reduced model is quoted at 2.5 times its breaking limit without a flag. |
| 3 | Derivation, every step | **Needs work** | ψ_mn undefined. sin mθ case skipped. Volume step missing. Suspension A, B never shown. Q, N, R from (B2) skipped. Sign step for "84 %" missing. (B3) verified correct. |
| 4 | Checks | **Partly met** | Poles, frequencies and damping ratios are consistent with K_s (verified). Add the one-line check 600 − 502.6 = 97 N/m → 1.13 Hz. No limiting case is given (for example u_max → 0 is given numerically, which is good). |
| 5 | Numerical method as code does it | **Needs work** | The page integrates the Riccati flow for K_s (explicit Euler, `suspGains`); the note does not say so, and the 612.6 vs 612.9 gap comes from it. The two LQRs are solved separately, not as "one LQR". The filter's heave-aware A_d contradicts §8.5. |
| 6 | Equation to screen | **Not addressed** | Nothing says where a_z, i_par, the stroke or u show on the figure or in the data panel, although the store holds `a_z_meas`, `i_par` and `y_s0`–`y_s3`. |
| 7 | Limits of the model | **Needs work** | Missing: bump stops, ideal sensors, linear-only controllability, the 41 Hz invariant point, reduced-model breaking. The sideways-channel remark points to a §15 that does not contain it. |
| 8 | Further reading | **Not met** | No source is cited for the controllability rank test, LQR with a cross term, feedback linearisation, or quarter-car active suspension LQR. Each is a standard textbook result and should carry one reference that was opened and read. |
| Form | Symbols, voice, ★ | **Needs work** | Eight symbol clashes (u, A, B, N, R, Q, d, s, **y**). Forward references to (54), (N4)–(N5) and §9. "Kalman test" next to the Kalman filter. One headline-style closing sentence. Joint design not restated outside ★. |
| Render | Layout | **Minor** | KaTeX clean. At 390 px the inline Riccati equation and K_s wrap badly; make them a numbered display. Nothing overflows. |

**Overall verdict for §8.6: needs work.** The numbers are right; every one I checked matches the stored runs or my
recomputation. The logic has three real gaps that a graduate would catch:

1. The two blocks split only on a flat road, through N z_a′.
2. "Not controllable from the suspension" is a linearisation statement. The real suspension can damp a swing parametrically.
3. The Key result says "needs its own actuator", but the section shows it is a matter of authority (12.6 A against 3 A).

A school student will also get lost at ψ_mn, at the unwritten suspension matrices, at the symbol clashes, and at the unexplained
fact that the motor controller doubles the spring's stroke on the washboard. Finally, the section does not show that the joint
design is better than the plain skyhook of §9 that its own table compares it with.
